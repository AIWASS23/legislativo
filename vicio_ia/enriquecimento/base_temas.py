"""Montagem da base de conhecimento dos temas (ADR-020), sem modelo: junta artefatos já revisados.

Entradas: a árvore preparada, os cartões da etapa 1, o mapa de artigos e o dicionário de termos finais (D14)
e a folha-verdade (só os IDs das questões, como exemplos de cada tema). Saída:
``dados/conhecimento/temas.jsonl``, com a proveniência no manifesto.
"""

from __future__ import annotations

import csv
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TextIO

from vicio_ia.configuracao import Caminhos
from vicio_ia.enriquecimento.manifesto import Manifesto
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada
from vicio_ia.sistema.base_temas import ArquivoBaseTemas, ReferenciaTema, TemaBase, TermoTema
from vicio_ia.sistema.folha import LeitorFolha, RotuloFolha
from vicio_ia.sistema.mapa_artigos import LinhaMapa, MapaArtigos
from vicio_ia.temas.cartoes import ArquivoCartoes, CartaoTema


class MontadorBaseTemas:
    """Monta um registro por tema publicável, na ordem da árvore."""

    def __init__(
        self,
        temas: Sequence[TemaPreparado],
        cartoes: Sequence[CartaoTema],
        mapa: Sequence[LinhaMapa],
        termos: Sequence[Mapping[str, str]],
        folha: Sequence[RotuloFolha],
    ) -> None:
        """Indexa as entradas por tema.

        Args:
            temas: Árvore preparada.
            cartoes: Cartões da etapa 1.
            mapa: Linhas do mapa de artigos final.
            termos: Linhas de ``termos.csv`` final.
            folha: Folha-verdade.
        """
        self._temas: list[TemaPreparado] = list(temas)
        self._por_id: dict[str, TemaPreparado] = {t.tema_id: t for t in temas}
        self._cartoes: dict[str, CartaoTema] = {c.tema_id: c for c in cartoes}
        self._mapa: dict[str, list[LinhaMapa]] = {}
        linha: LinhaMapa
        for linha in mapa:
            self._mapa.setdefault(linha.tema_id, []).append(linha)
        self._termos: dict[str, list[TermoTema]] = {}
        bruto: Mapping[str, str]
        for bruto in termos:
            self._termos.setdefault(bruto["tema_id"], []).append(
                TermoTema(
                    termo=bruto["termo"],
                    normalizado=bruto["termo_normalizado"],
                    tipo=bruto["tipo"],
                    alvo=bruto["tema_id_alvo"],
                    revisado=bruto["revisado"] == "sim",
                )
            )
        self._exemplos: dict[str, list[str]] = {}
        rotulo: RotuloFolha
        alvo: str
        for rotulo in folha:
            for alvo in rotulo.alvos:
                self._exemplos.setdefault(alvo, []).append(rotulo.id)

    def montar(self) -> list[TemaBase]:
        """Monta a base.

        Returns:
            Um registro por tema publicável.
        """
        base: list[TemaBase] = []
        tema: TemaPreparado
        for tema in self._temas:
            if not tema.publicavel:
                continue
            cartao: CartaoTema | None = self._cartoes.get(tema.tema_id)
            pai: TemaPreparado | None = self._por_id.get(tema.parent_id or "")
            irmaos: tuple[str, ...] = (
                tuple(i for i in pai.filhos if i != tema.tema_id and self._publicavel(i)) if pai else ()
            )
            base.append(
                TemaBase(
                    tema_id=tema.tema_id,
                    caminho=tema.caminho_exibicao,
                    titulo=tema.titulo_exibicao,
                    nivel=tema.nivel,
                    pai=tema.parent_id or "",
                    irmaos=irmaos,
                    filhos=tuple(f for f in tema.filhos if self._publicavel(f)),
                    escopo=cartao.escopo if cartao else "",
                    inclui=cartao.inclui if cartao else (),
                    nao_inclui=tuple((n.assunto, n.tema_id) for n in cartao.nao_inclui) if cartao else (),
                    ancoras=cartao.ancoras_legais if cartao else (),
                    referencias=tuple(
                        ReferenciaTema(r.lei, r.art_inicio, r.art_fim, r.forca)
                        for r in self._mapa.get(tema.tema_id, [])
                    ),
                    termos=tuple(self._termos.get(tema.tema_id, [])),
                    exemplos_folha=tuple(sorted(set(self._exemplos.get(tema.tema_id, [])))),
                )
            )
        return base

    def _publicavel(self, tema_id: str) -> bool:
        """Diz se um ID é de tema publicável.

        Args:
            tema_id: ID.

        Returns:
            ``True`` se publicável.
        """
        tema: TemaPreparado | None = self._por_id.get(tema_id)
        return tema is not None and tema.publicavel


class PipelineBaseTemas:
    """Monta e grava ``dados/conhecimento/temas.jsonl``."""

    COMANDO: str = "uv run python executar_base_temas.py"

    def __init__(self, caminhos: Caminhos | None = None) -> None:
        """Define a configuração.

        Args:
            caminhos: Caminhos do projeto.
        """
        self._caminhos: Caminhos = caminhos or Caminhos.padrao()

    def executar(self) -> Path:
        """Monta a base, grava e registra a proveniência.

        Returns:
            Caminho da base.
        """
        leitor: LeitorPreparados = LeitorPreparados(self._caminhos)
        temas: list[TemaPreparado] = leitor.temas()
        questoes: list[QuestaoPreparada] = leitor.questoes()
        pasta: Path = self._caminhos.dados_conhecimento
        arquivo_cartoes: Path = self._caminhos.dados_temas / "cartoes.jsonl"
        arquivo_mapa: Path = pasta / "mapa_artigos.csv"
        arquivo_termos: Path = pasta / "termos.csv"
        termos: list[dict[str, str]]
        entrada: TextIO
        with arquivo_termos.open(encoding="utf-8", newline="") as entrada:
            termos = list(csv.DictReader(entrada))
        folha: list[RotuloFolha] = LeitorFolha(self._caminhos.folha_verdade, temas, {q.id for q in questoes}).ler()
        base: list[TemaBase] = MontadorBaseTemas(
            temas, ArquivoCartoes(arquivo_cartoes).ler(), MapaArtigos.ler(arquivo_mapa).todas(), termos, folha
        ).montar()
        destino: Path = ArquivoBaseTemas(pasta / "temas.jsonl").gravar(base)
        raiz: Path = self._caminhos.raiz
        Manifesto(pasta / "manifesto.json", raiz).registrar(
            destino,
            "regra",
            self.COMANDO,
            {
                "entrada": "árvore preparada, cartões, mapa de artigos e termos finais (D14), IDs da folha-verdade",
                **{
                    f"sha256_{nome}": Manifesto.sha256(arquivo)[:12]
                    for nome, arquivo in (
                        ("cartoes", arquivo_cartoes),
                        ("mapa", arquivo_mapa),
                        ("termos", arquivo_termos),
                        ("folha", self._caminhos.folha_verdade),
                    )
                },
                "temas": str(len(base)),
                "modelo": "nenhum",
            },
        )
        tipos: Counter[str] = Counter(t.tipo for b in base for t in b.termos)
        print(
            f"Base de temas: {len(base)} temas; {sum(1 for b in base if b.referencias)} com referência legal; "
            f"termos {dict(sorted(tipos.items()))}; {sum(1 for b in base if b.exemplos_folha)} com exemplo na folha."
            f"\nArquivo: {destino}"
        )
        return destino
