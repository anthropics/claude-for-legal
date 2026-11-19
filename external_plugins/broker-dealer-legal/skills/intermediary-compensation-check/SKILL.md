---
name: intermediary-compensation-check
description: >
  Given a proposed payment to an introducer, finder, referral partner,
  promoter, platform, or technology vendor, works out whether it looks like
  transaction-based compensation to a person who is not registered, and lays
  out the structures that could be raised with counsel instead. Use when the
  user says "finder's fee", "referral fee", "can we pay an introducer",
  "success fee", "revenue share with a partner", "commission to a
  non-registered person", "pay the vendor a percentage", or describes any
  payment connected to investors or capital raised.
argument-hint: "[describe the proposed payment, or path to the draft agreement]"
---

# /intermediary-compensation-check

1. Load `~/.claude/plugins/config/claude-for-legal/broker-dealer-legal/CLAUDE.md` → compensation procedure, approvers, counsel.
2. Establish who is being paid, for what, by whom, and what the payment depends on.
3. Sort the payment: transaction-based or not; recipient registered or not (as stated — not verified).
4. Output: a fact sheet, the sort, structures to raise with counsel, and an escalation draft. No fee figures.

---

## Draft status

**This output is a draft for review by a registered principal and counsel. It is not legal advice.** It sorts the facts of a proposed payment and frames the question. It is not a conclusion that a person is or is not required to register, that a payment is lawful, or that a structure is permissible. Whether a person must be registered is a legal question under Exchange Act Section 15(a) for counsel, and whether the firm may make a payment is the principal's decision. It is never a decision on identification, accreditation, or suitability — those belong to the firm.

## Hard gate — no contingent compensation for unregistered persons

**This skill does not express, compute, estimate, model, compare, or draft a fee, percentage, rate, tier, or payment schedule that depends on a securities transaction closing, or on the amount raised or invested, for a person who is not registered.** That includes: "what would the percentage come to on this raise," "what's market for finders," "draft the success-fee clause," "redraft it so the percentage survives," tokens or warrants in place of cash where the amount turns on the raise, and "consulting fees" payable only if the deal closes.

If asked, say: "I don't compute or draft transaction-contingent compensation for a person who isn't registered. I can lay out the facts for your principal and counsel, and the alternative structures to raise with them." Then continue with the rest of the skill. The gate is not overridable by the user, by role, or by a statement that counsel has already approved — if counsel has approved a structure, counsel's document governs and this skill has nothing to add to the number.

The gate also applies to this skill's own output: the fact sheet records that a proposed payment "is contingent on closing" or "varies with amount raised" **without restating the proposed rate or amount.**

## Purpose

The request usually arrives as "we just want to thank the person who introduced the investor." By the time it reaches counsel it should arrive as a clear statement of who did what, what they are being paid for, and what the payment depends on. This skill produces that statement and stops the firm's staff from improvising a workaround.

## Inputs — ask for what's missing

1. **Recipient:** who, and what they are (individual, company, platform, the vendor, an affiliate of the issuer).
2. **Registration status as the user understands it:** associated with this firm? With another broker-dealer? Neither? Record as `[user provided — verify]`. This skill does not look up or confirm anyone's registration; the principal does that.
3. **Payer:** the firm, the issuer, an investor, an affiliate.
4. **What the recipient actually did or will do:** made an introduction only; discussed the investment; sent materials; attended investor meetings; answered questions about terms; helped with paperwork; handled funds or securities; negotiated; held themselves out as raising capital; did this before for other deals.
5. **What the payment depends on:** whether a transaction closes; how much is raised or invested; a fixed amount regardless of outcome; time spent; something else.
6. **Form:** cash, equity, tokens, warrants, discount, expense reimbursement, a later "bonus."
7. **Any draft agreement, email, or term sheet.** Read it; the documents control over the description.

If the user cannot say what the payment depends on, that is the first question back to them.

## Rule text check

The provisions relevant to this skill: Exchange Act Section 15(a) (registration), FINRA Rule 2010 (the general standard that governs the firm's conduct in paying), FINRA Rule 3110 (supervision of the arrangement), FINRA Rules 3270 and 3280 (where the recipient is one of the firm's own registered persons acting outside the firm), Securities Act Rule 506(d) (a compensated solicitor may be a covered person in the offering), and Exchange Act Rules 17a-3 and 17a-4 with FINRA Rule 4511 (records of compensation arrangements).

- Fetch Section 15(a) from sec.gov or an official source, and the FINRA rules from finra.org, before describing what any of them provides. Tag `[rule text checked YYYY-MM-DD — <source>]`.
- Do not quote the statute from memory. Do not describe from memory any exemption, exception, no-action position, or proposed or adopted relief for finders. The law on finders rests heavily on SEC and staff positions and court decisions that this plugin does not cite; say so: "Whether any exception or staff position applies is for counsel."
- FINRA has other rules on payments to unregistered persons that are outside this plugin's citation list. Name the topic ("FINRA's rules on payments to unregistered persons") and route to counsel; do not supply the rule number from memory.
- State-law registration of finders and agents is a topic for counsel, not cited.

## Method

