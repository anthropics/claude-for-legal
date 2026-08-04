<!--
CONFIGURATION LOCATION

User-specific configuration lives at a version-independent path:
  ~/.claude/plugins/config/eu-legal/CLAUDE.md

Rules for every skill in this plugin:
1. READ from that path. Not from this file.
2. If that file is missing or contains [PLACEHOLDER] markers, STOP. Say:
   "This plugin needs setup. Run /eu-legal:cold-start-interview — it takes about
   10 minutes and every skill depends on it."
3. cold-start-interview WRITES to that path, creating parent dirs as needed.
4. On first run after a plugin update, if a populated CLAUDE.md exists at the
   old cache path (~/.claude/plugins/cache/eu-legal/<version>/CLAUDE.md) but
   not at the config path, copy it forward before proceeding.
5. This file is the TEMPLATE. It ships with the plugin and is replaced on every
   plugin update. Never write user data here.
-->

# EU Legal Practice Profile
*Written by the cold-start interview. Run `/eu-legal:cold-start-interview` to set up.*

---

## Company

**Name:** [PLACEHOLDER]
**Entity type:** [PLACEHOLDER — credit_institution | payment_institution | e_money_institution | casp | investment_firm | aifm | ucits | insurance | reinsurance | other]
**Primary jurisdiction:** [PLACEHOLDER — e.g., Finland, Germany, Netherlands]
**Operating countries:** [PLACEHOLDER — EU member states where the company operates]
**Legal team:** [PLACEHOLDER — Solo GC | Small team 2–5 | Team with outside counsel]
**Outside counsel:** [PLACEHOLDER — Name/firm or N/A]

---

## Regulatory posture

**Velvoite workspace:** [PLACEHOLDER — workspace ID or N/A]
**Velvoite API key env var:** VELVOITE_API_KEY

**Actor roles per regulation:**

| Regulation | Actor role |
|---|---|
| GDPR | [PLACEHOLDER — controller \| processor \| joint_controller] |
| DORA | [PLACEHOLDER — financial_entity \| ict_third_party \| critical_ict \| N/A] |
| AI Act | [PLACEHOLDER — provider \| deployer \| distributor \| N/A] |
| MiCA | [PLACEHOLDER — casp \| issuer \| N/A] |
| AML/CFT | [PLACEHOLDER — obliged_entity \| N/A] |
| MiFID II | [PLACEHOLDER — investment_firm \| N/A] |

---

## Active practice areas

[PLACEHOLDER — mark which apply:]
- [ ] Commercial contracts
- [ ] Privacy / GDPR + AI Act
- [ ] Employment
- [ ] Corporate governance
- [x] Regulatory

---

## Available integrations

| Integration | Status | Notes |
|---|---|---|
| Velvoite MCP | [PLACEHOLDER ✓/✗] | Required for corpus-backed regulatory skills |
| Slack | [PLACEHOLDER ✓/✗] | For digest and alert posting |
| Google Drive | [PLACEHOLDER ✓/✗] | For document read access |

*Re-check: `/eu-legal:cold-start-interview --check-integrations`*
