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
| Passo 01, parte 1: texto canônico das questões ([ADR-004](docs/adr/01-dados/ADR-004-texto-canonico-das-questoes.md)) | Pronto: `dados/preparados/questoes.jsonl` |
| Provedores de LLM plugáveis e escolha de modelos pela máquina ([ADR-017](docs/adr/00-fundacao/ADR-017-provedores-plugaveis-e-analise-de-infra.md)) | Pronto: [`saidas/infra/relatorio_infra.md`](saidas/infra/relatorio_infra.md) |
| Análise exploratória (EDA) dos dados | Pronta: [`saidas/eda/relatorio_eda.md`](saidas/eda/relatorio_eda.md) |
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
| `uv run python executar_preparacao.py` | Passo 01: texto canônico das questões, com 8 checagens automáticas | `dados/preparados/questoes.jsonl`, `saidas/preparacao/` (relatório e amostra de conferência) |
| `uv run python executar_infra.py` | Analisa a máquina (CPU, RAM, GPU, Ollama, CLIs, credenciais) e recomenda um modelo por papel | `saidas/infra/relatorio_infra.md`, `perfil_maquina.json` |
| `uv run python executar_escolha_modelo.py` | Escolha interativa dos modelos (sugestão automática ou um por papel) | `config/escolha_modelos.json` |
| `uv run python executar_teste_llm.py` | Uma questão simples por modelo escolhido: funcionou? acertou? latência e tokens | `saidas/infra/teste_llm.json` |
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
| `gemini-agy` | assinatura | CLI `agy` (Antigravity) com login feito |
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

Sem `config/escolha_modelos.json`, a escolha é automática. O catálogo de candidatos
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
├── executar_eda.py            ← EDA
├── executar_preparacao.py     ← passo 01: texto canônico das questões
├── executar_infra.py          ← análise da máquina e recomendação de modelos
├── executar_escolha_modelo.py ← escolha interativa de modelos por papel
├── executar_teste_llm.py      ← teste rápido dos modelos escolhidos
├── executar_checagem.py       ← portão de qualidade
├── vicio_ia/                  ← código do pipeline
│   ├── configuracao.py        ← caminhos e parâmetros (sem argumentos de CLI)
│   ├── dominio.py, carregamento.py, texto.py, arvore.py, conhecimento.py, ambiente.py, relatorio.py
│   ├── eda/                   ← perfis e análises da EDA
│   ├── preparacao/            ← passo 01: texto canônico e checagens
│   ├── infra/                 ← analisador da máquina, catálogo, memória, recomendador
│   └── llm/                   ← contrato, provedores (ollama, claude-api/cli, gemini-agy, openai, huggingface), seleção
├── config/                    ← catálogo de modelos e escolha de modelos (editáveis)
├── ferramentas/               ← verificador de anotações e portão de qualidade
├── docs/
│   ├── adr/                   ← plano de implementação (ADRs por fase)
│   └── enunciado/             ← README original do case e PDF
├── dados/preparados/         ← saídas do passo 01 usadas pelos passos seguintes
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
- **Decisões tomadas à mão:** em `decisoes_manuais.md` (a criar).
