---
name: books-and-records-map
description: >
  Maps the records a described system creates or holds — onboarding platform,
  investor portal, token admin console, CRM, messaging, approval workflow — to
  the records the broker-dealer must make and keep, and specifies an export the
  firm can retain and produce. Use when the user says "books and records",
  "what do we need to retain", "record retention map", "17a-4", "can the
  platform export this for the firm", "export spec", "exam request", or a
  vendor asks what the firm needs out of its system.
argument-hint: "[system description, schema, or path to a data dictionary]"
---

# /books-and-records-map

1. Load `~/.claude/plugins/config/claude-for-legal/broker-dealer-legal/CLAUDE.md` → books-and-records procedure, retention schedule, business lines.
2. Inventory what the system creates, receives, changes, and deletes.
3. Map each record type to a category in the fetched rule text and the firm's retention schedule. Mark gaps.
4. Output: a record map, a gap list, an export specification, and questions for the principal and counsel.

---

## Draft status

**This output is a draft for review by a registered principal and counsel. It is not legal advice.** It is a working map. It is not a conclusion that a system, a vendor, or a storage method satisfies Exchange Act Rules 17a-3 or 17a-4 or FINRA Rule 4511, not a retention schedule the firm can adopt without review, and never a decision on identification, accreditation, or suitability — those belong to the firm. The firm, not its vendor, is responsible for its records; nothing here shifts that.

## Purpose

The firm's records increasingly live inside someone else's software: the onboarding flow has the identification evidence, the token console has the transfer approvals, the chat tool has the investor conversations. When an examiner asks, the firm needs to produce them — complete, dated, unaltered, and readable. This skill finds out whether that is possible before anyone asks.

## Inputs — ask for what's missing

- **The system:** what it does for the firm, who operates it (firm or vendor), where it is hosted.
- **A data dictionary, schema, or screen-by-screen description.** If none exists, interview: what objects exist (customers, entities, documents, subscriptions, approvals, messages, transfers, wallet addresses, allow-list entries), what fields, what events are logged.
- **Lifecycle:** what can be edited or deleted, by whom; whether history is kept; what happens at contract termination.
- **Current export abilities:** formats, scope, who can run them.
- **The firm's retention schedule and books-and-records procedure.**
- **The firm's business lines and custody model** (from the profile) — they determine which record categories exist at all.

## Rule text check

The provisions relevant to this skill: Exchange Act Rule 17a-3 (records to be made), Rule 17a-4 (records to be preserved, including the conditions on electronic recordkeeping and on records held by third parties), FINRA Rule 4511 (general books-and-records requirements), FINRA Rule 3110 (evidence of supervisory review), FINRA Rule 2210 (records of communications and approvals), FINRA Rule 3310 with 31 CFR 1023.220 and 31 CFR 1010.230 (identification and beneficial ownership records), Securities Act Rule 506(c) (the verification record, as the firm keeps it), and Regulation S-P (safeguarding customer information in storage and export).

- **Fetch the current text of Rules 17a-3 and 17a-4 from ecfr.gov and FINRA Rule 4511 from finra.org before Step 2.** Tag each mapped category with its paragraph and `[rule text checked YYYY-MM-DD — <source>]`.
- **Never state from memory:** any retention period; which paragraph covers which record; the electronic recordkeeping conditions (including anything about audit trails, non-rewriteable storage, or third-party undertakings); or how quickly records must be produced. Each comes from the fetched text with a paragraph reference, or from the firm's retention schedule tagged `[firm procedure — retention schedule, dated X]`, or is left as `[rule text not checked — verify]`.
- If the rule text could not be fetched, the map is built against the firm's retention schedule only, and the output is headed accordingly. If neither is available, produce the system inventory (Step 1) and the export specification skeleton, and stop.
- Records requirements under provisions not on the plugin's list (for example, those specific to other registration categories or state law) are named as topics for counsel.

## Method

### Step 1: System inventory

One row per record type the system creates or holds:

| Record type | Created by (user / system / integration) | Key fields | Editable? Deletable? By whom? | History / audit log kept? | Timestamps (which, what timezone) | Attachments | Current export |
|---|---|---|---|---|---|---|---|

Include the records people forget: approval clicks and who clicked; rejected or abandoned applications; prior versions of edited data; screening results and their disposition; system-generated emails and notifications; chat and messaging; admin actions on the token contract (allow-list changes, freezes, forced transfers, mints, burns) and the off-chain approval behind each on-chain action; access logs; configuration changes to rules the system enforces.

### Step 2: Map to categories

For each record type: the category in the fetched text of Rule 17a-3 / 17a-4 or FINRA Rule 4511 it appears to fall under (paragraph reference), the retention period **from the fetched text or the firm's schedule**, and a confidence note. Where a record type could fall under more than one category or none clearly, mark `[review]` rather than choosing.

