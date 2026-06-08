---
name: employment-cold-start
description: >
  Set up the employment practice profile — learns your hiring countries,
  headcount, collective agreements, works council status, and termination
  policy, then writes the employment config. Run on first use of any
  employment skill, when employment.md is missing or has placeholders, or
  when your employment situation changes. Use when the user says "set up
  employment", "configure employment", "onboard employment", or runs any
  employment skill with a missing config.
argument-hint: "[--redo] to force a full re-run"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:employment-cold-start

1. Check `~/.claude/plugins/config/eu-legal/CLAUDE.md` — if placeholders, stop: "Run `/eu-legal:cold-start-interview` first. Employment setup requires the base profile."
2. Check `~/.claude/plugins/config/eu-legal/employment.md` — if populated and no `--redo`, ask: "Employment config already exists. Re-run and overwrite it?" Stop if user says no.
3. Run the interview workflow below.
4. Write `~/.claude/plugins/config/eu-legal/employment.md`.
5. Show summary. Offer next steps.

---

## Interview workflow

Ask questions one topic per message. Never dump all questions at once.

### 1. Hiring countries

Ask:
> "Which countries do you hire employees in? Select all that apply."

Present as a numbered checklist:
1. Finland (FI)
2. Germany (DE)
3. Estonia (EE)
4. Sweden (SE)
5. Netherlands (NL)
6. Other EU member state(s) — specify which

Accept multiple selections. Save as a list of country codes. At least one country must be selected.

If "Other EU" selected: ask which countries (free text). Record them under `other_eu_countries`.

### 2. Headcount

Ask:
> "Approximately how many employees do you have in total? And can you break it down by country if different?"

Collect:
- `total_headcount`: integer
- `headcount_by_country`: dict, e.g. `{FI: 25, DE: 8}`

**Threshold checks (run silently, record in config):**
- Finland ≥ 20 employees → YT-laki cooperation obligation applies; set `fi_yt_laki_applies: true`
- Germany ≥ 5 employees → Betriebsrat can be formed; set `de_betriebsrat_possible: true`
- Germany > 10 employees + ≥ 6 months tenure → KSchG applies; set `de_kschg_applies: true`
- Total ≥ 50 → whistleblower reporting channel mandatory; set `whistleblower_channel_required: true`

### 3. Collective agreements

Ask (separately per country if multiple):

**Finland:**
> "Does a collective agreement (työehtosopimus, TES) cover your employees in Finland? If yes, which one? (e.g., technology industry TES — Teknologiateollisuus, financial services, general)"

Record: `fi_collective_agreement: [name or none]`

**Germany:**
> "Is your German workforce covered by a collective agreement (Tarifvertrag)? If yes, which one? (e.g., IG Metall, ver.di, employer association membership)"

Record: `de_tarifvertrag: [name or none]`

### 4. Standard employment contract terms

Ask:
> "What are your standard employment contract terms? I'll ask about three things."

Ask separately:
1. "Do you use the statutory minimum notice periods, or longer contractual notice periods in Finland/Germany?"
   - Accept: `statutory` or a description like "3 months both sides in Finland"
   - Record: `fi_notice_period_policy` and `de_notice_period_policy`

2. "Do you include non-compete clauses in employment contracts? If yes, for how long, and in which countries?"
   - Record: `noncompete_used: true/false`, `noncompete_duration_months: N`, `noncompete_countries: [list]`
   - Note internally: Finnish law caps at 12 months; compensation required if >6 months (TSL Ch. 3 §5)

3. "Do you include IP assignment / invention assignment clauses?"
   - Record: `ip_assignment: true/false`

### 5. Finland — personnel representation

If FI in hiring countries:
> "In Finland, has the YT-laki cooperation obligation threshold (≥20 employees) been reached? And do you have existing personnel representation — a luottamusmies (shop steward) or henkilöstöedustaja (personnel rep)?"

Record:
- `fi_yt_laki_active: true/false` (may differ from threshold check if mixed workforce)
- `fi_personnel_rep_type: luottamusmies | henkilostoedustaja | none`
- `fi_union_affiliated: true/false`

### 6. Germany — works council

If DE in hiring countries:
> "In Germany, does a Betriebsrat (works council) exist? If yes, how many members?"

Record:
- `de_betriebsrat_exists: true/false`
- `de_betriebsrat_members: N` (0 if none)

### 7. Termination policy

Ask:
> "Three quick questions about your termination practice."

Ask separately:
1. "When does legal review a termination? (All terminations / performance/conduct only / RIFs only / exec only)"
   - Record: `termination_review_trigger`

2. "Do you offer standard severance above statutory entitlements? If yes, what formula?"
   - Record: `standard_severance: [none / formula e.g. '1 month per year']`

3. "What's the outside counsel threshold for terminations — at what point do you escalate to external employment counsel?"
   - Record: `outside_counsel_threshold: [description]`

---

## Write the config

Write to `~/.claude/plugins/config/eu-legal/employment.md` (create parent dirs if needed).

Template to fill and write:

```markdown
# Employment Practice Profile
*Written by /eu-legal:employment-cold-start on [DATE]. Run with --redo to update.*

---

## Hiring countries

**Countries:** [comma-separated list]
**Total headcount:** [N]
**Headcount by country:** [FI: N, DE: N, ...]

---

## Threshold checks

| Check | Applies | Notes |
|---|---|---|
| YT-laki (FI ≥20 employees) | [true/false] | Cooperation procedure required before major changes and collective redundancies |
| Betriebsrat possible (DE ≥5 employees) | [true/false] | Works council can be formed; consultation rights apply once formed |
| KSchG applies (DE >10 employees) | [true/false] | Dismissal protection applies to employees with >6 months tenure |
| Whistleblower channel required (total ≥50) | [true/false] | Directive 2019/1937 and Finnish implementing act 1171/2022 |

---

## Collective agreements

**Finland TES:** [name or none]
**Germany Tarifvertrag:** [name or none]

---

## Standard contract terms

**Finland notice periods:** [statutory / contractual description]
**Germany notice periods:** [statutory / contractual description]
**Non-compete clauses used:** [true/false]
**Non-compete max duration:** [N months or N/A]
**Non-compete countries:** [list or N/A]
**IP assignment clauses:** [true/false]

---

## Finland — personnel representation

**YT-laki cooperation active:** [true/false]
**Personnel rep type:** [luottamusmies / henkilostoedustaja / none]
**Union affiliated:** [true/false]

---

## Germany — works council

**Betriebsrat exists:** [true/false]
**Betriebsrat members:** [N]

---

## Termination policy

**Legal reviews terminations:** [all / performance-conduct / RIFs / exec]
**Standard severance:** [none / formula]
**Outside counsel threshold:** [description]

---

*Re-run: `/eu-legal:employment-cold-start --redo`*
```

---

## Offer next steps

After writing the config, say:

> "Employment profile saved. Try:
> - `/eu-legal:works-council-check` — does this decision require works council or YT-laki consultation?
> - `/eu-legal:termination-review` — review a proposed termination for legal risk
> - `/eu-legal:leave-review` — calculate leave entitlements for an employee
> - `/eu-legal:worker-classification` — classify a contractor or gig worker arrangement"

---

## Guardrail

> **RESEARCH NOTES — NOT LEGAL ADVICE.** The employment profile captures your current situation as described. Employment law has significant liability exposure — statutory obligations, collective agreement requirements, and threshold-triggered duties change as headcount and circumstances change. Review this profile with qualified employment counsel and update it whenever your employment situation materially changes. The profile drives the analysis in all other employment skills; attorney review is required before relying on any output for employment decisions. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.