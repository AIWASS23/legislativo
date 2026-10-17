# ADR-001: Stack, ambiente e padrão de código

**Status:** Aceito (implementado em 14/10/2026)
**Data:** 14/10/2026
**Decisores:** Autor do case
**Fase:** 00-fundacao (todos os passos)
**Relacionadas:** ADR-003, ADR-015

## Contexto

- O prazo é curto (até 18/10) e a banca quer ver **como** a classificação foi feita, do começo ao fim. Ela diz explicitamente que "código bonito ou infraestrutura sofisticada" não pesa.
- Mesmo assim, quem avaliar precisa conseguir rodar o código e ler cada etapa.
- Padrão de código pedido para o projeto:
  - orientado a objetos;
  - sem argumentos de linha de comando;
  - todas as variáveis tipadas;
  - docstrings em todas as classes e funções.
- Ferramentas pedidas: ambiente gerenciado com **uv** e dependências em **requirements.txt**, mais **ruff** para lint e formatação.
- A EDA (`executar_eda.py`) já foi construída nesse padrão, usando só a biblioteca padrão.

## Decisão

1. **Linguagem e ambiente:**
   - Python 3.12 (fixado em `.python-version`), com ambiente virtual `.venv` criado pelo `uv venv`.
   - Bibliotecas de execução fixadas com `==` em `requirements.txt`: `anthropic`, `numpy`, `scikit-learn`.
   - Ferramentas de desenvolvimento em `requirements-dev.txt`: `-r requirements.txt`, mais `mypy` e `ruff`.
2. **Biblioteca padrão primeiro.** Uma lib nova só entra quando uma etapa precisa dela. Ela é fixada no arquivo certo, com um comentário dizendo qual etapa a usa.
3. **Estrutura de código:**
   - Cada passo do pipeline é um subpacote de `vicio_ia/`, com uma classe orquestradora (`Pipeline<Passo>`) e um ponto de entrada `executar_<passo>.py` sem argumentos.
   - A configuração fica em dataclasses congeladas em `vicio_ia/configuracao.py`.
4. **Padrão obrigatório:**
   - Variáveis tipadas, incluindo as locais. Alvos de `for` e `with` são declarados antes, com tipo.
   - Aliases de tipo usam `type X = ...`.
   - Docstrings no estilo Google, em português.
   - Sem `argparse`, `sys.argv`, `*args` ou `**kwargs`.
5. **Portão de qualidade antes de cada entrega:** `uv run python executar_checagem.py`.
   Ele roda em sequência:
   - `ruff check .`
   - `ruff format --check .`
   - `mypy --strict` em `vicio_ia`, `ferramentas` e `executar_*.py`
   - o verificador de anotações e docstrings (`ferramentas/checar_anotacoes.py`)

   Sai com código 1 se algo falhar. É um ponto de entrada Python, e não um Makefile ou
   script de shell, para seguir o mesmo padrão e funcionar em qualquer sistema operacional.

## Opções consideradas

### Opção A: scripts soltos e notebooks

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | Nenhum |
| Efeito na régua | Neutro |
| Prazo | Rápido no início, lento para refazer as rodadas |

**Prós:** começa rápido; bom para explorar.
**Contras:** difícil reproduzir; estado escondido nas células; a banca não consegue reconstruir o caminho; contraria o padrão pedido.

### Opção B: pacote orientado a objetos + uv + requirements.txt (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Custo | Nenhum |
| Efeito na régua | Indireto: rodadas reprodutíveis permitem medir e iterar |
| Prazo | Compatível; a EDA já está pronta nesse formato |

**Prós:** cada etapa pode ser lida e rodada sozinha; tipagem pega erros cedo; segue o padrão pedido.
**Contras:** mais código do que um script.

### Opção C: `pyproject.toml` + `uv.lock` (projeto uv completo)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Custo | Nenhum |
| Efeito na régua | Neutro |
| Prazo | Compatível |

**Prós:** lock de todas as dependências indiretas; `uv sync` reproduz exatamente.
**Contras:** não é o formato pedido (`requirements.txt`).

## Análise de trade-offs

A opção B troca um pouco de velocidade inicial por rodadas reprodutíveis, que importam
porque o plano depende de iterar prompts e limiares contra o gold set (ADR-012, ADR-014).

A opção C reproduziria melhor as dependências indiretas, mas o formato pedido é
`requirements.txt`. Se a banca tiver problemas para instalar, a saída é gerar um
`requirements.lock.txt` com `uv pip compile`, sem mudar de formato.

## Consequências

- Toda etapa nova segue o molde de `vicio_ia/eda/`: perfis em dataclasses, análises com contrato comum, um orquestrador.
- O portão de qualidade adiciona alguns minutos por etapa.
- As dependências indiretas não ficam fixadas. Rever se aparecer quebra de instalação.

## Itens de ação

1. [x] Criar `.python-version`, `.venv`, `requirements.txt`, `requirements-dev.txt`, `ruff.toml` e `.gitignore`.
2. [x] Construir a EDA no padrão (`vicio_ia/eda/`, `executar_eda.py`).
3. [x] Verificador de anotações em `ferramentas/checar_anotacoes.py` (classes `AnalisadorModulo` e `VerificadorAnotacoes`), testado com um arquivo de violações propositais.
4. [x] Portão de qualidade em um comando: `executar_checagem.py` (classe `PortaoQualidade`, configuração em `ParametrosQualidade`).
5. [x] README do projeto com "Como rodar"; o enunciado original foi para `docs/enunciado/` (ADR-015).
