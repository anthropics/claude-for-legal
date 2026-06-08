---
name: leave-review
description: >
  Calculate leave entitlements and employer obligations for annual holiday,
  parental leave, maternity/paternity leave, and sick leave under Finnish,
  German, and EU law. Use when asked "how much holiday does this employee get?",
  "maternity leave rules in Finland", "German parental leave", "sick leave pay
  obligation", "can I recall someone from parental leave", or any leave
  entitlement question.
argument-hint: "[leave type] [jurisdiction] [employee tenure and status] — e.g. 'annual leave Finland 3 years' or 'parental leave Germany'"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:leave-review

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If placeholders, stop: "Run `/eu-legal:cold-start-interview` first."
2. Load `~/.claude/plugins/config/eu-legal/employment.md` if it exists. Read: hiring countries, fi_collective_agreement, de_tarifvertrag.
3. Identify leave type and jurisdiction from the argument.
4. Run the applicable framework below.
5. Output: entitlement, calculation, employer obligations, document requirements.

---

## Purpose

Leave entitlements under Finnish and German law exceed EU directive minimums significantly. The interaction with collective agreements (TES/Tarifvertrag) and individual contract terms can make the actual entitlement higher still. This skill calculates the floor; a lawyer or HR professional must verify against the applicable collective agreement.

---

## Step 1: Identify leave type

From the argument or by asking:
> "What type of leave are we looking at? (Annual holiday / Maternity leave / Paternity leave / Parental leave / Sick leave / Childcare leave / Other)"

Also confirm: jurisdiction (Finland / Germany / other EU) and employee details (tenure, whether collective agreement applies, full-time or part-time).

---

## Annual Holiday

### EU baseline (Working Time Directive 2003/88/EC Art. 7)
- **Minimum:** 4 weeks (20 working days) per year
- Cannot be replaced by pay-in-lieu except on termination
- Carried forward: national law rules; many member states allow limited carry-forward

### Finland — Vuosilomalaki (162/2005)

Call `mcp__velvoite__get_finnish_statute("VLL", "5")` for annual holiday accrual rates. Present accrual rates from the live statute text.

**Accrual rate:**
- First holiday year (April 1–March 31): 2 days per month employed
- After 1 full holiday year of employment (before end of first March 31 in employment): 2.5 days per month
- **2.5 days/month = 30 days = 6 weeks** after completing 1 full year of employment (holiday year runs April 1–March 31)

**Calculation:** multiply months worked in holiday year × accrual rate (2 or 2.5). Round up to whole days.

Example: employee has 3 years tenure, worked all 12 months of the holiday year → 12 × 2.5 = 30 days holiday entitlement.

**Holiday pay:**
- Salaried employees: full salary continues during holiday
- Hourly employees: holiday pay = 9% of earnings (≥1 year employment: 11.5%) — Vuosilomalaki §12

**Holiday bonus (lomakorvaus / lomaraha):**
Not a statutory minimum but standard in most collective agreements (TES): typically 50% of holiday pay as a bonus. If `fi_collective_agreement` is set in employment.md: note that the applicable TES likely includes lomaraha — verify with the TES text.

**Employer obligations:**
- Give holiday during the main holiday season (June 2–September 30) unless otherwise agreed
- Give notice of holiday timing at least 1 month before
- Cannot force all holiday below 24 days to be taken outside main season without agreement

### Germany — Bundesurlaubsgesetz (BUrlG)

**Minimum:** 20 working days per year (5-day week)
**Standard in practice:** 25–30 days — most collective agreements and individual contracts exceed the statutory minimum

**Full entitlement vests after:** 6 months employment (§4 BUrlG). Pro-rated in first 6 months: 1/12 per month.

**Calculation:** if contract specifies 25 days and employee has worked 6 months → full 25 days entitlement.

**Holiday pay:** full salary during holiday (§1 BUrlG)

**Carry-forward:** holiday not taken by year-end carries to March 31 of following year (§7(3) BUrlG). After March 31: lapses unless individual contract or TarV says otherwise. Note: CJEU Kreuziger/Max-Planck case — employer must actively request employee to take holiday or entitlement cannot lapse.

If `de_tarifvertrag` is set in employment.md: note that Tarifvertrag likely specifies higher entitlement — verify.

---

## Maternity Leave

### EU baseline (Pregnant Workers Directive 92/85/EEC)
- **Minimum:** 14 weeks maternity leave, at least 6 weeks must be post-birth
- Pay: at least sick pay level or equivalent

### Finland — äitiysvapaa

**Duration:** 40 working days (äitiysvapaa, TSL + sickness insurance act)
- Begins typically 30 working days before expected due date
- Can begin up to 50 working days before due date

**Pay:**
- Kela pays äitiysraha (maternity allowance) for the 40-day period
- Many TES require employer to top up to full salary — check `fi_collective_agreement`

**Employer obligations:**
- Cannot terminate employee due to pregnancy (TSL Ch. 7 §9) — void dismissal
- Must keep position open or offer equivalent role on return
- Employee must notify at least 2 months before leave starts

### Germany — Mutterschutz (MuSchG)

**Duration:**
- 6 weeks before expected due date (Mutterschutzfrist vor der Geburt) — cannot waive
- 8 weeks after birth (Mutterschutzfrist nach der Geburt); 12 weeks for premature birth or multiple birth

**Pay during Mutterschutz:**
- Employer pays Mutterschaftsgeld advance: daily pay up to €13/day
- Kasse (health insurer) pays the rest up to full net salary
- Net salary continues in full (§18 MuSchG)

