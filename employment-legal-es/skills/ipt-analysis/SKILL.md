---
name: ipt-analysis
description: Permanent disability (IPT/IPA) grade analysis under LGSS Art. 194-200 + Ley 2/2025
argument-hint: "Diagnoses (CIE-10), habitual profession, residual capacity, prior ICAM ruling"
---

# IPT/IPA Analysis

## Purpose

Analyze the probable permanent disability grade (IPT = Incapacidad Permanente Total, IPA = Incapacidad Permanente Absoluta) based on LGSS Art. 194-200 and Ley 2/2025 (reasonable adjustments reform).

## Scope

Four grades under LGSS Art. 194-200:
1. **Incapacidad Parcial (IP)** — permanent reduction <33% for habitual profession
2. **Incapacidad Permanente Total (IPT)** — unable to perform >33% of fundamental tasks in habitual profession (but can perform other professions)
3. **Incapacidad Permanente Absoluta (IPA)** — unable to perform ANY professional activity
4. **Gran Invalidez (GI)** — IPA + need for third-party care (30%+ dependency)

### Key Framework

**LGSS Art. 194:** Grade depends on:
- Severity of health impairment
- Habitual profession prior to baja IT
- Residual work capacity
- Age (relevant for grade assessment, not mandatory exclusion)

**Ley 2/2025 (effective 2025-01-01):** Requires reasonable adjustments before declaring IPT/IPA.
- Employer must adapt role/schedule/tools first
- Rejection of adjustments must be documented (excessive cost, operational burden)
- If adjustments fail or rejected → IPT/IPA assessment

## Workflow

### Step 0: Load Profile

Read `~/.claude/plugins/config/claude-for-legal/employment-legal-es/CLAUDE.md`.
Extract: `[base_reguladora]`, `[situation]`, `[objective_grade]`, `[diagnoses_or_issue]`, `[company]`, `[date]`.
If profile exists, skip questions already answered — only ask for missing data.

### Step 1: Collect Medical Evidence

Ask user (skip if already in profile):
- **Diagnoses (CIE-10)?** (e.g., "G83.4 spinal cord lesion, R15.9 fecal incontinence, G89.28 chronic pain post-procedure")
- **Date of onset?** (important for prognosis, chronicity)
- **Is prognosis stable or progressive?**
- **Functional capacity report from treating physician?** (yes/no/date)
- **Have you been evaluated by Médico del Tribunal (Medical Court) or ICAM?** (yes/no/date/grade)

Record: `[diagnoses]`, `[onset_date]`, `[prognosis]`, `[functional_report]`, `[prior_icam]`

### Step 2: Habitual Profession

Ask:
- **Your habitual profession before baja IT?** (e.g., "conductor de autobús público", "electricista", "abogado")
- **Primary tasks?** (e.g., "driving 8h/day, concentration, emergency response, physical endurance")
- **Physical demands:** sedentary / light / moderate / heavy
- **Cognitive demands:** routine / complex / high responsibility
- **Any special licenses?** (e.g., permiso grupo D conductor)

Record: `[profession]`, `[tasks]`, `[demands]`

### Step 3: Residual Capacity

Ask:
- **Can you walk >30 min continuously?**
- **Can you stand >2h continuously?**
- **Can you use fine motor skills?** (writing, keyboard, assembly)
- **Cognitive capacity:** concentration, memory, decision-making?
- **Emotional/psychological:** depression, anxiety, panic?
- **Any activity you CAN do currently?** (e.g., "desk work 2-3 hours, supervised tasks")

Record: `[residual_capacity]`

### Step 4: Apply LGSS Grades

Create analysis table:

| Grade | LGSS Article | Test | Your Case |
|---|---|---|---|
| **Incapacidad Parcial (IP)** | Art. 194.2 | Permanent reduction <33% fundamental tasks in habitual profession. Can perform same role with restrictions. | [Likely if: minor functional loss, can return to job with accommodation] |
| **IPT** | Art. 194.1 | **Unable to perform >33% fundamental tasks** in habitual profession. Cannot return to same job. BUT can perform other professional activities (retraining possible). | [Likely if: significant functional loss in core tasks, but could theoretically do desk work, different profession] |
| **IPA** | Art. 195 | **Unable to perform ANY professional activity** — total occupational incapacity. Not just habitual profession. Age, education, geographic factors considered. | [Likely if: severe multi-system impairment, no residual work capacity, age >55 + low education] |
| **Gran Invalidez (GI)** | Art. 196 | IPA + **need for third-party care** for basic activities (ADL). 30%+ dependency rating. | [Likely if: IPA + requiring constant caregiver for dressing, feeding, hygiene] |

### Step 5: Cite Ley 2/2025

Add subsection:

**Ley 2/2025 Analysis (Reasonable Adjustments):**

- Has employer offered role adaptation, schedule modification, tools/equipment, telework? **[Yes/No/Partial]**
- If Yes: Did adaptations allow you to perform habitual profession tasks? **[Yes/No/Ongoing]**
- If No: Has employer documented rejection (excessive cost, operational burden)? **[Yes/No/Unknown]**
- Implication: ICAM will require evidence that reasonable adjustments were attempted and failed before granting IPT/IPA.

