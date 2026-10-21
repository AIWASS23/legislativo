# Decisões tomadas à mão

O enunciado pede: "Se alguma decisão foi tomada à mão, registre qual e por quê." Este arquivo
lista todas elas. Cada decisão que afeta o pipeline está num arquivo de dados versionado
(`dados/temas/`), lido pelo código e conferido por checagens automáticas a cada
`uv run python executar_preparacao.py`.

Última atualização: 21/10/2026.

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

---

## D6. Gold set: sorteio e protocolo de rotulagem (15/10/2026)

**Contexto.** O case não traz questões rotuladas, e a previsão de precisão é avaliada. Só
rótulos feitos à mão, sem ver a saída dos modelos, medem acerto em vez de concordância
(ADR-012).

**Decisão: sorteio.**
- **60 questões**, estratificadas por disciplina de origem normalizada × formato, com alocação
  proporcional pelo método do maior resto e **semente 20261015** (`ParametrosGold` em
  `vicio_ia/configuracao.py`).
  - 14 estratos; 12 recebem questões. Os 2 estratos com uma questão só na população
    (Criminologia com 4 alternativas; fora do recorte de certo/errado) ficam sem sorteio.
  - Probabilidade de inclusão de ~0,17 em todos os estratos sorteados; o peso de cada
    questão nas estimativas é o inverso dela.
  - Ordem de rotulagem embaralhada, para não rotular estrato por estrato.
  - Duplicatas exatas ficariam fora do sorteio e herdariam o rótulo (hoje não há nenhuma).

**Decisão: protocolo de rotulagem.**
- **Rótulo cego:** quem rotula vê só o texto canônico. Nada de saída de modelo, nem de
  disciplina ou assunto de origem (ADR-006).
- **Fontes permitidas:** texto da lei, árvore e cartões de tema. Um LLM pode explicar o
  conteúdo jurídico, mas **nunca ser perguntado sobre o tema**; quando usado, fica registrado
  na coluna `observacao`.
- **Critérios:**
  - `tema_id` é o nó mais específico em que há segurança;
  - na dúvida entre subtemas, vale o pai, com os filhos plausíveis em `alternativos`;
  - `fora` quando nenhum tema do recorte serve;
  - `multitema` quando a questão cobre mais de um tema por igual;
  - certeza alta, média ou baixa.
- **Convenção dos duplicados:** a mesma de D1. A validação recusa nó fantasma e indica o canônico.
- **O gold não decide nada:** o `publicacao.csv` sai só do pipeline. Os rótulos medem a
  precisão e calibram a confiança.
- **Tempo gasto:** medido por questão na coluna `minutos` quando se usa o rotulador interativo.
- **Rotulagem concluída em 15/10:** as 60 questões foram rotuladas à mão pelo autor, direto na planilha
  (fora do rotulador interativo, por isso sem tempo por questão), e gravadas às 09:28. **Tempo total
  informado pelo autor: 3 horas** (~3 minutos por questão), dentro da estimativa de 2 a 3 minutos da ADR-012. Resultado: 0 fora, 12 multitema, 30 com alternativos, 45 com certeza alta e 15 média.

**Por quê.**
- Estratificar pela origem e pelo formato espalha a amostra pelos tipos de questão sem usar
  nenhuma saída de modelo.
- A semente fixa torna o sorteio reprodutível e auditável.
- Esconder os rótulos de origem evita que o gold herde os erros deles.

**Arquivos:** `dados/gold/amostra_leva1.csv` (sorteio), `rotulos_leva1.csv` (rótulos; o código
nunca sobrescreve uma linha preenchida), `caderno_leva1.md` (questões na ordem de rotulagem).

---

## D7. Cartões de tema: modelo fixo e revisão (15/10/2026)

