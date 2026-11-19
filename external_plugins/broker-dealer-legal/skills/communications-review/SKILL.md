---
name: communications-review
description: >
  Reviews a draft public or investor communication — web page, email, social
  post, deck, one-pager, data-room summary — against the firm's approval
  process, flags promissory, unbalanced, or unapproved statements, and produces
  a marked-up list plus a draft approval-log entry. Use when the user says
  "review this post", "can we send this to investors", "check this deck",
  "marketing review", "comms review", "is this promissory", or pastes
  investor-facing copy before it is used.
argument-hint: "[file path, URL of a draft, or paste the text] [--offering <name>]"
---

# /communications-review

1. Load `~/.claude/plugins/config/claude-for-legal/broker-dealer-legal/CLAUDE.md` → `## Communications approval`, exemptions, approver.
2. Establish what the piece is, who will see it, through which channel, and for which offering.
3. Read line by line. Flag promissory, exaggerated, unbalanced, unsupported, or unapproved statements.
4. Output: marked-up list, questions for the approver, and a draft approval-log entry with the approval left blank.

---

## Draft status

**This output is a draft for review by a registered principal and counsel. It is not legal advice.** It is a pre-review to make the approving principal's review faster. It is not approval of the communication, not a conclusion that the piece complies with FINRA Rule 2210 or is consistent with an offering exemption, and never a decision on identification, accreditation, or suitability — those belong to the firm. Nothing reviewed here may be used until the firm's approver has approved it under the firm's process.

## Purpose

Most problem communications are not fraudulent; they are enthusiastic. "Guaranteed," "can't lose," a projected return with no basis next to it, a benefits paragraph with the risks three clicks away. This skill reads the draft the way the approver will and hands back the lines to fix.

## Inputs — ask for what's missing

- The draft, complete, in the form the audience will see it (including images, captions, alt text, hashtags, linked landing pages, and footers — ask for them).
- **Audience and channel:** who receives it and how. Open to anyone, or a defined list? Existing customers, prospective investors, institutions?
- **Which offering**, if any, and the exemption that offering relies on (from the offering file or firm profile).
- **Who is the speaker:** the firm, a registered person, the issuer, a paid promoter, the vendor's platform.
- Whether an earlier version was approved (ask for the log entry).

If the draft is partial ("just check the headline"), do it, and head the output: `⚠️ SCOPE LIMITATION: only [X] was reviewed. The piece as the audience sees it has not been reviewed.`

## Rule text check

The provisions relevant to this skill: FINRA Rule 2210 (communications with the public — categories, content standards, approval, filing, recordkeeping), FINRA Rule 3110 (supervision and review of correspondence), FINRA Rule 2010 (the general standard), Securities Act Rules 506(b) and 506(c) (whether the offering may be generally solicited), Regulation Best Interest and FINRA Rule 2111 (only where the piece could be read as a recommendation), and FINRA Rule 4511 with Exchange Act Rule 17a-4 (keeping the communication and its approval).

- Fetch the current text of FINRA Rule 2210 from the FINRA rulebook at finra.org before classifying the piece or naming a content standard. Tag `[rule text checked YYYY-MM-DD — finra.org]`.
- **Never state from memory:** the definitions of the communication categories or any numeric line between them, which categories need principal approval before use, what must be filed with FINRA or when, any retention period, or the conditions on projections or performance. Use the fetched text with a paragraph reference, or tag `[rule text not checked — verify]` and present the point as a question for the approver.
- Advertising rules for investment advisers, state rules, and platform-specific rules are outside what this plugin cites. Name the topic and route it.

## Method

### Step 1: Classify — as a question, not an answer

Using the fetched definitions, state which FINRA Rule 2210 category the piece appears to fall into given audience and channel, and what the firm's process requires for that category. Present it as "appears to be [category] because [audience/channel fact] — approver to confirm `[review]`." If the audience facts are unknown, say classification is not possible and ask.

### Step 2: Solicitation check against the offering's exemption

If the piece relates to an offering:
- Offering recorded as **Rule 506(b)** and the piece is going to anyone beyond a defined, known audience → 🔴 `[review]` for counsel before any use. Say what the facts are (channel, reach); do not conclude that it is or is not general solicitation.
- Offering recorded as **Rule 506(c)** → note that the piece is consistent with the firm's recorded exemption only in the sense that solicitation is contemplated; flag any statement about who may invest for the approver.
- Exemption unknown → stop and ask.

### Step 3: Line-by-line read

Number every sentence, caption, and visual claim. Flag each that is:

| Flag | What to look for |
|---|---|
| **Promissory** | Guarantees or certainty about outcomes — "will," "guaranteed," "safe," "can't lose," "secured returns," "risk-free," certainty about liquidity, listing, or price |
| **Exaggerated / unwarranted** | Superlatives and claims with no stated basis — "best," "revolutionary," "institutional-grade," "fully compliant," "SEC-approved," "regulated token" |
| **Projection or performance** | Any forecast, target return, yield, hypothetical, back-test, or past performance figure — flag every one for the approver; do not assess whether an exception applies |
| **Unbalanced** | A benefit with no nearby, comparably prominent risk; risk disclosure only by link, footnote, or smaller type; omission of illiquidity, loss of principal, transfer restrictions, or technology risk where the piece discusses the upside |
| **Unsupported fact** | A number, ranking, partnership, licence, audit, or endorsement with no source in the file |
| **Regulatory status claim** | Anything implying a regulator approved or endorsed the offering, the token, or the platform; misuse of the firm's registration or membership as a quality mark |
| **Token-specific** | "Instant liquidity," "tradable 24/7," "on-chain = transparent = safe," price-appreciation language, staking or yield claims, statements about custody or insurance |
| **Recommendation-like** | Language that tells a person or a described class of persons that they should buy — raise Regulation Best Interest / FINRA Rule 2111 as a question for the principal |
| **Identity of speaker** | Unclear who is speaking; testimonial or paid promoter without the facts the approver needs; firm name absent or wrong |
| **Unapproved content** | Statements not found in the approved offering documents or inconsistent with them — quote both |

For each flag: quote the line, say why it is flagged in one sentence, and offer a neutral rewrite the approver can accept, edit, or reject. Rewrites remove the problem; they do not add new claims.

### Step 4: Check what is missing

Firm name and required identifications per the firm's house rules; risk language proportionate to the claims; date; source for third-party data; link destinations reviewed; consistency with the offering documents (amount, security, terms, eligibility).

### Step 5: Approval-process check

Has this piece (this version) been through the firm's process? Compare with the approval log. A changed version of an approved piece is a new piece — say so. If the piece is already in use without a log entry, report that fact to the approver and do not characterize it.

### Step 6: Draft the approval-log entry

Fill what is known; leave the approval decision, approver signature, and date blank.

## Output

```markdown
[WORK-PRODUCT HEADER — per firm profile ## Outputs]

> ⚠️ Reviewer note — Rule text: … · Procedures: … · Read: … · Flagged: … · Before relying: …

## Communications Pre-Review — [piece title] — v[N]

**Speaker:** …  **Audience / channel:** …  **Offering / exemption (as recorded):** …
**Apparent category:** … `[review]`

### Bottom line
[N lines flagged: N promissory, N projection/performance, N unbalanced, N unsupported. Not for use until [approver] approves. Top 3 fixes.]

### Marked-up list
| # | Line as drafted | Flag | Why | Suggested neutral rewrite | Severity |
|---|---|---|---|---|---|

### Missing from the piece
- …

### Questions for the approver / counsel
1. …

### Draft approval-log entry
| Field | Entry |
|---|---|
| Piece / version / date of draft | |
| Prepared by | |
| Speaker and channel | |
| Audience | |
| Offering and exemption (as recorded) | |
| Apparent category under FINRA Rule 2210 | `[review]` |
| Changes requested in pre-review | [N items — see marked-up list] |
| Filing with FINRA required? | *(approver to determine)* |
| **Approved / not approved** | ______ *(approver only)* |
| **Approver name, signature, date** | ______ |
| First-use date | |
| Where the final version is retained | |
```

## Escalation points

- **To the communications approver (named in the firm profile):** every piece. Specifically: every projection or performance figure; every testimonial or paid promotion; any piece already in use without a log entry.
- **To counsel:** any Rule 506(b) offering communication going beyond a known audience; any statement about regulatory status, registration, or legal characterization of a token; any communication prepared or distributed by the issuer, a promoter, or the vendor in which the firm's role is unclear; any promoter who is being paid (run `/broker-dealer-legal:intermediary-compensation-check`).
- **Stop and escalate:** a request to make the piece "pass" without changing the substance, to post before approval, or to move a claim to a channel the firm doesn't retain.

## Config-dependent fallbacks

- **Approver or log location not configured:** produce the review, leave those fields as "not configured," and say the entry cannot be filed until they are.
- **House rules empty:** note that only the general flags above were applied.

## Close with the next-steps decision tree

Per CLAUDE.md `## Outputs`: produce a clean revised draft with accepted rewrites, send to the approver with the log entry, send the counsel questions, hold the piece, or something else.
