---
name: termination-review
description: >
  Review a proposed termination for legal risk — jurisdiction-specific
  grounds analysis, notice period calculation, protected status flags, and
  required procedural steps. Covers Finland (TSL, YT-laki) and Germany
  (KSchG, BetrVG). Use when asked "can we fire this person", "reviewing a
  termination", "term review", "is this a valid dismissal", or when
  describing a termination scenario.
argument-hint: "[describe the termination — role, reason, tenure, jurisdiction]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:termination-review

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If placeholders, stop: "Run `/eu-legal:cold-start-interview` first."
2. Load `~/.claude/plugins/config/eu-legal/employment.md` if it exists. Read: termination review trigger, standard severance, outside counsel threshold.
3. Run the workflow below.
4. Output: risk assessment, required steps checklist, notice period, protected status flags.

---

## Purpose

Most terminations are legally sound. A few carry serious risk — wrongful dismissal claims, compensation orders, reinstatement orders, works council consultation failures that void the dismissal entirely. This skill identifies the risk; a qualified employment lawyer must review before the dismissal is communicated.

---

## Step 1: Gather facts

If not already provided in the argument, ask:

1. "Which country is this employment relationship governed by?" (Finland / Germany / other — if other, note that coverage is limited)
2. "What is the reason for the termination?" (misconduct / performance / redundancy / restructuring / other)
3. "How long has the employee been employed?" (years and months)
4. "What is the employee's role and seniority?"
5. "Any of these apply? (check all that apply): pregnant or on maternity leave / on parental leave / personnel representative or shop steward / recently reported a workplace concern or filed a complaint / on sick leave currently / member of works council (Germany)"

---

## Step 2: Jurisdiction check

Route to the applicable framework below. If both FI and DE apply (e.g., employee works across borders), apply both and note the more protective.

---

## Finland framework (Työsopimuslaki, TSL 55/2001)

### Grounds check

**Individual grounds (henkilöön liittyvä peruste, TSL Ch. 7 §2):**

Applies where the reason is the employee's conduct, performance, or personal circumstances.

Required elements — all must be satisfied:
- [ ] Substantial reason (asiallinen ja painava syy) — the conduct or incapacity is serious enough to justify dismissal
- [ ] Warning given (varoitus) — for conduct dismissals: has the employee received a written warning about this specific behaviour and been given the opportunity to correct it? Exception: conduct so serious that warning is not required (e.g., criminal conduct, gross breach of trust)
- [ ] Proportionality — is dismissal proportionate, or would a less severe measure (warning, demotion, transfer) suffice?
- [ ] No obligation to offer alternative work — has the employer explored reassignment?

Note whether each element is met, partially met, or not met. Any unmet element is a 🔴 risk.

**Financial/production grounds (taloudellinen tai tuotannollinen irtisanomisperuste, TSL Ch. 7 §3):**

Applies where the reason is a genuine reduction in the need for the employee's work.

Required elements:
- [ ] Genuine reduction in work — is the business reason real? (Not personal performance dressed up as redundancy)
- [ ] No suitable alternative work — employer must check: is there any other role this employee could fill, including after reasonable retraining?
- [ ] Re-employment obligation — TSL Ch. 6 §6: if employer rehires within 9 months of notice, former employee has re-employment priority
- [ ] YT-laki check — if ≥10 redundancies in 90 days: cooperation negotiations (YT-neuvottelut) required BEFORE notice. See works-council-check skill.

### Notice period calculation (TSL Ch. 6 §3)

Call `mcp__velvoite__get_finnish_statute("TSL", "6:3")` and `mcp__velvoite__get_finnish_statute("TSL", "6:4")` to retrieve current notice period rules. Present the notice period table from the live statute text — do NOT use hardcoded values.

**Employer-side notice periods by service length:**

| Service length | Employer notice period |
|---|---|
| < 1 year | 14 days |
| 1–4 years | 1 month |
| 4–8 years | 2 months |
| 8–12 years | 3 months |
| 12–15 years | 4 months |
| > 15 years | 6 months |

**Employee-side notice periods:**

| Service length | Employee notice period |
|---|---|
| < 5 years | 14 days |
| ≥ 5 years | 1 month |

Calculate and state: "Based on [N years] service, the employer's notice period is [X]. Last day of employment if notice given today ([DATE]): [DATE + notice period]."

Note: collective agreement (TES) may prescribe longer notice periods — check `fi_collective_agreement` from employment.md. If a TES applies and its terms are not known, flag: "Verify notice period against applicable TES `[review]`."

### Protected employees — Finland

Flag if any apply. Each requires heightened justification; some create near-absolute protection:

| Status | Protection |
|---|---|
| Pregnant (raskaus) | TSL Ch. 7 §9: dismissal during pregnancy presumed connected to pregnancy; extremely high risk |
| Maternity / parental leave (äitiys-, isyys-, vanhempainvapaa) | Cannot dismiss due to family leave; burden on employer to prove unconnected |
| Luottamusmies (shop steward) | TSL Ch. 7 §10: can only dismiss with consent of the majority of the workers they represent, or if work has entirely ceased |
| Henkilöstöedustaja (personnel rep) | Same heightened protection as luottamusmies |
| Current sick leave | Not absolute protection but timing creates strong inference of retaliation — document carefully |

---

## Germany framework (KSchG + BetrVG)

### KSchG applicability check

KSchG (Kündigungsschutzgesetz) applies if:
- Establishment has **more than 10 employees** (employees counted in full/part-time equivalents — part-time ≤20h/week counts as 0.5), AND
- Employee has been employed for **more than 6 months** (Wartezeit)

