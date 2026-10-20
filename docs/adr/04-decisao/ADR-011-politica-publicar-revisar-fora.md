# ADR-011: Política de decisão publicar / revisar / fora

**Status:** Aceito (implementado em 15/10/2026: `vicio_ia/decisao/`, `executar_decisao.py`)
**Etapa 2:** A política é revista pelas ADR-023 (fora e multitema) e ADR-025 (limiar).
**Data:** 14/10/2026 · revisada em 15/10/2026: duplicados publicados no canônico, lixeiras em dois níveis, desempate das sobreposições (ADR-005, `decisoes_manuais.md` D1–D3)
**Decisores:** Autor do case
**Fase:** 04-decisao (passo 07)
**Relacionadas:** ADR-005, ADR-008, ADR-010, ADR-012, ADR-013, ADR-015

## Contexto

- **Os custos são assimétricos.** Publicar errado é o erro mais caro: o aluno estuda a matéria errada. Revisar custa tempo do professor, que é escasso. `fora` tira a questão do recorte.
- **A régua é uma restrição dura.** Ficar abaixo de 95% nas publicadas provavelmente pesa mais do que qualquer ganho de cobertura. A escolha do limiar precisa considerar a **incerteza da estimativa**, não só o valor pontual.
- **Zonas de risco conhecidas** (EDA, ADR-005):
  - nós duplicados (dependem da convenção);
  - 15 pares de sobreposição;
  - 21 possíveis lixeiras;
  - 18 enunciados genéricos, que podem cobrir vários temas;
  - questões de jurisprudência (47).
- **Formato do `publicacao.csv`** (LEIA-ME): uma linha por questão; `tema_central_id` obrigatório em `publicar` e `revisar` e vazio em `fora`; `confianca` de 0 a 1; `motivo` obrigatório em `revisar` e `fora`.

## Decisão

Decisão em **quatro etapas**, aplicadas na ordem:

**1. Fora**
- `fora` quando as duas fontes principais (A e B) marcam que nenhum tema serve e o verificador confirma "nenhum". Exemplo: Q0142, isenção de ITCD (Tributário).
- Se só parte das fontes marca `fora`: `revisar` com motivo "possível fora do recorte".
- `disciplina_origem` não decide `fora` (ADR-006).

**2. Candidato consolidado**
- Consenso de ramo entre A, B, o voto barato e as regras, seguido do recuo para o pai (ADR-010). Resultado: o candidato `c` e o nível em que ficou.

**3. Regras que forçam `revisar`, qualquer que seja a probabilidade**

| Situação | Motivo no CSV |
|---|---|
| `c` está num grupo de sobreposição e a regra de desempate não resolve (as fontes divergem entre nós do grupo) | "sobreposição: X × Y" |
| `c` é lixeira **forte** sem concordância total e sem verificador favorável | "tema genérico sem evidência suficiente" |
| A e B em ramos diferentes | "dúvida entre X e Y" |
| Verificador discorda do candidato | "verificador sugere X" |
| Pelo menos duas fontes marcam multitema e o enunciado é genérico | "questão cobre vários temas: X; Y" |
| Recusa ou resposta inválida de algum modelo | "falha de classificação" |

O que **não** força revisão (decisões D1 e D3, ADR-005):
- **Nós duplicados:** a questão é publicada no nó canônico, porque os fantasmas nem são candidatos. O risco de o especialista ter usado a cópia vai para a margem de convenção da previsão (ADR-013).
- **Lixeiras moderadas:** entram só como variável de risco na calibração.

**4. Limiar calibrado**
- Para as questões restantes, usar a probabilidade calibrada `P(c certo)` (ADR-013).
- O limite inferior usado no critério já inclui a margem de convenção (ADR-013). Assim, publicar num nó da zona de convenção "custa" margem, e o limiar escolhido exige mais confiança justamente onde o risco de convenção é maior.
- Ordenar por `P` e publicar o maior conjunto em que o **limite inferior (percentil 10 do bootstrap) da precisão estimada fique em 95% ou mais**. Na prática, a estimativa pontual vai mirar ~97%.
- O resto vai para `revisar`, com motivo "baixa confiança (P = 0,xx)".
- **Por que estimativa por modelo:** o critério usa a precisão **estimada pelo modelo**
  (média da `P` calibrada das publicadas, com bootstrap), não a contagem direta no gold.
  Com ~40 publicadas no gold, a contagem direta nunca passa de 0,937 no limite inferior,
  nem com 40 acertos em 40 (ADR-012).
- **Regra de reserva:** se nenhum conjunto atingir limite inferior de 95%, publicar o
  maior conjunto com **estimativa pontual de 97% ou mais** (2 pontos de margem) e
  informar no `previsao.txt` o intervalo como ele é.

