#!/usr/bin/env python3
# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Assert each cookbook's README security table matches what its YAML grants.

CLAUDE.md, cookbook rule 2:

    The README's security table and the `agent.yaml` comments must match what
    the YAML actually grants. Don't claim a tool a subagent doesn't have.

`lint-tool-scope.py` enforces rule 1 (the orchestrator stays local-only) but
only ever reads `agent.yaml`. It never opens `subagents/*.yaml` or `README.md`,
so rule 2 was unenforced — a README could advertise connectors on a component
that holds none, and nothing failed. This lint closes that gap.

Three checks per cookbook:

  1. TABLE DRIFT — every README security-table row naming a component
     (`` `<leaf>` `` or `Orchestrator`) must list exactly the tools that
     component's YAML grants. Both directions are errors: claiming a tool the
     YAML withholds (over-claim) and omitting one the YAML grants
     (under-disclosure — the more serious of the two).
  2. PHANTOM CONNECTOR — every server declared in the orchestrator's
     `mcp_servers` must be granted to at least one component via an
     `mcp_toolset`. A declared-but-ungranted server reads as a live connector
     in the README and in deploy instructions while reaching nothing.
  3. STALE COMMENT — an `agent.yaml` comment claiming the leaves hold MCP or
     `web_fetch` must be true of at least one leaf.

Exits non-zero listing every mismatch. Exits 0 with a one-line summary per
cookbook on success.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

# Repo text is UTF-8 and this script's output uses non-ASCII markers (✓, —).
# On Windows the console defaults to a legacy code page (cp1252), which makes
# print() raise UnicodeEncodeError. Re-encode the streams instead of requiring
# every caller to remember PYTHONUTF8=1.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
COOKBOOKS_DIR = ROOT / "managed-agent-cookbooks"

# README tool label -> the name used in an agent_toolset config.
LABELS = {
    "read": "read", "grep": "grep", "glob": "glob", "write": "write",
    "edit": "edit", "webfetch": "web_fetch", "web_fetch": "web_fetch",
}
# `Agent` in a README table means "can call subagents", i.e. callable_agents.
AGENT_LABEL = "agent"


def _granted(doc: dict) -> tuple[set[str], set[str], bool]:
    """Return (agent_toolset tool names, mcp server names, has_callable_agents)."""
    tools, mcp = set(), set()
    for entry in doc.get("tools") or []:
        if not isinstance(entry, dict):
            continue
        ttype = entry.get("type", "")
        if ttype == "mcp_toolset":
            if (entry.get("default_config") or {}).get("enabled", False):
                mcp.add(entry.get("mcp_server_name", "<unnamed>"))
            continue
        if not ttype.startswith("agent_toolset"):
            continue
        default = bool((entry.get("default_config") or {}).get("enabled", False))
        for cfg in entry.get("configs") or []:
            if isinstance(cfg, dict) and bool(cfg.get("enabled", default)):
                tools.add(cfg.get("name"))
    return tools, mcp, bool(doc.get("callable_agents"))


def _wired_servers(cb: Path, comp: str) -> set[str]:
    """Servers a component has an mcp_toolset for, including ones off by default."""
    path = cb / "agent.yaml" if comp == "<orchestrator>" else cb / "subagents" / f"{comp}.yaml"
    if not path.is_file():
        return set()
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {
        e.get("mcp_server_name")
        for e in (doc.get("tools") or [])
        if isinstance(e, dict) and e.get("type") == "mcp_toolset"
    }


def _table_rows(readme: str):
    """Yield (line_no, component_label, declared_tool_labels) for security rows."""
    for i, line in enumerate(readme.split("\n"), 1):
        if not line.startswith("|") or line.count("|") < 4:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        head = cells[0]
        if head.lower().startswith(("tier", "---", ":--")) or set(head) <= set("-: "):
            continue
        # Component name: a backticked leaf name, or the literal "Orchestrator".
        m = re.search(r"`([a-z][a-z0-9-]*)`", head)
        if m:
            comp = m.group(1)
        elif head.strip("* ").lower() == "orchestrator":
            comp = "<orchestrator>"
        else:
            continue
        # A combined "`leaf` / Orchestrator" row publishes a union of two tiers
        # and cannot be checked against either — flag it rather than guess.
        combined = "/" in head and "orchestrator" in head.lower()
        declared = {t.lower() for t in re.findall(r"`([A-Za-z_]+)`", cells[-2])}
        yield i, comp, declared, combined, cells[-1]


