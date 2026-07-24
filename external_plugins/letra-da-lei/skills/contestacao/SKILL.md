---
name: letra-da-lei:contestacao
version: 0.1.0
description: Redige contestação cível brasileira (CPC arts. 335–342) — preliminares (art. 337), mérito com impugnação especificada e eventual reconvenção, fundamentada. Use para "redige uma contestação", "preciso contestar", "fui citado, monta a defesa", "resposta à inicial". Não use para recurso, embargos ou peças posteriores à fase postulatória.
argument-hint: "[descrição curta — ex.: 'contestação em ação de cobrança' ou caminho do PDF da inicial]"
---

# /contestacao

## ⚠️ PASSO ZERO — OBRIGATÓRIO ANTES DE QUALQUER RASCUNHO

**Não escreva uma linha da peça antes de completar o intake abaixo.** Use `AskUserQuestion` para coletar as informações em bloco — máximo 4 perguntas por rodada. Se faltou dado essencial após a primeira rodada, faça uma segunda antes de prosseguir.

### Perguntas obrigatórias — use AskUserQuestion

**Rodada 1 — A inicial e o processo:**
- A petição inicial está disponível? Peça o arquivo (PDF/DOCX) ou que o usuário cole o texto. **Sem a inicial, não há contestação útil** — informar ao usuário antes de seguir.
- **Número do processo** e data da citação (ou data da juntada do AR/mandado — art. 335 do CPC determina o prazo a partir daí).
- **Rito processual** — procedimento comum, JEC (juizado especial), juizado da Fazenda Pública, outro?
- **Réu qualificado** — nome completo, CPF/CNPJ, endereço; advogado(a) responsável pela defesa.

**Rodada 2 — Versão do réu e estratégia defensiva:**
- **Versão dos fatos** pela ótica do(a) réu(é) — onde diverge da narrativa do autor?
- **Documentos disponíveis** para a defesa — listar os que o usuário já tem.
- **Há preliminares a arguir?** (incompetência, prescrição, ilegitimidade, coisa julgada, falta de interesse — art. 337 do CPC). Para cada sim, pedir a fundamentação fática.
- **Há pretensão própria do réu** a formular contra o autor (reconvenção no rito comum, ou pedido contraposto no JEC)?
- **Provas** que o réu quer produzir — documental (já juntar), testemunhal (rol), pericial (área), depoimento pessoal do autor?

> **Regra de ouro:** impugnar fato sem fundamentação é pior do que não impugnar — equivale a confissão ficta (art. 341 do CPC). Não suponha a versão do réu: pergunte. Se o usuário não informar, marque `[VERIFICAR]` e liste no bloco de notas.

### Protocolo "Informar manualmente" — obrigatório

Após cada rodada de `AskUserQuestion`, verifique se alguma resposta foi **"Informar manualmente"**. Se sim, **não prossiga para a próxima etapa.** Compile todos os itens marcados dessa forma em uma única mensagem e solicite ao usuário que forneça os dados antes de continuar:

> "Você marcou os seguintes itens para preenchimento manual. Por favor, informe cada um antes de prosseguirmos:
> - [item 1]
> - [item 2]
> - ..."

Só avance para a redação quando **todos** os itens "Informar manualmente" tiverem sido respondidos ou explicitamente descartados pelo usuário (ex.: "não tenho esse dado" → marcar `[VERIFICAR]`).

---

1. Leia a **inicial** que está sendo contestada (peça o caminho do arquivo ou cole o texto). Sem ela não há contestação útil — só formalismo.
2. Faça o intake defensivo (Passo 2) — fatos da nossa versão, documentos, teses, eventual reconvenção.
3. **Chame `buscar_artigos` para todo dispositivo invocado.** Sem exceção. Preliminares do art. 337 incluem 13 hipóteses — cada uma exige a redação literal do inciso.
4. Monte a peça na estrutura preliminares → mérito → reconvenção → provas → pedidos (Passo 4).
5. Output: `.docx` em `outputs/contestacao-[slug]-[YYYY-MM-DD].docx` + bloco de notas para revisão.

---

# Contestação

## Propósito

A contestação concentra toda a defesa (princípio da eventualidade — CPC art. 336). O que não for alegado aqui está, em regra, precluso. Os fatos não impugnados especificamente presumem-se verdadeiros (art. 341). Por isso a contestação tem uma assimetria perigosa em relação à inicial: a falha na inicial é, em geral, sanável; a falha na contestação, em regra, não é.

