---
name: ip-assignment
description: >
  IP assignment audit — checks that all founders, employees, and contractors have
  properly assigned IP to the company. Flags gaps. Checks Business Finland IP
  restrictions if grants are active. Use when asking "do we own our IP",
  "IP assignment checklist", "does BF grant affect our IP", or before any M&A.
argument-hint: "[describe the company's IP situation]"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /fi-startup-legal:ip-assignment

1. Load profile. If placeholders, stop.
2. Call `mcp__velvoite__get_finnish_statute("KEKSINTOL")` — Laki oikeudesta työntekijän tekemiin keksintöihin (656/1967), the employee inventions act.
3. Run the IP audit workflow. Flag gaps. This is advisory — attorney review required.

---

## IP ownership checklist

### Founders
For each founder: did they sign an IP assignment agreement at incorporation? Does it cover:
- [ ] Code/software written before incorporation (if related to the business)
- [ ] Code/software written after incorporation
- [ ] Domain names, brand assets, trade secrets, know-how
- [ ] Any patents or patent applications

**Finnish employee invention rule (Laki oikeudesta työntekijän tekemiin keksintöihin):** An employer has the right to claim an invention made by an employee in the course of their employment duties. For founder-employees this is automatic — but a written IP assignment removes ambiguity.

Prior employer risk: if a founder previously worked for a company in this field, that employer may claim rights to inventions made during employment. Ask: "Did any founder work for another company in this field in the 12 months before starting this company?" If yes → route to outside counsel.

### Employees and contractors
- [ ] All employees: standard IP assignment clause in employment contract (covered by `/fi-startup-legal:first-hire-contract`)
- [ ] Contractors/freelancers: written IP assignment in each contractor agreement. Note: in Finland, software copyright vests in the author by default — contractor agreements MUST contain explicit assignment or the contractor retains copyright.

### Business Finland grants
If profile shows BF grants active: call this check.

BF funding terms: IP developed in the funded project must remain with the funded entity (same Y-tunnus). Key restrictions:
- Cannot transfer project IP to a subsidiary or affiliate without BF approval
- Control transfer outside EEA within 5 years of final funding installment requires prior BF approval
- "Control transfer" = change in majority ownership (direct or indirect)

Flag: is any M&A, restructuring, or foreign investor acquiring >50% planned? Route to outside counsel + notify BF.

---

## Guardrail

IP assignment gaps are the most common cause of failed M&A and VC due diligence in Finnish startups. Any gap identified here requires attorney action before the next funding round or exit process. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.
