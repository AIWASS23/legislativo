"""Propostas de conhecimento (ADR-020): normalização da lei e conversão da resposta, sem chamar modelo."""

from __future__ import annotations

import unittest
from typing import cast

from testes.fabrica import FabricaTestes
from vicio_ia.configuracao import Caminhos, ParametrosConhecimento
from vicio_ia.enriquecimento.propostas import (
    ErroPropostas,
    GeradorPropostas,
    GrupoTemas,
    NormalizadorLei,
    PropostasGrupo,
)
from vicio_ia.llm.cliente import ClienteLLM
from vicio_ia.llm.prompts import ArquivoPrompt
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.texto import ProcessadorTexto


class TesteNormalizadorLei(unittest.TestCase):
    """Formas livres da lei viram a forma canônica do mapa de artigos."""

    def setUp(self) -> None:
        """Cria o normalizador."""
        self.leis: NormalizadorLei = NormalizadorLei(ProcessadorTexto())

    def teste_codigos(self) -> None:
        """Siglas, nomes por extenso e decretos-leis dos códigos."""
        self.assertEqual(self.leis.normalizar("CP"), "CP")
        self.assertEqual(self.leis.normalizar("Código de Processo Penal"), "CPP")
        self.assertEqual(self.leis.normalizar("Decreto-Lei 3.689/1941"), "CPP")
        self.assertEqual(self.leis.normalizar("Lei 7.210/84"), "LEP")

    def teste_leis_numeradas(self) -> None:
        """Número com ou sem ponto; ano com 2 ou 4 dígitos; texto sem lei vira ``None``."""
        self.assertEqual(self.leis.normalizar("Lei 11.343/2006"), "Lei 11.343/2006")
        self.assertEqual(self.leis.normalizar("Lei nº 9099/95"), "Lei 9.099/1995")
        self.assertIsNone(self.leis.normalizar("doutrina majoritária"))


class TesteConversaoPropostas(unittest.TestCase):
    """A conversão aceita o que é válido, descarta o resto com aviso e exige todos os nós do grupo."""

    def setUp(self) -> None:
        """Monta o gerador sobre a árvore sintética (o cliente não é usado na conversão)."""
        temas: list[TemaPreparado] = FabricaTestes().temas()
        prompt: ArquivoPrompt = ArquivoPrompt(Caminhos.padrao().prompts / "conhecimento_tema.md")
        self.gerador: GeradorPropostas = GeradorPropostas(
            cast(ClienteLLM, object()), prompt, temas, "", [], ParametrosConhecimento(), 1
        )
        self.grupo: GrupoTemas = next(g for g in self.gerador.grupos() if g.pai.tema_id == "T")

    def teste_itens_validos_e_descartados(self) -> None:
        """Referência válida, lei desconhecida, intervalo invertido, termo forte e "exclui" sem destino."""
        dados: dict[str, object] = {
            "temas": [
                {
                    "tema_id": "X1",
                    "referencias": [
                        {"lei": "CP", "art_inicio": 121, "art_fim": 128},
                        {"lei": "tratado X", "art_inicio": 1, "art_fim": 2},
                        {"lei": "CPP", "art_inicio": 50, "art_fim": 10},
                    ],
                    "termos": [
                        {"termo": "Homicídio privilegiado", "tipo": "forte", "tema_id_alvo": "nenhum"},
                        {"termo": "homicidio privilegiado", "tipo": "fraco", "tema_id_alvo": "nenhum"},
                        {"termo": "rixa", "tipo": "exclui", "tema_id_alvo": "nenhum"},
                        {"termo": "lesão", "tipo": "exclui", "tema_id_alvo": "U"},
                    ],
                },
                {"tema_id": "X2", "referencias": [], "termos": []},
            ]
        }
        resultado: PropostasGrupo = self.gerador._converter(self.grupo, dados, False)
        self.assertEqual(
            [(r.lei, r.art_inicio, r.art_fim, r.forca) for r in resultado.referencias], [("CP", 121, 128, "exata")]
        )
        self.assertEqual(
            [(t.normalizado, t.tipo, t.tema_id_alvo) for t in resultado.termos],
            [("homicidio privilegiado", "forte", ""), ("lesao", "exclui", "U")],
        )
        self.assertEqual(len(resultado.avisos), 3)

    def teste_no_faltante_levanta_erro(self) -> None:
        """Se um nó do grupo não vier na resposta, a conversão falha (e a chamada é repetida)."""
        with self.assertRaises(ErroPropostas):
            self.gerador._converter(self.grupo, {"temas": [{"tema_id": "X1", "referencias": [], "termos": []}]}, False)


if __name__ == "__main__":
    unittest.main()
