---
name: letra-da-lei:peticao
version: 0.1.0
description: Redige petição inicial brasileira (CPC art. 319) com fundamentação verificada. Use para "redige uma inicial", "vou ajuizar [ação]", "monta a inicial", "preciso entrar com [ação]", ou qualquer peça inaugural cível, trabalhista, do consumidor, juizado, família ou mandado de segurança. Não use para contestação, recurso ou defesa.
argument-hint: "[tipo de ação ou descrição curta — ex.: 'indenizatória por dano moral']"
---

# /peticao

## ⚠️ PASSO ZERO — OBRIGATÓRIO ANTES DE QUALQUER RASCUNHO

**Não escreva uma linha da peça antes de completar o intake abaixo.** Use `AskUserQuestion` para coletar as informações em bloco — máximo 4 perguntas por rodada. Se faltou dado essencial após a primeira rodada, faça uma segunda antes de prosseguir. Peça redigida com dado inventado ou presumido invalida o trabalho.

### Perguntas obrigatórias — use AskUserQuestion

**Rodada 1 — Partes e fatos:**
- Nome completo, CPF/CNPJ, endereço, estado civil e profissão do(a) **autor(a)**.
- Nome completo, CPF/CNPJ e endereço do(a) **réu(é)** (se desconhecidos, declarar).
- Narrativa cronológica dos **fatos** — o que aconteceu, quando, com que provas.
- **Documentos disponíveis** — listar pelo menos os que o usuário já tem em mãos.

**Rodada 2 — Pedido e estratégia:**
- **Pedido principal** — o que se quer, certo e determinado; se pecuniário, o valor exato.
- **Competência e rito** — JEC (Juizado Especial Cível), Vara Cível comum, Trabalhista, Fazenda Pública? Comarca/cidade?
- **Tutela de urgência** — há pedido de liminar? Se sim, qual o perigo de dano e por que é urgente?
- **Danos morais** — são pedidos? Qual valor pretendido (ex.: R$ 10.000, R$ 15.000) ou quer deixar a critério do juízo?
- **Valor da causa** — já calculado? Ou precisa de ajuda para calcular conforme art. 292 do CPC?
- **Gratuidade de justiça** — o(a) autor(a) vai alegar hipossuficiência econômica e requerer os benefícios da justiça gratuita? **Se o(a) autor(a) for pessoa física, esta pergunta é obrigatória — deve ser feita mesmo que o usuário não mencione o tema.** Se a resposta for sim: incluir pedido expresso na inicial (CPC art. 99) e orientar o usuário a assinar declaração de hipossuficiência, que pode ser inserida na própria petição ou em documento apartado. Se for pessoa jurídica, perguntar apenas se houver indício de dificuldade financeira declarado pelo usuário.

> **Regra de ouro:** se o usuário não informou, não invente. Marque `[VERIFICAR]` e liste no bloco de notas final. A única exceção é dado não-essencial (ex.: e-mail da parte quando não exigido pelo juízo).

### Protocolo "Informar manualmente" — obrigatório

Após cada rodada de `AskUserQuestion`, verifique se alguma resposta foi **"Informar manualmente"**. Se sim, **não prossiga para a próxima etapa.** Compile todos os itens marcados dessa forma em uma única mensagem e solicite ao usuário que forneça os dados antes de continuar:

> "Você marcou os seguintes itens para preenchimento manual. Por favor, informe cada um antes de prosseguirmos:
> - [item 1]
> - [item 2]
> - ..."

Só avance para a redação quando **todos** os itens "Informar manualmente" tiverem sido respondidos ou explicitamente descartados pelo usuário (ex.: "não tenho esse dado" → marcar `[VERIFICAR]`).

---

