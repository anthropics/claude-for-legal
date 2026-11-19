---
name: outside-activity-notice
description: >
  Drafts a registered person's written notice to the firm of an outside
  business activity, and flags when the activity may instead (or also) need
  private securities transaction treatment. Use when the user says "outside
  business activity", "OBA", "I've been asked to join a board", "side
  business", "advising a startup", "paid in tokens for advising", "private
  securities transaction", "selling away", or a registered person describes
  any work, role, or investment activity outside the firm.
argument-hint: "[describe the activity, or path to the offer / agreement]"
---

# /outside-activity-notice

1. Load `~/.claude/plugins/config/claude-for-legal/broker-dealer-legal/CLAUDE.md` → outside-activities procedure, CCO, supervising principal.
2. Collect the facts of the activity. Check them against the documents.
3. Screen for securities involvement. If present, flag possible private securities transaction treatment.
4. Output: a draft notice for the registered person to review and submit, a flag sheet for the principal, and a firm-response block left blank.

---

## Draft status

**This output is a draft for review by a registered principal and counsel. It is not legal advice.** It drafts a notice in the registered person's name for that person to check, sign, and submit through the firm's process. It is not the firm's acknowledgment, approval, or conditions, not a conclusion that an activity is or is not an outside business activity or a private securities transaction, and never a decision on identification, accreditation, or suitability — those belong to the firm. The activity should not begin (or continue) on the strength of this draft.

## Purpose

Registered persons under-describe outside activities because they think of them as small. The firm then evaluates a two-line notice for something that turns out to involve raising money for a startup and being paid in tokens. This skill gets the full facts onto the notice the first time, and makes sure the securities question is asked before the principal has to guess.

## Inputs — ask for what's missing

- **Who:** the registered person (name, role at the firm, supervising principal).
- **The activity:** the organization, what it does, the person's title and actual duties.
- **Start date** — and whether it has already started.
- **Time:** hours, and whether during the firm's business hours.
- **Compensation:** whether any, from whom, in what form (cash, equity, options, tokens, carried interest, expense reimbursement), and what it depends on. Record form and basis.
- **Securities involvement** — ask each directly:
  - Does the organization issue, sell, or plan to sell securities, tokens, notes, or fund interests?
  - Will you introduce, solicit, or speak with investors, or help raise capital, in any way?
  - Will you receive anything that depends on money being raised or an investment being made?
  - Will you invest your own money, or receive equity or tokens?
  - Will you handle funds, wallets, or keys belonging to others?
  - Are any of the firm's customers, or the firm's issuers, involved?
- **Use of the firm:** name, email, premises, systems, customer relationships.
- Any offer letter, advisor agreement, token grant, or board appointment. Read it; documents control over the description.

## Rule text check

The provisions relevant to this skill: FINRA Rule 3270 (outside business activities of registered persons), FINRA Rule 3280 (private securities transactions of an associated person), FINRA Rule 3110 (the firm's supervision), FINRA Rule 2010, Exchange Act Section 15(a) (only where the outside entity or the person may be effecting securities transactions away from any registered firm), and FINRA Rule 4511 with Exchange Act Rules 17a-3 and 17a-4 (keeping the notice and the firm's response).

- **First, confirm at the FINRA rulebook (finra.org) that Rules 3270 and 3280 are still the rules in force.** FINRA has pursued rulemaking to replace or consolidate its outside-activity rules `[model knowledge — verify]`. If the rulebook shows a successor rule in effect, say so at the top, stop using the old numbers as current, tell the user this skill was written against Rules 3270 and 3280, and limit the output to the fact collection and a draft notice headed "prepared against superseded rule numbers — principal and counsel to conform."
- Fetch the current text before stating what a notice must contain, when it must be given, what the firm must consider, what counts as compensation, or what is excluded. Tag `[rule text checked YYYY-MM-DD — finra.org]`. **Never state these from memory.**
- If the text could not be fetched, tag `[rule text not checked — verify]` and build the notice from the firm's own procedure and form.
- Tax, employment-agreement, and state-law issues are named and routed, not cited.

## Method

### Step 1: Fact collection and document check

Compare the person's description with the documents. Common gaps: "advisor" whose agreement includes introducing investors; "no compensation" alongside a token or equity grant; "passive investment" with a board seat or management role; an activity that has already started. Show each discrepancy with both sources.

### Step 2: Securities screen — the flag for private securities transaction treatment

Mark each as yes / no / unknown:

| Indicator | Why it matters |
|---|---|
| The outside entity is raising or will raise capital, or issues tokens that may be securities | A securities transaction may exist for the person to participate in |
| The person will find, introduce, solicit, or communicate with investors | Participation in a securities transaction outside the firm |
| The person receives anything tied to capital raised or investments made | Selling compensation — also run the gate below |
| The person is paid in equity, options, or tokens of the issuer | May itself be a securities transaction; may be compensation |
| The person invests personally or co-invests with customers | Securities transaction by the person; possible conflict |
| The person structures, negotiates, or documents the investment | Participation beyond an introduction |
| The firm's customers or issuers are counterparties | Conflict and supervision questions |

**Any "yes" or "unknown"** → add at the top of the output: "⚠️ This activity may involve a private securities transaction. `[review]` Treatment under FINRA Rule 3280, in addition to or instead of FINRA Rule 3270, is for the principal and counsel to determine before the activity proceeds." Do not decide which rule governs. Do not conclude that a token is or is not a security.

**All "no"** → say the screen found no securities indicators on the facts given, and that the principal still makes the determination.

### Step 3: Compensation gate

If the person would receive compensation that depends on a securities transaction closing or on the amount raised — from anyone other than this firm through its normal payroll — do not compute, estimate, or draft it. Record "compensation contingent on capital raised: yes" without the rate, and run `/broker-dealer-legal:intermediary-compensation-check`. Note for counsel that a registered person paid transaction-based compensation outside their firm raises both the FINRA Rule 3280 question and, for the outside entity, the Exchange Act Section 15(a) question.

### Step 4: Conflicts and firm exposure

List, without resolving: overlap with the firm's customers, issuers, or business lines; use of the firm's name or resources; whether investors could believe the activity is the firm's; time commitment against the person's firm duties; access to confidential or customer information (Regulation S-P).

### Step 5: Draft the notice

Use the firm's form if the profile has one. Otherwise the format below. Write it in the registered person's first-person voice, complete and specific. Include facts that are unhelpful to the person; a notice that omits them is worse than none.

## Output

```markdown
[WORK-PRODUCT HEADER — per firm profile ## Outputs]

> ⚠️ Reviewer note — Rule text: … (rule currency: 3270/3280 confirmed in force | successor rule found | not checked) · Procedures: … · Read: … · Flagged: … · Before relying: …

[⚠️ private securities transaction flag, if raised]

## Draft Notice of Outside Activity

**To:** [CCO / supervising principal]   **From:** [registered person]   **Date:** ______

1. **Organization and what it does:** …
2. **My role, title, and duties:** …
3. **Start date (and whether already begun):** …
4. **Time commitment; during or outside firm hours:** …
5. **Compensation — whether any, from whom, form, and what it depends on:** … *(form and basis only; no contingent rates)*
6. **Securities involvement:** [answers to each screen question, in sentences]
7. **Connection to the firm's customers, issuers, or business:** …
8. **Use of the firm's name, premises, or systems:** none / describe
9. **Documents attached:** …
10. **I will update this notice if any of the above changes.**

**Signature of registered person:** ______________________

---
### For the firm — not completed by this draft
**Determination (outside business activity / private securities transaction / both / neither):** ______
**Approved, approved with conditions, or not approved:** ______
**Conditions and supervision, if any:** ______
**Principal name / signature / date:** ______
**Record retained at:** ______

---
## Flag sheet for the principal
| Indicator | Yes / No / Unknown | Source |
|---|---|---|

**Discrepancies between description and documents:** …
**Conflicts noted:** …
**Questions for counsel:** …
```

## Escalation points

- **To the supervising principal and CCO:** every notice — the determination and any approval are theirs. Flag first: any securities indicator; any activity that has already begun; any discrepancy between description and documents.
- **To counsel:** whether an instrument (including a token or a SAFE-type right to tokens) is a security; whether the outside entity or the person needs to be registered; any transaction-based compensation outside the firm; any activity involving the firm's customers' money.
- **Stop and escalate:** a request to describe the activity so that it reads as not involving securities, to leave out compensation, or to back-date the notice. Decline the wording, tell the user plainly that the accurate notice is the one that protects them, and offer to draft the accurate one.

## Config-dependent fallbacks

- **Firm procedure or form not indexed:** use the format above and note that it is not the firm's form.
- **Principal not named:** address the notice to "Chief Compliance Officer."

## Close with the next-steps decision tree

Per CLAUDE.md `## Outputs`: finalize the notice for the registered person to submit, draft the cover escalation to the principal, send the questions to counsel, hold the activity, or something else.
