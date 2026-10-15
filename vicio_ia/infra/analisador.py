"""Coleta do perfil da máquina: hardware, Ollama, CLIs de assinatura e credenciais."""

from __future__ import annotations

import json
import os
import platform
import re
import shutil
import subprocess
import urllib.error
import urllib.request
from datetime import datetime
from http.client import HTTPResponse
from pathlib import Path
from typing import ClassVar

from vicio_ia.ambiente import CarregadorAmbiente
from vicio_ia.configuracao import ParametrosLLM
from vicio_ia.infra.perfil import InfoCLI, InfoGPU, InfoOllama, ModeloLocal, PerfilMaquina


class AnalisadorInfra:
    """Detecta o que a máquina oferece para rodar ou acessar modelos de linguagem.

    Funciona em Linux (completo), macOS (CPU, memória, Apple Silicon) e, de forma
    parcial, em Windows. Toda detecção falha de forma silenciosa: o que não puder
    ser medido fica ``None`` no perfil.
    """

    GB: ClassVar[float] = 1e9
    _RE_PARAMETROS: ClassVar[re.Pattern[str]] = re.compile(r"([\d.]+)\s*([BbMm])")

    def __init__(self, parametros: ParametrosLLM, ambiente: CarregadorAmbiente) -> None:
        """Recebe as dependências.

        Args:
            parametros: Endereço do Ollama e demais parâmetros de LLM.
            ambiente: Detector de credenciais.
        """
        self._parametros: ParametrosLLM = parametros
        self._ambiente: CarregadorAmbiente = ambiente

    def analisar(self) -> PerfilMaquina:
        """Coleta o perfil completo da máquina.

        Returns:
            Perfil da máquina.
        """
        ram_total: float | None
        ram_disponivel: float | None
        ram_total, ram_disponivel = self._memoria()
        return PerfilMaquina(
            sistema=f"{platform.system()} {platform.release()}",
            arquitetura=platform.machine(),
            cpu_modelo=self._cpu_modelo(),
            cpu_threads=os.cpu_count() or 1,
            ram_total_gb=ram_total,
            ram_disponivel_gb=ram_disponivel,
            gpus=self._gpus(ram_total),
            disco_livre_gb=self._disco_livre(),
            ollama=self._ollama(),
            clis=(self._cli_claude(), self._cli_agy(), self._cli_codex()),
            credenciais=self._ambiente.credenciais(),
            coletado_em=datetime.now().isoformat(timespec="seconds"),
        )

    @staticmethod
    def _rodar(comando: list[str], timeout: float) -> str | None:
        """Executa um comando e devolve a saída, sem nunca lançar exceção.

        Args:
            comando: Comando e argumentos.
            timeout: Tempo máximo em segundos.

        Returns:
            Saída padrão, ou ``None`` se o comando não existir, falhar ou demorar demais.
        """
        if shutil.which(comando[0]) is None:
            return None
        try:
            processo: subprocess.CompletedProcess[str] = subprocess.run(
                comando, capture_output=True, text=True, timeout=timeout, check=False
            )
        except (OSError, subprocess.TimeoutExpired):
            return None
        return processo.stdout if processo.returncode == 0 else None

    def _http_json(self, caminho: str, corpo: dict[str, object] | None, timeout: float) -> dict[str, object] | None:
        """Chama a API HTTP do Ollama e decodifica a resposta JSON.

        Args:
            caminho: Caminho da API (``/api/tags``).
            corpo: Corpo JSON para POST; ``None`` faz GET.
            timeout: Tempo máximo em segundos.

        Returns:
            Resposta decodificada, ou ``None`` em caso de erro.
        """
        url: str = self._parametros.ollama_url.rstrip("/") + caminho
        dados: bytes | None = None if corpo is None else json.dumps(corpo).encode("utf-8")
        requisicao: urllib.request.Request = urllib.request.Request(
            url, data=dados, headers={"Content-Type": "application/json"}
        )
        resposta: HTTPResponse
        try:
            with urllib.request.urlopen(requisicao, timeout=timeout) as resposta:
                valor: object = json.loads(resposta.read().decode("utf-8"))
        except (urllib.error.URLError, OSError, ValueError):
            return None
        return valor if isinstance(valor, dict) else None

    def _cpu_modelo(self) -> str:
        """Descobre o modelo do processador.

        Returns:
            Nome do processador, ou ``"desconhecido"``.
        """
        cpuinfo: Path = Path("/proc/cpuinfo")
        if cpuinfo.is_file():
            linha: str
            for linha in cpuinfo.read_text(encoding="utf-8", errors="replace").splitlines():
                if linha.startswith("model name"):
                    return linha.split(":", 1)[1].strip()
        saida: str | None = self._rodar(["sysctl", "-n", "machdep.cpu.brand_string"], 5)
        if saida:
            return saida.strip()
        return platform.processor() or "desconhecido"

    def _memoria(self) -> tuple[float | None, float | None]:
        """Mede a memória RAM total e disponível.

        Returns:
            ``(total_gb, disponível_gb)``; ``None`` no que não puder ser medido.
        """
        meminfo: Path = Path("/proc/meminfo")
        if meminfo.is_file():
            valores: dict[str, float] = {}
            linha: str
            for linha in meminfo.read_text(encoding="utf-8").splitlines():
                partes: list[str] = linha.split()
                if len(partes) >= 2 and partes[1].isdigit():
                    valores[partes[0].rstrip(":")] = int(partes[1]) * 1024 / self.GB
            return valores.get("MemTotal"), valores.get("MemAvailable")
        saida: str | None = self._rodar(["sysctl", "-n", "hw.memsize"], 5)
        if saida and saida.strip().isdigit():
            return int(saida.strip()) / self.GB, None
        return None, None

    def _gpus(self, ram_total: float | None) -> tuple[InfoGPU, ...]:
        """Detecta GPUs NVIDIA (``nvidia-smi``), AMD (``rocm-smi``), Apple Silicon e integradas (``lspci``).

        Args:
            ram_total: RAM total, usada como memória da GPU unificada no Apple Silicon.

        Returns:
            GPUs encontradas.
        """
        gpus: list[InfoGPU] = []
        saida: str | None = self._rodar(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total,memory.free,driver_version",
                "--format=csv,noheader,nounits",
            ],
            10,
        )
        linha: str
        for linha in (saida or "").strip().splitlines():
            campos: list[str] = [campo.strip() for campo in linha.split(",")]
            if len(campos) >= 4:
                gpus.append(
                    InfoGPU(
                        nome=campos[0],
                        fabricante="NVIDIA",
                        tipo="dedicada",
                        vram_total_gb=float(campos[1]) * 1024**2 / self.GB,
                        vram_livre_gb=float(campos[2]) * 1024**2 / self.GB,
                        usavel_para_llm=True,
                        observacao=f"driver {campos[3]}",
                    )
                )
        if self._rodar(["rocm-smi", "--showmeminfo", "vram"], 10):
            gpus.append(InfoGPU("GPU AMD (ROCm)", "AMD", "dedicada", None, None, True, "VRAM não medida"))
        if platform.system() == "Darwin" and platform.machine() == "arm64":
            gpus.append(
                InfoGPU("Apple Silicon", "Apple", "unificada", ram_total, None, True, "memória unificada com a RAM")
            )
        gpus.extend(self._gpus_integradas(gpus))
        return tuple(gpus)

    def _gpus_integradas(self, ja_detectadas: list[InfoGPU]) -> list[InfoGPU]:
        """Lista GPUs integradas via ``lspci`` (só informativo).

        Args:
            ja_detectadas: GPUs já detectadas por outras ferramentas.

        Returns:
            GPUs integradas não listadas antes.
        """
        saida: str | None = self._rodar(["lspci"], 10)
        fabricantes: set[str] = {gpu.fabricante for gpu in ja_detectadas}
        integradas: list[InfoGPU] = []
        linha: str
        for linha in (saida or "").splitlines():
            if not re.search(r"VGA|3D|Display", linha) or "NVIDIA" in linha:
                continue
            nome: str = linha.split(": ", 1)[-1].strip()
            fabricante: str = "AMD" if re.search(r"AMD|ATI", nome) else "Intel" if "Intel" in nome else "outro"
            if fabricante in fabricantes:
                continue
            integradas.append(
                InfoGPU(nome, fabricante, "integrada", None, None, False, "integrada: o Ollama usa a dedicada ou a CPU")
            )
        return integradas

    def _disco_livre(self) -> float | None:
        """Mede o espaço livre onde o Ollama guarda os modelos (ou na pasta pessoal).

        Returns:
            Espaço livre em GB.
        """
        pasta: Path = Path(os.environ.get("OLLAMA_MODELS", Path.home() / ".ollama" / "models"))
        alvo: Path = pasta if pasta.exists() else Path.home()
        try:
            return shutil.disk_usage(alvo).free / self.GB
        except OSError:
            return None

    def _ollama(self) -> InfoOllama:
        """Verifica o servidor Ollama e coleta os metadados dos modelos instalados.

        Returns:
            Situação do Ollama.
        """
        versao: dict[str, object] | None = self._http_json("/api/version", None, 3)
        if versao is None:
            return InfoOllama(shutil.which("ollama") is not None, False, "", ())
        tags: dict[str, object] | None = self._http_json("/api/tags", None, 10)
        lista: object = (tags or {}).get("models", [])
        modelos: list[ModeloLocal] = []
        item: object
        for item in lista if isinstance(lista, list) else []:
            if isinstance(item, dict) and isinstance(item.get("name"), str):
                modelos.append(self._modelo_local(item))
        return InfoOllama(True, True, str(versao.get("version", "")), tuple(modelos))

    def _modelo_local(self, item: dict[str, object]) -> ModeloLocal:
        """Monta um :class:`ModeloLocal` a partir de ``/api/tags`` e ``/api/show``.

        Args:
            item: Entrada de ``/api/tags``.

        Returns:
            Modelo com metadados de memória (conservadores quando faltar dado).
        """
        nome: str = str(item["name"])
        tamanho: object = item.get("size", 0)
        detalhes: dict[str, object] = self._http_json("/api/show", {"model": nome}, 15) or {}
        basicos: object = detalhes.get("details", item.get("details", {}))
        info: object = detalhes.get("model_info", {})
        basicos_dict: dict[str, object] = basicos if isinstance(basicos, dict) else {}
        info_dict: dict[str, object] = info if isinstance(info, dict) else {}
        arquitetura: str = str(info_dict.get("general.architecture", ""))
        capacidades: object = detalhes.get("capabilities", [])
        camadas: int | None = self._inteiro(info_dict.get(f"{arquitetura}.block_count"))
        intervalo: int | None = self._inteiro(info_dict.get(f"{arquitetura}.full_attention_interval"))
        cabecas: int | None = self._inteiro(info_dict.get(f"{arquitetura}.attention.head_count"))
        cabecas_kv: int | None = self._inteiro(info_dict.get(f"{arquitetura}.attention.head_count_kv"))
        chave: int | None = self._inteiro(info_dict.get(f"{arquitetura}.attention.key_length"))
        valor: int | None = self._inteiro(info_dict.get(f"{arquitetura}.attention.value_length"))
        embedding: int | None = self._inteiro(info_dict.get(f"{arquitetura}.embedding_length"))
        completos: bool = cabecas_kv is not None
        if cabecas_kv is None:
            cabecas_kv = cabecas
        dim_kv: int | None = chave + valor if chave is not None and valor is not None else None
        if dim_kv is None and embedding and cabecas:
            dim_kv = 2 * (embedding // cabecas)
        camadas_kv: int | None = camadas // intervalo if camadas and intervalo else camadas
        return ModeloLocal(
            nome=nome,
            tamanho_gb=(tamanho if isinstance(tamanho, (int, float)) else 0) / self.GB,
            parametros_b=self._parametros_b(str(basicos_dict.get("parameter_size", ""))),
            quantizacao=str(basicos_dict.get("quantization_level", "")),
            familia=str(basicos_dict.get("family", arquitetura)),
            contexto_max=self._inteiro(info_dict.get(f"{arquitetura}.context_length")),
            camadas_kv=camadas_kv,
            cabecas_kv=cabecas_kv,
            dim_kv=dim_kv,
            metadados_completos=completos,
            capacidades=tuple(str(c) for c in capacidades) if isinstance(capacidades, list) else (),
        )

    @staticmethod
    def _inteiro(valor: object) -> int | None:
        """Converte metadado em inteiro; listas (valor por camada) viram o maior valor.

        Args:
            valor: Valor bruto do metadado.

        Returns:
            Inteiro, ou ``None`` se ausente ou inválido.
        """
        if isinstance(valor, bool):
            return None
        if isinstance(valor, int):
            return valor
        if isinstance(valor, list):
            inteiros: list[int] = [item for item in valor if isinstance(item, int) and not isinstance(item, bool)]
            return max(inteiros) if inteiros else None
        return None

    def _parametros_b(self, texto: str) -> float | None:
        """Converte ``"4.7B"`` ou ``"500M"`` em bilhões de parâmetros.

        Args:
            texto: Tamanho declarado pelo Ollama.

        Returns:
            Bilhões de parâmetros, ou ``None``.
        """
        correspondencia: re.Match[str] | None = self._RE_PARAMETROS.search(texto)
        if correspondencia is None:
            return None
        numero: float = float(correspondencia.group(1))
        return numero if correspondencia.group(2).upper() == "B" else numero / 1000

    def _cli_claude(self) -> InfoCLI:
        """Verifica a CLI ``claude`` (Claude Code, assinatura).

        Returns:
            Situação da CLI. O login não é verificado aqui (``executar_teste_llm.py`` verifica).
        """
        versao: str | None = self._rodar(["claude", "--version"], 15)
        if versao is None:
            return InfoCLI("claude", False, "", ())
        return InfoCLI("claude", True, versao.strip().split()[0], (), "login não verificado")

    def _cli_codex(self) -> InfoCLI:
        """Verifica a CLI ``codex`` (OpenAI Codex, assinatura do ChatGPT).

        Returns:
            Situação da CLI e se o login foi feito.
        """
        versao: str | None = self._rodar(["codex", "--version"], 15)
        if versao is None:
            return InfoCLI("codex", False, "", ())
        login: str | None = self._rodar(["codex", "login", "status"], 15)
        observacao: str = "login feito" if login is not None and "Logged in" in login else "login não verificado"
        return InfoCLI("codex", True, versao.strip().split()[-1], (), observacao)

    def _cli_agy(self) -> InfoCLI:
        """Verifica a CLI ``agy`` (Antigravity, assinatura) e lista os modelos dela.

        Returns:
            Situação da CLI, com os modelos disponíveis na conta.
        """
        versao: str | None = self._rodar(["agy", "--version"], 15)
        if versao is None:
            return InfoCLI("agy", False, "", ())
        saida: str | None = self._rodar(["agy", "models"], 60)
        modelos: list[tuple[str, str]] = []
        linha: str
        for linha in (saida or "").splitlines():
            if "\t" in linha:
                identificador: str
                nome: str
                identificador, nome = linha.split("\t", 1)
                modelos.append((identificador.strip(), nome.strip()))
        observacao: str = "" if modelos else "não listou modelos (login ou rede)"
        return InfoCLI("agy", True, versao.strip(), tuple(modelos), observacao)
