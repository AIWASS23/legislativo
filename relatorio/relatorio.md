# Classificação de tópicos: relatório do case Vício (Método VDE)

17/10/2026 · Código, dados e decisões: [README](../README.md) · Decisões tomadas à mão: [`decisoes_manuais.md`](../decisoes_manuais.md)

**Resultado.**
- Das 359 questões: **81 publicadas (23%)**, 276 para revisão (todas com tema sugerido) e 2 fora.
  Precisão prevista nas publicadas: **0,97** (intervalo de 0,93 a 1,00).
- Custo: 1.903 chamadas a modelos (~10,6 h de chamadas somadas); US$ 0 pagos, porque usei assinaturas que já
  tinha; 3 h de rotulagem manual.

## a) Como pensei

**A régua decide o desenho.** A meta é "95% de acerto nas publicadas, publicando o máximo". Com ela, o
problema deixa de ser só acertar o tema: é **saber quando se acertou**. Por isso decidi como medir antes
de escolher modelo. Parti de quatro hipóteses:

1. **Irmão é o erro mais caro.** O erro que mais pesa não é entender mal a questão: é escolher o
   **subtema irmão** errado. A régua aceita pai e filho, mas não irmão.
2. **Parte do erro é convenção da árvore**, não de Direito: em temas duplicados ou sobrepostos, o conteúdo
   pode estar certo e o nó, errado.
3. **Concordância separa o certo do duvidoso.** A concordância entre fontes independentes faz isso melhor
   que a confiança declarada por um modelo.
4. **O assunto de origem** das questões não serve como rótulo.

**Dados antes de modelo.** A análise exploratória (`saidas/eda/`) mudou o plano antes da primeira chamada.
- Só 20 dos 373 temas abaixo das disciplinas têm descrição de verdade. O resto tem só um texto-modelo
  ("Subtema de X. N questões") ou nada.
- Há 20 nós "fantasmas": cópias sem descrição e sem histórico.
- O assunto de origem bate com dois temas válidos em 67 questões. Nas 58 que também citam uma lei especial,
  ele cai no mesmo ramo da lei 0 vezes.

O que mudou: o assunto de origem nunca entra no prompt; escrevi, com um LLM, **cartões** para os 351 temas
utilizáveis (definição, o que entra, o que não entra e para onde vai); e registrei à mão a convenção dos
duplicados (D1) e as regras de desempate das sobreposições (D2).

**Um gabarito antes de tudo.** Rotulei à mão 60 questões sorteadas (estratificadas, semente fixa), **sem
ver resposta de modelo**, em 3 horas. Elas medem o acerto, calibram a confiança e escolhem o limiar. O
rótulo nunca decide uma questão. Toda medida usa probabilidade fora da amostra (validação cruzada).

**O pipeline:** quatro fontes e um verificador.
- **Classificadores A e B**, de famílias diferentes. A (GPT) vê a árvore inteira, com o escopo de cada
  tema; B (Gemini) é hierárquico: escolhe o tema e depois o subtema, com os cartões.
- **Voto barato** (GPT-OSS, modelo aberto, árvore enxuta) e **regras** pelas leis citadas.
- **Verificador contrastivo:** recebe os cartões do candidato, do pai, dos irmãos e do par de outra
  disciplina, sem saber qual é o candidato, e escolhe um deles. Ataca a hipótese 1.
- **Recuo para o pai:** quando a dúvida é entre irmãos, a questão vai para o pai, que a régua aceita. Nunca
  recua até a disciplina.

**O que testei.**
- **Régua estrita:** vale o tema que rotulei, o pai ou um filho dele.
- **Cobertura a 95%:** a fração do gold que daria para publicar com 95% de acerto, ordenando pela confiança.

| Experimento | Resultado no gold (60) | Decisão |
|---|---|---|
| E0: assunto de origem como rótulo | 12 de 33 (36%) | Hipótese 4 confirmada: o assunto fica só como sinal fraco |
| E2: um LLM sozinho (A) | 52 de 60 (87%); cobertura a 95%: 67% | "Razoável, não publicável". A autoconfiança não é calibrada: A declara 0,99 em erros |
| E3: B erra diferente de A? | B 52 de 60; os dois erram juntos 4 vezes, contra ~1 se fossem independentes | Parcialmente derrubada: a concordância de A e B não basta |
| E3b: voto barato | 30 de 60 (50%) | Fraco sozinho, bom detector de dúvida |
| E4: cartões × só títulos (em B) | 52 × 53 acertos; cobertura a 95%: 78% × 62% | Derrubada no acerto. Cartões mantidos: separam o certo do duvidoso |
| E5: pipeline × A sozinho | Mesma precisão em cada cobertura (top 28: 28/28 × 27/28) | "O ensemble acerta mais": derrubada. "Sabe quando acertou": confirmada |

