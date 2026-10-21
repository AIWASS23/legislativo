# ADR-019: Fronteira entre o modelo de linguagem e a decisão

**Status:** Implementado (21/10/2026)
**Data:** 20/10/2026
**Decisores:** Autor do case
**Fase:** 08-etapa2 (arquitetura)
**Relacionadas:** ADR-002, ADR-003, ADR-017, ADR-018, ADR-020, ADR-021, ADR-026

## Contexto

- **A regra.** O modelo de linguagem pode entrar antes da decisão, sempre documentado e versionado. Não pode
  escolher o tema, votar, julgar ou validar as questões avaliadas, e a classificação roda sem chamá-lo.
- **A banca vai conferir na prática:** "Rodar de novo, do zero, sem modelo de linguagem na decisão" é um dos
  critérios de avaliação.
- **O repositório já guarda saídas de LLM sobre as questões avaliadas.** São os votos e vereditos da etapa 1
  (`dados/classificacao/sinais.jsonl`, `runs/`). Uma leitura acidental desses arquivos contaminaria a decisão
  sem ninguém perceber.
- **O enunciado pede, no README:** o tempo de execução e a origem de cada artefato.

## Decisão

Separar o sistema em **duas fases, com dois comandos e uma trava técnica** entre elas.

**1. Fase de conhecimento** (`uv run python executar_enriquecimento.py`, pacote `vicio_ia/enriquecimento/`)
- Roda offline e pode chamar LLMs, pela camada `vicio_ia/llm` com cache, e modelos de embedding.
- Produz só os artefatos listados abaixo, em `dados/conhecimento/`, cada um com proveniência.

| Artefato | Pode usar LLM? | Guardado como |
|---|---|---|
| Texto canônico das questões | Só limpeza; a regra determinística da etapa 1 vem primeiro | `dados/preparados/questoes.jsonl` |
| Leis e artigos citados por questão | Sim, só quando a regex não resolve; o schema **não tem campo de tema** | `dados/conhecimento/citacoes.jsonl` |
| Documentos de tema (descrição enriquecida) | Sim, com revisão (ADR-020) | `dados/conhecimento/temas.jsonl` |
| Mapa lei/artigo → tema | LLM propõe, o autor revisa | `dados/conhecimento/mapa_artigos.csv` |
| Dicionário de termos | LLM propõe, o autor revisa | `dados/conhecimento/termos.csv` |
| Exemplos sintéticos por tema (opcional) | LLM propõe a partir do **documento do tema**, nunca de uma questão; o autor revisa | `dados/conhecimento/exemplos_sinteticos.jsonl` |
| Embeddings (questões, alternativas, temas) | Sim (modelo de embedding) | `dados/conhecimento/embeddings/*.npy` + ids |

**2. Fase de decisão** (`uv run python executar_sistema.py`, pacote `vicio_ia/sistema/`)
- Lê os anexos e os artefatos versionados.
- Treina os pesos leves com a folha, calibra e decide.
- Grava `relatorio/etapa2/publicacao.csv` e `relatorio/etapa2/previsao.txt`.
- **Não importa `vicio_ia.llm` nem `vicio_ia.classificacao`, e não abre conexão de rede.**

**3. Proibido em qualquer fase:**
- perguntar a um LLM o tema de uma questão, avaliada ou não, inclusive sob a forma de "extração";
- usar votos, vereditos ou decisões de LLM, entre eles `dados/classificacao/`, `dados/decisao/` e o
  `publicacao.csv` da etapa 1;
- destilar ou treinar com rótulos produzidos por LLM;
- gerar "exemplos" a partir do texto de questões avaliadas.

**4. Proveniência.** Cada artefato aparece em `dados/conhecimento/manifesto.json`, com:
- arquivo e SHA-256;
- origem: `manual`, `regra`, `llm+revisão` ou `embedding`;
- provedor, modelo e versão do prompt (o hash, como no cache da ADR-003), e o digest do modelo de embedding;
- data e comando que gera o artefato;
- revisão humana: quem revisou, quando, quantos itens foram revisados de quantos, e quantos foram
  aprovados, corrigidos ou apagados.

