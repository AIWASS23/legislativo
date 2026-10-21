"""Documentos de tema e textos das questões para a recuperação (ADR-020, ADR-021).

Enquanto a base de conhecimento revisada da ADR-020 não existe, o documento de cada tema publicável
junta o título e o caminho da árvore (com os títulos corrigidos da D4) e, opcionalmente, o cartão da
etapa 1 (escopo, o que entra e as âncoras legais). O que **não** entra no tema (``nao_inclui``) e a regra
de desempate ficam fora do documento, porque falam de outros temas e confundiriam a busca.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada
from vicio_ia.sistema.base_temas import TemaBase
from vicio_ia.temas.cartoes import CartaoTema


@dataclass(frozen=True)
class DocumentoTema:
    """Texto de busca de um tema publicável.

    Attributes:
        tema_id: ID do tema.
        texto: Texto usado na indexação.
    """

    tema_id: str
    texto: str


class MontadorDocumentos:
    """Monta os documentos dos temas publicáveis e o texto de busca das questões."""

    def __init__(self, temas: Sequence[TemaPreparado], cartoes: Sequence[CartaoTema]) -> None:
        """Guarda a árvore e os cartões.

        Args:
            temas: Árvore preparada.
            cartoes: Cartões da etapa 1 (rascunhos de LLM, permitidos como descrição enriquecida; ADR-020).
        """
        self._temas: list[TemaPreparado] = [t for t in temas if t.publicavel]
        self._cartoes: dict[str, CartaoTema] = {c.tema_id: c for c in cartoes}

    def documentos(self, com_cartao: bool) -> list[DocumentoTema]:
        """Documentos dos temas publicáveis, na ordem da árvore.

        Args:
            com_cartao: Inclui escopo, itens do que entra e âncoras legais do cartão.

        Returns:
            Um documento por tema publicável.
        """
        documentos: list[DocumentoTema] = []
        tema: TemaPreparado
        for tema in self._temas:
            partes: list[str] = [tema.titulo_exibicao, tema.caminho_exibicao]
            cartao: CartaoTema | None = self._cartoes.get(tema.tema_id)
            if com_cartao and cartao is not None:
                partes.extend([cartao.escopo, *cartao.inclui, *cartao.ancoras_legais])
            documentos.append(DocumentoTema(tema.tema_id, "\n".join(p for p in partes if p)))
        return documentos

    @staticmethod
    def documentos_base(base: Sequence[TemaBase], variante: str) -> list[DocumentoTema]:
        """Documentos dos temas a partir da base de conhecimento (ADR-020), na ordem da base.

        Args:
            base: Registros de ``dados/conhecimento/temas.jsonl``.
            variante: ``cartao``, ``cartao_termos`` ou ``cartao_termos_leis`` (E7b, E8b).

        Returns:
            Um documento por tema.
        """
        return [DocumentoTema(t.tema_id, t.texto(variante)) for t in base]

    @staticmethod
    def texto_questao(questao: QuestaoPreparada) -> str:
        """Texto de busca da questão: enunciado, comando e alternativas, sem o cabeçalho do texto canônico.

        Args:
            questao: Questão preparada.

        Returns:
            Texto de busca.
        """
        return "\n".join([questao.enunciado, questao.comando, *questao.alternativas.values()])

    @staticmethod
    def textos_alternativas(questao: QuestaoPreparada) -> Mapping[str, str]:
        """Texto de cada alternativa, para medir a dispersão entre elas (ADR-023).

        Args:
            questao: Questão preparada.

        Returns:
            ``letra -> texto``; vazio em certo/errado, cujas alternativas não têm conteúdo.
        """
        if questao.formato == "certo_errado":
            return {}
        return dict(questao.alternativas)