O E5 virou a regra de publicação. Quando o verificador confirma e A, B e o voto barato caem no mesmo ramo
(**consenso total**), o gold tem 28 acertos em 28. Na faixa seguinte (o verificador confirma, mas alguma
fonte discorda), 19 em 22. Publicar exige a primeira faixa.

**Becos sem saída.**
- **Regressão logística** com 7 sinais para calibrar: com 6 erros em 60, empatou com um palpite constante.
  Troquei por taxas de acerto por faixa de sinais, com suavização de Jeffreys, que venceram na validação
  cruzada (log-loss 0,29 × 0,31).
- **A primeira prévia publicou zero.** A regressão comprimia tudo em ~0,92, e eu descontava a ambiguidade do
  rótulo no lugar errado.
- **Modelos.** Comecei com Claude por API, mas repetir o mesmo modelo não dá opiniões independentes.
  Criei uma camada de provedores plugáveis e escolhi um modelo por papel.
  Descartados: o modelo local (4B), que gerava 2 tokens/s; o Gemini "high", que levaria 27 h; e um modelo
  do Hugging Face treinado em projetos de lei, que não classifica.
- **Cotas das assinaturas.** Foram o gargalo real. A CLI do Claude esgotou no meio dos cartões, e o
  verificador trocou de Claude para Gemini. Isso o deixou na mesma família de B, um risco que aceitei.
- **Embeddings:** adiados, porque a árvore inteira cabe no prompt.

**Do limiar à previsão.**
- **Chance de acerto de cada candidata:** a taxa da sua faixa, multiplicada por (1 − taxa suposta de
  discordância de convenção do nó). As taxas supostas são 20% para cópia em outra disciplina, 10% para
  sobreposição e 3% para "(Parte N)".
- **Limiar:** a régua vale para o **conjunto** das publicadas, não para cada questão: pelo menos 95% delas
  precisam estar certas. Publico o maior conjunto cujo **percentil 10** da precisão (1.000 sorteios da
  incerteza das faixas) fica em 95% ou mais. O corte só cai entre faixas:

  | Publicadas | Cobertura | Precisão estimada | Percentil 10 | Decisão |
  |---:|---:|---:|---:|---|
  | **81** | 23% | 0,983 | **0,955** | publicado |
  | 127 | 35% | 0,972 | 0,945 | não passou |
  | 135 | 38% | 0,967 | 0,940 | não passou |
  | 207 | 58% | 0,925 | 0,886 | não passou |

- **Resultado:** as 81 de consenso total em temas sem risco de convenção. As 46 seguintes (consenso em
  temas "(Parte N)", chance de 0,95) só entram com a confirmação da convenção (memo).
- **Alternativa descartada:** publicar enquanto a média estimada ficasse em 95% ou mais. Daria 135
  questões (38%), mas com percentil 10 de 0,94: mais de 10% de chance de o resultado real ficar abaixo da
  régua, o erro mais caro do case.
- **Ponto previsto:** a média de dois estimadores. Um é a taxa da faixa (0,983). O outro é o acerto do gold
  que caiu nas publicadas: 13 de 13, suavizado para 0,964, para não tratar 13 acertos como certeza (D12).
  A média dá **0,97**. O intervalo vem dos sorteios.
- **O que não medi:** a precisão numa amostra independente (a mesma amostra calibra e confere), a convenção
  real dos especialistas e a variação dos modelos entre execuções.

Gráficos de confiabilidade e de precisão × cobertura em [`saidas/avaliacao/graficos.md`](../saidas/avaliacao/graficos.md).

## b) Diagnóstico

