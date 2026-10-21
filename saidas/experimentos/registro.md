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

## Pré-registro: documento de tema final (E7b, E8b), E11b e E12 (21/10, antes de rodar)

**E7b e E8b. Documento de tema final** (`dados/conhecimento/temas.jsonl`, ADR-020).
- **Variantes do texto do tema:**
  - `cartao`: título, caminho, escopo, o que entra e âncoras legais. É o documento atual, do E7 e do E8.
  - `cartao_termos`: o anterior mais os termos `forte` e `fraco` do tema (revisados ou não; os `exclui`
    ficam de fora porque falam de outro nó, como o `nao_inclui`).
  - `cartao_termos_leis`: o anterior mais as referências do mapa revisado, por extenso ("CP, arts. 121 a 128").
- **As questões da folha não entram no texto do tema,** porque as métricas são medidas nelas. A base guarda só
  os IDs como exemplos, para o kNN (que é deixa-uma-fora).
- **Medição:** BM25 (E7b) e denso com o `qwen3-embedding:4b`, o modelo já escolhido no E8 (E8b), com as
  métricas do E7.
- **Regra, separada para o BM25 e para o denso:**
  - vence o maior recall@10 nas 92;
  - até uma questão de diferença é empate, decidido pelo top-1;
  - persistindo o empate, vence a variante mais simples.

**E11b. Separabilidade do fora com embeddings e kNN** (ADR-023), nas 100 da folha (8 fora).
- **Atributos densos, todos com o `qwen3-embedding:4b`:**
  1. similaridade máxima com os temas publicáveis (baixa indica fora);
  2. margem entre o 1º e o 2º tema (baixa indica fora);
  3. dispersão entre as alternativas: ramos de nível 1 distintos entre os melhores temas de cada alternativa,
     sobre as alternativas;
  4. similaridade com os temas inativos (5078 e 5234) menos a similaridade máxima com os publicáveis (alta
     indica fora);
  5. kNN deixa-uma-fora: similaridade com a questão fora mais parecida menos a similaridade com a questão com
     tema mais parecida (alta indica fora).
- **Também medido:** quantas das 8 fora têm uma regra forte (artigo no mapa ou termo `forte`).
- **Logística fora da amostra,** com os atributos 1, 3 e 5 escolhidos agora e a mesma validação cruzada do
  E11.
- **Critério:** separável se a AUC fora da amostra for ≥ 0,7. Se não for, vale o plano B da ADR-023: P(fora)
  igual à taxa da folha, e só se publica onde a folha mostrar taxa de fora compatível com 95%.

**E12. Deriva entre antigas e novas** (ADR-024).
- **Grupos:** as 259 antigas avaliadas (fora da folha) contra as 300 novas.
- **Atributos sem rótulo:**
  - similaridade densa máxima, margem densa, dispersão densa e BM25 máximo;
  - presença de artigo citado, tamanho em tokens e formato certo/errado;
  - disciplina de origem e disciplina do melhor tema denso.
- **Medida:** a AUC "nova × antiga" de cada atributo numérico, com intervalo de 90% por bootstrap, e as
  proporções dos categóricos.
- **Critério:** há deriva se, na similaridade máxima ou na margem, o intervalo da AUC excluir 0,5 e
  |AUC − 0,5| ≥ 0,1. Havendo deriva, a previsão das novas é alargada (ADR-025), e a cobertura é informada
  separadamente para antigas e novas.

## E7b e E8b. Documento de tema final: resultado (21/10)

Arquivos: `saidas/etapa2/experimentos_etapa2.md` (E7b) e `saidas/etapa2/e8_embeddings.md` (E8b).

| Variante (92 com tema) | BM25: top-1 | BM25: recall@10 | Denso (`qwen3-embedding:4b`): top-1 | Denso: recall@10 |
|---|---:|---:|---:|---:|
| `cartao` (o documento do E7 e do E8) | 67% | 93% | 79% | 98% |
| `cartao_termos` | **73%** | **97%** | 84% | 98% |
| `cartao_termos_leis` | 73% | 97% | **86%** | **98%** |

