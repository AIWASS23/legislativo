# ADR-026: Entrega, reprodutibilidade e repositório na etapa 2

**Status:** Implementado (21/10/2026). Revisa a ADR-015 para a etapa 2.
**Data:** 20/10/2026
**Decisores:** Autor do case
**Fase:** 08-etapa2 (entrega)
**Relacionadas:** ADR-003, ADR-015, ADR-018, ADR-019

## Contexto

- **O que o enunciado pede:**
  - um repositório público com `publicacao.csv` (659 linhas), `previsao.txt` (para as 559), o relatório e o
    código;
  - **um comando** que regenera o `publicacao.csv` a partir dos anexos, sem modelo de linguagem;
  - os **artefatos versionados**;
  - um README com **como rodar, quanto tempo leva e de onde veio cada artefato**;
  - as decisões tomadas à mão registradas;
  - **relatório de até 4 páginas** (seções a–e), com o memo de 1 página.
- **Os anexos foram movidos para `anexos/1-ENTREGA/` e `anexos/2-ENTREGA/`.** O código ainda lê
  `anexos/questoes.jsonl`, então o pipeline está quebrado até o ajuste.
- **A entrega da etapa 1** (commit `02d7e19`, publicada) precisa continuar acessível para comparação.

## Decisão

**1. Anexos.**
- `Caminhos` ganha a pasta da etapa, configurável em `configuracao.py`, com padrão `anexos/2-ENTREGA`.
- Os anexos da etapa 1 ficam intactos em `anexos/1-ENTREGA/`, para reproduzir a etapa 1 se for preciso.

**2. Etapa 1 preservada.**
- A etapa 1 fica no commit `02d7e19` (sem tag, por decisão do autor).
- Os entregáveis da etapa 1 vão para `relatorio/etapa1/`: `publicacao.csv`, `previsao.txt`,
  `relatorio.md`, `relatorio.pdf` e `arquitetura.png`.
- Os da etapa 2 ocupam `relatorio/etapa2/` (`Caminhos.entregaveis` depende da etapa).

**3. Comandos.**

| Comando | Fase | O que faz | Chama modelo? |
|---|---|---|---|
| `uv run python executar_enriquecimento.py` | Conhecimento | Propostas de termos e de mapa de artigos para revisão (ADR-020), manifesto | Sim (cache) |
| `uv run python executar_citacoes.py` | Conhecimento | Citações de lei e artigo das 659 questões, por regex (`dados/conhecimento/citacoes.jsonl`) | Não |
| `uv run python executar_embeddings.py` | Conhecimento | Vetores dos candidatos (cache em `runs/embeddings/`), E8 e E9, exportação do modelo escolhido para `dados/conhecimento/embeddings/` | Embedding local (Ollama), com cache |
| `uv run python executar_revisao_conhecimento.py` | Conhecimento | Revisão interativa das propostas (ADR-020) | Não |
| `uv run python executar_sistema.py` | Decisão | Treina com a folha, calibra, decide; grava `relatorio/etapa2/publicacao.csv` e `relatorio/etapa2/previsao.txt` | **Não** (trava da ADR-019) |
| `uv run python executar_avaliacao_etapa2.py` | Avaliação | Experimentos E7 a E12, gráficos e métricas fora da amostra | Não |
| `uv run python executar_validacao.py` | Entrega | Confere os entregáveis contra o LEIA-ME novo | Não |

**4. Validador atualizado.**
- **`publicacao.csv`:** 659 linhas, IDs únicos, tema ativo e publicável; `fora` sem tema; motivo em `revisar`
  e em `fora`; confiança em [0, 1].
- **`previsao.txt`:** as quatro linhas do formato, e a cobertura prevista igual à observada nas 559.

**5. Tempo e reprodução.**
- O `executar_sistema.py` mede o próprio tempo e grava em `saidas/sistema/execucao.json`. Meta: menos de 1
  minuto num notebook comum.
- **Roteiro de reprodução do zero:**
  1. clonar num diretório temporário;
  2. rodar `uv sync`;
  3. rodar `executar_sistema.py` com a rede bloqueada e sem credenciais;
  4. conferir o SHA-256 do `publicacao.csv`.
- O hash e o tempo vão para o README e para o relatório.

**6. README.**
- **Origem de cada artefato:** uma tabela gerada do manifesto da ADR-019, com origem, modelo, revisão e hash.
- **Tempos:** os da fase de conhecimento, medidos uma vez, e os da decisão.
- **Decisões tomadas à mão:** D13 em diante, em `decisoes_manuais.md`.

**7. Relatório.**
- `relatorio/etapa2/relatorio.md` e o PDF, com até 4 páginas, nas seções a–e do enunciado:
  - a) o sistema;
  - b) os 100 rótulos;
  - c) diagnóstico;
  - d) produção;
  - e) memo, em 1 página.
- O PDF é gerado a partir do Markdown, como na etapa 1.

**8. Portão de qualidade.** O mesmo da etapa 1 (ruff, mypy estrito, anotações e testes), mais os testes novos:
- a fronteira do LLM;
- a escolha do nó pela régua;
- as regras de fora;
- o validador de 659 linhas;
- o determinismo: duas execuções geram o mesmo arquivo, byte a byte.

## Opções consideradas

### Opção A: sobrescrever a etapa 1 sem arquivar

**Contras:** perde a comparação. A própria etapa 2 usa a etapa 1 como linha de base no relatório.

### Opção B: tag mais pasta de arquivo (escolhida)

**Prós:** a etapa 1 fica acessível pela tag e legível no repositório. A etapa 2 fica limpa em `relatorio/etapa2/`.

### Opção C: um repositório novo para a etapa 2

**Contras:** o enunciado fala na continuação do mesmo case. Repositório novo duplica histórico e confunde o
envio.

## Análise de trade-offs

A banca vai clonar e rodar. O que conta é um comando, sem rede nem credenciais, que gere sempre o mesmo
arquivo. A tag e a pasta de arquivo mantêm a etapa 1 visível sem atrapalhar a leitura da etapa 2.

## Consequências

- `executar_pipeline.py` passa a ser o pipeline da etapa 1. O README aponta para `executar_sistema.py` como
  o comando principal.
- O link do enunciado no README precisa apontar para os dois PDFs, ou para o repositório original do case,
  porque `docs/enunciado/` está no `.gitignore`.

## Itens de ação

1. [x] `Caminhos`: pasta da etapa configurável; passo 01 lendo `anexos/2-ENTREGA`.
2. [x] A pasta `relatorio/etapa1/` e o commit `02d7e19`. A tag foi dispensada pelo autor.
3. [x] Pontos de entrada da tabela acima, sem argumentos, no padrão da ADR-001.
4. [x] Validador para 659 linhas e para a previsão das 559.
5. [x] Medida de tempo e hash dos entregáveis no README. A reprodução num clone limpo foi feita pelo autor (21/10).
6. [x] README e relatório da etapa 2 (`relatorio/etapa2/`).
