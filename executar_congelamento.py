"""Congelamento do pipeline (ADR-012, ADR-014). Uso: ``uv run python executar_congelamento.py`` (sem argumentos).

Grava a impressão digital de prompts, cartões, árvores, decisões da árvore, escolha de modelos e do
código de classificação, decisão e calibração em ``saidas/experimentos/congelamento.json`` e marca o
congelamento em ``registro.md``. O passo 07 avisa se algo mudar depois disso.
"""

from pathlib import Path

from vicio_ia.avaliacao.congelamento import RegistroCongelamento
from vicio_ia.configuracao import Caminhos


def main() -> None:
    """Registra o congelamento."""
    registro: RegistroCongelamento = RegistroCongelamento(Caminhos.padrao())
    destino: Path = registro.registrar(
        "Prompts, cartões (rascunhos do modelo, sem revisão manual: D7), regras de decisão (D9, D10), "
        "modelos por papel (D8) e parâmetros congelados antes da rodada final (decisão do autor, 16/10)."
    )
    print(f"Congelado: {destino}")


if __name__ == "__main__":
    main()
