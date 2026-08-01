"""Confidence scoring: the signal that separates a clean text-native PDF from a
scanned exhibit that a text extractor hollowed out."""

from engine.confidence import score_extraction
from engine.models import ExtractionResult


def _pages(*texts):
    return ExtractionResult(source_path="doc.pdf", page_texts=list(texts), ok=True)


def test_text_native_scores_high():
    # Three full pages of ordinary body text.
    page = "Lorem ipsum dolor sit amet. " * 60  # ~1600 chars
    score = score_extraction(_pages(page, page, page))
    assert score.overall >= 0.65
    assert score.dimensions["coverage"] == 1.0
    assert score.dimensions["density"] == 1.0
    assert score.dimensions["legibility"] > 0.99


def test_scanned_empty_pages_score_near_zero():
    # A scanned/image PDF: the text extractor returns empty strings per page.
    score = score_extraction(_pages("", "", ""))
    assert score.overall == 0.0
    assert score.dimensions["coverage"] == 0.0
    assert score.dimensions["density"] == 0.0


def test_failed_extraction_scores_zero():
    result = ExtractionResult(source_path="x.pdf", ok=False, error="encrypted")
    score = score_extraction(result)
    assert score.overall == 0.0


def test_no_pages_scores_zero():
    score = score_extraction(_pages())
    assert score.overall == 0.0
    assert score.page_count == 0


def test_sparse_pages_below_coverage_bar():
    # A dozen stray OCR-ish characters per page — below the coverage threshold,
    # so coverage collapses even though the page isn't literally empty.
    score = score_extraction(_pages("a b c d", "x y z", "1 2 3"), min_chars_per_page=100)
    assert score.dimensions["coverage"] == 0.0
    assert score.overall < 0.3


def test_mojibake_penalized_by_legibility():
    # Text that "extracted to something" but is mostly control/replacement bytes.
    garbage = "\x00\x01�\x02�" * 400  # long, dense, but illegible
    score = score_extraction(_pages(garbage, garbage, garbage))
    # Coverage/density can look fine; legibility is what catches this.
    assert score.dimensions["legibility"] < 0.1
    assert score.overall < 0.65


def test_reason_string_is_human_readable():
    page = "Lorem ipsum dolor sit amet. " * 60
    score = score_extraction(_pages(page))
    r = score.reason()
    assert "confidence=" in r and "coverage=" in r and "chars/page" in r
