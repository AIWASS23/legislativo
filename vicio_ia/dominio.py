"""Entidades de domínio: questão e tema, do jeito que vêm dos anexos."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final, Literal

type TipoDescricao = Literal["raiz", "vazia", "modelo", "rica"]
"""Classificação da descrição de um tema.

* ``raiz``: descrição de disciplina ("Disciplina (root). N questões...").
* ``vazia``: sem descrição.
* ``modelo``: texto-modelo sem conteúdo ("Subtema de X. N questões no source").
* ``rica``: descrição de verdade, com conteúdo jurídico.
"""

_RE_CONTAGEM_MODELO: Final[re.Pattern[str]] = re.compile(r"(\d+)\s+questões\s+no\s+source")
_RE_CONTAGEM_RAIZ: Final[re.Pattern[str]] = re.compile(r"Disciplina \(root\)\.\s*(\d+)\s+questões")


@dataclass(frozen=True)
class Questao:
    """Uma questão de concurso, como está em ``questoes.jsonl``.

    Attributes:
        id: Identificador da questão no case (``Q0001``...).
        enunciado_html: Enunciado em HTML cru, como está no banco.
        comando: Comando da questão (pode vir vazio ou com ruído).
        alternativas: Letra da alternativa -> texto (pode conter HTML).
        disciplina_origem: Disciplina atribuída pelo site de origem (pode estar errada).
        assunto_origem: Assunto atribuído pelo site de origem (pode estar errado).
    """

    id: str
    enunciado_html: str
    comando: str
    alternativas: Mapping[str, str]
    disciplina_origem: str
    assunto_origem: str


@dataclass(frozen=True)
class Tema:
    """Um nó da árvore de temas (uma linha de ``temas.csv``).

    Attributes:
        tema_id: Identificador do tema, mantido como texto.
        parent_id: Identificador do pai; ``None`` para as disciplinas (raízes).
        disciplina: Disciplina a que o nó pertence.
        nivel: 0 = disciplina, 1 = tema, 2 = subtema.
        titulo: Título exibido na plataforma.
        caminho: Caminho completo, separado por ``" > "``.
        descricao: Descrição como veio no CSV.
        status: ``active`` ou ``inactive``.
    """

    tema_id: str
    parent_id: str | None
    disciplina: str
    nivel: int
    titulo: str
    caminho: str
    descricao: str
    status: str

    @property
    def ativo(self) -> bool:
        """Indica se o tema pode ser usado (``status == "active"``)."""
        return self.status == "active"

    @property
    def tipo_descricao(self) -> TipoDescricao:
        """Classifica a descrição em raiz, vazia, modelo ou rica."""
        if self.nivel == 0:
            return "raiz"
        if not self.descricao.strip():
            return "vazia"
        if _RE_CONTAGEM_MODELO.search(self.descricao):
            return "modelo"
        return "rica"

    @property
    def n_questoes_origem(self) -> int | None:
        """Quantidade de questões que o nó tinha no sistema de origem.

        O número é lido da descrição-modelo (ou da descrição da raiz). Nós com
        descrição vazia ou rica não informam contagem e devolvem ``None``.
        """
        correspondencia: re.Match[str] | None = _RE_CONTAGEM_MODELO.search(self.descricao)
        if correspondencia is None:
            correspondencia = _RE_CONTAGEM_RAIZ.search(self.descricao)
        if correspondencia is None:
            return None
        return int(correspondencia.group(1))
