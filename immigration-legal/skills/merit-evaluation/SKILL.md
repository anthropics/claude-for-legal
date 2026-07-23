---
name: merit-evaluation
description: >
  Criterion-by-criterion merit evaluation for EB-1A, EB-2 NIW, or O-1. Takes an
  applicant profile and evidence inventory, returns GREEN / YELLOW / RED per
  criterion with reasoning and evidence citations, a criterion count, and a filing
  recommendation. The core Meritocrat workflow in skill form. Use when the attorney
  says "evaluate this client", "run merit eval", "how does this person look for
  EB-1A", "NIW analysis", "O-1 assessment", or provides a client profile for review.
argument-hint: "[--visa eb1a|eb2niw|o1a|o1b] [--posture aggressive|standard|conservative] [--tabular] [--compare eb1a,eb2niw]"
---

# /merit-evaluation

Criterion-by-criterion analysis of an applicant's fitness for a specific visa category. Returns a structured assessment with a rating per criterion, reasoning, evidence citations, gaps, and a filing recommendation. Every claim must be tied to specific evidence the attorney provided — no invented facts.

## Instructions

1. **Read the practice profile** at `~/.claude/plugins/config/claude-for-legal/immigration-legal/CLAUDE.md`. Extract: risk posture for the requested visa type, evidence standards (citation thresholds, media tier, comparable evidence posture), and escalation rules.

2. **Load the appropriate reference file** from this skill's directory:
   - EB-1A → `eb1a-criteria.md`
   - EB-2 NIW → `eb2niw-prongs.md`
   - O-1A or O-1B → `o1-criteria.md`

3. **Collect the applicant profile.** If not provided, ask. You need:
   - Full name and field/industry
   - Career stage (early / mid / senior / established)
   - Evidence inventory (what do they have? — publications, citations, awards, press, roles, salary data, expert letters available, etc.)
   - Proposed endeavor / role in the US (for NIW: especially important)
   - Any prior immigration history (prior visa approvals, RFEs, denials)

4. **Run the criterion analysis** per the visa type.

5. **Return the structured output** per the format below.

6. **Apply escalation rules.** If the result falls into an escalation scenario (borderline criterion count, YELLOW on 2+ criteria, etc.), flag it per `## Escalation rules` in the practice profile.

---

## Flags

`--visa` — specify the visa type. If omitted, ask the attorney which visa to evaluate for. If the attorney says "run all three" or "compare EB-1A and NIW", run both and produce a side-by-side comparison.

`--posture` — override the practice profile posture for this evaluation only. Useful when the attorney wants to see how the case looks through a different lens before deciding how to file.

`--tabular` — output the criterion table only, without the narrative reasoning. Useful when the attorney wants a quick read before diving into analysis.

`--compare` — run evaluation for multiple visa types and return a comparison table. Example: `--compare eb1a,eb2niw`

---

## Posture definitions

Apply the firm's calibrated posture from the practice profile, unless overridden by `--posture`:

**Aggressive:** Lend benefit of the doubt on borderline evidence. If evidence is present but thin, call YELLOW rather than RED. If evidence is strong in the right direction, call GREEN even if not overwhelming. Note the aggressive call explicitly so the attorney can decide whether to push it.

**Standard:** Apply USCIS Policy Manual guidance as written. GREEN means clearly met. YELLOW means arguable — the criterion can be claimed but carries RFE risk. RED means the criterion is not met on current evidence.

**Conservative:** Require clear, unambiguous evidence before calling GREEN. YELLOW means real risk of USCIS denial on that criterion. RED means do not file without more evidence.

---

## Output format

### Header

```
MERIT EVALUATION — [VISA TYPE]
Applicant: [Name]
Field: [Field]
Posture: [Aggressive / Standard / Conservative] (from practice profile [or: override])
Date: [YYYY-MM-DD]
Attorney: [from practice profile]

PRIVILEGED & CONFIDENTIAL — ATTORNEY WORK PRODUCT — PREPARED AT THE DIRECTION OF COUNSEL
```

---

### For EB-1A

#### Criterion table

