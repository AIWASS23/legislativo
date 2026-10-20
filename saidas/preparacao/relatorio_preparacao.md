# Passo 01: questões e árvore preparadas

_Gerado em 20/10/2026 10:02._

Questões convertidas no texto canônico da ADR-004: HTML limpo (inclusive o lixo colado do Word), alternativas sempre incluídas (exceto em certo/errado), comando só quando útil e com conteúdo, e nenhum rótulo de origem no texto (ADR-006).

Saída para os próximos passos: `dados/preparados/questoes.jsonl`. Amostra para conferência manual: `conferencia_texto_canonico.md`. Para gerar de novo: `uv run python executar_preparacao.py`.

## Sumário

1. Formatos
2. Comando no texto canônico
3. Tamanho do texto canônico
4. Marcas guardadas para decisão e calibração
5. Checagens automáticas: questões
6. Árvore: nós utilizáveis
7. Árvore: lixeiras (decisão manual)
8. Árvore: sobreposições e zona de convenção
9. Árvore: títulos corrigidos (só exibição)
10. Árvore: texto para os prompts
11. Checagens automáticas: árvore

## 1. Formatos

- 659 questões preparadas.

**Questões por formato**

| formato | questões | % |
|---|---|---|
| multipla_escolha_5 | 440 | 66.80 |
| certo_errado | 118 | 17.90 |
| multipla_escolha_4 | 101 | 15.30 |

_completa em `tabelas/01_01_formatos.csv`._

## 2. Comando no texto canônico

- O comando entrou em 50 questões (7.6%).
- Ficou de fora em 609: vazio (401), suspeito de ter sido gerado (62), repete o enunciado (72) ou só frase-padrão como 'Julgue o item a seguir' (74).

**Destino do comando**

| motivo | questões | % |
|---|---|---|
| vazio | 401 | 60.80 |
| so_frase_padrao | 74 | 11.20 |
| repete_enunciado | 72 | 10.90 |
| suspeito | 62 | 9.40 |
| incluido | 50 | 7.60 |

_completa em `tabelas/02_01_motivo_comando.csv`._

## 3. Tamanho do texto canônico

- Mediana de 230 tokens por questão (estimativa: 3.5 caracteres por token); máximo de 1175; 165.514 tokens no total.
- A questão vai na parte variável do prompt; a árvore de temas é a parte fixa (ADR-007, ADR-008).

**Distribuição de tamanho**

| medida | n | mín | p25 | mediana | p75 | p95 | máx | média |
|---|---|---|---|---|---|---|---|---|
| tokens estimados | 659 | 51.00 | 141.00 | 230.00 | 321.50 | 512.80 | 1175.00 | 251.20 |
| caracteres | 659 | 177.00 | 495.00 | 806.00 | 1126.00 | 1794.70 | 4112.00 | 879.00 |

_completa em `tabelas/03_01_tamanho.csv`._

**Questões mais longas**

| id | formato | tokens estimados | caracteres |
|---|---|---|---|
| Q0284 | multipla_escolha_5 | 1175 | 4112 |
| Q0289 | multipla_escolha_5 | 943 | 3299 |
| Q0070 | multipla_escolha_5 | 873 | 3054 |
| Q0097 | multipla_escolha_5 | 777 | 2719 |
| Q0020 | multipla_escolha_5 | 755 | 2644 |
| Q0089 | multipla_escolha_5 | 743 | 2602 |
| Q0146 | multipla_escolha_5 | 743 | 2601 |
| Q0493 | multipla_escolha_5 | 726 | 2542 |
| Q0100 | multipla_escolha_5 | 721 | 2523 |
| Q0623 | multipla_escolha_5 | 692 | 2423 |

_completa em `tabelas/03_02_maiores.csv`._

## 4. Marcas guardadas para decisão e calibração

- As marcas acompanham a questão em `questoes.jsonl` (ADR-011, ADR-013).

**Questões por marca**

| marca | questões | % |
|---|---|---|
| enunciado genérico | 18 | 2.70 |
| HTML colado do Word no original | 1 | 0.20 |
| cita alguma lei | 173 | 26.30 |
| cita jurisprudência | 96 | 14.60 |
| duplicata de outra questão (texto completo) | 0 | 0.00 |

_completa em `tabelas/04_01_marcas.csv`._

## 5. Checagens automáticas: questões

- 8 de 8 checagens aprovadas.

