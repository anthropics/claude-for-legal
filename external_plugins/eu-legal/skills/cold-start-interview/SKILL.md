---
name: cold-start-interview
description: >
  Set up the eu-legal plugin — learns your company profile, entity type,
  jurisdiction, and regulatory posture, then writes the practice configuration.
  Run on first install, when CLAUDE.md is missing or has placeholders, or when
  your company profile changes. Use --redo to force a re-run, or
  --check-integrations to re-probe Velvoite, Slack, and Drive only.
argument-hint: "[--redo] [--check-integrations]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:cold-start-interview

1. Check `~/.claude/plugins/config/eu-legal/CLAUDE.md` — if populated and no `--redo`, confirm before overwriting.
2. Run the interview workflow below.
3. Probe integration availability (Velvoite, Slack, Google Drive).
4. Write `~/.claude/plugins/config/eu-legal/CLAUDE.md` (create parent directories as needed). Show summary. Offer first task.

---

## --check-integrations

Re-probes Velvoite, Slack, and Google Drive. Updates `## Available integrations` only. Does not re-interview. Use after connecting or disconnecting an MCP server.

Report ✓ only if a tool call actually succeeded. Never report ✓ based on `.mcp.json` declarations alone — that misleads users into thinking something is wired up when it isn't.

---

## Migration

On first run after a plugin update: if a populated CLAUDE.md (no `[PLACEHOLDER]` markers) exists at the old cache path (`~/.claude/plugins/cache/eu-legal/<version>/CLAUDE.md` for any version) but not at the config path, copy it to `~/.claude/plugins/config/eu-legal/CLAUDE.md` and tell the user what was migrated. Then offer `--check-integrations` to verify integrations still work.

---

## Interview workflow

Ask questions conversationally — one topic per message. Never dump all questions at once.

### 1. Company basics

Ask:
> "Let's set up eu-legal. What's your company name, and which EU country is your primary legal home — where you're incorporated or where your main regulatory supervisor sits?"

Then ask: which other EU member states does the company operate in? (Optional — press Enter to skip.)

### 2. Entity type

Ask:
> "What type of regulated entity are you? This determines which regulatory obligations surface in your skills."

Present as a numbered list:
1. Credit institution (bank, savings bank, credit union)
2. Payment institution
3. E-money institution
4. CASP — crypto-asset service provider (MiCA)
5. Investment firm (MiFID II)
6. AIFM — alternative investment fund manager
7. UCITS management company
8. Insurance undertaking
9. Reinsurance undertaking
10. Other — general EU company, no FSA supervision

Save the machine-readable code:
| Selection | Code |
|---|---|
| 1 | `credit_institution` |
| 2 | `payment_institution` |
| 3 | `e_money_institution` |
| 4 | `casp` |
| 5 | `investment_firm` |
| 6 | `aifm` |
| 7 | `ucits` |
| 8 | `insurance` |
| 9 | `reinsurance` |
| 10 | `other` |

### 3. Velvoite integration

Ask:
> "Do you have a Velvoite account? (velvoite.eu — free 30-day trial available.) Velvoite provides the EU finreg corpus that powers the regulatory skills. Without it, those skills give general guidance only."

**If yes:** Ask for their workspace ID (found at app.velvoite.eu → Settings → Workspace). Ask which env var holds their API key (default: `VELVOITE_API_KEY`).

Then probe: run `echo "${VELVOITE_API_KEY:+set}"`. If it prints `set`, call `mcp__velvoite__get_company_profile()`.

- **On success:** mark Velvoite ✓. Import actor roles directly from `profile.actor_roles` (a dict of regulation code → list of role codes). Use this mapping for display names in the config:

  | Code | Display name |
  |---|---|
  | `gdpr` | GDPR |
  | `ai_act` | AI Act |
  | `dora` | DORA |
  | `mica` | MiCA |
  | `mifid2` | MiFID II |
  | `aml` | AML/CFT |
  | `crd_crr` | CRD/CRR |
  | `psd` | PSD |
  | `idd` | IDD |
  | `solvency_2` | Solvency II |
  | `sfdr` | SFDR |
  | `emir` | EMIR |
  | `bmr` | BMR |

  Skip step 4 (manual actor role entry) — roles are imported.

