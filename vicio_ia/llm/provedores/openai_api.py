"""Provedor OpenAI (Chat Completions com JSON Schema); base também do Hugging Face."""

from __future__ import annotations

import time
from typing import ClassVar

import openai
from openai.types.chat import ChatCompletion

from vicio_ia.ambiente import CarregadorAmbiente
from vicio_ia.llm.contratos import ErroProvedor, ProvedorLLM, RequisicaoLLM, RespostaLLM, UsoTokens


class ProvedorOpenAI(ProvedorLLM):
    """Chama a API de Chat Completions da OpenAI com ``response_format`` em JSON Schema."""

    nome: ClassVar[str] = "openai"
    descricao: ClassVar[str] = "OpenAI via API (cobrado por token)"
    VARIAVEIS_CREDENCIAL: ClassVar[tuple[str, ...]] = ("OPENAI_API_KEY",)
    SCHEMA_ESTRITO: ClassVar[bool] = True
    USA_MAX_COMPLETION_TOKENS: ClassVar[bool] = True

    def __init__(self, ambiente: CarregadorAmbiente, timeout_segundos: int, url_base: str | None = None) -> None:
        """Configura o acesso.

        Args:
            ambiente: Leitor de credenciais.
            timeout_segundos: Tempo máximo por chamada.
            url_base: Endpoint alternativo compatível com a API da OpenAI (``None`` = OpenAI).
        """
        self._ambiente: CarregadorAmbiente = ambiente
        self._timeout: int = timeout_segundos
        self._url_base: str | None = url_base

    def credencial(self) -> str | None:
        """Busca a chave de API.

        Returns:
            A chave, ou ``None``.
        """
        return self._ambiente.valor(self.VARIAVEIS_CREDENCIAL)

    def gerar(self, requisicao: RequisicaoLLM, modelo: str) -> RespostaLLM:
        """Faz uma chamada.

        Args:
            requisicao: Conteúdo e schema.
            modelo: ID do modelo.

        Returns:
            Resposta padronizada (sem custo: calculado à parte com a tabela de preços).

        Raises:
            ErroProvedor: Sem credencial, erro de API, recusa ou resposta sem o JSON esperado.
        """
        chave: str | None = self.credencial()
        if not chave:
            raise ErroProvedor(f"{self.nome}: falta credencial ({' ou '.join(self.VARIAVEIS_CREDENCIAL)})")
        cliente: openai.OpenAI = openai.OpenAI(api_key=chave, base_url=self._url_base, timeout=float(self._timeout))
        formato: openai.types.shared_params.ResponseFormatJSONSchema | openai.types.shared_params.ResponseFormatText = (
            {
                "type": "json_schema",
                "json_schema": {
                    "name": requisicao.nome_schema,
                    "schema": dict(requisicao.schema),
                    "strict": self.SCHEMA_ESTRITO,
                },
            }
            if requisicao.schema is not None
            else {"type": "text"}
        )
        inicio: float = time.perf_counter()
        try:
            if self.USA_MAX_COMPLETION_TOKENS:
                resposta: ChatCompletion = cliente.chat.completions.create(
                    model=modelo,
                    messages=[
                        {"role": "system", "content": requisicao.sistema},
                        {"role": "user", "content": requisicao.usuario},
                    ],
                    response_format=formato,
                    max_completion_tokens=requisicao.max_tokens,
                )
            else:
                resposta = cliente.chat.completions.create(
                    model=modelo,
                    messages=[
                        {"role": "system", "content": requisicao.sistema},
                        {"role": "user", "content": requisicao.usuario},
                    ],
                    response_format=formato,
                    max_tokens=requisicao.max_tokens,
                    temperature=0,
                )
        except openai.AuthenticationError as erro:
            raise ErroProvedor(f"{self.nome}: credencial inválida") from erro
        except openai.APIError as erro:
            raise ErroProvedor(f"{self.nome}: erro de API: {erro}") from erro
        latencia: float = time.perf_counter() - inicio
        if not resposta.choices:
            raise ErroProvedor(f"{self.nome}: resposta sem escolhas")
        escolha: openai.types.chat.chat_completion.Choice = resposta.choices[0]
        if escolha.message.refusal:
            raise ErroProvedor(f"{self.nome}: o modelo recusou: {escolha.message.refusal[:200]}")
        texto: str = escolha.message.content or ""
        dados: dict[str, object] | None = self.extrair_json(texto) if requisicao.schema is not None else None
        self.exigir_dados(requisicao, dados, texto)
        uso: UsoTokens = (
            UsoTokens(entrada=resposta.usage.prompt_tokens, saida=resposta.usage.completion_tokens)
            if resposta.usage
            else UsoTokens()
        )
        return RespostaLLM(
            provedor=self.nome,
            modelo=resposta.model or modelo,
            texto=texto,
            dados=dados,
            uso=uso,
            latencia_s=latencia,
            motivo_parada=str(escolha.finish_reason),
        )
