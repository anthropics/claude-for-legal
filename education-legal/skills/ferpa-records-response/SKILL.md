---
name: ferpa-records-response
description: >
  Respond to a records request under FERPA (34 CFR Part 99). Identifies
  education records vs. excluded categories (sole-possession notes,
  law-enforcement-unit records, employment records, treatment records); applies
  the consent-vs-exception framework; redacts PII; logs the access under
  §99.32; drafts the response letter within the 45-day federal default (or
  shorter state window). Use when the user says "FERPA records request",
  "records subpoena", "parent wants records", "third party records request",
  "directory information request".
argument-hint: "[the request letter or describe the requester, scope, and basis]"
---

# /ferpa-records-response

1. Load `~/.claude/plugins/config/claude-for-legal/education-legal/CLAUDE.md` → state(s), records custodian, directory-information policy, response window, access-log location.
2. Walk the workflow below.
3. Identify scope, requester status, consent/exception basis. Redact appropriately.
4. Draft the response letter and the §99.32 log entry. Track the response window.

---

## Matter context

Check `## Matter workspaces`. Practice-level by default for district counsel; per-matter for advocacy.

---

## Purpose

FERPA records responses look routine until they aren't. The hard parts are: (a) figuring out what's an education record vs. what's excluded, (b) figuring out whether consent or an exception applies, and (c) redacting in a way that doesn't either over-protect (refusing what the requester is entitled to) or under-protect (releasing another student's PII).

## Load context

Per CLAUDE.md. Read `## FERPA` and `## Jurisdictional footprint`.

## Output header

Per CLAUDE.md `## Outputs`. **Strip the privileged header from the response letter that goes to the requester.**

## Workflow

### Step 1: Identify the requester

| Requester | Default basis |
|---|---|
| Parent of a student < 18 | Right of access under 34 CFR §99.10 |
| Eligible student (≥ 18 or attending postsecondary — K-12 default cuts off at 18) | Right of access transfers to the student under §99.5 |
| Third party with written consent | §99.30 |
| Third party under a §99.31 exception | School official with legitimate educational interest, other school, authorized representatives of audit/eval, financial aid, court order/subpoena, health/safety emergency, parent of a dependent student under IRC, directory information (subject to opt-out), etc. |
| Third party without consent or exception | No release |

Surface the requester's status explicitly. If status is ambiguous (e.g., a parent post-18 — eligible student now controls; a non-custodial parent — generally has same rights as custodial parent unless a court order specifically revokes those rights under §99.4), flag and ask.

### Step 2: Identify the scope of "education records"

Education records = records directly related to a student and maintained by an educational agency or institution or by a party acting for it (§99.3).

**Excluded from education records** (do NOT produce):
- **Sole-possession records** — records kept in the sole possession of the maker, used only as a personal memory aid, and not accessible to or revealed to anyone except a temporary substitute for the maker (§99.3 exclusion (b)(1)). Teacher's personal classroom notes, kept in their desk, never shared — excluded.
- **Law-enforcement-unit records** — records created and maintained by a law-enforcement unit of the institution for a law-enforcement purpose (§99.3 exclusion (b)(2), §99.8).
- **Employment records** — records relating to a person who is employed by the agency and that relate exclusively to the person in that capacity and are not available for use for any other purpose (§99.3 exclusion (b)(3)).
- **Treatment records** for postsecondary students 18+ when used only for treatment (excluded under §99.3 (b)(4) — primarily relevant in higher ed).
- **Records created after the student is no longer in attendance** that are not directly related to the student's attendance (§99.3 (b)(5)).
- **Grades on peer-graded papers** before they're collected and recorded by the teacher (Owasso Indep. Sch. Dist. No. I-011 v. Falvo, 534 U.S. 426 (2002)).

Apply the exclusions before deciding the response.

### Step 3: Apply the consent or exception framework

If the requester is a parent or eligible student requesting their own records: produce, subject to redaction of third-party PII.

If a third party with consent: verify the consent is in writing, signed and dated, specifies the records, the purpose, and the party to whom disclosure may be made (§99.30(b)). Produce subject to redaction.

If a third party under a §99.31 exception: identify the specific exception. Document the basis. Produce subject to the exception's limits.

If directory information: check whether the parent has opted out. The district's directory-information policy (in the practice profile's `## FERPA`) lists which categories are designated and the opt-out posture.

