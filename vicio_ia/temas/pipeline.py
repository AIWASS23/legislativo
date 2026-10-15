"""Orquestração do passo 02: rascunhos por LLM, ajustes manuais, checagens e versões da árvore (ADR-007)."""

from __future__ import annotations

from pathlib import Path

from vicio_ia.carregamento import CarregadorDados
from vicio_ia.configuracao import Caminhos, ParametrosCartoes, ParametrosLLM, ParametrosPreparacao
from vicio_ia.llm.cliente import ClienteLLM, FabricaClientes
from vicio_ia.llm.prompts import ArquivoPrompt
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.preparacao.validacao import ResultadoChecagem
from vicio_ia.temas.arvore_prompt import MaterialArvore, TamanhoMaterial
from vicio_ia.temas.cartoes import AjustesCartoes, ArquivoCartoes, CartaoTema, ErroCartoes, ValidadorCartoes
from vicio_ia.temas.gerador_cartoes import GeradorCartoes
from vicio_ia.temas.revisao import CadernoRevisaoCartoes
from vicio_ia.texto import ProcessadorTexto


class PipelineCartoes:
    """Gera, ajusta, confere e grava os cartões de tema.

    Saídas:

    * ``dados/temas/cartoes_gerados.jsonl``: rascunhos do modelo (refeitos do cache sem custo);
    * ``dados/temas/cartoes_ajustes.csv``: correções manuais (criado vazio; nunca sobrescrito);
    * ``dados/temas/cartoes.jsonl`` e ``arvore_escopo.txt``: cartões finais e árvore com escopo,
      gravados só se todas as checagens passarem;
    * ``saidas/cartoes/revisao_cartoes.md`` e ``relatorio_cartoes.md``: revisão priorizada,
      checagens e tamanho de cada versão do material.
    """

    def __init__(
        self,
        caminhos: Caminhos | None = None,
        parametros: ParametrosCartoes | None = None,
        parametros_llm: ParametrosLLM | None = None,
        parametros_preparacao: ParametrosPreparacao | None = None,
    ) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto (opcional).
            parametros: Parâmetros do passo 02 (opcional).
            parametros_llm: Parâmetros de LLM (opcional).
            parametros_preparacao: Parâmetros do passo 01, para estimar tokens (opcional).
        """
        self._caminhos: Caminhos = caminhos if caminhos is not None else Caminhos.padrao()
        self._parametros: ParametrosCartoes = parametros if parametros is not None else ParametrosCartoes()
        self._parametros_llm: ParametrosLLM = parametros_llm if parametros_llm is not None else ParametrosLLM()
        self._preparacao: ParametrosPreparacao = (
            parametros_preparacao if parametros_preparacao is not None else ParametrosPreparacao()
        )

    def executar(self) -> Path:
        """Roda o passo 02.

        Returns:
            Caminho de ``dados/temas/cartoes.jsonl``.

        Raises:
            ErroCartoes: Se alguma checagem dos cartões finais falhar.
        """
        leitor: LeitorPreparados = LeitorPreparados(self._caminhos)
        temas: list[TemaPreparado] = leitor.temas()
        enxuta: str = leitor.arvore_enxuta()
        descricoes: dict[str, str] = {
            tema.tema_id: tema.descricao.strip()
            for tema in CarregadorDados(self._caminhos).carregar_temas()
            if tema.tipo_descricao == "rica"
        }
        fabrica: FabricaClientes = FabricaClientes(self._caminhos, self._parametros_llm)
        cliente: ClienteLLM = fabrica.cliente("cartoes", self._parametros.papel_modelo)
        prompt: ArquivoPrompt = ArquivoPrompt(self._caminhos.prompts / "cartao_tema.md")
        gerador: GeradorCartoes = GeradorCartoes(
            cliente, prompt, temas, enxuta, descricoes, self._parametros, fabrica.paralelismo(cliente.provedor)
        )
        print(
            f"Cartões: {len(gerador.grupos())} chamadas com {cliente.provedor}:{cliente.modelo} "
            f"(prompt {prompt.versao}), até {fabrica.paralelismo(cliente.provedor)} em paralelo"
        )
        try:
            gerados: list[CartaoTema] = gerador.gerar()
        finally:
            fabrica.escrever_resumo_custos()
            print(f"Chamadas: {fabrica.resumo_sessao()}")
        ArquivoCartoes(self._caminhos.dados_temas / "cartoes_gerados.jsonl").gravar(gerados)

        ajustes: AjustesCartoes = AjustesCartoes(self._caminhos.dados_temas / "cartoes_ajustes.csv")
        ajustes.garantir()
        finais: list[CartaoTema] = ajustes.aplicar(gerados, ajustes.ler())
        checagens: list[ResultadoChecagem] = ValidadorCartoes(self._parametros.max_chars_escopo).validar(finais, temas)
        material: MaterialArvore = MaterialArvore(temas, finais, enxuta)
        revisao: Path = CadernoRevisaoCartoes(ProcessadorTexto(), self._parametros.limiar_similaridade_irmaos).escrever(
            self._caminhos.saida_cartoes / "revisao_cartoes.md", finais, temas, material
        )
        tamanhos: list[TamanhoMaterial] = material.tamanhos(self._preparacao.chars_por_token)
        relatorio: Path = self._escrever_relatorio(finais, checagens, tamanhos)
        falhas: list[ResultadoChecagem] = [c for c in checagens if not c.aprovada]
        if falhas:
            detalhes: str = "; ".join(f"{f.regra}: {', '.join(f.violacoes)}" for f in falhas)
            raise ErroCartoes(f"checagens reprovadas (veja {relatorio}): {detalhes}")
        destino: Path = self._caminhos.dados_temas / "cartoes.jsonl"
        ArquivoCartoes(destino).gravar(finais)
        (self._caminhos.dados_temas / "arvore_escopo.txt").write_text(material.com_escopo(), encoding="utf-8")
        ajustados: int = sum(1 for cartao in finais if cartao.origem == "ajustado")
        print(f"{len(finais)} cartões ({ajustados} ajustados à mão); {len(checagens)}/{len(checagens)} checagens ok")
        tamanho: TamanhoMaterial
        for tamanho in tamanhos:
            print(f"  {tamanho.nome}: {tamanho.bytes:,} bytes, ~{tamanho.tokens:,} tokens")
        print(f"Cartões: {destino}\nRevisão: {revisao}")
        return destino

    def _escrever_relatorio(
        self,
        cartoes: list[CartaoTema],
        checagens: list[ResultadoChecagem],
        tamanhos: list[TamanhoMaterial],
    ) -> Path:
        """Grava o relatório do passo 02.

        Args:
            cartoes: Cartões finais.
            checagens: Resultado das checagens.
            tamanhos: Tamanho de cada versão do material.

        Returns:
            Caminho do relatório.
        """
        sem_ancora: int = sum(1 for cartao in cartoes if not cartao.ancoras_legais)
        media_nao_inclui: float = sum(len(c.nao_inclui) for c in cartoes) / len(cartoes) if cartoes else 0.0
        linhas: list[str] = [
            "# Passo 02: cartões de tema",
            "",
            f"- Cartões: {len(cartoes)}; ajustados à mão: {sum(1 for c in cartoes if c.origem == 'ajustado')}.",
            f"- Sem âncora legal: {sem_ancora}; itens de `nao_inclui` por cartão: {media_nao_inclui:.1f} em média.",
            f"- Modelos: {', '.join(sorted({c.modelo for c in cartoes}))}.",
            "",
            "## Checagens",
            "",
            "| Regra | Resultado | Violações |",
            "|---|---|---|",
        ]
        linhas.extend(
            f"| {c.regra} | {'ok' if c.aprovada else 'FALHOU'} | {', '.join(c.violacoes) or '—'} |" for c in checagens
        )
        linhas.extend(["", "## Tamanho de cada versão do material (ADR-007, ADR-008)", ""])
        linhas.extend(["| Versão | Bytes | Tokens estimados |", "|---|---:|---:|"])
        linhas.extend(f"| {t.nome} | {t.bytes:,} | {t.tokens:,} |" for t in tamanhos)
        destino: Path = self._caminhos.saida_cartoes / "relatorio_cartoes.md"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")
        return destino
