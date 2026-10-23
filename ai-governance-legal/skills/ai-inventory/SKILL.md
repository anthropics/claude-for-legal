---
name: ai-inventory
description: >
  EU AI Act per-system inventory — track each AI system's role (provider,
  deployer, importer, distributor, authorized representative, product
  manufacturer) and risk tier (prohibited, high-risk, limited, minimal,
  GPAI, GPAI+systemic). Role and tier are assessed per system, not per
  company. Use when the user says "ai inventory", "add an ai system",
  "what systems do we have", "classify this ai system", "eu ai act
  register", or "ai system registry".
argument-hint: "[list | add | edit <id> | classify <id> | show <id>]"
---

# /ai-inventory

## When this runs

The user wants to manage their AI system inventory under the EU AI Act. The
core idea the skill exists to enforce: **role and tier are per-system, not
per-company.** A single organization can be a *provider* of System A, a
*deployer* of System B, and an *importer* of System C. Each combination
triggers a different set of obligations under the AI Act. The inventory
exists so those assessments are tracked where you can find them — the
obligations themselves are derived in conversation, not from a table.

## What to do

1. **Read the config.** Read
   `~/.claude/plugins/config/claude-for-legal/ai-governance-legal/CLAUDE.md`.
   If it doesn't exist or still has `[PLACEHOLDER]` markers, direct the user
   to `/ai-governance-legal:cold-start-interview` first.

2. **Read the inventory.** Inventory lives at
   `~/.claude/plugins/config/claude-for-legal/ai-governance-legal/ai-systems.yaml`.
   If it doesn't exist, create it with an empty `systems:` list when the
   first `add` runs.

3. **Dispatch on the argument:**

   - No argument, or `list` → show the inventory table (see **List** below).
   - `add` → run the **Add** flow.
   - `edit <id>` → show the current record, ask what to change, update one
     field, confirm, write.
   - `classify <id>` → run the **Classification walk-through** on an
     existing record, updating role, tier, role_basis, and tier_basis.
   - `show <id>` → show the full record.

4. **On list, offer the dashboard:**
   "Want the full dashboard? Filter by status / tier / EU nexus / owner.
   Say the word."

5. **Close every action with a hook into the lawyer's work.**
   After any write, say:
   > Recorded. When you're ready to walk through obligations for this
   > system, just ask — I'll do it in-conversation and flag where the AI
   > Act article mapping needs your verification. I don't derive
   > obligations from a table because the mapping is complex and changing.

## List format

Render as a compact table:

| ID | Name | Owner | Status | EU nexus | Role | Tier | Next review |
|----|------|-------|--------|----------|------|------|-------------|
| sys-001 | Resume screening | HR / Jamie | in_production | yes | deployer | high_risk | 2026-08-01 |
| sys-002 | Email drafting assistant | IT / Priya | in_production | no | deployer | limited | 2026-12-01 |

Under the table, show counts by tier and a line: "N systems flagged for
review within 30 days."

## Add flow (interview)

Ask, one field at a time (or accept a paste). The required fields are
`name`, `owner`, `description`, `status`, `eu_nexus`. The rest can be
deferred — say so explicitly: "you can come back to classification with
`/ai-governance-legal:ai-inventory classify <id>`."

1. **Name.** Short label for the system.
2. **Owner.** Person or team accountable for it day-to-day.
3. **Description.** One or two sentences. What does it do, and against
   what data?
4. **Status.** `planned | in_development | in_production | deprecated`.
5. **EU nexus.** Is the system placed on the market or put into service in
   the EU, used by a deployer established or located in the EU, or used by
   a provider or deployer established or located outside the EU to produce
   output that is used in the EU? If any of these are true, EU AI Act
   analysis applies (Article 2(1)). The Act applies in Iceland,
   Liechtenstein and Norway only once it is incorporated into the EEA
   Agreement; check its EEA status before relying on a nexus with those
   countries alone.
6. **Proceed to classification?** Offer to run the walk-through now, or
   skip and come back later.

Assign an ID: `sys-NNN` where NNN is the next integer in the file.

## Classification walk-through

The walk-through produces `role`, `role_basis`, `tier`, `tier_basis`. Both
bases are tagged `[verify against current AI Act text]` — not because the
skill is hedging, but because the article mapping is complex and the AI
Act is still phasing in. The lawyer owns verification.

### Step 1: Role

> **Who does what to this system?**

Options, with the distinguishing test:

- **Provider** — you develop it (or have it developed) and place it on the
  EU market or put it into service under your own name or trademark.
- **Deployer** — you use it under your own authority, not for personal
  non-professional use. (Most common inside companies.)
- **Importer** — you are located or established in the EU and place on
  the EU market an AI system that bears the name or trademark of a person
  established outside the EU.
- **Distributor** — you make an AI system available on the EU market
  without being the provider or importer.
