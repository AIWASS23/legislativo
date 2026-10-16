"""Congelamento do pipeline antes da leva 2 do gold (ADR-012, ADR-014).

Grava a impressão digital (SHA-256) de tudo o que decide a resposta: prompts, cartões, árvores,
decisões manuais da árvore, escolha de modelos por papel e o código de classificação, decisão e
calibração. A leva 2 só é sorteada com um congelamento registrado e sem nenhuma diferença desde
então: ela mede o pipeline entregue, não ajusta.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import ClassVar, TextIO

from vicio_ia.configuracao import Caminhos


class RegistroCongelamento:
    """Registra e confere o congelamento (``saidas/experimentos/congelamento.json``)."""

    PADROES: ClassVar[tuple[str, ...]] = (
        "prompts/*.md",
        "dados/preparados/questoes.jsonl",
        "dados/preparados/temas.json",
        "dados/preparados/arvore_enxuta.txt",
        "dados/temas/*.csv",
        "dados/temas/cartoes.jsonl",
        "dados/temas/arvore_escopo.txt",
        "vicio_ia/configuracao.py",
        "vicio_ia/classificacao/*.py",
        "vicio_ia/decisao/*.py",
        "vicio_ia/sinais/*.py",
        "vicio_ia/temas/arvore_prompt.py",
        "vicio_ia/avaliacao/calibracao.py",
        "vicio_ia/avaliacao/previsao.py",
        "vicio_ia/avaliacao/pontuador.py",
    )

    def __init__(self, caminhos: Caminhos) -> None:
        """Define os caminhos.

        Args:
            caminhos: Caminhos do projeto.
        """
        self._raiz: Path = caminhos.raiz
        self._escolha: Path = caminhos.escolha_modelos
        self._arquivo: Path = caminhos.raiz / "saidas" / "experimentos" / "congelamento.json"
        self._registro: Path = caminhos.raiz / "saidas" / "experimentos" / "registro.md"

    @property
    def arquivo(self) -> Path:
        """Caminho do registro em JSON."""
        return self._arquivo

    def impressoes(self) -> dict[str, str]:
        """Calcula o SHA-256 (16 primeiros dígitos) de cada arquivo congelado e da escolha de modelos.

        Returns:
            ``caminho relativo -> hash``; a escolha de modelos entra só com os papéis (sem a data).
        """
        impressoes: dict[str, str] = {}
        padrao: str
        for padrao in self.PADROES:
            caminho: Path
            for caminho in sorted(self._raiz.glob(padrao)):
                if caminho.is_file():
                    impressoes[str(caminho.relative_to(self._raiz))] = self._hash(caminho.read_bytes())
        conteudo: object = json.loads(self._escolha.read_text(encoding="utf-8")) if self._escolha.is_file() else {}
        papeis: object = conteudo.get("papeis", {}) if isinstance(conteudo, dict) else {}
        impressoes["config/escolha_modelos.json#papeis"] = self._hash(
            json.dumps(papeis, ensure_ascii=False, sort_keys=True).encode("utf-8")
        )
        return impressoes

    def registrar(self, motivo: str) -> Path:
        """Grava o congelamento e acrescenta o marco em ``registro.md``.

        Args:
            motivo: Por que se congela agora.

        Returns:
            Caminho do JSON.
        """
        impressoes: dict[str, str] = self.impressoes()
        agora: str = datetime.now().isoformat(timespec="seconds")
        self._arquivo.parent.mkdir(parents=True, exist_ok=True)
        self._arquivo.write_text(
            json.dumps({"congelado_em": agora, "motivo": motivo, "arquivos": impressoes}, ensure_ascii=False, indent=1)
            + "\n",
            encoding="utf-8",
        )
        linhas: list[str] = [
            "",
            f"## Congelamento ({agora})",
            "",
            f"{motivo}",
            "",
            f"{len(impressoes)} arquivos com impressão digital em `saidas/experimentos/congelamento.json`. A partir",
            "daqui, nenhum prompt, cartão, regra, modelo ou parâmetro muda; a leva 2 só mede.",
            "",
        ]
        arquivo: TextIO
        with self._registro.open("a", encoding="utf-8") as arquivo:
            arquivo.write("\n".join(linhas))
        return self._arquivo

    def conferir(self) -> tuple[bool, list[str]]:
        """Compara os arquivos atuais com o congelamento.

        Returns:
            ``(há congelamento registrado, diferenças)``; sem diferenças, a lista vem vazia.
        """
        if not self._arquivo.is_file():
            return False, []
        conteudo: object = json.loads(self._arquivo.read_text(encoding="utf-8"))
        gravadas: object = conteudo.get("arquivos", {}) if isinstance(conteudo, dict) else {}
        congeladas: dict[str, str] = {str(k): str(v) for k, v in gravadas.items()} if isinstance(gravadas, dict) else {}
        atuais: dict[str, str] = self.impressoes()
        diferencas: list[str] = [
            f"{nome}: {'mudou' if nome in atuais else 'sumiu'}"
            for nome, valor in sorted(congeladas.items())
            if atuais.get(nome) != valor
        ]
        diferencas.extend(f"{nome}: novo" for nome in sorted(set(atuais) - set(congeladas)))
        return True, diferencas

    @staticmethod
    def _hash(conteudo: bytes) -> str:
        """SHA-256 curto.

        Args:
            conteudo: Bytes.

        Returns:
            16 primeiros dígitos hexadecimais.
        """
        return hashlib.sha256(conteudo).hexdigest()[:16]
