# eu-legal — EU Legal Operations for Claude Code

A Claude Code / Cowork plugin for legal teams at EU-regulated financial institutions. One setup, one profile, complete EU legal stack.

Built by [Silly Pilot Oy](https://velvoite.eu) — the team behind [Velvoite](https://velvoite.eu), the EU financial regulation compliance platform.

---

## What it covers

| Practice area | Skills |
|---|---|
| **Regulatory** | Obligations, deadlines, reg-watch, reg-gap-analysis, enforcement-intelligence |
| **Privacy / GDPR + AI Act** | DSAR response, DPA review, PIA/DPIA generation, triage, policy monitor, AI Act compliance |
| **Commercial** | Contract review, NDA review, vendor agreement review (incl. DORA ICT), escalation, playbook |
| **Employment** | Worker classification, termination review, works council check, leave review, international expansion |
| **Corporate** | Entity compliance (OY/GmbH/SAS/BV), board minutes, M&A diligence, closing checklist |

---

## Why it's different

Most legal plugins give you generic templates. eu-legal is backed by the **Velvoite EU finreg corpus** — enforcement decisions, obligation databases, and court case law (Finnish KHO, German administrative courts) across DORA, MiCA, GDPR, AI Act, MiFID II, AML, Solvency II and more.

In practice:
- `vendor-agreement-review` pulls live DORA Art. 30 ICT third-party obligations inline
- `enforcement-intelligence` shows what your entity type actually gets fined for — with case citations
- `reg-gap-analysis` scores gaps by enforcement frequency, not just article text
- `termination-review` cites Finnish TSL and German KSchG notice periods from the actual statutes

Skills work without a Velvoite account (general EU law guidance). With one they give corpus-backed answers.

---

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
claude plugin install eu-legal@velvoite-legal
```

**Step 4 — Restart Claude Code** (mandatory — close and reopen).

---

## Setup

Run the cold-start interview once — takes about 10 minutes:

```
/eu-legal:cold-start-interview
```

It captures your entity type (credit institution, payment institution, CASP, etc.), primary jurisdiction (Finland, Germany, etc.), regulatory posture, and active practice areas. Everything else flows from there.

For full Velvoite corpus depth, add your API key to `.envrc`:
```bash
export VELVOITE_API_KEY=vv_your_key_here
```

Free 30-day trial at [velvoite.eu](https://velvoite.eu).

---

## Skills at a glance

### Regulatory
| Skill | What it does |
|---|---|
| `/eu-legal:obligations` | Obligations scoped to your entity type and actor roles, sorted by enforcement frequency |
| `/eu-legal:deadlines` | Upcoming compliance dates (default 90-day horizon) |
| `/eu-legal:reg-watch` | What changed in EU regulation this week |
| `/eu-legal:reg-gap-analysis` | Gap analysis against any EU regulation — P1/P2/P3 prioritised |
| `/eu-legal:enforcement-intelligence` | What regulators actually fine your entity type for + KHO/German case law |

### Privacy
| Skill | What it does |
|---|---|
| `/eu-legal:dsar-response` | Walk through a DSAR and draft the response |
| `/eu-legal:dpa-review` | Review a DPA as controller or processor |
| `/eu-legal:pia-generation` | Generate a PIA or DPIA (with Art. 35 mandatory trigger check) |
| `/eu-legal:privacy-triage` | Does this processing need a DPIA? Routes to right next step |
| `/eu-legal:policy-monitor` | Detect drift between privacy policy and actual practice |
| `/eu-legal:ai-act-compliance` | AI system risk classification + FRIA + GDPR/AI Act joint check |

### Commercial
| Skill | What it does |
|---|---|
| `/eu-legal:contract-review` | Review any commercial agreement against your playbook |
| `/eu-legal:nda-review` | NDA review under EU Trade Secrets Directive |
| `/eu-legal:vendor-agreement-review` | Vendor review with DORA Art. 30 ICT clause compliance |
| `/eu-legal:escalation-flagger` | Flag non-standard positions for escalation |
| `/eu-legal:playbook-init` | Set up your standard commercial positions |
| `/eu-legal:renewal-tracker` | Track contract renewals and cancel-by deadlines |

### Employment
| Skill | What it does |
|---|---|
| `/eu-legal:worker-classification` | Employee vs. contractor under Platform Work Directive + Finnish/German law |
| `/eu-legal:termination-review` | Termination risk assessment (TSL/KSchG/YT-laki) |
| `/eu-legal:works-council-check` | When must a works council be consulted? (YT-laki/BetrVG) |
| `/eu-legal:leave-review` | Leave entitlements under EU directives + Finnish/German law |
| `/eu-legal:international-expansion` | Hiring in a new EU country — legal checklist |
| `/eu-legal:policy-drafting` | Draft employment policies (remote work, monitoring, whistleblower) |

### Corporate
| Skill | What it does |
|---|---|
| `/eu-legal:entity-compliance` | Filing obligations for OY/GmbH/SAS/BV + national registers |
| `/eu-legal:board-minutes` | Draft board minutes (one-tier/two-tier) |
| `/eu-legal:written-consent` | Board/shareholder written resolutions |
| `/eu-legal:m-a-diligence-summary` | M&A diligence summary with EU merger control trigger check |
| `/eu-legal:closing-checklist` | Transaction closing checklist |

---

## Jurisdictions

**EU-wide baseline** — all skills apply EU directive law by default.

**Deep national support:**
- 🇫🇮 **Finland** — TSL, YT-laki, Vuosilomalaki, PRH, FIN-FSA, Finnish KHO case law via Velvoite
- 🇩🇪 **Germany** — KSchG, BetrVG, BUrlG, GmbH/AG, Handelsregister, BaFin enforcement via Velvoite

Other EU member states: skills apply EU directive minimums and route to outside counsel for national specifics.

---

## Practice area sub-configs

Each practice area has a detailed config that unlocks deeper behaviour. Populate them after the base cold-start:

```
/eu-legal:privacy-cold-start      # DPA playbook, DSAR process, AI Act posture
/eu-legal:commercial-cold-start   # Contract playbook, DORA ICT register
/eu-legal:employment-cold-start   # Workforce footprint, FI/DE-specific settings
/eu-legal:corporate-cold-start    # Entity register, board structure
```

Skills work without these — they fall back to the base profile.

---

## Requirements

- Claude Code or Cowork
- Velvoite API key for corpus-backed features (free 30-day trial at [velvoite.eu](https://velvoite.eu))

---

## License

Apache 2.0 — see [LICENSE](LICENSE).

Copyright 2026 Silly Pilot Oy.

---

## Disclaimer

Every output from this plugin is a draft for attorney review — not legal advice, not a legal conclusion, not a substitute for a lawyer. Skills are built with guardrails that reflect that: jurisdiction assumptions surfaced, conservative defaults on legal calls, explicit gates before anything is filed or relied on. A lawyer reviews, verifies, and takes professional responsibility for anything that leaves the building.
