"""Experimentos da etapa 2 na folha-verdade (ADR-024): E7 (só lexical) e E11 (separabilidade do fora).

Nenhum experimento chama modelo nem lê resposta de LLM sobre questão (ADR-019). O E7 não tem parâmetro
aprendido, então é medido direto na folha; o E11 mede cada atributo isolado (AUC com intervalo por
bootstrap) e uma logística pequena fora da amostra (validação cruzada repetida).
"""

from __future__ import annotations

import csv
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TextIO

import numpy as np

from vicio_ia.configuracao import Caminhos, ParametrosEDA, ParametrosSistema
from vicio_ia.estatistica import Matriz
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada
from vicio_ia.sistema.base_temas import ArquivoBaseTemas, TemaBase
from vicio_ia.sistema.documentos import DocumentoTema, MontadorDocumentos
from vicio_ia.sistema.folha import LeitorFolha, RotuloFolha
from vicio_ia.sistema.lexical import IndiceBM25, TokenizadorLexical
from vicio_ia.sistema.metricas import MetricasBinarias
from vicio_ia.sistema.ranking import AvaliadorRanking, Metrica, RankingQuestao, RegraEscolha
from vicio_ia.sistema.validacao import ValidacaoCruzadaRepetida
from vicio_ia.temas.cartoes import ArquivoCartoes, CartaoTema
from vicio_ia.texto import ProcessadorTexto


@dataclass(frozen=True)
class AtributosFora:
    """Atributos de uma questão para separar o "fora" (ADR-023).

    Attributes:
        id: ID da questão.
        pontuacao_maxima: Maior pontuação BM25 entre os temas.
        margem: ``(1º - 2º) / 1º`` (0 sem pontuação).
        dispersao: Ramos de nível 1 distintos entre os melhores temas das alternativas, sobre o número de
            alternativas pontuadas; ``nan`` em certo/errado.
        generico: Enunciado genérico (marca da etapa 1).
        parte_n_origem: O assunto de origem tem "(Parte N)".
        origem_fora_do_recorte: A disciplina de origem não está no recorte.
    """

    id: str
    pontuacao_maxima: float
    margem: float
    dispersao: float
    generico: bool
    parte_n_origem: bool
    origem_fora_do_recorte: bool


