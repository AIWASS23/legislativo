"""Validação dos entregáveis (ADR-015). Uso: ``uv run python executar_validacao.py`` (sem argumentos).

Confere ``publicacao.csv`` e ``previsao.txt`` da pasta dos entregáveis da etapa em vigor (``relatorio/etapa2/``) contra o formato do LEIA-ME. Sai com
código 1 se houver problema.
"""

import sys

from vicio_ia.entrega.validador import ValidadorEntrega


def main() -> None:
    """Valida e mostra o resultado."""
    problemas: list[str] = ValidadorEntrega().validar()
    if problemas:
        print(f"Entrega inválida ({len(problemas)} problemas):")
        problema: str
        for problema in problemas[:30]:
            print(f"  - {problema}")
        sys.exit(1)
    print("Entrega válida: publicacao.csv e previsao.txt no formato do LEIA-ME.")


if __name__ == "__main__":
    main()
