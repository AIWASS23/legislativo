# ADR-004: Texto canônico das questões

**Status:** Aceito (implementado em 15/10/2026)
**Data:** 14/10/2026 · revisada em 15/10/2026: refinamentos descobertos na implementação e na conferência manual
**Decisores:** Autor do case
**Fase:** 01-dados (passo 01, preparar)
**Relacionadas:** ADR-006, ADR-007, ADR-008, ADR-009

## Contexto

A EDA (`saidas/eda/relatorio_eda.md`, seções 2 a 7) mostrou como as questões chegam:

- **Formato:** 255 de múltipla escolha com 5 alternativas, 46 com 4 e 58 de certo/errado. Nas de certo/errado, as alternativas ("Certo"/"Errado") não dizem nada.
- **HTML:**
  - 171 alternativas com HTML e 83 com quebra de linha no meio da frase.
  - A **Q0099** traz HTML colado do Word: 108.363 caracteres, 24,4% de todo o HTML do recorte, quase tudo CSS e metadados.
  - O recorte tem 443.917 caracteres brutos e ~329 mil depois da limpeza.
- **Escapes literais** (descoberto na conferência manual): **1.043 sequências `\n` e `\t` gravadas como texto** (os dois caracteres, não quebras de verdade), em **106 questões (29,5%)**, quase todas nas alternativas. É um defeito de escape duplo no banco. Por exemplo, "Ministério\nPúblico" na Q0003.
- **Comando:**
  - 101 vazios (7 deles só com `<br>`).
  - **62 suspeitos de terem sido gerados**, como "Explique o que é a prisão preventiva" numa questão de múltipla escolha; 12 estão em questões de certo/errado.
  - **72 repetem o enunciado.** Na maioria, o comando está copiado no fim do enunciado, como "Diante do caso narrado, é correto afirmar que:" na Q0099.
  - 124 úteis, mas **74 deles são só frase-padrão** ("Julgue o item a seguir.", "Assinale a alternativa correta.", esta até em questões de certo/errado).
- **Certo/errado com a afirmação no comando:** em algumas questões, o enunciado é só o contexto e o item a julgar está no comando (ex.: Q0235, "Neste caso, o recurso [...] não terá efeito...").
- **Enunciado genérico:** 18 enunciados não têm nenhuma palavra de conteúdo ("Assinale a alternativa correta"), e o assunto está todo nas alternativas. Outros 10 são curtos mas específicos ("A remição").
- **Repetição:** 13 questões dividem 2 enunciados genéricos, mas nenhuma questão é duplicada quando se compara o texto completo.

## Decisão

O texto que vai para os modelos e para os embeddings é sempre montado pela classe
`MontadorTextoCanonico` (`vicio_ia/preparacao/texto_canonico.py`), no formato:

```
[Q0065] Múltipla escolha (5 alternativas)
Enunciado: O crime de extorsão mediante sequestro (CP, art. 159)
A) é qualificado se do fato resulta lesão corporal grave ou morte.
...
E) consuma-se quando o agente obtém vantagem como preço do resgate...
```

```
[Q0008] Certo ou errado (julgar a afirmação)
Enunciado: A progressão de regime do cumprimento da pena de condenado por crime contra a
administração pública condiciona-se à reparação do dano que ele causou, [...]
```

Regras:

1. **Limpeza** com `ProcessadorTexto.html_para_texto`:
   - converte escapes literais (`\n` vira quebra de linha; `\t` vira espaço);
   - remove comentários e blocos `<style>`, `<script>` e `<xml>` junto com o conteúdo;
   - `<br>` e fim de parágrafo viram quebra de linha; decodifica entidades (`&nbsp;`);
   - o enunciado mantém as quebras de linha (itens I, II, III...); as alternativas ficam numa linha só.
2. **As alternativas entram sempre**, menos em certo/errado.
   - Em certo/errado, o cabeçalho diz "Certo ou errado (julgar a afirmação)" e o texto traz o enunciado e, quando for o caso, o comando.
   - Não se usa o prefixo "Julgue o item: <enunciado>", previsto na primeira versão desta ADR, porque às vezes a afirmação está no comando.
3. **O comando só entra quando é útil e tem conteúdo próprio.** O destino de cada comando fica registrado em `motivo_comando`:

| `motivo_comando` | Regra | Questões |
|---|---|---|
| `incluido` | Útil e com ao menos uma palavra fora das frases-padrão de prova | 50 |
| `so_frase_padrao` | Útil, mas só frase-padrão ("Julgue o item a seguir.") | 74 |
| `repete_enunciado` | Está contido no enunciado (ou o enunciado no começo dele) | 72 |
| `suspeito` | Pede o que não cabe em questão objetiva ("Explique...", "Complete...") | 62 |
| `vazio` | Ausente ou só HTML | 101 |

