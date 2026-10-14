"""Provedor Claude via API da Anthropic (SDK ``anthropic``), cobrado por token."""

from __future__ import annotations

import time
from typing import ClassVar, Literal

import anthropic
from anthropic.types import Message, OutputConfigParam, TextBlock
from anthropic.types.beta import BetaMessage, BetaOutputConfigParam, BetaTextBlock

from vicio_ia.llm.contratos import ErroProvedor, ProvedorLLM, RequisicaoLLM, RespostaLLM, UsoTokens

type Esforco = Literal["low", "medium", "high", "xhigh", "max"]
"""Níveis aceitos em ``output_config.effort``."""


class ProvedorClaudeAPI(ProvedorLLM):
    """Chama a Messages API com saída estruturada (``output_config.format``) e esforço configurável.

    Nos modelos que aceitam, liga o *fallback* do servidor para recusas (``fallbacks="default"``,
    beta ``server-side-fallback-2026-07-01``). As credenciais seguem a ordem do SDK:
    ``ANTHROPIC_API_KEY``, ``ANTHROPIC_AUTH_TOKEN`` ou o perfil do ``ant auth login``.
    """

    nome: ClassVar[str] = "claude-api"
    descricao: ClassVar[str] = "Claude via API da Anthropic (cobrado por token)"
    MODELOS_COM_FALLBACK: ClassVar[frozenset[str]] = frozenset(
        {"claude-fable-5-1", "claude-opus-5-5", "claude-opus-5", "claude-sonnet-5-5"}
    )
    BETA_FALLBACK: ClassVar[str] = "server-side-fallback-2026-07-01"
    ESFORCOS: ClassVar[dict[str, Esforco]] = {
        "low": "low",
        "medium": "medium",
        "high": "high",
        "xhigh": "xhigh",
        "max": "max",
    }

    def __init__(self, esforco: str, timeout_segundos: int) -> None:
        """Configura o cliente.

        Args:
            esforco: ``effort`` (``low``, ``medium``, ``high``, ``xhigh`` ou ``max``).
            timeout_segundos: Tempo máximo por chamada.

        Raises:
            ErroProvedor: Se o esforço for inválido.
        """
        if esforco not in self.ESFORCOS:
            raise ErroProvedor(f"claude-api: esforço inválido {esforco!r} (opções: {', '.join(self.ESFORCOS)})")
        self._esforco: Esforco = self.ESFORCOS[esforco]
        self._timeout: int = timeout_segundos

    def gerar(self, requisicao: RequisicaoLLM, modelo: str) -> RespostaLLM:
        """Faz uma chamada à API.

        Args:
            requisicao: Conteúdo e schema.
            modelo: ID do modelo (``claude-opus-5-5``).

        Returns:
            Resposta padronizada (sem custo: calculado à parte com a tabela de preços).

        Raises:
            ErroProvedor: Sem credencial, erro de API, recusa ou resposta sem o JSON esperado.
        """
        inicio: float = time.perf_counter()
        try:
            cliente: anthropic.Anthropic = anthropic.Anthropic(timeout=float(self._timeout))
            if modelo in self.MODELOS_COM_FALLBACK:
                resposta: RespostaLLM = self._gerar_beta(cliente, requisicao, modelo, inicio)
            else:
                resposta = self._gerar_padrao(cliente, requisicao, modelo, inicio)
        except anthropic.AuthenticationError as erro:
            raise ErroProvedor("claude-api: credencial inválida ou ausente (ANTHROPIC_API_KEY)") from erro
        except anthropic.APIError as erro:
            raise ErroProvedor(f"claude-api: erro de API: {erro}") from erro
        except TypeError as erro:
            raise ErroProvedor(f"claude-api: credencial ausente ({erro})") from erro
        if resposta.motivo_parada == "refusal":
            raise ErroProvedor("claude-api: o modelo recusou a requisição (stop_reason=refusal)")
        self.exigir_dados(requisicao, resposta.dados, resposta.texto)
        return resposta

    def _gerar_padrao(
        self, cliente: anthropic.Anthropic, requisicao: RequisicaoLLM, modelo: str, inicio: float
    ) -> RespostaLLM:
        """Chamada pela API estável (modelos sem fallback de servidor, como o Haiku).

        Args:
            cliente: Cliente do SDK.
            requisicao: Conteúdo e schema.
            modelo: ID do modelo.
            inicio: Instante de início, para a latência.

        Returns:
            Resposta padronizada.
        """
        configuracao: OutputConfigParam = {"effort": self._esforco}
        if requisicao.schema is not None:
            configuracao["format"] = {"type": "json_schema", "schema": dict(requisicao.schema)}
        mensagem: Message = cliente.messages.create(
            model=modelo,
            max_tokens=requisicao.max_tokens,
            system=requisicao.sistema,
            messages=[{"role": "user", "content": requisicao.usuario}],
            output_config=configuracao,
        )
        texto: str = next((bloco.text for bloco in mensagem.content if isinstance(bloco, TextBlock)), "")
        return RespostaLLM(
            provedor=self.nome,
            modelo=mensagem.model,
            texto=texto,
            dados=self.extrair_json(texto) if requisicao.schema is not None else None,
            uso=UsoTokens(
                entrada=mensagem.usage.input_tokens,
                saida=mensagem.usage.output_tokens,
                cache_lido=mensagem.usage.cache_read_input_tokens or 0,
                cache_escrito=mensagem.usage.cache_creation_input_tokens or 0,
            ),
            latencia_s=time.perf_counter() - inicio,
            motivo_parada=str(mensagem.stop_reason),
        )

    def _gerar_beta(
        self, cliente: anthropic.Anthropic, requisicao: RequisicaoLLM, modelo: str, inicio: float
    ) -> RespostaLLM:
        """Chamada pela API beta com ``fallbacks="default"`` (recusa vira resposta de outro modelo).

        Args:
            cliente: Cliente do SDK.
            requisicao: Conteúdo e schema.
            modelo: ID do modelo.
            inicio: Instante de início, para a latência.

        Returns:
            Resposta padronizada (``modelo`` é o que de fato respondeu).
        """
        configuracao: BetaOutputConfigParam = {"effort": self._esforco}
        if requisicao.schema is not None:
            configuracao["format"] = {"type": "json_schema", "schema": dict(requisicao.schema)}
        mensagem: BetaMessage = cliente.beta.messages.create(
            model=modelo,
            max_tokens=requisicao.max_tokens,
            system=requisicao.sistema,
            messages=[{"role": "user", "content": requisicao.usuario}],
            output_config=configuracao,
            betas=[self.BETA_FALLBACK],
            fallbacks="default",
        )
        texto: str = next((bloco.text for bloco in mensagem.content if isinstance(bloco, BetaTextBlock)), "")
        return RespostaLLM(
            provedor=self.nome,
            modelo=mensagem.model,
            texto=texto,
            dados=self.extrair_json(texto) if requisicao.schema is not None else None,
            uso=UsoTokens(
                entrada=mensagem.usage.input_tokens,
                saida=mensagem.usage.output_tokens,
                cache_lido=mensagem.usage.cache_read_input_tokens or 0,
                cache_escrito=mensagem.usage.cache_creation_input_tokens or 0,
            ),
            latencia_s=time.perf_counter() - inicio,
            motivo_parada=str(mensagem.stop_reason),
        )
