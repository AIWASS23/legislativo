"""Fase de conhecimento da etapa 2 (ADR-019, ADR-020, ADR-021).

Roda offline e pode chamar LLMs e modelos de embedding, sempre pela camada ``vicio_ia.llm``, com cache.
Produz só artefatos versionados em ``dados/conhecimento/``, cada um com proveniência no manifesto.
Nunca pede a um modelo o tema de uma questão.
"""
