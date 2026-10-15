"""Verificador contrastivo (ADR-008, regras 4 e 5).

O verificador não pergunta "isto está certo?", que tende a confirmar. Ele recebe os cartões
do candidato, do pai, dos irmãos, dos filhos e de alguns extras (segundo colocado, par de
sobreposição), **sem saber qual é o candidato**, e escolhe o que descreve o núcleo cobrado.
O veredito sai da relação entre a escolha e o candidato.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from typing import ClassVar

from vicio_ia.classificacao.montador_prompt import MontadorPrompt
from vicio_ia.classificacao.respostas import Veredito, VereditoVerificador
from vicio_ia.classificacao.schemas import FabricaSchemas
from vicio_ia.llm.cliente import ClienteLLM, ResultadoChamada
from vicio_ia.llm.contratos import ErroProvedor, RequisicaoLLM
from vicio_ia.llm.prompts import ArquivoPrompt
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada
from vicio_ia.temas.arvore_prompt import MaterialArvore


class VerificadorContrastivo:
    """Confere um candidato contra os vizinhos, com os cartões do ramo."""

    MAX_TOKENS: ClassVar[int] = 1500
    _RE_ID_CARTAO: ClassVar[re.Pattern[str]] = re.compile(r"^\[(\d+)\]", re.MULTILINE)

    def __init__(
        self,
        cliente: ClienteLLM,
        montador: MontadorPrompt,
        schemas: FabricaSchemas,
        prompt: ArquivoPrompt,
        material: MaterialArvore,
        temas: Sequence[TemaPreparado],
    ) -> None:
        """Guarda as dependências.

        Args:
            cliente: Cliente do papel ``verificador``.
            montador: Montador de requisições.
            schemas: Fábrica de schemas.
            prompt: ``prompts/verificador.md``.
            material: Versões da árvore (cartões por ramo).
            temas: Árvore preparada.
        """
        self._cliente: ClienteLLM = cliente
        self._montador: MontadorPrompt = montador
        self._schemas: FabricaSchemas = schemas
        self._prompt: ArquivoPrompt = prompt
        self._material: MaterialArvore = material
        self._temas: dict[str, TemaPreparado] = {tema.tema_id: tema for tema in temas}

    @property
    def cliente(self) -> ClienteLLM:
        """Cliente do papel."""
        return self._cliente

    def extras_de(self, candidato: str, sugeridos: Sequence[str]) -> list[str]:
        """Escolhe os nós extras mostrados ao verificador.

        Entram os sugeridos (segundos colocados e escolhas das outras fontes) e os nós do mesmo
        grupo de sobreposição que estão no nível do candidato ou acima.

        Args:
            candidato: Candidato preliminar.
            sugeridos: IDs sugeridos pelas fontes.

        Returns:
            IDs publicáveis, sem o candidato.
        """
        extras: list[str] = [s for s in sugeridos if s and s != candidato and s in self._temas]
        tema: TemaPreparado = self._temas[candidato]
        if tema.grupo_sobreposicao:
            par: TemaPreparado
            for par in self._temas.values():
                if (
                    par.publicavel
                    and par.grupo_sobreposicao == tema.grupo_sobreposicao
                    and par.disciplina != tema.disciplina
                    and par.nivel <= tema.nivel
                ):
                    extras.append(par.tema_id)
        return [e for e in dict.fromkeys(extras) if self._temas[e].publicavel]

    def verificar(self, questao: QuestaoPreparada, candidato: str, sugeridos: Sequence[str]) -> VereditoVerificador:
        """Verifica o candidato.

        Args:
            questao: Questão preparada.
            candidato: Candidato preliminar (publicável).
            sugeridos: Outros nós indicados pelas fontes.

        Returns:
            Veredito (``falha`` se as duas tentativas falharem).
        """
        cartoes: str = self._material.cartoes_ramo(candidato, self.extras_de(candidato, sugeridos))
        opcoes: list[str] = list(dict.fromkeys(self._RE_ID_CARTAO.findall(cartoes)))
        ultimo: str = ""
        try:
            requisicao: RequisicaoLLM = self._montador.requisicao(
                self._cliente.provedor,
                self._prompt.preencher({"cartoes": cartoes.strip()}),
                questao.texto_canonico,
                self._schemas.verificador(opcoes),
                self._prompt.nome,
                self.MAX_TOKENS,
            )
        except ErroProvedor as erro:
            return self._falha(candidato, opcoes, str(erro))
        tentativa: int
        for tentativa in (1, 2):
            try:
                resultado: ResultadoChamada = self._cliente.gerar(
                    requisicao, self._prompt.versao, f"{questao.id}:{candidato}", tentativa
                )
            except ErroProvedor as erro:
                ultimo = str(erro)
                continue
            dados: dict[str, object] = resultado.resposta.dados or {}
            escolha: str = str(dados.get("escolha_id", ""))
            if escolha not in (*opcoes, FabricaSchemas.NENHUM):
                ultimo = f"escolha fora das opções: {escolha!r}"
                continue
            confianca: object = dados.get("confianca")
            return VereditoVerificador(
                veredito=self.relacao(escolha, candidato),
                candidato_id=candidato,
                escolha_id=escolha,
                opcoes=tuple(opcoes),
                nucleo=str(dados.get("nucleo", "")).strip(),
                justificativa=str(dados.get("justificativa", "")).strip(),
                confianca=float(confianca)
                if isinstance(confianca, (int, float)) and not isinstance(confianca, bool)
                else None,
                motivo="",
                provedor=self._cliente.provedor,
                modelo=self._cliente.modelo,
                versao_prompt=self._prompt.versao,
                do_cache=resultado.do_cache,
                latencia_s=round(resultado.resposta.latencia_s, 2),
            )
        return self._falha(candidato, opcoes, ultimo)

    def relacao(self, escolha: str, candidato: str) -> Veredito:
        """Classifica a escolha em relação ao candidato.

        Args:
            escolha: Cartão escolhido (ou ``nenhum``).
            candidato: Candidato preliminar.

        Returns:
            Veredito.
        """
        if escolha == FabricaSchemas.NENHUM:
            return "nenhum"
        if escolha == candidato:
            return "confirma"
        pai_candidato: str | None = self._temas[candidato].parent_id
        pai_escolha: str | None = self._temas[escolha].parent_id if escolha in self._temas else None
        if escolha == pai_candidato:
            return "pai"
        if pai_escolha == candidato:
            return "filho"
        if pai_escolha is not None and pai_escolha == pai_candidato and self._temas[candidato].nivel > 0:
            return "irmao"
        return "outro"

    def _falha(self, candidato: str, opcoes: Sequence[str], erro: str) -> VereditoVerificador:
        """Monta o veredito de falha.

        Args:
            candidato: Candidato preliminar.
            opcoes: Cartões mostrados.
            erro: Mensagem.

        Returns:
            Veredito ``falha``.
        """
        return VereditoVerificador(
            "falha",
            candidato,
            "",
            tuple(opcoes),
            "",
            "",
            None,
            erro,
            self._cliente.provedor,
            self._cliente.modelo,
            self._prompt.versao,
            False,
            0.0,
        )
