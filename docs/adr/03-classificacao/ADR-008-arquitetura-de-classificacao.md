# ADR-008: Arquitetura de classificação (ensemble heterogêneo + verificador contrastivo)

**Status:** Aceito (código implementado em 15/10/2026; rodada completa das 359 em 17/10/2026)
**Data:** 14/10/2026 · revisada em 14/10/2026: componentes por papel, orçamento de prompt por provedor ([ADR-002](../00-fundacao/ADR-002-provedor-e-modelos-de-llm.md), revisão 2) · revisada em 15/10/2026: A no `codex` e verificador no `agy`, fora da cota do Claude Code
**Decisores:** Autor do case
**Fase:** 03-classificacao (passos 03, 05 e 06)
**Relacionadas:** ADR-002, ADR-004, ADR-005, ADR-007, ADR-009, ADR-010, ADR-011, ADR-013, ADR-017

## Contexto

- **Precisão mínima de 95% nas publicadas**, com o máximo de cobertura. Isso exige não só acertar, mas **saber quando se acertou**: a confiança precisa separar o certo do duvidoso.
- **Não há rótulos para treinar.** Um classificador supervisionado não é viável no case (em produção sim, ADR-016).
- **A árvore cabe no prompt dos modelos grandes.** São 351 nós publicáveis, ~18–20 mil tokens com o escopo de cada nó (ADR-007). Não é preciso recuperar candidatos antes de chamar o LLM.
- **O erro que custa caro é o irmão errado**, outro subtema do mesmo tema. Nem os títulos nem os sinais fracos separam bem esses casos.
- **Não há `temperature` nos modelos Claude atuais.** Concordância entre chamadas idênticas não mede nada; as fontes precisam ser diferentes.
- **Modelos por papel, de qualquer provedor** (ADR-002, revisão 2):
  - cada componente é um **papel**, e o modelo de cada papel é escolhido de acordo com a máquina e as credenciais (ADR-017);
  - A e B vêm de **famílias diferentes** sempre que possível.
- **Cada provedor tem um limite de prompt:** Ollama com 16 mil tokens de contexto; `agy` com o prompt inteiro como argumento (~120 KB); CLI `claude` com o prompt de sistema como argumento (~120 KB). Só as APIs têm cache de prompt.
- **Sinais fracos disponíveis:** leis citadas (93 questões) e assunto de origem (ADR-006).

## Decisão

Um **ensemble de fontes heterogêneas** seguido de um **verificador contrastivo**:

| Componente | Papel (ADR-002) | Nesta máquina (ADR-017) | Entrada | Saída |
|---|---|---|---|---|
| **A: plano** | `classificador_a` | GPT `gpt-6.1-sol` (CLI `codex`) | Texto canônico + árvore com escopo | Tema central, segundo colocado, extras, núcleo cobrado (1 frase), marcas `multitema` e `fora`, autoconfiança |
| **B: hierárquico** | `classificador_b` | Gemini 3.8 Flash `-low` (`agy`) | 1ª chamada: disciplina e tema (nível 1, com escopo). 2ª chamada: subtema, com os cartões dos filhos | Mesmos campos de A |
| **Voto barato** | `voto_barato` | GPT-OSS 120B `-medium` (CLI `agy`) | Texto canônico + árvore enxuta | Tema central |
| **Regras** | — (sem LLM) | — | Leis citadas → temas (`MapaLegislacao`) | Temas indicados |
| **Embeddings** | — (opcional, ADR-009) | — | Questão × cartões | Top-k |
| **Verificador** | `verificador` | Gemini 3.8 Flash `-medium` (CLI `agy`) | Questão + cartões do candidato, dos irmãos e do pai | "Candidato certo / irmão X / pai / nenhum", com justificativa |

**Orçamento de prompt por papel** (as três versões do material vêm da ADR-007):

| Papel | Material | Tamanho estimado | Ollama (16 mil) | `agy` (≤120 KB) | CLI `claude` | API |
|---|---|---|---|---|---|---|
| Classificador A | Árvore com escopo | ~18–20 mil tokens (~70 KB) | Não cabe | Cabe | Cabe (árvore vai pela entrada padrão) | Cabe, com cache |
| Classificador B | Temas de nível 1 com escopo; depois os cartões dos filhos | ~3–4 mil + ~1–3 mil | Cabe | Cabe | Cabe | Cabe |
| Voto barato | Árvore enxuta | ~9 mil com a questão | Cabe | Cabe | Cabe | Cabe |
| Verificador | Cartões do ramo | ~2–4 mil | Cabe | Cabe | Cabe | Cabe |

Regras de execução:

