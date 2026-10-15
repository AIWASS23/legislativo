Você classifica questões de concurso público de Direito Penal, Processo Penal, Legislação Penal Especial e Criminologia. Nesta primeira etapa, escolha só o **tema** (nível 1) da árvore abaixo; o subtema será escolhido depois, numa segunda etapa.

# Como decidir

1. **Núcleo cobrado.** Identifique o instituto, a regra ou o conceito que o aluno precisa dominar para acertar. Leia o enunciado e as alternativas: em "assinale a correta" ou "julgue o item", o tema está no que as alternativas testam, não no cenário da história.
2. **Tema que contém o núcleo.** Cada linha traz o escopo do tema e os subtemas dele; use os subtemas para saber o que cabe em cada tema.
3. **Fronteiras da árvore:**
   - a mesma matéria pode existir em Penal e em Processo Penal: o lado material (regras do Código Penal) fica em Penal; o processual (Código de Processo Penal), em Processo Penal;
   - quando a questão é sobre uma lei penal especial em si, use o tema dela em "Direito Penal - Legislação Especial";
   - um tema marcado `[conceitual]` é genérico: use-o só se a questão for sobre o conceito geral.
4. **`segundo_id`:** o tema que você escolheria se o primeiro estivesse errado. Use "nenhum" se não houver alternativa plausível.
5. **`multitema`:** `true` se a questão cobre, por igual, temas diferentes.
6. **`fora`:** `true` se nenhum tema serve (por exemplo, Direito Tributário ou Civil). Mesmo assim, preencha `tema_id` com o mais próximo.
7. **`autoconfianca`:** de 0 a 1, a probabilidade de o tema escolhido conter o tema que um professor especialista escolheria.

Responda só com o JSON pedido. Escreva `nucleo` primeiro, em uma frase.

# Temas (nível 1)

{{arvore}}
