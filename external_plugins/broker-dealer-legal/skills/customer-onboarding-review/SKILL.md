---
name: customer-onboarding-review
description: >
  Reviews an individual (KYC) or entity (KYB) onboarding file for completeness
  against the firm's customer identification and beneficial ownership
  procedures, and produces a gap list plus a draft file memo. Use when the user
  says "review this KYC file", "is this onboarding file complete", "KYB check",
  "what's missing from this investor file", "beneficial owner file", or points
  at a customer file before account opening or subscription.
argument-hint: "[file path or folder for the customer file] [--individual | --entity]"
---

# /customer-onboarding-review

1. Load `~/.claude/plugins/config/claude-for-legal/broker-dealer-legal/CLAUDE.md` → procedures index, escalation contacts.
2. Read the firm's customer identification and beneficial ownership procedures; build the checklist from them.
3. Read the customer file. Record present / missing / inconsistent for each item.
4. Output: gap list and a draft file memo for the principal.

---

## Draft status

**This output is a draft for review by a registered principal and counsel. It is not legal advice.** It reports what the file contains and does not contain. It is never a decision that the customer is identified, that identity has been verified, that an investor is accredited, or that anything is suitable. It is never a decision on identification, accreditation, or suitability — those decisions belong to the firm. Do not use the words "verified," "cleared," "passed," "approved," or "compliant" about the customer or the file.

## Purpose

Before a principal looks at a file, someone has to notice that the entity's ownership chart stops one level short or that the address on the ID doesn't match the application. This skill does that first pass against the firm's own written procedures and hands the principal a list, not a verdict.

## Inputs — ask for what's missing

- The customer file (path, folder, or pasted contents).
- Individual or entity. If entity: the entity type and, if the firm has it, the ownership and control information collected.
- Which offering or account this onboarding is for (for the memo header only).
- The firm's procedures, if not already indexed in the profile.

If the firm's procedures are not available, say: "I don't have the firm's customer identification procedure, so I can only run a generic completeness pass. A generic pass cannot tell you whether the file meets YOUR procedure. Paste or point me at the procedure, or say 'generic' and I'll mark the output accordingly." Wait for the answer.

## Rule text check

