---
name: policy-drafting
description: >
  Draft employment policies in EU-compliant form — remote work, employee
  monitoring, AI use (employee-facing), whistleblower reporting, and equal
  treatment. Includes works council consultation requirements, GDPR Art. 88
  limits on employee data, Finnish privacy-in-working-life rules, and German
  BetrVG co-determination rights. Use when asked to "draft a remote work
  policy", "write an employee monitoring policy", "whistleblower policy",
  "AI use policy for employees", or "equal treatment policy".
argument-hint: "[policy type] — e.g. 'remote work policy', 'employee monitoring', 'whistleblower', 'AI use policy', 'equal treatment'"
version: 0.1.0
owner: Silly Pilot Oy
last_reviewed: 2026-06-01
---

# /eu-legal:policy-drafting

1. Load `~/.claude/plugins/config/eu-legal/CLAUDE.md`. If placeholders, stop: "Run `/eu-legal:cold-start-interview` first."
2. Load `~/.claude/plugins/config/eu-legal/employment.md` if it exists. Read: hiring countries, de_betriebsrat_exists, fi_yt_laki_applies, total_headcount, whistleblower_channel_required.
3. Identify the policy type from the argument.
4. Run the applicable framework below.
5. Output: draft policy for attorney review, with a pre-rollout checklist of consultation requirements.

---

## Purpose

Employment policies create legal obligations as well as rights. A monitoring policy that doesn't comply with GDPR Art. 88 or the Finnish privacy-in-working-life act exposes the employer to DPA enforcement. A whistleblower policy that doesn't meet Directive 2019/1937 requirements exposes the employer to national authority fines. A policy rolled out in Germany without Betriebsrat approval under §87 BetrVG may be void. This skill drafts compliant first drafts and identifies what must happen before the policy is communicated.

---

## Step 1: Identify policy type and collect context

From the argument, identify which policy type to draft. If not specified, ask:
> "Which policy would you like to draft? (1) Remote work / (2) Employee monitoring / (3) AI use for employees / (4) Whistleblower reporting / (5) Equal treatment"

Also collect (if not in employment.md):
- Primary jurisdiction for the policy (Finland / Germany / both)
- Approximate headcount (for whistleblower threshold check)
- Applicable collective agreement (TES/Tarifvertrag) — may have policy-specific requirements

---

## Policy type 1: Remote Work Policy

### Legal basis
- EU: Transparent and Predictable Working Conditions Directive (2019/1152) — employee has right to request flexible arrangements; employer must respond within reasonable time
- Finland: TSL Ch. 2 §13a — right to request remote work; employer must give reasoned refusal
- Germany: no statutory right to remote work (Homeoffice-Gesetz proposal did not pass), but request right exists in some Tarifverträge; BetrVG §87(1) No. 14 — co-determination right on "mobile working" since 2021

### Works council consultation (before rollout)
- **Finland (≥20 employees):** If policy changes existing practice or introduces new monitoring requirements → YT-laki §16 procedure required before implementation
- **Germany (Betriebsrat exists):** BetrVG §87(1) No. 14 — employer must negotiate a Betriebsvereinbarung on mobile work before implementing a company-wide remote work policy. Cannot act unilaterally.

### GDPR / Data protection requirements
- If remote work involves monitoring home office equipment: GDPR Art. 88 applies (employee data processing)
- Proportionality: monitoring must be necessary and proportionate; no keystroke logging or continuous camera surveillance
- Finland: Laki yksityisyyden suojasta työelämässä (759/2004) — employer can only process employee data for purposes directly related to employment; must inform employees of monitoring

### Draft policy template