- **Authorized representative** — you are located or established in the
  EU and have received and accepted a written mandate from a provider to
  perform and carry out on its behalf its obligations and procedures under
  the AI Act.
- **Product manufacturer** — you place an AI system on the EU market or
  put it into service together with your product and under your own name
  or trademark. If the AI system is a high-risk AI system that is a safety
  component of a product covered by the Union harmonisation legislation
  listed in Section A of Annex I, and it is placed on the market together
  with the product under your name or trademark, or put into service under
  your name or trademark after the product has been placed on the market,
  you are treated as the provider of that high-risk AI system (Article
  25(3)). Otherwise, test the provider role above and the dual-role flag
  below.

**Dual-role flag.** If the user substantially modifies a vendor system
(fine-tunes on their own data, changes the intended purpose, rebrands),
they may become a **provider** of the modified system even if they started
as a deployer. Call this out when they describe any modification beyond
configuration. `[verify against current AI Act text — Article 25, provider
obligations and substantial modification]`

Write the role. Write `role_basis` in one sentence.

### Step 2: Tier

> **What does the system do, and does the use case fall into a regulated
> category?**

Check in order:

**A. Article 5 prohibited practices.** `[verify against current AI Act
text — Article 5]`

Summaries, not definitive text:
- Subliminal techniques beyond a person's consciousness, or purposefully
  manipulative or deceptive techniques, with the objective or effect of
  materially distorting behavior by appreciably impairing informed
  decision-making, causing a decision the person would not otherwise have
  taken in a manner that causes or is reasonably likely to cause significant
  harm
- Exploiting vulnerabilities (age, disability, specific social or economic
  situation) with the objective or effect of materially distorting behavior,
  causing or reasonably likely to cause significant harm
- Social scoring, by any actor, public or private, leading to detrimental or
  unfavorable treatment in unrelated social contexts, or treatment
  unjustified or disproportionate to the social behavior or its gravity
- Real-time remote biometric ID in publicly accessible spaces for law
  enforcement (narrow exceptions)
- Biometric categorization inferring race, political opinions, union
  membership, religious or philosophical beliefs, sex life, or sexual
  orientation (labeling or filtering of lawfully acquired biometric datasets,
  and categorizing biometric data in law enforcement, excepted)
- Emotion recognition in the workplace or education (medical and safety
  exceptions)
- Untargeted scraping of facial images from the internet or CCTV to create
  or expand facial recognition databases
- Assessing or predicting the risk of a person committing a criminal offence
  based solely on profiling or on personality traits and characteristics
  (support for a human assessment already based on objective and verifiable
  facts directly linked to a criminal activity excepted)
- From 2 December 2026: generating or manipulating realistic images, video,
  audio or similar material of an identifiable person's intimate parts, or of
  an identifiable person engaged in sexually explicit activities, without
  that person's freely given, specific, informed, unambiguous and explicit
  consent; generating or manipulating child sexual abuse material or
  performance (Directive 2011/93/EU, Article 2(c) and (e)), except where a
  "without right" defence applies under national law (Article 5(1a) and (1b)
  limit the scope)

If matched → tier is `prohibited`. Flag the use case as stop and route to
the governance team's prohibited-practice workflow.

**B. Annex III high-risk areas.** `[verify against current AI Act text —
Annex III]`

Summaries:
1. Biometrics, where the use is permitted by law: remote biometric
   identification (not one-to-one verification), biometric categorization
   according to sensitive or protected attributes or characteristics based on
   the inference of those attributes or characteristics, and emotion
   recognition
2. Critical infrastructure (safety components in the management and
   operation of critical digital infrastructure, road traffic, supply of
   water / gas / heating / electricity)
3. Education and vocational training (access, admission or assignment;
   evaluation of learning outcomes; assessing the appropriate level of
   education; monitoring prohibited behavior during tests)
4. Employment, worker management, self-employment access: recruitment and
   selection; decisions affecting terms of work, promotion or termination;
   task allocation based on individual behavior or personal traits;
   monitoring and evaluating performance and behavior
5. Essential private and public services (eligibility for, or granting,
   reducing, revoking or reclaiming, public assistance benefits and services,
   by or for public authorities; creditworthiness or credit scoring of
   individuals, other than detecting financial fraud; risk assessment and
   pricing for life/health insurance; evaluating and classifying emergency
   calls, emergency dispatch and emergency healthcare patient triage)
6. Law enforcement, where permitted by law, for use by or on behalf of law
   enforcement authorities, or by Union institutions, bodies, offices or
   agencies in their support (risk of a person becoming a crime victim;
   polygraphs and similar tools; reliability of evidence in investigating or
   prosecuting crime; risk of offending or re-offending not solely on the
   basis of profiling; assessing personality traits and characteristics or
   past criminal behavior; profiling in detecting, investigating or
   prosecuting crime)
