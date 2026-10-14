"""Credenciais de provedores: leitura do ``.env`` e detecção de chaves, sem nunca expor valores."""

from __future__ import annotations

import os
from pathlib import Path
from typing import ClassVar


class CarregadorAmbiente:
    """Carrega o ``.env`` do projeto e informa quais credenciais existem.

    Variáveis já definidas no ambiente têm prioridade sobre o ``.env``. Os
    valores das chaves nunca são impressos nem gravados: só se informa se existem.
    """

    CREDENCIAIS: ClassVar[dict[str, tuple[str, ...]]] = {
        "anthropic": ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"),
        "openai": ("OPENAI_API_KEY",),
        "huggingface": ("HF_TOKEN", "HUGGING_FACE_HUB_TOKEN"),
    }

    def __init__(self, arquivo_env: Path) -> None:
        """Define o arquivo ``.env`` a ler.

        Args:
            arquivo_env: Caminho do ``.env`` (pode não existir).
        """
        self._arquivo_env: Path = arquivo_env

    def carregar_env(self) -> list[str]:
        """Lê o ``.env`` e define no ambiente as variáveis que ainda não existem.

        Linhas vazias e comentários (``#``) são ignorados; aspas em volta do valor são removidas.

        Returns:
            Nomes das variáveis definidas a partir do arquivo.
        """
        if not self._arquivo_env.is_file():
            return []
        definidas: list[str] = []
        linha: str
        for linha in self._arquivo_env.read_text(encoding="utf-8").splitlines():
            limpa: str = linha.strip()
            if not limpa or limpa.startswith("#") or "=" not in limpa:
                continue
            nome: str
            valor: str
            nome, valor = limpa.removeprefix("export ").split("=", 1)
            nome = nome.strip()
            valor = valor.strip().strip('"').strip("'")
            if nome and nome not in os.environ:
                os.environ[nome] = valor
                definidas.append(nome)
        return definidas

    def valor(self, nomes: tuple[str, ...]) -> str | None:
        """Devolve o valor da primeira variável definida da lista.

        Args:
            nomes: Nomes de variáveis, em ordem de preferência.

        Returns:
            O valor, ou ``None`` se nenhuma estiver definida.
        """
        nome: str
        for nome in nomes:
            valor: str | None = os.environ.get(nome)
            if valor:
                return valor
        return None

    def token_huggingface(self) -> str | None:
        """Busca o token do Hugging Face no ambiente ou no arquivo salvo pelo ``hf auth login``.

        Returns:
            O token, ou ``None`` se não houver.
        """
        token: str | None = self.valor(self.CREDENCIAIS["huggingface"])
        if token:
            return token
        pasta_hf: Path = Path(os.environ.get("HF_HOME", Path.home() / ".cache" / "huggingface"))
        arquivo: Path = pasta_hf / "token"
        if arquivo.is_file():
            conteudo: str = arquivo.read_text(encoding="utf-8").strip()
            return conteudo or None
        return None

    def credenciais(self) -> dict[str, bool]:
        """Informa quais credenciais de API estão disponíveis.

        Returns:
            ``provedor -> existe credencial``. Para a Anthropic, também conta um
            perfil do ``ant auth login`` em ``~/.config/anthropic``.
        """
        perfil_ant: bool = (Path.home() / ".config" / "anthropic").is_dir()
        return {
            "anthropic": self.valor(self.CREDENCIAIS["anthropic"]) is not None or perfil_ant,
            "openai": self.valor(self.CREDENCIAIS["openai"]) is not None,
            "huggingface": self.token_huggingface() is not None,
        }