**Nas questões.**
- **Ruído do banco:** "\n" e "\t" gravados como texto em 106 questões (29%); uma questão com 108 mil
  caracteres de HTML colado do Word. O campo "comando" quase nunca ajuda: vazio em 101 questões, gerado por
  outra ferramenta em 62, cópia do enunciado em 72, frase-padrão em 74. Só 50 trazem informação.
- **Enunciados genéricos** ("Assinale a correta") com alternativas de temas diferentes: no gold, 20% são
  multitema. Não há um tema central único, e qualquer escolha pode errar.
- **Certo/errado (58):** as alternativas não dizem nada; às vezes a afirmação está no comando.
- **Jurisprudência (49):** o tema vem do caso julgado, não de um artigo de lei.
- **Rótulos de origem errados.** Exemplos: extorsão mediante sequestro como "Lesão Corporal"; falso
  testemunho como "Concurso de Crimes". Quem confia neles herda os erros (36%).

**Nos temas.**
- **Sem definição:** o título é a única pista, para máquina e para humano. "Conceitos e Espécies de
  Prisão", "Prisão Preventiva" e "Medidas Cautelares Diversas" só se separam com uma regra escrita.
- **Duplicados:** 20 fantasmas (ativos, sem descrição e sem questões), como "Penal > Lei Maria da Penha"
  ao lado de "Legislação Especial > Lei Maria da Penha", e "Teoria da Pena (Parte 1)" e "(Parte 2)". A
  equipe disse que a escolha fica a critério do candidato. Adotei o nó com histórico (D1), mas o gabarito
  pode ter usado o outro.
- **Sobreposições:** "Ação Penal" em Penal e em Processo Penal; Juizados; interceptação; "Teoria da Pena" ×
  "Teorias Legitimadoras da Pena".
- **Lixeiras:** "Conceito e Fontes do Direito Penal" concentra 74% das questões do tema; "Lei Penal no
  Tempo", 80%. Na dúvida, modelo e humano escapam para o tema introdutório.
- **Títulos com erro:** "Crimonológicas", "Comeptência", "Estaturo".

**Que questão é difícil, com evidência.**
- **Irmãos e fronteiras.** O pipeline errou o tema sugerido em 6 questões do gold, e as 6 foram para
  revisão. Em 5 delas, o tema escolhido estava na minha própria lista de "também plausível".
  - Três erros são entre irmãos: dois entre "Teorias de Nível Sociológico" e "Teorias Criminológicas em
    Espécie", que se sobrepõem; um em ação penal privada.
  - Três são fronteiras entre temas: prazos do inquérito × denúncia; atribuição da Polícia Federal ×
    competência; correspondência do preso (LEP × inviolabilidade).
- **Convenção.** É ela que derruba a cobertura de Legislação Especial: só 12% publicadas, contra 40% em
  Criminologia, 26% em Penal e 19% em Processo Penal. LEP (15 questões), Drogas (11) e Maria da Penha (9)
  vão para revisão porque o tema tem cópia em outra disciplina.
- **De onde vêm as 276 revisões:**
  - 46 têm consenso total, mas em temas "(Parte N)";
  - 51 estão em temas com cópia em outra disciplina (30 delas com consenso total);
  - 28 estão em sobreposições;
  - 4 cobrem vários temas e têm enunciado genérico. Três delas têm confiança de 0,98: foram para revisão
    por essa regra, não por dúvida sobre o tema;
  - o resto é discordância entre as fontes (na faixa "confirma parcial", 86% de acerto no gold), dúvida do
    verificador e 14 "possível fora do recorte".

## c) Produção: 50 mil questões por semana

O case deixou três lições:
1. A qualidade não depende de um LLM mais forte: depende de **evidência** para saber quando se acertou.
2. Assinaturas não escalam: cotas que acabam em horas, nenhum processamento em lote e 13 a 66 mil tokens de
   sobrecarga do agente por chamada.
3. O custo dominante é o tempo do professor.

**Arquitetura: cascata de custo crescente, com humano no ciclo.**
```
importação → texto canônico → duplicatas (hash, embeddings): duplicata validada herda o tema
  → cache por (questão, versão da árvore e do pipeline): só segue o novo ou o reportado
  → N1: classificador treinado + voto barato; se concordam com P alta, decide
  → N2 (o resto): dois LLMs de famílias diferentes + verificador, em lote, árvore em cache
  → limiar por disciplina → publicar | fila do professor (acessos × incerteza) | fora
```

