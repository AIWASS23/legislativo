"""Colunas obrigatórias do ``publicacao.csv`` (ADR-011, LEIA-ME), régua do gold, corte do limiar e estimador direto."""

from __future__ import annotations

import unittest
from dataclasses import replace

from testes.fabrica import FabricaTestes
from vicio_ia.arvore import ArvoreTemas
from vicio_ia.avaliacao.calibracao import CalibradorFaixas, ExemploCalibracao
from vicio_ia.avaliacao.planilha import RotuloGold
from vicio_ia.avaliacao.pontuador import PontuadorRegua
from vicio_ia.avaliacao.previsao import PrevisorPrecisao
from vicio_ia.configuracao import ParametrosCalibracao
from vicio_ia.decisao.agregacao import AgregadorSinais, DecisaoPreliminar
from vicio_ia.decisao.pipeline import ErroPublicacao, LinhaPublicacao, PipelineDecisao
from vicio_ia.dominio import Tema
from vicio_ia.preparacao.arvore_preparada import TemaPreparado


class TesteColunasPublicacao(unittest.TestCase):
    """O validador do passo 07 recusa linhas fora do formato do LEIA-ME."""

    def setUp(self) -> None:
        """Monta a árvore e uma publicação válida de três linhas."""
        self.temas: list[TemaPreparado] = FabricaTestes().temas()
        self.validas: list[LinhaPublicacao] = [
            LinhaPublicacao("Q1", "publicar", "X1", "", 0.98, ""),
            LinhaPublicacao("Q2", "revisar", "T", "X1;X2", 0.85, "baixa confiança (P = 0,85)"),
            LinhaPublicacao("Q3", "fora", "", "", 0.7, "nenhum tema do recorte serve"),
        ]

    def _falha(self, linhas: list[LinhaPublicacao]) -> str:
        """Roda o validador esperando erro.

        Args:
            linhas: Linhas a validar.

        Returns:
            Mensagem do erro.
        """
        contexto: unittest.case._AssertRaisesContext[ErroPublicacao]
        with self.assertRaises(ErroPublicacao) as contexto:
            PipelineDecisao._validar(linhas, self.temas, len(linhas))
        return str(contexto.exception)

    def teste_publicacao_valida_passa(self) -> None:
        """As três decisões no formato certo passam."""
        PipelineDecisao._validar(self.validas, self.temas, 3)

    def teste_revisar_sem_tema_falha(self) -> None:
        """O LEIA-ME exige o tema sugerido em revisar."""
        linhas: list[LinhaPublicacao] = [self.validas[0], replace(self.validas[1], tema_central_id=""), self.validas[2]]
        self.assertIn("revisar sem sugestão publicável", self._falha(linhas))

    def teste_fora_com_tema_falha(self) -> None:
        """Em fora, o tema central fica vazio."""
        linhas: list[LinhaPublicacao] = [
            self.validas[0],
            self.validas[1],
            replace(self.validas[2], tema_central_id="U"),
        ]
        self.assertIn("fora com tema", self._falha(linhas))

    def teste_motivo_obrigatorio_em_revisar_e_fora(self) -> None:
        """Revisar e fora sem motivo falham."""
        linhas: list[LinhaPublicacao] = [self.validas[0], replace(self.validas[1], motivo=""), self.validas[2]]
        self.assertIn("sem motivo", self._falha(linhas))

    def teste_publicar_em_no_nao_publicavel_falha(self) -> None:
        """Publicar numa disciplina (não publicável) falha."""
        linhas: list[LinhaPublicacao] = [
            replace(self.validas[0], tema_central_id="D"),
            self.validas[1],
            self.validas[2],
        ]
        self.assertIn("não publicável", self._falha(linhas))

    def teste_confianca_fora_de_zero_a_um_falha(self) -> None:
        """A confiança tem de estar entre 0 e 1."""
        linhas: list[LinhaPublicacao] = [replace(self.validas[0], confianca=1.2), self.validas[1], self.validas[2]]
        self.assertIn("confiança fora de [0, 1]", self._falha(linhas))

    def teste_extra_invalido_falha(self) -> None:
        """Extras precisam ser temas publicáveis."""
        linhas: list[LinhaPublicacao] = [replace(self.validas[0], extras_ids="X2;E"), self.validas[1], self.validas[2]]
        self.assertIn("extra não publicável", self._falha(linhas))

    def teste_numero_de_linhas_e_ids_unicos(self) -> None:
        """Faltar uma questão ou repetir um ID falha."""
        self.assertIn("IDs únicos", self._falha([self.validas[0], self.validas[0], self.validas[2]]))