- **On failure (env var not set):** Tell the user: "`VELVOITE_API_KEY` is not set. Add it to your `.envrc` (`export VELVOITE_API_KEY=vv_your_key_here`) and run `direnv allow`, then re-run `/eu-legal:cold-start-interview`." Mark Velvoite ✗. Continue interview; set all actor roles to `[PLACEHOLDER]`.
- **On failure (API error):** Tell the user what went wrong in one line and how to fix it (bad key → re-create at app.velvoite.eu/account; no profile → finish workspace setup). Mark Velvoite ✗. Continue.

**If no:** Mark Velvoite ✗. Offer: "No account yet? Free 30-day trial at velvoite.eu." Proceed to step 4.

### 4. Actor roles (only if Velvoite probe did not succeed)

Ask one regulation at a time. Skip any where the entity type makes it clearly inapplicable (e.g., don't ask about MiCA for a credit institution that isn't a CASP).

- **GDPR:** controller / processor / both controller and processor / not applicable
- **DORA:** financial_entity / ict_third_party / critical_ict / not applicable
- **AI Act:** provider / deployer / both provider and deployer / not applicable
- **MiCA:** casp / issuer / not applicable
- **AML/CFT:** obliged_entity / not applicable
- **MiFID II:** investment_firm / not applicable

### 5. Active practice areas

Ask:
> "Which practice areas should be active? I'll suppress skills for areas you don't use."

Show as checkboxes. Default: all checked (user can uncheck).
- [ ] Commercial contracts
- [ ] Privacy / GDPR + AI Act
- [ ] Employment
- [ ] Corporate governance
- [x] Regulatory (always recommended — this is where Velvoite depth lives)

### 6. Legal team

Ask:
> "How is your legal team structured?"

Options:
1. Solo GC or in-house lawyer
2. Small in-house team (2–5 lawyers)
3. In-house team + regular outside counsel

If outside counsel: ask for firm name(s) and jurisdiction/practice area coverage (one question, free text).

### 7. Integration probe

After the interview, probe Slack and Google Drive by attempting a lightweight read on each. Report honestly using ✓ / ✗ / ⚪.

---

## Write the config

Read the CLAUDE.md template from the plugin directory. Replace every `[PLACEHOLDER]` marker with the answer from the interview. Keep all headings, table structure, and comment blocks byte-for-byte identical — other skills parse specific heading text.

Write to `~/.claude/plugins/config/eu-legal/CLAUDE.md` (create parent dirs: `mkdir -p ~/.claude/plugins/config/eu-legal/`).

Show a brief summary of what was written (company name, entity type, Velvoite status, active practice areas).

---

## Practice-area configs (optional deeper setup)

The base profile captures entity type, jurisdiction, and regulatory posture. For each practice area, a separate config file enables more detailed, practice-specific behaviour:

| Practice area | Config path | How to populate |
|---|---|---|
| Privacy / GDPR + AI Act | `~/.claude/plugins/config/eu-legal/privacy.md` | `/eu-legal:privacy-cold-start` (Plan 2) |
| Commercial contracts | `~/.claude/plugins/config/eu-legal/commercial.md` | `/eu-legal:commercial-cold-start` (Plan 3) |
| Employment | `~/.claude/plugins/config/eu-legal/employment.md` | `/eu-legal:employment-cold-start` (Plan 4) |
| Corporate governance | `~/.claude/plugins/config/eu-legal/corporate.md` | `/eu-legal:corporate-cold-start` (Plan 5) |

Skills work without these files — they fall back to base profile. The practice-area configs unlock detailed behaviour: DPA playbook positions, contract standard terms, works council thresholds, board structure, Finnish KHO case law notes.

Then offer:
> "Setup complete. Try:
> - `/eu-legal:obligations` — what regulatory obligations apply to you
> - `/eu-legal:deadlines` — upcoming compliance dates in the next 90 days
> - `/eu-legal:reg-watch` — what changed in EU regulation this week"

---

## Disclaimer

Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
