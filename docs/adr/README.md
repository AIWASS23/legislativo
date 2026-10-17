# Plano de implementação: classificação de tópicos (case Vício / Método VDE)

Este diretório é o plano de implementação da solução, escrito como um conjunto de
**ADRs** (*Architecture Decision Records*). Cada ADR registra uma decisão: o contexto,
as opções consideradas, o que foi escolhido, as consequências e os itens de ação que
implementam a decisão. As pastas seguem as fases do pipeline, e a numeração é única
entre pastas (ADR-001 a ADR-017), para que as referências não quebrem se um arquivo mudar de pasta.


---

## 1. Objetivo e régua

Para cada uma das **359 questões** (Penal, Processo Penal, Legislação Penal Especial e
Criminologia), decidir entre `publicar` (vai direto para o aluno), `revisar` (vai para o
professor com uma sugestão) ou `fora` (nenhum tema da árvore serve).

- **Régua:** das publicadas, **pelo menos 95% certas**. Respeitado isso, publicar o máximo possível.
- **Conta como certo:** o tema do especialista ou um nó do mesmo ramo (pai ou filho direto).
  Outro subtema do mesmo tema é erro.
- **Também é avaliado:** o quanto a previsão de precisão e cobertura (`previsao.txt`) acerta o
  resultado real; o raciocínio, o diagnóstico e o desenho para produção; a clareza para quem não é técnico.

## 2. Estado atual

| Item | Situação |
|---|---|
| Ambiente, padrão de código e portão de qualidade (`executar_checagem.py`) | Pronto: [ADR-001](00-fundacao/ADR-001-stack-e-ambiente.md) |
| Passo 01 completo (`executar_preparacao.py`): texto canônico das questões e árvore preparada | Pronto: [ADR-004](01-dados/ADR-004-texto-canonico-das-questoes.md) e [ADR-005](01-dados/ADR-005-tratamento-da-arvore-de-temas.md); decisões em `decisoes_manuais.md` |
| Provedores de LLM plugáveis, análise de infraestrutura e escolha de modelos | Pronto: [ADR-002](00-fundacao/ADR-002-provedor-e-modelos-de-llm.md) (decisão) e [ADR-017](00-fundacao/ADR-017-provedores-plugaveis-e-analise-de-infra.md) (implementação) |
| EDA de questões e árvore (`executar_eda.py`, `saidas/eda/`) | Pronta: base de [ADR-004](01-dados/ADR-004-texto-canonico-das-questoes.md), [ADR-005](01-dados/ADR-005-tratamento-da-arvore-de-temas.md), [ADR-006](01-dados/ADR-006-rotulos-de-origem-como-sinal-fraco.md) |
| Cache de chamadas e custo; cartões de tema (`executar_cartoes.py`); classificação e verificação (`executar_classificacao.py`) | Prontos: [ADR-003](00-fundacao/ADR-003-cache-reprodutibilidade-e-custo.md), [ADR-007](02-temas/ADR-007-cartoes-de-tema.md) e [ADR-008](03-classificacao/ADR-008-arquitetura-de-classificacao.md); rodada completa das 359 feita; cartões sem revisão manual (D7) |
| Gold set (`executar_gold.py`, `executar_rotulagem.py`): sorteio, planilha, caderno, rotulagem interativa e régua | Pronto: [ADR-012](05-avaliacao/ADR-012-gold-set-manual-cego.md); 60 questões rotuladas à mão; decisão D6 |
| Decisão, calibração, previsão, experimentos e gráficos (`executar_decisao.py`, `executar_graficos.py`) | Prontos: [ADR-010](04-decisao/ADR-010-granularidade-e-recuo-para-o-pai.md), [ADR-011](04-decisao/ADR-011-politica-publicar-revisar-fora.md), [ADR-013](05-avaliacao/ADR-013-calibracao-e-previsao.md), [ADR-014](05-avaliacao/ADR-014-experimentos-e-registro.md); 81 publicar, 276 revisar, 2 fora |
| Entrega: README, relatório (com o memo) e validador | Pronto: [ADR-015](06-entrega/ADR-015-repositorio-e-entregaveis.md); faltam o push público e o e-mail |
| Produção | Desenho na [ADR-016](07-producao/ADR-016-arquitetura-de-producao.md) e na seção c do relatório |

## 3. Visão do pipeline

