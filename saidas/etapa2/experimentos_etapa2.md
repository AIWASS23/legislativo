# Experimentos da etapa 2 (folha-verdade)

Gerado em 21/10/2026 07:21. Base: 100 questões da folha-verdade (92 com tema, 8 fora). Régua da etapa 2: tema central, extra, ou pai ou filho de um deles. Nenhum modelo foi chamado.

| Experimento | Variante | Métrica | Valor | Detalhe |
|---|---|---|---:|---|
| E7 | títulos e caminho | acerto top-1 (100) | 0.470 | 47/100 |
| E7 | títulos e caminho | acerto top-1 (92 com tema) | 0.511 | 47/92 |
| E7 | títulos e caminho | recall@5 (92) | 0.761 | 70/92 |
| E7 | títulos e caminho | recall@10 (92) | 0.859 | 79/92 |
| E7 | títulos e caminho | acerto top-1, tema central de nível 1 | 0.547 | 29/53 |
| E7 | títulos e caminho | acerto top-1, tema central de nível 2 | 0.462 | 18/39 |
| E7 | com cartão | acerto top-1 (100) | 0.620 | 62/100 |
| E7 | com cartão | acerto top-1 (92 com tema) | 0.674 | 62/92 |
| E7 | com cartão | recall@5 (92) | 0.924 | 85/92 |
| E7 | com cartão | recall@10 (92) | 0.935 | 86/92 |
| E7 | com cartão | acerto top-1, tema central de nível 1 | 0.811 | 43/53 |
| E7 | com cartão | acerto top-1, tema central de nível 2 | 0.487 | 19/39 |
| E7b | cartao | acerto top-1 (100) | 0.620 | 62/100 |
| E7b | cartao | acerto top-1 (92 com tema) | 0.674 | 62/92 |
| E7b | cartao | recall@5 (92) | 0.924 | 85/92 |
| E7b | cartao | recall@10 (92) | 0.935 | 86/92 |
| E7b | cartao | acerto top-1, tema central de nível 1 | 0.811 | 43/53 |
| E7b | cartao | acerto top-1, tema central de nível 2 | 0.487 | 19/39 |
| E7b | cartao_termos | acerto top-1 (100) | 0.670 | 67/100 |
| E7b | cartao_termos | acerto top-1 (92 com tema) | 0.728 | 67/92 |
| E7b | cartao_termos | recall@5 (92) | 0.902 | 83/92 |
| E7b | cartao_termos | recall@10 (92) | 0.967 | 89/92 |
| E7b | cartao_termos | acerto top-1, tema central de nível 1 | 0.849 | 45/53 |
| E7b | cartao_termos | acerto top-1, tema central de nível 2 | 0.564 | 22/39 |
| E7b | cartao_termos_leis | acerto top-1 (100) | 0.670 | 67/100 |
| E7b | cartao_termos_leis | acerto top-1 (92 com tema) | 0.728 | 67/92 |
| E7b | cartao_termos_leis | recall@5 (92) | 0.924 | 85/92 |
| E7b | cartao_termos_leis | recall@10 (92) | 0.967 | 89/92 |
| E7b | cartao_termos_leis | acerto top-1, tema central de nível 1 | 0.849 | 45/53 |
| E7b | cartao_termos_leis | acerto top-1, tema central de nível 2 | 0.564 | 22/39 |
| E11 | pontuação máxima baixa | AUC | 0.668 | IC 90%: 0.52–0.80 |
| E11 | margem baixa | AUC | 0.626 | IC 90%: 0.43–0.79 |
| E11 | dispersão entre alternativas | AUC | 0.594 | IC 90%: 0.41–0.77 |
| E11 | enunciado genérico | AUC | 0.478 | IC 90%: 0.46–0.49 |
| E11 | (Parte N) no assunto de origem | AUC | 0.579 | IC 90%: 0.44–0.73 |
| E11 | disciplina de origem fora do recorte | AUC | 0.489 | IC 90%: 0.47–0.50 |
| E11 | logística: pontuação máxima baixa, margem baixa, dispersão entre alternativas | AUC fora da amostra | 0.537 | IC 90%: 0.35–0.72; 5 partes × 10 repetições |

**E7b, documento de tema no BM25:** vence `cartao_termos` pela regra pré-registrada (maior recall@10; até uma questão de diferença é empate, decidido pelo top-1; depois, a variante mais simples). Documento do BM25 em uso no sistema: `cartao_termos`.

## E11: atributos das questões fora × mediana das questões com tema

| Questão | Pontuação máxima | Margem | Dispersão | Genérico | (Parte N) | Origem fora |
|---|---:|---:|---:|---|---|---|
| **mediana (com tema)** | 42.48 | 0.19 | 0.60 | | | |
| Q0002 | 14.20 | 0.04 | 1.00 | não | não | não |
| Q0017 | 27.24 | 0.08 | 0.40 | não | sim | não |
| Q0039 | 34.23 | 0.42 | 0.80 | não | não | não |
| Q0043 | 38.10 | 0.05 | 0.25 | não | sim | não |
| Q0087 | 28.35 | 0.11 | 1.00 | não | não | não |
| Q0252 | 41.16 | 0.07 | 0.50 | não | sim | não |
| Q0291 | 39.03 | 0.38 | — | não | não | não |
| Q0303 | 51.34 | 0.01 | 1.00 | não | não | não |
