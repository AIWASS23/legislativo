"""Teste rápido de ponta a ponta: uma questão simples enviada ao modelo de cada papel."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import ClassVar

from vicio_ia.configuracao import Caminhos, ParametrosLLM
from vicio_ia.llm.contratos import ErroProvedor, ProvedorLLM, RequisicaoLLM, RespostaLLM
from vicio_ia.llm.fabrica import FabricaProvedores
from vicio_ia.llm.selecao import EscolhaPapel, SeletorModelos


@dataclass(frozen=True)
class ResultadoTeste:
    """Resultado do teste de um modelo.

    Attributes:
        papeis: Papéis que usam este modelo.
        provedor: Provedor.
        modelo: Modelo.
        sucesso: A chamada funcionou e devolveu JSON válido.
        acertou: Escolheu o tema esperado.
        resposta: Resposta estruturada ou mensagem de erro.
        latencia_s: Tempo da chamada.
        tokens_entrada: Tokens de entrada (com cache).
        tokens_saida: Tokens de saída.
        custo_usd: Custo informado pelo provedor, se houver.
    """

    papeis: tuple[str, ...]
    provedor: str
    modelo: str
    sucesso: bool
    acertou: bool
    resposta: str
    latencia_s: float
    tokens_entrada: int
    tokens_saida: int
    custo_usd: float | None


class TesteProvedores:
    """Envia uma questão fácil, com saída estruturada, a cada modelo resolvido e mostra o resultado."""

    SISTEMA: ClassVar[str] = (
        "Você classifica questões de concurso de Direito Penal em um tema. "
        "Escolha o tema central entre as opções do schema e justifique em uma frase."
    )
    QUESTAO: ClassVar[str] = (
        "Tício, aproveitando a distração da vítima, pegou o celular que ela deixara sobre a mesa do bar "
        "e foi embora sem usar violência ou grave ameaça. Que crime Tício cometeu?\n"
        "Temas possíveis: 5159 = Furto; 5160 = Roubo; 5150 = Homicídio."
    )
    TEMA_ESPERADO: ClassVar[str] = "5159"
    SCHEMA: ClassVar[dict[str, object]] = {
        "type": "object",
        "properties": {
            "tema_id": {"type": "string", "enum": ["5159", "5160", "5150"]},
            "justificativa": {"type": "string"},
        },
        "required": ["tema_id", "justificativa"],
        "additionalProperties": False,
    }

    def __init__(self, caminhos: Caminhos | None = None, parametros: ParametrosLLM | None = None) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto (opcional).
            parametros: Parâmetros de LLM (opcional).
        """
        self._caminhos: Caminhos = caminhos if caminhos is not None else Caminhos.padrao()
        self._parametros: ParametrosLLM = parametros if parametros is not None else ParametrosLLM()

    def executar(self) -> bool:
        """Testa cada modelo distinto escolhido para os papéis.

        Returns:
            ``True`` se todos responderam com JSON válido.
        """
        escolhas: dict[str, EscolhaPapel] = SeletorModelos(self._caminhos, self._parametros).resolver()
        if not escolhas:
            print("Nenhum modelo resolvido. Rode executar_infra.py para ver o que falta.")
            return False
        agrupados: dict[tuple[str, str], list[str]] = {}
        escolha: EscolhaPapel
        for escolha in escolhas.values():
            agrupados.setdefault((escolha.provedor, escolha.modelo), []).append(escolha.papel)
        fabrica: FabricaProvedores = FabricaProvedores(self._caminhos, self._parametros)
        requisicao: RequisicaoLLM = RequisicaoLLM(self.SISTEMA, self.QUESTAO, self.SCHEMA, "classificacao", 512)
        resultados: list[ResultadoTeste] = []
        chave: tuple[str, str]
        papeis: list[str]
        for chave, papeis in agrupados.items():
            print(f"Testando {chave[0]}:{chave[1]} ({', '.join(papeis)})...", flush=True)
            resultados.append(self._testar(fabrica, chave[0], chave[1], tuple(papeis), requisicao))
        self._imprimir(resultados)
        destino: Path = self._caminhos.saida_infra / "teste_llm.json"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(
            json.dumps([asdict(r) for r in resultados], ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Detalhes: {destino}")
        return all(resultado.sucesso for resultado in resultados)

    def _testar(
        self, fabrica: FabricaProvedores, provedor: str, modelo: str, papeis: tuple[str, ...], requisicao: RequisicaoLLM
    ) -> ResultadoTeste:
        """Faz a chamada de teste a um modelo.

        Args:
            fabrica: Fábrica de provedores.
            provedor: Nome do provedor.
            modelo: Modelo.
            papeis: Papéis que usam o modelo.
            requisicao: Questão de teste.

        Returns:
            Resultado do teste (falhas viram ``sucesso=False``, sem interromper os demais).
        """
        try:
            instancia: ProvedorLLM = fabrica.obter(provedor)
            resposta: RespostaLLM = instancia.gerar(requisicao, modelo)
        except ErroProvedor as erro:
            return ResultadoTeste(papeis, provedor, modelo, False, False, str(erro), 0.0, 0, 0, None)
        dados: dict[str, object] = resposta.dados or {}
        entrada: int = resposta.uso.entrada + resposta.uso.cache_lido + resposta.uso.cache_escrito
        return ResultadoTeste(
            papeis=papeis,
            provedor=provedor,
            modelo=resposta.modelo,
            sucesso=True,
            acertou=str(dados.get("tema_id")) == self.TEMA_ESPERADO,
            resposta=json.dumps(dados, ensure_ascii=False),
            latencia_s=round(resposta.latencia_s, 2),
            tokens_entrada=entrada,
            tokens_saida=resposta.uso.saida,
            custo_usd=resposta.custo_usd,
        )

    @staticmethod
    def _imprimir(resultados: list[ResultadoTeste]) -> None:
        """Mostra um resumo no terminal.

        Args:
            resultados: Resultados dos testes.
        """
        resultado: ResultadoTeste
        for resultado in resultados:
            situacao: str = "OK" if resultado.sucesso else "FALHA"
            if resultado.sucesso:
                situacao += " (acertou)" if resultado.acertou else " (errou o tema)"
            print(f"[{situacao}] {resultado.provedor}:{resultado.modelo} — {', '.join(resultado.papeis)}")
            if resultado.sucesso:
                custo: str = f", US$ {resultado.custo_usd:.4f}" if resultado.custo_usd else ""
                print(
                    f"    {resultado.latencia_s:.1f}s, {resultado.tokens_entrada} tokens de entrada, "
                    f"{resultado.tokens_saida} de saída{custo}"
                )
            print(f"    {resultado.resposta[:200]}")
