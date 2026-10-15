"""Custo e tempo das chamadas a modelos, por papel e por modelo (ADR-003).

O resumo sai do próprio cache (``runs/``), então é medido, não estimado. Em provedores de
assinatura o custo informado é o equivalente de lista (``claude-cli``) ou não existe
(``gemini-agy``); nos locais, é zero. O que custa nesses casos é o tempo.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import ClassVar, Literal

from vicio_ia.infra.catalogo import CatalogoModelos, ModeloCatalogado
from vicio_ia.llm.cache import RegistroChamada
from vicio_ia.llm.contratos import UsoTokens

type TipoCusto = Literal["pago", "equivalente_de_lista", "assinatura", "local"]
"""Natureza do custo informado."""


class TabelaPrecos:
    """Preços por milhão de tokens, lidos do catálogo de modelos (``config/catalogo_modelos.json``)."""

    FATOR_CACHE_LIDO: ClassVar[float] = 0.1
    FATOR_CACHE_ESCRITO: ClassVar[float] = 1.25

    def __init__(self, modelos: Sequence[ModeloCatalogado]) -> None:
        """Indexa os preços conhecidos.

        Args:
            modelos: Modelos do catálogo.
        """
        self._precos: dict[tuple[str, str], tuple[float, float]] = {
            (modelo.provedor, modelo.modelo): (modelo.preco_entrada, modelo.preco_saida)
            for modelo in modelos
            if modelo.preco_entrada is not None and modelo.preco_saida is not None
        }

    @classmethod
    def do_catalogo(cls, caminho: Path) -> TabelaPrecos:
        """Lê a tabela do arquivo de catálogo.

        Args:
            caminho: ``config/catalogo_modelos.json``.

        Returns:
            Tabela de preços (vazia se o arquivo não existir).
        """
        if not caminho.is_file():
            return cls([])
        return cls(CatalogoModelos(caminho).ler_arquivo())

    def custo(self, provedor: str, modelo: str, uso: UsoTokens) -> float | None:
        """Calcula o custo de uma chamada.

        Args:
            provedor: Provedor.
            modelo: Modelo.
            uso: Tokens consumidos.

        Returns:
            Custo em USD, ou ``None`` se o preço não for conhecido.
        """
        precos: tuple[float, float] | None = self._precos.get((provedor, modelo))
        if precos is None:
            return None
        entrada: float = (
            uso.entrada + uso.cache_lido * self.FATOR_CACHE_LIDO + uso.cache_escrito * self.FATOR_CACHE_ESCRITO
        )
        return (entrada * precos[0] + (uso.saida + uso.raciocinio) * precos[1]) / 1_000_000


@dataclass(frozen=True)
class ResumoUso:
    """Uso agregado de um papel com um modelo.

    Attributes:
        papel: Papel.
        provedor: Provedor.
        modelo: Modelo.
        versoes_prompt: Versões de prompt usadas.
        chamadas: Chamadas feitas (cada uma paga uma vez; as repetidas vêm do cache).
        tokens_entrada: Tokens de entrada, incluindo os servidos pelo cache de prompt.
        tokens_saida: Tokens de saída, incluindo raciocínio.
        latencia_total_s: Soma das latências (tempo sequencial equivalente).
        latencia_media_s: Latência média por chamada.
        custo_usd: Soma dos custos conhecidos (``None`` se nenhum).
        tipo_custo: Natureza do custo.
    """

    papel: str
    provedor: str
    modelo: str
    versoes_prompt: tuple[str, ...]
    chamadas: int
    tokens_entrada: int
    tokens_saida: int
    latencia_total_s: float
    latencia_media_s: float
    custo_usd: float | None
    tipo_custo: TipoCusto


class ContadorCusto:
    """Agrega o cache por papel e modelo e grava ``saidas/custos/resumo_custos.md`` e ``.json``."""

    PROVEDORES_LOCAIS: ClassVar[frozenset[str]] = frozenset({"ollama"})
    PROVEDORES_ASSINATURA: ClassVar[frozenset[str]] = frozenset({"claude-cli", "gemini-agy"})

    def resumir(self, registros: Sequence[RegistroChamada]) -> list[ResumoUso]:
        """Agrega os registros.

        Args:
            registros: Chamadas gravadas no cache.

        Returns:
            Um resumo por (papel, provedor, modelo), ordenado por papel.
        """
        grupos: dict[tuple[str, str, str], list[RegistroChamada]] = {}
        registro: RegistroChamada
        for registro in registros:
            grupos.setdefault((registro.papel, registro.resposta.provedor, registro.resposta.modelo), []).append(
                registro
            )
        resumos: list[ResumoUso] = []
        chave: tuple[str, str, str]
        for chave in sorted(grupos):
            itens: list[RegistroChamada] = grupos[chave]
            custos: list[float] = [item.custo_usd for item in itens if item.custo_usd is not None]
            latencia: float = sum(item.resposta.latencia_s for item in itens)
            resumos.append(
                ResumoUso(
                    papel=chave[0],
                    provedor=chave[1],
                    modelo=chave[2],
                    versoes_prompt=tuple(sorted({item.versao_prompt for item in itens})),
                    chamadas=len(itens),
                    tokens_entrada=sum(
                        item.resposta.uso.entrada + item.resposta.uso.cache_lido + item.resposta.uso.cache_escrito
                        for item in itens
                    ),
                    tokens_saida=sum(item.resposta.uso.saida + item.resposta.uso.raciocinio for item in itens),
                    latencia_total_s=round(latencia, 1),
                    latencia_media_s=round(latencia / len(itens), 2),
                    custo_usd=round(sum(custos), 4) if custos else None,
                    tipo_custo=self._tipo(chave[1]),
                )
            )
        return resumos

    def escrever(self, registros: Sequence[RegistroChamada], pasta: Path) -> Path:
        """Grava o resumo em Markdown e JSON.

        Args:
            registros: Chamadas gravadas no cache.
            pasta: ``saidas/custos/``.

        Returns:
            Caminho do Markdown.
        """
        resumos: list[ResumoUso] = self.resumir(registros)
        pasta.mkdir(parents=True, exist_ok=True)
        (pasta / "resumo_custos.json").write_text(
            json.dumps([asdict(resumo) for resumo in resumos], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        linhas: list[str] = [
            "# Custo e tempo das chamadas a modelos",
            "",
            f"Gerado em {datetime.now():%d/%m/%Y %H:%M} a partir do cache (`runs/`). Cada chamada é paga uma vez;",
            "as repetições vêm do cache e não entram aqui.",
            "",
            "- **pago:** API cobrada por token (preço do catálogo, ou o informado pelo provedor).",
            "- **equivalente_de_lista:** a CLI `claude` informa quanto custaria na API; com assinatura, não é cobrado.",
            "- **assinatura:** CLI sem custo informado; o custo real é a cota e o tempo.",
            "- **local:** modelo na própria máquina; custo zero, só tempo.",
            "",
            "| Papel | Provedor | Modelo | Chamadas | Tokens entrada | Tokens saída | Tempo total | Média | Custo (USD) | Tipo |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---|",
        ]
        resumo: ResumoUso
        for resumo in resumos:
            custo: str = "—" if resumo.custo_usd is None else f"{resumo.custo_usd:.2f}"
            linhas.append(
                f"| {resumo.papel} | {resumo.provedor} | {resumo.modelo} | {resumo.chamadas} | "
                f"{resumo.tokens_entrada:,} | {resumo.tokens_saida:,} | {resumo.latencia_total_s / 60:.1f} min | "
                f"{resumo.latencia_media_s:.1f} s | {custo} | {resumo.tipo_custo} |"
            )
        total_chamadas: int = sum(r.chamadas for r in resumos)
        total_tempo: float = sum(r.latencia_total_s for r in resumos)
        pagos: float = sum(r.custo_usd or 0.0 for r in resumos if r.tipo_custo == "pago")
        lista: float = sum(r.custo_usd or 0.0 for r in resumos if r.tipo_custo == "equivalente_de_lista")
        linhas.extend(
            [
                "",
                (
                    f"**Total:** {total_chamadas} chamadas; {total_tempo / 3600:.2f} h de tempo sequencial equivalente; "
                    f"US$ {pagos:.2f} pagos; US$ {lista:.2f} em equivalente de lista (assinatura)."
                ),
                "",
            ]
        )
        destino: Path = pasta / "resumo_custos.md"
        destino.write_text("\n".join(linhas), encoding="utf-8")
        return destino

    def _tipo(self, provedor: str) -> TipoCusto:
        """Classifica a natureza do custo pelo provedor.

        Args:
            provedor: Nome do provedor.

        Returns:
            Tipo do custo.
        """
        if provedor in self.PROVEDORES_LOCAIS:
            return "local"
        if provedor == "claude-cli":
            return "equivalente_de_lista"
        if provedor in self.PROVEDORES_ASSINATURA:
            return "assinatura"
        return "pago"
