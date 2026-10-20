"""Revisão humana das propostas de conhecimento (ADR-020) e montagem dos artefatos finais.

A fila segue a prioridade da ADR-020:

1. todas as linhas do mapa lei/artigo → tema (as regras de maior peso);
2. os termos ``forte`` e ``exclui`` das zonas de risco (lixeiras e sobreposições) e
   os termos fortes propostos para mais de um tema;
3. uma amostra aleatória (semente fixa) do restante dos termos, para estimar a taxa de erro do que não
   foi revisado.

Cada decisão (aceitar, corrigir, apagar) é gravada em ``dados/conhecimento/revisao.csv`` assim que é
tomada; a revisão pode ser interrompida e retomada. Ao sair, os artefatos finais
(``dados/conhecimento/mapa_artigos.csv`` e ``termos.csv``) são remontados a partir das propostas e das
decisões, e o manifesto registra quanto foi revisado.
"""

from __future__ import annotations

import csv
import random
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import ClassVar, TextIO

from vicio_ia.configuracao import Caminhos
from vicio_ia.enriquecimento.manifesto import Manifesto
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.temas.cartoes import ArquivoCartoes, CartaoTema
from vicio_ia.texto import ProcessadorTexto


class _Sair(Exception):
    """Pedido de saída (``q``, Ctrl+C ou fim da entrada)."""


@dataclass(frozen=True)
class ItemRevisao:
    """Uma proposta na fila de revisão.

    Attributes:
        tipo: ``artigo`` ou ``termo``.
        chave: Identificação estável da proposta.
        tema_id: Tema da proposta.
        campos: Linha do CSV de propostas.
        prioridade: 1 (mapa), 2 (termos de risco) ou 3 (amostra).
    """

    tipo: str
    chave: str
    tema_id: str
    campos: dict[str, str]
    prioridade: int


@dataclass(frozen=True)
class DecisaoRevisao:
    """Decisão do revisor sobre uma proposta.

    Attributes:
        chave: Chave da proposta.
        tipo: ``artigo`` ou ``termo``.
        decisao: ``aceitar``, ``corrigir`` ou ``apagar``.
        correcao: Campos corrigidos, separados por ``|`` (artigo: lei, início, fim, tema; termo: termo, tema,
            tipo, alvo).
        revisado_em: Data e hora.
    """

    chave: str
    tipo: str
    decisao: str
    correcao: str
    revisado_em: str


class ArquivoRevisao:
    """Decisões de revisão, gravadas uma a uma (só acréscimo)."""

    COLUNAS: ClassVar[tuple[str, ...]] = ("chave", "tipo", "decisao", "correcao", "revisado_em")

    def __init__(self, caminho: Path) -> None:
        """Define o arquivo.

        Args:
            caminho: ``dados/conhecimento/revisao.csv``.
        """
        self._caminho: Path = caminho

    def ler(self) -> dict[str, DecisaoRevisao]:
        """Lê as decisões; a última decisão de cada chave vale.

        Returns:
            Decisões por chave.
        """
        if not self._caminho.is_file():
            return {}
        decisoes: dict[str, DecisaoRevisao] = {}
        arquivo: TextIO
        with self._caminho.open(encoding="utf-8", newline="") as arquivo:
            linha: dict[str, str]
            for linha in csv.DictReader(arquivo):
                decisoes[linha["chave"]] = DecisaoRevisao(
                    linha["chave"], linha["tipo"], linha["decisao"], linha.get("correcao", ""), linha["revisado_em"]
                )
        return decisoes

    def acrescentar(self, decisao: DecisaoRevisao) -> None:
        """Grava uma decisão no fim do arquivo.

        Args:
            decisao: Decisão.
        """
        novo: bool = not self._caminho.is_file()
        self._caminho.parent.mkdir(parents=True, exist_ok=True)
        arquivo: TextIO
        with self._caminho.open("a", encoding="utf-8", newline="") as arquivo:
            escritor: csv.DictWriter[str] = csv.DictWriter(arquivo, fieldnames=list(self.COLUNAS))
            if novo:
                escritor.writeheader()
            escritor.writerow(
                {
                    "chave": decisao.chave,
                    "tipo": decisao.tipo,
                    "decisao": decisao.decisao,
                    "correcao": decisao.correcao,
                    "revisado_em": decisao.revisado_em,
                }
            )