```
REMOTE WORK POLICY
[Company name] — effective [DATE]
[Version: DRAFT — FOR ATTORNEY REVIEW AND WORKS COUNCIL CONSULTATION BEFORE ROLLOUT]

1. SCOPE
This policy applies to all employees of [Company] working remotely on a regular or occasional basis. "Remote work" means work performed at a location other than the company's designated workplace, including home, co-working spaces, and other locations.

2. ELIGIBILITY
Remote work is available to employees in roles where work can be performed effectively outside the office, as determined by the employee's manager. Remote work availability depends on role requirements, performance, and operational needs.

3. REQUESTING REMOTE WORK
Employees may request regular remote work arrangements. Requests should be made in writing to the employee's manager and HR. The company will respond within [30 days] with either approval, a modified proposal, or a reasoned refusal. A reasoned refusal must state the business reason why the request cannot be accommodated.

4. WORKING HOURS AND AVAILABILITY
Employees working remotely remain subject to their contracted working hours and the [Finnish/German] Working Hours Act / Arbeitszeitsgesetz. Core hours of availability: [e.g., 09:00–15:00 local time, Monday–Friday]. Outside core hours, employees may organise their time flexibly, subject to applicable working time limits.

5. HEALTH AND SAFETY
The employee is responsible for ensuring their remote workspace meets basic ergonomic and safety requirements. The company will provide guidance on workspace requirements. Employer occupational health and safety obligations (Finnish occupational safety and health act / German ArbSchG) apply to remote work locations to the extent practicable.

6. DATA SECURITY
Employees must follow the company's information security policy when working remotely: use VPN, lock screens when unattended, do not use public Wi-Fi without VPN, and store work documents on company-approved systems only.

7. EQUIPMENT
[Employer-provided equipment]: The company provides [laptop, headset, monitor — list]. Employees are responsible for maintaining equipment in working order.
[Employee-provided equipment (BYOD)]: If using personal equipment, the employee must ensure it meets the company's security requirements.

8. MONITORING
[Employer note: any monitoring tools must be described here. Apply the monitoring policy framework — see Policy type 2 — before inserting monitoring terms. Do not include monitoring without GDPR Art. 88 / privacy-in-working-life compliance review.]

9. COSTS AND EXPENSES
[Finland: employer typically reimburses reasonable additional costs per TES or agreement]
[Germany: employer pays Aufwendungsersatz per §670 BGB for expenses caused by remote work; internet costs: employer pays a reasonable share if employee uses home internet for work]

10. CHANGE OR WITHDRAWAL
Either party may request a change to a regular remote work arrangement with [1 month] notice. The company may withdraw remote work access for business reasons with reasonable notice, except where a permanent arrangement has been agreed in the employment contract.

11. APPLICABLE LAW
This policy is governed by [Finnish / German] employment law and the employee's employment contract.

---
[REVIEWER NOTE: This policy must be reviewed by employment counsel before rollout. In Germany: Betriebsvereinbarung required under BetrVG §87(1) No. 14 — do not communicate this policy to employees until works council agreement is in place. In Finland: if changing existing practice for ≥20 employees, YT-laki §16 consultation required before implementation.]
```

---

## Policy type 2: Employee Monitoring Policy

### Legal basis
- GDPR Art. 88 — member states may provide specific rules on employee data processing; proportionality and necessity required
- Finland: Laki yksityisyyden suojasta työelämässä (759/2004) §4 — employer may only process personal data that is directly necessary for the employment relationship; employee must be informed of monitoring; most monitoring requires prior notification and YT-laki consultation
- Germany: BetrVG §87(1) No. 6 — introduction and use of technical devices capable of monitoring employee performance or behaviour requires Betriebsrat co-determination

### Works council consultation (before rollout)
- **Germany:** BetrVG §87(1) No. 6 is a mandatory co-determination right. No monitoring system — email logs, access logs, key card records, screen monitoring, GPS tracking, call recording, productivity tools — may be introduced without a Betriebsvereinbarung. This is not a consultation requirement; it is a consent requirement. Unilateral introduction = void measure.
- **Finland (≥20 employees):** YT-laki §16 — introduction of monitoring systems that affect working conditions requires YT-neuvottelut before implementation.

### What monitoring is permissible under Finnish privacy-in-working-life act (759/2004)

