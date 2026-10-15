"""Geração dos rascunhos de cartão por LLM, uma chamada por tema pai (ADR-007)."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass

from vicio_ia.configuracao import ParametrosCartoes
from vicio_ia.llm.cliente import ClienteLLM, ResultadoChamada
from vicio_ia.llm.contratos import ErroProvedor, RequisicaoLLM
from vicio_ia.llm.prompts import ArquivoPrompt
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.temas.cartoes import CartaoTema, ItemNaoInclui


class ErroGeracaoCartoes(Exception):
    """O modelo não devolveu os cartões pedidos, mesmo depois de repetir a chamada."""


@dataclass(frozen=True)
class GrupoCartoes:
    """Nós de um mesmo pai cujos cartões são pedidos numa chamada.

    Attributes:
        rotulo: Identificação do grupo no cache (``filhos:5063`` ou ``filhos:5062:2``).
        pai: Disciplina ou tema pai.
        alvos: Nós que recebem cartão nesta chamada.
        irmaos_fora: Outros filhos do mesmo pai que ficaram em outro bloco.
    """

    rotulo: str
    pai: TemaPreparado
    alvos: tuple[TemaPreparado, ...]
    irmaos_fora: tuple[TemaPreparado, ...]


class GeradorCartoes:
    """Pede ao modelo os cartões de cada grupo, em paralelo, com cache (ADR-003)."""

    def __init__(
        self,
        cliente: ClienteLLM,
        prompt: ArquivoPrompt,
        temas: Sequence[TemaPreparado],
        arvore_enxuta: str,
        descricoes: Mapping[str, str],
        parametros: ParametrosCartoes,
        paralelismo: int,
    ) -> None:
        """Guarda as dependências.

        Args:
            cliente: Cliente do papel ``cartoes`` (modelo do verificador).
            prompt: ``prompts/cartao_tema.md``.
            temas: Árvore preparada.
            arvore_enxuta: Árvore enxuta (vai no prompt de sistema).
            descricoes: Descrições com conteúdo jurídico, por ID (só os nós que têm).
            parametros: Parâmetros do passo 02.
            paralelismo: Chamadas simultâneas.
        """
        self._cliente: ClienteLLM = cliente
        self._prompt: ArquivoPrompt = prompt
        self._temas: dict[str, TemaPreparado] = {tema.tema_id: tema for tema in temas}
        self._publicaveis: list[str] = sorted(tema.tema_id for tema in temas if tema.publicavel)
        self._sistema: str = prompt.preencher({"arvore": arvore_enxuta.strip()})
        self._descricoes: Mapping[str, str] = descricoes
        self._parametros: ParametrosCartoes = parametros
        self._paralelismo: int = paralelismo

    def grupos(self) -> list[GrupoCartoes]:
        """Monta os grupos: temas de nível 1 por disciplina e subtemas por tema pai.

        Pais com mais filhos que o limite são divididos em blocos de tamanho parecido.

        Returns:
            Grupos na ordem da árvore.
        """
        grupos: list[GrupoCartoes] = []
        pais: list[TemaPreparado] = sorted(
            (tema for tema in self._temas.values() if tema.nivel in (0, 1)), key=lambda t: (t.nivel, t.caminho)
        )
        pai: TemaPreparado
        for pai in pais:
            filhos: list[TemaPreparado] = sorted(
                (self._temas[i] for i in pai.filhos if i in self._temas and self._temas[i].publicavel),
                key=lambda t: t.caminho_exibicao,
            )
            if not filhos:
                continue
            blocos: int = math.ceil(len(filhos) / self._parametros.max_cartoes_por_chamada)
            tamanho: int = math.ceil(len(filhos) / blocos)
            indice: int
            for indice in range(blocos):
                alvos: tuple[TemaPreparado, ...] = tuple(filhos[indice * tamanho : (indice + 1) * tamanho])
                rotulo: str = f"filhos:{pai.tema_id}" if blocos == 1 else f"filhos:{pai.tema_id}:{indice + 1}"
                fora: tuple[TemaPreparado, ...] = tuple(f for f in filhos if f not in alvos)
                grupos.append(GrupoCartoes(rotulo, pai, alvos, fora))
        return grupos

    def gerar(self) -> list[CartaoTema]:
        """Gera os cartões de todos os grupos.

        Returns:
            Cartões ordenados pelo caminho de exibição.

        Raises:
            ErroGeracaoCartoes: Se algum grupo falhar duas vezes.
        """
        grupos: list[GrupoCartoes] = self.grupos()
        cartoes: list[CartaoTema] = []
        falhas: list[str] = []
        executor: ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=self._paralelismo) as executor:
            futuros: dict[Future[tuple[list[CartaoTema], bool]], GrupoCartoes] = {
                executor.submit(self._gerar_grupo, grupo): grupo for grupo in grupos
            }
            feito: Future[tuple[list[CartaoTema], bool]]
            posicao: int
            for posicao, feito in enumerate(as_completed(futuros), start=1):
                grupo: GrupoCartoes = futuros[feito]
                try:
                    resultado: tuple[list[CartaoTema], bool] = feito.result()
                except (ErroProvedor, ErroGeracaoCartoes) as erro:
                    falhas.append(f"{grupo.rotulo}: {erro}")
                    print(f"  [{posicao}/{len(grupos)}] {grupo.rotulo}: FALHOU ({erro})")
                    continue
                cartoes.extend(resultado[0])
                origem: str = "cache" if resultado[1] else "modelo"
                print(f"  [{posicao}/{len(grupos)}] {grupo.rotulo}: {len(resultado[0])} cartões ({origem})")
        if falhas:
            raise ErroGeracaoCartoes("; ".join(falhas))
        return sorted(cartoes, key=lambda cartao: (cartao.caminho, cartao.tema_id))

    def _gerar_grupo(self, grupo: GrupoCartoes) -> tuple[list[CartaoTema], bool]:
        """Chama o modelo para um grupo, repetindo uma vez se a resposta vier incompleta.

        Args:
            grupo: Grupo a gerar.

        Returns:
            ``(cartões, todas as respostas vieram do cache)``.

        Raises:
            ErroGeracaoCartoes: Se a segunda tentativa também vier incompleta.
            ErroProvedor: Se a chamada falhar.
        """
        requisicao: RequisicaoLLM = RequisicaoLLM(
            sistema=self._sistema,
            usuario=self._tarefa(grupo),
            schema=self._schema(grupo),
            nome_schema="cartoes_de_tema",
            max_tokens=self._parametros.max_tokens_saida,
        )
        ultimo_erro: str = ""
        tentativa: int
        for tentativa in (1, 2):
            resultado: ResultadoChamada = self._cliente.gerar(requisicao, self._prompt.versao, grupo.rotulo, tentativa)
            try:
                return self._converter(grupo, resultado.resposta.dados or {}, resultado), resultado.do_cache
            except ErroGeracaoCartoes as erro:
                ultimo_erro = str(erro)
        raise ErroGeracaoCartoes(f"{grupo.rotulo}: {ultimo_erro}")

    def _tarefa(self, grupo: GrupoCartoes) -> str:
        """Monta a mensagem da tarefa de um grupo.

        Args:
            grupo: Grupo.

        Returns:
            Texto da tarefa.
        """
        linhas: list[str] = [
            "# Tarefa",
            "",
            (
                f"Escreva os cartões dos {len(grupo.alvos)} nós abaixo, filhos de "
                f"**{grupo.pai.caminho_exibicao}** (ID {grupo.pai.tema_id})."
            ),
        ]
        if grupo.irmaos_fora:
            linhas.append(
                "Os demais filhos do mesmo pai estão no fim, só como contexto: não escreva cartões para eles, "
                "mas use-os em `nao_inclui` quando couber."
            )
        linhas.extend(["", "## Nós que recebem cartão", ""])
        alvo: TemaPreparado
        for alvo in grupo.alvos:
            marca: str = " [conceitual]" if alvo.lixeira == "forte" else ""
            linhas.append(f"### {alvo.tema_id} | {alvo.caminho_exibicao}{marca}")
            if alvo.tema_id in self._descricoes:
                linhas.append(f"- Descrição na árvore: {self._descricoes[alvo.tema_id]}")
            subtemas: list[TemaPreparado] = [
                self._temas[i] for i in alvo.filhos if i in self._temas and self._temas[i].publicavel
            ]
            if subtemas:
                linhas.append(
                    "- Subtemas (têm cartão próprio): "
                    + "; ".join(f"{sub.tema_id} {sub.titulo_exibicao}" for sub in subtemas)
                )
            if alvo.grupo_sobreposicao:
                linhas.append(
                    f"- Regra de sobreposição (decisão do autor, grupo {alvo.grupo_sobreposicao}): {alvo.regra_desempate}"
                )
            linhas.append("")
        if grupo.irmaos_fora:
            linhas.extend(["## Outros filhos do mesmo pai (só contexto)", ""])
            linhas.extend(f"- {irmao.tema_id} | {irmao.titulo_exibicao}" for irmao in grupo.irmaos_fora)
        return "\n".join(linhas).strip() + "\n"

    def _schema(self, grupo: GrupoCartoes) -> dict[str, object]:
        """Monta o JSON Schema da resposta, com ``enum`` dos IDs.

        Args:
            grupo: Grupo.

        Returns:
            Schema.
        """
        texto: dict[str, object] = {"type": "string"}
        lista: dict[str, object] = {"type": "array", "items": texto}
        item: dict[str, object] = {
            "type": "object",
            "properties": {"assunto": texto, "tema_id": {"type": "string", "enum": self._publicaveis}},
            "required": ["assunto", "tema_id"],
            "additionalProperties": False,
        }
        cartao: dict[str, object] = {
            "type": "object",
            "properties": {
                "tema_id": {"type": "string", "enum": [alvo.tema_id for alvo in grupo.alvos]},
                "escopo": texto,
                "inclui": lista,
                "nao_inclui": {"type": "array", "items": item},
                "ancoras_legais": lista,
                "regra_desempate": texto,
            },
            "required": ["tema_id", "escopo", "inclui", "nao_inclui", "ancoras_legais", "regra_desempate"],
            "additionalProperties": False,
        }
        return {
            "type": "object",
            "properties": {"cartoes": {"type": "array", "items": cartao}},
            "required": ["cartoes"],
            "additionalProperties": False,
        }

    def _converter(
        self, grupo: GrupoCartoes, dados: Mapping[str, object], resultado: ResultadoChamada
    ) -> list[CartaoTema]:
        """Converte a resposta em cartões, conferindo que veio um cartão para cada nó.

        Itens de ``nao_inclui`` que apontam para nó não publicável ou para o próprio nó são descartados.

        Args:
            grupo: Grupo pedido.
            dados: Resposta estruturada.
            resultado: Chamada (para registrar o modelo).

        Returns:
            Cartões do grupo.

        Raises:
            ErroGeracaoCartoes: Se faltar cartão, sobrar ou vier malformado.
        """
        brutos: object = dados.get("cartoes")
        if not isinstance(brutos, list):
            raise ErroGeracaoCartoes("resposta sem a lista 'cartoes'")
        por_id: dict[str, dict[str, object]] = {}
        bruto: object
        for bruto in brutos:
            if isinstance(bruto, dict) and isinstance(bruto.get("tema_id"), str):
                por_id[str(bruto["tema_id"])] = {str(k): v for k, v in bruto.items()}
        esperados: set[str] = {alvo.tema_id for alvo in grupo.alvos}
        if set(por_id) != esperados:
            raise ErroGeracaoCartoes(
                f"faltaram {sorted(esperados - set(por_id))}, sobraram {sorted(set(por_id) - esperados)}"
            )
        modelo: str = f"{resultado.resposta.provedor}:{resultado.resposta.modelo}"
        cartoes: list[CartaoTema] = []
        alvo: TemaPreparado
        for alvo in grupo.alvos:
            objeto: dict[str, object] = por_id[alvo.tema_id]
            regra: str = self._texto(objeto.get("regra_desempate")).strip()
            cartoes.append(
                CartaoTema(
                    tema_id=alvo.tema_id,
                    caminho=alvo.caminho_exibicao,
                    titulo_exibicao=alvo.titulo_exibicao,
                    escopo=self._texto(objeto.get("escopo")).strip(),
                    inclui=self._textos(objeto.get("inclui")),
                    nao_inclui=self._nao_inclui(objeto.get("nao_inclui"), alvo.tema_id),
                    ancoras_legais=self._textos(objeto.get("ancoras_legais")),
                    regra_desempate=regra if regra else alvo.regra_desempate,
                    origem="gerado",
                    modelo=modelo,
                )
            )
        return cartoes

    def _nao_inclui(self, valor: object, tema_id: str) -> tuple[ItemNaoInclui, ...]:
        """Converte e filtra os itens de ``nao_inclui``.

        Args:
            valor: Lista bruta.
            tema_id: Nó do cartão.

        Returns:
            Itens válidos.
        """
        itens: list[ItemNaoInclui] = []
        bruto: object
        for bruto in valor if isinstance(valor, list) else []:
            if not isinstance(bruto, dict):
                continue
            destino: str = self._texto(bruto.get("tema_id")).strip()
            assunto: str = self._texto(bruto.get("assunto")).strip()
            if assunto and destino != tema_id and destino in self._temas and self._temas[destino].publicavel:
                itens.append(ItemNaoInclui(assunto, destino))
        return tuple(itens)

    @staticmethod
    def _texto(valor: object) -> str:
        """Converte um valor em texto.

        Args:
            valor: Valor bruto.

        Returns:
            O texto, ou ``""`` se não for texto.
        """
        return valor if isinstance(valor, str) else ""

    @staticmethod
    def _textos(valor: object) -> tuple[str, ...]:
        """Converte uma lista bruta em textos não vazios.

        Args:
            valor: Valor bruto.

        Returns:
            Textos.
        """
        return (
            tuple(item.strip() for item in valor if isinstance(item, str) and item.strip())
            if isinstance(valor, list)
            else ()
        )
