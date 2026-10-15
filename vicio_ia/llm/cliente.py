"""Cliente de um papel: provedor e modelo escolhidos, com cache e custo em toda chamada (ADR-003)."""

from __future__ import annotations

import threading
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from vicio_ia.configuracao import Caminhos, ParametrosLLM
from vicio_ia.llm.cache import CacheChamadas, RegistroChamada
from vicio_ia.llm.contratos import ErroProvedor, ProvedorLLM, RequisicaoLLM, RespostaLLM
from vicio_ia.llm.custo import ContadorCusto, TabelaPrecos
from vicio_ia.llm.fabrica import FabricaProvedores
from vicio_ia.llm.selecao import EscolhaPapel, SeletorModelos


class ErroForaDoCache(ErroProvedor):
    """No modo só cache, a chamada pedida não está gravada."""


@dataclass(frozen=True)
class ResultadoChamada:
    """Resposta de uma chamada e de onde ela veio.

    Attributes:
        resposta: Resposta padronizada.
        do_cache: ``True`` se veio do cache (nenhum modelo foi chamado).
        chave: Chave da chamada no cache.
    """

    resposta: RespostaLLM
    do_cache: bool
    chave: str


class ClienteLLM:
    """Faz as chamadas de um papel: consulta o cache, chama o provedor se preciso e grava."""

    def __init__(
        self,
        papel: str,
        provedor: ProvedorLLM,
        modelo: str,
        cache: CacheChamadas,
        precos: TabelaPrecos,
        rodada: str,
        somente_cache: bool,
    ) -> None:
        """Monta o cliente.

        Args:
            papel: Papel registrado no cache (pasta de ``runs/``).
            provedor: Provedor escolhido para o papel.
            modelo: Modelo escolhido.
            cache: Cache de chamadas.
            precos: Tabela de preços.
            rodada: Identificador da execução.
            somente_cache: Não chama modelos; falha se a chamada não estiver no cache.
        """
        self._papel: str = papel
        self._provedor: ProvedorLLM = provedor
        self._modelo: str = modelo
        self._cache: CacheChamadas = cache
        self._precos: TabelaPrecos = precos
        self._rodada: str = rodada
        self._somente_cache: bool = somente_cache
        self._trava: threading.Lock = threading.Lock()
        self._chamadas_reais: int = 0
        self._do_cache: int = 0

    @property
    def papel(self) -> str:
        """Papel do cliente."""
        return self._papel

    @property
    def provedor(self) -> str:
        """Nome do provedor."""
        return self._provedor.nome

    @property
    def modelo(self) -> str:
        """Modelo."""
        return self._modelo

    @property
    def estatisticas(self) -> tuple[int, int]:
        """``(chamadas feitas ao modelo, respostas servidas pelo cache)`` nesta execução."""
        with self._trava:
            return self._chamadas_reais, self._do_cache

    def gerar(self, requisicao: RequisicaoLLM, versao_prompt: str, rotulo: str, tentativa: int = 1) -> ResultadoChamada:
        """Faz uma chamada, usando o cache quando possível.

        Args:
            requisicao: Prompt, tarefa e schema.
            versao_prompt: Versão do arquivo de prompt (entra na chave).
            rotulo: O que está sendo processado (ID da questão ou do tema), para o registro.
            tentativa: 1 na primeira chamada; 2 ou mais para repetir depois de resposta inválida.

        Returns:
            Resposta e origem.

        Raises:
            ErroForaDoCache: No modo só cache, se a chamada não estiver gravada.
            ErroProvedor: Se a chamada ao provedor falhar.
        """
        chave: str = CacheChamadas.chave(
            self._provedor.nome,
            self._modelo,
            self._provedor.parametros_cache(),
            requisicao,
            versao_prompt,
            tentativa,
        )
        gravado: RegistroChamada | None = self._cache.obter(chave)
        if gravado is not None:
            with self._trava:
                self._do_cache += 1
            return ResultadoChamada(gravado.resposta, True, chave)
        if self._somente_cache:
            raise ErroForaDoCache(f"{self._papel}: {rotulo} não está no cache (modo só cache)")
        resposta: RespostaLLM = self._provedor.gerar(requisicao, self._modelo)
        custo: float | None = (
            resposta.custo_usd
            if resposta.custo_usd is not None
            else self._precos.custo(resposta.provedor, self._modelo, resposta.uso)
        )
        self._cache.gravar(
            RegistroChamada(
                chave=chave,
                papel=self._papel,
                rotulo=rotulo,
                versao_prompt=versao_prompt,
                tentativa=tentativa,
                resposta=resposta,
                custo_usd=custo,
                rodada=self._rodada,
                horario=datetime.now().isoformat(timespec="seconds"),
            )
        )
        with self._trava:
            self._chamadas_reais += 1
        return ResultadoChamada(resposta, False, chave)


