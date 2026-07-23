---
name: rfe-response
description: >
  Analyzes a USCIS Request for Evidence (RFE), maps each RFE request to existing
  evidence and gaps, and scaffolds the response. Use when the attorney says "we got
  an RFE", "analyze this RFE", "help with the RFE response", or uploads an RFE
  notice. This skill is the post-filing counterpart to merit-evaluation.
argument-hint: "[--visa eb1a|eb2niw|o1a] [--strategy aggressive|standard|conservative]"
---

# /rfe-response

*Phase 3 skill — full implementation coming in the next build cycle.*

RFE analysis and response scaffold. Takes the RFE notice (USCIS I-797 with the RFE attached), maps each request to the evidence already on file and evidence gaps, and produces a structured response plan. The response scaffold follows the same IRAC pattern as `petition-letter-draft` — it structures the response so the attorney can write it efficiently.

**What this skill produces:**
- An RFE analysis: what USCIS is asking for, criterion by criterion or issue by issue
- An evidence mapping: for each RFE request, what evidence is already on file and what is missing
- A response scaffold: one section per RFE request with the regulatory standard, existing evidence inventory, `[ATTORNEY ANALYSIS: ...]` prompts, and a blank response section
- A strategy recommendation: whether to respond with existing evidence (reframe), seek new evidence, or (if appropriate) withdraw and refile

**What this skill does not do:**
- Write the legal argument in the response — that requires attorney judgment
- Guarantee that the response will overcome the RFE
- Draft expert letters — those are coordinated separately

**Dependencies:** Reads the practice profile for risk posture, evidence standards, and house style. Reads the active matter file for prior merit evaluation results and evidence inventory. Works best when run after `/immigration-legal:evidence-organizer` — knows what evidence the attorney has on file.

**Common RFE patterns this skill is calibrated to handle:**
- EB-1A: USCIS concedes some criteria but challenges "final merits" under *Kazarian* step 2
- EB-2 NIW: USCIS challenges Prong 3 (waiver justification) or requires more specificity in the proposed endeavor
- O-1A: USCIS challenges the significance of awards/memberships or the "major media" tier of press coverage
- All visa types: USCIS requests evidence of employment authorization, itinerary (O-1), or beneficiary identity documents

---

*To use now: paste the RFE text and describe what evidence you have on file, and I will produce an RFE analysis and response scaffold manually. This stub will be replaced with a structured workflow in the next release.*
