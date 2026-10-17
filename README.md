# Classificação de tópicos de questões jurídicas: case Vício (Método VDE)

Solução para o case de IA da Vício: decidir, para cada uma das 359 questões de Penal,
Processo Penal, Legislação Penal Especial e Criminologia, entre **publicar** (direto para o
aluno, num tema da árvore), **revisar** (fila do professor, com sugestão) ou **fora**
(nenhum tema serve). A régua é **95% de acerto nas publicadas**, publicando o máximo possível.

- Enunciado original: [`docs/enunciado/`](docs/enunciado/) (README do case e PDF).
- Plano de implementação, em ADRs: [`docs/adr/README.md`](docs/adr/README.md).

## Resultado

| Entregável | Conteúdo |
|---|---|
| [`relatorio/publicacao.csv`](relatorio/publicacao.csv) | 359 linhas no formato do LEIA-ME: **81 publicar** (23%), **276 revisar** (todas com tema sugerido, extras e motivo) e **2 fora** |
| [`relatorio/previsao.txt`](relatorio/previsao.txt) | Precisão prevista **0,97** (0,93–1,00); cobertura **0,23** (0,22–0,24); como chegamos nesses números e o que não foi medido |
| [`relatorio/relatorio.md`](relatorio/relatorio.md) ([PDF](relatorio/relatorio.pdf), 5 páginas) | a) como pensei; b) diagnóstico; c) produção; o que faria com mais tempo; d) memo para o professor |
| [`decisoes_manuais.md`](decisoes_manuais.md) | Toda decisão tomada à mão (D1 a D12), com o porquê |
| [`saidas/decisao/relatorio_decisao.md`](saidas/decisao/relatorio_decisao.md) | Motivos de revisar e fora, calibração e escolha do calibrador |
| [`saidas/avaliacao/graficos.md`](saidas/avaliacao/graficos.md) | Confiabilidade e precisão × cobertura (gold e 359) |
| [`saidas/experimentos/registro.md`](saidas/experimentos/registro.md) | Experimentos E0 a E5: hipótese, resultado e decisão |
| [`saidas/custos/resumo_custos.md`](saidas/custos/resumo_custos.md) | Chamadas, tokens, tempo e custo por papel, medidos no cache |

## Como rodar

### 1. Pré-requisitos

