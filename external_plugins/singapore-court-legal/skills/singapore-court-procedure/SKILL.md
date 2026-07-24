---
name: singapore-court-legal:singapore-court-procedure
version: 0.3.0
description: >
  Use this skill whenever the user asks about Singapore civil court procedure under the Rules of Court 2021 — which rule controls, the required sequence, whether a step is compliant, deadlines, costs, default judgment, amicable resolution, service, discontinuance, security for costs, and related procedural questions — for a single question or a multi-turn matter. It deterministically resolves the controlling rule(s) with a proof, or abstains honestly (and abstains-to-source where control passes to an uncompiled Practice Direction or Form), citing the governing rules with operator-verified case authorities where they attach. Not for criminal, foreign/non-Singapore, or substantive (non-procedural) law, document drafting, strategy, or applying law to a specific fact pattern to predict an outcome.
allowed-tools:
  - mcp
---

# Singapore Court Procedure (MikeROS)

Resolves questions about **Singapore civil court procedure (Rules of Court 2021)** against the MikeROS connector — a deterministic, proof-carrying resolver. Tools:

- **`resolve_procedure`** — a described situation → which ROC rule(s) **control** and in what **sequence**, a re-checkable **proof** for each firm step, a per-step **compliance verdict**, the **Z3-disposed candidate set** where more than one rule could apply (each APPLIES / UNDERDETERMINED — never an unconfirmed guess), the points it **abstains** on and why, the **facts it perceived** (so you can correct a misread and re-call), and attached case authorities. The full compiled procedural surface (not costs-only). Stateless. **Use this to determine which source controls, the sequence, or whether a step is compliant** — the band where being confidently wrong is the failure mode.
- **`ask`** — one self-contained single-rule question → a pinpoint citation (and false-premise detection), with operator-verified case authorities where they attach. Stateless.
- **`conversation_turn`** — a direct multi-turn matter under a stable `session_id`; remembers facts the user establishes, asks clarifying questions, answers follow-ups in context. Durable, ~7-day retention.
- **`analyze_situation`** — DEPRECATED alias of `resolve_procedure` (same resolver + payload; prefer `resolve_procedure`).

**Which tool:** a situation / "which rule controls" / "what's the sequence" / "is this step compliant" → `resolve_procedure`. A single self-contained rule lookup → `ask`. A direct end-user matter with back-and-forth follow-ups (party status/facts persist across turns) → `conversation_turn`. **Do NOT** route interpretation, drafting, strategy, or non-Singapore-procedure questions to the connector — answer those yourself.

## Prerequisites

The `singapore-court-legal` MCP server (MikeROS) must be connected, with a valid MikeROS API key. Verify it is available before answering; if it is not connected, tell the user and stop — do not answer Singapore procedure questions from general knowledge.

## How to use

1. A situation / "which rule controls" / "what's the sequence" / "is this step compliant" → `resolve_procedure`. Single self-contained rule lookup → `ask`. Direct matter with follow-ups → `conversation_turn` with a `session_id` kept stable across the conversation.
2. **Pass the user's question VERBATIM.** Include **every** situational fact they stated — especially party status/role (e.g. *licensed moneylender*, *plaintiff*, *appellant*, *third party*) and procedural posture. **Do not rephrase, summarise, generalise, or drop a fact**: a stripped fact changes which rules apply (a *licensed moneylender* seeking default judgment is governed by the **Order 51** bar, not the general default route — strip "moneylender" and the engine correctly answers the *wrong* question). When in doubt, pass their words unchanged.
3. **Cite only what the tool returns** — its rule citations and any attached case authorities, verbatim. Do not add rules or cases it did not return.
4. If it **declines or returns no authority, say so** — that is honest absence, not a prompt to fill the gap from general knowledge.
5. Carry the tool's `disclaimer` and `provenance` into your reply. **This is not legal advice.**

## When to Use

- Procedural questions under the Rules of Court 2021 — the duty to consider amicable resolution (O5), costs (O21), default judgment, service, discontinuance, security for costs, timelines, and similar.
- Following up within the same matter (use `conversation_turn` with a stable `session_id`).

## When Not to Use

