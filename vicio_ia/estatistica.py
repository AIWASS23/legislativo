"""Estatística compartilhada pelas duas etapas: regressão logística L2 implementada com ``numpy``.

Fica fora de ``vicio_ia.avaliacao`` para que a fase de decisão da etapa 2 (``vicio_ia.sistema``) possa usá-la
sem importar os módulos da etapa 1 que tratam votos de LLM (ADR-019).
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

type Matriz = npt.NDArray[np.float64]
"""Matriz (ou vetor) de reais."""


class RegressaoLogisticaL2:
    """Regressão logística com penalidade L2 (o intercepto não é penalizado), ajustada por IRLS."""

    def __init__(self, penalidade: float, max_iteracoes: int = 100, tolerancia: float = 1e-8) -> None:
        """Define a regularização e o critério de parada.

        Args:
            penalidade: Força da penalidade L2.
            max_iteracoes: Máximo de iterações de Newton.
            tolerancia: Mudança mínima nos coeficientes para continuar.
        """
        self._penalidade: float = penalidade
        self._max_iteracoes: int = max_iteracoes
        self._tolerancia: float = tolerancia
        self._coeficientes: Matriz = np.zeros(0, dtype=np.float64)

    @property
    def coeficientes(self) -> Matriz:
        """Intercepto seguido dos coeficientes das variáveis."""
        return self._coeficientes.copy()

    def ajustar(self, x: Matriz, y: Matriz, pesos: Matriz) -> RegressaoLogisticaL2:
        """Ajusta o modelo.

        Args:
            x: Variáveis (``n × k``).
            y: Alvo 0/1 (``n``).
            pesos: Peso de cada exemplo (``n``), ex.: inverso da probabilidade de inclusão.

        Returns:
            O próprio modelo.
        """
        projeto: Matriz = np.hstack([np.ones((x.shape[0], 1), dtype=np.float64), x])
        beta: Matriz = np.zeros(projeto.shape[1], dtype=np.float64)
        penal: Matriz = np.eye(projeto.shape[1], dtype=np.float64) * self._penalidade
        penal[0, 0] = 0.0
        _iteracao: int
        for _iteracao in range(self._max_iteracoes):
            p: Matriz = self._sigmoide(projeto @ beta)
            w: Matriz = pesos * p * (1.0 - p)
            gradiente: Matriz = projeto.T @ (pesos * (y - p)) - penal @ beta
            hessiana: Matriz = projeto.T @ (projeto * w[:, None]) + penal + np.eye(projeto.shape[1]) * 1e-9
            passo: Matriz = np.linalg.solve(hessiana, gradiente)
            beta = beta + passo
            if float(np.max(np.abs(passo))) < self._tolerancia:
                break
        self._coeficientes = beta
        return self

    def prever(self, x: Matriz) -> Matriz:
        """Probabilidade de acerto.

        Args:
            x: Variáveis (``n × k``).

        Returns:
            Probabilidades (``n``).
        """
        projeto: Matriz = np.hstack([np.ones((x.shape[0], 1), dtype=np.float64), x])
        return self._sigmoide(projeto @ self._coeficientes)

    @staticmethod
    def _sigmoide(z: Matriz) -> Matriz:
        """Função logística, estável para valores grandes.

        Args:
            z: Valores.

        Returns:
            ``1 / (1 + e^-z)``.
        """
        resultado: Matriz = 1.0 / (1.0 + np.exp(-np.clip(z, -30.0, 30.0)))
        return resultado
