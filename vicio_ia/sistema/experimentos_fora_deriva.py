"""E11b (fora com embeddings e kNN, ADR-023) e E12 (deriva entre antigas e novas, ADR-024).

Só lê artefatos: os vetores do modelo escolhido, a base de temas, as citações e o mapa de artigos. Nenhum
modelo é chamado. O E11b mede, nas 100 questões da folha, quanto cada atributo separa as 8 questões fora
(AUC com intervalo por bootstrap) e uma logística fora da amostra com três atributos pré-registrados. O E12
compara, sem rótulo, as 259 antigas avaliadas com as 300 novas.
"""

from __future__ import annotations

import csv
import math
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import ClassVar, TextIO

import numpy as np
import numpy.typing as npt

from vicio_ia.configuracao import Caminhos, ParametrosEDA, ParametrosSistema
from vicio_ia.enriquecimento.citacoes import ArquivoCitacoes, CitacoesQuestao
from vicio_ia.estatistica import Matriz
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada
from vicio_ia.sistema.base_temas import ArquivoBaseTemas, TemaBase
from vicio_ia.sistema.documentos import DocumentoTema, MontadorDocumentos
from vicio_ia.sistema.folha import LeitorFolha, RotuloFolha
from vicio_ia.sistema.lexical import IndiceBM25, TokenizadorLexical
from vicio_ia.sistema.mapa_artigos import MapaArtigos
from vicio_ia.sistema.metricas import MetricasBinarias
from vicio_ia.sistema.ranking import Metrica
from vicio_ia.sistema.validacao import ValidacaoCruzadaRepetida
from vicio_ia.sistema.vetores import ArquivoVetores, VetoresConhecimento
from vicio_ia.texto import ProcessadorTexto


@dataclass(frozen=True)
class AtributosQuestao:
    """Atributos sem rótulo de uma questão (E11b e E12).

    Attributes:
        id: ID da questão.
        similaridade_maxima: Maior similaridade densa com um tema publicável.
        margem: Diferença entre a 1ª e a 2ª similaridade.
        dispersao: Ramos de nível 1 distintos entre os melhores temas das alternativas, sobre as alternativas;
            ``nan`` em certo/errado.
        inativo_menos_maximo: Maior similaridade com um tema inativo menos a similaridade máxima.
        bm25_maximo: Maior pontuação BM25.
        tem_artigo: A questão cita artigo com a lei resolvida.
        regra_forte: Algum artigo citado acha linha no mapa, ou a questão contém um termo ``forte``.
        tokens: Tamanho estimado em tokens.
        certo_errado: Formato certo/errado.
        disciplina_origem: Disciplina de origem informada no banco.
        disciplina_melhor: Disciplina do tema mais similar.
    """

    id: str
    similaridade_maxima: float
    margem: float
    dispersao: float
    inativo_menos_maximo: float
    bm25_maximo: float
    tem_artigo: bool
    regra_forte: bool
    tokens: int
    certo_errado: bool
    disciplina_origem: str
    disciplina_melhor: str


