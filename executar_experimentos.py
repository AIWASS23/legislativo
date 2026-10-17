"""Experimentos no gold set (ADR-014). Uso: ``uv run python executar_experimentos.py`` (sem argumentos).

Roda E0 (assunto de origem), E2 (classificador A sozinho) e E3 (B e voto barato sozinhos, e
erros em comum de A e B) com os rótulos já feitos e ``dados/classificacao/sinais.jsonl``.
Acrescenta os resultados em ``saidas/experimentos/resultados.csv``; mostra só números agregados.
"""

from vicio_ia.avaliacao.experimentos import PipelineExperimentos


def main() -> None:
    """Roda os experimentos com a configuração padrão do projeto."""
    PipelineExperimentos().executar()


if __name__ == "__main__":
    main()