| Monitoring type | Permissible? | Requirements |
|---|---|---|
| Access logs (who entered building, when) | Yes, if proportionate | Must inform employees; YT consultation if ≥20 |
| Email content monitoring | Only if specific grounds (security investigation, work completion) | Must inform; cannot monitor content routinely |
| Internet access logs (which sites visited) | Yes, if proportionate and work-related | Must inform employees |
| Keystroke logging / screen recording | No (disproportionate as routine monitoring) | Not permitted |
| GPS tracking (company vehicles) | Yes, if work-related | Inform employees; cannot track off-duty |
| Productivity software (output metrics) | Yes, if non-invasive | Inform employees; YT consultation |
| AI-based performance scoring | Permitted only with safeguards | GDPR Art. 22 profiling restrictions; must inform; YT consultation |

### Draft policy template

```
EMPLOYEE MONITORING POLICY
[Company name] — effective [DATE]
[Version: DRAFT — FOR ATTORNEY REVIEW AND WORKS COUNCIL CONSULTATION BEFORE ROLLOUT]

1. PURPOSE AND LEGAL BASIS
[Company] monitors certain employee activities to ensure the security of company systems, compliance with company policies, and the effective operation of the business. This policy describes what is monitored, why, and how information is used.

Legal basis for processing: [Article 6(1)(b) GDPR — necessary for performance of the employment contract; Article 6(1)(f) GDPR — legitimate interests in IT security and compliance]. Processing of sensitive data categories requires Article 9 basis — state if applicable.

2. WHAT WE MONITOR

We monitor the following:
- IT system access logs: which systems were accessed, when, and from which device. Purpose: IT security, incident investigation.
- Company email metadata: sender, recipient, subject line, timestamps. Purpose: security, compliance. [Note: email content is NOT routinely monitored. Content may be accessed only for specific security or legal investigation purposes, following the procedure in section 6.]
- Internet access logs: which domains were accessed from company networks or devices. Purpose: security, policy compliance.
- Building access logs: entry/exit records from key card systems. Purpose: site security.
- [Company vehicles only:] GPS location during working hours. Purpose: fleet management, safety.

We do NOT monitor:
- Keystroke logging or screen recording during normal work
- Personal devices used for private purposes
- Personal email or personal social media accounts
- Location outside working hours

3. HOW MONITORING DATA IS USED
Monitoring data is used only for the purposes stated above. Access to monitoring data is restricted to IT security team, HR (in HR-related investigations), and management (for business purposes). Monitoring data is not used for automated individual decision-making (GDPR Art. 22) without human review.

4. RETENTION
Monitoring data is retained for [90 days] for IT logs; [30 days] for access logs; unless longer retention is required for an ongoing investigation.

5. EMPLOYEE RIGHTS
Employees have the right to access their own monitoring data (GDPR Art. 15), to request correction of inaccurate data (Art. 16), and to object to processing where it affects their fundamental rights (Art. 21). Contact [data protection contact] to exercise these rights.

6. INVESTIGATIONS
If monitoring data suggests a security incident, policy violation, or other concern, the company may initiate an investigation. Any investigation involving review of personal communications (e.g., email content) will be conducted with prior authorisation from [HR lead / Legal] and with notice to the employee unless legal proceedings require confidentiality.

7. WORKS COUNCIL
[Germany: This policy was agreed with the Betriebsrat by Betriebsvereinbarung dated [DATE]. [Leave blank until agreement in place — do not rollout without.]]
[Finland: This policy was developed following YT-laki §16 consultation with employee representatives on [DATE].]

---
[REVIEWER NOTE: Before rollout — Germany: Betriebsvereinbarung required under BetrVG §87(1) No. 6. Finland: YT-laki §16 consultation required for ≥20 employees. Remove any monitoring type not explicitly stated here before communicating to employees — adding monitoring later requires a new consultation cycle.]
```

---

## Policy type 3: AI Use Policy (Employee-Facing)

