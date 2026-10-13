"""Estruturas de relatório (tabelas e seções) e gravação em Markdown, CSV e JSON, usadas pela EDA e pela infra."""

from __future__ import annotations

import csv
import json
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import Field, dataclass, field, fields, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import TextIO

type Celula = str | int | float
"""Valor de uma célula de tabela."""


class RegistroTabular:
    """Base para dataclasses que viram linhas de CSV (perfis de questão e de tema).

    Booleanos viram 0/1, ``None`` vira célula vazia e tuplas viram texto
    separado por ``;``.
    """

    @classmethod
    def colunas(cls) -> list[str]:
        """Nomes das colunas, na ordem dos campos da dataclass.

        Returns:
            Lista de nomes de campos.

        Raises:
            TypeError: Se a subclasse não for uma dataclass.
        """
        if not is_dataclass(cls):
            raise TypeError(f"{cls.__name__} precisa ser uma dataclass")
        return [campo.name for campo in fields(cls)]

    def como_linha(self) -> list[Celula]:
        """Converte a instância numa linha de CSV.

        Returns:
            Valores na ordem de :meth:`colunas`.

        Raises:
            TypeError: Se a subclasse não for uma dataclass.
        """
        if not is_dataclass(self) or isinstance(self, type):
            raise TypeError(f"{type(self).__name__} precisa ser uma dataclass")
        linha: list[Celula] = []
        campo: Field[object]
        for campo in fields(self):
            linha.append(self._converter(getattr(self, campo.name)))
        return linha

    @staticmethod
    def _converter(valor: object) -> Celula:
        """Converte um valor de campo em célula.

        Args:
            valor: Valor original.

        Returns:
            Valor pronto para o CSV.
        """
        if valor is None:
            return ""
        if isinstance(valor, bool):
            return int(valor)
        if isinstance(valor, (int, float, str)):
            return valor
        if isinstance(valor, (tuple, list, set, frozenset)):
            return ";".join(str(item) for item in valor)
        return str(valor)


@dataclass
class Tabela:
    """Uma tabela de resultados.

    Attributes:
        nome: Identificador curto, usado no nome do CSV (``tipos_comando``).
        titulo: Título exibido no relatório.
        colunas: Cabeçalho.
        linhas: Linhas completas (o CSV recebe todas; o Markdown, só as primeiras).
        nota: Texto opcional exibido abaixo da tabela.
    """

    nome: str
    titulo: str
    colunas: list[str]
    linhas: list[list[Celula]]
    nota: str = ""


@dataclass
class Secao:
    """Uma seção do relatório.

    Attributes:
        titulo: Título da seção.
        achados: Frases curtas com o que a seção mostra (viram tópicos no Markdown).
        tabelas: Tabelas de apoio.
        metricas: Números-chave, gravados em ``resumo_eda.json``.
    """

    titulo: str
    achados: list[str] = field(default_factory=list)
    tabelas: list[Tabela] = field(default_factory=list)
    metricas: dict[str, Celula] = field(default_factory=dict)


class Analise(ABC):
    """Contrato comum das análises da EDA."""

    @abstractmethod
    def executar(self) -> list[Secao]:
        """Roda a análise.

        Returns:
            Seções prontas para o relatório.
        """


