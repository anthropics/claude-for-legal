# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Shared fixtures for the `scripts/` suite.

Three properties of the scripts under test shape everything here:

1. **They are not importable.** `scripts/` is not a package, and
   `lint-tool-scope.py` is not a valid Python identifier, so neither `import`
   nor `importlib.import_module` can reach them. Every module is loaded by
   path through `importlib.util.spec_from_file_location`.

2. **`orchestrate.py` imports `anthropic` at module scope**, which the suite
   deliberately does not depend on (`tests/README.md`: no new dependencies
   beyond pytest). The client is used only inside `run()`, which needs a live
   session and is out of scope, so the import is satisfied with a stand-in
   that turns any attempt to construct a client into a loud failure.

3. **They resolve paths at import time, not call time.** `lint-tool-scope.py`
   pins `COOKBOOKS_DIR` to the real cookbook tree and `orchestrate.py` pins
   `AUDIT_PATH` to `./out/handoff-audit.jsonl`. Both are redirected here.
   The audit redirect matters beyond isolation: `AUDIT_PATH` is *relative*, so
   an unredirected rejection test writes `out/handoff-audit.jsonl` into
   whatever directory pytest was launched from — the repo root, which does not
   gitignore `out/`. Tests reach `orchestrate.py` only through the
   `orchestrate` fixture, which cannot hand back an unredirected module.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import types
from contextlib import contextmanager
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"

# Sentinel for factory arguments where None is itself a meaningful value.
_UNSET = object()


# ---------------------------------------------------------------------------
# Loading the scripts
# ---------------------------------------------------------------------------


@contextmanager
def _stand_ins(modules: dict[str, types.ModuleType]):
    """Install stand-in modules in `sys.modules` for the duration of a load.

    Restores the previous state on exit, so a machine that does have the real
    package installed is left with it. The stand-in stays reachable through
    the loaded module's own globals either way — `import x` binds the name at
    exec time, and rebinding `sys.modules` afterwards does not disturb it.
    """
    saved = {name: sys.modules.get(name) for name in modules}
    sys.modules.update(modules)
    try:
        yield
    finally:
        for name, previous in saved.items():
            if previous is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = previous


