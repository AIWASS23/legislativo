"""Cartões de tema (ADR-007): tipos, leitura e gravação, ajustes manuais e checagens."""

from __future__ import annotations

import csv
import json
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import ClassVar, TextIO

from vicio_ia.leitura_json import CamposJSON, ErroCampoJSON
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.validacao import ResultadoChecagem


class ErroCartoes(Exception):
    """Arquivo de cartões ou de ajustes inválido."""


@dataclass(frozen=True)
class ItemNaoInclui:
    """Assunto que parece do tema, mas pertence a outro nó.

    Attributes:
        assunto: Descrição curta do assunto.
        tema_id: Nó onde o assunto pertence.
    """

    assunto: str
    tema_id: str


@dataclass(frozen=True)
class CartaoTema:
    """Definição de um tema publicável.

    Attributes:
        tema_id: ID do nó.
        caminho: Caminho de exibição.
        titulo_exibicao: Título de exibição.
        escopo: O que o tema cobre (1–2 frases).
        inclui: Assuntos típicos do tema.
        nao_inclui: Assuntos parecidos que pertencem a outros nós.
        ancoras_legais: Dispositivos de referência.
        regra_desempate: Quando escolher este nó em vez do vizinho mais parecido.
        origem: ``gerado`` (rascunho do modelo) ou ``ajustado`` (com ajuste manual).
        modelo: Provedor e modelo que geraram o rascunho.
    """

    tema_id: str
    caminho: str
    titulo_exibicao: str
    escopo: str
    inclui: tuple[str, ...]
    nao_inclui: tuple[ItemNaoInclui, ...]
    ancoras_legais: tuple[str, ...]
    regra_desempate: str
    origem: str
    modelo: str

    def como_dict(self) -> dict[str, object]:
        """Converte o cartão num dicionário serializável.

        Returns:
            Dicionário.
        """
        return asdict(self)

    @classmethod
    def de_dict(cls, objeto: Mapping[str, object], origem: str) -> CartaoTema:
        """Reconstrói um cartão lido do disco.

        Args:
            objeto: Objeto decodificado.
            origem: Arquivo e linha (para mensagens de erro).

        Returns:
            Cartão.

        Raises:
            ErroCampoJSON: Se faltar campo ou o tipo estiver errado.
        """
        campos: CamposJSON = CamposJSON(objeto, origem)
        itens: object = objeto.get("nao_inclui")
        if not isinstance(itens, list):
            raise ErroCampoJSON(f"{origem}: nao_inclui deveria ser lista")
        nao_inclui: list[ItemNaoInclui] = []
        item: object
        for item in itens:
            if not isinstance(item, dict):
                raise ErroCampoJSON(f"{origem}: item de nao_inclui deveria ser objeto")
            campos_item: CamposJSON = CamposJSON({str(k): v for k, v in item.items()}, f"{origem}, nao_inclui")
            nao_inclui.append(ItemNaoInclui(campos_item.texto("assunto"), campos_item.texto("tema_id")))
        return cls(
            tema_id=campos.texto("tema_id"),
            caminho=campos.texto("caminho"),
            titulo_exibicao=campos.texto("titulo_exibicao"),
            escopo=campos.texto("escopo"),
            inclui=campos.textos("inclui"),
            nao_inclui=tuple(nao_inclui),
            ancoras_legais=campos.textos("ancoras_legais"),
            regra_desempate=campos.texto("regra_desempate"),
            origem=campos.texto("origem"),
            modelo=campos.texto("modelo"),
        )


class ArquivoCartoes:
    """Lê e grava cartões em JSONL (uma linha por cartão, na ordem da árvore)."""

    def __init__(self, caminho: Path) -> None:
        """Define o arquivo.

        Args:
            caminho: ``dados/temas/cartoes*.jsonl``.
        """
        self._caminho: Path = caminho

    @property
    def caminho(self) -> Path:
        """Caminho do arquivo."""
        return self._caminho

    def existe(self) -> bool:
        """Indica se o arquivo existe.

        Returns:
            ``True`` se existir.
        """
        return self._caminho.is_file()

    def ler(self) -> list[CartaoTema]:
        """Lê os cartões.

        Returns:
            Cartões na ordem do arquivo.

        Raises:
            ErroCartoes: Se o arquivo não existir.
        """
        if not self._caminho.is_file():
            raise ErroCartoes(f"{self._caminho} não existe: rode `uv run python executar_cartoes.py`")
        cartoes: list[CartaoTema] = []
        numero: int
        linha: str
        for numero, linha in enumerate(self._caminho.read_text(encoding="utf-8").splitlines(), start=1):
            if linha.strip():
                valor: object = json.loads(linha)
                if not isinstance(valor, dict):
                    raise ErroCartoes(f"{self._caminho.name}:{numero}: linha não é objeto")
                cartoes.append(
                    CartaoTema.de_dict({str(k): v for k, v in valor.items()}, f"{self._caminho.name}:{numero}")
                )
        return cartoes

    def gravar(self, cartoes: Sequence[CartaoTema]) -> None:
        """Grava os cartões.

        Args:
            cartoes: Cartões na ordem da árvore.
        """
        self._caminho.parent.mkdir(parents=True, exist_ok=True)
        texto: str = "".join(json.dumps(cartao.como_dict(), ensure_ascii=False) + "\n" for cartao in cartoes)
        self._caminho.write_text(texto, encoding="utf-8")