O README mostra esse manifesto como uma tabela "origem de cada artefato".

**5. Trava técnica.**
- **Teste estático:** um teste unitário percorre os imports de `vicio_ia/sistema/` (AST) e falha se encontrar
  `vicio_ia.llm`, `vicio_ia.classificacao`, `anthropic`, `openai`, `requests`, `httpx` ou `urllib.request`.
  Também falha se algum caminho lido apontar para `dados/classificacao/` ou `dados/decisao/`.
- **Trava em tempo de execução:**
  - o `executar_sistema.py` define `VICIO_SEM_LLM=1`, e com essa variável a `FabricaProvedores` levanta
    erro;
  - o mesmo comando substitui `socket.socket.connect` por uma função que levanta erro, de modo que qualquer
    tentativa de rede derruba a execução.
- **Reprodução do zero:** num clone limpo, sem credenciais, sem Ollama e com a rede bloqueada,
  `uv run python executar_sistema.py` precisa gerar o mesmo `publicacao.csv`, byte a byte. O hash fica
  registrado no README e no relatório.

**6. Congelamento.** Depois da revisão humana, os artefatos de conhecimento entram no congelamento (D11), e o
`executar_sistema.py` avisa se algum mudou.

## Opções consideradas

### Opção A: um único pipeline, com uma opção que desliga o LLM

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Risco de violar a regra | Alto: um caminho de código esquecido ainda pode chamar o modelo |
| Auditoria | Difícil |

**Prós:** menos código.
**Contras:** a garantia depende de disciplina, e não de estrutura.

### Opção B: duas fases, sem trava

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Risco | Médio: a separação existe, mas não é verificada |

**Prós:** clara para quem lê.
**Contras:** nada impede uma regressão silenciosa.

### Opção C: duas fases, proveniência e trava estática e em tempo de execução (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Risco | Baixo: a violação vira teste vermelho ou erro em tempo de execução |
| Auditoria | O manifesto e o README respondem "de onde veio cada artefato" |

**Prós:** a regra fica verificável, não só declarada.
**Contras:** mais um teste e um manifesto para manter.

## Análise de trade-offs

A banca vai rodar o sistema do zero. Uma regra que só existe no texto não sobrevive a essa conferência,
porque basta um import esquecido. Com a trava, a afirmação "a decisão não chama modelo" passa a ser
demonstrável. O custo é pequeno: um teste AST e um guarda de socket.

## Consequências

- A fase de conhecimento pode ser cara e lenta, porque roda uma vez e fica em cache. A fase de decisão
  precisa ser rápida (meta: menos de 1 minuto num notebook) e é medida.
- Toda questão nova, em produção, passa pela fase de conhecimento antes da decisão (ADR-027).
- O código da etapa 1 que chama LLMs para classificar continua no repositório como histórico, mas fora dos
  pontos de entrada da etapa 2.

## Itens de ação

1. [x] `vicio_ia/enriquecimento/`: orquestrador da fase de conhecimento e `executar_enriquecimento.py`.
2. [x] `vicio_ia/sistema/`: orquestrador da decisão e `executar_sistema.py`, com `VICIO_SEM_LLM=1` e o
   guarda de socket.
3. [x] `FabricaProvedores`: levantar erro quando `VICIO_SEM_LLM=1`.
4. [x] `dados/conhecimento/manifesto.json` e a classe que o grava e confere.
5. [x] Teste `testes/teste_fronteira_llm.py`: AST dos imports, caminhos proibidos, guarda de rede.
6. [x] Reprodução do zero (clone limpo, sem rede), feita pelo autor (21/10), com o hash do `publicacao.csv` no
   README.
