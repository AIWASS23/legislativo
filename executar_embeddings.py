"""Embeddings da fase de conhecimento (ADR-021). Uso: ``uv run python executar_embeddings.py``.

Gera os vetores dos modelos candidatos pelo Ollama local (camada ``vicio_ia/llm``, com cache em
``runs/embeddings/``), mede o E8 e o E9 na folha-verdade e exporta os vetores do modelo escolhido para
``dados/conhecimento/embeddings/``. A fase de decisão só lê essa exportação. Requer ``ollama pull`` de cada
candidato listado em ``ParametrosEmbeddings``.
"""

from vicio_ia.enriquecimento.pipeline_embeddings import PipelineEmbeddings


def main() -> None:
    """Roda o passo de embeddings com a configuração padrão do projeto."""
    PipelineEmbeddings().executar()


if __name__ == "__main__":
    main()