@dataclass(frozen=True)
class AjusteCartao:
    """Correção manual de um campo de um cartão.

    Attributes:
        tema_id: Nó corrigido.
        campo: ``escopo``, ``inclui``, ``nao_inclui``, ``ancoras_legais`` ou ``regra_desempate``.
        valor: Novo valor. Listas separadas por ``" | "``; em ``nao_inclui``, cada item é
            ``assunto -> tema_id``.
        motivo: Por que o rascunho foi corrigido.
    """

    tema_id: str
    campo: str
    valor: str
    motivo: str


class AjustesCartoes:
    """Lê e aplica ``dados/temas/cartoes_ajustes.csv`` (decisões manuais, D7)."""

    COLUNAS: ClassVar[tuple[str, ...]] = ("tema_id", "campo", "valor", "motivo")
    CAMPOS: ClassVar[frozenset[str]] = frozenset(
        {"escopo", "inclui", "nao_inclui", "ancoras_legais", "regra_desempate"}
    )
    SEPARADOR_LISTA: ClassVar[str] = " | "
    SEPARADOR_ITEM: ClassVar[str] = " -> "

    def __init__(self, caminho: Path) -> None:
        """Define o arquivo.

        Args:
            caminho: ``dados/temas/cartoes_ajustes.csv``.
        """
        self._caminho: Path = caminho

    def garantir(self) -> None:
        """Cria o arquivo só com o cabeçalho, se ele não existir."""
        if not self._caminho.is_file():
            self._caminho.parent.mkdir(parents=True, exist_ok=True)
            arquivo: TextIO
            with self._caminho.open("w", encoding="utf-8", newline="") as arquivo:
                csv.writer(arquivo).writerow(self.COLUNAS)

    def ler(self) -> list[AjusteCartao]:
        """Lê os ajustes.

        Returns:
            Ajustes na ordem do arquivo (vazio se o arquivo não existir).

        Raises:
            ErroCartoes: Se faltar coluna ou o campo for inválido.
        """
        if not self._caminho.is_file():
            return []
        ajustes: list[AjusteCartao] = []
        arquivo: TextIO
        with self._caminho.open(encoding="utf-8", newline="") as arquivo:
            leitor: csv.DictReader[str] = csv.DictReader(arquivo)
            faltantes: list[str] = [c for c in self.COLUNAS if c not in (leitor.fieldnames or [])]
            if faltantes:
                raise ErroCartoes(f"{self._caminho.name}: colunas ausentes {faltantes}")
            linha: dict[str, str]
            for linha in leitor:
                limpa: dict[str, str] = {chave: (valor or "").strip() for chave, valor in linha.items()}
                if limpa["campo"] not in self.CAMPOS:
                    raise ErroCartoes(f"{self._caminho.name}: campo inválido {limpa['campo']!r} em {limpa['tema_id']}")
                ajustes.append(AjusteCartao(limpa["tema_id"], limpa["campo"], limpa["valor"], limpa["motivo"]))
        return ajustes

    def aplicar(self, cartoes: Sequence[CartaoTema], ajustes: Sequence[AjusteCartao]) -> list[CartaoTema]:
        """Aplica os ajustes sobre os rascunhos.

        Args:
            cartoes: Rascunhos gerados.
            ajustes: Ajustes manuais.

        Returns:
            Cartões finais, na mesma ordem.

        Raises:
            ErroCartoes: Se um ajuste citar um tema sem cartão.
        """
        por_id: dict[str, CartaoTema] = {cartao.tema_id: cartao for cartao in cartoes}
        ajuste: AjusteCartao
        for ajuste in ajustes:
            if ajuste.tema_id not in por_id:
                raise ErroCartoes(f"ajuste para tema sem cartão: {ajuste.tema_id}")
            atual: CartaoTema = por_id[ajuste.tema_id]
            lista: tuple[str, ...] = tuple(
                parte.strip() for parte in ajuste.valor.split(self.SEPARADOR_LISTA.strip()) if parte.strip()
            )
            if ajuste.campo == "escopo":
                atual = replace(atual, escopo=ajuste.valor)
            elif ajuste.campo == "regra_desempate":
                atual = replace(atual, regra_desempate=ajuste.valor)
            elif ajuste.campo == "inclui":
                atual = replace(atual, inclui=lista)
            elif ajuste.campo == "ancoras_legais":
                atual = replace(atual, ancoras_legais=lista)
            else:
                atual = replace(atual, nao_inclui=tuple(self._item(parte, ajuste.tema_id) for parte in lista))
            por_id[ajuste.tema_id] = replace(atual, origem="ajustado")
        return [por_id[cartao.tema_id] for cartao in cartoes]

    def _item(self, texto: str, tema_id: str) -> ItemNaoInclui:
        """Converte ``assunto -> tema_id`` num item.

        Args:
            texto: Item escrito no CSV.
            tema_id: Tema do ajuste (para a mensagem de erro).

        Returns:
            Item.

        Raises:
            ErroCartoes: Se faltar a seta.
        """
        if self.SEPARADOR_ITEM.strip() not in texto:
            raise ErroCartoes(f"ajuste de {tema_id}: item de nao_inclui sem '->': {texto!r}")
        assunto: str
        destino: str
        assunto, destino = texto.rsplit(self.SEPARADOR_ITEM.strip(), 1)
        return ItemNaoInclui(assunto.strip(), destino.strip())


