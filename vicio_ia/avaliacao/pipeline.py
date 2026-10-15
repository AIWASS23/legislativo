"""Orquestração do gold set (ADR-012): sorteio, planilha, caderno e situação da rotulagem, levas 1 e 2."""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Sequence
from pathlib import Path

from vicio_ia.avaliacao.amostragem import AmostradorGold, ArquivoAmostra, CandidatoLeva2, ItemAmostra
from vicio_ia.avaliacao.planilha import CadernoRotulagem, PlanilhaRotulos, RotuloGold, SituacaoLinha
from vicio_ia.configuracao import Caminhos, ParametrosEDA, ParametrosGold
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada


class PipelineGold:
    """Prepara e acompanha a leva 1 do gold set.

    Saídas em ``dados/gold/``:

    * ``amostra_leva1.csv``: questões sorteadas, estrato e probabilidade de inclusão. Se já
      existir, é mantida (e o sorteio atual é só conferido contra ela);
    * ``rotulos_leva1.csv``: planilha de rótulos; criada vazia se não existir, **nunca sobrescrita**;
    * ``caderno_leva1.md``: as questões na ordem de rotulagem, só com o texto canônico.

    A leva 2 (``amostra_leva2.csv``, ``rotulos_leva2.csv``, ``caderno_leva2.md``) só é sorteada com
    ``ParametrosGold.leva2_liberada`` ligado (depois do congelamento de prompts e regras) e com as
    probabilidades calibradas gravadas pelo passo 07 (``dados/decisao/probabilidades.json``).
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
        """Sorteia (ou reaproveita) a leva 1, garante a planilha, grava o caderno e mostra a situação.

        Returns:
            Situação de cada linha da planilha.
        """
        leitor: LeitorPreparados = LeitorPreparados(self._caminhos)
        questoes: list[QuestaoPreparada] = leitor.questoes()
        temas: list[TemaPreparado] = leitor.temas()
        amostrador: AmostradorGold = AmostradorGold(self._parametros, self._parametros_eda)
        amostra: list[ItemAmostra] = self._amostra_leva1(amostrador, questoes)
        situacoes: list[SituacaoLinha] = self._processar(1, amostra, questoes, temas)
        segunda: list[ItemAmostra] = self._amostra_leva2(amostrador, {item.id for item in amostra})
        if segunda:
            situacoes = situacoes + self._processar(2, segunda, questoes, temas)
        return situacoes

    def _processar(
        self,
        leva: int,
        amostra: Sequence[ItemAmostra],
        questoes: Sequence[QuestaoPreparada],
        temas: Sequence[TemaPreparado],
    ) -> list[SituacaoLinha]:
        """Garante a planilha, grava o caderno e mostra a situação de uma leva.

        Args:
            leva: Número da leva.
            amostra: Itens da leva.
            questoes: Questões preparadas.
            temas: Árvore preparada.

        Returns:
            Situação de cada linha da planilha da leva.
        """
        pasta: Path = self._caminhos.dados_gold
        planilha: PlanilhaRotulos = PlanilhaRotulos(pasta / f"rotulos_leva{leva}.csv", self._parametros, temas)
        acrescentadas: int = planilha.garantir(amostra)
        rotulos: list[RotuloGold] = planilha.ler()
        situacoes: list[SituacaoLinha] = planilha.validar(rotulos)
        caderno: Path = CadernoRotulagem().escrever(
            pasta / f"caderno_leva{leva}.md",
            leva,
            amostra,
            {questao.id: questao for questao in questoes},
            {rotulo.id: rotulo for rotulo in rotulos},
        )
        self._imprimir(leva, amostra, situacoes, planilha.caminho, caderno, acrescentadas)
        return situacoes

    def _amostra_leva2(self, amostrador: AmostradorGold, leva1: set[str]) -> list[ItemAmostra]:
        """Reaproveita a leva 2 gravada ou, se liberada, sorteia pelas probabilidades calibradas.

        Args:
            amostrador: Amostrador configurado.
            leva1: IDs da leva 1 (não se repetem).

        Returns:
            Itens da leva 2, ou vazio se ela não existe nem foi liberada.
        """
        arquivo: ArquivoAmostra = ArquivoAmostra(self._caminhos.dados_gold / "amostra_leva2.csv")
        if arquivo.existe():
            return arquivo.ler()
        origem: Path = self._caminhos.raiz / "dados" / "decisao" / "probabilidades.json"
        if not self._parametros.leva2_liberada:
            print("\nLeva 2: bloqueada até o congelamento (ParametrosGold.leva2_liberada = False).")
            return []
        if not origem.is_file():
            print(f"\nLeva 2: liberada, mas falta {origem}; rode antes `uv run python executar_decisao.py`.")
            return []
        conteudo: object = json.loads(origem.read_text(encoding="utf-8"))
        if not isinstance(conteudo, dict):
            return []
        limiar: object = conteudo.get("limiar")
        brutas: object = conteudo.get("candidatas")
        if not isinstance(limiar, (int, float)) or not isinstance(brutas, dict):
            return []
        candidatos: list[CandidatoLeva2] = [
            CandidatoLeva2(str(i), float(v)) for i, v in brutas.items() if isinstance(v, (int, float))
        ]
        sorteio: list[ItemAmostra] = amostrador.leva2(candidatos, float(limiar), frozenset(leva1))
        arquivo.gravar(sorteio)
        print(f"\nAmostra da leva 2 sorteada (limiar {float(limiar):.3f}): {arquivo.caminho}")
        return sorteio

    def _amostra_leva1(self, amostrador: AmostradorGold, questoes: Sequence[QuestaoPreparada]) -> list[ItemAmostra]:
        """Sorteia a leva 1, ou reaproveita a gravada.

        Args:
            amostrador: Amostrador configurado.
            questoes: Questões preparadas.

        Returns:
            Itens da leva 1 na ordem de rotulagem.
        """
        arquivo: ArquivoAmostra = ArquivoAmostra(self._caminhos.dados_gold / "amostra_leva1.csv")
        sorteio: list[ItemAmostra] = amostrador.leva1(questoes)
        if not arquivo.existe():
            arquivo.gravar(sorteio)
            print(f"Amostra da leva 1 sorteada (semente {self._parametros.semente}): {arquivo.caminho}")
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
        leva: int,
        amostra: Sequence[ItemAmostra],
        situacoes: Sequence[SituacaoLinha],
        planilha: Path,
        caderno: Path,
        acrescentadas: int,
    ) -> None:
        """Mostra os estratos e a situação da rotulagem.

        Args:
            leva: Número da leva.
            amostra: Itens da leva.
            situacoes: Situação de cada linha da planilha.
            planilha: Caminho da planilha.
            caderno: Caminho do caderno.
            acrescentadas: Linhas novas acrescentadas à planilha nesta execução.
        """
        print(f"\nEstratos da leva {leva} (sorteadas / população):")
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
            f"\nRotulagem da leva {leva}: {contagem['rotulada']}/{len(amostra)} rotuladas, {contagem['pendente']} pendentes, "
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
