"""Perfil de cada questão: formato, tamanho, ruído, origem e pistas legislativas."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import ClassVar, Literal

from vicio_ia.configuracao import ParametrosEDA
from vicio_ia.conhecimento import MapaLegislacao
from vicio_ia.dominio import Questao
from vicio_ia.relatorio import RegistroTabular
from vicio_ia.texto import ProcessadorTexto

type FormatoQuestao = Literal["multipla_escolha_5", "multipla_escolha_4", "certo_errado", "outro"]
"""Formato da questão, deduzido das chaves e textos das alternativas."""

type TipoComando = Literal["vazio", "repete_enunciado", "suspeito", "util"]
"""Classificação do campo ``comando``.

* ``vazio``: ausente, em branco ou só HTML.
* ``repete_enunciado``: copia o começo do enunciado (ou vice-versa).
* ``suspeito``: pede algo que não cabe em questão objetiva ("Explique...",
  "Complete a frase...") e parece gerado por outra ferramenta.
* ``util``: comando normal ("Assinale a alternativa correta").
"""


@dataclass(frozen=True)
class PerfilQuestao(RegistroTabular):
    """Características calculadas de uma questão.

    Attributes:
        id: ID da questão.
        formato: Formato deduzido das alternativas.
        n_alternativas: Número de alternativas.
        chars_enunciado: Caracteres do enunciado limpo.
        chars_comando: Caracteres do comando limpo.
        chars_alternativas: Soma dos caracteres das alternativas limpas.
        chars_total: Soma dos três anteriores.
        chars_brutos: Caracteres do HTML original (enunciado, comando e alternativas).
        html_de_editor: Algum campo tem marcação colada de editor (Word).
        palavras_conteudo_enunciado: Palavras do enunciado fora das frases-padrão.
        enunciado_curto: Enunciado abaixo do limiar de caracteres.
        enunciado_generico: Enunciado sem conteúdo temático (assunto está nas alternativas).
        tipo_comando: Classificação do comando.
        comando_so_html: Comando que só tinha HTML (ex.: ``<br>``).
        tags_html: Tags HTML distintas encontradas em qualquer campo.
        alternativas_com_html: Alternativas que contêm HTML ou entidades.
        alternativas_com_quebra: Alternativas com quebra de linha no meio do texto.
        entidades_html: Total de entidades HTML (``&nbsp;``...).
        disciplina_origem: Disciplina de origem, como veio.
        disciplina_normalizada: Disciplina da árvore correspondente ("" se fora do recorte).
        origem_no_recorte: Disciplina de origem corresponde a uma disciplina da árvore.
        assunto_origem: Assunto de origem, como veio.
        assunto_sem_parte: Assunto sem o marcador "(Parte N)".
        assunto_tem_parte: Assunto tem o marcador "(Parte N)".
        assunto_multiplo: Assunto lista mais de um tópico (separados por vírgula).
        leis_citadas: Números das leis citadas por número ou apelido.
        menciona_cp: Cita o Código Penal.
        menciona_cpp: Cita o Código de Processo Penal.
        menciona_cf: Cita a Constituição.
        menciona_jurisprudencia: Cita STF, STJ, súmula ou jurisprudência.
        hash_enunciado: Hash do enunciado normalizado.
        hash_completo: Hash do enunciado mais alternativas, normalizados.
    """

    id: str
    formato: FormatoQuestao
    n_alternativas: int
    chars_enunciado: int
    chars_comando: int
    chars_alternativas: int
    chars_total: int
    chars_brutos: int
    html_de_editor: bool
    palavras_conteudo_enunciado: int
    enunciado_curto: bool
    enunciado_generico: bool
    tipo_comando: TipoComando
    comando_so_html: bool
    tags_html: tuple[str, ...]
    alternativas_com_html: int
    alternativas_com_quebra: int
    entidades_html: int
    disciplina_origem: str
    disciplina_normalizada: str
    origem_no_recorte: bool
    assunto_origem: str
    assunto_sem_parte: str
    assunto_tem_parte: bool
    assunto_multiplo: bool
    leis_citadas: tuple[str, ...]
    menciona_cp: bool
    menciona_cpp: bool
    menciona_cf: bool
    menciona_jurisprudencia: bool
    hash_enunciado: str
    hash_completo: str


@dataclass(frozen=True)
class TextoLimpo:
    """Campos de uma questão já convertidos de HTML para texto.

    Attributes:
        enunciado: Enunciado limpo.
        comando: Comando limpo.
        alternativas: Letra -> alternativa limpa, em uma linha.
    """

    enunciado: str
    comando: str
    alternativas: Mapping[str, str]

    @property
    def completo(self) -> str:
        """Enunciado, comando e alternativas juntos, para buscas no texto."""
        return "\n".join([self.enunciado, self.comando, *self.alternativas.values()])


class PerfiladorQuestoes:
    """Calcula o :class:`PerfilQuestao` de cada questão."""

    _RE_CP: ClassVar[re.Pattern[str]] = re.compile(r"\bCP\b|\b[Cc][óo]digo [Pp]enal\b")
    _RE_CPP: ClassVar[re.Pattern[str]] = re.compile(r"\bCPP\b|\b[Cc][óo]digo de [Pp]rocesso [Pp]enal\b")
    _RE_CF: ClassVar[re.Pattern[str]] = re.compile(r"\bCF(?:/88)?\b|\bCRFB\b|\b[Cc]onstitui[çc][ãa]o\b")

    def __init__(self, parametros: ParametrosEDA, processador: ProcessadorTexto, legislacao: MapaLegislacao) -> None:
        """Recebe as dependências.

        Args:
            parametros: Limiares e listas da EDA.
            processador: Limpeza e normalização de texto.
            legislacao: Catálogo de leis.
        """
        self._parametros: ParametrosEDA = parametros
        self._processador: ProcessadorTexto = processador
        self._legislacao: MapaLegislacao = legislacao

    def limpar(self, questao: Questao) -> TextoLimpo:
        """Converte os campos HTML da questão em texto.

        Args:
            questao: Questão original.

        Returns:
            Campos limpos.
        """
        alternativas: dict[str, str] = {}
        letra: str
        texto: str
        for letra, texto in questao.alternativas.items():
            alternativas[letra] = self._processador.achatar(self._processador.html_para_texto(texto))
        return TextoLimpo(
            enunciado=self._processador.html_para_texto(questao.enunciado_html),
            comando=self._processador.html_para_texto(questao.comando),
            alternativas=alternativas,
        )

    def perfilar_todas(self, questoes: Sequence[Questao]) -> list[PerfilQuestao]:
        """Perfila uma lista de questões.

        Args:
            questoes: Questões originais.

        Returns:
            Um perfil por questão, na mesma ordem.
        """
        return [self.perfilar(questao) for questao in questoes]

    def perfilar(self, questao: Questao) -> PerfilQuestao:
        """Calcula o perfil de uma questão.

        Args:
            questao: Questão original.

        Returns:
            Perfil calculado.
        """
        limpo: TextoLimpo = self.limpar(questao)
        chars_alternativas: int = sum(len(texto) for texto in limpo.alternativas.values())
        palavras_conteudo: int = self._palavras_conteudo(limpo.enunciado)
        tags: list[str] = self._processador.nomes_tags(questao.enunciado_html) + self._processador.nomes_tags(
            questao.comando
        )
        entidades: int = len(self._processador.entidades(questao.enunciado_html)) + len(
            self._processador.entidades(questao.comando)
        )
        alternativas_com_html: int = 0
        alternativas_com_quebra: int = 0
        texto_bruto: str
        for texto_bruto in questao.alternativas.values():
            tags_alternativa: list[str] = self._processador.nomes_tags(texto_bruto)
            entidades_alternativa: int = len(self._processador.entidades(texto_bruto))
            tags.extend(tags_alternativa)
            entidades += entidades_alternativa
            alternativas_com_html += int(bool(tags_alternativa) or entidades_alternativa > 0)
            alternativas_com_quebra += int("\n" in texto_bruto.strip())
        disciplina: str = questao.disciplina_origem.strip()
        disciplina_normalizada: str = self._parametros.mapa_disciplinas.get(disciplina, "")
        assunto: str = questao.assunto_origem.strip()
        normalizado: str = f" {self._processador.normalizar(limpo.completo)} "
        campos_brutos: list[str] = [questao.enunciado_html, questao.comando, *questao.alternativas.values()]
        return PerfilQuestao(
            id=questao.id,
            formato=self._formato(questao.alternativas),
            n_alternativas=len(questao.alternativas),
            chars_enunciado=len(limpo.enunciado),
            chars_comando=len(limpo.comando),
            chars_alternativas=chars_alternativas,
            chars_total=len(limpo.enunciado) + len(limpo.comando) + chars_alternativas,
            chars_brutos=sum(len(campo) for campo in campos_brutos),
            html_de_editor=any(self._processador.tem_html_de_editor(campo) for campo in campos_brutos),
            palavras_conteudo_enunciado=palavras_conteudo,
            enunciado_curto=len(limpo.enunciado) < self._parametros.limiar_enunciado_curto,
            enunciado_generico=palavras_conteudo <= self._parametros.max_palavras_conteudo_generico,
            tipo_comando=self._tipo_comando(limpo.comando, limpo.enunciado),
            comando_so_html=bool(questao.comando.strip()) and not limpo.comando,
            tags_html=tuple(sorted(set(tags))),
            alternativas_com_html=alternativas_com_html,
            alternativas_com_quebra=alternativas_com_quebra,
            entidades_html=entidades,
            disciplina_origem=disciplina,
            disciplina_normalizada=disciplina_normalizada,
            origem_no_recorte=bool(disciplina_normalizada),
            assunto_origem=assunto,
            assunto_sem_parte=self._processador.remover_parte(assunto).strip(" ,-"),
            assunto_tem_parte=self._processador.tem_parte(assunto),
            assunto_multiplo="," in assunto,
            leis_citadas=self._legislacao.leis_citadas(limpo.completo),
            menciona_cp=self._RE_CP.search(limpo.completo) is not None,
            menciona_cpp=self._RE_CPP.search(limpo.completo) is not None,
            menciona_cf=self._RE_CF.search(limpo.completo) is not None,
            menciona_jurisprudencia=any(
                f" {termo} " in normalizado for termo in self._parametros.termos_jurisprudencia
            ),
            hash_enunciado=self._hash(self._processador.normalizar(limpo.enunciado)),
            hash_completo=self._hash(
                self._processador.normalizar(limpo.enunciado + " " + " ".join(limpo.alternativas.values()))
            ),
        )

    def _formato(self, alternativas: Mapping[str, str]) -> FormatoQuestao:
        """Deduz o formato a partir das alternativas.

        Args:
            alternativas: Letra -> texto original.

        Returns:
            Formato da questão.
        """
        letras: set[str] = set(alternativas)
        if letras == {"C", "E"}:
            return "certo_errado"
        if len(letras) == 5:
            return "multipla_escolha_5"
        if len(letras) == 4:
            return "multipla_escolha_4"
        return "outro"

    def _palavras_conteudo(self, enunciado: str) -> int:
        """Conta as palavras do enunciado que não são de ligação nem frase-padrão.

        Args:
            enunciado: Enunciado limpo.

        Returns:
            Número de palavras com conteúdo temático.
        """
        sem_conteudo: frozenset[str] = self._parametros.palavras_sem_conteudo
        return sum(
            1
            for token in self._processador.tokens(enunciado)
            if token not in sem_conteudo and len(token) > 1 and not token.isdigit()
        )

    def _tipo_comando(self, comando: str, enunciado: str) -> TipoComando:
        """Classifica o comando da questão.

        Args:
            comando: Comando limpo.
            enunciado: Enunciado limpo.

        Returns:
            Tipo do comando.
        """
        if not comando:
            return "vazio"
        comando_norm: str = self._processador.normalizar(comando)
        enunciado_norm: str = self._processador.normalizar(enunciado)
        if (
            len(comando_norm) >= 10
            and enunciado_norm
            and (enunciado_norm.startswith(comando_norm[:60]) or comando_norm.startswith(enunciado_norm[:60]))
        ):
            return "repete_enunciado"
        palavras: set[str] = set(comando_norm.split())
        if palavras & set(self._parametros.termos_comando_suspeito):
            return "suspeito"
        return "util"

    @staticmethod
    def _hash(texto: str) -> str:
        """Gera um hash curto e estável para um texto normalizado.

        Args:
            texto: Texto normalizado.

        Returns:
            Os 12 primeiros caracteres do SHA-1.
        """
        return hashlib.sha1(texto.encode("utf-8")).hexdigest()[:12]
