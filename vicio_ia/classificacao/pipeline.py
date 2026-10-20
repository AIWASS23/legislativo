"""Orquestração dos passos 05 e 06: classificadores em paralelo, candidato preliminar e verificador (ADR-008)."""

from __future__ import annotations

import json
import time
from collections import Counter
from collections.abc import Sequence
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import ClassVar

from vicio_ia.avaliacao.amostragem import ArquivoAmostra, ItemAmostra
from vicio_ia.avaliacao.planilha import PlanilhaRotulos
from vicio_ia.classificacao.classificadores import (
    Classificador,
    ClassificadorHierarquico,
    ClassificadorPlano,
    VotoBarato,
)
from vicio_ia.classificacao.montador_prompt import MontadorPrompt
from vicio_ia.classificacao.respostas import SinaisQuestao, VereditoVerificador, VotoClassificador
from vicio_ia.classificacao.schemas import FabricaSchemas
from vicio_ia.classificacao.verificador import VerificadorContrastivo
from vicio_ia.configuracao import Caminhos, ParametrosClassificacao, ParametrosGold, ParametrosLLM
from vicio_ia.conhecimento import MapaLegislacao
from vicio_ia.etapa import GuardaEtapa
from vicio_ia.llm.cliente import FabricaClientes
from vicio_ia.llm.prompts import ArquivoPrompt
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada
from vicio_ia.sinais.regras import SinalLegislacao
from vicio_ia.temas.arvore_prompt import MaterialArvore
from vicio_ia.temas.cartoes import ArquivoCartoes, CartaoTema
from vicio_ia.texto import ProcessadorTexto


