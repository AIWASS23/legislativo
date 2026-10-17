"""Recuo para o pai (ADR-010): quando publicar no subtema, quando recuar e quando nunca recuar."""

from __future__ import annotations

import unittest

from testes.fabrica import FabricaTestes
from vicio_ia.classificacao.respostas import SinaisQuestao
from vicio_ia.decisao.agregacao import AgregadorSinais, DecisaoPreliminar


class TesteRecuo(unittest.TestCase):
    """As cinco situações da ADR-010 e as lixeiras fortes (D3)."""

    def setUp(self) -> None:
        """Monta a árvore sintética e o agregador."""
        self.fabrica: FabricaTestes = FabricaTestes()
        self.agregador: AgregadorSinais = AgregadorSinais(self.fabrica.temas())

    def _decidir(self, sinais: SinaisQuestao) -> DecisaoPreliminar:
        """Decide uma questão sem marcas especiais e sem assunto de origem.

        Args:
            sinais: Sinais da questão.

        Returns:
            Decisão preliminar.
        """
        return self.agregador.decidir(sinais, self.fabrica.questao(), ())

    def teste_subtema_confirmado_publica_o_subtema(self) -> None:
        """A, B e voto no subtema X1 e verificador confirma: candidata em X1, sem recuo."""
        decisao: DecisaoPreliminar = self._decidir(self.fabrica.simples("X1", "X1", "X1", "confirma", "X1", "X1"))
        self.assertEqual(decisao.acao, "candidata")
        self.assertEqual(decisao.tema_id, "X1")
        self.assertFalse(decisao.recuou)
        self.assertEqual(decisao.nivel, 2)

    def teste_verificador_escolhe_irmao_recua_para_o_pai(self) -> None:
        """Fontes em X1, verificador escolhe o irmão X2: recua para T e guarda os dois subtemas."""
        decisao: DecisaoPreliminar = self._decidir(self.fabrica.simples("X1", "X1", "X1", "irmao", "X1", "X2"))
        self.assertEqual(decisao.acao, "candidata")
        self.assertEqual(decisao.tema_id, "T")
        self.assertTrue(decisao.recuou)
        self.assertEqual(set(decisao.extras_ids), {"X1", "X2"})

    def teste_verificador_escolhe_o_pai_recua(self) -> None:
        """Verificador escolhe o pai T: recua para T."""
        decisao: DecisaoPreliminar = self._decidir(self.fabrica.simples("X1", "X1", "X1", "pai", "X1", "T"))
        self.assertEqual(decisao.tema_id, "T")
        self.assertTrue(decisao.recuou)

    def teste_verificador_escolhe_filho_mantem_o_candidato(self) -> None:
        """Candidato T e verificador escolhe o filho X1: publica T (certo para T e para X1) e guarda X1."""
        decisao: DecisaoPreliminar = self._decidir(self.fabrica.simples("T", "T", "T", "filho", "T", "X1"))
        self.assertEqual(decisao.tema_id, "T")
        self.assertFalse(decisao.recuou)
        self.assertIn("X1", decisao.extras_ids)

    def teste_divergencia_entre_tema_e_filho_confirmada_no_filho(self) -> None:
        """A em T e B em X1 (mesmo ramo); candidato X1 confirmado: publica X1."""
        decisao: DecisaoPreliminar = self._decidir(self.fabrica.simples("T", "X1", "X1", "confirma", "X1", "X1"))
        self.assertEqual(decisao.acao, "candidata")
        self.assertEqual(decisao.tema_id, "X1")

    def teste_ramos_diferentes_vao_para_revisao_sem_recuo(self) -> None:
        """A em X1 e B em U (ramos diferentes): revisar, sem recuo."""
        decisao: DecisaoPreliminar = self._decidir(self.fabrica.simples("X1", "U", "X1", "nao_rodou", "", ""))
        self.assertEqual(decisao.acao, "revisar")
        self.assertEqual(decisao.motivo, "dúvida entre X1 e U")
        self.assertFalse(decisao.recuou)

    def teste_nunca_recua_para_a_disciplina(self) -> None:
        """Candidato de nível 1 com verificador no irmão U: o pai é a disciplina, então vai para revisão."""
        decisao: DecisaoPreliminar = self._decidir(self.fabrica.simples("T", "T", "T", "irmao", "T", "U"))
        self.assertEqual(decisao.acao, "revisar")
        self.assertEqual(decisao.motivo, "verificador sugere U")
        self.assertNotEqual(decisao.tema_id, "D")

    def teste_lixeira_forte_sem_concordancia_total_recua(self) -> None:
        """Subtema lixeira LX com o voto barato discordando: recua para o pai T2."""
        decisao: DecisaoPreliminar = self._decidir(self.fabrica.simples("LX", "LX", "U", "confirma", "LX", "LX"))
        self.assertEqual(decisao.tema_id, "T2")
        self.assertTrue(decisao.recuou)
        self.assertIn("LX", decisao.extras_ids)

    def teste_lixeira_forte_com_concordancia_total_publica(self) -> None:
        """Subtema lixeira LX com as três fontes e o verificador de acordo: candidata em LX."""
        decisao: DecisaoPreliminar = self._decidir(self.fabrica.simples("LX", "LX", "LX", "confirma", "LX", "LX"))
        self.assertEqual(decisao.acao, "candidata")
        self.assertEqual(decisao.tema_id, "LX")

    def teste_lixeira_forte_de_nivel_1_sem_concordancia_vai_para_revisao(self) -> None:
        """Tema lixeira L sem pai publicável e sem concordância total: revisar."""
        decisao: DecisaoPreliminar = self._decidir(self.fabrica.simples("L", "L", "U", "confirma", "L", "L"))
        self.assertEqual(decisao.acao, "revisar")
        self.assertEqual(decisao.motivo, "tema genérico sem evidência suficiente")


if __name__ == "__main__":
    unittest.main()
