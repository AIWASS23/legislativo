"""Configuração central do projeto: caminhos, parâmetros da EDA, de LLM e do portão de qualidade.

Não há argumentos de linha de comando. Para mudar um caminho ou um limiar,
altere os valores padrão das dataclasses deste módulo.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

ETAPA_ATUAL: Final[int] = 2
"""Etapa do case em vigor (ADR-018). Os anexos de cada etapa ficam em ``anexos/<etapa>-ENTREGA/``."""


@dataclass(frozen=True)
class Caminhos:
    """Caminhos de entrada e saída do projeto.

    Attributes:
        raiz: Pasta raiz do projeto.
        anexos: Pasta com os arquivos brutos recebidos no case (nunca é alterada).
        questoes: Arquivo ``questoes.jsonl``.
        temas: Arquivo ``temas.csv``.
        saida_eda: Pasta onde a EDA grava relatório, tabelas e resumo.
        saida_infra: Pasta onde a análise de infraestrutura grava perfil e recomendação.
        config: Pasta de configurações editáveis (catálogo de modelos, escolha de modelos).
        catalogo_modelos: Catálogo editável de modelos candidatos (ADR-017).
        escolha_modelos: Escolha de provedor e modelo por papel (``auto`` ou manual).
        env: Arquivo ``.env`` opcional com chaves de API (ignorado pelo git).
        dados_preparados: Pasta com as saídas do passo 01 usadas pelos passos seguintes.
        saida_preparacao: Pasta com o resumo e a conferência do passo 01.
        dados_temas: Decisões manuais sobre a árvore (lixeiras, sobreposições, correções de título)
            e cartões de tema (gerados, ajustes manuais e finais, ADR-007).
        dados_gold: Amostras, rótulos manuais e cadernos do gold set (ADR-012).
        prompts: Prompts versionados de cada papel (a versão é o hash do arquivo).
        runs: Cache de chamadas a modelos, só de acréscimo (``runs/<papel>/<data>.jsonl``, ADR-003).
        saida_custos: Resumo de custo e tempo por papel e por modelo.
        saida_cartoes: Material de revisão dos cartões e tamanhos das versões da árvore.
        dados_classificacao: Respostas e sinais por questão (ADR-008).
        saida_classificacao: Resumo agregado da classificação.
        entregaveis: Pasta do ``publicacao.csv``, do ``previsao.txt`` e do relatório (ADR-015).
        etapa: Etapa do case cujos anexos são lidos (1 ou 2, ADR-026).
        folha_verdade: ``folha_verdade.csv`` da etapa 2 (100 questões rotuladas pela equipe, ADR-024).
        dados_conhecimento: Artefatos da fase de conhecimento da etapa 2, com manifesto (ADR-019, ADR-020).
        saida_etapa2: Relatórios e experimentos da etapa 2 (E7 em diante, ADR-024).
    """

    raiz: Path
    anexos: Path
    questoes: Path
    temas: Path
    saida_eda: Path
    saida_infra: Path
    config: Path
    catalogo_modelos: Path
    escolha_modelos: Path
    env: Path
    dados_preparados: Path
    saida_preparacao: Path
    dados_temas: Path
    dados_gold: Path
    prompts: Path
    runs: Path
    saida_custos: Path
    saida_cartoes: Path
    dados_classificacao: Path
    saida_classificacao: Path
    entregaveis: Path
    etapa: int
    folha_verdade: Path
    dados_conhecimento: Path
    saida_etapa2: Path

    @classmethod
    def padrao(cls, etapa: int = ETAPA_ATUAL) -> Caminhos:
        """Monta os caminhos a partir da localização deste arquivo.

        Args:
            etapa: Etapa do case cujos anexos são lidos (padrão: a etapa em vigor).

        Returns:
            Instância com os caminhos padrão do projeto.
        """
        raiz: Path = Path(__file__).resolve().parent.parent
        anexos: Path = raiz / "anexos" / f"{etapa}-ENTREGA"
        config: Path = raiz / "config"
        return cls(
            raiz=raiz,
            anexos=anexos,
            questoes=anexos / "questoes.jsonl",
            temas=anexos / "temas.csv",
            saida_eda=raiz / "saidas" / "eda",
            saida_infra=raiz / "saidas" / "infra",
            config=config,
            catalogo_modelos=config / "catalogo_modelos.json",
            escolha_modelos=config / "escolha_modelos.json",
            env=raiz / ".env",
            dados_preparados=raiz / "dados" / "preparados",
            saida_preparacao=raiz / "saidas" / "preparacao",
            dados_temas=raiz / "dados" / "temas",
            dados_gold=raiz / "dados" / "gold",
            prompts=raiz / "prompts",
            runs=raiz / "runs",
            saida_custos=raiz / "saidas" / "custos",
            saida_cartoes=raiz / "saidas" / "cartoes",
            dados_classificacao=raiz / "dados" / "classificacao",
            saida_classificacao=raiz / "saidas" / "classificacao",
            entregaveis=raiz / "relatorio",
            etapa=etapa,
            folha_verdade=anexos / "folha_verdade.csv",
            dados_conhecimento=raiz / "dados" / "conhecimento",
            saida_etapa2=raiz / "saidas" / "etapa2",
        )


def _mapa_disciplinas_padrao() -> dict[str, str]:
    """Cria o mapa de nomes de disciplina de origem para disciplinas da árvore.

    Returns:
        Dicionário ``nome na origem -> disciplina da árvore``. Nomes ausentes
        do mapa são tratados como fora do recorte.
    """
    return {
        "Penal": "Penal",
        "Direito Penal": "Penal",
        "Processo Penal": "Processo Penal",
        "Direito Processual Penal": "Processo Penal",
        "Direito Penal - Legislação Especial": "Direito Penal - Legislação Especial",
        "Criminologia": "Criminologia",
    }


def _palavras_sem_conteudo_padrao() -> frozenset[str]:
    """Cria o conjunto de palavras ignoradas ao medir o conteúdo de um enunciado.

    Junta palavras de ligação e o vocabulário de frases-padrão de prova
    ("assinale a alternativa correta", "julgue o item" etc.). Tudo já está
    normalizado (minúsculas, sem acento).

    Returns:
        Conjunto imutável de palavras sem conteúdo temático.
    """
    ligacao: set[str] = {
        "a",
        "o",
        "as",
        "os",
        "e",
        "de",
        "da",
        "do",
        "das",
        "dos",
        "em",
        "no",
        "na",
        "nos",
        "nas",
        "um",
        "uma",
        "uns",
        "umas",
        "ao",
        "aos",
        "que",
        "se",
        "com",
        "por",
        "para",
        "pela",
        "pelo",
        "pelas",
        "pelos",
        "ou",
        "como",
        "mais",
        "menos",
        "sua",
        "seu",
        "suas",
        "seus",
        "esta",
        "este",
        "estas",
        "estes",
        "essa",
        "esse",
        "isso",
        "isto",
        "qual",
        "quais",
        "ser",
        "sao",
        "ha",
        "foi",
        "num",
        "numa",
        "dentre",
        "entre",
        "mas",
        "la",
        "lo",
        "lhe",
    }
    frases_padrao: set[str] = {
        "assinale",
        "assinalar",
        "alternativa",
        "alternativas",
        "opcao",
        "opcoes",
        "correta",
        "corretas",
        "correto",
        "corretos",
        "incorreta",
        "incorretas",
        "incorreto",
        "incorretos",
        "errada",
        "erradas",
        "errado",
        "certa",
        "certo",
        "verdadeira",
        "verdadeiras",
        "falsa",
        "falsas",
        "afirmar",
        "afirma",
        "afirmativa",
        "afirmativas",
        "afirmacao",
        "afirmacoes",
        "assertiva",
        "assertivas",
        "marque",
        "marcar",
        "analise",
        "analisar",
        "considere",
        "considerando",
        "considerar",
        "julgue",
        "julgar",
        "item",
        "itens",
        "abaixo",
        "acima",
        "seguir",
        "seguinte",
        "seguintes",
        "sobre",
        "acerca",
        "respeito",
        "tocante",
        "concerne",
        "refere",
        "relacao",
        "ponto",
        "vista",
        "legal",
        "apenas",
        "somente",
        "exceto",
        "nao",
        "todas",
        "todos",
        "nenhuma",
        "quanto",
        "conforme",
        "segundo",
        "assunto",
        "tema",
        "questao",
        "enunciado",
        "resposta",
        "indique",
        "identifique",
        "aponte",
        "proposicao",
        "proposicoes",
        "apresentado",
        "apresentada",
        "apresentados",
        "apresentadas",
        "subsequente",
        "subsequentes",
        "proximo",
        "proximos",
        "proxima",
        "proximas",
        "hipotetica",
        "hipotetico",
        "situacao",
        "caso",
        "narrado",
        "narrada",
        "contexto",
        "diante",
        "neste",
        "nesta",
        "nesse",
        "nessa",
        "deste",
        "desta",
        "desse",
        "dessa",
    }
    return frozenset(ligacao | frases_padrao)


@dataclass(frozen=True)
class ParametrosEDA:
    """Limiares e listas usados pelas heurísticas da EDA.

    Attributes:
        limiar_enunciado_curto: Enunciados limpos com menos caracteres que isto
            são marcados como curtos (só descritivo; curto não é genérico).
        max_palavras_conteudo_generico: Enunciado com até este número de
            palavras de conteúdo é considerado genérico (o assunto está nas
            alternativas).
        limiar_participacao_lixeira: Fração mínima das questões do pai
            concentradas num nó para marcá-lo como possível lixeira.
        min_questoes_lixeira: Número mínimo de questões históricas no nó para
            marcá-lo como possível lixeira.
        limiar_similaridade_canonico: Similaridade mínima entre títulos para
            casar um nó fantasma com o nó canônico.
        limiar_similaridade_digitacao: Similaridade mínima entre duas palavras
            de títulos para suspeitar de erro de digitação.
        linhas_por_tabela_md: Linhas de cada tabela exibidas no Markdown; o
            CSV correspondente sempre tem todas.
        chars_trecho: Tamanho máximo dos trechos de texto exibidos nas tabelas.
        mapa_disciplinas: Normalização dos nomes de disciplina de origem.
        palavras_sem_conteudo: Palavras ignoradas ao medir conteúdo.
        termos_comando_suspeito: Palavras que indicam um comando gerado
            artificialmente (não combinam com questão objetiva).
        termos_titulo_generico: Expressões que indicam tema introdutório ou
            genérico, candidatas a "lixeira".
        termos_jurisprudencia: Expressões que indicam questão de jurisprudência.
    """

    limiar_enunciado_curto: int = 40
    max_palavras_conteudo_generico: int = 0
    limiar_participacao_lixeira: float = 0.5
    min_questoes_lixeira: int = 60
    limiar_similaridade_canonico: float = 0.85
    limiar_similaridade_digitacao: float = 0.85
    linhas_por_tabela_md: int = 25
    chars_trecho: int = 120
    mapa_disciplinas: dict[str, str] = field(default_factory=_mapa_disciplinas_padrao)
    palavras_sem_conteudo: frozenset[str] = field(default_factory=_palavras_sem_conteudo_padrao)
    termos_comando_suspeito: tuple[str, ...] = (
        "explique",
        "complete",
        "defina",
        "descreva",
        "responda",
    )
    termos_titulo_generico: tuple[str, ...] = (
        "conceito",
        "nocoes gerais",
        "caracteristicas",
        "teoria geral",
        "introducao",
        "disposicoes gerais",
        "principios",
        "fontes",
        "classificacao",
    )
    termos_jurisprudencia: tuple[str, ...] = (
        "stf",
        "stj",
        "sumula",
        "jurisprudencia",
        "tribunais superiores",
        "supremo tribunal federal",
        "superior tribunal de justica",
        "informativo",
    )


@dataclass(frozen=True)
class ParametrosQualidade:
    """O que o portão de qualidade checa (ADR-001).

    Attributes:
        pacotes: Pacotes Python checados pelo ``mypy --strict``.
        pontos_de_entrada: Padrões ``glob`` (relativos à raiz) dos scripts de entrada,
            também checados pelo mypy.
        padroes_anotacoes: Padrões ``glob`` dos arquivos conferidos pelo verificador
            de anotações e docstrings.
    """

    pacotes: tuple[str, ...] = ("vicio_ia", "ferramentas", "testes")
    pontos_de_entrada: tuple[str, ...] = ("executar_*.py",)
    padroes_anotacoes: tuple[str, ...] = ("vicio_ia/**/*.py", "ferramentas/**/*.py", "testes/**/*.py", "executar_*.py")


def _qualidade_minima_padrao() -> dict[str, int]:
    """Cria a qualidade mínima (1 a 5) exigida de um modelo em cada papel.

    Returns:
        Dicionário ``papel -> qualidade mínima``.
    """
    return {"classificador_a": 3, "classificador_b": 3, "voto_barato": 1, "verificador": 4}


def _paralelismo_padrao() -> dict[str, int]:
    """Cria o limite de chamadas simultâneas por provedor.

    As CLIs de assinatura têm limite de uso e o Ollama tem uma GPU só; as APIs aguentam mais.

    Returns:
        Dicionário ``provedor -> chamadas simultâneas``.
    """
    return {
        "claude-cli": 3,
        "gemini-agy": 3,
        "codex-cli": 3,
        "ollama": 1,
        "claude-api": 8,
        "openai": 8,
        "huggingface": 4,
    }


@dataclass(frozen=True)
class ParametrosLLM:
    """Provedores, modelos e critérios de recomendação (ADR-017).

    A escolha de modelo por papel fica em ``config/escolha_modelos.json``
    (gerado por ``executar_escolha_modelo.py`` ou editado à mão). Sem esse arquivo,
    ou com ``"modo": "auto"``, o recomendador escolhe a partir da infraestrutura.

    Attributes:
        papeis: Papéis do ensemble (ADR-008) que recebem um modelo.
        qualidade_minima: Qualidade mínima (1 a 5) aceita em cada papel.
        contexto_necessario_tokens: Contexto que o prompt de classificação exige
            (árvore + questão + folga). Define a memória dos modelos locais.
        tokens_saida_estimados: Tokens de saída por chamada, para estimar custo.
        exige_saida_estruturada: Descarta modelos sem saída em JSON Schema.
        peso_qualidade: Peso da qualidade na pontuação de recomendação.
        peso_custo: Peso do custo na pontuação.
        peso_velocidade: Peso da velocidade na pontuação.
        max_tokens_saida: Limite de tokens de saída por chamada.
        timeout_segundos: Tempo máximo por chamada.
        ollama_url: Endereço do servidor Ollama.
        ollama_pensar: Ativa o raciocínio dos modelos locais que o suportam (mais lento).
        huggingface_url: Endpoint compatível com OpenAI do Hugging Face Inference Providers.
        claude_esforco: Esforço (``effort``) nas chamadas do provedor ``claude-api``.
        claude_cli_esforco: Esforço (``--effort``) nas chamadas do provedor ``claude-cli`` ("" = padrão da CLI).
        codex_esforco: Esforço de raciocínio (``model_reasoning_effort``) nas chamadas do provedor ``codex-cli``.
        paralelismo: Chamadas simultâneas por provedor nas rodadas em lote.
        fracao_vram_utilizavel: Fração da VRAM livre considerada utilizável.
        sobrecarga_memoria_gb: Memória extra estimada por modelo local carregado.
        bytes_cache_kv: Bytes por elemento do cache de atenção (2 = f16, padrão do Ollama).
        max_bytes_argumento_cli: Tamanho máximo de um prompt passado como argumento a uma CLI.
    """

    papeis: tuple[str, ...] = ("classificador_a", "classificador_b", "voto_barato", "verificador")
    qualidade_minima: dict[str, int] = field(default_factory=_qualidade_minima_padrao)
    contexto_necessario_tokens: int = 16384
    tokens_saida_estimados: int = 1000
    exige_saida_estruturada: bool = True
    peso_qualidade: float = 0.6
    peso_custo: float = 0.2
    peso_velocidade: float = 0.2
    max_tokens_saida: int = 4096
    timeout_segundos: int = 300
    ollama_url: str = "http://localhost:11434"
    ollama_pensar: bool = False
    huggingface_url: str = "https://router.huggingface.co/v1"
    claude_esforco: str = "low"
    claude_cli_esforco: str = "medium"
    codex_esforco: str = "medium"
    paralelismo: dict[str, int] = field(default_factory=_paralelismo_padrao)
    fracao_vram_utilizavel: float = 0.9
    sobrecarga_memoria_gb: float = 0.8
    bytes_cache_kv: int = 2
    max_bytes_argumento_cli: int = 120_000


@dataclass(frozen=True)
class ParametrosPreparacao:
    """Parâmetros do passo 01 (preparação das questões, ADR-004).

    Attributes:
        chars_por_token: Caracteres por token usados para estimar o tamanho do texto.
        ids_conferencia: Questões que sempre entram na amostra de conferência manual.
        tamanho_conferencia: Tamanho da amostra de conferência (completada com
            exemplos de formatos e tipos de comando ainda não cobertos).
    """

    chars_por_token: float = 3.5
    ids_conferencia: tuple[str, ...] = ("Q0099", "Q0008", "Q0090", "Q0122")
    tamanho_conferencia: int = 10


@dataclass(frozen=True)
class ParametrosGold:
    """Parâmetros do gold set manual cego (ADR-012).

    Attributes:
        semente: Semente do sorteio da amostra (fixa, para reprodutibilidade).
        tamanho_leva1: Questões do gold set, estratificadas por disciplina de origem normalizada e formato.
        niveis_certeza: Valores aceitos na coluna ``certeza``.
        max_resultados_busca: Temas exibidos por busca na rotulagem interativa.
        rotulo_fora_do_recorte: Estrato das questões cuja disciplina de origem não está no recorte.
    """

    semente: int = 20261015
    tamanho_leva1: int = 60
    niveis_certeza: tuple[str, ...] = ("alta", "media", "baixa")
    max_resultados_busca: int = 15
    rotulo_fora_do_recorte: str = "(fora do recorte)"


@dataclass(frozen=True)
class ParametrosCartoes:
    """Parâmetros do passo 02 (cartões de tema, ADR-007).

    Attributes:
        provedor: Provedor que gera os rascunhos. Fixo, e não o do papel verificador, para que trocar
            o verificador não invalide no cache os rascunhos já gerados (gerados em 15/10 com Opus 5.5).
        modelo: Modelo que gera os rascunhos.
        max_cartoes_por_chamada: Máximo de cartões pedidos numa chamada (blocos maiores são divididos).
        max_chars_escopo: Tamanho máximo aceito para o escopo de um cartão.
        max_tokens_saida: Limite de tokens de saída por chamada.
        limiar_similaridade_irmaos: Similaridade de títulos a partir da qual dois irmãos
            entram na revisão prioritária.
    """

    provedor: str = "claude-cli"
    modelo: str = "claude-opus-5-5"
    max_cartoes_por_chamada: int = 16
    max_chars_escopo: int = 400
    max_tokens_saida: int = 16000
    limiar_similaridade_irmaos: float = 0.5


@dataclass(frozen=True)
class ParametrosClassificacao:
    """Parâmetros dos passos 05 e 06 (classificação e verificação, ADR-008).

    Attributes:
        adiar_gold_pendente: Não classifica as questões do gold ainda sem rótulo, para o
            rótulo continuar cego (ADR-012). Elas entram numa execução depois de rotuladas.
        somente_ids: Classifica só estas questões (vazio = todas); útil no teste de fumaça.
        limite: Máximo de questões por execução (0 = sem limite).
        verificar: Roda o verificador nas candidatas a publicar.
        com_escopo_a: O classificador A recebe a árvore com escopo (``False`` = só títulos, E4).
        chars_por_token_local: Caracteres por token na estimativa do contexto do modelo local
            (conservador).
    """

    adiar_gold_pendente: bool = True
    somente_ids: tuple[str, ...] = ()
    limite: int = 0
    verificar: bool = True
    com_escopo_a: bool = True
    chars_por_token_local: float = 3.0


def _taxas_convencao_padrao() -> dict[str, float]:
    """Cria as taxas supostas de discordância de convenção por tipo de nó (ADR-013).

    Returns:
        ``tipo_convencao -> taxa``. O gold não mede esse risco; as taxas são hipóteses declaradas.
    """
    return {"duplicado_outra_disciplina": 0.20, "sobreposicao": 0.10, "duplicado_parte": 0.03}


@dataclass(frozen=True)
class ParametrosCalibracao:
    """Parâmetros da calibração, do limiar e da previsão (ADR-011, ADR-013).

    Attributes:
        penalidades_l2: Grade de penalidades L2 da regressão logística (o intercepto não é penalizado);
            a usada é a de menor log-loss na validação cruzada.
        partes_validacao: Partes da validação cruzada estratificada.
        reamostras: Reamostras do bootstrap completo.
        semente: Semente da validação cruzada e do bootstrap.
        alvo_precisao: Precisão mínima exigida das publicadas.
        percentil_limiar: Percentil do bootstrap usado como limite inferior no critério do limiar.
        reserva_pontual: Estimativa pontual mínima na regra de reserva (sem conjunto que atinja o alvo).
        percentis_intervalo: Percentis do intervalo informado no ``previsao.txt``.
        min_gold_direto: Itens do gold publicados a partir dos quais o ponto é o estimador direto.
        prior_direto: Pseudo-contagem de acertos e de erros na suavização do estimador direto (0,5 = Jeffreys, D12).
        taxas_convencao: Taxas supostas de discordância de convenção por tipo de nó.
        fatores_sensibilidade: Multiplicadores das taxas mostrados no ``previsao.txt``.
        margem_ambiguidade_no_limiar: Desconta a margem de ambiguidade do rótulo também no limiar. Desligado:
            pela ADR-011, o critério do limiar desconta só a margem de convenção; a de ambiguidade alarga o
            intervalo informado.
        total_questoes: Questões do case (denominador da cobertura).
    """

    penalidades_l2: tuple[float, ...] = (0.01, 0.03, 0.1, 0.3, 1.0, 3.0)
    partes_validacao: int = 5
    reamostras: int = 1000
    semente: int = 20261016
    alvo_precisao: float = 0.95
    percentil_limiar: float = 10.0
    reserva_pontual: float = 0.97
    percentis_intervalo: tuple[float, float] = (5.0, 95.0)
    min_gold_direto: int = 40
    prior_direto: float = 0.5
    taxas_convencao: dict[str, float] = field(default_factory=_taxas_convencao_padrao)
    fatores_sensibilidade: tuple[float, ...] = (0.0, 1.0, 2.0)
    margem_ambiguidade_no_limiar: bool = False
    total_questoes: int = 359


@dataclass(frozen=True)
class ParametrosSistema:
    """Parâmetros do sistema de classificação da etapa 2, que decide sem LLM (ADR-019 a ADR-025).

    Attributes:
        partes_validacao: Partes da validação cruzada estratificada (ADR-024).
        repeticoes_validacao: Repetições da validação cruzada; a repetição ``r`` usa a semente ``semente + r``.
        semente: Semente base da validação cruzada e dos sorteios.
        bm25_k1: Saturação da frequência do termo no BM25 (ADR-021).
        bm25_b: Peso da normalização pelo tamanho do documento no BM25.
        top_k_recall: Tamanhos de lista para o recall@k nos experimentos.
        reamostras_auc: Reamostras do bootstrap do intervalo da AUC (E11).
        variavel_sem_llm: Variável de ambiente que, com valor ``"1"``, proíbe criar provedores de LLM (ADR-019).
        questoes_etapa1: Questões da etapa 1 (Q0001 a Q0359); as demais são as novas da etapa 2 (ADR-018).
        amostra_conferencia: Citações sorteadas para a conferência do autor (ADR-021).
    """

    partes_validacao: int = 5
    repeticoes_validacao: int = 10
    semente: int = 20261020
    bm25_k1: float = 1.2
    bm25_b: float = 0.75
    top_k_recall: tuple[int, ...] = (1, 5, 10)
    reamostras_auc: int = 1000
    variavel_sem_llm: str = "VICIO_SEM_LLM"
    questoes_etapa1: int = 359
    amostra_conferencia: int = 20


@dataclass(frozen=True)
class ModeloEmbedding:
    """Um modelo de embedding candidato (ADR-021, experimento E8).

    Attributes:
        nome: Nome do modelo no provedor.
        prefixo_consulta: Prefixo das questões e alternativas (instrução de busca, quando o modelo pede).
        prefixo_documento: Prefixo dos documentos de tema.
        contexto_tokens: Janela de contexto usada (o excedente é truncado).
    """

    nome: str
    prefixo_consulta: str = ""
    prefixo_documento: str = ""
    contexto_tokens: int = 8192


def _candidatos_embedding_padrao() -> tuple[ModeloEmbedding, ...]:
    """Candidatos do E8: modelos multilíngues que rodam no Ollama local (GPU de 6 GB ou CPU).

    Returns:
        Modelos na ordem do relatório.
    """
    instrucao_qwen: str = (
        "Instruct: Given a Brazilian criminal law exam question, retrieve the syllabus topic it assesses\nQuery: "
    )
    return (
        ModeloEmbedding("bge-m3"),
        ModeloEmbedding("qwen3-embedding:0.6b", prefixo_consulta=instrucao_qwen),
        ModeloEmbedding("qwen3-embedding:4b", prefixo_consulta=instrucao_qwen),
        ModeloEmbedding("snowflake-arctic-embed2", prefixo_consulta="query: "),
        ModeloEmbedding("granite-embedding:278m", contexto_tokens=512),
    )


@dataclass(frozen=True)
class ParametrosEmbeddings:
    """Parâmetros dos embeddings da fase de conhecimento (ADR-021).

    Attributes:
        provedor: Provedor de embedding (pela camada ``vicio_ia/llm``).
        candidatos: Modelos comparados no E8.
        escolhido: Modelo exportado para ``dados/conhecimento/embeddings/`` (o vencedor do E8, 20/10).
        lote: Textos por chamada.
        timeout_segundos: Tempo máximo por lote.
        rrf_k: Constante da fusão por posição recíproca (BM25 + denso) medida no E8.
        vizinhos_knn: Vizinhos rotulados considerados no kNN do E9.
    """

    provedor: str = "ollama"
    candidatos: tuple[ModeloEmbedding, ...] = field(default_factory=_candidatos_embedding_padrao)
    escolhido: str = "qwen3-embedding:4b"
    lote: int = 32
    timeout_segundos: int = 600
    rrf_k: int = 60
    vizinhos_knn: int = 10


@dataclass(frozen=True)
class ParametrosConhecimento:
    """Parâmetros da fase de conhecimento da etapa 2 (ADR-019, ADR-020).

    Attributes:
        provedor: Provedor que propõe o mapa de artigos e os termos. Fora da cota do Claude Code (D8).
        modelo: Modelo que propõe.
        papel: Papel registrado no cache (pasta de ``runs/``).
        max_temas_por_chamada: Máximo de temas pedidos numa chamada (blocos maiores são divididos).
        max_tokens_saida: Limite de tokens de saída por chamada.
        artigo_maximo: Maior número de artigo aceito numa proposta (o CP vai até o 361; o CPP, até o 811).
        max_chars_termo: Tamanho máximo de um termo proposto.
    """

    provedor: str = "codex-cli"
    modelo: str = "gpt-6.1-sol"
    papel: str = "conhecimento"
    max_temas_por_chamada: int = 12
    max_tokens_saida: int = 16000
    artigo_maximo: int = 1000
    max_chars_termo: int = 60