**Decisão.**
- Os 351 cartões foram rascunhados pelo Claude Opus 5.5 (CLI `claude`), em 58 chamadas, uma por tema pai (ADR-007).
- O modelo dos cartões ficou **fixo** (`ParametrosCartoes`), em vez de seguir o papel de verificador.
  Assim, trocar o verificador não invalida no cache os rascunhos já gerados.
- Correções manuais vão em `dados/temas/cartoes_ajustes.csv` e são aplicadas sobre os rascunhos a cada
  execução. Até agora: **nenhum ajuste**; a revisão das prioridades 1 a 3
  (`saidas/cartoes/revisao_cartoes.md`) está pendente.

**Por quê.** Os cartões são o material que o professor valida (memo). O rascunho por LLM cobre os 351
nós no prazo; a revisão humana se concentra onde a régua pune: lixeiras, sobreposições e irmãos parecidos.

---

## D8. Modelos por papel fora da cota do Claude Code (15/10/2026)

**Contexto.** A CLI `claude` divide a cota com a sessão de trabalho. Numa rodada dos cartões a cota
acabou e 35 chamadas falharam. O modelo local (`qwen3.5:4b`) gera ~2 tokens/s nesta GPU: ~34 s por
questão e ~3,4 h por rodada.

**Decisão** (`config/escolha_modelos.json`, modo manual):

| Papel | Modelo |
|---|---|
| Classificador A | GPT `gpt-6.1-sol` pela CLI `codex` (assinatura do ChatGPT) |
| Classificador B | Gemini 3.8 Flash `-low` pela CLI `agy` |
| Voto barato | GPT-OSS 120B `-medium` pela CLI `agy` |
| Verificador | Gemini 3.8 Flash `-medium` pela CLI `agy` (até 15/10 às 15h: Claude Opus 5.5 `-medium`) |

**Por quê.** Nenhum papel gasta a cota do Claude Code. O voto barato é um modelo aberto,
equivalente ao que rodaria auto-hospedado em produção (ADR-016).

**Troca do verificador (15/10, ~15h20, decisão do autor).** No `agy`, Claude e GPT-OSS dividem uma
cota, que acabou depois de ~120 chamadas e volta ~19h. O verificador passou para o Gemini 3.8 Flash
`-medium`, que tem cota própria e leva ~30 s por verificação. **Risco aceito:** é a mesma família do
classificador B, então um erro de B tende a passar pelo verificador. O E3 mede o quanto A e B erram
juntos, e a calibração aprende o peso do veredito no gold.
**Risco:** cada assinatura tem limite próprio. O do `codex` acabou às 15h de 15/10 (volta às 18:57),
com 85 das 359 questões classificadas por A, entre elas as 60 do gold. As chamadas que faltam são
refeitas na execução seguinte; o resto vem do cache.

---

## D9. Regras de decisão definidas na implementação (15/10/2026)

**Decisão** (código em `vicio_ia/decisao/` e `vicio_ia/avaliacao/previsao.py`):
1. **Verificador escolhe um irmão do candidato:** recuo para o pai, quando ele é publicável (ADR-010:
   as fontes concordam no ramo, mas divergem entre os filhos). Se o verificador escolhe outro ramo,
   a questão vai para `revisar`.
2. **Verificador escolhe um filho do candidato:** publica-se o candidato e o filho vai para `extras_ids`.
   O candidato está certo pela régua tanto se o especialista escolheu ele quanto se escolheu o filho.
3. **O verificador não sabe qual é o candidato** e não recebe o voto barato entre as sugestões, para o
   prompt dele não depender da ordem em que as respostas chegam.
4. **Confiança de `fora`:** a confiança do verificador em "nenhum" (o gold não tem nenhuma
   questão `fora` para calibrar).
5. **Ponto da previsão:** já desconta a margem de convenção (perda esperada pelas taxas supostas).
   O limite inferior do intervalo desconta também a margem de ambiguidade; o critério do limiar, não
   (ADR-011; corrigido em 16/10).
