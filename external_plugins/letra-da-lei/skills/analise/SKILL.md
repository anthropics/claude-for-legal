---
name: letra-da-lei:analise
version: 0.1.0
description: Diagnostica a fase de um processo cível ou trabalhista e redige a peça cabível (réplica, recursos, cumprimento de sentença, embargos, ações autônomas etc.), fundamentada. Use para "o que faço agora?", "perdi a sentença, como recorro?", "cabe [peça/recurso]?". Não use para petição inicial, contestação ou fundamentação judicial — há skills próprias.
argument-hint: "[fase do processo ou documento recebido — ex.: 'recebi a contestação' ou caminho do PDF da sentença]"
---

# /analise

## ⚠️ PASSO ZERO — OBRIGATÓRIO ANTES DE QUALQUER RASCUNHO

**Não produza nenhuma peça antes de completar o intake.** Esta skill serve a múltiplos momentos processuais — uma peça feita sem diagnóstico da fase é, em regra, inútil ou danosa. Use `AskUserQuestion` para coletar as informações em bloco — máximo 4 perguntas por rodada.

### Perguntas obrigatórias — use AskUserQuestion

**Rodada 1 — Fase e documentos:**
- **O que acabou de acontecer no processo?** (Ex.: "recebi a contestação", "a sentença saiu ontem e perdi", "o juiz deferiu a tutela do autor", "ganhei e quero cobrar".) Se o usuário tiver o(s) documento(s) gerado(s) nessa fase, pedir o arquivo ou o texto colado.
- **Qual é o rito processual?** — procedimento comum, JEC (juizado especial), trabalhista, Fazenda Pública, outro?
- **Qual parte o usuário representa?** — autor(a), réu(é), ambos?
- **Há prazo correndo?** Se sim, qual é a data de publicação/intimação do ato e qual a data-limite que o usuário conhece?

> **Guardrail obrigatório:** Se o usuário não fornecer nenhuma informação sobre a fase do processo e nenhum documento, **não produza nada.** Explique que sem saber em que ponto o processo está, qualquer peça seria genérica e possivelmente inadequada. Ofereça as perguntas acima. **Não ceda se o usuário insistir.** Veja Passo 1 para o roteiro de recusa.

### Protocolo "Informar manualmente" — obrigatório

Após cada rodada de `AskUserQuestion`, verifique se alguma resposta foi **"Informar manualmente"**. Se sim, **não prossiga para a próxima etapa.** Compile todos os itens marcados dessa forma em uma única mensagem e solicite ao usuário que forneça os dados antes de continuar:

> "Você marcou os seguintes itens para preenchimento manual. Por favor, informe cada um antes de prosseguirmos:
> - [item 1]
> - [item 2]
> - ..."

Só avance para a redação quando **todos** os itens "Informar manualmente" tiverem sido respondidos ou explicitamente descartados pelo usuário (ex.: "não tenho esse dado" → marcar `[VERIFICAR]`).

---

1. Colete os documentos e a descrição da fase (Passo 0 acima).
2. **Diagnostique a fase processual** e mapeie qual peça é cabível (Passo 2).
3. **Confirme o diagnóstico com o usuário** antes de redigir qualquer linha.
4. Faça o intake específico para a peça identificada (Passo 3).
5. **Chame `buscar_artigos` para todo dispositivo que entrar na peça** — sem exceção.
6. Estruture e gere o `.docx` + `NOTAS.md` (Passos 4 a 6).

---

# Análise Processual e Minuta

## Propósito

O advogado sabe o que aconteceu; nem sempre sabe qual é a próxima peça, ou como estruturá-la com rigor. Esta skill lê o que está nos autos — ou o que o usuário descreveu — identifica o momento processual, propõe a peça mais adequada e redige o rascunho com fundamentação verificada lei por lei.

O que separa esta skill das demais:

1. **Ela diagnostica antes de redigir.** Nenhuma linha de peça sai sem que a fase processual esteja identificada e confirmada pelo usuário.
2. **Ela cobre a fase pós-postulação no rito comum e trabalhista:** réplica, recursos (apelação, recurso ordinário, agravo, embargos), cumprimento de sentença e execução de obrigação.
3. **Ela não adivinha intenção.** Se o usuário quer recorrer mas a sentença foi favorável, a skill pergunta antes de produzir.

O rascunho gerado **não é peça pronta** — é andaime revisável. Quem assina, ajusta tom e decide estratégia é a pessoa habilitada na OAB.

## Regra absoluta — fontes da peça

### Fonte 1 — Lei federal (MCP)