```
anexos/ ──► [01] preparar ──► questões limpas + árvore marcada (fantasmas, lixeiras, sobreposições)
                 │
                 ├──► [02] cartões de tema (LLM + revisão humana)
                 ├──► [03] sinais por regra (leis citadas)          ─┐
                 ├──► [04] embeddings (opcional, ADR-009)            │
                 │                                                   ▼
                 └──► [05] classificador A (árvore plana)  ─┐
                      [05] classificador B (hierárquico)    ─┼─► [06] verificador contrastivo
                      [05] voto barato                      ─┘              │
                                                                                    ▼
      Modelo de cada papel: papéis e critérios na ADR-002; escolha pela máquina na ADR-017.
      Nesta máquina: A = Claude Opus (CLI claude), B = Gemini Flash (CLI agy),
      voto barato = qwen3.5:4b (Ollama), verificador = Claude Opus.

      gold set manual cego (ADR-012) ──► [08] calibração ──► [07] agregação + recuo + política de decisão
                                                 │                                  │
                                                 ▼                                  ▼
                                           previsao.txt                     publicacao.csv
```

## 4. Índice das ADRs

| Nº | Decisão | Pasta (fase) | Status |
|---|---|---|---|
| [001](00-fundacao/ADR-001-stack-e-ambiente.md) | Stack, ambiente e padrão de código | 00-fundacao | Aceito |
| [002](00-fundacao/ADR-002-provedor-e-modelos-de-llm.md) | Provedores e modelos de LLM (independência de provedor, papéis por critério) | 00-fundacao | Aceito (revisão 2) |
| [003](00-fundacao/ADR-003-cache-reprodutibilidade-e-custo.md) | Cache de chamadas, reprodutibilidade e custo | 00-fundacao | Aceito (implementado) |
| [004](01-dados/ADR-004-texto-canonico-das-questoes.md) | Texto canônico das questões | 01-dados | Aceito (implementado) |
| [005](01-dados/ADR-005-tratamento-da-arvore-de-temas.md) | Tratamento da árvore (fantasmas, lixeiras, sobreposições) | 01-dados | Aceito (implementado) |
| [006](01-dados/ADR-006-rotulos-de-origem-como-sinal-fraco.md) | Rótulos de origem como sinal fraco | 01-dados | Aceito |
| [007](02-temas/ADR-007-cartoes-de-tema.md) | Cartões de tema | 02-temas | Aceito (rascunhos gerados; sem revisão manual) |
| [008](03-classificacao/ADR-008-arquitetura-de-classificacao.md) | Arquitetura de classificação (ensemble + verificador) | 03-classificacao | Aceito (rodada completa das 359) |
| [009](03-classificacao/ADR-009-embeddings.md) | Embeddings como sinal opcional | 03-classificacao | Proposto |
| [010](04-decisao/ADR-010-granularidade-e-recuo-para-o-pai.md) | Granularidade e recuo para o tema pai | 04-decisao | Aceito (implementado) |
| [011](04-decisao/ADR-011-politica-publicar-revisar-fora.md) | Política publicar / revisar / fora | 04-decisao | Aceito (implementado) |
| [012](05-avaliacao/ADR-012-gold-set-manual-cego.md) | Gold set manual cego | 05-avaliacao | Aceito (60 questões rotuladas) |
| [013](05-avaliacao/ADR-013-calibracao-e-previsao.md) | Calibração e previsão de precisão e cobertura | 05-avaliacao | Aceito (implementado) |
| [014](05-avaliacao/ADR-014-experimentos-e-registro.md) | Experimentos e registro dos becos sem saída | 05-avaliacao | Aceito (E0 a E5 feitos; E6 não rodado) |
| [015](06-entrega/ADR-015-repositorio-e-entregaveis.md) | Repositório e entregáveis | 06-entrega | Aceito (faltam o push público e o e-mail) |
| [016](07-producao/ADR-016-arquitetura-de-producao.md) | Arquitetura de produção (50 mil questões/semana) | 07-producao | Proposto (desenho para o relatório) |
| [017](00-fundacao/ADR-017-provedores-plugaveis-e-analise-de-infra.md) | Análise da máquina e recomendação de modelos (implementa a ADR-002) | 00-fundacao | Aceito |

**Status:** *Proposto* = decidido para implementar, pode mudar com os experimentos;
*Aceito* = implementado ou em vigor; *Substituído* = trocado por outra ADR (indicar qual).
Para registrar uma decisão nova, copie [`template.md`](template.md).

## 5. Roteiro de implementação

Cada passo vira um subpacote de `vicio_ia/` com uma classe orquestradora e um ponto de
entrada `executar_<passo>.py` sem argumentos ([ADR-001](00-fundacao/ADR-001-stack-e-ambiente.md)).

