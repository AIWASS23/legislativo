"""Representação lexical, sem modelo (ADR-021): tokenização normalizada e índice BM25.

A tokenização usa o ``ProcessadorTexto`` da etapa 1 (minúsculas, sem acento, só letras e números),
reduz cada palavra ao singular e descarta as palavras sem conteúdo temático (ligação e frases-padrão de
prova, da EDA). Números ficam, porque o número do artigo citado é uma pista forte.
"""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Sequence

import numpy as np

from vicio_ia.estatistica import Matriz
from vicio_ia.texto import ProcessadorTexto


class TokenizadorLexical:
    """Converte texto em termos para o BM25."""

    def __init__(self, processador: ProcessadorTexto, palavras_vazias: frozenset[str]) -> None:
        """Guarda o processador e as palavras descartadas.

        Args:
            processador: Normalizador de texto.
            palavras_vazias: Palavras sem conteúdo temático (já normalizadas).
        """
        self._processador: ProcessadorTexto = processador
        self._vazias: frozenset[str] = palavras_vazias

    def termos(self, texto: str) -> list[str]:
        """Termos do texto, na ordem, com repetição.

        Args:
            texto: Texto qualquer.

        Returns:
            Palavras normalizadas no singular, sem as vazias e sem letras soltas.
        """
        return [
            self._processador.singular(t)
            for t in self._processador.tokens(texto)
            if t not in self._vazias and (len(t) > 1 or t.isdigit())
        ]


class IndiceBM25:
    """Índice BM25 (Okapi) sobre uma lista fixa de documentos."""

    def __init__(self, documentos: Sequence[Sequence[str]], k1: float, b: float) -> None:
        """Indexa os documentos.

        Args:
            documentos: Termos de cada documento.
            k1: Saturação da frequência do termo.
            b: Peso da normalização pelo tamanho do documento.
        """
        self._n: int = len(documentos)
        self._k1: float = k1
        self._b: float = b
        self._tamanhos: Matriz = np.array([len(d) for d in documentos], dtype=np.float64)
        self._media: float = float(self._tamanhos.mean()) if self._n else 0.0
        self._postings: dict[str, list[tuple[int, int]]] = {}
        indice: int
        termos: Sequence[str]
        for indice, termos in enumerate(documentos):
            termo: str
            quantidade: int
            for termo, quantidade in Counter(termos).items():
                self._postings.setdefault(termo, []).append((indice, quantidade))
        self._idf: dict[str, float] = {
            termo: math.log(1.0 + (self._n - len(lista) + 0.5) / (len(lista) + 0.5))
            for termo, lista in self._postings.items()
        }

    def pontuar(self, consulta: Sequence[str]) -> Matriz:
        """Pontuação BM25 da consulta contra cada documento.

        Args:
            consulta: Termos da consulta (repetições contam uma vez).

        Returns:
            Vetor com uma pontuação por documento, na ordem do índice.
        """
        pontos: Matriz = np.zeros(self._n, dtype=np.float64)
        termo: str
        for termo in sorted(set(consulta)):
            lista: list[tuple[int, int]] | None = self._postings.get(termo)
            if not lista:
                continue
            idf: float = self._idf[termo]
            documento: int
            frequencia: int
            for documento, frequencia in lista:
                normal: float = 1.0 - self._b + self._b * float(self._tamanhos[documento]) / self._media
                pontos[documento] += idf * frequencia * (self._k1 + 1.0) / (frequencia + self._k1 * normal)
        return pontos
