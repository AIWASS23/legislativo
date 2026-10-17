# ADR-012: Gold set manual cego

**Status:** Aceito (implementado; 60 questões rotuladas à mão em 15/10/2026)
**Data:** 14/10/2026 · revisada em 17/10/2026: o gold é uma amostra única de 60 questões
**Decisores:** Autor do case
**Fase:** 05-avaliacao (do passo 01 em diante)
**Relacionadas:** ADR-010, ADR-011, ADR-013, ADR-014

## Contexto

- **Prever a própria precisão sem gabarito faz parte do problema.** O enunciado diz: "você não recebe nenhuma questão rotulada; como estimar a própria precisão sem gabarito faz parte do problema". E a banca compara a previsão com o resultado real.
- **Concordância entre modelos não basta.** Ela mede a confiança relativa, mas não a precisão absoluta: modelos parecidos erram juntos.
- **Só um conjunto rotulado de forma independente** permite calibrar a confiança (ADR-013), escolher o limiar (ADR-011) e comparar experimentos (ADR-014).
- **Os rótulos são nossos, não dos especialistas.** Eles podem diferir em convenção: nós duplicados, Ação Penal em Penal × Processo Penal, nível de especificidade.
- **Tempo:** com 2 a 3 minutos por questão, 60 questões custam cerca de 3 horas.

## Decisão

Rotular à mão **60 questões sorteadas**, **antes** de qualquer saída de modelo sobre elas:

- **Sorteio** estratificado por disciplina de origem normalizada e formato, com alocação proporcional pelo método do maior resto e semente fixa (20261015).
- **Probabilidade de inclusão** registrada para cada questão; o peso nas estimativas é o inverso dela.
- **Ordem de rotulagem** embaralhada, para não rotular estrato por estrato.
- **O mesmo gold serve** aos experimentos (ADR-014), à calibração e à previsão (ADR-013). Para não medir o pipeline nos dados em que ele foi ajustado, toda medida de acerto usa P **fora da amostra** (validação cruzada em 5 partes).

**Arquivos** (`dados/gold/`):
- `amostra_leva1.csv`: o sorteio, com estrato e probabilidade de inclusão;
- `rotulos_leva1.csv`: a planilha de rótulos, criada vazia pelo código e **nunca sobrescrita**;
- `caderno_leva1.md`: as questões na ordem de rotulagem, só com o texto canônico.

Colunas da planilha:

| Coluna | Conteúdo |
|---|---|
| `id` | ID da questão |
| `tema_id` | O nó **mais específico** em que há segurança |
| `alternativos` | Outros nós plausíveis (`;`), sobretudo irmãos e o par de sobreposição |
| `fora` | s/n |
| `multitema` | s/n |
| `certeza` | alta / média / baixa |
| `observacao`, `minutos`, `rotulado_em` | Livre; tempo gasto; data e hora |

Regras:

1. **Rótulo cego:** quem rotula vê só o texto canônico. Nada de saída de modelo, nem disciplina ou assunto de origem. As questões do gold ficaram fora de qualquer rodada de modelo até serem rotuladas.
2. **Fontes permitidas:** texto da lei (Planalto), cartões de tema e árvore. Um LLM pode **explicar o conteúdo jurídico**, mas **nunca ser perguntado sobre o tema**. Assim o gold não herda o viés dos classificadores. O uso fica registrado.
3. **Dúvida entre subtemas:** rotular o nó pai em `tema_id` e listar os filhos plausíveis em `alternativos`.
4. **Pontuação** com a classe `PontuadorRegua`, idêntica à régua da banca (`ArvoreTemas.mesmo_ramo`):
   - **estrita:** só o `tema_id` vale; publicar num filho quando o rótulo é o pai com irmãos plausíveis conta como **erro**;
   - **tolerante:** vale qualquer nó entre `tema_id` e `alternativos` (com a mesma regra de pai e filho);
   - questão rotulada `fora` e publicada é sempre erro;
   - a diferença entre as duas vira a margem de ambiguidade do intervalo (ADR-013).
5. **O gold não sobrescreve decisões.** O `publicacao.csv` sai só do pipeline; os rótulos medem, não decidem.

## Opções consideradas

