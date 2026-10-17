"""Dados sintéticos para os testes: uma árvore pequena, questões e sinais montados à mão.

Árvore usada em todos os testes::

    D  Penal (disciplina, nível 0)
    ├── T   Tema com filhos (nível 1)
    │   ├── X1  Subtema 1
    │   └── X2  Subtema 2
    ├── U   Tema sem filhos
    ├── L   Tema genérico, lixeira forte, sem filhos
    ├── T2  Tema com um subtema lixeira
    │   └── LX  Subtema genérico, lixeira forte
    ├── P1  Tema em grupo de sobreposição "g"
    └── K   Tema com cópia "(Parte N)" (risco de convenção)
    E  Processo Penal (disciplina, nível 0)
    └── P2  Tema em grupo de sobreposição "g"
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from vicio_ia.classificacao.respostas import SinaisQuestao, Veredito, VereditoVerificador, VotoClassificador
from vicio_ia.preparacao.arvore_preparada import NivelLixeira, TemaPreparado, TipoConvencao
from vicio_ia.preparacao.texto_canonico import MarcasQuestao, QuestaoPreparada


class FabricaTestes:
    """Monta temas, questões, votos e sinais com valores padrão, só com o que cada teste precisa mudar."""

    DISCIPLINA_DE: ClassVar[dict[str, str]] = {"P2": "Processo Penal"}

    def temas(self) -> list[TemaPreparado]:
        """Árvore do docstring do módulo.

        Returns:
            Nós preparados.
        """
        return [
            self.tema("D", None, 0, ("T", "U", "L", "T2", "P1", "K"), publicavel=False),
            self.tema("E", None, 0, ("P2",), publicavel=False, disciplina="Processo Penal"),
            self.tema("T", "D", 1, ("X1", "X2")),
            self.tema("X1", "T", 2, ()),
            self.tema("X2", "T", 2, ()),
            self.tema("U", "D", 1, ()),
            self.tema("L", "D", 1, (), lixeira="forte"),
            self.tema("T2", "D", 1, ("LX",)),
            self.tema("LX", "T2", 2, (), lixeira="forte"),
            self.tema("P1", "D", 1, (), grupo="g"),
            self.tema("P2", "E", 1, (), grupo="g", disciplina="Processo Penal"),
            self.tema("K", "D", 1, (), convencao="duplicado_parte"),
        ]

    @staticmethod
    def tema(
        tema_id: str,
        pai: str | None,
        nivel: int,
        filhos: Sequence[str],
        publicavel: bool = True,
        lixeira: NivelLixeira = "",
        grupo: str = "",
        convencao: TipoConvencao = "",
        disciplina: str = "Penal",
    ) -> TemaPreparado:
        """Cria um nó.

        Args:
            tema_id: ID.
            pai: ID do pai (``None`` para disciplina).
            nivel: Nível.
            filhos: IDs dos filhos.
            publicavel: Pode ser tema central.
            lixeira: Nível de lixeira.
            grupo: Grupo de sobreposição.
            convencao: Tipo de risco de convenção.
            disciplina: Disciplina.

        Returns:
            Nó preparado.
        """
        caminho: str = f"{disciplina} > {tema_id}" if pai is not None else disciplina
        return TemaPreparado(
            tema_id=tema_id,
            parent_id=pai,
            disciplina=disciplina,
            nivel=nivel,
            titulo=tema_id,
            titulo_exibicao=tema_id,
            caminho=caminho,
            caminho_exibicao=caminho,
            status="active",
            publicavel=publicavel,
            fantasma=False,
            canonico_id=None,
            duplicado_por=(),
            lixeira=lixeira,
            grupo_sobreposicao=grupo,
            regra_desempate=f"regra do grupo {grupo}" if grupo else "",
            tipo_convencao=convencao,
            zona_convencao=bool(convencao),
            aceita_recuo=nivel == 1 and bool(filhos),
            filhos=tuple(filhos),
            n_questoes_origem=None,
        )

    @staticmethod
    def questao(questao_id: str = "Q1", generico: bool = False, jurisprudencia: bool = False) -> QuestaoPreparada:
        """Cria uma questão preparada mínima.

        Args:
            questao_id: ID.
            generico: Enunciado genérico (o assunto está nas alternativas).
            jurisprudencia: Cita jurisprudência.

        Returns:
            Questão preparada.
        """
        return QuestaoPreparada(
            id=questao_id,
            formato="multipla_escolha_5",
            texto_canonico=f"[{questao_id}] texto",
            enunciado="texto",
            comando="",
            tipo_comando="vazio",
            motivo_comando="vazio",
            alternativas={"A": "a", "B": "b"},
            marcas=MarcasQuestao(
                enunciado_generico=generico,
                html_de_editor=False,
                leis_citadas=(),
                menciona_cp=False,
                menciona_cpp=False,
                menciona_cf=False,
                menciona_jurisprudencia=jurisprudencia,
            ),
            hash_completo="0",
            duplicata_de=None,
            caracteres=5,
            tokens_estimados=2,
            original={},
        )

    @staticmethod
    def voto(
        papel: str,
        tema_id: str,
        ok: bool = True,
        fora: bool = False,
        multitema: bool = False,
        autoconfianca: float | None = 0.9,
    ) -> VotoClassificador:
        """Cria um voto.

        Args:
            papel: Papel.
            tema_id: Tema escolhido ("" se falhou).
            ok: Voto válido.
            fora: Marca de fora.
            multitema: Marca de multitema.
            autoconfianca: Autoconfiança.

        Returns:
            Voto.
        """
        if not ok:
            return VotoClassificador.falha(papel, "teste", "modelo", "v1", "erro simulado")
        return VotoClassificador(
            papel,
            "teste",
            "modelo",
            "v1",
            True,
            "",
            tema_id,
            "",
            (),
            "núcleo",
            fora,
            multitema,
            autoconfianca,
            (tema_id,),
            False,
            0.0,
        )

    @staticmethod
    def veredito(veredito: Veredito, candidato: str, escolha: str, confianca: float = 0.9) -> VereditoVerificador:
        """Cria um veredito do verificador.

        Args:
            veredito: Relação da escolha com o candidato.
            candidato: Candidato conferido.
            escolha: Cartão escolhido.
            confianca: Confiança declarada.

        Returns:
            Veredito.
        """
        if veredito == "nao_rodou":
            return VereditoVerificador.nao_rodou("A e B em ramos diferentes")
        return VereditoVerificador(
            veredito,
            candidato,
            escolha,
            (candidato, escolha),
            "núcleo",
            "porque",
            confianca,
            "",
            "teste",
            "modelo",
            "v1",
            False,
            0.0,
        )

    def sinais(
        self,
        a: VotoClassificador,
        b: VotoClassificador,
        barato: VotoClassificador,
        verificador: VereditoVerificador,
        regras: Sequence[str] = (),
        questao_id: str = "Q1",
    ) -> SinaisQuestao:
        """Monta a linha de sinais de uma questão.

        Args:
            a: Voto do classificador A.
            b: Voto do classificador B.
            barato: Voto barato.
            verificador: Veredito.
            regras: Temas indicados pelas leis citadas.
            questao_id: ID.

        Returns:
            Sinais.
        """
        return SinaisQuestao(questao_id, (a, b, barato), (), tuple(regras), verificador)

    def simples(
        self,
        tema_a: str,
        tema_b: str,
        tema_barato: str,
        veredito: Veredito,
        candidato: str,
        escolha: str,
    ) -> SinaisQuestao:
        """Atalho: três votos válidos e um veredito.

        Args:
            tema_a: Tema de A.
            tema_b: Tema de B.
            tema_barato: Tema do voto barato.
            veredito: Veredito.
            candidato: Candidato conferido.
            escolha: Cartão escolhido pelo verificador.

        Returns:
            Sinais.
        """
        return self.sinais(
            self.voto("classificador_a", tema_a),
            self.voto("classificador_b", tema_b),
            self.voto("voto_barato", tema_barato),
            self.veredito(veredito, candidato, escolha),
        )
