# Contributing to billing-legal

Thanks for your interest in contributing. This plugin is part of the [claude-for-legal](https://github.com/anthropics/claude-for-legal) ecosystem and follows its architecture conventions.

## Architecture conventions

Skills are instruction files (`SKILL.md`), not executable code. They tell Claude what to read, what to ask, and what to write — all within the file-based config system at `~/.claude/plugins/config/claude-for-legal/billing/`.

- **Skills** (`skills/<name>/SKILL.md`) — user-invocable commands. Follow the frontmatter format (`name`, `description`, `argument-hint`, optionally `disable-model-invocation: true` for skills that write financial records).
- **Agents** (`agents/<name>.md`) — scheduled or triggered automation. Follow the frontmatter format (`name`, `description`, `model`, `tools`).
- **Hooks** (`hooks/`) — shell scripts (`*.ps1`) and the `hooks.json` manifest. Scripts must be idempotent and exit 0 in all cases. Stop hooks that block must output valid JSON to stdout.
- **`.claude-plugin/config-template.md`** — the user config template. Kept out of root to pass strict plugin validation. cold-start-interview uses it as the structural reference when writing `~/.claude/plugins/config/claude-for-legal/billing/CLAUDE.md`. Developer notes only in the HTML comment block; runtime behavior lives in SKILL.md files.

## Data format

The `time-register.yaml` and `invoice-register.yaml` files are top-level YAML lists (no wrapper key). Each entry starts with `- id:` at column 0. Skills that append to these files must follow this format exactly to avoid corrupting the register.

## Pull request checklist

- [ ] Skill frontmatter includes `name`, `description`, and `argument-hint`
- [ ] Skills that write financial records include `disable-model-invocation: true`
- [ ] YAML append instructions use top-level list format (`- id:` at column 0)
- [ ] Hook scripts exit 0 in all cases; Stop hooks that block output `{"decision":"block","reason":"..."}` to stdout
- [ ] No hardcoded paths — use `billing_data_path` from config, resolved at runtime
- [ ] README updated if a new skill or workflow is added
- [ ] No real billing data (YAML registers, invoice files) committed to the repo — `.gitignore` covers these but double-check

## Reporting issues

Open a GitHub issue with:
1. What you expected to happen
2. What actually happened (paste any error output)
3. Which skill or hook was running
4. Whether you're using a shared folder or local config
