"""Passo de citações da fase de conhecimento (ADR-021, decisão 3): regex nas 659 questões, sem modelo.

Grava ``dados/conhecimento/citacoes.jsonl`` com a proveniência no manifesto e o relatório
``saidas/etapa2/citacoes.md``. O relatório mede a cobertura, lista os pendentes, cruza as citações com o
mapa de artigos (o final, se já houver revisão; senão a proposta) e sorteia uma amostra para a conferência
do autor.
"""

from __future__ import annotations

import random
from collections import Counter
from collections.abc import Mapping, Sequence
from datetime import datetime
from pathlib import Path

from vicio_ia.configuracao import Caminhos, ParametrosSistema
from vicio_ia.enriquecimento.citacoes import ArquivoCitacoes, ArtigoCitado, CitacoesQuestao, ExtratorCitacoes
from vicio_ia.enriquecimento.manifesto import Manifesto
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada
from vicio_ia.sistema.documentos import MontadorDocumentos
from vicio_ia.sistema.folha import LeitorFolha, ReguaEtapa2, RotuloFolha
from vicio_ia.sistema.mapa_artigos import LinhaMapa, MapaArtigos


class PipelineCitacoes:
    """Extrai as citações, grava o artefato e o relatório."""

    COMANDO: str = "uv run python executar_citacoes.py"

    def __init__(self, caminhos: Caminhos | None = None, parametros: ParametrosSistema | None = None) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto.
            parametros: Parâmetros do sistema.
        """
        self._caminhos: Caminhos = caminhos or Caminhos.padrao()
        self._parametros: ParametrosSistema = parametros or ParametrosSistema()

    def executar(self) -> Path:
        """Extrai e grava.

        Returns:
            Caminho do relatório.
        """
        leitor: LeitorPreparados = LeitorPreparados(self._caminhos)
        questoes: list[QuestaoPreparada] = leitor.questoes()
        temas: list[TemaPreparado] = leitor.temas()
        extrator: ExtratorCitacoes = ExtratorCitacoes()
        citacoes: list[CitacoesQuestao] = [
            extrator.extrair(q.id, MontadorDocumentos.texto_questao(q)) for q in questoes
        ]
        pasta: Path = self._caminhos.dados_conhecimento
        destino: Path = ArquivoCitacoes(pasta / "citacoes.jsonl").gravar(citacoes)
        regra: Path = self._caminhos.raiz / "vicio_ia" / "enriquecimento" / "citacoes.py"
        Manifesto(pasta / "manifesto.json", self._caminhos.raiz).registrar(
            destino,
            "regra",
            self.COMANDO,
            {
                "regra": f"vicio_ia/enriquecimento/citacoes.py@{Manifesto.sha256(regra)[:12]}",
                "entrada": "dados/preparados/questoes.jsonl (enunciado, comando e alternativas)",
                "questoes": str(len(citacoes)),
                "artigos": str(sum(len(c.artigos) for c in citacoes)),
                "pendentes": str(sum(len(c.pendentes) for c in citacoes)),
                "modelo": "nenhum",
            },
        )
        folha: list[RotuloFolha] = LeitorFolha(self._caminhos.folha_verdade, temas, {q.id for q in questoes}).ler()
        return self._relatorio(citacoes, temas, folha)

    def _arquivo_mapa(self) -> Path:
        """Mapa final, se a revisão já o montou; senão, a proposta.

        Returns:
            Caminho do mapa.
        """
        final: Path = self._caminhos.dados_conhecimento / "mapa_artigos.csv"
        return final if final.is_file() else self._caminhos.dados_conhecimento / "propostas" / "mapa_artigos.csv"

    def _relatorio(
        self, citacoes: Sequence[CitacoesQuestao], temas: Sequence[TemaPreparado], folha: Sequence[RotuloFolha]
    ) -> Path:
        """Grava o relatório do passo.

        Args:
            citacoes: Citações por questão.
            temas: Árvore preparada.
            folha: Folha-verdade.

        Returns:
            Caminho do relatório.
        """
        p: ParametrosSistema = self._parametros
        com_artigo: list[CitacoesQuestao] = [c for c in citacoes if c.artigos]
        antigas: int = sum(1 for c in com_artigo if self._antiga(c.id))
        novas: int = len(com_artigo) - antigas
        total_antigas: int = sum(1 for c in citacoes if self._antiga(c.id))
        ids_folha: set[str] = {r.id for r in folha}
        resolucoes: Counter[str] = Counter(a.resolucao for c in citacoes for a in c.artigos)
        leis: Counter[str] = Counter(a.lei for c in citacoes for a in c.artigos)
        pendentes: list[tuple[str, str]] = [(c.id, t) for c in citacoes for t in c.pendentes]
        arquivo_mapa: Path = self._arquivo_mapa()
        mapa: MapaArtigos = MapaArtigos.ler(arquivo_mapa)
        temas_mapa: dict[str, list[str]] = {c.id: self._temas_mapa(c, mapa) for c in com_artigo}
        no_mapa: list[str] = [i for i, t in temas_mapa.items() if t]
        relativo: str = arquivo_mapa.relative_to(self._caminhos.raiz).as_posix()
        linhas: list[str] = [
            "# Citações de lei e artigo nas questões",
            "",
            (
                f"Gerado em {datetime.now():%d/%m/%Y %H:%M} por `{self.COMANDO}`. Extração só por expressões "
                "regulares, sem modelo de linguagem (ADR-021). Artefato: `dados/conhecimento/citacoes.jsonl`."
            ),
            "",
            "## Cobertura",
            "",
            (
                f"- Questões com pelo menos um artigo citado: {len(com_artigo)} de {len(citacoes)} "
                f"({antigas} de {total_antigas} antigas e {novas} de {len(citacoes) - total_antigas} novas); "
                f"{sum(1 for c in com_artigo if c.id in ids_folha)} delas estão na folha-verdade."
            ),
            f"- Questões que citam alguma lei, com ou sem artigo: {sum(1 for c in citacoes if c.leis)}.",
            (
                f"- Artigos com a lei resolvida: {sum(resolucoes.values())} "
                f"({', '.join(f'{r} {q}' for r, q in resolucoes.most_common())})."
            ),
            f"- Artigos sem lei resolvida (pendentes): {len(pendentes)}.",
            f"- Artigos por lei: {', '.join(f'{lei} ({q})' for lei, q in leis.most_common())}.",
            "",
            (
                "As resoluções são: `explicita` (a lei está junto do artigo), `enumeracao` (herdada do artigo "
                'seguinte da mesma enumeração), `anafora` ("do mesmo diploma"), `repeticao` (o mesmo artigo já '
                "apareceu com a lei) e `contexto` (a questão só cita uma lei)."
            ),
            "",
        ]
        if pendentes:
            linhas.extend(["## Pendentes", "", "| Questão | Trecho |", "|---|---|"])
            linhas.extend(f"| {i} | {self._celula(t)} |" for i, t in pendentes)
            linhas.append("")
        linhas.extend(self._secao_mapa(relativo, com_artigo, temas_mapa, no_mapa, temas, folha))
        linhas.extend(self._secao_amostra(citacoes, p))
        pasta: Path = self._caminhos.saida_etapa2
        pasta.mkdir(parents=True, exist_ok=True)
        destino: Path = pasta / "citacoes.md"
        destino.write_text("\n".join(linhas), encoding="utf-8")
        print(
            f"Citações: {len(com_artigo)} questões com artigo, {sum(resolucoes.values())} artigos resolvidos, "
            f"{len(pendentes)} pendentes; {len(no_mapa)} questões batem no mapa ({relativo})."
            f"\nRelatório: {destino}"
        )
        return destino

    def _secao_mapa(
        self,
        relativo: str,
        com_artigo: Sequence[CitacoesQuestao],
        temas_mapa: Mapping[str, list[str]],
        no_mapa: Sequence[str],
        temas: Sequence[TemaPreparado],
        folha: Sequence[RotuloFolha],
    ) -> list[str]:
        """Cruza as citações com o mapa de artigos e mede o acerto na folha pela régua da etapa 2.

        Args:
            relativo: Mapa usado (caminho relativo).
            com_artigo: Questões com artigo citado.
            temas_mapa: Temas do mapa por questão.
            no_mapa: Questões com algum tema no mapa.
            temas: Árvore preparada.
            folha: Folha-verdade.

        Returns:
            Linhas da seção.
        """
        regua: ReguaEtapa2 = ReguaEtapa2(temas)
        caminho: dict[str, str] = {t.tema_id: t.caminho_exibicao for t in temas}
        avaliadas: list[tuple[RotuloFolha, list[str]]] = [(r, temas_mapa[r.id]) for r in folha if temas_mapa.get(r.id)]
        com_tema: list[tuple[RotuloFolha, list[str]]] = [(r, t) for r, t in avaliadas if not r.fora]
        algum: int = sum(1 for r, t in com_tema if any(regua.acerta(x, r) for x in t))
        todos: int = sum(1 for r, t in com_tema if all(regua.acerta(x, r) for x in t))
        unico: int = sum(1 for _, t in com_tema if len(t) == 1)
        linhas: list[str] = [
            "## Citações × mapa de artigos",
            "",
            f"Mapa usado: `{relativo}`.",
            "",
            (
                f"- Questões com artigo citado que acham pelo menos uma linha no mapa: {len(no_mapa)} de "
                f"{len(com_artigo)}."
            ),
            (
                f"- Na folha-verdade: {len(avaliadas)} questões acham linha no mapa; "
                f"fora da taxonomia entre elas: {sum(1 for r, _ in avaliadas if r.fora)}."
            ),
            (
                f"- Das {len(com_tema)} com tema: em {algum}, algum tema do mapa acerta pela régua; em {todos}, todos "
                f"acertam; em {unico}, o mapa aponta um único tema."
            ),
            "",
            "| Questão | Fora | Temas do mapa | Acerto pela régua |",
            "|---|---|---|---|",
        ]
        rotulo: RotuloFolha
        alvos: list[str]
        for rotulo, alvos in avaliadas:
            acertos: str = "—" if rotulo.fora else ", ".join("sim" if regua.acerta(x, rotulo) else "não" for x in alvos)
            nomes: str = "; ".join(f"{x} {caminho.get(x, '?')}" for x in alvos)
            linhas.append(f"| {rotulo.id} | {'sim' if rotulo.fora else 'não'} | {self._celula(nomes)} | {acertos} |")
        linhas.append("")
        return linhas

    def _secao_amostra(self, citacoes: Sequence[CitacoesQuestao], p: ParametrosSistema) -> list[str]:
        """Sorteia artigos citados para o autor conferir a extração.

        Args:
            citacoes: Citações por questão.
            p: Parâmetros (tamanho da amostra e semente).

        Returns:
            Linhas da seção.
        """
        todos: list[tuple[str, ArtigoCitado]] = [(c.id, a) for c in citacoes for a in c.artigos]
        sorteio: random.Random = random.Random(p.semente)
        amostra: list[tuple[str, ArtigoCitado]] = sorted(
            sorteio.sample(todos, min(p.amostra_conferencia, len(todos))), key=lambda x: x[0]
        )
        linhas: list[str] = [
            f"## Amostra para conferência ({len(amostra)} artigos sorteados, semente {p.semente})",
            "",
            "Marque na última coluna se a lei e o artigo extraídos estão certos.",
            "",
            "| Questão | Lei | Artigos | Resolução | Trecho | Certo? |",
            "|---|---|---|---|---|---|",
        ]
        questao: str
        artigo: ArtigoCitado
        for questao, artigo in amostra:
            artigos: str = str(artigo.inicio) if artigo.inicio == artigo.fim else f"{artigo.inicio}–{artigo.fim}"
            linhas.append(
                f"| {questao} | {artigo.lei} | {artigos} | {artigo.resolucao} | {self._celula(artigo.trecho)} | |"
            )
        linhas.append("")
        return linhas

    @staticmethod
    def _temas_mapa(citacao: CitacoesQuestao, mapa: MapaArtigos) -> list[str]:
        """Temas do mapa para os artigos citados, sem repetição, na ordem em que aparecem.

        Args:
            citacao: Citações da questão.
            mapa: Mapa de artigos.

        Returns:
            IDs dos temas.
        """
        temas: list[str] = []
        artigo: ArtigoCitado
        linha: LinhaMapa
        for artigo in citacao.artigos:
            for linha in mapa.linhas(artigo.lei, artigo.inicio, artigo.fim):
                if linha.tema_id not in temas:
                    temas.append(linha.tema_id)
        return temas

    def _antiga(self, questao_id: str) -> bool:
        """Diz se a questão é da etapa 1.

        Args:
            questao_id: ID (``Q0001``).

        Returns:
            ``True`` para Q0001 a Q0359.
        """
        return int(questao_id[1:]) <= self._parametros.questoes_etapa1

    @staticmethod
    def _celula(texto: str) -> str:
        """Texto seguro para uma célula de tabela Markdown.

        Args:
            texto: Texto.

        Returns:
            Texto sem barras verticais nem quebras de linha.
        """
        return texto.replace("|", "/").replace("\n", " ")