| # | Criterion | Rating | Evidence on hand | Gaps | Notes |
|---|---|---|---|---|---|
| 1 | Prizes / Awards | 🟢 GREEN / 🟡 YELLOW / 🔴 RED | [specific evidence] | [what's missing] | [reasoning, posture call] |
| 2 | Membership | … | … | … | … |
| 3 | Published material about | … | … | … | … |
| 4 | Judging | … | … | … | … |
| 5 | Original contributions | … | … | … | … |
| 6 | Scholarly articles | … | … | … | … |
| 7 | Artistic exhibitions | … | … | … | … |
| 8 | Leading/critical role | … | … | … | … |
| 9 | High salary | … | … | … | … |
| 10 | Commercial success | … | … | … | … |

**Criteria met (GREEN):** [count] of 10
**Criteria arguable (YELLOW):** [count] of 10
**Criteria not met (RED):** [count] of 10
**Minimum threshold:** 3 criteria required

#### Criterion-by-criterion reasoning

For each criterion (one section per criterion):

**[Number]. [Criterion name]** — 🟢 GREEN / 🟡 YELLOW / 🔴 RED

*Regulatory standard:* [one-sentence statement of what this criterion requires, cited to 8 CFR 204.5(h)(3) or Policy Manual]

*Evidence assessed:* [specific evidence provided — cite what the attorney gave you, not invented evidence. If no evidence was provided for this criterion, state that explicitly.]

*Analysis:* [Apply the regulatory standard to the evidence. Explain the reasoning. Note where posture affected the call. Cite any policy guidance that governs this type of evidence.]

*Gaps / what would strengthen this criterion:* [Specific, actionable — not "more evidence" but "evidence from a publication at or above the national trade press tier" or "a citation report showing total citations exceed [threshold from practice profile]"]

---

#### Final merits assessment (Kazarian step 2 — EB-1A)

After completing the criterion table, address the holistic inquiry:

> Does the totality of the evidence, even setting aside the individual criteria, establish that this beneficiary is among the small percentage at the very top of their field with sustained national or international acclaim?

[2–4 sentence holistic assessment. Identify the strongest pillar of the case. Identify the most significant vulnerability. This is attorney judgment territory — the skill provides analysis, not legal advice.]

---

#### Filing recommendation

**Recommendation:** [File now / Develop additional evidence first — specify what / Do not file — specify why]

**Reasoning:** [2–3 sentences. Tie the recommendation to the criterion count, the posture, the escalation rules in the practice profile, and the holistic assessment.]

**Escalation:** [Per practice profile `## Escalation rules`: this decision [does / does not] require partner sign-off / second reviewer. Reason: [quote the applicable escalation rule].]

**Evidence development priorities (if not filing now):** [Ranked list of the 2–3 evidence items that would most improve the case, in order of impact and practicality.]

---

### For EB-2 NIW

Replace the criterion table with a prong table:

| Prong | Rating | Evidence on hand | Gaps | Notes |
|---|---|---|---|---|
| 1 — Substantial merit + national importance | 🟢 / 🟡 / 🔴 | … | … | … |
| 2 — Well-positioned to advance the endeavor | 🟢 / 🟡 / 🔴 | … | … | … |
| 3 — Beneficial to waive job offer/labor cert | 🟢 / 🟡 / 🔴 | … | … | … |
| Proposed endeavor specificity | 🟢 / 🟡 / 🔴 | … | … | [Is the proposed endeavor concrete enough?] |

**All three prongs required.** If any prong is RED, the petition cannot proceed without addressing it — note prominently.

Prong-by-prong reasoning follows the same format as EB-1A criterion reasoning.

**Proposed endeavor assessment:** Evaluate whether the description of the beneficiary's proposed work in the US is specific enough to support all three prongs. Flag vagueness as a separate issue — it is a common RFE trigger.

Filing recommendation follows the same format.

---

### For O-1A

Replace with O-1A criterion table (8 criteria, need 3):

| # | Criterion | Rating | Evidence on hand | Gaps | Notes |
|---|---|---|---|---|---|
| O1A-1 | Prizes / Awards | … | … | … | … |
| O1A-2 | Membership | … | … | … | … |
| O1A-3 | Published material about | … | … | … | … |
| O1A-4 | Judging | … | … | … | … |
| O1A-5 | Original contributions | … | … | … | … |
| O1A-6 | Scholarly articles | … | … | … | … |
| O1A-7 | Critical/essential capacity | … | … | … | … |
| O1A-8 | High salary | … | … | … | … |

Also note: **Advisory opinion requirement** — identify the applicable peer group / union / professional organization. Flag if no advisory opinion source has been identified.

For O-1B (Arts or MPTV), adapt the criterion list from `o1-criteria.md` and note the distinction standard vs. extraordinary achievement standard as applicable.

---

### Comparable evidence section (O-1 only)

If the firm posture permits comparable evidence:

> **Comparable evidence analysis:**
> Do any of the standard criteria not readily apply to this beneficiary's occupation? [Yes / No — reasoning]
> If yes: what comparable evidence could establish the same type of extraordinary ability? [Specific evidence types]
> Firm posture on comparable evidence: [from practice profile]

If firm posture is "never" → omit this section; note that comparable evidence is not in scope for this firm.

---

### Cross-visa comparison (--compare flag)

When running a comparison, produce a summary table after all individual analyses:

| | EB-1A | EB-2 NIW | O-1A |
|---|---|---|---|
| Criteria met | [N]/10 | [all 3 prongs? Y/N] | [N]/8 |
| Strongest criterion/prong | [name] | [name] | [name] |
| Most significant gap | [name] | [name] | [name] |
| Filing readiness | [Ready / Develop first / Not ready] | … | … |
| **Recommendation** | | | |

Conclude with: "Recommended visa type for this applicant: [type] — [2-sentence rationale]."

---

## Evidence citation discipline

Every GREEN or YELLOW call must cite *specific* evidence the attorney provided. Do not infer evidence that was not stated. If evidence for a criterion was not provided, that criterion defaults to RED (unless posture is aggressive AND there is a reasonable basis to expect the evidence exists based on the career profile — in which case, call YELLOW and flag "assumed — confirm before filing").

**Never say:** "The beneficiary likely has…" or "As a [field] professional, they probably have…"
**Always say:** "Evidence provided: [specific item]. Evidence not provided for this criterion: [note gap]."

---

## Interpretability guarantee

Every criterion conclusion must be traceable: attorney can see the regulatory standard applied, the evidence assessed, and the reasoning for the rating. If a call feels wrong, the attorney can identify exactly where to push back and what evidence would change the rating. This is the interpretability that makes the evaluation useful, not just fast.

---

## Failure modes to avoid

- **Inflating ratings to make the case look stronger.** The attorney needs an honest read, not optimism. YELLOW means real RFE risk. RED means do not file without more evidence.
- **Evaluating EB-1A criteria for a NIW case.** Load the right reference file for the visa type.
- **Ignoring the practice profile posture.** Posture is how the firm practices — don't override it silently.
- **Producing a generic assessment without citing specific evidence.** Every rating must be traceable to what the attorney provided.
- **Forgetting the escalation check.** Always apply `## Escalation rules` from the practice profile before closing the output.
