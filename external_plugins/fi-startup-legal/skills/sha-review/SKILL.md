---
name: sha-review
description: >
  Review a Finnish shareholders' agreement (osakassopimus) against the seriesseed.fi
  market standard — three-tier leaver, pre-emption rights, drag-along, tag-along,
  ROFR, anti-dilution, board composition, protective provisions. Use when reviewing
  a SHA, asking "is our SHA standard", or preparing for a funding round.
argument-hint: "[paste or describe the SHA, or 'seriesseed-check' for a quick checklist]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
seriesseed_template_version: "4.0"
---

# /fi-startup-legal:sha-review

1. Load profile. If placeholders, stop.
2. **Detect operating mode:**
   - **Mode 1 — Document review:** User has provided actual SHA text. Run a term-by-term comparison against the seriesseed.fi v4.0 standard.
   - **Mode 2 — Checklist only:** No document provided. Output the standard checklist with market-standard terms. Label output: "[CHECKLIST MODE — no document reviewed. Reflects market standard only, not your actual SHA.]"
   State the mode explicitly at the start of the output.
3. Call `mcp__velvoite__get_finnish_statute("OYL", "3")` for share transfer and buyback rules.
4. Call `mcp__velvoite__get_finnish_statute("OYL", "9")` for shareholder rights.
5. **Output preamble (before any RAG table):**
   > ⚠️ **Attorney review required before signing.** This is a template comparison — not a legal opinion. GREEN status means "matches market standard", not that a clause is enforceable or suitable for your investor relationship. A Finnish startup lawyer must review before you sign.
6. Review against seriesseed.fi v4.0 standard. Output: term-by-term RAG status.

---

## seriesseed.fi standard checklist

**Note on sources:** seriesseed.fi SHA terms are private contractual standards, not statute — no EUR-Lex verification applies. For the OYL statutory rights referenced (pre-emption, share transfer restrictions), call `mcp__velvoite__get_eu_regulation_article` is not relevant here; instead call `mcp__velvoite__get_finnish_statute("OYL", "3")` to verify the Finnish Companies Act provisions on share transfers.

The Startup Foundation (startup-saatio.fi) seriesseed.fi templates are the Finnish market standard for seed rounds. This skill reflects **seriesseed.fi v4.0 (2024 update)** — verify the current version at seriesseed.fi before a live deal. `last_verified: 2026-06-01`. Key 2024 changes: three-tier leaver, KYC/AML provisions.

Review each section:

### Leaver provisions
| Term | Market standard | Status |
|---|---|---|
| Good Leaver definition | Leaves voluntarily after cliff, or involuntary without cause | |
| Early Leaver definition | Leaves before cliff OR voluntarily before 2 years | |
| Bad Leaver definition | Termination for cause, material breach, non-compete violation | |
| Good Leaver share price | Fair market value | |
| Early/Bad Leaver share price | Subscription price (nominal) | |
| Vesting schedule | 4 years, 1-year cliff | |
| Acceleration | Single-trigger (involuntary termination post-M&A) market standard | |

### Transfer restrictions
| Term | Market standard | Notes |
|---|---|---|
| Pre-emption right | Existing shareholders have right to buy before external transfer | OYL §3 allows; must be in SHA or yhtiöjärjestys |
| ROFR (right of first refusal) | At same price as third-party offer | |
| Drag-along threshold | >2/3 of all shares (seriesseed.fi 4.0 standard) — 75% is above standard and more protective for founders; anything below 2/3 is aggressive | Must be in SHA; cannot be in yhtiöjärjestys alone |
| Tag-along | Minority can join any majority sale at same price | |
| Lock-up | Typically 12 months post-IPO if applicable | |

### Investor protections
| Term | Market standard | Notes |
|---|---|---|
| Anti-dilution | Broad-based weighted average (not full ratchet) | Full ratchet is aggressive — flag |
| Pro-rata right | Investor can maintain % in future rounds | |
| Information rights | Quarterly financials, annual audited accounts | |
| Board seat | Lead investor gets 1 board seat for rounds >€500k | |
| Protective provisions | New share issuance, M&A, budget approval require investor consent | List the standard matters |

**Cross-border governing law check:** If any investor is foreign, confirm the SHA specifies governing law explicitly. A SHA drafted under Finnish OYL assumptions with Swedish or UK governing law creates significant interpretation gaps. Flag for outside counsel if governing law is ambiguous.

### 2024 seriesseed.fi updates
The Startup Foundation updated templates in 2024 to add:
- KYC/AML representations from investors
- Sanctions screening obligations
- Three-tier leaver (replacing two-tier) — check if the SHA being reviewed uses three-tier or older two-tier format

---

## What this skill does NOT do

- **Foreign-law SHAs**: Applies Finnish law framing only. For English-law, Swedish-law, or US Delaware SHAs, route to a specialist.
- **Post-seed terms**: Covers seriesseed.fi seed-stage standard. Series A and later rounds use different market terms.
- **Enforceability assessment**: RAG status means deviation from market standard — not that a clause is legally void or enforceable.
- **Tax implications of leaver provisions**: Good/bad leaver treatment has TVL implications — run `/fi-startup-legal:esop-designer` for tax framing.
- **Legal advice**: Outputs are legal support tools. No attorney-client relationship or privilege is created.

---

## Guardrail

SHA review identifies deviations from market standard. Whether a deviation is acceptable depends on the specific investor relationship and negotiating dynamics. Attorney review required before signing. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill. GREEN status is not legal clearance to sign.