1. Faça a entrevista de intake (Passo 1 abaixo) — partes, fatos, pedido, juízo, rito.
2. **Chame `buscar_artigos` para todo dispositivo legal que entrar na peça.** Sem exceção. Memória do modelo é proibida para citar artigo.
3. Monte a peça na estrutura do CPC art. 319 (Passo 3).
4. Output: rascunho `.docx` em `outputs/peticao-[slug]-[YYYY-MM-DD].docx` + bloco de notas para o(a) advogado(a) revisor(a) com cada marcador `[VERIFICAR]` e `[CITAÇÃO PENDENTE]` que sobrou.

---

# Petição Inicial

## Propósito

A inicial é o documento que abre o processo. Tudo que vier depois — saneamento, instrução, sentença — é moldado pelo que está aqui. Os fatos não narrados não viram causa de pedir; o pedido não formulado não pode ser concedido (CPC art. 141 e 492). Esta skill produz um **rascunho com fundamentação verificada artigo por artigo contra o texto vigente da lei** — e nada mais. Quem assina é a pessoa habilitada na OAB, que revisa, ajusta, e responde profissionalmente.

## Regra absoluta — fontes da peça

### Fonte 1 — Lei federal (MCP)

**Toda e qualquer citação de lei federal nesta peça vem do MCP da Letra da Lei.** Sem exceções. **Carregue a skill `letra-da-lei:pesquisa` e siga-a** para qualquer busca — ela define as ferramentas (`buscar_artigos`, `acervo · consultar`, `acervo · listar`, `reclame_aqui`), os parâmetros (`query`, `norma`), os campos retornados e as verificações de vigência (`situacao`) e de texto integral (`is_truncated` → `consultar`). Memória do modelo é proibida para citar artigo — leis mudam (ex.: Lei 14.905/2024 alterou CC arts. 389 e 406).

Regras desta peça (além da `pesquisa`):
- Citação sem `citacao` + `source_url` da ferramenta → não entra; vira `[CITAÇÃO PENDENTE]`.
- `situacao` ≠ `vigente` → `[VERIFICAR VIGÊNCIA — situação: <X>]`.
- Norma estadual/municipal/infralegal → `[FORA DO CORPUS]`.
- Busca do MCP vazia, contraditória ou irrelevante? Registre a lacuna via `acervo · reclame_aqui` antes de seguir.

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

**A regra vale também para alertas e referências administrativas.** Sempre que um dispositivo legal for mencionado fora de um bloco de citação (ex.: em alerta de prescrição, em nota ao advogado, em texto corrido), a referência deve aparecer como `[citação verificada via MCP — citacao: XXX]` ou a citação literal deve ser inserida com bloco completo. Referência a artigo em texto corrido sem citacao conta como citação não verificada para fins de auditoria.

**Por que a regra é absoluta:** memória de modelo erra número de artigo, parágrafo, inciso, redação vigente (leis são alteradas — ex.: Lei 14.905/2024 mudou CC arts. 389 e 406) e — pior — afirma coisas que a lei não diz. Em peça processual isso é sancionável (CPC art. 80, II; art. 81; e responsabilidade do(a) advogado(a) perante a OAB). O MCP existe exatamente para eliminar essa categoria de erro.

## Passo 1 — Intake

Faça as perguntas abaixo, uma por vez ou em bloco curto, antes de redigir. Não invente nada que o usuário não forneceu.

### 1.1 Partes

- **Autor(a/es):** nome completo, nacionalidade, estado civil, profissão, CPF/CNPJ, endereço, e-mail (CPC art. 319, II).
- **Réu(s)/ré(s):** mesmos dados; se desconhecidos, declarar (art. 319, § 1º) e indicar como serão buscados.
- Há litisconsórcio? Necessário ou facultativo? Ativo ou passivo?

### 1.2 Causa de pedir e fatos

- Narrativa cronológica do que aconteceu (causa de pedir remota e próxima).
- Documentos que comprovam cada fato — peça que o usuário os anexe ou liste, mesmo que digitalize depois.
- Há prova testemunhal? Pericial? Confissão prévia? Documento eletrônico?

### 1.3 Pedido

