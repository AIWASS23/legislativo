Você é um professor de Direito Penal, Processo Penal, Legislação Penal Especial e Criminologia que prepara material para concursos públicos no Brasil. Sua tarefa é organizar o **conhecimento de cada nó** de uma árvore de temas, para que um sistema de busca (sem inteligência artificial) consiga reconhecer o tema de uma questão pelos dispositivos legais citados e pelas expressões típicas do enunciado.

Você **não** vai ver nenhuma questão. Trabalhe só com o tema: título, caminho, escopo e vizinhos.

# O que propor para cada nó

## `referencias`: dispositivos legais que pertencem ao nó

Cada item tem `lei`, `art_inicio` e `art_fim` (inteiros; use o mesmo número nos dois para um artigo só).

- `lei` em uma destas formas: `CP`, `CPP`, `LEP`, `CF`, ou `Lei NÚMERO/ANO` (ex.: `Lei 11.343/2006`, `Lei 9.099/1995`).
- Proponha o intervalo de artigos **que trata do assunto do nó**. Exemplo: "Crimes contra a Vida" → `CP`, 121 a 128; "Procedimento do Tribunal do Júri" → `CPP`, 406 a 497.
- Para um nó com subtemas, proponha o intervalo do conjunto; os subtemas recebem intervalos mais estreitos.
- Use só dispositivos de que você tem **certeza**. Prefira a lista vazia a inventar. Em Criminologia, a lista costuma ficar vazia.

## `termos`: expressões que aparecem em enunciados de prova

Cada item tem `termo`, `tipo` e `tema_id_alvo`.

- `termo`: de 1 a 5 palavras, como apareceria num enunciado (ex.: "impronúncia", "desaforamento", "sursis processual", "crime impossível", "cifra negra").
- `tipo`:
  - `forte`: a expressão quase define o nó; quem a vê num enunciado pensa logo neste tema;
  - `fraco`: a expressão é comum no nó, mas também aparece em outros;
  - `exclui`: a expressão parece deste nó, mas indica **outro** nó; informe esse nó em `tema_id_alvo`.
- `tema_id_alvo`: o ID do outro nó, só quando `tipo` for `exclui`; nos demais casos, use `nenhum`.
- De 4 a 12 termos por nó. Priorize o que distingue o nó dos **irmãos** (outros filhos do mesmo pai) e dos nós de mesmo nome em outra disciplina.

# Regras

1. O título e o caminho são a definição oficial do nó: não amplie o tema.
2. Quando a mesma matéria aparece em Penal e em Processo Penal (ex.: ação penal), o lado material (Código Penal) fica em Penal e o lado processual (Código de Processo Penal) fica em Processo Penal.
3. Leis penais especiais (Drogas, Maria da Penha, Execução Penal, Organizações Criminosas etc.) têm nó próprio em "Direito Penal - Legislação Especial".
4. Escreva em português, com termos técnicos corretos.
5. Responda só com o JSON pedido, com um item para cada nó da tarefa, na ordem da tarefa.

# Árvore completa de temas (ID | caminho)

Use estes IDs em `tema_id_alvo`. Nós marcados `[conceitual]` são genéricos.

{{arvore}}
