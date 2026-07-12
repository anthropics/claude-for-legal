---
name: billing-report
description: >
  Cross-client and cross-attorney billing reports — WIP summary, hours by client,
  attorney utilization, budget status across all matters, AI cost summary, and
  invoice history. Use for month-end review, partner reporting, client budget
  conversations, or firm-wide billing oversight.
argument-hint: "[--client <slug>] [--attorney <slug>] [--month YYYY-MM] [--wip] [--invoice <id>]"
---

# /billing-legal:billing-report

## When this runs

Attorney or billing manager wants a broad view of billing activity — not a single entry or a single invoice, but a summary across time periods, clients, or attorneys.

## Instructions

### 1. Read config

Read `~/.claude/plugins/config/claude-for-legal/billing/CLAUDE.md`. Get `billing_data_path`. Check for placeholders.

### 2. Dispatch on flag

Parse `$ARGUMENTS`. Default (no flags): show the WIP dashboard.

---

### `--wip` or default: WIP dashboard

Show all unbilled time (status `pending` or `approved`) across all clients and attorneys. This is the "what's in the pipeline" view.

```markdown
## WIP Dashboard — as of [today]

| Client | Attorney | Pending entries | Pending hours | Pending amount | Approved (ready to bill) |
|---|---|---|---|---|---|
| Acme Corp | Alice Jones | 3 | 2.4h | $840 | $420 |
| Beta LLP | Alice Jones | 1 | 1.0h | $350 | — |
| Gamma Inc | Bob Smith | 2 | 0.8h | $220 | $220 |

**Total WIP: [Nh]  ·  $[total]**
**Ready to invoice now: $[approved total] across [N] clients**

---

### Budget status (clients with a budget cap)

| Client | Budget cap | Billed to date | WIP | Total exposure | % used |
|---|---|---|---|---|---|
| Acme Corp | $15,000 | $6,400 | $840 | $7,240 | 48% |

⚠ [Client] — [pct]% of budget used (show clients ≥ 75%)
```

---

### `--client <slug>`: Client billing history

Show complete billing history for one client: all invoices issued, all WIP, all write-offs.

```markdown
## Billing History — [Client Name]

**Arrangement:** [hourly / flat-fee / etc.]
**Billing contact:** [name and email]

### Invoices issued

| Invoice | Period | Hours | Fees | Status |
|---|---|---|---|---|
| INV-2026-001 | Jan 2026 | 4.2h | $1,470 | issued |
| INV-2026-005 | Mar 2026 | 2.8h | $980 | issued |

**Total billed to date: [Nh]  ·  $[total]**

### WIP (unbilled)

| Date | Attorney | Hours | Amount | Status | Narrative |
|---|---|---|---|---|---|
| 2026-05-21 | Alice Jones | 0.8h | $280 | pending | Reviewed vendor MSA redline... |

**WIP: [Nh]  ·  $[total]**

### Write-offs

| Date | Attorney | Written-off hours | Written-off amount | Reason |
|---|---|---|---|---|
| 2026-04-10 | Alice Jones | 0.3h | $105 | Client relationship |

**Total written off: [Nh]  ·  $[total]**

### Budget summary

| | Value |
|---|---|
| Budget cap | $[cap] |
| Total billed | $[billed] |
| WIP | $[wip] |
| Total exposure | $[billed + wip] |
| Remaining budget | $[cap - exposure] |
| Budget used | [pct]% |
```

---

### `--attorney <slug>`: Attorney utilization summary

Show time logged by one attorney across all clients for the current month and year-to-date.

```markdown
## Billing Summary — [Attorney Name]

**This month ([YYYY-MM]):**

| Client | Matter | Hours | Amount | Status |
|---|---|---|---|---|
| Acme Corp | acme-msa-2026 | 1.2h | $420 | pending |
| Beta LLP | beta-nda-2026 | 0.6h | $210 | approved |

**Month total: [Nh]  ·  $[total]  (pending + approved)**
**Month billed: [Nh]  ·  $[total]  (status: billed)**

---

**Year-to-date ([YYYY]):**

| Month | Hours billed | Fees billed | Hours WIP | Fees WIP |
|---|---|---|---|---|
| Jan 2026 | 18.4h | $6,440 | — | — |
| Feb 2026 | 21.0h | $7,350 | — | — |
| ...

**YTD billed: [Nh]  ·  $[total]**
**YTD WIP:    [Nh]  ·  $[total]**

---

**AI cost summary (session tracking):**
*Total AI cost logged this month: $[amount] (for your reference — not billed to clients)*
```

---

### `--month YYYY-MM`: Monthly activity report

Show all billing activity in a given month across all attorneys and clients. Useful for month-end partner meetings.

```markdown
## Monthly Billing Report — [Month Year]

### Hours logged

| Client | Attorney | Hours | Fees | Status |
|---|---|---|---|---|

**Total: [Nh]  ·  $[total]**

### Invoices issued this month

| Invoice | Client | Hours | Fees |
|---|---|---|---|

**Total invoiced: $[total]**

### WIP generated this month (not yet billed)

**[Nh]  ·  $[total]**

### Write-offs this month

**[Nh]  ·  $[total]**

### AI cost this month (all sessions)

**$[total]** (for firm reference — not billed to clients)
```

---

### `--invoice <id>`: Invoice detail

Show the full content of a previously issued invoice — reconstructed from the time register. Useful for responding to client billing questions.

```markdown
## Invoice [id] — [Client Name]

[Reconstructed from time-register entries matching invoice_id: [id]]
[Same format as the invoice exhibit, without regenerating the file]
```

---

## What this skill does not do

- Generate or modify invoices — use `/billing-legal:invoice-generate` and `/billing-legal:wip-review`
- Send reports anywhere — outputs are in-conversation only; copy/paste to share
- Show reports for time before this plugin was installed — only entries in `time-register.yaml` are visible