def _load_script(filename: str, stand_ins: dict[str, types.ModuleType] | None = None):
    """Load `scripts/<filename>` by path and return the module object.

    The module is registered in `sys.modules` under a `scripts_`-prefixed,
    underscored name (`scripts_lint_tool_scope`) so it cannot shadow a real
    top-level package, and is unregistered again if execution raises.
    """
    path = SCRIPTS_DIR / filename
    if not path.is_file():
        raise FileNotFoundError(f"no script at {path}")
    modname = "scripts_" + path.stem.replace("-", "_")
    spec = importlib.util.spec_from_file_location(modname, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot build a module spec for {path}")
    module = importlib.util.module_from_spec(spec)
    with _stand_ins(stand_ins or {}):
        sys.modules[modname] = module
        try:
            spec.loader.exec_module(module)
        except BaseException:
            sys.modules.pop(modname, None)
            raise
    return module


def _anthropic_stand_in() -> types.ModuleType:
    """A stand-in for the `anthropic` package that refuses to build a client.

    `orchestrate.py` touches `anthropic` in exactly one place — the
    `Anthropic()` construction inside `run()`. Nothing this suite covers goes
    near it, so reaching this is a test straying into live-session territory
    rather than a missing dependency, and it should say so.
    """
    stub = types.ModuleType("anthropic")

    def _refuse(*_args, **_kwargs):
        raise AssertionError(
            "orchestrate.run() tried to construct an Anthropic client. This "
            "suite covers the pure handoff/sanitize helpers; anything needing "
            "a live session belongs behind an explicit mock."
        )

    stub.Anthropic = _refuse
    return stub


@pytest.fixture(scope="session")
def validate_script():
    """`scripts/validate.py` — `_load`, `main`."""
    return _load_script("validate.py")


@pytest.fixture(scope="session")
def _lint_module():
    """`scripts/lint-tool-scope.py`, unredirected. Use `lint_script`."""
    return _load_script("lint-tool-scope.py")


@pytest.fixture(scope="session")
def _orchestrate_module():
    """`scripts/orchestrate.py`, unredirected. Use `orchestrate`."""
    return _load_script("orchestrate.py", {"anthropic": _anthropic_stand_in()})


# ---------------------------------------------------------------------------
# orchestrate.py — audit-log isolation
# ---------------------------------------------------------------------------


@pytest.fixture
def orchestrate(_orchestrate_module, tmp_path, monkeypatch):
    """`scripts/orchestrate.py` with its audit log redirected into `tmp_path`.

    This is the only fixture that hands out the module. `extract_handoff`
    writes an audit record on every path it takes, approve or reject, so a
    module without this redirect leaves `out/handoff-audit.jsonl` behind in
    the working directory.
    """
    monkeypatch.setattr(
        _orchestrate_module, "AUDIT_PATH", tmp_path / "out" / "handoff-audit.jsonl"
    )
    return _orchestrate_module


@pytest.fixture
def audit_records(orchestrate):
    """Return a reader for the records written so far, oldest first.

    The audit record is part of the contract, not a side effect — the
    `raw_len` derivation that PR #56 changed is observable nowhere else — so
    it is captured for assertions rather than suppressed.
    """

    def _read() -> list[dict]:
        path = orchestrate.AUDIT_PATH
        if not path.exists():
            return []
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    return _read


# ---------------------------------------------------------------------------
# orchestrate.py — handoff payloads
# ---------------------------------------------------------------------------

# Parameter sets that satisfy each intent's schema in `HANDOFF_INTENTS`. Kept
# minimal and slug-shaped, matching the pattern rule the script documents.
_VALID_PARAMS: dict[str, dict] = {
    "slack_send_message": {"channel": "C01234567", "report_path": "./out/report.md"},
    "launch_review": {"ticket_id": "LEGAL-1234"},
    "deal_debrief": {"matter_id": "M-2026-014"},
    "playbook_monitor": {},
}


@pytest.fixture
def handoff_text():
    """Factory for agent output containing a `handoff_request` blob.

    Called with no arguments it produces a blob that passes every gate, so a
    test can vary one field and attribute the rejection to that field. The
    `before`/`after` arguments surround the JSON with prose: agent output is
    a text stream, and text carrying its own braces is what distinguishes
    `raw_decode` from the regex it replaced in PR #56.
    """

    def _make(
        *,
        target: str = "reg-monitor",
        intent: str = "slack_send_message",
        params=_UNSET,
        event=_UNSET,
        before: str = "",
        after: str = "",
    ) -> str:
        payload: dict = {"intent": intent}
        payload["params"] = _VALID_PARAMS.get(intent, {}) if params is _UNSET else params
        if event is not _UNSET:
            payload["event"] = event
        obj = {"type": "handoff_request", "target_agent": target, "payload": payload}
        return f"{before}{json.dumps(obj)}{after}"

    return _make


# ---------------------------------------------------------------------------
# lint-tool-scope.py — synthetic cookbook trees
# ---------------------------------------------------------------------------


def clean_orchestrator_tools() -> list[dict]:
    """The compliant orchestrator `tools:` block the real cookbooks ship.

    Local-only tools, `default_config.enabled` false, no `mcp_toolset`, no
    Slack. Every violation fixture is this block with one thing changed.
    """
    return [
        {
            "type": "agent_toolset_20260401",
            "default_config": {"enabled": False},
            "configs": [
                {"name": "read", "enabled": True},
                {"name": "grep", "enabled": True},
                {"name": "glob", "enabled": True},
            ],
        }
    ]


@pytest.fixture
def lint_script(_lint_module, cookbooks_dir):
    """`scripts/lint-tool-scope.py` with `COOKBOOKS_DIR` pointed at `tmp_path`.

    Only `COOKBOOKS_DIR` needs redirecting. `ROOT` exists to derive it at
    import time and is read nowhere else, so patching it as well would be
    theatre.
    """
    return _lint_module


@pytest.fixture
def cookbooks_dir(_lint_module, tmp_path, monkeypatch):
    """An empty stand-in for `managed-agent-cookbooks/`.

    `_lint_one(path)` takes its target as an argument and needs none of this,
    but `main()` globs `COOKBOOKS_DIR` and would otherwise walk the real tree
    — reporting on the repo's own cookbooks instead of the fixture's.
    """
    directory = tmp_path / "managed-agent-cookbooks"
    directory.mkdir()
    monkeypatch.setattr(_lint_module, "COOKBOOKS_DIR", directory)
    return directory


@pytest.fixture
def cookbook(cookbooks_dir):
    """Factory writing a synthetic `<slug>/agent.yaml`; returns its path.

    With no arguments the cookbook is clean, so a test can introduce exactly
    one violation and know what it is measuring. Pass `doc=` to write a
    mapping verbatim when the point of the test is a malformed document.
    Content is invented — no client material, no real matter names.

    A test that needs unparseable YAML rather than an unexpected shape can
    write the bytes itself; `cookbooks_dir` is the tree `main()` walks.
    """

    def _make(slug: str = "demo-cookbook", *, tools=_UNSET, doc: dict | None = None) -> Path:
        if doc is None:
            doc = {"name": slug, "model": "claude-opus-4-7"}
            doc["tools"] = clean_orchestrator_tools() if tools is _UNSET else tools
        directory = cookbooks_dir / slug
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / "agent.yaml"
        path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
        return path

    return _make


# ---------------------------------------------------------------------------
# validate.py — instance and schema files
# ---------------------------------------------------------------------------


@pytest.fixture
def write_doc(tmp_path):
    """Factory writing an object to `tmp_path` as JSON or YAML; returns its path.

    `validate.py` dispatches on the file suffix, so the suffix is the point:
    the same object written as `.json` and as `.yaml` must validate alike.
    """

    def _make(obj, name: str = "doc.json") -> Path:
        path = tmp_path / name
        if path.suffix in (".yaml", ".yml"):
            path.write_text(yaml.safe_dump(obj, sort_keys=False), encoding="utf-8")
        else:
            path.write_text(json.dumps(obj), encoding="utf-8")
        return path

    return _make
