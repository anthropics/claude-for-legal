---
name: offering-file-review
description: >
  Checks an offering file gate by gate — issuer file, screening, bad actor
  questionnaires, counsel review, principal approval, filings — and lists what
  blocks the offering from opening to investors. Use when the user says
  "offering file review", "is this deal ready to open", "what's blocking
  launch", "gate check", "pre-launch checklist", or points at an offering
  folder before the firm begins selling.
argument-hint: "[offering folder path or name] [--gate N]"
---

# /offering-file-review

1. Load `~/.claude/plugins/config/claude-for-legal/broker-dealer-legal/CLAUDE.md` → `## Offering gates`, procedures index, approvers.
2. Read the offering file. For each gate, record the evidence present against the evidence the firm requires.
3. Output: a gate table, a blocker list in order, and an escalation draft for the supervising principal.

---

## Draft status

**This output is a draft for review by a registered principal and counsel. It is not legal advice.** It reports which gates have the evidence the firm's procedure asks for. It is not approval of the offering, not a finding that due diligence was reasonable, not a conclusion that an exemption is available or that no one is disqualified, and never a decision on identification, accreditation, or suitability — those belong to the firm. A gate is "evidence present" or "evidence missing"; only a principal marks it passed.

## Purpose

Offerings open early because everyone assumed someone else had the questionnaire from the fifth director. This skill reads the file the way the supervising principal will, in the firm's gate order, and says plainly what is not there.

## Inputs — ask for what's missing

- The offering folder (or an index of it).
- The exemption the offering relies on, as stated in the offering documents.
- Whether the issuer is the firm itself or an affiliate (this changes which filing gate questions arise).
- Whether the security is tokenized (if yes, add the token gate below).
- The intended launch date, if any.

## Rule text check

