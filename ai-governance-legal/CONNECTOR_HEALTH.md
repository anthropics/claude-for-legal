# LawAI Gov Hub — Connector Health Check

This file records the end-to-end health check performed against the LawAI Gov Hub MCP server before this connector entry was added to `.mcp.json`. **Two captures** are documented below: a local capture during development and a **live production capture against `https://mcp.lawaigovhub.com/mcp/`** — the URL the connector resolves to in the plugin's `.mcp.json`.

To reproduce, clone the [lawaigovhub repo](https://github.com/Brokemountain/http-lawaigovhub.com-) and run `python -m mcp_server` plus `pytest mcp_server/tests/`, or hit the live endpoint with the official MCP Python client.

## Result

**PASS** — server identifies as `LawAI Gov Hub` over the streamable-HTTP transport, all five tools answer, primary-source policy enforced (0 aggregator URLs leaked under `official_only=true`), unknown-id errors return the contracted `isError=true` MCP error shape.

## Production capture

Captured at **2026-05-15T08:55:25Z** against `https://mcp.lawaigovhub.com/mcp/`.

### Service identity

| Field | Value |
| --- | --- |
| Service | `lawai-gov-hub-mcp` |
| Version | `1.0.0` |
| MCP protocol version | `2025-11-25` |
| Server name (from `initialize`) | `LawAI Gov Hub` |
| Transport | Streamable HTTP |
| TLS | Let's Encrypt (auto-renewed by certbot) |

### `/healthz` response (live)

```json
{
  "status": "ok",
  "service": "lawai-gov-hub-mcp",
  "version": "1.0.0",
  "transport": "streamable-http",
  "endpoint": "/mcp",
  "regulations_indexed": 14275,
  "jurisdictions_total": 265,
  "active_jurisdictions": 240,
  "hallucination_cases_indexed": 1275,
  "site_stats": {
    "total_profiles": 265,
    "country_profiles": 252,
    "regional_profiles": 13,
    "active_profiles": 240,
    "total_entries": 14394
  },
  "tools": [
    "search_regulations",
    "fetch_regulation",
    "list_jurisdictions",
    "search_cases",
    "fetch_case"
  ]
}
```

### Probes (live)

| # | Probe | Result |
| - | --- | --- |
| 1 | `search_regulations(query="EU AI Act", jurisdiction="EU", year_from=2024)` | `total=9`; first hit is the official EUR-Lex corrigendum `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689R(01)`, `is_primary_source=true` |
| 2 | `fetch_regulation(id="eu:a60727cb8857")` | Round-trips the id; same `source_url` as probe 1; `retrieved_at=2026-05-15T08:53:28+00:00` |
| 3 | `list_jurisdictions(active_only=true)` | `total=240`; top three by entry count: US (4533), GB (957), CN (933) |
| 4 | `search_cases(query="sanction")` | `total=355`; first hit: `Staley v. City of Elba, et al.` |
| 5 | **Aggregator audit** (`search_regulations(limit=100, official_only=true)`) | **0** non-primary URLs in the sample of 100 — primary-source policy enforced |
| 6 | `fetch_regulation(id="NOPE:000000000000")` | `isError=true`, body begins `Error executing tool fetch_regulation: No regulation with id` — contracted MCP error shape, no transport-level exception |

The aggregator audit is the contract enforcement: with `official_only=true`, every result is on a primary source (government register, court system, intergovernmental body). The blocklist covers `regulations.ai`, `incidentdatabase.ai`, `wp.oecd.ai`, `techieray.com`, `damiencharlotin.com`, and major social/blog hosts; the allowlist covers `.gov`, `.gov.<cctld>`, `.europa.eu`, `.gob.*`, `.gouv.*`, `.int`, parliament/legislature domains, and similar.

## Local capture (development)

Captured at **2026-05-14T14:42:06Z** against `http://127.0.0.1:8767/mcp/` during development. Same five tools, same response shape, same audit result (0 non-primary URLs in 100). The local capture is what the 12-test pytest suite validates on every change.

## Reproducing this check

From a clone of the [lawaigovhub repo](https://github.com/Brokemountain/http-lawaigovhub.com-):

```bash
python -m venv .venv && . .venv/bin/activate
pip install "mcp[cli]>=1.16" httpx pytest uvicorn starlette
python -m pytest mcp_server/tests/ -v   # 12 tests, ~4s
```

To probe the live endpoint:

```bash
curl -sS https://mcp.lawaigovhub.com/healthz
curl -sS -X POST https://mcp.lawaigovhub.com/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## What the connector cannot do

For transparency:

- It is **read-only**. There are no write tools, no auth flows, no PII exchange — the dataset is public AI regulation.
- Source coverage matches the public website at `lawaigovhub.com`. When a primary register has not yet been linked for an entry, the entry is still indexed but `is_primary_source` will be `false`; the default `official_only=true` filters those out.
- Citation strings are formatted for legal documents but **do not relieve the lawyer of verifying the cite against the linked primary source**. The plugin already flags this in its citation-tiering language; the connector enforces it by always linking the primary source so verification is one click away.

## Operational notes

- The MCP server runs as a `lawai-mcp` systemd unit on the same DigitalOcean droplet as `lawaigovhub.com`, on `127.0.0.1:8765`. nginx terminates TLS for `mcp.lawaigovhub.com` and proxies to the local service.
- TLS certificate auto-renews via certbot's scheduled task (Let's Encrypt cert).
- DNS-rebinding protection is enabled in the MCP transport: only `mcp.lawaigovhub.com` and loopback are accepted as Host headers.
