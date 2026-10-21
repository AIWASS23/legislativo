"""Passo 07: decisão e entregáveis (ADR-010, ADR-011, ADR-013). Uso: ``uv run python executar_decisao.py``.

Agrega os sinais de ``dados/classificacao/sinais.jsonl``, calibra a confiança no gold, escolhe
o limiar de publicação e grava ``publicacao.csv`` e ``previsao.txt`` em ``relatorio/etapa1/``, com o relatório em
``saidas/decisao/``. Não chama nenhum modelo.
"""

from vicio_ia.decisao.pipeline import PipelineDecisao


def main() -> None:
    """Roda o passo 07 com a configuração padrão do projeto."""
    PipelineDecisao().executar()


if __name__ == "__main__":
    main()
