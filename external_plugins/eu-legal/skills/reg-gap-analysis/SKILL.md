---
name: reg-gap-analysis
description: >
  Gap analysis between your current practice and a new or changed EU
  regulation — outputs a structured gap list with remediation steps, owners,
  and priority. Use when a new regulation drops, assessing readiness for an
  upcoming requirement, or asking "does DORA apply to us", "are we compliant
  with the AI Act", "DORA gap analysis", "what do we still need to do for
  [regulation]".
argument-hint: "[regulation or description] — e.g. 'dora' or 'EU AI Act high-risk'"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:reg-gap-analysis

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If placeholders, stop: "Run `/eu-legal:cold-start-interview` first."
2. Identify the regulation from the argument.
3. Run the workflow below.
4. Output gap table and remediation plan. This is a draft for attorney review — not a compliance opinion.

---

## EU legislative process context

Unlike US federal rulemaking (notice-and-comment under the APA), EU regulations follow a different pipeline. Flag the current status of the regulation being analysed:

- **Commission proposal** → Council and Parliament positions → **trilogue** → **adoption** → publication in Official Journal → **entry into force** (20 days after publication) → **application date** (often 12–24 months after entry into force)
- **Level 2**: Delegated Regulations, Implementing Acts (Commission); **RTS and ITS** drafted by EBA/ESMA/EIOPA and adopted by the Commission as binding Delegated/Implementing Regulations
- **Level 3**: Guidelines, Recommendations, Q&As (EBA, ESMA, EIOPA — soft law, but supervisory expectations; national competent authorities generally expect compliance)

Note: **Regulations** are directly applicable in all member states. **Directives** require national transposition — obligations may vary by member state.

## Step 1: Identify and confirm

Confirm: "You want a gap analysis against [regulation]. Is this the current in-force version, an upcoming application date, or a recent amendment? And are you analysing your full compliance programme or a specific process?"

## Step 2: Fetch obligations

**Live regulation text:** Before fetching obligations, call `mcp__velvoite__get_eu_regulation_article(regulation_code)` to get the EUR-Lex URL for the regulation being analysed. This allows WebFetch of the actual regulation text to cross-check obligation descriptions against the source. The Velvoite corpus provides obligation intelligence; EUR-Lex provides the verbatim source text.

**If Velvoite available:**
Call `mcp__velvoite__get_canonical_obligations` with the identified regulation and the actor role from profile. This gives the "what the law requires" input — article-level obligations with enforcement history.

**If Velvoite not available:**
Use public regulation text for the identified regulation. Note: without corpus data, obligation completeness is not guaranteed.

## Step 3: Current-practice interview

Group related obligations into clusters (max 8 clusters). For each cluster ask:
> "For [cluster description]: do you have a documented process? Is it implemented and tested? When was it last reviewed?"

Accept one of: ✓ fully implemented / ~ partially implemented / ✗ not implemented / ? unknown.

Ask one cluster at a time. Do not ask all 8 at once.

## Step 4: Gap table

Render:
| Obligation | Article | Status | Gap | Remediation | Owner | Priority |
|---|---|---|---|---|---|---|

Priority:
- **P1** — enforcement risk (high enforcement count in corpus) or deadline within 90 days
- **P2** — material gap in implementation
- **P3** — documentation or evidence gap only

## Step 5: Remediation plan

List P1 gaps. For each:
- Suggested action (1–2 sentences)
- Effort: S (< 1 week) / M (1–4 weeks) / L (1+ months)
- Suggested owner: Legal / Compliance / IT / Operations / Board

Offer to export the gap table as a markdown file for the compliance team.

---

## Guardrail

This analysis identifies gaps based on your answers and the Velvoite corpus (or public regulation text). It is a working document for attorney review — not a legal opinion, not a compliance certification, and not a substitute for advice from a qualified lawyer familiar with your specific circumstances. Regulatory interpretation varies by competent authority and jurisdiction. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.