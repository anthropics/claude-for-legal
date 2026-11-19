---
name: accredited-verification
description: >
  Walks a Rule 506(c) accredited investor verification file: the basis the
  investor claims, the evidence collected, how the evidence lines up against
  the current rule text and the firm's procedure, and a draft decision record
  for the principal to complete. Use when the user says "accredited
  verification", "506(c) verification", "verify this investor", "is this
  enough evidence of accredited status", "verification letter", or is
  assembling an investor's verification file before a subscription is accepted.
argument-hint: "[investor file path or reference] [--basis <claimed basis>]"
---

# /accredited-verification

1. Load `~/.claude/plugins/config/claude-for-legal/broker-dealer-legal/CLAUDE.md` → exemptions used, verification procedure, approvers.
2. Confirm the offering relies on Rule 506(c). If not, stop and route.
3. Record the claimed basis; fetch the current rule text; list the evidence; line it up; draft the decision record.
4. Output: evidence table, gaps, and a draft decision record with the decision left blank.

---

## Draft status

**This output is a draft for review by a registered principal and counsel. It is not legal advice.** It organizes a verification file. It is never a decision that an investor is accredited, that the steps taken were reasonable, or that a subscription may be accepted — those decisions belong to the firm (and, as the offering documents allocate it, the issuer). More generally it is never a decision on identification, accreditation, or suitability. Do not write "verified," "qualifies," "is accredited," or "meets the test." Write "the file contains," "the investor claims," "for the principal to decide."

## Purpose

A verification file fails in boring ways: the letter is from the wrong kind of professional, the statements are stale, the entity claims a basis that depends on its owners and nobody collected anything on the owners. This skill lays the file out so the principal sees basis, evidence, and gaps on one page and signs a decision record that says what was actually looked at.

## Inputs — ask for what's missing

- **Which exemption the offering relies on**, from the offering file or the firm profile. Ask; do not infer from the marketing.
- **Who is responsible for verification** in this offering (issuer, firm, a third-party service) per the offering documents and the firm's procedure.
- **The investor:** natural person or entity; if entity, type.
- **The basis claimed** — the investor's own selection on the questionnaire. If none was selected, that is the first gap.
- **The evidence in the file**, with the date of each item.
- **The firm's verification procedure.**

## Gate: is this a Rule 506(c) file?

If the offering relies on Rule 506(b) or another exemption, say: "This skill walks the verification step specific to Rule 506(c). This offering is recorded as relying on [X], where the investor-status process is different. I can lay out what the file contains, but which process applies is a question for the principal and counsel `[review]`." Do not run the 506(c) walk-through against a non-506(c) offering as though it applied.

If the offering's exemption is unknown, stop and ask.

## Rule text check

The provisions relevant to this skill are Securities Act Rule 501(a) (the accredited investor definition), Rule 506(c) (the exemption and its verification condition), and, for the firm's own conduct, FINRA Rule 3110 (supervision) and FINRA Rule 4511 with Exchange Act Rules 17a-3 and 17a-4 (keeping the record).

- **Fetch the current text of Rule 501(a) and Rule 506(c) from ecfr.gov or sec.gov before Step 2.** Tag `[rule text checked YYYY-MM-DD — <source>]`.
- **Never state from memory** any income or net worth figure, any asset or investment threshold, any look-back period, how recent a document must be, which professionals may give a confirmation, or which credentials or entity categories are in the definition. Every one of those comes from the fetched text or is left as a pointer.
- If the text could not be fetched: say so at the top, tag every reference `[rule text not checked — verify]`, and reduce the output to an inventory of the file (basis claimed, documents present, dates) with no line-up against the rule.
- Check sec.gov for current staff guidance on verification under Rule 506(c) and note what you found or that you could not check. Staff guidance exists and changes `[model knowledge — verify]`; do not describe its content from memory.
- State securities law questions are named and routed to counsel, not cited.

## Method

### Step 1: Record the claimed basis

One line: who the investor is, what basis they selected, where in the file they selected it. If the basis claimed does not match the kind of investor (a natural-person basis claimed by an entity, or the reverse), record the mismatch and stop the line-up until it is resolved with the investor through the firm's channel.

