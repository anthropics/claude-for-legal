---
name: ai-act-compliance
description: >
  EU AI Act compliance check for AI systems — risk classification
  (prohibited / high-risk / limited / minimal), FRIA generation for
  high-risk deployers, and combined GDPR + AI Act analysis for systems
  processing personal data. Pre-maps Annex III high-risk categories for
  financial institutions. Use when asking "does this AI system comply with
  the AI Act", "AI Act risk assessment", "do we need a FRIA", or describing
  an AI system.
argument-hint: "[describe the AI system and its use case]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:ai-act-compliance

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md` — entity type, AI Act actor role (provider/deployer/distributor).
2. Load `~/.claude/plugins/config/eu-legal/privacy.md` for high-risk AI systems list and FRIA approach. If missing, proceed without.
3. Run the workflow below.
4. Output is preliminary — high-risk classification and FRIA require qualified legal review.

---

## Purpose

The EU AI Act (Regulation (EU) 2024/1689, applicable from 2 August 2026 for most provisions) creates tiered obligations based on risk.

Application dates are phased:
- **Already in force — 2 February 2025:** Prohibited practices (Art. 5). If you deploy any prohibited AI system, you are already non-compliant.
- **2 August 2025:** GPAI model obligations
- **2 August 2026:** High-risk AI systems (Annex III — this is the date relevant for financial institution deployers)
- **2 August 2027:** Annex I safety component systems This skill classifies the system, maps the applicable obligations, and flags where GDPR and AI Act requirements overlap and can be addressed jointly.

## Step 1: Actor role

From base profile, confirm AI Act role:
- **Provider**: develops or places an AI system on the market (including for own use if making available externally)
- **Deployer**: uses an AI system under their own authority in a professional context
- **Distributor**: makes an AI system available without modifying it
- **Importer**: places a non-EU provider's system on the EU market

Most financial institutions are **deployers** for third-party AI (fraud detection, credit scoring tools) and **providers** for internally-developed AI.

## Step 2: Risk classification

**Live verification:** Before classifying, call `mcp__velvoite__get_eu_regulation_article("ai_act", "6")` for Annex references and `mcp__velvoite__get_eu_regulation_article("ai_act", "5")` for prohibited practices. Fetch the returned URLs to verify the classification criteria against the current EUR-Lex text. The AI Act application dates and Annex III categories are particularly important to verify against live text. If either call fails to return a section URL, fall back to `mcp__velvoite__get_eurlex_document("32024R1689")` to retrieve the full AI Act document URL and fetch the text directly.

### Prohibited (Art. 5) — hard stop

These are prohibited regardless of use case. Check:
- Real-time remote biometric identification in publicly accessible spaces (with narrow law enforcement exception)
- Social scoring systems that lead to detrimental treatment
- Subliminal manipulation causing harm
- Exploitation of vulnerabilities of specific groups
- Emotion recognition in workplace or educational institutions (except for medical/safety purposes)
- Biometric categorisation based on sensitive characteristics
- AI systems used by law enforcement for **predictive policing of individuals** based solely on profiling (Art. 5(1)(d))
- AI systems that **scrape facial images from the internet or CCTV footage** to build or expand facial recognition databases (Art. 5(1)(e))

If any prohibited practice applies: **STOP. This system cannot be deployed. Route to legal immediately.**

**Verify prohibited practices against live text:** Call `mcp__velvoite__get_eu_regulation_article("ai_act", "5")` and fetch the section_url to confirm the current prohibited practice list. The AI Act prohibited practices have been amended — live text takes precedence.

### High-risk (Art. 6 + Annexes II and III)

**Annex II** (safety components of products under EU harmonisation law): medical devices, vehicles, aviation, lifts, toys, etc. Check if the AI system is a safety component of such a product.

**Annex III — pre-mapped for financial institutions** (check all that apply):

| Use case | High-risk? | Notes |
|---|---|---|
| Credit scoring / creditworthiness assessment | Yes | Annex III §5(b) |
| Fraud detection with individual profiling/scoring | ⚠️ Depends | Annex III §5(b) only if system profiles or scores individuals — generic transaction monitoring without individual scoring is NOT high-risk under Annex III. Assess whether the system produces individual risk scores or decisions. |
| Insurance underwriting (individual risk pricing) | Yes | Annex III §5(b) |
| Employment decisions (recruitment, promotion, termination) | Yes | Annex III §4 |
| Identity verification / biometric authentication | Yes | Annex III §1 |
| Customer service chatbots | No | Limited risk (Art. 50 transparency) unless decision-making |
| Internal analytics / BI tools | No | Minimal risk |
| AML transaction monitoring (no individual scoring) | Context-dependent | Check if individual profiling is involved |

For each system described by the user: classify based on the table above and the full Annex III criteria.

### Limited risk (Art. 50)

AI systems that interact with humans (chatbots), generate content (deepfakes), or recommend content: transparency obligations only — users must be informed they are interacting with AI.

### Minimal risk

Everything else: no specific AI Act obligations (but GDPR and other law still applies).

## Step 3: High-risk compliance checklist (deployers and providers)

For each high-risk system:

**Provider obligations (Art. 9-15, 43, 49):**
- [ ] Risk management system (Art. 9): documented and ongoing
- [ ] Training data governance (Art. 10): data quality, bias assessment
- [ ] Technical documentation (Art. 11): maintained and up to date
- [ ] Automatic logging (Art. 12): events logged to the extent possible
- [ ] Transparency to deployers (Art. 13): instructions for use, capabilities, limitations
- [ ] Human oversight measures (Art. 14): designed in, not an afterthought
- [ ] Accuracy, robustness, cybersecurity (Art. 15)
- [ ] Conformity assessment (Art. 43): self-assessment (Annex VI) or third-party (notified body) depending on system type
- [ ] EU declaration of conformity (Art. 47)
- [ ] CE marking (where applicable)
- [ ] Registration in EU database (Art. 49): required before placing on market

**Deployer obligations (Art. 26):**
- [ ] Use AI system in accordance with provider's instructions for use
- [ ] Assign human oversight to competent persons
- [ ] Monitor operation, report serious incidents to provider and market surveillance
- [ ] Conduct FRIA if required (Art. 27)
- [ ] Inform affected employees where applicable (Art. 26(7))

## Step 4: FRIA (Fundamental Rights Impact Assessment)

Art. 27 FRIA is required for:
- Bodies governed by public law deploying Annex III high-risk AI
- Private operators deploying Annex III systems in areas of **Art. 27(1)**: critical infrastructure, education, employment, essential private services (credit, insurance), law enforcement support, migration, justice administration

For financial institution deployers using credit scoring, insurance underwriting, or similar: **FRIA is required**.

FRIA structure (Art. 27(2)):
1. Description of processes in which the high-risk AI will be used and its purposes
2. Time period and frequency of use
3. Categories of affected natural persons
4. Specific risks of harm to fundamental rights (non-discrimination, privacy, dignity, consumer protection)
5. Existing measures to address those risks
6. Identification of the role and responsibilities of relevant actors

## Step 5: GDPR + AI Act joint check

If the system processes personal data:
- A DPIA (Art. 35 GDPR) may be required alongside the FRIA — assess using privacy-triage logic
- Can the DPIA and FRIA be run as a joint assessment? EDPB/EAIB guidance allows this for efficiency
- Automated decision-making with legal or similarly significant effects: GDPR Art. 22 rights apply alongside AI Act Art. 14 human oversight — ensure consistency
- High-risk AI training data: GDPR applies to all personal data in training sets — Art. 6 legal basis required even for training

Recommendation: "Run `/eu-legal:pia-generation` for the DPIA component — the two assessments can be conducted simultaneously."

---

## Guardrail

This classification is preliminary. High-risk determination under Annex III requires legal review — the criteria involve interpretation and the Commission is issuing guidance. Conformity assessments for certain high-risk AI systems require notified body involvement. This output is a working document for attorney review and should not be used as a compliance certification. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.