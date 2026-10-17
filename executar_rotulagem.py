"""Rotulagem interativa do gold set (ADR-012). Uso: ``uv run python executar_rotulagem.py``.

Mostra cada questão pendente só com o texto canônico, ajuda a buscar o tema na árvore e
grava o rótulo assim que ele é confirmado. Pode ser interrompida (``q`` ou Ctrl+C) e retomada.
"""

from vicio_ia.avaliacao.rotulagem import RotuladorInterativo


def main() -> None:
    """Rotula as questões pendentes com a configuração padrão do projeto."""
    RotuladorInterativo().executar()


if __name__ == "__main__":
    main()
