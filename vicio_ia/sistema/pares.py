"""Candidatos e atributos dos pares (questão, tema) do ranqueador (ADR-022), só a partir de artefatos.

Os candidatos de uma questão são a união dos mais bem colocados no denso e no BM25, dos temas apontados pelo mapa
de artigos e pelos termos ``forte``, e dos pais dos subtemas candidatos (assim o recuo para o pai pode ser
escolhido). Cada par recebe 20 atributos. O último, o kNN na folha, depende de quais questões rotuladas estão
disponíveis e é recalculado em cada partição da validação cruzada, para não usar o rótulo da própria questão.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import numpy as np

from vicio_ia.configuracao import Caminhos, ParametrosEDA, ParametrosSistema
from vicio_ia.enriquecimento.citacoes import ArquivoCitacoes, ArtigoCitado, CitacoesQuestao
from vicio_ia.estatistica import Matriz
from vicio_ia.preparacao.arvore_preparada import TemaPreparado
from vicio_ia.preparacao.leitura import LeitorPreparados
from vicio_ia.preparacao.texto_canonico import QuestaoPreparada
from vicio_ia.sistema.base_temas import ArquivoBaseTemas, TemaBase, TermoTema
from vicio_ia.sistema.documentos import DocumentoTema, MontadorDocumentos
from vicio_ia.sistema.folha import LeitorFolha, RotuloFolha
from vicio_ia.sistema.lexical import IndiceBM25, TokenizadorLexical
from vicio_ia.sistema.mapa_artigos import MapaArtigos
from vicio_ia.sistema.vetores import ArquivoVetores, ConjuntoVetores, VetoresConhecimento
from vicio_ia.texto import ProcessadorTexto


@dataclass(frozen=True)
class DadosSistema:
    """Tudo o que a fase de decisão lê do disco.

    Attributes:
        questoes: As 659 questões preparadas.
        temas: Árvore preparada.
        base: Base de temas (ADR-020), na ordem dos vetores de tema.
        vetores: Vetores do modelo escolhido (ADR-021).
        citacoes: Citações por questão.
        mapa: Mapa de artigos revisado.
        folha: Folha-verdade.
    """

    questoes: tuple[QuestaoPreparada, ...]
    temas: tuple[TemaPreparado, ...]
    base: tuple[TemaBase, ...]
    vetores: VetoresConhecimento
    citacoes: Mapping[str, CitacoesQuestao]
    mapa: MapaArtigos
    folha: tuple[RotuloFolha, ...]


class CarregadorSistema:
    """Lê os artefatos versionados da fase de conhecimento."""

    def __init__(self, caminhos: Caminhos) -> None:
        """Guarda os caminhos.

        Args:
            caminhos: Caminhos do projeto.
        """
        self._caminhos: Caminhos = caminhos

    def carregar(self) -> DadosSistema:
        """Lê tudo.

        Returns:
            Dados do sistema.

        Raises:
            ValueError: Se a base de temas e os vetores de tema não estiverem na mesma ordem.
        """
        leitor: LeitorPreparados = LeitorPreparados(self._caminhos)
        questoes: list[QuestaoPreparada] = leitor.questoes()
        temas: list[TemaPreparado] = leitor.temas()
        pasta: Path = self._caminhos.dados_conhecimento
        base: list[TemaBase] = ArquivoBaseTemas(pasta / "temas.jsonl").ler()
        vetores: VetoresConhecimento = ArquivoVetores(pasta / "embeddings").ler()
        if tuple(t.tema_id for t in base) != vetores.temas.ids:
            raise ValueError("a base de temas e os vetores de tema estão em ordens diferentes")
        return DadosSistema(
            questoes=tuple(questoes),
            temas=tuple(temas),
            base=tuple(base),
            vetores=vetores,
            citacoes=ArquivoCitacoes(pasta / "citacoes.jsonl").ler(),
            mapa=MapaArtigos.ler(pasta / "mapa_artigos.csv"),
            folha=tuple(LeitorFolha(self._caminhos.folha_verdade, temas, {q.id for q in questoes}).ler()),
        )


@dataclass(frozen=True)
class ParesQuestao:
    """Candidatos de uma questão e os atributos fixos de cada par.

    Attributes:
        id: ID da questão.
        candidatos: Temas candidatos, do mais ao menos similar no denso.
        atributos: Uma linha por candidato, sem a coluna de kNN.
    """

    id: str
    candidatos: tuple[str, ...]
    atributos: Matriz


class GeradorPares:
    """Monta os candidatos e os atributos de todas as questões."""

    NOMES: ClassVar[tuple[str, ...]] = (
        "similaridade densa",
        "distância ao melhor denso",
        "1 / posição no denso",
        "melhor denso no ramo − melhor denso",
        "BM25 relativo ao melhor",
        "1 / posição no BM25",
        "artigo citado no mapa do tema",
        "artigo citado no mapa do ramo",
        "lei citada nas referências do tema",
        "termos fortes presentes",
        "termos fracos presentes",
        "termo exclui do tema presente",
        "termo exclui de outro tema apontando para este",
        "alternativas cujo melhor tema está no ramo",
        "tema de nível 1",
        "tema lixeira",
        "assunto de origem casa com o ramo",
        "exemplos sintéticos do tema − melhor exemplo",
        "exemplos sintéticos do ramo − melhor exemplo",
        "kNN: vizinhos rotulados no ramo",
    )

    def __init__(self, dados: DadosSistema, parametros: ParametrosSistema) -> None:
        """Pré-calcula as similaridades, o BM25, os ramos e os termos presentes.

        Args:
            dados: Dados do sistema.
            parametros: Parâmetros do sistema.
        """
        self._dados: DadosSistema = dados
        self._parametros: ParametrosSistema = parametros
        self._processador: ProcessadorTexto = ProcessadorTexto()
        self._ids_temas: tuple[str, ...] = tuple(t.tema_id for t in dados.base)
        self._coluna: dict[str, int] = {t: k for k, t in enumerate(self._ids_temas)}
        self._por_id: dict[str, TemaBase] = {t.tema_id: t for t in dados.base}
        self._ramo: dict[str, frozenset[str]] = {t.tema_id: self._calcular_ramo(t) for t in dados.base}
        ids: list[str] = [q.id for q in dados.questoes]
        self._linha: dict[str, int] = {i: k for k, i in enumerate(ids)}
        questoes_v: Matriz = dados.vetores.questoes.submatriz(ids)
        self._denso: Matriz = questoes_v @ dados.vetores.temas.matriz.T
        self._similaridade_questoes: Matriz = questoes_v @ questoes_v.T
        self._bm25: Matriz = self._calcular_bm25()
        self._exemplos: Matriz = self._calcular_exemplos(questoes_v)
        self._rotulos: dict[str, RotuloFolha] = {r.id: r for r in dados.folha}
        self._lixeiras: frozenset[str] = frozenset(t.tema_id for t in dados.temas if t.lixeira)

    @property
    def ids_temas(self) -> tuple[str, ...]:
        """Temas publicáveis, na ordem das colunas."""
        return self._ids_temas

    def ramo(self, tema_id: str) -> frozenset[str]:
        """O próprio tema, o pai publicável e os filhos publicáveis.

        Args:
            tema_id: Tema.

        Returns:
            IDs do ramo.
        """
        return self._ramo[tema_id]

    def _calcular_ramo(self, tema: TemaBase) -> frozenset[str]:
        """Ramo de um tema, só com publicáveis.

        Args:
            tema: Registro do tema.

        Returns:
            IDs do ramo.
        """
        publicaveis: set[str] = {t.tema_id for t in self._dados.base}
        membros: set[str] = {tema.tema_id, *tema.filhos}
        if tema.pai in publicaveis:
            membros.add(tema.pai)
        return frozenset(membros)

    def _calcular_bm25(self) -> Matriz:
        """Pontuação BM25 de todas as questões contra os documentos de tema.

        Returns:
            Matriz questões × temas.
        """
        p: ParametrosSistema = self._parametros
        documentos: list[DocumentoTema] = MontadorDocumentos.documentos_base(self._dados.base, p.documento_tema_bm25)
        tokenizador: TokenizadorLexical = TokenizadorLexical(self._processador, ParametrosEDA().palavras_sem_conteudo)
        indice: IndiceBM25 = IndiceBM25([tokenizador.termos(d.texto) for d in documentos], p.bm25_k1, p.bm25_b)
        return np.array(
            [indice.pontuar(tokenizador.termos(MontadorDocumentos.texto_questao(q))) for q in self._dados.questoes],
            dtype=np.float64,
        )

    def _calcular_exemplos(self, questoes_v: Matriz) -> Matriz:
        """Similaridade de cada questão com o exemplo sintético mais parecido de cada tema (E13).

        Args:
            questoes_v: Vetores das questões, na ordem das questões.

        Returns:
            Matriz questões × temas (0 em tudo se não houver exemplos).
        """
        exemplos: ConjuntoVetores = self._dados.vetores.exemplos
        maximos: Matriz = np.zeros((questoes_v.shape[0], len(self._ids_temas)), dtype=np.float64)
        if not exemplos.ids:
            return maximos
        maximos.fill(-1.0)
        similaridade: Matriz = questoes_v @ exemplos.matriz.T
        coluna: int
        id_exemplo: str
        for coluna, id_exemplo in enumerate(exemplos.ids):
            tema: str = id_exemplo.rsplit(":", 1)[0]
            if tema in self._coluna:
                destino: int = self._coluna[tema]
                maximos[:, destino] = np.maximum(maximos[:, destino], similaridade[:, coluna])
        return maximos

    def pares(self) -> dict[str, ParesQuestao]:
        """Candidatos e atributos fixos de todas as questões.

        Returns:
            Pares por ID da questão.
        """
        return {q.id: self._pares_questao(q) for q in self._dados.questoes}

    def _pares_questao(self, questao: QuestaoPreparada) -> ParesQuestao:
        """Candidatos e atributos de uma questão.

        Args:
            questao: Questão.

        Returns:
            Pares da questão.
        """
        linha: int = self._linha[questao.id]
        denso: Matriz = self._denso[linha]
        bm25: Matriz = self._bm25[linha]
        k: int = self._parametros.candidatos_por_fonte
        ordem_denso: list[int] = [int(i) for i in np.argsort(-denso, kind="stable")]
        ordem_bm25: list[int] = [int(i) for i in np.argsort(-bm25, kind="stable")]
        posicao_denso: dict[str, int] = {self._ids_temas[c]: p + 1 for p, c in enumerate(ordem_denso)}
        posicao_bm25: dict[str, int] = {self._ids_temas[c]: p + 1 for p, c in enumerate(ordem_bm25)}
        temas_mapa: set[str] = self._temas_mapa(questao.id)
        presentes: dict[str, tuple[int, int, bool]] = {}
        entrada_exclui: set[str] = set()
        self._termos_presentes(questao, presentes, entrada_exclui)
        candidatos: set[str] = {self._ids_temas[c] for c in ordem_denso[:k]} | {
            self._ids_temas[c] for c in ordem_bm25[:k]
        }
        candidatos |= temas_mapa & set(self._ids_temas)
        candidatos |= {t for t, (fortes, _, _) in presentes.items() if fortes > 0}
        candidatos |= {self._por_id[t].pai for t in list(candidatos) if self._por_id[t].pai in self._coluna}
        ordenados: tuple[str, ...] = tuple(sorted(candidatos, key=lambda t: posicao_denso[t]))
        melhor_denso: float = float(denso.max())
        melhor_bm25: float = float(bm25.max())
        exemplos: Matriz = self._exemplos[linha]
        melhor_exemplo: float = float(exemplos.max())
        alternativas: list[str] = self._melhores_alternativas(questao)
        leis: set[str] = {MapaArtigos.chave_lei(a.lei) for a in self._citacoes(questao.id)}
        origem: str = self._processador.normalizar(str(questao.original.get("assunto_origem") or ""))
        linhas: list[list[float]] = []
        tema: str
        for tema in ordenados:
            registro: TemaBase = self._por_id[tema]
            ramo: frozenset[str] = self._ramo[tema]
            fortes: int
            fracos: int
            sai: bool
            fortes, fracos, sai = presentes.get(tema, (0, 0, False))
            linhas.append(
                [
                    float(denso[self._coluna[tema]]),
                    float(denso[self._coluna[tema]]) - melhor_denso,
                    1.0 / posicao_denso[tema],
                    max(float(denso[self._coluna[t]]) for t in ramo) - melhor_denso,
                    float(bm25[self._coluna[tema]]) / melhor_bm25 if melhor_bm25 > 0 else 0.0,
                    1.0 / posicao_bm25[tema],
                    1.0 if tema in temas_mapa else 0.0,
                    1.0 if (ramo - {tema}) & temas_mapa else 0.0,
                    1.0 if leis & {MapaArtigos.chave_lei(r.lei) for r in registro.referencias} else 0.0,
                    float(min(fortes, 3)),
                    min(fracos, 5) / 5.0,
                    1.0 if sai else 0.0,
                    1.0 if tema in entrada_exclui else 0.0,
                    sum(1 for a in alternativas if a in ramo) / len(alternativas) if alternativas else 0.0,
                    1.0 if registro.nivel == 1 else 0.0,
                    1.0 if self._lixeira(tema) else 0.0,
                    1.0 if origem and any(self._casa_origem(origem, t) for t in ramo) else 0.0,
                    float(exemplos[self._coluna[tema]]) - melhor_exemplo,
                    max(float(exemplos[self._coluna[t]]) for t in ramo) - melhor_exemplo,
                ]
            )
        return ParesQuestao(questao.id, ordenados, np.array(linhas, dtype=np.float64))

    def _citacoes(self, questao_id: str) -> list[ArtigoCitado]:
        """Artigos citados na questão.

        Args:
            questao_id: ID.

        Returns:
            Artigos com a lei resolvida.
        """
        citacao: CitacoesQuestao | None = self._dados.citacoes.get(questao_id)
        return list(citacao.artigos) if citacao else []

    def _temas_mapa(self, questao_id: str) -> set[str]:
        """Temas do mapa de artigos para os artigos citados.

        Args:
            questao_id: ID.

        Returns:
            IDs de tema.
        """
        citacao: CitacoesQuestao | None = self._dados.citacoes.get(questao_id)
        if citacao is None:
            return set()
        return {linha.tema_id for a in citacao.artigos for linha in self._dados.mapa.linhas(a.lei, a.inicio, a.fim)}

    def _termos_presentes(
        self, questao: QuestaoPreparada, presentes: dict[str, tuple[int, int, bool]], entrada_exclui: set[str]
    ) -> None:
        """Conta os termos de cada tema presentes na questão.

        Args:
            questao: Questão.
            presentes: Saída: ``tema -> (fortes, fracos, algum exclui do tema)``.
            entrada_exclui: Saída: temas apontados por um termo ``exclui`` presente.
        """
        texto: str = f" {self._processador.normalizar(MontadorDocumentos.texto_questao(questao))} "
        registro: TemaBase
        for registro in self._dados.base:
            fortes: int = 0
            fracos: int = 0
            sai: bool = False
            termo_tema: TermoTema
            for termo_tema in registro.termos:
                if not termo_tema.normalizado or f" {termo_tema.normalizado} " not in texto:
                    continue
                if termo_tema.tipo == "forte":
                    fortes += 1
                elif termo_tema.tipo == "fraco":
                    fracos += 1
                elif termo_tema.tipo == "exclui":
                    sai = True
                    if termo_tema.alvo:
                        entrada_exclui.add(termo_tema.alvo)
            if fortes or fracos or sai:
                presentes[registro.tema_id] = (fortes, fracos, sai)

    def _melhores_alternativas(self, questao: QuestaoPreparada) -> list[str]:
        """Melhor tema denso de cada alternativa.

        Args:
            questao: Questão.

        Returns:
            Um tema por alternativa (vazio em certo/errado).
        """
        ids: list[str] = [
            f"{questao.id}:{letra}"
            for letra in MontadorDocumentos.textos_alternativas(questao)
            if f"{questao.id}:{letra}" in self._dados.vetores.alternativas.ids
        ]
        if not ids:
            return []
        similaridade: Matriz = self._dados.vetores.alternativas.submatriz(ids) @ self._dados.vetores.temas.matriz.T
        return [self._ids_temas[int(np.argmax(linha))] for linha in similaridade]

    def _lixeira(self, tema_id: str) -> bool:
        """Diz se o tema é lixeira (D3).

        Args:
            tema_id: Tema.

        Returns:
            ``True`` se for lixeira.
        """
        return tema_id in self._lixeiras

    def _casa_origem(self, origem: str, tema_id: str) -> bool:
        """Diz se o assunto de origem e o título do tema contêm um ao outro (sinal fraco, ADR-006).

        Args:
            origem: Assunto de origem normalizado.
            tema_id: Tema.

        Returns:
            ``True`` se casarem.
        """
        titulo: str = self._processador.normalizar(self._por_id[tema_id].titulo)
        return len(titulo) >= 6 and len(origem) >= 6 and (titulo in origem or origem in titulo)

    def knn(self, questao_id: str, candidatos: Sequence[str], rotulados: Sequence[str]) -> Matriz:
        """Coluna de kNN: soma das similaridades dos vizinhos rotulados cujo alvo está no ramo do candidato.

        Args:
            questao_id: Questão.
            candidatos: Candidatos da questão.
            rotulados: Questões da folha disponíveis como vizinhas (a própria questão é sempre excluída).

        Returns:
            Uma linha por candidato, uma coluna.
        """
        disponiveis: list[str] = [r for r in rotulados if r != questao_id]
        coluna: Matriz = np.zeros((len(candidatos), 1), dtype=np.float64)
        if not disponiveis:
            return coluna
        linha: int = self._linha[questao_id]
        similaridade: Matriz = self._similaridade_questoes[linha, [self._linha[r] for r in disponiveis]]
        vizinho: int
        for vizinho in [int(v) for v in np.argsort(-similaridade, kind="stable")[: self._parametros.vizinhos_sistema]]:
            alvos: tuple[str, ...] = self._rotulos[disponiveis[vizinho]].alvos
            peso: float = max(float(similaridade[vizinho]), 0.0)
            indice: int
            candidato: str
            for indice, candidato in enumerate(candidatos):
                if self._ramo[candidato] & set(alvos):
                    coluna[indice, 0] += peso
        return coluna

    def matriz(self, pares: ParesQuestao, rotulados: Sequence[str]) -> Matriz:
        """Atributos completos de uma questão (os fixos e o kNN).

        Args:
            pares: Pares da questão.
            rotulados: Questões da folha disponíveis como vizinhas.

        Returns:
            Matriz candidatos × 20.
        """
        return np.hstack([pares.atributos, self.knn(pares.id, pares.candidatos, rotulados)])

    def concordancia(self, questao_id: str, tema_id: str) -> bool:
        """Faixa de evidência de concordância (ADR-025): o melhor tema do BM25 está no ramo do melhor tema do denso,
        e o nó escolhido também.

        Args:
            questao_id: Questão.
            tema_id: Nó escolhido.

        Returns:
            ``True`` se as duas representações concordam no ramo do nó.
        """
        linha: int = self._linha[questao_id]
        melhor_denso: str = self._ids_temas[int(np.argmax(self._denso[linha]))]
        melhor_bm25: str = self._ids_temas[int(np.argmax(self._bm25[linha]))]
        ramo: frozenset[str] = self._ramo[melhor_denso]
        return melhor_bm25 in ramo and tema_id in ramo

    def inativo_menos_maximo(self, questao_id: str) -> float:
        """Similaridade com o tema inativo mais próximo menos a similaridade máxima com os publicáveis (E11b).

        Args:
            questao_id: Questão.

        Returns:
            Diferença (maior = mais perto de um tema inativo).
        """
        vetor: Matriz = self._dados.vetores.questoes.submatriz([questao_id])[0]
        return float((self._dados.vetores.inativos.matriz @ vetor).max() - self._denso[self._linha[questao_id]].max())
