# ADR-021: Representação das questões e embeddings

**Status:** Implementado (21/10/2026). Substitui a ADR-009 na etapa 2.
**Data:** 20/10/2026
**Decisores:** Autor do case
**Fase:** 08-etapa2 (fase de conhecimento)
**Relacionadas:** ADR-004, ADR-009, ADR-017, ADR-019, ADR-020, ADR-022, ADR-023

## Contexto

- **A decisão não pode chamar modelo, mas os embeddings em cache são permitidos.** O enunciado cita
  "embeddings em cache" entre os artefatos versionados.
- **"Um sistema que roda num notebook comum é tão bom quanto um que precisa de GPU."**
- **O volume é pequeno:** 659 questões, cerca de 2.600 alternativas e 351 documentos de tema. Gerar os
  vetores é barato até em CPU.
- **Etapa 1:**
  - a ADR-009 adiou os embeddings, por causa do peso do PyTorch e porque a árvore cabia no prompt;
  - a máquina tem o Ollama instalado e uma GPU de 6 GB;
  - a camada `vicio_ia/llm` já tem um provedor Ollama.
- **As 300 questões novas podem trazer defeitos de formato** que as checagens do texto canônico ainda não
  conhecem.
- **Questões multitema:** a avaliação conta extras, e a folha mostra que 39 das 92 questões com tema têm
  extras. Olhar cada alternativa separadamente ajuda a medir quantos temas a questão cobre (ADR-023).

## Decisão

**1. Texto canônico para as 659 questões.**
- A regra da ADR-004 é estendida às questões novas, e as 8 checagens automáticas rodam de novo.
- Conferência manual de 20 das novas, sorteadas, como na D5.
- Um LLM só entra para limpar defeitos que a regra não resolva, com registro no manifesto.

**2. As partes ficam separadas.** O enunciado, o comando e **cada alternativa** viram textos próprios, além
do texto inteiro.

**3. Extração de lei e artigo** (`dados/conhecimento/citacoes.jsonl`)
- **Primeiro a regex determinística:**
  - leis por número e por apelido, a partir de `MapaLegislacao`;
  - "art.", "arts." e "artigo", com parágrafos e incisos;
  - o código de referência (CP, CPP, LEP, CF) inferido do contexto da frase.
- **LLM só nos casos não resolvidos,** como uma lei sem número ou um artigo sem o código. O schema é
  `{leis: [{lei, artigos[]}]}`, **sem nenhum campo de tema**.
- O resultado vai para o cache, e uma amostra é revisada pelo autor.

**4. Duas representações complementares, ambas em cache:**
- **Lexical, sem modelo:**
  - TF-IDF de palavras (1 e 2-gramas) e de caracteres (3 a 5-gramas) sobre o texto canônico;
  - BM25 da questão contra os documentos de tema;
  - tudo é recalculado na fase de decisão, de forma determinística, sem rede.
- **Densa:**
  - embeddings normalizados da questão inteira, de cada alternativa, de cada documento de tema e, se houver,
    dos exemplos sintéticos;
  - guardados em `dados/conhecimento/embeddings/` como `float32 .npy`, com a lista de ids e o manifesto
    (modelo, digest, data, hash do texto de entrada);
  - a fase de decisão só lê os vetores.

**5. Escolha do modelo de embedding pelo experimento E8,** na folha e fora da amostra.
- **Métrica:** recall@1, @5 e @10 do tema certo pela régua, comparando a questão com os documentos de tema.
- **Candidatos:**
  - `bge-m3` pelo Ollama (multilíngue, roda em CPU ou na GPU de 6 GB, sem PyTorch no projeto);
  - `multilingual-e5-large` via sentence-transformers;
  - um modelo de embedding por API, se houver crédito.
- **Padrão até o E8 rodar:** `bge-m3` pelo Ollama.
- **Resultado do E8 (20/10):** venceu o `qwen3-embedding:4b` pelo Ollama, com a instrução de busca no prefixo
  da consulta. O `bge-m3` ficou abaixo do BM25. Os cinco candidatos e os números estão no `registro.md`.