**Toda citação de lei federal nesta peça vem do MCP da Letra da Lei.** Sem exceção. **Carregue a skill `letra-da-lei:pesquisa` e siga-a** para qualquer busca — ela define as ferramentas (`buscar_artigos`, `acervo · consultar`, `acervo · listar`, `reclame_aqui`), os parâmetros (`query`, `norma`), os campos retornados e as verificações de vigência (`situacao`) e de texto integral (`is_truncated` → `consultar`). Memória do modelo é proibida para citar artigo — leis mudam.

Regras desta peça (além da `pesquisa`):
- Citação sem `citacao` + `source_url` da ferramenta → não entra; vira `[CITAÇÃO PENDENTE]`.
- `situacao` ≠ `vigente` → `[VERIFICAR VIGÊNCIA — situação: <X>]`.
- Norma estadual/municipal/infralegal → `[FORA DO CORPUS]`.
- Busca do MCP vazia, contraditória ou irrelevante? Registre a lacuna via `acervo · reclame_aqui` antes de seguir.

### Fonte 2 — Jurisprudência (MCP)

Jurisprudência verificada via MCP da Letra da Lei é uma fonte válida para **todas as peças**. Use as ferramentas conforme o escopo:

- **Federal (STF/STJ/TST/CARF):** `jurisprudencia-federal · buscar_precedentes` (busca ampla — súmulas, temas, OJs, acórdãos) ou `jurisprudencia-federal · buscar_vinculantes` (restringe a precedentes vinculantes do art. 927 CPC: súmulas vinculantes, temas de repercussão geral, temas repetitivos). Filtre por `autoridade` (`STF`, `STJ`, `TST`, `CARF`).
- **Estadual — IRDRs (TJs):** `jurisprudencia-estadual · buscar_vinculantes` (ferramenta distinta) com o parâmetro **obrigatório** `localidade` (sigla da UF, ex.: `"AM"`, ou `"BR"` para busca nacional). IRDR vincula apenas na UF que o decidiu.

**Força do precedente — campo `eficacia` retornado pelo MCP:**
- `vinculante` = observância obrigatória (art. 927 CPC) — citar em qualquer peça sem restrição adicional.
- `obrigatoria` = forte deferência (ex.: súmulas comuns) — citar com o enunciado literal.
- `persuasiva` = subsídio argumentativo — citar com o marcador `[JURISPRUDÊNCIA PERSUASIVA — revisar pertinência ao caso antes do protocolo]`.

**Formato de citação de jurisprudência no rascunho e no .docx:**

```
    [Enunciado literal retornado pelo MCP — sem aspas, recuado 1,25 cm à esquerda,
     alinhamento justificado, fonte 1pt menor que o corpo do texto]
    Fonte: [autoridade] | [tipo] | search_id: [search_id] | eficacia: [eficacia]

[Linha em branco — texto principal retoma aqui]
```

Se o MCP retornar enunciado truncado (`is_truncated: true`), chamar `acervo · consultar` (`dominio: "jurisprudencia"`, `esfera: "federal"` ou `"estadual"`, com os `search_ids` da busca ou uma `citacao` conhecida) para obter o texto integral antes de citar.

**Resultado zero ou precedente não pertinente:** inserir `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]`. Nunca copiar enunciado de memória.

**Para o Recurso Extraordinário (RE ao STF):** jurisprudência do STF é estruturalmente necessária. Use `jurisprudencia-federal · buscar_precedentes` com `autoridade: "STF"` para localizar o Tema de Repercussão Geral aplicável. Se o MCP retornar resultado pertinente, cite com o formato acima (sem marcador adicional se `eficacia: vinculante`). Se não retornar, inserir `[JURISPRUDÊNCIA — confirmar Tema e tese antes do protocolo]` em vermelho no .docx.

### Fonte 3 — Autos do processo (petições anteriores)

Quando o usuário enviar o processo completo ou documentos dos autos, a skill pode **extrair e citar conteúdo das peças já produzidas** — especialmente petições anteriores da parte que o usuário representa (inicial, apelação, embargos de declaração etc.).

Regras para uso de fonte dos autos:
- Prioridade: petições anteriores assinadas pelo(a) advogado(a) do usuário, pois revelam as teses já sustentadas e o que foi prequestionado.
- O acórdão recorrido e outras decisões judiciais dos autos **não são jurisprudência** — são objeto do recurso e podem ser citados literalmente para demonstrar o cabimento ou o erro da decisão.
- Ao usar conteúdo dos autos, sinalizar a fonte: `Fonte: [nome do documento nos autos] — [data/ID do documento]`.
- Nunca atribuir à parte contrária argumento que não conste dos autos.

