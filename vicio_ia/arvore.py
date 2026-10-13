"""Índice da árvore de temas com consultas de parentesco."""

from __future__ import annotations

from collections.abc import Sequence

from vicio_ia.dominio import Tema


class ArvoreTemas:
    """Árvore de temas em memória (disciplina > tema > subtema).

    A régua do case considera certo publicar no tema do especialista ou num
    nó do mesmo ramo (pai ou filho direto); :meth:`mesmo_ramo` implementa
    exatamente essa regra e é reutilizada nas próximas etapas.
    """

    def __init__(self, temas: Sequence[Tema]) -> None:
        """Indexa os temas por ID e monta as listas de filhos.

        Args:
            temas: Todos os temas de ``temas.csv``.
        """
        self._por_id: dict[str, Tema] = {}
        self._filhos: dict[str, list[str]] = {}
        self._ids_duplicados: list[str] = []
        tema: Tema
        for tema in temas:
            if tema.tema_id in self._por_id:
                self._ids_duplicados.append(tema.tema_id)
            self._por_id[tema.tema_id] = tema
            self._filhos.setdefault(tema.tema_id, [])
        for tema in self._por_id.values():
            if tema.parent_id is not None:
                self._filhos.setdefault(tema.parent_id, []).append(tema.tema_id)

    def __len__(self) -> int:
        """Número de nós distintos na árvore."""
        return len(self._por_id)

    @property
    def ids_duplicados(self) -> list[str]:
        """IDs que apareceram mais de uma vez no CSV (o último prevalece)."""
        return list(self._ids_duplicados)

    def todos(self) -> list[Tema]:
        """Devolve todos os nós, na ordem do CSV.

        Returns:
            Lista de temas.
        """
        return list(self._por_id.values())

    def existe(self, tema_id: str) -> bool:
        """Indica se o ID existe na árvore.

        Args:
            tema_id: ID do tema.

        Returns:
            ``True`` se existir.
        """
        return tema_id in self._por_id

    def tema(self, tema_id: str) -> Tema:
        """Busca um tema pelo ID.

        Args:
            tema_id: ID do tema.

        Returns:
            O tema.

        Raises:
            KeyError: Se o ID não existir.
        """
        if tema_id not in self._por_id:
            raise KeyError(f"tema inexistente: {tema_id}")
        return self._por_id[tema_id]

    def pai(self, tema_id: str) -> Tema | None:
        """Busca o pai de um tema.

        Args:
            tema_id: ID do tema.

        Returns:
            O pai, ou ``None`` para raízes e nós órfãos.
        """
        pai_id: str | None = self.tema(tema_id).parent_id
        if pai_id is None:
            return None
        return self._por_id.get(pai_id)

    def filhos(self, tema_id: str) -> list[Tema]:
        """Lista os filhos diretos de um tema.

        Args:
            tema_id: ID do tema.

        Returns:
            Filhos na ordem do CSV.
        """
        return [self._por_id[filho] for filho in self._filhos.get(tema_id, []) if filho in self._por_id]

    def irmaos(self, tema_id: str) -> list[Tema]:
        """Lista os irmãos de um tema (mesmo pai), sem incluir o próprio.

        Args:
            tema_id: ID do tema.

        Returns:
            Irmãos na ordem do CSV. Para raízes, as outras raízes.
        """
        tema: Tema = self.tema(tema_id)
        candidatos: list[Tema] = self.raizes() if tema.parent_id is None else self.filhos(tema.parent_id)
        return [irmao for irmao in candidatos if irmao.tema_id != tema_id]

    def raizes(self) -> list[Tema]:
        """Lista as disciplinas (nós sem pai).

        Returns:
            Raízes na ordem do CSV.
        """
        return [tema for tema in self._por_id.values() if tema.parent_id is None]

    def orfaos(self) -> list[Tema]:
        """Lista nós cujo ``parent_id`` não existe na árvore.

        Returns:
            Nós órfãos.
        """
        return [
            tema for tema in self._por_id.values() if tema.parent_id is not None and tema.parent_id not in self._por_id
        ]

    def ancestrais(self, tema_id: str) -> list[Tema]:
        """Lista os ancestrais de um tema, da raiz até o pai.

        Args:
            tema_id: ID do tema.

        Returns:
            Ancestrais em ordem descendente (raiz primeiro). Para ao encontrar
            um ciclo ou um pai inexistente.
        """
        cadeia: list[Tema] = []
        vistos: set[str] = {tema_id}
        atual: Tema | None = self.pai(tema_id)
        while atual is not None and atual.tema_id not in vistos:
            cadeia.append(atual)
            vistos.add(atual.tema_id)
            atual = self.pai(atual.tema_id)
        cadeia.reverse()
        return cadeia

    def mesmo_ramo(self, tema_a: str, tema_b: str) -> bool:
        """Aplica a régua do case: mesmo nó, ou um é pai direto do outro.

        Publicar em outro subtema do mesmo tema (irmão) conta como erro.

        Args:
            tema_a: ID de um tema.
            tema_b: ID de outro tema.

        Returns:
            ``True`` se a publicação em ``tema_a`` contaria como certa para o
            rótulo ``tema_b`` (a relação é simétrica).
        """
        if tema_a == tema_b:
            return True
        if not self.existe(tema_a) or not self.existe(tema_b):
            return False
        return self.tema(tema_a).parent_id == tema_b or self.tema(tema_b).parent_id == tema_a
