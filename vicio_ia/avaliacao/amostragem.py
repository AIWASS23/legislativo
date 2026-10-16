"""Sorteio das amostras do gold set (ADR-012), com probabilidades de inclusão registradas."""

from __future__ import annotations

import csv
import math
import random
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Literal, TextIO

from vicio_ia.configuracao import ParametrosEDA, ParametrosGold
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada

type EstratoLeva2 = Literal["publicacao", "fronteira"]
"""Estratos da leva 2: acima do limiar mais a fronteira, ou perto do limiar."""


class ErroAmostra(Exception):
    """Arquivo de amostra inválido, ou sorteio impossível com os parâmetros dados."""


@dataclass(frozen=True)
class ItemAmostra:
    """Uma questão sorteada para o gold set.

    Attributes:
        ordem: Posição na ordem de rotulagem (1, 2, ...); embaralhada para não rotular por estrato.
        id: ID da questão.
        leva: 1 (desenvolvimento) ou 2 (estimativa).
        estrato: Estrato do sorteio (``"Penal | multipla_escolha_5"``, ``"publicacao"``...).
        tamanho_estrato: Questões do estrato na população (``N_h``).
        sorteadas_estrato: Questões sorteadas no estrato (``n_h``).
        prob_inclusao: ``n_h / N_h``; o peso da questão nas estimativas é o inverso.
    """

    ordem: int
    id: str
    leva: int
    estrato: str
    tamanho_estrato: int
    sorteadas_estrato: int
    prob_inclusao: float


@dataclass(frozen=True)
class CandidatoLeva2:
    """Questão disponível para a leva 2, com a probabilidade calibrada de acerto (ADR-013).

    A probabilidade só serve para o sorteio; ela nunca aparece para quem rotula.

    Attributes:
        id: ID da questão.
        probabilidade: Probabilidade calibrada de a publicação estar certa.
    """

    id: str
    probabilidade: float


