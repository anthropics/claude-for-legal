---
name: works-council-check
description: >
  Check whether a planned decision requires works council or employee
  representative body consultation — YT-laki in Finland, BetrVG in Germany,
  and EU collective redundancy rules. Use when asking "do we need to consult
  the works council?", "does YT-laki apply here?", "can we restructure without
  consultation?", "collective redundancy procedure", or before any major
  workforce or organisational change.
argument-hint: "[describe the decision or change — e.g. 'closing the Helsinki office', 'removing 15 roles', 'changing remote work policy']"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:works-council-check

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If placeholders, stop: "Run `/eu-legal:cold-start-interview` first."
2. Load `~/.claude/plugins/config/eu-legal/employment.md` if it exists. Read: headcount thresholds, fi_yt_laki_applies, fi_personnel_rep_type, de_betriebsrat_exists, hiring countries.
3. Run the workflow below.
4. Output: consultation required (yes/no/recommended), which body, what procedure, timeline, consequence of skipping.

---

## Purpose

Consultation failures are among the most expensive employment law mistakes in Finland and Germany. In Germany, a dismissal without BetrVG §102 consultation is void — the employer must reinstate the employee and pay back salary regardless of the substantive grounds. In Finland, breach of YT-laki cooperation obligations triggers employer liability. This skill determines whether consultation is required before you act.

---

## Step 1: Identify the decision

If not already described, ask:
> "What decision or change are you considering? (e.g., redundancies, office closure, outsourcing, change to working hours, implementation of monitoring technology, change to remote work policy)"

Also ask:
> "How many employees are affected, and in which countries?"

---

## Step 2: Route by jurisdiction

### Finland — YT-laki 1333/2021

**Threshold check:**
If `fi_yt_laki_applies: false` (fewer than 20 employees regularly), YT-laki does not apply. Note: even below 20, employer has good faith consultation obligations under general employment law principles.

If `fi_yt_laki_applies: true`, check the decision type:

Call `mcp__velvoite__get_finnish_statute("YTL", "51")` for cooperation negotiation requirements and `mcp__velvoite__get_finnish_statute("YTL", "16")` for general cooperation scope. Present thresholds from the live statute text.

**Decisions requiring YT-neuvottelut (cooperation procedure):**

| Decision type | YT-laki provision | Minimum negotiation period |
|---|---|---|
| Collective redundancies (≥10 employees in 90 days) | §51 | 6 weeks (employers ≥30 employees); 6 weeks or shorter period agreed with personnel rep |
| Significant changes to work or working conditions | §16 | Negotiate until agreement or until parties find no agreement possible |
| Outsourcing or acquisition affecting personnel | §16 | Negotiate to completion |
| Changes to use of fixed-term or part-time employment | §16 | Negotiate to completion |
| Introduction of surveillance or monitoring systems | §16 | Negotiate to completion |
| Changes to remote work practices (significant change) | §16 | Negotiate to completion |
| Reduction of fewer than 10 employees (financial/production grounds) | §47 | Recommend consultation even if below threshold |

**Who to consult:**
- If `fi_personnel_rep_type: luottamusmies` → consult the luottamusmies (shop steward)
- If `fi_personnel_rep_type: henkilostoedustaja` → consult the henkilöstöedustaja (personnel rep)
- If `fi_personnel_rep_type: none` → consult directly with the employees affected; document the process

**What the procedure requires:**
1. Employer gives written notice (neuvottelukutsu) to personnel rep stating: what is being considered, why, and what alternatives have been considered
2. Negotiations held in good faith — employer must provide necessary information; employee rep can request additional information
3. Employer must genuinely consider alternatives and employee proposals
4. Employer documents that negotiations occurred and what was discussed
5. After negotiations conclude: employer issues decision; personnel rep has right to be informed of the outcome

**Consequence of skipping:**
- Employer liable for compensation up to 35 days' salary per affected employee (YT-laki §62)
- For collective redundancies: does not invalidate the dismissal, but creates significant liability exposure
- Criminal liability (fine) for employer's responsible person in serious cases (YT-laki §62 §3)

---

### Germany — BetrVG

**Threshold check:**
If `de_betriebsrat_exists: false` from employment.md: no Betriebsrat consultation required. Note: if ≥5 employees, employees have the right to form one — if they do, consultation requirements apply from that point.

