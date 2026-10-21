"""Experimentos da etapa 2 na folha-verdade (ADR-024). Uso: ``uv run python executar_avaliacao_etapa2.py``.

Roda o E7 e o E7b (lexical), o E11 (separabilidade do fora com atributos lexicais), o E11b (com embeddings e
kNN) e o E12 (deriva entre antigas e novas) e grava os relatórios em ``saidas/etapa2/``. Não chama nenhum
modelo: os vetores vêm de ``dados/conhecimento/embeddings/``.
"""

from vicio_ia.sistema.experimentos import ExperimentosEtapa2
from vicio_ia.sistema.experimentos_fora_deriva import ExperimentoForaDeriva


def main() -> None:
    """Roda os experimentos com a configuração padrão do projeto."""
    ExperimentosEtapa2().executar()
    ExperimentoForaDeriva().executar()


if __name__ == "__main__":
    main()
