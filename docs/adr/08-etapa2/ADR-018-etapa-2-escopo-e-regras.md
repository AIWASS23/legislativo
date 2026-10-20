# ADR-018: Etapa 2: escopo, regras novas e o que muda no sistema

**Status:** Aceito (escopo da etapa 2)
**Data:** 20/10/2026
**Decisores:** Autor do case
**Fase:** 08-etapa2 (todas as fases)
**Relacionadas:** ADR-019 a ADR-027; revisa ADR-002, 007, 008, 009, 011, 012, 013, 014, 015, 016 e 017

## Contexto

A Vício abriu uma etapa complementar do mesmo case, com foco no **sistema de classificação** construído
pelo candidato. O enunciado novo está em `docs/enunciado/case-ia-classificacao-de-topicos-ajustes.pdf`, e os
anexos em `anexos/2-ENTREGA/`.

**Prazo.**
- A equipe prefere a entrega completa a uma entrega pela metade.
- Pedidos de mais prazo precisam ser feitos **antes de quinta-feira (22/10)**.
- O limite absoluto é **segunda-feira, 26/10**.

**O que muda em relação à etapa 1.**

| | Etapa 1 | Etapa 2 |
|---|---|---|
| Questões | 359 | **659**. Q0001–Q0359 são as mesmas, byte a byte; Q0360–Q0659 vêm de concursos recentes, "como numa importação nova" |
| Temas | 377 | Os mesmos 377 (`temas.csv` idêntico) |
| Rótulos | Nenhum | `folha_verdade.csv`: **100 questões** classificadas pela equipe, para treinar, calibrar ou testar |
| Avaliação | 359 | As **559** questões fora da folha-verdade |
| Modelo de linguagem | Podia classificar | Só **antes** da decisão, documentado e versionado (detalhes abaixo) |
| Régua de acerto | Tema da equipe, pai ou filho | Tema central **ou um extra** da equipe, ou pai ou filho de um deles |
| Relatório | 5 páginas, seções a–d | **4 páginas**, seções a–e: sistema, os 100 rótulos, diagnóstico, produção e memo |
| Código | Pipeline e README | Um comando que regenera o `publicacao.csv` **sem modelo de linguagem**; artefatos versionados; README com tempo de execução e a origem de cada artefato |

**O que o modelo de linguagem pode e não pode fazer.**
- **Pode, antes da decisão:** gerar embeddings, limpar e normalizar o texto, extrair a lei e o artigo
  citados, enriquecer a descrição dos temas, e propor termos ou exemplos que o autor revisa e guarda como dado.
- **Não pode:** escolher o tema, votar, julgar ou validar as questões avaliadas.
- **Na hora de classificar,** o sistema roda sem chamar nenhum modelo de linguagem.

**Como a equipe avalia.**
- **O que pesa:**
  - a cobertura com precisão ≥ 95% nas questões fora da folha;
  - como os dados foram organizados e o que o sistema aprende com eles;
  - o quanto a previsão acerta o próprio resultado;
  - rodar de novo, do zero, sem modelo de linguagem na decisão.
- **O que não pesa:** modelo sofisticado, infraestrutura e volume de código.

**O que os dados novos mostram** (análise de 20/10, antes de qualquer modelo):

- **A folha-verdade só tem questões antigas.** As 100 estão entre Q0001 e Q0359, e nenhuma das 300 novas
  foi rotulada. O conjunto avaliado tem 259 antigas e 300 novas, então a calibração feita nas antigas
  precisa ser conferida contra uma possível mudança de distribuição (ADR-024, ADR-025).
- **Composição da folha:**
  - 92 questões com tema, em 61 temas distintos;
  - o tema central é de nível 1 em 53 delas e de nível 2 em 39;
  - 39 trazem pelo menos um extra.
- **8 questões são "fora" (8%).** É a convenção mais difícil, e nem sempre intuitiva (ADR-023).
- **O sistema da etapa 1, medido na folha** com a régua nova:
  - publicou 29 questões: 27 certas e 2 erradas, uma precisão de 93%;
  - **os dois erros são questões que a equipe marcou como fora** (Q0039 e Q0303);
  - a sugestão de tema acertou 88 de 100.
- **Convenção dos duplicados (D1):**
  - os nós "(Parte N)" nunca aparecem na folha, o que confirma o nó canônico;
  - a LEP fantasma (`6734`, em Processo Penal) aparece 2 vezes: central em Q0138 e extra em Q0324.
- **O gold manual da etapa 1 coincide com a folha em 14 questões:** 12 concordam, 1 discorda e 1 a equipe
  marcou como fora.
- **As 300 novas trazem 10 questões de Direito Penal Militar ou Processual Penal Militar.** A árvore não
  tem nenhum nó militar.
- **Poucas questões citam artigo de lei:** 57 das 359 antigas (16%) e 36 das 300 novas (12%).

## Decisão

1. **Um sistema próprio, sem modelo de linguagem na decisão,** organizado em duas fases separadas
   (ADR-019):
   - **fase de conhecimento:** offline; pode usar LLM e modelos de embedding; os artefatos ficam
     versionados e com proveniência;
   - **fase de decisão:** um comando, sem LLM e sem rede, regenera o `publicacao.csv` e o `previsao.txt`.
2. **Organizar o conhecimento dos dados como o centro do trabalho:**
   - documentos de tema, mapa de artigos e dicionário de termos (ADR-020);
   - representações das questões (ADR-021);
   - os 100 rótulos (ADR-024).
3. **Classificar por recuperação e ranqueamento aprendido** (ADR-022), com um componente explícito para
   "fora" e multitema (ADR-023).
