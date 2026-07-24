---
name: karsi-arguman
description: >
  Use this skill when the user states a legal position and wants to stress-test
  it — find rulings that went the OTHER way, identify the strongest counter-
  arguments, and surface qualifications, exceptions, or doctrinal lines that
  cut against the user's framing. Built for litigation preparation: see what
  the opposing side will cite before they cite it.
allowed-tools:
  - mcp
---

# Counter-Argument Finder

When a lawyer is preparing a position, the most dangerous citations are the
ones they did not look for. This skill flips a stated position and goes
hunting for rulings that contradict, qualify, or outright reject it —
across the same court system and across chambers.

It is the inverse of `caselaw-search`: instead of confirming a position,
it tries to break it.

## Prerequisites

The `arguman-legal` MCP server must be connected. Verify availability
before starting. If unavailable, inform the user and stop.

## When to Use

- The user has a draft argument, brief, or appellate strategy and wants
  to know what the other side will cite.
- The user asserts a doctrine and wants to find its limits, exceptions,
  or competing line.
- Pre-hearing preparation — anticipating the panel's hardest questions.
- Stress-testing a research result obtained via `caselaw-search`.

Examples:

- "Müvekkilim haksız tahrik indirimi alacak — karşı tarafın itiraz edebileceği
  Yargıtay kararları neler?"
- "Tasarrufun iptali davası açtık, eşin muvazaalı mal kaçırması savımız var.
  Karşı yönde içtihat var mı?"
- "İdari sözleşmenin feshini istiyoruz; Danıştay'ın bu fesih sebebini kabul
  etmediği kararlar olabilir mi?"

## When Not to Use

- **Initial research** — use `caselaw-search` first to establish the position,
  then bring it here for stress-testing.
- **Drafting the actual response brief** — this skill surfaces opposing
  authority; drafting belongs to `litigation-legal` or similar.
- **Devil's-advocate on questions of fact** — this is doctrinal, not factual.
- **Adversarial profiling of a specific judge** ("how does Judge X usually
  rule on…?") — out of scope for both policy and accuracy reasons.

## Communication Rules

- **Mirror the user's language.** Turkish → Turkish, English → English.
  Default to Turkish (Turkish litigators are the primary audience).
- Be **honest about strength**. If you cannot find genuine counter-authority,
  say so explicitly — do not manufacture conflict. "Karşı yönde belirgin bir
  içtihat bulamadım, yalnızca aşağıdaki kararlar konuyu daraltıyor" is a
  valid finding.
- **Separate** counter-authority (rulings that go the other way) from
  **qualifications** (rulings that limit / scope the position) — both
  matter but they aren't the same threat.
- Cite every authority verbatim: court + chamber + esas no + karar no +
  tarih + collection.
- Flag HGK / CGK / içtihadı birleştirme decisions as binding when they
  appear on either side.

## Workflow

### 1. Restate the position precisely

Before searching, restate the user's legal claim in doctrinal terms:

- Identify the **rule** (statute / doctrine the position relies on)
- Identify the **elements** that must be proven
- Identify the **weakest element** — counter-authority usually attacks
  the most contested element, not the rule itself

If the user's framing is colloquial, translate to doctrine first (see
`caselaw-search` for the colloquial → doctrinal table). Surface your
translation so the user can confirm.

### 2. Flip and search

Run two complementary searches:

**a. Negation search** — `search` with the position inverted:

- Position: "haksız tahrik indirimi uygulanır" →
  search: "haksız tahrik indirimi uygulanmaz" / "haksız tahrik koşulları gerçekleşmemiş"
- Position: "tasarrufun iptali şartları oluşmuş" →
  search: "tasarrufun iptali şartları oluşmamış" / "muvazaa iddiasının reddi"

**b. Element-attack search** — `search` for the weakest element being absent:

- "haksız tahrik" weakest element = "haksız fiil" or "kusur dengesi" →
  search those specifically with `expand=false`

Use `daire` and `yil_min`/`yil_max` filters when scoping helps; the
goal is **relevant counter-authority**, not breadth.

### 3. Expand from the strongest counter-case

Pick the most directly contradictory ruling from step 2 and:

- `get_full_text(point_id)` — verify the holding actually contradicts
  the user's position (not just on facts but on doctrine)
- `find_similar(point_id)` — neighboring rulings on the same contra position
- `find_citing_cases(esas_no)` — has this contra-line been adopted or
  abandoned downstream?

### 4. Categorize the threat

For each finding, classify:

| Threat level | Definition | Example |
|---|---|---|
| **Binding contra** | HGK/CGK/İBK that goes the other way | Position likely loses unless distinguishable on facts |
| **Persuasive contra** | Chamber ruling that goes the other way | Argue distinguishability; address head-on |
| **Qualifier** | Same line but narrower scope than user assumed | Refine the position; do not abandon |
| **Outdated** | Older counter-line later overruled or eroded | Note for completeness; pre-empt opponent citing it |
| **Distinguishable** | Different facts, opposing party will still try to cite | Prepare distinguishing brief in advance |

### 5. Present the threat map

Lead with the **strongest counter-authority** and the **best response to it**.
Lawyers planning a hearing want to know the worst case first, then the
next-worst, then qualifications. Structure:

```
1. [Binding contra]   — full citation, holding, distinguishing argument
2. [Persuasive contra] — same
3. [Qualifiers]        — same
4. [Distinguishable / weak] — brief mention only
```

If the search returned no real counter-authority, say so plainly and
recommend the user proceed with confidence — but flag that absence of
authority is not the same as authority for the position.

## Helpful information

- Provider: arguman.ai (Istanbul, Türkiye)
- Auth: OAuth 2.1 with Dynamic Client Registration + PKCE
- Coverage: nearly 15 million rulings across 8 collections (Yargıtay,
  Danıştay, AYM, AİHM multilingual HUDOC, Uyuşmazlık, BGH)
- Cross-lingual retrieval — counter-authority searches in Turkish also
  surface ECtHR (EN/FR) and BGH (DE) rulings that contradict the position
- This skill is best used **after** `caselaw-search` has established a
  baseline position to flip
- Documentation: https://arguman.ai/docs/mcp
- Support: iletisim@arguman.ai
