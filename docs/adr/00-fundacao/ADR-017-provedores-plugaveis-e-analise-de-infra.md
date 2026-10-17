# ADR-017: Provedores de LLM plugáveis e escolha de modelos pela infraestrutura

**Status:** Aceito (implementado em 14/10/2026). Implementa a escolha de provedores e modelos da [ADR-002 (revisão 2)](ADR-002-provedor-e-modelos-de-llm.md).
**Data:** 14/10/2026
**Decisores:** Autor do case
**Fase:** 00-fundacao (passos 02, 05 e 06)
**Relacionadas:** ADR-001, ADR-002, ADR-003, ADR-008, ADR-009, ADR-014, ADR-016

## Contexto

- **A revisão 1 da ADR-002 amarrava o pipeline à API da Anthropic.** A revisão 2 passou a exigir independência de fornecedor; esta ADR registra como isso foi implementado:
  - o enunciado diz "use as suas ferramentas (assinatura, créditos de API, modelos locais)";
  - quem avaliar pode rodar o código numa máquina com outras credenciais;
  - o ensemble (ADR-008) ganha independência quando mistura famílias de modelos.
- **Provedores pedidos:** Ollama (local), Claude, Hugging Face, OpenAI e Gemini via `agy`.
- **Escolhas feitas com o usuário:**

| Provedor | Como chama |
|---|---|
| Gemini | CLI `agy` do Antigravity, com assinatura |
| Claude | Dois caminhos: API (chave) e CLI `claude -p` (assinatura) |
| Hugging Face | Inference Providers remoto (`HF_TOKEN`), mais GGUF do Hub rodando localmente pelo Ollama (`hf.co/...`), sem PyTorch |

- **A escolha deve olhar a máquina.** A memória de GPU decide quais modelos locais rodam, e com que contexto. O usuário pode escolher os modelos ou aceitar uma sugestão automática.
- **Máquina de desenvolvimento** (perfil coletado em 14/10/2026):
  - Ryzen 7 7735HS, 32 GB de RAM;
  - RTX 4050 com 6 GB de VRAM;
  - Ollama 0.34 com `qwen3.5:4b` e `codellama:7b`;
  - CLIs `claude` 2.1.299 e `agy` 1.3.5 (esta com 10 modelos: Gemini 3.8 Flash, Claude Opus/Sonnet 5.5, GPT-OSS 120B);
  - token do HF; sem chaves da Anthropic ou da OpenAI.

## Decisão

**1. Contrato único** (`vicio_ia/llm/contratos.py`):

- `ProvedorLLM.gerar(RequisicaoLLM, modelo) -> RespostaLLM`.
- A resposta é padronizada: texto, JSON decodificado, tokens (entrada, saída, cache, raciocínio), latência, motivo de parada e custo (quando o provedor informa).
- Classificadores e verificador só conhecem esse contrato.

**2. Seis provedores** (`vicio_ia/llm/provedores/`), criados por nome na `FabricaProvedores`:

| Provedor | Acesso | Como chama | Saída estruturada |
|---|---|---|---|
| `ollama` | local | API HTTP `/api/chat` (biblioteca padrão); `num_ctx` fixo; `think` só em modelos com essa capacidade | `format` = JSON Schema |
| `claude-api` | API | SDK `anthropic`; `fallbacks="default"` nos modelos que aceitam; recusa vira erro | `output_config.format` |
| `claude-cli` | assinatura | `claude -p` com `--system-prompt`, sem ferramentas nem MCP, sem salvar sessão, em pasta vazia; tarefa pela entrada padrão | `--json-schema` → `structured_output` |
| `gemini-agy` | assinatura | `agy -p` em `--sandbox`, pasta vazia; instruções no início do prompt (a CLI não troca o prompt de sistema) | `--json-schema` → `structured_output` |
| `openai` | API | SDK `openai` 3.x, Chat Completions | `response_format` JSON Schema estrito |
| `huggingface` | API | Mesmo cliente, roteador `router.huggingface.co/v1`; token do ambiente ou do `hf auth login` | JSON Schema não estrito |