6. **Calibração:** regressão logística L2 implementada com `numpy` (IRLS). O `scikit-learn` não tem
   tipos, e o padrão do projeto exige `mypy --strict`. O modelo é o mesmo da ADR-013.
7. **Intervalo do bootstrap:** o limiar fica fixo nas reamostras (a calibração é reajustada, o conjunto
   publicado não). Refazer o limiar em cada reamostra exigiria um bootstrap aninhado.

---

## D10. Calibração por faixas e chance efetiva (16/10/2026)

**Contexto.** Na primeira prévia do passo 07 (15/10), nada foi publicado:
- a regressão logística de 7 variáveis mal superou um palpite constante. São só 6 erros em 60
  questões, então ela puxou todas as probabilidades para ~0,92;
- a margem de ambiguidade estava, por engano, também no critério do limiar.

**Decisão.**
1. **Calibração por faixas**, a alternativa prevista na ADR-013. A taxa de acerto observada em cada faixa
   de sinais, com suavização de Jeffreys:

   | Faixa | Quando | Gold | P |
   |---|---|---|---|
   | consenso total | verificador confirma; A, B e voto barato no ramo | 28/28 | 0,983 |
   | confirma parcial | verificador confirma; alguma fonte discorda | 19/22 | 0,848 |
   | verificador vizinho | verificador escolheu pai, filho ou irmão | 2/2 | 0,833 |
   | outros | revisões forçadas, falhas | 5/8 | 0,611 |

   O pipeline escolhe, pela menor log-loss na validação cruzada, entre as faixas e a regressão (grade de
   penalidades). As faixas venceram: 0,287 contra 0,312. A incerteza vem de sorteios da Beta de cada faixa:
   o bootstrap comum diria que 28 em 28 é "100% sem variação".
2. **Chance efetiva** = P × (1 − taxa suposta de convenção do nó: 20%, 10% ou 3%). É ela que ordena as
   candidatas e vai para a coluna `confianca`. Sem isso, as poucas questões em nós com cópia em outra
   disciplina (taxa suposta de 20%) barravam a faixa inteira. Margem de convenção da faixa de consenso:
   0,057.
3. **O corte só cai entre valores diferentes de P**, nunca no meio de uma faixa (que escolheria questões
   de forma arbitrária).
4. **Pesos amostrais nas faixas** (tamanho efetivo de Kish), para a taxa continuar correta se os
   estratos do gold tiverem probabilidades de inclusão diferentes.

**Por quê.**
- Com 6 erros no gold, um modelo de 7 variáveis não tem como aprender, e faixas são auditáveis.
- O E5 mostrou que a autoconfiança dos modelos não separa erros: eles declaram 0,99 em respostas erradas.
  O que separa é a concordância entre fontes independentes.

**Limite assumido.** O gold tem 60 questões e 6 erros (régua estrita). Na faixa de consenso total, 28
acertos em 28 dão percentil 10 de 0,953, o que certifica 95% só nos nós sem risco de convenção. As
questões de consenso em nós "(Parte N)" (chance efetiva de 0,953, percentil 10 de ~0,92) vão para revisão.
A previsão foi calibrada e conferida no mesmo gold, com validação cruzada; não houve teste numa amostra
independente, e o `previsao.txt` e o relatório dizem isso.

---

## D11. Congelamento antes da rodada final (16/10/2026, 13:02)

**Decisão do autor:** congelar o pipeline antes de completar a classificação e de gerar os entregáveis.

**O que ficou congelado** (`saidas/experimentos/congelamento.json`): 34 arquivos com impressão digital
(SHA-256).
- Os 6 prompts, as árvores e os cartões.
- As decisões manuais da árvore.
- A escolha de modelos por papel.
- O código de classificação, decisão e calibração, e a configuração.

A partir daqui, nada disso muda. O passo 07 avisa se algo mudar.

