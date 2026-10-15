"""Caderno de revisão dos cartões, ordenado por prioridade (ADR-007)."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from pathlib import Path

from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.temas.arvore_prompt import MaterialArvore
from vicio_ia.temas.cartoes import CartaoTema
from vicio_ia.texto import ProcessadorTexto


class CadernoRevisaoCartoes:
    """Gera ``saidas/cartoes/revisao_cartoes.md``: primeiro as zonas de risco da régua.

    Prioridades:

    1. lixeiras fortes (escopo estrito e regra de quando usar o nó genérico);
    2. nós em grupo de sobreposição (a regra do cartão não pode contrariar a D2);
    3. irmãos com títulos parecidos (a fronteira que a régua pune);
    4. os demais (revisão amostral).
    """

    def __init__(self, processador: ProcessadorTexto, limiar_similaridade: float) -> None:
        """Define o critério de irmãos parecidos.

        Args:
            processador: Normalizador de texto (similaridade de títulos).
            limiar_similaridade: Similaridade mínima entre títulos de irmãos.
        """
        self._processador: ProcessadorTexto = processador
        self._limiar: float = limiar_similaridade

    def prioridades(self, temas: Sequence[TemaPreparado]) -> dict[str, tuple[int, str]]:
        """Calcula a prioridade de revisão de cada nó publicável.

        Args:
            temas: Árvore preparada.

        Returns:
            ``tema_id -> (prioridade 1 a 4, motivo)``.
        """
        por_id: dict[str, TemaPreparado] = {tema.tema_id: tema for tema in temas}
        prioridades: dict[str, tuple[int, str]] = {}
        tema: TemaPreparado
        for tema in temas:
            if not tema.publicavel:
                continue
            if tema.lixeira == "forte":
                prioridades[tema.tema_id] = (1, "lixeira forte")
            elif tema.grupo_sobreposicao:
                prioridades[tema.tema_id] = (2, f"sobreposição ({tema.grupo_sobreposicao})")
            else:
                parecido: str = self._irmao_parecido(tema, por_id)
                prioridades[tema.tema_id] = (3, f"irmão parecido: {parecido}") if parecido else (4, "amostral")
        return prioridades

    def escrever(
        self,
        destino: Path,
        cartoes: Sequence[CartaoTema],
        temas: Sequence[TemaPreparado],
        material: MaterialArvore,
    ) -> Path:
        """Grava o caderno.

        Args:
            destino: Caminho do ``.md``.
            cartoes: Cartões finais.
            temas: Árvore preparada.
            material: Formatador dos cartões.

        Returns:
            Caminho gravado.
        """
        prioridades: dict[str, tuple[int, str]] = self.prioridades(temas)
        por_id: dict[str, TemaPreparado] = {tema.tema_id: tema for tema in temas}
        ordenados: list[CartaoTema] = sorted(
            cartoes, key=lambda c: (prioridades.get(c.tema_id, (4, ""))[0], c.caminho, c.tema_id)
        )
        contagem: dict[int, int] = {}
        cartao: CartaoTema
        for cartao in cartoes:
            nivel: int = prioridades.get(cartao.tema_id, (4, ""))[0]
            contagem[nivel] = contagem.get(nivel, 0) + 1
        linhas: list[str] = [
            "# Revisão dos cartões de tema",
            "",
            (
                f"Gerado em {datetime.now():%d/%m/%Y %H:%M}. {len(cartoes)} cartões; prioridade 1 (lixeiras fortes): "
                f"{contagem.get(1, 0)}, 2 (sobreposições): {contagem.get(2, 0)}, 3 (irmãos parecidos): "
                f"{contagem.get(3, 0)}, 4 (amostral): {contagem.get(4, 0)}."
            ),
            "",
            "Para corrigir um cartão, acrescente uma linha em `dados/temas/cartoes_ajustes.csv`",
            "(`tema_id,campo,valor,motivo`; listas separadas por ` | `; em `nao_inclui`, `assunto -> tema_id`)",
            "e rode `uv run python executar_cartoes.py` de novo (os rascunhos vêm do cache).",
            "",
        ]
        atual: int = 0
        for cartao in ordenados:
            prioridade: int
            motivo: str
            prioridade, motivo = prioridades.get(cartao.tema_id, (4, "amostral"))
            if prioridade != atual:
                atual = prioridade
                linhas.extend([f"## Prioridade {prioridade}", ""])
            linhas.append(f"### {cartao.tema_id} · {motivo}{' · AJUSTADO' if cartao.origem == 'ajustado' else ''}")
            linhas.append("")
            linhas.append("```text")
            linhas.append(material.formatar(cartao))
            linhas.append("```")
            tema: TemaPreparado | None = por_id.get(cartao.tema_id)
            if tema is not None and tema.grupo_sobreposicao:
                linhas.append(f"Regra D2 (decisão manual): {tema.regra_desempate}")
            linhas.append("")
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text("\n".join(linhas), encoding="utf-8")
        return destino

    def _irmao_parecido(self, tema: TemaPreparado, por_id: dict[str, TemaPreparado]) -> str:
        """Procura um irmão publicável com título parecido.

        Args:
            tema: Nó.
            por_id: Árvore indexada.

        Returns:
            ``"ID título"`` do irmão mais parecido acima do limiar, ou ``""``.
        """
        if tema.parent_id is None or tema.parent_id not in por_id:
            return ""
        melhor: tuple[float, str] = (0.0, "")
        irmao_id: str
        for irmao_id in por_id[tema.parent_id].filhos:
            irmao: TemaPreparado | None = por_id.get(irmao_id)
            if irmao is None or irmao.tema_id == tema.tema_id or not irmao.publicavel:
                continue
            similaridade: float = self._processador.similaridade(tema.titulo_exibicao, irmao.titulo_exibicao)
            if similaridade > melhor[0]:
                melhor = (similaridade, f"{irmao.tema_id} {irmao.titulo_exibicao}")
        return melhor[1] if melhor[0] >= self._limiar else ""
