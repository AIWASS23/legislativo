"""Pipeline completo (ADR-015). Uso: ``uv run python executar_pipeline.py`` (sem argumentos).

Roda, em ordem, a preparação (01), os cartões (02), a classificação e a verificação (05 e 06), a
decisão (07) e a validação dos entregáveis. Com o cache ``runs/`` completo, nenhum modelo é chamado.
"""

import sys

from vicio_ia.classificacao.pipeline import PipelineClassificacao
from vicio_ia.decisao.pipeline import PipelineDecisao
from vicio_ia.entrega.validador import ValidadorEntrega
from vicio_ia.preparacao.pipeline import PipelinePreparacao
from vicio_ia.temas.pipeline import PipelineCartoes


def main() -> None:
    """Roda todos os passos com a configuração padrão do projeto."""
    PipelinePreparacao().executar()
    PipelineCartoes().executar()
    PipelineClassificacao().executar()
    PipelineDecisao().executar()
    problemas: list[str] = ValidadorEntrega().validar()
    if problemas:
        print("Entrega inválida:\n  - " + "\n  - ".join(problemas[:30]))
        sys.exit(1)
    print("Pipeline completo; entrega válida.")


if __name__ == "__main__":
    main()
