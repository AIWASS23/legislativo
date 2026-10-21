"""Gráficos da etapa 2 (ADR-025): confiabilidade e precisão × cobertura, com a tabela equivalente.

Saídas em ``saidas/sistema/`` (PNG para o relatório e SVG):

* ``confiabilidade``: P(certo) calibrada fora da amostra × acerto observado na folha, em faixas de 20 questões,
  com intervalo de 90% (Jeffreys). As questões fora da taxonomia contam como erro, como na régua;
* ``precisao_cobertura``: a precisão observada fora da amostra na folha, ordenada pela confiança, e a precisão
  estimada pelo modelo nas 559 avaliadas (ponto e percentil 10), com o corte publicado e o corte estrito;
* ``graficos.md``: as mesmas informações em tabela.

Mesma paleta e mesmo estilo dos gráficos da etapa 1 (azul, laranja; referências em cinza). Não chama modelo.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import matplotlib

matplotlib.use("Agg")

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from vicio_ia.estatistica import Matriz
from vicio_ia.sistema.politica import Previsao


@dataclass(frozen=True)
class EstiloGraficos:
    """Cores e medidas dos gráficos (a paleta validada da etapa 1, modo claro).

    Attributes:
        superficie: Fundo.
        texto: Texto principal.
        texto_secundario: Rótulos, eixos e anotações.
        grade: Linhas de grade.
        referencia: Linhas de referência (meta de 95%, diagonal, cortes).
        series: Cores das séries: folha fora da amostra, estimativa nas 559.
    """

    superficie: str = "#fcfcfb"
    texto: str = "#0b0b0b"
    texto_secundario: str = "#52514e"
    grade: str = "#e6e5e1"
    referencia: str = "#8d8c86"
    series: tuple[str, str] = ("#2a78d6", "#eb6834")


class GraficosEtapa2:
    """Desenha os dois gráficos e grava a tabela equivalente."""

    POR_FAIXA: ClassVar[int] = 20
    SORTEIOS: ClassVar[int] = 20000

    def __init__(self, pasta: Path, alvo: float, semente: int, estilo: EstiloGraficos | None = None) -> None:
        """Define o destino e o estilo.

        Args:
            pasta: Pasta de saída (``saidas/sistema``).
            alvo: Precisão-alvo (0,95), desenhada como referência.
            semente: Semente dos sorteios dos intervalos.
            estilo: Cores e medidas.
        """
        self._pasta: Path = pasta
        self._alvo: float = alvo
        self._semente: int = semente
        self._estilo: EstiloGraficos = estilo or EstiloGraficos()

    def gerar(self, p_folha: Matriz, acerto_folha: Matriz, previsao: Previsao) -> Path:
        """Gera os gráficos e ``graficos.md``.

        Args:
            p_folha: P(certo) calibrada fora da amostra do nó escolhido, nas 100 da folha.
            acerto_folha: Acerto pela régua (0/1; as questões fora são 0).
            previsao: Previsão no limiar escolhido, com a curva do estimador do modelo.

        Returns:
            Caminho de ``graficos.md``.
        """
        self._pasta.mkdir(parents=True, exist_ok=True)
        faixas: list[tuple[int, float, float, float, float]] = self._confiabilidade(p_folha, acerto_folha)
        topo: list[tuple[int, float, float, float]] = self._precisao_cobertura(p_folha, acerto_folha, previsao)
        return self._tabela(faixas, topo, previsao)

    def _jeffreys(self, acertos: int, total: int) -> tuple[float, float]:
        """Intervalo de 90% de Jeffreys.

        Args:
            acertos: Acertos.
            total: Questões.

        Returns:
            Percentis 5 e 95.
        """
        gerador: np.random.Generator = np.random.default_rng(self._semente)
        sorteios: Matriz = gerador.beta(acertos + 0.5, total - acertos + 0.5, self.SORTEIOS)
        return float(np.percentile(sorteios, 5)), float(np.percentile(sorteios, 95))

    def _confiabilidade(self, p_folha: Matriz, acerto_folha: Matriz) -> list[tuple[int, float, float, float, float]]:
        """Gráfico de confiabilidade em faixas de ``POR_FAIXA`` questões, da menor para a maior P.

        Args:
            p_folha: P calibrada fora da amostra.
            acerto_folha: Acerto (0/1).

        Returns:
            ``(questões, P média, acerto observado, limite inferior, limite superior)`` por faixa.
        """
        ordem: list[int] = [int(i) for i in np.argsort(p_folha, kind="stable")]
        faixas: list[tuple[int, float, float, float, float]] = []
        inicio: int
        for inicio in range(0, len(ordem), self.POR_FAIXA):
            indices: list[int] = ordem[inicio : inicio + self.POR_FAIXA]
            acertos: int = int(acerto_folha[indices].sum())
            baixo: float
            alto: float
            baixo, alto = self._jeffreys(acertos, len(indices))
            faixas.append((len(indices), float(p_folha[indices].mean()), acertos / len(indices), baixo, alto))
        e: EstiloGraficos = self._estilo
        figura: Figure = Figure(figsize=(6.4, 5.2), dpi=150, facecolor=e.superficie)
        eixo: Axes = figura.add_subplot()
        self._preparar_eixo(eixo, "P(certo) prevista, fora da amostra", "Acerto observado na folha (régua da etapa 2)")
        eixo.plot([0.3, 1.0], [0.3, 1.0], color=e.referencia, linewidth=1, linestyle="--", zorder=1)
        faixa: tuple[int, float, float, float, float]
        for faixa in faixas:
            eixo.vlines(faixa[1], faixa[3], faixa[4], color=e.series[0], linewidth=2, alpha=0.45, zorder=2)
            eixo.plot(
                faixa[1],
                faixa[2],
                marker="o",
                color=e.series[0],
                markersize=8,
                markeredgecolor=e.superficie,
                markeredgewidth=2,
                zorder=3,
            )
            eixo.annotate(
                f"{faixa[2] * faixa[0]:.0f}/{faixa[0]}",
                (faixa[1], faixa[2]),
                xytext=(9, -4),
                textcoords="offset points",
                fontsize=9,
                color=e.texto,
            )
        eixo.set_xlim(0.3, 1.02)
        eixo.set_ylim(0.3, 1.02)
        eixo.set_title(
            "Confiabilidade: folha-verdade fora da amostra (faixas de 20)", loc="left", fontsize=11, color=e.texto
        )
        figura.text(
            0.01,
            0.01,
            "Pontos: acerto observado (fora da taxonomia conta como erro). Linhas: 90% (Jeffreys). Diagonal: P = acerto.",
            fontsize=7.5,
            color=e.texto_secundario,
        )
        self._gravar(figura, "confiabilidade")
        return faixas

    def _precisao_cobertura(
        self, p_folha: Matriz, acerto_folha: Matriz, previsao: Previsao
    ) -> list[tuple[int, float, float, float]]:
        """Precisão × cobertura: a folha fora da amostra e a estimativa do modelo nas 559.

        Args:
            p_folha: P calibrada fora da amostra.
            acerto_folha: Acerto (0/1).
            previsao: Previsão com a curva do estimador do modelo.

        Returns:
            ``(k, precisão observada no topo k, limite inferior, limite superior)`` da folha.
        """
        ordem: list[int] = [int(i) for i in np.argsort(-p_folha, kind="stable")]
        acumulado: Matriz = np.cumsum(acerto_folha[ordem])
        topo: list[tuple[int, float, float, float]] = []
        k: int
        for k in range(1, len(ordem) + 1):
            baixo: float
            alto: float
            baixo, alto = self._jeffreys(int(acumulado[k - 1]), k)
            topo.append((k, float(acumulado[k - 1]) / k, baixo, alto))
        e: EstiloGraficos = self._estilo
        figura: Figure = Figure(figsize=(6.8, 4.8), dpi=150, facecolor=e.superficie)
        eixo: Axes = figura.add_subplot()
        self._preparar_eixo(eixo, "Cobertura (fração publicada)", "Precisão")
        eixo.axhline(self._alvo, color=e.referencia, linewidth=1, linestyle="--", zorder=1)
        eixo.annotate(
            "meta: 95%",
            (0.0, self._alvo),
            xytext=(4, 3),
            textcoords="offset points",
            fontsize=8,
            color=e.texto_secundario,
        )
        x_folha: list[float] = [k / len(ordem) for k, _, _, _ in topo]
        eixo.fill_between(
            x_folha, [t[2] for t in topo], [t[3] for t in topo], color=e.series[0], alpha=0.12, linewidth=0, zorder=1
        )
        eixo.plot(
            x_folha, [t[1] for t in topo], color=e.series[0], linewidth=2, zorder=3, label="folha, fora da amostra"
        )
        curva: list[tuple[int, float, float]] = [c for c in previsao.curva if c[0] > 0]
        x_559: list[float] = [n / previsao.avaliadas for n, _, _ in curva]
        eixo.fill_between(
            x_559, [c[2] for c in curva], [c[1] for c in curva], color=e.series[1], alpha=0.15, linewidth=0, zorder=1
        )
        eixo.plot(
            x_559, [c[1] for c in curva], color=e.series[1], linewidth=2, zorder=3, label="559 avaliadas, estimativa"
        )
        cobertura: float = previsao.publicadas / previsao.avaliadas
        estrito: float = previsao.publicadas_estrito / previsao.avaliadas
        eixo.axvline(cobertura, color=e.texto_secundario, linewidth=1, zorder=2)
        eixo.annotate(
            f"publicado: {previsao.publicadas} ({cobertura:.0%})",
            (cobertura, 0.80),
            xytext=(4, 0),
            textcoords="offset points",
            fontsize=8,
            color=e.texto,
        )
        eixo.axvline(estrito, color=e.referencia, linewidth=1, linestyle=":", zorder=2)
        eixo.text(
            estrito + 0.008,
            0.765,
            f"estrito (P10 ≥ 95%): {previsao.publicadas_estrito}",
            rotation=90,
            fontsize=8,
            color=e.texto_secundario,
            va="bottom",
        )
        eixo.set_xlim(0.0, 1.0)
        eixo.set_ylim(0.75, 1.01)
        eixo.legend(loc="upper right", frameon=False, fontsize=8, labelcolor=e.texto_secundario)
        eixo.set_title("Precisão × cobertura", loc="left", fontsize=11, color=e.texto)
        figura.text(
            0.01,
            0.01,
            "Azul: acerto das k de maior confiança na folha (faixa: 90%, Jeffreys). Laranja: ponto e percentil 10 do modelo.",
            fontsize=7.5,
            color=e.texto_secundario,
        )
        self._gravar(figura, "precisao_cobertura")
        return topo

    def _preparar_eixo(self, eixo: Axes, rotulo_x: str, rotulo_y: str) -> None:
        """Aplica o estilo comum a um eixo.

        Args:
            eixo: Eixo do gráfico.
            rotulo_x: Rótulo do eixo x.
            rotulo_y: Rótulo do eixo y.
        """
        e: EstiloGraficos = self._estilo
        eixo.set_facecolor(e.superficie)
        eixo.grid(True, color=e.grade, linewidth=0.8)
        eixo.set_axisbelow(True)
        eixo.set_xlabel(rotulo_x, color=e.texto_secundario, fontsize=9)
        eixo.set_ylabel(rotulo_y, color=e.texto_secundario, fontsize=9)
        eixo.tick_params(colors=e.texto_secundario, labelsize=8)
        lado: str
        for lado in ("top", "right"):
            eixo.spines[lado].set_visible(False)
        for lado in ("left", "bottom"):
            eixo.spines[lado].set_color(e.grade)

    def _gravar(self, figura: Figure, nome: str) -> None:
        """Grava o gráfico em PNG e SVG (sem data nos metadados, para a saída não mudar entre execuções).

        Args:
            figura: Figura.
            nome: Nome do arquivo, sem extensão.
        """
        figura.tight_layout(rect=(0, 0.03, 1, 1))
        figura.savefig(self._pasta / f"{nome}.png", facecolor=figura.get_facecolor(), metadata={"Software": None})
        figura.savefig(
            self._pasta / f"{nome}.svg", facecolor=figura.get_facecolor(), metadata={"Date": None, "Creator": None}
        )

    def _tabela(
        self,
        faixas: Sequence[tuple[int, float, float, float, float]],
        topo: Sequence[tuple[int, float, float, float]],
        previsao: Previsao,
    ) -> Path:
        """Grava ``graficos.md`` com as mesmas informações dos gráficos.

        Args:
            faixas: Faixas de confiabilidade.
            topo: Precisão no topo k da folha.
            previsao: Previsão.

        Returns:
            Caminho gravado.
        """
        linhas: list[str] = [
            "# Gráficos da etapa 2",
            "",
            "![Confiabilidade](confiabilidade.png)",
            "",
            "| Faixa (20 questões) | P média prevista | Acerto observado | Intervalo de 90% |",
            "|---:|---:|---:|---|",
            *(
                f"| {i + 1} | {f[1]:.3f} | {f[2] * f[0]:.0f}/{f[0]} ({f[2]:.0%}) | {f[3]:.2f}–{f[4]:.2f} |"
                for i, f in enumerate(faixas)
            ),
            "",
            "![Precisão × cobertura](precisao_cobertura.png)",
            "",
            "| Questões da folha (maior P primeiro) | Precisão observada | Intervalo de 90% |",
            "|---:|---:|---|",
            *(f"| {t[0]} | {t[1]:.0%} | {t[2]:.2f}–{t[3]:.2f} |" for t in topo if t[0] % 10 == 0),
            "",
            (
                f"Nas 559 avaliadas: {previsao.publicadas} publicadas (precisão prevista {previsao.precisao:.2f}, "
                f"{previsao.precisao_intervalo[0]:.2f}–{previsao.precisao_intervalo[1]:.2f}); pelo critério estrito "
                f"(percentil 10 ≥ 95%), seriam {previsao.publicadas_estrito}."
            ),
            "",
        ]
        destino: Path = self._pasta / "graficos.md"
        destino.write_text("\n".join(linhas), encoding="utf-8")
        return destino
