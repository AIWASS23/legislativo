"""Portão de qualidade do código (ADR-001). Uso: ``uv run python executar_checagem.py`` (sem argumentos).

Roda ``ruff check``, ``ruff format --check``, ``mypy --strict`` e o verificador de
anotações e docstrings. Sai com código 1 se alguma checagem falhar.
"""

import sys

from ferramentas.portao_qualidade import PortaoQualidade


def main() -> None:
    """Executa todas as checagens e encerra com o código de saída correspondente."""
    sys.exit(0 if PortaoQualidade().executar() else 1)


if __name__ == "__main__":
    main()
