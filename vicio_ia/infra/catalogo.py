"""Catálogo de modelos candidatos: arquivo editável + modelos descobertos na máquina."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, replace
from pathlib import Path
from typing import ClassVar, Literal

from vicio_ia.infra.perfil import InfoCLI, ModeloLocal, PerfilMaquina

type TipoAcesso = Literal["local", "api", "assinatura"]
"""Como o modelo é acessado: rodando na máquina, por API paga ou por CLI de assinatura."""

type OrigemModelo = Literal["catalogo", "descoberto"]
"""``catalogo`` (veio do arquivo) ou ``descoberto`` (Ollama instalado ou listado por CLI)."""


class ErroCatalogo(Exception):
    """Erro no arquivo de catálogo de modelos."""


@dataclass(frozen=True)
class ModeloCatalogado:
    """Um modelo candidato, com o que é preciso para avaliá-lo.

    Attributes:
        provedor: Nome do provedor (``ollama``, ``claude-api``, ``claude-cli``, ``gemini-agy``,
            ``openai``, ``huggingface``).
        modelo: Identificador do modelo no provedor.
        familia: Família (``claude``, ``gemini``, ``qwen``...), usada para diversificar o ensemble.
        acesso: Local, API ou assinatura.
        qualidade: Nota estimada de 1 a 5 para a tarefa.
        contexto_max: Contexto máximo em tokens (``None`` se desconhecido).
        saida_estruturada: Suporta saída em JSON Schema.
        preco_entrada: USD por milhão de tokens de entrada (``None`` se não se aplica).
        preco_saida: USD por milhão de tokens de saída.
        tamanho_gb: Tamanho do arquivo (modelos locais).
        parametros_b: Bilhões de parâmetros (modelos locais).
        camadas_kv: Camadas com cache de atenção (modelos locais).
        cabecas_kv: Cabeças de chave/valor (modelos locais).
        dim_kv: Dimensão de chave + valor por cabeça (modelos locais).
        instalado: Já está disponível na máquina (modelos locais).
        metadados_completos: ``False`` quando a memória foi estimada sem todos os metadados.
        origem: Catálogo ou descoberto.
        verificar: Nome ou disponibilidade ainda não confirmados.
        inadequado: Modelo inadequado para a tarefa (ex.: especializado em código); nunca é escolhido.
        ajuste_velocidade: Correção da nota de velocidade (-2 a +2), ex.: variantes de esforço alto são mais lentas.
        observacao: Nota livre.
    """

    provedor: str
    modelo: str
    familia: str
    acesso: TipoAcesso
    qualidade: int
    contexto_max: int | None
    saida_estruturada: bool
    preco_entrada: float | None
    preco_saida: float | None
    tamanho_gb: float | None
    parametros_b: float | None
    camadas_kv: int | None
    cabecas_kv: int | None
    dim_kv: int | None
    instalado: bool
    metadados_completos: bool
    origem: OrigemModelo
    verificar: bool
    inadequado: bool
    ajuste_velocidade: int
    observacao: str

    @property
    def chave(self) -> str:
        """Identificador único ``provedor:modelo``."""
        return f"{self.provedor}:{self.modelo}"


class CatalogoModelos:
    """Monta a lista de modelos candidatos para a máquina analisada."""

    ACESSO_POR_PROVEDOR: ClassVar[dict[str, TipoAcesso]] = {
        "ollama": "local",
        "claude-api": "api",
        "openai": "api",
        "huggingface": "api",
        "claude-cli": "assinatura",
        "gemini-agy": "assinatura",
    }
    _RE_CODIGO: ClassVar[re.Pattern[str]] = re.compile(r"code|coder|starcoder", re.IGNORECASE)

    def __init__(self, arquivo: Path) -> None:
        """Define o arquivo de catálogo.

        Args:
            arquivo: ``config/catalogo_modelos.json``.
        """
        self._arquivo: Path = arquivo

    def montar(self, perfil: PerfilMaquina) -> list[ModeloCatalogado]:
        """Junta o arquivo de catálogo com os modelos descobertos na máquina.

        Modelos instalados no Ollama substituem a entrada do catálogo de mesmo nome,
        com os metadados reais. Modelos listados pela CLI ``agy`` entram como ``gemini-agy``.

        Args:
            perfil: Perfil da máquina.

        Returns:
            Modelos candidatos, sem repetição.
        """
        modelos: dict[str, ModeloCatalogado] = {modelo.chave: modelo for modelo in self.ler_arquivo()}
        local: ModeloLocal
        for local in perfil.ollama.modelos:
            descoberto: ModeloCatalogado = self._de_ollama(local, modelos.get(f"ollama:{local.nome}"))
            modelos[descoberto.chave] = descoberto
        agy: InfoCLI | None = perfil.cli("agy")
        identificador: str
        nome: str
        for identificador, nome in agy.modelos if agy is not None else ():
            candidato: ModeloCatalogado = self._de_agy(identificador, nome)
            modelos.setdefault(candidato.chave, candidato)
        return list(modelos.values())

    def ler_arquivo(self) -> list[ModeloCatalogado]:
        """Lê e valida ``config/catalogo_modelos.json``.

        Returns:
            Modelos do arquivo.

        Raises:
            ErroCatalogo: Se o arquivo não existir ou tiver entradas inválidas.
        """
        if not self._arquivo.is_file():
            raise ErroCatalogo(f"catálogo não encontrado: {self._arquivo}")
        conteudo: object = json.loads(self._arquivo.read_text(encoding="utf-8"))
        entradas: object = conteudo.get("modelos") if isinstance(conteudo, dict) else None
        if not isinstance(entradas, list):
            raise ErroCatalogo("o catálogo precisa de uma lista 'modelos'")
        modelos: list[ModeloCatalogado] = []
        posicao: int
        entrada: object
        for posicao, entrada in enumerate(entradas, start=1):
            if not isinstance(entrada, dict):
                raise ErroCatalogo(f"entrada {posicao} do catálogo não é um objeto")
            modelos.append(self._de_entrada(entrada, posicao))
        return modelos

    def _de_entrada(self, entrada: dict[str, object], posicao: int) -> ModeloCatalogado:
        """Converte uma entrada do arquivo em :class:`ModeloCatalogado`.

        Args:
            entrada: Objeto JSON da entrada.
            posicao: Posição no arquivo (para mensagens de erro).

        Returns:
            Modelo validado.

        Raises:
            ErroCatalogo: Se faltar campo obrigatório ou o provedor for desconhecido.
        """
        provedor: object = entrada.get("provedor")
        modelo: object = entrada.get("modelo")
        qualidade: object = entrada.get("qualidade")
        if not isinstance(provedor, str) or provedor not in self.ACESSO_POR_PROVEDOR:
            raise ErroCatalogo(f"entrada {posicao}: provedor inválido {provedor!r}")
        if not isinstance(modelo, str) or not modelo:
            raise ErroCatalogo(f"entrada {posicao}: campo 'modelo' obrigatório")
        if not isinstance(qualidade, int) or not 1 <= qualidade <= 5:
            raise ErroCatalogo(f"entrada {posicao}: 'qualidade' deve ser inteiro de 1 a 5")
        return ModeloCatalogado(
            provedor=provedor,
            modelo=modelo,
            familia=str(entrada.get("familia", "")) or modelo.split(":")[0],
            acesso=self.ACESSO_POR_PROVEDOR[provedor],
            qualidade=qualidade,
            contexto_max=self._inteiro(entrada.get("contexto_max")),
            saida_estruturada=bool(entrada.get("saida_estruturada", True)),
            preco_entrada=self._numero(entrada.get("preco_entrada")),
            preco_saida=self._numero(entrada.get("preco_saida")),
            tamanho_gb=self._numero(entrada.get("tamanho_gb")),
            parametros_b=self._numero(entrada.get("parametros_b")),
            camadas_kv=self._inteiro(entrada.get("camadas_kv")),
            cabecas_kv=self._inteiro(entrada.get("cabecas_kv")),
            dim_kv=self._inteiro(entrada.get("dim_kv")),
            instalado=False,
            metadados_completos=True,
            origem="catalogo",
            verificar=bool(entrada.get("verificar", False)),
            inadequado=bool(entrada.get("inadequado", False)),
            ajuste_velocidade=self._inteiro(entrada.get("ajuste_velocidade")) or 0,
            observacao=str(entrada.get("observacao", "")),
        )

    def _de_ollama(self, local: ModeloLocal, do_catalogo: ModeloCatalogado | None) -> ModeloCatalogado:
        """Converte um modelo instalado no Ollama, preservando a nota do catálogo se houver.

        Args:
            local: Modelo instalado.
            do_catalogo: Entrada do catálogo com o mesmo nome, se existir.

        Returns:
            Modelo com metadados reais e ``instalado=True``.
        """
        codigo: bool = self._RE_CODIGO.search(local.nome) is not None
        qualidade: int = do_catalogo.qualidade if do_catalogo else self._qualidade_por_tamanho(local.parametros_b)
        observacao: str = do_catalogo.observacao if do_catalogo else ""
        if codigo:
            qualidade = 1
            observacao = "modelo especializado em código: inadequado para texto jurídico"
        base: ModeloCatalogado = do_catalogo or ModeloCatalogado(
            provedor="ollama",
            modelo=local.nome,
            familia=local.familia,
            acesso="local",
            qualidade=qualidade,
            contexto_max=None,
            saida_estruturada=True,
            preco_entrada=None,
            preco_saida=None,
            tamanho_gb=None,
            parametros_b=None,
            camadas_kv=None,
            cabecas_kv=None,
            dim_kv=None,
            instalado=True,
            metadados_completos=True,
            origem="descoberto",
            verificar=False,
            inadequado=codigo,
            ajuste_velocidade=0,
            observacao=observacao,
        )
        return replace(
            base,
            familia=local.familia or base.familia,
            qualidade=qualidade,
            contexto_max=local.contexto_max or base.contexto_max,
            tamanho_gb=local.tamanho_gb,
            parametros_b=local.parametros_b or base.parametros_b,
            camadas_kv=local.camadas_kv or base.camadas_kv,
            cabecas_kv=local.cabecas_kv or base.cabecas_kv,
            dim_kv=local.dim_kv or base.dim_kv,
            instalado=True,
            metadados_completos=local.metadados_completos,
            verificar=False,
            inadequado=codigo,
            observacao=observacao,
        )

    def _de_agy(self, identificador: str, nome: str) -> ModeloCatalogado:
        """Cria a entrada de um modelo listado pela CLI ``agy``.

        Args:
            identificador: ID usado em ``--model`` (``gemini-3.8-flash-low``).
            nome: Nome exibido pela CLI.

        Returns:
            Modelo de acesso por assinatura.
        """
        minusculo: str = identificador.lower()
        familia: str = next((f for f in ("gemini", "claude", "gpt") if f in minusculo), minusculo.split("-")[0])
        contexto: int = 131072 if "gpt-oss" in minusculo else 1_000_000
        return ModeloCatalogado(
            provedor="gemini-agy",
            modelo=identificador,
            familia=familia,
            acesso="assinatura",
            qualidade=self._qualidade_por_nome(minusculo),
            contexto_max=contexto,
            saida_estruturada=True,
            preco_entrada=None,
            preco_saida=None,
            tamanho_gb=None,
            parametros_b=None,
            camadas_kv=None,
            cabecas_kv=None,
            dim_kv=None,
            instalado=True,
            metadados_completos=True,
            origem="descoberto",
            verificar=False,
            inadequado=False,
            ajuste_velocidade=self._ajuste_por_esforco(minusculo),
            observacao=f"Via CLI agy ({nome}); contexto estimado.",
        )

    @staticmethod
    def _ajuste_por_esforco(nome: str) -> int:
        """Ajusta a velocidade pelo sufixo de esforço dos modelos do ``agy``.

        Medido em 14/10/2026 numa questão trivial: ``gemini-3.8-flash-high`` ~270 s e 66 mil tokens
        de entrada; variantes ``-low`` de 4 a 30 s, com ~13 a 40 mil tokens (o agente acrescenta o
        próprio prompt). A CLI ``claude`` levou ~4,5 s com 1,2 mil tokens.

        Args:
            nome: Identificador em minúsculas.

        Returns:
            0 para ``-low``, -1 para ``-medium``, -2 para ``-high``; -1 sem sufixo.
        """
        if nome.endswith("-low"):
            return 0
        if nome.endswith("-high"):
            return -2
        return -1

    @staticmethod
    def _qualidade_por_nome(nome: str) -> int:
        """Estima a qualidade de um modelo de assinatura pelo nome.

        Args:
            nome: Identificador em minúsculas.

        Returns:
            Nota de 1 a 5 (estimativa).
        """
        regras: tuple[tuple[str, int], ...] = (
            ("opus", 5),
            ("pro", 5),
            ("sonnet", 4),
            ("flash", 4),
            ("gpt-oss-120b", 4),
            ("haiku", 3),
            ("gpt-oss-20b", 3),
        )
        trecho: str
        nota: int
        for trecho, nota in regras:
            if trecho in nome:
                return nota
        return 3

    @staticmethod
    def _qualidade_por_tamanho(parametros_b: float | None) -> int:
        """Estima a qualidade de um modelo local pelo número de parâmetros.

        Args:
            parametros_b: Bilhões de parâmetros.

        Returns:
            Nota de 1 a 5 (estimativa).
        """
        if parametros_b is None or parametros_b < 6:
            return 1
        if parametros_b < 15:
            return 2
        if parametros_b < 40:
            return 3
        return 4

    @staticmethod
    def _inteiro(valor: object) -> int | None:
        """Lê um inteiro opcional do JSON.

        Args:
            valor: Valor bruto.

        Returns:
            Inteiro ou ``None``.
        """
        return valor if isinstance(valor, int) and not isinstance(valor, bool) else None

    @staticmethod
    def _numero(valor: object) -> float | None:
        """Lê um número opcional do JSON.

        Args:
            valor: Valor bruto.

        Returns:
            Número ou ``None``.
        """
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            return None
        return float(valor)
