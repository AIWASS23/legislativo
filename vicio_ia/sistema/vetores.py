"""Vetores de embedding em cache como artefato versionado (ADR-021).

A fase de conhecimento grava, e a fase de decisão só lê, os vetores em ``dados/conhecimento/embeddings/``:
um ``.npy`` (``float32``, normalizado) e a lista de IDs para cada conjunto (questões, alternativas e temas),
mais o ``modelo.json`` com o modelo, o digest e o hash dos textos de entrada. Nenhum modelo é chamado aqui.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import numpy as np

from vicio_ia.estatistica import Matriz


class ErroVetores(Exception):
    """Os vetores em disco estão ausentes ou inconsistentes."""


@dataclass(frozen=True)
class ConjuntoVetores:
    """Vetores normalizados de um conjunto de textos.

    Attributes:
        ids: ID de cada linha (``Q0001``, ``Q0001:A``, ``5159``).
        matriz: Uma linha por ID, com norma 1.
    """

    ids: tuple[str, ...]
    matriz: Matriz

    def submatriz(self, ids: Sequence[str]) -> Matriz:
        """Vetores de vários IDs, na ordem pedida.

        Args:
            ids: IDs.

        Returns:
            Matriz com uma linha por ID.

        Raises:
            ErroVetores: Se algum ID não tiver vetor.
        """
        posicao: dict[str, int] = {i: k for k, i in enumerate(self.ids)}
        faltando: list[str] = [i for i in ids if i not in posicao]
        if faltando:
            raise ErroVetores(f"sem vetor para {len(faltando)} IDs (ex.: {faltando[:3]})")
        return self.matriz[[posicao[i] for i in ids]]


@dataclass(frozen=True)
class VetoresConhecimento:
    """Os três conjuntos de vetores de um modelo.

    Attributes:
        modelo: Modelo que gerou os vetores.
        questoes: Questão inteira (enunciado, comando e alternativas).
        alternativas: Cada alternativa das questões de múltipla escolha.
        temas: Documento de cada tema publicável.
    """

    modelo: str
    questoes: ConjuntoVetores
    alternativas: ConjuntoVetores
    temas: ConjuntoVetores


class ArquivoVetores:
    """Grava e lê os vetores de ``dados/conhecimento/embeddings/``."""

    CONJUNTOS: ClassVar[tuple[str, ...]] = ("questoes", "alternativas", "temas")

    def __init__(self, pasta: Path) -> None:
        """Define a pasta.

        Args:
            pasta: ``dados/conhecimento/embeddings``.
        """
        self._pasta: Path = pasta

    @staticmethod
    def normalizar(matriz: Matriz) -> Matriz:
        """Divide cada linha pela sua norma (linhas nulas ficam nulas).

        Args:
            matriz: Vetores brutos.

        Returns:
            Vetores com norma 1.
        """
        normas: Matriz = np.linalg.norm(matriz, axis=1, keepdims=True)
        return np.asarray(matriz / np.where(normas > 0, normas, 1.0), dtype=np.float64)

    def gravar(self, vetores: VetoresConhecimento, info: Mapping[str, object]) -> list[Path]:
        """Grava os três conjuntos e o ``modelo.json``.

        Args:
            vetores: Vetores do modelo escolhido.
            info: Proveniência (modelo, digest, prefixos, hash dos textos).

        Returns:
            Arquivos gravados.
        """
        self._pasta.mkdir(parents=True, exist_ok=True)
        gravados: list[Path] = []
        nome: str
        conjunto: ConjuntoVetores
        for nome, conjunto in zip(self.CONJUNTOS, (vetores.questoes, vetores.alternativas, vetores.temas), strict=True):
            matriz: Path = self._pasta / f"{nome}.npy"
            ids: Path = self._pasta / f"{nome}_ids.json"
            np.save(matriz, conjunto.matriz.astype(np.float32), allow_pickle=False)
            ids.write_text(json.dumps(list(conjunto.ids), ensure_ascii=False) + "\n", encoding="utf-8")
            gravados.extend([matriz, ids])
        modelo: Path = self._pasta / "modelo.json"
        modelo.write_text(json.dumps(dict(info), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        gravados.append(modelo)
        return gravados

    def ler(self) -> VetoresConhecimento:
        """Lê os vetores gravados.

        Returns:
            Vetores do modelo escolhido.

        Raises:
            ErroVetores: Se faltar arquivo ou se IDs e linhas não baterem.
        """
        modelo: Path = self._pasta / "modelo.json"
        if not modelo.is_file():
            raise ErroVetores(f"{modelo} não existe (rode: uv run python executar_embeddings.py)")
        info: object = json.loads(modelo.read_text(encoding="utf-8"))
        conjuntos: list[ConjuntoVetores] = []
        nome: str
        for nome in self.CONJUNTOS:
            matriz: Matriz = np.asarray(np.load(self._pasta / f"{nome}.npy", allow_pickle=False), dtype=np.float64)
            ids: object = json.loads((self._pasta / f"{nome}_ids.json").read_text(encoding="utf-8"))
            if not isinstance(ids, list) or len(ids) != matriz.shape[0]:
                raise ErroVetores(f"{nome}: {matriz.shape[0]} vetores e IDs inconsistentes")
            conjuntos.append(ConjuntoVetores(tuple(str(i) for i in ids), matriz))
        return VetoresConhecimento(
            modelo=str(info.get("modelo", "")) if isinstance(info, dict) else "",
            questoes=conjuntos[0],
            alternativas=conjuntos[1],
            temas=conjuntos[2],
        )
