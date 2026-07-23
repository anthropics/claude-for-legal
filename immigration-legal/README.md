# immigration-legal

Employment-based immigration practice toolkit for partner attorneys. Follows the claude-for-legal plugin conventions: same `CLAUDE.md` practice-profile pattern, same cold-start-interview flow, same skill structure as `commercial-legal`, `employment-legal`, and `privacy-legal`.

---

## What this plugin does

Merit evaluation, evidence mapping, and petition scaffolding for EB-1A, EB-2 NIW, and O-1 petitions — with architecture in place for EB-1B, EB-2 PERM, H-1B, and L-1 in future builds.

The plugin is **attorney-facing**. It runs in the attorney's Claude Desktop while the client's data and portfolio lives in Meritocrat (app.meritocrat.us). The same skill logic is designed to deploy via the Managed Agents API behind Meritocrat's applicant-facing flow — same SKILL.md, same evaluation logic, different runtime.

---

## Install

### Claude Desktop (Cowork mode)

1. Copy the `immigration-legal/` folder into your Claude plugins directory.
2. In Claude Desktop: Settings → Plugins → Install from folder → select `immigration-legal/`.
3. Run `/immigration-legal:cold-start-interview` to set up your practice profile.

### Claude Code

1. Add the plugin path to your `.mcp.json` or Claude Code config.
2. Run `/immigration-legal:cold-start-interview` in a new session.

---

## First use

Run the cold-start interview once. It will:
- Ask about your firm, visa mix, and risk posture
- Ask for a sample petition letter and (optionally) an RFE response
- Write your practice profile to `~/.claude/plugins/config/claude-for-legal/immigration-legal/CLAUDE.md`

After that, every skill reads from your practice profile automatically. You do not need to re-explain your firm's standards on every run.

---

## Skills

### Phase 1 — Spine (fully implemented)

| Skill | Command | What it does |
|---|---|---|
| Cold-start interview | `/immigration-legal:cold-start-interview` | One-time setup — writes your practice profile |
| Merit evaluation | `/immigration-legal:merit-evaluation` | Criterion-by-criterion GREEN/YELLOW/RED for EB-1A, EB-2 NIW, O-1A, or O-1B |
| Evidence organizer | `/immigration-legal:evidence-organizer` | Maps exhibits to criteria, flags coverage gaps |

### Phase 2 — Strategy and drafting (stubs — manual fallback available)

| Skill | Command | What it does |
|---|---|---|
| Intake | `/immigration-legal:intake` | Structured new-client intake + cross-visa triage |
| Strategy memo | `/immigration-legal:strategy-memo` | Which visa, which criteria to lead, evidence development plan |
| Petition letter draft | `/immigration-legal:petition-letter-draft` | IRAC scaffold per criterion — rule, evidence inventory, attorney-analysis prompts |

### Phase 3 — Post-filing (stubs — manual fallback available)

| Skill | Command | What it does |
|---|---|---|
| RFE response | `/immigration-legal:rfe-response` | Analyzes RFE, maps to evidence gaps, scaffolds response |
| Client update | `/immigration-legal:client-update` | Routine client correspondence in plain language |

### Phase 4 — Operational (fully implemented)

| Skill | Command | What it does |
|---|---|---|
| Matter workspace | `/immigration-legal:matter-workspace` | Multi-client file management (new / list / switch / close) |
| Customize | `/immigration-legal:customize` | Edit one section of the practice profile without re-running setup |

**Note on Phase 2–3 stubs:** These skills load cleanly and describe exactly what they will do. Until fully implemented, each stub includes a manual fallback: describe what you need in the chat and the Phase 1 skills (or Claude directly) will handle it. The stubs are replaced in place when the next build cycle completes — no reinstall required.

---

## How this relates to Meritocrat

**Runtime separation, shared logic.**

The `immigration-legal` plugin runs in your Claude Desktop. Meritocrat (app.meritocrat.us) runs on the Anthropic Managed Agents API. They share skill definitions but not runtime:

- **Desktop (attorney):** You run `/immigration-legal:merit-evaluation` on a client. The evaluation reads your firm's practice profile (posture, evidence thresholds) and the client data you describe or paste. Output goes to your conversation and (if using matter workspaces) to the client matter folder on your machine.

- **Meritocrat (applicant):** The same merit-evaluation logic runs server-side against the applicant's portfolio stored in Meritocrat. The output surfaces in the Meritocrat UI for the applicant.

**What stays different:**
- The `CLAUDE.md` practice profile is firm-specific in Desktop; it becomes tenant-specific configuration in the Meritocrat backend.
- Meritocrat holds the applicant's portfolio (publications list, citation counts, award certificates, press links). The Desktop plugin works from whatever you paste or point it at.
- The attorney-facing Desktop skills are designed for the attorney's workflow — reviewing, deciding, drafting. The applicant-facing Meritocrat skills are designed for the applicant's workflow — submitting evidence, tracking progress.

**Interpretability guarantee:** Every criterion conclusion in `merit-evaluation` must cite specific evidence and state the reasoning. This constraint is enforced by the SKILL.md prompt design itself, not a separate feature. The same constraint applies in both runtimes.

---

## Practice profile

Your practice profile lives at:
```
~/.claude/plugins/config/claude-for-legal/immigration-legal/CLAUDE.md
```

It's a plain text file. You can:
- Edit it directly (any text editor)
- Run `/immigration-legal:customize` to change one section guided
- Run `/immigration-legal:cold-start-interview --redo` for a full re-interview

The profile stores: firm name, USCIS service centers, visa mix, risk posture per visa type, evidence thresholds, comparable-evidence posture, house style, and escalation rules.

---

## Regulatory reference files

The `skills/merit-evaluation/` directory contains regulatory reference files maintained alongside the skill:

| File | Covers |
|---|---|
| `eb1a-criteria.md` | 8 CFR 204.5(h)(3) — all 10 EB-1A criteria with interpretive guidance |
| `eb2niw-prongs.md` | Matter of Dhanasar, 26 I&N Dec. 884 (AAO 2016) — all 3 NIW prongs |
| `o1-criteria.md` | 8 CFR 214.2(o)(3) — O-1A (8 criteria) and O-1B (arts/MPTV) |

These files are citation anchors for the merit-evaluation skill. They are not legal advice — attorneys must independently verify current USCIS guidance before filing.

---

## Visa types in scope

| Visa | Status |
|---|---|
| EB-1A | Active — full skill set |
| EB-2 NIW | Active — full skill set |
| O-1A | Active — full skill set |
| O-1B | Active — merit-evaluation supported |
| EB-1B | Planned — reference criteria loaded, stubs present |
| EB-2 PERM | Planned — labor certification track; out of scope for merit-evaluation |
| H-1B | Planned — specialty occupation; out of scope for merit-evaluation |
| L-1 | Planned — intracompany transferee; out of scope for merit-evaluation |

---

## Conventions

This plugin follows the `claude-for-legal` conventions exactly:
- Practice profile at `~/.claude/plugins/config/claude-for-legal/immigration-legal/CLAUDE.md`
- Matter workspaces at `~/.claude/plugins/config/claude-for-legal/immigration-legal/matters/`
- Shared company profile at `~/.claude/plugins/config/claude-for-legal/company-profile.md` (read if present; skip firm questions if so)
- Cold-start interview writes the profile; `customize` edits one section; `--redo` re-interviews
- Every skill reads the practice profile before doing anything

---

*Plugin version: 1.0.0. Regulatory references current as of 2025. Attorneys must independently verify USCIS guidance before filing.*
