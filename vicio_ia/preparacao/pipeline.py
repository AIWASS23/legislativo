"""Orquestração do passo 01: prepara as questões e grava as saídas para os passos seguintes."""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Sequence
from pathlib import Path
from typing import TextIO

from vicio_ia.carregamento import CarregadorDados
from vicio_ia.configuracao import Caminhos, ParametrosEDA, ParametrosPreparacao
from vicio_ia.conhecimento import MapaLegislacao
from vicio_ia.dominio import Questao
from vicio_ia.eda.estatisticas import CalculadoraEstatisticas, ResumoNumerico
from vicio_ia.eda.perfil_questoes import PerfiladorQuestoes
from vicio_ia.preparacao.texto_canonico import MontadorTextoCanonico, QuestaoPreparada
from vicio_ia.preparacao.validacao import ResultadoChecagem, ValidadorQuestoesPreparadas
from vicio_ia.relatorio import Celula, EscritorRelatorio, Secao, Tabela
from vicio_ia.texto import ProcessadorTexto


class ErroPreparacao(Exception):
    """Alguma checagem do passo 01 falhou."""


class PipelinePreparacao:
    """Prepara as questões (ADR-004) e grava ``dados/preparados/questoes.jsonl``.

    Saídas:

    * ``dados/preparados/questoes.jsonl``: uma questão preparada por linha (texto canônico,
      campos limpos, marcas, hash e campos originais);
    * ``saidas/preparacao/relatorio_preparacao.md`` e ``resumo_preparacao.json``: números e checagens;
    * ``saidas/preparacao/conferencia_texto_canonico.md``: amostra para conferência manual.
    """

    def __init__(
        self,
        caminhos: Caminhos | None = None,
        parametros: ParametrosPreparacao | None = None,
        parametros_eda: ParametrosEDA | None = None,
    ) -> None:
        """Define a configuração; sem parâmetros, usa os padrões do projeto.

        Args:
            caminhos: Caminhos do projeto (opcional).
            parametros: Parâmetros do passo 01 (opcional).
            parametros_eda: Parâmetros de perfil das questões (opcional).
        """
        self._caminhos: Caminhos = caminhos if caminhos is not None else Caminhos.padrao()
        self._parametros: ParametrosPreparacao = parametros if parametros is not None else ParametrosPreparacao()
        self._parametros_eda: ParametrosEDA = parametros_eda if parametros_eda is not None else ParametrosEDA()

    def executar(self) -> Path:
        """Prepara, valida e grava as questões.

        Returns:
            Caminho de ``questoes.jsonl``.

        Raises:
            ErroPreparacao: Se alguma checagem falhar (nada é gravado em ``dados/``).
        """
        carregador: CarregadorDados = CarregadorDados(self._caminhos)
        questoes: list[Questao] = carregador.para_questoes(carregador.ler_questoes_brutas())
        processador: ProcessadorTexto = ProcessadorTexto()
        perfilador: PerfiladorQuestoes = PerfiladorQuestoes(
            self._parametros_eda, processador, MapaLegislacao(processador)
        )
        montador: MontadorTextoCanonico = MontadorTextoCanonico(
            perfilador, processador, self._parametros_eda, self._parametros
        )
        preparadas: list[QuestaoPreparada] = self._preparar(questoes, montador)
        checagens: list[ResultadoChecagem] = ValidadorQuestoesPreparadas(montador).validar(questoes, preparadas)
        escritor: EscritorRelatorio = EscritorRelatorio(self._caminhos.saida_preparacao, 30, nome_base="preparacao")
        escritor.preparar_pasta()
        escritor.escrever("Passo 01: questões preparadas", self._introducao(), self._secoes(preparadas, checagens))
        conferencia: Path = self._escrever_conferencia(preparadas)
        falhas: list[ResultadoChecagem] = [checagem for checagem in checagens if not checagem.aprovada]
        if falhas:
            detalhes: str = "; ".join(f"{f.regra}: {', '.join(f.violacoes)}" for f in falhas)
            raise ErroPreparacao(f"checagens reprovadas: {detalhes}")
        destino: Path = self._gravar(preparadas)
        self._imprimir(preparadas, checagens, destino, conferencia)
        return destino

    @staticmethod
    def _preparar(questoes: Sequence[Questao], montador: MontadorTextoCanonico) -> list[QuestaoPreparada]:
        """Prepara as questões, apontando duplicatas pelo texto completo.

        Args:
            questoes: Questões originais.
            montador: Montador do texto canônico.

        Returns:
            Questões preparadas, na ordem original.
        """
        primeira_por_hash: dict[str, str] = {}
        preparadas: list[QuestaoPreparada] = []
        questao: Questao
        for questao in questoes:
            preparada: QuestaoPreparada = montador.preparar(questao, None)
            original: str | None = primeira_por_hash.get(preparada.hash_completo)
            if original is None:
                primeira_por_hash[preparada.hash_completo] = questao.id
            else:
                preparada = montador.preparar(questao, original)
            preparadas.append(preparada)
        return preparadas

    def _gravar(self, preparadas: Sequence[QuestaoPreparada]) -> Path:
        """Grava ``dados/preparados/questoes.jsonl``.

        Args:
            preparadas: Questões preparadas.

        Returns:
            Caminho do arquivo.
        """
        self._caminhos.dados_preparados.mkdir(parents=True, exist_ok=True)
        destino: Path = self._caminhos.dados_preparados / "questoes.jsonl"
        arquivo: TextIO
        with destino.open("w", encoding="utf-8") as arquivo:
            preparada: QuestaoPreparada
            for preparada in preparadas:
                arquivo.write(json.dumps(preparada.como_dict(), ensure_ascii=False) + "\n")
        return destino

    @staticmethod
    def _introducao() -> list[str]:
        """Texto do topo do relatório.

        Returns:
            Parágrafos.
        """
        return [
            (
                "Questões convertidas no texto canônico da ADR-004: HTML limpo (inclusive o lixo colado do Word), "
                "alternativas sempre incluídas (exceto em certo/errado), comando só quando útil e com conteúdo, "
                "e nenhum rótulo de origem no texto (ADR-006)."
            ),
            (
                "Saída para os próximos passos: `dados/preparados/questoes.jsonl`. "
                "Amostra para conferência manual: `conferencia_texto_canonico.md`. "
                "Para gerar de novo: `uv run python executar_preparacao.py`."
            ),
        ]

    def _secoes(self, preparadas: Sequence[QuestaoPreparada], checagens: Sequence[ResultadoChecagem]) -> list[Secao]:
        """Monta as seções do relatório.

        Args:
            preparadas: Questões preparadas.
            checagens: Resultado das checagens.

        Returns:
            Seções na ordem de exibição.
        """
        total: int = len(preparadas)
        estatisticas: CalculadoraEstatisticas = CalculadoraEstatisticas()

        formatos: Counter[str] = Counter(p.formato for p in preparadas)
        secao_formatos: Secao = Secao("Formatos")
        secao_formatos.achados = [f"{total} questões preparadas."]
        secao_formatos.tabelas = [
            Tabela(
                "formatos",
                "Questões por formato",
                ["formato", "questões", "%"],
                [[nome, n, estatisticas.percentual(n, total)] for nome, n in formatos.most_common()],
            )
        ]
        secao_formatos.metricas = {"questoes": total, **{nome: n for nome, n in formatos.items()}}

        motivos: Counter[str] = Counter(p.motivo_comando for p in preparadas)
        secao_comando: Secao = Secao("Comando no texto canônico")
        secao_comando.achados = [
            f"O comando entrou em {motivos['incluido']} questões ({estatisticas.percentual(motivos['incluido'], total)}%).",
            (
                f"Ficou de fora em {total - motivos['incluido']}: vazio ({motivos['vazio']}), suspeito de ter sido gerado "
                f"({motivos['suspeito']}), repete o enunciado ({motivos['repete_enunciado']}) ou só frase-padrão como "
                f"'Julgue o item a seguir' ({motivos['so_frase_padrao']})."
            ),
        ]
        secao_comando.tabelas = [
            Tabela(
                "motivo_comando",
                "Destino do comando",
                ["motivo", "questões", "%"],
                [[nome, n, estatisticas.percentual(n, total)] for nome, n in motivos.most_common()],
            )
        ]
        secao_comando.metricas = {f"comando_{nome}": n for nome, n in motivos.items()}

        tokens: ResumoNumerico = estatisticas.resumir([float(p.tokens_estimados) for p in preparadas])
        caracteres: ResumoNumerico = estatisticas.resumir([float(p.caracteres) for p in preparadas])
        soma_tokens: int = sum(p.tokens_estimados for p in preparadas)
        maiores: list[QuestaoPreparada] = sorted(preparadas, key=lambda p: p.tokens_estimados, reverse=True)[:10]
        secao_tamanho: Secao = Secao("Tamanho do texto canônico")
        secao_tamanho.achados = [
            (
                f"Mediana de {tokens.mediana:.0f} tokens por questão (estimativa: {self._parametros.chars_por_token} "
                f"caracteres por token); máximo de {tokens.maximo:.0f}; {self._milhar(soma_tokens)} tokens no total."
            ),
            "A questão vai na parte variável do prompt; a árvore de temas é a parte fixa (ADR-007, ADR-008).",
        ]
        secao_tamanho.tabelas = [
            Tabela(
                "tamanho",
                "Distribuição de tamanho",
                list(CalculadoraEstatisticas.COLUNAS_RESUMO),
                [tokens.como_linha("tokens estimados"), caracteres.como_linha("caracteres")],
            ),
            Tabela(
                "maiores",
                "Questões mais longas",
                ["id", "formato", "tokens estimados", "caracteres"],
                [[p.id, p.formato, p.tokens_estimados, p.caracteres] for p in maiores],
            ),
        ]
        secao_tamanho.metricas = {
            "tokens_total": soma_tokens,
            "tokens_mediana": tokens.mediana,
            "tokens_max": tokens.maximo,
        }

        marcas: dict[str, int] = {
            "enunciado genérico": sum(1 for p in preparadas if p.marcas.enunciado_generico),
            "HTML colado do Word no original": sum(1 for p in preparadas if p.marcas.html_de_editor),
            "cita alguma lei": sum(1 for p in preparadas if p.marcas.leis_citadas),
            "cita jurisprudência": sum(1 for p in preparadas if p.marcas.menciona_jurisprudencia),
            "duplicata de outra questão (texto completo)": sum(1 for p in preparadas if p.duplicata_de),
        }
        secao_marcas: Secao = Secao("Marcas guardadas para decisão e calibração")
        secao_marcas.achados = ["As marcas acompanham a questão em `questoes.jsonl` (ADR-011, ADR-013)."]
        secao_marcas.tabelas = [
            Tabela(
                "marcas",
                "Questões por marca",
                ["marca", "questões", "%"],
                [[nome, n, estatisticas.percentual(n, total)] for nome, n in marcas.items()],
            )
        ]
        secao_marcas.metricas = {nome: n for nome, n in marcas.items()}

        linhas_checagem: list[list[Celula]] = [
            [c.regra, "aprovada" if c.aprovada else "REPROVADA", ", ".join(c.violacoes)] for c in checagens
        ]
        aprovadas: int = sum(1 for c in checagens if c.aprovada)
        secao_checagens: Secao = Secao("Checagens automáticas")
        secao_checagens.achados = [f"{aprovadas} de {len(checagens)} checagens aprovadas."]
        secao_checagens.tabelas = [
            Tabela("checagens", "Regras verificadas", ["regra", "resultado", "violações"], linhas_checagem)
        ]
        secao_checagens.metricas = {"checagens_aprovadas": aprovadas, "checagens": len(checagens)}
        return [secao_formatos, secao_comando, secao_tamanho, secao_marcas, secao_checagens]

    @staticmethod
    def _milhar(valor: int) -> str:
        """Formata um inteiro com ponto como separador de milhar.

        Args:
            valor: Número a formatar.

        Returns:
            Texto no formato brasileiro (``33.517``).
        """
        return f"{valor:,}".replace(",", ".")

    def _amostra_conferencia(self, preparadas: Sequence[QuestaoPreparada]) -> list[QuestaoPreparada]:
        """Escolhe a amostra de conferência manual.

        Começa pelas questões configuradas e completa com a primeira questão de cada
        combinação (formato, destino do comando) ainda não coberta.

        Args:
            preparadas: Questões preparadas.

        Returns:
            Amostra, sem repetição.
        """
        por_id: dict[str, QuestaoPreparada] = {p.id: p for p in preparadas}
        amostra: list[QuestaoPreparada] = [por_id[i] for i in self._parametros.ids_conferencia if i in por_id]
        cobertas: set[tuple[str, str]] = {(p.formato, p.motivo_comando) for p in amostra}
        preparada: QuestaoPreparada
        for preparada in preparadas:
            if len(amostra) >= self._parametros.tamanho_conferencia:
                break
            chave: tuple[str, str] = (preparada.formato, preparada.motivo_comando)
            if chave not in cobertas:
                amostra.append(preparada)
                cobertas.add(chave)
        return amostra

    def _escrever_conferencia(self, preparadas: Sequence[QuestaoPreparada]) -> Path:
        """Grava a amostra de conferência manual em Markdown.

        Args:
            preparadas: Questões preparadas.

        Returns:
            Caminho do arquivo.
        """
        partes: list[str] = [
            "# Conferência do texto canônico (ADR-004)",
            "",
            (
                "Amostra para conferir à mão: o texto abaixo é exatamente o que os modelos recebem. "
                "Verificar se nada do conteúdo se perdeu na limpeza, se o comando certo entrou ou saiu "
                "e se nenhum rótulo de origem aparece."
            ),
            "",
        ]
        preparada: QuestaoPreparada
        for preparada in self._amostra_conferencia(preparadas):
            original: dict[str, object] = preparada.original
            partes.extend(
                [
                    f"## {preparada.id}: {preparada.formato}, comando {preparada.motivo_comando}",
                    "",
                    (
                        f"- Tamanho: {preparada.caracteres} caracteres (~{preparada.tokens_estimados} tokens); "
                        f"original com {self._tamanho_original(original)} caracteres."
                    ),
                    f"- Comando original: {preparada.comando[:160] or '(vazio)'}",
                    (
                        f"- Rótulos de origem (fora do texto): {original.get('disciplina_origem') or '(vazio)'} / "
                        f"{original.get('assunto_origem') or '(vazio)'}"
                    ),
                    "",
                    "```text",
                    preparada.texto_canonico,
                    "```",
                    "",
                ]
            )
        destino: Path = self._caminhos.saida_preparacao / "conferencia_texto_canonico.md"
        destino.write_text("\n".join(partes), encoding="utf-8")
        return destino

    @staticmethod
    def _tamanho_original(original: dict[str, object]) -> int:
        """Soma os caracteres dos campos HTML originais.

        Args:
            original: Campos originais da questão.

        Returns:
            Total de caracteres de enunciado, comando e alternativas.
        """
        alternativas: object = original.get("alternativas", {})
        total: int = len(str(original.get("enunciado_html", ""))) + len(str(original.get("comando", "")))
        if isinstance(alternativas, dict):
            total += sum(len(str(texto)) for texto in alternativas.values())
        return total

    @staticmethod
    def _imprimir(
        preparadas: Sequence[QuestaoPreparada], checagens: Sequence[ResultadoChecagem], destino: Path, conferencia: Path
    ) -> None:
        """Mostra um resumo no terminal.

        Args:
            preparadas: Questões preparadas.
            checagens: Resultado das checagens.
            destino: Caminho de ``questoes.jsonl``.
            conferencia: Caminho da amostra de conferência.
        """
        aprovadas: int = sum(1 for c in checagens if c.aprovada)
        print(f"Passo 01: {len(preparadas)} questões preparadas; {aprovadas}/{len(checagens)} checagens aprovadas.")
        print(f"Questões:    {destino}")
        print(f"Conferência: {conferencia}")
