---
name: client-update
description: >
  Routine client correspondence in plain language — case filed, RFE received, RFE
  response submitted, approval notice received, denial, interview scheduled. Not
  substantive legal advice; updates only. Use when the attorney says "draft a client
  update", "send the RFE notice to the client", "write up the approval for the
  client", or needs to communicate a case event to the applicant in plain English.
argument-hint: "[--event filed|rfe-received|rfe-submitted|approved|denied|interview] [--tone formal|warm]"
---

# /client-update

*Phase 3 skill — full implementation coming in the next build cycle.*

Routine client correspondence for standard immigration case events. Plain language, required elements per the event type, and attorney-review routing before sending. Mirrors `legal-clinic:client-letter` — this skill drafts the update; the attorney reviews and sends.

**Supported event types:**

- **filed** — "Your petition has been filed. Here is what happens next."
- **rfe-received** — "USCIS has requested additional evidence. Here is what that means and what we need from you."
- **rfe-submitted** — "We have responded to USCIS's request. Here is what to expect."
- **approved** — "Your petition has been approved. Here are your next steps." (Distinguish I-140 approval from visa issuance; distinguish O-1 approval from work authorization start.)
- **denied** — "USCIS has denied your petition. Here are your options." (Flags appeal / MTR / refile paths — no substantive legal advice on which to choose.)
- **interview** — "You have been scheduled for an interview. Here is how to prepare."

**What this skill does not do:**
- Give substantive legal advice about strategy in the update — that goes in a separate call or memo
- Send the email — it drafts it for attorney review and sends
- Substitute for attorney review before the update goes out

**Dependencies:** Reads the practice profile for house style (tone preference). Reads the active matter for client name, visa type, and case history. Uses the matter `history.md` to log the correspondence event.

**Format:** Plain language. Short sentences. No legal jargon without immediate explanation. Signed by the attorney of record. Does NOT include the work-product header — this is client-facing correspondence, not attorney work product.

---

*To use now: tell me the event type and the client name, and I will draft the update manually. This stub will be replaced with a structured workflow in the next release.*
