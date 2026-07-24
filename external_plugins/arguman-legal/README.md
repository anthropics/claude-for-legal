# arguman-legal

arguman.ai brings nearly 15 million Turkish, European, and German case-law
records into Claude via a single hybrid-search MCP server with
**cross-lingual semantic search** — meaning a Turkish query surfaces
relevant English/French ECtHR judgments and German BGH rulings in their
original languages, purpose-built for comparative legal work. Covers the
courts whose rulings shape Turkish law in practice (Yargıtay, Danıştay,
Anayasa Mahkemesi, Uyuşmazlık Mahkemesi), the full multilingual HUDOC
corpus of ECtHR, and the German Bundesgerichtshof (criminal and civil).
Search results carry full provenance (esas no, karar no, tarih, daire /
Application No., Beschwerde-Nr.) so every citation can be verified.

- Use **arguman-legal** to run hybrid lexical + semantic search with
  neural reranking across 8 case-law collections — query in Turkish,
  English, or German and retrieve results across all three languages.
- Look up cases by docket number (esas/karar no, ECtHR Application No.,
  BGH Beschwerde-Nr.), retrieve full opinions, trace citation networks,
  and find similar rulings across chambers and jurisdictions.
- Stress-test legal positions by finding counter-authority — rulings that
  cut against a stated argument.
- Calculate Turkish criminal sentence enforcement (infaz hesaplama) under
  the CGTİHK (Law No. 5275).

## Example use cases

1. "Cezada haksız tahrik indirimi nasıl uygulanır? Yargıtay 1. CD'den son
   5 yıl içtihatları."
2. "AYM bireysel başvuru — ifade özgürlüğü (m.26) — sosyal medya paylaşımı
   nedeniyle disiplin cezası."
3. "Esas 2023/14587 numaralı Yargıtay 1. CD kararının tam metnini getir ve
   bu karara atıf yapan diğer kararları listele."
4. "Tasarrufun iptali davası açtık. Karşı tarafın itiraz edebileceği
   Yargıtay kararları nelerdir?" (counter-argument prep)
5. "Verilen 8 yıl hapis cezası için infaz süresini hesapla (tek suç,
   sabıkasız, 5275/107)."

## When to Use

- Turkish case-law research across Yargıtay, Danıştay, AYM, Uyuşmazlık.
- ECtHR judgments in their original languages — query in Turkish, surface
  relevant English/French rulings; ideal for Strasbourg jurisprudence
  research without language barriers.
- German BGH comparative analysis (criminal and civil) — particularly
  valuable for academic and doctoral work that cross-references German
  doctrine with Turkish reception; query in Turkish, retrieve German
  judgments via cross-lingual embeddings.
- Comparative cross-jurisdictional work (TR ↔ ECtHR ↔ BGH) in a single
  query.
- Citation lookup by docket number; full-text retrieval; similar-case
  discovery; citation-network traversal.
- Counter-argument identification for litigation preparation.
- Turkish criminal infaz / sentence-enforcement calculation.

## When Not to Use

- **Turkish statutes, regulations, or secondary legislation text** — use
  the official `mevzuat` MCP plugin.
- **Drafting petitions (dilekçe), contracts, or motions** — use first-party
  plugins such as `litigation-legal`.
- **US, UK, or EU case law** — use `cocounsel-legal`, `eulex-legal`, or
  `courtlistener`.
- **Live court filing, e-imza, or UYAP docket operations** — out of scope.
- **Predicting case outcomes** or analytics on specific judges, lawyers,
  or parties — out of scope for both ethical and policy reasons.
- **Exhaustive enumeration** ("every case ever mentioning X") — search
  returns ranked top results, not exhaustive lists.

## Skills

This plugin ships three skills:

- **`caselaw-search`** — hybrid search workflow with collection mapping,
  doctrinal translation (colloquial → legal Turkish), and drift detection.
- **`citation-network`** — anchor → similar → citing traversal for
  building doctrinal lineage maps.
- **`karsi-arguman`** — counter-argument finder for litigation preparation;
  stress-tests a stated position by finding rulings that go the other way.

## Authentication

OAuth 2.1 with Dynamic Client Registration (RFC 7591) and PKCE — no
manual API key, no static client ID. The Claude client registers itself
on first connect and runs the standard browser auth flow.

## Known limitations

- AYM bireysel başvuru coverage starts from late 2012 (the date the
  individual application procedure became operative); earlier norm-control
  decisions are indexed but pre-2012 individual applications are not.
- BGH coverage is concentrated post-1990; older Bundesgerichtshof rulings
  are sparse.
- ECtHR coverage spans the full multilingual HUDOC corpus in original
  languages (English, French primarily; other official translations
  where available). Searches use cross-lingual embeddings — Turkish
  query → English/French results — but Turkish translations of ECtHR
  judgments are not separately indexed (use the official European
  Court translation services if you need verbatim Turkish text).
- Reverse-citation graph traversal at scale is not yet exposed —
  `find_citing_cases` operates one hop at a time.

## Links

- **Website:** https://arguman.ai
- **Documentation:** https://arguman.ai/docs/mcp
- **Privacy:** https://arguman.ai/privacy
- **Terms:** https://arguman.ai/terms
- **Support:** iletisim@arguman.ai
- **MCP endpoint:** https://mcp.arguman.ai/mcp
- **Health probe:** https://mcp.arguman.ai/health
