"""Revisão das propostas de conhecimento (ADR-020). Uso: ``uv run python executar_revisao_conhecimento.py``.

Mostra, na ordem de prioridade da ADR-020, cada proposta de mapa de artigos e de termos, com o contexto
do tema, e grava a decisão (aceitar, corrigir, apagar) a cada item. Pode ser interrompida (``q`` ou
Ctrl+C) e retomada. Ao sair, remonta ``dados/conhecimento/mapa_artigos.csv`` e ``termos.csv``. Não chama
nenhum modelo.
"""

from vicio_ia.enriquecimento.revisao import RevisorInterativo


def main() -> None:
    """Abre a revisão com a configuração padrão do projeto."""
    RevisorInterativo().executar()


if __name__ == "__main__":
    main()
