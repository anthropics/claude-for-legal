# Immigration Practice Profile

*Written by the cold-start interview on [DATE]. Edit this file directly — every
skill in this plugin reads it before doing anything. If something below is wrong,
fix it here and it's fixed everywhere.*

*To re-run the interview: `/immigration-legal:cold-start-interview --redo`*
*To check integrations: `/immigration-legal:cold-start-interview --check-integrations`*
*To edit one thing: `/immigration-legal:customize`*

---

## Who we are

**Firm name:** [PLACEHOLDER]
**Practice setting:** [solo / small firm / midsize firm / large firm / in-house]
**Primary USCIS service centers:** [e.g., Nebraska SC, Texas SC, California SC]
**Attorneys using this plugin:** [names/roles — e.g., "Jane Smith (partner), Tom Lee (associate)"]

**Practice mix (approximate % of caseload):**
- EB-1A (Alien of Extraordinary Ability): [PLACEHOLDER]%
- EB-2 NIW (National Interest Waiver): [PLACEHOLDER]%
- O-1A/B (Extraordinary Ability/Achievement): [PLACEHOLDER]%
- Other (EB-1B, PERM, H-1B, L-1, etc.): [PLACEHOLDER]%

**The thing that drives most of your work:** [PLACEHOLDER — e.g., "STEM academics and researchers referred from university OIS offices"]

---

## Who's using this

**Role:** [Partner attorney / Associate attorney / Paralegal under attorney supervision / Other]
**Supervising attorney (if not partner):** [Name / N/A]

---

## Available integrations

| Integration | Status | Fallback if unavailable |
|---|---|---|
| Case management (Clio, MyCase, INSZoom, etc.) | [✓ / ✗] | Manual case tracking; matter-workspace logs history locally |
| Document storage (Drive, SharePoint, Box, Dropbox) | [✓ / ✗] | User uploads documents directly for each skill run |
| Meritocrat (app.meritocrat.us) | [✓ / ✗] | Attorney works from documents pasted into conversation |
| Slack | [✓ / ✗] | Client updates and alerts delivered inline |

*Re-check: `/immigration-legal:cold-start-interview --check-integrations`*

---

## Risk posture

*Drives how merit-evaluation reads evidence. Aggressive = lend benefit of the doubt on borderline criteria. Standard = apply USCIS Policy Manual guidance as written. Conservative = require clear, unambiguous evidence before calling a criterion met.*

| Visa type | Posture | Notes |
|---|---|---|
| EB-1A | [aggressive / standard / conservative] | [PLACEHOLDER] |
| EB-2 NIW | [aggressive / standard / conservative] | [PLACEHOLDER] |
| O-1A | [aggressive / standard / conservative] | [PLACEHOLDER] |
| O-1B | [aggressive / standard / conservative] | [PLACEHOLDER] |

**Default posture for unlisted visa types:** [standard]

---

## Evidence standards

*These thresholds feed merit-evaluation's GREEN/YELLOW/RED calls. Adjust to match your firm's filing practice.*

**"Scholarly articles" (EB-1A criterion 6 / NIW):**
- Minimum publication count to claim "extensive": [PLACEHOLDER — e.g., 10]
- Minimum citation count to claim "highly cited": [PLACEHOLDER — e.g., 50 per paper OR 200 total]
- Accepted sources: [e.g., peer-reviewed journals only / peer-reviewed + conference proceedings / any scholarly venue]

**"Published material about" (EB-1A criterion 3 / O-1):**
- Minimum media tier: [e.g., national trade press or above / any credible press / any mention]
- Direct coverage required (not incidental mentions): [yes / no]
- Self-authored content counts: [never / only if republished by third party / yes]

**"Original contributions of major significance" (EB-1A criterion 5 / NIW prong 1):**
- Must show real-world adoption or impact: [required / preferred / not required]
- Citation count alone is sufficient: [yes / no — if no, what else is required]
- Must distinguish from ordinary professional contributions: [yes / no]

