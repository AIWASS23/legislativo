"""Montagem das requisições com checagem do limite de cada provedor antes de chamar (ADR-008, regra 3)."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import ClassVar

from vicio_ia.configuracao import ParametrosLLM
from vicio_ia.llm.contratos import ErroProvedor, RequisicaoLLM


class ErroOrcamentoPrompt(ErroProvedor):
    """O prompt não cabe no limite do provedor escolhido; nada é truncado."""


class MontadorPrompt:
    """Cria :class:`RequisicaoLLM` e falha antes de chamar se o prompt não couber no provedor.

    Limites:

    * ``gemini-agy``: prompt inteiro (instruções + tarefa) e schema como argumento de linha de comando;
    * ``claude-cli``: o schema como argumento (o prompt de sistema vai por arquivo);
    * ``ollama``: tokens estimados do prompt mais a saída dentro do contexto (``num_ctx``).
    """

    FOLGA_BYTES: ClassVar[int] = 512

    def __init__(self, parametros: ParametrosLLM, chars_por_token_local: float) -> None:
        """Guarda os limites.

        Args:
            parametros: Parâmetros de LLM (limite de argumento e contexto do Ollama).
            chars_por_token_local: Caracteres por token usados na estimativa do modelo local
                (conservador: menos caracteres por token que o padrão).
        """
        self._max_bytes: int = parametros.max_bytes_argumento_cli
        self._contexto_local: int = parametros.contexto_necessario_tokens
        self._chars_por_token: float = chars_por_token_local

    def requisicao(
        self,
        provedor: str,
        sistema: str,
        usuario: str,
        schema: Mapping[str, object],
        nome_schema: str,
        max_tokens: int,
    ) -> RequisicaoLLM:
        """Monta a requisição, conferindo o limite do provedor.

        Args:
            provedor: Provedor que vai receber a chamada.
            sistema: Prompt de sistema.
            usuario: Tarefa (a questão).
            schema: JSON Schema da resposta.
            nome_schema: Nome do schema.
            max_tokens: Limite de saída.

        Returns:
            Requisição pronta.

        Raises:
            ErroOrcamentoPrompt: Se o prompt passar do limite do provedor.
        """
        bytes_schema: int = len(json.dumps(dict(schema), ensure_ascii=False).encode("utf-8"))
        if provedor in ("gemini-agy", "claude-cli") and bytes_schema > self._max_bytes:
            raise ErroOrcamentoPrompt(f"{provedor}: schema com {bytes_schema:,} bytes passa de {self._max_bytes:,}")
        if provedor == "gemini-agy":
            total: int = len(sistema.encode("utf-8")) + len(usuario.encode("utf-8")) + self.FOLGA_BYTES
            if total > self._max_bytes:
                raise ErroOrcamentoPrompt(f"gemini-agy: prompt com {total:,} bytes passa de {self._max_bytes:,}")
        if provedor == "ollama":
            tokens: int = round((len(sistema) + len(usuario)) / self._chars_por_token) + max_tokens
            if tokens > self._contexto_local:
                raise ErroOrcamentoPrompt(
                    f"ollama: ~{tokens:,} tokens (prompt + saída) passam do contexto de {self._contexto_local:,}"
                )
        return RequisicaoLLM(
            sistema=sistema, usuario=usuario, schema=schema, nome_schema=nome_schema, max_tokens=max_tokens
        )
