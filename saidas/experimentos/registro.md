# Registro dos experimentos (ADR-014)

Cada experimento: hipótese → resultado → decisão, inclusive quando a hipótese caiu. Os números
vêm de `resultados.csv`. Base de todos: gold set (60 questões rotuladas à mão).

- **Régua estrita:** só o tema que rotulamos (ou o pai ou um filho direto dele).
- **Régua tolerante:** vale também qualquer tema que o rotulador listou como plausível.
- **Cobertura a 95%:** a fração das 60 que daria para publicar com 95% de acerto, publicando primeiro
  as de maior confiança.

## E0. Assunto de origem como rótulo

- **Hipótese:** o assunto de origem das questões é um rótulo ruim.
- **Resultado:** publicar pelo assunto, quando ele aponta um único nó válido, acerta 12 de 33 (36%).
- **Decisão:** confirmada. O assunto de origem nunca entra no prompt; é só um sinal fraco (ADR-006).

## E2. Um modelo sozinho

- **Hipótese:** um LLM sozinho é "razoável, mas não publicável".
- **Resultado:** o classificador A (GPT `gpt-6.1-sol`) acerta 52 de 60 (87%); pela régua tolerante,
  59 de 60. Ordenado pela autoconfiança, chega a 67% de cobertura a 95%.
- **Decisão:** confirmada. 87% fica longe de 95%, e a autoconfiança não é calibrada: o modelo declara
  0,99 em respostas erradas.

## E3. Hierárquico × plano (e o voto barato)

- **Hipótese:** o classificador B (hierárquico) erra de forma diferente de A.
- **Resultado:**
  - B (Gemini Flash `-low`) acerta 52 de 60 (87%); pela régua tolerante, 60 de 60;
  - A e B erram juntos em 4 questões; se fossem independentes, seriam ~1;
  - o voto barato (GPT-OSS) acerta 30 de 60 (50%).
- **Decisão:** **parcialmente derrubada**. Os erros são correlacionados (questões difíceis para os dois).
  Mesmo assim, B fica no ensemble: a concordância de A, B e voto barato é o melhor separador que temos
  (ver E5). O voto barato sozinho é fraco, mas é um bom detector de dúvida: quando ele concorda com A e
  B, o gold não tem erros.

## E4. Cartões de tema × só títulos

- **Hipótese:** os cartões reduzem o erro entre irmãos.
- **Desenho:** feito com o classificador B, porque a cota de A é a mais escassa. Mesmo modelo, mesmos
  prompts; só muda o material.
- **Resultado:** com cartões, 52 de 60 (87%); só com títulos, 53 de 60 (88%). Cobertura a 95%: 78% com
  cartões, 62% sem.
- **Decisão:** **hipótese derrubada no acerto** (uma questão de diferença), mas os cartões melhoram a
  separação entre o certo e o duvidoso. Mantidos. Ressalva: 60 questões.

## E5. Pipeline completo × A sozinho

- **Hipótese:** ensemble, verificador e recuo aumentam a cobertura a 95%.
- **Desenho:** a P de cada questão do gold vem de um calibrador ajustado sem ela (validação cruzada).
- **Resultado** (régua estrita, mesmo número de publicadas):

  | Publicadas | Pipeline | A sozinho |
  |---:|---:|---:|
  | 28 | 28/28 | 27/28 |
  | 40 | 37/40 | 38/40 |
  | 50 | 47/50 | 46/50 |

- **Decisão:** "o ensemble acerta mais" foi **derrubada**: a precisão é a mesma em cada cobertura.
  "O ensemble sabe quando acertou" foi **confirmada**: a faixa de consenso total (verificador confirma e
  A, B e voto barato no mesmo ramo) tem 28 de 28 e é a única certificável. Daí a calibração por faixas (D10).

## Calibração (D10)

- **Hipótese:** uma regressão logística com 7 variáveis dos sinais dá a probabilidade de acerto.
- **Resultado:** com 6 erros em 60, a regressão empata com um palpite constante (Brier 0,089 × 0,090).
  As faixas de sinais com suavização de Jeffreys ganham na validação cruzada (log-loss 0,287 × 0,312).
- **Decisão:** a regressão foi **derrubada**; usamos as faixas. A regressão continua no código e entra se
  ganhar na validação cruzada.

## Pendentes

- **E6** (modelos por papel): não rodado, porque a cota das assinaturas foi o gargalo. A escolha por papel
  ficou ditada pelas cotas (D8).
- **E1** (embeddings): opcional, não rodado.

## Congelamento (2026-10-16T13:02:14)

Prompts, cartões (rascunhos do modelo, sem revisão manual: D7), regras de decisão (D9, D10), modelos por papel (D8) e parâmetros congelados antes da rodada final (decisão do autor, 16/10).

34 arquivos com impressão digital em `saidas/experimentos/congelamento.json`. A partir
daqui, nenhum prompt, cartão, regra, modelo ou parâmetro de decisão muda.

## Congelamento (2026-10-17T14:37:45)

Recongelamento em 17/10, sem efeito nas decisões: (1) os testes unitários entraram no portão de qualidade (ParametrosQualidade em configuracao.py); (2) o texto explicativo do previsao.txt foi corrigido (calibração por faixas e sorteios da Beta). Nenhum prompt, cartão, regra de decisão, parâmetro de calibração ou modelo mudou.

34 arquivos com impressão digital em `saidas/experimentos/congelamento.json`. A partir
daqui, nenhum prompt, cartão, regra, modelo ou parâmetro de decisão muda.


## Congelamento (2026-10-17T14:43:39)

Recongelamento em 17/10, sem efeito nas decisões: remoção de código sem uso e ordem estável dos extras_ids empatados (o conjunto de extras não muda; antes a ordem variava entre execuções, porque dependia da ordem de iteração de conjuntos). Conferido: duas execuções geram o mesmo publicacao.csv, byte a byte; em relação à execução anterior, só a ordem dos extras de 4 questões mudou.

34 arquivos com impressão digital em `saidas/experimentos/congelamento.json`. A partir
daqui, nenhum prompt, cartão, regra, modelo ou parâmetro de decisão muda.

## Congelamento (2026-10-17T14:45:39)

Recongelamento em 17/10, sem efeito nas decisões: só docstrings e mensagens (o gold set passou a ser descrito como uma amostra única).

34 arquivos com impressão digital em `saidas/experimentos/congelamento.json`. A partir
daqui, nenhum prompt, cartão, regra, modelo ou parâmetro de decisão muda.
