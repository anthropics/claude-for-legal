---
name: contingencia-cambio
description: Common→professional contingency procedure (RD 1430/2009, Art. 156.2.f LGSS)
argument-hint: "Diagnosis, job duties, employer response, medical evidence"
---

# Contingency Change: Common → Professional

## Purpose

Analyze viability and economic impact of changing contingency classification from **common** (enfermedad común) to **professional** (enfermedad profesional).

## Legal Framework

### Art. 156.2.f LGSS

Disease is classified as professional if:
- **Direct causation:** work activities directly caused the disease, OR
- **Aggravation:** disease existed but work conditions significantly aggravated it (empeoramiento)
- Work conditions must be **non-standard** for general population (hazards specific to job, industry, company negligence)

### RD 1430/2009 — Determinación de Contingencia

Procedure for classification change:
1. Worker or representative files request with INSS
2. ICAM (Inspección) investigates: medical evidence + workplace conditions
3. ICAM issues determination (common or professional)
4. If rejected: appeal to juzgado (procedimiento contencioso-administrativo)

### Art. 25 LPRL — Employer Duty

Employer must:
- Identify and assess workplace hazards
- Implement prevention measures
- Adapt work to individual (especially workers with health conditions)
- **Documented failure or negligence = evidence for Art. 156.2.f claim**

### Art. 164 LGSS — Recargo de Prestaciones

If professional contingency + employer violated LPRL:
- **30-50% increase** in disability pension
- Applied retroactively to disease onset
- Can add €10k-50k+ over lifetime pension

---

## Workflow

### Step 1: Establish Medical Causation

Ask:
- **Diagnosis (CIE-10)?** (e.g., "G83.4 spinal cord lesion")
- **Was diagnosis pre-existing or onset during employment?**
  - Pre-existing: when? age? severity before work?
  - Onset during work: when? under what circumstances?
- **Has any medical provider stated causation or aggravation?** (yes/no/date/provider)
- **Medical opinion: work-related Yes/No?**

Record: `[diagnosis]`, `[onset_work_or_preexisting]`, `[medical_opinion_causation]`

---

### Step 2: Job Duties and Hazards

Ask:
- **Job title and main duties?**
- **Physical demands:** (e.g., "driving 8h/day, vibration, sitting posture, stress")
- **Environmental hazards:** (e.g., "noise >85dB", "chemical exposure", "shift work", "ergonomic poor")
- **Duration in role:** (from/to dates)
- **Were hazards documented by company?** (safety assessments, OHS records)
- **Any prior complaints or incidents?** (accident, near-miss, injury on job)

Record: `[job_title]`, `[duties]`, `[hazards]`, `[duration]`, `[documented_hazards]`

---

### Step 3: Employer Response

Ask:
- **Did employer acknowledge job-related risk?** (yes/no/silent)
- **Did employer implement prevention measures?** (safety equipment, schedule adjustments, ergonomic improvements, reallocation)
- **Medical report from occupational medicine physician (empresa)?** (yes/date/content)
- **Did employer adapt work when you reported health issues?** (yes/no/how/when)
- **Any documented evidence of negligence?** (ignored medical advice, ignored safety violations, continued hazardous duty despite health condition)

Record: `[employer_acknowledgment]`, `[prevention_measures]`, `[medical_report_empresa]`, `[adaptation]`, `[negligence_evidence]`

---

### Step 4: Analyze Art. 156.2.f Test

Create decision matrix:

| Test | Result | Implication |
|---|---|---|
| **Medical causation** | [Onset during work / Pre-existing but aggravated] | ✅ Supports common→professional |
| **Diagnosis expected in general population?** | [Yes, rare / Common but worsened] | ✅ Specific to hazards → professional |
| **Hazard non-standard?** | [Yes, specific to job / industry] | ✅ Supports professional |
| **Employer documented hazard?** | [Yes / No] | ✅ Yes = negligence evidence |
| **Employer ignored medical advice?** | [Yes / No / N/A] | ✅ Yes = Art. 25 LPRL breach |
| **Employer adapted work?** | [No / Refused / Attempted but failed] | ✅ No/Refused = stronger case |