**Formato de citação de documento dos autos no .docx:**

```
    [Trecho literal extraído do documento — sem aspas, recuado 1,25 cm,
     alinhamento justificado, fonte 1pt menor que o corpo]
    Fonte: [nome do documento] — [data/ID] — autos nº [número do processo]

[Linha em branco — texto principal retoma aqui]
```

**Formato obrigatório de citação no rascunho e no .docx:**

```
    [Texto literal retornado pelo MCP — sem aspas, recuado 1,25 cm à esquerda,
     alinhamento justificado, fonte 1pt menor que o corpo do texto]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: [lei_slug]

[Linha em branco — texto principal retoma aqui, com formatação normal]
```

Regras de formatação da citação no .docx:
- **Recuo:** margem esquerda deslocada 1,25 cm (720 DXA) em relação ao texto principal.
- **Alinhamento:** justificado.
- **Fonte:** 1pt menor que o corpo (se o corpo for 12pt, a citação é 11pt).
- **Sem aspas:** o texto da lei não leva aspas de abertura nem de fechamento.
- **Fonte abaixo:** a linha "Fonte: ..." vem imediatamente após o texto da lei, na mesma formatação recuada e menor. Não vem antes.
- **Linha em branco após:** após o bloco citação + fonte, uma linha em branco separa do próximo parágrafo de texto principal.

Se o bloco `Fonte:` não puder ser preenchido (citacao ou source_url ausentes), o artigo não foi buscado via MCP — não entra na peça.

## Passo 1 — Guardrail: sem fase, sem peça

Se o usuário não forneceu:
- nenhuma descrição do que aconteceu no processo, **E**
- nenhum documento (inicial, contestação, sentença, decisão, etc.),

responda com clareza e firmeza:

> "Para redigir a peça certa, preciso saber em que ponto o processo está. Sem essa informação, qualquer minuta seria genérica e possivelmente inadequada para o seu caso. Me conta: (a) o que acabou de acontecer? (b) qual é o documento mais recente do processo — contestação, sentença, decisão interlocutória, algo do tribunal? (c) você representa o(a) autor(a) ou o(a) réu(é)?"

Se o usuário insistir ("monta uma apelação genérica", "faz um modelo de réplica") **mantenha a recusa.** Uma apelação sem a sentença que se ataca não tem como ser fundamentada — ela é pura forma vazia. Explique isso de forma direta, sem julgamento. Não ceda nas duas insistências. Resposta direta, sem moralismo.

## Passo 2 — Diagnóstico da fase e mapa de peça cabível

Após receber os documentos ou a descrição da fase, diagnostique e mapeie:

