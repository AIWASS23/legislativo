"""Análise da infraestrutura e recomendação de modelos (ADR-017). Uso: ``uv run python executar_infra.py``.

Grava ``saidas/infra/relatorio_infra.md``, ``resumo_infra.json`` e ``perfil_maquina.json``.
"""

from vicio_ia.infra.pipeline import PipelineInfra


def main() -> None:
    """Analisa a máquina e recomenda modelos com a configuração padrão do projeto."""
    PipelineInfra().executar()


if __name__ == "__main__":
    main()