class AmostradorGold:
    """Sorteia as levas do gold set com semente fixa.

    * **Leva 1:** estratificada por disciplina de origem normalizada e formato, com alocação
      proporcional pelo método do maior resto. Questões duplicadas ficam fora (herdam o rótulo).
    * **Leva 2:** depois do congelamento; ``leva2_publicacao`` questões com ``P ≥ limiar`` (onde o
      pipeline publicaria) e ``leva2_fronteira`` com ``limiar - largura_fronteira ≤ P < limiar``, sem
      repetir a leva 1. Estrato menor que o pedido entra inteiro.
    """

    COLUNAS: ClassVar[tuple[str, ...]] = (
        "ordem",
        "id",
        "leva",
        "estrato",
        "tamanho_estrato",
        "sorteadas_estrato",
        "prob_inclusao",
    )

    def __init__(self, parametros: ParametrosGold, parametros_eda: ParametrosEDA) -> None:
        """Guarda os parâmetros do sorteio e o mapa de disciplinas de origem.

        Args:
            parametros: Parâmetros do gold set.
            parametros_eda: Parâmetros da EDA (mapa de disciplinas de origem).
        """
        self._parametros: ParametrosGold = parametros
        self._mapa_disciplinas: dict[str, str] = parametros_eda.mapa_disciplinas

    def estrato_leva1(self, questao: QuestaoPreparada) -> str:
        """Estrato da leva 1: disciplina de origem normalizada e formato.

        Args:
            questao: Questão preparada.

        Returns:
            Nome do estrato.
        """
        bruta: object = questao.original.get("disciplina_origem", "")
        disciplina: str = self._mapa_disciplinas.get(str(bruta).strip(), "") or self._parametros.rotulo_fora_do_recorte
        return f"{disciplina} | {questao.formato}"

    def leva1(self, questoes: Sequence[QuestaoPreparada]) -> list[ItemAmostra]:
        """Sorteia a leva 1.

        Args:
            questoes: Todas as questões preparadas.

        Returns:
            Itens na ordem de rotulagem.

        Raises:
            ErroAmostra: Se a amostra pedida for maior que a população.
        """
        estratos: dict[str, list[str]] = {}
        questao: QuestaoPreparada
        for questao in questoes:
            if questao.duplicata_de is None:
                estratos.setdefault(self.estrato_leva1(questao), []).append(questao.id)
        tamanho: int = self._parametros.tamanho_leva1
        alocacao: dict[str, int] = self._alocar(estratos, tamanho)
        return self._sortear(estratos, alocacao, 1, self._parametros.semente)

    def leva2(self, candidatos: Sequence[CandidatoLeva2], limiar: float, excluir: frozenset[str]) -> list[ItemAmostra]:
        """Sorteia a leva 2 nos estratos de publicação e de fronteira.

        Se um estrato tiver menos questões que o pedido, entram todas (probabilidade de
        inclusão 1) e um aviso é impresso.

        Args:
            candidatos: Questões com a probabilidade calibrada (depois do congelamento).
            limiar: Limiar de publicação escolhido (ADR-011).
            excluir: IDs já rotulados (leva 1).

        Returns:
            Itens na ordem de rotulagem.
        """
        largura: float = self._parametros.largura_fronteira
        estratos: dict[str, list[str]] = {"publicacao": [], "fronteira": []}
        candidato: CandidatoLeva2
        for candidato in candidatos:
            if candidato.id in excluir:
                continue
            if candidato.probabilidade >= limiar:
                estratos["publicacao"].append(candidato.id)
            elif candidato.probabilidade >= limiar - largura:
                estratos["fronteira"].append(candidato.id)
        pedidos: dict[str, int] = {
            "publicacao": self._parametros.leva2_publicacao,
            "fronteira": self._parametros.leva2_fronteira,
        }
        alocacao: dict[str, int] = {nome: min(pedido, len(estratos[nome])) for nome, pedido in pedidos.items()}
        nome: str
        for nome in sorted(pedidos):
            if alocacao[nome] < pedidos[nome]:
                print(
                    f"AVISO: leva 2, estrato {nome}: só {alocacao[nome]} questões (pedidas {pedidos[nome]}); entram todas"
                )
        return self._sortear(estratos, alocacao, 2, self._parametros.semente + 2)

    @staticmethod
    def _alocar(estratos: dict[str, list[str]], tamanho: int) -> dict[str, int]:
        """Aloca a amostra proporcionalmente pelo método do maior resto.

        Empates no resto são desfeitos pelo estrato maior e, depois, pelo nome,
        para o resultado não depender da ordem dos dados.

        Args:
            estratos: Estrato -> IDs da população.
            tamanho: Tamanho total da amostra.

        Returns:
            Estrato -> questões a sortear.

        Raises:
            ErroAmostra: Se ``tamanho`` for maior que a população.
        """
        populacao: int = sum(len(ids) for ids in estratos.values())
        if tamanho > populacao:
            raise ErroAmostra(f"amostra de {tamanho} maior que a população de {populacao}")
        cotas: dict[str, float] = {nome: tamanho * len(ids) / populacao for nome, ids in estratos.items()}
        alocacao: dict[str, int] = {nome: math.floor(cota) for nome, cota in cotas.items()}
        faltam: int = tamanho - sum(alocacao.values())
        ordem: list[str] = sorted(cotas, key=lambda nome: (-(cotas[nome] - alocacao[nome]), -len(estratos[nome]), nome))
        nome: str
        for nome in ordem[:faltam]:
            alocacao[nome] += 1
        return alocacao

    @staticmethod
    def _sortear(
        estratos: dict[str, list[str]], alocacao: dict[str, int], leva: int, semente: int
    ) -> list[ItemAmostra]:
        """Sorteia dentro de cada estrato e embaralha a ordem de rotulagem.

        Args:
            estratos: Estrato -> IDs da população.
            alocacao: Estrato -> questões a sortear.
            leva: Número da leva.
            semente: Semente do gerador.

        Returns:
            Itens numerados na ordem de rotulagem.
        """
        gerador: random.Random = random.Random(semente)
        sorteados: list[tuple[str, str]] = []
        nome: str
        for nome in sorted(estratos):
            populacao: list[str] = sorted(estratos[nome])
            questao_id: str
            for questao_id in gerador.sample(populacao, alocacao.get(nome, 0)):
                sorteados.append((questao_id, nome))
        gerador.shuffle(sorteados)
        itens: list[ItemAmostra] = []
        posicao: int
        par: tuple[str, str]
        for posicao, par in enumerate(sorteados, start=1):
            tamanho_estrato: int = len(estratos[par[1]])
            sorteadas: int = alocacao[par[1]]
            itens.append(
                ItemAmostra(
                    ordem=posicao,
                    id=par[0],
                    leva=leva,
                    estrato=par[1],
                    tamanho_estrato=tamanho_estrato,
                    sorteadas_estrato=sorteadas,
                    prob_inclusao=round(sorteadas / tamanho_estrato, 6),
                )
            )
        return itens


