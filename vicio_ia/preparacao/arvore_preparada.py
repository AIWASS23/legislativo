"""Árvore de temas preparada (ADR-005): nós utilizáveis, fantasmas, lixeiras, sobreposições e títulos."""

from __future__ import annotations

import csv
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import ClassVar, Literal, TextIO

from vicio_ia.arvore import ArvoreTemas
from vicio_ia.dominio import Tema
from vicio_ia.eda.perfil_temas import PerfilTema

type TipoConvencao = Literal["duplicado_outra_disciplina", "sobreposicao", "duplicado_parte", ""]
"""Risco de convenção do nó, do mais para o menos provável de afetar a régua (ADR-013).

* ``duplicado_outra_disciplina``: o nó (ou um ancestral) tem cópia fantasma em outra disciplina (ex.: LEP);
* ``sobreposicao``: o nó está num grupo de sobreposição entre nós válidos (ex.: Ação Penal);
* ``duplicado_parte``: o nó (ou um ancestral) tem cópia "(Parte N)" na mesma disciplina.
"""

type NivelLixeira = Literal["forte", "moderada", ""]
"""``forte``: publicar só com concordância total e verificador favorável; ``moderada``: só variável de risco."""


class ErroDecisoesArvore(Exception):
    """Arquivo de decisões manuais da árvore ausente ou malformado."""


@dataclass(frozen=True)
class DecisoesArvore:
    """Decisões manuais sobre a árvore, lidas de ``dados/temas/`` (registradas em ``decisoes_manuais.md``).

    Attributes:
        lixeiras: ``tema_id -> (nível, justificativa)``; o nível ``fora`` documenta falsos positivos.
        sobreposicoes: ``tema_id -> (grupo, regra de desempate)``.
        correcoes: ``tema_id -> (título original, título de exibição)``.
    """

    lixeiras: dict[str, tuple[str, str]]
    sobreposicoes: dict[str, tuple[str, str]]
    correcoes: dict[str, tuple[str, str]]


class LeitorDecisoesArvore:
    """Lê os CSVs de decisões manuais da árvore."""

    ARQUIVOS: ClassVar[dict[str, tuple[str, ...]]] = {
        "lixeiras.csv": ("tema_id", "nivel", "justificativa"),
        "sobreposicoes.csv": ("grupo", "tema_id", "regra_desempate"),
        "correcoes_titulo.csv": ("tema_id", "titulo_original", "titulo_exibicao", "motivo"),
    }
    NIVEIS_LIXEIRA: ClassVar[frozenset[str]] = frozenset({"forte", "moderada", "fora"})

    def __init__(self, pasta: Path) -> None:
        """Define a pasta das decisões.

        Args:
            pasta: ``dados/temas/``.
        """
        self._pasta: Path = pasta

    def ler(self) -> DecisoesArvore:
        """Lê e valida os três arquivos.

        Returns:
            Decisões carregadas.

        Raises:
            ErroDecisoesArvore: Se faltar arquivo, coluna, ou houver nível de lixeira inválido.
        """
        lixeiras: dict[str, tuple[str, str]] = {}
        linha: dict[str, str]
        for linha in self._linhas("lixeiras.csv"):
            if linha["nivel"] not in self.NIVEIS_LIXEIRA:
                raise ErroDecisoesArvore(f"lixeiras.csv: nível inválido {linha['nivel']!r} no tema {linha['tema_id']}")
            lixeiras[linha["tema_id"]] = (linha["nivel"], linha["justificativa"])
        sobreposicoes: dict[str, tuple[str, str]] = {
            linha["tema_id"]: (linha["grupo"], linha["regra_desempate"]) for linha in self._linhas("sobreposicoes.csv")
        }
        correcoes: dict[str, tuple[str, str]] = {
            linha["tema_id"]: (linha["titulo_original"], linha["titulo_exibicao"])
            for linha in self._linhas("correcoes_titulo.csv")
        }
        return DecisoesArvore(lixeiras, sobreposicoes, correcoes)

    def _linhas(self, nome: str) -> list[dict[str, str]]:
        """Lê um CSV de decisões, conferindo o cabeçalho.

        Args:
            nome: Nome do arquivo.

        Returns:
            Linhas com os valores sem espaços nas pontas.

        Raises:
            ErroDecisoesArvore: Se o arquivo não existir ou faltar coluna.
        """
        caminho: Path = self._pasta / nome
        if not caminho.is_file():
            raise ErroDecisoesArvore(f"arquivo de decisões ausente: {caminho}")
        arquivo: TextIO
        with caminho.open(encoding="utf-8", newline="") as arquivo:
            leitor: csv.DictReader[str] = csv.DictReader(arquivo)
            faltantes: list[str] = [c for c in self.ARQUIVOS[nome] if c not in (leitor.fieldnames or [])]
            if faltantes:
                raise ErroDecisoesArvore(f"{nome}: colunas ausentes {faltantes}")
            return [{chave: (valor or "").strip() for chave, valor in linha.items()} for linha in leitor]


