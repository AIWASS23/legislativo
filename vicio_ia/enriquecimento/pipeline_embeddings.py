"""Passo de embeddings da fase de conhecimento (ADR-021): vetores dos candidatos, E8 e E9, e a exportação.

1. Gera, com cache por conteúdo, os vetores de cada modelo candidato para as 659 questões, as alternativas e os
   documentos de tema (os mesmos do BM25: título, caminho e cartão).
2. Mede o E8 e o E9 na folha-verdade (só numpy; nenhum modelo é chamado na medição).
3. Exporta os vetores do modelo escolhido (``ParametrosEmbeddings.escolhido``) para
   ``dados/conhecimento/embeddings/``, com a proveniência no manifesto. É só isso que a fase de decisão lê.
"""

from __future__ import annotations

import csv
import hashlib
from collections.abc import Mapping, Sequence
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from typing import TextIO

from vicio_ia.configuracao import (
    Caminhos,
    ModeloEmbedding,
    ParametrosEDA,
    ParametrosEmbeddings,
    ParametrosLLM,
    ParametrosSistema,
)
from vicio_ia.enriquecimento.embeddings import GeradorEmbeddings
from vicio_ia.enriquecimento.manifesto import Manifesto
from vicio_ia.estatistica import Matriz
from vicio_ia.llm.embeddings import ProvedorEmbedding
from vicio_ia.llm.fabrica import FabricaProvedores
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada
from vicio_ia.sistema.base_temas import ArquivoBaseTemas, TemaBase
from vicio_ia.sistema.documentos import DocumentoTema, MontadorDocumentos
from vicio_ia.sistema.experimento_embeddings import CandidatoEmbedding, ExperimentoEmbeddings, ResultadoE8
from vicio_ia.sistema.folha import LeitorFolha, RotuloFolha
from vicio_ia.sistema.lexical import IndiceBM25, TokenizadorLexical
from vicio_ia.sistema.ranking import AvaliadorRanking, Metrica, RankingQuestao, RegraEscolha
from vicio_ia.sistema.vetores import ArquivoVetores, ConjuntoVetores, VetoresConhecimento
from vicio_ia.texto import ProcessadorTexto


