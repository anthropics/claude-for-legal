---
name: belgian-corporate-law
description: >
  Belgian entity formation and vehicle selection — choose the right Belgian
  company form for a new venture and produce the incorporation checklist, under
  the 2019 Code of Companies and Associations (CCA / Dutch "WVV" / French
  "CSA"). Produces a vehicle-recommendation memo comparing BV/SRL, NV/SA, CV/SC,
  the partnership forms, and a foreign-company branch, plus a step-by-step
  incorporation checklist (financial plan, notarial deed, capital/contributions,
  Crossroads Bank registration, UBO register, Belgian Official Gazette
  publication). Use when the user says "incorporate in Belgium", "set up a
  Belgian company", "BV or NV", "BV/SRL", "NV/SA", "which company form in
  Belgium", "Belgian subsidiary", "branch vs subsidiary in Belgium", or asks how
  to form a Belgian legal entity. Does NOT do tax structuring, draft the
  articles of association, or cover non-profits (ASBL/VZW) or foundations.
argument-hint: "[--compare | --checklist] [venture facts]"
version: 1.0.0
---

# /belgian-corporate-law

1. Load `~/.claude/plugins/config/claude-for-legal/corporate-legal/CLAUDE.md` → `## Company profile`, `## Who's using this`. The profile supplies the work-product header, the non-lawyer gate, and any standing escalation contact.
2. Route by flag:
   - No flag: full flow — intake (Step 1) → escalation screen (Step 2) → vehicle match (Steps 3–4) → incorporation checklist (Step 5) → recommendation memo.
   - `--compare`: produce the Step 3 vehicle comparison only, skip the intake and the memo.
   - `--checklist`: the form is already chosen — confirm it, then produce the Step 5 incorporation checklist only.
3. Apply the corporate-legal plugin guardrails throughout — `## Shared guardrails`, `## Jurisdiction recognition`, the reviewer note and decision-tree formats in `## Outputs`. This skill does not restate them; the plugin CLAUDE.md controls.

---

## Purpose

Belgium's 2019 Code of Companies and Associations cut the company menu from roughly seventeen forms to a handful, abolished minimum capital for the private limited company, and traded it for a stricter financial-plan-and-founders'-liability regime. The result: vehicle selection is no longer "pick the BVBA by default." It is a real decision with personal-liability consequences for the founders.

This skill runs that decision once, cleanly. It takes the venture's facts, screens for the situations a corporate generalist should not resolve alone, recommends a form with its reasoning visible, and hands the lawyer a memo and an incorporation checklist. The Belgian notary still drafts the deed and verifies legality — this skill prepares the instruction, it does not replace the notary.

## Jurisdiction and currency

This skill covers **Belgian** for-profit company law under the **Code of Companies and Associations** (CCA) — Dutch *Wetboek van vennootschappen en verenigingen* (WVV), French *Code des sociétés et des associations* (CSA) — in force since 1 May 2019 and mandatory for all companies since 1 January 2024 `[verify — CCA]`.

The CCA is amended periodically and figures move. Before relying on any capital figure, deadline, or liability rule in this skill: confirm it against the current consolidated CCA on the Belgian official sources, or have Belgian counsel or the instrumenting notary confirm it. Every hard rule below is tagged `[verify — CCA]`; treat the tag as an instruction, not decoration. If a research connector is available, run a currency check per the plugin's currency trigger. This skill does **not** bundle a reference table precisely so that it cannot ship stale law — the current statute is the authority.

## Audience and delegation

**For:** a corporate lawyer (in-house or in practice) advising a founder or a group on forming a Belgian entity, or a non-lawyer founder working with an attorney. Belgian-qualified counsel is assumed to be reachable for the calls this skill escalates.

**Delegation line.** Claude drafts a recommendation and a checklist. The choice of vehicle, the financial plan, the articles of association, and the notarial deed are the lawyer's and the notary's. The recommendation memo is structured as a decision surface — a ranked comparison with the reasoning exposed — never as a settled answer. Where the call turns on tax, cross-border structuring, or a regulated activity, the skill stops and routes (Step 2).

---

## Step 1: Intake — the facts that drive vehicle choice

Collect the following before recommending anything. If an item is missing, **ask for it** — do not assume a default and do not proceed silently on a guess. If the user cannot answer an item, record it as `unknown` and treat it as a confidence-lowering gap in Step 4.

