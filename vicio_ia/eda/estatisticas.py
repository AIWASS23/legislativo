"""Estatísticas descritivas simples, sem dependências externas."""

from __future__ import annotations

import statistics
from collections.abc import Sequence
from dataclasses import dataclass
from typing import ClassVar

from vicio_ia.relatorio import Celula


@dataclass(frozen=True)
class ResumoNumerico:
    """Resumo de uma distribuição numérica.

    Attributes:
        n: Quantidade de valores.
        minimo: Menor valor.
        p25: Percentil 25.
        mediana: Percentil 50.
        p75: Percentil 75.
        p95: Percentil 95.
        maximo: Maior valor.
        media: Média aritmética.
    """

    n: int
    minimo: float
    p25: float
    mediana: float
    p75: float
    p95: float
    maximo: float
    media: float

    def como_linha(self, nome: str) -> list[Celula]:
        """Converte o resumo numa linha de tabela.

        Args:
            nome: Nome da medida (primeira coluna).

        Returns:
            ``[nome, n, mínimo, p25, mediana, p75, p95, máximo, média]``.
        """
        return [
            nome,
            self.n,
            self.minimo,
            self.p25,
            self.mediana,
            self.p75,
            self.p95,
            self.maximo,
            round(self.media, 1),
        ]


class CalculadoraEstatisticas:
    """Calcula resumos numéricos e percentuais."""

    COLUNAS_RESUMO: ClassVar[tuple[str, ...]] = ("medida", "n", "mín", "p25", "mediana", "p75", "p95", "máx", "média")

    def resumir(self, valores: Sequence[float]) -> ResumoNumerico:
        """Resume uma lista de números.

        Args:
            valores: Valores a resumir (pode ser vazia).

        Returns:
            Resumo; com zeros se a lista estiver vazia.
        """
        if not valores:
            return ResumoNumerico(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        ordenados: list[float] = sorted(float(valor) for valor in valores)
        if len(ordenados) == 1:
            unico: float = ordenados[0]
            return ResumoNumerico(1, unico, unico, unico, unico, unico, unico, unico)
        cortes: list[float] = statistics.quantiles(ordenados, n=100, method="inclusive")
        return ResumoNumerico(
            n=len(ordenados),
            minimo=ordenados[0],
            p25=cortes[24],
            mediana=statistics.median(ordenados),
            p75=cortes[74],
            p95=cortes[94],
            maximo=ordenados[-1],
            media=statistics.fmean(ordenados),
        )

    @staticmethod
    def percentual(parte: int, total: int) -> float:
        """Calcula ``parte / total`` em porcentagem, com uma casa decimal.

        Args:
            parte: Numerador.
            total: Denominador.

        Returns:
            Porcentagem (0 se o total for zero).
        """
        return round(100.0 * parte / total, 1) if total else 0.0
