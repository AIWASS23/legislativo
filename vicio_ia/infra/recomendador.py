"""Avaliação dos modelos candidatos na máquina e sugestão de um modelo por papel do ensemble."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

from vicio_ia.configuracao import ParametrosLLM
from vicio_ia.infra.catalogo import ModeloCatalogado
from vicio_ia.infra.memoria import EstimadorMemoria, EstimativaMemoria
from vicio_ia.infra.perfil import InfoCLI, InfoGPU, PerfilMaquina

type Execucao = Literal["gpu", "gpu_parcial", "cpu", "api", "assinatura"]
"""Onde o modelo roda: GPU inteira, GPU + CPU, só CPU, API paga ou CLI de assinatura."""


@dataclass(frozen=True)
class AvaliacaoModelo:
    """Avaliação de um modelo candidato nesta máquina.

    Attributes:
        modelo: Modelo avaliado.
        viavel: Roda nesta máquina (cabe na memória, contexto e saída estruturada atendidos).
        pronto: Pode ser usado agora (viável, instalado e com credencial ou CLI disponível).
        execucao: Onde roda.
        memoria: Estimativa de memória (só modelos locais).
        contexto_max_gpu: Maior contexto que cabe inteiro na GPU (só modelos locais).
        custo_por_chamada_usd: Custo estimado de uma chamada (só API com preço conhecido).
        nota_qualidade: 1 a 5.
        nota_custo: 1 a 5 (5 = mais barato).
        nota_velocidade: 1 a 5 (5 = mais rápido).
        pontuacao: Média ponderada das notas.
        motivo: Por que é inviável, o que falta para ficar pronto, ou o resumo da execução.
    """

    modelo: ModeloCatalogado
    viavel: bool
    pronto: bool
    execucao: Execucao | None
    memoria: EstimativaMemoria | None
    contexto_max_gpu: int | None
    custo_por_chamada_usd: float | None
    nota_qualidade: int
    nota_custo: int
    nota_velocidade: int
    pontuacao: float
    motivo: str


@dataclass(frozen=True)
class Recomendacao:
    """Resultado da recomendação.

    Attributes:
        avaliacoes: Todas as avaliações, prontas primeiro, depois por pontuação.
        papeis: Modelo sugerido para cada papel (``None`` se nenhum atende).
        sugestoes: O que mudar na máquina ou nas credenciais para ter opções melhores.
    """

    avaliacoes: tuple[AvaliacaoModelo, ...]
    papeis: dict[str, AvaliacaoModelo | None]
    sugestoes: tuple[str, ...]


class RecomendadorModelos:
    """Avalia modelos contra o perfil da máquina e sugere um modelo por papel.

    Regras dos papéis (ADR-008, ADR-017):

    * ``classificador_a``: melhor pontuação entre os prontos;
    * ``classificador_b``: melhor de **outra família** que o A (diversidade do ensemble);
    * ``voto_barato``: o mais barato (local antes de assinatura e API), depois o mais rápido,
      depois o de maior qualidade; de preferência diferente de A e B;
    * ``verificador``: maior qualidade entre os prontos.
    """

    def __init__(self, perfil: PerfilMaquina, parametros: ParametrosLLM, estimador: EstimadorMemoria) -> None:
        """Recebe as dependências.

        Args:
            perfil: Perfil da máquina.
            parametros: Critérios de recomendação.
            estimador: Estimador de memória de modelos locais.
        """
        self._perfil: PerfilMaquina = perfil
        self._parametros: ParametrosLLM = parametros
        self._estimador: EstimadorMemoria = estimador

    def recomendar(self, modelos: list[ModeloCatalogado]) -> Recomendacao:
        """Avalia todos os modelos e escolhe um por papel.

        Args:
            modelos: Candidatos do catálogo.

        Returns:
            Avaliações ordenadas, papéis e sugestões.
        """
        avaliacoes: list[AvaliacaoModelo] = [self.avaliar(modelo) for modelo in modelos]
        avaliacoes.sort(key=lambda a: (not a.pronto, not a.viavel, -a.pontuacao, a.modelo.chave))
        return Recomendacao(tuple(avaliacoes), self._papeis(avaliacoes), self._sugestoes(avaliacoes))

    def avaliar(self, modelo: ModeloCatalogado) -> AvaliacaoModelo:
        """Avalia um modelo nesta máquina; modelos inadequados à tarefa nunca ficam prontos.

        Args:
            modelo: Modelo candidato.

        Returns:
            Avaliação com viabilidade, prontidão, notas e motivo.
        """
        avaliacao: AvaliacaoModelo = self._avaliar_base(modelo)
        if modelo.inadequado:
            return replace(avaliacao, pronto=False, motivo=f"inadequado: {modelo.observacao}; {avaliacao.motivo}")
        return avaliacao

    def _avaliar_base(self, modelo: ModeloCatalogado) -> AvaliacaoModelo:
        """Avalia memória, contexto, saída estruturada e credenciais de um modelo.

        Args:
            modelo: Modelo candidato.

        Returns:
            Avaliação.
        """
        necessario: int = self._parametros.contexto_necessario_tokens
        if self._parametros.exige_saida_estruturada and not modelo.saida_estruturada:
            return self._inviavel(modelo, "não suporta saída estruturada (JSON Schema)")
        if modelo.contexto_max is not None and modelo.contexto_max < necessario:
            return self._inviavel(modelo, f"contexto máximo {modelo.contexto_max:,} < necessário {necessario:,}")
        if modelo.acesso == "local":
            return self._avaliar_local(modelo)
        pronto: bool
        motivo: str
        pronto, motivo = self._prontidao_remota(modelo)
        execucao: Execucao = "api" if modelo.acesso == "api" else "assinatura"
        custo: float | None = self._custo_por_chamada(modelo)
        return self._montar(modelo, True, pronto, execucao, None, None, custo, motivo)

    def _avaliar_local(self, modelo: ModeloCatalogado) -> AvaliacaoModelo:
        """Avalia um modelo do Ollama: memória, GPU, instalação e servidor.

        Args:
            modelo: Modelo local.

        Returns:
            Avaliação.
        """
        estimativa: EstimativaMemoria = self._estimador.estimar(modelo, self._parametros.contexto_necessario_tokens)
        gpu: InfoGPU | None = self._perfil.gpu_principal()
        vram: float = self._vram_utilizavel(gpu)
        ram: float = self._perfil.ram_disponivel_gb or (self._perfil.ram_total_gb or 0.0) * 0.5
        contexto_gpu: int | None = self._estimador.contexto_que_cabe(modelo, vram) if gpu else None
        execucao: Execucao
        if gpu and estimativa.total_gb <= vram:
            execucao = "gpu"
        elif gpu and estimativa.total_gb <= vram + ram:
            execucao = "gpu_parcial"
        elif not gpu and estimativa.total_gb <= ram:
            execucao = "cpu"
        else:
            return self._inviavel(
                modelo,
                f"precisa ~{estimativa.total_gb:.1f} GB com {self._parametros.contexto_necessario_tokens:,} tokens; "
                f"há ~{vram:.1f} GB de VRAM e ~{ram:.1f} GB de RAM livres",
                estimativa,
            )
        resumo: str = self._resumo_local(execucao, estimativa, contexto_gpu)
        if not self._perfil.ollama.ativo:
            motivo: str = "Ollama instalado mas parado" if self._perfil.ollama.instalado else "Ollama não instalado"
            return self._montar(modelo, True, False, execucao, estimativa, contexto_gpu, None, f"{motivo}; {resumo}")
        if not modelo.instalado:
            espaco: float = self._perfil.disco_livre_gb or 0.0
            if modelo.tamanho_gb and modelo.tamanho_gb > espaco:
                return self._inviavel(
                    modelo, f"precisa {modelo.tamanho_gb:.1f} GB em disco; há {espaco:.1f} GB", estimativa
                )
            baixar: str = f"baixar com `ollama pull {modelo.modelo}` ({modelo.tamanho_gb or 0:.1f} GB)"
            return self._montar(modelo, True, False, execucao, estimativa, contexto_gpu, None, f"{baixar}; {resumo}")
        return self._montar(modelo, True, True, execucao, estimativa, contexto_gpu, None, resumo)

    def _vram_utilizavel(self, gpu: InfoGPU | None) -> float:
        """Calcula a VRAM que o modelo pode usar.

        Args:
            gpu: GPU principal.

        Returns:
            VRAM utilizável em GB (0 sem GPU). GPU unificada usa 75% da RAM total.
        """
        if gpu is None:
            return 0.0
        if gpu.tipo == "unificada":
            return (gpu.vram_total_gb or 0.0) * 0.75
        base: float = gpu.vram_livre_gb if gpu.vram_livre_gb is not None else gpu.vram_total_gb or 0.0
        return base * self._parametros.fracao_vram_utilizavel

    def _resumo_local(self, execucao: Execucao, estimativa: EstimativaMemoria, contexto_gpu: int | None) -> str:
        """Descreve como o modelo local roda.

        Args:
            execucao: Onde roda.
            estimativa: Memória estimada.
            contexto_gpu: Maior contexto que cabe na GPU.

        Returns:
            Frase curta.
        """
        onde: dict[Execucao, str] = {
            "gpu": "inteiro na GPU",
            "gpu_parcial": "dividido entre GPU e CPU (mais lento)",
            "cpu": "só na CPU (lento)",
            "api": "",
            "assinatura": "",
        }
        texto: str = f"roda {onde[execucao]}; ~{estimativa.total_gb:.1f} GB"
        if contexto_gpu == 0:
            texto += "; os pesos não cabem inteiros na GPU"
        elif contexto_gpu is not None:
            texto += f"; cabe inteiro na GPU até ~{contexto_gpu:,} tokens"
        if estimativa.conservadora:
            texto += " (estimativa conservadora)"
        return texto

    def _prontidao_remota(self, modelo: ModeloCatalogado) -> tuple[bool, str]:
        """Verifica credencial ou CLI de um modelo remoto; modelos "a confirmar" não ficam prontos.

        Args:
            modelo: Modelo de API ou assinatura.

        Returns:
            ``(pronto, motivo)``.
        """
        pronto_base: bool
        motivo_base: str
        pronto_base, motivo_base = self._credencial_remota(modelo)
        if pronto_base and modelo.verificar:
            return False, (
                f"{motivo_base}; nome/disponibilidade a confirmar "
                "(teste com executar_teste_llm.py e marque verificar=false no catálogo)"
            )
        return pronto_base, motivo_base

    def _credencial_remota(self, modelo: ModeloCatalogado) -> tuple[bool, str]:
        """Verifica a credencial (API) ou a CLI (assinatura) de um modelo remoto.

        Args:
            modelo: Modelo de API ou assinatura.

        Returns:
            ``(tem credencial ou CLI, motivo)``.
        """
        credenciais: dict[str, bool] = self._perfil.credenciais
        if modelo.provedor == "claude-api":
            pronto: bool = credenciais.get("anthropic", False)
            return pronto, "API Anthropic" if pronto else "falta ANTHROPIC_API_KEY (ou `ant auth login`)"
        if modelo.provedor == "openai":
            pronto = credenciais.get("openai", False)
            return pronto, "API OpenAI" if pronto else "falta OPENAI_API_KEY"
        if modelo.provedor == "huggingface":
            pronto = credenciais.get("huggingface", False)
            return pronto, "Inference Providers (HF)" if pronto else "falta HF_TOKEN (ou `hf auth login`)"
        nome_cli: str = "claude" if modelo.provedor == "claude-cli" else "agy"
        cli: InfoCLI | None = self._perfil.cli(nome_cli)
        if cli is None or not cli.instalado:
            return False, f"CLI `{nome_cli}` não instalada"
        return True, f"assinatura via CLI `{nome_cli}` {cli.versao}".strip()

    def _custo_por_chamada(self, modelo: ModeloCatalogado) -> float | None:
        """Estima o custo de uma chamada de classificação.

        Args:
            modelo: Modelo de API.

        Returns:
            Custo em USD, ou ``None`` se o preço for desconhecido ou não se aplicar.
        """
        if modelo.preco_entrada is None or modelo.preco_saida is None:
            return None
        entrada: float = modelo.preco_entrada * self._parametros.contexto_necessario_tokens
        saida: float = modelo.preco_saida * self._parametros.tokens_saida_estimados
        return (entrada + saida) / 1e6

    def _notas(self, modelo: ModeloCatalogado, execucao: Execucao | None, custo: float | None) -> tuple[int, int]:
        """Calcula as notas de custo e velocidade.

        Args:
            modelo: Modelo avaliado.
            execucao: Onde roda.
            custo: Custo por chamada (API).

        Returns:
            ``(nota_custo, nota_velocidade)``, de 1 a 5.
        """
        velocidade: dict[Execucao, int] = {"gpu": 4, "gpu_parcial": 2, "cpu": 1, "api": 4, "assinatura": 3}
        nota_velocidade: int = velocidade[execucao] if execucao else 1
        if execucao == "gpu" and (modelo.parametros_b or 0) > 9:
            nota_velocidade = 3
        nota_velocidade = max(1, min(5, nota_velocidade + modelo.ajuste_velocidade))
        if modelo.acesso == "local":
            return 5, nota_velocidade
        if modelo.acesso == "assinatura":
            return 4, nota_velocidade
        if custo is None:
            return 3, nota_velocidade
        limites: tuple[tuple[float, int], ...] = ((0.005, 5), (0.02, 4), (0.05, 3), (0.1, 2))
        limite: float
        nota: int
        for limite, nota in limites:
            if custo < limite:
                return nota, nota_velocidade
        return 1, nota_velocidade

    def _montar(
        self,
        modelo: ModeloCatalogado,
        viavel: bool,
        pronto: bool,
        execucao: Execucao | None,
        memoria: EstimativaMemoria | None,
        contexto_gpu: int | None,
        custo: float | None,
        motivo: str,
    ) -> AvaliacaoModelo:
        """Monta a avaliação calculando notas e pontuação.

        Args:
            modelo: Modelo avaliado.
            viavel: Roda nesta máquina.
            pronto: Pode ser usado agora.
            execucao: Onde roda.
            memoria: Estimativa de memória.
            contexto_gpu: Maior contexto que cabe na GPU.
            custo: Custo por chamada.
            motivo: Explicação.

        Returns:
            Avaliação completa.
        """
        nota_custo: int
        nota_velocidade: int
        nota_custo, nota_velocidade = self._notas(modelo, execucao, custo)
        pontuacao: float = (
            self._parametros.peso_qualidade * modelo.qualidade
            + self._parametros.peso_custo * nota_custo
            + self._parametros.peso_velocidade * nota_velocidade
        )
        return AvaliacaoModelo(
            modelo=modelo,
            viavel=viavel,
            pronto=pronto,
            execucao=execucao,
            memoria=memoria,
            contexto_max_gpu=contexto_gpu,
            custo_por_chamada_usd=custo,
            nota_qualidade=modelo.qualidade,
            nota_custo=nota_custo,
            nota_velocidade=nota_velocidade,
            pontuacao=round(pontuacao if viavel else 0.0, 2),
            motivo=motivo,
        )

    def _inviavel(
        self, modelo: ModeloCatalogado, motivo: str, memoria: EstimativaMemoria | None = None
    ) -> AvaliacaoModelo:
        """Monta a avaliação de um modelo que não roda nesta máquina.

        Args:
            modelo: Modelo avaliado.
            motivo: Por que não roda.
            memoria: Estimativa de memória, se calculada.

        Returns:
            Avaliação com ``viavel=False``.
        """
        return self._montar(modelo, False, False, None, memoria, None, None, motivo)

    def _papeis(self, avaliacoes: list[AvaliacaoModelo]) -> dict[str, AvaliacaoModelo | None]:
        """Escolhe um modelo pronto para cada papel.

        Args:
            avaliacoes: Avaliações ordenadas.

        Returns:
            ``papel -> avaliação`` (``None`` se nenhum modelo pronto atende a qualidade mínima).
        """
        prontas: list[AvaliacaoModelo] = [a for a in avaliacoes if a.pronto]
        minimo: dict[str, int] = self._parametros.qualidade_minima

        def aptas(papel: str) -> list[AvaliacaoModelo]:
            """Filtra as avaliações prontas que atendem a qualidade mínima do papel."""
            return [a for a in prontas if a.nota_qualidade >= minimo.get(papel, 1)]

        papeis: dict[str, AvaliacaoModelo | None] = {}
        candidatas_a: list[AvaliacaoModelo] = aptas("classificador_a")
        escolha_a: AvaliacaoModelo | None = candidatas_a[0] if candidatas_a else None
        candidatas_b: list[AvaliacaoModelo] = [a for a in aptas("classificador_b") if a is not escolha_a]
        outra_familia: list[AvaliacaoModelo] = [
            a for a in candidatas_b if escolha_a is None or a.modelo.familia != escolha_a.modelo.familia
        ]
        escolha_b: AvaliacaoModelo | None = self._primeira([outra_familia, candidatas_b])
        baratas: list[AvaliacaoModelo] = sorted(
            aptas("voto_barato"), key=lambda a: (-a.nota_custo, -a.nota_velocidade, -a.nota_qualidade, -a.pontuacao)
        )
        diferentes: list[AvaliacaoModelo] = [a for a in baratas if a is not escolha_a and a is not escolha_b]
        escolha_voto: AvaliacaoModelo | None = self._primeira([diferentes, baratas])
        verificadoras: list[AvaliacaoModelo] = sorted(
            aptas("verificador"), key=lambda a: (-a.nota_qualidade, -a.pontuacao)
        )
        papeis["classificador_a"] = escolha_a
        papeis["classificador_b"] = escolha_b
        papeis["voto_barato"] = escolha_voto
        papeis["verificador"] = self._primeira([verificadoras])
        return {papel: papeis.get(papel) for papel in self._parametros.papeis}

    @staticmethod
    def _primeira(listas: list[list[AvaliacaoModelo]]) -> AvaliacaoModelo | None:
        """Devolve o primeiro item da primeira lista não vazia.

        Args:
            listas: Listas em ordem de preferência.

        Returns:
            A avaliação, ou ``None`` se todas estiverem vazias.
        """
        lista: list[AvaliacaoModelo]
        for lista in listas:
            if lista:
                return lista[0]
        return None

    def _sugestoes(self, avaliacoes: list[AvaliacaoModelo]) -> tuple[str, ...]:
        """Sugere mudanças que liberariam opções melhores.

        Args:
            avaliacoes: Avaliações ordenadas.

        Returns:
            Até seis sugestões, da mais para a menos valiosa.
        """
        melhor_pronta: int = max((a.nota_qualidade for a in avaliacoes if a.pronto), default=0)
        sugestoes: list[str] = []
        vistos: set[str] = set()
        avaliacao: AvaliacaoModelo
        for avaliacao in sorted(avaliacoes, key=lambda a: (-a.nota_qualidade, -a.pontuacao)):
            if avaliacao.pronto or not avaliacao.viavel or avaliacao.nota_qualidade <= melhor_pronta:
                continue
            if avaliacao.motivo in vistos:
                continue
            vistos.add(avaliacao.motivo)
            sugestoes.append(
                f"{avaliacao.modelo.chave} (qualidade {avaliacao.nota_qualidade}): {avaliacao.motivo.split(';')[0]}"
            )
        locais_gpu: list[AvaliacaoModelo] = [
            a for a in avaliacoes if a.modelo.acesso == "local" and not a.modelo.instalado and a.execucao == "gpu"
        ]
        if locais_gpu:
            melhor_local: AvaliacaoModelo = max(locais_gpu, key=lambda a: (a.nota_qualidade, a.pontuacao))
            sugestoes.append(
                f"Melhor modelo local que roda inteiro na GPU: {melhor_local.modelo.modelo} "
                f"({melhor_local.motivo.split(';')[0]})"
            )
        return tuple(sugestoes[:6])