### Legal basis
- EU AI Act (Regulation 2024/1689) — transparency and information obligations for AI systems interacting with employees (Art. 50); high-risk AI for employment, HR, and worker management subject to conformity assessment (Annex III)
- GDPR Art. 22 — right not to be subject to solely automated decisions with significant effect; applies to AI-based performance evaluation, promotion decisions, disciplinary AI systems
- Finland: Laki yksityisyyden suojasta työelämässä (759/2004) — employee data processing; AI systems are subject to same proportionality standard
- Germany: BetrVG §87(1) No. 6 — AI performance monitoring tools trigger co-determination right. §90+91 BetrVG — employer must consult Betriebsrat before introducing new work processes (including AI tools)

### Works council consultation
- **Germany:** Any AI tool that monitors performance, schedules work, or evaluates output requires Betriebsvereinbarung under §87(1) No. 6 before deployment to employees.
- **Finland (≥20 employees):** Introduction of AI tools that materially affect how work is done or monitored → YT-laki §16 procedure.

### Draft policy template

```
AI TOOLS POLICY FOR EMPLOYEES
[Company name] — effective [DATE]
[Version: DRAFT — FOR ATTORNEY REVIEW AND WORKS COUNCIL CONSULTATION BEFORE ROLLOUT]

1. SCOPE
This policy applies to all employees using AI tools provided by [Company], or using externally available AI tools for work purposes.

2. APPROVED AI TOOLS
The following AI tools are approved for use at [Company]:
[List approved tools, e.g.: GitHub Copilot (coding only), Claude / ChatGPT (drafting and research), internal AI assistant (describe scope)]

Using AI tools not on this list for work purposes requires prior approval from [IT/Legal/manager — specify].

3. WHAT YOU MUST NOT ENTER INTO AI TOOLS
Do not enter into any AI tool (including approved tools):
- Personal data of clients, employees, or third parties, unless the tool is explicitly approved for this and data processing terms are in place
- Confidential company information (financial data, unreleased products, M&A discussions) into consumer-grade AI tools
- Source code that is not already public, unless using a tool with code privacy guarantees (e.g., GitHub Copilot with enterprise data protection)
- Passwords, API keys, or credentials

4. ACCURACY AND VERIFICATION
AI tools can produce incorrect, outdated, or fabricated output. You are responsible for verifying AI-generated content before using it in customer communications, legal documents, financial calculations, or other consequential outputs. Treating AI output as final without review is a policy violation.

5. AI-BASED PERFORMANCE TOOLS
[If company uses AI for performance assessment or work allocation]: [Company] uses [tool name] for [purpose]. This tool processes [what data] for the purpose of [what decisions]. Human review is applied to all significant decisions affecting individual employees. You have the right to request human review of any individual decision made with significant AI input — contact [HR contact].

The use of AI for employment-related decisions that significantly affect you (performance ratings used for pay, promotion, or disciplinary action) is subject to GDPR Art. 22 safeguards. You have the right to: (a) know that an automated system was used, (b) obtain an explanation, (c) request human review of the decision.

6. INTELLECTUAL PROPERTY
AI-generated output created in the course of your employment belongs to [Company] under standard IP assignment terms. Verify before publishing or using AI-generated work that you hold or the company holds the necessary rights.

7. WORKS COUNCIL
[Germany: The introduction of AI performance monitoring tools described in section 5 was agreed with the Betriebsrat by Betriebsvereinbarung dated [DATE].]
[Finland: This policy was developed following YT-laki §16 consultation with employee representatives on [DATE].]

---
[REVIEWER NOTE: Before rollout — Germany: any AI tool that monitors performance or outputs requires Betriebsvereinbarung. Finland: YT-laki consultation for ≥20 employees before rollout. Check whether any AI tool used for employment decisions (performance, scheduling, candidate screening) qualifies as high-risk under EU AI Act Annex III — if so, conformity assessment required before deployment.]
```

---

## Policy type 4: Whistleblower Reporting Policy

### Legal basis
- EU Whistleblower Directive 2019/1937 — mandatory internal reporting channel for:
  - Private sector employers ≥50 employees
  - All public sector employers
