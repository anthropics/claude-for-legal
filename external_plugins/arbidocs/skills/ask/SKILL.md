---
name: arbidocs:ask
version: 0.1.0
description: >
  Use this skill when the user wants to ask a question about documents in their ARBI
  workspace and receive a cited AI answer — e.g. "what does my contract say about
  termination?", "summarize the Jones dispute", "what are my obligations under the NDA?".
allowed-tools:
  - mcp
---

# Ask ARBI

Sends a question to the ARBI AI assistant and returns a cited answer grounded in the user's workspace documents.

## Prerequisites

The `ARBI` MCP server must be connected. Verify it is available before starting. If not connected, inform the user and stop.

## When to Use

- User asks a question about their documents ("what does X say about Y?")
- User wants a synthesized answer with citations from their workspace
- User wants to continue a conversation thread about their documents

## When Not to Use

- **User wants raw search results, not an AI answer** — use `/arbidocs:search` instead
- **Questions about public law that aren't in the workspace** — use a legal research connector
- **Legal advice** — ARBI synthesizes what your documents say; a licensed lawyer advises on implications

## Workflow

### 1. Understand the question
Identify:
- What the user is asking about (a specific document, a topic, a matter)
- Whether this is a new question or a follow-up to a prior conversation

### 2. Ask the ARBI AI assistant

**Option A — New question (no prior conversation):**

Call `send_message` with:
- `message` (string, required): The user's question in natural language

**Option B — Follow-up in an existing conversation:**

If the user is continuing a previous exchange, use the `conversation_ext_id` from the prior `send_message` response:
- `message` (string, required): The follow-up question
- `conversation_ext_id` (string, optional): ID from the prior turn to maintain thread context

### 3. Present the answer
- Present the `response` text returned by `send_message`
- If citations are included in the response, preserve them — do not strip or paraphrase citations
- Preserve citations exactly as returned — do not paraphrase, reformat, or strip citation markers
- If the answer is "I don't have information about that", tell the user — do not fill the gap with outside knowledge

### 4. Offer follow-up
After presenting the answer:
- Offer to search for related documents via `/arbidocs:search`
- Offer to ask a follow-up question (use the same `conversation_ext_id`)
- If the answer cited specific documents, offer to retrieve them via `get_document`

## Communication Rules
- Never expose `conversation_ext_id`, `msg_ext_id`, or internal ARBI IDs to the user
- Do not mention tool call names or implementation details
- If the ARBI assistant returns an error or quota message, translate it to plain language
