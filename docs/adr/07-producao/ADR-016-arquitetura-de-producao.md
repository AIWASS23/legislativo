# ADR-016: Arquitetura de produção (50 mil questões por semana)

**Status:** Proposto (desenho da seção c do relatório; não implementado no case). Custos revisados em 17/10/2026 com o perfil de tokens medido
**Data:** 14/10/2026 · revisada em 14/10/2026: modelos por papel e escolha de provedor em produção ([ADR-002](../00-fundacao/ADR-002-provedor-e-modelos-de-llm.md), revisão 2)
**Decisores:** Autor do case; equipe Vício
**Fase:** 07-producao
**Relacionadas:** ADR-002, ADR-003, ADR-005, ADR-007, ADR-008, ADR-009, ADR-011, ADR-013, ADR-014, ADR-017

## Contexto

O relatório (seção c) pergunta como a solução funcionaria "toda semana em 50 mil questões
e com as novas importações":

- que tipos de IA usar e em que ponto (embeddings, classificador treinado, LLM, agentes, revisão humana);
- quanto custaria por questão;
- como medir a qualidade continuamente;
- como encaixar no fluxo de importação, revisão e reportes de alunos.

O que muda em relação ao case:

- **Haverá rótulos.** Cada revisão de professor vira um rótulo validado; com o tempo, milhares.
- **A maior parte da base não muda de uma semana para outra.** Reclassificar tudo toda semana é desperdício.
- **A taxonomia muda** (correção de fantasmas e lixeiras, temas novos), e cada mudança afeta parte da base.
- **Custo e latência pesam mais** que no case, e há tempo de professor, que é escasso.
- **O pipeline já é independente de provedor** (ADR-002, revisão 2): cada papel pode usar qualquer provedor. Mas **o que serve no case não serve necessariamente em produção**:
  - as CLIs de assinatura (`claude -p`, `agy`) usam cotas de planos individuais, não têm processamento em lote e acrescentam a sobrecarga de um agente (até dezenas de milhares de tokens por chamada no teste do case);
  - em produção os candidatos são as **APIs com lote e cache de prompt** e os **modelos abertos servidos em GPU própria** (Ollama ou vLLM).

## Decisão

Uma **cascata de custo crescente**, com decisões versionadas e humanos no ciclo. Os papéis
são os mesmos do case (ADR-008); só mudam os provedores:

```
importação ──► normalizar (ADR-004) ──► hash + quase-duplicatas (embeddings)
                                              │ duplicata de questão validada → herda o tema
                                              ▼
        cache por (hash, versão da taxonomia, versão do pipeline) → só segue o que é novo ou mudou
                                              ▼
 N1  classificador treinado (embeddings + regressão sobre rótulos validados)
     + papel "voto barato" em lote (modelo pequeno: API em lote ou modelo aberto em GPU própria)
        │ concordam e P calibrada alta → decide
        ▼ demais (~30–40%, a medir)
 N2  papéis "classificador A", "classificador B" (famílias diferentes) e "verificador", em lote,
     com a árvore e os cartões em cache de prompt
        ▼
 Política de decisão (ADR-011) com limiar calibrado por disciplina
        ├─► publicar
        ├─► fila do professor (prioridade = impacto × incerteza), com sugestão e 2º colocado
        └─► fora → agrupamento → proposta de tema novo
```

**Onde cada tipo de IA entra**

| Componente | Função | Provedor em produção | Por quê |
|---|---|---|---|
| Embeddings (modelo multilíngue local) | Quase-duplicatas, kNN sobre rótulos validados, agrupar os "fora" | Servidor próprio (CPU ou GPU) | Barato, roda em toda questão; aqui é central (ADR-009) |
| Classificador treinado | Primeiro nível de decisão | Servidor próprio | Custo quase zero; melhora a cada semana de revisões |
| Papel voto barato | Segunda opinião em toda questão nova | API em lote com modelo pequeno (ex.: Claude Haiku 5.5, ~US$ 0,0015 por questão) **ou** modelo aberto em GPU própria | O mais barato que passar no gold de regressão |
| Papéis A, B e verificador | Só nos casos incertos | APIs em lote, de famílias diferentes (ex.: Claude + Gemini ou OpenAI), com cache de prompt | Onde a qualidade compensa; famílias diferentes mantêm a independência dos votos |
| Agentes | **Não** por questão; só na manutenção da taxonomia (propor temas novos a partir dos "fora", sugerir fusão de duplicados) | Qualquer | Classificar não precisa de ferramentas; agentes encarecem e dificultam auditar |
| Revisão humana | Fila priorizada; cada decisão vira rótulo | — | Fonte da verdade e do aprendizado |

