"""Base de conhecimento dos temas (ADR-020): um registro por tema publicável, lido como dado pela decisão.

Cada registro junta a identidade do tema na árvore, o cartão da etapa 1, as referências legais do mapa
revisado, os termos revisados (e os não revisados, marcados) e os IDs das questões da folha-verdade que têm o
tema como central ou extra. O texto de busca do tema sai daqui, numa de três variantes (E7b e E8b). As
questões da folha nunca entram no texto, só como IDs.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, TextIO

from vicio_ia.leitura_json import CamposJSON


@dataclass(frozen=True)
class ReferenciaTema:
    """Intervalo de artigos do mapa revisado.

    Attributes:
        lei: Lei canônica.
        inicio: Primeiro artigo.
        fim: Último artigo.
        forca: ``exata`` ou ``ramo``.
    """

    lei: str
    inicio: int
    fim: int
    forca: str


@dataclass(frozen=True)
class TermoTema:
    """Termo do dicionário.

    Attributes:
        termo: Termo como foi escrito.
        normalizado: Forma de comparação.
        tipo: ``forte``, ``fraco`` ou ``exclui``.
        alvo: Nó indicado por um ``exclui``; vazio nos demais.
        revisado: O autor revisou o termo (D14).
    """

    termo: str
    normalizado: str
    tipo: str
    alvo: str
    revisado: bool


@dataclass(frozen=True)
class TemaBase:
    """Registro de um tema publicável.

    Attributes:
        tema_id: ID do tema.
        caminho: Caminho de exibição.
        titulo: Título de exibição.
        nivel: 1 (tema) ou 2 (subtema).
        pai: ID do pai.
        irmaos: Irmãos publicáveis.
        filhos: Filhos publicáveis.
        escopo: Escopo do cartão.
        inclui: O que entra no tema (cartão).
        nao_inclui: ``(assunto, tema_id)`` do que parece do tema e é de outro nó (cartão).
        ancoras: Âncoras legais do cartão, em texto livre.
        referencias: Referências do mapa revisado.
        termos: Termos do dicionário.
        exemplos_folha: Questões da folha com o tema como central ou extra (só os IDs).
    """

    tema_id: str
    caminho: str
    titulo: str
    nivel: int
    pai: str
    irmaos: tuple[str, ...]
    filhos: tuple[str, ...]
    escopo: str
    inclui: tuple[str, ...]
    nao_inclui: tuple[tuple[str, str], ...]
    ancoras: tuple[str, ...]
    referencias: tuple[ReferenciaTema, ...]
    termos: tuple[TermoTema, ...]
    exemplos_folha: tuple[str, ...]

    VARIANTES: ClassVar[tuple[str, ...]] = ("cartao", "cartao_termos", "cartao_termos_leis")

    def texto(self, variante: str) -> str:
        """Texto de busca do tema.

        Args:
            variante: ``cartao``, ``cartao_termos`` ou ``cartao_termos_leis``.

        Returns:
            Texto com uma parte por linha.

        Raises:
            ValueError: Se a variante for desconhecida.
        """
        if variante not in self.VARIANTES:
            raise ValueError(f"variante de documento desconhecida: {variante!r}")
        partes: list[str] = [self.titulo, self.caminho, self.escopo, *self.inclui, *self.ancoras]
        if variante in {"cartao_termos", "cartao_termos_leis"}:
            partes.extend(t.termo for t in self.termos if t.tipo in {"forte", "fraco"})
        if variante == "cartao_termos_leis":
            partes.extend(self._referencia_por_extenso(r) for r in self.referencias)
        return "\n".join(p for p in partes if p)

    @staticmethod
    def _referencia_por_extenso(referencia: ReferenciaTema) -> str:
        """Referência legal em texto ("CP, arts. 121 a 128").

        Args:
            referencia: Referência.

        Returns:
            Texto.
        """
        if referencia.inicio == referencia.fim:
            return f"{referencia.lei}, art. {referencia.inicio}"
        return f"{referencia.lei}, arts. {referencia.inicio} a {referencia.fim}"

    def como_dict(self) -> dict[str, object]:
        """Converte em dicionário serializável em JSON.

        Returns:
            Dicionário com listas no lugar das tuplas.
        """
        return {
            "tema_id": self.tema_id,
            "caminho": self.caminho,
            "titulo": self.titulo,
            "nivel": self.nivel,
            "pai": self.pai,
            "irmaos": list(self.irmaos),
            "filhos": list(self.filhos),
            "escopo": self.escopo,
            "inclui": list(self.inclui),
            "nao_inclui": [{"assunto": a, "tema_id": t} for a, t in self.nao_inclui],
            "ancoras": list(self.ancoras),
            "referencias": [
                {"lei": r.lei, "inicio": r.inicio, "fim": r.fim, "forca": r.forca} for r in self.referencias
            ],
            "termos": [
                {"termo": t.termo, "normalizado": t.normalizado, "tipo": t.tipo, "alvo": t.alvo, "revisado": t.revisado}
                for t in self.termos
            ],
            "exemplos_folha": list(self.exemplos_folha),
        }

    @classmethod
    def de_dict(cls, objeto: Mapping[str, object], origem: str) -> TemaBase:
        """Reconstrói o registro lido do disco.

        Args:
            objeto: Linha decodificada.
            origem: Arquivo e linha (para mensagens de erro).

        Returns:
            Registro.
        """
        campos: CamposJSON = CamposJSON(objeto, origem)
        nao_inclui: list[tuple[str, str]] = []
        item: dict[str, object]
        for item in campos.objetos("nao_inclui"):
            nao: CamposJSON = CamposJSON(item, f"{origem}, nao_inclui")
            nao_inclui.append((nao.texto("assunto"), nao.texto("tema_id")))
        referencias: list[ReferenciaTema] = []
        for item in campos.objetos("referencias"):
            ref: CamposJSON = CamposJSON(item, f"{origem}, referencias")
            referencias.append(
                ReferenciaTema(ref.texto("lei"), ref.inteiro("inicio"), ref.inteiro("fim"), ref.texto("forca"))
            )
        termos: list[TermoTema] = []
        for item in campos.objetos("termos"):
            termo: CamposJSON = CamposJSON(item, f"{origem}, termos")
            termos.append(
                TermoTema(
                    termo.texto("termo"),
                    termo.texto("normalizado"),
                    termo.texto("tipo"),
                    termo.texto("alvo"),
                    termo.booleano("revisado"),
                )
            )
        return cls(
            tema_id=campos.texto("tema_id"),
            caminho=campos.texto("caminho"),
            titulo=campos.texto("titulo"),
            nivel=campos.inteiro("nivel"),
            pai=campos.texto("pai"),
            irmaos=campos.textos("irmaos"),
            filhos=campos.textos("filhos"),
            escopo=campos.texto("escopo"),
            inclui=campos.textos("inclui"),
            nao_inclui=tuple(nao_inclui),
            ancoras=campos.textos("ancoras"),
            referencias=tuple(referencias),
            termos=tuple(termos),
            exemplos_folha=campos.textos("exemplos_folha"),
        )


class ArquivoBaseTemas:
    """Lê e grava ``dados/conhecimento/temas.jsonl`` (um tema por linha, na ordem da árvore)."""

    def __init__(self, caminho: Path) -> None:
        """Define o arquivo.

        Args:
            caminho: Arquivo JSONL.
        """
        self._caminho: Path = caminho

    def gravar(self, temas: Iterable[TemaBase]) -> Path:
        """Grava a base.

        Args:
            temas: Registros, na ordem desejada.

        Returns:
            O caminho gravado.
        """
        self._caminho.parent.mkdir(parents=True, exist_ok=True)
        arquivo: TextIO
        with self._caminho.open("w", encoding="utf-8") as arquivo:
            tema: TemaBase
            for tema in temas:
                arquivo.write(json.dumps(tema.como_dict(), ensure_ascii=False) + "\n")
        return self._caminho

    def ler(self) -> list[TemaBase]:
        """Lê a base.

        Returns:
            Registros, na ordem do arquivo.
        """
        temas: list[TemaBase] = []
        numero: int
        linha: str
        for numero, linha in enumerate(self._caminho.read_text(encoding="utf-8").splitlines(), start=1):
            if linha.strip():
                objeto: object = json.loads(linha)
                if isinstance(objeto, dict):
                    temas.append(TemaBase.de_dict(objeto, f"{self._caminho.name}:{numero}"))
        return temas
