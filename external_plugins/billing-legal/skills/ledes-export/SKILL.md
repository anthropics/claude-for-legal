---
name: ledes-export
description: >
  Export a billing invoice to LEDES 1998B format for submission to corporate
  legal department e-billing systems. Use after generating an invoice exhibit
  with invoice-generate, when a client's legal ops team requires LEDES format
  for their matter management or e-billing platform.
argument-hint: "--invoice <id> | --client <slug> [--period YYYY-MM]"
---

# /billing-legal:ledes-export

## When this runs

An invoice has been generated and the client requires LEDES 1998B format for their e-billing system. This is common for corporate legal departments, insurance companies, and large institutional clients.

## Instructions

### 1. Read config

Read `~/.claude/plugins/config/claude-for-legal/billing/CLAUDE.md`. Check for placeholders — if present, stop and direct to `/billing-legal:cold-start-interview`.

Get:
- `billing_data_path`
- `Firm name`
- `LEDES export` setting — if `disabled`, warn: "LEDES export is disabled in your billing config. Enable it with `/billing-legal:customize` or set `LEDES export: enabled` in your billing CLAUDE.md. Proceeding anyway — you can always run this skill directly."
- `Default timekeeper classification`

### 2. Resolve scope

Parse `$ARGUMENTS`:

**`--invoice <id>`** (preferred): Load the invoice record from `[billing_data_path]/invoice-register.yaml` where `id: [id]`. Get `period_start`, `period_end`, `client`, `entry_ids`, `total_fees`, `date`.

If no matching invoice found: "Invoice [id] not found in invoice-register.yaml. Check `/billing-legal:billing-report --invoice [id]` or use `--client` to export by client and period."

**`--client <slug> [--period YYYY-MM]`**: Read `[billing_data_path]/time-register.yaml`. Filter to entries with `client: [slug]` and `status: billed` (or `approved` if `--period` is used without a finalized invoice). If `--period` is supplied, restrict to entries in that month.

If neither argument is provided: list clients that have billed or approved entries and ask which one to export.

### 3. Load entries and attorney profiles

From `time-register.yaml`, load all entries matching the resolved scope. Exclude entries with `status: write-off` — zero-dollar lines are not valid in LEDES format.

For each unique attorney slug in the entries, read `[billing_data_path]/attorneys/[slug].yaml`. Get:
- `name`
- `timekeeper_id` (fall back to attorney slug if field is absent)
- `timekeeper_classification` (fall back to `Default timekeeper classification` from config, then `AT`)

Read `[billing_data_path]/clients/[client-slug].yaml`. Get:
- `name`
- `ledes_client_id` (fall back to client slug uppercased, with hyphens replaced by underscores, e.g., `acme-corp` → `ACME_CORP`)

### 4. Compute dates

All dates in LEDES 1998B are formatted `YYYYMMDD` (no separators).

- `INVOICE_DATE`: use `date` from invoice record, or today's date if exporting outside a finalized invoice
- `BILLING_START_DATE`: earliest entry date in scope, formatted YYYYMMDD
- `BILLING_END_DATE`: latest entry date in scope, formatted YYYYMMDD

If loaded from an invoice record, use `period_start` and `period_end` instead of computing from entries.

### 5. Compute write-down adjustment per entry

LEDES requires `LINE_ITEM_ADJUSTMENT_AMOUNT` — the amount reduced from the original billing through a write-down. The time register does not store original hours separately, so:

- Check `notes` field for the pattern "written down" or "write-down". If present, the entry was reduced.
- Compute `LINE_ITEM_ADJUSTMENT_AMOUNT` = 0.00 for entries with no write-down (the common case).
- For entries that were written down: the current `amount` is already the post-write-down figure. If the original amount is inferable from notes (e.g., "written down from 1.2h"), use it. Otherwise use 0.00 — LEDES reviewers care more about the final amount than the adjustment.

### 6. Build the LEDES 1998B file

LEDES 1998B format rules:
- Line 1: `LEDES1998B[]` (literal, no spaces)
- Line 2: pipe-delimited column headers, ending with `[]`
- Lines 3+: one data row per time entry, pipe-delimited, ending with `[]`
- No trailing newline after the last `[]`
- All numeric amounts formatted with exactly 2 decimal places (e.g., `280.00`)
- Dates formatted YYYYMMDD
- Pipe characters in narrative text must be replaced with a space

**Column order (fixed — do not reorder):**

```
INVOICE_DATE|INVOICE_NUMBER|CLIENT_ID|LAW_FIRM_MATTER_ID|INVOICE_TOTAL|BILLING_START_DATE|BILLING_END_DATE|INVOICE_DESCRIPTION|LINE_ITEM_NUMBER|EXP/FEE/INV_ADJ_TYPE|LINE_ITEM_TASK_CODE|LINE_ITEM_EXPENSE_CODE|LINE_ITEM_ACTIVITY_CODE|TIMEKEEPER_ID|TIMEKEEPER_NAME|LINE_ITEM_NUMBER_OF_UNITS|LINE_ITEM_ADJUSTMENT_AMOUNT|LINE_ITEM_TOTAL|LINE_ITEM_DESCRIPTION|LAW_FIRM_MATTER_ID|TIMEKEEPER_CLASSIFICATION
```

**Field values per row:**

