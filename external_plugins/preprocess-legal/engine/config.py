"""Configuration for the preprocess-legal engine.

Loaded from the practice profile (a JSON file the cold-start / customize flow
writes). Everything has a safe default so the engine runs headless in tests and
so a missing/partial config never crashes a Read — it just falls back to
sensible behavior.

The capability is opt-in: ``enabled`` defaults to False. Nothing is intercepted
until the attorney turns it on.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class PreprocessConfig:
    # Master switch. Opt-in by design — an off config passes every Read through
    # untouched.
    enabled: bool = False

    # Confidence at or above this passes through as clean text; below it, the
    # document is withheld (slice 2 will route it to OCR instead).
    threshold: float = 0.65

    # A page must clear this many characters to count as "covered" text.
    min_chars_per_page: int = 100

    # Only these suffixes are routed. Anything else is passed through untouched.
    file_types: List[str] = field(default_factory=lambda: [".pdf"])

    # Files smaller than this are cheap enough to read directly — no point
    # paying extraction latency to save a few tokens. 0 disables the floor.
    min_bytes_to_route: int = 0

    # Where extracted text / withheld markers are written. Resolved to an
    # absolute path at load time. Defaults to a cache dir beside the config.
    cache_dir: str = ""

    def routes(self, path: Path) -> bool:
        """Should this path be intercepted at all?"""
        if not self.enabled:
            return False
        if path.suffix.lower() not in [s.lower() for s in self.file_types]:
            return False
        try:
            if self.min_bytes_to_route and path.stat().st_size < self.min_bytes_to_route:
                return False
        except OSError:
            return False
        return True


def load_config(config_path: Optional[str] = None) -> PreprocessConfig:
    """Load config from JSON, falling back to defaults for any missing key.

    A malformed or missing file yields the default (disabled) config rather than
    raising — a broken config must never break the user's Read tool.
    """
    cfg = PreprocessConfig()

    if config_path:
        p = Path(config_path)
        if p.is_file():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except (ValueError, OSError):
                data = {}
            for key in (
                "enabled",
                "threshold",
                "min_chars_per_page",
                "file_types",
                "min_bytes_to_route",
                "cache_dir",
            ):
                if key in data:
                    setattr(cfg, key, data[key])

    # Resolve the cache dir. Default: a hidden cache folder next to the config,
    # or under the current dir if no config path was given.
    if cfg.cache_dir:
        cache = Path(cfg.cache_dir).expanduser()
    elif config_path:
        cache = Path(config_path).expanduser().resolve().parent / ".preprocess-cache"
    else:
        cache = Path(".preprocess-cache")
    cfg.cache_dir = str(cache)

    return cfg
