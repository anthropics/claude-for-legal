---
name: cold-start-interview
description: >
  Cold-start setup — learns your state(s), audience (district counsel / family
  advocate / clinic), and house framing from seed documents (sample IEP, 504
  plan, district handbook or advocacy playbook, Title IX procedure, OCR letters
  or due-process decisions). Builds the state-aware practice profile every
  other skill reads. Use on fresh install, when CLAUDE.md still has
  [PLACEHOLDER] markers, or when re-running with --redo or --check-integrations.
argument-hint: "[--redo | --check-integrations | --quick | --full]"
---

# /cold-start-interview

1. Check `~/.claude/plugins/config/claude-for-legal/education-legal/CLAUDE.md`. If `--check-integrations`, skip the interview — re-run only the integrations probe and rewrite the `## Available integrations` table at that config path. When probing: only report ✓ if an MCP tool call actually succeeded. Configured-but-untested connectors should be marked ⚪ with a one-line how-to. Never report ✓ based on `.mcp.json` declarations alone.
2. Run the interview below (Part 0 first — role + audience + integrations — then state, then seed documents).
3. Build the jurisdictional footprint and the audience-aware framing table.
4. If a populated CLAUDE.md (no `[PLACEHOLDER]` markers) exists at `~/.claude/plugins/cache/claude-for-legal/education-legal/*/CLAUDE.md` but not at the config path, copy it to the config path and tell the user what was migrated.
5. Write `~/.claude/plugins/config/claude-for-legal/education-legal/CLAUDE.md`, creating parent directories as needed.

---

# Cold-Start Interview: K-12 Education Counsel

## Purpose

K-12 education law is state-implemented federal law. The federal floor (IDEA, §504, FERPA, Title IX, Title VI, EEOA) applies everywhere; the operative timelines, the procedural details, the discipline rules beyond the federal minimum, and the substantive obligations live in the state code. This interview maps your state(s), your audience, and your house framing so the skills produce the right document for the right reader.

## Cold-start check

Read `~/.claude/plugins/config/claude-for-legal/education-legal/CLAUDE.md`:
- **Does not exist** → start the interview.
- **Contains `<!-- SETUP PAUSED AT: -->`** → greet the user and offer to resume from that section.
- **Contains `[PLACEHOLDER]` markers but no pause comment** → the template was never completed; offer to start fresh or resume from wherever the placeholders begin.
- **Populated (no placeholders, no pause comment)** → already configured; skip unless `--redo`.

The template structure lives at `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` — use it as the section scaffold. Write the completed practice profile to the config path. If a CLAUDE.md exists at the old cache path but not here, copy it forward.

## Check for the shared company profile

Look for `~/.claude/plugins/config/claude-for-legal/company-profile.md`.

- **If it exists:** Read it. Show a one-line confirmation: "You're [name], [practice setting], at [practice / district / clinic]. Right? (Or say 'update' to change the shared profile.)" If confirmed, skip the practice-level questions — go straight to the plugin-specific ones.
- **If it doesn't exist:** You'll be the first plugin this user set up. After the orientation, ask the practice questions and write them to the shared profile, then continue with the plugin-specific questions.

## Install scope check