| Column | Value |
|---|---|
| INVOICE_DATE | Invoice date, YYYYMMDD |
| INVOICE_NUMBER | Invoice ID (e.g., `INV-2026-007`) |
| CLIENT_ID | `client.ledes_client_id` or slug uppercased |
| LAW_FIRM_MATTER_ID | `entry.matter_slug` (or empty string if null) |
| INVOICE_TOTAL | Sum of all entry amounts in this export, 2 decimal places — same value on every row |
| BILLING_START_DATE | Period start, YYYYMMDD |
| BILLING_END_DATE | Period end, YYYYMMDD |
| INVOICE_DESCRIPTION | `Legal Services — [Firm Name]` |
| LINE_ITEM_NUMBER | Sequential integer starting at 1 |
| EXP/FEE/INV_ADJ_TYPE | `F` (fee — for all time entries) |
| LINE_ITEM_TASK_CODE | `entry.task_code` or empty string |
| LINE_ITEM_EXPENSE_CODE | (empty) |
| LINE_ITEM_ACTIVITY_CODE | (empty) |
| TIMEKEEPER_ID | `attorney.timekeeper_id` or attorney slug |
| TIMEKEEPER_NAME | `attorney.name` |
| LINE_ITEM_NUMBER_OF_UNITS | `entry.hours` (decimal, e.g., `0.80`) |
| LINE_ITEM_ADJUSTMENT_AMOUNT | Write-down delta or `0.00` |
| LINE_ITEM_TOTAL | `entry.amount`, 2 decimal places |
| LINE_ITEM_DESCRIPTION | `entry.narrative` (pipe chars replaced with spaces) |
| LAW_FIRM_MATTER_ID | `entry.matter_slug` again (LEDES spec repeats this column) |
| TIMEKEEPER_CLASSIFICATION | `attorney.timekeeper_classification` |

**Example output:**

```
LEDES1998B[]
INVOICE_DATE|INVOICE_NUMBER|CLIENT_ID|LAW_FIRM_MATTER_ID|INVOICE_TOTAL|BILLING_START_DATE|BILLING_END_DATE|INVOICE_DESCRIPTION|LINE_ITEM_NUMBER|EXP/FEE/INV_ADJ_TYPE|LINE_ITEM_TASK_CODE|LINE_ITEM_EXPENSE_CODE|LINE_ITEM_ACTIVITY_CODE|TIMEKEEPER_ID|TIMEKEEPER_NAME|LINE_ITEM_NUMBER_OF_UNITS|LINE_ITEM_ADJUSTMENT_AMOUNT|LINE_ITEM_TOTAL|LINE_ITEM_DESCRIPTION|LAW_FIRM_MATTER_ID|TIMEKEEPER_CLASSIFICATION[]
20260601|INV-2026-007|ACME_CORP|acme-msa-2026|420.00|20260501|20260531|Legal Services — Hartley & Associates LLP|1|F|L200|||aj001|Alice Jones|0.80|0.00|280.00|Reviewed vendor MSA redline; drafted markup on limitation of liability and IP ownership|acme-msa-2026|AT[]
20260601|INV-2026-007|ACME_CORP|acme-msa-2026|420.00|20260501|20260531|Legal Services — Hartley & Associates LLP|2|F|L200|||aj001|Alice Jones|0.40|0.00|140.00|Call with client re counterparty response; revised markup|acme-msa-2026|AT[]
```

### 7. Write the file

Write to `[billing_data_path]/invoices/[invoice-id].ledes`.

If exporting without a finalized invoice (--client + --period), use the filename `[client-slug]-[YYYY-MM].ledes`.

### 8. Confirm

```
✓ LEDES 1998B export written:
   File:     [billing_data_path]/invoices/[filename].ledes
   Entries:  [N] line items
   Total:    $[total]
   Client:   [Client Name]  (CLIENT_ID: [ledes_client_id])
   Period:   [start] – [end]

Write-off entries excluded: [N]  (zero-dollar lines are not valid in LEDES format)

To submit: attach this file to your e-billing portal upload.
To view: open in any text editor — it's pipe-delimited plain text.

Tip: if the client's system rejects the file, verify the CLIENT_ID matches
what their e-billing system expects. Update it with:
  /billing-legal:rate-card override --client [slug]
```

---

## Notes on LEDES 1998B compatibility

LEDES 1998B is the most widely accepted variant. A few edge cases:

- **No task code:** Some e-billing systems require LINE_ITEM_TASK_CODE. If entries are missing task codes, the upload may be rejected. Consider enabling `Task codes: required` in your billing config.
- **Timekeeper ID:** Many corporate clients map timekeeper IDs to their own records. Set `timekeeper_id` on attorney profiles to match the ID your client has on file, via `/billing-legal:rate-card set --attorney [slug]`.
- **Client ID:** Corporate clients often assign their own matter/client IDs. Set `ledes_client_id` on the client profile to match, via `/billing-legal:rate-card override --client [slug]`.
- **Flat-fee matters:** LEDES line items require a unit count and line total. For flat-fee entries, hours are logged but amounts are $0 (or the flat amount divided across entries). The export will include these as-is.

---

## What this skill does not do

- Submit the file to any e-billing system — this is a file export only
- Generate the primary invoice — use `/billing-legal:invoice-generate` first
- Validate against a specific client's LEDES configuration — contact the client's legal ops team for their field requirements