**"High salary" (EB-1A criterion 8):**
- Benchmark source: [e.g., BLS OES, Glassdoor, employer data, survey evidence]
- Minimum percentile threshold: [e.g., top 10% in field and geography]

**O-1 comparable evidence:**
- Willing to use: [yes — freely / yes — with justification memo / reluctant — only when no standard criteria available / never]
- Notes: [PLACEHOLDER]

---

## House style

**Petition letter tone:** [formal / conversational / depends on adjudicator — note any conventions]
**Exhibit numbering:** [e.g., "Exhibit A-1, A-2…" / "Tab 1, Tab 2…" / client-specific]
**Declaration format:** [e.g., first-person signed declaration / third-person expert letter / both depending on witness]
**Expert letter template:** [path to template if one exists / none — skill generates from scratch]
**Criterion heading style:** [e.g., "CRITERION 1: AWARDS" / "I. Awards of Excellence" / firm's standard]
**Pagination convention:** [e.g., "Page X of Y" in footer / none]
**Work-product header:** PRIVILEGED & CONFIDENTIAL — ATTORNEY WORK PRODUCT — PREPARED AT THE DIRECTION OF COUNSEL

---

## Escalation rules

| Decision | Who decides | Notes |
|---|---|---|
| Merit evaluation (GREEN/YELLOW) | [Associate / Partner / Anyone] | [PLACEHOLDER] |
| Merit evaluation (borderline — YELLOW/RED) | [PLACEHOLDER] | [PLACEHOLDER] |
| Visa type selection (EB-1A vs. NIW) | [PLACEHOLDER] | [PLACEHOLDER] |
| RFE response strategy | [PLACEHOLDER] | [PLACEHOLDER] |
| Decision to file despite weak criterion count | [PLACEHOLDER] | [PLACEHOLDER] |
| Client engagement / fee agreement | [PLACEHOLDER] | [PLACEHOLDER] |

**Second-reviewer required before filing:** [always / when criterion count is below X / only for complex matters / never]

---

## Cross-plugin handoffs

- **Entity formation or corporate structure questions** → flag to corporate counsel
- **Non-compete / restrictive covenant questions tied to employment** → flag to employment-legal plugin
- **Tax questions related to foreign national employment** → flag to tax counsel
- **Consular processing questions (DS-260, visa stamping)** → [note if in-scope or out-of-scope for this firm]
- **Removal / deportation defense** → [in-scope or out-of-scope]

---

## Matter workspaces

**Enabled:** [✓ / ✗]
*Enable for firms with multiple active clients. Disable for single-client or in-house use.*

**Active matter:** none — practice-level context only

**Storage root:** `~/.claude/plugins/config/claude-for-legal/immigration-legal/matters/`

**Cross-matter context:** off
*When off, skills working in matter A never read files from matter B.*

---

## Visa types in scope

| Visa | Status | Notes |
|---|---|---|
| EB-1A | active | Full merit-evaluation, evidence-organizer, petition-letter-draft, RFE response |
| EB-2 NIW | active | Full merit-evaluation, evidence-organizer, petition-letter-draft, RFE response |
| O-1A | active | Full merit-evaluation, evidence-organizer, petition-letter-draft, RFE response |
| O-1B | active | Full merit-evaluation with arts/entertainment criteria |
| EB-1B | planned | Outstanding professor/researcher — criteria reference loaded, skill stubs present |
| EB-2 PERM | planned | Labor certification track — out of scope for merit-evaluation |
| H-1B | planned | Specialty occupation — out of scope for merit-evaluation |
| L-1 | planned | Intracompany transferee — out of scope for merit-evaluation |

---

## Seed documents reviewed

| Document | Type | Date reviewed | Notes |
|---|---|---|---|
| [PLACEHOLDER] | [petition letter / RFE response / approval notice] | [date] | [what you learned from it] |

*Add more rows as you share documents with `/immigration-legal:cold-start-interview`.*

---

*To re-run the interview: `/immigration-legal:cold-start-interview --redo`*
*To edit one section: `/immigration-legal:customize`*
*To check integrations: `/immigration-legal:cold-start-interview --check-integrations`*
