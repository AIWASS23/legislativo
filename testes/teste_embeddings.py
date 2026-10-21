"""Embeddings (ADR-021): cache por conteúdo, prefixos, artefato em disco, E8 e kNN, com provedor falso."""

from __future__ import annotations

import hashlib
import tempfile
import unittest
from collections.abc import Sequence
from pathlib import Path
from typing import ClassVar

import numpy as np

from testes.fabrica import FabricaTestes
from vicio_ia.configuracao import Caminhos, ModeloEmbedding, ParametrosLLM
from vicio_ia.enriquecimento.embeddings import GeradorEmbeddings
from vicio_ia.estatistica import Matriz
from vicio_ia.llm.contratos import ErroProvedor
from vicio_ia.llm.embeddings import ProvedorEmbedding, RespostaEmbedding
from vicio_ia.llm.fabrica import FabricaProvedores
from vicio_ia.sistema.experimento_embeddings import CandidatoEmbedding, ExperimentoEmbeddings, ResultadoE8
from vicio_ia.sistema.folha import RotuloFolha
from vicio_ia.sistema.vetores import ArquivoVetores, ConjuntoVetores, ErroVetores, VetoresConhecimento


class ProvedorFalso(ProvedorEmbedding):
    """Vetor determinístico a partir do hash do texto; conta os textos recebidos."""

    nome: ClassVar[str] = "falso"
    descricao: ClassVar[str] = "Provedor de teste"

    def __init__(self) -> None:
        """Zera o contador."""
        self.recebidos: list[str] = []

    def embutir(self, textos: Sequence[str], modelo: str, contexto_tokens: int) -> RespostaEmbedding:
        """Gera vetores de 4 dimensões a partir do hash.

        Args:
            textos: Textos.
            modelo: Ignorado.
            contexto_tokens: Ignorado.

        Returns:
            Vetores (não normalizados, de propósito).
        """
        self.recebidos.extend(textos)
        vetores: list[tuple[float, ...]] = [
            tuple(float(b) + 1.0 for b in hashlib.sha256(t.encode("utf-8")).digest()[:4]) for t in textos
        ]
        return RespostaEmbedding(self.nome, modelo, tuple(vetores), 0, 0.0)

    def digest(self, modelo: str) -> str:
        """Digest fixo.

        Args:
            modelo: Ignorado.

        Returns:
            ``"d1"``.
        """
        return "d1"


class TesteGeradorEmbeddings(unittest.TestCase):
    """O cache evita recalcular; o prefixo de consulta só vale para consultas; a saída tem norma 1."""

    def teste_cache_prefixo_e_norma(self) -> None:
        """Segunda chamada não chama o provedor; repetidos no mesmo lote são calculados uma vez."""
        provedor: ProvedorFalso = ProvedorFalso()
        modelo: ModeloEmbedding = ModeloEmbedding("m", prefixo_consulta="query: ")
        pasta: str
        with tempfile.TemporaryDirectory() as pasta:
            gerador: GeradorEmbeddings = GeradorEmbeddings(provedor, modelo, Path(pasta), lote=2)
            primeira: Matriz = gerador.vetores(["a", "b", "a"], consulta=True)
            self.assertEqual(provedor.recebidos, ["query: a", "query: b"])
            self.assertTrue(np.allclose(np.linalg.norm(primeira, axis=1), 1.0))
            self.assertTrue(np.allclose(primeira[0], primeira[2]))
            gerador.vetores(["a"], consulta=False)
            self.assertEqual(provedor.recebidos[-1], "a")
            de_novo: GeradorEmbeddings = GeradorEmbeddings(provedor, modelo, Path(pasta), lote=2)
            segunda: Matriz = de_novo.vetores(["a", "b"], consulta=True)
            self.assertEqual(de_novo.calculados, 0)
            self.assertTrue(np.allclose(segunda, primeira[:2], atol=1e-6))


