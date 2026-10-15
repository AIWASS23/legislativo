"""Limpeza e normalização de texto: HTML cru do banco, acentos e plurais."""

from __future__ import annotations

import html
import re
import unicodedata
from difflib import SequenceMatcher
from typing import ClassVar


class ProcessadorTexto:
    """Converte HTML em texto e gera formas normalizadas para comparação.

    A classe só guarda expressões regulares compiladas (atributos de classe),
    então uma única instância pode ser compartilhada por todo o projeto.
    """

    PALAVRAS_LIGACAO: ClassVar[frozenset[str]] = frozenset(
        {"a", "o", "as", "os", "e", "de", "da", "do", "das", "dos", "em", "no", "na", "nos", "nas", "ao", "aos"}
    )

    _RE_BLOCO_IGNORADO: ClassVar[re.Pattern[str]] = re.compile(
        r"<!--.*?-->|<\s*(style|script|xml)\b.*?<\s*/\s*\1\s*>", re.IGNORECASE | re.DOTALL
    )
    _RE_ESCAPE_LITERAL: ClassVar[re.Pattern[str]] = re.compile(r"\\(?:r\\n|n|r|t)")
    _RE_EDITOR: ClassVar[re.Pattern[str]] = re.compile(r"<!--\[if|<\s*[wom]:|mso-", re.IGNORECASE)
    _RE_QUEBRA: ClassVar[re.Pattern[str]] = re.compile(r"<\s*br\s*/?\s*>|</\s*(?:p|div|li)\s*>", re.IGNORECASE)
    _RE_TAG: ClassVar[re.Pattern[str]] = re.compile(r"<[^>]*>")
    _RE_NOME_TAG: ClassVar[re.Pattern[str]] = re.compile(r"<\s*([a-zA-Z][a-zA-Z0-9]*)")
    _RE_ENTIDADE: ClassVar[re.Pattern[str]] = re.compile(r"&(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);")
    _RE_ESPACOS: ClassVar[re.Pattern[str]] = re.compile(r"[ \t\r\f\v ]+")
    _RE_BRANCOS: ClassVar[re.Pattern[str]] = re.compile(r"\s+")
    _RE_LINHAS_VAZIAS: ClassVar[re.Pattern[str]] = re.compile(r"\n{3,}")
    _RE_NAO_ALFANUMERICO: ClassVar[re.Pattern[str]] = re.compile(r"[^a-z0-9]+")
    _RE_PARTE: ClassVar[re.Pattern[str]] = re.compile(r"\(?\s*\bparte\s+0*\d+\s*\)?", re.IGNORECASE)
    _SUFIXOS_PLURAL: ClassVar[tuple[tuple[str, str], ...]] = (
        ("oes", "ao"),
        ("aes", "ao"),
        ("ais", "al"),
        ("eis", "el"),
        ("ois", "ol"),
        ("uis", "ul"),
        ("ns", "m"),
    )

    def html_para_texto(self, html_bruto: str) -> str:
        """Converte HTML cru em texto legível, preservando quebras de linha.

        Escapes literais vindos do banco (os dois caracteres ``\\`` + ``n``, ou ``\\t``)
        viram quebra de linha ou espaço. Comentários (inclusive os condicionais do Word) e blocos ``<style>``,
        ``<script>`` e ``<xml>`` são removidos com o conteúdo; ``<br>`` e fins de
        parágrafo viram quebra de linha; as demais tags são removidas mantendo
        o texto; entidades (``&nbsp;``) são decodificadas.

        Args:
            html_bruto: Texto com HTML, como está no banco.

        Returns:
            Texto limpo, sem espaços repetidos e com no máximo uma linha em branco seguida.
        """
        texto: str = self._RE_ESCAPE_LITERAL.sub(lambda m: " " if m.group(0) == "\\t" else "\n", html_bruto)
        texto = self._RE_BLOCO_IGNORADO.sub("", texto)
        texto = self._RE_QUEBRA.sub("\n", texto)
        texto = self._RE_TAG.sub("", texto)
        texto = html.unescape(texto)
        linhas: list[str] = [self._RE_ESPACOS.sub(" ", linha).strip() for linha in texto.split("\n")]
        texto = self._RE_LINHAS_VAZIAS.sub("\n\n", "\n".join(linhas))
        return texto.strip()

    def escapes_literais(self, texto: str) -> int:
        """Conta escapes literais (``\\n``, ``\\t``, ``\\r`` escritos como texto) vindos do banco.

        Args:
            texto: Texto bruto.

        Returns:
            Número de ocorrências.
        """
        return len(self._RE_ESCAPE_LITERAL.findall(texto))

    def tem_html_de_editor(self, html_bruto: str) -> bool:
        """Indica se o texto traz marcação colada de editor (Word: ``mso-``, ``<w:>``, comentários condicionais).

        Args:
            html_bruto: Texto com HTML.

        Returns:
            ``True`` se houver marcação de editor.
        """
        return self._RE_EDITOR.search(html_bruto) is not None

    def achatar(self, texto: str) -> str:
        """Coloca o texto numa única linha, com espaços simples.

        Args:
            texto: Texto qualquer.

        Returns:
            Texto sem quebras de linha nem espaços repetidos.
        """
        return self._RE_BRANCOS.sub(" ", texto).strip()

    def trecho(self, texto: str, limite: int) -> str:
        """Gera um trecho de uma linha para exibição em tabelas.

        Args:
            texto: Texto a resumir.
            limite: Número máximo de caracteres.

        Returns:
            Texto achatado, cortado com reticências se passar do limite.
        """
        plano: str = self.achatar(texto)
        return plano if len(plano) <= limite else plano[: limite - 1].rstrip() + "…"

    def nomes_tags(self, html_bruto: str) -> list[str]:
        """Lista os nomes das tags HTML de abertura encontradas.

        Args:
            html_bruto: Texto com HTML.

        Returns:
            Nomes das tags em minúsculas, na ordem em que aparecem.
        """
        return [nome.lower() for nome in self._RE_NOME_TAG.findall(html_bruto)]

    def entidades(self, html_bruto: str) -> list[str]:
        """Lista as entidades HTML encontradas (``&nbsp;``, ``&#233;``...).

        Args:
            html_bruto: Texto com HTML.

        Returns:
            Entidades na ordem em que aparecem.
        """
        return self._RE_ENTIDADE.findall(html_bruto)

    def normalizar(self, texto: str) -> str:
        """Gera a forma de comparação: minúsculas, sem acento e só letras e números.

        Args:
            texto: Texto qualquer (pode conter HTML já limpo).

        Returns:
            Texto normalizado com palavras separadas por um espaço.
        """
        decomposto: str = unicodedata.normalize("NFKD", texto)
        sem_acento: str = "".join(caractere for caractere in decomposto if not unicodedata.combining(caractere))
        return self._RE_NAO_ALFANUMERICO.sub(" ", sem_acento.lower()).strip()

    def tokens(self, texto: str) -> list[str]:
        """Separa o texto normalizado em palavras.

        Args:
            texto: Texto qualquer.

        Returns:
            Palavras normalizadas.
        """
        normalizado: str = self.normalizar(texto)
        return normalizado.split() if normalizado else []

    def singular(self, token: str) -> str:
        """Reduz uma palavra normalizada ao singular com regras simples do português.

        Não é um lematizador: serve para que "Espécie" e "Espécies" ou
        "Penal" e "Penais" virem a mesma chave de comparação.

        Args:
            token: Palavra normalizada (sem acento, minúscula).

        Returns:
            Forma aproximada no singular.
        """
        if len(token) <= 3 or token.isdigit():
            return token
        sufixo: str
        troca: str
        for sufixo, troca in self._SUFIXOS_PLURAL:
            if token.endswith(sufixo):
                return token[: -len(sufixo)] + troca
        if token.endswith(("res", "zes", "ses")):
            return token[:-2]
        if token.endswith("s"):
            return token[:-1]
        return token

    def tem_parte(self, texto: str) -> bool:
        """Indica se o texto tem um marcador do tipo "(Parte 02)".

        Args:
            texto: Título ou assunto.

        Returns:
            ``True`` se houver o marcador.
        """
        return self._RE_PARTE.search(texto) is not None

    def remover_parte(self, texto: str) -> str:
        """Remove marcadores do tipo "(Parte 02)" de um título ou assunto.

        Args:
            texto: Título ou assunto.

        Returns:
            Texto sem o marcador e sem espaços nas pontas.
        """
        return self.achatar(self._RE_PARTE.sub(" ", texto))

    def chave_comparacao(self, texto: str, manter_parte: bool) -> str:
        """Gera a chave usada para comparar títulos e assuntos.

        A chave é normalizada, sem palavras de ligação, no singular e com
        números sem zeros à esquerda ("Parte 02" e "Parte 2" coincidem).

        Args:
            texto: Título ou assunto.
            manter_parte: Se ``False``, remove o marcador "(Parte N)" antes.

        Returns:
            Palavras da chave separadas por espaço.
        """
        base: str = texto if manter_parte else self.remover_parte(texto)
        partes: list[str] = []
        token: str
        for token in self.tokens(base):
            if token in self.PALAVRAS_LIGACAO:
                continue
            partes.append(str(int(token)) if token.isdigit() else self.singular(token))
        return " ".join(partes)

    def similaridade(self, texto_a: str, texto_b: str) -> float:
        """Mede a semelhança entre dois títulos, de 0 a 1.

        Usa o maior valor entre a sobreposição de palavras (Jaccard) e a
        semelhança de sequência de caracteres, ambas sobre a chave de
        comparação sem "(Parte N)". A segunda pega erros de digitação.

        Args:
            texto_a: Primeiro título.
            texto_b: Segundo título.

        Returns:
            Similaridade entre 0 (nada em comum) e 1 (iguais).
        """
        chave_a: str = self.chave_comparacao(texto_a, manter_parte=False)
        chave_b: str = self.chave_comparacao(texto_b, manter_parte=False)
        if not chave_a or not chave_b:
            return 0.0
        palavras_a: set[str] = set(chave_a.split())
        palavras_b: set[str] = set(chave_b.split())
        jaccard: float = len(palavras_a & palavras_b) / len(palavras_a | palavras_b)
        sequencia: float = SequenceMatcher(None, chave_a, chave_b).ratio()
        return max(jaccard, sequencia)