- Finland implementing act: Laki ilmoittajansuojelusta (1171/2022) — in force from 1 January 2023 for employers ≥50 employees
- Germany implementing act: Hinweisgeberschutzgesetz (HinSchG) — in force from 2 July 2023 for employers ≥50 employees (private sector ≥250 from 2 July 2023; ≥50 from 17 December 2023)

### Mandatory requirements

**Reporting channel requirements (both Directive and implementing acts):**
- Secure, confidential channel that allows both written and verbal reporting
- Channel must allow anonymous reporting (employer must accept anonymous reports, though cannot compel reporter to identify themselves)
- Designated impartial person or department to handle reports
- Acknowledgement within 7 days of receiving report
- Feedback to reporter within 3 months (6 months with extension)
- No retaliation against reporter — null and void

**Scope of reports covered:**
- Violations of EU law in: financial services, anti-money laundering, product safety, transport safety, food safety, environmental law, radiation, nuclear safety, public health, consumer protection, privacy and data protection, network and information security, competition law, corporate tax, and EU institutional law
- Finland: also covers serious Finnish employment law violations
- Germany: also covers serious German law violations

**Threshold check:** if `whistleblower_channel_required: true` from employment.md, mandatory. If `total_headcount` < 50 but ≥ 10: recommendation only (Directive permits member states to exempt <50; check current FI and DE rules).

### Draft policy template

```
WHISTLEBLOWER REPORTING POLICY
[Company name] — effective [DATE]
[Version: DRAFT — FOR ATTORNEY REVIEW BEFORE ROLLOUT]

1. PURPOSE
[Company] is committed to lawful and ethical conduct. This policy establishes a safe, confidential channel for employees and other persons to report concerns about violations of law or serious breaches of company policy, without fear of retaliation.

This policy implements the requirements of EU Directive 2019/1937 on the protection of persons who report breaches of Union law, [Finnish Act on the Protection of Whistleblowers 1171/2022 / German Hinweisgeberschutzgesetz (HinSchG)].

2. WHO CAN REPORT
Any person associated with [Company] may make a report under this policy, including:
- Current and former employees
- Job applicants
- Contractors, suppliers, and business partners
- Shareholders and board members

3. WHAT CAN BE REPORTED
Reports should concern suspected violations of:
- EU law in the areas of financial services, anti-money laundering, data protection, competition, consumer protection, environmental law, product safety, and public procurement
- [Finland: serious violations of Finnish employment law, financial markets regulation, or other significant regulatory requirements]
- [Germany: serious violations of German law, including employment law violations, criminal conduct, or serious regulatory breaches]
- Serious violations of company policy or internal controls, where there is a public interest concern

This policy is not designed for general HR grievances (employment disputes, salary questions, holiday entitlements) — those should be raised through normal HR channels.

4. HOW TO REPORT

**Internal reporting channel:**
[Channel method: e.g., confidential online reporting portal at [URL], encrypted email at [address], or dedicated phone line at [number]]

Reports may be made anonymously. Identifying yourself is not required, though it makes follow-up easier. The company accepts anonymous reports.

**External reporting channel:**
You may also report directly to the relevant authority without making an internal report first. In Finland: the Occupational Safety and Health Administration (aluehallintovirasto) and sector-specific authorities. In Germany: the Bundesamt für Justiz (BfJ) operates a federal external reporting channel.

5. CONFIDENTIALITY
The identity of the reporter will be kept confidential to the maximum extent possible. Information that could identify the reporter will not be disclosed except where required by law. The person handling reports will not disclose the reporter's identity without their consent.

6. HANDLING PROCESS
After a report is received:
- **Within 7 days:** Acknowledgement of receipt
- **Within 3 months:** Feedback on the action taken (or planned), including whether the matter was investigated and its outcome — subject to confidentiality obligations regarding others involved
- Reports are handled by [designated person / function, e.g., "the Legal team" or "the Independent Ethics Officer"]
- Reports may be investigated by an internal or external investigator

7. PROTECTION FROM RETALIATION
Retaliation against a reporter, facilitator of a report, or any person associated with a report is prohibited and will result in disciplinary action. Retaliation includes dismissal, demotion, salary reduction, harassment, or any other detrimental treatment connected to a report. Any person who believes they have been retaliated against should contact [HR / Legal contact] immediately.

Reports made in good faith are protected even if the reported concern turns out to be unfounded. False reports made knowingly and maliciously are not protected and may result in disciplinary action.

8. RECORD-KEEPING
[Company] maintains a confidential register of reports received. This register records the date of report, the subject matter (not the reporter's identity), the action taken, and the outcome. Records are retained for [5 years] after the close of the matter.

9. REVIEW
This policy is reviewed annually and updated as required by law or best practice.

---
[REVIEWER NOTE: Before rollout — verify that the reporting channel meets technical requirements (secure, confidential, anonymous-capable) before communicating this policy. Germany: report this policy to Betriebsrat — §87 BetrVG co-determination may apply to the implementation of the reporting system. Finland: YT-laki §16 consultation recommended before rollout for ≥20 employees. Confirm implementing act applicability threshold for current headcount. [model knowledge — verify current HinSchG applicability thresholds for employers 50–249 employees]]
```

