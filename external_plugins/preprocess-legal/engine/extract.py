"""Text-native PDF extraction backend (pdfplumber).

This is the ONLY module that imports pdfplumber. Everything else in the engine
speaks in terms of ``ExtractionResult``, so the backend is swappable — slice 2's
OCR cascade plugs in behind the same ``Extractor`` interface without touching the
scoring or gate logic.

Failure policy: any error (missing pdfplumber, encrypted or corrupt PDF) returns
``ExtractionResult(ok=False, ...)`` rather than raising. The gate treats a failed
extraction as an automatic withhold — the engine fails closed, never silently
passing a document it could not read.
"""

from __future__ import annotations

from .models import ExtractionResult


def extract_text(source_path: str) -> ExtractionResult:
    try:
        import pdfplumber
    except ImportError as exc:  # pragma: no cover - environment dependent
        return ExtractionResult(
            source_path=source_path,
            ok=False,
            error=f"pdfplumber not installed: {exc}",
        )

    try:
        page_texts = []
        with pdfplumber.open(source_path) as pdf:
            for page in pdf.pages:
                page_texts.append(page.extract_text() or "")
        return ExtractionResult(source_path=source_path, page_texts=page_texts, ok=True)
    except Exception as exc:  # noqa: BLE001 - fail closed on any reader error
        return ExtractionResult(
            source_path=source_path,
            ok=False,
            error=f"{type(exc).__name__}: {exc}",
        )