### Opção A: sem gold; estimar só pela concordância entre modelos

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | Nenhum |
| Efeito na régua | Previsão otimista e sem âncora; risco alto de errar a previsão |
| Prazo | Rápido |

**Prós:** sem trabalho manual.
**Contras:** confunde concordância com acerto; a previsão vira chute.

### Opção B: "gold prata" rotulado por um LLM mais forte

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | Baixo |
| Efeito na régua | Otimista: o rotulador compartilha viés com os classificadores |
| Prazo | Rápido |

**Prós:** escala.
**Contras:** mede concordância entre modelos de novo, não acerto.

### Opção C: gold manual cego de 60 questões (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Custo | ~3 horas humanas |
| Efeito na régua | Âncora real para calibrar, escolher o limiar e prever |
| Prazo | Caminho crítico: rotular antes da primeira rodada de modelo |

**Prós:** independente dos modelos; a margem de ambiguidade fica explícita.
**Contras:** amostra pequena (intervalos largos); a convenção do rotulador não é a do especialista; a
previsão é calibrada e conferida no mesmo gold (com validação cruzada), sem uma amostra independente.

## Análise de trade-offs

A banca avalia "o quanto a sua previsão acerta o seu próprio resultado". Só a opção C dá uma medida
que não depende dos próprios modelos.

**Limite do gold:** com 60 questões, a contagem direta **não certifica 95% no limite inferior** com
poucas publicadas no gold (nem 28 acertos em 28: o percentil 10 é ~0,95). Por isso o limiar usa a
estimativa da calibração (ADR-011, ADR-013), e só passa no critério de 95% a faixa com evidência
suficiente: consenso total em nós sem risco de convenção.

## Consequências

- **Caminho crítico:** a rotulagem precisa vir antes da primeira rodada de modelo nas questões do gold.
- A estimativa considera o desenho amostral: peso pelo inverso da probabilidade de inclusão.
- O gold vai para o repositório (`dados/gold/`), como evidência do método.

## Implementação

- `uv run python executar_gold.py`: sorteia a amostra (ou reaproveita a gravada, avisando se o
  sorteio atual divergir), cria a planilha se não existir, grava o caderno e mostra a situação
  (rotuladas, pendentes, inválidas, tempo).
- `uv run python executar_rotulagem.py`: rotulagem interativa no terminal.
  - Mostra só o texto canônico.
  - Busca temas por palavras no caminho da árvore; ao escolher um tema, mostra pai, irmãos,
    filhos e o par de sobreposição com a regra de desempate.
  - Grava cada rótulo ao confirmar; pode ser interrompida e retomada.
- Sorteio: 14 estratos, 12 com questões sorteadas. Os 2 estratos com uma questão só na população
  ficam de fora pela alocação proporcional. A probabilidade de inclusão é de ~0,17 nos demais (D6).
- A validação recusa nó não publicável e fantasma (indicando o canônico), `fora` com tema, tema repetido
  em `alternativos` e certeza fora dos três níveis.
- `PontuadorRegua.relacao` classifica cada erro (pai, filho, irmão, outro ramo) para o diagnóstico do relatório.
- **Resultado (15/10):** 60 questões rotuladas à mão pelo autor, em ~3 horas: 0 fora, 12 multitema, 30 com
  alternativos, certeza alta em 45 e média em 15.

## Itens de ação

1. [x] `vicio_ia/avaliacao/amostragem.py`: `AmostradorGold` (amostra estratificada com semente fixa e probabilidades de inclusão) e `ArquivoAmostra`.
2. [x] `vicio_ia/avaliacao/planilha.py`: `PlanilhaRotulos` (cria, acrescenta, valida e grava de forma atômica, sem sobrescrever rótulos) e `CadernoRotulagem`.
3. [x] `vicio_ia/avaliacao/pontuador.py`: `PontuadorRegua` (estrita e tolerante).
4. [x] `vicio_ia/avaliacao/rotulagem.py` e `pipeline.py`; entradas `executar_rotulagem.py` e `executar_gold.py`.
5. [x] Rotular as 60 questões: feito à mão pelo autor em 15/10.
6. [x] Registrar em `decisoes_manuais.md` (D6): semente, critérios, uso de LLM só para explicação e tempo gasto (3 horas).