1. **Founders** — how many; natural persons or legal entities; are all of them Belgian residents? (Non-resident founders → Step 2 cross-border trigger.)
2. **Liability appetite** — do the founders need their personal assets shielded from business debts, or is unlimited liability acceptable?
3. **Capital available at start** — how much equity will actually be contributed, in cash and in kind. (Contributions in kind → Step 2 trigger — a registered-auditor report applies.)
4. **Funding intent** — bootstrapped, or will the company raise external investment / issue multiple share classes / aim at a listing?
5. **Activity** — what the company will do, in one or two sentences. Flag whether it is a **regulated activity** (financial services, insurance, healthcare, transport, security, etc.) → Step 2 trigger.
6. **Governance preference** — single decision-maker or a board; any intent to separate management from supervision.
7. **Existing group** — is there a parent company (Belgian or foreign)? If a foreign parent, a Belgian **branch** is an alternative to a subsidiary — keep both on the table for Step 3.
8. **Horizon** — is this a long-term operating company, a holding vehicle, or a short-life special-purpose entity?

For `--checklist` runs, instead confirm: the chosen form, the founders, the registered-office address in Belgium, and whether contributions include anything other than cash.

---

## Step 2: Escalation screen — stop before recommending if any trigger fires

This skill handles a standard Belgian incorporation. The following take the decision outside a corporate generalist's lane. If any fires, **say so plainly, name what is needed, and route** — do not push past it with a confident answer (plugin `## Jurisdiction recognition`, point 5).

| Trigger | Why it escalates | Route to |
|---|---|---|
| **Regulated activity** | Licensing / authorisation can dictate or constrain the legal form and capital before company law does. | Sector regulator + specialist counsel |
| **Non-resident founders or cross-border management** | Tax residence, the place of effective management, and substance questions interact with the CCA's statutory-seat rule. | Belgian tax counsel + the home-jurisdiction adviser |
| **Tax-driven structuring** | Holding/IP/financing structures, participation-exemption planning, and management-company set-ups are tax-led, not company-law-led. | Belgian tax adviser |
| **Listing ambition or a complex investor round** | Share classes, governance, and form interact with capital-markets and VC-deal requirements. | Capital-markets / VC counsel |
| **Non-profit purpose** (ASBL/VZW, AISBL, foundation) | A different Book of the CCA governs associations and foundations — out of this skill's scope entirely. | Association/foundation specialist |
| **Contributions in kind** | A registered auditor's valuation report is required; valuation is not a company-law drafting task. | Registered auditor (*bedrijfsrevisor / réviseur*) |
| **Distress, insolvency, or restructuring context** | Forming an entity near insolvency raises avoidance and liability questions. | Insolvency counsel |

Escalating does not mean abandoning the user. Produce the partial analysis you safely can, mark every escalation-dependent conclusion `[review — escalated]`, and give the user the specific question to put to the specialist.

---

## Step 3: The vehicle menu (2019 CCA)

The for-profit forms a standard venture chooses among. Every capital figure and hard rule is `[verify — CCA]` — confirm against the current statute.

| Form (NL / FR) | Legal personality | Member liability | Minimum capital | Incorporation deed | Typical fit |
|---|---|---|---|---|---|
| **BV / SRL** — *besloten vennootschap / société à responsabilité limitée* | Yes | Limited to the contribution | **None** — abolished; replaced by a "sufficient initial equity" requirement `[verify — CCA]` | Notarial deed required `[verify — CCA]` | The default for SMEs, startups, holding and operating companies. Flexible: one or more shareholders, multiple share/voting classes, freely organised share-transfer rules. |
| **NV / SA** — *naamloze vennootschap / société anonyme* | Yes | Limited to the contribution | **€61,500**, fully subscribed `[verify — CCA]` | Notarial deed required `[verify — CCA]` | Larger companies, capital-intensive ventures, listing candidates. Permits a sole shareholder and a sole director; supports a one-tier or two-tier board. |
| **CV / SC** — *coöperatieve vennootschap / société coopérative* | Yes | Limited to the contribution | None `[verify — CCA]` | Notarial deed required `[verify — CCA]` | Reserved for ventures with a **genuine cooperative purpose** — the CCA narrowed this form; do not use it as a generic limited-liability vehicle. |
| **VOF / SNC** — *vennootschap onder firma / société en nom collectif* | Yes | **Unlimited, joint and several** | None | Private deed permitted `[verify — CCA]` | Partners who accept full liability and want simplicity; professional partnerships. |
| **CommV / SComm** — *commanditaire vennootschap / société en commandite* | Yes | Active partners unlimited; limited partners up to their contribution | None | Private deed permitted `[verify — CCA]` | A managing partner plus passive investors. |
| **Maatschap / société simple** | **No legal personality** | Unlimited | None | Private deed | Joint ventures, cost-sharing, simple holding of assets. Cannot itself contract or own as a person. |
| **Belgian branch** of a foreign company (*bijkantoor / succursale*) | No — extension of the foreign company | The foreign company is fully liable | n/a | Foreign-company resolution + Belgian filings | A foreign parent wanting a Belgian presence without a separate legal person. |

