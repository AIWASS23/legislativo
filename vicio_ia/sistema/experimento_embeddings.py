"""E8 (escolha do modelo de embedding) e E9 (kNN na folha) sobre vetores já gerados (ADR-021, ADR-024).

Nada aqui chama modelo: a fase de conhecimento gera os vetores de cada candidato e entrega as matrizes. Para
cada modelo são medidos, na folha-verdade e com a régua da etapa 2:

- **E8, denso:** a questão inteira contra os documentos de tema, pela similaridade do cosseno;
- **E8, fusão:** BM25 e denso combinados pela posição recíproca (RRF), sem parâmetro aprendido;
- **E9, kNN:** os vizinhos mais parecidos entre as outras 99 questões da folha votam nos seus temas
  (deixa-uma-fora, então é medido fora da amostra).

A regra de escolha foi pré-registrada: vence o maior recall@10 do denso nas 92 com tema; diferença de até uma
questão é empate, e o empate vai para o maior acerto no top-1.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from vicio_ia.estatistica import Matriz
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.sistema.folha import ReguaEtapa2, RotuloFolha
from vicio_ia.sistema.ranking import AvaliadorRanking, Metrica, RankingQuestao


@dataclass(frozen=True)
class CandidatoEmbedding:
    """Vetores de um modelo candidato, já recortados para o experimento.

    Attributes:
        modelo: Nome do modelo.
        questoes: Vetores das questões da folha, na ordem da folha (norma 1).
        temas: Vetores dos documentos de tema, na ordem de ``ids_temas`` (norma 1).
        segundos: Tempo para gerar todos os vetores do modelo (questões, alternativas e temas).
    """

    modelo: str
    questoes: Matriz
    temas: Matriz
    segundos: float


@dataclass(frozen=True)
class ResultadoE8:
    """Métricas do E8 e do E9 e o vencedor pela regra pré-registrada.

    Attributes:
        metricas: Todas as métricas.
        vencedor: Modelo escolhido pela regra.
        rankings_denso: Ranking denso por modelo, na ordem da folha.
    """

    metricas: tuple[Metrica, ...]
    vencedor: str
    rankings_denso: dict[str, tuple[RankingQuestao, ...]]


class ExperimentoEmbeddings:
    """Mede os candidatos de embedding na folha-verdade."""

    def __init__(
        self,
        temas: Sequence[TemaPreparado],
        folha: Sequence[RotuloFolha],
        ids_temas: Sequence[str],
        pontos_bm25: Sequence[Matriz],
        top_k: Sequence[int],
        rrf_k: int,
        vizinhos: int,
    ) -> None:
        """Guarda a base do experimento.

        Args:
            temas: Árvore preparada.
            folha: Rótulos da folha-verdade.
            ids_temas: Temas publicáveis, na ordem das colunas de pontuação.
            pontos_bm25: Pontuação BM25 de cada questão da folha contra os temas (a mesma do E7).
            top_k: Tamanhos de lista do recall.
            rrf_k: Constante da fusão por posição recíproca.
            vizinhos: Vizinhos do kNN.
        """
        self._folha: tuple[RotuloFolha, ...] = tuple(folha)
        self._ids_temas: tuple[str, ...] = tuple(ids_temas)
        self._pontos_bm25: tuple[Matriz, ...] = tuple(pontos_bm25)
        self._avaliador: AvaliadorRanking = AvaliadorRanking(temas, top_k)
        self._regua: ReguaEtapa2 = ReguaEtapa2(temas)
        self._rrf_k: int = rrf_k
        self._vizinhos: int = vizinhos

    def medir(self, candidatos: Sequence[CandidatoEmbedding]) -> ResultadoE8:
        """Roda o E8 e o E9 para todos os candidatos.

        Args:
            candidatos: Vetores de cada modelo.

        Returns:
            Métricas e vencedor.
        """
        metricas: list[Metrica] = [self._teto_knn()]
        rankings_denso: dict[str, tuple[RankingQuestao, ...]] = {}
        candidato: CandidatoEmbedding
        for candidato in candidatos:
            similaridade: Matriz = candidato.questoes @ candidato.temas.T
            denso: list[RankingQuestao] = [
                self._avaliador.ordenar(r, similaridade[i], self._ids_temas) for i, r in enumerate(self._folha)
            ]
            rankings_denso[candidato.modelo] = tuple(denso)
            metricas.extend(self._avaliador.metricas("E8", f"{candidato.modelo}: denso", self._folha, denso))
            fusao: list[RankingQuestao] = [
                self._avaliador.ordenar(r, self._rrf(self._pontos_bm25[i], similaridade[i]), self._ids_temas)
                for i, r in enumerate(self._folha)
            ]
            metricas.extend(
                self._avaliador.metricas("E8", f"{candidato.modelo}: BM25 + denso (RRF)", self._folha, fusao)
            )
            knn: list[RankingQuestao] = self._knn(candidato.questoes)
            metricas.extend(
                self._avaliador.metricas("E9", f"{candidato.modelo}: kNN (k={self._vizinhos})", self._folha, knn)
            )
            metricas.append(
                Metrica("E8", f"{candidato.modelo}: denso", "segundos para gerar os vetores", candidato.segundos)
            )
        return ResultadoE8(tuple(metricas), self._vencedor(metricas, candidatos), rankings_denso)

    def _rrf(self, bm25: Matriz, denso: Matriz) -> Matriz:
        """Fusão por posição recíproca: ``1/(k + posição no BM25) + 1/(k + posição no denso)``.

        Args:
            bm25: Pontuação BM25 de cada tema.
            denso: Similaridade de cada tema.

        Returns:
            Pontuação fundida.
        """
        posicoes: Matriz = np.zeros(len(self._ids_temas), dtype=np.float64)
        pontos: Matriz
        for pontos in (bm25, denso):
            ordem: npt.NDArray[np.intp] = np.argsort(-pontos, kind="stable")
            posicao: Matriz = np.empty(len(ordem), dtype=np.float64)
            posicao[ordem] = np.arange(1, len(ordem) + 1, dtype=np.float64)
            posicoes += 1.0 / (self._rrf_k + posicao)
        return posicoes

    def _knn(self, questoes: Matriz) -> list[RankingQuestao]:
        """kNN deixa-uma-fora: os vizinhos com tema votam no central e nos extras, com o peso da similaridade.

        Args:
            questoes: Vetores das questões da folha.

        Returns:
            Ranking de cada questão da folha.
        """
        coluna: dict[str, int] = {t: k for k, t in enumerate(self._ids_temas)}
        similaridade: Matriz = questoes @ questoes.T
        np.fill_diagonal(similaridade, -np.inf)
        rankings: list[RankingQuestao] = []
        indice: int
        rotulo: RotuloFolha
        for indice, rotulo in enumerate(self._folha):
            pontos: Matriz = np.zeros(len(self._ids_temas), dtype=np.float64)
            vizinho: int
            for vizinho in [int(v) for v in np.argsort(-similaridade[indice], kind="stable")[: self._vizinhos]]:
                alvo: str
                for alvo in self._folha[vizinho].alvos:
                    if alvo in coluna:
                        pontos[coluna[alvo]] += max(float(similaridade[indice, vizinho]), 0.0)
            rankings.append(self._avaliador.ordenar(rotulo, pontos, self._ids_temas))
        return rankings

    def _teto_knn(self) -> Metrica:
        """Teto do kNN: questões com tema cujo acerto aparece entre os temas de outra questão da folha.

        Returns:
            Métrica do E9.
        """
        com_tema: list[RotuloFolha] = [r for r in self._folha if not r.fora]
        cobertas: int = 0
        rotulo: RotuloFolha
        for rotulo in com_tema:
            outros: set[str] = {a for r in self._folha if r.id != rotulo.id for a in r.alvos}
            cobertas += any(self._regua.acerta(a, rotulo) for a in outros)
        return Metrica(
            "E9",
            "teto",
            "tema certo presente em outra questão da folha (92)",
            cobertas / len(com_tema),
            f"{cobertas}/{len(com_tema)}",
        )

    @staticmethod
    def _vencedor(metricas: Sequence[Metrica], candidatos: Sequence[CandidatoEmbedding]) -> str:
        """Aplica a regra pré-registrada: maior recall@10 do denso; até uma questão de diferença é empate.

        Args:
            metricas: Métricas medidas.
            candidatos: Candidatos, na ordem da configuração (desempate final).

        Returns:
            Nome do modelo vencedor.
        """

        def valor(modelo: str, nome: str) -> float:
            """Métrica do denso de um modelo.

            Args:
                modelo: Modelo.
                nome: Nome da métrica.

            Returns:
                Valor.
            """
            return next(m.valor for m in metricas if m.variante == f"{modelo}: denso" and m.nome == nome)

        nomes: list[str] = [c.modelo for c in candidatos]
        melhor_recall: float = max(valor(n, "recall@10 (92)") for n in nomes)
        empatados: list[str] = [n for n in nomes if valor(n, "recall@10 (92)") >= melhor_recall - 1.5 / 92]
        return max(empatados, key=lambda n: (valor(n, "acerto top-1 (92 com tema)"), -nomes.index(n)))
