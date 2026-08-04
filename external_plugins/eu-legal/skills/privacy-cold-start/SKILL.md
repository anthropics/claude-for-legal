---
name: privacy-cold-start
description: >
  Set up the privacy practice config — DPA playbook positions, DSAR process,
  DPIA triggers, and AI Act posture. Writes ~/.claude/plugins/config/eu-legal/privacy.md.
  Run after cold-start-interview, or when privacy practice settings change.
argument-hint: "[--redo]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:privacy-cold-start

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If placeholders, stop: "Run `/eu-legal:cold-start-interview` first."
2. Check `~/.claude/plugins/config/eu-legal/privacy.md` — if populated and no `--redo`, confirm before overwriting.
3. Run the interview below. Write the config. Show summary.

---

## Interview

Ask one topic per message.

### 1. Role
"Are you primarily a data controller, processor, or both for the personal data you handle?"

### 2. Data categories
"What categories of personal data do you process? (e.g. employee data, customer financial data, transaction data, biometric data, health data)"

### 3. DPO
"Do you have a Data Protection Officer? (Required if: public authority; large-scale systematic monitoring; large-scale special category data processing.) Name or 'not required' or 'not yet appointed'."

### 4. Lead supervisory authority
"Which supervisory authority is your lead authority under GDPR Art. 56? Your lead SA is in the EU member state where your main establishment is (where central administration or main processing decisions are made).

Examples: Tietosuojavaltuutettu (Finland), BfDI or the relevant LfDI (Germany), CNIL (France), DPC (Ireland), AP (Netherlands).

⚠️ **ICO (UK) is NOT an EU supervisory authority.** Post-Brexit, ICO operates under UK GDPR and cannot be the Art. 56 lead SA for EU-incorporated entities. List ICO only if your entity is incorporated in the UK or has significant UK operations requiring UK GDPR compliance alongside EU GDPR."

### 5. DPA playbook — processor side
"When a customer sends you their DPA (you are the processor), what are your standard positions on:
- Audit rights (e.g. questionnaire first, on-site max once/year with 30 days notice)
- Breach notification window to controller (e.g. 24h / 48h / 72h)
- Subprocessor change notice period (e.g. 14 days / 30 days)
- Data location (EU only / EU + adequacy decisions / unrestricted)
- Deletion timeline on termination (e.g. 30 days / 90 days)"

### 6. DPA playbook — controller side
"When you send a DPA to a vendor (you are the controller), what do you require:
- Audit rights
- Breach notification window (GDPR Art. 33 requires you to notify your DPA within 72h of becoming aware)
- Subprocessor restrictions
- Data location"

### 7. DSAR process
"For handling Data Subject Access Requests:
- How do you verify identity? (e.g. ID document + account email match)
- List the systems where personal data lives (every system — this becomes the search checklist)
- Who handles routine requests vs. who escalates complex ones?"

### 8. DPIA triggers
"Beyond GDPR Art. 35 mandatory triggers, do you have any additional internal DPIA triggers? (e.g. new vendor with access to >10,000 records, any AI system using personal data, any cross-border transfer to new country)"

### 9. AI Act posture
"Do you use or deploy any AI systems that process personal data? List them if yes. For each: what does it do, who are the data subjects? (This maps to EU AI Act Annex III high-risk categories: credit scoring, fraud detection, employment decisions, insurance underwriting, identity verification.)"

---

## Write config

Read `eu-legal/privacy.md` template. Replace all `[PLACEHOLDER]` markers with interview answers. Write to `~/.claude/plugins/config/eu-legal/privacy.md` (create parent dirs).

Show summary. Offer: "Try `/eu-legal:dpa-review` to review an incoming DPA, or `/eu-legal:privacy-triage` to check if a new processing activity needs a DPIA."

---

## Disclaimer

Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
