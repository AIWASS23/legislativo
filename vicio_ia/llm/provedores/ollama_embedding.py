"""Provedor de embeddings do Ollama (``/api/embed``): modelos locais, sem custo e sem PyTorch no projeto."""

from __future__ import annotations

import time
from collections.abc import Sequence
from typing import ClassVar

from vicio_ia.llm.contratos import ErroProvedor
from vicio_ia.llm.embeddings import ProvedorEmbedding, RespostaEmbedding
from vicio_ia.llm.provedores.ollama import ServidorOllama


class ProvedorEmbeddingOllama(ProvedorEmbedding):
    """Gera embeddings com um modelo do Ollama local, em lotes."""

    nome: ClassVar[str] = "ollama"
    descricao: ClassVar[str] = "Embeddings locais via Ollama (GPU/CPU desta máquina)"

    def __init__(self, url: str, timeout_segundos: int) -> None:
        """Configura o acesso ao servidor.

        Args:
            url: Endereço do Ollama.
            timeout_segundos: Tempo máximo por lote.
        """
        self._servidor: ServidorOllama = ServidorOllama(url)
        self._timeout: int = timeout_segundos

    def embutir(self, textos: Sequence[str], modelo: str, contexto_tokens: int) -> RespostaEmbedding:
        """Gera os vetores de um lote.

        Args:
            textos: Textos do lote.
            modelo: Nome do modelo no Ollama.
            contexto_tokens: ``num_ctx`` da chamada; o excedente é truncado pelo servidor.

        Returns:
            Vetores na ordem dos textos.

        Raises:
            ErroProvedor: Se o servidor falhar ou devolver um número de vetores diferente do de textos.
        """
        corpo: dict[str, object] = {
            "model": modelo,
            "input": list(textos),
            "truncate": True,
            "options": {"num_ctx": contexto_tokens},
        }
        inicio: float = time.perf_counter()
        resposta: dict[str, object] = self._servidor.requisitar("/api/embed", corpo, self._timeout)
        latencia: float = time.perf_counter() - inicio
        brutos: object = resposta.get("embeddings")
        if not isinstance(brutos, list) or len(brutos) != len(textos):
            raise ErroProvedor(f"ollama: /api/embed devolveu {type(brutos).__name__} para {len(textos)} textos")
        vetores: list[tuple[float, ...]] = []
        bruto: object
        for bruto in brutos:
            if not isinstance(bruto, list) or not bruto:
                raise ErroProvedor("ollama: vetor vazio ou inválido em /api/embed")
            vetores.append(tuple(float(v) for v in bruto))
        tokens: object = resposta.get("prompt_eval_count")
        return RespostaEmbedding(
            provedor=self.nome,
            modelo=modelo,
            vetores=tuple(vetores),
            tokens=tokens if isinstance(tokens, int) and not isinstance(tokens, bool) else 0,
            latencia_s=latencia,
        )

    def digest(self, modelo: str) -> str:
        """Digest do modelo instalado, pela lista do servidor (``/api/tags``).

        Args:
            modelo: Nome do modelo (``bge-m3`` vale como ``bge-m3:latest``).

        Returns:
            Digest SHA-256 do modelo.

        Raises:
            ErroProvedor: Se o modelo não estiver instalado (``ollama pull <modelo>``).
        """
        nomes: set[str] = {modelo, modelo if ":" in modelo else f"{modelo}:latest"}
        lista: object = self._servidor.requisitar("/api/tags", None, 30).get("models", [])
        item: object
        for item in lista if isinstance(lista, list) else []:
            if isinstance(item, dict) and (item.get("name") in nomes or item.get("model") in nomes):
                return str(item.get("digest", ""))
        raise ErroProvedor(f"ollama: modelo {modelo!r} não instalado (rode: ollama pull {modelo})")
