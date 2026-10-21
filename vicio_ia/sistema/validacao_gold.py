"""Medida secundária com o gold manual do autor (ADR-024, decisão 6), separada da folha-verdade.

O gold da etapa 1 tem 60 questões rotuladas à mão pelo autor: 14 estão na folha (servem para medir a diferença de
convenção entre o autor e a equipe) e 46 estão entre as 559 avaliadas (servem de checagem independente da
entrega). O gold não entra no treino nem na calibração: só confere o ``publicacao.csv`` já gravado.
"""

from __future__ import annotations

import csv
from collections.abc import Mapping
from pathlib import Path
from typing import ClassVar, TextIO

from vicio_ia.configuracao import Caminhos
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.sistema.folha import ReguaEtapa2, RotuloFolha


class ValidacaoGold:
    """Confere a entrega contra o gold e grava ``saidas/etapa2/gold_secundario.md``."""

    FAIXAS: ClassVar[tuple[tuple[float, float], ...]] = ((0.0, 0.8), (0.8, 0.9), (0.9, 0.95), (0.95, 1.01))

    def __init__(self, caminhos: Caminhos | None = None) -> None:
        """Guarda os caminhos.

        Args:
            caminhos: Caminhos do projeto.
        """
        self._caminhos: Caminhos = caminhos or Caminhos.padrao()

    @staticmethod
    def _ler(arquivo: Path) -> list[dict[str, str]]:
        """Lê um CSV.

        Args:
            arquivo: CSV.

        Returns:
            Linhas.
        """
        entrada: TextIO
        with arquivo.open(encoding="utf-8", newline="") as entrada:
            return list(csv.DictReader(entrada))

    def executar(self) -> Path:
        """Mede e grava o relatório.

        Returns:
            Caminho do relatório.
        """
        temas: list[TemaPreparado] = LeitorPreparados(self._caminhos).temas()
        regua: ReguaEtapa2 = ReguaEtapa2(temas)
        folha: dict[str, RotuloFolha] = {}
        linha: dict[str, str]
        for linha in self._ler(self._caminhos.folha_verdade):
            fora_folha: bool = linha["fora_da_taxonomia"] == "1"
            folha[linha["id"]] = RotuloFolha(
                linha["id"],
                "" if fora_folha else linha["tema_central_id"],
                tuple(e for e in linha["extras_ids"].split(";") if e),
                fora_folha,
            )
        gold: dict[str, RotuloFolha] = {}
        for linha in self._ler(self._caminhos.dados_gold / "rotulos_leva1.csv"):
            fora_gold: bool = linha["fora"] == "s"
            gold[linha["id"]] = RotuloFolha(
                linha["id"],
                "" if fora_gold else linha["tema_id"],
                () if fora_gold else tuple(a for a in linha["alternativos"].split(";") if a),
                fora_gold,
            )
        entrega: dict[str, dict[str, str]] = {
            linha["id"]: linha for linha in self._ler(self._caminhos.entregaveis / "publicacao.csv")
        }
        return self._gravar(gold, folha, entrega, regua)

    def _gravar(
        self,
        gold: Mapping[str, RotuloFolha],
        folha: Mapping[str, RotuloFolha],
        entrega: Mapping[str, Mapping[str, str]],
        regua: ReguaEtapa2,
    ) -> Path:
        """Calcula as medidas e grava o relatório.

        Args:
            gold: Rótulos do autor.
            folha: Rótulos da equipe.
            entrega: Linhas do ``publicacao.csv``.
            regua: Régua da etapa 2.

        Returns:
            Caminho do relatório.
        """
        comuns: list[str] = sorted(i for i in gold if i in folha)
        concordam: int = sum(
            1
            for i in comuns
            if (gold[i].fora and folha[i].fora)
            or (not gold[i].fora and regua.acerta(gold[i].tema_central_id, folha[i]))
        )
        avaliadas: list[str] = sorted(i for i in gold if i not in folha)

        def certo(questao: str) -> bool:
            """Diz se o tema da entrega está certo pela régua, com o rótulo do autor.

            Args:
                questao: ID.

            Returns:
                ``True`` se certo.
            """
            tema: str = entrega[questao]["tema_central_id"]
            return bool(tema) and not gold[questao].fora and regua.acerta(tema, gold[questao])

        publicadas: list[str] = [i for i in avaliadas if entrega[i]["decisao"] == "publicar"]
        linhas: list[str] = [
            "# Medida secundária: gold manual do autor (ADR-024)",
            "",
            (
                "O gold da etapa 1 foi rotulado à mão pelo autor, sem LLM. Ele não entra no treino nem na calibração: só "
                "confere o `relatorio/publicacao.csv` já gravado, com a régua da etapa 2."
            ),
            "",
            (
                f"- **Convenção (14 questões na folha):** o tema do autor acerta pela régua da equipe em {concordam} de "
                f"{len(comuns)}."
            ),
            (
                f"- **Tema sugerido certo nas {len(avaliadas)} avaliadas do gold:** "
                f"{sum(1 for i in avaliadas if certo(i))} de {len(avaliadas)} "
                f"(questões fora no gold: {sum(1 for i in avaliadas if gold[i].fora)})."
            ),
            (
                f"- **Publicadas entre elas:** {len(publicadas)}, das quais {sum(1 for i in publicadas if certo(i))} "
                "certas."
            ),
            "",
            "| Confiança | Questões | Certas | Confiança média |",
            "|---|---:|---:|---:|",
        ]
        baixo: float
        alto: float
        for baixo, alto in self.FAIXAS:
            faixa: list[str] = [
                i
                for i in avaliadas
                if entrega[i]["decisao"] != "fora" and baixo <= float(entrega[i]["confianca"]) < alto
            ]
            media: float = sum(float(entrega[i]["confianca"]) for i in faixa) / len(faixa) if faixa else 0.0
            linhas.append(
                f"| {baixo:.2f}–{min(alto, 1.0):.2f} | {len(faixa)} | {sum(1 for i in faixa if certo(i))} | {media:.3f} |"
            )
        linhas.append("")
        pasta: Path = self._caminhos.saida_etapa2
        pasta.mkdir(parents=True, exist_ok=True)
        destino: Path = pasta / "gold_secundario.md"
        destino.write_text("\n".join(linhas), encoding="utf-8")
        print(
            f"Gold (medida secundária): {len(publicadas)} publicadas nas {len(avaliadas)} avaliadas. Relatório: {destino}"
        )
        return destino
