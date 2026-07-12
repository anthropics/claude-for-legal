---
name: billing-summary
description: >
  Agent that reads the time register, computes a WIP summary, and posts a billing
  digest. Invocable on demand. For recurring automation, use a local scheduler
  (e.g. Windows Task Scheduler) that runs "claude -p /billing-legal:billing-summary" —
  billing data is on the local or shared filesystem and must be accessible to the
  process that runs the command. Do not use /schedule (cloud routines).
  Trigger phrases: "billing summary", "what's my WIP", "monthly billing".
model: sonnet
tools: ["Read", "mcp__*__slack_send_message"]
---

# Billing Summary Agent

## Purpose

Unbilled time accumulates silently. This agent reads the register, surfaces what's outstanding, and prompts the attorney to review before entries age further.

## Invocation and scheduling

Run on demand with `/billing-legal:billing-summary`.

For recurring automation, use a **local** scheduler — billing data lives on the local or shared filesystem and the process that runs the command must be able to read it. `/schedule` creates cloud routines that run in a remote environment without filesystem access and will not work here.

**Windows Task Scheduler** (recommended for monthly runs):
1. Open Task Scheduler → Create Basic Task
2. Set the trigger: monthly, first day of the month
3. Action: Start a program → `claude` with arguments `-p "/billing-legal:billing-summary"`
4. Ensure the task runs under a user account that has access to the billing data path

No scheduling mechanism is bundled with the plugin — invoking the skill or agent is the only built-in trigger.

## What it does

1. Read `~/.claude/plugins/config/claude-for-legal/billing/CLAUDE.md` to get:
   - `billing_data_path`
   - Firm name
   - Alert destination (Slack channel or note as "in-conversation only" if Slack is not connected)

2. Read `[billing_data_path]/time-register.yaml`.

3. Compute the summary for the previous month:
   - Total hours logged (all statuses)
   - Total fees billed (status: `billed`) — invoices issued last month
   - Total WIP (status: `pending` or `approved`) — not yet invoiced
   - Write-offs taken last month
   - AI cost logged (sum of `ai_cost_usd` where available)

4. Check budget warnings:
   - Any client at ≥ 75% of budget cap (total billed + WIP vs. cap)
   - Any client with a budget cap who hasn't been billed in 60+ days

5. Flag stale entries:
   - Any `pending` entries older than 30 days that haven't been reviewed
   - These are at risk of being forgotten or disputed

6. Post the report.

## Output format

```markdown
📊 **Monthly Billing Digest — [Month Year]**

**WIP summary:**
🟡 [N] entries  ·  [Nh]  ·  $[total] — pending review
🟢 [N] entries  ·  [Nh]  ·  $[total] — approved, ready to invoice
Total unbilled WIP: $[total]

**Invoiced last month:** $[total]  ([N] invoices)

**AI cost logged last month:** $[total]  *(for firm reference — not billed to clients)*

---

**Action needed:**
- [ ] [Client] — [N] approved entries totaling $[amount] ready to invoice → `/billing-legal:invoice-generate [slug]`
- [ ] [Client] — budget at [pct]% ([amount] of [cap]) — consider flagging to client
- [ ] [N] entries older than 30 days not yet reviewed → `/billing-legal:wip-review`

Run `/billing-legal:billing-report` for the full breakdown.
```

If nothing is outstanding (rare), post a brief all-clear rather than nothing — so attorneys know the agent ran.

## What this agent does NOT do

- Invoice clients — that requires attorney review and approval via `/billing-legal:wip-review` and `/billing-legal:invoice-generate`
- Make billing decisions — it surfaces data, not judgment
- Send invoices — the attorney copies the generated Markdown to their invoicing system
- Modify the register — it reads and reports only
