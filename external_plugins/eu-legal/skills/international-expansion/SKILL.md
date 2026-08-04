---
name: international-expansion
description: >
  Legal checklist for hiring in a new EU country — presence type, employment
  contract requirements, works council thresholds, collective agreement
  coverage, dismissal rules, and top surprises for Nordic/German employers.
  Covers Finland, Germany, Estonia, Sweden, Netherlands, France in v1; routes
  other EU countries to outside counsel with a question list. Also covers
  posted workers (Directive 2018/957) and social security coordination
  (Reg 883/2004). Use when asked "we want to hire in [country]", "expanding to
  [country]", "posted worker rules", "what do we need to know to hire in [X]".
argument-hint: "[target country] — e.g. 'Netherlands' or 'Estonia' or 'posted worker Finland to Germany'"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:international-expansion

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If placeholders, stop: "Run `/eu-legal:cold-start-interview` first."
2. Load `~/.claude/plugins/config/eu-legal/employment.md` if it exists. Read: hiring countries already active (for context), headcount, outside counsel.
3. Identify the target country and expansion type from the argument.
4. Route to the relevant country profile below, or to the outside counsel checklist for unlisted countries.
5. Output: checklist of required steps before first hire.

---

## Purpose

Each EU country has different employment law, social security, tax, and registration requirements. What works in Finland does not transfer to the Netherlands, and what works in Germany does not transfer to France. This skill gives the key legal checkpoints for v1 coverage countries; for others, it produces a structured briefing checklist to take to local counsel.

---

## Step 1: Determine presence type

Ask if not clear from the argument:
> "How do you plan to engage this person or team? Select the model:"

1. **Local entity** — incorporate a subsidiary or branch in the target country
2. **Employer of Record (EOR)** — third-party company employs the worker; you direct the work
3. **Posted worker** — send an existing Finnish/German employee temporarily
4. **Genuine contractor** — engage an independent contractor (apply `/eu-legal:worker-classification` first)
5. **Remote employee** — hire someone living in target country as your employee (requires local entity or EOR in most cases)

Note: hiring an employee without local presence or EOR creates "permanent establishment" risk (corporate tax) and employer obligation risk (local payroll tax, social contributions) in most EU countries. Flag this prominently if the user selects "remote employee" without a local entity.

---

## Step 2: Posted workers (if applicable)

If presence type is "posted worker" — an employee of the Finnish/German company sent to work in another EU state:

**Directive 2018/957 (amending 96/71/EC) — host country minimum terms apply:**

The host country's mandatory rules on the following must be applied (regardless of what the employment contract says):
- Maximum work periods and minimum rest periods
- Minimum paid annual leave
- Remuneration (minimum wage of host country, including applicable collective agreement pay scales)
- Health and safety
- Equal treatment (non-discrimination)
- Accommodation and subsistence where provided by employer
- For postings > 12 months (extendable to 18 months by notification): nearly all employment terms of host country apply

**Social security (Reg 883/2004):**
- For postings up to 24 months: employee remains in home country social security; employer must obtain A1 certificate from home country authority (Kela in Finland, Deutsche Rentenversicherung in Germany)
- Apply for A1 before the posting begins — retroactive applications are possible but create gaps
- After 24 months: local social security of host country applies unless extension agreed between competent authorities

**Employer obligations for postings:**
- [ ] Notify host country labour authority before posting begins (most EU member states require online notification)
- [ ] Obtain A1 certificate
- [ ] Apply host country minimum wage and working time rules
- [ ] Keep employment documentation accessible in host country during posting

---

## Step 3: Country profiles

> **⚠️ All numeric thresholds, durations, benefit amounts, minimum wages, and headcount figures in this section are `[model knowledge — verify with local counsel before relying]`. These change annually with legislation, collective agreement updates, and court interpretation. `last_verified: 2026-06-01`**

### Finland (FI) — for employers expanding into Finland