---

## Policy type 5: Equal Treatment Policy

### Legal basis
- Finland: Tasa-arvolaki (Laki naisten ja miesten välisestä tasa-arvosta, 609/1986) — gender equality; employers ≥30 employees must have tasa-arvosuunnitelma (equality plan) updated every 2 years
- Finland: Yhdenvertaisuuslaki (1325/2014) — equal treatment across all grounds; employers ≥30 employees must have yhdenvertaisuussuunnitelma (equality and non-discrimination plan)
- Germany: AGG (Allgemeines Gleichbehandlungsgesetz) — anti-discrimination; applies to all employers regardless of size
- EU: Employment Equality Directive (2000/78/EC), Race Equality Directive (2000/43/EC)

### Protected characteristics (all EU/FI/DE)
| Ground | FI (Tasa-arvo/YV) | DE (AGG) | EU Directives |
|---|---|---|---|
| Sex / gender | yes | yes | yes |
| Pregnancy / parental status | yes | yes | yes |
| Ethnic origin / nationality | yes | yes | yes |
| Disability | yes | yes | yes |
| Age | yes | yes | yes |
| Sexual orientation | yes | yes | yes |
| Religion or belief | yes | yes | yes |
| Language | yes (Finnish specific) | — | — |

### Draft policy template

```
EQUAL TREATMENT AND NON-DISCRIMINATION POLICY
[Company name] — effective [DATE]
[Version: DRAFT — FOR ATTORNEY REVIEW BEFORE ROLLOUT]

1. COMMITMENT
[Company] is committed to equal treatment of all employees, candidates, and persons associated with the company. Discrimination, harassment, and victimisation based on any protected characteristic are prohibited.

2. SCOPE
This policy applies to all aspects of employment including: recruitment and selection, terms and conditions, pay, access to training and development, promotion, and termination. It applies to all employees, managers, contractors, and third parties acting on the company's behalf.

3. PROTECTED CHARACTERISTICS
No person will be treated less favourably because of: sex or gender; pregnancy or parental leave status; marital or family status; ethnic or national origin; race; colour; language; religion or belief; disability; age; sexual orientation; gender identity; or political opinion.

4. WHAT CONSTITUTES DISCRIMINATION

**Direct discrimination:** treating a person less favourably because of a protected characteristic.

**Indirect discrimination:** applying a practice, criterion, or provision that, while apparently neutral, puts persons with a protected characteristic at a particular disadvantage — unless the practice is objectively justified.

**Harassment:** unwanted conduct related to a protected characteristic that has the purpose or effect of violating a person's dignity or creating an intimidating, hostile, degrading, or offensive environment.

**Victimisation:** treating a person unfairly because they have raised a concern under this policy or assisted another person in doing so.

5. OBLIGATIONS OF MANAGERS
Managers are responsible for ensuring equal treatment within their teams, including in: hiring decisions, performance reviews, access to development opportunities, and disciplinary processes. Managers who become aware of potential discrimination must report it to HR promptly.

6. REASONABLE ADJUSTMENTS (DISABILITY)
[Company] will make reasonable adjustments for employees and candidates with disabilities to ensure they are not placed at a substantial disadvantage. Employees may request an adjustment at any time by contacting HR. Adjustments will be documented and reviewed regularly.

[Finland: Employers must take proportionate measures to enable a disabled person to access, perform, and advance in employment — Yhdenvertaisuuslaki §15]
[Germany: §164 SGB IX — employer with ≥20 employees is subject to the Schwerbehindertenrecht; quota obligation (5% of positions for severely disabled persons)]

7. PAY EQUITY
[Finland: required for employers ≥30 employees — tasa-arvosuunnitelma must include a pay survey (palkkakartoitus) every 3 years examining whether pay differences between men and women performing equivalent work are justified]
[Germany: Entgelttransparenzgesetz — employees in companies ≥200 have the right to request information about the pay of comparators of the opposite sex]

8. REPORTING A CONCERN
Any employee who believes they have experienced or witnessed discrimination, harassment, or victimisation should report it to [HR contact] or their manager (or, if the manager is involved, to [alternate contact or whistleblower channel]).

All reports will be treated confidentially to the extent possible and investigated promptly. Victimisation of a person who raises a concern in good faith is a disciplinary offence.

9. EQUALITY PLAN [Finland — required for ≥30 employees]
In accordance with Finnish equality legislation, [Company] maintains:
- A tasa-arvosuunnitelma (gender equality plan) updated every 2 years, including a palkkakartoitus (pay survey)
- A yhdenvertaisuussuunnitelma (non-discrimination and equality plan) updated every 2 years

These plans are developed in cooperation with employee representatives and are available to all employees. [Link to current plans or note location]

10. REVIEW
This policy is reviewed every 2 years, or sooner if required by changes in law. [Finland: equality plans updated in conjunction with this review.]

---
[REVIEWER NOTE: Finland ≥30 employees: tasa-arvosuunnitelma and yhdenvertaisuussuunnitelma are legally required — this policy template does not substitute for them. They must be prepared in cooperation with employee representatives. Germany: AGG §12 requires employers to take measures to prevent discrimination — this policy satisfies that obligation, but consider adding AGG-specific complaint procedures (Beschwerdestelle designation required under §13 AGG). Check that pay survey has been or will be conducted within required cycle.]
```

