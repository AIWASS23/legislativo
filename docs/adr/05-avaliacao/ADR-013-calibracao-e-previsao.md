# ADR-013: Calibração da confiança e previsão de precisão e cobertura

**Status:** Aceito (implementado em 15/10/2026; o intervalo de cobertura supõe avaliação nas 359)
**Etapa 2:** A calibração e a previsão são revistas pela ADR-025.
**Data:** 14/10/2026 · revisada em 15/10/2026: margem de convenção por tipo de risco (ADR-005, `decisoes_manuais.md` D1) · em 17/10/2026: estimador direto suavizado (D12)
**Decisores:** Autor do case
**Fase:** 05-avaliacao (passo 08)
**Relacionadas:** ADR-005, ADR-008, ADR-010, ADR-011, ADR-012

## Contexto

- **O `previsao.txt` pede** precisão e cobertura previstas, cada uma com intervalo, e uma explicação de como se chegou aos números. A banca compara com o resultado real.
- **A confiança alimenta o limiar.** A coluna `confianca` precisa ser uma probabilidade **calibrada**, porque a política de decisão escolhe o limiar a partir dela (ADR-011).
- **Os dados para calibrar são poucos:** ~120 questões rotuladas (ADR-012), 60 de desenvolvimento e 60 da zona de publicação.
- **Há incertezas que nenhuma amostra nossa mede:**
  - a convenção dos especialistas (duplicados, sobreposições);
  - se a banca avalia as 359 questões ou um subconjunto ("as questões que guardamos").

## Decisão

**1. Calibração.** Regressão logística com regularização L2 (scikit-learn) sobre **poucas variáveis**, todas vindas dos sinais (ADR-008):

| Variável | Valores |
|---|---|
| `concordancia_ramo` | Número de fontes (A, B, voto barato, regras) no ramo do candidato: 0–4 |
| `veredito_verificador` | confirma / pai / irmão / nenhum / não rodou |
| `autoconfianca_media` | Média da autoconfiança de A e B |
| `nivel_publicado` | Subtema ou tema (recuo) |
| `zona_risco` | Lixeira forte ou moderada, enunciado genérico ou jurisprudência |
| `origem_mesmo_ramo` | O assunto de origem cai no ramo do candidato (sinal fraco, ADR-006) |

- Avaliação por **validação cruzada estratificada com 5 partes** no gold: Brier, log-loss e curva de confiabilidade.
- Depois do congelamento, ajuste final com o gold inteiro.
- Se a regressão ficar instável, usar uma tabela de faixas (concordância × verificador) com as taxas observadas e suavização de Beta.

**2. Previsão de precisão**

- **Estimador direto:** proporção de acertos (régua estrita) entre os itens do gold que caem na zona publicada, com peso pelo desenho amostral.
- **Estimador por modelo:** média da `P` calibrada das publicadas nas 359.
- **Ponto:** o estimador direto, se houver 40 ou mais itens do gold publicados. Senão, a média dos dois.
  O direto entra com a suavização de Jeffreys no tamanho efetivo de Kish, `(acertos + 0,5) / (n + 1)`, como as faixas da calibração (D12, 17/10): 13 acertos em 13 dão 0,964, não 1,000.
- **Intervalo de 90%:**
  - **bootstrap completo** com 1.000 reamostras: reamostrar o gold, reajustar a calibração, refazer o limiar e recalcular a precisão. Usar os percentis 5 e 95;
  - o limite inferior é **alargado por duas margens**, que cobrem o que o gold não mede:
    - **(a) ambiguidade do rótulo:** precisão tolerante menos precisão estrita no gold (ADR-012);
    - **(b) convenção dos especialistas:** `m = Σ_t (publicadas no tipo t / publicadas) × p_t`, com o `tipo_convencao` do tema publicado (ADR-005) e taxas de discordância **supostas**: `duplicado_outra_disciplina` 20%, `sobreposicao` 10%, `duplicado_parte` 3%.
  - O tipo de convenção **não** entra como variável da calibração: o gold é rotulado com a nossa convenção, então não consegue aprender esse risco.
  - Por que essas taxas: a cópia em outra disciplina é um lugar plausível para o especialista; a sobreposição tem regra de desempate; um nó "(Parte N)", sem filhos nem descrição, é improvável para quem classifica pelo conteúdo.
  - As taxas ficam configuráveis, e o `previsao.txt` mostra a sensibilidade (taxas × 0, × 1 e × 2).
- **Por que o modelo pesa tanto:** com ~40 publicadas no gold, a contagem direta tem
  intervalo de ~10 pontos e não certifica 95% no limite inferior (ADR-012). O estimador
  por modelo usa todas as questões rotuladas e por isso é a base do limiar
  (ADR-011). A contagem direta serve de checagem e entra no ponto.
- **Checagem:** a precisão de cada faixa é conferida fora da amostra (validação cruzada) e mostrada no gráfico de confiabilidade.

**3. Previsão de cobertura**

- **Ponto:** número de publicadas dividido por 359, um valor exato.
- **Intervalo:**
  - se a avaliação for nas 359: só arredondamento (±0,01);
  - se for num subconjunto de tamanho desconhecido: tratar como amostra aleatória e usar o intervalo binomial, assumindo m ≈ 180 (metade). A hipótese é declarada no texto.

**4. `previsao.txt`.** As quatro linhas do formato do LEIA-ME, seguidas de uma explicação em linguagem simples: o gold, a calibração, a incerteza, a margem de convenção, a hipótese da cobertura e o que **não** foi medido.

## Opções consideradas

