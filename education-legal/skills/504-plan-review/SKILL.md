---
name: 504-plan-review
description: >
  Review a Section 504 plan against 34 CFR §104.35-36 — eligibility framework,
  accommodations (not specially designed instruction), no measurable-goals
  requirement, procedural safeguards. Calls out the structural differences from
  IEPs. Audience-aware deliverable. Use when the user says "review this 504
  plan", "is this student eligible under §504", "check this accommodation
  list", or attaches a 504 plan.
argument-hint: "[504 plan file path, or paste the plan]"
---

# /504-plan-review

1. Load `~/.claude/plugins/config/claude-for-legal/education-legal/CLAUDE.md` → state(s), audience context, §504 coordinator, template location.
2. Use the workflow below.
3. Check eligibility framework, accommodations, procedural safeguards. Apply the state overlay.
4. Surface findings. Do NOT decide eligibility — that's the team's call under §104.35(c).

---

## Matter context

Check `## Matter workspaces` in CLAUDE.md. If enabled and no active matter, ask which matter. Otherwise practice-level.

---

## Purpose

Section 504 is a different statute from IDEA — anti-discrimination, not entitlement-to-FAPE-as-specially-designed-instruction. The framework, eligibility test, and procedural requirements are different. The most common error in 504 review is reflexively applying IEP logic — looking for measurable annual goals (there are none), looking for an LRE continuum (the analysis is different), looking for transition plans (not required at all). This skill keeps the §504 framework on its own footing.

**Hard gate:** this skill does NOT conclude eligibility. Under 34 CFR §104.35(c), eligibility is a team determination based on information from a variety of sources. The skill surfaces findings; the team decides.

## Load context

`~/.claude/plugins/config/claude-for-legal/education-legal/CLAUDE.md` → state(s), audience context, §504 coordinator, template location, state overlay.

## Output header

Prepend the work-product header per CLAUDE.md `## Outputs`.

## Workflow

### Step 1: Audience framing

Same branching as `iep-review`: district-counsel memo, parent-advocate redline, clinic-supervised draft.

### Step 2: Eligibility framework (34 CFR §104.35)

A student is eligible under §504 if the student:
1. Has a physical or mental impairment;
2. That substantially limits;
3. One or more major life activities.

Under the ADAAA (which §504 incorporates via cross-reference and OCR has explicitly applied to §504), "substantially limits" is construed broadly. Major life activities include caring for oneself, performing manual tasks, seeing, hearing, eating, sleeping, walking, standing, lifting, bending, speaking, breathing, learning, reading, concentrating, thinking, communicating, and working (and major bodily functions).

For each prong, check the eligibility documentation:
- **Impairment** — identified, supported by evaluation data?
- **Substantial limitation** — analyzed in comparison to the average student, without consideration of mitigating measures (other than ordinary eyeglasses or contacts) per ADAAA?
- **Major life activity affected** — named, with the connection to school performance described?

A plan that lists a diagnosis and accommodations without working through these three prongs is missing the eligibility analysis. Flag.

> **Research the OCR guidance on §504 eligibility before relying.** OCR has issued multiple Dear Colleague Letters interpreting §504 eligibility under the ADAAA. The currently operative guidance set may differ from prior versions; some letters have been rescinded. Cite by source and date. Verify currency. `[OCR guidance — verify currency]`

### Step 3: Evaluation (34 CFR §104.35(a)-(b))

- Was an evaluation conducted before placement and any significant change in placement?
- Was the evaluation drawn from a variety of sources (aptitude and achievement tests, teacher recommendations, physical condition, social and cultural background, adaptive behavior)?
- Was a knowledgeable group of persons assembled, including persons knowledgeable about the student, the evaluation data, and placement options (§104.35(c)(3))?

Flag a 504 plan where the evaluation step appears skipped — common error when a 504 plan is built off a single doctor's note without a team meeting.

### Step 4: Accommodations — not specially designed instruction

§504 plans typically deliver accommodations (changes to how, when, or where the student accesses content) rather than specially designed instruction (changes to what is taught — IDEA territory).

- Each accommodation specific enough to implement: "extended time" alone is not enough (extended to what — 1.5x? 2x? unlimited?); "preferential seating" alone is not enough (near the teacher? away from windows? specific student?).
- Where the accommodation is provided: which classes, which settings.
- Who is responsible: which staff implements, which staff communicates.

If the plan crosses into specially designed instruction (modified curriculum, separate instruction, goals against which progress is measured), that's a signal the student may need an IEP under IDEA, not a §504 plan. Flag as `[review]` — the team decides.

### Step 5: Procedural safeguards (34 CFR §104.36)

§504 requires:
- Notice to parents.
- An opportunity to examine relevant records.
- An impartial hearing with the right to participation by counsel.
- A review procedure.

Districts often adopt §504 procedures that parallel IDEA's procedural safeguards. Check the district's adopted procedure (location in the practice profile) against §104.36 requirements.

### Step 6: State overlay

Some states overlay additional 504 requirements (timeline for evaluation, required participants on the team, periodic-review cadence). Check the practice profile's `## Section 504` and `## Jurisdictional footprint`.

> **Research state §504 overlay before flagging.** Do not rely on memory.

### Step 7: Source attribution

Per CLAUDE.md `## Source attribution` — tag citations. ADAAA-§504 guidance is a moving target (OCR guidance has shifted); the 2024 §504 regulations updated several provisions. Verify currency.

## Output

```markdown
[WORK-PRODUCT HEADER]

## §504 Plan Review: [Student initials] — [Grade] — [State]

**Overall:** [Compliance gaps identified | Structurally complete; team-judgment items for review | Ready]

### Eligibility (34 CFR §104.35)
| Prong | Status | Notes |
|---|---|---|
| Impairment | [✓ / ⚠️ / 🔴] | |
| Substantial limitation (ADAAA broad construction) | [✓ / ⚠️ / 🔴] | |
| Major life activity affected | [✓ / ⚠️ / 🔴] | |

### Evaluation (§104.35(a)-(c))
[Variety of sources; team composition; pre-placement check.]

### Accommodations
[Each accommodation, with specificity check; flag any that cross into specially designed instruction.]

### Procedural safeguards (§104.36)
[Notice, records access, hearing, review — present and adequate?]

### State overlay
[State-specific §504 requirements, cited.]

### IDEA cross-check
[Does anything in the §504 plan suggest the student may need an IEP under IDEA instead? `[review]` for the team.]

### Action items
- [ ] [specific change needed; cite the §104.xx subpart]
```

**Person-first language enforced. PII discipline applied.**

## Consequential-action gate

If the user asks "is this student eligible under §504?", respond:

> "Eligibility under §504 is a team determination under §104.35(c). I can surface the eligibility analysis the team should work through — the three-prong framework, the evaluation data, the ADAAA broad-construction guidance — but I won't conclude eligibility for the team."

Then deliver the analysis.

**For parent-advocate audience, the gate before producing a letter alleging §504 violations:** same gate as `iep-review` — read `## Who's using this`, gate non-lawyer use with the brief-for-attorney structure.

---

## Close with the next-steps decision tree

Per CLAUDE.md `## Outputs`.

## What this skill does NOT do

- **Determine eligibility.** Team determination.
- **Apply IEP logic to a §504 plan.** Different statute, different framework.
- **State ADAAA / §504 guidance from memory** — every guidance reference is researched and cited at review time.
- **Draft the 504 plan** — reviews it.