def _lint_one(cb: Path) -> list[str]:
    errs: list[str] = []
    agent_path = cb / "agent.yaml"
    if not agent_path.is_file():
        return [f"{cb.name}: missing agent.yaml"]
    agent_doc = yaml.safe_load(agent_path.read_text(encoding="utf-8")) or {}
    orch_tools, orch_mcp, orch_agents = _granted(agent_doc)

    comps: dict[str, tuple[set[str], set[str], bool]] = {"<orchestrator>": (orch_tools, orch_mcp, True)}
    for sub in sorted((cb / "subagents").glob("*.yaml")):
        comps[sub.stem] = _granted(yaml.safe_load(sub.read_text(encoding="utf-8")) or {})

    rel_agent = agent_path.relative_to(ROOT)

    # 2. Phantom connectors.
    declared_servers = {
        s.get("name") for s in (agent_doc.get("mcp_servers") or []) if isinstance(s, dict)
    }
    all_granted_mcp = set().union(*(m for _, m, _ in comps.values())) if comps else set()
    # A toolset present but disabled still counts as "wired", just off by default.
    for sub in sorted((cb / "subagents").glob("*.yaml")):
        for entry in (yaml.safe_load(sub.read_text(encoding="utf-8")) or {}).get("tools") or []:
            if isinstance(entry, dict) and entry.get("type") == "mcp_toolset":
                all_granted_mcp.add(entry.get("mcp_server_name"))
    for name in sorted(declared_servers - all_granted_mcp):
        errs.append(
            f"{rel_agent}: PHANTOM CONNECTOR '{name}' declared in mcp_servers but "
            f"granted to no component via mcp_toolset — remove it or grant it to a leaf"
        )

    # 3. Stale orchestrator comments.
    agent_src = agent_path.read_text(encoding="utf-8")
    # Join the comment block into one logical string so a claim wrapped across
    # two `#` lines still reads as one sentence, then split on sentence ends so
    # a later sentence can negate an earlier claim without tripping the match.
    comment_block = " ".join(
        l.strip().lstrip("#").strip() for l in agent_src.split("\n") if l.strip().startswith("#")
    )
    claims = [s for s in re.split(r"(?<=[.;])\s+", comment_block) if "held by" in s]
    leaf_tools = set().union(*(t for k, (t, _, _) in comps.items() if k != "<orchestrator>")) or set()
    leaf_mcp = set().union(*(m for k, (_, m, _) in comps.items() if k != "<orchestrator>")) or set()
    if any("web_fetch" in c for c in claims) and "web_fetch" not in leaf_tools:
        errs.append(
            f"{rel_agent}: STALE COMMENT claims web_fetch is held by a subagent leaf, "
            f"but no leaf grants web_fetch"
        )
    if any("MCP" in c for c in claims) and not leaf_mcp:
        errs.append(
            f"{rel_agent}: STALE COMMENT claims MCP is held by the subagent leaves, "
            f"but no leaf grants an enabled mcp_toolset"
        )

    # 1. Table drift.
    readme_path = cb / "README.md"
    if readme_path.is_file():
        rel_readme = readme_path.relative_to(ROOT)
        for line, comp, declared, combined, connectors in _table_rows(readme_path.read_text(encoding="utf-8")):
            if comp not in comps:
                continue
            # A component with no mcp_toolset at all must advertise no connector.
            # Name-by-name matching is left to review (READMEs use display names
            # like "Google Drive" for `gdrive`), but none-vs-some is checkable —
            # and it is the direction that overstates the security surface.
            wired = comps[comp][1] or _wired_servers(cb, comp)
            if not wired and not re.match(r"none\b", connectors.strip().strip("*"), re.I):
                errs.append(
                    f"{rel_readme}:{line}: CONNECTOR DRIFT '{comp}' README advertises "
                    f"connectors ({connectors!r}) but the YAML grants no mcp_toolset"
                )
            if combined:
                errs.append(
                    f"{rel_readme}:{line}: COMBINED ROW '{comp} / Orchestrator' publishes a "
                    f"union of two tiers — split into one row per component so each is checkable"
                )
                continue
            tools, _, has_agents = comps[comp]
            # Compare canonical tool names, not README labels — `WebFetch` and
            # `web_fetch` are the same grant and must not read as a mismatch.
            actual = {LABELS[k] for k in LABELS if LABELS[k] in tools}
            if has_agents:
                actual.add(AGENT_LABEL)
            declared_norm = {
                LABELS[d] if d in LABELS else d
                for d in declared
                if d in LABELS or d == AGENT_LABEL
            }
            over = declared_norm - actual
            under = actual - declared_norm
            if over:
                errs.append(
                    f"{rel_readme}:{line}: TABLE DRIFT '{comp}' README claims "
                    f"{sorted(over)} that the YAML does not grant"
                )
            if under:
                errs.append(
                    f"{rel_readme}:{line}: TABLE DRIFT '{comp}' YAML grants "
                    f"{sorted(under)} that the README does not disclose"
                )
    return errs


def main() -> int:
    if not COOKBOOKS_DIR.is_dir():
        print(f"no cookbooks dir at {COOKBOOKS_DIR}", file=sys.stderr)
        return 2
    total, clean = [], []
    for cb in sorted(d for d in COOKBOOKS_DIR.iterdir() if (d / "agent.yaml").is_file()):
        errs = _lint_one(cb)
        total.extend(errs) if errs else clean.append(cb.name)
    if total:
        print("cookbook-docs lint FAILED:", file=sys.stderr)
        for e in total:
            print(f"  {e}", file=sys.stderr)
        return 1
    for slug in clean:
        print(f"  ✓ {slug:24s} README security table matches YAML grants")
    return 0


if __name__ == "__main__":
    sys.exit(main())
