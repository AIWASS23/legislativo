"""Experimento E4 (ADR-014): os cartões de tema reduzem o erro? Classificador B com cartões × só títulos.

Adaptação ao limite das assinaturas: a ADR previa o E4 com o classificador A, cuja cota (``codex``)
é a mais escassa. Aqui o E4 usa o classificador B (Gemini, cota livre), mudando só o material do
prompt: escopo e cartões, ou só ID e caminho. Mesmo modelo, mesmos prompts, mesmas questões.
"""

from __future__ import annotations

from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor

from vicio_ia.arvore import ArvoreTemas
from vicio_ia.avaliacao.experimentos import RegistroExperimentos
from vicio_ia.avaliacao.metricas import AvaliadorGold, PrevisaoSistema, ResultadoAvaliacao
from vicio_ia.avaliacao.planilha import PlanilhaRotulos, RotuloGold, SituacaoLinha
from vicio_ia.avaliacao.pontuador import ModoRegua, PontuadorRegua
from vicio_ia.carregamento import CarregadorDados
from vicio_ia.classificacao.classificadores import ClassificadorHierarquico
from vicio_ia.classificacao.montador_prompt import MontadorPrompt
from vicio_ia.classificacao.respostas import VotoClassificador
from vicio_ia.classificacao.schemas import FabricaSchemas
from vicio_ia.configuracao import Caminhos, ParametrosClassificacao, ParametrosGold, ParametrosLLM
from vicio_ia.llm.cliente import FabricaClientes
from vicio_ia.llm.prompts import ArquivoPrompt
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada
from vicio_ia.temas.arvore_prompt import MaterialArvore
from vicio_ia.temas.cartoes import ArquivoCartoes


class ExperimentoCartoes:
    """Roda o E4 nas questões rotuladas da leva 1 e registra o resultado."""

    def __init__(self, caminhos: Caminhos | None = None) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto (opcional).
        """
        self._caminhos: Caminhos = caminhos if caminhos is not None else Caminhos.padrao()

    def executar(self) -> None:
        """Classifica o gold com B nas duas versões do material e compara pela régua."""
        leitor: LeitorPreparados = LeitorPreparados(self._caminhos)
        temas: list[TemaPreparado] = leitor.temas()
        questoes: dict[str, QuestaoPreparada] = {q.id: q for q in leitor.questoes()}
        planilha: PlanilhaRotulos = PlanilhaRotulos(
            self._caminhos.dados_gold / "rotulos_leva1.csv", ParametrosGold(), temas
        )
        situacoes: list[SituacaoLinha] = planilha.validar(planilha.ler())
        rotulos: list[RotuloGold] = [s.rotulo for s in situacoes if s.situacao == "rotulada"]
        material: MaterialArvore = MaterialArvore(
            temas, ArquivoCartoes(self._caminhos.dados_temas / "cartoes.jsonl").ler(), leitor.arvore_enxuta()
        )
        parametros: ParametrosLLM = ParametrosLLM()
        fabrica: FabricaClientes = FabricaClientes(self._caminhos, parametros)
        montador: MontadorPrompt = MontadorPrompt(parametros, ParametrosClassificacao().chars_por_token_local)
        schemas: FabricaSchemas = FabricaSchemas(temas)
        prompt_tema: ArquivoPrompt = ArquivoPrompt(self._caminhos.prompts / "classificador_hierarquico_tema.md")
        prompt_sub: ArquivoPrompt = ArquivoPrompt(self._caminhos.prompts / "classificador_hierarquico_subtema.md")
        avaliador: AvaliadorGold = AvaliadorGold(
            PontuadorRegua(ArvoreTemas(CarregadorDados(self._caminhos).carregar_temas()))
        )
        registro: RegistroExperimentos = RegistroExperimentos(self._caminhos.raiz / "saidas" / "experimentos")
        variantes: list[tuple[str, str, bool]] = [
            ("classificador_b", "B com escopo e cartões", True),
            ("e4_b_so_titulos", "B só com títulos (sem escopo nem cartões)", False),
        ]
        papel: str
        descricao: str
        com_cartoes: bool
        for papel, descricao, com_cartoes in variantes:
            classificador: ClassificadorHierarquico = ClassificadorHierarquico(
                fabrica.cliente(papel, "classificador_b"),
                montador,
                schemas,
                prompt_tema,
                prompt_sub,
                material,
                temas,
                com_cartoes,
            )
            votos: list[VotoClassificador] = self._classificar(
                classificador, [questoes[r.id] for r in rotulos], fabrica.paralelismo(classificador.cliente.provedor)
            )
            previsoes: dict[str, PrevisaoSistema] = {
                r.id: PrevisaoSistema(r.id, v.tema_id, v.autoconfianca or 0.0)
                for r, v in zip(rotulos, votos, strict=True)
                if v.ok
            }
            modelo: str = f"{classificador.cliente.provedor}:{classificador.cliente.modelo}"
            falhas: int = sum(1 for voto in votos if not voto.ok)
            modo: ModoRegua
            for modo in ("estrita", "tolerante"):
                resultado: ResultadoAvaliacao = avaliador.avaliar(previsoes, rotulos, modo)
                registro.registrar("E4", descricao, resultado, modelo, f"{falhas} falhas" if falhas else "")
                print(
                    f"  E4 {descricao} ({modo}): {resultado.acertos_top1}/{resultado.com_tema} certas "
                    f"({resultado.precisao_top1:.0%}); cobertura a 95%: {resultado.cobertura_95:.0%}"
                )
        fabrica.escrever_resumo_custos()
        print(f"Chamadas: {fabrica.resumo_sessao()}\nResultados: {registro.arquivo}")

    @staticmethod
    def _classificar(
        classificador: ClassificadorHierarquico, questoes: Sequence[QuestaoPreparada], paralelismo: int
    ) -> list[VotoClassificador]:
        """Classifica em paralelo, mantendo a ordem.

        Args:
            classificador: Variante de B.
            questoes: Questões do gold.
            paralelismo: Chamadas simultâneas.

        Returns:
            Votos na ordem das questões.
        """
        executor: ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=paralelismo) as executor:
            return list(executor.map(classificador.classificar, questoes))
