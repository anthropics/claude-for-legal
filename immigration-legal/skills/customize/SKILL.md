---
name: customize
description: >
  Guided customization of your immigration practice profile — change one thing
  without re-running the whole cold-start interview. Adjust risk posture, evidence
  standards, comparable-evidence posture, escalation rules, house style, visa types
  in scope, or matter workspace settings. Use when the attorney says "change my
  [thing]", "update my profile", "tune my posture", "my citation threshold is wrong",
  or "add a new visa type".
argument-hint: "[posture | evidence | comparable | escalation | style | visas | workspaces | integrations]"
---

# /customize

Edits one section of the practice profile at a time. Reads the current value, proposes a change, and writes it back. Does not re-run the full cold-start interview.

## Instructions

1. **Read the practice profile** at `~/.claude/plugins/config/claude-for-legal/immigration-legal/CLAUDE.md`.

2. **Identify what the attorney wants to change.** If not clear from the argument or conversation, ask: "Which part of your practice profile do you want to update? (posture / evidence standards / comparable evidence / escalation / house style / visa types / matter workspaces / integrations)"

3. **Show the current value** for the section being changed.

4. **Ask for the new value.** Be specific — don't accept vague answers. "More aggressive on NIW" → "How aggressive? What should the new posture be — aggressive / standard / conservative?"

5. **Propose the edit.** Show the before/after diff in plain English.

6. **Write the change** after confirmation.

7. **Show downstream effects.** If the change affects how another skill behaves, note it. Example: "Changing your EB-1A posture from standard to aggressive means merit-evaluation will call YELLOW on criteria where evidence is present but thin, rather than RED. Your next evaluation will reflect this."

---

## Sections and what to ask

### `posture` — Risk posture per visa type

> "Current EB-1A posture: [X]. What should it be — aggressive / standard / conservative? Any notes on when to override?"

Update `## Risk posture` in the practice profile. Note: posture affects every merit-evaluation output; change it deliberately.

### `evidence` — Evidence thresholds

> "Which threshold do you want to change? (publication count / citation count / accepted source types / media tier / contributions bar / salary benchmark / salary percentile)"

Show current value → ask for new value → write.

For citation thresholds: ask whether the new threshold is "per paper", "total", or "field-adjusted". Write it precisely — ambiguous thresholds produce inconsistent merit evaluations.

### `comparable` — O-1 comparable evidence posture

> "Current posture: [willing / reluctant / never]. What should it be, and any notes on when you'll use it?"

Update `## Evidence standards → "O-1 comparable evidence"`.

### `escalation` — Escalation rules

> "Which escalation rule do you want to change? (merit evaluation authority / borderline cases / visa type selection / RFE strategy / filing decision / second-reviewer requirement)"

Show current matrix row → ask for new rule → write.

### `style` — House style

> "Which style element? (tone / exhibit numbering / declaration format / criterion heading style / other)"

Show current value → ask for new value → note which skills use this (petition-letter-draft, rfe-response, client-update).

### `visas` — Visa types in scope

> "Which visa type do you want to add or change status for?"

For adding a new visa type: mark it `active` and note which skills are available for it. For EB-1B, PERM, H-1B, L-1 (currently `planned`): note that skill stubs exist but full skill development is pending.

### `workspaces` — Matter workspace settings

> "What do you want to change? (enable/disable / cross-matter context on/off / storage root path)"

### `integrations` — Re-check integrations

Runs the same integration check as `--check-integrations` in cold-start-interview. Updates `## Available integrations`.

---

## Diff format

Show changes as:

> **Section:** [section name]
> **Current:** [current value in plain English]
> **Proposed:** [new value in plain English]
> **Downstream effect:** [how this changes skill behavior]
>
> Confirm this change? (yes / no / adjust)

Write only after confirmation. Show the updated practice profile section after writing.

---

## What this skill does not do

- **Re-run the full interview.** For a full re-interview, use `/immigration-legal:cold-start-interview --redo`.
- **Change multiple sections at once.** Handle one section per run to keep diffs clear and auditable.
- **Override a change without showing the diff.** Always show before/after before writing.
