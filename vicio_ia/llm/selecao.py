"""Resolução do modelo de cada papel: escolha manual em arquivo ou sugestão automática pela infraestrutura."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal

from vicio_ia.configuracao import Caminhos, ParametrosLLM
from vicio_ia.infra.pipeline import PipelineInfra, ResultadoInfra
from vicio_ia.infra.recomendador import AvaliacaoModelo
from vicio_ia.llm.contratos import ErroProvedor
from vicio_ia.llm.fabrica import FabricaProvedores

type OrigemEscolha = Literal["manual", "auto"]
"""``manual`` (definida em ``config/escolha_modelos.json``) ou ``auto`` (sugerida pelo recomendador)."""


@dataclass(frozen=True)
class EscolhaPapel:
    """Modelo resolvido para um papel do ensemble.

    Attributes:
        papel: Nome do papel (``classificador_a``...).
        provedor: Provedor escolhido.
        modelo: Modelo escolhido.
        origem: Manual ou automática.
    """

    papel: str
    provedor: str
    modelo: str
    origem: OrigemEscolha


class ArquivoEscolha:
    """Lê e grava ``config/escolha_modelos.json``.

    Formato::

        {"modo": "manual",
         "papeis": {"classificador_a": {"provedor": "claude-cli", "modelo": "claude-opus-5-5"}, ...}}

    Com ``"modo": "auto"`` (ou sem o arquivo), todos os papéis vêm do recomendador. No modo
    manual, papéis ausentes também vêm do recomendador.
    """

    def __init__(self, caminho: Path) -> None:
        """Define o arquivo.

        Args:
            caminho: Caminho do JSON de escolha.
        """
        self._caminho: Path = caminho

    def ler(self) -> tuple[str, dict[str, tuple[str, str]]]:
        """Lê o modo e as escolhas manuais.

        Returns:
            ``(modo, papel -> (provedor, modelo))``; ``("auto", {})`` se o arquivo não existir.

        Raises:
            ErroProvedor: Se o arquivo estiver malformado.
        """
        if not self._caminho.is_file():
            return "auto", {}
        try:
            conteudo: object = json.loads(self._caminho.read_text(encoding="utf-8"))
        except ValueError as erro:
            raise ErroProvedor(f"{self._caminho.name}: JSON inválido ({erro})") from erro
        if not isinstance(conteudo, dict):
            raise ErroProvedor(f"{self._caminho.name}: esperado um objeto JSON")
        modo: str = str(conteudo.get("modo", "auto"))
        if modo not in ("auto", "manual"):
            raise ErroProvedor(f"{self._caminho.name}: 'modo' deve ser 'auto' ou 'manual'")
        papeis: object = conteudo.get("papeis", {})
        escolhas: dict[str, tuple[str, str]] = {}
        papel: object
        valor: object
        for papel, valor in papeis.items() if isinstance(papeis, dict) else []:
            if (
                isinstance(valor, dict)
                and isinstance(valor.get("provedor"), str)
                and isinstance(valor.get("modelo"), str)
            ):
                escolhas[str(papel)] = (str(valor["provedor"]), str(valor["modelo"]))
        return modo, escolhas

    def gravar(self, modo: str, papeis: Mapping[str, tuple[str, str]]) -> None:
        """Grava o arquivo de escolha.

        Args:
            modo: ``auto`` ou ``manual``.
            papeis: ``papel -> (provedor, modelo)`` (ignorado no modo ``auto``).
        """
        self._caminho.parent.mkdir(parents=True, exist_ok=True)
        conteudo: dict[str, object] = {
            "modo": modo,
            "papeis": {papel: {"provedor": p, "modelo": m} for papel, (p, m) in papeis.items()},
            "atualizado_em": datetime.now().isoformat(timespec="seconds"),
        }
        self._caminho.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class SeletorModelos:
    """Decide o provedor e o modelo de cada papel, respeitando a escolha manual quando houver."""

    def __init__(self, caminhos: Caminhos | None = None, parametros: ParametrosLLM | None = None) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto (opcional).
            parametros: Parâmetros de LLM (opcional).
        """
        self._caminhos: Caminhos = caminhos if caminhos is not None else Caminhos.padrao()
        self._parametros: ParametrosLLM = parametros if parametros is not None else ParametrosLLM()

    def resolver(self) -> dict[str, EscolhaPapel]:
        """Resolve todos os papéis e grava ``saidas/infra/escolha_resolvida.json``.

        Returns:
            ``papel -> escolha``; papéis sem modelo pronto ficam de fora.

        Raises:
            ErroProvedor: Se uma escolha manual usar um provedor desconhecido.
        """
        modo: str
        manuais: dict[str, tuple[str, str]]
        modo, manuais = ArquivoEscolha(self._caminhos.escolha_modelos).ler()
        if modo == "auto":
            manuais = {}
        provedor: str
        modelo: str
        for provedor, modelo in manuais.values():
            if provedor not in FabricaProvedores.NOMES:
                raise ErroProvedor(f"escolha manual com provedor desconhecido: {provedor!r} ({modelo})")
        escolhas: dict[str, EscolhaPapel] = {}
        faltantes: list[str] = [papel for papel in self._parametros.papeis if papel not in manuais]
        if faltantes:
            resultado: ResultadoInfra = PipelineInfra(self._caminhos, self._parametros).analisar()
            papel: str
            for papel in faltantes:
                avaliacao: AvaliacaoModelo | None = resultado.recomendacao.papeis.get(papel)
                if avaliacao is not None:
                    escolhas[papel] = EscolhaPapel(papel, avaliacao.modelo.provedor, avaliacao.modelo.modelo, "auto")
        for papel, (provedor, modelo) in manuais.items():
            escolhas[papel] = EscolhaPapel(papel, provedor, modelo, "manual")
        ordenadas: dict[str, EscolhaPapel] = {p: escolhas[p] for p in self._parametros.papeis if p in escolhas}
        self._gravar_resolvida(ordenadas)
        return ordenadas

    def _gravar_resolvida(self, escolhas: dict[str, EscolhaPapel]) -> None:
        """Registra a escolha resolvida, para rastrear quais modelos geraram os resultados.

        Args:
            escolhas: Escolhas por papel.
        """
        destino: Path = self._caminhos.saida_infra / "escolha_resolvida.json"
        destino.parent.mkdir(parents=True, exist_ok=True)
        conteudo: dict[str, object] = {
            "resolvido_em": datetime.now().isoformat(timespec="seconds"),
            "papeis": {papel: asdict(escolha) for papel, escolha in escolhas.items()},
        }
        destino.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
