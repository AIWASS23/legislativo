"""Extração determinística das leis e dos artigos citados nas questões (ADR-021, decisão 3).

Só expressões regulares, sem modelo: o resultado é o mesmo em qualquer máquina. Um artigo citado recebe a
lei por um destes caminhos, nesta ordem:

1. **explícita:** a lei vem logo depois do artigo ("art. 155, § 4º, do CP") ou logo antes ("CP, art. 155");
2. **enumeração:** o artigo herda a lei do artigo seguinte da mesma enumeração ("art. 155, caput, c/c
   art. 14, II, ambos do CP");
3. **anáfora:** "do mesmo diploma", "da referida lei" e "do Códex" apontam para a última lei citada antes;
4. **repetição:** o mesmo número de artigo já apareceu na questão com a lei ("audiência do art. 16", depois
   de "art. 16 da Lei Maria da Penha");
5. **contexto:** a questão cita uma única lei, e o artigo sem lei fica com ela. A regra não vale quando a
   questão fala de uma lei sem nome ("arts. 74 e 75 da Lei"), porque essa lei pode ser outra.

O que sobra fica como pendente, com o trecho, para a conferência do autor. A resposta do autor fica em
``dados/conhecimento/citacoes_manuais.csv`` e é aplicada por cima da extração (resolução ``manual``). Nenhum
modelo de linguagem entra neste passo.
"""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, TextIO

from vicio_ia.leitura_json import CamposJSON


@dataclass(frozen=True)
class ArtigoCitado:
    """Artigo, ou intervalo de artigos, citado numa questão, já com a lei.

    Attributes:
        lei: Lei canônica (``CP``, ``CPP``, ``LEP``, ``CF``, ``CPM``, ``CPPM`` ou ``Lei 11.343/2006``).
        inicio: Primeiro artigo (o sufixo de letra, como em 147-A, é ignorado).
        fim: Último artigo (igual ao primeiro, exceto em intervalos como "arts. 158-A a 158-F").
        resolucao: ``explicita``, ``enumeracao``, ``anafora``, ``repeticao``, ``contexto`` ou ``manual``.
        trecho: Trecho da questão em volta da citação.
    """

    lei: str
    inicio: int
    fim: int
    resolucao: str
    trecho: str


@dataclass(frozen=True)
class CitacoesQuestao:
    """Leis e artigos citados numa questão.

    Attributes:
        id: ID da questão.
        leis: Leis citadas, com ou sem artigo, na ordem da primeira menção.
        artigos: Artigos com a lei resolvida.
        pendentes: Trechos de artigos cuja lei não foi resolvida.
    """

    id: str
    leis: tuple[str, ...]
    artigos: tuple[ArtigoCitado, ...]
    pendentes: tuple[str, ...]

    def como_dict(self) -> dict[str, object]:
        """Converte em dicionário serializável em JSON.

        Returns:
            Dicionário com listas no lugar das tuplas.
        """
        return {
            "id": self.id,
            "leis": list(self.leis),
            "artigos": [
                {"lei": a.lei, "inicio": a.inicio, "fim": a.fim, "resolucao": a.resolucao, "trecho": a.trecho}
                for a in self.artigos
            ],
            "pendentes": list(self.pendentes),
        }

    @classmethod
    def de_dict(cls, objeto: Mapping[str, object], origem: str) -> CitacoesQuestao:
        """Reconstrói as citações lidas do disco.

        Args:
            objeto: Linha decodificada.
            origem: Arquivo e linha (para mensagens de erro).

        Returns:
            Citações da questão.
        """
        campos: CamposJSON = CamposJSON(objeto, origem)
        artigos: list[ArtigoCitado] = []
        item: dict[str, object]
        for item in campos.objetos("artigos"):
            artigo: CamposJSON = CamposJSON(item, f"{origem}, artigos")
            artigos.append(
                ArtigoCitado(
                    lei=artigo.texto("lei"),
                    inicio=artigo.inteiro("inicio"),
                    fim=artigo.inteiro("fim"),
                    resolucao=artigo.texto("resolucao"),
                    trecho=artigo.texto("trecho"),
                )
            )
        return cls(
            id=campos.texto("id"),
            leis=campos.textos("leis"),
            artigos=tuple(artigos),
            pendentes=campos.textos("pendentes"),
        )