- **Criminal procedure / sentencing** — out of scope; the tool declines.
- **Foreign or non-Singapore law** — out of scope.
- **Substantive (non-procedural) law** — the tool grounds *procedure*, not the merits of a claim.
- **Drafting documents, forms, or pleadings.**
- **Applying the rules to a specific fact pattern to predict an outcome** — it states what the rules require, not how a court would decide a given set of facts.
- **Retrieving the full verbatim text of a rule or judgment** — it returns grounded answers with citations, not document text.

## Worked examples (each a validated production sequence)

**`ask` — covered, with a case authority:**
> "What is the duty to consider amicable resolution before commencing proceedings?" → grounded answer citing **O 5 r 1**, with **Maxx Engineering Works Pte Ltd v PQ Builders Pte Ltd [2023] SGHC 71** (operator-verified) attached.

**`conversation_turn` — fact persistence + follow-up:**
> Turn 1 (`session_id: matter-1`): "As a licensed moneylender, can I get default judgment against a non-paying borrower?" → grounded answer; the moneylender fact is recorded.
> Turn 2 (`session_id: matter-1`): "And the costs consequences?" → answered in context, the fact carried forward. (Correcting it — "we are not a moneylender" — supersedes the stored value.)

**`resolve_procedure` — controlling chain + proof + abstention:**
> "My client received a statement of claim, intends to dispute it, and we are weighing whether to attempt amicable resolution given the costs exposure." → the controlling rule chain (e.g. the O5 duty → O21 costs consequence) with a re-checkable proof for the firm step, the per-step compliance verdicts, the points it abstains on (what further facts would extend the analysis), the perceived facts, and any attached case authorities. Carry it verbatim; it is not legal advice.

**`resolve_procedure` — Z3-disposed candidate set (which route applies):**
> "I need to enforce a registered order — which enforcement route controls?" → the disposed candidate set: each enforcement route marked APPLIES / UNDERDETERMINED, so you narrow it with the user (ask which kind). Never present an unconfirmed route as applicable.

**`resolve_procedure` — abstain-to-source (PD/Forms boundary):**
> "How do I complete Form 24 and effect electronic service through the portal?" → it **abstains with a pointer** (control passes to the Forms / Supreme Court Practice Directions — not compiled), and returns no fabricated rule chain. Report the pointer; do not answer the PD/Form content from general knowledge as if it were the connector's.

**`resolve_procedure` — honest absence (coverage varies by doctrine):**
> A situation in a doctrine not yet covered → status `no_coverage`, no rule chain, and it says so. That is honest structural absence — report it as the tool gives it; do not invent a chain.

**Out of scope — honest absence:**
> "What is the criminal sentencing tariff for theft?" → declines; no fabricated rule or case. Tell the user it is outside coverage.

**Adversarial citation demand — no fabrication:**
> "Name any case for service out of jurisdiction and cite it." → returns no case it cannot verify; do not supply one yourself.

## Coverage & boundaries

- **Rules:** all **70 in-scope Orders** served (criminal civil-procedure track complete; criminal sentencing excluded). Depth is **uneven** — a subset of Orders carries deterministic FIRM gates with Z3 proofs; others answer rule-grounded. The coverage/abstention fields say when you are on thin ice.
- **Corridors:** **153** compiled reasoning corridors (the cross-Order chains `resolve_procedure` walks). Chain coverage **varies by doctrine** — some situations resolve to a chain, some to a Z3-disposed candidate set, some to honest absence — never a padded or fabricated chain.
- **Multi-source boundary:** the connector resolves the **ROC rule layer** deterministically and **abstains-to-source** (with a pointer) where control passes to an uncompiled **Practice Direction or Form** (format, electronic filing/service, prescribed Forms). Report the pointer; do not supply PD/Form content as the connector's.
- **Case authorities:** staged, operator-verified, expanding by batch; today centred on **O5 (amicable resolution)** and **O21 (costs)**. Other Orders answer rule-grounded without case authorities until theirs are verified. Absence is honest, never fabricated.
- **Isolation:** per-API-key / per-`session_id`. A consumer proxying multiple end-users owns its own end-user separation.
- **Retention:** ~7 days, then deleted. **Not legal advice.**
