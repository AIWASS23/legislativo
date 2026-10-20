"""Contrato comum dos provedores de embedding (ADR-021): textos entram, vetores saem.

Os embeddings só são gerados na fase de conhecimento. A fase de decisão lê os vetores gravados em
``dados/conhecimento/embeddings/`` e nunca cria um provedor (a trava da ADR-019 vale para a fábrica inteira).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class RespostaEmbedding:
    """Vetores de um lote de textos.

    Attributes:
        provedor: Nome do provedor.
        modelo: Modelo que gerou os vetores.
        vetores: Um vetor por texto, na ordem da entrada.
        tokens: Tokens de entrada processados (quando o provedor informa).
        latencia_s: Tempo da chamada em segundos.
    """

    provedor: str
    modelo: str
    vetores: tuple[tuple[float, ...], ...]
    tokens: int
    latencia_s: float


class ProvedorEmbedding(ABC):
    """Contrato de um provedor de embedding."""

    nome: ClassVar[str]
    descricao: ClassVar[str]

    @abstractmethod
    def embutir(self, textos: Sequence[str], modelo: str, contexto_tokens: int) -> RespostaEmbedding:
        """Gera os vetores de um lote.

        Args:
            textos: Textos já com o prefixo do modelo, se houver.
            modelo: Identificador do modelo no provedor.
            contexto_tokens: Janela de contexto (o texto além dela é truncado).

        Returns:
            Vetores na ordem dos textos.

        Raises:
            ErroProvedor: Se a chamada falhar ou a resposta vier incompleta.
        """

    @abstractmethod
    def digest(self, modelo: str) -> str:
        """Identificação exata dos pesos do modelo, para o manifesto e para a chave do cache.

        Args:
            modelo: Identificador do modelo.

        Returns:
            Digest (ou versão) do modelo.

        Raises:
            ErroProvedor: Se o modelo não estiver disponível.
        """