Notes that change the choice:

- The old **BVBA/SPRL** is now the **BV/SRL** — same family, but the no-minimum-capital and financial-plan regime is new. The partnership-limited-by-shares (**Comm.VA / SCA**) was **abolished** by the CCA `[verify — CCA]`; do not recommend it.
- **"No minimum capital" is not "no discipline."** The BV requires *sufficient initial equity* for the planned activity, evidenced by the financial plan. If the company goes bankrupt within three years of incorporation and the initial equity was manifestly insufficient for the planned activity, the **founders can be held personally liable** `[verify — CCA]`. The capital requirement did not disappear — it became a judgment call the founders own.
- **Branch vs subsidiary** is a genuine fork when there is a foreign parent. A subsidiary (usually a BV) is a separate legal person with its own limited liability; a branch is not — the foreign company carries the branch's liabilities, though both still trigger Belgian registration, accounting, and tax-filing duties. The choice is usually tax- and liability-led → pair this with the Step 2 cross-border and tax routes.

## Step 4: Match facts to vehicle

Apply the intake to the menu. State the recommendation **with the reasoning visible** and a confidence band (see `## Confidence bands`). Do not collapse it to a one-word answer — give the runner-up and why it lost.

Decision logic, in order:

1. **Limited liability needed?** If yes, the realistic set is BV/SRL, NV/SA, or (genuine cooperative only) CV/SC. If unlimited liability is acceptable and simplicity is valued, a partnership or the *maatschap* may fit.
2. **BV/SRL vs NV/SA.** Default to **BV/SRL** unless a concrete factor points to the NV: a listing ambition, a capital structure or governance model the NV serves better, or a counterparty/sector that expects an NV. The NV's €61,500 minimum capital `[verify — CCA]` is a cost the venture should be choosing on purpose, not defaulting into.
3. **Cooperative purpose?** Only recommend CV/SC if the venture is a real cooperative. If it is not, say so — the CCA does not allow the CV as a generic limited-liability shell.
4. **Foreign parent?** Put **branch vs Belgian subsidiary** explicitly to the user and flag that the resolution is tax- and liability-led (Step 2).
5. **Financial-plan reality check.** For any BV or NV, state plainly that the founders must prepare a robust financial plan and that thin initial equity against an ambitious activity creates founders'-liability exposure `[verify — CCA]`. If the Step 1 capital figure looks light for the described activity, flag it `[review]`.

If a Step 2 trigger fired, the recommendation is provisional — mark it `[review — escalated]` and name the specialist call it depends on.

## Step 5: Incorporation checklist

The path to a live Belgian company once the form is chosen. Items and order are `[verify — CCA]` against current practice; the instrumenting notary's checklist is authoritative for a capital company.

1. **Financial plan** (BV, NV, CV) — founders prepare a financial plan with the content the CCA prescribes; it is handed to the notary and retained. It is the evidentiary backbone of the founders'-liability test `[verify — CCA]`.
2. **Registered office** — a registered office address in Belgium.
3. **Capital / contributions** — cash contributions deposited to a blocked account with a bank certificate; **contributions in kind** require a registered-auditor report (Step 2). NV: confirm the subscription and paid-up rules `[verify — CCA]`.
4. **Articles of association** — drafted (by counsel / the notary — not this skill) and adopted in the deed.
5. **Incorporation deed** — BV, NV and CV are incorporated by **notarial deed** before a Belgian notary, who verifies legality `[verify — CCA]`. Partnerships (VOF, CommV) and the *maatschap* may be formed by private deed `[verify — CCA]`.
6. **Crossroads Bank for Enterprises (KBO / BCE)** — registration and allocation of the enterprise number; deposit of the deed at the registry of the competent Enterprise Court.
7. **Belgian Official Gazette** — publication of the incorporation in the *Belgisch Staatsblad / Moniteur belge*.
8. **UBO register** — file the ultimate-beneficial-owner information `[verify — CCA]`.
9. **VAT registration** — if the activity requires it, before activity starts.
10. **Ancillary set-up** — social-security affiliation for self-employed founders/directors, sector authorisations (from Step 2), accounting and bookkeeping arrangements, insurance. Flag these; they sit outside this skill's scope.

