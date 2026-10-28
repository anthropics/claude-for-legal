---
name: verify-citations
version: 0.1.0
description: >
  Use this skill whenever a user asks to verify, check or confirm legal citations, statute references, court decision signatures or quoted legal theses in a document that relies on Polish law or EU law — including drafts produced by other Claude for Legal plugins that carry `[verify]` tags on Polish or EU sources. Also use when the user asks for LEGAION or LEGAION Verifier by name.
argument-hint: "[paste the document or point to the file]"
allowed-tools:
  - mcp
---

# Verify citations against official registers

LEGAION Verifier extracts every legal claim in a document (statute unit, court decision, date, quoted thesis) and checks each one against the official register it should come from — ISAP for Polish statutes, SAOS for Polish court decisions, EUR-Lex for EU law, and national registers where a queryable source exists. A claim is only `verified` when the register actually returned the unit during this request and its text supports the claim.

## Prerequisites

The `legaion-verifier` MCP server must be connected. Call `whoami` first. If the call fails or the server is not listed, tell the user the LEGAION Verifier connector needs to be connected and signed in (a LEGAION account is required; a free trial is available at https://www.legaion.com) — then stop. Do not attempt to verify citations from model knowledge as a substitute.

## Gate: what this skill will not do

These are hard limits, stated before the workflow so they are not skipped:

- **Never upgrade a verdict.** If the server says `unverified`, `fabricated` or `unknown`, report exactly that. Do not "confirm" a citation from memory, from training data or from a different source to make the result look cleaner.
- **Never treat `unavailable` as a pass.** `unitCheck.status: "unavailable"` means the register did not answer. The claim was not checked. Say so.
- **Do not judge relevance or legal merit.** The server checks existence, form and content match. Whether the citation supports the argument is the reviewing lawyer's call.
- **No legal advice.** Output is a draft for the professional who signs the document.

## Workflow

### 1. Get the document

- Use the full text the user pasted or the file they pointed to. Send the whole document, not a summary — `spanOffset` positions refer to the exact text sent.
- If the document is long and mixes jurisdictions, keep it whole; the server routes each claim to its register.
- Ask for the document type only if it is not obvious (e.g. `pismo procesowe`, `umowa`, `opinia prawna`, `regulamin`).

### 2. Run the verification

Call `verifier_engine` with:
- `documentContent` (required): the full text.
- `documentType` (optional): as above.
- `outputLanguage`: the user's language (`en` or `pl`).
- `caseId` (optional): only if the user explicitly asks to attach the result to a LEGAION case. Never pass a case id the user did not give or confirm.

### 3. Report the result

Lead with the decision, then the detail:

1. **Publication gate** — `publicationGate.decision` (`APPROVED` / `MANUAL_REVIEW` / `BLOCKED`) and the score, with one line on what drove it (`scoreBreakdown.reasons`). Present it as advice for the reviewer, not an action taken.
2. **Counts** — `verdictCounts`: verified / unverified / fabricated / unknown.
3. **Every claim that is not `verified` first**, one row each:
   - the claim as cited (`legalBasis`), and where it sits in the document (paragraph from `spanOffset`)
   - verdict
   - what the register said, from `unitCheck.status` and `unitCheck.note` — distinguish "the register said no" from "the register did not answer"
   - register URL if present
4. **Verified claims**, compactly: citation, register, `sourceUrl`, `fetchedAt`.
5. **Audit line** — that verification used two independent stages (`dualModelVerification`) and that the request and stage outputs are hashed (`auditTrace`), so the result can be tied to this exact input later. Do not print the hashes unless the user asks.

Tag provenance on the load-bearing item, not the paragraph: every verified citation carries `[LEGAION · <register> · fetched <fetchedAt>]`; every non-verified one carries `[not verified — <reason>]`.

### 4. Hand back

- If other plugins in the session produced the draft, point to the specific `[verify]` items this run resolved and the ones it could not.
- Suggest re-running later for claims where the register was unavailable — registers are occasionally down, and the server does not guess.
- Never quote client document content back into support channels or issues.

## Known limitations to state when relevant

- A court decision cited with a correct signature but a wrong date comes back `unverified`; the discrepancy is visible in the citation quote, not as a separate flag.
- `fabricated` is rare: it requires the register to confirm absence. Most problems surface as `unverified`.
- Coverage outside Poland and the EU depends on whether a queryable national register exists; otherwise the verdict is `unknown` with an explanation.

## Helpful information

- Documentation and output format: https://github.com/legaion/mcp-verifier
- Support: office@aidvocates.com
- Provider: LEGAION — Aidvocates, Inc.
- Privacy: https://www.legaion.com/privacy
