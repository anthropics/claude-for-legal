"""Plain data types shared across the engine.

These carry no dependencies (no pdfplumber, no I/O) so both the extraction
backend and the pure scoring/gate logic can import them freely.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class ExtractionResult:
    """The output of a text-extraction pass over one document.

    ``page_texts`` is the raw text pulled from each page, in order. A scanned /
    image-only PDF run through a text extractor yields empty or near-empty
    strings here — that emptiness is exactly the signal the confidence scorer
    keys on, so we keep per-page granularity rather than one merged blob.
    """

    source_path: str
    page_texts: List[str] = field(default_factory=list)
    # True only if the extractor completed without raising. A hard failure
    # (corrupt/encrypted PDF) is different from a successful-but-empty scan and
    # the gate treats it as an automatic withhold.
    ok: bool = True
    error: str = ""

    @property
    def page_count(self) -> int:
        return len(self.page_texts)

    @property
    def full_text(self) -> str:
        return "\n".join(self.page_texts)