1. **Toda chamada passa pelo contrato `ProvedorLLM`.** O classificador recebe o provedor e o modelo do papel pelo `SeletorModelos`, nunca um SDK direto.
2. **Saída estruturada** com `enum` de IDs publicáveis. A resposta é validada contra o schema; se falhar, a chamada é repetida uma vez. Se falhar de novo, o papel fica sem voto e a questão tende a `revisar`.
3. **O prompt de cada papel respeita o limite do provedor escolhido.** O montador mede o tamanho e falha antes de chamar, em vez de truncar.
4. **O verificador roda só onde importa:** questões em que o consenso pode levar a `publicar` (consenso de ramo entre A, B e o voto barato). Não roda nas que já vão para `revisar`.
5. **Pergunta contrastiva:** o verificador não pergunta "isto está certo?", que tende a confirmar. Ele pergunta: "entre o candidato, cada irmão e o pai, qual descreve o núcleo cobrado?".
6. **Saída do passo:** uma linha por questão com todas as respostas e sinais, que alimenta a agregação (ADR-010, ADR-011) e a calibração (ADR-013). Cada voto registra o provedor e o modelo que o produziu.

## Opções consideradas

### Opção A: uma chamada de LLM por questão

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | 1 chamada por questão (~US$ 0,04 no perfil `claude-api`; cota ou zero em assinatura e local) |
| Efeito na régua | Acerto razoável, mas a confiança autodeclarada é mal calibrada; difícil escolher o limiar |
| Prazo | Rápido |

**Prós:** simples; é o "razoável em minutos" que o enunciado cita.
**Contras:** sem evidência independente para separar certo de duvidoso; o case diz que "razoável não serve".

### Opção B: ensemble heterogêneo + verificador contrastivo (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Custo | 4–5 chamadas por questão (~US$ 0,08 no perfil `claude-api`, ADR-002; sem custo marginal em assinatura e local, pagando em tempo) |
| Efeito na régua | Positivo: concordância entre fontes diferentes é um bom preditor de acerto; o verificador ataca o erro entre irmãos |
| Prazo | Compatível (quinta e sexta) |

**Prós:** cada fonte é auditável; a confiança vem de evidência, não de autodeclaração; famílias diferentes em A e B.
**Contras:** mais peças; as CLIs são lentas e variáveis (rodadas completas precisam de paralelismo).

### Opção C: agente com ferramentas (busca na árvore, leitura de leis, várias rodadas)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Alta |
| Custo | Alto e variável |
| Efeito na régua | Incerto; mais difícil de calibrar e reproduzir |
| Prazo | Arriscado |

**Prós:** flexível em questões difíceis.
**Contras:** a árvore já cabe no prompt, então não há o que buscar. Um agente não melhora a decisão central e piora a auditoria. As CLIs `claude` e `agy` são agentes, mas aqui rodam sem ferramentas, só como modelo.

### Opção D: classificador supervisionado (embeddings + regressão)

**Prós:** barato e calibrável.
**Contras:** sem rótulos no case. Fica para produção, treinado com as revisões dos professores (ADR-016).

## Análise de trade-offs

A régua mede precisão **nas publicadas**, então o que mais vale é separar bem o certo do
duvidoso. A opção B produz exatamente esse tipo de evidência:

- concordância entre modelos de **famílias** e prompts diferentes;
- concordância com regras independentes;
- um teste dirigido ao erro mais caro, o irmão errado.

Com a revisão 2 da ADR-002, o risco de erros correlacionados caiu: A e B não são mais da
mesma família (nesta máquina, Claude × Gemini, e o voto barato é Qwen). O risco que sobra é
o viés comum dos prompts, reduzido pelas estruturas diferentes (A plano, B hierárquico) e
pelas regras e embeddings, que não são LLM. O tamanho do efeito é medido nos experimentos
E2, E3 e E5 (ADR-014).

O custo deixou de ser só dinheiro. Com assinaturas e modelo local, o preço é **tempo**:
- pelas latências do teste (4–30 s por chamada nas CLIs, ~7 s no modelo local), uma rodada completa leva **~4–7 h** em sequência;
- com paralelismo limitado por provedor, **~1,5–2 h**;
- são estimativas, a confirmar na primeira rodada.

A opção C só valeria se a árvore não coubesse no contexto.

## Consequências

- O passo 05 gera ~1.100 respostas por rodada, e o passo 06 algumas centenas; todas ficam em cache (ADR-003), com provedor e modelo na chave.
- O modelo local pequeno participa só como voto barato, com a árvore enxuta. Ele não comporta a árvore com escopo nem tem qualidade para classificador principal nesta máquina.
- Trocar o provedor de um papel não muda o classificador, só a configuração (`config/escolha_modelos.json`).
- A agregação recebe sinais ricos o bastante para recuar ao pai (ADR-010) e para forçar revisão (ADR-011).
- Em produção, a mesma arquitetura vira cascata: fontes baratas primeiro (ADR-016).

## Implementação (15/10/2026)

