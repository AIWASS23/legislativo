# Classificação de tópicos sem LLM na decisão: relatório da etapa 2

21/10/2026 · Código e como rodar: [README](../../README.md) · Decisões tomadas à mão: [`decisoes_manuais.md`](../../decisoes_manuais.md) · Experimentos: [`registro.md`](../../saidas/experimentos/registro.md)

**Resultado.**
- **As 659 questões:** 152 publicar, 497 revisar (todas com tema sugerido e motivo) e 10 fora.
- **As 559 avaliadas:** **127 publicadas (23%)**, com precisão prevista de **0,96** (0,91–0,99).
- **Como regenerar:** um comando, sem modelo de linguagem e sem rede, em ~47 s de CPU, com a mesma saída byte a byte.
- **Checagem independente:** no gold que rotulei à mão (46 das avaliadas), as 10 publicadas estão certas.
- **Custo:** US$ 0 pagos. O LLM só trabalhou sobre os temas (124 chamadas, nenhuma questão entrou), e a revisão
  me tomou 3 h.

## a) O sistema

**Duas fases** ([diagrama](arquitetura.png)). O LLM organiza o conhecimento antes; a decisão só lê artefatos
versionados, cada um com a sua origem no manifesto (`dados/conhecimento/manifesto.json`).

**Fase de conhecimento: o que o LLM e os embeddings fizeram, sempre sobre os temas e nunca sobre as questões.**
- **Mapa lei/artigo → tema e termos:**
  - o `codex` (`gpt-6.1-sol`) propôs 568 linhas e 3.945 termos;
  - revisei 1.680 itens em 3 h: todo o mapa, os termos de risco e uma amostra de 315, com 3,2% de erro (D14).
- **Citações:** a regex resolve 209 artigos em 94 questões. Resolvi 3 pendentes à mão, e uma amostra de 20 deu
  20 certos.
- **Base de temas:** cartão, termos e leis. As questões da folha entram só como IDs.
- **Exemplos sintéticos:** 3 questões-modelo por tema (D16).
- **Embeddings:** o `qwen3-embedding:4b` local venceu 5 candidatos (E8), com top-1 de 79% e recall@10 de 98%,
  contra 67% e 93% do BM25. Os vetores ficam em cache.

**Fase de decisão (`executar_sistema.py`, sem LLM; uma trava bloqueia a rede e qualquer provedor).**
1. **Candidatos:** os 10 primeiros do denso e do BM25, os temas do mapa, os dos termos fortes e os pais dos
   subtemas. O tema certo está entre eles em 91 de 92 questões.
2. **20 atributos por par (questão, tema):** denso e BM25, mapa de artigos, termos, exemplos sintéticos, vizinhos
   rotulados da folha e estrutura da árvore.
3. **Ranqueador:** gradient boosting (o vencedor do E10). O rótulo de cada par já é a régua (tema central, extra,
   pai ou filho), então ele estima direto **P(certo | publicar o nó)**. Com os pais entre os candidatos, o recuo
   para o pai sai sozinho quando a dúvida é entre irmãos.
4. **Regras com motivo:** direito militar → `fora` (a árvore não tem tema militar); perto de tema inativo →
   `revisar`.
5. **Calibração e limiar:** publica-se o maior conjunto com ponto estimado ≥ 97% (D15). A previsão junta o modelo
   e o acerto fora da amostra da folha na mesma faixa (24 de 25).

**Os experimentos que formaram o sistema** (todos pré-registrados, na folha e fora da amostra):

| Experimento | Resultado | Decisão |
|---|---|---|
| E7b, E8b: documento do tema | Termos revisados: +6 pontos no top-1 do BM25 e +5 no denso; leis: +2 no denso | Documentos com termos (BM25) e com termos e leis (denso) |
| E10: logística × boosting | Log-loss de 0,403, contra 0,433; topo 50 com 48 certas e 1 fora, contra 45 e 3 | Boosting |
| E13: exemplos sintéticos | Log-loss de 0,363, contra 0,403; nó certo em 82, contra 77 | Adotados: 97 → 127 publicadas |
| E11b: separar o fora | AUC fora da amostra de 0,61 (o limite era 0,7) | Plano B: o fora entra como risco na calibração |
| E12: deriva antigas × novas | AUC de 0,58 na similaridade (efeito < 0,1) | Sem alargar a previsão |
| LambdaMART, embeddings extras, filtro de concordância, antitemas, gold no treino | Pioram ou não mudam | Descartados (registro) |

## b) Os 100 rótulos

**Como usei a folha:**
1. **Treino.** Cada uma das 100 questões gera cerca de 22 pares candidatos, rotulados pela régua da avaliação
   (as 8 fora só geram negativos). São cerca de 2.200 pares.
