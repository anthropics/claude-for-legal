---
name: iep-review
description: >
  Review an IEP draft or finalized IEP against IDEA's required content (34 CFR
  §300.320) — present levels, measurable annual goals, services, accommodations,
  LRE justification, transition (if applicable), and the special-factor
  checklists. Audience-aware: district-counsel compliance memo, parent-advocate
  redline, clinic-supervised draft. Use when the user says "review this IEP",
  "check this IEP", "are these goals measurable", "is this LRE justified", or
  attaches an IEP.
argument-hint: "[IEP file path, or paste the IEP]"
---

# /iep-review

1. Load `~/.claude/plugins/config/claude-for-legal/education-legal/CLAUDE.md` → state(s), audience context, IDEA section, transition-age start, LRE continuum, seed-document house style.
2. Use the workflow below.
3. Check every required content element under 34 CFR §300.320. Apply the state overlay flagged in the practice profile.
4. Surface findings — do NOT decide FAPE. Eligibility, FAPE, and the team's substantive judgment stay with the IEP team.

---

## Matter context

Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗`, skip — skills use practice-level context. If enabled and there is no active matter, ask: "Which matter is this for?" Load the active matter's `matter.md`. Write outputs to the matter folder. Never read another matter's files unless `Cross-matter context` is `on`.

---

## Purpose

An IEP is a legal document with seven required content categories under 34 CFR §300.320. Most IEPs comply on the structural surface and fall down on the substance — goals that aren't measurable, LRE justifications that conclude rather than analyze, transition plans that are checkbox-only, services that are written so vaguely they can't be implemented or enforced. The skill checks the structure and then probes the substance.

**Hard gate:** this skill does NOT produce a "this IEP denies FAPE" conclusion. FAPE is a team determination informed by *Endrew F.*'s "appropriately ambitious" standard; the team applies it to the individual student. The skill surfaces findings — the team decides.

## Load context

`~/.claude/plugins/config/claude-for-legal/education-legal/CLAUDE.md` → state(s), audience context, district's IEP system, LRE continuum, transition-age start, house style from seed IEPs.

## Output header

Prepend the work-product header per CLAUDE.md `## Outputs`. For parent-advocate audience, the header is "RESEARCH NOTES — NOT LEGAL ADVICE" unless the user is a lawyer.

## Workflow

### Step 1: Identify the audience framing

Read `## Who's using this → Audience context` in CLAUDE.md. The deliverable's framing branches here:

- **District counsel / LEA staff** → compliance memo. "Here's what's exposure-creating, here's the fix." Severity-rated findings. Internal action items.
- **Parent / family advocate** → parent-facing redline or rights-asserting letter. "Here's what the law requires, here's what the IEP does, here's the gap." Plain-language; statutory cites for backup; never adversarial-for-its-own-sake.
- **Clinic supervisor / clinic student** → supervised-draft framing. Every conclusion gated for supervisor sign-off. Citations doubled-checked. Pedagogical — show the analysis.

The findings are the same. The deliverable differs.

### Step 2: Run the §300.320 content checklist

For each required category, check presence AND substance. A category that's present but vacuous is a finding.

#### (a) Present levels of academic achievement and functional performance (PLAAFP)

- Specific, current, data-supported? Or generic ("works below grade level")?
- Does it describe how the disability affects involvement and progress in the general curriculum?
- Are the data sources cited (assessments, work samples, observations, dates)?
- For ages 16+ (or younger if state policy): does it include the data that supports the transition plan (transition assessments, student interview, parent input)?

#### (b) Measurable annual goals

This is the most-fudged section. Apply the four-component test for each goal:

| Component | Question |
|---|---|
| **Condition** | Under what circumstances will the student perform? (Setting, materials, prompts.) |
| **Behavior** | What observable, measurable action is the goal? ("Will know" is not measurable; "will identify orally given a printed list" is.) |
| **Criterion** | What's the standard for mastery? (Accuracy %, frequency, duration, trials.) |
| **Timeframe** | By when? |

