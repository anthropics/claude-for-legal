---
name: cold-start-interview
description: Role, situation, and phase setup → configurable profile for employment-legal-es
argument-hint: "No arguments; conversational interview"
---

# Cold-Start Interview

## Purpose

Gather essential context to configure the user's profile. Answers one question at a time, then writes the profile to the config path.

## Workflow

### Step 1: Role

Ask: **What is your role?**

Options:
- `trabajador` = employee, worker, union representative
- `abogado` = attorney, labor law specialist, in-house counsel
- `asesor` = HR advisor, business advisor, consultant

Record: `[role]`

### Step 2: Situation

Ask: **What is your current situation?**

Options:
- `baja IT` = on sick leave (IT), no IPT/IPA filed yet
- `IPT pendiente` = awaiting IPT ruling (ICAM or court) — unable to do habitual profession
- `IPA pendiente` = awaiting IPA ruling — unable to do ANY profession (multi-system, severe)
- `IPT declarada` = already ruled IPT/IPA
- `plan pensiones` = occupational pension inquiry
- `revolving` = revolving credit usury claim
- `contingencia` = common→professional contingency procedure
- Other: describe briefly

If user says "IPT pendiente" AND has multi-system diagnoses (neurological + urological + psychiatric + chronic pain), proactively note: "Given your diagnoses, IPA may be the more appropriate target — do you want to explore that?"

Record: `[situation]`

### Step 3: Company / Employer

Ask: **Company name and sector (if employee)?** Or skip if attorney.

Record: `[company]` (optional)

### Step 4: Key Dates

Ask: **When did your situation start?**
- If IT: sick leave start date (YYYY-MM-DD)
- If IPT: approximate diagnosis date or ICAM filing date
- If revolving: contract date
- If contingency: baja IT start date

Record: `[date]`

### Step 5: Diagnoses / Details + Base Reguladora

Ask: **Main diagnoses (CIE-10 if available) or issue description?**

Examples:
- "G83.4 spinal cord lesion, R15.9 fecal incontinence, driver profession"
- "M54.40 lumbago with sciatica, office work"
- "Revolving card Visa & Go, TAE 22,42%, saldo 5.186€"

Record: `[diagnoses_or_issue]`

If situation is IT / IPT / IPA / contingencia, also ask:

**¿Cuál es tu salario neto mensual de referencia antes de la baja?** (Base reguladora para calcular pensión estimada.)

Example: "1.830 €/mes neto IT delegada TMB"

Record: `[base_reguladora]` (used by ipt-analysis and contingencia-cambio for economic impact table)

### Step 6: Phase

Ask: **What phase are you in?**

Options:
- `inicial` = just started, gathering info
- `documentación` = collecting medical/labor evidence
- `procedimiento abierto` = filed claim, awaiting ruling
- `sentencia` = ruling received, planning next steps

Record: `[phase]`

### Step 7: Write Profile

Once all answers collected, write profile to:
```
~/.claude/plugins/config/claude-for-legal/employment-legal-es/CLAUDE.md
```

Append under "### User Profile" section:

```markdown
### User Profile — [timestamp]

- **Role:** [role] ([trabajador/abogado/asesor])
- **Situation:** [situation]
- **Objective grade:** [IPT / IPA / GI — infer from diagnoses if multi-system]
- **Company:** [company, if applicable; else "N/A"]
- **Start Date:** [date]
- **Day count:** [days from start date to today]
- **Diagnoses/Issue:** [diagnoses_or_issue]
- **Base reguladora:** [base_reguladora — monthly net salary reference, or "N/A"]
- **Phase:** [phase]

**Available Skills for your situation:**
- [List 2-3 skills relevant to the situation]

**Next step:** Ask me `/employment-legal-es:[skill]` to dive deeper.
```

### Step 8: Confirm and Suggest

Say to user:

```
Profile saved. Here are the skills most relevant to your situation:

- [Skill 1]: [short description]
- [Skill 2]: [short description]

Which would you like to explore first, or would you like a brief overview of all skills?
```

---

## Example Flow

**User:** `Hey, I'm an employee on sick leave and want to understand my options.`

**Claude:**
1. Role: "Are you the employee, an attorney advising, or an HR advisor?" → `trabajador`
2. Situation: "What's your situation? Sick leave, disability claim pending, pension question, credit claim?" → `baja IT`
3. Company: "Employer name and sector?" → `TMB (public transport Barcelona)`
4. Date: "When did your sick leave start?" → `2025-03-10`
5. Diagnoses: "Any diagnoses or key health issues?" → `G83.4 cauda equina, conductor profession, discapacidad 41%`
6. Phase: "What phase are you in?" → `documentación`

**Profile saved:**
```markdown
### User Profile — 2025-05-14

- **Role:** trabajador
- **Situation:** baja IT
- **Company:** TMB (Barcelona public transport)
- **Start Date:** 2025-03-10
- **Diagnoses/Issue:** G83.4 spinal cord lesion, fecal incontinence (R15.9), conductor, 41% disability rating
- **Phase:** documentación

**Available Skills for your situation:**
- `it-seguimiento`: Timeline from 2025-03-10 (now day 431)
- `ipt-analysis`: IPT/IPA grade analysis with medical evidence
- `contingencia-cambio`: Common→professional contingency procedure

Next step: Ask me `/employment-legal-es:it-seguimiento` to see your timeline.
```

---

## Disclaimer

```
BORRADOR DE TRABAJO — NO CONSTITUYE ASESORAMIENTO JURÍDICO — 
REVISAR CON ABOGADO LABORALISTA COLEGIADO EN ESPAÑA ANTES DE ACTUAR
```

This interview is a setup tool only. Answers are stored locally. Actual legal advice and procedural decisions must be made with a qualified Spanish employment law attorney.

---

## Notes

- Config path creation is automatic (mkdir -p if needed)
- Profile is **not** sent to external services — remains local
- User can run `cold-start-interview` again to update profile
- All subsequent skills read the stored profile to personalize outputs
