"""Sistema da etapa 2 (ADR-022, ADR-023, ADR-025): escolha do nó, regras de fora, calibração, limiar e determinismo."""

from __future__ import annotations

import unittest
from typing import ClassVar, cast

import numpy as np

from vicio_ia.configuracao import ConfigRanqueador
from vicio_ia.estatistica import Matriz
from vicio_ia.sistema.pares import GeradorPares, ParesQuestao
from vicio_ia.sistema.politica import Calibrador, EscolhaQuestao, EscolhedorNo, EstimadorLimiar, Previsao, RegrasFora
from vicio_ia.sistema.ranqueador import criar_modelo


class GeradorFalso:
    """Ramos da árvore sintética (T com filhos X1 e X2; U e L soltos) e concordância fixa."""

    RAMOS: ClassVar[dict[str, frozenset[str]]] = {
        "T": frozenset({"T", "X1", "X2"}),
        "X1": frozenset({"X1", "T"}),
        "X2": frozenset({"X2", "T"}),
        "U": frozenset({"U"}),
        "L": frozenset({"L"}),
    }

    def ramo(self, tema_id: str) -> frozenset[str]:
        """Ramo do tema.

        Args:
            tema_id: Tema.

        Returns:
            IDs do ramo.
        """
        return self.RAMOS[tema_id]

    def concordancia(self, questao_id: str, tema_id: str) -> bool:
        """Concordância fixa.

        Args:
            questao_id: Ignorado.
            tema_id: Tema.

        Returns:
            ``True`` só para T.
        """
        return tema_id == "T"


class TesteEscolhaNo(unittest.TestCase):
    """O nó é o de maior P; os extras são de outro ramo, acima do limiar e no máximo três."""

    def setUp(self) -> None:
        """Escolhedor sobre o gerador falso."""
        self.escolhedor: EscolhedorNo = EscolhedorNo(cast(GeradorPares, GeradorFalso()), 0.5, 1)
        self.pares: ParesQuestao = ParesQuestao("Q1", ("X1", "T", "U", "L"), np.zeros((4, 1)))

    def teste_pai_vence_quando_tem_mais_chance(self) -> None:
        """Com o pai mais provável que o filho, publica-se o pai (o recuo da ADR-010)."""
        escolha: EscolhaQuestao = self.escolhedor.escolher(self.pares, np.array([0.6, 0.9, 0.7, 0.55]))
        self.assertEqual(escolha.tema, "T")
        self.assertTrue(escolha.concorda)
        self.assertEqual(escolha.extras, ("U",))
        self.assertEqual(escolha.alternativa, "U")

    def teste_extra_nao_repete_o_ramo(self) -> None:
        """X1 escolhido: T (mesmo ramo) não vira extra; U abaixo do limiar também não."""
        escolha: EscolhaQuestao = self.escolhedor.escolher(self.pares, np.array([0.9, 0.8, 0.4, 0.3]))
        self.assertEqual(escolha.tema, "X1")
        self.assertEqual(escolha.extras, ())
        self.assertEqual(escolha.alternativa, "U")


class TesteRegrasFora(unittest.TestCase):
    """Direito militar sempre vai para fora; a proximidade com tema inativo usa o percentil da folha."""

    def teste_regras(self) -> None:
        """Disciplinas militares e o corte do inativo."""
        self.assertTrue(RegrasFora.militar("Direito Penal Militar"))
        self.assertTrue(RegrasFora.militar("Direito Processual Penal Militar"))
        self.assertFalse(RegrasFora.militar("Direito Penal"))
        corte: float = RegrasFora.limiar_da_folha([float(v) for v in range(11)], 0.9)
        self.assertAlmostEqual(corte, 9.0)
        regras: RegrasFora = RegrasFora(corte)
        self.assertTrue(regras.inativo(9.5))
        self.assertFalse(regras.inativo(9.0))


