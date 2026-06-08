---
name: startup-nda
description: >
  NDA review and generation for Finnish startups — three scenarios (investor,
  partner/integration, M&A due diligence), mutual vs one-way, EU Trade Secrets
  Directive (Liikesalaisuuslaki 595/2018) framing, AI product definition
  expansions. Use when reviewing or drafting an NDA, asking "is this NDA okay",
  "NDA with investor", "NDA with partner", "M&A NDA".
argument-hint: "[paste NDA text or describe: who is the counterparty and what is the purpose?]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /fi-startup-legal:startup-nda

1. Load `~/.claude/plugins/config/fi-startup-legal/CLAUDE.md`. Extract: `bf_grants_active`, `ai_product`, `stage`. If placeholders, stop: run `/fi-startup-legal:startup-cold-start` first.
2. Call `mcp__velvoite__get_finnish_statute("LSL", "2")` — fetch live trade secret definition. If unavailable: note `[LSL §2 definition not fetched — verify current text at finlex.fi]` and proceed.
3. Detect scenario from user input (see table below). Confirm before proceeding.
4. Detect mode: **draft** (user wants an NDA generated) or **review** (user has an NDA to check).
5. Apply profile adaptations (AI definition expansion, BF advisory note) if flags are set.
6. Execute: draft from scaffold OR review against checklist.

---

## Confidence

- **High (proceed and flag):** Clause clearly matches or clearly deviates from the checklist — state the finding plainly.
- **Medium (surface with note):** Clause is ambiguous, non-standard, or sits between scenarios — flag with `[review]` and explain the ambiguity in one sentence.
- **Low (halt and ask):** Clause type not covered by this skill's checklists, the scenario doesn't fit A/B/C, or the NDA structure is significantly non-standard — stop, explain what's outside scope, and ask before proceeding.

---

## Scenario detection

| User input signals | Scenario |
|---|---|
| "investor", "VC", "angel", "fund", "fundraising", "pitch" | A — Investor |
| "partner", "integration", "API", "vendor", "supplier", "co-development", "co-marketing" | B — Partner/Integration |
| "acquisition", "M&A", "due diligence", "data room", "acquirer", "merger" | C — M&A |
| Ambiguous | Ask explicitly |

Confirm detected scenario before drafting or reviewing. Example: *"This looks like a Partner/Integration NDA — is that right, or is this a different context?"*

---

## Pre-flight escalation

Before drafting or reviewing, flag and confirm if any of the following apply:

| Signal | Action |
|---|---|
| Counterparty is non-Finnish (US, UK, non-EU) | Flag: governing-law section may not apply — confirm whether to proceed under Finnish framing or surface the gap for counsel |
| Inbound NDA already has non-EU governing law | Do not silently apply Finnish-law checklist — surface the deviation and ask whether to proceed or route to counsel |
| NDA appears employment-linked (contractor NDAs, post-employment restrictions) | Route to `/fi-startup-legal:non-compete-check`; employment-adjacent obligations are outside this skill's scope |
| Four or more parties | Outside scope — route to Finnish counsel |
| Structure does not fit scenario A, B, or C | State what's non-standard and ask before proceeding |

---

## Profile adaptations

Apply when the relevant flag is set in the loaded profile.

### BF grant advisory (if `bf_grants_active: yes`)

BF grant restrictions govern **IP transfer**, not confidentiality — they do not
belong as a clause in the NDA. Instead, surface this note in your output:

> **Business Finland grant active:** BF grant IP restrictions are a separate
> matter from this NDA. Disclose them in the relevant commercial agreement
> (partnership agreement, SPA, or due diligence disclosure letter). Run
> `/fi-startup-legal:bf-grant-check` before signing any transaction involving
> BF-funded IP.

### AI product definition expansion (if `ai_product: yes`)

Add to the definition of Confidential Information in all scenarios:

> "Confidential Information includes, without limitation, model architecture,
> training data composition and sources, fine-tuning methodology, system prompts,
> evaluation benchmarks, API specifications, model weights, and inference
> infrastructure details."

---

## Scenario A — Investor / Fundraising NDA

**Context:** Startup sharing pitch materials, financials, cap table with a potential
investor pre-term sheet.
**Direction:** One-way (startup → investor). Mutual only if investor shares fund
strategy — rare.
**Typical length:** 1–2 pages.

> **Market note:** Finnish VCs and angels typically do not sign NDAs before a first
> meeting. If an investor declines, this is normal — not a red flag. For early-stage
> fundraising, consider whether requiring an NDA creates more friction than protection.

### Review checklist

| Clause | Finnish market standard | Flag if |
|---|---|---|
| Direction | One-way (startup discloses) | Mutual without clear reason |
| Definition scope | Pitch deck, financials, cap table, tech overview | Overly broad or includes public info |
| No-use obligation | Investor may not use info to compete or advise competitors | Missing entirely |
| Exclusions | Public domain, prior knowledge, independent development, required disclosure | Missing any of the four |
| Duration | 1–2 years | >3 years or <1 year |
| Return/deletion | On request or deal termination | Missing |
| Governing law | Finnish law, Helsinki District Court | Non-EU governing law |