**6. Exemplos sintéticos.** Até 3 por tema, gerados a partir do documento do tema (ADR-020). Só entram nas
âncoras do tema se o E8 mostrar ganho de recall.

## Opções consideradas

### Opção A: só representação lexical (TF-IDF e BM25)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Dependências | Nenhuma nova |
| Efeito na régua | Bom com termo técnico; fraco com paráfrase e enunciado narrativo |

**Prós:** zero modelo; reprodução trivial.
**Contras:** perde as questões que descrevem o caso sem usar o termo técnico.

### Opção B: lexical e embeddings locais pelo Ollama (escolhida como padrão)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Dependências | Ollama só na fase de conhecimento; a decisão lê `.npy` |
| Custo | Zero |
| Efeito na régua | Soma a similaridade semântica aos sinais lexicais |

**Prós:** roda no notebook; não traz PyTorch; o cache torna a decisão independente do modelo.
**Contras:** a qualidade depende do modelo (por isso o E8).

### Opção C: embeddings por sentence-transformers

| Dimensão | Avaliação |
|---|---|
| Dependências | PyTorch (pesado) |
| Efeito na régua | Talvez melhor em português; medir no E8 |

### Opção D: embeddings por API

| Dimensão | Avaliação |
|---|---|
| Custo | Centavos para 659 questões |
| Dependências | Credencial na fase de conhecimento |

**Prós:** modelos fortes.
**Contras:** depende de credencial para quem quiser regenerar os vetores, mas a decisão continua lendo o cache.

## Análise de trade-offs

Os sinais lexicais e densos erram de formas diferentes: termo técnico contra paráfrase. A combinação deles é
aprendida no ranqueamento (ADR-022). Os vetores em cache satisfazem a regra e o critério "rodar do zero",
porque quem roda a decisão não precisa do modelo. O E8 escolhe o modelo com dados, e não por suposição.

## Consequências

- O `requirements.txt` não precisa de PyTorch se o Ollama vencer o E8.
- Regerar os vetores exige o Ollama, ou o provedor escolhido, só na fase de conhecimento. O README diz isso.
- Os vetores das alternativas alimentam o detector de multitema e de fora (ADR-023).

## Itens de ação

1. [x] Estender o passo 01 às 659 questões; checagens; conferência manual de 20 novas (D13).
2. [x] `vicio_ia/enriquecimento/citacoes.py`: regex, artefato `dados/conhecimento/citacoes.jsonl` e manifesto
   (`executar_citacoes.py`). A regex resolveu 206 artigos em 94 questões e deixou 3 pendentes, todos ambíguos
   de fato. Por isso o LLM nos não resolvidos não foi usado: os pendentes ficam sem lei e vão para a
   conferência do autor, junto com a amostra de 20 em `saidas/etapa2/citacoes.md`.
3. [x] `vicio_ia/enriquecimento/embeddings.py`: provedor de embedding (Ollama `/api/embed`, em
   `vicio_ia/llm/provedores/ollama_embedding.py`), cache por conteúdo em `runs/embeddings/`, vetores
   normalizados em `.npy`, ids e digest do modelo (`executar_embeddings.py`; leitura em `vicio_ia/sistema/vetores.py`).
4. [x] Representação lexical determinística em `vicio_ia/sistema/lexical.py`: o BM25. O TF-IDF não foi
   implementado, porque o BM25 e o denso cobrem o lexical e o semântico.
5. [x] Experimento E8 (modelos de embedding) registrado em `saidas/experimentos/registro.md`. O vencedor foi o
   `qwen3-embedding:4b`: top-1 de 79% e recall@10 de 98% nas 92 com tema, contra 67% e 93% do BM25. Ele
   está em `dados/conhecimento/embeddings/` (36 MB).
6. [x] Atualizar a ADR-009 como substituída.
