"""Política publicar / revisar / fora (ADR-011, etapas 1 a 3) e variáveis da calibração."""

from __future__ import annotations

import unittest
from dataclasses import replace

from testes.fabrica import FabricaTestes
from vicio_ia.avaliacao.calibracao import CalibradorFaixas
from vicio_ia.classificacao.respostas import SinaisQuestao, VotoClassificador
from vicio_ia.decisao.agregacao import AgregadorSinais, DecisaoPreliminar


class TestePolitica(unittest.TestCase):
    """Fora, falhas, verificador em outro ramo, sobreposição, multitema e concordância."""

    def setUp(self) -> None:
        """Monta a árvore sintética e o agregador."""
        self.fabrica: FabricaTestes = FabricaTestes()
        self.agregador: AgregadorSinais = AgregadorSinais(self.fabrica.temas())

    def _decidir(
        self, sinais: SinaisQuestao, generico: bool = False, origem: tuple[str, ...] = ()
    ) -> DecisaoPreliminar:
        """Decide uma questão.

        Args:
            sinais: Sinais da questão.
            generico: Enunciado genérico.
            origem: Temas do assunto de origem.

        Returns:
            Decisão preliminar.
        """
        return self.agregador.decidir(sinais, self.fabrica.questao(generico=generico), origem)

    def teste_fora_exige_a_b_e_o_verificador(self) -> None:
        """A e B marcam fora e o verificador responde "nenhum": decisão fora."""
        f: FabricaTestes = self.fabrica
        sinais: SinaisQuestao = f.sinais(
            f.voto("classificador_a", "U", fora=True),
            f.voto("classificador_b", "U", fora=True),
            f.voto("voto_barato", "U"),
            f.veredito("nenhum", "U", "nenhum"),
        )
        decisao: DecisaoPreliminar = self._decidir(sinais)
        self.assertEqual(decisao.acao, "fora")
        self.assertEqual(decisao.motivo, "nenhum tema do recorte serve")

    def teste_fora_parcial_vai_para_revisao(self) -> None:
        """Só A marca fora: revisar com o motivo "possível fora do recorte"."""
        f: FabricaTestes = self.fabrica
        sinais: SinaisQuestao = f.sinais(
            f.voto("classificador_a", "U", fora=True),
            f.voto("classificador_b", "U"),
            f.voto("voto_barato", "U"),
            f.veredito("confirma", "U", "U"),
        )
        decisao: DecisaoPreliminar = self._decidir(sinais)
        self.assertEqual(decisao.acao, "revisar")
        self.assertEqual(decisao.motivo, "possível fora do recorte")

    def teste_falha_de_a_sugere_o_tema_de_b(self) -> None:
        """A sem voto válido: revisar por falha, com a sugestão de B."""
        f: FabricaTestes = self.fabrica
        sinais: SinaisQuestao = f.sinais(
            f.voto("classificador_a", "", ok=False),
            f.voto("classificador_b", "X1"),
            f.voto("voto_barato", "U"),
            f.veredito("nao_rodou", "", ""),
        )
        decisao: DecisaoPreliminar = self._decidir(sinais)
        self.assertEqual(decisao.acao, "revisar")
        self.assertEqual(decisao.motivo, "falha de classificação")
        self.assertEqual(decisao.tema_id, "X1")

    def teste_falha_de_a_e_b_sugere_o_voto_barato(self) -> None:
        """A e B sem voto: a sugestão ao professor vem do voto barato (o LEIA-ME exige tema em revisar)."""
        f: FabricaTestes = self.fabrica
        sinais: SinaisQuestao = f.sinais(
            f.voto("classificador_a", "", ok=False),
            f.voto("classificador_b", "", ok=False),
            f.voto("voto_barato", "U"),
            f.veredito("nao_rodou", "", ""),
        )
        decisao: DecisaoPreliminar = self._decidir(sinais)
        self.assertEqual(decisao.acao, "revisar")
        self.assertEqual(decisao.tema_id, "U")

    def teste_verificador_em_outro_ramo_vai_para_revisao(self) -> None:
        """Verificador escolhe um nó de outro ramo: revisar, com a escolha dele no motivo e nos extras."""
        decisao: DecisaoPreliminar = self._decidir(self.fabrica.simples("P1", "P1", "P1", "outro", "P1", "P2"))
        self.assertEqual(decisao.acao, "revisar")
        self.assertEqual(decisao.motivo, "verificador sugere P2")
        self.assertIn("P2", decisao.extras_ids)

    def teste_sobreposicao_em_conflito_vai_para_revisao(self) -> None:
        """Candidato P1 e voto barato no par P2 do mesmo grupo (outra disciplina): revisar por sobreposição."""
        decisao: DecisaoPreliminar = self._decidir(self.fabrica.simples("P1", "P1", "P2", "confirma", "P1", "P1"))
        self.assertEqual(decisao.acao, "revisar")
        self.assertEqual(decisao.motivo, "sobreposição: P1 × P2")

    def teste_sobreposicao_sem_conflito_segue_candidata(self) -> None:
        """Candidato P1 com todas as fontes em P1: a regra de desempate resolveu, segue candidata."""
        decisao: DecisaoPreliminar = self._decidir(self.fabrica.simples("P1", "P1", "P1", "confirma", "P1", "P1"))
        self.assertEqual(decisao.acao, "candidata")

    def teste_multitema_com_enunciado_generico_vai_para_revisao(self) -> None:
        """A e B marcam multitema e o enunciado é genérico: revisar."""
        f: FabricaTestes = self.fabrica
        sinais: SinaisQuestao = f.sinais(
            f.voto("classificador_a", "U", multitema=True),
            f.voto("classificador_b", "U", multitema=True),
            f.voto("voto_barato", "U"),
            f.veredito("confirma", "U", "U"),
        )
        decisao: DecisaoPreliminar = self._decidir(sinais, generico=True)
        self.assertEqual(decisao.acao, "revisar")
        self.assertTrue(decisao.motivo.startswith("questão cobre vários temas"))

    def teste_multitema_sem_enunciado_generico_segue_candidata(self) -> None:
        """Multitema sem enunciado genérico não força revisão."""
        f: FabricaTestes = self.fabrica
        sinais: SinaisQuestao = f.sinais(
            f.voto("classificador_a", "U", multitema=True),
            f.voto("classificador_b", "U", multitema=True),
            f.voto("voto_barato", "U"),
            f.veredito("confirma", "U", "U"),
        )
        self.assertEqual(self._decidir(sinais).acao, "candidata")

    def teste_verificador_que_falhou_vai_para_revisao(self) -> None:
        """A e B de acordo, mas o verificador falhou: revisar por falha."""
        decisao: DecisaoPreliminar = self._decidir(self.fabrica.simples("U", "U", "U", "falha", "U", ""))
        self.assertEqual(decisao.acao, "revisar")
        self.assertEqual(decisao.motivo, "falha de classificação")

    def teste_fontes_no_ramo_e_concordancia(self) -> None:
        """A, B, voto barato e regras no ramo do tema: concordância 4 e as quatro fontes registradas."""
        f: FabricaTestes = self.fabrica
        sinais: SinaisQuestao = f.sinais(
            f.voto("classificador_a", "X1"),
            f.voto("classificador_b", "X1"),
            f.voto("voto_barato", "T"),
            f.veredito("confirma", "X1", "X1"),
            regras=("T",),
        )
        decisao: DecisaoPreliminar = self._decidir(sinais, origem=("X1",))
        self.assertEqual(decisao.concordancia_ramo, 4)
        self.assertEqual(set(decisao.fontes_no_ramo), {"classificador_a", "classificador_b", "voto_barato", "regras"})
        self.assertTrue(decisao.origem_mesmo_ramo)

    def teste_extras_empatados_saem_em_ordem_de_id(self) -> None:
        """Extras com a mesma contagem saem ordenados pelo ID (resultado igual em toda execução)."""
        f: FabricaTestes = self.fabrica
        a: VotoClassificador = replace(f.voto("classificador_a", "X1"), extras_ids=("U", "L", "K"))
        b: VotoClassificador = replace(f.voto("classificador_b", "X1"), extras_ids=("K", "L", "U"))
        sinais: SinaisQuestao = f.sinais(a, b, f.voto("voto_barato", "X1"), f.veredito("confirma", "X1", "X1"))
        self.assertEqual(self._decidir(sinais).extras_ids, ("K", "L", "U"))

    def teste_faixas_da_calibracao(self) -> None:
        """Consenso total exige as três fontes de LLM no ramo e o verificador confirmando."""
        consenso: DecisaoPreliminar = self._decidir(self.fabrica.simples("X1", "X1", "X1", "confirma", "X1", "X1"))
        parcial: DecisaoPreliminar = self._decidir(self.fabrica.simples("X1", "X1", "U", "confirma", "X1", "X1"))
        vizinho: DecisaoPreliminar = self._decidir(self.fabrica.simples("X1", "X1", "X1", "pai", "X1", "T"))
        revisao: DecisaoPreliminar = self._decidir(self.fabrica.simples("X1", "U", "X1", "nao_rodou", "", ""))
        self.assertEqual(CalibradorFaixas.faixa(consenso), "consenso_total")
        self.assertEqual(CalibradorFaixas.faixa(parcial), "confirma_parcial")
        self.assertEqual(CalibradorFaixas.faixa(vizinho), "verificador_vizinho")
        self.assertEqual(CalibradorFaixas.faixa(revisao), "outros")


if __name__ == "__main__":
    unittest.main()
