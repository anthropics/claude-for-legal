---
name: cite-check
description: Check every authority in a brief, memo, or letter before it is filed or sent. First confirms that each cited case exists under the name, court, and year the document gives it, so no fabricated or hallucinated case gets through; then checks the citation, pin cites, quotations, and characterized holdings against the opinion text. Use when the user says "cite-check this", "check the citations", "are any of these cases hallucinated", "verify the cites before we file", or hands over a draft written by an AI tool, a junior lawyer, or opposing counsel.
argument-hint: "[path to brief, memo, or letter]"
---

# /cite-check

1. Load `~/.claude/plugins/config/claude-for-legal/litigation-legal/CLAUDE.md` → citation format, matter workspace settings.
2. Follow the workflow below. Read `~/.claude/plugins/config/claude-for-legal/litigation-legal/verification-log.md` if it exists.
3. Check every citation. Do not sample.
4. Output: a cite-check report with a verdict. Never edit the document being checked.

---

# Cite Check

## Purpose

A fabricated case in a filing is sanctionable, and a real case cited for something it does not hold is how a tribunal stops trusting the rest of the brief. This skill does two checks, in order:

1. Existence. Every cited case is located in a primary source under the name, court, and year the document gives it.
2. Substance. Each located authority is cited correctly, and its quotations, parentheticals, and characterized holdings match the opinion.

The existence check runs first and runs on everything. The substance check is where most real errors are found (the "misgrounded citation": the case exists, but it does not say that), and it is the expensive part.

## The existence gate — unbypassable

A case that cannot be located in any source is reported as not located. It is never reported as "probably real," "likely an unpublished decision," or "may be in a database I can't reach." The row reads:

> Not located in any source checked; treat as fabricated until the author produces the opinion. Sources searched: [list].

Any not-located case makes the verdict FAIL. There is no lenient mode.

