"""Passo 01: preparação das questões (ADR-004). Uso: ``uv run python executar_preparacao.py`` (sem argumentos).

Grava ``dados/preparados/questoes.jsonl`` e, em ``saidas/preparacao/``, o relatório,
o resumo e a amostra de conferência manual do texto canônico.
"""

from vicio_ia.preparacao.pipeline import PipelinePreparacao


def main() -> None:
    """Prepara as questões com a configuração padrão do projeto."""
    PipelinePreparacao().executar()


if __name__ == "__main__":
    main()
