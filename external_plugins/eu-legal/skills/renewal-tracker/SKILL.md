---
name: renewal-tracker
description: >
  Track expiring contracts and flag renewal/termination decisions before notice
  windows close. Reads the renewal register at
  ~/.claude/plugins/config/eu-legal/renewal-register.yaml. Flags contracts with
  notice periods approaching (90/30/7 days), highlights auto-renewal clauses, and
  notes Finnish hiljainen uusiminen (automatic renewal) provisions. Use when the
  user asks "what's renewing soon", "what renewals are due", "did we miss a
  cancellation window", "add this to the renewal tracker", or on a scheduled basis.
argument-hint: "[--days N | --missed | --add]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:renewal-tracker

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md` (base profile — for entity type and jurisdiction context).
2. Load `~/.claude/plugins/config/eu-legal/commercial.md` if it exists (for escalation matrix and business owner defaults).
3. Read `~/.claude/plugins/config/eu-legal/renewal-register.yaml`. If missing or empty: see "Empty register" section below.
4. Run the workflow below.

---

## Purpose

Nobody reads a contract twice. The renewal date is extracted once at review time and lives in the register. This skill surfaces what is coming before the window closes — not after.

Not Velvoite-dependent. Works without `VELVOITE_API_KEY`.

---

## The register

Lives at `~/.claude/plugins/config/eu-legal/renewal-register.yaml`. Each entry:

```yaml
- counterparty: "Acme SaaS Oy"
  agreement: "Acme Platform Subscription Agreement"
  signed_date: 2025-06-15
  initial_term_end: 2026-06-15
  current_term_end: 2026-06-15           # rolls forward after each auto-renewal
  renewal_mechanism: "auto-renew annual"
  notice_period_days: 60
  notice_method: "email"                 # email / portal / kirjattu kirje (registered post) / per contract §X
  transit_buffer_days: 0                 # 0 for email; 5 for domestic registered post; 10 for international
  cancel_by_calendar: 2026-04-16         # current_term_end minus notice_period_days
  cancel_by_effective: 2026-04-16        # rolled back to last business day in governing-law jurisdiction
  send_by_effective: 2026-04-16          # cancel_by_effective minus transit_buffer_days
  cancel_by_roll_note: ""                # e.g., "rolled back from Sunday 2026-11-01"
  cancel_by_provenance: "[model calculation — verify against the notice clause]"
  hiljainen_uusiminen: false             # Finnish automatic renewal — flag explicitly
  price_on_renewal: "then-current list (uncapped)"
  annual_value_eur: 48000                # EUR (not USD)
  business_owner: "juha@company.fi"
  status: "active"                       # active | cancelled | renewed | lapsed
  notes: "Pricing uncapped — revisit before renewal."
```

**Rolling renewals:** Store `initial_term_end` for the record, but compute cancel-by dates from `current_term_end`. When a renewal fires (cancel window passes, no notice given), prompt:
> "This contract auto-renewed on [date]. Update the register: new `current_term_end` is [date + renewal period], new `cancel_by_effective` is [computed], new `send_by_effective` is [computed]. Confirm?"

**Transit time:** Alert off `send_by_effective`, not `cancel_by_effective`. A 60-day window with registered post (kirjattu kirje) is effectively ~55 days if transit_buffer_days is 5.

---

## Business-day check — EU governing law calendars

When computing or ingesting a cancel-by date, roll back to the last business day. Business day calendars depend on governing law jurisdiction:

- **Finnish law:** Finnish public holidays (yleiset pyhäpäivät) — Uudenvuodenpäivä, Loppiainen, Pitkäperjantai, Pääsiäinen, Vappu, Helatorstai, Juhannuspäivä, Pyhäinpäivä, Itsenäisyyspäivä, Joulu. `[model knowledge — verify against current Finnish holiday calendar]`
- **German law:** Federal holidays (gesetzliche Feiertage) plus Bundesland-specific holidays — if governing law is German, ask which Bundesland. `[model knowledge — verify]`
- **English law:** England and Wales bank holidays. `[model knowledge — verify]`
- **Other EU:** flag "Business-day roll-back uses [jurisdiction] as stated in governing law. Verify against [jurisdiction] public holiday calendar."

Roll BACK (never forward). Record both `cancel_by_calendar` (raw arithmetic) and `cancel_by_effective` (last effective business day), plus a `cancel_by_roll_note` if they differ.

---

## Finnish hiljainen uusiminen (automatic renewal) — explicit flag

Finnish law recognises hiljainen uusiminen — an agreement that renews automatically if neither party gives notice. This is common in Finnish commercial contracts and service agreements.

When adding a Finnish-law contract to the register, or when reviewing an agreement governed by Finnish law:
- Check explicitly for automatic renewal (hiljainen uusiminen) provisions.
- Flag these in the register: `hiljainen_uusiminen: true`.
- Output note: "This contract contains an automatic renewal clause (hiljainen uusiminen) under Finnish law. If no termination notice is given by [cancel_by_effective], the contract renews automatically for [renewal period]. Ensure the business owner is aware."

Do not assume a Finnish-law contract lacks this feature — it is often implied rather than explicit. If governing law is Finnish and the renewal mechanism is ambiguous, flag for review: "Finnish law may allow automatic renewal (hiljainen uusiminen) in the absence of an explicit notice-of-termination provision. Verify the renewal clause with local counsel. `[model knowledge — verify]`"

---

## Modes

### Mode 1: Ingest a renewal (handoff from review skill)

When `contract-review`, `nda-review`, or `vendor-agreement-review` finds an auto-renewal clause, it hands off a record. Append to register. If the counterparty already has an entry, ask: replacement (renewed agreement) or additional agreement?

When adding via `--add`: ask the user for each field. Pre-compute cancel_by_calendar, cancel_by_effective, send_by_effective. Show the computed dates and ask for confirmation before writing.

### Mode 2: What's coming up (default)

Default window: next 90 days. Urgency bands are half-open intervals:
- 🔴 **0–13 days** (send_by_effective in less than 14 days — including today)
- 🟠 **14–44 days**
- 🟡 **45–89 days**

Fire alerts off `send_by_effective`, not `cancel_by_effective`.

```markdown
## Renewals — next 90 days

