"""Folha-verdade, régua da etapa 2, validação cruzada repetida e AUC (ADR-023, ADR-024)."""

from __future__ import annotations

import tempfile
import unittest
from collections import Counter
from pathlib import Path

from testes.fabrica import FabricaTestes
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.sistema.folha import ErroFolha, LeitorFolha, ReguaEtapa2, RotuloFolha
from vicio_ia.sistema.metricas import MetricasBinarias
from vicio_ia.sistema.validacao import Particao, ValidacaoCruzadaRepetida


class TesteReguaEtapa2(unittest.TestCase):
    """Central, extra, ou pai ou filho de um deles; irmão e fora são erro."""

    def setUp(self) -> None:
        """Monta a régua sobre a árvore sintética."""
        self.regua: ReguaEtapa2 = ReguaEtapa2(FabricaTestes().temas())

    def teste_central_pai_e_irmao(self) -> None:
        """Rótulo X1: X1 e o pai T acertam; o irmão X2 e outro tema erram."""
        rotulo: RotuloFolha = RotuloFolha("Q1", "X1", (), False)
        self.assertTrue(self.regua.acerta("X1", rotulo))
        self.assertTrue(self.regua.acerta("T", rotulo))
        self.assertFalse(self.regua.acerta("X2", rotulo))
        self.assertFalse(self.regua.acerta("U", rotulo))

    def teste_extra_e_o_ramo_do_extra_contam(self) -> None:
        """Rótulo U com extra X2: X2 e o pai dele (T) acertam; X1 (irmão do extra) erra."""
        rotulo: RotuloFolha = RotuloFolha("Q1", "U", ("X2",), False)
        self.assertTrue(self.regua.acerta("X2", rotulo))
        self.assertTrue(self.regua.acerta("T", rotulo))
        self.assertFalse(self.regua.acerta("X1", rotulo))

    def teste_fora_e_tema_vazio_sao_erro(self) -> None:
        """Publicar uma questão fora é sempre erro; tema vazio nunca acerta."""
        self.assertFalse(self.regua.acerta("U", RotuloFolha("Q1", "", (), True)))
        self.assertFalse(self.regua.acerta("", RotuloFolha("Q1", "U", (), False)))


class TesteLeitorFolha(unittest.TestCase):
    """O leitor aceita o formato do LEIA-ME e junta todos os problemas numa mensagem."""

    def setUp(self) -> None:
        """Árvore sintética e diretório temporário."""
        self.temas: list[TemaPreparado] = FabricaTestes().temas()
        self.pasta: tempfile.TemporaryDirectory[str] = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        """Apaga o diretório temporário."""
        self.pasta.cleanup()

    def _ler(self, linhas: list[str]) -> list[RotuloFolha]:
        """Grava um CSV com o cabeçalho do LEIA-ME e lê.

        Args:
            linhas: Linhas de dados.

        Returns:
            Rótulos lidos.
        """
        caminho: Path = Path(self.pasta.name) / "folha.csv"
        cabecalho: str = "id,tema_central_id,tema_central_caminho,extras_ids,fora_da_taxonomia"
        caminho.write_text("\n".join([cabecalho, *linhas]) + "\n", encoding="utf-8")
        return LeitorFolha(caminho, self.temas, {"Q1", "Q2", "Q3"}).ler()

    def teste_linhas_validas(self) -> None:
        """Tema com extras e questão fora."""
        rotulos: list[RotuloFolha] = self._ler(["Q1,X1,Penal > T > X1,U;K,0", "Q2,,,,1"])
        self.assertEqual(rotulos[0], RotuloFolha("Q1", "X1", ("U", "K"), False))
        self.assertTrue(rotulos[1].fora)
        self.assertEqual(rotulos[1].alvos, ())

    def teste_problemas_juntos(self) -> None:
        """Questão inexistente, tema inexistente e fora com tema aparecem na mesma mensagem."""
        contexto: unittest.case._AssertRaisesContext[ErroFolha]
        with self.assertRaises(ErroFolha) as contexto:
            self._ler(["Q9,X1,,,0", "Q1,ZZ,,,0", "Q2,U,,,1"])
        mensagem: str = str(contexto.exception)
        self.assertIn("Q9: questão inexistente", mensagem)
        self.assertIn("Q1: tema ZZ inexistente", mensagem)
        self.assertIn("Q2: fora da taxonomia com tema central", mensagem)


class TesteValidacaoCruzada(unittest.TestCase):
    """Partições determinísticas, disjuntas, completas e estratificadas."""

    def setUp(self) -> None:
        """Estratos desbalanceados, como na folha (poucos "fora")."""
        self.estratos: list[str] = ["Penal"] * 40 + ["Processo Penal"] * 30 + ["Criminologia"] * 22 + ["fora"] * 8
        self.validacao: ValidacaoCruzadaRepetida = ValidacaoCruzadaRepetida(5, 3, 7)

    def teste_cada_exemplo_cai_em_teste_uma_vez_por_repeticao(self) -> None:
        """Em cada repetição, os testes cobrem todos os índices sem repetir, e treino e teste são disjuntos."""
        particoes: list[Particao] = self.validacao.particoes(self.estratos)
        self.assertEqual(len(particoes), 15)
        repeticao: int
        for repeticao in range(3):
            testes: list[int] = [i for p in particoes if p.repeticao == repeticao for i in p.teste]
            self.assertEqual(sorted(testes), list(range(100)))
        particao: Particao
        for particao in particoes:
            self.assertFalse(set(particao.treino) & set(particao.teste))

    def teste_estratificacao_e_determinismo(self) -> None:
        """Cada parte tem 1 ou 2 "fora" (8 em 5 partes), e a mesma semente dá as mesmas partições."""
        particoes: list[Particao] = self.validacao.particoes(self.estratos)
        particao: Particao
        for particao in particoes:
            contagem: Counter[str] = Counter(self.estratos[i] for i in particao.teste)
            self.assertIn(contagem["fora"], {1, 2})
        self.assertEqual(particoes, self.validacao.particoes(self.estratos))


class TesteAUC(unittest.TestCase):
    """AUC por Mann-Whitney, com empates."""

    def teste_casos_extremos(self) -> None:
        """Separação perfeita, invertida, empate total e classe vazia."""
        self.assertEqual(MetricasBinarias.auc([0.9, 0.8, 0.1], [True, True, False]), 1.0)
        self.assertEqual(MetricasBinarias.auc([0.1, 0.2, 0.9], [True, True, False]), 0.0)
        self.assertEqual(MetricasBinarias.auc([0.5, 0.5], [True, False]), 0.5)
        self.assertEqual(MetricasBinarias.auc([0.5, 0.7], [False, False]), 0.5)


if __name__ == "__main__":
    unittest.main()