**Cartões sem revisão manual.** Ficam como os rascunhos do modelo (D7). A revisão das zonas de risco não
coube antes do congelamento. Mudar o escopo de um cartão refaria as 359 chamadas do classificador A,
inviável com a cota.

**Recongelamentos (17/10), todos sem efeito nas decisões e registrados em `saidas/experimentos/registro.md`:**
1. Os testes unitários entraram no portão de qualidade (`ParametrosQualidade`), e o texto explicativo do
   `previsao.txt` foi corrigido (calibração por faixas e sorteios da Beta).
2. Foi removido código sem uso. A ordem dos `extras_ids` empatados ficou estável: antes, ela variava entre
   execuções, porque dependia da ordem de iteração de conjuntos. Duas execuções seguidas agora geram o
   mesmo `publicacao.csv`, byte a byte; em relação à execução anterior, só mudou a ordem dos extras de 4
   questões.
3. Só docstrings e mensagens: o gold set passou a ser descrito como uma amostra única.
4. A fórmula do ponto da precisão prevista mudou (D12). As decisões do `publicacao.csv` não mudaram.
5. O `publicacao.csv` e o `previsao.txt` passaram da raiz para `relatorio/`, junto com o relatório. Os dois
   arquivos saem idênticos, byte a byte.

---

## D12. Suavização do estimador direto na precisão prevista (17/10/2026)

**Contexto.** Pela ADR-013, com menos de 40 itens do gold entre as publicadas, o ponto da precisão é a
média do estimador direto com o estimador por modelo. Só 13 questões do gold caíram nas 81 publicadas,
e as 13 estão certas. O direto bruto dava 1,000; com o modelo (0,983), o ponto saía 0,99.

**Decisão do autor.** Aplicar ao estimador direto a mesma suavização de Jeffreys da calibração, no
tamanho efetivo de Kish: `(acertos + 0,5) / (n + 1)`. Para 13 em 13, isso dá 0,964. O ponto passa a ser
(0,964 + 0,983) / 2 = **0,973**, informado como **0,97**.

**Por quê.** Treze acertos em treze não provam 100%. Sem suavização, o direto tratava a amostra pequena
como certeza, enquanto o estimador por modelo já descontava esse tamanho. Com a suavização, os dois
estimadores ficam no mesmo critério, e o ponto fica menos otimista.

**O que não mudou.** O limiar, as 81 publicadas, a coluna `confianca` e o intervalo (0,93–1,00), que vem
dos sorteios da Beta. A mudança foi feita depois do congelamento (D11), com recongelamento registrado.
Ela muda só o número informado, não as decisões.

---

## D13. Etapa 2: anexos novos e conferência das 300 questões novas (20/10/2026)

**Anexos.**
- O autor moveu os anexos para `anexos/1-ENTREGA/` (etapa 1) e `anexos/2-ENTREGA/` (etapa 2).
- `Caminhos` lê a pasta da etapa em vigor (`ETAPA_ATUAL = 2`, em `vicio_ia/configuracao.py`).
- A classificação por LLM, o experimento E4 e o passo 07 da etapa 1 recusam rodar na etapa 2
  (`GuardaEtapa`). Para reproduzir a etapa 1, use a tag `entrega-1`.

**Passo 01 nas 659 questões.**
- As 8 checagens passaram.
- As 359 questões antigas saem idênticas, byte a byte, ao texto canônico da etapa 1.

**Conferência manual de 20 questões novas,** sorteadas com a semente 20261020:
- **Nenhum defeito muda o conteúdo.**
- **Único defeito, cosmético:** quebras de linha no meio da frase, herdadas do HTML (Q0486).
- **As 300 novas não têm comando** (300 vazios), nem enunciado genérico, nem HTML de editor.
- **O assunto de origem das novas é mais específico** (ex.: "Lei do Colarinho Branco - Lei nº 7.492",
  "Desacato").
