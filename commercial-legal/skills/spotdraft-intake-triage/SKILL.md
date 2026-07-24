---
name: spotdraft-intake-triage
description: >
  Fetch pending legal intake requests from SpotDraft, classify by type and urgency,
  and route each to the appropriate commercial-legal skill or escalation path. Use
  when the user asks to triage SpotDraft intakes or clear the legal intake queue.
argument-hint: "[optional intake ID to triage one request]"
---

# /spotdraft-intake-triage

Classifies pending SpotDraft legal intakes and recommends the right commercial-legal skill — does not complete the review.

## Instructions

1. **Confirm SpotDraft is connected** via MCP (same failure bounce as other SpotDraft skills).

2. **Fetch intakes.** Call `get_legal_intakes` for pending items. For each (or a single ID if provided), call `get_legal_intake_by_id` for type, requester, documents, and notes.

3. **Classify each intake:**
   - **Type:** NDA / Vendor MSA / SaaS subscription / Other (from intake metadata and attachments)
   - **Urgency:** RED (requested sign-by date within 7 days or hard deadline stated) / YELLOW (no hard deadline) / GREEN (exploratory, no deadline)

4. **Recommend routing** — do not run the review skill automatically:

   | Type | Route to |
   |---|---|
   | NDA | `/commercial-legal:review` (NDA triage) |
   | Vendor MSA | `/commercial-legal:review` (vendor-agreement-review) |
   | SaaS MSA | `/commercial-legal:review` (saas-msa-review overlay) |
   | Other / unclear | `/commercial-legal:escalation-flagger` with reason |

5. **Output one block per intake** using the format below. Tag `[SpotDraft CLM]` on intake IDs and factual claims.

## Examples

```
/commercial-legal:spotdraft-intake-triage
```

```
/commercial-legal:spotdraft-intake-triage intake-12345
```

---

## Purpose

Fetch pending legal intake requests from SpotDraft, classify them by type and urgency, and route each to the most appropriate `commercial-legal` skill or escalation path. The reviewing lawyer picks up from the recommended skill.

## Auth

OAuth — intakes are scoped to what the authorized user can see in SpotDraft.

## MCP tools (read-only)

| Tool | What it fetches |
|---|---|
| `get_legal_intakes` | List of pending intakes |
| `get_legal_intake_by_id` | Intake detail: type, requester, documents, notes |

## Output format (per intake)

```
## Intake [ID]: [Name/Title]

Requester: [name / team]
Type detected: [NDA / Vendor MSA / SaaS subscription / Other]
Urgency: [RED — requested sign-by <date> / YELLOW — no hard deadline / GREEN — exploratory]

Recommended routing:
- If NDA: → /commercial-legal:review (NDA triage, self-serve if GREEN-eligible)
- If Vendor MSA: → /commercial-legal:review (vendor-agreement-review)
- If SaaS MSA: → /commercial-legal:review (saas-msa-review overlay)
- If Other: → /commercial-legal:escalation-flagger [reason]

[SpotDraft CLM — intake ID: XXX]
```

This skill does not complete the review and performs no write operations.
