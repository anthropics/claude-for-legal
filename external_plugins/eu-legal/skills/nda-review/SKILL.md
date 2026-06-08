---
name: nda-review
description: >
  Dedicated EU-law NDA review — deeper than contract-review for NDAs. Applies
  EU Trade Secrets Directive 2016/943 framing, detects mutual vs. one-way, checks
  standard confidentiality provisions, and flags governing law deviations. Also
  loaded by /eu-legal:contract-review when an NDA is detected. Use when the user
  says "review this NDA", "check this confidentiality agreement", "is this NDA
  okay", or attaches an inbound NDA.
argument-hint: "[file path | Drive link | paste text]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:nda-review

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If missing or has `[PLACEHOLDER]`, stop: "Run `/eu-legal:cold-start-interview` first."
2. Load `~/.claude/plugins/config/eu-legal/commercial.md`. If missing or has `[PLACEHOLDER]`, stop: "Run `/eu-legal:commercial-cold-start` first."
3. Get the NDA (file path, Drive link, or pasted text). If none, ask.
4. Run the workflow below.

---

## Purpose

Most inbound NDAs are fine. A few have landmines. This skill sorts them quickly so legal only reads the ones that matter — using EU Trade Secrets Directive framing rather than US common law analysis.

**This is a draft for attorney review and does not constitute legal advice.**

---

## EU legal framework

This skill applies:
- **Directive (EU) 2016/943** on the protection of undisclosed know-how and business information (Trade Secrets Directive) — definition of trade secret (Art. 2(1)), unlawful acquisition (Art. 4(2)), unlawful use and disclosure (Art. 4(3)), lawful acquisition (Art. 3).
- **National implementing legislation:** Liikesalaisuuslaki 595/2018 (Finland); GeschGehG — Geschäftsgeheimnisgesetz (Germany); Wet bescherming bedrijfsgeheimen (Netherlands). Note the applicable national law based on governing law in `commercial.md`. `[model knowledge — verify]`
- **GDPR (Regulation (EU) 2016/679):** If the NDA involves disclosure of personal data or employee information, flag that the NDA does not substitute for GDPR compliance — personal data shared under confidentiality is still subject to data subject rights.

Do NOT apply US common law trade secrets analysis (Uniform Trade Secrets Act, Defend Trade Secrets Act). If the NDA uses US common law language, flag it and propose EU TSD framing as a replacement.

---

## Step 1: Orientation

Before triaging, answer:

| Question | Answer |
|---|---|
| Mutual or one-way? | |
| Whose paper is it? | |
| Which side are we? | |
| Purpose of disclosure | |
| Governing law | |
| Duration | |
| Contemplated transaction | |

**One-way NDA check:** If the NDA is one-way (only one party discloses), do not auto-flag RED. Ask:
> "Is your organisation the only party disclosing information, or should this be mutual? A one-way NDA is appropriate when only one side shares — for example, sharing your technology with a vendor who shares nothing back."
Use the answer plus the `commercial.md` playbook to determine the bucket.

---

## Step 2: Scope check

**Before reviewing NDA-specific provisions, check whether the document is doing more than its name suggests.** NDAs can hide: standstills, licensing grants, exclusivity, non-solicits, non-competes, IP assignments, right of first refusal, MFN clauses, arbitration provisions that govern far more than confidentiality disputes.

If the NDA contains obligations beyond confidentiality: **auto-YELLOW regardless of NDA-term analysis.** Flag:
> "This document is labelled an NDA but contains [provision]. It is more than an NDA. Route for attorney review."

---

## Step 3: Triage

Classify into GREEN / YELLOW / RED using `commercial.md` NDA triage positions.

**GREEN — route to signature**

The NDA satisfies every position in `commercial.md`, no term triggers a RED flag, and the playbook has attorney-reviewed NDA positions. GREEN cannot be issued against missing or `[PLACEHOLDER]` positions.

**YELLOW — needs a lawyer's eyes on specific items**

One or more terms deviate from the playbook but are not categorical deal-breakers, OR a term appears that `commercial.md` doesn't address.

**RED — stop, talk to legal first**

The NDA hits a "never accept" position in `commercial.md`, or a term is incompatible with the company's standard posture.

---

## Step 4: Detailed checks

For each check, apply the position from `commercial.md`. If the playbook is silent on a term, ask the user and offer to record the answer.

### Definition of Confidential Information (EU TSD framing)

Check against Art. 2(1) TSD three-limb test:
1. The information is secret (not generally known or readily accessible in the relevant circles)
2. The information has commercial value because of its secrecy
3. Reasonable steps have been taken to keep it secret

Flag if the definition is either too narrow (excludes orally disclosed information without confirmation window) or too broad (captures publicly available information). Flag any US common law language ("misappropriation", "improper means") and propose:
> "Replace with EU TSD Art. 2(1) definition: 'information that (a) is secret in the sense that it is not, as a body or in the precise configuration and assembly of its components, generally known among or readily accessible to persons within the circles that normally deal with the kind of information in question; (b) has commercial value because it is secret; and (c) has been subject to reasonable steps under the circumstances, by the person lawfully in control of the information, to keep it secret.' `[Directive (EU) 2016/943 Art. 2(1) — model knowledge — verify]`"

### Standard carve-outs (Art. 3 TSD — lawful acquisition)

