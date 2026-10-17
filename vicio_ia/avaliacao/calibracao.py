"""Calibração da confiança (ADR-013): dois calibradores intercambiáveis.

* **Logístico:** regressão logística L2 sobre poucas variáveis dos sinais, implementada com ``numpy``
  (mínimos quadrados reponderados, IRLS), para manter o código tipado de ponta a ponta.
* **Faixas:** a alternativa da ADR-013 para quando a regressão fica instável. Taxa de acerto observada
  em cada faixa de sinais (consenso total, confirmação parcial...), com suavização de Jeffreys, e
  incerteza por sorteios da distribuição Beta de cada faixa.

O alvo é o acerto pela régua **estrita** no gold. O pipeline usa o de menor log-loss na validação cruzada.
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
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


class CalibradorBase(ABC):
    """Contrato comum: ajustar no gold, prever ``P(acerto)`` e gerar reamostras para o bootstrap."""

    @property
    @abstractmethod
    def nome(self) -> str:
        """Nome do método (para o relatório)."""

    @abstractmethod
    def novo(self) -> CalibradorBase:
        """Cria um calibrador não ajustado com os mesmos hiperparâmetros.

        Returns:
            Calibrador novo.
        """

    @abstractmethod
    def ajustar(self, exemplos: Sequence[ExemploCalibracao]) -> CalibradorBase:
        """Ajusta nos exemplos rotulados.

        Args:
            exemplos: Gold rotulado.

        Returns:
            O próprio calibrador.
        """

    @abstractmethod
    def prever(self, decisoes: Sequence[DecisaoPreliminar]) -> list[float]:
        """Probabilidade calibrada de acerto.

        Args:
            decisoes: Decisões com tema.

        Returns:
            Probabilidades na mesma ordem.
        """

    def amostrar(
        self,
        decisoes: Sequence[DecisaoPreliminar],
        exemplos: Sequence[ExemploCalibracao],
        reamostras: int,
        gerador: np.random.Generator,
    ) -> Matriz:
        """Bootstrap não paramétrico: reamostra o gold, reajusta e prevê as decisões.

        Args:
            decisoes: Decisões a prever.
            exemplos: Gold rotulado.
            reamostras: Número de reamostras.
            gerador: Gerador aleatório.

        Returns:
            Matriz ``reamostras válidas × decisões``.
        """
        linhas: list[list[float]] = []
        _reamostra: int
        for _reamostra in range(reamostras):
            sorteio: list[int] = [int(i) for i in gerador.integers(0, len(exemplos), len(exemplos))]
            amostra: list[ExemploCalibracao] = [exemplos[i] for i in sorteio]
            if len({e.acerto for e in amostra}) < 2:
                continue
            linhas.append(self.novo().ajustar(amostra).prever(decisoes))
        return np.array(linhas, dtype=np.float64).reshape(len(linhas), len(decisoes))

    def validar(self, exemplos: Sequence[ExemploCalibracao], partes: int, semente: int) -> ValidacaoCalibracao:
        """Validação cruzada estratificada (acertos e erros distribuídos entre as partes).

        Args:
            exemplos: Exemplos rotulados.
            partes: Número de partes.
            semente: Semente do embaralhamento.

        Returns:
            Métricas fora da amostra.
        """
        return self._metricas(exemplos, self.fora_da_amostra(exemplos, partes, semente))

    def fora_da_amostra(self, exemplos: Sequence[ExemploCalibracao], partes: int, semente: int) -> list[float]:
        """Probabilidade de cada exemplo prevista por um calibrador ajustado sem ele (validação cruzada).

        Args:
            exemplos: Exemplos rotulados.
            partes: Número de partes.
            semente: Semente do embaralhamento.

        Returns:
            Probabilidades na ordem dos exemplos.
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
            probabilidades: list[float] = self.novo().ajustar(treino).prever([exemplos[i].decisao for i in teste])
            indice: int
            probabilidade: float
            for indice, probabilidade in zip(teste, probabilidades, strict=True):
                previstas[indice] = probabilidade
        return previstas

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


