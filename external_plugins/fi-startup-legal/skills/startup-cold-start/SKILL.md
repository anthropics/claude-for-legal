---
name: startup-cold-start
description: >
  Set up the fi-startup-legal plugin — learns your startup's stage, founders,
  funding, grants, and legal setup, then writes the practice profile. Run on
  first install or when your situation changes. Use --redo to re-run.
argument-hint: "[--redo]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /fi-startup-legal:startup-cold-start

1. Check `~/.claude/plugins/config/fi-startup-legal/CLAUDE.md` — if populated and no --redo, confirm before overwriting.
2. Probe integrations: call `mcp__velvoite__search_finnish_statutes("test")` to verify Finlex works, and `mcp__velvoite__search_finnish_companies("test")` to verify PRH works. Report ✓/✗ for each. Velvoite: check `VELVOITE_API_KEY` env var — if set, call `mcp__velvoite__get_finnish_company` to verify PRH+Velvoite both work. Report all three as one probe step.
3. Run interview below. Write profile. Offer first action.

---

## Interview

One topic per message. Plain language — no legal jargon.

### 1. Company basics
"Let's set up fi-startup-legal. What's your company name? And have you incorporated yet?"

If yes: ask for business ID (Y-tunnus). Call `mcp__velvoite__get_finnish_company(business_id)` to verify and pre-fill name, registration date, address. Confirm: "Found [name], registered [date]. Is this right?"

If no: set stage = pre-incorporation.

### 2. Stage
"What best describes where you are?"
1. Just an idea — haven't incorporated yet
2. Incorporated, haven't raised money yet
3. Raised a pre-seed or seed round (€0–2M)
4. Raised a Series A or larger

### 3. Founders
"Who are the founders? (Name + role + approximate equity % for each. It's okay if not finalised.)"

### 4. Business Finland grants
"Have you received any Business Finland funding? (R&D grant, TUTLI, Tempo, etc.)"
If yes: ask which grants and approximate amounts. This affects IP transfer restrictions.

### 5. Legal setup
"Do you have a shareholders' agreement (osakassopimus) in place yet?"
If yes: ask if it follows the seriesseed.fi format or something else.

"Do you have an option/ESOP pool?"
If yes: ask size (%) and whether it's TVL §66 options or a §66a share issue scheme.

### 6. Outside counsel
"Are you working with a law firm? (Fondia, Nordic Law, Dottir, Lexia, or other — or none yet.)"

### 7. AI product flag
"Is your product or service AI-based? (Determines whether EU AI Act compliance is relevant for you.)"
If yes: offer Velvoite API key for AI Act depth. Note: free 30-day trial at velvoite.eu.

**If no Velvoite API key:** Profile setup completes without corpus backing. Note to the user:
> "Skills will work using EU law knowledge, but statute lookups (Finnish TSL, OYL, TVL §66) and EU regulation verification (GDPR Art. 28, DORA Art. 30) will use training data rather than live sources. For legally-sensitive decisions, verify citations at finlex.fi and eur-lex.europa.eu. Add `VELVOITE_API_KEY` to your `.envrc` for live verification — free 30-day trial at velvoite.eu."

---

## Write profile

Read the CLAUDE.md template. Replace all [PLACEHOLDER] markers. Write to `~/.claude/plugins/config/fi-startup-legal/CLAUDE.md`.

Show summary. Then offer based on stage:
- Pre-incorporation: "Try `/fi-startup-legal:oy-setup` to start the incorporation wizard."
- Incorporated, no SHA: "Try `/fi-startup-legal:founder-agreement` to set up your co-founder agreement."
- Post-seed: "Try `/fi-startup-legal:sha-review` to review your shareholders' agreement."
- Series A: "Try `/fi-startup-legal:term-sheet-review` to review an incoming term sheet."

---

## Disclaimer

This plugin provides legal support, not legal advice. Outputs do not constitute legal advice, create an attorney-client relationship, or confer legal professional privilege. Attorney review is recommended before signing any document or making any filing.