**3. Análise da infraestrutura** (`vicio_ia/infra/`):

- **`AnalisadorInfra`** coleta:
  - CPU, RAM total e disponível;
  - GPUs (`nvidia-smi`, `rocm-smi`, Apple Silicon e as integradas via `lspci`, só como informação);
  - disco livre;
  - Ollama (versão, modelos instalados e metadados de arquitetura via `/api/show`);
  - CLIs (`claude --version`, `agy models`);
  - presença de credenciais, sem nunca expor valores.
- **`EstimadorMemoria`** soma os pesos do modelo, o cache de atenção e uma sobrecarga.
  - O cache por token vale camadas com cache × cabeças KV × (dim. chave + dim. valor) × bytes.
  - Em modelos híbridos, contam só as camadas de atenção completa.
  - O resultado diz se o modelo roda na GPU inteira, dividido com a CPU ou só na CPU, e qual o maior contexto que cabe na GPU.
- **`CatalogoModelos`** junta o arquivo editável `config/catalogo_modelos.json` com o que foi descoberto na máquina (modelos do Ollama e do `agy`).
  - Modelos de código são marcados como inadequados.
  - Nomes não confirmados ficam com `verificar: true` e não entram na escolha automática até serem testados.
- **`RecomendadorModelos`** dá notas de 1 a 5 de qualidade, custo e velocidade e calcula a pontuação com pesos configuráveis (0,6 / 0,2 / 0,2). Depois escolhe um modelo por papel:

| Papel | Regra |
|---|---|
| Classificador A | Melhor pontuação |
| Classificador B | Melhor de **outra família** |
| Voto barato | Local antes de assinatura e API; depois velocidade; depois qualidade |
| Verificador | Maior qualidade |

**4. Escolha** em `config/escolha_modelos.json`:
- `"modo": "auto"` (padrão, também quando o arquivo não existe) usa o recomendador.
- `"modo": "manual"` fixa o provedor e o modelo de cada papel.
- O arquivo é gerado por `executar_escolha_modelo.py`, que pergunta no terminal, sem argumentos, ou editado à mão.
- O `SeletorModelos` resolve os papéis e registra o resultado em `saidas/infra/escolha_resolvida.json`.

**5. Pontos de entrada:**

| Comando | Faz |
|---|---|
| `executar_infra.py` | Gera `saidas/infra/relatorio_infra.md` |
| `executar_escolha_modelo.py` | Escolha interativa dos modelos |
| `executar_teste_llm.py` | Uma questão simples por modelo escolhido; mostra latência, tokens e se acertou |

## Medições na máquina de desenvolvimento (14/10/2026)

Questão de teste: furto de celular, com 3 opções de tema. Todos acertaram.

| Provedor:modelo | Latência | Tokens de entrada | Tokens de saída | Observação |
|---|---|---|---|---|
| `claude-cli:claude-opus-5-5` | 4,5 s | 1.244 | 151 | Equivalente de lista US$ 0,013 (assinatura) |
| `gemini-agy:claude-opus-5-5-low` | 11,7 s | 40.613 | 350 | O agente acrescenta o próprio prompt |
| `gemini-agy:gemini-3.8-flash-low` | 4–29 s | ~13.000 | ~2.700 | Variação grande entre chamadas |
| `gemini-agy:gemini-3.8-flash-high` | **271 s** | 66.166 | 33.698 | Inviável em lote: ~27 h para 359 questões |
| `gemini-agy:claude-sonnet-5-5-low` | 6,0 s | 20.166 | 206 | |
| `ollama:qwen3.5:4b` | 6,9 s | 122 | 66 | Dividido entre GPU e CPU com 16 mil tokens de contexto |

Essas medições calibraram o recomendador:
- a velocidade base das CLIs ficou em 3;
- variantes do `agy`: `-low` fica neutra, `-medium` perde 1 e `-high` perde 2.

Escolha automática resultante nesta máquina:

| Papel | Modelo |
|---|---|
| Classificador A | `claude-cli:claude-opus-5-5` |
| Classificador B | `gemini-agy:gemini-3.8-flash-low` |
| Voto barato | `ollama:qwen3.5:4b` |
| Verificador | `claude-cli:claude-opus-5-5` |

