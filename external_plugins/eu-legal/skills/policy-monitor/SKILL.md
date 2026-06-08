---
name: policy-monitor
description: >
  Detect drift between your privacy policy commitments and actual practice.
  Two modes: (1) query — check whether a specific new practice is covered by
  the current policy; (2) sweep — review recent privacy activities for policy
  drift. Use when asking "does our policy cover this", "we want to start doing
  X — does the policy need updating", or "run the policy monitor".
argument-hint: "[describe new practice, or 'sweep' for a full review]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:policy-monitor

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If placeholders, stop: "Run `/eu-legal:cold-start-interview` first."
2. Load `~/.claude/plugins/config/eu-legal/privacy.md` for privacy policy commitments. If missing, note: "Run `/eu-legal:privacy-cold-start` to record your privacy policy commitments."
3. Determine mode: query (specific new practice) or sweep (general drift check).
4. **Input gate (Mode 1):** If no processing activity is described, ask: "What new practice or processing activity do you want to check?" Before running Mode 1, confirm you have at minimum: (a) the purpose, (b) the data categories involved, (c) who the data subjects are. If these are not provided, ask before proceeding.
5. **Input gate (Mode 2):** Sweep requires the user to provide a list of recent processing activities. Ask: "What privacy-relevant activities have started or changed in the last 90 days?" Do not infer activities from context — require an explicit list before running the sweep.
6. Run the workflow below.

---

## Purpose

Privacy policies are legal commitments under GDPR Art. 13/14 (transparency obligations). If practice diverges from policy without updating the policy, the controller is in breach. This skill finds that gap.

**Audience:** DPOs, privacy counsel, or compliance officers with visibility into the entity's processing activities. Mode 2 sweep requires the user to provide the list of activities — this skill does not discover them autonomously.

**Important:** A "Covered" verdict does not guarantee regulatory compliance. It means the described practice appears consistent with the current policy commitments on file. Have your DPO or privacy counsel confirm before relying on the verdict.

## Mode 1: Query — specific new practice

The user describes something new they want to start doing.

Step 1: Identify what GDPR Art. 13/14 would require in the privacy notice for this processing (purposes, legal basis, recipients, transfers, retention, rights).

Step 2: Compare against the privacy policy commitments in privacy.md. Does the policy already cover this? Specifically:
- Is the purpose disclosed?
- Is the legal basis stated?
- Are any new recipients or categories of recipients disclosed?
- Are new transfer destinations covered (adequacy / SCC)?
- Is the retention period consistent with what's stated?

Step 3: Verdict and next action (output all three fields):

| Verdict | Meaning | Required next action |
|---|---|---|
| **Covered** | Practice appears consistent with current policy | Document the check; confirm with DPO before proceeding |
| **Gap** | Policy needs updating before this practice begins | Draft additional policy language; get attorney/DPO sign-off; update policy before processing starts |
| **Major gap** | Significant new processing category not covered | Stop — full policy review required; run `/eu-legal:pia-generation` if DPIA trigger may be met; route to DPO or outside counsel |

Step 4: If a DPIA trigger may be present (large-scale, special categories, automated decisions affecting individuals), add: "This activity may also trigger a mandatory DPIA — run `/eu-legal:privacy-triage` to assess."

## Mode 2: Sweep

Review the last significant privacy activities (from context or by asking the user) for drift.

For each activity: was the privacy notice updated? Is the processing documented in a record of processing activities (RoPA)? Is the legal basis still valid (particularly for consent-based processing: was consent obtained; can users withdraw)?

For each activity in the provided list: was the privacy notice updated? Is the processing documented in a record of processing activities (RoPA)? Is the legal basis still valid?

**Output format for Mode 2 sweep:**

| Processing activity | Policy coverage | RoPA documented | Legal basis valid | Action required |
|---|---|---|---|---|
| [each activity] | Covered / Gap / Major gap | Yes / No / Unknown | Yes / No / Review | [specific action] |

**GDPR Art. 30 RoPA obligation** `[model knowledge — verify with supervisory authority guidance]`: Required for all organisations UNLESS all of these apply: (a) fewer than 250 employees, AND (b) processing is occasional (not systematic/regular), AND (c) no special category data (Art. 9) or criminal data (Art. 10), AND (d) unlikely to result in risk to data subjects. If ANY exception fails, RoPA is required regardless of headcount.

---

## What this skill does NOT do

- **Does not update your privacy policy**: Identifies gaps and can draft language — does not publish or apply changes.
- **Does not conduct a DPIA**: Identifies when one may be needed; route to `/eu-legal:privacy-triage` and `/eu-legal:pia-generation`.
- **Does not cover ePrivacy / cookies**: Cookie consent and tracking are outside this skill's scope.
- **Does not audit your RoPA**: Checks whether a RoPA is required, not whether your current RoPA is accurate or complete.
- **Does not replace DPO review**: A "Covered" verdict is a preliminary check, not a compliance sign-off.

---

## Guardrail

This analysis is not legal advice. A "Covered" verdict does not guarantee regulatory compliance — it means the practice appears consistent with your policy commitments on file. Identified gaps require DPO and attorney review before the new processing begins. Publishing an inaccurate privacy notice violates GDPR Art. 13/14; supervisory authorities regularly fine for transparency failures. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
