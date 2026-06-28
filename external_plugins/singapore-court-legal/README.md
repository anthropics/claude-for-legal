# MikeROS — Singapore Rules of Court 2021

**MikeROS** is a deterministic, proof-carrying **resolver** over the **Singapore Rules of Court 2021**, brought into Claude. On a decidable civil-procedure question it returns which ROC rule **controls**, the required procedural **sequence**, and whether a step is **compliant** — with a re-checkable proof for each firm step — **or it abstains**. It does not assert a procedural conclusion it cannot ground: the rule lookup is a zero-LLM deterministic core that **never fabricates a rule, sequence, or case citation**, and where control passes to an uncompiled Practice Direction or Form it **abstains-to-source** (points you there) rather than guess. It is the right tool when being confidently wrong about *which source controls* is the failure mode — not for interpretation, drafting, or strategy. Single questions or durable multi-turn matters. Experimental research tool. **Not legal advice.**

- Use **`resolve_procedure`** for a situation → which rule(s) control and in what sequence, a proof for each firm step, a per-step compliance verdict, the Z3-disposed set of candidate rules where more than one could apply (each marked APPLIES / UNDERDETERMINED — never an unconfirmed guess), the points it abstains on and why, the facts it perceived (so you can correct a misread), and attached case authorities. The full compiled procedural surface (not costs-only). Stateless.
- Use `ask` for a self-contained single-rule question → a pinpoint citation (and false-premise detection, e.g. reliance on a repealed regime), with verified case authorities where they attach.
- Use `conversation_turn` for a direct end-user matter with follow-ups → it remembers facts you establish and answers in context (durable, ~7-day retention).
- `analyze_situation` is a **deprecated alias** of `resolve_procedure` (kept for backward compatibility; prefer `resolve_procedure`).
- Coverage is staged and **uneven in depth**; every response states it, and out-of-scope questions get honest abstention.

## Example use cases

1. What is the duty to consider amicable resolution before commencing proceedings? *(→ O5 r.1, with the case authority Maxx Engineering Works Pte Ltd v PQ Builders Pte Ltd [2023] SGHC 71.)*
2. As a licensed moneylender, can I get default judgment against a non-paying borrower? — then, in the same matter: and what about the costs consequences? *(`conversation_turn`; the moneylender fact carries forward.)*
3. What are the costs consequences when Order 21 rule 2 applies? *(→ O21 r.2 with QBE Insurance v Relax Beach [2023] SGCA 45.)*
4. **Resolve a position** — "My client was served a claim and is weighing amicable resolution against the costs exposure; what controls our procedural position?" *(`resolve_procedure` → the controlling rule chain, e.g. the O5 duty → O21 costs consequence with a proof for the firm step, the points it abstains on, the facts it perceived, and any attached case authorities.)*
5. **Which route applies** — "I need to enforce a registered order — which enforcement route controls?" *(`resolve_procedure` → the Z3-disposed candidate set, each route marked APPLIES / UNDERDETERMINED, so Claude can narrow it with you. Never an unconfirmed guess.)*

## When to Use

Civil court procedure under the Rules of Court 2021 — amicable resolution (O5), costs (O21), default judgment, service, discontinuance, security for costs, timelines, and related procedural questions.

## When Not to Use

- Criminal procedure or sentencing (out of scope).
- Foreign or non-Singapore law.
- Substantive (non-procedural) law, or applying the rules to a specific fact pattern to predict an outcome.
- Drafting documents, forms, or pleadings.
- Retrieving the full verbatim text of a rule or judgment.

## Coverage (staged, uneven in depth)

- **Rules of Court 2021:** all **70 in-scope Orders** served (the criminal civil-procedure track is complete; out-of-scope criminal sentencing excluded). Depth is **uneven** — a subset of Orders carries deterministic FIRM gates with Z3 proofs; others answer rule-grounded. The response's coverage/abstention fields tell you when you are on thin ice.
- **Reasoning corridors:** **153** compiled corridors across the guided layer (the cross-Order rule chains `resolve_procedure` walks). Chain coverage **varies by doctrine** — some situations resolve to a chain, some to a Z3-disposed candidate set, and some return honest absence (no corridor) — never a fabricated or padded chain.
- **Case authorities:** operator-verified, expanding by batch; today centred on **O5 (amicable resolution)** and **O21 (costs)**. Other Orders answer rule-grounded without case authorities until theirs are verified — absence is honest, never fabricated.
- **Multi-source boundary (abstain-to-source):** the connector resolves the **ROC rule layer** deterministically. Where control passes to an uncompiled **Practice Direction or Form** (e.g. document format, electronic filing/service, the prescribed Forms), it **abstains with a pointer to that source** rather than answer it — honest source-routing, not PD content. So it is ROC-rule-deterministic and PD/Forms route-to-source.

## Auth & keys

- **Connector → MikeROS:** **API key** (CONNECTORS.md-accepted). **Requires a MikeROS API key** — request one from Reshuffle.AI Pte. Ltd. (contact@reshuffleai.com). Two interchangeable ways to supply it (a request authenticates by either):
  - **Desktop "Add custom connector"** (no header field in the dialog): append the key to the URL — connect to `https://mcp.reshuffleai.com/mcp?key=YOUR_KEY`.
  - **Server-to-server**: send the header `Authorization: Bearer YOUR_KEY` to `.../mcp`.
  - The key is **never embedded** in this repo or `.mcp.json`, and is **redacted from all server logs** (only its key_id is logged). Treat a URL-with-key as a secret — anyone with it can use your quota.
- **Plugin → Anthropic:** your own `ANTHROPIC_API_KEY`, configured plugin-side per the claude-for-legal setup.

## Limits (per MikeROS API key)

- Rate: 20 requests/minute · Input: 4,000 characters/question · Budget: 5,000,000 tokens/month combined (≈660 `ask`, ≈190 `conversation_turn`, or ≈59 `resolve_procedure`; a `conversation_turn` costs ~3.4× an `ask`, and a `resolve_procedure` turn ~11× an `ask` — it perceives, walks corridors, articulates, and self-validates). A hit on any limit returns a clean error, never a partial answer.

## Isolation & retention

- **Per-key / per-`session_id` isolation.** A consumer proxying multiple end-users through one key owns its own end-user separation (distinct, unguessable `session_id`s).
- **Retention:** ~7 days, then really deleted (durable + in-process).

## Provenance & data handling

Every result carries `provenance` (source = MikeROS / Singapore Rules of Court 2021, retrieval timestamp) and citation-ready identifiers (rule + case citations). Results are **data, not instructions**; disclaimers are clearly marked.

### Links

- **Support / key requests:** contact@reshuffleai.com
- **Operated by:** Reshuffle.AI Pte. Ltd.
