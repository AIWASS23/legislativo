# ADR-020: Base de conhecimento dos temas

**Status:** Implementado (21/10/2026; revisão do autor na D14, exemplos sintéticos na D16)
**Data:** 20/10/2026
**Decisores:** Autor do case
**Fase:** 08-etapa2 (fase de conhecimento)
**Relacionadas:** ADR-005, ADR-007, ADR-018, ADR-019, ADR-021, ADR-022

## Contexto

- **São 351 temas utilizáveis, e só 20 têm descrição de verdade.** Os demais têm um texto-modelo ("Subtema
  de X. N questões") ou nada (EDA da etapa 1).
- **A folha cobre poucos temas.** As 92 questões com tema estão em só 61 temas distintos, então a maioria
  dos temas **não tem nenhum exemplo rotulado**. Para esses temas, a decisão depende de casar a questão com
  a descrição do tema, e a qualidade dessa descrição limita o sistema.
- **Os cartões da etapa 1 já existem.** São 351 cartões, rascunhados por LLM e sem revisão (D7), com
  escopo, o que entra, o que não entra e leis de referência. Pela regra nova, "enriquecer a descrição dos
  temas" é permitido.
- **Poucas questões citam artigo** (12–16%), mas quando citam, o artigo aponta o tema com muita precisão.
  Um mapa artigo → tema rende pouca cobertura e muita precisão.
- **O enunciado aceita termos e exemplos propostos por LLM,** desde que o autor os **revise e guarde como
  dado**.
- **O tempo humano é o recurso escasso:** a revisão precisa caber em cerca de 3 a 4 horas do autor, na quarta,
  21/10.

## Decisão

Construir, para cada tema utilizável, um **documento de tema** versionado e dois artefatos estruturados. O
LLM propõe, o autor revisa por prioridade, e o resultado fica guardado como dado.

**1. Documento de tema** (`dados/conhecimento/temas.jsonl`)
- **Identidade:** id, caminho, título corrigido para exibição (D4), nível, pai, irmãos e filhos.
- **Escopo:** o cartão da etapa 1, com o que entra e o que não entra (este último com o ID do nó certo).
- **Referências legais estruturadas:** lei e artigos, alimentando o mapa abaixo.
- **Termos característicos:** os do dicionário abaixo.
- **Exemplos rotulados da folha,** quando houver. Servem como âncora do kNN (ADR-022).
- **Texto para embedding:** caminho, escopo, termos e, se o experimento E8 mostrar ganho, até 3 exemplos
  sintéticos (ADR-021).

**2. Mapa lei/artigo → tema** (`dados/conhecimento/mapa_artigos.csv`)
- **Colunas:** `lei`, `art_inicio`, `art_fim`, `tema_id`, `forca` (`exata` ou `ramo`), `origem` e `revisado`.
- **Exemplo:** CP, arts. 121 a 128 → Crimes contra a Vida; CPP, arts. 406 a 497 → Procedimento do Tribunal do Júri.
- **Proposto pelo LLM** a partir da árvore e das leis do recorte (CP, CPP, LEP e leis especiais da ADR-005).
- **Revisado integralmente pelo autor,** com o texto da lei aberto (Planalto). São poucas centenas de linhas.

**3. Dicionário de termos** (`dados/conhecimento/termos.csv`)
- **Colunas:** `termo` (normalizado), `tema_id`, `tipo`, `origem` e `revisado`.
- **Tipos:**
  - `forte`: o termo quase define o tema; exemplos: "impronúncia", "desaforamento", "sursis processual";
  - `fraco`: o termo é comum ao tema;
  - `exclui`: o termo aponta para outro nó.
- **Fontes:** o LLM propõe a partir do documento do tema, e os termos mais discriminativos das questões da
  folha entram por TF-IDF por classe, já que a folha é dado de treino.

**4. Protocolo de revisão,** pela ordem, até onde o tempo permitir:
1. **Mapa de artigos:** revisão de 100% das linhas, porque as regras dele são as de maior peso.
2. **Termos `forte` e `exclui` das zonas de risco:** lixeiras (D3), sobreposições (D2), irmãos parecidos e
   os temas onde a etapa 1 errou na folha.
3. **Amostra aleatória de 10% do restante,** para estimar a taxa de erro dos itens não revisados. Essa taxa
   vai para o relatório.
4. **Documentos de tema:** revisão das zonas de risco. O restante fica como rascunho do modelo, e isso é
   declarado no manifesto.

A revisão usa uma ferramenta interativa no terminal, no modelo do `executar_rotulagem.py`:
- mostra a proposta, o caminho do tema e os vizinhos;
- aceita, corrige ou apaga cada item;
- grava a cada item e pode ser retomada;
- registra no manifesto quem revisou, quando, e quantos itens foram aprovados, corrigidos ou apagados.

**5. Convenção dos duplicados (D1).**
- A folha confirma o nó canônico: "(Parte N)" nunca aparece.
- A LEP fantasma (6734) aparece 2 vezes, e o documento da LEP canônica (4703) registra isso.
- O efeito sobre a decisão é medido pela régua: publicar na LEP canônica erra quando a equipe usou só a
  fantasma (ADR-024).

## Opções consideradas

### Opção A: usar os títulos e os cartões como estão

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Tempo humano | Nenhum |
| Efeito na régua | Limitado: cartões sem revisão erram justamente nas zonas de risco; não há mapa de artigos |

**Prós:** zero esforço.
**Contras:** desperdiça o sinal mais preciso que existe (o artigo citado) e não organiza o conhecimento,
que é o centro da avaliação.

### Opção B: documentos, mapa e dicionário, com revisão priorizada (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Tempo humano | ~3–4 h, priorizadas |
| Efeito na régua | Regras de alta precisão onde há artigo ou termo forte; descrição melhor para os temas sem exemplo |

**Prós:** cumpre "propor, revisar, guardar como dado"; cada item tem origem e estado de revisão.
**Contras:** depende do tempo do autor; o que não for revisado é declarado como tal.

### Opção C: muitos exemplos sintéticos por tema como base de treino

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Tempo humano | Alto: revisar milhares de exemplos é inviável |
| Efeito na régua | Incerto: o estilo sintético difere do estilo das provas |

**Prós:** daria exemplos a todos os temas.
**Contras:** a revisão não cabe no prazo, e um exemplo sintético errado vira rótulo errado. Fica só como
âncora opcional de embedding (até 3 por tema), condicionada ao experimento E8 (ADR-021).

## Análise de trade-offs

O enunciado diz que organizar o conhecimento dos dados é o centro do trabalho. O mapa de artigos e os termos
fortes dão decisões de alta precisão e explicáveis ("a questão cita o art. 155 do CP"), justamente o tipo de
decisão que pode ser certificada em 95%. A descrição melhor dos temas ajuda a recuperação para os temas sem
exemplo. A revisão priorizada coloca o tempo humano onde o erro custa mais.

## Consequências

- O sistema fica explicável: cada publicação cita a regra, o termo ou o vizinho rotulado que a sustentou.
- A qualidade depende da revisão. O relatório informa quanto foi revisado e a taxa de erro estimada no restante.
- Na produção, o professor revisa os documentos de tema, e não questões uma a uma (ADR-027).

## Itens de ação

1. [x] Prompt versionado `prompts/conhecimento_tema.md`, com schema JSON sem nenhum campo de questão.
2. [x] `vicio_ia/enriquecimento/propostas.py`: gerar as propostas por tema, com cache e manifesto.
3. [x] Ferramenta de revisão interativa e o registro da revisão no manifesto (`executar_revisao_conhecimento.py`).
4. [x] Revisar o mapa de artigos (100%), os termos das zonas de risco e a amostra de 10% (20/10, 3 h).
5. [x] Registrar em `decisoes_manuais.md` (D14): o protocolo de revisão, o tempo gasto e as taxas medidas.
