---
name: deadlines
description: >
  Upcoming EU regulatory compliance deadlines for your entity — default 90-day
  horizon, configurable. Use when asking "what's due soon", "compliance
  calendar", "DORA deadlines", "what do we need to do by end of quarter", or
  similar.
argument-hint: "[days] [regulation] — e.g. '30' or '60 dora'"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:deadlines

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If placeholders, stop: "Run `/eu-legal:cold-start-interview` first."
2. Check Velvoite: if `VELVOITE_API_KEY` not set, run Fallback.
3. Run the workflow below.

---

## Parse args

- `days` (optional integer, default 90): look-ahead window.
- `regulation` (optional): filter to a specific regulation code.

## Workflow

Call `mcp__velvoite__get_deadlines` with:
- `days_ahead`: from args
- `regulation`: from args if provided
- `include_overdue`: false

Render date-ascending:
| Date | Regulation | Deadline description | Notes |
|---|---|---|---|

Formatting:
- Within 7 days: prefix row with ⚠ and bold the date
- Within 30 days: bold the date
- If more than 8 rows: group by regulation

Add after the table:
> "Source: Velvoite corpus. Verify against the Official Journal and your competent authority's published compliance calendar — deadlines can shift via implementing acts or supervisory guidance."

If no results: say explicitly "No deadlines found in the Velvoite corpus for the next [N] days" and suggest checking EUR-Lex directly for the regulation.

---

## Fallback (VELVOITE_API_KEY not set)

Show key publicly-known EU regulatory dates relevant to the entity type from profile. Mark each `[public information — verify against Official Journal]`. Add:
> **Velvoite corpus not connected.** For live deadline tracking with authority-specific dates: add `VELVOITE_API_KEY` to your `.envrc`. Free 30-day trial at velvoite.eu.

---

## Disclaimer

Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
