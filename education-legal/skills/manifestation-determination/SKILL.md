---
name: manifestation-determination
description: >
  Walk the IDEA discipline framework (34 CFR §300.530): 10-school-day rule,
  the two statutory questions answered separately, IAES (interim alternative
  educational settings), services-during-removal. Produces a structured
  determination memo for the team; surfaces state overlay (longer-than-federal
  removal limits, restraint/seclusion). Use when the user says "manifestation
  determination", "MDR", "10-day rule", "this student has been suspended",
  or describes a disciplinary removal of a student with an IEP.
argument-hint: "[discipline file path, or describe the removal pattern + IEP context]"
---

# /manifestation-determination

1. Load `~/.claude/plugins/config/claude-for-legal/education-legal/CLAUDE.md` → state(s), audience context, discipline framework, MDR participants, IAES placements.
2. Walk the workflow below.
3. Answer the two statutory questions **separately** — causal relationship AND failure to implement.
4. Surface the determination structure. **Do NOT decide whether the conduct was a manifestation** — that's the team's call under §300.530(e).

---

## Matter context

Check `## Matter workspaces`. If enabled and no active matter, ask. Otherwise practice-level.

---

## Purpose

A manifestation determination is one of the highest-stakes routine decisions in K-12 education law. Get it wrong and the student is removed from the educational placement without the FAPE the IEP requires; get it wrong in the other direction and the district is exposed to a due-process complaint. The two statutory questions are independent and must be answered separately — collapsing them is the most common error. This skill walks the framework and forces the structure.

**Hard gate:** the skill does NOT decide manifestation. Under 34 CFR §300.530(e), the LEA, parent, and relevant members of the student's IEP team make the determination. The skill produces the analysis for the team.

## Load context

`~/.claude/plugins/config/claude-for-legal/education-legal/CLAUDE.md` → state(s), discipline framework, MDR participants, IAES placements, restraint/seclusion policy.

## Output header

Per CLAUDE.md `## Outputs`.

## Workflow

### Step 1: Audience framing

- **District counsel** → memo for the team and for the file.
- **Parent advocate** → analysis framed around the parent's position, with the two-question structure to bring to the meeting.
- **Clinic** → supervised draft with conservative gates.

### Step 2: Establish the trigger

A manifestation determination is required when the LEA proposes a removal that constitutes a **change in placement** (34 CFR §300.530(e), §300.536). Change in placement is triggered by:

- A removal of more than 10 consecutive school days, OR
- A series of removals that **cumulatively** total more than 10 school days in a school year **and** constitute a pattern, considering:
  - Substantial similarity of conduct across the incidents,
  - Length of each removal,
  - Total amount of time removed,
  - Proximity of removals to one another.

The pattern analysis is fact-bound and judgment-laden. Surface the factual record and the considerations — do not silently decide pattern-vs-not.

**Count the days.** Walk through the removals in the record:

| Date | Incident | Removal length (school days) | Cumulative |
|---|---|---|---|
| | | | |

Flag any state overlay that's more restrictive than federal (e.g., some states limit cumulative removals below 10 days; some states impose additional rules for restraint-and-seclusion incidents).

> **Research state discipline-removal overlay before relying.** State law often imposes additional restrictions. Cite primary sources. Verify currency.

### Step 3: Answer the two statutory questions — SEPARATELY

Under 34 CFR §300.530(e)(1), the team must determine:

> **Question 1 — Causal relationship.** Was the conduct in question **caused by, or had a direct and substantial relationship to, the student's disability**?
>
> **Question 2 — Failure to implement.** Was the conduct in question **the direct result of the LEA's failure to implement the IEP**?

