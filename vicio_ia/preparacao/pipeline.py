"""Orquestração do passo 01: prepara as questões (ADR-004) e a árvore de temas (ADR-005)."""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Sequence
from pathlib import Path
from typing import TextIO

from vicio_ia.arvore import ArvoreTemas
from vicio_ia.carregamento import CarregadorDados
from vicio_ia.configuracao import Caminhos, ParametrosEDA, ParametrosPreparacao
from vicio_ia.conhecimento import MapaLegislacao
from vicio_ia.dominio import Questao, Tema
from vicio_ia.eda.estatisticas import CalculadoraEstatisticas, ResumoNumerico
from vicio_ia.eda.perfil_questoes import PerfiladorQuestoes
from vicio_ia.eda.perfil_temas import PerfiladorTemas, PerfilTema
from vicio_ia.preparacao.arvore_preparada import DecisoesArvore, LeitorDecisoesArvore, PreparadorArvore, TemaPreparado
from vicio_ia.preparacao.texto_canonico import MontadorTextoCanonico, QuestaoPreparada
from vicio_ia.preparacao.validacao import ResultadoChecagem, ValidadorArvorePreparada, ValidadorQuestoesPreparadas
from vicio_ia.relatorio import Celula, EscritorRelatorio, Secao, Tabela
from vicio_ia.texto import ProcessadorTexto


class ErroPreparacao(Exception):
    """Alguma checagem do passo 01 falhou."""


