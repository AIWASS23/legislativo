"""Citações de lei e artigo nas questões (ADR-021). Uso: ``uv run python executar_citacoes.py``.

Fase de conhecimento, mas sem modelo: só expressões regulares. Grava ``dados/conhecimento/citacoes.jsonl``,
registra a proveniência no manifesto e escreve o relatório em ``saidas/etapa2/citacoes.md``.
"""

from vicio_ia.enriquecimento.pipeline_citacoes import PipelineCitacoes


def main() -> None:
    """Roda o passo de citações com a configuração padrão do projeto."""
    PipelineCitacoes().executar()


if __name__ == "__main__":
    main()