class PipelineClassificacao:
    """Classifica as questões com A, B e o voto barato, e verifica as candidatas a publicar.

    Saídas:

    * ``dados/classificacao/sinais.jsonl``: uma linha por questão classificada, com todos os votos
      (provedor, modelo e versão do prompt de cada um), as regras e o veredito do verificador;
    * ``saidas/classificacao/resumo_classificacao.md``: números agregados (nenhuma questão individual);
    * ``saidas/custos/resumo_custos.md``: custo e tempo por papel (ADR-003).

    Questões do gold ainda sem rótulo ficam de fora (``adiar_gold_pendente``), para o rótulo
    continuar cego. Rodar de novo depois da rotulagem completa o arquivo; o que já foi feito vem
    do cache.
    """

    PAPEIS: ClassVar[tuple[str, ...]] = ("classificador_a", "classificador_b", "voto_barato")

    def __init__(
        self,
        caminhos: Caminhos | None = None,
        parametros: ParametrosClassificacao | None = None,
        parametros_llm: ParametrosLLM | None = None,
        parametros_gold: ParametrosGold | None = None,
    ) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto (opcional).
            parametros: Parâmetros da classificação (opcional).
            parametros_llm: Parâmetros de LLM (opcional).
            parametros_gold: Parâmetros do gold set, para ler a planilha (opcional).
        """
        self._caminhos: Caminhos = caminhos if caminhos is not None else Caminhos.padrao()
        self._parametros: ParametrosClassificacao = parametros if parametros is not None else ParametrosClassificacao()
        self._parametros_llm: ParametrosLLM = parametros_llm if parametros_llm is not None else ParametrosLLM()
        self._parametros_gold: ParametrosGold = parametros_gold if parametros_gold is not None else ParametrosGold()
        self._temas: dict[str, TemaPreparado] = {}

    def executar(self) -> Path:
        """Roda os passos 05 e 06.

        Returns:
            Caminho de ``sinais.jsonl``.
        """
        GuardaEtapa.exigir_etapa1(self._caminhos, "A classificação por LLM (passos 05 e 06)")
        leitor: LeitorPreparados = LeitorPreparados(self._caminhos)
        questoes: list[QuestaoPreparada] = leitor.questoes()
        temas: list[TemaPreparado] = leitor.temas()
        self._temas = {tema.tema_id: tema for tema in temas}
        cartoes: list[CartaoTema] = ArquivoCartoes(self._caminhos.dados_temas / "cartoes.jsonl").ler()
        material: MaterialArvore = MaterialArvore(temas, cartoes, leitor.arvore_enxuta())
        selecionadas: list[QuestaoPreparada]
        adiadas: int
        selecionadas, adiadas = self._selecionar(questoes, temas)

        fabrica: FabricaClientes = FabricaClientes(self._caminhos, self._parametros_llm)
        schemas: FabricaSchemas = FabricaSchemas(temas)
        montador: MontadorPrompt = MontadorPrompt(self._parametros_llm, self._parametros.chars_por_token_local)
        prompts: Path = self._caminhos.prompts
        classificadores: list[Classificador] = [
            ClassificadorPlano(
                fabrica.cliente("classificador_a"),
                montador,
                schemas,
                ArquivoPrompt(prompts / "classificador_plano.md"),
                material,
                self._parametros.com_escopo_a,
            ),
            ClassificadorHierarquico(
                fabrica.cliente("classificador_b"),
                montador,
                schemas,
                ArquivoPrompt(prompts / "classificador_hierarquico_tema.md"),
                ArquivoPrompt(prompts / "classificador_hierarquico_subtema.md"),
                material,
                temas,
            ),
            VotoBarato(
                fabrica.cliente("voto_barato"), montador, schemas, ArquivoPrompt(prompts / "voto_barato.md"), material
            ),
        ]
        verificador: VerificadorContrastivo = VerificadorContrastivo(
            fabrica.cliente("verificador"),
            montador,
            schemas,
            ArquivoPrompt(prompts / "verificador.md"),
            material,
            temas,
        )
        print(
            f"Classificação: {len(selecionadas)} questões ({adiadas} do gold adiadas até serem rotuladas); "
            + "; ".join(f"{c.cliente.papel}={c.cliente.provedor}:{c.cliente.modelo}" for c in classificadores)
            + f"; verificador={verificador.cliente.provedor}:{verificador.cliente.modelo}",
            flush=True,
        )
        inicio: float = time.monotonic()
        votos: dict[str, list[VotoClassificador]] = {questao.id: [] for questao in selecionadas}
        lentos: list[Classificador] = [c for c in classificadores if c.cliente.papel == "voto_barato"]
        principais: list[Classificador] = [c for c in classificadores if c.cliente.papel != "voto_barato"]
        executores_lentos: list[ThreadPoolExecutor] = []
        futuros_lentos: dict[Future[VotoClassificador], str]
        executores: list[ThreadPoolExecutor]
        futuros: dict[Future[VotoClassificador], str]
        try:
            executores_lentos, futuros_lentos = self._iniciar(lentos, selecionadas, fabrica)
            executores, futuros = self._iniciar(principais, selecionadas, fabrica)
            try:
                self._acompanhar(futuros, votos, len(futuros), "A e B")
            finally:
                self._encerrar(executores)
            vereditos: dict[str, VereditoVerificador] = self._verificar(verificador, selecionadas, votos, fabrica)
            self._acompanhar(futuros_lentos, votos, len(futuros_lentos), "voto barato")
        finally:
            self._encerrar(executores_lentos)
            fabrica.escrever_resumo_custos()
            print(f"Chamadas: {fabrica.resumo_sessao()}", flush=True)
        regras: SinalLegislacao = SinalLegislacao(MapaLegislacao(ProcessadorTexto()), temas)
        sinais: list[SinaisQuestao] = [
            SinaisQuestao(
                id=questao.id,
                votos=tuple(sorted(votos[questao.id], key=lambda voto: self.PAPEIS.index(voto.papel))),
                leis=questao.marcas.leis_citadas,
                regras=regras.temas(questao),
                verificador=vereditos[questao.id],
            )
            for questao in selecionadas
        ]
        destino: Path = self._gravar(sinais)
        resumo: Path = self._escrever_resumo(sinais, adiadas, time.monotonic() - inicio, fabrica.rodada)
        print(f"Sinais: {destino}\nResumo: {resumo}", flush=True)
        return destino

    def _selecionar(
        self, questoes: Sequence[QuestaoPreparada], temas: Sequence[TemaPreparado]
    ) -> tuple[list[QuestaoPreparada], int]:
        """Aplica os filtros: só IDs pedidos, gold pendente adiado e limite.

        Args:
            questoes: Todas as questões preparadas.
            temas: Árvore preparada (para ler a planilha do gold).

        Returns:
            ``(questões a classificar, número de questões do gold adiadas)``.
        """
        pendentes: set[str] = self._gold_pendente(temas) if self._parametros.adiar_gold_pendente else set()
        pedidas: set[str] = set(self._parametros.somente_ids)
        escolhidas: list[QuestaoPreparada] = [
            q for q in questoes if (not pedidas or q.id in pedidas) and q.id not in pendentes
        ]
        adiadas: int = sum(1 for q in questoes if (not pedidas or q.id in pedidas) and q.id in pendentes)
        gold: set[str] = self._gold_leva1()
        escolhidas.sort(key=lambda q: (q.id not in gold, q.id))
        if self._parametros.limite > 0:
            escolhidas = escolhidas[: self._parametros.limite]
        return escolhidas, adiadas

    def _gold_leva1(self) -> set[str]:
        """IDs do gold set (classificados primeiro, para os experimentos começarem cedo).

        Returns:
            IDs da amostra, ou vazio se ela não existir.
        """
        amostra: ArquivoAmostra = ArquivoAmostra(self._caminhos.dados_gold / "amostra_leva1.csv")
        return {item.id for item in amostra.ler()} if amostra.existe() else set()

    def _gold_pendente(self, temas: Sequence[TemaPreparado]) -> set[str]:
        """Lista as questões do gold ainda sem rótulo (rótulo cego, ADR-012).

        Args:
            temas: Árvore preparada.

        Returns:
            IDs pendentes.
        """
        amostra: ArquivoAmostra = ArquivoAmostra(self._caminhos.dados_gold / "amostra_leva1.csv")
        if not amostra.existe():
            return set()
        itens: list[ItemAmostra] = amostra.ler()
        planilha: PlanilhaRotulos = PlanilhaRotulos(
            self._caminhos.dados_gold / "rotulos_leva1.csv", self._parametros_gold, temas
        )
        if not planilha.caminho.is_file():
            return {item.id for item in itens}
        feitos: set[str] = {rotulo.id for rotulo in planilha.ler() if rotulo.preenchido}
        return {item.id for item in itens if item.id not in feitos}

    @staticmethod
    def _iniciar(
        classificadores: Sequence[Classificador],
        questoes: Sequence[QuestaoPreparada],
        fabrica: FabricaClientes,
    ) -> tuple[list[ThreadPoolExecutor], dict[Future[VotoClassificador], str]]:
        """Dispara os classificadores, com um executor por papel (limite de chamadas por provedor).

        O voto barato (modelo local, o mais lento) é disparado à parte, para o verificador não
        esperar por ele: o verificador só usa A e B.

        Args:
            classificadores: Classificadores a disparar.
            questoes: Questões a classificar (na ordem de prioridade).
            fabrica: Fábrica (limites de paralelismo).

        Returns:
            ``(executores, tarefa -> ID da questão)``.
        """
        executores: list[ThreadPoolExecutor] = [
            ThreadPoolExecutor(max_workers=fabrica.paralelismo(c.cliente.provedor), thread_name_prefix=c.cliente.papel)
            for c in classificadores
        ]
        futuros: dict[Future[VotoClassificador], str] = {}
        indice: int
        classificador: Classificador
        for indice, classificador in enumerate(classificadores):
            questao: QuestaoPreparada
            for questao in questoes:
                futuros[executores[indice].submit(classificador.classificar, questao)] = questao.id
        return executores, futuros

    @staticmethod
    def _encerrar(executores: Sequence[ThreadPoolExecutor]) -> None:
        """Espera e encerra os executores.

        Args:
            executores: Executores a encerrar.
        """
        executor: ThreadPoolExecutor
        for executor in executores:
            executor.shutdown(wait=True)

    @staticmethod
    def _acompanhar(
        futuros: dict[Future[VotoClassificador], str], votos: dict[str, list[VotoClassificador]], total: int, nome: str
    ) -> None:
        """Recolhe os votos à medida que ficam prontos e mostra o progresso.

        Args:
            futuros: Tarefa -> ID da questão.
            votos: Acumulador.
            total: Número de tarefas.
            nome: Grupo mostrado no progresso.
        """
        falhas: Counter[str] = Counter()
        passo: int = max(1, total // 20)
        feitas: int
        futuro: Future[VotoClassificador]
        for feitas, futuro in enumerate(as_completed(futuros), start=1):
            voto: VotoClassificador = futuro.result()
            votos[futuros[futuro]].append(voto)
            if not voto.ok:
                falhas[voto.papel] += 1
            if feitas % passo == 0 or feitas == total:
                print(f"  {nome}: {feitas}/{total} ({dict(falhas) or 'sem falhas'})", flush=True)

    def _verificar(
        self,
        verificador: VerificadorContrastivo,
        questoes: Sequence[QuestaoPreparada],
        votos: dict[str, list[VotoClassificador]],
        fabrica: FabricaClientes,
    ) -> dict[str, VereditoVerificador]:
        """Roda o verificador onde A e B concordam no ramo (ou ambos marcam ``fora``).

        Args:
            verificador: Verificador contrastivo.
            questoes: Questões classificadas.
            votos: Votos por questão.
            fabrica: Fábrica (limite de paralelismo).

        Returns:
            ``ID da questão -> veredito``.
        """
        vereditos: dict[str, VereditoVerificador] = {}
        tarefas: list[tuple[QuestaoPreparada, str, list[str]]] = []
        questao: QuestaoPreparada
        for questao in questoes:
            candidato: str
            sugeridos: list[str]
            motivo: str
            candidato, sugeridos, motivo = self.candidato_preliminar(votos[questao.id])
            if not self._parametros.verificar:
                vereditos[questao.id] = VereditoVerificador.nao_rodou("verificador desligado")
            elif not candidato:
                vereditos[questao.id] = VereditoVerificador.nao_rodou(motivo)
            else:
                tarefas.append((questao, candidato, sugeridos))
        print(f"Verificador: {len(tarefas)} candidatas", flush=True)
        executor: ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=fabrica.paralelismo(verificador.cliente.provedor)) as executor:
            futuros: dict[Future[VereditoVerificador], str] = {
                executor.submit(verificador.verificar, tarefa[0], tarefa[1], tarefa[2]): tarefa[0].id
                for tarefa in tarefas
            }
            passo: int = max(1, len(tarefas) // 10)
            feitas: int
            futuro: Future[VereditoVerificador]
            for feitas, futuro in enumerate(as_completed(futuros), start=1):
                vereditos[futuros[futuro]] = futuro.result()
                if feitas % passo == 0 or feitas == len(tarefas):
                    print(f"  verificador: {feitas}/{len(tarefas)}", flush=True)
        return vereditos

    def candidato_preliminar(self, votos: Sequence[VotoClassificador]) -> tuple[str, list[str], str]:
        """Escolhe o candidato que o verificador vai conferir.

        Regra: A e B válidos e no mesmo ramo (mesmo nó, ou pai e filho); o candidato é o mais
        específico dos dois. Se A e B marcam ``fora``, confere o tema de A (o verificador pode
        responder "nenhum").

        Args:
            votos: Votos da questão.

        Returns:
            ``(candidato, nós sugeridos pelas fontes, motivo de não rodar)``.
        """
        por_papel: dict[str, VotoClassificador] = {voto.papel: voto for voto in votos if voto.ok}
        a: VotoClassificador | None = por_papel.get("classificador_a")
        b: VotoClassificador | None = por_papel.get("classificador_b")
        if a is None or b is None:
            return "", [], "falta voto válido de A ou de B"
        sugeridos: list[str] = [a.tema_id, b.tema_id, a.segundo_id, b.segundo_id]
        if a.fora and b.fora:
            return a.tema_id, sugeridos, ""
        if not self._mesmo_ramo(a.tema_id, b.tema_id):
            return "", [], "A e B em ramos diferentes"
        candidato: str = a.tema_id if self._temas[a.tema_id].nivel >= self._temas[b.tema_id].nivel else b.tema_id
        return candidato, sugeridos, ""

    def _mesmo_ramo(self, tema_a: str, tema_b: str) -> bool:
        """Mesmo nó, ou um é pai direto do outro (a régua do case).

        Args:
            tema_a: Um ID.
            tema_b: Outro ID.

        Returns:
            ``True`` se estão no mesmo ramo.
        """
        if tema_a == tema_b:
            return True
        return self._temas[tema_a].parent_id == tema_b or self._temas[tema_b].parent_id == tema_a

    def _gravar(self, sinais: Sequence[SinaisQuestao]) -> Path:
        """Grava ``sinais.jsonl``.

        Args:
            sinais: Linhas na ordem das questões.

        Returns:
            Caminho gravado.
        """
        destino: Path = self._caminhos.dados_classificacao / "sinais.jsonl"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(
            "".join(json.dumps(linha.como_dict(), ensure_ascii=False) + "\n" for linha in sinais), encoding="utf-8"
        )
        return destino

    def _escrever_resumo(self, sinais: Sequence[SinaisQuestao], adiadas: int, segundos: float, rodada: str) -> Path:
        """Grava números agregados da rodada (nada por questão, para não expor o gold pendente).

        Args:
            sinais: Linhas geradas.
            adiadas: Questões do gold adiadas.
            segundos: Duração da execução.
            rodada: Identificador da rodada.

        Returns:
            Caminho do resumo.
        """
        total: int = len(sinais)
        ok: Counter[str] = Counter(voto.papel for linha in sinais for voto in linha.votos if voto.ok)
        exato: int = 0
        ramo: int = 0
        barato_com_a: int = 0
        fora: int = 0
        linha: SinaisQuestao
        for linha in sinais:
            a: VotoClassificador | None = linha.voto("classificador_a")
            b: VotoClassificador | None = linha.voto("classificador_b")
            v: VotoClassificador | None = linha.voto("voto_barato")
            if a is not None and b is not None and a.ok and b.ok:
                exato += a.tema_id == b.tema_id
                ramo += self._mesmo_ramo(a.tema_id, b.tema_id)
                fora += a.fora and b.fora
            if a is not None and v is not None and a.ok and v.ok:
                barato_com_a += self._mesmo_ramo(a.tema_id, v.tema_id)
        vereditos: Counter[str] = Counter(linha.verificador.veredito for linha in sinais)
        linhas: list[str] = [
            "# Passos 05 e 06: classificação e verificação",
            "",
            f"Rodada {rodada}, {datetime.now():%d/%m/%Y %H:%M}; duração {segundos / 60:.1f} min.",
            f"Questões classificadas: {total}; do gold adiadas até serem rotuladas: {adiadas}.",
            "",
            "| Medida | Valor |",
            "|---|---:|",
            *(f"| Votos válidos: {papel} | {ok[papel]} de {total} |" for papel in self.PAPEIS),
            f"| A = B (mesmo nó) | {exato} |",
            f"| A e B no mesmo ramo (régua) | {ramo} |",
            f"| Voto barato no ramo de A | {barato_com_a} |",
            f"| A e B marcam fora | {fora} |",
            *(f"| Verificador: {nome} | {quantidade} |" for nome, quantidade in sorted(vereditos.items())),
            "",
            "Concordância não é acerto: o acerto é medido no gold (ADR-012, ADR-014).",
            "",
        ]
        destino: Path = self._caminhos.saida_classificacao / "resumo_classificacao.md"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text("\n".join(linhas), encoding="utf-8")
        return destino
