"""E14: quanto mais rótulos ajudariam, e quais questões rotular primeiro (rotulagem ativa, para a produção).

Nenhuma questão da entrega é rotulada: rotular à mão questões avaliadas e treinar com elas misturaria o rótulo do
autor com a resposta do sistema. O experimento tem duas partes:

1. **Curva de aprendizado na folha:** o ranqueador do sistema é treinado com 40, 60 e 80 das 100 questões
   (sorteio estratificado, 10 repetições) e medido nas restantes. Se a log-loss ainda cai entre 60 e 80, mais
   rótulos ainda melhoram o modelo.
2. **Fila de rotulagem ativa:** as questões em ``revisar`` mais próximas do limiar de publicação, em rodízio
   pelas disciplinas. É a fila que o professor rotularia primeiro na produção (ADR-027).
"""

from __future__ import annotations

import csv
from collections.abc import Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import ClassVar, TextIO

import numpy as np
import numpy.typing as npt

from vicio_ia.configuracao import Caminhos, ParametrosSistema
from vicio_ia.estatistica import Matriz
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.sistema.folha import ReguaEtapa2, RotuloFolha
from vicio_ia.sistema.pares import CarregadorSistema, DadosSistema, GeradorPares, ParesQuestao
from vicio_ia.sistema.politica import Calibrador, EscolhaQuestao, EscolhedorNo
from vicio_ia.sistema.ranqueador import ModeloPares, TreinoRanqueador, criar_modelo
from vicio_ia.sistema.validacao import ValidacaoCruzadaRepetida