**Regras verificadas**

| regra | resultado | violações |
|---|---|---|
| todas as questões foram preparadas, uma vez cada | aprovada |  |
| nenhum texto canônico vazio | aprovada |  |
| nenhuma tag HTML no texto canônico | aprovada |  |
| nenhum escape literal (barra + n ou t) no texto canônico | aprovada |  |
| nenhum resíduo de editor (CSS do Word) no texto canônico | aprovada |  |
| múltipla escolha traz todas as alternativas; certo/errado não traz alternativas | aprovada |  |
| comando no texto só quando útil e com conteúdo | aprovada |  |
| rótulos de origem não entram no texto canônico (ADR-006) | aprovada |  |

_completa em `tabelas/05_01_checagens.csv`._

## 6. Árvore: nós utilizáveis

- 351 nós podem ser tema central; 20 fantasmas ficam de fora, cada um apontando para o nó canônico; 2 inativos ficam de fora.
- 51 temas de nível 1 têm subtemas e aceitam o recuo para o pai (ADR-010).
- Convenção dos nós duplicados (decisão manual): vale o nó com histórico, em Legislação Especial ou sem o sufixo '(Parte N)'. Os fantasmas nunca são tema central.

**Nós publicáveis por disciplina**

| disciplina | nível 1 | nível 2 | nível 1 com filhos (recuo) |
|---|---|---|---|
| Criminologia | 11 | 14 | 7 |
| Direito Penal - Legislação Especial | 26 | 0 | 0 |
| Penal | 31 | 139 | 25 |
| Processo Penal | 21 | 109 | 19 |

_completa em `tabelas/06_01_publicaveis.csv`._

**Fantasmas e o nó que vale no lugar deles**

| fantasma | caminho do fantasma | canônico | caminho do canônico |
|---|---|---|---|
| 6716 | Penal > Abuso de Autoridade | 4684 | Direito Penal - Legislação Especial > Abuso de Autoridade |
| 6717 | Penal > Crimes contra o meio ambiente | 4688 | Direito Penal - Legislação Especial > Crimes contra o meio ambiente |
| 6718 | Penal > Dos Crimes Contra a Administração Pública (Parte 1) | 5087 | Penal > Dos Crimes Contra a Administração Pública |
| 6720 | Penal > Dos Crimes Contra o Patrimônio (Parte 1) | 5157 | Penal > Dos Crimes Contra o Patrimônio |
| 6719 | Penal > Dos Crimes contra a Administração Pública (Parte 2) | 5087 | Penal > Dos Crimes Contra a Administração Pública |
| 6721 | Penal > Dos Crimes contra o Patrimônio (Parte 2) | 5157 | Penal > Dos Crimes Contra o Patrimônio |
| 6722 | Penal > Estatuto do Idoso - Crimes | 4696 | Direito Penal - Legislação Especial > Estatuto do Idoso - Crimes |
| 6723 | Penal > Lavagem de Dinheiro | 4702 | Direito Penal - Legislação Especial > Lavagem de Dinheiro |
| 6724 | Penal > Lei Maria da Penha | 4704 | Direito Penal - Legislação Especial > Lei Maria da Penha |
| 6725 | Penal > Organizações Criminosas | 4705 | Direito Penal - Legislação Especial > Organizações Criminosas |
| 6726 | Penal > Teoria da Pena (Parte 1) | 5199 | Penal > Teoria da Pena |
| 6727 | Penal > Teoria da Pena (Parte 2) | 5199 | Penal > Teoria da Pena |
| 6728 | Penal > Tráfico de Drogas | 4708 | Direito Penal - Legislação Especial > Tráfico de Drogas |
| 6732 | Processo Penal > Competência (Parte 1) | 5480 | Processo Penal > Competência |
| 6733 | Processo Penal > Competência (Parte 2) | 5480 | Processo Penal > Competência |
| 6734 | Processo Penal > Lei de Execução Penal | 4703 | Direito Penal - Legislação Especial > Lei de Execução Penal |
| 6735 | Processo Penal > Provas em Espécie | 5543 | Processo Penal > Provas em Espécies |
| 6736 | Processo Penal > Recursos (Parte 03) - Espécies | 5560 | Processo Penal > Recursos em Espécies |
| 6737 | Processo Penal > Sentença Penal (Parte 1) | 5572 | Processo Penal > Sentença Penal |
| 6738 | Processo Penal > Sentença Penal (Parte 2) | 5572 | Processo Penal > Sentença Penal |