### Step 5: Economic Impact Table

Create scenario table comparing common vs. professional:

| Aspect | **Common Contingency** | **Professional Contingency** | **Impact** |
|---|---|---|---|
| **Base Regulatory** | Reduced (carencia, calculation rules) | 100% (no carencia) | +15-30% increase |
| **Disability Grade** | IPT assessed on common basis | Same IPT, but professional classification | No change per se |
| **Recargo Prestaciones (Art. 164)** | None | +30-50% if LPRL violated | +30-50% boost |
| **Occupation Pension** | Common rules, capital reduced | Professional, capital increased | +20-40% capital |
| **Duration** | Limited (365-730 days IT) | Longer/indefinite if professional | Indefinite professional pension |
| **Lump Sum Example** | 60,000€ IPT common | 60,000€ IPT × 1.4 (recargo) = 84,000€ | **+24,000€** |
| **Monthly Pension 2026** | 1,200€ common | 1,200€ × 1.4 = 1,680€/month | **+480€/month** |
| **30-Year Value** | 432,000€ lifetime | 604,800€ lifetime | **+172,800€** |

**Note:** Figures are illustrative. Actual amounts depend on:
- Salary regulador (earnings base)
- Grade assigned (IP/IPT/IPA/GI)
- Recargo % applied (30-50%)
- Pensioner's lifespan

---

### Step 6: Argumentary for INSS Request

Draft outline for formal request:

```markdown
## Argumentación Cambio Contingencia
### Solicitud a INSS (RD 1430/2009)

**Trabajador:** [Name, NIF, empresa]
**Enfermedad:** [CIE-10, diagnosis]
**Solicitud:** Cambio contingencia común → profesional (Art. 156.2.f LGSS)

#### Hechos Probados

1. **Causación médica:** [Diagnosis onset during employment / pre-existing but significantly aggravated by job]
   - Evidence: [Medical reports, dates, providers]
   
2. **Especificidad del riesgo:** [Hazard specific to job, non-standard for general population]
   - Evidence: [Job description, hazard analysis, industry norms]
   
3. **Incumplimiento empleador (Art. 25 LPRL):** [Employer failed to adapt work, ignored medical advice, continued hazardous duty]
   - Evidence: [Emails, medical reports to employer, labor inspector reports, dates]

4. **Resultado:** [Disability (IPT/IPA/IP) attributable to job]
   - ICAM assessment pending / date of prior ruling

#### Base Legal

- Art. 156.2.f LGSS (enfermedad profesional por agravación)
- Art. 25 LPRL (deber adaptación)
- Art. 164 LGSS (recargo prestaciones + incumplimiento)
- RD 1430/2009 (procedimiento determinación)

#### Petitorio

1. Reclasificación contingencia común → profesional
2. Recargo prestaciones 30-50% (Art. 164)
3. Retroactivity desde fecha enfermedad

**Firma abogado/trabajador**
```

---

### Step 7: Documentation Checklist

Create actionable checklist:

```markdown
## Documentation to Gather (ANTES de solicitud)

**Medical Evidence:**
- [ ] Medical records from occupational medicine (empresa)
- [ ] Treatment records (especialista, hospital) with diagnostic dates
- [ ] Functional capacity evaluation
- [ ] Prior ICAM ruling (if exists)
- [ ] Letter from treating physician stating work-related causation or aggravation

**Work Documentation:**
- [ ] Job description (empresa)
- [ ] Contract (type, duration, hazards clause)
- [ ] Safety assessment or hazard analysis (if empresa has)
- [ ] Work schedule, rotation
- [ ] Photos/video of worksite (hazards visible)
- [ ] Incident/accident reports (if applicable)

**Employer Response:**
- [ ] Emails requesting accommodation (with dates/responses)
- [ ] Medical reports from empresa occupational physician
- [ ] Any letters from empresa acknowledging health issue
- [ ] Copies of refusals or negligence (in writing if possible)

**Labor Inspection / Union Records:**
- [ ] Labor inspector reports (if CCOO/UGT filed complaint)
- [ ] Union documentation of workplace conditions
- [ ] Witness statements from coworkers (same hazards, similar illnesses)

**Expert Opinion:**
- [ ] Letter from external toxicologist, ergonomist, or occupational health specialist
  - Stating: hazard non-standard, causation plausible, employer negligence evident
```

