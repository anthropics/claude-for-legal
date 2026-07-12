---
name: billing-status
description: >
  Show the current billing state — active client, hours logged today, WIP for the
  active matter, and budget status. Also serves as the end-of-session billing panel
  when triggered by the Stop hook. Use when checking billing state, logging time at
  end of a session, or switching clients.
argument-hint: "[--session-end to show the end-of-session panel | --client <slug> to view a specific client]"
---

# /billing-legal:billing-status

## When this runs

Manually (`/billing-legal:billing-status`), or triggered by the Stop hook at end of session with `--session-end`. With `--client <slug>`, shows status for that client even if a different one is active.

## Instructions

### 1. Read config

Read `~/.claude/plugins/config/claude-for-legal/billing/CLAUDE.md`. If it has `[PLACEHOLDER]` values, say: "Billing setup isn't complete yet. Run `/billing-legal:cold-start-interview` first." Stop.

Get `billing_data_path` from the config.

### 2. Determine active client and matter

Check these sources in order (first match wins):

1. If `--client <slug>` was passed, use that client.
2. Check each installed plugin's active matter by reading its practice-level `CLAUDE.md` at `~/.claude/plugins/config/claude-for-legal/<plugin>/CLAUDE.md`. Check these plugins in order: `commercial-legal`, `ip-legal`, `corporate-legal`, `ai-governance-legal`, `product-legal`, `litigation-legal`. For each, look for a line matching the pattern `Active matter: <slug>` where `<slug>` is not the literal word `none` and not the phrase `none — practice-level context only`. The first non-none slug found is the active matter.
3. Once the active matter slug and plugin are known, read the matter's context file at `~/.claude/plugins/config/claude-for-legal/<plugin>/matters/<slug>/matter.md`. Parse the `**Client:**` line to get the client display name, and derive a client slug from it (lowercase-hyphenated). If `matter.md` is not found, use the matter slug itself as the client identifier.
4. Look up `[billing_data_path]/clients/<client-slug>.yaml`. If the file does not exist, proceed with the display name from `matter.md` and note in the panel that no billing profile exists for this client yet (offer to create one via `/billing-legal:time-entry`).

If no active matter is found and `--session-end` was passed, show a minimal panel asking which client to log against.

### 3. Determine session time and activity log (--session-end only)

When triggered with `--session-end`:

1. **Locate the session timer file.** Timer files live at `[billing_data_path]/.sessions/[attorney-slug]_[session-id]` — one file per session per attorney, so multiple attorneys sharing the same data path do not interfere.
   - When triggered by the Stop hook's block decision, the reason text contains `Session timer: [path]`. Extract the exact path from that context and use it.
   - When invoked manually (no path in context), scan `[billing_data_path]/.sessions/` for files matching `[active-attorney-slug]_*` (excluding `_activity` files) modified in the last 24 hours. Use the most recently modified.
   - If no file is found either way, prompt: "How long was this session? (Enter as hours like `0.8` or minutes like `48m`)" and hold `session_file = null`.
2. If a timer file was found, read its Unix timestamp, compute elapsed minutes, round UP to the next 0.1h increment:
   - 1–6 min → 0.1h
   - 7–12 min → 0.2h
   - 13–18 min → 0.3h
   - ... (ceiling division: `ceil(minutes / 6) × 0.1`)
3. **Load the activity log (if present).** Look for a file at `[timer-file-path]_activity` (same path as the timer file with `_activity` appended). If it exists, read all lines. Each line has the format `ISO8601_TIMESTAMP|TOOL_NAME|FILENAME`. Parse into a list of `{timestamp, tool, filename}` objects. Hold this list in memory as `session_activity`.
4. Hold the computed elapsed time, the session file path, and `session_activity` in memory. Do NOT delete either file yet — deletion happens only after a terminal decision (log or skip). Edit, switch-client, and cancel paths leave files intact so the Stop hook can re-prompt.

### 4. Look up today's entries and WIP

Read `[billing_data_path]/time-register.yaml`.

Compute:
- **Today's hours** for the active attorney on the active client (entries with today's date and matching attorney slug)
- **WIP total** for the active client: sum of `amount` for all entries where `status: pending` or `status: approved` (not yet billed)
- **Budget status**: read `budget_cap` and `budget_billed` from the client YAML; add WIP to `budget_billed` for the running total; compute percentage.
- **Today's AI cost**: not tracked per session — show `[not tracked]` unless the session-start hook captures it (future feature)

### 5. Display the billing panel

**Standard panel (no --session-end):**

```
┌─────────────────────────────────────────────────────────────┐
│  BILLING  [Client Name]  /  [matter-slug]                   │
│  Today: [N]h logged   WIP: $[N]   Rate: $[N]/hr             │
│  Budget: $[billed] of $[cap] ([pct]%)  [warning if ≥ 75%]   │
└─────────────────────────────────────────────────────────────┘
```

If there's no budget cap, omit the budget line.

If the client has `arrangement: flat-fee`, show: `[Flat fee matter — time tracked for records only]` instead of the rate and WIP dollar amounts.

