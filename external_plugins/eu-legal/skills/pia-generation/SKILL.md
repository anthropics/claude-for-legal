---
name: pia-generation
description: >
  Generate a Privacy Impact Assessment (PIA) or GDPR Data Protection Impact
  Assessment (DPIA) for a new processing activity, feature, or system. Checks
  whether a DPIA is mandatory under GDPR Art. 35 before starting. Use when
  saying "write a PIA", "DPIA for this feature", "privacy review this", or
  describing a new data processing activity.
argument-hint: "[describe the processing activity or system]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:pia-generation

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If placeholders, stop: "Run `/eu-legal:cold-start-interview` first."
2. Load `~/.claude/plugins/config/eu-legal/privacy.md` for DPIA triggers and house style. If missing, use GDPR Art. 35 mandatory criteria only.
3. Run Step 1 (mandatory DPIA check) before anything else.
4. Draft the PIA/DPIA. Output is draft for DPO/attorney review.

---

## Step 1: Mandatory DPIA trigger check (GDPR Art. 35)

**Live verification:** Call `mcp__velvoite__get_eu_regulation_article("gdpr", "35")` and fetch the section_url to verify the current Art. 35 mandatory DPIA triggers from EUR-Lex before applying the 9-criterion checklist below.

A DPIA is mandatory if the processing is "likely to result in a high risk." Check:

**WP29 / EDPB 9 criteria (2+ criteria = DPIA required):**
1. Evaluation or scoring (profiling)
2. Automated decision-making with legal or similarly significant effects
3. Systematic monitoring (CCTV, employee monitoring, network monitoring)
4. Sensitive data or data of a highly personal nature (Art. 9/10, financial data, location)
5. Large-scale processing
6. Matching or combining datasets from different sources
7. Data concerning vulnerable data subjects (children, employees, patients)
8. Innovative use or applying new technological solutions
9. Processing that "prevents data subjects from exercising a right or using a service or a contract" (e.g. screening, profiling for access)

**Finnish supervisory authority list (Tietosuojavaltuutettu):** check if the specific processing type appears on the Finnish DPA's published list of processing requiring mandatory DPIA.

**Custom triggers from privacy.md:** check any additional internal triggers.

**Verdict:**
- 2+ criteria → **DPIA mandatory** — proceed with full DPIA
- 1 criterion → **PIA recommended** — proceed with PIA, note it may escalate to DPIA
- 0 criteria → **PIA optional** — note this and ask if user wants to proceed anyway

## Step 2: PIA/DPIA interview

Gather information through conversation. One topic at a time.

1. **Processing description**: what data, what purposes, what operations (collect, store, use, share, delete)?
2. **Legal basis** (Art. 6): contract / legal obligation / legitimate interests (LIA required) / consent / vital interests / public task. If special categories (Art. 9): which Art. 9(2) basis?
3. **Data subjects**: who are they? Are any vulnerable (employees, children, customers in financial difficulty)?
4. **Data flows**: where does data come from? Where does it go? Any third-country transfers?
5. **Retention**: how long is data kept? What triggers deletion?
6. **Existing controls**: what technical and organisational measures are already in place?
7. **Risks identified**: what could go wrong? Impact on data subjects?

## Step 3: Draft PIA/DPIA

Structure (based on EDPB Guidelines 04/2022 on DPIA (based on WP29 WP248 rev.01)):

**1. Description of processing** — systematic description per Art. 35(7)(a): purposes, nature, scope, context, categories of data, recipients, retention periods.

**2. Necessity and proportionality** — assessment of necessity and proportionality of the processing in relation to purposes per Art. 35(7)(b). Legal basis analysis. Data minimisation check.

**3. Risks to data subjects** — identification of risks per Art. 35(7)(c): unauthorized access, unexpected change of purpose, data unavailability. Assess likelihood and severity.

**4. Existing controls** — technical (encryption, access controls, pseudonymisation) and organisational (training, policies, contracts).

**5. Residual risks and measures** — gaps between identified risks and existing controls. Proposed additional measures. Residual risk after measures.

**6. Conclusion** — overall risk level (low / medium / high). If high residual risk: prior consultation with supervisory authority required per Art. 36. DPO consultation (if DPO exists): required per Art. 35(2).

**7. Sign-off fields** — DPO name/date, controller representative name/date, review date.

---

## Guardrail

This draft requires review by the DPO (if appointed) and legal counsel before finalisation. If the residual risk is assessed as high, prior consultation with the supervisory authority is mandatory under GDPR Art. 36 — do not proceed with the processing without completing that consultation. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.