- Pedido principal (certo e determinado — CPC art. 322 e 324).
- Pedidos sucessivos, subsidiários, alternativos, cumulados?
- Tutela de urgência ou da evidência? (CPC art. 300 e ss.) Em caso positivo: probabilidade do direito + perigo de dano + reversibilidade.
- Pedidos genéricos (art. 324, § 1º) — só nas hipóteses do artigo; justificar.

### 1.4 Juízo competente e rito

- Competência: territorial, em razão da matéria, em razão da pessoa, valor. Buscar no MCP os arts. 42 a 53 do CPC se necessário.
- Rito: procedimento comum, juizado especial cível (Lei 9.099/1995 — buscar via MCP), juizado da Fazenda Pública, procedimento especial (art. 539 e ss.).
- Valor da causa (art. 291 a 293).

### 1.5 Conferência rápida — relação de consumo, trabalhista, família?

Se houver pista de **relação de consumo** (CDC) → chamar `buscar_artigos` com `Lei-8078-1990` para fundamentar. Se **trabalhista** (CLT) → `DL-5452-1943`. Se **família** → Código Civil (`Lei-10406-2002`) + Estatuto do Idoso/ECA/Lei Maria da Penha conforme o caso. Não decidir o regime sem checar a lei.

### 1.6 Dados adicionais obrigatórios por regime (perguntar na Rodada 2)

**Se trabalhista:** perguntar obrigatoriamente:
- **Remuneração mensal bruta** do(a) reclamante — dado essencial para calcular FGTS (8% × remuneração × meses), férias, 13º salário e aviso prévio. Sem esse valor, todos os pedidos pecuniários ficam com `[VERIFICAR: calcular]`, transferindo o cálculo inteiro para o(a) advogado(a). Se o usuário não souber o valor exato, marcar `[VERIFICAR: informar salário mensal — R$ ___]` e listar no bloco de notas.
- **Cabeçalho da peça:** em petição inicial trabalhista, o nº da Vara é desconhecido antes da distribuição. Usar no cabeçalho: `___ª VARA DO TRABALHO DE [COMARCA]`, com o número em branco (`_`), sem marcador `[VERIFICAR]` e sem destacar em vermelho — é lacuna esperada e normal na inicial.

**Se consumidor:** perguntar obrigatoriamente:
- Valor do dano material (se houver), para compor o valor da causa (CPC art. 292, V).

**Se família com menor:** confirmar se há filhos menores — define obrigatoriedade de via judicial e intervenção do MP.

## Passo 2 — Pesquisa legal (MCP)

Para **cada tese jurídica** que vai sustentar o pedido:

1. Identifique a norma matriz (CC, CDC, CLT, CPC, lei especial).
2. Chame `buscar_artigos` com query precisa (palavras do instituto + número se souber) e o parâmetro `norma` (sigla/slug da lei) para restringir a busca.
3. Registre no rascunho o bloco completo no formato padrão de citação:
   ```
       [Texto literal retornado — sem aspas, recuado, justificado, fonte menor]
       Fonte: [citacao] | [source_url] | situação: [situacao] | lei: [lei_slug]

   ```
4. Se a tese depende de norma fora do corpus (estadual, municipal, infralegal, resolução de agência), **flag** `[FORA DO CORPUS LETRA DA LEI — verificar manualmente]` e siga.

**Sem suplementação silenciosa.** Se a busca no MCP devolver pouco ou nada para um instituto que a peça precisa invocar, pare e pergunte ao usuário antes de buscar em outro lugar:

> "O MCP retornou [N] resultados para [tema]. Cobertura parece fina. Quer: (a) refinar a query; (b) tentar outra `norma`; (c) buscar na web — resultados ficarão marcados `[busca web — verificar fonte primária]` e devem ser conferidos antes do protocolo; (d) deixar `[CITAÇÃO PENDENTE]` e seguir?"

A decisão é do(a) advogado(a), não da skill.

## Passo 2.1 — Mapeamento de precedentes vinculantes (Repercussão Geral STF e Repetitivos STJ)

**Execute este passo após o Passo 2, antes de redigir qualquer linha da peça.**