### Draft scaffold

> ⚠️ **Draft only — not legal advice. Have a Finnish startup lawyer review before signing.**

When drafting, generate a complete agreement using this structure. Replace all
`[BRACKETED]` items with actual values from context. Apply AI expansion if
`ai_product: yes`.

```
NON-DISCLOSURE AGREEMENT

[STARTUP NAME] (Business ID: [Y-TUNNUS]) ("Disclosing Party")
[INVESTOR NAME / FUND NAME] ("Receiving Party")

1. CONFIDENTIAL INFORMATION
   Means all non-public information disclosed by Disclosing Party relating to
   its business, technology, financials, and cap table, whether disclosed orally
   or in writing. [AI EXPANSION IF ai_product: yes]
   Excludes: (a) public domain; (b) prior knowledge; (c) independent development;
   (d) required disclosure by law.

2. OBLIGATIONS
   Receiving Party shall: (a) keep Confidential Information strictly confidential;
   (b) not use it for any purpose other than evaluating a potential investment in
   Disclosing Party; (c) not disclose to third parties without prior written
   consent; (d) not use to compete with Disclosing Party or advise competitors.

3. DURATION
   [2] years from the date of this Agreement.

4. RETURN / DELETION
   Upon request or termination of investment discussions, promptly return or
   destroy all Confidential Information.

5. GOVERNING LAW
   Finnish law. Disputes: Helsinki District Court.

6. REMEDIES
   Disclosing Party is entitled to seek injunctive relief (LSL §8) and damages
   including unjust enrichment (LSL §11) for any breach.

Signed: _________________ Date: _____________
```

---

## Scenario B — Partner / Integration NDA

**Context:** Tech integration, API access, co-marketing, supplier relationship,
co-development. Both parties share material.
**Direction:** Mutual.
**Typical length:** 2–4 pages.

### Review checklist

| Clause | Finnish market standard | Flag if |
|---|---|---|
| Direction | Mutual | One-way without clear reason |
| Definition scope | Broad — tech, business plans, customer data, integration specs | Excludes technical information |
| Purpose limitation | Restricted to agreed partnership purpose only | Missing |
| IP ownership | Each party retains its own IP; NDA ≠ license | Missing or ambiguous |
| Sub-contractor disclosure | Permitted only with prior written consent + equivalent obligations | Permitted without restriction |
| Duration | 3–5 years; perpetual for trade secrets | <2 years |
| Survival | Obligations survive termination of the partnership agreement | Missing |
| Return/destruction | On termination or request, with written confirmation | Missing |
| Governing law | Finnish law, Helsinki District Court | Non-EU governing law |

### Draft scaffold

> ⚠️ **Draft only — not legal advice. Have a Finnish startup lawyer review before signing.**

When drafting, generate a complete agreement using this structure. Replace all
`[BRACKETED]` items with actual values from context. Apply AI expansion if
`ai_product: yes`.

```
MUTUAL NON-DISCLOSURE AGREEMENT

[PARTY A NAME] (Business ID: [Y-TUNNUS]) and
[PARTY B NAME] (Business ID/reg. no.: [X])
(each a "Party", together the "Parties")

1. CONFIDENTIAL INFORMATION
   Means all non-public information disclosed by either Party relating to its
   business, technology, products, customers, and operations.
   [AI EXPANSION IF ai_product: yes]
   Excludes: (a) public domain; (b) prior knowledge; (c) independent development;
   (d) required disclosure by law or authority.

2. PURPOSE
   Confidential Information may only be used for [DESCRIBE PURPOSE: e.g.
   evaluating and implementing a technical integration between Party A's [X]
   and Party B's [Y]].

3. OBLIGATIONS
   Each Party shall: (a) keep Confidential Information strictly confidential;
   (b) use it only for the Purpose; (c) restrict access to employees and
   contractors with need to know, bound by equivalent obligations.

4. IP OWNERSHIP
   This Agreement does not transfer any IP rights. Each Party retains full
   ownership of its own IP. Disclosure does not constitute a license.

5. SUB-CONTRACTORS
   Disclosure to sub-contractors requires prior written consent and execution
   of equivalent confidentiality obligations.

6. DURATION
   [3] years from the date of this Agreement. Trade secret obligations (LSL §2)
   survive indefinitely. Obligations survive termination of the Parties'
   cooperation.

7. RETURN / DESTRUCTION
   On termination or request, return or destroy all Confidential Information
   and confirm in writing.

8. GOVERNING LAW
   Finnish law. Disputes: Helsinki District Court.

9. REMEDIES
   Each Party is entitled to seek injunctive relief (LSL §8) and damages
   including unjust enrichment (LSL §11) for breach.

Signed: _________________ Date: _____________
```

