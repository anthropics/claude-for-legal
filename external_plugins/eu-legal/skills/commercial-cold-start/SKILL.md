---
name: commercial-cold-start
description: >
  Set up the commercial contracts practice for eu-legal — learns your governing
  law preferences, dispute resolution, liability positions, sales-side and
  purchasing-side playbooks, DORA ICT provider status, and escalation thresholds.
  Writes ~/.claude/plugins/config/eu-legal/commercial.md. Run on first use or
  with --redo to refresh. Use when setting up commercial contracts, updating
  playbook positions, or before running contract-review, nda-review, or
  vendor-agreement-review for the first time.
argument-hint: "[--redo] [--check-integrations]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:commercial-cold-start

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If missing or has `[PLACEHOLDER]`, stop: "Run `/eu-legal:cold-start-interview` first — I need your base profile before setting up commercial contracts."
2. If `commercial.md` exists and is populated (no `[PLACEHOLDER]` values) and `--redo` is not passed: confirm before overwriting. "Your commercial playbook is already configured. Passing `--redo` will overwrite it. Do you want to continue?"
3. Run the interview workflow below.
4. Write `~/.claude/plugins/config/eu-legal/commercial.md`. Show summary. Offer first task: "Run `/eu-legal:contract-review` to review a contract, or `/eu-legal:nda-review` for an NDA."

---

## --redo

Force a full re-run of the interview and overwrite `commercial.md`. Use when the company's legal posture, governing law preference, or liability positions change.

---

## Interview workflow

Ask questions conversationally — one topic per message. Never dump all questions at once.

### 1. Governing law preference

Ask:
> "Which governing law does your organisation prefer for commercial contracts?"

Present as a numbered list:
1. Finnish law (Finland — Courts of Helsinki)
2. German law (Germany — choice of city)
3. English law (England & Wales) (Note: England & Wales is outside the EU post-Brexit — selecting English governing law will trigger the "non-EU governing law" escalation flag in escalation-flagger. This is a valid commercial choice but acknowledge the escalation.)
4. Swedish law (Sweden)
5. Dutch law (Netherlands)
6. French law (France)
7. Other EU member state (specify)

Save the machine-readable code:
| Selection | Code |
|---|---|
| 1 | `finnish_law` |
| 2 | `german_law` |
| 3 | `english_law` |
| 4 | `swedish_law` |
| 5 | `dutch_law` |
| 6 | `french_law` |
| 7 | `other_eu` |

### 2. Dispute resolution

Ask:
> "What's your preferred dispute resolution mechanism for cross-border contracts?"

1. Finnish courts (District Court of Helsinki / Helsinki Court of Appeal)
2. ICC arbitration (seat: Paris; or specify another seat)
3. SCC arbitration (Stockholm Chamber of Commerce — seat: Stockholm)
4. LCIA arbitration (London Court of International Arbitration — seat: London)
5. German courts (choice of city)
6. Netherlands Arbitration Institute (NAI)
7. Other (specify)

Note: Finnish courts for contracts where both parties are Finnish; ICC/SCC for cross-border EU contracts. LCIA is recommended only for English-law agreements.

Save: `dispute_resolution_preferred`, `dispute_resolution_acceptable`, `dispute_resolution_never`.

### 3. Standard liability positions

Ask:
> "Let's set your liability positions. What's your standard direct liability cap — typically expressed as a multiple of fees paid in the preceding 12 months?"

- Standard: "12 months of fees paid in the 12 months preceding the claim"
- Acceptable fallbacks (ask): higher caps for data breach / IP infringement?
- Consequential damages: excluded (standard)? Ask for carve-outs (data breach, IP, gross negligence, fraud).
- Never accept: uncapped indirect liability.

Save: `liability_direct_cap`, `liability_indirect`, `liability_carveouts`, `liability_never`.

### 4. Sales-side playbook

Ask:
> "You're selling. Walk me through your standard positions. Let's start with IP ownership — does IP created under a services agreement stay with you (licensor model) or transfer to the customer (work-for-hire)?"

Cover:
- IP ownership and background IP licence
- Audit rights (what you grant customers)
- Data processing: do you process customer personal data? (If yes: reference your DPA template)
- Termination: standard notice period, termination for cause vs. convenience
- The one deal-breaker (what you will never accept from a customer)

Save as `sales_side_playbook` with sub-fields for each position.

### 5. Purchasing-side playbook

Ask:
> "You're buying. What do you require from vendors? Let's start: do you require vendors to sign YOUR DPA as processor, or will you accept their DPA template with redlines?"

Cover:
- DPA requirement (your paper / their paper with redlines / either)
- Audit rights you require from vendors
- Subcontracting: do you require approval rights over subcontractors?
- SLA minimum: what uptime / response time do you require?
- Never accept from a vendor (e.g., vendor retains rights to use your data for training, uncapped liability waiver)

Save as `purchasing_side_playbook`.

### 6. DORA ICT provider status