class ExperimentoRotulagem:
    """Roda o E14 e grava ``saidas/etapa2/e14_rotulagem.md`` e ``fila_rotulagem_ativa.csv``."""

    TAMANHOS: ClassVar[tuple[int, ...]] = (40, 60, 80)
    REPETICOES: ClassVar[int] = 10
    TAMANHO_FILA: ClassVar[int] = 150

    def __init__(self, caminhos: Caminhos | None = None, parametros: ParametrosSistema | None = None) -> None:
        """Guarda a configuração.

        Args:
            caminhos: Caminhos do projeto.
            parametros: Parâmetros do sistema.
        """
        self._caminhos: Caminhos = caminhos or Caminhos.padrao()
        self._parametros: ParametrosSistema = parametros or ParametrosSistema()

    def executar(self) -> Path:
        """Roda as duas partes.

        Returns:
            Caminho do relatório.
        """
        p: ParametrosSistema = self._parametros
        dados: DadosSistema = CarregadorSistema(self._caminhos).carregar()
        gerador: GeradorPares = GeradorPares(dados, p)
        pares: dict[str, ParesQuestao] = gerador.pares()
        curva: list[tuple[int, float, float, float]] = self._curva(dados, gerador, pares)
        fila: list[dict[str, str]] = self._fila(dados)
        return self._gravar(curva, fila)

    def _curva(
        self, dados: DadosSistema, gerador: GeradorPares, pares: Mapping[str, ParesQuestao]
    ) -> list[tuple[int, float, float, float]]:
        """Curva de aprendizado: log-loss e acerto no teste para cada tamanho de treino.

        Args:
            dados: Dados do sistema.
            gerador: Gerador dos atributos.
            pares: Pares por questão.

        Returns:
            ``(tamanho, log-loss média, acerto médio, desvio da log-loss)``.
        """
        p: ParametrosSistema = self._parametros
        folha: tuple[RotuloFolha, ...] = dados.folha
        regua: ReguaEtapa2 = ReguaEtapa2(dados.temas)
        escolhedor: EscolhedorNo = EscolhedorNo(gerador, p.limiar_extra, p.max_extras)
        treino: TreinoRanqueador = TreinoRanqueador(
            gerador, pares, folha, dados.temas, ValidacaoCruzadaRepetida(5, 1, p.semente), p.ranqueador
        )
        estratos: list[str] = ValidacaoCruzadaRepetida.estratos_folha(folha, dados.temas)
        resultado: list[tuple[int, float, float, float]] = []
        tamanho: int
        for tamanho in self.TAMANHOS:
            perdas: list[float] = []
            acertos: list[float] = []
            repeticao: int
            for repeticao in range(self.REPETICOES):
                indices_treino: list[int] = self._sorteio_estratificado(estratos, tamanho, p.semente + repeticao)
                teste: list[int] = [i for i in range(len(folha)) if i not in set(indices_treino)]
                rotulados: list[str] = [folha[i].id for i in indices_treino]
                modelo: ModeloPares = criar_modelo(p.ranqueador).ajustar(
                    np.vstack([gerador.matriz(pares[folha[i].id], rotulados) for i in indices_treino]),
                    np.concatenate([treino.rotulos(folha[i]) for i in indices_treino]),
                )
                escolhas: list[EscolhaQuestao] = [
                    escolhedor.escolher(
                        pares[folha[i].id], modelo.prever(gerador.matriz(pares[folha[i].id], rotulados))
                    )
                    for i in teste
                ]
                p_teste: Matriz = np.array([e.p for e in escolhas], dtype=np.float64)
                y_teste: Matriz = np.array(
                    [1.0 if regua.acerta(e.tema, folha[i]) else 0.0 for e, i in zip(escolhas, teste, strict=True)],
                    dtype=np.float64,
                )
                perdas.append(Calibrador.log_loss(p_teste, y_teste))
                acertos.append(float(y_teste.mean()))
            resultado.append((tamanho, float(np.mean(perdas)), float(np.mean(acertos)), float(np.std(perdas))))
            print(f"  E14 treino com {tamanho}: log-loss {resultado[-1][1]:.3f}, acerto {resultado[-1][2]:.0%}")
        return resultado

    @staticmethod
    def _sorteio_estratificado(estratos: Sequence[str], tamanho: int, semente: int) -> list[int]:
        """Sorteia ``tamanho`` índices, proporcional a cada estrato.

        Args:
            estratos: Estrato de cada questão.
            tamanho: Quantas sortear.
            semente: Semente.

        Returns:
            Índices sorteados, em ordem crescente.
        """
        gerador: np.random.Generator = np.random.default_rng(semente)
        ordem: npt.NDArray[np.int64] = gerador.permutation(len(estratos))
        por_estrato: dict[str, list[int]] = {}
        indice: int
        for indice in ordem:
            por_estrato.setdefault(estratos[int(indice)], []).append(int(indice))
        escolhidos: list[int] = []
        nome: str
        membros: list[int]
        for nome, membros in sorted(por_estrato.items()):
            cota: int = round(tamanho * len(membros) / len(estratos))
            escolhidos.extend(membros[:cota])
        restantes: list[int] = [int(i) for i in ordem if int(i) not in set(escolhidos)]
        escolhidos.extend(restantes[: max(0, tamanho - len(escolhidos))])
        return sorted(escolhidos[:tamanho])

    def _fila(self, dados: DadosSistema) -> list[dict[str, str]]:
        """Fila de rotulagem ativa: ``revisar`` mais perto do limiar, em rodízio pelas disciplinas.

        Args:
            dados: Dados do sistema.

        Returns:
            Linhas da fila.
        """
        entrada: TextIO
        with (self._caminhos.entregaveis / "publicacao.csv").open(encoding="utf-8", newline="") as entrada:
            linhas: list[dict[str, str]] = list(csv.DictReader(entrada))
        na_folha: set[str] = {r.id for r in dados.folha}
        temas: dict[str, TemaPreparado] = {t.tema_id: t for t in dados.temas}
        candidatas: list[dict[str, str]] = sorted(
            (
                linha
                for linha in linhas
                if linha["decisao"] == "revisar" and linha["id"] not in na_folha and linha["tema_central_id"] in temas
            ),
            key=lambda linha: (-float(linha["confianca"]), linha["id"]),
        )
        por_disciplina: dict[str, list[dict[str, str]]] = {}
        linha: dict[str, str]
        for linha in candidatas:
            por_disciplina.setdefault(temas[linha["tema_central_id"]].disciplina, []).append(linha)
        fila: list[dict[str, str]] = []
        while len(fila) < self.TAMANHO_FILA and any(por_disciplina.values()):
            nome: str
            for nome in sorted(por_disciplina):
                if por_disciplina[nome] and len(fila) < self.TAMANHO_FILA:
                    escolhida: dict[str, str] = por_disciplina[nome].pop(0)
                    fila.append(
                        {
                            "ordem": str(len(fila) + 1),
                            "id": escolhida["id"],
                            "tema_sugerido": escolhida["tema_central_id"],
                            "caminho": temas[escolhida["tema_central_id"]].caminho_exibicao,
                            "confianca": escolhida["confianca"],
                            "disciplina": nome,
                        }
                    )
        return fila

    def _gravar(self, curva: Sequence[tuple[int, float, float, float]], fila: Sequence[Mapping[str, str]]) -> Path:
        """Grava a fila e o relatório.

        Args:
            curva: Curva de aprendizado.
            fila: Fila de rotulagem ativa.

        Returns:
            Caminho do relatório.
        """
        pasta: Path = self._caminhos.saida_etapa2
        pasta.mkdir(parents=True, exist_ok=True)
        arquivo: TextIO
        with (pasta / "fila_rotulagem_ativa.csv").open("w", encoding="utf-8", newline="") as arquivo:
            escritor: csv.DictWriter[str] = csv.DictWriter(
                arquivo, fieldnames=["ordem", "id", "tema_sugerido", "caminho", "confianca", "disciplina"]
            )
            escritor.writeheader()
            escritor.writerows(fila)
        linhas: list[str] = [
            "# E14: rotulagem ativa (curva de aprendizado e fila para a produção)",
            "",
            (
                f"Gerado em {datetime.now():%d/%m/%Y %H:%M}. Ranqueador: {self._parametros.ranqueador.nome}. Treino com "
                f"parte da folha, teste no resto, {self.REPETICOES} sorteios estratificados por tamanho."
            ),
            "",
            "| Questões rotuladas no treino | Log-loss no teste | Desvio | Acerto do nó no teste |",
            "|---:|---:|---:|---:|",
            *(f"| {n} | {perda:.3f} | {desvio:.3f} | {acerto:.0%} |" for n, perda, acerto, desvio in curva),
            "",
            (
                f"Fila de rotulagem ativa: `saidas/etapa2/fila_rotulagem_ativa.csv`, com as {len(fila)} questões em "
                "`revisar` mais perto do limiar, em rodízio pelas disciplinas."
            ),
            "",
        ]
        destino: Path = pasta / "e14_rotulagem.md"
        destino.write_text("\n".join(linhas), encoding="utf-8")
        print(f"E14: relatório {destino}")
        return destino