Esta skill produz **rascunho com fundamentação jurídica verificada artigo por artigo contra o texto vigente da lei**. A análise estratégica (qual preliminar levantar primeiro, qual fato confessar para fortalecer outro, se cabe reconvenção ou apenas pedido contraposto) é do(a) advogado(a).

## Regra absoluta — fontes da peça

### Fonte 1 — Lei federal (MCP)

**Toda citação de lei federal vem do MCP da Letra da Lei.** Sem exceção. **Carregue a skill `letra-da-lei:pesquisa` e siga-a** para qualquer busca — ela define as ferramentas (`buscar_artigos`, `acervo · consultar`, `acervo · listar`, `reclame_aqui`), os parâmetros (`query`, `norma`), os campos retornados e as verificações de vigência (`situacao`) e de texto integral (`is_truncated` → `consultar`). Memória do modelo é proibida para citar artigo — leis mudam (ex.: Lei 14.905/2024 mudou CC arts. 389 e 406).

Regras desta peça (além da `pesquisa`):
- Citação sem `citacao` + `source_url` da ferramenta → não entra; vira `[CITAÇÃO PENDENTE]`.
- `situacao` ≠ `vigente` → `[VERIFICAR VIGÊNCIA — situação: <X>]`.
- Norma estadual/municipal/infralegal → `[FORA DO CORPUS]`.
- Busca do MCP vazia, contraditória ou irrelevante? Registre a lacuna via `acervo · reclame_aqui` antes de seguir.

**Formato obrigatório de citação de lei no rascunho e no .docx:**

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

Por quê: contestação com dispositivo citado errado destrói a defesa. O juiz lê, vê que o art. invocado não existe ou diz outra coisa, e a tese morre. Pior, a contestação é a peça em que o(a) advogado(a) assume a defesa — a credibilidade construída ou destruída aqui acompanha o processo todo.

### Fonte 2 — Jurisprudência (MCP)

Jurisprudência verificada via MCP da Letra da Lei é uma fonte válida. Use as ferramentas conforme o escopo:

- **Federal (STF/STJ/TST/CARF):** `jurisprudencia-federal · buscar_precedentes` (busca ampla — súmulas, temas, OJs, acórdãos) ou `jurisprudencia-federal · buscar_vinculantes` (restringe a precedentes vinculantes do art. 927 CPC: súmulas vinculantes, temas de repercussão geral, temas repetitivos). Filtre por `autoridade` (`STF`, `STJ`, `TST`, `CARF`).
- **Estadual — IRDRs (TJs):** `jurisprudencia-estadual · buscar_vinculantes` (ferramenta distinta) com o parâmetro **obrigatório** `localidade` (sigla da UF, ex.: `"SP"`, ou `"BR"` para busca nacional). IRDR vincula apenas na UF que o decidiu.

**Força do precedente — campo `eficacia` retornado pelo MCP:**
- `vinculante` = observância obrigatória (art. 927 CPC) — citar sem restrição adicional.
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

## Passo 1 — Ler a inicial

**Pré-requisito não-negociável.** Sem a inicial em mãos, peça:

> "Para redigir a contestação preciso da petição inicial. Você pode (a) colar o texto, (b) anexar o PDF/DOCX, ou (c) descrever os pedidos, a causa de pedir e os documentos mencionados. Sem isso, qualquer contestação que eu produzir será genérica e provavelmente inútil."

Da inicial, extraia (e devolva ao usuário para confirmação antes de prosseguir):

- **Partes** — autor(a), réu(s), litisconsórcio.
- **Pedidos** — listados por letra/numeração, com valor de cada um.
- **Causa de pedir** — fatos narrados + fundamentos invocados.
- **Documentos juntados** — lista pelos `(doc. nº)`.
- **Tutela de urgência** — pedida? deferida?
- **Audiência de conciliação** — designada? data?
- **Rito** — comum, juizado, especial?
- **Data da juntada do AR ou do mandado** (CPC art. 335, III) — para conferir prazo.

## Passo 2 — Intake defensivo

Pergunte (uma por vez se o usuário estiver disperso):

### 2.1 Versão da(o) ré(u)

- O que de fato aconteceu, na visão do(a) ré(u)? Onde diverge da narrativa do autor?
- Que documentos comprovam a versão da(o) ré(u)? (Pedir a juntar.)
- Há comunicações (e-mails, mensagens, atas) entre as partes que mudem a interpretação?

### 2.2 Preliminares possíveis (CPC art. 337)

