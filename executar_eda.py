"""Ponto de entrada da EDA. Uso: ``uv run python executar_eda.py`` (sem argumentos).

A configuração (caminhos e limiares) fica em ``vicio_ia/configuracao.py``.
"""

from vicio_ia.eda.pipeline import PipelineEDA


def main() -> None:
    """Executa a EDA completa com a configuração padrão do projeto."""
    PipelineEDA().executar()


if __name__ == "__main__":
    main()
