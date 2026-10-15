"""Passo 02: cartões de tema (ADR-007). Uso: ``uv run python executar_cartoes.py`` (sem argumentos).

Gera os rascunhos com o modelo do papel verificador (uma chamada por tema pai, com cache),
aplica os ajustes de ``dados/temas/cartoes_ajustes.csv``, confere e grava os cartões finais,
a árvore com escopo e o caderno de revisão.
"""

from vicio_ia.temas.pipeline import PipelineCartoes


def main() -> None:
    """Roda o passo 02 com a configuração padrão do projeto."""
    PipelineCartoes().executar()


if __name__ == "__main__":
    main()
