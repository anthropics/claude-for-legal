---
name: gdpr-basics
description: >
  Minimum GDPR compliance for Finnish startups — privacy notice, cookie consent,
  first DPA with processors, DSAR process. Routes to Velvoite for DPIA if needed.
  Use when asking "do we need a privacy policy", "GDPR for our startup",
  "cookie consent", or "first DPA".
argument-hint: "[describe your product and what user data you handle]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /fi-startup-legal:gdpr-basics

1. Load profile. Check AI flag and Velvoite availability.
1.5. **Input gate:** Before running the checklist, confirm the user has described their product or data processing activity. If no description is provided, ask: "What does your product do and what personal data does it collect or process?" Do not run a generic checklist without understanding the use case.

  If the description includes any of the following, **halt and route before proceeding:**
  - Special category data (health, biometric, genetic, racial/ethnic origin, religion, political opinion, sexual orientation)
  - Children's data (users under 16)
  - Automated decision-making with legal or significant effects (GDPR Art. 22)
  - Large-scale systematic monitoring of individuals

  For any of these: "This processing activity triggers heightened GDPR requirements. Run `/eu-legal:privacy-triage` for a mandatory DPIA assessment before proceeding with this checklist."
2. Run the GDPR basics checklist, tailored to the described use case.
3. If DPIA or AI Act check needed: run `/eu-legal:privacy-triage` (DPIA assessment), `/eu-legal:pia-generation` (full PIA), or `/eu-legal:dpa-review` (DPA review).

---

## GDPR startup minimum

### Do you need to comply?
Yes, if you: (a) are established in the EU, or (b) offer goods/services to EU individuals, or (c) monitor EU individuals. Finnish startups: always yes.

**Live verification:** Call `mcp__velvoite__get_eu_regulation_article("gdpr", "13")` for privacy notice requirements and `mcp__velvoite__get_eu_regulation_article("gdpr", "28")` for processor DPA requirements. Fetch the returned section_url values to verify the requirement lists below against current EUR-Lex text.

### Privacy notice (tietosuojaseloste) — **Mandatory**
Required by GDPR Art. 13/14 before collecting personal data. Must cover:
- [ ] Who you are (controller identity + contact)
- [ ] What data you collect
- [ ] Why (purposes) and legal basis for each purpose (Art. 6: contract / legitimate interests / consent / legal obligation)
- [ ] How long you keep it
- [ ] Who you share it with (categories of recipients, transfers outside EU)
- [ ] Data subject rights (access, erasure, correction, portability, objection)
- [ ] Right to complain to Tietosuojavaltuutettu (Finnish DPA)
- [ ] Contact for DPO (if appointed) or privacy queries

### Cookie consent
ePrivacy Directive (implemented in Finland via Sähköisen viestinnän palvelulaki) requires consent before non-essential cookies. Functional/strictly necessary cookies: no consent required. Analytics, advertising, tracking: consent required before setting.

### First processor DPA
If you use any service that processes your users' personal data on your behalf (Stripe, Mailchimp, AWS, Google Analytics, Intercom, Mixpanel, etc.) — you need a Data Processing Agreement with them. Most have standard DPAs available in their terms/settings.

### Record of Processing Activities (RoPA) — **Conditional**
Required if: >250 employees, OR processing is not occasional, OR high-risk. Most early startups: not required, but good practice to maintain one.

### DSAR process
Have a named person or email address for data subject requests. Must respond within 1 month (extendable to 3 for complex requests).

### Breach notification
Personal data breach must be notified to Tietosuojavaltuutettu within 72 hours if likely to result in risk to individuals. Keep a breach register regardless.

### DPIA — **Context-dependent**
Required when processing is likely to result in high risk (Art. 35). Run `/eu-legal:privacy-triage` to assess whether your processing triggers a mandatory DPIA.

---

## Velvoite depth (optional)

If you're an AI startup processing significant personal data, or building a product involving profiling, automated decisions, or biometrics — add your Velvoite API key for:
- Full DPIA workflow (GDPR Art. 35 mandatory trigger check)
- AI Act compliance check (risk classification, FRIA)
- Enforcement intelligence (what Finnish/EU startups get fined for)

Free 30-day trial at velvoite.eu.

---

## Limitations — read before using this output

- **Not a compliance certificate.** A completed checklist does not mean your product is GDPR-compliant. A qualified lawyer must review your actual privacy notice, DPA templates, and consent mechanisms before publication.
- **Not covered:** International data transfers (Chapter V — SCCs/BCRs), Art. 32 security measures, sector-specific rules (eHealth, financial services), EDPB guidelines, and enforcement decisions.
- **For depth:** DPIA assessment → `/eu-legal:privacy-triage`. Full PIA → `/eu-legal:pia-generation`. DPA review → `/eu-legal:dpa-review`.
- **Not legal advice.** Outputs are legal support tools. No attorney-client relationship or privilege is created by using this skill.

GDPR compliance is ongoing, not a one-time checklist. Finnish Tietosuojavaltuutettu (TSV) can issue fines up to €20M or 4% of global turnover.
