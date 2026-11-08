---
name: log-leave
description: >
  Add a new leave to the leave register with the minimum information needed to
  start tracking deadlines. Use when an employee goes on leave and you want the
  weekly leave-tracker run to check designation, certification, and exhaustion
  clocks from day one.
argument-hint: "[describe the leave — employee/role, type, jurisdiction, start date]"
---

# /log-leave

Adds a new leave entry to `~/.claude/plugins/config/claude-for-legal/employment-legal/leave-register.yaml` with the minimum
information needed to start tracking deadlines. Use when an employee goes on
leave and you want `/employment-legal:leave-tracker` to check the clocks from
day one.

This skill does not state the law. Coverage thresholds, eligibility
requirements, entitlements, and deadlines are researched and cited at the time
of logging, the same way the leave-tracker agent does it — the numbers come
from research, not from this file.

## Instructions

1. Read `~/.claude/plugins/config/claude-for-legal/employment-legal/CLAUDE.md` → employee count (`Who we are`), jurisdictional footprint, jurisdiction table, Systems section, and any jurisdiction-specific leave rules the team has already researched and recorded.

2. Ask all of the following in a single prompt — do not drip them one at a time:

   > A few quick questions to set up leave tracking:
   >
   > - Employee name or role (anonymized is fine)
   > - Where do they work? (State — this determines which rules apply)
   > - Leave type: FMLA / state leave (which state) / USERRA / ADA accommodation
   > - Leave start date
   > - Is this intermittent leave? What is their normal schedule (hours/week)?
   > - Expected return date (if known — leave blank if not)
   > - Length of service and approximate hours worked recently, and how many
   >   employees work at or near their worksite (eligibility for some leave
   >   laws turns on these)
   > - Has the designation notice been sent? If yes, when?
   > - Has medical certification been requested? If yes, when?

3. **Confirm coverage and eligibility before creating any clock.** The leave
   type the user names is not proof that the regime applies. For the selected
   regime — and any regime that may run concurrently (e.g., FMLA alongside a
   state leave law, or ADA accommodation after statutory leave) — research the
   currently operative employer-coverage threshold and employee-eligibility
   requirements for this jurisdiction, cite the controlling statute and
   implementing regulations, and check them against the employee count in the
   practice profile and the facts from step 2.
   - Covered and eligible → continue to step 4 for that regime.
   - Not covered or not eligible → do not create that regime's clocks. Record
     the basis in `coverage_eligibility` and `controlling_sources`, say so in
     the confirmation, and flag whether a different regime (a state leave law,
     ADA or a state equivalent as accommodation) may apply instead `[review]`.
   - A fact is missing or the rule could not be confirmed → record
     `coverage_eligibility` as unconfirmed with what is missing, ask for it in
     the confirmation, and tag every deadline computed for that regime
     `[verify — coverage/eligibility not confirmed]`.

4. Determine the entitlement for each regime that applies. The jurisdiction
   table in the practice profile records escalation rules, not leave
   entitlements — do not fill the entitlement from it or from memory. Use a
   researched rule the team has already recorded in the practice profile (with
   its cite) if there is one; otherwise research the currently operative
   entitlement and measurement method, cite it, and verify currency. Express it
   against the employee's actual normal schedule — do not assume a 40-hour
   week.

5. Compute the first upcoming deadline from the researched rule for each
   applicable regime. Each regime sets its own clocks, and some run from events
   other than leave start — never carry one regime's timing over to another.
   - **FMLA / state equivalents:** research the designation-notice deadline and
     the medical-certification deadline and cure period for the applicable
     jurisdiction and employer. If both are done, the next decision point is the
     projected exhaustion date at the current usage rate.
   - **ADA (or state equivalent) leave as accommodation:** no designation or
     certification clock carries over from FMLA. Record whether the interactive
     process has been initiated; the first decision point is initiating and
     documenting it, plus any researched deadline that applies.
   - **USERRA:** state which clock is running and whose it is — the employee's
     application-for-reemployment window or the employer's reinstatement
     obligation. Cite 38 USC and the implementing DOL regulations.

   Record each deadline's pinpoint cite in `controlling_sources` and note whose
   clock it is (employer obligation vs. employee obligation). If no research
   tool is responding this session, a deadline supplied from model knowledge
   carries `[model knowledge — verify]` on the date itself, `controlling_sources`
   says it is unverified model knowledge, and the reviewer note's **Sources:**
   line says so.

6. Write a new entry to `~/.claude/plugins/config/claude-for-legal/employment-legal/leave-register.yaml` using the leave register
   format from the leave-tracker agent, including `coverage_eligibility`,
   `entitlement`, and `controlling_sources`. If the file doesn't exist, create
   it.

7. Confirm in a short block:
   > "Logged. [Employee/Role] — [Leave type] — [Jurisdiction] — started [date].
   > Coverage/eligibility: [confirmed / not covered or not eligible — no [regime]
   > clock created / unconfirmed — need: (missing facts)].
   > First deadline: [what it is, when, whose clock] [source tag].
   > Run /employment-legal:leave-tracker weekly to check deadlines — it does not
   > run on its own, so set a recurring reminder."

## Examples

```
/employment-legal:log-leave
```

```
/employment-legal:log-leave
Sarah (Sr. Engineer, works in California) just started FMLA today for a
serious health condition. Intermittent. No designation sent yet.
```
