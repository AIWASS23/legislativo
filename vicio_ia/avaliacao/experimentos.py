"""Experimentos no gold, leva 1 (ADR-014): E0 (assunto de origem), E2 (A sozinho), E3 (B × A).

Cada execução acrescenta uma linha por experimento e modo da régua em
``saidas/experimentos/resultados.csv``. As métricas são agregadas: nenhuma questão
individual é mostrada, para não expor a saída dos modelos a quem ainda rotula.
"""

from __future__ import annotations

import csv
import json
from collections.abc import Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import ClassVar, TextIO

from vicio_ia.arvore import ArvoreTemas
from vicio_ia.avaliacao.metricas import AvaliadorGold, PrevisaoSistema, ResultadoAvaliacao
from vicio_ia.avaliacao.planilha import PlanilhaRotulos, RotuloGold, SituacaoLinha
from vicio_ia.avaliacao.pontuador import ModoRegua, PontuadorRegua
from vicio_ia.carregamento import CarregadorDados
from vicio_ia.classificacao.respostas import SinaisQuestao, VotoClassificador
from vicio_ia.configuracao import Caminhos, ParametrosGold
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada
from vicio_ia.sinais.origem import SinalOrigem
from vicio_ia.texto import ProcessadorTexto


class RegistroExperimentos:
    """Acrescenta resultados em ``saidas/experimentos/resultados.csv`` (só de acréscimo)."""

    COLUNAS: ClassVar[tuple[str, ...]] = (
        "horario",
        "experimento",
        "descricao",
        "modo",
        "rotuladas",
        "com_tema",
        "acertos",
        "precisao_top1",
        "cobertura_95",
        "modelos",
        "observacao",
    )

    def __init__(self, pasta: Path) -> None:
        """Define a pasta.

        Args:
            pasta: ``saidas/experimentos/``.
        """
        self._arquivo: Path = pasta / "resultados.csv"

    @property
    def arquivo(self) -> Path:
        """Caminho do CSV."""
        return self._arquivo

    def registrar(
        self, experimento: str, descricao: str, resultado: ResultadoAvaliacao, modelos: str, observacao: str
    ) -> None:
        """Acrescenta uma linha.

        Args:
            experimento: ID (``E0``...).
            descricao: O que foi testado.
            resultado: Métricas.
            modelos: Provedor e modelo de cada papel envolvido.
            observacao: Nota livre.
        """
        novo: bool = not self._arquivo.is_file()
        self._arquivo.parent.mkdir(parents=True, exist_ok=True)
        arquivo: TextIO
        with self._arquivo.open("a", encoding="utf-8", newline="") as arquivo:
            linhas: list[list[str | int]] = [list(self.COLUNAS)] if novo else []
            linhas.append(
                [
                    datetime.now().isoformat(timespec="seconds"),
                    experimento,
                    descricao,
                    resultado.modo,
                    resultado.rotuladas,
                    resultado.com_tema,
                    resultado.acertos_top1,
                    f"{resultado.precisao_top1:.3f}",
                    f"{resultado.cobertura_95:.3f}",
                    modelos,
                    observacao,
                ]
            )
            csv.writer(arquivo).writerows(linhas)


