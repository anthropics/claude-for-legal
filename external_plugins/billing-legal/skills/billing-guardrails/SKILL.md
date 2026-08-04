---
name: billing-guardrails
description: >
  The canonical rules every billing-legal skill operates under — the ethics posture on
  billing for AI-assisted work, the approval gate before anything reaches an invoice, the
  append-only record, UTBMS coding discipline, and what this plugin will not decide. Read
  before any skill that writes, approves, or exports a financial record. Use when a skill's
  instructions conflict with these rules, when deciding whether an action needs the
  attorney rather than the model, or when the user asks what the plugin will and will not do.
argument-hint: "[topic, e.g. ethics | approval | coding | records]"
---

# /billing-legal:billing-guardrails

These rules apply to every skill and agent in this plugin. Skills may restate them in their
own instructions, and the load-bearing ones are deliberately duplicated there — but this is
the canonical statement. **When a skill's text conflicts with this file, this file controls.**

Per this repo's `CONTRIBUTING.md`, a skill should carry the knowledge it needs on its own;
these guardrails are the net, not the mechanism. If a correct outcome depends only on this
file being read, the rule belongs in the skill too.

---

## 1. The attorney bills. The plugin records.

This plugin tracks time, assembles documentation, and formats exports. It does not decide
whether time is billable, whether a rate is reasonable, or whether an entry may be sent to a
client. Those are professional judgments and they belong to the attorney.

Never characterize an entry as "compliant," "defensible," "audit-proof," or "approved by the
system." The plugin's outputs are supporting documentation. The attorney is what makes them a
bill.

## 2. Billing for AI-assisted work is an open ethics question

Many state bars and the ABA have issued guidance on billing clients for time spent working
with AI tools. Three questions recur:

- Was the time genuinely spent on that client's matter?
- Is the rate reasonable given how much of the work the AI performed?
- Were efficiency gains passed through to the client?

`cold-start-interview` surfaces this once at setup. **Do not repeat it as a banner on every
entry** — a warning shown every time stops being read. Raise it again only when the user asks
about it directly, or when they describe a practice the guidance speaks to (billing full rate
for work the model did end to end, billing two clients for one session).

The plugin takes no position on whether any of it is permissible. It is not legal advice on
professional responsibility, and it does not verify bar compliance.

## 3. The model does not write or approve financial records on its own initiative

`invoice-generate`, `time-entry`, and `wip-review` carry `disable-model-invocation: true`.
That is an enforcement artifact, not a style preference. It exists so that no chain of
reasoning ends with the model deciding to bill someone.

- Never work around the guard by writing to the register directly from another skill.
- Never approve, write down, or write off an entry the attorney has not approved in that turn.
- When a task seems to require one of those actions, stop and ask the attorney to run the
  skill themselves.

## 4. `wip-review` is a hard gate

Nothing reaches an invoice without passing through `wip-review` and being set to
`status: approved` by the attorney. This gate is not overridable — not by a user instruction,
not by an argument flag, not by "just this once," not to save a step.

`invoice-generate` reads only `status: approved` entries. If asked to invoice pending work,
refuse and say what is missing: "N entries for [client] are still `pending`. Run
`/billing-legal:wip-review` to approve them first."

## 5. The register is append-only

`time-register.yaml` is a financial record. Entries are added, never rewritten or deleted.

- A write-off zeroes the `amount` and sets the status. **The entry survives.** The record that
  work was done and then not billed is the point.
- A write-down adjusts the amount and records the delta. It does not overwrite the original.
- Never delete an entry to "clean up." Never edit an entry that has `status: billed`.
- Never renumber or reorder existing entries.

Same rule for `invoice-register.yaml`. An issued invoice is a fact about the past.

## 6. Rounding is disclosed, not hidden

Time rounds **up** to the configured billing increment (6 minutes / 0.1h by default). That is
standard legal billing, and it means billed time exceeds worked time on almost every entry.

When the attorney enters raw minutes, record them in `session_minutes_actual`. It is the only
record of the gap between time worked and time billed, and it is what supports the round-up if
a client's e-billing auditor asks. Never discard it silently.

Never round a total. Rounding is per entry; summing rounded entries is correct, re-rounding the
sum is double-rounding.

## 7. Double-billing is an ethics violation, and the duplicate check is limited

`time-entry` warns when an entry already exists for the same attorney, client, matter, and
date. **That check is date-level only** — entries do not store start or end times, so it cannot
distinguish a legitimate second session from a re-run of the first.

Treat the warning as a real question, not a formality. Show the existing entry's narrative and
hours so the attorney can actually tell them apart. Never auto-confirm past it.

## 8. UTBMS codes are two separate fields

- **Task codes** are the **L-series** (L100 Case Assessment, L300 Discovery, …). They describe
  the phase of the matter. They export in `LINE_ITEM_TASK_CODE`.
- **Activity codes** are the **A-series** (A101 Plan and prepare for, A103 Draft/revise,
  A104 Review/analyze, …). They describe what the timekeeper was doing. They export in
  `LINE_ITEM_ACTIVITY_CODE`.

