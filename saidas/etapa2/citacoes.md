# Citações de lei e artigo nas questões

Gerado em 21/10/2026 06:43 por `uv run python executar_citacoes.py`. Extração só por expressões regulares, sem modelo de linguagem (ADR-021). Artefato: `dados/conhecimento/citacoes.jsonl`.

## Cobertura

- Questões com pelo menos um artigo citado: 94 de 659 (58 de 359 antigas e 36 de 300 novas); 15 delas estão na folha-verdade.
- Questões que citam alguma lei, com ou sem artigo: 286.
- Artigos com a lei resolvida: 209 (explicita 186, repeticao 6, contexto 6, anafora 5, enumeracao 3, manual 3).
- Artigos sem lei resolvida (pendentes): 0.
- Artigos por lei: CP (106), CPP (34), Lei 11.343/2006 (13), CF (8), Lei 8.069/1990 (8), Lei 11.340/2006 (8), Lei 14.597/2023 (7), Lei 9.099/1995 (5), Lei 10.826/2003 (3), Lei 9.609/1998 (3), Lei 2.889/1956 (2), Lei 4.737/1965 (2), LEP (2), Lei 9.613/1998 (2), Lei 12.850/2013 (2), Lei 9.605/1998 (2), Lei 7.716/1989 (1), Lei 8.666/1993 (1).

As resoluções são: `explicita` (a lei está junto do artigo), `enumeracao` (herdada do artigo seguinte da mesma enumeração), `anafora` ("do mesmo diploma"), `repeticao` (o mesmo artigo já apareceu com a lei), `contexto` (a questão só cita uma lei) e `manual` (pendente resolvido pelo autor em `dados/conhecimento/citacoes_manuais.csv`).

## Citações × mapa de artigos

Mapa usado: `dados/conhecimento/mapa_artigos.csv`.

- Questões com artigo citado que acham pelo menos uma linha no mapa: 88 de 94.
- Na folha-verdade: 15 questões acham linha no mapa; fora da taxonomia entre elas: 1.
- Das 14 com tema: em 10, algum tema do mapa acerta pela régua; em 5, todos acertam; em 3, o mapa aponta um único tema.

| Questão | Fora | Temas do mapa | Acerto pela régua |
|---|---|---|---|
| Q0012 | não | 4701 Direito Penal - Legislação Especial > Juizado Especial Criminal; 5539 Processo Penal > Procedimento Sumaríssimo; 5540 Processo Penal > Procedimento Sumaríssimo > Competência dos Juizados Especiais Criminais | sim, não, não |
| Q0028 | não | 5524 Processo Penal > Procedimento do Tribunal do Júri; 5526 Processo Penal > Procedimento do Tribunal do Júri > Procedimento Bifásico do Tribunal do Júri; 5527 Processo Penal > Procedimento do Tribunal do Júri > Impronúncia, Desclassificação, Absolvição Sumária e Pronúncia | sim, sim, sim |
| Q0077 | não | 4698 Direito Penal - Legislação Especial > Genocídio; 5149 Penal > Dos Crimes Contra a Vida; 5150 Penal > Dos Crimes Contra a Vida > Homicídio; 4692 Direito Penal - Legislação Especial > Crimes Eleitorais; 5102 Penal > Dos Crimes Contra a Dignidade Sexual | não, não, não, não, não |
| Q0087 | sim | 4703 Direito Penal - Legislação Especial > Lei de Execução Penal | — |
| Q0110 | não | 5102 Penal > Dos Crimes Contra a Dignidade Sexual | não |
| Q0138 | não | 5199 Penal > Teoria da Pena; 5207 Penal > Teoria da Pena > Suspensão Condicional da Pena | sim, não |
| Q0150 | não | 4708 Direito Penal - Legislação Especial > Tráfico de Drogas | sim |
| Q0186 | não | 5199 Penal > Teoria da Pena; 5202 Penal > Teoria da Pena > Primeira Fase da Dosimetria: Circunstâncias Judiciais | sim, sim |
| Q0202 | não | 5102 Penal > Dos Crimes Contra a Dignidade Sexual; 5108 Penal > Dos Crimes Contra a Dignidade Sexual > Corrupção de Menores; 5109 Penal > Dos Crimes Contra a Dignidade Sexual > Outros Crimes Contra a Dignidade Sexual | não, não, não |
| Q0208 | não | 5149 Penal > Dos Crimes Contra a Vida; 5150 Penal > Dos Crimes Contra a Vida > Homicídio | não, não |
| Q0251 | não | 5191 Penal > Punibilidade | sim |
| Q0259 | não | 5157 Penal > Dos Crimes Contra o Patrimônio; 5164 Penal > Dos Crimes Contra o Patrimônio > Dano; 5159 Penal > Dos Crimes Contra o Patrimônio > Furto | sim, sim, não |
| Q0316 | não | 5218 Penal > Teoria do Crime: Fato Típico; 5224 Penal > Teoria do Crime: Fato Típico > Erro de Tipo | sim, sim |
| Q0336 | não | 5157 Penal > Dos Crimes Contra o Patrimônio; 5160 Penal > Dos Crimes Contra o Patrimônio > Roubo; 5159 Penal > Dos Crimes Contra o Patrimônio > Furto; 5175 Penal > Iter Criminis; 5177 Penal > Iter Criminis > Crime Consumado e Tentado; 5165 Penal > Dos Crimes Contra o Patrimônio > Apropriação indébita | sim, não, sim, sim, sim, não |
| Q0345 | não | 5199 Penal > Teoria da Pena; 5203 Penal > Teoria da Pena > Segunda Fase da Dosimetria: Agravantes e Atenuantes; 5102 Penal > Dos Crimes Contra a Dignidade Sexual; 5110 Penal > Dos Crimes Contra a Dignidade Sexual > Disposições Gerais dos Crimes Contra a Dignidade Sexual | não, não, sim, não |

