# ADR-014: Experimentos e registro dos becos sem saída

**Status:** Aceito (E0, E2, E3 e E4 em 15/10/2026; E5 em 16/10/2026; E6 e E1 não rodados)
**Etapa 2:** Os experimentos E7 a E12 seguem o protocolo da ADR-024.
**Data:** 14/10/2026 · revisada em 14/10/2026: E6 compara provedores e modelos por papel ([ADR-002](../00-fundacao/ADR-002-provedor-e-modelos-de-llm.md), revisão 2)
**Decisores:** Autor do case
**Fase:** 05-avaliacao (passos 05 a 08)
**Relacionadas:** ADR-002, ADR-003, ADR-006, ADR-007, ADR-008, ADR-009, ADR-011, ADR-012, ADR-016, ADR-017

## Contexto

- **O relatório pede o raciocínio** (seção a): "hipóteses, o que você testou, o que descartou e por quê. Queremos ver o caminho, inclusive os becos sem saída."
- **Quatro decisões do plano dependem de medição:**
  - o valor dos cartões (ADR-007);
  - o ganho do ensemble e do verificador (ADR-008);
  - os embeddings (ADR-009);
  - o provedor, o modelo e o esforço de cada papel (ADR-002, ADR-017).
- **As notas de qualidade do catálogo de modelos são estimativas** (`config/catalogo_modelos.json`). O recomendador escolhe os modelos com base nelas até que sejam medidas.
- **As CLIs de assinatura variam muito em tempo e tokens.** No teste de 14/10/2026, o mesmo modelo levou de 4 a 29 s. Velocidade também precisa ser medida, não suposta.
- **O risco é sobreajustar.** Com 60 questões de desenvolvimento, iterar sem disciplina faz parecer que tudo funciona.

## Decisão

Rodar um **conjunto fixo de experimentos** no gold set (ADR-012), com protocolo e registro padronizados:

| ID | Hipótese | Configuração | Decide |
|---|---|---|---|
| **E0** | O assunto de origem é um rótulo ruim | Publicar pelo assunto quando ele bate com um único nó válido | Tamanho do problema (diagnóstico) |
| **E1** | Embeddings acrescentam sinal independente | Top-1 e top-5 questão × cartões; ganho na calibração | ADR-009 (opcional) |
| **E2** | Um LLM sozinho é "razoável, mas não publicável" | Classificador A sozinho; curva precisão × cobertura pela autoconfiança | Ponto de partida |
| **E3** | O prompt hierárquico erra de forma diferente do plano | B × A: acerto e correlação dos erros | Manter B no ensemble |
| **E4** | Cartões reduzem o erro entre irmãos | A com títulos × A com cartões | ADR-007 |
| **E5** | Ensemble + verificador + recuo aumentam a cobertura a 95% | Pipeline completo × E2 | Arquitetura (ADR-008, ADR-010) |
| **E6** | A escolha automática de modelo por papel é a melhor disponível | Para cada papel, os candidatos prontos de cada provedor e as variantes de esforço (ex.: Claude Opus pela CLI × Gemini Flash `-low` × `-medium` pelo `agy` × modelo local; no perfil `claude-api`, Opus × Sonnet × Haiku) | Notas reais de qualidade e velocidade no catálogo; escolha por papel (ADR-002, ADR-017); modelo do voto barato em produção (ADR-016) |

**Protocolo**

1. **Métricas iguais em todos:** acerto top-1 pela régua (estrita e tolerante), curva precisão × cobertura, **cobertura a 95% de precisão**, custo por questão (ou cota, nas assinaturas), latência média e p95, e tokens por chamada.
2. **Uma mudança por vez:** mesmo texto canônico, mesmo cache, mesmo gold.
3. **Congelamento na sexta:** a partir daí, nenhum prompt ou regra muda.
4. **Registro automático:** cada execução grava uma linha em `saidas/experimentos/resultados.csv`, com o provedor e o modelo de cada papel (de `saidas/infra/escolha_resolvida.json`).
5. **Fechar o ciclo do E6:** o acerto medido vira a `qualidade` (1 a 5) do modelo no catálogo e a latência medida substitui a heurística de velocidade do recomendador. A nova escolha automática é registrada.
6. **Diário:** `saidas/experimentos/registro.md` traz, para cada experimento, **hipótese → resultado → decisão**, inclusive quando a hipótese caiu. É a matéria-prima da seção (a) do relatório.

## Opções consideradas

### Opção A: iterar livremente e relatar só o resultado final

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | Variável |
| Efeito na avaliação | Negativo: a banca quer o caminho; resultados otimistas por sobreajuste |
| Prazo | Parece mais rápido |

**Prós:** menos burocracia.
**Contras:** não sobra nada para a seção (a); risco de enganar a si mesmo.

### Opção B: conjunto fixo, protocolo e diário (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa a média |
| Custo | Rodadas no gold (60 questões): sem custo marginal em assinatura e local; no perfil `claude-api`, incluso no orçamento da ADR-002 |
| Efeito na avaliação | Positivo: decisões justificadas por números; becos sem saída documentados |
| Prazo | Quinta e sexta |