---

### Step 8: Timing and Procedure

Explain INSS procedure:

```markdown
## INSS Procedure Timeline

**Phase 1: Request (Week 1)**
- File with INSS Afiliación y Recaudación (if IT ongoing)
- Or file with ICAM directly (if claiming occupational disease retroactively)
- Include medical + work documentation

**Phase 2: ICAM Investigation (Weeks 2-12)**
- Inspección visits workplace (if requested + contested)
- Reviews medical evidence
- May request additional docs

**Phase 3: Determination (Weeks 12-16)**
- ICAM issues "Acta de Determinación de Contingencia"
- Ruling: common or professional

**Phase 4: Appeal (if rejected)**
- File recurso de reposición (28 days)
- If rejected again: appeal to juzgado
- Judicial timeline: 12-36 months

**If Professional + Art. 164 Breach:**
- Recargo automatically applied (30-50%)
- Retroactive to disease onset date
```

---

### Step 9: Output

Structure final report:

```markdown
## Contingency Change Analysis — [Worker]

### Viability Assessment: [High / Moderate / Low]

**Overall:** [1-2 sentence summary of viability]

### Art. 156.2.f LGSS Test Results

[Decision matrix from Step 4]

### Economic Impact (If Successful)

[Table from Step 5 showing common vs. professional scenarios]

### Case Strengths

- [Medical causation documented]
- [Employer negligence evidence]
- [Prior rulings on similar cases [verificar CENDOJ]]

### Case Risks

- [Burden of proof on worker]
- [Employer may dispute causation]
- [ICAM may rule disease pre-existing despite aggravation]

### Recommended Next Steps

1. **Gather documentation** (checklist above)
2. **Secure medical opinion** (independent toxicologist/ergonomist letter)
3. **File INSS request** (RD 1430/2009, include all evidence)
4. **Parallel: Contingency change claim + IPT/IPA claim** (both can proceed)
5. **Retain laboralista** (for ICAM defense if contested)

### Timeline

- Request filing: Week 1
- ICAM investigation: Weeks 2-12
- Determination: Week 16
- Appeal (if needed): Weeks 17-48
- Judicial (if needed): Months 12-36

### Attorney Coordination

Consult laboralista specializing in **occupational disease / Art. 156.2.f** — not all laboralistas handle procedimiento administrativo before juzgado.
```

---

## Key References

| Reference | Scope |
|---|---|
| **Art. 156.2.f LGSS** | Professional disease (causation + aggravation) |
| **RD 1430/2009** | Determinación contingencia procedure |
| **Art. 25 LPRL** | Employer duty to adapt + negligence |
| **Art. 164 LGSS** | Recargo prestaciones (30-50%) |
| **STS [verificar CENDOJ]** | Jurisprudencia on professional causation |

---

## Disclaimer

```
BORRADOR DE TRABAJO — NO CONSTITUYE ASESORAMIENTO JURÍDICO — 
REVISAR CON ABOGADO LABORALISTA COLEGIADO EN ESPAÑA ANTES DE ACTUAR
```

This analysis is draft only. Actual determination is exclusive to ICAM or courts. Consult a qualified Spanish employment lawyer before filing requests or appeals. Viability assessment may change with additional evidence.