@dataclass(frozen=True)
class TemaPreparado:
    """Nó da árvore pronto para os passos seguintes.

    Attributes:
        tema_id: ID do tema.
        parent_id: ID do pai (``None`` nas disciplinas).
        disciplina: Disciplina.
        nivel: 0 = disciplina, 1 = tema, 2 = subtema.
        titulo: Título original.
        titulo_exibicao: Título com erros corrigidos (só para prompts e relatórios; o ID não muda).
        caminho: Caminho original.
        caminho_exibicao: Caminho montado com os títulos de exibição.
        status: ``active`` ou ``inactive``.
        publicavel: Pode ser tema central (ativo, não fantasma, abaixo da disciplina).
        fantasma: Nó sem descrição e sem histórico, criado na importação.
        canonico_id: Para fantasmas, o nó que vale no lugar dele.
        duplicado_por: Fantasmas que apontam para este nó ou para um ancestral dele.
        lixeira: Nível de lixeira (``forte``, ``moderada`` ou vazio).
        grupo_sobreposicao: Grupo de sobreposição (próprio ou herdado do ancestral).
        regra_desempate: Regra de desempate do nó dentro do grupo.
        tipo_convencao: Tipo de risco de convenção (vazio se não há risco).
        zona_convencao: Publicável e com risco de convenção (entra na margem de convenção, ADR-013).
        aceita_recuo: Tema de nível 1 com filhos (destino do recuo para o pai, ADR-010).
        filhos: IDs dos filhos diretos.
        n_questoes_origem: Questões no sistema antigo (``None`` se não informado).
    """

    tema_id: str
    parent_id: str | None
    disciplina: str
    nivel: int
    titulo: str
    titulo_exibicao: str
    caminho: str
    caminho_exibicao: str
    status: str
    publicavel: bool
    fantasma: bool
    canonico_id: str | None
    duplicado_por: tuple[str, ...]
    lixeira: NivelLixeira
    grupo_sobreposicao: str
    regra_desempate: str
    tipo_convencao: TipoConvencao
    zona_convencao: bool
    aceita_recuo: bool
    filhos: tuple[str, ...]
    n_questoes_origem: int | None

    def como_dict(self) -> dict[str, object]:
        """Converte em dicionário serializável em JSON.

        Returns:
            Dicionário com todos os campos.
        """
        return asdict(self)


