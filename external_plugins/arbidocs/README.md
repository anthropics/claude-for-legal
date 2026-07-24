# ARBI

ARBI is an AI-native document workspace for legal teams. Upload your own documents — contracts, pleadings, correspondence, research memos — and search or query them with Claude. Data is encrypted in transit and at rest.

- Search your workspace using hybrid semantic and keyword search across all uploaded documents, with citation-level provenance on every result.
- Ask the ARBI AI assistant questions about your documents and receive answers grounded in your own case files.
- Upload documents directly from Claude Code into your ARBI workspace.
- Organize documents with folders and tags across matters or practice areas.

## Example use cases

1. Search my workspace for any document mentioning the liquidated damages clause in the Northfield contract.
2. What does the Jones settlement agreement say about confidentiality obligations for the plaintiff?
3. Find all emails in the Smith matter that reference the October board meeting.

## Tools

| Tool | What it does |
|---|---|
| `search_documents` | Hybrid semantic + keyword search across your workspace — returns matched chunks with document title, date, and source provenance. |
| `retrieve` | Retrieve the AI assistant's answer to a question about your workspace documents, with citations. |
| `send_message` | Ask the ARBI AI assistant a question in a conversation thread and receive a cited answer grounded in your documents. |
| `upload_file` | Upload a local file (PDF, DOCX, TXT) into your ARBI workspace for storage and search. |
| `list_documents` | List documents in your workspace with metadata (title, date, nature, status). |
| `get_document` | Fetch full metadata for a specific document. |
| `list_folders` | List all folder paths in the workspace. |
| `list_tags` | List all tags defined in the workspace. |

All read tools are non-destructive. Write tools (`upload_file`, `send_message`) modify workspace state.

## When to use / When not to use

- ✅ Searching your own uploaded documents for specific clauses, facts, or references
- ✅ Asking questions grounded in documents you have uploaded to your workspace
- ✅ Uploading new documents for storage and later retrieval
- ❌ Searching public legal databases, case law, or statutes (use a legal research connector instead)
- ❌ Legal advice — ARBI retrieves and synthesizes your documents; a licensed lawyer applies the law to your facts

## Skills

| Skill | Does |
|---|---|
| `/arbidocs:search` | Search workspace documents using hybrid semantic search and return cited results |
| `/arbidocs:ask` | Ask the ARBI AI assistant a question about workspace documents and return a cited answer |

### Setup

An ARBI account is required. Sign up at https://arbidocs.com. When you add the ARBI connector in Claude, you will be prompted to authenticate with your ARBI account via OAuth.

### Links

- **Website:** https://arbidocs.com
- **Documentation:** https://arbidocs.com/docs
- **Support:** support@arbi.city
