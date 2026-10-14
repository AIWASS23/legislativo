"""Contrato comum dos provedores de LLM: requisição, resposta, uso de tokens e erros."""

from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import ClassVar


class ErroProvedor(Exception):
    """Falha ao chamar um provedor (indisponível, credencial ausente, resposta inválida, recusa)."""


@dataclass(frozen=True)
class RequisicaoLLM:
    """Uma chamada a um modelo.

    Attributes:
        sistema: Instruções de sistema (papel, regras, árvore de temas).
        usuario: Conteúdo da tarefa (a questão).
        schema: JSON Schema da resposta; ``None`` para texto livre.
        nome_schema: Nome do schema (exigido por alguns provedores).
        max_tokens: Limite de tokens de saída.
    """

    sistema: str
    usuario: str
    schema: Mapping[str, object] | None = None
    nome_schema: str = "resposta"
    max_tokens: int = 4096


@dataclass(frozen=True)
class UsoTokens:
    """Tokens consumidos numa chamada.

    Attributes:
        entrada: Tokens de entrada sem cache.
        saida: Tokens de saída.
        cache_lido: Tokens de entrada servidos do cache de prompt.
        cache_escrito: Tokens de entrada gravados no cache de prompt.
        raciocinio: Tokens de raciocínio (quando o provedor informa à parte).
    """

    entrada: int = 0
    saida: int = 0
    cache_lido: int = 0
    cache_escrito: int = 0
    raciocinio: int = 0


@dataclass(frozen=True)
class RespostaLLM:
    """Resultado de uma chamada.

    Attributes:
        provedor: Nome do provedor.
        modelo: Modelo que respondeu.
        texto: Texto bruto da resposta.
        dados: Resposta estruturada (JSON decodificado), quando houve schema.
        uso: Tokens consumidos.
        latencia_s: Tempo da chamada em segundos.
        motivo_parada: Motivo de parada informado pelo provedor.
        custo_usd: Custo informado pelo provedor (nas CLIs, equivalente de lista); ``None`` se não informado.
        extras: Metadados adicionais do provedor (sem segredos).
    """

    provedor: str
    modelo: str
    texto: str
    dados: dict[str, object] | None
    uso: UsoTokens
    latencia_s: float
    motivo_parada: str
    custo_usd: float | None = None
    extras: dict[str, object] = field(default_factory=dict)


class ProvedorLLM(ABC):
    """Contrato de um provedor de LLM.

    Cada provedor sabe chamar um tipo de serviço e devolve sempre :class:`RespostaLLM`,
    para que classificadores e verificador não dependam de qual modelo está por trás.
    """

    nome: ClassVar[str]
    descricao: ClassVar[str]
    _RE_OBJETO_JSON: ClassVar[re.Pattern[str]] = re.compile(r"\{.*\}", re.DOTALL)

    @abstractmethod
    def gerar(self, requisicao: RequisicaoLLM, modelo: str) -> RespostaLLM:
        """Faz uma chamada ao modelo.

        Args:
            requisicao: Conteúdo e formato esperado.
            modelo: Identificador do modelo no provedor.

        Returns:
            Resposta padronizada.

        Raises:
            ErroProvedor: Se a chamada falhar ou a resposta não respeitar o schema.
        """

    @classmethod
    def extrair_json(cls, texto: str) -> dict[str, object] | None:
        """Decodifica um objeto JSON de um texto, tolerando texto em volta.

        Args:
            texto: Texto da resposta.

        Returns:
            Objeto decodificado, ou ``None`` se não houver um objeto JSON válido.
        """
        candidatos: list[str] = [texto.strip()]
        correspondencia: re.Match[str] | None = cls._RE_OBJETO_JSON.search(texto)
        if correspondencia is not None:
            candidatos.append(correspondencia.group(0))
        candidato: str
        for candidato in candidatos:
            try:
                valor: object = json.loads(candidato)
            except ValueError:
                continue
            if isinstance(valor, dict):
                return {str(chave): item for chave, item in valor.items()}
        return None

    def exigir_dados(self, requisicao: RequisicaoLLM, dados: dict[str, object] | None, texto: str) -> None:
        """Falha se havia schema e a resposta não trouxe um objeto JSON.

        Args:
            requisicao: Requisição original.
            dados: Dados decodificados.
            texto: Texto bruto (para a mensagem de erro).

        Raises:
            ErroProvedor: Se faltar a resposta estruturada.
        """
        if requisicao.schema is not None and dados is None:
            raise ErroProvedor(f"{self.nome}: resposta sem JSON válido: {texto[:300]!r}")
