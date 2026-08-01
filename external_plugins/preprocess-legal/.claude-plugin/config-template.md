# preprocess-legal — configuration

The engine reads a JSON config. Point the hook at it with the
`PREPROCESS_LEGAL_CONFIG` environment variable, or place it at the default path:

```
~/.claude/plugins/config/claude-for-legal/preprocess/config.json
```

## Example

```json
{
  "enabled": true,
  "threshold": 0.65,
  "min_chars_per_page": 100,
  "file_types": [".pdf"],
  "min_bytes_to_route": 0,
  "cache_dir": ""
}
```

## Fields

| Field | Default | Meaning |
|-------|---------|---------|
| `enabled` | `false` | Master switch. Opt-in — while `false`, every Read passes through untouched. |
| `threshold` | `0.65` | Confidence at or above this passes through as clean text; below it, the document is withheld. |
| `min_chars_per_page` | `100` | Characters a page must clear to count as "covered" text (separates a real page from a scanned image's stray characters). |
| `file_types` | `[".pdf"]` | Only these suffixes are intercepted. Everything else is passed through. |
| `min_bytes_to_route` | `0` | Files smaller than this are read directly (not worth extraction latency). `0` disables the floor. |
| `cache_dir` | `""` | Where extracted text / withheld markers are written. Empty → a `.preprocess-cache/` folder beside this config. |

A missing or malformed config falls back to the safe default (disabled) — a
broken config never breaks your Read tool.
