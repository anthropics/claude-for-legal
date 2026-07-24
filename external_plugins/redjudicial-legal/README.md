# Red Judicial — Chile

Red Judicial brings the Chilean legal corpus into Claude. It exposes a single MCP tool, `redjudicial_search`, that searches across cross-linked sources:

- **Court jurisprudence** — over 2.5 million decisions: 287,000+ Supreme Court (Corte Suprema, 2005–present) and ~1.4M Courts of Appeals (Cortes de Apelaciones, active backfill toward ~2M), ingested with full text and indexed daily.
- **Constitutional Tribunal** — Tribunal Constitucional rulings (12,000+).
- **Administrative & specialized case law** — Comptroller General opinions (Contraloría, 90,000+), tax authority and Tax & Customs Courts (SII, TTA), labor authority (Dirección del Trabajo), financial-market regulator (CMF), social-security (SUSESO), competition court (TDLC), consumer protection (SERNAC), environmental courts, the industrial-property court (TDPI) and the national human-rights institute (INDH).
- **Statutes** — roughly 19,000 in-force norms from BCN / LeyChile (the official Chilean legislative repository), with article-level granularity.
- **Doctrine** — academic articles from open-access sources (SciELO, university repositories).
- **First-instance rulings** (civil, labor, criminal, family, debt collection) — labor (~214,000) and debt collection complete; civil, criminal, family in active incorporation.

Each result returns a verifiable citation with a link back to the official source (Poder Judicial, BCN, and the issuing authority). The tool is read-only and does not write to user systems.

For Spanish-speaking practitioners and firms in Chile and Latin America. See [README.es.md](./README.es.md) for the Spanish version.

## Example use cases

1. Research how the Chilean Supreme Court has ruled on `lucro cesante` (loss of profits) in commercial liability cases over the last five years.
2. Retrieve the in-force version of an article of the Civil Code along with the most recent rulings interpreting it.
3. Cross-reference a Supreme Court holding on labor dismissal with academic doctrine on `despido injustificado`.
4. Build a memo summarizing the dominant criteria of a specific Chilean Supreme Court justice on tax matters (when used together with the public Red Judicial product).

## When to Use

- Questions answerable from Chilean caselaw, statutes, or open-access doctrine.
- Locating the current text of a Chilean statute, decree, or regulation, and its most recent jurisprudential interpretation.
- Cross-source research that combines a Supreme Court holding, the underlying statutory framework, and academic commentary.
- Comparative research between Chilean jurisprudence and Latin American hispanophone jurisdictions (planned expansion).

## When Not to Use

- U.S. or other non-Chilean primary law — out of corpus today. Red Judicial does not cover those jurisdictions; for other jurisdictions, use the appropriate plugin from the marketplace.
- First-instance rulings — labor and debt collection are complete; civil, criminal and family are in active incorporation.
- Real-time docket monitoring of specific cases — not supported.
- Drafting Chilean pleadings or contracts — Red Judicial provides primary-source research; drafting is left to the attorney.
- Outcome predictions for a specific case — the corpus supports research, not prediction.

## Authentication

The MCP server at `https://ia.redjudicial.cl/mcp/v1` is OAuth 2.0 protected with **Dynamic Client Registration** (RFC 7591) and **PKCE** (RFC 7636). Clients that support DCR — including Claude.ai web Custom Connectors — discover the authorization server through the standard metadata endpoint at `https://ia.redjudicial.cl/.well-known/oauth-authorization-server` (RFC 8414) and register themselves automatically. No pre-shared client ID is needed.

End users sign in with their Red Judicial account and grant the connector consent before the tool becomes available.

## Coverage by jurisdiction

| Jurisdiction | Source | Status |
|---|---|---|
| Chile — Supreme Court (Corte Suprema) | Poder Judicial | ✅ live (287,000+ decisions, 2005-present) |
| Chile — Courts of Appeals (Cortes de Apelaciones) | Poder Judicial | ✅ live (~1.4M, active backfill toward ~2M) |
| Chile — Constitutional Tribunal (TC) | Tribunal Constitucional | ✅ live (12,000+) |
| Chile — Comptroller General (Contraloría) | CGR | ✅ live (90,000+ opinions) |
| Chile — tax (SII, Tax & Customs Courts) | SII / TTA | ✅ live |
| Chile — labor (Dirección del Trabajo) | DT | ✅ live |
| Chile — financial markets, social security, competition, consumer | CMF / SUSESO / TDLC / SERNAC | ✅ live |
| Chile — environmental courts, IP court, human-rights institute | TA / TDPI / INDH | ✅ live |
| Chile — statutes and decrees | BCN / LeyChile | ✅ live (~19,000 in-force norms) |
| Chile — open-access doctrine | SciELO, university repositories | ✅ partial (~2,500 articles) |
| Chile — first-instance: labor + debt collection | Poder Judicial | ✅ live (~245,000) |
| Chile — first-instance: civil, criminal, family | Poder Judicial | 🚧 in active incorporation |
| LATAM hispanophone expansion (Colombia, Mexico, Argentina) | Multiple | 🔭 exploratory |

## Compliance and privacy

- Operated by **Simpley SpA**, a Chilean company (RUT 77.983.964-8), under the **Red Judicial** brand.
- Data hosted in `sa-east-1` (AWS São Paulo).
- No training on user queries. Each request is processed and discarded except for billing-grade counters.
- Compliance roadmap aligned with the new Chilean Data Protection Law (Ley 21.719, effective 1 December 2026): designated DPO and Data Protection Impact Assessment in progress.
- Privacy policy: https://ia.redjudicial.cl/legal/privacidad
- Terms of service: https://ia.redjudicial.cl/legal/terminos

## Disclaimer

Red Judicial provides primary-source legal research with verifiable citations. It does not provide legal advice and is not a substitute for a qualified attorney. Every result links to its official source and should be verified there before use; professional judgment and responsibility for any filing or advice remain with the lawyer.

## Subscription and billing

Red Judicial uses a credit-based model with five subscription tiers. Each call to `redjudicial_search` consumes one credit. A monthly free allowance is available; paid tiers extend the cap and unlock additional tools as they roll out (`redjudicial_get_norm`, `redjudicial_get_sentence`, `redjudicial_research_brief` — planned). Pricing and signup: https://ia.redjudicial.cl/pricing

## Compliance with the partner-plugin technical bar

This plugin satisfies the five criteria documented in [`CONNECTORS.md`](../../CONNECTORS.md):

1. **HTTPS + OAuth 2.0** with Dynamic Client Registration and PKCE on the streamable HTTP transport at `/mcp/v1`.
2. **Read-heavy tools only.** `redjudicial_search` is read-only; no writes to user systems.
3. **Provenance on every result.** Each hit returns `citation`, `url` (link to the official source), `source` (`jurisprudencia` / `ley` / `doctrina`), and the issuing court or authority with the decision/publication date.
4. **No instructional content in tool results.** Tool responses are data plus structured metadata (`result_quality`, `suggested_followups`, `display_hints`); no embedded directives to the calling model.
5. **Graceful error degradation.** 401 (unauthenticated), 402 (out of credits), 5xx (upstream) are returned with clean JSON-RPC error codes and human-readable messages, plus `suggested_followups` where applicable.

### Links

- **Documentation:** https://ia.redjudicial.cl/mcp
- **Sign up / pricing:** https://ia.redjudicial.cl/pricing
- **Support:** contacto@redjudicial.cl
- **Operator:** Simpley SpA (Chile, RUT 77.983.964-8)
- **License:** Apache-2.0
