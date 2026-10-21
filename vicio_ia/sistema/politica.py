"""Política de decisão da etapa 2 (ADR-022, ADR-023, ADR-025): nó, extras, regras de fora, calibração e limiar.

- **Nó:** o candidato de maior P(certo); **extras:** até 3 temas de outro ramo com P ≥ 0,5.
- **Regras de fora** (plano B da ADR-023, com motivo explícito):
  - disciplina de origem militar → ``fora`` (a árvore não tem nó militar);
  - proximidade com tema inativo acima do percentil 90 das questões com tema da folha → ``revisar``.
- **Calibração:** identidade, Platt ou Platt com a faixa de concordância entre o denso e o BM25, escolhida pela
  menor log-loss fora da amostra nas 100 da folha.
- **Limiar e previsão** (ADR-013, ADR-025, D15):
  - pela ADR-025, publica-se o maior conjunto das 559 avaliadas cujo percentil 10 da precisão do modelo (bootstrap
    da calibração) é ≥ 95%; sem nenhum, vale a reserva pontual de 97%;
  - pela D15 (decisão do autor), a reserva pontual é o critério: o maior conjunto com ponto do modelo ≥ 97%;
  - o ponto informado junta o estimador direto, que é o acerto fora da amostra das questões da folha na mesma
    faixa, com Jeffreys (D12).
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import ClassVar

import numpy as np
import numpy.typing as npt

from vicio_ia.estatistica import Matriz, RegressaoLogisticaL2
from vicio_ia.sistema.pares import GeradorPares, ParesQuestao


@dataclass(frozen=True)
class EscolhaQuestao:
    """Nó escolhido para uma questão, antes do limiar.

    Attributes:
        id: ID da questão.
        tema: Nó de maior P(certo).
        p: P(certo) do nó, como sai do ranqueador.
        extras: Temas de outro ramo com P ≥ limiar, do mais provável ao menos.
        alternativa: Melhor candidato fora do ramo do nó (para o motivo de ``revisar``).
        concorda: O nó está na faixa de concordância entre o denso e o BM25 (ADR-025).
    """

    id: str
    tema: str
    p: float
    extras: tuple[str, ...]
    alternativa: str
    concorda: bool


class EscolhedorNo:
    """Escolhe o nó e os extras a partir das probabilidades dos candidatos."""

    def __init__(self, gerador: GeradorPares, limiar_extra: float, max_extras: int) -> None:
        """Guarda os parâmetros.

        Args:
            gerador: Gerador dos pares (para os ramos).
            limiar_extra: P mínima de um extra.
            max_extras: Máximo de extras.
        """
        self._gerador: GeradorPares = gerador
        self._limiar_extra: float = limiar_extra
        self._max_extras: int = max_extras

    def escolher(self, pares: ParesQuestao, probabilidades: Matriz) -> EscolhaQuestao:
        """Escolhe o nó de maior P (empate pela ordem dos candidatos) e os extras.

        Args:
            pares: Pares da questão.
            probabilidades: P(certo) de cada candidato.

        Returns:
            Escolha da questão.
        """
        ordem: list[int] = [int(i) for i in np.argsort(-probabilidades, kind="stable")]
        tema: str = pares.candidatos[ordem[0]]
        ramo: frozenset[str] = self._gerador.ramo(tema)
        fora_do_ramo: list[int] = [i for i in ordem if pares.candidatos[i] not in ramo]
        extras: list[str] = []
        indice: int
        for indice in fora_do_ramo:
            candidato: str = pares.candidatos[indice]
            if probabilidades[indice] < self._limiar_extra or len(extras) == self._max_extras:
                break
            if not any(candidato in self._gerador.ramo(e) for e in extras):
                extras.append(candidato)
        alternativa: str = pares.candidatos[fora_do_ramo[0]] if fora_do_ramo else ""
        return EscolhaQuestao(
            pares.id,
            tema,
            float(probabilidades[ordem[0]]),
            tuple(extras),
            alternativa,
            self._gerador.concordancia(pares.id, tema),
        )


class Calibrador:
    """Calibração de P(certo) do nó escolhido (ADR-025).

    Três opções, escolhidas pela menor log-loss fora da amostra nas 100 da folha:
    - ``identidade``: a P do ranqueador;
    - ``platt``: logística no logit da P;
    - ``platt_concordancia``: logística no logit da P e na faixa de evidência de concordância (o melhor tema do
      denso e o do BM25 no mesmo ramo, com o nó escolhido nesse ramo).
    """

    TIPOS: ClassVar[tuple[str, ...]] = ("identidade", "platt", "platt_concordancia")
    NOMES: ClassVar[dict[str, str]] = {
        "identidade": "a identidade",
        "platt": "Platt",
        "platt_concordancia": "Platt com a faixa de concordância entre o denso e o BM25",
    }

    def __init__(self, tipo: str, coeficientes: tuple[float, ...] = ()) -> None:
        """Define o calibrador.

        Args:
            tipo: Um de :attr:`TIPOS`.
            coeficientes: Intercepto e inclinações (vazio na identidade).
        """
        self.tipo: str = tipo
        self.coeficientes: tuple[float, ...] = coeficientes

    @staticmethod
    def logit(p: Matriz) -> Matriz:
        """Logit com as pontas cortadas em 1e-4.

        Args:
            p: Probabilidades.

        Returns:
            Logits.
        """
        cortada: Matriz = np.clip(p, 1e-4, 1 - 1e-4)
        return np.asarray(np.log(cortada / (1 - cortada)), dtype=np.float64)

    @classmethod
    def _atributos(cls, tipo: str, p: Matriz, concorda: Matriz) -> Matriz:
        """Atributos do Platt.

        Args:
            tipo: Tipo do calibrador.
            p: P do ranqueador.
            concorda: 1 na faixa de concordância.

        Returns:
            Matriz de atributos.
        """
        z: Matriz = cls.logit(p)[:, None]
        return np.hstack([z, concorda[:, None]]) if tipo == "platt_concordancia" else z

    @classmethod
    def ajustar(cls, tipo: str, p: Matriz, concorda: Matriz, y: Matriz) -> Calibrador:
        """Ajusta um calibrador do tipo pedido.

        Args:
            tipo: Tipo do calibrador.
            p: P(certo) fora da amostra.
            concorda: 1 na faixa de concordância.
            y: Acerto (0/1).

        Returns:
            Calibrador ajustado.
        """
        if tipo == "identidade":
            return cls(tipo)
        modelo: RegressaoLogisticaL2 = RegressaoLogisticaL2(1e-3).ajustar(
            cls._atributos(tipo, p, concorda), y, np.ones(len(y), dtype=np.float64)
        )
        return cls(tipo, tuple(float(c) for c in modelo.coeficientes))

    def aplicar(self, p: Matriz, concorda: Matriz) -> Matriz:
        """P calibrada.

        Args:
            p: P(certo) do ranqueador.
            concorda: 1 na faixa de concordância.

        Returns:
            P calibrada.
        """
        if self.tipo == "identidade":
            return np.asarray(p, dtype=np.float64)
        coeficientes: Matriz = np.array(self.coeficientes, dtype=np.float64)
        z: Matriz = coeficientes[0] + self._atributos(self.tipo, p, concorda) @ coeficientes[1:]
        return np.asarray(1.0 / (1.0 + np.exp(-z)), dtype=np.float64)

    @staticmethod
    def log_loss(p: Matriz, y: Matriz) -> float:
        """Log-loss média.

        Args:
            p: Probabilidades.
            y: Acerto (0/1).

        Returns:
            Log-loss.
        """
        cortada: Matriz = np.clip(p, 1e-6, 1 - 1e-6)
        return float(-np.mean(y * np.log(cortada) + (1 - y) * np.log(1 - cortada)))

    @classmethod
    def escolher(
        cls, p: Matriz, concorda: Matriz, y: Matriz, partes: int, semente: int
    ) -> tuple[Calibrador, dict[str, float]]:
        """Escolhe o calibrador pela log-loss fora da amostra (validação cruzada em ``partes``).

        Args:
            p: P(certo) fora da amostra do nó escolhido, nas questões da folha.
            concorda: 1 na faixa de concordância.
            y: Acerto pela régua.
            partes: Partes da validação cruzada.
            semente: Semente do sorteio das partes.

        Returns:
            Calibrador ajustado em todos os pontos e a log-loss fora da amostra de cada tipo.
        """
        gerador: np.random.Generator = np.random.default_rng(semente)
        parte: npt.NDArray[np.int64] = np.asarray(gerador.permutation(len(p)) % partes, dtype=np.int64)
        perdas: dict[str, float] = {}
        tipo: str
        for tipo in cls.TIPOS:
            previsto: Matriz = np.zeros(len(p), dtype=np.float64)
            indice: int
            for indice in range(partes):
                teste: npt.NDArray[np.bool_] = np.asarray(parte == indice, dtype=np.bool_)
                treino: npt.NDArray[np.bool_] = np.logical_not(teste)
                ajustado: Calibrador = cls.ajustar(tipo, p[treino], concorda[treino], y[treino])
                previsto[teste] = ajustado.aplicar(p[teste], concorda[teste])
            perdas[tipo] = cls.log_loss(previsto, y)
        melhor: str = min(cls.TIPOS, key=lambda t: (perdas[t], cls.TIPOS.index(t)))
        return cls.ajustar(melhor, p, concorda, y), perdas


@dataclass(frozen=True)
class Previsao:
    """Limiar e previsão de precisão e cobertura para as avaliadas (ADR-025).

    Attributes:
        limiar: P calibrada mínima para publicar; ``inf`` se nada passa.
        publicadas: Publicadas entre as avaliadas elegíveis.
        avaliadas: Total de avaliadas (559).
        precisao: Ponto da precisão informada.
        precisao_intervalo: Percentis 5 e 95.
        precisao_p10: Percentil 10 do estimador do modelo (o critério do limiar).
        modelo: Ponto do estimador do modelo.
        direto: Ponto do estimador direto (0 sem questões da folha na faixa).
        folha_na_faixa: Questões da folha fora da amostra na faixa publicada e quantas estão certas.
        curva: ``(publicadas, ponto, percentil 10)`` do estimador do modelo, para cada corte avaliado.
        regra: ``percentil 10``, ``reserva pontual`` ou ``nenhuma``.
        publicadas_estrito: Publicadas pelo critério estrito (percentil 10 ≥ alvo), para comparação.
    """

    limiar: float
    publicadas: int
    avaliadas: int
    precisao: float
    precisao_intervalo: tuple[float, float]
    precisao_p10: float
    modelo: float
    direto: float
    folha_na_faixa: tuple[int, int]
    curva: tuple[tuple[int, float, float], ...]
    regra: str
    publicadas_estrito: int


class EstimadorLimiar:
    """Escolhe o limiar e estima a precisão do conjunto publicado (sorteios com semente fixa)."""

    def __init__(
        self,
        p_folha: Matriz,
        concorda_folha: Matriz,
        acerto_folha: Matriz,
        calibrador: Calibrador,
        sorteios: int,
        semente: int,
    ) -> None:
        """Guarda a folha fora da amostra.

        Args:
            p_folha: P(certo) fora da amostra do nó escolhido, nas questões da folha.
            concorda_folha: 1 na faixa de concordância.
            acerto_folha: Acerto pela régua (0/1).
            calibrador: Calibrador escolhido.
            sorteios: Número de sorteios.
            semente: Semente.
        """
        self._p: Matriz = p_folha
        self._concorda: Matriz = concorda_folha
        self._y: Matriz = acerto_folha
        self._calibrador: Calibrador = calibrador
        self._sorteios: int = sorteios
        self._semente: int = semente

    def estimar(
        self,
        p_avaliadas: Matriz,
        concorda_avaliadas: Matriz,
        alvo: float,
        percentil: float,
        reserva: float,
        avaliadas: int,
        min_direto: int,
        min_parcial: int,
        criterio: str,
    ) -> Previsao:
        """Avalia todos os cortes entre valores distintos da P calibrada e escolhe o maior conjunto admissível.

        Como na etapa 1 (ADR-013, ADR-025): o conjunto de cada corte fica fixo pela calibração principal, e o
        critério do limiar usa os sorteios do estimador do modelo (a P média das publicadas com a calibração
        refeita em cada bootstrap da folha; a identidade, que não tem parâmetro, é refeita como Platt). Se nenhum
        corte alcança o alvo no percentil, vale a reserva pontual. O ponto informado junta o estimador direto
        (acerto fora da amostra das questões da folha na faixa, com Jeffreys): só ele, com ``min_direto`` ou mais
        questões na faixa; a média dos dois, com menos (D12); só o modelo, com menos de ``min_parcial`` (D15).

        Args:
            p_avaliadas: P(certo) do ranqueador das avaliadas elegíveis (sem regra de fora ou de revisão).
            concorda_avaliadas: 1 na faixa de concordância.
            alvo: Precisão mínima no percentil.
            percentil: Percentil do critério (0,10).
            reserva: Ponto mínimo da reserva pontual (0,97).
            avaliadas: Total de avaliadas (o denominador da cobertura).
            min_direto: Questões da folha na faixa a partir das quais o ponto é só o estimador direto.
            min_parcial: Questões da folha na faixa abaixo das quais o estimador direto não entra (D15).
            criterio: ``percentil`` (ADR-025: percentil 10 ≥ alvo, reserva se nenhum) ou ``reserva`` (D15: ponto
                do modelo ≥ reserva).

        Returns:
            Previsão no corte escolhido.
        """
        calibradas: Matriz = self._calibrador.aplicar(p_avaliadas, concorda_avaliadas)
        ordem: npt.NDArray[np.intp] = np.argsort(-calibradas, kind="stable")
        p_ordem: Matriz = p_avaliadas[ordem]
        concorda_ordem: Matriz = concorda_avaliadas[ordem]
        calibradas_ordem: Matriz = calibradas[ordem]
        cortes: Matriz = np.array(sorted({float(v) for v in calibradas_ordem}, reverse=True), dtype=np.float64)
        quantas: npt.NDArray[np.intp] = np.searchsorted(-calibradas_ordem, -cortes, side="right")
        tipo_sorteio: str = "platt" if self._calibrador.tipo == "identidade" else self._calibrador.tipo
        gerador: np.random.Generator = np.random.default_rng(self._semente)
        n_folha: int = len(self._p)
        modelo: Matriz = np.zeros((self._sorteios, len(cortes)), dtype=np.float64)
        sorteio: int
        for sorteio in range(self._sorteios):
            indices: npt.NDArray[np.int64] = gerador.integers(0, n_folha, size=n_folha)
            reamostrado: Calibrador = Calibrador.ajustar(
                tipo_sorteio, self._p[indices], self._concorda[indices], self._y[indices]
            )
            acumulada: Matriz = np.cumsum(reamostrado.aplicar(p_ordem, concorda_ordem)) / np.arange(1, len(p_ordem) + 1)
            modelo[sorteio] = acumulada[quantas - 1]
        pontos: Matriz = modelo.mean(axis=0)
        p10: Matriz = np.quantile(modelo, percentil, axis=0)
        curva: list[tuple[int, float, float]] = [
            (int(quantas[k]), float(pontos[k]), float(p10[k])) for k in range(len(cortes))
        ]
        estritos: list[int] = [k for k in range(len(cortes)) if p10[k] >= alvo]
        publicadas_estrito: int = max((curva[k][0] for k in estritos), default=0)
        admissiveis: list[int] = estritos if criterio == "percentil" else []
        regra: str = "percentil 10"
        if not admissiveis:
            admissiveis = [k for k in range(len(cortes)) if pontos[k] >= reserva]
            regra = "reserva pontual"
        if not admissiveis:
            return Previsao(
                math.inf,
                0,
                avaliadas,
                0.0,
                (0.0, 0.0),
                0.0,
                0.0,
                0.0,
                (0, 0),
                tuple(curva),
                "nenhuma",
                publicadas_estrito,
            )
        escolhido: int = max(admissiveis, key=lambda k: (curva[k][0], -k))
        corte_final: float = float(cortes[escolhido])
        faixa: npt.NDArray[np.bool_] = np.asarray(
            self._calibrador.aplicar(self._p, self._concorda) >= corte_final, dtype=np.bool_
        )
        n: int = int(faixa.sum())
        h: int = int(self._y[faixa].sum())
        sorteios_modelo: Matriz = modelo[:, escolhido]
        sorteios_direto: Matriz = gerador.beta(h + 0.5, n - h + 0.5, size=self._sorteios)
        direto: float = (h + 0.5) / (n + 1)
        combinado: Matriz
        ponto: float
        if n < min_parcial:
            combinado, ponto = sorteios_modelo, float(pontos[escolhido])
        elif n >= min_direto:
            combinado, ponto = sorteios_direto, direto
        else:
            combinado, ponto = (sorteios_modelo + sorteios_direto) / 2.0, (float(pontos[escolhido]) + direto) / 2.0
        return Previsao(
            limiar=corte_final,
            publicadas=curva[escolhido][0],
            avaliadas=avaliadas,
            precisao=ponto,
            precisao_intervalo=(float(np.quantile(combinado, 0.05)), float(np.quantile(combinado, 0.95))),
            precisao_p10=float(p10[escolhido]),
            modelo=float(pontos[escolhido]),
            direto=direto if n else 0.0,
            folha_na_faixa=(n, h),
            curva=tuple(curva),
            regra=regra,
            publicadas_estrito=publicadas_estrito,
        )


class RegrasFora:
    """Regras de fora e de revisão com motivo explícito (ADR-023, plano B)."""

    MOTIVO_MILITAR: str = "direito militar: a árvore não tem tema militar"
    MOTIVO_INATIVO: str = "perto de um tema inativo da árvore: possível fora da taxonomia"

    def __init__(self, limiar_inativo: float) -> None:
        """Define o corte da proximidade com tema inativo.

        Args:
            limiar_inativo: Valor acima do qual a questão vai para ``revisar``.
        """
        self.limiar_inativo: float = limiar_inativo

    @staticmethod
    def militar(disciplina_origem: str) -> bool:
        """Diz se a disciplina de origem é de direito militar.

        Args:
            disciplina_origem: Disciplina de origem (como veio do banco).

        Returns:
            ``True`` se for militar.
        """
        return "militar" in disciplina_origem.lower()

    def inativo(self, valor: float) -> bool:
        """Diz se a questão está perto demais de um tema inativo.

        Args:
            valor: Similaridade com o inativo mais próximo menos a similaridade máxima.

        Returns:
            ``True`` se passar do corte.
        """
        return valor > self.limiar_inativo

    @staticmethod
    def limiar_da_folha(valores_com_tema: Sequence[float], percentil: float) -> float:
        """Corte no percentil das questões com tema da folha.

        Args:
            valores_com_tema: Proximidade com tema inativo das questões com tema da folha.
            percentil: Percentil (0,90).

        Returns:
            Corte.
        """
        return float(np.quantile(np.asarray(valores_com_tema, dtype=np.float64), percentil))
