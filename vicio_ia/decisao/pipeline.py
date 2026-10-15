"""Passo 07: decisão final, ``publicacao.csv`` e ``previsao.txt`` (ADR-010, ADR-011, ADR-013, ADR-015)."""

from __future__ import annotations

import csv
import json
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import ClassVar, TextIO

from vicio_ia.arvore import ArvoreTemas
from vicio_ia.avaliacao.amostragem import ArquivoAmostra
from vicio_ia.avaliacao.calibracao import (
    Calibrador,
    ExemploCalibracao,
    SeletorPenalidade,
    ValidacaoCalibracao,
    VetorizadorDecisao,
)
from vicio_ia.avaliacao.planilha import PlanilhaRotulos, RotuloGold, SituacaoLinha
from vicio_ia.avaliacao.pontuador import PontuadorRegua
from vicio_ia.avaliacao.previsao import PrevisorPrecisao, ResultadoPrevisao
from vicio_ia.carregamento import CarregadorDados
from vicio_ia.classificacao.respostas import SinaisQuestao
from vicio_ia.configuracao import Caminhos, ParametrosCalibracao, ParametrosGold
from vicio_ia.decisao.agregacao import AgregadorSinais, DecisaoPreliminar
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada
from vicio_ia.sinais.origem import SinalOrigem
from vicio_ia.texto import ProcessadorTexto


class ErroPublicacao(Exception):
    """O ``publicacao.csv`` gerado não respeita o formato do LEIA-ME."""


@dataclass(frozen=True)
class LinhaPublicacao:
    """Uma linha do ``publicacao.csv``.

    Attributes:
        id: ID da questão.
        decisao: ``publicar``, ``revisar`` ou ``fora``.
        tema_central_id: Tema (vazio em ``fora``).
        extras_ids: Outros temas, separados por ``;``.
        confianca: Chance de o tema central estar certo (em ``fora``, de ``fora`` estar certo).
        motivo: Obrigatório em ``revisar`` e ``fora``.
    """

    id: str
    decisao: str
    tema_central_id: str
    extras_ids: str
    confianca: float
    motivo: str