The five standard carve-outs that align with Directive Art. 3 (lawful acquisition of trade secrets):
1. Information that is or becomes public other than through breach
2. Information the receiving party already had before disclosure
3. Information independently developed without reference to the disclosed information (Art. 3(1)(b) TSD)
4. Information received from a third party without restriction (Art. 3(1)(c) TSD)
5. Information required to be disclosed by law or court order (with notice to discloser where legally permitted)

Flag missing carve-outs. Flag if carve-out (3) uses US language ("developed without use of confidential information") rather than EU TSD framing ("independent discovery or creation" per Art. 3(1)(b)).

### Unlawful acquisition, use, and disclosure (Arts. 4(2) and 4(3) TSD)

Check that the prohibited activities section aligns with TSD Art. 4 rather than US UTSA / DTSA language. The TSD frames unlawful use and disclosure as: use or disclosure by a person who acquired the trade secret unlawfully, or who obtained it in breach of a confidentiality or limited use obligation.

If the NDA uses "improper means" (UTSA language) without a TSD equivalent, flag it.

### Duration and survival

Check: initial term, post-term survival of confidentiality obligations, whether trade secrets are carved out with longer / indefinite protection.

Note: Under TSD Art. 10(2), courts may set a limited period for confidentiality injunctions where the secret has ceased to be a trade secret. Perpetual NDAs are enforceable in the EU but courts may interpret them narrowly for information that becomes public.

Apply the duration position from `commercial.md`. Flag if outside the playbook range.

### Residuals clause

A residuals clause allows the receiving party to use information retained in unaided human memory. Flag if present; apply `commercial.md` position. If `commercial.md` is silent: ask. "A residuals clause is present in Section [X]. Should this be GREEN (acceptable), YELLOW (negotiable), or RED (never accept) for your organisation? I'll record your answer."

### Return or destruction on termination

Check: is there an obligation to return or destroy confidential information on termination? Is there a carve-out for backup / archival copies and legal holds?

EU data protection note: if confidential information includes personal data, return/destruction must also comply with GDPR Art. 17 (right to erasure) and any applicable retention obligations. Flag if no alignment.

### Governing law

Compare to `commercial.md` governing law preference.
- If EU governing law: note the applicable national TSD implementation.
- If Finnish law: Call `mcp__velvoite__get_finnish_statute("LSL", "2")` for the current Finnish trade secret definition. Present the three-element definition from the live statute text. "Liikesalaisuuslaki (Business Secrets Act 595/2018) implements Directive 2016/943 in Finland. Art. 4 of the Act defines trade secrets; §§ 4–7 define unlawful acquisition, use, and disclosure. `[model knowledge — verify]`"
  Then call `mcp__velvoite__search_cjeu_cases("trade secret", "Directive 2016/943")` to surface any CJEU judgments interpreting the Trade Secrets Directive. Fetch the URL for any relevant case. If found, note: "CJEU [celex]: [one-line holding on what the court required]." If none found, omit.
- If German law: "GeschGehG (Gesetz zum Schutz von Geschäftsgeheimnissen, 2019) implements Directive 2016/943 in Germany. `[model knowledge — verify]`"
- If outside EU: 🟠 flag. "Governing law is [jurisdiction]. Your playbook prefers EU law. TSD protections may not apply. `[review]`"

### Restrictive covenants

Check for non-solicits, non-competes, exclusivity. Flag any covenants that go beyond confidentiality — these auto-YELLOW the NDA regardless of other terms.

---

## Step 5: Redline granularity

Edit at the smallest possible granularity — replace a word before a phrase, a phrase before a sentence. Only replace a whole clause when surgical edits would be harder to read than a fresh draft.

---

## Output

```
CONFIDENTIAL — INTERNAL LEGAL ANALYSIS — DRAFT FOR ATTORNEY REVIEW

## NDA Triage: [Counterparty]

[GREEN — route to signature | YELLOW — flag for [approver] | RED — stop, talk to legal first]

### Executive Summary

[For GREEN: "No red flags identified under the playbook and EU TSD framework. Route for signature per standard process."]
[For YELLOW/RED: bullet list of specific actionable items]

### Flagged items (YELLOW/RED only)

**1. [Issue]** — Section [X]
   What: [one line]
   Why flagged: [playbook position or "playbook is silent on this"]
   Legal risk: 🔴/🟠/🟡/🟢 | Business friction: 🔴/🟠/🟡/🟢
   Proposed redline: "[specific language]"

[repeat for each flag]

### Everything else

| Check | Status | Framework |
|---|---|---|
| Mutual / one-way | [pass/flag] | commercial.md position |
| CI definition (TSD Art. 2(1)) | [pass/flag] | Directive 2016/943 |
| Standard carve-outs (TSD Art. 3) | [pass/flag] | Directive 2016/943 |
| Unlawful use / disclosure (TSD Art. 4) | [pass/flag] | Directive 2016/943 |
| Duration and survival | [pass/flag] | commercial.md position |
| Residuals | [pass/flag] | commercial.md position |
| Return / destruction | [pass/flag] | commercial.md position |
| Governing law | [pass/flag] | commercial.md preference |
| Restrictive covenants | [pass/flag] | commercial.md / auto-YELLOW |
```

**Guardrail:** Append to every output — "This analysis is a draft for attorney review and does not constitute legal advice."

---

## Close with next-steps decision tree

> **What next?**
> 1. **Route for signature** — if GREEN, confirm the approval process
> 2. **Escalate** — I'll draft a note to [approver] with the flagged items
> 3. **Redline and return** — I'll produce specific redline language for each flagged item
> 4. **Use our paper instead** — recommend if counterparty is a startup or small vendor
> 5. **Something else**

---

## Disclaimer

Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
