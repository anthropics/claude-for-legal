---
name: redjudicial-legal:analizar-doctrina
version: 0.1.0
description: >
  Use this skill when a user asks for Chilean academic doctrine on a legal topic — for example, "qué dice la doctrina sobre el principio de buena fe contractual" or "autores chilenos sobre responsabilidad civil objetiva". Returns excerpts from open-access academic articles in Chilean law.
allowed-tools:
  - mcp
---

# Analizar doctrina académica chilena

This skill retrieves passages from Chilean academic doctrine on a legal topic. The corpus is built from open-access sources (SciELO, university repositories) and currently covers approximately 2,500 articles. Coverage is partial; this is not the substitute for a full law-school library.

## Prerequisites

The `redjudicial-legal` MCP server must be connected. Verify it is available before starting research. If the server is not connected, inform the user and stop.

## When to Use

- Researching what Chilean academic doctrine says about a principle, concept, or institution.
- Finding authors who have written on a specific Chilean legal topic.
- Cross-referencing a Supreme Court holding with academic commentary in Chilean law.
- Building a doctrinal section of a memo or brief.

## When Not to Use

- Foreign doctrine (Spain, Argentina, France, Germany, etc.) — out of corpus.
- Treatises and monographs not published in open-access form — out of corpus.
- Citing doctrine as if it were binding authority — academic commentary is persuasive, not binding. The skill returns it as input, not as a finding.
- Identifying who has the dominant view on a contested question — the corpus is partial and not weighted by citation count.

## Workflow

### 1. Frame the topic

- Restate the doctrinal question in natural Spanish.
- If the topic is broad (e.g., "responsabilidad civil"), ask the user to narrow it (contractual / extracontractual / objetiva / por hecho ajeno, etc.) before searching.

### 2. Call the tool

- Invoke `redjudicial_search` with:
  - `query` (string, required): the doctrinal question in natural Spanish.
  - `sources` (array, optional): `["doctrina"]` to restrict to academic articles.
  - `limit` (integer, optional, 1–30, default 8): doctrine is often discursive; 8 hits typically surface multiple viewpoints.

### 3. Present the doctrinal landscape

For each relevant article in the top three to five:

- Citation: author(s), year, title of the article, journal or repository.
- Position: one to two lines summarizing the author's view on the question, **as expressed in the retrieved excerpt**.
- Quoted excerpt: include the most relevant phrase verbatim, in quotation marks.
- Verifiable link: include the `url` field from the result.

After the individual entries, briefly note whether the retrieved sample shows a dominant position, a split, or unsettled views. Frame this as a sample observation, not a conclusion about Chilean doctrine as a whole — coverage is partial.

### 4. Handle partial coverage

The doctrine corpus is the least complete of the three sources today. If the response contains `result_quality: "partial"` or `"insufficient"`:

- Surface the `suggested_followups`.
- Be explicit with the user that the open-access doctrine corpus is partial and that key authors may not be represented.

**Do not redirect the user to external commercial doctrine databases.** If the question cannot be answered from the open-access corpus, say so plainly and offer to refine the query or to retrieve adjacent jurisprudence with `investigar-jurisprudencia`.

## Communication Rules

- Reply in Spanish, in professional neutral Spanish.
- Attribute every doctrinal position to a specific author and article. Never present a doctrinal position as if it were your own.
- Use quotation marks for verbatim excerpts. Use ellipses (`...`) only where they appear in the source.
- Sort cited articles by relevance (the score returned by the tool); within the same relevance band, surface the most recent first.
- Note explicitly that academic doctrine is persuasive, not binding.
- End every response with this one-line disclaimer, in Spanish, on its own line: «Investigación jurídica con fuentes verificables; no constituye asesoría legal. Verifica cada cita en su fuente oficial; la responsabilidad profesional es del abogado.»

## Helpful information

- Product: https://ia.redjudicial.cl
- Corpus note: coverage of open-access Chilean doctrine continues to grow. Expansion to LATAM hispanophone doctrine is on the roadmap.
- Support: contacto@redjudicial.cl