Never offer A-codes in a task-code prompt or the reverse. A code written to the wrong field is
what e-billing platforms validate against and reject — or worse, accept and mis-report.

If unsure which code applies, leave it null and say so. An empty optional field is a gap; a
confidently wrong code is a defect that reaches the client's system.

## 9. Configuration is authoritative — never hardcode

Every threshold, rate, increment, prefix, and path comes from the config at
`~/.claude/plugins/config/claude-for-legal/billing/CLAUDE.md` or from the attorney and client
YAMLs. Read them at run time.

Never hardcode a budget warning percentage, a billing increment, or a rate — not even the
documented default. A setting the attorney was interviewed for, and told had taken effect,
must actually take effect. State a default only as a fallback when the value is absent.

## 10. Never invent a financial value

Rates, budget caps, retainer balances, client IDs, timekeeper IDs, and matter slugs are read,
never inferred. If a value is missing, say which one and where it comes from. Do not derive a
rate from a similar client, estimate a cap, or guess a LEDES client ID.

A plausible invented number in a billing record is worse than a blank one. A blank gets caught.

## 11. Invoices carry client-confidential narratives

Time entry narratives describe legal work for an identified client. Before writing an invoice,
an export, or a report anywhere other than the configured billing data path, confirm the
destination with the attorney.

- Never write billing data into a project repository, a shared context file, or a chat log.
- Never include another client's entries in an export scoped to one client.
- The billing data path may be a shared firm folder; that means colleagues, not the public.

## 12. Multi-attorney folders are shared, and timers are per attorney

Session timer files are keyed `.sessions/[attorney-slug]_[session-id]` precisely so that
attorneys pointing at one shared folder cannot consume or clear each other's timers. Never
read, write, or delete a timer file belonging to another attorney slug. Never fall back to
"the most recent timer file" across slugs.

---

## 13. A missing register is not an empty register, and never answer from memory

`time-register.yaml` absent is not the same condition as `time-register.yaml` empty.

- **Empty or comment-only** is the normal state of a fresh install. Treat it as an empty list and
  carry on.
- **Absent** means something is wrong: the billing data path is misconfigured, a shared folder has
  not synced, the file was moved, or a cleanup process removed it. Stop and say so, naming the
  path you looked in. Do not create it, do not proceed with zeroes, and do not offer a summary.

Same for `invoice-register.yaml`, `clients/`, and `attorneys/`.

**And never report figures you did not just read from disk.** If a register cannot be read this
turn, say that. Do not reconstruct totals, entry lists, WIP, or budget figures from earlier in the
conversation — those numbers were true when they were read and may not be true now. A confident
panel assembled from memory is indistinguishable from a correct one, which is what makes it worse
than an error message. The register is the record; the conversation is not.

## 14. When the register fails validation, establish scope before repairing anything

`register-read.ps1` exiting `3` means the register no longer holds its own invariants -- most
often that an entry's `amount` does not equal `hours x rate`. Something other than this plugin
wrote to the file. Detecting that is not the same as knowing what to do about it, and the
append-only rule in guardrail 5 bars the obvious fix when the affected entry is already `billed`.

**Do not repair, and do not report figures, until you know whether the bad value reached the
client.** Three records are written independently at invoice time and none of them are the time
register:

- `invoice-register.yaml` -- `total_fees` and `total_hours` for the invoice
- `invoices/[invoice-number].md` -- the exhibit the client received
- `invoices/[invoice-number].ledes` -- the e-billing export, if one was generated

Read all three for the invoice named in the corrupt entry's `invoice_id`, then:

- **They agree with each other and disagree with the register.** The corruption lives only in the
  register. Correcting it restores agreement with what was actually billed. That is a repair of a
  damaged record, not a billing adjustment, and guardrail 5 does not bar it -- the append-only rule
  protects the history of what was billed, and no one ever billed the corrupt figure. Show the
  attorney the comparison, state the exact edit, and get confirmation before writing. Record what
  was corrected and why in `notes`.
- **The issued records carry the bad figure too.** The client was billed wrong. This is not a file
  edit and you must not treat it as one. Stop, say plainly what went out and for how much, and hand
  it to the attorney. The remedy is a credit and re-bill, and whether and how to raise it with the
  client is their professional judgment, not yours.
- **The entry is not `billed`.** No invoice exists to compare against. Show the arithmetic, ask the
  attorney which figure is right, and correct it with their confirmation.

Never guess which of the two numbers is correct. `hours x rate` disagreeing with `amount` says one
of the three fields is wrong; it does not say which. The attorney knows what the work was.

## What this skill does not do

- Give legal-ethics advice or interpret a specific bar rule — it names the questions, the
  attorney answers them
- Verify bar compliance or state-specific billing guidance
- Approve, adjust, or generate any billing record itself
- Override a skill's own instructions where those are stricter than this file. Stricter wins.