**Dismissal protection:**
- §17 MuSchG: dismissal void during pregnancy and 4 months post-birth
- Employer must apply to Gewerbeaufsichtsamt for exceptional approval — rarely granted

---

## Paternity / Second-Parent Leave

### EU baseline (Parental Leave Directive 2019/1158 Art. 4)
- **Minimum:** 10 working days paternity leave around the time of birth
- Must be paid at sick pay level at minimum

### Finland — isyysvapaa

**Duration:** up to 54 working days, flexible timing within 2 years of birth
- New 2023 parental leave model: each parent has 160 days (kuukausittainen vanhempainraha). The old isyysvapaa concept merged into the new equal parental leave model.

**Pay:** Kela pays isyysraha at 70–90% of income. Many TES top up.

### Germany — Elternzeit (BEEG)

Paternity leave as a distinct concept is not mandatory in Germany beyond the EU minimum. The primary mechanism is Elternzeit (parental leave) — see below.

**Elterngeld:** payable to either parent; father can take leave simultaneously with mother or after.

---

## Parental Leave

### EU baseline (Parental Leave Directive 2019/1158 Art. 5)
- **Minimum:** 4 months per parent, of which 2 months are non-transferable
- Member states may make payment conditional on length of service (max 1 year)

### Finland — vanhempainvapaa (new 2023 model, Kela reform effective 1.8.2022)

**Duration per parent:** 160 working days (approximately 6.5 months) each
- Non-transferable: cannot give days to the other parent (equal model)
- Can be taken in segments; full flexibility within 2 years of birth
- Single parents: entitled to both parents' quota (320 days)

**Pay:** Kela pays vanhempainraha at 70–90% of earnings. Many TES top up for first portion.

**Hoitovapaa (childcare leave):** after vanhempainvapaa ends, parent may take unpaid leave until child turns 3 years old. Job protection: employer must offer the same or equivalent role on return.

**Employer obligations:**
- Cannot terminate employee on grounds of family leave (TSL)
- Must keep position open or offer equivalent role
- Employee must give 2 months notice of leave and 1 month notice of return

### Germany — Elternzeit (BEEG)

**Duration:** up to 3 years per child (each parent independently)
- Can be split into up to 3 periods before child's 8th birthday (§16 BEEG — 2015 reform)
- Both parents can take Elternzeit simultaneously
- Can work part-time up to 32h/week during Elternzeit (§15(4) BEEG)

**Pay (Elterngeld):**
- Basic Elterngeld (Basiselterngeld): 65–100% of net income, max €1,800/month, for 12 months (14 months if both parents take at least 2 months each)
- ElterngeldPlus: halved monthly amount over double the period
- Partnerschaftsbonus: extra 4 months each if both parents work 25–32h/week simultaneously

**Job protection:**
- §18 BEEG: employer cannot dismiss during Elternzeit; requires Gewerbeaufsicht approval
- Return right: same or equivalent position

**Employer obligations:**
- Employee must notify Elternzeit at least 7 weeks before it begins (§16 BEEG)
- Employer cannot unilaterally reduce notice period or change terms

---

## Sick Leave

### EU baseline
No EU minimum sick leave entitlement. National law governs.

### Finland

**Finnish employer sick pay obligation (TSL Ch. 2 §11):**
- Employment under 1 month: no statutory sick pay obligation
- Employment 1 month to 3 years: employer pays full salary for the duration of incapacity up to **9 working days** per illness episode
- Employment over 3 years: employer pays full salary up to **4 weeks** per illness episode (many collective agreements (TES) extend this to 28 days or longer regardless of tenure — check applicable TES)

**After employer sick pay period:**
- Kela pays sairauspäiväraha (sickness allowance) from day 2 of illness (omavastuu day 1): approximately 70% of income, up to 300 working days

**Employer obligations:**
- Request sickness certificate (lääkärintodistus) — after how many days is negotiated in TES or company policy; statutory: after 3 days
- Cannot terminate employment solely due to illness without examining redeployment possibilities

### Germany — EFZG (Entgeltfortzahlungsgesetz)

**Employer obligation:**
- Full salary (Lohnfortzahlung) for up to **6 weeks** (42 calendar days) per illness, per new illness episode
- "New episode" if employee has been healthy for >6 months between episodes of the same illness

**After 6 weeks:**
- Krankengeld from health insurer (Krankenkasse): 70% of gross salary (up to Beitragsbemessungsgrenze), for up to 78 weeks within a rolling 3-year period for the same illness

**Employer obligations:**
- After 4 weeks continuous sick leave: employer must offer bEM (betriebliches Eingliederungsmanagement — return-to-work integration management) before any illness-related dismissal; failure weakens dismissal grounds

---

## Step 3: Output format

For each leave type reviewed, output:

**Entitlement:** [number of days/weeks + basis]
**Pay obligation:** [employer obligation + state benefit + collective agreement note if applicable]
**Job protection:** [yes/no/conditions]
**Employer document requirements:** [what notices, certificates, forms are required and when]
**Collective agreement note:** [if TES/Tarifvertrag applies — may be more generous; verify against applicable agreement]

---

## Guardrail

> **RESEARCH NOTES — NOT LEGAL ADVICE.** Leave entitlements interact with collective agreements, individual contract terms, and Kela/Krankenkasse rules in ways that affect the actual entitlement. This analysis calculates the statutory floor. Verify the applicable TES or Tarifvertrag for enhanced entitlements, and confirm current Kela/Krankenkasse benefit levels before communicating entitlements to employees. [model knowledge — verify current benefit amounts] Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.