class ExperimentoForaDeriva:
    """Roda o E11b e o E12 e grava ``saidas/etapa2/e11b_e12.md`` e ``e11b_e12.csv``."""

    LOGISTICA: ClassVar[tuple[str, ...]] = (
        "similaridade máxima baixa",
        "dispersão densa entre alternativas",
        "kNN: mais perto de fora que de tema",
    )
    """Atributos da logística do E11b, pré-registrados."""

    def __init__(self, caminhos: Caminhos | None = None, parametros: ParametrosSistema | None = None) -> None:
        """Guarda a configuração.

        Args:
            caminhos: Caminhos do projeto.
            parametros: Parâmetros do sistema.
        """
        self._caminhos: Caminhos = caminhos or Caminhos.padrao()
        self._parametros: ParametrosSistema = parametros or ParametrosSistema()
        self._processador: ProcessadorTexto = ProcessadorTexto()

    def executar(self) -> Path:
        """Roda os dois experimentos.

        Returns:
            Caminho do relatório.
        """
        leitor: LeitorPreparados = LeitorPreparados(self._caminhos)
        questoes: list[QuestaoPreparada] = leitor.questoes()
        temas: list[TemaPreparado] = leitor.temas()
        conhecimento: Path = self._caminhos.dados_conhecimento
        folha: list[RotuloFolha] = LeitorFolha(self._caminhos.folha_verdade, temas, {q.id for q in questoes}).ler()
        vetores: VetoresConhecimento = ArquivoVetores(conhecimento / "embeddings").ler()
        base: list[TemaBase] = ArquivoBaseTemas(conhecimento / "temas.jsonl").ler()
        citacoes: dict[str, CitacoesQuestao] = ArquivoCitacoes(conhecimento / "citacoes.jsonl").ler()
        mapa: MapaArtigos = MapaArtigos.ler(conhecimento / "mapa_artigos.csv")
        atributos: dict[str, AtributosQuestao] = self._atributos(questoes, vetores, base, citacoes, mapa)
        metricas_e11: list[Metrica] = self._e11b(folha, temas, atributos, vetores)
        metricas_e12: list[Metrica] = self._e12(questoes, folha, atributos)
        return self._gravar(metricas_e11, metricas_e12, folha, atributos, questoes)

    def _atributos(
        self,
        questoes: Sequence[QuestaoPreparada],
        vetores: VetoresConhecimento,
        base: Sequence[TemaBase],
        citacoes: Mapping[str, CitacoesQuestao],
        mapa: MapaArtigos,
    ) -> dict[str, AtributosQuestao]:
        """Calcula os atributos sem rótulo das 659 questões.

        Args:
            questoes: Questões preparadas.
            vetores: Vetores do modelo escolhido.
            base: Base de temas (na ordem dos vetores de tema).
            citacoes: Citações por questão.
            mapa: Mapa de artigos revisado.

        Returns:
            Atributos por ID.
        """
        por_id: dict[str, TemaBase] = {t.tema_id: t for t in base}
        ids_temas: tuple[str, ...] = vetores.temas.ids
        ramo: list[str] = [t if por_id[t].nivel == 1 else por_id[t].pai for t in ids_temas]
        disciplina: list[str] = [por_id[t].caminho.split(" > ")[0] for t in ids_temas]
        similaridade: Matriz = vetores.questoes.submatriz([q.id for q in questoes]) @ vetores.temas.matriz.T
        inativos: Matriz = vetores.questoes.submatriz([q.id for q in questoes]) @ vetores.inativos.matriz.T
        alternativas: dict[str, int] = {i: k for k, i in enumerate(vetores.alternativas.ids)}
        similaridade_alt: Matriz = vetores.alternativas.matriz @ vetores.temas.matriz.T
        documentos: list[DocumentoTema] = MontadorDocumentos.documentos_base(base, self._parametros.documento_tema_bm25)
        tokenizador: TokenizadorLexical = TokenizadorLexical(self._processador, ParametrosEDA().palavras_sem_conteudo)
        p: ParametrosSistema = self._parametros
        indice: IndiceBM25 = IndiceBM25([tokenizador.termos(d.texto) for d in documentos], p.bm25_k1, p.bm25_b)
        fortes: set[str] = {t.normalizado for b in base for t in b.termos if t.tipo == "forte" and t.normalizado}
        atributos: dict[str, AtributosQuestao] = {}
        linha: int
        questao: QuestaoPreparada
        for linha, questao in enumerate(questoes):
            ordenadas: Matriz = np.sort(similaridade[linha])
            ramos: list[str] = [
                ramo[int(np.argmax(similaridade_alt[alternativas[f"{questao.id}:{letra}"]]))]
                for letra in MontadorDocumentos.textos_alternativas(questao)
                if f"{questao.id}:{letra}" in alternativas
            ]
            texto: str = MontadorDocumentos.texto_questao(questao)
            citacao: CitacoesQuestao | None = citacoes.get(questao.id)
            artigos: bool = citacao is not None and bool(citacao.artigos)
            no_mapa: bool = citacao is not None and any(mapa.linhas(a.lei, a.inicio, a.fim) for a in citacao.artigos)
            normalizado: str = f" {self._processador.normalizar(texto)} "
            atributos[questao.id] = AtributosQuestao(
                id=questao.id,
                similaridade_maxima=float(ordenadas[-1]),
                margem=float(ordenadas[-1] - ordenadas[-2]),
                dispersao=len(set(ramos)) / len(ramos) if ramos else math.nan,
                inativo_menos_maximo=float(inativos[linha].max() - ordenadas[-1]),
                bm25_maximo=float(indice.pontuar(tokenizador.termos(texto)).max()),
                tem_artigo=artigos,
                regra_forte=no_mapa or any(f" {f} " in normalizado for f in fortes),
                tokens=questao.tokens_estimados,
                certo_errado=questao.formato == "certo_errado",
                disciplina_origem=str(questao.original.get("disciplina_origem") or ""),
                disciplina_melhor=disciplina[int(np.argmax(similaridade[linha]))],
            )
        return atributos

    @staticmethod
    def _knn_fora(folha: Sequence[RotuloFolha], vetores: VetoresConhecimento) -> list[float]:
        """kNN deixa-uma-fora: similaridade com a questão fora mais parecida menos a com tema mais parecida.

        Args:
            folha: Rótulos.
            vetores: Vetores do modelo escolhido.

        Returns:
            Um valor por questão da folha (maior = mais perto das questões fora).
        """
        matriz: Matriz = vetores.questoes.submatriz([r.id for r in folha])
        similaridade: Matriz = matriz @ matriz.T
        np.fill_diagonal(similaridade, -np.inf)
        fora: npt.NDArray[np.bool_] = np.array([r.fora for r in folha], dtype=np.bool_)
        com_tema: npt.NDArray[np.bool_] = np.logical_not(fora)
        return [float(similaridade[i, fora].max() - similaridade[i, com_tema].max()) for i in range(len(folha))]

    def _e11b(
        self,
        folha: Sequence[RotuloFolha],
        temas: Sequence[TemaPreparado],
        atributos: Mapping[str, AtributosQuestao],
        vetores: VetoresConhecimento,
    ) -> list[Metrica]:
        """AUC de cada atributo e da logística pré-registrada, fora da amostra.

        Args:
            folha: Rótulos.
            temas: Árvore preparada.
            atributos: Atributos por questão.
            vetores: Vetores do modelo escolhido.

        Returns:
            Métricas do E11b.
        """
        p: ParametrosSistema = self._parametros
        da_folha: list[AtributosQuestao] = [atributos[r.id] for r in folha]
        fora: list[bool] = [r.fora for r in folha]
        colunas: dict[str, list[float]] = {
            "similaridade máxima baixa": [-a.similaridade_maxima for a in da_folha],
            "margem densa baixa": [-a.margem for a in da_folha],
            "dispersão densa entre alternativas": [0.0 if math.isnan(a.dispersao) else a.dispersao for a in da_folha],
            "tema inativo perto do melhor tema": [a.inativo_menos_maximo for a in da_folha],
            "kNN: mais perto de fora que de tema": self._knn_fora(folha, vetores),
            "sem regra forte (artigo no mapa ou termo forte)": [0.0 if a.regra_forte else 1.0 for a in da_folha],
        }
        metricas: list[Metrica] = []
        nome: str
        valores: list[float]
        for nome, valores in colunas.items():
            baixo: float
            alto: float
            baixo, alto = MetricasBinarias.intervalo_auc(valores, fora, p.reamostras_auc, p.semente)
            metricas.append(
                Metrica("E11b", nome, "AUC", MetricasBinarias.auc(valores, fora), f"IC 90%: {baixo:.2f}–{alto:.2f}")
            )
        x: Matriz = np.array([[colunas[c][i] for c in self.LOGISTICA] for i in range(len(folha))], dtype=np.float64)
        y: Matriz = np.array([1.0 if f else 0.0 for f in fora], dtype=np.float64)
        validacao: ValidacaoCruzadaRepetida = ValidacaoCruzadaRepetida(
            p.partes_validacao, p.repeticoes_validacao, p.semente
        )
        previsao: Matriz = ValidacaoCruzadaRepetida.logistica_fora_da_amostra(
            x, y, validacao.particoes(ValidacaoCruzadaRepetida.estratos_folha(folha, temas)), 1.0
        )
        previstas: list[float] = [float(v) for v in previsao]
        baixo_cv: float
        alto_cv: float
        baixo_cv, alto_cv = MetricasBinarias.intervalo_auc(previstas, fora, p.reamostras_auc, p.semente)
        metricas.append(
            Metrica(
                "E11b",
                "logística: " + ", ".join(self.LOGISTICA),
                "AUC fora da amostra",
                MetricasBinarias.auc(previstas, fora),
                f"IC 90%: {baixo_cv:.2f}–{alto_cv:.2f}; {p.partes_validacao} partes × {p.repeticoes_validacao} repetições",
            )
        )
        com_regra: int = sum(1 for a, f in zip(da_folha, fora, strict=True) if f and a.regra_forte)
        metricas.append(
            Metrica(
                "E11b",
                "fora com regra forte",
                "questões fora com artigo no mapa ou termo forte",
                com_regra,
                f"{com_regra}/{sum(fora)}",
            )
        )
        return metricas

    def _e12(
        self,
        questoes: Sequence[QuestaoPreparada],
        folha: Sequence[RotuloFolha],
        atributos: Mapping[str, AtributosQuestao],
    ) -> list[Metrica]:
        """AUC "nova × antiga" dos atributos numéricos e proporções dos categóricos.

        Args:
            questoes: Questões preparadas.
            folha: Rótulos (as da folha ficam de fora do grupo das antigas).
            atributos: Atributos por questão.

        Returns:
            Métricas do E12.
        """
        p: ParametrosSistema = self._parametros
        na_folha: set[str] = {r.id for r in folha}
        grupo: list[AtributosQuestao] = [atributos[q.id] for q in questoes if q.id not in na_folha]
        nova: list[bool] = [int(a.id[1:]) > p.questoes_etapa1 for a in grupo]
        numericos: dict[str, list[float]] = {
            "similaridade máxima": [a.similaridade_maxima for a in grupo],
            "margem densa": [a.margem for a in grupo],
            "dispersão densa": [0.0 if math.isnan(a.dispersao) else a.dispersao for a in grupo],
            "BM25 máximo": [a.bm25_maximo for a in grupo],
            "tamanho em tokens": [float(a.tokens) for a in grupo],
        }
        metricas: list[Metrica] = []
        nome: str
        valores: list[float]
        for nome, valores in numericos.items():
            baixo: float
            alto: float
            baixo, alto = MetricasBinarias.intervalo_auc(valores, nova, p.reamostras_auc, p.semente)
            antigas: list[float] = [v for v, n in zip(valores, nova, strict=True) if not n]
            novas: list[float] = [v for v, n in zip(valores, nova, strict=True) if n]
            metricas.append(
                Metrica(
                    "E12",
                    nome,
                    "AUC nova × antiga",
                    MetricasBinarias.auc(valores, nova),
                    f"IC 90%: {baixo:.2f}–{alto:.2f}; mediana antigas {float(np.median(antigas)):.3f}, "
                    f"novas {float(np.median(novas)):.3f}",
                )
            )
        binarios: dict[str, list[bool]] = {
            "cita artigo": [a.tem_artigo for a in grupo],
            "certo/errado": [a.certo_errado for a in grupo],
            "regra forte": [a.regra_forte for a in grupo],
        }
        marca: list[bool]
        for nome, marca in binarios.items():
            n_antigas: int = sum(1 for m, n in zip(marca, nova, strict=True) if m and not n)
            n_novas: int = sum(1 for m, n in zip(marca, nova, strict=True) if m and n)
            total_antigas: int = nova.count(False)
            total_novas: int = nova.count(True)
            metricas.append(
                Metrica(
                    "E12",
                    nome,
                    "diferença de proporção (novas − antigas)",
                    n_novas / total_novas - n_antigas / total_antigas,
                    f"antigas {n_antigas}/{total_antigas}, novas {n_novas}/{total_novas}",
                )
            )
        campo: str
        for campo in ("disciplina_origem", "disciplina_melhor"):
            antigas_c: Counter[str] = Counter(getattr(a, campo) for a, n in zip(grupo, nova, strict=True) if not n)
            novas_c: Counter[str] = Counter(getattr(a, campo) for a, n in zip(grupo, nova, strict=True) if n)
            categorias: list[str] = sorted(set(antigas_c) | set(novas_c))
            variacao: float = 0.5 * sum(
                abs(novas_c[c] / max(sum(novas_c.values()), 1) - antigas_c[c] / max(sum(antigas_c.values()), 1))
                for c in categorias
            )
            detalhe: str = "; ".join(f"{c or '(vazio)'}: {antigas_c[c]} → {novas_c[c]}" for c in categorias)
            metricas.append(Metrica("E12", campo.replace("_", " "), "variação total (0 a 1)", variacao, detalhe))
        return metricas

    def _deriva(self, metricas: Sequence[Metrica]) -> str:
        """Aplica o critério pré-registrado do E12 à similaridade máxima e à margem.

        Args:
            metricas: Métricas do E12.

        Returns:
            Texto com a conclusão.
        """
        achados: list[str] = []
        metrica: Metrica
        for metrica in metricas:
            if metrica.variante in {"similaridade máxima", "margem densa"} and metrica.nome == "AUC nova × antiga":
                intervalo: list[str] = metrica.detalhe.split(";")[0].removeprefix("IC 90%: ").split("–")
                baixo: float = float(intervalo[0])
                alto: float = float(intervalo[1])
                if (baixo > 0.5 or alto < 0.5) and abs(metrica.valor - 0.5) >= 0.1:
                    achados.append(f"{metrica.variante} (AUC {metrica.valor:.2f})")
        if achados:
            return "**Há deriva** pelo critério pré-registrado: " + ", ".join(achados) + "."
        return "**Não há deriva** pelo critério pré-registrado na similaridade máxima nem na margem."

    def _gravar(
        self,
        metricas_e11: Sequence[Metrica],
        metricas_e12: Sequence[Metrica],
        folha: Sequence[RotuloFolha],
        atributos: Mapping[str, AtributosQuestao],
        questoes: Sequence[QuestaoPreparada],
    ) -> Path:
        """Grava o CSV e o relatório.

        Args:
            metricas_e11: Métricas do E11b.
            metricas_e12: Métricas do E12.
            folha: Rótulos.
            atributos: Atributos por questão.
            questoes: Questões preparadas.

        Returns:
            Caminho do relatório.
        """
        pasta: Path = self._caminhos.saida_etapa2
        pasta.mkdir(parents=True, exist_ok=True)
        todas: list[Metrica] = [*metricas_e11, *metricas_e12]
        linhas_csv: list[list[str]] = [["experimento", "variante", "metrica", "valor", "detalhe"]]
        linhas_csv.extend([m.experimento, m.variante, m.nome, f"{m.valor:.4f}", m.detalhe] for m in todas)
        arquivo: TextIO
        with (pasta / "e11b_e12.csv").open("w", encoding="utf-8", newline="") as arquivo:
            csv.writer(arquivo).writerows(linhas_csv)
        logistica: Metrica = next(m for m in metricas_e11 if m.nome == "AUC fora da amostra")
        separavel: bool = logistica.valor >= 0.7
        militares: int = sum(
            1
            for q in questoes
            if "militar" in self._processador.normalizar(str(q.original.get("disciplina_origem") or ""))
        )
        linhas: list[str] = [
            "# E11b e E12: fora com embeddings e deriva entre antigas e novas",
            "",
            (
                f"Gerado em {datetime.now():%d/%m/%Y %H:%M}. Vetores de `dados/conhecimento/embeddings/`; nenhum modelo "
                "foi chamado. E11b: 100 questões da folha (8 fora). E12: 259 antigas avaliadas × 300 novas, sem rótulo."
            ),
            "",
            "## E11b: separabilidade do fora",
            "",
            "| Atributo | Métrica | Valor | Detalhe |",
            "|---|---|---:|---|",
            *(f"| {m.variante} | {m.nome} | {m.valor:.2f} | {m.detalhe} |" for m in metricas_e11),
            "",
            (
                f"**Critério pré-registrado** (AUC fora da amostra ≥ 0,7): {'separável' if separavel else 'não separável'}"
                f" (AUC {logistica.valor:.2f}). "
                + (
                    "P(fora) entra como componente da decisão (ADR-023)."
                    if separavel
                    else "Vale o plano B da ADR-023: P(fora) igual à taxa da folha e publicação só nas faixas em que "
                    "a folha mostrar taxa de fora compatível com 95%."
                )
            ),
            "",
            "| Questão fora | Similaridade máxima | Margem | Dispersão | Regra forte | Disciplina do melhor tema |",
            "|---|---:|---:|---:|---|---|",
        ]
        rotulo: RotuloFolha
        for rotulo in folha:
            if rotulo.fora:
                a: AtributosQuestao = atributos[rotulo.id]
                dispersao: str = "—" if math.isnan(a.dispersao) else f"{a.dispersao:.2f}"
                linhas.append(
                    f"| {a.id} | {a.similaridade_maxima:.3f} | {a.margem:.3f} | {dispersao} | "
                    f"{'sim' if a.regra_forte else 'não'} | {a.disciplina_melhor} |"
                )
        com_tema: list[AtributosQuestao] = [atributos[r.id] for r in folha if not r.fora]
        linhas.extend(
            [
                (
                    f"| **mediana (com tema)** | {float(np.median([a.similaridade_maxima for a in com_tema])):.3f} | "
                    f"{float(np.median([a.margem for a in com_tema])):.3f} | "
                    f"{float(np.nanmedian([a.dispersao for a in com_tema])):.2f} | | |"
                ),
                "",
                "## E12: deriva entre as antigas avaliadas e as novas",
                "",
                "| Atributo | Métrica | Valor | Detalhe |",
                "|---|---|---:|---|",
                *(f"| {m.variante} | {m.nome} | {m.valor:.2f} | {m.detalhe} |" for m in metricas_e12),
                "",
                self._deriva(metricas_e12),
                "",
                f"Questões com disciplina de origem militar (sem nó na árvore, ADR-023): {militares}.",
                "",
            ]
        )
        destino: Path = pasta / "e11b_e12.md"
        destino.write_text("\n".join(linhas), encoding="utf-8")
        print(f"E11b: AUC fora da amostra {logistica.valor:.2f}. {self._deriva(metricas_e12)}\nRelatório: {destino}")
        return destino