_completa em `tabelas/06_02_fantasmas.csv`._

## 7. Árvore: lixeiras (decisão manual)

- 11 lixeiras fortes (publicar só com concordância total e verificador favorável), 7 moderadas (só variável de risco na calibração) e 3 suspeitas descartadas como falso positivo da heurística.
- Na árvore enxuta, as lixeiras fortes levam a marca [conceitual].

**Lixeiras revisadas**

| tema_id | caminho | nível | justificativa |
|---|---|---|---|
| 5171 | Penal > Introdução ao Estudo do Direito Penal > Conceito e Fontes do Direito Penal | forte | Conceito e Fontes do Direito Penal: título introdutório que absorve tudo (310 questões, 74% do tema) |
| 5581 | Processo Penal > Sistemas e Princípios Processuais Penais > Sistemas Processuais Penais | forte | Sistemas Processuais Penais: genérico, absorve o processo penal inteiro (285, 53%) |
| 5582 | Processo Penal > Sistemas e Princípios Processuais Penais > Princípios do Processo Penal | forte | Princípios do Processo Penal: concentração muito alta para 'princípios' (253, 47%) |
| 5467 | Processo Penal > Ação Penal > Características e Condições da Ação Penal | forte | Características e Condições da Ação Penal: genérico dentro de um tema já sobreposto (212) |
| 5585 | Processo Penal > Teoria Geral das Prisões > Conceitos e Espécies de Prisão | forte | Conceitos e Espécies de Prisão: absorve as prisões em espécie (209, 58%; Preventiva tem 4, Medidas Cautelares 0) |
| 5499 | Processo Penal > Inquérito Policial > Conceito, Finalidade e Características do Inquérito Policial | forte | Conceito, Finalidade e Características do Inquérito Policial: introdutório (164) |
| 5200 | Penal > Teoria da Pena > Sanção Penal: Conceito, Finalidade e Modalidades | forte | Sanção Penal: Conceito, Finalidade e Modalidades: introdutório (107) |
| 5088 | Penal > Dos Crimes Contra a Administração Pública > Noções gerais dos crimes praticados contra a administração pública | forte | Noções gerais dos crimes contra a administração pública: literalmente 'noções gerais' (100) |
| 5212 | Penal > Teoria do Crime: Culpabilidade > Conceito e Elementos da Culpabilidade | forte | Conceito e Elementos da Culpabilidade: introdutório (100) |
| 5595 | Processo Penal > Teoria Geral das Provas > Princípios Relativos à Prova Penal | forte | Princípios Relativos à Prova Penal: genérico (79) |
| 5117 | Penal > Dos Crimes Contra a Fé Pública e de Falsidade Documental > Dos Crimes contra a Fé Pública | forte | Dos Crimes contra a Fé Pública: filho com o mesmo nome do pai, lixeira de fato (103, 58%) |
| 5181 | Penal > Lei Penal no Tempo e no Espaço > Lei penal no Tempo | moderada | Lei Penal no Tempo: tema real, mas concentração alta (227, 80%) |
| 5507 | Processo Penal > Lei Processual no Tempo e no Espaço > Lei processual no Tempo | moderada | Lei Processual no Tempo: tema real, mas concentração alta (80, 81%) |
| 5526 | Processo Penal > Procedimento do Tribunal do Júri > Procedimento Bifásico do Tribunal do Júri | moderada | Procedimento Bifásico do Júri: guarda-chuva do júri (143, 56%) |
| 5510 | Processo Penal > Nulidades > Nulidade Absoluta e Relativa | moderada | Nulidade Absoluta e Relativa: conceito central, mas absorve nulidades em geral (104, 77%) |
| 5540 | Processo Penal > Procedimento Sumaríssimo > Competência dos Juizados Especiais Criminais | moderada | Competência dos Juizados Especiais Criminais: parece absorver a Lei 9.099 inteira (74, 79%) |
| 5514 | Processo Penal > Parte Geral dos Recursos > Pressupostos Objetivos e Subjetivos de Admissibilidade Recursal | moderada | Pressupostos de Admissibilidade Recursal: genérico de recursos (68, 52%) |
| 4387 | Criminologia > Teorias Sociológicas Explicativas da Criminalidade > Teorias de Nível Sociológico | moderada | Teorias de Nível Sociológico: sobrepõe-se a 'Teorias Criminológicas em Espécie' (84, 83%) |
| 5150 | Penal > Dos Crimes Contra a Vida > Homicídio | fora | Homicídio: específico, só muito cobrado (falso positivo da heurística) |
| 5064 | Penal > Ação Penal > Ação Penal Pública | fora | Ação Penal Pública: distribuição natural; o problema é a sobreposição Penal x Processo Penal, tratada em sobreposicoes.csv |
| 5172 | Penal > Introdução ao Estudo do Direito Penal > Princípios do Direito Penal | fora | Princípios do Direito Penal: concentração normal (15%); insignificância e legalidade são tema próprio |

