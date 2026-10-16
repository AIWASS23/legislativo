# Classificação de tópicos de questões jurídicas: case Vício (Método VDE)

Solução para o case de IA da Vício: decidir, para cada uma das 359 questões de Penal,
Processo Penal, Legislação Penal Especial e Criminologia, entre **publicar** (direto para o
aluno, num tema da árvore), **revisar** (fila do professor, com sugestão) ou **fora**
(nenhum tema serve). A régua é **95% de acerto nas publicadas**, publicando o máximo possível.

- Enunciado original: [`docs/enunciado/`](docs/enunciado/) (README do case e PDF).
- Plano de implementação, em ADRs: [`docs/adr/README.md`](docs/adr/README.md).

## Situação

| Parte | Estado |
|---|---|
| Ambiente e padrão de código ([ADR-001](docs/adr/00-fundacao/ADR-001-stack-e-ambiente.md)) | Pronto |
| Passo 01: texto canônico das questões e árvore preparada ([ADR-004](docs/adr/01-dados/ADR-004-texto-canonico-das-questoes.md), [ADR-005](docs/adr/01-dados/ADR-005-tratamento-da-arvore-de-temas.md)) | Pronto: `dados/preparados/` (questões, `temas.json`, árvore para os prompts) |
| Decisões tomadas à mão | [`decisoes_manuais.md`](decisoes_manuais.md) |
| Provedores de LLM plugáveis e escolha de modelos pela máquina ([ADR-017](docs/adr/00-fundacao/ADR-017-provedores-plugaveis-e-analise-de-infra.md)) | Pronto: [`saidas/infra/relatorio_infra.md`](saidas/infra/relatorio_infra.md) |
| Análise exploratória (EDA) dos dados | Pronta: [`saidas/eda/relatorio_eda.md`](saidas/eda/relatorio_eda.md) |
| Cache de chamadas, custo e tempo ([ADR-003](docs/adr/00-fundacao/ADR-003-cache-reprodutibilidade-e-custo.md)) | Pronto: `runs/` e [`saidas/custos/resumo_custos.md`](saidas/custos/resumo_custos.md) |
| Cartões de tema ([ADR-007](docs/adr/02-temas/ADR-007-cartoes-de-tema.md)) | Gerados por LLM; revisão manual pendente (`saidas/cartoes/revisao_cartoes.md`) |
| Classificação e verificação ([ADR-008](docs/adr/03-classificacao/ADR-008-arquitetura-de-classificacao.md)) | Código pronto; rodada completa em andamento |
| Decisão, calibração e previsão ([ADR-010](docs/adr/04-decisao/ADR-010-granularidade-e-recuo-para-o-pai.md), [ADR-011](docs/adr/04-decisao/ADR-011-politica-publicar-revisar-fora.md), [ADR-013](docs/adr/05-avaliacao/ADR-013-calibracao-e-previsao.md)) | Código pronto; aguarda a rodada completa |
| Gold set manual cego, leva 1 ([ADR-012](docs/adr/05-avaliacao/ADR-012-gold-set-manual-cego.md)) | Sorteio, planilha, rotulagem interativa e régua prontos; rotulagem em andamento (`dados/gold/`) |
| Preparação, classificação, decisão, avaliação | Em andamento; ver o [roteiro](docs/adr/README.md#5-roteiro-de-implementação) |
| Entregáveis (`publicacao.csv`, `previsao.txt`, relatório) | Ainda não gerados |

## Como rodar

### 1. Pré-requisitos

- [uv](https://docs.astral.sh/uv/). Ele instala o Python 3.12 (fixado em `.python-version`) se não houver um na máquina.
- Os anexos do case em `anexos/`. Eles **não são versionados**: baixe o
  [ZIP dos anexos](https://github.com/viciod/case-vicio-ia/raw/main/anexos-case-ia.zip) e extraia
  `questoes.jsonl`, `temas.csv`, `LEIA-ME.md` e `entrega_modelo.csv` em `anexos/`.

### 2. Ambiente

```bash
uv venv                                   # cria .venv com Python 3.12
uv pip install -r requirements-dev.txt    # execução + ferramentas de checagem
# ou, só para executar: uv pip install -r requirements.txt
```

### 3. Etapas disponíveis

Todo ponto de entrada roda **sem argumentos**. Caminhos e limiares ficam em
[`vicio_ia/configuracao.py`](vicio_ia/configuracao.py).

| Comando | O que faz | Saídas |
|---|---|---|
| `uv run python executar_eda.py` | Análise exploratória das questões e da árvore de temas | `saidas/eda/relatorio_eda.md`, `resumo_eda.json`, `tabelas/*.csv` |
| `uv run python executar_preparacao.py` | Passo 01: texto canônico das questões (8 checagens) e árvore preparada a partir das decisões em `dados/temas/` (9 checagens) | `dados/preparados/` (`questoes.jsonl`, `temas.json`, `arvore_enxuta.txt`), `saidas/preparacao/` |
| `uv run python executar_infra.py` | Analisa a máquina (CPU, RAM, GPU, Ollama, CLIs, credenciais) e recomenda um modelo por papel | `saidas/infra/relatorio_infra.md`, `perfil_maquina.json` |
| `uv run python executar_escolha_modelo.py` | Escolha interativa dos modelos (sugestão automática ou um por papel) | `config/escolha_modelos.json` |
| `uv run python executar_teste_llm.py` | Uma questão simples por modelo escolhido: funcionou? acertou? latência e tokens | `saidas/infra/teste_llm.json` |
| `uv run python executar_cartoes.py` | Passo 02: cartões de tema por LLM (uma chamada por tema pai, com cache), ajustes manuais de `dados/temas/cartoes_ajustes.csv`, 6 checagens e as versões da árvore para os prompts | `dados/temas/cartoes.jsonl`, `arvore_escopo.txt`, `saidas/cartoes/` |
| `uv run python executar_classificacao.py` | Passos 05 e 06: classificadores A (plano) e B (hierárquico), voto barato, regras das leis citadas e verificador contrastivo; pula o gold ainda sem rótulo | `dados/classificacao/sinais.jsonl`, `saidas/classificacao/`, `saidas/custos/` |
| `uv run python executar_experimentos.py` | Experimentos no gold (ADR-014): E0 (assunto de origem), E2 (A sozinho), E3 (B e voto barato sozinhos; erros em comum de A e B). Só números agregados | `saidas/experimentos/resultados.csv` |
| `uv run python executar_experimento_cartoes.py` | Experimento E4: classificador B com escopo e cartões × só títulos, no gold (com cache) | `saidas/experimentos/resultados.csv` |
| `uv run python executar_congelamento.py` | Congela o pipeline antes da leva 2: impressão digital de prompts, cartões, árvores, decisões, modelos e código | `saidas/experimentos/congelamento.json`, `registro.md` |
| `uv run python executar_decisao.py` | Passo 07: agregação, recuo para o pai, regras que forçam revisão, calibração no gold, limiar e previsão. Não chama modelo | `publicacao.csv`, `previsao.txt`, `saidas/decisao/`, `dados/decisao/` |
| `uv run python executar_gold.py` | Gold set, leva 1: sorteio estratificado com semente fixa (ou reaproveita o gravado), planilha de rótulos (nunca sobrescrita), caderno e situação da rotulagem | `dados/gold/` (`amostra_leva1.csv`, `rotulos_leva1.csv`, `caderno_leva1.md`) |
| `uv run python executar_rotulagem.py` | Rotulagem interativa no terminal: só o texto canônico, busca de temas na árvore, grava a cada questão e retoma de onde parou | `dados/gold/rotulos_leva1.csv` |
| `uv run python executar_validacao.py` | Confere `publicacao.csv` e `previsao.txt` contra o formato do LEIA-ME (sai com código 1 se houver problema) | Resumo no terminal |
| `uv run python executar_pipeline.py` | Roda tudo em ordem (01, 02, 05/06, 07) e valida a entrega; com o cache `runs/` completo, não chama nenhum modelo | Todos os acima |
| `uv run python executar_checagem.py` | Portão de qualidade: ruff, formatação, mypy estrito, anotações e docstrings | Resumo no terminal; código de saída 1 se algo falhar |

As próximas etapas (preparar, cartões, classificar, decidir, avaliar) entram nesta tabela à medida que forem implementadas.

### 4. Provedores de LLM e credenciais

O pipeline não depende de um fornecedor ([ADR-017](docs/adr/00-fundacao/ADR-017-provedores-plugaveis-e-analise-de-infra.md)).
Cada papel do ensemble (classificador A, classificador B, voto barato, verificador) usa o
modelo escolhido para a máquina. Basta ter **um** dos provedores abaixo:

| Provedor | Acesso | O que precisa |
|---|---|---|
| `ollama` | local (GPU/CPU) | [Ollama](https://ollama.com) rodando e um modelo baixado (`ollama pull ...`). GGUF do Hugging Face: `ollama pull hf.co/<usuario>/<repo>:<quant>` |
| `claude-cli` | assinatura | CLI `claude` (Claude Code) com login feito |
| `gemini-agy` | assinatura | CLI `agy` (Antigravity) com login feito; também dá acesso a Claude Opus/Sonnet e GPT-OSS |
| `codex-cli` | assinatura | CLI `codex` (OpenAI Codex) com login do ChatGPT |
| `claude-api` | API paga | `ANTHROPIC_API_KEY` (ou `ant auth login`) |
| `openai` | API paga | `OPENAI_API_KEY` |
| `huggingface` | API (Inference Providers) | `HF_TOKEN` (ou `hf auth login`) |

As chaves podem ficar num arquivo `.env` na raiz, que o git ignora (ex.: `ANTHROPIC_API_KEY=...`).
Elas nunca são impressas nem gravadas.

Fluxo recomendado:

```bash
uv run python executar_infra.py           # o que esta máquina oferece e o que é sugerido
uv run python executar_escolha_modelo.py  # aceitar a sugestão ou escolher por papel (opcional)
uv run python executar_teste_llm.py       # confirma que cada modelo escolhido responde
```

A escolha usada nas rodadas está congelada em `config/escolha_modelos.json` (modo manual):
classificador A = GPT `gpt-6.1-sol` (`codex-cli`), classificador B = Gemini 3.8 Flash `-low` (`gemini-agy`),
voto barato = GPT-OSS 120B `-medium` (`gemini-agy`) e verificador = Gemini 3.8 Flash `-medium` (`gemini-agy`),
sem gasto da cota do Claude Code. O `qwen3.5:4b` local saiu do voto barato: nesta GPU ele gera ~2 tokens/s
(~34 s por questão, ~3,4 h por rodada). Com `"modo": "auto"` (ou sem o arquivo), a
escolha é automática. O catálogo de candidatos
(qualidade estimada, preços, tamanhos) fica em `config/catalogo_modelos.json` e pode ser editado.

## Padrão de código

Definido na [ADR-001](docs/adr/00-fundacao/ADR-001-stack-e-ambiente.md) e conferido pelo `executar_checagem.py`:

- **Orientado a objetos**: cada etapa é um subpacote de `vicio_ia/` com uma classe orquestradora e um `executar_<etapa>.py`.
- **Sem argumentos de linha de comando**, sem `*args` nem `**kwargs`. A configuração fica em dataclasses congeladas.
- **Tudo tipado**, inclusive variáveis locais. Alvos de `for` e `with` são declarados antes; aliases usam `type X = ...`.
- **Docstrings** em módulos, classes e funções, em português.
- **Dependências** fixadas com `==`: execução em `requirements.txt`, desenvolvimento em `requirements-dev.txt`.
- O portão precisa passar antes de cada entrega:

```bash
uv run python executar_checagem.py
```

## Estrutura do repositório

```
├── README.md                  ← este arquivo
├── decisoes_manuais.md        ← toda decisão tomada à mão, com o porquê
├── executar_eda.py            ← EDA
├── executar_preparacao.py     ← passo 01: texto canônico das questões
├── executar_infra.py          ← análise da máquina e recomendação de modelos
├── executar_escolha_modelo.py ← escolha interativa de modelos por papel
├── executar_teste_llm.py      ← teste rápido dos modelos escolhidos
├── executar_cartoes.py        ← passo 02: cartões de tema
├── executar_classificacao.py  ← passos 05 e 06: classificação e verificação
├── executar_experimentos.py   ← experimentos no gold (E0, E2, E3)
├── executar_experimento_cartoes.py ← experimento E4 (cartões × títulos)
├── executar_decisao.py        ← passo 07: publicacao.csv e previsao.txt
├── executar_validacao.py      ← validação dos entregáveis
├── executar_pipeline.py       ← todos os passos, a partir do cache
├── executar_gold.py           ← gold set: sorteio, planilha, caderno e situação
├── executar_rotulagem.py      ← rotulagem interativa do gold set
├── executar_checagem.py       ← portão de qualidade
├── vicio_ia/                  ← código do pipeline
│   ├── configuracao.py        ← caminhos e parâmetros (sem argumentos de CLI)
│   ├── dominio.py, carregamento.py, texto.py, arvore.py, conhecimento.py, ambiente.py, relatorio.py, leitura_json.py
│   ├── eda/                   ← perfis e análises da EDA
│   ├── preparacao/            ← passo 01: texto canônico, árvore preparada, checagens e leitura das saídas
│   ├── temas/                 ← passo 02: cartões, versões da árvore para os prompts, revisão
│   ├── classificacao/         ← classificadores, voto barato, verificador, schemas, montador de prompt
│   ├── sinais/                ← sinais sem LLM (leis citadas)
│   ├── decisao/               ← agregação, recuo, política publicar/revisar/fora, publicacao.csv
│   ├── avaliacao/             ← gold set, régua, métricas, experimentos, calibração e previsão
│   ├── entrega/               ← validador dos entregáveis
│   ├── infra/                 ← analisador da máquina, catálogo, memória, recomendador
│   └── llm/                   ← contrato, provedores (ollama, claude-api/cli, gemini-agy, codex-cli, openai, huggingface), seleção, cache, custo
├── config/                    ← catálogo de modelos e escolha de modelos (editáveis)
├── prompts/                   ← prompts versionados de cada papel (a versão entra na chave do cache)
├── runs/                      ← cache de chamadas a modelos, só de acréscimo (respostas brutas)
├── ferramentas/               ← verificador de anotações e portão de qualidade
├── docs/
│   ├── adr/                   ← plano de implementação (ADRs por fase)
│   └── enunciado/             ← README original do case e PDF
├── dados/temas/              ← decisões manuais sobre a árvore (lixeiras, sobreposições, títulos)
├── dados/preparados/         ← saídas do passo 01 usadas pelos passos seguintes
├── dados/gold/               ← amostras, rótulos manuais e cadernos do gold set
├── saidas/eda/                ← relatório, resumo e tabelas da EDA
├── saidas/preparacao/         ← relatório e conferência do passo 01
├── saidas/infra/              ← perfil da máquina, recomendação, escolha resolvida, teste dos modelos
├── anexos/                    ← dados do case (não versionados; ver "Como rodar")
└── requirements.txt, requirements-dev.txt, ruff.toml, .python-version
```

## Entrega

As seções que o case exige no README serão preenchidas conforme o pipeline avança
([ADR-015](docs/adr/06-entrega/ADR-015-repositorio-e-entregaveis.md)):

- **Passos que geram o `publicacao.csv`:** a preencher.
- **Modelos usados, custo e tempo:** a preencher, com valores medidos do cache de chamadas ([ADR-003](docs/adr/00-fundacao/ADR-003-cache-reprodutibilidade-e-custo.md)).
- **Decisões tomadas à mão:** em [`decisoes_manuais.md`](decisoes_manuais.md) (D1 a D11 até agora).