**Legal entity requirement:**
- Branch (sivuliike) or subsidiary (tytäryhtiö) registered with Patentti- ja rekisterihallitus (PRH)
- No local entity needed if using EOR, but Finnish tax authority (Verohallinto) may deem permanent establishment if Finnish employee exercises authority to conclude contracts

**Employment contract:**
- Must be in writing (or written statement of terms within 1 month, TSL Ch. 2 §4)
- Finnish as language standard if employee is Finnish-speaking; bilingual acceptable
- Must include: parties, start date, workplace, role, salary, notice period
- Probation period: max 6 months (TSL Ch. 1 §4); 6 months if training obligation

**Works council / YT-laki:**
- Applies at ≥20 employees regularly in Finland (see works-council-check skill)
- Personnel representation: luottamusmies if employees are unionised; henkilöstöedustaja otherwise
- 🟡 Top surprise for German employers: Finnish cooperation procedure (YT-neuvottelut) looks similar to BetrVG §111 but has different timing and liability rules — the obligation does not freeze the decision, it requires genuine prior negotiation

**Collective agreement coverage:**
- Erga omnes system: if a general binding (yleissitova) TES exists for the industry, it applies to ALL employers in that industry — even non-members. Most major industries have erga omnes TES.
- Check: tyosuojelu.fi or SAK/EK/STTK databases for applicable TES
- 🔴 Top surprise: employer may be bound by a TES it didn't sign and may not know about

**Dismissal:**
- TSL grounds required (individual or financial/production)
- Re-employment obligation 9 months post-notice
- See termination-review skill for full framework

**Top 3 surprises for German employers in Finland:**
1. No Betriebsrat equivalent for daily decisions — YT-laki only applies to major changes. Day-to-day management decisions do not require prior consultation.
2. Employer is bound by the erga omnes TES for the industry even without signing it — check the applicable TES before setting any employment terms.
3. Finnish termination law requires a "substantial and weighty reason" (asiallinen ja painava syy) — similar standard to KSchG but with a different procedural cadence: warning before conduct dismissal is required but there is no §102 BetrVG equivalent for individual dismissals.

---

### Germany (DE) — for employers expanding into Germany

**Legal entity requirement:**
- GmbH (most common) or branch (Zweigniederlassung) registered at Handelsregister
- Registration at Finanzamt for payroll tax (Lohnsteuer) and social insurance registration (Deutsche Rentenversicherung, Krankenkasse, Berufsgenossenschaft)

**Employment contract:**
- No statutory written contract requirement, but NachwG (Nachweisgesetz) requires written statement of terms on day 1 since 2022
- Required contents: parties, start date, place of work, role, probation, salary, working hours, holiday, notice period, applicable Tarifvertrag
- Probation: max 6 months (§622(3) BGB) — notice during probation: 2 weeks

**Works council / BetrVG:**
- At ≥5 permanent employees: employees have the right to form a Betriebsrat — employer cannot prevent this
- Once formed: mandatory consultation for dismissals, working hours changes, surveillance, hiring (see works-council-check skill)
- 🔴 Top surprise for Finnish employers: a Betriebsrat can be formed at any time by the employees themselves. A Finnish company with 6 German employees has no Betriebsrat today and can have one tomorrow — and once formed, all future dismissals require §102 consultation.

**Collective agreement coverage:**
- NOT erga omnes by default: Tarifvertrag binds only employer association members (tarifrechtlich) or individually signed agreements
- But: allgemeinverbindlich (generally binding) declarations can extend some TarVs — check BMAS database
- 🟡 Advantage over Finland: German employer can often choose not to be bound by TarV if not joining employer association; but must then still compete for talent against TarV-paying employers

**Dismissal:**
- KSchG requires valid grounds once >10 employees and >6 months tenure
- §102 BetrVG consultation mandatory if Betriebsrat exists
- See termination-review skill for full framework

