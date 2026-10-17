# ADR-005: Tratamento da árvore de temas

**Status:** Aceito (implementado em 15/10/2026)
**Data:** 14/10/2026 · revisada em 15/10/2026: convenção dos duplicados decidida (a equipe da Vício deixou a critério do autor), lixeiras em dois níveis e tipos de risco de convenção
**Decisores:** Autor do case
**Fase:** 01-dados (passo 01, preparar)
**Relacionadas:** ADR-004, ADR-007, ADR-008, ADR-010, ADR-011, ADR-013

## Contexto

A EDA (seções 10 a 18) mostrou que a árvore tem estrutura consistente (0 problemas de
pai, nível, caminho ou ID), mas o conteúdo tem armadilhas:

- **2 nós inativos** (5078 Direito penal econômico, 5234 Tratados). O LEIA-ME proíbe usá-los.
- **20 nós "fantasmas":** ativos, sem descrição e sem histórico.
  - 8 copiam um tema de Legislação Especial em outra disciplina, como 6734 LEP em Processo Penal × 4703 LEP em Legislação Especial.
  - 12 são variantes na mesma disciplina: 11 "(Parte N)", como 6726/6727 "Teoria da Pena (Parte 1/2)", mais 6735 "Provas em Espécie" × 5543 "Provas em Espécies".
  - Todos têm um canônico com similaridade de título de 0,95 a 1,0.
  - 26 questões têm assunto de origem idêntico ao título de um fantasma, o que indica que foram criados na importação.
- **21 possíveis lixeiras**, com falsos positivos (ex.: 5150 Homicídio).
- **Sobreposições legítimas:** "Ação Penal" em Penal (5063) e em Processo Penal (5466), com 67 questões de assunto ambíguo, e outros pares (Interceptação, Juizados, Pena, Sentença, Organizações Criminosas × meios de prova).
- **Títulos com erro:** Crimonológicas, Estaturo, Comeptência, Crimescontra, Caractéristas, Legitimidoras, Falso Testemunha e dois títulos que começam com número.
- **A régua pune convenção errada.** Um nó duplicado só conta como certo se for o mesmo que o especialista escolheu.
- **A equipe da Vício deixou a convenção a critério do autor** (resposta à pergunta enviada em 14/10).
- **Exposição medida:** até 83 questões (23% do recorte) têm algum sinal de pertencer à zona dos duplicados (lei citada, disciplina de origem ou assunto de origem).

## Decisão

O passo 01 (`uv run python executar_preparacao.py`) grava, além das questões (ADR-004):

- `dados/preparados/temas.json`: um registro por nó, com os campos abaixo;
- `dados/preparados/arvore_enxuta.txt`: a árvore para os prompts.

| Campo | Regra |
|---|---|
| `publicavel` | Ativo, não fantasma e abaixo da disciplina (351 nós). **Só esses IDs entram no `enum` da saída dos modelos.** |
| `canonico_id` | Para fantasmas, o nó que vale no lugar deles (mapeamento automático da EDA, adotado sem alteração). |
| `lixeira` | `forte` (11), `moderada` (7) ou vazio, conforme `dados/temas/lixeiras.csv` (revisão manual). |
| `grupo_sobreposicao` e `regra_desempate` | De `dados/temas/sobreposicoes.csv` (6 grupos); os subtemas herdam do tema. |
| `tipo_convencao` e `zona_convencao` | Risco de a convenção divergir da do especialista (abaixo). |
| `aceita_recuo` | Tema de nível 1 publicável com filhos (51 nós; ADR-010). |
| `titulo_exibicao` e `caminho_exibicao` | Títulos com erro corrigidos só para exibição (`dados/temas/correcoes_titulo.csv`); o ID não muda. |

**1. Convenção dos duplicados.**
- Vale o nó com histórico: o de Legislação Especial, ou o tema sem "(Parte N)".
- Os fantasmas nunca são tema central.
- As questões do assunto são **publicadas no canônico**, e não mandadas para revisão em bloco.

**2. Tipos de risco de convenção.** Cada nó publicável recebe um tipo, do mais ao menos provável de divergir do especialista:

| `tipo_convencao` | Quando | Nós |
|---|---|---|
| `duplicado_outra_disciplina` | O nó (ou um ancestral) tem cópia fantasma em outra disciplina | 8 |
| `sobreposicao` | O nó está num grupo de sobreposição (próprio ou herdado) | 35 |
| `duplicado_parte` | O nó (ou um ancestral) tem cópia "(Parte N)" na mesma disciplina. Vale para os subtemas, porque publicar em "Furto" é erro se o especialista usou "Dos Crimes Contra o Patrimônio (Parte 1)" | 71 |

A previsão (ADR-013) desconta uma margem por tipo, porque o gold não mede esse risco.

