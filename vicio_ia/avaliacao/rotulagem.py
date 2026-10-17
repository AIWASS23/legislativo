"""Rotulagem interativa do gold set no terminal (ADR-012).

Mostra só o texto canônico da questão (nunca saída de modelo nem rótulo de origem),
ajuda a achar o tema por busca no caminho da árvore e grava cada rótulo assim que ele
é confirmado. Pode ser interrompida e retomada: só as questões pendentes são mostradas.
"""

from __future__ import annotations

import sys
import time
from collections.abc import Sequence
from datetime import datetime
from typing import ClassVar

from vicio_ia.avaliacao.amostragem import ArquivoAmostra, ItemAmostra
from vicio_ia.avaliacao.planilha import PlanilhaRotulos, RotuloGold
from vicio_ia.configuracao import Caminhos, ParametrosGold
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada
from vicio_ia.texto import ProcessadorTexto


class _Sair(Exception):
    """Pedido de saída (``q``, Ctrl+C ou fim da entrada)."""


class _Pular(Exception):
    """Pedido para deixar a questão pendente e ir para a próxima."""


class BuscadorTemas:
    """Busca temas publicáveis por palavras (ou começos de palavra) no caminho de exibição."""

    def __init__(self, temas: Sequence[TemaPreparado], processador: ProcessadorTexto, limite: int) -> None:
        """Indexa os caminhos normalizados.

        Args:
            temas: Árvore preparada.
            processador: Normalizador de texto.
            limite: Máximo de resultados por busca.
        """
        self._processador: ProcessadorTexto = processador
        self._limite: int = limite
        self._indice: list[tuple[TemaPreparado, list[str], list[str]]] = [
            (tema, processador.tokens(tema.caminho_exibicao), processador.tokens(tema.titulo_exibicao))
            for tema in temas
            if tema.publicavel
        ]

    def buscar(self, consulta: str) -> list[TemaPreparado]:
        """Busca os temas em que toda palavra da consulta começa alguma palavra do caminho.

        Os que casam no próprio título vêm primeiro; depois, os mais rasos.

        Args:
            consulta: Palavras digitadas.

        Returns:
            Até ``limite`` temas.
        """
        termos: list[str] = self._processador.tokens(consulta)
        if not termos:
            return []
        achados: list[tuple[int, int, str, TemaPreparado]] = []
        entrada: tuple[TemaPreparado, list[str], list[str]]
        for entrada in self._indice:
            if all(any(palavra.startswith(termo) for palavra in entrada[1]) for termo in termos):
                no_titulo: int = sum(1 for termo in termos if any(p.startswith(termo) for p in entrada[2]))
                achados.append((-no_titulo, entrada[0].nivel, entrada[0].caminho_exibicao, entrada[0]))
        achados.sort(key=lambda achado: (achado[0], achado[1], achado[2]))
        return [achado[3] for achado in achados[: self._limite]]


