"""Revisão das propostas de conhecimento (ADR-020): fila por prioridade e aplicação das decisões."""

from __future__ import annotations

import csv
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from typing import TextIO

from testes.fabrica import FabricaTestes
from vicio_ia.configuracao import Caminhos
from vicio_ia.enriquecimento.revisao import DecisaoRevisao, FilaRevisao, ItemRevisao, MontadorConhecimento


class TesteRevisaoConhecimento(unittest.TestCase):
    """O mapa vem primeiro, depois os termos de risco; as decisões alteram os artefatos finais."""

    def setUp(self) -> None:
        """Cria as propostas num diretório temporário."""
        self.pasta: tempfile.TemporaryDirectory[str] = tempfile.TemporaryDirectory()
        raiz: Path = Path(self.pasta.name)
        self.caminhos: Caminhos = replace(Caminhos.padrao(), raiz=raiz, dados_conhecimento=raiz / "conhecimento")
        propostas: Path = self.caminhos.dados_conhecimento / "propostas"
        propostas.mkdir(parents=True)
        self.artigos: list[dict[str, str]] = [
            {
                "lei": "CP",
                "art_inicio": "121",
                "art_fim": "128",
                "tema_id": "X1",
                "caminho": "",
                "forca": "exata",
                "origem": "llm",
            },
            {
                "lei": "CP",
                "art_inicio": "1",
                "art_fim": "4",
                "tema_id": "U",
                "caminho": "",
                "forca": "exata",
                "origem": "llm",
            },
        ]
        self.termos: list[dict[str, str]] = [
            {
                "termo": "rixa",
                "termo_normalizado": "rixa",
                "tema_id": "L",
                "caminho": "",
                "tipo": "forte",
                "tema_id_alvo": "",
                "origem": "llm",
            },
            {
                "termo": "dolo",
                "termo_normalizado": "dolo",
                "tema_id": "U",
                "caminho": "",
                "tipo": "fraco",
                "tema_id_alvo": "",
                "origem": "llm",
            },
        ]
        self._gravar(propostas / "mapa_artigos.csv", self.artigos)
        self._gravar(propostas / "termos.csv", self.termos)

    def tearDown(self) -> None:
        """Apaga o diretório temporário."""
        self.pasta.cleanup()

    @staticmethod
    def _gravar(destino: Path, linhas: list[dict[str, str]]) -> None:
        """Grava um CSV de propostas.

        Args:
            destino: Arquivo.
            linhas: Linhas.
        """
        arquivo: TextIO
        with destino.open("w", encoding="utf-8", newline="") as arquivo:
            escritor: csv.DictWriter[str] = csv.DictWriter(arquivo, fieldnames=list(linhas[0]))
            escritor.writeheader()
            escritor.writerows(linhas)

    def teste_fila_por_prioridade(self) -> None:
        """Os 2 artigos vêm primeiro; o termo forte da lixeira L é de risco; "dolo" cai na amostra."""
        fila: list[ItemRevisao] = FilaRevisao(FabricaTestes().temas()).montar(self.artigos, self.termos)
        self.assertEqual([i.prioridade for i in fila], [1, 1, 2, 3])
        self.assertEqual(fila[2].campos["termo"], "rixa")

    def teste_decisoes_aplicadas(self) -> None:
        """Artigo corrigido, artigo apagado, termo aceito e termo não revisado."""
        fila: list[ItemRevisao] = FilaRevisao(FabricaTestes().temas()).montar(self.artigos, self.termos)
        decisoes: dict[str, DecisaoRevisao] = {
            fila[0].chave: DecisaoRevisao(fila[0].chave, "artigo", "corrigir", "CP|121|129|X1", "2026-10-21T09:00:00"),
            fila[1].chave: DecisaoRevisao(fila[1].chave, "artigo", "apagar", "", "2026-10-21T09:01:00"),
            fila[2].chave: DecisaoRevisao(fila[2].chave, "termo", "aceitar", "", "2026-10-21T09:02:00"),
        }
        resumo: dict[str, str] = MontadorConhecimento(self.caminhos).montar(decisoes, fila)
        artigos: list[dict[str, str]] = MontadorConhecimento.ler_csv(
            self.caminhos.dados_conhecimento / "mapa_artigos.csv"
        )
        termos: list[dict[str, str]] = MontadorConhecimento.ler_csv(self.caminhos.dados_conhecimento / "termos.csv")
        self.assertEqual([(a["art_fim"], a["revisado"]) for a in artigos], [("129", "sim")])
        self.assertEqual([(t["termo"], t["revisado"]) for t in termos], [("rixa", "sim"), ("dolo", "nao")])
        self.assertEqual(resumo["amostra_revisada"], "0/1")
        self.assertTrue((self.caminhos.dados_conhecimento / "manifesto.json").is_file())


if __name__ == "__main__":
    unittest.main()
