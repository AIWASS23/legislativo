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

## Congelamento (2026-10-17T14:55:52)

Recongelamento em 17/10: o ponto da precisão prevista usa o estimador direto com a suavização de Jeffreys da calibração (D12): 13 acertos em 13 dão 0,964, e o ponto passa de 0,99 para 0,97. O limiar, as 81 publicadas, a coluna confianca e o intervalo não mudaram; nenhum prompt, cartão, regra de decisão ou modelo mudou.

34 arquivos com impressão digital em `saidas/experimentos/congelamento.json`. A partir
daqui, nenhum prompt, cartão, regra, modelo ou parâmetro de decisão muda.

## Congelamento (2026-10-17T15:13:28)

Recongelamento em 17/10, sem efeito nas decisões: publicacao.csv e previsao.txt passam a ser gravados e validados em relatorio/ (Caminhos.entregaveis), junto com o relatório. Conferido: os dois arquivos saem idênticos, byte a byte, aos que estavam na raiz.

34 arquivos com impressão digital em `saidas/experimentos/congelamento.json`. A partir
daqui, nenhum prompt, cartão, regra, modelo ou parâmetro de decisão muda.

---

# Etapa 2: pré-registro dos experimentos (20/10/2026, antes de rodar)

Base: a folha-verdade (100 questões rotuladas pela equipe; 92 com tema, 8 fora). Régua da etapa 2: acerta
quem publica no tema central, num extra, ou no pai ou filho de um deles; questão fora publicada é sempre erro.
Tudo o que tiver parâmetro aprendido é medido fora da amostra (validação cruzada estratificada, 5 partes,
10 repetições; ADR-024). Nenhum experimento usa resposta de LLM sobre questão (ADR-019).

- **E7. Só lexical (BM25 contra os documentos de tema).** Hipótese: o BM25 acerta o tema no top-1 bem menos
  que o LLM da etapa 1 (88% na folha), mas tem recall@10 alto o bastante para gerar candidatos. Variantes:
  documento só com título e caminho; documento com o cartão. Métricas: acerto no top-1 (nas 100 e nas 92),
  recall@5 e @10 nas 92. Sem parâmetro aprendido: medido direto na folha.
- **E8. Só embeddings; escolha do modelo de embedding** (ADR-021). Hipótese: supera o E7 no top-1 e no recall.
- **E9. Só kNN na folha.** Hipótese: ajuda nos temas frequentes, não cobre os temas sem exemplo.
- **E10. Ranqueador completo × soma ponderada sem treino** (ADR-022). Hipótese: o treino com a folha melhora
  a log-loss e o acerto no top-1.
- **E11. Separabilidade do "fora"** (ADR-023). Hipótese: a dispersão entre as alternativas e a margem do
  melhor candidato separam as questões fora (AUC fora da amostra ≥ 0,7). Se não separarem, vale o plano B
  da ADR-023. Métricas: AUC de cada atributo, com intervalo de 90% por bootstrap; AUC fora da amostra de uma
  logística com 2 ou 3 atributos.
- **E12. Deriva entre as questões antigas e as novas** (ADR-024). Hipótese: as novas têm distribuição
  diferente de similaridade e margem; se tiverem, o intervalo da previsão para elas é alargado.

## E7. Só lexical: resultado (20/10)

Arquivos: `saidas/etapa2/experimentos_etapa2.md`, `resultados_etapa2.csv` e `e7_ranking_folha.csv`.

| Documento do tema | Top-1 (92 com tema) | Recall@5 | Recall@10 | Top-1, central nível 1 | Top-1, central nível 2 |
|---|---:|---:|---:|---:|---:|
| Título e caminho | 47/92 (51%) | 76% | 86% | 29/53 | 18/39 |
| Com o cartão | 62/92 (67%) | 92% | 93% | 43/53 (81%) | 19/39 (49%) |

- **Hipótese confirmada.** No top-1, o BM25 fica bem abaixo da sugestão do LLM da etapa 1 (88% na folha).
  Mas o recall@10 de 93% basta para gerar os candidatos do ranqueador.
- **Os cartões valem 16 pontos no top-1** e ficam no documento de tema (ADR-020).
- **O erro se concentra nos subtemas** (49%). É ali que a escolha do nó pela régua (ADR-022) deve render.

## E11. Separabilidade do fora, só com atributos lexicais: resultado (20/10)

- **AUC de cada atributo isolado,** com intervalo de 90%:

  | Atributo | AUC | Intervalo |
  |---|---:|---|
  | Pontuação máxima baixa | 0,67 | 0,52–0,80 |
  | Margem baixa | 0,63 | 0,43–0,79 |
  | Dispersão entre as alternativas | 0,59 | 0,41–0,77 |
  | "(Parte N)" no assunto de origem | 0,58 | 0,44–0,73 |

  O enunciado genérico e a disciplina de origem fora do recorte ficam em ~0,5, porque nenhuma questão fora
  da folha tem essas marcas.
- **Logística com os três primeiros atributos, fora da amostra:** AUC de 0,54 (0,35–0,72).
- **Decisão:** com atributos lexicais, o fora **não é separável** (abaixo do limite de 0,7 pré-registrado).
  - Repetir com embeddings e kNN (E8, E9) antes de acionar o plano B da ADR-023.
  - Se continuar inseparável, só se publica onde a folha mostrar uma taxa de fora compatível com 95%.

