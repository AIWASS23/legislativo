# ADR-024: Uso dos 100 rótulos da folha-verdade e protocolo de avaliação

**Status:** Proposto. Revisa o papel do gold manual (ADR-012) e dos experimentos (ADR-014) na etapa 2.
**Data:** 20/10/2026
**Decisores:** Autor do case
**Fase:** 08-etapa2 (avaliação)
**Relacionadas:** ADR-012, ADR-014, ADR-018, ADR-022, ADR-023, ADR-025

## Contexto

- **O enunciado entrega `folha_verdade.csv`:** 100 questões rotuladas pela equipe, para uso livre (treinar,
  calibrar ou testar). O relatório precisa explicar como foram usadas e o que mostraram sobre o sistema e
  sobre a convenção da equipe (seção b).
- **Como a folha foi sorteada:**
  - de forma aleatória e estratificada por disciplina, com a mesma mistura das questões avaliadas, inclusive
    as fora;
  - na prática, só entre Q0001 e Q0359, então as 300 questões novas não têm nenhum exemplo.
- **Conteúdo:** 92 questões com tema, em 61 temas, e 8 fora. As 100 questões **não entram na avaliação.**
- **O gold manual da etapa 1 (60 questões) foi rotulado pelo autor,** e 46 delas estão entre as avaliadas.
  - Concorda com a folha em 12 das 14 questões em comum.
  - Usá-lo para treinar ou decidir seria classificar à mão questões avaliadas.
- **Nenhum desses rótulos pode vir de LLM** (ADR-019).

## Decisão

**1. A folha tem quatro usos, todos com validação cruzada:**
1. **Memória do kNN:** vizinhos rotulados (ADR-022).
2. **Treino dos pesos:** os do ranqueador (cerca de 15) e os do componente de fora (2 ou 3) (ADR-022, ADR-023).
3. **Calibração:** P(certo) fora da amostra (ADR-025).
4. **Teste:** todas as métricas do relatório saem fora da amostra.

**2. Protocolo de validação.**
- **Validação cruzada estratificada em 5 partes,** por disciplina e por fora, **repetida 10 vezes** com
  sementes fixas.
- Cada questão recebe P fora da amostra (a média das repetições), e as métricas vêm com a variação entre as
  repetições.
- **O kNN dentro da validação exclui a própria questão e a sua parte,** para não haver vazamento.
- **Seleção de modelo:** só entre as configurações pré-registradas dos experimentos E7 a E12, pela menor
  log-loss fora da amostra. Todas as configurações testadas ficam no registro, inclusive as descartadas.
- **Modelo final:** reajustado com as 100 questões e aplicado às 559 avaliadas e às próprias 100, que
  recebem decisão, mas ficam fora da previsão.

**3. Proibições:**
- usar o gold manual em treino, kNN ou decisão;
- rotular à mão mais questões avaliadas;
- olhar as 559 para escolher modelo ou limiar. Isso inclui não ajustar nada pela distribuição de decisões
  nas avaliadas, com uma exceção: a medida de deriva do item 5, que só alarga o intervalo.

**4. O que a folha revela sobre a convenção** (seção b do relatório, e ajustes):
- **Nível:** o tema central é de nível 1 em 53 questões e de nível 2 em 39. A escolha do nó pela régua
  (ADR-022) aproveita isso.
- **Extras:** 39 de 92 questões têm extras. Ganham peso o detector de multitema e o campo `extras_ids`.
- **Duplicados:**
  - "(Parte N)" nunca aparece, o que confirma a D1;
  - a LEP fantasma aparece 2 vezes;
  - a taxa de desvio da convenção é medida por tipo (cópia em outra disciplina, sobreposição, "(Parte N)") e
    substitui as taxas supostas da etapa 1 (20%, 10%, 3%);
  - a sensibilidade fica no `previsao.txt`.
- **Fora:** 8%, com os padrões descritos na ADR-023.

**5. Deriva entre questões antigas e novas** (experimento E12):
- comparar, entre as 259 antigas avaliadas e as 300 novas, as distribuições dos atributos que não dependem
  de rótulo: similaridade máxima, margem, dispersão, presença de artigo e disciplina de origem;
- se houver deriva, alargar o intervalo da previsão para as novas (ADR-025) e informar a cobertura prevista
  separadamente.

**6. Gold manual como medida secundária.** Medir a concordância do sistema com o gold nas 46 questões
avaliadas que ele cobre, sempre separada da folha. É mais um teste, com a ressalva de que a convenção do
autor não é a da equipe.

## Opções consideradas

### Opção A: separar 30 rótulos para teste e treinar com 70

| Dimensão | Avaliação |
|---|---|
| Efeito na régua | Treino e calibração mais pobres |
| Medida | Um teste "puro", mas com intervalo enorme (30 itens) |

**Contras:** com 100 rótulos, separar um pedaço desperdiça dado. A validação cruzada repetida mede melhor.

### Opção B: validação cruzada repetida, com todas as métricas fora da amostra (escolhida)

| Dimensão | Avaliação |
|---|---|
| Efeito na régua | Usa os 100 rótulos para treinar, calibrar e testar |
| Medida | Fora da amostra, com a variação entre as repetições |
| Risco | Seleção de modelo com otimismo leve, controlado pelo pré-registro dos experimentos |

### Opção C: somar o gold manual ao treino (160 rótulos)

| Dimensão | Avaliação |
|---|---|
| Efeito na régua | Mais exemplos |
| Regras | Classificaria à mão questões avaliadas, e a convenção do autor difere da equipe (2 discordâncias em 14) |

**Contras:** descartada.

## Análise de trade-offs

Com 100 rótulos, cada um é precioso, e a validação cruzada repetida é o jeito padrão de usar todos sem medir
o sistema nos mesmos dados em que ele aprendeu. O pré-registro dos experimentos limita o otimismo da seleção
de modelo. A deriva é o ponto cego que a folha não cobre: ela tem só questões antigas, e a previsão precisa
dizer isso.

## Consequências

- O relatório (seção b) responde diretamente "como usei os 100 rótulos": kNN, pesos, calibração e teste,
  sempre fora da amostra.
- O `previsao.txt` explica que a calibração vem das antigas e como a deriva para as novas foi tratada.
- O gold manual deixa de ser âncora, mas continua no repositório como evidência da etapa 1.

## Itens de ação

1. [ ] `vicio_ia/sistema/folha.py`: leitura e validação da folha, com o acerto pela régua nova (central,
   extras, pai e filho).
2. [ ] `vicio_ia/sistema/validacao.py`: validação cruzada repetida e estratificada, sem vazamento no kNN.
3. [ ] Pré-registrar E7 a E12 em `saidas/experimentos/registro.md` antes de rodar.
4. [ ] Medir a convenção (nível, extras, duplicados, fora) e as taxas de desvio por tipo de convenção.
5. [ ] Experimento E12 (deriva entre antigas e novas).