| Fase identificada | Peça cabível | Base legal |
|---|---|---|
| Autor recebeu contestação — réu arguiu matérias do art. 337 ou fatos extintivos/modificativos/impeditivos | Réplica **obrigatória** | CPC arts. 350-351 |
| Autor recebeu contestação — réu não arguiu matérias novas | Réplica **facultativa** (estratégica) | CPC art. 350 |
| Parte precisa de medida urgente antes de ajuizar a ação principal — urgência que antecipa o próprio bem da vida pretendido | Tutela antecipada antecedente | CPC art. 303 |
| Parte precisa de medida urgente para **assegurar** o resultado da ação principal — não antecipa o bem da vida, mas garante a utilidade do processo futuro | Tutela cautelar antecedente | CPC arts. 305-310 |
| Parte perdeu sentença — rito comum ou especial (não JEC, não trabalhista) | Apelação | CPC arts. 1.009-1.014 |
| Parte recebeu decisão interlocutória que consta no rol do art. 1.015 do CPC | Agravo de instrumento | CPC arts. 1.015-1.020 |
| Parte recebeu sentença/decisão com omissão, contradição, obscuridade ou erro material | Embargos de declaração | CPC arts. 1.022-1.026 |
| Parte ganhou sentença de pagar quantia — quer cobrar | Cumprimento de sentença (quantia) | CPC arts. 523-527 |
| Parte ganhou sentença de obrigação de fazer/não fazer — quer cobrar | Cumprimento de sentença (obrigação) | CPC art. 536 |
| Parte ganhou sentença de entregar coisa — quer cobrar | Cumprimento de sentença (entrega) | CPC art. 538 |
| Executado quer se defender em cumprimento de sentença de quantia certa — transcorridos os 15 dias do art. 523 sem pagamento | Impugnação ao cumprimento de sentença | CPC art. 525 |
| Executado quer se defender em execução de **título extrajudicial** (cheque, nota promissória, contrato, CDA etc.) | Embargos à execução | CPC arts. 914-917 |
| Executado quer arguir matéria de **ordem pública** (prescrição, nulidade do título, ilegitimidade) **sem penhora prévia e sem dilação probatória**, em qualquer execução | Exceção de pré-executividade | Construção pretoriana — STJ Súmula 393; âncora normativa: CPC art. 803, par. único |
| **Terceiro que não é parte** no processo sofre penhora, arresto ou constrição sobre bem seu | Embargos de terceiro | CPC arts. 674-681 |
| Parte perdeu sentença da Vara do Trabalho | Recurso ordinário trabalhista | CLT art. 895, I |
| Parte perdeu sentença de juizado especial cível (JEC) | Recurso inominado | Lei 9.099 art. 41 |
| Parte perdeu acórdão de TRF, TJ ou TST e quer levar questão constitucional ao STF — após esgotadas as vias ordinárias (inclusive embargos de declaração para prequestionamento) | Recurso Extraordinário | CF art. 102, III, "a" + CPC arts. 1.029-1.035 |
| Parte perdeu acórdão de TRF ou TJ e quer levar questão de direito federal infraconstitucional ao STJ | Recurso Especial (REsp) | CF art. 105, III + CPC arts. 1.029-1.032 |
| ⚠️ Acórdão de TRF ou TJ viola **simultaneamente** lei federal infraconstitucional **e** a Constituição Federal | **RE + REsp interpostos simultaneamente** em petições separadas ao mesmo Presidente/VP do tribunal de origem | CF arts. 102 III "a" e 105 III + CPC art. 1.031 — a não interposição de um implica preclusão da matéria correspondente |
| Presidente/VP do tribunal de origem negou seguimento ao RE/REsp por inadmissibilidade geral (art. 1.030, V, CPC) — motivo não é conformidade com repetitivo/RG | Agravo em RE ou Agravo em REsp (ARE/AREsp) ao tribunal superior | CPC art. 1.042 |
| Acórdão de turma do STJ ou STF em RE/REsp **diverge de outro acórdão do mesmo tribunal** sobre a mesma questão | Embargos de divergência | CPC arts. 1.043-1.044 |
| Presidente/VP do tribunal de origem negou seguimento ao RE ou REsp **com fundamento em conformidade com entendimento de casos repetitivos ou RG** (art. 1.030, I ou III, CPC) | Agravo Interno ao próprio tribunal de origem | CPC arts. 1.021 + 1.030, §2º |
| Relator do tribunal (qualquer instância) proferiu decisão monocrática e a parte quer submeter ao colegiado | Agravo Interno | CPC art. 1.021 |
| Tribunal **denegou** HC/MS/HD/MI em **competência originária** (única instância) e a parte vencida quer recorrer | Recurso Ordinário Constitucional | CF art. 102, II (ao STF) ou 105, II (ao STJ) + CPC arts. 1.027-1.028 |
| Ato/decisão usurpou competência de tribunal, descumpriu decisão dele, ou contrariou súmula vinculante, decisão do STF em controle concentrado, IRDR ou IAC — **antes** do trânsito em julgado | Reclamação constitucional | CPC arts. 988-993 |
| Decisão **de mérito transitada em julgado** padece de um dos vícios do art. 966 (incompetência absoluta, violação manifesta de norma, prova falsa, prova nova, erro de fato etc.) | Ação Rescisória | CPC arts. 966-975 |
| Terceiro (que não é parte na ação) pretende a coisa ou o direito disputado entre autor e réu — sentença ainda não proferida | Oposição | CPC arts. 682-686 |
| **Poder Público** quer suspender liminar/sentença concessiva de MS ou tutela de urgência que cause grave lesão à ordem, saúde, segurança ou economia públicas | Suspensão de segurança | Lei 12.016/2009 art. 15 (MS) / Lei 8.437/1992 art. 4 [FORA DO CORPUS] (outras ações) |
| Há **múltiplos processos** com mesma questão unicamente de direito e risco de decisões divergentes — parte, MP ou Defensoria quer fixar tese vinculante no tribunal | Suscitação de IRDR | CPC arts. 976-987 |
| ⚠️ Situação não coberta por nenhum módulo acima | **Módulo subsidiário** — a skill diagnostica a fase e orienta o próximo passo, mas informa que não há minuta específica disponível | — |

**Antes de prosseguir, devolva o diagnóstico ao usuário para confirmação:**

