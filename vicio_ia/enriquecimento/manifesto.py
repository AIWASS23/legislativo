"""Manifesto de proveniência dos artefatos da fase de conhecimento (ADR-019).

Cada artefato gravado em ``dados/conhecimento/`` aparece no manifesto com o hash, a origem
(``manual``, ``regra``, ``llm+revisão``, ``llm (proposta, sem revisão)`` ou ``embedding``), o comando que
o gera e os detalhes (provedor, modelo, versão do prompt, revisão humana). O README mostra o manifesto
como a tabela "de onde veio cada artefato".
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class EntradaManifesto:
    """Proveniência de um artefato.

    Attributes:
        arquivo: Caminho relativo à raiz do projeto.
        sha256: Hash do conteúdo.
        origem: Como o artefato foi produzido.
        comando: Comando que o gera.
        detalhes: Provedor, modelo, versão do prompt, revisão humana etc.
        atualizado_em: Data e hora da última gravação.
    """

    arquivo: str
    sha256: str
    origem: str
    comando: str
    detalhes: dict[str, str]
    atualizado_em: str


class Manifesto:
    """Lê e atualiza ``dados/conhecimento/manifesto.json``."""

    def __init__(self, caminho: Path, raiz: Path) -> None:
        """Define o arquivo e a raiz usada nos caminhos relativos.

        Args:
            caminho: Arquivo do manifesto.
            raiz: Raiz do projeto.
        """
        self._caminho: Path = caminho
        self._raiz: Path = raiz

    def ler(self) -> dict[str, EntradaManifesto]:
        """Lê o manifesto.

        Returns:
            Entradas por caminho relativo (vazio se o arquivo não existir).
        """
        if not self._caminho.is_file():
            return {}
        bruto: object = json.loads(self._caminho.read_text(encoding="utf-8"))
        entradas: dict[str, EntradaManifesto] = {}
        if isinstance(bruto, dict):
            chave: object
            valor: object
            for chave, valor in bruto.items():
                if isinstance(valor, dict):
                    detalhes: object = valor.get("detalhes", {})
                    entradas[str(chave)] = EntradaManifesto(
                        arquivo=str(chave),
                        sha256=str(valor.get("sha256", "")),
                        origem=str(valor.get("origem", "")),
                        comando=str(valor.get("comando", "")),
                        detalhes={str(k): str(v) for k, v in detalhes.items()} if isinstance(detalhes, dict) else {},
                        atualizado_em=str(valor.get("atualizado_em", "")),
                    )
        return entradas

    @staticmethod
    def sha256(arquivo: Path) -> str:
        """Hash SHA-256 de um arquivo.

        Args:
            arquivo: Arquivo.

        Returns:
            Hash em hexadecimal.
        """
        return hashlib.sha256(arquivo.read_bytes()).hexdigest()

    def registrar(self, arquivo: Path, origem: str, comando: str, detalhes: Mapping[str, str]) -> EntradaManifesto:
        """Grava ou atualiza a entrada de um artefato.

        Args:
            arquivo: Artefato (já gravado).
            origem: Como foi produzido.
            comando: Comando que o gera.
            detalhes: Detalhes de proveniência.

        Returns:
            Entrada gravada.
        """
        relativo: str = arquivo.resolve().relative_to(self._raiz.resolve()).as_posix()
        entrada: EntradaManifesto = EntradaManifesto(
            arquivo=relativo,
            sha256=self.sha256(arquivo),
            origem=origem,
            comando=comando,
            detalhes=dict(sorted(detalhes.items())),
            atualizado_em=datetime.now().isoformat(timespec="seconds"),
        )
        entradas: dict[str, EntradaManifesto] = self.ler()
        entradas[relativo] = entrada
        self._caminho.parent.mkdir(parents=True, exist_ok=True)
        conteudo: dict[str, dict[str, object]] = {
            chave: {
                "sha256": e.sha256,
                "origem": e.origem,
                "comando": e.comando,
                "detalhes": e.detalhes,
                "atualizado_em": e.atualizado_em,
            }
            for chave, e in sorted(entradas.items())
        }
        self._caminho.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return entrada
