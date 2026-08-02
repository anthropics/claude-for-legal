# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""`validate.py` — harness-side schema validation of worker output.

The script is 44 lines and its contract is three exit codes: 0 valid, 1
invalid, 2 usage. What makes it worth testing is not its size but its
position — the deploy harness runs it between a reader subagent and the
orchestrator, and branches on the exit code. Whatever it says is what the
pipeline believes about a worker's output.

The schemas it validates against are not synthetic. They ship in this repo,
one per subagent under `output_schema:`, and the deploy script extracts them.
So the first section runs against those eleven real blocks rather than
fixtures: a schema that is itself malformed cannot validate anything, and
nothing else in the repo checks them.

Two behaviors are pinned as documented rather than endorsed. `_load` chooses
its parser by exact suffix, so `.YAML` is read as JSON. And `main()` handles
exactly one failure — `ValidationError` — while a missing file, a malformed
document and an invalid *schema* all escape as tracebacks that exit 1, the
same code as an honestly-invalid document. A harness branching on the exit
code cannot tell "the worker produced bad output" from "the path was wrong."
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATE_PY = REPO_ROOT / "scripts" / "validate.py"

# A small schema for the cases that are about the script rather than the repo.
SCHEMA = {
    "type": "object",
    "required": ["status"],
    "properties": {
        "status": {"type": "string", "enum": ["ok", "fail"]},
        "items": {"type": "array", "items": {"type": "integer"}},
    },
}