Flag any goal that fails any of the four components. Flag goals that bundle multiple skills ("will improve reading"). Flag goals where the criterion is "as observed by the teacher" — that's an observation method, not a criterion.

#### (c) Progress measurement

For each goal: how is progress measured (assessment instrument, observation protocol, work-sample analysis)? How often will the parent be informed? Is the measurement method actually capable of detecting the change the goal describes?

#### (d) Services, accommodations, and supplementary aids

- Each service stated as a measurable unit: frequency × duration × location × start date × end date. "Speech therapy weekly" is not a service description; "Speech therapy, 30 min/week, individual, speech room, beginning [date] through [date]" is.
- Accommodations distinguishable from modifications. Accommodations change how, not what; modifications change what.
- Supplementary aids and services explicitly listed (this is load-bearing for the LRE analysis under step (e)).

#### (e) LRE justification

Federal IDEA requires removal from the general education environment only when education in the general environment with supplementary aids and services cannot be achieved satisfactorily (34 CFR §300.114-117). The justification must:

- Identify the placement on the LRE continuum (general ed with supports, resource, separate class, separate school, residential, etc.).
- Describe the supplementary aids and services considered.
- Explain why each less-restrictive option was rejected.

A justification that says "the student needs a self-contained setting because of his disability" is conclusory and not what the law requires. Flag.

#### (f) Transition services (if applicable)

Federal IDEA: transition plan required no later than the IEP in effect when the student turns 16 (34 CFR §300.320(b)). Many states set this earlier — Texas at 14, several states earlier still. Check the practice profile's `## IDEA / Special education → Transition-planning start age`.

If applicable, check:
- Appropriate measurable postsecondary goals based on age-appropriate transition assessments (education, employment, independent living where appropriate).
- Transition services needed to assist the student in reaching those goals.
- Courses of study aligned with the postsecondary goals.

Vague postsecondary goals ("will pursue further education") are findings.

#### (g) Special-factor checklists

For each, was it considered, and if a need was identified, is it addressed?

- Behavior impeding learning → Behavior Intervention Plan (BIP) and/or positive behavior supports?
- Limited English proficiency → language needs?
- Blind or visually impaired → Braille instruction and use (or rationale for not providing)?
- Deaf or hard of hearing → language and communication needs, opportunities for direct communication?
- Assistive technology needs?

A blank box is not a consideration. Flag.

### Step 3: Apply state overlay

Check the practice profile's `## Jurisdictional footprint` and `## IDEA / Special education` sections for state-specific overlays:

- State evaluation timeline (if shorter than federal 60 calendar days).
- State transition-planning start age.
- State-specific BIP / FBA requirements.
- State-required IEP elements beyond federal (e.g., Texas requires specific Autism Supplements; California requires specific State Standards alignment).

> **Research and cite state overlay before flagging.** Do not rely on memory for state-specific IEP elements. For the state(s) in scope, identify the currently operative state special-education code section governing IEP content, any state administrative rules, and the state DOE's published IEP form. Cite with pinpoint citations. Verify currency.

### Step 4: Substance probe — *Endrew F.* and progress

For an IEP review (not just a content check), the substance question matters: is the IEP reasonably calculated to enable the student to make progress appropriate in light of the student's circumstances (*Endrew F. v. Douglas County School District*, 580 U.S. 386 (2017))?

This is NOT a question the skill answers — it's a question the team answers. But the skill can surface signals:

- Are the goals "appropriately ambitious," or are they sub-grade-level for a student capable of grade-level work?
- Have prior IEPs' goals been mastered? If not, has the IEP team adjusted services?
- Does the IEP describe progress, or does it recite the same goals year after year?

Flag these as `[review]` items for the team. The skill does not conclude denial of FAPE.

### Step 5: Source attribution and currency

Per CLAUDE.md `## Source attribution`: tag every citation. The IDEA regulations (34 CFR Part 300) are stable but not immutable; OSEP and OCR guidance shifts; *Endrew F.* is settled, but its application to specific service decisions is fact-bound.

