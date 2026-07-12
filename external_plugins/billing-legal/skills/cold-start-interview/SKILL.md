---
name: cold-start-interview
description: >
  Run the cold-start interview to set up your billing practice profile — firm info,
  attorney profiles, hourly rates, billing data location, and panel preferences.
  Use on first install when the profile is missing or still contains placeholders,
  or when re-onboarding with --redo, or when re-checking settings with --check.
  This is the ONLY skill that should run on a fresh install.
argument-hint: "[--redo to start over | --check to review current settings]"
---

# /billing-legal:cold-start-interview

## When this runs

First time (no config exists), `--redo` (re-run fully), or `--check` (review without changing). With `--redo`, confirm before overwriting anything.

## What to do

### Phase 0: Preflight

1. Check for `~/.claude/plugins/config/claude-for-legal/billing/CLAUDE.md`. If it exists and has no `[PLACEHOLDER]` markers and no `--redo` flag, say:

   > Your billing profile is already configured. Run `/billing-legal:cold-start-interview --redo` to start over, or `/billing-legal:customize` to change one thing.

   Then stop.

2. Check for `~/.claude/plugins/config/claude-for-legal/company-profile.md`. If it exists, read the firm name and address from there to pre-fill relevant fields. If it doesn't exist, create it at the end of this interview (the billing plugin creates a minimal version; the full version comes from other claude-for-legal plugins).

---

### Phase 1: Ethics flag (show once, always first)

Before anything else, display this — even if they've seen it before on a `--redo`:

> **A note on billing for AI-assisted work**
>
> Many state bars and the ABA have issued guidance on billing clients for time spent with AI tools. The key questions: Was the time genuinely spent on the client's matter? Is the rate reasonable given the assistance the AI provided? Were any efficiency gains passed through to the client?
>
> Before using this module for client billing, verify your bar's current guidance. The ABA's formal opinions are at americanbar.org. If you're outside the US, check your jurisdiction's professional conduct regulator.
>
> This plugin tracks time and generates supporting documentation. It does not make billing decisions — that's the attorney's professional responsibility.

Ask: "Understood — ready to continue? [Y/n]". If no, stop without writing anything.

---

### Phase 2: Firm info

Ask these questions in sequence. Show each current value if re-doing.

1. **Firm name:** (if company-profile.md exists, offer to use that name — "Use [name from company-profile.md]?")
2. **Billing address:** (full mailing address for invoices)
3. **Billing email:** (the from/reply-to on invoices)
4. **Remittance instructions:** (e.g., "Net 30. Checks payable to [firm]. ACH available on request." — suggest a default)
5. **Invoice prefix:** (default `INV` — appears in invoice numbers like `INV-2026-001`)
6. **Starting invoice number:** (default `001` — increment is tracked in the data)

---

### Phase 3: Billing data location

> Where should billing data live? For solo use, the default is your local config folder. For firm use with shared access, you can point to a shared OneDrive or network folder — all attorneys at the firm need to point to the same path.

Ask:
- **Solo (local)** → default `~/.claude/plugins/config/claude-for-legal/billing/` (expand to full path for Windows: `C:/Users/[username]/.claude/plugins/config/claude-for-legal/billing/`)
- **Shared folder** → ask for the path, e.g., `C:/Users/[name]/OneDrive/Firm Billing/claude-for-legal/billing/`

Note: *When using a shared folder, each attorney runs this cold-start on their own machine but points to the same shared data path. Attorney profiles and client profiles are created in that shared folder on first run; subsequent attorneys can add themselves.*

Verify the path exists or confirm creation.

---

### Phase 4: Attorney profiles

> Tell me about the attorney(s) using this module. Start with yourself — you can add others after setup, or right now.

For each attorney, ask:
1. **Name** (full name as it should appear on invoices)
2. **Email** (for attorney identification in multi-attorney reports)
3. **Slug** (suggest lowercase-hyphenated from name, e.g., `alice-jones` — confirm)
4. **Default hourly rate** (USD per hour; this is the rate used unless a client-specific override is set)
5. **Billing increment** (6-minute / 0.1h is standard; some firms use 0.2h — default `0.1`)

After the first attorney, ask: "Are there other attorneys at your firm using this? [Y/n]"
If yes, repeat. If no, continue.

Write each attorney to `[billing_data_path]/attorneys/[slug].yaml`.

Then ask: "Which of these attorney profiles is yours on this machine?" (List the slugs just configured, plus any already in `[billing_data_path]/attorneys/`.) This sets `**Active attorney:**` in the config — the session timer hooks use it to key timer files by attorney, so multiple attorneys sharing the same billing folder do not interfere with each other.

---

### Phase 5: Task codes

> UTBMS task codes are industry-standard billing codes used by many firms and clients (L100 Case Assessment, L200 Pleadings, L300 Discovery, etc.). Using them makes invoices more professional and easier for clients to process.

Options:
- **Required** — every time entry must include a task code
- **Optional** — prompted but not required (default)
- **Hidden** — don't ask; omit from invoices

---

### Phase 5.5: LEDES export

> Many corporate legal departments and insurance companies require invoices in LEDES 1998B format for their e-billing systems (Serengeti, TyMetrix, Legal Tracker, etc.). Enable LEDES export to generate a machine-readable file alongside your invoice exhibits.

Ask: "Enable LEDES 1998B export? [Y/n]"