@dataclass(frozen=True)
class _Mencao:
    """Lei mencionada no texto.

    Attributes:
        inicio: Posição inicial no texto.
        fim: Posição final.
        lei: Lei canônica; vazio numa anáfora ("do mesmo diploma"); ``?`` numa lei sem nome ("da Lei,").
    """

    inicio: int
    fim: int
    lei: str


@dataclass(frozen=True)
class _Intervalo:
    """Artigos de uma menção, antes de resolver a lei.

    Attributes:
        inicio: Primeiro artigo.
        fim: Último artigo.
    """

    inicio: int
    fim: int


@dataclass
class _MencaoArtigo:
    """Menção a artigos ("arts. 74 e 75"), com a lei, quando já resolvida.

    Attributes:
        inicio: Posição inicial no texto.
        fim: Posição final.
        intervalos: Artigos citados.
        lei: Lei resolvida; vazio enquanto não houver.
        resolucao: Como a lei foi resolvida; ``sem_nome`` bloqueia as outras regras ("da Lei,").
    """

    inicio: int
    fim: int
    intervalos: tuple[_Intervalo, ...]
    lei: str = ""
    resolucao: str = ""


class ExtratorCitacoes:
    """Acha as leis e os artigos citados num texto de questão."""

    ANOS: ClassVar[dict[str, str]] = {
        "1521": "1951",
        "2889": "1956",
        "3688": "1941",
        "4737": "1965",
        "7492": "1986",
        "7716": "1989",
        "8069": "1990",
        "8072": "1990",
        "8078": "1990",
        "8137": "1990",
        "9099": "1995",
        "9296": "1996",
        "9455": "1997",
        "9503": "1997",
        "9605": "1998",
        "9609": "1998",
        "9613": "1998",
        "10741": "2003",
        "10826": "2003",
        "11105": "2005",
        "11340": "2006",
        "11343": "2006",
        "12037": "2009",
        "12830": "2013",
        "12850": "2013",
        "13260": "2016",
        "13869": "2019",
        "13964": "2019",
        "14133": "2021",
        "14597": "2023",
    }
    """Ano das leis do recorte, para a forma canônica quando a questão cita só o número."""

    CODIGOS_POR_NUMERO: ClassVar[dict[str, str]] = {
        "2848": "CP",
        "3689": "CPP",
        "7210": "LEP",
        "1001": "CPM",
        "1002": "CPPM",
    }
    APELIDOS: ClassVar[dict[str, str]] = {
        "codigo penal militar": "CPM",
        "cpm": "CPM",
        "codigo de processo penal militar": "CPPM",
        "cppm": "CPPM",
        "codigo penal": "CP",
        "cp": "CP",
        "estatuto repressivo": "CP",
        "diploma repressivo": "CP",
        "diploma criminal": "CP",
        "diploma penal": "CP",
        "codigo de processo penal": "CPP",
        "codigo processual penal": "CPP",
        "cpp": "CPP",
        "estatuto processual penal": "CPP",
        "estatuto processual": "CPP",
        "diploma processual penal": "CPP",
        "diploma processual": "CPP",
        "lei de execucao penal": "LEP",
        "lei de execucoes penais": "LEP",
        "lei das execucoes penais": "LEP",
        "lep": "LEP",
        "constituicao federal": "CF",
        "constituicao da republica": "CF",
        "constituicao": "CF",
        "carta magna": "CF",
        "carta constitucional": "CF",
        "texto constitucional": "CF",
        "cf": "CF",
        "crfb": "CF",
        "crf": "CF",
        "lei maria da penha": "Lei 11.340/2006",
        "maria da penha": "Lei 11.340/2006",
        "lei de drogas": "Lei 11.343/2006",
        "lei antidrogas": "Lei 11.343/2006",
        "lei de toxicos": "Lei 11.343/2006",
        "lei de entorpecentes": "Lei 11.343/2006",
        "lei dos juizados especiais": "Lei 9.099/1995",
        "lei de crimes ambientais": "Lei 9.605/1998",
        "lei dos crimes ambientais": "Lei 9.605/1998",
        "lei de lavagem de dinheiro": "Lei 9.613/1998",
        "lei de lavagem de capitais": "Lei 9.613/1998",
        "lei de lavagem": "Lei 9.613/1998",
        "lei de abuso de autoridade": "Lei 13.869/2019",
        "lei do abuso de autoridade": "Lei 13.869/2019",
        "estatuto do desarmamento": "Lei 10.826/2003",
        "lei das organizacoes criminosas": "Lei 12.850/2013",
        "lei de organizacoes criminosas": "Lei 12.850/2013",
        "lei do crime organizado": "Lei 12.850/2013",
        "lei dos crimes hediondos": "Lei 8.072/1990",
        "lei de crimes hediondos": "Lei 8.072/1990",
        "lei de tortura": "Lei 9.455/1997",
        "lei da tortura": "Lei 9.455/1997",
        "lei antiterrorismo": "Lei 13.260/2016",
        "estatuto da crianca e do adolescente": "Lei 8.069/1990",
        "eca": "Lei 8.069/1990",
        "estatuto do idoso": "Lei 10.741/2003",
        "estatuto da pessoa idosa": "Lei 10.741/2003",
        "lei de interceptacao telefonica": "Lei 9.296/1996",
        "lei de identificacao criminal": "Lei 12.037/2009",
        "lei do racismo": "Lei 7.716/1989",
        "codigo eleitoral": "Lei 4.737/1965",
        "codigo de transito brasileiro": "Lei 9.503/1997",
        "codigo de transito": "Lei 9.503/1997",
        "ctb": "Lei 9.503/1997",
        "codigo de defesa do consumidor": "Lei 8.078/1990",
        "cdc": "Lei 8.078/1990",
        "lei das contravencoes penais": "Lei 3.688/1941",
        "lei de contravencoes penais": "Lei 3.688/1941",
        "lcp": "Lei 3.688/1941",
        "pacote anticrime": "Lei 13.964/2019",
        "lei anticrime": "Lei 13.964/2019",
        "lei geral do esporte": "Lei 14.597/2023",
        "lei de licitacoes": "Lei 14.133/2021",
    }
    """Nomes e siglas de leis, na forma dobrada (minúsculas, sem acento)."""

    ANAFORAS: ClassVar[tuple[str, ...]] = (
        r"mesmo\s+diploma",
        r"mesmo\s+codigo",
        r"mesmo\s+estatuto",
        r"mesma\s+lei",
        r"referid[oa]\s+(?:diploma|lei|codigo)",
        r"citad[oa]\s+(?:diploma|lei|codigo)",
        r"aludid[oa]\s+(?:diploma|lei|codigo)",
        r"diploma\s+legal",
        r"codex",
    )
    """Expressões que remetem à última lei citada antes."""

    SEM_NOME: ClassVar[str] = "?"
    _RE_LEI_SEM_NOME: ClassVar[re.Pattern[str]] = re.compile(r"\blei\b(?=\s*[,.;:)])")

    CONECTORES: ClassVar[frozenset[str]] = frozenset(
        {
            "caput",
            "paragrafo",
            "paragrafos",
            "unico",
            "inciso",
            "incisos",
            "alinea",
            "alineas",
            "item",
            "itens",
            "e",
            "c",
            "ambos",
            "todos",
            "do",
            "da",
            "dos",
            "das",
            "de",
            "no",
            "na",
            "nos",
            "nas",
            "parte",
            "final",
            "inicial",
            "primeira",
            "primeiro",
            "segundo",
            "terceiro",
            "quarto",
            "quinto",
            "sexto",
            "seguintes",
            "ss",
            "combinado",
            "com",
            "respectivamente",
            "referido",
            "referida",
            "citado",
            "citada",
            "mencionado",
            "mencionada",
            "aludido",
            "aludida",
        }
    )
    """Palavras aceitas entre o artigo e a lei ("art. 155, § 4º, inciso I, do CP")."""

    JANELA_DEPOIS: ClassVar[int] = 120
    JANELA_ANTES: ClassVar[int] = 40
    JANELA_TRECHO: ClassVar[int] = 50

    _NUM: ClassVar[str] = r"\d{1,4}(?:\s?[o°](?![a-z]))?(?:\s*-\s*[a-z](?![a-z]))?"
    _SEPARADOR: ClassVar[str] = r"(?:\s*,\s*(?:caput\s*,\s*)?(?:e\s+)?|\s+e\s+|\s+a\s+|\s+ate\s+|\s+ao\s+)"
    _RE_ARTIGO: ClassVar[re.Pattern[str]] = re.compile(
        rf"\b(?:arts?\.?|artigos?)\s*(?:n\s*[o°.]*\s*)?(?P<lista>{_NUM}(?:{_SEPARADOR}{_NUM})*)"
    )
    _RE_ITEM_LISTA: ClassVar[re.Pattern[str]] = re.compile(rf"(?P<num>\d{{1,4}})[^\d]*?(?P<sep>{_SEPARADOR})?(?=\d|$)")
    _RE_LEI_NUMERO: ClassVar[re.Pattern[str]] = re.compile(
        r"\b(?:lei|decreto[\s-]*lei)(?:\s+(?:federal|complementar|ordinaria))?\s*(?:n\s*[o°.]*\s*)?"
        r"(?P<numero>\d{1,2}\.?\d{3})(?!\d)"
        r"(?:\s*/\s*(?P<ano>\d{4}|\d{2})(?!\d)|,?\s+de\s+\d{1,2}\s*o?\s+de\s+[a-z]+\s+de\s+(?P<ano_extenso>\d{4}))?"
    )
    _RE_PARENTESES: ClassVar[re.Pattern[str]] = re.compile(r"\([^()]{0,100}\)")
    _RE_PALAVRA: ClassVar[re.Pattern[str]] = re.compile(r"[a-z0-9]+")
    _RE_ORDINAL: ClassVar[re.Pattern[str]] = re.compile(r"\d+[a-z]?")
    _RE_ROMANO: ClassVar[re.Pattern[str]] = re.compile(r"l?x{0,3}(?:ix|iv|v?i{0,3})")
    _RE_FIM_DE_FRASE: ClassVar[re.Pattern[str]] = re.compile(r"[.!?]\s")
    _RE_BRANCOS: ClassVar[re.Pattern[str]] = re.compile(r"\s+")

    def __init__(self) -> None:
        """Compila as expressões dos apelidos e das anáforas, da mais longa para a mais curta."""
        apelidos: list[str] = sorted(self.APELIDOS, key=len, reverse=True)
        self._re_apelido: re.Pattern[str] = re.compile(
            r"\b(" + "|".join(r"\s+".join(map(re.escape, a.split())) for a in apelidos) + r")\b"
        )
        self._re_anafora: re.Pattern[str] = re.compile(r"\b(?:" + "|".join(self.ANAFORAS) + r")\b")

    @staticmethod
    def dobrar(texto: str) -> str:
        """Minúsculas e sem acento, com o mesmo tamanho do texto (as posições continuam valendo).

        Args:
            texto: Texto original.

        Returns:
            Texto dobrado, caractere a caractere.
        """
        caractere: str
        saida: list[str] = []
        for caractere in texto:
            base: str = unicodedata.normalize("NFKD", caractere)[:1] or caractere
            saida.append(base.lower()[:1] or base)
        return "".join(saida)

    def extrair(self, questao_id: str, texto: str) -> CitacoesQuestao:
        """Acha as leis e os artigos citados.

        Args:
            questao_id: ID da questão.
            texto: Enunciado, comando e alternativas.

        Returns:
            Citações da questão.
        """
        dobrado: str = self.dobrar(texto)
        mencoes: list[_Mencao] = self._mencoes_lei(dobrado)
        artigos: list[_MencaoArtigo] = self._mencoes_artigo(dobrado)
        self._resolver(dobrado, mencoes, artigos)
        leis: list[str] = []
        mencao: _Mencao
        for mencao in mencoes:
            if mencao.lei and mencao.lei != self.SEM_NOME and mencao.lei not in leis:
                leis.append(mencao.lei)
        citados: list[ArtigoCitado] = []
        pendentes: list[str] = []
        artigo: _MencaoArtigo
        for artigo in artigos:
            trecho: str = self._trecho(texto, artigo.inicio, artigo.fim)
            if not artigo.lei:
                pendentes.append(trecho)
                continue
            intervalo: _Intervalo
            for intervalo in artigo.intervalos:
                citados.append(ArtigoCitado(artigo.lei, intervalo.inicio, intervalo.fim, artigo.resolucao, trecho))
        return CitacoesQuestao(questao_id, tuple(leis), tuple(citados), tuple(pendentes))

    def _mencoes_lei(self, dobrado: str) -> list[_Mencao]:
        """Leis mencionadas, pelo número, pelo nome ou por anáfora, sem sobreposição.

        Args:
            dobrado: Texto dobrado.

        Returns:
            Menções em ordem de posição.
        """
        candidatas: list[_Mencao] = []
        achado: re.Match[str]
        for achado in self._RE_LEI_NUMERO.finditer(dobrado):
            ano: str | None = achado.group("ano") or achado.group("ano_extenso")
            candidatas.append(_Mencao(achado.start(), achado.end(), self._lei_por_numero(achado.group("numero"), ano)))
        for achado in self._re_apelido.finditer(dobrado):
            candidatas.append(
                _Mencao(achado.start(), achado.end(), self.APELIDOS[self._RE_BRANCOS.sub(" ", achado.group(1))])
            )
        for achado in self._re_anafora.finditer(dobrado):
            candidatas.append(_Mencao(achado.start(), achado.end(), ""))
        for achado in self._RE_LEI_SEM_NOME.finditer(dobrado):
            candidatas.append(_Mencao(achado.start(), achado.end(), self.SEM_NOME))
        candidatas.sort(key=lambda m: (m.inicio, -(m.fim - m.inicio)))
        mencoes: list[_Mencao] = []
        candidata: _Mencao
        for candidata in candidatas:
            if not mencoes or candidata.inicio >= mencoes[-1].fim:
                mencoes.append(candidata)
        return mencoes

    def _lei_por_numero(self, numero_bruto: str, ano: str | None) -> str:
        """Forma canônica de uma lei citada pelo número.

        Args:
            numero_bruto: Número como está no texto (``11.343``).
            ano: Ano com 2 ou 4 dígitos, se houver.

        Returns:
            ``CP``, ``CPP``, ``LEP``, ``CPM``, ``CPPM`` ou ``Lei 11.343/2006`` (sem o ano, se desconhecido).
        """
        numero: str = numero_bruto.replace(".", "")
        if numero in self.CODIGOS_POR_NUMERO:
            return self.CODIGOS_POR_NUMERO[numero]
        if ano is not None and len(ano) == 2:
            ano = ("19" if int(ano) > 30 else "20") + ano
        ano_final: str | None = ano or self.ANOS.get(numero)
        formatado: str = f"{int(numero):,}".replace(",", ".")
        return f"Lei {formatado}/{ano_final}" if ano_final else f"Lei {formatado}"

    def _mencoes_artigo(self, dobrado: str) -> list[_MencaoArtigo]:
        """Menções a artigos, com os números e os intervalos.

        Args:
            dobrado: Texto dobrado.

        Returns:
            Menções em ordem de posição.
        """
        mencoes: list[_MencaoArtigo] = []
        achado: re.Match[str]
        for achado in self._RE_ARTIGO.finditer(dobrado):
            intervalos: list[_Intervalo] = []
            em_intervalo: bool = False
            item: re.Match[str]
            for item in self._RE_ITEM_LISTA.finditer(achado.group("lista")):
                numero: int = int(item.group("num"))
                if em_intervalo and intervalos:
                    anterior: _Intervalo = intervalos[-1]
                    intervalos[-1] = _Intervalo(anterior.inicio, max(anterior.inicio, numero))
                else:
                    intervalos.append(_Intervalo(numero, numero))
                separador: str = (item.group("sep") or "").strip(" ,")
                em_intervalo = separador in {"a", "ate", "ao"}
            if intervalos:
                mencoes.append(_MencaoArtigo(achado.start(), achado.end(), tuple(intervalos)))
        return mencoes

    def _resolver(self, dobrado: str, mencoes: Sequence[_Mencao], artigos: Sequence[_MencaoArtigo]) -> None:
        """Dá a lei a cada menção a artigo, pelos cinco caminhos, em ordem.

        Args:
            dobrado: Texto dobrado.
            mencoes: Leis mencionadas.
            artigos: Menções a artigos (alteradas no lugar).
        """
        indice: int
        artigo: _MencaoArtigo
        for indice, artigo in enumerate(artigos):
            limite: int = artigos[indice + 1].inicio if indice + 1 < len(artigos) else len(dobrado)
            depois: _Mencao | None = self._lei_depois(dobrado, artigo, mencoes, limite)
            if depois is not None:
                self._atribuir(artigo, depois, mencoes, "explicita")
        self._enumeracoes(dobrado, artigos)
        for indice, artigo in enumerate(artigos):
            if artigo.lei or artigo.resolucao:
                continue
            piso: int = artigos[indice - 1].fim if indice > 0 else 0
            antes: _Mencao | None = self._lei_antes(dobrado, artigo, mencoes, piso)
            if antes is not None:
                self._atribuir(artigo, antes, mencoes, "explicita")
        self._enumeracoes(dobrado, artigos)
        self._repeticoes(artigos)
        unicas: set[str] = {m.lei for m in mencoes if m.lei}
        if len(unicas) == 1 and self.SEM_NOME not in unicas:
            lei_unica: str = next(iter(unicas))
            for artigo in artigos:
                if not artigo.lei and not artigo.resolucao:
                    artigo.lei = lei_unica
                    artigo.resolucao = "contexto"

    def _lei_depois(
        self, dobrado: str, artigo: _MencaoArtigo, mencoes: Sequence[_Mencao], limite: int
    ) -> _Mencao | None:
        """Lei logo depois do artigo, separada só por parágrafos, incisos e conectores.

        Args:
            dobrado: Texto dobrado.
            artigo: Menção a artigo.
            mencoes: Leis mencionadas.
            limite: Início da próxima menção a artigo.

        Returns:
            A menção à lei, ou ``None``.
        """
        mencao: _Mencao
        for mencao in mencoes:
            if mencao.inicio < artigo.fim:
                continue
            if mencao.inicio > min(limite, artigo.fim + self.JANELA_DEPOIS):
                return None
            vao: str = dobrado[artigo.fim : mencao.inicio]
            return mencao if self._so_conectores(vao) and not self._RE_FIM_DE_FRASE.search(vao) else None
        return None

    def _lei_antes(self, dobrado: str, artigo: _MencaoArtigo, mencoes: Sequence[_Mencao], piso: int) -> _Mencao | None:
        """Lei logo antes do artigo, na mesma frase ("CP, art. 155"; "o Código Penal, em seu art. 59").

        Args:
            dobrado: Texto dobrado.
            artigo: Menção a artigo.
            mencoes: Leis mencionadas.
            piso: Fim da menção a artigo anterior.

        Returns:
            A menção à lei, ou ``None``.
        """
        anteriores: list[_Mencao] = [m for m in mencoes if piso <= m.inicio and m.fim <= artigo.inicio]
        if not anteriores:
            return None
        mencao: _Mencao = anteriores[-1]
        vao: str = dobrado[mencao.fim : artigo.inicio]
        if len(vao) > self.JANELA_ANTES or self._RE_FIM_DE_FRASE.search(vao):
            return None
        return mencao

    def _enumeracoes(self, dobrado: str, artigos: Sequence[_MencaoArtigo]) -> None:
        """Propaga a lei de trás para a frente dentro de uma enumeração de artigos.

        Args:
            dobrado: Texto dobrado.
            artigos: Menções a artigos (alteradas no lugar).
        """
        indice: int
        for indice in range(len(artigos) - 2, -1, -1):
            atual: _MencaoArtigo = artigos[indice]
            seguinte: _MencaoArtigo = artigos[indice + 1]
            if atual.lei or atual.resolucao or not seguinte.lei:
                continue
            vao: str = dobrado[atual.fim : seguinte.inicio].replace(";", ",").replace("/", " ")
            if len(vao) <= self.JANELA_DEPOIS and self._so_conectores(vao):
                atual.lei = seguinte.lei
                atual.resolucao = "enumeracao"

    @staticmethod
    def _repeticoes(artigos: Sequence[_MencaoArtigo]) -> None:
        """Dá ao artigo sem lei a lei do mesmo número citado em outro ponto da questão, se for uma só.

        Args:
            artigos: Menções a artigos (alteradas no lugar).
        """
        leis_por_numero: dict[int, set[str]] = {}
        artigo: _MencaoArtigo
        intervalo: _Intervalo
        for artigo in artigos:
            if artigo.lei:
                for intervalo in artigo.intervalos:
                    leis_por_numero.setdefault(intervalo.inicio, set()).add(artigo.lei)
        for artigo in artigos:
            if artigo.lei or artigo.resolucao:
                continue
            leis: set[str] = set().union(*(leis_por_numero.get(i.inicio, set()) for i in artigo.intervalos))
            if len(leis) == 1:
                artigo.lei = next(iter(leis))
                artigo.resolucao = "repeticao"

    def _atribuir(self, artigo: _MencaoArtigo, mencao: _Mencao, mencoes: Sequence[_Mencao], forma: str) -> None:
        """Atribui a lei de uma menção ao artigo, resolvendo a anáfora pela última lei citada antes dela.

        Args:
            artigo: Menção a artigo (alterada no lugar).
            mencao: Menção à lei.
            mencoes: Todas as menções.
            forma: Resolução quando a menção não é anáfora.
        """
        if mencao.lei == self.SEM_NOME:
            artigo.resolucao = "sem_nome"
            return
        if mencao.lei:
            artigo.lei = mencao.lei
            artigo.resolucao = forma
            return
        anteriores: list[str] = [m.lei for m in mencoes if m.lei and m.lei != self.SEM_NOME and m.fim <= mencao.inicio]
        if anteriores:
            artigo.lei = anteriores[-1]
            artigo.resolucao = "anafora"

    def _so_conectores(self, vao: str) -> bool:
        """Diz se o trecho entre o artigo e a lei só tem parágrafos, incisos, alíneas e conectores.

        Args:
            vao: Trecho dobrado.

        Returns:
            ``True`` se só houver conectores (parênteses curtos são ignorados).
        """
        anterior: str = ""
        while anterior != vao:
            anterior, vao = vao, self._RE_PARENTESES.sub(" ", vao)
        palavra: str
        for palavra in self._RE_PALAVRA.findall(vao):
            if palavra in self.CONECTORES or len(palavra) == 1:
                continue
            if self._RE_ORDINAL.fullmatch(palavra) or self._RE_ROMANO.fullmatch(palavra):
                continue
            return False
        return True

    def _trecho(self, texto: str, inicio: int, fim: int) -> str:
        """Trecho do texto original em volta de uma menção, numa linha.

        Args:
            texto: Texto original.
            inicio: Início da menção.
            fim: Fim da menção.

        Returns:
            Trecho com reticências nas pontas cortadas.
        """
        de: int = max(0, inicio - self.JANELA_TRECHO)
        ate: int = min(len(texto), fim + self.JANELA_TRECHO)
        miolo: str = self._RE_BRANCOS.sub(" ", texto[de:ate]).strip()
        return ("…" if de > 0 else "") + miolo + ("…" if ate < len(texto) else "")


