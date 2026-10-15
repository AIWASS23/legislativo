"""Métricas dos experimentos no gold (ADR-014): acerto pela régua, curva precisão × cobertura e cobertura a 95%."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from vicio_ia.avaliacao.planilha import RotuloGold
from vicio_ia.avaliacao.pontuador import ModoRegua, PontuadorRegua


@dataclass(frozen=True)
class PrevisaoSistema:
    """O que um sistema publicaria para uma questão.

    Attributes:
        id: ID da questão.
        tema_id: Tema que seria publicado ("" = o sistema não propõe tema).
        pontuacao: Confiança usada para ordenar (maior = publica primeiro).
    """

    id: str
    tema_id: str
    pontuacao: float


@dataclass(frozen=True)
class PontoCurva:
    """Um ponto da curva precisão × cobertura.

    Attributes:
        publicadas: Questões publicadas (as de maior pontuação).
        cobertura: Fração das questões rotuladas que foi publicada.
        precisao: Fração das publicadas que acerta pela régua.
        limiar: Menor pontuação publicada.
    """

    publicadas: int
    cobertura: float
    precisao: float
    limiar: float


@dataclass(frozen=True)
class ResultadoAvaliacao:
    """Desempenho de um sistema no gold, num modo da régua.

    Attributes:
        modo: ``estrita`` ou ``tolerante``.
        rotuladas: Questões rotuladas avaliadas.
        com_tema: Questões em que o sistema propôs tema.
        acertos_top1: Acertos publicando todas as questões com tema.
        precisao_top1: Acertos sobre as questões com tema.
        cobertura_95: Maior cobertura com precisão de pelo menos 95% (publicando pela pontuação).
        curva: Curva precisão × cobertura.
    """

    modo: ModoRegua
    rotuladas: int
    com_tema: int
    acertos_top1: int
    precisao_top1: float
    cobertura_95: float
    curva: tuple[PontoCurva, ...]


class AvaliadorGold:
    """Avalia previsões contra os rótulos do gold com a régua do case."""

    def __init__(self, pontuador: PontuadorRegua, alvo_precisao: float = 0.95) -> None:
        """Define a régua e a precisão-alvo.

        Args:
            pontuador: Régua (estrita e tolerante).
            alvo_precisao: Precisão mínima para medir a cobertura (0,95 no case).
        """
        self._pontuador: PontuadorRegua = pontuador
        self._alvo: float = alvo_precisao

    @property
    def pontuador(self) -> PontuadorRegua:
        """Régua usada."""
        return self._pontuador

    def avaliar(
        self, previsoes: Mapping[str, PrevisaoSistema], rotulos: Sequence[RotuloGold], modo: ModoRegua
    ) -> ResultadoAvaliacao:
        """Calcula as métricas.

        Questões rotuladas sem previsão contam como não publicadas. Publicar uma questão
        rotulada ``fora`` é erro.

        Args:
            previsoes: Previsão por ID.
            rotulos: Rótulos preenchidos e válidos.
            modo: Modo da régua.

        Returns:
            Resultado.
        """
        avaliadas: list[tuple[float, bool]] = []
        rotulo: RotuloGold
        for rotulo in rotulos:
            previsao: PrevisaoSistema | None = previsoes.get(rotulo.id)
            if previsao is None or not previsao.tema_id:
                continue
            avaliadas.append((previsao.pontuacao, self._pontuador.acerta(previsao.tema_id, rotulo, modo)))
        avaliadas.sort(key=lambda par: -par[0])
        curva: list[PontoCurva] = []
        acertos: int = 0
        indice: int
        par: tuple[float, bool]
        for indice, par in enumerate(avaliadas, start=1):
            acertos += par[1]
            ultimo_do_empate: bool = indice == len(avaliadas) or avaliadas[indice][0] != par[0]
            if ultimo_do_empate:
                curva.append(PontoCurva(indice, indice / len(rotulos), acertos / indice, par[0]))
        cobertura: float = max((p.cobertura for p in curva if p.precisao >= self._alvo), default=0.0)
        total_acertos: int = sum(1 for par in avaliadas if par[1])
        return ResultadoAvaliacao(
            modo=modo,
            rotuladas=len(rotulos),
            com_tema=len(avaliadas),
            acertos_top1=total_acertos,
            precisao_top1=total_acertos / len(avaliadas) if avaliadas else 0.0,
            cobertura_95=cobertura,
            curva=tuple(curva),
        )