class PipelineDecisao:
    """Agrega os sinais, calibra no gold, escolhe o limiar e grava os entregáveis."""

    COLUNAS: ClassVar[tuple[str, ...]] = ("id", "decisao", "tema_central_id", "extras_ids", "confianca", "motivo")

    def __init__(
        self,
        caminhos: Caminhos | None = None,
        parametros: ParametrosCalibracao | None = None,
        parametros_gold: ParametrosGold | None = None,
    ) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto (opcional).
            parametros: Parâmetros da calibração e do limiar (opcional).
            parametros_gold: Parâmetros do gold set (opcional).
        """
        self._caminhos: Caminhos = caminhos if caminhos is not None else Caminhos.padrao()
        self._parametros: ParametrosCalibracao = parametros if parametros is not None else ParametrosCalibracao()
        self._gold: ParametrosGold = parametros_gold if parametros_gold is not None else ParametrosGold()

    def executar(self) -> Path:
        """Roda o passo 07.

        Returns:
            Caminho do ``publicacao.csv``.

        Raises:
            ErroPublicacao: Se o arquivo gerado não passar no validador.
        """
        leitor: LeitorPreparados = LeitorPreparados(self._caminhos)
        questoes: list[QuestaoPreparada] = leitor.questoes()
        temas: list[TemaPreparado] = leitor.temas()
        sinais: dict[str, SinaisQuestao] = self._sinais()
        agregador: AgregadorSinais = AgregadorSinais(temas)
        origem: SinalOrigem = SinalOrigem(temas, ProcessadorTexto())
        preliminares: dict[str, DecisaoPreliminar] = {
            q.id: agregador.decidir(sinais[q.id], q, origem.temas(q)) for q in questoes if q.id in sinais
        }
        pontuador: PontuadorRegua = PontuadorRegua(ArvoreTemas(CarregadorDados(self._caminhos).carregar_temas()))
        rotulos: dict[str, tuple[RotuloGold, float]] = self._rotulos(temas)
        exemplos: list[ExemploCalibracao] = []
        tolerante: dict[str, bool] = {}
        questao_id: str
        rotulo: RotuloGold
        peso: float
        for questao_id, (rotulo, peso) in rotulos.items():
            decisao: DecisaoPreliminar | None = preliminares.get(questao_id)
            if decisao is None or not decisao.tema_id or decisao.acao == "fora":
                continue
            exemplos.append(ExemploCalibracao(decisao, pontuador.acerta(decisao.tema_id, rotulo, "estrita"), peso))
            tolerante[questao_id] = pontuador.acerta(decisao.tema_id, rotulo, "tolerante")
        if len({e.acerto for e in exemplos}) < 2:
            raise ErroPublicacao(f"gold insuficiente para calibrar: {len(exemplos)} exemplos com tema")
        vetorizador: VetorizadorDecisao = VetorizadorDecisao()
        penalidade: float
        grade: list[tuple[float, ValidacaoCalibracao]]
        penalidade, grade = SeletorPenalidade(vetorizador).escolher(
            exemplos, self._parametros.penalidades_l2, self._parametros.partes_validacao, self._parametros.semente
        )
        validacao: ValidacaoCalibracao = next(v for pena, v in grade if pena == penalidade)
        coeficientes: dict[str, float] = Calibrador(penalidade, vetorizador).ajustar(exemplos).coeficientes
        com_tema: list[DecisaoPreliminar] = [d for d in preliminares.values() if d.tema_id and d.acao != "fora"]
        previsao: ResultadoPrevisao = PrevisorPrecisao(self._parametros, vetorizador, penalidade).prever(
            com_tema, exemplos, tolerante
        )
        linhas: list[LinhaPublicacao] = self._linhas(questoes, preliminares, sinais, previsao)
        self._validar(linhas, temas, len(questoes))
        destino: Path = self._gravar_csv(linhas)
        self._gravar_previsao(previsao, validacao, len(exemplos))
        self._gravar_preliminares(list(preliminares.values()), previsao)
        relatorio: Path = self._relatorio(
            linhas, preliminares, previsao, validacao, coeficientes, len(exemplos), penalidade, grade
        )
        contagem: Counter[str] = Counter(linha.decisao for linha in linhas)
        print(
            f"Decisão: {contagem['publicar']} publicar, {contagem['revisar']} revisar, {contagem['fora']} fora; "
            f"precisão prevista {previsao.precisao_ponto:.3f} ({previsao.precisao_intervalo[0]:.2f}–"
            f"{previsao.precisao_intervalo[1]:.2f}); cobertura {previsao.cobertura:.3f}; regra: {previsao.regra}"
        )
        print(f"Entregáveis: {destino}, {self._caminhos.raiz / 'previsao.txt'}\nRelatório: {relatorio}")
        return destino

    def _sinais(self) -> dict[str, SinaisQuestao]:
        """Lê ``sinais.jsonl``.

        Returns:
            Sinais por ID.

        Raises:
            ErroPublicacao: Se o arquivo não existir.
        """
        arquivo: Path = self._caminhos.dados_classificacao / "sinais.jsonl"
        if not arquivo.is_file():
            raise ErroPublicacao(f"{arquivo} não existe: rode `uv run python executar_classificacao.py`")
        sinais: dict[str, SinaisQuestao] = {}
        numero: int
        linha: str
        for numero, linha in enumerate(arquivo.read_text(encoding="utf-8").splitlines(), start=1):
            if linha.strip():
                valor: object = json.loads(linha)
                if isinstance(valor, dict):
                    item: SinaisQuestao = SinaisQuestao.de_dict(
                        {str(k): v for k, v in valor.items()}, f"sinais.jsonl:{numero}"
                    )
                    sinais[item.id] = item
        return sinais

    def _rotulos(self, temas: Sequence[TemaPreparado]) -> dict[str, tuple[RotuloGold, float]]:
        """Lê os rótulos válidos das levas, com o peso amostral (inverso da probabilidade de inclusão).

        Args:
            temas: Árvore preparada.

        Returns:
            ``ID -> (rótulo, peso)``.
        """
        rotulos: dict[str, tuple[RotuloGold, float]] = {}
        leva: int
        for leva in (1, 2):
            amostra: ArquivoAmostra = ArquivoAmostra(self._caminhos.dados_gold / f"amostra_leva{leva}.csv")
            planilha: PlanilhaRotulos = PlanilhaRotulos(
                self._caminhos.dados_gold / f"rotulos_leva{leva}.csv", self._gold, temas
            )
            if not amostra.existe() or not planilha.caminho.is_file():
                continue
            pesos: dict[str, float] = {item.id: 1.0 / item.prob_inclusao for item in amostra.ler()}
            situacoes: list[SituacaoLinha] = planilha.validar(planilha.ler())
            situacao: SituacaoLinha
            for situacao in situacoes:
                if situacao.situacao == "rotulada":
                    rotulos[situacao.rotulo.id] = (situacao.rotulo, pesos.get(situacao.rotulo.id, 1.0))
        return rotulos

    def _linhas(
        self,
        questoes: Sequence[QuestaoPreparada],
        preliminares: Mapping[str, DecisaoPreliminar],
        sinais: Mapping[str, SinaisQuestao],
        previsao: ResultadoPrevisao,
    ) -> list[LinhaPublicacao]:
        """Monta as 359 linhas.

        Args:
            questoes: Todas as questões.
            preliminares: Decisões preliminares.
            sinais: Sinais (para a confiança de ``fora``).
            previsao: Limiar e probabilidades.

        Returns:
            Linhas na ordem das questões.
        """
        publicadas: set[str] = set(previsao.publicadas)
        linhas: list[LinhaPublicacao] = []
        questao: QuestaoPreparada
        for questao in questoes:
            decisao: DecisaoPreliminar | None = preliminares.get(questao.id)
            if decisao is None or not decisao.tema_id:
                linhas.append(LinhaPublicacao(questao.id, "revisar", "", "", 0.0, "falha de classificação"))
                continue
            extras: str = ";".join(decisao.extras_ids)
            if decisao.acao == "fora":
                confianca: float | None = sinais[questao.id].verificador.confianca
                linhas.append(LinhaPublicacao(questao.id, "fora", "", "", round(confianca or 0.5, 3), decisao.motivo))
                continue
            probabilidade: float = previsao.probabilidades.get(questao.id, 0.0)
            if decisao.acao == "candidata" and questao.id in publicadas:
                linhas.append(LinhaPublicacao(questao.id, "publicar", decisao.tema_id, extras, probabilidade, ""))
            elif decisao.acao == "candidata":
                motivo: str = f"baixa confiança (P = {probabilidade:.2f})".replace(".", ",")
                linhas.append(LinhaPublicacao(questao.id, "revisar", decisao.tema_id, extras, probabilidade, motivo))
            else:
                linhas.append(
                    LinhaPublicacao(questao.id, "revisar", decisao.tema_id, extras, probabilidade, decisao.motivo)
                )
        return linhas

    @staticmethod
    def _validar(linhas: Sequence[LinhaPublicacao], temas: Sequence[TemaPreparado], total: int) -> None:
        """Confere o formato do LEIA-ME.

        Args:
            linhas: Linhas geradas.
            temas: Árvore preparada.
            total: Número de questões.

        Raises:
            ErroPublicacao: Se alguma regra falhar.
        """
        publicaveis: set[str] = {tema.tema_id for tema in temas if tema.publicavel}
        problemas: list[str] = []
        ids: list[str] = [linha.id for linha in linhas]
        if len(ids) != total or len(set(ids)) != total:
            problemas.append(f"esperadas {total} linhas com IDs únicos; há {len(ids)} ({len(set(ids))} únicos)")
        linha: LinhaPublicacao
        for linha in linhas:
            if linha.decisao not in ("publicar", "revisar", "fora"):
                problemas.append(f"{linha.id}: decisão inválida")
            if linha.decisao == "publicar" and linha.tema_central_id not in publicaveis:
                problemas.append(f"{linha.id}: tema publicado não publicável")
            if linha.decisao == "revisar" and linha.tema_central_id not in publicaveis:
                problemas.append(f"{linha.id}: revisar sem sugestão publicável (o LEIA-ME exige o tema)")
            if linha.decisao == "fora" and linha.tema_central_id:
                problemas.append(f"{linha.id}: fora com tema")
            if linha.decisao in ("revisar", "fora") and not linha.motivo:
                problemas.append(f"{linha.id}: sem motivo")
            if not 0.0 <= linha.confianca <= 1.0:
                problemas.append(f"{linha.id}: confiança fora de [0, 1]")
            if any(extra not in publicaveis for extra in linha.extras_ids.split(";") if extra):
                problemas.append(f"{linha.id}: extra não publicável")
        if problemas:
            raise ErroPublicacao("; ".join(problemas[:20]))

    def _gravar_csv(self, linhas: Sequence[LinhaPublicacao]) -> Path:
        """Grava ``publicacao.csv`` na raiz.

        Args:
            linhas: Linhas validadas.

        Returns:
            Caminho gravado.
        """
        destino: Path = self._caminhos.raiz / "publicacao.csv"
        arquivo: TextIO
        with destino.open("w", encoding="utf-8", newline="") as arquivo:
            csv.writer(arquivo).writerows(
                [
                    list(self.COLUNAS),
                    *[
                        [l.id, l.decisao, l.tema_central_id, l.extras_ids, f"{l.confianca:.2f}", l.motivo]
                        for l in linhas
                    ],
                ]
            )
        return destino

    def _gravar_previsao(self, previsao: ResultadoPrevisao, validacao: ValidacaoCalibracao, exemplos: int) -> Path:
        """Grava ``previsao.txt`` na raiz, no formato do LEIA-ME, com a explicação.

        Args:
            previsao: Previsão.
            validacao: Validação cruzada da calibração.
            exemplos: Exemplos do gold usados.

        Returns:
            Caminho gravado.
        """
        p: ParametrosCalibracao = self._parametros
        baixo: float
        alto: float
        baixo, alto = previsao.precisao_intervalo
        sensibilidade: str = "; ".join(
            f"taxas × {fator:g}: ponto {ponto:.3f}, limite inferior {inferior:.3f}"
            for fator, ponto, inferior in previsao.sensibilidade
        )
        direta: str = (
            f"{previsao.precisao_direta:.3f} em {previsao.gold_publicadas} questões do gold que caem nas publicadas"
            if previsao.precisao_direta is not None
            else "sem questões do gold nas publicadas"
        )
        texto: list[str] = [
            f"precisao_prevista: {previsao.precisao_ponto:.2f}",
            f"precisao_intervalo: {baixo:.2f}-{alto:.2f}",
            f"cobertura_prevista: {previsao.cobertura:.2f}",
            f"cobertura_intervalo: {previsao.cobertura_intervalo[0]:.2f}-{previsao.cobertura_intervalo[1]:.2f}",
            "",
            "Como chegamos nesses números",
            "",
            (
                f"1. Rotulamos à mão, sem ver a resposta dos modelos, {exemplos} questões sorteadas (gold set). Elas "
                "medem se o tema escolhido pelo pipeline acerta pela régua do case (tema do especialista, pai ou filho direto)."
            ),
            (
                "2. Cada questão foi classificada por quatro fontes diferentes (dois classificadores de famílias distintas, "
                "um voto barato e as leis citadas) e conferida por um verificador que compara o candidato com os vizinhos."
            ),
            (
                f"3. Uma regressão logística aprendeu, no gold, a chance de acerto a partir da concordância entre as fontes, "
                f"do veredito do verificador e de marcas de risco. Na validação cruzada, o erro quadrático (Brier) foi "
                f"{validacao.brier:.3f}, contra {validacao.brier_base:.3f} de um palpite constante."
            ),
            (
                f"4. Publicamos as questões de maior chance de acerto enquanto o limite inferior da precisão estimada ficou "
                f"em {p.alvo_precisao:.0%} ou mais (regra usada: {previsao.regra}; limiar P = {previsao.limiar:.2f}). "
                f"O resto foi para revisão do professor."
            ),
            (
                f"5. A precisão prevista combina a média da chance de acerto das publicadas ({previsao.precisao_modelo:.3f}) "
                f"com o acerto direto no gold ({direta})."
            ),
            (
                f"6. Descontamos {previsao.margem_convencao:.3f} pelo risco de convenção: em temas duplicados ou "
                "sobrepostos, o especialista pode ter usado o outro nó, e o nosso gold não mede isso. As taxas de "
                f"discordância são hipóteses ({sensibilidade})."
            ),
            (
                f"7. O intervalo vem de {previsao.reamostras_validas} reamostras do gold (bootstrap), com o limite inferior "
                f"alargado também pela ambiguidade dos rótulos ({previsao.margem_ambiguidade:.3f}: diferença entre a "
                "régua tolerante e a estrita no gold)."
            ),
            (
                f"8. Cobertura: {len(previsao.publicadas)} publicadas de {p.total_questoes}. É um número exato se a avaliação "
                "usar as 359 questões; o intervalo de ±0,01 cobre só arredondamento."
            ),
            "",
            (
                "O que não foi medido: a convenção real dos especialistas nos nós duplicados (só suposta) e a variação "
                "das respostas dos modelos entre execuções (as respostas estão gravadas no cache e não mudam)."
            ),
            "",
        ]
        destino: Path = self._caminhos.raiz / "previsao.txt"
        destino.write_text("\n".join(texto), encoding="utf-8")
        return destino

    def _gravar_preliminares(self, preliminares: Sequence[DecisaoPreliminar], previsao: ResultadoPrevisao) -> Path:
        """Grava as decisões preliminares e as probabilidades das candidatas (para a leva 2 do gold).

        Args:
            preliminares: Decisões preliminares.
            previsao: Limiar e probabilidades.

        Returns:
            Caminho das decisões preliminares.
        """
        destino: Path = self._caminhos.raiz / "dados" / "decisao" / "preliminares.jsonl"
        destino.parent.mkdir(parents=True, exist_ok=True)
        candidatas: dict[str, float] = {
            d.id: previsao.probabilidades[d.id]
            for d in preliminares
            if d.acao == "candidata" and d.id in previsao.probabilidades
        }
        (destino.parent / "probabilidades.json").write_text(
            json.dumps(
                {
                    "limiar": previsao.limiar,
                    "gerado_em": datetime.now().isoformat(timespec="seconds"),
                    "candidatas": candidatas,
                },
                ensure_ascii=False,
                indent=1,
            )
            + "\n",
            encoding="utf-8",
        )
        destino.write_text(
            "".join(json.dumps(d.como_dict(), ensure_ascii=False) + "\n" for d in preliminares), encoding="utf-8"
        )
        return destino

    def _relatorio(
        self,
        linhas: Sequence[LinhaPublicacao],
        preliminares: Mapping[str, DecisaoPreliminar],
        previsao: ResultadoPrevisao,
        validacao: ValidacaoCalibracao,
        coeficientes: Mapping[str, float],
        exemplos: int,
        penalidade: float,
        grade: Sequence[tuple[float, ValidacaoCalibracao]],
    ) -> Path:
        """Grava ``saidas/decisao/relatorio_decisao.md``.

        Args:
            linhas: Linhas do CSV.
            preliminares: Decisões preliminares.
            previsao: Previsão.
            validacao: Validação cruzada.
            coeficientes: Coeficientes da calibração.
            exemplos: Exemplos do gold.
            penalidade: Penalidade L2 escolhida.
            grade: Validação de cada penalidade da grade.

        Returns:
            Caminho gravado.
        """
        contagem: Counter[str] = Counter(linha.decisao for linha in linhas)
        motivos: Counter[str] = Counter(
            linha.motivo.split(":")[0].split(" (")[0] if linha.motivo else ""
            for linha in linhas
            if linha.decisao != "publicar"
        )
        publicadas: set[str] = set(previsao.publicadas)
        recuadas: int = sum(1 for i in publicadas if preliminares[i].recuou)
        nivel1: int = sum(1 for i in publicadas if preliminares[i].nivel == 1)
        tipos: Counter[str] = Counter(preliminares[i].tipo_convencao or "sem risco" for i in publicadas)
        texto: list[str] = [
            "# Passo 07: decisão",
            "",
            f"Gerado em {datetime.now():%d/%m/%Y %H:%M}.",
            "",
            f"- Publicar: {contagem['publicar']}; revisar: {contagem['revisar']}; fora: {contagem['fora']}.",
            f"- Publicadas no nível 1: {nivel1}, das quais {recuadas} por recuo para o pai (ADR-010).",
            f"- Tipo de convenção das publicadas: {dict(tipos)}.",
            f"- Limiar P = {previsao.limiar:.3f} ({previsao.regra}).",
            (
                f"- Precisão: ponto {previsao.precisao_ponto:.3f}, intervalo {previsao.precisao_intervalo[0]:.3f}–"
                f"{previsao.precisao_intervalo[1]:.3f}; modelo {previsao.precisao_modelo:.3f}; direta "
                f"{previsao.precisao_direta} em {previsao.gold_publicadas} do gold; margens: convenção "
                f"{previsao.margem_convencao:.3f}, ambiguidade {previsao.margem_ambiguidade:.3f}."
            ),
            "",
            "## Motivos de revisar e fora",
            "",
            "| Motivo | Questões |",
            "|---|---:|",
            *(f"| {motivo or '—'} | {n} |" for motivo, n in motivos.most_common()),
            "",
            f"## Calibração ({exemplos} questões do gold com tema)",
            "",
            (
                f"Validação cruzada: taxa de acerto {validacao.taxa_acerto:.3f}; Brier {validacao.brier:.4f} "
                f"(palpite constante: {validacao.brier_base:.4f}); log-loss {validacao.log_loss:.4f}."
            ),
            "",
            "| Faixa de P | Questões | P média | Acerto observado |",
            "|---|---:|---:|---:|",
            *(f"| {faixa} | {n} | {media:.3f} | {obs:.3f} |" for faixa, n, media, obs in validacao.faixas),
            "",
            f"Penalidade L2 escolhida pela menor log-loss na validação cruzada: {penalidade:g}.",
            "",
            "| Penalidade L2 | Brier | Log-loss |",
            "|---:|---:|---:|",
            *(f"| {pena:g} | {v.brier:.4f} | {v.log_loss:.4f} |" for pena, v in grade),
            "",
            "| Variável | Coeficiente |",
            "|---|---:|",
            *(f"| {nome} | {valor} |" for nome, valor in coeficientes.items()),
            "",
        ]
        destino: Path = self._caminhos.raiz / "saidas" / "decisao" / "relatorio_decisao.md"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text("\n".join(texto), encoding="utf-8")
        return destino
