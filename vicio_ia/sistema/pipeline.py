"""Sistema de classificação da etapa 2, de ponta a ponta, sem modelo de linguagem (ADR-019 a ADR-025).

Lê só artefatos versionados (``dados/preparados/``, ``dados/conhecimento/`` e a folha-verdade), treina o
ranqueador na folha, mede fora da amostra, calibra, escolhe o limiar e grava:

- ``relatorio/etapa2/publicacao.csv``: as 659 questões, no formato do LEIA-ME;
- ``relatorio/etapa2/previsao.txt``: precisão e cobertura previstas para as 559 avaliadas;
- ``saidas/sistema/diagnostico.md`` e ``execucao.json``: o diagnóstico e o tempo.

A saída é determinística: as mesmas entradas geram os mesmos arquivos, byte a byte.
"""

from __future__ import annotations

import csv
import json
import time
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

import numpy as np

from vicio_ia.configuracao import Caminhos, ParametrosSistema
from vicio_ia.estatistica import Matriz
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada
from vicio_ia.sistema.folha import ReguaEtapa2, RotuloFolha
from vicio_ia.sistema.pares import CarregadorSistema, DadosSistema, GeradorPares, ParesQuestao
from vicio_ia.sistema.politica import Calibrador, EscolhaQuestao, EscolhedorNo, EstimadorLimiar, Previsao, RegrasFora
from vicio_ia.sistema.ranqueador import ModeloPares, TreinoRanqueador
from vicio_ia.sistema.validacao import ValidacaoCruzadaRepetida


@dataclass(frozen=True)
class DecisaoQuestao:
    """Uma linha do ``publicacao.csv``.

    Attributes:
        id: ID da questão.
        decisao: ``publicar``, ``revisar`` ou ``fora``.
        tema: Tema central (vazio em ``fora``).
        extras: Extras.
        confianca: Chance de o tema central estar certo (em ``fora``, a chance de nenhum tema servir).
        motivo: Motivo (obrigatório em ``revisar`` e ``fora``).
    """

    id: str
    decisao: str
    tema: str
    extras: tuple[str, ...]
    confianca: float
    motivo: str