If yes:
- Set `LEDES export: enabled` in the config.
- Ask: "Default timekeeper classification for attorneys at your firm? (AT = attorney, PA = paralegal, OF = of counsel, CL = law clerk — default: AT)"
- Write `Default timekeeper classification: [answer]` to the config.
- For each attorney profile just created, add `timekeeper_classification: [default]` to their YAML unless the attorney specified a different one.
- Say: "LEDES export enabled. To set a client-specific LEDES client ID (what their e-billing system calls your firm), run `/billing-legal:rate-card override --client [slug]` after setup. To set a timekeeper ID for a specific attorney (for clients who map to their own IDs), run `/billing-legal:rate-card set --attorney [slug]`."

If no:
- Set `LEDES export: disabled` in the config.
- Say: "You can enable it later with `/billing-legal:customize`."

---

### Phase 6: Billing panel

> The billing panel appears at the end of each Claude Code session when a matter is active. It shows how long the session ran, the rounded billable time, and a prompt to log the entry. This is the core time-capture mechanism.

> To activate the automatic end-of-session panel, I need to add a hook to your Claude Code settings. This adds one line to `~/.claude/settings.json` (or your project `.claude/settings.json`).

Ask: "Enable the end-of-session billing panel? [Y/n]"

If yes:
- Ask whether to configure it in **user settings** (`~/.claude/settings.json`) — applies to all projects — or **project settings** (`.claude/settings.json` in the current directory) — applies to this project only.
- Determine the target settings.json path. Read it if it exists; create it with `{"hooks":{}}` if not.
- Copy `billing-stop.ps1` and `session-start.ps1` from the plugin cache into the billing config hooks directory: `[billing_data_path]/hooks/`. This ensures the scripts survive plugin updates.
- Add two hooks to the settings.json `hooks` object (preserving any existing hooks):
  - A `Stop` hook with command: `powershell -NoProfile -NonInteractive -File "[billing_data_path]/hooks/billing-stop.ps1"`
  - A `UserPromptSubmit` hook with command: `powershell -NoProfile -NonInteractive -File "[billing_data_path]/hooks/session-start.ps1"`
- Then ask: "Enable activity logging? This adds a lightweight hook that silently records which documents were opened or edited during each session. At billing time, the panel shows you the files touched so you can write a more specific narrative — and the log is attached to the time entry for audit purposes. The log is stored locally and only included in invoice exports if you choose. [Y/n]"
- If activity logging yes:
  - Copy `activity-log.ps1` from the plugin cache into `[billing_data_path]/hooks/`.
  - Add a `PostToolUse` hook: `powershell -NoProfile -NonInteractive -File "[billing_data_path]/hooks/activity-log.ps1"`
  - Ask: "Include the activity log in invoice exhibits as a collapsed audit trail section? [Y/n]"
  - Set `Activity logging: enabled` and `Activity log on invoice: [enabled|disabled]` in the config.
- If activity logging no:
  - Set `Activity logging: disabled` and `Activity log on invoice: disabled` in the config.
- Show the user the exact additions to settings.json and confirm before writing.
- After writing: "The billing panel is now active. At the end of each session Claude will prompt you to log time. The session timer starts on your first message. You can disable it anytime with `/billing-legal:customize`."

If no: "You can always run `/billing-legal:billing-status` manually to log time."

---

### Phase 7: Auto-detect active matter

> When you open a matter in another claude-for-legal plugin (like `/commercial-legal:matter-workspace switch acme-corp`), billing can automatically switch to that client so you don't have to do it twice.

Ask: "Enable automatic matter detection? [Y/n]" (default yes)

If yes, this writes `Auto-detect active matter: enabled` to the config. Skills will check the active matter from other plugins' CLAUDE.md files when they run.

---

### Phase 8: Budget warning threshold

Ask: "At what percentage of a client's budget cap should the billing panel warn you? (Default: 75%)"

---

### Phase 9: Write config and confirm

Write `~/.claude/plugins/config/claude-for-legal/billing/CLAUDE.md` with all values filled in. Use `.claude-plugin/config-template.md` as the structural reference for section names and placeholder markers. Show the user a summary before writing and ask for confirmation.

Create the following directories under the billing data path if they don't exist:
- `attorneys/`
- `clients/`
- `invoices/`

Create `time-register.yaml` if it doesn't exist. Write only these comment lines — no YAML keys or empty lists:
```yaml
# Billing time register — append only. Do not edit entries after they are billed.
# Format: top-level YAML list. Each entry begins with "- id:".
# Generated by /billing-legal:cold-start-interview
```

Create `invoice-register.yaml` if it doesn't exist. Write only these comment lines:
```yaml
# Invoice register — index of all issued invoices.
# Format: top-level YAML list. Each entry begins with "- id:".
```

---

### Phase 10: Close

> Setup complete. Here's what to do next:
>
> - `/billing-legal:rate-card` — set client-specific rate overrides and billing arrangements
> - `/billing-legal:billing-status` — see your current billing state or log time manually
> - `/billing-legal:time-entry` — add a time entry by hand
>
> When you're working in a matter (like `/commercial-legal:matter-workspace switch acme-corp`), the billing panel will automatically associate that session with that client.
>
> To change any of these settings later: `/billing-legal:customize`

---

## What this skill does not do

- Make billing decisions — those are the attorney's professional responsibility
- Verify bar compliance — attorneys are responsible for their own ethics rules
- Create client profiles — those are created the first time you log time for a new client (via `/billing-legal:time-entry` or the billing panel)
- Push to accounting software — invoices are Markdown files for copy-paste or printing