class FilaRevisao:
    """Monta a fila de revisão a partir das propostas, na ordem de prioridade da ADR-020."""

    FRACAO_AMOSTRA: ClassVar[float] = 0.10
    SEMENTE: ClassVar[int] = 20261021

    def __init__(self, temas: Sequence[TemaPreparado]) -> None:
        """Guarda a árvore.

        Args:
            temas: Árvore preparada.
        """
        self._temas: dict[str, TemaPreparado] = {t.tema_id: t for t in temas}

    @staticmethod
    def chave_artigo(linha: Mapping[str, str]) -> str:
        """Chave estável de uma linha do mapa.

        Args:
            linha: Linha do CSV.

        Returns:
            Chave.
        """
        return f"artigo|{linha['lei']}|{linha['art_inicio']}|{linha['art_fim']}|{linha['tema_id']}"

    @staticmethod
    def chave_termo(linha: Mapping[str, str]) -> str:
        """Chave estável de uma linha de termos.

        Args:
            linha: Linha do CSV.

        Returns:
            Chave.
        """
        return f"termo|{linha['termo_normalizado']}|{linha['tema_id']}|{linha['tipo']}"

    def _risco(self, tema_id: str) -> bool:
        """Tema em zona de risco para o sentido dos termos: lixeira ou sobreposição (ADR-020).

        A zona de convenção dos duplicados fica de fora: o risco dela é a escolha do nó, não o termo.

        Args:
            tema_id: Tema.

        Returns:
            ``True`` se o tema estiver numa zona de risco.
        """
        tema: TemaPreparado | None = self._temas.get(tema_id)
        return tema is not None and bool(tema.lixeira or tema.grupo_sobreposicao)

    def montar(self, artigos: Sequence[Mapping[str, str]], termos: Sequence[Mapping[str, str]]) -> list[ItemRevisao]:
        """Monta a fila completa.

        Args:
            artigos: Linhas do mapa proposto.
            termos: Linhas dos termos propostos.

        Returns:
            Itens em ordem de prioridade.
        """
        fila: list[ItemRevisao] = [
            ItemRevisao("artigo", self.chave_artigo(a), a["tema_id"], dict(a), 1) for a in artigos
        ]
        fortes: Counter[str] = Counter(t["termo_normalizado"] for t in termos if t["tipo"] == "forte")
        prioritarios: list[ItemRevisao] = []
        restantes: list[ItemRevisao] = []
        termo: Mapping[str, str]
        for termo in termos:
            conflito: bool = termo["tipo"] == "forte" and fortes[termo["termo_normalizado"]] > 1
            risco: bool = termo["tipo"] in {"forte", "exclui"} and self._risco(termo["tema_id"])
            item: ItemRevisao = ItemRevisao("termo", self.chave_termo(termo), termo["tema_id"], dict(termo), 2)
            if conflito or risco:
                prioritarios.append(item)
            else:
                restantes.append(item)
        tamanho: int = max(1, round(len(restantes) * self.FRACAO_AMOSTRA)) if restantes else 0
        amostra: list[ItemRevisao] = random.Random(self.SEMENTE).sample(restantes, tamanho)
        fila.extend(prioritarios)
        fila.extend(ItemRevisao(i.tipo, i.chave, i.tema_id, i.campos, 3) for i in amostra)
        return fila


