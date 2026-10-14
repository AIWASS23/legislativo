"""Orquestração da EDA: carrega, perfila, analisa e grava as saídas."""

from __future__ import annotations

from pathlib import Path

from vicio_ia.arvore import ArvoreTemas
from vicio_ia.carregamento import CarregadorDados, RegistroBruto
from vicio_ia.configuracao import Caminhos, ParametrosEDA
from vicio_ia.conhecimento import MapaLegislacao
from vicio_ia.dominio import Questao, Tema
from vicio_ia.eda.analise_cruzada import AnaliseCruzada
from vicio_ia.eda.analise_questoes import AnaliseQuestoes
from vicio_ia.eda.analise_temas import AnaliseTemas
from vicio_ia.eda.estatisticas import CalculadoraEstatisticas
from vicio_ia.eda.perfil_questoes import PerfiladorQuestoes, PerfilQuestao
from vicio_ia.eda.perfil_temas import PerfiladorTemas, PerfilTema
from vicio_ia.relatorio import Analise, EscritorRelatorio, Secao
from vicio_ia.texto import ProcessadorTexto


class PipelineEDA:
    """Executa a EDA completa com a configuração padrão do projeto.

    Saídas em ``saidas/eda/``:

    * ``relatorio_eda.md``: relatório legível, seção por seção;
    * ``resumo_eda.json``: números-chave de cada seção;
    * ``tabelas/*.csv``: todas as tabelas completas, mais ``perfil_questoes.csv``
      e ``perfil_temas.csv`` (base do passo 01).
    """

    def __init__(self, caminhos: Caminhos | None = None, parametros: ParametrosEDA | None = None) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos de entrada e saída (opcional, útil em testes).
            parametros: Limiares da EDA (opcional, útil em testes).
        """
        self._caminhos: Caminhos = caminhos if caminhos is not None else Caminhos.padrao()
        self._parametros: ParametrosEDA = parametros if parametros is not None else ParametrosEDA()

    def executar(self) -> Path:
        """Roda a EDA de ponta a ponta.

        Returns:
            Caminho do relatório Markdown gerado.
        """
        carregador: CarregadorDados = CarregadorDados(self._caminhos)
        registros: list[RegistroBruto] = carregador.ler_questoes_brutas()
        questoes: list[Questao] = carregador.para_questoes(registros)
        temas: list[Tema] = carregador.carregar_temas()

        processador: ProcessadorTexto = ProcessadorTexto()
        legislacao: MapaLegislacao = MapaLegislacao(processador)
        estatisticas: CalculadoraEstatisticas = CalculadoraEstatisticas()
        arvore: ArvoreTemas = ArvoreTemas(temas)

        perfilador_questoes: PerfiladorQuestoes = PerfiladorQuestoes(self._parametros, processador, legislacao)
        perfis_questoes: list[PerfilQuestao] = perfilador_questoes.perfilar_todas(questoes)
        perfis_temas: list[PerfilTema] = PerfiladorTemas(arvore, self._parametros, processador).perfilar_todos()

        analises: list[Analise] = [
            AnaliseQuestoes(
                registros,
                questoes,
                perfis_questoes,
                perfilador_questoes,
                processador,
                legislacao,
                estatisticas,
                self._parametros,
            ),
            AnaliseTemas(arvore, perfis_temas, processador, estatisticas, self._parametros),
            AnaliseCruzada(perfis_questoes, perfis_temas, arvore, processador, legislacao, estatisticas),
        ]
        secoes: list[Secao] = []
        analise: Analise
        for analise in analises:
            secoes.extend(analise.executar())

        escritor: EscritorRelatorio = EscritorRelatorio(self._caminhos.saida_eda, self._parametros.linhas_por_tabela_md)
        escritor.preparar_pasta()
        escritor.escrever_csv(
            "perfil_questoes", PerfilQuestao.colunas(), [perfil.como_linha() for perfil in perfis_questoes]
        )
        escritor.escrever_csv("perfil_temas", PerfilTema.colunas(), [perfil.como_linha() for perfil in perfis_temas])
        relatorio: Path = escritor.escrever("EDA: questões e árvore de temas", self._introducao(), secoes)
        self._imprimir_resumo(relatorio, len(questoes), len(arvore), secoes)
        return relatorio

    def _introducao(self) -> list[str]:
        """Texto exibido no topo do relatório.

        Returns:
            Parágrafos de introdução.
        """
        return [
            f"Fontes: `{self._caminhos.questoes.name}` e `{self._caminhos.temas.name}` (pasta `anexos/`, sem alterações).",
            (
                "Cada seção traz os achados em tópicos e tabelas de apoio. O Markdown mostra só as primeiras linhas de "
                "cada tabela; as versões completas estão em `tabelas/`. `tabelas/perfil_questoes.csv` e "
                "`tabelas/perfil_temas.csv` têm uma linha por questão e por tema, com todas as marcas calculadas."
            ),
            (
                "As heurísticas (lixeiras, fantasmas, comandos suspeitos, enunciados genéricos) servem para orientar a "
                "revisão humana, não para decidir sozinhas. Os limiares estão em `vicio_ia/configuracao.py`."
            ),
            "Para gerar de novo: `uv run python executar_eda.py`.",
        ]

    @staticmethod
    def _imprimir_resumo(relatorio: Path, n_questoes: int, n_temas: int, secoes: list[Secao]) -> None:
        """Mostra no terminal onde ficaram as saídas.

        Args:
            relatorio: Caminho do relatório.
            n_questoes: Número de questões lidas.
            n_temas: Número de temas lidos.
            secoes: Seções geradas.
        """
        n_tabelas: int = sum(len(secao.tabelas) for secao in secoes)
        print(f"EDA concluída: {n_questoes} questões, {n_temas} temas, {len(secoes)} seções, {n_tabelas} tabelas.")
        print(f"Relatório: {relatorio}")
        print(f"Tabelas:   {relatorio.parent / 'tabelas'}")
