"""Passos 05 e 06: classificação e verificação (ADR-008). Uso: ``uv run python executar_classificacao.py``.

Classifica as questões com os modelos escolhidos para cada papel (A, B, voto barato),
verifica as candidatas a publicar e grava ``dados/classificacao/sinais.jsonl``. Questões do
gold ainda sem rótulo ficam para depois. Tudo passa pelo cache: rodar de novo só chama o que
falta.
"""

from vicio_ia.classificacao.pipeline import PipelineClassificacao


def main() -> None:
    """Roda os passos 05 e 06 com a configuração padrão do projeto."""
    PipelineClassificacao().executar()


if __name__ == "__main__":
    main()
