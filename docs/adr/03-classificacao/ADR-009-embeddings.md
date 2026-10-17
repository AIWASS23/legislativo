# ADR-009: Embeddings como sinal opcional no case

**Status:** Proposto
**Data:** 14/10/2026
**Decisores:** Autor do case
**Fase:** 03-classificacao (passo 04)
**Relacionadas:** ADR-001, ADR-007, ADR-008, ADR-014, ADR-016

## Contexto

- **Papel no case:** uma similaridade entre a questão e os cartões de tema daria um sinal independente dos LLMs para o ensemble (ADR-008).
- **Pouco ganho esperado aqui:**
  - a árvore inteira cabe no prompt, então embeddings não são necessários para recuperar candidatos;
  - com 359 questões e sem rótulos, não há kNN sobre questões já classificadas, que é onde embeddings mais rendem.
- **Custo de instalação alto:** modelos locais multilíngues (e5, BGE-M3 via `sentence-transformers`) trazem o PyTorch, com alguns GB no Linux. Embeddings por API exigem outra conta (por exemplo, Voyage).
- **Na produção é diferente (ADR-016):** deduplicação, kNN sobre rótulos validados e classificador treinado dependem de embeddings.

## Decisão

1. **O pipeline do case funciona sem embeddings.** O passo 04 é **opcional** e fica fora do caminho crítico.
2. Se sobrar tempo na sexta-feira, rodar o **E1** (ADR-014):
   - modelo local pequeno e multilíngue (`intfloat/multilingual-e5-small`), com a instalação do PyTorch **só para CPU** (índice de pacotes de CPU), em `requirements-embeddings.txt` separado, para não pesar o ambiente principal;
   - métricas: acerto em top-1 e top-5 no gold e ganho de calibração quando entra como variável.
3. O embedding entra no ensemble **só se o E1 mostrar ganho**. Caso contrário, o resultado vai para o relatório como beco sem saída medido, e para a seção de produção como componente central.

## Opções consideradas

### Opção A: sem embeddings no case (base da decisão)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Nenhuma |
| Custo | Nenhum |
| Efeito na régua | Pequeno: perde-se um sinal independente |
| Prazo | Ganha tempo para o que mais pesa (gold, calibração) |

**Prós:** foco; ambiente leve.
**Contras:** o ensemble fica só com LLMs e regras.

### Opção B: modelo local pequeno em CPU, opcional (escolhida como extensão)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Média (instalação do PyTorch para CPU) |
| Custo | Zero em API; ~1 GB em disco |
| Efeito na régua | A medir (E1) |
| Prazo | Só se houver folga |

**Prós:** sinal de outra natureza que os LLMs; também é a peça que a produção usa.
**Contras:** dependência pesada; ganho incerto nesse volume.

### Opção C: embeddings por API (Voyage ou outro)

**Prós:** sem PyTorch; modelos fortes.
**Contras:** outra conta e outra chave; dados saem para mais um provedor.

### Opção D: modelo grande local (BGE-M3, e5-large)

**Prós:** melhor qualidade.
**Contras:** mais lento em CPU e mais pesado; não compensa para um sinal opcional.

## Análise de trade-offs

No case, o gargalo da nota é a confiança bem calibrada e a previsão honesta, não um sinal
a mais de recuperação. Gastar a manhã de sexta com o PyTorch tiraria tempo do gold set
(ADR-012), que é o caminho crítico. Por isso o embedding fica como extensão medida.

A decisão muda se o E2 mostrar muitos erros de "tema completamente fora" (não só irmão
errado). Nesse caso, um sinal de similaridade passa a valer mais.

## Consequências

- `requirements.txt` continua leve; quem avaliar o case não precisa instalar o PyTorch.
- A seção de produção do relatório precisa explicar por que os embeddings são centrais lá e opcionais aqui.

## Itens de ação

1. [ ] (Opcional) `requirements-embeddings.txt` com `sentence-transformers` e PyTorch para CPU.
2. [ ] (Opcional) `vicio_ia/sinais/embeddings.py`: classe `SinalEmbeddings` (cartões indexados uma vez, top-k por questão, cache em disco).
3. [ ] (Opcional) Rodar o E1 e registrar o resultado (ADR-014).
