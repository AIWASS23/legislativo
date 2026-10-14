"""Análise cruzada: o que os rótulos de origem e as leis citadas dizem sobre a árvore."""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from vicio_ia.arvore import ArvoreTemas
from vicio_ia.conhecimento import LeiConhecida, MapaLegislacao
from vicio_ia.eda.estatisticas import CalculadoraEstatisticas
from vicio_ia.eda.perfil_questoes import PerfilQuestao
from vicio_ia.eda.perfil_temas import PerfilTema
from vicio_ia.relatorio import Analise, Celula, Secao, Tabela
from vicio_ia.texto import ProcessadorTexto

type CategoriaCasamento = Literal["vazio", "tema_valido", "fantasma", "inativo", "sem_correspondencia"]
"""Resultado de procurar o assunto de origem entre os títulos da árvore."""


@dataclass(frozen=True)
class CasamentoAssunto:
    """Resultado de casar um assunto de origem com títulos da árvore.

    Attributes:
        categoria: O melhor tipo de nó encontrado (válido > fantasma > inativo).
        temas: IDs de todos os nós cujo título bateu.
    """

    categoria: CategoriaCasamento
    temas: tuple[str, ...]


class AnaliseCruzada(Analise):
    """Assunto de origem × títulos, consistência de disciplina, leis × temas e cobertura de sinais fracos."""

    def __init__(
        self,
        perfis_questoes: Sequence[PerfilQuestao],
        perfis_temas: Sequence[PerfilTema],
        arvore: ArvoreTemas,
        processador: ProcessadorTexto,
        legislacao: MapaLegislacao,
        estatisticas: CalculadoraEstatisticas,
    ) -> None:
        """Recebe dados e dependências e indexa os títulos da árvore.

        Args:
            perfis_questoes: Perfil de cada questão.
            perfis_temas: Perfil de cada nó.
            arvore: Árvore de temas.
            processador: Limpeza e normalização de texto.
            legislacao: Catálogo de leis.
            estatisticas: Cálculos descritivos.
        """
        self._questoes: Sequence[PerfilQuestao] = perfis_questoes
        self._temas: dict[str, PerfilTema] = {perfil.tema_id: perfil for perfil in perfis_temas}
        self._arvore: ArvoreTemas = arvore
        self._processador: ProcessadorTexto = processador
        self._legislacao: MapaLegislacao = legislacao
        self._estatisticas: CalculadoraEstatisticas = estatisticas
        self._indice: dict[str, list[str]] = defaultdict(list)
        perfil: PerfilTema
        for perfil in perfis_temas:
            if perfil.nivel > 0:
                self._indice[processador.chave_comparacao(perfil.titulo, manter_parte=True)].append(perfil.tema_id)
        self._casamentos: dict[str, CasamentoAssunto] = {
            questao.id: self._casar(questao.assunto_origem) for questao in perfis_questoes
        }

    def executar(self) -> list[Secao]:
        """Roda todas as análises cruzadas.

        Returns:
            Seções na ordem de exibição.
        """
        return [
            self._assunto_vs_arvore(),
            self._consistencia_disciplina(),
            self._leis_vs_temas(),
            self._sinais_fracos(),
        ]

    def _situacao(self, tema_id: str) -> str:
        """Resume a situação de um nó.

        Args:
            tema_id: ID do tema.

        Returns:
            ``inexistente``, ``inativo``, ``fantasma``, ``raiz`` ou ``válido``.
        """
        perfil: PerfilTema | None = self._temas.get(tema_id)
        if perfil is None:
            return "inexistente"
        if perfil.status != "active":
            return "inativo"
        if perfil.fantasma:
            return "fantasma"
        if perfil.nivel == 0:
            return "raiz"
        return "válido"

    def _descrever(self, tema_ids: Sequence[str]) -> str:
        """Descreve uma lista de nós para tabelas.

        Args:
            tema_ids: IDs dos nós.

        Returns:
            ``"id caminho [situação]"`` separados por ``" | "``.
        """
        partes: list[str] = []
        tema_id: str
        for tema_id in tema_ids:
            perfil: PerfilTema | None = self._temas.get(tema_id)
            caminho: str = perfil.caminho if perfil is not None else "?"
            partes.append(f"{tema_id} {caminho} [{self._situacao(tema_id)}]")
        return " | ".join(partes)

    def _casar(self, assunto: str) -> CasamentoAssunto:
        """Procura o assunto de origem entre os títulos da árvore.

        Cada parte separada por vírgula é procurada primeiro com o marcador
        "(Parte N)" (para achar os fantasmas) e, se não bater, sem ele.

        Args:
            assunto: Assunto de origem.

        Returns:
            Categoria e nós encontrados.
        """
        if not assunto.strip():
            return CasamentoAssunto("vazio", ())
        encontrados: list[str] = []
        pedaco: str
        for pedaco in assunto.split(","):
            if not pedaco.strip():
                continue
            ids: list[str] = self._indice.get(self._processador.chave_comparacao(pedaco, manter_parte=True), [])
            if not ids:
                ids = self._indice.get(self._processador.chave_comparacao(pedaco, manter_parte=False), [])
            encontrados.extend(identificador for identificador in ids if identificador not in encontrados)
        situacoes: set[str] = {self._situacao(identificador) for identificador in encontrados}
        categoria: CategoriaCasamento
        if "válido" in situacoes:
            categoria = "tema_valido"
        elif "fantasma" in situacoes:
            categoria = "fantasma"
        elif "inativo" in situacoes:
            categoria = "inativo"
        else:
            categoria = "sem_correspondencia"
        return CasamentoAssunto(categoria, tuple(encontrados))

    def _validos(self, tema_ids: Sequence[str]) -> list[str]:
        """Filtra os nós válidos de uma lista.

        Args:
            tema_ids: IDs dos nós.

        Returns:
            Apenas os IDs de nós válidos.
        """
        return [tema_id for tema_id in tema_ids if self._situacao(tema_id) == "válido"]

    def _assunto_vs_arvore(self) -> Secao:
        """Mostra quantos assuntos de origem batem com títulos da árvore, e com que tipo de nó.

        Returns:
            Seção de assunto × árvore.
        """
        categorias: Counter[str] = Counter(casamento.categoria for casamento in self._casamentos.values())
        por_assunto: dict[str, list[str]] = defaultdict(list)
        questao: PerfilQuestao
        for questao in self._questoes:
            por_assunto[questao.assunto_origem].append(questao.id)
        linhas: list[list[Celula]] = []
        assunto: str
        ids: list[str]
        for assunto, ids in sorted(por_assunto.items(), key=lambda item: len(item[1]), reverse=True):
            casamento: CasamentoAssunto = self._casamentos[ids[0]]
            linhas.append([assunto or "(vazio)", len(ids), casamento.categoria, self._descrever(casamento.temas)])
        ambiguos: int = sum(1 for casamento in self._casamentos.values() if len(self._validos(casamento.temas)) > 1)
        total: int = len(self._questoes)
        linhas_categorias: list[list[Celula]] = [
            [categoria, n, self._estatisticas.percentual(n, total)] for categoria, n in categorias.most_common()
        ]
        secao: Secao = Secao("Cruzamento: assunto de origem × títulos da árvore")
        secao.achados = [
            (
                f"{categorias['tema_valido']} questões ({self._estatisticas.percentual(categorias['tema_valido'], total)}%) "
                "têm assunto de origem igual ao título de um nó válido; isso não quer dizer que o tema esteja certo "
                "(ex.: extorsão mediante sequestro com assunto 'Lesão Corporal')."
            ),
            (
                f"{categorias['fantasma']} questões têm assunto igual ao título de um nó fantasma (ex.: 'Teoria da Pena (Parte 02)' "
                "e o nó 'Teoria da Pena (Parte 2)'). Isso reforça a hipótese de que os fantasmas vieram da importação."
            ),
            f"{ambiguos} questões têm assunto que bate com mais de um nó válido (ex.: 'Ação Penal' em Penal e em Processo Penal).",
            f"{categorias['sem_correspondencia']} sem correspondência e {categorias['vazio']} sem assunto.",
        ]
        secao.tabelas = [
            Tabela(
                "categorias_casamento",
                "Questões por resultado do casamento",
                ["resultado", "questões", "%"],
                linhas_categorias,
            ),
            Tabela(
                "assunto_vs_arvore",
                "Cada assunto de origem e os nós com o mesmo título",
                ["assunto", "questões", "resultado", "nós"],
                linhas,
            ),
        ]
        secao.metricas = {**{f"assunto_{nome}": n for nome, n in categorias.items()}, "assunto_ambiguo": ambiguos}
        return secao

    def _consistencia_disciplina(self) -> Secao:
        """Compara a disciplina de origem com a disciplina do nó casado pelo assunto.

        Returns:
            Seção de consistência entre disciplina e assunto.
        """
        consistentes: int = 0
        fora_recorte: int = 0
        inconsistentes: list[list[Celula]] = []
        questao: PerfilQuestao
        for questao in self._questoes:
            validos: list[str] = self._validos(self._casamentos[questao.id].temas)
            if not validos:
                continue
            if not questao.disciplina_normalizada:
                fora_recorte += 1
                continue
            disciplinas: set[str] = {self._temas[tema_id].disciplina for tema_id in validos}
            if questao.disciplina_normalizada in disciplinas:
                consistentes += 1
            else:
                inconsistentes.append(
                    [questao.id, questao.disciplina_origem, questao.assunto_origem, self._descrever(validos)]
                )
        secao: Secao = Secao("Cruzamento: disciplina de origem × disciplina do assunto")
        secao.achados = [
            (
                f"Entre as questões cujo assunto bate com um nó válido: {consistentes} têm disciplina de origem coerente, "
                f"{len(inconsistentes)} incoerente e {fora_recorte} vêm de disciplina fora do recorte."
            ),
            "Incoerência entre os dois rótulos de origem é mais um sinal de que eles não servem como gabarito.",
        ]
        secao.tabelas = [
            Tabela(
                "disciplina_incoerente",
                "Disciplina de origem incoerente com o assunto",
                ["id", "disciplina de origem", "assunto", "nós do assunto"],
                inconsistentes,
            ),
        ]
        secao.metricas = {
            "coerentes": consistentes,
            "incoerentes": len(inconsistentes),
            "fora_do_recorte": fora_recorte,
        }
        return secao

    def _leis_vs_temas(self) -> Secao:
        """Confere o catálogo de leis contra a árvore e conta as citações.

        Returns:
            Seção de leis × temas.
        """
        citacoes: Counter[str] = Counter(numero for questao in self._questoes for numero in questao.leis_citadas)
        linhas: list[list[Celula]] = []
        problemas: list[str] = []
        lei: LeiConhecida
        for lei in self._legislacao.todas():
            if not lei.temas:
                continue
            situacoes: list[str] = [self._situacao(tema_id) for tema_id in lei.temas]
            if "válido" not in situacoes:
                problemas.append(lei.numero)
            linhas.append([lei.numero, lei.nome, citacoes[lei.numero], self._descrever(lei.temas)])
        linhas.sort(key=lambda linha: int(linha[2]), reverse=True)
        com_fantasma: int = sum(
            1 for lei in self._legislacao.todas() if any(self._situacao(tema_id) == "fantasma" for tema_id in lei.temas)
        )
        secao: Secao = Secao("Cruzamento: leis citadas × temas")
        secao.achados = [
            f"{len(linhas)} leis do catálogo apontam para temas; {len(problemas)} apontam só para nós inválidos.",
            (
                f"{com_fantasma} leis têm um nó válido em Legislação Especial e um fantasma com o mesmo nome em Penal ou "
                "Processo Penal: a duplicidade atinge justamente as leis mais cobradas (Drogas, LEP, Maria da Penha)."
            ),
        ]
        secao.tabelas = [
            Tabela(
                "leis_temas",
                "Leis do catálogo, citações e temas indicados",
                ["lei", "nome", "questões", "temas"],
                linhas,
            )
        ]
        secao.metricas = {
            "leis_com_tema": len(linhas),
            "leis_sem_tema_valido": len(problemas),
            "leis_com_fantasma": com_fantasma,
        }
        return secao

    def _sinais_fracos(self) -> Secao:
        """Mede quantas questões têm algum sinal fraco de tema e se os sinais concordam.

        Returns:
            Seção de cobertura dos sinais fracos.
        """
        linhas_questoes: list[list[Celula]] = []
        so_assunto: int = 0
        so_lei: int = 0
        ambos: int = 0
        concordam: int = 0
        mesma_disciplina: int = 0
        conflitos: Counter[str] = Counter()
        questao: PerfilQuestao
        for questao in self._questoes:
            temas_assunto: list[str] = self._validos(self._casamentos[questao.id].temas)
            temas_lei: list[str] = []
            numero: str
            for numero in questao.leis_citadas:
                lei: LeiConhecida | None = self._legislacao.lei(numero)
                if lei is not None:
                    temas_lei.extend(tema_id for tema_id in self._validos(lei.temas) if tema_id not in temas_lei)
            if temas_assunto and temas_lei:
                ambos += 1
                if any(self._arvore.mesmo_ramo(a, b) for a in temas_assunto for b in temas_lei):
                    concordam += 1
                else:
                    conflitos[questao.assunto_origem] += 1
                disciplinas_assunto: set[str] = {self._temas[tema_id].disciplina for tema_id in temas_assunto}
                if disciplinas_assunto & {self._temas[tema_id].disciplina for tema_id in temas_lei}:
                    mesma_disciplina += 1
            elif temas_assunto:
                so_assunto += 1
            elif temas_lei:
                so_lei += 1
            linhas_questoes.append(
                [questao.id, self._casamentos[questao.id].categoria, ";".join(temas_assunto), ";".join(temas_lei)]
            )
        total: int = len(self._questoes)
        nenhum: int = total - so_assunto - so_lei - ambos
        linhas_resumo: list[list[Celula]] = [
            ["só assunto de origem", so_assunto, self._estatisticas.percentual(so_assunto, total)],
            ["só lei citada", so_lei, self._estatisticas.percentual(so_lei, total)],
            ["os dois", ambos, self._estatisticas.percentual(ambos, total)],
            ["nenhum", nenhum, self._estatisticas.percentual(nenhum, total)],
        ]
        assunto_conflito: str
        n_conflito: int
        assunto_conflito, n_conflito = conflitos.most_common(1)[0] if conflitos else ("", 0)
        n_assunto_conflito: int = sum(1 for questao in self._questoes if questao.assunto_origem == assunto_conflito)
        linhas_conflitos: list[list[Celula]] = [
            [assunto or "(vazio)", n, sum(1 for questao in self._questoes if questao.assunto_origem == assunto)]
            for assunto, n in conflitos.most_common()
        ]
        secao: Secao = Secao("Cruzamento: cobertura dos sinais fracos")
        secao.achados = [
            (
                f"{total - nenhum} questões ({self._estatisticas.percentual(total - nenhum, total)}%) têm ao menos um sinal fraco "
                f"de tema (assunto de origem com título válido ou lei catalogada); {nenhum} não têm nenhum."
            ),
            (
                f"Quando os dois sinais existem ({ambos} questões), caem no mesmo ramo em {concordam} e na mesma disciplina em "
                f"{mesma_disciplina}. Não é erro de cálculo: a lei aponta para Legislação Especial e o assunto de origem "
                "aponta para Penal ou Processo Penal."
            ),
            (
                f"Em vários desses casos o assunto de origem está claramente errado. '{assunto_conflito}' aparece em "
                f"{n_conflito} dos conflitos (de {n_assunto_conflito} questões com esse assunto): o site de origem também tem "
                "lixeiras, e o assunto mais frequente do recorte é uma delas."
            ),
            (
                "Conclusão: sinal fraco serve para desempate e para medir concordância, nunca como rótulo. "
                "O classificador principal continua sendo o modelo de linguagem."
            ),
        ]
        secao.tabelas = [
            Tabela("cobertura_sinais", "Cobertura dos sinais fracos", ["sinal", "questões", "%"], linhas_resumo),
            Tabela(
                "assuntos_em_conflito",
                "Assuntos de origem em conflito com a lei citada",
                ["assunto de origem", "conflitos", "questões com o assunto"],
                linhas_conflitos,
            ),
            Tabela(
                "sinais_por_questao",
                "Sinais fracos por questão",
                ["id", "assunto de origem", "temas pelo assunto", "temas pela lei"],
                linhas_questoes,
            ),
        ]
        secao.metricas = {
            "sem_sinal": nenhum,
            "dois_sinais": ambos,
            "dois_sinais_mesmo_ramo": concordam,
            "dois_sinais_mesma_disciplina": mesma_disciplina,
        }
        return secao