- **Modelos por papel, fora da cota do Claude Code.** A CLI `claude` divide a cota com a sessão de
  trabalho; numa rodada de cartões ela se esgotou e 35 chamadas falharam. Por isso:
  - A passou para o GPT `gpt-6.1-sol` pela CLI `codex` (novo provedor `codex-cli`, assinatura do ChatGPT);
  - o verificador passou para o Claude Opus 5.5 `-medium` pela CLI `agy` e, quando a cota do `agy`
    para modelos não Gemini acabou, para o Gemini 3.8 Flash `-medium` (mesma família de B: risco
    aceito e medido; D8);
  - o voto barato passou do `qwen3.5:4b` local para o GPT-OSS 120B pelo `agy`. Nesta GPU, o modelo local
    gera ~2 tokens/s (~34 s por questão, ~3,4 h por rodada, uma chamada por vez); o GPT-OSS leva ~20 s,
    com 3 em paralelo. É um modelo aberto, o equivalente auto-hospedável da camada barata em produção (ADR-016);
  - A (GPT), B (Gemini), voto (GPT-OSS) e verificador (Claude) vêm de modelos diferentes; o verificador não é da família de A.
  - A escolha está congelada em `config/escolha_modelos.json`.
- **Verificador sem favorito:** recebe os cartões do candidato, do pai, dos irmãos, dos filhos, dos
  nós sugeridos pelas fontes e do par de sobreposição de outra disciplina, em ordem da árvore, **sem
  saber qual é o candidato**. O veredito (confirma, pai, filho, irmão, outro, nenhum) sai da relação
  entre a escolha e o candidato.
- **Candidato preliminar:** A e B válidos e no mesmo ramo; vale o mais específico dos dois. Se os dois
  marcam `fora`, o verificador confere o tema de A e pode responder "nenhum". Sem isso, o
  verificador não roda e a questão tende a `revisar` (ADR-011).
- **Classificador B:** a 2ª etapa só roda se o tema escolhido tiver subtemas; a autoconfiança final é
  o produto das duas etapas.
- **Resposta inválida:** repetida uma vez como tentativa 2 (outra chave no cache, ADR-003); se falhar
  de novo, o papel fica sem voto, com o erro registrado.
- **Limites:** o `MontadorPrompt` mede o prompt de cada chamada contra o provedor (argumento de CLI no
  `agy`, contexto no Ollama) e falha antes de chamar. A CLI `claude` recebe o prompt de sistema por
  arquivo e o `codex`, pela entrada padrão.
- **Gold cego:** as questões do gold ainda sem rótulo ficam de fora da rodada
  (`adiar_gold_pendente`). Elas entram numa execução depois de rotuladas, e o resto vem do cache.
- **Item 5 (contexto por papel no recomendador):** não feito. Com a escolha congelada, a proteção
  que importa é a checagem do montador a cada chamada.

## Itens de ação

1. [x] `prompts/classificador_plano.md`, `prompts/classificador_hierarquico_tema.md`, `prompts/classificador_hierarquico_subtema.md`, `prompts/voto_barato.md`, `prompts/verificador.md`.
2. [x] `vicio_ia/classificacao/schemas.py` (em vez de `vicio_ia/llm/schemas.py`): schemas JSON (com `enum` de IDs) gerados a partir de `temas.json`.
3. [x] `vicio_ia/classificacao/classificadores.py` (`ClassificadorPlano`, `ClassificadorHierarquico`, `VotoBarato`): contrato comum `Classificador.classificar(questao) -> RespostaClassificador`; provedor e modelo do papel via `SeletorModelos`.
4. [x] `vicio_ia/classificacao/montador_prompt.py`: monta o prompt de cada papel com a versão certa do material (ADR-007) e checa o limite do provedor antes de chamar.
5. [ ] (adiado) `ParametrosLLM`: contexto necessário **por papel** (hoje um valor único de 16 mil), para o recomendador avaliar cada papel com o tamanho real do seu prompt.
6. [x] `ProvedorClaudeCLI`: o prompt de sistema vai sempre por arquivo (`--system-prompt-file`), sem limite de argumento.
7. [x] `vicio_ia/sinais/regras.py`: `SinalLegislacao` (reusa `MapaLegislacao`, só IDs válidos).
8. [x] `vicio_ia/classificacao/verificador.py`: `VerificadorContrastivo`.
9. [x] `vicio_ia/classificacao/pipeline.py` e `executar_classificacao.py`: gera `dados/classificacao/sinais.jsonl` (uma linha por questão com tudo, incluindo provedor e modelo de cada voto), com paralelismo limitado por provedor.
10. [x] Teste de fumaça em 10 questões **fora** do gold (15/10): 100% de respostas válidas; latência média de A 8,6 s, B 29 s, verificador 14–30 s e voto barato ~20 s (GPT-OSS) ou 34 s (`qwen3.5:4b`, que saiu).
11. [x] Rodada completa das 359 questões (17/10): A, B e voto barato nas 359; verificador nas 325 candidatas.