[verificar CENDOJ for TSJ Cataluña jurisprudencia on Ley 2/2025 implementation — field still evolving]

### Step 6: Construct Case

**Strengths:**
- [List: chronic diagnosis, multiple systems affected, prior ICAM ruling, functional reports]

**Weaknesses:**
- [List: prognosis unclear, residual capacity unclear, young age, potential for retraining]

**Key Evidence Needed:**
- [ ] Complete medical history (10+ years if available)
- [ ] Recent functional capacity evaluation by physiatrist / occupational therapist
- [ ] Employer's response to adaptation requests (dates, rejections)
- [ ] Prior ICAM/court rulings (if applicable)
- [ ] Psychological evaluation (if depression/anxiety present)
- [ ] Testimony from employer re: job demands

### Step 6b: Economic Impact Table (use base_reguladora from profile)

If `[base_reguladora]` is available, compute:

| Escenario | Base reguladora | % pensión | Pensión mensual | Recargo Art.164 | Total mensual | Valor 30 años |
|---|---|---|---|---|---|---|
| Contingencia común IPT | [base] | 55% | [calc] | 0% | [calc] | [calc] |
| Contingencia profesional IPT | [base] | 75% | [calc] | +30% | [calc] | [calc] |
| Contingencia profesional IPA | [base] | 100% | [calc] | +30% | [calc] | [calc] |

Note: percentages are reference rates — actual rate depends on contribution years and INSS resolution. Tag: `[verificar INSS — bases cotización reales]`

### Step 7: Output

Structure as:

```markdown
## IPT/IPA Analysis — [profession]

### Probable Grade: [IPT / IPA / IP / GI]

**Legal Basis:**
- LGSS Art. 194-200 (four grades)
- Ley 2/2025 (reasonable adjustments required)
- Jurisprudencia CENDOJ [verificar TSJ [region] precedent on similar diagnoses]

### Grade Rationale

[Paragraph explaining why this grade is most likely, citing specific functional losses vs. habitual profession demands]

Example:
"IPT is most likely because diagnoses (G83.4 spinal cord lesion, R15.9 incontinence, chronic pain G89.28) prevent >33% of conductor duties (continuous driving, emergency response, physical endurance) but residual capacity for desk work, supervisory roles, or administrative tasks exists. Age 48 and education suggest retraining feasible."

### Ley 2/2025 Status

[Has employer implemented reasonable adjustments? Any documented rejections?]

### Strengths of Your Case

| Strength | Citation |
|---|---|
| Diagnosis chronicity (onset [date], 7+ years) | LGSS Art. 194 (permanence) |
| Multiple organ systems (neuro, GI, psych) | Medical complexity favors higher grade |
| Prior ICAM ruling [if yes] | [Grade/date] — binding unless new evidence |
| Functional report confirms <33% capacity | [Physician/date] |

### Weaknesses / Challenges

| Weakness | Mitigation |
|---|---|
| Residual capacity for desk work unclear | Request formal occupational therapy evaluation |
| Age 48 — retraining feasible per jurisprudencia [verificar] | Argue cognitive/psychological barriers to retraining |
| Prognosis "stable" not improving | Emphasize irreversibility + 10-year diagnosis trajectory |

### Next Steps

**Immediate (weeks):**
- [ ] Request formal functional capacity evaluation (physiatrist)
- [ ] Collect employer documentation of adaptation requests + rejections
- [ ] Gather 10-year medical history from all treating providers
- [ ] Request prior ICAM reports/rulings (if applicable)

**If pursuing IPT/IPA (months):**
- [ ] File request with INSS (Art. 199 LGSS) or appeal existing ruling
- [ ] If rejected: ICAM procedure (independent medical review)
- [ ] If ICAM fails: judicial appeal to juzgado (procedimiento de revisión, Art. 213 LGSS)

**Attorney coordination:**
- Consult laboralista to plan ICAM/judicial strategy
- Consider contingency change (common→professional, Art. 156.2.f LGSS) in parallel
- Plan 30%+ pension boost from contingency change if available

---

## Key References

| Reference | Scope |
|---|---|
| **LGSS Art. 194-200** | Four disability grades, criteria |
| **Ley 2/2025** | Reasonable adjustments, contract termination reform |
| **STS [date] [verificar CENDOJ]** | Jurisprudencia IPT grade criteria |
| **ICAM Procedimiento** | Medical assessment, grounds for appeal |

---

## Disclaimer

```
BORRADOR DE TRABAJO — NO CONSTITUYE ASESORAMIENTO JURÍDICO — 
REVISAR CON ABOGADO LABORALISTA COLEGIADO EN ESPAÑA ANTES DE ACTUAR
```

This analysis is a draft estimate only. Actual grade determination is exclusive to ICAM (Inspección de Clase, Afiliación y Recaudación) or courts. Consult a qualified Spanish employment lawyer before filing claims or appeals.
