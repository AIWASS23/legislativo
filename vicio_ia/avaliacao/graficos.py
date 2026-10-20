"""Gráficos de confiabilidade e de precisão × cobertura (ADR-013), com as tabelas equivalentes.

Saídas em ``saidas/avaliacao/`` (PNG para o relatório e SVG):

* ``confiabilidade``: P prevista fora da amostra × acerto observado por faixa, no gold (régua estrita);
* ``precisao_cobertura_gold``: pipeline (P fora da amostra) × A e B sozinhos, no gold;
* ``precisao_cobertura_359``: precisão estimada (chance efetiva) × cobertura nas 359, com o percentil 10
  e o corte escolhido pelo passo 07;
* ``graficos.md``: as mesmas informações em tabela.

Cores: as três primeiras posições da paleta categórica validada (azul, laranja, verde-água), sempre na
mesma ordem; linhas de referência em cinza; cada curva com rótulo direto, além da legenda.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import matplotlib

matplotlib.use("Agg")

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from vicio_ia.arvore import ArvoreTemas
from vicio_ia.avaliacao.calibracao import (
    CalibradorBase,
    CalibradorFaixas,
    ExemploCalibracao,
    SeletorCalibrador,
    VetorizadorDecisao,
)
from vicio_ia.avaliacao.metricas import AvaliadorGold, PontoCurva, PrevisaoSistema
from vicio_ia.avaliacao.planilha import PlanilhaRotulos, RotuloGold, SituacaoLinha
from vicio_ia.avaliacao.pontuador import PontuadorRegua
from vicio_ia.avaliacao.previsao import PrevisorPrecisao, ResultadoPrevisao
from vicio_ia.carregamento import CarregadorDados
from vicio_ia.classificacao.respostas import SinaisQuestao, VotoClassificador
from vicio_ia.configuracao import Caminhos, ParametrosCalibracao, ParametrosGold
from vicio_ia.decisao.agregacao import AgregadorSinais, DecisaoPreliminar
from vicio_ia.estatistica import Matriz
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada
from vicio_ia.sinais.origem import SinalOrigem
from vicio_ia.texto import ProcessadorTexto


@dataclass(frozen=True)
class Estilo:
    """Cores e medidas dos gráficos (paleta categórica validada, modo claro).

    Attributes:
        superficie: Fundo.
        texto: Texto principal.
        texto_secundario: Rótulos, eixos e anotações.
        grade: Linhas de grade (recessivas).
        referencia: Linhas de referência (meta de 95%, diagonal).
        series: Cores das séries, na ordem fixa: pipeline, A, B.
    """

    superficie: str = "#fcfcfb"
    texto: str = "#0b0b0b"
    texto_secundario: str = "#52514e"
    grade: str = "#e6e5e1"
    referencia: str = "#8d8c86"
    series: tuple[str, str, str] = ("#2a78d6", "#eb6834", "#1baf7a")


class GraficosAvaliacao:
    """Gera os três gráficos e a tabela equivalente a partir do gold, dos sinais e da calibração."""

    NOMES_FAIXAS: ClassVar[dict[str, str]] = {
        "consenso_total": "consenso total",
        "confirma_parcial": "confirma parcial",
        "verificador_vizinho": "verificador vizinho",
        "outros": "outros",
    }

    def __init__(
        self,
        caminhos: Caminhos | None = None,
        parametros: ParametrosCalibracao | None = None,
        estilo: Estilo | None = None,
    ) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto (opcional).
            parametros: Parâmetros da calibração (opcional).
            estilo: Cores e medidas (opcional).
        """
        self._caminhos: Caminhos = caminhos if caminhos is not None else Caminhos.padrao()
        self._parametros: ParametrosCalibracao = parametros if parametros is not None else ParametrosCalibracao()
        self._estilo: Estilo = estilo if estilo is not None else Estilo()
        self._pasta: Path = self._caminhos.raiz / "saidas" / "avaliacao"

    def executar(self) -> Path:
        """Gera os gráficos e ``graficos.md``.

        Returns:
            Caminho de ``graficos.md``.
        """
        leitor: LeitorPreparados = LeitorPreparados(self._caminhos)
        questoes: dict[str, QuestaoPreparada] = {q.id: q for q in leitor.questoes()}
        temas: list[TemaPreparado] = leitor.temas()
        sinais: dict[str, SinaisQuestao] = self._sinais()
        agregador: AgregadorSinais = AgregadorSinais(temas)
        origem: SinalOrigem = SinalOrigem(temas, ProcessadorTexto())
        preliminares: dict[str, DecisaoPreliminar] = {
            i: agregador.decidir(s, questoes[i], origem.temas(questoes[i])) for i, s in sinais.items()
        }
        pontuador: PontuadorRegua = PontuadorRegua(ArvoreTemas(CarregadorDados(self._caminhos).carregar_temas()))
        rotulos: list[RotuloGold] = self._rotulos(temas)
        exemplos: list[ExemploCalibracao] = [
            ExemploCalibracao(preliminares[r.id], pontuador.acerta(preliminares[r.id].tema_id, r, "estrita"), 1.0)
            for r in rotulos
            if r.id in preliminares and preliminares[r.id].tema_id and preliminares[r.id].acao != "fora"
        ]
        calibrador: CalibradorBase
        calibrador, _ = SeletorCalibrador(VetorizadorDecisao()).escolher(
            exemplos, self._parametros.penalidades_l2, self._parametros.partes_validacao, self._parametros.semente
        )
        fora: list[float] = calibrador.fora_da_amostra(
            exemplos, self._parametros.partes_validacao, self._parametros.semente
        )
        self._pasta.mkdir(parents=True, exist_ok=True)
        faixas: list[tuple[str, int, float, float, float, float]] = self._confiabilidade(exemplos, fora)
        curvas: dict[str, tuple[PontoCurva, ...]] = self._precisao_cobertura_gold(
            exemplos, fora, sinais, rotulos, pontuador
        )
        com_tema: list[DecisaoPreliminar] = [d for d in preliminares.values() if d.tema_id and d.acao != "fora"]
        tolerante: dict[str, bool] = {
            r.id: pontuador.acerta(preliminares[r.id].tema_id, r, "tolerante")
            for r in rotulos
            if r.id in preliminares and preliminares[r.id].tema_id
        }
        populacao: list[tuple[int, float, float, float]] = self._precisao_cobertura_359(
            com_tema, exemplos, calibrador, tolerante
        )
        return self._tabelas(calibrador.nome, faixas, curvas, populacao, len(rotulos))

    def _confiabilidade(
        self, exemplos: Sequence[ExemploCalibracao], fora: Sequence[float]
    ) -> list[tuple[str, int, float, float, float, float]]:
        """Gráfico de confiabilidade por faixa (P fora da amostra × acerto observado).

        Args:
            exemplos: Gold com tema.
            fora: P fora da amostra de cada exemplo.

        Returns:
            ``(faixa, n, P média prevista, acerto observado, limite inferior, limite superior)`` (90%, Jeffreys).
        """
        linhas: list[tuple[str, int, float, float, float, float]] = []
        faixa: str
        for faixa in CalibradorFaixas.FAIXAS:
            indices: list[int] = [i for i, e in enumerate(exemplos) if CalibradorFaixas.faixa(e.decisao) == faixa]
            if not indices:
                continue
            acertos: int = sum(1 for i in indices if exemplos[i].acerto)
            gerador: np.random.Generator = np.random.default_rng(self._parametros.semente)
            sorteios: Matriz = gerador.beta(acertos + 0.5, len(indices) - acertos + 0.5, 20000)
            linhas.append(
                (
                    faixa,
                    len(indices),
                    float(np.mean([fora[i] for i in indices])),
                    acertos / len(indices),
                    float(np.percentile(sorteios, 5)),
                    float(np.percentile(sorteios, 95)),
                )
            )
        e: Estilo = self._estilo
        figura: Figure = Figure(figsize=(6.4, 5.2), dpi=150, facecolor=e.superficie)
        eixo: Axes = figura.add_subplot()
        self._preparar_eixo(eixo, "P prevista (fora da amostra)", "Acerto observado no gold (régua estrita)")
        eixo.plot([0.4, 1.0], [0.4, 1.0], color=e.referencia, linewidth=1, linestyle="--", zorder=1)
        linha: tuple[str, int, float, float, float, float]
        for linha in linhas:
            eixo.vlines(linha[2], linha[4], linha[5], color=e.series[0], linewidth=2, alpha=0.45, zorder=2)
            eixo.plot(
                linha[2],
                linha[3],
                marker="o",
                color=e.series[0],
                markersize=8,
                markeredgecolor=e.superficie,
                markeredgewidth=2,
                zorder=3,
            )
            a_direita: bool = linha[2] < 0.7
            eixo.annotate(
                f"{self.NOMES_FAIXAS[linha[0]]} ({linha[3] * linha[1]:.0f}/{linha[1]})",
                (linha[2], linha[3]),
                xytext=(9, -4) if a_direita else (-9, -14),
                textcoords="offset points",
                fontsize=9,
                color=e.texto,
                ha="left" if a_direita else "right",
            )
        eixo.set_xlim(0.4, 1.02)
        eixo.set_ylim(0.4, 1.02)
        eixo.set_title("Confiabilidade da calibração por faixas (gold set)", loc="left", fontsize=11, color=e.texto)
        figura.text(
            0.01,
            0.01,
            "Pontos: acerto observado. Linhas: intervalo de 90% (Jeffreys). Na diagonal, P prevista = acerto.",
            fontsize=7.5,
            color=e.texto_secundario,
        )
        self._gravar(figura, "confiabilidade")
        return linhas

    def _precisao_cobertura_gold(
        self,
        exemplos: Sequence[ExemploCalibracao],
        fora: Sequence[float],
        sinais: Mapping[str, SinaisQuestao],
        rotulos: Sequence[RotuloGold],
        pontuador: PontuadorRegua,
    ) -> dict[str, tuple[PontoCurva, ...]]:
        """Curvas de precisão × cobertura no gold: pipeline, A sozinho e B sozinho.

        Args:
            exemplos: Gold com tema (decisões do pipeline).
            fora: P fora da amostra.
            sinais: Sinais por questão.
            rotulos: Rótulos válidos.
            pontuador: Régua.

        Returns:
            ``nome -> pontos da curva`` (régua estrita).
        """
        avaliador: AvaliadorGold = AvaliadorGold(pontuador)
        pipeline: dict[str, PrevisaoSistema] = {
            e.decisao.id: PrevisaoSistema(e.decisao.id, e.decisao.tema_id if e.decisao.acao == "candidata" else "", p)
            for e, p in zip(exemplos, fora, strict=True)
        }
        sistemas: dict[str, dict[str, PrevisaoSistema]] = {"pipeline": pipeline}
        papel: str
        nome: str
        for papel, nome in (("classificador_a", "A sozinho"), ("classificador_b", "B sozinho")):
            previsoes: dict[str, PrevisaoSistema] = {}
            rotulo: RotuloGold
            for rotulo in rotulos:
                voto: VotoClassificador | None = sinais[rotulo.id].voto(papel) if rotulo.id in sinais else None
                if voto is not None and voto.ok:
                    previsoes[rotulo.id] = PrevisaoSistema(rotulo.id, voto.tema_id, voto.autoconfianca or 0.0)
            sistemas[nome] = previsoes
        curvas: dict[str, tuple[PontoCurva, ...]] = {
            nome: avaliador.avaliar(previsoes, rotulos, "estrita").curva for nome, previsoes in sistemas.items()
        }
        e: Estilo = self._estilo
        figura: Figure = Figure(figsize=(6.4, 4.6), dpi=150, facecolor=e.superficie)
        eixo: Axes = figura.add_subplot()
        self._preparar_eixo(eixo, "Cobertura (fração das 60 questões do gold publicada)", "Precisão (régua estrita)")
        self._meta(eixo)
        indice: int
        pontos: tuple[PontoCurva, ...]
        for indice, (nome, pontos) in enumerate(curvas.items()):
            x: list[float] = [p.cobertura for p in pontos]
            y: list[float] = [p.precisao for p in pontos]
            rotulo_serie: str = "pipeline (P fora da amostra)" if nome == "pipeline" else f"{nome} (autoconfiança)"
            eixo.plot(
                x,
                y,
                color=e.series[indice],
                linewidth=2,
                marker="o" if nome == "pipeline" else "",
                markersize=7,
                markeredgecolor=e.superficie,
                markeredgewidth=1.5,
                label=rotulo_serie,
                zorder=3 if nome == "pipeline" else 2,
            )
            if x:
                deslocamento: tuple[int, int] = {"pipeline": (6, 0), "A sozinho": (6, 6)}.get(nome, (6, -10))
                eixo.annotate(
                    nome, (x[-1], y[-1]), xytext=deslocamento, textcoords="offset points", fontsize=9, color=e.texto
                )
        eixo.set_xlim(0.0, 1.08)
        eixo.set_ylim(0.75, 1.01)
        eixo.legend(loc="lower left", frameon=False, fontsize=8, labelcolor=e.texto_secundario)
        eixo.set_title("Precisão × cobertura no gold set", loc="left", fontsize=11, color=e.texto)
        self._gravar(figura, "precisao_cobertura_gold")
        return curvas

    def _precisao_cobertura_359(
        self,
        com_tema: Sequence[DecisaoPreliminar],
        exemplos: Sequence[ExemploCalibracao],
        calibrador: CalibradorBase,
        tolerante: Mapping[str, bool],
    ) -> list[tuple[int, float, float, float]]:
        """Precisão estimada × cobertura nas 359, pela chance efetiva, com o corte do passo 07.

        Args:
            com_tema: Decisões com tema.
            exemplos: Gold.
            calibrador: Calibrador escolhido.
            tolerante: Acerto tolerante do gold, por ID.

        Returns:
            ``(publicadas, cobertura, precisão estimada, percentil 10)`` em cada corte permitido.
        """
        p: ParametrosCalibracao = self._parametros
        previsao: ResultadoPrevisao = PrevisorPrecisao(p, calibrador).prever(com_tema, exemplos, tolerante)
        principal: CalibradorBase = calibrador.novo().ajustar(exemplos)
        candidatas: list[DecisaoPreliminar] = sorted(
            (d for d in com_tema if d.acao == "candidata"), key=lambda d: (-previsao.probabilidades[d.id], d.id)
        )
        fatores: Matriz = np.array(
            [1.0 - p.taxas_convencao.get(d.tipo_convencao, 0.0) for d in candidatas], dtype=np.float64
        )
        sorteios: Matriz = principal.amostrar(candidatas, exemplos, p.reamostras, np.random.default_rng(p.semente))
        acumulados: Matriz = np.cumsum(sorteios * fatores, axis=1) / np.arange(1, len(candidatas) + 1)
        pontos: list[float] = list(
            np.cumsum([previsao.probabilidades[d.id] for d in candidatas]) / np.arange(1, len(candidatas) + 1)
        )
        cortes: list[int] = sorted(PrevisorPrecisao._cortes(candidatas, previsao.probabilidades))
        serie: list[tuple[int, float, float, float]] = [
            (
                k,
                k / p.total_questoes,
                pontos[k - 1],
                float(np.percentile(acumulados[:, k - 1], p.percentil_limiar)) if sorteios.shape[0] else pontos[k - 1],
            )
            for k in cortes
        ]
        e: Estilo = self._estilo
        figura: Figure = Figure(figsize=(6.4, 4.6), dpi=150, facecolor=e.superficie)
        eixo: Axes = figura.add_subplot()
        self._preparar_eixo(eixo, "Cobertura (fração das 359 questões publicada)", "Precisão estimada")
        self._meta(eixo)
        x: list[float] = [s[1] for s in serie]
        eixo.fill_between(x, [s[3] for s in serie], [s[2] for s in serie], color=e.series[0], alpha=0.18, linewidth=0)
        eixo.plot(
            x,
            [s[2] for s in serie],
            color=e.series[0],
            linewidth=2,
            marker="o",
            markersize=6,
            markeredgecolor=e.superficie,
            markeredgewidth=1.5,
            label="estimativa pontual",
            zorder=3,
        )
        eixo.plot(
            x, [s[3] for s in serie], color=e.series[0], linewidth=1, linestyle=":", label="percentil 10", zorder=3
        )
        publicadas: int = len(previsao.publicadas)
        if publicadas:
            eixo.axvline(publicadas / p.total_questoes, color=e.texto_secundario, linewidth=1)
            eixo.annotate(
                f"publicadas: {publicadas} ({publicadas / p.total_questoes:.0%})",
                (publicadas / p.total_questoes, 0.80),
                xytext=(6, 0),
                textcoords="offset points",
                fontsize=9,
                color=e.texto,
            )
        eixo.set_xlim(0.0, max(x, default=0.5) * 1.1)
        eixo.set_ylim(0.6, 1.01)
        eixo.legend(loc="lower left", frameon=False, fontsize=8, labelcolor=e.texto_secundario)
        eixo.set_title("Precisão estimada × cobertura nas 359 (chance efetiva)", loc="left", fontsize=11, color=e.texto)
        figura.text(
            0.01,
            0.01,
            "A faixa sombreada vai do percentil 10 à estimativa pontual. O corte só cai entre faixas.",
            fontsize=7.5,
            color=e.texto_secundario,
        )
        self._gravar(figura, "precisao_cobertura_359")
        return serie

    def _preparar_eixo(self, eixo: Axes, rotulo_x: str, rotulo_y: str) -> None:
        """Aplica o estilo comum a um eixo.

        Args:
            eixo: Eixo do gráfico.
            rotulo_x: Rótulo do eixo x.
            rotulo_y: Rótulo do eixo y.
        """
        e: Estilo = self._estilo
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

    def _meta(self, eixo: Axes) -> None:
        """Desenha a meta de 95%.

        Args:
            eixo: Eixo do gráfico.
        """
        e: Estilo = self._estilo
        eixo.axhline(self._parametros.alvo_precisao, color=e.referencia, linewidth=1, linestyle="--", zorder=1)
        eixo.annotate(
            "meta: 95%",
            (0.0, self._parametros.alvo_precisao),
            xytext=(4, 3),
            textcoords="offset points",
            fontsize=8,
            color=e.texto_secundario,
        )

    def _gravar(self, figura: Figure, nome: str) -> None:
        """Grava o gráfico em PNG e SVG.

        Args:
            figura: Figura.
            nome: Nome do arquivo, sem extensão.
        """
        figura.tight_layout(rect=(0, 0.03, 1, 1))
        figura.savefig(self._pasta / f"{nome}.png", facecolor=figura.get_facecolor())
        figura.savefig(self._pasta / f"{nome}.svg", facecolor=figura.get_facecolor())

    def _tabelas(
        self,
        metodo: str,
        faixas: Sequence[tuple[str, int, float, float, float, float]],
        curvas: Mapping[str, Sequence[PontoCurva]],
        populacao: Sequence[tuple[int, float, float, float]],
        rotuladas: int,
    ) -> Path:
        """Grava ``graficos.md`` com os gráficos e as tabelas equivalentes.

        Args:
            metodo: Calibrador usado.
            faixas: Dados da confiabilidade.
            curvas: Curvas do gold.
            populacao: Curva nas 359.
            rotuladas: Questões do gold.

        Returns:
            Caminho gravado.
        """
        linhas: list[str] = [
            "# Gráficos de avaliação (ADR-013)",
            "",
            f"Gold set: {rotuladas} questões, régua estrita. Calibrador: {metodo}. A P de cada questão do gold vem",
            "de um calibrador ajustado sem ela (validação cruzada em 5 partes).",
            "",
            "## Confiabilidade",
            "",
            "![Confiabilidade](confiabilidade.png)",
            "",
            "| Faixa | Questões | P prevista (fora da amostra) | Acerto observado | Intervalo de 90% |",
            "|---|---:|---:|---:|---|",
            *(
                f"| {self.NOMES_FAIXAS[f]} | {n} | {pm:.3f} | {obs:.3f} | {lo:.3f}–{hi:.3f} |"
                for f, n, pm, obs, lo, hi in faixas
            ),
            "",
            "## Precisão × cobertura no gold",
            "",
            "![Precisão × cobertura no gold](precisao_cobertura_gold.png)",
            "",
            "| Sistema | Publicadas | Cobertura | Precisão |",
            "|---|---:|---:|---:|",
        ]
        nome: str
        pontos: Sequence[PontoCurva]
        for nome, pontos in curvas.items():
            linhas.extend(f"| {nome} | {pt.publicadas} | {pt.cobertura:.2f} | {pt.precisao:.3f} |" for pt in pontos)
        linhas.extend(
            [
                "",
                "## Precisão estimada × cobertura nas 359",
                "",
                "![Precisão estimada × cobertura nas 359](precisao_cobertura_359.png)",
                "",
                "| Publicadas | Cobertura | Precisão estimada | Percentil 10 |",
                "|---:|---:|---:|---:|",
                *(f"| {k} | {cob:.3f} | {pt:.3f} | {p10:.3f} |" for k, cob, pt, p10 in populacao),
                "",
            ]
        )
        destino: Path = self._pasta / "graficos.md"
        destino.write_text("\n".join(linhas), encoding="utf-8")
        return destino

    def _sinais(self) -> dict[str, SinaisQuestao]:
        """Lê ``sinais.jsonl``.

        Returns:
            Sinais por ID.
        """
        sinais: dict[str, SinaisQuestao] = {}
        numero: int
        linha: str
        arquivo: Path = self._caminhos.dados_classificacao / "sinais.jsonl"
        for numero, linha in enumerate(arquivo.read_text(encoding="utf-8").splitlines(), start=1):
            if linha.strip():
                valor: object = json.loads(linha)
                if isinstance(valor, dict):
                    item: SinaisQuestao = SinaisQuestao.de_dict({str(k): v for k, v in valor.items()}, f"{numero}")
                    sinais[item.id] = item
        return sinais

    def _rotulos(self, temas: Sequence[TemaPreparado]) -> list[RotuloGold]:
        """Lê os rótulos válidos do gold.

        Args:
            temas: Árvore preparada.

        Returns:
            Rótulos válidos.
        """
        planilha: PlanilhaRotulos = PlanilhaRotulos(
            self._caminhos.dados_gold / "rotulos_leva1.csv", ParametrosGold(), temas
        )
        situacoes: list[SituacaoLinha] = planilha.validar(planilha.ler())
        return [s.rotulo for s in situacoes if s.situacao == "rotulada"]