Para cada tese central da petição, verifique se existe precedente vinculante (art. 927 CPC) que possa afetar diretamente o caso: um tema pendente pode suspender o processo; um tema decidido pode determinar o desfecho. Use o MCP como primeira fonte.

### Como buscar

Para cada tese central (ex.: "reconhecimento de vínculo empregatício em pejotização", "responsabilidade do fornecedor por fraude bancária"):

1. **`jurisprudencia-federal · buscar_vinculantes`** com query em linguagem natural descrevendo a tese. Filtre por `autoridade: "STF"` para repercussão geral ou `autoridade: "STJ"` para repetitivos.
2. Se a busca retornar resultado pertinente, note o `search_id`, `tipo` (tema_repercussao_geral / tema_repetitivo), `situacao` e o enunciado.
3. Para IRDRs estaduais relevantes: `jurisprudencia-estadual · buscar_vinculantes` com `localidade` = UF do juízo.

### Como inserir na peça

**Precedentes vinculantes pertinentes** encontrados via MCP: inserir na seção "Do Direito" correspondente usando o formato padrão de citação de jurisprudência (Fonte 2 acima). Campo `eficacia: vinculante` dispensa marcador adicional.

**Temas pendentes:** acrescentar ao lado do enunciado:

```
[ATENÇÃO — TEMA PENDENTE: processos sobre esta matéria podem estar
 suspensos ou sujeitos à modulação. Verificar impacto antes de ajuizar.]
```

**Se o MCP não retornar resultado pertinente:**

```
[JURISPRUDÊNCIA — busca de precedentes vinculantes realizada via MCP
 sem resultado direto para esta tese. Verificar manualmente se necessário.]
```

**Não omitir silenciosamente.** O(a) advogado(a) precisa saber que a busca foi feita.

### Limitações desta etapa

- O MCP cobre STF, STJ, TST, CARF (federal) e IRDRs dos TJs (estadual). Precedentes de TRTs e outros tribunais especializados devem ser verificados manualmente — marcar `[FORA DO CORPUS — verificar precedentes do tribunal local manualmente]` se relevante.
- A skill **não analisa** se o tema é favorável ou desfavorável ao cliente. Essa avaliação é do(a) advogado(a).

## Passo 3 — Estrutura da peça (CPC art. 319)

