---
name: plan-pensiones-ipt
description: Occupational pension plan + IPT capital scenarios (carencia, collective agreement)
argument-hint: "Plan name, entry date, reglament/key terms, salary regulador"
---

# Plan de Pensiones de Empleo + IPT

## Purpose

Analyze IPT (Incapacidad Permanente Total) capital in occupational pension plans under LGSS Art. 179 + plan reglament.

Key variables: carencia (waiting period), capital assegurado (insured amount), acuerdos sindicales (collective agreement overrides).

## Legal Framework

### LGSS Art. 179 — Pensión en Régimen de Jubilación

Occupational pension plan (plan de pensiones de empleo) typically:
- Covers retirement, disability (IPT/IPA), death
- Capital formula: X × salario regulador (varies by reglament)
- Carencia requirement: typically 3 years (can be waived by agreement)
- IPT capital: usually 50-100% of retirement capital (depends on reglament)

### Key Terms

**Salario Regulador**
- Average pensionable salary, typically last 12-24 months
- Calculation per reglament (differs by plan)
- Example: last 24 months ÷ 24 = average monthly salary

**Capital Assegurado (Insured Amount)**
- Formula: X × salario regulador (X = coefficient per reglament, 3-4 typical)
- Example: 3.5 × 28,000€ annual salary = 98,000€ capital

**Carencia (Waiting Period)**
- Standard: 3 years from entry into plan
- If <3 years + IPT declared → capital may be forfeit or reduced
- Exception: collective agreement may waive or reduce carencia for IPT (Art. 156.2.f cases)

**Compatibilidad (Compatibility)**
- IPT common: pension INCOMPATIBLE with continuation of employment
- IPT professional: pension INCOMPATIBLE with continuation (contract terminated)
- IPA: pension usually INCOMPATIBLE with any professional activity
- Important: occupational pension can coexist with INSS IPT pension (both received)

---

## Workflow

### Step 1: Plan Identification

Ask:
- **Plan name?** (e.g., "VidaCaixa P.P.E. TB", "Caja Ingenieros", "Santander Ocupación")
- **Plan manager/gestora?** (VidaCaixa, Santander, AXA, etc.)
- **Entry date into plan?** (YYYY-MM-DD)

Record: `[plan_name]`, `[gestora]`, `[entry_date]`

---

### Step 2: Reglament & Key Terms

Ask:
- **Do you have a copy of the plan reglament?** (yes/no/partial)
- **If yes: What is the capital formula for IPT?** (e.g., "3.5 × salario regulador")
- **Carencia period stated?** (typically 3 years; any exceptions for IPT?)
- **What is the salario regulador definition?** (last 12/24 months? how calculated?)
- **Are collective agreements mentioned in the reglament?** (check if CCOO/UGT may have modified terms)

Record: `[reglament_available]`, `[capital_formula]`, `[carencia]`, `[salary_definition]`, `[collective_agreement_clause]`

**If reglament not available:**
- Request from plan gestora (legal obligation to provide)
- Document request date (shows diligence)
- Use estimated formula pending receipt

---

### Step 3: Salary Regulador Calculation

Ask:
- **Salary before baja IT (latest 12-24 months)?**
- **Nóminas from last 24 months?** (yes/partial/no)

Collect sample:
```
Jan 2024: €2,200
Feb 2024: €2,200
...
Dec 2024: €2,200
Jan 2025: €2,200
Feb 2025: €2,200 (last month before baja IT 10-mar-2025)

Salario regulador = sum(24 months) ÷ 24
              = (24 × €2,200) ÷ 24 = €2,200 average
```

Record: `[salario_regulador]`

---

### Step 4: Carencia Analysis

Create scenario table:

| Scenario | Entry Date | Baja IT Date | Carencia 3 Years Satisfied? | Implication |
|---|---|---|---|---|
| **Case A: >3 years** | 2022-01-15 | 2025-03-10 | ✅ YES (3.16 years) | Full capital eligible |
| **Case B: <3 years** | 2024-03-15 | 2025-03-10 | ❌ NO (0.99 years) | Capital forfeited UNLESS exception |
| **Case C: Borderline** | 2022-03-15 | 2025-03-10 | ✅ YES (exactly 3.00) | Full capital (verify exact date rules) |

Ask:
- **How many years between entry date and baja IT date?**
- **Does your plan reglament mention carencia waiver for occupational disease (Art. 156.2.f)?** (yes/no/unknown)
- **Has there been any CCOO/UGT agreement modifying carencia for IPT?** (yes/no/unknown)

