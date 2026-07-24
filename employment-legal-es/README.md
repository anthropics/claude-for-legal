# employment-legal-es

**Spanish employment and social security law plugin for Claude.**

> **⚠️ Draft tool — not legal advice. Consult a qualified Spanish employment lawyer before taking action.**

## Overview

`employment-legal-es` covers Spanish employment and social security law — a jurisdiction not covered by other plugins in this repo.

**Jurisdiction:** Spain (LGSS RDLeg 8/2015, ET RDLeg 2/2015, Ley 2/2025, TJUE doctrine)

### What it does

- **IPT/IPA analysis:** Permanent disability grade analysis under LGSS Art. 194-200 + Ley 2/2025
- **Contingency change:** Common→professional contingency procedure (RD 1430/2009, Art. 156.2.f LGSS)
- **Sick leave timeline:** IT milestones (day 365/545/730) with dates and required actions
- **Occupational pensions + IPT:** Capital scenarios, carencia analysis, collective agreement overrides
- **Revolving credit usury:** STS 149/2020 (Wizink) test, SAC complaint letter draft
- **Cold-start setup:** Role, situation, phase → configurable profile

## Skills

| Skill | Purpose |
|---|---|
| `cold-start-interview` | Initial setup: role (worker/attorney/advisor), situation, company, phase |
| `ipt-analysis` | Permanent disability grade (IPT/IPA) analysis with LGSS art. + Ley 2/2025 |
| `contingencia-cambio` | Common→professional contingency via RD 1430/2009 + economic impact |
| `it-seguimiento` | Sick leave timeline: day 365 (extension), 545 (payer change), 730 (termination) |
| `plan-pensiones-ipt` | Occupational pension capital + IPT scenarios (carencia, collective agreement) |
| `revolving-reclamacion` | Revolving usury claim: STS 149/2020 test, SAC letter, escalation path |

## Installation

```bash
claude plugin install employment-legal-es
```

Or import directly:
```bash
claude plugin install git+https://github.com/anthropics/claude-for-legal.git/employment-legal-es
```

## Usage

Each skill is conversational — answer setup questions, provide documents/dates, get structured analysis.

### Example: IPT analysis

```
User: /employment-legal-es:ipt-analysis
Claude: What are your diagnoses (CIE-10)? Your habitual profession? Any prior ICAM ruling?
User: [Provides details]
Claude: [Table: probable IPT grade | legal basis | case strengths/weaknesses | next steps]
```

### Example: Sick leave timeline

```
User: /employment-legal-es:it-seguimiento
Claude: Sick leave start date?
User: 2025-03-10
Claude: [Timeline: day 365 = 2026-03-10 (extension due), day 545 = 2026-08-07 (payer change), ...]
```

## Disclaimer

**All outputs are draft work product — not legal advice.**

Every output includes the mandatory header:
```
BORRADOR DE TRABAJO — NO CONSTITUYE ASESORAMIENTO JURÍDICO — 
REVISAR CON ABOGADO LABORALISTA COLEGIADO EN ESPAÑA ANTES DE ACTUAR
```

- Consult a **qualified Spanish employment lawyer** before sending any letter, filing any claim, or taking consequential action
- Calculations are **estimates** — verify with relevant authorities (INSS, ICAM, VidaCaixa, Banco de España)
- Never send SAC letters, official complaints, or procedural documents without attorney review
- Jurisdictional scope: **Spain only** — art. 156.2.f LGSS, TJUE doctrine, CENDOJ jurisprudencia

## Sources

| Source | Type | Authority |
|---|---|---|
| CENDOJ | Jurisprudencia | Poder Judicial https://www.poderjudicial.es/cgpj/es/Poder-Judicial |
| BOE | Normativa | Ministerio de Justicia https://www.boe.es/ |
| INSS | Prestaciones, plazos | Seguridad Social https://www.seg-social.gob.es/ |
| Banco de España | TAE/CER estadísticas | Banco Central https://www.bde.es/ |
| ICAM | Dictamenes, procedimientos | Seguridad Social https://www.seg-social.gob.es/ |

## Key References

- **STS 149/2020** — Revolving usury (Wizink precedent)
- **Ley 2/2025** — IPT contract termination + reasonable adjustments
- **RD 1430/2009** — Contingency determination procedure
- **Art. 156.2.f LGSS** — Disease aggravated by work
- **Art. 25 LPRL** — Employer duty to adapt workplace

## License

Apache 2.0 (matching anthropics/claude-for-legal)

## Contributing

Contributions welcome. All code must follow the parent repo guidelines and include proper CENDOJ/BOE source attribution.

---

**Author:** Community contribution  
**Updated:** 2025-05-14  
**Status:** Early release (v0.1.0)
