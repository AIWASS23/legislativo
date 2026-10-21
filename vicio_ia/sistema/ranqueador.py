"""Ranqueador de temas (ADR-022): modelo sobre os pares (questão, tema), sem modelo de linguagem.

O modelo é uma logística L2 ou um gradient boosting de árvores, escolhido no E10 pela log-loss fora da amostra.

Um par é positivo quando publicar aquele tema estaria certo pela régua da etapa 2 (o tema central, um extra, ou
o pai ou filho de um deles). Por isso a probabilidade prevista de um par já é P(certo | publicar o nó), e a
escolha do nó pela régua (ADR-022, decisão 4) vira escolher o candidato de maior probabilidade: os pais dos
subtemas também são candidatos, e o recuo para o pai acontece quando ele soma mais chance que os filhos.

As questões fora da folha entram no treino com todos os pares negativos, então a probabilidade já desconta o
risco de fora (plano B da ADR-023). As 659 questões são previstas pelos modelos da validação cruzada (cada um
treinado com 80% da folha): as da folha, pelos modelos que não as viram; as avaliadas, pela média de todos.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier  # type: ignore[import-untyped]

from vicio_ia.configuracao import ConfigRanqueador
from vicio_ia.estatistica import Matriz, RegressaoLogisticaL2
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.sistema.folha import ReguaEtapa2, RotuloFolha
from vicio_ia.sistema.pares import GeradorPares, ParesQuestao
from vicio_ia.sistema.validacao import Particao, ValidacaoCruzadaRepetida


class ModeloPares(ABC):
    """Contrato de um modelo de pares: ajusta com os pares rotulados e prevê P(certo) de cada par."""

    @abstractmethod
    def ajustar(self, x: Matriz, y: Matriz) -> ModeloPares:
        """Ajusta o modelo.

        Args:
            x: Atributos dos pares.
            y: 1 nos pares certos pela régua.

        Returns:
            O próprio modelo.
        """

    @abstractmethod
    def prever(self, x: Matriz) -> Matriz:
        """P(certo) de cada par.

        Args:
            x: Atributos dos pares.

        Returns:
            Probabilidades.
        """

    @property
    def coeficientes(self) -> Matriz | None:
        """Intercepto e pesos dos atributos padronizados, quando o modelo é linear."""
        return None


class ModeloLogistico(ModeloPares):
    """Logística L2 sobre atributos padronizados pela média e pelo desvio do treino."""

    def __init__(self, penalidade: float) -> None:
        """Define a penalidade.

        Args:
            penalidade: Penalidade L2.
        """
        self._penalidade: float = penalidade
        self._media: Matriz = np.zeros(0, dtype=np.float64)
        self._desvio: Matriz = np.ones(0, dtype=np.float64)
        self._logistica: RegressaoLogisticaL2 = RegressaoLogisticaL2(penalidade)

    def ajustar(self, x: Matriz, y: Matriz) -> ModeloLogistico:
        """Ajusta o modelo.

        Args:
            x: Atributos dos pares.
            y: 1 nos pares certos pela régua.

        Returns:
            O próprio modelo.
        """
        self._media = x.mean(axis=0)
        self._desvio = x.std(axis=0) + 1e-9
        self._logistica = RegressaoLogisticaL2(self._penalidade).ajustar(
            (x - self._media) / self._desvio, y, np.ones(len(y), dtype=np.float64)
        )
        return self

    def prever(self, x: Matriz) -> Matriz:
        """P(certo) de cada par.

        Args:
            x: Atributos dos pares.

        Returns:
            Probabilidades.
        """
        return self._logistica.prever((x - self._media) / self._desvio)

    @property
    def coeficientes(self) -> Matriz | None:
        """Intercepto seguido dos coeficientes dos atributos padronizados."""
        return self._logistica.coeficientes


class ModeloBoosting(ModeloPares):
    """Gradient boosting de árvores por histograma (``HistGradientBoostingClassifier``, o algoritmo do LightGBM).

    Semente fixa e sem parada antecipada: o mesmo treino gera o mesmo modelo.
    """

    def __init__(self, config: ConfigRanqueador) -> None:
        """Guarda a configuração.

        Args:
            config: Profundidade, folha mínima, árvores, taxa de aprendizado e L2.
        """
        self._config: ConfigRanqueador = config
        self._modelo: object = None

    def ajustar(self, x: Matriz, y: Matriz) -> ModeloBoosting:
        """Ajusta o modelo.

        Args:
            x: Atributos dos pares.
            y: 1 nos pares certos pela régua.

        Returns:
            O próprio modelo.
        """
        c: ConfigRanqueador = self._config
        modelo: HistGradientBoostingClassifier = HistGradientBoostingClassifier(
            max_depth=c.profundidade,
            min_samples_leaf=c.folha_minima,
            max_iter=c.iteracoes,
            learning_rate=c.taxa_aprendizado,
            l2_regularization=c.l2,
            early_stopping=False,
            random_state=0,
        )
        self._modelo = modelo.fit(x, y)
        return self

    def prever(self, x: Matriz) -> Matriz:
        """P(certo) de cada par.

        Args:
            x: Atributos dos pares.

        Returns:
            Probabilidades.
        """
        modelo: HistGradientBoostingClassifier = self._modelo
        return np.asarray(modelo.predict_proba(x)[:, 1], dtype=np.float64)


def criar_modelo(config: ConfigRanqueador) -> ModeloPares:
    """Cria um modelo de pares pela configuração.

    Args:
        config: Configuração do ranqueador.

    Returns:
        Modelo sem ajuste.

    Raises:
        ValueError: Se o tipo for desconhecido.
    """
    if config.tipo == "logistica":
        return ModeloLogistico(config.penalidade)
    if config.tipo == "boosting":
        return ModeloBoosting(config)
    raise ValueError(f"tipo de ranqueador desconhecido: {config.tipo!r}")


class TreinoRanqueador:
    """Treina o ranqueador na folha, mede fora da amostra e prevê as 659 questões."""

    def __init__(
        self,
        gerador: GeradorPares,
        pares: Mapping[str, ParesQuestao],
        folha: Sequence[RotuloFolha],
        temas: Sequence[TemaPreparado],
        validacao: ValidacaoCruzadaRepetida,
        config: ConfigRanqueador,
    ) -> None:
        """Guarda as dependências.

        Args:
            gerador: Gerador dos atributos (para o kNN de cada partição).
            pares: Pares fixos por questão.
            folha: Folha-verdade.
            temas: Árvore preparada.
            validacao: Validação cruzada repetida.
            config: Configuração do ranqueador (logística ou boosting, E10).
        """
        self._gerador: GeradorPares = gerador
        self._pares: Mapping[str, ParesQuestao] = pares
        self._folha: tuple[RotuloFolha, ...] = tuple(folha)
        self._temas: tuple[TemaPreparado, ...] = tuple(temas)
        self._regua: ReguaEtapa2 = ReguaEtapa2(temas)
        self._validacao: ValidacaoCruzadaRepetida = validacao
        self._config: ConfigRanqueador = config

    def rotulos(self, rotulo: RotuloFolha) -> Matriz:
        """Rótulo de cada candidato de uma questão da folha.

        Args:
            rotulo: Rótulo da equipe.

        Returns:
            1 nos candidatos certos pela régua.
        """
        return np.array(
            [1.0 if self._regua.acerta(t, rotulo) else 0.0 for t in self._pares[rotulo.id].candidatos],
            dtype=np.float64,
        )

    def _ajustar(self, indices: Sequence[int]) -> ModeloPares:
        """Ajusta nas questões da folha indicadas; o kNN só usa essas questões como vizinhas.

        Args:
            indices: Posições na folha.

        Returns:
            Modelo ajustado.
        """
        rotulados: list[str] = [self._folha[i].id for i in indices]
        blocos_x: list[Matriz] = [self._gerador.matriz(self._pares[self._folha[i].id], rotulados) for i in indices]
        blocos_y: list[Matriz] = [self.rotulos(self._folha[i]) for i in indices]
        return criar_modelo(self._config).ajustar(np.vstack(blocos_x), np.concatenate(blocos_y))

    def fora_da_amostra(self, outras: Sequence[str]) -> dict[str, Matriz]:
        """P(certo) de cada candidato, sempre prevista por modelos que não viram a questão.

        Nas questões da folha, é a média, entre as repetições, do modelo da partição em que a questão ficou no
        teste. Nas outras questões, é a média dos modelos de todas as partições. Assim as duas ficam na mesma
        escala (modelos treinados com 80% da folha), e a calibração medida na folha vale para as avaliadas.

        Args:
            outras: Questões fora da folha a prever.

        Returns:
            Probabilidade média de cada candidato, por questão.
        """
        ids: list[str] = [r.id for r in self._folha] + list(outras)
        soma: dict[str, Matriz] = {q: np.zeros(len(self._pares[q].candidatos)) for q in ids}
        contagem: dict[str, int] = {q: 0 for q in ids}
        particao: Particao
        for particao in self._validacao.particoes(ValidacaoCruzadaRepetida.estratos_folha(self._folha, self._temas)):
            modelo: ModeloPares = self._ajustar(particao.treino)
            rotulados: list[str] = [self._folha[i].id for i in particao.treino]
            alvos: list[str] = [self._folha[i].id for i in particao.teste] + list(outras)
            questao: str
            for questao in alvos:
                soma[questao] += modelo.prever(self._gerador.matriz(self._pares[questao], rotulados))
                contagem[questao] += 1
        return {q: soma[q] / max(contagem[q], 1) for q in soma}

    def ajustar_final(self) -> ModeloPares:
        """Ajusta nas 100 questões da folha (só para relatar os pesos; a decisão usa os modelos da validação).

        Returns:
            Modelo final.
        """
        return self._ajustar(range(len(self._folha)))