```
EXCELENTÍSSIMO(A) SENHOR(A) DOUTOR(A) JUIZ(A) DE DIREITO DA [...] VARA [CÍVEL / DA
FAMÍLIA / DO JUIZADO ESPECIAL CÍVEL / DA FAZENDA PÚBLICA / DO TRABALHO] DA COMARCA
DE [...]

                                                          [Distribuição por dependência? Sim/Não]
                                                          [Valor da causa: R$ ...]

[NOME DO AUTOR], [qualificação completa — art. 319, II], por seu(sua) advogado(a)
infra-assinado(a) (procuração anexa — doc. 01), vem, respeitosamente, à presença
de Vossa Excelência propor a presente

                AÇÃO [denominação — ex.: DE INDENIZAÇÃO POR DANOS MORAIS]

em face de [NOME DO RÉU], [qualificação completa], pelos fatos e fundamentos a
seguir expostos.

I — DOS FATOS

[Narrativa cronológica, factual, sem argumentação jurídica aqui. Cada fato com
referência ao doc. que o comprova: "(doc. nº)" — não inventar números de doc se
o usuário não forneceu; marcar `[DOC. A NUMERAR]`.]

II — DO DIREITO

[Aqui entram os fundamentos jurídicos do pedido — art. 319, III. CADA dispositivo
citado abaixo deve ter sido retornado por `buscar_artigos`. Estrutura
sugerida:]

II.1 — [Instituto / tese 1 — ex.: Da responsabilidade civil do fornecedor]

Dispõe o art. 14 do Código de Defesa do Consumidor (Lei nº 8.078/1990):

    [texto literal retornado pelo MCP — sem aspas, recuado, justificado, fonte 1pt menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-8078-1990

[Aplicação ao caso concreto — subsunção. 2-4 parágrafos. Formatação normal.]

II.2 — [tese 2] — mesma estrutura

[...]

III — DA TUTELA DE URGÊNCIA  (se aplicável)

[Texto introdutório da tutela de urgência.]

    [Texto literal do art. 300 via MCP — sem aspas, recuado, justificado, fonte menor]
    Fonte: [citacao] | [source_url] | situação: [situacao] | lei: Lei-13105-2015

[Demonstrar probabilidade do direito + perigo de dano + reversibilidade — formatação normal.]

IV — DOS PEDIDOS

Diante do exposto, requer:

  a) [pedido principal — certo e determinado, art. 322 do CPC];
  b) a citação do(s/a/as) réu(s/ré/és) para, querendo, oferecer contestação no
     prazo legal, sob pena de revelia;
  c) a produção de todas as provas em direito admitidas, especialmente
     [documental / testemunhal / pericial / depoimento pessoal] (art. 319, VI);
  d) [pedidos acessórios — honorários (art. 85), custas, juros, correção];
  e) [tutela / liminar, se houver — repetir o pedido específico].

V — DO VALOR DA CAUSA

Atribui-se à causa o valor de R$ [...] (art. 291 do CPC), [explicação do critério —
ex.: "correspondente ao pedido econômico nos termos do art. 292, V"].

V — DA OPÇÃO PELA AUDIÊNCIA DE CONCILIAÇÃO  (art. 319, VII)

[X] Tem interesse na realização de audiência de conciliação/mediação.
[ ] Não tem interesse.

Termos em que,
Pede deferimento.

[Cidade], [data].

_______________________________________
[NOME DA(O) ADVOGADA(O)]
OAB/[UF] nº [...]
```

## Passo 4 — Conferências obrigatórias antes da entrega

Antes de salvar o `.docx`, rode mentalmente esta checklist e reporte cada item:

1. **CPC art. 319 — requisitos.** Todos os 7 incisos atendidos? Para cada um, sim/não/N/A.
2. **Pedido certo e determinado** (art. 322 e 324). Se genérico, justificou nos termos do art. 324, § 1º?
3. **Causa de pedir cobre o pedido?** O fato narrado sustenta cada pedido formulado? (Princípio da congruência — art. 141 e 492.)
4. **Valor da causa.** Calculado conforme art. 291 a 293? Tem critério?
5. **Documentos essenciais** (art. 320). Procuração, comprovantes de fato constitutivo, prova do título se executiva — listados?
6. **Competência** verificada via MCP, não de memória?
7. **Tutela de urgência** (se houver): probabilidade + perigo + reversibilidade declinados?
8. **Pedido de citação** consta? (Erro frequente.)
9. **Gratuidade de justiça** — se o(a) autor(a) é pessoa física, o pedido foi feito ou a ausência foi registrada como `[VERIFICAR]` e anotada no bloco de notas?
10. **Auditoria de legislação — obrigatória:** para cada dispositivo legal citado na peça (incluindo alertas e notas), verifique se o bloco `citacao / source_url` está presente. Citação sem esses campos = foi de memória = **inválida**. Remova ou converta em `[CITAÇÃO PENDENTE]`.
11. **Auditoria de jurisprudência — obrigatória:** para cada enunciado jurisprudencial na peça, verifique se há `search_id` e `eficacia` do MCP. Sem esses campos = foi de memória = **inválida**. Substitua por `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]`.
12. **Prescrição — verificação obrigatória em ações trabalhistas:** se o regime for CLT, calcular o prazo prescricional antes de entregar a peça. Regra (CLT, art. 11 — buscar via MCP, norma `DL-5452-1943`): 5 anos durante a vigência do contrato, **limite de 2 anos após a extinção**. Comparar a data de término do contrato com a data atual. Se o prazo de 2 anos já expirou ou está próximo de expirar (menos de 30 dias), inserir alerta em vermelho no início da peça e no bloco de notas, com instrução expressa de não protocolar sem análise prévia. Exceção: pedido de anotação na CTPS para fins previdenciários não está sujeito a prazo prescricional (CLT, art. 11, § 1º).
13. **Marcadores remanescentes:** `[VERIFICAR]`, `[CITAÇÃO PENDENTE]`, `[DOC. A NUMERAR]`, `[FORA DO CORPUS]`, `[JURISPRUDÊNCIA]` — todos listados no bloco de notas?

