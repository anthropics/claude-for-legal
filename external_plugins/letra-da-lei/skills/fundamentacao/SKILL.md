---
name: letra-da-lei:fundamentacao
version: 0.1.0
description: Estrutura a fundamentação de sentença, decisão interlocutória ou despacho conforme o art. 489 do CPC (esp. § 1º), com dispositivos verificados. Use para "monta a fundamentação", "fundamentar a sentença", "estrutura a decisão sobre [tese]". Não use para peças de parte ou parecer ministerial.
argument-hint: "[tipo de decisão — ex.: 'sentença em ação de cobrança' ou 'decisão sobre tutela de urgência']"
---

# /fundamentacao

## ⚠️ PASSO ZERO — OBRIGATÓRIO ANTES DE QUALQUER RASCUNHO

**Não escreva uma linha da minuta antes de completar o intake abaixo.** Use `AskUserQuestion` para coletar as informações em bloco — máximo 4 perguntas por rodada. Fundamentação redigida sem os autos é genérica, viola o art. 489, § 1º, III do CPC, e é candidata a embargo declaratório ou cassação em grau recursal.

### Perguntas obrigatórias — use AskUserQuestion

**Rodada 1 — Autos e tipo de pronunciamento:**
- **Tipo de pronunciamento** — sentença (art. 203, § 1º), decisão interlocutória (§ 2º) ou despacho fundamentado?
- **Os autos estão disponíveis?** Peça o arquivo da inicial e da contestação (PDF/DOCX ou texto colado). Se não houver contestação, confirmar se o réu é revel.
- **Número do processo**, vara, comarca e nome das partes.
- **Há tutela de urgência já concedida** (liminar/antecipação de tutela) que precisa ser mantida, revogada ou ratificada na sentença?

**Rodada 2 — Pedidos, teses e provas:**
- **Pedidos da inicial** — listar por letra/número com valor de cada um.
- **Teses da defesa** — principais argumentos do(a) réu(é) na contestação (preliminares + mérito).
- **Provas produzidas** — quais documentos foram juntados? Houve perícia? Depoimentos? Síntese das conclusões.
- **Há reconvenção ou pedido contraposto** formulado pelo(a) réu(é)?
- **Qual a orientação do(a) magistrado(a)** — procedência total, parcial ou improcedência? (Isso define o roteiro da fundamentação; marcar como `[CONVICÇÃO JUDICIAL — confirmar ou substituir]` no rascunho.)

> **Regra de ouro:** toda tese das partes capaz de infirmar a conclusão **precisa ser enfrentada** (art. 489, § 1º, IV do CPC). Se o usuário não informar uma tese, marque `[VERIFICAR — tese pode ter sido omitida]` no rascunho. Jamais suprima silenciosamente argumento que o usuário não listou.

### Protocolo "Informar manualmente" — obrigatório

Após cada rodada de `AskUserQuestion`, verifique se alguma resposta foi **"Informar manualmente"**. Se sim, **não prossiga para a próxima etapa.** Compile todos os itens marcados dessa forma em uma única mensagem e solicite ao usuário que forneça os dados antes de continuar:

> "Você marcou os seguintes itens para preenchimento manual. Por favor, informe cada um antes de prosseguirmos:
> - [item 1]
> - [item 2]
> - ..."

Só avance para a redação quando **todos** os itens "Informar manualmente" tiverem sido respondidos ou explicitamente descartados pelo usuário (ex.: "não tenho esse dado" → marcar `[VERIFICAR]`).

---

1. **Leia os autos** — pelo menos a inicial, a contestação e as provas relevantes. Sem isso, fundamentação é genérica e cai no inciso III do § 1º do art. 489.
2. Defina o tipo de pronunciamento (sentença, decisão interlocutória, despacho fundamentado).
3. Identifique cada tese das partes que precisa ser enfrentada (gatilho do art. 489, § 1º, IV).
4. **Para cada dispositivo legal aplicado, chame `buscar_artigos`.** Citação de memória é proibida.
5. Estruture relatório + fundamentação + dispositivo. Em cada item, checagem contra o § 1º (Passo 5).
6. Output: rascunho `.docx` + bloco de notas com cada `[A REVISAR]` e `[DECISÃO PESSOAL]` listado.

---

# Fundamentação Judicial

## Propósito e limite

Esta skill **estrutura** a fundamentação e **fornece a base legal verificada** — nunca decide. A convicção do(a) juiz(a) é insubstituível. O texto produzido é um andaime: a magistrada(o) preenche, ajusta, contraria, e firma.

O que esta skill resolve bem:

- **Risco de anulação por falta de fundamentação** (CPC art. 489, § 1º) — checa cada um dos seis incisos.
- **Erro de citação legal** — toda lei federal vem do MCP, texto literal do Planalto.
- **Esquecimento de argumento** (art. 489, § 1º, IV) — força mapeamento explícito das teses.

O que **não** resolve:

- Convicção judicial. A skill propõe; o(a) juiz(a) decide. O cabeçalho de cada bloco gerado leva `[CONVICÇÃO JUDICIAL — confirmar ou substituir]`.
- Jurisprudência não encontrada no MCP. O MCP cobre legislação federal e jurisprudência federal (STF/STJ/TST/CARF) + IRDRs estaduais. O que não for encontrado via MCP fica `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — conferir manualmente no STJ/STF/tribunal]`.
- Política de uso de IA no Judiciário. Resoluções do CNJ e atos normativos do tribunal local estão **fora do corpus** desta skill. Verifique a Resolução CNJ aplicável e o ato normativo do seu tribunal antes de usar IA na atividade-fim.

## Regra absoluta — fontes da decisão

### Fonte 1 — Lei federal (MCP)

Toda lei federal citada na fundamentação vem do MCP da Letra da Lei. Sem exceção. **Carregue a skill `letra-da-lei:pesquisa` e siga-a** para qualquer busca — ela define as ferramentas (`buscar_artigos`, `acervo · consultar`, `acervo · listar`, `reclame_aqui`), os parâmetros (`query`, `norma`), os campos retornados e as verificações de vigência (`situacao`) e de texto integral (`is_truncated` → `consultar`).

Regras desta decisão (além da `pesquisa`):
- `situacao` ≠ `vigente` → `[VERIFICAR VIGÊNCIA — situação: <X>]`; sem memória do modelo para número ou redação de artigo.
- Norma estadual, regimento interno, resolução de CNJ/CNMP → `[FORA DO CORPUS]`.
- Busca do MCP vazia, contraditória ou irrelevante? Registre a lacuna via `acervo · reclame_aqui` antes de seguir.

Por quê: decisão judicial que cita artigo errado ou parágrafo inexistente é embargo declaratório certo, e em casos sérios é cassação no tribunal. O custo individual (retrabalho), institucional (autoridade do gabinete) e sistêmico (confiança no Judiciário) é alto demais para depender de memória de modelo.

### Fonte 2 — Jurisprudência (MCP)

Súmulas, temas de repercussão geral e repetitivos verificados via MCP da Letra da Lei são fontes válidas para a fundamentação. Use as ferramentas conforme o escopo:

- **Federal (STF/STJ/TST/CARF):** `jurisprudencia-federal · buscar_precedentes` (busca ampla) ou `jurisprudencia-federal · buscar_vinculantes` (restringe a vinculantes do art. 927 CPC). Filtre por `autoridade` (`STF`, `STJ`, `TST`, `CARF`).
- **Estadual — IRDRs (TJs):** `jurisprudencia-estadual · buscar_vinculantes` (ferramenta distinta) com o parâmetro **obrigatório** `localidade` (sigla da UF, ou `"BR"` para busca nacional).
- **Texto truncado (`is_truncated: true`):** chame `acervo · consultar` (`dominio: "jurisprudencia"`, `esfera: "federal"`/`"estadual"`) antes de citar.

**Força do precedente — campo `eficacia` retornado pelo MCP:**
- `vinculante` = observância obrigatória (art. 927 CPC) — citar com texto literal e identificar os fundamentos determinantes (exigência do art. 489, § 1º, V do CPC).
- `obrigatoria` = forte deferência — citar com enunciado literal e demonstração de adequação ao caso.
- `persuasiva` = subsídio — citar com marcador `[JURISPRUDÊNCIA PERSUASIVA — revisar pertinência ao caso]`.

**Formato de citação de jurisprudência:**

```
    [Enunciado literal retornado pelo MCP — sem aspas, recuado à esquerda,
     alinhamento justificado, fonte 1pt menor que o corpo do texto]
    Fonte: [autoridade] | [tipo] | search_id: [search_id] | eficacia: [eficacia]

```

**Precedente invocado pela parte mas não encontrado via MCP:** marca `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP — confirmar manualmente no STJ/STF/tribunal antes de publicar]`.

**Precedente NÃO invocado pela parte e não encontrado via MCP:** não inserir; deixar o argumento fundado exclusivamente na lei.

## Passo 1 — Ler os autos

**Pré-requisito não-negociável.** Peça ao usuário:

> "Para fundamentar com qualidade preciso, no mínimo, da petição inicial, da contestação, e — se houver — das principais provas (depoimento, perícia, documentos chave). Quanto mais completos os autos, menor o risco do art. 489, § 1º, IV (deixar de enfrentar argumento capaz de infirmar a conclusão). Pode anexar PDF/DOCX ou colar os trechos relevantes."

Extraia e devolva ao usuário para confirmação:

- **Partes** e qualificação resumida.
- **Pedidos** da inicial — letra por letra.
- **Causa de pedir** — fatos + fundamentos.
- **Preliminares** levantadas na contestação (art. 337) — uma a uma.
- **Defesa de mérito** — teses do(a) ré(u).
- **Reconvenção / pedido contraposto** — se houver.
- **Provas produzidas** — documental, testemunhal (síntese dos depoimentos), pericial (conclusão do laudo).
- **Pareceres, manifestações de terceiros** (MP, amicus curiae, etc.).

**Mapeamento de teses.** Antes de redigir, liste explicitamente:

```
Teses do(a) autor(a) a enfrentar:
  T1: [...]
  T2: [...]
  ...

Teses da(o) ré(u) a enfrentar:
  D1: [...]
  D2: [...]
  ...

Questões processuais pendentes (preliminares):
  P1: [...]
  ...
```

**Esse mapa é a vacina contra o art. 489, § 1º, IV.** Toda tese listada precisa ser enfrentada na fundamentação — ou expressamente declarada prejudicada (e por quê).

## Passo 2 — Tipo de pronunciamento

| Tipo | Quando | Estrutura mínima |
|---|---|---|
| Sentença (art. 203, § 1º, do CPC) | Põe fim à fase cognitiva em 1º grau, com ou sem mérito | Relatório + fundamentação + dispositivo |
| Decisão interlocutória (art. 203, § 2º) | Resolve questão incidente | Fundamentação + dispositivo (relatório dispensado) |
| Despacho fundamentado | Apenas impulso, mas a lei exige motivação | Síntese + fundamento |

Busque art. 203 do CPC via MCP e cole o texto na sua nota interna — não na decisão.

## Passo 3 — Pesquisa legal (MCP)

Para **cada norma** que vai aparecer na fundamentação:

1. Identifique o instituto (e.g., "responsabilidade civil objetiva do fornecedor", "ônus da prova", "boa-fé objetiva").
2. `buscar_artigos` com query precisa + o parâmetro `norma` (sigla/slug, e.g., `CDC` ou `Lei-8078-1990`; `CC` ou `Lei-10406-2002`).
3. Cole o texto literal — entre aspas — na fundamentação, com `source_url` em nota de rodapé ou ao final.
4. Norma fora do corpus: `[FORA DO CORPUS — verificar manualmente]`.

**Sem suplementação silenciosa.** Cobertura fina no MCP → pergunte ao usuário antes de buscar fora.

## Passo 4 — Estrutura da decisão

