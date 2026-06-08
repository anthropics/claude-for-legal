---
name: customize
description: >
  Change one thing in your eu-legal profile without re-running the full
  cold-start interview. Adjust entity type, jurisdictions, actor roles,
  active practice areas, Velvoite workspace, legal team, or outside counsel.
  Use when the user says "change my entity type", "update my jurisdiction",
  "add a practice area", "update my profile", or similar.
argument-hint: "[section name, or describe what you want to change]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:customize

1. Read `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If missing or placeholders, stop: "Run `/eu-legal:cold-start-interview` first."
2. Show the customizable map (see below).
3. Ask what to change. Make the change. Write the updated config back.
4. Confirm what was updated.

---

## Customizable sections

Show the current value for each section, grouped:

**Company identity**
- Entity type — current: [from profile]
- Primary jurisdiction — current: [from profile]
- Operating countries — current: [from profile]

**Regulatory posture**
- Actor roles per regulation — current: [table from profile]
- Velvoite workspace ID — current: [from profile]

**Practice areas**
- Active practice areas — current: [checked list from profile]

**Legal team**
- Team structure — current: [from profile]
- Outside counsel — current: [from profile]

**Integrations**
- Re-probe integrations: suggest `/eu-legal:cold-start-interview --check-integrations`

---

## Making the change

Ask exactly one clarifying question if needed. Then update the relevant section in `~/.claude/plugins/config/eu-legal/CLAUDE.md` using Edit (not a full rewrite). Show a one-line diff of what changed. Confirm: "Updated. All skills will use the new value on their next run."

For actor role changes: offer to re-import from Velvoite if the API key is set — call `mcp__velvoite__get_company_profile()` and update the whole actor roles table.

---

## Fallback (VELVOITE_API_KEY not set)

Profile editing works entirely locally — you can update entity type, jurisdictions, practice areas, legal team, and outside counsel without Velvoite.

The only feature unavailable without `VELVOITE_API_KEY` is the actor-role re-import (which auto-fills your regulation roles from your Velvoite workspace). You can still edit actor roles manually in the profile — they are plain text fields in the actor roles table.

To enable re-import: add `VELVOITE_API_KEY` to your `.envrc` and run `direnv allow`, then re-run `/eu-legal:customize` for actor role changes.

---

## Disclaimer

Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