class TesteRegua(unittest.TestCase):
    """A régua do case aplicada ao gold, nos modos estrito e tolerante (ADR-012)."""

    def setUp(self) -> None:
        """Monta a árvore original (``Tema``) a partir da sintética."""
        temas: list[Tema] = [
            Tema(t.tema_id, t.parent_id, t.disciplina, t.nivel, t.titulo, t.caminho, "", "active")
            for t in FabricaTestes().temas()
        ]
        self.regua: PontuadorRegua = PontuadorRegua(ArvoreTemas(temas))

    @staticmethod
    def _rotulo(tema_id: str, alternativos: tuple[str, ...] = (), fora: bool = False) -> RotuloGold:
        """Cria um rótulo.

        Args:
            tema_id: Tema rotulado.
            alternativos: Alternativos plausíveis.
            fora: Rotulada fora.

        Returns:
            Rótulo.
        """
        return RotuloGold("Q1", tema_id, alternativos, fora, False, "alta", "", None, "")

    def teste_pai_e_filho_contam_como_certo(self) -> None:
        """Publicar o pai ou um filho direto do rotulado está certo."""
        self.assertTrue(self.regua.acerta("T", self._rotulo("X1"), "estrita"))
        self.assertTrue(self.regua.acerta("X1", self._rotulo("T"), "estrita"))

    def teste_irmao_conta_como_erro(self) -> None:
        """Publicar o irmão é erro nos dois modos, salvo se ele estiver entre os alternativos (tolerante)."""
        self.assertFalse(self.regua.acerta("X2", self._rotulo("X1"), "estrita"))
        self.assertFalse(self.regua.acerta("X2", self._rotulo("X1"), "tolerante"))
        self.assertTrue(self.regua.acerta("X2", self._rotulo("X1", ("X2",)), "tolerante"))

    def teste_filho_com_irmao_plausivel_e_erro_na_estrita(self) -> None:
        """Rótulo no pai com dois filhos plausíveis: publicar um filho é erro na estrita, certo na tolerante."""
        rotulo: RotuloGold = self._rotulo("T", ("X1", "X2"))
        self.assertFalse(self.regua.acerta("X1", rotulo, "estrita"))
        self.assertTrue(self.regua.acerta("X1", rotulo, "tolerante"))

    def teste_publicar_questao_fora_e_erro(self) -> None:
        """Publicar uma questão rotulada fora é sempre erro."""
        self.assertFalse(self.regua.acerta("U", self._rotulo("", fora=True), "tolerante"))


class TesteCorteDoLimiar(unittest.TestCase):
    """O limiar só corta entre valores diferentes de P (nunca no meio de uma faixa)."""

    def teste_cortes_respeitam_empates(self) -> None:
        """Com P = 0,98, 0,98, 0,95 e 0,85, os conjuntos permitidos têm 2, 3 ou 4 questões, nunca 1."""
        fabrica: FabricaTestes = FabricaTestes()
        agregador: AgregadorSinais = AgregadorSinais(fabrica.temas())
        base: DecisaoPreliminar = agregador.decidir(
            fabrica.simples("X1", "X1", "X1", "confirma", "X1", "X1"), fabrica.questao(), ()
        )
        candidatas: list[DecisaoPreliminar] = [replace(base, id=f"Q{i}") for i in range(4)]
        probabilidades: dict[str, float] = {"Q0": 0.98, "Q1": 0.98, "Q2": 0.95, "Q3": 0.85}
        self.assertEqual(PrevisorPrecisao._cortes(candidatas, probabilidades), [4, 3, 2])


class TesteEstimadorDireto(unittest.TestCase):
    """O acerto do gold nas publicadas entra no ponto com a suavização de Jeffreys (D12)."""

    def setUp(self) -> None:
        """Monta o previsor e uma decisão de consenso para os exemplos."""
        fabrica: FabricaTestes = FabricaTestes()
        self.base: DecisaoPreliminar = AgregadorSinais(fabrica.temas()).decidir(
            fabrica.simples("X1", "X1", "X1", "confirma", "X1", "X1"), fabrica.questao(), ()
        )
        self.previsor: PrevisorPrecisao = PrevisorPrecisao(ParametrosCalibracao(), CalibradorFaixas())

    def _exemplos(self, pesos: list[float], erros: int = 0) -> list[ExemploCalibracao]:
        """Exemplos do gold com os pesos dados; os ``erros`` primeiros erram.

        Args:
            pesos: Peso amostral de cada exemplo.
            erros: Quantos exemplos erram.

        Returns:
            Exemplos.
        """
        return [
            ExemploCalibracao(replace(self.base, id=f"Q{i}"), acerto=i >= erros, peso=peso)
            for i, peso in enumerate(pesos)
        ]

    def teste_treze_acertos_em_treze_nao_viram_certeza(self) -> None:
        """13 em 13 com pesos iguais: (13 + 0,5) / (13 + 1) = 0,964."""
        self.assertAlmostEqual(self.previsor._suavizar(self._exemplos([5.9] * 13)), 13.5 / 14)

    def teste_pesos_desiguais_usam_o_tamanho_efetivo(self) -> None:
        """Pesos 1 e 3, os dois certos: n efetivo = 16 / 10 = 1,6 e acerto (1,6 + 0,5) / 2,6."""
        self.assertAlmostEqual(self.previsor._suavizar(self._exemplos([1.0, 3.0])), 2.1 / 2.6)

    def teste_erro_entra_na_taxa(self) -> None:
        """Um erro em quatro, pesos iguais: (3 + 0,5) / 5 = 0,7."""
        self.assertAlmostEqual(self.previsor._suavizar(self._exemplos([1.0] * 4, erros=1)), 0.7)


if __name__ == "__main__":
    unittest.main()
