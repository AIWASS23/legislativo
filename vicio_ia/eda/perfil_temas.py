"""Perfil de cada nó da árvore: fantasmas, lixeiras, anomalias de título e uso possível."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from typing import ClassVar

from vicio_ia.arvore import ArvoreTemas
from vicio_ia.configuracao import ParametrosEDA
from vicio_ia.dominio import Tema, TipoDescricao
from vicio_ia.relatorio import RegistroTabular
from vicio_ia.texto import ProcessadorTexto


@dataclass(frozen=True)
class PerfilTema(RegistroTabular):
    """Características calculadas de um nó da árvore.

    Attributes:
        tema_id: ID do tema.
        parent_id: ID do pai ("" para raízes).
        disciplina: Disciplina do nó.
        nivel: 0 = disciplina, 1 = tema, 2 = subtema.
        titulo: Título original.
        caminho: Caminho original.
        status: ``active`` ou ``inactive``.
        tipo_descricao: raiz, vazia, modelo ou rica.
        n_questoes_origem: Questões que o nó tinha na origem (``None`` se não informado).
        n_filhos: Número de filhos diretos.
        total_questoes_irmaos: Soma das questões do nó e dos irmãos com contagem.
        participacao_no_pai: Fração das questões do grupo de irmãos que está neste nó.
        fantasma: Nó ativo, abaixo da raiz, sem descrição e sem histórico.
        canonico_id: Para fantasmas, o nó equivalente mais parecido ("" se não houver).
        canonico_caminho: Caminho do nó canônico.
        similaridade_canonico: Similaridade entre os títulos (``None`` se não houver canônico).
        titulo_generico: Título contém termo introdutório/genérico.
        concentracao_alta: Nó sem filhos que concentra a maior parte das questões dos irmãos.
        suspeita_lixeira: Nó sem filhos com concentração alta, ou com título genérico e muitas
            questões. Nós com filhos ficam de fora: a contagem deles soma a dos subtemas.
        motivo_lixeira: Explicação curta da suspeita.
        publicavel: Ativo, não fantasma e abaixo da raiz (pode ser tema central).
        aceita_recuo: Tema de nível 1 com filhos (destino do recuo para o pai).
        anomalias_titulo: Problemas encontrados no título.
    """

    tema_id: str
    parent_id: str
    disciplina: str
    nivel: int
    titulo: str
    caminho: str
    status: str
    tipo_descricao: TipoDescricao
    n_questoes_origem: int | None
    n_filhos: int
    total_questoes_irmaos: int | None
    participacao_no_pai: float | None
    fantasma: bool
    canonico_id: str
    canonico_caminho: str
    similaridade_canonico: float | None
    titulo_generico: bool
    concentracao_alta: bool
    suspeita_lixeira: bool
    motivo_lixeira: str
    publicavel: bool
    aceita_recuo: bool
    anomalias_titulo: tuple[str, ...]


@dataclass(frozen=True)
class Canonico:
    """Nó equivalente encontrado para um fantasma.

    Attributes:
        tema: Nó canônico.
        similaridade: Similaridade entre os títulos, de 0 a 1.
    """

    tema: Tema
    similaridade: float


class PerfiladorTemas:
    """Calcula o :class:`PerfilTema` de cada nó da árvore."""

    _RE_NUMERO_INICIAL: ClassVar[re.Pattern[str]] = re.compile(r"^\d+\s")
    _LIGACAO_COLADA: ClassVar[frozenset[str]] = frozenset(
        {
            "contra",
            "de",
            "do",
            "da",
            "dos",
            "das",
            "em",
            "no",
            "na",
            "nos",
            "nas",
            "por",
            "para",
            "com",
            "sem",
            "sobre",
            "entre",
        }
    )

    def __init__(self, arvore: ArvoreTemas, parametros: ParametrosEDA, processador: ProcessadorTexto) -> None:
        """Recebe as dependências e prepara vocabulários de comparação.

        Args:
            arvore: Árvore de temas.
            parametros: Limiares e listas da EDA.
            processador: Limpeza e normalização de texto.
        """
        self._arvore: ArvoreTemas = arvore
        self._parametros: ParametrosEDA = parametros
        self._processador: ProcessadorTexto = processador
        self._termos_genericos: list[str] = [
            processador.chave_comparacao(termo, manter_parte=False) for termo in parametros.termos_titulo_generico
        ]
        self._fantasmas: set[str] = {tema.tema_id for tema in arvore.todos() if self.eh_fantasma(tema)}
        self._freq_titulos: Counter[str] = Counter(
            token for tema in arvore.todos() for token in processador.tokens(tema.titulo)
        )
        self._freq_corpus: Counter[str] = Counter(
            token for tema in arvore.todos() for token in processador.tokens(f"{tema.caminho} {tema.descricao}")
        )

    @staticmethod
    def eh_fantasma(tema: Tema) -> bool:
        """Indica se o nó é um "fantasma": ativo, abaixo da raiz e sem descrição.

        Esses nós não têm histórico de questões e repetem nomes do site de
        origem ("Teoria da Pena (Parte 2)") ou de outra disciplina.

        Args:
            tema: Nó da árvore.

        Returns:
            ``True`` se for fantasma.
        """
        return tema.ativo and tema.nivel > 0 and tema.tipo_descricao == "vazia"

    def perfilar_todos(self) -> list[PerfilTema]:
        """Perfila todos os nós, na ordem do CSV.

        Returns:
            Um perfil por nó.
        """
        return [self.perfilar(tema) for tema in self._arvore.todos()]

    def perfilar(self, tema: Tema) -> PerfilTema:
        """Calcula o perfil de um nó.

        Args:
            tema: Nó da árvore.

        Returns:
            Perfil calculado.
        """
        fantasma: bool = tema.tema_id in self._fantasmas
        canonico: Canonico | None = self.canonico(tema) if fantasma else None
        total_irmaos: int | None
        participacao: float | None
        total_irmaos, participacao = self._participacao(tema)
        if participacao is not None:
            participacao = round(participacao, 3)
        n_questoes: int | None = tema.n_questoes_origem
        titulo_generico: bool = self._titulo_generico(tema)
        folha: bool = not self._arvore.filhos(tema.tema_id)
        concentracao_alta: bool = (
            folha
            and participacao is not None
            and n_questoes is not None
            and participacao >= self._parametros.limiar_participacao_lixeira
            and n_questoes >= self._parametros.min_questoes_lixeira
        )
        generico_volumoso: bool = (
            folha and titulo_generico and n_questoes is not None and n_questoes >= self._parametros.min_questoes_lixeira
        )
        motivos: list[str] = []
        if concentracao_alta and participacao is not None:
            motivos.append(f"concentra {participacao:.0%} das questões dos irmãos")
        if generico_volumoso:
            motivos.append(f"título genérico com {n_questoes} questões")
        publicavel: bool = tema.ativo and not fantasma and tema.nivel > 0
        return PerfilTema(
            tema_id=tema.tema_id,
            parent_id=tema.parent_id or "",
            disciplina=tema.disciplina,
            nivel=tema.nivel,
            titulo=tema.titulo,
            caminho=tema.caminho,
            status=tema.status,
            tipo_descricao=tema.tipo_descricao,
            n_questoes_origem=n_questoes,
            n_filhos=len(self._arvore.filhos(tema.tema_id)),
            total_questoes_irmaos=total_irmaos,
            participacao_no_pai=participacao,
            fantasma=fantasma,
            canonico_id="" if canonico is None else canonico.tema.tema_id,
            canonico_caminho="" if canonico is None else canonico.tema.caminho,
            similaridade_canonico=None if canonico is None else round(canonico.similaridade, 3),
            titulo_generico=titulo_generico,
            concentracao_alta=concentracao_alta,
            suspeita_lixeira=bool(motivos),
            motivo_lixeira="; ".join(motivos),
            publicavel=publicavel,
            aceita_recuo=publicavel and tema.nivel == 1 and bool(self._arvore.filhos(tema.tema_id)),
            anomalias_titulo=self._anomalias_titulo(tema),
        )

    def canonico(self, tema: Tema) -> Canonico | None:
        """Procura o nó não fantasma com título mais parecido (em qualquer disciplina).

        Empates favorecem a mesma disciplina e, depois, o nível mais alto da árvore.

        Args:
            tema: Nó (normalmente um fantasma).

        Returns:
            O candidato acima do limiar de similaridade, ou ``None``.
        """
        melhor: Canonico | None = None
        melhor_chave: tuple[float, int, int] = (-1.0, 0, 0)
        candidato: Tema
        for candidato in self._arvore.todos():
            if candidato.tema_id == tema.tema_id or candidato.tema_id in self._fantasmas:
                continue
            if not candidato.ativo or candidato.nivel == 0:
                continue
            similaridade: float = self._processador.similaridade(tema.titulo, candidato.titulo)
            chave: tuple[float, int, int] = (
                similaridade,
                int(candidato.disciplina == tema.disciplina),
                -candidato.nivel,
            )
            if similaridade >= self._parametros.limiar_similaridade_canonico and chave > melhor_chave:
                melhor = Canonico(candidato, similaridade)
                melhor_chave = chave
        return melhor

    def _participacao(self, tema: Tema) -> tuple[int | None, float | None]:
        """Calcula a fração das questões do grupo de irmãos que está no nó.

        Args:
            tema: Nó da árvore.

        Returns:
            ``(total do grupo, participação)``; ``(None, None)`` para raízes ou
            nós sem contagem.
        """
        n_questoes: int | None = tema.n_questoes_origem
        if tema.nivel == 0 or n_questoes is None:
            return None, None
        total: int = n_questoes + sum(irmao.n_questoes_origem or 0 for irmao in self._arvore.irmaos(tema.tema_id))
        if total == 0:
            return total, None
        return total, n_questoes / total

    def _titulo_generico(self, tema: Tema) -> bool:
        """Indica se o título contém um termo introdutório ou genérico.

        Args:
            tema: Nó da árvore.

        Returns:
            ``True`` se algum termo de ``termos_titulo_generico`` aparecer como
            sequência de palavras no título.
        """
        chave: str = f" {self._processador.chave_comparacao(tema.titulo, manter_parte=False)} "
        return any(f" {termo} " in chave for termo in self._termos_genericos if termo)

    def _anomalias_titulo(self, tema: Tema) -> tuple[str, ...]:
        """Procura problemas de digitação e formatação no título.

        Args:
            tema: Nó da árvore.

        Returns:
            Descrições curtas das anomalias encontradas.
        """
        anomalias: list[str] = []
        if self._RE_NUMERO_INICIAL.match(tema.titulo):
            anomalias.append("começa com número")
        if tema.titulo != tema.titulo.strip() or "  " in tema.titulo:
            anomalias.append("espaços irregulares")
        token: str
        for token in self._processador.tokens(tema.titulo):
            colada: str = self._palavras_coladas(token)
            if colada:
                anomalias.append(f"palavras coladas: {token} -> {colada}")
            parecida: str = self._palavra_parecida(token)
            if parecida:
                anomalias.append(f"possível erro de digitação: {token} ~ {parecida}")
        return tuple(anomalias)

    def _palavras_coladas(self, token: str) -> str:
        """Verifica se uma palavra rara é uma palavra comum colada a uma preposição ("crimescontra").

        Args:
            token: Palavra normalizada de um título.

        Returns:
            As duas palavras separadas por espaço, ou ``""``.
        """
        if self._freq_titulos[token] > 1 or len(token) < 6:
            return ""
        posicao: int
        for posicao in range(2, len(token) - 1):
            esquerda: str = token[:posicao]
            direita: str = token[posicao:]
            if esquerda in self._LIGACAO_COLADA and len(direita) >= 4 and self._freq_titulos[direita] >= 2:
                return f"{esquerda} {direita}"
            if direita in self._LIGACAO_COLADA and len(esquerda) >= 4 and self._freq_titulos[esquerda] >= 2:
                return f"{esquerda} {direita}"
        return ""

    def _palavra_parecida(self, token: str) -> str:
        """Procura uma grafia a uma troca de letra (ou inversão de vizinhas) de distância, e mais comum.

        Só olha palavras que aparecem num único título. Trocas de vogal no fim
        da palavra (gênero e número: "criminosos"/"criminosas") são ignoradas.
        A grafia sugerida precisa ser mais frequente no corpus de títulos,
        caminhos e descrições.

        Args:
            token: Palavra normalizada de um título.

        Returns:
            A grafia mais provável, ou ``""``.
        """
        if len(token) < 5 or token.isdigit() or self._freq_titulos[token] > 1:
            return ""
        melhor: str = ""
        outro: str
        for outro in self._freq_titulos:
            if len(outro) != len(token) or outro == token:
                continue
            if self._freq_corpus[outro] <= self._freq_corpus[token]:
                continue
            if not self._um_erro_de_digitacao(token, outro):
                continue
            if not melhor or self._freq_corpus[outro] > self._freq_corpus[melhor]:
                melhor = outro
        return melhor

    @staticmethod
    def _um_erro_de_digitacao(palavra: str, referencia: str) -> bool:
        """Indica se duas palavras do mesmo tamanho diferem por um único erro de digitação.

        Aceita uma letra trocada ou duas letras vizinhas invertidas. Rejeita
        trocas na primeira ou na última letra (costumam ser outra palavra:
        "denúncia"/"renúncia", "causal"/"causas") e a troca entre "a", "e" e
        "o" nas três últimas letras (flexão de gênero e número).

        Args:
            palavra: Palavra suspeita.
            referencia: Grafia de referência, do mesmo tamanho.

        Returns:
            ``True`` se a diferença parecer erro de digitação.
        """
        diferencas: list[int] = [indice for indice in range(len(palavra)) if palavra[indice] != referencia[indice]]
        if len(diferencas) == 1:
            indice: int = diferencas[0]
            if indice == 0 or indice == len(palavra) - 1:
                return False
            flexao: bool = {palavra[indice], referencia[indice]} <= {"a", "e", "o"} and indice >= len(palavra) - 3
            return not flexao
        if len(diferencas) == 2 and diferencas[1] == diferencas[0] + 1:
            primeira: int = diferencas[0]
            return palavra[primeira] == referencia[primeira + 1] and palavra[primeira + 1] == referencia[primeira]
        return False
