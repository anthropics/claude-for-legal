---
name: privacy-triage
description: >
  Quickly determine whether a new processing activity needs a DPIA, a
  mandatory GDPR DPIA, or can proceed — surfaces privacy policy conflicts
  and routes to the right next step. Use when asking "does this need a
  DPIA", "privacy check on X", "is this okay from a privacy perspective",
  or describing a new data processing activity.
argument-hint: "[describe the processing activity]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:privacy-triage

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If placeholders, stop: "Run `/eu-legal:cold-start-interview` first."
2. Load `~/.claude/plugins/config/eu-legal/privacy.md` for DPIA triggers. If missing, use GDPR Art. 35 baseline.
3. Run the triage workflow. Output a verdict and next step — not a full assessment.

---

## Purpose

Fast triage — 5 minutes, not 5 hours. The output is a routing decision: stop / consult legal / PIA recommended / DPIA mandatory / proceed with standard controls.

## Triage questions

Ask these three questions, then give a verdict:

**Q1: What data is involved?**
Classify: personal data only / special categories (Art. 9: racial or ethnic origin, political opinions, religious beliefs, philosophical beliefs, trade union membership, genetic data, biometric data (for identification purposes), health data, sex life, sexual orientation) / criminal records (Art. 10) / children's data / financial/location data (high personal nature per EDPB).

**Q2: What happens to the data?**
Classify the operation: collect only / automated decision-making with significant effects / systematic monitoring / profiling / matching datasets / sharing with new recipients / transferring outside EU.

**Q3: At what scale?**
Classify: individual / small-scale (< 500 data subjects) / large-scale (EDPB: number of subjects, volume of data, geographic extent, duration all matter).

## Verdict table

**Live verification:** Call `mcp__velvoite__get_eu_regulation_article("gdpr", "22")` to verify automated decision-making conditions and exceptions from live EUR-Lex text before routing.

| Situation | Verdict |
|---|---|
| Special categories + large scale, or automated decisions with legal effects | **DPIA mandatory** — run `/eu-legal:pia-generation` before proceeding |
| 2+ of the 9 WP29 criteria | **DPIA mandatory** |
| 1 WP29 criterion | **PIA recommended** — run `/eu-legal:pia-generation`; may escalate to DPIA |
| Processing appears **prohibited**: no Art. 6 legal basis, or Art. 5 principles violated, or falls within Art. 9 without Art. 9(2) exception, or Art. 22 automated decision without Art. 22(2) exception | **STOP** — route to legal immediately; do not proceed |
| Standard personal data, small scale, clear legal basis, existing controls | **Proceed** — document legal basis, apply standard data minimisation and security controls |

## Special checks for EU financial institutions

If entity type from base profile is a regulated financial entity:
- Employee monitoring: Finnish Laki yksityisyyden suojasta työelämässä (759/2004) and GDPR Art. 88 — proportionality is strict; blanket monitoring not permitted
- Transaction data profiling: MiFID II and AMLD may require retention AND processing that needs a compatible legal basis under GDPR Art. 6(4)
- Automated credit/fraud decisions: Annex III EU AI Act high-risk system → flag AI Act compliance check alongside DPIA

---

## Guardrail

Triage is not a DPIA. A DPIA verdict here requires running `/eu-legal:pia-generation` before the processing begins. GDPR Art. 35(10) and national law may impose additional requirements beyond this triage. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.