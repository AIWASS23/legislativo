# EDA: questões e árvore de temas

_Gerado em 14/10/2026 10:31._

Fontes: `questoes.jsonl` e `temas.csv` (pasta `anexos/`, sem alterações).

Cada seção traz os achados em tópicos e tabelas de apoio. O Markdown mostra só as primeiras linhas de cada tabela; as versões completas estão em `tabelas/`. `tabelas/perfil_questoes.csv` e `tabelas/perfil_temas.csv` têm uma linha por questão e por tema, com todas as marcas calculadas.

As heurísticas (lixeiras, fantasmas, comandos suspeitos, enunciados genéricos) servem para orientar a revisão humana, não para decidir sozinhas. Os limiares estão em `vicio_ia/configuracao.py`.

Para gerar de novo: `uv run python executar_eda.py`.

## Sumário

1. Questões: integridade dos dados
2. Questões: formato
3. Questões: ruído de HTML e formatação
4. Questões: tamanho do texto
5. Questões: o campo `comando`
6. Questões: enunciados genéricos
7. Questões: repetições
8. Questões: disciplina e assunto de origem
9. Questões: legislação e referências citadas
10. Temas: estrutura da árvore
11. Temas: descrições
12. Temas: contagem histórica de questões
13. Temas: nós fantasmas
14. Temas: títulos repetidos
15. Temas: sobreposição entre disciplinas
16. Temas: possíveis lixeiras
17. Temas: anomalias de título
18. Temas: nós utilizáveis como tema central
19. Cruzamento: assunto de origem × títulos da árvore
20. Cruzamento: disciplina de origem × disciplina do assunto
21. Cruzamento: leis citadas × temas
22. Cruzamento: cobertura dos sinais fracos

## 1. Questões: integridade dos dados

- 359 registros, 359 IDs únicos; 0 IDs repetidos; 0 fora do padrão Q0000.
- Campos fora do esquema: nenhum.
- Alternativas vazias depois da limpeza: 0.
- Campos vazios não são erro de leitura: o `comando` vazio é comum e o assunto de origem às vezes falta.

**Campos ausentes e vazios**

| campo | ausente | vazio | % vazio |
|---|---|---|---|
| id | 0 | 0 | 0.00 |
| enunciado_html | 0 | 0 | 0.00 |
| comando | 0 | 94 | 26.20 |
| alternativas | 0 | 0 | 0.00 |
| disciplina_origem | 0 | 1 | 0.30 |
| assunto_origem | 0 | 18 | 5.00 |

_completa em `tabelas/01_01_campos.csv`._

## 2. Questões: formato

- 255 de múltipla escolha com 5 alternativas, 46 com 4 e 58 de certo/errado.
- Nas de certo/errado as alternativas ('Certo'/'Errado') não dizem nada: o assunto está só no enunciado.

**Formatos**

| formato | n | % |
|---|---|---|
| multipla_escolha_5 | 255 | 71.00 |
| certo_errado | 58 | 16.20 |
| multipla_escolha_4 | 46 | 12.80 |

_completa em `tabelas/02_01_formatos.csv`._

**Letras das alternativas**

| letras | n | % |
|---|---|---|
| A,B,C,D,E | 255 | 71.00 |
| C,E | 58 | 16.20 |
| A,B,C,D | 46 | 12.80 |

_completa em `tabelas/02_02_letras_alternativas.csv`._

## 3. Questões: ruído de HTML e formatação

- Tags encontradas: <w> (1206), <br> (720), <i> (61), <span> (46), <b> (45), <m> (36), <p> (16), <sup> (15), <xml> (9), <u> (7), <o> (6), <style> (3), <em> (2). Nenhuma imagem ou tabela: o conteúdo é todo textual.
- Questões com HTML colado do Word: 1 (Q0099), somando 108.363 caracteres brutos (24.4% de todo o HTML do recorte), quase tudo CSS e metadados que a limpeza descarta.
- Antes da limpeza o recorte tem 443.917 caracteres; depois, 329.314. Mandar o HTML cru para um modelo pagaria tokens de lixo.
- 171 alternativas têm HTML ou entidades; 83 alternativas (20 questões) têm quebra de linha no meio da frase (texto colado de PDF).
- 7 comandos contêm só HTML (ex.: `<br>`) e ficam vazios depois da limpeza.
- Conclusão: uma limpeza simples (quebras, tags, entidades e espaços) basta; não há perda de conteúdo.

**Tags HTML**

| tag | ocorrências | questões |
|---|---|---|
| w | 1206 | 1 |
| br | 720 | 152 |
| i | 61 | 39 |
| span | 46 | 16 |
| b | 45 | 30 |
| m | 36 | 1 |
| p | 16 | 6 |
| sup | 15 | 7 |
| xml | 9 | 1 |
| u | 7 | 7 |
| o | 6 | 1 |
| style | 3 | 1 |
| em | 2 | 1 |

_completa em `tabelas/03_01_tags_html.csv`._

**Entidades HTML**

| entidade | ocorrências |
|---|---|
| &nbsp; | 14 |
| &#45; | 3 |

_completa em `tabelas/03_02_entidades_html.csv`._

**Questões que mais encolhem na limpeza**

| id | caracteres brutos | caracteres limpos | % removido | HTML de editor |
|---|---|---|---|---|
| Q0099 | 108363 | 1521 | 98.60 | sim |
| Q0047 | 1765 | 1333 | 24.50 | não |
| Q0196 | 1126 | 903 | 19.80 | não |
| Q0019 | 1330 | 1140 | 14.30 | não |
| Q0190 | 1237 | 1051 | 15.00 | não |
| Q0077 | 1570 | 1411 | 10.10 | não |
| Q0310 | 1063 | 948 | 10.80 | não |
| Q0269 | 1210 | 1097 | 9.30 | não |
| Q0202 | 1698 | 1586 | 6.60 | não |
| Q0063 | 1391 | 1283 | 7.80 | não |

_completa em `tabelas/03_03_maior_reducao_limpeza.csv`._

## 4. Questões: tamanho do texto

- Texto total: mediana de 828 caracteres por questão; 329.314 caracteres no recorte (cerca de 82.328 tokens).
- As alternativas costumam ter mais texto que o enunciado: o classificador precisa recebê-las sempre.

**Distribuição de tamanho**

| medida | n | mín | p25 | mediana | p75 | p95 | máx | média |
|---|---|---|---|---|---|---|---|---|
| enunciado (caracteres) | 359 | 9.00 | 89.00 | 201.00 | 517.50 | 1089.80 | 2450.00 | 365.20 |
| comando (caracteres) | 359 | 0.00 | 0.00 | 31.00 | 59.50 | 113.10 | 211.00 | 40.60 |
| alternativas (caracteres) | 359 | 10.00 | 97.00 | 425.00 | 798.50 | 1345.90 | 2285.00 | 511.60 |
| total (caracteres) | 359 | 104.00 | 517.00 | 828.00 | 1162.50 | 1976.80 | 4236.00 | 917.30 |
| palavras de conteúdo no enunciado | 359 | 0.00 | 6.00 | 18.00 | 47.00 | 96.20 | 208.00 | 32.00 |

_completa em `tabelas/04_01_tamanhos.csv`._

**Questões mais longas**

| id | formato | caracteres | enunciado |
|---|---|---|---|
| Q0284 | multipla_escolha_5 | 4236 | No dia 2 de fevereiro de 2022, por volta das 21h, Bernardo, sargento da Marinha, ao se aproximar com seu veículo automo… |
| Q0289 | multipla_escolha_5 | 3226 | “A Lei nº 11.340/2006 aporta em nosso ordenamento jurídico em resposta às graves violações de direitos sofridas pelas m… |
| Q0070 | multipla_escolha_5 | 2981 | Carlos Alberto foi preso preventivamente em 1º de fevereiro de 2024, pela suposta prática do crime de tráfico de drogas… |
| Q0097 | multipla_escolha_5 | 2753 | Inquérito policial revelou que um grupo de 16 pessoas, além de outras não identificadas, dedicava-se ao comércio ilícit… |
| Q0020 | multipla_escolha_5 | 2704 | Assinale com V (verdadeiro) ou com F (falso) as seguintes afirmações sobre posições jurisprudenciais do Superior Tribun… |
| Q0146 | multipla_escolha_5 | 2603 | A Constituição Federal de 1988, no artigo 5°, inciso LVI, prevê expressamente a inadmissibilidade da utilização no proc… |
| Q0089 | multipla_escolha_5 | 2519 | De acordo com o Glossário Jurídico do Supremo Tribunal Federal, “o princípio da insignificância tem o sentido de exclui… |
| Q0100 | multipla_escolha_5 | 2440 | Augusto levou sua filha, Ana, de treze anos de idade, a uma boate cuja entrada era permitida apenas para pessoas maiore… |
| Q0329 | multipla_escolha_5 | 2289 | Em determinado estado brasileiro, uma investigação revelou um esquema criminoso que envolvia a competição futebolística… |
| Q0323 | multipla_escolha_5 | 2282 | Acerca de provas, instrumentos legais de obtenção de prova e procedimento probatório, assinale a opção correta |

_completa em `tabelas/04_02_mais_longas.csv`._

## 5. Questões: o campo `comando`

