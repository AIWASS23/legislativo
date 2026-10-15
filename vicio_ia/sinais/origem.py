"""Assunto de origem -> nós da árvore (sinal fraco, ADR-006): baseline E0 e variável da calibração."""

from __future__ import annotations

from collections.abc import Sequence

from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada
from vicio_ia.texto import ProcessadorTexto


class SinalOrigem:
    """Casa o assunto de origem com títulos da árvore, como a EDA (seção do assunto × árvore).

    Cada parte separada por vírgula é procurada primeiro com o marcador "(Parte N)" e, se não
    bater, sem ele. Fantasmas viram o canônico (D1); só nós publicáveis são devolvidos. O
    assunto de origem nunca entra no prompt dos modelos (ADR-004).
    """

    def __init__(self, temas: Sequence[TemaPreparado], processador: ProcessadorTexto) -> None:
        """Indexa os títulos originais dos nós abaixo das disciplinas.

        Args:
            temas: Árvore preparada.
            processador: Normalizador de texto.
        """
        self._processador: ProcessadorTexto = processador
        self._temas: dict[str, TemaPreparado] = {tema.tema_id: tema for tema in temas}
        self._indice: dict[str, list[str]] = {}
        tema: TemaPreparado
        for tema in temas:
            if tema.nivel > 0:
                chave: str = processador.chave_comparacao(tema.titulo, manter_parte=True)
                self._indice.setdefault(chave, []).append(tema.tema_id)

    def temas(self, questao: QuestaoPreparada) -> tuple[str, ...]:
        """Nós publicáveis que casam com o assunto de origem.

        Args:
            questao: Questão preparada (o assunto de origem está nos campos originais).

        Returns:
            IDs publicáveis, sem repetição.
        """
        assunto: str = str(questao.original.get("assunto_origem", "") or "")
        achados: list[str] = []
        pedaco: str
        for pedaco in assunto.split(","):
            if not pedaco.strip():
                continue
            ids: list[str] = self._indice.get(self._processador.chave_comparacao(pedaco, manter_parte=True), [])
            if not ids:
                ids = self._indice.get(self._processador.chave_comparacao(pedaco, manter_parte=False), [])
            tema_id: str
            for tema_id in ids:
                destino: str = self._canonico(tema_id)
                if destino and destino not in achados:
                    achados.append(destino)
        return tuple(achados)

    def _canonico(self, tema_id: str) -> str:
        """Troca fantasma pelo canônico e descarta o que não é publicável.

        Args:
            tema_id: ID encontrado.

        Returns:
            ID publicável, ou ``""``.
        """
        tema: TemaPreparado | None = self._temas.get(tema_id)
        if tema is not None and tema.canonico_id is not None:
            tema = self._temas.get(tema.canonico_id)
        return tema.tema_id if tema is not None and tema.publicavel else ""
