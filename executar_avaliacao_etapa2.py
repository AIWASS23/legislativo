"""Experimentos da etapa 2 na folha-verdade (ADR-024). Uso: ``uv run python executar_avaliacao_etapa2.py``.

Roda o E7 (só lexical) e o E11 (separabilidade do fora) e grava o relatório em ``saidas/etapa2/``.
Não chama nenhum modelo.
"""

from vicio_ia.sistema.experimentos import ExperimentosEtapa2


def main() -> None:
    """Roda os experimentos com a configuração padrão do projeto."""
    ExperimentosEtapa2().executar()


if __name__ == "__main__":
    main()
