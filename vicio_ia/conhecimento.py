"""Conhecimento de domínio: leis do recorte e os temas que elas costumam indicar.

O mapeamento é um sinal fraco (uma questão pode citar a Lei de Drogas para
cobrar Processo Penal, por exemplo). Ele serve para a EDA medir quantas
questões trazem uma pista legislativa e, depois, como uma das regras do passo 03.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import ClassVar, Final

from vicio_ia.texto import ProcessadorTexto


@dataclass(frozen=True)
class LeiConhecida:
    """Uma lei relevante para o recorte e os temas candidatos que ela indica.

    Attributes:
        numero: Número da lei sem pontos nem ano (``"11340"``).
        nome: Nome usual da lei.
        temas: IDs de ``temas.csv`` que a lei costuma indicar (pode incluir nós
            duplicados, de propósito, para documentar a duplicidade).
        apelidos: Expressões normalizadas que citam a lei sem o número
            ("maria da penha", "lep").
    """

    numero: str
    nome: str
    temas: tuple[str, ...]
    apelidos: tuple[str, ...] = ()


LEIS_DO_RECORTE: Final[tuple[LeiConhecida, ...]] = (
    LeiConhecida("2848", "Código Penal", ()),
    LeiConhecida("3689", "Código de Processo Penal", ()),
    LeiConhecida("11340", "Lei Maria da Penha", ("4704", "6724"), ("maria da penha",)),
    LeiConhecida("11343", "Lei de Drogas", ("4708", "6728"), ("lei de drogas", "lei antidrogas", "lei de toxicos")),
    LeiConhecida(
        "9099",
        "Lei dos Juizados Especiais",
        ("4701", "5539"),
        ("juizado especial criminal", "juizados especiais criminais", "juizados especiais"),
    ),
    LeiConhecida("9605", "Lei de Crimes Ambientais", ("4688", "6717"), ("crimes ambientais", "lei ambiental")),
    LeiConhecida(
        "9613", "Lei de Lavagem de Dinheiro", ("4702", "6723"), ("lavagem de dinheiro", "lavagem de capitais")
    ),
    LeiConhecida("13869", "Lei de Abuso de Autoridade", ("4684", "6716"), ("abuso de autoridade",)),
    LeiConhecida("10826", "Estatuto do Desarmamento", ("4697",), ("estatuto do desarmamento",)),
    LeiConhecida(
        "12850",
        "Lei das Organizações Criminosas",
        ("4705", "6725"),
        ("organizacao criminosa", "organizacoes criminosas"),
    ),
    LeiConhecida("7210", "Lei de Execução Penal", ("4703", "6734"), ("lei de execucao penal", "lep")),
    LeiConhecida("8072", "Lei dos Crimes Hediondos", ("4693",), ("crimes hediondos", "crime hediondo")),
    LeiConhecida("9455", "Lei de Tortura", ("4707",), ("lei de tortura", "crime de tortura")),
    LeiConhecida("13260", "Lei Antiterrorismo", ("4706",), ("terrorismo",)),
    LeiConhecida("2889", "Lei do Genocídio", ("4698",), ("genocidio",)),
    LeiConhecida("7492", "Crimes contra o Sistema Financeiro", ("4689",), ("sistema financeiro nacional",)),
    LeiConhecida("8137", "Crimes contra a Ordem Tributária", ("4695",), ("ordem tributaria",)),
    LeiConhecida("8078", "Código de Defesa do Consumidor", ("4694",), ("codigo de defesa do consumidor", "cdc")),
    LeiConhecida("9503", "Código de Trânsito Brasileiro", ("4691",), ("codigo de transito", "ctb")),
    LeiConhecida(
        "10741", "Estatuto da Pessoa Idosa", ("4696", "6722"), ("estatuto do idoso", "estatuto da pessoa idosa")
    ),
    LeiConhecida("9296", "Lei de Interceptação Telefônica", ("4700", "5555"), ("interceptacao telefonica",)),
    LeiConhecida("12037", "Lei de Identificação Criminal", ("4699",), ("identificacao criminal",)),
    LeiConhecida("7716", "Lei do Racismo", ("4690",), ("racismo", "preconceito de raca")),
    LeiConhecida("1521", "Lei de Economia Popular", ("4687",), ("economia popular",)),
    LeiConhecida("4737", "Código Eleitoral", ("4692",), ("codigo eleitoral", "crime eleitoral", "crimes eleitorais")),
    LeiConhecida("11105", "Lei de Biossegurança", ("4685",), ("biosseguranca",)),
    LeiConhecida("3688", "Lei das Contravenções Penais", ("4686",), ("contravencoes penais", "contravencao penal")),
    LeiConhecida(
        "8069", "Estatuto da Criança e do Adolescente", ("4709",), ("estatuto da crianca e do adolescente", "eca")
    ),
    LeiConhecida("12830", "Investigação criminal pelo delegado", ("5498",)),
    LeiConhecida("12015", "Reforma dos crimes contra a dignidade sexual", ("5102",)),
    LeiConhecida("13104", "Lei do Feminicídio", ("5151",)),
    LeiConhecida("13718", "Lei da Importunação Sexual", ("5105",)),
    LeiConhecida("14132", "Lei do crime de Perseguição", ("5130",)),
    LeiConhecida("14188", "Violência psicológica contra a mulher", ("5131",)),
    LeiConhecida("13964", "Pacote Anticrime", (), ("pacote anticrime",)),
)
"""Catálogo de leis do recorte. ``temas`` vazio = lei sem tema próprio (código ou lei transversal)."""


class MapaLegislacao:
    """Encontra leis citadas num texto e informa os temas que elas indicam."""

    _RE_LEI: ClassVar[re.Pattern[str]] = re.compile(
        r"\b(?:lei|decreto[\s-]*lei)(?:\s+(?:federal|complementar|ordin[aá]ria))?"
        r"\s*(?:n[º°o.]*\s*\.?\s*)?(\d{1,2}\.?\d{3})(?:\s*/\s*(\d{2,4}))?",
        re.IGNORECASE,
    )

    def __init__(self, processador: ProcessadorTexto, leis: Sequence[LeiConhecida] = LEIS_DO_RECORTE) -> None:
        """Indexa o catálogo de leis.

        Args:
            processador: Processador usado para normalizar o texto.
            leis: Catálogo de leis conhecidas.
        """
        self._processador: ProcessadorTexto = processador
        self._por_numero: dict[str, LeiConhecida] = {lei.numero: lei for lei in leis}

    def leis_citadas(self, texto: str) -> tuple[str, ...]:
        """Lista as leis citadas pelo número ("Lei nº 11.343/06") ou pelo apelido.

        Números que não estão no catálogo também são devolvidos, para a EDA
        mostrar quais leis aparecem e ainda não têm mapeamento.

        Args:
            texto: Texto já limpo de HTML.

        Returns:
            Números das leis, sem repetição, em ordem crescente.
        """
        encontrados: set[str] = set()
        correspondencia: re.Match[str]
        for correspondencia in self._RE_LEI.finditer(texto):
            encontrados.add(correspondencia.group(1).replace(".", ""))
        normalizado: str = f" {self._processador.normalizar(texto)} "
        lei: LeiConhecida
        apelido: str
        for lei in self._por_numero.values():
            for apelido in lei.apelidos:
                if f" {apelido} " in normalizado:
                    encontrados.add(lei.numero)
        return tuple(sorted(encontrados, key=int))

    def lei(self, numero: str) -> LeiConhecida | None:
        """Busca uma lei do catálogo pelo número.

        Args:
            numero: Número sem pontos (``"11340"``).

        Returns:
            A lei, ou ``None`` se não estiver catalogada.
        """
        return self._por_numero.get(numero)

    def todas(self) -> list[LeiConhecida]:
        """Devolve o catálogo completo.

        Returns:
            Leis conhecidas, na ordem do catálogo.
        """
        return list(self._por_numero.values())