## Opções consideradas

### Opção A: manter só a API da Anthropic (ADR-002, revisão 1)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | ~US$ 0,08 por questão (exige chave) |
| Efeito na régua | Bom, mas com diversidade só dentro de uma família |
| Portabilidade | Baixa: sem chave, nada roda |

**Prós:** Batch e cache de prompt; um único SDK.
**Contras:** não roda nesta máquina hoje (sem chave); ignora assinaturas e GPU local.

### Opção B: biblioteca de gateway (ex.: LiteLLM)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média (dependência grande) |
| Custo | Nenhum |
| Efeito na régua | Neutro |
| Portabilidade | Boa para APIs; **não cobre as CLIs de assinatura** |

**Prós:** muitos provedores prontos.
**Contras:** não chama `claude -p` nem `agy`; tipagem fraca para o `mypy --strict`; esconde detalhes que importam (cache, fallback, `num_ctx`).

### Opção C: contrato próprio + provedores finos + recomendador pela infraestrutura (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média (~1.500 linhas, tudo tipado e testado no portão) |
| Custo | Nenhum; o usuário escolhe entre assinatura, API e local |
| Efeito na régua | Positivo: ensemble com famílias diferentes (Claude, Gemini, Qwen) |
| Portabilidade | Alta: a escolha se adapta à máquina e às credenciais |

**Prós:** roda com o que houver na máquina; a escolha fica registrada; adicionar um provedor é uma classe nova.
**Contras:** as CLIs não têm Batch nem cache de prompt e são mais lentas; o `agy` gasta muitos tokens por chamada.

## Análise de trade-offs

O ganho principal é de independência, que é o que dá valor ao ensemble (ADR-008). A
Opção C permite Claude, Gemini e um modelo local, cada um com erros diferentes, sem nenhuma chave paga.

O custo é velocidade e previsibilidade nas CLIs: o mesmo modelo variou de 4 a 29 s. Isso
pede cache de chamadas (ADR-003) e paralelismo moderado nas rodadas completas.

As notas de qualidade do catálogo são estimativas, mas agora há como medi-las: o
experimento E6 (ADR-014) roda cada provedor no gold e substitui a estimativa pelo número real.

## Consequências

- A ADR-002 (revisão 2) define o requisito, os provedores, os papéis e os critérios; esta ADR define o analisador da máquina, o catálogo, a estimativa de memória e o recomendador que aplicam esses critérios.
- A chave do cache de chamadas (ADR-003) precisa incluir o provedor, além do modelo.
- O README do case informa os provedores e modelos realmente usados, a partir de `saidas/infra/escolha_resolvida.json`.
- `claude-api` e `openai` foram verificados pelo mypy contra os SDKs instalados, mas não foram chamados de verdade (não há chave nesta máquina). Testar quando houver chave.

## Itens de ação

1. [x] Contrato e seis provedores (`vicio_ia/llm/`), mais a fábrica. Sétimo provedor, `codex-cli`, em 15/10.
2. [x] Analisador, catálogo, estimador de memória e recomendador (`vicio_ia/infra/`).
3. [x] `executar_infra.py`, `executar_escolha_modelo.py` (testado com terminal simulado) e `executar_teste_llm.py` (3 provedores reais testados).
4. [x] `openai==3.31.0` em `requirements.txt`; portão de qualidade aprovado (46 arquivos).
5. [x] Integrar o cache de chamadas (ADR-003) ao contrato, com chave incluindo o provedor (`ClienteLLM`, 15/10).
6. [x] Paralelismo limitado por provedor nas rodadas completas (CLIs e Ollama) (`ParametrosLLM.paralelismo`, 15/10).
7. [ ] Usar as latências medidas por `executar_teste_llm.py` como nota de velocidade, no lugar da heurística.
8. [ ] (fora do escopo sem credencial) Testar `claude-api`, `openai` e os modelos `huggingface` marcados `verificar` quando houver credencial ou confirmação.
9. [ ] No E6, medir a qualidade real de cada candidato no gold e atualizar o catálogo.
