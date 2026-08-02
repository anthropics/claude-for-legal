# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""`lint-tool-scope.py` — orchestrator tool-scope enforcement.

The script encodes one rule from CLAUDE.md: an orchestrator gets local-only
tools, while MCP clients, Write, and Slack live on the subagent leaves. It is
the only executable check on that boundary — the rest is prose in READMEs and
`agent.yaml` comments — so what it fails to flag, nothing flags.

Three violation classes are named in its docstring: `mcp_toolset` on the
orchestrator, an enabled `write`, and any `slack*` tool. A fourth is enforced
but not listed there — `default_config.enabled: true`, which grants the whole
toolset implicitly. All four are covered here, along with the cases the script
deliberately passes over, because a linter that flags too much gets disabled
and a linter that flags too little reads as a green check.

Every fixture cookbook is `clean_orchestrator_tools()` with one thing changed,
so a reported violation can be attributed to that change. The exception is the
first section, which runs the linter over the repo's own five cookbooks: that
is the assertion CLAUDE.md's pre-PR checklist actually depends on, and it
cannot be made against synthetic data.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from conftest import clean_orchestrator_tools

REPO_ROOT = Path(__file__).resolve().parents[1]
SHIPPED_COOKBOOKS = sorted((REPO_ROOT / "managed-agent-cookbooks").glob("*/agent.yaml"))


def _with_config(config: dict) -> list[dict]:
    """The compliant orchestrator block plus one extra tool config."""
    tools = clean_orchestrator_tools()
    tools[0]["configs"].append(config)
    return tools


def _write_raw(cookbooks_dir: Path, slug: str, text: str) -> Path:
    """Write `agent.yaml` bytes directly, for documents YAML round-tripping cannot express."""
    directory = cookbooks_dir / slug
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "agent.yaml"
    path.write_text(text, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# The repo's own cookbooks
# ---------------------------------------------------------------------------


def test_the_shipped_cookbooks_pass_their_own_linter(lint_script):
    """The check CLAUDE.md tells contributors to run before opening a PR.

    Synthetic fixtures prove the linter detects what it looks for; only this
    proves the tree it ships alongside is actually clean.
    """
    offending = {
        path.parent.name: errors
        for path in SHIPPED_COOKBOOKS
        if (errors := lint_script._lint_one(path))
    }

    assert offending == {}
    # Canary: a moved or renamed tree would otherwise assert nothing at all.
    assert len(SHIPPED_COOKBOOKS) >= 5


def test_the_documented_cli_invocation_exits_zero(lint_script):
    """`python3 scripts/lint-tool-scope.py`, exactly as CLAUDE.md spells it.

    `lint_script` is requested so this cannot run before the module imports
    cleanly; the subprocess itself gets the real, unpatched `COOKBOOKS_DIR`.
    """
    completed = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "lint-tool-scope.py")],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.count("✓") == len(SHIPPED_COOKBOOKS)


# ---------------------------------------------------------------------------
# The four violation classes
# ---------------------------------------------------------------------------


def test_an_mcp_toolset_on_the_orchestrator_is_reported(lint_script, cookbook):
    """The message has to name the file and the server, per the script's docstring."""
    path = cookbook("leaky", tools=[{"type": "mcp_toolset", "mcp_server_name": "box"}])

    errors = lint_script._lint_one(path)

    assert len(errors) == 1
    assert str(path) in errors[0]
    assert "box" in errors[0]
    assert "subagent leaf" in errors[0]


def test_an_unnamed_mcp_toolset_is_still_reported(lint_script, cookbook):
    """A missing `mcp_server_name` must not swallow the violation."""
    path = cookbook("leaky", tools=[{"type": "mcp_toolset"}])

    errors = lint_script._lint_one(path)

    assert len(errors) == 1
    assert "<unnamed>" in errors[0]


def test_an_enabled_write_config_is_reported(lint_script, cookbook):
    path = cookbook("writer", tools=_with_config({"name": "write", "enabled": True}))

    errors = lint_script._lint_one(path)

    assert len(errors) == 1
    assert "write" in errors[0]


