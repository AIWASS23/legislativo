"""Provedor Gemini (e demais modelos da conta) via CLI ``agy`` do Antigravity, usando a assinatura."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import ClassVar

from vicio_ia.llm.contratos import ErroProvedor, RequisicaoLLM, RespostaLLM, UsoTokens
from vicio_ia.llm.provedores.cli_base import ProvedorCLI


class ProvedorGeminiAgy(ProvedorCLI):
    """Chama ``agy -p`` em sandbox, numa pasta vazia, com ``--json-schema``.

    A CLI não aceita substituir o prompt de sistema; as instruções vão no início do
    prompt, que é passado como argumento (limite configurável, ``max_bytes_argumento_cli``).
    """

    nome: ClassVar[str] = "gemini-agy"
    descricao: ClassVar[str] = "Gemini (e outros modelos da conta) via CLI `agy` (assinatura Antigravity)"
    executavel: ClassVar[str] = "agy"

    def gerar(self, requisicao: RequisicaoLLM, modelo: str) -> RespostaLLM:
        """Faz uma chamada via CLI.

        Args:
            requisicao: Conteúdo e schema.
            modelo: ID listado por ``agy models`` (``gemini-3.8-flash-low``).

        Returns:
            Resposta padronizada.

        Raises:
            ErroProvedor: Se a CLI falhar, o status não for sucesso ou faltar a resposta estruturada.
        """
        prompt: str = (
            "Siga as instruções abaixo e responda somente com o resultado pedido; não use ferramentas.\n\n"
            f"# Instruções\n{requisicao.sistema}\n\n# Tarefa\n{requisicao.usuario}"
        )
        self.checar_tamanho(prompt, "prompt")
        comando: list[str] = [
            self.executavel,
            "-p",
            prompt,
            "--output-format",
            "json",
            "--model",
            modelo,
            "--sandbox",
            "--print-timeout",
            f"{self._timeout}s",
        ]
        if requisicao.schema is not None:
            comando.extend(["--json-schema", json.dumps(dict(requisicao.schema), ensure_ascii=False)])
        pasta: str
        with tempfile.TemporaryDirectory(prefix="vicio_agy_") as pasta:
            saida: dict[str, object]
            latencia: float
            saida, latencia = self.executar(comando, None, Path(pasta))
        status: str = str(saida.get("status", ""))
        if status != "SUCCESS":
            raise ErroProvedor(f"gemini-agy: status {status!r}: {str(saida.get('response', ''))[:300]}")
        estruturado: object = saida.get("structured_output")
        texto: str = str(saida.get("response", ""))
        dados: dict[str, object] | None = (
            {str(chave): valor for chave, valor in estruturado.items()}
            if isinstance(estruturado, dict)
            else self.extrair_json(texto)
        )
        self.exigir_dados(requisicao, dados, texto)
        uso: object = saida.get("usage", {})
        uso_dict: dict[str, object] = uso if isinstance(uso, dict) else {}
        return RespostaLLM(
            provedor=self.nome,
            modelo=modelo,
            texto=texto,
            dados=dados,
            uso=UsoTokens(
                entrada=self.inteiro(uso_dict.get("input_tokens")),
                saida=self.inteiro(uso_dict.get("output_tokens")),
                cache_lido=self.inteiro(uso_dict.get("cache_read_tokens")),
                raciocinio=self.inteiro(uso_dict.get("thinking_tokens")),
            ),
            latencia_s=latencia,
            motivo_parada=status,
            custo_usd=None,
            extras={"num_turns": saida.get("num_turns"), "duracao_cli_s": saida.get("duration_seconds")},
        )