## Formatação padrão do documento

Todo o texto da peça — cabeçalho, qualificações, fatos, fundamentos, pedidos, valor da causa — deve estar em **alinhamento justificado**. Não há exceção para nenhuma seção. A citação de lei segue as regras próprias da seção "Regra absoluta" (recuada, justificada, fonte menor), mas o restante do documento também é justificado — não alinhado à esquerda.

No .docx, isso equivale a `AlignmentType.JUSTIFIED` (docx-js) ou `alignment: justify` (pandoc/CSS) em todos os parágrafos.

## Passo 5 — Output

Salve **dois arquivos**:

- `outputs/peticao-[slug]-[YYYY-MM-DD].docx` — a peça em si, formatada.
- `outputs/peticao-[slug]-NOTAS.md` — bloco de notas para revisão.

**Marcadores em vermelho — obrigatório.** Após gerar o `.docx`, execute o script `colorir_marcadores.py` (disponível em `scripts/`) para aplicar cor vermelha e negrito a todos os marcadores inline. O(a) advogado(a) revisor(a) deve conseguir identificar visualmente todos os pontos pendentes sem fazer busca manual.

```bash
python scripts/colorir_marcadores.py outputs/peticao-[slug]-[YYYY-MM-DD].docx
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

```
## Notas de revisão — Petição Inicial — [data]

**Skill:** peticao (Letra da Lei)
**Fonte da legislação:** MCP Letra da Lei (texto verbatim do Planalto)

### Marcadores inline a resolver
- `[VERIFICAR: ...]` — N ocorrências
- `[CITAÇÃO PENDENTE]` — N
- `[FORA DO CORPUS]` — N
- `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]` — N

### Dispositivos citados (todos verificados via MCP)
- [lei_slug]-[Art-N] — [source_url]
- ...

### Pontos abertos para a(o) advogada(o)
- [premissas que precisam ser confirmadas]
- [estratégia processual que foi assumida e merece discussão]
- [pedidos formulados que comportam variação tática]

### O que esta skill NÃO fez
- Jurisprudência não encontrada via MCP está marcada `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]` — preencher manualmente se relevante.
- Não calculou prazos para a outra parte responder — é tarefa do(a) advogado(a).
- Não conferiu documentos do usuário (eles foram apenas listados).
- Não verificou conflito de interesses — premissa da(o) advogada(o).
- Não protocolou nada. Não pode protocolar. Você protocola.
```

## O que esta skill NÃO faz

- **Não protocola.** Nunca. Protocolar é ato privativo de advogado(a) habilitado(a) (Estatuto da OAB — Lei 8.906/1994) e exige assinatura digital pessoal no PJe/eSAJ/Projudi/etc.
- **Não insere jurisprudência não verificada.** Qualquer enunciado não encontrado via MCP fica como `[JURISPRUDÊNCIA — a ser inserida pelo(a) advogado(a)]`. Jurisprudência verificada via MCP pode ser inserida — consulte a Fonte 2 acima.
- **Não substitui o(a) advogado(a).** Produz rascunho com fundamentação verificada — quem analisa estratégia processual, decide pedidos, ajusta tom, e assina é a pessoa habilitada.
- **Não pesquisa norma estadual, municipal, ou infralegal** (decretos, portarias, resoluções de agência). Marca `[FORA DO CORPUS]` e segue.
- **Não inventa fatos.** Só usa o que o usuário forneceu no intake. Lacuna fica como `[VERIFICAR]`.
