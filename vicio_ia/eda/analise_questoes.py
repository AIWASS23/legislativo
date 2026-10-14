"""Análise exploratória das questões (``questoes.jsonl``)."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from collections.abc import Sequence
from typing import ClassVar

from vicio_ia.carregamento import CarregadorDados, RegistroBruto
from vicio_ia.configuracao import ParametrosEDA
from vicio_ia.conhecimento import LeiConhecida, MapaLegislacao
from vicio_ia.dominio import Questao
from vicio_ia.eda.estatisticas import CalculadoraEstatisticas
from vicio_ia.eda.perfil_questoes import PerfiladorQuestoes, PerfilQuestao, TextoLimpo
from vicio_ia.relatorio import Analise, Celula, Secao, Tabela
from vicio_ia.texto import ProcessadorTexto


class AnaliseQuestoes(Analise):
    """Integridade, formato, ruído, tamanho, comando, enunciados, repetições, origem e leis."""

    _RE_ID: ClassVar[re.Pattern[str]] = re.compile(r"Q\d{4}")

    def __init__(
        self,
        registros: Sequence[RegistroBruto],
        questoes: Sequence[Questao],
        perfis: Sequence[PerfilQuestao],
        perfilador: PerfiladorQuestoes,
        processador: ProcessadorTexto,
        legislacao: MapaLegislacao,
        estatisticas: CalculadoraEstatisticas,
        parametros: ParametrosEDA,
    ) -> None:
        """Recebe dados e dependências.

        Args:
            registros: Registros brutos do JSONL (para checar integridade).
            questoes: Questões convertidas.
            perfis: Perfil de cada questão (mesma ordem de ``questoes``).
            perfilador: Usado para obter o texto limpo das questões.
            processador: Limpeza e normalização de texto.
            legislacao: Catálogo de leis.
            estatisticas: Cálculos descritivos.
            parametros: Limiares e listas da EDA.
        """
        self._registros: Sequence[RegistroBruto] = registros
        self._questoes: Sequence[Questao] = questoes
        self._perfis: Sequence[PerfilQuestao] = perfis
        self._processador: ProcessadorTexto = processador
        self._legislacao: MapaLegislacao = legislacao
        self._estatisticas: CalculadoraEstatisticas = estatisticas
        self._parametros: ParametrosEDA = parametros
        self._total: int = len(questoes)
        self._limpos: dict[str, TextoLimpo] = {questao.id: perfilador.limpar(questao) for questao in questoes}

    def executar(self) -> list[Secao]:
        """Roda todas as análises de questões.

        Returns:
            Seções na ordem de exibição.
        """
        return [
            self._integridade(),
            self._formato(),
            self._ruido_html(),
            self._tamanhos(),
            self._comando(),
            self._enunciados_genericos(),
            self._repeticoes(),
            self._origem(),
            self._legislacao_citada(),
        ]

    def _pct(self, parte: int) -> float:
        """Porcentagem em relação ao total de questões.

        Args:
            parte: Quantidade.

        Returns:
            Porcentagem com uma casa decimal.
        """
        return self._estatisticas.percentual(parte, self._total)

    @staticmethod
    def _milhar(valor: float) -> str:
        """Formata um número inteiro com ponto como separador de milhar.

        Args:
            valor: Número a formatar.

        Returns:
            Texto no formato brasileiro (``443.917``).
        """
        return f"{valor:,.0f}".replace(",", ".")

    def _trecho(self, texto: str) -> str:
        """Trecho curto para tabelas.

        Args:
            texto: Texto completo.

        Returns:
            Trecho de uma linha.
        """
        return self._processador.trecho(texto, self._parametros.chars_trecho)

    @staticmethod
    def _vazio(valor: object) -> bool:
        """Indica se um valor bruto está vazio (``None``, texto em branco, coleção vazia).

        Args:
            valor: Valor bruto.

        Returns:
            ``True`` se vazio.
        """
        if valor is None:
            return True
        if isinstance(valor, str):
            return not valor.strip()
        if isinstance(valor, (dict, list)):
            return not valor
        return False

    def _integridade(self) -> Secao:
        """Checa IDs, campos ausentes ou vazios e alternativas vazias.

        Returns:
            Seção de integridade.
        """
        ids: list[str] = [str(registro.get("id", "")) for registro in self._registros]
        contagem_ids: Counter[str] = Counter(ids)
        repetidos: list[str] = sorted(identificador for identificador, n in contagem_ids.items() if n > 1)
        fora_padrao: list[str] = [identificador for identificador in ids if not self._RE_ID.fullmatch(identificador)]
        esperados: set[str] = set(CarregadorDados.CAMPOS_QUESTAO)
        extras: Counter[str] = Counter(
            chave for registro in self._registros for chave in registro if chave not in esperados
        )
        linhas: list[list[Celula]] = []
        campo: str
        for campo in CarregadorDados.CAMPOS_QUESTAO:
            ausentes: int = sum(1 for registro in self._registros if campo not in registro)
            vazios: int = sum(1 for registro in self._registros if campo in registro and self._vazio(registro[campo]))
            linhas.append([campo, ausentes, vazios, self._pct(vazios)])
        alternativas_vazias: int = sum(
            1 for questao in self._questoes for texto in self._limpos[questao.id].alternativas.values() if not texto
        )
        secao: Secao = Secao("Questões: integridade dos dados")
        secao.achados = [
            (
                f"{len(self._registros)} registros, {len(contagem_ids)} IDs únicos; "
                f"{len(repetidos)} IDs repetidos; {len(fora_padrao)} fora do padrão Q0000."
            ),
            "Campos fora do esquema: " + (", ".join(f"{chave} ({n})" for chave, n in extras.items()) or "nenhum") + ".",
            f"Alternativas vazias depois da limpeza: {alternativas_vazias}.",
            "Campos vazios não são erro de leitura: o `comando` vazio é comum e o assunto de origem às vezes falta.",
        ]
        secao.tabelas = [Tabela("campos", "Campos ausentes e vazios", ["campo", "ausente", "vazio", "% vazio"], linhas)]
        secao.metricas = {
            "registros": len(self._registros),
            "ids_unicos": len(contagem_ids),
            "ids_repetidos": len(repetidos),
            "ids_fora_padrao": len(fora_padrao),
            "alternativas_vazias": alternativas_vazias,
        }
        return secao

    def _formato(self) -> Secao:
        """Distribuição dos formatos e das letras das alternativas.

        Returns:
            Seção de formato.
        """
        formatos: Counter[str] = Counter(perfil.formato for perfil in self._perfis)
        letras: Counter[str] = Counter(",".join(sorted(questao.alternativas)) for questao in self._questoes)
        linhas_formato: list[list[Celula]] = [[nome, n, self._pct(n)] for nome, n in formatos.most_common()]
        linhas_letras: list[list[Celula]] = [[nome or "(nenhuma)", n, self._pct(n)] for nome, n in letras.most_common()]
        secao: Secao = Secao("Questões: formato")
        secao.achados = [
            (
                f"{formatos['multipla_escolha_5']} de múltipla escolha com 5 alternativas, "
                f"{formatos['multipla_escolha_4']} com 4 e {formatos['certo_errado']} de certo/errado."
            ),
            "Nas de certo/errado as alternativas ('Certo'/'Errado') não dizem nada: o assunto está só no enunciado.",
        ]
        secao.tabelas = [
            Tabela("formatos", "Formatos", ["formato", "n", "%"], linhas_formato),
            Tabela("letras_alternativas", "Letras das alternativas", ["letras", "n", "%"], linhas_letras),
        ]
        secao.metricas = {nome: n for nome, n in formatos.items()}
        return secao

    def _ruido_html(self) -> Secao:
        """Mede tags, entidades e quebras de linha nos campos.

        Returns:
            Seção de ruído de HTML.
        """
        ocorrencias: Counter[str] = Counter()
        questoes_com_tag: Counter[str] = Counter()
        questao: Questao
        for questao in self._questoes:
            tags: list[str] = self._processador.nomes_tags(questao.enunciado_html) + self._processador.nomes_tags(
                questao.comando
            )
            texto: str
            for texto in questao.alternativas.values():
                tags.extend(self._processador.nomes_tags(texto))
            ocorrencias.update(tags)
            questoes_com_tag.update(set(tags))
        entidades: Counter[str] = Counter(
            entidade
            for questao in self._questoes
            for campo in [questao.enunciado_html, questao.comando, *questao.alternativas.values()]
            for entidade in self._processador.entidades(campo)
        )
        alt_html: int = sum(perfil.alternativas_com_html for perfil in self._perfis)
        alt_quebra: int = sum(perfil.alternativas_com_quebra for perfil in self._perfis)
        questoes_alt_quebra: int = sum(1 for perfil in self._perfis if perfil.alternativas_com_quebra)
        comando_so_html: int = sum(1 for perfil in self._perfis if perfil.comando_so_html)
        editor: list[PerfilQuestao] = [perfil for perfil in self._perfis if perfil.html_de_editor]
        brutos: int = sum(perfil.chars_brutos for perfil in self._perfis)
        limpos: int = sum(perfil.chars_total for perfil in self._perfis)
        brutos_editor: int = sum(perfil.chars_brutos for perfil in editor)
        midia: list[str] = sorted(set(ocorrencias) & {"img", "table", "iframe", "object", "svg"})
        maior_reducao: list[PerfilQuestao] = sorted(
            self._perfis, key=lambda perfil: perfil.chars_brutos - perfil.chars_total, reverse=True
        )[:10]
        linhas_reducao: list[list[Celula]] = [
            [
                perfil.id,
                perfil.chars_brutos,
                perfil.chars_total,
                self._estatisticas.percentual(perfil.chars_brutos - perfil.chars_total, perfil.chars_brutos),
                "sim" if perfil.html_de_editor else "não",
            ]
            for perfil in maior_reducao
        ]
        linhas_tags: list[list[Celula]] = [[tag, n, questoes_com_tag[tag]] for tag, n in ocorrencias.most_common()]
        linhas_entidades: list[list[Celula]] = [[entidade, n] for entidade, n in entidades.most_common()]
        secao: Secao = Secao("Questões: ruído de HTML e formatação")
        secao.achados = [
            f"Tags encontradas: {', '.join(f'<{tag}> ({n})' for tag, n in ocorrencias.most_common())}. "
            + (
                f"Há mídia/tabela: {', '.join(midia)}."
                if midia
                else "Nenhuma imagem ou tabela: o conteúdo é todo textual."
            ),
            (
                f"Questões com HTML colado do Word: {len(editor)} ({', '.join(perfil.id for perfil in editor) or 'nenhuma'}), "
                f"somando {self._milhar(brutos_editor)} caracteres brutos ({self._estatisticas.percentual(brutos_editor, brutos)}% "
                "de todo o HTML do recorte), quase tudo CSS e metadados que a limpeza descarta."
            ),
            (
                f"Antes da limpeza o recorte tem {self._milhar(brutos)} caracteres; depois, {self._milhar(limpos)}. "
                "Mandar o HTML cru para um modelo pagaria tokens de lixo."
            ),
            (
                f"{alt_html} alternativas têm HTML ou entidades; {alt_quebra} alternativas "
                f"({questoes_alt_quebra} questões) têm quebra de linha no meio da frase (texto colado de PDF)."
            ),
            f"{comando_so_html} comandos contêm só HTML (ex.: `<br>`) e ficam vazios depois da limpeza.",
            "Conclusão: uma limpeza simples (quebras, tags, entidades e espaços) basta; não há perda de conteúdo.",
        ]
        secao.tabelas = [
            Tabela("tags_html", "Tags HTML", ["tag", "ocorrências", "questões"], linhas_tags),
            Tabela("entidades_html", "Entidades HTML", ["entidade", "ocorrências"], linhas_entidades),
            Tabela(
                "maior_reducao_limpeza",
                "Questões que mais encolhem na limpeza",
                ["id", "caracteres brutos", "caracteres limpos", "% removido", "HTML de editor"],
                linhas_reducao,
            ),
        ]
        secao.metricas = {
            "alternativas_com_html": alt_html,
            "alternativas_com_quebra": alt_quebra,
            "comandos_so_html": comando_so_html,
            "entidades": sum(entidades.values()),
            "questoes_html_de_editor": len(editor),
            "caracteres_brutos": brutos,
            "caracteres_limpos": limpos,
        }
        return secao

    def _tamanhos(self) -> Secao:
        """Distribuição de tamanho (em caracteres) de cada parte da questão.

        Returns:
            Seção de tamanhos.
        """
        medidas: dict[str, list[float]] = {
            "enunciado (caracteres)": [float(perfil.chars_enunciado) for perfil in self._perfis],
            "comando (caracteres)": [float(perfil.chars_comando) for perfil in self._perfis],
            "alternativas (caracteres)": [float(perfil.chars_alternativas) for perfil in self._perfis],
            "total (caracteres)": [float(perfil.chars_total) for perfil in self._perfis],
            "palavras de conteúdo no enunciado": [float(perfil.palavras_conteudo_enunciado) for perfil in self._perfis],
        }
        linhas: list[list[Celula]] = [
            self._estatisticas.resumir(valores).como_linha(nome) for nome, valores in medidas.items()
        ]
        total: float = sum(medidas["total (caracteres)"])
        mais_longas: list[PerfilQuestao] = sorted(self._perfis, key=lambda perfil: perfil.chars_total, reverse=True)[
            :10
        ]
        linhas_longas: list[list[Celula]] = [
            [perfil.id, perfil.formato, perfil.chars_total, self._trecho(self._limpos[perfil.id].enunciado)]
            for perfil in mais_longas
        ]
        secao: Secao = Secao("Questões: tamanho do texto")
        secao.achados = [
            (
                f"Texto total: mediana de {self._estatisticas.resumir(medidas['total (caracteres)']).mediana:.0f} "
                f"caracteres por questão; {self._milhar(total)} caracteres no recorte (cerca de {self._milhar(total / 4)} tokens)."
            ),
            "As alternativas costumam ter mais texto que o enunciado: o classificador precisa recebê-las sempre.",
        ]
        secao.tabelas = [
            Tabela("tamanhos", "Distribuição de tamanho", list(CalculadoraEstatisticas.COLUNAS_RESUMO), linhas),
            Tabela("mais_longas", "Questões mais longas", ["id", "formato", "caracteres", "enunciado"], linhas_longas),
        ]
        secao.metricas = {"caracteres_total": int(total), "tokens_estimados": int(total / 4)}
        return secao

    def _comando(self) -> Secao:
        """Classifica os comandos e mostra os suspeitos de terem sido gerados.

        Returns:
            Seção sobre o campo ``comando``.
        """
        tipos: Counter[str] = Counter(perfil.tipo_comando for perfil in self._perfis)
        exemplos: dict[str, list[str]] = defaultdict(list)
        perfil: PerfilQuestao
        for perfil in self._perfis:
            exemplos[perfil.tipo_comando].append(perfil.id)
        primeiras: Counter[str] = Counter(
            self._processador.tokens(limpo.comando)[0]
            for limpo in self._limpos.values()
            if self._processador.tokens(limpo.comando)
        )
        linhas_tipos: list[list[Celula]] = [
            [tipo, n, self._pct(n), ", ".join(exemplos[tipo][:6])] for tipo, n in tipos.most_common()
        ]
        linhas_primeiras: list[list[Celula]] = [[palavra, n] for palavra, n in primeiras.most_common(20)]
        linhas_suspeitos: list[list[Celula]] = [
            [
                perfil.id,
                perfil.formato,
                self._trecho(self._limpos[perfil.id].comando),
                self._trecho(self._limpos[perfil.id].enunciado),
            ]
            for perfil in self._perfis
            if perfil.tipo_comando == "suspeito"
        ]
        suspeitos_ce: int = sum(
            1 for perfil in self._perfis if perfil.tipo_comando == "suspeito" and perfil.formato == "certo_errado"
        )
        secao: Secao = Secao("Questões: o campo `comando`")
        secao.achados = [
            (
                f"{tipos['vazio']} comandos vazios ({self._pct(tipos['vazio'])}%), {tipos['util']} úteis, "
                f"{tipos['suspeito']} suspeitos e {tipos['repete_enunciado']} que só repetem o enunciado."
            ),
            (
                f"Os suspeitos pedem algo que não cabe em questão objetiva ('Explique...', 'Complete a frase...'); "
                f"{suspeitos_ce} deles estão em questões de certo/errado. Parecem gerados por outra ferramenta."
            ),
            "Decisão para o passo 01: usar o comando só quando for útil; suspeito ou repetido fica fora do texto do modelo.",
        ]
        secao.tabelas = [
            Tabela("tipos_comando", "Tipos de comando", ["tipo", "n", "%", "exemplos"], linhas_tipos),
            Tabela("primeira_palavra_comando", "Primeira palavra do comando", ["palavra", "n"], linhas_primeiras),
            Tabela(
                "comandos_suspeitos", "Comandos suspeitos", ["id", "formato", "comando", "enunciado"], linhas_suspeitos
            ),
        ]
        secao.metricas = {f"comando_{tipo}": n for tipo, n in tipos.items()}
        return secao

    def _enunciados_genericos(self) -> Secao:
        """Separa enunciados genéricos (sem assunto) de enunciados apenas curtos.

        Returns:
            Seção sobre enunciados genéricos.
        """
        genericos: list[PerfilQuestao] = [perfil for perfil in self._perfis if perfil.enunciado_generico]
        curtos: list[PerfilQuestao] = [perfil for perfil in self._perfis if perfil.enunciado_curto]
        curtos_especificos: list[PerfilQuestao] = [perfil for perfil in curtos if not perfil.enunciado_generico]
        linhas_genericos: list[list[Celula]] = [
            [perfil.id, perfil.formato, self._trecho(self._limpos[perfil.id].enunciado), perfil.assunto_origem]
            for perfil in genericos
        ]
        linhas_curtos: list[list[Celula]] = [
            [perfil.id, perfil.palavras_conteudo_enunciado, self._trecho(self._limpos[perfil.id].enunciado)]
            for perfil in curtos_especificos
        ]
        secao: Secao = Secao("Questões: enunciados genéricos")
        secao.achados = [
            (
                f"{len(genericos)} enunciados genéricos (nenhuma palavra de conteúdo, ex.: 'Assinale a alternativa correta'): "
                "o assunto está inteiro nas alternativas, que podem cobrir mais de um tema."
            ),
            (
                f"{len(curtos)} enunciados têm menos de {self._parametros.limiar_enunciado_curto} caracteres, "
                f"mas {len(curtos_especificos)} deles são específicos ('A remição', 'A prisão preventiva'): "
                "tamanho não é critério; conteúdo é."
            ),
        ]
        secao.tabelas = [
            Tabela(
                "enunciados_genericos",
                "Enunciados genéricos",
                ["id", "formato", "enunciado", "assunto de origem"],
                linhas_genericos,
            ),
            Tabela(
                "curtos_especificos",
                "Curtos, mas específicos",
                ["id", "palavras de conteúdo", "enunciado"],
                linhas_curtos,
            ),
        ]
        secao.metricas = {
            "genericos": len(genericos),
            "curtos": len(curtos),
            "curtos_especificos": len(curtos_especificos),
        }
        return secao

    def _repeticoes(self) -> Secao:
        """Procura enunciados idênticos e questões duplicadas.

        Returns:
            Seção de repetições.
        """
        por_enunciado: dict[str, list[str]] = defaultdict(list)
        por_completo: dict[str, list[str]] = defaultdict(list)
        perfil: PerfilQuestao
        for perfil in self._perfis:
            por_enunciado[perfil.hash_enunciado].append(perfil.id)
            por_completo[perfil.hash_completo].append(perfil.id)
        grupos_enunciado: list[list[str]] = sorted(
            (ids for ids in por_enunciado.values() if len(ids) > 1), key=len, reverse=True
        )
        grupos_completo: list[list[str]] = [ids for ids in por_completo.values() if len(ids) > 1]
        linhas_enunciado: list[list[Celula]] = [
            [len(ids), ", ".join(ids), self._trecho(self._limpos[ids[0]].enunciado)] for ids in grupos_enunciado
        ]
        linhas_completo: list[list[Celula]] = [
            [len(ids), ", ".join(ids), self._trecho(self._limpos[ids[0]].enunciado)] for ids in grupos_completo
        ]
        secao: Secao = Secao("Questões: repetições")
        secao.achados = [
            (
                f"{len(grupos_enunciado)} grupos de enunciado idêntico, somando "
                f"{sum(len(ids) for ids in grupos_enunciado)} questões."
            ),
            f"{len(grupos_completo)} grupos de questões idênticas (enunciado e alternativas).",
            "Enunciado igual não significa questão igual: deduplicar só pelo texto completo.",
        ]
        secao.tabelas = [
            Tabela("enunciados_repetidos", "Enunciados idênticos", ["n", "ids", "enunciado"], linhas_enunciado),
            Tabela("questoes_duplicadas", "Questões idênticas", ["n", "ids", "enunciado"], linhas_completo),
        ]
        secao.metricas = {"grupos_enunciado_igual": len(grupos_enunciado), "grupos_questao_igual": len(grupos_completo)}
        return secao

    def _origem(self) -> Secao:
        """Analisa disciplina e assunto de origem.

        Returns:
            Seção sobre os rótulos de origem.
        """
        disciplinas: Counter[str] = Counter(perfil.disciplina_origem for perfil in self._perfis)
        linhas_disciplinas: list[list[Celula]] = [
            [
                nome or "(vazio)",
                self._parametros.mapa_disciplinas.get(nome, "") or "(fora do recorte)",
                n,
                self._pct(n),
            ]
            for nome, n in disciplinas.most_common()
        ]
        fora: list[PerfilQuestao] = [perfil for perfil in self._perfis if not perfil.origem_no_recorte]
        linhas_fora: list[list[Celula]] = [
            [
                perfil.id,
                perfil.disciplina_origem or "(vazio)",
                perfil.assunto_origem or "(vazio)",
                self._trecho(self._limpos[perfil.id].enunciado),
            ]
            for perfil in fora
        ]
        assuntos: Counter[str] = Counter(perfil.assunto_origem for perfil in self._perfis)
        assuntos_sem_parte: Counter[str] = Counter(
            perfil.assunto_sem_parte for perfil in self._perfis if perfil.assunto_sem_parte
        )
        vazios: int = assuntos[""]
        com_parte: int = sum(1 for perfil in self._perfis if perfil.assunto_tem_parte)
        multiplos: int = sum(1 for perfil in self._perfis if perfil.assunto_multiplo)
        linhas_assuntos: list[list[Celula]] = [
            [nome or "(vazio)", n, self._pct(n)] for nome, n in assuntos.most_common()
        ]
        secao: Secao = Secao("Questões: disciplina e assunto de origem")
        secao.achados = [
            (
                f"{len(disciplinas)} nomes de disciplina de origem; {len(fora)} questões vêm de disciplinas fora do recorte "
                "(Tributário, Constitucional, Civil, Ambiental, vazio...). Isso é sinal, não decisão: várias são penais de fato."
            ),
            "A mesma disciplina aparece com nomes diferentes ('Penal' e 'Direito Penal').",
            (
                f"{len(assuntos)} assuntos distintos ({len(assuntos_sem_parte)} sem o marcador '(Parte N)'); "
                f"{vazios} questões sem assunto, {com_parte} com '(Parte N)' e {multiplos} com mais de um assunto."
            ),
            (
                "Os assuntos de origem vêm do site de onde as questões foram importadas e podem estar errados: "
                "servem só como sinal fraco e como baseline (ver análise cruzada)."
            ),
        ]
        secao.tabelas = [
            Tabela(
                "disciplinas_origem",
                "Disciplinas de origem",
                ["disciplina de origem", "disciplina na árvore", "n", "%"],
                linhas_disciplinas,
            ),
            Tabela(
                "fora_do_recorte",
                "Questões de disciplinas fora do recorte",
                ["id", "disciplina", "assunto", "enunciado"],
                linhas_fora,
            ),
            Tabela("assuntos_origem", "Assuntos de origem", ["assunto", "n", "%"], linhas_assuntos),
        ]
        secao.metricas = {
            "disciplinas_origem": len(disciplinas),
            "fora_do_recorte": len(fora),
            "assuntos_distintos": len(assuntos),
            "assuntos_vazios": vazios,
            "assuntos_com_parte": com_parte,
            "assuntos_multiplos": multiplos,
        }
        return secao

    def _legislacao_citada(self) -> Secao:
        """Conta leis e diplomas citados nas questões.

        Returns:
            Seção sobre legislação citada.
        """
        leis: Counter[str] = Counter(numero for perfil in self._perfis for numero in perfil.leis_citadas)
        linhas: list[list[Celula]] = []
        numero: str
        n: int
        for numero, n in leis.most_common():
            lei: LeiConhecida | None = self._legislacao.lei(numero)
            linhas.append(
                [
                    numero,
                    lei.nome if lei is not None else "(não catalogada)",
                    n,
                    ", ".join(lei.temas) if lei is not None else "",
                ]
            )
        com_lei: int = sum(1 for perfil in self._perfis if perfil.leis_citadas)
        referencias: dict[str, int] = {
            "Código Penal": sum(1 for perfil in self._perfis if perfil.menciona_cp),
            "Código de Processo Penal": sum(1 for perfil in self._perfis if perfil.menciona_cpp),
            "Constituição": sum(1 for perfil in self._perfis if perfil.menciona_cf),
            "Jurisprudência (STF, STJ, súmula)": sum(1 for perfil in self._perfis if perfil.menciona_jurisprudencia),
            "Alguma lei (número ou apelido)": com_lei,
        }
        linhas_referencias: list[list[Celula]] = [[nome, n, self._pct(n)] for nome, n in referencias.items()]
        secao: Secao = Secao("Questões: legislação e referências citadas")
        secao.achados = [
            f"{com_lei} questões ({self._pct(com_lei)}%) citam alguma lei por número ou apelido.",
            (
                f"{referencias['Jurisprudência (STF, STJ, súmula)']} questões citam jurisprudência: tendem a ser mais "
                "difíceis de classificar, porque o tema vem do caso julgado, não de um artigo."
            ),
            "Os temas indicados por lei são um sinal fraco (passo 03): a mesma lei pode ser cobrada em mais de um tema.",
        ]
        secao.tabelas = [
            Tabela("referencias", "Referências citadas", ["referência", "questões", "%"], linhas_referencias),
            Tabela("leis_citadas", "Leis citadas", ["lei", "nome", "questões", "temas indicados"], linhas),
        ]
        secao.metricas = {"questoes_com_lei": com_lei, **{nome: n for nome, n in referencias.items()}}
        return secao