> "Com base no(s) documento(s) fornecido(s), a fase que identifico é: [fase]. A peça mais adequada é: [peça], com fundamento no(s) art(s). [X] do [diploma]. Confirmo o entendimento antes de redigir — está correto?"

Só redigia após a confirmação. Se o usuário discordar, pergunte o que está errado e ajuste.

## Passo 3 — Intake específico por tipo de peça

Após confirmar o diagnóstico, faça o intake específico para a peça identificada. Use `AskUserQuestion` — máximo 4 perguntas por rodada.

> **Distinção estrutural — recursos × ações autônomas de impugnação (ler antes de qualquer módulo).**
> A natureza da peça molda o intake e a estrutura. Não tratar as duas categorias do mesmo jeito:
>
> - **Recursos** (apelação, agravo de instrumento, embargos de declaração, recurso ordinário trabalhista, recurso inominado, RE, REsp, ARE/AREsp, agravo interno, recurso ordinário constitucional): impugnam decisão **dentro do mesmo processo** e têm **prazo de interposição** (em regra em dias úteis, contados da intimação). A peça abre por uma seção de **tempestividade**.
> - **Ações autônomas de impugnação** (reclamação, ação rescisória): **não são recursos** — instauram **processo novo**. O intake e a estrutura aproximam-se de uma **petição inicial** (qualificação completa das partes, causa de pedir, pedido, valor da causa, instrução documental — requisitos do art. 319 e seguintes), não do fluxo recursal. **Não há "tempestividade recursal"** — há cabimento de ação e, conforme o caso, prazo decadencial ou limite negativo:
>   - **Ação rescisória:** prazo **decadencial** (não de interposição). 2 anos com termo inicial **variável** conforme a hipótese do art. 966 — regra geral do trânsito em julgado da última decisão; **descoberta da prova nova** no inciso VII (teto de 5 anos); **ciência da simulação/colusão** para terceiro prejudicado e MP (art. 975, §§2º e 3º). Ver módulo da rescisória.
>   - **Reclamação:** sem prazo de interposição, mas **inadmissível após o trânsito em julgado** da decisão reclamada (art. 988, §5º, I). Ver módulo da reclamação.
>
> Tratar uma ação autônoma como recurso (ou vice-versa) é erro estrutural — e é o erro que mais escapa em refatorações. Confirmar a natureza antes de escolher o esqueleto da peça.

---

### Como usar os módulos

Cada família de peça está em um arquivo de `references/`. **Depois de confirmar o diagnóstico (Passo 2), abra apenas o arquivo da peça identificada e siga o módulo** — não carregue os outros. Cada arquivo é autossuficiente quanto ao intake e à estrutura; a **Regra absoluta** (Fonte 1/2/3) e os **Passos 4–6** abaixo valem para todos.

| Peça diagnosticada | Arquivo de referência |
|---|---|
| Réplica; tutela antecipada/cautelar antecedente | `references/replica-e-tutelas.md` |
| Apelação, agravo de instrumento, embargos de declaração, recurso ordinário trabalhista, recurso inominado (JEC), recurso ordinário constitucional, agravo interno | `references/recursos-ordinarios.md` |
| Recurso extraordinário, recurso especial, agravo em RE/REsp, embargos de divergência | `references/recursos-extraordinarios.md` |
| Cumprimento de sentença (quantia/obrigação), impugnação ao cumprimento, embargos à execução, exceção de pré-executividade | `references/cumprimento-e-execucao.md` |
| Reclamação, ação rescisória, oposição, embargos de terceiro, suspensão de segurança | `references/acoes-autonomas.md` |
| Suscitação de IRDR | `references/irdr.md` |

### 3.6 — Módulo subsidiário — situação não coberta por módulo específico

Quando o diagnóstico do Passo 2 identificar a fase processual mas não houver módulo de minuta correspondente, a skill não recusa o trabalho — ela:

1. **Descreve a fase e a peça cabível** com clareza, indicando o fundamento legal (buscar via MCP o que for possível).
2. **Informa ao usuário** que não há módulo específico ainda disponível.
3. **Oferece produzir uma estrutura básica** com intake mínimo, usando os princípios gerais da skill (dispositivos via MCP, sem jurisprudência sem marcador, marcadores nos pontos incertos).
4. **Registra o gap** para que o usuário saiba que a peça gerada é menos estruturada que as produzidas por módulos dedicados.

Resposta padrão quando ativado:

> "Identifiquei que a fase processual é [fase] e que a peça cabível seria [peça], com fundamento no(s) art(s). [X] do [diploma]. Esta skill ainda não tem um módulo dedicado para esse tipo de peça. Posso produzir uma minuta estrutural básica — menos detalhada que as peças com módulo próprio — ou prefere que eu apenas oriente os próximos passos processuais sem redigir o documento?"

