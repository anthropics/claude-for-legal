---
name: founder-agreement
description: >
  Co-founder agreement and vesting setup — equity split, roles, vesting schedule
  (Finnish good/bad/early leaver), IP assignment, non-compete validity check.
  Use when setting up co-founder terms, asking "founder agreement checklist",
  "vesting schedule", "what should a co-founder agreement cover in Finland".
argument-hint: "[number of founders, or describe the situation]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /fi-startup-legal:founder-agreement

1. Load `~/.claude/plugins/config/fi-startup-legal/CLAUDE.md`. If placeholders, stop: setup first.
2. Call `mcp__velvoite__get_finnish_statute("TSL", "3:5")` for current non-compete rules.
3. Run the workflow below. Output is a draft checklist — attorney review required before signing.

---

## Purpose

A founder agreement (typically part of or alongside the osakassopimus) covers what happens if a co-founder leaves. Most Finnish startup disputes stem from a missing or vague founder agreement. This skill walks through the key terms.

## Key terms to cover

### Equity split
Ask: "How is equity split between founders?" Note: equal splits (50/50, 33/33/33) are common but can cause deadlock. Suggest a tiebreaker mechanism if equal split.

### Founder vesting
Finnish market standard (following seriesseed.fi): 4-year total, 1-year cliff.

**Leaver mechanics (three-tier standard):**

| Type | Definition | Share treatment |
|---|---|---|
| Good Leaver | Leaves after cliff, no fault | Keeps vested shares at fair market value |
| Early Leaver | Leaves before cliff OR voluntarily before 2 years | Returns unvested shares at nominal value (subscription price) |
| Bad Leaver | Termination for cause, breach, non-compete violation | Returns ALL shares (vested + unvested) at nominal value |

Call `mcp__velvoite__get_finnish_statute("OYL", "3")` for share buyback/redemption rules under Finnish company law.

### IP assignment
Every founder must assign all relevant IP to the company at founding. This includes:
- Software, code, designs created before incorporation (if related to the business)
- Patents, trade secrets, know-how
- Domain names, brand assets

Flag: did any founder previously work for an employer in this field? Employee invention rules (Laki oikeudesta työntekijän tekemiin keksintöihin) may apply. Route to `/fi-startup-legal:ip-assignment` for full IP audit.

### Non-compete
Finnish law (TSL §3:5, fetched live from Finlex): non-compete max 12 months after employment ends. Compensation required if restriction exceeds 6 months:
- 6–12 months restriction → 50% of salary for restricted period
- Note: founder non-competes in SHA are shareholder agreements, not employment law — different rules may apply. Route to outside counsel for founder-specific non-competes >12 months.

### Decision-making
For 2 founders: veto rights allocation, deadlock resolution.
For 3+ founders: voting thresholds for major decisions (new share issuance, sale, key hires).

---

## Guardrail

Founder agreements and vesting mechanics have significant long-term consequences. Have a Finnish startup lawyer review the final terms before signing. Recommended firms: Nordic Law, Dottir, Lexia Growth, Fondia. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
