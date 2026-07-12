---
name: invoice-generate
disable-model-invocation: true
description: >
  Generate a printable invoice exhibit from approved time entries for a client.
  Produces a Markdown file formatted as supporting documentation to attach to a
  client invoice. Use when billing period closes and entries have been approved
  in wip-review.
argument-hint: "<client-slug> [--period YYYY-MM to YYYY-MM] [--matter <slug>]"
---

# /billing-legal:invoice-generate

## When this runs

Billing period has closed. Entries have been reviewed and approved via `/billing-legal:wip-review`. Attorney is ready to generate a supporting invoice document.

## Instructions

### 1. Read config

Read `~/.claude/plugins/config/claude-for-legal/billing/CLAUDE.md`. Get:
- `billing_data_path`
- `Firm name`
- `Billing address`
- `Billing email`
- `Invoice prefix`
- `Next invoice number`
- `Task codes` setting

### 2. Determine scope

Parse `$ARGUMENTS`:
- First token: required `<client-slug>`
- `--period YYYY-MM` or `--period YYYY-MM to YYYY-MM`: restrict to entries in that month or range (default: all approved entries for the client)
- `--matter <slug>`: restrict to one matter

If no `client-slug` provided: list clients with approved entries and ask which one.

### 3. Load entries and client info

Read `[billing_data_path]/time-register.yaml`. Filter to:
- `client: [client-slug]`
- `status: approved`
- Within the period if `--period` was specified

If no entries match: "No approved entries found for [client] in this period. Run `/billing-legal:wip-review` first to approve pending entries."

Read `[billing_data_path]/clients/[slug].yaml` for:
- `name` (display name)
- `billing_contact`
- `billing_address`
- `arrangement`
- `budget_cap`, `budget_billed`, `retainer_balance`

### 4. Determine invoice number

Read `[billing_data_path]/invoice-register.yaml`. Find the highest existing invoice number for the current year. Assign the next sequential number: `[prefix]-[YYYY]-[NNN]` (zero-padded 3 digits, e.g., `INV-2026-007`).

### 5. Confirm before generating

Show a pre-invoice summary:

```
Ready to generate Invoice [number]

Client:     [Client Name]
Period:     [date range or "All approved entries"]
Entries:    [N] entries
Total hours: [Nh]
Total fees:  $[total]
Arrangement: [arrangement]

Retainer balance (before this invoice): $[balance]
Retainer balance (after this invoice):  $[balance - fees]

Continue? [Y/n]  (or 'wip' to go back to WIP review)
```

If retainer balance would go negative, warn:
> ⚠ This invoice exceeds the retainer balance by $[overage]. Client will owe the balance on net payment terms.

### 6. Generate the invoice exhibit

Write the invoice to `[billing_data_path]/invoices/[invoice-number].md`:

```markdown
---
invoice: [invoice-number]
client: [client-slug]
date: [YYYY-MM-DD]
period_start: [YYYY-MM-DD]
period_end: [YYYY-MM-DD]
total_hours: [Nh]
total_fees: [amount]
status: issued
---

# Time & Billing Detail
## Supporting Documentation — Invoice [invoice-number]

**[Firm Name]**
[Billing Address]
[Billing Email]

---

**Client:** [Client Display Name]
**Attention:** [billing_contact name]
**Billing Address:** [billing_address]

**Invoice:** [invoice-number]
**Invoice Date:** [YYYY-MM-DD]
**Billing Period:** [period start] – [period end]

---

## Time Entries

[Group by matter slug. For each matter group:]

### [Matter slug] — [Client name] ([matter description if available])

| Date | Attorney | Description | Code | Hours | Rate | Amount |
|---|---|---|---|---|---|---|
| [date] | [name] | [narrative] | [code or —] | [hours]h | $[rate]/hr | $[amount] |

**Matter subtotal: [Nh]  ·  $[amount]**

---

[Next matter group...]

---

## Summary

| | Hours | Amount |
|---|---|---|
| **Total billable time** | **[Nh]** | **$[total]** |
[If there were write-downs:]
| Write-downs (not billed) | [Nh] | ($[written-down-amount]) |

[If retainer:]
| Retainer on file | | $[retainer_balance] |
| Less: this invoice | | ($[total]) |
| **Retainer balance after invoice** | | **$[balance]** |

---

*This document is supporting detail for Invoice [invoice-number]. Payment terms and remittance instructions are on the invoice. Questions: [billing_email].*

*Prepared [date] · [Firm Name]*
```

**Omit the `Code` column entirely if `Task codes: hidden` is set in config.**

**For flat-fee matters:**
- Include the time entries table (client may want to see the work performed)
- Replace the amount column with "— (flat fee)"
- Summary section shows hours but no dollar total; instead: "Flat fee arrangement — see invoice for amount"

**For contingency matters:**
- Include time entries with $0 rate
- Note: "Contingency matter — fees contingent on outcome"

### 7. Add activity audit trail (if enabled)

Check config for `Activity log on invoice: enabled`. If enabled:

For each matter group in the invoice, collect all `activity_log` entries from the time register entries in that group (skip entries where `activity_log` is null). If any exist, append a collapsed audit section immediately after the matter's time entries table:

```markdown
<details>
<summary>AI session activity — audit trail</summary>

| Time | Action | Document |
|---|---|---|
| [YYYY-MM-DD HH:MM] | [Edit/Write/Read] | [filename] |

</details>
```

Parse each activity log entry (format: `ISO8601_TIMESTAMP|TOOL_NAME|FILENAME`). Convert timestamp to `YYYY-MM-DD HH:MM` in local time. Sort by timestamp ascending. Deduplicate: if the same file appears more than once with the same action, collapse to one row and note the count, e.g., `vendor-nda.docx (×3)`.

The `<details>` block keeps the audit trail accessible without cluttering the invoice exhibit. Most Markdown renderers (GitHub, VS Code, browser-based viewers) render it as a collapsed section.

If `Activity log on invoice: disabled` (or the setting is absent from config), skip this step entirely.

### 9. Update registers

**Update invoice-register.yaml** — append:
```yaml
- id: [invoice-number]
  client: [client-slug]
  date: [YYYY-MM-DD]
  period_start: [YYYY-MM-DD]
  period_end: [YYYY-MM-DD]
  total_hours: [N]
  total_fees: [amount]
  entry_ids: [[list of te-* ids]]
  status: issued
```

**Update time-register.yaml** — for each included entry, change `status: approved` → `status: billed` and set `invoice_id: [invoice-number]`.

**Update client YAML** — add invoice total to `budget_billed`. If retainer: subtract from `retainer_balance`.

**Update CLAUDE.md** — increment `Next invoice number` by 1.

### 10. Confirm and close

> ✓ Invoice [invoice-number] generated:
>    File: [billing_data_path]/invoices/[invoice-number].md
>    Entries marked billed: [N]
>    Total: $[amount]
>
> To print or share: open the file and copy/paste into Word, or convert to PDF with any Markdown-to-PDF tool.
>
> To view: `/billing-legal:billing-report --invoice [invoice-number]`
>
> LEDES export: if your client requires LEDES 1998B format for their e-billing system, run:
>   `/billing-legal:ledes-export --invoice [invoice-number]`

---

## What this skill does not do

- Send invoices — attorney copies the Markdown to their invoicing system or email
- Interface with accounting software — the Markdown is designed for copy/paste
- Generate the primary invoice (letterhead, payment terms) — this document is supporting detail; the attorney creates the primary invoice in their billing system
- Delete or undo issued invoices — contact billing counsel if a correction is needed after issuance
