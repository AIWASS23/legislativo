"""Trava da fase de decisão: sem LLM e sem rede (ADR-019).

O ``executar_sistema.py`` ativa a trava antes de qualquer outra coisa:

* define a variável de ambiente que faz a ``FabricaProvedores`` recusar criar provedores de LLM;
* troca ``socket.socket.connect``, ``socket.socket.connect_ex`` e ``socket.getaddrinfo`` por funções que
  levantam erro, de modo que qualquer tentativa de rede derruba a execução em vez de passar despercebida.
"""

from __future__ import annotations

import os
import socket
from collections.abc import Callable

from vicio_ia.configuracao import ParametrosSistema


class ErroTrava(Exception):
    """A fase de decisão tentou usar a rede ou um modelo de linguagem."""


def _conectar_bloqueado(conexao: socket.socket, endereco: object) -> None:
    """Substitui ``socket.connect`` enquanto a trava está ativa.

    Args:
        conexao: Socket que tentou conectar.
        endereco: Endereço pedido.

    Raises:
        ErroTrava: Sempre.
    """
    raise ErroTrava(f"a fase de decisão não acessa a rede (tentativa de conexão a {endereco!r}; ADR-019)")


def _conectar_ex_bloqueado(conexao: socket.socket, endereco: object) -> int:
    """Substitui ``socket.connect_ex`` enquanto a trava está ativa.

    Args:
        conexao: Socket que tentou conectar.
        endereco: Endereço pedido.

    Returns:
        Nunca retorna.

    Raises:
        ErroTrava: Sempre.
    """
    raise ErroTrava(f"a fase de decisão não acessa a rede (tentativa de conexão a {endereco!r}; ADR-019)")


def _resolver_bloqueado(
    host: object, port: object, family: int = 0, type: int = 0, proto: int = 0, flags: int = 0
) -> list[object]:
    """Substitui ``socket.getaddrinfo`` enquanto a trava está ativa.

    Args:
        host: Nome pedido.
        port: Porta pedida.
        family: Ignorado.
        type: Ignorado.
        proto: Ignorado.
        flags: Ignorado.

    Returns:
        Nunca retorna.

    Raises:
        ErroTrava: Sempre.
    """
    raise ErroTrava(f"a fase de decisão não acessa a rede (tentativa de resolver {host!r}; ADR-019)")


class TravaSemLLM:
    """Ativa e desativa a trava da fase de decisão."""

    def __init__(self, parametros: ParametrosSistema | None = None) -> None:
        """Guarda o nome da variável de ambiente.

        Args:
            parametros: Parâmetros do sistema (padrão: os do projeto).
        """
        self._variavel: str = (parametros or ParametrosSistema()).variavel_sem_llm
        self._originais: dict[str, Callable[..., object]] = {}
        self._valor_anterior: str | None = None

    @property
    def ativa(self) -> bool:
        """Indica se a trava está ativa nesta instância."""
        return bool(self._originais)

    def ativar(self) -> None:
        """Proíbe provedores de LLM e acesso à rede no processo atual."""
        if self.ativa:
            return
        self._valor_anterior = os.environ.get(self._variavel)
        os.environ[self._variavel] = "1"
        self._originais = {
            "connect": socket.socket.connect,
            "connect_ex": socket.socket.connect_ex,
            "getaddrinfo": socket.getaddrinfo,
        }
        setattr(socket.socket, "connect", _conectar_bloqueado)  # noqa: B010
        setattr(socket.socket, "connect_ex", _conectar_ex_bloqueado)  # noqa: B010
        setattr(socket, "getaddrinfo", _resolver_bloqueado)  # noqa: B010

    def desativar(self) -> None:
        """Devolve o processo ao estado anterior (usado nos testes)."""
        if not self.ativa:
            return
        setattr(socket.socket, "connect", self._originais["connect"])  # noqa: B010
        setattr(socket.socket, "connect_ex", self._originais["connect_ex"])  # noqa: B010
        setattr(socket, "getaddrinfo", self._originais["getaddrinfo"])  # noqa: B010
        self._originais = {}
        if self._valor_anterior is None:
            os.environ.pop(self._variavel, None)
        else:
            os.environ[self._variavel] = self._valor_anterior
