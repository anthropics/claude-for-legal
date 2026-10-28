# LEGAION Verifier

LEGAION Verifier checks the legal citations in a document against the official registers they should come from, and records which register was queried, at what address, and at what time. It covers Polish law (ISAP for statutes, SAOS for court decisions), EU law (EUR-Lex), and national registers of other jurisdictions where a queryable source exists.

The design rule: **no citation is marked verified unless the register answered.** A register that is down, or a citation the register does not know, comes back `unverified` or `unknown` — never a green light. This fills the gap the Claude for Legal plugins leave open for Polish and EU primary sources, where the U.S. research connectors do not reach.

- Verify every statute article, court decision signature and quoted thesis in a draft before it is signed, filed or sent.
- Get a per-claim verdict (`verified` / `unverified` / `fabricated` / `unknown`) with the register URL, the register text and the `fetchedAt` timestamp, so a reviewer can repeat the check.
- Get a publication gate (`APPROVED` / `MANUAL_REVIEW` / `BLOCKED`) computed deterministically from the verdicts, plus SHA-256 hashes of the request and both verification stages for the audit file.
- Run a contract or consumer-terms risk audit, optionally matched against the Polish UOKiK register of abusive clauses.

Requires a LEGAION account (a free trial is available at https://www.legaion.com). Authentication is OAuth 2.1 with dynamic client registration — no API key; you sign in once in the browser window the client opens.

## Skills

| Skill | Command | What it does |
|---|---|---|
| Verify citations | `/legaion-verifier:verify-citations` | Runs `verifier_engine` on a document and reports each citation with its verdict and source. |
| Contract risk X-ray | `/legaion-verifier:contract-risk-xray` | Runs `deep_xray` on a contract, terms of service or consumer template; optional UOKiK abusive-clause register check. |

## Example use cases

1. "Check every citation in this draft pleading against ISAP and SAOS before I file it."
2. "This vendor agreement cites EU and Polish law — verify each reference and tell me what the register says."
3. "Audit our consumer terms for abusive clauses against the UOKiK register."
4. "The privacy notice quotes GDPR articles — confirm the quotes match EUR-Lex."

## When to use

- A document cites Polish statutes, Polish court decisions, or EU law, and someone is about to rely on it.
- A model-drafted text (from any plugin in this marketplace) contains citations to Polish or EU sources that are tagged `[verify]`.
- Contracts, terms of service and consumer templates governed by Polish law need a risk audit.

## When not to use

- U.S. federal or state law — use CourtListener, Trellis, Descrybe or CoCounsel Legal.
- Judging whether a citation is *relevant* to the argument — the server checks existence, form and content match, not legal strategy.
- Drafting, summarising or rewriting documents.
- Legal advice. Every output is a draft for review by the professional who signs the document.

## Tools exposed by the server

All tools are read-only (`readOnlyHint: true`).

| Tool | Purpose |
|---|---|
| `verifier_engine` | Verify citations and claims in a document. Returns claims with verdicts, sources (register URL + `fetchedAt`), overall verdict, publication gate and audit hashes. |
| `deep_xray` | Risk audit of a contract, terms of service or consumer template. Mode `klauzule_abuzywne` adds UOKiK register matches. |
| `list_cases`, `list_clients` | The signed-in user's LEGAION cases and clients (platform plan). |
| `whoami` | Confirms the connection and the signed-in account. |

## Data handling

- The server runs under the signed-in user's row-level permissions.
- Document content sent to `verifier_engine` or `deep_xray` is processed for the request and is not stored. If a `caseId` is passed, only the verification result is attached to that LEGAION case — not the document text.
- Registers are queried live; `fetchedAt` is the time of that query.
- Privacy: https://www.legaion.com/privacy

## Links

- **Documentation, tool schemas and output format:** https://github.com/legaion/mcp-verifier
- **Official MCP Registry:** `com.legaion/verifier`
- **Support:** office@aidvocates.com
- **Provider:** LEGAION — Aidvocates, Inc.