The provisions relevant to this skill, each only at the gate where it applies: Securities Act Rules 506(b) and 506(c) (the exemption relied on), Rule 506(d) (bad actor disqualification — Gate 3), FINRA Rule 3110 (supervision and the principal's review — Gate 5), FINRA Rules 5122 and 5123 (filings — Gate 6), FINRA Rule 2210 (offering communications — hand-off), FINRA Rule 2111 and Regulation Best Interest (only if the firm makes recommendations), and Exchange Act Rules 17a-3 and 17a-4 with FINRA Rule 4511 (keeping the file).

- Fetch current text from ecfr.gov, sec.gov, or the FINRA rulebook before saying anything about what a provision requires. Tag `[rule text checked YYYY-MM-DD — <source>]`.
- **Never state from memory:** who is a covered person under Rule 506(d), what events disqualify or the look-back periods, which offerings FINRA Rules 5122 or 5123 apply to or exempt, or any filing deadline. Look it up, or tag `[rule text not checked — verify]` and leave the row as a question.
- SEC and state notice filings for the offering are a real gate item, but the provisions governing them are outside what this plugin cites. Name the topic ("SEC and state notice filings") and assign it to counsel.

## Method

Use the firm's gates from the profile in the firm's order. If the profile still has the defaults, use the six below and say so.

### Gate 1 — Issuer file

Against the firm's due diligence procedure: formation and good-standing documents; capitalization; governing documents; financial statements (and what kind); offering documents in final or near-final form; use of proceeds; material contracts; litigation and regulatory history; the issuer's completed questionnaire; a diligence memo. If there is no diligence memo, note it and point to `/broker-dealer-legal:diligence-memo`.

Check that the documents describe the same deal: the security, the amount, the price, and the exemption stated in the offering document, the subscription agreement, and the firm's engagement agreement agree. Disagreement is a 🔴 blocker.

### Gate 2 — Screening

Record whether the file contains evidence that the firm's required screening of the issuer and its people was run, on whom, by whom, when, and whether hits were dispositioned by a named person. Compare the list of people screened with the list of people named in the offering documents and the cap table. Anyone named but not screened is a gap. Do not run or interpret screening.

### Gate 3 — Bad actor questionnaires

1. From the fetched Rule 506(d) text, identify the categories of covered persons. If the text was not fetched, do not list them from memory — ask the user for the firm's covered-person list for this offering and tag it `[user provided]`.
2. Build the list of actual people and entities in each category from the offering documents, cap table, and engagement and compensation arrangements. Include anyone being paid in connection with the sale — and for each such person, cross-check `/broker-dealer-legal:intermediary-compensation-check`.
3. For each: is there a questionnaire, signed, dated, complete, and recent enough under the firm's procedure? Any "yes" answer or attached disclosure is 🔴 and goes to counsel as it stands — do not assess whether an event is disqualifying, waivable, or disclosable.
4. Note whether the file shows a process for refreshing questionnaires during a continuing offering.

### Gate 4 — Counsel review

Is there written evidence that counsel reviewed what the firm's procedure says counsel reviews (offering documents, exemption analysis, token design where relevant)? Record who, when, and the scope stated. "Counsel was on the email" is not evidence. If the scope of counsel's review is narrower than the open legal questions in the file, list the uncovered questions.

### Gate 5 — Principal approval

Is there a dated approval by the principal named in the firm profile, and does it post-date the final versions of the documents it approves? An approval that pre-dates a later change to the offering documents is a gap. Record whether the file shows what the principal reviewed.

### Gate 6 — Filings

List each filing the firm's procedure identifies for this kind of offering, who is responsible (firm, issuer, counsel), status, and evidence. For FINRA Rules 5122 and 5123: state whether the fetched text indicates the rule applies to this offering, with the paragraph reference; if not fetched or not clear, mark `[review]` for counsel. Never supply a deadline from memory.

### Additional gate — token design (only if tokenized)

Is there a completed `/broker-dealer-legal:token-controls-review` and evidence that its questions were answered by the principal and counsel? If not, 🔴.

### Additional gate — communications

Are the offering's investor-facing materials in the approval log? If not, hand off to `/broker-dealer-legal:communications-review`.

### Order the blockers

A blocker is any gate item whose evidence is missing, stale, or inconsistent. Order by dependency (what must happen before the next thing can), not by gate number, and name the owner of each.

## Output

```markdown
[WORK-PRODUCT HEADER — per firm profile ## Outputs]

> ⚠️ Reviewer note — Rule text: … · Procedures: … · Read: … · Flagged: … · Before relying: …

## Offering File Review — [issuer / offering] — as of [date]

**Exemption stated in offering documents:** …   **Intended open date:** …

### Bottom line
[N of N gates have complete evidence. N blockers. The offering cannot be presented to the principal as ready until: top 3.]

### Gate table
| # | Gate | Evidence required (firm procedure) | Evidence in file | Status: Evidence present / Partial / Missing | Sign-off recorded? |
|---|---|---|---|---|---|

### What blocks opening — in order
| # | Blocker | Gate | Severity | Owner | Depends on |
|---|---|---|---|---|---|

### Covered persons and questionnaires
| Person / entity | Why covered (rule paragraph / firm list) | Questionnaire in file | Dated | Disclosures → counsel |
|---|---|---|---|---|

### Questions for counsel
[Numbered, specific.]

### Draft escalation to [supervising principal]
[Five lines: what the offering is, what's complete, what blocks, what decision is needed, by when.]
```

Status words are "Evidence present / Partial / Missing." Never "Passed," "Cleared," or "Approved."

## Escalation points

- **To the supervising principal:** the full blocker list; any request to open with a blocker outstanding; any document inconsistency; any approval that pre-dates the final documents.
- **To counsel:** every questionnaire disclosure; every exemption question (including anything in the file suggesting general solicitation in an offering recorded as Rule 506(b)); whether FINRA Rules 5122 or 5123 apply; SEC and state notice filings; any compensated person who is not registered.
- **Stop and escalate:** if the file shows sales activity or investor funds received before principal approval is recorded. Report the fact with its source and nothing more; do not characterize it.

## Config-dependent fallbacks

- **Gates not configured:** use the six defaults and add: "These are default gates, not your firm's. Configure them with `/broker-dealer-legal:cold-start-interview --redo gates`."
- **Approver not named:** leave the sign-off column as "approver not configured."

## Close with the next-steps decision tree

Per CLAUDE.md `## Outputs`: draft the request list to the issuer, send the escalation, send the counsel questions, hold the offering, or something else. Offer a dashboard view when the gate table runs past ten rows.