If `de_betriebsrat_exists: true`, determine the BetrVG provision:

**Decisions requiring mandatory consultation or co-determination:**

| Decision type | BetrVG provision | Consequence of skipping |
|---|---|---|
| Individual dismissal (ordinary or extraordinary) | §102 | Dismissal is void (nichtig) |
| Mass redundancy (≥20 employees or thresholds below) | §112 + §111 | Interest of balance of interests (Interessenausgleich) required; Sozialplan mandatory; failure = compensation liability |
| Change to working hours, breaks, or overtime | §87(1) No. 2+3 | Co-determination right — measure cannot be implemented without agreement or arbitration board ruling |
| Introduction of technical monitoring/surveillance devices | §87(1) No. 6 | Co-determination right — cannot implement without Betriebsvereinbarung or arbitration |
| Hiring / internal transfer / reclassification | §99 | Cannot implement without Betriebsrat consent or Labour Court order |
| Changes to pay structure or bonuses | §87(1) No. 10+11 | Co-determination right |
| Major operational change (Betriebsänderung) affecting >20 employees | §111 | Balance of interests required; Sozialplan mandatory; failure = §113 compensation per affected employee |
| Introduction of AI-based performance monitoring or scoring | §87(1) No. 6 + emerging case law | Co-determination right; proceed only with Betriebsvereinbarung |

**Major operational change (§111) threshold:**
Applies if establishment has >20 employees AND the change is: closure or relocation of the establishment or significant parts; merger; major changes to organisation, purpose, or equipment; introduction of new working methods or production processes with material effects on workforce.

**Sozialplan requirement:**
When §111 applies and the employer has >20 employees: a Sozialplan (social plan — compensation for affected employees) must be negotiated with the Betriebsrat. If no agreement: either party may go to the arbitration board (Einigungsstelle). The Sozialplan has force of a works agreement (Betriebsvereinbarung).

**§102 consultation procedure:**
1. Employer gives written notice to Betriebsrat: employee name, type and timing of dismissal, grounds
2. Betriebsrat has 1 week to respond (ordinary dismissal) or 3 days (extraordinary dismissal)
3. If Betriebsrat objects: must state grounds; employer must inform employee of objection
4. Employer may dismiss after period elapses even without Betriebsrat agreement
5. **Notice given before period elapses = void dismissal.**

---

### EU — Collective redundancy thresholds (Directive 98/59/EC)

EU collective redundancy rules apply where national law implements the Directive (all EU member states). Thresholds triggering special procedure:

| Establishment size | Redundancy threshold | Consultation period |
|---|---|---|
| 20–99 employees | ≥ 10 redundancies in 30 days | Minimum 30 days advance notice to authority |
| ≥ 100 employees | ≥ 10% of workforce OR ≥ 30 in 30 days | Minimum 30 days advance notice to authority |

**Finland implementing act:** YT-laki §48 + YT-laki §51 — notification to TE-toimisto (Employment and Economic Development Office) required when ≥10 redundancies within 90 days.

**Germany implementing act:** KSchG §§ 17-18 — notification to Bundesagentur für Arbeit required before collective dismissals. Failure: dismissals void.

---

## Step 3: Output

**Consultation required:** [Yes — mandatory / Yes — recommended / No — but document decision / Uncertain — legal review needed]

**Which body:** [Betriebsrat / Luottamusmies / Henkilöstöedustaja / Employees directly / None / Authority notification also required]

**Applicable provision:** [BetrVG §102 / YT-laki §51 / YT-laki §16 / EU Directive 98/59 / KSchG §17]

**Minimum procedure:**
[Numbered list of required steps with sequence and timing]

**Timeline:**
[Earliest date the decision/dismissal can be implemented given notice and consultation periods]

**If skipped:**
[Specific consequence — void dismissal / compensation liability / criminal fine / authority penalty]

---

## Guardrail

> **RESEARCH NOTES — NOT LEGAL ADVICE.** Consultation requirements are jurisdiction-specific and fact-sensitive. A void dismissal (Germany) or compensation liability (Finland) can result from procedural failures even when the substantive grounds are sound. Have an employment lawyer confirm the consultation procedure and timing before the decision is communicated to employees. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.