class ValidadorCartoes:
    """Checagens automáticas dos cartões. Se alguma falhar, os cartões finais não são gravados."""

    def __init__(self, max_chars_escopo: int) -> None:
        """Define os limites.

        Args:
            max_chars_escopo: Tamanho máximo do escopo.
        """
        self._max_escopo: int = max_chars_escopo

    def validar(self, cartoes: Sequence[CartaoTema], temas: Sequence[TemaPreparado]) -> list[ResultadoChecagem]:
        """Roda as checagens.

        Args:
            cartoes: Cartões finais.
            temas: Árvore preparada.

        Returns:
            Resultado de cada checagem.
        """
        publicaveis: dict[str, TemaPreparado] = {tema.tema_id: tema for tema in temas if tema.publicavel}
        ids: list[str] = [cartao.tema_id for cartao in cartoes]
        repetidos: list[str] = sorted({i for i in ids if ids.count(i) > 1})
        faltando: list[str] = sorted(set(publicaveis) - set(ids))
        sobrando: list[str] = sorted(set(ids) - set(publicaveis))
        destinos_invalidos: list[str] = [
            f"{c.tema_id}->{item.tema_id}" for c in cartoes for item in c.nao_inclui if item.tema_id not in publicaveis
        ]
        aponta_si: list[str] = [c.tema_id for c in cartoes if any(item.tema_id == c.tema_id for item in c.nao_inclui)]
        escopo_ruim: list[str] = [
            c.tema_id for c in cartoes if not c.escopo.strip() or len(c.escopo) > self._max_escopo
        ]
        sem_inclui: list[str] = [c.tema_id for c in cartoes if not c.inclui]
        regra_faltando: list[str] = [
            c.tema_id
            for c in cartoes
            if c.tema_id in publicaveis
            and (publicaveis[c.tema_id].lixeira == "forte" or publicaveis[c.tema_id].grupo_sobreposicao)
            and not c.regra_desempate.strip()
        ]
        return [
            ResultadoChecagem(
                "um cartão por tema publicável, sem repetição",
                not (repetidos or faltando or sobrando),
                tuple([*repetidos, *faltando, *sobrando][:20]),
            ),
            ResultadoChecagem(
                "nao_inclui aponta só para temas publicáveis", not destinos_invalidos, tuple(destinos_invalidos[:20])
            ),
            ResultadoChecagem("nao_inclui não aponta para o próprio tema", not aponta_si, tuple(aponta_si[:20])),
            ResultadoChecagem(
                f"escopo preenchido e com até {self._max_escopo} caracteres", not escopo_ruim, tuple(escopo_ruim[:20])
            ),
            ResultadoChecagem("inclui tem ao menos um item", not sem_inclui, tuple(sem_inclui[:20])),
            ResultadoChecagem(
                "lixeiras fortes e sobreposições têm regra de desempate", not regra_faltando, tuple(regra_faltando[:20])
            ),
        ]
