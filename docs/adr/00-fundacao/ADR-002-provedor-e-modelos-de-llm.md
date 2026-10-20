# ADR-002: Provedores e modelos de LLM

**Status:** Aceito (revisão 2: independência de provedor)
**Etapa 2:** Os provedores servem só à fase de conhecimento (ADR-019).
**Data:** 14/10/2026 (revisão 1) · revisada em 14/10/2026 (revisão 2)
**Decisores:** Autor do case
**Fase:** 00-fundacao (passos 02, 05 e 06)
**Relacionadas:** ADR-003, ADR-007, ADR-008, ADR-014, ADR-016, ADR-017

## Histórico

| Revisão | Data | Mudança |
|---|---|---|
| 1 | 14/10/2026 | API da Anthropic, um modelo Claude fixo por papel (Opus, Sonnet, Haiku). |
| 2 | 14/10/2026 | **Novo requisito: não depender de um fornecedor.** Qualquer um de seis provedores pode atender os papéis. O modelo de cada papel é escolhido de acordo com a máquina e as credenciais, automaticamente ou pelo usuário. A configuração da revisão 1 vira uma das opções e o perfil do provedor `claude-api`. Implementação do analisador e do recomendador: [ADR-017](ADR-017-provedores-plugaveis-e-analise-de-infra.md). |

## Contexto

- **A classificação depende de entender texto jurídico.** As questões não vêm rotuladas, os rótulos de origem não servem como gabarito (ADR-006) e só 20 dos 373 temas abaixo das disciplinas têm descrição de verdade (EDA, seção 11).
- **O volume é pequeno.** São cerca de 82 mil tokens de texto limpo nas 359 questões (EDA, seção 4). A árvore com ID e caminho ocupa ~7,5 mil tokens; com os cartões de tema (ADR-007), ~20–30 mil.
- **O ensemble precisa de diversidade.** A arquitetura de classificação (ADR-008) depende de classificadores com erros pouco correlacionados.
- **Novo requisito (revisão 2): independência de provedor.**
  - O enunciado diz "use as suas ferramentas (assinatura, créditos de API, modelos locais)".
  - A banca pode rodar o código numa máquina com outras credenciais.
  - A máquina de desenvolvimento **não tem chave da Anthropic nem da OpenAI**. Tem assinaturas acessadas por CLI (`claude` e `agy`), GPU de 6 GB com Ollama e token do Hugging Face.
  - Provedores pedidos: Ollama, Claude, Hugging Face, OpenAI e Gemini via `agy`.
  - Escolhas feitas com o usuário: Gemini pela CLI `agy` (assinatura); Claude pela API **e** pela CLI `claude -p`; Hugging Face remoto (Inference Providers) **e** GGUF do Hub rodando localmente pelo Ollama.
- **Restrições dos modelos Claude atuais:**
  - Opus 5.5 e Sonnet 5.5 **não aceitam `temperature`**. A diversidade tem que vir de modelos e prompts diferentes, não de amostragem.
  - Esses modelos **não aceitam `tool_choice` forçado**. A saída estruturada sai por `output_config.format`.
  - No Opus 5.5 o raciocínio não pode ser desligado; o controle é o `effort` (padrão `medium`).
- **Restrições medidas nas CLIs de assinatura** (ADR-017, 14/10/2026):
  - o `agy` acrescenta o prompt do agente a cada chamada: 13–66 mil tokens de entrada numa questão trivial;
  - a variante `gemini-3.8-flash-high` levou 271 s; as variantes `-low` levaram de 4 a 29 s;
  - a CLI `claude` respondeu em 4,5 s com 1,2 mil tokens.

## Decisão

**1. Requisito de independência.** Nenhuma etapa chama SDK ou CLI de LLM diretamente.
- Tudo passa pelo contrato `ProvedorLLM` (`vicio_ia/llm/`): requisição, resposta padronizada, tokens, latência e custo.
- Qualquer provedor pode atender qualquer papel; basta **um** disponível para o pipeline rodar.

