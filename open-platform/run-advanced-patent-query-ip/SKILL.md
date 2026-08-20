---
copyright: "Copyright © Patsnap. All rights reserved."
name: run-advanced-patent-query-ip
description: Execute a user-supplied Patsnap advanced patent query containing field operators such as ANCS:, TAC_ALL:, DESC_B:, MAINF:, ALL_AN:, PN:, APD:, PBD:, APNO:, or PRNO:, then generate an evidence-backed competitor patent report with portfolio counts, company-level technical summaries, hierarchical patent details, optional literature context, Markdown output, and an accessible HTML rendering. Use when the user explicitly asks to run a Patsnap query or create a report from one; require verified Patsnap MCP or documented global API access and never collect credentials in chat.
---

# Run an advanced Patsnap query and create a competitor report

## Purpose

Accept a Patsnap professional query and a report title.

Retrieve matching patent records through verified Patsnap global capabilities.

Generate a Markdown report with three sections:

1. Recently published patent overview.
2. Company-level technology summaries.
3. Patent details grouped by technical subarea and applicant.

Render the Markdown as an accessible HTML report.

Optionally incorporate literature context when a verified literature service is configured.

## Trigger rules

Use this skill when the user:

- Supplies a Patsnap query containing field operators.
- Asks to execute or run a Patsnap query.
- Asks to generate a report from an advanced patent query.

Relevant operators include:

- `ANCS:`
- `TAC_ALL:`
- `DESC_B:`
- `MAINF:`
- `ALL_AN:`
- `PN:`
- `APD:[...]`
- `PBD:[...]`
- `APNO:`
- `PRNO:`

Preserve field codes exactly.

Do not silently rewrite the user’s query.

If correction is necessary, show the proposed query and explain the change.

## Inputs

Require:

- Patsnap query.

Accept:

- Report title; default `Patent search report`.
- Maximum result count; default 200.
- Target jurisdictions.
- Date and date-field interpretation.
- Preferred counting unit.
- Report language; default English.
- Whether literature context is required.
- Whether AI synthesis is allowed.

Validate that the result limit is a positive integer.

Record the query, limit, retrieval date, returned count, language, and data cut-off in the report.

## Credential and installation rules

Never ask the user to paste an API key into the conversation.

Never write credentials inside this skill directory.

Never create a bundled `.env` file.

Never search fixed personal directories for shared credentials.

Use the MCP client’s credential mechanism whenever possible.

For an explicitly configured REST workflow, read credentials from the execution environment.

Use `PATSNAP_API_KEY` only for a documented Patsnap global REST endpoint.

Use `PATSNAP_BASE_URL` only when the user or environment supplies a verified endpoint.

Do not default to a legacy China-market connector domain.

Do not silently install Python packages.

Tell the user which dependencies are missing and let the surrounding environment manage installation approval.

## Patsnap MCP mapping

### Required: Advanced Patent Search

Official page: https://open.patsnap.com/marketplace/mcp-servers/patent-search

Verified 2026-08-07.

Configuration key: `advanced_patent_search`.

Transport: `streamableHttp`.

Current Connect-panel URL pattern:

`https://open.patsnap.com/marketplace/mcp-servers/patent-search`

Copy the current URL from the official Connect panel.

Keep the real key secret.

Use documented capabilities such as:

- `search_patents_nested` for controlled structured retrieval.
- `search_patent_count` for total-count context.
- `search_patent_field` for distributions.
- `search_patent_by_pn` for record verification.
- Assignee-specific search for entity checks.
- Semantic, keyword-suggestion, similarity, and image tools only when required by the task.

Translate the Patsnap field query into exact tool arguments only when the connected schema supports it.

Do not invent an MCP argument.

### Recommended: Patent Briefing

Official page: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

Verified 2026-08-07.

Configuration key: `patent_briefing`.

Transport: `streamableHttp`.

Current Connect-panel URL pattern:

`https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`

Use its documented bibliography, legal-status, family, claim, description, translated-text, drawing, and technical-summary capabilities to verify detailed records.

### REST and literature fallback

The bundled clients may run only when exact global endpoints and response schemas are explicitly configured and verified.

They must fail closed when the endpoint is absent.

Do not guess a global endpoint from a legacy Chinese endpoint.

Do not use the source’s China-only ARK/Doubao defaults.

If no verified literature connector or endpoint exists, skip literature retrieval and state that it was not executed.

If AI synthesis is unavailable, preserve retrieved facts and omit synthetic summaries.

## Execution workflow

### Step 1: Validate the request

Confirm the query contains meaningful Patsnap syntax or a clearly stated execution request.

Confirm title and result limit.

Identify confidentiality constraints.

Identify jurisdiction and date ambiguities.

Do not infer a “recent publications” date range unless the query or user defines it.

### Step 2: Validate access

Prefer Advanced Patent Search through the connected MCP client.

If using REST scripts, call the configuration guard before network access.

Do not print credentials.

Run a minimal non-destructive capability check where available.

