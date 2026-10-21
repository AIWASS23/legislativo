"""Rankings de temas e as métricas de recuperação na folha-verdade (E7, E8, E9; ADR-024).

Qualquer fonte de pontuação (BM25, embeddings, kNN, fusão) vira um :class:`RankingQuestao`, e todas são
medidas pelas mesmas métricas: acerto no top-1 nas 100 e nas 92 com tema, recall@k nas 92 e acerto no
top-1 por nível do tema central.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

from vicio_ia.estatistica import Matriz
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.sistema.folha import ReguaEtapa2, RotuloFolha


@dataclass(frozen=True)
class Metrica:
    """Um número de um experimento.

    Attributes:
        experimento: ``E7``, ``E11``...
        variante: Variante medida.
        nome: Nome da métrica.
        valor: Valor.
        detalhe: Texto livre (intervalo, contagem).
    """

    experimento: str
    variante: str
    nome: str
    valor: float
    detalhe: str = ""


@dataclass(frozen=True)
class RankingQuestao:
    """Ranking de temas para uma questão da folha.

    Attributes:
        id: ID da questão.
        ordem: Temas do melhor para o pior.
        pontos: Pontuações na mesma ordem.
        primeiro_acerto: Posição (1 em diante) do primeiro tema certo pela régua; 0 se nenhum.
    """

    id: str
    ordem: tuple[str, ...]
    pontos: tuple[float, ...]
    primeiro_acerto: int


class AvaliadorRanking:
    """Ordena pontuações de temas e calcula as métricas de recuperação."""

    def __init__(self, temas: Sequence[TemaPreparado], top_k: Sequence[int]) -> None:
        """Guarda a árvore e os tamanhos de lista do recall.

        Args:
            temas: Árvore preparada.
            top_k: Tamanhos de lista (o primeiro, 1, é o top-1; os demais viram recall@k).
        """
        self._regua: ReguaEtapa2 = ReguaEtapa2(temas)
        self._nivel: dict[str, int] = {t.tema_id: t.nivel for t in temas}
        self._top_k: tuple[int, ...] = tuple(top_k)

    def ordenar(self, rotulo: RotuloFolha, pontos: Matriz, ids_temas: Sequence[str]) -> RankingQuestao:
        """Ordena os temas pela pontuação (empate pela ordem da árvore) e acha o primeiro acerto.

        Args:
            rotulo: Rótulo da equipe.
            pontos: Pontuação de cada tema, na ordem de ``ids_temas``.
            ids_temas: Temas pontuados.

        Returns:
            Ranking.
        """
        ordem: list[int] = [int(i) for i in np.argsort(-pontos, kind="stable")]
        temas_ordem: tuple[str, ...] = tuple(ids_temas[i] for i in ordem)
        primeiro: int = next((k + 1 for k, t in enumerate(temas_ordem) if self._regua.acerta(t, rotulo)), 0)
        return RankingQuestao(rotulo.id, temas_ordem, tuple(float(pontos[i]) for i in ordem), primeiro)

    def metricas(
        self, experimento: str, variante: str, folha: Sequence[RotuloFolha], rankings: Sequence[RankingQuestao]
    ) -> list[Metrica]:
        """Acerto no top-1, recall@k e acerto no top-1 por nível do tema central.

        Args:
            experimento: ``E7``, ``E8``...
            variante: Nome da variante.
            folha: Rótulos.
            rankings: Rankings, na ordem da folha.

        Returns:
            Métricas.
        """
        com_tema: list[tuple[RotuloFolha, RankingQuestao]] = [
            (r, k) for r, k in zip(folha, rankings, strict=True) if not r.fora
        ]
        acertos_top1: int = sum(1 for k in rankings if k.primeiro_acerto == 1)
        metricas: list[Metrica] = [
            Metrica(
                experimento, variante, "acerto top-1 (100)", acertos_top1 / len(folha), f"{acertos_top1}/{len(folha)}"
            ),
            Metrica(
                experimento,
                variante,
                "acerto top-1 (92 com tema)",
                acertos_top1 / len(com_tema),
                f"{acertos_top1}/{len(com_tema)}",
            ),
        ]
        k: int
        for k in self._top_k[1:]:
            dentro: int = sum(1 for _, rk in com_tema if 0 < rk.primeiro_acerto <= k)
            metricas.append(
                Metrica(experimento, variante, f"recall@{k} (92)", dentro / len(com_tema), f"{dentro}/{len(com_tema)}")
            )
        nivel_rotulo: int
        for nivel_rotulo in (1, 2):
            grupo: list[RankingQuestao] = [
                rk for r, rk in com_tema if self._nivel.get(r.tema_central_id) == nivel_rotulo
            ]
            if grupo:
                certos: int = sum(1 for rk in grupo if rk.primeiro_acerto == 1)
                metricas.append(
                    Metrica(
                        experimento,
                        variante,
                        f"acerto top-1, tema central de nível {nivel_rotulo}",
                        certos / len(grupo),
                        f"{certos}/{len(grupo)}",
                    )
                )
        return metricas


class RegraEscolha:
    """Regra pré-registrada de escolha entre variantes (E8, E7b, E8b).

    Vence o maior recall@10 nas 92 com tema; até uma questão de diferença é empate, decidido pelo acerto no
    top-1; persistindo o empate, vence a primeira variante da lista (a mais simples).
    """

    @staticmethod
    def escolher(metricas: Sequence[Metrica], experimento: str, variantes: Sequence[str]) -> str:
        """Aplica a regra.

        Args:
            metricas: Métricas medidas.
            experimento: Experimento das métricas (``E8``, ``E7b``...).
            variantes: Variantes candidatas, da mais simples para a mais complexa.

        Returns:
            Variante vencedora.
        """

        def valor(variante: str, nome: str) -> float:
            """Valor de uma métrica.

            Args:
                variante: Variante.
                nome: Nome da métrica.

            Returns:
                Valor.
            """
            return next(
                m.valor for m in metricas if m.experimento == experimento and m.variante == variante and m.nome == nome
            )

        melhor: float = max(valor(v, "recall@10 (92)") for v in variantes)
        empatadas: list[str] = [v for v in variantes if valor(v, "recall@10 (92)") >= melhor - 1.5 / 92]
        lista: list[str] = list(variantes)
        return max(empatadas, key=lambda v: (valor(v, "acerto top-1 (92 com tema)"), -lista.index(v)))
