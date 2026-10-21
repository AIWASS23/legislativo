"""Base de temas (ADR-020): variantes do texto, ida e volta em disco, montagem e regra de escolha (E7b, E8b)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from testes.fabrica import FabricaTestes
from vicio_ia.enriquecimento.base_temas import MontadorBaseTemas
from vicio_ia.sistema.base_temas import ArquivoBaseTemas, ReferenciaTema, TemaBase, TermoTema
from vicio_ia.sistema.folha import RotuloFolha
from vicio_ia.sistema.mapa_artigos import LinhaMapa
from vicio_ia.sistema.ranking import Metrica, RegraEscolha


class TesteTemaBase(unittest.TestCase):
    """O texto de cada variante só acrescenta o que deve; os ``exclui`` e as questões nunca entram."""

    def setUp(self) -> None:
        """Um tema com cartão, termos dos três tipos, uma referência e um exemplo da folha."""
        self.tema: TemaBase = TemaBase(
            tema_id="X1",
            caminho="D > T > X1",
            titulo="X1",
            nivel=2,
            pai="T",
            irmaos=("X2",),
            filhos=(),
            escopo="Escopo do tema.",
            inclui=("item",),
            nao_inclui=(("outro assunto", "X2"),),
            ancoras=("CP, art. 155",),
            referencias=(ReferenciaTema("CP", 155, 156, "exata"),),
            termos=(
                TermoTema("furto", "furto", "forte", "", True),
                TermoTema("subtração", "subtracao", "fraco", "", False),
                TermoTema("roubo", "roubo", "exclui", "X2", True),
            ),
            exemplos_folha=("Q0001",),
        )

    def teste_variantes(self) -> None:
        """``cartao`` sem termos; ``cartao_termos`` com forte e fraco; ``cartao_termos_leis`` com a referência."""
        cartao: str = self.tema.texto("cartao")
        termos: str = self.tema.texto("cartao_termos")
        leis: str = self.tema.texto("cartao_termos_leis")
        self.assertNotIn("furto", cartao)
        self.assertIn("furto", termos)
        self.assertIn("subtração", termos)
        self.assertNotIn("roubo", leis)
        self.assertNotIn("outro assunto", leis)
        self.assertNotIn("Q0001", leis)
        self.assertTrue(leis.endswith("CP, arts. 155 a 156"))
        with self.assertRaises(ValueError):
            self.tema.texto("outra")

    def teste_ida_e_volta(self) -> None:
        """Gravar e ler devolve o mesmo registro."""
        pasta: str
        with tempfile.TemporaryDirectory() as pasta:
            arquivo: ArquivoBaseTemas = ArquivoBaseTemas(Path(pasta) / "temas.jsonl")
            arquivo.gravar([self.tema])
            self.assertEqual(arquivo.ler(), [self.tema])


class TesteMontadorBaseTemas(unittest.TestCase):
    """A montagem junta mapa, termos e exemplos da folha por tema, só para os publicáveis."""

    def teste_montagem(self) -> None:
        """X1 recebe a linha do mapa, o termo e a questão da folha (central); T recebe o extra."""
        base: list[TemaBase] = MontadorBaseTemas(
            FabricaTestes().temas(),
            [],
            [LinhaMapa("CP", 1, 2, "X1", "exata", True)],
            [
                {
                    "termo": "x",
                    "termo_normalizado": "x",
                    "tema_id": "X1",
                    "tipo": "forte",
                    "tema_id_alvo": "",
                    "revisado": "sim",
                }
            ],
            [RotuloFolha("Q1", "X1", ("T",), False), RotuloFolha("Q2", "", (), True)],
        ).montar()
        por_id: dict[str, TemaBase] = {t.tema_id: t for t in base}
        self.assertNotIn("D", por_id)
        self.assertEqual(por_id["X1"].referencias, (ReferenciaTema("CP", 1, 2, "exata"),))
        self.assertEqual(por_id["X1"].termos, (TermoTema("x", "x", "forte", "", True),))
        self.assertEqual(por_id["X1"].exemplos_folha, ("Q1",))
        self.assertEqual(por_id["X1"].irmaos, ("X2",))
        self.assertEqual(por_id["T"].exemplos_folha, ("Q1",))
        self.assertEqual(por_id["T"].filhos, ("X1", "X2"))


class TesteRegraEscolha(unittest.TestCase):
    """Maior recall@10; até uma questão é empate, decidido pelo top-1; depois, a primeira da lista."""

    @staticmethod
    def _metricas(variante: str, recall: int, top1: int) -> list[Metrica]:
        """Recall@10 e top-1 de uma variante (em questões de 92).

        Args:
            variante: Variante.
            recall: Questões no recall@10.
            top1: Questões no top-1.

        Returns:
            As duas métricas.
        """
        return [
            Metrica("E", variante, "recall@10 (92)", recall / 92),
            Metrica("E", variante, "acerto top-1 (92 com tema)", top1 / 92),
        ]

    def teste_regra(self) -> None:
        """Empate de recall (diferença de 1) vai para o top-1; empate total vai para a primeira."""
        metricas: list[Metrica] = [
            *self._metricas("a", 89, 60),
            *self._metricas("b", 90, 58),
            *self._metricas("c", 80, 80),
        ]
        self.assertEqual(RegraEscolha.escolher(metricas, "E", ["a", "b", "c"]), "a")
        iguais: list[Metrica] = [*self._metricas("a", 89, 60), *self._metricas("b", 89, 60)]
        self.assertEqual(RegraEscolha.escolher(iguais, "E", ["a", "b"]), "a")
        distante: list[Metrica] = [*self._metricas("a", 87, 70), *self._metricas("b", 90, 50)]
        self.assertEqual(RegraEscolha.escolher(distante, "E", ["a", "b"]), "b")
