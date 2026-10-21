# ADR-025: Calibração, limiar e previsão na etapa 2

**Status:** Implementado com ajustes (21/10/2026; ver D15). Revisa as ADR-011 e ADR-013 para a etapa 2.
**Data:** 20/10/2026
**Decisores:** Autor do case
**Fase:** 08-etapa2 (decisão e avaliação)
**Relacionadas:** ADR-011, ADR-013, ADR-022, ADR-023, ADR-024

## Contexto

- **A régua continua a mesma:** pelo menos 95% de acerto no conjunto publicado e, respeitado isso, o máximo
  de cobertura.
- **O que muda:**
  - a avaliação e a previsão valem para as **559 questões fora da folha**;
  - o acerto agora inclui os extras;
  - a calibração tem rótulos da equipe (a folha), não do autor.
- **O que a etapa 1 ensinou:**
  - **as faixas venceram a regressão** com poucos erros; o limiar pelo percentil 10 funcionou;
  - **o estimador direto precisa de suavização,** pela D12;
  - **as taxas de convenção eram suposições,** e agora podem ser medidas (ADR-024).
- **Riscos novos:**
  - **o fora:** 8% na folha (ADR-023);
  - **a deriva:** a folha só tem questões antigas, e metade das avaliadas é nova (ADR-024).

## Decisão

**1. Calibração.**
- A entrada é a P(certo) composta (ADR-022 e ADR-023), fora da amostra, nas 100 questões da folha.
- O calibrador é escolhido pela menor log-loss fora da amostra, entre:
  - **faixas de evidência,** como na etapa 1, agora por âncora:
    - regra forte (artigo `exata` ou termo `forte`) no nó escolhido;
    - concordância entre as representações (lexical, densa e kNN no mesmo ramo);
    - o resto;
  - **Platt** (logística em 2 ou 3 atributos: P composta, margem e P(fora));
  - a isotônica fica de fora, porque é instável com 100 pontos.
- **A incerteza** vem de sorteios Beta por faixa, ou de bootstrap da calibração, como na etapa 1.

**2. Limiar.**
- Publicar o maior conjunto cuja precisão estimada tenha percentil 10 ≥ 95%, nas 559 avaliadas.
- O corte só cai entre valores distintos de P.
- A regra de reserva (ponto ≥ 97%) continua.
- As questões da folha recebem decisão com o mesmo limiar, mas não entram na previsão.

**3. Desconto de convenção medido, e não suposto.**
- A chance efetiva de cada candidata desconta a taxa de desvio de convenção do tipo do nó: cópia em outra
  disciplina, sobreposição ou "(Parte N)".
- **Taxa:** a que foi medida na folha, com suavização de Jeffreys.
- **Sensibilidade:** taxas multiplicadas por 0, 1 e 2, no `previsao.txt`.

**4. Previsão para as 559.**
- **Ponto da precisão:** a média do estimador por modelo (a P média das publicadas entre as 559) com o
  estimador direto (acerto fora da amostra das questões da folha que cairiam na zona publicada, com Jeffreys,
  como na D12).
- **Intervalo:** percentis 5 e 95 dos sorteios. No limite inferior, entram três margens:
  - **ambiguidade:** a diferença entre a régua com e sem extras na folha;
  - **fora:** a incerteza da taxa de fora na faixa publicada (Beta);
  - **deriva:** se o E12 mostrar deriva, um alargamento para as novas, proporcional à mudança medida na
    distribuição dos atributos.
- **Cobertura:** publicadas ÷ 559. É exata dado o sistema, com ± 0,01 de arredondamento. Informar também a
  cobertura das antigas e das novas, separadas.

**5. Coluna `confianca`.** A P(certo) calibrada, ou seja, a chance efetiva. Na decisão `fora`, entra P(fora).

## Opções consideradas

### Opção A: reaproveitar sem mudança a calibração e o limiar da etapa 1

**Contras:** as faixas da etapa 1 eram definidas por votos de LLM, que não existem mais. A estrutura da
calibração continua, mas as faixas precisam ser redefinidas.

### Opção B: limiar pela estimativa pontual (média ≥ 95%)

| Dimensão | Avaliação |
|---|---|
| Efeito na régua | Mais cobertura, com mais de 10% de chance de ficar abaixo de 95% |

**Contras:** na etapa 1 esse critério foi descartado, e a razão continua valendo: estourar a régua é o erro
mais caro.

### Opção C: faixas de evidência ou Platt, escolhidos por validação cruzada; limiar pelo percentil 10; margens de fora e de deriva (escolhida)

| Dimensão | Avaliação |
|---|---|
| Efeito na régua | Conservador onde a evidência é fraca; publica com segurança onde há regra forte |
| Previsão | Explicita as três fontes de incerteza que a folha não cobre bem |

## Análise de trade-offs

A banca compara a previsão com o resultado real. Na etapa 1, a margem era sobre a convenção suposta. Agora,
a convenção é medida, e os pontos cegos passam a ser o fora e a deriva. A previsão precisa nomear esses dois
riscos e mostrar o efeito de cada um.

## Consequências

- A cobertura das questões novas pode ficar menor que a das antigas. Isso é esperado e vai para o
  relatório (seção c).
- O `previsao.txt` passa a ter três margens nomeadas e a sensibilidade das taxas de convenção medidas.

## Itens de ação

1. [x] Calibração em `vicio_ia/sistema/politica.py`: identidade, Platt ou Platt com a faixa de concordância,
   escolhidos pela log-loss fora da amostra. A identidade venceu.
2. [x] `EstimadorLimiar` para as 559, com cobertura separada para antigas e novas. O fora entra pelo estimador
   direto, e não há margem de deriva, porque o E12 não mostrou deriva.
3. [x] Testes do limiar e do determinismo (`testes/teste_sistema.py`). A previsão exclui a folha, como confere
   o validador.
4. [x] Gráficos de confiabilidade e de precisão × cobertura da etapa 2, gerados pelo `executar_sistema.py` em
   `saidas/sistema/` (`confiabilidade.png`, `precisao_cobertura.png` e a tabela em `graficos.md`).

## Implementação (21/10/2026)

Implementado em `vicio_ia/sistema/` (`pares.py`, `ranqueador.py`, `politica.py` e `pipeline.py`) e rodado por
`executar_sistema.py`, sem LLM e com a trava de rede.
- **Ajustes da implementação e regra de publicação** adotada pelo autor (reserva pontual de 97%): na D15 de
  `decisoes_manuais.md`.
- **Ranqueador:** gradient boosting (E10), com os atributos dos exemplos sintéticos (E13, D16).
- **Resultado final:** 127 das 559 avaliadas publicadas, com previsão de 0,96 (0,91–0,99). No gold do autor, as 10
  publicadas estão certas.
