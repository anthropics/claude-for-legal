"""preprocess-legal extraction engine.

Slice 1: text-native PDF extraction + per-document confidence scoring + a gate
that refuses to silently pass degraded output into the model's context.

The engine is deliberately split so the parts that need the pdfplumber dependency
(``extract``) are isolated from the pure decision logic (``confidence``, ``gate``).
Only ``extract`` imports pdfplumber; everything else operates on plain data and is
unit-testable without any PDF library installed. This keeps the extraction backend
swappable (the interface, not pdfplumber, is the contract) per the plugin's design.
"""

from .confidence import ConfidenceScore, score_extraction
from .gate import Decision, ProcessResult, decide, process
from .config import PreprocessConfig, load_config

__all__ = [
    "ConfidenceScore",
    "score_extraction",
    "Decision",
    "ProcessResult",
    "decide",
    "process",
    "PreprocessConfig",
    "load_config",
]