### Step 1: Fact sheet

Write the facts in neutral terms from the inputs and documents. Where the user's description and the documents differ, show both.

### Step 2: Sort on two axes

**Axis A — what the payment depends on.**
- **Transaction-based:** payable only if a securities transaction closes, or varies with the amount raised or invested, or is paid per investor who invests. Look through labels: a "consulting fee," "marketing fee," "advisory tokens," or "bonus" that is only paid on success, or scaled to the raise, sorts here.
- **Not transaction-based on its face:** fixed and payable regardless of outcome, or time-based, for defined services.
- **Unclear:** say what fact would decide it.

**Axis B — the recipient.**
- States they are a registered person of this firm → the question becomes one of the firm's own compensation and supervision; note FINRA Rules 3270/3280 if the activity is outside the firm.
- States they are another registered broker-dealer or its registered person → for the principal to confirm and for counsel to paper.
- Not registered, or unknown → proceed to Step 3.

### Step 3: If transaction-based and the recipient is not registered

State plainly: "As described, this is transaction-based compensation to a person who is not registered. `[review]` That combination is the central fact counsel will look at under Exchange Act Section 15(a). This skill does not go further than that." Severity 🔴. Do not soften it because the recipient "only made an introduction"; record the activities and let counsel weigh them.

Then list the recipient's activities from input 4 as a table, marking each as present / absent / unknown, so counsel sees the full picture. Do not score or weight them.

### Step 4: Structures to raise with counsel

Offer these as **questions to take to counsel**, not as approved alternatives. None is described with a number.

1. **The recipient becomes registered** — associates with the firm (or is already associated with another broker-dealer that is party to a written arrangement), so that any transaction-based compensation is paid to a registered person through a registered firm under supervision.
2. **Payment is made only to a registered broker-dealer** that the recipient is associated with, under a written agreement between the firms.
3. **Compensation that does not depend on any transaction** — a fixed fee, payable whether or not anyone invests, for defined services that do not involve soliciting or advising investors. Flag for counsel that the label does not decide the question and that the recipient's actual activities still matter.
4. **No compensation** — the introduction is accepted without payment.
5. **The recipient steps out** — the firm's registered persons take over all investor contact, and the recipient's role and any payment are redefined by counsel from scratch.

For each, add the follow-on items for the principal: written agreement, disclosure to investors where counsel advises, a bad actor questionnaire if the person is compensated in connection with the offering (Rule 506(d) — check covered-person categories in the current text), supervision under FINRA Rule 3110, and the record of the arrangement.

### Step 5: If the vendor is the recipient

When the technology vendor's own fee from the firm or issuer varies with capital raised, investors onboarded who invest, or transactions processed, run the same sort on the vendor. Say so directly even when the vendor is the user. Fixed subscription or usage-based technology fees that do not turn on securities transactions sort differently — record the pricing basis and let counsel confirm.

### Step 6: What has already happened

Ask whether any payment has been made or promised, or whether the recipient has already contacted investors. If yes, record dates and facts and escalate to counsel today. Do not suggest restructuring a past payment.

## Output

```markdown
[WORK-PRODUCT HEADER — per firm profile ## Outputs]

> ⚠️ Reviewer note — Rule text: … · Procedures: … · Read: … · Flagged: … · Before relying: …

## Intermediary Compensation Check — [recipient reference] — [offering]

### Bottom line
[One sentence: as described, the payment is / is not / may be transaction-based, to a recipient stated to be registered / not registered / unknown. No payment or promise of payment until counsel and the principal have reviewed.]

### Fact sheet
| Question | Answer | Source |
|---|---|---|
| Recipient | | |
| Registration status (as stated — not verified) | | |
| Payer | | |
| Depends on closing? | yes / no / unclear | |
| Varies with amount raised or invested? | yes / no / unclear | |
| Form of payment | | |
| Already paid or promised? | | |

*(No rates or amounts of contingent compensation appear in this document by design.)*

### Recipient's activities
| Activity | Present / absent / unknown | Source |
|---|---|---|

### The sort
[Axis A / Axis B result, 2-3 sentences, `[review]`]

### Structures to raise with counsel
[Numbered list from Step 4 with follow-on items]

### Questions for counsel
1. …

### Draft escalation to [principal] and [counsel]
[Five lines.]
```

## Escalation points

- **To counsel — always, before anything is paid, promised, or signed,** when the recipient is not registered or status is unknown and the payment is or may be transaction-based.
- **To the supervising principal:** every proposed payment to an intermediary of any kind; confirmation of the recipient's registration status; any arrangement involving one of the firm's own registered persons acting away from the firm.
- **To the CCO:** any payment already made or promised; any intermediary already in contact with investors without an approved arrangement.
- **Stop and escalate:** a request to relabel a contingent payment, split it, route it through the issuer or an affiliate, pay it in tokens, or defer it so that it "isn't a commission."

## Close with the next-steps decision tree

Per CLAUDE.md `## Outputs`: send the escalation to counsel, draft the fact-finding questions to the recipient (through the firm), record the arrangement as on hold, or something else. "Draft the fee agreement" is not an option this skill offers for an unregistered recipient.