7. Migration, asylum, border control, where permitted by law, for use by or
   on behalf of competent public authorities or by Union institutions,
   bodies, offices or agencies (polygraphs and similar tools; risks,
   including security, irregular migration or health risks, posed by a
   person who intends to enter or has entered; examination of asylum, visa
   and residence permit applications and related complaints; detecting,
   recognizing or identifying persons, other than verification of travel
   documents)
8. Administration of justice and democratic processes (assisting a judicial
   authority, or alternative dispute resolution, in researching and
   interpreting facts and the law and applying the law to facts; influencing
   the outcome of elections or referenda or voting behavior, other than tools
   whose output natural persons are not directly exposed to)

If matched → tier is `high_risk`. Note the Annex III area and subsection.

**C. GPAI.** `[verify against current AI Act text — Article 51 and
surrounding]`

- **GPAI:** model trained on broad data at scale, designed for generality,
  capable of competently performing a wide range of distinct tasks.
- **GPAI + systemic risk:** cumulative compute > 10^25 FLOPs, or designated
  by the Commission.

**D. Limited risk.** Chatbots interacting with natural persons, systems
generating synthetic audio, image, video or text content, deepfakes, text
generated or manipulated by AI and published to inform the public on
matters of public interest, and biometric categorization systems outside
both Article 5 and Annex III point 1(b): transparency obligations apply
(Article 50, subject to its exceptions, such as assistive standard editing
and text that has undergone human review or editorial control under a
person's editorial responsibility). Emotion recognition and biometric
categorization according to sensitive or protected attributes or
characteristics based on the inference of those attributes or
characteristics, where outside Article 5, are `high_risk` under Annex III
point 1 where their use is permitted by law (step B); the Article 50(3)
notice duty applies to them as well, except as Article 50(3) provides for
systems permitted by law to detect, prevent or investigate criminal
offences.

**E. Minimal risk.** Everything else.

Write the tier. Write `tier_basis` in one sentence, citing the article or
Annex entry that matched, tagged `[verify against current AI Act text]`.

### Step 3: Recommendations

Offer three next steps:
1. "Want me to walk through obligations for this system? I'll do it in
   conversation — I don't derive them from a table."
2. "Want to run `/ai-governance-legal:aia-generation` to produce a full
   impact assessment?"
3. "Want to set a next review date? I'll add it to the inventory."

## Record format

```yaml
systems:
  - id: sys-001
    name: "Resume screening tool"
    owner: "HR / Jamie"
    description: "Filters inbound CVs against job criteria"
    status: in_production          # planned | in_development | in_production | deprecated
    eu_nexus: true                 # placed on the market or put into service in the EU, deployer established or located in the EU, or output used in the EU (Article 2(1))
    role: deployer                 # provider | deployer | importer | distributor | authorized_rep | product_manufacturer
    role_basis: "We license from VendorX and deploy internally [verify against current AI Act text]"
    tier: high_risk                # prohibited | high_risk | limited | minimal | gpai | gpai_systemic
    tier_basis: "Annex III(4)(a) — employment, recruitment selection [verify against current AI Act text]"
    obligations_assessed: false
    obligations_note: "To assess: as deployer of a high-risk system — human oversight, input data quality, monitoring, record-keeping, informing workers, FRIA (Article 27(1)) for an Annex III system outside point 2 if the deployer is a body governed by public law or a private entity providing public services, and for any deployer of an Annex III point 5(b) or (c) system; see Articles 26 and 27 [verify against current AI Act text]"
    next_review: "2026-08-01"
    review_trigger: "on substantial modification or annually"
    created: "2026-05-11"
    updated: "2026-05-11"
```

## Why this skill does NOT auto-derive obligations

The inventory stores role, tier, and the basis for each. It does NOT
contain a hardcoded role × tier → obligations table.

When the user asks "what are my obligations for System X?", the skill
does the analysis **in conversation**, tagged `[verify]`, and routes to
`/ai-governance-legal:aia-generation` for the formal impact assessment
if needed.

This is deliberate:
- Article mapping is complex and the AI Act is phasing in: as amended by
  Regulation (EU) 2026/1744, Article 113 applies the high-risk rules
  (Chapter III, Sections 1 to 3) from 2 December 2027 for Annex III systems
  and 2 August 2028 for Annex I systems, and Article 111 sets transitional
  deadlines running to 31 December 2030.
- Confident-and-wrong on a compliance obligation ends up in a board memo.
- The inventory is a registry for the lawyer. The lawyer owns the
  obligation analysis.

## Guardrails

- **Never classify silently.** The classification walk-through must be
  visible; do not auto-classify from a system description.
- **`[verify]` tags stay.** They are not hedging — they are the point.
  Do not strip them in outputs.
- **Flag substantial modification.** Whenever a system is modified beyond
  configuration, prompt the user to re-run `/ai-inventory classify` —
  modification can change role.
- **Don't declare obligations from a table.** If asked, do the analysis
  in conversation and route to `/aia-generation` for anything that needs
  a formal record.