**2. Provedores suportados:**

| Provedor | Acesso | Precisa de | Custo marginal | Principais limites |
|---|---|---|---|---|
| `ollama` | local | Ollama rodando + modelo baixado (inclui `hf.co/...`) | zero | Memória da GPU (contexto × tamanho do modelo); modelos pequenos têm qualidade baixa |
| `claude-cli` | assinatura | CLI `claude` com login | cota da assinatura | Sem Batch nem cache controlável; prompt de sistema até ~120 KB |
| `gemini-agy` | assinatura | CLI `agy` com login | cota da assinatura | Sobrecarga de tokens do agente; variantes `-high` lentas; prompt até ~120 KB |
| `claude-api` | API | `ANTHROPIC_API_KEY` ou `ant auth login` | por token | Precisa de chave |
| `openai` | API | `OPENAI_API_KEY` | por token | Precisa de chave |
| `huggingface` | API | `HF_TOKEN` ou `hf auth login` | por token (varia) | Disponibilidade varia por modelo; schema não estrito |

**3. Papéis definidos por critério, não por modelo:**

| Papel | Para quê | Qualidade mínima (1–5) | Critério de escolha |
|---|---|---|---|
| Classificador A (árvore plana) | Classificação principal | 3 | Maior pontuação (qualidade 0,6 · custo 0,2 · velocidade 0,2) |
| Classificador B (hierárquico) | Segunda opinião independente | 3 | Melhor pontuação de **outra família** que A |
| Voto barato | Terceira opinião; candidato a produção (ADR-016) | 1 | O mais barato (local, depois assinatura, depois API), depois o mais rápido, depois o de maior qualidade |
| Verificador contrastivo | Decidir entre irmãos, o erro que a régua pune | 4 | Maior qualidade |
| Rascunho dos cartões de tema | Roda uma vez, com revisão humana (ADR-007) | 4 | Usa o modelo do verificador |

**4. Como o modelo de cada papel é definido:**
- **Automático** (padrão): o recomendador da ADR-017 avalia os candidatos contra a máquina (memória, credenciais, CLIs) e aplica os critérios acima.
- **Manual:** `executar_escolha_modelo.py` (perguntas no terminal) ou edição de `config/escolha_modelos.json`.
- A escolha usada fica em `saidas/infra/escolha_resolvida.json` e vai para o README da entrega.

**5. Regras comuns a todos os provedores:**
- Saída estruturada com JSON Schema. O campo de tema é um `enum` só com IDs publicáveis (ADR-005), então um ID inválido nunca sai do modelo.
- Temperatura 0 onde o provedor aceita. A diversidade do ensemble vem de família e prompt, nunca de amostragem.
- Recusa, erro ou resposta sem JSON viram `ErroProvedor`, e a questão vai para `revisar` com o motivo "falha de classificação" (ADR-011).
- Modelo e provedor ficam gravados em cada resposta em cache (ADR-003).

**6. Regras por provedor:**
- **`claude-api`:**
  - `output_config.format` para a saída estruturada;
  - `effort` em `low` para classificar e `medium` para verificar (o E6 decide);
  - `fallbacks="default"` no Opus e no Sonnet 5.5;
  - prefixo da árvore e dos cartões com `cache_control` (leitura a US$ 0,20 por milhão de tokens);
  - **Batch API** (50% mais barata) nas rodadas completas.
- **`claude-cli`:** `--system-prompt` próprio (substitui o do Claude Code), sem ferramentas nem MCP, sem salvar sessão, numa pasta vazia; a tarefa vai pela entrada padrão.
- **`gemini-agy`:**
  - só variantes `-low` (ou `-medium`) em rodadas completas; **`-high` proibido em lote** (271 s por questão);
  - instruções no início do prompt; `--sandbox`; pasta vazia.
- **`ollama`:**
  - `num_ctx` igual ao contexto necessário (16 mil tokens por padrão);
  - raciocínio desligado (`think: false`);
  - só modelos cuja estimativa de memória cabe na máquina (ADR-017).