**Prós:** cada decisão do plano tem evidência; o relatório se escreve sozinho em parte.
**Contras:** menos liberdade para explorar ideias fora da lista. Ideias novas entram como E7+ com o mesmo protocolo.

## Análise de trade-offs

O diário custa minutos por experimento e é exatamente o que a banca pede. O congelamento
antes da rodada final e a medida fora da amostra (validação cruzada) tornam a previsão (ADR-013)
mais confiável. Sem eles, a precisão estimada estaria medida nos dados usados para ajustar.

## Consequências

- O relatório (seção a) tem uma tabela de experimentos com os números e uma linha por beco sem saída.
- Mudanças posteriores ao congelamento precisam ser declaradas no relatório como "depois do congelamento".
- A escolha de modelos fica congelada junto com os prompts: depois do congelamento, `config/escolha_modelos.json` fica em modo manual com a escolha validada pelo E6, para que uma mudança na máquina (um modelo novo baixado, uma chave configurada) não troque o modelo de um papel no meio da avaliação.

## Implementação (15/10/2026)

- `uv run python executar_experimentos.py` roda E0, E2 e E3 (e E3b, o voto barato sozinho) no gold e
  acrescenta uma linha por experimento e modo da régua em `saidas/experimentos/resultados.csv`.
- Métricas (`vicio_ia/avaliacao/metricas.py`): acerto top-1, precisão entre as questões com tema e
  cobertura a 95% pela curva de precisão × cobertura. O E3 também conta os erros em comum de A e B,
  contra o esperado se fossem independentes.
- **E4 adaptado à cota (15/10):** a ADR previa o E4 com o classificador A, mas a cota dele (`codex`) é a
  mais escassa. O E4 roda com o classificador B (Gemini), mudando só o material: escopo e cartões, ou só
  ID e caminho (`executar_experimento_cartoes.py`).
- **E2 e E3 (15/10), 60 questões, régua estrita:** A (GPT) e B (Gemini) acertam 52 de 60 (87%); pela
  tolerante, 98% e 100%. O voto barato (GPT-OSS) acerta 30 de 60 (50%). A e B erram juntos em 4 questões,
  contra ~1 se fossem independentes: os erros são correlacionados, o que justifica o verificador.
- **E4 (15/10), 60 questões:** B com escopo e cartões acerta 52 de 60 (87%); só com títulos, 53 de 60 (88%).
  O acerto não muda (uma questão de diferença). A cobertura a 95%, que depende de a autoconfiança ordenar
  bem as questões, sobe de 62% para 78% com os cartões.
  - **Decisão:** manter os cartões; eles não custam acerto e melhoram a separação entre o certo e o
    duvidoso, que é o que a régua mede.
  - **Ressalva:** com 60 questões, a diferença de cobertura ainda é ruidosa. A hipótese "cartões reduzem o
    erro entre irmãos" não se confirmou no acerto top-1.
- **E5 (16/10), P fora da amostra:** pipeline completo × A sozinho, no mesmo número de publicadas:
  top 28: 28/28 × 27/28; top 40: 37/40 × 38/40; top 50: 47/50 × 46/50. Precisão parecida.
  - **O ganho do pipeline é saber onde parar:** a faixa de consenso total tem 28/28 e é certificável.
    A autoconfiança de A não é calibrada: ele declara 0,99 em questões erradas. Os 3 erros da faixa
    "confirma parcial" têm autoconfiança de 0,86 a 0,99.
  - Cobertura a 95% no gold: 47% ordenando pela P calibrada e 35% pela chance efetiva, que desconta um
    risco de convenção que o gold não mede.
- **Primeiro resultado (E0, 15/10):** publicar pelo assunto de origem, quando ele aponta um único nó
  válido, acerta 12 de 33 (36%) na régua estrita. O rótulo de origem é ruim, como previa a ADR-006.

## Itens de ação

1. [x] `vicio_ia/avaliacao/experimentos.py` (E0, E2, E3), `experimento_cartoes.py` (E4) e `metricas.py` (`AvaliadorGold`), em vez de uma classe base por experimento (15/10).
2. [x] `executar_experimentos.py` e `executar_experimento_cartoes.py` atualizam `saidas/experimentos/resultados.csv` (15/10).
2b. [x] E5 (pipeline completo × A sozinho), com P fora da amostra (16/10).
2c. [ ] E6 (modelos por papel), se a cota permitir.
3. [x] `saidas/experimentos/registro.md`: hipótese → resultado → decisão de E0, E2, E3, E4, E5 e da calibração (16/10).
4. [x] Congelamento marcado em `registro.md` e em `congelamento.json` (34 arquivos com SHA-256, inclusive a escolha de modelos), em 16/10, 13:02 (`executar_congelamento.py`; D11).
5. [ ] E6: atualizar `qualidade` no `config/catalogo_modelos.json` com o acerto medido e passar a usar a latência medida como nota de velocidade (ADR-017, item 7).
