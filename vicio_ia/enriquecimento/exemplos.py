"""Exemplos sintéticos por tema (ADR-021, decisão 6): questões-modelo propostas por LLM, só a partir do tema.

Uma chamada por grupo de irmãos, os mesmos grupos das propostas de conhecimento (ADR-020). A entrada só tem a
árvore, o cartão e os vizinhos de cada tema; **nenhuma questão real** entra na chamada, e o schema da resposta não
tem campo de questão real (ADR-019). O resultado vai para ``dados/conhecimento/exemplos_sinteticos.jsonl``. Medido
no experimento E13 e adotado, ele vira dois atributos do ranqueador (similaridade com os exemplos do tema e do ramo).
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, TextIO

from vicio_ia.configuracao import Caminhos, ParametrosConhecimento, ParametrosLLM
from vicio_ia.enriquecimento.manifesto import Manifesto
from vicio_ia.enriquecimento.propostas import GeradorPropostas, GrupoTemas
from vicio_ia.llm.cliente import ClienteLLM, FabricaClientes, ResultadoChamada
from vicio_ia.llm.contratos import ErroProvedor, RequisicaoLLM
from vicio_ia.llm.prompts import ArquivoPrompt
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.temas.cartoes import ArquivoCartoes, CartaoTema


class ErroExemplos(Exception):
    """O modelo não devolveu os exemplos pedidos, mesmo depois de repetir a chamada."""


@dataclass(frozen=True)
class ExemplosTema:
    """Questões-modelo de um tema.

    Attributes:
        tema_id: Tema.
        exemplos: Textos das questões-modelo.
    """

    tema_id: str
    exemplos: tuple[str, ...]


class GeradorExemplos:
    """Pede as questões-modelo de cada grupo de irmãos, em paralelo, com cache (ADR-003)."""

    POR_TEMA: ClassVar[int] = 3
    MIN_CARACTERES: ClassVar[int] = 80

    def __init__(
        self,
        cliente: ClienteLLM,
        prompt: ArquivoPrompt,
        grupos: Sequence[GrupoTemas],
        arvore_enxuta: str,
        cartoes: Sequence[CartaoTema],
        parametros: ParametrosConhecimento,
        paralelismo: int,
    ) -> None:
        """Guarda as dependências.

        Args:
            cliente: Cliente do papel ``exemplos``.
            prompt: ``prompts/exemplos_tema.md``.
            grupos: Grupos de irmãos (os mesmos das propostas).
            arvore_enxuta: Árvore enxuta (vai no prompt de sistema).
            cartoes: Cartões da etapa 1.
            parametros: Parâmetros da fase de conhecimento.
            paralelismo: Chamadas simultâneas.
        """
        self._cliente: ClienteLLM = cliente
        self._prompt: ArquivoPrompt = prompt
        self._grupos: tuple[GrupoTemas, ...] = tuple(grupos)
        self._sistema: str = prompt.preencher({"arvore": arvore_enxuta.strip()})
        self._cartoes: dict[str, CartaoTema] = {c.tema_id: c for c in cartoes}
        self._parametros: ParametrosConhecimento = parametros
        self._paralelismo: int = paralelismo

    def gerar(self) -> list[ExemplosTema]:
        """Gera os exemplos de todos os grupos.

        Returns:
            Exemplos por tema, na ordem dos grupos.

        Raises:
            ErroExemplos: Se algum grupo falhar.
        """
        resultados: dict[str, list[ExemplosTema]] = {}
        falhas: list[str] = []
        executor: ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=self._paralelismo) as executor:
            futuros: dict[Future[list[ExemplosTema]], GrupoTemas] = {
                executor.submit(self._gerar_grupo, grupo): grupo for grupo in self._grupos
            }
            feito: Future[list[ExemplosTema]]
            posicao: int
            for posicao, feito in enumerate(as_completed(futuros), start=1):
                grupo: GrupoTemas = futuros[feito]
                try:
                    resultados[grupo.rotulo] = feito.result()
                except (ErroProvedor, ErroExemplos) as erro:
                    falhas.append(f"{grupo.rotulo}: {erro}")
                    print(f"  [{posicao}/{len(self._grupos)}] {grupo.rotulo}: FALHOU ({erro})")
                    continue
                print(f"  [{posicao}/{len(self._grupos)}] {grupo.rotulo}: {len(resultados[grupo.rotulo])} temas")
        if falhas:
            raise ErroExemplos("; ".join(falhas))
        return [e for grupo in self._grupos for e in resultados[grupo.rotulo]]

    def _gerar_grupo(self, grupo: GrupoTemas) -> list[ExemplosTema]:
        """Chama o modelo para um grupo, repetindo uma vez se a resposta vier incompleta.

        Args:
            grupo: Grupo.

        Returns:
            Exemplos dos temas do grupo.

        Raises:
            ErroExemplos: Se a segunda tentativa também vier incompleta.
        """
        requisicao: RequisicaoLLM = RequisicaoLLM(
            sistema=self._sistema,
            usuario=self._tarefa(grupo),
            schema=self._schema(grupo),
            nome_schema="exemplos_de_tema",
            max_tokens=self._parametros.max_tokens_saida,
        )
        ultimo_erro: str = ""
        tentativa: int
        for tentativa in (1, 2):
            resultado: ResultadoChamada = self._cliente.gerar(requisicao, self._prompt.versao, grupo.rotulo, tentativa)
            try:
                return self._converter(grupo, resultado.resposta.dados or {})
            except ErroExemplos as erro:
                ultimo_erro = str(erro)
        raise ErroExemplos(ultimo_erro)

    def _tarefa(self, grupo: GrupoTemas) -> str:
        """Mensagem da tarefa de um grupo (só temas; nenhuma questão real).

        Args:
            grupo: Grupo.

        Returns:
            Texto da tarefa.
        """
        linhas: list[str] = [
            "# Tarefa",
            "",
            (
                f"Escreva {self.POR_TEMA} questões-modelo para cada um dos {len(grupo.alvos)} nós abaixo, filhos de "
                f"**{grupo.pai.caminho_exibicao}** (ID {grupo.pai.tema_id})."
            ),
            "",
            "## Nós",
            "",
        ]
        alvo: TemaPreparado
        for alvo in grupo.alvos:
            linhas.append(f"### {alvo.tema_id} | {alvo.caminho_exibicao}")
            cartao: CartaoTema | None = self._cartoes.get(alvo.tema_id)
            if cartao is not None:
                linhas.append(f"- Escopo: {cartao.escopo}")
                if cartao.inclui:
                    linhas.append("- Costuma incluir: " + "; ".join(cartao.inclui))
                if cartao.nao_inclui:
                    linhas.append("- Não inclui (é de outro nó): " + "; ".join(n.assunto for n in cartao.nao_inclui))
            linhas.append("")
        if grupo.irmaos_fora:
            linhas.extend(["## Outros filhos do mesmo pai (só contexto; não escreva para eles)", ""])
            linhas.extend(f"- {irmao.tema_id} | {irmao.titulo_exibicao}" for irmao in grupo.irmaos_fora)
        return "\n".join(linhas).strip() + "\n"

    def _schema(self, grupo: GrupoTemas) -> dict[str, object]:
        """JSON Schema da resposta: IDs em ``enum`` e três textos por tema.

        Args:
            grupo: Grupo.

        Returns:
            Schema.
        """
        item: dict[str, object] = {
            "type": "object",
            "properties": {
                "tema_id": {"type": "string", "enum": [a.tema_id for a in grupo.alvos]},
                "exemplos": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": self.POR_TEMA,
                    "maxItems": self.POR_TEMA,
                },
            },
            "required": ["tema_id", "exemplos"],
            "additionalProperties": False,
        }
        return {
            "type": "object",
            "properties": {"temas": {"type": "array", "items": item}},
            "required": ["temas"],
            "additionalProperties": False,
        }

    def _converter(self, grupo: GrupoTemas, dados: Mapping[str, object]) -> list[ExemplosTema]:
        """Confere a resposta: todo nó do grupo precisa de exemplos com tamanho mínimo.

        Args:
            grupo: Grupo pedido.
            dados: Resposta estruturada.

        Returns:
            Exemplos por tema, na ordem do grupo.

        Raises:
            ErroExemplos: Se faltar nó ou exemplo válido.
        """
        itens: object = dados.get("temas")
        if not isinstance(itens, list):
            raise ErroExemplos("resposta sem a lista 'temas'")
        por_tema: dict[str, tuple[str, ...]] = {}
        item: object
        for item in itens:
            if not isinstance(item, dict):
                continue
            brutos: object = item.get("exemplos")
            textos: tuple[str, ...] = tuple(
                str(t).strip()
                for t in (brutos if isinstance(brutos, list) else [])
                if len(str(t).strip()) >= self.MIN_CARACTERES
            )
            if textos:
                por_tema.setdefault(str(item.get("tema_id", "")), textos)
        faltantes: list[str] = [a.tema_id for a in grupo.alvos if a.tema_id not in por_tema]
        if faltantes:
            raise ErroExemplos(f"faltam exemplos para {', '.join(faltantes)}")
        return [ExemplosTema(a.tema_id, por_tema[a.tema_id]) for a in grupo.alvos]


class PipelineExemplos:
    """Gera os exemplos e grava ``dados/conhecimento/exemplos_sinteticos.jsonl``."""

    COMANDO: ClassVar[str] = "uv run python executar_exemplos.py"
    PAPEL: ClassVar[str] = "exemplos"

    def __init__(self, caminhos: Caminhos | None = None) -> None:
        """Define a configuração.

        Args:
            caminhos: Caminhos do projeto.
        """
        self._caminhos: Caminhos = caminhos or Caminhos.padrao()

    def executar(self) -> Path:
        """Gera e grava.

        Returns:
            Caminho do arquivo.
        """
        leitor: LeitorPreparados = LeitorPreparados(self._caminhos)
        temas: list[TemaPreparado] = leitor.temas()
        cartoes: list[CartaoTema] = ArquivoCartoes(self._caminhos.dados_temas / "cartoes.jsonl").ler()
        p: ParametrosConhecimento = ParametrosConhecimento()
        fabrica: FabricaClientes = FabricaClientes(self._caminhos, ParametrosLLM())
        cliente: ClienteLLM = fabrica.cliente_fixo(self.PAPEL, p.provedor, p.modelo)
        prompt: ArquivoPrompt = ArquivoPrompt(self._caminhos.prompts / "exemplos_tema.md")
        grupos: list[GrupoTemas] = GeradorPropostas(
            cliente, prompt, temas, leitor.arvore_enxuta(), cartoes, p, 1
        ).grupos()
        print(f"Exemplos sintéticos: {len(grupos)} chamadas com {cliente.provedor}:{cliente.modelo} ({prompt.versao})")
        try:
            exemplos: list[ExemplosTema] = GeradorExemplos(
                cliente, prompt, grupos, leitor.arvore_enxuta(), cartoes, p, fabrica.paralelismo(cliente.provedor)
            ).gerar()
        finally:
            fabrica.escrever_resumo_custos()
            print(f"Chamadas: {fabrica.resumo_sessao()}")
        destino: Path = self._caminhos.dados_conhecimento / "exemplos_sinteticos.jsonl"
        destino.parent.mkdir(parents=True, exist_ok=True)
        arquivo: TextIO
        with destino.open("w", encoding="utf-8") as arquivo:
            exemplo: ExemplosTema
            for exemplo in exemplos:
                arquivo.write(
                    json.dumps({"tema_id": exemplo.tema_id, "exemplos": list(exemplo.exemplos)}, ensure_ascii=False)
                    + "\n"
                )
        Manifesto(self._caminhos.dados_conhecimento / "manifesto.json", self._caminhos.raiz).registrar(
            destino,
            "llm (proposta, sem revisão)",
            self.COMANDO,
            {
                "provedor": cliente.provedor,
                "modelo": cliente.modelo,
                "prompt": prompt.versao,
                "entrada": "árvore preparada e cartões da etapa 1; nenhuma questão real",
                "temas": str(len(exemplos)),
                "revisao": "pendente",
            },
        )
        print(f"{len(exemplos)} temas com exemplos. Arquivo: {destino}")
        return destino