- **BM25:** vence `cartao_termos`. Os dois documentos com termos empatam (89 de 92 no recall@10 e 67 de 92 no
  top-1), e o desempate vai para o mais simples.
- **Denso:** vence `cartao_termos_leis`. O recall@10 empata nos três (90 de 92), e o top-1 sobe de 73 para 79
  questões; nos subtemas, de 62% para 72%.
- **Os termos revisados são o maior ganho da base de conhecimento:** +6 pontos no top-1 do BM25 e +5 no denso.
  As referências legais por extenso somam mais 2 pontos no denso.
- **Configuração:** `ParametrosSistema.documento_tema_bm25 = "cartao_termos"` e
  `ParametrosEmbeddings.documento_tema = "cartao_termos_leis"`. Os vetores dos temas foram exportados de novo
  com esse documento, junto com os dos 2 temas inativos.

## E11b. Fora com embeddings e kNN: resultado (21/10)

Arquivo: `saidas/etapa2/e11b_e12.md`.

| Atributo (8 fora × 92 com tema) | AUC | Intervalo de 90% |
|---|---:|---|
| Similaridade máxima baixa | 0,74 | 0,58–0,88 |
| Margem densa baixa | 0,61 | 0,48–0,73 |
| Dispersão densa entre as alternativas | 0,61 | 0,43–0,78 |
| Tema inativo perto do melhor tema | 0,83 | 0,73–0,91 |
| kNN: mais perto de fora que de tema | 0,54 | 0,40–0,68 |
| Sem regra forte | 0,57 | 0,45–0,70 |
| **Logística pré-registrada** (atributos 1, 3 e 5), fora da amostra | **0,61** | 0,42–0,78 |

- **Decisão, pelo critério pré-registrado:** o fora **não é separável** (AUC fora da amostra de 0,61, abaixo
  de 0,7). Vale o plano B da ADR-023:
  - P(fora) fica igual à taxa da folha, Beta(8,5; 92,5);
  - só se publica onde a folha mostrar taxa de fora compatível com 95%.
- **As regras fortes não protegem do fora:** 6 das 8 questões fora têm artigo no mapa ou termo `forte`.
- **Achado exploratório, fora da regra:** a proximidade com um tema inativo, isolada, chega a uma AUC de 0,83.
  - Ela não entrou na logística pré-registrada e foi medida em só 8 positivos, então não muda a decisão.
  - Ela já está prevista como regra na ADR-023 (decisão 2, "tema inativo"). Entra como sinal de `revisar`, que
    só pode custar cobertura, e não precisão. O limiar será escolhido na validação cruzada do ranqueador.
- **O kNN não ajuda no fora:** as questões fora da folha não se parecem entre si.

## E12. Deriva entre antigas e novas: resultado (21/10)

| Atributo (259 antigas avaliadas × 300 novas) | AUC nova × antiga | Intervalo de 90% | Medianas (antigas → novas) |
|---|---:|---|---|
| Similaridade máxima | 0,58 | 0,54–0,62 | 0,699 → 0,718 |
| Margem densa | 0,51 | 0,47–0,56 | 0,035 → 0,037 |
| Dispersão densa | 0,49 | 0,45–0,53 | 0,40 → 0,40 |
| BM25 máximo | 0,49 | 0,45–0,53 | 43,8 → 43,6 |
| Tamanho em tokens | 0,40 | 0,36–0,44 | 251 → 210 |

- **Decisão, pelo critério pré-registrado:** **não há deriva.**
  - Na similaridade máxima, o intervalo exclui 0,5, mas o efeito (|0,58 − 0,5| = 0,08) fica abaixo de 0,1.
  - Na margem, não há diferença.
  - O intervalo da previsão das novas não é alargado por deriva. A cobertura continua informada em separado
    para antigas e novas (ADR-024).
