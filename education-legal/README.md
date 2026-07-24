# K-12 Education Law Plugin

K-12 education law workflows: IEP and 504 plan review, manifestation determinations under IDEA's discipline framework, FERPA records responses within statutory windows, Title IX grievance procedure, due process complaints, and district compliance audits. Built around a state-aware practice profile learned at cold-start — the plugin knows your state, your audience (district counsel / family advocate / clinic supervisor / clinic student), and the variants that matter.

**Every output is a draft for attorney or team review — cited, flagged, and gated — not a legal conclusion or a team determination.** The plugin does the work: reads the IEP, applies your house framing, finds the issues, drafts the memo. A lawyer reviews. An IEP team decides. A manifestation team determines. A Title IX decision-maker finds. Eligibility, FAPE, manifestation, and Title IX findings stay with the humans who are statutorily authorized to make them. Citations are tagged by source so you know which ones came from a primary-source tool and which need checking. Privilege markers are applied conservatively so nothing waives by accident. PII is redacted by default in templates and samples.

**Higher education is out of scope for v1.** FERPA, Title IX, ADA, and §504 all behave differently postsecondary — those questions belong in a higher-ed practitioner's hands.

## Who this is for

| Role | Primary workflows |
|---|---|
| **District counsel / LEA staff** | Compliance audit, IEP/504 review, manifestation determinations, FERPA responses, Title IX grievance procedure |
| **Parent / family advocate** | IEP/504 review with rights-asserting framing, due process complaints, OCR-complaint preparation |
| **Education-law clinic supervisor** | Supervises clinic-student work; sets conservative gates |
| **Clinic student** | Drafts under supervision; conservative defaults; every conclusion routed for supervisor sign-off |

## First run: cold-start

Asks which state(s) you're in, what audience you serve, and reads seed documents (a sample IEP, a 504 plan, your district handbook or your advocacy practice's playbook, the adopted Title IX grievance procedure, a few OCR letters or due-process decisions). Builds a state-aware practice profile.

```
/education-legal:cold-start-interview
```

Your configuration is stored at `~/.claude/plugins/config/claude-for-legal/education-legal/CLAUDE.md` and survives plugin updates.

## Prerequisites

- **Persistent data path.** The matter folders, verification log, and any portfolio trackers are written to `~/.claude/plugins/config/claude-for-legal/education-legal/`, a version-independent path that survives plugin updates. These files contain confidential student records. Make sure that directory is backed up and access-controlled.
- **Legal research access.** Skills in this plugin intentionally do not store substantive legal rules (state evaluation timelines, current Title IX regulatory version, state discipline-removal rules, state-specific due-process filing requirements, state special-education code provisions). Every state-specific rule is researched and cited at the time of review. Make sure the session has access to the research tools you rely on (web search, ecfr.gov, state-code sources, OSEP and OCR guidance archives).
- **Outside counsel / supervising attorney.** No state-specific or high-stakes legal advice is produced without outside counsel engagement (for district counsel) or supervising-attorney sign-off (for clinics). Hard gates fire on due-process complaints, OCR complaints, Title IX findings, and manifestation determinations.

## Skills

| Skill | Does |
|---|---|
| `/education-legal:cold-start-interview` | Cold-start — learns state, audience, and house framing from seed documents |
| `/education-legal:compliance-audit` | Audits a district policy or procedure against IDEA / §504 / FERPA / Title IX / Title VI / EEOA / state code; gap report with citations and severity |
| `/education-legal:iep-review` | Reviews an IEP against 34 CFR §300.320; audience-aware deliverable (district memo / parent redline / clinic-supervised draft) |
| `/education-legal:504-plan-review` | Reviews a 504 plan against 34 CFR §104.35-36; calls out the structural differences from IEPs |
| `/education-legal:manifestation-determination` | Walks the IDEA discipline framework (34 CFR §300.530); two-question analysis; IAES and services-during-removal |
| `/education-legal:ferpa-records-response` | Responds to a records request; identifies education records vs. excluded categories; redacts; logs the access; drafts the response letter |
| `/education-legal:title-ix-grievance` | Walks the Title IX grievance procedure under the regulatory version named in the practice profile |
| `/education-legal:due-process-complaint` | Drafts or reviews an IDEA due-process complaint; enforces required content elements; tracks the resolution-session window |

## Interactive skills vs. scheduled agents

The skills above run when you invoke them — for when you're working a matter. The agent below runs on a schedule — for what moves while you're not looking:

| Agent | What it watches | Default cadence |
|---|---|---|
| **regulation-watcher** | OSEP Dear Colleague Letters and policy guidance; OCR Dear Colleague Letters; Federal Register education entries (Title IX rulemaking is active); state-DOE feed configured in the practice profile | Weekly (Monday) |

## How it learns

Your practice profile at `~/.claude/plugins/config/claude-for-legal/education-legal/CLAUDE.md` isn't static — it improves as you use the plugin. Skills tell you when an output used a default you should tune. You can re-run setup, edit the file directly, or tell a skill to record a new position.

## Notes

- **State law is the operative law.** The plugin encodes the federal floor (IDEA, §504, FERPA, Title IX, Title VI, EEOA). Every analysis applies the federal rule, then explicitly checks the state for a shorter timeline, an additional procedural step, an additional substantive right, a different form, or a different filing location. The state is where compliance actually lives.
- **No fabricated guidance.** Every substantive claim cites the statute, regulation, or controlling case. If the source doesn't support the claim, the skill says so. Provenance tags travel inline — `[CourtListener]`, `[statute / regulator site]`, `[user provided]`, `[model knowledge — verify]`.
- **Person-first language.** "Student with a disability," not "disabled student." The plugin surfaces and replaces dated framing in source documents. Honors stated identity-first preferences when the family or student has expressed one.
- **PII discipline.** Templates, samples, and clinic training materials are redacted by default. Echo only what the immediate output requires.
- **Surface, don't decide.** Eligibility, FAPE, manifestation, and Title IX findings are surfaced for the team or the decision-maker — never decided by the skill.
- **Title IX regs change.** The plugin asks at cold-start which regulatory version is operative for your district at the time of the alleged conduct, and tags every procedural element with that version.
