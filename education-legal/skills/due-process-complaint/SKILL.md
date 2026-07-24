---
name: due-process-complaint
description: >
  Draft or review an IDEA due-process complaint (34 CFR §300.508). Enforces
  the required content elements; tracks the 15-day resolution-session window
  and the 30-day pre-hearing resolution period; surfaces state-DOE-specific
  filing requirements (where filed, format, language). Use when the user says
  "due process complaint", "DPC", "request for due process hearing",
  "sufficiency challenge", "resolution session", or attaches a complaint.
argument-hint: "[draft complaint, or describe the dispute (parties, issues, proposed remedy)]"
---

# /due-process-complaint

1. Load `~/.claude/plugins/config/claude-for-legal/education-legal/CLAUDE.md` → state(s), state-DOE filing location, audience context.
2. For a draft: build the complaint with the §300.508(b) content elements. For a review: check the existing complaint against §300.508(b) and sufficiency standards.
3. Apply state-DOE filing overlay (location, format, language requirements).
4. Surface the 15-day and 30-day timelines.

---

## Matter context

Due-process complaints are matter-driven. If matter workspaces are enabled, use the active matter. Otherwise practice-level with strong PII discipline.

---

## Purpose

A due-process complaint is the procedural mechanism for challenging an LEA's identification, evaluation, placement, or provision of FAPE for a student with a disability (IDEA, 20 USC §1415(b)(6); 34 CFR §300.507-518). Most complaints fail not on the merits but on the procedural front — required content elements missing, sufficiency challenges sustained, resolution-session protocols misapplied. The skill builds the procedural compliance in.

**Hard gate:** filing a due-process complaint is a consequential legal action with statute-of-limitations consequences (under IDEA, 2 years from when the parent knew or should have known of the action, unless the state sets a different period). The skill produces drafts and reviews; the lawyer files.

## Load context

Per CLAUDE.md.

## Output header

Per CLAUDE.md `## Outputs`. **The complaint itself is filed externally — strip the privileged header from the filing draft.** The internal analysis carries the header.

## Workflow

### Step 1: Audience framing

- **Parent advocate / parent's counsel** → draft of the complaint to file. The complaint is the deliverable.
- **District counsel** → analysis of a complaint filed against the district, with response strategy, sufficiency review, and resolution-session positioning.
- **Clinic** → supervised draft with conservative gates.

### Step 2: Required content elements (34 CFR §300.508(b))

Every due-process complaint must include:

| Element | Requirement |
|---|---|
| (1) Student's name | |
| (2) Address of residence | (Or contact info if homeless under McKinney-Vento) |
| (3) Name of school the student is attending | |
| (4) Description of the nature of the problem | Including facts relating to the problem |
| (5) Proposed resolution | To the extent known and available at the time |

These are jurisdictional. A complaint missing any element is subject to a **sufficiency challenge** under §300.508(d).

For a draft: build each element. For a review: check each element.

### Step 3: Statute of limitations

- Federal default: 2 years from when the party knew or should have known of the alleged action that forms the basis of the complaint (§300.507(a)(2)).
- Exceptions: specific misrepresentations by the LEA that the LEA had resolved the problem; LEA's withholding of information that the LEA was required under IDEA to provide.
- Some states set a different period. Verify the state-specific limit.

> **Research the state-specific SOL. Do not rely on memory. Cite.**

If the limitations issue is borderline, flag as `[review]`. The skill does not silently decide SOL.

### Step 4: Issues — frame as discrete due-process claims

A due-process complaint typically frames issues as discrete claims, each with:
- The legal basis (specific IDEA provision, §504, or state regulation).
- The factual basis (what the LEA did or failed to do).
- The remedy requested (compensatory services, change in placement, IEE at public expense, change in IEP, reimbursement for private placement, etc.).

Common issue categories:
- Failure to evaluate / re-evaluate in the area of suspected disability.
- Failure to provide FAPE (substantive — *Endrew F.* standard).
- Failure to provide FAPE (procedural — material procedural violations under §300.513(a)).
- LRE / placement disputes.
- Failure to implement the IEP.
- Failure to convene the IEP team or address parent input.
- Discipline-related (manifestation determination, services-during-removal).
- IEE at public expense (after a district evaluation the parent disagrees with).

For each issue, surface the procedural-vs-substantive distinction. Under §300.513(a), procedural violations are only a basis for a FAPE denial finding if they impeded the student's right to FAPE, significantly impeded the parent's opportunity to participate, or caused a deprivation of educational benefit.

### Step 5: Filing — state-DOE overlay

Where the complaint gets filed varies by state:
- Some states: state DOE administers; complaints filed with a specific office/portal.
- Some states: hearing office is a separate entity.
- Some states: specific form is required.
- Some states: complaint must be in English and the parent's native language for the parent's copy.
- All states: a copy goes to the other party simultaneously (§300.508(a)(1)).

Apply the practice profile's `## Jurisdictional footprint → State-DOE complaint filing location`.

