"""Exemplos sintéticos por tema (ADR-021). Uso: ``uv run python executar_exemplos.py``.

Fase de conhecimento: o LLM propõe questões-modelo só a partir dos temas (nenhuma questão real entra na chamada),
pela camada ``vicio_ia/llm``, com cache em ``runs/exemplos/``. Grava a proposta em
``dados/conhecimento/exemplos_sinteticos.jsonl``, com a proveniência no manifesto.
"""

from vicio_ia.enriquecimento.exemplos import PipelineExemplos


def main() -> None:
    """Gera os exemplos com a configuração padrão do projeto."""
    PipelineExemplos().executar()


if __name__ == "__main__":
    main()
