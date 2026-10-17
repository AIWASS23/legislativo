"""Planilha de rótulos manuais e caderno de rotulagem do gold set (ADR-012).

A planilha (``dados/gold/rotulos_leva1.csv``) é a única fonte dos rótulos. O código
cria a planilha vazia e acrescenta linhas, mas **nunca apaga nem sobrescreve um rótulo**.
"""

from __future__ import annotations

import csv
import os
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Literal, TextIO

from vicio_ia.avaliacao.amostragem import ItemAmostra
from vicio_ia.configuracao import ParametrosGold
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada

type SituacaoRotulo = Literal["pendente", "rotulada", "invalida"]
"""Situação de uma linha da planilha."""


class ErroPlanilha(Exception):
    """A planilha de rótulos tem estrutura inválida (colunas, IDs fora da amostra)."""


@dataclass(frozen=True)
class RotuloGold:
    """Rótulo manual de uma questão.

    Attributes:
        id: ID da questão.
        tema_id: Nó mais específico em que há segurança ("" se ``fora`` ou pendente).
        alternativos: Outros nós plausíveis (irmãos, par de sobreposição).
        fora: A questão não pertence a nenhum tema do recorte.
        multitema: A questão cobre mais de um tema de forma equilibrada.
        certeza: ``alta``, ``media`` ou ``baixa`` ("" se pendente).
        observacao: Texto livre (dúvida, fonte consultada, uso de LLM para explicar conteúdo).
        minutos: Tempo gasto na questão (``None`` se não medido).
        rotulado_em: Data e hora do rótulo (ISO 8601).
    """

    id: str
    tema_id: str
    alternativos: tuple[str, ...]
    fora: bool
    multitema: bool
    certeza: str
    observacao: str
    minutos: float | None
    rotulado_em: str

    @property
    def preenchido(self) -> bool:
        """Indica se a linha já tem decisão (tema ou ``fora``)."""
        return self.fora or bool(self.tema_id)

    @classmethod
    def vazio(cls, questao_id: str) -> RotuloGold:
        """Cria uma linha pendente.

        Args:
            questao_id: ID da questão.

        Returns:
            Rótulo sem decisão.
        """
        return cls(questao_id, "", (), False, False, "", "", None, "")


@dataclass(frozen=True)
class SituacaoLinha:
    """Resultado da validação de uma linha.

    Attributes:
        rotulo: Rótulo lido.
        situacao: Pendente, rotulada ou inválida.
        problemas: O que está errado (vazio se válida).
    """

    rotulo: RotuloGold
    situacao: SituacaoRotulo
    problemas: tuple[str, ...]


