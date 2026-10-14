"""Portão de qualidade: roda todas as checagens do padrão de código (ADR-001) em sequência."""

from __future__ import annotations

import subprocess
import sys
import time
from dataclasses import dataclass

from ferramentas.checar_anotacoes import Problema, VerificadorAnotacoes
from vicio_ia.configuracao import Caminhos, ParametrosQualidade


@dataclass(frozen=True)
class Etapa:
    """Uma checagem feita por ferramenta externa.

    Attributes:
        nome: Nome exibido no resumo.
        comando: Comando completo, já com o interpretador do ambiente.
    """

    nome: str
    comando: tuple[str, ...]


@dataclass(frozen=True)
class ResultadoEtapa:
    """Resultado de uma checagem.

    Attributes:
        nome: Nome da checagem.
        sucesso: ``True`` se passou.
        saida: Saída da ferramenta (exibida só em caso de falha).
        segundos: Duração da checagem.
    """

    nome: str
    sucesso: bool
    saida: str
    segundos: float


class PortaoQualidade:
    """Executa ruff (lint e formatação), mypy estrito e o verificador de anotações.

    As ferramentas externas são chamadas com o mesmo interpretador que roda este
    código (``python -m ruff``, ``python -m mypy``); com ``uv run``, é o do ``.venv``.
    """

    def __init__(self, caminhos: Caminhos | None = None, parametros: ParametrosQualidade | None = None) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto (opcional, útil em testes).
            parametros: O que checar (opcional, útil em testes).
        """
        self._caminhos: Caminhos = caminhos if caminhos is not None else Caminhos.padrao()
        self._parametros: ParametrosQualidade = parametros if parametros is not None else ParametrosQualidade()

    def alvos_python(self) -> list[str]:
        """Lista pacotes e pontos de entrada que o mypy deve checar.

        Returns:
            Caminhos relativos à raiz.
        """
        entradas: list[str] = sorted(
            str(caminho.relative_to(self._caminhos.raiz))
            for padrao in self._parametros.pontos_de_entrada
            for caminho in self._caminhos.raiz.glob(padrao)
        )
        return [*self._parametros.pacotes, *entradas]

    def etapas(self) -> list[Etapa]:
        """Monta a lista de checagens externas.

        Returns:
            Etapas na ordem de execução.
        """
        python: str = sys.executable
        return [
            Etapa("ruff check", (python, "-m", "ruff", "check", ".")),
            Etapa("ruff format --check", (python, "-m", "ruff", "format", "--check", ".")),
            Etapa("mypy --strict", (python, "-m", "mypy", "--strict", *self.alvos_python())),
        ]

    def executar(self) -> bool:
        """Roda todas as checagens e imprime um resumo.

        Returns:
            ``True`` se todas passaram.
        """
        resultados: list[ResultadoEtapa] = [self._rodar(etapa) for etapa in self.etapas()]
        resultados.append(self._rodar_verificador())
        resultado: ResultadoEtapa
        for resultado in resultados:
            marca: str = "OK   " if resultado.sucesso else "FALHA"
            print(f"[{marca}] {resultado.nome} ({resultado.segundos:.1f}s)")
            if not resultado.sucesso:
                print(self._recuar(resultado.saida))
        aprovado: bool = all(resultado.sucesso for resultado in resultados)
        print("Portão de qualidade: aprovado." if aprovado else "Portão de qualidade: reprovado.")
        return aprovado

    def _rodar(self, etapa: Etapa) -> ResultadoEtapa:
        """Executa uma ferramenta externa na raiz do projeto.

        Args:
            etapa: Checagem a executar.

        Returns:
            Resultado da checagem.
        """
        inicio: float = time.perf_counter()
        processo: subprocess.CompletedProcess[str] = subprocess.run(
            list(etapa.comando), cwd=self._caminhos.raiz, capture_output=True, text=True, check=False
        )
        saida: str = (processo.stdout + processo.stderr).strip()
        return ResultadoEtapa(etapa.nome, processo.returncode == 0, saida, time.perf_counter() - inicio)

    def _rodar_verificador(self) -> ResultadoEtapa:
        """Executa o verificador de anotações e docstrings.

        Returns:
            Resultado da checagem.
        """
        inicio: float = time.perf_counter()
        verificador: VerificadorAnotacoes = VerificadorAnotacoes(
            self._caminhos.raiz, self._parametros.padroes_anotacoes
        )
        problemas: list[Problema] = verificador.verificar()
        saida: str = "\n".join(str(problema) for problema in problemas)
        nome: str = f"anotações e docstrings ({len(verificador.arquivos())} arquivos)"
        return ResultadoEtapa(nome, not problemas, saida, time.perf_counter() - inicio)

    @staticmethod
    def _recuar(texto: str) -> str:
        """Recua a saída de uma ferramenta para destacá-la no resumo.

        Args:
            texto: Saída original.

        Returns:
            Texto com quatro espaços no início de cada linha.
        """
        return "\n".join(f"    {linha}" for linha in texto.splitlines())
