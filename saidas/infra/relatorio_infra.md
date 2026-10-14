# Infraestrutura e recomendação de modelos

_Gerado em 14/10/2026 10:49._

Retrato da máquina e avaliação dos modelos candidatos para o pipeline de classificação (ADR-017).

Critério: contexto de 16,384 tokens, saída em JSON Schema, pesos qualidade 0.6 / custo 0.2 / velocidade 0.2. As notas de qualidade são estimativas do catálogo (`config/catalogo_modelos.json`), a validar no experimento E6.

Para escolher modelos: `uv run python executar_escolha_modelo.py` (interativo) ou editar `config/escolha_modelos.json`. Para gerar de novo: `uv run python executar_infra.py`.

## Sumário

1. Máquina
2. Provedores
3. Papéis sugeridos (escolha automática)
4. Modelos avaliados

## 1. Máquina

- Linux 7.0.0-38-generic (x86_64); AMD Ryzen 7 7735HS with Radeon Graphics, 16 threads.
- RAM: 32.9 GB no total, 18.1 GB disponíveis; disco livre: 64.6 GB.
- GPU usada para modelos locais: NVIDIA GeForce RTX 4050 Laptop GPU com 6.4 GB de VRAM.

**GPUs**

| nome | fabricante | tipo | VRAM (GB) | livre (GB) | usada p/ LLM | obs. |
|---|---|---|---|---|---|---|
| NVIDIA GeForce RTX 4050 Laptop GPU | NVIDIA | dedicada | 6.4 | 1.5 | sim | driver 580.159.03 |
| Advanced Micro Devices, Inc. [AMD/ATI] Rembrandt [Radeon 680M] (rev 0a) | AMD | integrada | ? | ? | não | integrada: o Ollama usa a dedicada ou a CPU |

_completa em `tabelas/01_01_gpus.csv`._

## 2. Provedores

- 4 de 6 provedores prontos para uso nesta máquina.
- Credenciais são lidas do ambiente ou do `.env` (ignorado pelo git); só se informa se existem.

**Situação dos provedores**

| provedor | acesso | situação | detalhe |
|---|---|---|---|
| ollama | local | pronto | versão 0.34.0; 2 modelos instalados: qwen3.5:4b, codellama:7b |
| claude-cli | assinatura | pronto | claude 2.1.299; login não verificado |
| gemini-agy | assinatura | pronto | agy 1.3.5; 10 modelos na conta |
| claude-api | api | indisponível | falta ANTHROPIC_API_KEY |
| openai | api | indisponível | falta OPENAI_API_KEY |
| huggingface | api | pronto | credencial encontrada |

_completa em `tabelas/02_01_provedores.csv`._

## 3. Papéis sugeridos (escolha automática)

- Classificador A: melhor pontuação; B: melhor de outra família (diversidade); voto barato: maior custo + velocidade; verificador: maior qualidade.

**Modelo sugerido por papel**

| papel | provedor | modelo | por quê |
|---|---|---|---|
| classificador_a | claude-cli | claude-opus-5-5 | assinatura via CLI `claude` 2.1.299 |
| classificador_b | gemini-agy | gemini-3.8-flash-low | assinatura via CLI `agy` 1.3.5 |
| voto_barato | ollama | qwen3.5:4b | roda dividido entre GPU e CPU (mais lento); ~6.3 GB; os pesos não cabem inteiros na GPU (estimativa conservadora) |
| verificador | claude-cli | claude-opus-5-5 | assinatura via CLI `claude` 2.1.299 |

_completa em `tabelas/03_01_papeis.csv`._

## 4. Modelos avaliados

- 28 modelos avaliados: 14 prontos, 27 viáveis nesta máquina.
- Pronto = viável e utilizável agora; viável = cabe na máquina, mas falta baixar o modelo ou configurar credencial.

**Ranking (prontos primeiro)**