The provisions relevant to this skill are 31 CFR 1023.220 (customer identification program for broker-dealers), 31 CFR 1010.230 (beneficial ownership requirements for legal entity customers), FINRA Rule 3310 (AML compliance program), FINRA Rule 2090 (know your customer), and Regulation S-P (handling of the customer's information).

- Before citing any of them for what it requires, fetch the current text from ecfr.gov (the 31 CFR sections), the FINRA rulebook at finra.org, or sec.gov, and tag the line `[rule text checked YYYY-MM-DD — <source>]`.
- Do not quote rule text from memory. Do not state from memory which identifying information is required, any ownership percentage, any timing requirement, or any exemption or exclusion from the entity requirements. Look it up or leave it as a pointer.
- If the text could not be fetched, say so in the reviewer note and tag each reference `[rule text not checked — verify]`.
- Confirm at the source that each provision is in force in its current form; the beneficial ownership requirements in particular have been the subject of regulatory change `[model knowledge — verify]`.
- Anything outside the listed provisions (sanctions screening rules, state requirements, tax forms) is named as a topic and routed, not cited.

## Method

### Step 1: Build the checklist from the firm's procedure

Read the firm's procedure and extract each discrete item it requires for this customer type: information collected, documents or non-documentary methods used, who reviews, what is recorded, what screening is run, when it must be complete. Each checklist row carries `[firm procedure — <name>, dated X, §Y]`.

Where the firm's procedure appears silent on something the fetched rule text addresses, do not fill the gap yourself. Add a row: "Procedure does not appear to address [topic] — for the AML compliance officer `[review]`."

### Step 2: Read the file and mark each row

For each row: **Present** (cite the document in the file), **Missing**, **Inconsistent** (two documents disagree — quote both), or **Unreadable / expired / undated** (say which).

Read for internal consistency, which a checklist alone misses:
- name, date of birth, and address agree across application, identification, and any supporting document;
- documents are legible, complete (all pages), and not past any expiry shown on their face;
- for an entity, the formation documents, the ownership information, and the person signing all describe the same entity and the same people;
- the person acting for an entity has something in the file showing authority to act;
- ownership information reaches natural persons as far as the firm's procedure requires — if a layer is another entity and the file stops there, mark it.

### Step 3: Note red flags without resolving them

List anything the firm's procedure treats as a red flag, plus anything a careful reader would stop on (reluctance to provide information recorded in the file notes, documents that look altered, a structure with no apparent purpose, funds coming from a party who is not the customer). Each is tagged `[review]`. Do not assess whether the red flag is "explained" — that is the AML compliance officer's call.

### Step 4: Do not screen, and do not decide

This skill does not run sanctions, PEP, or adverse-media screening and does not treat a screening printout in the file as a result it can interpret. It records whether the file contains evidence that the firm's required screening was run, by whom, and on what date.

### Step 5: Draft the file memo

Write the memo in the firm's voice as a draft for the reviewing principal to edit and sign. Leave the conclusion line blank.

## Output

```markdown
[WORK-PRODUCT HEADER — per firm profile ## Outputs]

> ⚠️ Reviewer note — Rule text: … · Procedures: … · Read: … · Flagged: … · Before relying: …

## Onboarding File Review — [customer reference, not full identifiers] — [Individual | Entity]

**For:** [offering / account]   **Reviewed against:** [firm procedure, date | GENERIC — firm procedure not provided]

### Bottom line
[N items missing, N inconsistent, N red flags for the AML compliance officer. The file is not ready for principal review until: top 3.]

### Gap list
| # | Item required by procedure | Status | Evidence in file / what's missing | Severity | Who resolves |
|---|---|---|---|---|---|

### Red flags for review
| # | What the file shows | Where | Note |
|---|---|---|---|

### Draft request to the customer
[Plain-language list of what to ask for — no legal characterization, no promise of acceptance.]

### Draft file memo
**Customer / reference:** …
**Documents reviewed:** [by type and file reference]
**Items outstanding at the date of this memo:** …
**Red flags noted and to whom referred:** …
**Screening evidence in file:** [present, run by X on DATE | not in file]
**Conclusion of the reviewing principal:** ______________________ *(to be completed by the firm — not by this draft)*
**Reviewed by / date:** ______________________
```

Refer to identity documents by type and file reference. Do not reproduce identification numbers, dates of birth, or account numbers in the output.

## Escalation points

- **To the AML compliance officer (named in the firm profile):** any red flag; any inconsistency in identifying information; any entity whose ownership cannot be traced as far as the procedure requires; any file where screening evidence is absent.
- **To the supervising principal:** any request to open the account or accept the subscription with items outstanding. This skill does not draft an exception approval; it drafts the escalation describing what is outstanding.
- **To counsel:** whether an entity falls inside or outside the beneficial ownership requirements; non-US customers or documents; any question about relying on another financial institution's identification work; any question about sharing the file with the issuer or a vendor (Regulation S-P).
- **Stop and escalate immediately:** if the file suggests the customer is acting for an undisclosed third party, or the user asks how to complete the file in a way that avoids a requirement.

## Config-dependent fallbacks

- **Procedure not indexed:** output is headed `GENERIC COMPLETENESS PASS — NOT A REVIEW AGAINST THE FIRM'S PROCEDURES`.
- **AML compliance officer not named:** route escalations to the CCO and append a line asking the user to fill the principals table.

## Close with the next-steps decision tree

End with the decision tree per CLAUDE.md `## Outputs`: send the draft request to the customer (through the firm's approved channel), escalate the red flags, get more facts, hold the file, or something else. The principal picks.
