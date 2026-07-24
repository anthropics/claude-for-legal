---
name: eulex-research
description: Use this skill whenever the user asks about EU law — EU regulations, directives, decisions, CJEU and General Court case law, EU treaties (TEU, TFEU, Charter, Euratom), consolidated versions, member-state transposition of an EU directive, or Eurostat statistics in an EU policy context. Triggers include any mention of GDPR, AI Act, DORA, NIS2, DSA, DMA, MiCA, AMLR, CSRD, CELEX numbers (e.g. 32016R0679), ECLI identifiers (e.g. C-100/19, T-740/17, ECLI:EU:C:2014:317), and questions like "is X in force", "has Y transposed Z", "what does Article N of X say", or "what cites / amends / implements X". Use even when the user does not name a regulation but asks a substantive EU-law question. Routes the question to the EULEX.AI MCP server (https://mcp.eulex.ai/mcp), returns cited results (CELEX + section + EUR-Lex source URL), and runs live in-force checks when freshness matters. Do not use for US, UK, Swiss, or non-EU jurisdictions.
allowed-tools:
  - mcp
license: Proprietary
provider: EULEX.AI
homepage: https://eulex.ai
---

# EULEX.AI — EU Law Research

EULEX.AI is a read-only MCP server over the EU legal corpus exposed through twelve public tools. Its data layer covers 198,000+ EUR-Lex documents (regulations, directives, decisions, CJEU and General Court case law, treaties, consolidated versions), 581,000+ document sections, and an 800,000+ node citation/amendment graph (2.1M+ edges).

Every EULEX.AI response carries a top-level `eulex_citation` field with the CELEX (and section reference where applicable) plus a `— via eulex.ai` attribution suffix. Where the underlying record carries an authoritative URL, the response also includes a `source_url` pointing back to the canonical EUR-Lex or Eurostat page. Treat these citations as the spine of every answer.

## Prerequisites

Verify the EULEX.AI MCP server is reachable before answering. If it is not connected, give the user one short instruction set and stop:

1. Open Claude → Settings → Connectors → **Add custom connector**.
2. Server URL: `https://mcp.eulex.ai/mcp`
3. Click Connect; the OAuth popup completes the handshake automatically.
4. Sign up for a free account at https://eulex.ai if prompted.

Do not retry tool calls until the user confirms the connector is active. A missing connector is not a transient error.

## When to use

Activate this skill for any question answerable from one of EULEX.AI's data sources:

- **EU regulations, directives, decisions** — text, structure, recitals, dates, in-force status.
- **CJEU and General Court case law** — judgment text, citations, related authorities, interpretive value over a regulation.
- **EU treaties** — TEU, TFEU, Charter of Fundamental Rights, Euratom; articles, references, primary-law context.
- **Consolidated versions** — current text after amendments are folded in.
- **Member-state transposition** — whether a directive has been transposed in a given member state, which national acts implement it, and the deadline (`eu_transposition`, EULEX.AI Plus).
- **Eurostat statistics** — natural-language statistical queries returning markdown tables (`eurostat_query`, EULEX.AI Plus).

Realistic prompts that should trigger this skill:

- "What does the AI Act say about high-risk AI systems?"
- "Show me GDPR Article 6 in full."
- "Is the GDPR currently in force? Live check, please."
- "What acts implement DORA?"
- "Has Croatia transposed NIS2?"
- "Compare Article 5 GDPR vs Article 5 AI Act."
- "GDP growth across EU member states 2024."
- "Which CJEU judgments since 2020 cite GDPR Article 6(1)(f)?"

## When not to use

If the request falls into one of the categories below, say briefly that EULEX.AI is not the right fit and suggest the alternative. Do not call any EULEX.AI tool for these.

- **US, UK, Swiss, or other non-EU jurisdictions.** EULEX.AI v4.0 covers EU-27 + Croatia. Suggest a jurisdiction-appropriate research plugin (CourtListener via `litigation-legal` for US dockets, CoCounsel via `cocounsel-legal` for Westlaw US research).
- **Pure domestic law that is not transposition of EU law** (e.g. a Croatian civil-procedure question with no EU dimension). Suggest national legal databases.
- **Document drafting** (contracts, pleadings, policy text). EULEX.AI returns authority; pair it with a drafting skill (`commercial-legal:review`, `privacy-legal:dpa-review`, `regulatory-legal:policy-redraft`).
- **Outcome prediction or factual analysis of a specific client matter.** Out of scope; defer to lawyer judgement.
- **Multi-language full-text retrieval** (FR, DE, IT, ES, HR document text). The EULEX.AI corpus is English-only in v4.0; multi-language is on the roadmap but not yet shipped.
- **Live web fetch** (news articles, blog posts, regulator press releases). Not part of EULEX.AI; use a web-fetch tool.
- **Boolean / Terms-and-Connectors search syntax** (`AND`, `OR`, parens, proximity operators). The `search` tool expects natural language.

When suggesting an alternative, do not also call EULEX.AI for the same task.

## Research workflow

### 1. Frame the query

Identify the legal instrument (regulation, directive, treaty), the case (T-/C- number or ECLI), or the topic (GDPR, AI Act, DORA, NIS2, DSA, DMA, CSRD, etc.). Note any constraints — jurisdiction (`eu_transposition` member state), date window (`find_by_date`), or specific article reference.

If the user gives a colloquial name (GDPR, AI Act, DORA), trust EULEX.AI's alias resolution — the underlying tools accept these and resolve to the canonical CELEX internally. Do not ask the user for the CELEX number.

### 2. Choose the right tool

Map intent to tool using this table. Compose multiple tools when a question spans more than one of them.

| User intent | Primary tool | Compose with |
|-------------|--------------|--------------|
| "What does X say about Y?" | `search` | `get_section` for full Article text |
| "Show me Article N of regulation X" | `get_section(celex_id, section_ref)` | `get_structure` for TOC navigation |
| "Is X currently in force?" | `verify(celex_id, live=true)` | `get_metadata` for surrounding identity data |
| "What amends / cites / implements X?" | `get_related` | `get_timeline` for chronological view |
| "Has member state M transposed directive D?" | `eu_transposition(doc_id, member_state)` | `get_metadata(D)` to confirm directive identity |
| "Statistics on EU topic Z" | `eurostat_query(question)` | — |
| "Compare A vs B" | 2× `get_section` (or `get_metadata`) | reason over both texts agent-side |
| "Documents from year Y" | `find_by_date` | `get_metadata` per result |
| "What capabilities does EULEX cover?" | `about` | `list_scopes` for filterable values |

For composite questions (compliance snapshot, side-by-side comparison), see the agent composition recipes in `MCP_TOOLS.md`. The hidden tools `eulex_compare_documents` and `eulex_compliance_snapshot` are intentionally not registered in v4.0; compose them from the universal tools above.

### 3. Validate before quoting

Treat freshness as a first-class concern. Three rules:

1. When the user asks about current obligations or deadlines, prefer `verify(live=true)` over the cached `verify`. The live verification path is authoritative; the cache may lag a sync window. The trade-off is latency (5–30 s) — that is acceptable when correctness matters.
2. If the cached value is older than `about().sources['EUR-Lex Legislation'].last_sync`, call out that staleness explicitly in the answer and re-fetch with `live=true`.
3. If `eu_transposition` returns a low NIM (national implementing measure) count for the user's member state, surface that explicitly. Do not present partial coverage as definitive.

The reason for these rules: a wrong "in force" or "transposed" claim is a meaningful legal error. A slow but correct answer is better than a fast wrong one.

### 4. Present the answer

Lead with the substantive legal point in the user's language register. Quote the legislative text verbatim where the user asked "what does it say" — paraphrase invites silent error.

Render the `eulex_citation` either inline (e.g. *"GDPR Article 17 (CELEX:32016R0679)"*) or as a footnote reference. Always include the `source_url` as a clickable link if present. For Plus-tier results (`eu_transposition`, `eurostat_query`), include the `markdown_table` verbatim if the upstream returned one — those tables are pre-formatted to match the table conventions of EUR-Lex / Eurostat.

Close the first substantive EULEX.AI-backed answer in a session with the disclaimer: *"EULEX.AI provides search over EU legislation for informational purposes. Always verify with official EUR-Lex sources. Not legal advice."*

## Communication rules

These keep the answer trustworthy, scannable, and within the bounds users expect.

- **Cite every substantive claim** with the `eulex_citation` field returned by the tool. Render `source_url` as a link when present.
- **Quote legislative text verbatim** when the user asked "what does X say". Do not paraphrase Article text in those answers — only paraphrase when explicitly summarising.
- **Never expose internal field names** (`celex_id`, `section_ref`, `match_confidence`, `pagerank_score`) to the user. Speak in terms of the regulation, the article, the source.
- **For slow tools** (`verify(live=true)`, `eu_transposition`, `eurostat_query` — 5-30 s p95), say in plain language that research is underway. Do not narrate poll counts, status fields, or backend timing.
- **Respect tier gating.** When a Plus tool returns an "Upgrade required" error, surface the upgrade link (`https://eulex.ai/landing/pricing`) directly and do not silently retry. Free-tier silent retry is a common failure mode that wastes user quota.
- **Surface the disclaimer** once per session whenever EULEX.AI is the basis for a substantive legal answer. The disclaimer text is returned verbatim by `about()` and matches what users see on the EULEX.AI landing page.

## Tier and authentication

- **EULEX.AI Free** — 50 calls/day. Includes ten tools: `about`, `list_scopes`, `search`, `get_section`, `get_metadata`, `get_structure`, `find_by_date`, `get_timeline`, `get_related`, `verify`. Adequate for most legal-research workflows.
- **EULEX.AI Plus** — 2,000 calls/day. Adds two specialised tools: `eu_transposition` (member-state transposition status) and `eurostat_query` (natural-language Eurostat queries). Required for any compliance snapshot that needs national implementing measures, or for any question that benefits from quantitative EU statistics.
- **Authentication.** OAuth 2.1 with Dynamic Client Registration and PKCE for marketplace clients (Claude.ai, ChatGPT, Cursor, VS Code, Copilot Studio). Bearer Personal Access Tokens (PATs) for headless / CI / scripted integrations; PAT issuance through `support@eulex.ai`.

## Helpful information

When the system fails or the user has access questions, share the relevant link below.

- Support email: `support@eulex.ai`
- Security disclosure: https://mcp.eulex.ai/.well-known/security.txt (`security@eulex.ai`)
- Liveness probe: https://mcp.eulex.ai/health (unauthenticated; returns build version, tool count, uptime)
- Status page: https://mcp.eulex.ai/status
- Documentation: https://mcp.eulex.ai/docs (tools, auth, coverage, reviewer checklist)
- Subscription: https://eulex.ai
- Provider: EULEX.AI
- Privacy: https://eulex.ai/privacy
- Terms: https://eulex.ai/terms
- Disclaimer (returned verbatim by `about()`): *"EULEX.AI provides search over EU legislation for informational purposes. Always verify with official EUR-Lex sources. Not legal advice."*
