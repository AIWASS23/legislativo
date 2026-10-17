"""Candidato consolidado, recuo para o pai e regras que forçam ``revisar`` (ADR-010, ADR-011, etapas 1 a 3).

A etapa 4 (limiar pela probabilidade calibrada, ADR-013) é aplicada depois, só às candidatas.
Os motivos são textos fixos, curtos e com IDs, para o professor entender sem abrir o código.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from typing import Literal

from vicio_ia.classificacao.respostas import SinaisQuestao, VereditoVerificador, VotoClassificador
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada

type AcaoPreliminar = Literal["candidata", "revisar", "fora"]
"""``candidata`` vai para o limiar calibrado; ``revisar`` e ``fora`` já estão decididas."""


class IndiceArvore:
    """Consultas de parentesco sobre a árvore preparada (a régua: mesmo nó, pai ou filho direto)."""

    def __init__(self, temas: Sequence[TemaPreparado]) -> None:
        """Indexa os nós.

        Args:
            temas: Árvore preparada.
        """
        self._temas: dict[str, TemaPreparado] = {tema.tema_id: tema for tema in temas}

    def tema(self, tema_id: str) -> TemaPreparado:
        """Busca um nó.

        Args:
            tema_id: ID.

        Returns:
            O nó.
        """
        return self._temas[tema_id]

    def mesmo_ramo(self, tema_a: str, tema_b: str) -> bool:
        """Mesmo nó, ou um é pai direto do outro.

        Args:
            tema_a: Um ID.
            tema_b: Outro ID.

        Returns:
            ``True`` se a régua aceitaria um pelo outro.
        """
        if tema_a == tema_b:
            return True
        if tema_a not in self._temas or tema_b not in self._temas:
            return False
        return self._temas[tema_a].parent_id == tema_b or self._temas[tema_b].parent_id == tema_a

    def pai_publicavel(self, tema_id: str) -> str:
        """Pai do nó, se for publicável (nunca a disciplina).

        Args:
            tema_id: ID.

        Returns:
            ID do pai, ou ``""``.
        """
        pai: str | None = self._temas[tema_id].parent_id
        if pai is None or pai not in self._temas or not self._temas[pai].publicavel:
            return ""
        return pai


@dataclass(frozen=True)
class DecisaoPreliminar:
    """Resultado das etapas 1 a 3 da política, com as variáveis da calibração.

    Attributes:
        id: ID da questão.
        acao: ``candidata``, ``revisar`` ou ``fora``.
        tema_id: Tema consolidado (em ``revisar``, a sugestão ao professor).
        nivel: Nível do tema (1 = tema, 2 = subtema).
        recuou: O tema é o pai do candidato preliminar (ADR-010).
        motivo: Motivo fixo de ``revisar`` ou ``fora`` ("" nas candidatas).
        extras_ids: Temas de outro ramo indicados por duas fontes ou mais (até 3), ou os
            subtemas candidatos de uma questão recuada.
        concordancia_ramo: Fontes (A, B, voto barato, regras) no ramo do tema: 0 a 4.
        fontes_no_ramo: Quais fontes estão no ramo do tema (papéis e ``regras``).
        veredito: Veredito do verificador.
        autoconfianca_media: Média da autoconfiança de A e B.
        lixeira: Nível de lixeira do tema.
        zona_risco: Lixeira, enunciado genérico ou jurisprudência.
        origem_mesmo_ramo: O assunto de origem cai no ramo do tema (sinal fraco, ADR-006).
        tipo_convencao: Tipo de risco de convenção do tema (ADR-005), para a margem da previsão.
    """

    id: str
    acao: AcaoPreliminar
    tema_id: str
    nivel: int
    recuou: bool
    motivo: str
    extras_ids: tuple[str, ...]
    concordancia_ramo: int
    fontes_no_ramo: tuple[str, ...]
    veredito: str
    autoconfianca_media: float | None
    lixeira: str
    zona_risco: bool
    origem_mesmo_ramo: bool
    tipo_convencao: str

    def como_dict(self) -> dict[str, object]:
        """Converte em dicionário serializável.

        Returns:
            Dicionário.
        """
        return asdict(self)


class AgregadorSinais:
    """Aplica as etapas 1 a 3 da ADR-011 e o recuo da ADR-010 aos sinais de uma questão."""

    def __init__(self, temas: Sequence[TemaPreparado]) -> None:
        """Indexa a árvore.

        Args:
            temas: Árvore preparada.
        """
        self._arvore: IndiceArvore = IndiceArvore(temas)

    def decidir(self, sinais: SinaisQuestao, questao: QuestaoPreparada, origem: Sequence[str]) -> DecisaoPreliminar:
        """Decide a ação preliminar de uma questão.

        Args:
            sinais: Votos, regras e veredito.
            questao: Questão preparada (marcas de enunciado genérico e jurisprudência).
            origem: Temas que casam com o assunto de origem (sinal fraco).

        Returns:
            Decisão preliminar.
        """
        a: VotoClassificador | None = self._valido(sinais.voto("classificador_a"))
        b: VotoClassificador | None = self._valido(sinais.voto("classificador_b"))
        verificador: VereditoVerificador = sinais.verificador
        if a is None or b is None:
            barato: VotoClassificador | None = self._valido(sinais.voto("voto_barato"))
            reserva: VotoClassificador | None = a or b or barato
            sugestao: str = reserva.tema_id if reserva is not None else ""
            return self._montar(sinais, questao, origem, "revisar", sugestao, False, "falha de classificação", ())
        if a.fora and b.fora and verificador.veredito == "nenhum":
            return self._montar(sinais, questao, origem, "fora", a.tema_id, False, "nenhum tema do recorte serve", ())
        if a.fora or b.fora or verificador.veredito == "nenhum":
            return self._montar(sinais, questao, origem, "revisar", a.tema_id, False, "possível fora do recorte", ())
        if not self._arvore.mesmo_ramo(a.tema_id, b.tema_id):
            return self._montar(
                sinais,
                questao,
                origem,
                "revisar",
                a.tema_id,
                False,
                f"dúvida entre {a.tema_id} e {b.tema_id}",
                (b.tema_id,),
            )
        candidato: str = verificador.candidato_id or a.tema_id
        tema: str = candidato
        recuou: bool = False
        subtemas: tuple[str, ...] = ()
        veredito: str = verificador.veredito
        if veredito in ("falha", "nao_rodou"):
            return self._montar(sinais, questao, origem, "revisar", candidato, False, "falha de classificação", ())
        if veredito == "outro":
            return self._montar(
                sinais,
                questao,
                origem,
                "revisar",
                candidato,
                False,
                f"verificador sugere {verificador.escolha_id}",
                (verificador.escolha_id,),
            )
        if veredito in ("pai", "irmao"):
            pai: str = self._arvore.pai_publicavel(candidato)
            if not pai:
                return self._montar(
                    sinais,
                    questao,
                    origem,
                    "revisar",
                    candidato,
                    False,
                    f"verificador sugere {verificador.escolha_id}",
                    (verificador.escolha_id,),
                )
            tema, recuou = pai, True
            subtemas = tuple(s for s in (candidato, verificador.escolha_id) if s and s != pai)
        elif veredito == "filho":
            subtemas = (verificador.escolha_id,)
        if self._arvore.tema(tema).lixeira == "forte" and not self._concordancia_total(sinais, tema, veredito):
            pai_lixeira: str = self._arvore.pai_publicavel(tema)
            if not pai_lixeira:
                return self._montar(
                    sinais, questao, origem, "revisar", tema, recuou, "tema genérico sem evidência suficiente", subtemas
                )
            subtemas = (tema, *subtemas)
            tema, recuou = pai_lixeira, True
        conflito: str = self._conflito_sobreposicao(sinais, tema)
        if conflito:
            return self._montar(
                sinais, questao, origem, "revisar", tema, recuou, f"sobreposição: {tema} × {conflito}", (conflito,)
            )
        if sum(1 for voto in (a, b) if voto.multitema) >= 2 and questao.marcas.enunciado_generico:
            extras: tuple[str, ...] = self._extras(sinais, tema)
            return self._montar(
                sinais,
                questao,
                origem,
                "revisar",
                tema,
                recuou,
                f"questão cobre vários temas: {'; '.join((tema, *extras))}",
                extras,
            )
        return self._montar(sinais, questao, origem, "candidata", tema, recuou, "", subtemas)

    @staticmethod
    def _valido(voto: VotoClassificador | None) -> VotoClassificador | None:
        """Descarta voto ausente ou inválido.

        Args:
            voto: Voto.

        Returns:
            O voto, se válido.
        """
        return voto if voto is not None and voto.ok and voto.tema_id else None

    def _concordancia_total(self, sinais: SinaisQuestao, tema: str, veredito: str) -> bool:
        """A, B e o voto barato no ramo do tema, e o verificador confirmou.

        Args:
            sinais: Sinais da questão.
            tema: Tema consolidado.
            veredito: Veredito do verificador.

        Returns:
            ``True`` se houver concordância total.
        """
        votos: list[VotoClassificador] = [v for v in sinais.votos if v.ok and v.tema_id]
        return (
            veredito == "confirma"
            and len(votos) == 3
            and all(self._arvore.mesmo_ramo(voto.tema_id, tema) for voto in votos)
        )

    def _conflito_sobreposicao(self, sinais: SinaisQuestao, tema: str) -> str:
        """Procura uma fonte que escolheu outro nó do mesmo grupo de sobreposição, fora do ramo.

        Args:
            sinais: Sinais da questão.
            tema: Tema consolidado.

        Returns:
            ID do nó em conflito, ou ``""``.
        """
        grupo: str = self._arvore.tema(tema).grupo_sobreposicao
        if not grupo:
            return ""
        escolhas: list[str] = [v.tema_id for v in sinais.votos if v.ok and v.tema_id]
        if sinais.verificador.escolha_id:
            escolhas.append(sinais.verificador.escolha_id)
        escolha: str
        for escolha in escolhas:
            try:
                outro: TemaPreparado = self._arvore.tema(escolha)
            except KeyError:
                continue
            if outro.grupo_sobreposicao == grupo and not self._arvore.mesmo_ramo(escolha, tema):
                return escolha
        return ""

    def _extras(self, sinais: SinaisQuestao, tema: str) -> tuple[str, ...]:
        """Temas de outro ramo indicados por duas fontes ou mais (até 3).

        Args:
            sinais: Sinais da questão.
            tema: Tema consolidado.

        Returns:
            IDs, do mais ao menos indicado; empates em ordem de ID, para o resultado não depender da
            ordem de iteração de conjuntos (que muda a cada execução do Python).
        """
        fontes: list[set[str]] = [set(v.extras_ids) | {v.tema_id, v.segundo_id} for v in sinais.votos if v.ok]
        fontes.append(set(sinais.regras))
        contagem: Counter[str] = Counter(item for fonte in fontes for item in fonte if item)
        ordenados: list[tuple[str, int]] = sorted(contagem.items(), key=lambda par: (-par[1], par[0]))
        return tuple(
            item for item, quantidade in ordenados if quantidade >= 2 and not self._arvore.mesmo_ramo(item, tema)
        )[:3]

    def _montar(
        self,
        sinais: SinaisQuestao,
        questao: QuestaoPreparada,
        origem: Sequence[str],
        acao: AcaoPreliminar,
        tema: str,
        recuou: bool,
        motivo: str,
        subtemas: Sequence[str],
    ) -> DecisaoPreliminar:
        """Monta a decisão com as variáveis da calibração.

        Args:
            sinais: Sinais da questão.
            questao: Questão preparada.
            origem: Temas do assunto de origem.
            acao: Ação preliminar.
            tema: Tema consolidado ou sugerido.
            recuou: Houve recuo para o pai.
            motivo: Motivo fixo.
            subtemas: Subtemas candidatos (recuo) ou extras específicos do motivo.

        Returns:
            Decisão preliminar.
        """
        no: TemaPreparado | None = self._arvore.tema(tema) if tema else None
        votos: list[VotoClassificador] = [v for v in sinais.votos if v.ok and v.tema_id]
        fontes: list[str] = [v.papel for v in votos if tema and self._arvore.mesmo_ramo(v.tema_id, tema)]
        if tema and any(self._arvore.mesmo_ramo(r, tema) for r in sinais.regras):
            fontes.append("regras")
        confiancas: list[float] = [
            v.autoconfianca
            for v in votos
            if v.papel in ("classificador_a", "classificador_b") and v.autoconfianca is not None
        ]
        extras: tuple[str, ...] = tuple(dict.fromkeys([*subtemas, *(self._extras(sinais, tema) if tema else ())]))
        return DecisaoPreliminar(
            id=sinais.id,
            acao=acao,
            tema_id=tema,
            nivel=no.nivel if no is not None else 0,
            recuou=recuou,
            motivo=motivo,
            extras_ids=tuple(e for e in extras if e and e != tema)[:3],
            concordancia_ramo=len(fontes),
            fontes_no_ramo=tuple(fontes),
            veredito=sinais.verificador.veredito,
            autoconfianca_media=round(sum(confiancas) / len(confiancas), 3) if confiancas else None,
            lixeira=no.lixeira if no is not None else "",
            zona_risco=(no is not None and no.lixeira != "")
            or questao.marcas.enunciado_generico
            or questao.marcas.menciona_jurisprudencia,
            origem_mesmo_ramo=bool(tema) and any(self._arvore.mesmo_ramo(o, tema) for o in origem),
            tipo_convencao=no.tipo_convencao if no is not None else "",
        )
