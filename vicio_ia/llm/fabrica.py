"""Criação de provedores de LLM pelo nome."""

from __future__ import annotations

import os
from typing import ClassVar

from vicio_ia.ambiente import CarregadorAmbiente
from vicio_ia.configuracao import Caminhos, ParametrosLLM, ParametrosSistema
from vicio_ia.llm.contratos import ErroProvedor, ProvedorLLM
from vicio_ia.llm.provedores.claude_api import ProvedorClaudeAPI
from vicio_ia.llm.provedores.claude_cli import ProvedorClaudeCLI
from vicio_ia.llm.provedores.codex_cli import ProvedorCodexCLI
from vicio_ia.llm.provedores.gemini_agy import ProvedorGeminiAgy
from vicio_ia.llm.provedores.huggingface import ProvedorHuggingFace
from vicio_ia.llm.provedores.ollama import ProvedorOllama
from vicio_ia.llm.provedores.openai_api import ProvedorOpenAI


class FabricaProvedores:
    """Cria (e reaproveita) instâncias de provedores a partir do nome configurado."""

    NOMES: ClassVar[tuple[str, ...]] = (
        "ollama",
        "claude-api",
        "claude-cli",
        "gemini-agy",
        "codex-cli",
        "openai",
        "huggingface",
    )

    def __init__(self, caminhos: Caminhos, parametros: ParametrosLLM) -> None:
        """Recebe a configuração e carrega o ``.env``.

        Args:
            caminhos: Caminhos do projeto.
            parametros: Parâmetros de LLM.

        Raises:
            ErroProvedor: Se a trava da fase de decisão estiver ativa (``VICIO_SEM_LLM=1``).
        """
        variavel: str = ParametrosSistema().variavel_sem_llm
        if os.environ.get(variavel) == "1":
            raise ErroProvedor(
                f"{variavel}=1: a fase de decisão da etapa 2 não pode chamar modelo de linguagem (ADR-019)"
            )
        self._parametros: ParametrosLLM = parametros
        self._ambiente: CarregadorAmbiente = CarregadorAmbiente(caminhos.env)
        self._ambiente.carregar_env()
        self._criados: dict[str, ProvedorLLM] = {}

    def obter(self, nome: str) -> ProvedorLLM:
        """Devolve o provedor pedido, criando-o na primeira vez.

        Args:
            nome: Um de :attr:`NOMES`.

        Returns:
            Instância do provedor.

        Raises:
            ErroProvedor: Se o nome for desconhecido.
        """
        if nome not in self._criados:
            self._criados[nome] = self._criar(nome)
        return self._criados[nome]

    def _criar(self, nome: str) -> ProvedorLLM:
        """Instancia um provedor.

        Args:
            nome: Nome do provedor.

        Returns:
            Instância nova.

        Raises:
            ErroProvedor: Se o nome for desconhecido.
        """
        p: ParametrosLLM = self._parametros
        if nome == "ollama":
            return ProvedorOllama(p.ollama_url, p.contexto_necessario_tokens, p.ollama_pensar, p.timeout_segundos)
        if nome == "claude-api":
            return ProvedorClaudeAPI(p.claude_esforco, p.timeout_segundos)
        if nome == "claude-cli":
            return ProvedorClaudeCLI(p.timeout_segundos, p.max_bytes_argumento_cli, p.claude_cli_esforco)
        if nome == "gemini-agy":
            return ProvedorGeminiAgy(p.timeout_segundos, p.max_bytes_argumento_cli)
        if nome == "codex-cli":
            return ProvedorCodexCLI(p.timeout_segundos, p.max_bytes_argumento_cli, p.codex_esforco)
        if nome == "openai":
            return ProvedorOpenAI(self._ambiente, p.timeout_segundos)
        if nome == "huggingface":
            return ProvedorHuggingFace(self._ambiente, p.timeout_segundos, p.huggingface_url)
        raise ErroProvedor(f"provedor desconhecido: {nome!r} (opções: {', '.join(self.NOMES)})")