| # | provedor | modelo | pronto | execução | qualidade | custo | velocidade | pontuação | memória (GB) | contexto máx. na GPU | US$/chamada | motivo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | claude-cli | claude-opus-5-5 | sim | assinatura | 5 | 4 | 3 | 4.40 |  |  |  | assinatura via CLI `claude` 2.1.299 |
| 2 | gemini-agy | claude-opus-5-5-low | sim | assinatura | 5 | 4 | 3 | 4.40 |  |  |  | assinatura via CLI `agy` 1.3.5 |
| 3 | gemini-agy | claude-opus-5-5-medium | sim | assinatura | 5 | 4 | 2 | 4.20 |  |  |  | assinatura via CLI `agy` 1.3.5 |
| 4 | gemini-agy | claude-opus-5-5-high | sim | assinatura | 5 | 4 | 1 | 4.00 |  |  |  | assinatura via CLI `agy` 1.3.5 |
| 5 | claude-cli | claude-sonnet-5-5 | sim | assinatura | 4 | 4 | 3 | 3.80 |  |  |  | assinatura via CLI `claude` 2.1.299 |
| 6 | gemini-agy | claude-sonnet-5-5-low | sim | assinatura | 4 | 4 | 3 | 3.80 |  |  |  | assinatura via CLI `agy` 1.3.5 |
| 7 | gemini-agy | gemini-3.8-flash-low | sim | assinatura | 4 | 4 | 3 | 3.80 |  |  |  | assinatura via CLI `agy` 1.3.5 |
| 8 | gemini-agy | claude-sonnet-5-5-medium | sim | assinatura | 4 | 4 | 2 | 3.60 |  |  |  | assinatura via CLI `agy` 1.3.5 |
| 9 | gemini-agy | gemini-3.8-flash-medium | sim | assinatura | 4 | 4 | 2 | 3.60 |  |  |  | assinatura via CLI `agy` 1.3.5 |
| 10 | gemini-agy | gpt-oss-120b-medium | sim | assinatura | 4 | 4 | 2 | 3.60 |  |  |  | assinatura via CLI `agy` 1.3.5 |
| 11 | gemini-agy | claude-sonnet-5-5-high | sim | assinatura | 4 | 4 | 1 | 3.40 |  |  |  | assinatura via CLI `agy` 1.3.5 |
| 12 | gemini-agy | gemini-3.8-flash-high | sim | assinatura | 4 | 4 | 1 | 3.40 |  |  |  | assinatura via CLI `agy` 1.3.5 |
| 13 | claude-cli | claude-haiku-5-5 | sim | assinatura | 3 | 4 | 3 | 3.20 |  |  |  | assinatura via CLI `claude` 2.1.299 |
| 14 | ollama | qwen3.5:4b | sim | gpu_parcial | 1 | 5 | 2 | 2.00 | 6.3 | 0 |  | roda dividido entre GPU e CPU (mais lento); ~6.3 GB; os pesos não cabem inteiros na GPU (estimativa conservadora) |
| 15 | openai | gpt-5 | viável | api | 5 | 3 | 4 | 4.40 |  |  |  | falta OPENAI_API_KEY |
| 16 | claude-api | claude-opus-5-5 | viável | api | 5 | 2 | 4 | 4.20 |  |  | 0.0855 | falta ANTHROPIC_API_KEY (ou `ant auth login`) |
| 17 | claude-api | claude-sonnet-5-5 | viável | api | 4 | 3 | 4 | 3.80 |  |  | 0.0428 | falta ANTHROPIC_API_KEY (ou `ant auth login`) |
| 18 | huggingface | Qwen/Qwen3-235B-A22B-Instruct-2507 | viável | api | 4 | 3 | 4 | 3.80 |  |  |  | Inference Providers (HF); nome/disponibilidade a confirmar (teste com executar_teste_llm.py e marque verificar=false no catálogo) |
| 19 | openai | gpt-5-mini | viável | api | 4 | 3 | 4 | 3.80 |  |  |  | falta OPENAI_API_KEY |
| 20 | claude-api | claude-haiku-5-5 | viável | api | 3 | 5 | 4 | 3.60 |  |  | 0.0021 | falta ANTHROPIC_API_KEY (ou `ant auth login`) |
| 21 | huggingface | meta-llama/Llama-3.3-70B-Instruct | viável | api | 3 | 3 | 4 | 3.20 |  |  |  | Inference Providers (HF); nome/disponibilidade a confirmar (teste com executar_teste_llm.py e marque verificar=false no catálogo) |
| 22 | ollama | gemma3:12b | viável | gpu_parcial | 3 | 5 | 2 | 3.20 | 15.3 | 0 |  | baixar com `ollama pull gemma3:12b` (8.1 GB); roda dividido entre GPU e CPU (mais lento); ~15.3 GB; os pesos não cabem inteiros na GPU |
| 23 | ollama | qwen3:14b | viável | gpu_parcial | 3 | 5 | 2 | 3.20 | 12.8 | 0 |  | baixar com `ollama pull qwen3:14b` (9.3 GB); roda dividido entre GPU e CPU (mais lento); ~12.8 GB; os pesos não cabem inteiros na GPU |
| 24 | ollama | llama3.1:8b | viável | gpu_parcial | 2 | 5 | 2 | 2.60 | 7.8 | 0 |  | baixar com `ollama pull llama3.1:8b` (4.9 GB); roda dividido entre GPU e CPU (mais lento); ~7.8 GB; os pesos não cabem inteiros na GPU |
| 25 | ollama | qwen3:8b | viável | gpu_parcial | 2 | 5 | 2 | 2.60 | 8.4 | 0 |  | baixar com `ollama pull qwen3:8b` (5.2 GB); roda dividido entre GPU e CPU (mais lento); ~8.4 GB; os pesos não cabem inteiros na GPU |
| 26 | ollama | codellama:7b | viável | gpu_parcial | 1 | 5 | 2 | 2.00 | 13.2 | 0 |  | inadequado: modelo especializado em código: inadequado para texto jurídico; roda dividido entre GPU e CPU (mais lento); ~13.2 GB; os pesos não cabem inteiros n… |
| 27 | ollama | qwen3:4b | viável | gpu_parcial | 1 | 5 | 2 | 2.00 | 5.8 | 0 |  | baixar com `ollama pull qwen3:4b` (2.6 GB); roda dividido entre GPU e CPU (mais lento); ~5.8 GB; os pesos não cabem inteiros na GPU |
| 28 | ollama | qwen3:30b | não | — | 3 | 5 | 1 | 0.00 | 21.4 |  |  | precisa ~21.4 GB com 16,384 tokens; há ~1.4 GB de VRAM e ~18.1 GB de RAM livres |

_completa em `tabelas/04_01_modelos.csv`._
