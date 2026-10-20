"""Propostas de mapa lei/artigo → tema e de dicionário de termos, por LLM, para revisão (ADR-020).

Uma chamada por tema pai (os filhos publicáveis de cada disciplina ou tema), como nos cartões da etapa 1.
O prompt só traz o tema (título, caminho, cartão e vizinhos); **nenhuma questão** entra na chamada, e o
schema da resposta não tem campo de questão (ADR-019). O resultado é uma proposta: só vira dado do
sistema depois da revisão do autor.
"""

from __future__ import annotations

import math
import re
from collections.abc import Mapping, Sequence
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import ClassVar

from vicio_ia.configuracao import ParametrosConhecimento
from vicio_ia.llm.cliente import ClienteLLM, ResultadoChamada
from vicio_ia.llm.contratos import ErroProvedor, RequisicaoLLM
from vicio_ia.llm.prompts import ArquivoPrompt
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.temas.cartoes import CartaoTema
from vicio_ia.texto import ProcessadorTexto


class ErroPropostas(Exception):
    """O modelo não devolveu as propostas pedidas, mesmo depois de repetir a chamada."""


@dataclass(frozen=True)
class ReferenciaProposta:
    """Intervalo de artigos de uma lei proposto para um tema.

    Attributes:
        lei: Lei normalizada (``CP``, ``CPP``, ``LEP``, ``CF`` ou ``Lei 11.343/2006``).
        art_inicio: Primeiro artigo.
        art_fim: Último artigo.
        tema_id: Tema.
        forca: ``ramo`` para tema com subtemas (o intervalo cobre o conjunto); ``exata`` nos demais.
    """

    lei: str
    art_inicio: int
    art_fim: int
    tema_id: str
    forca: str


@dataclass(frozen=True)
class TermoProposto:
    """Expressão característica proposta para um tema.

    Attributes:
        termo: Expressão como o modelo escreveu.
        normalizado: Forma de comparação (minúsculas, sem acento).
        tema_id: Tema.
        tipo: ``forte``, ``fraco`` ou ``exclui``.
        tema_id_alvo: Nó indicado por um termo ``exclui``; vazio nos demais.
    """

    termo: str
    normalizado: str
    tema_id: str
    tipo: str
    tema_id_alvo: str


@dataclass(frozen=True)
class GrupoTemas:
    """Filhos publicáveis de um mesmo pai, pedidos numa chamada.

    Attributes:
        rotulo: Identificação no cache (``filhos:5063`` ou ``filhos:5062:2``).
        pai: Disciplina ou tema pai.
        alvos: Temas que recebem propostas nesta chamada.
        irmaos_fora: Outros filhos do mesmo pai, em outro bloco.
    """

    rotulo: str
    pai: TemaPreparado
    alvos: tuple[TemaPreparado, ...]
    irmaos_fora: tuple[TemaPreparado, ...]


@dataclass(frozen=True)
class PropostasGrupo:
    """Resultado de um grupo.

    Attributes:
        referencias: Referências aceitas.
        termos: Termos aceitos.
        avisos: Itens descartados e por quê.
        do_cache: Todas as respostas vieram do cache.
    """

    referencias: tuple[ReferenciaProposta, ...]
    termos: tuple[TermoProposto, ...]
    avisos: tuple[str, ...]
    do_cache: bool


class NormalizadorLei:
    """Converte a forma livre de uma lei na forma canônica do mapa de artigos."""

    CODIGOS: ClassVar[dict[str, str]] = {
        "cp": "CP",
        "codigo penal": "CP",
        "cpp": "CPP",
        "codigo de processo penal": "CPP",
        "lep": "LEP",
        "lei de execucao penal": "LEP",
        "cf": "CF",
        "cf 88": "CF",
        "cf 1988": "CF",
        "crfb": "CF",
        "constituicao federal": "CF",
    }
    NUMEROS: ClassVar[dict[str, str]] = {"2848": "CP", "3689": "CPP", "7210": "LEP"}
    _RE_LEI: ClassVar[re.Pattern[str]] = re.compile(r"(\d{1,2}\.?\d{3})\s*/\s*(\d{4}|\d{2})\b")

    def __init__(self, processador: ProcessadorTexto) -> None:
        """Guarda o normalizador de texto.

        Args:
            processador: Normalizador de texto.
        """
        self._processador: ProcessadorTexto = processador

    def normalizar(self, bruto: str) -> str | None:
        """Forma canônica da lei.

        Args:
            bruto: Lei como o modelo escreveu (``CP``, ``Lei 11.343/2006``, ``Lei nº 9.099/95``...).

        Returns:
            ``CP``, ``CPP``, ``LEP``, ``CF`` ou ``Lei 11.343/2006``; ``None`` se não reconhecer.
        """
        chave: str = self._processador.normalizar(bruto)
        if chave in self.CODIGOS:
            return self.CODIGOS[chave]
        achado: re.Match[str] | None = self._RE_LEI.search(bruto)
        if achado is None:
            return None
        numero: str = achado.group(1).replace(".", "")
        if numero in self.NUMEROS:
            return self.NUMEROS[numero]
        ano: str = achado.group(2)
        if len(ano) == 2:
            ano = ("19" if int(ano) > 30 else "20") + ano
        return f"Lei {int(numero):,}/{ano}".replace(",", ".")


