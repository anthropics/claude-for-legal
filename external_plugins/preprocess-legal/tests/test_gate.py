"""The gate: routing, pass/withhold, and the exact bytes written for the redirect."""

from pathlib import Path

import pytest

from engine.confidence import score_extraction
from engine.config import PreprocessConfig
from engine.gate import Decision, decide, process
from engine.models import ExtractionResult


# --- fake extractors (no pdfplumber) ---------------------------------------

def _text_native(_path):
    page = "Lorem ipsum dolor sit amet. " * 60
    return ExtractionResult(source_path=_path, page_texts=[page, page, page], ok=True)


def _scanned(_path):
    return ExtractionResult(source_path=_path, page_texts=["", "", ""], ok=True)


def _failed(_path):
    return ExtractionResult(source_path=_path, ok=False, error="encrypted")


def _cfg(tmp_path, **overrides):
    cfg = PreprocessConfig(enabled=True, cache_dir=str(tmp_path))
    for k, v in overrides.items():
        setattr(cfg, k, v)
    return cfg


# --- decide() (pure) --------------------------------------------------------

def test_decide_pass_and_withhold():
    high = score_extraction(_text_native("d.pdf"))
    low = score_extraction(_scanned("d.pdf"))
    assert decide(high, 0.65) is Decision.PASS
    assert decide(low, 0.65) is Decision.WITHHOLD


# --- process() end to end ---------------------------------------------------

def test_pass_writes_clean_text(tmp_path):
    res = process("matter/contract.pdf", _cfg(tmp_path), extractor=_text_native)
    assert res.decision is Decision.PASS
    out = Path(res.redirect_path)
    assert out.is_file()
    assert "Lorem ipsum" in out.read_text(encoding="utf-8")
    assert "WITHHELD" not in out.read_text(encoding="utf-8")


def test_scanned_writes_withheld_marker(tmp_path):
    res = process("matter/exhibit.pdf", _cfg(tmp_path), extractor=_scanned)
    assert res.decision is Decision.WITHHOLD
    text = Path(res.redirect_path).read_text(encoding="utf-8")
    assert "DOCUMENT WITHHELD FROM CONTEXT" in text
    assert "matter/exhibit.pdf" in text


def test_failed_extraction_withholds(tmp_path):
    res = process("matter/broken.pdf", _cfg(tmp_path), extractor=_failed)
    assert res.decision is Decision.WITHHOLD
    assert "WITHHELD" in Path(res.redirect_path).read_text(encoding="utf-8")


def test_disabled_config_skips(tmp_path):
    res = process("matter/contract.pdf", _cfg(tmp_path, enabled=False), extractor=_text_native)
    assert res.decision is Decision.SKIP
    assert res.redirect_path is None


def test_non_pdf_skips(tmp_path):
    res = process("matter/notes.txt", _cfg(tmp_path), extractor=_text_native)
    assert res.decision is Decision.SKIP


def test_warm_cache_reuses_without_reextracting(tmp_path):
    calls = {"n": 0}

    def counting(_path):
        calls["n"] += 1
        return _text_native(_path)

    cfg = _cfg(tmp_path)
    first = process("matter/contract.pdf", cfg, extractor=counting)
    second = process("matter/contract.pdf", cfg, extractor=counting)
    assert calls["n"] == 1  # second call hit the cache
    assert first.cached is False and second.cached is True
    assert second.decision is Decision.PASS
    assert first.redirect_path == second.redirect_path


def test_min_bytes_floor_skips_small_files(tmp_path):
    # A real small file: below the byte floor, not worth extraction latency.
    small = tmp_path / "small.pdf"
    small.write_bytes(b"%PDF-1.4 tiny")
    cfg = _cfg(tmp_path, min_bytes_to_route=1_000_000)
    res = process(str(small), cfg, extractor=_text_native)
    assert res.decision is Decision.SKIP