| Tipo de IA | Onde entra | Por quê |
|---|---|---|
| Embeddings (modelo próprio) | Toda questão: duplicatas, vizinhos já validados, agrupar os "fora" | Quase de graça; reaproveita os rótulos |
| Classificador treinado | N1 | Custo ~zero; melhora toda semana com as revisões |
| LLM pequeno ou aberto | Voto barato em toda questão nova | Detecta dúvida a baixo custo (E3b) |
| LLMs fortes + verificador | N2, só nos incertos | A qualidade compensa ali; famílias diferentes mantêm a independência dos votos |
| Agentes | Fora do fluxo por questão: manutenção da árvore (propor temas a partir dos "fora", sugerir fusões) | A árvore cabe no contexto; agente por questão encarece e dificulta auditar |
| Professor | Fila priorizada com sugestão, segunda opção e definições | Fonte da verdade; cada decisão vira rótulo |

**Custo por questão.**

Base: o perfil de tokens medido no case, sem a sobrecarga das CLIs. No N2, são ~70 mil tokens de entrada
por questão, ~85% deles repetidos (árvore e cartões) e em cache de prompt. A saída tem 5 a 12 mil tokens,
quase tudo raciocínio do verificador. O preço é o de lista de um modelo intermediário, em lote.

| Etapa | Custo |
|---|---|
| N1: embeddings, classificador e voto barato em lote | ~US$ 0,002 por questão |
| N2 | ~US$ 0,04 a 0,08 por questão que chega até ele |
| N2 na média, com 35% a 50% das questões chegando lá | ~US$ 0,015 a 0,04 por questão |
| **Total de máquina** | **~US$ 0,02 a 0,04 por questão processada** |

- **Rodada completa:** as 50 mil saem por US$ 1 a 2 mil.
- **Semana típica:** com o cache, só o que mudou é processado. Exemplo: 5 mil questões, US$ 100 a 200.
- **Comparação:** o ensemble completo em todas as 50 mil, toda semana, custaria US$ 4 a 7,5 mil.
- **Professor:** rotular do zero me custou 3 min por questão; validar uma sugestão deve levar ~1 min. Por
  isso a fila é ordenada por impacto (acessos dos alunos) e não precisa zerar: o que não foi revisado
  não é publicado.

**Qualidade contínua.**
- **Auditoria semanal:** 150 publicadas sorteadas por disciplina, revisadas por professores. A precisão sai
  com intervalo; se o limite inferior cair abaixo de 95%, o limiar sobe sozinho.
- **Gold de regressão** (~500 rótulos): nenhuma troca de prompt, modelo, cartão ou árvore entra sem passar
  nele.
- **Reportes de alunos:** a questão reportada volta para a fila com prioridade. Um painel mostra a taxa de
  reporte por tema, por versão e por modelo; um pico aponta lixeira, definição ruim ou piora de um modelo.
- **Deriva por lote de importação:** distribuição de temas e taxas de publicar, revisar e fora.
- **Versionamento:** cada decisão grava modelo, prompt e as versões da árvore, dos cartões e da calibração.
  O cache do case já faz isso por chamada.

**Encaixe nos fluxos.**
- **Importação:** lote noturno.
- **Revisão:** uma tela com a questão, a sugestão, a segunda opção e as definições. Aceitar leva um clique,
  e cada aceite realimenta o N1 e a calibração.
- **Reportes:** viram sinal de qualidade e prioridade na fila.
- **Mudança na árvore:** reclassifica só as questões cujos candidatos tocam os nós alterados.

Já servem à produção: o texto canônico, a camada de provedores com cache e custo, os cartões e a calibração.

## O que faria com mais tempo

1. **Confirmar a convenção com a equipe e reprocessar**, sem nenhuma chamada nova. A cobertura iria de 23%
   para 35% só com os "(Parte N)", e para 46% com todos os duplicados.
2. **Revisar os cartões das zonas de risco** com um especialista. Ficaram como rascunho do modelo (D7).
3. **Ampliar o gold** em 150 questões, concentradas na faixa "confirma parcial" e nos temas de risco. Isso
   certificaria mais faixas e testaria a previsão numa amostra independente.
4. **Rodar o E6:** comparar modelos por papel e trocar o verificador para uma família diferente da de B.
5. Medir a variação entre execuções (rodar duas vezes) e usar embeddings para achar duplicatas.