class GeradorPropostas:
    """Pede ao modelo o mapa de artigos e os termos de cada grupo, em paralelo, com cache (ADR-003)."""

    TIPOS: ClassVar[tuple[str, ...]] = ("forte", "fraco", "exclui")
    SEM_ALVO: ClassVar[str] = "nenhum"

    def __init__(
        self,
        cliente: ClienteLLM,
        prompt: ArquivoPrompt,
        temas: Sequence[TemaPreparado],
        arvore_enxuta: str,
        cartoes: Sequence[CartaoTema],
        parametros: ParametrosConhecimento,
        paralelismo: int,
    ) -> None:
        """Guarda as dependências.

        Args:
            cliente: Cliente do papel ``conhecimento``.
            prompt: ``prompts/conhecimento_tema.md``.
            temas: Árvore preparada.
            arvore_enxuta: Árvore enxuta (vai no prompt de sistema).
            cartoes: Cartões da etapa 1 (escopo e âncoras como ponto de partida).
            parametros: Parâmetros da fase de conhecimento.
            paralelismo: Chamadas simultâneas.
        """
        self._cliente: ClienteLLM = cliente
        self._prompt: ArquivoPrompt = prompt
        self._temas: dict[str, TemaPreparado] = {tema.tema_id: tema for tema in temas}
        self._publicaveis: list[str] = sorted(tema.tema_id for tema in temas if tema.publicavel)
        self._sistema: str = prompt.preencher({"arvore": arvore_enxuta.strip()})
        self._cartoes: dict[str, CartaoTema] = {cartao.tema_id: cartao for cartao in cartoes}
        self._parametros: ParametrosConhecimento = parametros
        self._paralelismo: int = paralelismo
        self._processador: ProcessadorTexto = ProcessadorTexto()
        self._leis: NormalizadorLei = NormalizadorLei(self._processador)

    def grupos(self) -> list[GrupoTemas]:
        """Monta os grupos: temas de nível 1 por disciplina e subtemas por tema pai.

        Returns:
            Grupos na ordem da árvore.
        """
        grupos: list[GrupoTemas] = []
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
            blocos: int = math.ceil(len(filhos) / self._parametros.max_temas_por_chamada)
            tamanho: int = math.ceil(len(filhos) / blocos)
            indice: int
            for indice in range(blocos):
                alvos: tuple[TemaPreparado, ...] = tuple(filhos[indice * tamanho : (indice + 1) * tamanho])
                rotulo: str = f"filhos:{pai.tema_id}" if blocos == 1 else f"filhos:{pai.tema_id}:{indice + 1}"
                grupos.append(GrupoTemas(rotulo, pai, alvos, tuple(f for f in filhos if f not in alvos)))
        return grupos

    def gerar(self) -> list[PropostasGrupo]:
        """Gera as propostas de todos os grupos.

        Returns:
            Resultados dos grupos, na ordem da árvore.

        Raises:
            ErroPropostas: Se algum grupo falhar duas vezes ou se o provedor falhar.
        """
        grupos: list[GrupoTemas] = self.grupos()
        resultados: dict[str, PropostasGrupo] = {}
        falhas: list[str] = []
        executor: ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=self._paralelismo) as executor:
            futuros: dict[Future[PropostasGrupo], GrupoTemas] = {
                executor.submit(self._gerar_grupo, grupo): grupo for grupo in grupos
            }
            feito: Future[PropostasGrupo]
            posicao: int
            for posicao, feito in enumerate(as_completed(futuros), start=1):
                grupo: GrupoTemas = futuros[feito]
                try:
                    resultado: PropostasGrupo = feito.result()
                except (ErroProvedor, ErroPropostas) as erro:
                    falhas.append(f"{grupo.rotulo}: {erro}")
                    print(f"  [{posicao}/{len(grupos)}] {grupo.rotulo}: FALHOU ({erro})")
                    continue
                resultados[grupo.rotulo] = resultado
                origem: str = "cache" if resultado.do_cache else "modelo"
                print(
                    f"  [{posicao}/{len(grupos)}] {grupo.rotulo}: {len(resultado.referencias)} referências, "
                    f"{len(resultado.termos)} termos ({origem})"
                )
        if falhas:
            raise ErroPropostas("; ".join(falhas))
        return [resultados[grupo.rotulo] for grupo in grupos]

    def _gerar_grupo(self, grupo: GrupoTemas) -> PropostasGrupo:
        """Chama o modelo para um grupo, repetindo uma vez se a resposta vier incompleta.

        Args:
            grupo: Grupo.

        Returns:
            Propostas do grupo.

        Raises:
            ErroPropostas: Se a segunda tentativa também vier incompleta.
            ErroProvedor: Se a chamada falhar.
        """
        requisicao: RequisicaoLLM = RequisicaoLLM(
            sistema=self._sistema,
            usuario=self._tarefa(grupo),
            schema=self._schema(grupo),
            nome_schema="conhecimento_de_tema",
            max_tokens=self._parametros.max_tokens_saida,
        )
        ultimo_erro: str = ""
        tentativa: int
        for tentativa in (1, 2):
            resultado: ResultadoChamada = self._cliente.gerar(requisicao, self._prompt.versao, grupo.rotulo, tentativa)
            try:
                return self._converter(grupo, resultado.resposta.dados or {}, resultado.do_cache)
            except ErroPropostas as erro:
                ultimo_erro = str(erro)
        raise ErroPropostas(f"{grupo.rotulo}: {ultimo_erro}")

    def _tarefa(self, grupo: GrupoTemas) -> str:
        """Monta a mensagem da tarefa de um grupo (só temas; nenhuma questão).

        Args:
            grupo: Grupo.

        Returns:
            Texto da tarefa.
        """
        linhas: list[str] = [
            "# Tarefa",
            "",
            (
                f"Proponha `referencias` e `termos` para os {len(grupo.alvos)} nós abaixo, filhos de "
                f"**{grupo.pai.caminho_exibicao}** (ID {grupo.pai.tema_id})."
            ),
            "",
            "## Nós",
            "",
        ]
        alvo: TemaPreparado
        for alvo in grupo.alvos:
            marca: str = " [conceitual]" if alvo.lixeira == "forte" else ""
            linhas.append(f"### {alvo.tema_id} | {alvo.caminho_exibicao}{marca}")
            cartao: CartaoTema | None = self._cartoes.get(alvo.tema_id)
            if cartao is not None:
                linhas.append(f"- Escopo (rascunho): {cartao.escopo}")
                if cartao.inclui:
                    linhas.append("- Costuma incluir: " + "; ".join(cartao.inclui))
                if cartao.ancoras_legais:
                    linhas.append("- Âncoras do rascunho (confira antes de usar): " + "; ".join(cartao.ancoras_legais))
            subtemas: list[TemaPreparado] = [
                self._temas[i] for i in alvo.filhos if i in self._temas and self._temas[i].publicavel
            ]
            if subtemas:
                linhas.append(
                    "- Subtemas (recebem propostas próprias): "
                    + "; ".join(f"{sub.tema_id} {sub.titulo_exibicao}" for sub in subtemas)
                )
            if alvo.grupo_sobreposicao:
                linhas.append(f"- Regra de sobreposição (decisão do autor): {alvo.regra_desempate}")
            linhas.append("")
        if grupo.irmaos_fora:
            linhas.extend(["## Outros filhos do mesmo pai (só contexto)", ""])
            linhas.extend(f"- {irmao.tema_id} | {irmao.titulo_exibicao}" for irmao in grupo.irmaos_fora)
        return "\n".join(linhas).strip() + "\n"

    def _schema(self, grupo: GrupoTemas) -> dict[str, object]:
        """JSON Schema da resposta: IDs em ``enum``; nenhum campo de questão.

        Args:
            grupo: Grupo.

        Returns:
            Schema.
        """
        texto: dict[str, object] = {"type": "string"}
        inteiro: dict[str, object] = {"type": "integer"}
        referencia: dict[str, object] = {
            "type": "object",
            "properties": {"lei": texto, "art_inicio": inteiro, "art_fim": inteiro},
            "required": ["lei", "art_inicio", "art_fim"],
            "additionalProperties": False,
        }
        termo: dict[str, object] = {
            "type": "object",
            "properties": {
                "termo": texto,
                "tipo": {"type": "string", "enum": list(self.TIPOS)},
                "tema_id_alvo": {"type": "string", "enum": [self.SEM_ALVO, *self._publicaveis]},
            },
            "required": ["termo", "tipo", "tema_id_alvo"],
            "additionalProperties": False,
        }
        item: dict[str, object] = {
            "type": "object",
            "properties": {
                "tema_id": {"type": "string", "enum": [alvo.tema_id for alvo in grupo.alvos]},
                "referencias": {"type": "array", "items": referencia},
                "termos": {"type": "array", "items": termo},
            },
            "required": ["tema_id", "referencias", "termos"],
            "additionalProperties": False,
        }
        return {
            "type": "object",
            "properties": {"temas": {"type": "array", "items": item}},
            "required": ["temas"],
            "additionalProperties": False,
        }

    def _converter(self, grupo: GrupoTemas, dados: Mapping[str, object], do_cache: bool) -> PropostasGrupo:
        """Converte e confere a resposta; itens inválidos são descartados com aviso.

        Args:
            grupo: Grupo pedido.
            dados: Resposta estruturada.
            do_cache: A resposta veio do cache.

        Returns:
            Propostas do grupo.

        Raises:
            ErroPropostas: Se faltar algum nó do grupo na resposta.
        """
        itens: object = dados.get("temas")
        if not isinstance(itens, list):
            raise ErroPropostas("resposta sem a lista 'temas'")
        por_tema: dict[str, Mapping[str, object]] = {}
        item: object
        for item in itens:
            if isinstance(item, dict) and str(item.get("tema_id", "")) in {a.tema_id for a in grupo.alvos}:
                por_tema.setdefault(str(item["tema_id"]), {str(k): v for k, v in item.items()})
        faltantes: list[str] = [a.tema_id for a in grupo.alvos if a.tema_id not in por_tema]
        if faltantes:
            raise ErroPropostas(f"faltam os nós {', '.join(faltantes)}")
        referencias: list[ReferenciaProposta] = []
        termos: list[TermoProposto] = []
        avisos: list[str] = []
        alvo: TemaPreparado
        for alvo in grupo.alvos:
            bruto: Mapping[str, object] = por_tema[alvo.tema_id]
            forca: str = "ramo" if any(self._temas[i].publicavel for i in alvo.filhos if i in self._temas) else "exata"
            referencias.extend(self._referencias(alvo.tema_id, bruto.get("referencias"), forca, avisos))
            termos.extend(self._termos(alvo.tema_id, bruto.get("termos"), avisos))
        return PropostasGrupo(tuple(referencias), tuple(termos), tuple(avisos), do_cache)

    def _referencias(self, tema_id: str, valor: object, forca: str, avisos: list[str]) -> list[ReferenciaProposta]:
        """Converte as referências de um tema.

        Args:
            tema_id: Tema.
            valor: Lista bruta.
            forca: Força das referências do tema.
            avisos: Lista onde os descartes são registrados.

        Returns:
            Referências aceitas, sem repetição.
        """
        aceitas: list[ReferenciaProposta] = []
        if not isinstance(valor, list):
            return aceitas
        maximo: int = self._parametros.artigo_maximo
        item: object
        for item in valor:
            if not isinstance(item, dict):
                continue
            lei: str | None = self._leis.normalizar(str(item.get("lei", "")))
            inicio: object = item.get("art_inicio")
            fim: object = item.get("art_fim")
            if lei is None:
                avisos.append(f"{tema_id}: lei não reconhecida {item.get('lei')!r}")
            elif not (isinstance(inicio, int) and isinstance(fim, int) and 1 <= inicio <= fim <= maximo):
                avisos.append(f"{tema_id}: intervalo inválido {lei} {inicio}–{fim}")
            else:
                referencia: ReferenciaProposta = ReferenciaProposta(lei, inicio, fim, tema_id, forca)
                if referencia not in aceitas:
                    aceitas.append(referencia)
        return aceitas

    def _termos(self, tema_id: str, valor: object, avisos: list[str]) -> list[TermoProposto]:
        """Converte os termos de um tema.

        Args:
            tema_id: Tema.
            valor: Lista bruta.
            avisos: Lista onde os descartes são registrados.

        Returns:
            Termos aceitos, sem repetição (pela forma normalizada).
        """
        aceitos: list[TermoProposto] = []
        if not isinstance(valor, list):
            return aceitos
        vistos: set[str] = set()
        item: object
        for item in valor:
            if not isinstance(item, dict):
                continue
            termo: str = str(item.get("termo", "")).strip()
            normalizado: str = self._processador.normalizar(termo)
            tipo: str = str(item.get("tipo", ""))
            alvo: str = str(item.get("tema_id_alvo", self.SEM_ALVO))
            if not normalizado or len(termo) > self._parametros.max_chars_termo:
                avisos.append(f"{tema_id}: termo vazio ou longo demais {termo!r}")
            elif tipo not in self.TIPOS:
                avisos.append(f"{tema_id}: tipo inválido {tipo!r} em {termo!r}")
            elif tipo == "exclui" and (alvo == self.SEM_ALVO or alvo == tema_id or alvo not in self._publicaveis):
                avisos.append(f"{tema_id}: termo 'exclui' sem nó de destino válido: {termo!r} → {alvo}")
            elif normalizado not in vistos:
                vistos.add(normalizado)
                aceitos.append(TermoProposto(termo, normalizado, tema_id, tipo, alvo if tipo == "exclui" else ""))
        return aceitos