4. **Manter a régua da etapa 1** (ADR-025):
   - publicar o maior conjunto cujo percentil 10 da precisão estimada fique em 95% ou mais;
   - a previsão vale para as 559 questões avaliadas.
5. **O que continua da etapa 1:**
   - o texto canônico (ADR-004);
   - a árvore preparada e as decisões D1–D4 (ADR-005), revisitadas com a folha;
   - o assunto de origem como sinal fraco (ADR-006);
   - os cartões de tema, como descrição enriquecida (ADR-007, estendida pela ADR-020);
   - o recuo para o pai (ADR-010);
   - o limiar pelo limite inferior (ADR-011, ADR-013);
   - o cache e a proveniência das chamadas (ADR-003);
   - a camada de provedores, **só para a fase de conhecimento** (ADR-002, ADR-017);
   - o validador e o portão de qualidade.
6. **O que sai da decisão:**
   - os classificadores A e B, o voto barato e o verificador da ADR-008;
   - o arquivo `dados/classificacao/sinais.jsonl` e o `publicacao.csv` da etapa 1. São escolhas de tema
     feitas por LLM sobre as questões avaliadas, e o sistema da etapa 2 **não pode lê-los** (ADR-019).
7. **O gold manual de 60 questões vira só medida:** nunca entra em treino nem em decisão (ADR-024).
8. **A entrega da etapa 1 fica preservada** numa tag do git e numa pasta de arquivo (ADR-026).
9. **Cronograma:**
   - entrega completa até **domingo, 25/10**, com segunda, 26/10, de folga;
   - **quarta, 21/10, à noite:** ponto de decisão sobre pedir mais prazo à Carla. Ela pediu aviso antes de
     quinta.

## Opções consideradas

### Opção A: adaptar o pipeline da etapa 1, destilando os rótulos do LLM

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | Nenhum (as respostas estão no cache) |
| Efeito na régua | Alto no papel |
| Regras | **Proibido:** o LLM teria escolhido o tema das questões avaliadas, e a decisão herdaria essa escolha |

**Prós:** rápido.
**Contras:** viola a regra central da etapa. Descartada.

### Opção B: só regras e dicionário de termos

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | Nenhum |
| Efeito na régua | Precisão alta onde a regra dispara, cobertura baixa (só 12–16% citam artigo) |
| Prazo | Rápido |

**Prós:** auditável e trivialmente reprodutível.
**Contras:** não generaliza para os enunciados sem lei citada, que são a maioria.

### Opção C: base de conhecimento, recuperação e ranqueamento aprendido com a folha (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Custo | Baixo: embeddings locais ou em cache; a decisão roda em CPU |
| Efeito na régua | Combina as regras (alta precisão) com a similaridade semântica (cobertura); a calibração vem dos 100 rótulos |
| Prazo | Cabe até 25/10, se a revisão humana dos artefatos for priorizada (ADR-020) |

**Prós:** cumpre a regra; aprende com os dados; cada peça é mensurável e auditável.
**Contras:** 100 rótulos são poucos para aprender, por isso o modelo precisa ter baixa capacidade.

## Análise de trade-offs

A opção C é a única que respeita a regra e ainda usa o que os dados oferecem: a árvore, as leis, os termos e
os exemplos rotulados. O resultado da etapa 1 medido na folha mostra onde está o risco. O LLM acertava o
tema, mas o sistema não sabia reconhecer "fora". Na etapa 2, o componente de fora deixa de ser um detalhe e
passa a decidir se algum conjunto pode ser certificado em 95%.

## Consequências

- As ADRs da etapa 1 continuam válidas como histórico. A tabela abaixo mostra o papel de cada uma nesta etapa.
- O trabalho humano do autor se concentra na **revisão dos artefatos propostos por LLM** (ADR-020), e não na
  rotulagem de questões.
- Os anexos foram movidos para `anexos/1-ENTREGA/` e `anexos/2-ENTREGA/`. O código ainda lê `anexos/` e
  precisa ser ajustado (ADR-026).

| ADR da etapa 1 | Na etapa 2 |
|---|---|
| 002, 017 (provedores) | Só para a fase de conhecimento (ADR-019) |
| 003 (cache) | Vale também para os artefatos de conhecimento |
| 004, 005, 006 (dados) | Continuam; D1 é conferida com a folha (ADR-024) |
| 007 (cartões) | Estendida pela ADR-020 |
| 008 (ensemble de LLMs) | **Substituída** pela ADR-022 na decisão |
| 009 (embeddings opcionais) | **Substituída** pela ADR-021 |
| 010 (recuo para o pai) | Continua, dentro da escolha do nó pela régua (ADR-022) |
| 011, 013 (política, calibração e previsão) | Revistas pelas ADR-023 e ADR-025 |
| 012, 014 (gold e experimentos) | O gold vira só medida; os experimentos novos ficam na ADR-024 |
| 015 (entrega) | Revista pela ADR-026 |
| 016 (produção) | Revista pela ADR-027 |

## Itens de ação

1. [x] Ler o enunciado novo e analisar os anexos (folha, questões novas, temas): 20/10.
2. [x] Medir o sistema da etapa 1 na folha, para o diagnóstico e o relatório: 20/10.
3. [ ] Escrever e implementar as ADR-019 a ADR-027.
4. [ ] Atualizar o índice (`docs/adr/README.md`) com a etapa 2, o cronograma e a definição de pronto.
5. [ ] Quarta, 21/10, à noite: decidir se é preciso pedir mais prazo à Carla.