- **A diferença está no rótulo de origem, não no conteúdo:**
  - as novas usam "Direito Penal" no lugar de "Penal" e "Legislação Especial" (variação total de 0,19);
  - a disciplina do melhor tema denso quase não muda (0,06);
  - as novas são mais curtas (mediana de 210 tokens, contra 251), citam artigo um pouco menos (12% contra
    17%) e têm um pouco mais de certo/errado (20% contra 17%).
- **10 novas são de direito militar,** sem nó na árvore. Ficam com a regra de fora da ADR-023.

## E10. Ranqueador: logística × gradient boosting: pré-registro (21/10, antes da grade)

**Exploração anterior.** Antes deste registro, quatro configurações de boosting foram exploradas na folha, numa
pasta temporária e fora do sistema:
- (profundidade 2, folha mínima 20, 100 iterações): log-loss 0,411;
- (3, 20, 200): 0,404;
- (3, 10, 300): 0,417;
- (sem limite, 15, 200): 0,423.

Duas delas, (2, 20, 100) e (3, 20, 200), também foram simuladas de ponta a ponta. Por isso a grade abaixo é
fixada agora e medida inteira, e o resultado da exploração não decide sozinho.

- **Configurações:**
  - a referência: logística L2 (penalidade 10, o sistema atual);
  - 8 de `HistGradientBoostingClassifier` (scikit-learn, o mesmo algoritmo do LightGBM): profundidade máxima 2
    ou 3, folha mínima 10 ou 20 e 100 ou 200 iterações, com taxa de aprendizado 0,05, regularização L2 1,0 e
    semente 0.
- **Base:** os mesmos 18 atributos, os mesmos candidatos e a mesma validação cruzada (5 partes × 10
  repetições). O kNN usa só as questões de treino de cada partição.
- **Métricas:**
  - log-loss fora da amostra do nó escolhido nas 100 da folha (o critério);
  - acerto do nó;
  - acertos e fora entre as 20, 30 e 50 de maior confiança.
- **Regra (ADR-024):**
  - vence a menor log-loss;
  - uma diferença menor que 0,005 é empate, decidido pela configuração mais simples, na ordem: logística,
    depois profundidade, folha mínima maior e menos iterações.
- **Consequência:**
  - o vencedor vira o ranqueador do `executar_sistema.py`, com o resto do sistema igual (calibração, limiar
    D15 e regras);
  - se a logística vencer, nada muda;
  - todas as configurações ficam no relatório do E10.

## E10. Ranqueador: resultado (21/10)

Arquivo: `saidas/etapa2/e10_ranqueador.md` (todas as 9 configurações).

| Configuração (folha, fora da amostra) | Log-loss | Acerto (100) | Topo 50: certas (fora) |
|---|---:|---:|---:|
| Logística L2 (referência) | 0,433 | 81 | 45 (3) |
| Boosting: as 8 configurações | 0,400–0,412 | 76–79 | 47–49 (1–2) |
| **Boosting, profundidade 2, folha ≥ 20, 200 árvores** (vencedor) | 0,403 | 77 | 48 (1) |

- **Regra:** a menor log-loss é 0,400 (profundidade 3, folha ≥ 10, 100 árvores). Três configurações ficam a
  menos de 0,005 dela, e o desempate vai para a mais simples.
- **Hipótese:** pré-registrada assim: "o treino melhora a log-loss e o acerto no top-1". **Confirmada em parte.**
  - Todas as 8 configurações de boosting melhoram a log-loss.
  - O acerto geral piora (77, contra 81).
  - A ordenação do topo melhora em todas: as árvores empurram as questões fora para baixo, e só a Q0087 continua
    no topo.
- **Decisão:** o boosting vencedor vira o ranqueador do sistema (`ParametrosSistema.ranqueador`).
  - **Efeito:** com a mesma regra da D15, o sistema passa de 16 para **97** publicadas entre as 559 (17%), com
    previsão de 0,95 (0,90–0,99).
  - **Escolha do autor:** manter essa versão (D15).