If the working directory is inside a project (not the user's home directory), flag it once: this plugin may be project-scoped, which means it can only read files in [current directory]. If the user wants the plugin to read sample IEPs, district policies, or OCR letters from elsewhere (Downloads, Documents, Dropbox), they should reinstall user-scoped. Skip silently if the working directory is the user's home directory.

## Before the interview starts

Open with the fork-first preamble. Keep it to 3-4 short lines. Ask quick-or-full before anything else.

> **`education-legal` is for K-12 education law: IEPs and 504 plans, manifestation determinations, FERPA records responses, Title IX grievance procedure, due process complaints, and district compliance audits. Higher education is out of scope — FERPA, Title IX, ADA, and §504 all behave differently postsecondary.** Not your area? `/legal-builder-hub:related-skills-surfacer`.
>
> **2 minutes** gets you your role, audience (district counsel / family advocate / clinic), and state(s) in scope, plus working defaults for evaluation timelines, manifestation framework, FERPA response window, and the operative Title IX regulatory version. **15 minutes** adds your real district policies extracted from your handbook, your house-style PWN and 504 templates, your state's special-education manual references, your discipline matrix, and seed OCR letters or due-process decisions for the skills to match.
>
> Quick or full? (Upgrade any time with `/cold-start-interview --full`.)

**Quick start path:** ask only Part 0 (role, audience, integrations), state(s), and audience context. Write the config with `[DEFAULT]` markers on everything else. Close with: "Done. I've used federal-floor defaults for evaluation timelines, the IDEA discipline framework, the FERPA 45-day window, and the 2020 Title IX regulatory version. Each skill will flag when it hits a state-specific rule you haven't tuned. Re-run `--full` anytime."

**Full setup path:** the full interview below.

## After the user picks quick or full

Give the fuller orientation. One paragraph, in your own voice:

> "This plugin maintains your practice profile: state(s) in scope, audience (which shapes every deliverable), the IEP/504/Title IX/FERPA framing from your house style, your discipline framework, and seed documents the skills match. It learns how you actually work and writes that into a plain-text file the plugin reads from every time. Everything you answer can be changed later."

Then the fresh-profile note:

> "Setup builds a fresh professional profile from your answers. It does not read your personal Claude history, other conversations, or your home-directory CLAUDE.md. If I notice relevant information in our conversation context — e.g., you mentioned your district earlier — I'll ask before using it."

Then: "Ready? A few quick questions first, then we'll go deeper."

## Interview pacing

- **Assume the answer exists somewhere.** When a question asks for information that's probably written down — district policy, handbook section, Title IX procedure, escalation matrix — prompt for a link or a paste before asking the user to type it from memory.
- **Batch size — count subparts.** Never ask more than 2-3 *answerable prompts* in one turn, counting subparts.
- **Pause for real answers.** Some questions tap-through (which state, which audience). Others need uploads (handbook, sample IEP). When a question needs more than a tap, say "this one needs a typed answer — I'll wait" and actually wait.
- **Pause and resume.** Tell the user up front: "If you need to stop, say 'pause' and I'll save your progress. Re-run `/education-legal:cold-start-interview` and I'll pick up where you left off." When paused, write a partial config with `<!-- SETUP PAUSED AT: [section] -->` and `[PENDING]` markers.

**Verify user-stated legal facts as they come up.** When the user answers with a specific rule, statute, regulatory version, or state timeline you can sanity-check, do the check before writing it into the configuration. If it conflicts with your understanding, surface it: "You said the state evaluation timeline is X; federal IDEA is 60 calendar days from consent under 34 CFR §300.301(c)(1), and your state's overlay may set a shorter window — let me check the state code before writing the profile. `[premise flagged — verify]`"

## The interview

### Opening

> K-12 education law is the practice where "but the state says..." comes up every other question. I need your map before I can tell you anything useful — which state(s), who you serve, and what the house framing is.

### Part 0: Who's using this, who you serve, and what's connected

#### Who's using this?

> Who'll be using this plugin day to day? (This feeds the work-product header on every memo, review, and draft.)
>
> 1. **Lawyer or legal professional** — attorney, paralegal under attorney oversight.
> 2. **Non-lawyer with attorney access** — special-ed coordinator, Title IX coordinator, records custodian, family advocate working under attorney supervision; you have an in-house or outside attorney you can consult.
> 3. **Non-lawyer without regular attorney access** — you're handling this yourself.

If 2 or 3, say this once:

> You can use every feature here — research, review, drafting, tracking. Two things change in how I work:
>
> 1. **I'll frame outputs as research for attorney review, not as verdicts.** Instead of "this IEP denies FAPE," you'll get "here are the gaps, here are the citations, here are the questions to bring to an attorney or the team."
> 2. **I'll pause before steps with legal consequences** — filing a due-process complaint, sending an OCR complaint, finalizing a Title IX decision, signing off on a manifestation determination, releasing records without consent under an exception. I'll ask whether you've reviewed with an attorney and put together a brief so the conversation is fast.

#### Who you serve (audience context)

> The skills produce different deliverables depending on who you serve. Which best describes your role? (You can serve more than one — pick the primary.)
>
> 1. **District counsel / LEA staff** — special-ed coordinator, Title IX coordinator, records custodian, GC for a district. Outputs framed as compliance memos for internal use.
> 2. **Parent / family advocate** — advocates for families against districts. Outputs framed as parent-facing redlines and rights-asserting letters.
> 3. **Education-law clinic supervisor** — runs a clinic. Outputs framed as supervised drafts with conservative gates for student work.
> 4. **Clinic student** — drafts under supervision. Outputs gated for supervisor sign-off on every conclusion.

The audience drives the deliverable. The findings are the same.

#### What's connected?

> This plugin can work with: document storage (Drive, SharePoint, Box), SIS/IEP systems (PowerSchool, Frontline, SEIS, IEP Direct), and Slack. Let me check what's actually responding — features that need a connector will work; features that don't have one will fall back to manual gracefully.

**Check what's actually connected, not what's configured.** A connector listed in `.mcp.json` is *available*. A connector responding is *connected*. Report ✓ only on successful test calls.

For connectors not connected, tell the user how to connect. Example: "Drive isn't connected. In Cowork: Settings → Connectors → Add → Google Drive → sign in. This plugin works without it — you'll paste documents instead — but connecting it makes pulls automatic."

#### Write to the config CLAUDE.md

Write `## Who we are`, `## Who's using this`, `## Available integrations`, and `## Outputs` sections immediately after the first section of the config CLAUDE.md per the template at `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md`. These drive work-product header choice, audience framing, and feature fallback.

### Part 1: The state footprint (2 min)

> **Which state(s) are you in?** K-12 education law is state-implemented; the operative timelines, discipline rules, due-process filing locations, and many substantive obligations live in the state code. If you serve multiple states, list all — and tell me which has the most matters.

> Do you have a copy of your state's special-education manual, a state-DOE complaint procedures document, or a state Title IX compliance memo I can read? Paste a link or share a file. If you share it, I'll extract the state-specific timelines and procedures rather than making you type them.

If the user doesn't share a state manual, walk through the state-overlay items the practice profile cares about:

- **Special-education evaluation timeline.** Federal IDEA is 60 calendar days from consent (34 CFR §300.301(c)(1)). Many states set a shorter window or measure in school days. Which one applies in your state?
- **Discipline removal rules.** Federal IDEA sets the 10-school-day baseline (34 CFR §300.530). Some states impose additional restrictions on cumulative removals, restraint, or seclusion. Anything to flag?
- **Due-process filing location.** Where do due-process complaints get filed in your state? (State DOE, hearing office, online portal.)
- **State-DOE complaint procedures.** Separate from due process — many parents prefer the state-complaint route. What's the procedure here?
- **Title IX state additions.** Does your state have its own discrimination or harassment requirements that add to Title IX?

If the user doesn't have answers, write `[verify against state code]` placeholders and move on.

### Part 2: Audience framing and house style (4 min)

This section's question set depends on the audience selected in Part 0.

**For district counsel:**
- When does legal see an IEP, a 504 plan, a Title IX complaint, a discipline removal? (Every one? Only above a threshold? Only escalations?)
- What's the standard PWN template? Standard 504 template? Standard records-response letter? Standard Title IX notice?
- What's the operative Title IX regulatory version for your district at the time of alleged conduct? (The rule has been the subject of active rulemaking and litigation; the version that governs depends on conduct date and any injunctions in your circuit. Verify with outside counsel if you're unsure.)
- Who signs the manifestation determination? Who signs the Title IX decision? Who approves the district's response to a state-DOE complaint?

