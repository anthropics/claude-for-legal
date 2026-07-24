---
name: arbidocs:search
version: 0.1.0
description: >
  Use this skill when the user wants to search their ARBI workspace for documents,
  clauses, facts, or references — e.g. "find everything about the indemnification clause",
  "search for emails mentioning the merger", "what documents mention Jones v. Smith".
allowed-tools:
  - mcp
---

# ARBI Workspace Search

Searches the user's ARBI workspace using hybrid semantic + keyword search and returns matched document chunks with title, date, and citation provenance.

## Prerequisites

The `ARBI` MCP server must be connected. Verify it is available before starting. If not connected, inform the user and stop.

## When to Use

- User wants to find documents, clauses, or references in their workspace
- User asks "do I have anything about X", "search for Y", "find all Z"
- User needs to locate a specific fact, date, name, or clause across uploaded documents

## When Not to Use

- **Questions about public law, case law, or statutes** — use a legal research connector (CourtListener, CoCounsel Legal, etc.)
- **Questions requiring legal advice** — this skill retrieves text; a licensed lawyer applies it to facts
- **User wants an AI-generated answer, not search results** — use `/arbidocs:ask` instead

## Workflow

### 1. Understand the query
Identify what the user is looking for:
- A specific clause or provision (e.g., "indemnification", "limitation of liability")
- A fact, name, or date (e.g., "closing date", "John Smith", "October 2024")
- A document type (e.g., "all NDAs", "the Smith settlement")

### 2. Search the workspace
Call `search_documents` with the user's query.

**Parameters:**
- `query` (string, required): Natural language description of what to find
- `n_results` (int, optional): Number of results to return (default: 10; increase to 20 for broad searches)
- `search_mode` (string, optional): `"hybrid"` (default) for best results; `"semantic"` for conceptual; `"keyword"` for exact terms

### 3. Present results
- Show each result with: document title, date, a quoted excerpt, and a note of which document it came from
- Group results by document when multiple chunks come from the same source
- If no results, say so clearly — do not guess or hallucinate document content
- If results seem off-topic, try a rephrased search before concluding nothing exists

### 4. Offer to go deeper
After presenting results, offer to:
- Ask a follow-up question via `/arbidocs:ask`
- Retrieve the full document via `get_document`
- Search with different terms if the first results were not helpful
