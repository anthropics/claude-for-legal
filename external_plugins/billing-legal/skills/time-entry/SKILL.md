---
name: time-entry
disable-model-invocation: true
description: >
  Add a time entry manually — for work done outside a Claude Code session,
  corrections, or entries not captured by the billing panel. Use when logging
  time for a phone call, document review done in another tool, court appearance,
  or any billable work not associated with a Claude session.
argument-hint: "[--client <slug>] [--matter <slug>] [--date YYYY-MM-DD]"
---

# /billing-legal:time-entry

## When this runs

Attorney needs to log a time entry manually, outside of the end-of-session billing panel.

## Instructions

### 1. Read config

Read `~/.claude/plugins/config/claude-for-legal/billing/CLAUDE.md`. If `[PLACEHOLDER]` values are present, stop and direct to `/billing-legal:cold-start-interview`.

Get `billing_data_path` from config.

### 2. Determine which attorney

Check if any argument or context identifies the attorney. If not, read the attorney profiles in `[billing_data_path]/attorneys/` and ask: "Which attorney is this entry for?" (If only one attorney is configured, use them without asking.)

### 3. Collect entry details

Ask in sequence. Pre-fill from `$ARGUMENTS` if provided.

**Client:**
- If `--client <slug>` was passed and the client exists in `[billing_data_path]/clients/`, use it.
- Otherwise, list available clients (from `clients/*.yaml`) and ask which one.
- If the client doesn't exist yet, ask: "Client `[name]` isn't in the system yet. Create a profile now? [Y/n]". If yes, run a brief client intake (see "Creating a new client" below).

**Matter:**
- If `--matter <slug>` was passed, use it.
- Otherwise, ask: "What's the matter slug? (Leave blank if this entry isn't tied to a specific matter.)"

**Date:**
- If `--date YYYY-MM-DD` was passed, use it.
- Otherwise, default to today and confirm: "Date: [today] — correct? [Y/n]"

**Hours:**
- Ask: "How much time? (Enter as decimal hours like `0.8`, or as minutes like `48m`)"
- Convert minutes to hours: `minutes / 60`, then round UP to the next billing increment (from attorney's `billing_increment` setting, default 0.1h).
- Show the result: "That's [raw] — rounded to [rounded]h at [increment]-hour increments. Use [rounded]h? [Y/n]"

**Rate:**
- Look up the rate in order: client-specific override (from attorney YAML) → default rate (from attorney YAML).
- Show: "Rate: $[rate]/hr — is that right? [Y/n]"
- If billing arrangement is `flat-fee` or `no-charge`, show that instead of a rate prompt.

**Narrative (required):**
- Ask: "Describe the work — this will appear on the invoice."
- If the attorney submits a one-word or very short narrative (under 20 characters), gently push back: "Billing narratives should be descriptive enough for a client to understand what they're paying for. Can you add more detail? (e.g., 'Reviewed vendor NDA; drafted markup on confidentiality and IP ownership provisions.')"

**Task code (optional or required, per config):**
- If `Task codes: required`: ask "Task code (required):" — provide a quick reference:
  - L100 Case Assessment / Strategy
  - L110 Fact Investigation / Development
  - L120 Analysis / Strategy
  - L160 Settlement / Non-Binding ADR
  - L190 Other Case Assessment
  - L200 Pre-Trial Pleadings and Motions
  - L210 Complaint
  - L250 Other Written Motions / Submissions
  - L300 Discovery
  - L310 Written Discovery
  - L320 Document Production
  - L400 Trial Preparation and Trial
  - L500 Appeal
  - A100 Project Administration / Management
  - A103 Review / Analyze
  - A104 Draft / Revise
  - A105 Research
  - A106 Communicate (in firm)
  - A107 Communicate (other party)
- If `Task codes: optional`: ask with "(press enter to skip)"
- If `Task codes: hidden`: skip

**Notes:**
- Ask: "Any notes on this entry? (Internal use only — won't appear on invoice. Press enter to skip.)"
  
### 4. Anti-double-billing check

Before writing, read `time-register.yaml`. If the file is empty or contains only comment lines (starting with `#`), treat it as an empty list.

Scan for entries with all three of:
- Same `attorney`
- Same `client` and `matter_slug`
- Same `date`

If any such entry is found, warn:
> There is already a time entry for [attorney] on [client] / [matter] for [date]: "[existing narrative]" ([existing hours]h). Are you sure you want to add another entry? Verify this is not a duplicate before proceeding — double-billing is a professional ethics violation. [Y/n]

Note: the check is date-level only because entries do not store start or end times. If the attorney confirms, proceed — they may legitimately have multiple entries on the same date (e.g., a morning review session and an afternoon call).

### 5. Confirm and write

Show the entry summary:

```
Ready to log:
  Date:       [date]
  Attorney:   [name]
  Client:     [client name]
  Matter:     [matter slug or "not specified"]
  Hours:      [hours]h   →   $[amount] at $[rate]/hr
  Task code:  [code or "—"]
  Narrative:  [narrative]
  Notes:      [notes or "—"]
  Status:     pending

Log this entry? [Y/n]
```

On confirmation, generate an entry ID (`te-YYYY-MMDD-NNN` where NNN is zero-padded sequential for the day) and append a new top-level list item to `[billing_data_path]/time-register.yaml`. If the file is empty or comment-only, the first entry becomes the first list item. Each item starts with `- id:` at column 0:

```yaml
- id: te-[YYYY-MMDD]-[NNN]
  date: [YYYY-MM-DD]
  attorney: [slug]
  client: [slug]
  matter_slug: [slug or null]
  plugin: null
  hours: [hours]
  rate: [rate]
  amount: [hours * rate, rounded to 2 decimal places]
  task_code: [code or null]
  narrative: "[narrative]"
  status: pending
  invoice_id: null
  session_minutes_actual: null
  ai_cost_usd: null
  notes: "[notes or null]"
  activity_log: null
```

After writing, confirm:
> ✓ Logged: [hours]h for [client name] on [date] — status: pending (ID: [id])

### Creating a new client

When a client doesn't exist and the attorney confirms creating one:

Ask:
1. **Client display name** (how it appears on invoices)
2. **Slug** (suggest from name, confirm)
3. **Billing contact** (name + email; e.g., "Jane Smith \<jane@client.com\>")
4. **Billing address**
5. **Billing arrangement** (hourly | flat-fee | contingency | no-charge | courtesy) — default `hourly`
6. **Budget cap** (press enter for none)
7. **Retainer balance** (press enter for none)
8. **Notes** (e.g., "Prefers monthly invoices")

Write to `[billing_data_path]/clients/[slug].yaml`:

```yaml
slug: [slug]
name: [display name]
billing_contact: "[name] <[email]>"
billing_address: "[address]"
arrangement: [arrangement]
budget_cap: [number or null]
budget_billed: 0
retainer_balance: [number or null]
notes: "[notes or null]"
```

## What this skill does not do

- Generate invoices — use `/billing-legal:invoice-generate`
- Review pending entries — use `/billing-legal:wip-review`
- Set hourly rates — use `/billing-legal:rate-card`
