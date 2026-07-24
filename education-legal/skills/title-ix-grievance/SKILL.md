---
name: title-ix-grievance
description: >
  Walk the Title IX grievance procedure under the regulatory version named in
  the practice profile (the rule has been the subject of active rulemaking and
  litigation — the operative version depends on the date of alleged conduct and
  any injunctions in the circuit). Notice, supportive measures, investigation,
  decision, appeals. Surfaces version-tagged procedural elements; flags
  state-mandated additions. Use when the user says "Title IX complaint",
  "Title IX grievance", "supportive measures", "Title IX investigation",
  "Title IX appeal", or attaches a complaint.
argument-hint: "[complaint or describe the parties, conduct, dates]"
---

# /title-ix-grievance

1. Load `~/.claude/plugins/config/claude-for-legal/education-legal/CLAUDE.md` → state(s), Title IX coordinator, **operative regulatory version**, district's adopted grievance procedure location, investigator/decision-maker model.
2. **Confirm the operative regulatory version before doing substantive work.** The Title IX regulations have been the subject of active rulemaking and litigation; the 2020 final rule, the 2024 final rule, and subsequent injunctions in various circuits mean the operative version depends on (a) the date of the alleged conduct, (b) the date of the institutional action, and (c) the circuit. If the practice profile is silent or stale, stop and ask.
3. Walk the version-appropriate procedural framework below.
4. **Do NOT decide Title IX findings.** The decision-maker (under the operative version's model) makes findings.

---

## Matter context

Check `## Matter workspaces`. K-12 districts may handle multiple Title IX matters simultaneously; per-matter context strongly preferred. Confidentiality between matters is critical.

---

## Purpose

Title IX in K-12 has gone through multiple regulatory cycles in the last decade — 2011 Dear Colleague Letter (rescinded), 2017 interim guidance, 2020 final rule, 2024 final rule with subsequent litigation injunctions in many circuits. The operative version for any given case depends on conduct date, action date, and circuit. The skill does not decide which version applies — that's a legal question for the district's counsel under outside-counsel advice. The skill walks the version named in the practice profile and tags every procedural element with that version.

**Hard gate:** the skill does NOT make Title IX findings. The decision-maker (whose identity depends on the version's model) makes findings on the merits.

## Load context

Per CLAUDE.md. Read `## Title IX` carefully — especially the **Currently-operative regulatory version** line.

If that line is blank, `[PLACEHOLDER]`, or stale: stop. Say:

> "I can't run a Title IX grievance procedure analysis without knowing which regulatory version is operative for your district at the time of the alleged conduct. The rule has changed multiple times. Tell me the version named in your district's adopted grievance procedure, OR tell me the conduct date and the circuit so we can identify the operative version. Verify with outside counsel if the version isn't clear — this is exactly the kind of question that benefits from legal advice."

## Output header

Per CLAUDE.md `## Outputs`. **Strip from external notices that go to complainant or respondent.**

## Workflow

### Step 1: Audience framing

- **District counsel** → internal compliance memo for the Title IX coordinator and superintendent.
- **Parent advocate (for either complainant or respondent's family)** → analysis framed around the party's procedural rights and substantive position.
- **Clinic** → supervised draft; conservative gates on every conclusion.

### Step 2: Confirm operative version — version-tag every element

Each procedural requirement below is tagged with the regulatory version naming it. Apply ONLY the version operative for this matter.

> **Research and verify the operative version before relying.** The 2020 final rule and the 2024 final rule differ on: definition of sexual harassment, single-investigator vs. separated decision-maker, live hearing requirement, cross-examination, standard of evidence permitted, appeal scope. Some 2024-rule provisions have been enjoined in some circuits. Cite the version and check current enforceability. `[Title IX regulatory version — verify]`

### Step 3: Notice

- Notice of allegations to both parties: who, what, when, the conduct alleged, the version's grievance procedure, the right to an advisor.
- For minors (K-12 default): notice to parents.
- Timing: "upon receipt" / "promptly" — version-dependent.

### Step 4: Supportive measures (§106.30 (2020 rule), version-dependent)

- Non-disciplinary, non-punitive, available to both parties.
- Examples: counseling, course adjustments, no-contact directives, schedule adjustments, safety planning.
- Not contingent on a complaint being filed.
- Title IX coordinator promptly contacts the complainant about supportive measures.

In K-12, where complainant and respondent are often classmates, supportive measures interact with IEPs and 504 plans — flag if a measure would change the educational placement.

### Step 5: Filing a formal complaint

- Who can file (complainant or Title IX coordinator, under the version's rules).
- What the complaint must contain.
- Where it's filed.

### Step 6: Investigation

Version-dependent. Common elements across versions:
- Equitable treatment of complainant and respondent.
- Right to inspect and review evidence (version dictates scope and form).
- Right to be accompanied by an advisor.
- Equal opportunity to present witnesses and evidence.

Single-investigator model vs. separated decision-maker is version-dependent. For 2020 rule postsecondary, the live hearing with cross-examination by advisor is required — but **K-12 may use a different model** under the 2020 rule (§106.45(b)(6)(ii)). Verify the K-12 specifics against the version in effect.

### Step 7: Determination

- Standard of evidence: preponderance OR clear-and-convincing — version-dependent and (under some versions) the institution chooses for sex-discrimination cases consistent with the standard for other comparable cases.
- Written determination with required content: allegations, procedural steps, findings of fact, conclusions, sanctions, remedies, appeal rights.

Issued by the decision-maker, separated from the investigator under the version's model where applicable.

### Step 8: Appeals

- Grounds: procedural irregularity, new evidence, conflict of interest/bias, additional version-specific grounds.
- Decision-maker for the appeal must not have been involved in the underlying investigation or decision (separation under most versions).
- Timing.

### Step 9: State overlay

Some states impose additional requirements. For K-12, state-mandated anti-bullying or anti-harassment laws may overlap with Title IX (and overlap with §504 / IDEA when the parties are students with disabilities). Surface the overlay.

> **Research state overlay. Cite. Verify.**

### Step 10: Cross-references that often come up

- If respondent has an IEP or 504 plan and the matter implicates discipline: trigger the manifestation-determination framework alongside Title IX procedure. The two run in parallel, not in series.
- If the matter involves protected-class harassment beyond sex (race, national origin, religion): Title VI, OCR jurisdiction, possibly EEOA — flag.
- FERPA: investigation records are education records subject to FERPA. Disclosure to the opposing party in the grievance procedure is generally permitted under Title IX's procedural rights, which Title IX coordinates with FERPA via specific exceptions.

## Output

```markdown
[WORK-PRODUCT HEADER on internal analysis]

## Title IX Grievance Analysis: [Matter slug] — [District / State]

**Regulatory version applied:** [version, with date and source] `[Title IX version — verify]`
**Conduct date:** [date] (drives version determination)
**Procedural posture:** [Notice / Supportive measures / Investigation / Determination / Appeal]

### Notice
[Status, completeness against version's requirements.]

### Supportive measures
[Offered, accepted, intersecting with IEP/504 if applicable.]

### Investigation (version-tagged)
[Each procedural element, with version cite.]

### Determination (version-tagged)
[Standard of evidence; decision-maker separation; required content.]

### Appeals
[Grounds, decision-maker, timing — version-tagged.]

### State overlay
[State-mandated additions; cited.]

### Cross-references
- [IEP / 504 / manifestation — if respondent or complainant has one]
- [Title VI / EEOA — if other protected-class allegations]
- [FERPA — coordination with investigation records]

### Action items
- [ ] [version-specific procedural step, with cite]
```

**Person-first language. PII discipline doubly important here — Title IX matters involve sensitive sexual conduct allegations. Echo only what the immediate output requires; use party initials or matter slug; never write names into persistent files.**

## Consequential-action gate

If the user asks "did this conduct violate Title IX?" or "should we sustain the complaint?":

> "Title IX findings are made by the decision-maker under the operative version's model — not by this skill. I can produce the procedural analysis the decision-maker should work through and flag the procedural elements the version requires, but I won't conclude the merits."

Before issuing a written determination or a notice that goes to a complainant or respondent:

> A written determination has direct legal consequences — it triggers appeal rights, sanctions, and possibly OCR exposure. The version applied here is [X], and I'm not in a position to confirm that's the operative version for your district at the time of this conduct. Have you confirmed the operative version with outside counsel? If yes, proceed. If no, here's the brief: [version applied, conduct date, circuit, what was decided, what's at stake].

Do not produce a final written determination past this gate without an explicit yes.

---

## Close with the next-steps decision tree

Per CLAUDE.md.

## What this skill does NOT do

- **Decide the operative regulatory version.** That's a legal question for outside counsel; the skill applies the version named in the profile.
- **Make findings on the merits.** Decision-maker territory.
- **Apply postsecondary Title IX requirements to K-12 without flagging the K-12-specific provisions.** K-12 and higher ed are structurally different under the rule.
- **Skip the version-tagging.** Every procedural element gets the version cite.
- **Write party names into persistent files.** Initials or matter slug.
