"""Provedor Claude via CLI ``claude -p`` (Claude Code), usando a assinatura do usuário."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import ClassVar

from vicio_ia.llm.contratos import ErroProvedor, RequisicaoLLM, RespostaLLM, UsoTokens
from vicio_ia.llm.provedores.cli_base import ProvedorCLI


class ProvedorClaudeCLI(ProvedorCLI):
    """Chama ``claude -p`` sem ferramentas, sem MCP e sem salvar sessão.

    O prompt de sistema do Claude Code é substituído pelo da requisição, gravado num
    arquivo da pasta temporária (``--system-prompt-file``, sem limite de tamanho de
    argumento). A tarefa vai pela entrada padrão. A saída estruturada usa
    ``--json-schema`` e chega no campo ``structured_output``.
    """

    nome: ClassVar[str] = "claude-cli"
    descricao: ClassVar[str] = "Claude via CLI `claude -p` (assinatura)"
    executavel: ClassVar[str] = "claude"
    ESFORCOS: ClassVar[frozenset[str]] = frozenset({"", "low", "medium", "high", "xhigh", "max"})

    def __init__(self, timeout_segundos: int, max_bytes_argumento: int, esforco: str) -> None:
        """Configura os limites da chamada e o esforço.

        Args:
            timeout_segundos: Tempo máximo por chamada.
            max_bytes_argumento: Tamanho máximo do schema passado como argumento.
            esforco: ``--effort`` da CLI (``""`` = padrão da CLI).

        Raises:
            ErroProvedor: Se o esforço for inválido.
        """
        super().__init__(timeout_segundos, max_bytes_argumento)
        if esforco not in self.ESFORCOS:
            raise ErroProvedor(f"claude-cli: esforço inválido {esforco!r}")
        self._esforco: str = esforco

    def parametros_cache(self) -> dict[str, object]:
        """O esforço muda a resposta.

        Returns:
            ``{"esforco": ...}``.
        """
        return {"esforco": self._esforco}

    def gerar(self, requisicao: RequisicaoLLM, modelo: str) -> RespostaLLM:
        """Faz uma chamada via CLI.

        Args:
            requisicao: Conteúdo e schema.
            modelo: ID do modelo (``claude-opus-5-5``) ou apelido (``opus``).

        Returns:
            Resposta padronizada; ``custo_usd`` é o equivalente de lista informado pela CLI.

        Raises:
            ErroProvedor: Se a CLI falhar, reportar erro ou não devolver a resposta estruturada.
        """
        pasta: str
        with tempfile.TemporaryDirectory(prefix="vicio_claude_") as pasta:
            arquivo_sistema: Path = Path(pasta) / "sistema.md"
            arquivo_sistema.write_text(requisicao.sistema, encoding="utf-8")
            comando: list[str] = [
                self.executavel,
                "-p",
                "--output-format",
                "json",
                "--model",
                modelo,
                "--no-session-persistence",
                "--strict-mcp-config",
                "--system-prompt-file",
                str(arquivo_sistema),
                "--tools",
                "",
            ]
            if self._esforco:
                comando.extend(["--effort", self._esforco])
            if requisicao.schema is not None:
                schema: str = json.dumps(dict(requisicao.schema), ensure_ascii=False)
                self.checar_tamanho(schema, "schema")
                comando.extend(["--json-schema", schema])
            saida: dict[str, object]
            latencia: float
            saida, latencia = self.executar(comando, requisicao.usuario, Path(pasta))
        if saida.get("is_error") is True or saida.get("subtype") not in (None, "success"):
            raise ErroProvedor(f"claude-cli: erro reportado pela CLI: {str(saida.get('result', ''))[:300]}")
        estruturado: object = saida.get("structured_output")
        texto: str = str(saida.get("result", ""))
        dados: dict[str, object] | None = (
            {str(chave): valor for chave, valor in estruturado.items()}
            if isinstance(estruturado, dict)
            else self.extrair_json(texto)
        )
        self.exigir_dados(requisicao, dados, texto)
        uso: object = saida.get("usage", {})
        uso_dict: dict[str, object] = uso if isinstance(uso, dict) else {}
        custo: object = saida.get("total_cost_usd")
        return RespostaLLM(
            provedor=self.nome,
            modelo=modelo,
            texto=texto,
            dados=dados,
            uso=UsoTokens(
                entrada=self.inteiro(uso_dict.get("input_tokens")),
                saida=self.inteiro(uso_dict.get("output_tokens")),
                cache_lido=self.inteiro(uso_dict.get("cache_read_input_tokens")),
                cache_escrito=self.inteiro(uso_dict.get("cache_creation_input_tokens")),
            ),
            latencia_s=latencia,
            motivo_parada=str(saida.get("terminal_reason", saida.get("stop_reason", ""))),
            custo_usd=float(custo) if isinstance(custo, (int, float)) else None,
            extras={"num_turns": saida.get("num_turns"), "custo_e_equivalente_de_lista": True},
        )
