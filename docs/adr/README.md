# Plano de implementação: classificação de tópicos (case Vício / Método VDE)

Este diretório é o plano de implementação da solução, escrito como um conjunto de
**ADRs** (*Architecture Decision Records*). Cada ADR registra uma decisão: o contexto,
as opções consideradas, o que foi escolhido, as consequências e os itens de ação que
implementam a decisão. As pastas seguem as fases do pipeline, e a numeração é única
entre pastas (ADR-001 a ADR-027), para que as referências não quebrem se um arquivo mudar de pasta.

**Etapa 2 (desde 20/10/2026):** a seção 0 resume o que mudou. As ADR-018 a ADR-027, em
[`08-etapa2/`](08-etapa2/), revisam o plano para um sistema que decide **sem modelo de linguagem**.


---

## 0. Etapa 2: sistema de classificação sem LLM na decisão

**Enunciado:** `docs/enunciado/case-ia-classificacao-de-topicos-ajustes.pdf`. **Anexos:** `anexos/2-ENTREGA/`.

- **Dados:**
  - 659 questões (Q0001–Q0359 iguais às da etapa 1; Q0360–Q0659 novas) e os mesmos 377 temas;
  - `folha_verdade.csv`: 100 questões rotuladas pela equipe;
  - a avaliação é feita nas 559 questões fora da folha.
- **Regra do LLM:**
  - pode entrar antes da decisão, documentado e versionado: embeddings, limpeza, extração de lei e artigo,
    descrição dos temas, termos e exemplos revisados;
  - não pode escolher, votar, julgar nem validar;
  - a classificação roda sem chamar modelo.
- **Régua:** ≥ 95% de acerto nas publicadas. Conta como certo o tema central, um extra, ou o pai ou filho
  de um deles.
- **Entregáveis:**
  - `publicacao.csv` (659 linhas) e `previsao.txt` (para as 559);
  - relatório de até 4 páginas, com as seções a–e;
  - um comando que regenera a saída sem LLM;
  - artefatos versionados, e um README com o tempo de execução e a origem de cada artefato.
- **Prazo:** pedir mais prazo antes de quinta, 22/10. O limite é segunda, 26/10.

| Nº | Decisão | Status |
|---|---|---|
| [018](08-etapa2/ADR-018-etapa-2-escopo-e-regras.md) | Escopo, regras novas e o que muda; achados da folha | Aceito |
| [019](08-etapa2/ADR-019-fronteira-llm-e-decisao.md) | Fronteira LLM × decisão: duas fases, proveniência e trava técnica | Proposto |
| [020](08-etapa2/ADR-020-base-de-conhecimento-dos-temas.md) | Base de conhecimento dos temas: documentos, mapa de artigos e termos, com revisão | Proposto |
| [021](08-etapa2/ADR-021-representacao-das-questoes-e-embeddings.md) | Representação das questões e embeddings em cache (substitui a ADR-009) | Proposto |
| [022](08-etapa2/ADR-022-classificador-sem-llm.md) | Classificador sem LLM: candidatos, ranqueamento e escolha do nó pela régua (substitui a ADR-008 na decisão) | Proposto |
| [023](08-etapa2/ADR-023-fora-e-multitema.md) | "Fora" e multitema: P(fora), regras e dispersão entre as alternativas | Proposto |
| [024](08-etapa2/ADR-024-uso-da-folha-verdade.md) | Uso dos 100 rótulos e protocolo de avaliação; deriva entre antigas e novas | Proposto |
| [025](08-etapa2/ADR-025-calibracao-limiar-e-previsao.md) | Calibração, limiar e previsão para as 559 | Proposto |
| [026](08-etapa2/ADR-026-entrega-e-reprodutibilidade.md) | Entrega, reprodução do zero e repositório | Proposto |
| [027](08-etapa2/ADR-027-producao-e-retreino.md) | Produção: custo, ciclo do professor e retreino | Proposto |

**Achados de 20/10, antes de qualquer modelo** (detalhes na ADR-018):
- a folha só tem questões antigas;
- 8% são fora;
- o sistema da etapa 1, medido na folha, publicou 29 e acertou 27 (93%), e **os 2 erros eram questões fora**;
- os nós "(Parte N)" nunca aparecem na folha;
- 10 das questões novas são de direito militar, sem nó na árvore.

**Experimentos da etapa 2** (continuam a numeração da ADR-014; todos fora da amostra, na folha):

| Experimento | O que mede | ADR |
|---|---|---|
| E7 | Só representação lexical | 022 |
| E8 | Só embeddings; escolha do modelo de embedding | 021 |
| E9 | Só kNN na folha | 022 |
| E10 | Ranqueador completo × soma ponderada sem treino | 022 |
| E11 | Separabilidade do fora (AUC) e taxa de fora por faixa | 023 |
| E12 | Deriva entre as questões antigas e as novas | 024 |

**Cronograma:**