- **Dez novas são de Direito Penal Militar ou Processual Penal Militar,** e não há nó militar na árvore
  (ADR-023).


## D14. Revisão do mapa de artigos e dos termos propostos (20/10/2026)

**Protocolo** (ADR-020).
- **O que foi revisado:** as propostas do `codex-cli:gpt-6.1-sol` (`executar_enriquecimento.py`; entrada: só a
  árvore e os cartões, nenhuma questão).
- **Fila de 1.680 itens,** em três blocos, na ordem da ADR-020:
  1. as 568 linhas do mapa lei/artigo → tema;
  2. 797 termos de risco: `forte` e `exclui` de lixeiras e sobreposições, e termos fortes propostos para mais de
     um tema;
  3. uma amostra aleatória de 315 termos (10% do restante, semente 20261021), para estimar a taxa de erro do que
     não foi revisado.
- **Critérios:**
  - uma linha do mapa só fica se uma questão que cita o artigo costuma ser daquele tema;
  - um termo `forte` precisa quase definir o tema;
  - num conflito, o termo fica `forte` só no tema dono e vira `fraco` ou `exclui` nos outros.

**Forma de registro.**
- O autor decidiu os 1.680 itens num arquivo de respostas e o passou de uma vez à ferramenta
  (`executar_revisao_conhecimento.py`, pela entrada padrão).
- Por isso todas as decisões em `dados/conhecimento/revisao.csv` têm o mesmo horário (20/10/2026 16:04:52), que
  é o da gravação, não o de cada decisão.
- As decisões são do autor. Nenhum modelo revisou nada.
- **Tempo gasto:** 3 horas.

**Resultado.**

| Bloco | Itens | Aceitos | Corrigidos | Apagados |
|---|---:|---:|---:|---:|
| 1. Mapa de artigos | 568 | 456 | 15 | 97 |
| 2. Termos de risco | 797 | 573 | 224 | 0 |
| 3. Amostra aleatória de termos | 315 | 305 | 10 | 0 |

- **O mapa final tem 471 linhas,** todas revisadas. O modelo errou mais no mapa (20% das linhas mudaram) e nos
  termos de risco (28% corrigidos) do que no resto.
- **Erro estimado nos termos não revisados:** 10 de 315 na amostra, ou 3,2% (intervalo de 95% de Wilson: 1,7%
  a 5,7%). Isso equivale a cerca de 90 dos 2.833 termos que ficaram como rascunho do modelo. Esses termos estão
  marcados com `revisado = nao` em `dados/conhecimento/termos.csv`.
- **Efeito na folha-verdade:** das 14 questões da folha com tema que citam artigo, todos os temas apontados
  pelo mapa acertam pela régua em 5, contra 3 com a proposta (`saidas/etapa2/citacoes.md`). O mapa continua a
  apontar mais de um tema em muitas questões, e por isso entra no ranqueador como candidato e atributo, não
  como regra de publicação.

**Conferência das citações** (`saidas/etapa2/citacoes.md`, 21/10).
- **Amostra:** o autor conferiu os 20 artigos sorteados (semente 20261020), e os 20 estavam certos (lei e
  número).
- **Os 3 pendentes da extração** foram resolvidos à mão em `dados/conhecimento/citacoes_manuais.csv`, aplicado
  pelo `executar_citacoes.py` com a resolução `manual`:
  - Q0190, "arts. 74 e 75 da Lei" e "(art. 76)": Lei 9.099/1995, porque a questão é sobre os Juizados
    Especiais Criminais;
  - Q0592, "artigos 89 a 108": Lei 8.666/1993, os crimes da antiga Lei de Licitações.
- **Resultado:** 209 artigos com a lei resolvida em 94 questões, e nenhum pendente.

## D15. Sistema da etapa 2: regra de publicação e decisões de implementação (21/10/2026)

