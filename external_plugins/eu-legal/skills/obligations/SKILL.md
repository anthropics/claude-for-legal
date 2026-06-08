---
name: obligations
description: >
  List the EU regulatory obligations that apply to your entity — scoped to
  your entity type and actor roles. Supports an optional regulation filter.
  Use when asking "what obligations apply to us", "what does DORA require",
  "our MiCA obligations", "show me GDPR duties", or similar.
argument-hint: "[regulation] [limit] — e.g. 'dora' or 'gdpr 20'"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:obligations

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If placeholders, stop: "Run `/eu-legal:cold-start-interview` first."
2. Check Velvoite: if `VELVOITE_API_KEY` not set, run Fallback.
3. Run the workflow below.

---

## Purpose

Show what EU law actually requires — scoped to this entity's type and roles, not a generic list. Sorted by enforcement frequency so the highest-risk obligations surface first.

**Audience:** Compliance officers and in-house legal teams at EU-regulated entities. Output is a structured compliance reference — not a compliance programme or legal advice. Have qualified legal counsel validate the obligations list before relying on it as a compliance baseline.

**Delegation:** This skill lists obligations. It does not assess your compliance posture against them, prioritise remediation, or confirm which obligations your entity has already addressed. Run `/eu-legal:reg-gap-analysis` for a structured gap assessment.

## Parse args

- `regulation` (optional): one of `dora`, `gdpr`, `mica`, `ai_act`, `aml`, `mifid2`, `crd_crr`, `psd`, `idd`, `solvency_2`, `sfdr`, `emir`, `bmr`. If not provided, query all regulations.
- `limit` (optional integer, default 30): max obligations to show.

## Read from profile

From `~/.claude/plugins/config/eu-legal/CLAUDE.md`:
- Entity type (for context)
- Actor roles table — find the row for the requested regulation, use that role as `actor_role` param

## Workflow

### Step 1: Summary count

Call `mcp__velvoite__get_obligation_summary` with `actor_role` from profile for the requested regulation (omit if querying all).

Show a summary table:
| Regulation | Total obligations | Notes |
|---|---|---|

### Step 2: Obligation detail

Call `mcp__velvoite__get_canonical_obligations` with:
- `regulation`: from args (omit if all)
- `actor_role`: from profile for that regulation
- `limit`: from args

Render as a markdown table, sorted by enforcement count descending:
| # | Regulation | Article | Obligation summary | Enforcement count |
|---|---|---|---|---|

### Step 3: Highlight top 3

Bold the top 3 rows. Add below the table:
> "**Source: Velvoite corpus (enforcement-frequency ranked).** The top 3 obligations above have the highest enforcement frequency — use this as a starting point for your compliance programme, not as a complete or verified baseline."

### Step 4: Related deadlines prompt

If any obligations have upcoming deadlines, note: "Run `/eu-legal:deadlines` to see your compliance calendar."

---

## Fallback (VELVOITE_API_KEY not set)

Show general obligations for the entity type based on public regulation text. Cover: GDPR Art. 5/6/13/15/17/25/32/33, DORA Art. 5-15 (for financial entities), AI Act Art. 10/13/14/15 (for deployers/providers) — whichever apply to the entity type from profile.

Add the following header above the fallback table:
> **⚠️ Source: model knowledge — public regulation text `[last_verified: 2026-06-01]`.** This list has not been verified against the Velvoite corpus. It may be incomplete and does not reflect enforcement frequency, supervisory guidance, or RTS/ITS developments. Connect Velvoite for corpus-verified results.

Add at the end:
> **Velvoite corpus not connected.** For article-level requirements with enforcement frequency, authority guidance, and obligation-specific corpus answers: add `VELVOITE_API_KEY` to your `.envrc`. Free 30-day trial at velvoite.eu.

---

## What this skill does NOT do

- **Gap assessment**: Does not assess whether your entity complies with listed obligations — run `/eu-legal:reg-gap-analysis` for that.
- **National implementing law**: Covers EU-level regulatory obligations only. Finnish tietosuojalaki, German BDSG, and other national transposition acts are not separately enumerated.
- **Completeness guarantee**: The Velvoite corpus covers major EU regulations — it may not include all applicable Level 2/3 measures, ESMA Q&As, or supervisory expectations.
- **Legal advice**: Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created.

---

## Guardrail

This output is a structured compliance reference. It is not a compliance programme, a legal opinion, or a confirmation that listed obligations apply to your specific situation. Verify applicable obligations with qualified legal counsel before treating this as your compliance baseline. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
