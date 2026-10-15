# Passo 02: cartões de tema

- Cartões: 351; ajustados à mão: 0.
- Sem âncora legal: 5; itens de `nao_inclui` por cartão: 4.9 em média.
- Modelos: claude-cli:claude-opus-5-5.

## Checagens

| Regra | Resultado | Violações |
|---|---|---|
| um cartão por tema publicável, sem repetição | ok | — |
| nao_inclui aponta só para temas publicáveis | ok | — |
| nao_inclui não aponta para o próprio tema | ok | — |
| escopo preenchido e com até 400 caracteres | ok | — |
| inclui tem ao menos um item | ok | — |
| lixeiras fortes e sobreposições têm regra de desempate | ok | — |

## Tamanho de cada versão do material (ADR-007, ADR-008)

| Versão | Bytes | Tokens estimados |
|---|---:|---:|
| árvore enxuta (voto barato) | 26,901 | 7,448 |
| árvore com escopo (classificador A) | 108,360 | 29,834 |
| nível 1 com escopo (classificador B, etapa 1) | 34,926 | 9,587 |
| maior bloco de cartões dos filhos (classificador B, etapa 2) | 22,208 | 6,075 |
| maior ramo de cartões (verificador) | 58,647 | 16,022 |