## Amostra para conferência (20 artigos sorteados, semente 20261020)

Marque na última coluna se a lei e o artigo extraídos estão certos.

| Questão | Lei | Artigos | Resolução | Trecho | Certo? |
|---|---|---|---|---|---|
| Q0016 | CPP | 3 | explicita | …tação conforme a Constituição Federal, ao § 1º do Art. 3º-B do CPP, incluído pela Lei nº 13.964/2019, para es… | |
| Q0020 | CP | 307 | explicita | …r maus antecedentes constitui o crime previsto no artigo 307, caput, do Código Penal (atribuir-se ou atribuir… | |
| Q0020 | CF | 5 | explicita | …gido pelo princípio constitucional da autodefesa (artigo 5o, inciso LXIII, CF). ( ) Segundo jurisprudência d… | |
| Q0033 | CPP | 366 | explicita | …ital e que não constituiu defensor, nos termos do art. 366 do Código de Processo Penal. não admite revogação… | |
| Q0036 | Lei 11.340/2006 | 16 | explicita | …do. Designar, de ofício, a audiência prevista no Art. 16 da Lei Maria da Penha, por ser ato processual obr… | |
| Q0070 | CP | 42 | explicita | …nto da reprimenda total a ser cumprida (detração, Art. 42 do CP), não podendo ser contabilizado para fins d… | |
| Q0112 | Lei 12.850/2013 | 2 | explicita | …, financiar ou integrar organização criminosa, do art. 2° da Lei n° 12.850/13, são aumentadas de 1/6 a 2/3,… | |
| Q0114 | CF | 5 | explicita | …pio da irretroatividade da lei penal prejudicial (art. 5°, LX, CRF/88), seus efeitos deverão ser prospectiv… | |
| Q0150 | Lei 11.343/2006 | 40 | explicita | …- A majorante do tráfico transnacional de drogas (art. 40, inciso I, da Lei n. 11.343/2006) configura-se co… | |
| Q0174 | Lei 8.069/1990 | 241 | explicita | …suficiente para a caracterização do tipo penal do art. 241-A do ECA, sendo imprescindível o efetivo acesso de… | |
| Q0174 | CP | 154 | explicita | …nvasão de dispositivos informáticos, definidos no art. 154-A do Código Penal, são de ação penal pública incond… | |
| Q0271 | CPP | 617 | explicita | …e que beneficie o réu, o que é feito por força do artigo 617 do CPP, a contrario sensu, que permite concluir s… | |
| Q0289 | Lei 11.340/2006 | 21 | explicita | …da, a ofendida deve ser comunicada, nos termos do art. 21 da Lei nº 11.340/2006. | |
| Q0336 | CP | 155 | enumeracao | …crime de furto, na sua forma tentada, previsto no art. 155, caput, c/c art. 14, II, ambos do CP. praticou o… | |
| Q0336 | CP | 14 | explicita | …ua forma tentada, previsto no art. 157, caput c/c art. 14, II, ambos do CP. praticou o crime de furto consu… | |
| Q0345 | CP | 61 | explicita | …no Art. 61, inciso II, alínea f, do Código Penal (Art. 61. São circunstâncias que sempre agravam a pena, qu… | |
| Q0536 | CPP | 158 | explicita | …r: Tendo em vista que o regramento constante dos arts. 158-A a 158-F do Código de Processo Penal entrou em vigor em 20… | |
| Q0625 | CP | 316 | explicita | …olicial cometem o crime de concussão, previsto no artigo 316 do Código Penal. Mévio e o policial cometem o cri… | |
| Q0641 | CP | 333 | explicita | …pectivamente. Ambos incorrem em corrupção ativa (art. 333, Código Penal) e peculato (art. 312, Código Penal… | |
| Q0641 | CP | 317 | explicita | …rrupção ativa (art. 333, Código Penal) e passiva (art. 317, Código Penal). José pratica prevaricação (art. 3… | |