---

## Passo 4 — Pesquisa legal (MCP)

Para cada dispositivo identificado no diagnóstico e na estrutura:

1. Identifique a norma (CPC, CLT, CC, lei especial).
2. Chame `buscar_artigos` com query precisa + `norma`.
3. Registre o bloco completo no formato padrão de citação.
4. Norma fora do corpus → `[FORA DO CORPUS]`.

**Prioridades de busca por tipo de peça:**

| Peça | Dispositivos essenciais | norma (sigla/slug) |
|---|---|---|
| Réplica | arts. 350, 351, 435 | Lei-13105-2015 |
| Tutela antecipada antecedente | arts. 303 (caput e §§1º-6º), 304 (estabilização) | Lei-13105-2015 |
| Tutela cautelar antecedente | arts. 305, 306, 307, 308, 309, 310 | Lei-13105-2015 |
| Apelação | arts. 1.009, 1.010, 1.012, 1.003 §5º, 85 §11 | Lei-13105-2015 |
| Agravo de instrumento | art. 1.015 (inciso específico), 1.016-1.020 | Lei-13105-2015 |
| Embargos de declaração | arts. 1.022, 1.023, 1.024 | Lei-13105-2015 |
| Cumprimento (quantia) | arts. 523, 523 §1º, 835 | Lei-13105-2015 |
| Cumprimento (obrigação) | arts. 536, 537 | Lei-13105-2015 |
| Impugnação ao cumprimento de sentença | arts. 525 (caput e §§1º, 4º, 5º, 6º, 12-14) | Lei-13105-2015 |
| Embargos à execução | arts. 914 (caput e §§1º-2º), 915 (caput e §§1º-3º), 917 (caput e §§1º-7º), 919 (caput e §§1º-5º) | Lei-13105-2015 |
| Exceção de pré-executividade | art. 803 (caput e par. único — base normativa mais próxima), art. 924 (extinção da execução); dispositivo de prescrição/decadência aplicável à obrigação via MCP; cabimento é pretoriano — marcador obrigatório | Lei-13105-2015 + lei especial da obrigação |
| Embargos de terceiro | arts. 674 (caput e §§1º-2º), 675 (caput e par. único), 676, 677 (caput e §§1º-4º), 678 (caput e par. único), 679, 681; art. 792 se fraude à execução | Lei-13105-2015 |
| Recurso ordinário trabalhista | CLT arts. 895, 899 | DL-5452-1943 |
| Recurso inominado JEC | Lei 9.099 arts. 41, 42 | [verificar norma — provável Lei-9099-1995] |
| Recurso Extraordinário | CF art. 102 III "a"; CPC arts. 1.029, 1.003 §5º, 1.035, 1.037; dispositivos constitucionais violados; art. 1.031 se simultâneo com REsp | CF-1988 + Lei-13105-2015 |
| Recurso Especial | CF art. 105 III; CPC arts. 1.029, 1.003 §5º, 1.032, 85 §11; dispositivos de lei federal violados; art. 1.031 se simultâneo com RE | CF-1988 + Lei-13105-2015 |
| Agravo em RE / Agravo em REsp | CPC arts. 1.042, 1.030 V, 1.003 §5º | Lei-13105-2015 |
| Embargos de divergência | CPC arts. 1.043 (caput e §§1º-5º), 1.044 (caput e §§1º-2º); dispositivo legal/constitucional da questão de fundo via MCP; acórdão paradigma com `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP]` | Lei-13105-2015 |
| Agravo Interno | CPC arts. 1.021, 1.021 §2º; se hipótese 2: também art. 1.030 §2º | Lei-13105-2015 |
| Recurso Ordinário Constitucional | CF art. 102 II ou 105 II; CPC arts. 1.027, 1.028; prazo: 15 dias úteis (art. 1.003 §5º) na regra geral, inclusive HC ao STF (102 II "a"); 5 dias (Lei 8.038 art. 30 — `[VERIFICAR/FORA DO CORPUS]`) só no HC ao STJ (105 II "a"); dispositivo legal violado | CF-1988 + Lei-13105-2015 |
| Reclamação constitucional | CPC arts. 988 (caput, inciso e §§4º/5º), 989, 992 | Lei-13105-2015 |
| Ação Rescisória | CPC arts. 966 (inciso e §§1º/5º/6º), 967, 968 (I, II, §§1º/2º), 969, 970, 975 (caput e §§1º/2º/3º) | Lei-13105-2015 |
| Oposição | CPC arts. 682, 683 (caput e par. único), 684, 685 (caput e par. único), 686 | Lei-13105-2015 |
| Suspensão de segurança | Lei 12.016/2009 art. 15 (caput e §§1º-5º) no corpus; Lei 8.437/1992 art. 4 [FORA DO CORPUS — transcrever manualmente] | Lei-12016-2009 |
| Suscitação de IRDR | CPC arts. 976 (caput e §§1º-5º), 977 (caput e par. único), 978, 980 (caput e par. único), 982 (caput e §§1º-5º), 985 (caput e §§1º-2º), 987 (caput e §§1º-2º); dispositivo legal controvertido via MCP | Lei-13105-2015 |

