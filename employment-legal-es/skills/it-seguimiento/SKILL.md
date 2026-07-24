---
name: it-seguimiento
description: Sick leave (IT) timeline — day 365/545/730, payer changes, required actions
argument-hint: "Sick leave start date (YYYY-MM-DD)"
---

# IT Seguimiento: Sick Leave Timeline

## Purpose

Calculate key dates and required actions from sick leave start through potential termination.

## Legal Framework

### LGSS Sick Leave Rules

| Day | Event | Legal Basis | Action Required |
|---|---|---|---|
| **Day 1-365** | Automatic extension | LGSS Art. 196 | None (automatic) |
| **Day 365** | Extension decision point | LGSS Art. 196 | Request prórroga OR stop paying (empresa) |
| **Day 545** | Possible payer change | LGSS Art. 197 | Check: still empresa pagando or changed to INSS? |
| **Day 730** | Maximum IT duration | LGSS Art. 198 | Decision: IPT/IPA claim OR terminate contract |

### Key Rules

**Payer: Empresa vs INSS**
- Days 1-365: Employer pays 100% salary (delegada system) OR INSS directly (non-delegada)
- Day 365: Employer may request replacement by INSS (cost relief)
- Day 545: Latest point for payer change (employer → INSS)
- Day 730: INSS takes over entirely (if still on IT)

**Extension (Prórroga)**
- Automatic at day 365 (LGSS Art. 196.2) — payment continues
- Possible extension to day 545 for re-evaluation (médico del tribunal)
- Beyond day 545: ICAM decision (IPT probable) or return to work

**Termination**
- Day 730: IT maximum (Art. 198.2)
- Options: (a) IPT/IPA declared → permanent pension, or (b) return to work, or (c) contract extinction (justo motivo)

---

## Workflow

### Step 1: IT Start Date

Ask: **When did your sick leave (IT) start? (YYYY-MM-DD)**

Record: `[start_date]` (e.g., "2025-03-10")

### Step 2: Calculate Key Dates

Using formula:
```
Day 1 = [start_date]
Day 365 = Day 1 + 365 days
Day 545 = Day 1 + 545 days
Day 730 = Day 1 + 730 days
Today = [current date]
Days elapsed = Today - Day 1
Days remaining (until max 730) = 730 - Days elapsed
```

Example:
```
Start: 2025-03-10
Day 1: 2025-03-10
Day 365: 2026-03-10 (automatic extension)
Day 545: 2026-08-07 (possible payer change)
Day 730: 2027-03-10 (maximum IT)

Today: 2025-05-14
Days elapsed: 65
Days remaining: 665
```

### Step 3: Current Status

Ask:
- **How long have you been on IT? (days or estimated months)**
- **Is employer still paying your salary?** (yes/no/uncertain)
- **Has INSS taken over payment yet?** (yes/no/unknown)
- **Have you had any formal medical review by tribunal médico?** (yes/no/date)
- **Any communication from empresa or INSS about prórroga or termination?** (yes/describe)

Record: `[current_status]`, `[payer_status]`, `[medical_reviews]`, `[communications]`

### Step 4: Timeline Output

Create detailed timeline:

```markdown
## IT Timeline — [Start Date to Today]

### Current Status
- **IT Start:** [start_date]
- **Days elapsed:** [X days] (approximately [Y months])
- **Days remaining (until day 730):** [Z days]
- **Current payer:** [empresa / INSS / unknown]
- **Phase:** [extension phase / re-evaluation phase / terminal phase]

### Key Dates & Milestones

#### ✅ Day 1 → Day 365: Automatic Extension Phase

| Date | Day | Event | Status | Action |
|---|---|---|---|---|
| [start_date] | 1 | IT declared | [✅ Completed] | — |
| [date +30] | 31 | Monthly check-in (empresa) | [Expected] | Keep employer updated |
| [date +180] | 180 | Mid-year assessment | [Expected] | Request status from empresa |
| [date +365] | 365 | **Automatic extension** | [Upcoming/Completed] | **No action required** — continues automatic |

**Key Point:** Extension at day 365 is **automatic**. No request needed. Payment continues (empresa or INSS).

---

#### ⚠️ Day 365 → Day 545: Re-evaluation Phase

| Date | Day | Event | Legal Basis | Action Required |
|---|---|---|---|---|
| [date +365] | **365** | **Extension confirmed** | LGSS Art. 196.2 | Notify employer of continued IT status |
| [date +365+14] | 379 | (approx) Request formal evaluation | Empresa option | Empresa MAY request tribunal médico review |
| [date +400] | ~400 | Medical review period | Tribunal médico | **You:** Request independent medical evaluation [verificar regional rules] |
| [date +545] | **545** | **Deadline: Payer change or decision** | LGSS Art. 197 | **CRITICAL:** Check with INSS if employer switching payment |

**Key Point:** Around day 365-400, employer often requests **tribunal médico** (medical court review) to evaluate prognosis. This is when IPT/IPA claims typically are evaluated in parallel.

---

#### 🔴 Day 545 → Day 730: Terminal Phase

| Date | Day | Event | Legal Basis | Action Required |
|---|---|---|---|---|
| [date +545] | **545** | **Payer change deadline** | LGSS Art. 197 | **ACTION REQUIRED:** 1) Confirm INSS payment if changed; 2) If still empresa → request INSS takeover |
| [date +600] | 600 | ICAM decision window | RD 1430/2009 | ICAM likely issues IPT/IPA determination |
| [date +700] | 700 | Pre-termination review | LGSS Art. 198 | Prepare: if ICAM rejects IPT → plan return to work OR challenge ruling |
| [date +730] | **730** | **MAXIMUM IT DURATION** | LGSS Art. 198.2 | **CRITICAL DECISION POINT:** (a) IPT/IPA confirmed → permanent pension; (b) return to work; (c) contract termination |

**Key Point:** IT **cannot exceed 730 days**. At this point, one of three things must happen:

1. **IPT/IPA declared** → you transition to permanent disability pension (LGSS Art. 197.3)
2. **Return to work** → you resume job (or modified role if Ley 2/2025 adaptations)
3. **Contract termination** → justo causa extinction (medical grounds, Art. 49 ET) OR negotiated severance

---

### Step 5: Employer Payer Status

Ask:
- **At day 365, did employer notify you of extension?** (yes/no/uncertain)
- **At day 545 (approx), has employer mentioned payer change?** (yes/no/silent)
- **Are you receiving payment currently?** (yes, from empresa / yes, from INSS / uncertain)
- **Any documentation of payer change?** (letters, email, bank changes)

Inform:

```markdown
#### Payer Status Check

**Your situation:**
- [If before day 365:] Employer MUST be paying 100% (empresa delegada) or INSS directly. If no payment → contact INSS/empresa immediately.
- [If day 365-545:] Employer likely paying, but may request INSS takeover. **ACTION:** Request confirmation from INSS (sede.seg-social.gob.es "Tu Seguridad Social" → Prestaciones IT) of current payer and amounts.
- [If after day 545:] INSS MUST be paying (or INSS already was). If receiving from empresa after day 545 → notify INSS immediately (may be overpayment).

**Next Action:**
- [ ] Log into https://sede.seg-social.gob.es (with cl@ve or certificado digital)
- [ ] Navigate to "Tu Seguridad Social" → "Prestaciones" → "Incapacidad Temporal"
- [ ] Verify: payer (empresa/INSS), amount, pago próximo (next payment date)
- [ ] Screenshot or document payer status for records
```

---

### Step 6: Parallel Proceedings

Add subsection on concurrent actions:

```markdown
### Parallel Actions (Concurrent with IT Timeline)

**During days 1-365:**
- Gather medical evidence for IPT claim (diagnoses, functional capacity reports)
- Request occupational health evaluation (external, independent)
- Document employer's response (or lack) to requests for accommodation (Ley 2/2025)

**During days 365-545 (Re-evaluation phase):**
- Cooperate with tribunal médico evaluation (do not skip appointments)
- Provide functional capacity documentation
- File IPT/IPA claim with INSS if not already filed
- Consider contingency change claim (common→professional, Art. 156.2.f) in parallel
- If employer applies for IT extension → medical evidence critical

**During days 545-730 (Terminal phase):**
- ICAM determination expected (approx day 600)
- If IPT/IPA rejected: prepare appeal (judicial review, Art. 213 LGSS)
- If IPT/IPA approved: confirm transition to permanent pension (Art. 197.3 LGSS)
- If return to work required: plan role with Ley 2/2025 adjustments

