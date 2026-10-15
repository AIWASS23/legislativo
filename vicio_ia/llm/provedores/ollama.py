"""Provedor Ollama: modelos locais (inclusive GGUF do Hugging Face via ``hf.co/...``)."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from http.client import HTTPResponse
from typing import ClassVar

from vicio_ia.llm.contratos import ErroProvedor, ProvedorLLM, RequisicaoLLM, RespostaLLM, UsoTokens


class ProvedorOllama(ProvedorLLM):
    """Chama o servidor Ollama local pela API HTTP (``/api/chat``), sem dependências externas.

    A saída estruturada usa o campo ``format`` com o JSON Schema. O contexto (``num_ctx``)
    é fixado pela configuração, porque define a memória usada na GPU.
    """

    nome: ClassVar[str] = "ollama"
    descricao: ClassVar[str] = "Modelos locais via Ollama (GPU/CPU desta máquina)"

    def __init__(self, url: str, contexto_tokens: int, pensar: bool, timeout_segundos: int) -> None:
        """Configura o acesso ao servidor.

        Args:
            url: Endereço do Ollama (``http://localhost:11434``).
            contexto_tokens: ``num_ctx`` usado em todas as chamadas.
            pensar: Liga o raciocínio nos modelos que o suportam.
            timeout_segundos: Tempo máximo por chamada.
        """
        self._url: str = url.rstrip("/")
        self._contexto: int = contexto_tokens
        self._pensar: bool = pensar
        self._timeout: int = timeout_segundos
        self._capacidades: dict[str, tuple[str, ...]] = {}

    def parametros_cache(self) -> dict[str, object]:
        """Contexto e raciocínio mudam a resposta do modelo local.

        Returns:
            ``{"num_ctx": ..., "pensar": ...}``.
        """
        return {"num_ctx": self._contexto, "pensar": self._pensar}

    def gerar(self, requisicao: RequisicaoLLM, modelo: str) -> RespostaLLM:
        """Faz uma chamada ao modelo local.

        Args:
            requisicao: Conteúdo e schema.
            modelo: Nome do modelo no Ollama.

        Returns:
            Resposta padronizada.

        Raises:
            ErroProvedor: Se o servidor falhar ou a resposta não tiver o JSON esperado.
        """
        corpo: dict[str, object] = {
            "model": modelo,
            "stream": False,
            "messages": [
                {"role": "system", "content": requisicao.sistema},
                {"role": "user", "content": requisicao.usuario},
            ],
            "options": {"temperature": 0, "num_ctx": self._contexto, "num_predict": requisicao.max_tokens},
        }
        if requisicao.schema is not None:
            corpo["format"] = dict(requisicao.schema)
        if "thinking" in self._capacidades_de(modelo):
            corpo["think"] = self._pensar
        inicio: float = time.perf_counter()
        resposta: dict[str, object] = self._post("/api/chat", corpo, self._timeout)
        latencia: float = time.perf_counter() - inicio
        mensagem: object = resposta.get("message", {})
        texto: str = str(mensagem.get("content", "")) if isinstance(mensagem, dict) else ""
        dados: dict[str, object] | None = self.extrair_json(texto) if requisicao.schema is not None else None
        self.exigir_dados(requisicao, dados, texto)
        return RespostaLLM(
            provedor=self.nome,
            modelo=modelo,
            texto=texto,
            dados=dados,
            uso=UsoTokens(
                entrada=self._inteiro(resposta.get("prompt_eval_count")),
                saida=self._inteiro(resposta.get("eval_count")),
            ),
            latencia_s=latencia,
            motivo_parada=str(resposta.get("done_reason", "")),
            custo_usd=0.0,
        )

    def _capacidades_de(self, modelo: str) -> tuple[str, ...]:
        """Consulta (uma vez por modelo) as capacidades declaradas pelo Ollama.

        Args:
            modelo: Nome do modelo.

        Returns:
            Capacidades (``completion``, ``thinking``...).
        """
        if modelo not in self._capacidades:
            detalhes: dict[str, object] = self._post("/api/show", {"model": modelo}, 30)
            capacidades: object = detalhes.get("capabilities", [])
            self._capacidades[modelo] = tuple(str(c) for c in capacidades) if isinstance(capacidades, list) else ()
        return self._capacidades[modelo]

    def _post(self, caminho: str, corpo: dict[str, object], timeout: float) -> dict[str, object]:
        """Faz um POST JSON ao Ollama.

        Args:
            caminho: Caminho da API.
            corpo: Corpo da requisição.
            timeout: Tempo máximo em segundos.

        Returns:
            Resposta decodificada.

        Raises:
            ErroProvedor: Se o servidor não responder ou devolver erro.
        """
        requisicao: urllib.request.Request = urllib.request.Request(
            self._url + caminho, data=json.dumps(corpo).encode("utf-8"), headers={"Content-Type": "application/json"}
        )
        resposta: HTTPResponse
        try:
            with urllib.request.urlopen(requisicao, timeout=timeout) as resposta:
                valor: object = json.loads(resposta.read().decode("utf-8"))
        except urllib.error.HTTPError as erro:
            detalhe: str = erro.read().decode("utf-8", errors="replace")[:300]
            raise ErroProvedor(f"ollama: HTTP {erro.code} em {caminho}: {detalhe}") from erro
        except (urllib.error.URLError, OSError, ValueError) as erro:
            raise ErroProvedor(f"ollama: servidor indisponível em {self._url} ({erro})") from erro
        if not isinstance(valor, dict):
            raise ErroProvedor(f"ollama: resposta inesperada em {caminho}")
        return {str(chave): item for chave, item in valor.items()}

    @staticmethod
    def _inteiro(valor: object) -> int:
        """Converte um contador da resposta em inteiro.

        Args:
            valor: Valor bruto.

        Returns:
            Inteiro (0 se ausente).
        """
        return valor if isinstance(valor, int) and not isinstance(valor, bool) else 0
