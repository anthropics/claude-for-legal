---
name: contract-risk-xray
version: 0.1.0
description: >
  Use this skill when a user asks for a risk audit of a contract, terms of service, regulamin or consumer template governed by Polish law, or asks whether clauses could be abusive (klauzule abuzywne) under Polish consumer law and the UOKiK register. Also use when the user asks for LEGAION Deep X-Ray by name.
argument-hint: "[paste the contract or point to the file] [--abusive-clauses]"
allowed-tools:
  - mcp
---

# Contract risk X-ray

Runs the LEGAION `deep_xray` audit on a contract, terms of service or consumer template. Returns risks by level (critical / high / medium / low), clause-by-clause status, recommendations and a numeric score. In `klauzule_abuzywne` mode it also matches clauses against the Polish UOKiK register of abusive clauses, with entry number, URL and fetch timestamp.

## Prerequisites

The `legaion-verifier` MCP server must be connected. Call `whoami` first; if it fails, tell the user the LEGAION Verifier connector needs to be connected and signed in, then stop.

## Gate

- **A UOKiK match is only confirmed if the server fetched the register entry.** If the status is `unconfirmed`, report it as unconfirmed — do not present it as a register match.
- **The score is a triage aid, not a legal conclusion.** Present risks as items for the reviewing lawyer, with the reasoning the server returned.
- **No legal advice and no redrafting from this skill.** If the user wants redlines, hand the flagged clauses to the reviewing lawyer or to the drafting skill they use — and say that the redraft has not been verified by LEGAION.

## Workflow

1. **Get the full document text.** Ask for the kind only if unclear: `umowa` (contract, default), `regulamin` (terms of service), `wzorzec konsumencki` (consumer template).
2. **Choose the mode.**
   - `standard` — full risk audit.
   - `klauzule_abuzywne` — audit plus UOKiK register check. Use it by default for consumer-facing documents (`regulamin`, `wzorzec konsumencki`) or when the user mentions consumers or abusive clauses.
3. **Call `deep_xray`** with `documentContent`, `documentType`, `analysisMode` and `outputLanguage` (the user's language).
4. **Report**, most severe first:
   - overall score and the count of risks per level;
   - each critical and high risk: the clause (quote the minimum needed), why it was flagged, the recommendation;
   - in `klauzule_abuzywne` mode: each register match with entry number, URL and `fetchedAt`, and its status (confirmed / unconfirmed);
   - medium and low risks as a compact list.
5. **Offer the follow-up:** if the document also cites statutes or case law, offer `/legaion-verifier:verify-citations` on the same text.

## Helpful information

- Documentation: https://github.com/legaion/mcp-verifier
- Support: office@aidvocates.com
- Provider: LEGAION — Aidvocates, Inc.
