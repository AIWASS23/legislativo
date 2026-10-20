"""Validação cruzada repetida e estratificada na folha-verdade (ADR-024).

Cada repetição embaralha as questões dentro de cada estrato (disciplina do tema central, ou "fora") e
as distribui em rodízio pelas partes, de modo que todas as partes tenham a mesma mistura. A repetição
``r`` usa a semente ``semente + r``: o resultado é o mesmo em toda execução.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np

from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.sistema.folha import RotuloFolha


@dataclass(frozen=True)
class Particao:
    """Uma divisão treino/teste.

    Attributes:
        repeticao: Número da repetição (0 em diante).
        parte: Número da parte que é teste (0 em diante).
        treino: Índices de treino.
        teste: Índices de teste.
    """

    repeticao: int
    parte: int
    treino: tuple[int, ...]
    teste: tuple[int, ...]


class ValidacaoCruzadaRepetida:
    """Gera as partições da validação cruzada repetida e estratificada."""

    ESTRATO_FORA: str = "fora"

    def __init__(self, partes: int, repeticoes: int, semente: int) -> None:
        """Define o desenho.

        Args:
            partes: Número de partes (``k``).
            repeticoes: Número de repetições.
            semente: Semente base.

        Raises:
            ValueError: Se ``partes`` for menor que 2 ou ``repeticoes`` menor que 1.
        """
        if partes < 2 or repeticoes < 1:
            raise ValueError("a validação cruzada precisa de pelo menos 2 partes e 1 repetição")
        self._partes: int = partes
        self._repeticoes: int = repeticoes
        self._semente: int = semente

    @classmethod
    def estratos_folha(cls, rotulos: Sequence[RotuloFolha], temas: Sequence[TemaPreparado]) -> list[str]:
        """Estrato de cada rótulo: a disciplina do tema central, ou "fora".

        Args:
            rotulos: Rótulos da folha.
            temas: Árvore preparada.

        Returns:
            Estratos, na ordem dos rótulos.
        """
        disciplina: Mapping[str, str] = {tema.tema_id: tema.disciplina for tema in temas}
        return [cls.ESTRATO_FORA if r.fora else disciplina.get(r.tema_central_id, "?") for r in rotulos]

    def particoes(self, estratos: Sequence[str]) -> list[Particao]:
        """Gera todas as partições, repetição por repetição.

        Args:
            estratos: Estrato de cada exemplo.

        Returns:
            ``repeticoes × partes`` partições; em cada repetição, cada exemplo cai em teste uma vez só.
        """
        n: int = len(estratos)
        grupos: dict[str, list[int]] = {}
        indice: int
        for indice in range(n):
            grupos.setdefault(estratos[indice], []).append(indice)
        particoes: list[Particao] = []
        repeticao: int
        for repeticao in range(self._repeticoes):
            gerador: np.random.Generator = np.random.default_rng(self._semente + repeticao)
            parte_de: list[int] = [0] * n
            contador: int = int(gerador.integers(self._partes))
            estrato: str
            for estrato in sorted(grupos):
                membros: list[int] = [int(i) for i in gerador.permutation(grupos[estrato])]
                for indice in membros:
                    parte_de[indice] = contador % self._partes
                    contador += 1
            parte: int
            for parte in range(self._partes):
                teste: tuple[int, ...] = tuple(i for i in range(n) if parte_de[i] == parte)
                treino: tuple[int, ...] = tuple(i for i in range(n) if parte_de[i] != parte)
                particoes.append(Particao(repeticao, parte, treino, teste))
        return particoes