_completa em `tabelas/07_01_lixeiras.csv`._

## 8. Árvore: sobreposições e zona de convenção

- 15 nós canônicos têm fantasma duplicado; 6 grupos de sobreposição têm regra de desempate (herdada pelos subtemas).
- 114 nós publicáveis estão na zona de convenção: publicar neles entra na margem de convenção da previsão (ADR-013), porque o gold não mede esse risco. Por tipo: duplicado_parte 71, sobreposicao 35, duplicado_outra_disciplina 8.
- Os tipos vão do mais ao menos provável de divergir do especialista: cópia em outra disciplina (ex.: LEP), sobreposição entre nós válidos (ex.: Ação Penal) e cópia '(Parte N)' na mesma disciplina, que vale também para os subtemas do canônico.

**Grupos de sobreposição e regras de desempate**

| grupo | tema_id | caminho | regra de desempate |
|---|---|---|---|
| acao_penal | 5063 | Penal > Ação Penal | Penal: espécies de ação penal, representação, requisição, renúncia, perdão e perempção como regras do CP (arts. 100 a 106) |
| acao_penal | 5466 | Processo Penal > Ação Penal | Processo Penal: denúncia, queixa, prazos, requisitos, legitimidade e condições da ação (CPP, arts. 24 a 62) |
| acao_penal | 5198 | Penal > Punibilidade > Decadência | Penal: decadência como causa de extinção da punibilidade (CP, art. 107, IV); contagem de prazo e procedimento vão para Processo Penal |
| interceptacao | 4700 | Direito Penal - Legislação Especial > Interceptação Telefônica | Legislação Especial: a Lei 9.296/96 como lei (requisitos, prazo, legitimados, crime de interceptação ilegal) |
| interceptacao | 5555 | Processo Penal > Provas em Espécies > Interceptação Telefônica e Quebra do Sigilo de Dados Telefônicos | Processo Penal: interceptação e quebra de sigilo como meio de prova (licitude, prova emprestada, encontro fortuito) |
| juizados | 4701 | Direito Penal - Legislação Especial > Juizado Especial Criminal | Legislação Especial: a Lei 9.099/95 como lei (menor potencial ofensivo e institutos despenalizadores em visão geral) |
| juizados | 5539 | Processo Penal > Procedimento Sumaríssimo | Processo Penal: o procedimento sumaríssimo (rito, competência, transação penal, suspensão condicional do processo) |
| pena | 5200 | Penal > Teoria da Pena > Sanção Penal: Conceito, Finalidade e Modalidades | Penal: conceito, finalidade e modalidades da sanção penal no Código Penal (art. 59 e espécies de pena) |
| pena | 4384 | Criminologia > Teorias Legitimadoras da Pena | Criminologia: as teorias que justificam a pena (absolutas, relativas, mistas; prevenção geral e especial) |
| sentenca | 5572 | Processo Penal > Sentença Penal | Processo Penal > Sentença Penal: classificação, efeitos, correlação, emendatio e mutatio libelli, absolutória e condenatória |
| sentenca | 5537 | Processo Penal > Procedimento Ordinário > Sentença | Procedimento Ordinário > Sentença: a sentença como ato final do rito ordinário (momento, prazo, estrutura) |
| orcrim_meios_prova | 4705 | Direito Penal - Legislação Especial > Organizações Criminosas | Legislação Especial: a Lei 12.850/13 como lei (conceito de organização criminosa, crimes, visão geral) |
| orcrim_meios_prova | 5557 | Processo Penal > Provas em Espécies > Colaboração Premiada | Processo Penal: colaboração premiada como meio de obtenção de prova |
| orcrim_meios_prova | 5558 | Processo Penal > Provas em Espécies > Ação Controlada | Processo Penal: ação controlada como meio de obtenção de prova |
| orcrim_meios_prova | 5559 | Processo Penal > Provas em Espécies > Infiltração de Agentes | Processo Penal: infiltração de agentes como meio de obtenção de prova |

