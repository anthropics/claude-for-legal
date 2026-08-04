---
name: customer-contract
description: >
  First customer contract checklist for a Finnish startup — liability cap,
  IP ownership, GDPR data processing clause, governing law (Finnish default),
  SLA. Reviews a contract or helps draft key terms. Use when signing first
  customer, asking "what should our customer contract say", "is this contract
  fair", or reviewing a customer's paper.
argument-hint: "[describe the deal or paste the contract]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /fi-startup-legal:customer-contract

1. Load profile.
2. Run the review/checklist. Route to `/fi-startup-legal:gdpr-basics` if data processing is involved.

---

## Key terms checklist

### IP ownership
We (the startup) must retain all IP in our product/platform. The customer gets a license to use, not ownership. Key question: does the contract try to claim ownership of anything we build?
- [ ] Our product IP clearly remains ours
- [ ] Customer data remains theirs (we are processor)
- [ ] Customisations/configurations: who owns them? (We should, unless paid bespoke work)

### Liability
- [ ] Limitation of liability clause present
- Our recommended starting position: liability capped at fees paid in 12 months preceding the claim
- Customer may push for higher cap for data breaches — consider accepting for: personal data breaches (GDPR exposure), death/personal injury (cannot be limited in Finland)
- [ ] Mutual limitation (not one-sided against us)
- [ ] Exclusion of consequential loss (indirect damages, lost profits)

### GDPR / data processing
Does the customer send us personal data to process on their behalf?
If yes: a Data Processing Agreement (DPA) is required by GDPR Art. 28 — route to `/fi-startup-legal:gdpr-basics`

### Governing law
Finnish law default for Finnish customers. For international customers:
- EU customers: Finnish law or the customer's local law — avoid US governing law
- Note: Finnish courts apply Finnish law; disputes in Finnish courts are in Finnish

### SLA (if relevant)
- Uptime commitment: 99.5% monthly (industry standard for SaaS)
- Scheduled maintenance windows excluded
- Remedies: service credits, not cash

### VAT

- [ ] Does the startup need to charge VAT on this contract?
  - VAT registration mandatory if annual turnover exceeds **€15,000** (2026 threshold, AVL §3)
  - Below threshold: registration optional but can be beneficial if customers are VAT-registered businesses
  - First contract should clarify whether prices are VAT-inclusive or VAT-exclusive; state VAT registration number (ALV-numero) if registered
  - Foreign customers (EU business-to-business): reverse charge mechanism applies — no Finnish VAT charged, customer accounts for VAT in their country

### Termination
- Notice period: 30-90 days for convenience
- Data return/deletion obligations on termination
- Survival of confidentiality provisions

---

## Guardrail

Customer contracts are legally binding. This checklist covers key issues for a standard SaaS or service contract. For large enterprise contracts, pilot programs, or regulated sector customers, have a lawyer review before signing. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