<div style="page-break-before: always"></div>

## d) Memo para o professor

**Assunto:** classificação automática das 359 questões: o que encontrei e do que preciso de você.

**O que foi feito.** Um sistema leu as 359 questões e sugeriu um tema para cada uma. Ele só publica sozinho
quando várias "opiniões" independentes concordam e um conferente confirma. Conferi à mão uma amostra desse
grupo e não encontrei erro. O resto vai para você, sempre com uma sugestão.

**Resultado.**
- **81 publicadas (23%).** Estimo 97% de acerto (entre 93% e 100%): de 81, cerca de 2 erradas; no pior
  cenário razoável, 6. A meta de 95% vale para o conjunto das publicadas, não para cada questão. Por isso
  parei em 81: com as 46 seguintes, a média continuaria perto de 97%, mas a margem de segurança cairia
  abaixo de 95%.
- **276 na sua fila**, cada uma com o tema sugerido, as alternativas e o motivo da dúvida.
- **2 fora do recorte:**
  - Q0142: isenção de ITCD, Direito Tributário;
  - Q0168: suborno de técnico de futebol para alterar o resultado de um jogo; nenhum tema da árvore cobre
    esse crime.

**O que encontrei nos temas.** É o que mais atrapalha, para a máquina e para quem estuda.
1. **Quase nenhum tema tem definição:** só 20 de 373 têm descrição de verdade. O título é a única pista.
2. **Temas duplicados.** "Lei Maria da Penha", "Tráfico de Drogas", "Lavagem" e "Lei de Execução Penal",
   entre outros, existem em Legislação Especial e também em Penal ou em Processo Penal. "Teoria da Pena
   (Parte 1)" e "(Parte 2)" convivem com "Teoria da Pena". As cópias não têm nenhuma questão.
3. **Temas que viraram "lixeira":** "Conceito e Fontes do Direito Penal" reúne 74% das questões do tema;
   "Lei Penal no Tempo", 80%.
4. **Temas sobrepostos:** "Ação Penal" em Penal e em Processo Penal; Juizados Especiais; "Teoria da Pena" ×
   "Teorias Legitimadoras da Pena".
5. **Subtemas que se confundem:** "Teorias de Nível Sociológico" × "Teorias Criminológicas em Espécie"
   respondem por 2 dos 6 erros que encontrei na minha amostra.
6. **Títulos com erro de digitação:** "Crimonológicas", "Comeptência", "Estaturo".

**O que recomendo mudar.**
- **Apagar as cópias e os "(Parte N)"**, movendo o que houver para o tema original.
- **Escrever uma linha por tema:** "entra / não entra / vai para". Deixei um rascunho para os 351 temas;
  falta a sua validação.
- **Dividir as lixeiras** em subtemas concretos.
- **Escrever a regra dos pares material × processual.** Exemplo: CP, arts. 100 a 106, em Penal; denúncia e
  queixa em Processo Penal.
- **Corrigir os títulos.**

**Do que preciso de você, por ordem de impacto.**
1. **Uma regra sobre os duplicados (~30 min).**
   - A pergunta: numa questão de LEP, o tema certo é "Legislação Especial > LEP" ou "Processo Penal > LEP"?
     E nos "(Parte N)", vale o tema sem número?
   - Usei o tema que tem histórico de questões. Se você confirmar só a regra dos "(Parte N)", publico mais
     **46 questões**, sem refazer nada: a cobertura vai de 23% para 35%. Confirmando também as cópias,
     **84 questões** (46%).
2. **Validar as definições dos temas de risco** (~2 h): as cópias, as 6 sobreposições e as 11 lixeiras
   mais fortes.
3. **Revisar a fila de 276 questões**, a 1 ou 2 min cada (a sugestão já vem pronta). A coluna de confiança
   mostra por onde começar: nas 46 de consenso, deve bastar confirmar. Três questões têm confiança alta
   (0,98) e mesmo assim estão na fila, porque cobrem vários temas: nelas, falta escolher o tema central.
4. **Confirmar os 2 "fora"** e olhar 14 questões que talvez sejam de outra matéria.
5. **Daqui para a frente:** revisar uma amostra de ~150 publicadas por semana, para saber se os 95% se
   mantêm.