- **`openai`:** `response_format` com JSON Schema estrito; `max_completion_tokens`.
- **`huggingface`:** roteador compatível com a API da OpenAI; schema não estrito; modelos marcados `verificar` só entram depois de testados.

**7. Escolha atual na máquina de desenvolvimento** (automática, medida em 14/10/2026):

| Papel | Provedor:modelo | Teste (questão trivial) |
|---|---|---|
| Classificador A | `claude-cli:claude-opus-5-5` | Acertou; 4,5 s |
| Classificador B | `gemini-agy:gemini-3.8-flash-low` | Acertou; 4–29 s |
| Voto barato | `ollama:qwen3.5:4b` | Acertou; 6,9 s (dividido entre GPU e CPU) |
| Verificador | `claude-cli:claude-opus-5-5` | Acertou; 4,5 s |

## Opções consideradas

### Opção A: um único modelo forte (Opus 5.5 via API) em tudo

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | ~US$ 0,04 por chamada |
| Efeito na régua | Boa precisão individual, mas sem diversidade: concordância entre chamadas iguais não mede nada |
| Portabilidade | Baixa: sem chave, nada roda |

**Prós:** simples; melhor modelo em cada chamada.
**Contras:** sem `temperature`, mesmo modelo e mesmo prompt dão respostas quase iguais; depende de chave paga.

### Opção B: API da Anthropic com um modelo Claude por papel (revisão 1)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Custo | ~US$ 0,08 por questão por rodada completa (perfil `claude-api`, abaixo) |
| Efeito na régua | Diversidade entre modelos, mas da mesma família |
| Portabilidade | Baixa: exige `ANTHROPIC_API_KEY`, ausente na máquina de desenvolvimento |

**Prós:** Batch, cache de prompt e `fallbacks`; um SDK só.
**Contras:** erros correlacionados (mesma família); não usa assinaturas nem a GPU; não roda sem chave.

### Opção C: só modelos locais (Ollama)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Custo | Zero |
| Efeito na régua | Fraco: com 6 GB de VRAM, só modelos pequenos (qualidade estimada 1–2) rodam inteiros na GPU |
| Portabilidade | Depende da GPU de cada máquina |

**Prós:** sem custo; dados não saem da máquina.
**Contras:** qualidade jurídica insuficiente para classificador principal nesta máquina; no teste, `qwen3.5:4b` trocou "patrimonio" por "Patrimônio Cultural e Histórico".

### Opção D: biblioteca de gateway (ex.: LiteLLM)

**Prós:** muitos provedores prontos.
**Contras:** não chama as CLIs de assinatura (`claude -p`, `agy`); dependência grande, com tipagem fraca para o `mypy --strict`; esconde detalhes que importam (`fallbacks`, `num_ctx`, cache).

### Opção E: provedores plugáveis + papéis por critério + escolha pela máquina (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média (contrato, seis provedores, recomendador; ADR-017) |
| Custo | O que o usuário tiver: zero (local), cota (assinatura) ou por token (API) |
| Efeito na régua | Positivo: ensemble com famílias diferentes (Claude, Gemini, Qwen) |
| Portabilidade | Alta: roda com qualquer provedor disponível |

**Prós:** independência real entre classificadores; roda nesta máquina sem chave paga; a escolha fica registrada; um provedor novo é uma classe nova.
**Contras:** CLIs mais lentas, com latência variável e sem Batch; o `agy` gasta muitos tokens por chamada; as notas de qualidade do catálogo são estimativas até o E6.

## Análise de trade-offs

O argumento decisivo continua estatístico: o plano estima a precisão pela concordância
entre fontes independentes (ADR-008, ADR-013). A revisão 2 **fortalece** esse argumento.
Na revisão 1, a diversidade vinha só de modelos diferentes da mesma família. Agora, A e B
vêm de famílias diferentes sempre que a máquina permite.

