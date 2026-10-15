# Revisão dos cartões de tema

Gerado em 15/10/2026 14:05. 351 cartões; prioridade 1 (lixeiras fortes): 11, 2 (sobreposições): 34, 3 (irmãos parecidos): 177, 4 (amostral): 129.

Para corrigir um cartão, acrescente uma linha em `dados/temas/cartoes_ajustes.csv`
(`tema_id,campo,valor,motivo`; listas separadas por ` | `; em `nao_inclui`, `assunto -> tema_id`)
e rode `uv run python executar_cartoes.py` de novo (os rascunhos vêm do cache).

## Prioridade 1

### 5088 · lixeira forte

```text
[5088] Penal > Dos Crimes Contra a Administração Pública > Noções gerais dos crimes praticados contra a administração pública [conceitual]
Escopo: Aspectos gerais do Título XI do CP: bem jurídico, conceito penal de funcionário público e equiparado (art. 327), classificação em crimes funcionais próprios e impróprios e regras comuns. Não abrange os elementos de cada crime em espécie.
Inclui: Conceito de funcionário público e funcionário por equiparação (art. 327, caput e § 1º); Causa de aumento do art. 327, § 2º (cargos em comissão e direção); Crimes funcionais próprios e impróprios; Crimes praticados por particular contra a Administração em geral (visão geral); Insignificância nos crimes contra a Administração Pública (Súmula 599 do STJ); Progressão de regime condicionada à reparação do dano (CP, art. 33, § 4º)
Não inclui: Comunicabilidade da condição de funcionário ao particular coautor ou partícipe → 5076; Perda do cargo como efeito da condenação (art. 92, I) → 5209; Resposta preliminar do funcionário no procedimento dos crimes funcionais (CPP, art. 514) → 5533; Elementos e consumação do peculato em suas modalidades → 5089; Crimes de abuso de autoridade (Lei 13.869/2019) → 4684
Âncoras legais: CP, art. 327; CP, art. 33, § 4º
Desempate: Use este nó só quando a questão tratar de conceito de funcionário público, classificação ou regras comuns aos crimes do Título XI; se exigir os elementos de um tipo específico, classifique no subtema desse crime.
```

### 5117 · lixeira forte

```text
[5117] Penal > Dos Crimes Contra a Fé Pública e de Falsidade Documental > Dos Crimes contra a Fé Pública [conceitual]
Escopo: Noções gerais dos crimes contra a fé pública (bem jurídico, requisitos do falso, falsificação grosseira) e capítulos do Título X sem subtema próprio: moeda falsa, falsificação de títulos e papéis públicos e fraudes em certames de interesse público.
Inclui: Fé pública como bem jurídico e sujeito passivo; Requisitos gerais do falso: imitação da verdade, dano potencial, dolo; Falsificação grosseira e crime impossível ou estelionato (Súmula 73 do STJ); Moeda falsa, crimes assimilados e petrechos para falsificação (arts. 289 a 291); Falsificação de títulos e outros papéis públicos (arts. 293 a 295); Fraudes em certames de interesse público (art. 311-A)
Não inclui: Falsificação de documento público ou particular, falsidade ideológica, uso de documento falso → 5118; Falsa identidade e adulteração de sinal identificador de veículo → 5119; Competência da Justiça Federal para moeda falsa → 5482; Falso testemunho ou falsa perícia → 5081; Classificações gerais de crimes (crime formal, de perigo) → 5174
Âncoras legais: CP, arts. 289 a 295; CP, art. 311-A; STJ, Súmula 73
Desempate: Use este nó para questões sobre o conceito e os requisitos gerais dos crimes contra a fé pública ou sobre moeda falsa, papéis públicos e fraude em certames; se a questão tratar de crime específico dos arts. 296 a 305, use 5118, e dos arts. 306 a 311, use 5119.
```

### 5171 · lixeira forte

```text
[5171] Penal > Introdução ao Estudo do Direito Penal > Conceito e Fontes do Direito Penal [conceitual]
Escopo: Conceito, finalidade e características do Direito Penal, suas divisões e velocidades, e fontes materiais e formais (lei, costume, princípios gerais, jurisprudência, tratados). Sem subtemas próprios.
Inclui: Conceito formal, material e sociológico de Direito Penal; Missão do Direito Penal: proteção de bens jurídicos; Direito Penal objetivo e subjetivo (ius puniendi); Fontes materiais (União, CF, art. 22, I) e formais imediatas e mediatas; Papel do costume, da jurisprudência, das súmulas vinculantes e dos tratados como fontes; Velocidades do Direito Penal (Silva Sánchez); Direito Penal comum e especial, substantivo e adjetivo
Não inclui: Princípios da legalidade, intervenção mínima, lesividade etc. → 5172; Analogia, interpretação extensiva e analógica → 5173; Direito Penal do Inimigo como corrente político-criminal → 4376; Conceito e objeto da Criminologia → 4381; Classificação doutrinária dos crimes → 5174
Âncoras legais: CF, art. 22, I; CF, art. 5º, XXXIX; CP, art. 1º
Desempate: Use apenas quando a questão versar sobre o conceito, a finalidade, as características ou as fontes do Direito Penal em geral; se o núcleo for um princípio específico, um método interpretativo ou uma classificação de crimes, use o irmão correspondente.
```

### 5200 · lixeira forte

```text
[5200] Penal > Teoria da Pena > Sanção Penal: Conceito, Finalidade e Modalidades [conceitual]
Escopo: Conceito de sanção penal, suas finalidades (retributiva, preventiva geral e especial, ressocializadora) conforme o art. 59 do CP, as espécies de pena (art. 32) e as penas vedadas pela CF. Abrange também a distinção entre pena e medida de segurança.
Inclui: Conceito de sanção penal e suas espécies: pena e medida de segurança; Finalidades da pena no CP: reprovação e prevenção (art. 59, teoria mista); Espécies de pena: privativa de liberdade, restritiva de direitos e multa (art. 32); Penas permitidas e vedadas na CF (art. 5º, XLVI e XLVII); Características da pena: personalidade, legalidade, proporcionalidade, inderrogabilidade; Visão geral do sistema de individualização da pena
Não inclui: Teorias legitimadoras da pena sob o enfoque criminológico → 4384; Medida de segurança: espécies, pressupostos e duração → 5184; Regimes e regras da pena privativa de liberdade → 5201; Requisitos e espécies das penas restritivas de direitos → 5205; Princípios penais da humanidade e da individualização → 5172; Fixação da pena-base pelo art. 59 → 5202
Âncoras legais: CP, art. 32; CP, art. 59; CF, art. 5º, XLVI; CF, art. 5º, XLVII
Desempate: Use este nó quando a questão tratar do conceito, da finalidade ou das espécies de sanção penal no Código Penal (art. 59 e art. 32) de forma geral. Se a questão tratar das regras de uma espécie de pena ou de uma fase da dosimetria, use o nó específico. Se tratar das teorias da pena sob o enfoque criminológico, use o nó 4384.
```
Regra D2 (decisão manual): Penal: conceito, finalidade e modalidades da sanção penal no Código Penal (art. 59 e espécies de pena)

### 5212 · lixeira forte

```text
[5212] Penal > Teoria do Crime: Culpabilidade > Conceito e Elementos da Culpabilidade [conceitual]
Escopo: Conceito de culpabilidade, teorias que a explicam (psicológica, psicológico-normativa, normativa pura) e seus elementos em geral: imputabilidade, potencial consciência da ilicitude e exigibilidade de conduta diversa.
Inclui: Teoria psicológica, psicológico-normativa e normativa pura da culpabilidade; Elementos da culpabilidade no finalismo; Culpabilidade como elemento do crime x pressuposto de aplicação da pena (conceitos bipartido e tripartido); Culpabilidade do fato x culpabilidade do autor; Coculpabilidade e coculpabilidade às avessas; Culpabilidade como fundamento e limite da pena; teoria funcionalista da culpabilidade
Não inclui: Hipóteses e critérios de inimputabilidade (doença mental, menoridade, embriaguez) → 5213; Erro sobre a ilicitude do fato e teorias extremada e limitada da culpabilidade aplicadas ao erro → 5214; Culpabilidade como circunstância judicial do art. 59 do CP → 5202; Princípio da culpabilidade e vedação da responsabilidade penal objetiva → 5172; Dolo e culpa como elementos do fato típico → 5222; Causas de exculpação não previstas em lei → 5217
Desempate: Use este nó só para questões sobre o conceito, as teorias e os elementos da culpabilidade em geral; se a questão tratar de uma excludente específica (inimputabilidade, erro de proibição, coação, obediência ou causa supralegal), use o nó próprio dela.
```

### 5467 · lixeira forte

```text
[5467] Processo Penal > Ação Penal > Características e Condições da Ação Penal [conceitual]
Escopo: Conceito de ação penal, características (direito público, subjetivo, autônomo, abstrato e instrumental) e condições da ação: genéricas (legitimidade, interesse, possibilidade jurídica, justa causa) e específicas (condições de procedibilidade).
Inclui: Conceito de ação penal como direito de pedir ao Estado-juiz a aplicação do direito penal; Características: direito público, subjetivo, autônomo, abstrato, determinado e instrumental; Condições genéricas da ação: legitimidade, interesse de agir e possibilidade jurídica do pedido; Justa causa como lastro probatório mínimo; Condições específicas de procedibilidade em geral (representação, requisição, entrada do agente no território); Distinção entre condições de procedibilidade e condições objetivas de punibilidade
Não inclui: Classificação da ação penal (pública incondicionada, condicionada, privada) → 5468; Rejeição da denúncia por falta de condição da ação ou de justa causa (CPP, art. 395) → 5531; Prazo, retratação e forma da representação → 5471; Princípios da ação penal (obrigatoriedade, indisponibilidade, oportunidade) → 5469; Conceito e espécies de ação penal segundo o Código Penal (CP, art. 100) → 5063
Âncoras legais: CPP, art. 395, II e III; CPP, art. 24
Desempate: Use este nó genérico só quando a questão tratar do conceito, das características ou das condições da ação em abstrato. Se tratar de uma espécie de ação, da denúncia, da queixa ou da rejeição da peça (CPP, art. 395), use o nó específico. Questões sobre a ação penal segundo o CP ficam em 5063.
```
Regra D2 (decisão manual): herdada de 5466: Processo Penal: denúncia, queixa, prazos, requisitos, legitimidade e condições da ação (CPP, arts. 24 a 62)

### 5499 · lixeira forte

```text
[5499] Processo Penal > Inquérito Policial > Conceito, Finalidade e Características do Inquérito Policial [conceitual]
Escopo: Noções gerais do inquérito policial: conceito, natureza jurídica administrativa, finalidade, destinatários, valor probatório e características (escrito, sigiloso, inquisitivo, discricionário, oficioso, indisponível, dispensável).
Inclui: Conceito e natureza jurídica de procedimento administrativo pré-processual; Finalidade: apurar autoria e materialidade para subsidiar a ação penal; Características: forma escrita, sigilo, inquisitoriedade, oficiosidade, oficialidade, indisponibilidade, dispensabilidade; Sigilo e acesso do defensor aos elementos já documentados (Súmula Vinculante 14); Valor probatório relativo dos elementos informativos (CPP, art. 155); Vícios do inquérito não contaminam a ação penal; Polícia judiciária e atribuição da autoridade policial
Não inclui: Instauração, diligências, indiciamento e prazos do inquérito → 5500; Relatório final, arquivamento e desarquivamento → 5501; Controle judicial da investigação pelo juiz das garantias → 5503; Inquérito civil conduzido pelo Ministério Público → 5504; Prova ilícita e derivada obtida na investigação → 5594
Âncoras legais: CPP, art. 4º; CPP, art. 9º; CPP, art. 12; CPP, art. 17; CPP, art. 20; CPP, art. 155; Súmula Vinculante 14; Lei 12.830/2013
Desempate: Use este nó só para conceito, natureza, finalidade e características gerais do IP; questões sobre atos específicos de instauração, diligências, prazos ou arquivamento vão para 5500 ou 5501.
```

### 5582 · lixeira forte

```text
[5582] Processo Penal > Sistemas e Princípios Processuais Penais > Princípios do Processo Penal [conceitual]
Escopo: Princípios gerais e constitucionais que regem o processo penal como um todo: devido processo legal, contraditório, ampla defesa, presunção de inocência, juiz natural, publicidade, vedação à autoincriminação, duração razoável, entre outros. Princípios específicos de ação, prova, recursos e júri ficam em nós próprios.
Inclui: Devido processo legal, contraditório e ampla defesa (defesa técnica e autodefesa); Presunção de inocência/não culpabilidade e in dubio pro reo; Juiz natural e promotor natural; Nemo tenetur se detegere (vedação à autoincriminação); Publicidade dos atos processuais e motivação das decisões; Duração razoável do processo, favor rei e paridade de armas; Princípio da verdade real/processual e da identidade física do juiz como princípios gerais
Não inclui: Princípios da obrigatoriedade, indisponibilidade, oportunidade e indivisibilidade da ação penal → 5469; Princípios relativos à prova (comunhão, liberdade probatória, vedação de provas ilícitas) → 5595; Princípios recursais (voluntariedade, unirrecorribilidade, non reformatio in pejus) → 5513; Princípios constitucionais do júri (plenitude de defesa, soberania dos veredictos, sigilo das votações) → 5525; Sistema acusatório, inquisitivo e misto → 5581; Princípios do Direito Penal material (legalidade, insignificância, culpabilidade) → 5172
Âncoras legais: CF, art. 5º, LIII; CF, art. 5º, LIV; CF, art. 5º, LV; CF, art. 5º, LVII; CF, art. 5º, LXIII; CF, art. 5º, LXXVIII; CF, art. 93, IX; CPP, art. 186
Desempate: Use este nó quando a questão versar sobre princípios gerais do processo penal; se o princípio for próprio da ação penal, da prova, dos recursos ou do júri, classifique no nó específico (5469, 5595, 5513, 5525).
```

### 5581 · lixeira forte

```text
[5581] Processo Penal > Sistemas e Princípios Processuais Penais > Sistemas Processuais Penais [conceitual]
Escopo: Conceito, características e distinção dos sistemas processuais penais (inquisitivo, acusatório e misto) e a identificação do sistema adotado no Brasil, inclusive após a Lei 13.964/2019 (estrutura acusatória do CPP).
Inclui: Características do sistema inquisitivo (concentração das funções, sigilo, réu como objeto); Características do sistema acusatório (separação entre acusar e julgar, contraditório, publicidade); Sistema misto ou francês (fase inquisitiva e fase acusatória); Sistema adotado no Brasil e art. 3º-A do CPP; Gestão da prova e iniciativa probatória do juiz como critério de distinção dos sistemas; Vedação à iniciativa do juiz na fase de investigação
Não inclui: Princípios gerais do processo (contraditório, ampla defesa, presunção de inocência) → 5582; Competências e atuação do juiz das garantias na investigação → 5503; Sistemas de avaliação da prova (íntima convicção, prova tarifada, livre convencimento motivado) → 5592; Características do inquérito policial (inquisitivo, sigiloso, escrito) → 5499
Âncoras legais: CPP, art. 3º-A; CF, art. 129, I
Desempate: Use este nó quando a questão tratar da comparação ou caracterização dos modelos inquisitivo, acusatório e misto ou do sistema adotado no Brasil; se tratar da disciplina do juiz das garantias, use 5503, e se tratar de valoração da prova, use 5592.
```

### 5585 · lixeira forte

```text
[5585] Processo Penal > Teoria Geral das Prisões > Conceitos e Espécies de Prisão [conceitual]
Escopo: Noções gerais de prisão no processo penal: conceito, distinção entre prisão-pena e prisão processual (cautelar), prisão civil e administrativa, e o rol geral de modalidades. Não trata do regime específico de cada prisão.
Inclui: Conceito de prisão e regra geral do art. 283 do CPP; Distinção entre prisão-pena (definitiva) e prisão cautelar (provisória); Prisão civil (devedor de alimentos) e vedação da prisão do depositário infiel (Súmula Vinculante 25); Prisão administrativa e prisão disciplinar militar; Quadro geral das prisões cautelares vigentes: flagrante, preventiva e temporária; Extinção da prisão por pronúncia e por sentença condenatória recorrível como espécies autônomas; Execução provisória da pena e presunção de inocência (ADCs 43, 44 e 54), em visão geral
Não inclui: Requisitos e hipóteses da prisão em flagrante → 5518; Pressupostos, fundamentos e cabimento da prisão preventiva → 5519; Cabimento e prazos da prisão temporária → 5520; Prisão domiciliar substitutiva da preventiva → 5521; Regimes de cumprimento da pena privativa de liberdade → 5201; Uso de algemas, comunicação da prisão e direitos do preso → 5587
Âncoras legais: CPP, art. 283; CPP, art. 282; CF, art. 5º, LXI; CF, art. 5º, LXVII; Súmula Vinculante 25
Desempate: Use este nó só quando a questão tratar do conceito de prisão ou comparar espécies em termos gerais; se ela cobrar requisitos, prazos ou procedimento de uma espécie determinada (flagrante, preventiva, temporária, domiciliar), classifique no nó dessa espécie em Prisões em Espécie.
```

### 5595 · lixeira forte

```text
[5595] Processo Penal > Teoria Geral das Provas > Princípios Relativos à Prova Penal [conceitual]
Escopo: Conceito e conteúdo geral dos princípios que regem a prova penal (comunhão, contraditório da prova, liberdade probatória e seus limites, autorresponsabilidade, oralidade, nemo tenetur se detegere aplicado à produção probatória).
Inclui: Princípio da comunhão ou aquisição da prova; Princípio do contraditório e da audiência bilateral na produção da prova; Liberdade probatória e seus limites (ex.: restrições da lei civil quanto ao estado das pessoas); Princípio da autorresponsabilidade das partes; Princípios da oralidade, concentração e imediação na prova; Nemo tenetur se detegere: direito de não produzir prova contra si mesmo
Não inclui: Distribuição do ônus da prova e poderes instrutórios do juiz → 5591; Inadmissibilidade da prova ilícita e teoria dos frutos da árvore envenenada → 5594; Livre convencimento motivado como sistema de valoração → 5592; Princípios gerais do processo penal (presunção de inocência, devido processo legal, juiz natural) → 5582; Direito ao silêncio no interrogatório judicial → 5547
Âncoras legais: CF, art. 5º, LV; CF, art. 5º, LXIII; CPP, art. 155, parágrafo único
Desempate: Use este nó só quando a questão cobrar o enunciado ou o conteúdo de um princípio probatório em si; se cobrar ônus, ilicitude, prova emprestada ou sistema de valoração, use o nó específico (5591, 5594, 5593 ou 5592), e princípios gerais do processo vão para 5582.
```

## Prioridade 2

### 4384 · sobreposição (pena)

```text
[4384] Criminologia > Teorias Legitimadoras da Pena
Escopo: Teorias que justificam e legitimam a pena: absolutas (retribuição), relativas (prevenção geral e especial, positiva e negativa), mistas ou unificadoras e teorias deslegitimadoras ou agnósticas.
Inclui: Teorias absolutas ou retributivas (Kant, Hegel); Prevenção geral negativa (coação psicológica de Feuerbach) e positiva (Welzel, Jakobs); Prevenção especial negativa (neutralização) e positiva (ressocialização); Teorias mistas ou ecléticas adotadas pelo CP, art. 59; Teoria dialética unificadora de Roxin; Teoria agnóstica ou negativa da pena (Zaffaroni)
Não inclui: Conceito e modalidades de sanção penal (penas e medidas de segurança) no Código Penal → 5200; Modelos dissuasório, ressocializador e restaurador de reação ao delito → 4370; Abolicionismo penal e movimentos de política criminal → 4375; Direito Penal do Inimigo → 4376; Regras da LEP sobre execução e ressocialização do condenado → 4703
Âncoras legais: CP, art. 59; Lei 7.210/1984, art. 1º; Immanuel Kant; G. W. F. Hegel; Paul Anselm von Feuerbach; Claus Roxin
Desempate: As teorias que justificam a pena (absolutas, relativas e mistas; prevenção geral e especial) ficam neste nó; questões dogmáticas sobre o conceito e as espécies de sanção penal no CP vão para 5200.
```
Regra D2 (decisão manual): Criminologia: as teorias que justificam a pena (absolutas, relativas, mistas; prevenção geral e especial)

### 4700 · sobreposição (interceptacao)

```text
[4700] Direito Penal - Legislação Especial > Interceptação Telefônica
Escopo: Lei 9.296/1996 como lei: requisitos e vedações da interceptação de comunicações telefônicas, telemáticas e de informática, legitimados, prazo, procedimento e crimes de interceptação ilegal.
Inclui: Requisitos: ordem do juiz competente, indícios razoáveis, prova indisponível por outros meios, crime punido com reclusão (art. 2º); Legitimados para requerer a medida (art. 3º); Prazo de 15 dias renovável por igual período (art. 5º); Autuação em apartado e sigilo das diligências (arts. 8º e 9º); Crime de interceptação ou quebra de segredo de justiça sem autorização (art. 10); Crime de captação ambiental não autorizada (art. 10-A)
Não inclui: Interceptação telefônica como meio de prova no processo (valoração, encontro fortuito, validade da prova) → 5555; Captação ambiental como meio de obtenção de prova → 5556; Prova emprestada da interceptação → 5593; Prova ilícita e derivada → 5594; Violação de correspondência e comunicação telefônica no CP (art. 151) → 5133
Âncoras legais: CF, art. 5º, XII; Lei 9.296/1996, arts. 1º a 5º; Lei 9.296/1996, art. 10; Lei 9.296/1996, art. 10-A
Desempate: Escolha este nó quando a questão cobrar a Lei 9.296/96 como lei (requisitos, prazo, legitimados, crime de interceptação ilegal); se o foco for o uso da interceptação como prova no processo, use 5555.
```
Regra D2 (decisão manual): Legislação Especial: a Lei 9.296/96 como lei (requisitos, prazo, legitimados, crime de interceptação ilegal)

### 4701 · sobreposição (juizados)

```text
[4701] Direito Penal - Legislação Especial > Juizado Especial Criminal
Escopo: Lei 9.099/1995 como lei na parte criminal: conceito de infração de menor potencial ofensivo e visão geral dos institutos despenalizadores e do rito dos Juizados Especiais Criminais.
Inclui: Conceito de infração de menor potencial ofensivo (art. 61); Princípios e critérios orientadores do JECrim (art. 62); Termo circunstanciado e vedação de prisão em flagrante a quem assume compromisso (art. 69); Composição civil dos danos (art. 74); Visão geral da transação penal e da suspensão condicional do processo; Representação na lesão corporal leve e culposa (art. 88)
Não inclui: Requisitos e procedimento detalhado da transação penal → 5541; Requisitos e condições da suspensão condicional do processo → 5542; Regras de competência dos Juizados Especiais Criminais → 5540; Recursos no âmbito dos Juizados e turma recursal → 5569; Vedação da Lei 9.099/95 na violência doméstica contra a mulher → 4704; Acordo de não persecução penal → 5502
Âncoras legais: Lei 9.099/1995, arts. 60 a 62; Lei 9.099/1995, art. 69; Lei 9.099/1995, arts. 74 e 76; Lei 9.099/1995, arts. 88 e 89; CF, art. 98, I
Desempate: Use este nó quando a questão cobrar a Lei 9.099/95 como lei (menor potencial ofensivo e institutos despenalizadores em visão geral); se detalhar um instituto ou o rito processual, use o subtema de Procedimento Sumaríssimo correspondente.
```
Regra D2 (decisão manual): Legislação Especial: a Lei 9.099/95 como lei (menor potencial ofensivo e institutos despenalizadores em visão geral)

### 4705 · sobreposição (orcrim_meios_prova)

```text
[4705] Direito Penal - Legislação Especial > Organizações Criminosas
Escopo: Lei 12.850/2013 como lei: conceito de organização criminosa, crime de promover, constituir, financiar ou integrar organização, causas de aumento, crimes da lei e visão geral dos meios de obtenção de prova.
Inclui: Conceito legal de organização criminosa (art. 1º, § 1º: 4 ou mais pessoas, estrutura ordenada, divisão de tarefas, penas máximas superiores a 4 anos ou caráter transnacional); Crime de promover, constituir, financiar ou integrar organização criminosa (art. 2º); Embaraço à investigação e aumentos de pena (art. 2º, §§ 1º a 4º); Afastamento cautelar do funcionário público (art. 2º, § 5º); Rol dos meios de obtenção de prova em visão geral (art. 3º); Crimes ocorridos na investigação e obtenção da prova (arts. 18 a 21)
Não inclui: Colaboração premiada: acordo, homologação, valor probatório → 5557; Infiltração de agentes → 5559; Ação controlada → 5558; Associação criminosa (CP, art. 288) → 5146; Associação para o tráfico (Lei 11.343/2006, art. 35) → 4708; Organização terrorista (Lei 13.260/2016) → 4706
Âncoras legais: Lei 12.850/2013, art. 1º; Lei 12.850/2013, art. 2º; Lei 12.850/2013, art. 3º; Lei 12.850/2013, arts. 18 a 21
Desempate: Escolha este nó quando a questão cobrar a Lei 12.850/13 como lei (conceito de organização criminosa, crimes, visão geral); se detalhar um meio de obtenção de prova específico, use o nó correspondente em Provas em Espécie.
```
Regra D2 (decisão manual): Legislação Especial: a Lei 12.850/13 como lei (conceito de organização criminosa, crimes, visão geral)

### 5063 · sobreposição (acao_penal)

```text
[5063] Penal > Ação Penal
Escopo: Ação penal pelo lado material: as regras do Código Penal sobre espécies de ação (pública incondicionada, condicionada e privada), representação, requisição, renúncia, perdão e perempção (CP, arts. 100 a 106). O procedimento da denúncia e da queixa é tratado em Processo Penal.
Inclui: Regra geral da ação penal pública e ressalva expressa de ação privada (CP, art. 100); Ação penal no crime complexo (CP, art. 101); Irretratabilidade da representação após o oferecimento da denúncia (CP, art. 102); Prazo decadencial de 6 meses previsto no CP (art. 103); Renúncia expressa ou tácita ao direito de queixa (CP, art. 104); Perdão do ofendido: extensão aos querelados e necessidade de aceitação (CP, arts. 105 e 106); Ação privada subsidiária da pública no CP (art. 100, § 3º)
Não inclui: Requisitos da denúncia, prazos para oferecê-la e procedimento do oferecimento → 5473; Requisitos, procuração e aditamento da queixa-crime → 5474; Princípios da ação penal (obrigatoriedade, indivisibilidade etc.) pelo enfoque processual → 5469; Hipóteses de perempção do CPP, art. 60, como causa de extinção da punibilidade → 5195; Decadência como causa extintiva da punibilidade (CP, art. 107, IV) → 5198; Ação penal nos crimes contra a dignidade sexual (CP, art. 225) → 5110
Âncoras legais: CP, arts. 100 a 106; CPP, arts. 24 a 62
Desempate: Classifique aqui (ou em 5064/5065) quando a questão tratar das espécies de ação, da representação, da requisição, da renúncia, do perdão ou da perempção como regras do CP (arts. 100 a 106). Se tratar do procedimento previsto no CPP, use Processo Penal > Ação Penal (5466 e filhos). Use o nó-pai quando a questão cobrir ação pública e ação privada ao mesmo tempo.
```
Regra D2 (decisão manual): Penal: espécies de ação penal, representação, requisição, renúncia, perdão e perempção como regras do CP (arts. 100 a 106)

### 5065 · sobreposição (acao_penal)

```text
[5065] Penal > Ação Penal > Ação Penal Privada
Escopo: Ação penal de iniciativa privada pelas regras do Código Penal: queixa do ofendido ou do representante, espécies (exclusiva, personalíssima e subsidiária da pública), sucessão processual (CADI), decadência do direito de queixa, renúncia e perdão do ofendido (CP, arts. 100, §§ 2º a 4º, e 103 a 106).
Inclui: Ação privada exclusiva, personalíssima e subsidiária da pública: conceito e cabimento no CP; Legitimidade do ofendido ou do representante legal para a queixa (CP, art. 100, § 2º); Sucessão em caso de morte ou ausência do ofendido: cônjuge, ascendente, descendente ou irmão (CP, art. 100, § 4º); Ação privada subsidiária pela inércia do Ministério Público (CP, art. 100, § 3º; CF, art. 5º, LIX); Prazo decadencial de seis meses para a queixa e seu termo inicial (CP, art. 103); Renúncia expressa ou tácita ao direito de queixa (CP, art. 104); Perdão do ofendido: cabimento, aceitação, extensão aos querelados e limite temporal (CP, arts. 105 e 106); Perempção como instituto exclusivo da ação privada, em noção geral
Não inclui: Requisitos formais da queixa-crime, procuração com poderes especiais e aditamento pelo MP → 5474; Regras processuais da ação de iniciativa privada no CPP (arts. 29 a 38, indivisibilidade, intervenção do MP) → 5472; Renúncia e perdão do ofendido como causas de extinção da punibilidade (CP, art. 107, V) → 5196; Hipóteses de perempção do CPP, art. 60, como causa extintiva da punibilidade → 5195; Decadência como causa de extinção da punibilidade (CP, art. 107, IV) → 5198; Espécie de ação penal nos crimes contra a honra (CP, art. 145) → 5121
Âncoras legais: CP, art. 100, §§ 2º a 4º; CP, art. 103; CP, art. 104; CP, art. 105; CP, art. 106; CF, art. 5º, LIX
Desempate: Use este nó quando a questão tratar da ação privada, da queixa, da renúncia, do perdão ou da perempção como regras do CP (arts. 100 a 106). Se o foco for o procedimento do CPP, use 5472 ou 5474. Se for a extinção da punibilidade do art. 107, use os nós de Punibilidade.
```
Regra D2 (decisão manual): herdada de 5063: Penal: espécies de ação penal, representação, requisição, renúncia, perdão e perempção como regras do CP (arts. 100 a 106)

### 5064 · sobreposição (acao_penal)

```text
[5064] Penal > Ação Penal > Ação Penal Pública
Escopo: Ação penal pública pelas regras do Código Penal: regra geral da ação pública, titularidade do Ministério Público, ação condicionada à representação do ofendido ou à requisição do Ministro da Justiça, ação no crime complexo e irretratabilidade da representação após a denúncia (CP, arts. 100 a 103).
Inclui: Regra geral: ação penal pública, salvo declaração expressa da lei (CP, art. 100, caput); Titularidade do Ministério Público para a ação penal pública (CP, art. 100, § 1º; CF, art. 129, I); Ação pública condicionada à representação do ofendido: natureza de condição de procedibilidade; Ação pública condicionada à requisição do Ministro da Justiça; Ação penal no crime complexo (CP, art. 101); Retratação da representação até o oferecimento da denúncia (CP, art. 102); Prazo decadencial de seis meses para a representação (CP, art. 103)
Não inclui: Forma, destinatário e prazo processual da representação no CPP (art. 39) → 5471; Requisitos da denúncia e prazos para o oferecimento (CPP, arts. 41 e 46) → 5473; Princípios da obrigatoriedade, indisponibilidade e oficialidade da ação pública → 5469; Ação penal na lesão corporal em violência doméstica e audiência de renúncia à representação (Lei 11.340/2006, art. 16) → 4704; Ação penal nos crimes contra a dignidade sexual (CP, art. 225) → 5110; Ação privada subsidiária da pública pela inércia do MP → 5065
Âncoras legais: CP, art. 100, caput e § 1º; CP, art. 101; CP, art. 102; CP, art. 103; CF, art. 129, I
Desempate: Use este nó quando a questão tratar da ação pública, da representação ou da requisição como regras do CP (arts. 100 a 106). Se o foco for o procedimento do CPP (denúncia, forma e prazos processuais da representação), use os nós de Processo Penal > Ação Penal (5470, 5471, 5473).
```
Regra D2 (decisão manual): herdada de 5063: Penal: espécies de ação penal, representação, requisição, renúncia, perdão e perempção como regras do CP (arts. 100 a 106)

### 5198 · sobreposição (acao_penal)

```text
[5198] Penal > Punibilidade > Decadência
Escopo: Decadência como causa de extinção da punibilidade (CP, art. 107, IV): perda do direito de queixa ou de representação pelo não exercício no prazo legal, em regra de seis meses do conhecimento da autoria.
Inclui: Conceito e natureza da decadência como causa extintiva da punibilidade; Prazo decadencial de seis meses contado do dia em que o ofendido soube quem é o autor do crime (CP, art. 103); Incidência na ação penal privada e na pública condicionada à representação; Natureza de prazo penal, fatal e improrrogável, não sujeito a suspensão ou interrupção; Decadência na ação penal privada subsidiária da pública (não extingue a punibilidade); Distinção entre decadência, perempção, renúncia e perdão do ofendido
Não inclui: Procedimento e contagem do prazo para oferecimento da queixa-crime → 5472; Forma, destinatário e procedimento da representação do ofendido → 5471; Perempção por inércia do querelante já no curso da ação → 5195; Renúncia ao direito de queixa e perdão do ofendido → 5196; Prescrição da pretensão punitiva → 5188
Âncoras legais: CP, art. 103; CP, art. 107, IV; CPP, art. 38; Lei 9.099/1995, art. 91
Desempate: Use este nó para a decadência como causa de extinção da punibilidade (CP, art. 107, IV); questões sobre contagem de prazo e procedimento de queixa ou representação vão para Processo Penal (5472 ou 5471).
```
Regra D2 (decisão manual): Penal: decadência como causa de extinção da punibilidade (CP, art. 107, IV); contagem de prazo e procedimento vão para Processo Penal

### 5466 · sobreposição (acao_penal)

```text
[5466] Processo Penal > Ação Penal
Escopo: Ação penal sob a ótica do CPP: titularidade, espécies (pública incondicionada, condicionada, privada e subsidiária), condições da ação, princípios, denúncia, queixa e ação civil ex delicto. Todas as partes têm subtema próprio.
Inclui: Titularidade privativa do MP na ação pública (CF, art. 129, I); Representação do ofendido e requisição do Ministro da Justiça como condições de procedibilidade; Ação penal privada exclusiva, personalíssima e subsidiária da pública; Requisitos e prazos da denúncia e da queixa (CPP, arts. 41 e 46); Princípios da obrigatoriedade, indisponibilidade, oportunidade e indivisibilidade; Condições da ação penal e justa causa; Ação civil ex delicto e reparação do dano
Não inclui: Regras de ação penal previstas no Código Penal (CP, arts. 100 a 106) → 5063; Decadência como causa de extinção da punibilidade (CP, art. 107, IV) → 5198; Renúncia e perdão do ofendido como causas extintivas da punibilidade (CP, arts. 104 a 106) → 5196; Rejeição e recebimento da denúncia ou queixa (CPP, art. 395) → 5531; Arquivamento do inquérito policial → 5501; Acordo de não persecução penal → 5502
Âncoras legais: CF, art. 129, I; CF, art. 5º, LIX; CPP, arts. 24 a 62; CPP, art. 41; CPP, arts. 63 a 68
Desempate: Escolha este nó (ou seu subtema) quando a questão tratar de denúncia, queixa, prazos, requisitos, legitimidade ou condições da ação segundo o CPP (arts. 24 a 62); se tratar das regras do Código Penal sobre ação penal ou da extinção da punibilidade, use Penal > Ação Penal (5063) ou Punibilidade (5191).
```
Regra D2 (decisão manual): Processo Penal: denúncia, queixa, prazos, requisitos, legitimidade e condições da ação (CPP, arts. 24 a 62)

### 5475 · sobreposição (acao_penal)

```text
[5475] Processo Penal > Ação Penal > Ação Civil Ex Delicto
Escopo: Ação civil ex delicto: reparação do dano causado pelo crime no juízo cível. Abrange a execução da sentença penal condenatória, a ação civil de conhecimento, a relação entre a decisão penal e a decisão cível e a legitimidade do MP para propô-la (CPP, arts. 63 a 68).
Inclui: Execução no cível da sentença penal condenatória transitada em julgado como título executivo; Fixação de valor mínimo de indenização na sentença penal (CPP, art. 387, IV) e liquidação do restante; Ação civil de conhecimento proposta durante o processo penal e suspensão do processo cível; Sentenças absolutórias que fazem coisa julgada no cível (inexistência do fato, excludentes de ilicitude) e as que não fazem; Arquivamento do inquérito, extinção da punibilidade e atipicidade que não impedem a ação civil; Legitimidade do MP para a ação civil quando o titular é pobre (CPP, art. 68) e inconstitucionalidade progressiva
Não inclui: Obrigação de indenizar como efeito genérico da condenação previsto no CP, art. 91, I → 5209; Efeitos da sentença condenatória vistos sob o ângulo do CPP, inclusive a sentença em si → 5577; Sequestro, hipoteca legal e arresto para garantir a reparação → 5496; Requisitos e fundamentos da sentença absolutória (CPP, art. 386) → 5574
Âncoras legais: CPP, arts. 63 a 68; CPP, art. 387, IV; CPP, art. 386; CP, art. 91, I
Desempate: Escolha este nó quando a questão tratar de como a vítima obtém no cível a reparação do dano e da repercussão cível da decisão penal (CPP, arts. 63 a 68). Se tratar do efeito material de tornar certa a obrigação de indenizar (CP, art. 91), use 5209.
```
Regra D2 (decisão manual): herdada de 5466: Processo Penal: denúncia, queixa, prazos, requisitos, legitimidade e condições da ação (CPP, arts. 24 a 62)

### 5471 · sobreposição (acao_penal)

```text
[5471] Processo Penal > Ação Penal > Ação Penal Pública Condicionada
Escopo: Ação penal pública condicionada à representação do ofendido ou à requisição do Ministro da Justiça, no regime do CPP: titularidade do MP, forma, prazo e destinatários da representação, retratação e efeitos da requisição.
Inclui: Representação: natureza de condição de procedibilidade, ausência de formalidade e destinatários (juiz, MP, autoridade policial); Prazo decadencial de 6 meses para representar, contado do conhecimento da autoria; Retratação da representação até o oferecimento da denúncia (CPP, art. 25) e retratação da retratação; Representação por representante legal, curador especial e sucessores (CADI); Requisição do Ministro da Justiça: hipóteses, ausência de prazo decadencial e não vinculação do MP; Crimes condicionados por lei: lesão leve e culposa (Lei 9.099/1995, art. 88) e estelionato (CP, art. 171, § 5º); Eficácia objetiva da representação em relação aos coautores
Não inclui: Regra do CP sobre quando a ação depende de representação ou requisição (CP, art. 100, § 1º) → 5064; Decadência como causa de extinção da punibilidade (CP, arts. 103 e 107, IV) → 5198; Retratação da representação em audiência específica na Lei Maria da Penha (Lei 11.340/2006, art. 16) → 4704; Ação pública incondicionada, regra geral em que o MP age sem manifestação do ofendido → 5470; Natureza da representação como condição de procedibilidade, examinada em abstrato entre as condições da ação → 5467
Âncoras legais: CPP, art. 24; CPP, art. 25; CPP, art. 38; CPP, art. 39; Lei 9.099/1995, art. 88; CP, art. 171, § 5º
Desempate: Use este nó quando a questão tratar da representação ou requisição no regime processual (forma, prazo, retratação, legitimidade, CPP, arts. 24 a 39). Se tratar só da previsão do CP sobre a espécie de ação (CP, art. 100), use 5064.
```
Regra D2 (decisão manual): herdada de 5466: Processo Penal: denúncia, queixa, prazos, requisitos, legitimidade e condições da ação (CPP, arts. 24 a 62)

### 5470 · sobreposição (acao_penal)

```text
[5470] Processo Penal > Ação Penal > Ação Penal Pública Incondicionada
Escopo: Ação penal pública incondicionada no regime do CPP: regra geral da ação penal, promovida privativamente pelo MP mediante denúncia, sem depender de manifestação do ofendido ou de terceiros.
Inclui: Titularidade privativa do MP (CF, art. 129, I) e oferecimento de denúncia independentemente da vontade da vítima; Ação incondicionada como regra quando a lei silencia; Crimes de ação incondicionada cobrados em prova: crimes contra a dignidade sexual (CP, art. 225), lesão corporal em violência doméstica contra a mulher; Provocação do MP por qualquer pessoa (delatio criminis) nos crimes de ação pública; Ação incondicionada nos crimes praticados em detrimento de patrimônio ou interesse da União, Estado ou Município (CPP, art. 24, § 2º)
Não inclui: Previsão material do CP de que a ação é pública salvo disposição em contrário (CP, art. 100, caput) → 5064; Ação pública condicionada à representação ou requisição → 5471; Ação penal privada subsidiária da pública em caso de inércia do MP → 5472; Requisitos formais e prazo da denúncia → 5473; Princípios da obrigatoriedade e da indisponibilidade estudados em si → 5469
Âncoras legais: CF, art. 129, I; CPP, art. 24; CPP, art. 27; CP, art. 225; CP, art. 100
Desempate: Use este nó quando a questão perguntar se determinado crime é de ação pública incondicionada ou tratar da atuação do MP sem condição de procedibilidade no regime do CPP. Se a questão for sobre a regra do CP (art. 100), use 5064.
```
Regra D2 (decisão manual): herdada de 5466: Processo Penal: denúncia, queixa, prazos, requisitos, legitimidade e condições da ação (CPP, arts. 24 a 62)

### 5472 · sobreposição (acao_penal)

```text
[5472] Processo Penal > Ação Penal > Ação Penal de Iniciativa Privada
Escopo: Ação penal de iniciativa privada no regime do CPP: espécies (exclusiva, personalíssima e subsidiária da pública), legitimidade do ofendido e sucessores, princípios próprios e atuação do MP como fiscal ou interveniente.
Inclui: Ação privada exclusiva, personalíssima (CP, art. 236) e subsidiária da pública (CF, art. 5º, LIX; CPP, art. 29); Poderes do MP na ação subsidiária: aditar, repudiar a queixa, oferecer denúncia substitutiva e retomar a ação; Legitimidade do ofendido, do representante legal, do curador especial e sucessão processual (CADI, CPP, art. 31); Princípios da oportunidade, disponibilidade e indivisibilidade aplicados à ação privada; Renúncia, perdão e perempção como institutos processuais da ação privada (CPP, arts. 48 a 60); Prazo decadencial de 6 meses e sua contagem na ação subsidiária
Não inclui: Regra do CP sobre ação de iniciativa privada (CP, art. 100, §§ 2º a 4º) → 5065; Requisitos formais da peça, procuração com poderes especiais e aditamento da queixa → 5474; Perempção como causa de extinção da punibilidade → 5195; Renúncia e perdão do ofendido como causas extintivas da punibilidade (CP, arts. 104 a 106) → 5196; Decadência como causa de extinção da punibilidade → 5198
Âncoras legais: CF, art. 5º, LIX; CPP, art. 29; CPP, art. 30; CPP, art. 31; CPP, art. 38; CPP, arts. 48 a 60
Desempate: Use este nó para espécies, legitimidade e regime processual da ação privada (CPP, arts. 29 a 60); se a questão tratar da peça de queixa em si (requisitos, procuração, aditamento), use 5474; se tratar da regra do CP ou da extinção da punibilidade, use 5065 ou o nó de Punibilidade correspondente.
```
Regra D2 (decisão manual): herdada de 5466: Processo Penal: denúncia, queixa, prazos, requisitos, legitimidade e condições da ação (CPP, arts. 24 a 62)

### 5468 · sobreposição (acao_penal)

```text
[5468] Processo Penal > Ação Penal > Classificação da Ação Penal
Escopo: Classificação da ação penal no processo penal: critério subjetivo (titularidade) que divide em pública (incondicionada e condicionada) e de iniciativa privada (exclusiva, personalíssima, subsidiária), além de classificações doutrinárias como ação popular e secundária.
Inclui: Divisão da ação pela titularidade: pública e de iniciativa privada; Subespécies: pública incondicionada, condicionada à representação e à requisição; privada exclusiva, personalíssima e subsidiária; Como identificar a espécie de ação no tipo penal ou no capítulo ("somente se procede mediante..."); Ação penal secundária (mudança da espécie conforme circunstâncias, como no CP, art. 145, parágrafo único); Ação penal popular, adesiva e de ofício (procedimento judicialiforme) como classificações doutrinárias; Ação penal nos crimes complexos (CP, art. 101)
Não inclui: Regime detalhado da representação e da requisição → 5471; Regime detalhado da ação privada e da ação subsidiária → 5472; Classificação da ação penal pela ótica do Código Penal (CP, art. 100) → 5063; Características e condições da ação penal → 5467
Âncoras legais: CPP, art. 24; CPP, art. 29; CPP, art. 30; CP, art. 100; CP, art. 101
Desempate: Use este nó quando a questão pedir o quadro geral das espécies de ação ou comparar várias espécies entre si no CPP. Se tratar das regras de uma espécie só, use 5470, 5471 ou 5472. Se a questão estiver centrada no CP, art. 100, use 5063.
```
Regra D2 (decisão manual): herdada de 5466: Processo Penal: denúncia, queixa, prazos, requisitos, legitimidade e condições da ação (CPP, arts. 24 a 62)

### 5473 · sobreposição (acao_penal)

```text
[5473] Processo Penal > Ação Penal > Denúncia
Escopo: Denúncia como peça inicial da ação penal pública: requisitos formais, prazos de oferecimento, rol de testemunhas, denúncia genérica e alternativa, aditamento e dispensa do inquérito.
Inclui: Requisitos da denúncia (CPP, art. 41): exposição do fato e circunstâncias, qualificação do acusado, classificação do crime e rol de testemunhas; Prazo de 5 dias para réu preso e 15 dias para réu solto (CPP, art. 46) e consequência do descumprimento; Dispensa do inquérito quando houver elementos suficientes (CPP, art. 39, § 5º, e art. 46, § 1º); Denúncia genérica nos crimes societários e inépcia da peça; Denúncia alternativa e aditamento da denúncia; Prazos especiais de denúncia em leis específicas (ex.: Lei de Drogas)
Não inclui: Rejeição e recebimento da denúncia (CPP, art. 395 e 396) → 5531; Aditamento após mutatio libelli na fase de sentença (CPP, art. 384) → 5579; Requisitos e procuração da queixa-crime → 5474; Arquivamento do inquérito em vez do oferecimento da denúncia → 5501; Acordo de não persecução penal como alternativa à denúncia → 5502
Âncoras legais: CPP, art. 41; CPP, art. 46; CPP, art. 39, § 5º; CF, art. 129, I
Desempate: Use este nó para o conteúdo, a forma e o prazo da denúncia. Se a questão tratar do juízo de admissibilidade da peça (rejeição ou recebimento), use 5531.
```
Regra D2 (decisão manual): herdada de 5466: Processo Penal: denúncia, queixa, prazos, requisitos, legitimidade e condições da ação (CPP, arts. 24 a 62)

### 5469 · sobreposição (acao_penal)

```text
[5469] Processo Penal > Ação Penal > Princípios da Ação Penal
Escopo: Princípios específicos da ação penal: obrigatoriedade, indisponibilidade, oficialidade, oficiosidade, autoritariedade e divisibilidade na ação pública; oportunidade, disponibilidade e indivisibilidade na ação privada; intranscendência para ambas.
Inclui: Obrigatoriedade (legalidade processual) e mitigação por transação penal, ANPP e colaboração premiada (discricionariedade regrada); Indisponibilidade: o MP não pode desistir da ação nem do recurso (CPP, arts. 42 e 576); Oportunidade e disponibilidade na ação privada; Indivisibilidade da ação privada (CPP, art. 48) e a polêmica sobre (in)divisibilidade da ação pública; Intranscendência (pessoalidade) da ação penal; Oficialidade, oficiosidade e autoritariedade
Não inclui: Princípios gerais do processo penal (contraditório, ampla defesa, presunção de inocência) → 5582; Requisitos e cabimento da transação penal → 5541; Requisitos e cabimento do acordo de não persecução penal → 5502; Princípios do direito penal material (legalidade, intervenção mínima) → 5172; Efeitos da renúncia e do perdão sobre os coautores na ação privada → 5472
Âncoras legais: CPP, art. 42; CPP, art. 48; CPP, art. 49; CPP, art. 51; CPP, art. 576
Desempate: Use este nó quando a questão perguntar qual princípio rege a ação penal ou como ele se aplica. Se tratar de princípios gerais do processo penal, use 5582. Se tratar dos requisitos de um instituto despenalizador, use o nó desse instituto.
```
Regra D2 (decisão manual): herdada de 5466: Processo Penal: denúncia, queixa, prazos, requisitos, legitimidade e condições da ação (CPP, arts. 24 a 62)

### 5474 · sobreposição (acao_penal)

```text
[5474] Processo Penal > Ação Penal > Queixa Crime
Escopo: Queixa-crime como peça inicial da ação penal de iniciativa privada: requisitos formais, procuração com poderes especiais, prazo decadencial, aditamento pelo MP e inclusão de todos os autores.
Inclui: Requisitos da queixa (CPP, art. 41) e capacidade postulatória; Procuração com poderes especiais e menção ao fato criminoso (CPP, art. 44); Aditamento da queixa pelo MP em 3 dias (CPP, arts. 45 e 46, § 2º); Oferecimento da queixa contra todos os autores e consequências da omissão (renúncia tácita); Prazo de 6 meses para oferecer a queixa; Queixa subsidiária na inércia do MP (forma da peça)
Não inclui: Espécies, legitimidade e regime geral da ação privada → 5472; Requisitos e prazo da denúncia → 5473; Rejeição e recebimento da queixa → 5531; Queixa e ação privada segundo o Código Penal (CP, art. 100, § 2º) → 5065; Decadência do direito de queixa como extinção da punibilidade → 5198
Âncoras legais: CPP, art. 41; CPP, art. 44; CPP, art. 45; CPP, art. 46, § 2º; CPP, art. 38
Desempate: Use este nó quando a questão tratar da peça de queixa (requisitos, procuração, aditamento, prazo). Se tratar das espécies de ação privada ou da legitimidade e dos princípios dela, use 5472.
```
Regra D2 (decisão manual): herdada de 5466: Processo Penal: denúncia, queixa, prazos, requisitos, legitimidade e condições da ação (CPP, arts. 24 a 62)

### 5537 · sobreposição (sentenca)

```text
[5537] Processo Penal > Procedimento Ordinário > Sentença
Escopo: Sentença como ato final do procedimento ordinário: momento (em audiência ou após memoriais), prazo para prolação e estrutura formal (relatório, fundamentação e dispositivo).
Inclui: Sentença proferida em audiência após os debates (CPP, art. 403); Prazo de 10 dias após memoriais (CPP, art. 403, § 3º, e art. 404, parágrafo único); Requisitos formais da sentença (CPP, art. 381); Dever de motivação (CF, art. 93, IX); Pedido de esclarecimento ao juiz por obscuridade, ambiguidade ou contradição (CPP, art. 382); Correção de erro material e publicação da sentença
Não inclui: Emendatio libelli e mutatio libelli (CPP, arts. 383 e 384) → 5579; Fundamentos da sentença absolutória (CPP, art. 386) → 5574; Conteúdo da sentença condenatória (CPP, art. 387) → 5575; Fixação da pena e do regime na sentença → 5576; Efeitos da sentença condenatória → 5577; Sentença no Tribunal do Júri → 5529
Âncoras legais: CPP, art. 381; CPP, art. 382; CPP, art. 403; CPP, art. 404; CF, art. 93, IX
Desempate: Use este nó para a sentença como ato final do rito ordinário (momento, prazo, estrutura); questões sobre conteúdo absolutório ou condenatório, correlação, emendatio/mutatio, pena ou efeitos vão para os subtemas de Sentença Penal (5572).
```
Regra D2 (decisão manual): Procedimento Ordinário > Sentença: a sentença como ato final do rito ordinário (momento, prazo, estrutura)

### 5539 · sobreposição (juizados)

```text
[5539] Processo Penal > Procedimento Sumaríssimo
Escopo: Procedimento sumaríssimo dos Juizados Especiais Criminais (Lei 9.099/1995) para infrações de menor potencial ofensivo: fase preliminar, composição civil, rito em audiência única, competência, transação penal e suspensão condicional do processo (estes três com subtema próprio).
Inclui: Termo circunstanciado e fase preliminar; Composição civil dos danos e seus efeitos sobre a representação; Denúncia oral e audiência de instrução e julgamento em ato único; Critérios orientadores: oralidade, informalidade, economia processual e celeridade; Hipóteses de remessa ao juízo comum (citação por edital, complexidade); Visão de conjunto do rito sumaríssimo
Não inclui: Conceito de infração de menor potencial ofensivo e competência do JECrim → 5540; Requisitos e efeitos da transação penal → 5541; Suspensão condicional do processo (art. 89 da Lei 9.099/1995) → 5542; Apelação e embargos no âmbito dos Juizados Especiais → 5569; Rito sumário do CPP (crimes com pena máxima inferior a 4 anos) → 5538
Âncoras legais: Lei 9.099/1995, arts. 60 a 92; CF, art. 98, I; CPP, art. 538
Desempate: Questões sobre o rito, a competência, a transação penal e a suspensão condicional do processo dos Juizados ficam em Processo Penal (este nó ou seus subtemas), e não no nó de Legislação Especial Juizado Especial Criminal (4701); use este nó quando a questão tratar do rito sumaríssimo em geral ou de mais de um desses institutos ao mesmo tempo.
```
Regra D2 (decisão manual): Processo Penal: o procedimento sumaríssimo (rito, competência, transação penal, suspensão condicional do processo)

### 5540 · sobreposição (juizados)

```text
[5540] Processo Penal > Procedimento Sumaríssimo > Competência dos Juizados Especiais Criminais
Escopo: Competência dos Juizados Especiais Criminais para infrações de menor potencial ofensivo: conceito de IMPO, competência territorial, conexão e continência com o juízo comum e hipóteses de remessa ao juízo comum. Como o rito sumaríssimo não tem subtema próprio, as questões sobre ele também ficam aqui.
Inclui: Conceito de infração de menor potencial ofensivo: contravenções e crimes com pena máxima até 2 anos, cumulada ou não com multa; Competência territorial pelo lugar em que foi praticada a infração (art. 63); Conexão e continência com crime de competência do juízo comum, com aplicação da transação e da composição civil no juízo comum; Remessa ao juízo comum quando o autor não é encontrado para citação pessoal ou quando a causa é complexa; Exclusão da Lei 9.099/95 na violência doméstica contra a mulher (art. 41 da Lei 11.340/2006) e na Justiça Militar; Rito sumaríssimo: termo circunstanciado, audiência preliminar, denúncia oral, audiência de instrução e julgamento
Não inclui: Requisitos, cabimento e efeitos da transação penal → 5541; Requisitos, período de prova e revogação da suspensão condicional do processo → 5542; Apelação, embargos e turma recursal nos Juizados → 5569; Regras gerais de competência territorial e de conexão do CPP fora dos Juizados → 5483; Institutos da Lei Maria da Penha em si, como medidas protetivas → 4704
Âncoras legais: CF, art. 98, I; Lei 9.099/95, arts. 60 a 63; Lei 9.099/95, art. 66, parágrafo único; Lei 9.099/95, arts. 69 e 77 a 83; Lei 9.099/95, art. 90-A; Lei 11.340/2006, art. 41
Desempate: Questões processuais sobre o procedimento sumaríssimo (rito, competência, transação penal, suspensão condicional do processo) ficam em Processo Penal. Use este nó quando se tratar de competência do JECrim, do conceito de IMPO ou do rito em si, e não de transação (5541) ou de sursis processual (5542). Use 4701 apenas quando a questão tratar da Lei 9.099/95 por outro ângulo que não seja processual.
```
Regra D2 (decisão manual): herdada de 5539: Processo Penal: o procedimento sumaríssimo (rito, competência, transação penal, suspensão condicional do processo)

### 5542 · sobreposição (juizados)

```text
[5542] Processo Penal > Procedimento Sumaríssimo > Suspensão Condicional do Processo
Escopo: Suspensão condicional do processo (sursis processual, art. 89 da Lei 9.099/95): cabimento em crimes com pena mínima de até 1 ano, requisitos, proposta pelo MP, condições, período de prova, revogação e extinção da punibilidade.
Inclui: Cabimento: crime com pena mínima cominada igual ou inferior a 1 ano, mesmo fora dos Juizados; Requisitos: não estar sendo processado nem ter sido condenado por outro crime e presença dos requisitos do sursis penal (art. 77 do CP); Condições obrigatórias e facultativas e período de prova de 2 a 4 anos; Revogação obrigatória e facultativa; prescrição não corre durante a suspensão; Recusa do MP e aplicação do art. 28 do CPP (Súmula 696 do STF); Concurso de crimes e crime continuado no cálculo da pena mínima (Súmula 723 do STF e Súmula 243 do STJ); Desclassificação ou procedência parcial (Súmula 337 do STJ); vedação na Lei Maria da Penha (Súmula 536 do STJ)
Não inclui: Suspensão condicional da pena (sursis do art. 77 do CP) → 5207; Transação penal (art. 76 da Lei 9.099/95) → 5541; Acordo de não persecução penal (art. 28-A do CPP) → 5502; Conceito de infração de menor potencial ofensivo e competência do JECrim → 5540
Âncoras legais: Lei 9.099/95, art. 89; Lei 9.099/95, art. 90-A; CP, art. 77; Lei 11.340/2006, art. 41
Desempate: Questões processuais sobre o procedimento sumaríssimo (rito, competência, transação penal, suspensão condicional do processo) ficam em Processo Penal. Use este nó sempre que a questão tratar da suspensão do processo já com denúncia oferecida (art. 89), com pena mínima de até 1 ano. Se a questão tratar da suspensão da pena após a condenação, use 5207.
```
Regra D2 (decisão manual): herdada de 5539: Processo Penal: o procedimento sumaríssimo (rito, competência, transação penal, suspensão condicional do processo)

### 5541 · sobreposição (juizados)

```text
[5541] Processo Penal > Procedimento Sumaríssimo > Transação Penal
Escopo: Transação penal (art. 76 da Lei 9.099/95): proposta do MP de aplicação imediata de pena restritiva de direitos ou de multa nas infrações de menor potencial ofensivo, antes da denúncia, com seus requisitos, impedimentos, homologação e efeitos.
Inclui: Cabimento nas infrações de menor potencial ofensivo, na ação pública e, segundo a jurisprudência, na privada; Impedimentos: condenação anterior à pena privativa de liberdade por sentença definitiva, benefício recebido nos últimos 5 anos e antecedentes desfavoráveis; Natureza da sentença homologatória e efeitos: não gera reincidência nem consta de certidão de antecedentes; Descumprimento das condições e retomada da persecução penal (Súmula Vinculante 35); Recusa do MP em oferecer a proposta e redução da multa pela metade; Recurso contra a sentença homologatória (apelação, art. 76, § 5º)
Não inclui: Suspensão condicional do processo (art. 89 da Lei 9.099/95) → 5542; Acordo de não persecução penal (art. 28-A do CPP) → 5502; Conceito de IMPO, competência do JECrim e rito sumaríssimo → 5540; Processamento da apelação na turma recursal → 5569
Âncoras legais: Lei 9.099/95, art. 76; Lei 9.099/95, art. 61; Lei 11.340/2006, art. 41
Desempate: Questões processuais sobre o procedimento sumaríssimo (rito, competência, transação penal, suspensão condicional do processo) ficam em Processo Penal. Use este nó quando a questão tratar do acordo pré-processual do art. 76, feito antes da denúncia. Se tratar da suspensão do processo após a denúncia, use 5542; se tratar do ANPP, use 5502.
```
Regra D2 (decisão manual): herdada de 5539: Processo Penal: o procedimento sumaríssimo (rito, competência, transação penal, suspensão condicional do processo)

### 5558 · sobreposição (orcrim_meios_prova)

```text
[5558] Processo Penal > Provas em Espécies > Ação Controlada
Escopo: Ação controlada como meio de obtenção de prova: retardamento da intervenção policial ou administrativa para agir no momento mais eficaz à formação de provas, com seus requisitos, comunicação ao juiz e limites.
Inclui: Conceito de ação controlada e flagrante diferido ou prorrogado; Comunicação prévia ao juiz competente e sigilo da comunicação na Lei 12.850/2013; Ação controlada na Lei de Drogas, com autorização judicial e oitiva do MP; Ação controlada transnacional e cooperação de autoridades estrangeiras; Diferença entre ação controlada e flagrante preparado ou esperado; Auto circunstanciado ao término da diligência
Não inclui: Crime de organização criminosa e aspectos penais da Lei 12.850/2013 → 4705; Infiltração de agentes policiais → 5559; Espécies de flagrante (próprio, impróprio, preparado, esperado) e lavratura do auto → 5518; Crimes e tipos penais da Lei de Drogas → 4708
Âncoras legais: Lei 12.850/2013, arts. 8º e 9º; Lei 12.850/2013, art. 3º, III; Lei 11.343/2006, art. 53, II
Desempate: Questões sobre ação controlada como meio de obtenção de prova (requisitos, comunicação ao juiz, retardamento do flagrante) ficam aqui; questões sobre a Lei de Organizações Criminosas em si, sobretudo os tipos penais, vão para 4705.
```
Regra D2 (decisão manual): Processo Penal: ação controlada como meio de obtenção de prova

### 5557 · sobreposição (orcrim_meios_prova)

```text
[5557] Processo Penal > Provas em Espécies > Colaboração Premiada
Escopo: Colaboração premiada como meio de obtenção de prova: natureza de negócio jurídico processual, legitimidade, negociação, homologação judicial, resultados exigidos, prêmios, direitos do colaborador e valor probatório das declarações.
Inclui: Natureza jurídica: negócio jurídico processual e meio de obtenção de prova; Resultados exigidos (identificação de coautores, estrutura, prevenção de infrações, recuperação de produto, localização de vítima); Legitimidade do delegado e do MP para celebrar o acordo; Homologação judicial: regularidade, legalidade e voluntariedade; Benefícios: perdão judicial, redução e substituição da pena, não oferecimento de denúncia; Vedação de sentença ou medidas cautelares fundadas apenas nas declarações do colaborador; Direitos do colaborador, sigilo e retratação da proposta; Delação na Lei de Drogas e na Lei de Lavagem como meio de prova
Não inclui: Crime de organização criminosa e tipos penais da Lei 12.850/2013 → 4705; Acordo de não persecução penal → 5502; Perdão judicial como causa extintiva da punibilidade do CP → 5197; Confissão do acusado como meio de prova → 5548; Infiltração de agentes e ação controlada → 5559
Âncoras legais: Lei 12.850/2013, arts. 3º-A a 7º; Lei 12.850/2013, art. 3º, I; Lei 11.343/2006, art. 41; Lei 9.613/1998, art. 1º, § 5º
Desempate: Questões sobre a colaboração premiada como meio de obtenção de prova (acordo, homologação, requisitos, valor probatório, direitos do colaborador) ficam aqui; questões sobre a Lei de Organizações Criminosas em si, sobretudo seus tipos penais, vão para 4705.
```
Regra D2 (decisão manual): Processo Penal: colaboração premiada como meio de obtenção de prova

### 5559 · sobreposição (orcrim_meios_prova)

```text
[5559] Processo Penal > Provas em Espécies > Infiltração de Agentes
Escopo: Infiltração de agentes como meio de obtenção de prova: requisitos, autorização judicial, prazo, infiltração virtual, direitos e responsabilidade do agente infiltrado e relatório circunstanciado.
Inclui: Requisitos: autorização judicial, indícios de organização criminosa e subsidiariedade da medida; Prazo de até 6 meses e renovações; Infiltração virtual de agentes (Lei 12.850/2013 e ECA); Direitos do agente: recusar ou cessar a infiltração, preservação de identidade; Proporcionalidade e responsabilidade penal do agente infiltrado; Diferença entre agente infiltrado e agente provocador; Relatório circunstanciado e sigilo do pedido
Não inclui: Crime de organização criminosa e tipos penais da Lei 12.850/2013 → 4705; Ação controlada → 5558; Colaboração premiada → 5557; Flagrante preparado e crime impossível → 5518; Crimes contra criança e adolescente no ECA → 4709
Âncoras legais: Lei 12.850/2013, arts. 10 a 14; Lei 12.850/2013, arts. 10-A a 10-D; Lei 11.343/2006, art. 53, I; Lei 8.069/1990, arts. 190-A a 190-E
Desempate: Questões sobre a infiltração de agentes como meio de obtenção de prova (requisitos, prazo, autorização, atuação do agente) ficam aqui; questões sobre a Lei de Organizações Criminosas em si, sobretudo os tipos penais, vão para 4705.
```
Regra D2 (decisão manual): Processo Penal: infiltração de agentes como meio de obtenção de prova

### 5555 · sobreposição (interceptacao)

```text
[5555] Processo Penal > Provas em Espécies > Interceptação Telefônica e Quebra do Sigilo de Dados Telefônicos
Escopo: Interceptação telefônica e telemática e quebra de sigilo de dados telefônicos como meio de prova: requisitos, autorização judicial, prazo, transcrição, licitude, prova emprestada e encontro fortuito de provas.
Inclui: Requisitos: indícios de autoria, prova não obtível por outros meios, crime punido com reclusão; Legitimidade para requerer e decretação de ofício; Prazo de 15 dias e sucessivas renovações; Diferença entre interceptação, escuta e gravação telefônica clandestina; Quebra de sigilo de dados e registros telefônicos; Encontro fortuito de provas (serendipidade); Uso da interceptação como prova emprestada em outro processo ou no processo administrativo; Transcrição integral ou parcial e incidente de inutilização
Não inclui: Aspectos da Lei 9.296/1996 tratados como legislação especial em si, como o tipo penal do art. 10 → 4700; Captação ambiental → 5556; Teoria da prova emprestada em geral → 5593; Prova ilícita e derivação em geral → 5594
Âncoras legais: CF, art. 5º, XII; Lei 9.296/1996, arts. 1º a 9º
Desempate: Questões sobre interceptação e quebra de sigilo como meio de prova (licitude, prova emprestada, encontro fortuito) ficam aqui; questões sobre a Lei 9.296/1996 em si como legislação especial, como seu tipo penal, vão para 4700.
```
Regra D2 (decisão manual): Processo Penal: interceptação e quebra de sigilo como meio de prova (licitude, prova emprestada, encontro fortuito)

### 5572 · sobreposição (sentenca)

```text
[5572] Processo Penal > Sentença Penal
Escopo: Sentença penal sob a ótica processual: classificação dos provimentos, requisitos, sentença absolutória e condenatória, fixação da pena e do regime na sentença, correlação entre acusação e sentença, emendatio e mutatio libelli e efeitos processuais da condenação (com subtemas próprios).
Inclui: Requisitos formais da sentença (CPP, art. 381); Hipóteses de absolvição do art. 386 do CPP; Conteúdo da sentença condenatória (art. 387), inclusive valor mínimo de reparação; Emendatio libelli (art. 383) e mutatio libelli (art. 384); Princípio da correlação ou congruência; Publicação e intimação da sentença
Não inclui: Sentença proferida no plenário do júri → 5529; Prazo e momento da sentença na audiência do rito ordinário → 5537; Critérios materiais de dosimetria da pena (circunstâncias judiciais) → 5202; Efeitos extrapenais específicos da condenação previstos no CP, art. 92 → 5209; Ação civil ex delicto e execução civil da sentença → 5475
Âncoras legais: CPP, arts. 381 a 393; CPP, arts. 383 e 384; CPP, art. 386; CPP, art. 387
Desempate: Questões sobre classificação dos provimentos, efeitos, correlação, emendatio e mutatio libelli e sentença absolutória ou condenatória ficam em Processo Penal > Sentença Penal (este nó ou seus subtemas), e não em Sentença do rito ordinário (5537) nem nos nós de Teoria da Pena; use este nó genérico quando a questão abranger mais de um desses aspectos.
```
Regra D2 (decisão manual): Processo Penal > Sentença Penal: classificação, efeitos, correlação, emendatio e mutatio libelli, absolutória e condenatória

### 5573 · sobreposição (sentenca)

```text
[5573] Processo Penal > Sentença Penal > Classificação dos Provimentos Judiciais
Escopo: Classificação dos atos do juiz no processo penal (despachos, decisões interlocutórias simples e mistas, decisões definitivas e sentenças) e as espécies doutrinárias de sentença, além do conceito e dos requisitos formais da sentença penal.
Inclui: Despachos de mero expediente x decisões interlocutórias simples e mistas (terminativas e não terminativas); Decisões definitivas ou terminativas de mérito (ex.: extinção da punibilidade) x sentenças em sentido estrito; Sentença absolutória própria e imprópria, condenatória e terminativa de mérito como classificação; Sentença subjetivamente simples, plúrima e complexa; sentença suicida, vazia e autofágica; Requisitos formais da sentença: relatório, fundamentação e dispositivo (CPP, art. 381)
Não inclui: Hipóteses de absolvição do art. 386 do CPP e seus efeitos → 5574; Conteúdo obrigatório da sentença condenatória (art. 387 do CPP) → 5575; Prolação da sentença no rito ordinário (prazo, sentença em audiência) → 5537; Embargos de declaração contra a sentença (art. 382 do CPP) → 5565; Sentença proferida pelo juiz-presidente no Tribunal do Júri → 5529
Âncoras legais: CPP, art. 381; CPP, art. 800; CF, art. 93, IX
Desempate: Herdando a regra de 5572, use este nó quando a questão tratar da natureza ou espécie do provimento judicial ou dos requisitos formais da sentença em geral; se tratar do conteúdo ou dos efeitos de uma sentença absolutória ou condenatória específica, use 5574 ou 5575.
```
Regra D2 (decisão manual): herdada de 5572: Processo Penal > Sentença Penal: classificação, efeitos, correlação, emendatio e mutatio libelli, absolutória e condenatória

### 5577 · sobreposição (sentenca)

```text
[5577] Processo Penal > Sentença Penal > Efeitos Decorrentes da Sentença Penal Condenatória
Escopo: Efeitos processuais e civis da sentença penal condenatória no CPP: fixação do valor mínimo de reparação, formação de título executivo, coisa julgada e execução provisória da pena. Os efeitos materiais previstos no CP (arts. 91 e 92) ficam em Teoria da Pena.
Inclui: Fixação de valor mínimo para reparação dos danos (CPP, art. 387, IV), com exigência de pedido expresso e contraditório; Sentença condenatória transitada em julgado como título executivo judicial (CPP, art. 63); Execução civil do valor mínimo sem prejuízo da liquidação do dano efetivo (CPP, art. 63, parágrafo único); Execução provisória da pena e presunção de inocência (CF, art. 5º, LVII; execução imediata no Júri, CPP, art. 492, I, e); Revogação do lançamento do nome do réu no rol dos culpados e da prisão como efeito automático da sentença
Não inclui: Efeitos genéricos e específicos da condenação do CP (confisco, perda de cargo, incapacidade para dirigir) → 5209; Ação civil ex delicto e repercussão da absolvição no cível → 5475; Fixação da pena e do regime inicial na sentença → 5576; Efeitos da sentença absolutória (soltura, cessação de cautelares) → 5574; Reabilitação criminal → 5210
Âncoras legais: CPP, art. 387, IV; CPP, art. 63; CPP, art. 492, I, e; CF, art. 5º, LVII; CP, art. 91, I
Desempate: Herdando a regra de 5572, use este nó quando a questão tratar das consequências processuais ou civis da condenação; se tratar dos efeitos penais e extrapenais previstos nos arts. 91 e 92 do CP, use 5209.
```
Regra D2 (decisão manual): herdada de 5572: Processo Penal > Sentença Penal: classificação, efeitos, correlação, emendatio e mutatio libelli, absolutória e condenatória

### 5579 · sobreposição (sentenca)

```text
[5579] Processo Penal > Sentença Penal > Emendatio Libelli e Mutatio Libelli
Escopo: Mecanismos de adequação entre imputação e sentença: emendatio libelli (nova definição jurídica do mesmo fato, art. 383 do CPP) e mutatio libelli (nova definição jurídica por elemento ou circunstância não contida na acusação, com aditamento do MP, art. 384 do CPP).
Inclui: Emendatio libelli: o juiz atribui definição jurídica diversa sem alterar os fatos, ainda que a pena seja mais grave; Emendatio e proposta de suspensão condicional do processo ou remessa ao juízo competente (CPP, art. 383, §§ 1º e 2º); Mutatio libelli: aditamento pelo MP em 5 dias, defesa, até 3 testemunhas, novo interrogatório (CPP, art. 384); Aplicação do art. 28 do CPP se o MP não aditar; adstrição do juiz aos termos do aditamento; Inaplicabilidade da mutatio em segunda instância (Súmula 453 do STF) e possibilidade de emendatio em recurso, sem reformatio in pejus; Desclassificação e procedência parcial com cabimento de sursis processual (Súmula 337 do STJ)
Não inclui: Princípio da correlação em abstrato e vedação de sentença extra, ultra ou citra petita → 5578; Desclassificação na primeira fase do Júri (CPP, art. 419) → 5527; Requisitos e procedimento da suspensão condicional do processo → 5542; Vedação da reformatio in pejus como princípio recursal → 5513
Âncoras legais: CPP, art. 383; CPP, art. 384; CPP, art. 28; Súmula 453 do STF; Súmula 337 do STJ
Desempate: Herdando a regra de 5572, use este nó sempre que a questão envolver o procedimento ou os requisitos dos arts. 383 e 384 do CPP; se ela tratar apenas da regra de congruência entre fato imputado e sentença, sem esses institutos, use 5578.
```
Regra D2 (decisão manual): herdada de 5572: Processo Penal > Sentença Penal: classificação, efeitos, correlação, emendatio e mutatio libelli, absolutória e condenatória

### 5576 · sobreposição (sentenca)

```text
[5576] Processo Penal > Sentença Penal > Fixação da Pena e do Regime Penitenciário
Escopo: Atividade do juiz, na sentença condenatória, de fixar a pena e o regime inicial (CPP, art. 387, I a III e § 2º), incluindo a detração para fins de regime e a fundamentação do regime mais gravoso. As regras materiais de dosimetria e dos regimes ficam em Teoria da Pena.
Inclui: Dever de considerar agravantes e atenuantes e circunstâncias dos arts. 59 e 60 do CP ao condenar (CPP, art. 387, I a III); Detração na sentença para determinação do regime inicial (CPP, art. 387, § 2º); Fundamentação idônea para regime mais severo que o permitido pela pena (Súmulas 718 e 719 do STF; Súmula 440 do STJ); Fixação do regime inicial e da substituição da pena na própria sentença; Vício de fundamentação na dosimetria como fundamento de nulidade da sentença
Não inclui: Circunstâncias judiciais do art. 59 do CP (primeira fase) → 5202; Agravantes e atenuantes em espécie (segunda fase) → 5203; Causas de aumento e diminuição (terceira fase) → 5204; Regras materiais dos regimes fechado, semiaberto e aberto (CP, art. 33) → 5201; Requisitos das penas restritivas de direitos (CP, art. 44) → 5205; Progressão de regime na execução → 4703
Âncoras legais: CPP, art. 387, I, II e III; CPP, art. 387, § 2º; CP, art. 33; CP, art. 68; Súmula 718 do STF; Súmula 719 do STF; Súmula 440 do STJ
Desempate: Herdando a regra de 5572, use este nó quando a questão tratar da fixação da pena ou do regime como ato da sentença (art. 387 do CPP, detração para regime, fundamentação); se ela versar sobre as regras materiais do CP de cada fase da dosimetria ou dos regimes, use os nós de Teoria da Pena (5201 a 5205).
```
Regra D2 (decisão manual): herdada de 5572: Processo Penal > Sentença Penal: classificação, efeitos, correlação, emendatio e mutatio libelli, absolutória e condenatória

### 5578 · sobreposição (sentenca)

```text
[5578] Processo Penal > Sentença Penal > Princípio da Correlação entre Acusação e Sentença
Escopo: Princípio da correlação ou congruência entre a acusação e a sentença: o réu se defende dos fatos imputados e o juiz não pode julgar fora, além ou aquém deles. Também abrange os limites do art. 385 do CPP.
Inclui: O réu se defende dos fatos narrados, não da capitulação jurídica; Vedação de sentença extra petita, ultra petita e citra petita; Nulidade da sentença que condena por fato não descrito na denúncia ou queixa; Condenação mesmo com pedido de absolvição do MP e reconhecimento de agravantes não alegadas (CPP, art. 385); Correlação como decorrência do sistema acusatório, do contraditório e da ampla defesa
Não inclui: Procedimento da emendatio e da mutatio libelli (arts. 383 e 384 do CPP) → 5579; Sistema acusatório em abstrato → 5581; Requisitos da denúncia (descrição do fato, art. 41 do CPP) → 5473; Nulidades em espécie e regime das nulidades → 5511
Âncoras legais: CPP, art. 385; CPP, art. 41; CF, art. 5º, LV
Desempate: Herdando a regra de 5572, use este nó para o princípio da congruência e o art. 385 do CPP; se a questão cobrar o mecanismo de redefinição jurídica dos arts. 383 ou 384, use 5579.
```
Regra D2 (decisão manual): herdada de 5572: Processo Penal > Sentença Penal: classificação, efeitos, correlação, emendatio e mutatio libelli, absolutória e condenatória

### 5574 · sobreposição (sentenca)

```text
[5574] Processo Penal > Sentença Penal > Sentença Absolutória
Escopo: Sentença que julga improcedente a pretensão punitiva: hipóteses de absolvição do art. 386 do CPP, absolvição própria e imprópria e providências e efeitos do dispositivo absolutório.
Inclui: Fundamentos da absolvição: inexistência do fato, falta de prova, atipicidade, excludentes, falta de provas para condenar (CPP, art. 386, I a VII); In dubio pro reo como fundamento da absolvição; Absolvição imprópria com aplicação de medida de segurança (CPP, art. 386, parágrafo único, III); Soltura do réu e cessação das medidas cautelares (CPP, art. 386, parágrafo único, I e II); Interesse da defesa em recorrer para mudar o fundamento da absolvição
Não inclui: Absolvição sumária no procedimento comum (CPP, art. 397) → 5534; Absolvição sumária no Júri (CPP, art. 415) → 5527; Efeitos civis da absolvição e ação civil ex delicto (CPP, arts. 65 a 67) → 5475; Regras materiais da medida de segurança → 5184; Classificação doutrinária das sentenças em geral → 5573
Âncoras legais: CPP, art. 386
Desempate: Herdando a regra de 5572, use este nó para o conteúdo e os efeitos penais da sentença absolutória de mérito proferida ao final da instrução; absolvições sumárias vão para 5534 ou 5527.
```
Regra D2 (decisão manual): herdada de 5572: Processo Penal > Sentença Penal: classificação, efeitos, correlação, emendatio e mutatio libelli, absolutória e condenatória

### 5575 · sobreposição (sentenca)

```text
[5575] Processo Penal > Sentença Penal > Sentença Condenatória
Escopo: Sentença que julga procedente a pretensão punitiva: conteúdo obrigatório (CPP, art. 387), fundamentação, decisão sobre a prisão ou as cautelares, publicação e intimação da condenação. A dosimetria, os efeitos e a correlação têm nós irmãos próprios.
Inclui: Conteúdo da sentença condenatória (CPP, art. 387); Decisão fundamentada sobre manutenção ou decretação de preventiva ou outra cautelar (CPP, art. 387, § 1º); Publicação da sentença e registro (CPP, arts. 389 e 390); Intimação da sentença condenatória ao réu e ao defensor (CPP, art. 392); Dever de fundamentação da condenação (CF, art. 93, IX)
Não inclui: Fixação da pena, detração e regime inicial na sentença → 5576; Valor mínimo de reparação e demais efeitos da condenação → 5577; Condenação apesar de pedido de absolvição do MP (CPP, art. 385) → 5578; Requisitos e hipóteses da prisão preventiva → 5519; Sentença condenatória no Júri (CPP, art. 492) → 5529
Âncoras legais: CPP, art. 387; CPP, art. 389; CPP, art. 392; CF, art. 93, IX
Desempate: Herdando a regra de 5572, use este nó para o conteúdo e as formalidades da sentença condenatória em geral; se o foco for dosimetria ou regime, use 5576; se forem os efeitos da condenação, use 5577; se for a congruência com a acusação, use 5578.
```
Regra D2 (decisão manual): herdada de 5572: Processo Penal > Sentença Penal: classificação, efeitos, correlação, emendatio e mutatio libelli, absolutória e condenatória

## Prioridade 3

### 4366 · irmão parecido: 4367 Classificação dos Criminosos

```text
[4366] Criminologia > Classificação das Vítimas
Escopo: Tipologias de vítimas elaboradas pela Vitimologia, a partir do grau de participação ou culpa da vítima no delito e de suas características pessoais e sociais (Mendelsohn, Von Hentig, Jiménez de Asúa, Neuman).
Inclui: Classificação de Mendelsohn: vítima completamente inocente (ideal), menos culpada, tão culpada quanto, mais culpada que o infrator e única culpada; Tipologia de Von Hentig: vítima isolada, por proximidade, com ânimo de lucro, deprimida, agressiva, sem valor etc.; Classificação de Jiménez de Asúa: vítimas indiferentes (indeterminadas) e determinadas; resistentes e coadjuvantes; Classificação de Elías Neuman: vítimas individuais, familiares, coletivas e sociais; Vítima provocadora, simuladora e imaginária; Comportamento da vítima como critério de classificação
Não inclui: Vitimização primária, secundária e terciária → 4390; Síndromes de Estocolmo, de Londres, de Lima e da mulher de Potifar → 4383; Conceito, origem e fases históricas da Vitimologia → 4389; Tipologias de delinquentes (Lombroso, Ferri, Garofalo) → 4367; Comportamento da vítima como circunstância judicial na dosimetria → 5202
Âncoras legais: Benjamin Mendelsohn; Hans von Hentig, The Criminal and His Victim (1948); Luis Jiménez de Asúa; Elías Neuman
Desempate: Escolha este nó quando a questão pedir o enquadramento de uma vítima numa tipologia de autor; se tratar das fases ou espécies do processo de vitimização, use 4390.
```

### 4367 · irmão parecido: 4366 Classificação das Vítimas

```text
[4367] Criminologia > Classificação dos Criminosos
Escopo: Tipologias de delinquentes propostas pela Criminologia, sobretudo as da Escola Positiva (Lombroso, Ferri, Garofalo) e as classificações posteriores, como a de Hilário Veiga de Carvalho.
Inclui: Criminoso nato, louco, por paixão, ocasional e epiléptico em Lombroso; Classificação de Ferri: nato, louco, habitual, ocasional e passional; Classificação de Garofalo: assassinos, violentos, ímprobos e cínicos; Classificação de Hilário Veiga de Carvalho: biocriminoso puro, biocriminoso preponderante, mesobiocriminoso, mesocriminoso preponderante e mesocriminoso puro; Criminoso habitual, profissional e ocasional; Atavismo e estigmas físicos como critério de classificação
Não inclui: Postulados gerais e método da Escola Positiva → 4373; Teorias biológicas e psicológicas que explicam a criminalidade no indivíduo → 4386; Tipologias de vítimas → 4366; Inimputabilidade por doença mental no Código Penal → 5213
Âncoras legais: Cesare Lombroso, O Homem Delinquente (1876); Enrico Ferri; Raffaele Garofalo; Hilário Veiga de Carvalho
Desempate: Escolha este nó quando a questão cobrar as categorias de delinquentes de um autor; se cobrar os fundamentos gerais da escola (método, determinismo, defesa social), use 4373.
```

### 4371 · irmão parecido: 4380 Teoria Geral da Criminologia

```text
[4371] Criminologia > Etapas Evolutivas e Escolas Criminológicas
Escopo: Evolução histórica do pensamento criminológico: fase pré-científica (Antiguidade, Idade Média e Moderna; 4372) e escolas criminológicas (Clássica, Positiva, Terceira Escola e afins; 4373).
Inclui: Transição da fase pré-científica para a científica da Criminologia; Marco científico: Lombroso (1876) e a cunhagem do termo Criminologia (Topinard/Garofalo); Visão panorâmica da sucessão entre escolas penais e criminológicas; Contraste geral entre Escola Clássica e Escola Positiva; Pensamento criminal na Antiguidade, Idade Média e Iluminismo
Não inclui: Teorias sociológicas como Escola de Chicago, anomia, associação diferencial e labeling approach → 4388; Tipologias de criminosos de Lombroso, Ferri e Garofalo → 4367; Movimentos de política criminal (Nova Defesa Social, Lei e Ordem, abolicionismo) → 4375; Conceito, objeto e método da Criminologia → 4380
Âncoras legais: Cesare Beccaria, Dos Delitos e das Penas (1764); Cesare Lombroso; Enrico Ferri; Raffaele Garofalo; Francesco Carrara
Desempate: Use o nó geral só para a visão panorâmica da evolução; questões sobre períodos históricos anteriores à fase científica vão para 4372 e questões sobre uma escola específica vão para 4373.
```

### 4374 · irmão parecido: 4367 Classificação dos Criminosos

```text
[4374] Criminologia > Política Criminal
Escopo: Política Criminal como estratégia estatal de enfrentamento da criminalidade e sua relação com a Criminologia e a dogmática penal. As correntes (4375) e o Direito Penal do Inimigo (4376) têm nós próprios.
Inclui: Conceito e função da Política Criminal; Relação tripartida entre Criminologia, Política Criminal e Direito Penal; Frase de von Liszt: o Direito Penal é a barreira intransponível da Política Criminal; Política Criminal como ponte entre o saber empírico e a norma penal; Política criminal e escolhas legislativas de criminalização
Não inclui: Movimento Lei e Ordem, tolerância zero, abolicionismo, minimalismo e garantismo → 4375; Direito Penal do Inimigo de Günther Jakobs → 4376; Criminalização primária e secundária → 4378; Princípios penais como intervenção mínima e fragmentariedade na dogmática → 5172; Prevenção primária, secundária e terciária do delito → 4369
Âncoras legais: Franz von Liszt; Claus Roxin
Desempate: Use o nó geral para o conceito de Política Criminal e sua relação com Criminologia e Direito Penal; se a questão tratar de uma corrente específica, use 4375 ou 4376.
```

### 4377 · irmão parecido: 4374 Política Criminal

```text
[4377] Criminologia > Processos de Criminalização e Cifras Criminais
Escopo: Seletividade do sistema penal: processos de criminalização (primária, secundária; 4378) e criminalidade não registrada nas estatísticas oficiais (cifras criminais; 4379).
Inclui: Seletividade do sistema penal como visão geral; Relação entre a criminalização seletiva e as cifras ocultas; Estatísticas oficiais e suas limitações; Agências de criminalização (legislativo, polícia, MP, Judiciário, sistema penitenciário)
Não inclui: Definição de criminalização primária, secundária e terciária → 4378; Cifra negra, dourada, cinza, amarela, verde e rosa → 4379; Teoria do etiquetamento (labeling approach) e criminologia crítica → 4388; Vitimização secundária causada pelas instâncias formais → 4390
Âncoras legais: Eugenio Raúl Zaffaroni; Alessandro Baratta; Edwin Sutherland
Desempate: Use o nó geral só quando a questão tratar conjuntamente da seletividade e das cifras; questões sobre um tipo de criminalização vão para 4378 e sobre um tipo de cifra vão para 4379.
```

### 4380 · irmão parecido: 4371 Etapas Evolutivas e Escolas Criminológicas

```text
[4380] Criminologia > Teoria Geral da Criminologia
Escopo: Fundamentos da Criminologia como ciência: conceito, objeto (delito, delinquente, vítima e controle social; 4381), método empírico e interdisciplinar e funções (4382).
Inclui: Criminologia como ciência empírica, interdisciplinar e do 'ser'; Objetos da Criminologia: delito, delinquente, vítima e controle social; Controle social formal e informal; Método empírico, indutivo e interdisciplinar; Diferenças entre Criminologia, Direito Penal e Política Criminal; Funções da Criminologia
Não inclui: Evolução histórica e escolas criminológicas → 4371; Conceito e evolução histórica da Vitimologia → 4389; Conceito e fontes do Direito Penal → 5171; Conceito e função da Política Criminal → 4374
Âncoras legais: Antonio García-Pablos de Molina; Edwin Sutherland
Desempate: Use o nó geral quando a questão misturar conceito, objeto e método; se o foco for o conceito ou os objetos, use 4381; se for o método ou as funções, use 4382.
```

### 4381 · irmão parecido: 4382 Métodos e funções da Criminologia

```text
[4381] Criminologia > Teoria Geral da Criminologia > Conceito e objeto da Criminologia
Escopo: Conceito de Criminologia como ciência empírica e interdisciplinar, autonomia e relação com Direito Penal e Política Criminal, e seu objeto: delito, delinquente, vítima e controle social.
Inclui: Conceito de Criminologia como ciência empírica, interdisciplinar e do 'ser'; Objeto da Criminologia: delito, delinquente, vítima e controle social (García-Pablos de Molina); Conceito criminológico de delito como problema social e comunitário (incidência massiva, aflitiva, persistente, com consenso sobre a etiologia); Distinção entre Criminologia (ser), Direito Penal (dever-ser) e Política Criminal no modelo integrado; Ampliação histórica do objeto: do delinquente (positivismo) à vítima e ao controle social; Controle social formal e informal como objeto de estudo; Autonomia científica e origem do termo (Topinard, Garofalo)
Não inclui: Método empírico, indutivo e interdisciplinar e funções da Criminologia → 4382; Vitimologia, conceito de vítima e processo de vitimização → 4389; Correntes e conceito de Política Criminal → 4375; Evolução histórica e escolas (Clássica, Positiva etc.) → 4373; Conceito e fontes do Direito Penal → 5171; Criminalização primária e secundária → 4378
Âncoras legais: García-Pablos de Molina e Luiz Flávio Gomes, Criminologia; Raffaele Garofalo; Paul Topinard
Desempate: Escolha este nó quando a questão tratar do que é a Criminologia, da sua relação com outras ciências penais ou de quais são seus objetos; se tratar de como ela investiga (método) ou para que serve (funções), use 4382.
```

### 4382 · irmão parecido: 4381 Conceito e objeto da Criminologia

```text
[4382] Criminologia > Teoria Geral da Criminologia > Métodos e funções da Criminologia
Escopo: Métodos de investigação da Criminologia (empírico, indutivo, interdisciplinar, quantitativo e qualitativo) e suas funções: informar sobre o delito, prevenir a criminalidade e subsidiar a Política Criminal e o Direito Penal.
Inclui: Método empírico e indutivo da Criminologia versus método lógico-dedutivo e abstrato do Direito Penal; Interdisciplinaridade como método; Técnicas quantitativas (estatísticas) e qualitativas (entrevistas, observação); Inquéritos de vitimização e de autorrevelação (self-report) como técnicas de pesquisa; Função de fornecer informação válida e confiável sobre o delito, o delinquente, a vítima e o controle social; Função de prevenção do delito e de intervenção no homem delinquente; Criminologia como ciência de informação que subsidia a Política Criminal
Não inclui: Conceito e objeto da Criminologia (delito, delinquente, vítima, controle social) → 4381; Cifras ocultas, negras e douradas da criminalidade → 4379; Prevenção primária, secundária e terciária → 4369; Modelos de reação ao delito (dissuasório, ressocializador, restaurativo) → 4370; Interpretação da norma penal → 5173
Âncoras legais: García-Pablos de Molina e Luiz Flávio Gomes, Criminologia
Desempate: Escolha este nó quando a questão tratar da forma de investigação da Criminologia (empirismo, indução, interdisciplinaridade, técnicas de pesquisa) ou das suas finalidades; se tratar do que ela estuda, use 4381; se tratar de modalidades de prevenção, use 4369.
```

### 4388 · irmão parecido: 4387 Teorias de Nível Sociológico

```text
[4388] Criminologia > Teorias Sociológicas Explicativas da Criminalidade > Teorias Criminológicas em Espécie
Escopo: Questões que cobram várias teorias sociológicas da criminalidade ao mesmo tempo (relacionar autor, teoria e conceito) misturando os níveis individual e sociológico, e teorias específicas que não se encaixam claramente em nenhum dos dois níveis.
Inclui: Questão de associação entre autores, teorias e conceitos-chave que mistura teorias micro e macro; Comparação entre teorias de controle/aprendizagem e teorias estruturais na mesma questão; Teoria das janelas quebradas (Wilson e Kelling) como explicação da criminalidade; Teorias de oportunidade e das atividades rotineiras (Cohen e Felson) como explicação do delito; Quadros gerais do tipo 'assinale a correspondência correta entre teoria e premissa'
Não inclui: Questão sobre uma única teoria de processo individual (controle social de Hirschi, neutralização, aprendizagem social de Akers) → 4386; Questão sobre uma única teoria macrossociológica (Escola de Chicago, anomia, subcultura, associação diferencial, labelling approach, criminologia crítica) → 4387; Escola Clássica, Escola Positiva (Lombroso, Ferri, Garofalo) e evolução histórica das escolas → 4373; Programa de tolerância zero e movimentos de lei e ordem como política criminal → 4375; Cifra negra, cifra dourada e seletividade da criminalização → 4379
Âncoras legais: Wilson e Kelling (janelas quebradas); Cohen e Felson (atividades rotineiras)
Desempate: Use este nó quando a questão abranger várias teorias de níveis diferentes (individual e sociológico) ou tratar de teoria fora desses dois grupos; se a questão se concentrar em uma só teoria ou só em teorias do mesmo nível, use 4386 ou 4387.
```

### 4386 · irmão parecido: 4387 Teorias de Nível Sociológico

```text
[4386] Criminologia > Teorias Sociológicas Explicativas da Criminalidade > Teorias de Nível Individual
Escopo: Teorias sociológicas e psicossociais de nível micro, que explicam o crime pelo processo individual de aprendizagem, vínculo ou decisão do agente: controle social, neutralização, aprendizagem social e escolha racional.
Inclui: Teoria do controle social ou dos vínculos sociais de Travis Hirschi (apego, compromisso, envolvimento e crença); Teoria da contenção de Walter Reckless; Técnicas de neutralização de Sykes e Matza (negação da responsabilidade, do dano, da vítima etc.); Teoria da aprendizagem social de Akers (reforço diferencial); Teoria da escolha racional aplicada ao delinquente; Teoria do autocontrole de Gottfredson e Hirschi
Não inclui: Associação diferencial de Sutherland e crimes do colarinho branco, tratadas pela doutrina nacional entre as teorias sociológicas de consenso → 4387; Explicações biológicas e antropológicas do criminoso (Lombroso, criminoso nato) → 4373; Tipologias de delinquentes (classificação de Ferri e outras) → 4367; Questão que mistura teorias individuais e estruturais → 4388
Âncoras legais: Travis Hirschi, Causes of Delinquency (1969); Gresham Sykes e David Matza (técnicas de neutralização); Ronald Akers (aprendizagem social)
Desempate: Use este nó quando a explicação do crime se apoiar em mecanismos do próprio indivíduo (vínculos, autocontrole, racionalizações, decisão); se a causa estiver na estrutura social, na cidade, na cultura do grupo ou na reação social, use 4387.
```

### 4387 · irmão parecido: 4386 Teorias de Nível Individual

```text
[4387] Criminologia > Teorias Sociológicas Explicativas da Criminalidade > Teorias de Nível Sociológico
Escopo: Teorias macrossociológicas que explicam o crime pela estrutura e dinâmica social, divididas em teorias do consenso (Chicago, associação diferencial, anomia, subcultura) e do conflito (labelling approach, criminologia crítica).
Inclui: Divisão entre teorias do consenso (funcionalistas) e do conflito; Escola de Chicago: ecologia criminal, zonas concêntricas, desorganização social; Associação diferencial de Sutherland e crimes do colarinho branco; Teoria da anomia (Durkheim e Merton: modos de adaptação individual); Teoria da subcultura delinquente (Albert Cohen; Cloward e Ohlin); Labelling approach: desvio primário e secundário (Lemert), Becker, rotulação; Criminologia crítica ou radical (Baratta, neorrealismo, abolicionismo como corrente teórica)
Não inclui: Teorias de controle, neutralização, aprendizagem social de Akers e escolha racional → 4386; Criminalização primária e secundária como processo de seleção → 4378; Cifra negra e cifra dourada → 4379; Abolicionismo, minimalismo e direito penal máximo como correntes de política criminal → 4375; Questão que mistura teorias individuais e estruturais → 4388
Âncoras legais: Émile Durkheim e Robert Merton (anomia); Edwin Sutherland (associação diferencial); Albert Cohen (subcultura delinquente); Howard Becker e Edwin Lemert (labelling approach); Alessandro Baratta (criminologia crítica)
Desempate: Use este nó quando a questão tratar de teoria(s) estrutural(is), do consenso ou do conflito, inclusive a associação diferencial; se a ênfase for o processo individual (vínculos, neutralização, autocontrole), use 4386; se combinar teorias dos dois níveis, use 4388.
```

### 4389 · irmão parecido: 4380 Teoria Geral da Criminologia

```text
[4389] Criminologia > Vitimologia
Escopo: Vitimologia como estudo da vítima: conceito, origem, fases históricas do papel da vítima e sua proteção. O processo de vitimização tem nó próprio (4390).
Inclui: Conceito e objeto da Vitimologia; Origem com Mendelsohn e Von Hentig após a Segunda Guerra; Fases do protagonismo, da neutralização e do redescobrimento da vítima; Natureza da Vitimologia: ciência autônoma ou ramo da Criminologia; Declaração da ONU sobre os Princípios Básicos de Justiça para Vítimas (Resolução 40/34 de 1985); Políticas de assistência e reparação à vítima
Não inclui: Vitimização primária, secundária e terciária → 4390; Tipologias de vítimas → 4366; Síndromes e teorias explicativas da vitimização → 4383; Declaração do ofendido como meio de prova no CPP → 5549; Escuta especializada e depoimento especial de criança vítima → 4709
Âncoras legais: Benjamin Mendelsohn; Hans von Hentig; Resolução ONU 40/34 (1985); CPP, art. 201
Desempate: Use o nó geral para conceito, história e proteção da vítima; se a questão tratar das espécies ou fases da vitimização, use 4390.
```

### 4686 · irmão parecido: 4703 Lei de Execução Penal

```text
[4686] Direito Penal - Legislação Especial > Contravenções Penais
Escopo: Lei das Contravenções Penais (Decreto-Lei 3.688/1941) e contravenções esparsas: regras gerais próprias (tentativa, territorialidade, prisão simples, reincidência, ação penal) e contravenções em espécie.
Inclui: Impunibilidade da tentativa de contravenção; Aplicação da lei brasileira só à contravenção praticada no território nacional; Prisão simples, limite de cumprimento e reincidência entre crime e contravenção; Vias de fato, porte de arma branca, perturbação do sossego, jogo de azar e jogo do bicho; Ação penal pública incondicionada nas contravenções; Incompetência da Justiça Federal para julgar contravenções (CF, art. 109, IV)
Não inclui: Transação penal e procedimento do Juizado Especial Criminal → 4701; Posse e porte de arma de fogo (Lei 10.826/2003) → 4697; Importunação sexual (art. 215-A do CP, que substituiu a antiga contravenção) → 5105; Vias de fato no âmbito da violência doméstica contra a mulher → 4704; Perseguição (art. 147-A do CP), que revogou a contravenção de perturbação da tranquilidade → 5130
Âncoras legais: Decreto-Lei 3.688/1941, art. 2º; Decreto-Lei 3.688/1941, art. 4º; Decreto-Lei 3.688/1941, art. 7º; Decreto-Lei 3.688/1941, art. 17; Decreto-Lei 3.688/1941, art. 21; CF, art. 109, IV
Desempate: Use este nó quando a questão for sobre regra ou tipo da LCP; se o foco for o rito do JECrim ou o contexto de violência doméstica, use 4701 ou 4704.
```

### 4692 · irmão parecido: 4693 Crimes Hediondos

```text
[4692] Direito Penal - Legislação Especial > Crimes Eleitorais
Escopo: Crimes eleitorais previstos no Código Eleitoral e na legislação eleitoral esparsa (como a Lei 9.504/1997), com suas regras de ação penal e penas.
Inclui: Corrupção eleitoral (compra de votos), art. 299 do Código Eleitoral; Calúnia, difamação e injúria eleitorais; Denunciação caluniosa com finalidade eleitoral (art. 326-A do Código Eleitoral); Violência política contra a mulher (art. 326-B do Código Eleitoral); Ação penal pública nos crimes eleitorais; Crimes eleitorais da Lei 9.504/1997 (dia da eleição, pesquisas fraudulentas)
Não inclui: Interrupção do processo eleitoral e violência política dos arts. 359-N e 359-P do CP → 5155; Crimes contra a honra comuns do CP → 5120; Denunciação caluniosa comum (art. 339 do CP) → 5080; Competência da Justiça Eleitoral para crimes comuns conexos → 5482
Âncoras legais: Lei 4.737/1965, art. 299; Lei 4.737/1965, art. 326-A; Lei 4.737/1965, art. 326-B; Lei 4.737/1965, art. 355
Desempate: Use este nó para tipos do Código Eleitoral e da Lei 9.504/1997; crimes contra o funcionamento das eleições inseridos no CP (Título XII) vão para 5155.
```

### 4693 · irmão parecido: 4692 Crimes Eleitorais

```text
[4693] Direito Penal - Legislação Especial > Crimes Hediondos
Escopo: Lei 8.072/1990: rol dos crimes hediondos e equiparados (tortura, tráfico, terrorismo) e as consequências próprias, como vedações de anistia, graça, indulto e fiança, prisão temporária ampliada e associação criminosa qualificada.
Inclui: Rol taxativo dos crimes hediondos do art. 1º da Lei 8.072/1990; Equiparados a hediondos e mandado de criminalização do art. 5º, XLIII, da CF; Vedação de anistia, graça, indulto e fiança; Inconstitucionalidade do regime inicial obrigatoriamente fechado; Prisão temporária de 30 dias prorrogáveis; Associação criminosa para hediondos (art. 8º) e delação; Hediondez de crimes específicos (homicídio qualificado, estupro, latrocínio, posse e porte de arma de uso proibido)
Não inclui: Frações de progressão de regime para hediondos (art. 112 da LEP) → 4703; Tráfico privilegiado e tipos da Lei de Drogas → 4708; Tipos de tortura da Lei 9.455/1997 → 4707; Requisitos e procedimento da prisão temporária → 5520; Anistia, graça e indulto como causas gerais de extinção da punibilidade → 5193; Requisitos gerais do livramento condicional → 5208
Âncoras legais: Lei 8.072/1990, art. 1º; Lei 8.072/1990, art. 2º; Lei 8.072/1990, art. 8º; CF, art. 5º, XLIII
Desempate: Use este nó quando a questão tratar da natureza hedionda do crime ou de efeito previsto na Lei 8.072/1990; se tratar da estrutura do tipo penal, use o nó do crime.
```

### 4695 · irmão parecido: 4691 Crimes de Trânsito

```text
[4695] Direito Penal - Legislação Especial > Crimes Tributários
Escopo: Crimes contra a ordem tributária da Lei 8.137/1990 (arts. 1º a 3º), incluídos o lançamento definitivo como condição de tipicidade, a suspensão e a extinção da punibilidade pelo parcelamento ou pagamento e a insignificância em matéria tributária.
Inclui: Supressão ou redução de tributo mediante fraude (art. 1º) como crime material; Súmula Vinculante 24: tipicidade depende do lançamento definitivo; Crimes formais do art. 2º, como apropriação de tributo declarado e não recolhido (contumácia, RHC 163.334); Crimes funcionais contra a ordem tributária (art. 3º); Extinção da punibilidade pelo pagamento e suspensão pelo parcelamento; Representação fiscal para fins penais
Não inclui: Contrabando e descaminho (art. 334 e 334-A do CP) → 5094; Apropriação indébita previdenciária (art. 168-A do CP) → 5165; Excesso de exação (art. 316, § 1º, do CP) → 5091; Crimes contra a ordem econômica e as relações de consumo da Lei 8.137/1990 (arts. 4º a 7º) → 4687; Lavagem de dinheiro do produto da sonegação → 4702
Âncoras legais: Lei 8.137/1990, arts. 1º a 3º; Lei 10.684/2003, art. 9º; Lei 9.430/1996, art. 83
Desempate: Use este nó quando o bem jurídico for a arrecadação tributária com base na Lei 8.137/1990; tributo aduaneiro iludido na importação (descaminho) vai para 5094.
```

### 4687 · irmão parecido: 4689 Crimes contra o Sistema Financeiro

```text
[4687] Direito Penal - Legislação Especial > Crimes contra a Economia Popular
Escopo: Crimes contra a economia popular (Lei 1.521/1951), como usura e pirâmide financeira, e, como nó mais próximo, os crimes contra a ordem econômica e as relações de consumo fora do CDC (Lei 8.137/1990, arts. 4º a 7º).
Inclui: Usura pecuniária ou real (art. 4º da Lei 1.521/1951); Pirâmide financeira e correntes (art. 2º, IX, da Lei 1.521/1951); Fraude de pesos e medidas e outras condutas contra a economia popular; Competência da Justiça Estadual (Súmula 498 do STF); Crimes contra a ordem econômica (Lei 8.137/1990, art. 4º); Crimes contra as relações de consumo da Lei 8.137/1990 (art. 7º)
Não inclui: Captação irregular de recursos, operar instituição financeira sem autorização e evasão de divisas → 4689; Crimes tipificados no Código de Defesa do Consumidor (Lei 8.078/1990) → 4694; Sonegação fiscal (Lei 8.137/1990, arts. 1º a 3º) → 4695; Estelionato contra vítima determinada → 5166
Âncoras legais: Lei 1.521/1951, art. 2º; Lei 1.521/1951, art. 4º; Lei 8.137/1990, art. 4º; Lei 8.137/1990, art. 7º
Desempate: Use este nó quando a lesão atingir um número indeterminado de pessoas (economia popular); se houver instituição financeira ou operação de câmbio, use 4689.
```

### 4689 · irmão parecido: 4687 Crimes contra a Economia Popular

```text
[4689] Direito Penal - Legislação Especial > Crimes contra o Sistema Financeiro
Escopo: Crimes contra o Sistema Financeiro Nacional (Lei 7.492/1986): conceito de instituição financeira, gestão fraudulenta e temerária, operação sem autorização, evasão de divisas, responsabilidade penal e competência federal.
Inclui: Conceito e equiparação de instituição financeira (art. 1º); Gestão fraudulenta e gestão temerária (art. 4º); Operar instituição financeira sem autorização (art. 16); Obtenção de financiamento mediante fraude (art. 19); Evasão de divisas e manutenção de depósitos no exterior não declarados (art. 22); Responsabilidade de controladores e administradores, e delação (art. 25); Ação penal do MPF e competência da Justiça Federal (art. 26)
Não inclui: Pirâmide financeira sem atividade de instituição financeira → 4687; Lavagem de capitais → 4702; Sonegação fiscal → 4695; Estelionato comum → 5166; Organização criminosa voltada a fraudes financeiras → 4705
Âncoras legais: Lei 7.492/1986, art. 1º; Lei 7.492/1986, art. 4º; Lei 7.492/1986, art. 16; Lei 7.492/1986, art. 22; Lei 7.492/1986, art. 25; Lei 7.492/1986, art. 26; CF, art. 109, VI
Desempate: Use este nó quando a conduta envolver instituição financeira, câmbio ou o mercado financeiro regulado; se o foco for ocultar a origem ilícita de valores, use 4702.
```

### 4688 · irmão parecido: 4687 Crimes contra a Economia Popular

```text
[4688] Direito Penal - Legislação Especial > Crimes contra o meio ambiente
Escopo: Lei 9.605/1998: responsabilidade penal da pessoa jurídica, penas e institutos despenalizadores ambientais, e crimes contra a fauna, a flora, o ordenamento urbano e o patrimônio cultural, de poluição e contra a administração ambiental.
Inclui: Responsabilidade penal da pessoa jurídica (CF, art. 225, § 3º) e superação da dupla imputação; Desconsideração da personalidade jurídica e penas aplicáveis à pessoa jurídica; Transação condicionada à composição do dano e suspensão do processo com laudo de reparação; Crimes contra a fauna, incluindo maus-tratos a animais (art. 32); Crimes contra a flora, poluição e crimes contra a administração ambiental; Insignificância em crimes ambientais
Não inclui: Crimes envolvendo OGM e embriões (Lei 11.105/2005) → 4685; Incêndio e outros crimes de perigo comum do CP → 5126; Competência da Justiça Federal ou Estadual em crimes ambientais → 5482; Maus-tratos a pessoa sob guarda (art. 136 do CP) → 5143; Transação penal e suspensão do processo em geral (Lei 9.099/1995) → 4701
Âncoras legais: CF, art. 225, § 3º; Lei 9.605/1998, art. 3º; Lei 9.605/1998, art. 4º; Lei 9.605/1998, arts. 21 a 24; Lei 9.605/1998, arts. 27 e 28; Lei 9.605/1998, art. 32
Desempate: Use este nó quando a questão envolver a Lei 9.605/1998, inclusive suas regras próprias de transação e sursis processual; regras gerais da Lei 9.099/1995 vão para 4701.
```

### 4690 · irmão parecido: 4691 Crimes de Trânsito

```text
[4690] Direito Penal - Legislação Especial > Crimes de Racismo
Escopo: Crimes resultantes de preconceito de raça, cor, etnia, religião ou procedência nacional (Lei 7.716/1989), incluindo a injúria racial deslocada para o art. 2º-A, o mandado constitucional de criminalização e a equiparação da homotransfobia ao racismo.
Inclui: Imprescritibilidade e inafiançabilidade do racismo (CF, art. 5º, XLII); Injúria racial (art. 2º-A da Lei 7.716/1989) e sua equiparação ao racismo; Praticar, induzir ou incitar discriminação ou preconceito (art. 20), inclusive por meios de comunicação; Homofobia e transfobia enquadradas como racismo (ADO 26 e MI 4733); Condutas de impedimento de acesso a cargos, estabelecimentos e serviços; Racismo recreativo e agravantes da Lei 14.532/2023
Não inclui: Injúria qualificada por religião, idade ou deficiência (art. 140, § 3º, do CP) → 5124; Genocídio (Lei 2.889/1956) → 4698; Ultraje a culto e crimes contra o sentimento religioso (art. 208 do CP) → 5137; Discriminação contra pessoa idosa → 4696
Âncoras legais: CF, art. 5º, XLII; Lei 7.716/1989, art. 2º-A; Lei 7.716/1989, art. 20
Desempate: Use este nó quando houver ofensa ou discriminação por raça, cor, etnia, religião, procedência nacional ou orientação sexual; injúria discriminatória por idade ou deficiência continua no CP (5124).
```

### 4691 · irmão parecido: 4690 Crimes de Racismo

```text
[4691] Direito Penal - Legislação Especial > Crimes de Trânsito
Escopo: Crimes de trânsito do Código de Trânsito Brasileiro (Lei 9.503/1997, arts. 291 a 312-B): disposições gerais, institutos despenalizadores, suspensão da habilitação e tipos em espécie.
Inclui: Homicídio culposo e lesão corporal culposa na direção de veículo (arts. 302 e 303); Embriaguez ao volante e meios de prova (art. 306); Racha, direção sem habilitação, entrega da direção a pessoa não habilitada (Súmula 575 do STJ); Omissão de socorro e fuga do local do acidente (arts. 304 e 305); Aplicação da Lei 9.099/1995 à lesão culposa de trânsito e suas exceções (art. 291); Não imposição de flagrante a quem presta socorro (art. 301) e vedação de substituição da pena (art. 312-B)
Não inclui: Distinção entre dolo eventual e culpa consciente em acidentes → 5222; Homicídio doloso praticado com veículo → 5150; Omissão de socorro do art. 135 do CP → 5142; Embriaguez e actio libera in causa na culpabilidade → 5213
Âncoras legais: Lei 9.503/1997, art. 291; Lei 9.503/1997, art. 301; Lei 9.503/1997, arts. 302 a 312; Lei 9.503/1997, art. 312-B
Desempate: Use este nó quando a questão aplicar tipos ou regras do CTB; se discutir em abstrato o elemento subjetivo (dolo eventual vs. culpa consciente), use 5222.
```

### 4694 · irmão parecido: 4690 Crimes de Racismo

```text
[4694] Direito Penal - Legislação Especial > Crimes previstos no CDC
Escopo: Infrações penais previstas no Código de Defesa do Consumidor (Lei 8.078/1990, arts. 61 a 80): tipos em espécie, agravantes, penas e intervenção das entidades de defesa do consumidor no processo penal.
Inclui: Omissão de informação sobre nocividade ou periculosidade de produtos (art. 63); Afirmação falsa ou enganosa e publicidade enganosa ou abusiva (arts. 66 e 67); Cobrança abusiva de dívidas (art. 71); Impedir o acesso a cadastros e omitir correção de informações (arts. 72 e 73); Agravantes específicas (art. 76) e penas cumulativas (art. 78); Assistência e ação penal subsidiária por entidades legitimadas (art. 80)
Não inclui: Crimes contra as relações de consumo da Lei 8.137/1990 (art. 7º) → 4687; Usura e crimes contra a economia popular → 4687; Falsificação ou adulteração de alimentos e medicamentos (arts. 272 e 273 do CP) → 5145; Estelionato contra consumidor determinado → 5166
Âncoras legais: Lei 8.078/1990, arts. 61 a 80
Desempate: Use este nó só para os tipos da Lei 8.078/1990; crimes contra o consumo previstos na Lei 8.137/1990 vão para 4687.
```

### 4697 · irmão parecido: 4696 Estatuto do Idoso - Crimes

```text
[4697] Direito Penal - Legislação Especial > Estatuto do Desarmamento
Escopo: Crimes do Estatuto do Desarmamento (Lei 10.826/2003, arts. 12 a 21): posse, porte, disparo, omissão de cautela, comércio ilegal e tráfico internacional de arma de fogo, munição e acessório, e questões de abolitio temporária e hediondez.
Inclui: Distinção entre posse (art. 12) e porte (art. 14) de arma de uso permitido; Posse ou porte de arma de uso restrito ou proibido e figuras equiparadas (art. 16); Disparo de arma de fogo e omissão de cautela (arts. 13 e 15); Comércio ilegal e tráfico internacional de arma de fogo (arts. 17 e 18); Perigo abstrato: arma desmuniciada, munição isolada e arma inapta; Abolitio criminis temporária da posse pelo prazo de entrega (arts. 30 a 32); Inconstitucionalidade da vedação à liberdade provisória (ADI 3112)
Não inclui: Porte de arma branca (art. 19 da LCP) → 4686; Majorante do emprego de arma de fogo no roubo → 5160; Majorante do uso de arma no tráfico de drogas (Lei 11.343/2006, art. 40, IV) → 4708; Consequências gerais da hediondez (Lei 8.072/1990) → 4693
Âncoras legais: Lei 10.826/2003, arts. 12 a 21; Lei 10.826/2003, arts. 30 a 32
Desempate: Use este nó quando o crime for a própria posse, porte ou circulação da arma de fogo; quando a arma for apenas meio de outro crime (roubo, tráfico), use o nó desse crime.
```

### 4696 · irmão parecido: 4697 Estatuto do Desarmamento

```text
[4696] Direito Penal - Legislação Especial > Estatuto do Idoso - Crimes
Escopo: Crimes e disposições penais e processuais penais do Estatuto da Pessoa Idosa (Lei 10.741/2003): tipos penais com vítima idosa, ação penal e procedimento aplicável.
Inclui: Tipos penais dos arts. 96 a 108 (discriminação, omissão de socorro a idoso, abandono, apropriação de proventos, retenção de cartão); Ação penal pública incondicionada nos crimes do Estatuto (art. 95); Inaplicabilidade das escusas absolutórias dos arts. 181 e 182 do CP aos crimes do Estatuto; Procedimento da Lei 9.099/95 para crimes com pena máxima até 4 anos (art. 94) e a interpretação da ADI 3096; Apropriação ou desvio de bens, proventos ou pensão do idoso (art. 102)
Não inclui: Exclusão das imunidades patrimoniais do CP quando a vítima tem 60 anos ou mais (CP, art. 183, III) → 5158; Agravante genérica do crime contra maior de 60 anos (CP, art. 61, II, h) → 5203; Abandono de incapaz previsto no Código Penal → 5141; Maus-tratos do art. 136 do CP → 5143; Institutos despenalizadores da Lei 9.099/95 em visão geral → 4701
Âncoras legais: Lei 10.741/2003, arts. 93 a 108; Lei 10.741/2003, art. 94; Lei 10.741/2003, art. 95
```

### 4699 · irmão parecido: 4705 Organizações Criminosas

```text
[4699] Direito Penal - Legislação Especial > Identificação Criminal
Escopo: Identificação criminal do civilmente identificado (CF, art. 5º, LVIII, e Lei 12.037/2009): hipóteses autorizadoras, processos datiloscópico e fotográfico, coleta de perfil genético e bancos de dados.
Inclui: Regra de não identificação criminal do civilmente identificado e exceções legais; Hipóteses do art. 3º da Lei 12.037/2009 (documento rasurado, insuficiente, conflitante, essencial às investigações); Coleta de material biológico para perfil genético (Lei 12.654/2012); Identificação do perfil genético de condenados (LEP, art. 9º-A); Banco Nacional de Perfis Genéticos e Banco Multibiométrico; Exclusão dos dados em caso de absolvição, arquivamento ou rejeição da denúncia
Não inclui: Reconhecimento de pessoas e coisas como meio de prova → 5551; Exame de corpo de delito → 5545; Diligências da autoridade policial no inquérito (CPP, art. 6º) → 5500; Direitos e deveres do preso na execução penal → 4703
Âncoras legais: CF, art. 5º, LVIII; Lei 12.037/2009, arts. 1º a 3º; Lei 12.037/2009, art. 5º-A; Lei 7.210/1984, art. 9º-A
Desempate: Use este nó quando a questão tratar das hipóteses e procedimentos de identificação criminal ou perfil genético; se tratar do reconhecimento ou perícia como prova no processo, use o nó de Provas em Espécie.
```

### 4704 · irmão parecido: 4703 Lei de Execução Penal

```text
[4704] Direito Penal - Legislação Especial > Lei Maria da Penha
Escopo: Lei 11.340/2006 (Maria da Penha): conceito e formas de violência doméstica e familiar contra a mulher, medidas protetivas de urgência, crime de descumprimento, atuação policial e regras processuais especiais.
Inclui: Conceito de violência doméstica e familiar e âmbito de incidência (art. 5º); Formas de violência: física, psicológica, sexual, patrimonial e moral (art. 7º); Medidas protetivas de urgência (arts. 18 a 24) e crime de descumprimento (art. 24-A); Afastamento do agressor pela autoridade policial (art. 12-C); Renúncia à representação apenas em audiência perante o juiz (art. 16); Vedação da Lei 9.099/95 e de penas de cesta básica ou pecuniárias (arts. 17 e 41); Súmulas do STJ sobre violência doméstica (536, 542, 588, 589)
Não inclui: Feminicídio (tipo penal do CP) → 5151; Violência psicológica contra a mulher (CP, art. 147-B) → 5131; Lesão corporal em violência doméstica (CP, art. 129, § 9º) → 5077; Ameaça e perseguição (CP, arts. 147 e 147-A) → 5130; Prisão preventiva em geral (CPP, arts. 311 a 316) → 5519
Âncoras legais: Lei 11.340/2006, arts. 5º e 7º; Lei 11.340/2006, arts. 12-C e 16; Lei 11.340/2006, arts. 18 a 24-A; Lei 11.340/2006, arts. 17 e 41; CF, art. 226, § 8º
Desempate: Use este nó quando a questão versar sobre a Lei 11.340/2006 em si; se cobrar a estrutura de um tipo penal do CP (feminicídio, lesão, ameaça), use o nó do respectivo crime.
```

### 4703 · irmão parecido: 4704 Lei Maria da Penha

```text
[4703] Direito Penal - Legislação Especial > Lei de Execução Penal
Escopo: Lei de Execução Penal (Lei 7.210/1984): direitos e deveres do preso, disciplina, órgãos da execução, regimes e progressão, remição, autorizações de saída, RDD e incidentes da execução.
Inclui: Direitos e deveres do condenado e assistência ao preso; Faltas disciplinares graves e sanções (art. 50 e seguintes); Regime disciplinar diferenciado (art. 52); Progressão e regressão de regime (arts. 112 e 118); Remição pelo trabalho e pelo estudo (art. 126); Permissão de saída e saída temporária (arts. 120 a 125); Competência do juízo da execução e órgãos da execução (arts. 61 e 66)
Não inclui: Agravo em execução → 5566; Requisitos do livramento condicional no CP → 5208; Regimes iniciais e penas privativas de liberdade no CP → 5201; Penas restritivas de direitos no CP → 5205; Coleta de perfil genético do condenado → 4699; Fixação do regime na sentença → 5576
Âncoras legais: Lei 7.210/1984, arts. 41 e 50; Lei 7.210/1984, art. 52; Lei 7.210/1984, arts. 112 e 118; Lei 7.210/1984, arts. 120 a 126; Lei 7.210/1984, art. 66
Desempate: Use este nó para a fase de execução regida pela LEP; se a questão tratar da pena ou instituto como regulado no CP (cominação, requisitos materiais), use o nó de Teoria da Pena.
```

### 4706 · irmão parecido: 4690 Crimes de Racismo

```text
[4706] Direito Penal - Legislação Especial > Terrorismo
Escopo: Lei Antiterrorismo (Lei 13.260/2016): conceito de terrorismo, atos de terrorismo, organização terrorista, atos preparatórios, financiamento, excludente de manifestações sociais e regras processuais.
Inclui: Conceito de terrorismo: motivação por xenofobia ou discriminação e finalidade de provocar terror social ou generalizado (art. 2º); Excludente para manifestações políticas e movimentos sociais (art. 2º, § 2º); Promover, constituir, integrar ou prestar auxílio a organização terrorista (art. 3º); Punição de atos preparatórios (art. 5º); Financiamento do terrorismo (art. 6º); Competência da Justiça Federal (art. 11); Equiparação a crime hediondo (CF, art. 5º, XLIII)
Não inclui: Crimes contra o Estado Democrático de Direito (CP, arts. 359-I e seguintes) → 5155; Organização criminosa (Lei 12.850/2013) → 4705; Regime jurídico geral dos crimes hediondos e equiparados → 4693; Fases do iter criminis e impunibilidade de atos preparatórios em geral → 5176; Crimes de racismo → 4690
Âncoras legais: Lei 13.260/2016, art. 2º; Lei 13.260/2016, arts. 3º a 6º; Lei 13.260/2016, art. 11; CF, art. 5º, XLIII
```

### 4708 · irmão parecido: 4705 Organizações Criminosas

```text
[4708] Direito Penal - Legislação Especial > Tráfico de Drogas
Escopo: Lei de Drogas (Lei 11.343/2006) na parte penal e processual: porte para consumo, tráfico e figuras equiparadas, tráfico privilegiado, associação para o tráfico, causas de aumento e procedimento especial.
Inclui: Porte de droga para consumo pessoal (art. 28) e decisão do STF no RE 635.659; Tráfico de drogas e condutas equiparadas (art. 33, caput e § 1º); Tráfico privilegiado e afastamento da hediondez (art. 33, § 4º); Uso compartilhado (art. 33, § 3º); Associação para o tráfico (art. 35) e financiamento (art. 36); Causas de aumento, inclusive transnacionalidade e interestadualidade (art. 40); Procedimento especial, laudo de constatação e defesa prévia (arts. 48 a 59)
Não inclui: Regime jurídico geral dos crimes hediondos e equiparados → 4693; Associação criminosa (CP, art. 288) → 5146; Organização criminosa (Lei 12.850/2013) → 4705; Lavagem do produto do tráfico → 4702; Crimes contra a saúde pública do CP (falsificação de medicamentos etc.) → 5145
Âncoras legais: Lei 11.343/2006, art. 28; Lei 11.343/2006, art. 33; Lei 11.343/2006, arts. 35 e 36; Lei 11.343/2006, art. 40; Lei 11.343/2006, arts. 48 a 59; Lei 11.343/2006, art. 70
```

### 4709 · irmão parecido: 4688 Crimes contra o meio ambiente

```text
[4709] Direito Penal - Legislação Especial > Violência contra Criança e Adolescente
Escopo: Tutela penal e processual da criança e do adolescente em leis especiais: crimes do ECA, sistema de garantia de direitos da vítima ou testemunha de violência (Lei 13.431/2017) e Lei Henry Borel (Lei 14.344/2022).
Inclui: Crimes do ECA (arts. 228 a 244-B), como produção e divulgação de pornografia infantojuvenil (arts. 240 a 241-E); Corrupção de menores do ECA (art. 244-B) e Súmula 500 do STJ; Escuta especializada e depoimento especial (Lei 13.431/2017); Formas de violência contra criança e adolescente (Lei 13.431/2017, art. 4º); Medidas protetivas e crimes da Lei 14.344/2022 (Lei Henry Borel)
Não inclui: Estupro de vulnerável (CP, art. 217-A) → 5103; Corrupção de menores do CP (art. 218) e demais crimes sexuais contra vulnerável → 5108; Maus-tratos (CP, art. 136) → 5143; Abandono de incapaz (CP, art. 133) → 5141; Tortura-castigo de criança sob guarda (Lei 9.455/1997) → 4707; Intimidação sistemática (bullying) do CP → 5129
Âncoras legais: Lei 8.069/1990, arts. 240 a 241-E; Lei 8.069/1990, art. 244-B; Lei 13.431/2017, arts. 4º, 7º e 8º; Lei 14.344/2022; CF, art. 227, § 4º
Desempate: Use este nó quando a questão tratar do ECA, da Lei 13.431/2017 ou da Lei 14.344/2022; se o tipo penal estiver no Código Penal (estupro de vulnerável, art. 218), use o nó do respectivo crime.
```

### 5066 · irmão parecido: 5071 Concurso de Pessoas

```text
[5066] Penal > Concurso de Crimes
Escopo: Concurso de crimes: pluralidade de infrações praticadas pelo mesmo agente e os sistemas de aplicação da pena (cúmulo material, exasperação). Abrange o concurso material, o formal, o crime continuado e a multa no concurso de crimes.
Inclui: Distinção geral entre concurso material, formal e crime continuado; Sistemas do cúmulo material e da exasperação; Concurso material benéfico como limite do concurso formal e do continuado; Questões comparativas entre as modalidades; Limite de cumprimento da pena e unificação no concurso de crimes
Não inclui: Pluralidade de agentes num mesmo crime → 5071; Conflito aparente de normas: consunção, especialidade e subsidiariedade → 5183; Prescrição no concurso de crimes, contada isoladamente para cada crime (CP, art. 119) → 5190; Requisitos do crime continuado e continuidade delitiva específica → 5069; Unificação das penas no juízo da execução → 4703
Âncoras legais: CP, arts. 69 a 72; CP, art. 75; CP, art. 119
Desempate: Use o nó-pai quando a questão comparar modalidades ou tratar dos sistemas de aplicação da pena em geral. Se a questão for sobre uma única modalidade, use o subtema dela (5067, 5068, 5069 ou 5070).
```

### 5068 · irmão parecido: 5067 Concurso Material

```text
[5068] Penal > Concurso de Crimes > Concurso Formal
Escopo: Concurso formal (ideal) de crimes: uma só ação ou omissão que produz dois ou mais crimes. Abrange as espécies próprio e impróprio, o sistema da exasperação, o cúmulo de penas por desígnios autônomos e o concurso material benéfico.
Inclui: Conceito e requisitos: unidade de conduta e pluralidade de resultados/crimes; Concurso formal próprio (perfeito) e impróprio (imperfeito, com desígnios autônomos); Concurso formal homogêneo e heterogêneo; Exasperação de 1/6 até metade; fração conforme o número de crimes; Cúmulo material das penas no concurso formal impróprio; Concurso material benéfico (art. 70, parágrafo único); Aplicação do art. 70 na aberratio ictus e na aberratio criminis com duplo resultado (arts. 73 e 74, parte final)
Não inclui: Pluralidade de condutas com soma de penas (cúmulo material) → 5067; Aplicação distinta e integral da multa no concurso de crimes → 5070; Conceito de erro na execução e resultado diverso do pretendido como espécies de erro acidental → 5224; Conflito aparente de normas (consunção, especialidade, subsidiariedade) → 5183; Prescrição de cada crime isoladamente no concurso (art. 119 do CP) → 5187
Âncoras legais: CP, art. 70; CP, art. 73; CP, art. 74
Desempate: Escolha este nó quando houver uma única conduta com vários resultados; se houver mais de uma conduta, vá para concurso material (5067) ou crime continuado (5069).
```

### 5067 · irmão parecido: 5068 Concurso Formal

```text
[5067] Penal > Concurso de Crimes > Concurso Material
Escopo: Concurso material (real) de crimes: duas ou mais ações ou omissões que geram dois ou mais crimes, idênticos ou não, com aplicação cumulativa das penas e regras sobre a ordem de execução e o cumprimento de penas restritivas de direitos.
Inclui: Conceito e requisitos: pluralidade de condutas e de crimes; Concurso material homogêneo e heterogêneo; Sistema do cúmulo material: soma das penas privativas de liberdade; Reclusão e detenção cumuladas: executa-se primeiro a reclusão; Restritivas de direitos no concurso material: cumprimento simultâneo ou sucessivo (art. 69, §§ 1º e 2º); Distinção entre concurso material e crime continuado quando faltam os requisitos do art. 71
Não inclui: Uma só conduta com vários resultados e concurso material benéfico → 5068; Pluralidade de condutas em continuidade delitiva (art. 71) → 5069; Multa no concurso de crimes (art. 72) → 5070; Limite máximo de 40 anos de cumprimento e unificação de penas (art. 75 do CP) → 5201; Soma de penas para a suspensão condicional do processo (Súmula 243 do STJ) → 5542
Âncoras legais: CP, art. 69; CP, art. 76
Desempate: Escolha este nó para várias condutas com soma de penas; se o enunciado trata do concurso material benéfico do art. 70, parágrafo único, a questão vai para concurso formal (5068).
```

### 5070 · irmão parecido: 5068 Concurso Formal

```text
[5070] Penal > Concurso de Crimes > Pena de Multa no Concurso de Crimes
Escopo: Regra da pena de multa no concurso de crimes: aplicação distinta e integral das multas (art. 72 do CP) e seu alcance nas hipóteses de concurso material, formal e de crime continuado.
Inclui: Multas aplicadas distinta e integralmente no concurso de crimes (art. 72); Afastamento da exasperação para a multa no concurso material e formal; Debate sobre a aplicação do art. 72 ao crime continuado (STJ: multa única com o aumento do art. 71); Cálculo das multas cumuladas na sentença com pluralidade de crimes
Não inclui: Sistema de dias-multa, valor do dia-multa e execução da multa em geral → 5206; Exasperação da pena privativa de liberdade no concurso formal → 5068; Exasperação da pena privativa de liberdade no crime continuado → 5069
Âncoras legais: CP, art. 72
Desempate: Escolha este nó sempre que o ponto central for a multa em situação de pluralidade de crimes; regras gerais da multa, sem concurso, vão para 5206.
```

### 5071 · irmão parecido: 5066 Concurso de Crimes

```text
[5071] Penal > Concurso de Pessoas
Escopo: Concurso de pessoas: requisitos, teorias (monista, dualista, pluralista) e punição de quem concorre para o crime, incluindo autoria, participação, cooperação dolosamente distinta e comunicabilidade de circunstâncias.
Inclui: Requisitos do concurso de pessoas: pluralidade de agentes, relevância causal, liame subjetivo e identidade de infração; Teoria monista adotada pelo CP e suas exceções pluralistas; Teorias sobre a autoria (restritiva, extensiva, domínio do fato) em visão geral; Participação de menor importância (CP, art. 29, § 1º); Impunibilidade do ajuste, da determinação e do auxílio se o crime não chega a ser tentado (CP, art. 31)
Não inclui: Comunicação de circunstâncias e elementares de caráter pessoal (CP, art. 30) → 5076; Autoria mediata, autoria colateral e coautoria → 5073; Desvio subjetivo entre agentes (CP, art. 29, § 2º) → 5075; Associação criminosa como crime autônomo (CP, art. 288) → 5146; Organização criminosa (Lei 12.850/2013) → 4705; Pluralidade de crimes praticados pelo mesmo agente → 5066
Âncoras legais: CP, arts. 29 a 31
Desempate: Use o nó-pai para os requisitos e as teorias gerais do concurso de pessoas. Se a questão tratar de um instituto com subtema próprio (participação, autoria mediata, cooperação dolosamente distinta, comunicabilidade), use esse subtema.
```

### 5072 · irmão parecido: 5074 Participação

```text
[5072] Penal > Concurso de Pessoas > Autores e Partícipes
Escopo: Distinção entre autor e partícipe e teorias que a fundamentam (restritiva, extensiva, objetivo-formal, domínio do fato). Abrange também a teoria monista do art. 29, caput, suas exceções pluralistas e os requisitos do concurso de pessoas.
Inclui: Teorias da autoria: restritiva (objetivo-formal e objetivo-material), extensiva/subjetiva e do domínio do fato; Critério para distinguir autor de partícipe; Teoria monista ou unitária (art. 29, caput) e exceções pluralistas (ex.: aborto consentido x provocado; corrupção ativa x passiva); Requisitos do concurso: pluralidade de agentes e condutas, relevância causal, liame subjetivo e identidade de infração; Concurso necessário x eventual (crimes plurissubjetivos e monossubjetivos); Concurso de pessoas em crimes culposos e omissivos (visão geral)
Não inclui: Autoria mediata, autoria colateral, autoria incerta e coautoria (inclusive sucessiva) → 5073; Formas de participação (induzimento, instigação, auxílio), teorias da acessoriedade e participação de menor importância → 5074; Agente que quis participar de crime menos grave (art. 29, § 2º) → 5075; Comunicabilidade de circunstâncias e elementares pessoais (art. 30) → 5076; Agravantes aplicáveis no concurso de pessoas (art. 62) → 5203; Associação criminosa como crime autônomo (CP, art. 288) → 5146
Âncoras legais: CP, art. 29; CP, art. 62
Desempate: Use este nó quando a questão tratar do critério geral para distinguir autor de partícipe, das teorias da autoria ou dos requisitos/teoria monista; se focar numa modalidade específica de autoria vá para 5073, e se focar no regime do partícipe vá para 5074.
```

### 5074 · irmão parecido: 5072 Autores e Partícipes

```text
[5074] Penal > Concurso de Pessoas > Participação
Escopo: Participação em sentido estrito: modalidades (induzimento, instigação, auxílio), teorias da acessoriedade, participação de menor importância e casos de impunibilidade do ajuste, instigação e auxílio (art. 31).
Inclui: Participação moral (induzimento e instigação) e material (auxílio); Teorias da acessoriedade: mínima, limitada, máxima e hiperacessoriedade; Participação de menor importância: diminuição de 1/6 a 1/3 (art. 29, § 1º); Impunibilidade do ajuste, determinação, instigação e auxílio se o crime não chega a ser tentado (art. 31); Participação por omissão, conivência e participação negativa; Participação sucessiva e participação em cadeia; Participação posterior à consumação e sua distinção do favorecimento
Não inclui: Distinção geral entre autor e partícipe e teoria do domínio do fato → 5072; Coautoria e autoria mediata → 5073; Partícipe que quis participar de crime menos grave (art. 29, § 2º) → 5075; Favorecimento pessoal e real como crimes autônomos → 5084; Desistência voluntária e arrependimento eficaz em geral → 5178
Âncoras legais: CP, art. 29, § 1º; CP, art. 31
Desempate: Use este nó quando a questão tratar do regime jurídico do partícipe (forma de contribuição, acessoriedade, menor importância, art. 31); se a dúvida for apenas se o agente é autor ou partícipe pelo critério teórico, use 5072.
```

### 5077 · irmão parecido: 5063 Ação Penal

```text
[5077] Penal > Das Lesões Corporais
Escopo: Crime de lesão corporal (CP, art. 129) em todas as formas: leve, grave, gravíssima, seguida de morte, privilegiada, culposa e as lesões qualificadas pela violência doméstica ou cometidas contra agentes de segurança.
Inclui: Lesão corporal leve e princípio da insignificância; Lesões graves e gravíssimas (CP, art. 129, §§ 1º e 2º); Lesão corporal seguida de morte como crime preterdoloso; Lesão corporal privilegiada e substituição da pena; Lesão corporal culposa e perdão judicial; Lesão em contexto de violência doméstica e contra a mulher (CP, art. 129, §§ 9º, 10 e 13); Ação penal na lesão leve e na lesão culposa (Lei 9.099/1995, art. 88)
Não inclui: Lesão corporal culposa na direção de veículo automotor (CTB, art. 303) → 4691; Tortura que resulta em lesão corporal → 4707; Maus-tratos com resultado de lesão grave → 5143; Inaplicabilidade da Lei 9.099/1995 e medidas protetivas na violência doméstica → 4704; Exame de corpo de delito para comprovar as lesões → 5545
Âncoras legais: CP, art. 129; Lei 9.099/1995, art. 88; Lei 11.340/2006, art. 41
Desempate: Escolha este nó quando o núcleo da questão for o tipo do art. 129 do CP. Se a lesão for só resultado qualificador de outro crime (roubo, tortura, maus-tratos), use o nó desse crime.
```

### 5079 · irmão parecido: 5087 Dos Crimes Contra a Administração Pública

```text
[5079] Penal > Dos Crimes Contra a Administração Judicial
Escopo: Crimes contra a administração da Justiça (CP, arts. 338 a 359): denunciação caluniosa, falso testemunho, fraude processual, favorecimentos, exercício arbitrário das próprias razões e outros tipos do capítulo.
Inclui: Visão geral e bem jurídico dos crimes contra a administração da Justiça; Comparação entre denunciação caluniosa, comunicação falsa de crime e autoacusação falsa; Coação no curso do processo (CP, art. 344), quando não estiver em subtema próprio; Fuga de pessoa presa, evasão mediante violência e arrebatamento de preso; Patrocínio infiel e exploração de prestígio; Questões que misturam vários tipos do capítulo
Não inclui: Prevaricação, corrupção e outros crimes de funcionário contra a Administração em geral → 5087; Calúnia como crime contra a honra → 5122; Abuso de autoridade (Lei 13.869/2019) → 4684; Requisitos, tipicidade e retratação do falso testemunho → 5081; Favorecimento pessoal e real e a distinção com a receptação → 5084
Âncoras legais: CP, arts. 338 a 359
Desempate: Use o nó-pai quando a questão comparar vários tipos do capítulo ou tratar de crime sem subtema próprio fora de 5086. Se a questão tratar de um único tipo com subtema, use esse subtema.
```

### 5082 · irmão parecido: 5085 Exercício Arbitrário ou Abuso de Poder

```text
[5082] Penal > Dos Crimes Contra a Administração Judicial > Exercício Arbitrário das Próprias Razões
Escopo: Crime de fazer justiça pelas próprias mãos para satisfazer pretensão, ainda que legítima, salvo quando a lei permite (CP, art. 345), e a figura correlata de tirar, suprimir, destruir ou danificar coisa própria em poder de terceiro (CP, art. 346).
Inclui: Elementos do tipo: pretensão legítima ou supostamente legítima satisfeita por meios próprios; Ressalva "salvo quando a lei o permite" (ex.: desforço imediato na posse); Ação penal privada quando não há violência e pública quando há violência; Cúmulo com a pena correspondente à violência; Coisa própria em poder de terceiro por determinação judicial ou convenção (art. 346); Distinção com furto, roubo e extorsão quando o agente busca crédito que entende devido
Não inclui: Exercício arbitrário ou abuso de poder por funcionário público (art. 350, revogado) → 5085; Subtração de coisa alheia móvel sem pretensão legítima → 5159; Constrangimento mediante violência ou grave ameaça para obter vantagem indevida → 5161; Condutas de autoridade pública tipificadas como abuso de autoridade → 4684; Regras gerais da ação penal privada no Código Penal → 5065
Âncoras legais: CP, art. 345; CP, art. 346
Desempate: Escolha este nó quando um particular satisfaz por conta própria uma pretensão que entende legítima; se o agente é funcionário que abusa do poder, use 5085 ou 4684.
```

### 5085 · irmão parecido: 5082 Exercício Arbitrário das Próprias Razões

```text
[5085] Penal > Dos Crimes Contra a Administração Judicial > Exercício Arbitrário ou Abuso de Poder
Escopo: Crime de exercício arbitrário ou abuso de poder do CP, art. 350, praticado por funcionário contra preso ou na execução de prisão ou diligência, e sua revogação expressa pela Lei 13.869/2019.
Inclui: Tipo do antigo art. 350 do CP e suas figuras equiparadas; Revogação expressa do art. 350 pela nova Lei de Abuso de Autoridade; Continuidade normativo-típica das condutas migradas para a Lei 13.869/2019; Questões de direito intertemporal sobre fatos praticados na vigência do art. 350
Não inclui: Análise dos tipos e regras da Lei 13.869/2019 (abuso de autoridade) → 4684; Fazer justiça pelas próprias mãos por particular → 5082; Violência arbitrária praticada no exercício da função (art. 322) → 5098; Regras gerais de abolitio criminis e lei penal no tempo → 5181
Âncoras legais: CP, art. 350; Lei 13.869/2019
Desempate: Use este nó só quando a questão tratar do art. 350 do CP ou de sua revogação; se cobrar os tipos atuais da Lei 13.869/2019, use 4684.
```

### 5087 · irmão parecido: 5079 Dos Crimes Contra a Administração Judicial

```text
[5087] Penal > Dos Crimes Contra a Administração Pública
Escopo: Crimes contra a Administração Pública do Título XI do CP, praticados por funcionário público ou por particular: peculato, concussão, corrupção, prevaricação, contrabando, descaminho, desacato e outros. Não inclui os crimes contra a administração da Justiça.
Inclui: Conceito penal de funcionário público e equiparado (CP, art. 327); Crimes funcionais próprios e impróprios; Distinção entre peculato, concussão e corrupção passiva; Reparação do dano como condição para progressão de regime (CP, art. 33, § 4º); Crimes praticados por particular contra a Administração; Questões que comparam vários tipos do título
Não inclui: Denunciação caluniosa, falso testemunho e favorecimentos → 5079; Conceito de funcionário público e noções gerais isoladas → 5088; Crimes de abuso de autoridade → 4684; Crimes contra as finanças públicas (CP, arts. 359-A a 359-H) → 5147; Sonegação fiscal da Lei 8.137/1990 → 4695; Perda do cargo como efeito da condenação → 5209
Âncoras legais: CP, arts. 312 a 337-A; CP, art. 327
Desempate: Use o nó-pai só quando a questão comparar vários crimes do título. Para conceitos gerais (funcionário público, crime funcional) use 5088 e, para um tipo específico, o subtema correspondente.
```

### 5097 · irmão parecido: 5098 Violência Arbitrária

```text
[5097] Penal > Dos Crimes Contra a Administração Pública > Advocacia Administrativa
Escopo: Advocacia administrativa (CP, art. 321): funcionário público que patrocina, direta ou indiretamente, interesse privado perante a Administração, valendo-se da qualidade de funcionário; inclui a forma qualificada pelo interesse ilegítimo.
Inclui: Patrocínio de interesse privado legítimo ou ilegítimo perante a Administração; Atuação direta ou por interposta pessoa (testa de ferro); Forma qualificada do parágrafo único (interesse ilegítimo); Desnecessidade de ser advogado ou de obter vantagem; Natureza de crime funcional próprio e de menor potencial ofensivo
Não inclui: Advocacia administrativa perante a administração fazendária (Lei 8.137/1990, art. 3º, III) → 4695; Particular que solicita vantagem a pretexto de influir em ato de funcionário → 5101; Funcionário que recebe vantagem indevida em razão da função → 5092; Funcionário que deixa de praticar ato de ofício para satisfazer interesse pessoal → 5095
Âncoras legais: CP, art. 321
Desempate: Escolha este nó quando o funcionário defende interesse alheio perante a Administração usando sua condição; se houver vantagem indevida pela função, use 5092; se o agente for particular alegando influência, use 5101.
```

### 5093 · irmão parecido: 5092 Corrupção Passiva

```text
[5093] Penal > Dos Crimes Contra a Administração Pública > Corrupção Ativa
Escopo: Corrupção ativa (CP, art. 333): particular que oferece ou promete vantagem indevida a funcionário público para determiná-lo a praticar, omitir ou retardar ato de ofício, incluindo a causa de aumento e a corrupção ativa em transação comercial internacional.
Inclui: Núcleos 'oferecer' e 'prometer' e consumação formal; Exceção pluralista à teoria monista em relação à corrupção passiva; Atipicidade da mera entrega após solicitação ou exigência do funcionário; Aumento de pena se o funcionário pratica, omite ou retarda o ato (parágrafo único); Oferta a policial para evitar prisão ou autuação; Corrupção ativa em transação comercial internacional (art. 337-B)
Não inclui: Funcionário que solicita, recebe ou aceita promessa de vantagem → 5092; Dar ou prometer vantagem a testemunha ou perito (art. 343) → 5081; Corrupção de menores para fins sexuais (CP, art. 218) → 5108; Compra de votos (Código Eleitoral, art. 299) → 4692
Âncoras legais: CP, art. 333; CP, art. 337-B
Desempate: Use este nó quando a conduta analisada é a do particular que oferece ou promete; quando é a do funcionário que solicita ou recebe, use 5092.
```

### 5092 · irmão parecido: 5093 Corrupção Ativa

```text
[5092] Penal > Dos Crimes Contra a Administração Pública > Corrupção Passiva
Escopo: Corrupção passiva (CP, art. 317): funcionário que solicita, recebe ou aceita promessa de vantagem indevida em razão da função, com a forma majorada (§ 1º) e a corrupção passiva privilegiada, por pedido ou influência de outrem (§ 2º).
Inclui: Núcleos 'solicitar', 'receber' e 'aceitar promessa'; Corrupção própria e imprópria; antecedente e subsequente; Ato de ofício e vantagem indevida; Majorante do § 1º: retarda, deixa de praticar ou pratica ato com infração de dever; Corrupção passiva privilegiada (§ 2º): cede a pedido ou influência; Independência em relação à corrupção ativa
Não inclui: Funcionário que exige a vantagem indevida → 5091; Particular que oferece ou promete vantagem → 5093; Omissão ou retardo de ato por interesse ou sentimento pessoal, sem vantagem nem pedido → 5095; Particular que solicita vantagem a pretexto de influir no funcionário → 5101; Facilitação de contrabando ou descaminho (art. 318) → 5094
Âncoras legais: CP, art. 317
Desempate: Use este nó para solicitar/receber/aceitar promessa de vantagem pelo funcionário, ou ceder a pedido/influência (§ 2º); se exigir, use 5091; se agir só por interesse ou sentimento pessoal, use 5095.
```

### 5098 · irmão parecido: 5097 Advocacia Administrativa

```text
[5098] Penal > Dos Crimes Contra a Administração Pública > Violência Arbitrária
Escopo: Violência arbitrária (CP, art. 322): praticar violência no exercício da função ou a pretexto de exercê-la, com cúmulo da pena correspondente à violência; inclui a discussão sobre sua revogação pelas leis de abuso de autoridade.
Inclui: Violência física contra pessoa no exercício ou a pretexto da função; Cúmulo material com a pena da violência (lesão corporal, homicídio); Debate sobre revogação tácita pela Lei 4.898/1965 e reflexos da Lei 13.869/2019; Crime funcional próprio
Não inclui: Crimes da Lei de Abuso de Autoridade (Lei 13.869/2019) → 4684; Tortura praticada por agente público (Lei 9.455/1997) → 4707; Tipificação e graus da lesão corporal resultante → 5077; Exercício arbitrário ou abuso de poder (art. 350) → 5085
Âncoras legais: CP, art. 322
Desempate: Use este nó quando a questão tratar do art. 322 do CP ou de sua vigência; se a conduta for enquadrada na Lei de Abuso de Autoridade ou na Lei de Tortura, use 4684 ou 4707.
```

### 5102 · irmão parecido: 5128 Dos Crimes Contra a Liberdade Pessoal

```text
[5102] Penal > Dos Crimes Contra a Dignidade Sexual
Escopo: Crimes contra a dignidade sexual (CP, arts. 213 a 234-B): estupro, violação sexual mediante fraude, importunação, assédio, registro não autorizado, crimes contra vulnerável, exploração sexual e disposições gerais.
Inclui: Bem jurídico (liberdade e dignidade sexual) e evolução após a Lei 12.015/2009; Comparação entre estupro, importunação sexual e violação sexual mediante fraude; Ação penal pública incondicionada (CP, art. 225); Causas de aumento de pena comuns (CP, arts. 226 e 234-A); Lenocínio, favorecimento da prostituição e ultraje público ao pudor; Questões que misturam vários tipos do título
Não inclui: Crimes de pornografia infantil do ECA (arts. 240 a 241-E) → 4709; Tráfico de pessoas para exploração sexual (CP, art. 149-A) → 5132; Corrupção de menores do ECA (art. 244-B) → 4709; Hediondez do estupro e do estupro de vulnerável → 4693; Elementos e consumação do estupro e do estupro de vulnerável → 5103
Âncoras legais: CP, arts. 213 a 234-B; Lei 12.015/2009
Desempate: Use o nó-pai quando a questão comparar tipos do título ou tratar do bem jurídico em geral. Se a questão tratar de um tipo ou das disposições gerais (arts. 225 a 234-B), use o subtema correspondente.
```

### 5106 · irmão parecido: 5105 Importunação Sexual

```text
[5106] Penal > Dos Crimes Contra a Dignidade Sexual > Assédio Sexual
Escopo: Crime de assédio sexual (CP, art. 216-A): constranger alguém para obter vantagem ou favorecimento sexual, valendo-se o agente da condição de superior hierárquico ou de ascendência inerentes a emprego, cargo ou função.
Inclui: Elementos do tipo do art. 216-A: constrangimento com fim de vantagem ou favorecimento sexual; Exigência de relação de superioridade hierárquica ou ascendência laboral (crime próprio); Discussão sobre assédio entre professor e aluno e entre colegas sem hierarquia; Causa de aumento de até um terço se a vítima é menor de 18 anos (art. 216-A, § 2º); Natureza formal do crime e momento consumativo; Distinção entre assédio sexual e assédio moral
Não inclui: Ato libidinoso sem anuência praticado contra alguém para satisfazer a própria lascívia, sem relação hierárquica → 5105; Constrangimento com violência ou grave ameaça para conjunção carnal ou outro ato libidinoso → 5103; Perseguição reiterada (stalking) sem relação de hierarquia → 5130; Ação penal e causas de aumento comuns aos crimes sexuais (arts. 225 e 226) → 5110
Âncoras legais: CP, art. 216-A
Desempate: Escolha este nó quando o constrangimento sexual se apoia na superioridade hierárquica ou ascendência de emprego, cargo ou função; sem essa relação, veja importunação (5105) ou estupro (5103).
```

### 5110 · irmão parecido: 5109 Outros Crimes Contra a Dignidade Sexual

```text
[5110] Penal > Dos Crimes Contra a Dignidade Sexual > Disposições Gerais dos Crimes Contra a Dignidade Sexual
Escopo: Normas comuns aos crimes contra a dignidade sexual: ação penal (art. 225), causas de aumento de pena gerais (arts. 226 e 234-A) e segredo de justiça (art. 234-B).
Inclui: Ação penal pública incondicionada nos crimes sexuais após a Lei 13.718/2018; Regime anterior da ação penal nos crimes sexuais e questões de direito intertemporal; Causas de aumento do art. 226 (concurso de agentes, estupro coletivo e corretivo, agente ascendente, padrasto, tutor, empregador etc.); Causas de aumento do art. 234-A (gravidez, transmissão de doença sexualmente transmissível, vítima idosa ou com deficiência); Segredo de justiça nos processos por crimes sexuais (art. 234-B)
Não inclui: Regras gerais da ação penal pública no Código Penal (art. 100) → 5064; Procedimento da ação penal pública incondicionada no CPP → 5470; Elementos típicos do estupro e do estupro de vulnerável → 5103; Natureza hedionda do estupro e do estupro de vulnerável → 4693; Aplicação genérica de causas de aumento na terceira fase da dosimetria → 5204
Âncoras legais: CP, art. 225; CP, art. 226; CP, art. 234-A; CP, art. 234-B
Desempate: Escolha este nó quando a questão tratar da ação penal ou das majorantes comuns dos crimes sexuais (arts. 225, 226, 234-A, 234-B); se tratar de elementar ou qualificadora de um tipo específico, use o nó desse crime.
```

### 5105 · irmão parecido: 5106 Assédio Sexual

```text
[5105] Penal > Dos Crimes Contra a Dignidade Sexual > Importunação Sexual
Escopo: Crime de importunação sexual (CP, art. 215-A, incluído pela Lei 13.718/2018): praticar contra alguém, sem a sua anuência, ato libidinoso com o objetivo de satisfazer a própria lascívia ou a de terceiro.
Inclui: Elementos do art. 215-A: ato libidinoso contra alguém, sem anuência; Subsidiariedade expressa: só se aplica se o ato não constitui crime mais grave; Casos típicos: ejaculação ou toques em transporte público; Revogação da contravenção de importunação ofensiva ao pudor (LCP, art. 61); Inaplicabilidade a vítima menor de 14 anos, segundo o STJ (configura estupro de vulnerável)
Não inclui: Ato libidinoso mediante violência ou grave ameaça, ou contra vulnerável → 5103; Ato obsceno em lugar público sem vítima determinada (art. 233) → 5109; Constrangimento sexual com abuso de ascendência hierárquica → 5106; Ato libidinoso obtido mediante fraude → 5104
Âncoras legais: CP, art. 215-A
Desempate: Escolha este nó quando houver ato libidinoso contra pessoa determinada sem a sua anuência, mas sem violência, grave ameaça, fraude ou vulnerabilidade; ato obsceno sem vítima dirigida é 5109.
```

### 5109 · irmão parecido: 5110 Disposições Gerais dos Crimes Contra a Dignidade Sexual

```text
[5109] Penal > Dos Crimes Contra a Dignidade Sexual > Outros Crimes Contra a Dignidade Sexual
Escopo: Crimes do Título VI do CP sem nó próprio: satisfação de lascívia na presença de criança ou adolescente, favorecimento da exploração sexual de vulnerável, divulgação de cena de estupro ou de nudez, lenocínio, casa de prostituição, rufianismo, promoção de migração ilegal e ultraje público ao pudor.
Inclui: Satisfação de lascívia mediante presença de criança ou adolescente (art. 218-A); Favorecimento da prostituição ou outra forma de exploração sexual de criança, adolescente ou vulnerável (art. 218-B); Divulgação de cena de estupro, de sexo, nudez ou pornografia sem consentimento, incluída a pornografia de vingança (art. 218-C); Mediação para servir à lascívia de outrem, favorecimento da prostituição, casa de prostituição e rufianismo (arts. 227 a 230); Promoção de migração ilegal (art. 232-A); Ato obsceno e escrito ou objeto obsceno (arts. 233 e 234)
Não inclui: Induzir menor de 14 anos a satisfazer a lascívia de outrem (art. 218) → 5108; Produzir, fotografar ou registrar cena de nudez ou de ato sexual sem autorização (art. 216-B) → 5107; Tráfico de pessoas para fins de exploração sexual (art. 149-A) → 5132; Pornografia infantojuvenil prevista no ECA (arts. 240 a 241-E) → 4709; Ato libidinoso dirigido a vítima determinada sem anuência → 5105
Âncoras legais: CP, art. 218-A; CP, art. 218-B; CP, art. 218-C; CP, arts. 227 a 230; CP, art. 232-A; CP, art. 233; CP, art. 234
Desempate: Use este nó só para os crimes do Título VI que não têm subtema próprio; se o tipo for o dos arts. 213, 215, 215-A, 216-A, 216-B, 217-A ou 218, use o nó específico.
```

### 5107 · irmão parecido: 5109 Outros Crimes Contra a Dignidade Sexual

```text
[5107] Penal > Dos Crimes Contra a Dignidade Sexual > Registro Não Autorizado da Intimidade Sexual
Escopo: Crime de registro não autorizado da intimidade sexual (CP, art. 216-B, incluído pela Lei 13.772/2018): produzir, fotografar, filmar ou registrar, por qualquer meio, conteúdo com cena de nudez ou ato sexual ou libidinoso de caráter íntimo e privado sem autorização dos participantes.
Inclui: Condutas de produzir, fotografar, filmar ou registrar cena íntima sem autorização; Figura equiparada da montagem para incluir pessoa em cena de nudez ou ato sexual (art. 216-B, parágrafo único); Natureza de infração de menor potencial ofensivo; Distinção entre registrar (art. 216-B) e divulgar (art. 218-C)
Não inclui: Divulgação, venda ou transmissão de cena de sexo, nudez ou estupro (art. 218-C) → 5109; Registro de cena de sexo envolvendo criança ou adolescente (ECA, art. 240) → 4709; Invasão de dispositivo informático para obter dados ou imagens (art. 154-A) → 5133; Violência psicológica contra a mulher (art. 147-B) → 5131
Âncoras legais: CP, art. 216-B
Desempate: Escolha este nó quando a conduta for registrar ou montar a cena íntima; se a conduta for divulgar ou compartilhar o conteúdo, use 5109 (art. 218-C).
```

### 5104 · irmão parecido: 5105 Importunação Sexual

```text
[5104] Penal > Dos Crimes Contra a Dignidade Sexual > Violação Sexual Mediante Fraude
Escopo: Crime de violação sexual mediante fraude (CP, art. 215): ter conjunção carnal ou praticar outro ato libidinoso com alguém mediante fraude ou outro meio que impeça ou dificulte a livre manifestação de vontade da vítima.
Inclui: Estelionato sexual: fraude que vicia o consentimento da vítima; Casos típicos: falso médico, falso líder espiritual, engano sobre a identidade do parceiro; Meio que dificulta (sem anular) a manifestação de vontade; Multa cumulativa quando há fim de obter vantagem econômica (art. 215, parágrafo único); Distinção entre fraude (art. 215) e anulação da capacidade de resistir (art. 217-A, § 1º)
Não inclui: Vítima que não pode oferecer resistência, como a dopada ou desacordada (art. 217-A, § 1º) → 5103; Ato libidinoso sem anuência e sem fraude (art. 215-A) → 5105; Fraude para obter vantagem patrimonial ilícita (art. 171) → 5166; Ação penal e majorantes comuns dos crimes sexuais → 5110
Âncoras legais: CP, art. 215
Desempate: Escolha este nó quando a vítima consente por engano ou tem a vontade apenas dificultada; se a capacidade de resistir foi eliminada, use 5103 (estupro de vulnerável).
```

### 5116 · irmão parecido: 5144 Dos Crimes Contra a Saúde Pública e Dos Crimes Contra à Paz Pública

```text
[5116] Penal > Dos Crimes Contra a Fé Pública e de Falsidade Documental
Escopo: Crimes contra a fé pública (CP, arts. 289 a 311-A): moeda falsa, falsificação de títulos e papéis públicos, falsidade documental, falsidade ideológica, uso de documento falso e outras falsidades.
Inclui: Fé pública como bem jurídico; Distinção entre falsidade material e falsidade ideológica; Moeda falsa e crimes assimilados; Uso de documento falso e o conflito com a falsificação; Falsa identidade e fraudes em certames de interesse público; Falsificação grosseira e crime impossível ou estelionato
Não inclui: Estelionato com uso de documento falso (Súmula 17 do STJ) → 5166; Falso testemunho e falsa perícia → 5081; Incidente de falsidade documental no processo → 5497; Falsidade ideológica eleitoral (Código Eleitoral, art. 350) → 4692; Falsificação de documento público e particular → 5118
Âncoras legais: CP, arts. 289 a 311-A
Desempate: Use o nó-pai quando a questão percorrer vários capítulos do título. Para o conceito de fé pública use 5117, para a falsidade documental 5118 e para as demais falsidades 5119.
```

### 5118 · irmão parecido: 5119 De outras falsidades

```text
[5118] Penal > Dos Crimes Contra a Fé Pública e de Falsidade Documental > Da Falsidade Documental
Escopo: Crimes do Capítulo III do Título X do CP (arts. 296 a 305): falsificação de selo ou sinal público, falsificação de documento público e particular, falsidade ideológica, falso reconhecimento de firma, certidão ou atestado falso, uso e supressão de documento.
Inclui: Falsificação de documento público e documentos equiparados (art. 297, § 2º); Falsificação de documento particular, inclusive cartão de crédito ou débito (art. 298, parágrafo único); Falsidade material x falsidade ideológica (art. 299); Certidão ou atestado ideologicamente falso e falsidade de atestado médico (arts. 301 e 302); Uso de documento falso (art. 304) e competência conforme o órgão a que foi apresentado; Supressão de documento (art. 305); Falsificação de selo ou sinal público e falso reconhecimento de firma (arts. 296 e 300)
Não inclui: Falsa identidade, uso de documento de identidade alheio e adulteração de sinal identificador de veículo → 5119; Moeda falsa, falsificação de papéis públicos e conceito/requisitos gerais do falso (imitação da verdade, dano potencial) → 5117; Falso usado como meio para estelionato e absorção pela Súmula 17 do STJ → 5166; Incidente de falsidade documental no processo → 5497; Falsidade ideológica para fins eleitorais (Código Eleitoral) → 4692; Falso como meio de supressão ou redução de tributo → 4695
Âncoras legais: CP, arts. 296 a 305; STJ, Súmula 17; STJ, Súmula 546
Desempate: Escolha este nó quando o objeto material do falso for um documento (público ou particular), selo ou sinal público, atestado ou certidão; se a conduta consistir em se atribuir identidade falsa sem apresentar documento falsificado, ou em adulterar sinal de veículo, use 5119.
```

### 5119 · irmão parecido: 5118 Da Falsidade Documental

```text
[5119] Penal > Dos Crimes Contra a Fé Pública e de Falsidade Documental > De outras falsidades
Escopo: Crimes do Capítulo IV do Título X do CP (arts. 306 a 311): falsificação de sinal usado em contraste de metal precioso, falsa identidade, uso de documento de identidade alheio, fraudes de lei sobre estrangeiro e adulteração de sinal identificador de veículo.
Inclui: Falsa identidade (art. 307), inclusive perante autoridade policial em autodefesa (Súmula 522 do STJ); Uso, como próprio, de documento de identidade alheio ou cessão de documento próprio (art. 308); Fraude de lei sobre estrangeiro (arts. 309 e 310); Adulteração de sinal identificador de veículo (art. 311) e figuras equiparadas; Falsificação de sinal empregado no contraste de metal precioso ou na fiscalização alfandegária (art. 306)
Não inclui: Uso de documento falso, ainda que de identidade falsificada (art. 304) → 5118; Fraudes em certames de interesse público (art. 311-A) e moeda falsa → 5117; Receptação de veículo com sinal adulterado → 5169; Identificação criminal do civilmente identificado → 4699
Âncoras legais: CP, arts. 306 a 311; STJ, Súmula 522
Desempate: Escolha este nó quando a conduta for atribuir-se ou atribuir a terceiro falsa identidade, usar documento de identidade verdadeiro alheio ou adulterar sinal de veículo; se houver falsificação ou uso de documento falsificado, use 5118.
```

### 5120 · irmão parecido: 5149 Dos Crimes Contra a Vida

```text
[5120] Penal > Dos Crimes Contra a Honra
Escopo: Crimes contra a honra (CP, arts. 138 a 145): calúnia, difamação, injúria e as disposições comuns, como causas de aumento, exclusão do crime, retratação, pedido de explicações e ação penal.
Inclui: Honra objetiva e honra subjetiva; Distinção entre calúnia, difamação e injúria; Exceção da verdade e exceção de notoriedade; Retratação (CP, art. 143) e pedido de explicações (CP, art. 144); Ação penal nos crimes contra a honra (CP, art. 145); Causas de aumento (CP, art. 141)
Não inclui: Denunciação caluniosa (CP, art. 339) → 5080; Injúria racial e crimes da Lei 7.716/1989 → 4690; Crimes contra a honra na propaganda eleitoral → 4692; Desacato a funcionário público → 5100; Procedimento especial dos crimes contra a honra (CPP, arts. 519 a 523) → 5538
Âncoras legais: CP, arts. 138 a 145
Desempate: Use o nó-pai quando a questão comparar calúnia, difamação e injúria entre si. Para um único tipo use 5122, 5123 ou 5124 e, para as regras comuns (arts. 141 a 145), use 5121.
```

### 5125 · irmão parecido: 5147 Dos Crimes contra as Finanças Públicas

```text
[5125] Penal > Dos Crimes Contra a Incolumidade Pública
Escopo: Crimes contra a incolumidade pública dos arts. 250 a 266 do CP: crimes de perigo comum (incêndio, explosão, desabamento etc.) e crimes contra a segurança dos meios de comunicação, de transporte e de outros serviços públicos. Na árvore, os crimes contra a saúde pública ficam em outro nó.
Inclui: Incolumidade pública como bem jurídico coletivo; Crimes de perigo comum: perigo concreto e perigo abstrato; Incêndio, explosão, inundação e desabamento; Atentado contra a segurança de transporte e de serviços de utilidade pública; Formas qualificadas pelo resultado (CP, arts. 258 e 263)
Não inclui: Epidemia, envenenamento de água e falsificação de medicamentos → 5145; Porte e disparo de arma de fogo → 4697; Crimes de trânsito do CTB → 4691; Perigo para a vida ou a saúde de pessoa determinada (CP, art. 132) → 5140; Interrupção de serviços essenciais → 5156
Âncoras legais: CP, arts. 250 a 266
Desempate: Use o nó-pai quando a questão tratar do conceito de incolumidade pública ou abarcar os dois capítulos. Se envolver perigo para pessoa determinada, use Periclitação da Vida e da Saúde (5138).
```

### 5128 · irmão parecido: 5102 Dos Crimes Contra a Dignidade Sexual

```text
[5128] Penal > Dos Crimes Contra a Liberdade Pessoal
Escopo: Crimes contra a liberdade individual (CP, arts. 146 a 154-B): constrangimento ilegal, bullying, ameaça, perseguição, violência psicológica contra a mulher, sequestro, redução à condição análoga à de escravo, tráfico de pessoas e crimes contra a inviolabilidade. O constrangimento ilegal não tem subtema próprio.
Inclui: Constrangimento ilegal e suas excludentes (CP, art. 146, § 3º); Liberdade individual como bem jurídico; Comparação entre ameaça, constrangimento ilegal e sequestro; Questões que misturam vários crimes do capítulo; Violação de dispositivo informático (CP, art. 154-A) em visão geral do capítulo
Não inclui: Extorsão mediante sequestro (CP, art. 159) → 5161; Tortura (Lei 9.455/1997) → 4707; Estupro como constrangimento à prática sexual → 5103; Perseguição (stalking) e ameaça → 5130; Violação de domicílio, de correspondência e de segredos → 5133; Medidas protetivas da Lei Maria da Penha → 4704
Âncoras legais: CP, arts. 146 a 154-B
Desempate: Use o nó-pai para o constrangimento ilegal (sem subtema próprio) e para questões que comparam vários crimes do capítulo. Para os demais tipos, use o subtema.
```

### 5138 · irmão parecido: 5149 Dos Crimes Contra a Vida

```text
[5138] Penal > Dos Crimes Contra a Periclitação da Vida e da Saúde
Escopo: Crimes de periclitação da vida e da saúde (CP, arts. 130 a 136): crimes de perigo individual, como contágio venéreo, contágio de moléstia grave, perigo para a vida de outrem, abandono de incapaz, exposição de recém-nascido, omissão de socorro e maus-tratos.
Inclui: Natureza de crimes de perigo, concreto ou abstrato, contra pessoa determinada; Dolo de perigo e distinção do dolo de dano; Formas qualificadas pelo resultado lesão grave ou morte; Condicionamento de atendimento médico-hospitalar emergencial (CP, art. 135-A); Questões que comparam vários tipos do capítulo
Não inclui: Crimes de perigo comum contra número indeterminado de pessoas → 5126; Maus-tratos contra idoso (Estatuto da Pessoa Idosa) → 4696; Omissão de socorro no trânsito (CTB, art. 304) → 4691; Tortura-castigo contra pessoa sob guarda (Lei 9.455/1997, art. 1º, II) → 4707; Crimes omissivos impróprios e o dever de garante → 5223
Âncoras legais: CP, arts. 130 a 136
Desempate: Use o nó-pai quando a questão tratar das características gerais dos crimes de perigo individual ou de tipo sem subtema (CP, art. 135-A). Para os demais tipos, use o subtema.
```

### 5144 · irmão parecido: 5116 Dos Crimes Contra a Fé Pública e de Falsidade Documental

```text
[5144] Penal > Dos Crimes Contra a Saúde Pública e Dos Crimes Contra à Paz Pública
Escopo: Crimes contra a saúde pública (CP, arts. 267 a 285) e crimes contra a paz pública (CP, arts. 286 a 288-A): epidemia, envenenamento, falsificação de produtos terapêuticos, incitação e apologia ao crime, associação criminosa e milícia privada.
Inclui: Epidemia, infração de medida sanitária preventiva e falsificação de medicamentos; Exercício ilegal da medicina e charlatanismo; Incitação ao crime e apologia de crime ou criminoso; Associação criminosa (CP, art. 288) e constituição de milícia privada (CP, art. 288-A); Questões que tratam dos dois capítulos em conjunto
Não inclui: Tráfico de drogas e associação para o tráfico (Lei 11.343/2006) → 4708; Organização criminosa (Lei 12.850/2013) → 4705; Crimes de perigo comum, como incêndio e explosão → 5126; Concurso eventual de pessoas, distinto da associação criminosa → 5071; Crimes contra as relações de consumo do CDC → 4694
Âncoras legais: CP, arts. 267 a 285; CP, arts. 286 a 288-A
Desempate: Use o nó-pai só quando a questão abranger os dois capítulos. Para a saúde pública use 5145 e, para a paz pública (incluindo associação criminosa e milícia), use 5146.
```

### 5146 · irmão parecido: 5145 Dos Crimes Contra a Saúde Pública

```text
[5146] Penal > Dos Crimes Contra a Saúde Pública e Dos Crimes Contra à Paz Pública > Crimes Contra à Paz Pública
Escopo: Crimes do Título IX da Parte Especial do CP (crimes contra a paz pública): incitação ao crime, apologia de crime ou criminoso, associação criminosa e constituição de milícia privada.
Inclui: Incitação ao crime (art. 286), inclusive a incitação à animosidade entre as Forças Armadas e os Poderes ou instituições (parágrafo único); Apologia de crime ou criminoso (art. 287); Associação criminosa: 3 ou mais pessoas, para fim específico de cometer crimes, com estabilidade e permanência (art. 288); Aumento de pena da associação criminosa armada ou com participação de criança ou adolescente (art. 288, parágrafo único); Constituição de milícia privada (art. 288-A); Natureza formal e de perigo abstrato; autonomia da associação criminosa em relação aos crimes praticados (concurso material)
Não inclui: Organização criminosa (4 ou mais pessoas, Lei 12.850/2013), colaboração premiada e infiltração previstas nessa lei → 4705; Associação para o tráfico (Lei 11.343/2006, art. 35) → 4708; Associação para praticar genocídio (Lei 2.889/1956) → 4698; Incitação à discriminação ou preconceito de raça, cor, etnia, religião ou procedência nacional (Lei 7.716/1989, art. 20) → 4690; Atos de terrorismo e organização terrorista (Lei 13.260/2016) → 4706; Crimes contra o Estado Democrático de Direito (CP, arts. 359-I a 359-T) → 5155
Âncoras legais: CP, art. 286; CP, art. 287; CP, art. 288; CP, art. 288-A
Desempate: Use este nó quando a questão tratar de associação de 3 ou mais pessoas para crimes em geral (CP, art. 288) ou de milícia privada; se for associação estruturada de 4 ou mais pessoas com divisão de tarefas (Lei 12.850/2013) ou associação para o tráfico, use 4705 ou 4708.
```

### 5145 · irmão parecido: 5146 Crimes Contra à Paz Pública

```text
[5145] Penal > Dos Crimes Contra a Saúde Pública e Dos Crimes Contra à Paz Pública > Dos Crimes Contra a Saúde Pública
Escopo: Crimes contra a saúde pública do CP (Título VIII, Capítulo III): epidemia, infração de medida sanitária, envenenamento e corrupção de água e alimentos, falsificação de produtos terapêuticos ou medicinais, exercício ilegal da medicina, charlatanismo e curandeirismo.
Inclui: Epidemia (art. 267), incluindo a forma com resultado morte, que é hedionda; Infração de medida sanitária preventiva (art. 268) e omissão de notificação de doença (art. 269); Envenenamento, corrupção ou poluição de água potável e de substância alimentícia ou medicinal (arts. 270 a 272); Falsificação, corrupção, adulteração ou alteração de produto destinado a fins terapêuticos ou medicinais (art. 273) e a desproporcionalidade da pena do § 1º-B reconhecida pelo STF; Outras substâncias nocivas, medicamento em desacordo com receita médica (arts. 274 a 281); Exercício ilegal da medicina, arte dentária ou farmacêutica, charlatanismo e curandeirismo (arts. 282 a 284); Forma qualificada pelo resultado lesão grave ou morte (art. 285 c/c art. 258)
Não inclui: Tráfico, porte para consumo e demais crimes envolvendo drogas (Lei 11.343/2006) → 4708; Incêndio, explosão, inundação, uso de gás tóxico e demais crimes de perigo comum (CP, arts. 250 a 259) → 5126; Atentado contra a segurança de transporte ou de serviço de utilidade pública (CP, arts. 260 a 266) → 5127; Perigo de contágio venéreo ou de moléstia grave a pessoa determinada (CP, arts. 130 e 131) → 5139; Crimes contra as relações de consumo e contra o consumidor (CDC) → 4694; Rol e regime jurídico dos crimes hediondos (Lei 8.072/1990) tratados em si → 4693
Âncoras legais: CP, arts. 267 a 285; CP, art. 273; CP, art. 282; CP, art. 284
Desempate: Use este nó quando o bem jurídico for a saúde de número indeterminado de pessoas e o tipo estiver nos arts. 267 a 285 do CP; se o perigo recair sobre pessoa determinada, use 5139 ou 5140; se a substância for droga ilícita da Lei 11.343/2006, use 4708.
```

### 5149 · irmão parecido: 5111 Dos Crimes contra a Família

```text
[5149] Penal > Dos Crimes Contra a Vida
Escopo: Crimes dolosos contra a vida (CP, arts. 121 a 128): homicídio, feminicídio, induzimento, instigação ou auxílio ao suicídio e à automutilação, infanticídio e aborto.
Inclui: Vida humana como bem jurídico: início da vida e marcos entre aborto, infanticídio e homicídio; Comparação entre os tipos do capítulo; Competência do Tribunal do Júri para crimes dolosos contra a vida (CF, art. 5º, XXXVIII, d) em visão material; Hediondez dos crimes contra a vida em visão geral; Questões que misturam vários tipos do capítulo
Não inclui: Homicídio qualificado, privilegiado e culposo → 5150; Homicídio culposo na direção de veículo (CTB, art. 302) → 4691; Latrocínio (CP, art. 157, § 3º, II) → 5160; Lesão corporal seguida de morte → 5077; Procedimento bifásico do Júri, pronúncia e impronúncia → 5526; Genocídio (Lei 2.889/1956) → 4698
Âncoras legais: CP, arts. 121 a 128; CP, art. 121-A; CF, art. 5º, XXXVIII
Desempate: Use o nó-pai quando a questão comparar tipos do capítulo ou tratar do bem jurídico vida em geral. Para um tipo específico, use o subtema.
```

### 5151 · irmão parecido: 5150 Homicídio

```text
[5151] Penal > Dos Crimes Contra a Vida > Feminicídio
Escopo: Feminicídio: matar mulher por razões da condição do sexo feminino. Desde a Lei 14.994/2024 é crime autônomo (CP, art. 121-A), com causas de aumento próprias e natureza hedionda.
Inclui: Tipo autônomo do art. 121-A (Lei 14.994/2024) e a revogação da antiga qualificadora do art. 121, § 2º, VI; Razões da condição de sexo feminino: violência doméstica e familiar, menosprezo ou discriminação à condição de mulher; Causas de aumento: gestação ou pós-parto, vítima menor de 14 ou maior de 60 anos ou com deficiência, presença de descendente ou ascendente, descumprimento de medida protetiva; Natureza objetiva ou subjetiva das razões de gênero e compatibilidade com o privilégio e com as qualificadoras; Comunicabilidade das circunstâncias pessoais aos coautores e partícipes; Hediondez e direito intertemporal entre a qualificadora e o crime autônomo
Não inclui: Homicídio de vítima mulher sem razões da condição do sexo feminino → 5150; Medidas protetivas e demais regras da Lei 11.340/2006 em si → 4704; Crime de violência psicológica contra a mulher (art. 147-B) → 5131; Rol e consequências gerais da Lei dos Crimes Hediondos → 4693; Lesão corporal praticada contra a mulher por razões do sexo feminino → 5077
Âncoras legais: CP, art. 121-A; Lei 8.072/1990, art. 1º, I-B; Lei 14.994/2024; Lei 11.340/2006, art. 5º
Desempate: Se a morte da mulher se deu por razões da condição do sexo feminino (violência doméstica ou familiar, menosprezo ou discriminação), classifique aqui e não em Homicídio (5150), mesmo que a questão se refira à antiga qualificadora do art. 121.
```

### 5150 · irmão parecido: 5151 Feminicídio

```text
[5150] Penal > Dos Crimes Contra a Vida > Homicídio
Escopo: Homicídio do art. 121 do CP: formas simples, privilegiada, qualificada e culposa, causas de aumento, perdão judicial no homicídio culposo e hediondez do homicídio qualificado.
Inclui: Homicídio simples e momento da morte (morte encefálica); Homicídio privilegiado (relevante valor social ou moral, violenta emoção logo após injusta provocação); Qualificadoras: motivo torpe ou fútil, meio cruel, recurso que dificulta a defesa, conexão, vítima agente de segurança, arma de uso restrito etc.; Homicídio qualificado-privilegiado e natureza objetiva ou subjetiva das qualificadoras; Homicídio culposo, majorantes do § 4º e perdão judicial do § 5º; Aumento por milícia privada ou grupo de extermínio e homicídio contra menor de 14 anos; Hediondez do homicídio qualificado e do praticado em atividade de grupo de extermínio
Não inclui: Morte de mulher por razões da condição do sexo feminino → 5151; Homicídio culposo na direção de veículo automotor (CTB, art. 302) → 4691; Lesão corporal seguida de morte (art. 129, § 3º) → 5077; Latrocínio (roubo com resultado morte) → 5160; Pronúncia, quesitos e julgamento do homicídio pelo júri → 5527; Perdão judicial como causa extintiva da punibilidade em geral → 5197
Âncoras legais: CP, art. 121; Lei 8.072/1990, art. 1º, I; CF, art. 5º, XXXVIII
Desempate: Use este nó para a morte dolosa ou culposa de pessoa nascida que não se encaixe em tipo específico; se houver razões de gênero, use Feminicídio (5151); se a autora for a mãe sob estado puerperal, use Infanticídio (5153).
```

### 5153 · irmão parecido: 5151 Feminicídio

```text
[5153] Penal > Dos Crimes Contra a Vida > Infanticídio
Escopo: Infanticídio do art. 123 do CP: matar a mãe o próprio filho, sob influência do estado puerperal, durante o parto ou logo após, incluindo o concurso de terceiros e as hipóteses de erro.
Inclui: Elementares: mãe como sujeito ativo, próprio filho, estado puerperal, durante o parto ou logo após; Crime próprio e critério fisiopsicológico do estado puerperal; Concurso de pessoas e comunicabilidade da elementar do estado puerperal ao terceiro (art. 30); Erro sobre a pessoa: mãe que mata outro recém-nascido pensando ser o próprio filho; Distinção entre infanticídio, aborto e homicídio conforme o momento da conduta; Inexistência de forma culposa de infanticídio
Não inclui: Conduta praticada antes do início do parto contra o feto → 5154; Exposição ou abandono de recém-nascido para ocultar desonra própria (art. 134) → 5141; Comunicabilidade de circunstâncias e elementares em tese, sem foco no infanticídio → 5076; Morte do filho pela mãe fora do estado puerperal → 5150
Âncoras legais: CP, art. 123; CP, art. 30; CP, art. 20, § 3º
Desempate: Escolha este nó quando a morte do filho pela mãe, ou a participação de terceiro nela, ocorrer durante o parto ou logo após, sob influência do estado puerperal; se for antes do parto, use Aborto (5154); se faltar o estado puerperal, use Homicídio (5150).
```

### 5157 · irmão parecido: 5111 Dos Crimes contra a Família

```text
[5157] Penal > Dos Crimes Contra o Patrimônio
Escopo: Crimes contra o patrimônio (CP, arts. 155 a 183): furto, roubo, extorsão, usurpação, dano, apropriação indébita, estelionato, receptação e as disposições gerais (imunidades).
Inclui: Distinção entre furto, roubo, extorsão, estelionato e apropriação indébita; Patrimônio como bem jurídico e princípio da insignificância nos crimes patrimoniais; Questões que misturam vários tipos do título; Momento consumativo nos crimes patrimoniais em visão comparativa
Não inclui: Imunidades absolutas e relativas (CP, arts. 181 a 183) → 5158; Peculato e apropriação por funcionário público → 5089; Lavagem de dinheiro como crime acessório → 4702; Crimes contra a economia popular → 4687; Favorecimento real (CP, art. 349), distinto da receptação → 5084; Hediondez do latrocínio e da extorsão mediante sequestro → 4693
Âncoras legais: CP, arts. 155 a 183
Desempate: Use o nó-pai só quando a questão comparar vários crimes patrimoniais sem se centrar em um deles. Para um tipo específico ou para as imunidades (5158), use o subtema.
```

### 5169 · irmão parecido: 5163 Usurpação

```text
[5169] Penal > Dos Crimes Contra o Patrimônio > Receptação
Escopo: Crimes de receptação do CP: receptação própria e imprópria, qualificada no exercício de atividade comercial, culposa, majorada por bens públicos, perdão judicial e privilégio, e receptação de animal (art. 180-A).
Inclui: Receptação própria e imprópria (art. 180, caput); Receptação qualificada no exercício de atividade comercial ou industrial (§ 1º) e equiparação (§ 2º); Receptação culposa (§ 3º) e perdão judicial (§ 5º); Autonomia: punição ainda que o autor do crime anterior seja desconhecido ou isento de pena (§ 4º); Receptação de bens públicos (§ 6º); Receptação de animal (art. 180-A)
Não inclui: Auxílio para tornar seguro o proveito do crime sem fim de lucro próprio (favorecimento real) → 5084; Ocultação ou dissimulação de bens provenientes de infração penal (lavagem de dinheiro) → 4702; Perdão judicial como causa geral de extinção da punibilidade → 5197; Aquisição ou ocultação de arma de fogo de origem ilícita (Estatuto do Desarmamento) → 4697
Âncoras legais: CP, art. 180; CP, art. 180-A
Desempate: Escolha este nó quando o agente adquirir, receber, ocultar ou conduzir produto de crime em proveito próprio ou alheio; se a finalidade for só ajudar o autor do crime a garantir o proveito, escolha Favorecimento Real (5084).
```

### 5163 · irmão parecido: 5169 Receptação

```text
[5163] Penal > Dos Crimes Contra o Patrimônio > Usurpação
Escopo: Crimes de usurpação dos arts. 161 e 162 do CP: alteração de limites, usurpação de águas e supressão ou alteração de marca em animais; o esbulho possessório (art. 161, § 1º, II) tem nó próprio.
Inclui: Alteração de limites: suprimir ou deslocar tapume, marco ou sinal divisório para apropriar-se de imóvel alheio (art. 161, caput); Usurpação de águas: desviar ou represar águas alheias (art. 161, § 1º, I); Supressão ou alteração de marca ou sinal indicativo de propriedade em gado ou rebanho (art. 162); Concurso com a pena da violência e ação penal privada (art. 161, §§ 2º e 3º)
Não inclui: Invasão de terreno ou edifício alheio para fins de esbulho → 5162; Usurpação de função pública (art. 328) → 5099; Furto de semovente domesticável de produção (art. 155, § 6º) → 5159; Introdução ou abandono de animais em propriedade alheia (art. 164) → 5164
Âncoras legais: CP, art. 161, caput e § 1º, I; CP, art. 161, §§ 2º e 3º; CP, art. 162
Desempate: Escolha este nó para alteração de limites, usurpação de águas ou supressão de marca em animais; se a questão tratar da invasão de imóvel com fim de esbulho, escolha Esbulho Possessório (5162).
```

### 5111 · irmão parecido: 5149 Dos Crimes Contra a Vida

```text
[5111] Penal > Dos Crimes contra a Família
Escopo: Crimes contra a família (CP, arts. 235 a 249): crimes contra o casamento, contra o estado de filiação, contra a assistência familiar e contra o pátrio poder (poder familiar), a tutela e a curatela.
Inclui: Família como bem jurídico tutelado; Bigamia e induzimento a erro essencial; Registro de filho alheio e parto suposto; Abandono material e abandono intelectual; Subtração de incapazes; Questões que comparam crimes de capítulos diferentes do título
Não inclui: Abandono de incapaz e exposição de recém-nascido (CP, arts. 133 e 134) → 5141; Crimes do ECA contra criança e adolescente → 4709; Violência doméstica e familiar contra a mulher (Lei 11.340/2006) → 4704; Imunidade entre cônjuges e parentes nos crimes patrimoniais → 5158; Abandono de pessoa idosa (Estatuto da Pessoa Idosa) → 4696
Âncoras legais: CP, arts. 235 a 249
Desempate: Use o nó-pai só quando a questão abranger mais de um capítulo do título. Nos demais casos, use o subtema do capítulo do crime (5112, 5113, 5114 ou 5115).
```

### 5114 · irmão parecido: 5113 Dos Crimes Contra o Estado de Filiação

```text
[5114] Penal > Dos Crimes contra a Família > Dos Crimes Contra a Assistência Familiar
Escopo: Crimes contra a assistência familiar do CP (arts. 244 a 247): abandono material, entrega de filho menor a pessoa inidônea, abandono intelectual e permissão para que menor frequente ambientes ou atividades que o pervertam.
Inclui: Abandono material: deixar de prover a subsistência do cônjuge, de filho menor ou inapto para o trabalho, de ascendente inválido ou maior de 60 anos; Abandono material por não pagamento de pensão alimentícia fixada, acordada ou majorada, sem justa causa; Frustração ou ilisão do pagamento de pensão por quem é solvente, inclusive abandonando emprego (art. 244, parágrafo único); Entrega de filho menor a pessoa em cuja companhia saiba ou deva saber que fica moral ou materialmente em perigo (art. 245) e as formas qualificadas; Abandono intelectual: deixar de prover, sem justa causa, a instrução primária de filho em idade escolar (art. 246); Permitir que menor frequente casa de jogo, conviva com pessoa viciosa, assista a espetáculo capaz de pervertê-lo ou mendigue (art. 247)
Não inclui: Abandono de incapaz e exposição ou abandono de recém-nascido (CP, arts. 133 e 134) → 5141; Maus-tratos a pessoa sob autoridade, guarda ou vigilância (CP, art. 136) → 5143; Abandono de idoso e omissão de assistência previstos no Estatuto do Idoso → 4696; Crimes do ECA contra criança e adolescente, como corrupção de menores do art. 244-B → 4709; Subtração de incapaz ou sonegação de incapaz a quem tem a guarda (CP, arts. 248 e 249) → 5115
Âncoras legais: CP, art. 244; CP, art. 245; CP, art. 246; CP, art. 247
Desempate: Escolha este nó quando o núcleo da questão for o descumprimento do dever de sustento, de educação ou de proteção moral do familiar; quando houver deixar a vítima em situação de perigo concreto à vida ou à saúde, use 5141 ou 5143.
```

### 5112 · irmão parecido: 5113 Dos Crimes Contra o Estado de Filiação

```text
[5112] Penal > Dos Crimes contra a Família > Dos Crimes Contra o Casamento
Escopo: Crimes contra o casamento do CP (arts. 235 a 239): bigamia, induzimento a erro essencial e ocultação de impedimento, conhecimento prévio de impedimento, simulação de autoridade para celebração e simulação de casamento, além da revogação do adultério (art. 240).
Inclui: Bigamia: contrair novo casamento sendo casado e punição de quem, não sendo casado, casa com pessoa casada sabendo dessa circunstância; Extinção da bigamia pela anulação do casamento anterior ou do posterior por motivo diverso da bigamia (art. 235, § 2º); Induzimento a erro essencial e ocultação de impedimento, com ação penal privativa do contraente enganado e dependente do trânsito em julgado da sentença de anulação (art. 236); Contrair casamento conhecendo impedimento que gere nulidade absoluta (art. 237); Simulação de autoridade para celebração de casamento e simulação de casamento (arts. 238 e 239); Abolitio criminis do adultério pela Lei 11.106/2005
Não inclui: Falsidade ideológica em documentos do processo de habilitação ou em registro público (CP, art. 299) → 5118; Usurpação de função pública fora da celebração de casamento (CP, art. 328) → 5099; Registro de nascimento inexistente ou parto suposto (CP, arts. 241 e 242) → 5113; Efeitos gerais da abolitio criminis sobre a punibilidade (CP, art. 107, III) → 5194
Âncoras legais: CP, art. 235; CP, art. 236; CP, art. 237; CP, art. 238; CP, art. 239; Lei 11.106/2005
Desempate: Escolha este nó quando o bem jurídico for a regularidade do casamento (celebração, impedimentos, monogamia); se a falsidade recair sobre documento genérico sem vínculo com a celebração, use 5118.
```

### 5113 · irmão parecido: 5114 Dos Crimes Contra a Assistência Familiar

```text
[5113] Penal > Dos Crimes contra a Família > Dos Crimes Contra o Estado de Filiação
Escopo: Crimes contra o estado de filiação do CP (arts. 241 a 243): registro de nascimento inexistente, parto suposto, supressão ou alteração de direito inerente ao estado civil de recém-nascido ("adoção à brasileira") e sonegação de estado de filiação.
Inclui: Promover no registro civil a inscrição de nascimento inexistente (art. 241); Dar parto alheio como próprio e registrar como seu o filho de outrem, a chamada adoção à brasileira (art. 242); Ocultar ou substituir recém-nascido, suprimindo ou alterando direito inerente ao estado civil; Perdão judicial e pena reduzida quando o crime é praticado por motivo de reconhecida nobreza (art. 242, parágrafo único); Sonegação de estado de filiação: deixar filho em asilo ou instituição ocultando a filiação ou atribuindo-lhe outra (art. 243); Termo inicial da prescrição nos crimes de falsificação de assento de registro civil (CP, art. 111, IV)
Não inclui: Falsidade ideológica ou material de documento público fora do assento de nascimento (CP, arts. 297 e 299) → 5118; Promover ou auxiliar o envio de criança ao exterior ou entregar filho mediante paga (ECA, arts. 238 e 239) → 4709; Exposição ou abandono de recém-nascido para ocultar desonra própria (CP, art. 134) → 5141; Regras gerais do perdão judicial como causa de extinção da punibilidade → 5197; Contagem dos prazos prescricionais e marcos iniciais em geral → 5187
Âncoras legais: CP, art. 241; CP, art. 242; CP, art. 243; CP, art. 111, IV
Desempate: Escolha este nó quando a falsidade ou ocultação atingir a filiação ou o estado civil de recém-nascido; se a conduta envolver venda ou envio de criança previsto no ECA, use 4709.
```

### 5115 · irmão parecido: 5114 Dos Crimes Contra a Assistência Familiar

```text
[5115] Penal > Dos Crimes contra a Família > Dos Crimes Contra o Pátrio Poder, a Tutela e a Curatela
Escopo: Crimes contra o poder familiar (antigo pátrio poder), a tutela e a curatela previstos no CP (arts. 248 e 249): induzimento a fuga, entrega arbitrária ou sonegação de incapazes e subtração de incapazes.
Inclui: Induzir menor de 18 anos ou interdito a fugir do lugar onde está por determinação de quem tem a guarda (art. 248); Confiar arbitrariamente menor ou interdito a outrem sem ordem do pai, tutor, curador ou da autoridade; Deixar de entregar, sem justa causa, menor ou interdito a quem legitimamente o reclame (sonegação de incapazes); Subtração de menor de 18 anos ou interdito ao poder de quem o tem sob guarda, inclusive pelo próprio pai destituído ou suspenso do poder familiar (art. 249, § 1º); Perdão judicial na subtração de incapazes quando o menor ou interdito é restituído sem ter sofrido maus-tratos ou privações (art. 249, § 2º); Subsidiariedade expressa do art. 249 em relação a crimes mais graves
Não inclui: Sequestro ou cárcere privado de menor, inclusive a forma qualificada (CP, art. 148) → 5132; Extorsão mediante sequestro de criança (CP, art. 159) → 5161; Subtração de criança ou adolescente para colocação em lar substituto (ECA, art. 237) → 4709; Entrega de filho menor a pessoa inidônea (CP, art. 245) → 5114; Tráfico de pessoas envolvendo criança (CP, art. 149-A) → 5132
Âncoras legais: CP, art. 248; CP, art. 249
Desempate: Escolha este nó quando a conduta retirar ou mantiver o incapaz fora da guarda legítima sem privação de liberdade como fim; se houver restrição da liberdade da vítima, use 5132; se a finalidade for colocação em lar substituto, use 4709.
```

### 5134 · irmão parecido: 5116 Dos Crimes Contra a Fé Pública e de Falsidade Documental

```text
[5134] Penal > Dos Crimes contra a Organização do Trabalho, a Propriedade Imaterial e ao Sentimento Religioso
Escopo: Crimes dos Títulos III e IV e do Capítulo do sentimento religioso e respeito aos mortos do CP: propriedade imaterial (violação de direito autoral), organização do trabalho e sentimento religioso/respeito aos mortos. Cada bloco tem subtema próprio.
Inclui: Violação de direito autoral (CP, art. 184) e ação penal respectiva (art. 186); Atentado contra a liberdade de trabalho e de associação; Frustração de direito assegurado por lei trabalhista; Aliciamento de trabalhadores; Ultraje a culto e impedimento ou perturbação de cerimônia religiosa; Impedimento ou perturbação de cerimônia funerária, violação de sepultura e vilipêndio a cadáver; Competência da Justiça Federal para crimes contra a organização do trabalho (aspecto geral)
Não inclui: Redução a condição análoga à de escravo (CP, art. 149) → 5132; Injúria qualificada por elemento religioso (CP, art. 140, § 3º) → 5124; Discriminação ou preconceito de religião (Lei 7.716/1989) → 4690; Sabotagem de serviços essenciais (CP, art. 359-R) → 5156; Regras de competência criminal da Justiça Federal em si → 5482
Âncoras legais: CP, arts. 184 a 186; CP, arts. 197 a 207; CP, arts. 208 a 212; CF, art. 109, VI
Desempate: Use este nó só para questões que abordem conjuntamente mais de um dos três blocos ou o título em geral; questão sobre crime específico vai ao subtema correspondente (5135, 5136 ou 5137).
```

### 5135 · irmão parecido: 5136 Dos Crimes contra a Propriedade Imaterial

```text
[5135] Penal > Dos Crimes contra a Organização do Trabalho, a Propriedade Imaterial e ao Sentimento Religioso > Dos Crimes Contra a Organização do Trabalho
Escopo: Crimes do Título IV da Parte Especial do CP (arts. 197 a 207), que protegem a liberdade de trabalho, a associação, a legislação trabalhista e a nacionalização do trabalho, incluindo o aliciamento de trabalhadores.
Inclui: Atentado contra a liberdade de trabalho, de contrato de trabalho e boicotagem violenta (arts. 197 e 198); Atentado contra a liberdade de associação (art. 199); Paralisação de trabalho com violência ou perturbação da ordem e paralisação de obra de interesse coletivo (arts. 200 e 201); Invasão de estabelecimento industrial, comercial ou agrícola e sabotagem (art. 202); Frustração de direito assegurado por lei trabalhista e de obrigação de nacionalização do trabalho (arts. 203 e 204); Exercício de atividade com infração de decisão administrativa (art. 205); Aliciamento para fim de emigração e aliciamento de trabalhadores de um local para outro do território nacional (arts. 206 e 207)
Não inclui: Redução à condição análoga à de escravo e tráfico de pessoas para trabalho (CP, arts. 149 e 149-A) → 5132; Competência da Justiça Federal ou Estadual para julgar crimes contra a organização do trabalho → 5482; Apropriação indébita previdenciária de contribuições descontadas dos empregados (CP, art. 168-A) → 5165; Sabotagem de serviços essenciais contra o Estado Democrático de Direito (CP, art. 359-R) → 5156; Recusa de emprego por discriminação de raça, cor, etnia, religião ou procedência nacional (Lei 7.716/1989) → 4690; Desobediência genérica a ordem legal de funcionário público (CP, art. 330) → 5100
Âncoras legais: CP, arts. 197 a 207; CF, art. 109, VI
Desempate: Use este nó quando a conduta atingir a liberdade de trabalho ou os direitos trabalhistas tipificados nos arts. 197 a 207 do CP; se houver sujeição a trabalho forçado, jornada exaustiva ou condições degradantes, use o 5132 (art. 149).
```

### 5136 · irmão parecido: 5135 Dos Crimes Contra a Organização do Trabalho

```text
[5136] Penal > Dos Crimes contra a Organização do Trabalho, a Propriedade Imaterial e ao Sentimento Religioso > Dos Crimes contra a Propriedade Imaterial
Escopo: Crimes contra a propriedade imaterial: violação de direito autoral e conexos (CP, arts. 184 e 186) e crimes contra a propriedade industrial da Lei 9.279/1996, já que os arts. 187 a 196 do CP foram revogados.
Inclui: Violação de direito autoral: figura simples e qualificadas por intuito de lucro (art. 184, caput e §§ 1º a 3º); Venda e exposição à venda de CDs e DVDs piratas e afastamento da adequação social (Súmula 502 do STJ); Materialidade comprovada por perícia por amostragem, sem identificar os titulares dos direitos (Súmula 574 do STJ); Exceção da cópia integral, em um só exemplar, para uso privado do copista e sem intuito de lucro (art. 184, § 4º); Ação penal nos crimes de violação de direito autoral (art. 186); Crimes contra patentes, desenhos industriais, marcas e indicações geográficas e concorrência desleal (Lei 9.279/1996); Violação de direitos de autor de programa de computador (Lei 9.609/1998, art. 12)
Não inclui: Importação de mercadoria pirateada sem pagar tributos ou de importação proibida (CP, arts. 334 e 334-A) → 5094; Falsificação de selo ou sinal público (CP, art. 296) → 5118; Busca e apreensão como meio de prova, em sua disciplina geral → 5554; Regras gerais de ação penal pública condicionada e privada no CP (art. 100) → 5063; Venda de produto com marca falsa como fraude contra o consumidor (CDC, arts. 61 a 80) → 4694
Âncoras legais: CP, art. 184; CP, art. 186; Lei 9.279/1996, arts. 183 a 195; Lei 9.609/1998, art. 12
Desempate: Use este nó quando o bem jurídico lesado for o direito autoral ou a propriedade industrial; se o foco for a entrada irregular da mercadoria no país, use o 5094.
```

### 5147 · irmão parecido: 5087 Dos Crimes Contra a Administração Pública

```text
[5147] Penal > Dos Crimes contra as Finanças Públicas
Escopo: Crimes contra as finanças públicas do CP (arts. 359-A a 359-H, incluídos pela Lei 10.028/2000), ligados à Lei de Responsabilidade Fiscal: operações de crédito, restos a pagar, aumento de despesa com pessoal em fim de mandato, entre outros.
Inclui: Contratação de operação de crédito sem autorização legislativa (art. 359-A); Inscrição de despesas não empenhadas em restos a pagar (art. 359-B); Assunção de obrigação no último ano do mandato ou legislatura (art. 359-C); Ordenação de despesa não autorizada (art. 359-D); Prestação de garantia graciosa e não cancelamento de restos a pagar (arts. 359-E e 359-F); Aumento de despesa total com pessoal no último ano do mandato (art. 359-G); Oferta pública ou colocação de títulos no mercado sem lei (art. 359-H)
Não inclui: Emprego irregular de verbas ou rendas públicas (CP, art. 315) → 5090; Peculato (CP, art. 312) → 5089; Sonegação fiscal e crimes contra a ordem tributária (Lei 8.137/1990) → 4695; Crimes contra o Sistema Financeiro Nacional (Lei 7.492/1986) → 4689
Âncoras legais: CP, arts. 359-A a 359-H; Lei 10.028/2000
Desempate: Escolha este nó quando a conduta envolver gestão fiscal/orçamentária vedada pela LRF (crédito, restos a pagar, despesa com pessoal); se envolver desvio ou aplicação irregular de verba pública, vá para 5089 ou 5090.
```

### 5148 · irmão parecido: 5155 Dos Crimes contra o Estado Democrático de Direito

```text
[5148] Penal > Dos Crimes contra as Instituições Democráticas
Escopo: Crimes contra as instituições democráticas do CP (Capítulo II do Título XII, Lei 14.197/2021): abolição violenta do Estado Democrático de Direito e golpe de Estado.
Inclui: Abolição violenta do Estado Democrático de Direito (CP, art. 359-L); Golpe de Estado (CP, art. 359-M); Elementares de violência ou grave ameaça e tentativa de depor governo legitimamente constituído; Crimes de atentado/empreendimento (tentativa equiparada à consumação nesses tipos); Concurso entre arts. 359-L e 359-M e a pena correspondente à violência
Não inclui: Visão geral do Título XII, revogação da Lei de Segurança Nacional e crimes contra a soberania nacional (arts. 359-I a 359-K) → 5155; Interrupção do processo eleitoral e violência política (arts. 359-N e 359-P) → 5155; Sabotagem (CP, art. 359-R) → 5156; Atos de terrorismo (Lei 13.260/2016) → 4706; Crimes do Código Eleitoral → 4692
Âncoras legais: CP, art. 359-L; CP, art. 359-M; Lei 14.197/2021
Desempate: Use este nó quando a questão tratar especificamente de abolição violenta do Estado Democrático de Direito ou golpe de Estado; questões sobre o Título XII em geral ou outros capítulos vão para 5155.
```

### 5155 · irmão parecido: 5148 Dos Crimes contra as Instituições Democráticas

```text
[5155] Penal > Dos Crimes contra o Estado Democrático de Direito
Escopo: Título XII do CP (Lei 14.197/2021) em visão geral: revogação da Lei de Segurança Nacional, crimes contra a soberania nacional, crimes no processo eleitoral e disposições comuns. Instituições democráticas (5148) e serviços essenciais (5156) têm nó próprio.
Inclui: Revogação da Lei 7.170/1983 (LSN) e criação do Título XII do CP; Atentado à soberania, atentado à integridade nacional e espionagem (arts. 359-I a 359-K); Interrupção do processo eleitoral (art. 359-N); Violência política (art. 359-P); Excludente do art. 359-T (manifestação crítica, reunião, greve e protesto não constituem crime); Bem jurídico e características gerais do título
Não inclui: Abolição violenta do Estado Democrático de Direito e golpe de Estado (arts. 359-L e 359-M) → 5148; Sabotagem de serviços essenciais (art. 359-R) → 5156; Terrorismo (Lei 13.260/2016) → 4706; Crimes eleitorais do Código Eleitoral → 4692
Âncoras legais: CP, arts. 359-I a 359-K; CP, art. 359-N; CP, art. 359-P; CP, art. 359-T; Lei 14.197/2021
Desempate: Use este nó para o Título XII como um todo e para os capítulos sem nó próprio (soberania nacional, processo eleitoral, disposições comuns); arts. 359-L e 359-M vão para 5148 e art. 359-R para 5156.
```

### 5156 · irmão parecido: 5102 Dos Crimes Contra a Dignidade Sexual

```text
[5156] Penal > Dos Crimes contra o Funcionamento dos Serviços Essenciais
Escopo: Crime de sabotagem contra o funcionamento dos serviços essenciais (CP, art. 359-R), inserido no Título XII pela Lei 14.197/2021, com o fim de abolir o Estado Democrático de Direito.
Inclui: Sabotagem: destruir ou inutilizar meios de comunicação, estabelecimentos, instalações ou serviços destinados à defesa nacional; Especial fim de agir: abolir o Estado Democrático de Direito; Distinção entre sabotagem e dano/atentado contra serviço de utilidade pública; Bem jurídico: funcionamento dos serviços essenciais ao Estado democrático
Não inclui: Atentado contra a segurança de serviço de utilidade pública e interrupção de serviço telefônico (CP, arts. 265 e 266) → 5127; Paralisação de trabalho de interesse coletivo (CP, art. 201) → 5135; Dano qualificado contra patrimônio público (CP, art. 163, parágrafo único) → 5164; Atos de terrorismo contra infraestrutura (Lei 13.260/2016) → 4706; Interrupção do processo eleitoral (art. 359-N) → 5155
Âncoras legais: CP, art. 359-R; Lei 14.197/2021
Desempate: Escolha este nó quando a destruição de serviço ou instalação essencial tiver o fim de abolir o Estado Democrático de Direito; sem esse fim, vá para 5127 ou 5164.
```

### 5170 · irmão parecido: 5155 Dos Crimes contra o Estado Democrático de Direito

```text
[5170] Penal > Introdução ao Estudo do Direito Penal
Escopo: Bases do Direito Penal: conceito, fontes, princípios, interpretação da norma penal e classificações dos crimes. Cada um desses itens tem subtema próprio.
Inclui: Conceito, caracteres e funções do Direito Penal; Fontes materiais e formais do Direito Penal; Princípios da legalidade, intervenção mínima, lesividade, insignificância, culpabilidade, proporcionalidade; Interpretação e analogia em matéria penal; Classificações doutrinárias dos crimes (comum/próprio, material/formal, instantâneo/permanente etc.); Velocidades do Direito Penal e Direito Penal do autor x do fato (como introdução dogmática)
Não inclui: Retroatividade da lei penal benéfica e lei temporária/excepcional → 5181; Conflito aparente de normas (especialidade, consunção, subsidiariedade) → 5183; Direito Penal do Inimigo como política criminal → 4376; Princípios do processo penal → 5582; Teorias legitimadoras da pena (Criminologia) → 4384
Âncoras legais: CF, art. 5º, XXXIX; CP, art. 1º
Desempate: Use este nó só quando a questão misturar vários temas introdutórios sem predominar um; se tratar de princípio, fonte, interpretação ou classificação específica, vá para o subtema (5171 a 5174).
```

### 5173 · irmão parecido: 5172 Princípios do Direito Penal

```text
[5173] Penal > Introdução ao Estudo do Direito Penal > Interpretação da Norma Penal
Escopo: Interpretação da lei penal quanto ao sujeito, aos meios e ao resultado, além da analogia e da distinção entre interpretação extensiva, analógica e analogia in malam partem.
Inclui: Interpretação autêntica, doutrinária e jurisprudencial; Interpretação gramatical, lógica, teleológica, histórica e sistemática; Interpretação declaratória, restritiva e extensiva; Interpretação analógica (intra legem) versus analogia; Vedação da analogia in malam partem e admissão in bonam partem; In dubio pro reo na interpretação da norma penal; Norma penal em branco e tipos abertos como objeto de interpretação
Não inclui: Interpretação da lei processual penal (CPP, art. 3º) → 5508; Princípio da legalidade e taxatividade como garantia → 5172; Conflito aparente de normas (especialidade, subsidiariedade, consunção) → 5183; Retroatividade da lei penal benéfica → 5181; Analogia e costume como fontes do Direito Penal → 5171
Âncoras legais: CP, art. 1º; CF, art. 5º, XXXIX
Desempate: Escolha este nó quando a questão tratar de métodos de interpretação ou do uso da analogia na lei penal material; se a norma interpretada for processual, use 5508; se o foco for a garantia da legalidade em si, use 5172.
```

### 5172 · irmão parecido: 5171 Conceito e Fontes do Direito Penal

```text
[5172] Penal > Introdução ao Estudo do Direito Penal > Princípios do Direito Penal
Escopo: Princípios constitucionais e doutrinários limitadores do poder punitivo: legalidade e seus desdobramentos, intervenção mínima, fragmentariedade, insignificância, lesividade, culpabilidade, proporcionalidade, humanidade, individualização da pena, entre outros.
Inclui: Legalidade, reserva legal, anterioridade e taxatividade; Intervenção mínima, subsidiariedade e fragmentariedade; Insignificância (vetores do STF) e adequação social; Lesividade/ofensividade e exclusiva proteção de bens jurídicos; Culpabilidade, responsabilidade subjetiva e personalidade/intranscendência da pena; Proporcionalidade, humanidade e individualização da pena; Ne bis in idem e alteridade
Não inclui: Princípios do processo penal (presunção de inocência, contraditório) → 5582; Retroatividade benéfica e ultratividade na sucessão de leis → 5181; Princípios do conflito aparente de normas (especialidade, consunção) → 5183; Culpabilidade como elemento do crime → 5212; Correntes de política criminal (abolicionismo, garantismo, lei e ordem) → 4375; Princípios da territorialidade e extraterritorialidade → 5182
Âncoras legais: CF, art. 5º, XXXIX; CF, art. 5º, XL; CF, art. 5º, XLV; CF, art. 5º, XLVI; CF, art. 5º, XLVII; CP, art. 1º
Desempate: Use este nó quando a questão cobrar o princípio como limite ao poder punitivo; se cobrar a aplicação da lei no tempo, o conflito aparente de normas ou a culpabilidade como elemento do crime, use o nó específico.
```

### 5175 · irmão parecido: 5228 Teoria do Crime: Ilicitude

```text
[5175] Penal > Iter Criminis
Escopo: Caminho do crime: fases (cogitação, preparação, execução, consumação), consumação e tentativa, desistência voluntária, arrependimento eficaz, arrependimento posterior e crime impossível. Cada instituto tem subtema próprio.
Inclui: Fases do iter criminis e punibilidade dos atos preparatórios; Crime consumado e tentado; critérios de redução da pena na tentativa; Crimes que não admitem tentativa; Desistência voluntária e arrependimento eficaz (ponte de ouro); Arrependimento posterior (ponte de prata); Crime impossível e Súmula 145 do STF (flagrante preparado)
Não inclui: Atenuante genérica de reparação do dano após o recebimento da denúncia (CP, art. 65, III, b) → 5203; Reparação do dano no peculato culposo (CP, art. 312, § 3º) → 5089; Prisão em flagrante preparado, esperado ou forjado (aspecto processual) → 5518; Comunicabilidade da desistência entre coautores e partícipes → 5076; Classificação de crimes materiais, formais e de mera conduta → 5174
Âncoras legais: CP, art. 14; CP, art. 15; CP, art. 16; CP, art. 17
Desempate: Use este nó apenas quando a questão comparar vários institutos do iter criminis ao mesmo tempo; tratando de um instituto, use o subtema correspondente (5176 a 5179).
```

### 5182 · irmão parecido: 5181 Lei penal no Tempo

```text
[5182] Penal > Lei Penal no Tempo e no Espaço > Lei penal no Espaço
Escopo: Aplicação da lei penal brasileira no espaço: territorialidade e seus conceitos, lugar do crime, extraterritorialidade incondicionada e condicionada, pena cumprida no estrangeiro e eficácia da sentença estrangeira.
Inclui: Princípio da territorialidade temperada e território por extensão (embarcações e aeronaves); Lugar do crime: teoria da ubiquidade; Extraterritorialidade incondicionada e condicionada (princípios da defesa, justiça universal, nacionalidade, representação); Requisitos da extraterritorialidade condicionada e hipótese do § 3º do art. 7º; Pena cumprida no estrangeiro (detração/atenuação); Eficácia de sentença estrangeira e homologação para efeitos penais; Imunidades diplomáticas e parlamentares como exceção à territorialidade
Não inclui: Lei processual penal no espaço (CPP, art. 1º, territorialidade do processo) → 5506; Competência territorial do juízo (lugar da infração no CPP, art. 70) → 5483; Tempo do crime e sucessão de leis penais → 5181; Imunidades prisionais e prisões especiais → 5586
Âncoras legais: CP, art. 5º; CP, art. 6º; CP, art. 7º; CP, art. 8º; CP, art. 9º
Desempate: Use este nó para a aplicação da lei penal material brasileira a fatos ocorridos dentro ou fora do território (CP, arts. 5º a 9º); se a questão tratar de qual foro ou juízo processa o crime ou da lei processual no espaço, use Competência Territorial (5483) ou Lei Processual no Espaço (5506).
```

### 5181 · irmão parecido: 5182 Lei penal no Espaço

```text
[5181] Penal > Lei Penal no Tempo e no Espaço > Lei penal no Tempo
Escopo: Aplicação da lei penal no tempo: tempo do crime, irretroatividade da lei mais grave, retroatividade e ultratividade da lei benéfica, novatio legis, leis excepcionais e temporárias, e contagem de prazo penal.
Inclui: Tempo do crime: teoria da atividade (CP, art. 4º); Novatio legis in mellius e in pejus; retroatividade da lei benéfica mesmo após o trânsito em julgado; Lei penal no tempo em crime permanente e continuado (Súmula 711 do STF); Combinação de leis (lex tertia) e Súmula 501 do STJ; Leis excepcionais e temporárias: ultratividade (CP, art. 3º); Lei intermediária e competência para aplicar a lei mais benéfica (Súmula 611 do STF); Contagem de prazo penal e frações não computáveis (CP, arts. 10 e 11)
Não inclui: Abolitio criminis como causa de extinção da punibilidade e seus efeitos → 5194; Lei processual penal no tempo (tempus regit actum, normas híbridas) → 5507; Princípio da legalidade e anterioridade como princípio geral → 5172; Lugar do crime e extraterritorialidade → 5182; Conflito entre normas vigentes simultaneamente sobre o mesmo fato → 5183
Âncoras legais: CF, art. 5º, XL; CP, art. 2º; CP, art. 3º; CP, art. 4º; CP, art. 10; CP, art. 11
Desempate: Use este nó quando a questão tratar da sucessão de leis penais materiais e de qual lei se aplica ao fato; se o foco for a extinção da punibilidade pela abolitio criminis, use 5194; se a norma for processual, use 5507.
```

### 5186 · irmão parecido: 5190 Outras Prescrições

```text
[5186] Penal > Prescrição > Conceito, Regras Gerais e Fundamentos da Prescrição
Escopo: Noções gerais da prescrição penal: conceito, natureza jurídica de causa extintiva da punibilidade, fundamentos, imprescritibilidade constitucional e regras comuns a todas as modalidades, como a tabela do art. 109, a redução de prazos pela idade e a prescrição no concurso de crimes.
Inclui: Conceito e natureza jurídica da prescrição como causa de extinção da punibilidade (CP, art. 107, IV); Fundamentos da prescrição (esquecimento, desinteresse estatal, segurança jurídica, inércia do Estado); Crimes imprescritíveis: racismo e ação de grupos armados contra a ordem constitucional; Tabela de prazos do art. 109 do CP como regra geral; Redução dos prazos pela metade para menor de 21 anos ao tempo do crime ou maior de 70 na sentença (CP, art. 115); Prescrição no concurso de crimes: incidência isolada sobre cada crime (CP, art. 119; Súmula 497 STF); Crimes acessórios, complexos e conexos (CP, art. 108); Distinção entre prescrição, decadência e perempção
Não inclui: Termo inicial, causas impeditivas/suspensivas e interruptivas do prazo → 5187; Prescrição pela pena máxima em abstrato, retroativa ou intercorrente → 5188; Prescrição após o trânsito em julgado pela pena aplicada → 5189; Prescrição da multa, das penas restritivas e da medida de segurança → 5190; Decadência do direito de queixa ou representação → 5198; Crime de racismo em si (tipos da Lei 7.716/1989) → 4690
Âncoras legais: CP, art. 107, IV; CP, art. 108; CP, art. 109; CP, art. 115; CP, art. 119; CF, art. 5º, XLII; CF, art. 5º, XLIV
Desempate: Use este nó quando a questão tratar de conceito, fundamentos, imprescritibilidade ou de regra comum a todas as modalidades (arts. 108, 109, 115 e 119); se o foco for uma modalidade específica (PPP, PPE ou prescrição de multa/medida de segurança) ou marcos do prazo, use o irmão correspondente.
```

### 5187 · irmão parecido: 5186 Conceito, Regras Gerais e Fundamentos da Prescrição

```text
[5187] Penal > Prescrição > Contagem dos Prazos e Causas Suspensivas e Interruptivas da Prescrição
Escopo: Contagem dos prazos prescricionais: termos iniciais da prescrição antes e depois do trânsito em julgado, causas impeditivas ou suspensivas e causas interruptivas, com seus efeitos sobre o curso do prazo.
Inclui: Termo inicial da prescrição antes do trânsito em julgado (CP, art. 111), inclusive crimes permanentes, tentativa, bigamia e crimes sexuais contra criança ou adolescente; Termo inicial da prescrição depois do trânsito em julgado (CP, art. 112); Causas impeditivas/suspensivas do art. 116 do CP, inclusive ANPP pendente e recursos inadmissíveis aos tribunais superiores; Suspensão pela citação por edital (CPP, art. 366; Súmula 415 STJ) e por carta rogatória (CPP, art. 368); Suspensão durante o sursis processual (Lei 9.099/1995, art. 89, § 6º); Causas interruptivas do art. 117 do CP: recebimento da denúncia, pronúncia, acórdão confirmatório, sentença ou acórdão condenatório, início do cumprimento e reincidência; Comunicabilidade da interrupção aos coautores e crimes conexos e reinício do prazo (CP, art. 117, §§ 1º e 2º); Contagem do prazo penal com inclusão do dia do começo (CP, art. 10)
Não inclui: Identificação do prazo pela pena máxima ou aplicada e cálculo da prescrição retroativa → 5188; Aumento de 1/3 do prazo da PPE pela reincidência → 5189; Regras processuais da citação por edital em si → 5488; Suspensão condicional do processo: requisitos e condições → 5542; Requisitos do acordo de não persecução penal → 5502
Âncoras legais: CP, art. 10; CP, art. 111; CP, art. 112; CP, art. 116; CP, art. 117; CPP, art. 366; CPP, art. 368; Lei 9.099/1995, art. 89, § 6º
Desempate: Use este nó quando a questão girar em torno de quando o prazo começa, para, é suspenso ou é interrompido; se o ponto central for o cálculo da modalidade (pena em abstrato, retroativa, intercorrente ou executória), use 5188 ou 5189.
```

### 5190 · irmão parecido: 5186 Conceito, Regras Gerais e Fundamentos da Prescrição

```text
[5190] Penal > Prescrição > Outras Prescrições
Escopo: Prescrições com regras próprias fora da PPP e da PPE da pena privativa de liberdade: prescrição da pena de multa, das penas restritivas de direitos, da medida de segurança, do ato infracional e prazos especiais previstos em leis extravagantes.
Inclui: Prescrição da pena de multa isolada ou cumulada (CP, art. 114); Prescrição das penas restritivas de direitos pelo mesmo prazo da privativa substituída (CP, art. 109, parágrafo único); Prescrição da medida de segurança; Prescrição aplicável às medidas socioeducativas (Súmula 338 STJ); Prescrição em 2 anos do porte de drogas para consumo pessoal (Lei 11.343/2006, art. 30); Prazos e regras prescricionais especiais em leis extravagantes, como crimes falimentares
Não inclui: Prescrição pela pena privativa em abstrato, retroativa ou intercorrente → 5188; Prescrição executória da pena privativa de liberdade → 5189; Execução e cobrança da multa → 5206; Espécies e duração da medida de segurança → 5184; Tipos penais e procedimento da Lei de Drogas → 4708
Âncoras legais: CP, art. 109, parágrafo único; CP, art. 114; Lei 11.343/2006, art. 30
Desempate: Use este nó quando a prescrição recair sobre multa, pena restritiva, medida de segurança, ato infracional ou prazo especial de lei extravagante; se tratar de pena privativa de liberdade pelo regime comum do CP, use 5188 ou 5189.
```

### 5189 · irmão parecido: 5188 Prescrição da Pretensão Punitiva

```text
[5189] Penal > Prescrição > Prescrição da Pretensão Executória
Escopo: Prescrição da pretensão executória: perda do direito de executar a pena imposta após o trânsito em julgado da condenação, regulada pela pena aplicada, com aumento de 1/3 se o condenado for reincidente, e com efeitos limitados à extinção da pena.
Inclui: PPE regulada pela pena aplicada após o trânsito em julgado (CP, art. 110, caput); Aumento de 1/3 do prazo para o reincidente (CP, art. 110, caput) e inaplicabilidade à PPP (Súmula 220 STJ); Prescrição no caso de evasão ou revogação do livramento condicional pelo tempo restante da pena (CP, art. 113); Efeitos da PPE: extingue só a pena principal e mantém os efeitos secundários da condenação, como reincidência e título executivo; Distinção entre PPE e PPP; Discussão sobre o trânsito em julgado necessário para o início da PPE (STF, Tema 788)
Não inclui: Prescrição retroativa e intercorrente pela pena em concreto antes do trânsito para ambas as partes → 5188; Marcos de início e interrupção do art. 112 e art. 117, V e VI, como foco da questão → 5187; Prescrição da multa e das penas restritivas → 5190; Requisitos e revogação do livramento condicional → 5208; Reincidência como agravante na dosimetria → 5203
Âncoras legais: CP, art. 110, caput; CP, art. 112; CP, art. 113
Desempate: Use este nó quando a prescrição ocorrer depois do trânsito em julgado definitivo e atingir apenas a execução da pena; se ocorrer antes do trânsito (mesmo com base na pena em concreto, como na retroativa ou intercorrente), use 5188.
```

### 5188 · irmão parecido: 5189 Prescrição da Pretensão Executória

```text
[5188] Penal > Prescrição > Prescrição da Pretensão Punitiva
Escopo: Prescrição da pretensão punitiva antes do trânsito em julgado definitivo: modalidades em abstrato (pena máxima cominada), retroativa e intercorrente/superveniente (pena em concreto), seus requisitos, cálculo e efeitos, além da prescrição virtual.
Inclui: PPP em abstrato, calculada pela pena máxima cominada (CP, art. 109); Consideração das causas de aumento e de diminuição e desconsideração de agravantes e atenuantes no cálculo; Prescrição retroativa pela pena aplicada com trânsito para a acusação e vedação de termo anterior à denúncia ou queixa (CP, art. 110, § 1º, Lei 12.234/2010); Prescrição intercorrente ou superveniente à sentença condenatória; Prescrição virtual, antecipada ou em perspectiva e sua rejeição (Súmula 438 STJ); Efeitos da PPP: elimina todos os efeitos da condenação, penais e extrapenais
Não inclui: Prescrição após o trânsito em julgado definitivo e aumento de 1/3 pela reincidência → 5189; Marcos iniciais, suspensivos e interruptivos do prazo → 5187; Redução pela idade (art. 115) e prescrição no concurso de crimes (art. 119) → 5186; Prescrição da multa, da medida de segurança e prazos especiais → 5190; Causas de aumento e de diminuição na terceira fase da dosimetria → 5204
Âncoras legais: CP, art. 109; CP, art. 110, § 1º
Desempate: Use este nó quando a prescrição atingir o direito de punir antes do trânsito em julgado definitivo, inclusive pela pena em concreto (retroativa e intercorrente); só use 5189 quando já houver trânsito para ambas as partes e a prescrição atingir a execução da pena.
```

### 5199 · irmão parecido: 5063 Ação Penal

```text
[5199] Penal > Teoria da Pena
Escopo: Sanção penal no Código Penal: espécies de pena, regimes, dosimetria trifásica, multa, penas restritivas de direitos, sursis, livramento condicional, efeitos da condenação e reabilitação. Cada instituto tem subtema próprio.
Inclui: Conceito, finalidades e espécies de pena; Penas privativas de liberdade e regimes iniciais (CP, art. 33); Dosimetria trifásica (CP, arts. 59 e 68); Substituição por restritivas de direitos e pena de multa; Suspensão condicional da pena e livramento condicional; Efeitos da condenação e reabilitação
Não inclui: Teorias legitimadoras da pena (Criminologia) → 4384; Progressão de regime, remição e faltas disciplinares na LEP → 4703; Medida de segurança → 5184; Aplicação da pena no concurso de crimes → 5066; Fixação da pena e do regime na sentença (CPP, art. 387) → 5576; Suspensão condicional do processo (Lei 9.099/1995, art. 89) → 5542
Âncoras legais: CP, arts. 32 a 95
Desempate: Use este nó só quando a questão percorrer vários institutos da pena sem predominar um; caso contrário, use o subtema específico (5200 a 5210).
```

### 5208 · irmão parecido: 5207 Suspensão Condicional da Pena

```text
[5208] Penal > Teoria da Pena > Livramento Condicional
Escopo: Livramento condicional: requisitos objetivos e subjetivos, frações de cumprimento, condições, revogação obrigatória e facultativa, prorrogação e extinção da pena (CP, arts. 83 a 90).
Inclui: Requisitos: pena igual ou superior a 2 anos e cumprimento de mais de 1/3, mais da metade ou mais de 2/3; Vedação ao reincidente específico em crime hediondo ou equiparado (art. 83, V); Requisitos subjetivos: bom comportamento, ausência de falta grave nos últimos 12 meses, aptidão para o trabalho; Condições obrigatórias e facultativas impostas ao liberado; Revogação obrigatória e facultativa (arts. 86 e 87); Efeitos da revogação sobre o cômputo do tempo (art. 88); Prorrogação do período de prova e extinção da pena (arts. 89 e 90)
Não inclui: Suspensão condicional da pena (sursis) → 5207; Procedimento do livramento na execução, cerimônia e incidentes (LEP, arts. 131 a 146) → 4703; Progressão de regime → 4703; Frações e vedações próprias da Lei de Crimes Hediondos → 4693; Recurso contra decisão sobre livramento na execução (agravo em execução) → 5566
Âncoras legais: CP, arts. 83 a 90; LEP, arts. 131 a 146
Desempate: Use este nó quando o liberado já cumpriu parte da pena privativa de liberdade. Se a execução da pena foi suspensa desde a sentença, use o nó 5207 (sursis).
```

### 5201 · irmão parecido: 5205 Penas Restritivas de Direitos

```text
[5201] Penal > Teoria da Pena > Penas Privativas de Liberdade
Escopo: Penas privativas de liberdade no CP: reclusão, detenção e prisão simples; regimes fechado, semiaberto e aberto; fixação do regime inicial; regras de cada regime; detração; e limite de cumprimento (arts. 33 a 42 e 75).
Inclui: Distinção entre reclusão e detenção; Regime inicial conforme a quantidade de pena e a reincidência (art. 33, § 2º); Súmulas 440 e 269 do STJ e Súmulas 718 e 719 do STF sobre regime; Regras dos regimes fechado, semiaberto e aberto (arts. 34 a 36); Regime especial das mulheres e direitos do preso (arts. 37 e 38); Trabalho do preso e superveniência de doença mental (arts. 39 a 41); Detração penal (art. 42); Limite de 40 anos de cumprimento e unificação das penas (art. 75)
Não inclui: Progressão e regressão de regime, remição e faltas disciplinares (LEP) → 4703; Substituição da pena privativa de liberdade por restritiva de direitos → 5205; Fixação do regime na sentença e detração no CPP (art. 387, § 2º) → 5576; Regime inicial em crimes hediondos → 4693; Espécies de pena em geral e finalidade da sanção → 5200
Âncoras legais: CP, arts. 33 a 42; CP, art. 75; CF, art. 5º, XLVII
Desempate: Use este nó para as regras do CP sobre regimes e cumprimento da pena privativa de liberdade. Se a questão for sobre progressão, regressão ou remição na execução, use o nó 4703.
```

### 5205 · irmão parecido: 5201 Penas Privativas de Liberdade

```text
[5205] Penal > Teoria da Pena > Penas Restritivas de Direitos
Escopo: Penas restritivas de direitos no CP: espécies, natureza autônoma e substitutiva, requisitos da substituição, duração, conversão em pena privativa de liberdade e regras de cada modalidade (arts. 43 a 48).
Inclui: Espécies: prestação pecuniária, perda de bens e valores, prestação de serviços, interdição temporária de direitos e limitação de fim de semana; Requisitos da substituição (art. 44): pena até 4 anos, crime sem violência ou grave ameaça, não reincidente em crime doloso; Substituição no crime culposo, qualquer que seja a pena; Reincidente: substituição se socialmente recomendável e sem reincidência específica (art. 44, § 3º); Conversão em privativa de liberdade pelo descumprimento, com abatimento do tempo cumprido (art. 44, § 4º); Prestação de serviços apenas para condenações superiores a 6 meses (art. 46); Súmula 588 do STJ: vedação de substituição em violência doméstica com violência ou grave ameaça
Não inclui: Pena de multa como pena autônoma (dias-multa) → 5206; Suspensão condicional da pena → 5207; Transação penal com proposta de pena restritiva nos Juizados → 5541; Vedações da Lei Maria da Penha (cesta básica e pagamento isolado de multa) → 4704; Substituição no tráfico de drogas → 4708
Âncoras legais: CP, arts. 43 a 48; CP, art. 44; CF, art. 5º, XLVI
Desempate: Use este nó quando a questão tratar da substituição da pena privativa de liberdade ou das modalidades restritivas. Se a questão tratar da suspensão da execução da pena, use o nó 5207.
```

### 5202 · irmão parecido: 5204 Terceira fase da Dosimetria: Causas de Aumento e de Diminuição

```text
[5202] Penal > Teoria da Pena > Primeira Fase da Dosimetria: Circunstâncias Judiciais
Escopo: Primeira fase da dosimetria no sistema trifásico: análise das oito circunstâncias judiciais do art. 59 do CP para fixar a pena-base dentro dos limites do tipo, e o uso dessas circunstâncias para outros fins previstos no art. 59.
Inclui: Sistema trifásico de Nelson Hungria (art. 68, caput); As oito circunstâncias judiciais: culpabilidade, antecedentes, conduta social, personalidade, motivos, circunstâncias, consequências e comportamento da vítima; Pena-base fixada dentro dos limites legais; Súmula 444 do STJ: inquéritos e ações em curso não agravam a pena-base; Maus antecedentes e período depurador; Vedação de bis in idem com elementares e qualificadoras; Fundamentação concreta para exasperar a pena-base; Qualificadora excedente usada como circunstância judicial
Não inclui: Reincidência e demais agravantes e atenuantes → 5203; Majorantes e minorantes → 5204; Preponderância de natureza e quantidade da droga (Lei 11.343/2006, art. 42) → 4708; Fixação da pena na sentença conforme o CPP (art. 387) → 5576; Princípio da individualização da pena → 5172
Âncoras legais: CP, art. 59; CP, art. 68
Desempate: Use este nó quando a questão tratar da pena-base e das circunstâncias do art. 59. Se a questão tratar de reincidência ou de agravantes e atenuantes legais (arts. 61 a 66), use o nó 5203.
```

### 5210 · irmão parecido: 5208 Livramento Condicional

```text
[5210] Penal > Teoria da Pena > Reabilitação Criminal
Escopo: Reabilitação criminal no CP: natureza, alcance (sigilo dos registros e efeitos específicos do art. 92), prazo e requisitos, revogação e renovação do pedido (arts. 93 a 95).
Inclui: Alcance: sigilo sobre o processo e a condenação (art. 93); Recuperação dos efeitos do art. 92, vedada a reintegração no cargo ou na função e no poder familiar quanto ao filho vítima; Prazo de 2 anos após a extinção ou o fim da execução da pena (art. 94); Requisitos: domicílio no país, bom comportamento público e privado, reparação do dano; Revogação de ofício ou a requerimento do MP diante de nova condenação (art. 95); Distinção entre reabilitação e período depurador da reincidência
Não inclui: Efeitos da condenação dos arts. 91 e 92 → 5209; Período depurador da reincidência (art. 64, I) → 5203; Indulto, graça e anistia → 5193; Recurso de ofício e procedimento da reabilitação no CPP → 5561
Âncoras legais: CP, arts. 93 a 95
Desempate: Use este nó quando a questão tratar do pedido de reabilitação. Se a questão tratar só da perda de cargo ou de outro efeito específico imposto pela condenação, use o nó 5209.
```

### 5203 · irmão parecido: 5204 Terceira fase da Dosimetria: Causas de Aumento e de Diminuição

```text
[5203] Penal > Teoria da Pena > Segunda Fase da Dosimetria: Agravantes e Atenuantes
Escopo: Segunda fase da dosimetria: agravantes (arts. 61 e 62), reincidência (arts. 63 e 64), atenuantes nominadas e inominadas (arts. 65 e 66) e concurso entre agravantes e atenuantes (art. 67).
Inclui: Rol das agravantes genéricas (art. 61) e agravantes no concurso de pessoas (art. 62); Reincidência: conceito, período depurador de 5 anos, crimes militares próprios e políticos; Atenuantes: menoridade relativa, maior de 70 anos, confissão espontânea, reparação do dano; Atenuante inominada (art. 66); Súmula 231 do STJ: atenuante não reduz a pena abaixo do mínimo; Súmula 545 do STJ: confissão usada para a condenação atenua a pena; Preponderância e compensação entre reincidência e confissão (art. 67); Súmula 241 do STJ: bis in idem entre reincidência e antecedentes
Não inclui: Maus antecedentes e circunstâncias judiciais → 5202; Causas de aumento e de diminuição em frações → 5204; Reincidência como causa de aumento do prazo da prescrição executória (art. 110) → 5187; Reabilitação criminal → 5210
Âncoras legais: CP, arts. 61 a 67
Desempate: Use este nó quando a circunstância estiver nos arts. 61 a 66 do CP, sem fração legal fixada. Se a lei prevê fração ou patamar de aumento ou de redução, use o nó 5204.
```

### 5207 · irmão parecido: 5208 Livramento Condicional

```text
[5207] Penal > Teoria da Pena > Suspensão Condicional da Pena
Escopo: Suspensão condicional da pena (sursis) no CP: espécies (simples, especial, etário e humanitário), requisitos, período de prova, condições, revogação obrigatória e facultativa, prorrogação e extinção (arts. 77 a 82).
Inclui: Requisitos: pena não superior a 2 anos, não reincidência em crime doloso, circunstâncias favoráveis, não cabimento de restritiva; Sursis etário e humanitário: pena até 4 anos (art. 77, § 2º); Sursis simples e especial e suas condições (art. 78); Período de prova de 2 a 4 anos (ou de 4 a 6 anos); Revogação obrigatória e facultativa (art. 81); Prorrogação automática do período de prova durante processo por outro crime; Extinção da pena ao fim do período de prova (art. 82); Sursis não se estende às restritivas de direitos nem à multa (art. 80)
Não inclui: Suspensão condicional do processo (Lei 9.099/1995, art. 89) → 5542; Livramento condicional → 5208; Substituição por pena restritiva de direitos → 5205; Audiência admonitória e execução do sursis (LEP, arts. 156 a 163) → 4703; Sursis nos crimes ambientais (Lei 9.605/1998) → 4688
Âncoras legais: CP, arts. 77 a 82; LEP, arts. 156 a 163
Desempate: Use este nó quando houver condenação e a execução da pena for suspensa. Se o processo for suspenso antes da condenação (Lei 9.099/1995, art. 89), use o nó 5542. Se a pena já estiver sendo cumprida, use o nó 5208.
```

### 5204 · irmão parecido: 5202 Primeira Fase da Dosimetria: Circunstâncias Judiciais

```text
[5204] Penal > Teoria da Pena > Terceira fase da Dosimetria: Causas de Aumento e de Diminuição
Escopo: Terceira fase da dosimetria: aplicação das causas de aumento (majorantes) e de diminuição (minorantes) da Parte Geral e da Parte Especial, que podem levar a pena além do máximo ou aquém do mínimo, e o concurso entre elas (art. 68, parágrafo único).
Inclui: Majorantes e minorantes expressas em frações ou patamares; Possibilidade de ultrapassar os limites abstratos do tipo; Concurso de causas de aumento ou de diminuição da Parte Especial (art. 68, parágrafo único); Súmula 443 do STJ: aumento no roubo exige fundamentação concreta, não basta o número de majorantes; Distinção entre qualificadora e causa de aumento; Ordem de incidência: primeiro os aumentos, depois as diminuições, em cascata
Não inclui: Fração de redução da tentativa → 5177; Arrependimento posterior como causa de diminuição → 5178; Exasperação no concurso formal e no crime continuado → 5066; Tráfico privilegiado (Lei 11.343/2006, art. 33, § 4º) → 4708; Agravantes e atenuantes genéricas → 5203; Semi-imputabilidade como causa de diminuição (art. 26, parágrafo único) → 5213
Âncoras legais: CP, art. 68
Desempate: Use este nó quando a questão tratar da técnica de aplicar majorantes e minorantes na dosimetria. Se a questão tratar do instituto que gera a causa (tentativa, concurso de crimes, tráfico privilegiado), use o nó desse instituto.
```

### 5211 · irmão parecido: 5228 Teoria do Crime: Ilicitude

```text
[5211] Penal > Teoria do Crime: Culpabilidade
Escopo: Culpabilidade como juízo de reprovação: conceito e elementos (imputabilidade, potencial consciência da ilicitude, exigibilidade de conduta diversa) e suas causas de exclusão legais e supralegais. Cada uma tem subtema próprio.
Inclui: Teorias da culpabilidade (psicológica, psicológico-normativa, normativa pura); Inimputabilidade por doença mental, menoridade e embriaguez completa fortuita; Erro de proibição direto e indireto; Coação moral irresistível e obediência hierárquica; Inexigibilidade de conduta diversa como causa supralegal; Actio libera in causa
Não inclui: Erro de tipo e descriminantes putativas por erro sobre a situação de fato → 5224; Excludentes de ilicitude (legítima defesa, estado de necessidade) → 5228; Coação física irresistível (exclusão da conduta) → 5221; Medida de segurança aplicável ao inimputável → 5184; Incidente de insanidade mental → 5497; Circunstâncias judiciais, incluída a culpabilidade do art. 59 → 5202
Âncoras legais: CP, arts. 21 a 28
Desempate: Use este nó só quando a questão abordar a culpabilidade de modo panorâmico ou comparar várias excludentes; questão sobre uma causa específica vai para o subtema (5212 a 5217).
```

### 5217 · irmão parecido: 5212 Conceito e Elementos da Culpabilidade

```text
[5217] Penal > Teoria do Crime: Culpabilidade > Causas Supralegais de Exclusão da Culpabilidade
Escopo: Hipóteses de exclusão da culpabilidade sem previsão legal expressa, apoiadas na inexigibilidade de conduta diversa como princípio geral, e o debate doutrinário e jurisprudencial sobre sua admissão.
Inclui: Inexigibilidade de conduta diversa como causa supralegal de exculpação; Estado de necessidade exculpante (teoria diferenciadora) fora das hipóteses do CP; Excesso exculpante na legítima defesa (medo, susto, perturbação); Cláusula de consciência e objeção de consciência; Desobediência civil como causa supralegal de exculpação; Ordem de superior em relação privada (sem hierarquia pública) tratada como inexigibilidade; Admissibilidade da tese de inexigibilidade no Tribunal do Júri
Não inclui: Consentimento do ofendido e outras causas supralegais de exclusão da ilicitude → 5233; Coação moral irresistível do art. 22 do CP → 5215; Obediência hierárquica a ordem não manifestamente ilegal de superior público → 5216; Exigibilidade de conduta diversa apenas como elemento da culpabilidade, em abstrato → 5212; Estado de necessidade justificante do art. 24 do CP → 5230
Âncoras legais: CP, art. 22; CP, art. 23, parágrafo único
Desempate: Use este nó quando a exculpação se apoiar em hipótese não prevista em lei; se a situação se enquadrar na coação moral ou na obediência hierárquica do art. 22 do CP, use 5215 ou 5216.
```

### 5213 · irmão parecido: 5212 Conceito e Elementos da Culpabilidade

```text
[5213] Penal > Teoria do Crime: Culpabilidade > Inimputabilidade
Escopo: Imputabilidade penal e suas exclusões: doença mental ou desenvolvimento mental incompleto ou retardado, menoridade, embriaguez, além da semi-imputabilidade e da irrelevância da emoção e da paixão.
Inclui: Critério biopsicológico (art. 26) e critério biológico da menoridade (art. 27; CF, art. 228); Semi-imputabilidade e redução de pena de 1/3 a 2/3; Emoção e paixão não excluem a imputabilidade; Embriaguez voluntária e culposa: actio libera in causa; Embriaguez completa por caso fortuito ou força maior (isenção) e incompleta (redução); Sentença absolutória imprópria para o inimputável por doença mental
Não inclui: Espécies, prazos e execução da medida de segurança → 5184; Procedimento do incidente de insanidade mental → 5497; Isenção de pena do dependente de drogas (Lei 11.343/2006, art. 45) → 4708; Agravante da embriaguez preordenada → 5203; Violenta emoção como privilégio no homicídio → 5150
Âncoras legais: CP, art. 26; CP, art. 27; CP, art. 28; CF, art. 228
Desempate: Use este nó para a análise da capacidade de culpabilidade; se a questão tratar da sanção aplicada ao inimputável (espécie, prazo, desinternação), use 5184.
```

### 5218 · irmão parecido: 5228 Teoria do Crime: Ilicitude

```text
[5218] Penal > Teoria do Crime: Fato Típico
Escopo: Primeiro substrato do crime: conceito, sujeitos e objeto do crime, conduta, resultado, nexo causal e imputação objetiva, tipicidade, dolo e culpa, omissão e erro de tipo. Cada elemento tem subtema próprio.
Inclui: Conceito analítico de crime e elementos do fato típico; Teorias da conduta (causal, finalista, social, funcional); Relação de causalidade e superveniência de causa independente (CP, art. 13); Dolo, culpa e crime preterdoloso (CP, arts. 18 e 19); Omissão própria e imprópria; dever de garante (art. 13, § 2º); Erro de tipo essencial e acidental (CP, art. 20); Tipicidade formal, material e conglobante
Não inclui: Tentativa e consumação → 5177; Crime impossível → 5179; Erro de proibição → 5214; Excludentes de ilicitude → 5228; Princípio da insignificância como princípio penal → 5172; Classificações doutrinárias dos crimes → 5174
Âncoras legais: CP, art. 13; CP, art. 18; CP, art. 19; CP, art. 20
Desempate: Use este nó só quando a questão cobrir vários elementos do fato típico sem foco em um; se tratar de conduta, resultado, nexo, dolo/culpa, omissão, erro de tipo ou tipicidade, use o subtema.
```

### 5219 · irmão parecido: 5226 Nexo Causal e Imputação Objetiva

```text
[5219] Penal > Teoria do Crime: Fato Típico > Conceito, Sujeito e Objeto do Crime
Escopo: Conceitos de crime (formal, material e analítico: bipartido, tripartido, quadripartido), distinção entre crime e contravenção, sujeitos ativo e passivo e objetos jurídico e material do delito.
Inclui: Conceito formal, material e analítico de crime; Teorias bipartida, tripartida e quadripartida; Diferença entre crime e contravenção (sistema dicotômico); Sujeito ativo: capacidade penal, crimes próprios e de mão própria; Responsabilidade penal da pessoa jurídica; Sujeito passivo constante/formal e eventual/material; Objeto jurídico (bem tutelado) e objeto material
Não inclui: Elementos do fato típico (conduta, resultado, nexo, tipicidade) como estrutura → 5220; Classificações gerais dos crimes (comum, próprio, plurissubsistente etc.) cobradas em lista → 5174; Crimes ambientais da pessoa jurídica em espécie e suas penas → 4688; Elementos da culpabilidade → 5212
Âncoras legais: Decreto-Lei 3.914/1941, art. 1º; CF, art. 225, § 3º; Lei 9.605/1998, art. 3º
Desempate: Use este nó quando a questão tratar do conceito de crime ou de seus sujeitos e objetos; se tratar dos elementos internos do fato típico, use 5220, e se for rol de classificações dos crimes, use 5174.
```

### 5222 · irmão parecido: 5223 Crimes Omissivos e Comissivos

```text
[5222] Penal > Teoria do Crime: Fato Típico > Crime Doloso e Culposo
Escopo: Elemento subjetivo e normativo do tipo: dolo e suas espécies, culpa e suas modalidades, excepcionalidade do crime culposo e crime preterdoloso/qualificado pelo resultado.
Inclui: Teorias do dolo (vontade, assentimento, representação); Dolo direto de 1º e 2º grau, dolo eventual, dolo genérico e específico; Culpa consciente x dolo eventual; Imprudência, negligência e imperícia; culpa inconsciente e imprópria; Excepcionalidade do crime culposo e inexistência de compensação de culpas; Crime preterdoloso e qualificado pelo resultado (CP, art. 19); Elementos do crime culposo (dever de cuidado, previsibilidade)
Não inclui: Erro que exclui o dolo e culpa imprópria por descriminante putativa → 5224; Homicídio culposo e dolo eventual no homicídio em espécie → 5150; Homicídio e lesão culposos na direção de veículo → 4691; Teorias da ação e ausência de conduta → 5221
Âncoras legais: CP, art. 18; CP, art. 19
Desempate: Use este nó quando a questão discutir dolo ou culpa em abstrato; se a dúvida decorrer de erro sobre elementar ou descriminante putativa, use 5224.
```

### 5223 · irmão parecido: 5222 Crime Doloso e Culposo

```text
[5223] Penal > Teoria do Crime: Fato Típico > Crimes Omissivos e Comissivos
Escopo: Classificação dos crimes quanto à forma da conduta: comissivos, omissivos próprios e omissivos impróprios (comissivos por omissão), relevância penal da omissão e posição de garantidor.
Inclui: Crime omissivo próprio x impróprio; Relevância da omissão e poder de agir; Hipóteses de dever de agir do garantidor (CP, art. 13, § 2º); Ingerência: criação do risco pelo comportamento anterior; Tentativa nos crimes omissivos; Crimes de conduta mista
Não inclui: Tipo de omissão de socorro em espécie → 5142; Nexo causal da ação e concausas (CP, art. 13, caput e § 1º) → 5226; Teorias da conduta e ausência de ação → 5221; Condescendência criminosa e prevaricação como tipos omissivos → 5096
Âncoras legais: CP, art. 13, § 2º
Desempate: Escolha este nó quando a questão versar sobre a omissão ou o dever de garantidor; se tratar de causalidade da ação e concausas, use 5226.
```

### 5224 · irmão parecido: 5220 Fato Típico

```text
[5224] Penal > Teoria do Crime: Fato Típico > Erro de Tipo
Escopo: Erro sobre elementos do tipo: erro de tipo essencial (escusável e inescusável) e acidental (sobre o objeto, sobre a pessoa, na execução, resultado diverso do pretendido), descriminantes putativas por erro de tipo e erro provocado por terceiro.
Inclui: Erro de tipo essencial escusável (exclui dolo e culpa) e inescusável (permite culpa); Erro sobre a pessoa (CP, art. 20, § 3º); Aberratio ictus e aberratio criminis (CP, arts. 73 e 74); Erro sobre o objeto e erro sobre o nexo causal (aberratio causae); Descriminantes putativas por erro de tipo permissivo (CP, art. 20, § 1º); Erro determinado por terceiro (CP, art. 20, § 2º); Delito putativo por erro de tipo
Não inclui: Erro de proibição direto e indireto (CP, art. 21) → 5214; Legítima defesa real e seus requisitos → 5231; Dolo e culpa em abstrato → 5222; Concurso formal resultante de aberratio ictus com unidade complexa (regras de pena) → 5068
Âncoras legais: CP, art. 20; CP, art. 73; CP, art. 74
Desempate: Use este nó quando o erro recair sobre a realidade fática ou elementar do tipo; se recair sobre a ilicitude do fato ou os limites de uma causa de justificação, use 5214.
```

### 5220 · irmão parecido: 5224 Erro de Tipo

```text
[5220] Penal > Teoria do Crime: Fato Típico > Fato Típico
Escopo: Fato típico como primeiro substrato do crime: conceito e elementos (conduta, resultado, nexo causal e tipicidade) e sua composição nos crimes dolosos, culposos, materiais e formais, sem aprofundar um elemento isolado.
Inclui: Conceito de fato típico e sua posição no conceito analítico; Elementos do fato típico e quando todos estão presentes; Diferença de estrutura do fato típico em crimes materiais e de mera conduta; Fato típico x ilicitude x culpabilidade (relação geral); Questões que combinam vários elementos do fato típico
Não inclui: Conceito analítico de crime e sujeitos/objetos → 5219; Teorias da ação e ausência de conduta → 5221; Tipicidade formal, material e conglobante → 5227; Nexo causal e imputação objetiva → 5226; Resultado naturalístico e normativo → 5225
Desempate: Use este nó só quando a questão tratar do fato típico como um todo ou de vários elementos ao mesmo tempo; se o foco for um elemento específico, use o irmão correspondente (5221, 5225, 5226 ou 5227).
```

### 5226 · irmão parecido: 5219 Conceito, Sujeito e Objeto do Crime

```text
[5226] Penal > Teoria do Crime: Fato Típico > Nexo Causal e Imputação Objetiva
Escopo: Relação de causalidade entre conduta e resultado: teoria da equivalência dos antecedentes, concausas absolutas e relativamente independentes, causa superveniente e teoria da imputação objetiva.
Inclui: Teoria da conditio sine qua non e eliminação hipotética de Thyrén; Concausas preexistentes, concomitantes e supervenientes; Causa superveniente relativamente independente que por si só produz o resultado (CP, art. 13, § 1º); Teoria da causalidade adequada; Imputação objetiva (Roxin e Jakobs): risco proibido, risco permitido, âmbito de proteção da norma; Princípio da confiança e autocolocação da vítima em risco
Não inclui: Relevância da omissão e dever de garantidor (CP, art. 13, § 2º) → 5223; Erro sobre o nexo causal (aberratio causae) → 5224; Espécies de resultado (naturalístico e jurídico) → 5225; Tipicidade conglobante e material → 5227
Âncoras legais: CP, art. 13, caput e § 1º
Desempate: Escolha este nó quando a questão discutir se o resultado pode ser atribuído à conduta; se a discussão for sobre o dever jurídico de agir na omissão, use 5223.
```

### 5228 · irmão parecido: 5211 Teoria do Crime: Culpabilidade

```text
[5228] Penal > Teoria do Crime: Ilicitude
Escopo: Ilicitude (antijuridicidade): conceito e relação com a tipicidade, causas legais de exclusão (estado de necessidade, legítima defesa, estrito cumprimento do dever legal, exercício regular de direito), excesso punível e causas supralegais. Exercício regular de direito não tem subtema próprio.
Inclui: Conceito de ilicitude formal e material; teoria da ratio cognoscendi; Rol do art. 23 do CP e excesso doloso ou culposo; Estado de necessidade (art. 24) e legítima defesa (art. 25); Estrito cumprimento do dever legal; Exercício regular de direito e ofendículos; Consentimento do ofendido como causa supralegal
Não inclui: Descriminante putativa por erro sobre a situação de fato (CP, art. 20, § 1º) → 5224; Erro de proibição indireto sobre limites da excludente → 5214; Coação moral irresistível e obediência hierárquica → 5211; Vedação de preventiva quando presente excludente (CPP, art. 314) → 5519; Efeito civil da sentença que reconhece excludente (CPP, art. 65) → 5475
Âncoras legais: CP, art. 23; CP, art. 24; CP, art. 25
Desempate: Use este nó quando a questão comparar várias excludentes ou tratar de exercício regular de direito/excesso em geral; questão centrada em uma excludente com subtema vai para 5229 a 5233.
```

### 5233 · irmão parecido: 5229 Conceito e Elementos da Ilicitude

```text
[5233] Penal > Teoria do Crime: Ilicitude > Causas Supralegais de Exclusão da Ilicitude
Escopo: Causas de exclusão da ilicitude não previstas em lei, admitidas pela doutrina e pela jurisprudência, com destaque para o consentimento do ofendido como causa supralegal de justificação.
Inclui: Consentimento do ofendido como excludente supralegal da ilicitude; Requisitos do consentimento: bem jurídico disponível, ofendido capaz, consentimento livre e anterior ou simultâneo à conduta; Fundamento da admissão de justificantes supralegais (analogia in bonam partem, ilicitude material); Distinção entre consentimento que exclui a ilicitude e consentimento que exclui a tipicidade; Consentimento do ofendido em lesões leves, intervenções cirúrgicas e práticas esportivas
Não inclui: Consentimento ou dissenso como elementar do tipo (ex.: violação de domicílio), afastando a tipicidade → 5227; Causas supralegais de exclusão da culpabilidade, como a inexigibilidade de conduta diversa → 5217; Exercício regular de direito e as excludentes legais do art. 23 sem nó próprio → 5229; Princípio da adequação social e insignificância → 5172
Âncoras legais: CP, art. 23
Desempate: Use este nó quando a questão tratar de justificante sem previsão legal, sobretudo o consentimento do ofendido; se o consentimento afastar elementar do tipo, use Tipicidade (5227), e se a causa supralegal excluir a culpabilidade, use 5217.
```

### 5229 · irmão parecido: 5233 Causas Supralegais de Exclusão da Ilicitude

```text
[5229] Penal > Teoria do Crime: Ilicitude > Conceito e Elementos da Ilicitude
Escopo: Conceito de ilicitude (antijuridicidade), suas espécies e relação com a tipicidade, além da visão geral das excludentes do art. 23 do CP. Inclui o exercício regular de direito e o excesso punível, que não têm subtema próprio.
Inclui: Conceito de ilicitude formal e material, objetiva e subjetiva; Relação entre tipicidade e ilicitude: ratio cognoscendi, ratio essendi e teoria dos elementos negativos do tipo; Rol das excludentes legais do art. 23 do CP e o elemento subjetivo das justificantes; Exercício regular de direito (inclusive ofendículos e intervenções médicas); Excesso doloso e culposo nas excludentes em geral (art. 23, parágrafo único); Efeitos civis do reconhecimento das excludentes (CC, art. 188)
Não inclui: Requisitos e espécies do estado de necessidade → 5230; Requisitos, espécies e excesso na legítima defesa → 5231; Estrito cumprimento do dever legal → 5232; Consentimento do ofendido e outras justificantes supralegais → 5233; Tipicidade conglobante e atipicidade de condutas fomentadas pelo ordenamento → 5227; Descriminantes putativas por erro sobre a situação de fato → 5224
Âncoras legais: CP, art. 23; CC, art. 188
Desempate: Use este nó para o conceito de ilicitude, para questões que comparam as excludentes em geral, para o exercício regular de direito e para o excesso tratado de forma genérica; se a questão focar uma excludente específica (estado de necessidade, legítima defesa ou estrito cumprimento), use o nó dela.
```

### 5480 · irmão parecido: 5466 Ação Penal

```text
[5480] Processo Penal > Competência
Escopo: Regras que definem o órgão jurisdicional competente para processar e julgar a infração: espécies e fixação, matéria, território, prerrogativa de função, juízo, conexão, continência e modificação. Todas as partes têm subtema próprio.
Inclui: Competência absoluta e relativa; Competência pelo lugar da infração e pelo domicílio do réu; Competência da Justiça Federal, Eleitoral e Militar em matéria criminal; Foro por prerrogativa de função; Conexão, continência, prevenção e distribuição; Perpetuatio jurisdictionis e desmembramento; Conflito de competência
Não inclui: Exceção de incompetência como meio processual de arguição → 5493; Competência dos Juizados Especiais Criminais → 5540; Nulidade por incompetência do juízo → 5511; Aplicação da lei processual penal no espaço (territorialidade) → 5506; Princípios constitucionais do Júri (plenitude de defesa, sigilo, soberania dos veredictos) → 5525
Âncoras legais: CPP, arts. 69 a 91; CF, art. 5º, XXXVIII; CF, art. 109; CF, art. 102, I
```

### 5483 · irmão parecido: 5482 Competência em Razão da Matéria

```text
[5483] Processo Penal > Competência > Competência Territorial
Escopo: Competência de foro (ratione loci): definição da comarca ou seção judiciária pelo lugar da infração ou, subsidiariamente, pelo domicílio ou residência do réu, incluindo crimes a distância, plurilocais e cometidos a bordo de embarcações e aeronaves.
Inclui: Teoria do resultado (CPP, art. 70) e lugar da consumação ou do último ato de execução na tentativa; Crimes a distância e foro quando a execução começa ou termina fora do território nacional; Crime continuado ou permanente praticado em mais de um território: fixação pela prevenção; Foro do domicílio ou residência do réu quando o lugar da infração é desconhecido; opção do querelante na ação privada exclusiva; Estelionato mediante depósito, cheque sem fundos ou transferência: foro do domicílio da vítima (CPP, art. 70, § 4º); Teoria da atividade nos Juizados (Lei 9.099/95, art. 63); Crimes cometidos fora do território nacional e a bordo de navios e aeronaves (CPP, arts. 88 a 90)
Não inclui: Aplicação da lei penal brasileira a crimes cometidos no estrangeiro (extraterritorialidade, lugar do crime no CP) → 5182; Justiça competente (Federal, Estadual, Eleitoral, Militar) conforme a natureza da infração → 5482; Distribuição e prevenção entre varas da mesma comarca → 5485; Arguição de incompetência territorial por exceção → 5493; Prorrogação da competência relativa não arguida e foro prevalente na conexão → 5486
Âncoras legais: CPP, arts. 70 a 73; CPP, arts. 88 a 90; CP, art. 6º; Lei 9.099/1995, art. 63
Desempate: Use este nó quando a questão perguntar em qual comarca ou seção judiciária o crime deve ser processado; se a dúvida for qual Justiça (Federal, Estadual etc.) é competente, use 5482.
```

### 5485 · irmão parecido: 5483 Competência Territorial

```text
[5485] Processo Penal > Competência > Competência de Juízo
Escopo: Competência de juízo: definição do órgão julgador dentro do mesmo foro (vara ou juízo), pela distribuição, pela prevenção e pela especialização de varas prevista nas leis de organização judiciária, além da competência funcional por fase do processo.
Inclui: Distribuição quando houver mais de um juiz igualmente competente (CPP, art. 75); Prevenção pela prática de ato ou medida anterior à denúncia (CPP, arts. 75, parágrafo único, e 83); Natureza relativa da nulidade por inobservância da prevenção (Súmula 706 do STF); Varas especializadas criadas por lei de organização judiciária (ex.: varas de crimes contra criança, de lavagem, de organizações criminosas); Competência funcional por fase do processo (conhecimento, execução) e por objeto do juízo; Divisão funcional entre juiz das garantias e juiz da instrução e julgamento sob o prisma da competência
Não inclui: Fixação da comarca pelo lugar da infração ou domicílio do réu → 5483; Prevenção como critério residual de prevalência na conexão ou continência (CPP, art. 78, II, c) → 5486; Atribuições e funcionamento do juiz das garantias no inquérito → 5503; Competência e funcionamento dos Juizados Especiais Criminais → 5540; Competência dos Juizados de Violência Doméstica e Familiar contra a Mulher → 4704
Âncoras legais: CPP, art. 75; CPP, art. 83; Súmula 706 do STF
Desempate: Use este nó quando o foro já estiver definido e a questão tratar de qual vara ou juiz dentro dele julgará (distribuição, prevenção, vara especializada); se a discussão for sobre a comarca, use 5483.
```

### 5482 · irmão parecido: 5483 Competência Territorial

```text
[5482] Processo Penal > Competência > Competência em Razão da Matéria
Escopo: Competência em razão da matéria (ratione materiae): repartição entre as Justiças Federal, Estadual, Eleitoral e Militar e competência constitucional do Tribunal do Júri para os crimes dolosos contra a vida, conforme a natureza da infração.
Inclui: Competência criminal da Justiça Federal (CF, art. 109, IV, V, V-A, VI, IX e X); Crimes contra sociedade de economia mista e contravenções penais: Justiça Estadual (Súmulas 42 e 38 do STJ); Justiça Militar da União e dos Estados (CF, arts. 124 e 125, § 4º); crime doloso contra a vida de civil por militar; Justiça Eleitoral e crimes comuns conexos a crimes eleitorais; Competência do Tribunal do Júri para os crimes dolosos contra a vida (CF, art. 5º, XXXVIII, d; CPP, art. 74, § 1º); Natureza absoluta da competência material e nulidade decorrente
Não inclui: Prevalência da Justiça Federal sobre a Estadual em crimes conexos (Súmula 122 do STJ) e demais regras de conexão → 5486; Incidente de deslocamento de competência para a Justiça Federal (CF, art. 109, § 5º) → 5486; Competência originária de tribunais em razão do cargo do acusado → 5484; Competência dos Juizados Especiais para infrações de menor potencial ofensivo → 5540; Tipificação e elementos dos crimes eleitorais → 4692
Âncoras legais: CF, art. 109, IV a VI, IX e X; CF, art. 124; CF, art. 125, § 4º; CF, art. 5º, XXXVIII, d; CPP, art. 74; Súmula 42 do STJ; Súmula 38 do STJ
Desempate: Use este nó quando a dúvida for qual Justiça ou órgão é competente pela natureza do crime isolado; havendo pluralidade de crimes conexos e discussão sobre qual juízo atrai os demais, use 5486.
```

### 5484 · irmão parecido: 5483 Competência Territorial

```text
[5484] Processo Penal > Competência > Competência por Prerrogativa de Função
Escopo: Competência originária dos tribunais em razão do cargo ou função do acusado (foro por prerrogativa de função), incluindo os tribunais competentes para cada autoridade, os limites temporais e funcionais do foro e sua relação com o Júri e com corréus.
Inclui: Competência originária do STF, STJ, TRF e TJ para julgar autoridades (CF, arts. 102, I, b e c; 105, I, a; 108, I, a; 96, III); Julgamento de prefeitos (CF, art. 29, X; Súmula 702 do STF); Alcance do foro: crimes cometidos no cargo e relacionados às funções (AP 937) e sua manutenção após a saída do cargo segundo o entendimento atual do STF; Foro estabelecido exclusivamente pela Constituição estadual x Tribunal do Júri (Súmula Vinculante 45); Atração de corréu sem prerrogativa por conexão ou continência (Súmula 704 do STF); Exceção da verdade contra autoridade com foro especial (CPP, art. 85); Prerrogativa de função no CPP (CPP, arts. 84 a 87)
Não inclui: Imunidades prisionais e prisão especial de autoridades → 5586; Regras gerais de conexão e continência e separação de processos → 5486; Repartição entre Justiças pela natureza da infração → 5482; Crimes de responsabilidade e abuso de autoridade como tipos penais → 4684
Âncoras legais: CF, art. 102, I, b e c; CF, art. 105, I, a; CF, art. 108, I, a; CF, art. 96, III; CF, art. 29, X; CPP, arts. 84 a 87; Súmula Vinculante 45; Súmula 702 do STF; Súmula 704 do STF
Desempate: Use este nó sempre que o critério decisivo for o cargo ou função do acusado, mesmo que a questão também envolva conexão com corréu ou crime doloso contra a vida.
```

### 5481 · irmão parecido: 5483 Competência Territorial

```text
[5481] Processo Penal > Competência > Espécies e Fixação de Competência Criminal
Escopo: Noções gerais de competência criminal: conceito de jurisdição e competência, critérios do art. 69 do CPP, espécies (material, pessoal, territorial, funcional), competência absoluta e relativa, roteiro de fixação e conflitos de competência.
Inclui: Distinção entre jurisdição e competência e princípio do juiz natural na fixação da competência; Critérios determinantes do CPP, art. 69 e sua enumeração; Classificação: ratione materiae, ratione personae, ratione loci e funcional; Competência absoluta x relativa e consequências da inobservância; Roteiro de fixação: Justiça competente, órgão, foro e juízo; Conflito positivo e negativo de competência e de atribuições (CPP, arts. 113 a 117)
Não inclui: Detalhamento da competência pelo lugar da infração → 5483; Repartição entre Justiças Federal, Estadual, Eleitoral e Militar → 5482; Foro por prerrogativa de função → 5484; Conexão, continência, prorrogação e perpetuatio jurisdictionis → 5486; Exceção de incompetência como questão incidente → 5493; Princípio do juiz natural como princípio processual geral → 5582
Âncoras legais: CPP, art. 69; CPP, arts. 113 a 117; CF, art. 5º, LIII
Desempate: Use este nó para questões sobre o sistema de competência em geral, classificação das espécies ou conflito de competência; se a questão aplicar um critério específico (lugar, matéria, função, juízo, conexão), use o nó desse critério.
```

### 5486 · irmão parecido: 5481 Espécies e Fixação de Competência Criminal

```text
[5486] Processo Penal > Competência > Prorrogação, Perpetuação e Modificação de Competência
Escopo: Alteração da competência originalmente fixada: conexão e continência (espécies, foro prevalente, separação de processos), perpetuatio jurisdictionis, prorrogação da competência relativa e hipóteses de deslocamento, como o desaforamento e o IDC.
Inclui: Conexão intersubjetiva, objetiva e instrumental (CPP, art. 76) e continência (CPP, art. 77); Regras de foro prevalente (CPP, art. 78), inclusive Júri x jurisdição comum e prevenção residual; Prevalência da Justiça Federal em crimes conexos (Súmula 122 do STJ); Separação obrigatória e facultativa de processos (CPP, arts. 79 e 80); Perpetuatio jurisdictionis após absolvição ou desclassificação (CPP, art. 81); Prorrogação da competência relativa não arguida oportunamente; Incidente de deslocamento de competência (CF, art. 109, § 5º) e desaforamento como hipóteses de modificação
Não inclui: Atração de corréu pelo foro por prerrogativa de função → 5484; Prevenção e distribuição como critérios originários de fixação do juízo → 5485; Procedimento do desaforamento na organização do Júri → 5528; Exceção de incompetência e seu processamento → 5493; Concurso de crimes no Código Penal (material, formal, continuado) → 5066
Âncoras legais: CPP, arts. 76 a 82; CPP, arts. 427 e 428; CF, art. 109, § 5º; Súmula 122 do STJ
Desempate: Use este nó quando a questão tratar de reunião ou separação de processos, foro prevalente ou alteração da competência já fixada; se o foco for o deslocamento por prerrogativa de função, use 5484, e se for o rito do desaforamento dentro do Júri, use 5528.
```

### 5487 · irmão parecido: 5583 Sujeitos do Processo

```text
[5487] Processo Penal > Comunicação dos Atos Processuais
Escopo: Formas de cientificar as partes e demais sujeitos dos atos processuais penais: citação, intimação e notificação, com requisitos, espécies, efeitos e contagem de prazos. Todas as partes têm subtema próprio.
Inclui: Citação pessoal por mandado e por carta precatória ou rogatória; Citação por hora certa e por edital; Suspensão do processo e do prazo prescricional do réu citado por edital (CPP, art. 366); Intimação pessoal e pela imprensa oficial; Intimação do defensor público, do dativo e do MP; Contagem de prazos processuais penais (CPP, art. 798)
Não inclui: Nulidade por falta ou defeito de citação → 5511; Resposta à acusação após a citação no rito ordinário → 5533; Tempestividade do recurso → 5514; Suspensão da prescrição como instituto material → 5187
Âncoras legais: CPP, arts. 351 a 372; CPP, art. 366; CPP, art. 798
```

### 5488 · irmão parecido: 5489 Intimação e Contagem dos Prazos

```text
[5488] Processo Penal > Comunicação dos Atos Processuais > Citação e Contagem dos Prazos
Escopo: Citação no processo penal: conceito, modalidades (pessoal, por mandado, precatória, rogatória, hora certa e edital), efeitos, revelia, suspensão do processo e da prescrição (art. 366), e contagem dos prazos que correm a partir da citação.
Inclui: Citação pessoal por mandado, carta precatória e carta rogatória (réu no estrangeiro em lugar sabido, com suspensão da prescrição); Citação de réu preso, militar e funcionário público; Citação por hora certa em caso de ocultação do réu; Citação por edital (prazo de 15 dias) e Súmulas 351 e 366 do STF; Art. 366 do CPP: suspensão do processo e da prescrição, produção antecipada de provas e prisão preventiva; Súmulas 415 e 455 do STJ; Revelia (art. 367) e completa formação da relação processual com a citação (art. 363); Contagem do prazo de 10 dias para a resposta à acusação a partir da citação
Não inclui: Conteúdo e processamento da resposta à acusação → 5533; Intimação de partes, defensores e MP e prazos que correm da intimação → 5489; Nulidade por falta ou vício de citação (art. 564, III, e) → 5511; Impossibilidade de citação por edital no JECRIM e remessa ao juízo comum → 5540; Regras gerais de suspensão e interrupção da prescrição fora do art. 366 → 5187
Âncoras legais: CPP, arts. 351 a 369; CPP, art. 396; CPP, art. 798; Lei 9.099/1995, art. 66
Desempate: Escolha este nó quando o ato de comunicação for a citação do acusado (chamamento inicial ao processo) ou quando o prazo discutido correr a partir dela; se o ato for intimação ou notificação para os demais atos, use 5489.
```

### 5489 · irmão parecido: 5488 Citação e Contagem dos Prazos

```text
[5489] Processo Penal > Comunicação dos Atos Processuais > Intimação e Contagem dos Prazos
Escopo: Intimação e notificação no processo penal: formas de intimação do réu, defensor constituído ou dativo, Defensoria, MP, querelante e assistente; intimação da sentença; e regras gerais de contagem dos prazos processuais penais a partir da intimação (art. 798 do CPP).
Inclui: Intimação por publicação no órgão oficial do defensor constituído, do advogado do querelante e do assistente (art. 370, §1º); Intimação pessoal do MP e do defensor nomeado; intimação pessoal e prazo em dobro da Defensoria Pública; Intimação da sentença ao réu e ao defensor (arts. 390 a 392); Prazos contínuos e peremptórios, exclusão do dia do começo e prorrogação para dia útil (art. 798); Súmula 710 do STF: prazo conta da intimação, não da juntada do mandado ou da precatória; Intimação da expedição de carta precatória (Súmula 155 do STF e Súmula 273 do STJ)
Não inclui: Citação do acusado e prazo para a resposta à acusação → 5488; Tempestividade e prazos específicos de cada recurso como requisito de admissibilidade → 5514; Nulidade por falta de intimação para ato processual (art. 564, III, o) → 5511; Intimação da pronúncia no procedimento do júri → 5527
Âncoras legais: CPP, arts. 370 a 372; CPP, arts. 390 a 392; CPP, art. 798; LC 80/1994, art. 44, I
Desempate: Escolha este nó quando a questão tratar de intimação/notificação ou da contagem geral de prazos processuais (art. 798, Súmula 710 do STF) sem relação com a citação; se o prazo correr da citação, use 5488; se o foco for a tempestividade de um recurso, use 5514.
```

### 5490 · irmão parecido: 5583 Sujeitos do Processo

```text
[5490] Processo Penal > Das Questões e Processos Incidentes
Escopo: Questões e processos incidentes do CPP: questões prejudiciais, exceções, restituição de coisas apreendidas, medidas assecuratórias e incidentes de falsidade e de insanidade mental. Todas as partes têm subtema próprio, exceto o conflito de jurisdição, que vai para Competência.
Inclui: Questões prejudiciais obrigatórias e facultativas; Exceções de suspeição, impedimento e incompatibilidade; Exceções de incompetência, ilegitimidade, litispendência e coisa julgada; Restituição de coisas apreendidas; Sequestro, hipoteca legal e arresto; Incidente de falsidade documental; Incidente de insanidade mental do acusado
Não inclui: Conflito de competência e regras de fixação da competência → 5480; Inimputabilidade por doença mental como causa de exclusão da culpabilidade → 5213; Busca e apreensão como meio de prova → 5554; Medidas assecuratórias da Lei de Lavagem de Dinheiro → 4702; Hipóteses de impedimento e suspeição do juiz como sujeito processual → 5583
Âncoras legais: CPP, arts. 92 a 154
```

### 5493 · irmão parecido: 5494 Exceção de Litispendência e de Coisa Julgada

```text
[5493] Processo Penal > Das Questões e Processos Incidentes > Exceção de Incompetência e de Ilegitimidade
Escopo: Exceções de incompetência do juízo e de ilegitimidade de parte (ad causam e ad processum) como incidentes processuais: cabimento, prazo, forma de arguição, declaração de ofício, processamento e efeitos.
Inclui: Exceção de incompetência: prazo de defesa, forma verbal ou escrita e oitiva do MP (CPP, art. 108); Declaração de ofício da incompetência pelo juiz (CPP, art. 109); Remessa dos autos ao juízo competente e ratificação dos atos; Exceção de ilegitimidade de parte: ad causam e ad processum (CPP, art. 110); Aplicação às exceções de ilegitimidade do rito da exceção de incompetência; Recurso cabível contra a decisão que julga procedente a exceção (RESE)
Não inclui: Critérios de fixação da competência e conflito de competência → 5481; Competência territorial pelo lugar da infração ou domicílio do réu → 5483; Nulidade por incompetência ou ilegitimidade de parte (CPP, art. 564) → 5511; Rejeição da denúncia por falta de pressuposto processual ou condição da ação → 5531; Condições da ação penal (legitimidade em abstrato) → 5467
Âncoras legais: CPP, art. 95, II e IV; CPP, arts. 108 a 110; CPP, art. 581, II e III
Desempate: Use este nó quando a questão tratar do meio de arguir a incompetência ou a ilegitimidade (exceção, prazo, processamento); se versar sobre qual juízo é competente, use os nós de Competência (5480 e filhos).
```

### 5494 · irmão parecido: 5493 Exceção de Incompetência e de Ilegitimidade

```text
[5494] Processo Penal > Das Questões e Processos Incidentes > Exceção de Litispendência e de Coisa Julgada
Escopo: Exceções de litispendência e de coisa julgada no CPP: conceito, identidade de demandas, forma de arguição, processamento e efeitos da procedência, inclusive o reconhecimento de ofício.
Inclui: Litispendência: duas ações penais em curso pelo mesmo fato contra o mesmo réu; Exceção de coisa julgada: fato já julgado por sentença definitiva; Limite da coisa julgada: só em relação ao fato principal objeto da sentença (CPP, art. 110, § 2º); Processamento pelo rito da exceção de incompetência (CPP, art. 110); Reconhecimento de ofício e extinção do segundo processo; Recurso contra a decisão que julga procedente a exceção de coisa julgada (RESE)
Não inclui: Princípio do ne bis in idem como princípio processual geral → 5582; Revisão criminal contra sentença condenatória transitada em julgado → 5478; Efeitos da sentença penal condenatória → 5577; Lei penal mais benéfica após o trânsito em julgado → 5181
Âncoras legais: CPP, art. 95, III e V; CPP, art. 110; CPP, art. 581, III
```

### 5492 · irmão parecido: 5493 Exceção de Incompetência e de Ilegitimidade

```text
[5492] Processo Penal > Das Questões e Processos Incidentes > Exceção de Suspeição, de Impedimento ou de Incompatibilidade
Escopo: Exceções de suspeição, impedimento e incompatibilidade do juiz, do MP, de peritos, intérpretes, serventuários e jurados: hipóteses legais, procedimento, precedência e efeitos.
Inclui: Precedência da arguição de suspeição sobre as demais exceções (CPP, art. 96); Reconhecimento espontâneo da suspeição pelo juiz (CPP, art. 97); Procedimento da exceção e julgamento pelo tribunal (CPP, arts. 98 a 103); Suspeição do MP, peritos, intérpretes, serventuários e jurados (CPP, arts. 104 a 106); Impossibilidade de opor suspeição às autoridades policiais (CPP, art. 107); Hipóteses de impedimento e de suspeição do juiz (CPP, arts. 252 e 254); Incompatibilidades e impedimentos (CPP, art. 112)
Não inclui: Impedimento do juiz das garantias para a fase processual → 5503; Recusa de jurados e composição do Conselho de Sentença → 5528; Poderes e deveres gerais do juiz e das partes como sujeitos processuais → 5583; Nulidade decorrente de suspeição do juiz (CPP, art. 564, I) → 5511
Âncoras legais: CPP, arts. 95 a 107; CPP, art. 112; CPP, arts. 252 a 256; CPP, art. 258
Desempate: Use este nó para hipóteses e arguição de suspeição/impedimento; se a questão tratar das atribuições gerais do juiz ou do MP sem foco na parcialidade, use 5583.
```

### 5498 · irmão parecido: 5583 Sujeitos do Processo

```text
[5498] Processo Penal > Inquérito Policial
Escopo: Investigação preliminar: conceito e características do inquérito policial, procedimento, conclusão e arquivamento, juiz das garantias, acordo de não persecução penal e inquérito civil. Todas as partes têm subtema próprio.
Inclui: Características do IP: inquisitivo, escrito, sigiloso, dispensável, indisponível; Instauração de ofício, por requisição ou a requerimento; Diligências da autoridade policial e indiciamento; Prazos de conclusão e relatório; Arquivamento do IP (CPP, art. 28); Juiz das garantias; Acordo de não persecução penal (CPP, art. 28-A)
Não inclui: Prisão temporária decretada na investigação → 5520; Interceptação telefônica → 5555; Identificação criminal (Lei 12.037/2009) → 4699; Transação penal → 5541; Audiência de custódia → 5589
Âncoras legais: CPP, arts. 3º-A a 3º-F; CPP, arts. 4º a 23; CPP, art. 28; CPP, art. 28-A; Lei 12.830/2013
```

### 5501 · irmão parecido: 5500 Procedimento do Inquérito Policial

```text
[5501] Processo Penal > Inquérito Policial > Conclusão e Arquivamento do Inquérito Policial
Escopo: Encerramento do inquérito policial: relatório da autoridade, remessa e providências do MP, arquivamento (sistemática do art. 28 do CPP), coisa julgada do arquivamento e desarquivamento por novas provas.
Inclui: Relatório final da autoridade policial e remessa ao juízo/MP; Devolução do inquérito para diligências imprescindíveis; Vedação de a autoridade policial arquivar o inquérito; Arquivamento pelo MP, comunicação à vítima e revisão pela instância superior (art. 28, redação da Lei 13.964/2019 e ADIs 6298 e outras); Desarquivamento diante de novas provas (Súmula 524 do STF); Arquivamento por atipicidade ou extinção da punibilidade e coisa julgada material; Arquivamento implícito e indireto
Não inclui: Prazos para conclusão do inquérito com investigado preso ou solto → 5500; Recusa do MP em propor ANPP e remessa ao órgão superior → 5502; Requisitos e prazo para oferecimento da denúncia → 5473; Princípio da obrigatoriedade da ação penal pública → 5469
Âncoras legais: CPP, art. 10, §§ 1º a 3º; CPP, art. 16; CPP, art. 17; CPP, art. 18; CPP, art. 28; Súmula 524 do STF
Desempate: Escolha este nó quando a questão tratar do que ocorre ao fim do IP (relatório, arquivamento, desarquivamento); prazos de duração e diligências em curso ficam em 5500.
```

### 5504 · irmão parecido: 5500 Procedimento do Inquérito Policial

```text
[5504] Processo Penal > Inquérito Policial > Inquérito Civil
Escopo: Inquérito civil: procedimento investigatório administrativo instaurado e presidido pelo Ministério Público para colher elementos para ação civil pública, com seu arquivamento e controle pelo Conselho Superior.
Inclui: Instauração e presidência exclusiva pelo Ministério Público; Finalidade de instruir ação civil pública na tutela de interesses difusos e coletivos; Caráter dispensável e inquisitivo do inquérito civil; Requisição de certidões, informações e perícias; Arquivamento e homologação pelo Conselho Superior do MP; Compromisso de ajustamento de conduta no curso do inquérito civil; Crime de recusa, retardamento ou omissão de dados requisitados pelo MP (Lei 7.347/1985, art. 10)
Não inclui: Características gerais do inquérito policial → 5499; Arquivamento do inquérito policial pelo art. 28 do CPP → 5501; Ação civil ex delicto para reparação do dano causado pelo crime → 5475; Investigação criminal conduzida pela autoridade policial → 5500
Âncoras legais: CF, art. 129, III; Lei 7.347/1985, art. 8º, § 1º; Lei 7.347/1985, art. 9º; Lei 7.347/1985, art. 10
Desempate: Use este nó quando a investigação for civil, do MP, voltada à ação civil pública; investigação de infração penal fica nos demais filhos de 5498.
```

### 5500 · irmão parecido: 5501 Conclusão e Arquivamento do Inquérito Policial

```text
[5500] Processo Penal > Inquérito Policial > Procedimento do Inquérito Policial
Escopo: Tramitação do inquérito policial: formas de instauração (notitia criminis, requisição, requerimento, representação), diligências da autoridade policial, indiciamento, incomunicabilidade e prazos de conclusão.
Inclui: Instauração de ofício, por requisição do juiz ou MP, requerimento do ofendido e auto de prisão em flagrante; Necessidade de representação ou requerimento nos crimes de ação pública condicionada ou privada; Diligências do art. 6º do CPP e reprodução simulada dos fatos; Indiciamento como ato privativo do delegado (Lei 12.830/2013); Prazos de conclusão: 10 dias preso e 30 dias solto (CPP) e prazos especiais; Requerimento de diligências pelo ofendido e indeferimento pela autoridade; Incomunicabilidade do indiciado e sua não recepção; Requisição de dados e informações pela autoridade (arts. 13-A e 13-B)
Não inclui: Características gerais e natureza do inquérito → 5499; Relatório final, arquivamento e desarquivamento → 5501; Interceptação telefônica durante a investigação → 5555; Busca e apreensão domiciliar → 5554; Identificação criminal do civilmente identificado → 4699; Lavratura e requisitos da prisão em flagrante → 5518
Âncoras legais: CPP, art. 5º; CPP, art. 6º; CPP, art. 7º; CPP, art. 10; CPP, art. 13; CPP, art. 13-A; CPP, art. 13-B; CPP, art. 14; CPP, art. 21; Lei 12.830/2013, art. 2º, § 6º
Desempate: Use este nó para atos de instauração e tramitação do IP; se a questão detalhar um meio de prova específico (interceptação, busca, perícia), use o nó da prova em espécie.
```

### 5505 · irmão parecido: 5580 Sistemas e Princípios Processuais Penais

```text
[5505] Processo Penal > Lei Processual no Tempo e no Espaço
Escopo: Aplicação da lei processual penal no tempo e no espaço e sua interpretação: tempus regit actum, normas mistas, territorialidade e interpretação extensiva e analógica. Todas as partes têm subtema próprio.
Inclui: Aplicação imediata da lei processual (CPP, art. 2º); Validade dos atos praticados sob a lei anterior; Normas processuais materiais ou mistas; Territorialidade da lei processual penal (CPP, art. 1º); Interpretação extensiva e analogia (CPP, art. 3º)
Não inclui: Retroatividade da lei penal benéfica e abolitio criminis → 5181; Territorialidade e extraterritorialidade da lei penal → 5182; Interpretação da norma penal material → 5173; Competência territorial (lugar da infração) → 5483
Âncoras legais: CPP, art. 1º; CPP, art. 2º; CPP, art. 3º
Desempate: Use este nó quando a questão tratar da aplicação da norma processual (tempus regit actum, normas mistas); se tratar da retroatividade da lei penal material, use Lei penal no Tempo (5181).
```

### 5508 · irmão parecido: 5506 Lei Processual no Espaço

```text
[5508] Processo Penal > Lei Processual no Tempo e no Espaço > Interpretação da Lei processual Penal
Escopo: Formas e métodos de interpretação da lei processual penal e integração de lacunas: interpretação extensiva, aplicação analógica, analogia e suplemento dos princípios gerais de direito admitidos pelo art. 3º do CPP.
Inclui: Admissão de interpretação extensiva e aplicação analógica na lei processual penal (CPP, art. 3º); Admissão da analogia no processo penal, inclusive in malam partem, em contraste com o Direito Penal material; Suplemento dos princípios gerais de direito para integrar lacunas; Distinção entre interpretação extensiva, interpretação analógica e analogia no processo penal; Classificação da interpretação quanto ao sujeito, ao meio e ao resultado aplicada à norma processual; Aplicação subsidiária do CPC ao processo penal por analogia
Não inclui: Interpretação da norma penal material e vedação da analogia in malam partem no CP → 5173; Aplicação da lei processual no tempo e normas processuais híbridas → 5507; Princípios do processo penal em geral (contraditório, ampla defesa, presunção de inocência) → 5582
Âncoras legais: CPP, art. 3º
Desempate: Use este nó quando a questão tratar de como interpretar ou integrar a norma processual penal (CPP, art. 3º); se tratar de interpretação ou analogia na lei penal material, use 5173.
```

### 5506 · irmão parecido: 5507 Lei processual no Tempo

```text
[5506] Processo Penal > Lei Processual no Tempo e no Espaço > Lei Processual no Espaço
Escopo: Aplicação da lei processual penal no espaço: princípio da territorialidade (lex fori) do art. 1º do CPP e suas ressalvas (tratados, prerrogativas constitucionais, crimes de responsabilidade, justiça militar, tribunal especial, legislação especial).
Inclui: Princípio da territorialidade absoluta da lei processual penal (lex fori); Ressalvas do art. 1º do CPP: tratados, convenções e regras de direito internacional; Ressalvas quanto a prerrogativas constitucionais e crimes de responsabilidade; Processos da competência da Justiça Militar e de tribunal especial como exceções ao CPP; Aplicação do CPP a processos regidos por lei especial quando esta não dispuser de modo diverso (CPP, art. 1º, parágrafo único); Atos processuais praticados no exterior (cartas rogatórias) e aplicação da lei do foro
Não inclui: Lei penal no espaço: territorialidade e extraterritorialidade do CP (arts. 5º a 7º) → 5182; Fixação da competência pelo lugar da infração ou domicílio do réu → 5483; Aplicação da lei processual penal no tempo → 5507; Competência por prerrogativa de função → 5484
Âncoras legais: CPP, art. 1º
Desempate: Use este nó quando a questão perguntar qual lei processual rege o processo conforme o território (CPP, art. 1º); se perguntar onde o crime se considera praticado ou a extraterritorialidade da lei penal, use 5182; se perguntar qual foro é competente, use 5483.
```

### 5507 · irmão parecido: 5506 Lei Processual no Espaço

```text
[5507] Processo Penal > Lei Processual no Tempo e no Espaço > Lei processual no Tempo
Escopo: Aplicação da lei processual penal no tempo: princípio tempus regit actum, aplicação imediata e validade dos atos já praticados (CPP, art. 2º), além do tratamento intertemporal das normas mistas ou híbridas.
Inclui: Princípio da aplicação imediata (tempus regit actum) e validade dos atos praticados sob a lei anterior; Irretroatividade da norma processual pura, ainda que mais gravosa ao réu; Normas processuais mistas ou híbridas e retroatividade do conteúdo material benéfico; Direito intertemporal das alterações da Lei 13.964/2019 (ex.: retroatividade do ANPP e da representação no estelionato); Regras de transição da Lei de Introdução ao CPP; Lei nova sobre prazos e recursos: aplica-se a lei vigente na data da decisão ou da intimação
Não inclui: Lei penal no tempo: retroatividade benéfica e ultratividade da lei penal material → 5181; Abolitio criminis como causa extintiva da punibilidade → 5194; Requisitos e cabimento do acordo de não persecução penal → 5502; Aplicação da lei processual penal no espaço → 5506; Interpretação extensiva e analogia na lei processual → 5508
Âncoras legais: CPP, art. 2º; CF, art. 5º, XL; Decreto-Lei 3.931/1941
Desempate: Use este nó quando a questão tratar da sucessão de normas processuais ou híbridas no tempo; se a norma for exclusivamente penal material (pena, tipo, extinção da punibilidade), use 5181.
```

### 5510 · irmão parecido: 5511 Nulidades em Espécie

```text
[5510] Processo Penal > Nulidades > Nulidade Absoluta e Relativa
Escopo: Teoria geral das nulidades no processo penal: distinção entre nulidade absoluta e relativa (e entre irregularidade e inexistência), princípios que regem a declaração da nulidade, momento de arguição, preclusão, convalidação e efeitos da decretação.
Inclui: Diferença entre nulidade absoluta (prejuízo presumido, arguível a qualquer tempo) e relativa (exige prova do prejuízo e arguição oportuna); Princípio do prejuízo (pas de nullité sans grief) e Súmula 523 STF na parte da regra geral; Princípio do interesse: a parte não pode arguir nulidade a que deu causa; Instrumentalidade das formas e princípio da causalidade ou consequencialidade (art. 573, §1º); Momentos de arguição das nulidades relativas e sua preclusão (art. 571); Convalidação ou sanação das nulidades relativas (art. 572); Súmula 160 STF: nulidade não arguida no recurso da acusação não pode ser reconhecida contra o réu; Atos inexistentes e meras irregularidades em contraste com atos nulos
Não inclui: Vícios específicos do rol do art. 564 do CPP e as súmulas sobre cada um (falta de citação, de defesa, de quesito obrigatório etc.) → 5511; Provas ilícitas e ilícitas por derivação, com o seu desentranhamento → 5594; Exceção de incompetência como meio processual de arguição → 5493; Exceção de suspeição ou de impedimento do juiz → 5492; Princípios gerais do processo penal, como devido processo legal e ampla defesa, quando não estão ligados ao regime das nulidades → 5582; Revisão criminal ou habeas corpus como via para anular o processo → 5478
Âncoras legais: CPP, arts. 563 a 566; CPP, arts. 571 a 573; Súmula 523 STF; Súmula 160 STF
Desempate: Escolha este nó quando a questão tratar do regime geral (classificação, princípios, preclusão, convalidação, efeitos) sem que o centro seja um vício concreto; se a questão perguntar se um defeito específico gera nulidade ou qual a sua natureza, use 5511.
```

### 5511 · irmão parecido: 5510 Nulidade Absoluta e Relativa

```text
[5511] Processo Penal > Nulidades > Nulidades em Espécie
Escopo: Hipóteses concretas de nulidade no processo penal: o rol do art. 564 do CPP e os vícios específicos reconhecidos pela jurisprudência e por súmulas, com a sua natureza (absoluta ou relativa) e as suas consequências.
Inclui: Rol do art. 564 do CPP: incompetência, suspeição, ilegitimidade de parte, falta de fórmulas ou termos essenciais; Falta ou nulidade da citação, do interrogatório ou da intimação (art. 564, III) e o seu suprimento pelo comparecimento (art. 570); Falta de defesa versus deficiência de defesa no caso concreto (Súmula 523 STF); Nulidades no Júri: falta de quesito obrigatório e quesitos da defesa (Súmulas 156 e 162 STF); nulidades posteriores à pronúncia; Súmula 706 STF: a inobservância da competência por prevenção gera nulidade relativa; Súmula 707 STF: falta de intimação do denunciado para as contrarrazões ao recurso contra a rejeição da denúncia; Súmula 155 STF: falta de intimação da expedição de precatória gera nulidade relativa; Súmula 712 STF: nulidade do desaforamento sem audiência da defesa
Não inclui: Conceito e distinção entre nulidade absoluta e relativa, princípios do prejuízo e do interesse, preclusão e convalidação em abstrato → 5510; Provas obtidas por meios ilícitos e teoria dos frutos da árvore envenenada → 5594; Regras sobre a forma da citação e a contagem dos prazos, sem discussão de nulidade → 5488; Violação da correlação entre acusação e sentença por emendatio ou mutatio libelli → 5579; Regras de fixação da competência, quando a questão não discute a nulidade → 5481
Âncoras legais: CPP, art. 564; CPP, arts. 567 a 570; Súmula 155 STF; Súmula 156 STF; Súmula 162 STF; Súmula 523 STF; Súmula 706 STF; Súmula 707 STF; Súmula 712 STF
Desempate: Escolha este nó quando a questão apresentar um vício concreto e perguntar se ele gera nulidade ou de que tipo; use 5510 quando a questão cobrar só a teoria geral ou os princípios das nulidades.
```

### 5512 · irmão parecido: 5584 Teoria Geral das Prisões

```text
[5512] Processo Penal > Parte Geral dos Recursos
Escopo: Teoria geral dos recursos no processo penal: conceito, classificação, pressupostos de admissibilidade, efeitos e princípios recursais. Todas as partes têm subtema próprio; recursos específicos ficam em Recursos em Espécie.
Inclui: Pressupostos objetivos (cabimento, tempestividade, adequação) e subjetivos (legitimidade, interesse); Recursos voluntários e de ofício; Efeitos devolutivo, suspensivo, regressivo e extensivo; Proibição da reformatio in pejus (CPP, art. 617); Fungibilidade, taxatividade e unirrecorribilidade; Desistência do recurso pelo MP (CPP, art. 576)
Não inclui: Recursos em espécie: cabimento e prazo de recurso específico → 5560; Recurso em sentido estrito → 5561; Apelação → 5562; Habeas corpus e revisão criminal → 5476; Recursos no âmbito dos Juizados Especiais → 5569
Âncoras legais: CPP, arts. 574 a 580; CPP, art. 617
Desempate: Use este nó para princípios, pressupostos e efeitos comuns a todos os recursos; se a questão tratar do cabimento, prazo ou processamento de um recurso determinado, use Recursos em Espécie (5560).
```

### 5516 · irmão parecido: 5515 Efeito dos Recursos

```text
[5516] Processo Penal > Parte Geral dos Recursos > Classificação dos Recursos
Escopo: Critérios gerais de classificação dos recursos no processo penal: quanto à iniciativa (voluntário ou de ofício), à fundamentação (livre ou vinculada), à extensão (total ou parcial), à natureza (ordinário ou extraordinário) e ao órgão que julga.
Inclui: Recurso voluntário x recurso de ofício (reexame necessário) e suas hipóteses legais; Recursos ordinários x extraordinários (excepcionais); Recursos de fundamentação livre x de fundamentação vinculada; Recurso total x parcial (impugnação de todo ou de parte da decisão); Recursos iterativos, reiterativos e mistos, conforme o órgão que reexamina; Natureza jurídica do recurso como desdobramento do direito de ação e distinção das ações autônomas de impugnação
Não inclui: Classificação dos recursos pelos efeitos (devolutivo, suspensivo, regressivo, extensivo) → 5515; Voluntariedade e demais princípios recursais tratados como princípio → 5513; Cabimento e requisitos de um recurso específico (RESE, apelação etc.) → 5561; Revisão criminal como ação autônoma de impugnação → 5478; Requisitos e cabimento do recurso extraordinário em espécie → 5570
Âncoras legais: CPP, art. 574; CPP, art. 599
Desempate: Use este nó quando a questão pedir o enquadramento do recurso numa categoria (de ofício/voluntário, ordinário/extraordinário, total/parcial, livre/vinculado); se o critério for o efeito produzido, use 5515, e se a voluntariedade for cobrada como princípio, use 5513.
```

### 5515 · irmão parecido: 5516 Classificação dos Recursos

```text
[5515] Processo Penal > Parte Geral dos Recursos > Efeito dos Recursos
Escopo: Efeitos produzidos pela interposição dos recursos no processo penal: devolutivo, suspensivo, regressivo (iterativo ou diferido), extensivo e translativo, além dos limites da devolução da matéria ao tribunal.
Inclui: Efeito devolutivo e a máxima tantum devolutum quantum appellatum; Efeito suspensivo: recursos que o têm e os que não o têm; apelação contra sentença condenatória x absolutória; Efeito regressivo, iterativo ou diferido (juízo de retratação no RESE); Efeito extensivo: aproveitamento por corréus da decisão fundada em motivos não exclusivamente pessoais; Efeito translativo e conhecimento de ofício de matérias de ordem pública; Efeito do recurso sobre a prisão e a liberdade do réu
Não inclui: Proibição da reformatio in pejus, direta ou indireta → 5513; Hipóteses de cabimento e processamento do RESE → 5561; Prazos e processamento da apelação → 5562; Efeito interruptivo dos embargos de declaração no seu regime próprio → 5565; Recurso voluntário x de ofício como critério de classificação → 5516
Âncoras legais: CPP, art. 580; CPP, art. 589; CPP, art. 584; CPP, art. 597
Desempate: Use este nó quando a questão tratar de quais efeitos um recurso produz ou dos limites da devolução; se a questão for sobre a vedação de piora da situação do réu, use 5513.
```

### 5517 · irmão parecido: 5543 Provas em Espécies

```text
[5517] Processo Penal > Prisões em Espécie
Escopo: Modalidades de prisão cautelar e alternativas: prisão em flagrante, preventiva, temporária, domiciliar, medidas cautelares diversas e liberdade provisória. Todas as partes têm subtema próprio.
Inclui: Hipóteses de flagrante e conversão em preventiva; Pressupostos e fundamentos da prisão preventiva; Prisão temporária (Lei 7.960/1989); Prisão domiciliar substitutiva; Medidas cautelares diversas da prisão (CPP, art. 319); Liberdade provisória com ou sem fiança
Não inclui: Conceito e espécies gerais de prisão → 5585; Audiência de custódia → 5589; Relaxamento da prisão ilegal → 5588; Imunidades prisionais e prisão especial → 5586; Regimes de cumprimento da pena privativa de liberdade → 5201; Habeas corpus contra prisão ilegal → 5477
Âncoras legais: CPP, arts. 282 a 350; CPP, arts. 301 a 310; CPP, arts. 311 a 316; CPP, art. 319; Lei 7.960/1989
Desempate: Use este nó quando a questão tratar de uma modalidade específica de prisão ou cautelar; para conceito, garantias gerais, custódia ou relaxamento, use Teoria Geral das Prisões (5584).
```

### 5521 · irmão parecido: 5518 Prisão em Flagrante

```text
[5521] Processo Penal > Prisões em Espécie > Prisão Domiciliar
Escopo: Prisão domiciliar cautelar, substitutiva da preventiva: hipóteses do art. 318 do CPP, regime especial de gestantes, mães e responsáveis por crianças ou pessoas com deficiência (arts. 318-A e 318-B) e prova idônea dos requisitos.
Inclui: Conceito: recolhimento na residência, só saindo com autorização judicial (CPP, art. 317); Hipóteses do art. 318: maior de 80 anos, doença grave, gestante, mãe ou responsável por criança menor de 12 anos ou pessoa com deficiência; Substituição obrigatória para gestante e mãe (art. 318-A) e exceções (violência ou grave ameaça, crime contra filho ou dependente); HC coletivo 143.641/STF; Cumulação com cautelares diversas (art. 318-B); Exigência de prova idônea dos requisitos
Não inclui: Prisão domiciliar na execução da pena (regime aberto, LEP, art. 117) → 4703; Recolhimento domiciliar noturno como cautelar do art. 319, V → 5522; Requisitos para a decretação da preventiva → 5519; Prisão especial e sala de Estado-Maior → 5586
Âncoras legais: CPP, arts. 317 e 318; CPP, art. 318-A; CPP, art. 318-B
Desempate: Use este nó para a domiciliar substitutiva da preventiva (CPP); se for a domiciliar na execução da pena definitiva (LEP), use Lei de Execução Penal (4703).
```

### 5519 · irmão parecido: 5520 Prisão Temporária

```text
[5519] Processo Penal > Prisões em Espécie > Prisão Preventiva
Escopo: Prisão preventiva: legitimidade para requerer, pressupostos (fumus comissi delicti e periculum libertatis), fundamentos, hipóteses de admissibilidade, fundamentação, revisão periódica, revogação e nova decretação.
Inclui: Decretação só a requerimento do MP, do querelante, do assistente ou por representação da autoridade policial, vedada de ofício (CPP, art. 311); Fundamentos: garantia da ordem pública e da ordem econômica, conveniência da instrução criminal, aplicação da lei penal, perigo gerado pela liberdade do imputado; Hipóteses do art. 313: crime doloso com pena máxima superior a 4 anos, reincidência, violência doméstica, dúvida sobre a identidade; Vedação como antecipação de pena e em caso de excludente de ilicitude (art. 314); Fundamentação concreta e contemporânea (art. 315); Revisão a cada 90 dias e revogação (art. 316); Conversão do flagrante em preventiva
Não inclui: Prisão temporária na investigação (Lei 7.960/1989) → 5520; Substituição da preventiva por domiciliar → 5521; Cautelares alternativas do art. 319 → 5522; Classificação geral das prisões (pena x cautelar) → 5585; Audiência de custódia → 5589
Âncoras legais: CPP, art. 282, § 6º; CPP, arts. 311 a 316; CPP, art. 310, II
Desempate: Use este nó quando a questão tratar dos requisitos ou da manutenção da preventiva, inclusive quando o flagrante é convertido nela; se tratar da homologação do auto de flagrante, use Prisão em Flagrante (5518).
```

### 5520 · irmão parecido: 5521 Prisão Domiciliar

```text
[5520] Processo Penal > Prisões em Espécie > Prisão Temporária
Escopo: Prisão temporária, cautelar exclusiva da fase de investigação, prevista na Lei 7.960/1989: hipóteses de cabimento, rol de crimes, prazos (5 + 5 dias e 30 + 30 nos hediondos), legitimidade e procedimento.
Inclui: Hipóteses do art. 1º da Lei 7.960/1989 e a combinação exigida pelo STF (ADI 4109); Rol de crimes que admitem a temporária; Prazo de 5 dias prorrogável por igual período e 30 + 30 dias nos crimes hediondos e equiparados; Vedação de decretação de ofício; representação da autoridade policial ou requerimento do MP; Prazo de 24 horas para decidir e soltura automática ao fim do prazo; Cabimento apenas no inquérito, nunca na ação penal
Não inclui: Prisão preventiva e seus fundamentos → 5519; Demais aspectos da Lei de Crimes Hediondos → 4693; Tramitação e prazos do inquérito policial → 5500; Competência do juiz das garantias → 5503
Âncoras legais: Lei 7.960/1989, arts. 1º e 2º; Lei 8.072/1990, art. 2º, § 4º
Desempate: Use este nó quando a questão tratar da prisão da Lei 7.960/1989 ou do prazo de 30 dias da Lei 8.072/1990; se tratar dos demais efeitos processuais da Lei dos Crimes Hediondos, use 4693.
```

### 5518 · irmão parecido: 5521 Prisão Domiciliar

```text
[5518] Processo Penal > Prisões em Espécie > Prisão em Flagrante
Escopo: Prisão em flagrante: sujeitos (flagrante facultativo e obrigatório), espécies de flagrante, flagrante em crime permanente, lavratura do auto, comunicações, nota de culpa e providências do juiz ao receber o auto.
Inclui: Flagrante facultativo (qualquer do povo) e obrigatório (autoridades policiais e seus agentes) (CPP, art. 301); Flagrante próprio, impróprio e presumido (art. 302); Flagrante preparado (Súmula 145/STF), esperado, forjado e diferido; Flagrante em crime permanente (art. 303); Lavratura do auto, oitivas, nota de culpa em 24 horas e comunicação ao juiz, ao MP, à família e à Defensoria; Decisão do juiz sobre o auto: relaxar, converter ou conceder liberdade provisória (art. 310); Restrições ao flagrante (infração de menor potencial ofensivo, art. 301 do CTB, porte de droga para consumo)
Não inclui: Audiência de custódia → 5589; Relaxamento do flagrante ilegal → 5588; Imunidades de parlamentares, magistrados e diplomatas quanto à prisão → 5586; Concessão de liberdade provisória e fiança após o flagrante → 5523; Ação controlada (flagrante prorrogado da Lei 12.850/2013) → 5558; Direitos constitucionais do preso → 5587
Âncoras legais: CF, art. 5º, LXI a LXIV; CPP, arts. 301 a 310; Súmula 145/STF
Desempate: Use este nó para as espécies de flagrante e a formalização do auto; o flagrante diferido da ação controlada vai para 5558 e a audiência de custódia vai para 5589.
```

### 5530 · irmão parecido: 5538 Procedimento Sumário

```text
[5530] Processo Penal > Procedimento Ordinário
Escopo: Rito comum ordinário (CPP, arts. 394 a 405): classificação dos procedimentos, oferecimento e recebimento da peça acusatória, resposta à acusação, absolvição sumária, audiência de instrução e julgamento, alegações e sentença. Todas as partes têm subtema próprio.
Inclui: Classificação dos procedimentos comum e especial (CPP, art. 394); Rejeição da denúncia ou queixa (CPP, art. 395); Resposta à acusação (CPP, arts. 396 e 396-A); Absolvição sumária (CPP, art. 397); Audiência una e ordem dos atos (CPP, art. 400); Alegações orais e memoriais (CPP, art. 403)
Não inclui: Procedimento sumário → 5538; Procedimento sumaríssimo dos Juizados → 5539; Rito do Tribunal do Júri e absolvição sumária do júri → 5524; Requisitos da denúncia → 5473; Interrogatório como meio de prova → 5547; Emendatio e mutatio libelli → 5579
Âncoras legais: CPP, arts. 394 a 405; CPP, art. 395; CPP, art. 397; CPP, art. 400
Desempate: Use este nó para o encadeamento dos atos do rito ordinário; se a questão tratar do conteúdo, classificação ou efeitos da sentença, use Sentença Penal (5572).
```

### 5536 · irmão parecido: 5534 Absolvição Sumária

```text
[5536] Processo Penal > Procedimento Ordinário > Alegações Orais
Escopo: Alegações finais no procedimento ordinário: debates orais ao fim da audiência, prazos, ordem de manifestação e conversão em memoriais escritos (CPP, arts. 403 e 404).
Inclui: Debates orais por 20 minutos, prorrogáveis por mais 10, para acusação e defesa; Prazo individual quando houver mais de um acusado; 10 minutos ao assistente do MP, com prorrogação do tempo da defesa; Conversão em memoriais escritos no prazo sucessivo de 5 dias pela complexidade ou número de acusados; Memoriais após a realização de diligência deferida (CPP, art. 404); Ordem de manifestação: acusação antes da defesa; Indispensabilidade das alegações finais defensivas
Não inclui: Debates em plenário do Tribunal do Júri, réplica e tréplica → 5528; Nulidade pela falta de alegações finais da defesa como vício em espécie → 5511; Requerimento de diligências ao fim da instrução (CPP, art. 402) e produção da prova em audiência → 5535; Prazo e prolação da sentença depois dos debates ou memoriais → 5537; Alegações orais no procedimento sumário (CPP, art. 534) → 5538
Âncoras legais: CPP, art. 403; CPP, art. 404
Desempate: Use este nó quando o foco for os debates ou memoriais do art. 403 do CPP; se a questão tratar da instrução ou das diligências do art. 402, use 5535; se tratar da decisão final, use 5537.
```

### 5538 · irmão parecido: 5539 Procedimento Sumaríssimo

```text
[5538] Processo Penal > Procedimento Sumário
Escopo: Procedimento comum sumário do CPP, aplicável aos crimes com pena máxima inferior a 4 anos: hipóteses de cabimento, audiência de instrução e julgamento, número de testemunhas, prazos e aplicação subsidiária das regras do rito ordinário.
Inclui: Cabimento: crime com pena máxima inferior a 4 anos (CPP, art. 394, § 1º, II); Audiência de instrução e julgamento em até 30 dias; Limite de 5 testemunhas por parte; Debates orais e sentença em audiência; Aplicação ao rito sumário de infrações de menor potencial ofensivo remetidas ao juízo comum (art. 538); Diferenças entre os ritos ordinário, sumário e sumaríssimo quanto a prazos e testemunhas
Não inclui: Classificação geral dos procedimentos (comum e especial) → 5532; Resposta à acusação → 5533; Absolvição sumária (CPP, art. 397) → 5534; Rito sumaríssimo dos Juizados Especiais Criminais → 5539
Âncoras legais: CPP, art. 394, § 1º, II; CPP, arts. 531 a 538
Desempate: Use este nó quando a questão tratar das regras próprias do rito sumário (prazo da audiência, número de testemunhas); fases comuns a todos os ritos (recebimento da denúncia, resposta, absolvição sumária) vão para os subtemas do Procedimento Ordinário.
```

### 5524 · irmão parecido: 5538 Procedimento Sumário

```text
[5524] Processo Penal > Procedimento do Tribunal do Júri
Escopo: Procedimento especial do Tribunal do Júri para crimes dolosos contra a vida: princípios constitucionais, rito bifásico, decisões da primeira fase, organização do júri, sessão plenária e sentença (todos com subtema próprio).
Inclui: Competência constitucional do júri para crimes dolosos contra a vida e conexos; Visão geral do procedimento escalonado (judicium accusationis e judicium causae); Questões que abrangem várias fases do júri ao mesmo tempo; Desaforamento; Preparação do processo para julgamento em plenário
Não inclui: Pronúncia, impronúncia, desclassificação e absolvição sumária no júri → 5527; Plenitude de defesa, sigilo das votações e soberania dos veredictos → 5525; Apelação contra decisão do júri (CPP, art. 593, III) → 5562; Conflito entre o júri e o foro por prerrogativa de função → 5484; Tipificação do homicídio e suas qualificadoras → 5150
Âncoras legais: CF, art. 5º, XXXVIII; CPP, arts. 406 a 497
Desempate: Use este nó só quando a questão tratar do júri em geral ou misturar fases; havendo foco numa fase ou instituto específico, use o subtema correspondente.
```

### 5525 · irmão parecido: 5526 Procedimento Bifásico do Tribunal do Júri

```text
[5525] Processo Penal > Procedimento do Tribunal do Júri > Princípios Constitucionais do Júri
Escopo: Princípios constitucionais do júri (CF, art. 5º, XXXVIII): plenitude de defesa, sigilo das votações, soberania dos veredictos e competência mínima para os crimes dolosos contra a vida, com seu alcance e seus limites.
Inclui: Plenitude de defesa x ampla defesa; defesa técnica e autodefesa; Sigilo das votações e interrupção da votação ao se formar a maioria; Soberania dos veredictos e seus limites: apelação por decisão manifestamente contrária à prova e revisão criminal; Competência mínima para crimes dolosos contra a vida tentados ou consumados; Prevalência do foro por prerrogativa previsto na CF sobre o júri (Súmula Vinculante 45); Júri como cláusula pétrea e direito fundamental
Não inclui: Fixação da competência por conexão e continência com crime do júri → 5481; Competência por prerrogativa de função em geral → 5484; Princípios gerais do processo penal (contraditório, devido processo legal) → 5582; Procedimento de votação e redação dos quesitos → 5528; Hipóteses de cabimento da apelação contra decisão do júri → 5562
Âncoras legais: CF, art. 5º, XXXVIII; Súmula Vinculante 45; CPP, art. 74, § 1º
Desempate: Use este nó quando a questão girar em torno do conteúdo ou do alcance de uma das garantias do art. 5º, XXXVIII; se tratar da regra procedimental do CPP que a executa, use o nó do ato (5528 ou 5529).
```

### 5526 · irmão parecido: 5525 Princípios Constitucionais do Júri

```text
[5526] Processo Penal > Procedimento do Tribunal do Júri > Procedimento Bifásico do Tribunal do Júri
Escopo: Estrutura bifásica do júri (judicium accusationis e judicium causae) e atos da primeira fase desde a denúncia até a audiência, além da preparação do processo para o plenário.
Inclui: Distinção entre a fase de formação da culpa e a fase de julgamento em plenário; Recebimento da denúncia, citação e resposta à acusação em 10 dias; Oitiva do MP sobre preliminares e documentos; Audiência de instrução, debates orais e prazo de 90 dias para conclusão; Preparação para o plenário: rol de até 5 testemunhas e requerimento de diligências; Relatório do processo e inclusão em pauta
Não inclui: Pronúncia, impronúncia, absolvição sumária e desclassificação ao fim da primeira fase → 5527; Desaforamento, jurados e sessão plenária → 5528; Resposta à acusação e audiência do procedimento ordinário → 5533; Classificação geral dos procedimentos (comum e especial) → 5532
Âncoras legais: CPP, arts. 406 a 412; CPP, arts. 422 a 424
Desempate: Use este nó quando a questão tratar da estrutura do rito ou de atos que levam à decisão de pronúncia ou ao plenário; se tratar da própria decisão que encerra a primeira fase, use 5527.
```

### 5543 · irmão parecido: 5517 Prisões em Espécie

```text
[5543] Processo Penal > Provas em Espécies
Escopo: Meios de prova e meios de obtenção de prova em espécie no CPP e em leis especiais: perícia, corpo de delito, interrogatório, confissão, testemunhas, reconhecimento, documentos, busca e apreensão, interceptação, colaboração premiada, infiltração etc. (cada um com subtema próprio).
Inclui: Distinção entre meio de prova e meio de obtenção de prova; Questões que comparam diversos meios de prova; Indícios (CPP, art. 239); Rol de provas nominadas do CPP e provas inominadas; Técnicas especiais de investigação da Lei 12.850/2013 em conjunto
Não inclui: Prova ilícita e derivada (frutos da árvore envenenada) → 5594; Ônus da prova e iniciativa probatória do juiz → 5591; Sistemas de valoração da prova (livre convencimento motivado) → 5592; Crimes e disposições gerais da Lei de Interceptação Telefônica → 4700; Tipos penais da Lei de Organizações Criminosas → 4705
Âncoras legais: CPP, arts. 158 a 250; Lei 9.296/1996; Lei 12.850/2013, arts. 3º a 14
Desempate: Use este nó só quando a questão abordar vários meios de prova ou a classificação dos meios de prova; regras de uma prova específica vão para o subtema dela, e regras gerais sobre prova (ônus, licitude, valoração) vão para Teoria Geral das Provas (5590).
```

### 5552 · irmão parecido: 5554 Busca e Apreensão

```text
[5552] Processo Penal > Provas em Espécies > Acareação
Escopo: Acareação como meio de prova no CPP: confronto entre pessoas cujas declarações divergem sobre fatos ou circunstâncias relevantes, com suas hipóteses de cabimento, procedimento e acareação por precatória.
Inclui: Hipóteses de cabimento: entre acusados, entre acusado e testemunha, entre testemunhas, entre acusado ou testemunha e ofendido, entre ofendidos; Requisito de divergência sobre fato ou circunstância relevante; Procedimento: reperguntas para explicação dos pontos divergentes e redução a termo; Acareação de testemunha ausente por carta precatória; Direito ao silêncio do acusado na acareação; Possibilidade de acareação no inquérito policial
Não inclui: Inquirição de testemunhas, contradita e compromisso → 5550; Reconhecimento pessoal ou de coisas pela vítima ou testemunha → 5551; Procedimento do interrogatório do acusado → 5547; Diligências da autoridade policial no inquérito em geral → 5500
Âncoras legais: CPP, arts. 229 e 230; CPP, art. 6º, VI
Desempate: Escolha este nó quando a questão tratar do confronto entre declarantes com versões divergentes; se tratar só do depoimento de uma pessoa, use o nó do respectivo meio de prova.
```

### 5554 · irmão parecido: 5552 Acareação

```text
[5554] Processo Penal > Provas em Espécies > Busca e Apreensão
Escopo: Busca e apreensão no processo penal: espécies (domiciliar e pessoal), hipóteses, requisitos do mandado, horário e formalidades de execução, inviolabilidade do domicílio e situações de busca sem mandado.
Inclui: Busca domiciliar e busca pessoal: hipóteses do art. 240 do CPP; Requisitos do mandado e vedação a mandado genérico; Inviolabilidade do domicílio: dia, noite, consentimento e flagrante delito; Busca pessoal sem mandado e fundada suspeita; Busca em escritório de advocacia e garantias do advogado; Busca em mulher feita por outra mulher; Formalidades da execução e auto circunstanciado
Não inclui: Restituição das coisas apreendidas → 5495; Sequestro, arresto e hipoteca legal de bens → 5496; Crime de violação de domicílio do Código Penal → 5133; Ilicitude da prova obtida em busca ilegal e teoria dos frutos da árvore envenenada → 5594; Cumprimento de mandado com abuso como crime de abuso de autoridade → 4684; Rastreamento e preservação do vestígio apreendido → 5544
Âncoras legais: CPP, arts. 240 a 250; CF, art. 5º, XI; Lei 8.906/1994, art. 7º, II e § 6º
Desempate: Escolha este nó quando o foco for a validade e a execução da diligência de busca; se o foco for a consequência da ilicitude para a prova, use 5594.
```

### 5544 · irmão parecido: 5558 Ação Controlada

```text
[5544] Processo Penal > Provas em Espécies > Cadeia de Custódia
Escopo: Cadeia de custódia da prova: conjunto de procedimentos para manter e documentar a história cronológica do vestígio, desde o reconhecimento até o descarte, conforme os arts. 158-A a 158-F do CPP.
Inclui: Conceito de cadeia de custódia e de vestígio; Etapas: reconhecimento, isolamento, fixação, coleta, acondicionamento, transporte, recebimento, processamento, armazenamento e descarte; Responsabilidade pela preservação do local do crime; Central de custódia e lacres; Consequências da quebra da cadeia de custódia (nulidade ou valoração da prova); Quebra da cadeia de custódia em prova digital
Não inclui: Obrigatoriedade do exame de corpo de delito nas infrações que deixam vestígios → 5545; Perito oficial, quesitos e laudo → 5546; Prova ilícita e teoria da contaminação → 5594; Execução da busca e apreensão → 5554
Âncoras legais: CPP, arts. 158-A a 158-F
Desempate: Escolha este nó quando a questão tratar do rastreamento, da preservação ou da manipulação do vestígio; se tratar da realização do exame ou do laudo, use 5545 ou 5546.
```

### 5556 · irmão parecido: 5559 Infiltração de Agentes

```text
[5556] Processo Penal > Provas em Espécies > Captação Ambiental
Escopo: Captação ambiental de sinais eletromagnéticos, ópticos ou acústicos como meio de obtenção de prova: requisitos, autorização judicial, prazo, gravação feita por um dos interlocutores e crime correlato.
Inclui: Requisitos da captação ambiental: autorização judicial, requerimento do MP ou da autoridade policial, crimes com pena máxima superior a 4 anos; Prazo de 15 dias renovável; Gravação ambiental feita por um dos interlocutores sem conhecimento do outro e sua utilização pela defesa; Captação ambiental na Lei 12.850/2013; Diferença entre captação ambiental, interceptação e escuta; Crime de captação ambiental sem autorização judicial (art. 10-A da Lei 9.296/1996)
Não inclui: Interceptação de comunicações telefônicas e quebra de sigilo de dados telefônicos → 5555; Infiltração de agentes → 5559; Teoria da prova ilícita em geral → 5594; Crime de organização criminosa → 4705
Âncoras legais: Lei 9.296/1996, arts. 8º-A e 10-A; Lei 12.850/2013, art. 3º, II
Desempate: Escolha este nó quando a questão tratar da captação de conversas ou imagens no ambiente; se for comunicação telefônica ou telemática em curso, use 5555.
```

### 5549 · irmão parecido: 5557 Colaboração Premiada

```text
[5549] Processo Penal > Provas em Espécies > Declaração do Ofendido
Escopo: Declarações do ofendido como meio de prova: oitiva da vítima, ausência de compromisso, condução coercitiva, direitos de comunicação e de atendimento e valor probatório da palavra da vítima.
Inclui: Ofendido não presta compromisso nem é computado no número de testemunhas; Condução coercitiva do ofendido que não comparece; Comunicação ao ofendido sobre ingresso e saída do acusado da prisão, audiências e sentença; Espaço separado e preservação da intimidade do ofendido; Relevância da palavra da vítima em crimes sexuais e de violência doméstica; Ofendido não responde por falso testemunho
Não inclui: Prova testemunhal: compromisso, contradita e número de testemunhas → 5550; Reconhecimento do acusado pela vítima → 5551; Depoimento especial de criança ou adolescente vítima → 4709; Medidas protetivas e procedimento da Lei Maria da Penha → 4704; Acareação entre ofendido e acusado → 5552
Âncoras legais: CPP, art. 201
Desempate: Escolha este nó quando a pessoa ouvida for a vítima do crime; se for terceiro que presenciou os fatos, use 5550.
```

### 5553 · irmão parecido: 5550 Prova Testemunhal

```text
[5553] Processo Penal > Provas em Espécies > Prova Documental
Escopo: Prova documental: conceito de documento, produção e juntada em qualquer fase, documentos públicos e particulares, cópias e traduções, autenticidade, valor probatório e documentos eletrônicos, conforme os arts. 231 a 238 do CPP.
Inclui: Conceito amplo de documento e suportes eletrônicos; Juntada de documentos em qualquer fase do processo e restrição no plenário do júri; Documentos em língua estrangeira e tradução; Cópia autenticada e original; Vedação a cartas particulares obtidas por meios criminosos; Exame de autenticidade e reconhecimento de letra; Restituição de documentos originais; Contraditório sobre o documento juntado
Não inclui: Incidente de falsidade documental → 5497; Requisitos e contraditório da prova emprestada → 5593; Crimes de falsidade documental do Código Penal → 5118; Exame grafotécnico e perícias em geral → 5546; Cadeia de custódia de prova digital → 5544
Âncoras legais: CPP, arts. 231 a 238; CPP, art. 479
Desempate: Escolha este nó quando a questão tratar da produção, juntada ou valor do documento; se tratar da arguição de falsidade, use 5497, e da teoria da prova emprestada, use 5593.
```

### 5550 · irmão parecido: 5553 Prova Documental

```text
[5550] Processo Penal > Provas em Espécies > Prova Testemunhal
Escopo: Prova testemunhal: capacidade para depor, dever de depor, compromisso, recusa e proibição de depor, contradita, número de testemunhas, forma de inquirição (exame direto e cruzado) e valor do depoimento, nos arts. 202 a 225 do CPP.
Inclui: Toda pessoa pode ser testemunha; testemunhas informantes sem compromisso; Recusa de parentes do acusado e proibição por sigilo profissional; Contradita e arguição de defeito; Número máximo de testemunhas por procedimento; Sistema de inquirição direta (cross-examination) e perguntas complementares do juiz; Testemunha por precatória, videoconferência e prerrogativas de autoridades; Depoimento policial e testemunho indireto (por ouvir dizer); Retirada do réu da sala quando causar temor à testemunha
Não inclui: Declarações da vítima → 5549; Acareação entre testemunhas → 5552; Reconhecimento de pessoas → 5551; Crime de falso testemunho → 5081; Depoimento especial de criança ou adolescente → 4709; Testemunhas no plenário do júri → 5528
Âncoras legais: CPP, arts. 202 a 225; CPP, art. 155
Desempate: Escolha este nó quando a pessoa ouvida for terceiro estranho à relação crime-vítima; se for o ofendido, use 5549, e se for o acusado, use 5547.
```

### 5560 · irmão parecido: 5517 Prisões em Espécie

```text
[5560] Processo Penal > Recursos em Espécies
Escopo: Recursos típicos do processo penal: apelação, RESE, embargos infringentes e de nulidade, embargos de declaração, carta testemunhável, correição parcial, agravo em execução, recursos especial e extraordinário, protesto por novo júri e recursos nos Juizados (todos com subtema próprio).
Inclui: Cabimento comparado entre apelação e RESE; Prazos de interposição e de razões de cada recurso; Fungibilidade aplicada a recurso específico; Processamento e julgamento dos recursos nos tribunais; Questões que abrangem vários recursos em espécie
Não inclui: Pressupostos de admissibilidade recursal em geral → 5514; Efeitos devolutivo, suspensivo, extensivo e regressivo em geral → 5515; Princípios recursais (reformatio in pejus, voluntariedade, taxatividade) → 5513; Habeas corpus → 5477; Revisão criminal → 5478; Mandado de segurança em matéria criminal → 5479
Âncoras legais: CPP, arts. 574 a 667; Lei 7.210/1984, art. 197; Lei 9.099/1995, arts. 82 e 83; CF, art. 102, III; CF, art. 105, III
Desempate: Use este nó quando a questão comparar recursos ou tratar de vários deles; se a questão versar sobre um único recurso, use o subtema dele; regras aplicáveis a todos os recursos vão para Parte Geral dos Recursos (5512).
```

### 5562 · irmão parecido: 5565 Embargos de Declaração

```text
[5562] Processo Penal > Recursos em Espécies > Apelação
Escopo: Apelação criminal: recurso contra sentenças definitivas ou com força de definitivas do juiz singular e contra decisões do Júri nas hipóteses legais (CPP, arts. 593 a 603). Cobre cabimento, prazos, legitimidade, razões, efeitos e julgamento.
Inclui: Hipóteses de cabimento do art. 593 do CPP, incluindo as alíneas do inciso III contra decisões do Júri; Prazo de 5 dias para interpor e de 8 dias para as razões; razões apresentadas no tribunal; Apelação supletiva do assistente e do ofendido (art. 598 do CPP); Efeito devolutivo limitado aos fundamentos no Júri (Súmula 713 do STF); Decisão dos jurados manifestamente contrária à prova dos autos e novo julgamento uma única vez; Efeitos suspensivo e devolutivo da apelação contra sentença absolutória ou condenatória; Subsidiariedade: cabe apelação quando não houver previsão de RESE
Não inclui: Decisões interlocutórias listadas no art. 581 do CPP, como rejeição da denúncia e pronúncia → 5561; Apelação no JECrim (prazo de 10 dias, turma recursal) → 5569; Princípios recursais gerais, como reformatio in pejus e voluntariedade → 5512; Pressupostos gerais de admissibilidade comuns a todos os recursos → 5514; Efeitos dos recursos em geral (devolutivo, suspensivo, extensivo, regressivo) → 5515
Âncoras legais: CPP, arts. 593 a 603; Súmula 713 do STF
Desempate: Escolha Apelação quando a decisão impugnada for sentença definitiva ou decisão do Júri prevista no art. 593; se a decisão estiver no rol do art. 581, use RESE (5561).
```

### 5568 · irmão parecido: 5571 Recurso Especial

```text
[5568] Processo Penal > Recursos em Espécies > Correição Parcial
Escopo: Correição parcial: meio impugnativo contra decisões ou despachos do juiz que importem erro ou abuso e causem inversão tumultuária do processo, quando não houver recurso específico.
Inclui: Natureza jurídica controvertida (recurso ou medida administrativo-disciplinar); Cabimento residual contra error in procedendo que tumultua o processo; Previsão em lei de organização judiciária e em regimentos internos; Previsão na Justiça Federal (Lei 5.010/1966); Processamento pelo rito do agravo ou do RESE, conforme a doutrina; Legitimidade do MP e da defesa
Não inclui: Decisões interlocutórias previstas no art. 581 do CPP → 5561; Denegação ou obstáculo ao seguimento de RESE → 5567; Mandado de segurança em matéria criminal → 5479
Âncoras legais: Lei 5.010/1966, art. 6º, I
Desempate: Use este nó quando a impugnação mirar o tumulto processual causado por erro ou abuso do juiz, sem recurso típico previsto.
```

### 5565 · irmão parecido: 5566 Agravo em Execução

```text
[5565] Processo Penal > Recursos em Espécies > Embargos de Declaração
Escopo: Embargos de declaração: recurso para sanar ambiguidade, obscuridade, contradição ou omissão de sentença, acórdão ou decisão (CPP, arts. 382 e 619-620), com efeito integrativo, interruptivo e eventualmente modificativo.
Inclui: Hipóteses de cabimento: ambiguidade, obscuridade, contradição e omissão; Prazo de 2 dias no CPP ('embarguinhos' contra sentença, art. 382); Embargos no JECrim com prazo de 5 dias (Lei 9.099/1995, art. 83); Efeitos infringentes ou modificativos excepcionais e necessidade de contraditório; Embargos para fins de prequestionamento; Interrupção do prazo para outros recursos; Correção de erro material
Não inclui: Embargos infringentes e de nulidade contra acórdão não unânime → 5564; Prequestionamento como requisito do REsp (Súmula 211 do STJ) → 5571; Prequestionamento como requisito do RE (Súmulas 282 e 356 do STF) → 5570; Regras gerais dos recursos no JECrim → 5569
Âncoras legais: CPP, art. 382; CPP, arts. 619 e 620; Lei 9.099/1995, art. 83
Desempate: Escolha este nó quando o núcleo for o vício de clareza ou completude da decisão; questões sobre embargos no JECrim também vêm aqui se o foco for a disciplina dos embargos.
```

### 5571 · irmão parecido: 5569 Recursos no Âmbito dos Juizados Especiais

```text
[5571] Processo Penal > Recursos em Espécies > Recurso Especial
Escopo: Recurso especial em matéria criminal: recurso ao STJ contra acórdão de tribunal que contrariar ou negar vigência a lei federal ou der a ela interpretação divergente (CF, art. 105, III), com requisitos de admissibilidade e efeitos próprios.
Inclui: Hipóteses do art. 105, III, alíneas a, b e c, da CF; Vedação ao reexame de provas (Súmula 7 do STJ); Prequestionamento (Súmula 211 do STJ); Não cabimento contra decisão de turma recursal (Súmula 203 do STJ); Divergência jurisprudencial e cotejo analítico; Agravo contra a inadmissão do REsp na origem; Ausência de efeito suspensivo e execução provisória da pena
Não inclui: Violação direta da Constituição e repercussão geral → 5570; Recursos contra acórdão de turma recursal do JECrim → 5569; Habeas corpus substitutivo de recurso especial → 5477; Embargos de declaração opostos para prequestionar → 5565
Âncoras legais: CF, art. 105, III; Súmula 7 do STJ; Súmula 211 do STJ; Súmula 203 do STJ
Desempate: Escolha REsp quando a questão envolver lei federal e o STJ; se envolver matéria constitucional e o STF, use 5570.
```

### 5570 · irmão parecido: 5571 Recurso Especial

```text
[5570] Processo Penal > Recursos em Espécies > Recurso Extraordinário
Escopo: Recurso extraordinário em matéria criminal: recurso ao STF contra decisão de única ou última instância que contrariar a Constituição ou nas demais hipóteses do art. 102, III, da CF, com repercussão geral e prequestionamento.
Inclui: Hipóteses do art. 102, III, da CF; Repercussão geral (CF, art. 102, § 3º); Exigência de ofensa direta à Constituição, não reflexa; Vedação ao reexame de provas (Súmula 279 do STF); Prequestionamento (Súmulas 282 e 356 do STF); Cabimento contra acórdão de turma recursal (Súmula 640 do STF); Interposição simultânea com o REsp
Não inclui: Violação de lei federal e divergência jurisprudencial → 5571; Recursos ordinários próprios do JECrim (apelação para turma recursal) → 5569; Habeas corpus no STF → 5477
Âncoras legais: CF, art. 102, III; CF, art. 102, § 3º; Súmula 279 do STF; Súmula 282 do STF; Súmula 356 do STF; Súmula 640 do STF
Desempate: Escolha RE quando a matéria for constitucional e o órgão for o STF; questões sobre o RE contra turma recursal também vêm aqui.
```

### 5561 · irmão parecido: 5569 Recursos no Âmbito dos Juizados Especiais

```text
[5561] Processo Penal > Recursos em Espécies > Recurso em sentido estrito (RESE)
Escopo: Recurso em sentido estrito: recurso de fundamentação vinculada contra as decisões taxativamente previstas no art. 581 do CPP e em leis especiais, com prazo, processamento e juízo de retratação próprios (CPP, arts. 581 a 592).
Inclui: Rol taxativo do art. 581 do CPP: rejeição da denúncia, incompetência, pronúncia, liberdade provisória, extinção da punibilidade; Prazo de 5 dias e prazo de 20 dias na hipótese de lista de jurados; Juízo de retratação (efeito regressivo, art. 589); Hipóteses de subida nos próprios autos ou por instrumento; Efeito suspensivo restrito às hipóteses legais; RESE contra a denegação da apelação; RESE contra o não recebimento da denúncia e a Súmula 707 do STF
Não inclui: Recurso contra impronúncia e absolvição sumária no Júri (apelação) → 5562; Decisões do juízo da execução (progressão, unificação, livramento) → 5566; Denegação do próprio RESE → 5567; Natureza e requisitos da pronúncia, sem foco no recurso → 5527; Rejeição da denúncia no JECrim (apelação do art. 82 da Lei 9.099/1995) → 5569
Âncoras legais: CPP, arts. 581 a 592; Súmula 707 do STF
Desempate: Escolha RESE quando a decisão impugnada estiver no rol do art. 581 do CPP; se for sentença definitiva ou não houver previsão, use Apelação (5562).
```

### 5569 · irmão parecido: 5571 Recurso Especial

```text
[5569] Processo Penal > Recursos em Espécies > Recursos no Âmbito dos Juizados Especiais
Escopo: Recursos no Juizado Especial Criminal: apelação para a turma recursal, embargos de declaração e cabimento de RE/REsp contra decisões das turmas recursais (Lei 9.099/1995, arts. 82 e 83).
Inclui: Apelação contra rejeição da denúncia ou da queixa e contra sentença, com prazo de 10 dias e razões junto; Apelação contra a sentença homologatória de transação penal; Julgamento pela turma recursal de juízes de primeiro grau; Embargos de declaração no JECrim; Cabimento de RE e não cabimento de REsp contra a turma recursal (Súmulas 640 do STF e 203 do STJ); Competência para habeas corpus e mandado de segurança contra ato da turma recursal
Não inclui: Requisitos e efeitos da transação penal → 5541; Suspensão condicional do processo → 5542; Competência e infrações de menor potencial ofensivo → 5540; Apelação no procedimento comum do CPP → 5562; Aspectos gerais da Lei 9.099/1995 sem foco recursal → 4701
Âncoras legais: Lei 9.099/1995, arts. 82 e 83; Súmula 640 do STF; Súmula 203 do STJ
Desempate: Use este nó quando o recurso impugnar decisão do JECrim ou da turma recursal; se o foco for o instituto despenalizador em si, use 5540, 5541, 5542 ou 4701.
```

### 5580 · irmão parecido: 5505 Lei Processual no Tempo e no Espaço

```text
[5580] Processo Penal > Sistemas e Princípios Processuais Penais
Escopo: Sistemas processuais penais (inquisitivo, acusatório e misto) e princípios gerais do processo penal (devido processo legal, contraditório, ampla defesa, presunção de inocência, juiz natural etc.), com subtemas próprios.
Inclui: Questões que relacionam o sistema acusatório aos princípios processuais; Estrutura acusatória do processo penal (CPP, art. 3º-A); Presunção de inocência e vedação de autoincriminação como princípios gerais; Juiz natural, publicidade e duração razoável do processo; Visão de conjunto dos fundamentos constitucionais do processo penal
Não inclui: Princípios da ação penal (obrigatoriedade, indisponibilidade, oportunidade) → 5469; Princípios recursais → 5513; Princípios relativos à prova penal → 5595; Princípios constitucionais do júri → 5525; Princípios do Direito Penal material (legalidade, insignificância) → 5172; Juiz das garantias → 5503
Âncoras legais: CPP, art. 3º-A; CF, art. 5º, LIII; CF, art. 5º, LIV; CF, art. 5º, LV; CF, art. 5º, LVII; CF, art. 5º, LXXVIII
Desempate: Use este nó só quando a questão misturar sistemas processuais e princípios gerais; princípios de um instituto específico (ação, prova, recursos, júri) vão para o nó desse instituto.
```

### 5583 · irmão parecido: 5487 Comunicação dos Atos Processuais

```text
[5583] Processo Penal > Sujeitos do Processo
Escopo: Sujeitos da relação processual penal: juiz, Ministério Público, acusado e defensor, assistente de acusação, auxiliares da justiça, peritos e intérpretes, com seus poderes, deveres, prerrogativas e impedimentos.
Inclui: Poderes e deveres do juiz no processo penal; Atuação do Ministério Público como parte e fiscal da lei; Acusado: identificação, presença e direito ao defensor; Defensor constituído, dativo e público; defesa técnica obrigatória; Assistente de acusação: quem pode ser, admissão e poderes; Peritos e intérpretes como auxiliares do juízo
Não inclui: Arguição de suspeição e impedimento por exceção → 5492; Querelante e legitimidade na ação penal privada → 5472; Interrogatório do acusado → 5547; Legitimidade do assistente para recorrer → 5514; Produção da prova pericial → 5546
Âncoras legais: CPP, arts. 251 a 281
```

### 5584 · irmão parecido: 5590 Teoria Geral das Provas

```text
[5584] Processo Penal > Teoria Geral das Prisões
Escopo: Teoria geral da prisão processual: conceito e espécies de prisão, direitos e garantias do preso, imunidades e prisões especiais, relaxamento da prisão ilegal e audiência de custódia (com subtemas próprios), sem tratar das prisões em espécie.
Inclui: Distinção entre prisão-pena e prisão processual (cautelar); Requisitos constitucionais da prisão: ordem escrita e fundamentada ou flagrante; Uso de algemas e emprego de força; Comunicação da prisão ao juiz e à família e direito ao silêncio; Regras gerais das cautelares pessoais (CPP, art. 282); Prisão especial e imunidades prisionais
Não inclui: Prisão em flagrante: espécies e auto → 5518; Prisão preventiva: requisitos e fundamentos → 5519; Prisão temporária (Lei 7.960/1989) → 5520; Liberdade provisória e fiança → 5523; Medidas cautelares diversas da prisão (CPP, art. 319) → 5522; Prisão domiciliar substitutiva da preventiva → 5521
Âncoras legais: CF, art. 5º, LXI a LXVI; CPP, arts. 282 a 300; CPP, art. 310
Desempate: Use este nó (ou seus subtemas) para regras comuns a toda prisão processual; se a questão tratar dos requisitos ou do regime de uma prisão específica, use o subtema de Prisões em Espécie (5517).
```

### 5587 · irmão parecido: 5585 Conceitos e Espécies de Prisão

```text
[5587] Processo Penal > Teoria Geral das Prisões > Direitos e Garantias sobre a Prisão
Escopo: Garantias constitucionais e legais que regem o ato da prisão e a situação do preso: ordem escrita e fundamentada, comunicação, informação de direitos, uso de força e algemas, cumprimento do mandado e respeito ao domicílio.
Inclui: Exigência de flagrante ou ordem escrita e fundamentada da autoridade judiciária; Comunicação imediata da prisão ao juiz, à família ou pessoa indicada, e remessa à Defensoria quando não houver advogado; Direito ao silêncio, à assistência de advogado e à identificação dos responsáveis pela prisão; Uso de algemas (Súmula Vinculante 11) e emprego moderado da força; Cumprimento do mandado: a qualquer dia e hora, inviolabilidade do domicílio e prisão fora da jurisdição (precatória e BNMP); Separação entre presos provisórios e condenados; integridade física e moral do preso; Nota de culpa
Não inclui: Apresentação do preso ao juiz em 24 horas → 5589; Relaxamento da prisão ilegal → 5588; Prisão especial e imunidades à prisão de certas autoridades → 5586; Direitos do preso na execução da pena (LEP) → 4703; Algemas no plenário do júri e sessão de julgamento → 5528
Âncoras legais: CF, art. 5º, LXI a LXIV; CF, art. 5º, XLIX; CPP, art. 283, § 2º; CPP, arts. 284 e 292; CPP, art. 289-A; CPP, art. 306; CPP, art. 300; Súmula Vinculante 11
Desempate: Escolha este nó quando a questão tratar das garantias do preso no momento e na forma da prisão. Se tratar de direitos durante a execução da pena, use 4703; se tratar da audiência de apresentação ao juiz, use 5589.
```

### 5588 · irmão parecido: 5587 Direitos e Garantias sobre a Prisão

```text
[5588] Processo Penal > Teoria Geral das Prisões > Relaxamento da Prisão
Escopo: Relaxamento da prisão ilegal: conceito, cabimento contra qualquer prisão ilegal (vícios formais, excesso de prazo, ausência de situação de flagrante), autoridade competente e distinção em relação à liberdade provisória e à revogação.
Inclui: Dever do juiz de relaxar imediatamente a prisão ilegal; Relaxamento do flagrante ilegal na análise do art. 310, I; Ilegalidade por flagrante forjado ou provocado, por ausência de estado de flagrância ou por vício no auto; Excesso de prazo da prisão cautelar como causa de relaxamento; Relaxamento sem vinculação a cautelares e possibilidade de nova decretação da prisão; Diferença entre relaxamento (prisão ilegal), liberdade provisória (prisão legal, mas desnecessária) e revogação (fim dos motivos)
Não inclui: Liberdade provisória com ou sem fiança → 5523; Revogação e reexame periódico da preventiva (art. 316) → 5519; Habeas corpus como ação para fazer cessar o constrangimento ilegal → 5477; Realização e prazo da audiência de custódia → 5589; Espécies de flagrante (próprio, impróprio, presumido, preparado, esperado) → 5518
Âncoras legais: CF, art. 5º, LXV; CPP, art. 310, I
Desempate: Escolha este nó quando a questão tratar da medida contra a prisão ilegal. Se a prisão for legal e a questão discutir sua necessidade, use 5523 (liberdade provisória) ou 5519 (revogação da preventiva); se tratar do instrumento habeas corpus, use 5477.
```

### 5590 · irmão parecido: 5584 Teoria Geral das Prisões

```text
[5590] Processo Penal > Teoria Geral das Provas
Escopo: Teoria geral da prova penal: conceito, objeto, finalidade, sujeitos e ônus da prova, princípios probatórios, sistemas de avaliação, prova emprestada e prova ilegal/ilícita (com subtemas próprios), sem tratar dos meios de prova em espécie.
Inclui: Conceito, objeto e finalidade da prova; Ônus da prova e iniciativa probatória do juiz (CPP, art. 156); Livre convencimento motivado e vedação de condenação só com elementos do inquérito (art. 155); Provas ilícitas, derivadas e suas exceções (art. 157); Prova emprestada: requisitos e contraditório; Princípios da comunhão da prova e da liberdade probatória
Não inclui: Regras de um meio de prova específico (testemunha, perícia, confissão) → 5543; Interceptação telefônica e seus requisitos → 5555; Cadeia de custódia (CPP, arts. 158-A a 158-F) → 5544; Princípios gerais do processo penal (contraditório, presunção de inocência) → 5582; Nulidade do processo decorrente de vício na prova → 5510
Âncoras legais: CPP, arts. 155 a 157; CF, art. 5º, LVI
Desempate: Use este nó (ou seus subtemas) quando a questão tratar de regra aplicável a toda prova; se tratar de como se produz ou se valora um meio de prova determinado, use Provas em Espécies (5543) e seu subtema.
```

### 5593 · irmão parecido: 5594 Prova Ilegal e Prova Ilícita

```text
[5593] Processo Penal > Teoria Geral das Provas > Prova Emprestada
Escopo: Prova emprestada: conceito, natureza, requisitos de validade (contraditório, licitude na origem, participação da parte contra quem se usa) e uso de prova produzida em um processo em outro, inclusive em processo administrativo disciplinar.
Inclui: Conceito e natureza jurídica da prova emprestada (ingressa como prova documental); Requisitos: produção lícita na origem e contraditório em relação à parte contra quem é usada; Exigência ou não de identidade de partes segundo a jurisprudência do STF e do STJ; Uso de interceptação telefônica de processo criminal em processo administrativo disciplinar (Súmula 591 do STJ); Compartilhamento de provas entre esferas penal, civil e administrativa; Prova emprestada obtida ilicitamente na origem
Não inclui: Requisitos e procedimento da interceptação telefônica e encontro fortuito de provas → 5555; Teoria dos frutos da árvore envenenada e exclusão de prova ilícita em geral → 5594; Produção e incidente de falsidade de documentos → 5553; Interceptação telefônica como lei (Lei 9.296/1996) em si → 4700
Âncoras legais: CPC, art. 372; Súmula 591 do STJ
Desempate: Use este nó quando o centro da questão for o transporte de prova de um processo para outro; se a discussão for apenas a licitude da obtenção original, use 5594.
```

### 5594 · irmão parecido: 5593 Prova Emprestada

```text
[5594] Processo Penal > Teoria Geral das Provas > Prova Ilegal e Prova Ilícita
Escopo: Provas vedadas: distinção entre prova ilícita (violação de norma material/constitucional) e ilegítima (violação de norma processual), inadmissibilidade, prova ilícita por derivação e suas exceções, desentranhamento e prova ilícita pro reo.
Inclui: Distinção doutrinária entre prova ilícita, ilegítima e ilegal; Inadmissibilidade e desentranhamento das provas ilícitas (art. 157, caput e § 3º); Prova ilícita por derivação: teoria dos frutos da árvore envenenada; Exceções: fonte independente, descoberta inevitável, nexo causal atenuado; Admissibilidade da prova ilícita pro reo (proporcionalidade); Licitude de gravação clandestina feita por um dos interlocutores; Consequência da violação de domicílio, de acesso a celular sem autorização e de outros direitos na validade da prova; Juiz que conheceu a prova inadmissível (art. 157, § 5º) e a decisão do STF
Não inclui: Requisitos legais da interceptação telefônica e quebra de sigilo telefônico → 5555; Requisitos da busca e apreensão e do mandado → 5554; Quebra da cadeia de custódia e seus efeitos → 5544; Uso de prova produzida em outro processo → 5593; Nulidade de atos processuais em geral → 5510
Âncoras legais: CF, art. 5º, LVI; CPP, art. 157
Desempate: Use este nó quando a questão tratar da admissibilidade e dos efeitos da ilicitude da prova (exclusão, derivação, exceções); se tratar dos requisitos de um meio de prova específico, use o nó desse meio de prova.
```

## Prioridade 4

### 4368 · amostral

```text
[4368] Criminologia > Criminologia no Estado Democrático de Direito
Escopo: Papel da Criminologia num Estado Democrático de Direito, abrangendo a prevenção do delito (4369) e os modelos de reação ao crime (4370). Use o nó geral para a função garantista e democrática da Criminologia e do controle social sem enfoque num desses subtemas.
Inclui: Compromisso da Criminologia com os direitos fundamentais e a dignidade humana; Limites democráticos ao controle social e à reação estatal ao crime; Visão geral conjunta de prevenção e resposta ao delito; Relação entre Criminologia, Estado de Direito e legitimidade da intervenção penal
Não inclui: Prevenção primária, secundária e terciária → 4369; Modelos dissuasório, ressocializador e restaurador (integrador) de reação ao crime → 4370; Movimentos de política criminal (Lei e Ordem, abolicionismo, minimalismo) → 4375; Teorias que justificam a pena (absolutas, relativas, mistas) → 4384; Transação penal e composição civil na Lei 9.099/1995 → 4701
Âncoras legais: CF, art. 1º, III; Antonio García-Pablos de Molina
Desempate: Use o nó geral somente quando a questão tratar da Criminologia no Estado Democrático sem pedir uma espécie de prevenção (4369) nem um modelo de reação ao delito (4370).
```

### 4370 · amostral

```text
[4370] Criminologia > Criminologia no Estado Democrático de Direito > Modelos de Reação ao Delito
Escopo: Modelos de resposta do Estado e da sociedade ao crime já cometido, conforme a Criminologia: modelo clássico ou dissuasório, modelo ressocializador e modelo integrador (consensual ou restaurativo), com suas finalidades, protagonistas e críticas.
Inclui: Modelo dissuasório (clássico/retributivo): castigo e intimidação, com o infrator como único protagonista; Modelo ressocializador: intervenção positiva sobre o infrator para reinseri-lo; Modelo integrador ou restaurativo: reparação do dano, conciliação e participação da vítima e da comunidade; Justiça restaurativa (mediação vítima-ofensor, círculos restaurativos) e justiça consensual; Comparação entre os modelos e protagonismo de infrator, vítima e comunidade em cada um; Lei 9.099/1995 como exemplo de modelo consensual de reação ao delito
Não inclui: Prevenção primária, secundária e terciária e prevenção situacional do crime → 4369; Teorias absolutas, relativas e mistas da pena (retribuição, prevenção geral e especial) → 4384; Abolicionismo, minimalismo e Movimento Lei e Ordem como correntes de política criminal → 4375; Requisitos e procedimento da transação penal → 5541; Regras da Lei 9.099/1995 sobre o Juizado Especial Criminal → 4701; Vitimização primária, secundária e terciária → 4390
Âncoras legais: Lei 9.099/1995, art. 74; Lei 9.099/1995, art. 76; Resolução CNJ 225/2016; García-Pablos de Molina e Luiz Flávio Gomes
Desempate: Escolha este nó quando a questão tratar da resposta ao crime já praticado (castigar, ressocializar ou reparar e conciliar); se tratar de evitar que o crime ocorra ou se repita por meio de programas preventivos, use 4369.
```

### 4369 · amostral

```text
[4369] Criminologia > Criminologia no Estado Democrático de Direito > Sistemas de Prevenção
Escopo: Sistemas e modelos de prevenção do delito estudados pela Criminologia: prevenção primária, secundária e terciária, prevenção situacional e comunitária, com seus destinatários, instrumentos e prazos de eficácia.
Inclui: Prevenção primária: atua nas raízes do crime com educação, moradia, emprego e políticas sociais de médio e longo prazo; Prevenção secundária: atua onde e quando o crime se manifesta, com policiamento, controle de meios de comunicação e urbanismo; Prevenção terciária: dirigida ao condenado ou recluso para evitar a reincidência; Prevenção situacional e Crime Prevention Through Environmental Design (CPTED): redução de oportunidades; Prevenção comunitária e participação social na segurança pública; Destinatários e críticas de cada nível de prevenção
Não inclui: Modelos dissuasório, ressocializador e restaurativo de reação ao crime → 4370; Prevenção geral e especial como finalidades da pena → 4384; Teoria das janelas quebradas, Escola de Chicago e outras teorias explicativas do crime → 4388; Regras de execução penal e assistência ao preso previstas na LEP → 4703; Criminalização secundária pelas agências de controle → 4378
Âncoras legais: García-Pablos de Molina e Luiz Flávio Gomes
Desempate: Escolha este nó quando a questão classificar medidas para evitar o crime ou a reincidência (prevenção primária, secundária, terciária ou situacional); se discutir a prevenção como finalidade da pena, use 4384.
```

### 4373 · amostral

```text
[4373] Criminologia > Etapas Evolutivas e Escolas Criminológicas > Escolas Criminológicas
Escopo: Escolas criminológicas e penais da fase científica (Clássica, Positiva, Terza Scuola, Escola Moderna Alemã e afins): seus representantes, postulados sobre crime, criminoso, livre-arbítrio, determinismo, métodos e finalidade da pena.
Inclui: Escola Clássica: Beccaria, Carrara, livre-arbítrio, crime como ente jurídico, método dedutivo-abstrato; Escola Positiva: Lombroso, Ferri e Garofalo; determinismo, método empírico-indutivo, periculosidade; Fases antropológica (Lombroso), sociológica (Ferri) e jurídica (Garofalo) do positivismo; Terza Scuola italiana (Carnevale, Alimena) e Escola Moderna Alemã ou de Política Criminal (von Liszt); Escola Correcionalista (Röder, Dorado Montero) e Escola Técnico-Jurídica (Rocco); Comparação entre os postulados das escolas clássica e positiva
Não inclui: Pensamento pré-científico sobre o crime na Antiguidade, Idade Média e Idade Moderna (fisionomia, frenologia, demonologia) → 4372; Tipologias de criminosos de Lombroso e Ferri (nato, louco, ocasional, passional, habitual) cobradas como classificação → 4367; Teorias sociológicas em espécie: Escola de Chicago, anomia, associação diferencial, labelling approach, criminologia crítica → 4388; Teorias absolutas, relativas e mistas da pena → 4384; Movimentos de política criminal: Lei e Ordem, abolicionismo, minimalismo, nova defesa social → 4375; Conceito, objeto e caráter científico da Criminologia → 4381
Âncoras legais: Cesare Beccaria, Dos Delitos e das Penas (1764); Cesare Lombroso, O Homem Delinquente (1876); Enrico Ferri, Sociologia Criminal; Raffaele Garofalo, Criminologia; Franz von Liszt
Desempate: Escolha este nó quando a questão tratar de uma escola sistematizada (da Clássica em diante) e seus postulados; se tratar de precursores ou ideias anteriores à formação das escolas, use 4372; se tratar das teorias sociológicas do século XX, use 4388 ou 4387.
```

### 4372 · amostral

```text
[4372] Criminologia > Etapas Evolutivas e Escolas Criminológicas > Etapas Evolutivas da Criminologia (Antiguidade, Idade Média e Idade Moderna)
Escopo: Evolução histórica do pensamento criminológico antes das escolas científicas: ideias sobre crime e criminoso na Antiguidade, na Idade Média e na Idade Moderna, os precursores e a fase pré-científica da Criminologia.
Inclui: Antiguidade: Código de Hamurabi, Platão e Aristóteles sobre crime, pena e causas sociais do delito; Idade Média: Santo Tomás de Aquino, Santo Agostinho, concepção do crime como pecado e demonologia; Idade Moderna: Thomas More (Utopia) e a crítica social às causas do crime; Fisionomia (Della Porta, Lavater) e frenologia (Gall) como precursoras da antropologia criminal; Distinção entre a fase pré-científica e a fase científica da Criminologia; Marcos históricos do surgimento da Criminologia como ciência autônoma
Não inclui: Postulados e representantes das escolas Clássica, Positiva, Terza Scuola e Escola Moderna Alemã → 4373; Conceito, objeto e autonomia científica da Criminologia → 4381; Métodos empírico e interdisciplinar e funções da Criminologia → 4382; Teorias sociológicas da criminalidade do século XX (Chicago, anomia, labelling) → 4388
Âncoras legais: Platão; Aristóteles; Santo Tomás de Aquino; Thomas More, Utopia; Giambattista Della Porta; Franz Joseph Gall
Desempate: Escolha este nó para ideias, autores e períodos anteriores à sistematização das escolas criminológicas (fase pré-científica e precursores); se a questão versar sobre os postulados de uma escola (Clássica, Positiva etc.), use 4373.
```

### 4375 · amostral

```text
[4375] Criminologia > Política Criminal > Correntes da Política Criminal
Escopo: Movimentos e correntes de política criminal que propõem como o Estado deve responder ao crime, do abolicionismo ao movimento lei e ordem, passando pelo minimalismo e pelo garantismo. Também cobre as velocidades do Direito Penal, exceto a terceira (Direito Penal do Inimigo), que tem nó próprio.
Inclui: Abolicionismo penal (Hulsman, Christie, Mathiesen); Direito penal mínimo e garantismo penal (Ferrajoli, Baratta, Zaffaroni); Movimento lei e ordem e política de tolerância zero; Neorrealismo de esquerda e realismo de direita; Velocidades do Direito Penal (Silva Sánchez): primeira e segunda velocidades; Direito penal máximo, expansionismo penal e direito penal simbólico; Conceito de política criminal e relação com Criminologia e dogmática penal
Não inclui: Direito Penal do Inimigo de Jakobs e terceira velocidade do Direito Penal → 4376; Teoria das janelas quebradas como teoria explicativa da criminalidade → 4388; Modelos de reação ao delito (dissuasório, ressocializador, justiça restaurativa) → 4370; Prevenção primária, secundária e terciária → 4369; Teorias absolutas, relativas e mistas da pena → 4384; Princípio da intervenção mínima como princípio dogmático do Direito Penal → 5172
Âncoras legais: Louk Hulsman; Nils Christie; Thomas Mathiesen; Luigi Ferrajoli; Alessandro Baratta; Eugenio Raúl Zaffaroni; Jesús-María Silva Sánchez
Desempate: Escolha este nó quando a questão comparar correntes político-criminais ou tratar de abolicionismo, minimalismo, garantismo ou lei e ordem. Se o foco for o tratamento do inimigo segundo Jakobs ou a terceira velocidade, use 4376.
```

### 4376 · amostral

```text
[4376] Criminologia > Política Criminal > Direito Penal do Inimigo
Escopo: Teoria do Direito Penal do Inimigo de Günther Jakobs, que distingue cidadão e inimigo. Cobre suas características (antecipação da punibilidade, penas desproporcionais, supressão de garantias, direito penal do autor), a relação com a terceira velocidade do Direito Penal e as críticas que recebe.
Inclui: Distinção entre Direito Penal do cidadão e Direito Penal do inimigo; Inimigo como não pessoa e perda do status de cidadão; Antecipação da tutela penal e punição de atos preparatórios; Penas desproporcionais e relativização ou supressão de garantias processuais; Direito penal do autor em oposição ao direito penal do fato; Terceira velocidade do Direito Penal (Silva Sánchez); Manifestações na legislação (terrorismo, crime organizado) e críticas garantistas
Não inclui: Abolicionismo, garantismo, movimento lei e ordem e as demais velocidades do Direito Penal → 4375; Prevenção geral positiva e funcionalismo sistêmico como teoria da pena → 4384; Tipos penais e regras da Lei de Terrorismo em si → 4706; Regras da Lei de Organizações Criminosas em si → 4705; Fases do iter criminis e punibilidade dos atos preparatórios na dogmática → 5176
Âncoras legais: Günther Jakobs; Jesús-María Silva Sánchez; Lei 13.260/2016, art. 5º
Desempate: Escolha este nó quando a questão tratar da teoria de Jakobs, da figura do inimigo ou da terceira velocidade. Se a questão só cobrar o texto de uma lei penal especial, use o nó da lei.
```

### 4379 · amostral

```text
[4379] Criminologia > Processos de Criminalização e Cifras Criminais > Cifras Criminais
Escopo: Cobre as cifras criminais, isto é, a diferença entre a criminalidade real e a registrada ou punida pelo sistema penal: cifra negra (oculta), cifra dourada e outras cifras "coloridas", suas causas e formas de medição.
Inclui: Cifra negra (oculta): crimes cometidos que não chegam ao conhecimento ou ao registro oficial; Cifra dourada: criminalidade de colarinho branco e dos poderosos, que fica impune ou não é registrada; Cifra cinza: ocorrências registradas que não chegam a processo ou condenação; Outras cifras coloridas citadas pela doutrina (amarela, verde, rosa) e seus significados; Causas da subnotificação: descrédito na polícia, medo de represália, vergonha, desconhecimento; Limites das estatísticas oficiais e pesquisas de vitimização (inquéritos de vitimização) para medir a criminalidade oculta; Relação das cifras com a seletividade do sistema penal
Não inclui: Conceito de criminalização primária e secundária e seletividade das agências penais → 4378; Teoria da associação diferencial e o conceito de crime de colarinho branco de Sutherland como teoria explicativa → 4388; Vitimização primária, secundária e terciária → 4390; Labeling approach e criminologia crítica como teorias → 4388
Âncoras legais: Edwin Sutherland (white collar crime); Pesquisas de vitimização (victim surveys)
Desempate: Use este nó quando a questão tratar da criminalidade não registrada ou não punida (cifras e suas cores, subnotificação, estatísticas); se o foco for o processo de seleção legislativa ou das agências que gera essa diferença, use 4378.
```

### 4378 · amostral

```text
[4378] Criminologia > Processos de Criminalização e Cifras Criminais > Criminalização Primária e Secundária
Escopo: Cobre os processos de criminalização: a primária (criação legislativa de tipos penais e sanções) e a secundária (atuação seletiva das agências policiais, do MP e do Judiciário sobre pessoas concretas), além da seletividade e vulnerabilidade que deles decorrem.
Inclui: Criminalização primária: ato legislativo que tipifica condutas e comina penas; Criminalização secundária: ação punitiva das agências (polícia, MP, juízes) sobre pessoas concretas; Seletividade estrutural do sistema penal e estereótipo do criminoso; Vulnerabilidade e posição de vulnerabilidade na seleção criminalizante (Zaffaroni); Criminalização terciária: efeitos da execução penal e do cárcere sobre o selecionado, quando citada pela doutrina; Agências de criminalização e empreendedores morais
Não inclui: Cifra negra, cifra dourada e demais cifras criminais → 4379; Vitimização primária, secundária e terciária → 4390; Prevenção primária, secundária e terciária do delito → 4369; Labeling approach, desvio primário e secundário (Lemert) e criminologia crítica como teorias → 4388; Movimentos de política criminal (abolicionismo, minimalismo, lei e ordem) → 4375
Âncoras legais: Eugenio Raúl Zaffaroni, Nilo Batista et al., Direito Penal Brasileiro; Howard Becker, Outsiders
Desempate: Use este nó quando a questão distinguir criminalização primária e secundária ou tratar da seletividade das agências; se pedir os postulados da teoria do etiquetamento ou da criminologia crítica como escolas, use 4388, e se tratar de vitimização primária, secundária ou terciária, use 4390.
```

### 4385 · amostral

```text
[4385] Criminologia > Teorias Sociológicas Explicativas da Criminalidade
Escopo: Teorias que explicam a criminalidade: classificação geral (consenso x conflito, macro x microssociológicas), teorias de nível individual (4386), de nível sociológico (4387) e teorias em espécie (4388).
Inclui: Distinção entre teorias do consenso e teorias do conflito; Distinção entre enfoques macrossociológicos e microssociológicos; Visão geral das teorias explicativas da criminalidade; Comparação entre teorias de nível individual e de nível sociológico
Não inclui: Escola de Chicago, anomia, associação diferencial, subcultura delinquente, labeling approach e criminologia crítica → 4388; Teorias de nível individual → 4386; Teorias de nível sociológico → 4387; Escola Clássica e Escola Positiva → 4373; Teorias com enfoque na vítima (estilo de vida, atividades rotineiras) → 4383
Âncoras legais: Émile Durkheim; Robert Merton; Edwin Sutherland; Albert Cohen
Desempate: Use o nó geral só para a classificação das teorias (consenso x conflito, macro x micro); se a questão cobrar o conteúdo de uma teoria específica, use 4388 ou o subtema de nível correspondente.
```

### 4383 · amostral

```text
[4383] Criminologia > Teorias e Síndromes com Enfoque nas Vítimas
Escopo: Teorias vitimológicas que explicam por que certas pessoas se tornam vítimas e síndromes psicológicas associadas à vítima (Estocolmo, Londres, Lima, mulher de Potifar e afins).
Inclui: Síndrome de Estocolmo (vínculo afetivo da vítima com o agressor); Síndrome de Londres (vítima que confronta o captor) e síndrome de Lima (captor que se afeiçoa à vítima); Síndrome da mulher de Potifar (falsa imputação de crime sexual por rejeição); Síndrome da mulher maltratada e ciclo da violência; Teoria do estilo de vida e teoria das atividades rotineiras (Cohen e Felson); Vitimodogmática e contribuição da vítima para o delito
Não inclui: Tipologias de vítimas (Mendelsohn, Von Hentig) → 4366; Vitimização primária, secundária e terciária → 4390; Medidas protetivas e formas de violência na Lei Maria da Penha → 4704; Teorias sociológicas centradas no delinquente → 4388
Âncoras legais: Lawrence Cohen e Marcus Felson; Michael Hindelang; Lenore Walker
Desempate: Escolha este nó quando a questão nomear uma síndrome ou uma teoria explicativa da vitimização; se pedir a categoria de uma vítima numa tipologia, use 4366; se pedir a fase da vitimização, use 4390.
```

### 4390 · amostral

```text
[4390] Criminologia > Vitimologia > Processo de Vitimização
Escopo: Estudo do processo pelo qual a pessoa se torna vítima e sofre danos: vitimização primária, secundária (sobrevitimização pelas instâncias de controle formal) e terciária (pelo meio social ou pela própria vítima), além de heterovitimização, revitimização e violência institucional.
Inclui: Vitimização primária: dano direto causado pelo crime (físico, psíquico, material); Vitimização secundária ou sobrevitimização: sofrimento causado pelas instâncias formais (polícia, MP, Judiciário, perícia); Vitimização terciária: estigmatização e abandono pela família, comunidade e grupo social, ou autovitimização; Heterovitimização (autorrecriminação da vítima) e revitimização; Violência institucional e medidas para evitar a revitimização (escuta especializada, depoimento especial, proteção da dignidade da vítima em audiência); Relação entre vitimização secundária e a não comunicação do crime às autoridades
Não inclui: Tipologias de vítimas de Mendelsohn, von Hentig e Neuman → 4366; Síndromes e teorias centradas na vítima (Estocolmo, Londres, mulher de Potifar, teoria das janelas quebradas aplicada à vítima, estilo de vida) → 4383; Cifras negras, douradas e demais cifras criminais como objeto de estudo → 4379; Crime de abuso de autoridade por violência institucional (Lei 13.869/2019, art. 15-A) → 4684; Regras processuais da oitiva do ofendido no CPP → 5549; Procedimento de escuta especializada e depoimento especial da Lei 13.431/2017 cobrado como lei em si → 4709
Âncoras legais: Lei 13.431/2017, art. 4º, IV; Lei 13.869/2019, art. 15-A; CPP, art. 201; CPP, art. 400-A; Benjamin Mendelsohn; Hans von Hentig
Desempate: Escolha este nó quando a questão tratar das fases ou espécies de vitimização (primária, secundária, terciária) e dos danos sofridos pela vítima; se tratar da tipologia das vítimas, use 4366, e se tratar de síndromes ou teorias vitimológicas nomeadas, use 4383.
```

### 4684 · amostral

```text
[4684] Direito Penal - Legislação Especial > Abuso de Autoridade
Escopo: Crimes de abuso de autoridade da Lei 13.869/2019: sujeitos ativos, elemento subjetivo especial (finalidade de prejudicar, beneficiar-se ou por capricho), ação penal, efeitos da condenação, penas restritivas e tipos em espécie.
Inclui: Sujeito ativo: agente público, servidor ou não, inclusive membros de Poderes, MP e tribunais de contas; Dolo específico e vedação do crime de hermenêutica (divergência na interpretação da lei ou na avaliação de fatos e provas); Ação penal pública incondicionada e ação privada subsidiária; Efeitos da condenação: indenização, inabilitação e perda do cargo condicionadas à reincidência; Tipos em espécie: decretar prisão fora das hipóteses legais, deixar de relaxar prisão ilegal, constranger preso, invadir domicílio, obter prova por meio ilícito; Independência entre as esferas penal, civil e administrativa
Não inclui: Violência arbitrária do art. 322 do CP → 5098; Tortura praticada por agente público (Lei 9.455/1997) → 4707; Exercício arbitrário ou abuso de poder do art. 350 do CP → 5085; Prevaricação (art. 319 do CP) → 5095; Crime de interceptação telefônica sem autorização judicial (Lei 9.296/1996, art. 10) → 4700; Relaxamento da prisão ilegal como instituto processual → 5588
Âncoras legais: Lei 13.869/2019, art. 1º; Lei 13.869/2019, art. 2º; Lei 13.869/2019, art. 3º; Lei 13.869/2019, arts. 4º e 5º; Lei 13.869/2019, arts. 9º a 38
Desempate: Use este nó quando a conduta abusiva de agente público for analisada à luz da Lei 13.869/2019; se o tipo cobrado for do CP (arts. 322 ou 350) ou da Lei de Tortura, use o nó próprio.
```

### 4685 · amostral

```text
[4685] Direito Penal - Legislação Especial > Biossegurança
Escopo: Crimes da Lei de Biossegurança (Lei 11.105/2005): utilização de embriões humanos, engenharia genética em células germinais, clonagem humana e liberação ou manejo irregular de organismos geneticamente modificados (OGM).
Inclui: Uso de células-tronco embrionárias em desacordo com o art. 5º da Lei 11.105/2005; Engenharia genética em célula germinal, zigoto ou embrião humano; Clonagem humana; Liberação ou descarte de OGM no meio ambiente em desacordo com as normas; Tecnologias genéticas de restrição do uso; Constitucionalidade da pesquisa com células-tronco embrionárias (ADI 3510)
Não inclui: Crimes contra a fauna, a flora e poluição (Lei 9.605/1998) → 4688; Aborto e proteção penal da vida intrauterina → 5154; Crimes contra a saúde pública do CP → 5145
Âncoras legais: Lei 11.105/2005, art. 5º; Lei 11.105/2005, arts. 24 a 29
Desempate: Use este nó quando o fato envolver embrião humano, clonagem ou OGM; danos ambientais genéricos vão para Crimes contra o meio ambiente (4688).
```

### 4698 · amostral

```text
[4698] Direito Penal - Legislação Especial > Genocídio
Escopo: Crime de genocídio previsto na Lei 2.889/1956: tipos, elementos subjetivos (intenção de destruir grupo nacional, étnico, racial ou religioso), associação e incitação, e reflexos penais e processuais.
Inclui: Condutas típicas do art. 1º da Lei 2.889/1956; Dolo específico de destruir, no todo ou em parte, grupo nacional, étnico, racial ou religioso; Associação para prática de genocídio (art. 2º) e incitação direta e pública (art. 3º); Genocídio como crime hediondo; Concurso entre genocídio e homicídios e competência do júri (STF, RE 351.487)
Não inclui: Crimes resultantes de preconceito de raça ou cor (Lei 7.716/1989) → 4690; Regime jurídico geral dos crimes hediondos (fiança, graça, progressão) → 4693; Extraterritorialidade incondicionada do genocídio (CP, art. 7º, I, d) → 5182; Regras gerais de competência em razão da matéria → 5482
Âncoras legais: Lei 2.889/1956, arts. 1º a 3º; Lei 8.072/1990, art. 1º, parágrafo único; CP, art. 7º, I, d
```

### 4702 · amostral

```text
[4702] Direito Penal - Legislação Especial > Lavagem de Dinheiro
Escopo: Crimes de lavagem ou ocultação de bens, direitos e valores (Lei 9.613/1998): tipos penais, autonomia em relação à infração antecedente, disposições processuais, medidas assecuratórias, colaboração e deveres de comunicação ao COAF.
Inclui: Tipo do art. 1º e extinção do rol taxativo de crimes antecedentes (Lei 12.683/2012); Autonomia do processo em relação à infração penal antecedente (art. 2º, II e § 1º); Competência da Justiça Federal nas hipóteses do art. 2º, III; Inaplicabilidade do art. 366 do CPP (art. 2º, § 2º); Medidas assecuratórias e alienação antecipada de bens (art. 4º); Colaboração espontânea com redução ou perdão (art. 1º, § 5º); Pessoas obrigadas e comunicação de operações suspeitas ao COAF (arts. 9º a 11)
Não inclui: Receptação (CP, art. 180) → 5169; Favorecimento real (CP, art. 349) → 5084; Crimes contra o Sistema Financeiro Nacional (Lei 7.492/1986) → 4689; Organização criminosa (Lei 12.850/2013) → 4705; Colaboração premiada como meio de obtenção de prova → 5557; Sequestro, arresto e hipoteca legal do CPP → 5496
Âncoras legais: Lei 9.613/1998, art. 1º; Lei 9.613/1998, art. 2º; Lei 9.613/1998, art. 4º; Lei 9.613/1998, arts. 9º a 11
```

### 4707 · amostral

```text
[4707] Direito Penal - Legislação Especial > Tortura
Escopo: Crimes de tortura da Lei 9.455/1997: modalidades típicas, tortura por omissão, qualificadoras, causas de aumento, efeitos da condenação, vedações constitucionais e extraterritorialidade.
Inclui: Tortura-prova, tortura-crime e tortura discriminatória (art. 1º, I); Tortura-castigo de pessoa sob guarda, poder ou autoridade (art. 1º, II); Tortura do preso ou submetido a medida de segurança (art. 1º, § 1º); Omissão de quem tinha o dever de evitar ou apurar (art. 1º, § 2º); Qualificadoras e aumentos de pena (art. 1º, §§ 3º e 4º); Perda do cargo como efeito automático da condenação (art. 1º, § 5º); Inafiançabilidade, insuscetibilidade de graça ou anistia e extraterritorialidade (art. 1º, § 6º; art. 2º)
Não inclui: Maus-tratos (CP, art. 136) → 5143; Crimes da Lei de Abuso de Autoridade (Lei 13.869/2019) → 4684; Tortura como meio qualificador do homicídio (CP, art. 121, § 2º, III) → 5150; Regime jurídico geral dos crimes hediondos e equiparados → 4693
Âncoras legais: Lei 9.455/1997, art. 1º; Lei 9.455/1997, art. 2º; CF, art. 5º, III e XLIII
Desempate: Use este nó quando o sofrimento intenso for elemento do tipo da Lei 9.455/97; se a questão tratar de maus-tratos com finalidade de educação ou correção sem esse dolo, use 5143.
```

### 5069 · amostral

```text
[5069] Penal > Concurso de Crimes > Crime Continuado
Escopo: Crime continuado (continuidade delitiva): várias condutas que geram crimes da mesma espécie, ligados por condições de tempo, lugar e modo de execução, tratados como crime único por ficção jurídica. Abrange a continuidade simples e a específica.
Inclui: Requisitos do art. 71: pluralidade de condutas, crimes da mesma espécie, conexão de tempo, lugar e modo de execução; Teorias objetiva e objetivo-subjetiva (unidade de desígnios, adotada pelo STJ); Crime continuado simples: exasperação de 1/6 a 2/3 conforme o número de infrações; Crime continuado específico: crimes dolosos com violência ou grave ameaça contra vítimas diferentes, aumento até o triplo (art. 71, parágrafo único); Critério temporal jurisprudencial (em regra, até 30 dias entre os crimes); Distinção entre continuidade delitiva e habitualidade ou reiteração criminosa
Não inclui: Lei penal mais grave aplicada ao crime continuado (Súmula 711 do STF) → 5181; Prescrição no crime continuado sem o acréscimo da continuação (Súmula 497 do STF) → 5187; Pluralidade de condutas sem os requisitos da continuidade (cúmulo material) → 5067; Pena de multa na continuidade delitiva → 5070; Crime habitual e crime permanente como classificações de crimes → 5174
Âncoras legais: CP, art. 71
Desempate: Escolha este nó quando a questão discutir requisitos ou dosimetria da continuidade delitiva; se o foco for lei no tempo ou prescrição no crime continuado, use 5181 ou 5187.
```

### 5073 · amostral

```text
[5073] Penal > Concurso de Pessoas > Autoria Mediata, Colateral e Coautoria
Escopo: Modalidades específicas de autoria: autoria mediata (uso de terceiro como instrumento), autoria colateral e incerta, coautoria (divisão de tarefas, coautoria sucessiva) e figuras afins, como autor intelectual e autoria por domínio da organização.
Inclui: Autoria mediata: instrumento inimputável, coagido, em erro ou em obediência hierárquica; Autoria mediata por aparelhos organizados de poder (Roxin); Inadmissibilidade de autoria mediata em crimes de mão própria; Autoria colateral, autoria incerta e autoria desconhecida; Coautoria: divisão de tarefas, domínio funcional do fato, coautoria sucessiva; Autor intelectual e executor de reserva; Multidão delinquente
Não inclui: Teorias gerais da autoria e distinção autor x partícipe → 5072; Instigação, induzimento e auxílio material como participação → 5074; Coação moral irresistível como excludente de culpabilidade do coagido (art. 22) → 5215; Obediência hierárquica como excludente de culpabilidade (art. 22) → 5216; Erro determinado por terceiro (art. 20, § 2º) analisado como erro de tipo → 5224
Âncoras legais: CP, art. 20, § 2º; CP, art. 22; CP, art. 29; CP, art. 62, III
Desempate: Use este nó quando o foco for a responsabilidade do autor mediato, do coautor ou dos autores colaterais; se o foco for a isenção de culpabilidade do instrumento (coagido, subordinado), use 5215 ou 5216.
```

### 5076 · amostral

```text
[5076] Penal > Concurso de Pessoas > Comunicabilidade de Circunstâncias, Condições e Elementares
Escopo: Regra do art. 30 do CP: incomunicabilidade das circunstâncias e condições de caráter pessoal, salvo quando elementares do crime, e comunicabilidade das circunstâncias objetivas conhecidas pelos concorrentes.
Inclui: Distinção entre elementares e circunstâncias; objetivas x subjetivas; Comunicação da elementar 'funcionário público' ao particular (ex.: peculato em coautoria); Partícipe ou coautor no infanticídio (comunicação do estado puerperal); Necessidade de conhecimento do concorrente para a comunicação; Qualificadoras subjetivas x objetivas no concurso (ex.: motivo torpe, meio cruel); Incomunicabilidade de reincidência, menoridade e outras condições pessoais
Não inclui: Elementos típicos do peculato em si → 5089; Elementos típicos do infanticídio em si → 5153; Concorrente que quis crime menos grave (art. 29, § 2º) → 5075; Conceito de funcionário público para fins penais e noções gerais dos crimes funcionais → 5088; Agravantes e atenuantes na dosimetria em geral → 5203
Âncoras legais: CP, art. 30; CP, art. 327
Desempate: Use este nó quando a questão perguntar se uma qualidade pessoal ou circunstância se estende ao comparsa (art. 30), mesmo que ambientada em peculato ou infanticídio; use o nó do crime só se a questão tratar dos elementos do tipo sem discutir o concurso.
```

### 5075 · amostral

```text
[5075] Penal > Concurso de Pessoas > Cooperação Dolosamente Distinta
Escopo: Cooperação dolosamente distinta (desvio subjetivo de conduta): concorrente que quis participar de crime menos grave responde pela pena deste, aumentada até metade se o resultado mais grave era previsível (art. 29, § 2º).
Inclui: Art. 29, § 2º: aplicação da pena do crime menos grave querido; Aumento de até metade quando o resultado mais grave era previsível; Excesso do executor (excesso quantitativo e qualitativo); Exemplo clássico: combinação de furto que evolui para roubo ou latrocínio; Distinção entre previsibilidade (aumento) e assunção do risco (dolo eventual, responde pelo crime mais grave); Exceção à teoria monista
Não inclui: Participação de menor importância (art. 29, § 1º) → 5074; Teoria monista e suas exceções pluralistas em geral → 5072; Comunicação de qualificadoras e circunstâncias ao coautor (art. 30) → 5076; Dolo eventual e culpa consciente em geral → 5222; Latrocínio e roubo majorado em si → 5160
Âncoras legais: CP, art. 29, § 2º
Desempate: Use este nó quando um concorrente quis crime diverso e menos grave que o praticado pelo outro; se o problema for a extensão de circunstância pessoal ou elementar ao comparsa, use 5076.
```

### 5080 · amostral

```text
[5080] Penal > Dos Crimes Contra a Administração Judicial > Denunciação Caluniosa, Comunicação Falsa de Crime ou Contravenção e Autoacusação Falsa
Escopo: Crimes que provocam indevidamente a atuação do Estado com imputação ou notícia falsa: denunciação caluniosa, comunicação falsa de crime ou contravenção e autoacusação falsa (CP, arts. 339 a 341).
Inclui: Denunciação caluniosa: dar causa a inquérito, PIC, processo judicial, PAD, inquérito civil ou ação de improbidade imputando crime, infração ético-disciplinar ou ato ímprobo a quem se sabe inocente; Exigência de dolo direto (ciência da inocência) e de imputação a pessoa determinada; Aumento pelo anonimato ou nome suposto e diminuição quando a imputação é de contravenção; Comunicação falsa de crime ou contravenção que se sabe não ter ocorrido, sem indicar autor determinado; Autoacusação falsa de crime inexistente ou praticado por outrem; Distinções entre os três tipos e consumação com a instauração da investigação ou procedimento
Não inclui: Calúnia como crime contra a honra, sem provocar investigação ou processo → 5122; Denunciação caluniosa com finalidade eleitoral (Código Eleitoral) → 4692; Falsa declaração de testemunha ou perito em processo → 5081; Atribuir-se falsa identidade para obter vantagem → 5119; Inovação artificiosa no estado de coisas para induzir juiz ou perito a erro → 5083
Âncoras legais: CP, art. 339; CP, art. 340; CP, art. 341
Desempate: Escolha este nó quando a falsidade consiste em imputar ou noticiar crime à autoridade, provocando sua atuação; se apenas ofende a honra sem provocar a máquina estatal, use calúnia (5122).
```

### 5081 · amostral

```text
[5081] Penal > Dos Crimes Contra a Administração Judicial > Falso Testemunho ou Falsa Perícia e Corrupção Ativa de Testemunha ou Perito
Escopo: Crimes de falso testemunho ou falsa perícia (fazer afirmação falsa, negar ou calar a verdade como testemunha, perito, contador, tradutor ou intérprete) e de corrupção ativa de testemunha ou perito (CP, arts. 342 e 343).
Inclui: Sujeitos ativos: testemunha, perito, contador, tradutor e intérprete; crime de mão própria; Participação do advogado que instrui a testemunha a mentir (admissão pela jurisprudência); Processo judicial, administrativo, inquérito policial ou juízo arbitral; Causas de aumento: suborno, processo penal e entidade da administração pública indireta; Retratação antes da sentença no processo em que ocorreu o ilícito extingue a punibilidade; Corrupção ativa de testemunha ou perito: dar, oferecer ou prometer vantagem para falsear
Não inclui: Corrupção ativa de funcionário público em geral → 5093; Uso de violência ou grave ameaça contra testemunha (coação no curso do processo) → 5086; Prova testemunhal, compromisso e informantes no CPP → 5550; Imputar crime a inocente dando causa a investigação → 5080; Inovar artificiosamente o estado de lugar, coisa ou pessoa → 5083
Âncoras legais: CP, art. 342; CP, art. 343
Desempate: Escolha este nó quando o núcleo é a falsidade do depoimento ou laudo ou o suborno para obtê-la; se o meio é violência ou grave ameaça contra a testemunha, use 5086.
```

### 5084 · amostral

```text
[5084] Penal > Dos Crimes Contra a Administração Judicial > Favorecimento Pessoal e Real
Escopo: Crimes de favorecimento pessoal (auxiliar autor de crime a subtrair-se à ação da autoridade) e favorecimento real (prestar auxílio destinado a tornar seguro o proveito do crime), previstos no CP, arts. 348 e 349.
Inclui: Favorecimento pessoal: auxílio posterior ao crime, sem ajuste prévio; Pena diversa conforme o crime do favorecido seja punido com reclusão ou não; Escusa absolutória para ascendente, descendente, cônjuge ou irmão (art. 348, § 2º); Favorecimento real: assegurar o proveito do crime fora dos casos de coautoria ou receptação; Distinção com participação: ajuste prévio torna o auxiliar partícipe; Distinção entre favorecimento real e receptação
Não inclui: Adquirir, receber ou ocultar produto de crime em proveito próprio ou alheio → 5169; Ingresso de aparelho celular em estabelecimento prisional (art. 349-A) → 5086; Ocultação ou dissimulação de bens provenientes de infração penal → 4702; Auxílio combinado antes ou durante a execução do crime → 5074; Facilitar a fuga de pessoa presa → 5086
Âncoras legais: CP, art. 348; CP, art. 349
Desempate: Escolha este nó para auxílio posterior e não ajustado ao autor ou ao proveito do crime; se o agente busca proveito econômico com o produto, use receptação (5169).
```

### 5083 · amostral

```text
[5083] Penal > Dos Crimes Contra a Administração Judicial > Fraude Processual
Escopo: Crime de fraude processual: inovar artificiosamente, na pendência de processo civil ou administrativo, o estado de lugar, de coisa ou de pessoa para induzir a erro o juiz ou o perito, com pena em dobro se destinado a produzir efeito em processo penal (CP, art. 347).
Inclui: Inovação artificiosa do estado de lugar, coisa ou pessoa; Finalidade especial de induzir a erro o juiz ou o perito; Crime formal: consuma-se com a inovação idônea, ainda que o erro não ocorra; Aplicação da pena em dobro quando o efeito se destina a processo penal, ainda que não iniciado; Questão da autodefesa do autor do crime que altera a cena
Não inclui: Inovar o local de acidente de trânsito com vítima (CTB) → 4691; Inovação artificiosa praticada por autoridade (Lei de Abuso de Autoridade) → 4684; Afirmação falsa de perito ou testemunha → 5081; Falsificação de documento público ou particular → 5118; Cadeia de custódia e preservação de vestígios no CPP → 5544
Âncoras legais: CP, art. 347
Desempate: Escolha este nó quando a fraude altera materialmente lugar, coisa ou pessoa para enganar juiz ou perito; se a fraude é falsificação de documento, use 5118.
```

### 5086 · amostral

```text
[5086] Penal > Dos Crimes Contra a Administração Judicial > Outros crimes contra a Administração Judicial
Escopo: Nó residual dos crimes contra a administração da justiça sem subtema próprio: reingresso de estrangeiro expulso, coação no curso do processo, ingresso de celular em presídio, fuga, evasão, arrebatamento, motim, patrocínio infiel, sonegação de papel, exploração de prestígio e outros (CP, arts. 338 a 359).
Inclui: Reingresso de estrangeiro expulso (art. 338); Coação no curso do processo, inclusive aumento em processo de crime contra a dignidade sexual (art. 344); Ingresso de aparelho de comunicação em estabelecimento prisional (art. 349-A); Fuga, evasão mediante violência, arrebatamento de preso e motim de presos (arts. 351 a 354); Patrocínio infiel e tergiversação (art. 355) e sonegação de papel ou objeto de valor probatório (art. 356); Exploração de prestígio junto a juiz, jurado, MP, perito ou testemunha (art. 357); Violência ou fraude em arrematação judicial e desobediência a decisão judicial sobre perda ou suspensão de direito (arts. 358 e 359)
Não inclui: Solicitar vantagem a pretexto de influir em funcionário público em geral (tráfico de influência) → 5101; Omissão do diretor de presídio quanto ao acesso do preso a celular (art. 319-A) → 5095; Fuga e posse de celular como falta grave na execução penal → 4703; Suborno de testemunha ou perito para falsear → 5081; Crimes contra as finanças públicas (arts. 359-A a 359-H) → 5147; Favorecimento pessoal ou real ao autor do crime → 5084
Âncoras legais: CP, art. 338; CP, art. 344; CP, art. 349-A; CP, arts. 351 a 359
Desempate: Use este nó residual só quando o crime contra a administração da justiça não estiver em nenhum subtema irmão (5080 a 5085); se a questão tratar de vários crimes do capítulo em conjunto, prefira o pai 5079.
```

### 5091 · amostral

```text
[5091] Penal > Dos Crimes Contra a Administração Pública > Concussão e Excesso de Exação
Escopo: Concussão (CP, art. 316, caput), em que o funcionário exige vantagem indevida em razão da função, e excesso de exação (art. 316, §§ 1º e 2º), relativo à cobrança indevida ou vexatória de tributo ou contribuição e ao desvio do que foi recebido indevidamente.
Inclui: Núcleo 'exigir' e metus publicae potestatis; Concussão como crime formal: consumação com a exigência; Exigência feita fora da função ou antes de assumi-la, mas em razão dela; Excesso de exação: cobrança de tributo indevido ou por meio vexatório; Forma qualificada do § 2º (desvio do que recebeu indevidamente); Recebimento posterior da vantagem como exaurimento
Não inclui: Funcionário que solicita ou recebe vantagem, sem exigir → 5092; Exigência de vantagem mediante violência ou grave ameaça, fora do contexto funcional → 5161; Particular que oferece ou promete vantagem ao funcionário → 5093; Apropriação ou desvio de dinheiro público de que tem a posse → 5089; Exigência de vantagem por funcionário fiscal para deixar de lançar tributo (Lei 8.137/1990, art. 3º, II) → 4695
Âncoras legais: CP, art. 316
Desempate: Use este nó quando o verbo for 'exigir' (imposição) ou houver cobrança indevida de tributo; 'solicitar', 'receber' ou 'aceitar promessa' vão para 5092.
```

### 5096 · amostral

```text
[5096] Penal > Dos Crimes Contra a Administração Pública > Condescendência Criminosa
Escopo: Condescendência criminosa (CP, art. 320): funcionário que, por indulgência, deixa de responsabilizar subordinado que cometeu infração no exercício do cargo ou, sem competência para isso, não leva o fato ao conhecimento da autoridade competente.
Inclui: Omissão por indulgência (tolerância, clemência) em relação a subordinado; Infração do subordinado cometida no exercício do cargo; Omissão em comunicar o fato à autoridade competente; Crime omissivo próprio, de menor potencial ofensivo; Distinção quanto ao motivo: indulgência x interesse ou sentimento pessoal
Não inclui: Omissão de ato de ofício para satisfazer interesse ou sentimento pessoal → 5095; Omissão em vedar acesso do preso a celular (art. 319-A) → 5095; Auxílio a autor de crime para subtrair-se à ação da autoridade → 5084; Omissão retribuída com vantagem indevida → 5092
Âncoras legais: CP, art. 320
Desempate: Escolha este nó quando a omissão consiste em não responsabilizar subordinado por indulgência; se o motivo for interesse ou sentimento pessoal, use 5095.
```

### 5094 · amostral

```text
[5094] Penal > Dos Crimes Contra a Administração Pública > Contrabando ou Descaminho
Escopo: Descaminho (CP, art. 334) e contrabando (CP, art. 334-A), crimes de particular contra a Administração em geral, envolvendo ilusão de tributos na importação/exportação e mercadoria proibida; abrange a facilitação pelo funcionário (art. 318).
Inclui: Distinção entre descaminho (mercadoria permitida, ilusão de tributo) e contrabando (mercadoria proibida); Insignificância no descaminho (parâmetro de R$ 20.000) e, em regra, inaplicabilidade ao contrabando; Contrabando de cigarros; Figuras equiparadas e aumento pelo transporte aéreo, marítimo ou fluvial; Desnecessidade de constituição definitiva do crédito tributário no descaminho; Facilitação de contrabando ou descaminho por funcionário (art. 318)
Não inclui: Sonegação fiscal e supressão de tributos internos (Lei 8.137/1990) → 4695; Tráfico internacional de drogas → 4708; Tráfico internacional de arma de fogo (Lei 10.826/2003, art. 18) → 4697; Competência da Justiça Federal para processar contrabando e descaminho → 5482; Importação de medicamento falsificado ou sem registro (CP, art. 273) → 5145
Âncoras legais: CP, art. 334; CP, art. 334-A; CP, art. 318
Desempate: Use este nó para importação/exportação de mercadorias com ilusão de tributo ou proibidas; se o objeto for droga, arma ou medicamento com tipo específico, prevalece a lei ou o tipo especial.
```

### 5090 · amostral

```text
[5090] Penal > Dos Crimes Contra a Administração Pública > Emprego Irregular de Verbas ou Rendas Públicas
Escopo: Emprego irregular de verbas ou rendas públicas (CP, art. 315): dar às verbas ou rendas públicas aplicação diversa da estabelecida em lei, sem desvio em proveito próprio ou alheio.
Inclui: Aplicação de verba pública em finalidade pública diversa da prevista em lei; Exigência de lei fixando a destinação da verba; Ausência de proveito particular como traço distintivo; Sujeito ativo: funcionário com poder de disposição das verbas; Crime de menor potencial ofensivo
Não inclui: Desvio de dinheiro público em proveito próprio ou alheio (peculato-desvio) → 5089; Ordenação de despesa não autorizada e demais crimes contra as finanças públicas (arts. 359-A a 359-H) → 5147; Conceito de funcionário público para fins penais → 5088
Âncoras legais: CP, art. 315
Desempate: Escolha este nó quando a verba é usada em outra finalidade pública, sem proveito particular; havendo desvio em proveito próprio ou alheio, use 5089; se a infração for às regras de finanças públicas dos arts. 359-A a 359-H, use 5147.
```

### 5089 · amostral

```text
[5089] Penal > Dos Crimes Contra a Administração Pública > Peculato e Peculato Mediante Erro de Outrem
Escopo: Peculato em todas as modalidades (CP, art. 312: apropriação, desvio, furto e culposo, com a reparação do dano) e peculato mediante erro de outrem (art. 313); abrange também a inserção de dados falsos e a modificação de sistema de informações (arts. 313-A e 313-B).
Inclui: Peculato-apropriação e peculato-desvio (art. 312, caput); Peculato-furto ou impróprio (art. 312, § 1º); Peculato culposo e reparação do dano antes ou depois da sentença irrecorrível (§§ 2º e 3º); Peculato de uso e bem particular sob guarda da Administração; Peculato mediante erro de outrem (art. 313); Inserção de dados falsos e modificação não autorizada em sistema (arts. 313-A e 313-B)
Não inclui: Aplicação de verba pública em finalidade pública diversa, sem proveito particular → 5090; Apropriação de coisa alheia por particular ou fora da função pública → 5165; Obtenção de vantagem induzindo a vítima em erro por quem não é funcionário → 5166; Comunicabilidade da condição de funcionário ao particular partícipe → 5076; Conceito de funcionário público e equiparado (art. 327) → 5088
Âncoras legais: CP, art. 312; CP, art. 313; CP, art. 313-A; CP, art. 313-B
Desempate: Use este nó quando o funcionário se apropria, desvia ou subtrai bem de que tem posse ou facilidade em razão do cargo, ou se aproveita de erro alheio; se a verba é só aplicada em outro fim público, use 5090.
```

### 5095 · amostral

```text
[5095] Penal > Dos Crimes Contra a Administração Pública > Prevaricação
Escopo: Prevaricação (CP, art. 319): retardar ou deixar de praticar ato de ofício, ou praticá-lo contra disposição legal, para satisfazer interesse ou sentimento pessoal; inclui a prevaricação imprópria do art. 319-A (acesso de preso a aparelho de comunicação).
Inclui: Elemento subjetivo especial: interesse ou sentimento pessoal; Retardar, omitir ou praticar ato de ofício contra a lei; Distinção com corrupção passiva privilegiada (ausência de pedido ou vantagem); Diretor ou agente penitenciário que deixa de vedar acesso a celular (art. 319-A); Crime de menor potencial ofensivo
Não inclui: Omissão de responsabilizar subordinado por indulgência → 5096; Funcionário que cede a pedido ou influência de outrem (art. 317, § 2º) → 5092; Particular que ingressa com celular em estabelecimento prisional (art. 349-A) → 5086; Condutas de autoridade tipificadas na Lei de Abuso de Autoridade → 4684
Âncoras legais: CP, art. 319; CP, art. 319-A
Desempate: Escolha este nó quando o motivo da conduta funcional for interesse ou sentimento pessoal; pedido ou influência de terceiro leva a 5092 (§ 2º) e indulgência com subordinado leva a 5096.
```

### 5100 · amostral

```text
[5100] Penal > Dos Crimes Contra a Administração Pública > Resistência, Desobediência e Desacato
Escopo: Crimes de particular contra a Administração em geral: resistência (CP, art. 329), desobediência (art. 330) e desacato (art. 331), incluindo a relação entre eles e a controvérsia sobre a convencionalidade do desacato.
Inclui: Resistência: oposição à execução de ato legal mediante violência ou ameaça; forma qualificada se o ato não se executa; Resistência passiva e fuga sem violência como atípicas; Desobediência: ordem legal de funcionário e destinatário com dever de cumpri-la; Desobediência afastada quando há sanção administrativa ou civil específica sem ressalva de cumulação; Desacato: ofensa ao funcionário no exercício da função ou em razão dela; constitucionalidade (STF, ADPF 496); Absorção da desobediência pela resistência
Não inclui: Descumprimento de medida protetiva de urgência (Lei 11.340/2006, art. 24-A) → 4704; Ofensa à honra de funcionário fora do exercício e sem relação com a função → 5124; Desobediência a decisão judicial sobre perda ou suspensão de direito (art. 359) → 5086; Violação de suspensão ou proibição de dirigir (CTB, art. 307) → 4691; Recusa de dados sobre a própria identidade à autoridade (LCP, art. 68) → 4686
Âncoras legais: CP, art. 329; CP, art. 330; CP, art. 331
Desempate: Use este nó para oposição, descumprimento ou ofensa de particular a funcionário no exercício da função; se a ordem descumprida for medida protetiva ou decisão com tipo especial, prevalece o nó da lei ou tipo específico.
```

### 5101 · amostral

```text
[5101] Penal > Dos Crimes Contra a Administração Pública > Tráfico de Influência
Escopo: Tráfico de influência (CP, art. 332): solicitar, exigir, cobrar ou obter vantagem a pretexto de influir em ato praticado por funcionário público no exercício da função; inclui a majorante e a modalidade em transação comercial internacional (art. 337-C).
Inclui: 'Venda de fumaça': alegação de influência real ou fictícia sobre funcionário; Sujeito ativo comum (qualquer pessoa, inclusive funcionário); Aumento de metade se o agente alega ou insinua que a vantagem se destina ao funcionário; Consumação formal com a solicitação, exigência ou cobrança; Tráfico de influência em transação comercial internacional (art. 337-C)
Não inclui: Exploração de prestígio perante juiz, jurado, membro do MP, perito ou testemunha (art. 357) → 5086; Funcionário que recebe vantagem em razão da própria função → 5092; Funcionário que patrocina interesse privado perante a Administração → 5097; Oferta de vantagem ao funcionário para que pratique ato de ofício → 5093
Âncoras legais: CP, art. 332; CP, art. 337-C
Desempate: Use este nó quando o agente vende influência sobre funcionário da Administração em geral; se a influência alegada recair sobre juiz, jurado, MP, perito ou testemunha, use 5086 (exploração de prestígio).
```

### 5099 · amostral

```text
[5099] Penal > Dos Crimes Contra a Administração Pública > Usurpação de Função Pública
Escopo: Usurpação de função pública (CP, art. 328): exercer indevidamente função pública, com a forma qualificada quando o agente aufere vantagem; abrange a distinção com figuras próximas de exercício ilegítimo de função.
Inclui: Prática efetiva de atos próprios do cargo por quem não está investido; Forma qualificada pelo auferimento de vantagem (parágrafo único); Sujeito ativo particular ou funcionário que usurpa função alheia; Distinção com exercício funcional ilegalmente antecipado ou prolongado (art. 324); Necessidade de praticar ato de ofício, não bastando intitular-se funcionário
Não inclui: Atribuir-se falsa identidade sem praticar atos da função (art. 307) → 5119; Fingir-se funcionário público (LCP, art. 45) → 4686; Fazer justiça pelas próprias mãos (art. 345) → 5082; Exigir vantagem em razão de função que efetivamente exerce → 5091
Âncoras legais: CP, art. 328; CP, art. 324
Desempate: Escolha este nó quando o agente pratica atos da função pública sem investidura; se apenas se apresenta como funcionário sem praticar atos, use 5119 ou 4686.
```

### 5108 · amostral

```text
[5108] Penal > Dos Crimes Contra a Dignidade Sexual > Corrupção de Menores
Escopo: Crime de corrupção de menores do Código Penal (art. 218): induzir alguém menor de 14 anos a satisfazer a lascívia de outrem. Não abrange a corrupção de menores do ECA (art. 244-B), que trata de levar o menor a praticar infração penal.
Inclui: Tipo do art. 218 do CP: induzir menor de 14 anos a satisfazer a lascívia de outrem; Lenocínio que tem como vítima o vulnerável etário; Distinção entre induzir a satisfazer a lascívia (contemplação) e a prática de ato libidinoso com o menor; Sujeito passivo menor de 14 anos e irrelevância do consentimento; Momento consumativo e tentativa
Não inclui: Corrupção de menor para a prática de infração penal (ECA, art. 244-B; Súmula 500 do STJ) → 4709; Prática de conjunção carnal ou ato libidinoso com menor de 14 anos → 5103; Praticar ato libidinoso na presença de menor de 14 anos (art. 218-A) e favorecimento da prostituição de vulnerável (art. 218-B) → 5109; Mediação para servir à lascívia de outrem com vítima maior de 14 anos (art. 227) → 5109
Âncoras legais: CP, art. 218
Desempate: Use este nó só para o art. 218 do CP (finalidade sexual, vítima menor de 14 anos); se o menor for levado a praticar infração penal, use 4709 (ECA, art. 244-B); se houver ato libidinoso com o próprio menor, use 5103.
```

### 5103 · amostral

```text
[5103] Penal > Dos Crimes Contra a Dignidade Sexual > Estupro e Estupro de Vulnerável
Escopo: Estupro (CP, art. 213), com suas qualificadoras, e estupro de vulnerável (CP, art. 217-A): conjunção carnal ou outro ato libidinoso mediante violência ou grave ameaça, ou com menor de 14 anos ou pessoa sem discernimento ou que não pode oferecer resistência.
Inclui: Tipo misto alternativo do art. 213 após a Lei 12.015/2009 (crime único ou concurso); Qualificadoras por lesão grave, morte ou vítima menor de 18 e maior de 14 anos; Estupro de vulnerável: menor de 14 anos, enfermidade, deficiência mental ou impossibilidade de resistir; Irrelevância do consentimento e da experiência sexual prévia da vítima (Súmula 593 do STJ; art. 217-A, § 5º); Estupro virtual e ato libidinoso sem contato físico; Consumação, tentativa e desclassificação para importunação sexual
Não inclui: Ato libidinoso sem violência nem grave ameaça e sem vulnerabilidade da vítima → 5105; Conjunção carnal obtida por fraude que impede ou dificulta a livre manifestação de vontade → 5104; Divulgação de cena de estupro (art. 218-C) → 5109; Ação penal e causas de aumento dos arts. 225, 226 e 234-A → 5110; Hediondez e consequências da Lei 8.072/1990 → 4693; Estupro no contexto de violência doméstica: medidas protetivas e regras da Lei Maria da Penha → 4704
Âncoras legais: CP, art. 213; CP, art. 217-A
Desempate: Escolha este nó quando houver violência ou grave ameaça, ou vítima vulnerável; se a vontade da vítima foi viciada por fraude sem que ela fosse vulnerável, use 5104; se não houve violência nem vulnerabilidade, use 5105.
```

### 5122 · amostral

```text
[5122] Penal > Dos Crimes Contra a Honra > Calúnia
Escopo: Crime de calúnia (CP, art. 138): imputar falsamente a alguém fato definido como crime. Abrange a figura de quem propala ou divulga a imputação, a calúnia contra os mortos e a exceção da verdade própria da calúnia, com suas vedações.
Inclui: Elementos do tipo: imputação de fato determinado, definido como crime, e falsidade da imputação; Distinção entre calúnia (fato criminoso), difamação (fato ofensivo) e injúria (qualidade negativa); Propalar ou divulgar a calúnia sabendo que é falsa (art. 138, § 1º); Calúnia contra os mortos (art. 138, § 2º); Exceção da verdade e hipóteses de vedação (art. 138, § 3º); Consumação quando terceiro toma conhecimento (honra objetiva); imputação de contravenção não configura calúnia
Não inclui: Dar causa a investigação, processo ou ação de improbidade contra alguém, imputando-lhe crime que sabe ser inocente (denunciação caluniosa) → 5080; Causas de aumento, exclusão do crime, retratação, pedido de explicações e ação penal nos crimes contra a honra (arts. 141 a 145) → 5121; Imputação de fato ofensivo à reputação que não constitui crime → 5123; Calúnia na propaganda eleitoral (Código Eleitoral) → 4692; Rito processual da queixa-crime e da ação penal privada → 5472
Âncoras legais: CP, art. 138
Desempate: Use este nó quando a questão tratar dos elementos do tipo de calúnia ou da exceção da verdade na calúnia. Se tratar de regra dos arts. 141 a 145 aplicável a todos os crimes contra a honra, use 5121. Se a imputação falsa provocar investigação ou processo contra a vítima, use 5080.
```

### 5123 · amostral

```text
[5123] Penal > Dos Crimes Contra a Honra > Difamação
Escopo: Crime de difamação (CP, art. 139): imputar a alguém fato ofensivo à reputação, verdadeiro ou falso, que não seja crime. Abrange a exceção da verdade restrita ao funcionário público ofendido no exercício das funções.
Inclui: Imputação de fato determinado, desonroso e não criminoso; a veracidade do fato é irrelevante; Ofensa à honra objetiva e consumação quando terceiro toma conhecimento; Imputação de contravenção penal configura difamação, não calúnia; Exceção da verdade cabível só contra funcionário público, ofendido em razão de suas funções (art. 139, parágrafo único); Distinção entre difamação, calúnia e injúria; Pessoa jurídica como possível vítima de difamação, segundo a doutrina
Não inclui: Imputação falsa de fato definido como crime → 5122; Atribuição de qualidade negativa, sem fato determinado → 5124; Imunidade judiciária, crítica literária e conceito desfavorável de funcionário público (exclusão do crime, art. 142) → 5121; Retratação do querelado como causa extintiva da punibilidade, em seu aspecto geral → 5196; Difamação na propaganda eleitoral → 4692
Âncoras legais: CP, art. 139
Desempate: Use este nó quando o núcleo da questão for imputar fato desonroso não criminoso ou a exceção da verdade na difamação. Se o fato imputado for crime, use 5122. Se a questão tratar das regras comuns dos arts. 141 a 145, use 5121.
```

### 5121 · amostral

```text
[5121] Penal > Dos Crimes Contra a Honra > Disposições Gerais e Comuns aos Crimes Contra a Honra
Escopo: Regras comuns à calúnia, difamação e injúria (CP, arts. 141 a 145): causas de aumento de pena, exclusão do crime, retratação, pedido de explicações em juízo e titularidade da ação penal.
Inclui: Causas de aumento do art. 141: contra Presidente da República ou chefe de governo estrangeiro, contra funcionário público em razão das funções, na presença de várias pessoas, contra idoso ou pessoa com deficiência, mediante paga, em redes sociais e contra a mulher por razões da condição do sexo feminino; Exclusão do crime do art. 142: ofensa irrogada em juízo, crítica literária, artística ou científica e conceito emitido por funcionário público; Retratação antes da sentença na calúnia e na difamação (art. 143); Pedido de explicações em juízo (art. 144); Regra da ação penal privada e exceções do art. 145: requisição do Ministro da Justiça e representação; Legitimidade concorrente do funcionário público ofendido (Súmula 714 do STF)
Não inclui: Elementos do tipo e exceção da verdade na calúnia → 5122; Elementos do tipo e exceção da verdade na difamação → 5123; Injúria real, injúria preconceituosa e perdão judicial na injúria (art. 140) → 5124; Renúncia, perdão do ofendido e retratação como causas de extinção da punibilidade em geral (art. 107 do CP) → 5196; Procedimento da queixa-crime e rito dos crimes contra a honra no CPP (arts. 519 a 523) → 5474; Requisitos e procedimento da representação no CPP → 5471
Âncoras legais: CP, art. 141; CP, art. 142; CP, art. 143; CP, art. 144; CP, art. 145; Súmula 714 do STF
Desempate: Use este nó quando a questão tratar de regra aplicável aos três crimes contra a honra (arts. 141 a 145), como majorantes, imunidades, retratação, pedido de explicações ou ação penal no CP. Se a questão tratar só dos elementos de um tipo específico, use 5122, 5123 ou 5124. Se tratar do procedimento previsto no CPP, use o nó de Processo Penal.
```

### 5124 · amostral

```text
[5124] Penal > Dos Crimes Contra a Honra > Injúria
Escopo: Crime de injúria (CP, art. 140): ofender a dignidade ou o decoro de alguém. Abrange o perdão judicial, a injúria real e a injúria qualificada pela utilização de elementos de religião ou condição de pessoa idosa ou com deficiência.
Inclui: Ofensa à honra subjetiva por atribuição de qualidade negativa, sem imputação de fato; consumação quando a própria vítima toma conhecimento; Inadmissibilidade de exceção da verdade; Perdão judicial por provocação direta ou retorsão imediata (art. 140, § 1º); Injúria real: violência ou vias de fato aviltantes, com cúmulo da pena da violência (art. 140, § 2º); Injúria qualificada pelo uso de elementos de religião ou condição de pessoa idosa ou com deficiência (art. 140, § 3º); Distinção entre injúria, calúnia e difamação
Não inclui: Injúria racial por raça, cor, etnia ou procedência nacional (Lei 7.716/1989, art. 2º-A, incluído pela Lei 14.532/2023) → 4690; Desacato a funcionário público no exercício da função ou em razão dela → 5100; Ação penal na injúria e causas de aumento do art. 141 → 5121; Lesão corporal resultante da injúria real, analisada como crime autônomo → 5077; Perdão judicial como causa geral de extinção da punibilidade → 5197; Injúria no contexto de violência doméstica e familiar contra a mulher, quanto às regras da Lei 11.340/2006 → 4704
Âncoras legais: CP, art. 140; Lei 7.716/1989, art. 2º-A
Desempate: Use este nó quando o núcleo da questão for a ofensa à dignidade ou ao decoro, a injúria real, a injúria qualificada do § 3º ou o perdão judicial na injúria. Se a ofensa for por raça, cor, etnia ou procedência nacional, use 4690. Se a vítima for funcionário público ofendido no exercício da função, na sua presença, use 5100.
```

### 5127 · amostral

```text
[5127] Penal > Dos Crimes Contra a Incolumidade Pública > Dos Crimes Contra a Segurança dos Meios de Comunicação e Transporte e Outros Serviços Públicos
Escopo: Crimes do Capítulo II do Título VIII do CP (arts. 260 a 266): atentados contra a segurança de transportes ferroviário, marítimo, fluvial, aéreo e outros, arremesso de projétil e atentado ou interrupção de serviços de utilidade pública e de comunicação.
Inclui: Perigo de desastre ferroviário e desastre ferroviário (art. 260); Atentado contra a segurança de transporte marítimo, fluvial ou aéreo, incluindo sinistro e forma culposa (art. 261); Atentado contra a segurança de outro meio de transporte (art. 262) e forma qualificada pelo resultado (art. 263); Arremesso de projétil contra veículo em movimento (art. 264); Atentado contra a segurança de serviço de utilidade pública: água, luz, força ou calor (art. 265); Interrupção ou perturbação de serviço telegráfico, telefônico, informático, telemático ou de informação de utilidade pública, com pena em dobro em calamidade pública (art. 266)
Não inclui: Incêndio, explosão, inundação, desabamento e demais crimes de perigo comum (arts. 250 a 259) → 5126; Envenenamento de água potável, epidemia e demais crimes contra a saúde pública → 5145; Paralisação de trabalho de interesse coletivo (art. 201) → 5135; Sabotagem de meios de transporte ou serviços essenciais com finalidade terrorista (Lei 13.260/2016) → 4706; Sabotagem de meios de comunicação e serviços essenciais com o fim de abolir o Estado Democrático de Direito (art. 359-R) → 5156; Crimes cometidos na direção de veículo automotor (CTB) → 4691
Âncoras legais: CP, arts. 260 a 266; CP, art. 263; CP, art. 266, §§ 1º e 2º
Desempate: Escolha este nó quando o perigo coletivo recair sobre meio de transporte, comunicação ou serviço de utilidade pública (arts. 260 a 266); se o perigo vier de fogo, explosão, gás, água, desabamento ou praga, sem atingir especificamente esses serviços, use 5126.
```

### 5126 · amostral

```text
[5126] Penal > Dos Crimes Contra a Incolumidade Pública > Dos Crimes de Perigo Comum
Escopo: Crimes do Capítulo I do Título VIII do CP (arts. 250 a 259): condutas que expõem a perigo a vida, a integridade ou o patrimônio de número indeterminado de pessoas, como incêndio, explosão, inundação e desabamento, com as formas qualificadas pelo resultado.
Inclui: Incêndio e suas causas de aumento e forma culposa (art. 250); Explosão (art. 251) e uso de gás tóxico ou asfixiante (art. 252); Fabrico, fornecimento, aquisição, posse ou transporte de explosivos ou gás tóxico (art. 253); Inundação e perigo de inundação (arts. 254 e 255); Desabamento ou desmoronamento (art. 256) e subtração, ocultação ou inutilização de material de salvamento (art. 257); Formas qualificadas pelo resultado lesão grave ou morte (art. 258); Difusão de doença ou praga (art. 259); Natureza de crime de perigo comum, concreto ou abstrato, e sujeito passivo coletivo
Não inclui: Atentados contra transportes, arremesso de projétil e interrupção de serviços de comunicação ou utilidade pública (arts. 260 a 266) → 5127; Crimes contra a saúde pública, como epidemia e envenenamento de água (arts. 267 a 285) → 5145; Posse, porte ou emprego de artefato explosivo ou incendiário regido pelo Estatuto do Desarmamento → 4697; Provocar incêndio em mata ou floresta (Lei 9.605/1998) → 4688; Dano qualificado pelo emprego de substância inflamável ou explosiva, sem perigo comum (art. 163, parágrafo único, II) → 5164; Homicídio qualificado pelo emprego de fogo ou explosivo (art. 121, §2º, III) → 5150
Âncoras legais: CP, arts. 250 a 259; CP, art. 258
Desempate: Escolha este nó quando o perigo coletivo vier de fogo, explosão, gás, água, desabamento ou praga (arts. 250 a 259); se o alvo for meio de transporte, comunicação ou serviço de utilidade pública, use 5127; se houver dolo de matar ou dano sem perigo coletivo, use o crime contra a pessoa ou o patrimônio.
```

### 5130 · amostral

```text
[5130] Penal > Dos Crimes Contra a Liberdade Pessoal > Ameaça e Perseguição
Escopo: Crimes de ameaça (CP, art. 147) e de perseguição/stalking (CP, art. 147-A): elementos do tipo, idoneidade da promessa de mal injusto e grave, reiteração da perseguição, causas de aumento, ação penal e consumação.
Inclui: Ameaça: promessa de mal injusto e grave por palavra, escrito, gesto ou meio simbólico; Ameaça como crime formal; ameaça em estado de ira ou embriaguez; Ameaça contra a mulher por razões da condição do sexo feminino: pena e ação penal; Perseguição (stalking): reiteração, ameaça à integridade física ou psicológica, invasão da esfera de liberdade ou privacidade; Causas de aumento da perseguição (criança, adolescente, idoso, mulher, concurso de agentes, emprego de arma); Ação penal pública condicionada à representação na ameaça e na perseguição
Não inclui: Constrangimento ilegal (CP, art. 146), que não tem subtema próprio → 5128; Violência psicológica contra a mulher (CP, art. 147-B) → 5131; Intimidação sistemática (bullying e cyberbullying) (CP, art. 146-A) → 5129; Grave ameaça como meio de execução da extorsão → 5161; Descumprimento de medida protetiva de urgência (Lei 11.340/2006, art. 24-A) → 4704
Âncoras legais: CP, art. 147; CP, art. 147-A
Desempate: Use este nó quando o núcleo for a promessa de mal grave (ameaça) ou a perseguição reiterada; se a conduta for dano emocional à mulher por humilhação, controle ou manipulação, use 5131; se for intimidação sistemática em grupo ou sem motivação evidente, use 5129.
```

### 5133 · amostral

```text
[5133] Penal > Dos Crimes Contra a Liberdade Pessoal > Dos Crimes contra a Inviolabilidade do Domicílio, Contra a Inviolabilidade da Correspondência e Contra a Inviolabilidade dos Segredos
Escopo: Crimes contra a inviolabilidade do domicílio, da correspondência e dos segredos (CP, arts. 150 a 154-B), incluindo violação de domicílio, violação de correspondência, divulgação de segredo, violação do segredo profissional e invasão de dispositivo informático.
Inclui: Violação de domicílio: conceito penal de casa, qualificadoras e hipóteses de exclusão do crime (flagrante delito, prisão ou diligência); Violação, sonegação ou destruição de correspondência e correspondência comercial; Divulgação de segredo contido em documento particular ou correspondência confidencial; Violação do segredo profissional (função, ministério, ofício ou profissão); Invasão de dispositivo informático (art. 154-A), qualificadoras e aumentos; Ação penal nos crimes de invasão de dispositivo informático (art. 154-B)
Não inclui: Busca e apreensão domiciliar como meio de prova no processo penal → 5554; Interceptação telefônica ilegal (Lei 9.296/1996) → 4700; Registro não autorizado da intimidade sexual (CP, art. 216-B) → 5107; Divulgação de cena de estupro, sexo ou nudez (CP, art. 218-C) → 5109; Violação de sigilo funcional por servidor público (CP, art. 325) → 5087; Prova obtida mediante violação de domicílio e sua ilicitude → 5594
Âncoras legais: CP, art. 150; CP, art. 151; CP, art. 152; CP, art. 153; CP, art. 154; CP, art. 154-A; CP, art. 154-B; CF, art. 5º, XI; CF, art. 5º, XII
Desempate: Use este nó quando a questão tratar da tipicidade penal da invasão de domicílio, correspondência, segredo ou dispositivo informático; se a questão discutir a validade da prova ou o procedimento da busca, use os nós de Processo Penal (5554 ou 5594).
```

### 5129 · amostral

```text
[5129] Penal > Dos Crimes Contra a Liberdade Pessoal > Intimidação Sistemática (Bullying)
Escopo: Crime de intimidação sistemática (bullying) e sua forma virtual (cyberbullying), previstos no CP, art. 146-A, incluído pela Lei 14.811/2024, e o conceito de bullying da Lei 13.185/2015.
Inclui: Tipo do art. 146-A: intimidação sistemática, individual ou em grupo, mediante violência física ou psicológica, de modo intencional e repetitivo, sem motivação evidente; Condutas: intimidação, humilhação, discriminação, ataques físicos, insultos, ações verbais, morais, sexuais, sociais, psicológicas ou virtuais; Cyberbullying: intimidação sistemática virtual pela internet, redes sociais, aplicativos ou jogos on-line (parágrafo único); Subsidiariedade da pena de multa (se a conduta não constituir crime mais grave); Conceito e classificação de bullying na Lei 13.185/2015 (Programa de Combate à Intimidação Sistemática)
Não inclui: Perseguição reiterada (stalking) (CP, art. 147-A) → 5130; Crimes do ECA e alterações da Lei 14.811/2024 no ECA e na Lei de Crimes Hediondos → 4709; Injúria isolada contra a vítima → 5124; Induzimento, instigação ou auxílio a suicídio ou automutilação (CP, art. 122) → 5152; Constrangimento ilegal (CP, art. 146) → 5128
Âncoras legais: CP, art. 146-A; Lei 13.185/2015; Lei 14.811/2024
Desempate: Use este nó quando a questão tratar de intimidação sistemática, repetitiva e sem motivação evidente (bullying/cyberbullying); se a conduta for perseguição dirigida que restringe a liberdade ou privacidade da vítima, use 5130.
```

### 5132 · amostral

```text
[5132] Penal > Dos Crimes Contra a Liberdade Pessoal > Sequestro, Cárcere Privado, Redução à Condição Análoga à de Escravo e Tráfico de Pessoas
Escopo: Crimes de sequestro e cárcere privado (CP, art. 148), redução à condição análoga à de escravo (CP, art. 149) e tráfico de pessoas (CP, art. 149-A): elementos, qualificadoras, causas de aumento e de diminuição, consumação e natureza permanente.
Inclui: Sequestro e cárcere privado: crime permanente e qualificadoras (vítima ascendente, descendente, cônjuge, idosa ou menor de 18 anos; internação fraudulenta; mais de 15 dias; fins libidinosos; grave sofrimento); Redução à condição análoga à de escravo: trabalhos forçados, jornada exaustiva, condições degradantes, restrição de locomoção por dívida; Figuras equiparadas do art. 149: cerceamento de transporte, vigilância ostensiva e retenção de documentos; Tráfico de pessoas: núcleos (agenciar, aliciar, recrutar, transportar etc.), meios e finalidades (remoção de órgãos, trabalho escravo, servidão, adoção ilegal, exploração sexual); Causas de aumento e minorante do tráfico de pessoas (agente primário que não integra organização criminosa); Lei 13.344/2016 (prevenção e repressão ao tráfico de pessoas)
Não inclui: Extorsão mediante sequestro e sequestro relâmpago (CP, arts. 158, § 3º, e 159) → 5161; Aliciamento de trabalhadores e frustração de direito trabalhista (CP, arts. 203, 206 e 207) → 5135; Competência da Justiça Federal para o crime de redução à condição análoga à de escravo → 5482; Sequestro de bens como medida assecuratória (CPP, arts. 125 a 133) → 5496; Subtração de incapazes (CP, art. 249) → 5115; Constrangimento ilegal (CP, art. 146) → 5128
Âncoras legais: CP, art. 148; CP, art. 149; CP, art. 149-A; Lei 13.344/2016
Desempate: Use este nó quando a privação da liberdade for o fim em si ou visar exploração (trabalho escravo, tráfico); se a privação da liberdade servir para obter vantagem econômica, use 5161.
```

### 5131 · amostral

```text
[5131] Penal > Dos Crimes Contra a Liberdade Pessoal > Violência Psicológica contra a Mulher
Escopo: Crime de violência psicológica contra a mulher (CP, art. 147-B, incluído pela Lei 14.188/2021): dano emocional causado mediante ameaça, constrangimento, humilhação, manipulação, isolamento, chantagem, ridicularização ou outro meio, e sua subsidiariedade expressa.
Inclui: Tipo do art. 147-B: causar dano emocional à mulher que a prejudique e perturbe seu pleno desenvolvimento ou vise degradar ou controlar suas ações, comportamentos, crenças e decisões; Meios executórios: ameaça, constrangimento, humilhação, manipulação, isolamento, chantagem, ridicularização, limitação do direito de ir e vir; Crime material (exige dano emocional) e sujeito passivo exclusivamente mulher; Subsidiariedade expressa (se a conduta não constitui crime mais grave); Inclusão pela Lei 14.188/2021 (Programa Sinal Vermelho)
Não inclui: Conceito de violência psicológica como forma de violência doméstica e medidas protetivas (Lei 11.340/2006) → 4704; Ameaça contra a mulher por razões da condição do sexo feminino (CP, art. 147) → 5130; Perseguição contra a mulher (CP, art. 147-A) → 5130; Lesão corporal contra a mulher por razões da condição do sexo feminino (CP, art. 129) → 5077; Feminicídio (CP, art. 121-A) → 5151
Âncoras legais: CP, art. 147-B; Lei 14.188/2021; Lei 11.340/2006, art. 7º, II
Desempate: Use este nó quando a questão tratar do tipo penal do art. 147-B do CP; se tratar das formas de violência, medidas protetivas ou procedimento da Lei Maria da Penha, use 4704; se o núcleo for promessa de mal grave ou perseguição, use 5130.
```

### 5141 · amostral

```text
[5141] Penal > Dos Crimes Contra a Periclitação da Vida e da Saúde > Abandono de Incapaz e Exposição ou Abandono de Recém-Nascido
Escopo: Crimes de abandono de incapaz (CP, art. 133) e de exposição ou abandono de recém-nascido para ocultar desonra própria (CP, art. 134), inclusive as formas qualificadas pelo resultado e as causas de aumento.
Inclui: Abandono de pessoa sob cuidado, guarda, vigilância ou autoridade, incapaz de se defender dos riscos; Crime próprio: exigência de vínculo de cuidado, guarda, vigilância ou autoridade entre o agente e a vítima; Formas qualificadas por lesão corporal grave ou morte (preterdolo); Aumento de pena: lugar ermo, agente ascendente, descendente, cônjuge, irmão, tutor ou curador, vítima maior de 60 anos; Exposição ou abandono de recém-nascido para ocultar desonra própria: tipo privilegiado e especial em relação ao art. 133; Distinção entre abandono com dolo de perigo e abandono com dolo de matar
Não inclui: Deixar de prestar assistência a criança abandonada ou extraviada encontrada por quem não tem dever de cuidado → 5142; Abandono material ou intelectual de filho e entrega de filho menor a pessoa inidônea (CP, arts. 244 a 246) → 5114; Abandono de idoso em hospitais, casas de saúde ou entidades de longa permanência (Lei 10.741/2003, art. 98) → 4696; Morte do próprio filho pela mãe, sob influência do estado puerperal → 5153; Dever de garante e crime omissivo impróprio em tese → 5223
Âncoras legais: CP, art. 133; CP, art. 134
Desempate: Escolha este nó quando o agente tem vínculo prévio de cuidado ou guarda com a vítima e a abandona. Se a omissão vem de qualquer pessoa sem esse vínculo diante de alguém em perigo, use 5142.
```

### 5143 · amostral

```text
[5143] Penal > Dos Crimes Contra a Periclitação da Vida e da Saúde > Maus-Tratos
Escopo: Crime de maus-tratos (CP, art. 136): expor a perigo a vida ou a saúde de pessoa sob autoridade, guarda ou vigilância, para fim de educação, ensino, tratamento ou custódia, com privação de alimentos ou de cuidados, trabalho excessivo ou abuso de meios de correção ou disciplina.
Inclui: Crime próprio: relação de autoridade, guarda ou vigilância com finalidade de educação, ensino, tratamento ou custódia; Condutas: privação de alimentação ou de cuidados indispensáveis, sujeição a trabalho excessivo ou inadequado, abuso de meios de correção ou disciplina; Formas qualificadas por lesão corporal grave ou morte; Aumento de pena quando a vítima é menor de 14 anos; Distinção entre maus-tratos (dolo de perigo, animus corrigendi) e tortura-castigo (intenso sofrimento físico ou mental)
Não inclui: Submeter pessoa sob guarda a intenso sofrimento físico ou mental como castigo (Lei 9.455/1997, art. 1º, II) → 4707; Maus-tratos a animais (Lei 9.605/1998, art. 32) → 4688; Expor a perigo a integridade e a saúde de idoso (Lei 10.741/2003, art. 99) → 4696; Crimes contra criança e adolescente previstos no ECA e na legislação especial → 4709; Lesão corporal dolosa contra descendente no âmbito doméstico (CP, art. 129, § 9º) → 5077
Âncoras legais: CP, art. 136
Desempate: Use este nó quando houver relação de autoridade, guarda ou vigilância com finalidade educativa, de tratamento ou custódia e abuso dos meios de correção. Se a vítima é idosa, use 4696. Se há intenso sofrimento infligido como castigo, use 4707.
```

### 5142 · amostral

```text
[5142] Penal > Dos Crimes Contra a Periclitação da Vida e da Saúde > Omissão de Socorro
Escopo: Crime de omissão de socorro (CP, art. 135) e de condicionamento de atendimento médico-hospitalar emergencial (CP, art. 135-A), inclusive as causas de aumento por lesão grave ou morte.
Inclui: Deixar de prestar assistência, sem risco pessoal, a criança abandonada ou extraviada, a pessoa inválida ou ferida, ao desamparo ou em grave e iminente perigo; Não pedir, nesses casos, o socorro da autoridade pública; Crime omissivo próprio, comum e instantâneo; dever genérico de solidariedade; Aumento de metade se resulta lesão grave e triplicação se resulta morte; Exigência de cheque-caução, nota promissória ou garantia, ou de formulários, como condição para atendimento emergencial (art. 135-A); Pluralidade de omitentes e socorro prestado por terceiro
Não inclui: Omissão de socorro pelo condutor de veículo envolvido em acidente (CTB, art. 304) → 4691; Omissão de socorro a pessoa idosa (Lei 10.741/2003, art. 97) → 4696; Aumento de pena no homicídio culposo por deixar de prestar imediato socorro à vítima (CP, art. 121, § 4º) → 5150; Omissão de quem tem dever de agir (garante), com responsabilização pelo resultado (CP, art. 13, § 2º) → 5223; Abandono de incapaz por quem tem o dever de cuidado ou guarda → 5141
Âncoras legais: CP, art. 135; CP, art. 135-A
Desempate: Escolha este nó para omissão de qualquer pessoa sem dever de garante. Se o omitente é condutor envolvido em acidente de trânsito, use 4691. Se a vítima é idosa, use 4696. Se o omitente é garante e responde pelo resultado, use 5223.
```

### 5139 · amostral

```text
[5139] Penal > Dos Crimes Contra a Periclitação da Vida e da Saúde > Perigo de Contágio Venéreo e de Moléstia Grave
Escopo: Crimes de perigo de contágio venéreo (CP, art. 130) e de perigo de contágio de moléstia grave (CP, art. 131), com suas formas qualificadas e a ação penal correspondente.
Inclui: Expor alguém a contágio de moléstia venérea por relações sexuais ou ato libidinoso, quando o agente sabe ou deve saber que está contaminado; Forma qualificada quando há intenção de transmitir a moléstia (CP, art. 130, § 1º); Ação penal pública condicionada à representação no art. 130 (§ 2º); Perigo de contágio de moléstia grave: ato capaz de produzir o contágio, praticado com o fim de transmitir a moléstia (crime formal); Concurso ou absorção quando o contágio efetivamente ocorre e produz lesão
Não inclui: Transmissão dolosa do HIV tratada como lesão corporal gravíssima (enfermidade incurável) → 5077; Causar epidemia ou infringir determinação do poder público destinada a impedir a propagação de doença contagiosa (CP, arts. 267 e 268) → 5145; Exposição genérica da vida ou da saúde de pessoa determinada a perigo direto e iminente → 5140; Estupro e demais crimes sexuais com aumento por transmissão de doença sexualmente transmissível → 5110
Âncoras legais: CP, art. 130; CP, art. 131
Desempate: Use este nó quando o perigo decorre do contágio de moléstia venérea ou grave a pessoa determinada. Se houve transmissão efetiva com lesão (por exemplo, HIV), use 5077. Se o risco é à coletividade, use 5145.
```

### 5140 · amostral

```text
[5140] Penal > Dos Crimes Contra a Periclitação da Vida e da Saúde > Perigo para a Vida ou a Saúde de Outrem
Escopo: Crime de perigo para a vida ou a saúde de outrem (CP, art. 132): expor pessoa determinada a perigo direto e iminente, com subsidiariedade expressa e causa de aumento no transporte irregular de trabalhadores.
Inclui: Perigo concreto, direto e iminente a pessoa certa e determinada; Crime expressamente subsidiário: só incide se o fato não constitui crime mais grave; Dolo de perigo, sem intenção de dano; Aumento de pena quando o perigo decorre do transporte de pessoas para a prestação de serviços em desacordo com as normas legais (parágrafo único); Distinção entre o tipo e a tentativa de homicídio ou de lesão corporal
Não inclui: Disparo de arma de fogo em lugar habitado ou em via pública (Lei 10.826/2003, art. 15) → 4697; Crimes de perigo comum contra número indeterminado de pessoas (incêndio, explosão etc.) → 5126; Perigo de contágio venéreo ou de moléstia grave → 5139; Direção perigosa, racha e demais crimes de perigo no trânsito (CTB) → 4691; Exposição a perigo de pessoa sob guarda mediante abuso dos meios de correção → 5143
Âncoras legais: CP, art. 132
Desempate: Use este nó para perigo concreto a pessoa determinada que não se enquadre em tipo de perigo mais específico. Se há contágio, use 5139. Se há relação de guarda e correção, use 5143. Se o perigo atinge a coletividade, use 5126. Se a conduta é disparo de arma, use 4697.
```

### 5154 · amostral

```text
[5154] Penal > Dos Crimes Contra a Vida > Aborto
Escopo: Crimes de aborto do CP: autoaborto e aborto consentido, aborto provocado por terceiro com ou sem consentimento, forma majorada pelo resultado e hipóteses legais e jurisprudenciais em que o aborto não é punido.
Inclui: Autoaborto e consentimento da gestante para o aborto (art. 124); Aborto provocado por terceiro sem consentimento (art. 125) e com consentimento (art. 126), inclusive consentimento inválido; Aumento de pena por lesão grave ou morte da gestante (art. 127); Aborto necessário e aborto em gravidez resultante de estupro (art. 128); Interrupção da gestação de feto anencéfalo (ADPF 54) e discussão sobre o aborto até o 3º mês (HC 124.306); Objeto material, início da proteção da vida intrauterina, consumação e tentativa
Não inclui: Lesão corporal gravíssima ou grave que resulta em aborto ou parto acelerado (art. 129, §§ 1º e 2º) → 5077; Morte do nascente ou recém-nascido pela mãe sob influência do estado puerperal → 5153; Feminicídio praticado contra mulher gestante (causa de aumento) → 5151; Rito do júri para julgamento do aborto → 5526; Anúncio de processo ou substância abortiva (contravenção penal) → 4686
Âncoras legais: CP, art. 124; CP, art. 125; CP, art. 126; CP, art. 127; CP, art. 128
Desempate: Escolha este nó quando a conduta tiver por fim interromper a gravidez e matar o feto; se o aborto for resultado não querido de uma agressão dolosa à gestante, use Lesões Corporais (5077).
```

### 5152 · amostral

```text
[5152] Penal > Dos Crimes Contra a Vida > Induzimento, Instigação ou Auxílio ao Suicídio
Escopo: Crime do art. 122 do CP, na redação da Lei 13.968/2019: induzir, instigar ou auxiliar alguém a suicidar-se ou a praticar automutilação, com formas qualificadas pelo resultado e causas de aumento.
Inclui: Condutas de induzimento, instigação e auxílio material ao suicídio ou à automutilação; Consumação como crime formal e qualificadoras por lesão grave/gravíssima ou morte (§§ 1º e 2º); Causas de aumento: motivo egoístico, torpe ou fútil, vítima menor ou com resistência diminuída, uso da internet ou rede social, líder de grupo; Desclassificação para lesão corporal gravíssima ou homicídio quando a vítima é menor de 14 anos ou não tem discernimento (§§ 6º e 7º); Pacto de morte, roleta-russa e distinção entre participação no suicídio e homicídio
Não inclui: Eutanásia e homicídio piedoso como forma privilegiada → 5150; Lesão corporal gravíssima em si (art. 129, § 2º) → 5077; Participação como forma de concurso de pessoas em tese → 5074; Intimidação sistemática (bullying) e cyberbullying → 5129
Âncoras legais: CP, art. 122; Lei 13.968/2019
Desempate: Escolha este nó quando a própria vítima executa o ato contra si e o agente apenas induz, instiga ou auxilia; se o agente pratica atos executórios da morte, ou a vítima é menor de 14 anos ou não tem discernimento (§ 7º), a questão vai para Homicídio (5150).
```

### 5167 · amostral

```text
[5167] Penal > Dos Crimes Contra o Patrimônio > Abuso de Incapazes
Escopo: Crime de abuso de incapazes (CP, art. 173): abusar da necessidade, paixão ou inexperiência de menor, ou da alienação ou debilidade mental de outrem, induzindo-o a praticar ato jurídico em prejuízo próprio ou de terceiro.
Inclui: Elementos do tipo do art. 173 do CP; Sujeito passivo: menor ou pessoa com alienação ou debilidade mental; Indução à prática de ato capaz de produzir efeito jurídico; Natureza formal: consumação com a prática do ato, independentemente do prejuízo efetivo; Diferença entre abuso de incapazes e estelionato (ausência de fraude)
Não inclui: Induzir pessoa idosa sem discernimento a outorgar procuração ou a doar bens (Estatuto do Idoso) → 4696; Obtenção de vantagem ilícita mediante artifício, ardil ou fraude → 5166; Induzimento à especulação (CP, art. 174) e demais fraudes do capítulo sem nó próprio → 5166
Âncoras legais: CP, art. 173
Desempate: Escolha este nó quando a vítima for menor ou pessoa com deficiência mental e o agente se aproveitar dessa condição para induzi-la a um ato jurídico prejudicial, sem uso de fraude; se houver engano por artifício ou ardil, escolha Estelionato (5166).
```

### 5165 · amostral

```text
[5165] Penal > Dos Crimes Contra o Patrimônio > Apropriação indébita
Escopo: Crimes de apropriação indébita do CP: apropriação indébita comum e majorada, apropriação indébita previdenciária, apropriação de coisa havida por erro, caso fortuito ou força da natureza, apropriação de tesouro e de coisa achada.
Inclui: Apropriação indébita (art. 168): posse ou detenção prévia lícita e inversão do ânimo; Causas de aumento do art. 168, § 1º (depositário necessário, tutor, curador, em razão de ofício ou profissão); Apropriação indébita previdenciária (art. 168-A) e extinção da punibilidade pelo pagamento; Apropriação de coisa havida por erro, caso fortuito ou força da natureza (art. 169); Apropriação de tesouro e de coisa achada (art. 169, parágrafo único); Forma privilegiada (art. 170 c/c art. 155, § 2º)
Não inclui: Apropriação de bem por funcionário público em razão do cargo (peculato) → 5089; Subtração de coisa alheia sem posse prévia → 5159; Sonegação fiscal e crimes contra a ordem tributária da Lei 8.137/1990 → 4695; Fraude anterior à obtenção da posse (dolo ab initio) → 5166
Âncoras legais: CP, art. 168; CP, art. 168-A; CP, art. 169; CP, art. 170
Desempate: Escolha este nó quando o agente já tinha a posse ou detenção lícita da coisa e só depois passou a agir como dono; se a fraude existia antes de obter a coisa, escolha Estelionato (5166); se o agente é funcionário público e a coisa estava com ele em razão do cargo, escolha Peculato (5089).
```

### 5164 · amostral

```text
[5164] Penal > Dos Crimes Contra o Patrimônio > Dano
Escopo: Crimes de dano do CP: dano simples e qualificado, introdução ou abandono de animais em propriedade alheia, dano em coisa de valor artístico, arqueológico ou histórico, alteração de local especialmente protegido e regras de ação penal do art. 167.
Inclui: Dano simples (art. 163, caput): destruir, inutilizar ou deteriorar coisa alheia; Dano qualificado (art. 163, parágrafo único): violência ou grave ameaça, substância inflamável ou explosiva, patrimônio público, motivo egoístico ou prejuízo considerável; Dano a patrimônio público, inclusive de concessionárias e de sociedades de economia mista; Introdução ou abandono de animais em propriedade alheia (art. 164); Ação penal privada no dano simples e no dano por motivo egoístico (art. 167); Dano praticado por preso para fugir e a exigência de dolo específico
Não inclui: Pichação e dano a bem especialmente protegido previstos na Lei 9.605/1998 → 4688; Destruição de bens para fraudar execução → 5168; Incêndio e explosão como crimes de perigo comum → 5126; Destruição de coisa própria para receber indenização de seguro (art. 171, § 2º, V) → 5166
Âncoras legais: CP, art. 163; CP, art. 164; CP, art. 165; CP, art. 166; CP, art. 167
```

### 5158 · amostral

```text
[5158] Penal > Dos Crimes Contra o Patrimônio > Disposições Gerais dos Crimes Contra o Patrimônio
Escopo: Disposições gerais do Título II do CP: imunidades penais absolutas e relativas nos crimes contra o patrimônio e as hipóteses em que não se aplicam.
Inclui: Imunidade absoluta (escusa absolutória) do art. 181: cônjuge na constância da sociedade conjugal, ascendente e descendente; Imunidade relativa do art. 182: ação condicionada à representação (cônjuge separado, irmão, tio ou sobrinho com quem o agente coabita); Exceções do art. 183: roubo ou extorsão, violência ou grave ameaça, estranho que participa do crime, vítima com 60 anos ou mais; Extensão das imunidades ao companheiro em união estável; Incomunicabilidade da imunidade ao coautor ou partícipe estranho
Não inclui: Regras gerais da ação penal pública condicionada no CP → 5064; Representação como condição de procedibilidade no processo penal → 5471; Requisito de representação próprio do estelionato (art. 171, § 5º) → 5166; Crimes patrimoniais contra a pessoa idosa previstos no Estatuto do Idoso → 4696
Âncoras legais: CP, art. 181; CP, art. 182; CP, art. 183
Desempate: Escolha este nó quando a questão tratar das imunidades dos arts. 181 a 183, qualquer que seja o crime patrimonial; se a questão tratar só dos elementos de um crime específico, escolha o nó desse crime.
```

### 5162 · amostral

```text
[5162] Penal > Dos Crimes Contra o Patrimônio > Esbulho Possessório
Escopo: Crime de esbulho possessório (CP, art. 161, § 1º, II): invadir, com violência a pessoa, grave ameaça ou concurso de mais de duas pessoas, terreno ou edifício alheio para fins de esbulho.
Inclui: Elementos do tipo: invasão de terreno ou edifício alheio com fim de esbulho; Meios executórios: violência a pessoa, grave ameaça ou concurso de mais de duas pessoas; Concurso material com a pena da violência (art. 161, § 2º); Ação penal privada quando a propriedade é particular e não há violência (art. 161, § 3º); Elemento subjetivo específico (intenção de ocupar o imóvel)
Não inclui: Alteração de limites e usurpação de águas (art. 161, caput e § 1º, I) → 5163; Supressão ou alteração de marca em animais (art. 162) → 5163; Entrada ou permanência em casa alheia sem fim de esbulho (violação de domicílio) → 5133; Fazer justiça pelas próprias mãos para retomar posse que se julga devida → 5082
Âncoras legais: CP, art. 161, § 1º, II; CP, art. 161, §§ 2º e 3º
Desempate: Escolha este nó quando a questão tratar da invasão de imóvel alheio com fim de esbulho (art. 161, § 1º, II); para as demais figuras dos arts. 161 e 162, escolha Usurpação (5163).
```

### 5166 · amostral

```text
[5166] Penal > Dos Crimes Contra o Patrimônio > Estelionato
Escopo: Estelionato (CP, art. 171) e suas formas equiparadas, majoradas e qualificadas, além das demais fraudes do Capítulo VI sem nó próprio (arts. 171-A, 172, 174 a 178); abuso de incapazes e fraude à execução têm nós próprios.
Inclui: Estelionato simples: artifício, ardil ou fraude, erro da vítima, vantagem ilícita e prejuízo alheio; Figuras equiparadas do art. 171, § 2º, incluindo fraude no pagamento por cheque (Súmulas 246 e 554 do STF); Fraude eletrônica (art. 171, § 2º-A) e estelionato contra idoso ou vulnerável (§ 4º); Ação penal condicionada à representação e suas exceções (art. 171, § 5º); Estelionato privilegiado e majorado contra entidade de direito público (§§ 1º e 3º); Relação com o falso: Súmula 17 do STJ (absorção); Fraude com ativos virtuais (art. 171-A) e duplicata simulada (art. 172); Distinção entre estelionato e furto mediante fraude
Não inclui: Fraude usada para diminuir a vigilância e subtrair a coisa (furto mediante fraude) → 5159; Abuso de incapazes (art. 173) → 5167; Fraude à execução (art. 179) → 5168; Falsificação e uso de documento falso como crimes autônomos → 5118; Fraudes contra o sistema financeiro e crimes contra as relações de consumo → 4689
Âncoras legais: CP, art. 171; CP, art. 171-A; CP, art. 172; CP, arts. 174 a 178
Desempate: Escolha este nó quando a vítima, enganada, entregar voluntariamente a coisa ou vantagem; se a fraude só servir para facilitar a subtração sem entrega voluntária, escolha Furto (5159).
```

### 5161 · amostral

```text
[5161] Penal > Dos Crimes Contra o Patrimônio > Extorsão
Escopo: Crimes de extorsão do CP: extorsão comum, majorada e qualificada, sequestro relâmpago (art. 158, § 3º), extorsão mediante sequestro e suas qualificadoras e delação premiada (art. 159), e extorsão indireta (art. 160).
Inclui: Extorsão (art. 158): constranger mediante violência ou grave ameaça a fazer, tolerar ou deixar de fazer algo para obter vantagem econômica; Natureza formal: Súmula 96 do STJ; Sequestro relâmpago: restrição da liberdade da vítima como condição necessária para obter a vantagem (art. 158, § 3º); Extorsão mediante sequestro, qualificadoras e delação premiada (art. 159, § 4º); Extorsão indireta (art. 160); Distinção entre extorsão e roubo (necessidade de colaboração da vítima)
Não inclui: Subtração com violência ou grave ameaça em que a colaboração da vítima é dispensável → 5160; Privação de liberdade sem fim de vantagem econômica (sequestro e cárcere privado) → 5132; Exigência de vantagem indevida por funcionário público em razão da função (concussão) → 5091; Cobrança violenta de dívida legítima (exercício arbitrário das próprias razões) → 5082; Caráter hediondo da extorsão qualificada e da extorsão mediante sequestro (Lei 8.072/1990) → 4693
Âncoras legais: CP, art. 158; CP, art. 159; CP, art. 160
Desempate: Escolha este nó quando a vantagem depender de comportamento da vítima; se o agente puder obter a coisa por si mesmo, subtraindo-a, escolha Roubo (5160).
```

### 5168 · amostral

```text
[5168] Penal > Dos Crimes Contra o Patrimônio > Fraude à Execução
Escopo: Crime de fraude à execução (CP, art. 179): fraudar execução alienando, desviando, destruindo ou danificando bens, ou simulando dívidas, com ação penal privada.
Inclui: Elementos do tipo do art. 179; Pressuposto de existência de ação de execução ou processo em curso; Condutas: alienar, desviar, destruir, danificar bens ou simular dívidas; Ação penal privada (art. 179, parágrafo único); Distinção entre fraude à execução penal e instituto processual civil
Não inclui: Estelionato e demais fraudes do Capítulo VI → 5166; Dano a coisa alheia sem finalidade de frustrar execução → 5164; Inovação artificiosa em processo para induzir juiz ou perito a erro (fraude processual) → 5083; Regras gerais da ação penal privada no CP → 5065
Âncoras legais: CP, art. 179
Desempate: Escolha este nó quando a fraude visar frustrar execução, alienando ou ocultando bens ou simulando dívidas; se a fraude alterar o estado de lugar, coisa ou pessoa para enganar o juiz, escolha Fraude Processual (5083).
```

### 5159 · amostral

```text
[5159] Penal > Dos Crimes Contra o Patrimônio > Furto
Escopo: Crimes de furto do CP: furto simples, noturno, privilegiado e qualificado, furto de energia, furto mediante fraude e eletrônico, furto de veículo transportado e de semovente, e furto de coisa comum.
Inclui: Furto simples (art. 155): subtração de coisa alheia móvel sem violência ou grave ameaça; Consumação: teoria da amotio/apprehensio (Súmula 582 do STJ); Furto noturno (§ 1º) e privilegiado (§ 2º), inclusive o privilégio combinado com qualificadora (Súmula 511 do STJ); Qualificadoras do § 4º (rompimento de obstáculo, abuso de confiança, fraude, escalada, destreza, chave falsa, concurso de pessoas); Furto com explosivo, fraude eletrônica, veículo levado para outro estado e semovente (§§ 4º-A a 7º); Equiparação da energia elétrica a coisa móvel (§ 3º); Furto de coisa comum (art. 156); Princípio da insignificância aplicado ao furto
Não inclui: Subtração com violência ou grave ameaça, inclusive empregada depois da subtração (roubo impróprio) → 5160; Entrega voluntária da coisa pela vítima enganada → 5166; Subtração por funcionário público valendo-se do cargo (peculato-furto) → 5089; Imunidade de quem furta de ascendente, descendente ou cônjuge → 5158; Princípio da insignificância como princípio geral do Direito Penal → 5172
Âncoras legais: CP, art. 155; CP, art. 156
Desempate: Escolha este nó quando houver subtração sem violência ou grave ameaça a pessoa; se a fraude levar a vítima a entregar a coisa, escolha Estelionato (5166).
```

### 5160 · amostral

```text
[5160] Penal > Dos Crimes Contra o Patrimônio > Roubo
Escopo: Crime de roubo (CP, art. 157): roubo próprio e impróprio, causas de aumento, emprego de arma, e roubo qualificado pela lesão grave ou pela morte (latrocínio).
Inclui: Roubo próprio (caput) e impróprio (§ 1º): violência ou grave ameaça antes ou depois da subtração; Consumação do roubo: Súmula 582 do STJ; Majorantes do § 2º (concurso de pessoas, restrição de liberdade da vítima, transporte de valores etc.); Emprego de arma de fogo e de arma de uso restrito ou proibido (§§ 2º-A e 2º-B); Latrocínio e roubo qualificado pela lesão grave (§ 3º); Súmula 610 do STF; Inaplicabilidade do princípio da insignificância ao roubo
Não inclui: Vantagem que depende de colaboração da vítima, inclusive sequestro relâmpago → 5161; Subtração sem violência ou grave ameaça → 5159; Caráter hediondo do latrocínio e do roubo majorado (Lei 8.072/1990) → 4693; Competência do júri ou do juiz singular para o latrocínio (Súmula 603 do STF) → 5482
Âncoras legais: CP, art. 157
Desempate: Escolha este nó quando o agente subtrair a coisa com violência ou grave ameaça sem depender de ato da vítima; se a vantagem exigir colaboração da vítima, escolha Extorsão (5161).
```

### 5137 · amostral

```text
[5137] Penal > Dos Crimes contra a Organização do Trabalho, a Propriedade Imaterial e ao Sentimento Religioso > Dos Crimes Contra o Sentimento Religioso e Respeito aos Mortos
Escopo: Crimes do Título V da Parte Especial do CP: ultraje a culto e impedimento ou perturbação de ato religioso (art. 208) e crimes contra o respeito aos mortos (arts. 209 a 212).
Inclui: Escárnio público de alguém por motivo de crença ou função religiosa (art. 208); Impedimento ou perturbação de cerimônia ou prática de culto religioso e vilipêndio público de ato ou objeto de culto (art. 208); Impedimento ou perturbação de enterro ou cerimônia funerária (art. 209); Violação de sepultura ou urna funerária (art. 210); Destruição, subtração ou ocultação de cadáver ou parte dele (art. 211); Vilipêndio a cadáver ou a suas cinzas (art. 212); Aumento de pena pelo emprego de violência no art. 208 (parágrafo único)
Não inclui: Injúria qualificada por elementos referentes a religião (CP, art. 140, § 3º) → 5124; Praticar, induzir ou incitar discriminação ou preconceito religioso (Lei 7.716/1989, art. 20) → 4690; Concurso entre homicídio e ocultação de cadáver para fins de soma de penas → 5067; Homicídio da vítima cujo cadáver é depois ocultado (tipificação do crime contra a vida) → 5150; Fraude processual pela alteração do local do crime para enganar o juiz ou perito (CP, art. 347) → 5083
Âncoras legais: CP, art. 208; CP, arts. 209 a 212
Desempate: Use este nó quando o bem jurídico for o sentimento religioso ou o respeito aos mortos (arts. 208 a 212); se a ofensa for dirigida à honra de pessoa específica com referência à religião, use o 5124; se houver discriminação religiosa prevista na Lei 7.716/1989, use o 4690.
```

### 5174 · amostral

```text
[5174] Penal > Introdução ao Estudo do Direito Penal > Classificações dos Crimes
Escopo: Classificação doutrinária das infrações penais: crime e contravenção, crimes comuns, próprios e de mão própria, materiais, formais e de mera conduta, de dano e de perigo, instantâneos e permanentes, unissubjetivos e plurissubjetivos, entre outras.
Inclui: Crime comum, próprio e de mão própria; Crime material, formal e de mera conduta; Crime de dano e de perigo (concreto e abstrato); Crime instantâneo, permanente e instantâneo de efeitos permanentes; Crime unissubjetivo e plurissubjetivo; unissubsistente e plurissubsistente; Crime simples, qualificado e privilegiado; crime vago, habitual, complexo; Distinção entre crime e contravenção (sistema dicotômico)
Não inclui: Crimes omissivos próprios e impróprios e o dever de agir → 5223; Crime doloso e culposo, preterdolo → 5222; Consumação e tentativa conforme a classificação do crime → 5177; Regime jurídico das contravenções penais (Decreto-Lei 3.688/1941) → 4686; Rol e regime dos crimes hediondos → 4693; Sujeito ativo, sujeito passivo e objeto do crime → 5219
Âncoras legais: Decreto-Lei 3.914/1941, art. 1º
Desempate: Use este nó quando a questão pede rotular ou distinguir categorias doutrinárias de crimes; se tratar do regime jurídico de um instituto (omissão, dolo/culpa, tentativa), use o nó específico da teoria do crime.
```

### 5177 · amostral

```text
[5177] Penal > Iter Criminis > Crime Consumado e Tentado
Escopo: Crime consumado e tentado (CP, art. 14): quando o crime se consuma, requisitos da tentativa (início da execução e não consumação por circunstâncias alheias à vontade do agente), espécies de tentativa, redução de pena e crimes que não admitem tentativa.
Inclui: Conceito de crime consumado: reúne todos os elementos da definição legal; Requisitos da tentativa: início da execução e não consumação por circunstâncias alheias à vontade do agente; Tentativa perfeita (acabada) e imperfeita (inacabada), branca (incruenta) e cruenta; Redução de 1/3 a 2/3 conforme a proximidade da consumação (art. 14, parágrafo único); Infrações que não admitem tentativa: culposos, preterdolosos, contravenções, omissivos próprios, habituais, unissubsistentes; Teoria objetiva (temperada) adotada para punir a tentativa e exceções (crimes de atentado ou de empreendimento); Tentativa com dolo eventual e tentativa no crime complexo (latrocínio tentado e consumado, Súmula 610 STF)
Não inclui: Interrupção da execução por vontade do próprio agente (tentativa abandonada ou qualificada) → 5178; Ineficácia absoluta do meio ou impropriedade absoluta do objeto (tentativa inidônea) → 5179; Distinção entre atos preparatórios e atos executórios; cogitação e exaurimento → 5176; Classificação de crimes materiais, formais e de mera conduta em si → 5174; Momento consumativo do roubo (inversão da posse, Súmula 582 STJ) estudado como elemento do próprio tipo → 5160; Momento consumativo do furto (teoria da amotio/apprehensio) estudado como elemento do próprio tipo → 5159
Âncoras legais: CP, art. 14; Súmula 610 do STF
Desempate: Escolha este nó quando a falha na consumação decorre de circunstâncias alheias à vontade do agente e o meio/objeto era ao menos relativamente idôneo; se o agente parou ou evitou o resultado voluntariamente, use 5178; se o meio ou objeto era absolutamente inidôneo, use 5179.
```

### 5179 · amostral

```text
[5179] Penal > Iter Criminis > Crime Impossível
Escopo: Crime impossível (tentativa inidônea ou quase crime, CP, art. 17): impunibilidade da tentativa por ineficácia absoluta do meio ou absoluta impropriedade do objeto, teoria objetiva temperada adotada e hipóteses jurisprudenciais correlatas.
Inclui: Ineficácia absoluta do meio e absoluta impropriedade do objeto; Teorias sintomática, subjetiva, objetiva pura e objetiva temperada (adotada pelo CP); Distinção entre inidoneidade absoluta (crime impossível) e relativa (tentativa punível); Flagrante preparado ou provocado como crime impossível (Súmula 145 STF); Sistema de vigilância ou monitoramento eletrônico em estabelecimento comercial não torna impossível o furto (Súmula 567 STJ); Natureza jurídica: causa de exclusão da tipicidade da tentativa
Não inclui: Tentativa punível com meio ou objeto relativamente inidôneo → 5177; Validade e espécies de prisão em flagrante (esperado, forjado, prorrogado) como medida processual → 5518; Delito putativo por erro de tipo e erro sobre elementar do tipo → 5224; Delito putativo por erro de proibição (agente supõe proibida conduta lícita) e erro sobre a ilicitude → 5214; Interrupção voluntária da execução pelo agente → 5178
Âncoras legais: CP, art. 17; Súmula 145 do STF; Súmula 567 do STJ
Desempate: Escolha este nó quando a consumação era impossível desde o início por inidoneidade absoluta do meio ou do objeto (ou por flagrante preparado); se a inidoneidade é relativa ou a consumação falhou por fator externo superveniente, use 5177; se a questão trata da legalidade da prisão em flagrante, use 5518.
```

### 5178 · amostral

```text
[5178] Penal > Iter Criminis > Desistência Voluntária, Arrependimento Eficaz e Arrependimento posterior
Escopo: Desistência voluntária e arrependimento eficaz (CP, art. 15), que fazem o agente responder só pelos atos já praticados, e arrependimento posterior (CP, art. 16), causa de diminuição de pena pela reparação do dano ou restituição da coisa até o recebimento da denúncia ou queixa.
Inclui: Desistência voluntária: agente interrompe a execução quando podia prosseguir (Fórmula de Frank); Arrependimento eficaz: agente esgota os atos executórios e impede o resultado; Voluntariedade x espontaneidade; resposta apenas pelos atos já praticados; Natureza jurídica: tentativa abandonada/qualificada (exclusão da tipicidade ou causa de extinção da punibilidade, conforme a corrente); Arrependimento posterior: crime sem violência ou grave ameaça à pessoa, reparação ou restituição voluntária até o recebimento da denúncia ou queixa, redução de 1/3 a 2/3; Comunicabilidade do arrependimento posterior aos coautores e arrependimento ineficaz
Não inclui: Reparação do dano após o recebimento da denúncia como atenuante genérica (CP, art. 65, III, b) → 5203; Reparação do dano no peculato culposo antes ou depois da sentença irrecorrível (CP, art. 312, §§ 2º e 3º) → 5089; Não consumação por circunstâncias alheias à vontade do agente → 5177; Colaboração premiada como meio de obtenção de prova → 5557; Pagamento do tributo e extinção da punibilidade nos crimes tributários → 4695
Âncoras legais: CP, art. 15; CP, art. 16
Desempate: Escolha este nó quando a não consumação ou a reparação decorre de ato voluntário do próprio agente; se a reparação ocorre após o recebimento da denúncia, use 5203; se o crime não se consumou por fator alheio à vontade do agente, use 5177.
```

### 5176 · amostral

```text
[5176] Penal > Iter Criminis > Fases do Iter Criminis
Escopo: Fases do iter criminis (cogitação, preparação, execução, consumação e exaurimento), sua relevância penal e critérios para distinguir atos preparatórios de atos executórios.
Inclui: Etapas: cogitação, atos preparatórios, atos executórios, consumação e exaurimento; Impunibilidade da cogitação e, em regra, dos atos preparatórios; Atos preparatórios tipificados como crimes autônomos (crimes-obstáculo, ex.: associação criminosa, petrechos para falsificação de moeda); Critérios de distinção preparação/execução: objetivo-formal, objetivo-material, objetivo-individual (Zaffaroni), hostilidade ao bem jurídico; Exaurimento: fase pós-consumativa e reflexo na dosimetria
Não inclui: Requisitos, espécies e pena da tentativa; crimes que não admitem tentativa → 5177; Classificação dos crimes em materiais, formais e de mera conduta → 5174; Impunibilidade do ajuste, determinação, instigação e auxílio quando o crime não chega a ser tentado (CP, art. 31) → 5074; Punição de atos preparatórios de terrorismo (Lei 13.260/2016, art. 5º) → 4706
Âncoras legais: CP, art. 14, II; CP, art. 288; CP, art. 291
Desempate: Escolha este nó quando a questão versar sobre a sequência de etapas do crime ou sobre a fronteira entre preparação e execução; se já houve início da execução e o foco é a punição da tentativa, use 5177.
```

### 5180 · amostral

```text
[5180] Penal > Lei Penal no Tempo e no Espaço
Escopo: Aplicação da lei penal (CP, arts. 1º a 12): lei penal no tempo, lei penal no espaço e conflito aparente de normas. Cada parte tem subtema próprio.
Inclui: Tempo do crime (teoria da atividade) e retroatividade da lei benéfica; Lei excepcional e temporária; novatio legis in pejus e in mellius; Lugar do crime (ubiquidade), territorialidade e extraterritorialidade; Pena cumprida no estrangeiro, eficácia de sentença estrangeira e contagem de prazo (arts. 8º a 10); Conflito aparente de normas: especialidade, subsidiariedade, consunção e alternatividade
Não inclui: Abolitio criminis como causa extintiva da punibilidade → 5194; Lei processual penal no tempo (tempus regit actum) → 5507; Competência territorial (lugar da infração no CPP) → 5483; Princípio da legalidade e anterioridade em si → 5172; Concurso formal e material de crimes → 5066
Âncoras legais: CP, arts. 1º a 12
Desempate: Use este nó só quando a questão abordar conjuntamente tempo, espaço e/ou conflito de normas; questões focadas em um deles vão para 5181, 5182 ou 5183.
```

### 5183 · amostral

```text
[5183] Penal > Lei Penal no Tempo e no Espaço > Conflito Aparente de Normas
Escopo: Conflito aparente de normas penais: situações em que um único fato parece se enquadrar em mais de um tipo penal, resolvidas pelos princípios da especialidade, subsidiariedade, consunção e alternatividade, para evitar o bis in idem.
Inclui: Requisitos do conflito aparente: unidade de fato e pluralidade de normas aparentemente aplicáveis; Princípio da especialidade (ex.: infanticídio x homicídio); Princípio da subsidiariedade expressa e tácita (soldado de reserva); Princípio da consunção: crime-meio, crime progressivo, progressão criminosa, antefato e pós-fato impuníveis; Princípio da alternatividade nos tipos mistos alternativos; Súmula 17 do STJ (falso exaurido no estelionato); Distinção entre conflito aparente de normas e concurso de crimes
Não inclui: Concurso formal ou material quando há efetiva pluralidade de crimes → 5066; Sucessão de leis penais no tempo e retroatividade benéfica → 5181; Classificação de crimes progressivos, complexos ou de tipo misto como tema classificatório → 5174; Princípio do ne bis in idem tratado como princípio geral do Direito Penal → 5172
Âncoras legais: CP, art. 12
Desempate: Escolha este nó quando a questão perguntar qual norma prevalece sobre um único fato (especialidade, subsidiariedade, consunção, alternatividade); se houver pluralidade real de crimes e a discussão for a soma ou exasperação das penas, use Concurso de Crimes (5066).
```

### 5184 · amostral

```text
[5184] Penal > Medida de Segurança
Escopo: Medida de segurança no Código Penal: pressupostos, espécies (internação e tratamento ambulatorial), prazo, perícia de cessação de periculosidade, desinternação e substituição da pena do semi-imputável.
Inclui: Espécies: internação em hospital de custódia e tratamento ambulatorial (CP, art. 96); Pressupostos: fato típico e ilícito, periculosidade e inimputabilidade/semi-imputabilidade; Prazo mínimo, perícia médica e desinternação ou liberação condicional (CP, art. 97); Substituição da pena por medida de segurança para o semi-imputável (CP, art. 98); Limite máximo de duração (Súmula 527 do STJ); Sistema vicariante e extinção da punibilidade na medida de segurança
Não inclui: Critério biopsicológico e hipóteses de inimputabilidade (CP, arts. 26 a 28) → 5213; Incidente de insanidade mental (CPP, arts. 149 a 154) → 5497; Execução da medida de segurança na LEP (arts. 171 a 179) → 4703; Sentença absolutória imprópria (CPP, art. 386, parágrafo único, III) → 5574
Âncoras legais: CP, arts. 96 a 99; Súmula 527 do STJ
Desempate: Escolha este nó quando a questão tratar da sanção aplicada ao inimputável/semi-imputável (espécie, prazo, cessação); se tratar de como se afere a inimputabilidade, use 5213.
```

### 5185 · amostral

```text
[5185] Penal > Prescrição
Escopo: Extinção da punibilidade pelo decurso do tempo (CP, arts. 109 a 119): fundamentos, prazos, pretensão punitiva (abstrata, retroativa, intercorrente), pretensão executória, causas suspensivas e interruptivas e prescrições especiais. Cada parte tem subtema próprio.
Inclui: Fundamentos e natureza jurídica da prescrição; Tabela de prazos do art. 109 e redução pela metade do art. 115; Prescrição da pretensão punitiva em abstrato, retroativa e intercorrente; Prescrição da pretensão executória e termo inicial (art. 112); Causas impeditivas/suspensivas (art. 116) e interruptivas (art. 117); Termo inicial em crimes permanentes e tentados (art. 111); Prescrição da multa, no concurso de crimes (art. 119) e imprescritibilidade constitucional
Não inclui: Decadência do direito de queixa ou representação → 5198; Perempção na ação penal privada → 5195; Rol geral das causas extintivas da punibilidade (CP, art. 107) → 5191; Crime continuado e aumento de pena (exceto efeito na prescrição) → 5069; Prescrição do porte de drogas para consumo (Lei 11.343/2006, art. 30) → 4708
Âncoras legais: CP, arts. 109 a 119; CF, art. 5º, XLII e XLIV; Súmula 146 do STF; Súmula 438 do STJ
Desempate: Use este nó quando a questão tratar de prescrição de forma ampla, sem foco em uma espécie ou em contagem/causas suspensivas; se for decadência ou outra causa do art. 107, vá ao subtema de 5191.
```

### 5191 · amostral

```text
[5191] Penal > Punibilidade
Escopo: Punibilidade e suas causas extintivas (CP, art. 107 e legislação esparsa): morte do agente, anistia, graça e indulto, abolitio criminis, decadência, perempção, renúncia, perdão, retratação e perdão judicial. Condições objetivas de punibilidade não têm subtema próprio. Prescrição tem nó próprio (5185).
Inclui: Conceito de punibilidade e natureza das causas extintivas; Rol do art. 107 do CP (caráter exemplificativo); Condições objetivas de punibilidade e escusas absolutórias (noção geral); Comunicabilidade da extinção da punibilidade (art. 108); Visão comparativa entre as causas extintivas
Não inclui: Prescrição da pretensão punitiva e executória → 5185; Escusas absolutórias dos crimes patrimoniais (CP, arts. 181 a 183) → 5158; Extinção da punibilidade pelo pagamento do tributo → 4695; Representação como condição de procedibilidade (CPP) → 5471; Reparação do dano no peculato culposo → 5089
Âncoras legais: CP, art. 107; CP, art. 108
Desempate: Use este nó quando a questão tratar do conceito de punibilidade ou comparar várias causas extintivas; se focar em uma só causa, use o subtema (5192 a 5198) ou 5185 para prescrição.
```

### 5194 · amostral

```text
[5194] Penal > Punibilidade > Abolitio Criminis
Escopo: Abolitio criminis como causa de extinção da punibilidade: lei posterior que deixa de considerar o fato crime, com cessação da execução e dos efeitos penais da sentença condenatória, mantidos os efeitos extrapenais.
Inclui: Conceito de abolitio criminis e sua natureza de lei penal supressiva da incriminação; Extinção da punibilidade pela lei que deixa de considerar o fato crime (CP, art. 107, III); Cessação da execução e dos efeitos penais da condenação, inclusive após o trânsito em julgado; Subsistência dos efeitos extrapenais (ex.: obrigação de reparar o dano); Distinção entre abolitio criminis e princípio da continuidade normativo-típica; Abolitio criminis temporária (ex.: vacatio de prazos para entrega de armas); Competência do juízo da execução para aplicá-la após o trânsito em julgado
Não inclui: Novatio legis in mellius, novatio legis in pejus, ultratividade e leis temporárias/excepcionais → 5181; Anistia como esquecimento jurídico do fato por lei do Congresso → 5193; Lei processual penal no tempo (tempus regit actum) → 5507; Regras específicas do Estatuto do Desarmamento sobre posse e entrega de armas → 4697
Âncoras legais: CP, art. 2º; CP, art. 107, III; LEP, art. 66, I
Desempate: Use este nó quando a questão tratar da supressão da figura típica e de seus efeitos sobre a punibilidade; se discutir a sucessão de leis penais em geral (retroatividade da lei mais benéfica, lei mais gravosa, leis temporárias), use 5181.
```

### 5193 · amostral

```text
[5193] Penal > Punibilidade > Anistia, Graça e Indulto
Escopo: Anistia, graça e indulto como causas de extinção da punibilidade por indulgência estatal: conceito, competência, espécies, alcance, efeitos e vedações constitucionais e legais.
Inclui: Anistia: lei do Congresso Nacional, efeitos retroativos, espécies (própria/imprópria, geral/parcial, condicionada/incondicionada); Graça (indulto individual) e indulto coletivo concedidos por decreto do Presidente da República; Delegação do indulto a Ministros, PGR e AGU; Comutação de pena como indulto parcial; Indulto extingue efeitos primários da condenação, mas não os secundários (Súmula 631 STJ); Vedação de graça e anistia para tortura, tráfico de drogas, terrorismo e crimes hediondos, e de indulto pela Lei 8.072/90
Não inclui: Abolitio criminis por lei que deixa de considerar o fato crime → 5194; Perdão judicial concedido pelo juiz na sentença → 5197; Perdão do ofendido na ação penal privada → 5196; Regime e vedações gerais da Lei dos Crimes Hediondos (progressão, liberdade provisória etc.) → 4693; Procedimento de concessão de indulto e comutação na execução penal → 4703
Âncoras legais: CP, art. 107, II; CF, art. 5º, XLIII; CF, art. 21, XVII; CF, art. 48, VIII; CF, art. 84, XII; Lei 8.072/1990, art. 2º, I; LEP, arts. 187 a 193
Desempate: Escolha este nó quando a extinção decorrer de clemência do Legislativo (anistia) ou do Executivo (graça/indulto); se o foco for o rito de processamento na execução penal, use 4703.
```

### 5192 · amostral

```text
[5192] Penal > Punibilidade > Morte do agente
Escopo: Morte do agente como causa de extinção da punibilidade: fundamento na intranscendência da pena, prova por certidão de óbito e consequências sobre a pena e os efeitos da condenação.
Inclui: Extinção da punibilidade pela morte do agente (CP, art. 107, I); Princípio da personalidade ou intranscendência da pena (CF, art. 5º, XLV); Exigência de certidão de óbito e oitiva do Ministério Público (CPP, art. 62); Certidão de óbito falsa: possibilidade de revogação da decisão extintiva segundo o STF; Pena de multa não se transmite aos herdeiros; Comunicabilidade: a morte de um coautor não extingue a punibilidade dos demais
Não inclui: Morte do ofendido e sucessão processual na ação penal privada → 5472; Perempção por falta de sucessão após a morte do querelante → 5195; Obrigação de reparar o dano transmitida aos herdeiros e ação civil ex delicto → 5475; Execução da pena de multa → 5206
Âncoras legais: CP, art. 107, I; CF, art. 5º, XLV; CPP, art. 62
Desempate: Use este nó quando quem morre é o autor do fato; se morre o ofendido ou o querelante, use 5472 ou 5195.
```

### 5197 · amostral

```text
[5197] Penal > Punibilidade > Perdão Judicial
Escopo: Perdão judicial como causa de extinção da punibilidade: faculdade do juiz de deixar de aplicar a pena nos casos expressos em lei, sua natureza jurídica, hipóteses legais e efeitos da sentença concessiva.
Inclui: Perdão judicial só nos casos previstos em lei (CP, art. 107, IX); Homicídio e lesão corporal culposos quando as consequências atingem gravemente o agente (CP, art. 121, §5º; art. 129, §8º); Natureza declaratória da sentença concessiva (Súmula 18 STJ); Sentença concessiva não gera reincidência (CP, art. 120); Perdão judicial nos crimes culposos de trânsito; Distinção entre perdão judicial e perdão do ofendido
Não inclui: Perdão do ofendido na ação penal privada → 5196; Perdão judicial como prêmio da colaboração premiada → 5557; Graça e indulto concedidos pelo Presidente da República → 5193; Requisitos típicos do homicídio culposo → 5150
Âncoras legais: CP, art. 107, IX; CP, art. 120; CP, art. 121, §5º; CP, art. 129, §8º; Lei 9.807/1999, art. 13
Desempate: Use este nó quando a extinção decorrer de ato do juiz que deixa de aplicar a pena por previsão legal; se o perdão vier do ofendido, use 5196, e se for benefício da colaboração premiada, use 5557.
```

### 5195 · amostral

```text
[5195] Penal > Punibilidade > Perempção
Escopo: Perempção como causa de extinção da punibilidade na ação penal exclusivamente privada: sanção à inércia ou negligência do querelante já no curso do processo, nas hipóteses legais.
Inclui: Hipóteses do CPP, art. 60: deixar de promover o andamento por 30 dias seguidos; Não comparecimento do substituto processual em 60 dias após a morte ou incapacidade do querelante; Ausência injustificada do querelante a ato do processo e falta de pedido de condenação nas alegações finais; Extinção da pessoa jurídica querelante sem sucessor; Inaplicabilidade à ação penal pública e à ação privada subsidiária da pública; Distinção entre perempção (após o início da ação) e decadência (antes da ação)
Não inclui: Decadência do direito de queixa ou de representação → 5198; Perdão do ofendido e renúncia ao direito de queixa → 5196; Ação penal privada subsidiária e retomada pelo Ministério Público → 5472; Morte do querelado (autor do fato) → 5192
Âncoras legais: CP, art. 107, IV; CPP, art. 60
Desempate: Use este nó quando a inércia do querelante ocorrer depois de iniciada a ação privada; inércia antes da queixa é decadência (5198), e ato voluntário de desistência é perdão do ofendido (5196).
```

### 5196 · amostral

```text
[5196] Penal > Punibilidade > Renúncia, Perdão do Ofendido e Retratação
Escopo: Renúncia ao direito de queixa, perdão do ofendido e retratação do agente como causas de extinção da punibilidade (CP, art. 107, V e VI): conceito, momento, forma, extensão aos coautores e aceitação.
Inclui: Renúncia expressa ou tácita, antes da ação, e sua extensão a todos os autores (CP, art. 104; CPP, art. 49); Perdão do ofendido na ação exclusivamente privada: bilateralidade, aceitação e momento até o trânsito em julgado (CP, arts. 105 e 106); Perdão concedido a um querelado aproveita a todos, mas não produz efeito quanto ao que recusa; Retratação do agente nos casos admitidos em lei (calúnia, difamação, falso testemunho); Retratação da representação até o oferecimento da denúncia (CPP, art. 25); Composição civil dos danos no JECrim como renúncia (Lei 9.099/1995, art. 74, parágrafo único)
Não inclui: Perdão judicial concedido pelo juiz → 5197; Decadência do direito de queixa ou de representação → 5198; Perempção da ação penal privada → 5195; Audiência de renúncia à representação na Lei Maria da Penha (art. 16) → 4704; Requisitos e particularidades da retratação nos crimes contra a honra → 5121; Retratação no crime de falso testemunho ou falsa perícia → 5081
Âncoras legais: CP, art. 104; CP, art. 105; CP, art. 106; CP, art. 107, V e VI; CP, art. 143; CPP, art. 25; CPP, art. 49; CPP, art. 51; Lei 9.099/1995, art. 74, parágrafo único
Desempate: Use este nó quando a extinção decorrer de ato de vontade do ofendido (renúncia, perdão) ou do agente (retratação) tratado como causa extintiva em geral; se a questão se concentrar no tipo específico (honra, falso testemunho) ou no rito da Maria da Penha, use 5121, 5081 ou 4704.
```

### 5209 · amostral

```text
[5209] Penal > Teoria da Pena > Efeitos da Condenação Penais e Extrapenais
Escopo: Efeitos da condenação previstos no Código Penal: o efeito principal (impor a pena), os efeitos secundários penais e os efeitos extrapenais genéricos e específicos (arts. 91, 91-A e 92), incluindo o confisco e a perda alargada de bens.
Inclui: Obrigação de reparar o dano como efeito genérico automático (art. 91, I); Confisco dos instrumentos e do produto do crime (art. 91, II); Perda alargada de bens incompatíveis com o rendimento lícito (art. 91-A); Perda de cargo, função pública ou mandato eletivo (art. 92, I); Incapacidade para o exercício do poder familiar, da tutela ou da curatela (art. 92, II); Inabilitação para dirigir veículo usado em crime doloso (art. 92, III); Exigência de declaração motivada na sentença para os efeitos específicos do art. 92; Efeitos secundários penais: reincidência, revogação de sursis e de livramento
Não inclui: Fixação, na sentença, do valor mínimo da reparação e efeitos da sentença condenatória no CPP (art. 387, IV) → 5577; Execução civil da sentença penal e ação civil ex delicto → 5475; Reabilitação e recuperação dos efeitos do art. 92 → 5210; Sequestro, arresto e hipoteca legal de bens no processo → 5496; Perda de cargo como efeito automático na Lei de Tortura → 4707
Âncoras legais: CP, art. 91; CP, art. 91-A; CP, art. 92; CF, art. 15, III
Desempate: Use este nó quando a questão tratar dos efeitos da condenação conforme as regras materiais do CP (arts. 91 a 92). Se a questão tratar do que a sentença deve conter ou dos efeitos dela conforme o CPP, use o nó 5577.
```

### 5206 · amostral

```text
[5206] Penal > Teoria da Pena > Pena de Multa
Escopo: Pena de multa no Código Penal: sistema de dias-multa, limites e valor do dia-multa, critérios de fixação, pagamento, conversão vedada, natureza de dívida de valor e legitimidade para a execução (arts. 49 a 52 e 60).
Inclui: Sistema de dias-multa: 10 a 360 dias, valor de 1/30 a 5 vezes o salário mínimo; Fixação considerando principalmente a situação econômica do réu (art. 60); Aumento até o triplo quando a multa é ineficaz (art. 60, § 1º); Pagamento em 10 dias, parcelamento e desconto em vencimentos (art. 50); Multa como dívida de valor; vedação da conversão em prisão (art. 51); Execução pelo Ministério Público no juízo da execução penal (art. 51, Lei 13.964/2019); Suspensão da execução da multa sobrevindo doença mental (art. 52); Multa substitutiva e multa vicariante
Não inclui: Aplicação distinta e integral das multas no concurso de crimes (art. 72) → 5070; Prestação pecuniária como pena restritiva de direitos → 5205; Prescrição da pena de multa (art. 114) → 5190; Multa em leis especiais com regras próprias (ex.: Lei de Drogas) → 4708
Âncoras legais: CP, art. 49; CP, art. 50; CP, art. 51; CP, art. 52; CP, art. 60
Desempate: Use este nó para as regras gerais de fixação e execução da multa. Se a questão tratar da soma de multas em concurso de crimes (art. 72), use o nó 5070. Se tratar da prestação pecuniária, use o nó 5205.
```

### 5215 · amostral

```text
[5215] Penal > Teoria do Crime: Culpabilidade > Coação Moral Irresistível
Escopo: Coação moral irresistível (vis compulsiva) como causa legal de exclusão da culpabilidade por inexigibilidade de conduta diversa, com punição apenas do coator, e o tratamento da coação resistível.
Inclui: Requisitos: ameaça grave, irresistível, contra o coagido ou pessoa próxima; Isenção de pena do coagido e punição exclusiva do coator; Coator como autor mediato do crime praticado pelo coagido; Coação moral resistível como atenuante genérica; Diferença entre coação moral (exclui culpabilidade) e coação física (exclui conduta); Concurso entre o crime do coator e o crime de tortura ou constrangimento contra o coagido
Não inclui: Coação física irresistível (vis absoluta) como ausência de conduta → 5221; Obediência hierárquica, segunda parte do art. 22 do CP → 5216; Coação no curso do processo (CP, art. 344) → 5086; Agravante de coagir outrem à execução do crime e atenuante da coação resistível na dosimetria → 5203; Autoria mediata em geral, sem foco na coação → 5073
Âncoras legais: CP, art. 22; CP, art. 65, III, c; CP, art. 62, II
Desempate: Use este nó quando a questão tratar da ameaça grave irresistível que leva alguém a cometer o crime; se a força física elimina a vontade do agente, use 5221.
```

### 5214 · amostral

```text
[5214] Penal > Teoria do Crime: Culpabilidade > Erro de Proibição
Escopo: Erro sobre a ilicitude do fato, que afeta a potencial consciência da ilicitude: espécies, efeitos do erro inevitável e do evitável, e distinção do desconhecimento da lei.
Inclui: Erro de proibição inevitável (isenta de pena) e evitável (reduz de 1/6 a 1/3); Erro de proibição direto, indireto (erro de permissão) e mandamental; Desconhecimento da lei como inescusável x erro sobre a ilicitude do fato; Critério de evitabilidade: possibilidade de atingir a consciência da ilicitude; Teorias extremada e limitada da culpabilidade no erro sobre causas de justificação; Descriminante putativa por erro quanto à existência ou aos limites da causa de justificação
Não inclui: Erro de tipo essencial e acidental (CP, art. 20) → 5224; Descriminante putativa por erro sobre os pressupostos fáticos (CP, art. 20, § 1º) → 5224; Erro determinado por terceiro (CP, art. 20, § 2º) → 5224; Atenuante do desconhecimento da lei na dosimetria → 5203; Erro de direito nas contravenções (LCP, art. 8º) → 4686
Âncoras legais: CP, art. 21; CP, art. 65, II
Desempate: Use este nó quando o agente conhece a situação de fato, mas acredita que a conduta é lícita; se ele se engana sobre um elemento do tipo ou sobre a situação de fato que justificaria a conduta, use 5224.
```

### 5216 · amostral

```text
[5216] Penal > Teoria do Crime: Culpabilidade > Obediência Hierárquica
Escopo: Obediência hierárquica como excludente da culpabilidade: cumprimento de ordem não manifestamente ilegal de superior hierárquico em relação de direito público, com punição apenas do autor da ordem.
Inclui: Requisitos: relação hierárquica de direito público, ordem não manifestamente ilegal, cumprimento estrito da ordem; Punibilidade apenas do superior que deu a ordem; Ordem manifestamente ilegal: ambos respondem, com atenuante para o subordinado; Inaplicabilidade às relações privadas, familiares ou religiosas; Excesso na execução da ordem; Distinção entre ordem ilegal (exculpante) e ordem legal (estrito cumprimento do dever)
Não inclui: Cumprimento de ordem legal como estrito cumprimento do dever legal → 5232; Coação moral irresistível, primeira parte do art. 22 do CP → 5215; Ordem de superior em relação privada tratada como inexigibilidade supralegal → 5217; Agravante de determinar a prática do crime a quem está sujeito à autoridade do agente → 5203; Crimes de abuso de autoridade (Lei 13.869/2019) → 4684
Âncoras legais: CP, art. 22; CP, art. 65, III, c; CP, art. 62, III
Desempate: Use este nó quando o subordinado público cumpre ordem ilegal, mas não manifestamente ilegal; se a ordem for legal, use 5232.
```

### 5221 · amostral

```text
[5221] Penal > Teoria do Crime: Fato Típico > Conduta
Escopo: Conduta como primeiro elemento do fato típico: teorias da ação (causal, neokantista, finalista, social, funcionalistas), elementos da conduta e hipóteses de ausência de conduta.
Inclui: Teorias causalista, finalista, social e funcionalista da ação; Elementos da conduta: voluntariedade e exteriorização; Ausência de conduta: coação física irresistível, atos reflexos, sonambulismo, hipnose; Caso fortuito e força maior como exclusão da conduta; Conduta da pessoa jurídica (dupla imputação); Formas de conduta: ação e omissão (visão geral)
Não inclui: Omissão própria e imprópria, dever de agir do garantidor → 5223; Dolo e culpa como elementos subjetivos da conduta → 5222; Coação moral irresistível (exclui a culpabilidade) → 5215; Visão do fato típico como um todo → 5220
Desempate: Escolha este nó para teorias da ação e ausência de conduta; se o foco for a omissão ou o dever de agir, use 5223, e se for dolo ou culpa, use 5222.
```

### 5225 · amostral

```text
[5225] Penal > Teoria do Crime: Fato Típico > Resultado
Escopo: Resultado como elemento do fato típico: resultado naturalístico e jurídico/normativo, e sua presença nos crimes materiais, formais e de mera conduta, de dano e de perigo.
Inclui: Resultado naturalístico x resultado jurídico (normativo); Crimes materiais, formais e de mera conduta quanto ao resultado; Crimes de dano e de perigo (concreto e abstrato); Exaurimento nos crimes formais; Teoria naturalística x teoria jurídica do resultado
Não inclui: Relação causal entre conduta e resultado → 5226; Momento consumativo e tentativa → 5177; Rol geral de classificações dos crimes → 5174; Crime qualificado pelo resultado e preterdolo → 5222
Desempate: Use este nó quando a questão tratar do resultado como elemento do fato típico; se cobrar várias classificações de crimes juntas, use 5174, e se tratar de consumação, use 5177.
```

### 5227 · amostral

```text
[5227] Penal > Teoria do Crime: Fato Típico > Tipicidade
Escopo: Tipicidade e tipo penal: evolução (Beling, Mayer, ratio essendi), tipicidade formal, material e conglobante, adequação típica imediata e mediata e elementos do tipo (objetivos, normativos, subjetivos).
Inclui: Tipicidade formal e material; Tipicidade conglobante (Zaffaroni) e atos fomentados pelo ordenamento; Adequação típica imediata e mediata (normas de extensão); Teorias da relação tipicidade-ilicitude: ratio cognoscendi, ratio essendi, elementos negativos do tipo; Elementos objetivos, normativos e subjetivos do tipo; Tipo aberto e fechado, tipo básico e derivado
Não inclui: Princípio da insignificância e requisitos do STF → 5172; Estrito cumprimento do dever legal como excludente de ilicitude → 5232; Conflito aparente de normas → 5183; Dolo e culpa como elementos subjetivos → 5222; Fato típico como um todo → 5220
Desempate: Use este nó quando o foco for o juízo de adequação ao tipo ou as espécies de tipicidade; se a questão girar em torno dos requisitos da insignificância como princípio, use 5172.
```

### 5230 · amostral

```text
[5230] Penal > Teoria do Crime: Ilicitude > Estado de Necessidade
Escopo: Estado de necessidade como excludente da ilicitude (CP, art. 24): requisitos, espécies, teorias unitária e diferenciadora, dever legal de enfrentar o perigo e redução de pena quando o sacrifício era razoavelmente exigível.
Inclui: Requisitos: perigo atual, não provocado voluntariamente, inevitável por outro modo, a direito próprio ou alheio; Inexigibilidade do sacrifício do bem ameaçado e ponderação de bens; Teoria unitária (CP) e teoria diferenciadora (CPM); Estado de necessidade próprio e de terceiro, agressivo e defensivo, real e putativo; Dever legal de enfrentar o perigo (art. 24, § 1º) e redução de pena (art. 24, § 2º); Furto famélico e responsabilidade civil no estado de necessidade agressivo
Não inclui: Reação a injusta agressão humana atual ou iminente → 5231; Estado de necessidade exculpante como causa supralegal de exclusão da culpabilidade → 5217; Coação moral irresistível → 5215; Estado de necessidade putativo por erro sobre a situação de fato (art. 20, § 1º) → 5224
Âncoras legais: CP, art. 24; CP, art. 23, I; CC, arts. 188, II, 929 e 930
Desempate: Escolha este nó quando o fato envolver perigo atual não originado de agressão injusta (fenômeno natural, animal, situação de risco); havendo agressão humana injusta, use Legítima Defesa (5231).
```

### 5232 · amostral

```text
[5232] Penal > Teoria do Crime: Ilicitude > Estrito Cumprimento do Dever Legal
Escopo: Estrito cumprimento do dever legal como excludente da ilicitude (CP, art. 23, III): fonte legal do dever, limites, destinatários e incompatibilidade com abusos e excessos.
Inclui: Conceito e requisitos: dever imposto por lei em sentido amplo, cumprido nos estritos limites; Destinatários: agentes públicos e, excepcionalmente, particulares; Uso da força na prisão e na resistência (CPP, arts. 284 e 292); Prisão em flagrante obrigatória pela autoridade policial (CPP, art. 301); Comunicabilidade da excludente aos coautores e partícipes; Discussão sobre a incompatibilidade com crimes culposos
Não inclui: Obediência a ordem não manifestamente ilegal de superior hierárquico → 5216; Policial que repele agressão a refém (art. 25, parágrafo único) → 5231; Exercício regular de direito → 5229; Crimes de abuso de autoridade praticados por agente público → 4684; Tipicidade conglobante como fundamento de atipicidade do cumprimento de dever → 5227
Âncoras legais: CP, art. 23, III; CPP, art. 284; CPP, art. 292; CPP, art. 301
Desempate: Use este nó quando o agente atua cumprindo dever imposto diretamente pela lei; se age por ordem de superior hierárquico, use Obediência Hierárquica (5216), e se reage a agressão injusta, use Legítima Defesa (5231).
```

### 5231 · amostral

```text
[5231] Penal > Teoria do Crime: Ilicitude > Legítima Defesa
Escopo: Legítima defesa como excludente da ilicitude (CP, art. 25): requisitos, espécies, excesso, legítima defesa de terceiro e hipótese do agente de segurança pública que repele agressão a vítima mantida refém.
Inclui: Requisitos: injusta agressão atual ou iminente, a direito próprio ou alheio, meios necessários usados com moderação; Legítima defesa própria e de terceiro, real e putativa, sucessiva e recíproca; Legítima defesa contra agressão de inimputável e erro na execução (aberratio ictus); Excesso doloso, culposo, intensivo e extensivo na legítima defesa; Agente de segurança pública que repele agressão a refém (art. 25, parágrafo único); Legítima defesa da honra (inconstitucionalidade reconhecida pelo STF)
Não inclui: Perigo atual não decorrente de agressão humana injusta → 5230; Ofendículos e exercício regular de direito → 5229; Legítima defesa putativa por erro sobre a situação de fato (art. 20, § 1º) → 5224; Absolvição sumária no júri por reconhecimento da legítima defesa → 5527; Uso da força pelo agente público no cumprimento de dever legal → 5232
Âncoras legais: CP, art. 25; CP, art. 23, II e parágrafo único; CC, art. 188, I
Desempate: Escolha este nó quando houver reação a agressão humana injusta, atual ou iminente, incluindo o excesso nessa reação; se o perigo não vier de agressão injusta, use Estado de Necessidade (5230), e se a questão girar em torno do erro do agente sobre a situação de fato, use Erro de Tipo (5224).
```

### 5476 · amostral

```text
[5476] Processo Penal > Ações Autônomas de Impugnação
Escopo: Meios de impugnação que não são recursos e instauram nova relação processual: habeas corpus, mandado de segurança em matéria criminal e revisão criminal. Todas as partes têm subtema próprio.
Inclui: Natureza jurídica das ações autônomas de impugnação, por oposição aos recursos; Habeas corpus preventivo e liberatório: cabimento, legitimidade e competência; Mandado de segurança contra ato judicial criminal; Revisão criminal: hipóteses de cabimento e legitimidade; Impugnação de decisão transitada em julgado
Não inclui: Teoria geral dos recursos: pressupostos, efeitos e princípios → 5512; Recursos em espécie (apelação, RESE, embargos) → 5560; Relaxamento da prisão ilegal pelo juiz → 5588; Ação civil ex delicto → 5475
Âncoras legais: CF, art. 5º, LXVIII; CF, art. 5º, LXIX; CPP, arts. 621 a 631; CPP, arts. 647 a 667
Desempate: Use este nó quando o meio de impugnação for ação autônoma (HC, MS, revisão criminal); se for recurso interposto na mesma relação processual, use Parte Geral dos Recursos (5512) ou Recursos em Espécie (5560).
```

### 5477 · amostral

```text
[5477] Processo Penal > Ações Autônomas de Impugnação > Habeas Corpus
Escopo: Ação constitucional de impugnação que protege a liberdade de locomoção contra violência ou coação ilegal, atual ou iminente, por ilegalidade ou abuso de poder: cabimento, legitimidade, competência, liminar, processamento e efeitos (CF, art. 5º, LXVIII; CPP, arts. 647 a 667).
Inclui: HC preventivo (salvo-conduto) e liberatório ou repressivo; hipóteses de coação ilegal do art. 648 do CPP; Impetração por qualquer pessoa, sem advogado; paciente, impetrante e autoridade coatora; concessão de ofício; Trancamento de inquérito ou ação penal por atipicidade, extinção da punibilidade ou falta de justa causa; Liminar em HC e competência originária dos tribunais; Súmula 691 do STF (HC contra indeferimento de liminar); Descabimento de HC: punições disciplinares militares (CF, art. 142, § 2º), pena exclusivamente de multa (Súmula 693 do STF), pena privativa de liberdade já extinta (Súmula 695 do STF); HC substitutivo de recurso próprio e o entendimento restritivo do STF e do STJ
Não inclui: Desconstituição de condenação transitada em julgado por erro judiciário ou prova nova → 5478; Impugnação de ato que fere direito líquido e certo sem afetar a liberdade de locomoção (ex.: restituição de bem, acesso aos autos pelo MP) → 5479; Pedido de relaxamento de prisão ilegal dirigido ao próprio juiz → 5588; Recurso em sentido estrito contra a decisão que concede ou nega habeas corpus (CPP, art. 581, X) → 5561; Requisitos e hipóteses de concessão da liberdade provisória, com ou sem fiança → 5523; Teoria e espécies de nulidades processuais, quando não se discute o HC como via de impugnação → 5511
Âncoras legais: CF, art. 5º, LXVIII; CF, art. 142, § 2º; CF, art. 102, I, d e i; CF, art. 105, I, c; CPP, arts. 647 a 667; CPP, art. 648; Súmula 691 do STF; Súmula 693 do STF; Súmula 695 do STF
Desempate: Escolha este nó quando a questão tratar do habeas corpus como via de impugnação (cabimento, legitimidade, competência, procedimento), mesmo que o pano de fundo seja uma prisão ou uma nulidade; se o foco for o instituto de fundo (requisitos da preventiva, relaxamento, espécie de nulidade), classifique no nó desse instituto.
```

### 5479 · amostral

```text
[5479] Processo Penal > Ações Autônomas de Impugnação > Mandado de Segurança
Escopo: Mandado de segurança em matéria criminal: remédio constitucional para proteger direito líquido e certo, não amparado por habeas corpus, violado ou ameaçado por ato ilegal ou abusivo de autoridade, inclusive ato judicial, e seu uso excepcional no processo penal (CF, art. 5º, LXIX; Lei 12.016/2009).
Inclui: Direito líquido e certo, prova pré-constituída e vedação de dilação probatória; Caráter residual: cabe só quando não houver HC nem recurso com efeito suspensivo; descabimento contra decisão transitada em julgado; MS contra ato judicial no processo penal: decisões teratológicas e flagrante ilegalidade; MS impetrado pelo MP ou pelo assistente de acusação e a citação do réu como litisconsorte passivo (Súmula 701 do STF); MS para restituição de bens, acesso do advogado aos autos e efeito suspensivo a recurso; Prazo decadencial de 120 dias, liminar, autoridade coatora e competência originária dos tribunais
Não inclui: Tutela da liberdade de locomoção ameaçada ou violada → 5477; Rescisão de sentença penal condenatória transitada em julgado → 5478; Correição parcial contra erro ou abuso que inverte a ordem do processo → 5568; Procedimento do incidente de restituição de coisas apreendidas no CPP → 5495; Sequestro, arresto e hipoteca legal como medidas assecuratórias → 5496
Âncoras legais: CF, art. 5º, LXIX; Lei 12.016/2009, art. 1º; Lei 12.016/2009, art. 5º; Lei 12.016/2009, art. 23; Súmula 701 do STF; Súmula 267 do STF; Súmula 268 do STF
Desempate: Escolha este nó quando o direito violado não for a liberdade de locomoção, pois se houver risco, ainda que indireto, à liberdade ambulatorial o remédio é o habeas corpus (5477).
```

### 5478 · amostral

```text
[5478] Processo Penal > Ações Autônomas de Impugnação > Revisão Criminal
Escopo: Ação autônoma de impugnação, exclusiva da defesa, para desconstituir sentença penal condenatória ou absolutória imprópria transitada em julgado nas hipóteses do art. 621 do CPP: cabimento, legitimidade, prazo, competência, processamento e efeitos (CPP, arts. 621 a 631).
Inclui: Hipóteses do art. 621 do CPP: decisão contrária à lei ou à evidência dos autos, provas falsas e provas novas de inocência ou de circunstância que diminua a pena; Revisão apenas pro reo: vedação da revisão pro societate, inclusive em caso de absolvição baseada em certidão de óbito falsa; Possibilidade de pedido a qualquer tempo, antes ou depois de extinta a pena; reiteração somente com novas provas (CPP, art. 622); Legitimidade do réu, de procurador habilitado e, após a morte, do cônjuge, ascendente, descendente ou irmão (CPP, art. 623); desnecessidade de recolhimento à prisão (Súmula 393 do STF); Competência originária dos tribunais e processamento (CPP, arts. 624 e 625); Efeitos do julgamento: absolvição, alteração da classificação, redução da pena ou anulação do processo; vedação da reformatio in pejus (CPP, art. 626); Indenização por erro judiciário (CPP, art. 630; CF, art. 5º, LXXV); Cabimento contra sentença do júri e contra sentença absolutória imprópria
Não inclui: Impugnação de decisão ainda não transitada em julgado por meio de apelação → 5562; Uso do habeas corpus para atacar ilegalidade que afeta a liberdade de locomoção, inclusive após o trânsito em julgado → 5477; Aplicação de lei penal mais benéfica posterior ao trânsito em julgado como regra de direito intertemporal → 5181; Reabilitação criminal para assegurar sigilo dos registros e suspender efeitos da condenação → 5210; Reparação do dano causado pelo crime à vítima (ação civil ex delicto) → 5475
Âncoras legais: CPP, arts. 621 a 631; CPP, art. 621; CPP, art. 622; CPP, art. 623; CPP, art. 626; CPP, art. 630; CF, art. 5º, LXXV; Súmula 393 do STF
Desempate: Escolha este nó quando a impugnação visar desconstituir a própria condenação transitada em julgado por erro judiciário ou prova nova; se o pedido for a proteção imediata da liberdade de locomoção sem exame aprofundado de provas, classifique em Habeas Corpus (5477).
```

### 5497 · amostral

```text
[5497] Processo Penal > Das Questões e Processos Incidentes > Incidente de Falsidade e de Insanidade Mental
Escopo: Incidente de falsidade documental e incidente de insanidade mental do acusado no CPP: instauração, legitimidade, procedimento, suspensão do processo e efeitos da decisão.
Inclui: Arguição de falsidade de documento constante dos autos (CPP, art. 145); Poderes especiais do procurador para arguir falsidade (CPP, art. 146); Decisão do incidente sem efeito de coisa julgada em outro processo (CPP, art. 148); Instauração do exame de insanidade mental de ofício ou a requerimento (CPP, art. 149); Nomeação de curador e suspensão do processo durante o exame; Doença mental superveniente à infração e suspensão do processo (CPP, art. 152); Prazo e internação para realização do exame (CPP, art. 150)
Não inclui: Crimes de falsificação de documento público ou particular e uso de documento falso → 5118; Inimputabilidade por doença mental e semi-imputabilidade (CP, art. 26) → 5213; Espécies, prazos e cessação da medida de segurança → 5184; Valor probatório dos documentos e sua juntada → 5553; Regras gerais sobre perícias e peritos → 5546; Superveniência de doença mental durante a execução da pena → 4703
Âncoras legais: CPP, arts. 145 a 148; CPP, arts. 149 a 154
Desempate: Use este nó quando a questão tratar do incidente processual (instauração, rito, suspensão); se tratar do conceito de inimputabilidade ou da medida de segurança aplicada, use 5213 ou 5184.
```

### 5496 · amostral

```text
[5496] Processo Penal > Das Questões e Processos Incidentes > Medidas Assecuratórias: Sequestro, Hipoteca Legal e Arresto
Escopo: Medidas assecuratórias do CPP sobre bens do investigado ou acusado: sequestro, hipoteca legal, arresto, alienação antecipada e utilização de bens, com requisitos, legitimidade, embargos e levantamento.
Inclui: Sequestro de bens imóveis e móveis adquiridos com os proventos da infração (CPP, arts. 125 a 132); Requisito de indícios veementes da proveniência ilícita (CPP, art. 126); Embargos de terceiro e do acusado ao sequestro (CPP, arts. 129 e 130); Levantamento do sequestro (CPP, art. 131); Hipoteca legal sobre imóveis do acusado para reparação do dano (CPP, arts. 134 e 135); Arresto de imóveis e de móveis penhoráveis (CPP, arts. 136 e 137); Alienação antecipada de bens (CPP, art. 144-A) e utilização por órgãos públicos (CPP, art. 133-A)
Não inclui: Confisco e perda de bens como efeito da condenação (CP, art. 91) → 5209; Medidas assecuratórias da Lei de Lavagem de Dinheiro → 4702; Apreensão e perdimento de bens na Lei de Drogas → 4708; Restituição de coisas apreendidas → 5495; Execução civil e ação civil ex delicto para reparação do dano → 5475; Busca e apreensão como meio de prova → 5554
Âncoras legais: CPP, arts. 125 a 144-A
Desempate: Use este nó para constrição patrimonial cautelar regida pelo CPP; se a questão for sobre a apreensão/devolução de coisas ligadas à prova ou ao crime, use 5495; se sobre lei especial, use o nó da lei.
```

### 5491 · amostral

```text
[5491] Processo Penal > Das Questões e Processos Incidentes > Questões Prejudiciais e Preliminares
Escopo: Questões prejudiciais (obrigatórias e facultativas, homogêneas e heterogêneas) e sua distinção das preliminares, com suspensão do processo e efeitos. Exceções específicas têm nós irmãos próprios.
Inclui: Conceito de questão prejudicial e distinção de questão preliminar; Prejudicial obrigatória sobre estado civil das pessoas (CPP, art. 92); Prejudicial facultativa de competência do juízo cível (CPP, art. 93); Suspensão do processo e prazo de suspensão na prejudicial facultativa; Classificação: homogêneas e heterogêneas, devolutivas e não devolutivas; Intervenção do MP na ação cível e decretação de ofício da suspensão (CPP, art. 94)
Não inclui: Suspensão do prazo prescricional enquanto não resolvida questão prejudicial (CP, art. 116, I) → 5187; Exceção de incompetência ou de ilegitimidade → 5493; Exceção de litispendência ou de coisa julgada → 5494; Exceção de suspeição ou impedimento → 5492; Recurso contra a decisão que ordena a suspensão do processo (RESE) → 5561
Âncoras legais: CPP, arts. 92 a 94; CP, art. 116, I
Desempate: Use este nó para prejudiciais e para a noção geral de questão preliminar; se a preliminar for uma exceção específica (suspeição, incompetência, ilegitimidade, litispendência, coisa julgada), use o nó irmão correspondente.
```

### 5495 · amostral

```text
[5495] Processo Penal > Das Questões e Processos Incidentes > Restituição de Coisas Apreendidas
Escopo: Restituição de coisas apreendidas no processo penal: requisitos, momento, autoridade competente, dúvida sobre o direito do reclamante, destinação de bens não reclamados e venda em leilão.
Inclui: Vedação de restituição enquanto a coisa interessar ao processo (CPP, art. 118); Coisas insuscetíveis de restituição por serem confiscáveis (CPP, art. 119); Restituição pela autoridade policial ou judicial sem dúvida sobre o direito (CPP, art. 120); Incidente de restituição com dúvida e remessa ao juízo cível; Coisas apreendidas em poder de terceiro de boa-fé; Destino dos bens não reclamados e leilão (CPP, arts. 122 e 123); Destinação de instrumentos do crime e bens perdidos (CPP, arts. 124 e 124-A)
Não inclui: Perda de instrumentos e produtos do crime como efeito da condenação (CP, art. 91, II) → 5209; Requisitos e cumprimento da busca e apreensão → 5554; Sequestro, hipoteca legal e arresto → 5496; Cadeia de custódia de vestígios apreendidos → 5544; Mandado de segurança contra apreensão ilegal → 5479
Âncoras legais: CPP, arts. 118 a 124-A; CP, art. 91, II
Desempate: Use este nó quando o foco for a devolução ou destinação da coisa apreendida; se for a constrição de bens para garantir reparação ou perdimento, use 5496.
```

### 5502 · amostral

```text
[5502] Processo Penal > Inquérito Policial > Acordo de Não Persecução Penal
Escopo: Acordo de não persecução penal (ANPP): negócio jurídico pré-processual entre MP e investigado, com seus requisitos, condições, vedações, homologação judicial, descumprimento e efeitos sobre a punibilidade.
Inclui: Requisitos: confissão formal e circunstanciada, infração sem violência ou grave ameaça, pena mínima inferior a 4 anos; Condições ajustáveis: reparação do dano, renúncia a bens, prestação de serviços, prestação pecuniária; Vedações: cabimento de transação penal, reincidência ou conduta habitual, benefício nos 5 anos anteriores, violência doméstica ou contra a mulher; Audiência de homologação, verificação de voluntariedade e recusa de homologação pelo juiz; Recusa do MP em propor e remessa ao órgão superior do MP; Descumprimento, rescisão, oferecimento de denúncia e extinção da punibilidade pelo cumprimento; Retroatividade do ANPP a processos em curso (jurisprudência do STF/STJ)
Não inclui: Transação penal em infrações de menor potencial ofensivo → 5541; Suspensão condicional do processo (Lei 9.099/1995, art. 89) → 5542; Colaboração premiada como meio de obtenção de prova → 5557; Arquivamento do inquérito policial e controle do art. 28 do CPP → 5501; Princípio da obrigatoriedade e sua mitigação em abstrato → 5469
Âncoras legais: CPP, art. 28-A; Lei 13.964/2019
Desempate: Use este nó quando a questão tratar do acordo do art. 28-A do CPP; se o instituto negocial for da Lei 9.099/1995 (transação penal ou sursis processual), use 5541 ou 5542.
```

### 5503 · amostral

```text
[5503] Processo Penal > Inquérito Policial > Juiz das Garantias
Escopo: Juiz das garantias: competência para controlar a legalidade da investigação e salvaguardar direitos do investigado, limites de atuação, cessação da competência e impedimento, conforme os arts. 3º-A a 3º-F do CPP e o julgamento das ADIs pelo STF.
Inclui: Rol de competências do art. 3º-B do CPP (decidir cautelares, prorrogar IP de preso, autorizar meios de obtenção de prova); Momento de cessação da competência (oferecimento da denúncia, conforme o STF); Impedimento do juiz das garantias para o processo de conhecimento; Infrações excluídas: menor potencial ofensivo, competência originária dos tribunais, júri e violência doméstica (STF); Decisão do STF nas ADIs 6298, 6299, 6300 e 6305 e prazo de implementação; Vedação ao uso de imagem do preso e regras do art. 3º-F; Prorrogação do inquérito com investigado preso pelo juiz das garantias
Não inclui: Sistema acusatório, inquisitivo e misto em abstrato → 5581; Realização e finalidade da audiência de custódia → 5589; Requisitos da prisão preventiva → 5519; Prazos e diligências do inquérito em si → 5500; Hipóteses de impedimento e suspeição do juiz em geral → 5492
Âncoras legais: CPP, art. 3º-A; CPP, art. 3º-B; CPP, art. 3º-C; CPP, art. 3º-D; CPP, art. 3º-E; CPP, art. 3º-F; Lei 13.964/2019
Desempate: Escolha este nó quando a questão girar em torno da figura do juiz das garantias e de sua competência; se tratar só da estrutura acusatória em tese, use 5581, e se tratar do rito da custódia, use 5589.
```

### 5509 · amostral

```text
[5509] Processo Penal > Nulidades
Escopo: Teoria das nulidades no processo penal: nulidade absoluta e relativa, princípios (prejuízo, interesse, causalidade, convalidação) e nulidades em espécie do CPP. Todas as partes têm subtema próprio.
Inclui: Distinção entre nulidade absoluta e relativa; Princípio pas de nullité sans grief (CPP, art. 563); Momento de arguição e preclusão (CPP, art. 571); Hipóteses do CPP, art. 564; Ausência ou deficiência de defesa; Nulidade por falta de citação ou de intimação
Não inclui: Prova ilícita e derivada → 5594; Exceções de suspeição e impedimento → 5492; Relaxamento de prisão ilegal → 5588; Revisão criminal para desconstituir condenação → 5478; Formas de citação e de intimação → 5487
Âncoras legais: CPP, arts. 563 a 573; CPP, art. 564
```

### 5514 · amostral

```text
[5514] Processo Penal > Parte Geral dos Recursos > Pressupostos Objetivos e Subjetivos de Admissibilidade Recursal
Escopo: Requisitos para que o recurso seja conhecido: pressupostos objetivos (cabimento, adequação, tempestividade, regularidade formal, preparo, ausência de fatos impeditivos ou extintivos) e subjetivos (legitimidade e interesse recursal).
Inclui: Legitimidade recursal do MP, do querelante, do réu, do defensor e do assistente/ofendido; Interesse recursal (sucumbência), inclusive o recurso da defesa contra absolvição para mudar o fundamento; Tempestividade como pressuposto geral e recurso interposto por petição ou termo; Fatos impeditivos e extintivos: renúncia e desistência do recurso; Conflito de vontade entre réu e defensor técnico quanto a recorrer; Preparo e deserção nos casos em que se exige; Juízo de admissibilidade (prelibação) e juízo de mérito
Não inclui: Fungibilidade recursal e recebimento de um recurso por outro → 5513; Indisponibilidade do recurso pelo Ministério Público tratada como princípio → 5513; Prazo e cabimento de um recurso específico → 5562; Contagem de prazo a partir da intimação → 5489; Recurso contra a denegação ou o não seguimento do RESE ou do agravo em execução → 5567
Âncoras legais: CPP, art. 577; CPP, art. 578; CPP, art. 598; CPP, art. 575; CPP, art. 806, § 2º
Desempate: Use este nó quando a questão perguntar se o recurso pode ser conhecido (quem pode recorrer, com que interesse, se há renúncia ou desistência); se a matéria for cabimento ou prazo de um recurso nominado, use o nó do recurso em espécie.
```

### 5513 · amostral

```text
[5513] Processo Penal > Parte Geral dos Recursos > Princípios Recursais no Processo Penal
Escopo: Princípios que regem o sistema recursal penal: duplo grau de jurisdição, voluntariedade, taxatividade, unirrecorribilidade, fungibilidade, disponibilidade e indisponibilidade, dialeticidade, complementaridade e vedação da reformatio in pejus.
Inclui: Duplo grau de jurisdição e sua base constitucional e convencional; Princípio da voluntariedade e da disponibilidade; vedação de desistência do recurso pelo MP; Taxatividade e unirrecorribilidade (singularidade); Fungibilidade recursal: ausência de má-fé e interposição no prazo correto; Proibição da reformatio in pejus direta e indireta, inclusive após anulação em recurso exclusivo da defesa e no Júri; Nulidade não arguida no recurso da acusação contra o réu (Súmula 160 do STF); Dialeticidade e complementaridade recursal
Não inclui: Hipóteses de recurso de ofício como espécie de classificação → 5516; Efeito extensivo do recurso a corréus → 5515; Legitimidade, interesse, renúncia e desistência como pressupostos de admissibilidade → 5514; Princípios gerais do processo penal fora da matéria recursal → 5582; Soberania dos veredictos e limites da apelação no Júri → 5525
Âncoras legais: CPP, art. 574; CPP, art. 576; CPP, art. 579; CPP, art. 617; Decreto 678/1992 (CADH), art. 8º, 2, h
Desempate: Use este nó quando a questão cobrar um princípio recursal (fungibilidade, reformatio in pejus, taxatividade, unirrecorribilidade, duplo grau); se tratar de requisitos de conhecimento, use 5514, e se tratar dos efeitos da interposição, use 5515.
```

### 5523 · amostral

```text
[5523] Processo Penal > Prisões em Espécie > Liberdade Provisória
Escopo: Liberdade provisória, com ou sem fiança, como alternativa à prisão em flagrante: cabimento, vedações, fiança (concessão, valor, dispensa, quebra, perda, cassação, reforço) e crimes inafiançáveis.
Inclui: Liberdade provisória com ou sem fiança (CPP, art. 310, III, e art. 321); Fiança arbitrada pelo delegado (pena máxima até 4 anos) e pelo juiz; Valores, dispensa, redução e aumento da fiança; Quebramento, perda, cassação e reforço da fiança; Crimes inafiançáveis (racismo, tortura, tráfico, terrorismo, hediondos, ação de grupos armados) e situações de vedação da fiança; Denegação da liberdade provisória ao reincidente ou integrante de organização criminosa armada ou milícia (CPP, art. 310, § 2º)
Não inclui: Relaxamento da prisão ilegal → 5588; Requisitos e procedimento das medidas cautelares do art. 319 aplicadas de forma autônoma → 5522; Audiência de custódia e seu procedimento → 5589; Conversão do flagrante em preventiva e seus requisitos → 5519; Regime especial dos crimes hediondos previsto na Lei 8.072/1990 como um todo → 4693
Âncoras legais: CF, art. 5º, LXVI; CF, art. 5º, XLII a XLIV; CPP, art. 310; CPP, arts. 321 a 350
Desempate: Use este nó quando a questão tratar da soltura do preso em flagrante legal, com ou sem fiança; se a prisão for ilegal e a questão for sobre soltura, use Relaxamento da Prisão (5588).
```

### 5522 · amostral

```text
[5522] Processo Penal > Prisões em Espécie > Medidas Cautelares Diversas da Prisão
Escopo: Medidas cautelares pessoais diversas da prisão: requisitos gerais (necessidade e adequação), rol do art. 319 do CPP, proibição de ausentar-se do país, aplicação isolada ou cumulativa, substituição e descumprimento.
Inclui: Requisitos do art. 282 (necessidade e adequação) e o contraditório prévio; Rol do art. 319: comparecimento periódico, proibição de acesso e de contato, recolhimento noturno, suspensão de função, internação provisória, fiança, monitoração eletrônica; Proibição de ausentar-se do país com entrega do passaporte (CPP, art. 320); Vedação de decretação de ofício pelo juiz após a Lei 13.964/2019; Descumprimento: substituição, cumulação ou preventiva como última medida (art. 282, § 4º); Revogação e nova decretação das cautelares
Não inclui: Medidas protetivas de urgência da Lei Maria da Penha → 4704; Sequestro, arresto e hipoteca legal de bens → 5496; Fiança como contracautela da liberdade provisória → 5523; Prisão domiciliar substitutiva da preventiva → 5521; Pressupostos e hipóteses de cabimento da prisão preventiva → 5519
Âncoras legais: CPP, art. 282; CPP, arts. 319 e 320
Desempate: Use este nó para as medidas do art. 319 e as regras gerais do art. 282; se a questão envolver a fiança no contexto da soltura do preso em flagrante, use Liberdade Provisória (5523).
```

### 5534 · amostral

```text
[5534] Processo Penal > Procedimento Ordinário > Absolvição Sumária
Escopo: Absolvição sumária no procedimento comum (CPP, art. 397): julgamento antecipado de mérito após a resposta à acusação, nas hipóteses legais taxativas, com natureza, momento, fundamentos e recurso cabível.
Inclui: Hipóteses do art. 397: excludente de ilicitude manifesta, excludente de culpabilidade (salvo inimputabilidade), fato evidentemente atípico e extinção da punibilidade; Vedação de absolvição sumária por inimputabilidade no rito comum; Momento: após a resposta à acusação e antes da designação da audiência; Exigência de prova manifesta ou evidente e aplicação do in dubio pro societate nessa fase; Natureza jurídica: decisão de mérito que faz coisa julgada material; Aplicação do art. 397 aos procedimentos de primeiro grau (CPP, art. 394, § 4º); Recurso cabível contra a absolvição sumária: apelação, ou RESE quando o fundamento for extinção da punibilidade
Não inclui: Absolvição sumária na primeira fase do Júri (CPP, art. 415), inclusive por inimputabilidade → 5527; Rejeição liminar da denúncia por inépcia, falta de pressuposto ou de justa causa (CPP, art. 395) → 5531; Conteúdo e prazo da resposta à acusação (CPP, arts. 396 e 396-A) → 5533; Sentença absolutória ao final da instrução e fundamentos do art. 386 do CPP → 5574; Requisitos materiais das excludentes de ilicitude, como a legítima defesa → 5231
Âncoras legais: CPP, art. 397; CPP, art. 394, § 4º; CPP, art. 593, I; CPP, art. 581, VIII
Desempate: Use este nó quando a questão tratar da decisão do art. 397 do CPP no rito comum; se a absolvição sumária for a do Júri (art. 415), use 5527; se o foco for o instituto material da excludente, use o nó de Penal.
```

### 5535 · amostral

```text
[5535] Processo Penal > Procedimento Ordinário > Audiência de Instrução e Julgamento
Escopo: Audiência de instrução e julgamento do procedimento ordinário (CPP, arts. 399 a 405): designação, prazo, ordem dos atos, limites da prova oral, concentração, identidade física do juiz, registro dos depoimentos e diligências finais.
Inclui: Designação da audiência, intimações e requisição do réu preso (CPP, art. 399); Identidade física do juiz (CPP, art. 399, § 2º); Realização em até 60 dias e ordem dos atos: ofendido, testemunhas de acusação e defesa, peritos, acareações, reconhecimento e interrogatório por último (CPP, art. 400); Número máximo de 8 testemunhas por parte e desistência (CPP, art. 401); Indeferimento de provas irrelevantes, impertinentes ou protelatórias; Requerimento de diligências ao fim da instrução (CPP, art. 402); Registro audiovisual dos depoimentos e termo de audiência (CPP, art. 405); Concentração dos atos e oralidade na audiência
Não inclui: Regras próprias do interrogatório: direito ao silêncio, videoconferência e entrevista com defensor → 5547; Regras da prova testemunhal: compromisso, contradita, cross-examination (CPP, art. 212) → 5550; Debates orais e memoriais (CPP, arts. 403 e 404) → 5536; Instrução preliminar e audiência da primeira fase do Júri → 5526; Audiência do procedimento sumário (CPP, arts. 531 a 536) → 5538; Reconhecimento de pessoas e coisas (CPP, art. 226) → 5551
Âncoras legais: CPP, art. 399; CPP, art. 400; CPP, art. 401; CPP, art. 402; CPP, art. 405; CF, art. 5º, LV
Desempate: Use este nó quando o foco for a dinâmica da audiência no rito ordinário (ordem dos atos, prazos, número de testemunhas, identidade física do juiz); se o foco for o regime de um meio de prova específico, use o nó de Provas em Espécies.
```

### 5532 · amostral

```text
[5532] Processo Penal > Procedimento Ordinário > Classificação dos Procedimentos
Escopo: Classificação dos procedimentos penais em comum (ordinário, sumário, sumaríssimo) e especial, com os critérios de escolha do rito, sobretudo a pena máxima, e a aplicação subsidiária do procedimento ordinário.
Inclui: Procedimento ordinário: crimes com pena máxima igual ou superior a 4 anos; Procedimento sumário: pena máxima inferior a 4 anos; Procedimento sumaríssimo: infrações de menor potencial ofensivo (Lei 9.099/1995); Procedimentos especiais previstos no CPP e em leis extravagantes; Aplicação subsidiária do rito ordinário aos demais (CPP, art. 394, § 5º); Aplicação dos arts. 395 a 398 a todos os procedimentos de primeiro grau (CPP, art. 394, § 4º); Prioridade de tramitação dos processos de crimes hediondos (CPP, art. 394-A)
Não inclui: Tramitação do procedimento sumário em si (audiência, debates) → 5538; Competência dos Juizados Especiais Criminais e conceito de menor potencial ofensivo → 5540; Rito bifásico do Tribunal do Júri → 5526; Procedimento especial da Lei de Drogas → 4708; Rito da Lei Maria da Penha e vedação da Lei 9.099/1995 → 4704
Âncoras legais: CPP, art. 394; CPP, art. 394-A; Lei 9.099/1995, art. 61
Desempate: Use este nó quando a questão pedir qual rito se aplica ou os critérios de classificação; se tratar do andamento de um rito específico (sumário, sumaríssimo, Júri), use o nó desse rito.
```

### 5533 · amostral

```text
[5533] Processo Penal > Procedimento Ordinário > Defesa Preliminar
Escopo: Resposta à acusação (defesa preliminar) no procedimento comum (CPP, arts. 396 e 396-A): prazo, conteúdo, obrigatoriedade e nomeação de defensor. Inclui a defesa preliminar anterior ao recebimento nos crimes funcionais (CPP, art. 514).
Inclui: Citação para resposta escrita em 10 dias (CPP, art. 396); Contagem do prazo na citação por edital a partir do comparecimento do acusado ou do defensor constituído; Conteúdo: preliminares, documentos, justificações, provas e rol de testemunhas (CPP, art. 396-A); Obrigatoriedade: nomeação de defensor se a resposta não for apresentada (CPP, art. 396-A, § 2º); Natureza de peça defensiva obrigatória e consequências de sua falta; Defesa preliminar do funcionário público antes do recebimento (CPP, art. 514) e Súmula 330 do STJ; Arguição de exceções na resposta
Não inclui: Decisão de absolvição sumária após a resposta (CPP, art. 397) → 5534; Recebimento ou rejeição da denúncia (CPP, arts. 395 e 396) → 5531; Modalidades de citação e revelia (CPP, arts. 351 a 366) → 5488; Defesa prévia no rito da Lei de Drogas (Lei 11.343/2006, art. 55) → 4708; Processamento das exceções de suspeição, incompetência, litispendência → 5492
Âncoras legais: CPP, art. 396; CPP, art. 396-A; CPP, art. 514
Desempate: Use este nó quando o foco for a peça defensiva inicial (prazo, conteúdo, obrigatoriedade); se a questão tratar da forma da citação, use 5488; se tratar da decisão posterior do juiz, use 5534.
```

### 5531 · amostral

```text
[5531] Processo Penal > Procedimento Ordinário > Oferecimento, Rejeição e Recebimento da Peça Acusatória
Escopo: Juízo de admissibilidade da denúncia ou queixa no procedimento comum: hipóteses de rejeição (CPP, art. 395), recebimento e citação (CPP, art. 396), momento do recebimento e efeitos da decisão.
Inclui: Rejeição por inépcia, falta de pressuposto processual ou condição da ação e ausência de justa causa (CPP, art. 395); Recebimento da peça e ordem de citação (CPP, art. 396); Discussão sobre o momento do recebimento (arts. 396 e 399); Natureza e fundamentação da decisão de recebimento; Súmula 709 do STF: acórdão que provê recurso contra rejeição vale como recebimento; Recebimento parcial e aditamento da denúncia antes do recebimento
Não inclui: Requisitos formais e prazo para oferecimento da denúncia (CPP, arts. 41 e 46) → 5473; Requisitos e prazo da queixa-crime → 5474; Cabimento do RESE contra a rejeição da denúncia (CPP, art. 581, I) → 5561; Recebimento da denúncia como causa interruptiva da prescrição (CP, art. 117, I) → 5187; Condições da ação penal em abstrato → 5467; Absolvição sumária (CPP, art. 397) → 5534
Âncoras legais: CPP, art. 395; CPP, art. 396; CPP, art. 394, § 4º
Desempate: Use este nó quando a questão tratar da decisão judicial de receber ou rejeitar a peça; se o foco for a elaboração da denúncia (requisitos, prazo), use 5473; se for a queixa, use 5474.
```

### 5527 · amostral

```text
[5527] Processo Penal > Procedimento do Tribunal do Júri > Impronúncia, Desclassificação, Absolvição Sumária e Pronúncia
Escopo: Decisões que encerram a primeira fase do júri (judicium accusationis): pronúncia, impronúncia, absolvição sumária e desclassificação, com requisitos, natureza jurídica, efeitos e recursos cabíveis.
Inclui: Pronúncia: materialidade e indícios suficientes de autoria, linguagem comedida e vedação de excesso (eloquência acusatória); Impronúncia: falta de prova da materialidade ou de indícios de autoria; nova denúncia enquanto não extinta a punibilidade; Absolvição sumária no júri: hipóteses do art. 415 e ressalva da inimputabilidade; Desclassificação na primeira fase e remessa ao juízo competente (art. 419); Debate sobre in dubio pro societate na pronúncia; Recursos: RESE contra a pronúncia e apelação contra impronúncia e absolvição sumária; Intimação da pronúncia e preclusão
Não inclui: Absolvição sumária do procedimento comum (art. 397 do CPP) → 5534; Desclassificação feita pelos jurados em plenário (art. 492, §§ 1º e 2º) → 5529; Estrutura e atos da primeira fase até a audiência (arts. 406 a 412) → 5526; Cabimento e processamento do RESE em geral → 5561; Cabimento e processamento da apelação em geral → 5562
Âncoras legais: CPP, arts. 413 a 421; CPP, art. 581, IV; CPP, art. 416
Desempate: Use este nó quando a questão tratar do conteúdo, dos requisitos ou dos efeitos da decisão que encerra a primeira fase; se tratar dos atos que vêm antes dela (resposta, audiência, prazos), use 5526.
```

### 5528 · amostral

```text
[5528] Processo Penal > Procedimento do Tribunal do Júri > Organização do Júri e Sessão de Julgamento
Escopo: Organização do Tribunal do Júri e desenvolvimento da sessão plenária: alistamento e função dos jurados, desaforamento, pauta, composição do conselho de sentença, instrução em plenário, debates, quesitação e votação.
Inclui: Alistamento, requisitos, isenções, direitos e deveres dos jurados; Desaforamento: hipóteses, legitimidade e processamento; Composição: juiz presidente, 25 jurados e 7 no conselho de sentença; recusas imotivadas e impedimentos; Instalação da sessão, adiamentos e ausência do acusado ou do defensor; Instrução em plenário, uso de algemas e leitura de peças; Debates: tempo, réplica, tréplica e vedações de referência (art. 478); Formulação e votação dos quesitos, incluindo o quesito genérico de absolvição; Ata da sessão e atribuições do juiz presidente
Não inclui: Sigilo das votações e soberania dos veredictos como garantias constitucionais → 5525; Sentença do juiz presidente, dosimetria e execução da pena após o veredicto → 5529; Preparação do processo para o plenário (arts. 422 a 424) → 5526; Protesto por novo júri → 5563
Âncoras legais: CPP, arts. 425 a 491; CPP, arts. 494 a 497; CPP, arts. 427 e 428
Desempate: Use este nó quando a questão tratar dos atos da sessão até a votação dos quesitos; se tratar da sentença lavrada após o veredicto, use 5529; se discutir a garantia constitucional em abstrato, use 5525.
```

### 5529 · amostral

```text
[5529] Processo Penal > Procedimento do Tribunal do Júri > Sentença do Júri
Escopo: Sentença proferida pelo juiz presidente com base no veredicto dos jurados: condenação, absolvição, desclassificação em plenário, dosimetria, execução da pena e leitura da sentença.
Inclui: Sentença condenatória: fixação da pena pelo juiz presidente, considerando as agravantes e atenuantes debatidas; Execução provisória da pena aplicada pelo júri (art. 492, I, e) e entendimento do STF; Sentença absolutória e seus efeitos (soltura, revogação de medidas); Desclassificação própria e imprópria em plenário e julgamento do crime conexo; Aplicação de institutos despenalizadores após a desclassificação; Leitura da sentença em plenário
Não inclui: Desclassificação na primeira fase (art. 419) → 5527; Formulação e votação dos quesitos → 5528; Apelação contra decisão do júri (art. 593, III) → 5562; Requisitos gerais da sentença condenatória no procedimento comum → 5575; Dosimetria da pena nas regras do Código Penal → 5203
Âncoras legais: CPP, arts. 492 e 493
Desempate: Use este nó quando a questão tratar do que o juiz presidente decide após a votação dos quesitos; se tratar da votação em si, use 5528.
```

### 5548 · amostral

```text
[5548] Processo Penal > Provas em Espécies > Confissão
Escopo: Confissão como meio de prova: admissão, pelo imputado, da autoria ou participação no fato, com suas espécies, características (divisibilidade e retratabilidade), requisitos de validade e valor probatório relativo, nos termos dos arts. 197 a 200 do CPP.
Inclui: Espécies: judicial e extrajudicial, simples, qualificada, complexa, parcial, retratada; Divisibilidade e retratabilidade da confissão; Valor relativo e necessidade de confronto com as demais provas; Silêncio não importa confissão; Voluntariedade e vedação de confissão obtida por coação ou tortura; Confissão extrajudicial não confirmada em juízo; Reflexo da confissão espontânea como atenuante genérica
Não inclui: Procedimento e formalidades do interrogatório judicial → 5547; Compensação da atenuante da confissão com a reincidência na dosimetria → 5203; Colaboração premiada → 5557; Crime de tortura para obter confissão → 4707; Confissão como requisito do acordo de não persecução penal → 5502; Sistema do livre convencimento motivado em geral → 5592
Âncoras legais: CPP, arts. 197 a 200; CF, art. 5º, LXIII; CP, art. 65, III, "d"
Desempate: Escolha este nó quando o núcleo for a admissão do fato pelo acusado e seu valor probatório; se a questão tratar do cálculo da pena com a atenuante, use 5203, e se tratar do ato de interrogar, use 5547.
```

### 5545 · amostral

```text
[5545] Processo Penal > Provas em Espécies > Exame de Corpo de Delito
Escopo: Exame de corpo de delito: obrigatoriedade nas infrações que deixam vestígios, exame direto e indireto, suprimento pela prova testemunhal, prioridades legais e nulidade pela sua falta.
Inclui: Indispensabilidade do exame nas infrações que deixam vestígios; Confissão não supre a falta do exame; Exame direto e indireto; Suprimento pela prova testemunhal quando desaparecidos os vestígios; Prioridade no exame em violência doméstica, contra criança, adolescente, idoso ou pessoa com deficiência; Exame complementar nas lesões corporais; Ausência do exame como causa de nulidade
Não inclui: Perícias em geral: perito oficial, assistente técnico, quesitos e laudo → 5546; Preservação e rastreamento dos vestígios → 5544; Classificação das lesões corporais no Código Penal → 5077; Incidente de insanidade mental → 5497; Nulidades em espécie em geral → 5511
Âncoras legais: CPP, art. 158; CPP, art. 167; CPP, art. 168; CPP, art. 564, III, "b"
Desempate: Escolha este nó quando a questão tratar da obrigatoriedade ou do suprimento do exame de corpo de delito; regras gerais sobre peritos e laudos vão para 5546.
```

### 5547 · amostral

```text
[5547] Processo Penal > Provas em Espécies > Interrogatório Judicial
Escopo: Interrogatório judicial do acusado: natureza de meio de defesa e de prova, momento, presença do defensor, entrevista reservada, videoconferência, direito ao silêncio e procedimento em duas partes.
Inclui: Natureza jurídica: meio de defesa e meio de prova; Interrogatório como último ato da instrução; Presença obrigatória de defensor e entrevista prévia reservada; Interrogatório por videoconferência e suas hipóteses; Direito ao silêncio e advertência prévia; Divisão em perguntas sobre a pessoa e sobre os fatos; Interrogatório de corréus em separado e reperguntas das partes; Novo interrogatório a qualquer tempo
Não inclui: Valor e espécies da confissão → 5548; Ordem dos atos na audiência de instrução e julgamento → 5535; Interrogatório no plenário do júri → 5528; Princípio do nemo tenetur se detegere em geral → 5582; Oitiva do indiciado no inquérito policial → 5500
Âncoras legais: CPP, arts. 185 a 196; CF, art. 5º, LXIII; CPP, art. 400
Desempate: Escolha este nó quando a questão tratar do ato de interrogar o acusado; se tratar do conteúdo admitido e de seu valor, use 5548.
```

### 5546 · amostral

```text
[5546] Processo Penal > Provas em Espécies > Perícia
Escopo: Perícias em geral no processo penal: perito oficial e não oficial, assistente técnico, quesitos, laudo, prazos, divergência entre peritos e perícias específicas (necropsia, exumação, local, grafotécnico, laboratoriais).
Inclui: Perito oficial único e dois peritos não oficiais; Assistente técnico e formulação de quesitos pelas partes; Laudo pericial, prazo e divergência entre peritos; Liberdade do juiz para aceitar ou rejeitar o laudo; Autópsia, exumação e exame de local; Exame grafotécnico e perícias laboratoriais; Perícia por precatória
Não inclui: Obrigatoriedade do exame de corpo de delito e seu suprimento → 5545; Cadeia de custódia dos vestígios → 5544; Incidente de insanidade mental do acusado → 5497; Crime de falsa perícia → 5081; Identificação criminal e perfil genético → 4699
Âncoras legais: CPP, arts. 159 a 184
Desempate: Escolha este nó para regras gerais de peritos, quesitos e laudos; se a questão tratar da indispensabilidade do exame nas infrações que deixam vestígios, use 5545.
```

### 5551 · amostral

```text
[5551] Processo Penal > Provas em Espécies > Reconhecimento de Pessoas e Coisas
Escopo: Reconhecimento de pessoas e coisas: procedimento do art. 226 do CPP, natureza vinculante das formalidades segundo a jurisprudência, reconhecimento fotográfico, reconhecimento de objetos e valor probatório.
Inclui: Etapas do reconhecimento pessoal: descrição prévia, colocação ao lado de pessoas semelhantes, auto pormenorizado; Formalidades do art. 226 como garantia mínima e não mera recomendação (STJ); Reconhecimento fotográfico e seu valor; Reconhecimento em juízo e no inquérito; Reconhecimento de objetos; Reconhecimento por várias pessoas feito separadamente; Falsas memórias e risco de erro judicial
Não inclui: Prova testemunhal em geral → 5550; Declarações da vítima → 5549; Identificação criminal datiloscópica e fotográfica → 4699; Acareação → 5552; Nulidade da prova por violação de forma legal em geral → 5594
Âncoras legais: CPP, arts. 226 a 228
Desempate: Escolha este nó quando a questão tratar da identificação do autor ou de objeto por vítima ou testemunha; se tratar da identificação civil ou criminal do investigado, use 4699.
```

### 5566 · amostral

```text
[5566] Processo Penal > Recursos em Espécies > Agravo em Execução
Escopo: Agravo em execução: recurso contra decisões do juiz da execução penal (LEP, art. 197). Cobre cabimento, prazo, legitimidade, ausência de efeito suspensivo e aplicação do rito do RESE.
Inclui: Cabimento contra decisões sobre progressão, regressão, remição, livramento condicional, unificação de penas e falta grave; Prazo de 5 dias (Súmula 700 do STF); Processamento pelo rito do recurso em sentido estrito, com juízo de retratação; Ausência de efeito suspensivo, em regra; Legitimidade do MP, do sentenciado e da defesa; Revogação tácita das hipóteses do art. 581 do CPP que tratam de matéria de execução
Não inclui: Direitos, deveres, faltas e regimes da execução penal em si, sem foco no recurso → 4703; Recurso contra decisões do juiz do processo de conhecimento listadas no art. 581 do CPP → 5561; Habeas corpus impetrado contra ato do juízo da execução → 5477; Requisitos materiais do livramento condicional → 5208
Âncoras legais: Lei 7.210/1984, art. 197; Súmula 700 do STF; CPP, arts. 581 a 592
Desempate: Use este nó quando a decisão impugnada for do juízo da execução penal; se a questão tratar só do direito executório, sem o recurso, use 4703.
```

### 5567 · amostral

```text
[5567] Processo Penal > Recursos em Espécies > Carta Testemunhavel
Escopo: Carta testemunhável: recurso contra a decisão que denega o RESE ou o agravo em execução, ou que obsta seu seguimento ao tribunal (CPP, arts. 639 a 646).
Inclui: Cabimento contra a denegação do recurso em sentido estrito ou contra o obstáculo ao seu seguimento; Uso contra a denegação de agravo em execução; Prazo de 48 horas e requerimento ao escrivão; Ausência de efeito suspensivo (art. 646 do CPP); Possibilidade de o tribunal julgar desde logo o mérito do recurso denegado; Caráter residual: não cabe contra a denegação da apelação, que comporta RESE
Não inclui: Denegação da apelação, impugnável por RESE (art. 581, XV, do CPP) → 5561; Correção de erro ou abuso que tumultua o processo → 5568; Inadmissão de REsp ou de RE na origem (agravo do art. 1.042 do CPC) → 5571
Âncoras legais: CPP, arts. 639 a 646
Desempate: Use este nó quando o recurso denegado for RESE ou agravo em execução; se for apelação denegada, use 5561.
```

### 5564 · amostral

```text
[5564] Processo Penal > Recursos em Espécies > Embargos Infringentes
Escopo: Embargos infringentes e de nulidade: recurso exclusivo da defesa contra acórdão de segunda instância não unânime desfavorável ao réu em apelação, RESE ou agravo em execução (CPP, art. 609, parágrafo único).
Inclui: Exclusividade da defesa; Pressuposto de decisão não unânime e desfavorável ao réu; Limitação à matéria objeto da divergência; Prazo de 10 dias a contar da publicação do acórdão; Distinção entre embargos infringentes (mérito) e de nulidade (matéria processual); Cabimento em apelação, RESE e agravo em execução, mas não em habeas corpus nem em revisão criminal
Não inclui: Aclaramento de omissão, contradição, obscuridade ou ambiguidade → 5565; Recurso contra a sentença de primeiro grau → 5562; Recursos contra acórdão de turma recursal do JECrim → 5569
Âncoras legais: CPP, art. 609, parágrafo único
Desempate: Use este nó se houver voto vencido favorável ao réu em julgamento colegiado de segundo grau; se o vício for omissão ou contradição, use 5565.
```

### 5563 · amostral

```text
[5563] Processo Penal > Recursos em Espécies > Protesto por novo Júri
Escopo: Protesto por novo júri: antigo recurso exclusivo da defesa contra condenação a pena igual ou superior a 20 anos por um único crime no Júri (antigos arts. 607 e 608 do CPP), revogado pela Lei 11.689/2008.
Inclui: Requisitos históricos: pena igual ou superior a 20 anos por um único crime; Exclusividade da defesa e uso por uma única vez; Revogação pela Lei 11.689/2008; Direito intertemporal: cabimento para fatos anteriores e julgamentos posteriores à revogação, conforme a jurisprudência; Inexistência atual do recurso no CPP
Não inclui: Regras gerais de aplicação da lei processual no tempo (tempus regit actum) → 5507; Apelação contra decisão do Júri contrária à prova dos autos → 5562; Sessão de julgamento e quesitação do Júri → 5528
Âncoras legais: Lei 11.689/2008
Desempate: Use este nó sempre que a questão mencionar o protesto por novo júri, inclusive sobre sua revogação; use 5507 só para a regra geral de direito intertemporal processual.
```

### 5589 · amostral

```text
[5589] Processo Penal > Teoria Geral das Prisões > Audiência de Custódia
Escopo: Apresentação do preso, sem demora, ao juiz: fundamento convencional e legal, prazo de 24 horas, finalidades, participantes, objeto da audiência, decisões possíveis e consequências da não realização.
Inclui: Previsão na CADH (art. 7.5) e no art. 310 do CPP, com a redação do Pacote Anticrime; Prazo de 24 horas após a prisão e presença do MP e da defesa; Finalidades: controlar a legalidade da prisão e coibir tortura e maus-tratos; Vedação de perguntas sobre o mérito da imputação; Cabimento também na prisão preventiva ou temporária por mandado, e não só no flagrante; Consequências da não realização no prazo (art. 310, §§ 3º e 4º) e uso de videoconferência; Resolução CNJ 213/2015 e ADPF 347
Não inclui: Requisitos, espécies e lavratura do auto de prisão em flagrante → 5518; Relaxamento da prisão ilegal como providência em si (art. 310, I) → 5588; Concessão de liberdade provisória com ou sem fiança → 5523; Conversão do flagrante em preventiva e requisitos do art. 312 → 5519; Atribuições do juiz das garantias na fase investigatória → 5503
Âncoras legais: CPP, art. 310; CPP, art. 287; Convenção Americana sobre Direitos Humanos, art. 7.5; Resolução CNJ 213/2015
Desempate: Escolha este nó quando a questão tratar do ato da audiência (prazo, finalidade, participantes, objeto, não realização). Se o foco for o conteúdo da decisão tomada nela (relaxar, converter em preventiva, conceder liberdade provisória), use o nó específico dessa medida.
```

### 5586 · amostral

```text
[5586] Processo Penal > Teoria Geral das Prisões > Imunidades Prisionais e Prisões Especiais
Escopo: Pessoas que não podem ser presas, ou só podem ser presas em certas hipóteses (imunidades prisionais), e o direito à prisão especial ou em sala de Estado-Maior antes do trânsito em julgado.
Inclui: Imunidade do Presidente da República à prisão nas infrações comuns enquanto não houver sentença condenatória; Parlamentares: prisão só em flagrante de crime inafiançável, com deliberação da Casa; Magistrados e membros do MP: prisão só por ordem do tribunal competente ou em flagrante de crime inafiançável; Advogados: sala de Estado-Maior e prisão em flagrante por crime no exercício da profissão; Diplomatas (Convenção de Viena) e restrições à prisão de eleitores e candidatos em período eleitoral; Vedação do flagrante nas infrações de menor potencial ofensivo com compromisso de comparecimento, no condutor que socorre a vítima e no usuário de drogas; Prisão especial do art. 295 do CPP: beneficiários, características e cessação com o trânsito em julgado
Não inclui: Foro por prerrogativa de função e competência originária → 5484; Hipóteses e espécies de flagrante → 5518; Prisão domiciliar como substituta da preventiva → 5521; Termo circunstanciado e procedimento dos Juizados Especiais Criminais → 4701; Tratamento penal do porte de droga para consumo → 4708
Âncoras legais: CF, art. 53, § 2º; CF, art. 27, § 1º; CF, art. 86, § 3º; CPP, art. 295; LC 35/1979, art. 33, II; Lei 8.625/1993, art. 40, III; Lei 8.906/1994, art. 7º, IV e V; Lei 9.099/1995, art. 69, parágrafo único; CTB, art. 301; Lei 11.343/2006, art. 48, § 2º; Código Eleitoral, art. 236
Desempate: Escolha este nó quando a questão perguntar se determinada pessoa pode ser presa ou onde deve ficar recolhida; se o foco for o tribunal competente para processá-la, use 5484.
```

### 5591 · amostral

```text
[5591] Processo Penal > Teoria Geral das Provas > Finalidade, Sujeitos e Ônus da Prova
Escopo: Finalidade da prova (convencimento do juiz), seu objeto e o que dispensa prova, conceitos de fonte, meio e destinatário, sujeitos da prova e distribuição do ônus da prova no processo penal, inclusive a iniciativa probatória do juiz.
Inclui: Finalidade e destinatário da prova; distinção entre fonte, meio e objeto de prova; Fatos que independem de prova: notórios, axiomáticos, inúteis e presunções legais; Ônus da prova: cabe a quem alega (acusação: autoria, materialidade e dolo; defesa: excludentes alegadas); In dubio pro reo como regra de julgamento ligada ao ônus probatório; Iniciativa probatória do juiz: produção antecipada de provas urgentes e diligências de ofício (art. 156, I e II); Vedação à substituição da atuação probatória da acusação pelo juiz (art. 3º-A); Sujeitos da prova e prova de direito (direito estrangeiro, estadual, municipal e costumeiro)
Não inclui: Princípios da comunhão da prova, da liberdade probatória e do nemo tenetur se detegere → 5595; Livre convencimento motivado e valor dos elementos do inquérito (art. 155) → 5592; Presunção de inocência como princípio geral do processo → 5582; Sistema acusatório e inquisitivo em geral → 5581; Absolvição por insuficiência de provas como espécie de sentença → 5574
Âncoras legais: CPP, art. 156; CPP, art. 3º-A; CPP, art. 386, VII
Desempate: Use este nó quando a questão tratar de quem deve provar, do que precisa ser provado ou dos poderes instrutórios do juiz; se tratar de como o juiz valora a prova, use 5592.
```

### 5592 · amostral

```text
[5592] Processo Penal > Teoria Geral das Provas > Sistemas de Avaliação da Prova
Escopo: Sistemas de apreciação da prova pelo juiz: íntima convicção, prova legal ou tarifada e livre convencimento motivado (persuasão racional), com seus reflexos no CPP, inclusive o valor dos elementos do inquérito.
Inclui: Sistema da íntima convicção e sua aplicação aos jurados do Tribunal do Júri; Sistema da prova legal ou tarifada e seus resquícios no CPP (prova do estado das pessoas, exame de corpo de delito); Livre convencimento motivado ou persuasão racional como regra (art. 155 e CF, art. 93, IX); Vedação de condenar exclusivamente com base em elementos informativos do inquérito, ressalvadas provas cautelares, não repetíveis e antecipadas; Ausência de hierarquia entre provas; juiz não fica adstrito ao laudo pericial (art. 182); Standards probatórios e valoração da prova
Não inclui: Distribuição do ônus da prova e poderes instrutórios do juiz → 5591; Valor da confissão e sua retratabilidade → 5548; Obrigatoriedade do exame de corpo de delito nos crimes que deixam vestígios → 5545; Quesitação e votação dos jurados na sessão de julgamento → 5528; Requisitos e fundamentação da sentença condenatória → 5575
Âncoras legais: CPP, art. 155; CPP, art. 182; CF, art. 93, IX
Desempate: Use este nó quando a questão tratar de como o juiz valora a prova e do sistema adotado; se tratar do valor de um meio de prova específico (confissão, perícia), prefira o nó desse meio de prova.
```
