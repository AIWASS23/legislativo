"""Testes unitários. Uso: ``uv run python executar_testes.py`` (sem argumentos).

Roda os arquivos ``testes/teste_*.py`` com o ``unittest`` da biblioteca padrão; os métodos de teste
começam com ``teste_``. Sai com código 1 se algum teste falhar. Também roda dentro do portão de
qualidade (``executar_checagem.py``).
"""

import sys
import unittest


def main() -> None:
    """Descobre e roda os testes."""
    carregador: unittest.TestLoader = unittest.TestLoader()
    carregador.testMethodPrefix = "teste"
    suite: unittest.TestSuite = carregador.discover(start_dir="testes", pattern="teste_*.py", top_level_dir=".")
    resultado: unittest.TestResult = unittest.TextTestRunner(verbosity=1).run(suite)
    sys.exit(0 if resultado.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
