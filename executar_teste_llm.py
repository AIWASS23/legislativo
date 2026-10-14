"""Teste rápido dos modelos escolhidos (ADR-017). Uso: ``uv run python executar_teste_llm.py``.

Envia uma questão simples, com saída estruturada, ao modelo de cada papel e mostra se a
chamada funcionou, se acertou o tema, a latência e os tokens. Consome uma chamada por modelo
(assinatura, API ou GPU local, conforme o provedor).
"""

import sys

from vicio_ia.llm.teste import TesteProvedores


def main() -> None:
    """Testa os modelos resolvidos; sai com código 1 se algum falhar."""
    sys.exit(0 if TesteProvedores().executar() else 1)


if __name__ == "__main__":
    main()
