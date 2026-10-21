# E10: ranqueador de pares, logística × gradient boosting

Gerado em 21/10/2026 08:53. Folha-verdade, fora da amostra (5 partes × 10 repetições), com os mesmos candidatos e atributos do sistema. Critério: menor log-loss do nó escolhido; diferença menor que 0.005 é empate, decidido pela configuração mais simples.

| Configuração | Log-loss | Acerto (100) | Topo 20: certas (fora) | Topo 30: certas (fora) | Topo 50: certas (fora) |
|---|---:|---:|---:|---:|---:|
| logística L2 (penalidade 10) | 0.433 | 81 | 19 (1) | 28 (2) | 45 (3) |
| boosting (profundidade 2, folha ≥ 20, 100 árvores) | 0.411 | 79 | 19 (1) | 29 (1) | 49 (1) |
| **boosting (profundidade 2, folha ≥ 20, 200 árvores)** | 0.403 | 77 | 19 (1) | 29 (1) | 48 (1) |
| boosting (profundidade 2, folha ≥ 10, 100 árvores) | 0.410 | 79 | 19 (1) | 29 (1) | 49 (1) |
| boosting (profundidade 2, folha ≥ 10, 200 árvores) | 0.411 | 76 | 19 (1) | 29 (1) | 48 (2) |
| boosting (profundidade 3, folha ≥ 20, 100 árvores) | 0.411 | 78 | 19 (1) | 29 (1) | 49 (1) |
| boosting (profundidade 3, folha ≥ 20, 200 árvores) | 0.404 | 76 | 19 (1) | 29 (1) | 48 (1) |
| boosting (profundidade 3, folha ≥ 10, 100 árvores) | 0.400 | 77 | 19 (1) | 29 (1) | 48 (1) |
| boosting (profundidade 3, folha ≥ 10, 200 árvores) | 0.412 | 76 | 19 (1) | 29 (1) | 47 (2) |

**Vencedor pela regra pré-registrada:** boosting (profundidade 2, folha ≥ 20, 200 árvores). Ranqueador em uso no sistema: boosting (profundidade 2, folha ≥ 20, 200 árvores).
