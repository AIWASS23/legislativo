"""Verificador do padrão de código do projeto (ADR-001).

Confere, por análise sintática (``ast``), o que o ruff e o mypy não exigem:

* toda variável tem anotação de tipo na primeira atribuição do escopo, inclusive
  as locais; alvos de ``for`` e ``with`` precisam ser declarados antes com tipo;
* atributos ``self.x`` são anotados na primeira atribuição (ou no corpo da classe);
* atributos de classe têm anotação;
* módulos, classes e funções têm docstring;
* parâmetros e retornos têm tipo e não há ``*args`` nem ``**kwargs``.

Variáveis de compreensões, de ``except ... as``, de padrões de ``match`` e de
expressões de atribuição (``:=``) não podem ser anotadas em Python e são ignoradas.
"""

from __future__ import annotations

import ast
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar


@dataclass(frozen=True)
class Problema:
    """Um desvio do padrão de código.

    Attributes:
        arquivo: Caminho do arquivo, relativo à raiz do projeto.
        linha: Linha onde o problema começa.
        descricao: O que está fora do padrão.
    """

    arquivo: str
    linha: int
    descricao: str

    def __str__(self) -> str:
        """Formata o problema como ``arquivo:linha: descrição``."""
        return f"{self.arquivo}:{self.linha}: {self.descricao}"


