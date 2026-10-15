"""Leitura das saídas do passo 01 (``dados/preparados/``) pelos passos seguintes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TextIO

from vicio_ia.configuracao import Caminhos
from vicio_ia.eda.perfil_questoes import FormatoQuestao, TipoComando
from vicio_ia.leitura_json import CamposJSON, ErroCampoJSON
from vicio_ia.preparacao.arvore_preparada import NivelLixeira, TemaPreparado, TipoConvencao
from vicio_ia.preparacao.texto_canonico import MarcasQuestao, MotivoComando, QuestaoPreparada


class ErroPreparadosAusentes(Exception):
    """As saídas do passo 01 não existem; é preciso rodar ``executar_preparacao.py``."""


class LeitorPreparados:
    """Lê ``questoes.jsonl`` e ``temas.json`` de volta para as dataclasses do passo 01."""

    def __init__(self, caminhos: Caminhos) -> None:
        """Define a pasta das saídas do passo 01.

        Args:
            caminhos: Caminhos do projeto.
        """
        self._pasta: Path = caminhos.dados_preparados

    def _exigir(self, nome: str) -> Path:
        """Confere que um arquivo do passo 01 existe.

        Args:
            nome: Nome do arquivo.

        Returns:
            Caminho do arquivo.

        Raises:
            ErroPreparadosAusentes: Se o arquivo não existir.
        """
        caminho: Path = self._pasta / nome
        if not caminho.is_file():
            raise ErroPreparadosAusentes(f"{caminho} não existe: rode `uv run python executar_preparacao.py`")
        return caminho

    def questoes(self) -> list[QuestaoPreparada]:
        """Lê as questões preparadas.

        Returns:
            Questões na ordem do arquivo.
        """
        questoes: list[QuestaoPreparada] = []
        arquivo: TextIO
        with self._exigir("questoes.jsonl").open(encoding="utf-8") as arquivo:
            linha: str
            for linha in arquivo:
                if linha.strip():
                    valor: object = json.loads(linha)
                    if not isinstance(valor, dict):
                        raise ErroCampoJSON("questoes.jsonl: linha não é um objeto")
                    questoes.append(self._questao({str(k): v for k, v in valor.items()}))
        return questoes

    def temas(self) -> list[TemaPreparado]:
        """Lê a árvore preparada.

        Returns:
            Nós na ordem do arquivo.
        """
        valor: object = json.loads(self._exigir("temas.json").read_text(encoding="utf-8"))
        if not isinstance(valor, list):
            raise ErroCampoJSON("temas.json: esperada uma lista")
        temas: list[TemaPreparado] = []
        item: object
        for item in valor:
            if not isinstance(item, dict):
                raise ErroCampoJSON("temas.json: item não é um objeto")
            temas.append(self._tema({str(k): v for k, v in item.items()}))
        return temas

    def arvore_enxuta(self) -> str:
        """Lê a árvore enxuta usada nos prompts.

        Returns:
            Texto da árvore.
        """
        return self._exigir("arvore_enxuta.txt").read_text(encoding="utf-8")

    @staticmethod
    def _questao(objeto: dict[str, object]) -> QuestaoPreparada:
        """Converte um objeto JSON em :class:`QuestaoPreparada`.

        Args:
            objeto: Linha de ``questoes.jsonl``.

        Returns:
            Questão preparada.
        """
        campos: CamposJSON = CamposJSON(objeto, f"questoes.jsonl, {objeto.get('id')}")
        marcas: CamposJSON = CamposJSON(campos.objeto("marcas"), f"questoes.jsonl, {objeto.get('id')}, marcas")
        formato: str = campos.texto("formato")
        tipo: str = campos.texto("tipo_comando")
        motivo: str = campos.texto("motivo_comando")
        return QuestaoPreparada(
            id=campos.texto("id"),
            formato=LeitorPreparados._formato(formato),
            texto_canonico=campos.texto("texto_canonico"),
            enunciado=campos.texto("enunciado"),
            comando=campos.texto("comando"),
            tipo_comando=LeitorPreparados._tipo_comando(tipo),
            motivo_comando=LeitorPreparados._motivo(motivo),
            alternativas=campos.dicionario_textos("alternativas"),
            marcas=MarcasQuestao(
                enunciado_generico=marcas.booleano("enunciado_generico"),
                html_de_editor=marcas.booleano("html_de_editor"),
                leis_citadas=marcas.textos("leis_citadas"),
                menciona_cp=marcas.booleano("menciona_cp"),
                menciona_cpp=marcas.booleano("menciona_cpp"),
                menciona_cf=marcas.booleano("menciona_cf"),
                menciona_jurisprudencia=marcas.booleano("menciona_jurisprudencia"),
            ),
            hash_completo=campos.texto("hash_completo"),
            duplicata_de=campos.texto_opcional("duplicata_de"),
            caracteres=campos.inteiro("caracteres"),
            tokens_estimados=campos.inteiro("tokens_estimados"),
            original=campos.objeto("original"),
        )

    @staticmethod
    def _formato(valor: str) -> FormatoQuestao:
        """Converte o texto do formato no tipo literal.

        Args:
            valor: Texto lido.

        Returns:
            Formato da questão.
        """
        formatos: dict[str, FormatoQuestao] = {
            "multipla_escolha_5": "multipla_escolha_5",
            "multipla_escolha_4": "multipla_escolha_4",
            "certo_errado": "certo_errado",
            "outro": "outro",
        }
        if valor not in formatos:
            raise ErroCampoJSON(f"questoes.jsonl: formato inválido {valor!r}")
        return formatos[valor]

    @staticmethod
    def _tipo_comando(valor: str) -> TipoComando:
        """Converte o texto do tipo de comando no tipo literal.

        Args:
            valor: Texto lido.

        Returns:
            Tipo do comando.
        """
        tipos: dict[str, TipoComando] = {
            "vazio": "vazio",
            "repete_enunciado": "repete_enunciado",
            "suspeito": "suspeito",
            "util": "util",
        }
        if valor not in tipos:
            raise ErroCampoJSON(f"questoes.jsonl: tipo_comando inválido {valor!r}")
        return tipos[valor]

    @staticmethod
    def _motivo(valor: str) -> MotivoComando:
        """Converte o texto do motivo do comando no tipo literal.

        Args:
            valor: Texto lido.

        Returns:
            Motivo do comando.
        """
        motivos: dict[str, MotivoComando] = {
            "incluido": "incluido",
            "vazio": "vazio",
            "suspeito": "suspeito",
            "repete_enunciado": "repete_enunciado",
            "so_frase_padrao": "so_frase_padrao",
        }
        if valor not in motivos:
            raise ErroCampoJSON(f"questoes.jsonl: motivo_comando inválido {valor!r}")
        return motivos[valor]

    @staticmethod
    def _tema(objeto: dict[str, object]) -> TemaPreparado:
        """Converte um objeto JSON em :class:`TemaPreparado`.

        Args:
            objeto: Item de ``temas.json``.

        Returns:
            Nó preparado.
        """
        campos: CamposJSON = CamposJSON(objeto, f"temas.json, {objeto.get('tema_id')}")
        lixeiras: dict[str, NivelLixeira] = {"forte": "forte", "moderada": "moderada", "": ""}
        tipos: dict[str, TipoConvencao] = {
            "duplicado_outra_disciplina": "duplicado_outra_disciplina",
            "sobreposicao": "sobreposicao",
            "duplicado_parte": "duplicado_parte",
            "": "",
        }
        lixeira: str = campos.texto("lixeira")
        tipo: str = campos.texto("tipo_convencao")
        if lixeira not in lixeiras or tipo not in tipos:
            raise ErroCampoJSON(f"temas.json, {objeto.get('tema_id')}: lixeira ou tipo_convencao inválido")
        return TemaPreparado(
            tema_id=campos.texto("tema_id"),
            parent_id=campos.texto_opcional("parent_id"),
            disciplina=campos.texto("disciplina"),
            nivel=campos.inteiro("nivel"),
            titulo=campos.texto("titulo"),
            titulo_exibicao=campos.texto("titulo_exibicao"),
            caminho=campos.texto("caminho"),
            caminho_exibicao=campos.texto("caminho_exibicao"),
            status=campos.texto("status"),
            publicavel=campos.booleano("publicavel"),
            fantasma=campos.booleano("fantasma"),
            canonico_id=campos.texto_opcional("canonico_id"),
            duplicado_por=campos.textos("duplicado_por"),
            lixeira=lixeiras[lixeira],
            grupo_sobreposicao=campos.texto("grupo_sobreposicao"),
            regra_desempate=campos.texto("regra_desempate"),
            tipo_convencao=tipos[tipo],
            zona_convencao=campos.booleano("zona_convencao"),
            aceita_recuo=campos.booleano("aceita_recuo"),
            filhos=campos.textos("filhos"),
            n_questoes_origem=campos.inteiro_opcional("n_questoes_origem"),
        )
