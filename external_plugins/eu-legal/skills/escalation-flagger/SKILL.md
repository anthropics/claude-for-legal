---
name: escalation-flagger
description: >
  Route a contract issue to the right approver per the escalation matrix in
  commercial.md, and draft the ask. EU-scoped: thresholds in EUR, EU-specific
  auto-triggers (cross-border data transfers outside EEA, ICT third-party DORA
  check, non-EU governing law, liability cap below regulatory exposure minimum).
  Use when the user says "who needs to approve this", "escalate this", "does this
  need GC sign-off", "route this for approval", or when another skill finds an issue
  that exceeds the reviewer's authority.
argument-hint: "[describe the issue, or reference a review memo]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:escalation-flagger

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If missing or has `[PLACEHOLDER]`, stop: "Run `/eu-legal:cold-start-interview` first."
2. Load `~/.claude/plugins/config/eu-legal/commercial.md` escalation section. If missing or has `[PLACEHOLDER]`, stop: "Run `/eu-legal:commercial-cold-start` first — I need your escalation matrix before routing."
3. Get the issue: from the user's description, or from a review memo referenced in the args.
4. Run the workflow below.

---

## Purpose

Names the right approver for a contract issue per the EUR escalation matrix in `commercial.md` and drafts the ask — in a form the approver can decide from without pulling up the contract.

---

## Step 1: Characterise the issue

What is being escalated?

- **EUR threshold:** Contract value exceeds someone's approval authority
- **Term deviation:** A term is outside the playbook fallbacks — someone more senior must decide whether to accept
- **Automatic EU trigger:** One of the always-escalate items (see below)
- **Business decision:** Not a legal call — needs the business owner

Do not escalate issues that are within the playbook's documented fallbacks. If the term is acceptable per `commercial.md`, it does not need to go up.

---

## Step 2: Check EU-specific automatic escalation triggers

These escalate regardless of EUR value. Check each:

| Trigger | Action |
|---|---|
| Any contract with cross-border data transfers outside the EEA (no adequacy decision, no SCCs, no BCRs) | Legal review required — GDPR Art. 44–49 |
| Any ICT third-party agreement for a financial entity (DORA in scope) | DORA compliance check required — route to `/eu-legal:vendor-agreement-review` if not yet run |
| Governing law outside the EU | Flag to legal — enforcement of EU rights (GDPR, DORA, TSD) may be impaired. Pre-approved exception: if the company's `commercial.md` playbook explicitly lists English law (England & Wales) as an accepted governing law choice, do not trigger this escalation for English-law contracts — the user has made a deliberate post-Brexit commercial choice. Flag only truly unexpected non-EU governing law (e.g., US law, Swiss law on a purely EU deal). |
| Liability cap below EUR [threshold from commercial.md] | Flag — potential exposure exceeds protected threshold |
| Any uncapped liability provision | Automatic escalation regardless of EUR value |
| Any IP assignment to the vendor | Automatic escalation — legal sign-off required |
| Any term on commercial.md "never accept" list | Automatic escalation |

Plus any additional triggers in `commercial.md` `escalation_auto_triggers`. Check the list from `commercial.md` and apply all of them.

---

## Step 3: Match to the EUR escalation matrix

```
Is the issue an automatic trigger?
  → YES: escalate to the named person for that trigger (from commercial.md)
  → NO: continue

Is the contract value above the reviewer's EUR threshold?
  → YES: escalate to whoever has authority at that EUR level (from commercial.md)
  → NO: continue

Is the term deviation outside all documented fallbacks?
  → YES: escalate to whoever can approve non-standard terms (from commercial.md)
  → NO: reviewer can approve — no escalation needed
```

---

## Step 4: Name the approver

Be specific. Not "escalate to legal leadership" — name the person or role from `commercial.md`. If the matrix doesn't name anyone for this situation: "The escalation matrix doesn't cover [situation]. Suggest asking [GC name or role from commercial.md] who owns this."

---

## Step 5: Draft the ask

The approver should be able to decide from the message alone.

```
**Escalating to:** [name or role from commercial.md]
**Via:** [Slack / email / meeting — from commercial.md]
**Urgency:** [deadline, if any]

---

Hey [name] —

Need your call on the [Counterparty] [agreement type]. [One sentence on deal context.]

**The issue:** [Plain language, one paragraph. What the contract says, why it's outside
our standard, what the actual risk is. EUR amounts throughout.]

**What the contract says:**
> "[exact quote]"

**What our playbook says:** [from commercial.md — the specific position violated]

**Applicable EU framework:** [DORA Art. 30 / GDPR Art. 28 / TSD Art. 4 / N/A] `[model knowledge — verify]`

**Options:**
1. **Accept** — [one line on why this might be okay]
2. **Push back with:** "[proposed counter-language]" — [one line on likely counterparty reaction]
3. **Walk** — [one line on whether that's realistic given the business context]

**My recommendation:** [which option and why, briefly]

**Need a decision by:** [date, if deadline exists]

[Link to full review memo]
```

---

## Calibration: when in doubt, escalate with a note

The cost of an unnecessary escalation is ~30 seconds of the approver's time. The cost of a missed escalation is signing an unapproved term. The costs are not symmetric. **When in doubt, escalate.**

If a term appears that `commercial.md` doesn't address, don't guess the threshold — ask the reviewing attorney whether this class of issue should escalate, and offer to record the answer in `commercial.md` so future reviews are consistent.

---

## What this skill does not do

- It does not approve anything. It routes.
- It does not decide between the options. The draft includes a recommendation but the approver decides.
- It does not send the escalation message — it drafts it. The lawyer sends it after reading.
- It does not apply US-specific thresholds or triggers. All amounts are in EUR.

---

## Disclaimer

Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
