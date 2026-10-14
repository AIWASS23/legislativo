"""Perfil da máquina: CPU, memória, GPUs, Ollama, CLIs de assinatura e credenciais."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

type TipoGPU = Literal["dedicada", "integrada", "unificada"]
"""``dedicada`` (VRAM própria), ``integrada`` (divide a RAM, pouco útil para LLM) ou ``unificada`` (Apple Silicon)."""


@dataclass(frozen=True)
class InfoGPU:
    """Uma GPU detectada.

    Attributes:
        nome: Nome do dispositivo.
        fabricante: NVIDIA, AMD, Intel ou Apple.
        tipo: Dedicada, integrada ou unificada.
        vram_total_gb: Memória de vídeo total (``None`` se desconhecida).
        vram_livre_gb: Memória de vídeo livre no momento da coleta.
        usavel_para_llm: Se o Ollama tende a usar essa GPU para rodar modelos.
        observacao: Detalhe adicional (driver, motivo de não ser usável).
    """

    nome: str
    fabricante: str
    tipo: TipoGPU
    vram_total_gb: float | None
    vram_livre_gb: float | None
    usavel_para_llm: bool
    observacao: str = ""


@dataclass(frozen=True)
class ModeloLocal:
    """Modelo instalado no Ollama, com os metadados usados para estimar memória.

    Attributes:
        nome: Nome no Ollama (``qwen3.5:4b``, ``hf.co/usuario/repo:Q4_K_M``).
        tamanho_gb: Tamanho do arquivo do modelo.
        parametros_b: Bilhões de parâmetros.
        quantizacao: Nível de quantização (``Q4_K_M``...).
        familia: Família declarada pelo modelo.
        contexto_max: Contexto máximo suportado (tokens).
        camadas_kv: Camadas que guardam cache de atenção (em modelos híbridos, só as de atenção completa).
        cabecas_kv: Cabeças de chave/valor por camada.
        dim_kv: Soma das dimensões de chave e valor por cabeça.
        metadados_completos: ``False`` quando algum dado foi estimado de forma conservadora.
        capacidades: Capacidades declaradas (``completion``, ``thinking``, ``vision``...).
    """

    nome: str
    tamanho_gb: float
    parametros_b: float | None
    quantizacao: str
    familia: str
    contexto_max: int | None
    camadas_kv: int | None
    cabecas_kv: int | None
    dim_kv: int | None
    metadados_completos: bool
    capacidades: tuple[str, ...]


@dataclass(frozen=True)
class InfoOllama:
    """Situação do Ollama na máquina.

    Attributes:
        instalado: O executável ``ollama`` existe.
        ativo: O servidor responde.
        versao: Versão do servidor ("" se inativo).
        modelos: Modelos instalados.
    """

    instalado: bool
    ativo: bool
    versao: str
    modelos: tuple[ModeloLocal, ...]


@dataclass(frozen=True)
class InfoCLI:
    """Uma CLI de agente usada como provedor por assinatura (``claude``, ``agy``).

    Attributes:
        nome: Nome do executável.
        instalado: O executável existe no PATH.
        versao: Versão informada pela CLI.
        modelos: Pares ``(id, nome)`` dos modelos que a CLI lista (vazio se não lista).
        observacao: Detalhe adicional.
    """

    nome: str
    instalado: bool
    versao: str
    modelos: tuple[tuple[str, str], ...]
    observacao: str = ""


@dataclass(frozen=True)
class PerfilMaquina:
    """Retrato da máquina no momento da análise.

    Attributes:
        sistema: Sistema operacional e versão.
        arquitetura: Arquitetura do processador (``x86_64``, ``arm64``).
        cpu_modelo: Modelo do processador.
        cpu_threads: Número de threads lógicas.
        ram_total_gb: Memória RAM total.
        ram_disponivel_gb: Memória RAM disponível no momento.
        gpus: GPUs detectadas.
        disco_livre_gb: Espaço livre onde os modelos locais ficam.
        ollama: Situação do Ollama.
        clis: CLIs de assinatura detectadas.
        credenciais: ``provedor -> existe credencial`` (nunca os valores).
        coletado_em: Data e hora da coleta (ISO 8601).
    """

    sistema: str
    arquitetura: str
    cpu_modelo: str
    cpu_threads: int
    ram_total_gb: float | None
    ram_disponivel_gb: float | None
    gpus: tuple[InfoGPU, ...]
    disco_livre_gb: float | None
    ollama: InfoOllama
    clis: tuple[InfoCLI, ...]
    credenciais: dict[str, bool]
    coletado_em: str

    def gpu_principal(self) -> InfoGPU | None:
        """Escolhe a GPU que o Ollama deve usar: a utilizável com mais VRAM.

        Returns:
            A GPU, ou ``None`` se nenhuma for utilizável.
        """
        usaveis: list[InfoGPU] = [gpu for gpu in self.gpus if gpu.usavel_para_llm]
        if not usaveis:
            return None
        return max(usaveis, key=lambda gpu: gpu.vram_total_gb or 0.0)

    def cli(self, nome: str) -> InfoCLI | None:
        """Busca uma CLI pelo nome.

        Args:
            nome: Nome do executável.

        Returns:
            A CLI, ou ``None`` se não foi verificada.
        """
        return next((cli for cli in self.clis if cli.nome == nome), None)

    def como_dict(self) -> dict[str, object]:
        """Converte o perfil em dicionário serializável em JSON.

        Returns:
            Dicionário com todos os campos.
        """
        return asdict(self)
