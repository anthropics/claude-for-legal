#!/usr/bin/env python3
"""PreToolUse hook: transparently redirect a Read of a heavy PDF to pre-extracted
text (or an honest withheld-marker) that the engine writes just-in-time.

Contract (Claude Code >= v2.1.190, CLI + Cowork + Desktop):
  stdin  : JSON with tool_name, tool_input.file_path, cwd, ...
  stdout : {"hookSpecificOutput": {"hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "updatedInput": {"file_path": "<redirect>"}}}
  exit 0 : always. This hook must never break a Read. On anything unexpected it
           prints nothing and exits 0, so the original file is read as normal.

The redirect target is materialized synchronously here — it must exist before the
Read returns, so extraction blocks the read (warm cache makes repeat reads cheap).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Make the sibling engine package importable regardless of cwd.
_PLUGIN_ROOT = Path(__file__).resolve().parent.parent
if str(_PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(_PLUGIN_ROOT))

_DEFAULT_CONFIG = (
    Path.home()
    / ".claude"
    / "plugins"
    / "config"
    / "claude-for-legal"
    / "preprocess"
    / "config.json"
)


def _passthrough() -> None:
    """Emit nothing and exit 0 — the original Read proceeds untouched."""
    sys.exit(0)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        _passthrough()

    if payload.get("tool_name") != "Read":
        _passthrough()

    file_path = (payload.get("tool_input") or {}).get("file_path")
    if not file_path:
        _passthrough()

    try:
        from engine import load_config, process
        from engine.gate import Decision

        config_path = os.environ.get("PREPROCESS_LEGAL_CONFIG") or (
            str(_DEFAULT_CONFIG) if _DEFAULT_CONFIG.is_file() else None
        )
        config = load_config(config_path)

        result = process(file_path, config)
        if result.decision is Decision.SKIP or not result.redirect_path:
            _passthrough()

        out = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "updatedInput": {"file_path": result.redirect_path},
            }
        }
        print(json.dumps(out))
        sys.exit(0)
    except Exception:
        # Fail open: never let a preprocessing error block a real Read.
        _passthrough()


if __name__ == "__main__":
    main()
