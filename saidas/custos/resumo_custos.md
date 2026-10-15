# Custo e tempo das chamadas a modelos

Gerado em 15/10/2026 16:18 a partir do cache (`runs/`). Cada chamada é paga uma vez;
as repetições vêm do cache e não entram aqui.

- **pago:** API cobrada por token (preço do catálogo, ou o informado pelo provedor).
- **equivalente_de_lista:** a CLI `claude` informa quanto custaria na API; com assinatura, não é cobrado.
- **assinatura:** CLI sem custo informado; o custo real é a cota e o tempo.
- **local:** modelo na própria máquina; custo zero, só tempo.

| Papel | Provedor | Modelo | Chamadas | Tokens entrada | Tokens saída | Tempo total | Média | Custo (USD) | Tipo |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| cartoes | claude-cli | claude-opus-5-5 | 58 | 1,076,943 | 329,793 | 49.4 min | 51.1 s | 14.81 | equivalente_de_lista |
| classificador_a | codex-cli | gpt-6.1-sol | 95 | 4,256,884 | 17,806 | 13.4 min | 8.4 s | — | assinatura |
| classificador_b | gemini-agy | gemini-3.8-flash-low | 641 | 19,894,379 | 1,084,551 | 193.6 min | 18.1 s | — | assinatura |
| verificador | gemini-agy | claude-opus-5-5-medium | 13 | 632,969 | 9,898 | 3.1 min | 14.3 s | — | assinatura |
| verificador | gemini-agy | gemini-3.8-flash-medium | 75 | 2,182,797 | 484,547 | 38.1 min | 30.5 s | — | assinatura |
| voto_barato | gemini-agy | gpt-oss-120b-medium | 80 | 4,951,231 | 91,534 | 27.3 min | 20.5 s | — | assinatura |
| voto_barato | ollama | qwen3.5:4b | 14 | 111,317 | 707 | 7.9 min | 33.8 s | 0.00 | local |

**Total:** 976 chamadas; 5.55 h de tempo sequencial equivalente; US$ 0.00 pagos; US$ 14.81 em equivalente de lista (assinatura).
