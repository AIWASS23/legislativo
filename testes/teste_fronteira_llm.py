"""Fronteira entre o LLM e a decisão da etapa 2 (ADR-019): imports, caminhos proibidos e a trava."""

from __future__ import annotations

import ast
import socket
import unittest
from collections.abc import Callable
from pathlib import Path
from typing import ClassVar

from vicio_ia.configuracao import Caminhos, ParametrosLLM
from vicio_ia.llm.contratos import ErroProvedor
from vicio_ia.llm.fabrica import FabricaProvedores
from vicio_ia.sistema.trava import ErroTrava, TravaSemLLM


class TesteImportsDoSistema(unittest.TestCase):
    """Nenhum módulo da fase de decisão importa LLM, rede ou os votos da etapa 1."""

    PROIBIDOS: ClassVar[tuple[str, ...]] = (
        "vicio_ia.llm",
        "vicio_ia.classificacao",
        "vicio_ia.decisao",
        "anthropic",
        "openai",
        "requests",
        "httpx",
        "urllib",
        "http",
        "subprocess",
    )
    ATRIBUTOS_PROIBIDOS: ClassVar[frozenset[str]] = frozenset({"dados_classificacao", "saida_classificacao", "runs"})
    TEXTOS_PROIBIDOS: ClassVar[tuple[str, ...]] = ("sinais.jsonl", "preliminares.jsonl", "dados/classificacao")

    def _arquivos(self) -> list[Path]:
        """Arquivos da fase de decisão: o pacote ``vicio_ia/sistema`` e o ``executar_sistema.py``.

        Returns:
            Caminhos dos arquivos.
        """
        raiz: Path = Caminhos.padrao().raiz
        arquivos: list[Path] = sorted((raiz / "vicio_ia" / "sistema").rglob("*.py"))
        entrada: Path = raiz / "executar_sistema.py"
        if entrada.is_file():
            arquivos.append(entrada)
        return arquivos

    def _modulos_importados(self, arvore: ast.AST) -> list[str]:
        """Nomes de módulos importados num arquivo.

        Args:
            arvore: AST do arquivo.

        Returns:
            Nomes completos dos módulos.
        """
        nomes: list[str] = []
        no: ast.AST
        for no in ast.walk(arvore):
            if isinstance(no, ast.Import):
                nomes.extend(alias.name for alias in no.names)
            elif isinstance(no, ast.ImportFrom) and no.module:
                nomes.append(no.module)
        return nomes

    def teste_sem_imports_proibidos(self) -> None:
        """Nenhum import de LLM, rede, subprocesso ou da decisão da etapa 1."""
        violacoes: list[str] = []
        arquivo: Path
        for arquivo in self._arquivos():
            nome: str
            for nome in self._modulos_importados(ast.parse(arquivo.read_text(encoding="utf-8"))):
                if any(nome == p or nome.startswith(p + ".") for p in self.PROIBIDOS):
                    violacoes.append(f"{arquivo.name}: {nome}")
        self.assertEqual(violacoes, [])

    def teste_sem_caminhos_da_etapa1(self) -> None:
        """Nenhuma referência aos votos e decisões de LLM gravados na etapa 1."""
        violacoes: list[str] = []
        arquivo: Path
        for arquivo in self._arquivos():
            no: ast.AST
            for no in ast.walk(ast.parse(arquivo.read_text(encoding="utf-8"))):
                if isinstance(no, ast.Attribute) and no.attr in self.ATRIBUTOS_PROIBIDOS:
                    violacoes.append(f"{arquivo.name}: .{no.attr}")
                if isinstance(no, ast.Constant) and isinstance(no.value, str):
                    violacoes.extend(f"{arquivo.name}: {t!r}" for t in self.TEXTOS_PROIBIDOS if t in no.value)
        self.assertEqual(violacoes, [])

    def teste_o_pacote_tem_modulos(self) -> None:
        """O teste só faz sentido se encontrar os módulos da fase de decisão."""
        self.assertGreater(len(self._arquivos()), 1)


class TesteTrava(unittest.TestCase):
    """A trava proíbe criar provedores e acessar a rede, e devolve tudo ao estado anterior."""

    def setUp(self) -> None:
        """Cria a trava (desativada)."""
        self.trava: TravaSemLLM = TravaSemLLM()
        self.conectar_original: Callable[..., object] = socket.socket.connect

    def tearDown(self) -> None:
        """Garante a trava desativada mesmo se um teste falhar."""
        self.trava.desativar()

    def teste_fabrica_recusa_provedores_com_a_trava(self) -> None:
        """Com a trava ativa, a fábrica de provedores levanta erro antes de criar qualquer coisa."""
        self.trava.ativar()
        with self.assertRaises(ErroProvedor):
            FabricaProvedores(Caminhos.padrao(), ParametrosLLM())

    def teste_rede_bloqueada_com_a_trava(self) -> None:
        """Conectar ou resolver nomes levanta ``ErroTrava``."""
        self.trava.ativar()
        conexao: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            with self.assertRaises(ErroTrava):
                conexao.connect(("127.0.0.1", 9))
        finally:
            conexao.close()
        with self.assertRaises(ErroTrava):
            socket.getaddrinfo("example.com", 80)

    def teste_desativar_restaura_o_socket(self) -> None:
        """Depois de desativar, ``socket.connect`` volta a ser o original e a fábrica volta a funcionar."""
        self.trava.ativar()
        self.trava.desativar()
        self.assertIs(socket.socket.connect, self.conectar_original)
        self.assertFalse(self.trava.ativa)


if __name__ == "__main__":
    unittest.main()
