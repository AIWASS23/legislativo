# ADR-023: "Fora" e multitema

**Status:** Implementado com o plano B (21/10/2026; ver E11b e D15)
**Data:** 20/10/2026
**Decisores:** Autor do case
**Fase:** 08-etapa2 (fase de decisão)
**Relacionadas:** ADR-011, ADR-018, ADR-021, ADR-022, ADR-024, ADR-025

## Contexto

- **8 das 100 questões da folha são "fora" (8%).** Publicar uma questão fora é sempre erro.
- **Foi aí que a etapa 1 falhou.** Das 29 publicações que caíram na folha, as 2 erradas eram questões fora
  (Q0039 e Q0303); a precisão foi de 93%.
- **O alcance desse risco:** se as questões fora forem indistinguíveis das demais, cerca de 8% de qualquer
  conjunto publicado será erro. Nenhum conjunto chegaria a 95%.
- **A convenção da equipe não é intuitiva.** Leitura do autor sobre as 8 questões, não confirmada pela equipe:

  | Padrão | Questões | Exemplo |
  |---|---|---|
  | Mistura de temas sem um central | Q0043, Q0252, Q0291, Q0303 | Q0043 mistura atenuante, critério trifásico, dias-multa e regime |
  | Assunto sem nó ativo | Q0017, Q0039 | Q0017: rito dos crimes de responsabilidade dos funcionários públicos. Q0039: ordem econômica (o tema "Direito penal econômico", 5078, está inativo) |
  | Sem explicação aparente | Q0002, Q0087 | Q0087: prisão domiciliar na execução penal, embora existam nós de LEP e de prisão domiciliar |