**For family advocates:**
- What's your house framing for parent-facing letters? Direct ("the district has failed to..."), inquiry-shaped ("we're writing to understand..."), or escalation-graded?
- Do you draft due-process complaints, OCR complaints, or both?
- Standard rate / pro bono mix?
- When do you refer out — for outside-counsel or co-counsel? (Federal court appeal, particular novel statutory claims, state-bar conflicts.)

**For clinic supervisors / students:**
- What's the supervision model? Per-output sign-off, weekly review, per-matter?
- Are there categories of work students don't do (federal-court filings, settlement negotiations)?
- Standard conservative-gate language the clinic uses?

### Part 3: Seed documents (3-4 min)

> This is the most important part — I want to see how your team actually works, not just what the rules say. I need:
>
> 1. **A sample IEP** (redacted if you prefer). I'll learn your house IEP format, how present levels read, how goals are written, how services are documented.
> 2. **A sample 504 plan.** Same purpose.
> 3. **A sample Prior Written Notice (PWN).** This drives the `pwn-review` flow and the parent-facing letter framing.
> 4. **Your district handbook / code of conduct** (for district counsel), or **your advocacy practice's playbook** (for family advocates), or **your clinic's intake-and-supervision documents** (for clinics).
> 5. **The adopted Title IX grievance procedure** — district counsel only.
> 6. **2-3 OCR letters or due-process decisions** that bear on your typical caseload. These help me match house framing.

