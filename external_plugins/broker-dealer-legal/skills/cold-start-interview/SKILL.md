---
name: cold-start-interview
description: >
  Cold-start interview — builds the broker-dealer firm profile (firm name, CRD,
  principals, business lines, exemptions used, custody model, who approves
  communications, where the written procedures live) and writes it to the
  plugin config. Use on fresh install, when CLAUDE.md still has [PLACEHOLDER]
  markers, when reconfiguring (--redo), or when re-checking what connectors
  and rule sources are actually responding (--check-integrations).
argument-hint: "[--redo [section] | --full | --check-integrations]"
---

# /cold-start-interview

1. Check `~/.claude/plugins/config/claude-for-legal/broker-dealer-legal/CLAUDE.md`. If a populated CLAUDE.md (no `[PLACEHOLDER]` markers) exists at `~/.claude/plugins/cache/claude-for-legal/broker-dealer-legal/*/CLAUDE.md` but not at the config path, copy it to the config path and tell the user what was migrated. If `--check-integrations`, skip the interview — re-run only the Part 0 `What's connected?` check and rewrite the `## Available integrations` table.
2. Use the interview workflow below. Part 0 first (role + integrations), then the firm, business lines, custody model, procedures, gates, communications approval, escalation.
3. Write `~/.claude/plugins/config/claude-for-legal/broker-dealer-legal/CLAUDE.md` (creating parent directories as needed).

When probing integrations: only report ✓ if a tool call actually succeeded. Configured-but-untested connectors are ⚪. Never report ✓ based on `.mcp.json` declarations alone.

---

## Purpose

Every other skill in this plugin reviews something against how THIS firm works: its approved business lines, its written procedures, its approvers. This interview captures that once, so a customer file is checked against the firm's customer identification procedure rather than a generic checklist, and an escalation names a real person.

**This output is a draft for review by a registered principal and counsel. It is not legal advice.** The profile records what the firm tells it. It does not verify registrations, approve business lines, or characterize the firm's custody position, and it is never a decision on identification, accreditation, or suitability — those belong to the firm.

## Cold-start check

Read `~/.claude/plugins/config/claude-for-legal/broker-dealer-legal/CLAUDE.md`:
- **Does not exist** → start the interview.
- **Contains `<!-- SETUP PAUSED AT: -->`** → greet the user and offer to resume from that section.
- **Contains `[PLACEHOLDER]` markers but no pause comment** → offer to start fresh or resume from where the placeholders begin.
- **Populated** → already configured; skip unless `--redo`.

The template structure lives at `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` — use it as the section scaffold.

## Check for the shared company profile

Look for `~/.claude/plugins/config/claude-for-legal/company-profile.md`.

- **If it exists:** read it, show a one-line confirmation, and skip the company questions.
- **If it doesn't exist:** ask the company questions (name, what the firm does, size, jurisdictions, regulators, risk appetite, key people) and write them to the shared profile, then continue. Tell the user the other Claude for Legal plugins will read it.

## Install scope check

