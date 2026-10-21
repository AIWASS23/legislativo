# ADR-022: Classificador sem LLM: candidatos, ranqueamento e escolha do nó

**Status:** Implementado com ajustes (21/10/2026; ver D15). Substitui a ADR-008 na decisão da etapa 2.
**Data:** 20/10/2026
**Decisores:** Autor do case
**Fase:** 08-etapa2 (fase de decisão)
**Relacionadas:** ADR-008, ADR-010, ADR-020, ADR-021, ADR-023, ADR-024, ADR-025

## Contexto

- **São 351 classes possíveis, e a folha tem só 92 questões com tema,** em 61 temas. Um classificador
  multiclasse supervisionado não aprende com isso.
- **A saída precisa vir de um ranqueamento de pares (questão, tema)** por sinais genéricos, com poucos pesos
  aprendidos na folha. Os temas sem exemplo são cobertos pela descrição (ADR-020).
- **A régua nova aceita o tema central, um extra, ou o pai ou filho de qualquer um deles.** Escolher o nó
  certo da árvore vale tanto quanto escolher o tema.
- **O enunciado pede uma probabilidade calibrável.** Cita embeddings, busca, regras sobre a árvore e sobre as
  leis, dicionário de termos, classificador treinado, kNN e modelo de ranqueamento.

## Decisão

**1. Geração de candidatos.** A união do top-k de cada fonte, com k = 10 por fonte e cerca de 30 candidatos
no total:
- similaridade de embedding entre a questão e o documento do tema (e os exemplos sintéticos, se houver);
- BM25 da questão contra os documentos de tema;
- regras: o mapa de artigos e os termos `forte`;
- kNN na folha: os temas das 5 questões rotuladas mais próximas, mais os ramos desses temas;
- o assunto de origem, quando coincide com um título de tema (sinal fraco, ADR-006).

**2. Atributos de cada par (questão, tema):**
- **Semânticos:** a similaridade de embedding e a posição do tema no ranking; o mesmo para BM25 e TF-IDF;
  a similaridade máxima entre os filhos do tema.
- **Regras:**
  - o artigo citado cai no intervalo do tema (`exata`) ou num tema do ramo (`ramo`);
  - a lei citada é a do tema;
  - quantos termos `forte` e `fraco` aparecem, e se algum termo `exclui` aparece.
- **kNN:** a soma das similaridades dos vizinhos rotulados cujo tema está no ramo do candidato.
- **Estrutura:** o nível do tema, se ele é lixeira (D3), se tem descrição real, quantos irmãos tem, e a
  fração das alternativas cujo melhor tema cai no ramo do candidato.
- **Origem:** se o assunto de origem coincide com o tema ou com o ramo.

**3. Modelo de ranqueamento.**
- Uma regressão logística sobre os pares, com L2 forte e cerca de 15 atributos padronizados.
- **Um par é positivo se o tema estiver certo pela régua:** é o tema central, um extra, ou o pai ou filho
  de um deles. São cerca de 92 questões × 30 candidatos ≈ 2.800 pares.
- A probabilidade de cada tema sai de um softmax dos escores entre os candidatos da questão.
- **Baseline sem aprendizado:** soma ponderada com pesos fixos, para medir se o treino ajuda (E10).

**4. Escolha do nó pela régua.**
- Para cada nó publicável `n`, calcular `P(certo | n) = Σ_t P(t) · 1[t está no ramo de n]`, onde o ramo de
  `n` inclui o próprio `n`, o pai e os filhos.
- Publicar o nó com a maior `P(certo | n)`. Isso generaliza o recuo para o pai da ADR-010: se a dúvida é
  entre irmãos, o pai soma as probabilidades deles e vence.
- **Nunca o nível 0 (disciplina).**

**5. Extras.** Os temas de outro ramo com `P(t)` acima de um limiar (no máximo 3) vão para `extras_ids`, como
pede o formato da entrega.

