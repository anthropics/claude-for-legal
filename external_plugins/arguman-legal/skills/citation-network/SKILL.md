---
name: citation-network
description: >
  Use this skill when the user wants to map the citation graph around a
  Turkish case — looking up a case by esas/karar number, finding similar
  rulings, or tracing which rulings cited a given decision. Especially
  valuable for tracking içtihadı birleştirme (HGK/CGK) influence and
  building a doctrinal lineage around a precedent.
allowed-tools:
  - mcp
---

# Citation Network — Turkish Case Lineage

Turkish high-court rulings travel as networks: a Yargıtay HGK içtihadı
birleştirme decision settles a dispute, lower chambers cite it, follow-on
rulings refine its edges, and over time a doctrinal line emerges.
This skill traces that network using three tools — `case_lookup`,
`find_similar`, and `find_citing_cases` — to give the user a connected
map of authority rather than a single isolated citation.

## Prerequisites

The `arguman-legal` MCP server must be connected. Verify availability
before starting. If unavailable, inform the user and stop.

## When to Use

- The user names a specific case (esas/karar no) and wants to see how it
  has been received, refined, or cited.
- The user wants to find rulings **similar in fact pattern or doctrine**
  to an identified anchor case.
- Tracking the influence of an HGK / CGK / Genel Kurul içtihadı birleştirme
  decision through later chambers.
- Building a "doctrinal lineage" view (anchor case → similar → who cited)
  for a memo or brief.

## When Not to Use

- **Open-ended doctrinal research without a starting case** — use the
  `caselaw-search` skill first to find an anchor, then come back here.
- **Statute/regulation lineage** (not case-law) — use the `mevzuat` MCP.
- **Live SEGBİS / UYAP docket tracking** — out of scope.
- **Judge or chamber analytics** — out of scope.

## Communication Rules

- **Mirror the user's language.** Turkish in → Turkish out; English in →
  English out. Default to Turkish when ambiguous (Turkish lawyers are the
  primary audience).
- Render every case as: **court** + **chamber** + **esas no** + **karar no**
  + **tarih** + **collection** (e.g., `Yargıtay HGK, E.2019/4-1234 K.2021/567,
  14.06.2021 (hukuk)`).
- For HGK / CGK / İBK decisions, **flag the binding nature explicitly**
  ("içtihadı birleştirme kararı — alt mahkemeler için bağlayıcı"). Other
  rulings are persuasive only; never overstate.
- When presenting the network, distinguish:
  - **Anchor** (the case the user named or you identified)
  - **Similar** (related by fact pattern / doctrine, from `find_similar`)
  - **Citing** (later rulings that referenced the anchor, from `find_citing_cases`)

## Workflow

### 1. Anchor the case

If the user gave an esas/karar reference:

```
case_lookup(esas_no="2023/14587", karar_no="2024/921", collection="ceza")
```

If they gave a docket fragment or chamber+date, try the most specific
fields first; fall back to `caselaw-search` if `case_lookup` returns no
hit.

For HGK/CGK rulings, esas numbers carry a kurul prefix, e.g.,
`E.2019/4-1234` (4 = ceza-genel-kurul indicator). Preserve the dash; do
not strip it.

### 2. Pull the full opinion

```
get_full_text(point_id=<from step 1>)
```

Verify the anchor actually addresses the issue the user named. If the
docket matched but the opinion is about a different issue (sometimes happens
with re-used esas numbers across years), say so and stop — do not
fabricate continuity.

### 3. Expand the network

Run both expansions:

- `find_similar(point_id=<anchor>)` — rulings near the anchor in
  embedding + lexical space. Best for "what other rulings are about
  the same problem?"
- `find_citing_cases(esas_no=<anchor>)` — rulings that explicitly
  cited the anchor's esas number. Best for "how was this received
  downstream?"

Note: reverse-citation traversal (citation graph at scale) is not yet
exposed; this skill operates one hop at a time.

### 4. Order and present

Sort the network by date (most recent first by default; let the user ask
for chronological if they want to see evolution). Group by:

- **Same chamber line** (e.g., all Yargıtay 1. CD rulings together)
- **Across-chamber adoption** (when a doctrine moves from one daire to
  another, this is a strong stability signal)
- **Higher-court endorsement** (HGK/CGK adopting a chamber line is
  near-decisive)

Surface contradictions. If `find_citing_cases` shows the anchor was
later overruled or qualified, flag that prominently.

## Helpful information

- Provider: arguman.ai (Istanbul, Türkiye)
- Auth: OAuth 2.1 with Dynamic Client Registration + PKCE
- Coverage: nearly 15 million rulings across 8 collections (Yargıtay,
  Danıştay, AYM, AİHM multilingual HUDOC, Uyuşmazlık, BGH)
- HGK/CGK esas format: `E.YYYY/<kurul-no>-<seq>` (preserve dash)
- ECtHR citation format: `<Case Name v. State, App. No. <num>/<yy>,
  <DD Month YYYY>>` — preserve original-language case name
- BGH citation format: `BGH, Beschluss/Urteil v. <DD.MM.YYYY>,
  Az. <Senat> <number>/<year>`
- Documentation: https://arguman.ai/docs/mcp
- Support: iletisim@arguman.ai