**Escolha do provedor de cada papel em produção:** o mesmo mecanismo do case (ADR-017),
com o catálogo de produção restrito a APIs com lote e a modelos servidos em GPU própria.

- A escolha é fixada em `config/escolha_modelos.json` (modo manual) e versionada.
- Só muda depois de passar no gold de regressão.
- O recomendador também serve para **dimensionar o servidor de GPU**: memória por modelo e contexto (ADR-017).

**Qualidade contínua**

1. **Auditoria semanal por amostragem:** ~100–200 publicadas, aleatórias e estratificadas por disciplina, revisadas por professores. Mede a precisão com intervalo. Alarme se o limite inferior cair abaixo de 95%; nesse caso o limiar sobe automaticamente.
2. **Reportes de alunos como sinal:**
   - reporte numa questão publicada pela máquina → a questão volta para a fila com prioridade alta;
   - taxa de reporte por tema, por versão do pipeline e **por provedor e modelo de cada papel** → painel; um pico indica lixeira, definição ruim ou piora de um modelo.
3. **Gold de regressão:** um conjunto congelado de rótulos validados (~500). Nenhuma troca de prompt, **provedor, modelo**, cartão ou taxonomia entra em produção sem rodar nele, com o mesmo protocolo da ADR-014.
4. **Deriva:** distribuição de temas, taxas de publicar, revisar e fora, e recusas, por lote de importação e por provedor.
5. **Versionamento:** cada decisão grava provedor, modelo, hash do prompt, versão da taxonomia, versão dos cartões e versão da calibração (ADR-003, em banco).

**Fluxos**

- **Importação:** lote noturno pelas APIs de lote dos provedores (na Anthropic, 50% mais barato; latência de horas é aceitável), ou fila no servidor de GPU própria.
- **Revisão:** interface com a questão, o tema sugerido, o 2º colocado e os cartões (ADR-007). Aceitar com um clique. Toda decisão realimenta o classificador treinado e a calibração toda semana.
- **Mudança na taxonomia:** versão nova da árvore → reclassifica só as questões cujos candidatos tocam os nós alterados.
- **Troca de provedor ou modelo:** gold de regressão → se passar, nova versão da escolha → reclassifica só a fração que desce para o N2, e não a base inteira.

**Custo por questão** (estimativa com o perfil Anthropic em lote, metade dos preços da ADR-002; outros provedores entram pela mesma conta, com seus preços):

| Etapa | Fração das questões | Custo unitário | Custo médio |
|---|---|---|---|
| Normalização, embeddings, classificador treinado | 100% | ~US$ 0 (servidor próprio) | ~US$ 0 |
| Voto barato (Haiku 5.5 em lote) | 100% das novas | ~US$ 0,0015 | ~US$ 0,002 |
| Papéis A, B e verificador em lote | ~35–50% (a medir) | ~US$ 0,04–0,08 | ~US$ 0,015–0,04 |
| **Total de máquina** | | | **~US$ 0,02–0,04 por questão processada** |

O custo unitário do N2 vem do perfil medido no case, sem a sobrecarga das CLIs: ~70 mil tokens de entrada por questão (~85% em cache de prompt) e 5 a 12 mil de saída, quase tudo raciocínio do verificador. O preço é o de lista de um modelo intermediário, em lote.

- Com o cache por hash e versão, uma semana típica processa **só o que é novo, mudou ou foi reportado**. Exemplo: 5 mil questões → ~US$ 100–200 por semana.
- Reprocessar as 50 mil (troca de taxonomia ou de modelo) → ~US$ 1–2 mil por rodada.
- **Alternativa com GPU própria** para o voto barato (ou para mais papéis, se um modelo aberto passar no gold): troca custo por questão por custo fixo do servidor. Compensa quando o gasto mensal com API daquele papel passa do custo mensal do servidor. A conta é feita com os preços locais e com a memória estimada pelo recomendador.
- O custo dominante passa a ser o **tempo do professor**: com 20–30% das novas indo para revisão e ~30–60 s por item com boa sugestão, 5 mil novas por semana dão ~10–25 horas de professor. A prioridade por impacto garante que esse tempo vá primeiro para as questões mais vistas.

