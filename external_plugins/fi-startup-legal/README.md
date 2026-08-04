# fi-startup-legal — Finnish Startup Legal Toolkit for Claude Code

A Claude Code / Cowork plugin for Finnish startup founders and early ops hires.
Covers the pre-seed through Series A journey. Backed by live Finnish statute data
(Finlex), the Finnish Trade Register (PRH), and optional Velvoite EU finreg corpus.

Built by [Silly Pilot Oy](https://velvoite.eu).

## What it covers

| Skill | What it does |
|---|---|
| `/fi-startup-legal:startup-cold-start` | Setup interview — writes your practice profile |
| `/fi-startup-legal:oy-setup` | OY incorporation wizard — yhtiöjärjestys, osakassopimus, PRH registration |
| `/fi-startup-legal:founder-agreement` | Co-founder mechanics + vesting + IP assignment |
| `/fi-startup-legal:ip-assignment` | IP audit — founders, employees, contractors, BF grants |
| `/fi-startup-legal:sha-review` | SHA review against seriesseed.fi standard |
| `/fi-startup-legal:term-sheet-review` | Term sheet in plain language — red/amber/green per term |
| `/fi-startup-legal:esop-designer` | TVL §66 vs §66a decision + 2026 reform status + AGM mechanics |
| `/fi-startup-legal:vesting-calculator` | Vesting schedule + leaver calculations |
| `/fi-startup-legal:bf-grant-check` | Business Finland IP restrictions + clawback risk |
| `/fi-startup-legal:first-hire-contract` | First employment contract checklist |
| `/fi-startup-legal:non-compete-check` | Non-compete validity + compensation check |
| `/fi-startup-legal:customer-contract` | First customer contract review |
| `/fi-startup-legal:startup-nda` | NDA review + generation (LSL framework) |
| `/fi-startup-legal:board-minutes` | OYL-compliant board minutes |
| `/fi-startup-legal:gdpr-basics` | GDPR minimum for startups |

## What makes it different

Skills call **live Finnish statute data** via Finlex MCP — TSL notice periods,
OYL share rules, TVL §66 ESOP provisions — not training-data guesses.
Company lookups go to **live PRH data**. The esop-designer reads the live TVL §66
statute text to determine whether the 2026 option tax reform (proposed: taxation
at sale rather than exercise) has been enacted, and presents rules accordingly.

## Install

**Step 1 — Clone the repo** (if you haven't already):
```bash
git clone https://github.com/Velvoite/law-for-eu
cd law-for-eu
```

**Step 2 — Add the marketplace** (in Claude Code or terminal):
```bash
claude plugin marketplace add /path/to/law-for-eu
```

**Step 3 — Install the plugin:**
```bash
claude plugin install fi-startup-legal@velvoite-legal
```

**Step 4 — Restart Claude Code** (mandatory — close and reopen).

## Setup

```
/fi-startup-legal:startup-cold-start
```

## Requirements

- Claude Code or Cowork
- No API key required for core features (Finlex + PRH are public)
- Velvoite API key for GDPR/AI Act depth (free trial: velvoite.eu)

## License

Apache 2.0 — Copyright 2026 Silly Pilot Oy