- [uv](https://docs.astral.sh/uv/). Ele instala o Python 3.12 (fixado em `.python-version`) se não houver um na máquina.
- Os anexos do case (`questoes.jsonl`, `temas.csv`, `LEIA-ME.md` e `entrega_modelo.csv`) já vêm no
  repositório, em `anexos/`, como foram recebidos. A origem é o
  [ZIP dos anexos](https://github.com/viciod/case-vicio-ia/raw/main/anexos-case-ia.zip) do case.

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
| `uv run python executar_congelamento.py` | Congela o pipeline antes da rodada final: impressão digital de prompts, cartões, árvores, decisões, modelos e código | `saidas/experimentos/congelamento.json`, `registro.md` |
| `uv run python executar_decisao.py` | Passo 07: agregação, recuo para o pai, regras que forçam revisão, calibração no gold, limiar e previsão. Não chama modelo | `relatorio/publicacao.csv`, `relatorio/previsao.txt`, `saidas/decisao/`, `dados/decisao/` |
| `uv run python executar_gold.py` | Gold set: sorteio estratificado com semente fixa (ou reaproveita o gravado), planilha de rótulos (nunca sobrescrita), caderno e situação da rotulagem | `dados/gold/` (`amostra_leva1.csv`, `rotulos_leva1.csv`, `caderno_leva1.md`) |
| `uv run python executar_rotulagem.py` | Rotulagem interativa no terminal: só o texto canônico, busca de temas na árvore, grava a cada questão e retoma de onde parou | `dados/gold/rotulos_leva1.csv` |
| `uv run python executar_validacao.py` | Confere `relatorio/publicacao.csv` e `relatorio/previsao.txt` contra o formato do LEIA-ME (sai com código 1 se houver problema) | Resumo no terminal |
| `uv run python executar_pipeline.py` | Roda tudo em ordem (01, 02, 05/06, 07) e valida a entrega; com o cache `runs/` completo, não chama nenhum modelo | Todos os acima |
| `uv run python executar_graficos.py` | Gráficos de confiabilidade e de precisão × cobertura (gold e 359), com as tabelas equivalentes | `saidas/avaliacao/` (PNG, SVG, `graficos.md`) |
| `uv run python executar_testes.py` | Testes unitários (recuo para o pai, política de decisão, colunas do `publicacao.csv`, régua e corte do limiar); também rodam no portão | Resumo no terminal |
| `uv run python executar_checagem.py` | Portão de qualidade: ruff, formatação, mypy estrito, anotações e docstrings | Resumo no terminal; código de saída 1 se algo falhar |


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

As chaves podem ficar num arquivo `.env` na raiz, que o git ignora. O modelo, com as variáveis de
`claude-api`, `openai` e `huggingface`, está em [`.env.example`](.env.example):

```bash
cp .env.example .env   # e preencha só as chaves dos provedores que for usar
```

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
- Testes unitários com o `unittest` da biblioteca padrão, em `testes/` (métodos `teste_*`).
- O portão (ruff, mypy estrito, testes e anotações) precisa passar antes de cada entrega:

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
├── executar_congelamento.py   ← congelamento do pipeline antes da rodada final (D11)
├── executar_decisao.py        ← passo 07: publicacao.csv e previsao.txt
├── executar_validacao.py      ← validação dos entregáveis
├── executar_pipeline.py       ← todos os passos, a partir do cache
├── executar_gold.py           ← gold set: sorteio, planilha, caderno e situação
├── executar_rotulagem.py      ← rotulagem interativa do gold set
├── executar_graficos.py       ← gráficos de confiabilidade e de precisão × cobertura
├── executar_testes.py         ← testes unitários
├── executar_checagem.py       ← portão de qualidade
├── relatorio/                 ← entregáveis: publicacao.csv, previsao.txt e o relatório (Markdown e PDF; o memo é a seção d)
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
├── testes/                    ← testes unitários (unittest)
├── docs/
│   ├── adr/                   ← plano de implementação (ADRs por fase)
│   └── enunciado/             ← README original do case e PDF
├── dados/temas/              ← decisões manuais sobre a árvore (lixeiras, sobreposições, títulos)
├── dados/preparados/         ← saídas do passo 01 usadas pelos passos seguintes
├── dados/gold/               ← amostra, rótulos manuais e caderno do gold set
├── dados/classificacao/      ← sinais de cada questão (votos, regras, verificador)
├── dados/decisao/            ← decisões preliminares (antes do limiar)
├── saidas/eda/                ← relatório, resumo e tabelas da EDA
├── saidas/preparacao/         ← relatório e conferência do passo 01
├── saidas/cartoes/            ← checagens e revisão dos cartões de tema
├── saidas/classificacao/      ← resumo das rodadas de classificação
├── saidas/decisao/            ← relatório da decisão e da calibração
├── saidas/avaliacao/          ← gráficos de confiabilidade e de precisão × cobertura
├── saidas/experimentos/       ← resultados, registro dos experimentos e congelamento
├── saidas/custos/             ← custo e tempo por papel
├── saidas/infra/              ← perfil da máquina, recomendação, escolha resolvida, teste dos modelos
├── anexos/                    ← dados do case, como foram recebidos (nunca alterados)
├── .env.example               ← modelo das chaves de API (copiar para .env)
└── requirements.txt, requirements-dev.txt, ruff.toml, .python-version
```

## Entrega

### Passos que geram o `publicacao.csv`

Os entregáveis ficam em [`relatorio/`](relatorio/): `publicacao.csv`, `previsao.txt` e o relatório.

Com os anexos em `anexos/` e o cache `runs/` do repositório, um comando refaz tudo **sem chamar nenhum
modelo**, em segundos (3,7 s medidos), e gera o mesmo `publicacao.csv`, byte a byte:

```bash
uv run python executar_pipeline.py
```

Ele roda, em ordem:

| Passo | Comando | O que faz | Saída usada adiante |
|---|---|---|---|
| 01 | `executar_preparacao.py` | Texto canônico das questões (sem HTML, sem os rótulos de origem) e árvore preparada com as decisões de `dados/temas/` (D1 a D4) | `dados/preparados/` |
| 02 | `executar_cartoes.py` | Cartões de tema (definição, o que entra, o que não entra) e as versões da árvore para os prompts | `dados/temas/cartoes.jsonl` |
| 05/06 | `executar_classificacao.py` | Classificador A (plano), classificador B (hierárquico), voto barato, regras das leis citadas e verificador contrastivo | `dados/classificacao/sinais.jsonl` |
| 07 | `executar_decisao.py` | Agregação, recuo para o pai, regras que forçam revisão, calibração por faixas no gold (`dados/gold/rotulos_leva1.csv`), limiar pelo limite inferior e previsão | `relatorio/publicacao.csv`, `relatorio/previsao.txt` |
| — | `executar_validacao.py` | Confere os dois entregáveis contra o LEIA-ME | — |

- **Congelamento:** o passo 07 confere a impressão digital de prompts, cartões, árvores, regras, modelos e
  código registrada antes da rodada final (D11). Se algo mudou depois disso, ele avisa.
- **Sem cache:** a mesma sequência chama os modelos de `config/escolha_modelos.json`. São ~1.700 chamadas,
  e as cotas das assinaturas espalharam a rodada por dois dias.
- **Outros passos:** os experimentos (`executar_experimentos.py`, `executar_experimento_cartoes.py`) e os
  gráficos (`executar_graficos.py`) não alteram o `publicacao.csv`.

### Modelos usados

Todos pelas assinaturas que eu já tinha, pela camada `vicio_ia/llm/`, sem chave de API paga.

| Papel | Modelo | Acesso | Chamadas | Tempo médio |
|---|---|---|---:|---:|
| Cartões de tema (351 temas, uma chamada por tema pai) | Claude Opus 5.5 | CLI `claude` | 58 | 51 s |
| Classificador A (plano, árvore com escopo) | GPT `gpt-6.1-sol` | CLI `codex` | 369 | 8 s |
| Classificador B (hierárquico, duas etapas) | Gemini 3.8 Flash `-low` | CLI `agy` | 642 | 18 s |
| Voto barato (árvore enxuta) | GPT-OSS 120B `-medium` | CLI `agy` | 374 | 18 s |
| Verificador contrastivo | Gemini 3.8 Flash `-medium` | CLI `agy` | 326 | 33 s |
| Experimento E4 (B só com títulos) | Gemini 3.8 Flash `-low` | CLI `agy` | 107 | 20 s |

Algumas chamadas ficaram no cache, mas não entram na decisão:
- 13 do verificador com Claude Opus, antes da troca para o Gemini, que aconteceu quando a cota acabou (D8);
- 14 do voto barato com o `qwen3.5:4b` local, abandonado por ser lento (~2 tokens/s nesta GPU).

### Custo e tempo

- **Chamadas:** 1.903 ao todo, com 74 milhões de tokens de entrada e 4,6 milhões de saída. As CLIs
  acrescentam de 13 a 66 mil tokens do próprio agente a cada chamada.
- **Custo:** US$ 0 pagos.
  - A CLI `claude` informa o equivalente na API: US$ 14,81, todo dos cartões.
  - `codex` e `agy` não informam custo.
  - O custo real foi a cota das assinaturas.
- **Tempo de máquina:** 10,6 h de chamadas somadas, menos em tempo de relógio graças ao paralelismo. As
  cotas espalharam as rodadas entre 15 e 17/10.
- **Tempo humano:**
  - 3 h para rotular as 60 questões do gold;
  - conferência manual do texto canônico (D5);
  - as decisões sobre a árvore (D1 a D4).
- **Refazer a entrega a partir do cache:** segundos, sem custo.

### Decisões tomadas à mão

Estão em [`decisoes_manuais.md`](decisoes_manuais.md), cada uma com o porquê:

| | Decisão |
|---|---|
| D1 | Nos temas duplicados, vale o nó com histórico de questões; os 20 fantasmas nunca são tema central |
| D2 | Regra de desempate das 6 sobreposições (lado material × processual) |
| D3 | Lixeiras em dois níveis (11 fortes, 7 moderadas; 3 falsos positivos descartados) |
| D4 | 9 títulos com erro corrigidos só para exibição nos prompts |
| D5 | Conferência manual do texto canônico, que gerou três correções |
| D6 | Gold set: sorteio, protocolo de rotulagem cega e tempo gasto |
| D7 | Cartões de tema com modelo fixo, sem revisão manual antes do congelamento |
| D8 | Modelos por papel fora da cota do Claude Code; verificador da mesma família de B (risco aceito) |
| D9 | Regras de decisão definidas na implementação (recuo pelo verificador, extras, confiança de fora, margens) |
| D10 | Calibração por faixas de sinais e chance efetiva com desconto de convenção |
| D11 | Congelamento antes da rodada final e os recongelamentos de 17/10, todos sem efeito nas decisões |
| D12 | Estimador direto da precisão suavizado (Jeffreys): ponto de 0,99 para 0,97 |

### O que ficou de fora

- **Cartões:** os rascunhos do modelo não foram revisados por um especialista.
- **E6** (modelos por papel) e **E1** (embeddings) não rodaram.
- **Previsão:** não foi testada numa amostra independente, porque a mesma amostra calibrou e conferiu.

O que eu faria com mais tempo está no fim da seção c do [relatório](relatorio/relatorio.md#o-que-faria-com-mais-tempo).
