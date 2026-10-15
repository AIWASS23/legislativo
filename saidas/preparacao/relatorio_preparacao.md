# Passo 01: questões preparadas

_Gerado em 15/10/2026 08:19._

Questões convertidas no texto canônico da ADR-004: HTML limpo (inclusive o lixo colado do Word), alternativas sempre incluídas (exceto em certo/errado), comando só quando útil e com conteúdo, e nenhum rótulo de origem no texto (ADR-006).

Saída para os próximos passos: `dados/preparados/questoes.jsonl`. Amostra para conferência manual: `conferencia_texto_canonico.md`. Para gerar de novo: `uv run python executar_preparacao.py`.

## Sumário

1. Formatos
2. Comando no texto canônico
3. Tamanho do texto canônico
4. Marcas guardadas para decisão e calibração
5. Checagens automáticas

## 1. Formatos

- 359 questões preparadas.

**Questões por formato**

| formato | questões | % |
|---|---|---|
| multipla_escolha_5 | 255 | 71.00 |
| certo_errado | 58 | 16.20 |
| multipla_escolha_4 | 46 | 12.80 |

_completa em `tabelas/01_01_formatos.csv`._

## 2. Comando no texto canônico

- O comando entrou em 50 questões (13.9%).
- Ficou de fora em 309: vazio (101), suspeito de ter sido gerado (62), repete o enunciado (72) ou só frase-padrão como 'Julgue o item a seguir' (74).

**Destino do comando**

| motivo | questões | % |
|---|---|---|
| vazio | 101 | 28.10 |
| so_frase_padrao | 74 | 20.60 |
| repete_enunciado | 72 | 20.10 |
| suspeito | 62 | 17.30 |
| incluido | 50 | 13.90 |

_completa em `tabelas/02_01_motivo_comando.csv`._

## 3. Tamanho do texto canônico

- Mediana de 250 tokens por questão (estimativa: 3.5 caracteres por token); máximo de 1175; 97.915 tokens no total.
- A questão vai na parte variável do prompt; a árvore de temas é a parte fixa (ADR-007, ADR-008).

**Distribuição de tamanho**

| medida | n | mín | p25 | mediana | p75 | p95 | máx | média |
|---|---|---|---|---|---|---|---|---|
| tokens estimados | 359 | 51.00 | 153.00 | 250.00 | 341.50 | 580.70 | 1175.00 | 272.70 |
| caracteres | 359 | 177.00 | 536.50 | 875.00 | 1196.00 | 2032.30 | 4112.00 | 954.60 |

_completa em `tabelas/03_01_tamanho.csv`._

**Questões mais longas**

| id | formato | tokens estimados | caracteres |
|---|---|---|---|
| Q0284 | multipla_escolha_5 | 1175 | 4112 |
| Q0289 | multipla_escolha_5 | 943 | 3299 |
| Q0070 | multipla_escolha_5 | 873 | 3054 |
| Q0097 | multipla_escolha_5 | 777 | 2719 |
| Q0020 | multipla_escolha_5 | 755 | 2644 |
| Q0089 | multipla_escolha_5 | 743 | 2602 |
| Q0146 | multipla_escolha_5 | 743 | 2601 |
| Q0100 | multipla_escolha_5 | 721 | 2523 |
| Q0329 | multipla_escolha_5 | 674 | 2358 |
| Q0323 | multipla_escolha_5 | 666 | 2331 |

_completa em `tabelas/03_02_maiores.csv`._

## 4. Marcas guardadas para decisão e calibração

- As marcas acompanham a questão em `questoes.jsonl` (ADR-011, ADR-013).

**Questões por marca**

| marca | questões | % |
|---|---|---|
| enunciado genérico | 18 | 5.00 |
| HTML colado do Word no original | 1 | 0.30 |
| cita alguma lei | 95 | 26.50 |
| cita jurisprudência | 49 | 13.60 |
| duplicata de outra questão (texto completo) | 0 | 0.00 |

_completa em `tabelas/04_01_marcas.csv`._

## 5. Checagens automáticas

- 8 de 8 checagens aprovadas.

**Regras verificadas**

| regra | resultado | violações |
|---|---|---|
| todas as questões foram preparadas, uma vez cada | aprovada |  |
| nenhum texto canônico vazio | aprovada |  |
| nenhuma tag HTML no texto canônico | aprovada |  |
| nenhum escape literal (barra + n ou t) no texto canônico | aprovada |  |
| nenhum resíduo de editor (CSS do Word) no texto canônico | aprovada |  |
| múltipla escolha traz todas as alternativas; certo/errado não traz alternativas | aprovada |  |
| comando no texto só quando útil e com conteúdo | aprovada |  |
| rótulos de origem não entram no texto canônico (ADR-006) | aprovada |  |

_completa em `tabelas/05_01_checagens.csv`._
