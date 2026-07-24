---
name: letra-da-lei:pesquisa
version: 0.1.0
description: Pesquisa e cita legislação e jurisprudência brasileiras, com verificação de vigência e fontes verificáveis. Skill-base carregada pelas peças para qualquer busca jurídica.
allowed-tools:
  - mcp
---

# Pesquisa Jurídica — Letra da Lei (MCP)

Esta é a skill-base de toda consulta à lei e à jurisprudência brasileiras. Outras skills da Letra da Lei (petição inicial, contestação, fundamentação, análise processual) **carregam esta** para buscar e citar. Aqui ficam as ferramentas, os parâmetros, os campos retornados e as verificações obrigatórias antes de citar.

## Pré-requisito

O servidor MCP **`letra-da-lei`** deve estar conectado (`https://mcp.letradalei.com/mcp`). Verifique antes de começar. Se não estiver, avise o usuário e pare — não responda de memória.

## Quando usar

- O usuário pergunta o que a lei brasileira diz sobre um tema.
- É preciso localizar um artigo, código ou estatuto específico.
- A pergunta envolve direitos, obrigações, prazos ou penalidades sob a lei federal.
- É preciso jurisprudência federal (STF/STJ/TST/CARF) ou IRDRs estaduais (TJs).
- Uma peça precisa de fundamentação verificada (esta skill é carregada por elas).

## Quando não usar

- **Aconselhamento jurídico ou prognóstico** — esta skill recupera e cita fontes; quem aplica aos fatos é o(a) advogado(a) habilitado(a).
- **Legislação estadual/municipal ou infralegal** (decretos, portarias, resoluções) — fora do acervo; sinalize a lacuna.

## Regra absoluta

**Pesquise primeiro, responda depois.** Nunca cite artigo ou precedente de memória — leis mudam (ex.: Lei 14.905/2024 alterou CC arts. 389 e 406) e a redação do modelo pode estar desatualizada ou simplesmente errada. Comece pelas ferramentas e fundamente a resposta no texto recuperado.

## Ferramentas (grupo · operação)

| Operação | Ferramenta | Para quê |
|---|---|---|
| Descobrir cobertura / a sigla (`norma`) de uma lei | `acervo · listar` (`dominio: "legislacao"`) | sem `area` → índice de áreas; com `area` (slug, ou `"all"`) → leis daquela área |
| Descobrir cobertura de jurisprudência | `acervo · listar` (`dominio: "jurisprudencia"` + `esfera`) | tribunais, tipos, eficácia, vocabulário de `area` |
| Buscar artigo por tema | `legislacao-federal · buscar_artigos` | busca semântica de dispositivos |
| Navegar a lei / relações de um artigo | `legislacao-federal · explorar_contexto` | sumário (um nível por vez) e `cita`/`citado_por`/`altera` |
| Texto **integral** (não truncado) | `acervo · consultar` | confirmar verbatim antes de citar |
| Jurisprudência federal — busca ampla | `jurisprudencia-federal · buscar_precedentes` | súmulas, temas, OJs, acórdãos, informativos |
| Jurisprudência federal — só vinculantes | `jurisprudencia-federal · buscar_vinculantes` | SV, repercussão geral, repetitivos (art. 927 CPC) |
| Jurisprudência estadual — IRDRs | `jurisprudencia-estadual · buscar_vinculantes` | IRDRs dos TJs |
| Registrar falha do acervo | `acervo · reclame_aqui` | lacuna, erro factual, resultado irrelevante |

## Legislação — `legislacao-federal · buscar_artigos`

**Parâmetros:** `query` (linguagem natural ou palavras-chave, PT; pode incluir o número do artigo), `norma` (sigla/slug opcional para restringir a uma lei: `CDC`, `CPC`, `CF-1988`, `Lei-8078-1990`), `area` (slugs separados por vírgula, opcional), `limit` (padrão 5, máx 10).

Não sabe a sigla da lei? Chame `acervo · listar` (`dominio: "legislacao"`) antes. Para um artigo já conhecido (norma + número), prefira `acervo · consultar`.

**Campos retornados:** `search_id`, `numero`, `citacao` (ex.: `"CDC, art. 14"`), `lei_slug`, `lei_titulo`, `texto`, `is_truncated`, `situacao` (`vigente`|`revogado`|`vetado`|`superada`), `score` (0–1; 1.0 = referência direta), `breadcrumb`, `section_id`, `source_url`.