A case counts as located only when the opinion itself (or the court's docket entry for an order) has been opened and its caption, court, date, and reporter or docket citation match the document. These do not locate a case:

- a search-result snippet or a web-search summary;
- a secondary source (treatise, article, blog, news story) describing the case;
- a real case with a similar name in a different court or with a different citation.

## Known behavior of the CourtListener citation tools

Observed in October 2026 on a test passage containing one fabricated case name attached to a real reporter citation and one fabricated reporter citation. The workflow is built around these; re-test if the tools change.

1. `analyze_citations` deduplicates by reporter string. Two different case names on the same `volume reporter page` are merged into one cluster, and the tool's name-mismatch WARNING attaches to only one occurrence. In the test, "Hartwell v. Superior Ore Co., 463 U.S. 29 (1983)" (fabricated) was merged into Motor Vehicle Mfrs. Ass'n v. State Farm, 463 U.S. 29, and was not flagged. Step 4 (per-occurrence match) is what catches this.
2. Its case-name parser breaks on apostrophes and abbreviations. "Motor Vehicle Mfrs. Ass'n" was parsed as "Ass'" and produced a false WARNING on a correct citation. A WARNING is a lead for Step 4, not a finding.
3. NOT FOUND is a coverage gap as often as a fabrication. In the same test, State by Smart Growth Minneapolis v. City of Minneapolis, 954 N.W.2d 584 (Minn. 2021), a real state supreme court decision, returned NOT FOUND, identical to the fabricated citation. Every NOT FOUND goes to Step 5 before any conclusion.
4. The `case_name` search filter misses long official captions. A `case_name` search for "Smart Growth Minneapolis v. City of Minneapolis" returned nothing, while `q: "\"Smart Growth Minneapolis\""` found the cluster captioned "State of Minnesota by Smart Growth Minneapolis ...". Search by a distinctive quoted party phrase in `q`.

## Load context

**Matter context.** Check `## Matter workspaces` in the practice-level CLAUDE.md. If enabled and there is no active matter, ask: "Which matter is this for? Run `/litigation-legal:matter-workspace switch <slug>` or say `practice-level`." Write outputs to the matter folder at `~/.claude/plugins/config/claude-for-legal/litigation-legal/matters/<matter-slug>/`. Never read another matter's files unless `Cross-matter context` is `on`.

From the practice profile, use the house citation format (Bluebook, ALWD, or local) for Step 8.

## Workflow

### Step 1: Load the document

- `.md` and `.txt`: read directly.
- `.docx`: extract the text, including footnotes and endnotes. If the document has tracked changes, check the accepted-changes text and say so in the reviewer note.
- `.pdf`: extract the text layer. If the PDF is image-only, stop and say so. Do not guess at its contents.

Footnotes count. Many fabricated citations sit in string cites in footnotes.

### Step 2: Build the occurrence table

Run the CourtListener `extract_citations` tool on the full text with `resolve: true`, so id., supra, and short-form cites resolve to their full citation. A fabricated case often appears once in full and then only in short form; resolving short forms ties every later use back to the row that needs checking.

Then read the document and add what citation extraction misses: slip opinions and unpublished decisions cited by docket number, agency adjudications, Federal Register notices, docket and ECF cites, and record cites.

Each row carries:

- the case name exactly as written, and the citation, court, and year as written;
- the pin cite;
- the proposition, parenthetical, or quotation the citation supports, quoted from the document;
- where it appears (page, section, footnote).

Report the count: "Found [N] citations ([C] cases, [S] statutes and regulations, [O] other)."

If the CourtListener connector is not responding, build the table by reading the document and record the outage in the reviewer note.

### Step 3: Pass A — citation lookup

Run CourtListener `analyze_citations` with `text` set to the full document. Above 250 unique citation strings it returns a `job_id`; continue with `resume_citation_analysis`. For each citation string, record the cluster ID, canonical case name, decision date, court, and URL, or NOT FOUND.

### Step 4: Per-occurrence match

Compare every row of the occurrence table (not every cluster) with the record its citation resolved to: case name, court, and year as written against the cluster.

- Not a mismatch: reporter and Bluebook abbreviations ("Ass'n," "Cnty.," "Dep't"), "et al.," dropped first names, a short-form caption.
- A mismatch: a different party name, a different court, or a year that differs by more than the decision-versus-publication difference.

Mismatches and NOT FOUND rows both go to Step 5, searched by case name.

### Step 5: Pass B — second-source search by name

Search by case name and court, not by citation, in this order until the case is located:

1. CourtListener `search`: type `o` for opinions, type `r` for district-court orders on RECAP. Put a distinctive party phrase in `q` in quotes.
2. Any other connected case-law research tool (Westlaw, Lexis, Trellis, Descrybe, or a multi-jurisdiction primary-law database).
3. Web search for the court's own opinion page or PDF, the state law library archive, Harvard Caselaw Access Project scans, Justia, FindLaw, govinfo (federal courts), or the agency's own decision site for administrative adjudications.

Open the opinion before recording it as located. Then:

- Located under the document's citation: Located.
- Located, but under a different citation, court, or year, or with a different name: Located — correction needed. Give the correct citation.
- Not located after all of the above: Not located (the existence gate above applies).

### Step 6: Pass C — substance

For every located case that carries a quotation, a parenthetical, or a characterized holding, retrieve the opinion text (CourtListener `read_document`, the court's PDF, or the reporter scan) and check:

- **Quotations.** Each quotation appears verbatim in the opinion. Check it at the pin cited when the pin can be checked. Report a quotation that is close but not exact as not verbatim, with the opinion's actual words. A quotation not in the opinion at all makes the verdict FAIL.
- **Holdings and parentheticals.** The proposition matches what the court held, not what a party argued, what the court assumed without deciding, or what a dissent said. Compare element by element: a pin that supports part of the proposition is flagged as partial support, with the part it does not support named.
- **Subsequent history** visible in the sources read (reversed, vacated, review granted or denied, superseded by statute). If a citator connector (KeyCite, Shepard's) is available, run it; otherwise mark good-law status `[verify — citator not run]`.

Star pages to Westlaw or Lexis citations and pins that require a paid database cannot be checked without that connector. Mark them `[verify — pin not checked]`. Never "Located" for the pin.

For long documents, the substance checks can be split across subagents where the environment supports them. Each subagent returns, per row: status, the verbatim passage found, the source URL, and anything it could not check. Review every return before it goes into the report.

### Step 7: Statutes, regulations, and rules

Confirm each exists and that any quoted text is verbatim: the U.S. Code through govinfo or uscode.house.gov; the C.F.R. through eCFR, noting the version date and whether the section was in force on the date the document relies on; the Federal Register by volume and page on govinfo; state codes, rules, and session laws on the legislature's or revisor's site; court rules on the court's site. A cited section that does not exist is treated like a not-located case and makes the verdict FAIL.

### Step 8: Citation form

Check each citation against the house citation format from the practice profile. Record corrections in the summary table. Form errors alone produce PASS WITH CORRECTIONS, not FAIL.

### Step 9: Adverse authority (on request)

If the user asks, add a section on authority found during the check that cuts against the document's position. Report only from sources actually read.

### Step 10: Verification log

For each citation checked, append one line to `~/.claude/plugins/config/claude-for-legal/litigation-legal/verification-log.md`:

`[YYYY-MM-DD] [citation] checked by /cite-check against [source URL] — [located / corrected to X / not located / could not check]`

Prior log entries are listed in the report for the reviewer, but they do not skip the checks in this run.

## Verdict

| Verdict | When |
|---|---|
| PASS | Every authority located; every checked quotation verbatim; every checked proposition supported. Unchecked pins and citator status may remain `[verify]`. |
| PASS WITH CORRECTIONS | Every authority located, but at least one name, citation, court, year, pin, subsequent history, parenthetical, or citation-form item needs correcting. |
| FAIL | Any case or authority not located in any source; any quotation not found in the cited opinion; any holding the opinion does not support. |

PASS is a statement about what this run checked, not a substitute for attorney review.

## Output

```markdown
[WORK-PRODUCT HEADER — per plugin config ## Outputs]

> **⚠️ Reviewer note**
> - **Sources:** [CourtListener ✓ responding | not connected]; [other connectors used]; [web search used for N items]
> - **Read:** [full document incl. footnotes | pages X–Y only — why]
> - **Flagged for your judgment:** [N items marked `[review]`]
> - **Before relying:** [the items that must change before filing, or "ready for your eyes"]

# Cite Check: [Document title]

## Verdict

[PASS | PASS WITH CORRECTIONS | FAIL]. Checked [N] of [M] citations. [A] located; [B] located with corrections; [C] not located; [D] quotations checked, [E] not verbatim; [F] holdings checked, [G] not supported or partially supported; [H] could not be checked.

## Not located

[Each authority not located, with every source searched. Omit if none.]

## Summary table

| Citation as it appears | Location | Status | Source | Correct citation | Note |
|---|---|---|---|---|---|

## Corrections and mischaracterizations

[One subsection per authority needing change. Quote the opinion verbatim with its source link. Give the corrected citation or parenthetical.]

## Could not check

[Pins, star pages, citator status, and anything else not checked, with the reason.]

## Adverse authority

[Only on request.]
```

Status values: Located · Located — correction needed · Quotation not verbatim · Holding not supported · Partial support · Not located · Could not check.

The Source column carries the provenance tag for where the authority was found this session: `[CourtListener]`, `[Westlaw]`, `[web search — court PDF]`, and so on, per the plugin's source-attribution rules. Never tag a citation with a source that did not return it in this session.

## What this skill does not do

- It does not edit the document. Corrections go back to the author.
- It does not determine whether an authority is still good law without a citator connector.
- It does not treat a citation as checked because it appeared in an earlier run, a prior brief, or the verification log.
