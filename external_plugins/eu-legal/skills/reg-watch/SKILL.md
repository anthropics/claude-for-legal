---
name: reg-watch
description: >
  What changed in EU financial regulation recently — new publications,
  guidelines, Q&As, RTS/ITS, supervisory notices — scoped to your entity
  type. Default 7-day lookback. Use when asking "what's new", "any DORA
  updates this week", "what changed in EU reg", "weekly regulatory digest",
  or similar.
argument-hint: "[days] — e.g. '14' for two weeks"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:reg-watch

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If placeholders, stop: "Run `/eu-legal:cold-start-interview` first."
2. Check Velvoite: if `VELVOITE_API_KEY` not set, run Fallback.
3. Run the workflow below.

---

## Parse args

- `days` (optional integer, default 7): lookback window.

## Workflow

Call `mcp__velvoite__get_recent_changes` with `days` from args.

For any item in the results that carries a CELEX number (format: `3YYYYTNNNN`, e.g. `32022R2554`), call `mcp__velvoite__get_eurlex_document(celex)` to resolve the canonical title and date before rendering. Use the returned `url` as the link target. If CELLAR is unavailable, fall back to the URL from the corpus result.

**Before grouping:** Check urgency. Any item with urgency level 1 or 2 in the corpus results must be surfaced first as a banner:

> 🔴 **CRITICAL — Requires immediate attention:**
> [list each urgency 1-2 item: title, source, one-line summary, and action deadline if present]

If no urgency 1-2 items: omit the banner entirely.

Group remaining results by regulation (most-active regulation first). For each item render:
- **Title** (linked if URL available)
- Source: EBA / ESMA / EIOPA / FIN-FSA / BaFin / EUR-Lex / Commission / other
- Document type: guideline / Q&A / RTS / ITS / supervisory notice / consultation / decision
- One-line plain-language summary of what it says

Regulations the entity does not participate in (actor role = N/A in profile): show in a collapsed "Other EU regulatory activity" section at the bottom, not in the main body.

If no results for a regulation the entity cares about: "No new publications for [regulation] in the last [N] days." — say this explicitly rather than omitting.

Add at the end:
> "Source: Velvoite corpus (EUR-Lex, EBA, ESMA, EIOPA, FIN-FSA, BaFin). AI-classified — verify at the original source for formal compliance purposes."

---

## Fallback (VELVOITE_API_KEY not set)

Tell the user: "Regulatory monitoring requires the Velvoite corpus. Add `VELVOITE_API_KEY` to your `.envrc` to enable this skill. Free 30-day trial at velvoite.eu.

In the meantime, check directly:
- EUR-Lex: eur-lex.europa.eu (Official Journal, regulations, directives)
- EBA: eba.europa.eu/news-press
- ESMA: esma.europa.eu/press-news
- EIOPA: eiopa.europa.eu/publications
- FIN-FSA: finanssivalvonta.fi/en/news
- BaFin: bafin.de/SharedDocs/Veroeffentlichungen/EN"

---

## Disclaimer

Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
