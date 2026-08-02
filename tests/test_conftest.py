# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Checks on the fixtures themselves.

`conftest.py` carries real logic — path-based loading, a stand-in for an
absent dependency, and two import-time constants redirected away from the
repo — and the modules that will consume it land over the following weeks.
Until they do, nothing executes any of it, and a broken loader would sit
green. These tests are that coverage.

Several are canaries in the same spirit as
`test_shell_static.test_known_mktemp_templates_are_still_parsed`: a fixture
whose "valid" default has quietly stopped being valid still produces passing
tests, because every assertion about a rejection keeps holding for the wrong
reason. Pinning the defaults against the real schemas is what keeps the
modules built on them honest.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------


def test_validate_script_loads(validate_script):
    assert callable(validate_script.main)
    assert callable(validate_script._load)


def test_hyphenated_script_loads(lint_script):
    """`lint-tool-scope.py` is not a valid identifier and needs the path loader."""
    assert callable(lint_script._lint_one)
    assert callable(lint_script.main)


def test_orchestrate_loads_without_the_anthropic_package(orchestrate):
    """The suite depends on pytest, jsonschema and pyyaml — not on `anthropic`.

    `orchestrate.py` imports it at module scope, so without the stand-in this
    module cannot be loaded at all on a clean environment.
    """
    assert callable(orchestrate.extract_handoff)
    assert callable(orchestrate.sanitize_event)


def test_anthropic_stand_in_refuses_to_build_a_client(orchestrate):
    with pytest.raises(AssertionError, match="live session"):
        orchestrate.anthropic.Anthropic()


def test_stand_in_does_not_leak_into_sys_modules(orchestrate):
    """Whatever `import anthropic` means elsewhere, it is not this object."""
    assert orchestrate.anthropic is not sys.modules.get("anthropic")


# ---------------------------------------------------------------------------
# Audit-log isolation
# ---------------------------------------------------------------------------


def test_audit_log_is_redirected_out_of_the_repo(orchestrate, handoff_text, tmp_path):
    """`AUDIT_PATH` is relative, so an unredirected write lands in the CWD.

    `.gitignore` covers `/outputs/`, not `/out/`, which is where the default
    resolves — an untracked audit log in the repo root is one `git add -A`
    from a PR.
    """
    repo_audit = REPO_ROOT / "out" / "handoff-audit.jsonl"
    existed_before = repo_audit.exists()

    assert orchestrate.extract_handoff(handoff_text(target="not-a-deployed-agent")) is None

    assert orchestrate.AUDIT_PATH.is_relative_to(tmp_path)
    assert orchestrate.AUDIT_PATH.exists(), "the rejection was not logged anywhere"
    assert repo_audit.exists() == existed_before


def test_audit_records_reads_back_a_rejection(orchestrate, handoff_text, audit_records):
    assert audit_records() == []

    orchestrate.extract_handoff(handoff_text(target="not-a-deployed-agent"))

    records = audit_records()
    assert len(records) == 1
    assert records[0]["result"] == "reject"
    assert records[0]["reason"] == "target_not_allowlisted"


# ---------------------------------------------------------------------------
# Handoff payload defaults
# ---------------------------------------------------------------------------


def test_default_handoff_is_approved(orchestrate, handoff_text, audit_records):
    """Canary: the factory's no-argument output must clear every gate.

    Tests that vary one field and assert a rejection are only meaningful if
    the unvaried blob is accepted. If this fails, those tests are passing on
    a broken baseline rather than on the field they name.
    """
    result = orchestrate.extract_handoff(handoff_text(), source_agent="diligence-grid")

    assert result is not None
    assert result["target_agent"] == "reg-monitor"
    assert result["intent"] == "slack_send_message"
    assert audit_records()[-1]["result"] == "approve"


@pytest.mark.parametrize("intent", sorted(["slack_send_message", "launch_review",
                                           "deal_debrief", "playbook_monitor"]))
def test_default_params_satisfy_every_intent_schema(orchestrate, handoff_text, intent):
    """Canary: each intent's stock parameters match its pattern constraints."""
    result = orchestrate.extract_handoff(handoff_text(intent=intent))

    assert result is not None, f"stock params for {intent!r} no longer validate"
    assert result["intent"] == intent


def test_intent_coverage_is_complete(orchestrate):
    """Canary: a new intent upstream must come with stock parameters here.

    Without this, `test_default_params_satisfy_every_intent_schema` silently
    stops covering the addition.
    """
    from conftest import _VALID_PARAMS

    assert set(_VALID_PARAMS) == set(orchestrate.HANDOFF_INTENTS)


def test_surrounding_prose_does_not_break_extraction(orchestrate, handoff_text):
    """The blob arrives inside a text stream, and text carries braces.

    A non-greedy regex stops at the first `}` and truncates the payload; a
    greedy one runs past the object into later braces. PR #56 replaced that
    regex with `raw_decode`, and this is the shape that distinguishes them.
    """
    text = handoff_text(
        before="Report is ready. Emitting handoff:\n",
        after="\nDone. (Config was {\"retries\": 2}.)",
    )

    assert orchestrate.extract_handoff(text) is not None


# ---------------------------------------------------------------------------
# Cookbook trees
# ---------------------------------------------------------------------------


def test_default_cookbook_is_clean(lint_script, cookbook):
    """Canary: the stock `tools:` block must pass the linter it is baseline for."""
    assert lint_script._lint_one(cookbook()) == []


def test_cookbook_violations_are_detected(lint_script, cookbook):
    """One change to the stock block, one violation — the shape every lint test takes."""
    tools = [{"type": "mcp_toolset", "mcp_server_name": "box"}]

    errs = lint_script._lint_one(cookbook("leaky", tools=tools))

    assert len(errs) == 1
    assert "mcp_toolset" in errs[0]


def test_main_walks_the_fixture_tree_not_the_repo(lint_script, cookbook, capsys):
    """`COOKBOOKS_DIR` is bound at import time to the real tree."""
    cookbook("alpha")
    cookbook("beta")

    assert lint_script.main() == 0

    out = capsys.readouterr().out
    assert "alpha" in out and "beta" in out
    assert "diligence-grid" not in out, "main() reached the repo's own cookbooks"


# ---------------------------------------------------------------------------
# validate.py inputs
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", ["doc.json", "doc.yaml", "doc.yml"])
def test_write_doc_round_trips_through_the_suffix_dispatch(validate_script, write_doc, name):
    """`validate.py` picks its parser off the suffix; both must reach one object."""
    obj = {"status": "ok", "items": [1, 2, 3]}

    assert validate_script._load(write_doc(obj, name)) == obj