class PlanilhaRotulos:
    """Lê, valida e grava a planilha de rótulos do gold set."""

    COLUNAS: ClassVar[tuple[str, ...]] = (
        "id",
        "tema_id",
        "alternativos",
        "fora",
        "multitema",
        "certeza",
        "observacao",
        "minutos",
        "rotulado_em",
    )
    SIM_NAO: ClassVar[frozenset[str]] = frozenset({"s", "n", ""})

    def __init__(self, caminho: Path, parametros: ParametrosGold, temas: Sequence[TemaPreparado]) -> None:
        """Define o arquivo e os temas aceitos.

        Args:
            caminho: ``dados/gold/rotulos_leva1.csv``.
            parametros: Parâmetros do gold set (níveis de certeza).
            temas: Árvore preparada (só os publicáveis valem como rótulo).
        """
        self._caminho: Path = caminho
        self._certezas: frozenset[str] = frozenset(parametros.niveis_certeza)
        self._publicaveis: frozenset[str] = frozenset(tema.tema_id for tema in temas if tema.publicavel)
        self._canonicos: dict[str, str] = {
            tema.tema_id: tema.canonico_id for tema in temas if tema.canonico_id is not None
        }

    @property
    def caminho(self) -> Path:
        """Caminho da planilha."""
        return self._caminho

    def garantir(self, amostra: Sequence[ItemAmostra]) -> int:
        """Cria a planilha se não existir; se existir, só acrescenta IDs novos da amostra.

        Args:
            amostra: Itens sorteados, na ordem de rotulagem.

        Returns:
            Número de linhas acrescentadas.

        Raises:
            ErroPlanilha: Se a planilha tiver IDs que não estão na amostra.
        """
        existentes: list[RotuloGold] = self.ler() if self._caminho.is_file() else []
        ids_amostra: set[str] = {item.id for item in amostra}
        estranhos: list[str] = [rotulo.id for rotulo in existentes if rotulo.id not in ids_amostra]
        if estranhos:
            raise ErroPlanilha(f"{self._caminho.name}: IDs fora da amostra {estranhos}")
        ja_tem: set[str] = {rotulo.id for rotulo in existentes}
        novos: list[RotuloGold] = [RotuloGold.vazio(item.id) for item in amostra if item.id not in ja_tem]
        if novos or not self._caminho.is_file():
            self._gravar([*existentes, *novos])
        return len(novos)

    def ler(self) -> list[RotuloGold]:
        """Lê a planilha.

        Returns:
            Rótulos na ordem do arquivo.

        Raises:
            ErroPlanilha: Se faltar coluna ou houver ID repetido.
        """
        rotulos: list[RotuloGold] = []
        vistos: set[str] = set()
        arquivo: TextIO
        with self._caminho.open(encoding="utf-8", newline="") as arquivo:
            leitor: csv.DictReader[str] = csv.DictReader(arquivo)
            faltantes: list[str] = [c for c in self.COLUNAS if c not in (leitor.fieldnames or [])]
            if faltantes:
                raise ErroPlanilha(f"{self._caminho.name}: colunas ausentes {faltantes}")
            linha: dict[str, str]
            for linha in leitor:
                limpa: dict[str, str] = {chave: (valor or "").strip() for chave, valor in linha.items()}
                if limpa["id"] in vistos:
                    raise ErroPlanilha(f"{self._caminho.name}: ID repetido {limpa['id']}")
                vistos.add(limpa["id"])
                rotulos.append(self._de_linha(limpa))
        return rotulos

    def registrar(self, rotulo: RotuloGold) -> None:
        """Grava o rótulo de uma questão pendente (gravação atômica).

        Args:
            rotulo: Rótulo completo.

        Raises:
            ErroPlanilha: Se a questão não estiver na planilha ou já tiver rótulo.
        """
        rotulos: list[RotuloGold] = self.ler()
        indices: list[int] = [i for i, atual in enumerate(rotulos) if atual.id == rotulo.id]
        if not indices:
            raise ErroPlanilha(f"{rotulo.id} não está na planilha")
        if rotulos[indices[0]].preenchido:
            raise ErroPlanilha(f"{rotulo.id} já tem rótulo; corrija à mão no CSV se for o caso")
        rotulos[indices[0]] = rotulo
        self._gravar(rotulos)

    def validar(self, rotulos: Sequence[RotuloGold]) -> list[SituacaoLinha]:
        """Confere cada linha preenchida.

        Regras: ``tema_id`` e ``alternativos`` são publicáveis (fantasma é recusado com a
        indicação do canônico); ``fora`` exclui ``tema_id``; ``certeza`` é um dos níveis.

        Args:
            rotulos: Rótulos lidos.

        Returns:
            Situação de cada linha, na mesma ordem.
        """
        situacoes: list[SituacaoLinha] = []
        rotulo: RotuloGold
        for rotulo in rotulos:
            if not rotulo.preenchido:
                situacoes.append(SituacaoLinha(rotulo, "pendente", ()))
                continue
            problemas: list[str] = []
            if rotulo.fora and rotulo.tema_id:
                problemas.append("fora=s com tema_id preenchido")
            if rotulo.tema_id:
                problemas.extend(self._problemas_tema(rotulo.tema_id, "tema_id"))
            alternativo: str
            for alternativo in rotulo.alternativos:
                problemas.extend(self._problemas_tema(alternativo, "alternativos"))
            if rotulo.tema_id and rotulo.tema_id in rotulo.alternativos:
                problemas.append("tema_id repetido em alternativos")
            if rotulo.certeza not in self._certezas:
                problemas.append(f"certeza {rotulo.certeza!r} fora de {sorted(self._certezas)}")
            if rotulo.minutos is not None and rotulo.minutos < 0:
                problemas.append("minutos negativo")
            situacoes.append(SituacaoLinha(rotulo, "invalida" if problemas else "rotulada", tuple(problemas)))
        return situacoes

    def _problemas_tema(self, tema_id: str, campo: str) -> list[str]:
        """Confere se um ID pode ser rótulo.

        Args:
            tema_id: ID informado.
            campo: Coluna de onde veio.

        Returns:
            Problemas encontrados.
        """
        if tema_id in self._publicaveis:
            return []
        if tema_id in self._canonicos:
            return [f"{campo}: {tema_id} é fantasma; use o canônico {self._canonicos[tema_id]}"]
        return [f"{campo}: {tema_id} não é tema publicável"]

    def _de_linha(self, linha: Mapping[str, str]) -> RotuloGold:
        """Converte uma linha do CSV em rótulo.

        Args:
            linha: Valores sem espaços nas pontas.

        Returns:
            Rótulo.

        Raises:
            ErroPlanilha: Se ``fora``, ``multitema`` ou ``minutos`` tiver valor inválido.
        """
        fora: str = linha["fora"].lower()
        multitema: str = linha["multitema"].lower()
        if fora not in self.SIM_NAO or multitema not in self.SIM_NAO:
            raise ErroPlanilha(f"{self._caminho.name}, {linha['id']}: fora e multitema aceitam s, n ou vazio")
        minutos: float | None = None
        if linha["minutos"]:
            try:
                minutos = float(linha["minutos"].replace(",", "."))
            except ValueError as erro:
                raise ErroPlanilha(f"{self._caminho.name}, {linha['id']}: minutos inválido") from erro
        alternativos: tuple[str, ...] = tuple(
            parte.strip() for parte in linha["alternativos"].replace(",", ";").split(";") if parte.strip()
        )
        return RotuloGold(
            id=linha["id"],
            tema_id=linha["tema_id"],
            alternativos=alternativos,
            fora=fora == "s",
            multitema=multitema == "s",
            certeza=linha["certeza"].lower().replace("é", "e"),
            observacao=linha["observacao"],
            minutos=minutos,
            rotulado_em=linha["rotulado_em"],
        )

    def _gravar(self, rotulos: Sequence[RotuloGold]) -> None:
        """Grava a planilha inteira num arquivo temporário e troca de uma vez.

        Args:
            rotulos: Todas as linhas.
        """
        linhas: list[list[str]] = [
            [
                rotulo.id,
                rotulo.tema_id,
                ";".join(rotulo.alternativos),
                ("s" if rotulo.fora else "n") if rotulo.preenchido else "",
                ("s" if rotulo.multitema else "n") if rotulo.preenchido else "",
                rotulo.certeza,
                rotulo.observacao,
                "" if rotulo.minutos is None else f"{rotulo.minutos:.1f}",
                rotulo.rotulado_em,
            ]
            for rotulo in rotulos
        ]
        self._caminho.parent.mkdir(parents=True, exist_ok=True)
        temporario: Path = self._caminho.with_suffix(".csv.tmp")
        arquivo: TextIO
        with temporario.open("w", encoding="utf-8", newline="") as arquivo:
            csv.writer(arquivo).writerows([list(self.COLUNAS), *linhas])
            arquivo.flush()
            os.fsync(arquivo.fileno())
        os.replace(temporario, self._caminho)


