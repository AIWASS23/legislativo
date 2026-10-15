# Decisões tomadas à mão

O enunciado pede: "Se alguma decisão foi tomada à mão, registre qual e por quê." Este arquivo
lista todas elas. Cada decisão que afeta o pipeline está num arquivo de dados versionado
(`dados/temas/`), lido pelo código e conferido por checagens automáticas a cada
`uv run python executar_preparacao.py`.

Última atualização: 15/10/2026.

---

## D1. Convenção dos nós duplicados (15/10/2026)

**Contexto.** A árvore tem 20 nós "fantasmas": ativos, sem descrição e sem histórico de
questões.
- 8 copiam temas de Legislação Especial em outra disciplina: LEP, Maria da Penha, Drogas,
  Organizações Criminosas, Lavagem, Abuso de Autoridade, Idoso e Meio Ambiente.
- 12 são variantes na mesma disciplina: "(Parte N)" e "Provas em Espécie" × "Provas em Espécies".

A régua conta como erro publicar num nó quando o especialista usou o outro. Perguntamos à
equipe da Vício qual nó vale; a resposta foi que **fica a critério do candidato**.

**Decisão.**
- **Vale o nó com histórico:** o de Legislação Especial, ou o tema sem o sufixo "(Parte N)".
- **Os fantasmas nunca são tema central:** ficam fora da lista de IDs que os modelos podem escolher.
- **As questões do assunto são publicadas no nó canônico.** Não vão para revisão só por
  estarem nessa zona.

**Por quê.**
- **Histórico:** os nós de Legislação Especial têm questões no sistema antigo (LEP 230,
  Drogas 116, Lavagem 46, Abuso 34...); as cópias têm zero.
- **Sinais de criação recente:** as cópias não têm descrição e têm os IDs mais altos da árvore.
- **Origem na importação:** 26 questões têm assunto de origem idêntico ao título de um
  fantasma, sinal de que esses nós vieram da importação do site de origem, não da curadoria.
- **Custo de revisar tudo:** mandar toda a zona para revisão custaria até 23% da cobertura
  (teto de 83 questões expostas), por um risco que as evidências indicam ser pequeno.

**Como o risco é tratado.**
- Nosso gold é rotulado com a nossa convenção, então ele não mede esse risco.
- Cada nó publicável recebe um tipo de risco de convenção (`tipo_convencao` em
  `dados/preparados/temas.json`):

| Tipo | Nós | Exemplo |
|---|---|---|
| Cópia em outra disciplina | 8 | LEP em Legislação Especial (cópia em Processo Penal) |
| Sobreposição entre nós válidos | 35 | Ação Penal em Penal e em Processo Penal |
| Cópia "(Parte N)" na mesma disciplina (vale também para os subtemas do canônico) | 71 | Furto, filho de "Dos Crimes Contra o Patrimônio" |

- A previsão de precisão desconta uma margem de convenção proporcional às publicadas em
  cada tipo (ADR-013).

**Arquivos:** mapeamento automático fantasma → canônico (`saidas/eda/tabelas/13_01_fantasmas.csv`),
adotado sem alteração.

---

## D2. Regra de desempate das sobreposições (15/10/2026)

**Contexto.** Alguns assuntos têm dois nós válidos em disciplinas (ou ramos) diferentes. O
principal é "Ação Penal", em Penal (5063) e em Processo Penal (5466): 67 questões têm assunto
de origem que bate com os dois.

**Decisão.** Seis grupos com regra de desempate, em `dados/temas/sobreposicoes.csv`. Os
subtemas herdam a regra do tema.