class ExperimentosEtapa2:
    """Roda o E7 e o E11 e grava o relatório em ``saidas/etapa2/``."""

    def __init__(self, caminhos: Caminhos | None = None, parametros: ParametrosSistema | None = None) -> None:
        """Guarda a configuração.

        Args:
            caminhos: Caminhos do projeto (padrão: os da etapa em vigor).
            parametros: Parâmetros do sistema.
        """
        self._caminhos: Caminhos = caminhos or Caminhos.padrao()
        self._parametros: ParametrosSistema = parametros or ParametrosSistema()
        self._eda: ParametrosEDA = ParametrosEDA()
        self._processador: ProcessadorTexto = ProcessadorTexto()
        self._tokenizador: TokenizadorLexical = TokenizadorLexical(self._processador, self._eda.palavras_sem_conteudo)

    def executar(self) -> Path:
        """Roda os experimentos.

        Returns:
            Caminho do relatório em Markdown.
        """
        leitor: LeitorPreparados = LeitorPreparados(self._caminhos)
        questoes: dict[str, QuestaoPreparada] = {q.id: q for q in leitor.questoes()}
        temas: list[TemaPreparado] = leitor.temas()
        cartoes: list[CartaoTema] = ArquivoCartoes(self._caminhos.dados_temas / "cartoes.jsonl").ler()
        folha: list[RotuloFolha] = LeitorFolha(self._caminhos.folha_verdade, temas, questoes.keys()).ler()
        avaliador: AvaliadorRanking = AvaliadorRanking(temas, self._parametros.top_k_recall)
        montador: MontadorDocumentos = MontadorDocumentos(temas, cartoes)
        metricas: list[Metrica] = []
        rankings: dict[str, list[RankingQuestao]] = {}
        variante: str
        com_cartao: bool
        for variante, com_cartao in (("títulos e caminho", False), ("com cartão", True)):
            documentos: list[DocumentoTema] = montador.documentos(com_cartao)
            indice: IndiceBM25 = self._indice(documentos)
            rankings[variante] = [self._ranking(questoes[r.id], r, documentos, indice, avaliador) for r in folha]
            metricas.extend(avaliador.metricas("E7", variante, folha, rankings[variante]))
        base: list[TemaBase] = ArquivoBaseTemas(self._caminhos.dados_conhecimento / "temas.jsonl").ler()
        for variante in TemaBase.VARIANTES:
            documentos_base: list[DocumentoTema] = MontadorDocumentos.documentos_base(base, variante)
            indice_base: IndiceBM25 = self._indice(documentos_base)
            rankings_base: list[RankingQuestao] = [
                self._ranking(questoes[r.id], r, documentos_base, indice_base, avaliador) for r in folha
            ]
            metricas.extend(avaliador.metricas("E7b", variante, folha, rankings_base))
        vencedor_e7b: str = RegraEscolha.escolher(metricas, "E7b", TemaBase.VARIANTES)
        print(f"E7b (documento de tema no BM25), vencedor pela regra pré-registrada: {vencedor_e7b}")
        documentos_cartao: list[DocumentoTema] = montador.documentos(True)
        indice_cartao: IndiceBM25 = self._indice(documentos_cartao)
        atributos: list[AtributosFora] = [
            self._atributos_fora(questoes[r.id], documentos_cartao, indice_cartao, temas) for r in folha
        ]
        metricas.extend(self._metricas_e11(folha, atributos, temas))
        notas: list[str] = [
            (
                f"**E7b, documento de tema no BM25:** vence `{vencedor_e7b}` pela regra pré-registrada (maior "
                "recall@10; até uma questão de diferença é empate, decidido pelo top-1; depois, a variante mais "
                f"simples). Documento do BM25 em uso no sistema: `{self._parametros.documento_tema_bm25}`."
            )
        ]
        return self._gravar(metricas, rankings["com cartão"], folha, atributos, notas)

    def _indice(self, documentos: Sequence[DocumentoTema]) -> IndiceBM25:
        """Indexa os documentos de tema.

        Args:
            documentos: Documentos.

        Returns:
            Índice BM25.
        """
        p: ParametrosSistema = self._parametros
        return IndiceBM25([self._tokenizador.termos(d.texto) for d in documentos], p.bm25_k1, p.bm25_b)

    def _ranking(
        self,
        questao: QuestaoPreparada,
        rotulo: RotuloFolha,
        documentos: Sequence[DocumentoTema],
        indice: IndiceBM25,
        avaliador: AvaliadorRanking,
    ) -> RankingQuestao:
        """Ordena os temas pelo BM25 para uma questão e acha a posição do primeiro acerto.

        Args:
            questao: Questão.
            rotulo: Rótulo da equipe.
            documentos: Documentos indexados.
            indice: Índice BM25.
            avaliador: Avaliador de rankings.

        Returns:
            Ranking.
        """
        pontos: Matriz = indice.pontuar(self._tokenizador.termos(MontadorDocumentos.texto_questao(questao)))
        return avaliador.ordenar(rotulo, pontos, [d.tema_id for d in documentos])

    def _ramo_nivel1(self, tema_id: str, temas: Mapping[str, TemaPreparado]) -> str:
        """Tema de nível 1 do ramo (o próprio tema, ou o pai de um subtema).

        Args:
            tema_id: Tema.
            temas: Árvore por ID.

        Returns:
            ID do tema de nível 1.
        """
        tema: TemaPreparado = temas[tema_id]
        if tema.nivel >= 2 and tema.parent_id:
            return tema.parent_id
        return tema_id

    def _atributos_fora(
        self,
        questao: QuestaoPreparada,
        documentos: Sequence[DocumentoTema],
        indice: IndiceBM25,
        temas: Sequence[TemaPreparado],
    ) -> AtributosFora:
        """Calcula os atributos de separação do fora.

        Args:
            questao: Questão.
            documentos: Documentos indexados.
            indice: Índice BM25.
            temas: Árvore preparada.

        Returns:
            Atributos.
        """
        por_id: dict[str, TemaPreparado] = {t.tema_id: t for t in temas}
        pontos: Matriz = np.sort(indice.pontuar(self._tokenizador.termos(MontadorDocumentos.texto_questao(questao))))
        primeiro: float = float(pontos[-1]) if pontos.size else 0.0
        segundo: float = float(pontos[-2]) if pontos.size > 1 else 0.0
        ramos: list[str] = []
        texto: str
        for texto in MontadorDocumentos.textos_alternativas(questao).values():
            termos: list[str] = self._tokenizador.termos(texto)
            if not termos:
                continue
            pontos_alt: Matriz = indice.pontuar(termos)
            if float(pontos_alt.max()) > 0:
                ramos.append(self._ramo_nivel1(documentos[int(np.argmax(pontos_alt))].tema_id, por_id))
        alternativas: int = len(MontadorDocumentos.textos_alternativas(questao))
        dispersao: float = len(set(ramos)) / len(ramos) if ramos else (math.nan if alternativas == 0 else 0.0)
        origem: Mapping[str, object] = questao.original
        assunto: str = str(origem.get("assunto_origem") or "")
        disciplina: str = str(origem.get("disciplina_origem") or "")
        return AtributosFora(
            id=questao.id,
            pontuacao_maxima=primeiro,
            margem=(primeiro - segundo) / primeiro if primeiro > 0 else 0.0,
            dispersao=dispersao,
            generico=questao.marcas.enunciado_generico,
            parte_n_origem=self._processador.tem_parte(assunto),
            origem_fora_do_recorte=disciplina not in self._eda.mapa_disciplinas,
        )

    def _colunas_fora(self, atributos: Sequence[AtributosFora]) -> dict[str, list[float]]:
        """Pontuação de "chance de ser fora" de cada atributo (maior = mais provável fora).

        Args:
            atributos: Atributos na ordem da folha.

        Returns:
            ``nome -> valores``; a dispersão ausente (certo/errado) vira 0.
        """
        return {
            "pontuação máxima baixa": [-a.pontuacao_maxima for a in atributos],
            "margem baixa": [-a.margem for a in atributos],
            "dispersão entre alternativas": [0.0 if math.isnan(a.dispersao) else a.dispersao for a in atributos],
            "enunciado genérico": [1.0 if a.generico else 0.0 for a in atributos],
            "(Parte N) no assunto de origem": [1.0 if a.parte_n_origem else 0.0 for a in atributos],
            "disciplina de origem fora do recorte": [1.0 if a.origem_fora_do_recorte else 0.0 for a in atributos],
        }

    def _metricas_e11(
        self, folha: Sequence[RotuloFolha], atributos: Sequence[AtributosFora], temas: Sequence[TemaPreparado]
    ) -> list[Metrica]:
        """AUC de cada atributo e da logística fora da amostra.

        Args:
            folha: Rótulos.
            atributos: Atributos, na ordem da folha.
            temas: Árvore preparada.

        Returns:
            Métricas do E11.
        """
        p: ParametrosSistema = self._parametros
        fora: list[bool] = [r.fora for r in folha]
        metricas: list[Metrica] = []
        colunas: dict[str, list[float]] = self._colunas_fora(atributos)
        nome: str
        valores: list[float]
        for nome, valores in colunas.items():
            auc: float = MetricasBinarias.auc(valores, fora)
            baixo: float
            alto: float
            baixo, alto = MetricasBinarias.intervalo_auc(valores, fora, p.reamostras_auc, p.semente)
            metricas.append(Metrica("E11", nome, "AUC", auc, f"IC 90%: {baixo:.2f}–{alto:.2f}"))
        selecionadas: list[str] = ["pontuação máxima baixa", "margem baixa", "dispersão entre alternativas"]
        x: Matriz = np.array([[colunas[c][i] for c in selecionadas] for i in range(len(folha))], dtype=np.float64)
        y: Matriz = np.array([1.0 if f else 0.0 for f in fora], dtype=np.float64)
        validacao: ValidacaoCruzadaRepetida = ValidacaoCruzadaRepetida(
            p.partes_validacao, p.repeticoes_validacao, p.semente
        )
        estratos: list[str] = ValidacaoCruzadaRepetida.estratos_folha(folha, temas)
        previsao: Matriz = ValidacaoCruzadaRepetida.logistica_fora_da_amostra(x, y, validacao.particoes(estratos), 1.0)
        previstas: list[float] = [float(v) for v in previsao]
        auc_cv: float = MetricasBinarias.auc(previstas, fora)
        baixo_cv: float
        alto_cv: float
        baixo_cv, alto_cv = MetricasBinarias.intervalo_auc(previstas, fora, p.reamostras_auc, p.semente)
        metricas.append(
            Metrica(
                "E11",
                "logística: " + ", ".join(selecionadas),
                "AUC fora da amostra",
                auc_cv,
                f"IC 90%: {baixo_cv:.2f}–{alto_cv:.2f}; {p.partes_validacao} partes × {p.repeticoes_validacao} repetições",
            )
        )
        return metricas

    def _gravar(
        self,
        metricas: Sequence[Metrica],
        rankings: Sequence[RankingQuestao],
        folha: Sequence[RotuloFolha],
        atributos: Sequence[AtributosFora],
        notas: Sequence[str],
    ) -> Path:
        """Grava o CSV de métricas, o ranking por questão e o relatório.

        Args:
            metricas: Métricas.
            rankings: Rankings da variante com cartão.
            folha: Rótulos.
            atributos: Atributos de fora.
            notas: Parágrafos depois da tabela do relatório.

        Returns:
            Caminho do relatório.
        """
        pasta: Path = self._caminhos.saida_etapa2
        pasta.mkdir(parents=True, exist_ok=True)
        arquivo: TextIO
        linhas_metricas: list[list[str]] = [["experimento", "variante", "metrica", "valor", "detalhe"]]
        linhas_metricas.extend([m.experimento, m.variante, m.nome, f"{m.valor:.4f}", m.detalhe] for m in metricas)
        with (pasta / "resultados_etapa2.csv").open("w", encoding="utf-8", newline="") as arquivo:
            csv.writer(arquivo).writerows(linhas_metricas)
        linhas_ranking: list[list[str]] = [
            ["id", "fora", "tema_central", "extras", "top1", "pontos_top1", "primeiro_acerto"]
        ]
        linhas_ranking.extend(
            [
                rotulo.id,
                str(int(rotulo.fora)),
                rotulo.tema_central_id,
                ";".join(rotulo.extras_ids),
                ranking.ordem[0],
                f"{ranking.pontos[0]:.3f}",
                str(ranking.primeiro_acerto),
            ]
            for rotulo, ranking in zip(folha, rankings, strict=True)
        )
        with (pasta / "e7_ranking_folha.csv").open("w", encoding="utf-8", newline="") as arquivo:
            csv.writer(arquivo).writerows(linhas_ranking)
        destino: Path = pasta / "experimentos_etapa2.md"
        destino.write_text("\n".join(self._markdown(metricas, folha, atributos, notas)) + "\n", encoding="utf-8")
        print(f"Experimentos da etapa 2: {destino}")
        return destino

    def _markdown(
        self,
        metricas: Sequence[Metrica],
        folha: Sequence[RotuloFolha],
        atributos: Sequence[AtributosFora],
        notas: Sequence[str],
    ) -> list[str]:
        """Monta o relatório.

        Args:
            metricas: Métricas.
            folha: Rótulos.
            atributos: Atributos de fora.
            notas: Parágrafos depois da tabela (vencedores pelas regras pré-registradas).

        Returns:
            Linhas do Markdown.
        """
        linhas: list[str] = [
            "# Experimentos da etapa 2 (folha-verdade)",
            "",
            (
                f"Gerado em {datetime.now():%d/%m/%Y %H:%M}. Base: {len(folha)} questões da folha-verdade "
                f"({sum(1 for r in folha if not r.fora)} com tema, {sum(1 for r in folha if r.fora)} fora). "
                "Régua da etapa 2: tema central, extra, ou pai ou filho de um deles. Nenhum modelo foi chamado."
            ),
            "",
            "| Experimento | Variante | Métrica | Valor | Detalhe |",
            "|---|---|---|---:|---|",
        ]
        linhas.extend(f"| {m.experimento} | {m.variante} | {m.nome} | {m.valor:.3f} | {m.detalhe} |" for m in metricas)
        linhas.extend(["", *notas])
        linhas.extend(
            [
                "",
                "## E11: atributos das questões fora × mediana das questões com tema",
                "",
                "| Questão | Pontuação máxima | Margem | Dispersão | Genérico | (Parte N) | Origem fora |",
                "|---|---:|---:|---:|---|---|---|",
            ]
        )
        dentro: list[AtributosFora] = [a for a, r in zip(atributos, folha, strict=True) if not r.fora]
        linhas.append(
            "| **mediana (com tema)** | "
            f"{float(np.median([a.pontuacao_maxima for a in dentro])):.2f} | "
            f"{float(np.median([a.margem for a in dentro])):.2f} | "
            f"{float(np.nanmedian([a.dispersao for a in dentro])):.2f} | | | |"
        )
        a: AtributosFora
        r: RotuloFolha
        for a, r in zip(atributos, folha, strict=True):
            if r.fora:
                dispersao: str = "—" if math.isnan(a.dispersao) else f"{a.dispersao:.2f}"
                linhas.append(
                    f"| {a.id} | {a.pontuacao_maxima:.2f} | {a.margem:.2f} | {dispersao} | "
                    f"{'sim' if a.generico else 'não'} | {'sim' if a.parte_n_origem else 'não'} | "
                    f"{'sim' if a.origem_fora_do_recorte else 'não'} |"
                )
        return linhas