**Colunas**
- `confianca`:
  - em `publicar` e `revisar`: `P(c certo)` calibrada;
  - em `fora`: a probabilidade estimada de `fora` estar certo. Essa leitura está documentada e incluída nas perguntas para a Carla.
- `extras_ids`: temas de outro ramo indicados por pelo menos duas fontes, no máximo 3. Para questões recuadas, os subtemas candidatos.
- `motivo`: modelos de texto fixos, curtos, com IDs, que o professor entende sem abrir o código.

## Opções consideradas

### Opção A: limiar sobre a autoconfiança de um modelo

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | Nenhum |
| Efeito na régua | Arriscado: a autoconfiança de LLM é mal calibrada |
| Prazo | Imediato |

**Prós:** simples.
**Contras:** sem base para escolher o limiar nem para prever a precisão.

### Opção B: regra fixa de votação (unanimidade + verificador → publicar)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | Nenhum |
| Efeito na régua | Boa precisão provável; cobertura possivelmente baixa |
| Prazo | Imediato |

**Prós:** fácil de explicar ao professor; não precisa de muitos dados para calibrar.
**Contras:** não usa a gradação da evidência; o limiar não é otimizado.

### Opção C: regras duras + probabilidade calibrada + limiar pelo limite inferior (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Custo | Nenhum além do gold (ADR-012) |
| Efeito na régua | Melhor equilíbrio: protege a régua e maximiza a cobertura dentro dela |
| Prazo | Compatível (sábado) |

**Prós:** cada `revisar` tem um motivo legível; o limiar segue diretamente a régua.
**Contras:** depende da qualidade da calibração. Com gold pequeno, o intervalo fica largo e o limiar, conservador.

## Análise de trade-offs

A opção C coloca o risco onde ele é medido. As regras duras tiram das publicadas os casos
em que a **convenção** é desconhecida, coisa que nenhuma calibração no nosso gold
consegue medir, porque o gold é rotulado por nós, não pelos especialistas. O limiar pelo
limite inferior troca um pouco de cobertura por segurança, o que combina com custos
assimétricos.

**Plano B:** se a calibração ficar instável (gold pequeno ou pouco variado), usamos a
opção B, com a precisão dela medida no gold, e documentamos a troca.

## Consequências

- O `publicacao.csv` é gerado por uma função determinística dos sinais em cache: muda uma regra, roda de novo, compara.
- O professor recebe uma fila de revisão em que cada item explica por que está ali, o que vira material para o memo.
- A Carla deixou a convenção dos duplicados a critério do autor (15/10/2026); a regra correspondente saiu da etapa 3. As demais perguntas (como `fora` é avaliado, `confianca` em `fora`) seguem a opção conservadora até haver resposta. Cada mudança fica registrada aqui com a data.

## Implementação (15/10/2026)

- Etapas 1 a 3 em `AgregadorSinais` (`vicio_ia/decisao/agregacao.py`), na ordem da decisão, com os
  motivos fixos da tabela. A ação preliminar é `candidata`, `revisar` ou `fora`.
- Etapa 4 em `PrevisorPrecisao` (`vicio_ia/avaliacao/previsao.py`): bootstrap da calibração, limite
  inferior (percentil 10) menos as margens de convenção e de ambiguidade, e a regra de reserva de 97%.
- `PipelineDecisao` grava `publicacao.csv` e `previsao.txt` em `relatorio/` (`Caminhos.entregaveis`), depois de um validador do formato do
  LEIA-ME: 359 linhas, IDs únicos, tema publicável, `fora` sem tema, motivo em `revisar` e `fora`,
  confiança em [0, 1] e extras válidos.
- `confianca` em `fora`: a confiança do verificador em "nenhum" (D9).

## Itens de ação

1. [x] Etapas 1 a 3 (fora, candidato e regras que forçam revisão) em `AgregadorSinais` (`vicio_ia/decisao/agregacao.py`, 15/10).
2. [x] Etapa 4 (limiar calibrado) em `PrevisorPrecisao` (`vicio_ia/avaliacao/previsao.py`); motivos e extras em `PipelineDecisao` (15/10).
3. [x] `vicio_ia/decisao/pipeline.py` e `executar_decisao.py`: gera o `publicacao.csv` a partir de `sinais.jsonl` e da calibração, com validador do formato (15/10; testado de ponta a ponta numa pasta temporária).
4. [x] Testes unitários dos motivos (`testes/teste_politica.py`: fora, falhas, verificador em outro ramo, sobreposição, multitema, concordância e faixas) e das colunas obrigatórias do `publicacao.csv` (`testes/teste_publicacao.py`), 17/10.
5. [ ] Comparar no gold as opções B e C (curva precisão × cobertura) antes de escolher a final (ADR-014).
