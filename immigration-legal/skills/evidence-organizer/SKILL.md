---
name: evidence-organizer
description: >
  Maps an exhibit inventory to visa criteria, producing a matrix with one row per
  exhibit and columns per criterion. Flags coverage gaps, redundant exhibits, and
  evidence that does not map to any criterion. Use when the attorney says "organize
  my exhibits", "map evidence to criteria", "what criteria am I missing evidence for",
  "build an exhibit map", or provides a list of documents and wants to know where they
  fit in the petition.
argument-hint: "[--visa eb1a|eb2niw|o1a|o1b] [--gaps-only] [--export]"
---

# /evidence-organizer

Takes an exhibit inventory (list of documents, letters, publications, certificates, etc.) and maps each exhibit to the criteria it supports for the specified visa type. Returns a coverage matrix, a gap analysis, and exhibit-by-exhibit notes. This is the pre-petition document triage tool — it turns a pile of files into a structured argument.

## Instructions

1. **Read the practice profile** at `~/.claude/plugins/config/claude-for-legal/immigration-legal/CLAUDE.md`. Extract: visa type in scope, evidence standards, exhibit numbering convention.

2. **Load the appropriate reference file** from the merit-evaluation skill directory:
   - EB-1A → `../merit-evaluation/eb1a-criteria.md`
   - EB-2 NIW → `../merit-evaluation/eb2niw-prongs.md`
   - O-1A or O-1B → `../merit-evaluation/o1-criteria.md`

3. **Collect the exhibit inventory.** If not provided, ask. Accept:
   - A list of document descriptions ("Google Scholar profile showing 450 citations across 12 papers", "Award certificate from IEEE Best Paper Award 2023", etc.)
   - File paths to actual documents — read them to assess their content
   - A prior merit-evaluation output from `/immigration-legal:merit-evaluation` — use the evidence listed there as the inventory

4. **Map each exhibit to criteria** per the matrix below.

5. **Produce the gap analysis** — which criteria have no supporting exhibits? Which are covered by only one exhibit (fragile)? Which are over-covered (potential to cut)?

6. **Return the structured output.**

---

## Flags

`--visa` — specify visa type. If omitted, ask. Must match the intended petition.

`--gaps-only` — return only the gap analysis section, not the full matrix. Useful when the attorney knows their exhibit list is incomplete and wants to see what's missing.

`--export` — format the output as a clean table suitable for copying into a petition preparation memo or case management note.

---

## Output format

### Header

```
EVIDENCE ORGANIZER — [VISA TYPE]
Applicant: [Name]
Field: [Field]
Date: [YYYY-MM-DD]
Exhibit numbering convention: [from practice profile — e.g., Exhibit A-1, A-2…]

PRIVILEGED & CONFIDENTIAL — ATTORNEY WORK PRODUCT — PREPARED AT THE DIRECTION OF COUNSEL
```

---

### Coverage matrix — EB-1A

One row per exhibit. Columns are the 10 EB-1A criteria (abbreviated). An ✓ indicates the exhibit supports that criterion; a (✓) indicates partial or indirect support worth noting; a blank indicates no relevance to that criterion.

| Exhibit | Description | C1 Awards | C2 Memb. | C3 Press | C4 Judge | C5 Contrib. | C6 Articles | C7 Display | C8 Role | C9 Salary | C10 Comm. | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A-1 | [description] | [✓/(✓)/—] | … | … | … | … | … | … | … | … | … | [notes on fit, strength, or gaps] |
| A-2 | … | … | … | … | … | … | … | … | … | … | … | … |

*Continue for all exhibits.*

**Total exhibits:** [N]
**Criteria with GREEN coverage (2+ strong exhibits):** [list]
**Criteria with YELLOW coverage (1 exhibit or indirect support):** [list]
**Criteria with no coverage (RED gap):** [list]

---

### Coverage matrix — EB-2 NIW

| Exhibit | Description | Prong 1: Merit + Nat'l Importance | Prong 2: Well-positioned | Prong 3: Waiver justified | Proposed Endeavor | Notes |
|---|---|---|---|---|---|---|
| … | … | … | … | … | … | … |

---

### Coverage matrix — O-1A

| Exhibit | Description | O1A-1 Awards | O1A-2 Memb. | O1A-3 Press | O1A-4 Judge | O1A-5 Contrib. | O1A-6 Articles | O1A-7 Role | O1A-8 Salary | Notes |
|---|---|---|---|---|---|---|---|---|---|---|

