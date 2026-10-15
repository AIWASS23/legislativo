"""Base dos provedores que usam CLIs de agente com assinatura (``claude``, ``agy``)."""

from __future__ import annotations

import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import ClassVar

from vicio_ia.llm.contratos import ErroProvedor, ProvedorLLM


class ProvedorCLI(ProvedorLLM):
    """Executa uma CLI de agente em modo não interativo e lê a resposta JSON.

    Cada chamada roda numa pasta temporária vazia (o agente não vê o projeto) e sem
    ferramentas habilitadas quando a CLI permite. O prompt nunca vai para o log.
    """

    executavel: ClassVar[str]

    def __init__(self, timeout_segundos: int, max_bytes_argumento: int) -> None:
        """Configura os limites da chamada.

        Args:
            timeout_segundos: Tempo máximo por chamada.
            max_bytes_argumento: Tamanho máximo de um texto passado como argumento de linha de comando.
        """
        self._timeout: int = timeout_segundos
        self._max_bytes: int = max_bytes_argumento

    def disponivel(self) -> bool:
        """Indica se o executável da CLI está no PATH.

        Returns:
            ``True`` se a CLI existe.
        """
        return shutil.which(self.executavel) is not None

    def checar_tamanho(self, texto: str, descricao: str) -> None:
        """Garante que um texto cabe como argumento de linha de comando.

        Args:
            texto: Texto a passar.
            descricao: O que é o texto (para a mensagem).

        Raises:
            ErroProvedor: Se passar do limite.
        """
        tamanho: int = len(texto.encode("utf-8"))
        if tamanho > self._max_bytes:
            raise ErroProvedor(
                f"{self.nome}: {descricao} com {tamanho:,} bytes passa do limite de {self._max_bytes:,} "
                "para argumento de CLI; reduza o contexto (ex.: classificação hierárquica)"
            )

    def executar(self, comando: list[str], entrada: str | None, pasta: Path) -> tuple[dict[str, object], float]:
        """Roda a CLI e decodifica a saída JSON.

        Args:
            comando: Comando completo.
            entrada: Texto enviado pela entrada padrão (``None`` para nada).
            pasta: Pasta de trabalho (temporária e vazia).

        Returns:
            ``(objeto JSON da saída, latência em segundos)``.

        Raises:
            ErroProvedor: Se a CLI não existir, falhar, demorar demais ou não devolver JSON.
        """
        if not self.disponivel():
            raise ErroProvedor(f"{self.nome}: CLI `{self.executavel}` não encontrada no PATH")
        inicio: float = time.perf_counter()
        try:
            processo: subprocess.CompletedProcess[str] = subprocess.run(
                comando,
                input=entrada,
                cwd=pasta,
                capture_output=True,
                text=True,
                timeout=self._timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as erro:
            raise ErroProvedor(f"{self.nome}: tempo esgotado ({self._timeout}s)") from erro
        latencia: float = time.perf_counter() - inicio
        if processo.returncode != 0:
            detalhe: str = processo.stderr.strip()[:500] or processo.stdout.strip()[-500:]
            raise ErroProvedor(f"{self.nome}: saiu com código {processo.returncode}: {detalhe}")
        return self._ultimo_json(processo.stdout), latencia

    def _ultimo_json(self, saida: str) -> dict[str, object]:
        """Decodifica a saída: um objeto JSON inteiro ou o último objeto por linha.

        Args:
            saida: Saída padrão da CLI.

        Returns:
            Objeto JSON.

        Raises:
            ErroProvedor: Se não houver objeto JSON.
        """
        candidatos: list[str] = [saida.strip(), *reversed(saida.strip().splitlines())]
        candidato: str
        for candidato in candidatos:
            try:
                valor: object = json.loads(candidato)
            except ValueError:
                continue
            if isinstance(valor, dict):
                return {str(chave): item for chave, item in valor.items()}
        raise ErroProvedor(f"{self.nome}: saída da CLI não é JSON: {saida[:300]!r}")

    @staticmethod
    def inteiro(valor: object) -> int:
        """Converte um contador da saída em inteiro.

        Args:
            valor: Valor bruto.

        Returns:
            Inteiro (0 se ausente).
        """
        return valor if isinstance(valor, int) and not isinstance(valor, bool) else 0
