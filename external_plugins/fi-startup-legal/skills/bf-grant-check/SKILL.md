---
name: bf-grant-check
description: >
  Business Finland grant IP compliance check — assesses whether a planned
  action (M&A, restructuring, foreign investment, IP transfer) triggers the
  5-year EEA control transfer restriction or IP retention requirement.
  Use when asking "can we sell to a US company", "does this VC deal affect
  our BF grant", "IP clawback risk", or before any major transaction.
argument-hint: "[describe the planned transaction or situation]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /fi-startup-legal:bf-grant-check

1. Load profile — check Business Finland grants active flag.
2. If no BF grants: "No Business Finland grants recorded in your profile. If you have grants, update via `/fi-startup-legal:startup-cold-start --redo`."
3. If BF grants active: run the compliance check below.

---

## Business Finland IP and control transfer restrictions

### IP retention requirement
IP developed in the BF-funded project must remain with the funded entity (same Y-tunnus) throughout the project and for a retention period after. Key rule: the IP cannot be transferred to a subsidiary, affiliate, or third party without BF approval.

**Triggers requiring BF notification or approval:**
- [ ] Transferring project IP to a new holding company
- [ ] Assigning patents or copyright from the funded entity to any other entity
- [ ] Licensing project IP exclusively to a single party (may be treated as transfer)
- [ ] M&A where the funded entity ceases to exist (merger, absorption)

### EEA control transfer restriction (5-year rule)
Within 5 years of receiving the final BF funding installment: a control transfer outside the European Economic Area requires prior BF approval.

**Note on the 5-year measurement period:** The 5 years runs from the **date of final payment** of the last funding installment, which may differ from the project completion date. Founders frequently miscalculate by measuring from project end rather than final payment. Check the payment history in your grant portal.

**"Control transfer"** = a change resulting in a non-EEA entity (person or company) acquiring direct or indirect majority control (>50% of shares or voting rights).

**Important:** The >50% threshold is the standard baseline, but **your specific grant agreement controls**. Some Business Finland programs (particularly large R&D and TUTLI grants post-2020) define control more broadly — some trigger at "significant influence" or use a lower ownership threshold. Always verify the exact wording in your grant agreement before assuming >50% is the trigger. When in doubt, contact Business Finland directly before proceeding with any transaction.

**Triggers (check all):**
- [ ] New investor acquires >50% of shares
- [ ] Existing non-EEA investor's stake crosses 50% threshold
- [ ] M&A where acquirer is headquartered outside EEA
- [ ] Complex ownership structures where indirect non-EEA control crosses 50%

**Foreign LP risk:** If a VC fund has non-EEA LPs, the fund itself is typically the direct shareholder — not the LPs. Whether LP-level non-EEA ownership constitutes "indirect control" requires case-by-case BF analysis. **Route to outside counsel + BF inquiry for any fund with significant non-EEA LP exposure.**

### Clawback
Non-compliance can result in full or partial recovery (clawback) of the grant. BF has discretion — cooperation and proactive notification typically reduces risk.

### Next steps
If a planned transaction may trigger these restrictions:
1. Do not proceed without checking
2. Contact Business Finland directly (puh. 029 5069 000 or businessfinland.fi/yhteystiedot)
3. Engage a lawyer familiar with BF grant terms

---

## Guardrail

This check identifies potential BF grant compliance issues. Business Finland grant terms vary by program and year — always review the specific grant agreement. This is not legal advice; route any material transaction to outside counsel and notify BF proactively. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