**DORA ICT third-party register (Art. 28(3)):** DORA requires financial entities to maintain a register of **all contractual arrangements** with ICT third-party service providers — not only "critical" ones. Ask:
- Has your organisation identified all ICT third-party service providers (any external provider of ICT services)?
- Is a written register of all such arrangements maintained?
Note: "Critical ICT third-party service providers" (CTPPs) is a separate designation made by the joint ESA committee under DORA Art. 43 — financial entities do not self-designate providers as critical.

Ask:
> "Has your organisation set up an ICT third-party register covering all ICT service providers under DORA Art. 28(3)? (Relevant if you are a financial entity.)"

Read entity type from `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If entity type is `other`, note that DORA ICT provider obligations may not apply directly but record the answer for context.

Options:
1. Yes — we maintain a register of all ICT third-party arrangements
2. Partially — we have an informal list but no formal register
3. No — we have not yet done this exercise
4. Not applicable — not a DORA-in-scope entity

Save: `dora_ict_register_status` (one of `formal_register` / `informal_list` / `not_done` / `not_applicable`).

If the answer is 1 or 2, ask:
> "You can list your ICT third-party providers here so the vendor-agreement-review skill can flag concentration risk. Do you want to add any now? (You can always add more later.)"

Save as `critical_ict_providers` (YAML list of vendor names).

### 7. Escalation thresholds

Ask:
> "Let's set your escalation matrix. Who can approve a contract, and at what threshold?"

Cover three levels (or fewer if a smaller team):
- Junior / paralegal / contract manager: threshold in EUR, what they can approve without escalation
- Lawyer / in-house counsel: threshold in EUR
- GC / head of legal: threshold in EUR
- Board / CFO: above GC threshold

Ask separately: automatic escalation triggers (regardless of EUR value):
- Any contract with governing law outside the EU?
- Any contract with a vendor that processes personal data outside the EU?
- Any ICT third-party agreement for a DORA-in-scope entity?
- Any contract with uncapped liability or IP assignment to the vendor?
- Liability cap below EUR [ask for threshold]?

Save: `escalation_matrix` (table), `escalation_auto_triggers` (list).

---

## Write commercial.md

After completing the interview, write `~/.claude/plugins/config/eu-legal/commercial.md`:

```markdown
# Commercial Contracts Playbook
*Written by /eu-legal:commercial-cold-start on [date]. Re-run with `--redo` to update.*

---

## Governing law and dispute resolution

**Preferred governing law:** [governing_law_preferred]
**Acceptable:** [governing_law_acceptable]
**Never:** [governing_law_never]

**Preferred dispute resolution:** [dispute_resolution_preferred]
**Acceptable:** [dispute_resolution_acceptable]
**Never:** [dispute_resolution_never]

---

## Liability positions

**Direct liability cap:** [liability_direct_cap — e.g., "12 months of fees paid in the 12 months preceding the claim"]
**Indirect / consequential damages:** [liability_indirect — e.g., "excluded, with carve-outs for data breach, IP infringement, and gross negligence"]
**Carve-outs above cap:** [liability_carveouts]
**Never accept:** [liability_never]

---

## Sales-side playbook

*Applies when we are the vendor / service provider. Usually our paper.*

**IP ownership:** [ip_ownership]
**Background IP licence:** [background_ip]
**Audit rights granted to customers:** [audit_rights_sales]
**Data processing:** [data_processing_sales]
**Termination notice period:** [termination_notice]
**Termination for convenience:** [termination_convenience]

**The one deal-breaker (sales-side):** [sales_deal_breaker]

**NDA triage positions:**
[Populated from interview — what makes an NDA GREEN, YELLOW, RED on sales-side]

---

## Purchasing-side playbook

*Applies when we are the customer / buyer. Usually their paper.*

**DPA requirement:** [dpa_requirement]
**Audit rights required from vendors:** [audit_rights_purchasing]
**Subcontracting:** [subcontracting]
**SLA minimum:** [sla_minimum]

**The one deal-breaker (purchasing-side):** [purchasing_deal_breaker]

---

## DORA ICT provider status

**ICT register status:** [dora_ict_register_status]
**Critical ICT third-party providers:**
[critical_ict_providers as YAML list]

---

## Escalation matrix

| Can approve | Without escalation (EUR) | Escalates to | Via |
|---|---|---|---|
| [role] | [EUR threshold] | [role] | [Slack/email/meeting] |
| [role] | [EUR threshold] | [role] | [method] |
| [role] | [EUR threshold] | [Board/CFO] | [method] |

**Automatic escalation triggers (regardless of EUR value):**
- [trigger list]

---

## House style

**Output language:** [language — Finnish/German/English/other]
**Where work product goes:** [Drive folder / local path / inline only]
**Renewal alerts go to:** [Slack channel / email / inline only]
```

---

## Summary and next steps

After writing `commercial.md`, show a one-paragraph summary of what was configured, then offer:

> "Your commercial playbook is ready. What's next?
> 1. **Review a contract** — paste or attach one and run `/eu-legal:contract-review`
> 2. **Review an NDA** — run `/eu-legal:nda-review`
> 3. **Review a vendor agreement** — run `/eu-legal:vendor-agreement-review`
> 4. **Update a specific playbook section** — run `/eu-legal:playbook-init`"

---

## Disclaimer

Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
