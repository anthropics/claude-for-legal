---
name: wip-review
disable-model-invocation: true
description: >
  Review, edit, and approve pending time entries before invoicing — the pre-billing
  step. Use when preparing to send an invoice, doing end-of-month billing review,
  writing down or writing off entries, or auditing unbilled WIP across matters.
argument-hint: "[--client <slug>] [--attorney <slug>] [--matter <slug>] [--all]"
---

# /billing-legal:wip-review

## When this runs

Attorney is preparing to invoice a client (or doing a general billing audit) and needs to review, approve, write down, or write off pending entries.

## Instructions

### 1. Read config

Read `~/.claude/plugins/config/claude-for-legal/billing/CLAUDE.md`. Get `billing_data_path`. Check for placeholders.

### 2. Determine scope

Parse `$ARGUMENTS`:
- `--client <slug>`: show only entries for that client
- `--attorney <slug>`: show only entries for that attorney
- `--matter <slug>`: show only entries for that matter slug
- `--all`: show all pending and approved entries across all clients and attorneys

If no arguments, default to: entries for the currently active matter's client (same detection logic as `/billing-legal:billing-status`). If no active matter, show all pending entries.

### 3. Load entries

Read `[billing_data_path]/time-register.yaml`. Filter to entries with `status: pending` or `status: approved` matching the scope.

If no entries match: "No pending entries found for [scope]. Run `/billing-legal:time-entry` to add entries, or check a different scope."

### 4. Display the WIP table

Show the entries in a clean table, grouped by client, then by matter, then sorted by date:

```markdown
## WIP Review — [Client Name]  (filter: [scope])

**Total pending: [N] entries  |  [Nh]  |  $[total]**

### [Matter slug] — [Matter description if known]

| # | Date | Attorney | Hrs | Rate | Amount | Code | Narrative | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-05-21 | Alice Jones | 0.8h | $350 | $280 | L200 | Reviewed vendor MSA redline... | pending |
| 2 | 2026-05-23 | Alice Jones | 0.4h | $350 | $140 | L200 | Call with client re: counterparty... | pending |

**Subtotal: 1.2h — $420**

---

### [Next matter or "No matter assigned"]

...

---

**Grand total: [Nh] — $[total]**
```

### 5. Action menu

After displaying the table, show:

```
What would you like to do?
  a  Approve all pending entries
  [N]  Act on entry #[N] (approve, write down, write off, edit)
  d  Done — exit review
```

Wait for input.

---

### Action: Approve all

Set all `pending` entries in scope to `approved`. Confirm the count before writing:
> Approve [N] entries totaling [Nh] / $[total]? [Y/n]

After writing: "✓ [N] entries approved — ready for invoice generation via `/billing-legal:invoice-generate [client-slug]`."

---

### Action: Act on entry #N

Show the full entry and offer:

```
Entry #[N]:  [date]  [attorney]  [hours]h  $[amount]  [narrative]

  a  Approve — move to approved
  w  Write down — reduce hours or amount
  x  Write off — zero out (write-off, not billed)
  e  Edit — correct narrative, task code, date, or attorney
  b  Back
```

**Approve:** Set `status: approved`. Show updated table row.

**Write down:**
- Ask: "Write down to what? (Enter new hours, or enter a dollar amount)"
- If hours: recalculate amount at the existing rate.
- If dollar amount: recalculate hours at the existing rate (for records).
- Show the change: `[original] → [new]`
- Ask for a write-down note (stored in `notes` field): "Reason for write-down: (required)"
- Confirm and write. Set `status: approved` after write-down.

**Write off:**
- Ask: "Write-off reason: (required — e.g., 'Client relationship', 'Billing error', 'Included in flat fee')"
- Set `hours: 0`, `amount: 0.00`, `status: write-off`, `notes: "[reason] — written off [date]"`.
- Confirm before writing. Written-off entries remain in the register for records but never appear on invoices.

**Edit:**
- Ask which field to change: narrative, task code, date, attorney, hours, rate.
- For hours/rate: warn that changing these on an approved entry requires a write-down note.
- For narrative: no restriction — corrections to descriptions are routine.
- Show the change and confirm before writing.

---

### 6. Exit

When the attorney types `d` (done) or has finished acting on entries, show a summary:

```markdown
## WIP Review Summary

Approved:   [N] entries  [Nh]  $[total]
Written down: [N] entries  (reduced by $[amount])
Written off:  [N] entries  (removed $[amount])
Still pending: [N] entries

Ready to invoice: [N] entries for [Client(s)] — run `/billing-legal:invoice-generate [client-slug]`
```

---

## What this skill does not do

- Generate invoices — use `/billing-legal:invoice-generate`
- Delete entries — entries are never deleted; write-off is the closest equivalent
- Handle entries that are already `billed` — those are closed; contact billing counsel if a billed entry needs correction
