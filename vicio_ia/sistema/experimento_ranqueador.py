"""E10: ranqueador de pares, logística × gradient boosting (ADR-022, ADR-024), fora da amostra na folha.

Cada configuração da grade pré-registrada (``ParametrosSistema.grade_e10``) é treinada com os mesmos candidatos,
atributos e partições do sistema. Vence a menor log-loss fora da amostra do nó escolhido; uma diferença menor que
``TOLERANCIA`` é empate, decidido pela configuração mais simples (a ordem da grade). Nenhum modelo de linguagem é
chamado.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import ClassVar, TextIO

import numpy as np

from vicio_ia.configuracao import Caminhos, ConfigRanqueador, ParametrosSistema
from vicio_ia.estatistica import Matriz
from vicio_ia.sistema.folha import ReguaEtapa2, RotuloFolha
from vicio_ia.sistema.pares import CarregadorSistema, DadosSistema, GeradorPares, ParesQuestao
from vicio_ia.sistema.politica import Calibrador, EscolhaQuestao, EscolhedorNo
from vicio_ia.sistema.ranqueador import TreinoRanqueador
from vicio_ia.sistema.validacao import ValidacaoCruzadaRepetida


@dataclass(frozen=True)
class ResultadoConfig:
    """Medidas de uma configuração, fora da amostra na folha.

    Attributes:
        config: Configuração.
        log_loss: Log-loss do nó escolhido (o critério).
        acertos: Nós escolhidos certos pela régua (de 100).
        topo: ``(k, certas, fora)`` entre as ``k`` de maior confiança.
    """

    config: ConfigRanqueador
    log_loss: float
    acertos: int
    topo: tuple[tuple[int, int, int], ...]


class ExperimentoRanqueador:
    """Roda o E10 e grava ``saidas/etapa2/e10_ranqueador.md`` e ``e10_ranqueador.csv``."""

    TOLERANCIA: ClassVar[float] = 0.005
    TOPOS: ClassVar[tuple[int, ...]] = (20, 30, 50)

    def __init__(self, caminhos: Caminhos | None = None, parametros: ParametrosSistema | None = None) -> None:
        """Guarda a configuração.

        Args:
            caminhos: Caminhos do projeto.
            parametros: Parâmetros do sistema.
        """
        self._caminhos: Caminhos = caminhos or Caminhos.padrao()
        self._parametros: ParametrosSistema = parametros or ParametrosSistema()

    def executar(self) -> Path:
        """Mede a grade e aplica a regra.

        Returns:
            Caminho do relatório.
        """
        p: ParametrosSistema = self._parametros
        dados: DadosSistema = CarregadorSistema(self._caminhos).carregar()
        gerador: GeradorPares = GeradorPares(dados, p)
        pares: dict[str, ParesQuestao] = gerador.pares()
        regua: ReguaEtapa2 = ReguaEtapa2(dados.temas)
        escolhedor: EscolhedorNo = EscolhedorNo(gerador, p.limiar_extra, p.max_extras)
        resultados: list[ResultadoConfig] = []
        config: ConfigRanqueador
        for config in p.grade_e10:
            treino: TreinoRanqueador = TreinoRanqueador(
                gerador,
                pares,
                dados.folha,
                dados.temas,
                ValidacaoCruzadaRepetida(p.partes_validacao, p.repeticoes_validacao, p.semente),
                config,
            )
            fora_amostra: dict[str, Matriz] = treino.fora_da_amostra([])
            escolhas: list[EscolhaQuestao] = [escolhedor.escolher(pares[r.id], fora_amostra[r.id]) for r in dados.folha]
            resultados.append(self._medir(config, escolhas, dados.folha, regua))
            print(f"  E10 {config.nome}: log-loss {resultados[-1].log_loss:.3f}, acerto {resultados[-1].acertos}/100")
        vencedor: ResultadoConfig = self._vencedor(resultados)
        return self._gravar(resultados, vencedor)

    def _medir(
        self,
        config: ConfigRanqueador,
        escolhas: list[EscolhaQuestao],
        folha: tuple[RotuloFolha, ...],
        regua: ReguaEtapa2,
    ) -> ResultadoConfig:
        """Medidas de uma configuração.

        Args:
            config: Configuração.
            escolhas: Nós escolhidos fora da amostra, na ordem da folha.
            folha: Rótulos.
            regua: Régua da etapa 2.

        Returns:
            Resultado.
        """
        p_folha: Matriz = np.array([e.p for e in escolhas], dtype=np.float64)
        acerto: Matriz = np.array(
            [1.0 if regua.acerta(e.tema, r) else 0.0 for e, r in zip(escolhas, folha, strict=True)], dtype=np.float64
        )
        ordem: list[int] = [int(i) for i in np.argsort(-p_folha, kind="stable")]
        topo: list[tuple[int, int, int]] = [
            (k, int(acerto[ordem[:k]].sum()), sum(1 for i in ordem[:k] if folha[i].fora)) for k in self.TOPOS
        ]
        return ResultadoConfig(config, Calibrador.log_loss(p_folha, acerto), int(acerto.sum()), tuple(topo))

    def _vencedor(self, resultados: list[ResultadoConfig]) -> ResultadoConfig:
        """Aplica a regra: menor log-loss, com empate abaixo da tolerância para a configuração mais simples.

        Args:
            resultados: Resultados, na ordem da grade.

        Returns:
            Vencedor.
        """
        melhor: float = min(r.log_loss for r in resultados)
        return next(r for r in resultados if r.log_loss < melhor + self.TOLERANCIA)

    def _gravar(self, resultados: list[ResultadoConfig], vencedor: ResultadoConfig) -> Path:
        """Grava o CSV e o relatório.

        Args:
            resultados: Resultados da grade.
            vencedor: Vencedor pela regra.

        Returns:
            Caminho do relatório.
        """
        pasta: Path = self._caminhos.saida_etapa2
        pasta.mkdir(parents=True, exist_ok=True)
        cabecalho: list[str] = ["configuracao", "log_loss", "acertos", *(f"topo{k}_certas" for k in self.TOPOS)]
        cabecalho.extend(f"topo{k}_fora" for k in self.TOPOS)
        linhas_csv: list[list[str]] = [cabecalho]
        r: ResultadoConfig
        for r in resultados:
            linhas_csv.append(
                [
                    r.config.nome,
                    f"{r.log_loss:.4f}",
                    str(r.acertos),
                    *(str(c) for _, c, _ in r.topo),
                    *(str(f) for _, _, f in r.topo),
                ]
            )
        arquivo: TextIO
        with (pasta / "e10_ranqueador.csv").open("w", encoding="utf-8", newline="") as arquivo:
            csv.writer(arquivo).writerows(linhas_csv)
        linhas: list[str] = [
            "# E10: ranqueador de pares, logística × gradient boosting",
            "",
            (
                f"Gerado em {datetime.now():%d/%m/%Y %H:%M}. Folha-verdade, fora da amostra (5 partes × 10 "
                "repetições), com os mesmos candidatos e atributos do sistema. Critério: menor log-loss do nó "
                f"escolhido; diferença menor que {self.TOLERANCIA} é empate, decidido pela configuração mais simples."
            ),
            "",
            "| Configuração | Log-loss | Acerto (100) | "
            + " | ".join(f"Topo {k}: certas (fora)" for k in self.TOPOS)
            + " |",
            "|---|---:|---:|" + "---:|" * len(self.TOPOS),
        ]
        linhas.extend(
            f"| {'**' if r is vencedor else ''}{r.config.nome}{'**' if r is vencedor else ''} | {r.log_loss:.3f} | "
            f"{r.acertos} | " + " | ".join(f"{c} ({f})" for _, c, f in r.topo) + " |"
            for r in resultados
        )
        linhas.extend(
            [
                "",
                (
                    f"**Vencedor pela regra pré-registrada:** {vencedor.config.nome}. Ranqueador em uso no sistema: "
                    f"{self._parametros.ranqueador.nome}."
                ),
                "",
            ]
        )
        destino: Path = pasta / "e10_ranqueador.md"
        destino.write_text("\n".join(linhas), encoding="utf-8")
        print(f"E10, vencedor pela regra: {vencedor.config.nome}. Relatório: {destino}")
        return destino