> **Research current state filing requirements. Cite. Verify.**

### Step 6: Timelines

| Timeline | Source | Triggered when |
|---|---|---|
| 10 days to respond if no prior PWN | §300.508(e) | Receipt of complaint |
| 15 days for resolution session | §300.510(a) | Receipt of complaint |
| 30-day pre-hearing resolution period | §300.510(b) | Receipt of complaint |
| 15 days for sufficiency challenge | §300.508(d) | Receipt of complaint |
| Hearing officer's 5-day sufficiency decision | §300.508(d)(2) | Receipt of sufficiency challenge |
| 45 days for decision (from end of resolution period) | §300.515(a) | End of 30-day resolution period or sooner resolution |

Some of these run in parallel. The skill produces a timeline calendar.

### Step 7: Resolution session

Within 15 days of receipt of complaint, LEA convenes a meeting with the parents and relevant IEP team members. Purpose: try to resolve the complaint before a hearing.

- Both parties may waive.
- Both parties may agree to mediation instead.
- Resolution-period agreement is binding (and reviewable by court).

For a parent-advocate draft, flag whether the parent wants resolution-session participation or to waive.

### Step 8: Source attribution and currency

Per CLAUDE.md. IDEA procedural safeguards are stable but state implementing rules change. Verify.

## Output

### Draft complaint (parent-advocate use)

```markdown
[The complaint itself — clean, no privileged header — for filing]

# Due Process Complaint Under IDEA

**Filed by:** [Parent name or counsel] on behalf of [Student name or initials], by parent
**Filed with:** [State-DOE filing location]
**Copy to:** [LEA]
**Date:** [date]

## Required content (§300.508(b))

1. **Student:** [name]
2. **Address:** [address] / [McKinney-Vento contact info]
3. **School:** [school name]
4. **Nature of the problem and supporting facts:** [paragraph describing the LEA action or inaction, the dates, the participants, the legal basis]
5. **Proposed resolution:** [requested remedy]

## Issues

### Issue 1: [discrete claim]
**Legal basis:** [IDEA provision; cite]
**Factual basis:** [paragraph; sourced]
**Remedy:** [requested]

### Issue 2: [discrete claim]
...

## Procedural

- Statute of limitations: [date when the parent knew or should have known; complaint timely under §300.507(a)(2) / state-specific period of X]
- Resolution-session posture: [requested / waiving / requesting mediation]
- Notice to LEA: [date complaint served]

[Signature block]
```

### Internal analysis (for review of an incoming complaint, district counsel use)

```markdown
[WORK-PRODUCT HEADER on the internal analysis]

## Due Process Complaint Analysis: [Matter slug]

### Sufficiency review (§300.508(b))
| Required element | Present? | Notes |
|---|---|---|
| (1) Name | [✓/🔴] | |
| (2) Address | [✓/🔴] | |
| (3) School | [✓/🔴] | |
| (4) Nature of problem + facts | [✓/⚠️/🔴] | [specificity check] |
| (5) Proposed resolution | [✓/⚠️/🔴] | |

**Sufficiency challenge:** [available — file by [date] / not available]

### Timeline
[Computed calendar from receipt date, citing each rule.]

### SOL analysis
[Date the parent knew or should have known; statutory period; flag if borderline.]

### Substantive issues
[Each issue framed by the complaint; procedural-vs-substantive call under §300.513(a); strength assessment with `[review]` flags.]

### Resolution-session positioning
[Convene? Waive? Mediate?]

### Action items
- [ ] [response steps with deadlines]
```

**Person-first language. PII discipline — use student initials or matter slug in any internal-analysis files; the filed complaint will use the student's name (required).**

## Consequential-action gate

**Before producing a complaint draft labeled "ready to file":**

> Filing a due-process complaint starts a regulated proceeding with statute-of-limitations, stay-put, and procedural-default consequences. Have you reviewed this complaint with an attorney before filing? If yes, proceed. If no, here's a brief to bring to them:
>
> - Student, school, state, LEA
> - Issues framed and the §300.508(b) compliance check
> - SOL analysis (when did the parent know; is the complaint timely)
> - Resolution-session posture
> - Stay-put implications (§300.518 — what's the current placement and is stay-put protective or harmful here)
> - Remedy requested
> - What could go wrong: sufficiency challenge, SOL bar, stay-put backfire, attorney-fee posture under §1415(i)(3)

Do not produce a final filing version past this gate without an explicit yes.

---

## Close with the next-steps decision tree

Per CLAUDE.md.

## What this skill does NOT do

- **File the complaint.** The lawyer files; the skill drafts.
- **Decide SOL on a borderline date.** Surfaces the analysis for the lawyer.
- **State state-specific filing rules from memory** — researched and cited.
- **Substitute for an IEE / FAPE / placement merits analysis.** The complaint frames the issues; the merits are tried at the hearing.
- **Collapse procedural and substantive FAPE claims.** They are analyzed differently under §300.513(a).
