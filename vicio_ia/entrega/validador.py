"""Validador dos entregáveis (ADR-015): ``publicacao.csv`` e ``previsao.txt`` no formato do LEIA-ME.

Lê os arquivos do disco, como a banca vai ler, sem usar nada do pipeline além da árvore.
"""

from __future__ import annotations

import csv
import re
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar, TextIO

from vicio_ia.carregamento import CarregadorDados
from vicio_ia.configuracao import Caminhos
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados


class ValidadorEntrega:
    """Confere o ``publicacao.csv`` e o ``previsao.txt`` da raiz do repositório."""

    COLUNAS: ClassVar[tuple[str, ...]] = ("id", "decisao", "tema_central_id", "extras_ids", "confianca", "motivo")
    _RE_LINHA: ClassVar[re.Pattern[str]] = re.compile(
        r"^(precisao_prevista|cobertura_prevista): (\d(?:\.\d+)?)\s*(?:#.*)?$|"
        r"^(precisao_intervalo|cobertura_intervalo): (\d(?:\.\d+)?)-(\d(?:\.\d+)?)\s*(?:#.*)?$"
    )

    def __init__(self, caminhos: Caminhos | None = None) -> None:
        """Define os caminhos; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto (opcional).
        """
        self._caminhos: Caminhos = caminhos if caminhos is not None else Caminhos.padrao()

    def validar(self) -> list[str]:
        """Roda todas as checagens.

        Returns:
            Problemas encontrados (vazio = entrega válida).
        """
        temas: list[TemaPreparado] = LeitorPreparados(self._caminhos).temas()
        publicaveis: set[str] = {tema.tema_id for tema in temas if tema.publicavel}
        ids_questoes: list[str] = [
            q.id
            for q in CarregadorDados(self._caminhos).para_questoes(
                CarregadorDados(self._caminhos).ler_questoes_brutas()
            )
        ]
        problemas: list[str] = []
        linhas: list[dict[str, str]] = self._ler_csv(problemas)
        publicadas: int = self._checar_csv(linhas, ids_questoes, publicaveis, problemas)
        self._checar_previsao(publicadas, len(ids_questoes), problemas)
        return problemas

    def _ler_csv(self, problemas: list[str]) -> list[dict[str, str]]:
        """Lê o ``publicacao.csv``.

        Args:
            problemas: Acumulador de problemas.

        Returns:
            Linhas (vazio se o arquivo faltar ou o cabeçalho estiver errado).
        """
        arquivo_csv: Path = self._caminhos.raiz / "publicacao.csv"
        if not arquivo_csv.is_file():
            problemas.append("publicacao.csv não existe")
            return []
        arquivo: TextIO
        with arquivo_csv.open(encoding="utf-8", newline="") as arquivo:
            leitor: csv.DictReader[str] = csv.DictReader(arquivo)
            if tuple(leitor.fieldnames or ()) != self.COLUNAS:
                problemas.append(f"cabeçalho {leitor.fieldnames} diferente de {list(self.COLUNAS)}")
                return []
            return [{k: (v or "").strip() for k, v in linha.items()} for linha in leitor]

    @staticmethod
    def _checar_csv(
        linhas: Sequence[dict[str, str]], ids_questoes: Sequence[str], publicaveis: set[str], problemas: list[str]
    ) -> int:
        """Confere cada linha do CSV.

        Args:
            linhas: Linhas lidas.
            ids_questoes: IDs das 359 questões.
            publicaveis: IDs de temas publicáveis.
            problemas: Acumulador de problemas.

        Returns:
            Número de questões publicadas.
        """
        if not linhas:
            return 0
        ids: list[str] = [linha["id"] for linha in linhas]
        if sorted(ids) != sorted(ids_questoes):
            faltam: set[str] = set(ids_questoes) - set(ids)
            sobram: set[str] = set(ids) - set(ids_questoes)
            repetidos: set[str] = {i for i in ids if ids.count(i) > 1}
            problemas.append(
                f"IDs: faltam {sorted(faltam)[:5]}, sobram {sorted(sobram)[:5]}, repetidos {sorted(repetidos)[:5]}"
            )
        linha: dict[str, str]
        for linha in linhas:
            rotulo: str = linha["id"]
            decisao: str = linha["decisao"]
            tema: str = linha["tema_central_id"]
            extras: list[str] = [e for e in linha["extras_ids"].split(";") if e] if linha["extras_ids"] else []
            if decisao not in ("publicar", "revisar", "fora"):
                problemas.append(f"{rotulo}: decisão {decisao!r}")
            if decisao in ("publicar", "revisar") and tema not in publicaveis:
                problemas.append(f"{rotulo}: tema_central_id {tema!r} vazio ou não publicável em {decisao}")
            if decisao == "fora" and tema:
                problemas.append(f"{rotulo}: tema_central_id preenchido em fora")
            if any(extra not in publicaveis for extra in extras):
                problemas.append(f"{rotulo}: extras_ids com ID inválido")
            if tema and tema in extras:
                problemas.append(f"{rotulo}: extras_ids repete o tema central")
            if "," in linha["extras_ids"] or " " in linha["extras_ids"]:
                problemas.append(f"{rotulo}: extras_ids deve usar ';' sem espaços")
            try:
                confianca: float = float(linha["confianca"])
            except ValueError:
                problemas.append(f"{rotulo}: confianca não numérica")
            else:
                if not 0.0 <= confianca <= 1.0:
                    problemas.append(f"{rotulo}: confianca fora de [0, 1]")
            if decisao in ("revisar", "fora") and not linha["motivo"]:
                problemas.append(f"{rotulo}: motivo vazio em {decisao}")
        return sum(1 for linha in linhas if linha["decisao"] == "publicar")

    def _checar_previsao(self, publicadas: int, total: int, problemas: list[str]) -> None:
        """Confere as quatro linhas do ``previsao.txt`` e a coerência com o CSV.

        Args:
            publicadas: Publicadas no CSV.
            total: Total de questões.
            problemas: Acumulador de problemas.
        """
        arquivo: Path = self._caminhos.raiz / "previsao.txt"
        if not arquivo.is_file():
            problemas.append("previsao.txt não existe")
            return
        primeiras: list[str] = arquivo.read_text(encoding="utf-8").splitlines()[:4]
        valores: dict[str, tuple[float, ...]] = {}
        linha: str
        for linha in primeiras:
            achado: re.Match[str] | None = self._RE_LINHA.match(linha.strip())
            if achado is None:
                problemas.append(f"previsao.txt: linha fora do formato: {linha!r}")
                continue
            if achado.group(1):
                valores[achado.group(1)] = (float(achado.group(2)),)
            else:
                valores[achado.group(3)] = (float(achado.group(4)), float(achado.group(5)))
        chaves: tuple[str, ...] = (
            "precisao_prevista",
            "precisao_intervalo",
            "cobertura_prevista",
            "cobertura_intervalo",
        )
        if tuple(valores) != chaves:
            problemas.append(f"previsao.txt: esperadas as linhas {list(chaves)} nesta ordem")
            return
        nome: str
        for nome in ("precisao", "cobertura"):
            ponto: float = valores[f"{nome}_prevista"][0]
            baixo: float = valores[f"{nome}_intervalo"][0]
            alto: float = valores[f"{nome}_intervalo"][1]
            if not 0.0 <= baixo <= ponto <= alto <= 1.0:
                problemas.append(f"previsao.txt: {nome} fora do intervalo ({baixo}–{alto}, ponto {ponto})")
        observada: float = publicadas / total if total else 0.0
        if abs(valores["cobertura_prevista"][0] - observada) > 0.005:
            problemas.append(
                f"previsao.txt: cobertura prevista {valores['cobertura_prevista'][0]} ≠ observada {observada:.3f}"
            )
