"""Orquestração do gold set (ADR-012): sorteio, planilha, caderno e situação da rotulagem."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from pathlib import Path

from vicio_ia.avaliacao.amostragem import AmostradorGold, ArquivoAmostra, ItemAmostra
from vicio_ia.avaliacao.planilha import CadernoRotulagem, PlanilhaRotulos, RotuloGold, SituacaoLinha
from vicio_ia.configuracao import Caminhos, ParametrosEDA, ParametrosGold
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada


class PipelineGold:
    """Prepara e acompanha o gold set.

    Saídas em ``dados/gold/``:

    * ``amostra_leva1.csv``: questões sorteadas, estrato e probabilidade de inclusão. Se já
      existir, é mantida (e o sorteio atual é só conferido contra ela);
    * ``rotulos_leva1.csv``: planilha de rótulos; criada vazia se não existir, **nunca sobrescrita**;
    * ``caderno_leva1.md``: as questões na ordem de rotulagem, só com o texto canônico.
    """

    def __init__(
        self,
        caminhos: Caminhos | None = None,
        parametros: ParametrosGold | None = None,
        parametros_eda: ParametrosEDA | None = None,
    ) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto (opcional).
            parametros: Parâmetros do gold set (opcional).
            parametros_eda: Parâmetros da EDA, para o mapa de disciplinas (opcional).
        """
        self._caminhos: Caminhos = caminhos if caminhos is not None else Caminhos.padrao()
        self._parametros: ParametrosGold = parametros if parametros is not None else ParametrosGold()
        self._parametros_eda: ParametrosEDA = parametros_eda if parametros_eda is not None else ParametrosEDA()

    def executar(self) -> list[SituacaoLinha]:
        """Sorteia (ou reaproveita) a amostra, garante a planilha, grava o caderno e mostra a situação.

        Returns:
            Situação de cada linha da planilha.
        """
        leitor: LeitorPreparados = LeitorPreparados(self._caminhos)
        questoes: list[QuestaoPreparada] = leitor.questoes()
        temas: list[TemaPreparado] = leitor.temas()
        amostrador: AmostradorGold = AmostradorGold(self._parametros, self._parametros_eda)
        amostra: list[ItemAmostra] = self._amostra(amostrador, questoes)
        return self._processar(amostra, questoes, temas)

    def _processar(
        self, amostra: Sequence[ItemAmostra], questoes: Sequence[QuestaoPreparada], temas: Sequence[TemaPreparado]
    ) -> list[SituacaoLinha]:
        """Garante a planilha, grava o caderno e mostra a situação do gold set.

        Args:
            amostra: Itens sorteados.
            questoes: Questões preparadas.
            temas: Árvore preparada.

        Returns:
            Situação de cada linha da planilha.
        """
        pasta: Path = self._caminhos.dados_gold
        planilha: PlanilhaRotulos = PlanilhaRotulos(pasta / "rotulos_leva1.csv", self._parametros, temas)
        acrescentadas: int = planilha.garantir(amostra)
        rotulos: list[RotuloGold] = planilha.ler()
        situacoes: list[SituacaoLinha] = planilha.validar(rotulos)
        caderno: Path = CadernoRotulagem().escrever(
            pasta / "caderno_leva1.md",
            amostra,
            {questao.id: questao for questao in questoes},
            {rotulo.id: rotulo for rotulo in rotulos},
        )
        self._imprimir(amostra, situacoes, planilha.caminho, caderno, acrescentadas)
        return situacoes

    def _amostra(self, amostrador: AmostradorGold, questoes: Sequence[QuestaoPreparada]) -> list[ItemAmostra]:
        """Sorteia a amostra do gold, ou reaproveita a gravada.

        Args:
            amostrador: Amostrador configurado.
            questoes: Questões preparadas.

        Returns:
            Itens na ordem de rotulagem.
        """
        arquivo: ArquivoAmostra = ArquivoAmostra(self._caminhos.dados_gold / "amostra_leva1.csv")
        sorteio: list[ItemAmostra] = amostrador.sortear(questoes)
        if not arquivo.existe():
            arquivo.gravar(sorteio)
            print(f"Amostra do gold sorteada (semente {self._parametros.semente}): {arquivo.caminho}")
            return sorteio
        gravada: list[ItemAmostra] = arquivo.ler()
        if [item.id for item in gravada] != [item.id for item in sorteio]:
            print(
                "AVISO: a amostra gravada difere do sorteio atual (dados ou parâmetros mudaram). "
                "Mantida a gravada, porque pode já ter rótulos."
            )
        return gravada

    @staticmethod
    def _imprimir(
        amostra: Sequence[ItemAmostra],
        situacoes: Sequence[SituacaoLinha],
        planilha: Path,
        caderno: Path,
        acrescentadas: int,
    ) -> None:
        """Mostra os estratos e a situação da rotulagem.

        Args:
            amostra: Itens sorteados.
            situacoes: Situação de cada linha da planilha.
            planilha: Caminho da planilha.
            caderno: Caminho do caderno.
            acrescentadas: Linhas novas acrescentadas à planilha nesta execução.
        """
        print("\nEstratos do gold set (sorteadas / população):")
        vistos: dict[str, tuple[int, int]] = {}
        item: ItemAmostra
        for item in amostra:
            vistos[item.estrato] = (item.sorteadas_estrato, item.tamanho_estrato)
        estrato: str
        for estrato in sorted(vistos):
            print(f"  {estrato:<55} {vistos[estrato][0]:>3} / {vistos[estrato][1]:>3}")

        contagem: Counter[str] = Counter(situacao.situacao for situacao in situacoes)
        rotuladas: list[RotuloGold] = [s.rotulo for s in situacoes if s.situacao == "rotulada"]
        minutos: float = sum(rotulo.minutos or 0.0 for rotulo in rotuladas)
        certezas: Counter[str] = Counter(rotulo.certeza for rotulo in rotuladas)
        print(
            f"\nRotulagem do gold set: {contagem['rotulada']}/{len(amostra)} rotuladas, {contagem['pendente']} pendentes, "
            f"{contagem['invalida']} inválidas"
            + (f" ({acrescentadas} linhas novas na planilha)" if acrescentadas else "")
        )
        if rotuladas:
            print(
                f"  fora: {sum(1 for r in rotuladas if r.fora)} · multitema: {sum(1 for r in rotuladas if r.multitema)}"
                f" · com alternativos: {sum(1 for r in rotuladas if r.alternativos)}"
                f" · certeza: {', '.join(f'{nivel} {n}' for nivel, n in sorted(certezas.items()))}"
            )
            print(f"  tempo: {minutos:.0f} min no total, {minutos / len(rotuladas):.1f} min por questão")
        situacao: SituacaoLinha
        for situacao in situacoes:
            if situacao.situacao == "invalida":
                print(f"  INVÁLIDA {situacao.rotulo.id}: {'; '.join(situacao.problemas)}")
        print(f"\nPlanilha: {planilha}\nCaderno:  {caderno}")
        print("Para rotular: uv run python executar_rotulagem.py")
