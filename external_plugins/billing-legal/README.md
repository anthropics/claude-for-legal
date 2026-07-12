# billing-legal

**A time tracking and billing plugin for the [claude-for-legal](https://github.com/anthropics/claude-for-legal) ecosystem.**

Attorneys spend billable time working inside Claude Code — reviewing contracts, drafting correspondence, researching matters. `billing-legal` captures that time automatically, associates it with the right client and matter, and generates printable invoice exhibits when billing period closes. It sits alongside your existing claude-for-legal plugins and follows the same file-based, config-driven architecture.

## Install

```
claude plugin install https://github.com/emtcmca/claude-for-legal-billing
```

Then run `/billing-legal:cold-start-interview` to set up.

---

## What it does

- **Automatic time capture** — An end-of-session panel appears after every Claude Code session when a matter is active. It shows the session duration (rounded up to 6-minute increments), the applicable rate, and prompts for a billing narrative before logging the entry.
- **Manual time entry** — Log time for work done outside Claude (phone calls, court appearances, document review in other tools).
- **Rate cards** — Per-attorney default rates, client-specific overrides, and billing arrangements (hourly, flat fee, contingency, no-charge, courtesy).
- **WIP pre-billing review** — Review, approve, write down, or write off pending entries before invoicing. Nothing goes on an invoice without attorney approval.
- **Invoice exhibits** — Generates a professional Markdown time-and-billing detail document to attach as supporting documentation to your client invoice. Handles retainer draw-down, budget tracking, and per-matter grouping.
- **Billing reports** — WIP dashboards, client billing history, attorney utilization, budget status, and AI cost summaries.
- **Budget warnings** — Panel warns at configurable thresholds (default 75% and 90%) when a client is approaching their budget cap.
- **Multi-attorney support** — All attorneys point to the same shared folder (OneDrive, network drive). Each attorney has their own rate card; the register is shared.
- **Billing digest agent** — On-demand agent surfaces outstanding WIP, stale entries, and budget alerts. Run manually with `/billing-legal:billing-summary`. For monthly automation, use Windows Task Scheduler to run `claude -p "/billing-legal:billing-summary"` — billing data is on the local filesystem and must be accessed by a local process, not a cloud routine.
- **LEDES 1998B export** — Generates a machine-readable LEDES 1998B file from any invoice for submission to corporate legal department e-billing systems (Serengeti, TyMetrix, Legal Tracker, and similar). Run `/billing-legal:ledes-export --invoice <id>` after generating an invoice exhibit.
- **Activity audit trail** — An optional PostToolUse hook silently logs which documents were edited, created, or read during each session. At billing time, the session panel shows you the files touched to help write a specific narrative. The log is stored in the time register entry and can be included in invoice exhibits as a collapsed audit trail section — providing the evidence of AI-assisted work that billing reviewers increasingly require.

---

## Requirements

- **Claude Code** (claude.ai/code or VS Code/JetBrains extension)
- **claude-for-legal** ecosystem — at minimum one legal plugin installed (commercial-legal, ip-legal, corporate-legal, etc.). [Installation instructions here.](https://github.com/anthropics/claude-for-legal)
- The plugin reads active matter context from your other claude-for-legal plugins. It works standalone, but it's most useful when you're also using matter workspaces.

---

## Installation

### Step 1 — Copy the plugin files

Copy the `billing-legal` folder into your claude-for-legal plugin directory. There are two ways to do this depending on how your other plugins are installed.

**If you have the claude-for-legal source repository:**

```powershell
# In PowerShell, from your claude-for-legal directory:
git clone https://github.com/[your-username]/billing-legal billing-legal
```

Or download the ZIP from GitHub and extract it into your `claude-for-legal` folder so the structure is:

```
claude-for-legal/
├── commercial-legal/
├── ip-legal/
├── billing-legal/      ← the new folder goes here
│   ├── .claude-plugin/
│   │   ├── plugin.json
│   │   └── config-template.md
│   ├── skills/
│   ├── agents/
│   └── hooks/
```

**If you installed claude-for-legal via the plugin cache only:**

Copy the `billing-legal` folder to:
```
C:\Users\[your-username]\.claude\plugins\cache\claude-for-legal\billing-legal\1.0.0\
```

### Step 2 — Register the plugin with Claude Code

The plugin is identified by `.claude-plugin/plugin.json`. Register it using the Claude Code CLI from inside the `billing-legal` folder:

```powershell
claude plugin install .
```

This writes the plugin to `enabledPlugins` in your `~/.claude/settings.json`, which is the supported install path for Claude Code plugins.

If the CLI command isn't available in your version of Claude Code, add the plugin manually to `~/.claude/settings.json`:

```json
{
  "enabledPlugins": [
    "path/to/claude-for-legal/billing-legal"
  ]
}
```

> To verify registration: open a new Claude Code session and type `/billing-legal:cold-start-interview`. If Claude doesn't recognize the command, the path in `enabledPlugins` doesn't point to the folder containing `.claude-plugin/plugin.json` — double-check the path.

### Step 3 — Run setup

In a new Claude Code session, run:

```
/billing-legal:cold-start-interview
```

This is the only command you need. The interview takes 10–15 minutes and sets up everything:

- Firm name and billing address (pre-populated from your company-profile.md if other plugins are installed)
- Where to store billing data (local or shared folder)
- Attorney profiles and hourly rates
- Invoice numbering and prefix
- Task code preferences (required, optional, or hidden)
- The end-of-session billing panel

You'll also see a one-time ethics notice about billing for AI-assisted work — the plugin prompts you to verify your state bar's guidance before using it for client billing.

---

## Multi-attorney setup (law firms)

For firms with multiple attorneys:

**Step 1 — Designate a shared billing folder.** Choose a location all attorneys can access: a shared OneDrive folder, a network drive, or a SharePoint-synced directory. For example:
```
C:\Users\[name]\OneDrive - FirmName\Billing\claude-for-legal\billing\
```

**Step 2 — First attorney runs cold-start.** The first attorney to set up the plugin configures the shared folder path. This creates the `attorneys/`, `clients/`, and register files in the shared location.

**Step 3 — Additional attorneys run cold-start, point to the same path.** Each subsequent attorney runs `/billing-legal:cold-start-interview` on their own machine. When asked for the billing data location, they enter the same shared folder path used in Step 2. Their attorney profile is added to the shared `attorneys/` folder.

**Important:** Two attorneys should not log time simultaneously if they're writing to the same YAML file within the same second. In practice this is rare — but for firms with very high concurrency needs (5+ attorneys billing simultaneously), a database-backed solution is a better fit than the file-based approach.

---

## Using the plugin

### The end-of-session billing panel

The main way time gets captured. If you enabled it during cold-start, it appears automatically at the end of each Claude Code session when a legal matter is active.

Example:

```
┌─────────────────────────────────────────────────────────────────┐
│  SESSION BILLING  Acme Corp  /  acme-msa-2026                   │
│  Session: 46 min  →  0.8h (rounded up to 6-min)                 │
│  Alice Jones  ·  $350/hr  →  $280.00                            │
│  Budget: $6,400 of $15,000  (43% used)                          │
│─────────────────────────────────────────────────────────────────│
│  Describe the work (required for billing):                      │
│  > Reviewed vendor MSA redline; drafted markup on limitation    │
│    of liability and IP ownership clauses.                        │
│─────────────────────────────────────────────────────────────────│
│  [log]  edit hours/rate  skip  switch client                    │
└─────────────────────────────────────────────────────────────────┘
```

Type your narrative and press **log** to save. Type **skip** if the session wasn't billable. Type **switch client** if the wrong client is shown.

The panel only fires when a legal matter is active (i.e., you've run a skill like `/commercial-legal:matter-workspace switch acme-msa-2026`). If no matter is active, the panel is suppressed.

### Switching clients

**Automatic:** When you switch matters in another plugin (e.g., `/commercial-legal:matter-workspace switch new-client-nda`), billing auto-detects the new client if "Auto-detect active matter" is enabled.

**Manual:** Run `/billing-legal:billing-status --client [slug]` to see the status for a specific client, or type **switch client** inside the billing panel.

### Logging time manually

For time spent outside Claude Code — phone calls, in-person meetings, court appearances, or work in other tools:

```
/billing-legal:time-entry
```

The skill walks you through selecting the client, matter, date, hours, rate, and narrative. It also checks for potential double-billing: if the same attorney already has an entry for the same client, matter, and date, you'll be warned before the entry is saved. The check is date-level — entries do not store start/end times, so overlap detection within a day is not possible.

**Entering hours:**
- As decimal hours: `0.8` (48 minutes)
- As minutes: `48m` (automatically converted and rounded up to 6-min increment)

### Setting and updating rates

```
/billing-legal:rate-card list                         # See all configured rates
/billing-legal:rate-card set --attorney alice-jones   # Update Alice's default rate
/billing-legal:rate-card override --attorney alice-jones --client acme-corp  # Client-specific rate
/billing-legal:rate-card override --client beta-llp   # Update a client's billing arrangement
```

**Billing arrangements:**

| Arrangement | Billing panel behavior | Invoice shows |
|---|---|---|
| `hourly` (default) | Shows hours × rate = amount | Hours, rate, amount |
| `flat-fee` | Tracks time; no dollar math | Hours (flat fee noted) |
| `contingency` | Tracks time; $0 rate | Hours (contingency noted) |
| `no-charge` | Panel suppressed | Not billed |
| `courtesy` | Tracks time; notes courtesy status | Hours (not billed) |

### Reviewing and approving time entries

Before generating an invoice, review pending entries:

```
/billing-legal:wip-review --client acme-corp
```

For each entry you can:
- **Approve** — marks it ready to invoice
- **Write down** — reduce hours or amount (requires a reason)
- **Write off** — zero it out entirely (not billed; stays in records)
- **Edit** — correct the narrative, task code, date, or attorney

Nothing moves to an invoice without explicit approval here.

### Generating invoice exhibits

After approving entries via `wip-review`:

```
/billing-legal:invoice-generate acme-corp
/billing-legal:invoice-generate acme-corp --period 2026-05          # Just May 2026
/billing-legal:invoice-generate acme-corp --matter acme-msa-2026    # One matter only
```

This generates a Markdown file at:
```
[billing_data_path]/invoices/INV-2026-007.md
```

The file is formatted as **supporting documentation** to attach to your primary client invoice. It includes:

- Firm header and client billing info
- Itemized time entries grouped by matter
- Hours and fees per matter with subtotals
- Grand total
- Retainer balance (if applicable)
- A note that it's supporting detail, not the invoice itself

**To print or share:** Open the `.md` file in VS Code, any Markdown editor, or paste it into Word. VS Code can export to PDF via a Markdown PDF extension. The formatting is clean enough to copy directly into most billing systems.

**Example output:**

```markdown
# Time & Billing Detail
## Supporting Documentation — Invoice INV-2026-007

**Hartley & Associates LLP**
123 Main St, Suite 400, Columbus, OH 43215
billing@hartley.law

---

**Client:** Acme Corp
**Attention:** Jane Smith <jane@acme.com>
**Invoice:** INV-2026-007
**Invoice Date:** 2026-06-01
**Billing Period:** May 1 – May 31, 2026

---

## Time Entries

### acme-msa-2026 — Acme Corp (Vendor MSA Review)

| Date | Attorney | Description | Code | Hours | Rate | Amount |
|---|---|---|---|---|---|---|
| 2026-05-21 | Alice Jones | Reviewed vendor MSA redline; drafted markup on limitation of liability and IP ownership | L200 | 0.8h | $350/hr | $280.00 |
| 2026-05-23 | Alice Jones | Call with client re: counterparty response; revised markup | L200 | 0.4h | $350/hr | $140.00 |

**Matter subtotal: 1.2h · $420.00**

---

## Summary

| | Hours | Amount |
|---|---|---|
| **Total billable time** | **1.2h** | **$420.00** |
| Retainer on file | | $2,500.00 |
| Less: this invoice | | ($420.00) |
| **Retainer balance after invoice** | | **$2,080.00** |
```

### Billing reports

```
/billing-legal:billing-report                          # WIP dashboard (all clients)
/billing-legal:billing-report --client acme-corp       # Full history for one client
/billing-legal:billing-report --attorney alice-jones   # Utilization summary
/billing-legal:billing-report --month 2026-05          # All activity in May 2026
/billing-legal:billing-report --invoice INV-2026-007   # Review a specific invoice
```

### Checking current status

```
/billing-legal:billing-status                          # Quick status for active client
/billing-legal:billing-status --client acme-corp       # Status for a specific client
```

---

## Data structure

All user data lives at the billing data path configured during cold-start (default `~/.claude/plugins/config/claude-for-legal/billing/`). For firms using a shared folder, this path is set to the shared location.

```
[billing_data_path]/
├── attorneys/
│   ├── alice-jones.yaml       # Attorney profile: name, email, default rate, overrides
│   └── bob-smith.yaml
├── clients/
│   ├── acme-corp.yaml         # Client profile: billing contact, arrangement, budget
│   └── beta-llp.yaml
├── .sessions/
│   ├── alice-jones_abc123     # Per-session timer: [attorney-slug]_[session-id]
│   └── alice-jones_abc123_activity  # Activity log for the same session (if enabled)
│                              # Both created by hooks, deleted on log/skip
├── time-register.yaml         # All time entries — append-only, never delete
├── invoice-register.yaml      # Index of issued invoices
└── invoices/
    ├── INV-2026-001.md        # Invoice exhibit — printable Markdown
    ├── INV-2026-001.ledes     # LEDES 1998B export (generated on demand)
    └── INV-2026-002.md
```

**The time register is append-only.** Entries are never deleted — they can be written off (set to $0) but the record stays. This is intentional: billing records are financial documents and should be preserved.

**Attorney profile example** (`attorneys/alice-jones.yaml`):

```yaml
slug: alice-jones
name: Alice Jones
email: alice@firm.com
default_rate: 350
billing_increment: 0.1    # 0.1 = 6-minute minimum; 0.2 = 12-minute
timekeeper_id: aj001      # used in LEDES exports; falls back to slug if absent
timekeeper_classification: AT  # AT=attorney, PA=paralegal, OF=of counsel, CL=clerk
rate_overrides:
  acme-corp: 325
```

**Client profile example** (`clients/acme-corp.yaml`):

```yaml
slug: acme-corp
name: Acme Corp
billing_contact: Jane Smith <jane@acme.com>
billing_address: 456 Corporate Blvd, Anytown, OH 44001
arrangement: hourly
budget_cap: 15000
budget_billed: 6820
retainer_balance: 1680
ledes_client_id: ACME-001  # client's ID in their e-billing system; falls back to slug
notes: Prefers monthly invoices. Budget warning at 75%.
```

**Time register entry example**:

```yaml
- id: te-2026-0521-001
  date: 2026-05-21
  attorney: alice-jones
  client: acme-corp
  matter_slug: acme-msa-2026
  plugin: commercial-legal
  hours: 0.8
  rate: 350
  amount: 280.00
  task_code: L200
  narrative: Reviewed vendor MSA redline; drafted markup on limitation of liability and IP ownership clauses.
  status: billed
  invoice_id: INV-2026-007
  session_minutes_actual: 46
  ai_cost_usd: 0.14
  notes: null
  activity_log:
    - "2026-05-21T14:23Z|Edit|vendor-nda-redline.docx"
    - "2026-05-21T14:31Z|Write|acme-markup-notes.md"
    - "2026-05-21T14:45Z|Read|acme-msa-background.pdf"
```

---

## LEDES 1998B Export

Many corporate legal departments and insurance companies require invoices in LEDES 1998B format for their e-billing systems. After generating an invoice exhibit with `/billing-legal:invoice-generate`, run:

```
/billing-legal:ledes-export --invoice INV-2026-007
```

This generates a `.ledes` file at `[billing_data_path]/invoices/INV-2026-007.ledes`. You can also export by client and period without a finalized invoice:

```
/billing-legal:ledes-export --client acme-corp --period 2026-05
```

### Setting up LEDES identifiers

Most e-billing systems require specific IDs that match their internal records. Set these once — they're stored in your attorney and client YAML files.

**Timekeeper ID and classification (per attorney):**
```
/billing-legal:rate-card set --attorney alice-jones
```
- **Timekeeper ID:** your firm-assigned ID or bar number (falls back to attorney slug if not set)
- **Timekeeper classification:** AT (attorney), PA (paralegal), OF (of counsel), CL (law clerk)

**LEDES client ID (per client):**
```
/billing-legal:rate-card override --client acme-corp
```
- **LEDES client ID:** the ID the client uses in their e-billing system (e.g., `ACME-001`). Falls back to the client slug uppercased if not set.

### LEDES format overview

The output is a pipe-delimited plain text file following the LEDES 1998B spec:

```
LEDES1998B[]
INVOICE_DATE|INVOICE_NUMBER|CLIENT_ID|...|TIMEKEEPER_CLASSIFICATION[]
20260601|INV-2026-007|ACME-001|...|AT[]
20260601|INV-2026-007|ACME-001|...|AT[]
```

Write-off entries are excluded (zero-dollar lines are not valid in LEDES format). Flat-fee entries are included with their tracked hours.

---

## Activity Audit Trail

Billing reviewers for AI-assisted work increasingly require evidence that the time was genuinely spent on the matter. The activity audit trail provides this.

### How it works

When activity logging is enabled, a lightweight PostToolUse hook silently records every file that was edited, created, or read during a session. At the end of the session, the billing panel shows you the list:

```
┌─────────────────────────────────────────────────────────────────┐
│  SESSION BILLING  Acme Corp  /  acme-msa-2026                   │
│  Session: 46 min  →  0.8h                                       │
│  Alice Jones  ·  $350/hr  →  $280.00                            │
│─────────────────────────────────────────────────────────────────│
│  Documents touched this session:                                │
│  · vendor-nda-redline.docx  (edited ×2)                         │
│  · acme-markup-notes.md  (created)                              │
│  · acme-msa-background.pdf  (read)                              │
│─────────────────────────────────────────────────────────────────│
│  Describe the work (required for billing):                      │
│  > Reviewed vendor NDA redline; drafted markup on...            │
└─────────────────────────────────────────────────────────────────┘
```

The document list helps you write a specific, accurate narrative. It's also stored in the time register entry as `activity_log`.

### Audit trail in invoice exhibits

When `Activity log on invoice: enabled` is set, a collapsed audit trail section is included in the invoice `.md` file after each matter's time entries:

```markdown
<details>
<summary>AI session activity — audit trail</summary>

| Time | Action | Document |
|---|---|---|
| 2026-05-21 14:23 | Edited | vendor-nda-redline.docx |
| 2026-05-21 14:31 | Created | acme-markup-notes.md |

</details>
```

The `<details>` block keeps it accessible without cluttering the invoice. Most Markdown renderers (GitHub, VS Code, browser-based viewers) render it as a collapsed section that clients or reviewers can expand.

### Privacy note

The activity log stores only filenames (not full paths) in the time register. It never records file contents. The log is stored locally in `[billing_data_path]/.sessions/` during the session and moved to the time register entry when time is logged. It is deleted from `.sessions/` on log or skip.

### Enabling activity logging

Enable it during cold-start setup, or run `/billing-legal:customize` to toggle it on. The hook is registered in your Claude Code `settings.json` alongside the existing billing hooks.

---

## UTBMS Task Codes

If task codes are enabled (required or optional), use these standard codes:

| Code | Description |
|---|---|
| **Case assessment** | |
| L100 | Case Assessment / Strategy |
| L110 | Fact Investigation / Development |
| L120 | Analysis / Strategy |
| L160 | Settlement / Non-Binding ADR |
| L190 | Other Case Assessment |
| **Pleadings & motions** | |
| L200 | Pre-Trial Pleadings and Motions |
| L210 | Complaint / Petition |
| L250 | Other Written Motions / Submissions |
| **Discovery** | |
| L300 | Discovery |
| L310 | Written Discovery |
| L320 | Document Production |
| **Trial** | |
| L400 | Trial Preparation and Trial |
| L500 | Appeal |
| **Project / transactional** | |
| A100 | Project Administration |
| A103 | Review / Analyze |
| A104 | Draft / Revise |
| A105 | Research |
| A106 | Communicate (internal) |
| A107 | Communicate (other party) |

For transactional work (contract review, drafting, deal support), the A-series codes are typically more appropriate than the L-series.

---

## Ethics and AI billing

The cold-start interview surfaces a one-time notice, but it's worth repeating here:

Many state bars and the ABA have issued guidance on billing clients for time spent with AI tools. Before using this plugin for client billing, verify your jurisdiction's current position. The key questions courts and disciplinary bodies ask:

1. Was the time genuinely spent on the client's matter?
2. Is the rate reasonable given the AI assistance provided?
3. Were efficiency gains passed through to the client?

The ABA's formal opinions are at [americanbar.org](https://www.americanbar.org). This plugin does not constitute legal advice, and the developer makes no representation about compliance with any bar's billing rules.

---

## Command reference

| Command | What it does |
|---|---|
| `/billing-legal:cold-start-interview` | First-time setup |
| `/billing-legal:cold-start-interview --redo` | Re-run full setup |
| `/billing-legal:billing-status` | Show active client status |
| `/billing-legal:billing-status --session-end` | Trigger end-of-session panel manually |
| `/billing-legal:billing-status --client <slug>` | Show status for specific client |
| `/billing-legal:time-entry` | Log time manually |
| `/billing-legal:rate-card list` | View all rates |
| `/billing-legal:rate-card set --attorney <slug>` | Update attorney rate |
| `/billing-legal:rate-card override --attorney <slug> --client <slug>` | Client-specific rate |
| `/billing-legal:rate-card override --client <slug>` | Update client arrangement/budget |
| `/billing-legal:wip-review` | Review pending entries (active client) |
| `/billing-legal:wip-review --client <slug>` | Review entries for specific client |
| `/billing-legal:wip-review --all` | Review all pending entries firm-wide |
| `/billing-legal:invoice-generate <slug>` | Generate invoice exhibit |
| `/billing-legal:invoice-generate <slug> --period YYYY-MM` | Invoice for one month |
| `/billing-legal:billing-report` | WIP dashboard |
| `/billing-legal:billing-report --client <slug>` | Client history |
| `/billing-legal:billing-report --attorney <slug>` | Attorney utilization |
| `/billing-legal:billing-report --month YYYY-MM` | Monthly activity |
| `/billing-legal:billing-report --invoice <id>` | Review issued invoice |
| `/billing-legal:ledes-export --invoice <id>` | Export invoice to LEDES 1998B format |
| `/billing-legal:ledes-export --client <slug> --period YYYY-MM` | Export by client and period |
| `/billing-legal:customize` | Change one setting |

---

## Billing workflow (end-to-end)

```
Work on matter in Claude Code
        ↓
[Activity log hook records file operations silently]
        ↓
Session ends → billing panel appears
  (shows documents touched to help write narrative)
        ↓
Type narrative → [log]
        ↓
Entry saved to time-register.yaml (status: pending)
  activity_log stored with the entry
        ↓
[End of billing period]
        ↓
/billing-legal:wip-review --client [slug]
  → approve / write down / write off
        ↓
/billing-legal:invoice-generate [slug]
        ↓
invoices/INV-YYYY-NNN.md created
  (includes collapsed audit trail if enabled)
        ↓
Copy into your billing system / attach to client invoice
        ↓
[If client requires e-billing submission]
        ↓
/billing-legal:ledes-export --invoice INV-YYYY-NNN
        ↓
invoices/INV-YYYY-NNN.ledes → upload to client's e-billing portal
```

---

## Moving billing data to a shared folder later

If you start solo and later want to move to a shared folder:

1. Copy your existing billing data folder to the new shared location
2. Run `/billing-legal:customize`
3. Update the "Data path" to the new shared path
4. Each other attorney runs `/billing-legal:cold-start-interview` on their machine and enters the same shared path

---

## Migrating to a database (when the firm outgrows the shared folder)

The YAML structure is designed for straightforward migration to Supabase or another database:

- Each `time-register.yaml` entry maps 1:1 to a row in a `time_entries` table
- `attorney`, `client`, and `matter_slug` become foreign key columns
- `invoices/*.md` files become rows in a `billing_documents` table
- The `id` field (`te-YYYY-MMDD-NNN`) is already a unique identifier

A migration script can read the YAML and bulk-insert to the database with no data loss. The schema is stable — entries written today will import cleanly later.

---

## Contributing

Pull requests welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. The plugin follows the architecture conventions of the claude-for-legal ecosystem — all skills are SKILL.md instruction files, config lives in `~/.claude/plugins/config/claude-for-legal/billing/`, and data structures are defined in this README and in the individual SKILL.md files.

---

## License

MIT. See [LICENSE](LICENSE) for terms.

---

## Author

Built by [Eric Tetzlaff](https://github.com/emtcmca) as an extension to the claude-for-legal ecosystem.