## E8 e E9: pré-registro detalhado (20/10, antes de rodar)

- **Candidatos do E8:** cinco modelos multilíngues de embedding, todos pelo Ollama local, sem custo e sem
  PyTorch no projeto: `bge-m3` (o padrão da ADR-021), `qwen3-embedding:0.6b`, `qwen3-embedding:4b`,
  `snowflake-arctic-embed2` e `granite-embedding:278m`. O `multilingual-e5-large` via sentence-transformers
  ficou de fora, porque traria o PyTorch; não há crédito de API de embedding.
- **Entrada:** a questão inteira (enunciado, comando e alternativas) contra o mesmo documento de tema do E7
  (título, caminho e cartão). Os prefixos de consulta seguem a recomendação de cada modelo.
- **Métricas:** as do E7 (acerto no top-1 nas 100 e nas 92; recall@5 e @10 nas 92; top-1 por nível). Não há
  parâmetro aprendido, então a medição é direta na folha.
- **Regra de escolha:** vence o maior recall@10 do denso nas 92, porque o papel dos embeddings é gerar
  candidatos para o ranqueador. Diferença de até uma questão é empate, decidido pelo maior acerto no top-1;
  persistindo o empate, vale a ordem da lista acima.
- **Medido junto, sem entrar na regra:** a fusão BM25 + denso por posição recíproca (RRF, k = 60), para saber
  se os dois sinais se complementam.
- **E9:** kNN deixa-uma-fora entre as 100 questões da folha (k = 10 vizinhos; cada vizinho com tema vota no
  central e nos extras, com o peso da similaridade), com os vetores de cada candidato. Também é medido o teto:
  quantas das 92 têm o tema certo entre os temas de outra questão da folha.

## E8. Escolha do modelo de embedding: resultado (20/10)

Arquivos: `saidas/etapa2/e8_embeddings.md` e `e8_resultados.csv`. Comando: `uv run python executar_embeddings.py`.

| Variante (92 com tema) | Top-1 | Recall@5 | Recall@10 | Top-1, nível 1 | Top-1, nível 2 |
|---|---:|---:|---:|---:|---:|
| BM25 com cartão (E7, referência) | 67% | 92% | 93% | 81% | 49% |
| `bge-m3`, denso | 66% | 86% | 91% | 72% | 59% |
| `qwen3-embedding:0.6b`, denso | 66% | 88% | 93% | 74% | 56% |
| **`qwen3-embedding:4b`, denso** | **79%** | **97%** | **98%** | 92% | 62% |
| `snowflake-arctic-embed2`, denso | 70% | 88% | 92% | 77% | 59% |
| `granite-embedding:278m`, denso | 57% | 80% | 88% | 68% | 41% |
| `qwen3-embedding:0.6b`, BM25 + denso (RRF) | 80% | 95% | 97% | 92% | 64% |
| `qwen3-embedding:4b`, BM25 + denso (RRF) | 79% | 98% | 99% | 91% | 64% |

- **Vencedor pela regra pré-registrada:** `qwen3-embedding:4b`, com recall@10 de 98% (90 de 92) e top-1 de
  79% (73 de 92). É o único modelo que, sozinho, supera o BM25 no top-1 e no recall, o que confirma a hipótese
  do E8 para ele. O `bge-m3`, padrão provisório da ADR-021, fica abaixo do BM25.
- **Os sinais se complementam:** a fusão por posição recíproca melhora todos os modelos menores. Com o
  `qwen3-embedding:4b`, ela leva o recall@10 a 99%, e o top-1 fica igual.
- **Custo:** os 3.478 vetores (659 questões, 2.604 alternativas e 351 temas) levaram 488 s na GPU de 6 GB,
  contra 99 s do `qwen3-embedding:0.6b`. A fase de decisão só lê os `.npy`, então não precisa de GPU.
  - **Plano B:** se o tempo de geração pesar na produção, o `qwen3-embedding:0.6b` com fusão chega perto do
    4b (top-1 de 80% e recall@10 de 97%).
- **Exportação:** `dados/conhecimento/embeddings/` (36 MB, dimensão 2560, `float32`), com o digest
  `df5bd2e3c74c` e o hash dos textos no `modelo.json` e no manifesto. Conferido que a leitura do artefato,
  com a trava `VICIO_SEM_LLM=1` e a rede bloqueada, reproduz o top-1 de 73 de 92.

## E9. kNN na folha: resultado (20/10)

- **Teto:** 77 das 92 questões com tema (84%) têm o tema certo entre os temas de outra questão da folha. As
  outras 15 não podem ser acertadas por kNN.
- **kNN deixa-uma-fora, k = 10:** o top-1 fica entre 28% e 37% conforme o modelo, e o recall@10, entre 68% e
  77% (77% com o `qwen3-embedding:4b`).
- **Hipótese confirmada:** sozinho, o kNN fica muito abaixo do denso contra os documentos de tema, porque a
  folha cobre só 61 temas. Ele entra no ranqueador como atributo (a similaridade com o vizinho rotulado mais
  próximo de cada tema candidato), e não como fonte principal de candidatos.