## Navegar a estrutura da lei e as citações — `legislacao-federal · explorar_contexto`

Às vezes um artigo só faz sentido com o que está em volta. Use `explorar_contexto` para **puxar mais contexto** sem novas buscas semânticas — vale a pena quando o artigo remete a outros, abre um capítulo, ou pode ter sido alterado:

- **Artigos vizinhos:** informe `norma` + `section_id` (de um resultado de `buscar_artigos`) para listar os artigos da mesma seção e subir/descer no sumário um nível por vez (`parent_id`). Bom para ler o instituto inteiro, não só o artigo isolado.
- **Relações de um artigo:** informe o `search_id` para ver o que ele `cita`, é `citado_por` e o que o `altera` — útil para trazer dispositivos correlatos ou conferir alterações. Filtre com `direction` (`cita`/`citado_por`).
- **Limite:** as relações vêm das remissões explícitas e alterações do texto oficial — **não** são exaustivas das remissões em prosa ("na forma do art. X"). `relacoes` vazio não significa ausência de citações; para as remissões textuais, leia o teor integral com `acervo · consultar`.

## Jurisprudência

- **Federal (STF/STJ/TST/CARF):** `jurisprudencia-federal · buscar_precedentes` (amplo) ou `buscar_vinculantes` (só art. 927 CPC). Filtre por `autoridade` (`STF`,`STJ`,`TST`,`CARF` — vírgula para vários), `tipo`, `eficacia`.
- **Estadual (IRDRs dos TJs):** `jurisprudencia-estadual · buscar_vinculantes` — ferramenta distinta, com `localidade` **obrigatório** (UF, ex.: `"SP"`; ou `"BR"` para busca nacional). Um IRDR vincula apenas na UF que o decidiu.

**Eficácia (campo `eficacia`):** `vinculante` (observância obrigatória, art. 927 CPC) · `obrigatoria` (forte deferência, ex.: súmulas comuns) · `persuasiva` (subsídio). `score` baixo (~0.5–0.6) pode indicar correspondência fraca — leia o enunciado e avalie.

## Texto integral — `acervo · consultar`

Retorna o texto **não truncado** (até 5 registros por chamada; o excedente volta em `omitidos`).

- `dominio: "legislacao"`: `search_ids` (handles de uma busca, podem cruzar leis) **ou** `norma` + `numeros` (até 5 artigos da MESMA lei).
- `dominio: "jurisprudencia"` + `esfera` (`"federal"`/`"estadual"`): `search_ids` **ou** uma `citacao` conhecida (ex.: `"STF SV 11"`, `"STJ Tema 69"`, `"TST OJ 191"`, `"TJAM IRDR Tema 5"`). Retorna o registro **mesmo se não vigente** — confira `situacao`.

## Verificações obrigatórias antes de citar

1. **Vigência:** confira `situacao`. Só `vigente` é citado sem ressalva; `revogado`/`vetado`/`superada` nunca como vigente.
2. **Texto integral:** se `is_truncated: true`, chame `acervo · consultar` e cite a partir do texto não truncado — nunca do truncado.
3. **Handle de verificação:** legislação precisa de `citacao` + `source_url`; jurisprudência precisa de `search_id` + `eficacia`. Sem isso, não cite.

## Lacunas — `acervo · reclame_aqui`

Quando a busca vier vazia, contraditória ou irrelevante: **registre** com `category` (`gap` | `inconsistencia` | `erro_factual` | `resultado_irrelevante` | `cobertura_ausente` | `outro`) + `description` específica + `context` (a consulta e os resultados). É esperado pela equipe da Letra da Lei e melhora o acervo — não é opcional quando há lacuna real. Depois, diga ao usuário, de forma explícita, o que não está coberto e onde procurar.

## Como apresentar / citar

- Cite a lei pela `citacao` + `source_url` (verificável no Planalto). Para jurisprudência, identifique `autoridade`, `tipo`, `search_id` e `eficacia`.
- Cole o `texto` verbatim — não parafraseie texto de lei/enunciado.
- Distinga o texto da fonte da sua própria síntese. Não apresente informação como aconselhamento jurídico.

## Idioma

Responda no idioma do usuário. Ao citar, preserve o português original do texto legal; traduza apenas se o usuário estiver em outro idioma.