### Opção A: precisão = taxa de acerto observada no gold, intervalo de Wilson

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | Nenhum |
| Efeito na previsão | Ignora a incerteza do limiar e da convenção; intervalo estreito demais |
| Prazo | Imediato |

**Prós:** simples, fácil de explicar.
**Contras:** otimista; não propaga a escolha do limiar; e, com o tamanho do gold, não
separa bem os casos. 39 de 40 dá 0,90–0,99 e 40 de 40 dá 0,94–1,00 no IC de 90%.

### Opção B: calibração isotônica sobre um escore composto

**Prós:** sem hipótese de forma funcional.
**Contras:** com ~120 pontos produz degraus e sobreajusta; precisa de mais dados.

### Opção C: logística com poucas variáveis + bootstrap completo + margem de convenção (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Custo | Nenhum (scikit-learn já no ambiente) |
| Efeito na previsão | Intervalo honesto: propaga amostra, limiar e convenção |
| Prazo | Compatível (sábado) |

**Prós:** cada componente da incerteza aparece e pode ser explicado.
**Contras:** intervalo largo. Isso é um custo aceitável, porque um intervalo estreito e errado pesa mais na avaliação.

## Análise de trade-offs

A avaliação compara a previsão com o resultado. Um intervalo estreito que erra é pior do
que um intervalo largo e honesto. O bootstrap completo é o único jeito de propagar a
incerteza do **limiar** (que depende da própria calibração). A margem de convenção cobre
o erro sistemático que o gold não vê.

A logística com poucas variáveis é o modelo de maior viés e menor variância que ainda
usa a gradação da evidência. É a escolha certa para ~120 pontos.

## Consequências

- O limiar da ADR-011 e a previsão saem do mesmo procedimento, então são coerentes por construção.
- O relatório ganha um gráfico de confiabilidade e a curva precisão × cobertura, que também servem de explicação para leigos.
- A Carla deixou a convenção dos duplicados a critério do autor: a margem (b) fica como cenário declarado, com taxas supostas e análise de sensibilidade. Se a cobertura for medida num subconjunto (pergunta ainda sem resposta), o intervalo de cobertura usa a hipótese binomial.

## Implementação (15/10/2026)

- `vicio_ia/avaliacao/calibracao.py`:
  - regressão logística L2 implementada com `numpy` (IRLS, intercepto sem penalidade), porque o
    `scikit-learn` não tem tipos e o projeto exige `mypy --strict`; testada com dados sintéticos;
  - 7 variáveis: concordância de ramo, verificador confirma, verificador no mesmo ramo, recuo,
    autoconfiança média, zona de risco e origem no mesmo ramo;
  - pesos pelo inverso da probabilidade de inclusão;
  - validação cruzada estratificada com 5 partes (Brier, log-loss, faixas de confiabilidade).
- `vicio_ia/avaliacao/previsao.py`:
  - limiar e previsão como na decisão; o ponto já desconta a margem de convenção;
  - o intervalo usa o limiar fixo nas reamostras (D9);
  - a sensibilidade ×0/×1/×2 vai para o `previsao.txt`.
- O ajuste usa todas as questões do gold com tema que não são `fora` (candidatas e revisões), para
  aproveitar os 60 exemplos do gold.

## Revisão de 16/10/2026 (D10)

- **Faixas no lugar da regressão**, que ficou instável: só 6 erros em 60, e o Brier ficou igual ao de um
  palpite constante. O pipeline escolhe pela menor log-loss na validação cruzada entre as faixas e uma grade
  de penalidades da regressão; as faixas venceram (0,287 × 0,312).
- **Chance efetiva:** P × (1 − taxa de convenção do nó) ordena as candidatas e vai para `confianca`. Assim,
  o risco de convenção pesa questão por questão, e não barra uma faixa inteira (ADR-011).
- **Corte só entre faixas**; pesos amostrais com tamanho efetivo de Kish.
- **Margem de ambiguidade fora do critério do limiar** (ADR-011): ela só alarga o intervalo informado.

## Limite assumido (17/10/2026)

- A calibração e a previsão usam o gold de 60 questões.
- A previsão foi calibrada e conferida no mesmo gold, com validação cruzada; não houve teste numa amostra
  independente. O `previsao.txt` e o relatório dizem isso.
- Com 28 acertos em 28 na faixa de consenso, só os nós sem risco de convenção passam no critério de 95%.

## Itens de ação

1. [x] `VetorizadorDecisao` (em `vicio_ia/avaliacao/calibracao.py`, 15/10): 7 variáveis a partir da decisão preliminar.
2. [x] `vicio_ia/avaliacao/calibracao.py`: `RegressaoLogisticaL2` (IRLS em `numpy`) e `Calibrador` (validação cruzada estratificada, faixas de confiabilidade) (15/10). A tabela de faixas com suavização de Beta, prevista como alternativa, não foi feita.
3. [x] `vicio_ia/avaliacao/previsao.py`: `PrevisorPrecisao` (estimadores, bootstrap, margens de rótulo e de convenção por tipo, sensibilidade, cobertura) (15/10).
6. [x] `ParametrosCalibracao.taxas_convencao` (20% / 10% / 3%), configuráveis (15/10).
4. [x] `previsao.txt` (formato do LEIA-ME e explicação) gravado por `PipelineDecisao` e conferido por `ValidadorEntrega` (15/10).
5. [x] Gráficos de confiabilidade e de precisão × cobertura (no gold e nas 359) em `saidas/avaliacao/`, com `graficos.md` trazendo as mesmas informações em tabela (`executar_graficos.py`, 17/10).
