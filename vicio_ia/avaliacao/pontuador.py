"""Régua do case aplicada ao gold set (ADR-012): modos estrito e tolerante."""

from __future__ import annotations

from typing import Literal

from vicio_ia.arvore import ArvoreTemas
from vicio_ia.avaliacao.planilha import RotuloGold

type ModoRegua = Literal["estrita", "tolerante"]
"""Como os rótulos alternativos entram na conta."""

type RelacaoRegua = Literal["exato", "pai", "filho", "irmao", "outro"]
"""Relação entre o nó publicado e o nó do rótulo, vista a partir do publicado."""


class PontuadorRegua:
    """Diz se uma publicação conta como certa, com a mesma regra da banca.

    A régua (``ArvoreTemas.mesmo_ramo``): certo se o nó publicado é o do especialista,
    o pai direto dele ou um filho direto. Irmão é erro. No gold, o especialista é o
    nosso rótulo, e há dois modos:

    * **estrita:** só o ``tema_id`` vale. Se o rótulo é um pai e há em ``alternativos``
      outro filho dele plausível, publicar num filho conta como erro (o especialista
      pode ter escolhido o irmão).
    * **tolerante:** vale qualquer nó entre ``tema_id`` e ``alternativos``.

    Questão rotulada ``fora`` e publicada é sempre erro.
    """

    def __init__(self, arvore: ArvoreTemas) -> None:
        """Guarda a árvore original (``temas.csv``), a mesma usada pela banca.

        Args:
            arvore: Árvore de temas.
        """
        self._arvore: ArvoreTemas = arvore

    def relacao(self, publicado: str, rotulado: str) -> RelacaoRegua:
        """Classifica a relação entre o nó publicado e o rotulado (para o diagnóstico).

        Args:
            publicado: Nó publicado.
            rotulado: Nó do rótulo.

        Returns:
            ``exato``, ``pai`` (o publicado é pai do rotulado), ``filho``, ``irmao`` ou ``outro``.
        """
        if publicado == rotulado:
            return "exato"
        if not self._arvore.existe(publicado) or not self._arvore.existe(rotulado):
            return "outro"
        pai_publicado: str | None = self._arvore.tema(publicado).parent_id
        pai_rotulado: str | None = self._arvore.tema(rotulado).parent_id
        if pai_rotulado == publicado:
            return "pai"
        if pai_publicado == rotulado:
            return "filho"
        if pai_publicado is not None and pai_publicado == pai_rotulado:
            return "irmao"
        return "outro"

    def acerta(self, publicado: str, rotulo: RotuloGold, modo: ModoRegua) -> bool:
        """Aplica a régua.

        Args:
            publicado: Nó em que a questão seria publicada.
            rotulo: Rótulo manual (preenchido).
            modo: ``estrita`` ou ``tolerante``.

        Returns:
            ``True`` se a publicação conta como certa.
        """
        if rotulo.fora or not rotulo.tema_id:
            return False
        if modo == "tolerante":
            return any(self._arvore.mesmo_ramo(publicado, aceito) for aceito in (rotulo.tema_id, *rotulo.alternativos))
        if not self._arvore.mesmo_ramo(publicado, rotulo.tema_id):
            return False
        if self.relacao(publicado, rotulo.tema_id) != "filho":
            return True
        irmaos_plausiveis: list[str] = [
            alternativo
            for alternativo in rotulo.alternativos
            if alternativo != publicado and self.relacao(alternativo, rotulo.tema_id) == "filho"
        ]
        return not irmaos_plausiveis