**Sem suplementação silenciosa.** MCP retornou pouco/nada → pergunte ao usuário antes de buscar em outro lugar.

## Passo 5 — Conferências obrigatórias antes da entrega

1. **Diagnóstico confirmado.** O tipo de peça foi confirmado pelo usuário antes de redigir?
2. **Prazo buscado via MCP.** O prazo aplicável foi verificado com o texto literal da lei (não de memória)? O texto está nas notas?
3. **Cabimento verificado.** Para agravo: o inciso do art. 1.015 está explícito? Para recurso ordinário trabalhista: o prazo é de 8 dias corridos (não úteis)?
4. **Auditoria de MCP — obrigatória.** Para cada dispositivo citado na peça, o bloco `citacao / source_url` está presente? Citação sem esses campos = foi de memória = **inválida**. Remova ou converta em `[CITAÇÃO PENDENTE]`.
5. **Auditoria de jurisprudência — obrigatória.** Há alguma súmula, acórdão, REsp, RE, OJ ou qualquer referência a decisão judicial na peça?
   - **Peças ordinárias:** Se sim, remova imediatamente e substitua por `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]`.
   - **Recurso Extraordinário:** Toda jurisprudência deve estar marcada com `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, data e texto exato do julgado antes do protocolo]`. Se houver referência a precedente **sem esse marcador**, adicione imediatamente. Referências a Temas de Repercussão Geral sem marcador = falha grave.
6. **Marcadores remanescentes.** `[VERIFICAR]`, `[CITAÇÃO PENDENTE]`, `[FORA DO CORPUS]`, `[JURISPRUDÊNCIA]`, `[DOC. A NUMERAR]` — todos listados no bloco de notas?
7. **Depósito recursal (trabalhista).** Se empregador recorrente, o depósito foi mencionado e o valor marcado como `[FORA DO CORPUS]`?

## Formatação padrão do documento

Todo o texto da peça — cabeçalho, qualificações, fatos, fundamentos, pedidos — deve estar em **alinhamento justificado**. Não há exceção para nenhuma seção. A citação de lei segue as regras próprias da seção "Regra absoluta" (recuada, justificada, fonte menor), mas o restante do documento também é justificado — não alinhado à esquerda.

No .docx, isso equivale a `AlignmentType.JUSTIFIED` (docx-js) em todos os parágrafos.

## Passo 6 — Output

Salve dois arquivos:

- `outputs/[tipo-peça]-[slug]-[YYYY-MM-DD].docx`
  - Tipos de prefixo: `replica`, `tutela-antecipada-antecedente`, `tutela-cautelar-antecedente`, `apelacao`, `agravo-instrumento`, `embargos-declaracao`, `cumprimento-sentenca`, `impugnacao-cumprimento`, `embargos-execucao`, `excecao-pre-executividade`, `embargos-terceiro`, `recurso-ordinario-trt`, `recurso-inominado-jec`, `recurso-extraordinario`, `recurso-especial`, `agravo-are`, `agravo-aresp`, `agravo-interno`, `recurso-ordinario-constitucional`, `embargos-divergencia`, `reclamacao`, `acao-rescisoria`, `oposicao`, `suspensao-seguranca`, `suscitacao-irdr`
- `outputs/[tipo-peça]-[slug]-NOTAS.md`

**Marcadores em vermelho — obrigatório.** Após gerar o `.docx`, execute o script `colorir_marcadores.py` para aplicar cor vermelha e negrito a todos os marcadores inline:

```bash
python scripts/colorir_marcadores.py outputs/[tipo-peça]-[slug]-[YYYY-MM-DD].docx
```

O script sobrescreve o arquivo no mesmo caminho. Se o script não estiver disponível, aplique manualmente cor `#FF0000` a cada ocorrência de `[VERIFICAR...]`, `[CITAÇÃO PENDENTE]`, `[FORA DO CORPUS...]`, `[JURISPRUDÊNCIA...]`, `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP...]` e `[DOC. A NUMERAR]`.