O preço é operacional. As CLIs de assinatura não têm Batch nem cache de prompt controlável
e variam muito em latência. Por isso:
- o cache de chamadas (ADR-003) passa a ser obrigatório;
- as rodadas completas precisam de paralelismo limitado por provedor;
- variantes `-high` do `agy` ficam proibidas em lote.

Quando houver chave paga, o perfil `claude-api` volta a ser a opção mais previsível (Batch,
cache, `fallbacks`), e o recomendador o escolhe sozinho pela pontuação.

**Custo por tipo de acesso** (a confirmar com o `usage` real, ADR-003):

| Acesso | Base | Estimativa por rodada completa (359 questões) |
|---|---|---|
| Local (`ollama`) | Energia e tempo da GPU | US$ 0; ~7 s por chamada nesta máquina |
| Assinatura (`claude-cli`, `gemini-agy`) | Cota do plano | US$ 0 marginal; a CLI `claude` informa o equivalente de lista (US$ 0,013 numa chamada trivial) |
| API (`claude-api`, perfil da revisão 1) | Por token | ~US$ 29 (~US$ 15 com Batch); detalhe abaixo |

Perfil `claude-api` (revisão 1), por questão:

| Chamada | Tokens (estimativa) | Custo |
|---|---|---|
| Opus 5.5, classificador A | 25 mil em cache + 0,5 mil de entrada + 1,5 mil de saída | ~US$ 0,037 |
| Sonnet 5.5, classificador B | idem | ~US$ 0,021 |
| Haiku 5.5, voto barato | 25 mil de entrada + 1 mil de saída | ~US$ 0,003 |
| Opus 5.5, verificador (~70% das questões) | 2 mil de entrada + 1 mil de saída | ~US$ 0,028 |
| **Total** | | **~US$ 0,08** |

## Consequências

- Classificadores, verificador e gerador de cartões dependem só do contrato `ProvedorLLM` e do papel. Trocar de modelo ou de fornecedor é mudar a configuração, não o código.
- O README da entrega informa os provedores e modelos realmente usados, a partir de `saidas/infra/escolha_resolvida.json`, e o custo medido.
- Sem `temperature`, a "autoconsistência" por amostragem fica descartada. Isso vai documentado no relatório.
- As ADRs 007, 008, 014 e 016 foram revisadas para falar em papéis em vez de modelos Claude. A ADR-008 ganhou um orçamento de prompt por papel, que respeita o limite de cada provedor; a ADR-016 separa os provedores do case dos de produção.
- Quem rodar o código precisa de pelo menos um provedor. `executar_infra.py` diz quais estão prontos e o que falta.

## Itens de ação

1. [x] `ParametrosLLM` em `vicio_ia/configuracao.py`: papéis, qualidade mínima, pesos, contexto e parâmetros de cada provedor.
2. [x] Contrato `ProvedorLLM`, seis provedores e fábrica (`vicio_ia/llm/`; detalhes na ADR-017).
3. [x] Teste de fumaça por modelo (`executar_teste_llm.py`): `claude-cli`, `gemini-agy` e `ollama` testados de verdade.
4. [ ] (fora do escopo: não há chave de API nesta máquina) `claude-api`: executor de lote (Batch API) e `cache_control` no prefixo da árvore.
5. [x] Integrar o cache de chamadas (ADR-003) ao contrato, com provedor e parâmetros na chave (`ClienteLLM`, 15/10).
6. [x] Paralelismo limitado por provedor nas rodadas completas (`ParametrosLLM.paralelismo`, 15/10).
7. [x] Registrar custo e latência reais por papel depois da primeira rodada completa (`saidas/custos/resumo_custos.md`, 17/10; resumo no README).
8. [ ] E6 (ADR-014): medir a qualidade real dos candidatos no gold e atualizar o catálogo.
9. [x] Atualizar ADR-007, ADR-008, ADR-014 e ADR-016 para falar em papéis em vez de modelos Claude (14/10/2026).
