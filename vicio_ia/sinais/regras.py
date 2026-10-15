"""Regra das leis citadas: lei citada -> temas que ela costuma indicar (sinal fraco, ADR-008)."""

from __future__ import annotations

from collections.abc import Sequence

from vicio_ia.conhecimento import LeiConhecida, MapaLegislacao
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada


class SinalLegislacao:
    """Converte as leis citadas numa questão em temas publicáveis.

    Nós fantasmas viram o canônico (D1); nós não publicáveis são descartados. O sinal é
    fraco: citar a Lei de Drogas pode ser para cobrar Processo Penal.
    """

    def __init__(self, mapa: MapaLegislacao, temas: Sequence[TemaPreparado]) -> None:
        """Indexa a árvore.

        Args:
            mapa: Mapa das leis do recorte.
            temas: Árvore preparada.
        """
        self._mapa: MapaLegislacao = mapa
        self._temas: dict[str, TemaPreparado] = {tema.tema_id: tema for tema in temas}

    def temas(self, questao: QuestaoPreparada) -> tuple[str, ...]:
        """Temas indicados pelas leis citadas.

        Args:
            questao: Questão preparada.

        Returns:
            IDs publicáveis, sem repetição, na ordem das leis.
        """
        indicados: list[str] = []
        numero: str
        for numero in questao.marcas.leis_citadas:
            lei: LeiConhecida | None = self._mapa.lei(numero)
            tema_id: str
            for tema_id in lei.temas if lei is not None else ():
                destino: str = self._canonico(tema_id)
                if destino and destino not in indicados:
                    indicados.append(destino)
        return tuple(indicados)

    def _canonico(self, tema_id: str) -> str:
        """Troca fantasma pelo canônico e descarta o que não é publicável.

        Args:
            tema_id: ID indicado pelo mapa.

        Returns:
            ID publicável, ou ``""``.
        """
        tema: TemaPreparado | None = self._temas.get(tema_id)
        if tema is None:
            return ""
        if tema.canonico_id is not None:
            tema = self._temas.get(tema.canonico_id)
        return tema.tema_id if tema is not None and tema.publicavel else ""
