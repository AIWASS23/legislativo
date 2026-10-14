"""Escolha interativa de modelos por papel (ADR-017). Uso: ``uv run python executar_escolha_modelo.py``.

Mostra os modelos viáveis nesta máquina e grava a escolha em ``config/escolha_modelos.json``
(modo automático ou um modelo por papel).
"""

import sys

from vicio_ia.llm.escolha_interativa import EscolhaInterativa


def main() -> None:
    """Conduz a escolha no terminal; sai com código 1 se nada for gravado."""
    sys.exit(0 if EscolhaInterativa().executar() else 1)


if __name__ == "__main__":
    main()
