---
name: non-compete-check
description: >
  Validate a Finnish non-compete clause against TSL §3:5 — maximum duration,
  compensation requirements, scope reasonableness. Use when reviewing or
  drafting a non-compete, or asking "is this non-compete valid in Finland",
  "do we need to pay for non-compete", "how long can a non-compete be".
argument-hint: "[describe or paste the non-compete clause]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /fi-startup-legal:non-compete-check

1. Load profile.
1.5. **Framework gate:** Before applying TSL §3:5, confirm the non-compete is in an employment agreement (governed by TSL). If it appears to be in any of the following, halt and flag:
   - SHA (shareholders' agreement / osakassopimus) → TSL §3:5 does not apply; governed by contract law. Route to `/fi-startup-legal:sha-review` or commercial counsel.
   - Board member service agreement → TSL does not apply to board members.
   - Consulting/contractor agreement → classification must be confirmed first (TSL only applies to employees); run `/fi-startup-legal:non-compete-check` only after confirming employment status.
2. Call `mcp__velvoite__get_finnish_statute("TSL", "3:5")` — fetch current non-compete statute text.
3. Call `mcp__velvoite__search_kho_decisions` for the current and two prior years. Fetch each listing URL and identify any decisions whose title relates to non-compete clauses (kilpailukielto), employment restrictions, or TSL §3. Call `mcp__velvoite__get_kho_decision(year, number)` for each relevant case and fetch the full text URL. Surface relevant precedents in the validation output as: "> KHO:[year]:[number]: [one-line holding on what the court required or invalidated]." If none found, omit.
4. Validate against the live statute. Flag any issues.

---

## Validation (from live statute text)

Apply the fetched TSL §3:5 text to check:

### Duration
- Maximum: 12 months after employment ends
- If restriction > 12 months: **INVALID** under Finnish law — clause is unenforceable beyond 12 months

### Compensation requirement

**Compensation rates (TSL §3:5, effective 1 January 2022):**
- Restriction of **6 months or less**: no compensation required
- Restriction of **more than 6 months up to 12 months**: employer must pay **40% of monthly salary** for each month of the restricted period
- Restriction of **more than 6 months** (alternative framing used in some agreements): **60% of monthly salary** if the restriction materially prevents earning a living in the field

Note: The pre-2022 "50% flat rate" is obsolete. Agreements referencing 50% may be non-compliant with current law.

- Payment timing: typically monthly during the restriction period
- If compensation is required but not included in the contract: **RED — clause may be unenforceable**

**Employer's right to release early:** Since the 2022 reform, the employer can unilaterally release the employee from a non-compete obligation during the restricted period (with reasonable notice). Release eliminates the compensation obligation going forward — relevant when the business changes direction or a founder leaves amicably.

### "Particularly weighty reason" requirement
Finnish law requires a "particularly weighty reason" (erityisen painava syy) for a non-compete to be valid. Legitimate reasons: access to trade secrets, customer relationships, sensitive competitive information. A blanket non-compete for all employees regardless of role is vulnerable.

Ask: does the employee have access to genuine trade secrets or key customer relationships? If no clear justification: **AMBER — validity risk**.

### Geographic scope
Unreasonably broad geographic scope (e.g. entire world for a role with no international dealings) is a validity risk. Finnish courts assess reasonableness.

### Scope of activities restricted
Must be related to the employee's actual duties and the employer's actual business. "Any employment in any competing company" without qualification is too broad.

## Output

| Issue | Status | Recommendation |
|---|---|---|
| Duration (max 12 months) | ✓/✗ | |
| Compensation (if >6 months) | ✓/✗ | |
| Weighty reason documented | ✓/✗ | |
| Scope reasonable | ✓/✗ | |

---

## Guardrail

Non-compete enforceability depends on facts and circumstances. Finnish courts have voided overly broad non-competes. This check identifies clear legal issues — full enforceability assessment requires legal advice. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