Pergunte direto, uma a uma — se sim, peça a fundamentação fática:

| Inciso | Preliminar | Pergunta gatilho |
|---|---|---|
| I | Inexistência/nulidade de citação | A citação foi válida? Pessoal? Por hora certa? |
| II | Incompetência absoluta/relativa | O juízo é competente? Foro de eleição? Domicílio do consumidor? |
| III | Incorreção do valor da causa | O valor está coerente com o pedido? |
| IV | Inépcia da petição inicial | Pedido faltando elemento? Causa de pedir confusa? |
| V | Perempção | Mesma demanda já extinta 3x por abandono? |
| VI | Litispendência | Mesma ação correndo em outro lugar? |
| VII | Coisa julgada | Já houve decisão definitiva sobre o mesmo? |
| VIII | Conexão | Há processo conexo? |
| IX | Incapacidade da parte, defeito de representação, falta de autorização | Autor é capaz? Representado? |
| X | Convenção de arbitragem | Há cláusula compromissória? |
| XI | Ausência de legitimidade ou de interesse processual | A(o) autor(a) é parte legítima? Tem interesse? |
| XII | Falta de caução ou de outra prestação que a lei exige como preliminar | Caso de cautio judicatum solvi (autor no estrangeiro)? |
| XIII | Indevida concessão do benefício de gratuidade de justiça | A gratuidade do art. 98 do CPC foi concedida indevidamente? |

Para cada "sim", busque o texto literal do art. 337 inciso correspondente via MCP. Não escreva "art. 337, IV" sem o texto colado ao lado.

### 2.3 Mérito — impugnação especificada dos fatos (art. 341)

**Regra de ouro sobre confissão: nunca confesse fato explicitamente.** Fato verdadeiro que não tem como impugnar → silencie. Não mencione, não destaque, não use a palavra "confesso" em nenhuma hipótese. A única exceção é quando o fato desfavorável é indispensável para construir uma tese própria do réu (ex.: para alegar prescrição, é preciso mencionar a data da violação do direito — mas mesmo assim, use "suposta violação" de forma fluida na narrativa, nunca em destaque isolado como confissão).

Para cada fato narrado na inicial, classifique internamente (para fins de estratégia, não para colocar na peça):

- **Impugnado por divergência** — aconteceu, mas não como o autor narrou. Versão correta: [...]. → Narrar a versão do réu.
- **Impugnado por inexistência** — não aconteceu. → Afirmar diretamente.
- **Verdadeiro mas sem saída** — não impugnar; omitir da contestação. → Não mencionar.
- **Verdadeiro e necessário para tese do réu** — mencionar de forma fluida, com "suposta" ou "alegada", apenas na medida do necessário. → Nunca isolar como linha de confissão.
- **Desconhecido** — não temos como confirmar ou negar; aplicabilidade do art. 341, parágrafo único?

**Cuidado:** o art. 341 lista exceções (representante público sem ônus de impugnar, fatos que dependem de documento da própria parte autora, etc.). Buscar o texto via MCP.

### 2.4 Reconvenção (art. 343)? Pedido contraposto (Lei 9.099/1995 nos juizados)?

- Há pretensão própria do(a) ré(u) contra o(a) autor(a) conexa ao mesmo fato? Valor?
- Se sim — pedido contraposto (juizado) ou reconvenção (rito comum)?
- Buscar art. 343 do CPC via MCP para conferir requisitos.

### 2.5 Provas

- Quais provas o(a) ré(u) quer produzir? Documental (já junta), testemunhal (rol), pericial (área), depoimento pessoal do autor?

## Passo 3 — Pesquisa legal (MCP)

Para cada tese — preliminar OU mérito:

1. Identifique a norma.
2. Chame `buscar_artigos` com query precisa + `norma`.
3. Registre no rascunho o bloco completo no formato padrão de citação:
   ```
       [Texto literal retornado — sem aspas, recuado, justificado, fonte menor]
       Fonte: [citacao] | [source_url] | situação: [situacao] | lei: [lei_slug]

   ```
4. Norma fora do corpus → `[FORA DO CORPUS]`.

**Sem suplementação silenciosa.** MCP retornou pouco/nada → pergunte ao usuário antes de buscar em outro lugar.

## Passo 4 — Estrutura da peça

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DE DIREITO DA [...] VARA [...]
DA COMARCA DE [...]

                                                  Processo nº [...]
                                                  [Classe processual]

