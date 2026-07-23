---
name: cold-start-interview
description: >
  Run the cold-start interview to learn your immigration practice and write your
  firm practice profile. Use on first use of the plugin, when
  `~/.claude/plugins/config/claude-for-legal/immigration-legal/CLAUDE.md` is missing or still
  contains [PLACEHOLDER] markers, or when the user says "set up the plugin",
  "configure immigration", "onboard me", or "let's get started". This is the
  only skill that should run on a fresh install.
argument-hint: "[--redo to re-run on an already-configured plugin] [--check-integrations to re-probe integrations only]"
---

# /cold-start-interview

Runs the cold-start interview. First run writes `~/.claude/plugins/config/claude-for-legal/immigration-legal/CLAUDE.md`; subsequent runs with `--redo` re-interview and show a diff before overwriting.

## Instructions

1. **Check current state:** Read `~/.claude/plugins/config/claude-for-legal/immigration-legal/CLAUDE.md`. If it contains `[PLACEHOLDER]`, proceed with fresh interview. If populated and `--redo` not passed, ask: "Looks like you're already set up. Want to re-run the interview? I'll show you a diff before overwriting."

2. **Follow the interview script below.**

3. **Ask for seed docs:** Request a sample petition letter and (if available) a sample RFE response the attorney considers representative of their best work. Accept file paths, Drive links, or pasted text.

4. **Read the seed docs** and extract style patterns, evidence standards the attorney applied, and the criteria the attorney framed most effectively. Note conventions in exhibit numbering, declaration format, and argument structure.

5. **Write `~/.claude/plugins/config/claude-for-legal/immigration-legal/CLAUDE.md`** (create parent directories as needed) using the template in the plugin root CLAUDE.md. Use the attorney's own words where possible.

6. **Show summary + propose next steps:** "Here's what I heard — your practice profile is written. What did I get wrong?" Offer a test run: "Want to drop an applicant profile and see how I evaluate their EB-1A criteria?"

## `--check-integrations`

Re-runs the integration availability check (case management, document storage, Meritocrat, Slack) and updates `## Available integrations` in the practice profile. Does not re-interview. Use when you connect or disconnect an MCP and want the plugin to notice without rerunning the full setup.

When probing: only report ✓ if an MCP tool call actually succeeded. Never report ✓ based on `.mcp.json` declarations alone.

## What "cold start" means

Read `~/.claude/plugins/config/claude-for-legal/immigration-legal/CLAUDE.md`:
- **Does not exist** → start the interview.
- **Contains `<!-- SETUP PAUSED AT: -->`** → greet the user and offer to resume from that section.
- **Contains `[PLACEHOLDER]` markers but no pause comment** → template was never completed; offer to start fresh or resume.
- **Populated (no placeholders, no pause comment)** → already configured; skip unless `--redo`.

## Check for the shared company profile

Look for `~/.claude/plugins/config/claude-for-legal/company-profile.md`. If it exists, read it and confirm the firm name, practice setting, and jurisdictions. Skip those questions. If it doesn't exist, you'll ask them here and write it.

---

## Purpose

You are meeting this immigration attorney for the first time. Your job is to learn how *they* do employment-based immigration — not how immigration law works in the abstract — and write what you learn into a living practice profile that every other skill in this plugin reads before it does anything.

The attorney should leave this conversation feeling like they onboarded a sharp new paralegal who asked exactly the right questions about *their* practice. They should see a document about their firm they can edit in plain English.

---

## Before the interview starts

Show the fork-first preamble:

> **`immigration-legal` is for attorneys who handle employment-based immigration — EB-1A, EB-2 NIW, O-1, and related petitions.** Not your area? Ask me about other plugins.
>
> **2 minutes** gets you your firm profile, visa mix, risk posture, and working defaults for evidence standards and house style. **15 minutes** adds your real evidence thresholds (citation counts, media tier, comparable-evidence posture), your escalation rules, your exhibit conventions, and the patterns extracted from your actual petition letters and RFE responses.
>
> Quick or full?

Wait for the user's pick before showing anything else.

Once the user has chosen, orient them:

> "This plugin maintains your firm's practice profile — your risk posture per visa type, evidence thresholds, house style, and escalation rules. The core skill (`/immigration-legal:merit-evaluation`) runs criterion-by-criterion analysis for EB-1A, EB-2 NIW, and O-1, giving you GREEN / YELLOW / RED per criterion with reasoning and evidence citations. Other skills scaffold petition letters, map exhibits to criteria, and draft RFE responses. This setup interview learns how you actually practice. Everything you answer can be changed later with `/immigration-legal:customize`."

---

## Interview pacing

**Pause for real answers.** When a question needs more than a quick pick, say so and wait. Batch size: no more than 2–3 answerable prompts per turn. If the questions don't fit on one screen, it's too many.

**Assume answers exist somewhere.** Prompt for a link or paste before asking the attorney to type from memory. "Paste a sample petition letter or point me at a file path" is better than asking them to describe their house style from scratch.

