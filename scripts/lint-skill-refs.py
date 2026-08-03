#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Assert every slash-command reference in plugin prose resolves to a real skill.

CLAUDE.md, "Skill names in prose must be canonical":

    When a SKILL.md (especially `customize` or `cold-start-interview`) tells the
    user "run `/foo`," `foo` must be the actual `skills/<foo>/` directory name.
    Short forms like `/triage` for `/use-case-triage` look right in prose but are
    dead commands — the user types them and nothing happens.

`claude plugin validate` does not check this: a `/foo` in prose is just text, so
a short form or a mangled find-and-replace ships silently and the user gets
nothing when they type it. This lint closes that gap.

Two defect classes are reported:

  1. DEAD REF — `/foo` (or `/<plugin>:<foo>`) names no skill directory. Refs to
     Claude Code built-ins (`/mcp`, `/plugin`, ...) are exempt.
  2. WRAPPED REF — the name resolves, but the source splits it across a line
     inside the backticks, so it renders with a space (`/handbook- updates`)
     and is not typable as written.

Scanned: each plugin's CLAUDE.md, README.md, skills/*/SKILL.md, agents/*.md.
Exits non-zero listing every offending file:line on any violation.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Claude Code built-in slash commands — legitimate refs, not plugin skills.
BUILTINS = {
    "add-dir", "agents", "bug", "clear", "compact", "config", "context", "cost",
    "doctor", "exit", "export", "feedback", "help", "hooks", "ide", "init",
    "install-github-app", "login", "logout", "loop", "mcp", "memory", "model",
    "output-style", "permissions", "plugin", "pr-comments", "privacy-settings",
    "quit", "release-notes", "resume", "review", "rewind", "sandbox", "settings",
    "skills", "statusline", "status", "terminal-setup", "todos", "upgrade",
    "usage", "vim", "workflows", "worktree",
}

# A backtick-delimited token starting with `/`. DOTALL so we can detect a name
# broken across a source line inside the backticks.
BACKTICKED = re.compile(r"`(/[^`]{1,120}?)`", re.S)
# A bare `/foo` in prose, when preceded by whitespace or an opening delimiter.
# Excludes path-like refs (`foo/bar`, `/foo/bar`), numeric folder prefixes, and
# the plugin half of a qualified `/plugin:skill` ref (handled by BACKTICKED).
BARE = re.compile(
    r"(?:(?<=\s)|(?<=\()|(?<=\[)|(?<=^))/([a-z][a-z0-9-]{1,63})(?![a-z0-9:/-])", re.M
)
NAME_OK = re.compile(r"^[a-z0-9][a-z0-9:-]*$")


def _plugin_dirs() -> list[Path]:
    dirs = [
        d for d in sorted(ROOT.iterdir())
        if d.is_dir() and (d / ".claude-plugin" / "plugin.json").is_file()
    ]
    ext = ROOT / "external_plugins"
    if ext.is_dir():
        dirs += [
            d for d in sorted(ext.iterdir())
            if d.is_dir() and (d / ".claude-plugin" / "plugin.json").is_file()
        ]
    return dirs


def _skills(plugin: Path) -> set[str]:
    skills_dir = plugin / "skills"
    if not skills_dir.is_dir():
        return set()
    return {d.name for d in skills_dir.iterdir() if d.is_dir()}


def _scan_files(plugin: Path):
    for rel in ("CLAUDE.md", "README.md"):
        p = plugin / rel
        if p.is_file():
            yield p
    yield from sorted(plugin.glob("skills/*/SKILL.md"))
    yield from sorted(plugin.glob("agents/*.md"))


def main() -> int:
    plugins = _plugin_dirs()
    if not plugins:
        print(f"no plugins found under {ROOT}", file=sys.stderr)
        return 2
    skills = {p.name: _skills(p) for p in plugins}
    errs: list[str] = []

    for plugin in plugins:
        own = skills[plugin.name]
        for path in _scan_files(plugin):
            src = path.read_text(encoding="utf-8")
            rel = path.relative_to(ROOT)

            # Collect (name, line, wrapped) candidates from both syntaxes.
            found: list[tuple[str, int, bool]] = []
            for m in BACKTICKED.finditer(src):
                raw = m.group(1)
                wrapped = "\n" in raw
                joined = re.sub(r"\n\s*", "", raw) if wrapped else raw
                parts = joined[1:].split()
                if not parts:
                    continue
                # First token is the command; the rest are arguments (--redo, ...).
                found.append((parts[0].rstrip(".,;:)!?"), src[: m.start()].count("\n") + 1, wrapped))
            for m in BARE.finditer(src):
                # Skip path-like refs: `/foo/bar` or `dir/foo`.
                if m.end() < len(src) and src[m.end()] == "/":
                    continue
                found.append((m.group(1), src[: m.start()].count("\n") + 1, False))

            for name, line, wrapped in found:
                if not NAME_OK.match(name):
                    continue
                if ":" in name:
                    target, _, skill = name.partition(":")
                    if target not in skills or not skill:
                        continue  # not one of ours — leave it alone
                    pool, label = skills[target], f"/{name}"
                else:
                    if name in BUILTINS:
                        continue
                    target, skill = plugin.name, name
                    pool, label = own, f"/{name}"
                if skill not in pool:
                    near = sorted(s for s in pool if s.startswith(skill) or skill in s)
                    hint = f" — did you mean {'/' + near[0]}?" if near else ""
                    errs.append(f"{rel}:{line}: DEAD REF {label} — no skills/{skill}/ in {target}{hint}")
                elif wrapped:
                    errs.append(
                        f"{rel}:{line}: WRAPPED REF {label} — name is split across a "
                        f"source line inside backticks; it renders with a space"
                    )

    if errs:
        print("skill-ref lint FAILED:", file=sys.stderr)
        for e in dict.fromkeys(errs):
            print(f"  {e}", file=sys.stderr)
        return 1
    total = sum(len(v) for v in skills.values())
    print(f"  ✓ slash-command refs resolve across {len(plugins)} plugins / {total} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
