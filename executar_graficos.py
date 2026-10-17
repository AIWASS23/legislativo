"""Gráficos de confiabilidade e de precisão × cobertura (ADR-013). Uso: ``uv run python executar_graficos.py``.

Lê o gold, ``dados/classificacao/sinais.jsonl`` e a calibração e grava ``saidas/avaliacao/`` (PNG, SVG e
``graficos.md`` com as tabelas equivalentes). Não chama nenhum modelo.
"""

from pathlib import Path

from vicio_ia.avaliacao.graficos import GraficosAvaliacao


def main() -> None:
    """Gera os gráficos com a configuração padrão do projeto."""
    destino: Path = GraficosAvaliacao().executar()
    print(f"Gráficos: {destino.parent}")


if __name__ == "__main__":
    main()