class PipelineEmbeddings:
    """Gera os vetores, mede o E8 e o E9 e exporta o modelo escolhido."""

    COMANDO: str = "uv run python executar_embeddings.py"

    def __init__(
        self,
        caminhos: Caminhos | None = None,
        parametros: ParametrosEmbeddings | None = None,
        sistema: ParametrosSistema | None = None,
        parametros_llm: ParametrosLLM | None = None,
    ) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto.
            parametros: Parâmetros dos embeddings.
            sistema: Parâmetros do sistema (BM25, recall@k).
            parametros_llm: Parâmetros de LLM (endereço do Ollama).
        """
        self._caminhos: Caminhos = caminhos or Caminhos.padrao()
        self._parametros: ParametrosEmbeddings = parametros or ParametrosEmbeddings()
        self._sistema: ParametrosSistema = sistema or ParametrosSistema()
        self._parametros_llm: ParametrosLLM = parametros_llm or ParametrosLLM()

    def executar(self) -> Path:
        """Roda o passo inteiro.

        Returns:
            Caminho do relatório do E8.

        Raises:
            ValueError: Se o modelo escolhido não estiver entre os candidatos.
        """
        p: ParametrosEmbeddings = self._parametros
        if p.escolhido not in {m.nome for m in p.candidatos}:
            raise ValueError(f"modelo escolhido {p.escolhido!r} não está entre os candidatos do E8")
        leitor: LeitorPreparados = LeitorPreparados(self._caminhos)
        questoes: list[QuestaoPreparada] = leitor.questoes()
        temas: list[TemaPreparado] = leitor.temas()
        folha: list[RotuloFolha] = LeitorFolha(self._caminhos.folha_verdade, temas, {q.id for q in questoes}).ler()
        base: list[TemaBase] = ArquivoBaseTemas(self._caminhos.dados_conhecimento / "temas.jsonl").ler()
        documentos: list[DocumentoTema] = MontadorDocumentos.documentos_base(base, p.documento_e8)
        textos: dict[str, dict[str, str]] = {
            "questoes": {q.id: MontadorDocumentos.texto_questao(q) for q in questoes},
            "alternativas": {
                f"{q.id}:{letra}": texto
                for q in questoes
                for letra, texto in MontadorDocumentos.textos_alternativas(q).items()
            },
            "temas": {d.tema_id: d.texto for d in documentos},
            "inativos": {
                t.tema_id: f"{t.titulo_exibicao}\n{t.caminho_exibicao}" for t in temas if t.status != "active"
            },
        }
        provedor: ProvedorEmbedding = FabricaProvedores(self._caminhos, self._parametros_llm).obter_embedding(
            p.provedor, p.timeout_segundos
        )
        print(
            f"Embeddings: {len(p.candidatos)} modelos × ({len(textos['questoes'])} questões, "
            f"{len(textos['alternativas'])} alternativas, {len(textos['temas'])} temas), via {provedor.nome}"
        )
        vetores: dict[str, VetoresConhecimento] = {}
        geradores: dict[str, GeradorEmbeddings] = {}
        modelo: ModeloEmbedding
        for modelo in p.candidatos:
            gerador: GeradorEmbeddings = GeradorEmbeddings(provedor, modelo, self._caminhos.runs / "embeddings", p.lote)
            vetores[modelo.nome] = VetoresConhecimento(
                modelo=modelo.nome,
                questoes=self._conjunto(gerador, textos["questoes"], True),
                alternativas=self._conjunto(gerador, textos["alternativas"], True),
                temas=self._conjunto(gerador, textos["temas"], False),
                inativos=self._conjunto(gerador, textos["inativos"], False),
            )
            geradores[modelo.nome] = gerador
            print(
                f"  {modelo.nome}: {gerador.calculados} vetores calculados agora "
                f"({gerador.segundos:.0f} s), dimensão {vetores[modelo.nome].temas.matriz.shape[1]}"
            )
        ids_temas: list[str] = [d.tema_id for d in documentos]
        pontos_bm25: list[Matriz] = self._bm25(documentos, {q.id: q for q in questoes}, folha)
        experimento: ExperimentoEmbeddings = ExperimentoEmbeddings(
            temas, folha, ids_temas, pontos_bm25, self._sistema.top_k_recall, p.rrf_k, p.vizinhos_knn
        )
        candidatos: list[CandidatoEmbedding] = [
            CandidatoEmbedding(
                nome, v.questoes.submatriz([r.id for r in folha]), v.temas.matriz, geradores[nome].segundos
            )
            for nome, v in vetores.items()
        ]
        resultado: ResultadoE8 = experimento.medir(candidatos)
        avaliador: AvaliadorRanking = AvaliadorRanking(temas, self._sistema.top_k_recall)
        rankings_bm25: list[RankingQuestao] = [
            avaliador.ordenar(r, pontos_bm25[i], ids_temas) for i, r in enumerate(folha)
        ]
        referencia: list[Metrica] = avaliador.metricas("E7", "BM25 com cartão (referência)", folha, rankings_bm25)
        gerador_escolhido: GeradorEmbeddings = geradores[p.escolhido]
        textos_variante: dict[str, dict[str, str]] = {
            v: {d.tema_id: d.texto for d in MontadorDocumentos.documentos_base(base, v)} for v in TemaBase.VARIANTES
        }
        temas_variante: dict[str, Matriz] = {
            v: gerador_escolhido.vetores(list(t.values()), False) for v, t in textos_variante.items()
        }
        questoes_por_id: dict[str, QuestaoPreparada] = {q.id: q for q in questoes}
        metricas_e8b: list[Metrica] = experimento.medir_documentos(
            vetores[p.escolhido].questoes.submatriz([r.id for r in folha]),
            temas_variante,
            {
                v: self._bm25(MontadorDocumentos.documentos_base(base, v), questoes_por_id, folha)
                for v in TemaBase.VARIANTES
            },
        )
        vencedor_e8b: str = RegraEscolha.escolher(
            metricas_e8b, "E8b", [f"{v}: denso" for v in TemaBase.VARIANTES]
        ).removesuffix(": denso")
        exportados: VetoresConhecimento = replace(
            vetores[p.escolhido],
            temas=ConjuntoVetores(tuple(textos_variante[p.documento_tema]), temas_variante[p.documento_tema]),
        )
        escolhido: ModeloEmbedding = next(m for m in p.candidatos if m.nome == p.escolhido)
        self._exportar(exportados, escolhido, gerador_escolhido, {**textos, "temas": textos_variante[p.documento_tema]})
        return self._relatorio(
            [*referencia, *resultado.metricas, *metricas_e8b], resultado.vencedor, vencedor_e8b, vetores
        )

    @staticmethod
    def _conjunto(gerador: GeradorEmbeddings, textos: Mapping[str, str], consulta: bool) -> ConjuntoVetores:
        """Vetores de um conjunto de textos.

        Args:
            gerador: Gerador do modelo.
            textos: ``id -> texto``.
            consulta: Questões e alternativas (``True``) ou documentos de tema (``False``).

        Returns:
            Conjunto com IDs e vetores normalizados.
        """
        return ConjuntoVetores(tuple(textos), gerador.vetores(list(textos.values()), consulta))

    def _bm25(
        self,
        documentos: Sequence[DocumentoTema],
        questoes: Mapping[str, QuestaoPreparada],
        folha: Sequence[RotuloFolha],
    ) -> list[Matriz]:
        """Pontuação BM25 das questões da folha contra os documentos de tema (a mesma do E7).

        Args:
            documentos: Documentos de tema.
            questoes: Questões por ID.
            folha: Rótulos.

        Returns:
            Uma pontuação por questão da folha.
        """
        s: ParametrosSistema = self._sistema
        tokenizador: TokenizadorLexical = TokenizadorLexical(ProcessadorTexto(), ParametrosEDA().palavras_sem_conteudo)
        indice: IndiceBM25 = IndiceBM25([tokenizador.termos(d.texto) for d in documentos], s.bm25_k1, s.bm25_b)
        return [indice.pontuar(tokenizador.termos(MontadorDocumentos.texto_questao(questoes[r.id]))) for r in folha]

    def _exportar(
        self,
        vetores: VetoresConhecimento,
        modelo: ModeloEmbedding,
        gerador: GeradorEmbeddings,
        textos: Mapping[str, Mapping[str, str]],
    ) -> None:
        """Grava os vetores do modelo escolhido como artefato versionado e registra o manifesto.

        Args:
            vetores: Vetores do modelo.
            modelo: Modelo e prefixos.
            gerador: Gerador (digest).
            textos: Textos de entrada por conjunto (para o hash).
        """
        hashes: dict[str, str] = {
            f"sha256_textos_{nome}": hashlib.sha256(
                "\n".join(f"{i}\t{t}" for i, t in conjunto.items()).encode("utf-8")
            ).hexdigest()
            for nome, conjunto in textos.items()
        }
        info: dict[str, str] = {
            "provedor": self._parametros.provedor,
            "modelo": modelo.nome,
            "digest": gerador.digest,
            "dimensao": str(vetores.temas.matriz.shape[1]),
            "contexto_tokens": str(modelo.contexto_tokens),
            "prefixo_consulta": modelo.prefixo_consulta,
            "prefixo_documento": modelo.prefixo_documento,
            "documento_tema": f"{self._parametros.documento_tema} (TemaBase.texto, dados/conhecimento/temas.jsonl)",
            "gerado_em": datetime.now().isoformat(timespec="seconds"),
            **hashes,
        }
        pasta: Path = self._caminhos.dados_conhecimento / "embeddings"
        manifesto: Manifesto = Manifesto(self._caminhos.dados_conhecimento / "manifesto.json", self._caminhos.raiz)
        detalhes: dict[str, str] = {k: v for k, v in info.items() if k != "gerado_em"}
        arquivo: Path
        for arquivo in ArquivoVetores(pasta).gravar(vetores, info):
            manifesto.registrar(arquivo, "embedding", self.COMANDO, detalhes)
        print(f"Exportado: {modelo.nome} ({gerador.digest[:12]}) em {pasta}")

    def _relatorio(
        self,
        metricas: Sequence[Metrica],
        vencedor: str,
        vencedor_e8b: str,
        vetores: Mapping[str, VetoresConhecimento],
    ) -> Path:
        """Grava o CSV de métricas e o relatório do E8, do E9 e do E8b.

        Args:
            metricas: Métricas (a referência do BM25 primeiro).
            vencedor: Modelo vencedor do E8 pela regra pré-registrada.
            vencedor_e8b: Documento de tema vencedor do E8b.
            vetores: Vetores por modelo (para a dimensão).

        Returns:
            Caminho do relatório.
        """
        pasta: Path = self._caminhos.saida_etapa2
        pasta.mkdir(parents=True, exist_ok=True)
        linhas_csv: list[list[str]] = [["experimento", "variante", "metrica", "valor", "detalhe"]]
        linhas_csv.extend([m.experimento, m.variante, m.nome, f"{m.valor:.4f}", m.detalhe] for m in metricas)
        arquivo: TextIO
        with (pasta / "e8_resultados.csv").open("w", encoding="utf-8", newline="") as arquivo:
            csv.writer(arquivo).writerows(linhas_csv)

        def celula(variante: str, nome: str) -> str:
            """Valor de uma métrica em porcentagem, com a contagem.

            Args:
                variante: Variante.
                nome: Métrica.

            Returns:
                Texto da célula.
            """
            metrica: Metrica | None = next((m for m in metricas if m.variante == variante and m.nome == nome), None)
            return "—" if metrica is None else f"{metrica.valor:.0%} ({metrica.detalhe})"

        colunas: tuple[str, ...] = (
            "acerto top-1 (92 com tema)",
            "recall@5 (92)",
            "recall@10 (92)",
            "acerto top-1, tema central de nível 1",
            "acerto top-1, tema central de nível 2",
        )
        cabecalho: str = "| Variante | Top-1 (92) | Recall@5 | Recall@10 | Top-1, nível 1 | Top-1, nível 2 |"
        separador: str = "|---|---:|---:|---:|---:|---:|"
        variantes: list[str] = list(dict.fromkeys(m.variante for m in metricas if m.experimento in {"E7", "E8"}))
        knn: list[str] = list(
            dict.fromkeys(m.variante for m in metricas if m.experimento == "E9" and m.variante != "teto")
        )
        teto: Metrica = next(m for m in metricas if m.experimento == "E9" and m.variante == "teto")
        e8b: list[str] = list(dict.fromkeys(m.variante for m in metricas if m.experimento == "E8b"))
        tempos: list[str] = [
            f"- `{nome}`: dimensão {v.temas.matriz.shape[1]}, "
            f"{next(m.valor for m in metricas if m.variante == f'{nome}: denso' and m.nome.startswith('segundos')):.0f} s "
            "nesta rodada (0 quando tudo veio do cache)."
            for nome, v in vetores.items()
        ]
        linhas: list[str] = [
            "# E8 e E9: embeddings e kNN na folha-verdade",
            "",
            (
                f"Gerado em {datetime.now():%d/%m/%Y %H:%M} por `{self.COMANDO}`. Base: as 100 questões da "
                "folha-verdade (92 com tema), com a régua da etapa 2. Documento de tema: título, caminho e cartão "
                "(o mesmo do BM25 no E7). A medição só usa vetores já gravados; nenhum modelo de linguagem decide nada."
            ),
            "",
            "## E8: questão inteira × documentos de tema",
            "",
            cabecalho,
            separador,
            *(f"| {v} | " + " | ".join(celula(v, c) for c in colunas) + " |" for v in variantes),
            "",
            (
                f"**Vencedor pela regra pré-registrada** (maior recall@10 do denso; até uma questão de diferença é "
                f"empate, decidido pelo top-1): `{vencedor}`. Modelo exportado para `dados/conhecimento/embeddings/`: "
                f"`{self._parametros.escolhido}`."
            ),
            "",
            "Modelos:",
            "",
            *tempos,
            "",
            "## E9: kNN deixa-uma-fora entre as questões da folha",
            "",
            f"Teto: {teto.nome}: {teto.valor:.0%} ({teto.detalhe}).",
            "",
            cabecalho,
            separador,
            *(f"| {v} | " + " | ".join(celula(v, c) for c in colunas) + " |" for v in knn),
            "",
            f"## E8b: documento do tema com o `{self._parametros.escolhido}`",
            "",
            (
                "Variantes do texto do tema (`dados/conhecimento/temas.jsonl`): `cartao` (título, caminho, escopo, o "
                "que entra e âncoras), `cartao_termos` (mais os termos `forte` e `fraco`) e `cartao_termos_leis` "
                "(mais as referências do mapa revisado). A fusão usa o BM25 da mesma variante."
            ),
            "",
            cabecalho,
            separador,
            *(f"| {v} | " + " | ".join(celula(v, c) for c in colunas) + " |" for v in e8b),
            "",
            (
                f"**Vencedor pela regra pré-registrada** (sobre o denso): `{vencedor_e8b}`. Documento exportado para "
                f"`dados/conhecimento/embeddings/temas.npy`: `{self._parametros.documento_tema}`."
            ),
            "",
        ]
        destino: Path = pasta / "e8_embeddings.md"
        destino.write_text("\n".join(linhas), encoding="utf-8")
        print(f"Vencedor do E8 pela regra: {vencedor}; do E8b: {vencedor_e8b}. Relatório: {destino}")
        return destino
