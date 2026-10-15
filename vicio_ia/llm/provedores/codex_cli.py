"""Provedor GPT via CLI ``codex exec`` (OpenAI Codex), usando a assinatura do ChatGPT."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import ClassVar

from vicio_ia.llm.contratos import ErroProvedor, RequisicaoLLM, RespostaLLM, UsoTokens
from vicio_ia.llm.provedores.cli_base import ProvedorCLI


class ProvedorCodexCLI(ProvedorCLI):
    """Chama ``codex exec`` numa pasta vazia, com sandbox somente leitura e sessão efêmera.

    A CLI não aceita substituir o prompt de sistema; as instruções vão no início do prompt,
    que é enviado pela entrada padrão (sem limite de argumento). O schema vai por arquivo
    (``--output-schema``) e a resposta final é lida de ``--output-last-message``. Os eventos
    JSONL (``--json``) trazem o uso de tokens em ``turn.completed``.
    """

    nome: ClassVar[str] = "codex-cli"
    descricao: ClassVar[str] = "GPT via CLI `codex exec` (assinatura ChatGPT)"
    executavel: ClassVar[str] = "codex"
    ESFORCOS: ClassVar[frozenset[str]] = frozenset({"", "minimal", "low", "medium", "high", "xhigh"})

    def __init__(self, timeout_segundos: int, max_bytes_argumento: int, esforco: str) -> None:
        """Configura os limites da chamada e o esforço de raciocínio.

        Args:
            timeout_segundos: Tempo máximo por chamada.
            max_bytes_argumento: Mantido pelo contrato das CLIs (o prompt vai pela entrada padrão).
            esforco: ``model_reasoning_effort`` (``""`` = padrão do ``~/.codex/config.toml``).

        Raises:
            ErroProvedor: Se o esforço for inválido.
        """
        super().__init__(timeout_segundos, max_bytes_argumento)
        if esforco not in self.ESFORCOS:
            raise ErroProvedor(f"codex-cli: esforço inválido {esforco!r}")
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
            modelo: ID do modelo na conta (``gpt-6.1-sol``).

        Returns:
            Resposta padronizada (sem custo informado: assinatura).

        Raises:
            ErroProvedor: Se a CLI falhar, o turno falhar ou faltar a resposta estruturada.
        """
        prompt: str = (
            "Siga as instruções abaixo e responda somente com o resultado pedido; não use ferramentas "
            "nem leia arquivos.\n\n"
            f"# Instruções\n{requisicao.sistema}\n\n# Tarefa\n{requisicao.usuario}"
        )
        pasta: str
        with tempfile.TemporaryDirectory(prefix="vicio_codex_") as pasta:
            base: Path = Path(pasta)
            resposta_arquivo: Path = base / "resposta.txt"
            comando: list[str] = [
                self.executavel,
                "exec",
                "--skip-git-repo-check",
                "--ephemeral",
                "--sandbox",
                "read-only",
                "--cd",
                pasta,
                "--model",
                modelo,
                "--json",
                "--output-last-message",
                str(resposta_arquivo),
            ]
            if self._esforco:
                comando.extend(["--config", f'model_reasoning_effort="{self._esforco}"'])
            if requisicao.schema is not None:
                schema_arquivo: Path = base / "schema.json"
                schema_arquivo.write_text(json.dumps(dict(requisicao.schema), ensure_ascii=False), encoding="utf-8")
                comando.extend(["--output-schema", str(schema_arquivo)])
            comando.append("-")
            ultimo: dict[str, object]
            latencia: float
            ultimo, latencia = self.executar(comando, prompt, base)
            texto: str = resposta_arquivo.read_text(encoding="utf-8").strip() if resposta_arquivo.is_file() else ""
        if ultimo.get("type") != "turn.completed":
            raise ErroProvedor(f"codex-cli: turno não concluído: {json.dumps(ultimo, ensure_ascii=False)[:300]}")
        dados: dict[str, object] | None = self.extrair_json(texto) if requisicao.schema is not None else None
        self.exigir_dados(requisicao, dados, texto)
        uso: object = ultimo.get("usage", {})
        uso_dict: dict[str, object] = uso if isinstance(uso, dict) else {}
        cache_lido: int = self.inteiro(uso_dict.get("cached_input_tokens"))
        return RespostaLLM(
            provedor=self.nome,
            modelo=modelo,
            texto=texto,
            dados=dados,
            uso=UsoTokens(
                entrada=max(0, self.inteiro(uso_dict.get("input_tokens")) - cache_lido),
                saida=self.inteiro(uso_dict.get("output_tokens")),
                cache_lido=cache_lido,
                cache_escrito=self.inteiro(uso_dict.get("cache_write_input_tokens")),
                raciocinio=self.inteiro(uso_dict.get("reasoning_output_tokens")),
            ),
            latencia_s=latencia,
            motivo_parada="turn.completed",
            custo_usd=None,
        )