2. **Medida fora da amostra.** Usei validação cruzada estratificada, com 5 partes e 10 repetições. O kNN só vê as
   questões de treino de cada parte. As 559 avaliadas são previstas pelos mesmos 50 modelos, para ficarem na escala
   em que a calibração foi medida.
3. **Calibração e previsão.** A P fora da amostra das 100 calibra a confiança. O acerto das questões da folha que
   cairiam na faixa publicada entra na previsão.
4. **Seleção de modelo só entre configurações pré-registradas,** pela menor log-loss (E8, E7b, E8b, E10, E13).
   Todas as configurações testadas estão no registro, inclusive as descartadas.

**O que não fiz com a folha, para não vazar:** escrever regra a partir das questões dela ou pôr o texto delas nos
documentos de tema. Por exemplo, a regra "assunto de origem aponta outro ramo → revisar" limpava o topo da folha,
mas no meu gold esse conflito aparece em 21 questões, 20 delas certas. Ficou de fora.

**O que os rótulos ensinaram:**
- **O fora da equipe não tem cara de fora.** As 8 questões fora têm conteúdo da árvore: fixação da pena, aplicação
  da lei penal, prisão domiciliar na LEP (art. 117).
  - Nenhum atributo as separa: AUC de 0,54 com atributos lexicais e de 0,61 com embeddings e kNN.
  - A proximidade com um tema inativo é o melhor sinal (AUC de 0,83) e virou regra de revisão.
- **Convenção.** A equipe nunca usa os nós "(Parte N)" e usou a LEP duplicada duas vezes. O meu gold bate com a
  folha em 12 de 14 questões.
- **Multitema é comum:** 39 das 92 questões com tema têm extras, por isso a régua aceita o extra.
- **A folha só tem questões antigas.** O E12 conferiu que as novas não mudam a similaridade nem a margem.

## c) Diagnóstico

**Onde acerta.** Fora da amostra, o nó escolhido acerta 82 das 100 questões da folha (82 das 92 com tema; as 8 fora
são sempre erro). Ordenadas pela confiança:

| Questões da folha | 20 | 30 | 40 | 50 | 70 | 100 |
|---|---:|---:|---:|---:|---:|---:|
| Certas | 19 (95%) | 29 (97%) | 39 (98%) | 48 (96%) | 64 (91%) | 82 (82%) |
| Fora entre elas | 1 | 1 | 1 | 2 | 3 | 8 |

**Onde erra e o que resolveria cada caso:**
- **Fora com cara de tema.** A Q0087 cita o art. 117 da LEP, e a equipe a marcou como fora. Nenhum sinal do texto
  separa esse caso; testei regras, antitemas e concordância. **Resolveria:** um critério de fora combinado com a
  equipe.
- **Subtemas irmãos.** O top-1 do denso é de 96% no nível 1 e de 72% no subtema. O recuo para o pai resolve parte.
  **Resolveria:** definições que digam o que separa os irmãos, revisadas pelo professor.
- **Os dados e os temas também atrapalham:**
  - 353 dos 373 temas não tinham descrição (os cartões, termos e exemplos suprem isso como rascunho);
  - há nós duplicados ("(Parte N)" e a LEP fantasma) e temas inativos com questões perto deles;
  - não há tema de Direito Penal Militar;
  - o assunto de origem das questões erra muito (36% de acerto na etapa 1).

**O que segura a cobertura é a incerteza, não a ordenação.**
- O topo 40 da folha está 98% certo, mas, com 100 rótulos, o percentil 10 da precisão fica 0,03 abaixo do ponto.
- Pelo critério estrito (percentil 10 ≥ 95%), seriam 58 publicadas, contra 127.
- A log-loss ainda cai com mais rótulos: 0,548, 0,477 e 0,446 com 40, 60 e 80 (E14).

**Conferência independente** (o meu gold da etapa 1, 46 questões avaliadas, fora do treino): as 10 publicadas e as 26
com confiança ≥ 0,80 estão certas, e o tema sugerido acerta 42 de 46. O gold não tem questões fora.

**O que faria com mais tempo:**
1. Rotular a fila de rotulagem ativa (150 questões perto do limiar).
2. Combinar a convenção de fora com a equipe.
3. Revisar os 2.833 termos e os 1.023 exemplos ainda em rascunho.
4. O desconto de convenção por tipo de nó, que ficou de fora (D15).

## d) Produção

**Fluxo** ([ADR-027](../../docs/adr/08-etapa2/ADR-027-producao-e-retreino.md); [diagrama de produção](arquitetura_producao.png)):
1. **Importação:** o texto canônico e o hash. Uma duplicata de questão validada herda o tema.
2. **Conhecimento:** a regex das citações (com um LLM pequeno só quando ela falha) e os embeddings da questão.
3. **Decisão em CPU:** os mesmos candidatos, o ranqueador, as regras, a calibração e o limiar.
4. **Saída:** publicar; revisar, para a fila do professor; ou fora, agrupado para propor temas novos.

