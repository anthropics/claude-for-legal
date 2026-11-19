---
name: token-controls-review
description: >
  Reviews a tokenized security's control design — allow-list, holder cap,
  lock-up, freeze, forced transfer, who holds the compliance role, and the
  custody or possession election — against the offering's stated terms and the
  firm's procedures, and lists the questions for the principal and counsel. Use
  when the user says "token controls", "review the token design", "transfer
  restrictions", "allow-list", "whitelist", "who holds the admin key",
  "compliance role", "forced transfer", "custody model for the token", or
  shares a token contract, spec, or term sheet for a security token.
argument-hint: "[path to the token spec, contract source, or term sheet] [--offering <name>]"
---

# /token-controls-review

1. Load `~/.claude/plugins/config/claude-for-legal/broker-dealer-legal/CLAUDE.md` → custody and settlement model, exemptions, approvers.
2. Establish what the design says each control does, who can operate it, and what record is kept.
3. Compare the controls with what the offering documents promise investors and what the firm's procedures assume.
4. Output: a control table, mismatches, and a numbered question list for the principal and counsel.

---

## Draft status

**This output is a draft for review by a registered principal and counsel. It is not legal advice.** It is a design review that produces questions. It is not a conclusion that a token is or is not a security, that a design satisfies any exemption or rule, that any party does or does not have custody, possession, or control, or that any party is or is not required to register. It is not a smart contract security audit. It is never a decision on identification, accreditation, or suitability — those belong to the firm.

## Purpose

A token's contract enforces whatever its roles are configured to enforce, regardless of what the offering memorandum says. If the document promises a lock-up and the contract has none — or the contract lets one key move any investor's tokens and nobody decided who holds it — the firm finds out at the worst time. This skill puts design, documents, and procedures side by side and turns every mismatch into a question with an owner.

## Inputs — ask for what's missing

- **The design:** token specification, contract source or interface, or a written description. Say which you were given; a description is not the code.
- **Deployment facts:** chain, contract address if deployed, whether upgradeable and who controls upgrades, whether audited and by whom (ask for the report).
- **Roles:** every privileged role (owner, admin, compliance/transfer agent role, minter, pauser, upgrader) and who holds each key today — named person or entity, single key or multi-signature, and the signing policy.
- **The offering documents:** the exemption stated, transfer restrictions, lock-up terms, investor eligibility, any holder limit, redemption or recovery terms.
- **The firm's role:** what the firm does in issuance, transfer approval, and settlement; what the vendor does; what the issuer does.
- **Custody facts:** where investors hold tokens (self-custody wallets, a custodian, the platform, the firm), who can move them, and what the firm and counsel have determined (from the profile).

## Rule text check

