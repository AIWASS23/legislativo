"""Escolha interativa dos modelos por papel, a partir da análise da máquina."""

from __future__ import annotations

import sys
from typing import ClassVar

from vicio_ia.configuracao import Caminhos, ParametrosLLM
from vicio_ia.infra.pipeline import PipelineInfra, ResultadoInfra
from vicio_ia.infra.recomendador import AvaliacaoModelo
from vicio_ia.llm.selecao import ArquivoEscolha


class EscolhaInterativa:
    """Mostra os modelos viáveis nesta máquina e grava a escolha em ``config/escolha_modelos.json``.

    Não usa argumentos de linha de comando: as perguntas são feitas no terminal. Fora de um
    terminal interativo, apenas mostra as opções e não grava nada.
    """

    RESPOSTAS_SIM: ClassVar[frozenset[str]] = frozenset({"", "s", "sim", "y", "yes"})

    def __init__(self, caminhos: Caminhos | None = None, parametros: ParametrosLLM | None = None) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto (opcional).
            parametros: Parâmetros de LLM (opcional).
        """
        self._caminhos: Caminhos = caminhos if caminhos is not None else Caminhos.padrao()
        self._parametros: ParametrosLLM = parametros if parametros is not None else ParametrosLLM()

    def executar(self) -> bool:
        """Conduz a escolha.

        Returns:
            ``True`` se uma escolha foi gravada.
        """
        print("Analisando a máquina e os provedores...", flush=True)
        resultado: ResultadoInfra = PipelineInfra(self._caminhos, self._parametros).analisar()
        opcoes: list[AvaliacaoModelo] = [a for a in resultado.recomendacao.avaliacoes if a.viavel]
        self._listar(opcoes, resultado)
        if not sys.stdin.isatty():
            print(
                "\nSem terminal interativo: nada foi gravado. Edite config/escolha_modelos.json ou rode num terminal."
            )
            return False
        arquivo: ArquivoEscolha = ArquivoEscolha(self._caminhos.escolha_modelos)
        if input("\nUsar a sugestão automática em todos os papéis? [S/n] ").strip().lower() in self.RESPOSTAS_SIM:
            arquivo.gravar("auto", {})
            print(f"Gravado: modo automático em {self._caminhos.escolha_modelos}")
            return True
        escolhas: dict[str, tuple[str, str]] = {}
        papel: str
        for papel in self._parametros.papeis:
            avaliacao: AvaliacaoModelo | None = self._perguntar(papel, opcoes, resultado.recomendacao.papeis.get(papel))
            if avaliacao is not None:
                escolhas[papel] = (avaliacao.modelo.provedor, avaliacao.modelo.modelo)
        arquivo.gravar("manual", escolhas)
        print(f"Gravado: escolha manual em {self._caminhos.escolha_modelos}")
        return True

    def _listar(self, opcoes: list[AvaliacaoModelo], resultado: ResultadoInfra) -> None:
        """Imprime a lista numerada de modelos viáveis e as sugestões.

        Args:
            opcoes: Modelos viáveis (prontos primeiro).
            resultado: Análise completa.
        """
        print("\nModelos viáveis nesta máquina (* = pronto para usar agora):")
        posicao: int
        avaliacao: AvaliacaoModelo
        for posicao, avaliacao in enumerate(opcoes, start=1):
            marca: str = "*" if avaliacao.pronto else " "
            print(
                f" {posicao:3}{marca} {avaliacao.modelo.chave:55} q{avaliacao.nota_qualidade} "
                f"{avaliacao.execucao or '':12} {avaliacao.motivo[:70]}"
            )
        print("\nSugestão automática:")
        papel: str
        sugerida: AvaliacaoModelo | None
        for papel, sugerida in resultado.recomendacao.papeis.items():
            print(f"  {papel:16} {sugerida.modelo.chave if sugerida else '(nenhum modelo pronto)'}")

    def _perguntar(
        self, papel: str, opcoes: list[AvaliacaoModelo], sugerida: AvaliacaoModelo | None
    ) -> AvaliacaoModelo | None:
        """Pergunta o modelo de um papel até receber uma resposta válida.

        Args:
            papel: Nome do papel.
            opcoes: Modelos viáveis numerados.
            sugerida: Sugestão automática (usada com Enter).

        Returns:
            A avaliação escolhida, ou ``None`` para deixar o papel em automático.
        """
        padrao: int | None = next((i for i, a in enumerate(opcoes, start=1) if a is sugerida), None)
        dica: str = f"Enter = {padrao}" if padrao else "Enter = automático"
        while True:
            resposta: str = input(f"{papel} [{dica}]: ").strip()
            if not resposta:
                return sugerida
            if not resposta.isdigit() or not 1 <= int(resposta) <= len(opcoes):
                print(f"  Digite um número de 1 a {len(opcoes)}.")
                continue
            escolhida: AvaliacaoModelo = opcoes[int(resposta) - 1]
            if escolhida.pronto:
                return escolhida
            confirma: str = input(f"  Não está pronto ({escolhida.motivo[:90]}). Usar mesmo assim? [s/N] ")
            if confirma.strip().lower() in self.RESPOSTAS_SIM - {""}:
                return escolhida
