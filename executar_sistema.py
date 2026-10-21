"""Sistema de classificação da etapa 2 (ADR-019 a ADR-026). Uso: ``uv run python executar_sistema.py``.

Regenera ``relatorio/etapa2/publicacao.csv`` e ``relatorio/etapa2/previsao.txt`` a partir dos anexos e dos artefatos
versionados, **sem chamar modelo de linguagem e sem rede**: a trava ``VICIO_SEM_LLM=1`` impede criar qualquer
provedor, e a ``TravaSemLLM`` bloqueia conexões de rede durante a execução. O tempo fica em
``saidas/sistema/execucao.json``.
"""

import os

from vicio_ia.configuracao import ParametrosSistema
from vicio_ia.sistema.pipeline import SistemaEtapa2
from vicio_ia.sistema.trava import TravaSemLLM


def main() -> None:
    """Roda o sistema com a trava ligada."""
    os.environ[ParametrosSistema().variavel_sem_llm] = "1"
    trava: TravaSemLLM = TravaSemLLM()
    trava.ativar()
    try:
        SistemaEtapa2().executar()
    finally:
        trava.desativar()


if __name__ == "__main__":
    main()
