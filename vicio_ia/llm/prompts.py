"""Prompts versionados (``prompts/*.md``): a versão é o hash do arquivo e entra na chave do cache."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping
from pathlib import Path
from typing import ClassVar


class ErroPrompt(Exception):
    """Arquivo de prompt ausente ou com marcador sem valor."""


class ArquivoPrompt:
    """Um prompt com marcadores ``{{nome}}``, preenchidos na hora da chamada.

    Marcadores com chaves duplas não colidem com exemplos de JSON dentro do prompt.
    """

    _RE_MARCADOR: ClassVar[re.Pattern[str]] = re.compile(r"\{\{([a-z_]+)\}\}")

    def __init__(self, caminho: Path) -> None:
        """Lê o arquivo.

        Args:
            caminho: ``prompts/<nome>.md``.

        Raises:
            ErroPrompt: Se o arquivo não existir.
        """
        if not caminho.is_file():
            raise ErroPrompt(f"prompt ausente: {caminho}")
        self._nome: str = caminho.stem
        self._texto: str = caminho.read_text(encoding="utf-8")
        self._versao: str = f"{self._nome}@{hashlib.sha256(self._texto.encode('utf-8')).hexdigest()[:12]}"

    @property
    def nome(self) -> str:
        """Nome do prompt (nome do arquivo sem extensão)."""
        return self._nome

    @property
    def versao(self) -> str:
        """``nome@hash`` do conteúdo do arquivo."""
        return self._versao

    @property
    def marcadores(self) -> frozenset[str]:
        """Marcadores presentes no texto."""
        return frozenset(self._RE_MARCADOR.findall(self._texto))

    def preencher(self, valores: Mapping[str, str]) -> str:
        """Substitui os marcadores.

        Args:
            valores: ``marcador -> texto``.

        Returns:
            Prompt preenchido.

        Raises:
            ErroPrompt: Se faltar valor para algum marcador ou sobrar valor sem marcador.
        """
        faltando: list[str] = sorted(self.marcadores - set(valores))
        sobrando: list[str] = sorted(set(valores) - self.marcadores)
        if faltando or sobrando:
            raise ErroPrompt(f"{self._nome}: marcadores sem valor {faltando}; valores sem marcador {sobrando}")
        return self._RE_MARCADOR.sub(lambda achado: valores[achado.group(1)], self._texto)