- 101 comandos vazios (28.1%), 182 úteis, 62 suspeitos e 14 que só repetem o enunciado.
- Os suspeitos pedem algo que não cabe em questão objetiva ('Explique...', 'Complete a frase...'); 12 deles estão em questões de certo/errado. Parecem gerados por outra ferramenta.
- Decisão para o passo 01: usar o comando só quando for útil; suspeito ou repetido fica fora do texto do modelo.

**Tipos de comando**

| tipo | n | % | exemplos |
|---|---|---|---|
| util | 182 | 50.70 | Q0001, Q0003, Q0004, Q0006, Q0007, Q0009 |
| vazio | 101 | 28.10 | Q0013, Q0016, Q0019, Q0022, Q0023, Q0027 |
| suspeito | 62 | 17.30 | Q0002, Q0005, Q0008, Q0017, Q0028, Q0029 |
| repete_enunciado | 14 | 3.90 | Q0018, Q0020, Q0031, Q0123, Q0142, Q0160 |

_completa em `tabelas/05_01_tipos_comando.csv`._

**Primeira palavra do comando**

| palavra | n |
|---|---|
| assinale | 103 |
| complete | 42 |
| julgue | 22 |
| explique | 16 |
| considerando | 7 |
| indique | 6 |
| a | 6 |
| esta | 5 |
| analise | 5 |
| sobre | 5 |
| diante | 5 |
| marque | 4 |
| no | 3 |
| acerca | 2 |
| nessa | 2 |
| responda | 2 |
| identifique | 2 |
| e | 2 |
| estao | 1 |
| o | 1 |

_completa em `tabelas/05_02_primeira_palavra_comando.csv`._

**Comandos suspeitos**

| id | formato | comando | enunciado |
|---|---|---|---|
| Q0002 | multipla_escolha_5 | Complete a frase de acordo com o autor. | Segundo Vera Regina Pereira de Andrade, a clientela do sistema penal é constituída de pobres, porque |
| Q0005 | multipla_escolha_5 | complete a frase com a alternativa correta. | Carlos foi denunciado pelo crime de furto qualificado, praticado em 15/5/2022. Após a tramitação regular do processo, o… |
| Q0008 | certo_errado | Explique as condições para a progressão de regime do cumprimento da pena em crimes contra a administração pública. | A progressão de regime do cumprimento da pena de condenado por crime contra a administração pública condiciona-se à rep… |
| Q0017 | multipla_escolha_5 | Complete a frase ou responda conforme o contexto do processo penal. | No processo e julgamento dos crimes de responsabilidade dos funcionários públicos, |
| Q0028 | certo_errado | Analise as disposições mencionadas e explique o procedimento adotado pelo juiz em cada etapa processual descrita. | O Código de Processo Penal, em seu art. 406, estabelece que o juiz, ao receber a denúncia ou a queixa, ordenará a citaç… |
| Q0029 | multipla_escolha_5 | Complete a frase ou explique o que configura crime de abuso de autoridade segundo a Lei nº 13.869/2019. | Nos termos da Lei nº 13.869/2019, configura crime de abuso de autoridade |
| Q0030 | multipla_escolha_5 | Complete a definição ou responda conforme o enunciado. | Aquele que, mediante violência ou grave ameaça constrange alguém a trabalhar ou não trabalhar durante certo periodo: |
| Q0033 | multipla_escolha_5 | Explique o que é a prisão preventiva. | A prisão preventiva |
| Q0034 | multipla_escolha_5 | Complete a frase sobre a situação em que o habeas corpus é medida de impugnação cabível. | A situação em que o habeas corpus é medida de impugnação cabível é |
| Q0038 | multipla_escolha_5 | Complete a afirmação sobre as prerrogativas do ofendido no processo penal brasileiro. | No que diz respeito ao ofendido e às suas prerrogativas no processo penal brasileiro, é correto afirmar que poderá: |
| Q0043 | multipla_escolha_4 | Complete o estudo sobre a fixação da pena. | Sobre a fixação da pena, tem-se o seguinte: |
| Q0056 | multipla_escolha_5 | Complete a frase sobre a determinação da pena no caso de pluralidade delitiva. | No caso de pluralidade delitiva, deve-se adotar, na determinação da pena, |
| Q0057 | multipla_escolha_5 | Complete a definição de iter criminis. | Por iter criminis compreende-se o conjunto de |
| Q0065 | multipla_escolha_5 | Complete a explicação sobre o crime de extorsão mediante sequestro previsto no artigo 159 do Código Penal. | O crime de extorsão mediante sequestro (CP, art. 159) |
| Q0066 | multipla_escolha_5 | Explique o que é o positivismo criminológico. | O positivismo criminológico |
| Q0072 | multipla_escolha_5 | Complete a frase sobre como o juiz forma seu juízo de convicção a respeito de fato submetido a julgamento. | Para formar seu juízo de convicção a respeito de fato submetido a julgamento, o juiz. |
| Q0085 | multipla_escolha_5 | Complete a frase ou explique a importância dessa circunstância no crime de concussão. | No crime de concussão, a circunstância de ser um dos agentes funcionário público |
| Q0087 | multipla_escolha_5 | Complete a frase ou responda sobre a prisão domiciliar na execução penal conforme a jurisprudência do Superior Tribunal… | De acordo com a jurisprudência do Superior Tribunal de Justiça, a prisão domiciliar na execução penal |
| Q0088 | certo_errado | Explique a diferença entre criminologia e vitimologia. | Enquanto a criminologia pode ser identificada como a ciência que se dedica ao estudo do crime, do criminoso e dos fator… |
| Q0096 | multipla_escolha_5 | Complete a frase sobre a derrogação da competência territorial. | Ocorre a derrogação da competência territorial: |
| Q0098 | multipla_escolha_5 | Complete a definição de "confissão qualificada" conforme a doutrina. | A doutrina denomina “confissão qualificada” aquela em que o acusado |
| Q0101 | multipla_escolha_5 | Complete a frase ou responda sobre a ação de divórcio ou dissolução de união estável segundo a Lei Maria da Penha. | De acordo com a Lei Maria da Penha, a ação de divórcio ou dissolução de união estável de mulher vítima de violência dom… |
| Q0106 | multipla_escolha_4 | Responda qual é o delito praticado pelos estudantes de Direito com o chamado “pendura” nas comemorações da instalação d… | Que delito praticam os estudantes de Direito com o chamado “pendura”, nas comemorações da instalação dos cursos jurídic… |
| Q0109 | multipla_escolha_4 | Complete a frase com a pena aplicável. | Aquele que oferece droga, eventualmente e sem objetivo de lucro, a pessoa de seu relacionamento, para juntos a consumir… |
| Q0117 | multipla_escolha_5 | Complete a frase com o nome da teoria correspondente. | O estudo das teorias relaciona-se intimamente com as finalidades da pena. Nesse sentido, a teoria que sustenta que a ún… |

_mostrando 25 de 62 linhas; completa em `tabelas/05_03_comandos_suspeitos.csv`._

## 6. Questões: enunciados genéricos

- 18 enunciados genéricos (nenhuma palavra de conteúdo, ex.: 'Assinale a alternativa correta'): o assunto está inteiro nas alternativas, que podem cobrir mais de um tema.
- 26 enunciados têm menos de 40 caracteres, mas 10 deles são específicos ('A remição', 'A prisão preventiva'): tamanho não é critério; conteúdo é.

**Enunciados genéricos**

| id | formato | enunciado | assunto de origem |
|---|---|---|---|
| Q0037 | multipla_escolha_4 | Assinale a alternativa INCORRETA: | Crimes contra a administração pública |
| Q0068 | multipla_escolha_5 | Marque a alternativa correta do ponto de vista legal. | Crimes contra a fé pública |
| Q0090 | multipla_escolha_5 | Assinale a alternativa CORRETA. | Ação Penal (Parte 01) |
| Q0172 | multipla_escolha_5 | Assinale a alternativa incorreta. | Ação Penal (Parte 01) |
| Q0177 | multipla_escolha_5 | Assinale a afirmativa incorreta. | Comunicação dos atos processuais |
| Q0192 | multipla_escolha_4 | Marque a opção INCORRETA. | Concussão e Excesso de Exação |
| Q0205 | multipla_escolha_4 | Assinale a alternativa correta. | Ação Penal (Parte 02) |
| Q0222 | multipla_escolha_5 | Assinale a alternativa correta. | Ação Penal |
| Q0239 | multipla_escolha_4 | Analise a opção CORRETA. | Punibilidade |
| Q0268 | multipla_escolha_5 | Assinale a alternativa correta: | Teoria do Crime (Ilicitude) |
| Q0282 | multipla_escolha_5 | Assinale a alternativa correta: | Ação Penal |
| Q0299 | multipla_escolha_5 | Assinale a alternativa correta. | Teorias Legitimidoras da Pena |
| Q0321 | multipla_escolha_4 | Assinale a alternativa CORRETA: | Concurso de Pessoas |
| Q0325 | multipla_escolha_5 | Considerando as afirmativas abaixo, é CORRETO afirmar que: | Ação Penal |
| Q0331 | multipla_escolha_5 | Assinale a alternativa incorreta. | Comunicação dos atos processuais |
| Q0333 | multipla_escolha_5 | Assinale a alternativa CORRETA. | Iter Criminis |
| Q0339 | multipla_escolha_4 | Assinale a alternativa correta. | Ação Penal (Parte 01) |
| Q0354 | multipla_escolha_5 | Assinale a alternativa INCORRETA. | Teoria do Crime (Fato Típico) Parte 02 |