**Health/safety emergency exception (§99.36).** Specific knowledge of an articulable and significant threat. Document the threat, the recipients, the information disclosed, and the legal basis (§99.32(a)(5)).

**Court order / subpoena (§99.31(a)(9)).** Make a reasonable effort to notify the parent or eligible student in advance, except in specific circumstances (grand jury, law enforcement subpoena marked not-for-disclosure). Document. Cite the court order or subpoena.

### Step 4: Redact

When the records contain information about other students or about identifiable third parties whose consent has not been obtained, redact before release. Redact:
- Names of other students.
- Identifiable details about other students (specific dates, specific event narratives that identify by elimination).
- Educator personnel-file information unrelated to the student.

**Do NOT redact** content the requester is entitled to: the substance of the requesting student's own records, including evaluations, IEP/504 plans, discipline records, and progress reports.

Specifically for **a student's IEP**: parents are entitled to a copy under IDEA at no cost (34 CFR §300.322(f)) — separate from the FERPA framework. Don't refuse an IEP request under a FERPA argument.

### Step 5: Track the response window

- **Federal default:** 45 days from receipt of request (34 CFR §99.10(b)).
- **State overlay:** some states (e.g., California Ed Code §49069) impose shorter windows. Check the practice profile.
- **For IEP-specific requests under IDEA:** the LEA must comply with a request without unnecessary delay and before any IEP meeting, due-process hearing, or resolution session (34 CFR §300.613(a)).

> **Research the operative state window. Cite. Verify.**

### Step 6: Log the access under §99.32

For each release of personally identifiable information from education records (other than to the parent, eligible student, school officials with legitimate educational interest under §99.31(a)(1), authorized state/federal officials under §99.31(a)(3), directory information disclosures, or disclosures with written consent), log:

- The parties who have requested or received personally identifiable information.
- The legitimate interests the parties had in requesting or obtaining the information.

The log is part of the student's education records and must be made available to the parent or eligible student. Use the access-log location in the practice profile.

### Step 7: Draft the response letter

Components:
- Acknowledge receipt.
- State the records being produced.
- State the records being withheld and the basis (excluded under §99.3(b)(X); third-party PII redacted under §99.31).
- Note the right to challenge content under §99.20.
- Note the right to file a FERPA complaint with the Family Policy Compliance Office at the U.S. Department of Education if the requester believes there's been a violation.

Strip the work-product header from the response letter.

## Output

```markdown
[WORK-PRODUCT HEADER on the internal analysis]

## FERPA Records Response: [Requester] — re: [Student initials]

### Requester status
[Parent | Eligible student | Third party with consent | Third party under §99.31(a)(X) exception | Other]
[Documentation: consent form / court order / health-safety basis / etc.]

### Records identified — produce / withhold table
| Record | Education record? | Produce / Withhold / Redact | Basis |
|---|---|---|---|
| | | | |

### Redactions
[Categories of third-party PII redacted; cite §99.31.]

### Timeline
- Request received: [date]
- Federal 45-day deadline: [date]
- State window (if shorter): [date — cited]
- IDEA pre-meeting requirement (if applicable): [date]

### §99.32 access log entry
- Released to: [party]
- Legitimate interest: [basis]
- Records: [enumerated]
- Date: [date]

### Response letter (clean — strip privileged header)
[Drafted letter]
```

## Consequential-action gate

Before releasing records under an exception that doesn't require consent (especially health/safety emergency, court order with notification obligations, law-enforcement-unit handoffs):

> Releasing records without consent under a §99.31 exception has the potential to: (a) trigger a FERPA complaint if the exception is misapplied, (b) expose the district to a damages claim if any state-law privacy right is implicated, and (c) intersect with discovery rules if there's pending litigation. Have you reviewed the specific exception with an attorney? If yes, proceed. If no, here's the brief: [requester, basis, exception cited, what's being released, what's withheld].

---

## Close with the next-steps decision tree

Per CLAUDE.md.

## What this skill does NOT do

- **Apply IEP-specific access rules without flagging IDEA's separate framework.** Parents have IEP access rights under IDEA independent of FERPA. The skill calls this out.
- **Skip directory-information opt-out check.** Always check the practice profile's policy.
- **Release without logging.** Every non-exempt release goes in the §99.32 log.
- **Decide whether a redaction is sufficient on its own.** Surfaces the redactions; the records custodian and counsel sign off.
