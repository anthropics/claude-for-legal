---
name: compliance-audit
description: >
  Audit a district policy, procedure, or handbook section for compliance gaps
  against IDEA, Section 504, FERPA, Title IX, Title VI, EEOA, and the state
  education code. Output: gap report with citations, severity, recommended
  remediation. Routes to the specific skills when a single area is in scope.
  Use when the user says "audit this policy", "compliance review", "is this
  handbook compliant", "is this procedure adequate", or attaches a policy.
argument-hint: "[policy / handbook section / procedure file path, or paste the text]"
---

# /compliance-audit

1. Load `~/.claude/plugins/config/claude-for-legal/education-legal/CLAUDE.md` → state(s), district context, all framework sections (IDEA, §504, FERPA, Title IX, discipline).
2. Identify which statutes the input policy implicates.
3. Run the gap analysis against each applicable framework. Cite. Tag severity.
4. Route to the specific skill when one area is the bulk of the issue.

---

## Matter context

Compliance audits are usually practice-level (district counsel auditing district policies). If matter workspaces are enabled and a specific matter is active, scope the audit to that matter.

---

## Purpose

A district has dozens of policies and procedures. Many were written years ago. Statutory frameworks have moved (ADAAA broad construction, 2024 §504 update, multiple Title IX rulemakings, state-code amendments). The skill identifies what's drifted and what's compliant — by statute, with citations, with severity.

This is the **broadest** skill in the plugin. It routes to the more specific skills when one area is the bulk of the issue (e.g., a Title IX policy review routes to `title-ix-grievance`; an IEP-procedure review routes to `iep-review` patterns; a records-policy review routes to `ferpa-records-response` patterns).

## Load context

Per CLAUDE.md. Read every framework section.

## Output header

Per CLAUDE.md `## Outputs`.

## Workflow

### Step 1: Identify which frameworks the policy implicates

Read the input. Tag each section with the framework(s) it touches:

| Section / Provision | Framework(s) implicated |
|---|---|
| [section] | [IDEA / §504 / FERPA / Title IX / Title VI / EEOA / state code] |

If the policy is single-framework (e.g., a Title IX grievance procedure), route to the specific skill:

> "This is primarily a Title IX procedure. The `title-ix-grievance` skill carries the version-tagged procedural framework in detail — running that against this policy will give you a more granular review than the audit skill. Want me to do that instead? Or proceed with the broader audit?"

For multi-framework policies (district handbook chapters, code of conduct, discipline matrix), proceed with the audit.

### Step 2: Per-framework gap analysis

For each framework that applies, run the relevant checklist.

#### IDEA

- Child-find procedures (34 CFR §300.111).
- Evaluation timeline (60 days federal; state overlay).
- IEP-team composition.
- LRE continuum.
- Procedural safeguards (notice, parental consent, due process).
- Discipline framework (10-day rule, manifestation, services-during-removal).
- Transition planning (age in state code).

#### Section 504

- Eligibility framework (§104.35: impairment, substantial limitation, major life activity) under ADAAA broad construction.
- Evaluation requirements (§104.35(a)-(b)).
- Procedural safeguards (§104.36: notice, records, hearing, review).
- 2024 §504 regulatory update items where applicable.

#### FERPA

- Definition of education records vs. excluded categories.
- Annual notification of rights (§99.7).
- Directory-information designation and opt-out.
- Access procedures (§99.10) and timeline.
- §99.31 exceptions properly limited.
- Access log under §99.32.

#### Title IX

- **Operative regulatory version named?** If the policy doesn't identify the version it's implementing, that's a finding.
- Notice of nondiscrimination.
- Coordinator designation.
- Grievance procedures matching the version's required elements.
- Training requirements.

#### Title VI / EEOA

- Race, color, national-origin nondiscrimination.
- English-learner services (EEOA, *Castañeda v. Pickard* framework).
- Language-access requirements for parents with limited English proficiency.

#### State education code

State-code overlay for each of the above frameworks. The practice profile's `## Jurisdictional footprint` is the entry point.

