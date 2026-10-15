"""JSON Schemas das respostas, com ``enum`` dos IDs permitidos em cada chamada (ADR-008)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from vicio_ia.preparacao.arvore_preparada import TemaPreparado


class FabricaSchemas:
    """Monta os schemas a partir da árvore preparada (só IDs publicáveis)."""

    NENHUM: ClassVar[str] = "nenhum"

    def __init__(self, temas: Sequence[TemaPreparado]) -> None:
        """Guarda os IDs publicáveis.

        Args:
            temas: Árvore preparada.
        """
        self._publicaveis: list[str] = sorted(tema.tema_id for tema in temas if tema.publicavel)

    @property
    def publicaveis(self) -> list[str]:
        """IDs publicáveis, em ordem."""
        return list(self._publicaveis)

    def completo(self, permitidos: Sequence[str]) -> dict[str, object]:
        """Schema dos classificadores A e B (etapa do tema).

        Args:
            permitidos: IDs aceitos em ``tema_id`` e ``segundo_id``.

        Returns:
            Schema.
        """
        ids: list[str] = list(permitidos)
        return self._objeto(
            {
                "nucleo": {"type": "string"},
                "tema_id": {"type": "string", "enum": ids},
                "segundo_id": {"type": "string", "enum": [*ids, ""]},
                "extras_ids": {"type": "array", "items": {"type": "string", "enum": self._publicaveis}},
                "multitema": {"type": "boolean"},
                "fora": {"type": "boolean"},
                "autoconfianca": {"type": "number"},
            }
        )

    def subtema(self, permitidos: Sequence[str]) -> dict[str, object]:
        """Schema da 2ª etapa do classificador B.

        Args:
            permitidos: O tema e os subtemas.

        Returns:
            Schema.
        """
        ids: list[str] = list(permitidos)
        return self._objeto(
            {
                "nucleo": {"type": "string"},
                "tema_id": {"type": "string", "enum": ids},
                "segundo_id": {"type": "string", "enum": [*ids, ""]},
                "autoconfianca": {"type": "number"},
            }
        )

    def simples(self) -> dict[str, object]:
        """Schema do voto barato.

        Returns:
            Schema.
        """
        return self._objeto({"nucleo": {"type": "string"}, "tema_id": {"type": "string", "enum": self._publicaveis}})

    def verificador(self, opcoes: Sequence[str]) -> dict[str, object]:
        """Schema do verificador contrastivo.

        Args:
            opcoes: IDs dos cartões mostrados.

        Returns:
            Schema.
        """
        return self._objeto(
            {
                "nucleo": {"type": "string"},
                "escolha_id": {"type": "string", "enum": [*opcoes, self.NENHUM]},
                "justificativa": {"type": "string"},
                "confianca": {"type": "number"},
            }
        )

    @staticmethod
    def _objeto(propriedades: dict[str, object]) -> dict[str, object]:
        """Envolve as propriedades num objeto com todos os campos obrigatórios.

        Args:
            propriedades: Campos, na ordem em que o modelo deve escrevê-los.

        Returns:
            Schema.
        """
        return {
            "type": "object",
            "properties": propriedades,
            "required": list(propriedades),
            "additionalProperties": False,
        }
