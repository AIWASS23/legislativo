# ADR-007: Cartões de tema

**Status:** Aceito (código e rascunhos em 15/10/2026; revisão manual não feita antes do congelamento: D7, D11)
**Data:** 14/10/2026 · revisada em 14/10/2026: modelos por papel e limites de prompt por provedor ([ADR-002](../00-fundacao/ADR-002-provedor-e-modelos-de-llm.md), revisão 2)
**Decisores:** Autor do case
**Fase:** 02-temas (passo 02)
**Relacionadas:** ADR-002, ADR-005, ADR-008, ADR-016, ADR-017

## Contexto

- **Quase nenhum tema tem definição de verdade.** Dos 373 nós abaixo das disciplinas, 333 têm só o texto-modelo ("Subtema de X. N questões no source"), 20 não têm descrição e só 20 têm descrição com conteúdo jurídico (EDA, seção 11). Na prática, o título é a única definição de cada tema.
- **Títulos sozinhos não separam irmãos parecidos.** Exemplos: "Conceitos e Espécies de Prisão" × "Prisão Preventiva" × "Medidas Cautelares Diversas da Prisão" (essa última com 0 questões na origem), ou "Ação Penal" em Penal × em Processo Penal. O erro que a régua pune é justamente escolher o irmão errado.
- **Só a disciplina ou o tema certo não basta.** O professor precisa revisar *definições*, não 359 questões.
- **Os modelos são escolhidos por papel, e cada provedor aceita um tamanho de prompt** (ADR-002, revisão 2):
  - o Ollama roda com contexto de 16 mil tokens, e o `qwen3.5:4b` só cabe inteiro na GPU até ~9,5 mil;
  - a CLI `agy` recebe o prompt como argumento (limite de ~120 KB);
  - só os provedores de API têm cache de prompt.

## Decisão

Gerar um **cartão por tema publicável** (351 nós), com estes campos:

| Campo | Conteúdo |
|---|---|
| `tema_id`, `caminho`, `titulo_exibicao` | Identificação |
| `escopo` | 1–2 frases: o que o tema cobre |
| `inclui` | Assuntos e institutos típicos |
| `nao_inclui` | O que parece mas pertence a outro nó, com o ID dele (ex.: "prisão preventiva → 5519") |
| `ancoras_legais` | Leis e artigos de referência (CP, CPP, leis especiais) |
| `regra_desempate` | Só para nós em grupo de sobreposição ou lixeira (ADR-005) |

Processo:

1. **Rascunho por LLM, com o modelo do papel verificador** (maior qualidade disponível; nesta máquina, Claude Opus 5.5 pela CLI `claude`).
   - Entrada: o nó, o caminho, os irmãos, o pai e a descrição, quando existe. Saída estruturada.
   - Uma chamada por tema pai, cobrindo todos os filhos de uma vez, para que o `nao_inclui` aponte para os irmãos.
   - A chamada passa pelo contrato `ProvedorLLM` (ADR-002), nunca pelo SDK direto.
2. **Revisão humana, priorizada:** os 21 nós de lixeira, os 15 pares de sobreposição e os irmãos do mesmo tema com títulos parecidos. Os demais têm revisão amostral.
3. **Três versões do material, para caber em qualquer provedor:**

| Versão | Conteúdo | Tamanho estimado | Usada por (ADR-008) |
|---|---|---|---|
| Árvore enxuta | ID + caminho de cada nó publicável | ~7,5 mil tokens | Voto barato (cabe no contexto do Ollama) |
| Árvore com escopo | ID + caminho + `escopo` de cada nó | ~18–20 mil tokens (~70 KB) | Classificador A |
| Cartões completos por ramo | Todos os campos dos filhos de um tema, ou do candidato, dos irmãos e do pai | ~1–4 mil tokens por chamada | Classificador B (etapa do subtema) e verificador |

4. **Outros usos:** embeddings (ADR-009) e o memo para o professor, como o material que ele valida.
5. **Medição:** o experimento E4 (ADR-014) compara classificar com títulos e com cartões no gold.

## Opções consideradas

### Opção A: só os títulos (e as 20 descrições existentes)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Nenhuma |
| Custo | Nenhum |
| Efeito na régua | Negativo em irmãos parecidos e sobreposições |
| Prazo | Imediato |

**Prós:** sem trabalho; sem risco de o LLM inventar escopo.
**Contras:** o modelo decide sozinho a fronteira entre irmãos, de forma implícita e sem como auditar.

### Opção B: cartões gerados por LLM e revisados por prioridade (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Custo | ~50 chamadas do modelo verificador (uma por tema pai): sem custo marginal por assinatura ou local; ~US$ 3–5 no perfil `claude-api`; mais 2–3 horas de revisão |
| Efeito na régua | Positivo esperado nas zonas de erro; medido pelo E4 |
| Prazo | Compatível (quinta-feira) |

