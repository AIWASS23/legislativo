# E14: rotulagem ativa (curva de aprendizado e fila para a produção)

Gerado em 21/10/2026 09:12. Ranqueador: boosting (profundidade 2, folha ≥ 20, 200 árvores). Treino com parte da folha, teste no resto, 10 sorteios estratificados por tamanho.

| Questões rotuladas no treino | Log-loss no teste | Desvio | Acerto do nó no teste |
|---:|---:|---:|---:|
| 40 | 0.548 | 0.126 | 74% |
| 60 | 0.477 | 0.150 | 75% |
| 80 | 0.446 | 0.078 | 75% |

Fila de rotulagem ativa: `saidas/etapa2/fila_rotulagem_ativa.csv`, com as 150 questões em `revisar` mais perto do limiar, em rodízio pelas disciplinas.