Record: `[years_in_plan]`, `[carencia_met]`, `[exception_clause]`

---

### Step 5: Collective Agreement Impact

Ask:
- **Is your company affiliated with collective bargaining?** (CCOO, UGT, CSIF, other)
- **Has a collective agreement been negotiated for plan pensiones terms?** (yes/no/unknown)
- **If yes: Do you know of any exception for IPT causation?** (e.g., "60% capital despite <3 years carencia")

Record: `[collective_agreement]`, `[ipt_exception]`

**Common Exception Example:**
- CCOO TMB agreement (Art. 156.2.f driver cases): "Plan capital 60% payable despite carencia, if causation common→professional proven"
- Not universal — varies by sector, company, year

---

### Step 6: Calculate Scenarios

Create **three-scenario table:**

```markdown
## Plan Pension IPT Capital Scenarios

### Your Situation
- **Plan:** [plan_name]
- **Entry:** [entry_date]
- **Baja IT:** [baja_it_date]
- **Years in plan:** [X.XX years]
- **Salario regulador:** €[amount]
- **Capital formula:** [formula] (per reglament)
- **Carencia:** [3 years / other]
- **Collective agreement:** [yes/no + details]

---

### Scenario 1: Literal Reglament (Carencia Applied)

| Item | Amount |
|---|---|
| Salario regulador | €[amount] |
| Capital formula (3.5×) | €[amount × 3.5] |
| Carencia status | <3 years → forfeited [if case B] |
| **Capital to receive** | **€0 (or % if partial carencia)** |
| Derechos consolidados | €[X] (always received, no carencia) |
| **TOTAL** | **€[X]** |

**Implication:** Only vested rights (aportaciones + interés técnico), no full disability capital.

---

### Scenario 2: Collective Agreement Exception (60% + Carencia Waived)

| Item | Amount |
|---|---|
| Salario regulador | €[amount] |
| Capital formula (3.5×) | €[amount × 3.5] |
| Collective agreement override | 60% despite carencia |
| **Capital to receive (60%)** | **€[amount × 3.5 × 0.6]** |
| Derechos consolidados | €[X] (included in above) |
| **TOTAL** | **€[amount × 3.5 × 0.6]** |

**Implication:** Partial capital due to collective agreement (Art. 156.2.f IPT cases).

---

### Scenario 3: No Carencia (Waived by Reglament or Court)

| Item | Amount |
|---|---|
| Salario regulador | €[amount] |
| Capital formula (3.5×) | €[amount × 3.5] |
| Carencia waived | Court/reglament exception |
| **Capital to receive (100%)** | **€[amount × 3.5]** |
| Derechos consolidados | Included above |
| **TOTAL** | **€[amount × 3.5]** |

**Implication:** Full capital (best case).

---

### Summary Table

| Scenario | Capital | Likelihood | Action |
|---|---|---|---|
| **Literal (carencia)** | €[0-X] | [High/Medium/Low] | Verify reglament language |
| **Collective agreement** | €[Y] | [High/Medium/Low] | Request agreement from CCOO/UGT |
| **No carencia (court)** | €[Z] | [High/Medium/Low] | Legal argument only if challenged |

**Most likely scenario:** [Scenario X based on your facts]
```

---

### Step 7: Occupational Pension + INSS IPT Compatibility

Explain:

```markdown
## Compatibility: Plan Pension + INSS IPT

### IPT (Incapacidad Permanente Total) Scenario

If you are declared IPT (total permanent disability):

| Pension | Amount | Compatibility | Notes |
|---|---|---|---|
| **Plan (Ocupacional)** | €[capital or monthly] | ✅ Received | Lump sum capital OR monthly renta (plan terms) |
| **INSS (IPT pensión)** | €[1,200-1,700/month estimate] | ✅ Received | 100% of base reguladora |
| **Employment** | €0 | ❌ NOT compatible | IPT = contract terminated (Ley 2/2025 adjustments req'd first) |

**Total monthly income (IPT case):** Plan monthly + INSS monthly = combined income

### IPA (Incapacidad Permanente Absoluta) Scenario

If IPA (absolute disability):

| Pension | Amount | Compatibility | Notes |
|---|---|---|---|
| **Plan (Ocupacional)** | €[may be reduced per reglament] | ✅ Received | Plan terms for IPA (may be higher than IPT) |
| **INSS (IPA pensión)** | €[1,800-2,200/month estimate] | ✅ Received | Higher base than IPT |
| **Employment** | €0 | ❌ NOT compatible | IPA = no professional activity |

**Important:** IPA may be INCOMPATIBLE with ANY occupational activity (not just employment). Verify plan reglament.
```