class PipelineExperimentos:
    """Roda os experimentos que só dependem do gold e de ``sinais.jsonl``."""

    MODOS: ClassVar[tuple[ModoRegua, ...]] = ("estrita", "tolerante")

    def __init__(self, caminhos: Caminhos | None = None, parametros_gold: ParametrosGold | None = None) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto (opcional).
            parametros_gold: Parâmetros do gold set (opcional).
        """
        self._caminhos: Caminhos = caminhos if caminhos is not None else Caminhos.padrao()
        self._gold: ParametrosGold = parametros_gold if parametros_gold is not None else ParametrosGold()

    def executar(self) -> Path:
        """Roda E0, E2 e E3 na leva 1 rotulada.

        Returns:
            Caminho de ``resultados.csv``.
        """
        leitor: LeitorPreparados = LeitorPreparados(self._caminhos)
        questoes: list[QuestaoPreparada] = leitor.questoes()
        temas: list[TemaPreparado] = leitor.temas()
        rotulos: list[RotuloGold] = self._rotulos(temas)
        avaliador: AvaliadorGold = AvaliadorGold(
            PontuadorRegua(ArvoreTemas(CarregadorDados(self._caminhos).carregar_temas()))
        )
        registro: RegistroExperimentos = RegistroExperimentos(self._caminhos.raiz / "saidas" / "experimentos")
        print(f"Gold, leva 1: {len(rotulos)} questões rotuladas e válidas")
        if not rotulos:
            print("Nada a avaliar ainda.")
            return registro.arquivo

        origem: SinalOrigem = SinalOrigem(temas, ProcessadorTexto())
        e0: dict[str, PrevisaoSistema] = {}
        questao: QuestaoPreparada
        for questao in questoes:
            achados: tuple[str, ...] = origem.temas(questao)
            if len(achados) == 1:
                e0[questao.id] = PrevisaoSistema(questao.id, achados[0], 1.0)
        self._registrar(registro, avaliador, "E0", "assunto de origem com um único nó válido", e0, rotulos, "", "")

        sinais: dict[str, SinaisQuestao] = self._sinais()
        faltando: int = sum(1 for rotulo in rotulos if rotulo.id not in sinais)
        nota: str = f"{faltando} rotuladas ainda sem classificação" if faltando else ""
        papel: str
        nome: str
        descricao: str
        for papel, nome, descricao in (
            ("classificador_a", "E2", "classificador A sozinho, ordenado pela autoconfiança"),
            ("classificador_b", "E3", "classificador B sozinho, ordenado pela autoconfiança"),
            ("voto_barato", "E3b", "voto barato sozinho (sem autoconfiança)"),
        ):
            previsoes: dict[str, PrevisaoSistema] = {}
            modelos: set[str] = set()
            linha: SinaisQuestao
            for linha in sinais.values():
                voto: VotoClassificador | None = linha.voto(papel)
                if voto is not None and voto.ok:
                    previsoes[linha.id] = PrevisaoSistema(linha.id, voto.tema_id, voto.autoconfianca or 0.0)
                    modelos.add(f"{voto.provedor}:{voto.modelo}")
            self._registrar(registro, avaliador, nome, descricao, previsoes, rotulos, ",".join(sorted(modelos)), nota)
        self._correlacao_erros(sinais, rotulos, avaliador)
        print(f"Resultados: {registro.arquivo}")
        return registro.arquivo

    def _rotulos(self, temas: Sequence[TemaPreparado]) -> list[RotuloGold]:
        """Lê os rótulos válidos da leva 1.

        Args:
            temas: Árvore preparada.

        Returns:
            Rótulos válidos.
        """
        planilha: PlanilhaRotulos = PlanilhaRotulos(self._caminhos.dados_gold / "rotulos_leva1.csv", self._gold, temas)
        if not planilha.caminho.is_file():
            return []
        situacoes: list[SituacaoLinha] = planilha.validar(planilha.ler())
        return [situacao.rotulo for situacao in situacoes if situacao.situacao == "rotulada"]

    def _sinais(self) -> dict[str, SinaisQuestao]:
        """Lê ``sinais.jsonl``, se existir.

        Returns:
            Sinais por ID.
        """
        arquivo: Path = self._caminhos.dados_classificacao / "sinais.jsonl"
        if not arquivo.is_file():
            return {}
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

    def _registrar(
        self,
        registro: RegistroExperimentos,
        avaliador: AvaliadorGold,
        experimento: str,
        descricao: str,
        previsoes: Mapping[str, PrevisaoSistema],
        rotulos: Sequence[RotuloGold],
        modelos: str,
        observacao: str,
    ) -> None:
        """Avalia nos dois modos, registra e mostra o resumo.

        Args:
            registro: Registro de resultados.
            avaliador: Avaliador com a régua.
            experimento: ID do experimento.
            descricao: Descrição.
            previsoes: Previsões do sistema.
            rotulos: Rótulos válidos.
            modelos: Modelos envolvidos.
            observacao: Nota.
        """
        modo: ModoRegua
        for modo in self.MODOS:
            resultado: ResultadoAvaliacao = avaliador.avaliar(previsoes, rotulos, modo)
            registro.registrar(experimento, descricao, resultado, modelos, observacao)
            print(
                f"  {experimento} ({modo}): {resultado.acertos_top1}/{resultado.com_tema} certas "
                f"({resultado.precisao_top1:.0%}) com tema em {resultado.com_tema}/{resultado.rotuladas}; "
                f"cobertura a 95%: {resultado.cobertura_95:.0%}"
            )

    def _correlacao_erros(
        self, sinais: Mapping[str, SinaisQuestao], rotulos: Sequence[RotuloGold], avaliador: AvaliadorGold
    ) -> None:
        """E3: quantas questões A e B erram juntos (régua estrita), contra o esperado se fossem independentes.

        Args:
            sinais: Sinais por ID.
            rotulos: Rótulos válidos.
            avaliador: Avaliador (para a régua).
        """
        pontuador: PontuadorRegua = avaliador.pontuador
        pares: list[tuple[bool, bool]] = []
        rotulo: RotuloGold
        for rotulo in rotulos:
            linha: SinaisQuestao | None = sinais.get(rotulo.id)
            if linha is None:
                continue
            a: VotoClassificador | None = linha.voto("classificador_a")
            b: VotoClassificador | None = linha.voto("classificador_b")
            if a is None or b is None or not a.ok or not b.ok:
                continue
            pares.append(
                (not pontuador.acerta(a.tema_id, rotulo, "estrita"), not pontuador.acerta(b.tema_id, rotulo, "estrita"))
            )
        if not pares:
            return
        n: int = len(pares)
        erro_a: float = sum(1 for p in pares if p[0]) / n
        erro_b: float = sum(1 for p in pares if p[1]) / n
        juntos: int = sum(1 for p in pares if p[0] and p[1])
        print(
            f"  E3 (erros juntos): A e B erram juntos em {juntos}/{n}; "
            f"se fossem independentes, seriam ~{erro_a * erro_b * n:.1f}"
        )