_completa em `tabelas/06_01_enunciados_genericos.csv`._

**Curtos, mas específicos**

| id | palavras de conteúdo | enunciado |
|---|---|---|
| Q0022 | 3 | Admite a modalidade culposa |
| Q0033 | 2 | A prisão preventiva |
| Q0066 | 2 | O positivismo criminológico |
| Q0122 | 1 | A remição |
| Q0258 | 3 | O exame de corpo de delito |
| Q0277 | 4 | NÃO configura crime contra idoso: |
| Q0286 | 2 | No cálculo da pena: |
| Q0301 | 3 | NÃO admite perdão judicial: |
| Q0314 | 2 | O habeas corpus é |
| Q0351 | 3 | Falsificar cartão de crédito é |

_completa em `tabelas/06_02_curtos_especificos.csv`._

## 7. Questões: repetições

- 2 grupos de enunciado idêntico, somando 13 questões.
- 0 grupos de questões idênticas (enunciado e alternativas).
- Enunciado igual não significa questão igual: deduplicar só pelo texto completo.

**Enunciados idênticos**

| n | ids | enunciado |
|---|---|---|
| 9 | Q0090, Q0205, Q0222, Q0268, Q0282, Q0299, Q0321, Q0333, Q0339 | Assinale a alternativa CORRETA. |
| 4 | Q0037, Q0172, Q0331, Q0354 | Assinale a alternativa INCORRETA: |

_completa em `tabelas/07_01_enunciados_repetidos.csv`._

**Questões idênticas**

_Nenhuma linha._

## 8. Questões: disciplina e assunto de origem

- 12 nomes de disciplina de origem; 8 questões vêm de disciplinas fora do recorte (Tributário, Constitucional, Civil, Ambiental, vazio...). Isso é sinal, não decisão: várias são penais de fato.
- A mesma disciplina aparece com nomes diferentes ('Penal' e 'Direito Penal').
- 95 assuntos distintos (89 sem o marcador '(Parte N)'); 18 questões sem assunto, 73 com '(Parte N)' e 37 com mais de um assunto.
- Os assuntos de origem vêm do site de onde as questões foram importadas e podem estar errados: servem só como sinal fraco e como baseline (ver análise cruzada).

**Disciplinas de origem**

| disciplina de origem | disciplina na árvore | n | % |
|---|---|---|---|
| Processo Penal | Processo Penal | 131 | 36.50 |
| Direito Penal | Penal | 129 | 35.90 |
| Direito Penal - Legislação Especial | Direito Penal - Legislação Especial | 32 | 8.90 |
| Criminologia | Criminologia | 31 | 8.60 |
| Penal | Penal | 27 | 7.50 |
| Direito Constitucional | (fora do recorte) | 2 | 0.60 |
| Direito Civil - Legislação Especial | (fora do recorte) | 2 | 0.60 |
| Disciplina Unificada | (fora do recorte) | 1 | 0.30 |
| (vazio) | (fora do recorte) | 1 | 0.30 |
| Direito Tributário | (fora do recorte) | 1 | 0.30 |
| Direito Processual Penal | Processo Penal | 1 | 0.30 |
| Direito Ambiental | (fora do recorte) | 1 | 0.30 |

_completa em `tabelas/08_01_disciplinas_origem.csv`._

**Questões de disciplinas fora do recorte**

| id | disciplina | assunto | enunciado |
|---|---|---|---|
| Q0014 | Disciplina Unificada | Medidas Socioeducativas | Caso a decisão do magistrado em relação à internação de Pedro seja questionada em juízo, ela não pode ser sanada pela v… |
| Q0016 | Direito Constitucional | (vazio) | À luz da atual jurisprudência dos Tribunais Superiores sobre o tema prisão, avalie as assertivas a seguir. I. Consoante… |
| Q0036 | (vazio) | (vazio) | Em uma Vara de Violência Doméstica e Familiar contra a Mulher, o Juiz de Direito recebeu os autos de inquérito policial… |
| Q0137 | Direito Civil - Legislação Especial | (vazio) | No que dispõe a legislação sobre a investigação criminal, conduzida pelo delegado de polícia é CORRETO afirmar que: |
| Q0142 | Direito Tributário | Impostos Estaduais | Assinale a alternativa que corresponde a uma operação isenta do Imposto sobre a Transmissão "Causa Mortis" e Doação de… |
| Q0218 | Direito Constitucional | (vazio) | João da Silva vai à agência bancária obter o levantamento de conta de FGTS de terceiro, usando documento falso. Desconf… |
| Q0277 | Direito Civil - Legislação Especial | (vazio) | NÃO configura crime contra idoso: |
| Q0309 | Direito Ambiental | Sistema de responsabilização por ilícitos ambientais | Segundo o Artigo 61 da Lei nº 9.605/98 a pena para quem disseminar doença ou praga ou espécies que possam causar dano à… |

_completa em `tabelas/08_02_fora_do_recorte.csv`._

**Assuntos de origem**

| assunto | n | % |
|---|---|---|
| Concurso de Crimes | 43 | 12.00 |
| Ação Penal | 20 | 5.60 |
| Ação Penal (Parte 01) | 19 | 5.30 |
| Inquérito Policial | 19 | 5.30 |
| Teoria da Pena (Parte 02) | 18 | 5.00 |
| (vazio) | 18 | 5.00 |
| Ação Penal (Parte 02) | 17 | 4.70 |
| Comunicação dos atos processuais | 13 | 3.60 |
| Teorias Legitimidoras da Pena | 10 | 2.80 |
| Sistemas e Princípios Processuais Penais | 10 | 2.80 |
| Lesão Corporal | 9 | 2.50 |
| Legislação Penal Especial | 9 | 2.50 |
| Teoria do Crime (Ilicitude) | 8 | 2.20 |
| Procedimento do Júri | 7 | 1.90 |
| Iter Criminis | 7 | 1.90 |
| Concurso de Pessoas | 7 | 1.90 |
| Competência (Parte 02) | 6 | 1.70 |
| Lei Processual Penal no tempo e no espaço | 6 | 1.70 |
| Conceitos Gerais de Criminologia | 5 | 1.40 |
| Teorias Sociológicas Explicativas da Criminalidade | 4 | 1.10 |
| Procedimento Ordinário e Sumário (Parte 02) | 4 | 1.10 |
| Criminologia no Estado Democrático de Direito | 4 | 1.10 |
| Punibilidade | 4 | 1.10 |
| Das Citações e Intimações, Citação no Processo Penal | 3 | 0.80 |
| Medida de Segurança | 3 | 0.80 |

_mostrando 25 de 95 linhas; completa em `tabelas/08_03_assuntos_origem.csv`._

## 9. Questões: legislação e referências citadas

- 93 questões (25.9%) citam alguma lei por número ou apelido.
- 47 questões citam jurisprudência: tendem a ser mais difíceis de classificar, porque o tema vem do caso julgado, não de um artigo.
- Os temas indicados por lei são um sinal fraco (passo 03): a mesma lei pode ser cobrada em mais de um tema.

**Referências citadas**

| referência | questões | % |
|---|---|---|
| Código Penal | 51 | 14.20 |
| Código de Processo Penal | 28 | 7.80 |
| Constituição | 12 | 3.30 |
| Jurisprudência (STF, STJ, súmula) | 47 | 13.10 |
| Alguma lei (número ou apelido) | 93 | 25.90 |

_completa em `tabelas/09_01_referencias.csv`._

**Leis citadas**

| lei | nome | questões | temas indicados |
|---|---|---|---|
| 11343 | Lei de Drogas | 13 | 4708, 6728 |
| 9099 | Lei dos Juizados Especiais | 10 | 4701, 5539 |
| 11340 | Lei Maria da Penha | 10 | 4704, 6724 |
| 13869 | Lei de Abuso de Autoridade | 7 | 4684, 6716 |
| 12850 | Lei das Organizações Criminosas | 7 | 4705, 6725 |
| 9605 | Lei de Crimes Ambientais | 6 | 4688, 6717 |
| 3688 | Lei das Contravenções Penais | 6 | 4686 |
| 9613 | Lei de Lavagem de Dinheiro | 5 | 4702, 6723 |
| 13964 | Pacote Anticrime | 5 |  |
| 7716 | Lei do Racismo | 5 | 4690 |
| 7210 | Lei de Execução Penal | 5 | 4703, 6734 |
| 8137 | Crimes contra a Ordem Tributária | 4 | 4695 |
| 8069 | Estatuto da Criança e do Adolescente | 3 | 4709 |
| 9296 | Lei de Interceptação Telefônica | 3 | 4700, 5555 |
| 10826 | Estatuto do Desarmamento | 3 | 4697 |
| 1521 | Lei de Economia Popular | 2 | 4687 |
| 9503 | Código de Trânsito Brasileiro | 2 | 4691 |
| 9455 | Lei de Tortura | 2 | 4707 |
| 13260 | Lei Antiterrorismo | 1 | 4706 |
| 10216 | (não catalogada) | 1 |  |
| 13146 | (não catalogada) | 1 |  |
| 2889 | Lei do Genocídio | 1 | 4698 |
| 4737 | Código Eleitoral | 1 | 4692 |
| 12015 | Reforma dos crimes contra a dignidade sexual | 1 | 5102 |
| 10741 | Estatuto da Pessoa Idosa | 1 | 4696, 6722 |

