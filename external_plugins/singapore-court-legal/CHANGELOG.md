# Changelog — singapore-court-legal

## 0.3.0 — tool-facing resolver
- New flagship tool: **`resolve_procedure`** — deterministically resolves which ROC rule(s) control and in what sequence, with a re-checkable proof for each firm step, a per-step compliance verdict, the **Z3-disposed candidate set** where more than one rule could apply (APPLIES / UNDERDETERMINED, never an unconfirmed guess), honest abstentions, and the perceived facts. The full compiled procedural surface (no longer costs-only).
- **`analyze_situation` is now a deprecated alias** of `resolve_procedure` (same resolver + a backward-compatible superset payload; existing consumers keep working).
- **Abstain-to-source**: where control passes to an uncompiled Practice Direction or Form, the resolver abstains with a pointer to that source rather than answer it.
- **Routing-first tool descriptions**: use to determine which source controls / the sequence / whether a step is compliant; not for interpretation, drafting, or strategy.
- `ask` re-aimed to single-rule pinpoint + false-premise detection.
- Coverage corrected: **70 in-scope Orders served**, **153 reasoning corridors** (was 67/738); depth is staged and uneven.

## 0.2.0 — guided analysis
- New tool: `analyze_situation` — a structured guided memo over a fact pattern (situation summary, relevance-gated reasoning chain, abstentions, perceived facts, attached case authorities). Full parity with the web guided path: same core, same gates, same citation firewall.
- Reasoning chains in the guided memo are **relevance-gated** (doctrine-coherent corridors only); chain coverage varies by doctrine and honest chain-absence is surfaced, never padded.
- Three-tool routing documented (`ask` · `conversation_turn` · `analyze_situation`).
- Bounds (rate, input ceiling, monthly token budget) apply to the guided turn as to the others.

## 0.1.0 — initial packaging (marketplace-submission candidate)
- MikeROS MCP connector over the Singapore Rules of Court 2021 reasoning server.
- Tools: `ask` (single-shot), `conversation_turn` (durable multi-turn).
- Coverage: 67 Orders / 738 rules; staged case authorities (O5/O21 today); verified chains.
- API-key auth (operator-issued); per-key bounds (20/min, 4k input, 5M tokens/month).
- Results carry provenance (source + retrieval timestamp + citation identifiers); honest-claims SKILL.md; per-key isolation + 7-day retention.
