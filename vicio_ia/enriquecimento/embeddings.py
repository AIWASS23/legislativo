"""Geração de embeddings com cache por conteúdo (ADR-021).

Cada vetor fica guardado em ``runs/embeddings/<modelo>/`` sob o SHA-256 do digest do modelo, da janela de
contexto e do texto com o prefixo. Rodar de novo só calcula os textos novos ou alterados (um documento de tema
revisado, por exemplo). O cache não é versionado; o artefato versionado é a exportação do modelo escolhido
em ``dados/conhecimento/embeddings/``.
"""

from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Sequence
from pathlib import Path

import numpy as np

from vicio_ia.configuracao import ModeloEmbedding
from vicio_ia.estatistica import Matriz
from vicio_ia.llm.embeddings import ProvedorEmbedding, RespostaEmbedding
from vicio_ia.sistema.vetores import ArquivoVetores


class CacheEmbeddings:
    """Vetores já calculados de um modelo, por chave de conteúdo."""

    def __init__(self, pasta: Path) -> None:
        """Carrega o cache da pasta, se existir.

        Args:
            pasta: ``runs/embeddings/<modelo>``.
        """
        self._pasta: Path = pasta
        self._chaves: list[str] = []
        self._vetores: Matriz = np.zeros((0, 0), dtype=np.float64)
        arquivo_chaves: Path = pasta / "chaves.json"
        if arquivo_chaves.is_file():
            bruto: object = json.loads(arquivo_chaves.read_text(encoding="utf-8"))
            self._chaves = [str(c) for c in bruto] if isinstance(bruto, list) else []
            self._vetores = np.asarray(np.load(pasta / "vetores.npy", allow_pickle=False), dtype=np.float64)
        self._posicao: dict[str, int] = {c: k for k, c in enumerate(self._chaves)}

    def __contains__(self, chave: object) -> bool:
        """Diz se a chave já tem vetor.

        Args:
            chave: Chave de conteúdo.

        Returns:
            ``True`` se houver vetor.
        """
        return chave in self._posicao

    def vetor(self, chave: str) -> Matriz:
        """Vetor de uma chave.

        Args:
            chave: Chave de conteúdo.

        Returns:
            Vetor.
        """
        return np.asarray(self._vetores[self._posicao[chave]], dtype=np.float64)

    def acrescentar(self, chaves: Sequence[str], vetores: Matriz) -> None:
        """Acrescenta vetores novos e regrava o cache.

        Args:
            chaves: Chaves novas.
            vetores: Um vetor por chave.
        """
        if not chaves:
            return
        base: Matriz = vetores if self._vetores.size == 0 else np.vstack([self._vetores, vetores])
        self._vetores = base
        chave: str
        for chave in chaves:
            self._posicao[chave] = len(self._chaves)
            self._chaves.append(chave)
        self._pasta.mkdir(parents=True, exist_ok=True)
        np.save(self._pasta / "vetores.npy", self._vetores.astype(np.float32), allow_pickle=False)
        (self._pasta / "chaves.json").write_text(json.dumps(self._chaves) + "\n", encoding="utf-8")


class GeradorEmbeddings:
    """Gera os vetores de um modelo, em lotes, consultando o cache antes."""

    def __init__(self, provedor: ProvedorEmbedding, modelo: ModeloEmbedding, pasta_cache: Path, lote: int) -> None:
        """Prepara o gerador e lê o digest do modelo.

        Args:
            provedor: Provedor de embedding.
            modelo: Modelo e prefixos.
            pasta_cache: ``runs/embeddings``.
            lote: Textos por chamada.
        """
        self._provedor: ProvedorEmbedding = provedor
        self._modelo: ModeloEmbedding = modelo
        self._lote: int = lote
        self.digest: str = provedor.digest(modelo.nome)
        self._cache: CacheEmbeddings = CacheEmbeddings(pasta_cache / self.pasta(modelo.nome))
        self.calculados: int = 0
        self.segundos: float = 0.0

    @staticmethod
    def pasta(nome_modelo: str) -> str:
        """Nome de pasta seguro para um modelo.

        Args:
            nome_modelo: Nome no provedor (``qwen3-embedding:0.6b``).

        Returns:
            Nome sem ``:`` nem ``/``.
        """
        return nome_modelo.replace(":", "_").replace("/", "_")

    def textos_com_prefixo(self, textos: Sequence[str], consulta: bool) -> list[str]:
        """Aplica o prefixo do modelo.

        Args:
            textos: Textos.
            consulta: ``True`` para questões e alternativas; ``False`` para documentos de tema.

        Returns:
            Textos com o prefixo.
        """
        prefixo: str = self._modelo.prefixo_consulta if consulta else self._modelo.prefixo_documento
        return [prefixo + t for t in textos]

    def vetores(self, textos: Sequence[str], consulta: bool) -> Matriz:
        """Vetores normalizados dos textos, na ordem da entrada.

        Args:
            textos: Textos.
            consulta: ``True`` para questões e alternativas; ``False`` para documentos de tema.

        Returns:
            Matriz com uma linha por texto, norma 1.
        """
        entradas: list[str] = self.textos_com_prefixo(textos, consulta)
        chaves: list[str] = [self._chave(t) for t in entradas]
        faltando: list[int] = [k for k, c in enumerate(chaves) if c not in self._cache]
        unicos: dict[str, int] = {}
        indice: int
        for indice in faltando:
            unicos.setdefault(chaves[indice], indice)
        pendentes: list[int] = list(unicos.values())
        inicio: int
        for inicio in range(0, len(pendentes), self._lote):
            bloco: list[int] = pendentes[inicio : inicio + self._lote]
            relogio: float = time.perf_counter()
            resposta: RespostaEmbedding = self._provedor.embutir(
                [entradas[k] for k in bloco], self._modelo.nome, self._modelo.contexto_tokens
            )
            self.segundos += time.perf_counter() - relogio
            self._cache.acrescentar([chaves[k] for k in bloco], np.asarray(resposta.vetores, dtype=np.float64))
            self.calculados += len(bloco)
        return ArquivoVetores.normalizar(np.asarray([self._cache.vetor(c) for c in chaves], dtype=np.float64))

    def _chave(self, texto: str) -> str:
        """Chave de conteúdo: digest do modelo, janela de contexto e texto com prefixo.

        Args:
            texto: Texto com prefixo.

        Returns:
            SHA-256 em hexadecimal.
        """
        semente: str = f"{self.digest}\x00{self._modelo.contexto_tokens}\x00{texto}"
        return hashlib.sha256(semente.encode("utf-8")).hexdigest()
