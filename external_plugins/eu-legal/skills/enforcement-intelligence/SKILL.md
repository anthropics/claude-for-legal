---
name: enforcement-intelligence
description: >
  What do regulators actually fine companies for — and what does case law say
  about it? Uses Velvoite enforcement decisions plus Finnish KHO and German
  court case law to produce a "fix this first" action list for your entity type.
  Use when asking "what are we most likely to get fined for", "enforcement
  trends", "what did BaFin fine payment institutions for", "KHO precedents on
  DORA", "top compliance risks", or similar.
argument-hint: "[regulation] [jurisdiction] — e.g. 'dora' or 'gdpr fi'"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:enforcement-intelligence

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If placeholders, stop: "Run `/eu-legal:cold-start-interview` first."
2. Check Velvoite: if `VELVOITE_API_KEY` not set, run Fallback.
3. Run the workflow below.
4. Output is for attorney review and compliance planning — not a legal opinion.

---

## Purpose

Most compliance tools tell you what the rules say. This skill tells you what regulators actually enforce. The difference: the rules are aspirational; enforcement decisions are evidence of what authorities prioritise, what they consider a material breach, and how much they fine for it. Combined with court case law (KHO for Finland, administrative courts for Germany), you get a defensible compliance posture grounded in real decisions, not just text.

## Parse args

- `regulation` (optional): focus on one regulation — `dora`, `gdpr`, `mica`, `ai_act`, `aml`, `mifid2`, etc. Default: all regulations relevant to entity type.
- `jurisdiction` (optional): `fi` (Finland — includes KHO case law), `de` (Germany — includes German court decisions), `eu` (EU-wide, no national case law layer). Default: primary jurisdiction from profile.

## Read from profile

- Entity type and actor roles → scope enforcement queries
- Primary jurisdiction → determines which case law layer to use

## Workflow

### Step 1: Enforcement landscape

Call `mcp__velvoite__get_enforcement_decisions` with entity type from profile and regulation filter if provided. Sort by fine amount descending.

Then call `mcp__velvoite__get_enforcement_intelligence` to get the top violated obligations summary.

Show:
**Enforcement summary for [entity type] — [regulation or all]**

| Rank | Violation area | Cases | Largest fine | Authority |
|---|---|---|---|---|

Cap at top 5 violation areas to keep output actionable.

### Step 2: Deep-dive top 3 violations

For each of the top 3 violation areas:

1. **What happened** — summarise 1–2 representative enforcement decisions: what the company did (or failed to do), what the authority found, what the fine was.

2. **What the authority expected** — extract the positive obligation from the decision: "The authority found that [entity type] must maintain X, test it Y-frequently, and document Z."

3. **Case law layer:**
   - **EU level (all jurisdictions):** Call `mcp__velvoite__search_cjeu_cases` with the violation topic as query (e.g. `"payment institution authorisation"`, `"data protection supervisory authority"`, `"ICT incident reporting"`). Fetch the URL for any directly relevant judgment. Surface as: "CJEU [celex]: [one-line holding]."
   - **Finnish level:** If jurisdiction includes `fi`, call `mcp__velvoite__search_kho_decisions` for the current and prior year to get the listing URL, then fetch it to identify relevant decisions by title. Call `mcp__velvoite__get_kho_decision(year, number)` for each relevant case and fetch its URL. Surface as: "KHO:[year]:[number]: [one-line holding]."
   - **German level:** If jurisdiction includes `de`, use `mcp__velvoite__search_cjeu_cases` with a German-context query to surface any CJEU cases that German courts have applied to this obligation type. Note: BVerwG/VG decisions are not available via MCP — reference by citation if known from corpus results.

4. **What to check in your organisation** — 3 specific questions to ask your compliance team about this violation area.

### Step 3: Fix-this-first action list

Synthesise a prioritised action list:

**Top 5 actions to reduce enforcement risk — [entity type] / [regulation(s)]**

| Priority | Action | Based on | Urgency |
|---|---|---|---|
| 1 | [Specific action] | [Authority / case] | [High / Medium] |
| ... | | | |

Urgency is High if: fine > €100k, multiple enforcement actions for same violation, or obligation has a near-term deadline in the compliance calendar.

### Step 4: Cross-reference

Note: "Run `/eu-legal:obligations [regulation]` to see the full obligation list. Run `/eu-legal:reg-gap-analysis [regulation]` to assess your current compliance posture against these risk areas."

---

## Fallback (VELVOITE_API_KEY not set)

Enforcement intelligence requires the Velvoite corpus — enforcement decisions and case law are not available from public text alone.

Add `VELVOITE_API_KEY` to your `.envrc` and run `direnv allow`. Free 30-day trial at velvoite.eu.

In the meantime, the EU enforcement landscape by regulation:
- **GDPR**: largest fines from CNIL (France), DPC (Ireland), BaFin. Top violation areas: consent, data transfers, breach notification, data minimisation.
- **DORA**: enforcement begins in 2025. EBA, ESMA, EIOPA as Joint Oversight. Key focus: ICT incident reporting, third-party risk, resilience testing.
- **AML/CFT**: FIN-FSA has levied fines on Finnish payment institutions for inadequate transaction monitoring, CDD failures.
- **MiFID II**: ESMA and national NCAs. Top areas: best execution, transaction reporting, client onboarding.

---

## Guardrail

Enforcement decisions describe past regulatory action in specific factual contexts. They are not a definitive statement of legal obligation for your organisation. Case law citations are from the Velvoite corpus and should be verified at source before reliance. This output is a working document for attorney review — not a legal opinion. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.