**Contexto.**
- O sistema sem LLM (`executar_sistema.py`) acerta o nó, fora da amostra, em 81 das 100 questões da folha: 81
  das 92 com tema, e as 8 fora são sempre erro.
- Pelo critério da ADR-025 (percentil 10 da precisão estimada ≥ 95%), só **3** das 559 avaliadas poderiam ser
  publicadas. Com 100 rótulos e 8% de questões fora que nenhum atributo separa (E11b), a incerteza da calibração
  é grande.
- Na folha, 19 das 20 questões de maior confiança fora da amostra estão certas; o único erro é uma questão
  fora, a Q0087.
- Na etapa 1, as 29 questões da folha que o LLM publicou tiveram 27 acertos (93%).

**Decisão do autor.**
- A reserva pontual da etapa 1 passa a ser o critério: publica-se o maior conjunto com ponto do estimador do
  modelo ≥ 97% (`ParametrosSistema.criterio_limiar = "reserva"`).
- O resultado do critério estrito continua no `previsao.txt` e no diagnóstico, para comparação.
- **Estimador direto no ponto:** com menos de 10 questões da folha na faixa publicada, ele não entra
  (`min_direto_parcial`). Com tão poucas, o Jeffreys domina: 1 de 1 daria 0,75.

**Resultado com a logística (primeira versão).**
- **Publicação:** 16 das 559 avaliadas (2,9%), 8 antigas e 8 novas. Ao todo, nas 659, ficaram 17 publicar, 632
  revisar e 10 fora.
- **Previsão:** 0,97 (0,92–1,00), com percentil 10 de 0,94.

**Troca do ranqueador pelo E10** (mesmo dia, registro em `saidas/experimentos/registro.md`).
- **Grade pré-registrada:** a logística e 8 configurações de gradient boosting. Quatro configurações tinham sido
  exploradas antes e estão declaradas no registro.
- **Vencedor pela menor log-loss fora da amostra:** o boosting com profundidade 2, folha ≥ 20 e 200 árvores
  (0,403, contra 0,433 da logística). Ele acerta menos no total (77, contra 81), mas ordena melhor o topo:
  - 48 certas entre as 50 de maior confiança, contra 45;
  - só uma questão fora no topo, contra três.
- **Calibração:** com o boosting, vence o Platt (log-loss de 0,393).
- **Resultado com a mesma regra (reserva de 97%):**
  - **97** das 559 publicadas (17,4%): 30 antigas (12%) e 67 novas (22%);
  - nas 659: 120 publicar, 529 revisar e 10 fora;
  - previsão de **0,95 (0,90–0,99)**: o modelo dá 0,970, e a folha na faixa tem 22 certas em 23 (direto de
    0,938, com Jeffreys);
  - pelo critério estrito seriam 48 publicadas, com previsão informada de 0,92, porque só 10 questões da folha
    cairiam na faixa.
- **Decisão do autor:** manter o boosting com a reserva de 97% na entrega (as alternativas eram cortar mais alto,
  com cerca de 40 publicadas, ou voltar à logística, com 16).

**Por quê.**
- O critério estrito protege a régua, mas publica quase nada.
- O ponto de 95% (cerca de 90 publicadas) teria uma chance alta de ficar abaixo de 95%.
- A reserva de 97% deixa folga e mantém o risco baixo.

**Decisões de implementação** (registradas aqui porque ajustam as ADR-022, ADR-023 e ADR-025):
1. **Rótulo do par pela régua.** Um par é positivo se publicar o tema estaria certo pela régua, então a
   logística estima direto P(certo | nó).
   - Os pais dos subtemas candidatos também são candidatos, e por isso o recuo para o pai sai de graça.
   - Isso substitui a soma `Σ P(t)` da ADR-022, com o mesmo efeito.
2. **Penalidade L2 fixa em 10.** As penalidades 1 e 100 foram medidas como sensibilidade:
   - acerto fora da amostra de 78, 81 e 79 em 100;
   - log-loss de 0,438, 0,433 e 0,450.
