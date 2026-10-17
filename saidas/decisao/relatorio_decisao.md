# Passo 07: decisão

Gerado em 17/10/2026 15:13.

- Publicar: 81; revisar: 276; fora: 2.
- Publicadas no nível 1: 27, das quais 0 por recuo para o pai (ADR-010).
- Tipo de convenção das publicadas: {'sem risco': 81}.
- Limiar P = 0.983 (limite inferior).
- Precisão: ponto 0.973, intervalo 0.933–1.000; modelo 0.983; direta 1.0 em 13 do gold (suavizada 0.9642); margens: convenção 0.000, ambiguidade 0.000.

## Motivos de revisar e fora

| Motivo | Questões |
|---|---:|
| baixa confiança | 211 |
| possível fora do recorte | 14 |
| questão cobre vários temas | 4 |
| dúvida entre 5492 e 5583 | 3 |
| sobreposição | 2 |
| nenhum tema do recorte serve | 2 |
| verificador sugere 5539 | 2 |
| verificador sugere 5534 | 1 |
| verificador sugere 5468 | 1 |
| dúvida entre 4709 e 5199 | 1 |
| dúvida entre 5118 e 5132 | 1 |
| dúvida entre 5549 e 5583 | 1 |
| verificador sugere 5557 | 1 |
| dúvida entre 5096 e 5116 | 1 |
| dúvida entre 5193 e 4703 | 1 |
| dúvida entre 4703 e 5181 | 1 |
| dúvida entre 4708 e 4705 | 1 |
| dúvida entre 5224 e 5103 | 1 |
| verificador sugere 5477 | 1 |
| dúvida entre 5194 e 5181 | 1 |
| dúvida entre 5533 e 5547 | 1 |
| dúvida entre 4378 e 4387 | 1 |
| dúvida entre 5520 e 4693 | 1 |
| dúvida entre 5484 e 5466 | 1 |
| verificador sugere 5554 | 1 |
| dúvida entre 5469 e 5472 | 1 |
| dúvida entre 4701 e 5539 | 1 |
| dúvida entre 5482 e 5500 | 1 |
| dúvida entre 5224 e 5109 | 1 |
| dúvida entre 5512 e 5560 | 1 |
| dúvida entre 5499 e 5582 | 1 |
| dúvida entre 4372 e 4373 | 1 |
| verificador sugere 5171 | 1 |
| dúvida entre 5584 e 5517 | 1 |
| dúvida entre 5473 e 5500 | 1 |
| dúvida entre 5199 e 4703 | 1 |
| dúvida entre 4375 e 4368 | 1 |
| dúvida entre 5562 e 5515 | 1 |
| dúvida entre 5540 e 4701 | 1 |
| dúvida entre 5120 e 5466 | 1 |
| verificador sugere 5500 | 1 |
| dúvida entre 5198 e 5064 | 1 |
| dúvida entre 5569 e 5561 | 1 |
| verificador sugere 5531 | 1 |
| dúvida entre 4374 e 4381 | 1 |
| verificador sugere 5543 | 1 |
| dúvida entre 5195 e 5065 | 1 |

## Calibração (60 questões do gold com tema)

Validação cruzada: taxa de acerto 0.900; Brier 0.0912 (palpite constante: 0.0900); log-loss 0.2877.

| Faixa de P | Questões | P média | Acerto observado |
|---|---:|---:|---:|
| 0.00–0.50 | 3 | 0.394 | 1.000 |
| 0.50–0.70 | 5 | 0.638 | 0.400 |
| 0.70–0.85 | 10 | 0.805 | 1.000 |
| 0.85–0.95 | 14 | 0.866 | 0.786 |
| 0.95–1.00 | 28 | 0.978 | 1.000 |

Calibrador escolhido pela menor log-loss na validação cruzada: **faixas de sinais com suavização de Jeffreys**.

| Calibrador | Brier | Log-loss |
|---|---:|---:|
| faixas de sinais com suavização de Jeffreys | 0.0912 | 0.2877 |
| regressão logística L2 (penalidade 3) | 0.0883 | 0.3150 |
| regressão logística L2 (penalidade 1) | 0.0891 | 0.3124 |
| regressão logística L2 (penalidade 0.3) | 0.1013 | 0.3400 |
| regressão logística L2 (penalidade 0.1) | 0.1154 | 0.3982 |
| regressão logística L2 (penalidade 0.03) | 0.1239 | 0.4786 |
| regressão logística L2 (penalidade 0.01) | 0.1280 | 0.5566 |

| Faixa | Questões do gold | Acertos | P (Jeffreys) |
|---|---:|---:|---:|
| consenso_total | 28 | 28 | 0.983 |
| confirma_parcial | 22 | 19 | 0.853 |
| verificador_vizinho | 2 | 2 | 0.833 |
| outros | 8 | 5 | 0.593 |