> **No silent supplement.** If a research query returns thin results for state-overlay IEP elements, report what was found and stop. Do not fill the gap from web search or model knowledge without asking.

## Output

```markdown
[WORK-PRODUCT HEADER — per plugin config ## Outputs — differs by role and audience]

## IEP Review: [Student initials or matter slug] — [Grade] — [State]

**Overall:** [Compliance gaps identified — see findings | Structurally complete; substance flags for team | Ready for finalization]

### Required content (34 CFR §300.320)
| Element | Status | Notes |
|---|---|---|
| Present levels (a) | [✓ / ⚠️ / 🔴] | [specific finding] |
| Annual goals (b) | [✓ / ⚠️ / 🔴] | [N goals reviewed; M fail measurability] |
| Progress measurement (c) | [✓ / ⚠️ / 🔴] | [specific finding] |
| Services / accommodations (d) | [✓ / ⚠️ / 🔴] | [specific finding] |
| LRE justification (e) | [✓ / ⚠️ / 🔴] | [specific finding] |
| Transition (f, if applicable) | [✓ / ⚠️ / 🔴 / N/A] | [specific finding] |
| Special factors (g) | [✓ / ⚠️ / 🔴] | [which were and weren't considered] |

### Goals — measurability detail
[Goal-by-goal table or list. For each: condition / behavior / criterion / timeframe — flag missing components.]

### LRE
[Continuum placement; supplementary aids considered; whether the justification reasons or concludes.]

### State overlay
[State-specific IEP elements; whether each is present. Cited.]

### Substance probe (for team consideration)
[*Endrew F.* signals — `[review]` items the team should weigh. Not a FAPE conclusion.]

### Action items
- [ ] [specific change needed; cite the §300.320 subpart]
```

**Person-first language enforced throughout the output.** If the source IEP uses deficit framing, flag it and offer the person-first alternative.

**PII discipline.** Echo only what the output requires. Use student initials or a matter slug in any persistent files.

## Consequential-action gate

This skill does not produce a FAPE conclusion. If the user asks "is this IEP FAPE-compliant?", respond:

> "FAPE is a team determination under *Endrew F.* — appropriately ambitious in light of the student's circumstances. I can surface the findings the team should weigh, and flag goals or services that fall short of statutory or regulatory requirements, but I won't conclude FAPE for the team. Here's what I'd bring to the IEP meeting."

Then deliver the findings.

**Before finalizing a parent-facing redline (advocate audience):** read `## Who's using this`. If the Role is non-lawyer, gate:

> Filing or sending a redline that asserts the district has failed to provide FAPE is a step toward due process. Have you reviewed this with an attorney? If yes, proceed. If no, here's a brief to bring to them:
>
> - Student (initials), grade, state, district
> - Findings — by §300.320 subpart, with severity
> - Goals failing measurability (count + examples)
> - LRE justification deficiencies
> - State-overlay gaps
> - What relief is being requested
> - What could go wrong (waiver, statute of limitations under IDEA, the district's likely response)

Do not produce a "send this letter" output past this gate without an explicit yes.

---

## Close with the next-steps decision tree

End with the next-steps decision tree per CLAUDE.md `## Outputs`. Customize the options:

- **Draft the parent letter / district memo / IEP team brief** — produce the audience-appropriate deliverable.
- **Escalate** — for district counsel, draft an outside-counsel brief; for advocate, draft a referral note.
- **Get more facts** — what's missing (evaluation data, prior IEPs, progress reports, parent input).
- **Watch and wait** — set the next ARD/IEP-meeting date; revisit then.
- **Something else.**

## What this skill does NOT do

- **Determine FAPE.** Team determination. The skill surfaces signals.
- **Decide eligibility.** That's the multidisciplinary team's call (and a different decision from the IEP review).
- **Draft the IEP** — reviews it.
- **State state-specific rules from memory** — every state-overlay rule is researched and cited at the time of review.
- **Write a parent's name into a persistent file.** Initials or matter slug only.