3. **As 559 são previstas pela média dos 50 modelos da validação cruzada,** os mesmos que preveem a folha fora da
   amostra.
   - Assim a P das avaliadas fica na mesma escala da P em que a calibração foi medida.
   - O modelo treinado com as 100 dava P mais alta (mediana de 0,856, contra 0,820 na folha).
4. **Calibração:** identidade, Platt, ou Platt com a faixa de concordância entre o denso e o BM25 (ADR-025).
   - A identidade venceu pela log-loss fora da amostra: 0,433, contra 0,465 do Platt e 0,473 do Platt com
     concordância.
   - Os sorteios da incerteza refazem a calibração por Platt em cada bootstrap da folha.
5. **Estimador direto fora do critério do limiar,** como na etapa 1. O critério usa só os sorteios do estimador
   do modelo; o direto entra no ponto (D12).
6. **Direito militar vai sempre para `fora`,** mesmo com regra forte. É mais estrito que a ADR-023, porque a árvore
   não tem nenhum nó militar.
7. **Tema inativo:** com a proximidade acima do percentil 90 das questões com tema da folha (−0,100), a questão
   vai para `revisar`. Atingiu 95 das 659 questões.
8. **Não feito por falta de prazo:** a soma ponderada sem treino (a referência original do E10, que foi feito
   como logística contra boosting) e o desconto de convenção por tipo de nó (ADR-025, item 3). Os desvios de
   convenção da folha já aparecem como erros fora da amostra.

## D16. Exemplos sintéticos por tema no ranqueador (21/10/2026)

**O que foi feito.**
- O LLM (`codex-cli:gpt-6.1-sol`, `executar_exemplos.py`) propôs 3 questões-modelo para cada tema publicável, só a
  partir da árvore e dos cartões, sem nenhuma questão real.
- Elas estão em `dados/conhecimento/exemplos_sinteticos.jsonl`, com a proveniência no manifesto.
- Os vetores entram como dois atributos do ranqueador: a similaridade com os exemplos do tema e com os do ramo,
  relativas ao melhor exemplo.

**Por quê.** O experimento E13, pré-registrado, mostrou ganho fora da amostra na folha:
- log-loss de 0,363, contra 0,403;
- 82 nós certos, contra 77;
- topo igual.

No sistema inteiro, a cobertura nas 559 passou de 97 para 127 publicadas, com previsão de 0,96 (0,91–0,99).

**Revisão.**
- Os exemplos são rascunho do modelo; o enunciado permite exemplos propostos por LLM revisados pelo autor.
- **Amostra para a conferência do autor:** 30 exemplos sorteados (semente 20261021), em
  `dados/conhecimento/revisao_exemplos.csv`.
- **Conferência da amostra, feita pelo assistente (LLM), não pelo autor:** 30 de 30 cobrem o tema indicado. Os
  dispositivos citados que foram conferidos estão corretos. Há duas ressalvas menores, anotadas no CSV: uma questão
  sobre a redação histórica do art. 350 do CP, que é o próprio nó, e uma sobre compromisso de ajustamento de
  conduta, coerente com o nó "Inquérito Civil".
- **Revisão do autor (21/10):** o autor revisou a conferência do assistente e a aceitou: 30 de 30 cobrem o tema. Os
  1.023 exemplos fora da amostra continuam como rascunho do modelo, como registra o manifesto.

**Também medidos e não adotados** (registro de 21/10):
- o ranqueador por lista (E10b, LambdaMART), com log-loss pior;
- o gold do autor no treino, com ganho pequeno, além de tirar a checagem independente;
- os antitemas, que não mudaram nenhuma publicação;
- a regra do assunto de origem, que é ruído no gold.

A rotulagem ativa (E14) fica para a produção, com a fila em `saidas/etapa2/fila_rotulagem_ativa.csv`.
