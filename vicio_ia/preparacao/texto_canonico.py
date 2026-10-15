"""Texto canônico das questões (ADR-004): o mesmo texto para classificadores, verificador e embeddings."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import ClassVar, Literal

from vicio_ia.configuracao import ParametrosEDA, ParametrosPreparacao
from vicio_ia.dominio import Questao
from vicio_ia.eda.perfil_questoes import FormatoQuestao, PerfiladorQuestoes, PerfilQuestao, TextoLimpo, TipoComando
from vicio_ia.texto import ProcessadorTexto

type MotivoComando = Literal["incluido", "vazio", "suspeito", "repete_enunciado", "so_frase_padrao"]
"""Por que o comando entrou ou não no texto canônico."""


@dataclass(frozen=True)
class MarcasQuestao:
    """Marcas da questão usadas pela decisão e pela calibração (ADR-011, ADR-013).

    Attributes:
        enunciado_generico: Enunciado sem palavra de conteúdo (o assunto está nas alternativas).
        html_de_editor: O original trazia marcação colada do Word.
        leis_citadas: Números das leis citadas por número ou apelido.
        menciona_cp: Cita o Código Penal.
        menciona_cpp: Cita o Código de Processo Penal.
        menciona_cf: Cita a Constituição.
        menciona_jurisprudencia: Cita STF, STJ, súmula ou jurisprudência.
    """

    enunciado_generico: bool
    html_de_editor: bool
    leis_citadas: tuple[str, ...]
    menciona_cp: bool
    menciona_cpp: bool
    menciona_cf: bool
    menciona_jurisprudencia: bool


@dataclass(frozen=True)
class QuestaoPreparada:
    """Questão pronta para os passos seguintes.

    Attributes:
        id: ID da questão.
        formato: Múltipla escolha (4 ou 5) ou certo/errado.
        texto_canonico: Texto enviado aos modelos (sem rótulos de origem, ADR-006).
        enunciado: Enunciado limpo (pode ter várias linhas).
        comando: Comando limpo, mesmo quando fica fora do texto canônico.
        tipo_comando: Classificação do comando feita na EDA.
        motivo_comando: Por que o comando entrou ou não no texto canônico.
        alternativas: Letra -> alternativa limpa, numa linha.
        marcas: Marcas para decisão e calibração.
        hash_completo: Hash do enunciado mais alternativas normalizados.
        duplicata_de: ID da primeira questão com o mesmo texto completo, se houver.
        caracteres: Tamanho do texto canônico.
        tokens_estimados: Estimativa de tokens do texto canônico.
        original: Campos originais, intocados (inclusive os rótulos de origem).
    """

    id: str
    formato: FormatoQuestao
    texto_canonico: str
    enunciado: str
    comando: str
    tipo_comando: TipoComando
    motivo_comando: MotivoComando
    alternativas: dict[str, str]
    marcas: MarcasQuestao
    hash_completo: str
    duplicata_de: str | None
    caracteres: int
    tokens_estimados: int
    original: dict[str, object]

    def como_dict(self) -> dict[str, object]:
        """Converte a questão em dicionário serializável em JSON.

        Returns:
            Dicionário com todos os campos (tuplas viram listas).
        """
        return asdict(self)


class MontadorTextoCanonico:
    """Monta o texto canônico e as marcas de cada questão.

    Formato (múltipla escolha)::

        [Q0065] Múltipla escolha (5 alternativas)
        Enunciado: O crime de extorsão mediante sequestro (CP, art. 159)
        A) é qualificado se do fato resulta lesão corporal grave ou morte.
        ...

    Em certo/errado, o cabeçalho avisa que é para julgar uma afirmação e as alternativas
    ("Certo"/"Errado") ficam de fora. O comando só entra quando é útil e tem conteúdo
    próprio. Os rótulos de origem (disciplina e assunto) nunca entram: o montador
    não lê esses campos (ADR-006).
    """

    CABECALHOS: ClassVar[dict[FormatoQuestao, str]] = {
        "multipla_escolha_5": "Múltipla escolha (5 alternativas)",
        "multipla_escolha_4": "Múltipla escolha (4 alternativas)",
        "certo_errado": "Certo ou errado (julgar a afirmação)",
        "outro": "Múltipla escolha",
    }

    def __init__(
        self,
        perfilador: PerfiladorQuestoes,
        processador: ProcessadorTexto,
        parametros_eda: ParametrosEDA,
        parametros: ParametrosPreparacao,
    ) -> None:
        """Recebe as dependências.

        Args:
            perfilador: Limpeza e perfil das questões (da EDA).
            processador: Normalização de texto.
            parametros_eda: Lista de palavras sem conteúdo.
            parametros: Parâmetros do passo 01.
        """
        self._perfilador: PerfiladorQuestoes = perfilador
        self._processador: ProcessadorTexto = processador
        self._sem_conteudo: frozenset[str] = parametros_eda.palavras_sem_conteudo
        self._parametros: ParametrosPreparacao = parametros

    def montar(self, questao: Questao, com_cabecalho: bool = True) -> str:
        """Monta só o texto canônico de uma questão.

        Args:
            questao: Questão original.
            com_cabecalho: Inclui a linha ``[ID] formato`` (embeddings podem dispensar).

        Returns:
            Texto canônico.
        """
        limpo: TextoLimpo = self._perfilador.limpar(questao)
        perfil: PerfilQuestao = self._perfilador.perfilar(questao)
        return self._texto(questao.id, perfil.formato, limpo, self._motivo_comando(perfil, limpo), com_cabecalho)

    def preparar(self, questao: Questao, duplicata_de: str | None) -> QuestaoPreparada:
        """Monta a questão preparada completa.

        Args:
            questao: Questão original.
            duplicata_de: ID da primeira questão com o mesmo texto completo, se houver.

        Returns:
            Questão preparada.
        """
        limpo: TextoLimpo = self._perfilador.limpar(questao)
        perfil: PerfilQuestao = self._perfilador.perfilar(questao)
        motivo: MotivoComando = self._motivo_comando(perfil, limpo)
        texto: str = self._texto(questao.id, perfil.formato, limpo, motivo, True)
        return QuestaoPreparada(
            id=questao.id,
            formato=perfil.formato,
            texto_canonico=texto,
            enunciado=limpo.enunciado,
            comando=limpo.comando,
            tipo_comando=perfil.tipo_comando,
            motivo_comando=motivo,
            alternativas=dict(limpo.alternativas),
            marcas=MarcasQuestao(
                enunciado_generico=perfil.enunciado_generico,
                html_de_editor=perfil.html_de_editor,
                leis_citadas=perfil.leis_citadas,
                menciona_cp=perfil.menciona_cp,
                menciona_cpp=perfil.menciona_cpp,
                menciona_cf=perfil.menciona_cf,
                menciona_jurisprudencia=perfil.menciona_jurisprudencia,
            ),
            hash_completo=perfil.hash_completo,
            duplicata_de=duplicata_de,
            caracteres=len(texto),
            tokens_estimados=round(len(texto) / self._parametros.chars_por_token),
            original={
                "enunciado_html": questao.enunciado_html,
                "comando": questao.comando,
                "alternativas": dict(questao.alternativas),
                "disciplina_origem": questao.disciplina_origem,
                "assunto_origem": questao.assunto_origem,
            },
        )

    def _motivo_comando(self, perfil: PerfilQuestao, limpo: TextoLimpo) -> MotivoComando:
        """Decide se o comando entra no texto canônico.

        Args:
            perfil: Perfil da questão (tipo do comando).
            limpo: Campos limpos.

        Returns:
            ``incluido`` só para comando útil com ao menos uma palavra de conteúdo.
        """
        if perfil.tipo_comando != "util":
            return perfil.tipo_comando
        conteudo: list[str] = [
            token
            for token in self._processador.tokens(limpo.comando)
            if token not in self._sem_conteudo and len(token) > 1 and not token.isdigit()
        ]
        return "incluido" if conteudo else "so_frase_padrao"

    def _texto(
        self, identificador: str, formato: FormatoQuestao, limpo: TextoLimpo, motivo: MotivoComando, cabecalho: bool
    ) -> str:
        """Monta as linhas do texto canônico.

        Args:
            identificador: ID da questão.
            formato: Formato da questão.
            limpo: Campos limpos.
            motivo: Decisão sobre o comando.
            cabecalho: Inclui a linha de cabeçalho.

        Returns:
            Texto canônico.
        """
        linhas: list[str] = []
        if cabecalho:
            linhas.append(f"[{identificador}] {self.CABECALHOS[formato]}")
        linhas.append(f"Enunciado: {limpo.enunciado}")
        if motivo == "incluido":
            linhas.append(f"Comando: {self._processador.achatar(limpo.comando)}")
        if formato != "certo_errado":
            letra: str
            texto: str
            for letra, texto in sorted(limpo.alternativas.items()):
                linhas.append(f"{letra}) {texto}")
        return "\n".join(linhas)
