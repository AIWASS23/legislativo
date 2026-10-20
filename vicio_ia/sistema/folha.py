"""Folha-verdade da etapa 2 e a régua de acerto nova (ADR-024).

A régua da etapa 2 conta como certo publicar no tema central da equipe, num dos extras, ou num nó do
mesmo ramo de qualquer um deles (pai ou filho direto). Publicar em outro subtema do mesmo tema (irmão)
é erro, e publicar uma questão que a equipe marcou como fora da taxonomia é sempre erro.
"""

from __future__ import annotations

import csv
from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, TextIO

from vicio_ia.preparacao.arvore_preparada import TemaPreparado


class ErroFolha(Exception):
    """A folha-verdade não está no formato do LEIA-ME."""


@dataclass(frozen=True)
class RotuloFolha:
    """Uma questão classificada pela equipe.

    Attributes:
        id: ID da questão.
        tema_central_id: Tema central (vazio quando a questão é fora da taxonomia).
        extras_ids: Outros temas que a questão também cobre.
        fora: A equipe marcou a questão como fora da taxonomia.
    """

    id: str
    tema_central_id: str
    extras_ids: tuple[str, ...]
    fora: bool

    @property
    def alvos(self) -> tuple[str, ...]:
        """Temas que contam como acerto (com os vizinhos de ramo): o central e os extras."""
        return () if self.fora else (self.tema_central_id, *self.extras_ids)


class LeitorFolha:
    """Lê e valida ``folha_verdade.csv``."""

    COLUNAS: ClassVar[tuple[str, ...]] = (
        "id",
        "tema_central_id",
        "tema_central_caminho",
        "extras_ids",
        "fora_da_taxonomia",
    )

    def __init__(self, caminho: Path, temas: Sequence[TemaPreparado], ids_questoes: Collection[str]) -> None:
        """Guarda o arquivo e o que é preciso para validá-lo.

        Args:
            caminho: ``folha_verdade.csv``.
            temas: Árvore preparada.
            ids_questoes: IDs das questões do case.
        """
        self._caminho: Path = caminho
        self._temas: dict[str, TemaPreparado] = {tema.tema_id: tema for tema in temas}
        self._ids_questoes: frozenset[str] = frozenset(ids_questoes)

    def ler(self) -> list[RotuloFolha]:
        """Lê a folha e confere cada linha.

        Returns:
            Rótulos na ordem do arquivo.

        Raises:
            ErroFolha: Com todos os problemas encontrados, se houver algum.
        """
        if not self._caminho.is_file():
            raise ErroFolha(f"{self._caminho} não existe")
        arquivo: TextIO
        with self._caminho.open(encoding="utf-8", newline="") as arquivo:
            leitor: csv.DictReader[str] = csv.DictReader(arquivo)
            faltantes: list[str] = [c for c in self.COLUNAS if c not in (leitor.fieldnames or [])]
            if faltantes:
                raise ErroFolha(f"{self._caminho.name}: colunas ausentes {faltantes}")
            linhas: list[dict[str, str]] = list(leitor)
        rotulos: list[RotuloFolha] = []
        problemas: list[str] = []
        vistos: set[str] = set()
        linha: dict[str, str]
        for linha in linhas:
            rotulo: RotuloFolha = self._rotulo(linha)
            problemas.extend(self._problemas(rotulo, linha.get("fora_da_taxonomia", ""), vistos))
            vistos.add(rotulo.id)
            rotulos.append(rotulo)
        if problemas:
            raise ErroFolha(f"{self._caminho.name}: " + "; ".join(problemas))
        return rotulos

    @staticmethod
    def _rotulo(linha: Mapping[str, str]) -> RotuloFolha:
        """Converte uma linha do CSV.

        Args:
            linha: Linha do CSV.

        Returns:
            Rótulo.
        """
        extras: tuple[str, ...] = tuple(x.strip() for x in linha.get("extras_ids", "").split(";") if x.strip())
        return RotuloFolha(
            id=linha.get("id", "").strip(),
            tema_central_id=linha.get("tema_central_id", "").strip(),
            extras_ids=extras,
            fora=linha.get("fora_da_taxonomia", "").strip() == "1",
        )

    def _problemas(self, rotulo: RotuloFolha, fora_bruto: str, vistos: Collection[str]) -> list[str]:
        """Confere um rótulo.

        Args:
            rotulo: Rótulo convertido.
            fora_bruto: Valor original de ``fora_da_taxonomia``.
            vistos: IDs já lidos.

        Returns:
            Problemas encontrados (vazio se o rótulo estiver certo).
        """
        problemas: list[str] = []
        if rotulo.id not in self._ids_questoes:
            problemas.append(f"{rotulo.id}: questão inexistente")
        if rotulo.id in vistos:
            problemas.append(f"{rotulo.id}: repetida")
        if fora_bruto.strip() not in {"0", "1"}:
            problemas.append(f"{rotulo.id}: fora_da_taxonomia deve ser 0 ou 1")
        if rotulo.fora and rotulo.tema_central_id:
            problemas.append(f"{rotulo.id}: fora da taxonomia com tema central")
        if not rotulo.fora and not rotulo.tema_central_id:
            problemas.append(f"{rotulo.id}: sem tema central e sem marca de fora")
        tema_id: str
        for tema_id in rotulo.alvos:
            tema: TemaPreparado | None = self._temas.get(tema_id)
            if tema is None:
                problemas.append(f"{rotulo.id}: tema {tema_id} inexistente")
            elif tema.status != "active":
                problemas.append(f"{rotulo.id}: tema {tema_id} inativo")
        return problemas


class ReguaEtapa2:
    """Régua de acerto da etapa 2: central, extra, ou pai ou filho de um deles."""

    def __init__(self, temas: Sequence[TemaPreparado]) -> None:
        """Monta o mapa de pais.

        Args:
            temas: Árvore preparada.
        """
        self._pai: dict[str, str | None] = {tema.tema_id: tema.parent_id for tema in temas}

    def mesmo_ramo(self, tema_a: str, tema_b: str) -> bool:
        """Mesmo nó, ou um é pai direto do outro (relação simétrica).

        Args:
            tema_a: Um tema.
            tema_b: Outro tema.

        Returns:
            ``True`` se estiverem no mesmo ramo.
        """
        if tema_a == tema_b:
            return bool(tema_a)
        return self._pai.get(tema_a) == tema_b or self._pai.get(tema_b) == tema_a

    def acerta(self, tema_publicado: str, rotulo: RotuloFolha) -> bool:
        """Diz se publicar ``tema_publicado`` contaria como certo para o rótulo da equipe.

        Args:
            tema_publicado: Tema escolhido pelo sistema.
            rotulo: Rótulo da equipe.

        Returns:
            ``True`` se o tema estiver no ramo do central ou de algum extra; ``False`` se a questão for fora.
        """
        if rotulo.fora or not tema_publicado:
            return False
        return any(self.mesmo_ramo(tema_publicado, alvo) for alvo in rotulo.alvos)