class ArquivoCitacoes:
    """Lê e grava ``dados/conhecimento/citacoes.jsonl`` (uma linha por questão, em ordem de ID)."""

    def __init__(self, caminho: Path) -> None:
        """Define o arquivo.

        Args:
            caminho: Arquivo JSONL.
        """
        self._caminho: Path = caminho

    def gravar(self, citacoes: Iterable[CitacoesQuestao]) -> Path:
        """Grava as citações.

        Args:
            citacoes: Citações por questão.

        Returns:
            O caminho gravado.
        """
        self._caminho.parent.mkdir(parents=True, exist_ok=True)
        arquivo: TextIO
        with self._caminho.open("w", encoding="utf-8") as arquivo:
            citacao: CitacoesQuestao
            for citacao in sorted(citacoes, key=lambda c: c.id):
                arquivo.write(json.dumps(citacao.como_dict(), ensure_ascii=False) + "\n")
        return self._caminho

    def ler(self) -> dict[str, CitacoesQuestao]:
        """Lê as citações.

        Returns:
            Citações por ID da questão.
        """
        citacoes: dict[str, CitacoesQuestao] = {}
        numero: int
        linha: str
        for numero, linha in enumerate(self._caminho.read_text(encoding="utf-8").splitlines(), start=1):
            if linha.strip():
                objeto: object = json.loads(linha)
                if isinstance(objeto, dict):
                    citacao: CitacoesQuestao = CitacoesQuestao.de_dict(objeto, f"{self._caminho.name}:{numero}")
                    citacoes[citacao.id] = citacao
        return citacoes


