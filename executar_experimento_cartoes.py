"""Experimento E4 (ADR-014): cartões de tema × só títulos. Uso: ``uv run python executar_experimento_cartoes.py``.

Classifica as questões rotuladas da leva 1 com o classificador B nas duas versões do material
(com cache) e acrescenta o resultado em ``saidas/experimentos/resultados.csv``.
"""

from vicio_ia.avaliacao.experimento_cartoes import ExperimentoCartoes


def main() -> None:
    """Roda o E4 com a configuração padrão do projeto."""
    ExperimentoCartoes().executar()


if __name__ == "__main__":
    main()