@pytest.mark.parametrize("tool", ["slack_send_message", "slack_post", "slackbot"])
def test_slack_tools_are_reported(lint_script, cookbook, tool):
    """Matched by prefix, so the rule covers the whole family, not one name."""
    path = cookbook("chatty", tools=_with_config({"name": tool, "enabled": True}))

    errors = lint_script._lint_one(path)

    assert len(errors) == 1
    assert tool in errors[0]
    assert "handoff_request" in errors[0]


def test_a_default_enabled_toolset_is_reported(lint_script, cookbook):
    """Undocumented fourth rule: an enabled default grants tools it cannot enumerate."""
    tools = clean_orchestrator_tools()
    tools[0]["default_config"]["enabled"] = True

    errors = lint_script._lint_one(cookbook("permissive", tools=tools))

    assert any("default_config.enabled=false" in e for e in errors)


def test_an_enabled_default_reaches_configs_with_no_explicit_flag(lint_script, cookbook):
    """`enabled` falls back to the default, so a bare entry inherits the grant.

    Two violations from one change: the implicit `write` and the default that
    made it implicit. A linter that reported only the default would leave the
    reader thinking Write was never granted.
    """
    tools = clean_orchestrator_tools()
    tools[0]["default_config"]["enabled"] = True
    tools[0]["configs"].append({"name": "write"})  # no explicit `enabled`

    errors = lint_script._lint_one(cookbook("permissive", tools=tools))

    assert len(errors) == 2
    assert any("must not enable 'write'" in e for e in errors)
    assert any("default_config.enabled=false" in e for e in errors)


def test_an_mcp_entry_short_circuits_its_own_configs(lint_script, cookbook):
    """`continue` after the mcp finding — the entry is condemned, not audited twice."""
    path = cookbook("leaky", tools=[{
        "type": "mcp_toolset",
        "mcp_server_name": "box",
        "configs": [{"name": "write", "enabled": True}],
    }])

    assert len(lint_script._lint_one(path)) == 1


def test_a_non_mapping_tools_entry_is_reported(lint_script, cookbook):
    path = cookbook("odd", tools=["agent_toolset_20260401"])

    errors = lint_script._lint_one(path)

    assert len(errors) == 1
    assert "tools[0] is not a mapping" in errors[0]


def test_a_non_mapping_config_entry_is_silently_skipped(lint_script, cookbook):
    """Asymmetry, pinned rather than endorsed.

    A malformed `tools[i]` is reported; a malformed `configs[j]` inside a
    well-formed entry is skipped without comment. `configs: [read, write]` is
    a natural way to get the shorthand wrong, and it lints clean — the author
    reads that as "no over-grant" when it is really "nothing was inspected".
    """
    tools = clean_orchestrator_tools()
    tools[0]["configs"].append("write")

    assert lint_script._lint_one(cookbook("odd", tools=tools)) == []


# ---------------------------------------------------------------------------
# What the linter deliberately passes over
# ---------------------------------------------------------------------------


def test_a_disabled_write_config_is_clean(lint_script, cookbook):
    """Declaring a tool and switching it off is how the cookbooks say "not this one"."""
    path = cookbook("careful", tools=_with_config({"name": "write", "enabled": False}))

    assert lint_script._lint_one(path) == []


def test_toolset_types_other_than_agent_toolset_are_ignored(lint_script, cookbook):
    """Only `mcp_toolset` and `agent_toolset*` are inspected; anything else falls through.

    A future toolset type therefore ships unlinted rather than flagged, which
    is the safer default for a check that gates PRs — but it does mean the
    rule set is a denylist, not an allowlist.
    """
    path = cookbook("future", tools=[{
        "type": "computer_20260401",
        "configs": [{"name": "write", "enabled": True}],
    }])

    assert lint_script._lint_one(path) == []


@pytest.mark.parametrize("tool", ["Slack_send_message", "SLACK_SEND"])
def test_slack_matching_is_case_sensitive(lint_script, cookbook, tool):
    """Documented behavior, not an endorsement.

    `name.startswith("slack")` is exact, so a capitalized variant is missed.
    Tool names arrive from a fixed API vocabulary that is lowercase, so this
    is a naming-drift risk rather than a live hole — pinned so that if the
    matching is ever made case-insensitive, it is a decision someone made.
    """
    path = cookbook("chatty", tools=_with_config({"name": tool, "enabled": True}))

    assert lint_script._lint_one(path) == []