**Prós:** as fronteiras ficam explícitas e revisáveis; o mesmo material serve ao classificador, ao verificador e ao professor.
**Contras:** um cartão errado propaga o erro. Por isso a revisão prioriza as zonas de risco.

### Opção C: cartões escritos à mão do zero

**Prós:** máxima confiabilidade.
**Contras:** 351 cartões não cabem no prazo; exige saber Direito Penal a fundo.

## Análise de trade-offs

A opção B concentra o esforço humano onde a régua pune: lixeiras, sobreposições e irmãos
parecidos. O risco de cartão errado é controlado de dois jeitos: pela revisão e pelo E4,
que mostra no gold se os cartões ajudam ou atrapalham. Se atrapalharem, voltamos aos
títulos e registramos o resultado como beco sem saída.

Entregar o material em três versões custa pouco (é o mesmo conteúdo recortado) e evita
que a escolha do provedor quebre o pipeline. Um modelo local pequeno não comporta a árvore
com cartões, mas comporta a árvore enxuta; o verificador só precisa do ramo.

## Consequências

- O prompt de cada papel tem tamanho conhecido e cabe nos limites do provedor escolhido. A ADR-008 define qual versão vai para cada papel.
- Nos provedores de API, a árvore fica num prefixo estável, com cache de prompt. Nas CLIs e no Ollama não há cache, e o tamanho do prompt pesa no tempo e, no `agy`, nos tokens.
- Os cartões viram um entregável à parte (`dados/temas/cartoes.jsonl`) e a base da recomendação ao professor: "valide estas definições" (memo).
- Em produção, os cartões são o contrato entre a taxonomia e o classificador (ADR-016).

## Implementação (15/10/2026)

- `uv run python executar_cartoes.py`: **58 chamadas**. São 7 para os temas de nível 1 (as
  disciplinas com mais de 16 temas divididas em blocos) e 51 para os subtemas, uma por tema pai.
  - O prompt de sistema traz a árvore enxuta inteira, para o `nao_inclui` apontar para qualquer nó.
  - A tarefa traz o nó, a descrição (quando existe), os subtemas, a marca `[conceitual]` e a regra D2 de sobreposição.
  - Saída estruturada com `enum` dos IDs.
  - Se faltar algum cartão, a chamada é repetida uma vez.
- **Modelo fixo para os cartões** (Claude Opus 5.5 pela CLI `claude`, `ParametrosCartoes`), e não o
  do papel verificador. Trocar o verificador (o que aconteceu em 15/10, ADR-008) não invalida no
  cache os rascunhos já gerados.
- **Ajustes manuais** em `dados/temas/cartoes_ajustes.csv` (`tema_id,campo,valor,motivo`),
  aplicados sobre os rascunhos. Os rascunhos ficam em `cartoes_gerados.jsonl`, e os finais, em
  `cartoes.jsonl`, que só é gravado se as 6 checagens passarem:
  - um cartão por tema publicável;
  - `nao_inclui` só com temas publicáveis e sem o próprio nó;
  - escopo preenchido e curto;
  - `inclui` não vazio;
  - regra de desempate nas lixeiras fortes e nas sobreposições.
- **Revisão priorizada** em `saidas/cartoes/revisao_cartoes.md`: lixeiras fortes, sobreposições (com
  a regra D2 ao lado), irmãos com títulos parecidos e os demais.
- **Versões do material** (`MaterialArvore`): enxuta, com escopo (`dados/temas/arvore_escopo.txt`),
  nível 1 com escopo e subtemas (B, etapa 1), cartões dos filhos (B, etapa 2) e cartões do ramo
  (verificador). O tamanho de cada uma fica em `saidas/cartoes/relatorio_cartoes.md`.

## Itens de ação

1. [x] `prompts/cartao_tema.md`: prompt de geração.
2. [x] `vicio_ia/temas/gerador_cartoes.py`: `GeradorCartoes`, uma chamada por tema pai, com cache (ADR-003), via `ClienteLLM`.
3. [x] `vicio_ia/temas/revisao.py` e `cartoes.py`: caderno de revisão por prioridade; ajustes manuais reimportados do CSV.
4. [ ] Revisar à mão as lixeiras, as sobreposições e os irmãos parecidos; registrar em `decisoes_manuais.md` (D7). Não coube antes do congelamento; está no memo, como pedido ao professor, e na lista "com mais tempo" do relatório.
5. [x] `vicio_ia/temas/arvore_prompt.py`: as versões do material com bytes estáveis, com o tamanho de cada uma.
