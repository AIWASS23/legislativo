# ADR-003: Cache de chamadas, reprodutibilidade e custo

**Status:** Aceito (implementado em 15/10/2026)
**Data:** 14/10/2026 · revisada em 15/10/2026: chave com parâmetros do provedor e tentativa; preços vindos do catálogo
**Decisores:** Autor do case
**Fase:** 00-fundacao (passos 02, 05 e 06)
**Relacionadas:** ADR-001, ADR-002, ADR-014, ADR-015

## Contexto

- **A banca quer ver o pipeline completo** ("os prompts, as chamadas a modelos") e pede no README o modelo usado, o custo e o tempo.
- **As chamadas não se repetem igual.** Os modelos usados não aceitam `temperature` (ADR-002), então duas chamadas idênticas podem dar respostas um pouco diferentes. Sem cache, o `publicacao.csv` não seria reproduzível.
- **O plano faz muitas rodadas.** São sete experimentos (ADR-014) e iterações sobre o gold (ADR-012). Pagar de novo por chamadas idênticas seria desperdício.

## Decisão

Toda chamada a modelo passa por um **cache em disco, só de acréscimo**:

- **Chave:** SHA-256 de `(provedor, modelo, versão do prompt, schema, parâmetros, texto de entrada)`. A versão do prompt é o hash do arquivo em `prompts/`.
- **Registro** (uma linha JSON por chamada, em `runs/<papel>/<data>.jsonl`): chave, ID da questão, modelo, resposta estruturada, `stop_reason`, `usage` (entrada, cache lido e escrito, saída), latência, custo calculado e horário.
- **Leitura:** se a chave existe, devolve a resposta gravada sem chamar a API. Para refazer, troca-se a versão do prompt ou se apaga o arquivo do papel.
- **Custo e tempo:** a classe `ContadorCusto` soma o `usage` por papel e por rodada, com a tabela de preços em `configuracao.py`. O README é alimentado por esse relatório.
- **Versionamento:** `runs/` entra no repositório. Assim a banca vê as respostas brutas, e o `publicacao.csv` pode ser refeito do cache **sem chave de API**.

## Opções consideradas

### Opção A: sem cache, chamando a API a cada rodada

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | Alto e repetido |
| Efeito na régua | Negativo: resultados mudam entre rodadas e confundem os experimentos |
| Prazo | Rodadas lentas |

**Prós:** nada a construir.
**Contras:** sem reprodutibilidade; sem trilha para a banca.

### Opção B: cache em disco JSONL, chaveado por hash (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa a média |
| Custo | Paga cada chamada uma vez |
| Efeito na régua | Positivo: experimentos comparáveis |
| Prazo | Algumas horas |

**Prós:** reprodutível; transparente; dá o custo exato.
**Contras:** o diretório `runs/` cresce (alguns MB; aceitável).

### Opção C: ferramenta de observabilidade externa (Langfuse, LangSmith)

**Prós:** interface pronta.
**Contras:** outra conta; dados em terceiros; nada disso pesa na avaliação.

## Análise de trade-offs

A opção B custa pouco e resolve três exigências ao mesmo tempo: reprodutibilidade,
transparência para a banca e o custo que o README tem que informar. A opção C só valeria
em produção, e mesmo lá a ADR-016 propõe guardar as decisões no próprio banco.

## Consequências

- Rodar `executar_decisao.py` com o cache cheio é instantâneo e grátis.
- Mudar uma vírgula num prompt invalida o cache daquele papel. Isso é desejado, mas exige disciplina para não iterar prompt depois do congelamento (ADR-012).
- O custo informado no README é medido, não estimado.

## Implementação

- **Chave:** SHA-256 de provedor, modelo, parâmetros do provedor que mudam a resposta
  (`ProvedorLLM.parametros_cache()`: contexto e raciocínio no Ollama, esforço no `claude-api` e
  no `claude-cli`), versão do prompt (`nome@hash` do arquivo em `prompts/`), prompt de sistema,
  tarefa, schema, limite de saída e **número da tentativa**. A repetição depois de uma resposta
  inválida usa a tentativa 2, para não receber do cache a mesma resposta inválida.
- **Só respostas bem-sucedidas são gravadas.** Falhas de provedor não entram no cache e são
  tentadas de novo na próxima execução.
- **Escrita segura com várias threads** (as rodadas em lote chamam em paralelo). Uma linha
  truncada por interrupção é ignorada na leitura.
- **Cliente por papel** (`ClienteLLM`, criado pela `FabricaClientes`): resolve provedor e modelo
  pelo `SeletorModelos`, consulta o cache, chama, calcula o custo e grava. O modo `somente_cache`
  refaz uma rodada sem chamar nenhum modelo e falha se faltar alguma chamada.
- **Custo:** o informado pelo provedor (a CLI `claude` informa o equivalente de lista); se não
  houver, o preço do catálogo (`config/catalogo_modelos.json`), com cache de prompt lido a 10% e
  escrito a 125%. O resumo separa pago, equivalente de lista, assinatura e local.
- **Escolha de modelos congelada** em `config/escolha_modelos.json` (modo manual, com a sugestão
  automática de 15/10). Assim, uma indisponibilidade passageira (ex.: Ollama parado) não troca o
  modelo de um papel no meio das rodadas, o que mudaria as chaves e misturaria modelos.
- **Conferido em 15/10:** duas rodadas seguidas com Ollama e CLI `claude`; a segunda veio toda do
  cache, sem nenhuma chamada.
- O executor de lote da API (Batch, 50%) não foi feito: não há chave de API nesta máquina, e as
  rodadas usam as assinaturas e o modelo local.

## Itens de ação

1. [x] `vicio_ia/llm/cache.py`: `CacheChamadas` e `RegistroChamada`.
2. [x] `vicio_ia/llm/custo.py`: `TabelaPrecos` e `ContadorCusto`.
3. [x] `vicio_ia/llm/cliente.py`: `ClienteLLM` e `FabricaClientes` (todos os provedores, provedor e parâmetros na chave). Executor de lote do `claude-api`: fora do escopo (sem chave de API).
4. [x] `saidas/custos/resumo_custos.md` e `.json`: custo e tempo por papel e modelo, gerados a cada execução.
5. [x] Conferir: rodar duas vezes seguidas; a segunda não fez nenhuma chamada.