- **Tempo:** o `executar_sistema.py` passa de 6 s para cerca de 45 s. A saída continua igual byte a byte entre
  execuções, inclusive com uma thread só.

## Explorações depois do E10 (21/10): gold, origem e antitemas

Nenhuma mudou o sistema. Ficam registradas, como pede a ADR-024.

- **Gold do autor como medida secundária** (`saidas/etapa2/gold_secundario.md`, ADR-024, decisão 6):
  - as 7 questões do gold que a entrega publica estão todas certas;
  - o tema sugerido está certo em 41 das 46 avaliadas do gold;
  - com confiança ≥ 0,80, as 26 estão certas;
  - a convenção do autor bate com a da equipe em 12 de 14;
  - nenhuma das 46 é fora.
- **Gold no treino** (as 46 sempre no treino, com medição só na folha): log-loss de 0,397, contra 0,403, e acerto
  de 79, contra 77. O topo é idêntico (19, 29 e 48 entre as 20, 30 e 50 de maior confiança).
  - **Não adotado:** a cobertura quase não mudaria, e o gold deixaria de ser a checagem independente da entrega.
- **Regra do assunto de origem** (o assunto de origem aponta um tema de outro ramo → revisar):
  - na folha, ela tira os 2 erros do topo, mas foi pensada a partir dessas mesmas questões fora;
  - no gold, o conflito aparece em 21 das 46, com 20 delas certas.
  - **Não adotada:** o conflito de origem não indica erro, e a regra inflaria a previsão por vazamento.
- **Antitemas** (10 descrições de áreas fora do recorte, escritas pelo assistente e não revisadas, em
  `dados/conhecimento/propostas/antitemas.csv`):
  - AUC de 0,60 nas 8 fora da folha, porque essas questões têm conteúdo do recorte;
  - nenhuma das 97 publicadas fica mais perto de um antitema que de um tema;
  - o antitema de direito militar é o mais próximo das 10 questões militares, confirmando pelo conteúdo a regra
    pela disciplina de origem.
  - **Não adotados:** não mudam a entrega. Ficam como proposta para a produção, em que a disciplina de origem pode
    não vir.

## Pré-registro: E13 (exemplos sintéticos), E10b (ranqueador por lista) e E14 (rotulagem ativa) (21/10)

- **E13. Exemplos sintéticos por tema** (ADR-021, decisão 6).
  - **Geração:** 3 questões-modelo por tema publicável, propostas pelo `codex-cli:gpt-6.1-sol` só a partir do tema
    (nenhuma questão real), sem revisão humana nesta medição.
  - **Uso medido:** dois atributos novos no ranqueador, com o boosting do E10: a similaridade máxima da questão
    com os exemplos do tema e com os exemplos do ramo, menos a similaridade máxima com os exemplos de qualquer
    tema.
  - **Critério:** o mesmo do E10 (log-loss do nó escolhido, fora da amostra). Adota-se só se a log-loss cair
    pelo menos 0,005 e o topo 50 não piorar.
- **E10b. Ranqueador por lista** (LambdaMART, `LGBMRanker` do LightGBM).
  - Mesmos candidatos, atributos e partições.
  - O escore do nó escolhido vira probabilidade por Platt, ajustado dentro de cada partição de treino.
  - **Critério:** o mesmo do E10, contra o boosting atual.
- **E14. Rotulagem ativa** (simulação, sem rotular nada da entrega).
  - **Curva de aprendizado na folha:** o sistema é treinado com 50, 70 e 85 das 100 questões (sorteio estratificado,
    5 repetições) e medido nas restantes. Medem-se a log-loss e o percentil 10 da precisão do topo, para
    extrapolar o ganho de 100 para 200 rótulos.
  - **Fila para a produção:** as 150 questões avaliadas mais úteis para rotular: as mais próximas do limiar e
    as de maior incerteza entre os candidatos.

## E10b. Ranqueador por lista (LambdaMART): resultado (21/10)