**End-of-session panel (--session-end):**

```
┌─────────────────────────────────────────────────────────────────┐
│  SESSION BILLING  [Client Name]  /  [matter-slug]               │
│  Session: [actual min] min  →  [rounded]h (6-min increments)    │
│  [Attorney Name]  ·  $[rate]/hr  →  $[amount]                   │
│  Budget: $[billed] of $[cap] ([pct]%)  [⚠ if ≥ 75%]            │
│─────────────────────────────────────────────────────────────────│
│  Documents touched this session:                                │
│  · vendor-nda-redline.docx  (edited ×2)                         │
│  · acme-markup-notes.md  (created)                              │
│  · acme-msa-draft.docx  (read)                                  │
│─────────────────────────────────────────────────────────────────│
│  Describe the work (required for billing):                      │
│  >                                                              │
│─────────────────────────────────────────────────────────────────│
│  [log]  edit hours/rate  skip  switch client                    │
└─────────────────────────────────────────────────────────────────┘
```

The "Documents touched" section is shown only when `session_activity` is non-empty and `Activity logging: enabled` is set in config. Display rules:
- Show only the filename, not the full path
- Group by filename: if the same file appears multiple times with the same action, collapse to one line with a count (e.g., `(edited ×3)`)
- If a file appears under both Edit and Write, show as `(edited/created)`
- Sort: Edit first, then Write, then Read
- Cap at 8 lines; if more, show `+ [N] more documents`
- Purpose: helps the attorney write a specific, accurate narrative

Wait for the attorney's response:

- **User types a narrative + `log`** (or just types a narrative and presses enter): Ask for task code if `Task codes: required` or `optional` in config. If optional: "Task code? (L100/L200/etc., or press enter to skip)". Then write the entry directly (do not delegate to `/billing-legal:time-entry`, which is `disable-model-invocation`):
  1. Generate an entry ID: `te-YYYY-MMDD-NNN` (NNN = next sequential number for the day, zero-padded).
  2. Read `[billing_data_path]/time-register.yaml`; if the file is empty or comment-only, treat as an empty list.
  2a. **Duplicate check** — scan existing entries for any with the same `attorney`, `client`, `matter_slug`, and `date` (today). If found, warn before proceeding: "There is already a time entry for [attorney] on [client] / [matter] today: '[existing narrative]' ([existing hours]h). Is this a separate billable activity or a duplicate? [Continue / Cancel]" If the attorney cancels, return to the panel without deleting the session timer file.
  3. Append a new top-level list item at the end of the file (each item starts with `- id:` at column 0):
     ```yaml
     - id: [id]
       date: [YYYY-MM-DD]
       attorney: [attorney-slug]
       client: [client-slug]
       matter_slug: [matter-slug or null]
       plugin: [active-plugin or null]
       hours: [rounded-hours]
       rate: [rate]
       amount: [hours * rate, 2 decimal places]
       task_code: [code or null]
       narrative: "[narrative]"
       status: pending
       invoice_id: null
       session_minutes_actual: [actual-elapsed-minutes]
       ai_cost_usd: null
       notes: null
       activity_log: [compact activity list or null — see below]
     ```
     **Populating `activity_log`:** If `session_activity` is non-empty, write it as a YAML list of strings, one entry per unique filename (deduplicated). Each string: `"[YYYY-MM-DDTHH:MMZ]|[TOOL]|[filename]"` — use the timestamp of the first occurrence for each filename. Cap at 50 entries. If `session_activity` is empty or activity logging is disabled, write `activity_log: null`.
  4. Delete the session timer file (the specific `[billing_data_path]/.sessions/[attorney-slug]_[session-id]` path) and the corresponding activity log file (`[timer-file-path]_activity`) if it exists. If no file path was held (manual hour entry), do nothing.
- **User types `edit hours/rate`**: Ask which value to change, then re-display panel. Do NOT delete the session timer file.
- **User types `skip`**: Delete the session timer file (same path as above) and the `_activity` log file if it exists. Confirm "OK — session not logged. You can log it later with `/billing-legal:time-entry`."
- **User types `switch client`**: Ask which client, update the active client, and re-display the panel for the new client.

### 6. Budget warnings

If budget percentage ≥ 90%:
> ⛔ Budget: $[billed] of $[cap] — [pct]% used. [Client] is near the ceiling. Consider discussing a revised estimate before logging more time.

If budget percentage ≥ 75% but < 90%:
> ⚠ Budget: $[billed] of $[cap] — [pct]% used. Consider flagging this to the client.

### 7. After logging (session-end only)

After writing the time entry, show a brief confirmation:

> ✓ Logged: [hours]h to [Client Name] / [matter-slug] — status: pending
> Total WIP for [Client Name]: $[new WIP total]

Then stop. Do not offer to generate an invoice — that's for `/billing-legal:wip-review` and `/billing-legal:invoice-generate`.

## What this skill does not do

- Generate invoices — use `/billing-legal:invoice-generate`
- Review or approve pending entries — use `/billing-legal:wip-review`
- Show cross-client or cross-attorney reports — use `/billing-legal:billing-report`
