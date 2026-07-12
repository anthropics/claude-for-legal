<!--
DEVELOPER NOTE — user config template. Kept in .claude-plugin/ (not root) to pass
strict plugin validation, which errors on root CLAUDE.md files that are not loaded
as plugin context.

The user's active config lives at:
  ~/.claude/plugins/config/claude-for-legal/billing/CLAUDE.md

cold-start-interview writes that file from scratch using interview answers, using
this template as the structural reference for section names and placeholder markers.
User data must never be written here.

Runtime behavior (placeholder checks, config-path reads, data-path resolution) is
defined in each skill's SKILL.md. Skills explicitly read from the config path and
do not rely on this file being auto-loaded.
-->

# Billing Practice Profile

*This file is written by the cold-start interview on first run. Until then, it's
a template. If you're seeing `[PLACEHOLDER]` values below, run `/billing-legal:cold-start-interview`.*

*Once populated: edit this file directly. Every skill reads it before doing anything.*

---

## Firm billing info

**Firm name:** [PLACEHOLDER]
**Billing address:** [PLACEHOLDER]
**Billing email:** [PLACEHOLDER]
**Remittance instructions:** [PLACEHOLDER — e.g., "Net 30. Payment by check or ACH. See invoice for details."]

*(Firm name syncs from `company-profile.md`. Edit there to update across all plugins.)*

---

## Billing data

**Data path:** [PLACEHOLDER — `~/.claude/plugins/config/claude-for-legal/billing/` for solo; shared OneDrive/network path for firms]

**Active attorney:** [PLACEHOLDER — slug of the attorney using this machine, e.g. `alice-jones`]

*Every skill reads and writes to the data path. `Active attorney` is a per-machine setting: in a firm using a shared data path, each attorney's machine has their own slug here. The session timer hook uses it to key timer files by attorney so multiple attorneys sharing the same folder do not interfere with each other's timers.*

---

## Attorneys

*One entry per attorney who uses this plugin. Slug is lowercase-hyphenated. Add or update via `/billing-legal:rate-card` or directly here.*

```yaml
# attorneys/[slug].yaml — created by cold-start-interview for each attorney
# Example:
#   slug: alice-jones
#   name: Alice Jones
#   email: alice@firm.com
#   default_rate: 350
#   billing_increment: 0.1   # 0.1 = 6-minute minimum; 0.2 = 12-minute
#   rate_overrides:
#     acme-corp: 325
#     beta-llp: 400
```

[PLACEHOLDER — attorney profiles added at cold-start]

---

## Invoice settings

**Invoice prefix:** [PLACEHOLDER — e.g., INV or BILL]
**Next invoice number:** [PLACEHOLDER — e.g., 001]
**Task codes:** [PLACEHOLDER — required | optional | hidden]
**Date format on invoices:** YYYY-MM-DD

---

## Panel settings

**Billing panel at end of session:** [PLACEHOLDER — enabled | disabled]
**Auto-detect active matter:** [PLACEHOLDER — enabled | disabled]
**Budget warning threshold:** [PLACEHOLDER — 75 (percent)]

---

## LEDES export

**LEDES export:** [PLACEHOLDER — enabled | disabled]
**Default timekeeper classification:** [PLACEHOLDER — AT | PA | OF | CL]

*(LEDES 1998B is the standard format required by most corporate legal departments and insurance companies for e-billing submission. Run `/billing-legal:ledes-export --invoice <id>` after generating an invoice exhibit. Set per-attorney timekeeper IDs and per-client LEDES client IDs via `/billing-legal:rate-card`.)*

---

## Activity logging

**Activity logging:** [PLACEHOLDER — enabled | disabled]
**Activity log on invoice:** [PLACEHOLDER — enabled | disabled]

*(When enabled, a PostToolUse hook silently records which documents were opened or edited during each session. The log appears in the billing panel at session end to help write accurate narratives, and is stored in the time register entry. If "Activity log on invoice" is enabled, a collapsed audit trail section is included in invoice exhibits.)*

---

## Notes

[PLACEHOLDER — any firm-specific billing rules, e.g., "minimum 0.2h per task for litigation matters" or "all invoices require partner approval before sending"]
