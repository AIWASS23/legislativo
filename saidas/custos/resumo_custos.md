# Custo e tempo das chamadas a modelos

Gerado em 20/10/2026 10:47 a partir do cache (`runs/`). Cada chamada é paga uma vez;
as repetições vêm do cache e não entram aqui.

- **pago:** API cobrada por token (preço do catálogo, ou o informado pelo provedor).
- **equivalente_de_lista:** a CLI `claude` informa quanto custaria na API; com assinatura, não é cobrado.
- **assinatura:** CLI sem custo informado; o custo real é a cota e o tempo.
- **local:** modelo na própria máquina; custo zero, só tempo.

| Papel | Provedor | Modelo | Chamadas | Tokens entrada | Tokens saída | Tempo total | Média | Custo (USD) | Tipo |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| cartoes | claude-cli | claude-opus-5-5 | 58 | 1,076,943 | 329,793 | 49.4 min | 51.1 s | 14.81 | equivalente_de_lista |
| classificador_a | codex-cli | gpt-6.1-sol | 369 | 16,546,108 | 74,913 | 50.6 min | 8.2 s | — | assinatura |
| classificador_b | gemini-agy | gemini-3.8-flash-low | 642 | 19,947,886 | 1,084,805 | 193.8 min | 18.1 s | — | assinatura |
| conhecimento | codex-cli | gpt-6.1-sol | 62 | 1,690,389 | 164,358 | 49.9 min | 48.3 s | — | assinatura |
| e4_b_so_titulos | gemini-agy | gemini-3.8-flash-low | 107 | 2,450,802 | 221,605 | 36.2 min | 20.3 s | — | assinatura |
| verificador | gemini-agy | claude-opus-5-5-medium | 13 | 632,969 | 9,898 | 3.1 min | 14.3 s | — | assinatura |
| verificador | gemini-agy | gemini-3.8-flash-medium | 326 | 9,314,026 | 2,461,933 | 181.0 min | 33.3 s | — | assinatura |
| voto_barato | gemini-agy | gpt-oss-120b-medium | 374 | 24,191,658 | 456,584 | 114.0 min | 18.3 s | — | assinatura |
| voto_barato | ollama | qwen3.5:4b | 14 | 111,317 | 707 | 7.9 min | 33.8 s | 0.00 | local |

**Total:** 1965 chamadas; 11.43 h de tempo sequencial equivalente; US$ 0.00 pagos; US$ 14.81 em equivalente de lista (assinatura).
