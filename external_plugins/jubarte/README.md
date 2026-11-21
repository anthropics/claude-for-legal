# jubarte

Real tracked changes for Word documents, on the user's own machine.

jubarte is an open-source engine (Apache-2.0, written in Rust) that reads a `.docx`,
applies edits as Word tracked changes with comments, compares two versions into a
redline, accepts or rejects changes, checks that Word will open the result, and
renders pages to PDF. This plugin connects it to Claude through a local MCP server
and adds a skill that tells Claude how to deliver a redline a lawyer can send.

- **No account, no subscription, no upload.** The server speaks stdio and opens no
  network port. It reads and writes only under the folder it was started in.
- **Edits that cannot land in the wrong place.** Each edit names one paragraph and
  one exact phrase. If a phrase is missing or appears twice, the whole plan is refused
  and nothing is written.
- **Works beside the practice-area plugins.** They decide what the contract should
  say; this one puts it into the document as tracked changes.

## Example use cases

1. Redline this NDA against our playbook and send me the Word file with tracked changes and a comment on each change.
2. Compare the vendor's draft with the version we sent on Friday and show me what they changed.
3. Accept all of our changes, reject opposing counsel's change to the indemnity cap, and give me a clean copy.
4. Before I send this, check that Word opens it cleanly and tell me which comments are still in it.

## Install

```
/plugin install jubarte --marketplace anthropics/claude-for-legal
```

## Requirements

[`uv`](https://docs.astral.sh/uv/) on the machine running Claude. The server is
started with `uvx --from 'jubarte-docx[mcp]==0.19.0' jubarte-mcp --root .`, which
downloads the `jubarte-docx` wheel from PyPI on first use. Nothing else is installed:
no LibreOffice, pandoc or Word.

## Tools

`docx_text`, `docx_inspect`, `docx_edit`, `docx_compare`, `docx_changes`,
`docx_accept`, `docx_reject`, `docx_validate`, `docx_comments`, `docx_audit`,
`docx_render`, `docx_capabilities`. Read tools carry the MCP read-only hint. No tool
replaces an existing file unless asked to. Details:
<https://github.com/jandira-tech/jubarte/blob/main/docs/adoption/mcp.md>.

## Artifacts

[`artifacts/`](./artifacts) holds three single-file pages that run the same engine
in the browser as WebAssembly. Paste one into Claude as an artifact, or open it
from disk. Each fetches the engine from cdn.jsdelivr.net (`jubarte-wasm@0.19.0`);
the documents stay in the tab.

| File | What it does |
|---|---|
| `word-to-pdf.html` | Word to PDF, with tracked changes and comments printed as Word prints them |
| `redline-two-drafts.html` | Two drafts in, one Word file with tracked changes out |
| `jubarte-desk.html` | Review changes one by one, compare, scrub names and comments, validate, print to PDF |

## What has been measured

On Crosby's RedlineBench and on the redline tasks of Harvey's Legal Agent
Benchmark, agents given jubarte scored the same as agents given each benchmark's own
document tools, and used fewer tokens and less time: about half on RedlineBench, 6%
to 14% on Harvey's tasks. One early run was slower. The legal quality of the markup
did not improve; the mechanics got cheaper and the output is a file Word accepts.

## Limits

- It does not give legal advice or decide what a clause should say.
- `.docx` only. Legacy `.doc`, PDF and Google Docs are out of scope.
- Rendering uses jubarte's own layout engine. It follows Word closely, and a page
  break can still fall differently from Word's.

## Support

Issues: <https://github.com/jandira-tech/jubarte/issues>.
Security reports: <https://github.com/jandira-tech/jubarte/security/advisories/new>.