**Top 3 surprises for Finnish employers in Germany:**
1. The Betriebsrat has veto rights on hiring, transfers, and dismissals — not just a consultation right. Failure to consult makes the dismissal void, not just risky.
2. Collective redundancy notification to Bundesagentur für Arbeit (§17 KSchG) has strict formal requirements — missing the form or timing makes the dismissals void, regardless of substantive grounds.
3. The 6-week employer sick pay obligation (EFZG) `[model knowledge — verify current EFZG duration]` is higher than Finnish employers typically expect — build this into employment cost modelling.

---

### Estonia (EE)

**Employment contract:**
- TLS (Töölepinguseadus) — employment contracts act
- Written contract required; probation max 4 months
- Minimum wage: set annually by government (check current rate [model knowledge — verify])

**Works council:**
- Töötajate usaldusisik (employee trustee) system — employees can elect a representative if ≥10 employees
- No BetrVG equivalent — consultation rights narrower than DE/FI

**Dismissal:**
- TLS requires grounds for dismissal after probation
- Notice periods: employee-side 30 days; employer-side 15–90 days by service length `[model knowledge — verify current TLS text]`
- Severance: 1 month salary for financial/production dismissals `[model knowledge — verify current TLS text]`

**Collective agreement:**
- No erga omnes system; collective agreements bind only signatories
- Collective agreements less prevalent than FI/DE

**Top 3 surprises for FI/DE employers:**
1. Estonia has a flat income tax system — payroll administration is significantly simpler than Finland or Germany.
2. Employment protection is less strong than FI/DE but not absent — financial/production dismissal still requires a genuine reason.
3. E-Residency does NOT create an employment law nexus — an Estonian e-resident working in Germany is still subject to German employment law.

---

### Sweden (SE)

**Employment contract:**
- LAS (Lagen om anställningsskydd) — employment protection act; strong protection
- Main rule: indefinite employment. Fixed-term employment heavily restricted — only for: vikariat (substitute), säsongsarbete (seasonal), överenskommen visstid (agreed fixed-term, ≤2yr in 5yr period)
- Written contract required; probation max 6 months (provanställning)

**Works council / MBL:**
- MBL (Medbestämmandelagen) — applies to all employers with ≥10 employees `[model knowledge — verify current MBL threshold]`
- Primary negotiation obligation before major changes (§11 MBL)
- Collective agreements very widely used (~90% coverage erga omnes through industrywide) `[model knowledge — verify current coverage rate]`

**Dismissal:**
- Saklig grund (objective grounds) required — similar to but stricter than Finnish "substantial reason"
- Turordning (last-in-first-out) rule for redundancies: cannot cherry-pick who to make redundant unless fewer than 10 employees
- Re-employment priority: 9 months

**Top 3 surprises for FI/DE employers:**
1. The turordning (last-in-first-out) rule for redundancies is stronger than in Germany or Finland — employer cannot bypass it without collective agreement exception. Select carefully who you hire first.
2. Collective agreement coverage is ~90% and erga omnes for many sectors. The employer is practically always bound by a TES equivalent (kollektivavtal).
3. Discrimination claims are administered by DO (Diskrimineringsombudsmannen) and are actively enforced — budget for this in HR processes.

---

### Netherlands (NL)

**Employment contract:**
- Burgerlijk Wetboek Art. 7:610 — employment law in the Civil Code
- Written contract standard; probation max 1 month (up to 2 months for contracts >2 years)
- Transitievergoeding (transition payment) on termination: 1/3 month salary per year, regardless of reason — payable from day 1 `[model knowledge — verify current formula]`

**Works council / WOR:**
- WOR (Wet op de ondernemingsraden) — applies at ≥50 employees `[model knowledge — verify current WOR threshold]`
- Ondernemingsraad (OR) has consent and advisory rights
- At 10–49 employees: personeelsvertegenwoordiging (PVT) — lighter consultation body `[model knowledge — verify current PVT threshold]`
- 🔴 Consent right: OR must consent before: profit sharing, pension changes, working time changes, salary systems, disciplinary procedures, personnel monitoring

