"""Base de conhecimento dos temas (ADR-020). Uso: ``uv run python executar_base_temas.py``.

Fase de conhecimento, sem modelo: junta a árvore, os cartões, o mapa de artigos e os termos revisados (D14)
e os IDs da folha-verdade em ``dados/conhecimento/temas.jsonl``, com a proveniência no manifesto.
"""

from vicio_ia.enriquecimento.base_temas import PipelineBaseTemas


def main() -> None:
    """Monta a base com a configuração padrão do projeto."""
    PipelineBaseTemas().executar()


if __name__ == "__main__":
    main()