If the working directory is inside a project (not the user's home directory), say once:

> **Heads up — it looks like this plugin may be project-scoped, which means I can only read files in [current directory]. If you'll want me to read investor or offering files from elsewhere, install user-scoped instead. You can continue with project scope, but you'll need to move files into this folder.**

## Before the interview starts

Show this preamble first:

> **`broker-dealer-legal` is for the compliance and deal staff of a small US broker-dealer doing private placements and tokenized securities, and for the technology vendor that serves it.** Not your area? `/legal-builder-hub:related-skills-surfacer`.
>
> **2 minutes** gets you your role, the firm, and who the principal and counsel are. **15 minutes** adds business lines, exemptions, the custody model, the procedures index, the offering gates, and communications approval.
>
> Quick or full? (Upgrade any time with `/broker-dealer-legal:cold-start-interview --full`.)

Do not read the user's home-directory `~/CLAUDE.md` or other personal memory to pre-populate the interview. The only inputs are the user's typed answers and documents they point at or paste in.

## Interview pacing

- **Assume the answer exists somewhere.** Written supervisory procedures, the firm's membership agreement, the approval matrix, the retention schedule — ask for a link or a paste before asking the user to type from memory.
- **2-3 answerable prompts per turn**, counting subparts.
- **Ask and wait** for typed answers and file pointers. Offer "skip for now" and record the gap.
- **Before writing:** list every skipped question and ask whether to fill it or leave a placeholder. Never write the profile with silent gaps.
- **Pause and resume.** On "pause," write a partial config with `<!-- SETUP PAUSED AT: [section] — run /broker-dealer-legal:cold-start-interview to resume -->` at the top and `[PENDING]` on unanswered fields.

**Verify user-stated facts as they come up.** If the user gives a CRD number, a rule number, an exemption, or a registration category, record it as `[user provided — verify]` unless they point you at the source (for example the firm's BrokerCheck page, which you may fetch if the user asks). If a stated rule number is not on the plugin's list in `## Rules in scope`, say so rather than writing it into the profile as though the plugin covers it. A wrong fact written here propagates into every later output.

## The interview

### Part 0: Who's using this, and what's connected

**Who's using this?**

> Who'll be using this plugin day to day?
>
> 1. **Lawyer or legal professional** — the firm's counsel or their staff.
> 2. **Registered principal or compliance staff** — you supervise or approve.
> 3. **Deal or operations staff** — you assemble files that a principal approves.
> 4. **Technology vendor staff** — you build or run the system the firm uses; you are not the firm.

For 2, 3, or 4, say once:

> Every output here is a draft for a registered principal and counsel. I'll lay out what a file contains, what's missing, and the questions to raise. I won't tell you a customer is identified, an investor is accredited, or an investment is suitable — those are the firm's decisions, made by the people you're about to name.

For 4, add:

> As a vendor, two things to keep in view: what your system does on the firm's behalf may itself raise registration questions, and the firm's records and customer information are the firm's. I'll flag both where they come up, as questions for the firm's principal and counsel.

**What's connected?** Test, don't assume:

- **Rule sources.** Try fetching one page from each of finra.org (rulebook), sec.gov, and ecfr.gov. Report ✓ only on a successful fetch. If a source refuses automated fetches, report ✗ and note the fallback: the user pastes current rule text, or references are tagged `[rule text not checked — verify]`.
- **Document storage** and **Slack** — ✓ only on a successful tool call; otherwise ⚪ "configured but not verified."

### Part 1: The firm

- Firm name and CRD number (ask for the BrokerCheck link rather than a typed number if they have it).
- The principals table: CCO, supervising principal for offerings, communications approver, AML compliance officer, outside securities counsel, and a backup for each. Record registrations as the firm states them.
- Who the user's own work goes to.

*(Feeds every skill's escalation points.)*

### Part 2: Business lines and exemptions

- What business lines is the firm approved for? Ask for a paste from the firm's own records rather than a description.
- Which offering exemptions does the firm work under — Rule 506(b), Rule 506(c), others? Record what the firm names. Do not infer an exemption from a description of the deal, and do not describe what an exemption requires.
- Customer types: individuals, entities, institutions. Does the firm treat any as retail customers?
- Does the firm make recommendations? *(Decides whether skills raise Regulation Best Interest and FINRA Rule 2111 questions for the principal.)*

### Part 3: Custody and settlement model

- Does the firm hold customer funds or securities? Record the firm's own statement.
- Where do investor funds go, and who is the party that holds them?
- For tokenized securities: who controls keys, who holds the compliance or administrative role on the token contract, and what has the firm and its counsel determined about custody or possession? Record the position and the date counsel last confirmed it.

If the answers to this part are uncertain or the user is guessing, write `[PENDING — confirm with counsel]` and tell the user: "I've left the custody section pending. `/broker-dealer-legal:token-controls-review` will produce the question list for counsel rather than assume an answer."

### Part 4: Procedures index

For each row in the template's `## Written procedures index`, ask for the file location, last-updated date, and owner. Offer to read each and record a one-paragraph summary of what it requires, tagged `[firm procedure — <name>, dated X]`.

### Part 5: Offering gates

Walk the six default gates (issuer file, screening, bad actor questionnaires, counsel review, principal approval, filings). For each: what evidence does the firm require, and who signs off? Let the firm reorder, rename, add, or remove gates.

### Part 6: Communications approval

Who approves before first use, where the approval log lives, which channels are in use, and any standing house rules or prohibited phrases.

### Part 7: Escalation

> When a review finds something that needs a decision — a gap in an identification file, a red flag on an issuer, a payment to someone who isn't registered — who does it go to, and how? Give me a name for the principal route and a name for the counsel route.

### Quick start path

Ask only Part 0, Part 1, and the first two questions of Part 2. Write the config with `[DEFAULT]` on gates (the six defaults) and `[PENDING]` on procedures and custody. Tell the user which skills will run generically until the procedures index is filled.

## Writing the profile

Write the completed profile to the config path using the template's section order. Keep the template's `## Rules in scope`, `## Decisions that belong to the firm`, `## Outputs`, and `## Shared guardrails` sections verbatim — they are not interview questions and the user's answers do not change them.

## Escalation points during setup

- **To counsel:** any uncertainty about approved business lines, which exemption applies to what the firm does, or the custody position. Do not resolve these in the interview.
- **To the principal:** any procedure the firm cannot locate. Record it as missing; a missing written procedure is a finding for the principal, not something to draft around.
- **Vendor users:** if the vendor's description of its own role includes handling investor funds, operating transfer controls, or being paid in relation to transactions, flag: "This is a question for the firm's counsel under Exchange Act Section 15(a) and possibly other registration categories outside what this plugin cites." Do not characterize the vendor's status.

## After writing

Show a short summary of the profile and offer a first task:

> - **Review a customer file** — `/broker-dealer-legal:customer-onboarding-review`
> - **Check an offering file gate by gate** — `/broker-dealer-legal:offering-file-review`
> - **Review a draft communication** — `/broker-dealer-legal:communications-review`
> - **Check a proposed payment to an introducer** — `/broker-dealer-legal:intermediary-compensation-check`

Close with the changeability note: the config is a plain-text file at `~/.claude/plugins/config/claude-for-legal/broker-dealer-legal/CLAUDE.md`; edit it directly, or re-run with `--redo <section>`.
