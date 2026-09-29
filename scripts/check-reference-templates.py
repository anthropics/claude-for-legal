#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Ensure every shipped plugin carries the shared reference templates.

Every plugin references two shared templates "in the plugin root":

  - references/dashboard-template.md        (each plugin's CLAUDE.md)
  - references/company-profile-template.md  (each cold-start-interview SKILL.md)

Those files live only at the repo root, but the marketplace installs each
plugin from its own subdirectory. This script asserts every core plugin ships
both templates, byte-identical to the repo-root canonical copies. Exits non-zero
on any mismatch; prints a one-line summary per plugin on success.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
TEMPLATES = ("dashboard-template.md", "company-profile-template.md")


def _core_plugins() -> list[Path]:
    """Core plugin dirs from marketplace.json (skips external_plugins/)."""
    doc = json.loads(MARKETPLACE.read_text())
    plugins: list[Path] = []
    for plugin in doc.get("plugins", []):
        source = plugin.get("source", "")
        if source.startswith("./external_plugins/") or not source.startswith("./"):
            continue
        plugins.append(ROOT / source[2:])
    return plugins


def main() -> int:
    canonical = {name: (ROOT / "references" / name).read_bytes() for name in TEMPLATES}
    errors: list[str] = []
    clean: list[str] = []
    for plugin_dir in sorted(_core_plugins()):
        plugin_errors = []
        for name, expected in canonical.items():
            actual = plugin_dir / "references" / name
            if not actual.is_file():
                plugin_errors.append(f"missing references/{name}")
            elif actual.read_bytes() != expected:
                plugin_errors.append(f"references/{name} differs from repo-root canonical")
        if plugin_errors:
            for e in plugin_errors:
                errors.append(f"{plugin_dir.name}: {e}")
        else:
            clean.append(plugin_dir.name)
    if errors:
        print("reference-template sync FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    for slug in clean:
        print(f"  ✓ {slug:24s} reference templates in sync")
    return 0

if __name__ == "__main__":
    sys.exit(main())