### Step 2: Identify what the rule text and the firm's procedure say about that basis

From the FETCHED text: locate the paragraph of Rule 501(a) the claimed basis corresponds to and the part of Rule 506(c) that addresses verification, including any listed methods relevant to this basis. Reference by paragraph; do not paraphrase thresholds into the output unless quoting the fetched text with its tag.

From the firm's procedure: which methods the firm accepts for this basis, what documents, how recent, who reviews.

Where the firm's procedure and the fetched text appear to differ, add a `[review]` row. Do not pick one.

### Step 3: Inventory the evidence

| # | Document | From whom | Dated | Covers which element of the basis | Complete / legible |
|---|---|---|---|---|---|

Read each document for what it actually says. A third-party confirmation letter: who signed, in what stated capacity, what they say they reviewed, as of when, and whether the letter says the thing the firm's procedure needs it to say. Financial documents: whose name is on them, what period, all pages present. An entity relying on its owners' status: is there evidence for each owner, or only for some.

### Step 4: Line up evidence against elements

For each element of the claimed basis (as found in the fetched text and the firm's procedure): the evidence that addresses it, or **no evidence in file**. Mark dates that look old relative to what the firm's procedure requires as `[review]` — do not rule on staleness.

### Step 5: Note what would make a reviewer pause

Inconsistencies between the questionnaire and the evidence; documents in a different name; redactions that remove the relevant figure; a confirmation from someone whose stated capacity is not one the fetched text or the firm's procedure lists; self-certification with nothing behind it; anything suggesting the evidence was prepared for the purpose of qualifying. Each tagged `[review]`.

### Step 6: Draft the decision record

A record of what was reviewed and when, with the decision and the signature left blank for the firm.

## Output

```markdown
[WORK-PRODUCT HEADER — per firm profile ## Outputs]

> ⚠️ Reviewer note — Rule text: … · Procedures: … · Read: … · Flagged: … · Before relying: …

## Rule 506(c) Verification File — [investor reference] — [offering]

**Exemption relied on (per offering file):** …   **Verification performed by (per offering documents):** …

### Bottom line
[Basis claimed: X. N of N elements have evidence in the file; N have none; N items flagged for the principal.]

### Basis claimed
[Step 1]

### Evidence inventory
[Step 3 table]

### Line-up
| Element of the basis (rule paragraph / firm procedure §) | Evidence in file | Gap or flag |
|---|---|---|

### Items for the principal's judgment
[Step 5 list]

### Draft decision record
**Investor / reference:** …   **Offering:** …   **Basis claimed:** …
**Documents reviewed (type, source, date):** …
**Method under the firm's procedure:** …
**Open items at the date of this record:** …
**Decision of the reviewing principal:** ______________________ *(to be completed by the firm — not by this draft)*
**Principal name / signature / date:** ______________________
**Record to be retained at:** [per firm retention schedule]
```

Do not reproduce account numbers, tax identifiers, or balances. Refer to documents by type, source, and date; say whether a figure is present, not what it is, unless the principal asks for it.

## Escalation points

- **To the supervising principal:** every file — the decision is theirs. Specifically flag: any element with no evidence; any basis/investor mismatch; any confirmation letter from a person whose capacity is unclear; any request to accept the subscription with open items.
- **To counsel:** whether a method not listed in the fetched rule text is acceptable; entity structures where status depends on owners; trusts and retirement vehicles; non-US investors; whether the offering can still rely on its exemption if an investor's status is in doubt; any state-law question.
- **Stop and escalate:** if the user asks how to word a record so that thin evidence reads as sufficient, or asks the skill to select a basis for the investor.

## Config-dependent fallbacks

- **Verification procedure not indexed:** head the output `INVENTORY ONLY — NOT REVIEWED AGAINST THE FIRM'S VERIFICATION PROCEDURE`.
- **Exemptions not recorded in the profile:** ask for the offering's exemption each time.

## Close with the next-steps decision tree

Per CLAUDE.md `## Outputs`: draft the request for additional evidence, escalate to the principal with the record attached, send the open legal questions to counsel, hold the subscription, or something else.