> **Research each framework's currently-operative rules before flagging gaps.** Do not rely on memory for current Title IX version, 2024 §504 amendments, recent OSEP guidance, recent OCR letters, or state-code amendments. Cite primary sources. Verify currency.

### Step 3: Severity rating

Per CLAUDE.md `## Cross-skill severity floor`. Canonical scale 🔴 / 🟠 / 🟡 / 🟢.

- **🔴 Blocking** — provision is non-compliant in a way that creates immediate exposure (e.g., FERPA release exception described in a way that authorizes more than the statute permits; due-process timeline shorter than IDEA requires; Title IX procedure missing required elements of the operative version).
- **🟠 High** — provision is unclear in a way that will produce wrong outcomes in practice (e.g., directory-information opt-out process buried; eligibility framework written pre-ADAAA; manifestation framework collapses the two questions).
- **🟡 Medium** — provision is technically compliant but uses outdated framing or could be clearer.
- **🟢 Low** — minor language or style.

### Step 4: Recommended remediation

For each finding, provide the specific edit recommended. Not "review this section" — a draft of the language that fixes it (or, for complex fixes, a specific question for the district to answer before the redraft).

### Step 5: Cross-statute interactions

Some findings have cross-statute consequences:
- A FERPA gap that affects a Title IX investigation procedure.
- A §504 procedure that overlaps an IDEA procedure (and the district's policy should clarify which applies).
- A discipline matrix that needs to coordinate with IDEA manifestation rules and §504 procedural safeguards.

Surface these explicitly.

### Step 6: Source attribution

Per CLAUDE.md.

## Output

```markdown
[WORK-PRODUCT HEADER]

## Compliance Audit: [policy name] — [District] — [State]

**Frameworks reviewed:** [list]
**Operative versions assumed:** [Title IX vX; §504 post-2024-update; state code current as of [date] — each `[verify]`]

### Findings — by framework

#### IDEA
| # | Section | Finding | Severity | Citation | Recommendation |
|---|---|---|---|---|---|
| | | | | | |

#### Section 504
[Same table.]

#### FERPA
[Same table.]

#### Title IX
[Same table — version-tagged.]

#### Title VI / EEOA
[Same table.]

#### State education code
[Same table.]

### Cross-statute interactions
[Findings that span frameworks; explained.]

### Summary
- 🔴 Blocking: [count]
- 🟠 High: [count]
- 🟡 Medium: [count]
- 🟢 Low: [count]

### Suggested order of remediation
[Prioritized list — usually 🔴 first, but sometimes a 🟠 with broad reach is more urgent.]
```

📊 **Dashboard offer** per CLAUDE.md when findings exceed ~10 rows.

**Person-first language. PII discipline applied.**

## Consequential-action gate

If the user asks the skill to make the policy edits and re-adopt the policy:

> Adopting a revised district policy has board-approval and notice-to-stakeholders implications. I can draft the proposed language for each finding, but adoption is the district's process. Want me to draft the revisions for the board packet? Or stop at the findings and recommendations?

For non-lawyer audience finalizing a redraft:

> Before adopting this revised policy: have you had outside counsel review for [list of high-stakes areas — Title IX procedural compliance, FERPA disclosure exceptions, IDEA discipline framework, §504 eligibility framework]? Adopting a non-compliant policy creates standing exposure. If yes, proceed. If no, here's the brief: [findings summary, what was changed, what the operative versions / state-overlay assumptions are, what could still go wrong].

---

## Close with the next-steps decision tree

Per CLAUDE.md. Customize:
- **Draft the revised policy / specific section** — produce the redline.
- **Route to a specific skill** — for the deep dive on Title IX, IEP procedure, FERPA response, etc.
- **Escalate to outside counsel** — draft the brief.
- **Get more facts** — what additional district documents are needed.

## What this skill does NOT do

- **Adopt the policy.** District process.
- **Decide the operative Title IX version** for the audit. Practice profile + outside counsel.
- **State framework rules from memory** — researched and cited at audit time.
- **Skip the cross-statute interactions.** Multi-framework policies need the interactions flagged.
- **Substitute for the per-framework skills** when one area is the focus.
