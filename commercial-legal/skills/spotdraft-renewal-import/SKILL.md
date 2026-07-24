---
name: spotdraft-renewal-import
description: >
  Bulk-import active contracts from SpotDraft into the renewal register at
  ~/.claude/plugins/config/claude-for-legal/commercial-legal/renewal-register.yaml.
  Use for a one-time CLM scan or when renewal-tracker Mode 3 needs SpotDraft as
  the source. Requires explicit confirmation before writing.
argument-hint: "[--dry-run to preview without writing]"
---

# /spotdraft-renewal-import

Fills the renewal register from SpotDraft active contracts — addresses contracts signed before the plugin was installed.

## Instructions

1. **Confirm SpotDraft is connected** via a successful MCP read (same bounce as `spotdraft-contract-lookup` if not).

2. **Call `get_contract_list`** with status filter for active/executed contracts. Paginate until all results are retrieved.

3. **For each contract**, call `get_contract_key_pointers` (renewal dates, notice periods, term) and `get_contract_status` to confirm lifecycle before import.

4. **Build a preview table** — do not write until the user confirms:

   > Found [N] contracts. Ready to import [M] with renewal dates. [P] have no renewal date and will be skipped.

5. **`--dry-run`:** Show the preview and proposed register entries only; do not write.

6. **On confirmation** (user must explicitly approve — not implied), merge into `~/.claude/plugins/config/claude-for-legal/commercial-legal/renewal-register.yaml`:
   - De-duplicate on `clm_id` (SpotDraft contract ID)
   - Update existing entries; append new ones
   - Never delete — mark missing-from-import as `status: check-spotdraft` only when reconciling in a future run (do not delete on import)
   - Append comment: `# Last imported from SpotDraft: [YYYY-MM-DD]`
   - Only write fields derivable from the API; use renewal-tracker register schema fields where possible

7. **Business-day fields:** If renewal dates need cancel-by computation, follow `renewal-tracker` conventions (`cancel_by_calendar`, `cancel_by_effective`, `cancel_by_provenance: "[model calculation — verify against the notice clause]"`).

## Examples

```
/commercial-legal:spotdraft-renewal-import
```

```
/commercial-legal:spotdraft-renewal-import --dry-run
```

---

## Purpose

Bulk-import active contracts from SpotDraft into the renewal register without manual entry. Complements `renewal-tracker` Mode 3 ([CLM] scan) when SpotDraft is the CLM.

## Auth

OAuth — only contracts the authorized user can view in SpotDraft are imported.

## MCP tools (read-only)

| Tool | What it fetches |
|---|---|
| `get_contract_list` | Active contracts (status: Executed / Active) |
| `get_contract_key_pointers` | Renewal dates, notice periods, term start/end |
| `get_contract_status` | Confirm lifecycle status before register write |

## Register target

`~/.claude/plugins/config/claude-for-legal/commercial-legal/renewal-register.yaml` (config directory — survives plugin updates). See `renewal-tracker` for the full entry schema.

## Gate

**Requires explicit user confirmation before writing.** Dry-run mode: `--dry-run` previews without writing.

## De-duplication

Match on `clm_id` (SpotDraft contract ID). Existing entries updated; new entries appended. No entry deleted on import.
