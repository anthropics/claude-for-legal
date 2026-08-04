---
name: oy-setup
description: >
  OY (Osakeyhtiö) incorporation wizard — walks through company name check,
  yhtiöjärjestys (articles of association), osakassopimus (shareholder agreement)
  checklist, and PRH registration steps. Use when incorporating a new Finnish
  company or when asking "how do I set up an OY", "incorporation checklist",
  "yhtiöjärjestys template".
argument-hint: "[company name to check]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /fi-startup-legal:oy-setup

1. Load `~/.claude/plugins/config/fi-startup-legal/CLAUDE.md`. If placeholders, stop: "Run `/fi-startup-legal:startup-cold-start` first."
2. Run the incorporation wizard below.
3. Output: step-by-step checklist. Every output is a draft — not legal advice.

---

## Step 1: Company name check

If a company name was provided as an argument or is in the profile, call `mcp__velvoite__search_finnish_companies(name)` to check if the name is available. Report: "Available — no exact match found" or "Conflict — [company] already exists with business ID [X]."

Key name rules (OYL §2:3): must include "Oy", "Oyj", or "Ab"; must be distinguishable from existing names in the register; no misleading terms (e.g. cannot imply bank/insurance unless licensed).

## Step 2: Incorporation checklist

Call `mcp__velvoite__get_finnish_statute("OYL", "2")` to retrieve current share capital and formation rules.

Walk through each item:

**Before PRH:**
- [ ] Company name confirmed available (PRH search above)
- [ ] Share capital: €0 minimum since 2019 (OYL §2:1). Typical startup: 2,500 shares at €0.01 = €25 paid-in capital.
- [ ] Shareholders: list all founders + initial equity split
- [ ] Perustamissopimus (memorandum of association): must include company name, address, founders, shares, share capital, board members, financial year
- [ ] Yhtiöjärjestys (articles of association): minimum content per OYL §2:3 — company name, domicile, line of business
- [ ] Board: minimum 1 member (+ deputy if only 1 member). EEA residency required unless PRH exemption obtained.
- [ ] Auditor: required if 2+ of: (1) turnover >€12M, (2) balance sheet >€6M, (3) >50 employees. Most early startups: no auditor required.

**PRH registration:**
- [ ] Register at prh.fi/yritykset/perustaminen (online, ~1–3 business days). **PRH registration fee (2026):** Verify the current fee at prh.fi/hinnasto before filing — fees are updated annually. As a reference point, recent online incorporation via YTJ e-service has been approximately €275–400 depending on the path chosen. The online (sähköinen) route is both faster and typically cheaper than paper equivalents (which are no longer accepted from 1.1.2026).
- [ ] YEL (entrepreneur pension): sole founder working in own company must register YEL within 3 months if annual work income >€9,010.28 (2026 threshold)
- If no board member or managing director (toimitusjohtaja) is resident in Finland, the company must designate a **Finnish address agent** (asiamies) — required under OYL if all representatives are EEA-resident but based abroad.

**After incorporation:**
- [ ] Open business bank account
- [ ] Register for VAT if turnover will exceed €15,000/year (threshold 2026)
- [ ] Sign osakassopimus (shareholders' agreement) — not required by law but essential for startups

## Step 3: Yhtiöjärjestys guidance

PRH provides an official template. Startups typically add these non-mandatory clauses:
- Lunastuslauseke (redemption clause): right for existing shareholders to buy shares before transfer to outsider
- Suostumuslauseke (consent clause): share transfers require board approval
- Note: drag-along and tag-along cannot be put in yhtiöjärjestys — they belong in osakassopimus

## Step 4: Next steps

After incorporation: run `/fi-startup-legal:founder-agreement` to set up your co-founder agreement.

---

## Guardrail

Incorporation involves legal and tax obligations. This checklist covers the standard path. If any founder is outside the EU/EEA, if the company has unusual share structure, or if you're in a regulated sector, consult a lawyer before filing. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