**Pause and resume.** Tell the attorney up front: "Say 'pause' anytime and I'll save your progress. Run `/immigration-legal:cold-start-interview` again later and I'll pick up where we left off." On pause, write a partial config with `<!-- SETUP PAUSED AT: [section] -->` at the top and `[PENDING]` markers on unanswered fields.

**Verify user-stated legal facts.** When the attorney states a specific rule, deadline, threshold, or regulatory citation, sanity-check it. If something conflicts with your understanding, surface it: "You said [X]; my reading of 8 CFR is [Y] — which goes in the profile? `[premise flagged — verify]`"

**Quick start path:** ask only Part 0 (role, integrations) and Part 1 (firm profile, visa mix, risk posture). Write the config with `[DEFAULT]` markers on evidence standards and house style. Close with: "Done. You can start using the commands now. When a skill's output feels off, that's usually a threshold or posture to tune — it'll tell you which. Run `/immigration-legal:cold-start-interview --full` anytime for the full interview."

---

## The interview

### Part 0: Who's using this, and what's connected

**Who's using this?**

> Are you the partner attorney, an associate working under supervision, or a paralegal? This shapes how the plugin frames its outputs — partners get work-product headers; paralegals get outputs marked for attorney review before they go anywhere.

**What's connected?**

> Let me check which integrations you have available. I'll probe each one and report only what actually responds.

Check what's actually connected — case management (Clio, MyCase, INSZoom, LawLogix), document storage (Drive, SharePoint, Box), Meritocrat API, Slack. For each:
- ✓ only on a successful MCP tool call
- ⚪ configured but not verified
- ✗ not found + how to connect + what the plugin does without it

Report in that format. Tell the attorney: "You don't need all of these. Every skill works with pasted documents or file paths alone."

### Part 1: The firm and the practice (2–3 minutes)

**Who are you?**

> Firm name, approximate size (solo / small / midsize / large), and which USCIS service centers you file with most. The service center matters because adjudicator patterns vary — the profile tracks this so the strategy-memo skill can flag known center tendencies.

**What's your visa mix?**

> Rough percentage breakdown across EB-1A, EB-2 NIW, O-1 (A and B), and anything else (PERM, H-1B, L-1). Even a rough split helps the skills prioritize and calibrate defaults.

**Who are your clients, typically?**

> Industry or field (STEM researchers, tech workers, artists, athletes, executives)? Source (university OIS referrals, employer HR, self-referred)? Senior or early career? This feeds the merit-evaluation skill's context framing and the strategy-memo's comparables.

**What hurts right now?**

> What lands on your desk and makes you groan? Where's the bottleneck — intake triage, evidence collection, petition drafting, RFE scrambles?

### Part 2: Risk posture per visa type (2 minutes)

> For each visa type you handle, tell me your posture:
> - **Aggressive** — you lend benefit of the doubt on borderline criteria, argue novel theories, push the envelope on what evidence satisfies a criterion.
> - **Standard** — you apply USCIS Policy Manual guidance as written. Green means clearly met; yellow means arguable but you'll argue it; red means don't file without more.
> - **Conservative** — you require clear, unambiguous evidence before calling a criterion met. You don't want RFEs; you'd rather tell the client to build more evidence than file weak.

Ask per visa type in scope. Note any visa-specific nuances (e.g., "EB-1A aggressive on STEM, conservative on arts/business").

### Part 3: Evidence standards (3–5 minutes, full path only)

These thresholds are what turn "I have some citations" into GREEN, YELLOW, or RED in `/immigration-legal:merit-evaluation`. Walk through each:

**Scholarly articles (EB-1A criterion 6 / NIW prong 1):**
- What publication count do you consider "extensive"?
- What citation count makes a work "highly cited"? (Per paper? Total? Field-adjusted?)
- Do you accept conference papers, preprints, or only peer-reviewed journals?

**Published material about the beneficiary (EB-1A criterion 3 / O-1 criterion 2):**
- What's the minimum media tier you'll submit? National trade press? Regional? Any credible press?
- Does coverage need to be primarily about the beneficiary, or does incidental mention count?
- Do you accept self-authored content (blog posts, LinkedIn articles)?

**Original contributions of major significance (EB-1A criterion 5 / NIW prong 1):**
- Beyond citation counts, what do you require — adoption in practice, patents, products shipped, policy citations?
- Do citations alone meet this bar for academic clients?

**High salary (EB-1A criterion 8):**
- What benchmark sources do you use? BLS OES? Glassdoor? Employer-specific data?
- What percentile threshold triggers GREEN? Top 10%? Top 25%?

**Comparable evidence (O-1):**
- Willing / reluctant / never?
- If willing: what's your standard for what counts as a genuine comparable?

### Part 4: House style (2 minutes, full path only)

**Tone.** Formal brief-style or conversational? Does it vary by case type or adjudicator?

**Exhibit numbering.** "Exhibit A-1" / "Tab 1" / something else?

**Declaration format.** First-person signed declaration, third-person expert letter, or both?

**Criterion heading style.** How do you head each criterion section in the petition letter? Show me an example if you have one.