_mostrando 25 de 32 linhas; completa em `tabelas/09_02_leis_citadas.csv`._

## 10. Temas: estrutura da árvore

- 377 nós em 4 disciplinas; profundidade máxima 2 (disciplina > tema > subtema).
- 2 nós inativos (não podem ser usados).
- 0 problemas de consistência (pai inexistente, nível, caminho, disciplina ou ID repetido).

**Nós ativos por disciplina e nível**

| disciplina | nível 0 | nível 1 | nível 2 | inativos |
|---|---|---|---|---|
| Criminologia | 1 | 11 | 14 | 0 |
| Direito Penal - Legislação Especial | 1 | 26 | 0 | 0 |
| Penal | 1 | 44 | 139 | 2 |
| Processo Penal | 1 | 28 | 109 | 0 |

_completa em `tabelas/10_01_nos_por_disciplina.csv`._

**Problemas de consistência**

_Nenhuma linha._

## 11. Temas: descrições

- Dos 373 nós abaixo das disciplinas, 333 têm só o texto-modelo ('Subtema de X. N questões no source'), sem conteúdo jurídico; 20 têm descrição de verdade e 20 não têm descrição.
- Consequência: o título é praticamente a única definição de cada tema. Vale escrever um 'cartão' por tema (passo 02) com o que entra, o que não entra e as leis/artigos de referência.

**Tipo de descrição por disciplina**

| disciplina | raiz | vazia | modelo | rica |
|---|---|---|---|---|
| Criminologia | 1 | 0 | 25 | 0 |
| Direito Penal - Legislação Especial | 1 | 0 | 26 | 0 |
| Penal | 1 | 13 | 169 | 3 |
| Processo Penal | 1 | 7 | 113 | 17 |

_completa em `tabelas/11_01_tipos_descricao.csv`._

**Nós com descrição de verdade**

| tema_id | caminho | descrição |
|---|---|---|
| 5063 | Penal > Ação Penal | Ação Penal, no âmbito do Direito Penal, trata da iniciativa estatal ou privada para provocar a jurisdição criminal, compreendendo legitimidade, interesse de ag… |
| 5185 | Penal > Prescrição | No Direito Penal, o tema da prescrição trata da extinção da punibilidade pelo decurso do tempo, disciplinada principalmente nos arts. 109 a 117 do Código Penal… |
| 5198 | Penal > Punibilidade > Decadência | No Direito Penal, a decadência é causa extintiva da punibilidade consistente na perda do direito de ação penal privada ou de representação, pelo decurso do pra… |
| 5466 | Processo Penal > Ação Penal | A Ação Penal, no Processo Penal brasileiro, disciplina a iniciativa jurisdicional para provocar a prestação jurisdicional penal, delimitando quem pode acusar,… |
| 5477 | Processo Penal > Ações Autônomas de Impugnação > Habeas Corpus | Habeas Corpus é a ação constitucional autônoma de impugnação destinada à tutela imediata da liberdade de locomoção, quando alguém sofre ou se encontra na iminê… |
| 5479 | Processo Penal > Ações Autônomas de Impugnação > Mandado de Segurança | Mandado de segurança, no âmbito das ações autônomas de impugnação em processo penal, é remédio constitucional destinado à tutela de direito líquido e certo vio… |
| 5480 | Processo Penal > Competência | Competência no Processo Penal é o conjunto de regras que define qual órgão jurisdicional deve processar e julgar a infração penal, delimitando a jurisdição cri… |
| 5487 | Processo Penal > Comunicação dos Atos Processuais | A Comunicação dos Atos Processuais no Processo Penal abrange as formas pelas quais o juiz, o Ministério Público, a defesa e os auxiliares da Justiça são cienti… |
| 5512 | Processo Penal > Parte Geral dos Recursos | A Parte Geral dos Recursos no processo penal disciplina a impugnação das decisões judiciais mediante reexame por órgão jurisdicional hierarquicamente competent… |
| 5530 | Processo Penal > Procedimento Ordinário | O procedimento ordinário no Processo Penal disciplina o rito comum de maior amplitude para o processamento da ação penal, especialmente nos crimes cuja pena má… |
| 5535 | Processo Penal > Procedimento Ordinário > Audiência de Instrução e Julgamento | A Audiência de Instrução e Julgamento, no procedimento ordinário do processo penal, é o ato central de produção da prova oral, com disciplina nos arts. 400 a 4… |
| 5537 | Processo Penal > Procedimento Ordinário > Sentença | No procedimento ordinário do Processo Penal, a sentença é o ato jurisdicional que encerra a fase cognitiva em primeiro grau, após a instrução probatória e as a… |
| 5548 | Processo Penal > Provas em Espécies > Confissão | No Processo Penal, a confissão é o meio de prova pelo qual o imputado admite a autoria ou participação no fato típico, podendo ser judicial ou extrajudicial, s… |
| 5553 | Processo Penal > Provas em Espécies > Prova Documental | Prova documental, no processo penal, abrange a produção, juntada, admissibilidade, autenticidade, integridade e valoração de documentos públicos e particulares… |
| 5550 | Processo Penal > Provas em Espécies > Prova Testemunhal | A prova testemunhal, no Processo Penal, é o meio de prova consistente na inquirição de pessoas que percebem fatos relevantes para a apuração da materialidade e… |
| 5560 | Processo Penal > Recursos em Espécies | No estudo de Recursos em Espécies no Processo Penal, examinam-se os meios impugnativos típicos previstos no Código de Processo Penal para provocar o reexame de… |
| 5562 | Processo Penal > Recursos em Espécies > Apelação | Apelação, no Processo Penal, é o recurso cabível contra sentenças definitivas ou com força de definitivas proferidas pelo juiz singular, disciplinado nos arts.… |
| 5565 | Processo Penal > Recursos em Espécies > Embargos de Declaração | Embargos de declaração, no processo penal, são o recurso cabível para sanar obscuridade, ambiguidade, contradição ou omissão da decisão judicial, inclusive acó… |
| 5571 | Processo Penal > Recursos em Espécies > Recurso Especial | O Recurso Especial, no âmbito do Processo Penal, é o meio impugnativo dirigido ao Superior Tribunal de Justiça para uniformização da interpretação da lei feder… |
| 5570 | Processo Penal > Recursos em Espécies > Recurso Extraordinário | No Processo Penal, o Recurso Extraordinário é o meio de impugnação dirigido ao Supremo Tribunal Federal para discutir, em sede excepcional, matéria constitucio… |

_completa em `tabelas/11_02_descricoes_ricas.csv`._

## 12. Temas: contagem histórica de questões

- 333 nós informam quantas questões tinham na origem; 40 não informam (fantasmas e nós com descrição rica).
- Mediana de 22 questões por nó, mas poucos nós concentram centenas: é o rastro das lixeiras deixadas pela classificação automática anterior.
- 7 nós com 0 questões, entre eles temas importantes (ex.: Medidas Cautelares Diversas da Prisão). Provavelmente é aí que deveriam estar questões que foram parar nas lixeiras.
- A contagem reflete a classificação antiga (com erros), então não serve como probabilidade a priori do tema.

**Nós com mais questões na origem**

| tema_id | caminho | questões | participação no pai |
|---|---|---|---|
| 5580 | Processo Penal > Sistemas e Princípios Processuais Penais | 538 | 0.20 |
| 5199 | Penal > Teoria da Pena | 453 | 0.11 |
| 5170 | Penal > Introdução ao Estudo do Direito Penal | 424 | 0.10 |
| 5087 | Penal > Dos Crimes Contra a Administração Pública | 368 | 0.09 |
| 5584 | Processo Penal > Teoria Geral das Prisões | 359 | 0.13 |
| 5498 | Processo Penal > Inquérito Policial | 337 | 0.12 |
| 5157 | Penal > Dos Crimes Contra o Patrimônio | 325 | 0.08 |
| 5171 | Penal > Introdução ao Estudo do Direito Penal > Conceito e Fontes do Direito Penal | 310 | 0.74 |
| 5581 | Processo Penal > Sistemas e Princípios Processuais Penais > Sistemas Processuais Penais | 285 | 0.53 |
| 5180 | Penal > Lei Penal no Tempo e no Espaço | 283 | 0.07 |
| 5149 | Penal > Dos Crimes Contra a Vida | 281 | 0.07 |
| 5218 | Penal > Teoria do Crime: Fato Típico | 264 | 0.06 |
| 5524 | Processo Penal > Procedimento do Tribunal do Júri | 253 | 0.09 |
| 5582 | Processo Penal > Sistemas e Princípios Processuais Penais > Princípios do Processo Penal | 253 | 0.47 |
| 5211 | Penal > Teoria do Crime: Culpabilidade | 237 | 0.06 |
| 5590 | Processo Penal > Teoria Geral das Provas | 237 | 0.09 |
| 4703 | Direito Penal - Legislação Especial > Lei de Execução Penal | 230 | 0.28 |
| 5181 | Penal > Lei Penal no Tempo e no Espaço > Lei penal no Tempo | 227 | 0.80 |
| 5150 | Penal > Dos Crimes Contra a Vida > Homicídio | 222 | 0.80 |
| 5467 | Processo Penal > Ação Penal > Características e Condições da Ação Penal | 212 | 0.35 |
| 5585 | Processo Penal > Teoria Geral das Prisões > Conceitos e Espécies de Prisão | 209 | 0.58 |
| 5116 | Penal > Dos Crimes Contra a Fé Pública e de Falsidade Documental | 178 | 0.04 |
| 5499 | Processo Penal > Inquérito Policial > Conceito, Finalidade e Caractéristas do Inquérito Policial | 164 | 0.49 |
| 5071 | Penal > Concurso de Pessoas | 159 | 0.04 |
| 5543 | Processo Penal > Provas em Espécies | 158 | 0.06 |