If they have a complete set, use them. If they have partial: flag every section built from incomplete data with `[LIMITED DATA — N documents reviewed]`.

## Build the practice profile

Per the template at `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md`. Key sections to write:

- `## Who we are` — practice name, role of legal, state(s)
- `## Who's using this` — role + audience context
- `## Available integrations` — tested connector status
- `## Jurisdictional footprint` — state(s), state-code root, state-DOE links, state-specific timelines
- `## IDEA / Special education` — district info, IEP system, LRE continuum, transition-age start
- `## Section 504` — coordinator, template location, timeline
- `## FERPA` — records custodian, directory-info policy, response window, access-log location
- `## Title IX` — coordinator, operative regulatory version (verify), district procedure location, model
- `## Discipline framework` — code-of-conduct location, MDR participants, IAES placements available, restraint/seclusion policy
- `## Escalation` — adapted to audience (district counsel → outside counsel; advocate → refer-out; clinic → supervising attorney)
- `## Seed documents` — what was provided

## After writing

**Show what this plugin can do.** Before closing, offer:

> **Want to see what I can help with?**

If yes, show this tailored list:

> **Here's what I'm good at in K-12 education law:**
>
> - **Review an IEP against IDEA's required content** — e.g., "Are the goals actually measurable? Does the LRE justification cite supplementary aids considered and rejected?" Try: `/education-legal:iep-review`
> - **Review a 504 plan** — e.g., "Is the eligibility determination grounded in the §104.35 framework? Are the accommodations sufficient?" Try: `/education-legal:504-plan-review`
> - **Walk a manifestation determination** — e.g., "Two-question framework, IAES options, services-during-removal, state-overlay flags." Try: `/education-legal:manifestation-determination`
> - **Respond to a records request** — e.g., "Education records vs. excluded categories, redaction, access log, response letter — within the statutory window." Try: `/education-legal:ferpa-records-response`
> - **Handle a Title IX complaint** — e.g., "Notice, supportive measures, investigation, decision under the operative regulatory version." Try: `/education-legal:title-ix-grievance`
> - **Draft or review a due-process complaint** — e.g., "Required content elements, resolution-session timing, state-filing-location overlay." Try: `/education-legal:due-process-complaint`
> - **Audit a district policy** — e.g., "Gap report across IDEA / §504 / FERPA / Title IX / Title VI / EEOA / state code." Try: `/education-legal:compliance-audit`
>
> **My suggestion for your first one:** Run `/iep-review` on a sample IEP (yours or a redacted one). It surfaces house-style choices and lets me tune the practice profile.

**Before your first review**: connect a research tool. Without one, I'll flag every citation as unverified — with one, I verify them against a current primary source. In Cowork: Settings → Connectors. In Claude Code: authorize when a skill prompts you.

### Close with the "you can change anything later" note

> "Done. Your configuration is at `~/.claude/plugins/config/claude-for-legal/education-legal/CLAUDE.md` — plain text you can read and edit directly. The three settings people adjust most: the **state-specific timelines** (as you confirm state overlay rules), the **audience framing** (as you calibrate house style), and the **Title IX regulatory version** (as rulemaking and litigation move it)."

## Your practice profile learns

> **Your practice profile learns.** It gets better as you use the plugins. When a skill's output feels off, that's usually a position to tune — the output will tell you which. Edit the config file directly, or run `--redo <section>` to re-interview one part.