[NOME DA(O) RÉ(U)], já qualificado(a) nos autos da ação que lhe move
[NOME DO AUTOR], por seu(sua) advogado(a) infra-assinado(a) (procuração doc. 01),
vem, respeitosamente, à presença de Vossa Excelência, com fundamento no art. 335
do Código de Processo Civil, apresentar

                                C O N T E S T A Ç Ã O

pelos fatos e fundamentos que passa a expor.

I — DAS PRELIMINARES                                   (omitir seção se não houver)

I.1 — [Preliminar 1 — ex.: Da incompetência relativa do juízo (art. 337, II,
       c/c art. 64 do CPC)]

Dispõe o art. 337, II, do CPC:

    [texto literal retornado pelo MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[Aplicação ao caso. Doc. que comprova. Pedido específico — formatação normal.]

I.2 — [Preliminar 2] — mesma estrutura

II — DO MÉRITO

II.1 — DA REALIDADE DOS FATOS  (versão da(o) ré(u))

[Contranarrativa cronológica. Cada divergência ancorada em documento.]

II.2 — DA IMPUGNAÇÃO ESPECIFICADA  (art. 341 do CPC)

Nos termos do art. 341 do CPC:

    [texto literal do art. 341 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015


Quanto aos fatos narrados na inicial, manifesta-se a(o) Ré(u) na forma seguinte:

  a) [fato 1]: IMPUGNADO. [Razão + doc.]
  b) [fato 2]: IMPUGNADO. [Versão do réu + doc. que sustenta.]
  c) [fato 3]: IMPUGNADO POR INEXISTÊNCIA. [Razão + doc.]
  d) [fato 4]: o(a) Ré(u) desconhece — pleiteia que o ônus probatório recaia
     sobre o autor (art. 373, I, do CPC). [Texto literal do art. 373, I.]

II.3 — DO DIREITO

II.3.a — [Tese de mérito 1 — ex.: Da inexistência de defeito do serviço]

Dispõe o art. 14, § 3º, do Código de Defesa do Consumidor:

    [texto literal via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-8078-1990

[Subsunção. 2-4 parágrafos. Formatação normal.]

II.3.b — [Tese 2] — mesma estrutura.

II.4 — DA INVERSÃO DO ÔNUS DA PROVA  (se aplicável, ou para refutar inversão
                                       pedida na inicial)

    [texto literal do art. 6º, VIII, do CDC, ou art. 373, §1º do CPC, via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: [lei_slug]


III — DA RECONVENÇÃO                                   (omitir seção se não houver)

Com fundamento no art. 343 do CPC:

    [texto literal do art. 343 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

apresenta a(o) Ré(u) reconvenção em face do(a) Autor(a) Reconvindo(a), pelos fundamentos a seguir.

[Estrutura: fatos, direito, pedidos, valor da causa da reconvenção.]

IV — DAS PROVAS

Protesta a(o) Ré(u) pela produção de todas as provas em direito admitidas,
especialmente:

  a) documental — em juntada com esta peça (docs. nº [...]);
  b) testemunhal — rol em momento oportuno;
  c) pericial — [especificar área e quesitos serão apresentados na fase
     instrutória];
  d) depoimento pessoal do(a) Autor(a), sob pena de confissão.

V — DOS PEDIDOS

Diante do exposto, requer a(o) Ré(u):

  a) [pedidos preliminares — ex.: a remessa dos autos ao foro competente; a
     extinção sem resolução de mérito por inépcia; o reconhecimento da
     prescrição];
  b) caso superadas as preliminares, no mérito, a TOTAL IMPROCEDÊNCIA dos
     pedidos formulados na inicial;
  c) a condenação do(a) Autor(a) ao pagamento de custas processuais e
     honorários advocatícios (art. 85 do CPC) — [texto literal via MCP];
  d) [se houver reconvenção] a procedência da reconvenção, com [pedidos
     específicos];
  e) a produção das provas indicadas no item IV.

Termos em que,
Pede deferimento.

[Cidade], [data].