class CalibradorLogistico(CalibradorBase):
    """Regressão logística L2 sobre as variáveis do :class:`VetorizadorDecisao`."""

    def __init__(self, penalidade: float, vetorizador: VetorizadorDecisao) -> None:
        """Define o modelo.

        Args:
            penalidade: Penalidade L2.
            vetorizador: Conversor de decisões em variáveis.
        """
        self._penalidade: float = penalidade
        self._vetorizador: VetorizadorDecisao = vetorizador
        self._modelo: RegressaoLogisticaL2 = RegressaoLogisticaL2(penalidade)

    @property
    def nome(self) -> str:
        """Nome do método."""
        return f"regressão logística L2 (penalidade {self._penalidade:g})"

    @property
    def coeficientes(self) -> dict[str, float]:
        """Coeficientes por variável (com o intercepto)."""
        valores: Matriz = self._modelo.coeficientes
        nomes: tuple[str, ...] = ("intercepto", *self._vetorizador.NOMES)
        return {nome: round(float(valor), 3) for nome, valor in zip(nomes, valores, strict=False)}

    def novo(self) -> CalibradorLogistico:
        """Cria um calibrador não ajustado com a mesma penalidade.

        Returns:
            Calibrador novo.
        """
        return CalibradorLogistico(self._penalidade, self._vetorizador)

    def ajustar(self, exemplos: Sequence[ExemploCalibracao]) -> CalibradorLogistico:
        """Ajusta nos exemplos rotulados, com o peso amostral.

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


class CalibradorFaixas(CalibradorBase):
    """Taxa de acerto observada por faixa de sinais, com suavização de Jeffreys.

    Faixas, da mais à menos confiável:

    * ``consenso_total``: o verificador confirma e A, B e o voto barato estão no ramo do tema;
    * ``confirma_parcial``: o verificador confirma, mas alguma fonte de LLM discorda;
    * ``verificador_vizinho``: o verificador escolheu o pai, um filho ou um irmão (houve recuo ou ajuste);
    * ``outros``: o resto (revisões forçadas, falhas).

    A taxa de cada faixa usa o peso amostral (inverso da probabilidade de inclusão), para continuar
    correta se a amostra do gold tiver estratos com probabilidades diferentes. A incerteza usa o
    tamanho efetivo de Kish, ``(Σw)² / Σw²``: com pesos iguais, é o próprio número de questões.
    """

    FAIXAS: ClassVar[tuple[str, ...]] = ("consenso_total", "confirma_parcial", "verificador_vizinho", "outros")
    FONTES_LLM: ClassVar[frozenset[str]] = frozenset({"classificador_a", "classificador_b", "voto_barato"})

    def __init__(self, prior: float = 0.5) -> None:
        """Define a suavização.

        Args:
            prior: Pseudo-contagem de acertos e de erros (0,5 = Jeffreys).
        """
        self._prior: float = prior
        self._brutas: dict[str, tuple[int, int]] = {}
        self._efetivas: dict[str, tuple[float, float]] = {}

    @property
    def nome(self) -> str:
        """Nome do método."""
        return "faixas de sinais com suavização de Jeffreys"

    @property
    def tabela(self) -> list[tuple[str, int, int, float]]:
        """``(faixa, exemplos, acertos, P)`` de cada faixa, na ordem de :attr:`FAIXAS`."""
        return [(faixa, *self._brutas.get(faixa, (0, 0)), round(self._taxa(faixa), 4)) for faixa in self.FAIXAS]

    @classmethod
    def faixa(cls, decisao: DecisaoPreliminar) -> str:
        """Faixa de uma decisão.

        Args:
            decisao: Decisão preliminar.

        Returns:
            Nome da faixa.
        """
        if decisao.veredito == "confirma":
            return "consenso_total" if cls.FONTES_LLM <= set(decisao.fontes_no_ramo) else "confirma_parcial"
        if decisao.veredito in ("pai", "filho", "irmao"):
            return "verificador_vizinho"
        return "outros"

    def novo(self) -> CalibradorFaixas:
        """Cria um calibrador não ajustado com a mesma suavização.

        Returns:
            Calibrador novo.
        """
        return CalibradorFaixas(self._prior)

    def ajustar(self, exemplos: Sequence[ExemploCalibracao]) -> CalibradorFaixas:
        """Conta exemplos e acertos por faixa, brutos e efetivos (com o peso amostral).

        Args:
            exemplos: Gold rotulado.

        Returns:
            O próprio calibrador.
        """
        por_faixa: dict[str, list[ExemploCalibracao]] = {faixa: [] for faixa in self.FAIXAS}
        exemplo: ExemploCalibracao
        for exemplo in exemplos:
            por_faixa[self.faixa(exemplo.decisao)].append(exemplo)
        self._brutas = {f: (len(itens), sum(1 for e in itens if e.acerto)) for f, itens in por_faixa.items()}
        self._efetivas = {f: self._efetiva(itens) for f, itens in por_faixa.items()}
        return self

    @staticmethod
    def _efetiva(exemplos: Sequence[ExemploCalibracao]) -> tuple[float, float]:
        """Tamanho efetivo de Kish e acertos efetivos de um grupo de exemplos.

        Args:
            exemplos: Exemplos de uma faixa.

        Returns:
            ``(n efetivo, acertos efetivos)``; ``(0, 0)`` se vazio.
        """
        if not exemplos:
            return 0.0, 0.0
        pesos: list[float] = [e.peso for e in exemplos]
        soma: float = sum(pesos)
        n_efetivo: float = soma * soma / sum(w * w for w in pesos)
        taxa: float = sum(e.peso for e in exemplos if e.acerto) / soma
        return n_efetivo, taxa * n_efetivo

    def prever(self, decisoes: Sequence[DecisaoPreliminar]) -> list[float]:
        """Taxa suavizada da faixa de cada decisão.

        Args:
            decisoes: Decisões com tema.

        Returns:
            Probabilidades na mesma ordem.
        """
        return [self._taxa(self.faixa(decisao)) for decisao in decisoes]

    def amostrar(
        self,
        decisoes: Sequence[DecisaoPreliminar],
        exemplos: Sequence[ExemploCalibracao],
        reamostras: int,
        gerador: np.random.Generator,
    ) -> Matriz:
        """Sorteia a taxa de cada faixa da distribuição Beta ajustada no gold.

        O bootstrap comum não serve aqui: numa faixa com 28 acertos em 28, toda reamostra dá 100%
        e a incerteza some. A Beta(acertos + 0,5, erros + 0,5) mantém a incerteza do tamanho da faixa.

        Args:
            decisoes: Decisões a prever.
            exemplos: Gold rotulado.
            reamostras: Número de sorteios.
            gerador: Gerador aleatório.

        Returns:
            Matriz ``sorteios × decisões``.
        """
        ajustado: CalibradorFaixas = self.novo().ajustar(exemplos)
        total: tuple[float, float] = self._efetiva(exemplos)
        sorteios: dict[str, Matriz] = {}
        faixa: str
        for faixa in self.FAIXAS:
            n: float
            acertos: float
            n, acertos = ajustado._efetivas.get(faixa, (0.0, 0.0))
            if n == 0:
                n, acertos = total
            sorteios[faixa] = gerador.beta(acertos + self._prior, n - acertos + self._prior, reamostras)
        colunas: list[Matriz] = [sorteios[self.faixa(decisao)] for decisao in decisoes]
        if not colunas:
            return np.zeros((reamostras, 0), dtype=np.float64)
        resultado: Matriz = np.stack(colunas, axis=1)
        return resultado

    def _taxa(self, faixa: str) -> float:
        """Taxa suavizada de uma faixa (a do gold inteiro, se a faixa não tiver exemplos).

        Args:
            faixa: Nome da faixa.

        Returns:
            ``(acertos + prior) / (n + 2 · prior)``.
        """
        n: float
        acertos: float
        n, acertos = self._efetivas.get(faixa, (0.0, 0.0))
        if n == 0:
            n = sum(c[0] for c in self._efetivas.values())
            acertos = sum(c[1] for c in self._efetivas.values())
        return (acertos + self._prior) / (n + 2 * self._prior)


class SeletorCalibrador:
    """Escolhe a penalidade da regressão e, depois, o método de menor log-loss na validação cruzada."""

    def __init__(self, vetorizador: VetorizadorDecisao) -> None:
        """Guarda o vetorizador.

        Args:
            vetorizador: Conversor de decisões em variáveis.
        """
        self._vetorizador: VetorizadorDecisao = vetorizador

    def escolher(
        self, exemplos: Sequence[ExemploCalibracao], penalidades: Sequence[float], partes: int, semente: int
    ) -> tuple[CalibradorBase, list[tuple[str, ValidacaoCalibracao]]]:
        """Valida a grade de penalidades e as faixas, e escolhe o melhor.

        Empates na log-loss (diferença menor que 0,001) ficam com o mais simples: faixas antes da
        regressão, e penalidade maior antes de menor.

        Args:
            exemplos: Gold rotulado.
            penalidades: Grade de penalidades da regressão.
            partes: Partes da validação cruzada.
            semente: Semente.

        Returns:
            ``(calibrador escolhido, [(nome, validação)])`` na ordem testada.
        """
        candidatos: list[CalibradorBase] = [
            CalibradorFaixas(),
            *(CalibradorLogistico(p, self._vetorizador) for p in sorted(penalidades, reverse=True)),
        ]
        resultados: list[tuple[CalibradorBase, ValidacaoCalibracao]] = [
            (c, c.validar(exemplos, partes, semente)) for c in candidatos
        ]
        melhor: float = min(v.log_loss for _, v in resultados)
        escolhido: CalibradorBase = next(c for c, v in resultados if v.log_loss <= melhor + 0.001)
        return escolhido, [(c.nome, v) for c, v in resultados]