| Grupo | Nós | Regra |
|---|---|---|
| acao_penal | 5063 × 5466 (+ 5198 Decadência) | Regras do CP (arts. 100–106, espécies, representação, renúncia, perdão, perempção; decadência como extinção da punibilidade) → Penal; denúncia, queixa, prazos, requisitos, condições da ação (CPP, arts. 24–62) → Processo Penal |
| interceptacao | 4700 × 5555 | A Lei 9.296/96 como lei → Legislação Especial; interceptação como meio de prova → Processo Penal |
| juizados | 4701 × 5539 | A Lei 9.099/95 em visão geral → Legislação Especial; o rito sumaríssimo, a transação e a suspensão condicional → Processo Penal |
| pena | 5200 × 4384 | Conceito e finalidade da pena no CP → Penal; teorias que justificam a pena → Criminologia |
| sentenca | 5572 × 5537 | Sentença em geral (efeitos, correlação, emendatio/mutatio) → Sentença Penal; sentença como ato do rito ordinário → Procedimento Ordinário |
| orcrim_meios_prova | 4705 × 5557, 5558, 5559 | A Lei 12.850/13 em visão geral → Legislação Especial; colaboração premiada, ação controlada e infiltração como meios de prova → Processo Penal |

Se a regra não resolver (os classificadores divergem entre os nós do grupo), a questão vai
para `revisar` com o motivo "sobreposição" (ADR-011).

**Por quê.** São escopos que se sobrepõem de verdade (lado material × processual). A regra
torna a escolha explicável ao professor e reprodutível. As regras serão refinadas nos
cartões de tema (ADR-007).

---

## D3. Lista de lixeiras em dois níveis (15/10/2026)

**Contexto.** A EDA apontou 21 nós suspeitos de "lixeira": concentram questões que não são
deles, ou têm título genérico com muitas questões. A heurística tem falsos positivos.

**Decisão** (revisão manual; arquivo `dados/temas/lixeiras.csv`):
- **Forte (11):** 5171, 5581, 5582, 5467, 5585, 5499, 5200, 5088, 5212, 5595, 5117.
  - Publicar só com concordância total entre os classificadores e o verificador a favor.
  - Na árvore enviada aos modelos, levam a marca `[conceitual]`: usar só se a questão for
    sobre o conceito geral.
- **Moderada (7):** 5181, 5507, 5526, 5510, 5540, 5514, 4387. São temas legítimos, mas
  concentrados demais; entram só como variável de risco na calibração, sem regra dura.
- **Fora da lista (3):** 5150 Homicídio (é só muito cobrado), 5064 Ação Penal Pública (o
  problema dela é a sobreposição, tratada em D2) e 5172 Princípios do Direito Penal
  (concentração normal).

**Por quê.** Os dois níveis protegem a régua onde a lixeira é óbvia (títulos introdutórios
que absorvem centenas de questões), sem derrubar cobertura em temas reais que só são muito
cobrados. A justificativa de cada nó está no CSV.

---

## D4. Títulos corrigidos para exibição (15/10/2026)

**Decisão.** Nove títulos com erro aparecem corrigidos nos prompts e relatórios; **o ID não
muda** (`dados/temas/correcoes_titulo.csv`): Crimonológicas, Legitimidoras, Estaturo de Idoso,
Falso Testemunha, Crimescontra, Comeptência, Caractéristas e os dois títulos que começam com
número ("12 Disposições...", "2 Oferecimento...").

**Por quê.** Erros de digitação atrapalham o modelo e quem lê. A correção é só de exibição,
para não alterar a avaliação, que usa os IDs. Uma checagem confere que o título original
registrado continua igual ao do `temas.csv`.

---

## D5. Conferência manual do texto canônico (15/10/2026)

**Decisão.** Uma amostra de 10 questões foi lida à mão (`saidas/preparacao/conferencia_texto_canonico.md`).

**Resultado.** Três defeitos corrigidos no código, que viraram regra ou checagem:
1. "\n" e "\t" gravados como texto no banco (106 questões);
2. comando copiado no fim do enunciado (72);
3. frases-padrão de prova contadas como conteúdo.

**Por quê.** As checagens automáticas da primeira versão não pegavam esses casos.