**Custo e tempo para 50 mil questões por semana: da ordem de US$ 0,0001 por questão.** Isso é de 200 a 400 vezes
menos que a decisão por LLM da etapa 1.
- **Decisão:** CPU, segundos a minutos para 50 mil.
- **Embeddings:** são cerca de 250 mil textos, contando as alternativas.
  - Nesta GPU de 6 GB, a ~7 textos por segundo, levariam ~10 h, uma noite.
  - Uma GPU de servidor ou uma API faz isso em menos de 1 h.
- **O custo dominante é o professor:** cerca de 1 minuto por sugestão confirmada.

**O professor no ciclo:**
- **Memória do kNN, imediata:** cada confirmação ou correção vira rótulo, e a próxima questão parecida já tem um
  vizinho validado.
- **Retreino semanal do ranqueador:** só entra se passar no gold de regressão (a folha mais as auditorias).
- **Calibração:** só com a auditoria aleatória de 150 publicadas por semana. A fila é enviesada pela incerteza e
  distorceria as probabilidades.
- **Alarme:** se o limite inferior da precisão cair abaixo de 95%, o limiar sobe.
- **Temas com correções repetidas:** viram revisão do documento do tema e dos termos. O LLM propõe, o professor
  revisa e tudo vira dado de novo.

**O que cresce sozinho,** sem LLM na decisão: os rótulos, que aumentam a cobertura (E14); os vizinhos validados,
que melhoram o kNN; e as revisões de tema, que melhoram os documentos.

<div style="page-break-before: always"></div>

## e) Memo para o professor

**O que mudou no classificador.** Ele agora decide sem inteligência artificial generativa. O modelo de linguagem só
ajudou a montar o "dicionário" de cada tema:
- os artigos de lei que pertencem a ele;
- as expressões típicas;
- questões-modelo.

Eu revisei esse material. Na hora de classificar, o sistema compara cada questão com esse dicionário e com as
questões que a equipe já classificou. Por isso é rápido, barato e explicável: cada sugestão vem de um artigo
citado, de um termo, ou da semelhança com um tema ou com uma questão já rotulada.

**O que você vai receber:**
- **127 das 559 questões vão direto para os alunos,** com uma precisão estimada de 96% (entre 91% e 99%). Quando o
  sistema fica entre dois subtemas parecidos, ele publica no tema-pai, que também conta como certo.
- **422 vão para a sua fila,** sempre com uma sugestão de tema:
  - 120 têm confiança de 90% ou mais: em geral, basta confirmar, em cerca de 1 minuto cada;
  - 83 estão marcadas "perto de um tema inativo": podem não ter tema na árvore;
  - as demais trazem a sugestão e uma segunda opção.
- **10 questões de Direito Penal Militar ficaram de fora,** porque a árvore não tem tema militar.

**Como o seu trabalho melhora o sistema:**
- **Cada sugestão que você confirma ou corrige vira um exemplo.** Na mesma hora, questões parecidas passam a ter
  esse vizinho. Toda semana, o modelo é retreinado com elas.
- **O que mais ajuda é rotular a fila de prioridade** (150 questões perto do limite de publicação). Hoje o sistema
  já ordena bem, mas tem só 100 exemplos para provar que está certo. Com o dobro, a parcela publicada direto deve
  crescer sem perder a régua de 95%.
- **Quando um tema é corrigido várias vezes,** o problema costuma estar na definição dele. Nesses casos, eu peço que
  você revise o dicionário do tema (termos e artigos), e não questão por questão.

**O que recomendo mudar nos temas:**
- **Duplicados:** desativar os nós "(Parte N)" e a LEP repetida. A equipe nunca usa os primeiros, e os dois confundem
  a classificação.
- **Temas inativos:** reativar ou remover de vez "Direito penal econômico" e "Tratados e convenções". Questões perto
  deles hoje vão para a revisão.
- **Direito Penal Militar:** criar um tema, ou deixar registrado que fica fora.
- **"Inquérito Civil" dentro de Processo Penal:** rever o lugar desse tema.
- **Descrições:** só 20 dos 373 temas tinham uma. Escrevi rascunhos com termos e exemplos, mas a sua revisão desses
  textos é o que mais melhora os subtemas parecidos.

**O que eu preciso de você:**
1. **Uma regra para "fora da taxonomia".** Algumas questões que a equipe marcou como fora, como uma sobre prisão
   domiciliar com o art. 117 da LEP, parecem ter tema na árvore. Saber o critério resolve o maior tipo de erro do
   sistema.
2. **A convenção dos temas duplicados:** "(Parte N)" e a LEP repetida. Qual nó vale?
3. **Uma auditoria de 150 publicadas por semana,** sorteadas. É ela que diz se a precisão continua acima de 95%.