class PipelinePreparacao:
    """Prepara as questões (ADR-004) e a árvore de temas (ADR-005) para os passos seguintes.

    Saídas:

    * ``dados/preparados/questoes.jsonl``: uma questão preparada por linha (texto canônico,
      campos limpos, marcas, hash e campos originais);
    * ``dados/preparados/temas.json``: cada nó com publicável, canônico, lixeira, sobreposição,
      zona de convenção, recuo e título de exibição;
    * ``dados/preparados/arvore_enxuta.txt``: árvore para os prompts (ID | caminho), bytes estáveis;
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
        """Prepara, valida e grava questões e árvore.

        Returns:
            Caminho de ``questoes.jsonl``.

        Raises:
            ErroPreparacao: Se alguma checagem falhar (nada é gravado em ``dados/preparados/``).
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

        temas: list[Tema] = carregador.carregar_temas()
        arvore: ArvoreTemas = ArvoreTemas(temas)
        perfis_temas: list[PerfilTema] = PerfiladorTemas(arvore, self._parametros_eda, processador).perfilar_todos()
        decisoes: DecisoesArvore = LeitorDecisoesArvore(self._caminhos.dados_temas).ler()
        preparador: PreparadorArvore = PreparadorArvore(arvore, perfis_temas, decisoes)
        temas_preparados: list[TemaPreparado] = preparador.preparar()
        enxuta: str = preparador.arvore_enxuta(temas_preparados)
        checagens_arvore: list[ResultadoChecagem] = ValidadorArvorePreparada().validar(
            temas_preparados, decisoes, enxuta, {tema.tema_id: tema.titulo for tema in temas}
        )

        escritor: EscritorRelatorio = EscritorRelatorio(self._caminhos.saida_preparacao, 40, nome_base="preparacao")
        escritor.preparar_pasta()
        escritor.escrever(
            "Passo 01: questões e árvore preparadas",
            self._introducao(),
            self._secoes(preparadas, checagens)
            + self._secoes_arvore(temas_preparados, decisoes, enxuta, checagens_arvore),
        )
        conferencia: Path = self._escrever_conferencia(preparadas)
        falhas: list[ResultadoChecagem] = [c for c in [*checagens, *checagens_arvore] if not c.aprovada]
        if falhas:
            detalhes: str = "; ".join(f"{f.regra}: {', '.join(f.violacoes)}" for f in falhas)
            raise ErroPreparacao(f"checagens reprovadas: {detalhes}")
        destino: Path = self._gravar(preparadas)
        self._gravar_arvore(temas_preparados, enxuta)
        self._imprimir(preparadas, checagens, destino, conferencia)
        publicaveis: int = sum(1 for tema in temas_preparados if tema.publicavel)
        aprovadas_arvore: int = sum(1 for c in checagens_arvore if c.aprovada)
        print(
            f"Árvore: {publicaveis} temas publicáveis; {aprovadas_arvore}/{len(checagens_arvore)} checagens aprovadas; "
            f"{self._caminhos.dados_preparados / 'temas.json'}"
        )
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

    def _gravar_arvore(self, temas: Sequence[TemaPreparado], enxuta: str) -> None:
        """Grava ``temas.json`` e ``arvore_enxuta.txt`` em ``dados/preparados/``.

        Args:
            temas: Nós preparados.
            enxuta: Texto da árvore enxuta.
        """
        self._caminhos.dados_preparados.mkdir(parents=True, exist_ok=True)
        (self._caminhos.dados_preparados / "temas.json").write_text(
            json.dumps([tema.como_dict() for tema in temas], ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
        )
        (self._caminhos.dados_preparados / "arvore_enxuta.txt").write_text(enxuta, encoding="utf-8")

    def _secoes_arvore(
        self,
        temas: Sequence[TemaPreparado],
        decisoes: DecisoesArvore,
        enxuta: str,
        checagens: Sequence[ResultadoChecagem],
    ) -> list[Secao]:
        """Monta as seções do relatório sobre a árvore.

        Args:
            temas: Nós preparados.
            decisoes: Decisões manuais.
            enxuta: Texto da árvore enxuta.
            checagens: Resultado das checagens da árvore.

        Returns:
            Seções na ordem de exibição.
        """
        por_id: dict[str, TemaPreparado] = {tema.tema_id: tema for tema in temas}
        publicaveis: list[TemaPreparado] = [tema for tema in temas if tema.publicavel]
        fantasmas: list[TemaPreparado] = [tema for tema in temas if tema.fantasma]
        contagem: Counter[tuple[str, int]] = Counter((tema.disciplina, tema.nivel) for tema in publicaveis)
        disciplinas: list[str] = sorted({tema.disciplina for tema in publicaveis})
        secao_nos: Secao = Secao("Árvore: nós utilizáveis")
        secao_nos.achados = [
            (
                f"{len(publicaveis)} nós podem ser tema central; {len(fantasmas)} fantasmas ficam de fora, cada um "
                f"apontando para o nó canônico; {sum(1 for t in temas if t.status != 'active')} inativos ficam de fora."
            ),
            f"{sum(1 for t in publicaveis if t.aceita_recuo)} temas de nível 1 têm subtemas e aceitam o recuo para o pai (ADR-010).",
            (
                "Convenção dos nós duplicados (decisão manual): vale o nó com histórico, em Legislação Especial ou sem "
                "o sufixo '(Parte N)'. Os fantasmas nunca são tema central."
            ),
        ]
        secao_nos.tabelas = [
            Tabela(
                "publicaveis",
                "Nós publicáveis por disciplina",
                ["disciplina", "nível 1", "nível 2", "nível 1 com filhos (recuo)"],
                [
                    [
                        disciplina,
                        contagem[(disciplina, 1)],
                        contagem[(disciplina, 2)],
                        sum(1 for t in publicaveis if t.disciplina == disciplina and t.aceita_recuo),
                    ]
                    for disciplina in disciplinas
                ],
            ),
            Tabela(
                "fantasmas",
                "Fantasmas e o nó que vale no lugar deles",
                ["fantasma", "caminho do fantasma", "canônico", "caminho do canônico"],
                [
                    [
                        f.tema_id,
                        f.caminho,
                        f.canonico_id or "",
                        por_id[f.canonico_id].caminho_exibicao if f.canonico_id else "",
                    ]
                    for f in fantasmas
                ],
            ),
        ]
        secao_nos.metricas = {
            "publicaveis": len(publicaveis),
            "fantasmas": len(fantasmas),
            "aceitam_recuo": sum(1 for t in publicaveis if t.aceita_recuo),
        }

        secao_lixeiras: Secao = Secao("Árvore: lixeiras (decisão manual)")
        niveis: Counter[str] = Counter(nivel for nivel, _ in decisoes.lixeiras.values())
        secao_lixeiras.achados = [
            (
                f"{niveis['forte']} lixeiras fortes (publicar só com concordância total e verificador favorável), "
                f"{niveis['moderada']} moderadas (só variável de risco na calibração) e {niveis['fora']} suspeitas "
                "descartadas como falso positivo da heurística."
            ),
            "Na árvore enxuta, as lixeiras fortes levam a marca [conceitual].",
        ]
        secao_lixeiras.tabelas = [
            Tabela(
                "lixeiras",
                "Lixeiras revisadas",
                ["tema_id", "caminho", "nível", "justificativa"],
                [
                    [i, por_id[i].caminho_exibicao, nivel, justificativa]
                    for i, (nivel, justificativa) in decisoes.lixeiras.items()
                ],
            )
        ]
        secao_lixeiras.metricas = {f"lixeira_{nivel}": n for nivel, n in niveis.items()}

        zona: list[TemaPreparado] = [tema for tema in publicaveis if tema.zona_convencao]
        com_duplicado: list[TemaPreparado] = [
            tema for tema in publicaveis if tema.tema_id in {f.canonico_id for f in fantasmas}
        ]
        tipos: Counter[str] = Counter(tema.tipo_convencao for tema in zona)
        secao_zona: Secao = Secao("Árvore: sobreposições e zona de convenção")
        secao_zona.achados = [
            (
                f"{len(com_duplicado)} nós canônicos têm fantasma duplicado; {len({g for g, _ in decisoes.sobreposicoes.values()})} "
                "grupos de sobreposição têm regra de desempate (herdada pelos subtemas)."
            ),
            (
                f"{len(zona)} nós publicáveis estão na zona de convenção: publicar neles entra na margem de convenção da "
                "previsão (ADR-013), porque o gold não mede esse risco. Por tipo: "
                + ", ".join(f"{tipo} {n}" for tipo, n in tipos.most_common())
                + "."
            ),
            (
                "Os tipos vão do mais ao menos provável de divergir do especialista: cópia em outra disciplina "
                "(ex.: LEP), sobreposição entre nós válidos (ex.: Ação Penal) e cópia '(Parte N)' na mesma "
                "disciplina, que vale também para os subtemas do canônico."
            ),
        ]
        secao_zona.tabelas = [
            Tabela(
                "sobreposicoes",
                "Grupos de sobreposição e regras de desempate",
                ["grupo", "tema_id", "caminho", "regra de desempate"],
                [[g, i, por_id[i].caminho_exibicao, regra] for i, (g, regra) in decisoes.sobreposicoes.items()],
            ),
            Tabela(
                "zona_convencao",
                "Nós na zona de convenção",
                ["tema_id", "caminho", "tipo", "duplicado por", "grupo"],
                [
                    [t.tema_id, t.caminho_exibicao, t.tipo_convencao, ";".join(t.duplicado_por), t.grupo_sobreposicao]
                    for t in zona
                ],
            ),
        ]
        secao_zona.metricas = {
            "zona_convencao": len(zona),
            "canonicos_com_duplicado": len(com_duplicado),
            **{f"zona_{tipo}": n for tipo, n in tipos.items()},
        }

        secao_titulos: Secao = Secao("Árvore: títulos corrigidos (só exibição)")
        secao_titulos.achados = [
            f"{len(decisoes.correcoes)} títulos com erro aparecem corrigidos nos prompts e relatórios; o ID não muda."
        ]
        secao_titulos.tabelas = [
            Tabela(
                "titulos",
                "Títulos corrigidos",
                ["tema_id", "original", "exibição"],
                [[i, original, exibicao] for i, (original, exibicao) in decisoes.correcoes.items()],
            )
        ]
        secao_titulos.metricas = {"titulos_corrigidos": len(decisoes.correcoes)}

        tokens: int = round(len(enxuta) / self._parametros.chars_por_token)
        secao_prompt: Secao = Secao("Árvore: texto para os prompts")
        secao_prompt.achados = [
            f"Árvore enxuta (`arvore_enxuta.txt`): {len(publicaveis)} linhas `ID | caminho`, "
            f"{len(enxuta.encode('utf-8')):,} bytes, ~{tokens:,} tokens.".replace(",", "."),
            (
                "É a versão do voto barato e a base das outras duas (com escopo e cartões por ramo), que vêm dos cartões "
                "de tema (ADR-007)."
            ),
        ]
        secao_prompt.metricas = {"arvore_enxuta_bytes": len(enxuta.encode("utf-8")), "arvore_enxuta_tokens": tokens}

        aprovadas: int = sum(1 for c in checagens if c.aprovada)
        secao_checagens: Secao = Secao("Checagens automáticas: árvore")
        secao_checagens.achados = [f"{aprovadas} de {len(checagens)} checagens aprovadas."]
        secao_checagens.tabelas = [
            Tabela(
                "checagens_arvore",
                "Regras verificadas",
                ["regra", "resultado", "violações"],
                [[c.regra, "aprovada" if c.aprovada else "REPROVADA", ", ".join(c.violacoes)] for c in checagens],
            )
        ]
        secao_checagens.metricas = {"checagens_aprovadas": aprovadas, "checagens": len(checagens)}
        return [secao_nos, secao_lixeiras, secao_zona, secao_titulos, secao_prompt, secao_checagens]

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
        secao_checagens: Secao = Secao("Checagens automáticas: questões")
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
