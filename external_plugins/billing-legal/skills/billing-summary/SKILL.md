---
name: billing-summary
description: >
  Run the billing digest — surface outstanding WIP, stale entries, and budget
  alerts across all clients and attorneys. Use when you want a quick billing
  health check, at the start of each month before invoicing, or any time you
  want to know what's unbilled. Trigger phrases: "billing summary",
  "what's my WIP", "monthly billing", "billing health check".
argument-hint: "[--month YYYY-MM to scope to a specific month]"
---

# /billing-legal:billing-summary

Runs the same analysis as the billing-summary agent but as an on-demand slash command. For automated monthly runs, use Windows Task Scheduler (or your OS equivalent) to run `claude -p "/billing-legal:billing-summary"` on a local process that can access the billing data path. Do not use `/schedule` — that feature runs cloud routines without access to your local or shared filesystem.

## Instructions

### 1. Read config

Read `~/.claude/plugins/config/claude-for-legal/billing/CLAUDE.md`. Get `billing_data_path`. If `[PLACEHOLDER]` values are present, stop: "Run `/billing-legal:cold-start-interview` first."

### 2. Determine scope

If `--month YYYY-MM` was passed, scope all calculations to that month. Otherwise use the previous full calendar month as the primary period, plus a running total of all current WIP regardless of age.

### 3. Compute the summary

Read `[billing_data_path]/time-register.yaml`. If empty or comment-only, report "No entries in the register yet."

Compute for the period (and all-time WIP where noted):

- **Entries logged this period** — all entries with a date in the period, any status
- **Invoiced this period** — entries with `status: billed` and `invoice_id` pointing to an invoice issued in the period (cross-reference `invoice-register.yaml`)
- **Current WIP (all time)** — entries with `status: pending` or `status: approved` across all dates
- **Write-offs this period** — entries with `status: write-off` and date in the period
- **AI cost this period** — sum of `ai_cost_usd` where non-null and date in period

Check for:
- **Stale pending entries** — `status: pending` with date older than 30 days (at risk of aging out or being disputed)
- **Budget warnings** — clients where `budget_billed + WIP ≥ 75%` of `budget_cap`
- **Clients with approved entries** — ready to invoice now

### 4. Post the report

```markdown
## Billing Digest — [Month or "as of today"]

**WIP summary:**
🟡 [N] pending entries  ·  [Nh]  ·  $[total]
🟢 [N] approved entries  ·  [Nh]  ·  $[total] — ready to invoice

**[Period] invoiced:** $[total]  ([N] invoices)

**AI cost [period]:** $[total]  *(firm reference — not billed to clients)*

---

**Action needed:**
- [ ] [Client] — [N] approved entries totaling $[amount] ready to invoice → `/billing-legal:invoice-generate [slug]`
- [ ] [Client] — budget at [pct]% ($[amount] of $[cap]) — consider flagging to client
- [ ] [N] entries older than 30 days not reviewed → `/billing-legal:wip-review`

Run `/billing-legal:billing-report` for the full breakdown.
```

If nothing is outstanding, say so explicitly — an all-clear is useful information.

## What this skill does not do

- Modify the register — it reads and reports only
- Invoice clients — use `/billing-legal:wip-review` then `/billing-legal:invoice-generate`
- Replace `/billing-legal:billing-report` — this is a digest; billing-report gives the full per-client and per-attorney breakdown