**3. Lixeiras em dois níveis.**
- **Forte:** publicar só com concordância total e verificador favorável (ADR-011); na árvore dos prompts, levam a marca `[conceitual]`.
- **Moderada:** só variável de risco na calibração.
- Três suspeitas foram descartadas como falso positivo: Homicídio, Ação Penal Pública e Princípios do Direito Penal.

**4. Sobreposições.** A regra de desempate escolhe o nó pelo lado material ou processual da questão (ex.: CP arts. 100–106 → Penal; CPP arts. 24–62 → Processo Penal). Se a regra não resolver, a questão vai para `revisar` (ADR-011).

**5. Árvore enxuta.**
- Formato: `ID | caminho de exibição`, só com nós publicáveis, ordenados pelo caminho, com bytes estáveis para o cache de prompt.
- Tamanho: 351 linhas, ~27 KB, ~7,4 mil tokens.
- As versões "com escopo" e "cartões por ramo" vêm dos cartões de tema (ADR-007).

**6. Checagens automáticas** (9). Se alguma falhar, nada é gravado em `dados/preparados/`:
- nenhum inativo, fantasma ou disciplina é publicável;
- todo fantasma aponta para um canônico publicável;
- toda lixeira e toda sobreposição citada existe e é publicável;
- toda correção confere com o título original do `temas.csv`;
- o título de exibição só difere nos nós corrigidos;
- a árvore enxuta lista exatamente os publicáveis, uma vez cada;
- o recuo só vale para temas de nível 1 com filhos;
- todo nó citado nas decisões existe.

Todas as decisões manuais estão em `decisoes_manuais.md` (D1 a D4).

## Opções consideradas

### Opção A: usar a árvore como veio

| Dimensão | Avaliação |
|---|---|
| Complexidade | Nenhuma |
| Custo | Nenhum |
| Efeito na régua | Negativo: o modelo pode escolher fantasma ou inativo, e cair em lixeira |
| Prazo | Imediato |

**Prós:** nada a decidir.
**Contras:** erros previsíveis entram nas publicadas.

### Opção B: excluir fantasmas e inativos, marcar lixeiras e sobreposições (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa (a EDA já calculava quase tudo) |
| Custo | Algumas horas de revisão |
| Efeito na régua | Positivo: remove erros de convenção e expõe as zonas de risco |
| Prazo | Compatível |

**Prós:** cada regra é auditável e explicável ao professor; as decisões ficam em arquivos de dados conferidos a cada execução.
**Contras:** depende de revisão manual (lixeiras, regras de desempate) e de uma convenção que o gold não consegue medir.

### Opção B2: mandar para revisão toda questão da zona dos duplicados

**Prós:** elimina o risco de convenção nas publicadas.
**Contras:** custaria até 23% da cobertura por um risco que as evidências (histórico, IDs, origem na importação) indicam ser pequeno. Rejeitada; o risco fica explícito na margem de convenção.

### Opção C: reconstruir a árvore (fundir duplicados, quebrar lixeiras)

**Prós:** seria o certo para a plataforma.
**Contras:** os IDs do gabarito são os da árvore atual; mudar a árvore quebra a avaliação. Vira **recomendação no memo** (ADR-015), não implementação.

## Análise de trade-offs

A opção B ataca a única fonte de erro que nenhum modelo consegue corrigir: a convenção de
quais nós valem. Com a convenção a critério do autor, publicar no canônico maximiza a
cobertura, e a margem por tipo de risco mantém a previsão honesta.

Os tipos têm pesos diferentes porque o risco é diferente. Uma cópia em outra disciplina
(LEP em Processo Penal) é um lugar plausível para um especialista. Um nó "(Parte 2)", sem
filhos nem descrição, é improvável para quem classifica pelo conteúdo.

## Consequências

- O `enum` do schema tem 351 IDs; IDs inválidos ficam impossíveis.
- 114 nós publicáveis estão na zona de convenção. A fração de publicadas neles define a margem da previsão.
- O memo para o professor ganha uma seção pronta: fantasmas, lixeiras, sobreposições e títulos, com a recomendação de fundir duplicados e apagar os "(Parte N)".

## Itens de ação

1. [x] Perguntar à Carla sobre nós duplicados. Resposta: a critério do autor.
2. [x] Revisar à mão as lixeiras e gravar `dados/temas/lixeiras.csv` (forte, moderada, fora), com justificativa.
3. [x] Gravar `dados/temas/sobreposicoes.csv` com os grupos e as regras de desempate (a refinar nos cartões, ADR-007).
4. [x] `vicio_ia/preparacao/arvore_preparada.py`: `LeitorDecisoesArvore`, `PreparadorArvore` e `TemaPreparado`; `ValidadorArvorePreparada` em `validacao.py`; integração ao `PipelinePreparacao`.
5. [x] Registrar em `decisoes_manuais.md`: convenção dos duplicados (D1), desempate (D2), lixeiras (D3), correções de título (D4).