@dataclass(frozen=True)
class CorrecaoCitacao:
    """Artigo de uma questão resolvido à mão pelo autor (um pendente da extração).

    Attributes:
        id: ID da questão.
        lei: Lei canônica.
        inicio: Primeiro artigo.
        fim: Último artigo.
    """

    id: str
    lei: str
    inicio: int
    fim: int


class CorrecoesCitacoes:
    """Lê ``dados/conhecimento/citacoes_manuais.csv`` e aplica as correções às citações extraídas.

    Uma questão listada no arquivo tem os artigos corrigidos acrescentados e os pendentes resolvidos: o autor
    responde por todos os pendentes da questão.
    """

    COLUNAS: ClassVar[tuple[str, ...]] = ("id", "lei", "art_inicio", "art_fim")

    def __init__(self, caminho: Path) -> None:
        """Define o arquivo.

        Args:
            caminho: CSV de correções.
        """
        self._caminho: Path = caminho

    def ler(self) -> list[CorrecaoCitacao]:
        """Lê as correções.

        Returns:
            Correções, na ordem do arquivo (vazio se o arquivo não existir).

        Raises:
            ValueError: Se faltar coluna ou o intervalo for inválido.
        """
        if not self._caminho.is_file():
            return []
        arquivo: TextIO
        with self._caminho.open(encoding="utf-8", newline="") as arquivo:
            leitor: csv.DictReader[str] = csv.DictReader(arquivo)
            if tuple(leitor.fieldnames or ())[: len(self.COLUNAS)] != self.COLUNAS:
                raise ValueError(f"{self._caminho.name}: colunas esperadas {', '.join(self.COLUNAS)}")
            correcoes: list[CorrecaoCitacao] = []
            linha: dict[str, str]
            for linha in leitor:
                inicio: int = int(linha["art_inicio"])
                fim: int = int(linha["art_fim"])
                if fim < inicio:
                    raise ValueError(f"{self._caminho.name}: intervalo invertido em {linha['id']}")
                correcoes.append(CorrecaoCitacao(linha["id"], linha["lei"], inicio, fim))
        return correcoes

    @staticmethod
    def aplicar(citacoes: Sequence[CitacoesQuestao], correcoes: Sequence[CorrecaoCitacao]) -> list[CitacoesQuestao]:
        """Acrescenta os artigos corrigidos e resolve os pendentes das questões corrigidas.

        Args:
            citacoes: Citações extraídas.
            correcoes: Correções do autor.

        Returns:
            Citações com as correções aplicadas, na mesma ordem.

        Raises:
            ValueError: Se uma correção citar uma questão sem pendentes.
        """
        por_questao: dict[str, list[CorrecaoCitacao]] = {}
        correcao: CorrecaoCitacao
        for correcao in correcoes:
            por_questao.setdefault(correcao.id, []).append(correcao)
        saida: list[CitacoesQuestao] = []
        citacao: CitacoesQuestao
        for citacao in citacoes:
            novas: list[CorrecaoCitacao] = por_questao.pop(citacao.id, [])
            if not novas:
                saida.append(citacao)
                continue
            if not citacao.pendentes:
                raise ValueError(f"correção manual para {citacao.id}, que não tem pendentes")
            artigos: list[ArtigoCitado] = list(citacao.artigos)
            leis: list[str] = list(citacao.leis)
            for correcao in novas:
                trecho: str = next((t for t in citacao.pendentes if str(correcao.inicio) in t), citacao.pendentes[0])
                artigos.append(ArtigoCitado(correcao.lei, correcao.inicio, correcao.fim, "manual", trecho))
                if correcao.lei not in leis:
                    leis.append(correcao.lei)
            saida.append(CitacoesQuestao(citacao.id, tuple(leis), tuple(artigos), ()))
        if por_questao:
            raise ValueError(f"correção manual para questões inexistentes: {', '.join(sorted(por_questao))}")
        return saida
