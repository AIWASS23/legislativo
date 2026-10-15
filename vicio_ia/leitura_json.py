"""Leitura tipada de campos de objetos JSON (valores chegam como ``object`` e são conferidos aqui)."""

from __future__ import annotations

from collections.abc import Mapping


class ErroCampoJSON(Exception):
    """Campo ausente ou com tipo inesperado num objeto JSON."""


class CamposJSON:
    """Converte campos de um objeto JSON nos tipos esperados, falhando com mensagem clara."""

    def __init__(self, objeto: Mapping[str, object], origem: str) -> None:
        """Guarda o objeto e uma descrição de onde ele veio (para as mensagens de erro).

        Args:
            objeto: Objeto JSON já decodificado.
            origem: Descrição curta (ex.: ``"temas.json, nó 4703"``).
        """
        self._objeto: Mapping[str, object] = objeto
        self._origem: str = origem

    def _erro(self, chave: str, esperado: str) -> ErroCampoJSON:
        """Monta a exceção para um campo inválido.

        Args:
            chave: Nome do campo.
            esperado: Tipo esperado.

        Returns:
            Exceção com a mensagem.
        """
        return ErroCampoJSON(f"{self._origem}: campo {chave!r} deveria ser {esperado}")

    def texto(self, chave: str) -> str:
        """Lê um texto obrigatório.

        Args:
            chave: Nome do campo.

        Returns:
            O texto.
        """
        valor: object = self._objeto.get(chave)
        if not isinstance(valor, str):
            raise self._erro(chave, "texto")
        return valor

    def texto_opcional(self, chave: str) -> str | None:
        """Lê um texto que pode ser ``null``.

        Args:
            chave: Nome do campo.

        Returns:
            O texto, ou ``None``.
        """
        valor: object = self._objeto.get(chave)
        if valor is None:
            return None
        if not isinstance(valor, str):
            raise self._erro(chave, "texto ou null")
        return valor

    def inteiro(self, chave: str) -> int:
        """Lê um inteiro obrigatório.

        Args:
            chave: Nome do campo.

        Returns:
            O inteiro.
        """
        valor: object = self._objeto.get(chave)
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise self._erro(chave, "inteiro")
        return valor

    def inteiro_opcional(self, chave: str) -> int | None:
        """Lê um inteiro que pode ser ``null``.

        Args:
            chave: Nome do campo.

        Returns:
            O inteiro, ou ``None``.
        """
        valor: object = self._objeto.get(chave)
        if valor is None:
            return None
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise self._erro(chave, "inteiro ou null")
        return valor

    def booleano(self, chave: str) -> bool:
        """Lê um booleano obrigatório.

        Args:
            chave: Nome do campo.

        Returns:
            O booleano.
        """
        valor: object = self._objeto.get(chave)
        if not isinstance(valor, bool):
            raise self._erro(chave, "booleano")
        return valor

    def textos(self, chave: str) -> tuple[str, ...]:
        """Lê uma lista de textos.

        Args:
            chave: Nome do campo.

        Returns:
            Tupla de textos.
        """
        valor: object = self._objeto.get(chave)
        if not isinstance(valor, list) or not all(isinstance(item, str) for item in valor):
            raise self._erro(chave, "lista de textos")
        return tuple(str(item) for item in valor)

    def dicionario_textos(self, chave: str) -> dict[str, str]:
        """Lê um objeto ``texto -> texto``.

        Args:
            chave: Nome do campo.

        Returns:
            Dicionário.
        """
        valor: object = self._objeto.get(chave)
        if not isinstance(valor, dict) or not all(isinstance(item, str) for item in valor.values()):
            raise self._erro(chave, "objeto de textos")
        return {str(k): str(v) for k, v in valor.items()}

    def objeto(self, chave: str) -> dict[str, object]:
        """Lê um objeto aninhado.

        Args:
            chave: Nome do campo.

        Returns:
            Dicionário com as chaves como texto.
        """
        valor: object = self._objeto.get(chave)
        if not isinstance(valor, dict):
            raise self._erro(chave, "objeto")
        return {str(k): v for k, v in valor.items()}

    def objeto_opcional(self, chave: str) -> dict[str, object] | None:
        """Lê um objeto aninhado que pode ser ``null``.

        Args:
            chave: Nome do campo.

        Returns:
            Dicionário, ou ``None``.
        """
        if self._objeto.get(chave) is None:
            return None
        return self.objeto(chave)

    def numero(self, chave: str) -> float:
        """Lê um número obrigatório (inteiro ou real).

        Args:
            chave: Nome do campo.

        Returns:
            O número como ``float``.
        """
        valor: object = self._objeto.get(chave)
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            raise self._erro(chave, "número")
        return float(valor)

    def numero_opcional(self, chave: str) -> float | None:
        """Lê um número que pode ser ``null``.

        Args:
            chave: Nome do campo.

        Returns:
            O número, ou ``None``.
        """
        if self._objeto.get(chave) is None:
            return None
        return self.numero(chave)