_completa em `tabelas/08_01_sobreposicoes.csv`._

**Nós na zona de convenção**

| tema_id | caminho | tipo | duplicado por | grupo |
|---|---|---|---|---|
| 4384 | Criminologia > Teorias Legitimadoras da Pena | sobreposicao |  | pena |
| 4684 | Direito Penal - Legislação Especial > Abuso de Autoridade | duplicado_outra_disciplina | 6716 |  |
| 4688 | Direito Penal - Legislação Especial > Crimes contra o meio ambiente | duplicado_outra_disciplina | 6717 |  |
| 4696 | Direito Penal - Legislação Especial > Estatuto do Idoso - Crimes | duplicado_outra_disciplina | 6722 |  |
| 4700 | Direito Penal - Legislação Especial > Interceptação Telefônica | sobreposicao |  | interceptacao |
| 4701 | Direito Penal - Legislação Especial > Juizado Especial Criminal | sobreposicao |  | juizados |
| 4702 | Direito Penal - Legislação Especial > Lavagem de Dinheiro | duplicado_outra_disciplina | 6723 |  |
| 4704 | Direito Penal - Legislação Especial > Lei Maria da Penha | duplicado_outra_disciplina | 6724 |  |
| 4703 | Direito Penal - Legislação Especial > Lei de Execução Penal | duplicado_outra_disciplina | 6734 |  |
| 4705 | Direito Penal - Legislação Especial > Organizações Criminosas | duplicado_outra_disciplina | 6725 | orcrim_meios_prova |
| 4708 | Direito Penal - Legislação Especial > Tráfico de Drogas | duplicado_outra_disciplina | 6728 |  |
| 5063 | Penal > Ação Penal | sobreposicao |  | acao_penal |
| 5065 | Penal > Ação Penal > Ação Penal Privada | sobreposicao |  | acao_penal |
| 5064 | Penal > Ação Penal > Ação Penal Pública | sobreposicao |  | acao_penal |
| 5087 | Penal > Dos Crimes Contra a Administração Pública | duplicado_parte | 6718;6719 |  |
| 5097 | Penal > Dos Crimes Contra a Administração Pública > Advocacia Administrativa | duplicado_parte | 6718;6719 |  |
| 5091 | Penal > Dos Crimes Contra a Administração Pública > Concussão e Excesso de Exação | duplicado_parte | 6718;6719 |  |
| 5096 | Penal > Dos Crimes Contra a Administração Pública > Condescendência Criminosa | duplicado_parte | 6718;6719 |  |
| 5094 | Penal > Dos Crimes Contra a Administração Pública > Contrabando ou Descaminho | duplicado_parte | 6718;6719 |  |
| 5093 | Penal > Dos Crimes Contra a Administração Pública > Corrupção Ativa | duplicado_parte | 6718;6719 |  |
| 5092 | Penal > Dos Crimes Contra a Administração Pública > Corrupção Passiva | duplicado_parte | 6718;6719 |  |
| 5090 | Penal > Dos Crimes Contra a Administração Pública > Emprego Irregular de Verbas ou Rendas Públicas | duplicado_parte | 6718;6719 |  |
| 5088 | Penal > Dos Crimes Contra a Administração Pública > Noções gerais dos crimes praticados contra a administração pública | duplicado_parte | 6718;6719 |  |
| 5089 | Penal > Dos Crimes Contra a Administração Pública > Peculato e Peculato Mediante Erro de Outrem | duplicado_parte | 6718;6719 |  |
| 5095 | Penal > Dos Crimes Contra a Administração Pública > Prevaricação | duplicado_parte | 6718;6719 |  |
| 5100 | Penal > Dos Crimes Contra a Administração Pública > Resistência, Desobediência e Desacato | duplicado_parte | 6718;6719 |  |
| 5101 | Penal > Dos Crimes Contra a Administração Pública > Tráfico de Influência | duplicado_parte | 6718;6719 |  |
| 5099 | Penal > Dos Crimes Contra a Administração Pública > Usurpação de Função Pública | duplicado_parte | 6718;6719 |  |
| 5098 | Penal > Dos Crimes Contra a Administração Pública > Violência Arbitrária | duplicado_parte | 6718;6719 |  |
| 5157 | Penal > Dos Crimes Contra o Patrimônio | duplicado_parte | 6720;6721 |  |
| 5158 | Penal > Dos Crimes Contra o Patrimônio > Disposições Gerais dos Crimes Contra o Patrimônio | duplicado_parte | 6720;6721 |  |
| 5167 | Penal > Dos Crimes Contra o Patrimônio > Abuso de Incapazes | duplicado_parte | 6720;6721 |  |
| 5165 | Penal > Dos Crimes Contra o Patrimônio > Apropriação indébita | duplicado_parte | 6720;6721 |  |
| 5164 | Penal > Dos Crimes Contra o Patrimônio > Dano | duplicado_parte | 6720;6721 |  |
| 5162 | Penal > Dos Crimes Contra o Patrimônio > Esbulho Possessório | duplicado_parte | 6720;6721 |  |
| 5166 | Penal > Dos Crimes Contra o Patrimônio > Estelionato | duplicado_parte | 6720;6721 |  |
| 5161 | Penal > Dos Crimes Contra o Patrimônio > Extorsão | duplicado_parte | 6720;6721 |  |
| 5168 | Penal > Dos Crimes Contra o Patrimônio > Fraude à Execução | duplicado_parte | 6720;6721 |  |
| 5159 | Penal > Dos Crimes Contra o Patrimônio > Furto | duplicado_parte | 6720;6721 |  |
| 5169 | Penal > Dos Crimes Contra o Patrimônio > Receptação | duplicado_parte | 6720;6721 |  |