class TesteCalibracaoELimiar(unittest.TestCase):
    """A calibração escolhida é uma das três; o limiar segue o critério e é determinístico."""

    def setUp(self) -> None:
        """Folha sintética bem calibrada: P alta acerta, P baixa erra."""
        gerador: np.random.Generator = np.random.default_rng(7)
        self.p: Matriz = np.clip(gerador.uniform(0.3, 0.999, size=100), 0.0, 1.0)
        self.y: Matriz = np.asarray(gerador.uniform(size=100) < self.p, dtype=np.float64)
        self.concorda: Matriz = np.asarray(self.p > 0.6, dtype=np.float64)

    def teste_calibrador(self) -> None:
        """O escolhido é um dos tipos, e a identidade devolve a própria P."""
        calibrador: Calibrador
        perdas: dict[str, float]
        calibrador, perdas = Calibrador.escolher(self.p, self.concorda, self.y, 5, 1)
        self.assertIn(calibrador.tipo, Calibrador.TIPOS)
        self.assertEqual(set(perdas), set(Calibrador.TIPOS))
        identidade: Calibrador = Calibrador("identidade")
        self.assertTrue(np.array_equal(identidade.aplicar(self.p, self.concorda), self.p))
        platt: Calibrador = Calibrador.ajustar("platt", self.p, self.concorda, self.y)
        calibradas: Matriz = platt.aplicar(np.array([0.5, 0.9]), np.array([0.0, 0.0]))
        self.assertLess(calibradas[0], calibradas[1])

    def _estimar(self, criterio: str) -> Previsao:
        """Roda o estimador nas avaliadas sintéticas.

        Args:
            criterio: ``reserva`` ou ``percentil``.

        Returns:
            Previsão.
        """
        avaliadas: Matriz = np.linspace(0.999, 0.5, 200)
        return EstimadorLimiar(self.p, self.concorda, self.y, Calibrador("identidade"), 300, 3).estimar(
            avaliadas, np.zeros(200), 0.95, 0.10, 0.97, 200, 40, 10, criterio
        )

    def teste_limiar_reserva_e_determinismo(self) -> None:
        """Na reserva, o ponto do modelo no corte é ≥ 97%; rodar de novo dá o mesmo corte e os mesmos números."""
        primeira: Previsao = self._estimar("reserva")
        self.assertEqual(primeira.regra, "reserva pontual")
        self.assertGreaterEqual(primeira.modelo, 0.97)
        self.assertGreater(primeira.publicadas, 0)
        self.assertGreaterEqual(primeira.publicadas, primeira.publicadas_estrito)
        self.assertEqual(primeira, self._estimar("reserva"))

    def teste_estrito_publica_menos(self) -> None:
        """O critério do percentil nunca publica mais que a reserva."""
        self.assertLessEqual(self._estimar("percentil").publicadas, self._estimar("reserva").publicadas)


class TesteModelosPares(unittest.TestCase):
    """O ranqueador é criado pela configuração, e o boosting é determinístico."""

    def teste_criar_e_determinismo(self) -> None:
        """Logística e boosting separam um padrão simples; o boosting dá a mesma saída em dois ajustes."""
        gerador: np.random.Generator = np.random.default_rng(3)
        x: Matriz = gerador.normal(size=(300, 3))
        y: Matriz = np.asarray(x[:, 0] + 0.2 * gerador.normal(size=300) > 0, dtype=np.float64)
        config: ConfigRanqueador
        for config in (ConfigRanqueador("logistica"), ConfigRanqueador("boosting", profundidade=2, iteracoes=50)):
            previsto: Matriz = criar_modelo(config).ajustar(x, y).prever(x)
            self.assertGreater(float(np.mean((previsto > 0.5) == (y > 0.5))), 0.85)
            self.assertTrue(np.array_equal(previsto, criar_modelo(config).ajustar(x, y).prever(x)))
        self.assertIsNone(criar_modelo(ConfigRanqueador("boosting")).coeficientes)
        with self.assertRaises(ValueError):
            criar_modelo(ConfigRanqueador("outro"))
