"""Respostas dos classificadores e do verificador, e a linha de sinais por questão (ADR-008)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass
from typing import Literal

from vicio_ia.leitura_json import CamposJSON, ErroCampoJSON

type Veredito = Literal["confirma", "pai", "filho", "irmao", "outro", "nenhum", "falha", "nao_rodou"]
"""Resposta do verificador em relação ao candidato.

* ``confirma``: escolheu o próprio candidato;
* ``pai`` / ``filho``: escolheu o pai ou um filho direto (mesmo ramo, conta na régua);
* ``irmao``: escolheu um irmão (erro na régua);
* ``outro``: escolheu um nó de outro ramo (ex.: o par de sobreposição);
* ``nenhum``: nenhum cartão serve;
* ``falha`` / ``nao_rodou``: sem veredito.
"""


@dataclass(frozen=True)
class VotoClassificador:
    """Resposta de um classificador (A, B ou voto barato) para uma questão.

    Attributes:
        papel: Papel (``classificador_a``, ``classificador_b``, ``voto_barato``).
        provedor: Provedor que respondeu.
        modelo: Modelo que respondeu.
        versao_prompt: Versões dos prompts usados (B usa dois, separados por ``+``).
        ok: A resposta foi válida.
        erro: Mensagem de erro quando ``ok`` é falso.
        tema_id: Tema escolhido ("" se falhou).
        segundo_id: Segundo colocado ("" se não houver).
        extras_ids: Temas de outros ramos também cobertos.
        nucleo: Núcleo cobrado, em uma frase.
        fora: Nenhum tema serve.
        multitema: Cobre temas diferentes por igual.
        autoconfianca: Probabilidade autodeclarada de acerto (``None`` se o papel não informa).
        etapas: Temas escolhidos em cada etapa (B: nível 1 e subtema).
        do_cache: Todas as chamadas vieram do cache.
        latencia_s: Soma das latências das chamadas.
    """

    papel: str
    provedor: str
    modelo: str
    versao_prompt: str
    ok: bool
    erro: str
    tema_id: str
    segundo_id: str
    extras_ids: tuple[str, ...]
    nucleo: str
    fora: bool
    multitema: bool
    autoconfianca: float | None
    etapas: tuple[str, ...]
    do_cache: bool
    latencia_s: float

    @classmethod
    def falha(cls, papel: str, provedor: str, modelo: str, versao_prompt: str, erro: str) -> VotoClassificador:
        """Cria o voto de uma chamada que falhou.

        Args:
            papel: Papel.
            provedor: Provedor.
            modelo: Modelo.
            versao_prompt: Versão do prompt.
            erro: Mensagem de erro.

        Returns:
            Voto sem tema.
        """
        return cls(
            papel, provedor, modelo, versao_prompt, False, erro, "", "", (), "", False, False, None, (), False, 0.0
        )

    @classmethod
    def de_dict(cls, objeto: Mapping[str, object], origem: str) -> VotoClassificador:
        """Reconstrói um voto lido do disco.

        Args:
            objeto: Objeto decodificado.
            origem: Descrição da origem (para mensagens de erro).

        Returns:
            Voto.
        """
        campos: CamposJSON = CamposJSON(objeto, origem)
        return cls(
            papel=campos.texto("papel"),
            provedor=campos.texto("provedor"),
            modelo=campos.texto("modelo"),
            versao_prompt=campos.texto("versao_prompt"),
            ok=campos.booleano("ok"),
            erro=campos.texto("erro"),
            tema_id=campos.texto("tema_id"),
            segundo_id=campos.texto("segundo_id"),
            extras_ids=campos.textos("extras_ids"),
            nucleo=campos.texto("nucleo"),
            fora=campos.booleano("fora"),
            multitema=campos.booleano("multitema"),
            autoconfianca=campos.numero_opcional("autoconfianca"),
            etapas=campos.textos("etapas"),
            do_cache=campos.booleano("do_cache"),
            latencia_s=campos.numero("latencia_s"),
        )


@dataclass(frozen=True)
class VereditoVerificador:
    """Resposta do verificador contrastivo.

    Attributes:
        veredito: Relação da escolha com o candidato.
        candidato_id: Candidato preliminar conferido ("" se não rodou).
        escolha_id: Cartão escolhido (``nenhum`` possível).
        opcoes: Cartões mostrados.
        nucleo: Núcleo cobrado, em uma frase.
        justificativa: Por que a escolha vence o vizinho mais parecido.
        confianca: Probabilidade autodeclarada.
        motivo: Por que não rodou, ou o erro.
        provedor: Provedor.
        modelo: Modelo.
        versao_prompt: Versão do prompt.
        do_cache: Veio do cache.
        latencia_s: Latência.
    """

    veredito: Veredito
    candidato_id: str
    escolha_id: str
    opcoes: tuple[str, ...]
    nucleo: str
    justificativa: str
    confianca: float | None
    motivo: str
    provedor: str
    modelo: str
    versao_prompt: str
    do_cache: bool
    latencia_s: float

    @classmethod
    def nao_rodou(cls, motivo: str) -> VereditoVerificador:
        """Cria o registro de verificação não feita.

        Args:
            motivo: Por que não rodou.

        Returns:
            Veredito ``nao_rodou``.
        """
        return cls("nao_rodou", "", "", (), "", "", None, motivo, "", "", "", False, 0.0)

    @classmethod
    def de_dict(cls, objeto: Mapping[str, object], origem: str) -> VereditoVerificador:
        """Reconstrói um veredito lido do disco.

        Args:
            objeto: Objeto decodificado.
            origem: Descrição da origem.

        Returns:
            Veredito.

        Raises:
            ErroCampoJSON: Se o veredito for desconhecido.
        """
        campos: CamposJSON = CamposJSON(objeto, origem)
        vereditos: dict[str, Veredito] = {
            "confirma": "confirma",
            "pai": "pai",
            "filho": "filho",
            "irmao": "irmao",
            "outro": "outro",
            "nenhum": "nenhum",
            "falha": "falha",
            "nao_rodou": "nao_rodou",
        }
        valor: str = campos.texto("veredito")
        if valor not in vereditos:
            raise ErroCampoJSON(f"{origem}: veredito inválido {valor!r}")
        return cls(
            veredito=vereditos[valor],
            candidato_id=campos.texto("candidato_id"),
            escolha_id=campos.texto("escolha_id"),
            opcoes=campos.textos("opcoes"),
            nucleo=campos.texto("nucleo"),
            justificativa=campos.texto("justificativa"),
            confianca=campos.numero_opcional("confianca"),
            motivo=campos.texto("motivo"),
            provedor=campos.texto("provedor"),
            modelo=campos.texto("modelo"),
            versao_prompt=campos.texto("versao_prompt"),
            do_cache=campos.booleano("do_cache"),
            latencia_s=campos.numero("latencia_s"),
        )


@dataclass(frozen=True)
class SinaisQuestao:
    """Tudo o que o passo 05/06 produziu para uma questão (uma linha de ``sinais.jsonl``).

    Attributes:
        id: ID da questão.
        votos: Votos de A, B e do voto barato.
        leis: Leis citadas.
        regras: Temas indicados pelas leis citadas (sinal fraco, só publicáveis).
        verificador: Veredito do verificador.
    """

    id: str
    votos: tuple[VotoClassificador, ...]
    leis: tuple[str, ...]
    regras: tuple[str, ...]
    verificador: VereditoVerificador

    def voto(self, papel: str) -> VotoClassificador | None:
        """Busca o voto de um papel.

        Args:
            papel: Papel.

        Returns:
            O voto, ou ``None`` se o papel não votou.
        """
        return next((voto for voto in self.votos if voto.papel == papel), None)

    def como_dict(self) -> dict[str, object]:
        """Converte em dicionário serializável.

        Returns:
            Dicionário.
        """
        return asdict(self)

    @classmethod
    def de_dict(cls, objeto: Mapping[str, object], origem: str) -> SinaisQuestao:
        """Reconstrói a linha lida do disco.

        Args:
            objeto: Objeto decodificado.
            origem: Descrição da origem.

        Returns:
            Sinais da questão.

        Raises:
            ErroCampoJSON: Se a estrutura estiver errada.
        """
        campos: CamposJSON = CamposJSON(objeto, origem)
        brutos: object = objeto.get("votos")
        if not isinstance(brutos, list):
            raise ErroCampoJSON(f"{origem}: votos deveria ser lista")
        votos: list[VotoClassificador] = []
        bruto: object
        for bruto in brutos:
            if not isinstance(bruto, dict):
                raise ErroCampoJSON(f"{origem}: voto deveria ser objeto")
            votos.append(VotoClassificador.de_dict({str(k): v for k, v in bruto.items()}, f"{origem}, voto"))
        return cls(
            id=campos.texto("id"),
            votos=tuple(votos),
            leis=campos.textos("leis"),
            regras=campos.textos("regras"),
            verificador=VereditoVerificador.de_dict(campos.objeto("verificador"), f"{origem}, verificador"),
        )
