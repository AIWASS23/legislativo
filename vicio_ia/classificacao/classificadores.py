"""Classificadores A (plano), B (hierárquico) e voto barato, com o mesmo contrato (ADR-008)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import ClassVar

from vicio_ia.classificacao.montador_prompt import MontadorPrompt
from vicio_ia.classificacao.respostas import VotoClassificador
from vicio_ia.classificacao.schemas import FabricaSchemas
from vicio_ia.llm.cliente import ClienteLLM, ResultadoChamada
from vicio_ia.llm.contratos import ErroProvedor, RequisicaoLLM
from vicio_ia.llm.prompts import ArquivoPrompt
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada
from vicio_ia.temas.arvore_prompt import MaterialArvore


@dataclass(frozen=True)
class RespostaEtapa:
    """Resposta válida de uma chamada.

    Attributes:
        dados: JSON decodificado.
        do_cache: Veio do cache.
        latencia_s: Latência registrada.
    """

    dados: dict[str, object]
    do_cache: bool
    latencia_s: float


class ErroRespostaInvalida(ErroProvedor):
    """A resposta veio, mas não respeita o schema (ID fora do permitido, campo ausente)."""


class Classificador(ABC):
    """Contrato comum: recebe a questão preparada e devolve um :class:`VotoClassificador`.

    Toda chamada passa pelo :class:`ClienteLLM` do papel (cache e custo, ADR-003). Uma
    resposta inválida é repetida uma vez (tentativa 2, outra chave no cache); se falhar de
    novo, o papel fica sem voto.
    """

    def __init__(self, cliente: ClienteLLM, montador: MontadorPrompt, schemas: FabricaSchemas) -> None:
        """Guarda as dependências comuns.

        Args:
            cliente: Cliente do papel.
            montador: Montador de requisições com checagem de limite.
            schemas: Fábrica de schemas.
        """
        self._cliente: ClienteLLM = cliente
        self._montador: MontadorPrompt = montador
        self._schemas: FabricaSchemas = schemas

    @property
    def cliente(self) -> ClienteLLM:
        """Cliente do papel."""
        return self._cliente

    @abstractmethod
    def classificar(self, questao: QuestaoPreparada) -> VotoClassificador:
        """Classifica uma questão.

        Args:
            questao: Questão preparada (só o texto canônico vai para o modelo).

        Returns:
            Voto (com ``ok`` falso se as duas tentativas falharem).
        """

    def _chamar(
        self,
        prompt: ArquivoPrompt,
        sistema: str,
        usuario: str,
        schema: Mapping[str, object],
        rotulo: str,
        permitidos: frozenset[str],
        max_tokens: int,
    ) -> RespostaEtapa:
        """Faz a chamada e valida ``tema_id`` contra os IDs permitidos, com uma repetição.

        Args:
            prompt: Prompt usado (versão na chave do cache).
            sistema: Prompt de sistema preenchido.
            usuario: Texto da questão.
            schema: Schema da resposta.
            rotulo: ID da questão (e etapa).
            permitidos: IDs aceitos em ``tema_id``.
            max_tokens: Limite de saída.

        Returns:
            Resposta válida.

        Raises:
            ErroProvedor: Se as duas tentativas falharem ou o prompt não couber no provedor.
        """
        requisicao: RequisicaoLLM = self._montador.requisicao(
            self._cliente.provedor, sistema, usuario, schema, prompt.nome, max_tokens
        )
        ultimo: str = ""
        tentativa: int
        for tentativa in (1, 2):
            try:
                resultado: ResultadoChamada = self._cliente.gerar(requisicao, prompt.versao, rotulo, tentativa)
            except ErroProvedor as erro:
                ultimo = str(erro)
                continue
            dados: dict[str, object] = resultado.resposta.dados or {}
            if str(dados.get("tema_id", "")) in permitidos:
                return RespostaEtapa(dados, resultado.do_cache, resultado.resposta.latencia_s)
            ultimo = f"tema_id fora do permitido: {dados.get('tema_id')!r}"
        raise ErroRespostaInvalida(f"{self._cliente.papel} {rotulo}: {ultimo}")

    def _voto(
        self,
        versao: str,
        dados: Mapping[str, object],
        tema_id: str,
        etapas: Sequence[str],
        do_cache: bool,
        latencia: float,
        autoconfianca: float | None,
    ) -> VotoClassificador:
        """Monta o voto a partir da resposta.

        Args:
            versao: Versão do prompt (ou das duas etapas).
            dados: Resposta da etapa principal (núcleo, segundo, extras, marcas).
            tema_id: Tema final.
            etapas: Temas escolhidos em cada etapa.
            do_cache: Todas as chamadas vieram do cache.
            latencia: Soma das latências.
            autoconfianca: Autoconfiança final.

        Returns:
            Voto válido.
        """
        segundo: str = str(dados.get("segundo_id", ""))
        extras_brutos: object = dados.get("extras_ids", [])
        extras: tuple[str, ...] = tuple(
            dict.fromkeys(
                str(item)
                for item in (extras_brutos if isinstance(extras_brutos, list) else [])
                if str(item) in self._schemas.publicaveis and str(item) != tema_id
            )
        )
        return VotoClassificador(
            papel=self._cliente.papel,
            provedor=self._cliente.provedor,
            modelo=self._cliente.modelo,
            versao_prompt=versao,
            ok=True,
            erro="",
            tema_id=tema_id,
            segundo_id=segundo if segundo != tema_id else "",
            extras_ids=extras[:3],
            nucleo=str(dados.get("nucleo", "")).strip(),
            fora=dados.get("fora") is True,
            multitema=dados.get("multitema") is True,
            autoconfianca=autoconfianca,
            etapas=tuple(etapas),
            do_cache=do_cache,
            latencia_s=round(latencia, 2),
        )

    @staticmethod
    def _confianca(dados: Mapping[str, object]) -> float | None:
        """Lê a autoconfiança, limitada a [0, 1].

        Args:
            dados: Resposta.

        Returns:
            Valor entre 0 e 1, ou ``None`` se ausente.
        """
        valor: object = dados.get("autoconfianca")
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            return None
        return min(1.0, max(0.0, float(valor if valor <= 1 else valor / 100)))


class ClassificadorPlano(Classificador):
    """Classificador A: a árvore inteira com o escopo de cada nó, numa chamada."""

    MAX_TOKENS: ClassVar[int] = 2000

    def __init__(
        self,
        cliente: ClienteLLM,
        montador: MontadorPrompt,
        schemas: FabricaSchemas,
        prompt: ArquivoPrompt,
        material: MaterialArvore,
        com_escopo: bool,
    ) -> None:
        """Prepara o prompt de sistema (estável entre questões).

        Args:
            cliente: Cliente do papel ``classificador_a``.
            montador: Montador de requisições.
            schemas: Fábrica de schemas.
            prompt: ``prompts/classificador_plano.md``.
            material: Versões da árvore.
            com_escopo: Usa a árvore com escopo (``False`` = só títulos, para o experimento E4).
        """
        super().__init__(cliente, montador, schemas)
        self._prompt: ArquivoPrompt = prompt
        self._sistema: str = prompt.preencher({"arvore": material.com_escopo() if com_escopo else material.enxuta})
        self._permitidos: frozenset[str] = frozenset(schemas.publicaveis)
        self._schema: dict[str, object] = schemas.completo(schemas.publicaveis)

    def classificar(self, questao: QuestaoPreparada) -> VotoClassificador:
        """Classifica com uma chamada.

        Args:
            questao: Questão preparada.

        Returns:
            Voto.
        """
        try:
            resposta: RespostaEtapa = self._chamar(
                self._prompt,
                self._sistema,
                questao.texto_canonico,
                self._schema,
                questao.id,
                self._permitidos,
                self.MAX_TOKENS,
            )
        except ErroProvedor as erro:
            return VotoClassificador.falha(
                self._cliente.papel, self._cliente.provedor, self._cliente.modelo, self._prompt.versao, str(erro)
            )
        tema: str = str(resposta.dados["tema_id"])
        return self._voto(
            self._prompt.versao,
            resposta.dados,
            tema,
            (tema,),
            resposta.do_cache,
            resposta.latencia_s,
            self._confianca(resposta.dados),
        )


class ClassificadorHierarquico(Classificador):
    """Classificador B: 1ª chamada escolhe o tema (nível 1); 2ª escolhe entre o tema e os subtemas."""

    MAX_TOKENS: ClassVar[int] = 2000

    def __init__(
        self,
        cliente: ClienteLLM,
        montador: MontadorPrompt,
        schemas: FabricaSchemas,
        prompt_tema: ArquivoPrompt,
        prompt_subtema: ArquivoPrompt,
        material: MaterialArvore,
        temas: Sequence[TemaPreparado],
    ) -> None:
        """Prepara o prompt da 1ª etapa e o índice dos filhos.

        Args:
            cliente: Cliente do papel ``classificador_b``.
            montador: Montador de requisições.
            schemas: Fábrica de schemas.
            prompt_tema: ``prompts/classificador_hierarquico_tema.md``.
            prompt_subtema: ``prompts/classificador_hierarquico_subtema.md``.
            material: Versões da árvore.
            temas: Árvore preparada.
        """
        super().__init__(cliente, montador, schemas)
        self._prompt_tema: ArquivoPrompt = prompt_tema
        self._prompt_subtema: ArquivoPrompt = prompt_subtema
        self._material: MaterialArvore = material
        self._sistema_tema: str = prompt_tema.preencher({"arvore": material.nivel1_com_escopo()})
        nivel1: list[str] = sorted(t.tema_id for t in temas if t.publicavel and t.nivel == 1)
        self._nivel1: frozenset[str] = frozenset(nivel1)
        self._schema_tema: dict[str, object] = schemas.completo(nivel1)
        por_id: dict[str, TemaPreparado] = {tema.tema_id: tema for tema in temas}
        self._filhos: dict[str, list[str]] = {
            tema_id: [f for f in por_id[tema_id].filhos if f in por_id and por_id[f].publicavel] for tema_id in nivel1
        }
        self._versao: str = f"{prompt_tema.versao}+{prompt_subtema.versao}"

    def classificar(self, questao: QuestaoPreparada) -> VotoClassificador:
        """Classifica em duas etapas (a 2ª só se o tema tiver subtemas).

        Args:
            questao: Questão preparada.

        Returns:
            Voto.
        """
        try:
            primeira: RespostaEtapa = self._chamar(
                self._prompt_tema,
                self._sistema_tema,
                questao.texto_canonico,
                self._schema_tema,
                f"{questao.id}:tema",
                self._nivel1,
                self.MAX_TOKENS,
            )
            tema: str = str(primeira.dados["tema_id"])
            filhos: list[str] = self._filhos.get(tema, [])
            if not filhos:
                return self._voto(
                    self._versao,
                    primeira.dados,
                    tema,
                    (tema,),
                    primeira.do_cache,
                    primeira.latencia_s,
                    self._confianca(primeira.dados),
                )
            opcoes: list[str] = [tema, *filhos]
            segunda: RespostaEtapa = self._chamar(
                self._prompt_subtema,
                self._prompt_subtema.preencher({"cartoes": self._material.cartoes_filhos(tema)}),
                questao.texto_canonico,
                self._schemas.subtema(opcoes),
                f"{questao.id}:subtema",
                frozenset(opcoes),
                self.MAX_TOKENS,
            )
        except ErroProvedor as erro:
            return VotoClassificador.falha(
                self._cliente.papel, self._cliente.provedor, self._cliente.modelo, self._versao, str(erro)
            )
        final: str = str(segunda.dados["tema_id"])
        conf_tema: float | None = self._confianca(primeira.dados)
        conf_sub: float | None = self._confianca(segunda.dados)
        confianca: float | None = conf_tema * conf_sub if conf_tema is not None and conf_sub is not None else None
        dados: dict[str, object] = dict(primeira.dados)
        dados["segundo_id"] = str(segunda.dados.get("segundo_id", "")) or str(primeira.dados.get("segundo_id", ""))
        dados["nucleo"] = str(segunda.dados.get("nucleo", "")) or str(primeira.dados.get("nucleo", ""))
        return self._voto(
            self._versao,
            dados,
            final,
            (tema, final),
            primeira.do_cache and segunda.do_cache,
            primeira.latencia_s + segunda.latencia_s,
            confianca,
        )


class VotoBarato(Classificador):
    """Voto barato: modelo pequeno com a árvore enxuta; só o tema."""

    MAX_TOKENS: ClassVar[int] = 600

    def __init__(
        self,
        cliente: ClienteLLM,
        montador: MontadorPrompt,
        schemas: FabricaSchemas,
        prompt: ArquivoPrompt,
        material: MaterialArvore,
    ) -> None:
        """Prepara o prompt de sistema.

        Args:
            cliente: Cliente do papel ``voto_barato``.
            montador: Montador de requisições.
            schemas: Fábrica de schemas.
            prompt: ``prompts/voto_barato.md``.
            material: Versões da árvore.
        """
        super().__init__(cliente, montador, schemas)
        self._prompt: ArquivoPrompt = prompt
        self._sistema: str = prompt.preencher({"arvore": material.enxuta.strip()})
        self._permitidos: frozenset[str] = frozenset(schemas.publicaveis)
        self._schema: dict[str, object] = schemas.simples()

    def classificar(self, questao: QuestaoPreparada) -> VotoClassificador:
        """Classifica com uma chamada.

        Args:
            questao: Questão preparada.

        Returns:
            Voto (sem autoconfiança).
        """
        try:
            resposta: RespostaEtapa = self._chamar(
                self._prompt,
                self._sistema,
                questao.texto_canonico,
                self._schema,
                questao.id,
                self._permitidos,
                self.MAX_TOKENS,
            )
        except ErroProvedor as erro:
            return VotoClassificador.falha(
                self._cliente.papel, self._cliente.provedor, self._cliente.modelo, self._prompt.versao, str(erro)
            )
        tema: str = str(resposta.dados["tema_id"])
        return self._voto(
            self._prompt.versao, resposta.dados, tema, (tema,), resposta.do_cache, resposta.latencia_s, None
        )
