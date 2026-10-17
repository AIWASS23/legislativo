# ADR-006: Rótulos de origem como sinal fraco, nunca como rótulo

**Status:** Aceito
**Data:** 14/10/2026
**Decisores:** Autor do case
**Fase:** 01-dados (passos 01 e 03)
**Relacionadas:** ADR-004, ADR-008, ADR-014

## Contexto

Cada questão traz `disciplina_origem` e `assunto_origem`, vindos do site de onde foi
importada. O LEIA-ME avisa que "podem estar errados". A EDA (seções 8, 19, 20 e 22) mediu o quanto:

- **Assuntos:** 95 distintos, 18 vazios, 73 com "(Parte N)" e 37 com mais de um assunto.
- **Disciplinas:** 8 questões vêm de disciplinas fora do recorte (Tributário, Constitucional, Civil, Ambiental, vazio). Várias são penais de fato, como Q0218 (prisão em flagrante) e Q0309 (Lei 9.605).
- **Batem com algum nó:** 253 questões têm assunto igual ao título de um nó válido, mas 67 delas batem com **dois** nós válidos (Ação Penal) e 26 com um **fantasma**.
- **Disciplina × assunto:** em 18 questões a disciplina de origem é incoerente com o assunto.
- **Assunto × lei citada:** das 57 questões em que os dois sinais existem, 0 caem no mesmo ramo e só 8 na mesma disciplina.
- **"Concurso de Crimes" é uma lixeira do site de origem.** É o assunto mais frequente (43 questões) e aparece em 15 desses conflitos (lei de trânsito, lavagem, drogas).
- **Erros evidentes:** Q0065 (extorsão mediante sequestro) está como "Lesão Corporal"; Q0176 (falso testemunho) como "Concurso de Crimes".

## Decisão

1. Os rótulos de origem **não entram no texto dos classificadores** (ADR-004). O modelo não deve se ancorar neles.
2. Eles são usados só como:
   - **baseline E0** (ADR-014): "e se publicássemos pelo assunto de origem?", para mostrar o tamanho do problema;
   - **variável fraca** na calibração (ADR-013), como "o assunto de origem cai no mesmo ramo da escolha final?", com peso aprendido no gold e não imposto;
   - **diagnóstico** (relatório, seção b).
3. `disciplina_origem` fora do recorte **não decide `fora`**. A decisão de `fora` é do conteúdo (ADR-011).

## Opções consideradas

### Opção A: usar o assunto de origem como rótulo quando ele bate com um título

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | Nenhum |
| Efeito na régua | Negativo: 67 ambíguas, 26 em fantasmas e erros evidentes |
| Prazo | Imediato |

**Prós:** cobertura rápida.
**Contras:** importa os erros da origem, que são o problema que o case quer resolver.

### Opção B: incluir o assunto de origem no prompt como "dica"

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | Nenhum |
| Efeito na régua | Arriscado: ancoragem; o modelo tende a confirmar a dica |
| Prazo | Imediato |

**Prós:** ajuda quando o rótulo está certo.
**Contras:** contamina justamente os casos difíceis; tira a independência do sinal.

### Opção C: só sinal fraco, com peso aprendido (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | Nenhum |
| Efeito na régua | Neutro a positivo: entra só se o gold mostrar que ajuda |
| Prazo | Compatível |

**Prós:** mantém o classificador independente; o peso é medido.
**Contras:** desperdiça o rótulo nos casos em que ele está certo, mas o classificador tende a acertar esses casos sozinho.

## Análise de trade-offs

O valor de um sinal fraco está em ser **independente** dos outros. Colocar o assunto no
prompt (opção B) destrói essa independência e tira a utilidade dele na calibração. A
opção C preserva o sinal para a etapa em que ele é medido contra o gold.

## Consequências

- O baseline E0 vira um número concreto no relatório: "publicar pelo assunto de origem acertaria X%".
- O achado de que "Concurso de Crimes" é lixeira no site de origem vai para o diagnóstico e para o memo: o problema das lixeiras já vem da origem dos dados.

## Itens de ação

1. [x] Medir os conflitos e as lixeiras da origem na EDA (`AnaliseCruzada`).
2. [x] Garantir que `MontadorTextoCanonico` não inclua `disciplina_origem` nem `assunto_origem`: checagem com sentinela em `ValidadorQuestoesPreparadas`, a cada execução do passo 01 (15/10/2026).
3. [x] `vicio_ia/avaliacao/experimentos.py`: E0 implementado (15/10). Resultado: 12 de 33 certas (36%), régua estrita.
4. [x] `origem_mesmo_ramo` é variável da calibração (`SinalOrigem` em `vicio_ia/sinais/origem.py`; `VetorizadorDecisao`, 15/10).
