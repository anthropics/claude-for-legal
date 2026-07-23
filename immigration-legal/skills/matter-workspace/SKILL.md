---
name: matter-workspace
description: >
  Manage client matter workspaces — new, list, switch, close, or detach
  (practice-level). Keeps one client's context separate from every other.
  Use when the attorney says "new matter", "new client", "switch to [client]",
  "list my matters", "close this matter", or when another skill needs to know
  which client file is active.
argument-hint: "<new | list | switch | close | none> [slug]"
---

# /matter-workspace

Immigration attorneys work across many active petitions simultaneously. A matter workspace keeps one client's evidence, history, and notes separate from every other. This skill manages those workspaces.

## Subcommands

- `/immigration-legal:matter-workspace new <slug>` — create a new client matter, run intake, write `matter.md`
- `/immigration-legal:matter-workspace list` — list active matters with status and active flag
- `/immigration-legal:matter-workspace switch <slug>` — set the active matter
- `/immigration-legal:matter-workspace close <slug>` — archive a matter (never delete)
- `/immigration-legal:matter-workspace none` — detach from any active matter, work at practice-level only

## Instructions

1. **Read the practice profile** at `~/.claude/plugins/config/claude-for-legal/immigration-legal/CLAUDE.md`. Check `## Matter workspaces → Enabled`. If `✗`, tell the attorney: "Matter workspaces are off in your practice profile. Edit `## Matter workspaces → Enabled: ✓` or run `/immigration-legal:customize` to enable them." Don't error — this is expected for solo practitioners with a small roster.

2. Dispatch on the first token of `$ARGUMENTS`:
   - `new` → run intake, write `matter.md`, seed `history.md` and `notes.md`
   - `list` → enumerate `matters/*/matter.md`, print table, mark active
   - `switch` → update `Active matter:` in practice-level CLAUDE.md
   - `close` → move `matters/<slug>/` → `matters/_archived/<slug>/`, log close date
   - `none` → set `Active matter:` to `none — practice-level context only`

3. Confirm before writing.

---

## Storage layout

```
~/.claude/plugins/config/claude-for-legal/immigration-legal/
├── CLAUDE.md                         # practice-level practice profile
└── matters/
    ├── <slug>/
    │   ├── matter.md                 # client profile, visa type, key facts, evidence status
    │   ├── history.md                # dated log of events and decisions (append-only)
    │   ├── notes.md                  # free-form working notes
    │   └── outputs/                  # skill outputs for this matter
    └── _archived/
        └── <slug>/                   # closed matters — readable for conflicts/retention
```

Slugs are lowercase with hyphens. Examples: `chen-wei-eb1a`, `patel-niw-2026`, `kim-jin-o1a`.

**Active matter** is the `Active matter:` line in the practice-level CLAUDE.md. Switching a matter edits that line — no separate state file.

**Cross-matter context** is off by default. When off, a skill working in matter A never reads files in matter B. When on, cross-matter reads are only allowed when the attorney explicitly requests them.

---

## Subcommand logic

### `new <slug>`

1. Confirm slug is not already in `matters/<slug>/` or `matters/_archived/<slug>/`.
2. Run the intake:
   - **Client full name** and preferred name / pronoun if relevant
   - **Target visa type(s)** (EB-1A / EB-2 NIW / O-1A / O-1B — may be multiple if cross-chargeability or backup visa is contemplated)
   - **Field / industry** and current position
   - **Career stage** (early / mid / senior / established / distinguished)
   - **Priority date goal** (if applicable — e.g., "client needs green card within 2 years for employer sponsorship deadline")
   - **Evidence status** (preliminary — what's known; full inventory done via `/immigration-legal:evidence-organizer`)
   - **Prior immigration history** (current status, prior petitions, RFEs, denials, any complications)
   - **Confidentiality level** (standard / heightened — heightened for high-profile clients or sensitive circumstances)
   - **Key facts and context** (2–5 sentences: anything that makes this matter non-standard)
   - **Related matters** (slugs of any connected files — e.g., spouse's concurrent case)
3. Write `matters/<slug>/matter.md` per the template below.
4. Seed `matters/<slug>/history.md` with an "Opened" entry.
5. Create empty `matters/<slug>/notes.md`.
6. Do **not** auto-switch. Ask: "Want to switch to `<slug>` now?"

### `list`

Enumerate `matters/*/matter.md`. Print:

| Slug | Client | Visa target | Stage | Opened | Status | Active |
|---|---|---|---|---|---|---|

Mark active matter with `*`. Include `_archived/` under a separate "Archived" heading.

### `switch <slug>`

1. Confirm `matters/<slug>/matter.md` exists.
2. Edit `Active matter:` line in practice-level CLAUDE.md.
3. Show the `matter.md` summary so the attorney can confirm they're on the right file.

### `close <slug>`

1. Confirm `matters/<slug>/` exists.
2. Append a "Closed" entry to `history.md` with today's date and a close reason.
3. Move `matters/<slug>/` → `matters/_archived/<slug>/`.
4. If this was the active matter, set `Active matter:` to `none — practice-level context only`.

### `none`

Set `Active matter:` to `none — practice-level context only`. Confirm.

---

## `matter.md` template

```markdown
[WORK-PRODUCT HEADER — PRIVILEGED & CONFIDENTIAL — ATTORNEY WORK PRODUCT]

# Matter: [Client name] — [Visa type] petition

**Slug:** [slug]
**Opened:** [YYYY-MM-DD]
**Status:** active
**Confidentiality:** [standard / heightened]

---

## Client

**Full name:** [name]
**Field:** [field / industry]
**Current position:** [title, employer, country]
**Career stage:** [early / mid / senior / established / distinguished]

## Target visa

**Primary:** [EB-1A / EB-2 NIW / O-1A / O-1B]
**Backup / alternative:** [if applicable]
**Priority date goal:** [if applicable]

## Evidence status

**Last merit evaluation:** [date / not yet run]
**Overall filing readiness:** [Green — file ready / Yellow — developing / Red — not ready]
**Key criteria met:** [list from last merit-eval, or "not yet assessed"]
**Key gaps:** [list from last merit-eval, or "not yet assessed"]

## Prior immigration history

[Current status (e.g., H-1B, F-1 OPT), prior petition history, any RFEs or denials, anything that affects strategy]

## Key facts

[2–5 sentences. What makes this matter non-standard. Anything that would affect strategy or risk assessment.]

## Matter-specific overrides to firm posture

*Any deviation from the practice-level playbook that applies only to this matter.*

- [e.g., "Client is high-profile — conservative posture on press / do not seek additional media coverage"]
- [e.g., "Priority is speed — willing to file with borderline criterion count if partner approves"]

## Related matters

- [slug — one line why related, e.g., "spouse concurrent NIW case"]

## Notes on confidentiality

[If heightened: reason, who may access this file, whether cross-matter context is restricted even if globally on]
```

## `history.md` seed

```markdown
# History: [Client name] — [Visa type]

Append-only event log. Most recent at top.

---

## [YYYY-MM-DD] — Matter opened

Intake completed. Slug: `[slug]`. Target visa: [type]. Status: active.
[Any initial context — e.g., "Opened following referral from [university OIS]. Client currently on H-1B expiring [date]."]
```