_mostrando 40 de 114 linhas; completa em `tabelas/08_02_zona_convencao.csv`._

## 9. Árvore: títulos corrigidos (só exibição)

- 9 títulos com erro aparecem corrigidos nos prompts e relatórios; o ID não muda.

**Títulos corrigidos**

| tema_id | original | exibição |
|---|---|---|
| 4373 | Escolas Crimonológicas | Escolas Criminológicas |
| 4384 | Teorias Legitimidoras da Pena | Teorias Legitimadoras da Pena |
| 4696 | Estaturo de Idoso - Crimes | Estatuto do Idoso - Crimes |
| 5081 | Falso Testemunha ou Falsa Perícia e Corrupção Ativa de Testemunha ou Perito | Falso Testemunho ou Falsa Perícia e Corrupção Ativa de Testemunha ou Perito |
| 5136 | Dos Crimescontra a Propriedade Imaterial | Dos Crimes contra a Propriedade Imaterial |
| 5158 | 12 Disposições Gerais dos Crimes Contra o Patrimônio | Disposições Gerais dos Crimes Contra o Patrimônio |
| 5483 | Comeptência Territorial | Competência Territorial |
| 5499 | Conceito, Finalidade e Caractéristas do Inquérito Policial | Conceito, Finalidade e Características do Inquérito Policial |
| 5531 | 2 Oferecimento, Rejeição e Recebimento da Peça Acusatória | Oferecimento, Rejeição e Recebimento da Peça Acusatória |

_completa em `tabelas/09_01_titulos.csv`._

## 10. Árvore: texto para os prompts

- Árvore enxuta (`arvore_enxuta.txt`): 351 linhas `ID | caminho`. 26.901 bytes. ~7.448 tokens.
- É a versão do voto barato e a base das outras duas (com escopo e cartões por ramo), que vêm dos cartões de tema (ADR-007).

## 11. Checagens automáticas: árvore

- 9 de 9 checagens aprovadas.

**Regras verificadas**

| regra | resultado | violações |
|---|---|---|
| nenhum nó inativo, fantasma ou disciplina é publicável | aprovada |  |
| todo fantasma aponta para um canônico publicável | aprovada |  |
| toda lixeira (forte, moderada ou fora) existe e é publicável | aprovada |  |
| todo nó de sobreposição existe e é publicável | aprovada |  |
| toda correção de título confere com o título original do temas.csv | aprovada |  |
| título de exibição só difere do original nos nós corrigidos | aprovada |  |
| a árvore enxuta lista exatamente os nós publicáveis, uma vez cada | aprovada |  |
| recuo para o pai só em temas de nível 1 publicáveis com filhos | aprovada |  |
| todo nó citado nas decisões existe na árvore | aprovada |  |

_completa em `tabelas/11_01_checagens_arvore.csv`._
