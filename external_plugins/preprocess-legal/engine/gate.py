"""The gate: extract → score → decide → materialize the file the model will read.

This is the orchestration layer. Given a source document path and a config, it:

  1. Routes  — decides whether this file is even in scope (config.routes()).
  2. Extracts — pulls text via the injected backend (default: pdfplumber).
  3. Scores   — per-document confidence (confidence.score_extraction()).
  4. Gates    — pass vs. withhold against the threshold.
  5. Writes   — the exact bytes the model will see: clean text on a pass, or an
                honest withheld-marker on a fail. Never degraded text silently.

Step 5 is the whole point. Because the engine writes the file the redirect hook
points at, "refuse to pass degraded output" is literal: a low-confidence scan
becomes a marker that *says* it was withheld, not hollow text masquerading as the
document.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, Optional

from .confidence import ConfidenceScore, score_extraction
from .config import PreprocessConfig
from .models import ExtractionResult

# An extractor is any callable path -> ExtractionResult. The default binds to
# pdfplumber lazily (see _default_extractor) so importing this module — and
# running the pure decision tests — never requires pdfplumber to be installed.
Extractor = Callable[[str], ExtractionResult]


class Decision(str, Enum):
    PASS = "pass"          # clean text, redirect the read to it
    WITHHOLD = "withhold"  # degraded/failed, redirect to an honest marker
    SKIP = "skip"          # out of scope, leave the read untouched


@dataclass
class ProcessResult:
    decision: Decision
    # The path the PreToolUse hook should redirect the Read to. None on SKIP,
    # which tells the hook to pass the original read through unchanged.
    redirect_path: Optional[str]
    score: Optional[ConfidenceScore]
    cached: bool = False
    source_path: str = ""


def decide(score: ConfidenceScore, threshold: float) -> Decision:
    """Pure pass/withhold decision — no I/O, trivially testable."""
    return Decision.PASS if score.overall >= threshold else Decision.WITHHOLD


def _cache_key(path: Path) -> str:
    """Stable key from path + size + mtime so re-reading an unchanged file hits
    the warm cache instead of re-extracting (the latency mitigation)."""
    try:
        st = path.stat()
        sig = f"{path.resolve()}|{st.st_size}|{int(st.st_mtime)}"
    except OSError:
        sig = str(path)
    return hashlib.sha256(sig.encode("utf-8")).hexdigest()[:16]


def _withheld_marker(source_path: str, score: ConfidenceScore, threshold: float) -> str:
    return (
        "[preprocess-legal] DOCUMENT WITHHELD FROM CONTEXT\n"
        "\n"
        f"Source: {source_path}\n"
        f"Reason: extraction {score.reason()} did not clear the confidence "
        f"threshold ({threshold:.2f}).\n"
        "\n"
        "This document is likely scanned or image-based. A text extractor "
        "returned little or no reliable text, so passing it into context would "
        "risk handing you plausible-looking but hollow or structurally-broken "
        "content (lost tables, dropped exhibit stamps, invisible redactions).\n"
        "\n"
        "It was deliberately NOT passed through silently. Next steps:\n"
        "  - Enable the OCR fallback (not yet available in this slice), or\n"
        "  - Open the source document directly for this exhibit.\n"
    )


def _default_extractor(source_path: str) -> ExtractionResult:
    # Lazy import: only touched at real runtime, never during pure tests.
    from .extract import extract_text

    return extract_text(source_path)


def process(
    source_path: str,
    config: PreprocessConfig,
    extractor: Optional[Extractor] = None,
) -> ProcessResult:
    """Run the full pipeline for one document. Safe to call on any path; returns
    a SKIP result (no redirect) for anything out of scope."""
    path = Path(source_path)

    if not config.routes(path):
        return ProcessResult(Decision.SKIP, None, None, source_path=source_path)

    cache_dir = Path(config.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = _cache_key(path)
    out_path = cache_dir / f"{key}.txt"

    # Warm-cache hit: an unchanged file we've already processed. Reuse the
    # materialized text/marker without re-extracting.
    if out_path.is_file():
        # Re-derive the decision label from the marker header so callers still
        # get a meaningful decision on a cache hit.
        head = out_path.read_text(encoding="utf-8", errors="replace")[:64]
        decision = Decision.WITHHOLD if "WITHHELD" in head else Decision.PASS
        return ProcessResult(
            decision, str(out_path), None, cached=True, source_path=source_path
        )

    extract = extractor or _default_extractor
    result: ExtractionResult = extract(source_path)
    score = score_extraction(result, min_chars_per_page=config.min_chars_per_page)
    decision = decide(score, config.threshold)

    if decision is Decision.PASS:
        out_path.write_text(result.full_text, encoding="utf-8")
    else:
        out_path.write_text(
            _withheld_marker(source_path, score, config.threshold),
            encoding="utf-8",
        )

    return ProcessResult(
        decision, str(out_path), score, cached=False, source_path=source_path
    )