class MontadorConhecimento:
    """Aplica as decisões às propostas e grava os artefatos finais com o estado de revisão."""

    def __init__(self, caminhos: Caminhos) -> None:
        """Guarda os caminhos.

        Args:
            caminhos: Caminhos do projeto.
        """
        self._caminhos: Caminhos = caminhos

    @staticmethod
    def ler_csv(caminho: Path) -> list[dict[str, str]]:
        """Lê um CSV.

        Args:
            caminho: Arquivo.

        Returns:
            Linhas (vazio se o arquivo não existir).
        """
        if not caminho.is_file():
            return []
        arquivo: TextIO
        with caminho.open(encoding="utf-8", newline="") as arquivo:
            return list(csv.DictReader(arquivo))

    def montar(self, decisoes: Mapping[str, DecisaoRevisao], fila: Sequence[ItemRevisao]) -> dict[str, str]:
        """Grava ``mapa_artigos.csv`` e ``termos.csv`` finais e registra o manifesto.

        Args:
            decisoes: Decisões por chave.
            fila: Fila de revisão (para separar a amostra na taxa de erro).

        Returns:
            Resumo da revisão (para o manifesto e o relatório).
        """
        pasta: Path = self._caminhos.dados_conhecimento
        artigos: list[dict[str, str]] = self.ler_csv(pasta / "propostas" / "mapa_artigos.csv")
        termos: list[dict[str, str]] = self.ler_csv(pasta / "propostas" / "termos.csv")
        artigos_finais: list[list[str]] = [["lei", "art_inicio", "art_fim", "tema_id", "forca", "revisado", "origem"]]
        linha: dict[str, str]
        for linha in artigos:
            decisao: DecisaoRevisao | None = decisoes.get(FilaRevisao.chave_artigo(linha))
            if decisao is not None and decisao.decisao == "apagar":
                continue
            campos: list[str] = [linha["lei"], linha["art_inicio"], linha["art_fim"], linha["tema_id"]]
            if decisao is not None and decisao.decisao == "corrigir":
                campos = decisao.correcao.split("|")
            artigos_finais.append([*campos, linha["forca"], "sim" if decisao else "nao", linha["origem"]])
        termos_finais: list[list[str]] = [
            ["termo", "termo_normalizado", "tema_id", "tipo", "tema_id_alvo", "revisado", "origem"]
        ]
        processador: ProcessadorTexto = ProcessadorTexto()
        for linha in termos:
            decisao_t: DecisaoRevisao | None = decisoes.get(FilaRevisao.chave_termo(linha))
            if decisao_t is not None and decisao_t.decisao == "apagar":
                continue
            termo: str = linha["termo"]
            tema: str = linha["tema_id"]
            tipo: str = linha["tipo"]
            alvo: str = linha["tema_id_alvo"]
            if decisao_t is not None and decisao_t.decisao == "corrigir":
                termo, tema, tipo, alvo = decisao_t.correcao.split("|")
            termos_finais.append(
                [termo, processador.normalizar(termo), tema, tipo, alvo, "sim" if decisao_t else "nao", linha["origem"]]
            )
        destino_artigos: Path = pasta / "mapa_artigos.csv"
        destino_termos: Path = pasta / "termos.csv"
        arquivo: TextIO
        with destino_artigos.open("w", encoding="utf-8", newline="") as arquivo:
            csv.writer(arquivo).writerows(artigos_finais)
        with destino_termos.open("w", encoding="utf-8", newline="") as arquivo:
            csv.writer(arquivo).writerows(termos_finais)
        resumo: dict[str, str] = self._resumo(decisoes, fila, len(artigos), len(termos))
        manifesto: Manifesto = Manifesto(pasta / "manifesto.json", self._caminhos.raiz)
        origem: str = "llm+revisão" if decisoes else "llm (proposta, sem revisão)"
        destino: Path
        for destino in (destino_artigos, destino_termos):
            manifesto.registrar(destino, origem, "uv run python executar_revisao_conhecimento.py", resumo)
        return resumo

    @staticmethod
    def _resumo(
        decisoes: Mapping[str, DecisaoRevisao], fila: Sequence[ItemRevisao], total_artigos: int, total_termos: int
    ) -> dict[str, str]:
        """Contagens da revisão, inclusive a taxa de erro na amostra aleatória.

        Args:
            decisoes: Decisões por chave.
            fila: Fila de revisão.
            total_artigos: Propostas de artigo.
            total_termos: Propostas de termo.

        Returns:
            Resumo em texto.
        """
        contagem: Counter[str] = Counter(f"{d.tipo}:{d.decisao}" for d in decisoes.values())
        amostra: list[str] = [i.chave for i in fila if i.prioridade == 3]
        revisadas: list[DecisaoRevisao] = [decisoes[c] for c in amostra if c in decisoes]
        erradas: int = sum(1 for d in revisadas if d.decisao != "aceitar")
        return {
            "artigos_propostos": str(total_artigos),
            "termos_propostos": str(total_termos),
            "decisoes": "; ".join(f"{k} {v}" for k, v in sorted(contagem.items())) or "nenhuma",
            "amostra_revisada": f"{len(revisadas)}/{len(amostra)}",
            "taxa_erro_amostra": f"{erradas}/{len(revisadas)}" if revisadas else "não medida",
            "revisor": "autor do case",
            "revisado_ate": max((d.revisado_em for d in decisoes.values()), default=""),
        }