def test_subagent_manifests_are_not_linted(lint_script, cookbook, cookbooks_dir, capsys):
    """The glob is `*/agent.yaml`. Leaves are where MCP and Write are supposed to be.

    Linting them with the orchestrator's rules would flag every correct
    cookbook in the repo.
    """
    cookbook("demo")
    leaf = cookbooks_dir / "demo" / "subagents"
    leaf.mkdir(parents=True)
    (leaf / "writer.yaml").write_text(
        "tools:\n  - {type: mcp_toolset, mcp_server_name: box}\n", encoding="utf-8"
    )

    assert lint_script.main() == 0
    assert "box" not in capsys.readouterr().err


# ---------------------------------------------------------------------------
# Malformed documents
# ---------------------------------------------------------------------------


@pytest.mark.xfail(
    strict=True,
    reason="known gap: _lint_one assumes a well-formed mapping. An empty or "
           "comment-only agent.yaml makes yaml.safe_load return None, and a "
           "non-string `type` or non-mapping `default_config` reaches "
           ".startswith/.get — all raise AttributeError out of main() as an "
           "opaque traceback. Remove this marker when fixed.",
)
@pytest.mark.parametrize("text", [
    pytest.param("", id="empty-file"),
    pytest.param("# scaffolded, not written yet\n", id="comments-only"),
    pytest.param("tools:\n  - type: 123\n", id="type-not-a-string"),
    pytest.param("tools:\n  - {type: agent_toolset_x, default_config: enabled}\n",
                 id="default-config-not-a-mapping"),
])
def test_a_malformed_cookbook_is_reported_rather_than_raised(lint_script, cookbooks_dir,
                                                             text):
    """`touch agent.yaml` in a new cookbook directory is enough to trigger this.

    Either outcome would be fine — reporting it as a violation, or treating a
    document with no `tools:` block as nothing to lint. Raising is not: the
    linter is the pre-PR gate, and a traceback names Python internals rather
    than the file that needs fixing.
    """
    path = _write_raw(cookbooks_dir, "scaffold", text)

    assert isinstance(lint_script._lint_one(path), list)


# ---------------------------------------------------------------------------
# main() — exit codes and reporting
# ---------------------------------------------------------------------------


def test_a_missing_cookbooks_dir_exits_2(lint_script, tmp_path, monkeypatch, capsys):
    """Distinct from a lint failure: 2 means the check never ran."""
    monkeypatch.setattr(lint_script, "COOKBOOKS_DIR", tmp_path / "gone")

    assert lint_script.main() == 2
    assert "no cookbooks dir" in capsys.readouterr().err


def test_an_empty_tree_exits_zero_and_says_nothing(lint_script, capsys):
    """Documented gap: nothing to lint is indistinguishable from everything passing.

    A misconfigured path that happens to exist reports success in silence.
    The only signal is the absent ✓ lines, which no CI step asserts on.
    """
    assert lint_script.main() == 0

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_violations_exit_1_and_report_on_stderr(lint_script, cookbook, capsys):
    """stdout stays clean so a CI log shows only the failures."""
    cookbook("leaky", tools=[{"type": "mcp_toolset", "mcp_server_name": "box"}])

    assert lint_script.main() == 1

    captured = capsys.readouterr()
    assert captured.out == ""
    assert "tool-scope lint FAILED:" in captured.err
    assert "box" in captured.err


def test_clean_cookbooks_are_listed_in_sorted_order(lint_script, cookbook, capsys):
    for slug in ["zeta", "alpha", "mid"]:
        cookbook(slug)

    assert lint_script.main() == 0

    listed = [line.split()[1] for line in capsys.readouterr().out.splitlines()]
    assert listed == ["alpha", "mid", "zeta"]


def test_no_clean_summary_is_printed_when_anything_fails(lint_script, cookbook, capsys):
    """One bad cookbook suppresses the whole ✓ list — the run failed, not partly passed."""
    cookbook("good")
    cookbook("leaky", tools=[{"type": "mcp_toolset", "mcp_server_name": "box"}])

    assert lint_script.main() == 1
    assert "good" not in capsys.readouterr().out