class RotuladorInterativo:
    """Conduz a rotulagem do gold set no terminal, uma questão por vez."""

    AJUDA: ClassVar[str] = (
        "Digite um ID de tema, ou palavras para buscar na árvore (ex.: 'furto', 'acao penal privada').\n"
        "  ID de disciplina ou de tema com filhos: lista os filhos.\n"
        "  f = fora do recorte · p = pular (fica pendente) · q = sair · ? = esta ajuda"
    )
    CERTEZAS: ClassVar[dict[str, str]] = {"a": "alta", "m": "media", "b": "baixa"}

    def __init__(self, caminhos: Caminhos | None = None, parametros: ParametrosGold | None = None) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto (opcional).
            parametros: Parâmetros do gold set (opcional).
        """
        self._caminhos: Caminhos = caminhos if caminhos is not None else Caminhos.padrao()
        self._parametros: ParametrosGold = parametros if parametros is not None else ParametrosGold()
        self._temas: dict[str, TemaPreparado] = {}
        self._buscador: BuscadorTemas | None = None

    def executar(self) -> None:
        """Rotula as questões pendentes do gold set, gravando cada uma ao confirmar."""
        if not sys.stdin.isatty():
            print("A rotulagem é interativa: rode `uv run python executar_rotulagem.py` num terminal.")
            return
        leitor: LeitorPreparados = LeitorPreparados(self._caminhos)
        questoes: dict[str, QuestaoPreparada] = {questao.id: questao for questao in leitor.questoes()}
        temas: list[TemaPreparado] = leitor.temas()
        self._temas = {tema.tema_id: tema for tema in temas}
        self._buscador = BuscadorTemas(temas, ProcessadorTexto(), self._parametros.max_resultados_busca)
        arquivo: ArquivoAmostra = ArquivoAmostra(self._caminhos.dados_gold / "amostra_leva1.csv")
        if not arquivo.existe():
            print("Amostra do gold não encontrada: rode antes `uv run python executar_gold.py`.")
            return
        amostra: list[ItemAmostra] = arquivo.ler()
        planilha: PlanilhaRotulos = PlanilhaRotulos(
            self._caminhos.dados_gold / "rotulos_leva1.csv", self._parametros, temas
        )
        planilha.garantir(amostra)
        feitos: set[str] = {rotulo.id for rotulo in planilha.ler() if rotulo.preenchido}
        pendentes: list[ItemAmostra] = [item for item in amostra if item.id not in feitos]
        if not pendentes:
            print(f"Gold set: todas as {len(amostra)} questões já estão rotuladas.")
            return
        print(f"Gold set: {len(feitos)}/{len(amostra)} rotuladas; {len(pendentes)} pendentes.\n{self.AJUDA}")
        gravadas: int = 0
        item: ItemAmostra
        try:
            for item in pendentes:
                try:
                    rotulo: RotuloGold = self._rotular(item, len(amostra), questoes[item.id])
                except _Pular:
                    print("Pulada (continua pendente).")
                    continue
                planilha.registrar(rotulo)
                gravadas += 1
                print(f"Gravado em {planilha.caminho.name}.")
        except _Sair:
            print("\nSaindo; o que foi confirmado já está gravado.")
        total: int = len(feitos) + gravadas
        print(f"Gold set: {total}/{len(amostra)} rotuladas ({gravadas} nesta sessão).")

    def _rotular(self, item: ItemAmostra, total: int, questao: QuestaoPreparada) -> RotuloGold:
        """Mostra a questão e coleta o rótulo.

        Args:
            item: Item da amostra.
            total: Tamanho do gold set.
            questao: Questão preparada.

        Returns:
            Rótulo completo.
        """
        print("\n" + "=" * 100)
        print(f"Questão {item.ordem}/{total} · {item.id}")
        print("=" * 100)
        print(questao.texto_canonico)
        print("-" * 100)
        inicio: float = time.monotonic()
        tema_id: str = self._escolher_tema()
        fora: bool = tema_id == ""
        alternativos: list[str] = [] if fora else self._escolher_alternativos(tema_id)
        multitema: bool = False if fora else self._sim_nao("Multitema (cobre mais de um tema por igual)? [s/N] ")
        certeza: str = self._certeza()
        observacao: str = self._perguntar("Observação (Enter = nenhuma): ").strip()
        minutos: float = (time.monotonic() - inicio) / 60
        return RotuloGold(
            id=item.id,
            tema_id=tema_id,
            alternativos=tuple(dict.fromkeys(alternativos)),
            fora=fora,
            multitema=multitema,
            certeza=certeza,
            observacao=observacao.replace("\n", " "),
            minutos=round(minutos, 1),
            rotulado_em=datetime.now().isoformat(timespec="seconds"),
        )

    def _escolher_tema(self) -> str:
        """Laço de busca e escolha do tema central.

        Returns:
            ID escolhido, ou ``""`` para fora do recorte.

        Raises:
            _Pular: Se o usuário pular a questão.
            _Sair: Se o usuário sair.
        """
        while True:
            entrada: str = self._perguntar("Tema> ").strip()
            comando: str = entrada.lower()
            if comando in {"", "?"}:
                print(self.AJUDA)
            elif comando == "q":
                raise _Sair
            elif comando == "p":
                raise _Pular
            elif comando == "f":
                if self._sim_nao("Confirmar: fora do recorte? [s/N] "):
                    return ""
            elif entrada.isdigit():
                if self._confirmar_id(entrada):
                    return entrada
            else:
                self._listar(self._buscar(entrada), "Nenhum tema encontrado.")

    def _confirmar_id(self, tema_id: str) -> bool:
        """Mostra o tema digitado e pede confirmação.

        Args:
            tema_id: ID digitado.

        Returns:
            ``True`` se o ID é publicável e foi confirmado.
        """
        tema: TemaPreparado | None = self._temas.get(tema_id)
        if tema is None:
            print(f"{tema_id} não existe na árvore.")
            return False
        if tema.canonico_id is not None:
            print(f"{tema_id} é uma cópia sem histórico (fantasma); use o canônico {tema.canonico_id}.")
            return False
        filhos: list[TemaPreparado] = self._publicaveis(tema.filhos)
        if not tema.publicavel:
            self._listar(filhos, f"{tema_id} não pode ser rótulo e não tem filhos publicáveis.")
            return False
        print(f"→ {tema.tema_id} | {tema.caminho_exibicao}{self._marcas(tema)}")
        if filhos:
            print("  Tem filhos; se a questão for de um só deles, prefira o filho:")
            self._listar(filhos, "")
        return self._sim_nao(f"Confirmar {tema_id}? [S/n] ", padrao=True)

    def _escolher_alternativos(self, tema_id: str) -> list[str]:
        """Mostra os vizinhos do tema e pede os alternativos plausíveis.

        Args:
            tema_id: Tema central escolhido.

        Returns:
            IDs dos alternativos (podem ser vazios).
        """
        tema: TemaPreparado = self._temas[tema_id]
        pai: TemaPreparado | None = self._temas.get(tema.parent_id) if tema.parent_id is not None else None
        mostrados: set[str] = {tema_id, *tema.filhos}
        if pai is not None and pai.publicavel:
            print(f"Pai:    {pai.tema_id} | {pai.titulo_exibicao}")
            irmaos: list[TemaPreparado] = [irmao for irmao in self._publicaveis(pai.filhos) if irmao.tema_id != tema_id]
            self._linha_vizinhos("Irmãos:", irmaos)
            mostrados.update([pai.tema_id, *pai.filhos])
        self._linha_vizinhos("Filhos:", self._publicaveis(tema.filhos))
        if tema.grupo_sobreposicao:
            pares: list[TemaPreparado] = [
                outro
                for outro in self._temas.values()
                if outro.publicavel
                and outro.grupo_sobreposicao == tema.grupo_sobreposicao
                and outro.tema_id not in mostrados
            ]
            self._linha_vizinhos(f"Sobreposição ({tema.grupo_sobreposicao}):", pares, completo=True)
            print(f"  Regra: {tema.regra_desempate}")
        while True:
            entrada: str = self._perguntar("Alternativos (IDs separados por espaço; Enter = nenhum; texto = busca): ")
            partes: list[str] = entrada.replace(";", " ").replace(",", " ").split()
            if not partes:
                return []
            if not all(parte.isdigit() for parte in partes):
                self._listar(self._buscar(entrada), "Nenhum tema encontrado.")
                continue
            invalidos: list[str] = [parte for parte in partes if not self._eh_publicavel(parte)]
            if invalidos:
                print(f"Não publicáveis: {', '.join(invalidos)}. Digite de novo.")
                continue
            return [parte for parte in partes if parte != tema_id]

    def _certeza(self) -> str:
        """Pede o nível de certeza.

        Returns:
            ``alta``, ``media`` ou ``baixa``.
        """
        while True:
            entrada: str = self._perguntar("Certeza [a]lta / [m]édia / [b]aixa: ").strip().lower()
            if entrada[:1] in self.CERTEZAS:
                return self.CERTEZAS[entrada[:1]]
            print("Responda a, m ou b.")

    def _sim_nao(self, pergunta: str, padrao: bool = False) -> bool:
        """Pergunta de sim ou não.

        Args:
            pergunta: Texto exibido.
            padrao: Resposta para Enter.

        Returns:
            ``True`` para sim.
        """
        while True:
            entrada: str = self._perguntar(pergunta).strip().lower()
            if not entrada:
                return padrao
            if entrada[:1] in {"s", "n"}:
                return entrada[:1] == "s"
            print("Responda s ou n.")

    @staticmethod
    def _perguntar(texto: str) -> str:
        """Lê uma linha do terminal.

        Args:
            texto: Prompt exibido.

        Returns:
            O que foi digitado.

        Raises:
            _Sair: Em Ctrl+C, fim da entrada ou ``q`` isolado fora do laço de tema.
        """
        try:
            resposta: str = input(texto)
        except (EOFError, KeyboardInterrupt) as erro:
            raise _Sair from erro
        if resposta.strip().lower() == "q":
            raise _Sair
        return resposta

    def _buscar(self, consulta: str) -> list[TemaPreparado]:
        """Busca temas pela consulta.

        Args:
            consulta: Palavras digitadas.

        Returns:
            Temas encontrados.
        """
        return self._buscador.buscar(consulta) if self._buscador is not None else []

    def _publicaveis(self, ids: Sequence[str]) -> list[TemaPreparado]:
        """Filtra os IDs publicáveis.

        Args:
            ids: IDs de temas.

        Returns:
            Temas publicáveis, na mesma ordem.
        """
        return [self._temas[tema_id] for tema_id in ids if self._eh_publicavel(tema_id)]

    def _eh_publicavel(self, tema_id: str) -> bool:
        """Indica se o ID pode ser rótulo.

        Args:
            tema_id: ID.

        Returns:
            ``True`` se for publicável.
        """
        return tema_id in self._temas and self._temas[tema_id].publicavel

    @staticmethod
    def _marcas(tema: TemaPreparado) -> str:
        """Marcas exibidas ao lado do caminho.

        Args:
            tema: Tema.

        Returns:
            Texto das marcas (pode ser vazio).
        """
        marcas: list[str] = []
        if tema.lixeira == "forte":
            marcas.append("conceitual")
        if tema.grupo_sobreposicao:
            marcas.append(f"sobreposição: {tema.grupo_sobreposicao}")
        return f"  [{'; '.join(marcas)}]" if marcas else ""

    def _listar(self, temas: Sequence[TemaPreparado], vazio: str) -> None:
        """Lista temas como ``ID | caminho``.

        Args:
            temas: Temas a listar.
            vazio: Mensagem quando não há temas.
        """
        if not temas:
            if vazio:
                print(vazio)
            return
        tema: TemaPreparado
        for tema in temas:
            print(f"  {tema.tema_id} | {tema.caminho_exibicao}{self._marcas(tema)}")

    @staticmethod
    def _linha_vizinhos(titulo: str, temas: Sequence[TemaPreparado], completo: bool = False) -> None:
        """Mostra uma linha de vizinhos (ID e caminho).

        Args:
            titulo: Rótulo da linha.
            temas: Vizinhos.
            completo: Mostra o caminho com a disciplina (para pares de outra disciplina).
        """
        if temas:
            print(
                f"{titulo} "
                + " · ".join(
                    f"{tema.tema_id} {tema.caminho_exibicao if completo else tema.caminho_exibicao.split(' > ', 1)[-1]}"
                    for tema in temas
                )
            )
