# ADR-010: Granularidade da publicação e recuo para o tema pai

**Status:** Aceito (implementado em 15/10/2026 em `vicio_ia/decisao/agregacao.py`; nunca recua para o nível 0)
**Data:** 14/10/2026
**Decisores:** Autor do case
**Fase:** 04-decisao (passo 07)
**Relacionadas:** ADR-005, ADR-008, ADR-011, ADR-013

## Contexto

A régua considera certo publicar no tema do especialista **ou num nó do mesmo ramo (pai
ou filho dele)**. Publicar em outro subtema do mesmo tema é erro.

Seja `T` um tema de nível 1 com filhos `X1..Xn`, e `y` o rótulo do especialista:

| Publicar em | Certo quando |
|---|---|
| Subtema `Xi` | `y = Xi` ou `y = T` |
| Tema `T` | `y = T`, `y` é qualquer filho `Xj`, ou `y` é a disciplina (se nível 0 contar) |

**Para a métrica, publicar em `T` nunca é pior que publicar num filho.** O ganho é a
chance de o especialista ter escolhido um irmão. A EDA mostra que isso é comum: irmãos
com títulos parecidos, lixeiras e subtemas com 0 questões na origem.

- **Onde o recuo é possível:** 51 temas de nível 1 têm filhos. Os 38 sem filhos (incluindo os 26 de Legislação Especial) não permitem recuo.
- **Custo para o aluno:**
  - quem estuda `T` vê a questão, mas quem estuda só `Xi` não vê;
  - publicar tudo no nível 1 recriaria "tópicos genéricos que atraem centenas de questões", justamente o problema que o case descreve.

## Decisão

**Recuo adaptativo:**

1. **Publicar no subtema** quando as fontes concordam no mesmo subtema e o verificador confirma esse subtema contra os irmãos (ADR-008).
2. **Recuar para o pai `T`** quando:
   - as fontes concordam no ramo de `T` mas divergem entre os filhos; ou
   - o verificador responde "pai"; ou
   - o subtema escolhido é uma lixeira sem concordância total (ADR-005).
3. **Nunca recuar para a disciplina (nível 0)**, mesmo que a Carla diga que conta. Seria criar a lixeira máxima.
4. **Divergência entre `T` e um filho `Xi`** já está no mesmo ramo: publicar `Xi` se o verificador confirmar; senão, `T`.
5. **Divergência entre ramos diferentes** não tem recuo: vai para `revisar` (ADR-011).
6. **Transparência:**
   - o relatório informa quantas publicadas ficaram no nível 1 por recuo;
   - os `extras_ids` guardam os subtemas candidatos;
   - a decisão de privilegiar o subtema sempre que houver confirmação fica registrada em `decisoes_manuais.md`.

## Opções consideradas

### Opção A: sempre o nó mais específico

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | Nenhum |
| Efeito na régua | Negativo: cada dúvida entre irmãos vira erro ou revisão |
| Prazo | Imediato |

**Prós:** máxima utilidade para o aluno quando acerta.
**Contras:** perde cobertura exatamente onde a régua permite segurança.

### Opção B: sempre publicar no nível 1

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa |
| Custo | Nenhum |
| Efeito na régua | Máxima precisão possível para a escolha de tema |
| Prazo | Imediato |

**Prós:** maximiza a métrica.
**Contras:** "joga para a métrica"; tira o subtema do aluno; recria lixeiras de nível 1. Seria difícil defender no relatório.

### Opção C: recuo adaptativo (escolhida)

| Dimensão | Avaliação |
|---|---|
| Complexidade | Baixa a média |
| Custo | Nenhum |
| Efeito na régua | Positivo: converte dúvida entre irmãos em publicação segura |
| Prazo | Compatível |

**Prós:** específico quando há evidência; seguro quando não há; defensável para o professor.
**Contras:** parte das publicadas fica no nível 1, com menos utilidade para quem estuda o subtema.

## Análise de trade-offs

A opção C usa a regra da régua como a própria régua justifica ("o aluno que estuda um tema
também vê as questões dos subtemas"), sem transformar isso em atalho geral.

Se a fração recuada ficar alta (acima de ~30% das publicadas), isso vira um achado para o
memo: os subtemas daquele tema são indistinguíveis e a árvore precisa ser revista ali.

## Consequências

- A agregação precisa saber, para cada candidato, quem é o pai e se `aceita_recuo` (ADR-005).
- A calibração (ADR-013) recebe "nível publicado" como variável: recuos devem ter precisão maior.
- O memo ganha a lista dos temas com mais recuos, um indicador de subtemas mal definidos.

## Implementação (15/10/2026)

`AgregadorSinais` (`vicio_ia/decisao/agregacao.py`):
- o candidato preliminar é o mais específico entre A e B, quando os dois estão no mesmo ramo;
- verificador "pai" ou "irmão": recua para o pai, se ele é publicável; senão, `revisar`;
- verificador "filho": mantém o candidato e guarda o filho em `extras_ids`;
- lixeira forte sem concordância total: recua para o pai, se houver; senão, `revisar`;
- o relatório do passo 07 informa quantas publicadas ficaram no nível 1 e quantas por recuo;
- as escolhas estão em `decisoes_manuais.md` (D9).

## Itens de ação

1. [x] Recuo implementado em `AgregadorSinais` (`vicio_ia/decisao/agregacao.py`), em vez de uma classe `PoliticaRecuo` à parte (15/10).
2. [x] Testes unitários das cinco situações (subtema confirmado, divergência entre irmãos, verificador "pai", divergência entre T e Xi, ramos diferentes), mais filho, nunca recuar à disciplina e lixeiras fortes: `testes/teste_recuo.py` (10 testes, 17/10).
3. [ ] Relatório de recuos por tema em `saidas/decisao/recuos.csv` (hoje o `relatorio_decisao.md` só traz o total de recuos).
4. [x] Registrar a decisão de granularidade em `decisoes_manuais.md` (D9, 15/10).