**Beyond day 730:**
- Impossible to remain on IT
- Must have concrete decision (permanent pension OR return/termination)
- If disputed: judicial process ongoing (can continue parallel to termination)
```

---

### Step 7: Action Checklist

Provide simple checklist by phase:

```markdown
## Action Checklist

### Phase 1: Days 1-365 (Automatic Extension)
- [ ] Document IT start date and first payment
- [ ] Receive notice of next appointment from empresa/INSS
- [ ] Gather medical evidence (diagnoses, test results, functional assessments)
- [ ] Request independent occupational health evaluation
- [ ] (Optional) File contingency change claim (Art. 156.2.f LGSS)

### Phase 2: Days 365-545 (Re-evaluation Window)
- [ ] ⚠️ Day 365: Confirm extension (should be automatic, no action needed unless empresa contests)
- [ ] Around day 365-400: Tribunal médico may request appointment — do NOT skip
- [ ] Day 400-500: File IPT/IPA claim if not already filed (INSS or ICAM)
- [ ] Day 500: Confirm payer status (INSS portal "Tu Seguridad Social")
- [ ] Day 545: **ACTION REQUIRED** — Confirm payer change or status with INSS

### Phase 3: Days 545-730 (Terminal Phase)
- [ ] Around day 600: Await ICAM determination letter (IPT/IPA grade or rejection)
- [ ] Day 700: Prepare contingency plan:
  - [ ] If IPT approved: secure transition documents to permanent pension
  - [ ] If rejected: prepare appeal (juzgado) AND return-to-work plan
  - [ ] If uncertain: request extension of evaluation period [verificar regional practice]
- [ ] Day 720: Final decision point — one of three paths must be chosen

### Beyond Day 730
- **Path A (IPT/IPA approved):**
  - [ ] Submit request for permanent pension (Art. 197.3 LGSS)
  - [ ] Transition to CLNP (Pensión Permanente)
  
- **Path B (Return to work):**
  - [ ] Coordinate with empresa on role with Ley 2/2025 adjustments
  - [ ] Request accommodation (Ley 2/2025) before accepting unmodified return
  
- **Path C (Termination):**
  - [ ] Negotiate severance OR file wrongful termination claim
  - [ ] Continue IPT/IPA appeal in parallel (pension claim not lost by termination)
```

---

### Step 8: Output

Format final timeline as:

```markdown
## IT Timeline — [Worker] — [Start Date] to Day 730

### Summary

- **IT Start:** [start_date]
- **Today:** [current_date]
- **Days elapsed:** [X] days ([Y] months)
- **Days remaining:** [Z] days (until maximum day 730)
- **Current phase:** [Automatic Extension / Re-evaluation / Terminal]
- **Current payer:** [empresa / INSS / uncertain]
- **Status:** [On track / At risk (reason) / Decision point]

### Timeline (Detailed)

[Table from Step 4 with your specific dates]

### Current Obligations

[Specific actions required in your phase]

### Next Milestone

[Immediate next date and action required]

### Important Notes

1. IT is automatic — do NOT assume contract is terminated
2. Payer change (empresa→INSS) is automatic if day 545 reached, but verify
3. Day 730 is hard limit — one decision must be made
4. IPT/IPA claim MUST be filed before day 730 (or rights lost)
5. If ICAM rejects IPT → appeal to juzgado (does NOT reset day 730 clock)

### Attorney Coordination

Consult laboralista specializing in IT procedures + IPT claims to prepare for terminal phase (day 545-730).
```

---

## References

| Reference | Scope |
|---|---|
| **LGSS Art. 196-198** | IT duration, extension, termination |
| **Art. 197.3 LGSS** | Transition to permanent pension on day 730+ |
| **Ley 2/2025** | Return-to-work adjustments |
| **RD 1430/2009** | ICAM procedure + determination timeline |

---

## Disclaimer

```
BORRADOR DE TRABAJO — NO CONSTITUYE ASESORAMIENTO JURÍDICO — 
REVISAR CON ABOGADO LABORALISTA COLEGIADO EN ESPAÑA ANTES DE ACTUAR
```

This timeline is informational. Regional variations and individual circumstances may alter dates/procedures [verificar with regional INSS office]. Consult a qualified Spanish employment lawyer for your specific situation.
