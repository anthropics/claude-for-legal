---
name: petition-letter-draft
description: >
  IRAC-style scaffold for a petition letter — one section per criterion or prong,
  with rule (cited to USCIS Policy Manual), evidence inventory, attorney-analysis
  prompts, and a blank conclusion. The scaffold, not the final letter. Use when the
  attorney says "draft the petition letter", "scaffold the I-140 letter", "start the
  O-1 support letter", or is ready to begin drafting after completing merit evaluation
  and evidence organization.
argument-hint: "[--visa eb1a|eb2niw|o1a|o1b] [--criteria 1,3,5,8] [--section <criterion name> for a single section]"
---

# /petition-letter-draft

*Phase 2 skill — full implementation coming in the next build cycle.*

IRAC-structured scaffold for the petition support letter (I-140 petition letter for EB categories; support letter for O-1 petitions). Each criterion or prong gets its own section with the legal rule stated and cited, an evidence inventory pulled from `/immigration-legal:evidence-organizer`, attorney-analysis prompts (in `[ATTORNEY ANALYSIS: ...]` brackets), and a blank conclusion for the attorney to complete.

Uses the same RESEARCH NEEDED / ATTORNEY ANALYSIS pattern as `legal-clinic:memo` — the skill does not write the legal argument; it structures the document so the attorney can write it efficiently.

**What this skill produces:**
- A structured petition letter scaffold in the firm's house style (tone, exhibit numbering, criterion heading format — all from the practice profile)
- For each criterion/prong: (1) Rule — regulatory text + Policy Manual citation, (2) Evidence inventory — mapped from the evidence-organizer output, (3) `[ATTORNEY ANALYSIS: ...]` prompts for the argument, (4) Conclusion — blank for attorney to complete
- Exhibit reference list at the end

**What this skill does not do:**
- Write the legal argument — that requires attorney judgment and knowledge of the specific client's evidence
- Substitute for attorney review before filing
- Generate expert letters — those are drafted separately by the attorneys working with the experts

**Dependencies:** Reads the practice profile for house style. Reads the active matter file for client details, visa type, criterion selection, and evidence inventory. Works best when run after both `/immigration-legal:merit-evaluation` and `/immigration-legal:evidence-organizer`.

**Format:** Uses the firm's criterion heading style, exhibit numbering convention, and tone preference from the practice profile. Work-product header prepended per practice profile `## Outputs`.

---

*To use now: provide the visa type, client name, and the evidence you want to argue for each criterion, and I will produce a structured scaffold manually. This stub will be replaced with a full automated scaffold workflow in the next release.*