**Aviso obrigatório ao usuário — incluir sempre após entregar a minuta:**

> ⚠️ **ITENS EM VERMELHO — VERIFICAÇÃO NECESSÁRIA ANTES DO PROTOCOLO**
> Os trechos marcados em vermelho no documento indicam pontos que precisam ser resolvidos pelo(a) advogado(a) antes de assinar e protocolar a peça. Revise cada marcador:
> - `[VERIFICAR: ...]` — dado não confirmado, presumido ou ausente
> - `[CITAÇÃO PENDENTE]` — artigo não localizado via MCP; incluir manualmente com fonte verificada
> - `[FORA DO CORPUS]` — norma estadual, municipal ou tabela do tribunal; verificar na fonte local
> - `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]` — espaço reservado para súmula ou julgado (peças ordinárias)
> - `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, data e texto exato do julgado antes do protocolo]` — precedente citado no corpo do RE que precisa ser conferido pelo(a) advogado(a) antes do protocolo
> - `[DOC. A NUMERAR]` — documento referenciado sem número; numerar ao juntar
>
> Nenhum desses marcadores pode permanecer na peça no momento do protocolo.

```
## Notas de revisão — [Tipo de Peça] — [data]

**Skill:** analise (Letra da Lei)
**Fase diagnosticada:** [fase]
**Peça produzida:** [tipo]
**Fonte da legislação:** MCP Letra da Lei (texto verbatim do Planalto)

### Prazo
- Prazo legal: [N] dias [úteis/corridos] (art. [X] do [diploma])
  Fonte MCP: [citacao] | [source_url]
- Data de publicação/intimação: [data]
- Data-limite estimada: [VERIFICAR — confirmar no sistema do tribunal,
  considerando feriados forenses e suspensões locais — fora do corpus desta skill]

### Marcadores inline a resolver
- `[VERIFICAR: ...]` — N ocorrências
- `[CITAÇÃO PENDENTE]` — N
- `[FORA DO CORPUS]` — N (norma estadual/infralegal/tabela do tribunal)
- `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]` — N (peças ordinárias)
- `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, data e texto exato do julgado antes do protocolo]` — N (RE/reclamação/rescisória)
- `[DOC. A NUMERAR]` — N

### Dispositivos citados (todos verificados via MCP)
- [lei_slug]-[Art-N] — [source_url]
- ...

### Pontos abertos para a(o) advogado(a)
- [premissas assumidas que merecem confirmação]
- [decisões estratégicas que a skill não pode tomar]
- [depósito recursal, preparo, custas — verificar tabelas locais]

### O que esta skill NÃO fez
- Não calculou o prazo final no sistema do tribunal — feriados forenses locais
  são [FORA DO CORPUS].
- Não inseriu jurisprudência — espaços marcados `[JURISPRUDÊNCIA]` precisam
  ser preenchidos pelo(a) advogado(a).
- Não confirmou o valor do depósito recursal (trabalhista) — consultar tabela
  vigente do TST.
- Não protocolou nada.
```

## O que esta skill NÃO faz

- **Não protocola.** Nunca. Protocolar é ato privativo de advogado(a) habilitado(a).
- **Não calcula prazo final.** Devolve o texto legal do prazo (via MCP) e os marcos. A contagem exata no PJe/eSAJ — com feriados forenses locais, recesso (CPC art. 220), suspensões — é do(a) advogado(a).
- **Não confirma cabimento de agravo sem consultar o art. 1.015 via MCP.** O rol é taxativo; a skill verifica o inciso antes de afirmar que cabe agravo.
- **Não insere jurisprudência sem marcador.** Em peças ordinárias, jurisprudência é vedada e sai como `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]`. No Recurso Extraordinário, precedentes do STF podem entrar no corpo da peça, mas sempre marcados com `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar número, data e texto exato do julgado antes do protocolo]`. Nenhum precedente entra limpo — sem marcador — em nenhuma peça.
- **Não cobre normas estaduais ou tabelamentos do tribunal.** Custas, depósito recursal, tabela de honorários periciais — `[FORA DO CORPUS]`.
- **Não decide estratégia.** "Apelar ou embargar primeiro?" é decisão profissional. A skill produz a peça que o(a) advogado(a) escolheu.
- **Não substitui o(a) advogado(a).** Produz rascunho — assinatura, responsabilidade e estratégia são da pessoa habilitada na OAB.
