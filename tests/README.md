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
  conftest.py                   # shared fixtures: path-loading the scripts,
                                #   tmp cookbook trees, handoff payload builders,
                                #   audit-log isolation
  test_conftest.py              # checks on the fixtures themselves — that the
                                #   stock payload really validates and the stock
                                #   cookbook really lints clean
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
```

## Design decisions

- **pytest only; no new runtime dependencies.** The scripts require
  `jsonschema` and `pyyaml`, which the suite reuses. `orchestrate.py` also
  imports `anthropic` at module scope, used in one place — the client
  constructed inside `run()`, which needs a live session and is out of scope.
  `conftest.py` satisfies that import with a stand-in that raises if anything
  tries to build a client, rather than taking on the SDK as a test dependency.
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
- **Fixtures are built by factories, not checked in.** Every lint case is the
  compliant `tools:` block with one thing changed, and every handoff case is a
  valid blob with one field varied. As files those would be a dozen
  near-identical trees whose small differences are the entire point. The
  factories live in `conftest.py` and default to the *passing* case, so a test
  introduces exactly one violation and can attribute the result to it.
- **The audit log is isolated, then asserted on.** `orchestrate.AUDIT_PATH` is
  relative, so an unredirected rejection test writes `out/handoff-audit.jsonl`
  into whatever directory pytest ran from — the repo root, which gitignores
  `/outputs/` but not `/out/`. The `orchestrate` fixture is the only way to
  reach the module and always redirects it under `tmp_path`. The records are
  then read back rather than discarded: the `raw_len` derivation that #56
  changed is observable nowhere else.
- **A known defect is an `xfail`, not a silent gap.** Where a script does the
  wrong thing, the suite asserts the behavior it *should* have under
  `xfail(strict=True)`: green while the defect stands, red the moment it is
  fixed and the marker outlives it. Fixing the scripts is a separate change —
  a tests PR should not edit what it tests. Two are marked so far.
  `extract_handoff` raises `TypeError` rather than rejecting when
  `target_agent` is a JSON array or object, because the allowlist check hashes
  the value. `_lint_one` raises `AttributeError` on an empty or comment-only
  `agent.yaml`, because `yaml.safe_load` returns `None` for one.
- **A control's documented limits are asserted, not implied.** `orchestrate.py`
  calls its denylist "trivially bypassed... not to stop a motivated attacker,"
  so `test_orchestrate_sanitize.py` carries a section asserting that
  homoglyphs, digit substitution and rephrasing pass straight through. Absent
  tests read as an absent weakness. If the denylist is ever hardened, those
  cases fail and the script's own docstring needs revisiting in the same
  change.
- **Invisible characters appear as escapes, never as literals.** A fixture
  containing a raw `U+200B` cannot be reviewed in a diff, which defeats the
  point of a test asserting that `U+200B` is removed.
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

Landed: `test_shell_static.py` (6 tests, needing nothing beyond `pytest` and
`bash`), `conftest.py` with `test_conftest.py` (20 tests over the fixtures),
`test_orchestrate_handoff.py` (64 cases over `extract_handoff` and
`_validate_params`), and `test_lint_tool_scope.py` (27 cases over `_lint_one`
and `main`, including the repo's own five cookbooks), and
`test_orchestrate_sanitize.py` (62 cases over `_strip_controls` and
`sanitize_event`). Six of those cases are expected failures — see above. One
module remains a proposal and lands next: `test_validate.py`.
