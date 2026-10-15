"""As três versões da árvore para os prompts (ADR-007): enxuta, com escopo e cartões por ramo.

Todas têm bytes estáveis (mesma ordem e mesmo texto a cada execução), para que o cache de
chamadas e o cache de prompt das APIs funcionem.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import ClassVar

from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.temas.cartoes import CartaoTema


@dataclass(frozen=True)
class TamanhoMaterial:
    """Tamanho de uma versão do material.

    Attributes:
        nome: Nome da versão.
        bytes: Tamanho em bytes (UTF-8).
        tokens: Tokens estimados.
    """

    nome: str
    bytes: int
    tokens: int


class MaterialArvore:
    """Gera os recortes da árvore e dos cartões usados por cada papel (ADR-008)."""

    LEGENDA_ESCOPO: ClassVar[str] = (
        "Temas em que a questão pode ser classificada (ID | caminho :: escopo). "
        "[conceitual] = use só se a questão for sobre o conceito geral do tema, não sobre um instituto específico."
    )
    MARCA_CONCEITUAL: ClassVar[str] = " [conceitual]"

    def __init__(self, temas: Sequence[TemaPreparado], cartoes: Sequence[CartaoTema], arvore_enxuta: str) -> None:
        """Indexa temas e cartões.

        Args:
            temas: Árvore preparada.
            cartoes: Cartões finais (um por tema publicável).
            arvore_enxuta: Árvore enxuta do passo 01.
        """
        self._temas: dict[str, TemaPreparado] = {tema.tema_id: tema for tema in temas}
        self._cartoes: dict[str, CartaoTema] = {cartao.tema_id: cartao for cartao in cartoes}
        self._enxuta: str = arvore_enxuta
        self._ordem: list[TemaPreparado] = sorted(
            (tema for tema in temas if tema.publicavel), key=lambda t: (t.caminho_exibicao, t.tema_id)
        )

    @property
    def enxuta(self) -> str:
        """Árvore enxuta (``ID | caminho``), para o voto barato."""
        return self._enxuta

    def com_escopo(self) -> str:
        """Árvore com o escopo de cada nó, para o classificador A.

        Returns:
            Texto com legenda e uma linha por nó publicável.
        """
        linhas: list[str] = [self.LEGENDA_ESCOPO]
        linhas.extend(self._linha_escopo(tema) for tema in self._ordem)
        return "\n".join(linhas) + "\n"

    def nivel1_com_escopo(self) -> str:
        """Só os temas de nível 1, com escopo e a lista de subtemas, para a 1ª etapa do classificador B.

        Returns:
            Texto com legenda e uma linha por tema de nível 1.
        """
        linhas: list[str] = [self.LEGENDA_ESCOPO]
        tema: TemaPreparado
        for tema in self._ordem:
            if tema.nivel != 1:
                continue
            subtemas: list[str] = [
                self._temas[i].titulo_exibicao for i in tema.filhos if i in self._temas and self._temas[i].publicavel
            ]
            sufixo: str = f" (subtemas: {'; '.join(subtemas)})" if subtemas else ""
            linhas.append(self._linha_escopo(tema) + sufixo)
        return "\n".join(linhas) + "\n"

    def nivel1_sem_escopo(self) -> str:
        """Só os temas de nível 1, com a lista de subtemas e sem escopo (experimento E4).

        Returns:
            Texto com uma linha por tema de nível 1.
        """
        linhas: list[str] = ["Temas em que a questão pode ser classificada (ID | caminho)."]
        tema: TemaPreparado
        for tema in self._ordem:
            if tema.nivel != 1:
                continue
            subtemas: list[str] = [
                self._temas[i].titulo_exibicao for i in tema.filhos if i in self._temas and self._temas[i].publicavel
            ]
            marca: str = self.MARCA_CONCEITUAL if tema.lixeira == "forte" else ""
            sufixo: str = f" (subtemas: {'; '.join(subtemas)})" if subtemas else ""
            linhas.append(f"{tema.tema_id} | {tema.caminho_exibicao}{marca}{sufixo}")
        return "\n".join(linhas) + "\n"

    def filhos_sem_cartoes(self, tema_id: str) -> str:
        """O tema e os filhos publicáveis só com ID e caminho (experimento E4).

        Args:
            tema_id: Tema de nível 1.

        Returns:
            Uma linha por nó.
        """
        tema: TemaPreparado = self._temas[tema_id]
        ids: list[str] = [tema_id, *(i for i in tema.filhos if i in self._temas and self._temas[i].publicavel)]
        return "\n".join(f"[{i}] {self._temas[i].caminho_exibicao}" for i in ids) + "\n"

    def cartoes_filhos(self, tema_id: str) -> str:
        """Cartões do tema e dos filhos publicáveis, para a 2ª etapa do classificador B.

        Args:
            tema_id: Tema de nível 1 escolhido na 1ª etapa.

        Returns:
            Cartões formatados (o do tema primeiro).
        """
        tema: TemaPreparado = self._temas[tema_id]
        ids: list[str] = [tema_id, *(i for i in tema.filhos if i in self._cartoes)]
        return "\n\n".join(self.formatar(self._cartoes[i]) for i in ids if i in self._cartoes) + "\n"

    def cartoes_ramo(self, tema_id: str, extras: Sequence[str]) -> str:
        """Cartões do candidato, do pai, dos irmãos e dos filhos, para o verificador.

        Args:
            tema_id: Nó candidato.
            extras: Outros nós a incluir (ex.: segundo colocado e par de sobreposição).

        Returns:
            Cartões formatados, sem repetição, na ordem da árvore.
        """
        tema: TemaPreparado = self._temas[tema_id]
        ids: set[str] = {tema_id, *tema.filhos, *extras}
        if tema.parent_id is not None and tema.parent_id in self._temas:
            pai: TemaPreparado = self._temas[tema.parent_id]
            ids.update(pai.filhos)
            if pai.publicavel:
                ids.add(pai.tema_id)
        ordenados: list[TemaPreparado] = [t for t in self._ordem if t.tema_id in ids and t.tema_id in self._cartoes]
        return "\n\n".join(self.formatar(self._cartoes[t.tema_id]) for t in ordenados) + "\n"

    def formatar(self, cartao: CartaoTema) -> str:
        """Formata um cartão para o prompt.

        Args:
            cartao: Cartão.

        Returns:
            Texto do cartão.
        """
        tema: TemaPreparado | None = self._temas.get(cartao.tema_id)
        marca: str = self.MARCA_CONCEITUAL if tema is not None and tema.lixeira == "forte" else ""
        linhas: list[str] = [f"[{cartao.tema_id}] {cartao.caminho}{marca}", f"Escopo: {cartao.escopo}"]
        if cartao.inclui:
            linhas.append("Inclui: " + "; ".join(cartao.inclui))
        if cartao.nao_inclui:
            linhas.append("Não inclui: " + "; ".join(f"{item.assunto} → {item.tema_id}" for item in cartao.nao_inclui))
        if cartao.ancoras_legais:
            linhas.append("Âncoras legais: " + "; ".join(cartao.ancoras_legais))
        if cartao.regra_desempate:
            linhas.append(f"Desempate: {cartao.regra_desempate}")
        return "\n".join(linhas)

    def tamanhos(self, chars_por_token: float) -> list[TamanhoMaterial]:
        """Mede cada versão do material.

        Args:
            chars_por_token: Caracteres por token usados na estimativa.

        Returns:
            Tamanhos: enxuta, com escopo, nível 1 com escopo e o maior ramo e o maior bloco de filhos.
        """
        ramos: list[str] = [self.cartoes_ramo(t.tema_id, ()) for t in self._ordem]
        filhos: list[str] = [self.cartoes_filhos(t.tema_id) for t in self._ordem if t.nivel == 1]
        versoes: list[tuple[str, str]] = [
            ("árvore enxuta (voto barato)", self._enxuta),
            ("árvore com escopo (classificador A)", self.com_escopo()),
            ("nível 1 com escopo (classificador B, etapa 1)", self.nivel1_com_escopo()),
            ("maior bloco de cartões dos filhos (classificador B, etapa 2)", max(filhos, key=len, default="")),
            ("maior ramo de cartões (verificador)", max(ramos, key=len, default="")),
        ]
        return [
            TamanhoMaterial(nome, len(texto.encode("utf-8")), round(len(texto) / chars_por_token))
            for nome, texto in versoes
        ]

    def _linha_escopo(self, tema: TemaPreparado) -> str:
        """Formata a linha de um nó na árvore com escopo.

        Args:
            tema: Nó publicável.

        Returns:
            ``ID | caminho [conceitual] :: escopo``.
        """
        marca: str = self.MARCA_CONCEITUAL if tema.lixeira == "forte" else ""
        cartao: CartaoTema | None = self._cartoes.get(tema.tema_id)
        escopo: str = f" :: {cartao.escopo}" if cartao is not None else ""
        return f"{tema.tema_id} | {tema.caminho_exibicao}{marca}{escopo}"