Do the reverse pass too: walk the firm's retention schedule and list every category the firm must keep for its business lines that this system might be expected to hold. Categories with no corresponding system record are gaps ("the firm must keep X; this system is where X happens; the system does not record X").

### Step 3: Gap list

Typical gaps to test for:
- records that can be edited or deleted with no retained history;
- approvals recorded as a status flag with no approver identity or timestamp;
- on-chain actions with no linked off-chain authorization record;
- communications in channels the system doesn't capture;
- documents stored as links to third-party locations that can change or expire;
- records purged on a schedule shorter than the firm's;
- no way to export everything for one customer, one offering, or one date range;
- exports that lose attachments, timestamps, or the link between records;
- records that exist only at the vendor with no agreed way for the firm to obtain them if the relationship ends;
- customer information exported or stored without the protections the firm's Regulation S-P procedures require.

Each gap gets a severity and an owner (vendor engineering / firm compliance / counsel).

### Step 4: Export specification

Write a specification the vendor can build to and the firm can test against. It is a proposal for the firm's review, not a statement of what the rules require.

- **Scope selectors:** by customer, by offering, by date range, by record type, and full export.
- **Contents:** every record type in the map; all fields; all prior versions; linked attachments in original format; the audit log entries for each record (who, what, when, before/after).
- **Identifiers:** stable IDs that link customer ↔ documents ↔ approvals ↔ subscriptions ↔ token actions ↔ on-chain transaction references.
- **Timestamps:** creation, each modification, each approval; stated timezone; source of time.
- **Format:** open, documented, human-readable without the vendor's software (for example CSV or JSON for data plus original files for documents, with a manifest); field dictionary included.
- **Integrity:** a manifest with file list, record counts, and hashes; the export itself logged.
- **Completeness evidence:** counts per record type that the firm can reconcile to the live system.
- **Delivery and access:** who at the firm can run it without vendor assistance; delivery to storage the firm controls; protection of customer information in transit and at rest.
- **Cadence:** on demand, and scheduled per the firm's procedure.
- **Exit:** full export on termination, in the same format, before any deletion.
- **Open design points for counsel** `[review]`: whether the firm's storage of the export, or the vendor's system itself, is intended to be the firm's record under Rule 17a-4's electronic recordkeeping conditions, and what those conditions then require of the storage and of the vendor. Do not answer this; pose it.

### Step 5: Test plan

Three tests the firm can run: export one known customer end-to-end and compare with the screens; export a date range and reconcile counts; edit a record and confirm the prior version and the edit event appear in the next export.

## Output

```markdown
[WORK-PRODUCT HEADER — per firm profile ## Outputs — no privilege header for vendor users]

> ⚠️ Reviewer note — Rule text: … · Procedures: [retention schedule dated X | not provided] · Read: … · Flagged: … · Before relying: …

## Books and Records Map — [system] — [firm] — as of [date]

### Bottom line
[N record types mapped, N unmapped `[review]`, N gaps (N 🔴). The system can / cannot currently export [scope]. Top 3 gaps.]

### Record map
| Record type | Category (rule ¶ / firm schedule line) | Retention (source) | Held in system? | History kept? | Exportable? | Note |
|---|---|---|---|---|---|---|

### Categories the firm must keep with no system record
| Category (source) | Where it happens today | Gap |
|---|---|---|

### Gap list
| # | Gap | Severity | Owner | Fix proposed |
|---|---|---|---|---|

### Export specification v0.1
[Step 4]

### Test plan
[Step 5]

### Questions for the principal and counsel
1. …
```

No customer data appears in the map. Use field names and record types, not sample values.

## Escalation points

- **To the CCO / supervising principal:** every 🔴 gap; any record that can be deleted or altered without history; any category the firm must keep that no system holds; adoption of the export specification and the retention periods.
- **To counsel:** the electronic recordkeeping question in Step 4; anything about a third party holding the firm's records; contract terms with the vendor on access, export, and exit; whether on-chain data alone can serve as any part of a required record; cross-border storage.
- **To the firm (when the user is the vendor):** every finding. The vendor does not decide what the firm's records are. Say: "This map is for the firm's compliance officer to review; I've written it so you can hand it over."
- **Stop and escalate:** a request to design deletion, editing, or off-system channels so that records are not retained.

## Config-dependent fallbacks

- **Retention schedule not indexed:** leave the Retention column as "per fetched rule text" or "not determined," never a remembered figure, and add an open item for the firm to supply its schedule.
- **Business lines not recorded:** ask before the reverse pass in Step 2.

## Close with the next-steps decision tree

Per CLAUDE.md `## Outputs`: turn the specification into a ticket set for the vendor, escalate the 🔴 gaps, send the counsel questions, schedule the test plan, or something else. Offer a dashboard view of the record map when it runs past ten rows.
