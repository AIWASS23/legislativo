"""Gold set (ADR-012). Uso: ``uv run python executar_gold.py`` (sem argumentos).

Sorteia a amostra (ou reaproveita a gravada), cria a planilha de rótulos se não existir
(nunca a sobrescreve), grava o caderno de rotulagem e mostra a situação.
"""

from vicio_ia.avaliacao.pipeline import PipelineGold


def main() -> None:
    """Prepara e acompanha o gold set com a configuração padrão do projeto."""
    PipelineGold().executar()


if __name__ == "__main__":
    main()