**6. Experimentos,** continuando a numeração da ADR-014, todos fora da amostra (ADR-024):
- **E7:** só lexical. **E8:** só embeddings, também usado para escolher o modelo (ADR-021). **E9:** só kNN.
- **E10:** o ranqueador completo, contra a soma ponderada sem treino.
- Métricas: acerto pela régua no top-1 e no nó escolhido, recall@5, log-loss, e a curva de precisão por
  cobertura.

## Opções consideradas

### Opção A: classificador multiclasse supervisionado (TF-IDF + regressão logística)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Efeito na régua | Péssimo: 290 dos 351 temas não têm exemplo |

**Contras:** não cobre os temas sem rótulo. Fica só como sinal (kNN), e não como decisor.

### Opção B: só similaridade de embedding (zero-shot)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Efeito na régua | Razoável no top-5, fraco no top-1 entre irmãos |

**Contras:** ignora artigo, termos e vizinhos rotulados; não aprende com a folha.

### Opção C: candidatos de várias fontes e ranqueador logístico de baixa capacidade (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Efeito na régua | Combina regras precisas e similaridade ampla; os pesos vêm da folha |
| Risco de sobreajuste | Controlado: cerca de 15 pesos, L2 forte, validação cruzada repetida |

### Opção D: learning-to-rank com árvores (LambdaMART, LightGBM)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Risco de sobreajuste | Alto com 92 consultas |
| Dependências | Uma biblioteca nova |

**Contras:** capacidade demais para 100 rótulos. Pode ser testada como E10b, se sobrar tempo.

## Análise de trade-offs

Com 100 rótulos, ganha o modelo com poucos parâmetros e atributos bem pensados. A escolha do nó pela régua
transforma a ambiguidade entre irmãos em cobertura: em vez de mandar para revisão, publica-se o pai, que a
régua aceita. Isso já era o recuo para o pai da etapa 1, agora com uma conta explícita.

## Consequências

- Cada decisão pode ser explicada pelos atributos que mais pesaram (artigo, termo, vizinho, similaridade).
  O `motivo` e o relatório usam isso.
- O sistema é determinístico: sementes fixas e ordem estável.
- A probabilidade de saída ainda precisa de calibração e do componente de fora (ADR-023, ADR-025).

## Itens de ação

1. [x] `vicio_ia/sistema/pares.py` (no lugar de `candidatos.py`): união das fontes, com o top-k configurável em `configuracao.py`.
2. [x] `vicio_ia/sistema/pares.py` (no lugar de `atributos.py`; 20 atributos): os atributos por par.
3. [x] `vicio_ia/sistema/ranqueador.py` (logística e gradient boosting; o boosting venceu o E10): regressão logística em pares (numpy, IRLS com L2, como na etapa 1)
   e o baseline com pesos fixos.
4. [x] `vicio_ia/sistema/politica.py` (no lugar de `no_pela_regua.py`; o par rotulado pela régua dá P(certo | nó) direto): `P(certo | n)` e a escolha do nó, com testes unitários
   (irmãos, pai, filho e extras).
5. [x] Experimentos E7, E9 e E10 no registro, e também E10b (LambdaMART) e E13 (exemplos sintéticos). A soma
   ponderada sem treino, a referência original do E10, ficou de fora.

## Implementação (21/10/2026)

Implementado em `vicio_ia/sistema/` (`pares.py`, `ranqueador.py`, `politica.py` e `pipeline.py`) e rodado por
`executar_sistema.py`, sem LLM e com a trava de rede.
- **Ajustes da implementação e regra de publicação** adotada pelo autor (reserva pontual de 97%): na D15 de
  `decisoes_manuais.md`.
- **Ranqueador:** gradient boosting (E10), com os atributos dos exemplos sintéticos (E13, D16).
- **Resultado final:** 127 das 559 avaliadas publicadas, com previsão de 0,96 (0,91–0,99). No gold do autor, as 10
  publicadas estão certas.