The notary typically coordinates items 5–8 for a capital company. The checklist is a brief for the notary and the registered agent, not a substitute for them.

### Consequential-action gate

Before the output is treated as a green light to incorporate, read `## Who's using this` in the corporate-legal practice profile. If the Role is **Non-lawyer**: incorporating a company, signing a notarial deed, and filing a financial plan create binding obligations and personal-liability exposure for the founders. State that the recommendation and checklist must be reviewed with a Belgian lawyer (*advocaat / avocat*) and the instrumenting notary before any step is taken, and give the user the brief to bring to them (the recommended form, the reasoning, the open Step 2 items, and the financial-plan exposure). Do not present the checklist as "ready to execute" past this gate without an explicit acknowledgement.

---

## Output format

Apply the work-product header and the `⚠️ Reviewer note` from the plugin `## Outputs` (with the EU jurisdiction note — Belgium is non-US, so US "attorney work product" protection does not attach). Then:

```
BELGIAN ENTITY — VEHICLE RECOMMENDATION
Venture: [one line]   |   Prepared: [date]

RECOMMENDED FORM: [BV/SRL | NV/SA | CV/SC | partnership | branch]
Confidence: [High | Medium | Low]

WHY THIS FORM
[2–4 sentences tying the Step 1 facts to the choice.]

RUNNER-UP: [form] — [one line on why it lost]

OPEN ITEMS BEFORE INCORPORATION
- [escalations from Step 2, each with the specialist to consult]
- [any `unknown` intake gap, and what to confirm]

INCORPORATION CHECKLIST
[the Step 5 list, tailored to the chosen form, with owner per item]

FINANCIAL-PLAN / FOUNDERS'-LIABILITY NOTE
[plain statement of the exposure — required for any BV or NV]
```

For `--compare`, output the Step 3 table plus the Step 4 decision logic, and stop. For `--checklist`, output the tailored Step 5 list plus the consequential-action gate, and stop.

If the comparison spans several forms with multiple attributes, offer the dashboard per the plugin `## Outputs` — do not build it unprompted.

## Worked example

**Input:** Two founders, both Belgian residents. ~€15,000 to contribute in cash. Building a B2B SaaS product; intend to raise a seed round in roughly 18 months. Want their personal assets protected. Not a regulated activity. No parent company.

**Output (abridged):**

> **RECOMMENDED FORM: BV/SRL** — Confidence: **High**
>
> **Why:** Limited liability is required, which rules out the partnerships and the *maatschap*. Between the two capital companies, the BV/SRL fits: no minimum capital `[verify — CCA]`, so the €15,000 is not measured against the NV's €61,500 floor `[verify — CCA]`; and the BV's freely structured share and voting classes accommodate the planned seed round without converting later. The NV's extra capital and formality buy nothing this venture needs yet.
>
> **Runner-up:** NV/SA — lost on cost and formality with no offsetting benefit at this stage.
>
> **Open items before incorporation:** Financial plan must be genuinely robust — a seed-stage SaaS plan on €15,000 of initial equity invites scrutiny under the founders'-liability test if the company fails within three years `[verify — CCA]` `[review]`. Seed-round share-class and cap-table design → corporate/VC counsel at raise time. Tax treatment of the structure → Belgian tax adviser.

The example shows the shape: a recommendation, the reasoning, the runner-up, and the flags handed back — not a bare answer.

## Confidence bands

- **High** — the facts point cleanly to one form (clear limited-liability need, no Step 2 trigger, capital comfortably consistent with the activity). Claude recommends and explains.
- **Medium** — the choice is defensible but turns on a factor the user should weigh (BV vs NV where a listing is a *maybe*; branch vs subsidiary). Claude recommends, states the dependency, and asks the user to confirm the assumption.
- **Low** — a Step 2 trigger fired, a key intake item is `unknown`, or the call is genuinely tax- or regulator-led. Claude names the uncertainty explicitly, gives only the analysis it can stand behind, and routes. It does **not** manufacture a confident recommendation to fill the gap.

