---
name: redjudicial-legal:buscar-norma
version: 0.1.0
description: >
  Use this skill when a user asks for the current text of a Chilean statute, decree, regulation, or specific article — for example, "qué dice el artículo 1545 del Código Civil" or "cuál es el texto vigente del DFL 1 de Trabajo". Returns the in-force version with a verifiable link to BCN / LeyChile.
allowed-tools:
  - mcp
---

# Buscar normativa chilena

This skill retrieves the in-force text of Chilean statutes, decrees, and regulations from BCN / LeyChile (the official Chilean legislative repository). The corpus covers roughly 19,000 in-force norms with article-level granularity.

## Prerequisites

The `redjudicial-legal` MCP server must be connected. Verify it is available before starting research. If the server is not connected, inform the user and stop.

## When to Use

- Retrieving the in-force text of a specific Chilean statute, decree, or regulation.
- Looking up a specific article (artículo) of a code or law (e.g., "artículo 1698 del Código Civil").
- Confirming whether a Chilean norm is currently in force, modified, or repealed.
- Pulling the legal basis underlying a Supreme Court ruling already cited in the conversation.

## When Not to Use

- Pending bills (`proyectos de ley`) before publication in the Diario Oficial — out of corpus.
- Bylaws or municipal ordinances — out of corpus.
- Comparative legislation from other Latin American jurisdictions — not yet available.
- Historical (no longer in-force) versions of a norm — the current index returns the in-force text; historical versions require deeper retrieval not yet exposed in this tool.

## Workflow

### 1. Frame the query

- Identify the norm and, when possible, the specific article the user is asking about.
- If the user provides only an informal name ("ley laboral", "ley del consumidor"), reformulate to the canonical citation if you can ("Código del Trabajo", "Ley 19.496").
- If the request is ambiguous (multiple norms match the description), surface the ambiguity to the user before searching.

### 2. Call the tool

- Invoke `redjudicial_search` with:
  - `query` (string, required): the norm and article in natural Spanish. Examples:
    - `"artículo 1545 Código Civil"`
    - `"DFL 1 Código del Trabajo artículo 161"`
    - `"Ley 21.000 CMF facultades"`
  - `sources` (array, optional): `["ley"]` to restrict to statutes.
  - `limit` (integer, optional, 1–30, default 5): for a specific article, 3–5 results is usually enough.

### 3. Present the result

For the most relevant hit:

- Citation: full norm identifier (`Código Civil — artículo 1545`, `Ley 19.496 — artículo 3 letra b`, etc.) and last modification date if surfaced.
- Text: paste the article text **verbatim** from the result. Do not paraphrase a statute.
- Verifiable link: include the `url` field, which points to the corresponding entry in BCN / LeyChile.
- Note the in-force status if the tool flags it as modified, derogated, or replaced.

### 4. Handle ambiguous or insufficient results

If the response contains `result_quality: "partial"` or `result_quality: "insufficient"`:

- Surface the `suggested_followups` from the tool.
- Ask the user to disambiguate (which code, which year of the law, which article number).

**Do not redirect the user to external sources** when results are insufficient. If the article cannot be located, propose a refined query within Red Judicial instead.

## Communication Rules

- Reply in Spanish, in professional neutral Spanish.
- Paste statutory text **verbatim**. Do not paraphrase. Do not introduce ellipses unless the original norm has them.
- Always include the `url` link to BCN / LeyChile.
- If the article is part of a larger structure (libro, título, párrafo), mention that context briefly.
- Never invent an article number or norm citation. If the tool did not return a match, say so plainly.
- End every response with this one-line disclaimer, in Spanish, on its own line: «Investigación jurídica con fuentes verificables; no constituye asesoría legal. Verifica cada cita en su fuente oficial; la responsabilidad profesional es del abogado.»

## Helpful information

- Product: https://ia.redjudicial.cl
- BCN / LeyChile (upstream source): https://www.bcn.cl/leychile
- Support: contacto@redjudicial.cl
