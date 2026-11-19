# Broker-Dealer Compliance Plugin

Reviews the files a small US broker-dealer builds every day — customer onboarding, Rule 506(c) verification, offering files, communications, intermediary payments, outside activity notices, issuer diligence, books-and-records maps, and tokenized security controls — against the firm's own written procedures. Built for the compliance and deal staff of a firm doing private placements and tokenized (digital asset) securities, and for the technology vendor that serves it.

**Every output is a draft for review by a registered principal and counsel — cited, flagged, and gated — not legal advice and not a firm decision.** The plugin does the first pass: reads the file, lines it up against the firm's procedure, finds the gaps, drafts the memo, the log entry, or the question list. A registered principal reviews and decides, with counsel on the legal questions. The plugin never decides that a customer is identified, that an investor is accredited, or that anything is suitable; those decisions belong to the firm, and every output leaves that line blank for the firm to complete.

*Proposed addition to [Claude for Legal](https://github.com/anthropics/claude-for-legal). Authored by UnyKorn LLC. Not an Anthropic plugin until and unless it is accepted upstream.*

## Who this is for

| Role | Primary workflows |
|---|---|
| **Compliance staff / CCO / AML compliance officer** | Onboarding file review, communications pre-review, outside activity notices, books-and-records mapping |
| **Deal staff** | Offering file gate check, diligence memo, 506(c) verification files, intermediary payment checks |
| **Supervising principal** | Receives the gap lists, draft records, and escalations; makes the decisions |
| **Outside securities counsel** | Receives the numbered question lists |
| **Technology vendor serving the firm** | Books-and-records export specification, token controls review — as inputs to the firm's review, not substitutes for it |

## First run: cold-start

Asks for the firm name and CRD, the principals, business lines, exemptions used, the custody model, who approves communications, and where the written procedures live. Writes the firm profile every other skill reads.

```
/broker-dealer-legal:cold-start-interview
```

## Install

Once this plugin is part of the Claude for Legal marketplace:

```
/plugin marketplace add <path-to-your-claude-for-legal-checkout>
/plugin install broker-dealer-legal@claude-for-legal
```

Until then, load it from a local copy of this folder:

```
claude --plugin-dir /path/to/broker-dealer-legal
```

Install user-scoped, restart Claude Code, then run the cold-start interview.

## Skills

| Skill | Does |
|---|---|
| `/broker-dealer-legal:cold-start-interview` | Cold-start: firm profile — firm, CRD, principals, business lines, exemptions, custody model, procedures index, offering gates, communications approval |
| `/broker-dealer-legal:customer-onboarding-review` | Reviews an individual (KYC) or entity (KYB) file for completeness against the firm's customer identification and beneficial ownership procedures; outputs gaps and a draft file memo |
| `/broker-dealer-legal:accredited-verification` | Walks a Rule 506(c) verification file — basis claimed, evidence, line-up — and drafts the decision record with the decision left blank |
| `/broker-dealer-legal:offering-file-review` | Checks an offering file gate by gate (issuer file, screening, bad actor questionnaires, counsel review, principal approval, filings) and lists what blocks opening |
| `/broker-dealer-legal:communications-review` | Pre-reviews a draft public or investor communication; flags promissory, unbalanced, or unapproved statements; outputs a marked-up list and a draft approval-log entry |
| `/broker-dealer-legal:intermediary-compensation-check` | Sorts a proposed payment to an introducer, finder, or partner: transaction-based or not, recipient registered or not; lists structures to raise with counsel. Never computes a contingent fee |
| `/broker-dealer-legal:outside-activity-notice` | Drafts a registered person's outside business activity notice and flags when private securities transaction treatment may apply |
| `/broker-dealer-legal:diligence-memo` | Turns an issuer due diligence questionnaire and documents into a draft diligence memo with red flags and open items |
| `/broker-dealer-legal:books-and-records-map` | Maps a described system's records to what the firm must make and keep, and specifies an export |
| `/broker-dealer-legal:token-controls-review` | Reviews a tokenized security design (allow-list, holder cap, lock-up, freeze, forced transfer, compliance role, custody or possession election) and lists questions for the principal and counsel |

## Rules and citation verification

The plugin cites a deliberately short list of provisions, and only where one applies:

Securities Exchange Act of 1934 Section 15(a) · Securities Act Rules 501(a), 506(b), 506(c), 506(d) · Regulation Best Interest · Regulation S-P · Exchange Act Rules 17a-3 and 17a-4 · FINRA Rules 2010, 2090, 2111, 2210, 3110, 3270, 3280, 3310, 4511, 5122, 5123 · 31 CFR 1023.220 · 31 CFR 1010.230

**Skills do not quote rule text or state thresholds, deadlines, or retention periods from memory.** Each skill is instructed to fetch the current text from the source — the FINRA rulebook at finra.org, sec.gov, or ecfr.gov — tag what it checked and when, confirm the rule is still in force in that form, and say so in the reviewer note when it could not. A rule reference that was not checked is a pointer for the reviewer, never a conclusion. Issues under provisions outside the list (state law, other SEC and FINRA rules, custody and resale rules for digital asset securities, tax, non-US law) are named as topics and routed to counsel without a citation.

## Hard gates

- **No firm decisions.** No output says a customer is identified, an investor is accredited, a communication or offering is approved, or an investment is suitable.
- **No contingent compensation for unregistered persons.** No skill expresses, computes, or drafts a fee that depends on a transaction closing, or on the amount raised, for a person who is not registered. The request is routed to `/broker-dealer-legal:intermediary-compensation-check`, which frames the question for counsel.
- **No custody characterization.** The plugin records the position the firm and its counsel have taken and lists the facts; it does not label an arrangement.

## Integrations

Ships with the general bucket of connectors in `.mcp.json`:

- **Slack** — search messages, read channels, find discussions
- **Google Drive** — search, read, and fetch documents

Rule sources (finra.org, sec.gov, ecfr.gov) are public websites read by web fetch; no connector is required. Where a source refuses automated fetches, paste the current text and the skill will tag it `[user provided]`.

## How it relates to the rest of Claude for Legal

This plugin follows the upstream house format: `.claude-plugin/plugin.json`, `skills/<name>/SKILL.md`, a template `CLAUDE.md` with the shared guardrails, user configuration at `~/.claude/plugins/config/claude-for-legal/broker-dealer-legal/CLAUDE.md`, and the shared `company-profile.md` one level up. The reviewer note, source tags, decision tree, and retrieved-content rules are the upstream ones, narrowed for a broker-dealer.

- **`regulatory-legal`** watches regulators and diffs new rules against a policy library. Pair them: when `regulatory-legal` flags a change to a rule on this plugin's list, update the firm's written procedure, then re-run the affected review here. This plugin does not monitor feeds.
- **`corporate-legal`** runs transaction diligence, closing checklists, and board consents from the issuer's or acquirer's side. This plugin is the intermediary's side of a private placement: the broker-dealer's own file on the issuer, the investors, and its own conduct. An issuer's counsel would use `corporate-legal`; the placement agent's staff would use this.
- Neither of those plugins is required. If the shared company profile already exists, this plugin's cold-start reads it and skips the company questions.

## How it learns

The firm profile at `~/.claude/plugins/config/claude-for-legal/broker-dealer-legal/CLAUDE.md` improves as you use the plugin. When an output says "generic checklist used — firm procedure not provided," that is the setting to fill in. Re-run setup, edit the file directly, or tell a skill to record a change.

## Notes

- The firm's written procedures are the value. Without them, every review is a generic checklist and says so at the top.
- A vendor can run the books-and-records and token skills, but the output is addressed to the firm. The vendor does not decide what the firm's records are or who holds custody.
- This plugin has no scheduled agents and no hooks. Nothing runs unless someone invokes it.
- US federal and FINRA provisions only. Non-US investors, issuers, and offerings are flagged and routed to counsel.

## Configuration

Your configuration is stored at `~/.claude/plugins/config/claude-for-legal/broker-dealer-legal/CLAUDE.md` and survives plugin updates — you only run setup once.

## Licence

Apache License 2.0 — see `LICENSE`. Copyright 2026 UnyKorn LLC. Offered as a proposed addition to the Apache-2.0 licensed Claude for Legal collection; see `CONTRIBUTING-NOTE.md`.