---

### Step 8: Questions for Gestora

Provide checklist for plan manager inquiry:

```markdown
## Questions for Plan Gestora

Send formal written request to your plan gestora (email + registered mail if critical):

1. **Plan regulations:** Provide full current reglament (Spanish or original language)

2. **Capital formula for IPT:** Confirm exact formula in Art. 15-20 reglament

3. **Carencia for IPT:** Does carencia apply to IPT? Any exceptions for:
   - Occupational disease (Art. 156.2.f LGSS)?
   - Work-related injury (accident)?
   - Collective agreement override?

4. **Salario regulador:** Confirm how it's calculated for your plan (last 12/24 months? includes/excludes what?)

5. **Collective agreement:** Is your plan subject to CCOO/UGT/CSIF agreement modifying terms? Request copy.

6. **Derechos consolidados:** If carencia not met, what consolidated rights are guaranteed?

7. **IPT capital estimate:** Given your entry date [date] + salario regulador €[amount], what is estimated IPT capital under:
   - Literal reglament (with carencia)
   - If carencia waived (per agreement/exception)
   - If occupational disease (Art. 156.2.f)

8. **Payment method:** Lump sum or monthly renta? Any options for Nelson to choose?

9. **Timeline:** When would capital be paid after IPT declared?

10. **Marital status/beneficiaries:** If you die before payment, who receives capital?

**Request completion deadline:** 15-30 days (legal obligation per Art. 18 LPS Planes Pensiones)
```

---

### Step 9: Output

Format final analysis:

```markdown
## Plan de Pensiones IPT Analysis — [Plan Name]

### Key Facts
- **Plan:** [plan_name]
- **Gestora:** [gestora]
- **Entry date:** [entry_date]
- **Years accrued:** [X.XX years]
- **Carencia status:** [Met / Not met (exception possible)]
- **Salario regulador:** €[amount/year]
- **Capital formula:** [formula, e.g., "3.5 × regulador"]
- **Collective agreement:** [Yes + details / No / Unknown]

### Capital Scenarios

[Table from Step 6 with your specific figures]

### Most Likely Scenario

**Capital to receive (IPT case):** €[most likely amount]

**Basis:** [Reglament literal / Collective agreement / Exception argument]

**Confidence level:** [High/Medium/Low]

### Compatibility with INSS

**IPT + Plan + INSS monthly pension:** All three compatible
- Plan capital: €[X] (lump sum or monthly)
- INSS IPT pension: €[Y]/month
- Combined monthly income: €[Z] (if plan paid monthly)

### Action Items

1. **Obtain reglament** from gestora (if not already have)
2. **Verify collective agreement** via CCOO/UGT representative (if applicable)
3. **Confirm salario regulador** with gestora (based on last 24 months)
4. **If carencia uncertain:** Request written opinion from gestora
5. **Plan for IPT transition:** Understand payment method + timing once declared

### Attorney Coordination

Consult laboralista to:
- Review reglament carencia clause for any exception
- Investigate collective agreement (may improve capital significantly)
- Plan timing: file IPT claim + plan capital request simultaneously
- Explore contingency change claim (Art. 156.2.f) to strengthen IPT + plan capital case

---

## Disclaimer

```
BORRADOR DE TRABAJO — NO CONSTITUYE ASESORAMIENTO JURÍDICO — 
REVISAR CON ABOGADO LABORALISTA COLEGIADO EN ESPAÑA ANTES DE ACTUAR
```

Capital figures are estimates based on assumed reglament terms. Verify with plan gestora for official figures. Carencia rules vary significantly by plan and agreement — do not assume without written confirmation. Consult a qualified Spanish employment lawyer before relying on capital projections.
```

---

## References

| Reference | Scope |
|---|---|
| **LGSS Art. 179** | Pensión régimen jubilación (includes disability) |
| **Reglament del Plan** | Authoritative source for capital formula, carencia, definitiones |
| **Collective agreements** | CCOO, UGT, CSIF may modify carencia/capital terms |
| **Art. 156.2.f LGSS** | IPT due to occupational aggravation (may affect carencia) |
| **Ley 2/2025** | May affect compatibility between plan + employment |
