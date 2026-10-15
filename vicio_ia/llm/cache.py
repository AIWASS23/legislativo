"""Cache de chamadas a modelos, só de acréscimo (ADR-003).

Cada chamada bem-sucedida vira uma linha JSON em ``runs/<papel>/<AAAA-MM-DD>.jsonl``. A chave
é o SHA-256 de tudo o que muda a resposta: provedor, modelo, parâmetros do provedor, versão do
prompt, prompt de sistema, tarefa, schema, limite de saída e número da tentativa. Com o cache
cheio, uma rodada inteira é refeita sem chamar nenhum modelo.
"""

from __future__ import annotations

import hashlib
import json
import threading
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import TextIO

from vicio_ia.leitura_json import CamposJSON, ErroCampoJSON
from vicio_ia.llm.contratos import RequisicaoLLM, RespostaLLM, UsoTokens


@dataclass(frozen=True)
class RegistroChamada:
    """Uma chamada gravada no cache.

    Attributes:
        chave: SHA-256 da chamada.
        papel: Papel que fez a chamada (``classificador_a``, ``cartoes``...).
        rotulo: O que foi processado (ID da questão, ID do tema pai...).
        versao_prompt: Hash curto do arquivo de prompt.
        tentativa: 1 na primeira chamada; 2 na repetição depois de resposta inválida.
        resposta: Resposta padronizada do provedor.
        custo_usd: Custo da chamada (informado pelo provedor ou calculado pela tabela de preços).
        rodada: Identificador da execução que fez a chamada (``AAAAMMDD-HHMMSS``).
        horario: Data e hora da chamada (ISO 8601).
    """

    chave: str
    papel: str
    rotulo: str
    versao_prompt: str
    tentativa: int
    resposta: RespostaLLM
    custo_usd: float | None
    rodada: str
    horario: str

    def como_dict(self) -> dict[str, object]:
        """Converte o registro num dicionário serializável.

        Returns:
            Dicionário com a resposta aninhada.
        """
        return asdict(self)

    @classmethod
    def de_dict(cls, objeto: Mapping[str, object], origem: str) -> RegistroChamada:
        """Reconstrói um registro lido do disco.

        Args:
            objeto: Linha decodificada.
            origem: Arquivo e linha (para mensagens de erro).

        Returns:
            Registro.
        """
        campos: CamposJSON = CamposJSON(objeto, origem)
        resposta: CamposJSON = CamposJSON(campos.objeto("resposta"), f"{origem}, resposta")
        uso: CamposJSON = CamposJSON(resposta.objeto("uso"), f"{origem}, uso")
        return cls(
            chave=campos.texto("chave"),
            papel=campos.texto("papel"),
            rotulo=campos.texto("rotulo"),
            versao_prompt=campos.texto("versao_prompt"),
            tentativa=campos.inteiro("tentativa"),
            resposta=RespostaLLM(
                provedor=resposta.texto("provedor"),
                modelo=resposta.texto("modelo"),
                texto=resposta.texto("texto"),
                dados=resposta.objeto_opcional("dados"),
                uso=UsoTokens(
                    entrada=uso.inteiro("entrada"),
                    saida=uso.inteiro("saida"),
                    cache_lido=uso.inteiro("cache_lido"),
                    cache_escrito=uso.inteiro("cache_escrito"),
                    raciocinio=uso.inteiro("raciocinio"),
                ),
                latencia_s=resposta.numero("latencia_s"),
                motivo_parada=resposta.texto("motivo_parada"),
                custo_usd=resposta.numero_opcional("custo_usd"),
                extras=resposta.objeto("extras"),
            ),
            custo_usd=campos.numero_opcional("custo_usd"),
            rodada=campos.texto("rodada"),
            horario=campos.texto("horario"),
        )