_______________________________________
[NOME DA(O) ADVOGADA(O)]
OAB/[UF] nº [...]
```

## Passo 5 — Conferências obrigatórias antes da entrega

1. **Prazo.** 15 dias úteis (art. 335 do CPC + art. 219) — texto literal via MCP. Termo inicial verificado? (Audiência de conciliação? Carta com AR? Citação por hora certa?)
2. **Princípio da eventualidade** (art. 336). Todas as defesas levantadas em conjunto?
3. **Impugnação especificada** (art. 341). Cada fato da inicial classificado? Lacuna = confissão ficta — perigosíssimo.
4. **Pedido contraposto vs. reconvenção.** Se rito é juizado, é pedido contraposto (Lei 9.099) — verificar.
5. **Documentos.** Procuração + comprovantes da versão da(o) ré(u) — listados?
6. **Auditoria de legislação — obrigatória:** para cada dispositivo legal citado na peça, verifique se o bloco `citacao / source_url` está presente. Citação sem esses campos = foi de memória = **inválida**. Remova ou converta em `[CITAÇÃO PENDENTE]`.
7. **Auditoria de jurisprudência — obrigatória:** para cada enunciado jurisprudencial na peça, verifique se há `search_id` e `eficacia` do MCP. Sem esses campos = foi de memória = **inválida**. Substitua por `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]`.
8. **Marcadores remanescentes:** `[VERIFICAR]`, `[CITAÇÃO PENDENTE]`, `[FORA DO CORPUS]`, `[JURISPRUDÊNCIA]`, `[doc. a numerar]` — todos listados no bloco de notas. Itens `[VERIFICAR]` devem aparecer destacados em vermelho no documento final para sinalizar visualmente que a peça está incompleta.

## Formatação padrão do documento

Todo o texto da peça — cabeçalho, qualificações, fatos, preliminares, mérito, pedidos — deve estar em **alinhamento justificado**. Não há exceção para nenhuma seção. A citação de lei segue as regras próprias da seção "Regra absoluta" (recuada, justificada, fonte menor), mas o restante do documento também é justificado — não alinhado à esquerda.

No .docx, isso equivale a `AlignmentType.JUSTIFIED` (docx-js) ou `alignment: justify` em todos os parágrafos.

## Passo 6 — Output

`outputs/contestacao-[slug]-[YYYY-MM-DD].docx` + `outputs/contestacao-[slug]-NOTAS.md` (mesmo formato do bloco da skill `peticao`).

**Marcadores em vermelho — obrigatório.** Após gerar o `.docx`, execute o script `colorir_marcadores.py` (disponível em `scripts/`) para aplicar cor vermelha e negrito a todos os marcadores inline:

```bash
python scripts/colorir_marcadores.py outputs/contestacao-[slug]-[YYYY-MM-DD].docx
```

O script sobrescreve o arquivo no mesmo caminho. Se o script não estiver disponível, aplique manualmente cor `#FF0000` a cada ocorrência de `[VERIFICAR...]`, `[CITAÇÃO PENDENTE]`, `[FORA DO CORPUS...]`, `[JURISPRUDÊNCIA...]` e `[DOC. A NUMERAR]`.

**Aviso obrigatório ao usuário — incluir sempre após entregar a minuta:**

> ⚠️ **ITENS EM VERMELHO — VERIFICAÇÃO NECESSÁRIA ANTES DO PROTOCOLO**
> Os trechos marcados em vermelho no documento indicam pontos que precisam ser resolvidos pelo(a) advogado(a) antes de assinar e protocolar a peça. Revise cada marcador:
> - `[VERIFICAR: ...]` — dado não confirmado, presumido ou ausente
> - `[CITAÇÃO PENDENTE]` — artigo não localizado via MCP; incluir manualmente com fonte verificada
> - `[FORA DO CORPUS]` — norma estadual, municipal ou tabela do tribunal; verificar na fonte local
> - `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]` — espaço reservado para súmula ou julgado a critério do(a) advogado(a)
> - `[DOC. A NUMERAR]` — documento referenciado sem número; numerar ao juntar
>
> Nenhum desses marcadores pode permanecer na peça no momento do protocolo.

## O que esta skill NÃO faz

- **Não protocola.** Ato privativo do(a) advogado(a) habilitado(a).
- **Não calcula o prazo final para você.** Devolve o texto do art. 335 do CPC (via MCP) e os marcos legais. O cálculo no PJe/eSAJ é seu — feriados forenses locais, suspensões, recesso (art. 220 do CPC) variam.
- **Não insere jurisprudência não verificada.** Qualquer enunciado não encontrado via MCP fica como `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]`. Jurisprudência verificada via MCP pode ser inserida — consulte a Fonte 2 acima.
- **Não decide estratégia.** "Confessar este fato para fortalecer a defesa naquele" é decisão profissional — a skill estrutura, você decide.
- **Não substitui o(a) advogado(a).** Produz rascunho — assinatura, responsabilidade e estratégia são da pessoa habilitada na OAB.