---

## Scenario C — M&A / Due Diligence NDA

**Context:** Potential acquisition, merger, or significant strategic investment
requiring full data room access.
**Direction:** Mutual but asymmetric — target discloses substantially more.
**Typical length:** 3–6 pages. Most formal; often negotiated clause by clause.

### Review checklist

| Clause | Finnish market standard | Flag if |
|---|---|---|
| Direction | Mutual (asymmetric in practice) | One-way only |
| Process confidentiality | Existence of discussions is itself confidential | Missing |
| Definition scope | Broadest — all data room materials, employee info, contracts, IP | Any carve-out of technical IP |
| Purpose limitation | Evaluation of transaction only | Missing |
| Standstill | Acquirer may not poach employees or customers during process | Missing |
| Non-solicitation | 12–24 months post-termination of discussions | <12 months |
| Permitted disclosure | Advisors on need-to-know + bound by equivalent obligations | Unrestricted advisor disclosure |
| Destruction/return | With written certification | No certification requirement |
| Duration | 2–3 years | <2 years |
| Survival | Obligations survive termination of discussions | Missing |
| Governing law | Finnish law, Helsinki District Court or FAI arbitration | Non-EU governing law |
| Remedies | Explicit injunction + damages language | Missing |

### Draft scaffold

> ⚠️ **Draft only — not legal advice. Have a Finnish startup lawyer review before signing.**

When drafting, generate a complete agreement using this structure. Replace all
`[BRACKETED]` items with actual values from context. Apply AI expansion if
`ai_product: yes`.

```
NON-DISCLOSURE AND STANDSTILL AGREEMENT

[TARGET NAME] (Business ID: [Y-TUNNUS]) ("Target")
[ACQUIRER / INVESTOR NAME] (Business ID/reg. no.: [X]) ("Recipient")

1. CONFIDENTIAL INFORMATION
   Means all non-public information disclosed by Target in connection with
   Recipient's evaluation of a potential transaction (the "Transaction"),
   including all data room materials, financial records, contracts, employee
   information, and IP documentation.
   [AI EXPANSION IF ai_product: yes]
   Excludes: (a) public domain; (b) prior knowledge; (c) independent development;
   (d) required disclosure by law, with prior written notice to Target.

2. PROCESS CONFIDENTIALITY
   The existence of discussions, terms of this Agreement, and fact that
   information has been disclosed are themselves Confidential Information.

3. PURPOSE
   Confidential Information may only be used to evaluate the Transaction.

4. OBLIGATIONS
   Recipient shall: (a) keep all Confidential Information strictly confidential;
   (b) use it solely to evaluate the Transaction; (c) restrict access to advisors
   (legal, financial, technical) on strict need-to-know, bound by equivalent
   obligations; (d) not use to compete with Target or approach Target's customers,
   partners, or employees.

5. STANDSTILL
   During discussions and for [12] months following termination, Recipient shall
   not: (a) solicit or hire any employee of Target identified through the process;
   (b) approach Target's customers or partners identified through disclosed materials.

6. RETURN / DESTRUCTION
   If the Transaction does not proceed, within [10] business days return or destroy
   all Confidential Information and provide written certification of destruction.

7. DURATION
   [3] years from the date of this Agreement. Trade secret obligations (LSL §2)
   survive indefinitely.

8. GOVERNING LAW
   Finnish law. Disputes: Helsinki District Court [or FAI arbitration — delete
   as applicable].

9. REMEDIES
   Target is entitled to seek immediate injunctive relief without bond (LSL §8)
   and full damages including unjust enrichment (LSL §11). Recipient acknowledges
   that breach would cause irreparable harm for which monetary damages are inadequate.

Signed: _________________ Date: _____________
```

---

## What this skill does NOT do

- **Cross-border governing law:** Does not advise on NDA terms when a non-Finnish governing law is required. If the inbound NDA already sets non-Finnish governing law, this skill surfaces the issue and routes to counsel — it does not apply Finnish-law positions to a non-Finnish-law agreement.
- **Employment-linked NDAs:** Post-employment NDAs, contractor confidentiality agreements, and non-solicitation clauses in employment contexts are governed by TSL §3:5 and are outside this skill's scope. Use `/fi-startup-legal:non-compete-check`.
- **Multi-party NDAs:** Covers bilateral agreements only. Three or more parties require a different structure; route to Finnish counsel.
- **Ongoing monitoring:** Does not track whether NDA obligations are being met or when the term expires.
- **Legal advice:** Generates drafts and review checklists — not legal advice. A Finnish startup lawyer should review before signing.

---

## Guardrail

NDAs are enforceable contracts. Have a Finnish startup lawyer review before signing — not just for M&A and core trade secrets, but any NDA where a breach would materially harm the company. Recommended firms: Nordic Law, Dottir, Lexia Growth, Fondia. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