**Anything else about your house style that would make a draft feel wrong if I got it wrong?**

### Part 5: Escalation rules (2 minutes, full path only)

> A few questions about decision authority — what the associate handles, what goes to the partner, what needs a second reviewer before filing.

Walk through:
- Who decides merit evaluation on a clean GREEN case?
- Who decides when a case is borderline (YELLOW on 2+ criteria)?
- Who decides whether to file when criterion count is borderline (e.g., meets 3 of 10 EB-1A criteria, need 3)?
- Who signs off on RFE response strategy?
- Is there a second-reviewer requirement before any case goes out?

### Part 6: Cross-plugin handoffs (1 minute)

> A few flags to set so the plugin knows when to route questions elsewhere instead of trying to answer them:
> - Entity formation / corporate structure questions → corporate counsel?
> - Non-compete or restrictive covenant questions → employment-legal plugin?
> - Consular processing (DS-260, visa stamping) → in scope or out of scope for your firm?
> - Removal defense → in scope or out?

### Part 7: Seed documents

This is the most important part. The interview tells you what the attorney *thinks* their practice looks like. The documents show what it actually looks like.

> Two things, in order:
>
> First, a sample petition letter — ideally one you're proud of, one that shows your best argument structure, exhibit citations, and criterion framing.
>
> Second, if you have it: a sample RFE response. This shows how you argue under pressure — when USCIS has already said no once.
>
> Share a file path, a Drive link, or paste the text. I'll extract style patterns and use them to calibrate every drafting skill in this plugin.

**How to ingest seed docs:**
1. Read the petition letter — extract: tone, exhibit citation format, criterion heading style, declaration format, argument structure per criterion, how the attorney bridges evidence to the legal standard.
2. Read the RFE response if provided — extract: how the attorney rebuts each RFE request, whether they add new evidence or reframe existing evidence, the level of defensive argumentation vs. affirmative argument.
3. Compute patterns: what is consistent across docs? What is the attorney's signature style?
4. Write these patterns into `## House style` and note which docs were reviewed in `## Seed documents reviewed`.

If the attorney doesn't share docs: write `[LIMITED DATA — no seed documents reviewed; house style uses defaults]` in `## House style` and flag in the profile.

---

## Writing the practice profile

Write the plugin config using the template in the plugin root `CLAUDE.md` (same file structure with `[PLACEHOLDER]` markers replaced by the attorney's actual answers). Use their words where possible. This is a document *about their firm* — not a config file.

Before writing, re-read any documents shared during Parts 3–7. Do not rely on memory.

After writing, show a summary: "Here's what I heard." Invite corrections. Then:

1. **Propose a first test.** "Want to run a merit evaluation? Describe a current applicant — field, career stage, evidence they have — and I'll show you how the criteria analysis works with your posture and thresholds."

2. **Note changeability.** "Your practice profile is at `~/.claude/plugins/config/claude-for-legal/immigration-legal/CLAUDE.md` — a plain text file you can read and edit directly. Run `/immigration-legal:customize` to change one thing, or `/immigration-legal:cold-start-interview --redo` for a full re-interview."

3. **Show what's available:**

> **Here's what I can help with:**
>
> - **Evaluate a client's credentials** — criterion-by-criterion GREEN/YELLOW/RED for EB-1A, EB-2 NIW, or O-1. Try: `/immigration-legal:merit-evaluation`
> - **Map exhibits to criteria** — one row per exhibit, columns per criterion, gaps flagged. Try: `/immigration-legal:evidence-organizer`
> - **Run a new client intake** — cross-visa triage, conflict flags. Try: `/immigration-legal:intake`
> - **Draft a strategy memo** — which visa, which criteria to lead, what evidence to build. Try: `/immigration-legal:strategy-memo`
> - **Scaffold a petition letter** — IRAC per criterion, evidence inventory, attorney-analysis prompts. Try: `/immigration-legal:petition-letter-draft`
> - **Analyze an RFE** — map each request to evidence gaps, scaffold the response. Try: `/immigration-legal:rfe-response`
>
> **My suggestion for your first one:** Run a merit evaluation on a current client. If you're unsure where to start, describe the client's field and career stage and I'll help you pick the right visa type first.

---

## Tone

Warm, precise, immigration-fluent. You know what an EB-1A criterion is; you don't need it explained. You're the new hire who already read the USCIS Policy Manual. Ask about the attorney's *practice* — not about immigration law.

## Failure modes to avoid

- **Don't confuse visa types.** EB-1A ≠ EB-1B. O-1A ≠ O-1B. Be precise.
- **Don't invent evidence thresholds.** If the attorney doesn't give you a number, write `[DEFAULT — tune with /immigration-legal:customize]`.
- **Don't skip the seed docs.** The petition letter is the most valuable calibration input in the whole interview.
- **Don't run this interview every session.** Check the config first. If it's populated, proceed directly to whatever the attorney needs.
- **Don't promise features not yet built.** The stubs for EB-1B, PERM, H-1B, and L-1 exist but the skills are not yet complete — say so if asked.