class AnalisadorModulo:
    """Analisa um arquivo Python e acumula os problemas encontrados."""

    PARAMETROS_IMPLICITOS: ClassVar[frozenset[str]] = frozenset({"self", "cls"})
    NOMES_IGNORADOS: ClassVar[frozenset[str]] = frozenset({"_"})

    def __init__(self, caminho: Path, rotulo: str) -> None:
        """Prepara a análise de um arquivo.

        Args:
            caminho: Caminho do arquivo.
            rotulo: Nome exibido nas mensagens (caminho relativo à raiz).
        """
        self._caminho: Path = caminho
        self._rotulo: str = rotulo
        self._problemas: list[Problema] = []

    def analisar(self) -> list[Problema]:
        """Analisa o arquivo inteiro.

        Returns:
            Problemas encontrados, na ordem em que aparecem.
        """
        modulo: ast.Module = ast.parse(self._caminho.read_text(encoding="utf-8"), filename=str(self._caminho))
        if ast.get_docstring(modulo) is None:
            self._registrar(1, "módulo sem docstring")
        self._verificar_bloco(modulo.body, set(), None)
        return list(self._problemas)

    def _registrar(self, linha: int, descricao: str) -> None:
        """Guarda um problema.

        Args:
            linha: Linha do problema.
            descricao: Descrição curta.
        """
        self._problemas.append(Problema(self._rotulo, linha, descricao))

    def _verificar_bloco(
        self, instrucoes: Sequence[ast.stmt], declarados: set[str], atributos: set[str] | None
    ) -> None:
        """Percorre um bloco de instruções em ordem, conferindo cada atribuição.

        Args:
            instrucoes: Instruções do bloco.
            declarados: Nomes já declarados com tipo no escopo (é atualizado).
            atributos: Atributos ``self.x`` já declarados na classe, ou ``None`` fora de métodos.
        """
        instrucao: ast.stmt
        for instrucao in instrucoes:
            if isinstance(instrucao, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._verificar_funcao(instrucao, set() if atributos is None else atributos)
            elif isinstance(instrucao, ast.ClassDef):
                self._verificar_classe(instrucao)
            elif isinstance(instrucao, ast.AnnAssign):
                self._declarar(instrucao.target, declarados, atributos)
            elif isinstance(instrucao, ast.Assign):
                alvo: ast.expr
                for alvo in instrucao.targets:
                    self._exigir_declaracao(alvo, "atribuição", declarados, atributos)
            elif isinstance(instrucao, (ast.For, ast.AsyncFor)):
                self._exigir_declaracao(instrucao.target, "alvo de for", declarados, atributos)
                self._verificar_bloco(instrucao.body, declarados, atributos)
                self._verificar_bloco(instrucao.orelse, declarados, atributos)
            elif isinstance(instrucao, (ast.With, ast.AsyncWith)):
                item: ast.withitem
                for item in instrucao.items:
                    if item.optional_vars is not None:
                        self._exigir_declaracao(item.optional_vars, "alvo de with", declarados, atributos)
                self._verificar_bloco(instrucao.body, declarados, atributos)
            elif isinstance(instrucao, (ast.If, ast.While)):
                self._verificar_bloco(instrucao.body, declarados, atributos)
                self._verificar_bloco(instrucao.orelse, declarados, atributos)
            elif isinstance(instrucao, (ast.Try, ast.TryStar)):
                self._verificar_bloco(instrucao.body, declarados, atributos)
                tratador: ast.ExceptHandler
                for tratador in instrucao.handlers:
                    self._verificar_bloco(tratador.body, declarados, atributos)
                self._verificar_bloco(instrucao.orelse, declarados, atributos)
                self._verificar_bloco(instrucao.finalbody, declarados, atributos)
            elif isinstance(instrucao, ast.Match):
                caso: ast.match_case
                for caso in instrucao.cases:
                    self._verificar_bloco(caso.body, declarados, atributos)

    def _verificar_classe(self, classe: ast.ClassDef) -> None:
        """Confere docstring, atributos de classe e métodos.

        Args:
            classe: Definição da classe.
        """
        if ast.get_docstring(classe) is None:
            self._registrar(classe.lineno, f"classe sem docstring: {classe.name}")
        atributos: set[str] = set()
        instrucao: ast.stmt
        for instrucao in classe.body:
            if isinstance(instrucao, ast.AnnAssign) and isinstance(instrucao.target, ast.Name):
                atributos.add(f"self.{instrucao.target.id}")
            elif isinstance(instrucao, ast.Assign):
                alvo: ast.expr
                for alvo in instrucao.targets:
                    nome: ast.expr
                    for nome in self._alvos(alvo):
                        if isinstance(nome, ast.Name):
                            self._registrar(instrucao.lineno, f"atributo de classe sem tipo: {classe.name}.{nome.id}")
        for instrucao in classe.body:
            if isinstance(instrucao, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._verificar_funcao(instrucao, atributos)
            elif isinstance(instrucao, ast.ClassDef):
                self._verificar_classe(instrucao)

    def _verificar_funcao(self, funcao: ast.FunctionDef | ast.AsyncFunctionDef, atributos: set[str]) -> None:
        """Confere docstring, assinatura e variáveis de uma função ou método.

        Args:
            funcao: Definição da função.
            atributos: Atributos ``self.x`` já declarados na classe (é atualizado).
        """
        if ast.get_docstring(funcao) is None:
            self._registrar(funcao.lineno, f"função sem docstring: {funcao.name}")
        argumentos: list[ast.arg] = [*funcao.args.posonlyargs, *funcao.args.args, *funcao.args.kwonlyargs]
        argumento: ast.arg
        for argumento in argumentos:
            if argumento.arg not in self.PARAMETROS_IMPLICITOS and argumento.annotation is None:
                self._registrar(funcao.lineno, f"parâmetro sem tipo: {funcao.name}({argumento.arg})")
        if funcao.args.vararg is not None or funcao.args.kwarg is not None:
            self._registrar(funcao.lineno, f"usa *args/**kwargs: {funcao.name}")
        if funcao.returns is None:
            self._registrar(funcao.lineno, f"retorno sem tipo: {funcao.name}")
        declarados: set[str] = {argumento.arg for argumento in argumentos}
        self._verificar_bloco(funcao.body, declarados, atributos)

    def _declarar(self, alvo: ast.expr, declarados: set[str], atributos: set[str] | None) -> None:
        """Registra um nome declarado com anotação.

        Args:
            alvo: Alvo de uma atribuição anotada.
            declarados: Nomes declarados no escopo (é atualizado).
            atributos: Atributos da classe (é atualizado), ou ``None``.
        """
        chave: str | None = self._chave(alvo)
        if chave is None:
            return
        if chave.startswith("self."):
            if atributos is not None:
                atributos.add(chave)
        else:
            declarados.add(chave)

    def _exigir_declaracao(
        self, alvo: ast.expr, contexto: str, declarados: set[str], atributos: set[str] | None
    ) -> None:
        """Registra problema para cada nome atribuído sem declaração prévia com tipo.

        Args:
            alvo: Alvo da atribuição (pode ser tupla).
            contexto: Tipo de atribuição, para a mensagem.
            declarados: Nomes declarados no escopo (é atualizado para não repetir o aviso).
            atributos: Atributos da classe (é atualizado), ou ``None``.
        """
        nome: ast.expr
        for nome in self._alvos(alvo):
            chave: str | None = self._chave(nome)
            if chave is None or chave in self.NOMES_IGNORADOS:
                continue
            conhecidos: set[str] | None = atributos if chave.startswith("self.") else declarados
            if conhecidos is None or chave in conhecidos:
                continue
            self._registrar(nome.lineno, f"{contexto} sem tipo: {chave}")
            conhecidos.add(chave)

    @staticmethod
    def _alvos(alvo: ast.expr) -> list[ast.expr]:
        """Desmonta alvos compostos (tuplas, listas, ``*resto``) em alvos simples.

        Args:
            alvo: Alvo de uma atribuição.

        Returns:
            Alvos simples, na ordem.
        """
        if isinstance(alvo, (ast.Tuple, ast.List)):
            simples: list[ast.expr] = []
            elemento: ast.expr
            for elemento in alvo.elts:
                simples.extend(AnalisadorModulo._alvos(elemento))
            return simples
        if isinstance(alvo, ast.Starred):
            return AnalisadorModulo._alvos(alvo.value)
        return [alvo]

    @staticmethod
    def _chave(alvo: ast.expr) -> str | None:
        """Identifica o que um alvo declara.

        Args:
            alvo: Alvo simples.

        Returns:
            O nome (``x``), ``self.x`` para atributos de instância, ou ``None``
            para alvos que não criam variável (``lista[0] = ...``, ``obj.x = ...``).
        """
        if isinstance(alvo, ast.Name):
            return alvo.id
        if isinstance(alvo, ast.Attribute) and isinstance(alvo.value, ast.Name) and alvo.value.id in {"self", "cls"}:
            return f"self.{alvo.attr}"
        return None


class VerificadorAnotacoes:
    """Aplica o :class:`AnalisadorModulo` a todos os arquivos do projeto."""

    def __init__(self, raiz: Path, padroes: Sequence[str]) -> None:
        """Define onde procurar arquivos.

        Args:
            raiz: Pasta raiz do projeto.
            padroes: Padrões ``glob`` relativos à raiz (``vicio_ia/**/*.py``).
        """
        self._raiz: Path = raiz
        self._padroes: tuple[str, ...] = tuple(padroes)

    def arquivos(self) -> list[Path]:
        """Lista os arquivos cobertos pelos padrões.

        Returns:
            Caminhos sem repetição, em ordem alfabética.
        """
        encontrados: set[Path] = set()
        padrao: str
        for padrao in self._padroes:
            encontrados.update(caminho for caminho in self._raiz.glob(padrao) if caminho.is_file())
        return sorted(encontrados)

    def verificar(self) -> list[Problema]:
        """Analisa todos os arquivos.

        Returns:
            Problemas de todos os arquivos.
        """
        problemas: list[Problema] = []
        caminho: Path
        for caminho in self.arquivos():
            problemas.extend(AnalisadorModulo(caminho, str(caminho.relative_to(self._raiz))).analisar())
        return problemas