def _shipped_schemas() -> list[tuple[Path, dict]]:
    """Every `output_schema:` block declared by a subagent manifest."""
    found = []
    for path in sorted((REPO_ROOT / "managed-agent-cookbooks").glob("*/subagents/*.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(doc, dict) and "output_schema" in doc:
            found.append((path, doc["output_schema"]))
    return found


def _is_a_valid_schema(schema) -> bool:
    try:
        jsonschema.Draft202012Validator.check_schema(schema)
    except jsonschema.SchemaError:
        return False
    return True


SHIPPED_SCHEMAS = _shipped_schemas()
# The sweep below deliberately runs only over schemas that are valid. The ones
# that are not are the subject of their own test rather than a silent skip.
VALID_SHIPPED = [
    pytest.param(schema, id=f"{path.parent.parent.name}/{path.stem}")
    for path, schema in SHIPPED_SCHEMAS if _is_a_valid_schema(schema)
]


@pytest.fixture
def run_cli(validate_script, monkeypatch, capsys):
    """Invoke `main()` with a synthesised argv; return (exit code, stdout, stderr)."""

    def _run(*args) -> tuple[int, str, str]:
        monkeypatch.setattr(sys, "argv", ["validate.py", *(str(a) for a in args)])
        code = validate_script.main()
        captured = capsys.readouterr()
        return code, captured.out, captured.err

    return _run


# ---------------------------------------------------------------------------
# The schemas this repo ships
# ---------------------------------------------------------------------------


def test_the_shipped_output_schemas_are_discoverable():
    """Canary: a renamed tree would make every sweep below assert nothing."""
    assert len(SHIPPED_SCHEMAS) >= 11


@pytest.mark.xfail(
    strict=True,
    reason="known defect: diligence-grid/subagents/extractor.yaml declares "
           "`value: {type: [string, number, null]}`, and YAML's bare null is a "
           "null value where JSON Schema requires the string \"null\". The "
           "block fails check_schema, so validate.py raises SchemaError — which "
           "it does not catch — on any extractor output. Remove this marker "
           "once the schema is fixed.",
)
def test_every_shipped_output_schema_is_a_valid_json_schema():
    """A schema that is itself invalid cannot validate anything.

    `validate.py` exists to check worker output against these blocks, and
    `jsonschema.validate` calls `check_schema` before it looks at the
    instance. An invalid schema therefore fails every document put through
    it, in a way that reports as a crash rather than as a schema problem.
    """
    invalid = {}
    for path, schema in SHIPPED_SCHEMAS:
        try:
            jsonschema.Draft202012Validator.check_schema(schema)
        except jsonschema.SchemaError as exc:
            location = "/".join(str(part) for part in exc.absolute_path)
            invalid[path.relative_to(REPO_ROOT).as_posix()] = f"{exc.message} at {location}"

    assert invalid == {}


@pytest.mark.parametrize("schema", VALID_SHIPPED)
def test_every_valid_shipped_schema_rejects_an_empty_document(run_cli, write_doc, schema):
    """The real schemas driven through the real entry point.

    Every one declares a non-empty top-level `required`, so `{}` must be
    rejected — and rejected as a validation failure, not as a crash.
    """
    code, out, err = run_cli(write_doc({}, "instance.json"),
                             write_doc(schema, "schema.json"))

    assert code == 1
    assert err.startswith("INVALID: ")
    assert out == ""


# ---------------------------------------------------------------------------
# _load — choosing a parser by suffix
# ---------------------------------------------------------------------------


def test_yaml_features_parse_from_a_yaml_file(validate_script, tmp_path):
    """Comments, unquoted scalars and block style — none of it is JSON."""
    path = tmp_path / "doc.yaml"
    path.write_text("# a comment\nstatus: ok\nitems:\n  - 1\n  - 2\n", encoding="utf-8")

    assert validate_script._load(path) == {"status": "ok", "items": [1, 2]}


def test_yaml_syntax_in_a_json_file_is_rejected(validate_script, tmp_path):
    """The dispatch is one-way: JSON parses as YAML, YAML does not parse as JSON."""
    path = tmp_path / "doc.json"
    path.write_text("status: ok\n", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        validate_script._load(path)


@pytest.mark.parametrize("name", ["doc.txt", "doc", "doc.JSON", "doc.schema"])
def test_unrecognised_suffixes_fall_back_to_json(validate_script, tmp_path, name):
    """Only `.yaml` and `.yml` route to YAML; everything else is assumed JSON."""
    path = tmp_path / name
    path.write_text('{"status": "ok"}', encoding="utf-8")

    assert validate_script._load(path) == {"status": "ok"}


def test_the_suffix_check_is_case_sensitive(validate_script, tmp_path):
    """Documented, not endorsed: `.YAML` takes the JSON path and fails there.

    The failure is at least loud — a YAML document is rarely valid JSON — but
    it reports as a JSON syntax error on a file the author called YAML.
    """
    path = tmp_path / "doc.YAML"
    path.write_text("status: ok\n", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        validate_script._load(path)


def test_a_missing_file_raises_from_the_loader(validate_script, tmp_path):
    """Correct at this level — a loader has nothing useful to return."""
    with pytest.raises(FileNotFoundError):
        validate_script._load(tmp_path / "absent.json")


# ---------------------------------------------------------------------------
# main() — the exit-code contract
# ---------------------------------------------------------------------------


def test_a_conforming_document_exits_0(run_cli, write_doc):
    code, out, err = run_cli(write_doc({"status": "ok"}, "instance.json"),
                             write_doc(SCHEMA, "schema.json"))

    assert (code, out.strip(), err) == (0, "OK", "")


def test_a_nonconforming_document_exits_1(run_cli, write_doc):
    """stdout stays empty on failure, so a harness capturing it sees nothing."""
    code, out, err = run_cli(write_doc({"status": "maybe"}, "instance.json"),
                             write_doc(SCHEMA, "schema.json"))

    assert code == 1
    assert out == ""
    assert "INVALID: " in err


@pytest.mark.parametrize("argc", [0, 1, 3])
def test_the_wrong_argument_count_exits_2(run_cli, argc):
    """2 is distinct from 1 — the check never ran, as opposed to failing."""
    code, out, err = run_cli(*[f"arg{n}" for n in range(argc)])

    assert code == 2
    assert "Usage:" in err
    assert out == ""


def test_a_yaml_schema_pairs_with_a_json_instance(run_cli, write_doc):
    """The usage line offers `<output.json> <schema.json|schema.yaml>`."""
    code, out, _ = run_cli(write_doc({"status": "ok"}, "instance.json"),
                           write_doc(SCHEMA, "schema.yaml"))

    assert (code, out.strip()) == (0, "OK")


# ---------------------------------------------------------------------------
# The INVALID message
# ---------------------------------------------------------------------------


def test_the_message_locates_a_nested_failure(run_cli, write_doc):
    """`absolute_path` joined with `/` — the reason it is worth printing."""
    instance = {"status": "ok", "items": [1, "two"]}

    _, _, err = run_cli(write_doc(instance, "instance.json"),
                        write_doc(SCHEMA, "schema.json"))

    assert err.strip().endswith(" at items/1")


def test_a_root_level_failure_has_no_location_to_report(run_cli, write_doc):
    """`absolute_path` is empty, so the message trails off after "at".

    Cosmetic, and pinned only so that tidying it up is a deliberate change
    rather than a surprise to whoever parses this output.
    """
    _, _, err = run_cli(write_doc({}, "instance.json"),
                        write_doc(SCHEMA, "schema.json"))

    assert err.strip() == "INVALID: 'status' is a required property at"


# ---------------------------------------------------------------------------
# The CLI
# ---------------------------------------------------------------------------


def _cli(*args) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(VALIDATE_PY), *(str(a) for a in args)],
                          cwd=REPO_ROOT, capture_output=True, text=True)


def test_the_cli_exits_0_and_prints_ok(write_doc):
    """The documented invocation, out of process, as the harness runs it."""
    completed = _cli(write_doc({"status": "ok"}, "instance.json"),
                     write_doc(SCHEMA, "schema.json"))

    assert completed.returncode == 0
    assert completed.stdout.strip() == "OK"


def test_the_cli_exits_2_with_no_arguments():
    completed = _cli()

    assert completed.returncode == 2
    assert "Usage:" in completed.stderr


@pytest.mark.parametrize("case", ["missing-file", "malformed-json", "malformed-yaml",
                                  "invalid-schema"])
def test_unhandled_inputs_still_fail_without_claiming_success(write_doc, tmp_path, case):
    """`main()` catches `ValidationError` and nothing else.

    A missing file, an unparseable document and a schema that fails
    `check_schema` all escape as tracebacks and exit 1 — the same code an
    honestly-invalid document produces. These assertions deliberately check
    only that the run fails and never prints OK, so they keep holding if the
    handling is ever improved; the collision itself is documented here rather
    than asserted.
    """
    schema = write_doc(SCHEMA, "schema.json")
    if case == "missing-file":
        instance = tmp_path / "absent.json"
    elif case == "malformed-json":
        instance = tmp_path / "broken.json"
        instance.write_text("{oops", encoding="utf-8")
    elif case == "malformed-yaml":
        instance = tmp_path / "broken.yaml"
        instance.write_text("items: [1, 2\n", encoding="utf-8")
    else:
        instance = write_doc({"status": "ok"}, "instance.json")
        schema = write_doc({"type": "not-a-json-schema-type"}, "badschema.json")

    completed = _cli(instance, schema)

    assert completed.returncode != 0
    assert "OK" not in completed.stdout
