# Resource Types — EU Publications Office

Full URI base: `http://publications.europa.eu/resource/authority/resource-type/`

## Legislation

| Code | Description |
|---|---|
| `REG` | Regulation |
| `REG_IMPL` | Implementing Regulation |
| `REG_DEL` | Delegated Regulation |
| `DIR` | Directive |
| `DIR_IMPL` | Implementing Directive |
| `DIR_DEL` | Delegated Directive |
| `DEC` | Decision |
| `DEC_IMPL` | Implementing Decision |
| `DEC_DEL` | Delegated Decision |
| `RECO` | Recommendation |
| `OPIN` | Opinion |
| `REGU` | Regulation (EU) |
| `FRAMEWORK_DECISION` | Framework Decision |

## CJEU (Court of Justice of the EU)

| Code | Description |
|---|---|
| `JUDG` | Judgment |
| `ORDER_CJEU` | Order |
| `AG_OPINION` | Advocate General Opinion |
| `CASELAW` | Case law (generic) |
| `document_cjeu` | CJEU document (CDM class, use as `cdm:document_cjeu`) |
| `case-law` | Case law (CDM class) |
| `summary_case-law` | Summary of case law |

## Other

| Code | Description |
|---|---|
| `CORRIGENDUM` | Corrigendum (always exclude with FILTER NOT EXISTS) |
| `OJ_L` | Official Journal L series |
| `OJ_C` | Official Journal C series |
| `COM` | COM document (Commission proposal) |
| `JOIN` | Joint proposal |
| `SWD` | Staff Working Document |
| `SEC` | SEC document |

## Usage examples

```sparql
-- Exclude corrigenda (best practice)
FILTER NOT EXISTS {
  ?work cdm:work_has_resource-type
        <http://publications.europa.eu/resource/authority/resource-type/CORRIGENDUM>
}

-- Multiple types with FILTER
FILTER(?type IN (
  <http://publications.europa.eu/resource/authority/resource-type/REG>,
  <http://publications.europa.eu/resource/authority/resource-type/DIR>
))
```
