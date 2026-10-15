"""Calibração da confiança (ADR-013): regressão logística L2 sobre poucas variáveis dos sinais.

A regressão é implementada com ``numpy`` (mínimos quadrados reponderados, IRLS), para manter
o código tipado de ponta a ponta. O alvo é o acerto pela régua **estrita** no gold.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import ClassVar

import numpy as np
import numpy.typing as npt

from vicio_ia.decisao.agregacao import DecisaoPreliminar

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


class VetorizadorDecisao:
    """Converte uma decisão preliminar nas variáveis da calibração (ADR-013, tabela 1)."""

    NOMES: ClassVar[tuple[str, ...]] = (
        "concordancia_ramo",
        "verificador_confirma",
        "verificador_mesmo_ramo",
        "recuou",
        "autoconfianca_media",
        "zona_risco",
        "origem_mesmo_ramo",
    )

    def vetor(self, decisao: DecisaoPreliminar) -> list[float]:
        """Variáveis de uma decisão.

        Args:
            decisao: Decisão preliminar.

        Returns:
            Valores na ordem de :attr:`NOMES` (concordância de 0 a 1; autoconfiança ausente = 0,5).
        """
        return [
            decisao.concordancia_ramo / 4.0,
            1.0 if decisao.veredito == "confirma" else 0.0,
            1.0 if decisao.veredito in ("pai", "filho") else 0.0,
            1.0 if decisao.recuou else 0.0,
            decisao.autoconfianca_media if decisao.autoconfianca_media is not None else 0.5,
            1.0 if decisao.zona_risco else 0.0,
            1.0 if decisao.origem_mesmo_ramo else 0.0,
        ]

    def matriz(self, decisoes: Sequence[DecisaoPreliminar]) -> Matriz:
        """Matriz de variáveis.

        Args:
            decisoes: Decisões.

        Returns:
            Matriz ``n × k``.
        """
        return np.array([self.vetor(d) for d in decisoes], dtype=np.float64).reshape(len(decisoes), len(self.NOMES))


@dataclass(frozen=True)
class ExemploCalibracao:
    """Questão rotulada usada no ajuste.

    Attributes:
        decisao: Decisão preliminar (com tema).
        acerto: O tema acerta pela régua estrita.
        peso: Peso amostral (inverso da probabilidade de inclusão).
    """

    decisao: DecisaoPreliminar
    acerto: bool
    peso: float


@dataclass(frozen=True)
class ValidacaoCalibracao:
    """Qualidade da calibração na validação cruzada.

    Attributes:
        exemplos: Exemplos usados.
        taxa_acerto: Fração de acertos.
        brier: Erro quadrático médio das probabilidades.
        brier_base: Brier de prever sempre a taxa de acerto (referência).
        log_loss: Perda logarítmica.
        faixas: ``(faixa, exemplos, P média prevista, acerto observado)`` da curva de confiabilidade.
    """

    exemplos: int
    taxa_acerto: float
    brier: float
    brier_base: float
    log_loss: float
    faixas: tuple[tuple[str, int, float, float], ...]


class SeletorPenalidade:
    """Escolhe a penalidade L2 pela menor log-loss na validação cruzada."""

    def __init__(self, vetorizador: VetorizadorDecisao) -> None:
        """Guarda o vetorizador.

        Args:
            vetorizador: Conversor de decisões em variáveis.
        """
        self._vetorizador: VetorizadorDecisao = vetorizador

    def escolher(
        self, exemplos: Sequence[ExemploCalibracao], penalidades: Sequence[float], partes: int, semente: int
    ) -> tuple[float, list[tuple[float, ValidacaoCalibracao]]]:
        """Valida cada penalidade da grade.

        Empates na log-loss (diferença menor que 0,001) ficam com a penalidade maior, mais conservadora.

        Args:
            exemplos: Gold rotulado.
            penalidades: Grade de penalidades.
            partes: Partes da validação cruzada.
            semente: Semente.

        Returns:
            ``(penalidade escolhida, [(penalidade, validação)])``.
        """
        resultados: list[tuple[float, ValidacaoCalibracao]] = [
            (penalidade, Calibrador(penalidade, self._vetorizador).validar(exemplos, partes, semente))
            for penalidade in penalidades
        ]
        melhor: float = min(r[1].log_loss for r in resultados)
        escolhida: float = max(p for p, v in resultados if v.log_loss <= melhor + 0.001)
        return escolhida, resultados


class Calibrador:
    """Ajusta e aplica a calibração; faz a validação cruzada estratificada."""

    def __init__(self, penalidade: float, vetorizador: VetorizadorDecisao) -> None:
        """Define o modelo.

        Args:
            penalidade: Penalidade L2.
            vetorizador: Conversor de decisões em variáveis.
        """
        self._penalidade: float = penalidade
        self._vetorizador: VetorizadorDecisao = vetorizador
        self._modelo: RegressaoLogisticaL2 = RegressaoLogisticaL2(penalidade)
        self._ajustado: bool = False

    @property
    def coeficientes(self) -> dict[str, float]:
        """Coeficientes por variável (com o intercepto)."""
        valores: Matriz = self._modelo.coeficientes
        nomes: tuple[str, ...] = ("intercepto", *self._vetorizador.NOMES)
        return {nome: round(float(valor), 3) for nome, valor in zip(nomes, valores, strict=False)}

    def ajustar(self, exemplos: Sequence[ExemploCalibracao]) -> Calibrador:
        """Ajusta nos exemplos rotulados.

        Args:
            exemplos: Exemplos.

        Returns:
            O próprio calibrador.
        """
        x: Matriz = self._vetorizador.matriz([e.decisao for e in exemplos])
        y: Matriz = np.array([1.0 if e.acerto else 0.0 for e in exemplos], dtype=np.float64)
        pesos: Matriz = np.array([e.peso for e in exemplos], dtype=np.float64)
        pesos = pesos * len(exemplos) / float(pesos.sum())
        self._modelo = RegressaoLogisticaL2(self._penalidade).ajustar(x, y, pesos)
        self._ajustado = True
        return self

    def prever(self, decisoes: Sequence[DecisaoPreliminar]) -> list[float]:
        """Probabilidade calibrada de acerto.

        Args:
            decisoes: Decisões com tema.

        Returns:
            Probabilidades na mesma ordem.
        """
        if not decisoes:
            return []
        return [float(p) for p in self._modelo.prever(self._vetorizador.matriz(decisoes))]

    def validar(self, exemplos: Sequence[ExemploCalibracao], partes: int, semente: int) -> ValidacaoCalibracao:
        """Validação cruzada estratificada (acertos e erros distribuídos entre as partes).

        Args:
            exemplos: Exemplos rotulados.
            partes: Número de partes.
            semente: Semente do embaralhamento.

        Returns:
            Métricas fora da amostra.
        """
        gerador: np.random.Generator = np.random.default_rng(semente)
        indices: dict[bool, list[int]] = {True: [], False: []}
        posicao: int
        exemplo: ExemploCalibracao
        for posicao, exemplo in enumerate(exemplos):
            indices[exemplo.acerto].append(posicao)
        parte_de: dict[int, int] = {}
        classe: bool
        for classe in (True, False):
            embaralhados: list[int] = [int(i) for i in gerador.permutation(indices[classe])]
            ordem: int
            item: int
            for ordem, item in enumerate(embaralhados):
                parte_de[item] = ordem % partes
        previstas: list[float] = [0.0] * len(exemplos)
        parte: int
        for parte in range(partes):
            treino: list[ExemploCalibracao] = [e for i, e in enumerate(exemplos) if parte_de[i] != parte]
            teste: list[int] = [i for i in range(len(exemplos)) if parte_de[i] == parte]
            if not teste or len({e.acerto for e in treino}) < 2:
                continue
            modelo: Calibrador = Calibrador(self._penalidade, self._vetorizador).ajustar(treino)
            probabilidades: list[float] = modelo.prever([exemplos[i].decisao for i in teste])
            indice: int
            probabilidade: float
            for indice, probabilidade in zip(teste, probabilidades, strict=True):
                previstas[indice] = probabilidade
        return self._metricas(exemplos, previstas)

    @staticmethod
    def _metricas(exemplos: Sequence[ExemploCalibracao], previstas: Sequence[float]) -> ValidacaoCalibracao:
        """Calcula Brier, log-loss e a curva de confiabilidade.

        Args:
            exemplos: Exemplos.
            previstas: Probabilidades fora da amostra.

        Returns:
            Métricas.
        """
        y: list[float] = [1.0 if e.acerto else 0.0 for e in exemplos]
        n: int = len(y)
        taxa: float = sum(y) / n if n else 0.0
        brier: float = sum((p - a) ** 2 for p, a in zip(previstas, y, strict=True)) / n if n else 0.0
        brier_base: float = sum((taxa - a) ** 2 for a in y) / n if n else 0.0
        eps: float = 1e-6
        perda: float = (
            -sum(
                a * math.log(min(max(p, eps), 1 - eps)) + (1 - a) * math.log(1 - min(max(p, eps), 1 - eps))
                for p, a in zip(previstas, y, strict=True)
            )
            / n
            if n
            else 0.0
        )
        faixas: list[tuple[str, int, float, float]] = []
        inferior: float
        superior: float
        for inferior, superior in ((0.0, 0.5), (0.5, 0.7), (0.7, 0.85), (0.85, 0.95), (0.95, 1.01)):
            dentro: list[int] = [i for i, p in enumerate(previstas) if inferior <= p < superior]
            if dentro:
                faixas.append(
                    (
                        f"{inferior:.2f}–{min(superior, 1.0):.2f}",
                        len(dentro),
                        round(sum(previstas[i] for i in dentro) / len(dentro), 3),
                        round(sum(y[i] for i in dentro) / len(dentro), 3),
                    )
                )
        return ValidacaoCalibracao(
            n, round(taxa, 3), round(brier, 4), round(brier_base, 4), round(perda, 4), tuple(faixas)
        )
