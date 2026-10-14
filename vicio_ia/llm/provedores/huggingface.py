"""Provedor Hugging Face Inference Providers (remoto), pelo roteador compatível com a API da OpenAI.

Modelos GGUF do Hub rodando localmente usam o provedor ``ollama`` com nomes ``hf.co/<usuario>/<repo>``.
"""

from __future__ import annotations

from typing import ClassVar

from vicio_ia.ambiente import CarregadorAmbiente
from vicio_ia.llm.provedores.openai_api import ProvedorOpenAI


class ProvedorHuggingFace(ProvedorOpenAI):
    """Chama modelos abertos hospedados pelos Inference Providers do Hugging Face.

    A credencial é o ``HF_TOKEN`` (ou o token salvo pelo ``hf auth login``). O schema não
    é exigido em modo estrito, porque o suporte varia entre os provedores parceiros.
    """

    nome: ClassVar[str] = "huggingface"
    descricao: ClassVar[str] = "Hugging Face Inference Providers (remoto, HF_TOKEN)"
    VARIAVEIS_CREDENCIAL: ClassVar[tuple[str, ...]] = ("HF_TOKEN", "HUGGING_FACE_HUB_TOKEN")
    SCHEMA_ESTRITO: ClassVar[bool] = False
    USA_MAX_COMPLETION_TOKENS: ClassVar[bool] = False

    def __init__(self, ambiente: CarregadorAmbiente, timeout_segundos: int, url_base: str) -> None:
        """Configura o acesso ao roteador.

        Args:
            ambiente: Leitor de credenciais.
            timeout_segundos: Tempo máximo por chamada.
            url_base: Endpoint do roteador (``https://router.huggingface.co/v1``).
        """
        super().__init__(ambiente, timeout_segundos, url_base)

    def credencial(self) -> str | None:
        """Busca o token no ambiente ou no arquivo do ``hf auth login``.

        Returns:
            O token, ou ``None``.
        """
        return self._ambiente.token_huggingface()
