# Tests for `scripts/`

Proposed pytest suite for the repo's tooling. The scripts under `scripts/`
carry real logic — output-schema validation, cookbook tool-scope linting, and
the security-sensitive handoff machinery in `orchestrate.py` — but currently
have no automated tests. Two of the three outside contributions merged to date
were fixes to these scripts ([#41], [#56]); this suite starts by pinning those
fixes down as regression tests so they cannot silently reappear.

[#41]: https://github.com/anthropics/claude-for-legal/pull/41
[#56]: https://github.com/anthropics/claude-for-legal/pull/56

## Proposed layout

```
tests/
  README.md                     # this file
  conftest.py                   # shared fixtures: tmp cookbook trees, sample payloads
  test_validate.py              # validate.py — schema pass/fail, YAML+JSON loading,
                                #   exit codes (0 valid / 1 invalid / 2 usage)
  test_lint_tool_scope.py       # lint-tool-scope.py — orchestrator over-grant
                                #   detection, clean-cookbook pass, exit codes
  test_orchestrate_sanitize.py  # orchestrate.py — _strip_controls / sanitize_event:
                                #   control chars, zero-width/bidi chars, length caps
  test_orchestrate_handoff.py   # orchestrate.py — extract_handoff / _validate_params:
                                #   nested-payload regression (#56), injection-shaped
                                #   params rejected, frame_handoff wrapping
  test_shell_static.py          # deploy-managed-agent.sh / test-cookbooks.sh —
                                #   bash -n syntax smoke; every mktemp -t template
                                #   ends in X's (#41 regression, including the
                                #   call site no dry-run can reach)
  fixtures/
    cookbooks/                  # minimal synthetic agent.yaml + subagents/ trees
    payloads/                   # sample handoff/event texts (synthetic only)
```

## Design decisions

- **pytest only; no new runtime dependencies.** The scripts already require
  `jsonschema` and `pyyaml`; the suite adds nothing beyond `pytest` itself.
- **Scripts are imported, not shelled out to, where possible.** `scripts/` is
  not a package, so `conftest.py` loads modules by path via `importlib`. Exit
  codes and CLI behavior get a thin `subprocess` smoke test each; unit tests
  target the functions directly.
- **Regression tests are keyed to upstream PRs.** Each carries a comment naming
  the PR it pins: the `extract_handoff` nested-`}` truncation from #56 in
  `test_orchestrate_handoff.py`, the `mktemp -t` template portability from #41
  in `test_shell_static.py`.
- **All fixture data is synthetic.** No client material, no real matter names,
  no content derived from practice — fixtures are minimal invented YAML/JSON
  shaped only to exercise the code paths.
- **The `mktemp -t` check covers a gap `test-cookbooks.sh` cannot.** #41 patched
  two `-t` templates in `deploy-managed-agent.sh`. Only one of them — the
  `skillcache` file opened at the top of the script — runs under `--dry-run`,
  which is all `test-cookbooks.sh` exercises; the `skill` template sits inside
  `upload_skill()` past the `DRY_RUN` early return and is reachable only on a
  live deploy with `ANTHROPIC_API_KEY` set. Reverting that second one would
  leave every cookbook passing dry-run and break only in production on Linux.
  Reading both templates as text covers them equally, with no network, no
  credentials, and no particular coreutils.
- **Static means static — the templates are not executed.** An earlier draft ran
  each extracted `mktemp` on the host. That tests coreutils rather than this
  repo, and for the one template a dry-run already reaches, it duplicates
  `test-cookbooks.sh`. `bash -n` plus the template assertion is the whole
  module. Behavioral testing of `deploy-managed-agent.sh` and
  `test-cookbooks.sh` (network calls, API stubbing, `bats` or subprocess
  harnesses) remains a follow-up.
- **Static checks carry a canary.** `test_known_mktemp_templates_are_still_parsed`
  fails if fewer than two `mktemp -t` sites parse out of
  `deploy-managed-agent.sh`, so a restructured script or a broken regex surfaces
  as a failure rather than as an assertion that silently checks nothing.
- **CI-ready but CI-independent.** The suite runs with plain
  `python3 -m pytest tests/` from the repo root; wiring it into a GitHub
  Actions workflow is a separate, later proposal.

## Running

```
pip install pytest jsonschema pyyaml
python3 -m pytest tests/
```

## Status

`test_shell_static.py` has landed: 6 tests, needing nothing beyond `pytest`
and `bash`. `conftest.py` and the remaining modules are still proposals and
land incrementally.