class ArquivoAmostra:
    """Grava e lê o CSV de uma amostra (``dados/gold/amostra_leva<N>.csv``)."""

    def __init__(self, caminho: Path) -> None:
        """Define o arquivo.

        Args:
            caminho: Caminho do CSV.
        """
        self._caminho: Path = caminho

    @property
    def caminho(self) -> Path:
        """Caminho do CSV."""
        return self._caminho

    def existe(self) -> bool:
        """Indica se o arquivo já foi gravado.

        Returns:
            ``True`` se existir.
        """
        return self._caminho.is_file()

    def gravar(self, itens: Sequence[ItemAmostra]) -> None:
        """Grava a amostra (sobrescreve: a amostra é derivada da semente, não é rótulo).

        Args:
            itens: Itens na ordem de rotulagem.
        """
        linhas: list[list[str | int]] = [
            [
                item.ordem,
                item.id,
                item.leva,
                item.estrato,
                item.tamanho_estrato,
                item.sorteadas_estrato,
                f"{item.prob_inclusao:.6f}",
            ]
            for item in itens
        ]
        self._caminho.parent.mkdir(parents=True, exist_ok=True)
        arquivo: TextIO
        with self._caminho.open("w", encoding="utf-8", newline="") as arquivo:
            csv.writer(arquivo).writerows([list(AmostradorGold.COLUNAS), *linhas])

    def ler(self) -> list[ItemAmostra]:
        """Lê a amostra gravada.

        Returns:
            Itens na ordem de rotulagem.

        Raises:
            ErroAmostra: Se faltar coluna ou algum valor for inválido.
        """
        itens: list[ItemAmostra] = []
        arquivo: TextIO
        with self._caminho.open(encoding="utf-8", newline="") as arquivo:
            leitor: csv.DictReader[str] = csv.DictReader(arquivo)
            faltantes: list[str] = [c for c in AmostradorGold.COLUNAS if c not in (leitor.fieldnames or [])]
            if faltantes:
                raise ErroAmostra(f"{self._caminho.name}: colunas ausentes {faltantes}")
            linha: dict[str, str]
            for linha in leitor:
                try:
                    itens.append(
                        ItemAmostra(
                            ordem=int(linha["ordem"]),
                            id=linha["id"].strip(),
                            leva=int(linha["leva"]),
                            estrato=linha["estrato"],
                            tamanho_estrato=int(linha["tamanho_estrato"]),
                            sorteadas_estrato=int(linha["sorteadas_estrato"]),
                            prob_inclusao=float(linha["prob_inclusao"]),
                        )
                    )
                except ValueError as erro:
                    raise ErroAmostra(f"{self._caminho.name}: linha inválida {linha}") from erro
        return itens
