---
name: playbook-init
description: >
  Guided setup or update of the commercial contracts playbook — walk through each
  playbook section conversationally and write commercial.md. Use when skipping
  commercial-cold-start, resetting specific positions, or when the user says "update
  my playbook", "change my liability position", "set my governing law", or "I want to
  reset my NDA positions". Note: /eu-legal:commercial-cold-start covers this as part
  of full setup.
argument-hint: "[section to update — e.g. 'liability' | 'governing-law' | 'nda-positions' | 'escalation' | blank for full run]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:playbook-init

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If missing or has `[PLACEHOLDER]`, stop: "Run `/eu-legal:cold-start-interview` first."
2. If `commercial.md` exists and is populated, load it. This is an update run: only modify the sections the user asks about, preserve the rest.
3. If `commercial.md` is missing or has all `[PLACEHOLDER]` values: run full setup (all sections below). Equivalent to `commercial-cold-start` playbook-only mode.
4. If an arg is provided (e.g., `liability`, `governing-law`): jump directly to that section. Otherwise guide through all sections.

---

## Purpose

Helps the user build or update their `commercial.md` playbook section by section, conversationally. Pre-populated with EU-sensible defaults so the user can accept, modify, or reject each position.

Note: `/eu-legal:commercial-cold-start` covers this as part of full plugin setup — run that on first install. Use `/eu-legal:playbook-init` to update a specific section or rebuild the playbook without re-running the full cold-start interview.

---

## EU-sensible defaults

Pre-populate these as starting points. Present them as defaults the user can accept, modify, or reject — do not present them as the "right" answer.

| Section | Default starting point |
|---|---|
| Preferred governing law | Finnish law (for Finnish-primary entities); German law (for German-primary entities) — read from `CLAUDE.md` primary jurisdiction |
| Cross-border dispute resolution | ICC arbitration, seat: Stockholm |
| Direct liability cap | 12 months of fees paid in the 12 months preceding the claim |
| Consequential damages | Excluded, with carve-outs for data breach, IP infringement, and gross negligence |
| Auto-renewal default notice | 30 days minimum (some EU member states impose longer statutory minimums — flag this) |
| DPA requirement (purchasing) | Vendor signs our DPA as processor |
| ICT audit rights | Right to audit (directly or via third-party auditors) — required for DORA in-scope entities |

---

## Section-by-section guide

Ask one section at a time. For each section:
1. Show the current value from `commercial.md` (or the EU-sensible default if not yet set)
2. Ask: "Does this match your position? Accept / modify / tell me your position"
3. Record the answer

### Section: Governing law and dispute resolution

> "Your current governing law preference is [from commercial.md or default]. Does this match your standard?
> - Preferred: [show current / default]
> - Acceptable: [show current / default]
> - Never: [show current / default — flag that outside-EU governing law is an automatic escalation trigger in the EU context]"

Offer to set `governing_law_never` to "any jurisdiction outside the EU" as an automatic escalation trigger.

For Finnish-law agreements: note that Finnish courts (District Court of Helsinki) are well-suited for domestic contracts. For cross-border EU: ICC or SCC arbitration is more common.

### Section: Liability cap

> "Your current direct liability cap is [from commercial.md or default: '12 months of fees paid in the preceding 12 months']. For each position below, tell me your standard, acceptable fallback, and never-accept:"

Walk through:
- Direct cap (multiple of fees)
- Indirect / consequential damages
- Carve-outs above the cap (data breach, IP, gross negligence, fraud — EU standard)
- Cap base definition ("fees paid in the 12 months preceding the claim" vs. other definitions)

Note: EU unfair contract terms rules (Directive 93/13/EEC for B2C; national implementations for B2B — e.g., Finnish Kuluttajansuojalaki, German BGB §§ 305–310) may constrain limitation clauses in standard terms. Flag this: "If you use standard terms (your form sent to customers or vendors without individual negotiation), EU unfair terms rules may apply. Blanket liability exclusions may be invalid. `[model knowledge — verify with local counsel]`"

### Section: NDA triage positions

> "Let's set your NDA triage positions — these determine when an NDA is GREEN (route to signature), YELLOW (flag for review), or RED (stop, talk to legal). For each item, tell me your position."

Walk through:
- Mutual vs. one-way NDAs (when is one-way acceptable?)
- Definition of confidential information (how broad?)
- Duration (acceptable range)
- Residuals clause (acceptable / not acceptable)
- Governing law (EU only? any EU? never outside EU?)
- Restrictive covenants in an NDA (auto-YELLOW or auto-RED?)

Note: "GREEN can only be issued if these positions have been reviewed by an attorney. I'll flag GREEN outputs against `[PLACEHOLDER]` positions as YELLOW automatically."

### Section: Sales-side playbook

Walk through each position: IP, audit rights, data processing, termination, deal-breaker.

### Section: Purchasing-side playbook

Walk through each position: DPA, audit rights, subcontracting, SLA minimum, deal-breaker.

### Section: Escalation thresholds

Walk through: EUR thresholds per role, automatic triggers.

---

## Write result

After all confirmed sections, update `~/.claude/plugins/config/eu-legal/commercial.md` — only the sections touched in this session. Preserve unchanged sections exactly as they were.

Show a diff-style summary of what changed:
```
Updated sections:
- Governing law: Finnish law preferred (was: [old value])
- Direct liability cap: 12 months fees (was: [PLACEHOLDER])
- NDA triage positions: added (was: not set)

Unchanged sections: purchasing-side playbook, escalation matrix
```

---

## After writing

> "Playbook updated. To use it:
> - Review a contract: `/eu-legal:contract-review`
> - Review an NDA: `/eu-legal:nda-review`
> - Review a vendor agreement: `/eu-legal:vendor-agreement-review`"

---

## Disclaimer

Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
