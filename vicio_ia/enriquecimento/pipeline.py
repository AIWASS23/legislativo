"""Fase de conhecimento da etapa 2: orquestrador (ADR-019, ADR-020).

Por enquanto, um passo: as propostas de mapa lei/artigo → tema e de termos, por LLM, gravadas em
``dados/conhecimento/propostas/`` para a revisão do autor. Os próximos passos (citações das questões e
embeddings, ADR-021) entram aqui.
"""

from __future__ import annotations

import csv
from collections import Counter
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path
from typing import TextIO

from vicio_ia.configuracao import Caminhos, ParametrosConhecimento, ParametrosLLM
from vicio_ia.enriquecimento.manifesto import Manifesto
from vicio_ia.enriquecimento.propostas import GeradorPropostas, PropostasGrupo, ReferenciaProposta, TermoProposto
from vicio_ia.llm.cliente import ClienteLLM, FabricaClientes
from vicio_ia.llm.prompts import ArquivoPrompt
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.temas.cartoes import ArquivoCartoes, CartaoTema


class PipelineEnriquecimento:
    """Roda a fase de conhecimento e registra a proveniência de cada artefato."""

    COMANDO: str = "uv run python executar_enriquecimento.py"

    def __init__(
        self,
        caminhos: Caminhos | None = None,
        parametros: ParametrosConhecimento | None = None,
        parametros_llm: ParametrosLLM | None = None,
    ) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto.
            parametros: Parâmetros da fase de conhecimento.
            parametros_llm: Parâmetros de LLM.
        """
        self._caminhos: Caminhos = caminhos or Caminhos.padrao()
        self._parametros: ParametrosConhecimento = parametros or ParametrosConhecimento()
        self._parametros_llm: ParametrosLLM = parametros_llm or ParametrosLLM()

    def executar(self) -> Path:
        """Gera as propostas e grava os arquivos, o manifesto e o relatório.

        Returns:
            Caminho do relatório.
        """
        leitor: LeitorPreparados = LeitorPreparados(self._caminhos)
        temas: list[TemaPreparado] = leitor.temas()
        cartoes: list[CartaoTema] = ArquivoCartoes(self._caminhos.dados_temas / "cartoes.jsonl").ler()
        p: ParametrosConhecimento = self._parametros
        fabrica: FabricaClientes = FabricaClientes(self._caminhos, self._parametros_llm)
        cliente: ClienteLLM = fabrica.cliente_fixo(p.papel, p.provedor, p.modelo)
        prompt: ArquivoPrompt = ArquivoPrompt(self._caminhos.prompts / "conhecimento_tema.md")
        gerador: GeradorPropostas = GeradorPropostas(
            cliente, prompt, temas, leitor.arvore_enxuta(), cartoes, p, fabrica.paralelismo(cliente.provedor)
        )
        print(
            f"Propostas de conhecimento: {len(gerador.grupos())} chamadas com {cliente.provedor}:{cliente.modelo} "
            f"(prompt {prompt.versao}), até {fabrica.paralelismo(cliente.provedor)} em paralelo"
        )
        try:
            resultados: list[PropostasGrupo] = gerador.gerar()
        finally:
            fabrica.escrever_resumo_custos()
            print(f"Chamadas: {fabrica.resumo_sessao()}")
        caminho: dict[str, str] = {t.tema_id: t.caminho_exibicao for t in temas}
        referencias: list[ReferenciaProposta] = sorted(
            (r for g in resultados for r in g.referencias), key=lambda r: (caminho[r.tema_id], r.lei, r.art_inicio)
        )
        termos: list[TermoProposto] = sorted(
            (t for g in resultados for t in g.termos), key=lambda t: (caminho[t.tema_id], t.tipo, t.normalizado)
        )
        avisos: list[str] = [a for g in resultados for a in g.avisos]
        pasta: Path = self._caminhos.dados_conhecimento / "propostas"
        pasta.mkdir(parents=True, exist_ok=True)
        origem: str = f"llm:{cliente.provedor}:{cliente.modelo}@{prompt.versao}"
        arquivo_mapa: Path = self._gravar_mapa(pasta / "mapa_artigos.csv", referencias, caminho, origem)
        arquivo_termos: Path = self._gravar_termos(pasta / "termos.csv", termos, caminho, origem)
        manifesto: Manifesto = Manifesto(self._caminhos.dados_conhecimento / "manifesto.json", self._caminhos.raiz)
        detalhes: dict[str, str] = {
            "provedor": cliente.provedor,
            "modelo": cliente.modelo,
            "prompt": prompt.versao,
            "chamadas": str(len(resultados)),
            "entrada": "árvore preparada e cartões da etapa 1; nenhuma questão",
            "revisao": "pendente",
        }
        arquivo: Path
        for arquivo in (arquivo_mapa, arquivo_termos):
            manifesto.registrar(arquivo, "llm (proposta, sem revisão)", self.COMANDO, detalhes)
        return self._relatorio(referencias, termos, avisos, temas, origem)

    @staticmethod
    def _gravar_mapa(
        destino: Path, referencias: Sequence[ReferenciaProposta], caminho: dict[str, str], origem: str
    ) -> Path:
        """Grava o mapa de artigos proposto.

        Args:
            destino: Arquivo.
            referencias: Referências.
            caminho: Caminho de exibição por tema.
            origem: Origem registrada em cada linha.

        Returns:
            O próprio destino.
        """
        linhas: list[list[str]] = [["lei", "art_inicio", "art_fim", "tema_id", "caminho", "forca", "origem"]]
        linhas.extend(
            [r.lei, str(r.art_inicio), str(r.art_fim), r.tema_id, caminho[r.tema_id], r.forca, origem]
            for r in referencias
        )
        arquivo: TextIO
        with destino.open("w", encoding="utf-8", newline="") as arquivo:
            csv.writer(arquivo).writerows(linhas)
        return destino

    @staticmethod
    def _gravar_termos(destino: Path, termos: Sequence[TermoProposto], caminho: dict[str, str], origem: str) -> Path:
        """Grava o dicionário de termos proposto.

        Args:
            destino: Arquivo.
            termos: Termos.
            caminho: Caminho de exibição por tema.
            origem: Origem registrada em cada linha.

        Returns:
            O próprio destino.
        """
        linhas: list[list[str]] = [
            ["termo", "termo_normalizado", "tema_id", "caminho", "tipo", "tema_id_alvo", "origem"]
        ]
        linhas.extend(
            [t.termo, t.normalizado, t.tema_id, caminho[t.tema_id], t.tipo, t.tema_id_alvo, origem] for t in termos
        )
        arquivo: TextIO
        with destino.open("w", encoding="utf-8", newline="") as arquivo:
            csv.writer(arquivo).writerows(linhas)
        return destino

    def _relatorio(
        self,
        referencias: Sequence[ReferenciaProposta],
        termos: Sequence[TermoProposto],
        avisos: Sequence[str],
        temas: Sequence[TemaPreparado],
        origem: str,
    ) -> Path:
        """Grava o resumo das propostas para orientar a revisão.

        Args:
            referencias: Referências aceitas.
            termos: Termos aceitos.
            avisos: Itens descartados.
            temas: Árvore preparada.
            origem: Modelo e versão do prompt.

        Returns:
            Caminho do relatório.
        """
        publicaveis: int = sum(1 for t in temas if t.publicavel)
        com_referencia: int = len({r.tema_id for r in referencias})
        tipos: Counter[str] = Counter(t.tipo for t in termos)
        leis: Counter[str] = Counter(r.lei for r in referencias)
        repetidos: Counter[str] = Counter(t.normalizado for t in termos if t.tipo == "forte")
        conflitos: list[str] = sorted(n for n, q in repetidos.items() if q > 1)
        linhas: list[str] = [
            "# Propostas de conhecimento dos temas (para revisão)",
            "",
            f"Gerado em {datetime.now():%d/%m/%Y %H:%M} por `{origem}`. Entrada: árvore e cartões; nenhuma questão.",
            "",
            f"- Referências legais: {len(referencias)}, em {com_referencia} de {publicaveis} temas publicáveis.",
            f"- Leis: {', '.join(f'{lei} ({q})' for lei, q in leis.most_common())}.",
            f"- Termos: {len(termos)} ({', '.join(f'{tipo} {q}' for tipo, q in sorted(tipos.items()))}).",
            f"- Termos `forte` repetidos em mais de um tema (conflitos a resolver na revisão): {len(conflitos)}.",
            f"- Itens descartados na conversão: {len(avisos)}.",
            "",
            "Arquivos: `dados/conhecimento/propostas/mapa_artigos.csv` e `termos.csv`.",
            "",
        ]
        if conflitos:
            linhas.extend(["## Termos fortes em mais de um tema", "", *(f"- {c}" for c in conflitos), ""])
        if avisos:
            linhas.extend(["## Itens descartados", "", *(f"- {a}" for a in avisos), ""])
        pasta: Path = self._caminhos.saida_etapa2
        pasta.mkdir(parents=True, exist_ok=True)
        destino: Path = pasta / "propostas_conhecimento.md"
        destino.write_text("\n".join(linhas), encoding="utf-8")
        print(
            f"{len(referencias)} referências ({com_referencia} temas), {len(termos)} termos, {len(avisos)} descartes."
            f"\nRelatório: {destino}"
        )
        return destino