_completa em `tabelas/12_01_maiores_contagens.csv`._

**Nós com 0 questões na origem**

| tema_id | caminho |
|---|---|
| 5090 | Penal > Dos Crimes Contra a Administração Pública > Emprego Irregular de Verbas ou Rendas Públicas |
| 5139 | Penal > Dos Crimes Contra a Periclitação da Vida e da Saúde > Perigo de Contágio Venéreo e de Moléstia Grave |
| 5163 | Penal > Dos Crimes Contra o Patrimônio > Usurpação |
| 5190 | Penal > Prescrição > Outras Prescrições |
| 5522 | Processo Penal > Prisões em Espécie > Medidas Cautelares Diversas da Prisão |
| 5558 | Processo Penal > Provas em Espécies > Ação Controlada |
| 5549 | Processo Penal > Provas em Espécies > Declaração do Ofendido |

_completa em `tabelas/12_02_nos_zerados.csv`._

**Nós sem contagem**

| tema_id | caminho | descrição | situação |
|---|---|---|---|
| 6716 | Penal > Abuso de Autoridade | vazia | fantasma |
| 5063 | Penal > Ação Penal | rica | válido |
| 6717 | Penal > Crimes contra o meio ambiente | vazia | fantasma |
| 6718 | Penal > Dos Crimes Contra a Administração Pública (Parte 1) | vazia | fantasma |
| 6720 | Penal > Dos Crimes Contra o Patrimônio (Parte 1) | vazia | fantasma |
| 6719 | Penal > Dos Crimes contra a Administração Pública (Parte 2) | vazia | fantasma |
| 6721 | Penal > Dos Crimes contra o Patrimônio (Parte 2) | vazia | fantasma |
| 6722 | Penal > Estatuto do Idoso - Crimes | vazia | fantasma |
| 6723 | Penal > Lavagem de Dinheiro | vazia | fantasma |
| 6724 | Penal > Lei Maria da Penha | vazia | fantasma |
| 6725 | Penal > Organizações Criminosas | vazia | fantasma |
| 5185 | Penal > Prescrição | rica | válido |
| 5198 | Penal > Punibilidade > Decadência | rica | válido |
| 6726 | Penal > Teoria da Pena (Parte 1) | vazia | fantasma |
| 6727 | Penal > Teoria da Pena (Parte 2) | vazia | fantasma |
| 6728 | Penal > Tráfico de Drogas | vazia | fantasma |
| 5466 | Processo Penal > Ação Penal | rica | válido |
| 5477 | Processo Penal > Ações Autônomas de Impugnação > Habeas Corpus | rica | válido |
| 5479 | Processo Penal > Ações Autônomas de Impugnação > Mandado de Segurança | rica | válido |
| 5480 | Processo Penal > Competência | rica | válido |
| 6732 | Processo Penal > Competência (Parte 1) | vazia | fantasma |
| 6733 | Processo Penal > Competência (Parte 2) | vazia | fantasma |
| 5487 | Processo Penal > Comunicação dos Atos Processuais | rica | válido |
| 6734 | Processo Penal > Lei de Execução Penal | vazia | fantasma |
| 5512 | Processo Penal > Parte Geral dos Recursos | rica | válido |

_mostrando 25 de 40 linhas; completa em `tabelas/12_03_nos_sem_contagem.csv`._

## 13. Temas: nós fantasmas

- 20 nós ativos sem descrição e sem histórico de questões: 11 são do tipo '(Parte N)' e 8 copiam um tema de outra disciplina (ex.: LEP em Processo Penal e em Legislação Especial).
- Hipótese: foram criados em lote, a partir dos assuntos do site de origem (os IDs são os mais altos da árvore). A análise cruzada mostra assuntos de origem que batem exatamente com esses nós.
- Canônico encontrado para 20 deles. Recomendação: não usar fantasma como tema central e confirmar com a equipe qual nó do par vale.

**Nós fantasmas e canônicos**

| tema_id | caminho | canônico | caminho do canônico | similaridade |
|---|---|---|---|---|
| 6716 | Penal > Abuso de Autoridade | 4684 | Direito Penal - Legislação Especial > Abuso de Autoridade | 1.00 |
| 6717 | Penal > Crimes contra o meio ambiente | 4688 | Direito Penal - Legislação Especial > Crimes contra o meio ambiente | 1.00 |
| 6718 | Penal > Dos Crimes Contra a Administração Pública (Parte 1) | 5087 | Penal > Dos Crimes Contra a Administração Pública | 1.00 |
| 6720 | Penal > Dos Crimes Contra o Patrimônio (Parte 1) | 5157 | Penal > Dos Crimes Contra o Patrimônio | 1.00 |
| 6719 | Penal > Dos Crimes contra a Administração Pública (Parte 2) | 5087 | Penal > Dos Crimes Contra a Administração Pública | 1.00 |
| 6721 | Penal > Dos Crimes contra o Patrimônio (Parte 2) | 5157 | Penal > Dos Crimes Contra o Patrimônio | 1.00 |
| 6722 | Penal > Estatuto do Idoso - Crimes | 4696 | Direito Penal - Legislação Especial > Estaturo de Idoso - Crimes | 0.95 |
| 6723 | Penal > Lavagem de Dinheiro | 4702 | Direito Penal - Legislação Especial > Lavagem de Dinheiro | 1.00 |
| 6724 | Penal > Lei Maria da Penha | 4704 | Direito Penal - Legislação Especial > Lei Maria da Penha | 1.00 |
| 6725 | Penal > Organizações Criminosas | 4705 | Direito Penal - Legislação Especial > Organizações Criminosas | 1.00 |
| 6726 | Penal > Teoria da Pena (Parte 1) | 5199 | Penal > Teoria da Pena | 1.00 |
| 6727 | Penal > Teoria da Pena (Parte 2) | 5199 | Penal > Teoria da Pena | 1.00 |
| 6728 | Penal > Tráfico de Drogas | 4708 | Direito Penal - Legislação Especial > Tráfico de Drogas | 1.00 |
| 6732 | Processo Penal > Competência (Parte 1) | 5480 | Processo Penal > Competência | 1.00 |
| 6733 | Processo Penal > Competência (Parte 2) | 5480 | Processo Penal > Competência | 1.00 |
| 6734 | Processo Penal > Lei de Execução Penal | 4703 | Direito Penal - Legislação Especial > Lei de Execução Penal | 1.00 |
| 6735 | Processo Penal > Provas em Espécie | 5543 | Processo Penal > Provas em Espécies | 1.00 |
| 6736 | Processo Penal > Recursos (Parte 03) - Espécies | 5560 | Processo Penal > Recursos em Espécies | 1.00 |
| 6737 | Processo Penal > Sentença Penal (Parte 1) | 5572 | Processo Penal > Sentença Penal | 1.00 |
| 6738 | Processo Penal > Sentença Penal (Parte 2) | 5572 | Processo Penal > Sentença Penal | 1.00 |

_completa em `tabelas/13_01_fantasmas.csv`._

## 14. Temas: títulos repetidos

- 15 títulos aparecem em mais de um nó; em 1 deles há mais de um nó válido (sem contar fantasmas), como 'Ação Penal' em Penal e em Processo Penal.
- Quando dois nós válidos têm o mesmo nome, o especialista precisa de uma regra para escolher; sem ela, a questão deve ir para revisão.

**Títulos repetidos**