class CacheChamadas:
    """Cache em disco, só de acréscimo, seguro para várias threads."""

    def __init__(self, pasta: Path) -> None:
        """Define a pasta do cache (``runs/``); a leitura é feita na primeira consulta.

        Args:
            pasta: Pasta raiz do cache.
        """
        self._pasta: Path = pasta
        self._registros: dict[str, RegistroChamada] | None = None
        self._trava: threading.Lock = threading.Lock()

    @staticmethod
    def chave(
        provedor: str,
        modelo: str,
        parametros: Mapping[str, object],
        requisicao: RequisicaoLLM,
        versao_prompt: str,
        tentativa: int,
    ) -> str:
        """Calcula a chave de uma chamada.

        Args:
            provedor: Nome do provedor.
            modelo: Modelo.
            parametros: Parâmetros do provedor que mudam a resposta.
            requisicao: Prompt, tarefa, schema e limite de saída.
            versao_prompt: Hash do arquivo de prompt.
            tentativa: Número da tentativa.

        Returns:
            SHA-256 em hexadecimal.
        """
        conteudo: dict[str, object] = {
            "provedor": provedor,
            "modelo": modelo,
            "parametros": dict(parametros),
            "versao_prompt": versao_prompt,
            "sistema": requisicao.sistema,
            "usuario": requisicao.usuario,
            "schema": dict(requisicao.schema) if requisicao.schema is not None else None,
            "nome_schema": requisicao.nome_schema,
            "max_tokens": requisicao.max_tokens,
            "tentativa": tentativa,
        }
        texto: str = json.dumps(conteudo, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(texto.encode("utf-8")).hexdigest()

    def obter(self, chave: str) -> RegistroChamada | None:
        """Busca uma chamada pela chave.

        Args:
            chave: Chave calculada por :meth:`chave`.

        Returns:
            O registro, ou ``None`` se a chamada nunca foi feita.
        """
        with self._trava:
            return self._carregados().get(chave)

    def gravar(self, registro: RegistroChamada) -> None:
        """Acrescenta uma chamada ao arquivo do papel e do dia.

        Args:
            registro: Chamada bem-sucedida.
        """
        destino: Path = self._pasta / registro.papel / f"{datetime.now():%Y-%m-%d}.jsonl"
        linha: str = json.dumps(registro.como_dict(), ensure_ascii=False) + "\n"
        with self._trava:
            carregados: dict[str, RegistroChamada] = self._carregados()
            if registro.chave in carregados:
                return
            destino.parent.mkdir(parents=True, exist_ok=True)
            arquivo: TextIO
            with destino.open("a", encoding="utf-8") as arquivo:
                arquivo.write(linha)
                arquivo.flush()
            carregados[registro.chave] = registro

    def registros(self) -> list[RegistroChamada]:
        """Lista todas as chamadas gravadas.

        Returns:
            Registros na ordem de leitura.
        """
        with self._trava:
            return list(self._carregados().values())

    def _carregados(self) -> dict[str, RegistroChamada]:
        """Lê o cache do disco na primeira vez (chamar com a trava adquirida).

        Linhas truncadas (gravação interrompida) são ignoradas.

        Returns:
            Chave -> registro.
        """
        if self._registros is None:
            registros: dict[str, RegistroChamada] = {}
            caminho: Path
            for caminho in sorted(self._pasta.glob("*/*.jsonl")) if self._pasta.is_dir() else []:
                numero: int
                linha: str
                for numero, linha in enumerate(caminho.read_text(encoding="utf-8").splitlines(), start=1):
                    try:
                        valor: object = json.loads(linha)
                    except ValueError:
                        continue
                    if isinstance(valor, dict):
                        try:
                            registro: RegistroChamada = RegistroChamada.de_dict(
                                {str(k): v for k, v in valor.items()}, f"{caminho.name}:{numero}"
                            )
                        except ErroCampoJSON:
                            continue
                        registros.setdefault(registro.chave, registro)
            self._registros = registros
        return self._registros
