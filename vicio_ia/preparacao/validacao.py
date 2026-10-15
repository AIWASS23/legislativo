"""Checagens automáticas das questões preparadas (regras da ADR-004 e da ADR-006)."""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass, replace
from typing import ClassVar

from vicio_ia.dominio import Questao
from vicio_ia.preparacao.texto_canonico import MontadorTextoCanonico, QuestaoPreparada


@dataclass(frozen=True)
class ResultadoChecagem:
    """Resultado de uma regra verificada.

    Attributes:
        regra: O que foi verificado.
        aprovada: ``True`` se nenhuma questão violou a regra.
        violacoes: IDs (ou descrições) das violações, limitados aos primeiros casos.
    """

    regra: str
    aprovada: bool
    violacoes: tuple[str, ...]


class ValidadorQuestoesPreparadas:
    """Confere as questões preparadas contra as regras do texto canônico."""

    SENTINELA: ClassVar[str] = "ROTULO_DE_ORIGEM_SENTINELA"
    _RE_TAG: ClassVar[re.Pattern[str]] = re.compile(r"<\s*/?\s*[a-zA-Z!][^>]*>")
    _RE_EDITOR: ClassVar[re.Pattern[str]] = re.compile(r"mso-|\{[^}]*:[^}]*;[^}]*\}")
    _RE_ESCAPE: ClassVar[re.Pattern[str]] = re.compile(r"\\[nrt]")
    MAX_VIOLACOES: ClassVar[int] = 10

    def __init__(self, montador: MontadorTextoCanonico) -> None:
        """Recebe o montador, usado no teste de vazamento dos rótulos de origem.

        Args:
            montador: Montador do texto canônico.
        """
        self._montador: MontadorTextoCanonico = montador

    def validar(self, questoes: Sequence[Questao], preparadas: Sequence[QuestaoPreparada]) -> list[ResultadoChecagem]:
        """Roda todas as checagens.

        Args:
            questoes: Questões originais.
            preparadas: Questões preparadas, na mesma ordem.

        Returns:
            Um resultado por regra.
        """
        ids_originais: list[str] = [questao.id for questao in questoes]
        ids_preparados: list[str] = [preparada.id for preparada in preparadas]
        return [
            self._resultado(
                "todas as questões foram preparadas, uma vez cada",
                [i for i in ids_originais if ids_preparados.count(i) != 1],
            ),
            self._resultado(
                "nenhum texto canônico vazio",
                [p.id for p in preparadas if not p.texto_canonico.strip()],
            ),
            self._resultado(
                "nenhuma tag HTML no texto canônico",
                [p.id for p in preparadas if self._RE_TAG.search(p.texto_canonico)],
            ),
            self._resultado(
                "nenhum escape literal (barra + n ou t) no texto canônico",
                [p.id for p in preparadas if self._RE_ESCAPE.search(p.texto_canonico)],
            ),
            self._resultado(
                "nenhum resíduo de editor (CSS do Word) no texto canônico",
                [p.id for p in preparadas if self._RE_EDITOR.search(p.texto_canonico)],
            ),
            self._resultado(
                "múltipla escolha traz todas as alternativas; certo/errado não traz alternativas",
                [p.id for p in preparadas if not self._alternativas_corretas(p)],
            ),
            self._resultado(
                "comando no texto só quando útil e com conteúdo",
                [p.id for p in preparadas if ("\nComando: " in p.texto_canonico) != (p.motivo_comando == "incluido")],
            ),
            self._resultado(
                "rótulos de origem não entram no texto canônico (ADR-006)",
                self._vazamentos_de_origem(questoes, preparadas),
            ),
        ]

    def _alternativas_corretas(self, preparada: QuestaoPreparada) -> bool:
        """Confere as linhas de alternativas do texto canônico.

        Args:
            preparada: Questão preparada.

        Returns:
            ``True`` se o texto tem exatamente as alternativas esperadas.
        """
        linhas: list[str] = preparada.texto_canonico.splitlines()
        letras: set[str] = {
            letra for letra in preparada.alternativas if any(linha.startswith(f"{letra}) ") for linha in linhas)
        }
        if preparada.formato == "certo_errado":
            return not letras
        return letras == set(preparada.alternativas)

    def _vazamentos_de_origem(self, questoes: Sequence[Questao], preparadas: Sequence[QuestaoPreparada]) -> list[str]:
        """Troca os rótulos de origem por uma sentinela e confere que o texto não muda.

        Args:
            questoes: Questões originais.
            preparadas: Questões preparadas.

        Returns:
            IDs em que o texto mudou ou a sentinela apareceu.
        """
        textos: dict[str, str] = {preparada.id: preparada.texto_canonico for preparada in preparadas}
        vazamentos: list[str] = []
        questao: Questao
        for questao in questoes:
            alterada: Questao = replace(questao, disciplina_origem=self.SENTINELA, assunto_origem=self.SENTINELA)
            texto: str = self._montador.montar(alterada)
            if self.SENTINELA in texto or texto != textos.get(questao.id):
                vazamentos.append(questao.id)
        return vazamentos

    def _resultado(self, regra: str, violacoes: list[str]) -> ResultadoChecagem:
        """Monta o resultado de uma regra.

        Args:
            regra: Descrição da regra.
            violacoes: Casos que violaram a regra.

        Returns:
            Resultado com no máximo :attr:`MAX_VIOLACOES` exemplos.
        """
        return ResultadoChecagem(regra, not violacoes, tuple(violacoes[: self.MAX_VIOLACOES]))