### 🔴 Send notice within 0–13 days

| Counterparty | Send by | Cancel by | Renewal date | EUR/year | Owner | Notes |
|---|---|---|---|---|---|---|
| [name] | **[send_by]** | [cancel_by_effective] | [term_end] | [EUR] | [owner] | [notes] |

### 🟠 Send notice in 14–44 days

[same table]

### 🟡 Send notice in 45–89 days

[same table]

---

**Recommended actions:**
- [ ] [Counterparty] — ping [business_owner]: do we want to keep this?
- [ ] [Counterparty] — pricing is uncapped; get a quote from an alternative before losing leverage
- [ ] [Counterparty] — hiljainen uusiminen clause: ensure business owner is aware before [cancel_by_effective]
```

If register has more than ~10 renewals in window: offer a dashboard. Offer the sortable view with counts by urgency tier (🔴 / 🟠 / 🟡), cancel-by timeline, and EUR totals by band.

### Mode 3 (--days N): Change the window

Apply N days as the lookback horizon instead of 90. Same output format, same urgency bands.

### Mode 4 (--missed): Missed windows

```markdown
## Missed cancellation windows

| Counterparty | Cancel-by was | Renewal date | Status |
|---|---|---|---|
| [name] | [date] | [date] | Will auto-renew on [date] |

**Options:**
- Negotiate late cancellation (depends on vendor and relationship)
- Accept the renewal; mark next year's cancel-by now
- Check agreement for other termination rights (for convenience, for cause, change of control)
```

---

## Empty register

If `renewal-register.yaml` is missing or empty:

> "Your renewal register is empty. I can:
> 1. **Add a contract now** — tell me the counterparty, agreement name, renewal date, and notice period
> 2. **Walk through adding contracts** — I'll ask for each field one by one
> 3. **Accept handoffs from reviews** — run `/eu-legal:contract-review` or `/eu-legal:vendor-agreement-review` on a contract; if an auto-renewal clause is found, I'll add it to the register automatically"

---

## Gate: acting on a renewal

Tracking is research. Acting (sending a non-renewal notice, letting an auto-renewal fire, countersigning a renewal form) is a legal step with binding effect.

Before the user proceeds to act on a renewal:
> "Sending a termination / non-renewal notice or allowing an auto-renewal to fire past the cancel-by date has legal and contractual consequences. Have you confirmed the decision with the business owner and your legal team? If no, here's a brief to bring to them: [counterparty, term end, cancel-by date, what happens if no notice is given, next-period cost, and the three things to verify before the window closes]."

Do not proceed past this gate without an explicit yes.

---

## What this skill does not do

- It does not cancel contracts. It tells you when to decide.
- It does not decide whether to renew. It surfaces the deadline and the business owner.
- It does not read contracts to find renewal dates — that happens at review time via `contract-review` or `vendor-agreement-review`. If a contract is in the register without a computed cancel-by date, flag it as incomplete and ask the user to fill in the gap.
- It does not use Velvoite or require `VELVOITE_API_KEY`.

---

## Disclaimer

Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
