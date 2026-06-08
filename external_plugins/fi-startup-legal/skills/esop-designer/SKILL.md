---
name: esop-designer
description: >
  Finnish ESOP/option scheme design — TVL §66 vs §66a decision tool, the proposed
  2026 reform (options taxed at sale rather than exercise — NOT yet enacted as of
  May 2026), AGM approval requirements, option pool sizing, typical Finnish vesting
  terms. Use when asking "how do we set up options", "ESOP for our startup",
  "TVL §66 vs §66a", "how does the 2026 option reform affect us".
argument-hint: "[describe the situation: company stage, number of beneficiaries, amounts]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /fi-startup-legal:esop-designer

1. Load profile. If placeholders, stop.
2. Call `mcp__velvoite__get_finnish_statute("TVL", "66")` — fetch live TVL §66 text.
3. Call `mcp__velvoite__get_finnish_statute("TVL", "66a")` — fetch live TVL §66a text.
4. Call `mcp__velvoite__get_finnish_statute("OYL", "10")` — AGM approval requirements for option schemes.
5. Call `mcp__velvoite__search_kho_decisions` for the current and two prior years. Fetch each listing URL and identify decisions related to stock options, option taxation, TVL §66, or startup equity. Call `mcp__velvoite__get_kho_decision(year, number)` for each relevant case. Surface any precedents that affect the §66 vs §66a analysis or option scheme validity. If none found, omit.
6. Run the §66 vs §66a decision workflow below. Output is advisory — tax advice requires a qualified tax advisor.

---

## TVL §66 vs §66a — which to use?

This decision is the most important tax choice for Finnish startup equity compensation. Always fetch current statute text before answering — the text is the ground truth.

### TVL §66 (stock options) — current law and proposed reform

**CURRENT LAW (default — apply this unless the live statute text shows otherwise):**

Under the law in force as of May 2026, options granted under TVL §66 are taxed as earned income (ansiotulo) **at exercise** — the spread between fair market value at exercise and the subscription price is taxed at progressive income tax rates (typically 30–40%+). The tax liability arises at exercise, before any exit occurs. This is the cash-flow problem for startup employees: tax is due even though the shares are illiquid.

On the eventual share sale: acquisition cost = subscription price + the amount already taxed as earned income at exercise (no double taxation).

**2026 GOVERNMENT PROPOSAL — NOT YET ENACTED AS OF MAY 2026:**

The Finnish government has proposed deferring this earned-income taxation from exercise to sale for options in qualifying unlisted companies. This would eliminate the cash-flow problem by aligning tax timing with the liquidity event.

**IMPORTANT:** As of May 2026, this is a legislative proposal only. It has NOT been enacted into law. Do not present it as current law.

**After fetching the live TVL §66 text:** read the statute carefully. If the enacted text now includes sale-timing language (e.g. "taxation occurs at the time of sale" or "myyntihetki"), the reform has been enacted — present the new rules and note the effective date. If the text still reads "taxation at exercise" (merkintähetki/hankintahetki), current law applies.

### TVL §66a (directed share issue at mathematical value)

An alternative to options: the company issues new shares to employees at the "mathematical value" (substansarvo — net assets divided by share count). If this is below market value, the difference is not income-taxed at subscription — the entire gain is treated as capital income when the shares are sold (~30% vs. up to 40%+ income tax).

Conditions (verify from fetched §66a statute): company must be unlisted; employee must work in the company; issue price must be at or above mathematical value.

**Additional §66a conditions (all must be met):**
- **Majority-of-employees rule:** The directed share issue must be offered to **more than half of the company's employees**. A targeted grant to selected founders or key hires does NOT qualify — this is a common and costly mistake.
- **>10% shareholder exclusion:** Any person (together with their spouse and minor children) who already owns more than 10% of the company's shares or votes **cannot participate** in a §66a issue and is excluded from the majority count.
- **Parent company restriction:** A parent company cannot use §66a to issue its own shares to employees of a subsidiary. The issuing company must be the direct employer.

If any of these conditions are not met, the subscription falls under TVL §66 (exercise taxation) rather than §66a.

Key difference from §66: shares are issued immediately (no vesting cliff possible via the scheme itself — but a separate SHA leaver mechanism can claw back shares). This makes §66a less flexible for standard cliff-and-monthly-vest ESOP structures.

**Practical comparison table (based on current law as of May 2026):**

| Factor | TVL §66 (current law) | TVL §66 (if reform enacted) | TVL §66a |
|---|---|---|---|
| Tax timing | At exercise | At sale | At sale |
| Tax type on gain | Earned income (progressive) | Earned income (progressive) | Capital gains (~30%) |
| Subscription price | At least FMV at grant | At least FMV at grant | At least mathematical value |
| Flexibility | High (strike price, cliff, vesting) | High | Lower (shares issued immediately) |
| AGM approval | Required | Required | Required |
| Cash-flow risk for employee | HIGH (tax before exit) | Low | Low |
| Good for | Standard ESOP if reform enacted | Standard startup ESOP | Early employees / low-net-asset stage |

### Recommendation logic

1. **Check if the §66 reform has been enacted** (read the live statute text fetched above).
2. If reform enacted: §66 is the standard choice for most startups. §66a advantage is reduced but still valid for capital gains rate benefit.
3. If reform NOT enacted (current law): §66 creates cash-flow risk. For early-stage companies with very low mathematical value, §66a may be more employee-friendly (capital gains rate, tax only at sale). Discuss the cash-flow risk explicitly with employees before granting §66 options.
4. If company has significant net assets (mathematical value close to market value): §66a advantage is small → use §66.

### AGM mechanics

From fetched OYL §10 text, apply current rules:
- Share options require approval from an extraordinary or annual general meeting
- Resolution must specify: total number of options, subscription price, subscription period, deviation from pre-emption rights (and reason — typically "to implement the employee option scheme")
- Board of directors then grants individual allocations based on the AGM authorisation

---

## Guardrail

Option scheme design has significant tax consequences for employees and the company. The TVL §66 reform was a government proposal as of May 2026 — verify current enactment status using the live statute text fetched above. This skill reads live Finlex data but does not replace advice from a Finnish tax advisor (veroasiantuntija). Before implementing any option scheme, have the scheme documents reviewed by a lawyer. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
