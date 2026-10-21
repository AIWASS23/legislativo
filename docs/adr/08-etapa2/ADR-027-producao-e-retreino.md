# ADR-027: Produção na etapa 2: custo, ciclo do professor e retreino

**Status:** Implementado no desenho (21/10/2026). Revisa a ADR-016 para a etapa 2.
**Data:** 20/10/2026
**Decisores:** Autor do case; equipe Vício
**Fase:** 08-etapa2 (produção; seção d do relatório)
**Relacionadas:** ADR-016, ADR-019, ADR-020, ADR-021, ADR-022, ADR-024, ADR-025

## Contexto

- **A seção d do relatório pergunta três coisas:**
  - o custo e o tempo para 50 mil questões por semana;
  - como a correção do professor vira dado de treino;
  - de quanto em quanto tempo o sistema se retreina.
- **A arquitetura da ADR-016 estimava US$ 0,02 a 0,04 por questão.** O custo vinha de LLMs na decisão (N2),
  o que agora é proibido. A decisão passa a custar quase nada, e o custo se desloca para a fase de
  conhecimento e para o professor.
- **O sistema da etapa 2 tem peças com ritmos de atualização diferentes:**
  - a memória do kNN aceita exemplo novo sem retreino;
  - os pesos do ranqueador e a calibração precisam de retreino;
  - os documentos de tema e os embeddings mudam quando a árvore muda.

## Decisão

**1. Fluxo por questão nova.**
1. **Importação:** o texto canônico e o hash; uma duplicata exata de questão validada herda o tema.
2. **Fase de conhecimento:**
   - as citações, pela regex, e por um LLM pequeno só quando a regex falha (cerca de 10% das questões);
   - o embedding da questão e das alternativas.
3. **Fase de decisão:** candidatos, ranqueador, P(fora), calibração e limiar, tudo em CPU.
4. **Saída:** `publicar`, `revisar` (fila do professor) ou `fora` (agrupado para propor temas).

**2. Custo e tempo para 50 mil questões por semana** (a confirmar com medidas do case):

| Etapa | Custo | Tempo |
|---|---|---|
| Embeddings (modelo local, como o `bge-m3`) | Servidor próprio; ~US$ 0 marginal | A medir: vetores por segundo na máquina do case, extrapolados para 50 mil |
| Embeddings por API (alternativa) | ~500 tokens × 50 mil = 25 milhões de tokens; centavos a poucos dólares por semana, conforme o modelo | Minutos, em lote |
| Extração por LLM pequeno (~10%) | ~5 mil chamadas curtas; poucos dólares por semana | Minutos, em lote |
| Decisão (CPU) | ~US$ 0 | Segundos a minutos para 50 mil (a medir) |
| **Total de máquina** | **Ordem de US$ 0,0001 por questão** | Uma janela noturna folgada |

- **A comparação vai para o relatório:** a arquitetura com LLM na decisão (ADR-016) custava cerca de 200 a
  400 vezes mais por questão.
- **O custo dominante continua sendo o professor:**
  - estimativa: ~1 minuto por item com sugestão, contra 3 minutos medidos para rotular do zero;
  - a fila é ordenada por impacto (acessos dos alunos) vezes incerteza;
  - o que não for revisado não é publicado.

**3. Como a correção do professor vira dado.**
- **Registro:** cada decisão do professor (aceitar, corrigir, marcar fora ou escolher o tema central de uma
  multitema) é gravada com a versão do sistema que fez a sugestão.
- **Uso imediato:** entra na **memória do kNN**, sem retreino. É o ganho mais rápido, porque a próxima questão
  parecida já tem um vizinho rotulado.
- **Uso no treino:** entra no **treino dos pesos** do ranqueador e do componente de fora.
- **Uso na calibração: só a auditoria aleatória entra.** As revisões da fila não entram, porque a fila é um
  conjunto escolhido pela própria incerteza do sistema, e calibrar com ela distorceria as probabilidades.
- **Correções repetidas num mesmo tema viram revisão do documento do tema e do dicionário** (ADR-020). É o
  professor corrigindo a definição, e não questão a questão.

**4. Frequência de atualização.**

| Peça | Quando | Portão |
|---|---|---|
| Memória do kNN | Contínua (a cada revisão) | Nenhum; o exemplo é rótulo humano |
| Pesos do ranqueador e de P(fora) | Semanal | Gold de regressão: a folha mais as auditorias acumuladas |
| Calibração e limiar | Semanal, só com a auditoria aleatória | Se o limite inferior cair abaixo de 95%, o limiar sobe automaticamente |
| Documentos de tema, termos e mapa de artigos | Quando o professor revisa um tema ou a árvore muda | Revisão humana registrada no manifesto |
| Embeddings | Quando o modelo ou o documento do tema muda | Recalcular só os afetados |

**5. Qualidade contínua** (como na ADR-016, sem LLM na decisão):
- **auditoria semanal** de 150 publicadas, sorteadas por disciplina;
- **reportes de alunos** como sinal de prioridade;
- **deriva** por lote de importação: similaridade máxima, margem e taxa de fora.

## Opções consideradas

### Opção A: manter a cascata da ADR-016, com LLM no N2

**Contras:** proibido pela regra da etapa 2 e centenas de vezes mais caro.

### Opção B: retreinar tudo a cada revisão

**Contras:** instável, e calibraria com dados enviesados (a fila).

### Opção C: kNN contínuo, pesos semanais, calibração só com a auditoria aleatória (escolhida)

**Prós:**
- o sistema aprende no dia seguinte, pelo kNN;
- os pesos ficam estáveis, porque o retreino é semanal e passa pelo portão;
- a calibração continua honesta, porque usa uma amostra aleatória.

## Análise de trade-offs

Sem LLM na decisão, a máquina deixa de ser o custo relevante. O que importa é transformar cada minuto do
professor em melhoria duradoura: o kNN aprende imediatamente, a correção de definição vale para todas as
questões do tema, e a auditoria aleatória mantém a calibração honesta.

## Consequências

- A seção d do relatório traz números medidos no case (vetores por segundo e decisões por segundo),
  extrapolados para 50 mil.
- A interface de revisão precisa registrar a decisão com a versão do sistema, e separar a auditoria da fila.

## Itens de ação

1. [x] Medir no case: tempo de embedding por questão e tempo de decisão para as 659. Embeddings: ~7 textos/s no
   `qwen3-embedding:4b`, numa GPU de 6 GB. Decisão: ~47 s para as 659, quase tudo treino da validação cruzada.
2. [x] Seção d do relatório com a tabela de custo e tempo e o ciclo do professor.
3. [x] Atualizar o diagrama de produção (`relatorio/etapa2/arquitetura_producao.png`) sem LLM na decisão.
4. [x] Marcar a ADR-016 como revista por esta ADR.