## Opções consideradas

### Opção A: LLM forte em toda questão, toda semana

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | ~US$ 0,08–0,15 × 50 mil = ~US$ 4–7,5 mil por semana (ensemble completo em toda questão) |
| Escala | Limitada por cota e custo |
| Efeito na qualidade | Boa, mas não melhora com o tempo |

**Prós:** simples; mesma arquitetura do case.
**Contras:** caro; desperdiça dinheiro em questões que não mudaram; não aprende com as revisões.

### Opção B: só classificador treinado

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média |
| Custo | ~US$ 0 |
| Escala | Ótima |
| Efeito na qualidade | Fraco em temas raros e novos; depende de rótulos que ainda não existem |

**Prós:** barato e rápido.
**Contras:** no começo não há rótulos; erra temas com poucos exemplos (vários nós têm menos de 10 questões).

### Opção C: cascata com cache por versão, papéis com provedores de produção e humano no ciclo (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média a alta |
| Custo | ~US$ 0,02–0,04 por questão processada; ~US$ 100–200 por semana típica |
| Escala | Boa (lote; o cache evita reprocessar) |
| Efeito na qualidade | Melhora toda semana com as revisões; monitorada continuamente, por provedor |

**Prós:** custo proporcional ao que muda; o LLM forte só onde compensa; ciclo de aprendizado; sem dependência de um fornecedor (cada papel pode trocar de provedor depois de passar no gold).
**Contras:** mais peças para operar; precisa de interface de revisão e de banco de decisões.

### Opção D: agente por questão (busca, leitura de lei, várias rodadas)

**Prós:** flexível.
**Contras:** custo e latência imprevisíveis; difícil de auditar e de calibrar; a árvore cabe no contexto, então não há o que buscar.

### Opção E: CLIs de assinatura em produção (como no case)

**Prós:** sem custo por token.
**Contras:** cotas de planos individuais, não pensadas para carga de produção de uma empresa; sem lote; latência variável (4–270 s por chamada no teste); sobrecarga de tokens do agente. Servem para o case e para experimentos, não para 50 mil questões.

## Análise de trade-offs

A opção C aproveita a vantagem que a produção tem e o case não tem: **rótulos que se
acumulam**. No começo, a cascata se comporta como o ensemble do case (N2 decide quase
tudo). Conforme as revisões viram rótulos, o N1 assume a maior parte e o custo cai.

O ponto de equilíbrio é empírico: a fração que desce para o N2 é medida pela auditoria
semanal e ajustada pelo limiar calibrado por disciplina. A opção A só faria sentido num
piloto curto, para criar os primeiros rótulos.

A independência de provedor herdada do case tem valor próprio em produção. Ela evita
depender de um único fornecedor (preço, disponibilidade, mudança de modelo) e mantém
famílias diferentes nos votos. O custo dessa flexibilidade é a disciplina de passar
toda troca pelo gold de regressão.

## Consequências

- Exige três peças que o case não tem: banco de decisões versionadas, interface de revisão e painel de qualidade (com recorte por provedor e modelo).
- A camada de provedores (`vicio_ia/llm/`) e o recomendador (`vicio_ia/infra/`) do case vão para produção sem mudança de contrato. Falta acrescentar o processamento em lote nos provedores de API (ADR-002, item 4).
- A taxonomia passa a ter dono e versão; as correções da ADR-005 (fantasmas, lixeiras, títulos) entram como a versão 2 da árvore.
- O professor deixa de "classificar questões" e passa a "validar sugestões e definições de tema". A meta é que ele gaste segundos por item, e não minutos.

## Itens de ação

1. [x] Seção (c) do relatório: diagrama, tabela de componentes (com o provedor de produção de cada papel), tabela de custos e indicadores de qualidade.
2. [ ] Usar os números reais do E6 (ADR-014) para calibrar a fração do N2 e escolher o modelo do voto barato em produção (API pequena × modelo aberto em GPU própria).
3. [x] No memo para o professor: o que muda no dia a dia dele (fila priorizada, validação de cartões).
4. [x] Lista "com mais tempo" no relatório. Ela prioriza o que muda a entrega do case: convenção, cartões, gold maior, E6 e variação entre execuções. Piloto, interface de revisão, gold de regressão e lote ficam no desenho de produção.