If **either** answer is yes, the conduct IS a manifestation. (§300.530(e)(2)–(3) — and §300.530(f) sets the LEA's obligations when conduct is a manifestation.)

The skill produces structured analysis for each question, **separately**:

#### Question 1 — Causal relationship to the disability

Apply the analytical framework:

- What is the student's disability? (Per the IEP, evaluation report.)
- What are the disability's known behavioral or functional manifestations? (Cite evaluation data, FBA findings, prior BIP, present levels.)
- What was the conduct?
- Is there a direct and substantial relationship between the conduct and the disability's known manifestations?

Surface evidence on both sides:

- **Pointing toward causal relationship:** [evidence — FBA findings, evaluation observations, prior behavior incidents of the same type, services in the IEP designed to address this behavior].
- **Pointing away from causal relationship:** [evidence — conduct unrelated to disability's known manifestations, premeditation suggesting non-disability-driven choice, dissimilar prior behavior].

Do not synthesize a yes/no. The team determines. The skill flags this as `[review — team determination]`.

#### Question 2 — Failure to implement the IEP

This is a different question and requires a different analytical lens:

- What does the IEP require? List specifically: services, frequency × duration × location, accommodations, BIP if any, supplementary aids, supports for school personnel.
- What was actually provided in the period leading up to the incident? Pull service-delivery logs, classroom-implementation evidence, BIP-fidelity data, any documented gaps.
- Is there a direct line between an implementation gap and the conduct?

Common implementation gaps that frequently surface in this analysis:
- BIP not implemented (or implemented inconsistently across staff).
- Accommodations skipped on the day of the incident.
- Services not provided at the frequency the IEP requires.
- Substitute or new staff unaware of the IEP requirements.

Surface evidence on both sides. Do not synthesize. `[review — team determination]`.

### Step 4: If the conduct IS a manifestation (under §300.530(f))

If the team determines manifestation, the LEA must:
- Conduct a functional behavioral assessment (FBA), if not already done, and implement a BIP — or review and modify the existing BIP.
- Return the student to the placement from which removed, unless the parent and LEA agree to a change in placement as part of modification of the BIP.

Exception: if the conduct involves weapons (§300.530(g)(1)), illegal drugs (§300.530(g)(2)), or serious bodily injury (§300.530(g)(3)), the student may be removed to an IAES for up to 45 school days regardless of manifestation.

### Step 5: If the conduct is NOT a manifestation (under §300.530(c))

The student may be disciplined the same way a non-disabled student would be, BUT:
- The student must continue to receive educational services so as to enable the student to continue to participate in the general education curriculum (FAPE during disciplinary removal) — §300.530(d)(1)(i).
- The student must receive, as appropriate, a functional behavioral assessment and behavioral intervention services and modifications designed to address the behavior so it does not recur — §300.530(d)(1)(ii).

The IAES is determined by the IEP team — §300.531.

### Step 6: Apply state overlay

Several states impose additional requirements:
- Some states require manifestation determinations on shorter cumulative thresholds.
- Some states have additional restraint/seclusion documentation requirements.
- Some states have additional rules for §504-eligible students (federal §504 has discipline rules at §104 implementing regs and OCR guidance).

> **Research state overlay. Cite. Verify currency.**

### Step 7: Source attribution

Per CLAUDE.md.

## Output

```markdown
[WORK-PRODUCT HEADER]

## Manifestation Determination Analysis: [Student initials] — [Grade] — [State]

### Trigger
- Proposed removal: [length, dates]
- Cumulative removals YTD: [count and pattern analysis]
- Change-in-placement determination: [met / unclear — `[review]`]

### Question 1 — Causal relationship (34 CFR §300.530(e)(1)(i))
**Disability:** [from IEP / eval]
**Disability's known manifestations:** [from FBA, eval, IEP present levels]
**Conduct:** [factual description]

**Evidence pointing toward causal relationship:**
- [bulleted, sourced]

**Evidence pointing away from causal relationship:**
- [bulleted, sourced]

**Team determination required.** `[review — team determination]`

### Question 2 — Failure to implement (34 CFR §300.530(e)(1)(ii))
**IEP requirements:** [list with frequency × duration × location]
**Implementation record:** [what was actually provided; gaps]
**BIP fidelity (if applicable):** [data]

**Evidence pointing toward implementation failure:**
- [bulleted, sourced]

**Evidence pointing away from implementation failure:**
- [bulleted, sourced]

**Team determination required.** `[review — team determination]`

### Path forward — by determination

**If manifestation (§300.530(f)):**
- FBA / BIP review and modification
- Return to placement, unless parent and LEA agree to change as part of BIP modification
- IAES exception applies only if conduct involves weapons / drugs / serious bodily injury under §300.530(g)

**If not manifestation (§300.530(c)-(d)):**
- Discipline as a non-disabled student would be
- FAPE during removal must continue (§300.530(d)(1)(i))
- FBA and behavioral services as appropriate (§300.530(d)(1)(ii))
- IAES determined by IEP team (§300.531)

### State overlay
[State-specific discipline rules, cited.]

### IAES options available in district
[From practice profile; flag if none on the LRE continuum match the analysis.]
```

**Person-first language. PII discipline. No FAPE conclusion.**

## Consequential-action gate

If the user asks "was this a manifestation?", respond:

> "Manifestation is a team determination under §300.530(e). I can produce the structured analysis the team should work through — the two questions answered separately, the evidence on each side, the implementation record — but I won't conclude manifestation for the team."

Then deliver the analysis.

For non-lawyer audience finalizing an MDR record:

> Finalizing a manifestation determination has direct legal consequences — it determines whether the student stays in placement, what services are required, and the LEA's exposure if the determination is challenged in due process. Have you reviewed this with an attorney? If yes, proceed. If no, here's a brief to bring to them: [conduct summary, the two questions and the evidence for each, the proposed determination, what's at stake].

---

## Close with the next-steps decision tree

Per CLAUDE.md `## Outputs`.

## What this skill does NOT do

- **Decide manifestation.** Team determination.
- **Decide FAPE during removal.** Team-driven; the skill flags requirements.
- **State state-specific discipline rules from memory** — researched and cited at the time of review.
- **Collapse the two statutory questions into one.** They are independent.
