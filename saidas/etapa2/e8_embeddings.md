# E8 e E9: embeddings e kNN na folha-verdade

Gerado em 21/10/2026 09:58 por `uv run python executar_embeddings.py`. Base: as 100 questões da folha-verdade (92 com tema), com a régua da etapa 2. Documento de tema: título, caminho e cartão (o mesmo do BM25 no E7). A medição só usa vetores já gravados; nenhum modelo de linguagem decide nada.

## E8: questão inteira × documentos de tema

| Variante | Top-1 (92) | Recall@5 | Recall@10 | Top-1, nível 1 | Top-1, nível 2 |
|---|---:|---:|---:|---:|---:|
| BM25 com cartão (referência) | 67% (62/92) | 92% (85/92) | 93% (86/92) | 81% (43/53) | 49% (19/39) |
| bge-m3: denso | 66% (61/92) | 86% (79/92) | 91% (84/92) | 72% (38/53) | 59% (23/39) |
| bge-m3: BM25 + denso (RRF) | 72% (66/92) | 93% (86/92) | 95% (87/92) | 81% (43/53) | 59% (23/39) |
| qwen3-embedding:0.6b: denso | 66% (61/92) | 88% (81/92) | 93% (86/92) | 74% (39/53) | 56% (22/39) |
| qwen3-embedding:0.6b: BM25 + denso (RRF) | 80% (74/92) | 95% (87/92) | 97% (89/92) | 92% (49/53) | 64% (25/39) |
| qwen3-embedding:4b: denso | 79% (73/92) | 97% (89/92) | 98% (90/92) | 92% (49/53) | 62% (24/39) |
| qwen3-embedding:4b: BM25 + denso (RRF) | 79% (73/92) | 98% (90/92) | 99% (91/92) | 91% (48/53) | 64% (25/39) |
| snowflake-arctic-embed2: denso | 70% (64/92) | 88% (81/92) | 92% (85/92) | 77% (41/53) | 59% (23/39) |
| snowflake-arctic-embed2: BM25 + denso (RRF) | 77% (71/92) | 93% (86/92) | 98% (90/92) | 89% (47/53) | 62% (24/39) |
| granite-embedding:278m: denso | 57% (52/92) | 80% (74/92) | 88% (81/92) | 68% (36/53) | 41% (16/39) |
| granite-embedding:278m: BM25 + denso (RRF) | 72% (66/92) | 89% (82/92) | 96% (88/92) | 83% (44/53) | 56% (22/39) |

**Vencedor pela regra pré-registrada** (maior recall@10 do denso; até uma questão de diferença é empate, decidido pelo top-1): `qwen3-embedding:4b`. Modelo exportado para `dados/conhecimento/embeddings/`: `qwen3-embedding:4b`.

Modelos:

- `bge-m3`: dimensão 1024, 0 s nesta rodada (0 quando tudo veio do cache).
- `qwen3-embedding:0.6b`: dimensão 1024, 0 s nesta rodada (0 quando tudo veio do cache).
- `qwen3-embedding:4b`: dimensão 2560, 0 s nesta rodada (0 quando tudo veio do cache).
- `snowflake-arctic-embed2`: dimensão 1024, 0 s nesta rodada (0 quando tudo veio do cache).
- `granite-embedding:278m`: dimensão 768, 0 s nesta rodada (0 quando tudo veio do cache).

## E9: kNN deixa-uma-fora entre as questões da folha

Teto: tema certo presente em outra questão da folha (92): 84% (77/92).

| Variante | Top-1 (92) | Recall@5 | Recall@10 | Top-1, nível 1 | Top-1, nível 2 |
|---|---:|---:|---:|---:|---:|
| bge-m3: kNN (k=10) | 28% (26/92) | 63% (58/92) | 70% (64/92) | 36% (19/53) | 18% (7/39) |
| qwen3-embedding:0.6b: kNN (k=10) | 37% (34/92) | 66% (61/92) | 71% (65/92) | 45% (24/53) | 26% (10/39) |
| qwen3-embedding:4b: kNN (k=10) | 36% (33/92) | 65% (60/92) | 77% (71/92) | 45% (24/53) | 23% (9/39) |
| snowflake-arctic-embed2: kNN (k=10) | 32% (29/92) | 65% (60/92) | 74% (68/92) | 42% (22/53) | 18% (7/39) |
| granite-embedding:278m: kNN (k=10) | 36% (33/92) | 59% (54/92) | 68% (63/92) | 38% (20/53) | 33% (13/39) |

## E8b: documento do tema com o `qwen3-embedding:4b`

Variantes do texto do tema (`dados/conhecimento/temas.jsonl`): `cartao` (título, caminho, escopo, o que entra e âncoras), `cartao_termos` (mais os termos `forte` e `fraco`) e `cartao_termos_leis` (mais as referências do mapa revisado). A fusão usa o BM25 da mesma variante.

| Variante | Top-1 (92) | Recall@5 | Recall@10 | Top-1, nível 1 | Top-1, nível 2 |
|---|---:|---:|---:|---:|---:|
| cartao: denso | 79% (73/92) | 97% (89/92) | 98% (90/92) | 92% (49/53) | 62% (24/39) |
| cartao: BM25 + denso (RRF) | 79% (73/92) | 98% (90/92) | 99% (91/92) | 91% (48/53) | 64% (25/39) |
| cartao_termos: denso | 84% (77/92) | 97% (89/92) | 98% (90/92) | 94% (50/53) | 69% (27/39) |
| cartao_termos: BM25 + denso (RRF) | 83% (76/92) | 98% (90/92) | 99% (91/92) | 91% (48/53) | 72% (28/39) |
| cartao_termos_leis: denso | 86% (79/92) | 97% (89/92) | 98% (90/92) | 96% (51/53) | 72% (28/39) |
| cartao_termos_leis: BM25 + denso (RRF) | 84% (77/92) | 98% (90/92) | 99% (91/92) | 91% (48/53) | 74% (29/39) |

**Vencedor pela regra pré-registrada** (sobre o denso): `cartao_termos_leis`. Documento exportado para `dados/conhecimento/embeddings/temas.npy`: `cartao_termos_leis`.