| Ranqueador (folha, fora da amostra) | Log-loss | Acerto (100) | Topo 20 / 30 / 50 | Fora no topo 50 |
|---|---:|---:|---|---:|
| Boosting atual (E10) | **0,403** | 77 | 19 / 29 / **48** | 1 |
| LambdaMART (profundidade 2, folha ≥ 20, 200 árvores) | 0,505 | 80 | 18 / 26 / 44 | 4 |
| LambdaMART (3, 20, 200) | 0,550 | 78 | 18 / 27 / 43 | 4 |
| LambdaMART (3, 10, 100) | 0,471 | 80 | 19 / 28 / 44 | 4 |

- **Não adotado.** O LambdaMART escolhe melhor o tema dentro da questão (80, contra 77), porque otimiza a ordem
  entre os candidatos.
- **O que piora:** a confiança entre questões, que é o que decide a publicação. A log-loss sobe, e o topo tem
  mais erros e mais questões fora.
- O LightGBM foi instalado só para o teste e não entra no `requirements.txt`.

## E14. Rotulagem ativa: resultado (21/10)

Arquivos: `saidas/etapa2/e14_rotulagem.md` e `saidas/etapa2/fila_rotulagem_ativa.csv` (150 questões).

| Rótulos no treino (folha) | Log-loss no teste | Acerto do nó |
|---:|---:|---:|
| 40 | 0,548 | 74% |
| 60 | 0,477 | 75% |
| 80 | 0,446 | 75% |

- **A log-loss ainda cai,** mas cada vez menos (−0,07 de 40 para 60, e −0,03 de 60 para 80). O acerto do nó
  estabiliza em 75%.
- **O ganho de mais rótulos vem da incerteza.** Com o dobro de rótulos, o intervalo da calibração estreita por cerca
  de √2.
  - Hoje, no conjunto publicado, o percentil 10 fica 0,028 abaixo do ponto. Com 200 rótulos, ficaria cerca de
    0,020 abaixo.
  - Com isso, o critério estrito (percentil 10 ≥ 95%) passaria a cobrir as cerca de 97 questões que hoje só a
    reserva pontual libera.
- **Para a produção (ADR-027):** a fila de rotulagem ativa são as 150 questões em `revisar` mais perto do limiar,
  em rodízio pelas disciplinas. Nada da entrega foi rotulado.

## E13. Exemplos sintéticos por tema: resultado (21/10)

- **Geração:** 1.053 questões-modelo (3 para cada um dos 351 temas), em 62 chamadas ao `codex-cli:gpt-6.1-sol`, sem
  falhas. A entrada só tinha os temas. Os vetores foram gerados com o `qwen3-embedding:4b`, com contexto de 1024.

| Variante (folha, fora da amostra) | Log-loss | Acerto (100) | Topo 20 / 30 / 50 | Fora no topo 50 |
|---|---:|---:|---|---:|
| Boosting (E10, 18 atributos) | 0,403 | 77 | 19 / 29 / 48 | 1 |
| **Boosting + exemplos (20 atributos)** | **0,363** | **82** | 19 / 29 / 48 | 2 |

- **Sozinhos, os exemplos não substituem o documento do tema** (E8c, só denso): o top-1 é de 76 de 92 com os
  exemplos, contra 79 de 92 com o documento.
- **Decisão pela regra pré-registrada: adotado.** A log-loss caiu 0,040, e o topo 50 não piorou.
- **Efeito no sistema** (mesma calibração, limiar D15 e regras):
  - **127** publicadas entre as 559 (22,7%), contra 97;
  - previsão de **0,96 (0,91–0,99)**, contra 0,95;
  - folha na faixa publicada: 24 certas em 25; pelo critério estrito, seriam 58 publicadas.
- **Gold (medida secundária):** 10 publicadas nas 46 avaliadas do gold, as 10 certas; tema sugerido certo em 42
  de 46.
- **O E10 não foi refeito com os 20 atributos.** A configuração do boosting continua a escolhida no E10.
