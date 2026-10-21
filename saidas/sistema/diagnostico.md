# Diagnóstico do sistema da etapa 2

Gerado por `uv run python executar_sistema.py`, sem modelo de linguagem e sem rede.

## Ranqueador fora da amostra (folha, 5 partes × 10 repetições)

- Nó escolhido certo pela régua: 82/100 (82/92 com tema).
- Calibração: a identidade (log-loss fora da amostra: identidade 0.363, platt 0.376, platt_concordancia 0.393); coeficientes: ().

| Questões da folha (maior P primeiro) | Certas | Fora entre elas | P da última |
|---:|---:|---:|---:|
| 10 | 9/10 (90%) | 1 | 0.948 |
| 20 | 19/20 (95%) | 1 | 0.940 |
| 30 | 29/30 (97%) | 1 | 0.925 |
| 40 | 39/40 (98%) | 1 | 0.912 |
| 50 | 48/50 (96%) | 2 | 0.860 |
| 60 | 55/60 (92%) | 2 | 0.831 |
| 70 | 64/70 (91%) | 3 | 0.807 |
| 80 | 74/80 (92%) | 3 | 0.742 |
| 90 | 79/90 (88%) | 6 | 0.620 |
| 100 | 82/100 (82%) | 8 | 0.414 |

## Ranqueador: boosting (profundidade 2, folha ≥ 20, 200 árvores); pesos do modelo final (atributos padronizados)

| Atributo | Peso |
|---|---:|
| (modelo não linear: sem pesos por atributo) | — |

## Limiar (avaliadas elegíveis)

- Critério: reserva pontual; pelo percentil 10 ≥ 95% seriam 58 publicadas.
- Corte em P calibrada 0.9291: 127 publicadas de 559; precisão 0.956 (percentil 10 0.942; 5–95: 0.909–0.987); modelo 0.970, direto 0.942; folha na faixa: 24/25 certas.

| Publicadas | Ponto | Percentil 10 |
|---:|---:|---:|
| 1 | 0.983 | 0.964 |
| 2 | 0.983 | 0.964 |
| 3 | 0.983 | 0.963 |
| 4 | 0.982 | 0.962 |
| 5 | 0.982 | 0.962 |
| 6 | 0.981 | 0.961 |
| 7 | 0.981 | 0.961 |
| 8 | 0.981 | 0.960 |
| 9 | 0.981 | 0.960 |
| 10 | 0.981 | 0.960 |
| 20 | 0.979 | 0.958 |
| 30 | 0.978 | 0.955 |
| 40 | 0.977 | 0.953 |
| 50 | 0.976 | 0.951 |
| 60 | 0.975 | 0.950 |
| 70 | 0.974 | 0.948 |
| 80 | 0.973 | 0.947 |
| 100 | 0.972 | 0.945 |
| 110 | 0.971 | 0.944 |
| 120 | 0.971 | 0.943 |
| 130 | 0.970 | 0.942 |
| 140 | 0.969 | 0.940 |
| 150 | 0.968 | 0.939 |
| 160 | 0.967 | 0.938 |
| 170 | 0.967 | 0.936 |
| 180 | 0.966 | 0.935 |
| 190 | 0.965 | 0.934 |
| 200 | 0.964 | 0.933 |
| 210 | 0.963 | 0.931 |
| 220 | 0.962 | 0.930 |
| 230 | 0.961 | 0.929 |
| 240 | 0.960 | 0.927 |
| 260 | 0.957 | 0.923 |
| 270 | 0.956 | 0.921 |
| 280 | 0.954 | 0.919 |
| 290 | 0.952 | 0.917 |
| 300 | 0.950 | 0.913 |
| 310 | 0.947 | 0.911 |
| 320 | 0.944 | 0.908 |
| 330 | 0.941 | 0.904 |
| 340 | 0.938 | 0.901 |
| 350 | 0.935 | 0.897 |
| 360 | 0.932 | 0.894 |
| 370 | 0.927 | 0.889 |
| 380 | 0.923 | 0.884 |
| 390 | 0.917 | 0.879 |
| 400 | 0.911 | 0.872 |
| 410 | 0.904 | 0.864 |
| 420 | 0.897 | 0.857 |
| 430 | 0.889 | 0.849 |
| 440 | 0.881 | 0.841 |
| 450 | 0.871 | 0.831 |
| 460 | 0.859 | 0.819 |

## Decisões

- Nas 659: {'fora': 10, 'publicar': 152, 'revisar': 497}.
- Regras: {'inativo': 95, 'militar': 10} (corte de tema inativo -0.100).
- Cobertura: {'avaliadas': (127, 559), 'antigas': (46, 259), 'novas': (81, 300)}.