4. **Os rótulos de origem não entram no texto do modelo** (ADR-006). O montador nem lê esses campos, e uma checagem automática confirma isso (abaixo).
5. **Marcas guardadas junto** (usadas na decisão e na calibração, ADR-011 e ADR-013): `enunciado_generico`, `html_de_editor`, `leis_citadas`, `menciona_cp`, `menciona_cpp`, `menciona_cf`, `menciona_jurisprudencia`, além de `formato` e `hash_completo`.
6. **Deduplicação só pelo texto completo** (`duplicata_de` aponta a primeira ocorrência), nunca só pelo enunciado.
7. **Checagens automáticas a cada execução.** Se alguma falhar, nada é gravado em `dados/`:
   - todas as questões preparadas, uma vez cada;
   - nenhum texto vazio;
   - nenhuma tag HTML;
   - nenhum escape literal;
   - nenhum resíduo de CSS do Word;
   - alternativas completas (e nenhuma em certo/errado);
   - comando presente se e só se `motivo_comando = incluido`;
   - **sentinela de origem:** o texto é refeito com disciplina e assunto trocados por uma sentinela e precisa sair idêntico.

**Saídas** (`uv run python executar_preparacao.py`):
- `dados/preparados/questoes.jsonl`: uma linha por questão, com texto canônico, campos limpos, `motivo_comando`, marcas, hash, tamanho e os campos originais intocados.
- `saidas/preparacao/relatorio_preparacao.md`, `resumo_preparacao.json` e `conferencia_texto_canonico.md` (amostra para conferência manual).

## Opções consideradas

### Opção A: mandar o HTML cru ao modelo

| Dimensão | Avaliação |
|---|---|
| Complexidade | Nenhuma |
| Custo | +35% de tokens; a Q0099 sozinha teria ~30 mil tokens de lixo |
| Efeito na régua | Negativo: ruído, escapes e comandos falsos confundem o modelo |
| Prazo | Imediato |

**Prós:** nada a construir.
**Contras:** caro, ruidoso e difícil de auditar.

### Opção B: texto canônico com regras explícitas e checagens automáticas (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa (a limpeza já existia) |
| Custo | Mínimo |
| Efeito na régua | Positivo: o modelo vê só o conteúdo |
| Prazo | Algumas horas |

**Prós:** cada regra tem um número da EDA por trás; as checagens impedem regressão.
**Contras:** as heurísticas de comando podem errar; o original fica guardado para revisão.

### Opção C: pedir a um LLM para "reescrever" a questão

**Prós:** poderia consertar comandos e frases quebradas.
**Contras:** o modelo pode mudar o conteúdo jurídico, o custo aumenta e não há ganho visível.

## Análise de trade-offs

A opção B remove o ruído medido sem mexer no conteúdo. O único risco é descartar um
comando útil classificado como suspeito, repetido ou frase-padrão. Nos três casos, o
conteúdo continua no texto: o comando suspeito descreve o enunciado, o repetido já está
nele, e a frase-padrão não acrescenta nada. A perda esperada é quase nula.

**Conferência manual (15/10/2026):** a amostra mostrou três defeitos que as checagens
automáticas da primeira versão não pegavam. Todos foram corrigidos e viraram regra ou checagem:
- escapes literais nas alternativas;
- comando duplicado quando copiado no fim do enunciado;
- frase-padrão contada como conteúdo.

Isso confirma o valor de conferir a saída à mão antes de seguir, e não só confiar nas checagens.

## Consequências

- Classificadores, verificador e embeddings recebem exatamente o mesmo texto. Diferenças entre eles vêm do modelo e do prompt, não da entrada.
- Mediana de ~250 tokens por questão (máximo ~1.200; ~98 mil no total). A questão é a parte variável do prompt; a árvore é a parte fixa (ADR-007, ADR-008).
- Questões com enunciado genérico (18) chegam marcadas e exigem mais evidência para serem publicadas.
- Os escapes literais, os comandos suspeitos e os comandos copiados no enunciado entram no diagnóstico (relatório, seção b) como defeitos do banco.
- A EDA passou a usar as mesmas regras (escapes literais, comando contido no enunciado), e os números dela foram atualizados.

## Itens de ação

1. [x] Limpeza de HTML com remoção de blocos de editor e de escapes literais (`ProcessadorTexto`).
2. [x] `vicio_ia/preparacao/texto_canonico.py`: classes `MontadorTextoCanonico`, `QuestaoPreparada` e `MarcasQuestao`.
3. [x] `vicio_ia/preparacao/pipeline.py`: `PipelinePreparacao` grava `dados/preparados/questoes.jsonl`; `vicio_ia/preparacao/validacao.py`: `ValidadorQuestoesPreparadas` (8 checagens).
4. [x] Conferir à mão 10 questões de formatos diferentes, incluindo Q0099, Q0008, Q0090 e Q0122. Três defeitos encontrados e corrigidos (ver "Análise de trade-offs").
5. [x] Ao implementar a ADR-005, estender a `PipelinePreparacao` com a árvore (`temas.json`) no mesmo `executar_preparacao.py` (15/10).