---

### Exhibit-by-exhibit notes

For each exhibit with substantive notes (don't repeat every row — focus on non-obvious mappings, strength assessments, and actionable comments):

**[Exhibit number] — [Description]**

- **Maps to:** [Criterion/Prong(s) it supports]
- **Strength:** [Strong / Moderate / Weak / Marginal — with reasoning]
- **Issue (if any):** [e.g., "Article mentions beneficiary but is not primarily about them — C3 support is borderline per practice profile's 'direct coverage required' standard" or "Citation count (23) falls below the firm's 'highly cited' threshold of 50 per paper"]
- **Action item (if any):** [e.g., "Obtain publisher circulation/traffic data to establish 'major media' tier" or "Request supplemental expert letter addressing significance of this contribution specifically"]

---

### Gap analysis

This is the primary output for attorneys using `--gaps-only` or reviewing a partially assembled file.

#### Criteria with no supporting exhibits

For each uncovered criterion:

**[Criterion name]** — No exhibit provided.

- **What's needed:** [Specific evidence type that would satisfy this criterion, calibrated to the practice profile's evidence standards]
- **Realistic to obtain?** [Yes — common for this field / Maybe — requires outreach / Unlikely — beneficiary's profile doesn't support this criterion / Not applicable — this criterion doesn't apply to beneficiary's field]
- **Alternative:** [If the criterion is not obtainable, note whether comparable evidence might substitute (O-1 only, per firm posture) or whether the case proceeds on other criteria]

#### Criteria with thin coverage (one exhibit or indirect support)

**[Criterion name]** — Covered by [N] exhibit(s), [direct/indirect].

- **Fragility:** [Explain why one exhibit is risky — e.g., "Single press article; if USCIS challenges the outlet's 'major media' status, the criterion falls"]
- **What would strengthen:** [Specific additional evidence]

#### Over-covered criteria (potential to cut)

**[Criterion name]** — Covered by [N] exhibits.

- **Observation:** [e.g., "7 exhibits map to scholarly articles. The petition can likely be streamlined to the 4 strongest — consider whether all 7 add signal or create noise"]
- **Recommendation:** [Keep all / Prioritize — suggest which to lead with / Cut — suggest which to remove]

---

### Exhibit numbering

Apply the firm's exhibit numbering convention from the practice profile:

> **Proposed exhibit numbering for this file:**
>
> [List all exhibits in the proposed numbering order, grouped by criterion. Example:
> - Exhibit A — Awards and Recognition (Criterion 1): A-1 [name], A-2 [name]
> - Exhibit B — Published Material (Criterion 3): B-1 [name], B-2 [name]
> - etc.]

*This is a proposal for the attorney to review and adjust. The actual exhibit list is the attorney's decision.*

---

### Summary and next steps

> **File readiness:** [Ready to assemble / Missing [N] critical exhibits / Fragile on [criterion(s)] — needs strengthening]
>
> **Top 3 action items before assembly:**
> 1. [Most impactful gap to fill — specific]
> 2. [Second most impactful]
> 3. [Third — or "none: file is ready to assemble"]
>
> **Recommended next skill:** [e.g., "/immigration-legal:petition-letter-draft to begin scaffolding the petition letter" or "/immigration-legal:merit-evaluation to re-run the analysis with the updated exhibit set"]

---

## Evidence citation discipline

Every observation about an exhibit must be traceable to what the attorney provided. Do not infer what a document says if you haven't read it — ask for it. If you cannot read an exhibit (file path not accessible), note it: "Exhibit not read — attorney should verify mapping."

Apply the practice profile's evidence standards when assessing exhibit strength:
- "Highly cited" threshold: from `## Evidence standards → "Scholarly articles → minimum citation count"`
- "Major media" tier: from `## Evidence standards → "Published material about"`
- "Original contributions" bar: from `## Evidence standards → "Original contributions of major significance"`

---

## Failure modes to avoid

- **Over-mapping.** Don't assign an exhibit to a criterion just because it *could* be loosely relevant. A citation count in the CV doesn't map to "judging" — don't mark it there.
- **Under-mapping.** A single expert letter can address multiple criteria (contributions, role, salary). Map it to all relevant criteria and note which parts address which.
- **Inventing exhibits.** If an exhibit wasn't provided, note the gap — don't assume it exists.
- **Ignoring the evidence standards.** An article in a regional blog is not "major media" if the practice profile requires national trade press. Apply the firm's standards, not generic ones.