If KSchG does NOT apply: dismissal is freer but still subject to AGG (anti-discrimination) and good faith. Note this explicitly.

If `de_kschg_applies: true` from profile, proceed with full KSchG analysis.

### Grounds check (KSchG §1)

Three valid grounds — must fit at least one:

**Person-related (personenbedingt):**
- Long-term incapacity or frequent short-term illness where no improvement is expected AND continued employment unreasonable — negative prognosis required
- [ ] Is there a documented negative prognosis (arztliches Attest)?
- [ ] Has employer explored all reasonable adjustments (§164 SGB IX for disabilities)?

**Conduct-related (verhaltensbedingt):**
- Deliberate breach of contractual obligations
- [ ] Has a prior warning (Abmahnung) been given for the same type of conduct? (Required except for the most serious breaches)
- [ ] Is the conduct continuing or was it a one-off?

**Operational (betriebsbedingt):**
- Genuine operational decision removing or reducing this type of work
- [ ] Is the business reason genuine and not a pretext?
- [ ] Social selection (Sozialauswahl, KSchG §1(3)): among comparable employees who could have been dismissed, were the correct criteria applied? (Age, tenure, dependants, disabilities — employee with weakest social score dismissed first)
- [ ] Has employer checked for alternative positions?

### Works council consultation (BetrVG §102) — MANDATORY

**Before every dismissal** (individual or collective), the Betriebsrat must be consulted. This is not optional.

If `de_betriebsrat_exists: true` from employment.md:
- [ ] Has written notification been given to the Betriebsrat with: name of employee, type of dismissal (ordinary/extraordinary), timing, reason?
- [ ] Has the consultation period elapsed? (Ordinary dismissal: 1 week; Extraordinary §626 dismissal: 3 days)
- [ ] If Betriebsrat objects: employer may still dismiss but must notify employee of the objection. Employee may seek interim injunction (Weiterbeschäftigung).

**Failure to consult = dismissal is void (nichtig).** This is the single most common reason German dismissals fail. Flag as 🔴 blocking if consultation has not been completed.

If no Betriebsrat exists: note this, but flag that if one is later formed, prior dismissals without consultation are not retroactively void.

### Notice periods (KSchG / §622 BGB)

**Statutory employer notice periods by service length:**

| Service length | Employer notice period |
|---|---|
| < 2 years | 4 weeks (to 15th or end of month) |
| 2–5 years | 1 month (to end of month) |
| 5–8 years | 2 months (to end of month) |
| 8–10 years | 3 months (to end of month) |
| 10–12 years | 4 months (to end of month) |
| 12–15 years | 5 months (to end of month) |
| 15–20 years | 6 months (to end of month) |
| ≥ 20 years | 7 months (to end of month) |

Calculate and state: "Based on [N years] service, the employer's notice period is [X months], running to end of month. Last day of employment if notice given today ([DATE]): [END OF MONTH + N MONTHS]."

### Protected employees — Germany

| Status | Protection |
|---|---|
| Pregnant (§17 MuSchG) | Dismissal void during pregnancy and 4 months post-birth; requires authority approval (Gewerbeaufsicht) |
| Parental leave (§18 BEEG) | Dismissal protection throughout parental leave period (up to 3 years); authority approval required |
| Betriebsrat member | Special protection: only collective dismissal with Betriebsrat consent, or extraordinary dismissal for serious cause |
| Severely disabled (GdB ≥50) | Requires Integrationsamt approval before dismissal |
| Maternity leave (MuSchG) | Same as pregnancy — void without authority approval |

---

## Step 3: Output

### Risk assessment

State overall risk:

- 🔴 **High** — grounds are weak or absent, protected status present, required consultation not done, or warning not given. Do not proceed without legal review.
- 🟠 **Medium-High** — one or more required elements uncertain; needs legal input before proceeding.
- 🟡 **Medium** — grounds appear sound but procedural steps remain; proceed carefully through checklist.
- 🟢 **Low** — grounds clear, procedure followed, no protected status. Still recommend attorney sign-off.

### Required steps checklist

Output as a checklist of what must happen BEFORE notice is given:

- [ ] [Step 1: e.g., "Obtain written warning file — verify warning was given for [specific conduct] and acknowledged"]
- [ ] [Step 2: e.g., "BetrVG §102 consultation — notify Betriebsrat in writing with grounds, wait 1 week"]
- [ ] [Step 3: e.g., "Verify no alternative positions available — document search"]
- [ ] [Step 4: e.g., "Check TES for any enhanced notice period or procedural requirements"]
- [ ] [Step 5: "Attorney sign-off before notice communicated"]

### Outside counsel escalation

If `outside_counsel_threshold` is set in employment.md: compare the facts against the threshold. If met, say: "Your employment profile sets outside counsel escalation when [threshold]. This termination meets that threshold — escalate before proceeding."

---

## Guardrail

> **CONFIDENTIAL — INTERNAL LEGAL ANALYSIS — NOT A SUBSTITUTE FOR EXTERNAL COUNSEL ADVICE.** Wrongful dismissal claims carry significant financial exposure: compensation up to [24 months salary in Finland (TSL Ch. 12 §2)] or [12 months + Sozialplan entitlements in Germany], plus reinstatement orders. This analysis identifies risk based on the facts as described — it is a working document for attorney review, not a legal opinion. An employment lawyer must review before the dismissal is communicated. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.