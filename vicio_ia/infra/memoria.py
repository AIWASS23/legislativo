"""Estimativa de memória de modelos locais: pesos + cache de atenção (KV) + sobrecarga."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from vicio_ia.configuracao import ParametrosLLM
from vicio_ia.infra.catalogo import ModeloCatalogado


@dataclass(frozen=True)
class EstimativaMemoria:
    """Memória que um modelo local precisa para um dado contexto.

    Attributes:
        pesos_gb: Memória dos pesos (tamanho do arquivo quantizado).
        cache_kv_gb: Memória do cache de atenção para o contexto pedido.
        total_gb: Pesos + cache + sobrecarga.
        kv_bytes_por_token: Bytes de cache de atenção por token de contexto.
        conservadora: ``True`` quando faltaram metadados e a estimativa foi feita pelo lado alto.
    """

    pesos_gb: float
    cache_kv_gb: float
    total_gb: float
    kv_bytes_por_token: float
    conservadora: bool


class EstimadorMemoria:
    """Estima a memória de modelos locais a partir dos metadados de arquitetura.

    Cache de atenção por token = camadas com cache × cabeças KV × (dim. chave + dim. valor)
    × bytes por elemento. Sem metadados, usa um valor por bilhão de parâmetros que fica
    acima do real nos modelos comuns.
    """

    BYTES_KV_POR_BILHAO_SEM_METADADOS: ClassVar[float] = 30_000.0
    BYTES_KV_SEM_NADA: ClassVar[float] = 150_000.0
    GB: ClassVar[float] = 1e9

    def __init__(self, parametros: ParametrosLLM) -> None:
        """Recebe os parâmetros de estimativa.

        Args:
            parametros: Bytes por elemento do cache e sobrecarga por modelo.
        """
        self._parametros: ParametrosLLM = parametros

    def kv_bytes_por_token(self, modelo: ModeloCatalogado) -> tuple[float, bool]:
        """Calcula os bytes de cache de atenção por token de contexto.

        Args:
            modelo: Modelo local.

        Returns:
            ``(bytes por token, estimativa conservadora?)``.
        """
        if modelo.camadas_kv and modelo.cabecas_kv and modelo.dim_kv:
            exato: float = float(
                modelo.camadas_kv * modelo.cabecas_kv * modelo.dim_kv * self._parametros.bytes_cache_kv
            )
            return exato, not modelo.metadados_completos
        if modelo.parametros_b:
            return self.BYTES_KV_POR_BILHAO_SEM_METADADOS * modelo.parametros_b, True
        return self.BYTES_KV_SEM_NADA, True

    def estimar(self, modelo: ModeloCatalogado, contexto_tokens: int) -> EstimativaMemoria:
        """Estima a memória total para rodar o modelo com o contexto pedido.

        Args:
            modelo: Modelo local.
            contexto_tokens: Tamanho do contexto (``num_ctx``).

        Returns:
            Estimativa de memória.
        """
        por_token: float
        conservadora: bool
        por_token, conservadora = self.kv_bytes_por_token(modelo)
        pesos: float = modelo.tamanho_gb or (modelo.parametros_b or 8.0) * 0.6
        cache: float = por_token * contexto_tokens / self.GB
        return EstimativaMemoria(
            pesos_gb=pesos,
            cache_kv_gb=cache,
            total_gb=pesos + cache + self._parametros.sobrecarga_memoria_gb,
            kv_bytes_por_token=por_token,
            conservadora=conservadora,
        )

    def contexto_que_cabe(self, modelo: ModeloCatalogado, memoria_gb: float) -> int:
        """Calcula o maior contexto que cabe numa quantidade de memória.

        Args:
            modelo: Modelo local.
            memoria_gb: Memória disponível (ex.: VRAM utilizável).

        Returns:
            Tokens de contexto (0 se nem os pesos cabem), limitado ao contexto máximo do modelo.
        """
        estimativa: EstimativaMemoria = self.estimar(modelo, 0)
        sobra: float = memoria_gb - estimativa.total_gb
        if sobra <= 0:
            return 0
        tokens: int = int(sobra * self.GB / estimativa.kv_bytes_por_token)
        return min(tokens, modelo.contexto_max) if modelo.contexto_max else tokens