class FabricaClientes:
    """Cria os clientes dos papéis com um cache, uma tabela de preços e uma rodada em comum."""

    def __init__(
        self,
        caminhos: Caminhos | None = None,
        parametros: ParametrosLLM | None = None,
        somente_cache: bool = False,
    ) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto (opcional).
            parametros: Parâmetros de LLM (opcional).
            somente_cache: Não chama modelos (refaz tudo a partir de ``runs/``).
        """
        self._caminhos: Caminhos = caminhos if caminhos is not None else Caminhos.padrao()
        self._parametros: ParametrosLLM = parametros if parametros is not None else ParametrosLLM()
        self._somente_cache: bool = somente_cache
        self._cache: CacheChamadas = CacheChamadas(self._caminhos.runs)
        self._precos: TabelaPrecos = TabelaPrecos.do_catalogo(self._caminhos.catalogo_modelos)
        self._provedores: FabricaProvedores = FabricaProvedores(self._caminhos, self._parametros)
        self._rodada: str = f"{datetime.now():%Y%m%d-%H%M%S}"
        self._escolhas: dict[str, EscolhaPapel] | None = None
        self._clientes: list[ClienteLLM] = []

    @property
    def rodada(self) -> str:
        """Identificador desta execução."""
        return self._rodada

    def escolhas(self) -> dict[str, EscolhaPapel]:
        """Resolve (uma vez) o provedor e o modelo de cada papel.

        Returns:
            ``papel -> escolha``.
        """
        if self._escolhas is None:
            self._escolhas = SeletorModelos(self._caminhos, self._parametros).resolver()
        return self._escolhas

    def cliente(self, papel: str, papel_modelo: str | None = None) -> ClienteLLM:
        """Cria o cliente de um papel.

        Args:
            papel: Papel registrado no cache (ex.: ``cartoes``).
            papel_modelo: Papel cujo modelo será usado (ex.: ``verificador``); padrão: o próprio ``papel``.

        Returns:
            Cliente pronto.

        Raises:
            ErroProvedor: Se o papel não tiver modelo escolhido.
        """
        origem: str = papel_modelo if papel_modelo is not None else papel
        escolha: EscolhaPapel | None = self.escolhas().get(origem)
        if escolha is None:
            raise ErroProvedor(f"nenhum modelo escolhido para o papel {origem!r}; rode executar_infra.py")
        cliente: ClienteLLM = ClienteLLM(
            papel,
            self._provedores.obter(escolha.provedor),
            escolha.modelo,
            self._cache,
            self._precos,
            self._rodada,
            self._somente_cache,
        )
        self._clientes.append(cliente)
        return cliente

    def cliente_fixo(self, papel: str, provedor: str, modelo: str) -> ClienteLLM:
        """Cria um cliente com provedor e modelo fixos, fora da escolha por papel.

        Args:
            papel: Papel registrado no cache.
            provedor: Nome do provedor.
            modelo: Modelo.

        Returns:
            Cliente pronto.
        """
        cliente: ClienteLLM = ClienteLLM(
            papel,
            self._provedores.obter(provedor),
            modelo,
            self._cache,
            self._precos,
            self._rodada,
            self._somente_cache,
        )
        self._clientes.append(cliente)
        return cliente

    def paralelismo(self, provedor: str) -> int:
        """Chamadas simultâneas permitidas para um provedor.

        Args:
            provedor: Nome do provedor.

        Returns:
            Limite configurado (1 se ausente).
        """
        return max(1, self._parametros.paralelismo.get(provedor, 1))

    def escrever_resumo_custos(self) -> Path:
        """Grava o resumo de custo e tempo a partir de todo o cache.

        Returns:
            Caminho de ``saidas/custos/resumo_custos.md``.
        """
        return ContadorCusto().escrever(self._cache.registros(), self._caminhos.saida_custos)

    def resumo_sessao(self) -> str:
        """Resume as chamadas desta execução por papel.

        Returns:
            Texto com chamadas feitas e respostas do cache.
        """
        partes: list[str] = []
        cliente: ClienteLLM
        for cliente in self._clientes:
            reais: int
            cache: int
            reais, cache = cliente.estatisticas
            partes.append(f"{cliente.papel} ({cliente.provedor}:{cliente.modelo}): {reais} chamadas, {cache} do cache")
        return "; ".join(partes) if partes else "nenhuma chamada"