class TesteArquivoVetores(unittest.TestCase):
    """Gravar e ler devolve os mesmos IDs e vetores; ID ausente é erro."""

    def teste_ida_e_volta(self) -> None:
        """Os três conjuntos e o modelo voltam iguais (com a precisão de ``float32``)."""
        matriz: Matriz = ArquivoVetores.normalizar(np.array([[3.0, 4.0], [1.0, 0.0]], dtype=np.float64))
        vetores: VetoresConhecimento = VetoresConhecimento(
            "m",
            ConjuntoVetores(("Q1", "Q2"), matriz),
            ConjuntoVetores(("Q1:A",), matriz[:1]),
            ConjuntoVetores(("T",), matriz[1:]),
            ConjuntoVetores(("I",), matriz[:1]),
        )
        pasta: str
        with tempfile.TemporaryDirectory() as pasta:
            arquivo: ArquivoVetores = ArquivoVetores(Path(pasta))
            arquivo.gravar(vetores, {"modelo": "m"})
            lidos: VetoresConhecimento = arquivo.ler()
        self.assertEqual(lidos.modelo, "m")
        self.assertEqual(lidos.questoes.ids, ("Q1", "Q2"))
        self.assertTrue(np.allclose(lidos.questoes.submatriz(["Q2", "Q1"]), matriz[::-1], atol=1e-6))
        with self.assertRaises(ErroVetores):
            lidos.temas.submatriz(["X"])

    def teste_fabrica_conhece_so_ollama(self) -> None:
        """Provedor de embedding desconhecido é erro."""
        fabrica: FabricaProvedores = FabricaProvedores(Caminhos.padrao(), ParametrosLLM())
        with self.assertRaises(ErroProvedor):
            fabrica.obter_embedding("outro", 10)


class TesteExperimentoEmbeddings(unittest.TestCase):
    """E8 escolhe pela regra pré-registrada; o kNN não usa a própria questão."""

    IDS_TEMAS: ClassVar[tuple[str, ...]] = ("T", "X1", "X2", "U")

    def setUp(self) -> None:
        """Folha sintética: duas questões de X1, uma de U e uma fora."""
        self.folha: list[RotuloFolha] = [
            RotuloFolha("Q1", "X1", (), False),
            RotuloFolha("Q2", "X1", (), False),
            RotuloFolha("Q3", "U", (), False),
            RotuloFolha("Q4", "", (), True),
        ]
        self.experimento: ExperimentoEmbeddings = ExperimentoEmbeddings(
            FabricaTestes().temas(),
            self.folha,
            self.IDS_TEMAS,
            [np.zeros(len(self.IDS_TEMAS), dtype=np.float64) for _ in self.folha],
            (1, 5, 10),
            60,
            1,
        )

    @staticmethod
    def _base() -> Matriz:
        """Base ortonormal de 4 dimensões (um eixo por tema).

        Returns:
            Matriz identidade.
        """
        return np.eye(4, dtype=np.float64)

    def teste_vencedor_pelo_top1_no_empate_do_recall(self) -> None:
        """Com só 4 temas o recall@10 empata; vence quem acerta mais no top-1."""
        eixo: Matriz = self._base()
        bom: Matriz = np.array([eixo[1], eixo[1], eixo[3], eixo[0]], dtype=np.float64)
        ruim: Matriz = np.array([eixo[2], eixo[2], eixo[2], eixo[0]], dtype=np.float64)
        resultado: ResultadoE8 = self.experimento.medir(
            [CandidatoEmbedding("ruim", ruim, eixo, 0.0), CandidatoEmbedding("bom", bom, eixo, 0.0)]
        )
        self.assertEqual(resultado.vencedor, "bom")
        self.assertEqual(resultado.rankings_denso["bom"][0].primeiro_acerto, 1)

    def teste_knn_deixa_uma_fora(self) -> None:
        """Q1 tem como vizinho Q2 (mesmo tema), não a si mesma; Q3 só tem vizinhos de outro tema."""
        eixo: Matriz = self._base()
        questoes: Matriz = ArquivoVetores.normalizar(
            np.array([eixo[1] + 0.1 * eixo[0], eixo[1], eixo[3], eixo[2]], dtype=np.float64)
        )
        resultado: ResultadoE8 = self.experimento.medir([CandidatoEmbedding("m", questoes, eixo, 0.0)])
        top1: float = next(
            m.valor for m in resultado.metricas if m.variante == "m: kNN (k=1)" and m.nome == "acerto top-1 (100)"
        )
        self.assertAlmostEqual(top1, 2 / 4)
        teto: float = next(m.valor for m in resultado.metricas if m.variante == "teto")
        self.assertAlmostEqual(teto, 2 / 3)