class EscritorRelatorio:
    """Grava o relatório em Markdown, cada tabela em CSV e as métricas em JSON."""

    def __init__(
        self, pasta_saida: Path, linhas_por_tabela: int, nome_base: str = "eda", limite_celula: int = 160
    ) -> None:
        """Define onde e como gravar.

        Args:
            pasta_saida: Pasta de saída (é criada se não existir).
            linhas_por_tabela: Máximo de linhas de cada tabela no Markdown.
            nome_base: Sufixo dos arquivos (``relatorio_<nome_base>.md``, ``resumo_<nome_base>.json``).
            limite_celula: Máximo de caracteres por célula no Markdown.
        """
        self._pasta: Path = pasta_saida
        self._nome_base: str = nome_base
        self._pasta_tabelas: Path = pasta_saida / "tabelas"
        self._linhas_por_tabela: int = linhas_por_tabela
        self._limite_celula: int = limite_celula

    def preparar_pasta(self) -> None:
        """Cria as pastas de saída e apaga CSVs de execuções anteriores."""
        self._pasta_tabelas.mkdir(parents=True, exist_ok=True)
        antigo: Path
        for antigo in self._pasta_tabelas.glob("*.csv"):
            antigo.unlink()

    def escrever_csv(self, nome_arquivo: str, colunas: Sequence[str], linhas: Sequence[Sequence[Celula]]) -> Path:
        """Grava uma tabela em CSV (UTF-8, separador vírgula).

        Args:
            nome_arquivo: Nome do arquivo, sem extensão.
            colunas: Cabeçalho.
            linhas: Linhas de valores.

        Returns:
            Caminho do arquivo gravado.
        """
        destino: Path = self._pasta_tabelas / f"{nome_arquivo}.csv"
        arquivo: TextIO
        with destino.open("w", encoding="utf-8", newline="") as arquivo:
            csv.writer(arquivo).writerows([list(colunas), *[list(linha) for linha in linhas]])
        return destino

    def escrever(self, titulo: str, introducao: Sequence[str], secoes: Sequence[Secao]) -> Path:
        """Grava o relatório completo.

        Args:
            titulo: Título do relatório.
            introducao: Parágrafos exibidos antes das seções.
            secoes: Seções na ordem de exibição.

        Returns:
            Caminho do Markdown gravado.
        """
        partes: list[str] = [f"# {titulo}", "", f"_Gerado em {datetime.now():%d/%m/%Y %H:%M}._", ""]
        paragrafo: str
        for paragrafo in introducao:
            partes.extend([paragrafo, ""])
        partes.extend(self._sumario(secoes))
        indice: int
        secao: Secao
        for indice, secao in enumerate(secoes, start=1):
            partes.extend(self._secao_markdown(indice, secao))
        destino: Path = self._pasta / f"relatorio_{self._nome_base}.md"
        destino.write_text("\n".join(partes).rstrip() + "\n", encoding="utf-8")
        self._escrever_resumo(secoes)
        return destino

    def _sumario(self, secoes: Sequence[Secao]) -> list[str]:
        """Monta o sumário com links para as seções.

        Args:
            secoes: Seções do relatório.

        Returns:
            Linhas de Markdown.
        """
        linhas: list[str] = ["## Sumário", ""]
        indice: int
        secao: Secao
        for indice, secao in enumerate(secoes, start=1):
            linhas.append(f"{indice}. {secao.titulo}")
        linhas.append("")
        return linhas

    def _secao_markdown(self, indice: int, secao: Secao) -> list[str]:
        """Converte uma seção em Markdown e grava os CSVs das suas tabelas.

        Args:
            indice: Número da seção.
            secao: Seção a converter.

        Returns:
            Linhas de Markdown.
        """
        linhas: list[str] = [f"## {indice}. {secao.titulo}", ""]
        achado: str
        for achado in secao.achados:
            linhas.append(f"- {achado}")
        if secao.achados:
            linhas.append("")
        posicao: int
        tabela: Tabela
        for posicao, tabela in enumerate(secao.tabelas, start=1):
            nome_csv: str = f"{indice:02d}_{posicao:02d}_{tabela.nome}"
            self.escrever_csv(nome_csv, tabela.colunas, tabela.linhas)
            linhas.extend(self._tabela_markdown(tabela, nome_csv))
        return linhas

    def _tabela_markdown(self, tabela: Tabela, nome_csv: str) -> list[str]:
        """Converte uma tabela em Markdown, limitando o número de linhas.

        Args:
            tabela: Tabela a converter.
            nome_csv: Nome do CSV com a versão completa.

        Returns:
            Linhas de Markdown.
        """
        linhas: list[str] = [f"**{tabela.titulo}**", ""]
        if not tabela.linhas:
            linhas.extend(["_Nenhuma linha._", ""])
            return linhas
        linhas.append("| " + " | ".join(self._celula(coluna) for coluna in tabela.colunas) + " |")
        linhas.append("|" + "|".join("---" for _ in tabela.colunas) + "|")
        linha: list[Celula]
        for linha in tabela.linhas[: self._linhas_por_tabela]:
            linhas.append("| " + " | ".join(self._celula(valor) for valor in linha) + " |")
        rodape: list[str] = []
        if len(tabela.linhas) > self._linhas_por_tabela:
            rodape.append(f"mostrando {self._linhas_por_tabela} de {len(tabela.linhas)} linhas")
        rodape.append(f"completa em `tabelas/{nome_csv}.csv`")
        linhas.extend(["", f"_{'; '.join(rodape)}._"])
        if tabela.nota:
            linhas.extend(["", f"> {tabela.nota}"])
        linhas.append("")
        return linhas

    def _celula(self, valor: Celula) -> str:
        """Formata uma célula para Markdown.

        Args:
            valor: Valor da célula.

        Returns:
            Texto sem quebras de linha, com ``|`` escapado e cortado no limite.
        """
        texto: str = f"{valor:.2f}" if isinstance(valor, float) else str(valor)
        texto = " ".join(texto.split()).replace("|", "\\|")
        if len(texto) > self._limite_celula:
            texto = texto[: self._limite_celula - 1].rstrip() + "…"
        return texto

    def _escrever_resumo(self, secoes: Sequence[Secao]) -> Path:
        """Grava as métricas de todas as seções em ``resumo_<nome_base>.json``.

        Args:
            secoes: Seções do relatório.

        Returns:
            Caminho do JSON gravado.
        """
        resumo: dict[str, dict[str, Celula]] = {secao.titulo: secao.metricas for secao in secoes}
        destino: Path = self._pasta / f"resumo_{self._nome_base}.json"
        destino.write_text(json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")
        return destino
