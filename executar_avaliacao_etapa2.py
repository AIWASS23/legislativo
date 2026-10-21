"""Experimentos da etapa 2 na folha-verdade (ADR-024). Uso: ``uv run python executar_avaliacao_etapa2.py``.

Roda o E7 e o E7b (lexical), o E11 (separabilidade do fora com atributos lexicais), o E11b (com embeddings e
kNN), o E12 (deriva entre antigas e novas), o E10 (ranqueador: logística × gradient boosting) e a medida
secundária com o gold do autor (sobre o ``relatorio/publicacao.csv`` já gravado) e grava os relatórios em
``saidas/etapa2/``. Não chama nenhum modelo de linguagem: os vetores vêm de
``dados/conhecimento/embeddings/``.
"""

from vicio_ia.sistema.experimento_ranqueador import ExperimentoRanqueador
from vicio_ia.sistema.experimentos import ExperimentosEtapa2
from vicio_ia.sistema.experimentos_fora_deriva import ExperimentoForaDeriva
from vicio_ia.sistema.validacao_gold import ValidacaoGold


def main() -> None:
    """Roda os experimentos com a configuração padrão do projeto."""
    ExperimentosEtapa2().executar()
    ExperimentoForaDeriva().executar()
    ExperimentoRanqueador().executar()
    ValidacaoGold().executar()


if __name__ == "__main__":
    main()
