"""Orquestração da análise de infraestrutura: perfil da máquina, catálogo, recomendação e relatório."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from vicio_ia.ambiente import CarregadorAmbiente
from vicio_ia.configuracao import Caminhos, ParametrosLLM
from vicio_ia.infra.analisador import AnalisadorInfra
from vicio_ia.infra.catalogo import CatalogoModelos, ModeloCatalogado
from vicio_ia.infra.memoria import EstimadorMemoria
from vicio_ia.infra.perfil import InfoCLI, InfoGPU, PerfilMaquina
from vicio_ia.infra.recomendador import AvaliacaoModelo, Recomendacao, RecomendadorModelos
from vicio_ia.relatorio import Celula, EscritorRelatorio, Secao, Tabela


@dataclass(frozen=True)
class ResultadoInfra:
    """Perfil da máquina e recomendação de modelos.

    Attributes:
        perfil: Perfil coletado.
        recomendacao: Avaliações, papéis e sugestões.
    """

    perfil: PerfilMaquina
    recomendacao: Recomendacao


class PipelineInfra:
    """Analisa a máquina, avalia os modelos candidatos e grava o relatório em ``saidas/infra/``."""

    def __init__(self, caminhos: Caminhos | None = None, parametros: ParametrosLLM | None = None) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto (opcional, útil em testes).
            parametros: Parâmetros de LLM (opcional, útil em testes).
        """
        self._caminhos: Caminhos = caminhos if caminhos is not None else Caminhos.padrao()
        self._parametros: ParametrosLLM = parametros if parametros is not None else ParametrosLLM()

    def analisar(self) -> ResultadoInfra:
        """Coleta o perfil e calcula a recomendação, sem gravar nada.

        Returns:
            Perfil e recomendação.
        """
        ambiente: CarregadorAmbiente = CarregadorAmbiente(self._caminhos.env)
        ambiente.carregar_env()
        perfil: PerfilMaquina = AnalisadorInfra(self._parametros, ambiente).analisar()
        modelos: list[ModeloCatalogado] = CatalogoModelos(self._caminhos.catalogo_modelos).montar(perfil)
        recomendador: RecomendadorModelos = RecomendadorModelos(
            perfil, self._parametros, EstimadorMemoria(self._parametros)
        )
        return ResultadoInfra(perfil, recomendador.recomendar(modelos))

    def executar(self) -> Path:
        """Analisa, grava perfil, recomendação e relatório, e imprime um resumo.

        Returns:
            Caminho do relatório Markdown.
        """
        resultado: ResultadoInfra = self.analisar()
        escritor: EscritorRelatorio = EscritorRelatorio(self._caminhos.saida_infra, 60, nome_base="infra")
        escritor.preparar_pasta()
        perfil_json: Path = self._caminhos.saida_infra / "perfil_maquina.json"
        perfil_json.write_text(json.dumps(resultado.perfil.como_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        relatorio: Path = escritor.escrever(
            "Infraestrutura e recomendação de modelos", self._introducao(), self._secoes(resultado)
        )
        self._imprimir(resultado, relatorio)
        return relatorio

    def _introducao(self) -> list[str]:
        """Texto exibido no topo do relatório.

        Returns:
            Parágrafos.
        """
        return [
            "Retrato da máquina e avaliação dos modelos candidatos para o pipeline de classificação (ADR-017).",
            (
                f"Critério: contexto de {self._parametros.contexto_necessario_tokens:,} tokens, saída em JSON Schema, "
                f"pesos qualidade {self._parametros.peso_qualidade} / custo {self._parametros.peso_custo} / "
                f"velocidade {self._parametros.peso_velocidade}. As notas de qualidade são estimativas do catálogo "
                "(`config/catalogo_modelos.json`), a validar no experimento E6."
            ),
            (
                "Para escolher modelos: `uv run python executar_escolha_modelo.py` (interativo) ou editar "
                "`config/escolha_modelos.json`. Para gerar de novo: `uv run python executar_infra.py`."
            ),
        ]

    def _secoes(self, resultado: ResultadoInfra) -> list[Secao]:
        """Monta as seções do relatório.

        Args:
            resultado: Perfil e recomendação.

        Returns:
            Seções na ordem de exibição.
        """
        return [
            self._secao_maquina(resultado.perfil),
            self._secao_provedores(resultado.perfil),
            self._secao_papeis(resultado.recomendacao),
            self._secao_modelos(resultado.recomendacao),
        ]

    def _secao_maquina(self, perfil: PerfilMaquina) -> Secao:
        """Seção com o hardware.

        Args:
            perfil: Perfil da máquina.

        Returns:
            Seção.
        """
        gpu: InfoGPU | None = perfil.gpu_principal()
        linhas: list[list[Celula]] = [
            [
                g.nome,
                g.fabricante,
                g.tipo,
                self._gb(g.vram_total_gb),
                self._gb(g.vram_livre_gb),
                "sim" if g.usavel_para_llm else "não",
                g.observacao,
            ]
            for g in perfil.gpus
        ]
        secao: Secao = Secao("Máquina")
        secao.achados = [
            f"{perfil.sistema} ({perfil.arquitetura}); {perfil.cpu_modelo}, {perfil.cpu_threads} threads.",
            (
                f"RAM: {self._gb(perfil.ram_total_gb)} GB no total, {self._gb(perfil.ram_disponivel_gb)} GB disponíveis; "
                f"disco livre: {self._gb(perfil.disco_livre_gb)} GB."
            ),
            (
                f"GPU usada para modelos locais: {gpu.nome} com {self._gb(gpu.vram_total_gb)} GB de VRAM."
                if gpu
                else "Nenhuma GPU utilizável: modelos locais rodam na CPU."
            ),
        ]
        secao.tabelas = [
            Tabela(
                "gpus",
                "GPUs",
                ["nome", "fabricante", "tipo", "VRAM (GB)", "livre (GB)", "usada p/ LLM", "obs."],
                linhas,
            )
        ]
        secao.metricas = {
            "ram_total_gb": round(perfil.ram_total_gb or 0.0, 1),
            "vram_gb": round(gpu.vram_total_gb or 0.0, 1) if gpu else 0.0,
            "cpu_threads": perfil.cpu_threads,
        }
        return secao

    def _secao_provedores(self, perfil: PerfilMaquina) -> Secao:
        """Seção com a situação de cada provedor.

        Args:
            perfil: Perfil da máquina.

        Returns:
            Seção.
        """
        claude: InfoCLI | None = perfil.cli("claude")
        agy: InfoCLI | None = perfil.cli("agy")
        codex: InfoCLI | None = perfil.cli("codex")
        ollama_detalhe: str = (
            f"versão {perfil.ollama.versao}; {len(perfil.ollama.modelos)} modelos instalados: "
            + ", ".join(m.nome for m in perfil.ollama.modelos)
            if perfil.ollama.ativo
            else ("instalado, servidor parado" if perfil.ollama.instalado else "não instalado")
        )
        linhas: list[list[Celula]] = [
            ["ollama", "local", "pronto" if perfil.ollama.ativo else "indisponível", ollama_detalhe],
            [
                "claude-cli",
                "assinatura",
                "pronto" if claude and claude.instalado else "indisponível",
                f"claude {claude.versao}; {claude.observacao}" if claude and claude.instalado else "CLI não instalada",
            ],
            [
                "gemini-agy",
                "assinatura",
                "pronto" if agy and agy.instalado and agy.modelos else "indisponível",
                f"agy {agy.versao}; {len(agy.modelos)} modelos na conta"
                if agy and agy.instalado
                else "CLI não instalada",
            ],
            [
                "codex-cli",
                "assinatura",
                "pronto" if codex and codex.instalado else "indisponível",
                f"codex {codex.versao}; {codex.observacao}" if codex and codex.instalado else "CLI não instalada",
            ],
            self._linha_api("claude-api", "anthropic", "ANTHROPIC_API_KEY", perfil),
            self._linha_api("openai", "openai", "OPENAI_API_KEY", perfil),
            self._linha_api("huggingface", "huggingface", "HF_TOKEN", perfil),
        ]
        prontos: int = sum(1 for linha in linhas if linha[2] == "pronto")
        secao: Secao = Secao("Provedores")
        secao.achados = [
            f"{prontos} de {len(linhas)} provedores prontos para uso nesta máquina.",
            "Credenciais são lidas do ambiente ou do `.env` (ignorado pelo git); só se informa se existem.",
        ]
        secao.tabelas = [
            Tabela("provedores", "Situação dos provedores", ["provedor", "acesso", "situação", "detalhe"], linhas)
        ]
        secao.metricas = {"provedores_prontos": prontos}
        return secao

    @staticmethod
    def _linha_api(provedor: str, credencial: str, variavel: str, perfil: PerfilMaquina) -> list[Celula]:
        """Linha da tabela de provedores para um provedor de API.

        Args:
            provedor: Nome do provedor.
            credencial: Chave em ``perfil.credenciais``.
            variavel: Variável de ambiente esperada.
            perfil: Perfil da máquina.

        Returns:
            Linha da tabela.
        """
        pronto: bool = perfil.credenciais.get(credencial, False)
        return [
            provedor,
            "api",
            "pronto" if pronto else "indisponível",
            "credencial encontrada" if pronto else f"falta {variavel}",
        ]

    def _secao_papeis(self, recomendacao: Recomendacao) -> Secao:
        """Seção com o modelo sugerido para cada papel e as sugestões de melhoria.

        Args:
            recomendacao: Recomendação calculada.

        Returns:
            Seção.
        """
        linhas: list[list[Celula]] = []
        papel: str
        avaliacao: AvaliacaoModelo | None
        for papel, avaliacao in recomendacao.papeis.items():
            if avaliacao is None:
                linhas.append([papel, "—", "—", "nenhum modelo pronto atende a qualidade mínima"])
            else:
                linhas.append([papel, avaliacao.modelo.provedor, avaliacao.modelo.modelo, avaliacao.motivo])
        secao: Secao = Secao("Papéis sugeridos (escolha automática)")
        secao.achados = [
            (
                "Classificador A: melhor pontuação; B: melhor de outra família (diversidade); voto barato: maior "
                "custo + velocidade; verificador: maior qualidade."
            ),
            *[f"Para melhorar: {sugestao}" for sugestao in recomendacao.sugestoes],
        ]
        secao.tabelas = [
            Tabela("papeis", "Modelo sugerido por papel", ["papel", "provedor", "modelo", "por quê"], linhas)
        ]
        secao.metricas = {
            papel: f"{a.modelo.provedor}:{a.modelo.modelo}" if a else "" for papel, a in recomendacao.papeis.items()
        }
        return secao

    def _secao_modelos(self, recomendacao: Recomendacao) -> Secao:
        """Seção com todos os modelos avaliados.

        Args:
            recomendacao: Recomendação calculada.

        Returns:
            Seção.
        """
        linhas: list[list[Celula]] = [
            [
                posicao,
                a.modelo.provedor,
                a.modelo.modelo,
                "sim" if a.pronto else ("viável" if a.viavel else "não"),
                a.execucao or "—",
                a.nota_qualidade,
                a.nota_custo,
                a.nota_velocidade,
                a.pontuacao,
                self._gb(a.memoria.total_gb) if a.memoria else "",
                f"{a.contexto_max_gpu:,}" if a.contexto_max_gpu is not None else "",
                f"{a.custo_por_chamada_usd:.4f}" if a.custo_por_chamada_usd is not None else "",
                a.motivo,
            ]
            for posicao, a in enumerate(recomendacao.avaliacoes, start=1)
        ]
        prontos: int = sum(1 for a in recomendacao.avaliacoes if a.pronto)
        viaveis: int = sum(1 for a in recomendacao.avaliacoes if a.viavel)
        secao: Secao = Secao("Modelos avaliados")
        secao.achados = [
            f"{len(recomendacao.avaliacoes)} modelos avaliados: {prontos} prontos, {viaveis} viáveis nesta máquina.",
            "Pronto = viável e utilizável agora; viável = cabe na máquina, mas falta baixar o modelo ou configurar credencial.",
        ]
        secao.tabelas = [
            Tabela(
                "modelos",
                "Ranking (prontos primeiro)",
                [
                    "#",
                    "provedor",
                    "modelo",
                    "pronto",
                    "execução",
                    "qualidade",
                    "custo",
                    "velocidade",
                    "pontuação",
                    "memória (GB)",
                    "contexto máx. na GPU",
                    "US$/chamada",
                    "motivo",
                ],
                linhas,
            )
        ]
        secao.metricas = {"modelos_avaliados": len(recomendacao.avaliacoes), "prontos": prontos, "viaveis": viaveis}
        return secao

    @staticmethod
    def _gb(valor: float | None) -> str:
        """Formata um valor em GB.

        Args:
            valor: Valor em GB.

        Returns:
            Texto com uma casa decimal, ou ``"?"``.
        """
        return f"{valor:.1f}" if valor is not None else "?"

    def _imprimir(self, resultado: ResultadoInfra, relatorio: Path) -> None:
        """Mostra um resumo no terminal.

        Args:
            resultado: Perfil e recomendação.
            relatorio: Caminho do relatório.
        """
        perfil: PerfilMaquina = resultado.perfil
        gpu: InfoGPU | None = perfil.gpu_principal()
        print(f"Máquina: {perfil.cpu_modelo} | RAM {self._gb(perfil.ram_total_gb)} GB", end="")
        print(f" | GPU {gpu.nome} {self._gb(gpu.vram_total_gb)} GB" if gpu else " | sem GPU utilizável")
        print("Papéis sugeridos:")
        papel: str
        avaliacao: AvaliacaoModelo | None
        for papel, avaliacao in resultado.recomendacao.papeis.items():
            escolha: str = f"{avaliacao.modelo.provedor}:{avaliacao.modelo.modelo}" if avaliacao else "(nenhum)"
            print(f"  {papel:16} {escolha}")
        print(f"Relatório: {relatorio}")
