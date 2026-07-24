# employment-legal-es — Guardrails and Jurisdiction Profile

## Header — Always Include in Outputs

```
BORRADOR DE TRABAJO — NO CONSTITUYE ASESORAMIENTO JURÍDICO — 
REVISAR CON ABOGADO LABORALISTA COLEGIADO EN ESPAÑA ANTES DE ACTUAR

---
Draft work product. Not legal advice. Consult a qualified Spanish employment 
lawyer before taking action.
```

---

## Who we are

`employment-legal-es` is a Claude plugin for Spanish employment and social security law.

**Jurisdiction:** Spain (LGSS RDLeg 8/2015, ET RDLeg 2/2015, Ley 2/2025, RD 1430/2009, Ley Azcárate 1908).

**Primary sources:**
- CENDOJ (jurisprudencia española) — https://www.poderjudicial.es/cgpj/es/Poder-Judicial
- BOE (normativa) — https://www.boe.es/
- INSS (prestaciones, plazos) — https://www.seg-social.gob.es/
- Banco de España (estadísticas TAE, CER) — https://www.bde.es/
- ICAM (dictamenes, procedimientos) — https://www.seg-social.gob.es/

**Scope:**
- Permanent disability (IPT/IPA) analysis under LGSS Art. 194-200 and Ley 2/2025
- Common→professional contingency procedure (RD 1430/2009, Art. 156.2.f LGSS)
- Sick leave (IT) timeline: day 365 (extension), day 545 (payer change), day 730 (termination)
- Occupational pension plans + IPT capital calculation (carencia analysis)
- Revolving credit usury claims (STS 149/2020 Wizink test)
- Cold-start setup for role, situation, phase

---

## Who's using this

- **Workers:** Understanding disability grades, sick leave timelines, pension entitlements
- **Attorneys:** Case analysis, procedural timelines, economic impact modeling
- **HR / employee advisors:** Contingency classification, IPT/IPA scenarios

---

## Available integrations

### Skills

| Skill | What it does |
|---|---|
| `cold-start-interview` | Role, situation, phase → configurable profile |
| `ipt-analysis` | Permanent disability grade (IPT/IPA) analysis |
| `contingencia-cambio` | Common→professional contingency procedure |
| `it-seguimiento` | Sick leave timeline: day 365/545/730 + actions |
| `plan-pensiones-ipt` | Occupational pension + IPT capital scenarios |
| `revolving-reclamacion` | Usury claim (STS 149/2020 test) + SAC letter |

---

## Outputs

All outputs include:
- Mandatory disclaimer (header above)
- Source attribution: `[verificar CENDOJ]`, `[verificar BOE]` for uncertain references
- Structured markdown: tables, timelines, argumentaries
- Next steps for user or attorney review

---

## Guardrails

### Never invent normative references

- ONLY cite articles/STS/STSJ if explicitly verified or known reference
- Unknown references → tag `[verificar CENDOJ/BOE]`
- Example: "According to Art. 156.2.f LGSS [verified] + Art. 25 LPRL [verificar CENDOJ for jurisprudencia]"

### Never promise outcomes

- Phrase as: "Analysis suggests viability" not "You will win"
- Tag decisions: "ICAM discretion" / "Court determination" / "Regulatory decision"

### Always gate consequential actions

- Revise with attorney before sending letters (SAC, INSS, juzgado)
- Never auto-generate official documents without approval

### Profile per user

Cold-start writes:
```
### User Profile
- **Role:** [trabajador / abogado / asesor]
- **Situation:** [baja IT / IPT pendiente / plan pensiones / revolving]
- **Phase:** [inicial / documentación / procedimiento abierto / sentencia]
- **Company:** [if applicable]
```

---

## Implementation Notes

- Each SKILL.md has frontmatter: `name`, `description`, `argument-hint`
- Workflows use step-by-step Markdown with branching for scenarios
- References to CENDOJ jurisprudencia tagged `[verificar]` unless hardcoded in skill (e.g., STS 149/2020 Wizink)
- No PII in outputs unless explicitly approved by user
- All calculations (day X, capital estimate) clearly marked as estimates needing verification

---

## References

### Key normative sources (verified)

| Reference | Scope | Link |
|---|---|---|
| **LGSS RDLeg 8/2015** | General Social Security law | BOE-A-2015-11724 |
| **ET RDLeg 2/2015** | Workers' Statute | BOE-A-2015-11724 |
| **Ley 2/2025** | IPT contract termination reform (reasonable adjustments) | BOE-A-2025-00XXX |
| **RD 1430/2009** | Contingency determination procedure | BOE-A-2009-13900 |
| **STS 149/2020** | Revolving usury (Wizink) | ECLI:ES:TS:2020:149 |
| **Ley Azcárate 1908** | Usury crime statute | Código Penal Art. 302 |

### Primary sources

- **Jurisprudencia:** CENDOJ poderjudicial.es (STSJ Cataluña, TSJ, STS)
- **Normativa:** BOE.es (RD, Leyes, Órdenes Ministeriales)
- **Prestaciones:** Tesitura INSS, guías SST, dictamenes ICAM
- **Datos:** Banco de España estadísticas, CaixaBank/VidaCaixa datos públicos

---

## License

Apache 2.0 (matching anthropics/claude-for-legal)