A skill that sounds equally sure on a clean two-founder BV and a tax-driven cross-border holding is performing calibration, not doing it. Let the band move.

## Failure modes

- **Stale figures.** The €61,500 NV minimum, the financial-plan content, the founders'-liability window — all can change. Mitigation: every hard rule is `[verify — CCA]`; the skill bundles no reference table; the currency trigger applies.
- **Topic drift.** Users will ask adjacent questions (tax rates, drafting the articles, an ASBL/VZW). Mitigation: the Step 2 screen and the scope section below route these out instead of answering them badly.
- **Over-confidence on a "simple" incorporation that is not.** A regulated activity or a non-resident founder makes a routine-looking BV non-routine. Mitigation: the Step 2 screen runs *before* the recommendation.

Legal-specific failure modes:

- **Legal advice vs. legal support.** The output is a draft recommendation and a checklist — an input to the lawyer's and the notary's judgment, not advice and not a legal conclusion. The recommendation memo is a decision surface; the consequential-action gate stops a non-lawyer from treating it as a green light.
- **Privilege.** Belgium has no US-style work-product doctrine; an internal analysis is not shielded from a supervisory authority by a US-style header. The skill applies `PRIVILEGED & CONFIDENTIAL` with the EU jurisdiction note from the plugin `## Outputs` and never asserts protection that Belgian law does not give.
- **Accountability gap.** The lawyer chooses the form; the founders own the financial plan; the notary instruments and verifies the deed. The skill makes the reasoning visible specifically so the lawyer engages the judgment rather than ratifying a black-box answer.

## What this skill does NOT do

- **Tax.** No corporate-tax, VAT-planning, participation-exemption, or management-company analysis. Vehicle choice has tax consequences — those go to a Belgian tax adviser.
- **Draft the constitutional documents.** It does not write the articles of association or the notarial deed. A Belgian notary instruments the deed for a capital company; counsel drafts the articles.
- **Non-profits and foundations.** ASBL/VZW, AISBL, and foundations are governed by a different Book of the CCA — out of scope; route to a specialist.
- **Cross-border and EU forms.** No SE (Societas Europaea), cross-border merger, conversion, or seat-transfer analysis.
- **Regulated-sector licensing.** It flags that a licence may exist; it does not assess or obtain one.
- **Ongoing compliance.** Annual accounts filing with the National Bank, the annual general meeting, and recurring filings are the job of `/corporate-legal:entity-compliance` (capture the new entity there once formed), not this skill.
- **Substitute for Belgian counsel or the notary.** It prepares the decision and the brief; qualified Belgian professionals make and instrument it.

## Maintenance

First-party skill, owned by the corporate-legal plugin maintainers. The current version is in the frontmatter `version` field; bump it on every substantive change.

**Review cadence:** review at minimum **annually**, and additionally whenever the Code of Companies and Associations is amended — in particular changes to minimum-capital figures, the financial-plan regime, founders'-liability rules, the list of company forms, or the incorporation/registration procedure. On each review, re-confirm every `[verify — CCA]` item against the current consolidated statute and bump `version`.

**Communicating material changes:** a change to the escalation triggers (Step 2), the scope boundaries, the delegation line, or a recommended vehicle's eligibility is **material** — record it in the commit message and the plugin release notes so existing users see what moved, not merely that the file changed. Routine wording fixes do not need this.

Because the skill bundles no `references/` content, currency depends on this review cadence plus the per-run currency trigger.

## Relationship to other skills

- **`/corporate-legal:entity-compliance`** — handles recurring filing deadlines and good-standing tracking, US-centric by default. No trigger overlap: this skill fires on Belgian *formation* questions; entity-compliance fires on *ongoing* filing questions. Once a Belgian entity is formed, add it to that tracker as a custom jurisdiction.
- **`/corporate-legal:cold-start-interview`** — populates the practice profile this skill reads.

This skill does not overlap with or override any other corporate-legal skill.

## Close with the next-steps decision tree

End with the next-steps decision tree per the plugin `## Outputs`. Customise the branches to what was produced — typically: draft the notary instruction letter; draft the founders' financial-plan outline; get more facts on an `unknown` intake item; route a Step 2 escalation to the named specialist; or register the formed entity in `entity-compliance`. The lawyer picks; do not pick for them.