| Passo | Entregável | Módulo / entrada | ADRs | Pronto quando |
|---|---|---|---|---|
| 01 preparar (pronto) | `dados/preparados/questoes.jsonl`, `temas.json`, `arvore_enxuta.txt` | `vicio_ia/preparacao/`, `executar_preparacao.py` | 004, 005, 006 | Feito: 359 questões com texto canônico; 351 temas publicáveis com canônico, lixeira, sobreposição e tipo de convenção |
| 02 cartões | `dados/temas/cartoes.jsonl` | `vicio_ia/temas/`, `executar_cartoes.py` | 007 | Feito: 351 cartões (rascunhos do modelo; revisão manual não coube: D7) |
| 03 regras | sinais por questão | `vicio_ia/sinais/regras.py` | 006, 008 | Lei citada → temas válidos |
| 04 embeddings | top-k por questão (opcional) | `vicio_ia/sinais/embeddings.py` | 009 | Só se o E1 mostrar ganho |
| 05 classificar | respostas A, B e voto barato | `vicio_ia/llm/` (pronto), `vicio_ia/classificacao/`, `prompts/` | 003, 008, 017 | 359 × 3 respostas válidas, em cache |
| 06 verificar | veredito por candidata | `vicio_ia/classificacao/verificador.py` | 008 | Candidatas a publicar verificadas |
| 07 decidir | `publicacao.csv` | `vicio_ia/decisao/`, `executar_decisao.py` | 010, 011 | Feito: validador passa; motivos preenchidos |
| 08 avaliar | gold set (`dados/gold/`), calibração, `previsao.txt`, registro de experimentos | `vicio_ia/avaliacao/`, `executar_gold.py`, `executar_rotulagem.py`, `executar_experimentos.py`, `executar_graficos.py` | 012, 013, 014 | Feito: gold rotulado (60), régua, calibração por faixas, previsão, gráficos e experimentos E0 a E5 registrados |
| 09 entregar | relatório, memo, README, repositório público | `docs/`, `relatorio/` | 015, 016 | Feito, menos o push público e o e-mail |

## 6. Cronograma

| Dia | Trabalho |
|---|---|
| **Qua 14/10** | Ambiente e EDA (feitos). ADRs. E-mail para a Carla (seção 7). Passo 01. Gold set (60 questões). |
| **Qui 15/10** | Passos 02 e 03. Cliente LLM com cache. Classificador A nas 359. Experimentos E0 e E2. Gold até 60. |
| **Sex 16/10** | Classificador B, voto barato, verificador, agregação e recuo. E3 a E6. **Congelar prompts e regras.** |
| **Sáb 17/10** | Calibração, limiar, `previsao.txt`, `publicacao.csv` com validador. Rascunho do relatório e do memo. |
| **Dom 18/10** | Relatório final, README, revisão, repositório público, e-mail com o link. Folga para imprevistos. |

## 7. Perguntas para a Carla (enviar em 14/10)

| Pergunta | Afeta |
|---|---|
| ~~Um nó duplicado conta como certo?~~ **Respondida (15/10): a critério do autor.** Decisão D1 em `decisoes_manuais.md` | ADR-005, ADR-011, ADR-013 |
| "Pai ou filho" inclui a disciplina (nível 0)? | ADR-010 |
| Como `fora` é avaliado? O especialista também marca questões como fora? | ADR-011 |
| A cobertura é medida sobre as 359 ou só sobre "as questões que guardamos"? | ADR-013 |
| Em `confianca` de uma linha `fora`, o que esperam (chance de ser fora mesmo)? | ADR-011 |

Enquanto não houver resposta, cada ADR afetada adota a opção conservadora: na dúvida, `revisar`.

## 8. Riscos principais

| Risco | Mitigação | ADR |
|---|---|---|
| Convenção dos especialistas diferente (duplicados, Ação Penal em Penal × Processo Penal) | Perguntar; mandar para revisão; margem de convenção no intervalo | 005, 011, 013 |
| Gold pequeno, intervalo largo | Limiar pelo limite inferior da calibração; só publica a faixa com evidência suficiente | 012, 013 |
| Sobreajuste do limiar e dos prompts ao gold | Validação cruzada (P fora da amostra); prompts congelados antes da rodada final | 012, 014 |
| Erros correlacionados no ensemble | Sinais de naturezas diferentes; verificador contrastivo | 008 |
| Custo ou falha de API | Cache em disco, Batch API, rodar primeiro no gold | 002, 003 |
| Falta de tempo | Embeddings opcionais; domingo como folga; o que faltar vai para "com mais tempo" | 009, 015 |

## 9. Definição de pronto da entrega

- [x] `publicacao.csv` com 359 linhas, aprovado pelo validador ([ADR-015](06-entrega/ADR-015-repositorio-e-entregaveis.md)).
- [x] `previsao.txt` com pontos, intervalos e explicação ([ADR-013](05-avaliacao/ADR-013-calibracao-e-previsao.md)).
- [x] Relatório com até 5 páginas (seções a–d) e memo de 1 página para o professor.
- [x] README: como rodar, que passos geram o `publicacao.csv`, modelos, custo, tempo e decisões manuais.
- [x] `decisoes_manuais.md` com toda decisão tomada à mão.
- [x] `uv run python executar_checagem.py` aprovado (ruff, formatação, mypy estrito, anotações e docstrings).
- [ ] Repositório público no GitHub e link enviado para carla@viciodeumaestudante.com.br.
