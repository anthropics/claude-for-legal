---
name: worker-classification
description: >
  Classify a worker as employee vs. independent contractor under EU, Finnish,
  and German law. Applies the Platform Work Directive (2024/2831) rebuttable
  presumption, TSL (Finland), and §611a BGB (Germany). Use when asked "is this
  person an employee or contractor?", "can we use a freelancer for this?",
  "contractor classification risk", or "platform worker classification".
argument-hint: "[describe the working arrangement or paste the contract]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:worker-classification

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If placeholders, stop: "Run `/eu-legal:cold-start-interview` first."
2. Load `~/.claude/plugins/config/eu-legal/employment.md` if it exists. Note hiring countries and KSchG/YT-laki thresholds.
3. Run the workflow below.
4. Output: classification conclusion, risk level, and recommended action.

---

## Purpose

Worker misclassification is a high-exposure risk: tax authorities (Verohallinto in Finland, Finanzamt in Germany), social security bodies, and labour courts all apply their own tests — and the consequences (back taxes, social contributions, fines, retroactive employment rights) are significant. This skill applies the legal tests; a qualified lawyer must review before acting on the conclusion.

---

## Step 1: Gather facts

Ask the user to describe the arrangement. If not already provided, ask:

1. "Who sets the remuneration (rate, schedule, amount) — the hiring company or the worker themselves?"
2. "Is work performance monitored electronically, or are working hours/output tracked by the company's systems?"
3. "Does the company give instructions about how to perform the work — conduct, dress code, tools, methodology?"
4. "Can the worker build their own client base, work for competitors, or subcontract the work to others?"
5. "Does the worker use their own tools and equipment, or the company's?"
6. "Is the worker economically dependent on this one company (>70% of income)?"
7. "Is the worker integrated into the company's organisation — regular team meetings, company email, company systems?"
8. "What jurisdiction(s) are relevant? (Country where work is performed, country of contract governing law)"

Accept answers in free text or as a summary of an existing contract.

---

## Step 2: Apply Platform Work Directive test (EU baseline)

**Directive 2024/2831 Art. 4 — applies where platform work is involved.**

> **Transposition status `[last_verified: 2026-06-01]`:** Directive 2024/2831 was adopted November 2024; transposition deadline is December 2026. As of June 2026, neither Finland nor Germany has enacted transposing national legislation. Apply these indicators as leading indicators of expected post-transposition law — they are not yet directly enforceable in FI or DE national courts, but FI and DE courts already apply similar logic through existing case law (see Steps 3–4). Flag this in any written analysis.

Five indicators. Count how many are present:

| Indicator | Present? |
|---|---|
| (1) Remuneration set or capped by platform/company | [Y/N/Partial] |
| (2) Work performance supervised electronically (real-time tracking, rating systems, algorithmic management) | [Y/N/Partial] |
| (3) Instructions on conduct, appearance, or how to perform the work | [Y/N/Partial] |
| (4) No freedom to build own client base, work for third parties, or subcontract | [Y/N/Partial] |
| (5) No freedom to organise own working time or accept/reject tasks | [Y/N/Partial] |

**Result:**
- **2 or more indicators present** → rebuttable presumption of employment relationship. Employer must rebut presumption (burden is reversed). Flag as 🔴 High risk if presumption applies.
- **1 indicator** → no presumption, but note the indicator(s) present.
- **0 indicators** → Platform Work Directive presumption does not apply.

Note: even if the worker is not on a "platform", courts in FI and DE may apply similar logic (economic dependency, integration). Apply the indicators as a checklist regardless.

---

## Step 3: Apply Finnish test (TSL §1)

Call `mcp__velvoite__get_finnish_statute("TSL", "1:1")` for the statutory employment relationship definition. Present the three-element test from the live statute text.

**Employment relationship exists under Työsopimuslaki if ALL THREE elements are present:**

