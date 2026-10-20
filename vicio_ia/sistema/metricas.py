"""Métricas de separação usadas nos experimentos da etapa 2 (E11, ADR-023)."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import numpy.typing as npt

type Vetor = npt.NDArray[np.float64]


class MetricasBinarias:
    """AUC (Mann-Whitney, com empates) e o seu intervalo por bootstrap estratificado."""

    @staticmethod
    def auc(pontuacoes: Sequence[float], positivos: Sequence[bool]) -> float:
        """Área sob a curva ROC: a chance de um positivo ter pontuação maior que um negativo.

        Args:
            pontuacoes: Pontuação de cada exemplo (maior = mais provável positivo).
            positivos: Rótulo de cada exemplo.

        Returns:
            AUC em [0, 1]; 0,5 quando uma das classes está vazia.
        """
        pos: Vetor = np.array([p for p, y in zip(pontuacoes, positivos, strict=True) if y], dtype=np.float64)
        neg: Vetor = np.array([p for p, y in zip(pontuacoes, positivos, strict=True) if not y], dtype=np.float64)
        if pos.size == 0 or neg.size == 0:
            return 0.5
        maiores: float = float((pos[:, None] > neg[None, :]).sum())
        empates: float = float((pos[:, None] == neg[None, :]).sum())
        return (maiores + 0.5 * empates) / float(pos.size * neg.size)

    @classmethod
    def intervalo_auc(
        cls, pontuacoes: Sequence[float], positivos: Sequence[bool], reamostras: int, semente: int
    ) -> tuple[float, float]:
        """Intervalo de 90% da AUC por bootstrap estratificado (reamostra positivos e negativos separadamente).

        Args:
            pontuacoes: Pontuação de cada exemplo.
            positivos: Rótulo de cada exemplo.
            reamostras: Número de reamostras.
            semente: Semente.

        Returns:
            Percentis 5 e 95.
        """
        gerador: np.random.Generator = np.random.default_rng(semente)
        idx_pos: list[int] = [i for i, y in enumerate(positivos) if y]
        idx_neg: list[int] = [i for i, y in enumerate(positivos) if not y]
        if not idx_pos or not idx_neg:
            return 0.5, 0.5
        valores: list[float] = []
        _: int
        for _ in range(reamostras):
            amostra: list[int] = [
                *(int(i) for i in gerador.choice(idx_pos, len(idx_pos))),
                *(int(i) for i in gerador.choice(idx_neg, len(idx_neg))),
            ]
            valores.append(cls.auc([pontuacoes[i] for i in amostra], [positivos[i] for i in amostra]))
        return float(np.percentile(valores, 5)), float(np.percentile(valores, 95))
