"""Mapa lei/artigo → tema da base de conhecimento (ADR-020), lido como dado pela fase de decisão.

O arquivo final (``dados/conhecimento/mapa_artigos.csv``) sai da revisão do autor; enquanto ele não existe,
os experimentos podem ler a proposta (``dados/conhecimento/propostas/mapa_artigos.csv``), que tem as mesmas
colunas de lei, artigos, tema e força, e nenhuma linha revisada.
"""

from __future__ import annotations

import csv
import re
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, TextIO


@dataclass(frozen=True)
class LinhaMapa:
    """Intervalo de artigos de uma lei que aponta um tema.

    Attributes:
        lei: Lei canônica (``CP``, ``CPP``, ``LEP``, ``CF`` ou ``Lei 11.343/2006``).
        art_inicio: Primeiro artigo.
        art_fim: Último artigo.
        tema_id: Tema.
        forca: ``exata`` ou ``ramo``.
        revisado: O autor revisou a linha.
    """

    lei: str
    art_inicio: int
    art_fim: int
    tema_id: str
    forca: str
    revisado: bool


class MapaArtigos:
    """Busca os temas que o mapa associa a um artigo citado."""

    _RE_NUMERO_LEI: ClassVar[re.Pattern[str]] = re.compile(r"^Lei\s+([\d.]+)")

    def __init__(self, linhas: Sequence[LinhaMapa]) -> None:
        """Indexa as linhas pela lei.

        Args:
            linhas: Linhas do mapa.
        """
        self._por_lei: dict[str, list[LinhaMapa]] = {}
        linha: LinhaMapa
        for linha in linhas:
            self._por_lei.setdefault(self.chave_lei(linha.lei), []).append(linha)

    @classmethod
    def ler(cls, arquivo: Path) -> MapaArtigos:
        """Lê o mapa final ou a proposta.

        Args:
            arquivo: ``mapa_artigos.csv``.

        Returns:
            Mapa indexado.
        """
        linhas: list[LinhaMapa] = []
        entrada: TextIO
        with arquivo.open(encoding="utf-8", newline="") as entrada:
            bruta: dict[str, str]
            for bruta in csv.DictReader(entrada):
                linhas.append(
                    LinhaMapa(
                        lei=bruta["lei"],
                        art_inicio=int(bruta["art_inicio"]),
                        art_fim=int(bruta["art_fim"]),
                        tema_id=bruta["tema_id"],
                        forca=bruta["forca"],
                        revisado=bruta.get("revisado", "") == "sim",
                    )
                )
        return cls(linhas)

    @classmethod
    def chave_lei(cls, lei: str) -> str:
        """Chave de comparação da lei: o código, ou o número de uma lei especial sem pontos nem ano.

        Assim, "Lei 9.609" (citada sem o ano) encontra "Lei 9.609/1998" no mapa.

        Args:
            lei: Lei canônica.

        Returns:
            ``CP``, ``CPP``... ou o número (``11343``).
        """
        achado: re.Match[str] | None = cls._RE_NUMERO_LEI.match(lei)
        return achado.group(1).replace(".", "") if achado else lei

    def todas(self) -> list[LinhaMapa]:
        """Todas as linhas, agrupadas por lei.

        Returns:
            Linhas do mapa.
        """
        return [linha for grupo in self._por_lei.values() for linha in grupo]

    def linhas(self, lei: str, inicio: int, fim: int) -> list[LinhaMapa]:
        """Linhas do mapa cujo intervalo cruza os artigos citados.

        Args:
            lei: Lei canônica da citação.
            inicio: Primeiro artigo citado.
            fim: Último artigo citado.

        Returns:
            Linhas, na ordem do arquivo.
        """
        candidatas: list[LinhaMapa] = self._por_lei.get(self.chave_lei(lei), [])
        return [linha for linha in candidatas if linha.art_inicio <= fim and inicio <= linha.art_fim]
