"""Citações de lei e artigo (ADR-021): os cinco caminhos de resolução, os pendentes e o mapa de artigos."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from vicio_ia.enriquecimento.citacoes import (
    ArquivoCitacoes,
    CitacoesQuestao,
    CorrecaoCitacao,
    CorrecoesCitacoes,
    ExtratorCitacoes,
)
from vicio_ia.sistema.mapa_artigos import LinhaMapa, MapaArtigos


class TesteExtratorCitacoes(unittest.TestCase):
    """Formas reais das questões viram (lei, artigo) com a resolução certa."""

    def setUp(self) -> None:
        """Cria o extrator."""
        self.extrator: ExtratorCitacoes = ExtratorCitacoes()

    def _artigos(self, texto: str) -> list[tuple[str, int, int, str]]:
        """Extrai e resume os artigos citados.

        Args:
            texto: Texto da questão.

        Returns:
            ``(lei, início, fim, resolução)`` de cada artigo.
        """
        citacoes: CitacoesQuestao = self.extrator.extrair("Q9999", texto)
        return [(a.lei, a.inicio, a.fim, a.resolucao) for a in citacoes.artigos]

    def teste_lei_depois_do_artigo(self) -> None:
        """Parágrafos, incisos e parênteses curtos entre o artigo e a lei não atrapalham."""
        self.assertEqual(self._artigos("art. 155, § 4º, inciso I, do CP"), [("CP", 155, 155, "explicita")])
        self.assertEqual(
            self._artigos("o art. 121, § 2.º, inciso II (homicídio qualificado por motivo fútil), do CP"),
            [("CP", 121, 121, "explicita")],
        )
        self.assertEqual(
            self._artigos("Art. 33, caput, da Lei nº 11.343/2006"), [("Lei 11.343/2006", 33, 33, "explicita")]
        )
        self.assertEqual(self._artigos("Art. 16 da Lei Maria da Penha"), [("Lei 11.340/2006", 16, 16, "explicita")])

    def teste_lei_antes_do_artigo(self) -> None:
        """Lei antes do artigo: "CP, art. 159" e "o Código de Processo Penal, em seu art. 406"."""
        self.assertEqual(self._artigos("extorsão mediante sequestro (CP, art. 159)"), [("CP", 159, 159, "explicita")])
        self.assertEqual(
            self._artigos("O Código de Processo Penal, em seu art. 406, estabelece"), [("CPP", 406, 406, "explicita")]
        )

    def teste_listas_e_intervalos(self) -> None:
        """Listas e intervalos: "arts. 33, caput, e 35", "arts. 158-A a 158-F" e "artigos 89 a 108"."""
        self.assertEqual(
            self._artigos("Arts. 33, caput, e 35, ambos da Lei nº 11.343/2006"),
            [("Lei 11.343/2006", 33, 33, "explicita"), ("Lei 11.343/2006", 35, 35, "explicita")],
        )
        self.assertEqual(
            self._artigos("arts. 158-A a 158-F do Código de Processo Penal"), [("CPP", 158, 158, "explicita")]
        )
        self.assertEqual(self._artigos("artigos 89 a 108 do CP"), [("CP", 89, 108, "explicita")])

    def teste_enumeracao(self) -> None:
        """O artigo herda a lei do artigo seguinte: "art. 155, caput, c/c art. 14, II, ambos do CP"."""
        self.assertEqual(
            self._artigos("previsto no art. 155, caput, c/c art. 14, II, ambos do CP."),
            [("CP", 155, 155, "enumeracao"), ("CP", 14, 14, "explicita")],
        )

    def teste_anafora_e_repeticao(self) -> None:
        """Anáfora ("do mesmo diploma legal") remete à lei anterior; o mesmo artigo repetido herda a lei."""
        self.assertEqual(
            self._artigos("O CPP, em seu art. 406, manda citar. O art. 409, do mesmo diploma legal, manda ouvir."),
            [("CPP", 406, 406, "explicita"), ("CPP", 409, 409, "anafora")],
        )
        self.assertEqual(
            self._artigos("Art. 129 do CP e Art. 16 da Lei 11.340/2006. A audiência do Art. 16, pois, é nula."),
            [
                ("CP", 129, 129, "explicita"),
                ("Lei 11.340/2006", 16, 16, "explicita"),
                ("Lei 11.340/2006", 16, 16, "repeticao"),
            ],
        )

    def teste_contexto_e_lei_sem_nome(self) -> None:
        """Lei única vale para o artigo solto, exceto quando a questão fala de uma lei sem nome."""
        self.assertEqual(
            self._artigos("Sobre o Código Penal. Art. 1º - Não há crime sem lei anterior."),
            [("CP", 1, 1, "contexto")],
        )
        citacoes: CitacoesQuestao = self.extrator.extrair(
            "Q9999",
            "pena (art. 77 do Código Penal). A composição, nos arts. 74 e 75 da Lei, é causa. Transação (art. 76).",
        )
        self.assertEqual([(a.lei, a.inicio) for a in citacoes.artigos], [("CP", 77)])
        self.assertEqual(len(citacoes.pendentes), 2)
        self.assertEqual(citacoes.leis, ("CP",))

    def teste_formas_da_lei(self) -> None:
        """Decreto-lei com data por extenso, lei sem ano, código militar e lei especial com ano curto."""
        self.assertEqual(
            self._artigos("art. 366 do Decreto-Lei nº 3.689, de 3 de outubro de 1941"), [("CPP", 366, 366, "explicita")]
        )
        self.assertEqual(self._artigos("art. 12 da Lei n°9.609, cujo"), [("Lei 9.609/1998", 12, 12, "explicita")])
        self.assertEqual(self._artigos("art. 9º do Código Penal Militar"), [("CPM", 9, 9, "explicita")])
        self.assertEqual(self._artigos("art. 2° da Lei n° 12.850/13"), [("Lei 12.850/2013", 2, 2, "explicita")])

    def teste_sem_citacao(self) -> None:
        """Texto sem artigo nem lei não gera nada."""
        citacoes: CitacoesQuestao = self.extrator.extrair("Q9999", "A arte de julgar exige prudência.")
        self.assertEqual((citacoes.leis, citacoes.artigos, citacoes.pendentes), ((), (), ()))

    def teste_arquivo_ida_e_volta(self) -> None:
        """Gravar e ler o JSONL devolve as mesmas citações."""
        citacoes: CitacoesQuestao = self.extrator.extrair("Q0001", "art. 155 do CP e art. 76 da Lei, solto")
        pasta: str
        with tempfile.TemporaryDirectory() as pasta:
            arquivo: ArquivoCitacoes = ArquivoCitacoes(Path(pasta) / "citacoes.jsonl")
            arquivo.gravar([citacoes])
            self.assertEqual(arquivo.ler(), {"Q0001": citacoes})


class TesteCorrecoesCitacoes(unittest.TestCase):
    """A correção do autor resolve os pendentes da questão e é recusada onde não há pendente."""

    def teste_aplicar(self) -> None:
        """O artigo corrigido entra como ``manual``, a lei entra na lista e os pendentes somem."""
        extrator: ExtratorCitacoes = ExtratorCitacoes()
        citacoes: list[CitacoesQuestao] = [
            extrator.extrair("Q1", "pena (art. 77 do CP). A composição, nos arts. 74 e 75 da Lei, é causa."),
            extrator.extrair("Q2", "art. 155 do CP"),
        ]
        corrigidas: list[CitacoesQuestao] = CorrecoesCitacoes.aplicar(
            citacoes, [CorrecaoCitacao("Q1", "Lei 9.099/1995", 74, 75)]
        )
        self.assertEqual(corrigidas[0].pendentes, ())
        self.assertEqual(corrigidas[0].leis, ("CP", "Lei 9.099/1995"))
        self.assertEqual(
            [(a.lei, a.inicio, a.fim, a.resolucao) for a in corrigidas[0].artigos],
            [("CP", 77, 77, "explicita"), ("Lei 9.099/1995", 74, 75, "manual")],
        )
        self.assertEqual(corrigidas[1], citacoes[1])
        with self.assertRaises(ValueError):
            CorrecoesCitacoes.aplicar(citacoes, [CorrecaoCitacao("Q2", "CP", 1, 1)])

    def teste_ler_csv(self) -> None:
        """Arquivo ausente vira lista vazia; colunas extras (observação) são aceitas."""
        pasta: str
        with tempfile.TemporaryDirectory() as pasta:
            arquivo: Path = Path(pasta) / "citacoes_manuais.csv"
            self.assertEqual(CorrecoesCitacoes(arquivo).ler(), [])
            arquivo.write_text("id,lei,art_inicio,art_fim,observacao\nQ1,Lei 8.666/1993,89,108,x\n", encoding="utf-8")
            self.assertEqual(CorrecoesCitacoes(arquivo).ler(), [CorrecaoCitacao("Q1", "Lei 8.666/1993", 89, 108)])


class TesteMapaArtigos(unittest.TestCase):
    """O mapa casa a lei pela chave (código ou número) e o artigo pelo intervalo."""

    def teste_busca(self) -> None:
        """Lei citada sem o ano acha a linha com ano; artigo fora do intervalo não acha nada."""
        mapa: MapaArtigos = MapaArtigos(
            [
                LinhaMapa("CP", 155, 155, "5159", "exata", False),
                LinhaMapa("CP", 155, 183, "5157", "ramo", True),
                LinhaMapa("Lei 9.609/1998", 12, 12, "4699", "exata", False),
            ]
        )
        self.assertEqual([linha.tema_id for linha in mapa.linhas("CP", 155, 155)], ["5159", "5157"])
        self.assertEqual([linha.tema_id for linha in mapa.linhas("Lei 9.609", 12, 12)], ["4699"])
        self.assertEqual(mapa.linhas("CPP", 155, 155), [])
        self.assertEqual(mapa.linhas("CP", 200, 210), [])
        self.assertEqual(MapaArtigos.chave_lei("Lei 11.343/2006"), "11343")
