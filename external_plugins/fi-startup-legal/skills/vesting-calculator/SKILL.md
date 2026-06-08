---
name: vesting-calculator
description: >
  Finnish startup vesting schedule generator — cliff, monthly vesting,
  good/early/bad leaver treatment, acceleration (single/double trigger),
  exercise window. Explains vesting mechanics in plain language.
  Use when asking "vesting schedule", "how much has [person] vested",
  "what happens if a co-founder leaves".
argument-hint: "[describe: grant size, start date, cliff, vesting period, or 'calculate [name]']"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /fi-startup-legal:vesting-calculator

1. Load profile for option scheme type (TVL §66 vs §66a, option pool size).
2. Collect inputs: grant size, grant date, cliff period, total vesting period, leaver type if applicable.
3. Calculate and display. All outputs are illustrative — actual vesting per signed agreements.

---

## Finnish market standard

- **Total vesting period:** 4 years
- **Cliff:** 1 year (nothing vests before the 1-year anniversary)
- **Post-cliff:** monthly vesting (1/48th per month after the cliff)
- **Exercise window:** Typically **5–10 years** from grant date in Finnish startup practice. 10 years is common in US-influenced term sheets; 5–7 years is also standard in Finnish-law option agreements. Windows shorter than 5 years are restrictive and should be flagged. The grant-level exercise window is separate from the **post-termination exercise window** — see below.

## Post-termination exercise window

**This is often the more practically important number.** Many Finnish option agreements give departing employees only **30–90 days to exercise vested options** after leaving employment, regardless of the grant-level 10-year window. An employee who cannot fund the exercise within that window loses vested options.

When reviewing or drafting an option agreement, always check:
- What is the post-termination exercise window? (30 days, 90 days, longer?)
- Does it differ for Good Leaver vs. Bad Leaver?
- Is the company obligated to give the employee advance notice of termination so they can arrange financing for exercise?

**TVL §66 tax note:** If an employee exercises options after leaving (within the post-termination window), TVL §66 earned income tax arises at exercise but the company may no longer be the employer for payroll withholding purposes. This creates practical complications — route to a Finnish tax advisor for departing employees exercising options.

## Vesting calculation

For any grant, calculate:
- Shares vested at cliff date (25% of total, after 12 months)
- Shares vesting per month after cliff (1/48th of total)
- Total vested as of any given date
- Total unvested remaining

Show as a table: Month | Cumulative vested | Cumulative unvested.

## Leaver calculation

Given a leaver date and leaver type (good/early/bad), calculate:
- Shares already vested → treatment per SHA leaver provisions
- Shares unvested → treatment per SHA leaver provisions
- If bad leaver: all shares (vested + unvested) at nominal value

## Acceleration

**Single-trigger:** full vesting acceleration on involuntary termination following M&A. Finnish market standard for founders.
**Double-trigger:** acceleration only on (1) M&A AND (2) involuntary termination within 12 months. Common for non-founder employees.

Show the post-acceleration vested share count.

---

## Guardrail

Vesting calculations are based on the inputs provided and market-standard terms. Actual vesting is governed by the signed option agreement and SHA. Consult the actual documents — this skill does not read them. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
