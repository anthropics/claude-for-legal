---
name: board-minutes
description: >
  Draft Finnish startup board meeting minutes — OYL-compliant format, quorum
  check, decision types, signing requirements. Use when asking "draft board
  minutes", "what needs board approval", or after a board meeting.
argument-hint: "[describe decisions made, or paste meeting notes]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /fi-startup-legal:board-minutes

1. Load profile.
2. Call `mcp__velvoite__get_finnish_statute("OYL", "6")` — board rules, quorum, decision-making. If unavailable: apply the OYL Chapter 6 rules below as fallback and note `[OYL §6 not fetched live — verify at finlex.fi]`.
3. **Input gate:** Before drafting, confirm the user has provided: (a) meeting date and location, (b) names of attendees and quorum count, (c) the chair's name, and (d) each decision that was made. If any are missing, ask before proceeding — do not draft minutes from partial input.
4. **Decision-type check:** For each stated agenda item, verify it falls within board authority (see Decision types below). If any item appears to require AGM approval (share issuance, option scheme, changes to yhtiöjärjestys, auditor, dividend, merger/demerger), halt and flag: "This decision may require an AGM resolution — do not draft board minutes for it until authority is confirmed with counsel."
5. Draft minutes from the confirmed input. Draft for attorney review before signing.

---

## OYL board governance (from live statute)

From fetched OYL §6 text, apply current rules for:

**Quorum:** majority of board members must be present (unless SHA requires higher threshold).

**Decision-making:** simple majority of those present, unless SHA specifies otherwise.

**Signing:** minutes must be signed by the chair and at least one board member present (or all members who participated).

## Decision types

**Board decisions (hallitus):** day-to-day management, operational decisions, entering contracts below the threshold in SHA, hiring/firing employees below CEO level.

**Shareholder/AGM decisions (yhtiökokous):** required for share issuance, option schemes, changes to yhtiöjärjestys, auditor appointment, dividend, merger/demerger, dissolution.

**Items typically requiring board approval:**
- Contracts above the threshold defined in SHA
- Hiring the CEO
- Opening/closing bank accounts
- Taking on debt above threshold
- Any matter with potential conflict of interest (must be disclosed)

## Minutes structure

> ⚠️ **Draft only. Minutes you sign are legally binding records. Review every line for accuracy before signing — including decision classification, quorum, and SHA threshold compliance. Have a Finnish company lawyer review before signing minutes for consequential decisions (share issuances, debt instruments, related-party transactions, conflict-of-interest disclosures).**

```
[COMPANY NAME] OY — BOARD MEETING MINUTES

Date: [date]
Location / method: [physical / Teams / written procedure]
Present: [names + roles]
Chair: [name]
Minutes secretary: [name]

§1 Opening and quorum
The chair opened the meeting. Quorum confirmed: [N] of [N] members present.

§2 Agenda
[List items]

§3 [Agenda item 1]
Proposal: [text]
Decision: The board resolved [text] / Passed unanimously / Passed [N]-[N].

[Repeat for each item]

§X Closing
The chair closed the meeting.

Signatures:
Chair: _______________
Board member: _______________
```

---

## What this skill does NOT do

- **Written shareholder resolutions** (osakkeenomistajan päätös ilman kokousta): different format and OYL §5:1 requirements — not covered here.
- **AGM minutes**: Annual general meeting minutes have separate statutory requirements.
- **Board decisions by circulation** (kiertokirje/per capsulam): different format.
- **SHA threshold compliance**: Does not read your SHA — verify each decision against SHA protective provisions and approval thresholds yourself.
- **Legal advice**: Generates a draft only. Signing incorrect minutes creates legal risk this skill cannot prevent.

---

## Guardrail

Board minutes are legal documents. Ensure they are signed promptly after the meeting. Decisions not properly documented in signed minutes may be challenged. Store signed minutes securely — they are required for M&A due diligence. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
