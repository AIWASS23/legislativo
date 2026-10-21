"""Separação entre as etapas do case (ADR-018, ADR-026).

A etapa 1 classificou com LLMs e foi entregue (commit ``02d7e19``). Na etapa 2, a decisão não pode
chamar modelo de linguagem (ADR-019). Os pontos de entrada da etapa 1 que chamam LLMs para classificar,
ou que gravam os entregáveis da etapa 1, recusam rodar quando os anexos em uso não são os da etapa 1.
"""

from __future__ import annotations

from vicio_ia.configuracao import Caminhos


class ErroEtapa(Exception):
    """Um passo foi chamado na etapa errada do case."""


class GuardaEtapa:
    """Confere a etapa antes de rodar um passo que só vale numa etapa."""

    @staticmethod
    def exigir_etapa1(caminhos: Caminhos, passo: str) -> None:
        """Recusa um passo da etapa 1 quando os anexos em uso são de outra etapa.

        Args:
            caminhos: Caminhos em uso (a etapa vem deles).
            passo: Nome do passo, para a mensagem de erro.

        Raises:
            ErroEtapa: Se a etapa em uso não for a 1.
        """
        if caminhos.etapa != 1:
            raise ErroEtapa(
                f"{passo} pertence à etapa 1 (commit 02d7e19). Na etapa {caminhos.etapa}, a decisão não chama "
                "modelo de linguagem (ADR-019): use executar_sistema.py. Para reproduzir a etapa 1, faça o "
                "checkout do commit 02d7e19."
            )
