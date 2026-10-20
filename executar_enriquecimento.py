"""Fase de conhecimento da etapa 2 (ADR-019, ADR-020). Uso: ``uv run python executar_enriquecimento.py``.

Pode chamar LLMs (pela camada ``vicio_ia/llm``, com cache em ``runs/``), mas só com informação dos temas:
nenhuma questão entra nas chamadas. Grava as propostas de mapa de artigos e de termos em
``dados/conhecimento/propostas/``, para revisão do autor, e registra a proveniência no manifesto.
"""

from vicio_ia.enriquecimento.pipeline import PipelineEnriquecimento


def main() -> None:
    """Roda a fase de conhecimento com a configuração padrão do projeto."""
    PipelineEnriquecimento().executar()


if __name__ == "__main__":
    main()
