# Boolean / Terms-and-Connectors syntax — per-database reference

A reference for the `boolean-search` skill. The controlling authority is **each database's own current search guide** —
connector grammars are stable but field/segment names and the specialist databases' operators change. Tag anything
beyond the core connectors below `[verify against the database's current search guide]`.

Westlaw has full Terms-and-Connectors grammar. The arbitration specialists have weak or partial Boolean — build a
tight Boolean for Westlaw and a stripped-down keyword/phrase version for the specialists.

---

## The differences that break a search

**1. Proximity does not survive a move to a specialist.** Westlaw runs full Terms-and-Connectors grammar; the
arbitration specialists (Kluwer Arbitration, Jus Mundi, ITA Law) **silently ignore proximity connectors** and lean on
phrase and natural-language retrieval. A `/s` or `/p` tie that holds precision on Westlaw is simply dropped on a
specialist — the string still runs, but looser than you think, and nothing warns you. So: always name the database a
string is written for, and when porting from Westlaw to a specialist, degrade proximity to phrases + AND/OR
deliberately and say what you dropped.

**2. On Westlaw, a space is OR — not a phrase.** `breach contract` finds documents with *breach* OR *contract*, not the
phrase "breach contract". Use quotation marks for an exact phrase: `"breach of contract"`.

---

## Westlaw — Terms and Connectors

| Function | Operator | Example | Notes |
|---|---|---|---|
| OR | *(a space)* | `car automobile vehicle` | the default between terms |
| AND | `&` or `and` | `negligence & damages` | |
| Phrase | `"..."` | `"res ipsa loquitur"` | exact phrase |
| Same paragraph | `/p` | `landlord /p repair!` | |
| Same sentence | `/s` | `damag! /s remote!` | |
| Within n terms (either order) | `/n` | `breach /5 contract` | n = 1–255 |
| Order-sensitive within sentence | `+s` | `donor +s gift` | first term precedes second, same sentence |
| Order-sensitive within n terms | `+n` | `prior +3 art` | first precedes second within n |
| BUT NOT (exclude) | `%` | `damages % punitive` | excludes documents with the second term |
| Root expander (truncation) | `!` | `negligen!` | unlimited trailing characters |
| Universal character (one char) | `*` | `wom*n` → woman/women | one `*` per character; trailing `*`s cap word length |
| Turn off plurals/equivalents | `#` | `#fee` | forces the exact form only |
| Field/segment restriction | `field(...)` | `ti("hadley" "baxendale")` | e.g. `ti()` title, `sy,di()` synopsis/digest, `he()` headnote — `[verify field names]` |

Westlaw auto-retrieves regular and irregular plurals and possessives; use `#` to suppress.

---

## Specialist databases — weak / partial Boolean

These cover international, comparative, and investment-treaty material that Westlaw covers thinly. Their search
engines are built more for browsing and semantic retrieval than for Boolean precision. **Graceful degradation:** drop
proximity connectors (they are typically ignored), keep phrases and AND/OR, and tell the user what you dropped and why.
Treat every operator below as `[verify against the database's current search guide]`.

### Kluwer Arbitration

- Generally supports basic `AND`, `OR`, `NOT`, quoted `"phrases"`, and a `*` wildcard; offers fielded/advanced search
  (by title, author, institution, date) but limited or no reliable proximity connectors.
- Strategy: a few quoted terms of art joined by AND, plus the fielded filters; rely on the filters, not proximity.

### Jus Mundi

- Built around **semantic / natural-language** search across multilingual treaty and case material; Boolean support is
  limited. Quoted exact phrases are the most reliable precision lever; AND/OR may be partial.
- Strategy: feed it the concept as a natural-language phrase plus one or two quoted terms of art; do not expect
  proximity or nested Boolean to behave. Lean on its filters (instrument, decision type, date, jurisdiction).

### ITA Law (italaw.com)

- Primarily a **document repository** with a simple site search; weak Boolean — effectively keyword + quoted phrase.
- Strategy: a small set of quoted terms; as a fallback, a Google site-restricted search often outperforms the on-site
  engine: `site:italaw.com "fair and equitable treatment" "legitimate expectations"`.

---

## Building blocks (database-agnostic method)

1. **Buckets joined by AND.** A good search is 2–4 concept buckets joined by AND; each bucket is an OR-set of expanded
   terms. `(bucket A terms) AND (bucket B terms) AND (bucket C terms)`.
2. **Expand each bucket** with cognates (root expander, aimed to avoid over-reach) and alternative expressions
   (enumerated OR-set — synonyms do not share a root).
3. **Tie related terms with proximity,** not bare AND, where they must relate to each other to be on point — `/s` or
   `/p` on Westlaw — to hold precision up without dropping recall to document-level co-occurrence. (On a weak-Boolean
   specialist proximity is unavailable; fall back to phrases + AND.)
4. **Parenthesise** every OR-set before joining with AND, so precedence is explicit.
5. **Truncate deliberately.** `repudiat!` is safe; `cler!` over-reaches (clerical/clergy/clerk) — prefer an explicit
   OR-list when a root bleeds into unrelated words.
