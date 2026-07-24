---
name: caselaw-search
description: >
  Use this skill whenever the user asks about Turkish case law, ECtHR judgments
  (in any language), or German BGH precedents. Runs hybrid lexical + semantic
  search with neural reranking and **cross-lingual retrieval** — a Turkish
  query surfaces relevant English/French/German rulings across Yargıtay,
  Danıştay, AYM, AİHM, Uyuşmazlık, and BGH collections (nearly 15 million
  rulings total). Handles natural-language Turkish, doctrinal translation,
  year/chamber filtering, and full-text retrieval with proper esas/karar
  citation.
allowed-tools:
  - mcp
---

# Multilingual Case-Law Search

`arguman-legal` provides hybrid case-law search across the major courts whose
output shapes Turkish law in practice: Yargıtay (Court of Cassation, criminal
and civil chambers), Danıştay (Council of State), Anayasa Mahkemesi (Constitutional
Court — both norm review and individual application), AİHM (the full
multilingual HUDOC corpus — judgments in their original language, primarily
English and French), Uyuşmazlık Mahkemesi (Conflicts Court), and the German
Bundesgerichtshof (criminal and civil — judgments in German).

Search combines lexical and semantic retrieval with **cross-lingual matching**
(Turkish queries hit English/French/German content) and neural reranking for
relevance ordering. This is the differentiator — comparative work no longer
requires manual translation of the query. Results carry full provenance
(esas no, karar no, tarih, daire, or Application No. / Beschwerde-Nr. for
ECtHR/BGH) so every citation can be verified.

## Prerequisites

The `arguman-legal` MCP server must be connected. Verify availability before
searching. If the server is not connected, inform the user and stop.

## When to Use

- Any question answerable from Turkish high-court rulings (Yargıtay,
  Danıştay, AYM), e.g.:
  - "Yargıtay 1. CD'nin haksız tahrik indirimini hangi koşullarda uyguladığı"
  - "Danıştay'ın imar planına itiraz sürelerine yaklaşımı"
  - "AYM'nin ifade özgürlüğü m.26 sosyal medya kararları"
- ECtHR judgments in their original languages (English, French primarily) —
  query in Turkish, receive results in EN/FR via cross-lingual embeddings;
  ideal for Strasbourg jurisprudence research without manual translation
- German BGH comparative analysis (criminal and civil) — query in Turkish,
  retrieve German-language judgments
- Citation lookup by esas/karar no, ECtHR Application No., or BGH Beschwerde-Nr.
- Cross-jurisdiction comparison in a single query (TR ↔ ECtHR ↔ BGH)

## When Not to Use

If the request matches one of the categories below, briefly tell the user
this skill isn't the right fit and point to the suggested alternative.

- **Turkish statute or regulation text** (e.g., "Türk Ceza Kanunu m.86 nedir?")
  - _Instead:_ suggest the official `mevzuat` MCP plugin.
- **Drafting petitions, contracts, or legal memoranda**
  - _Instead:_ suggest first-party plugins such as `litigation-legal`.
- **Live court-filing, e-imza, or UYAP operations** — out of scope.
- **Predicting case outcomes or guessing what a specific judge will do**
  — out of scope.
- **Analytics on specific judges, lawyers, or parties** — out of scope
  for both ethical and policy reasons; do not attempt.
- **US, UK, EU, or non-TR/DE jurisdictions** — suggest `cocounsel-legal`,
  `eulex-legal`, or `courtlistener`.
- **Exhaustive enumeration** ("bring me every single case mentioning X") —
  search returns ranked top results, not exhaustive lists. Set this
  expectation upfront.

## Communication Rules

- **Mirror the user's language.** If the user wrote in Turkish, respond
  in Turkish; if in English, respond in English. Most users of this skill
  are Turkish lawyers — default to Turkish when the language is ambiguous.
- Cite every authority verbatim with: **court** + **chamber (daire)** +
  **esas no** + **karar no** + **tarih** + **collection**.
  Example: `Yargıtay 1. CD, E.2023/14587 K.2024/921, 12.03.2024 (ceza)`.
- Keep Turkish legal terminology untranslated even when responding in
  English (esas no, karar no, daire, içtihadı birleştirme, HGK, CGK) —
  add a brief gloss on first use only.
- Never claim a ruling "binds" lower courts unless it is an HGK/CGK
  içtihadı birleştirme decision — verify before asserting.
- If a snippet is ambiguous, fetch full text with `get_full_text` rather
  than guess.