| Dia | Trabalho |
|---|---|
| Ter 20/10 | Análise do enunciado e da folha; ADRs 018–027 |
| Qua 21/10 | Anexos novos no passo 01; tag `entrega-1`; fase de conhecimento: citações, propostas de mapa e termos, embeddings (E8). **Revisão do autor (~3–4 h).** À noite: decidir se é preciso pedir prazo à Carla |
| Qui 22/10 | Candidatos, atributos, ranqueador e escolha do nó pela régua; validação cruzada; E7, E9, E10 |
| Sex 23/10 | Fora e multitema (E11); deriva (E12); calibração, limiar e previsão; `publicacao.csv` v1 |
| Sáb 24/10 | Relatório (4 páginas, a–e), memo, README com a origem dos artefatos e o tempo, diagramas |
| Dom 25/10 | Reprodução do zero sem rede e sem credenciais; revisão; publicação; e-mail |
| Seg 26/10 | Folga; data-limite |

**Definição de pronto da etapa 2:**
- [ ] `relatorio/publicacao.csv` com 659 linhas e `relatorio/previsao.txt` para as 559, aprovados pelo validador.
- [ ] `executar_sistema.py` regenera os dois arquivos sem LLM e sem rede, byte a byte, num clone limpo; tempo medido.
- [ ] Manifesto de artefatos, com a origem e a revisão de cada um; tabela no README.
- [ ] Relatório de até 4 páginas (a–e), com o memo de 1 página.
- [ ] `decisoes_manuais.md` com D13 em diante.
- [ ] Portão de qualidade aprovado, com os testes da fronteira do LLM, da escolha do nó, do fora e do determinismo.
- [ ] Repositório público atualizado e e-mail para a Carla.

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
| [008](03-classificacao/ADR-008-arquitetura-de-classificacao.md) | Arquitetura de classificação (ensemble + verificador) | 03-classificacao | Aceito (rodada completa das 359). Etapa 2: substituída na decisão pela ADR-022 |
| [009](03-classificacao/ADR-009-embeddings.md) | Embeddings como sinal opcional | 03-classificacao | Substituída pela ADR-021 (etapa 2) |
| [010](04-decisao/ADR-010-granularidade-e-recuo-para-o-pai.md) | Granularidade e recuo para o tema pai | 04-decisao | Aceito (implementado); vale na etapa 2, dentro da ADR-022 |
| [011](04-decisao/ADR-011-politica-publicar-revisar-fora.md) | Política publicar / revisar / fora | 04-decisao | Aceito (implementado). Etapa 2: revista pelas ADR-023 e ADR-025 |
| [012](05-avaliacao/ADR-012-gold-set-manual-cego.md) | Gold set manual cego | 05-avaliacao | Aceito (60 questões rotuladas). Etapa 2: só medida (ADR-024) |
| [013](05-avaliacao/ADR-013-calibracao-e-previsao.md) | Calibração e previsão de precisão e cobertura | 05-avaliacao | Aceito (implementado). Etapa 2: revista pela ADR-025 |
| [014](05-avaliacao/ADR-014-experimentos-e-registro.md) | Experimentos e registro dos becos sem saída | 05-avaliacao | Aceito (E0 a E5 feitos; E6 não rodado). Etapa 2: E7 a E12 (ADR-024) |
| [015](06-entrega/ADR-015-repositorio-e-entregaveis.md) | Repositório e entregáveis | 06-entrega | Aceito (etapa 1 entregue). Etapa 2: revista pela ADR-026 |
| [016](07-producao/ADR-016-arquitetura-de-producao.md) | Arquitetura de produção (50 mil questões/semana) | 07-producao | Proposto (etapa 1). Etapa 2: revista pela ADR-027 |
| [017](00-fundacao/ADR-017-provedores-plugaveis-e-analise-de-infra.md) | Análise da máquina e recomendação de modelos (implementa a ADR-002) | 00-fundacao | Aceito. Etapa 2: só na fase de conhecimento (ADR-019) |
| [018](08-etapa2/ADR-018-etapa-2-escopo-e-regras.md) | Etapa 2: escopo, regras novas e o que muda | 08-etapa2 | Aceito |
| [019](08-etapa2/ADR-019-fronteira-llm-e-decisao.md) | Fronteira entre o LLM e a decisão | 08-etapa2 | Proposto |
| [020](08-etapa2/ADR-020-base-de-conhecimento-dos-temas.md) | Base de conhecimento dos temas | 08-etapa2 | Proposto |
| [021](08-etapa2/ADR-021-representacao-das-questoes-e-embeddings.md) | Representação das questões e embeddings | 08-etapa2 | Proposto |
| [022](08-etapa2/ADR-022-classificador-sem-llm.md) | Classificador sem LLM | 08-etapa2 | Proposto |
| [023](08-etapa2/ADR-023-fora-e-multitema.md) | "Fora" e multitema | 08-etapa2 | Proposto |
| [024](08-etapa2/ADR-024-uso-da-folha-verdade.md) | Uso dos 100 rótulos e protocolo de avaliação | 08-etapa2 | Proposto |
| [025](08-etapa2/ADR-025-calibracao-limiar-e-previsao.md) | Calibração, limiar e previsão na etapa 2 | 08-etapa2 | Proposto |
| [026](08-etapa2/ADR-026-entrega-e-reprodutibilidade.md) | Entrega, reprodutibilidade e repositório na etapa 2 | 08-etapa2 | Proposto |
| [027](08-etapa2/ADR-027-producao-e-retreino.md) | Produção na etapa 2: custo, ciclo do professor e retreino | 08-etapa2 | Proposto |

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
