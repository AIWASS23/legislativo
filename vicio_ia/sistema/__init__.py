"""Fase de decisão da etapa 2: o sistema de classificação que roda sem modelo de linguagem (ADR-019).

Lê os anexos e os artefatos versionados da fase de conhecimento, aprende os pesos leves com a
folha-verdade, calibra e decide. Nenhum módulo deste pacote pode importar ``vicio_ia.llm`` ou
``vicio_ia.classificacao``, nem ler os votos de LLM da etapa 1; um teste confere isso.
"""