class SistemaEtapa2:
    """Roda o sistema e grava os entregáveis."""

    COMANDO: str = "uv run python executar_sistema.py"

    def __init__(self, caminhos: Caminhos | None = None, parametros: ParametrosSistema | None = None) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto.
            parametros: Parâmetros do sistema.
        """
        self._caminhos: Caminhos = caminhos or Caminhos.padrao()
        self._parametros: ParametrosSistema = parametros or ParametrosSistema()

    def executar(self) -> Path:
        """Roda tudo e grava os arquivos.

        Returns:
            Caminho do ``publicacao.csv``.
        """
        inicio: float = time.perf_counter()
        p: ParametrosSistema = self._parametros
        dados: DadosSistema = CarregadorSistema(self._caminhos).carregar()
        gerador: GeradorPares = GeradorPares(dados, p)
        pares: dict[str, ParesQuestao] = gerador.pares()
        regua: ReguaEtapa2 = ReguaEtapa2(dados.temas)
        treino: TreinoRanqueador = TreinoRanqueador(
            gerador,
            pares,
            dados.folha,
            dados.temas,
            ValidacaoCruzadaRepetida(p.partes_validacao, p.repeticoes_validacao, p.semente),
            p.ranqueador,
        )
        escolhedor: EscolhedorNo = EscolhedorNo(gerador, p.limiar_extra, p.max_extras)
        na_folha: set[str] = {r.id for r in dados.folha}
        fora_amostra: dict[str, Matriz] = treino.fora_da_amostra([q.id for q in dados.questoes if q.id not in na_folha])
        escolhas_folha: list[EscolhaQuestao] = [
            escolhedor.escolher(pares[r.id], fora_amostra[r.id]) for r in dados.folha
        ]
        p_folha: Matriz = np.array([e.p for e in escolhas_folha], dtype=np.float64)
        acerto_folha: Matriz = np.array(
            [1.0 if regua.acerta(e.tema, r) else 0.0 for e, r in zip(escolhas_folha, dados.folha, strict=True)],
            dtype=np.float64,
        )
        concorda_folha: Matriz = np.array([1.0 if e.concorda else 0.0 for e in escolhas_folha], dtype=np.float64)
        calibrador: Calibrador
        perdas: dict[str, float]
        calibrador, perdas = Calibrador.escolher(p_folha, concorda_folha, acerto_folha, p.partes_validacao, p.semente)
        modelo: ModeloPares = treino.ajustar_final()
        escolhas: dict[str, EscolhaQuestao] = {
            q.id: escolhedor.escolher(pares[q.id], fora_amostra[q.id]) for q in dados.questoes
        }
        regras: RegrasFora = RegrasFora(
            RegrasFora.limiar_da_folha(
                [gerador.inativo_menos_maximo(r.id) for r in dados.folha if not r.fora], p.percentil_inativo
            )
        )
        avaliadas: list[QuestaoPreparada] = [q for q in dados.questoes if q.id not in na_folha]
        bloqueio: dict[str, str] = {q.id: self._bloqueio(q, gerador, regras) for q in dados.questoes}
        elegiveis: list[EscolhaQuestao] = [escolhas[q.id] for q in avaliadas if not bloqueio[q.id]]
        previsao: Previsao = EstimadorLimiar(
            p_folha, concorda_folha, acerto_folha, calibrador, p.sorteios_previsao, p.semente
        ).estimar(
            np.array([e.p for e in elegiveis], dtype=np.float64),
            np.array([1.0 if e.concorda else 0.0 for e in elegiveis], dtype=np.float64),
            p.precisao_alvo,
            p.percentil_limiar,
            p.ponto_reserva,
            len(avaliadas),
            p.min_direto,
            p.min_direto_parcial,
            p.criterio_limiar,
        )
        todas: list[EscolhaQuestao] = [escolhas[q.id] for q in dados.questoes]
        calibradas: Matriz = calibrador.aplicar(
            np.array([e.p for e in todas], dtype=np.float64),
            np.array([1.0 if e.concorda else 0.0 for e in todas], dtype=np.float64),
        )
        decisoes: list[DecisaoQuestao] = [
            self._decidir(q, escolhas[q.id], float(c), bloqueio[q.id], previsao)
            for q, c in zip(dados.questoes, calibradas, strict=True)
        ]
        publicadas_avaliadas: int = sum(1 for d in decisoes if d.decisao == "publicar" and d.id not in na_folha)
        if publicadas_avaliadas != previsao.publicadas:
            raise RuntimeError(f"publicadas {publicadas_avaliadas} ≠ previstas {previsao.publicadas}")
        destino: Path = self._gravar_publicacao(decisoes)
        cobertura: dict[str, tuple[int, int]] = self._cobertura(decisoes, avaliadas)
        self._gravar_previsao(previsao, calibrador, cobertura, escolhas_folha, acerto_folha, dados.folha, regras)
        segundos: float = time.perf_counter() - inicio
        self._gravar_diagnostico(
            decisoes,
            previsao,
            calibrador,
            perdas,
            modelo,
            p_folha,
            acerto_folha,
            dados.folha,
            cobertura,
            regras,
            bloqueio,
        )
        self._gravar_execucao(segundos, decisoes, previsao)
        print(
            f"Sistema da etapa 2: {Counter(d.decisao for d in decisoes)} nas 659; "
            f"{previsao.publicadas} publicadas entre as {previsao.avaliadas} avaliadas "
            f"(precisão prevista {previsao.precisao:.2f}, {previsao.precisao_intervalo[0]:.2f}–"
            f"{previsao.precisao_intervalo[1]:.2f}); {segundos:.0f} s.\nEntregáveis: {destino.parent}"
        )
        return destino

    @staticmethod
    def _bloqueio(questao: QuestaoPreparada, gerador: GeradorPares, regras: RegrasFora) -> str:
        """Regra que impede a publicação, se houver.

        Args:
            questao: Questão.
            gerador: Gerador (proximidade com tema inativo).
            regras: Regras de fora.

        Returns:
            ``militar``, ``inativo`` ou vazio.
        """
        if RegrasFora.militar(str(questao.original.get("disciplina_origem") or "")):
            return "militar"
        if regras.inativo(gerador.inativo_menos_maximo(questao.id)):
            return "inativo"
        return ""

    @staticmethod
    def _decidir(
        questao: QuestaoPreparada, escolha: EscolhaQuestao, calibrada: float, bloqueio: str, previsao: Previsao
    ) -> DecisaoQuestao:
        """Decide uma questão.

        Args:
            questao: Questão.
            escolha: Nó escolhido.
            calibrada: P(certo) calibrada do nó.
            bloqueio: Regra de fora ou de revisão.
            previsao: Limiar escolhido.

        Returns:
            Linha do ``publicacao.csv``.
        """
        confianca: float = round(calibrada, 3)
        if bloqueio == "militar":
            return DecisaoQuestao(questao.id, "fora", "", (), round(1.0 - confianca, 3), RegrasFora.MOTIVO_MILITAR)
        if bloqueio == "inativo":
            return DecisaoQuestao(
                questao.id, "revisar", escolha.tema, escolha.extras, confianca, RegrasFora.MOTIVO_INATIVO
            )
        if calibrada >= previsao.limiar - 1e-12:
            return DecisaoQuestao(questao.id, "publicar", escolha.tema, escolha.extras, confianca, "")
        corte: str = "nenhum corte atinge 95%" if previsao.limiar == float("inf") else f"limiar {previsao.limiar:.3f}"
        alternativa: str = f"; outra opção: {escolha.alternativa}" if escolha.alternativa else ""
        motivo: str = f"confiança {calibrada:.3f} abaixo do limiar de publicação ({corte}){alternativa}"
        return DecisaoQuestao(questao.id, "revisar", escolha.tema, escolha.extras, confianca, motivo)

    def _gravar_publicacao(self, decisoes: Sequence[DecisaoQuestao]) -> Path:
        """Grava o ``publicacao.csv`` em ordem de ID.

        Args:
            decisoes: Decisões.

        Returns:
            Caminho gravado.
        """
        pasta: Path = self._caminhos.entregaveis
        pasta.mkdir(parents=True, exist_ok=True)
        linhas: list[list[str]] = [["id", "decisao", "tema_central_id", "extras_ids", "confianca", "motivo"]]
        linhas.extend(
            [d.id, d.decisao, d.tema, ";".join(d.extras), f"{d.confianca:.3f}", d.motivo]
            for d in sorted(decisoes, key=lambda d: d.id)
        )
        destino: Path = pasta / "publicacao.csv"
        arquivo: TextIO
        with destino.open("w", encoding="utf-8", newline="") as arquivo:
            csv.writer(arquivo, lineterminator="\n").writerows(linhas)
        return destino

    def _cobertura(
        self, decisoes: Sequence[DecisaoQuestao], avaliadas: Sequence[QuestaoPreparada]
    ) -> dict[str, tuple[int, int]]:
        """Publicadas e total nas avaliadas, nas antigas e nas novas.

        Args:
            decisoes: Decisões.
            avaliadas: Questões avaliadas.

        Returns:
            ``grupo -> (publicadas, total)``.
        """
        publicadas: set[str] = {d.id for d in decisoes if d.decisao == "publicar"}
        limite: int = self._parametros.questoes_etapa1
        grupos: dict[str, list[str]] = {
            "avaliadas": [q.id for q in avaliadas],
            "antigas": [q.id for q in avaliadas if int(q.id[1:]) <= limite],
            "novas": [q.id for q in avaliadas if int(q.id[1:]) > limite],
        }
        return {g: (sum(1 for i in ids if i in publicadas), len(ids)) for g, ids in grupos.items()}

    def _gravar_previsao(
        self,
        previsao: Previsao,
        calibrador: Calibrador,
        cobertura: Mapping[str, tuple[int, int]],
        escolhas_folha: Sequence[EscolhaQuestao],
        acerto_folha: Matriz,
        folha: Sequence[RotuloFolha],
        regras: RegrasFora,
    ) -> Path:
        """Grava o ``previsao.txt``: as quatro linhas do LEIA-ME e a explicação.

        Args:
            previsao: Previsão no limiar escolhido.
            calibrador: Calibração.
            cobertura: Publicadas e total por grupo.
            escolhas_folha: Nós escolhidos fora da amostra na folha.
            acerto_folha: Acerto desses nós.
            folha: Folha-verdade.
            regras: Regras de fora.

        Returns:
            Caminho gravado.
        """
        publicadas: int
        total: int
        publicadas, total = cobertura["avaliadas"]
        fracao: float = publicadas / total if total else 0.0
        com_tema: int = sum(1 for r in folha if not r.fora)
        acertos_com_tema: int = int(sum(a for a, r in zip(acerto_folha, folha, strict=True) if not r.fora))
        limiar_calibrado: str = "nenhum" if previsao.limiar == float("inf") else f"{previsao.limiar:.3f}"
        linhas: list[str] = [
            f"precisao_prevista: {previsao.precisao:.2f}   # fração das publicadas que estará certa",
            f"precisao_intervalo: {previsao.precisao_intervalo[0]:.2f}-{previsao.precisao_intervalo[1]:.2f}",
            f"cobertura_prevista: {fracao:.2f}  # fração das questões que você publicou",
            f"cobertura_intervalo: {max(0.0, fracao - 0.01):.2f}-{min(1.0, fracao + 0.01):.2f}",
            "",
            "Como chegamos nesses números",
            "",
            (
                f"1. Sistema. Nenhum modelo de linguagem decide: o ranqueador ({self._parametros.ranqueador.nome}, "
                "escolhido no experimento E10 pela log-loss fora da amostra) atua sobre os pares "
                "(questão, tema), com 20 atributos (similaridade de embedding em cache, BM25, mapa de artigos, termos "
                "revisados, exemplos sintéticos dos temas, vizinhos da folha, estrutura da árvore), treinado nas 100 questões da folha-verdade. O "
                "rótulo de cada par é a própria régua da avaliação, então a probabilidade de um tema é a chance de "
                "publicá-lo estar certo."
            ),
            (
                f"2. Medição fora da amostra. Em validação cruzada estratificada (5 partes, 10 repetições), o nó "
                f"escolhido acerta {int(acerto_folha.sum())} das 100 questões da folha ({acertos_com_tema} das "
                f"{com_tema} com tema; as 8 fora da taxonomia são sempre erro). A calibração escolhida pela log-loss "
                f"fora da amostra foi {Calibrador.NOMES[calibrador.tipo]}."
            ),
            (
                f"3. Limiar. Publicamos o maior conjunto das {total} questões avaliadas cuja precisão estimada pelo "
                f"modelo é de pelo menos 97% no ponto (a regra de reserva da etapa 1, adotada como critério; decisão "
                f"D15). O critério mais estrito, com o percentil 10 de pelo menos 95%, só permitiria publicar "
                f"{previsao.publicadas_estrito}: com 100 questões rotuladas e 8% de questões fora da taxonomia que "
                f"nenhum atributo separa, a incerteza não deixa ir além disso. O corte ficou em P(certo) = "
                f"{limiar_calibrado}: {publicadas} publicadas, com percentil 10 de {previsao.precisao_p10:.2f}."
            ),
            self._texto_precisao(previsao, escolhas_folha, acerto_folha),
            (
                f"5. Cobertura. É exata dado o sistema: {publicadas}/{total}. Nas antigas, "
                f"{cobertura['antigas'][0]}/{cobertura['antigas'][1]}; nas novas, {cobertura['novas'][0]}/"
                f"{cobertura['novas'][1]}. O intervalo de ± 0,01 cobre o arredondamento."
            ),
            (
                "6. Riscos que a previsão já carrega. (a) Fora da taxonomia: com 8 casos na folha, nenhum atributo "
                "separa as questões fora (AUC fora da amostra de 0,61), e elas entram na estimativa como erros "
                "dentro da faixa em que caem. (b) Direito militar: as 10 questões novas de direito militar vão "
                f"para fora, porque a árvore não tem tema militar. (c) Questões perto de um tema inativo vão para "
                f"revisar (corte {regras.limiar_inativo:.3f}, o percentil 90 das questões com tema da folha). (d) "
                "Deriva: as 300 questões novas não diferem das antigas na similaridade nem na margem (experimento "
                "E12), então o intervalo não foi alargado. (e) Convenção: a folha só tem questões da equipe, e "
                "desvios de convenção (nó duplicado, sobreposição) já aparecem como erros no estimador direto."
            ),
        ]
        destino: Path = self._caminhos.entregaveis / "previsao.txt"
        destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")
        return destino

    def _texto_precisao(
        self, previsao: Previsao, escolhas_folha: Sequence[EscolhaQuestao], acerto_folha: Matriz
    ) -> str:
        """Parágrafo do ``previsao.txt`` que explica o ponto e o intervalo da precisão.

        Args:
            previsao: Previsão no limiar escolhido.
            escolhas_folha: Nós escolhidos fora da amostra na folha.
            acerto_folha: Acerto desses nós.

        Returns:
            Parágrafo.
        """
        p: ParametrosSistema = self._parametros
        na_faixa: int
        certas: int
        na_faixa, certas = previsao.folha_na_faixa
        ordem: list[int] = sorted(range(len(escolhas_folha)), key=lambda i: -escolhas_folha[i].p)[:20]
        topo: int = int(sum(acerto_folha[i] for i in ordem))
        base: str = (
            f"4. Precisão. Em {p.sorteios_previsao} sorteios com semente fixa, o estimador do modelo (a P calibrada "
            f"média das publicadas, refazendo a calibração em bootstrap da folha) dá {previsao.modelo:.3f}. "
            f"Questões da folha que cairiam na faixa publicada, fora da amostra: {na_faixa} (certas: {certas}). "
        )
        if na_faixa < p.min_direto_parcial:
            detalhe: str = (
                f"Com menos de {p.min_direto_parcial}, o estimador direto seria quase só o prior de Jeffreys, então o "
                "ponto e o intervalo (percentis 5 e 95) vêm do modelo (D15). "
            )
        elif na_faixa < p.min_direto:
            detalhe = (
                f"O ponto é a média do modelo com o estimador direto ({previsao.direto:.3f}, com Jeffreys), como na "
                "D12, e o intervalo vem dos sorteios dos dois. "
            )
        else:
            detalhe = f"O ponto é o estimador direto ({previsao.direto:.3f}, com Jeffreys). "
        return (
            base
            + detalhe
            + f"Para referência, entre as 20 questões da folha de maior confiança fora da amostra, {topo} estão certas."
        )

    def _gravar_diagnostico(
        self,
        decisoes: Sequence[DecisaoQuestao],
        previsao: Previsao,
        calibrador: Calibrador,
        perdas: Mapping[str, float],
        modelo: ModeloPares,
        p_folha: Matriz,
        acerto_folha: Matriz,
        folha: Sequence[RotuloFolha],
        cobertura: Mapping[str, tuple[int, int]],
        regras: RegrasFora,
        bloqueio: Mapping[str, str],
    ) -> Path:
        """Grava o diagnóstico do sistema (base do relatório).

        Args:
            decisoes: Decisões.
            previsao: Previsão.
            calibrador: Calibração.
            perdas: Log-loss fora da amostra de cada calibrador.
            modelo: Modelo final.
            p_folha: P fora da amostra do nó escolhido na folha.
            acerto_folha: Acerto desses nós.
            folha: Folha-verdade.
            cobertura: Publicadas por grupo.
            regras: Regras de fora.
            bloqueio: Regra aplicada por questão.

        Returns:
            Caminho gravado.
        """
        pasta: Path = self._caminhos.raiz / "saidas" / "sistema"
        pasta.mkdir(parents=True, exist_ok=True)
        ordem: list[int] = [int(i) for i in np.argsort(-p_folha, kind="stable")]
        fora_folha: list[bool] = [r.fora for r in folha]
        curva_folha: list[str] = []
        k: int
        for k in (10, 20, 30, 40, 50, 60, 70, 80, 90, 100):
            topo: list[int] = ordem[:k]
            certas: int = int(sum(acerto_folha[i] for i in topo))
            foras: int = sum(1 for i in topo if fora_folha[i])
            curva_folha.append(f"| {k} | {certas}/{k} ({certas / k:.0%}) | {foras} | {p_folha[topo[-1]]:.3f} |")
        coeficientes: Matriz | None = modelo.coeficientes
        nomes: tuple[str, ...] = GeradorPares.NOMES
        pesos: list[str] = (
            [
                f"| {nome} | {coeficientes[i + 1]:+.2f} |"
                for i, nome in sorted(enumerate(nomes), key=lambda x: -abs(coeficientes[x[0] + 1]))
            ]
            if coeficientes is not None
            else ["| (modelo não linear: sem pesos por atributo) | — |"]
        )
        corte_curva: list[str] = [
            f"| {n} | {ponto:.3f} | {p10:.3f} |" for n, ponto, p10 in previsao.curva if n % 10 == 0 or n < 10
        ][:60]
        contagem: Counter[str] = Counter(d.decisao for d in decisoes)
        regra_contagem: Counter[str] = Counter(v for v in bloqueio.values() if v)
        linhas: list[str] = [
            "# Diagnóstico do sistema da etapa 2",
            "",
            f"Gerado por `{self.COMANDO}`, sem modelo de linguagem e sem rede.",
            "",
            "## Ranqueador fora da amostra (folha, 5 partes × 10 repetições)",
            "",
            (
                f"- Nó escolhido certo pela régua: {int(acerto_folha.sum())}/100 "
                f"({int(sum(a for a, f in zip(acerto_folha, fora_folha, strict=True) if not f))}/"
                f"{sum(1 for f in fora_folha if not f)} com tema)."
            ),
            (
                f"- Calibração: {Calibrador.NOMES[calibrador.tipo]} (log-loss fora da amostra: "
                + ", ".join(f"{t} {v:.3f}" for t, v in perdas.items())
                + f"); coeficientes: {tuple(round(c, 3) for c in calibrador.coeficientes)}."
            ),
            "",
            "| Questões da folha (maior P primeiro) | Certas | Fora entre elas | P da última |",
            "|---:|---:|---:|---:|",
            *curva_folha,
            "",
            f"## Ranqueador: {self._parametros.ranqueador.nome}; pesos do modelo final (atributos padronizados)",
            "",
            "| Atributo | Peso |",
            "|---|---:|",
            *pesos,
            "",
            "## Limiar (avaliadas elegíveis)",
            "",
            f"- Critério: {previsao.regra}; pelo percentil 10 ≥ 95% seriam {previsao.publicadas_estrito} publicadas.",
            (
                f"- Corte em P calibrada {previsao.limiar:.4f}: {previsao.publicadas} publicadas de "
                f"{previsao.avaliadas}; precisão {previsao.precisao:.3f} (percentil 10 {previsao.precisao_p10:.3f}; "
                f"5–95: {previsao.precisao_intervalo[0]:.3f}–{previsao.precisao_intervalo[1]:.3f}); modelo "
                f"{previsao.modelo:.3f}, direto {previsao.direto:.3f}; folha na faixa: {previsao.folha_na_faixa[1]}/"
                f"{previsao.folha_na_faixa[0]} certas."
            ),
            "",
            "| Publicadas | Ponto | Percentil 10 |",
            "|---:|---:|---:|",
            *corte_curva,
            "",
            "## Decisões",
            "",
            f"- Nas 659: {dict(sorted(contagem.items()))}.",
            f"- Regras: {dict(sorted(regra_contagem.items()))} (corte de tema inativo {regras.limiar_inativo:.3f}).",
            f"- Cobertura: {dict(cobertura)}.",
            "",
        ]
        destino: Path = pasta / "diagnostico.md"
        destino.write_text("\n".join(linhas), encoding="utf-8")
        return destino

    def _gravar_execucao(self, segundos: float, decisoes: Sequence[DecisaoQuestao], previsao: Previsao) -> Path:
        """Grava o tempo e as contagens da execução (fora dos entregáveis, que não levam horário).

        Args:
            segundos: Duração.
            decisoes: Decisões.
            previsao: Previsão.

        Returns:
            Caminho gravado.
        """
        pasta: Path = self._caminhos.raiz / "saidas" / "sistema"
        pasta.mkdir(parents=True, exist_ok=True)
        destino: Path = pasta / "execucao.json"
        conteudo: dict[str, object] = {
            "comando": self.COMANDO,
            "segundos": round(segundos, 1),
            "inicio": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time() - segundos)),
            "decisoes": dict(sorted(Counter(d.decisao for d in decisoes).items())),
            "publicadas_avaliadas": previsao.publicadas,
            "precisao_prevista": round(previsao.precisao, 4),
        }
        destino.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return destino