The provisions relevant to this skill: Securities Act Rules 506(b) and 506(c) and Rule 501(a) (the exemption and investor status the controls are meant to support), Rule 506(d) (who the role holders are), Exchange Act Section 15(a) (whether operating a control is activity that needs registration — a question, never an answer), FINRA Rule 3110 (supervision of the firm's part in operating controls), FINRA Rule 3310 with 31 CFR 1023.220 and 31 CFR 1010.230 (the identity behind each allow-listed address), Exchange Act Rules 17a-3 and 17a-4 with FINRA Rule 4511 (records of control actions), FINRA Rule 2210 (how the controls are described to investors), and Regulation S-P (customer information linked to on-chain addresses).

- Fetch current text from ecfr.gov, sec.gov, or finra.org before describing what any provision requires; tag `[rule text checked YYYY-MM-DD — <source>]` or `[rule text not checked — verify]`.
- **Never state from memory:** any holding period or resale condition; any number of holders that triggers any consequence; any investor limit; any condition on a broker-dealer's custody of digital asset securities. If the offering documents state such a figure, quote the document, tag it `[user provided — offering document]`, and ask counsel to confirm it.
- **Much of what matters here is outside this plugin's citation list** — resale restrictions on privately placed securities, holder-count registration triggers, broker-dealer custody and customer-protection requirements, transfer agent and trading-venue registration, SEC and staff statements on digital asset securities, state law. For each, name the topic in plain words in the question list and assign it to counsel. Do not supply a citation or a description of the requirement from memory. Check sec.gov and finra.org for current statements on digital asset securities and report what you found or that you could not check; this area changes quickly `[model knowledge — verify]`.

## Method

### Step 1: Describe each control as designed

For each control: what it does, what triggers it, who can operate it, whether it can be changed after deployment and by whom, and what on-chain event and off-chain record it leaves. Mark the source: `[contract source]`, `[spec]`, or `[described by user — not confirmed against code]`.

| Control | Questions to answer from the design |
|---|---|
| **Allow-list** | What must be true for an address to be added (onboarding complete? status determined by the firm? jurisdiction?) and who confirms it? Is it checked on send, receive, or both? Can an address be removed, and what happens to its balance? Is one investor ↔ many addresses handled? Who can add addresses — and can they add their own? |
| **Holder cap** | Is there one? Counted by address or by identified holder? Who set the number and from what source? What happens to a transfer that would exceed it? Can the cap be changed, and by whom? |
| **Lock-up** | Is it enforced in the contract or only by policy? From what start date per holder? Can it be shortened or waived, and by whom? Does it match the offering documents exactly? What happens on transfers between allow-listed holders during the period? |
| **Freeze / pause** | Per-address, global, or both? Who can invoke it, on what grounds, with whose approval? Is there a time limit or review? How is the holder told? |
| **Forced transfer / recovery / burn-and-reissue** | Under what stated circumstances (lost keys, court order, error, sanctions)? Who authorizes, who executes, and are those different people? Is it disclosed to investors? What record is made? |
| **Mint / burn** | Who can create or destroy supply? Is supply capped to the offering amount? How does a mint tie to a paid, accepted subscription? |
| **Upgradeability / role administration** | Can the logic be replaced? Can roles be reassigned? By one key? With a delay? Who is told? |

### Step 2: Who holds the compliance role

List every privileged role, the holder, the key arrangement, and the approval that precedes each use. Then ask, without answering:

- Is the holder the issuer, the firm, the vendor, or an individual? Is that what the offering documents say?
- Can a single person both approve and execute a restricted action?
- If the vendor or an individual operates transfers, approvals, or the allow-list, does that activity raise a registration question under Exchange Act Section 15(a) or another registration category? `[review]` → counsel.
- What happens if the role holder is unavailable, compromised, or leaves? Is there a documented succession and key-recovery process?
- Is each role holder among the persons from whom a bad actor questionnaire was collected, if the current Rule 506(d) text and counsel treat them as covered?
- Who supervises the firm's own personnel when they operate a control (FINRA Rule 3110), and where is that written?

### Step 3: Custody or possession election

Record, from the firm profile and the documents, what the firm and counsel have determined and when. Then lay out the facts that bear on it, as facts:

- who can move an investor's tokens without the investor (any role with forced transfer, burn, or upgrade power);
- who holds investor keys, if anyone other than the investor;
- where investor funds go and who controls them before closing;
- what the investor is told about all of the above.

If the profile's custody section is `[PENDING]`, or the design facts differ from what the profile records (for example, the firm is recorded as not holding customer assets but a firm employee holds the forced-transfer key), flag it 🔴: "The recorded custody position and the design facts appear to differ. `[review]` For counsel before launch." **Do not characterize the arrangement** as custody, non-custody, possession, or control.

### Step 4: Compare design ↔ offering documents ↔ firm procedures

Three-column comparison for every control. A mismatch is any place where: the documents promise a restriction the contract doesn't enforce; the contract has a power the documents don't disclose; the firm's procedures assume a step (principal approval before allow-listing; identification complete before transfer) that the system doesn't require; or a number in the contract differs from the number in the documents. Each mismatch is 🔴 or 🟠 and gets an owner.

### Step 5: Records

For each control action (allow-list add/remove, freeze, forced transfer, mint, burn, role change, upgrade): what on-chain event is emitted, what off-chain authorization record exists, and how the two are linked. Missing links hand off to `/broker-dealer-legal:books-and-records-map`.

### Step 6: Write the question list

Every `[review]`, every mismatch, and every unanswered design question becomes a numbered question addressed to the **principal** (operational and supervisory decisions) or **counsel** (legal characterization, registration, exemption, custody, disclosure). Questions are specific enough to answer in a sentence.

## Output

```markdown
[WORK-PRODUCT HEADER — per firm profile ## Outputs]

> ⚠️ Reviewer note — Rule text: … · Reviewed from: [contract source | spec | description only] · Procedures: … · Flagged: … · Before relying: … · This is not a smart contract security audit.

## Token Controls Review — [token / offering] — as of [date]

**Exemption stated in offering documents:** …  **Chain / contract:** …  **Upgradeable:** …  **Audit report provided:** …

### Bottom line
[N controls reviewed. N mismatches between design, documents, and procedures (N 🔴). N questions for the principal, N for counsel. The three to answer first.]

### Control table
| Control | As designed (source) | Who can operate | Changeable after deployment? | On-chain event / off-chain record | Offering documents say | Firm procedure assumes | Match? |
|---|---|---|---|---|---|---|---|

### Roles and keys
| Role | Powers | Holder | Key arrangement | Approval before use | Flag |
|---|---|---|---|---|---|

### Custody or possession — facts for counsel
**Position recorded in firm profile:** [text and date | PENDING]
**Design facts bearing on it:** …
**Apparent difference between recorded position and design:** [none noted | describe] `[review]`

### Mismatches
| # | Design says | Documents / procedures say | Severity | Owner |
|---|---|---|---|---|

### Questions for the principal
1. …

### Questions for counsel
1. … *(topics outside this plugin's citation list are named in plain words, without citations)*
```

## Escalation points

- **To counsel — before launch, always:** the custody or possession question; any role held by a party that is not registered and operates transfers or approvals; any mismatch between the contract and the offering documents; whether the controls as designed support the stated exemption and resale restrictions; undisclosed forced-transfer or upgrade powers; any plan for secondary transfers or trading.
- **To the supervising principal:** who holds each role and the approval required before each use; any control a single person can approve and execute; allow-listing that can occur before onboarding review is complete; the supervision write-up for firm personnel operating controls.
- **To the AML compliance officer:** how an address is tied to an identified customer, and how transfers to non-allow-listed or newly allow-listed addresses are reviewed.
- **Stop and escalate:** a deployed contract already holding investor tokens with a 🔴 mismatch; a request to describe an admin power to investors in softer terms than the code supports; a request to design a control so that a holder limit or eligibility check is avoided rather than enforced.

## Config-dependent fallbacks

- **Custody section `[PENDING]`:** run the review, mark the custody block PENDING, and put the custody question first in the counsel list.
- **Only a description provided, no code or spec:** head the output `REVIEWED FROM DESCRIPTION ONLY — NOT CONFIRMED AGAINST THE CONTRACT` and add, as question one for the principal, who will confirm the description against the deployed code.

## Handoff

🔴 mismatches carry forward at the same severity into `/broker-dealer-legal:offering-file-review` (token design gate). Investor-facing descriptions of the controls go through `/broker-dealer-legal:communications-review`.

## Close with the next-steps decision tree

Per CLAUDE.md `## Outputs`: format the question list as a memo to counsel, draft the role-and-approval matrix for the principal, hand the record links to the books-and-records map, hold the launch, or something else.
