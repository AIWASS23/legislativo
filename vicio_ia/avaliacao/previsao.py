"""Limiar de publicação e previsão de precisão e cobertura (ADR-011, etapa 4, e ADR-013).

1. A calibração dá ``P(acerto)`` a cada candidata. A **chance efetiva** desconta o risco de convenção
   do nó: ``P × (1 - taxa suposta do tipo de convenção)`` (ADR-005, ADR-013). É ela que ordena as
   candidatas e vai para a coluna ``confianca``: publicar num nó de risco "custa" confiança (ADR-011).
2. Reamostras da calibração (bootstrap, ou sorteios da Beta nas faixas) dão a incerteza da chance efetiva
   média de cada conjunto ``k`` (as ``k`` de maior chance, cortando só entre valores diferentes).
3. Publica-se o maior ``k`` cujo percentil 10 fica em 95% ou mais. Reserva: o maior ``k`` com estimativa
   pontual de 97% ou mais.
4. Intervalo informado: percentis 5 e 95 das reamostras para o conjunto escolhido (limiar fixo nas
   reamostras), menos as margens de convenção e de ambiguidade do rótulo no limite inferior.
5. Ponto informado: o estimador direto (acerto do gold que cai nas publicadas) com a mesma suavização de
   Jeffreys da calibração, combinado com o estimador por modelo (D12). Sem a suavização, 13 acertos em 13
   dariam 1,00 no direto, otimista demais para tão poucos itens.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np

from vicio_ia.avaliacao.calibracao import CalibradorBase, ExemploCalibracao
from vicio_ia.configuracao import ParametrosCalibracao
from vicio_ia.decisao.agregacao import DecisaoPreliminar
from vicio_ia.estatistica import Matriz


@dataclass(frozen=True)
class ResultadoPrevisao:
    """Limiar escolhido e previsão.

    Attributes:
        probabilidades: ``P`` calibrada de cada decisão com tema (candidatas e revisões).
        publicadas: IDs publicados, da maior para a menor ``P``.
        limiar: Menor ``P`` publicada (1,0 se nenhuma).
        regra: ``limite inferior``, ``reserva pontual`` ou ``nenhuma publicada``.
        precisao_modelo: Média da ``P`` das publicadas (estimador por modelo).
        precisao_direta: Acerto (régua estrita) do gold que cai nas publicadas, ou ``None``.
        precisao_direta_suavizada: O mesmo acerto com a suavização de Jeffreys no tamanho efetivo de Kish.
        gold_publicadas: Itens do gold entre as publicadas.
        margem_ambiguidade: Precisão tolerante menos estrita no gold.
        margem_convencao: Margem pela composição das publicadas e pelas taxas supostas.
        precisao_ponto: Ponto informado (já descontada a margem de convenção).
        precisao_intervalo: Intervalo informado.
        cobertura: Publicadas sobre o total de questões.
        cobertura_intervalo: Intervalo da cobertura.
        sensibilidade: ``(fator das taxas, ponto, limite inferior)``.
        reamostras_validas: Reamostras do bootstrap com as duas classes.
    """

    probabilidades: dict[str, float]
    publicadas: tuple[str, ...]
    limiar: float
    regra: str
    precisao_modelo: float
    precisao_direta: float | None
    precisao_direta_suavizada: float | None
    gold_publicadas: int
    margem_ambiguidade: float
    margem_convencao: float
    precisao_ponto: float
    precisao_intervalo: tuple[float, float]
    cobertura: float
    cobertura_intervalo: tuple[float, float]
    sensibilidade: tuple[tuple[float, float, float], ...]
    reamostras_validas: int


class PrevisorPrecisao:
    """Escolhe o limiar e prevê precisão e cobertura."""

    def __init__(self, parametros: ParametrosCalibracao, calibrador: CalibradorBase) -> None:
        """Guarda os parâmetros.

        Args:
            parametros: Parâmetros da calibração e do limiar.
            calibrador: Calibrador escolhido na validação cruzada (usado não ajustado, como molde).
        """
        self._parametros: ParametrosCalibracao = parametros
        self._calibrador: CalibradorBase = calibrador

    def prever(
        self,
        com_tema: Sequence[DecisaoPreliminar],
        exemplos: Sequence[ExemploCalibracao],
        acerto_tolerante: Mapping[str, bool],
    ) -> ResultadoPrevisao:
        """Ajusta, escolhe o limiar e calcula a previsão.

        Args:
            com_tema: Todas as decisões com tema (candidatas recebem o limiar; as demais só a ``P``).
            exemplos: Gold rotulado (acerto pela régua estrita e peso).
            acerto_tolerante: Acerto pela régua tolerante de cada exemplo, por ID.

        Returns:
            Previsão.
        """
        p: ParametrosCalibracao = self._parametros
        principal: CalibradorBase = self._calibrador.novo().ajustar(exemplos)
        calibradas: dict[str, float] = dict(zip((d.id for d in com_tema), principal.prever(com_tema), strict=True))
        fator: dict[str, float] = {d.id: 1.0 - p.taxas_convencao.get(d.tipo_convencao, 0.0) for d in com_tema}
        probabilidades: dict[str, float] = {i: round(calibradas[i] * fator[i], 4) for i in calibradas}
        candidatas: list[DecisaoPreliminar] = sorted(
            (d for d in com_tema if d.acao == "candidata"), key=lambda d: (-probabilidades[d.id], d.id)
        )
        reamostras: Matriz = principal.amostrar(candidatas, exemplos, p.reamostras, np.random.default_rng(p.semente))
        efetivas: Matriz = reamostras * np.array([fator[d.id] for d in candidatas], dtype=np.float64)
        acumuladas: Matriz = np.cumsum(efetivas, axis=1) / np.arange(1, len(candidatas) + 1)
        pontos: list[float] = list(
            np.cumsum([probabilidades[d.id] for d in candidatas]) / np.arange(1, len(candidatas) + 1)
        )
        ambiguidade: float = self._ambiguidade(exemplos, acerto_tolerante)
        desconto: float = ambiguidade if p.margem_ambiguidade_no_limiar else 0.0
        cortes: list[int] = self._cortes(candidatas, probabilidades)
        k: int = 0
        regra: str = "nenhuma publicada"
        indice: int
        if reamostras.shape[0] > 0:
            for indice in cortes:
                inferior: float = float(np.percentile(acumuladas[:, indice - 1], p.percentil_limiar))
                if inferior - desconto >= p.alvo_precisao:
                    k, regra = indice, "limite inferior"
                    break
        if k == 0:
            for indice in cortes:
                if pontos[indice - 1] >= p.reserva_pontual:
                    k, regra = indice, "reserva pontual"
                    break
        publicadas: list[DecisaoPreliminar] = candidatas[:k]
        ids_publicados: set[str] = {d.id for d in publicadas}
        no_conjunto: list[ExemploCalibracao] = [e for e in exemplos if e.decisao.id in ids_publicados]
        ambiguidade_publicadas: float = self._ambiguidade(no_conjunto, acerto_tolerante) if no_conjunto else ambiguidade
        return self._resultado(
            probabilidades,
            publicadas,
            regra,
            reamostras,
            exemplos,
            ambiguidade_publicadas,
            sum(calibradas[d.id] for d in candidatas[:k]) / k if k else 0.0,
        )

    @staticmethod
    def _cortes(candidatas: Sequence[DecisaoPreliminar], probabilidades: Mapping[str, float]) -> list[int]:
        """Tamanhos de conjunto permitidos: só na fronteira entre valores diferentes de ``P``.

        Com empates (todas as questões de uma faixa têm a mesma ``P``), cortar no meio escolheria
        questões de forma arbitrária.

        Args:
            candidatas: Candidatas ordenadas pela ``P``, da maior para a menor.
            probabilidades: ``P`` por ID.

        Returns:
            Tamanhos ``k`` permitidos, do maior para o menor.
        """
        cortes: list[int] = [
            k
            for k in range(1, len(candidatas) + 1)
            if k == len(candidatas) or probabilidades[candidatas[k].id] != probabilidades[candidatas[k - 1].id]
        ]
        return sorted(cortes, reverse=True)

    def _margens_convencao(self, candidatas: Sequence[DecisaoPreliminar], fator: float) -> list[float]:
        """Margem de convenção de cada prefixo das candidatas (ADR-013, margem b).

        Args:
            candidatas: Candidatas ordenadas.
            fator: Multiplicador das taxas supostas (sensibilidade).

        Returns:
            Margem para cada tamanho ``k`` (posição ``k - 1``).
        """
        taxas: dict[str, float] = self._parametros.taxas_convencao
        margens: list[float] = []
        soma: float = 0.0
        indice: int
        decisao: DecisaoPreliminar
        for indice, decisao in enumerate(candidatas, start=1):
            soma += taxas.get(decisao.tipo_convencao, 0.0) * fator
            margens.append(soma / indice)
        return margens

    def _suavizar(self, gold: Sequence[ExemploCalibracao]) -> float:
        """Acerto do gold nas publicadas com a suavização de Jeffreys (D12).

        Usa o tamanho efetivo de Kish, como a calibração: ``(acertos + a) / (n + 2a)``, com ``a`` = 0,5.

        Args:
            gold: Itens do gold que caem nas publicadas (não vazio).

        Returns:
            Acerto suavizado.
        """
        a: float = self._parametros.prior_direto
        pesos: list[float] = [e.peso for e in gold]
        soma: float = sum(pesos)
        n_efetivo: float = soma * soma / sum(w * w for w in pesos)
        acertos: float = sum(e.peso for e in gold if e.acerto) / soma * n_efetivo
        return (acertos + a) / (n_efetivo + 2 * a)

    @staticmethod
    def _ambiguidade(exemplos: Sequence[ExemploCalibracao], tolerante: Mapping[str, bool]) -> float:
        """Precisão tolerante menos estrita no gold com tema (ADR-013, margem a).

        Args:
            exemplos: Gold rotulado.
            tolerante: Acerto tolerante por ID.

        Returns:
            Diferença (0 se não houver exemplos).
        """
        if not exemplos:
            return 0.0
        estrita: float = sum(1 for e in exemplos if e.acerto) / len(exemplos)
        folgada: float = sum(1 for e in exemplos if tolerante.get(e.decisao.id, e.acerto)) / len(exemplos)
        return max(0.0, folgada - estrita)

    def _resultado(
        self,
        probabilidades: dict[str, float],
        publicadas: Sequence[DecisaoPreliminar],
        regra: str,
        reamostras: Matriz,
        exemplos: Sequence[ExemploCalibracao],
        ambiguidade: float,
        precisao_modelo: float,
    ) -> ResultadoPrevisao:
        """Monta a previsão do conjunto escolhido.

        Args:
            probabilidades: ``P`` por ID.
            publicadas: Publicadas.
            regra: Regra que escolheu o conjunto.
            reamostras: ``P`` reajustadas das candidatas (na ordem da ``P`` principal).
            exemplos: Gold rotulado.
            ambiguidade: Margem de ambiguidade (medida no gold que cai nas publicadas).
            precisao_modelo: Média da ``P`` das publicadas.

        Returns:
            Previsão.
        """
        p: ParametrosCalibracao = self._parametros
        k: int = len(publicadas)
        ids: set[str] = {d.id for d in publicadas}
        gold: list[ExemploCalibracao] = [e for e in exemplos if e.decisao.id in ids]
        peso_total: float = sum(e.peso for e in gold)
        direta: float | None = sum(e.peso for e in gold if e.acerto) / peso_total if gold and peso_total else None
        suavizada: float | None = self._suavizar(gold) if direta is not None else None
        if suavizada is None:
            bruto: float = precisao_modelo
        elif len(gold) >= p.min_gold_direto:
            bruto = suavizada
        else:
            bruto = (suavizada + precisao_modelo) / 2
        margem: float = self._margens_convencao(publicadas, 1.0)[-1] if k else 0.0
        if k and reamostras.shape[0] > 0:
            medias: Matriz = reamostras[:, :k].mean(axis=1)
            baixo: float = float(np.percentile(medias, p.percentis_intervalo[0]))
            alto: float = float(np.percentile(medias, p.percentis_intervalo[1]))
        else:
            baixo, alto = bruto, bruto
        intervalo: tuple[float, float] = (
            max(0.0, min(baixo, bruto) - margem - ambiguidade),
            min(1.0, max(alto, bruto)),
        )
        sensibilidade: list[tuple[float, float, float]] = []
        fator: float
        for fator in p.fatores_sensibilidade:
            m: float = self._margens_convencao(publicadas, fator)[-1] if k else 0.0
            sensibilidade.append((fator, round(bruto - m, 3), round(max(0.0, min(baixo, bruto) - m - ambiguidade), 3)))
        cobertura: float = k / p.total_questoes
        return ResultadoPrevisao(
            probabilidades=probabilidades,
            publicadas=tuple(d.id for d in publicadas),
            limiar=round(probabilidades[publicadas[-1].id], 4) if k else 1.0,
            regra=regra,
            precisao_modelo=round(precisao_modelo, 4),
            precisao_direta=round(direta, 4) if direta is not None else None,
            precisao_direta_suavizada=round(suavizada, 4) if suavizada is not None else None,
            gold_publicadas=len(gold),
            margem_ambiguidade=round(ambiguidade, 4),
            margem_convencao=round(margem, 4),
            precisao_ponto=round(bruto - margem, 4),
            precisao_intervalo=(round(intervalo[0], 4), round(intervalo[1], 4)),
            cobertura=round(cobertura, 4),
            cobertura_intervalo=(round(max(0.0, cobertura - 0.01), 4), round(min(1.0, cobertura + 0.01), 4)),
            sensibilidade=tuple(sensibilidade),
            reamostras_validas=int(reamostras.shape[0]),
        )