If access fails, return the exact failure and a configuration checklist.

### Step 3: Execute the query

Retrieve up to the selected limit.

Handle pagination explicitly.

Record total available hits separately from returned records when supported.

Record sort order and result cap.

Preserve raw identifiers needed for verification.

Do not fabricate missing fields.

### Step 4: Normalize records

Normalize publication numbers, applicants, dates, jurisdiction codes, legal status, abstract, claims, problem, solution, benefit, and image references.

Distinguish original applicant from current assignee.

Distinguish publication, application, priority, and grant dates.

Mark unavailable or unverified data explicitly.

### Step 5: Build the overview

Show query metadata and coverage.

Provide applicant or company counts under a stated counting unit.

Explain whether the result set is complete or capped.

Do not imply that a result count equals a unique patent family count.

### Step 6: Build company technology summaries

Summarize each company’s observed technical focus and technical approaches.

Link every material synthesis to retrieved records.

Separate retrieved facts from AI interpretation.

Do not generate a summary when evidence is too sparse.

### Step 7: Build detailed patent sections

Group records by:

1. Technical subarea.
2. Applicant or company.
3. Patent record.

For each patent show:

- Title.
- Publication number with a verified Patsnap or official link.
- Legal status and status date when available.
- Applicant and current assignee when available.
- Application date.
- Technical problem.
- Technical approach.
- Technical benefit.
- Abstract drawing with source and alt text when available.
- Evidence or retrieval note.

Do not embed an image from an untrusted scheme or path.

### Step 8: Add literature context when requested

Use a verified literature endpoint or connector.

Record search query, filters, result count, and retrieval date.

Keep patent and literature evidence separately labeled.

Do not use an undisclosed external AI service.

### Step 9: Generate Markdown and HTML

The shell entry point is:

```bash
bash scripts/run.sh "<query>" "<report title>" [limit]
```

Run it from the skill directory or allow it to resolve its own location.

The script writes Markdown under `reports/` and prints it to standard output.

It then calls `scripts/render_html.py` to create a matching HTML report.

The runner must not install dependencies silently.

The title must be passed as an argument, never interpolated into executable Python source.

Use a UTC timestamp and an ASCII-safe filename.

## Report display contract

After successful execution, display in the conversation:

- The complete first section: recently published patent overview.
- The complete second section: company technology summaries.

Do not paste the entire third section into the conversation when it is long.

Link the saved Markdown and HTML reports for full patent details.

State the actual paths.

## Scientific visual standard

Use semantic HTML with `lang="en"`.

Use a white background, charcoal text, restrained blue accent, and neutral borders.

Use an English system-font stack.

Use sentence-case headings.

Use accessible disclosure controls for hierarchical detail.

Use captions, units, cut-off dates, counting units, and source notes.

Use responsive tables and images.

Add print CSS.

Do not use gradients, oversized cards, decorative pills, emoji, or color-only status signals.

Escape all Markdown-derived content before injecting it into HTML.

Allow only safe link and image schemes.

## Example fixture

The `reports/report_20260416_152606.md` and `.html` files are historical report fixtures carried from the source package.

Treat their dates and findings as example data, not current intelligence.

The referenced PNG is an English-labeled patent drawing.

Preserve the binary image and add descriptive context in the localized example reports.

Do not reuse fixture facts in a live report.

## Dependencies

The Python retrieval scripts use `requests`.

Only use optional dependencies when the corresponding code path is explicitly enabled.

Do not declare or install unused `oss2`, `python-dotenv`, or China-only AI dependencies.

## Failure rules

If MCP access is missing, provide a connection checklist and do not run a synthetic search.

If REST configuration is missing, fail before making a request.

If authentication fails, do not retry with altered credentials.

If a response schema is unexpected, preserve a safe diagnostic and stop.

If pagination fails, label the report partial.

If literature retrieval fails, keep the patent report and label literature unavailable.

If an image cannot be retrieved or validated, omit it and preserve alt text or a note.

If HTML rendering fails, retain and link the Markdown report.

## Validation checklist

- Query preserved or changes disclosed.
- Limit is positive and recorded.
- No credential appears in chat, files, logs, or report output.
- No legacy Zhihuiya domain remains.
- No fixed personal directory remains.
- No silent dependency installation remains.
- Patsnap MCP names and URLs match official global pages.
- REST execution fails closed without verified settings.
- Every count has a counting unit and cap context.
- Patent identifiers and links are verified.
- Legal status has a source date or is marked unverified.
- AI synthesis is distinguished from retrieved evidence.
- Markdown content is safely rendered.
- HTML is accessible, responsive, and print-safe.
- Example fixtures are labeled historical.
- Output paths exist before being reported.

## Final response

Lead with whether execution succeeded, failed, or was downgraded to a search plan.

State the query, returned count, total count if known, cap, counting unit, and cut-off.

Show the complete first and second report sections.

Link the Markdown and HTML files.

State any partial-data, schema, literature, or rendering limitation.