| Element | Analysis |
|---|---|
| (1) Work performed for the employer | [describe: is output for employer's benefit?] |
| (2) Under employer's direction and supervision (johto ja valvonta) | [describe: does employer direct how/when work is done?] |
| (3) For remuneration | [describe: is payment for the work, not for a result?] |

Finnish courts also weigh:
- **Economic dependency**: >70% income from one client → strong indicator
- **Integration into organisation**: company email, access to systems, participates in company meetings
- **Tools and equipment**: company-provided → indicator of employment
- **Exclusivity or practical exclusivity**: cannot work for others in practice

**Conclusion (Finland):** Employee / Likely employee / Likely contractor / Contractor — with confidence level.

---

## Step 4: Apply German test (§611a BGB)

**Employee is personally dependent (persönliche Abhängigkeit):**

| Factor | Analysis |
|---|---|
| Follows instructions (weisungsgebunden) — on time, place, content | [Y/N/Partial] |
| Integrated into company organisation (eingliederung) — fixed schedule, company hierarchy | [Y/N/Partial] |
| No entrepreneurial risk — paid regardless of business outcome | [Y/N/Partial] |
| No own client base — works exclusively or predominantly for this one company | [Y/N/Partial] |

If the formal contract says "contractor" but the factual conduct shows the above, German courts treat the relationship as employment regardless of label. This is *faktisches Arbeitsverhältnis* — a de facto employment relationship.

**KSchG note:** If `de_kschg_applies: true` from profile and this worker would be classified as employee, KSchG dismissal protection applies after 6 months.

**Conclusion (Germany):** Employee / Likely employee / Likely contractor / Contractor — with confidence level.

---

## Step 5: Overall risk assessment

Synthesise across all applicable tests:

| Test | Conclusion | Risk |
|---|---|---|
| Platform Work Directive | [Employee presumption / No presumption] | [🔴/🟡/🟢] |
| Finland (TSL) | [if FI applicable] | [🔴/🟡/🟢] |
| Germany (§611a BGB) | [if DE applicable] | [🔴/🟡/🟢] |

**Overall risk:**
- 🔴 **High** — presumption of employment applies OR two or more tests conclude "employee" or "likely employee". Recommend converting to employment contract before engaging or continuing.
- 🟡 **Medium** — one test concludes "likely employee" or indicators are mixed. Legal review required before relying on contractor status.
- 🟢 **Low** — all applicable tests conclude "contractor" with confidence. Document the analysis.

---

## Step 6: Recommended action

Based on risk level:

**🔴 High:**
> "Based on this analysis, there is a significant risk that this arrangement will be treated as an employment relationship — potentially with retroactive effect. Consequences include back social contributions (pension, unemployment, health insurance), income tax liability for the company, and the full suite of employment rights (notice periods, protection against dismissal, leave entitlements). We strongly recommend: (1) do not start or continue this arrangement as a contractor relationship; (2) either convert to employment or fundamentally restructure the arrangement so the worker has genuine independence; (3) obtain advice from an employment lawyer before proceeding."

**🟡 Medium:**
> "The classification is uncertain. The arrangement has characteristics of both employment and contracting. Before relying on contractor status: obtain a written legal opinion from an employment lawyer familiar with [jurisdiction]; document the independence factors (multiple clients, own tools, right to subcontract, no exclusivity); review any existing contract to ensure it reflects actual practice."

**🟢 Low:**
> "The arrangement appears consistent with independent contracting under the applicable tests. Document this analysis. Review annually or whenever the arrangement materially changes — classification can shift if the company increases control or the worker's economic dependency increases."

---

## Guardrail

> **RESEARCH NOTES — NOT LEGAL ADVICE.** Worker classification has significant tax, social security, and employment law consequences. This analysis applies legal tests to the facts as described — it is a working document for attorney review, not a classification opinion. A qualified employment lawyer in the relevant jurisdiction must review before you rely on contractor status or convert an existing arrangement. Misclassification can result in back payments of social contributions, income tax liability, and retroactive employment rights. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.