class RevisorInterativo:
    """Revisão no terminal: mostra cada proposta com o contexto do tema e grava a decisão."""

    def __init__(self, caminhos: Caminhos | None = None) -> None:
        """Carrega a árvore, os cartões e as propostas.

        Args:
            caminhos: Caminhos do projeto.
        """
        self._caminhos: Caminhos = caminhos or Caminhos.padrao()
        leitor: LeitorPreparados = LeitorPreparados(self._caminhos)
        self._temas: dict[str, TemaPreparado] = {t.tema_id: t for t in leitor.temas()}
        self._cartoes: dict[str, CartaoTema] = {
            c.tema_id: c for c in ArquivoCartoes(self._caminhos.dados_temas / "cartoes.jsonl").ler()
        }
        self._arquivo: ArquivoRevisao = ArquivoRevisao(self._caminhos.dados_conhecimento / "revisao.csv")
        pasta: Path = self._caminhos.dados_conhecimento / "propostas"
        self._fila: list[ItemRevisao] = FilaRevisao(list(self._temas.values())).montar(
            MontadorConhecimento.ler_csv(pasta / "mapa_artigos.csv"),
            MontadorConhecimento.ler_csv(pasta / "termos.csv"),
        )

    def executar(self) -> None:
        """Revisa as propostas pendentes, na ordem da fila, e remonta os artefatos ao sair."""
        decisoes: dict[str, DecisaoRevisao] = self._arquivo.ler()
        pendentes: list[ItemRevisao] = [i for i in self._fila if i.chave not in decisoes]
        print(
            f"Revisão do conhecimento: {len(self._fila)} itens na fila, {len(pendentes)} pendentes.\n"
            "Enter ou a = aceitar · c = corrigir · x = apagar · p = pular · q = sair"
        )
        inicio: datetime = datetime.now()
        feitas: int = 0
        try:
            item: ItemRevisao
            for item in pendentes:
                decisao: DecisaoRevisao | None = self._revisar(item, len(self._fila) - len(pendentes) + feitas + 1)
                if decisao is not None:
                    self._arquivo.acrescentar(decisao)
                    feitas += 1
        except _Sair:
            print("\nRevisão interrompida; as decisões tomadas estão gravadas.")
        minutos: float = (datetime.now() - inicio).total_seconds() / 60
        resumo: dict[str, str] = MontadorConhecimento(self._caminhos).montar(self._arquivo.ler(), self._fila)
        print(f"{feitas} decisões nesta sessão ({minutos:.0f} min). Resumo: {resumo['decisoes']}.")
        print(f"Amostra: {resumo['amostra_revisada']} revisados; erro na amostra: {resumo['taxa_erro_amostra']}.")

    def _revisar(self, item: ItemRevisao, posicao: int) -> DecisaoRevisao | None:
        """Mostra um item e lê a decisão.

        Args:
            item: Item da fila.
            posicao: Posição na fila (1 em diante).

        Returns:
            Decisão, ou ``None`` se o item foi pulado.
        """
        nomes: dict[int, str] = {1: "mapa de artigos", 2: "termo de risco", 3: "amostra"}
        print(f"\n[{posicao}/{len(self._fila)}] {nomes[item.prioridade]}")
        self._mostrar(item)
        while True:
            entrada: str = self._perguntar("Decisão [a/c/x/p/q]: ").strip().lower()
            agora: str = datetime.now().isoformat(timespec="seconds")
            if entrada in {"", "a"}:
                return DecisaoRevisao(item.chave, item.tipo, "aceitar", "", agora)
            if entrada == "x":
                return DecisaoRevisao(item.chave, item.tipo, "apagar", "", agora)
            if entrada == "p":
                return None
            if entrada == "c":
                correcao: str | None = self._corrigir(item)
                if correcao is not None:
                    return DecisaoRevisao(item.chave, item.tipo, "corrigir", correcao, agora)
                continue
            print("Use a, c, x, p ou q.")

    def _mostrar(self, item: ItemRevisao) -> None:
        """Mostra a proposta e o contexto do tema.

        Args:
            item: Item da fila.
        """
        c: dict[str, str] = item.campos
        tema: TemaPreparado | None = self._temas.get(item.tema_id)
        caminho: str = tema.caminho_exibicao if tema else item.tema_id
        if item.tipo == "artigo":
            artigos: str = (
                f"art. {c['art_inicio']}"
                if c["art_inicio"] == c["art_fim"]
                else f"arts. {c['art_inicio']} a {c['art_fim']}"
            )
            print(f"  {c['lei']}, {artigos}  →  {item.tema_id} {caminho}  ({c['forca']})")
        else:
            alvo: str = ""
            if c["tipo"] == "exclui":
                destino: TemaPreparado | None = self._temas.get(c["tema_id_alvo"])
                alvo = f"  →  vai para {c['tema_id_alvo']} {destino.caminho_exibicao if destino else '?'}"
            print(f'  "{c["termo"]}" [{c["tipo"]}] em {item.tema_id} {caminho}{alvo}')
        cartao: CartaoTema | None = self._cartoes.get(item.tema_id)
        if cartao is not None:
            print(f"  Escopo: {cartao.escopo}")
        if tema is not None and tema.parent_id in self._temas:
            irmaos: list[str] = [
                self._temas[i].titulo_exibicao
                for i in self._temas[tema.parent_id].filhos
                if i in self._temas and i != tema.tema_id and self._temas[i].publicavel
            ]
            if irmaos:
                print("  Irmãos: " + "; ".join(irmaos[:12]))

    def _corrigir(self, item: ItemRevisao) -> str | None:
        """Lê os campos corrigidos (Enter mantém o valor atual).

        Args:
            item: Item da fila.

        Returns:
            Campos corrigidos separados por ``|``, ou ``None`` se algum valor for inválido.
        """
        c: dict[str, str] = item.campos
        if item.tipo == "artigo":
            lei: str = self._perguntar(f"  lei [{c['lei']}]: ").strip() or c["lei"]
            inicio: str = self._perguntar(f"  art. inicial [{c['art_inicio']}]: ").strip() or c["art_inicio"]
            fim: str = self._perguntar(f"  art. final [{c['art_fim']}]: ").strip() or c["art_fim"]
            tema: str = self._perguntar(f"  tema [{c['tema_id']}]: ").strip() or c["tema_id"]
            if not (inicio.isdigit() and fim.isdigit() and int(inicio) <= int(fim)) or tema not in self._temas:
                print("  Valores inválidos; nada foi gravado.")
                return None
            return f"{lei}|{inicio}|{fim}|{tema}"
        termo: str = self._perguntar(f"  termo [{c['termo']}]: ").strip() or c["termo"]
        tema_t: str = self._perguntar(f"  tema [{c['tema_id']}]: ").strip() or c["tema_id"]
        tipo: str = self._perguntar(f"  tipo forte/fraco/exclui [{c['tipo']}]: ").strip() or c["tipo"]
        alvo: str = c["tema_id_alvo"]
        if tipo == "exclui":
            alvo = self._perguntar(f"  vai para o tema [{alvo}]: ").strip() or alvo
        else:
            alvo = ""
        if (
            tipo not in {"forte", "fraco", "exclui"}
            or tema_t not in self._temas
            or (tipo == "exclui" and alvo not in self._temas)
        ):
            print("  Valores inválidos; nada foi gravado.")
            return None
        return f"{termo}|{tema_t}|{tipo}|{alvo}"

    @staticmethod
    def _perguntar(texto: str) -> str:
        """Lê uma linha do terminal.

        Args:
            texto: Prompt exibido.

        Returns:
            O que foi digitado.

        Raises:
            _Sair: Em Ctrl+C, fim da entrada ou ``q``.
        """
        try:
            resposta: str = input(texto)
        except (EOFError, KeyboardInterrupt) as erro:
            raise _Sair from erro
        if resposta.strip().lower() == "q":
            raise _Sair
        return resposta
