---
name: customize
description: >
  Guided customization of your billing practice profile — change one thing without
  re-running the whole cold-start interview. Adjust rates, billing data path, invoice
  settings, panel behavior, attorney profiles, client profiles, or task code
  preferences. Use when the user says "change my [thing]", "update my rate",
  "edit my billing config", "add a client", or "customize".
argument-hint: "[section name, or describe what you want to change]"
---

# /billing-legal:customize

## When this runs

The user wants to change something in their billing configuration without re-running the full cold-start interview.

## Instructions

### 1. Read config

Read `~/.claude/plugins/config/claude-for-legal/billing/CLAUDE.md`. Get `billing_data_path`. If `[PLACEHOLDER]` values are present, stop:
> You haven't run setup yet. Run `/billing-legal:cold-start-interview` first — customize is for adjusting a profile you already have.

### 2. Show the customizable map

List what can be changed, with current values:

```
Billing profile — customizable settings:

Firm info
  • Firm name: [current]
  • Billing address: [current]
  • Billing email: [current]
  • Remittance instructions: [current]

Invoices
  • Invoice prefix: [current]  (e.g., INV-2026-001)
  • Next invoice number: [current]
  • Task codes: [required / optional / hidden]

Panel & automation
  • End-of-session billing panel: [enabled / disabled]
  • Auto-detect active matter: [enabled / disabled]
  • Budget warning threshold: [pct]%

Billing data
  • Data path: [current path]  (change to move to/from shared folder)

Attorneys — [N configured]
  • [attorney name]: $[rate]/hr, [increment]h increment
  • [Run /billing-legal:rate-card to manage rates and overrides]

Clients — [N configured]
  • [Run /billing-legal:rate-card --client <slug> to manage client settings]

What would you like to change?
```

### 3. Make the change

On user input, identify the section and field. Show the current value, ask for the new value, explain what changes downstream, confirm, write it.

**Common changes and their downstream effects:**

- **Billing data path:** Moving to a shared folder. Confirm: "I'll update the config to point to [new path]. You'll need to manually move your existing `attorneys/`, `clients/`, `time-register.yaml`, and `invoices/` directory to the new path. Do that before your next time entry. Confirm the path change? [Y/n]"

- **Invoice prefix:** "New entries will use the new prefix. Existing invoices keep their original prefix — this won't retroactively renumber them."

- **Task codes required → optional:** "Future time entries won't require a task code, but existing entries and invoices aren't changed."

- **Budget warning threshold:** "The billing panel will warn at [new pct]% of a client's budget cap going forward."

- **Disabling the billing panel:** "The end-of-session prompt will no longer appear. You'll need to run `/billing-legal:billing-status` or `/billing-legal:time-entry` manually to log time. I'll remove both the Stop hook and the UserPromptSubmit hook from your settings.json — leaving either in place would keep creating timer files in `.sessions/` or producing stale block decisions. Want me to remove both? [Y/n]"

- **Enabling the billing panel (was disabled):** Walk through the hook setup (same as cold-start Phase 6).

### 4. For shared-profile changes

If the user wants to change the firm name or address, note: "Firm name is shared with other claude-for-legal plugins via `company-profile.md`. I'll update it there so the change flows everywhere. Confirm? [Y/n]"

### 5. Close

> Done. Your next output will reflect the change. Run `/billing-legal:customize` anytime to adjust.

---

## Guardrails

- Never delete an attorney or client profile — if they want to "remove" someone, set their status to `inactive` and explain what that means
- Never renumber issued invoices — the `Next invoice number` only affects future invoices
- Flag if a rate change would affect already-pending (but not yet approved) entries: "You have [N] pending entries for [client] at the old rate. Do you want to update those to the new rate, or keep them at the rate they were logged at? (Best practice: keep them as logged)"