- Surface the doctrinal translation you used when the user's wording was
  colloquial (e.g., "I searched 'haksız tahrik' for the colloquial
  'kavga edip vurdum'") so the user can confirm the framing.

## Workflow

### 1. Pick the collection

Map the user's question → collection set:

| Domain | Collections |
|---|---|
| Criminal law (TR) | `ceza` (+ `anayasa` if constitutional dimension) |
| Civil/commercial (TR) | `hukuk` (+ `anayasa`) |
| Administrative (TR) | `idare` (+ `anayasa`) |
| Constitutional review / individual application (TR) | `anayasa` |
| Human rights / ECHR violations | `aihm` (multilingual, EN/FR primary) + `anayasa` |
| Jurisdiction conflicts (civil vs. admin, etc.) | `uyusmazlik` |
| Comparative criminal (DE) | `bgh_straf` (German originals) |
| Comparative civil (DE) | `bgh_zivil` (German originals) |

For cross-lingual queries, no special handling needed — write the search
in Turkish and the embeddings will surface relevant EN/FR/DE judgments.
When citing, preserve the judgment's original language in quoted text;
add a brief Turkish gloss only when the user explicitly asks for translation.

For multi-collection queries (e.g., a constitutional-criminal question),
prefer two focused `search` calls over one diffuse one.

### 2. Decide expansion mode

The `search` tool has an `expand` parameter (boolean, both modes cost 1
credit — pick on quality, not price):

- `expand=false` (default): one focused pass. Use when the query already
  contains exact doctrinal terms, article numbers, esas/karar IDs, or
  4+ keyword phrases.
- `expand=true`: broader recall via query expansion + neural rerank. Use
  when the query is vague, natural-language, or uses lay wording.

### 3. Inspect for drift, then re-query if needed

Vector recall drifts to adjacent topics. After the first pass, check for
drift signals:

- Top results' **daire/court doesn't match** the question's domain
  (e.g., asking about ceza but results come from hukuk)
- **Cited articles/statutes diverge** from what the user implied
- **Snippets don't contain the core verb/issue**

If drift, **translate the user's wording into doctrinal Turkish legal
terms** and rerun with `expand=false`. Examples:

| User said | Doctrinal term |
|---|---|
| "Kavga edip vurdum" | haksız tahrik (TCK m.29) |
| "Borçludan mal kaçırıyor" | tasarrufun iptali davası (İİK m.277) |
| "Boşandım yeniden evlenemiyorum" | iddet süresi (TMK m.132) |
| "Eski karımdan dolayı eve geri dönmek istemiyor" | velayet — çocuğun üstün yararı |
| "Vergi denetimi yapıldı borç çıktı" | re'sen / ikmalen tarhiyat (VUK m.30/29) |
| "Polis arama yapmak istedi izin vermedim" | adli/önleme araması, makul şüphe |

### 4. Drill down

Once a candidate ruling is identified:

- `get_full_text(point_id)` — pull the full opinion when the snippet
  is insufficient
- `find_similar(point_id)` — neighboring rulings on the same issue
- `find_citing_cases(esas_no)` — see who cited this one (best with
  HGK/CGK içtihadı birleştirme decisions)
- `case_lookup(esas_no, karar_no?)` — verify a specific docket reference

### 5. Synthesize and cite

- Group rulings by **doctrinal position** (majority/minority, evolving line,
  içtihadı birleştirme anchor)
- Note **temporal trends** (older line → newer line, post-2017 anayasa
  değişiklikleri etc.) when relevant
- For each cited authority, render the full citation format from
  Communication Rules
- If results contradict each other, surface the conflict explicitly
  rather than picking a side silently

## Helpful information

- Provider: arguman.ai (Istanbul, Türkiye)
- Auth: OAuth 2.1 with Dynamic Client Registration + PKCE
- Coverage: nearly 15 million rulings across 8 collections (Yargıtay Ceza,
  Yargıtay Hukuk, Danıştay, AYM, AİHM multilingual HUDOC, Uyuşmazlık,
  BGH Straf, BGH Zivil)
- Cross-lingual retrieval: Turkish, English, French, and German queries
  all retrieve across all languages
- Free tier credits per user; rate limit returns HTTP 429 with `Retry-After`
- Privacy: https://arguman.ai/privacy
- Terms: https://arguman.ai/terms
- Documentation: https://arguman.ai/docs/mcp
- Support: iletisim@arguman.ai