- **A árvore tem dois temas inativos:** 5078 ("Direito penal econômico") e 5234 ("Tratados e convenções em
  matéria criminal"). O LEIA-ME manda não usar temas inativos.
- **As 300 questões novas trazem 10 de Direito Penal Militar ou Processual Penal Militar,** e não há nó
  militar na árvore.
- **Multitema é comum:** 39 das 92 questões com tema têm extras. Ter vários temas, portanto, não basta para
  ser "fora".

## Decisão

**1. Modelar P(fora) separadamente** do ranqueamento de temas.
- **Atributos** (poucos, porque há só 8 positivos):
  - a maior similaridade da questão com qualquer documento de tema, e a margem entre o primeiro e o segundo
    candidato;
  - a **dispersão entre as alternativas:** quantos ramos distintos aparecem como melhor tema de cada
    alternativa, e a entropia dessa distribuição;
  - o enunciado genérico (regra da etapa 1);
  - a similaridade com os documentos dos **temas inativos**;
  - a similaridade com as questões fora da folha (kNN);
  - a disciplina de origem fora do recorte: Militar, Tributário, Civil ou Constitucional.
- **Modelo:**
  - uma regressão logística com 2 ou 3 atributos, escolhidos no experimento E11 pela AUC fora da amostra;
  - o intercepto ancorado na taxa da folha, Beta(8,5; 92,5);
  - se nenhum atributo separar as questões fora (AUC fora da amostra < 0,7), P(fora) volta a ser a taxa da
    folha.

**2. Regras de fora com motivo explícito,** aplicadas antes do ranqueamento:
- disciplina de origem militar e nenhum candidato com regra forte (artigo ou termo `forte`) → `fora`,
  motivo "direito militar: sem tema na árvore";
- melhor candidato com alta similaridade a um tema inativo e nenhuma regra forte para um tema ativo →
  `fora`, motivo "tema inativo na árvore".

**3. Composição com o ranqueamento.**
- `P(certo) = P(nó certo | não fora) × (1 − P(fora))`.
- A calibração final (ADR-025) é aplicada sobre essa composição.

**4. Política.**
- **`fora`:** quando P(fora) é alta, com o limiar escolhido na validação cruzada para precisão alta no
  próprio "fora", ou quando uma regra do item 2 dispara.
- **`revisar`:** quando P(fora) é intermediária (motivo "possível fora do recorte"), ou quando a dispersão
  entre as alternativas é alta e não há tema dominante (motivo "questão cobre vários temas").
- **`publicar`:** exige P(fora) baixa e passar no limiar da ADR-025. A previsão leva a incerteza da taxa de
  fora entre as publicadas: os casos da folha que caem na faixa publicada entram numa Beta.

**5. Medir o alcance do risco antes de tudo** (E11):
- a AUC de P(fora) fora da amostra;
- a taxa de fora em cada faixa de confiança.

Se o fora não for separável, o plano B é publicar só as faixas em que a folha mostre taxa de fora
compatível com 95%. Uma regra forte não garante, sozinha, que a questão não seja fora: a Q0087 cita o
art. 117 da LEP, um tema ativo, e mesmo assim a equipe a marcou como fora. Por isso, o E11 mede a taxa de
fora em cada faixa, inclusive nas faixas sustentadas por artigo ou termo `forte`.

## Opções consideradas

### Opção A: tratar fora como mais uma classe do ranqueamento

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Efeito na régua | Ruim: com 8 exemplos, a "classe fora" nunca vence no softmax |

### Opção B: ignorar fora, como na etapa 1 (só 2 fora)

| Dimensão | Avaliação |
|---|---|
| Efeito na régua | Comprovadamente ruim: 93% na folha |

### Opção C: componente separado de P(fora), regras explícitas e dispersão entre as alternativas (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Efeito na régua | Ataca a causa medida do erro da etapa 1 |
| Risco | 8 positivos: a incerteza é grande e precisa aparecer no intervalo |

## Análise de trade-offs

O fora é o único erro que a etapa 1 cometeu na folha. Por isso merece um componente próprio. A dispersão
entre as alternativas é o melhor candidato a sinal, e não custa nada: a mistura de temas explica 4 dos 8
casos. As regras de militar e de tema inativo cobrem casos que não aparecem na folha, mas que o próprio
LEIA-ME e a árvore justificam. Com só 8 exemplos, a postura conservadora é: na dúvida, `revisar`, e não
`publicar` nem `fora`.

## Consequências

- O número de `fora` sobe em relação à etapa 1, que teve só 2.
- O memo para o professor pede a definição de "fora" da equipe, com os 8 casos como exemplo, e pergunta se
  vale criar temas para os assuntos sem nó (rito dos crimes funcionais, ordem econômica, direito militar).
- O relatório (seção b) mostra o que a folha revelou sobre essa convenção.

## Itens de ação

1. [x] Regras de militar e de tema inativo em `vicio_ia/sistema/politica.py` (`RegrasFora`). No plano B, P(fora)
   não tem modelo próprio: as questões fora entram no treino como negativos.
2. [x] Multitema: os extras saem do ranqueador (outro ramo com P ≥ 0,5), e a fração das alternativas no ramo é
   atributo. A dispersão foi medida no E11b (AUC de 0,61) e não ganhou módulo próprio.
3. [x] Experimento E11 (separabilidade do fora) e decisão sobre o plano B. O E11 lexical deu AUC de 0,54, e
   o E11b, com embeddings e kNN, deu 0,61 fora da amostra, os dois abaixo de 0,7. Vale o plano B (registro de
   21/10). A proximidade com um tema inativo (AUC isolada de 0,83, exploratória) entra como sinal de `revisar`.
4. [x] Testes unitários das regras de fora e da escolha do nó (`testes/teste_sistema.py`).

## Implementação (21/10/2026)

Implementado em `vicio_ia/sistema/` (`pares.py`, `ranqueador.py`, `politica.py` e `pipeline.py`) e rodado por
`executar_sistema.py`, sem LLM e com a trava de rede.
- **Ajustes da implementação e regra de publicação** adotada pelo autor (reserva pontual de 97%): na D15 de
  `decisoes_manuais.md`.
- **Ranqueador:** gradient boosting (E10), com os atributos dos exemplos sintéticos (E13, D16).
- **Resultado final:** 127 das 559 avaliadas publicadas, com previsão de 0,96 (0,91–0,99). No gold do autor, as 10
  publicadas estão certas.
