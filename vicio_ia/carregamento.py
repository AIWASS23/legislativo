"""Leitura dos anexos do case (``questoes.jsonl`` e ``temas.csv``)."""

from __future__ import annotations

import csv
import json
from typing import ClassVar, TextIO

from vicio_ia.configuracao import Caminhos
from vicio_ia.dominio import Questao, Tema

type RegistroBruto = dict[str, object]
"""Uma linha do JSONL exatamente como foi lida, antes de qualquer conversão."""


class ErroDeCarga(Exception):
    """Erro ao ler ou interpretar um arquivo de entrada."""


class CarregadorDados:
    """Lê os anexos e devolve registros brutos e entidades de domínio.

    Os registros brutos servem para checar integridade (campos ausentes, tipos
    inesperados). As entidades já vêm com valores coerentes: textos ausentes
    viram ``""`` e alternativas ausentes viram um dicionário vazio.
    """

    CAMPOS_QUESTAO: ClassVar[tuple[str, ...]] = (
        "id",
        "enunciado_html",
        "comando",
        "alternativas",
        "disciplina_origem",
        "assunto_origem",
    )
    CAMPOS_TEMA: ClassVar[tuple[str, ...]] = (
        "tema_id",
        "parent_id",
        "disciplina",
        "nivel",
        "titulo",
        "caminho",
        "descricao",
        "status",
    )

    def __init__(self, caminhos: Caminhos) -> None:
        """Guarda os caminhos dos arquivos de entrada.

        Args:
            caminhos: Caminhos do projeto.
        """
        self._caminhos: Caminhos = caminhos

    def ler_questoes_brutas(self) -> list[RegistroBruto]:
        """Lê ``questoes.jsonl`` linha a linha, sem converter os valores.

        Returns:
            Um dicionário por questão, na ordem do arquivo.

        Raises:
            ErroDeCarga: Se uma linha não for JSON válido ou não for um objeto.
        """
        registros: list[RegistroBruto] = []
        numero: int
        linha: str
        arquivo: TextIO
        with self._caminhos.questoes.open(encoding="utf-8") as arquivo:
            for numero, linha in enumerate(arquivo, start=1):
                if not linha.strip():
                    continue
                try:
                    valor: object = json.loads(linha)
                except json.JSONDecodeError as erro:
                    raise ErroDeCarga(f"{self._caminhos.questoes.name}, linha {numero}: {erro}") from erro
                if not isinstance(valor, dict):
                    raise ErroDeCarga(f"{self._caminhos.questoes.name}, linha {numero}: esperado um objeto JSON")
                registros.append(valor)
        return registros

    def ler_temas_brutos(self) -> list[dict[str, str]]:
        """Lê ``temas.csv`` como dicionários de texto.

        Returns:
            Uma linha do CSV por tema, na ordem do arquivo.

        Raises:
            ErroDeCarga: Se faltar alguma coluna esperada no cabeçalho.
        """
        linhas: list[dict[str, str]]
        arquivo: TextIO
        with self._caminhos.temas.open(encoding="utf-8", newline="") as arquivo:
            leitor: csv.DictReader[str] = csv.DictReader(arquivo)
            cabecalho: list[str] = list(leitor.fieldnames or [])
            faltantes: list[str] = [campo for campo in self.CAMPOS_TEMA if campo not in cabecalho]
            if faltantes:
                raise ErroDeCarga(f"{self._caminhos.temas.name}: colunas ausentes {faltantes}")
            linhas = list(leitor)
        return linhas

    def para_questoes(self, registros: list[RegistroBruto]) -> list[Questao]:
        """Converte registros brutos em :class:`Questao`.

        Args:
            registros: Registros lidos por :meth:`ler_questoes_brutas`.

        Returns:
            Questões na mesma ordem dos registros.
        """
        questoes: list[Questao] = []
        registro: RegistroBruto
        for registro in registros:
            questoes.append(
                Questao(
                    id=self._texto(registro, "id"),
                    enunciado_html=self._texto(registro, "enunciado_html"),
                    comando=self._texto(registro, "comando"),
                    alternativas=self._alternativas(registro),
                    disciplina_origem=self._texto(registro, "disciplina_origem"),
                    assunto_origem=self._texto(registro, "assunto_origem"),
                )
            )
        return questoes

    def carregar_temas(self) -> list[Tema]:
        """Lê ``temas.csv`` e converte cada linha em :class:`Tema`.

        Returns:
            Temas na ordem do arquivo.

        Raises:
            ErroDeCarga: Se ``nivel`` não for um número inteiro.
        """
        temas: list[Tema] = []
        linha: dict[str, str]
        for linha in self.ler_temas_brutos():
            nivel_texto: str = (linha.get("nivel") or "").strip()
            if not nivel_texto.isdigit():
                raise ErroDeCarga(f"tema {linha.get('tema_id')}: nível inválido {nivel_texto!r}")
            pai: str = (linha.get("parent_id") or "").strip()
            temas.append(
                Tema(
                    tema_id=(linha.get("tema_id") or "").strip(),
                    parent_id=pai or None,
                    disciplina=linha.get("disciplina") or "",
                    nivel=int(nivel_texto),
                    titulo=linha.get("titulo") or "",
                    caminho=linha.get("caminho") or "",
                    descricao=linha.get("descricao") or "",
                    status=(linha.get("status") or "").strip(),
                )
            )
        return temas

    @staticmethod
    def _texto(registro: RegistroBruto, chave: str) -> str:
        """Lê um campo de texto, tratando ausência e ``null`` como ``""``.

        Args:
            registro: Registro bruto.
            chave: Nome do campo.

        Returns:
            O valor como texto.
        """
        valor: object = registro.get(chave)
        if valor is None:
            return ""
        return valor if isinstance(valor, str) else str(valor)

    @staticmethod
    def _alternativas(registro: RegistroBruto) -> dict[str, str]:
        """Lê o campo ``alternativas``, aceitando ausência e valores nulos.

        Args:
            registro: Registro bruto.

        Returns:
            Letra -> texto da alternativa. Vazio se o campo não for um objeto.
        """
        valor: object = registro.get("alternativas")
        alternativas: dict[str, str] = {}
        if not isinstance(valor, dict):
            return alternativas
        letra: object
        texto: object
        for letra, texto in valor.items():
            alternativas[str(letra)] = "" if texto is None else str(texto)
        return alternativas
