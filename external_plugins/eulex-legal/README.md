# EULEX.AI Legal

EULEX.AI Legal brings semantic search and a citation/amendment knowledge graph over EU primary law, secondary legislation, CJEU case law, EU treaties, and member-state transposition status into Claude. Backed by 198,000+ EUR-Lex documents, 581,000+ document sections, an 800,000+ node Neo4j graph, a 3,072-dimension Pinecone vector index, and live EUR-Lex Cellar SPARQL plus Eurostat REST. Every result carries an `eulex_citation` (CELEX + section ref) and, where applicable, a `source_url` pointing back to the canonical EUR-Lex or Eurostat page. Read-only — no write tools, no irreversible operations.

- Semantic + keyword search across EU regulations, directives, decisions, CJEU judgments, treaties, and consolidated versions.
- Article-level retrieval (`get_section`, `get_structure`) with TOC navigation, neighbours, and source URLs.
- Citation / amendment / implementing-act graph (`get_related`) and chronological event timeline (`get_timeline`).
- Live in-force verification against EUR-Lex Cellar SPARQL (`verify(live=true)`).
- Member-state transposition status for directives (`eu_transposition`, EULEX.AI Plus).
- Natural-language Eurostat queries returning markdown tables (`eurostat_query`, EULEX.AI Plus).

## Example use cases

1. What does the AI Act say about high-risk AI systems? Quote Article 6 and the Annex III categories.
2. Has Croatia transposed NIS2 into national law? Show the implementing acts and dates.
3. Compare GDPR Article 6 to AI Act Article 5 on lawful processing vs prohibited practices.
4. List CJEU judgments since 2020 that cite GDPR Article 6(1)(f) on legitimate interests.
5. GDP growth across EU member states for the last available year — show as a table.

## When to Use

Any question answerable from EU primary law, EU secondary law (regulations, directives, decisions), CJEU and General Court case law, EU treaties (TEU, TFEU, Charter), consolidated versions, member-state transposition status (per `eu_transposition`), or Eurostat statistics from EULEX.AI's indexed corpus. Examples include:

- The text, structure, or recitals of a specific EU instrument (regulation, directive, treaty).
- Whether a directive has been transposed into a member state's law and which national acts implement it.
- What amends, repeals, or is implemented by a given EU act.
- How CJEU cases interpret a regulation or treaty article.
- Statistical context for EU policy questions (Eurostat).

## When Not to Use

- US, UK, Swiss, or other non-EU jurisdictions — EULEX.AI v4.0 covers EU-27 + Croatia only.
- Member-state domestic law that is not transposition of EU law (e.g. pure national civil-procedure questions).
- Pleadings, briefs, contracts, or document drafting (EULEX.AI returns authority; it does not draft).
- Predictions about case outcomes or factual analysis of a client's situation.
- Boolean / Terms-and-Connectors search syntax — `search` expects natural language.
- Live web pages or news — `web_fetch` is not part of EULEX.AI.
- Multi-language full-text retrieval — the EULEX.AI index is English-only in v4.0 (multi-language on the roadmap).

### Links

- **Documentation:** https://mcp.eulex.ai/docs
  - Tools: https://mcp.eulex.ai/docs/tools
  - Auth: https://mcp.eulex.ai/docs/auth
  - Data coverage: https://mcp.eulex.ai/docs/coverage
  - Reviewer checklist: https://mcp.eulex.ai/docs/review
- **Liveness:** https://mcp.eulex.ai/health (unauthenticated JSON, suitable for external uptime probes)
- **Support:** support@eulex.ai
- **Subscription:** EULEX.AI Free tier (50 calls/day, 10 free tools). EULEX.AI Plus (2,000 calls/day, all 12 tools — adds `eu_transposition` and `eurostat_query`). Sign-up: https://eulex.ai
- **Provider:** EULEX.AI
- **Privacy:** https://eulex.ai/privacy
- **Terms:** https://eulex.ai/terms