```
SENTENÇA

Processo nº [...]
Autor: [...]
Réu(s/é(s)): [...]

I — RELATÓRIO

[Síntese cronológica do processo. Não confundir relatório com fundamentação — aqui
descreve-se o que ocorreu nos autos, sem juízo de valor.]

  [Pedidos da inicial — citar inicial fls. [...]]
  [Defesa apresentada — citar contestação fls. [...]]
  [Réplica, se houver]
  [Saneamento — fls. [...]]
  [Instrução — provas produzidas]
  [Memoriais / alegações finais]
  [É o relatório.]

II — FUNDAMENTAÇÃO

  [Sequência sugerida:
   1. Questões processuais pendentes (preliminares da contestação, questões
      conhecíveis de ofício).
   2. Mérito — por tese, na ordem lógica (prejudiciais primeiro).
   3. Pedidos cumulados / sucessivos / acessórios.]

II.1 — DAS PRELIMINARES

II.1.1 — [Preliminar P1 — ex.: Da alegada incompetência relativa]

A(O) Ré(u) sustentou, com fundamento no art. 337, II, do CPC, a incompetência
relativa deste juízo, ao argumento de que [...].

Dispõe o art. 337, II, do CPC:

  "[texto literal via MCP]"

[Análise concreta dos elementos do caso. Por que a regra do art. 63 do CPC se
aplica ou não. Cita arts. 63 e 64 via MCP. Conclusão: acolhe-se / rejeita-se a
preliminar.]

II.2 — DO MÉRITO

II.2.1 — Da [tese de fundo principal — ex.: existência da relação de consumo]

[Identifica a controvérsia. Cita art. 2º e 3º do CDC via MCP. Enquadra os fatos.
Conclui.]

II.2.2 — Do [próximo ponto controvertido — ex.: defeito do serviço]

  Tese da parte autora (T1): [...]
  Tese da defesa (D1): [...]

Dispõe o art. 14 do CDC:

  "[texto literal via MCP]"

[Análise concreta. Subsunção. Em decisão monocrática, este é o item central — não
economize. Enfrente cada elemento normativo aplicado ao fato. Se a prova
documental ou pericial conduz a determinada conclusão, descreva o caminho.]

II.2.3 — Da [tese D2 — defesa que precisa ser enfrentada mesmo se já há
            convicção formada — art. 489, § 1º, IV]

[Enfrentamento explícito, com fundamento. Não é necessário concordar — é
necessário responder.]

II.2.4 — Do dano moral (e/ou material)

[Cita arts. 186 e 927 do CC via MCP, ou os do CDC conforme caso. Análise do dano,
nexo, prova. Quantum: critério (capacidade econômica do ofensor, gravidade,
caráter pedagógico) — cita arts. via MCP se houver tabelamento ou parâmetro
legal.]

II.2.5 — Dos juros e correção monetária

[Cita art. 405 do CC (juros legais) ou súmulas aplicáveis — flag estas como
`[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP]` para o(a) juiz(a) conferir.]

II.2.6 — Da sucumbência

Cita art. 85 e parágrafos do CPC via MCP. Critério de fixação.

III — DISPOSITIVO

Ante o exposto, JULGO [PROCEDENTE / PARCIALMENTE PROCEDENTE / IMPROCEDENTE] o(s)
pedido(s) formulado(s) na inicial, extinguindo o processo COM RESOLUÇÃO DE MÉRITO,
nos termos do art. 487, I, do CPC, para:

  a) [...]
  b) [...]

CONDENO a(o) [parte] ao pagamento das custas processuais e dos honorários
advocatícios, que fixo em [...]% sobre [base], com fundamento no art. 85, §§ 2º
e 3º, do CPC.

[Se aplicável] CONCEDO a gratuidade de justiça nos termos do art. 98 do CPC,
restando suspensa a exigibilidade na forma do § 3º.

P.R.I.

[Cidade], [data].

_______________________________________
[JUIZ(A) DE DIREITO]
```

## Passo 5 — Checagem obrigatória contra o art. 489, § 1º, do CPC

**Sem isto, a fundamentação é não-fundamentação.** Antes de devolver o `.docx`, rode esta checagem item por item. Para cada inciso, reporte explicitamente:

> Busque o texto do art. 489, § 1º, do CPC via MCP e mantenha-o aberto durante a checagem.

**Inciso I** — não se considera fundamentada a decisão que se limita à indicação, à reprodução ou à paráfrase de ato normativo, sem explicar sua relação com a causa.
- [ ] Cada dispositivo citado tem aplicação concreta explicada (1+ parágrafo de subsunção)?

**Inciso II** — empregar conceitos jurídicos indeterminados sem explicar o motivo concreto.
- [ ] "Boa-fé", "função social", "manifesta improcedência", "interesse público" — vieram acompanhadas de razão concreta no caso?

**Inciso III** — invocar motivos que se prestariam a justificar qualquer outra decisão.
- [ ] Trocando "Procedente" por "Improcedente", a fundamentação ainda fecharia? Se sim, ela é vazia.

**Inciso IV** — deixar de enfrentar todos os argumentos deduzidos no processo capazes de infirmar a conclusão.
- [ ] **Para cada T_n e D_n do mapa do Passo 1, há item correspondente na fundamentação?** Se uma tese ficou de fora, ou (a) foi enfrentada (mesmo sumariamente) ou (b) foi declarada prejudicada com motivo. Lacuna silenciosa = anulação.

**Inciso V** — limitar-se a invocar precedente ou enunciado de súmula sem identificar seus fundamentos determinantes e demonstrar adequação ao caso.
- [ ] Cada súmula/precedente citado tem (a) fundamentos determinantes resumidos + (b) demonstração de que o caso se enquadra?

**Inciso VI** — deixar de seguir enunciado de súmula, jurisprudência ou precedente invocado pela parte sem demonstrar distinguishing ou superação.
- [ ] Súmula/precedente invocado pela parte e afastado tem justificativa explícita?

A checagem é parte da entrega — vai listada no bloco de notas, com cada item resolvido ou explicitamente sinalizado.

## Passo 6 — Output

Salve:

- `outputs/fundamentacao-[tipo]-[slug]-[YYYY-MM-DD].docx` — a minuta da decisão.
- `outputs/fundamentacao-[tipo]-[slug]-NOTAS.md`.

**Marcadores em vermelho — obrigatório.** Após gerar o `.docx`, execute o script `colorir_marcadores.py` para aplicar cor vermelha e negrito a todos os marcadores inline:

```bash
python scripts/colorir_marcadores.py outputs/fundamentacao-[tipo]-[slug]-[YYYY-MM-DD].docx
```

O script sobrescreve o arquivo no mesmo caminho. Se o script não estiver disponível, aplique manualmente cor `#FF0000` a cada ocorrência de `[VERIFICAR...]`, `[CONVICÇÃO JUDICIAL...]`, `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP]`, `[FORA DO CORPUS]` e `[A REVISAR]`.

**Aviso obrigatório ao usuário — incluir sempre após entregar a minuta:**

> ⚠️ **ITENS EM VERMELHO — VERIFICAÇÃO NECESSÁRIA ANTES DA PUBLICAÇÃO**
> Os trechos marcados em vermelho na minuta indicam pontos que exigem decisão ou conferência do(a) magistrado(a) antes de publicar. Revise cada marcador:
> - `[CONVICÇÃO JUDICIAL — confirmar ou substituir]` — bloco de mérito que exige convicção pessoal do(a) juiz(a); substituir pelo texto definitivo
> - `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP]` — súmula ou precedente a confirmar manualmente no STJ/STF/tribunal
> - `[FORA DO CORPUS]` — norma estadual, regimental ou resolução do CNJ; verificar na fonte local
> - `[A REVISAR]` — ponto sinalizado durante a redação que precisa de atenção
>
> Nenhum desses marcadores pode permanecer na decisão no momento da publicação.

```
## Notas de revisão — Fundamentação Judicial — [data]

**Skill:** fundamentacao (Letra da Lei)
**Fonte da legislação:** MCP Letra da Lei (texto verbatim do Planalto)

### Mapa de teses (do Passo 1) e onde foram enfrentadas
- T1: [...] — enfrentada em II.2.[N]
- T2: [...] — enfrentada em II.2.[N]
- D1: [...] — enfrentada em II.2.[N]
- D2: [...] — declarada prejudicada em II.2.[N] (motivo: [...])
- ...

### Checagem do art. 489, § 1º (status item por item)
- I: OK / Pendente em [...]
- II: OK
- III: OK
- IV: OK
- V: N/A (sem precedente invocado nesta minuta)
- VI: OK

### Dispositivos citados (todos verificados via MCP)
- [lei_slug]-[Art-N] — [source_url]
- ...

### Marcadores que exigem decisão judicial
- `[CONVICÇÃO JUDICIAL — confirmar ou substituir]` — N ocorrências
- `[JURISPRUDÊNCIA NÃO VERIFICADA VIA MCP]` — N (precedentes/súmulas a conferir no STJ/STF/tribunal)
- `[FORA DO CORPUS]` — N (norma estadual/regimental/CNJ a checar manualmente)
- `[A REVISAR]` — N

### O que esta skill NÃO fez
- Não decidiu. Sugestões de provimento são placeholders — `[PROCEDENTE / IMPROCEDENTE — convicção judicial]`.
- Não pesquisou jurisprudência.
- Não conferiu resoluções do CNJ / atos normativos do tribunal sobre uso de IA — verificar.
- Não conferiu prevenção, conflito de competência, ou impedimentos/suspeição.
- Não calculou quantum indenizatório — propôs critérios; cabe ao(à) juiz(a) fixar.
```

## O que esta skill NÃO faz

- **Não decide.** A convicção é do(a) juiz(a). Cada bloco de mérito leva `[CONVICÇÃO JUDICIAL — confirmar ou substituir]`.
- **Não pesquisa jurisprudência.** MCP cobre só legislação federal. Súmulas, REsps, RREspGs ficam marcados para conferência manual.
- **Não dispensa leitura dos autos pelo(a) magistrado(a).** A leitura é o ato indelegável. A skill apenas estrutura o que o(a) juiz(a) já compreendeu.
- **Não substitui ato decisório.** Produz minuta. A decisão é proferida quando o(a) juiz(a) assina, não quando a skill gera.
- **Não decide sobre uso permitido de IA no gabinete.** Resoluções do CNJ e atos do tribunal local sobre uso de IA em atividade-fim devem ser consultados pelo(a) magistrado(a) antes de adotar a minuta. A skill é ferramenta — não cobre a política institucional.