class PreparadorArvore:
    """Junta a árvore, o perfil calculado na EDA e as decisões manuais (ADR-005)."""

    MARCA_CONCEITUAL: ClassVar[str] = " [conceitual]"
    LEGENDA: ClassVar[str] = (
        "Temas em que a questão pode ser classificada (ID | caminho). "
        "[conceitual] = use só se a questão for sobre o conceito geral do tema, não sobre um instituto específico."
    )

    def __init__(self, arvore: ArvoreTemas, perfis: Sequence[PerfilTema], decisoes: DecisoesArvore) -> None:
        """Recebe a árvore, os perfis e as decisões.

        Args:
            arvore: Árvore de temas.
            perfis: Perfil de cada nó (fantasmas, canônicos, recuo), calculado pela EDA.
            decisoes: Decisões manuais (lixeiras, sobreposições, correções).
        """
        self._arvore: ArvoreTemas = arvore
        self._perfis: dict[str, PerfilTema] = {perfil.tema_id: perfil for perfil in perfis}
        self._decisoes: DecisoesArvore = decisoes

    def preparar(self) -> list[TemaPreparado]:
        """Prepara todos os nós, na ordem do CSV.

        Returns:
            Nós preparados.
        """
        duplicados: dict[str, list[str]] = {}
        perfil: PerfilTema
        for perfil in self._perfis.values():
            if perfil.fantasma and perfil.canonico_id:
                duplicados.setdefault(perfil.canonico_id, []).append(perfil.tema_id)
        return [self._preparar_no(tema, duplicados) for tema in self._arvore.todos()]

    def _preparar_no(self, tema: Tema, duplicados: dict[str, list[str]]) -> TemaPreparado:
        """Prepara um nó.

        Args:
            tema: Nó original.
            duplicados: ``canônico -> fantasmas`` que apontam para ele.

        Returns:
            Nó preparado.
        """
        perfil: PerfilTema = self._perfis[tema.tema_id]
        nivel_lixeira: str = self._decisoes.lixeiras.get(tema.tema_id, ("", ""))[0]
        lixeira: NivelLixeira = (
            "forte" if nivel_lixeira == "forte" else "moderada" if nivel_lixeira == "moderada" else ""
        )
        grupo: str
        regra: str
        grupo, regra = self._sobreposicao(tema)
        linhagem: list[str] = [ancestral.tema_id for ancestral in self._arvore.ancestrais(tema.tema_id)] + [
            tema.tema_id
        ]
        duplicado_por: tuple[str, ...] = tuple(sorted(f for i in linhagem for f in duplicados.get(i, [])))
        tipo: TipoConvencao = self._tipo_convencao(tema, duplicado_por, grupo) if perfil.publicavel else ""
        return TemaPreparado(
            tema_id=tema.tema_id,
            parent_id=tema.parent_id,
            disciplina=tema.disciplina,
            nivel=tema.nivel,
            titulo=tema.titulo,
            titulo_exibicao=self.titulo_exibicao(tema.tema_id),
            caminho=tema.caminho,
            caminho_exibicao=self.caminho_exibicao(tema.tema_id),
            status=tema.status,
            publicavel=perfil.publicavel,
            fantasma=perfil.fantasma,
            canonico_id=perfil.canonico_id or None,
            duplicado_por=duplicado_por,
            lixeira=lixeira,
            grupo_sobreposicao=grupo,
            regra_desempate=regra,
            tipo_convencao=tipo,
            zona_convencao=bool(tipo),
            aceita_recuo=perfil.aceita_recuo,
            filhos=tuple(filho.tema_id for filho in self._arvore.filhos(tema.tema_id)),
            n_questoes_origem=tema.n_questoes_origem,
        )

    def _tipo_convencao(self, tema: Tema, duplicado_por: tuple[str, ...], grupo: str) -> TipoConvencao:
        """Classifica o risco de convenção de um nó publicável.

        Args:
            tema: Nó da árvore.
            duplicado_por: Fantasmas que duplicam o nó ou um ancestral dele.
            grupo: Grupo de sobreposição do nó.

        Returns:
            O tipo de maior risco que se aplica, ou vazio.
        """
        disciplinas_fantasmas: set[str] = {self._arvore.tema(f).disciplina for f in duplicado_por}
        if disciplinas_fantasmas - {tema.disciplina}:
            return "duplicado_outra_disciplina"
        if grupo:
            return "sobreposicao"
        if duplicado_por:
            return "duplicado_parte"
        return ""

    def titulo_exibicao(self, tema_id: str) -> str:
        """Título corrigido, quando há correção registrada.

        Args:
            tema_id: ID do tema.

        Returns:
            Título de exibição.
        """
        correcao: tuple[str, str] | None = self._decisoes.correcoes.get(tema_id)
        return correcao[1] if correcao else self._arvore.tema(tema_id).titulo

    def caminho_exibicao(self, tema_id: str) -> str:
        """Caminho montado com os títulos de exibição.

        Args:
            tema_id: ID do tema.

        Returns:
            Caminho ``Disciplina > Tema > Subtema``.
        """
        ids: list[str] = [ancestral.tema_id for ancestral in self._arvore.ancestrais(tema_id)] + [tema_id]
        return " > ".join(self.titulo_exibicao(identificador) for identificador in ids)

    def _sobreposicao(self, tema: Tema) -> tuple[str, str]:
        """Grupo de sobreposição do nó: o próprio ou o do ancestral mais próximo.

        Args:
            tema: Nó da árvore.

        Returns:
            ``(grupo, regra de desempate)``; vazio se o nó não está em grupo.
        """
        if tema.tema_id in self._decisoes.sobreposicoes:
            return self._decisoes.sobreposicoes[tema.tema_id]
        ancestral: Tema
        for ancestral in reversed(self._arvore.ancestrais(tema.tema_id)):
            if ancestral.tema_id in self._decisoes.sobreposicoes:
                grupo: str = self._decisoes.sobreposicoes[ancestral.tema_id][0]
                return grupo, f"herdada de {ancestral.tema_id}: {self._decisoes.sobreposicoes[ancestral.tema_id][1]}"
        return "", ""

    def arvore_enxuta(self, temas: Sequence[TemaPreparado]) -> str:
        """Gera a árvore enxuta para os prompts: só nós publicáveis, ``ID | caminho``, bytes estáveis.

        Lixeiras fortes recebem a marca ``[conceitual]``. A ordem é a do caminho, para que o
        texto não mude entre execuções (cache de prompt, ADR-003).

        Args:
            temas: Nós preparados.

        Returns:
            Texto da árvore, com legenda na primeira linha e quebra de linha no final.
        """
        linhas: list[str] = [self.LEGENDA]
        tema: TemaPreparado
        for tema in sorted((t for t in temas if t.publicavel), key=lambda t: (t.caminho_exibicao, t.tema_id)):
            marca: str = self.MARCA_CONCEITUAL if tema.lixeira == "forte" else ""
            linhas.append(f"{tema.tema_id} | {tema.caminho_exibicao}{marca}")
        return "\n".join(linhas) + "\n"
