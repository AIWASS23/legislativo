# ADR-015: Repositório e entregáveis

**Status:** Aceito (entregáveis, README, relatório e memo prontos em 17/10/2026; faltam o push público e o e-mail)
**Etapa 2:** A entrega é revista pela ADR-026.
**Data:** 14/10/2026
**Decisores:** Autor do case
**Fase:** 06-entrega (passo 09)
**Relacionadas:** ADR-001, ADR-003, ADR-005, ADR-011, ADR-012, ADR-013, ADR-016

## Contexto

O enunciado pede um **repositório público no GitHub** com:

- `publicacao.csv`: 359 linhas no formato do LEIA-ME;
- `previsao.txt`: quatro linhas mais a explicação;
- o relatório, com **até 5 páginas** (seções a: como pensou, b: diagnóstico, c: produção, d: memo de 1 página para o professor), em PDF ou Markdown;
- o código completo, mesmo que bagunçado;
- um README com "como rodar", "que passos geram o `publicacao.csv`", "decisões tomadas à mão e por quê", modelos usados, custo aproximado e tempo.

O link vai por e-mail para carla@viciodeumaestudante.com.br **até domingo, 18/10**.

O README do enunciado já foi movido para `docs/enunciado/`, e a raiz tem um README do projeto, ainda sem as seções de entrega (ADR-001). Ainda não há um validador de formato.

## Decisão

**1. Estrutura final do repositório**

```
/
├── README.md                 ← nosso: como rodar, passos, modelos, custo, tempo, decisões
├── decisoes_manuais.md       ← toda decisão tomada à mão (ADR-005, 010, 012)
├── relatorio/                ← entregáveis
│   ├── publicacao.csv
│   ├── previsao.txt
│   ├── relatorio.md          ← seções a–d (≤ 5 páginas); o memo é a seção d
│   └── relatorio.pdf         ← o mesmo relatório em PDF
├── docs/
│   ├── adr/                  ← este plano
│   └── enunciado/            ← README original do case e PDF
├── anexos/                   ← dados originais, intocados
├── dados/                    ← preparados, temas (cartões), gold, classificação
├── prompts/                  ← prompts versionados
├── runs/                     ← cache das chamadas (ADR-003)
├── saidas/                   ← eda, experimentos, avaliação, custos, decisão
├── vicio_ia/                 ← código
├── executar_*.py             ← um por passo, mais executar_pipeline.py
└── requirements*.txt, ruff.toml, .python-version, .gitignore
```

**2. Validador obrigatório.** A classe `ValidadorEntrega` roda antes de qualquer envio e falha se:

- o `publicacao.csv` não tiver exatamente as 359 questões, uma vez cada, com as colunas do LEIA-ME;
- `decisao` estiver fora de {publicar, revisar, fora};
- `tema_central_id` estiver vazio em publicar/revisar, preenchido em fora, ou não for publicável (inativo e fantasma proibidos);
- `extras_ids` tiver ID inválido, separador diferente de `;` ou repetir o tema central;
- `confianca` não estiver entre 0 e 1;
- `motivo` estiver vazio em revisar ou fora;
- o `previsao.txt` tiver as linhas fora do formato, o ponto fora do intervalo, ou a cobertura prevista diferente da observada no `publicacao.csv`.

**3. Reprodução sem chave de API.** O `executar_pipeline.py` roda todos os passos. Com o cache `runs/` presente, refaz o `publicacao.csv` sem chamar a API.

**4. Relatório em Markdown**, com páginas contadas pelo PDF exportado. O memo tem linguagem para quem não é técnico: nada de "calibração logística", tudo em termos de "questões", "temas" e "o que preciso de você".

**5. Publicação** (feita pelo autor, não automatizada):

- conferir que `.env` e chaves não estão no histórico do git;
- criar o repositório público;
- enviar o e-mail com o link, com um resumo de 3 linhas e o pedido de confirmação de recebimento.

## Opções consideradas

### Opção A: só os arquivos pedidos, com o código numa pasta

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | Nenhum |
| Efeito na avaliação | Neutro a negativo: a banca não consegue reproduzir nem ver o caminho |
| Prazo | Rápido |

**Prós:** mínimo esforço.
**Contras:** perde a trilha (cache, experimentos, ADRs) que sustenta o raciocínio.

### Opção B: repositório completo, com validador e cache versionado (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Custo | Nenhum |
| Efeito na avaliação | Positivo: tudo verificável; formato garantido |
| Prazo | Sábado e domingo |

**Prós:** a banca roda um comando e chega ao mesmo CSV; nenhum erro bobo de formato.
**Contras:** repositório maior (cache e saídas); exige cuidado com segredos.

## Análise de trade-offs

Um erro de formato no `publicacao.csv` (linha faltando, ID inativo) pode anular o trabalho
todo, e o validador custa uma hora. Versionar `runs/` e `saidas/` aumenta o repositório,
mas é o que torna o caminho auditável. Os dados de entrada já são públicos (o próprio
repositório do case os distribui), então incluí-los não cria risco novo.

## Consequências

- O README do enunciado sai da raiz e vai para `docs/enunciado/`, com os créditos mantidos.
- Domingo fica reservado para revisão e envio. O que faltar entra numa seção "com mais tempo".

## Itens de ação

1. [x] `vicio_ia/entrega/validador.py`: `ValidadorEntrega` e `executar_validacao.py` (15/10). Testado contra uma saída com `revisar` sem tema (pegou as 299 linhas); faltam testes unitários.
2. [x] `executar_pipeline.py`: orquestra os passos 01, 02, 05/06 e 07 e valida a entrega (15/10).
3. [x] Mover `README.md` e o PDF do enunciado para `docs/enunciado/`; escrever o novo `README.md` (versão inicial).
4. [x] Completar o README com passos, modelos, custo, tempo e decisões manuais (17/10).
5. [x] `decisoes_manuais.md`: decisões D1 a D9, cobrindo as ADR-005, 007, 008, 010, 011, 012 e 013 (15/10).
6. [x] `relatorio/relatorio.md`, com o memo como seção d (17/10). O PDF (`relatorio/relatorio.pdf`, 5 páginas) é gerado a partir do Markdown.
7. [ ] Conferir que não há segredos, rodar o portão de qualidade (ADR-001) e o validador (feitos em 17/10), fazer o push público e enviar o e-mail.