| nós | membros |
|---|---|
| 3 | 5087 Penal > Dos Crimes Contra a Administração Pública [válido] \| 6718 Penal > Dos Crimes Contra a Administração Pública (Parte 1) [fantasma] \| 6719 Penal >… |
| 3 | 5157 Penal > Dos Crimes Contra o Patrimônio [válido] \| 6720 Penal > Dos Crimes Contra o Patrimônio (Parte 1) [fantasma] \| 6721 Penal > Dos Crimes contra o Pa… |
| 3 | 5199 Penal > Teoria da Pena [válido] \| 6726 Penal > Teoria da Pena (Parte 1) [fantasma] \| 6727 Penal > Teoria da Pena (Parte 2) [fantasma] |
| 3 | 5480 Processo Penal > Competência [válido] \| 6732 Processo Penal > Competência (Parte 1) [fantasma] \| 6733 Processo Penal > Competência (Parte 2) [fantasma] |
| 3 | 5572 Processo Penal > Sentença Penal [válido] \| 6737 Processo Penal > Sentença Penal (Parte 1) [fantasma] \| 6738 Processo Penal > Sentença Penal (Parte 2) [f… |
| 2 | 4684 Direito Penal - Legislação Especial > Abuso de Autoridade [válido] \| 6716 Penal > Abuso de Autoridade [fantasma] |
| 2 | 4688 Direito Penal - Legislação Especial > Crimes contra o meio ambiente [válido] \| 6717 Penal > Crimes contra o meio ambiente [fantasma] |
| 2 | 4702 Direito Penal - Legislação Especial > Lavagem de Dinheiro [válido] \| 6723 Penal > Lavagem de Dinheiro [fantasma] |
| 2 | 4704 Direito Penal - Legislação Especial > Lei Maria da Penha [válido] \| 6724 Penal > Lei Maria da Penha [fantasma] |
| 2 | 4703 Direito Penal - Legislação Especial > Lei de Execução Penal [válido] \| 6734 Processo Penal > Lei de Execução Penal [fantasma] |
| 2 | 4705 Direito Penal - Legislação Especial > Organizações Criminosas [válido] \| 6725 Penal > Organizações Criminosas [fantasma] |
| 2 | 4708 Direito Penal - Legislação Especial > Tráfico de Drogas [válido] \| 6728 Penal > Tráfico de Drogas [fantasma] |
| 2 | 5063 Penal > Ação Penal [válido] \| 5466 Processo Penal > Ação Penal [válido] |
| 2 | 6735 Processo Penal > Provas em Espécie [fantasma] \| 5543 Processo Penal > Provas em Espécies [válido] |
| 2 | 6736 Processo Penal > Recursos (Parte 03) - Espécies [fantasma] \| 5560 Processo Penal > Recursos em Espécies [válido] |

_completa em `tabelas/14_01_titulos_repetidos.csv`._

## 15. Temas: sobreposição entre disciplinas

- 15 pares em que o título de um nó está contido no título de um nó de outra disciplina (ex.: Interceptação Telefônica em Legislação Especial e em Processo Penal; Teoria da Pena em Penal e Teorias Legitimadoras da Pena em Criminologia).
- São escopos que se sobrepõem de verdade: o mesmo assunto pode ser cobrado pelo lado material ou processual. Cada par precisa de uma regra de desempate nos cartões de tema.

**Títulos contidos em outra disciplina**

| tema_id | caminho | contido em | caminho |
|---|---|---|---|
| 4700 | Direito Penal - Legislação Especial > Interceptação Telefônica | 5555 | Processo Penal > Provas em Espécies > Interceptação Telefônica e Quebra do Sigilo de Dados Telefônicos |
| 4701 | Direito Penal - Legislação Especial > Juizado Especial Criminal | 5540 | Processo Penal > Procedimento Sumaríssimo > Competência dos Juizados Especiais Criminais |
| 5063 | Penal > Ação Penal | 5466 | Processo Penal > Ação Penal |
| 5063 | Penal > Ação Penal | 5471 | Processo Penal > Ação Penal > Ação Penal Pública Condicionada |
| 5063 | Penal > Ação Penal | 5470 | Processo Penal > Ação Penal > Ação Penal Pública Incondicionada |
| 5063 | Penal > Ação Penal | 5472 | Processo Penal > Ação Penal > Ação Penal de Iniciativa Privada |
| 5063 | Penal > Ação Penal | 5467 | Processo Penal > Ação Penal > Características e Condições da Ação Penal |
| 5063 | Penal > Ação Penal | 5468 | Processo Penal > Ação Penal > Classificação da Ação Penal |
| 5063 | Penal > Ação Penal | 5469 | Processo Penal > Ação Penal > Princípios da Ação Penal |
| 5065 | Penal > Ação Penal > Ação Penal Privada | 5472 | Processo Penal > Ação Penal > Ação Penal de Iniciativa Privada |
| 5064 | Penal > Ação Penal > Ação Penal Pública | 5471 | Processo Penal > Ação Penal > Ação Penal Pública Condicionada |
| 5064 | Penal > Ação Penal > Ação Penal Pública | 5470 | Processo Penal > Ação Penal > Ação Penal Pública Incondicionada |
| 5199 | Penal > Teoria da Pena | 4384 | Criminologia > Teorias Legitimidoras da Pena |
| 5466 | Processo Penal > Ação Penal | 5065 | Penal > Ação Penal > Ação Penal Privada |
| 5466 | Processo Penal > Ação Penal | 5064 | Penal > Ação Penal > Ação Penal Pública |

_completa em `tabelas/15_01_sobreposicoes.csv`._

## 16. Temas: possíveis lixeiras

- 21 nós suspeitos: concentram 50% ou mais das questões dos irmãos (com 60+ questões), ou têm título genérico ('Conceito', 'Noções gerais', 'Princípios', 'Introdução') com muitas questões.
- Só entram nós sem filhos: a contagem de um tema com subtemas soma a dos filhos e sempre parece inflada. É também nos temas com filhos que a decisão recua quando há dúvida entre subtemas.
- A heurística precisa de revisão humana: um tema específico e muito cobrado (ex.: Homicídio) também concentra questões sem ser lixeira. A lista final entra em decisoes_manuais.md.
- Uso: o prompt avisa que esses nós só servem para questões sobre o conceito geral, e publicar neles exige mais evidência.

**Possíveis lixeiras**

| tema_id | caminho | questões | total dos irmãos | participação | motivo |
|---|---|---|---|---|---|
| 5171 | Penal > Introdução ao Estudo do Direito Penal > Conceito e Fontes do Direito Penal | 310 | 420 | 0.74 | concentra 74% das questões dos irmãos; título genérico com 310 questões |
| 5581 | Processo Penal > Sistemas e Princípios Processuais Penais > Sistemas Processuais Penais | 285 | 538 | 0.53 | concentra 53% das questões dos irmãos |
| 5582 | Processo Penal > Sistemas e Princípios Processuais Penais > Princípios do Processo Penal | 253 | 538 | 0.47 | título genérico com 253 questões |
| 5181 | Penal > Lei Penal no Tempo e no Espaço > Lei penal no Tempo | 227 | 283 | 0.80 | concentra 80% das questões dos irmãos |
| 5150 | Penal > Dos Crimes Contra a Vida > Homicídio | 222 | 279 | 0.80 | concentra 80% das questões dos irmãos |
| 5467 | Processo Penal > Ação Penal > Características e Condições da Ação Penal | 212 | 613 | 0.35 | título genérico com 212 questões |
| 5585 | Processo Penal > Teoria Geral das Prisões > Conceitos e Espécies de Prisão | 209 | 359 | 0.58 | concentra 58% das questões dos irmãos; título genérico com 209 questões |
| 5499 | Processo Penal > Inquérito Policial > Conceito, Finalidade e Caractéristas do Inquérito Policial | 164 | 337 | 0.49 | título genérico com 164 questões |
| 5526 | Processo Penal > Procedimento do Tribunal do Júri > Procedimento Bifásico do Tribunal do Júri | 143 | 253 | 0.56 | concentra 56% das questões dos irmãos |
| 5200 | Penal > Teoria da Pena > Sanção Penal: Conceito, Finalidade e Modalidades | 107 | 453 | 0.24 | título genérico com 107 questões |
| 5510 | Processo Penal > Nulidades > Nulidade Absoluta e Relativa | 104 | 135 | 0.77 | concentra 77% das questões dos irmãos |
| 5117 | Penal > Dos Crimes Contra a Fé Pública e de Falsidade Documental > Dos Crimes contra a Fé Pública | 103 | 178 | 0.58 | concentra 58% das questões dos irmãos |
| 5088 | Penal > Dos Crimes Contra a Administração Pública > Noções gerais dos crimes praticados contra a administração pública | 100 | 368 | 0.27 | título genérico com 100 questões |
| 5212 | Penal > Teoria do Crime: Culpabilidade > Conceito e Elementos da Culpabilidade | 100 | 237 | 0.42 | título genérico com 100 questões |
| 4387 | Criminologia > Teorias Sociológicas Explicativas da Criminalidade > Teorias de Nível Sociológico | 84 | 101 | 0.83 | concentra 83% das questões dos irmãos |
| 5064 | Penal > Ação Penal > Ação Penal Pública | 82 | 108 | 0.76 | concentra 76% das questões dos irmãos |
| 5507 | Processo Penal > Lei Processual no Tempo e no Espaço > Lei processual no Tempo | 80 | 99 | 0.81 | concentra 81% das questões dos irmãos |
| 5595 | Processo Penal > Teoria Geral das Provas > Princípios Relativos à Prova Penal | 79 | 237 | 0.33 | título genérico com 79 questões |
| 5540 | Processo Penal > Procedimento Sumaríssimo > Competência dos Juizados Especiais Criminais | 74 | 94 | 0.79 | concentra 79% das questões dos irmãos |
| 5514 | Processo Penal > Parte Geral dos Recursos > Pressupostos Objetivos e Subjetivos de Admissibilidade Recursal | 68 | 132 | 0.52 | concentra 52% das questões dos irmãos |
| 5172 | Penal > Introdução ao Estudo do Direito Penal > Princípios do Direito Penal | 65 | 420 | 0.15 | título genérico com 65 questões |

_completa em `tabelas/16_01_lixeiras.csv`._

## 17. Temas: anomalias de título

- 7 títulos com suspeita de erro (número no início, palavras coladas, grafia estranha).
- Não muda a classificação (o ID é o que vale), mas confunde quem lê e vai para o memo do professor. No prompt, os títulos aparecem corrigidos.

**Anomalias de título**

| tema_id | título | anomalias |
|---|---|---|
| 4373 | Escolas Crimonológicas | possível erro de digitação: crimonologicas ~ criminologicas |
| 4696 | Estaturo de Idoso - Crimes | possível erro de digitação: estaturo ~ estatuto |
| 5081 | Falso Testemunha ou Falsa Perícia e Corrupção Ativa de Testemunha ou Perito | possível erro de digitação: perito ~ perigo |
| 5158 | 12 Disposições Gerais dos Crimes Contra o Patrimônio | começa com número |
| 5136 | Dos Crimescontra a Propriedade Imaterial | palavras coladas: crimescontra -> crimes contra |
| 5483 | Comeptência Territorial | possível erro de digitação: comeptencia ~ competencia |
| 5531 | 2 Oferecimento, Rejeição e Recebimento da Peça Acusatória | começa com número |

_completa em `tabelas/17_01_anomalias_titulo.csv`._

## 18. Temas: nós utilizáveis como tema central

- 351 nós podem ser tema central (ativos, não fantasmas, abaixo da disciplina).
- 51 temas de nível 1 têm subtemas e aceitam o recuo para o pai; 38 temas de nível 1 não têm filhos (o recuo não se aplica).
- Pela régua do case, publicar no tema pai é certo para qualquer subtema escolhido pelo especialista.

**Nós utilizáveis por disciplina**

| disciplina | nível 1 | nível 2 | nível 1 com filhos (recuo) | nível 1 sem filhos |
|---|---|---|---|---|
| Criminologia | 11 | 14 | 7 | 4 |
| Direito Penal - Legislação Especial | 26 | 0 | 0 | 26 |
| Penal | 31 | 139 | 25 | 6 |
| Processo Penal | 21 | 109 | 19 | 2 |

_completa em `tabelas/18_01_utilizaveis.csv`._

## 19. Cruzamento: assunto de origem × títulos da árvore

- 253 questões (70.5%) têm assunto de origem igual ao título de um nó válido; isso não quer dizer que o tema esteja certo (ex.: extorsão mediante sequestro com assunto 'Lesão Corporal').
- 26 questões têm assunto igual ao título de um nó fantasma (ex.: 'Teoria da Pena (Parte 02)' e o nó 'Teoria da Pena (Parte 2)'). Isso reforça a hipótese de que os fantasmas vieram da importação.
- 67 questões têm assunto que bate com mais de um nó válido (ex.: 'Ação Penal' em Penal e em Processo Penal).
- 62 sem correspondência e 18 sem assunto.

**Questões por resultado do casamento**

| resultado | questões | % |
|---|---|---|
| tema_valido | 253 | 70.50 |
| sem_correspondencia | 62 | 17.30 |
| fantasma | 26 | 7.20 |
| vazio | 18 | 5.00 |

_completa em `tabelas/19_01_categorias_casamento.csv`._

**Cada assunto de origem e os nós com o mesmo título**

| assunto | questões | resultado | nós |
|---|---|---|---|
| Concurso de Crimes | 43 | tema_valido | 5066 Penal > Concurso de Crimes [válido] |
| Ação Penal | 20 | tema_valido | 5063 Penal > Ação Penal [válido] \| 5466 Processo Penal > Ação Penal [válido] |
| Ação Penal (Parte 01) | 19 | tema_valido | 5063 Penal > Ação Penal [válido] \| 5466 Processo Penal > Ação Penal [válido] |
| Inquérito Policial | 19 | tema_valido | 5498 Processo Penal > Inquérito Policial [válido] |
| Teoria da Pena (Parte 02) | 18 | fantasma | 6727 Penal > Teoria da Pena (Parte 2) [fantasma] |
| (vazio) | 18 | vazio |  |
| Ação Penal (Parte 02) | 17 | tema_valido | 5063 Penal > Ação Penal [válido] \| 5466 Processo Penal > Ação Penal [válido] |
| Comunicação dos atos processuais | 13 | tema_valido | 5487 Processo Penal > Comunicação dos Atos Processuais [válido] |
| Teorias Legitimidoras da Pena | 10 | tema_valido | 4384 Criminologia > Teorias Legitimidoras da Pena [válido] |
| Sistemas e Princípios Processuais Penais | 10 | tema_valido | 5580 Processo Penal > Sistemas e Princípios Processuais Penais [válido] |
| Lesão Corporal | 9 | tema_valido | 5077 Penal > Das Lesões Corporais [válido] |
| Legislação Penal Especial | 9 | sem_correspondencia |  |
| Teoria do Crime (Ilicitude) | 8 | tema_valido | 5228 Penal > Teoria do Crime: Ilicitude [válido] |
| Procedimento do Júri | 7 | sem_correspondencia |  |
| Iter Criminis | 7 | tema_valido | 5175 Penal > Iter Criminis [válido] |
| Concurso de Pessoas | 7 | tema_valido | 5071 Penal > Concurso de Pessoas [válido] |
| Competência (Parte 02) | 6 | fantasma | 6733 Processo Penal > Competência (Parte 2) [fantasma] |
| Lei Processual Penal no tempo e no espaço | 6 | sem_correspondencia |  |
| Conceitos Gerais de Criminologia | 5 | sem_correspondencia |  |
| Teorias Sociológicas Explicativas da Criminalidade | 4 | tema_valido | 4385 Criminologia > Teorias Sociológicas Explicativas da Criminalidade [válido] |
| Procedimento Ordinário e Sumário (Parte 02) | 4 | sem_correspondencia |  |
| Criminologia no Estado Democrático de Direito | 4 | tema_valido | 4368 Criminologia > Criminologia no Estado Democrático de Direito [válido] |
| Punibilidade | 4 | tema_valido | 5191 Penal > Punibilidade [válido] |
| Das Citações e Intimações, Citação no Processo Penal | 3 | sem_correspondencia |  |
| Medida de Segurança | 3 | tema_valido | 5184 Penal > Medida de Segurança [válido] |

_mostrando 25 de 95 linhas; completa em `tabelas/19_02_assunto_vs_arvore.csv`._

## 20. Cruzamento: disciplina de origem × disciplina do assunto

- Entre as questões cujo assunto bate com um nó válido: 235 têm disciplina de origem coerente, 18 incoerente e 0 vêm de disciplina fora do recorte.
- Incoerência entre os dois rótulos de origem é mais um sinal de que eles não servem como gabarito.

**Disciplina de origem incoerente com o assunto**

| id | disciplina de origem | assunto | nós do assunto |
|---|---|---|---|
| Q0011 | Direito Penal - Legislação Especial | Concurso de Crimes | 5066 Penal > Concurso de Crimes [válido] |
| Q0029 | Direito Penal - Legislação Especial | Medida de Segurança | 5184 Penal > Medida de Segurança [válido] |
| Q0039 | Direito Penal - Legislação Especial | Concurso de Crimes | 5066 Penal > Concurso de Crimes [válido] |
| Q0062 | Direito Penal - Legislação Especial | Concurso de Crimes | 5066 Penal > Concurso de Crimes [válido] |
| Q0078 | Direito Penal - Legislação Especial | Concurso de Crimes | 5066 Penal > Concurso de Crimes [válido] |
| Q0109 | Direito Penal - Legislação Especial | Prescrição | 5185 Penal > Prescrição [válido] |
| Q0116 | Direito Penal - Legislação Especial | Prescrição | 5185 Penal > Prescrição [válido] |
| Q0145 | Direito Penal - Legislação Especial | Concurso de Crimes | 5066 Penal > Concurso de Crimes [válido] |
| Q0163 | Direito Penal - Legislação Especial | Concurso de Crimes | 5066 Penal > Concurso de Crimes [válido] |
| Q0181 | Direito Penal - Legislação Especial | Concurso de Crimes | 5066 Penal > Concurso de Crimes [válido] |
| Q0184 | Direito Penal - Legislação Especial | Concurso de Crimes | 5066 Penal > Concurso de Crimes [válido] |
| Q0262 | Direito Penal - Legislação Especial | Medida de Segurança | 5184 Penal > Medida de Segurança [válido] |
| Q0291 | Direito Penal - Legislação Especial | Ação Penal | 5063 Penal > Ação Penal [válido] \| 5466 Processo Penal > Ação Penal [válido] |
| Q0297 | Direito Penal - Legislação Especial | Ação Penal | 5063 Penal > Ação Penal [válido] \| 5466 Processo Penal > Ação Penal [válido] |
| Q0298 | Direito Penal - Legislação Especial | Teoria do Crime (Ilicitude) | 5228 Penal > Teoria do Crime: Ilicitude [válido] |
| Q0307 | Direito Penal - Legislação Especial | Concurso de Crimes | 5066 Penal > Concurso de Crimes [válido] |
| Q0326 | Direito Penal - Legislação Especial | Concurso de Crimes | 5066 Penal > Concurso de Crimes [válido] |
| Q0337 | Direito Penal - Legislação Especial | Concurso de Crimes | 5066 Penal > Concurso de Crimes [válido] |

_completa em `tabelas/20_01_disciplina_incoerente.csv`._

## 21. Cruzamento: leis citadas × temas

- 32 leis do catálogo apontam para temas; 0 apontam só para nós inválidos.
- 8 leis têm um nó válido em Legislação Especial e um fantasma com o mesmo nome em Penal ou Processo Penal: a duplicidade atinge justamente as leis mais cobradas (Drogas, LEP, Maria da Penha).

**Leis do catálogo, citações e temas indicados**

| lei | nome | questões | temas |
|---|---|---|---|
| 11343 | Lei de Drogas | 13 | 4708 Direito Penal - Legislação Especial > Tráfico de Drogas [válido] \| 6728 Penal > Tráfico de Drogas [fantasma] |
| 11340 | Lei Maria da Penha | 10 | 4704 Direito Penal - Legislação Especial > Lei Maria da Penha [válido] \| 6724 Penal > Lei Maria da Penha [fantasma] |
| 9099 | Lei dos Juizados Especiais | 10 | 4701 Direito Penal - Legislação Especial > Juizado Especial Criminal [válido] \| 5539 Processo Penal > Procedimento Sumaríssimo [válido] |
| 13869 | Lei de Abuso de Autoridade | 7 | 4684 Direito Penal - Legislação Especial > Abuso de Autoridade [válido] \| 6716 Penal > Abuso de Autoridade [fantasma] |
| 12850 | Lei das Organizações Criminosas | 7 | 4705 Direito Penal - Legislação Especial > Organizações Criminosas [válido] \| 6725 Penal > Organizações Criminosas [fantasma] |
| 9605 | Lei de Crimes Ambientais | 6 | 4688 Direito Penal - Legislação Especial > Crimes contra o meio ambiente [válido] \| 6717 Penal > Crimes contra o meio ambiente [fantasma] |
| 3688 | Lei das Contravenções Penais | 6 | 4686 Direito Penal - Legislação Especial > Contravenções Penais [válido] |
| 9613 | Lei de Lavagem de Dinheiro | 5 | 4702 Direito Penal - Legislação Especial > Lavagem de Dinheiro [válido] \| 6723 Penal > Lavagem de Dinheiro [fantasma] |
| 7210 | Lei de Execução Penal | 5 | 4703 Direito Penal - Legislação Especial > Lei de Execução Penal [válido] \| 6734 Processo Penal > Lei de Execução Penal [fantasma] |
| 7716 | Lei do Racismo | 5 | 4690 Direito Penal - Legislação Especial > Crimes de Racismo [válido] |
| 8137 | Crimes contra a Ordem Tributária | 4 | 4695 Direito Penal - Legislação Especial > Crimes Tributários [válido] |
| 10826 | Estatuto do Desarmamento | 3 | 4697 Direito Penal - Legislação Especial > Estatuto do Desarmamento [válido] |
| 9296 | Lei de Interceptação Telefônica | 3 | 4700 Direito Penal - Legislação Especial > Interceptação Telefônica [válido] \| 5555 Processo Penal > Provas em Espécies > Interceptação Telefônica e Quebra do… |
| 8069 | Estatuto da Criança e do Adolescente | 3 | 4709 Direito Penal - Legislação Especial > Violência contra Criança e Adolescente [válido] |
| 9455 | Lei de Tortura | 2 | 4707 Direito Penal - Legislação Especial > Tortura [válido] |
| 9503 | Código de Trânsito Brasileiro | 2 | 4691 Direito Penal - Legislação Especial > Crimes de Trânsito [válido] |
| 1521 | Lei de Economia Popular | 2 | 4687 Direito Penal - Legislação Especial > Crimes contra a Economia Popular [válido] |
| 8072 | Lei dos Crimes Hediondos | 1 | 4693 Direito Penal - Legislação Especial > Crimes Hediondos [válido] |
| 13260 | Lei Antiterrorismo | 1 | 4706 Direito Penal - Legislação Especial > Terrorismo [válido] |
| 2889 | Lei do Genocídio | 1 | 4698 Direito Penal - Legislação Especial > Genocídio [válido] |
| 8078 | Código de Defesa do Consumidor | 1 | 4694 Direito Penal - Legislação Especial > Crimes previstos no CDC [válido] |
| 10741 | Estatuto da Pessoa Idosa | 1 | 4696 Direito Penal - Legislação Especial > Estaturo de Idoso - Crimes [válido] \| 6722 Penal > Estatuto do Idoso - Crimes [fantasma] |
| 4737 | Código Eleitoral | 1 | 4692 Direito Penal - Legislação Especial > Crimes Eleitorais [válido] |
| 12015 | Reforma dos crimes contra a dignidade sexual | 1 | 5102 Penal > Dos Crimes Contra a Dignidade Sexual [válido] |
| 7492 | Crimes contra o Sistema Financeiro | 0 | 4689 Direito Penal - Legislação Especial > Crimes contra o Sistema Financeiro [válido] |

_mostrando 25 de 32 linhas; completa em `tabelas/21_01_leis_temas.csv`._

## 22. Cruzamento: cobertura dos sinais fracos

- 280 questões (78.0%) têm ao menos um sinal fraco de tema (assunto de origem com título válido ou lei catalogada); 79 não têm nenhum.
- Quando os dois sinais existem (57 questões), caem no mesmo ramo em 0 e na mesma disciplina em 8. Não é erro de cálculo: a lei aponta para Legislação Especial e o assunto de origem aponta para Penal ou Processo Penal.
- Em vários desses casos o assunto de origem está claramente errado. 'Concurso de Crimes' aparece em 15 dos conflitos (de 43 questões com esse assunto): o site de origem também tem lixeiras, e o assunto mais frequente do recorte é uma delas.
- Conclusão: sinal fraco serve para desempate e para medir concordância, nunca como rótulo. O classificador principal continua sendo o modelo de linguagem.

**Cobertura dos sinais fracos**

| sinal | questões | % |
|---|---|---|
| só assunto de origem | 196 | 54.60 |
| só lei citada | 27 | 7.50 |
| os dois | 57 | 15.90 |
| nenhum | 79 | 22.00 |

_completa em `tabelas/22_01_cobertura_sinais.csv`._

**Assuntos de origem em conflito com a lei citada**

| assunto de origem | conflitos | questões com o assunto |
|---|---|---|
| Concurso de Crimes | 15 | 43 |
| Ação Penal (Parte 02) | 7 | 17 |
| Ação Penal | 6 | 20 |
| Ação Penal (Parte 01) | 4 | 19 |
| Inquérito Policial | 4 | 19 |
| Teoria do Crime (Ilicitude) | 3 | 8 |
| Sistemas e Princípios Processuais Penais | 3 | 10 |
| Comunicação dos atos processuais | 3 | 13 |
| Medida de Segurança | 2 | 3 |
| Lesão Corporal | 2 | 9 |
| Prescrição | 2 | 3 |
| Concurso de Pessoas | 1 | 7 |
| Criminologia no Estado Democrático de Direito | 1 | 4 |
| Punibilidade | 1 | 4 |
| Corrupção passiva, Concussão e Excesso de Exação , Crimes contra a administração pública | 1 | 1 |
| Iter Criminis | 1 | 7 |
| Procedimento Ordinário | 1 | 1 |

_completa em `tabelas/22_02_assuntos_em_conflito.csv`._

**Sinais fracos por questão**

| id | assunto de origem | temas pelo assunto | temas pela lei |
|---|---|---|---|
| Q0001 | sem_correspondencia |  |  |
| Q0002 | tema_valido | 4384 |  |
| Q0003 | tema_valido | 5063;5466 |  |
| Q0004 | fantasma |  |  |
| Q0005 | sem_correspondencia |  |  |
| Q0006 | tema_valido | 5160 |  |
| Q0007 | tema_valido | 5063;5466 |  |
| Q0008 | fantasma |  |  |
| Q0009 | tema_valido | 5066 |  |
| Q0010 | tema_valido | 5066 | 4688 |
| Q0011 | tema_valido | 5066 | 4702 |
| Q0012 | tema_valido | 5063;5466 | 4701;5539 |
| Q0013 | sem_correspondencia |  |  |
| Q0014 | sem_correspondencia |  |  |
| Q0015 | tema_valido | 5498 |  |
| Q0016 | vazio |  |  |
| Q0017 | tema_valido | 5063;5466 |  |
| Q0018 | fantasma |  | 4701;5539 |
| Q0019 | tema_valido | 5063;5466 |  |
| Q0020 | tema_valido | 5063;5466 | 4709 |
| Q0021 | fantasma |  |  |
| Q0022 | tema_valido | 5066 |  |
| Q0023 | sem_correspondencia |  |  |
| Q0024 | vazio |  |  |
| Q0025 | tema_valido | 5063;5466 |  |

_mostrando 25 de 359 linhas; completa em `tabelas/22_03_sinais_por_questao.csv`._
