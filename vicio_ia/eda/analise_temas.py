"""Análise exploratória da árvore de temas (``temas.csv``)."""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Sequence

from vicio_ia.arvore import ArvoreTemas
from vicio_ia.configuracao import ParametrosEDA
from vicio_ia.dominio import Tema
from vicio_ia.eda.estatisticas import CalculadoraEstatisticas
from vicio_ia.eda.perfil_temas import PerfilTema
from vicio_ia.relatorio import Analise, Celula, Secao, Tabela
from vicio_ia.texto import ProcessadorTexto


class AnaliseTemas(Analise):
    """Estrutura, descrições, contagens, fantasmas, repetições, lixeiras, títulos e nós utilizáveis."""

    def __init__(
        self,
        arvore: ArvoreTemas,
        perfis: Sequence[PerfilTema],
        processador: ProcessadorTexto,
        estatisticas: CalculadoraEstatisticas,
        parametros: ParametrosEDA,
    ) -> None:
        """Recebe dados e dependências.

        Args:
            arvore: Árvore de temas.
            perfis: Perfil de cada nó.
            processador: Limpeza e normalização de texto.
            estatisticas: Cálculos descritivos.
            parametros: Limiares e listas da EDA.
        """
        self._arvore: ArvoreTemas = arvore
        self._perfis: Sequence[PerfilTema] = perfis
        self._processador: ProcessadorTexto = processador
        self._estatisticas: CalculadoraEstatisticas = estatisticas
        self._parametros: ParametrosEDA = parametros
        self._perfil_por_id: dict[str, PerfilTema] = {perfil.tema_id: perfil for perfil in perfis}

    def executar(self) -> list[Secao]:
        """Roda todas as análises da árvore.

        Returns:
            Seções na ordem de exibição.
        """
        return [
            self._estrutura(),
            self._descricoes(),
            self._contagens(),
            self._fantasmas(),
            self._titulos_repetidos(),
            self._sobreposicoes(),
            self._lixeiras(),
            self._anomalias(),
            self._utilizaveis(),
        ]

    def _situacao(self, tema_id: str) -> str:
        """Resume a situação de um nó para tabelas.

        Args:
            tema_id: ID do tema.

        Returns:
            ``inativo``, ``fantasma``, ``raiz`` ou ``válido``.
        """
        perfil: PerfilTema = self._perfil_por_id[tema_id]
        if perfil.status != "active":
            return "inativo"
        if perfil.fantasma:
            return "fantasma"
        if perfil.nivel == 0:
            return "raiz"
        return "válido"

    def _estrutura(self) -> Secao:
        """Contagem por disciplina e nível e checagens de consistência da árvore.

        Returns:
            Seção de estrutura.
        """
        contagem: Counter[tuple[str, int, str]] = Counter(
            (perfil.disciplina, perfil.nivel, perfil.status) for perfil in self._perfis
        )
        disciplinas: list[str] = sorted({perfil.disciplina for perfil in self._perfis})
        linhas: list[list[Celula]] = []
        disciplina: str
        for disciplina in disciplinas:
            linhas.append(
                [
                    disciplina,
                    contagem[(disciplina, 0, "active")],
                    contagem[(disciplina, 1, "active")],
                    contagem[(disciplina, 2, "active")],
                    sum(n for (nome, _, status), n in contagem.items() if nome == disciplina and status != "active"),
                ]
            )
        problemas: list[list[Celula]] = []
        tema: Tema
        for tema in self._arvore.todos():
            pai: Tema | None = self._arvore.pai(tema.tema_id)
            if tema.parent_id is not None and pai is None:
                problemas.append([tema.tema_id, "pai inexistente", tema.parent_id])
            if pai is not None and tema.nivel != pai.nivel + 1:
                problemas.append([tema.tema_id, "nível inconsistente com o pai", f"{tema.nivel} vs pai {pai.nivel}"])
            if tema.parent_id is None and tema.nivel != 0:
                problemas.append([tema.tema_id, "raiz com nível diferente de 0", str(tema.nivel)])
            esperado: str = " > ".join(
                [ancestral.titulo for ancestral in self._arvore.ancestrais(tema.tema_id)] + [tema.titulo]
            )
            if esperado != tema.caminho:
                problemas.append([tema.tema_id, "caminho diferente do esperado", tema.caminho])
            raizes: list[Tema] = self._arvore.ancestrais(tema.tema_id)[:1]
            if raizes and raizes[0].disciplina != tema.disciplina:
                problemas.append([tema.tema_id, "disciplina diferente da raiz", tema.disciplina])
        identificador: str
        for identificador in self._arvore.ids_duplicados:
            problemas.append([identificador, "ID repetido no CSV", ""])
        profundidade_max: int = max((perfil.nivel for perfil in self._perfis), default=0)
        secao: Secao = Secao("Temas: estrutura da árvore")
        secao.achados = [
            (
                f"{len(self._arvore)} nós em {len(self._arvore.raizes())} disciplinas; profundidade máxima {profundidade_max} "
                "(disciplina > tema > subtema)."
            ),
            f"{sum(1 for perfil in self._perfis if perfil.status != 'active')} nós inativos (não podem ser usados).",
            f"{len(problemas)} problemas de consistência (pai inexistente, nível, caminho, disciplina ou ID repetido).",
        ]
        secao.tabelas = [
            Tabela(
                "nos_por_disciplina",
                "Nós ativos por disciplina e nível",
                ["disciplina", "nível 0", "nível 1", "nível 2", "inativos"],
                linhas,
            ),
            Tabela("problemas_estrutura", "Problemas de consistência", ["tema_id", "problema", "detalhe"], problemas),
        ]
        secao.metricas = {
            "nos": len(self._arvore),
            "disciplinas": len(self._arvore.raizes()),
            "inativos": sum(1 for perfil in self._perfis if perfil.status != "active"),
            "problemas_estrutura": len(problemas),
        }
        return secao

    def _descricoes(self) -> Secao:
        """Classifica as descrições em raiz, vazia, modelo e rica.

        Returns:
            Seção de descrições.
        """
        tipos: Counter[str] = Counter(perfil.tipo_descricao for perfil in self._perfis)
        por_disciplina: Counter[tuple[str, str]] = Counter(
            (perfil.disciplina, perfil.tipo_descricao) for perfil in self._perfis
        )
        disciplinas: list[str] = sorted({perfil.disciplina for perfil in self._perfis})
        nomes_tipos: list[str] = ["raiz", "vazia", "modelo", "rica"]
        linhas: list[list[Celula]] = [
            [disciplina, *[por_disciplina[(disciplina, tipo)] for tipo in nomes_tipos]] for disciplina in disciplinas
        ]
        ricas: list[list[Celula]] = [
            [perfil.tema_id, perfil.caminho, self._processador.trecho(self._arvore.tema(perfil.tema_id).descricao, 200)]
            for perfil in self._perfis
            if perfil.tipo_descricao == "rica"
        ]
        abaixo_raiz: int = len(self._perfis) - tipos["raiz"]
        secao: Secao = Secao("Temas: descrições")
        secao.achados = [
            (
                f"Dos {abaixo_raiz} nós abaixo das disciplinas, {tipos['modelo']} têm só o texto-modelo "
                "('Subtema de X. N questões no source'), sem conteúdo jurídico; "
                f"{tipos['rica']} têm descrição de verdade e {tipos['vazia']} não têm descrição."
            ),
            (
                "Consequência: o título é praticamente a única definição de cada tema. Vale escrever um 'cartão' por tema "
                "(passo 02) com o que entra, o que não entra e as leis/artigos de referência."
            ),
        ]
        secao.tabelas = [
            Tabela("tipos_descricao", "Tipo de descrição por disciplina", ["disciplina", *nomes_tipos], linhas),
            Tabela("descricoes_ricas", "Nós com descrição de verdade", ["tema_id", "caminho", "descrição"], ricas),
        ]
        secao.metricas = {f"descricao_{tipo}": n for tipo, n in tipos.items()}
        return secao

    def _contagens(self) -> Secao:
        """Analisa a contagem histórica de questões por nó.

        Returns:
            Seção de contagens.
        """
        com_contagem: list[PerfilTema] = [
            perfil for perfil in self._perfis if perfil.nivel > 0 and perfil.n_questoes_origem is not None
        ]
        sem_contagem: list[PerfilTema] = [
            perfil for perfil in self._perfis if perfil.nivel > 0 and perfil.n_questoes_origem is None
        ]
        zerados: list[PerfilTema] = [perfil for perfil in com_contagem if perfil.n_questoes_origem == 0]
        maiores: list[PerfilTema] = sorted(
            com_contagem, key=lambda perfil: perfil.n_questoes_origem or 0, reverse=True
        )[:25]
        linhas_maiores: list[list[Celula]] = [
            [perfil.tema_id, perfil.caminho, perfil.n_questoes_origem or 0, perfil.participacao_no_pai or ""]
            for perfil in maiores
        ]
        linhas_zerados: list[list[Celula]] = [[perfil.tema_id, perfil.caminho] for perfil in zerados]
        linhas_sem: list[list[Celula]] = [
            [perfil.tema_id, perfil.caminho, perfil.tipo_descricao, self._situacao(perfil.tema_id)]
            for perfil in sem_contagem
        ]
        valores: list[float] = [float(perfil.n_questoes_origem or 0) for perfil in com_contagem]
        secao: Secao = Secao("Temas: contagem histórica de questões")
        secao.achados = [
            (
                f"{len(com_contagem)} nós informam quantas questões tinham na origem; {len(sem_contagem)} não informam "
                "(fantasmas e nós com descrição rica)."
            ),
            (
                f"Mediana de {self._estatisticas.resumir(valores).mediana:.0f} questões por nó, mas poucos nós concentram "
                "centenas: é o rastro das lixeiras deixadas pela classificação automática anterior."
            ),
            (
                f"{len(zerados)} nós com 0 questões, entre eles temas importantes (ex.: Medidas Cautelares Diversas da Prisão). "
                "Provavelmente é aí que deveriam estar questões que foram parar nas lixeiras."
            ),
            "A contagem reflete a classificação antiga (com erros), então não serve como probabilidade a priori do tema.",
        ]
        secao.tabelas = [
            Tabela(
                "maiores_contagens",
                "Nós com mais questões na origem",
                ["tema_id", "caminho", "questões", "participação no pai"],
                linhas_maiores,
            ),
            Tabela("nos_zerados", "Nós com 0 questões na origem", ["tema_id", "caminho"], linhas_zerados),
            Tabela("nos_sem_contagem", "Nós sem contagem", ["tema_id", "caminho", "descrição", "situação"], linhas_sem),
        ]
        secao.metricas = {"com_contagem": len(com_contagem), "sem_contagem": len(sem_contagem), "zerados": len(zerados)}
        return secao

    def _fantasmas(self) -> Secao:
        """Lista os nós fantasmas e o nó canônico de cada um.

        Returns:
            Seção de nós fantasmas.
        """
        fantasmas: list[PerfilTema] = [perfil for perfil in self._perfis if perfil.fantasma]
        linhas: list[list[Celula]] = [
            [
                perfil.tema_id,
                perfil.caminho,
                perfil.canonico_id or "(não encontrado)",
                perfil.canonico_caminho,
                perfil.similaridade_canonico if perfil.similaridade_canonico is not None else "",
            ]
            for perfil in fantasmas
        ]
        sem_canonico: int = sum(1 for perfil in fantasmas if not perfil.canonico_id)
        de_parte: int = sum(1 for perfil in fantasmas if self._processador.tem_parte(perfil.titulo))
        outra_disciplina: int = sum(
            1
            for perfil in fantasmas
            if perfil.canonico_id and self._perfil_por_id[perfil.canonico_id].disciplina != perfil.disciplina
        )
        secao: Secao = Secao("Temas: nós fantasmas")
        secao.achados = [
            (
                f"{len(fantasmas)} nós ativos sem descrição e sem histórico de questões: {de_parte} são do tipo "
                f"'(Parte N)' e {outra_disciplina} copiam um tema de outra disciplina (ex.: LEP em Processo Penal e em Legislação Especial)."
            ),
            (
                "Hipótese: foram criados em lote, a partir dos assuntos do site de origem (os IDs são os mais altos da árvore). "
                "A análise cruzada mostra assuntos de origem que batem exatamente com esses nós."
            ),
            (
                f"Canônico encontrado para {len(fantasmas) - sem_canonico} deles. Recomendação: não usar fantasma como tema central "
                "e confirmar com a equipe qual nó do par vale."
            ),
        ]
        secao.tabelas = [
            Tabela(
                "fantasmas",
                "Nós fantasmas e canônicos",
                ["tema_id", "caminho", "canônico", "caminho do canônico", "similaridade"],
                linhas,
            ),
        ]
        secao.metricas = {
            "fantasmas": len(fantasmas),
            "fantasmas_parte": de_parte,
            "fantasmas_sem_canonico": sem_canonico,
        }
        return secao

    def _titulos_repetidos(self) -> Secao:
        """Agrupa nós com o mesmo título (ignorando acento, plural e "(Parte N)").

        Returns:
            Seção de títulos repetidos.
        """
        grupos: dict[str, list[PerfilTema]] = defaultdict(list)
        perfil: PerfilTema
        for perfil in self._perfis:
            if perfil.nivel > 0:
                grupos[self._processador.chave_comparacao(perfil.titulo, manter_parte=False)].append(perfil)
        repetidos: list[list[PerfilTema]] = sorted(
            (membros for membros in grupos.values() if len(membros) > 1), key=len, reverse=True
        )
        linhas: list[list[Celula]] = [
            [
                len(membros),
                " | ".join(
                    f"{membro.tema_id} {membro.caminho} [{self._situacao(membro.tema_id)}]" for membro in membros
                ),
            ]
            for membros in repetidos
        ]
        so_validos: int = sum(
            1 for membros in repetidos if sum(1 for membro in membros if self._situacao(membro.tema_id) == "válido") > 1
        )
        secao: Secao = Secao("Temas: títulos repetidos")
        secao.achados = [
            (
                f"{len(repetidos)} títulos aparecem em mais de um nó; em {so_validos} deles há mais de um nó válido "
                "(sem contar fantasmas), como 'Ação Penal' em Penal e em Processo Penal."
            ),
            (
                "Quando dois nós válidos têm o mesmo nome, o especialista precisa de uma regra para escolher; sem ela, "
                "a questão deve ir para revisão."
            ),
        ]
        secao.tabelas = [Tabela("titulos_repetidos", "Títulos repetidos", ["nós", "membros"], linhas)]
        secao.metricas = {"titulos_repetidos": len(repetidos), "repetidos_entre_validos": so_validos}
        return secao

    def _sobreposicoes(self) -> Secao:
        """Procura títulos de uma disciplina contidos em títulos de outra (escopo sobreposto).

        Returns:
            Seção de sobreposições entre disciplinas.
        """
        validos: list[PerfilTema] = [perfil for perfil in self._perfis if perfil.publicavel]
        chaves: dict[str, set[str]] = {
            perfil.tema_id: set(self._processador.chave_comparacao(perfil.titulo, manter_parte=False).split())
            for perfil in validos
        }
        linhas: list[list[Celula]] = []
        menor: PerfilTema
        maior: PerfilTema
        for menor in validos:
            palavras_menor: set[str] = chaves[menor.tema_id]
            if len(palavras_menor) < 2:
                continue
            for maior in validos:
                if maior.tema_id == menor.tema_id or maior.disciplina == menor.disciplina:
                    continue
                if palavras_menor == chaves[maior.tema_id] and menor.tema_id > maior.tema_id:
                    continue
                if palavras_menor <= chaves[maior.tema_id]:
                    linhas.append([menor.tema_id, menor.caminho, maior.tema_id, maior.caminho])
        secao: Secao = Secao("Temas: sobreposição entre disciplinas")
        secao.achados = [
            (
                f"{len(linhas)} pares em que o título de um nó está contido no título de um nó de outra disciplina "
                "(ex.: Interceptação Telefônica em Legislação Especial e em Processo Penal; Teoria da Pena em Penal e "
                "Teorias Legitimadoras da Pena em Criminologia)."
            ),
            (
                "São escopos que se sobrepõem de verdade: o mesmo assunto pode ser cobrado pelo lado material ou processual. "
                "Cada par precisa de uma regra de desempate nos cartões de tema."
            ),
        ]
        secao.tabelas = [
            Tabela(
                "sobreposicoes",
                "Títulos contidos em outra disciplina",
                ["tema_id", "caminho", "contido em", "caminho"],
                linhas,
            )
        ]
        secao.metricas = {"pares_sobrepostos": len(linhas)}
        return secao

    def _lixeiras(self) -> Secao:
        """Lista os nós suspeitos de serem lixeiras.

        Returns:
            Seção de lixeiras.
        """
        suspeitos: list[PerfilTema] = sorted(
            (perfil for perfil in self._perfis if perfil.suspeita_lixeira),
            key=lambda perfil: perfil.n_questoes_origem or 0,
            reverse=True,
        )
        linhas: list[list[Celula]] = [
            [
                perfil.tema_id,
                perfil.caminho,
                perfil.n_questoes_origem or 0,
                perfil.total_questoes_irmaos or "",
                perfil.participacao_no_pai if perfil.participacao_no_pai is not None else "",
                perfil.motivo_lixeira,
            ]
            for perfil in suspeitos
        ]
        secao: Secao = Secao("Temas: possíveis lixeiras")
        secao.achados = [
            (
                f"{len(suspeitos)} nós suspeitos: concentram {self._parametros.limiar_participacao_lixeira:.0%} ou mais "
                f"das questões dos irmãos (com {self._parametros.min_questoes_lixeira}+ questões), ou têm título genérico "
                "('Conceito', 'Noções gerais', 'Princípios', 'Introdução') com muitas questões."
            ),
            (
                "Só entram nós sem filhos: a contagem de um tema com subtemas soma a dos filhos e sempre parece inflada. "
                "É também nos temas com filhos que a decisão recua quando há dúvida entre subtemas."
            ),
            (
                "A heurística precisa de revisão humana: um tema específico e muito cobrado (ex.: Homicídio) também concentra "
                "questões sem ser lixeira. A lista final entra em decisoes_manuais.md."
            ),
            "Uso: o prompt avisa que esses nós só servem para questões sobre o conceito geral, e publicar neles exige mais evidência.",
        ]
        secao.tabelas = [
            Tabela(
                "lixeiras",
                "Possíveis lixeiras",
                ["tema_id", "caminho", "questões", "total dos irmãos", "participação", "motivo"],
                linhas,
            ),
        ]
        secao.metricas = {"suspeitas_lixeira": len(suspeitos)}
        return secao

    def _anomalias(self) -> Secao:
        """Lista problemas de digitação e formatação nos títulos.

        Returns:
            Seção de anomalias de título.
        """
        com_anomalia: list[PerfilTema] = [perfil for perfil in self._perfis if perfil.anomalias_titulo]
        linhas: list[list[Celula]] = [
            [perfil.tema_id, perfil.titulo, "; ".join(perfil.anomalias_titulo)] for perfil in com_anomalia
        ]
        secao: Secao = Secao("Temas: anomalias de título")
        secao.achados = [
            f"{len(com_anomalia)} títulos com suspeita de erro (número no início, palavras coladas, grafia estranha).",
            (
                "Não muda a classificação (o ID é o que vale), mas confunde quem lê e vai para o memo do professor. "
                "No prompt, os títulos aparecem corrigidos."
            ),
        ]
        secao.tabelas = [Tabela("anomalias_titulo", "Anomalias de título", ["tema_id", "título", "anomalias"], linhas)]
        secao.metricas = {"titulos_com_anomalia": len(com_anomalia)}
        return secao

    def _utilizaveis(self) -> Secao:
        """Conta os nós que podem ser tema central e os que aceitam o recuo para o pai.

        Returns:
            Seção de nós utilizáveis.
        """
        publicaveis: list[PerfilTema] = [perfil for perfil in self._perfis if perfil.publicavel]
        por_disciplina: Counter[tuple[str, int]] = Counter((perfil.disciplina, perfil.nivel) for perfil in publicaveis)
        recuo: Counter[str] = Counter(perfil.disciplina for perfil in publicaveis if perfil.aceita_recuo)
        folhas_nivel1: Counter[str] = Counter(
            perfil.disciplina for perfil in publicaveis if perfil.nivel == 1 and perfil.n_filhos == 0
        )
        disciplinas: list[str] = sorted({perfil.disciplina for perfil in publicaveis})
        linhas: list[list[Celula]] = [
            [
                disciplina,
                por_disciplina[(disciplina, 1)],
                por_disciplina[(disciplina, 2)],
                recuo[disciplina],
                folhas_nivel1[disciplina],
            ]
            for disciplina in disciplinas
        ]
        secao: Secao = Secao("Temas: nós utilizáveis como tema central")
        secao.achados = [
            f"{len(publicaveis)} nós podem ser tema central (ativos, não fantasmas, abaixo da disciplina).",
            (
                f"{sum(recuo.values())} temas de nível 1 têm subtemas e aceitam o recuo para o pai; "
                f"{sum(folhas_nivel1.values())} temas de nível 1 não têm filhos (o recuo não se aplica)."
            ),
            "Pela régua do case, publicar no tema pai é certo para qualquer subtema escolhido pelo especialista.",
        ]
        secao.tabelas = [
            Tabela(
                "utilizaveis",
                "Nós utilizáveis por disciplina",
                ["disciplina", "nível 1", "nível 2", "nível 1 com filhos (recuo)", "nível 1 sem filhos"],
                linhas,
            )
        ]
        secao.metricas = {"publicaveis": len(publicaveis), "aceitam_recuo": sum(recuo.values())}
        return secao
