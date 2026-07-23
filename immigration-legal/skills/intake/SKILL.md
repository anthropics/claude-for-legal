---
name: intake
description: >
  Structured new-client intake interview — cross-visa triage, conflict flags, and
  a formatted case summary for the attorney to review. Use when the attorney says
  "new client intake", "run intake for [name]", "triage this applicant", or wants
  to assess a prospective client's fit before engaging. Does not decide case
  acceptance — that is the attorney's call.
argument-hint: "[--quick for abbreviated triage only] [--visa eb1a|eb2niw|o1a to pre-select visa type]"
---

# /intake

*Phase 2 skill — full implementation coming in the next build cycle.*

Structured intake interview for a new immigration client. Collects career profile, evidence inventory, and target visa, then runs a preliminary cross-visa triage (EB-1A vs. EB-2 NIW vs. O-1) to help the attorney prioritize. Flags potential conflicts, prior denial history, and any complications that affect strategy before engagement.

**What this skill produces:**
- A structured case summary formatted for the attorney's file (writes to the client matter folder if `/immigration-legal:matter-workspace new` has been run first)
- A preliminary triage: which visa type(s) appear most viable, and why — including a recommended order of pursuit and any visa types to rule out
- A conflict flag if the client or counterparty matches an existing active matter
- An evidence gap summary: what the client says they have vs. what they would need for the recommended visa

**What this skill does not do:**
- Decide whether to take the case — that is always the attorney's call
- Run a full merit evaluation — use `/immigration-legal:merit-evaluation` for that
- Guarantee visa eligibility

**Dependencies:** Reads the practice profile for visa types in scope, risk posture, and escalation rules. Reads the active matter (if set) to write the case summary to the right folder.

**Recommended next skill after intake:**
- `/immigration-legal:merit-evaluation` — full criterion analysis with the evidence inventory from intake
- `/immigration-legal:strategy-memo` — recommendation memo on visa selection and evidence development strategy

---

*To use now: describe the prospective client's profile (field, career stage, rough evidence) and I will run a preliminary triage manually using the merit-evaluation skill. This stub will be replaced with a structured intake workflow in the next release.*