---

## Pre-rollout checklist

After drafting any policy, output this checklist:

**Before communicating this policy to employees:**

- [ ] Attorney review complete — policy reflects current law and applicable collective agreement
- [ ] Finland (≥20 employees): YT-laki §16 consultation complete — personnel rep has been given opportunity to comment and discussion has concluded
- [ ] Germany (Betriebsrat exists): applicable BetrVG co-determination process complete — Betriebsvereinbarung signed or arbitration board ruling obtained
- [ ] Monitoring policies: GDPR Art. 88 / Finnish privacy-in-working-life act requirements confirmed with DPO or privacy counsel
- [ ] Whistleblower policy: reporting channel is operational and tested before policy communicated
- [ ] Equal treatment policy: equality plan development process initiated (Finland ≥30 employees); AGG Beschwerdestelle designated (Germany)
- [ ] Policy distributed and acknowledged — record employee acknowledgment date

---

## Guardrail

> **CONFIDENTIAL — INTERNAL LEGAL ANALYSIS — DRAFT FOR ATTORNEY REVIEW.** Employment policies create legal obligations as well as rights. Policies involving employee monitoring, performance assessment, or disciplinary procedures must be reviewed by an employment lawyer and — where required — agreed with the Betriebsrat (Germany) or developed through YT-laki consultation (Finland) before they are communicated to employees. A policy rolled out without required works council consultation may be void and expose the employer to liability. These drafts are starting points, not final documents. Outputs are legal support tools — not legal advice. No attorney-client relationship or privilege is created by using this skill.