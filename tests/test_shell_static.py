# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""Static checks for the shell scripts under `scripts/`.

No harness, no network, no API key: these assertions read the scripts as text
and shell out only to `bash -n`.

The `mktemp -t` check exists because `scripts/test-cookbooks.sh` structurally
cannot cover it. That harness runs `deploy-managed-agent.sh <slug> --dry-run`,
and `deploy-managed-agent.sh` has two `-t` templates: the `skillcache` one
executes on every invocation, but the `skill` one sits inside `upload_skill()`
*after* the `DRY_RUN` early return, so it is reachable only on a live deploy
with `ANTHROPIC_API_KEY` set. Reverting that second template to a bare prefix
would leave every cookbook passing dry-run and break only in production on
Linux. Reading the templates statically covers both call sites equally.

Behavioral testing of the scripts (network calls, API stubbing, `bats` or
subprocess harnesses) is a follow-up; this module is deliberately limited to
what needs no harness at all.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = sorted((REPO_ROOT / "scripts").glob("*.sh"))

# Capture a `mktemp` invocation's arguments up to the close of its command
# substitution or the end of the line. Stopping at `)` is what keeps
# `"$(mktemp -t skill.XXXXXX).zip"` from reporting a template of
# `skill.XXXXXX).zip`.
MKTEMP = re.compile(r"mktemp\b([^)\n]*)")
DASH_T = re.compile(r"(?:^|\s)-t\s+(\S+)")

# GNU mktemp expands a run of at least three trailing X's and errors out on a
# template without one; BSD/macOS mktemp treats the X's as literal prefix text
# and appends its own randomness. A template ending in X's is the portable
# form, and the repo's own convention is six.
TRAILING_X = re.compile(r"X{3,}$")


def mktemp_t_templates(path: Path) -> list[tuple[int, str]]:
    """Return `(lineno, template)` for every `mktemp -t <template>` in `path`.

    Only the `-t <template>` spelling is recognized. `mktemp` with no template
    and the `--tmpdir` long form carry no portability constraint of this kind
    and are intentionally not reported.
    """
    found = []
    for lineno, line in enumerate(path.read_text().splitlines(), 1):
        for args in MKTEMP.findall(line):
            match = DASH_T.search(args)
            if match:
                found.append((lineno, match.group(1)))
    return found


def test_scripts_are_discovered():
    """Guard against a vacuous pass if `scripts/` moves or the glob breaks."""
    assert SCRIPTS, f"no *.sh found under {REPO_ROOT / 'scripts'}"


def test_known_mktemp_templates_are_still_parsed():
    """Guard against a vacuous pass if the parser stops matching.

    `deploy-managed-agent.sh` carries two `mktemp -t` call sites, both patched
    upstream in PR #41. If this count drops, either the script was restructured
    or `MKTEMP`/`DASH_T` no longer match it — both cases need a human, because
    the portability assertion below would otherwise pass by finding nothing.
    """
    deploy = REPO_ROOT / "scripts" / "deploy-managed-agent.sh"
    templates = mktemp_t_templates(deploy)
    assert len(templates) >= 2, (
        f"expected at least 2 `mktemp -t` templates in {deploy.name}, "
        f"parsed {len(templates)}: {templates}"
    )


@pytest.mark.parametrize("script", SCRIPTS, ids=lambda p: p.name)
def test_bash_syntax(script: Path):
    proc = subprocess.run(
        ["bash", "-n", str(script)], capture_output=True, text=True
    )
    assert proc.returncode == 0, (
        f"bash -n {script.name} failed:\n{proc.stderr.strip()}"
    )


@pytest.mark.parametrize("script", SCRIPTS, ids=lambda p: p.name)
def test_mktemp_t_templates_are_portable(script: Path):
    """Every `mktemp -t` template must end in X's (upstream PR #41).

    A bare prefix such as `mktemp -t skill` works on macOS and fails on Linux,
    which was how the original bug reached main: it was authored and reviewed on
    BSD mktemp and took `test-cookbooks.sh` down to 0/5 on GNU coreutils.
    """
    bad = [
        f"  {script.name}:{lineno}: mktemp -t {template}"
        for lineno, template in mktemp_t_templates(script)
        if not TRAILING_X.search(template)
    ]
    assert not bad, (
        "`mktemp -t` template(s) with no trailing X run on BSD/macOS and fail "
        "outright on GNU mktemp, which needs at least three X's. Append "
        "`.XXXXXX`:\n" + "\n".join(bad)
    )
