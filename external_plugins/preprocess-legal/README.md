# preprocess-legal

Transparent local pre-processing for document-heavy legal work. Addresses
[issue #100](https://github.com/anthropics/claude-for-legal/issues/100): when
Claude reads a folder of PDFs (court filings, contracts, scanned exhibits), each
file is read in its native form — slow and token-heavy for large, scanned, or
poorly-OCR'd matters.

This plugin intercepts each read, extracts the text locally, and hands the model
clean text instead of the raw PDF — **but only when the extraction is
trustworthy.** A degraded scan is never silently passed through as hollow text.

## How it works

A `PreToolUse` hook fires on every `Read`. For a routed PDF it:

1. **Routes** — is this file in scope? (opt-in, by type and optional size floor)
2. **Extracts** — text-native content via `pdfplumber`
3. **Scores** — per-document confidence, as an explainable breakdown:
   - `coverage` — fraction of pages that produced real text
   - `density` — mean characters per page vs. a text-native baseline
   - `legibility` — fraction of characters that are actually readable
   - `overall = (weighted coverage + density) × legibility` — legibility is a
     **quality veto**, so a page full of plausible-looking mojibake cannot pass
     on quantity alone
4. **Gates** — at/above `threshold` → pass; below → withhold
5. **Redirects** — rewrites the Read's `file_path` (`updatedInput`) to point at:
   - a **clean-text** file on a pass, or
   - an **honest withheld-marker** on a fail — text that *says* the document was
     held back and why, never hollow content masquerading as the document

Because the engine writes the exact bytes the model reads, "refuse to pass
degraded output silently" is literal, not advisory. The redirect is transparent
to the model (confirmed on Claude Code ≥ v2.1.190, CLI + Cowork + Desktop).

## Design notes

- **Per-file, not per-folder.** Hooks fire per tool call — reading 20 PDFs fires
  20 times, each with one path. Routing is per document.
- **Fails safe.** A missing/broken config, a missing `pdfplumber`, or an
  encrypted/corrupt PDF never breaks a Read — the hook either withholds (fail
  closed) or passes the original through (fail open on unexpected errors).
- **Swappable backend.** Only `engine/extract.py` imports `pdfplumber`. The
  scoring and gate logic operate on a plain `ExtractionResult`, so slice 2's OCR
  cascade plugs in behind the same interface without touching the gate.
- **Warm cache.** Extraction is synchronous (the redirect target must exist when
  the read returns). Re-reading an unchanged file hits a cache keyed on
  path + size + mtime.

## Status

**Slice 1** — text-native extraction + confidence gate + withheld-marker.
**Deferred:** OCR fallback cascade for low-confidence scans (slice 2), caching
tuning for heavy synchronous matters (slice 3).

## Install & enable

1. Install the extraction dependency: `pip install -r requirements.txt`
2. Create a config (see `.claude-plugin/config-template.md`) and set `enabled: true`
3. Point the hook at it via `PREPROCESS_LEGAL_CONFIG`, or use the default path

## Develop

```
python -m pytest tests/     # pure scoring + gate tests, no pdfplumber required
```

## Open questions (tracked on issue #100)

- Scoped to a practice-area plugin, or closer to Cowork itself? Built behind a
  clean interface either way.
- Real-matter tuning: scanned-vs-text ratio, latency tolerance, and which
  structural losses (tables, exhibit stamps, Bates numbers, redactions) matter
  most — awaiting the reporter's answers.
