---
name: first-hire-contract
description: >
  Finnish startup first employment contract — mandatory terms under TSL,
  trial period, notice period, non-compete validity, IP assignment, ESOP
  offer mechanics. Use when hiring the first employee, reviewing a draft
  contract, or asking "what must be in a Finnish employment contract".
argument-hint: "[describe the role or paste the contract draft]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /fi-startup-legal:first-hire-contract

1. Load profile.
1.5. **Sector/TES gate:** If the company sector is unknown or not set in the profile, ask before running the checklist — TES (collective agreement) applicability depends on sector and cannot be assessed without it. If a sector-specific TES applies, note which TES and flag that its terms may override TSL defaults on notice periods, trial period, and compensation.
2. Call `mcp__velvoite__get_finnish_statute("TSL", "1:4")` — mandatory employment contract terms.
3. Call `mcp__velvoite__get_finnish_statute("TSL", "3:5")` — non-compete rules.
4. Call `mcp__velvoite__get_finnish_statute("TSL", "6:3")` — employee notice periods (live). Call `mcp__velvoite__get_finnish_statute("TSL", "6:4")` — employer notice periods (live). Derive notice period rules from the fetched text. If MCP unavailable: note `[TSL §6:3/§6:4 not fetched live — verify notice periods at finlex.fi before use]` and use the fallback table below.
5. Run checklist. Draft for attorney review.

---

## Mandatory terms (TSL §1:4, fetched live)

Every Finnish employment contract must cover (from fetched statute):
- [ ] Employer name and address
- [ ] Employee name and address
- [ ] Start date
- [ ] Duration: indefinite (toistaiseksi voimassa oleva) or fixed-term (with reason if fixed-term)
- [ ] Place of work (or principle that employee works in multiple locations)
- [ ] Main duties (työn pääasialliset tehtävät)
- [ ] Applicable collective agreement (TES), if any
- [ ] Salary and payment interval
- [ ] Normal working hours
- [ ] Annual holiday accrual reference (Vuosilomalaki)
- [ ] Notice period (irtisanomisaika)

If not given in writing at start: employer must provide within 7 days of start date (TSL §2:4).

## Trial period (koeaika)
Maximum 6 months (TSL §1:4). During trial: either party can terminate immediately with no notice, no reason required. If fixed-term contract < 12 months: trial period cannot exceed half the contract duration.

## Notice periods (fallback — from live statute fetch above; use only if MCP unavailable)
Employer notice (TSL §6:4) by service length:
- < 1 year: 14 days
- 1–4 years: 1 month
- 4–8 years: 2 months
- 8–12 years: 3 months
- 12–15 years: 4 months
- > 15 years: 6 months

Employee notice (TSL §6:3):
- < 5 years: 14 days
- > 5 years: 1 month

## Non-compete clause
See `/fi-startup-legal:non-compete-check` for full analysis. Key rules (TSL §3:5, live):
- Max 12 months after employment ends
- Compensation required if restriction > 6 months
- Must be "particularly weighty reason" (erityisen painava syy) to justify a non-compete

## IP assignment

> ⚠️ **Do not copy-paste a clause from here.** IP assignment language is jurisdiction-specific and fact-dependent. Have a Finnish employment lawyer draft this clause for your specific situation.

The contract must address: (a) inventions created during employment, (b) prior inventions the employee brings to the company, (c) the assignment mechanism and consideration, and (d) works created outside working hours. Run `/fi-startup-legal:ip-assignment` for the full IP audit checklist before any due diligence or funding round.

Note: Finnish employee invention law (Laki oikeudesta työntekijän tekemiin keksintöihin) gives the employer rights to employment-related inventions by default — an explicit assignment clause removes ambiguity but must be correctly drafted to cover all scenarios.

## YEL for founders
**YEL registration threshold:** The lower earnings limit (alin YEL-työtulo) is adjusted annually by an earnings index. The 2025 figure was approximately €9,010/year. For the current year's exact threshold, check **etk.fi** (Eläketurvakeskus) or **kela.fi** before advising a founder on their YEL obligation — using a stale figure could cause a founder to incorrectly conclude they are below the threshold. Failure to register results in retroactive claims with interest.

---

## What this skill does NOT do

- **Full contract draft**: Produces a checklist and annotated guidance — not a complete, ready-to-sign employment contract.
- **TES (collective agreement) terms**: TES coverage is sector-specific. If a TES applies, its terms may override TSL defaults on notice periods, trial period, and compensation.
- **Fixed-term contracts**: Require a statutory reason (TSL §1:3). This skill does not assess whether a proposed fixed-term arrangement is legally valid.
- **Remote work / cross-border**: Cross-border remote work creates tax and social security complexity outside this skill's scope.
- **Legal advice**: Outputs are legal support tools. No attorney-client relationship or privilege is created.

---

## Guardrail

Employment contracts create binding legal obligations. Have a Finnish employment lawyer or HR legal service (Fondia, Lexly) review before issuing. Collective agreement obligations depend on the industry sector — check if a TES applies. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