class CadernoRotulagem:
    """Gera o caderno em Markdown com as questões do gold set, na ordem de rotulagem.

    O caderno mostra **só o texto canônico** (ADR-004): nada de saída de modelo, nem os
    rótulos de origem, para o rótulo ficar cego e independente (ADR-006, ADR-012).
    """

    def escrever(
        self,
        destino: Path,
        amostra: Sequence[ItemAmostra],
        questoes: Mapping[str, QuestaoPreparada],
        rotulos: Mapping[str, RotuloGold],
    ) -> Path:
        """Grava o caderno.

        Args:
            destino: Caminho do ``.md``.
            amostra: Itens na ordem de rotulagem.
            questoes: Questões preparadas por ID.
            rotulos: Rótulos já gravados por ID (para marcar o que falta).

        Returns:
            Caminho gravado.
        """
        feitas: int = sum(1 for item in amostra if item.id in rotulos and rotulos[item.id].preenchido)
        linhas: list[str] = [
            "# Gold set: caderno de rotulagem",
            "",
            f"{len(amostra)} questões na ordem de rotulagem; {feitas} já rotuladas (marcadas com [x]).",
            "",
            "- Rotule pelo texto abaixo e pela árvore (`dados/preparados/arvore_enxuta.txt`).",
            "- Fontes permitidas: lei (Planalto), árvore e cartões de tema. Um LLM pode explicar o conteúdo",
            "  jurídico, mas nunca ser perguntado sobre o tema; se usar, registre na observação.",
            "- `tema_id`: o nó mais específico em que há segurança. Na dúvida entre subtemas, o pai, com os",
            "  filhos plausíveis em `alternativos`.",
            "- Rotulagem interativa: `uv run python executar_rotulagem.py`.",
            "",
        ]
        item: ItemAmostra
        for item in amostra:
            marca: str = "[x]" if item.id in rotulos and rotulos[item.id].preenchido else "[ ]"
            linhas.extend(
                [
                    f"## {item.ordem}. {item.id} {marca}",
                    "",
                    "```text",
                    questoes[item.id].texto_canonico,
                    "```",
                    "",
                ]
            )
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text("\n".join(linhas), encoding="utf-8")
        return destino
