---
name: redjudicial-legal:resumir-sentencia
version: 0.1.0
description: >
  Use this skill when a user provides a specific Chilean Supreme Court `Rol` (case number) and asks for a structured summary — for example, "resume la sentencia rol 12345-2023" or "qué dijo la Corte Suprema en el rol 78901-2024". Returns hechos, fundamentos, holding, voto disidente (if any), and citations.
allowed-tools:
  - mcp
---

# Resumir sentencia de la Corte Suprema

This skill produces a structured summary of a specific Chilean Supreme Court ruling identified by its `Rol` number.

## Prerequisites

The `redjudicial-legal` MCP server must be connected. Verify it is available before starting research. If the server is not connected, inform the user and stop.

## When to Use

- The user provides a specific `Rol` number (e.g., `Rol Nº 12345-2023`) and asks for a summary.
- The user references a ruling already returned by `investigar-jurisprudencia` and wants more detail.
- The user wants the holding, the reasoning, and any dissenting vote of a specific decision.

## When Not to Use

- Broad jurisprudential research without a specific `Rol` — use `redjudicial-legal:investigar-jurisprudencia` instead.
- Rulings from Cortes de Apelaciones or first-instance courts — not yet in the default index.
- Constitutional Tribunal rulings — not yet available.

## Workflow

### 1. Confirm the `Rol`

- Extract the `Rol` number and year from the user's request. The standard Chilean format is `Rol Nº NNNNN-AAAA` (number, hyphen, year).
- If the user's `Rol` is incomplete or ambiguous, ask before searching.

### 2. Call the tool

- Invoke `redjudicial_search` with:
  - `query` (string, required): the `Rol` and any disambiguating context. Example: `"Rol 12345-2023 Corte Suprema"`.
  - `sources` (array, optional): `["jurisprudencia"]`.
  - `limit` (integer, optional, 1–30, default 3): typically 3 hits will surface the ruling and surrounding excerpts.

### 3. Present the structured summary

If a hit matches the `Rol`, organize the answer in five sections:

- **Identificación**: `Rol`, fecha, tribunal (Corte Suprema), sala, ministros (if surfaced), redactor (if surfaced).
- **Hechos**: brief factual background drawn from the text.
- **Considerandos relevantes**: the central legal reasoning, in two to four bullet points.
- **Decisión**: the holding (acoge / rechaza / revoca / confirma) and the order issued.
- **Voto disidente o concurrente**: if the excerpts surface a separate vote, summarize it; otherwise note "Sin voto disidente surfaceado en el extracto recuperado".

Close with the verifiable link to the official Poder Judicial record (`url` field).

### 4. Handle missing or incomplete data

If the excerpts do not cover all five sections (which is common — they are excerpts of the ruling, not the full text):

- State plainly which sections are not covered by the retrieved excerpts.
- Offer to retrieve additional excerpts with a refined query (e.g., narrowing by considerando number).

**Do not fabricate any of the five sections.** If the excerpts do not contain the holding, say so — do not infer it. If the excerpts do not surface a dissenting vote, do not assume there was none.

**Do not redirect the user to external sources** if the ruling cannot be summarized fully.

## Communication Rules

- Reply in Spanish, in professional neutral Spanish.
- Cite directly from the excerpts when stating a holding or quoting a considerando. Use quotation marks.
- Never invent the names of ministros, the redactor, or a `Rol` number.
- Always include the verifiable link.
- End every response with this one-line disclaimer, in Spanish, on its own line: «Investigación jurídica con fuentes verificables; no constituye asesoría legal. Verifica cada cita en su fuente oficial; la responsabilidad profesional es del abogado.»

## Helpful information

- Product: https://ia.redjudicial.cl
- Roadmap: a dedicated `redjudicial_get_sentence(rol)` tool that returns the full ruling in one call is planned. Until then, this skill uses `redjudicial_search` with the `Rol` as query.
- Support: contacto@redjudicial.cl