**Dismissal:**
- Requires UWV (social security authority) or Kantonrechter (court) approval before dismissal — employer cannot simply give notice
- Two routes: UWV procedure for business reasons (typically 4 weeks+); Kantonrechter for personal grounds (1-3 months)
- Transitievergoeding always payable; additional vergoeding (compensation) if dismissal unfair

**Top 3 surprises for FI/DE employers:**
1. Dutch dismissal law requires prior government (UWV) or court approval — you cannot dismiss with notice alone. Plan for 4–12 weeks procedure time.
2. The transitievergoeding (transition payment of 1/3 month per year) is payable on every termination including redundancy — budget for it from day 1.
3. Dutch employment law distinguishes carefully between ZZP (zelfstandige zonder personeel — independent contractor) and employee. The same Platform Work Directive indicators apply; Dutch authorities actively audit this.

---

### France (FR)

**Employment contract:**
- Code du travail — comprehensive labour code; highly protective of employees
- CDI (contrat à durée indéterminée) is the norm; CDD (fixed-term) strictly limited
- Written contract required; probation: 2 months (workers), 3 months (supervisors), 4 months (cadres)

**Works council / CSE:**
- CSE (Comité Social et Économique) mandatory from ≥11 employees `[model knowledge — verify current Code du travail threshold]`
- At ≥11 employees: basic consultation rights
- At ≥50 employees: full CSE with broader powers; BDES (economic database) obligation `[model knowledge — verify current threshold]`
- 🔴 Strong co-determination: CSE must be consulted before major changes; consultation failure can result in offence d'entrave (criminal obstruction charge against management)

**Dismissal:**
- Cause réelle et sérieuse (real and serious ground) required
- Mandatory prior meeting (entretien préalable) with employee before any dismissal
- Notice period by collective agreement or statutory minimums
- Prud'hommes (labour tribunal): very active; statute of limitations 1 year (personal) / 12 months (discrimination)

**Top 3 surprises for FI/DE employers:**
1. The criminal offence d'entrave (obstruction) for failing to consult the CSE is not theoretical — managers can be personally fined or imprisoned. Consultation is not optional.
2. French collective agreements (conventions collectives) are complex, layered (national + sectoral + company level), and often more restrictive than the Code du travail. The applicable convention collective depends on the company's IDCC code (classification code).
3. Licenciement économique (economic dismissal) for companies ≥50 requires a Plan de Sauvegarde de l'Emploi (PSE) — a negotiated document covering redeployment, retraining, and outplacement. This is a multi-month process and requires validation by the DREETS (labour authority).

---

## Other EU countries

For EU member states not covered above (Austria, Belgium, Poland, Czech Republic, Spain, Italy, Portugal, etc.):

> "This skill covers Finland, Germany, Estonia, Sweden, Netherlands, and France in v1. For [target country], I can produce a structured question list to take to local employment counsel."

Generate the following checklist for outside counsel briefing:

**Questions for [country] employment counsel:**
1. What written contract requirements apply (statutory form, language, required clauses)?
2. What is the maximum probation period?
3. Is there a works council or employee representation body? At what headcount threshold? What are its consent vs. advisory rights?
4. What collective agreement system applies — erga omnes or opt-in only? Is there an applicable sectoral agreement?
5. What are the valid grounds for dismissal? Is prior authority approval required?
6. What are the notice periods by service length?
7. Is statutory severance payable on dismissal? If so, what formula?
8. What is the employer's sick pay obligation (days and percentage)?
9. What are the parental and maternity leave entitlements and the associated job protection period?
10. What are the top 3 surprises for employers coming from Finland or Germany?

---

## Guardrail

> **RESEARCH NOTES — NOT LEGAL ADVICE.** Employment law requirements in each EU member state vary significantly from the general principles described here. This checklist identifies key legal checkpoints — it does not substitute for advice from a qualified employment lawyer in the target country. Before the first hire: engage local counsel, confirm current minimum wage and benefit rates, and verify that the applicable collective agreement has been identified. [model knowledge — verify current thresholds and benefit amounts for each country] Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.