---
name: strategy-memo
description: >
  Internal attorney strategy memo: which visa to pursue, which criteria to lead
  with, what evidence to develop before filing, and a timeline. Use when the
  attorney says "draft a strategy memo", "what's our filing strategy for [client]",
  "what should we build before we file", or after a merit evaluation surfaces a
  borderline result that needs a plan. Internal document only — not for the client.
argument-hint: "[--visa eb1a|eb2niw|o1a] [--timeline <months>]"
---

# /strategy-memo

*Phase 2 skill — full implementation coming in the next build cycle.*

Recommendation memo for the attorney's internal file. Takes the output of `/immigration-legal:merit-evaluation` and `/immigration-legal:evidence-organizer` and synthesizes them into a strategic recommendation document: which visa type to pursue (and why), which criteria to anchor the petition on, which criteria are arguable vs. risky, what evidence the client should develop before filing, and a realistic timeline.

**What this skill produces:**
- A privileged internal memo (not for the client) with a recommendation on visa type, criterion selection, and evidence development
- A prioritized evidence development plan: what to get, from whom, by when
- A filing timeline tied to the client's priority date goals and current status
- An escalation note if the strategy decision requires partner sign-off per the practice profile

**What this skill does not do:**
- Draft the petition letter — use `/immigration-legal:petition-letter-draft` for that
- Predict USCIS outcomes — it provides a strategy based on the law and the evidence, not a guarantee
- Replace attorney judgment on whether to file

**Dependencies:** Reads the practice profile for risk posture, escalation rules, and visa types in scope. Reads the active matter file for prior merit evaluation results. Works best when run after `/immigration-legal:merit-evaluation` — can use the criterion analysis as its primary input.

**Format:** The memo follows the firm's house style from the practice profile. Sections: Recommendation, Visa Type Rationale, Criterion Strategy, Evidence Development Plan, Timeline, Escalation Note.

---

*To use now: provide a merit evaluation result (from `/immigration-legal:merit-evaluation`) and describe your strategic question, and I will draft the strategy memo from that input. This stub will be replaced with a structured skill workflow in the next release.*
