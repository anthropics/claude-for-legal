"""Per-document extraction confidence scoring.

Pure functions over an ``ExtractionResult`` — no I/O, no PDF library. Given the
text a backend pulled out of a document, decide how much to trust it.

The score is deliberately a breakdown, not a single opaque number. A confidence
value with no per-dimension reasons is not auditable, and the whole point of the
gate is that an attorney (or a downstream task) can see *why* a document was held
back. Each dimension is a 0..1 signal; ``overall`` is their weighted mean.

Dimensions
----------
coverage    Fraction of pages that produced real text. A scanned exhibit run
            through a text extractor returns empty pages — low coverage is the
            loudest signal that this document is image-based, not text-native.
density     Mean characters per page, saturated against a text-native baseline.
            A page with 12 stray characters scores near zero; a full page of
            body text saturates to 1.0.
legibility  Fraction of extracted characters that are actually readable (letters,
            digits, ordinary punctuation, whitespace) rather than control bytes
            or Unicode replacement chars. Catches the dangerous case: text that
            extracted to *something* but is mojibake — plausible-looking garbage
            that nothing downstream would flag.
"""

from __future__ import annotations

import string
from dataclasses import dataclass
from typing import Dict

from .models import ExtractionResult

# Characters we consider legible. Everything printable, plus whitespace.
_LEGIBLE = set(string.printable)

# A full page of body text runs well over a thousand characters. We saturate the
# density signal here so that anything at or above a normal text page scores 1.0
# and only sparse / near-empty pages are penalized.
_DENSITY_SATURATION_CHARS = 1200.0

# Coverage and density measure *quantity* — is there enough text on the page.
# They are combined into a quantity score, coverage weighted higher because "the
# extractor returned nothing for this page" is the highest-signal indicator of an
# image-only document.
_QUANTITY_WEIGHTS: Dict[str, float] = {
    "coverage": 0.6,
    "density": 0.4,
}
# Legibility measures *quality* — is the extracted text actually readable rather
# than mojibake. It multiplies the quantity score rather than adding to it, so it
# acts as a veto: a page full of illegible bytes has high quantity but cannot pass
# on quantity alone. This is the defense against text that "extracted to something"
# but is structurally garbage — the expensive way to be wrong in a case file.


@dataclass
class ConfidenceScore:
    """A 0..1 overall score plus the per-dimension breakdown behind it."""

    overall: float
    dimensions: Dict[str, float]
    page_count: int
    mean_chars_per_page: float

    def reason(self) -> str:
        """One-line human explanation, used in the withheld marker."""
        parts = [f"{k}={v:.2f}" for k, v in self.dimensions.items()]
        return (
            f"confidence={self.overall:.2f} "
            f"({', '.join(parts)}; {self.page_count} pages, "
            f"{self.mean_chars_per_page:.0f} chars/page)"
        )


def _legibility(text: str) -> float:
    # Whitespace-only text carries no legible content — its "printable" newlines
    # must not manufacture confidence for an effectively empty page.
    if not text.strip():
        return 0.0
    legible = sum(1 for ch in text if ch in _LEGIBLE)
    return legible / len(text)


def score_extraction(
    result: ExtractionResult,
    *,
    min_chars_per_page: int = 100,
) -> ConfidenceScore:
    """Score how trustworthy an extraction is.

    ``min_chars_per_page`` is the bar a page must clear to count as "covered" —
    below it, a page is treated as effectively blank (a scanned image yields a
    handful of stray characters at most).
    """
    pages = result.page_texts
    page_count = len(pages)

    # A hard extraction failure or a document with no pages has no trustworthy
    # text by definition. Return an all-zero score so the gate withholds it.
    if not result.ok or page_count == 0:
        dims = {"coverage": 0.0, "density": 0.0, "legibility": 0.0}
        return ConfidenceScore(0.0, dims, page_count, 0.0)

    covered = sum(1 for p in pages if len(p.strip()) >= min_chars_per_page)
    coverage = covered / page_count

    total_chars = sum(len(p) for p in pages)
    mean_chars = total_chars / page_count
    density = min(mean_chars / _DENSITY_SATURATION_CHARS, 1.0)

    legibility = _legibility(result.full_text)

    dims = {
        "coverage": round(coverage, 4),
        "density": round(density, 4),
        "legibility": round(legibility, 4),
    }
    # Quantity (weighted coverage + density) vetoed by quality (legibility).
    quantity = sum(_QUANTITY_WEIGHTS[k] * dims[k] for k in _QUANTITY_WEIGHTS)
    overall = quantity * legibility

    return ConfidenceScore(
        overall=round(overall, 4),
        dimensions=dims,
        page_count=page_count,
        mean_chars_per_page=round(mean_chars, 1),
    )
