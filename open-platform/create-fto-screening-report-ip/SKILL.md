---
copyright: "Copyright © Patsnap. All rights reserved."
name: create-fto-screening-report-ip
description: Create a traceable, screening-level freedom-to-operate report from a supplied risk-point Word document and user-approved Patsnap search expressions. Use when a patent analyst, IP team, product counsel, or R&D owner needs structured feature extraction, Patsnap patent retrieval, claim-data collection, claim-limitation comparison, candidate risk triage, HTML/DOCX reporting, and evidence JSON. Supports a bundled global Patsnap REST workflow or normalized evidence from verified Patsnap MCP connectors. The output is an FTO screening, not a legal clearance opinion.
---

# Create an FTO Screening Report

Version: 2.0 localized international edition

## Purpose

Convert:

1. a supplied risk-point `.docx` describing a target product, process, or
   technical implementation; and
2. one or more user-approved Patsnap search expressions

into a reproducible FTO screening package containing search provenance,
normalized candidate patents, retrieved claims, structured claim-limitation
comparisons, risk-triage lists, limitations, recommendations, and English HTML
and DOCX reports.

The source workflow uses P070, P002, P018, and optional AI07/AI66 capabilities.
The international edition preserves those functions while using the global
Patsnap base URL, current Bearer authentication, evidence-safe terminology,
and verified MCP alternatives.

## Legal and analytical boundary

This skill produces a screening, not a legal opinion or guarantee of freedom
to operate.

It does not:

- establish that every relevant patent has been found;
- infer enforceability from a simple legal-status filter;
- treat a pending application as a currently enforceable patent claim;
- determine infringement from a title, abstract, classification, semantic
  score, or AI output;
- assume one jurisdiction's doctrine of equivalents applies globally;
- conclude that a patent is invalid from automated prior-art or status data;
- replace review of all material independent/dependent claims, prosecution,
  family members, product evidence, relevant acts, and applicable law;
- replace qualified local counsel for a decision-material legal opinion.

## Trigger boundary

Use this skill when the user provides or identifies:

- an FTO risk-point or technical-feature Word document;
- a specific product/process/implementation and version;
- target jurisdiction(s) and commercial acts; and
- one or more Patsnap search expressions or authorization to prepare expressions
  for review before execution.

Appropriate use cases include:

- pre-launch invention-patent screening;
- design-freeze risk triage;
- export/import planning;
- technical-route risk review;
- due-diligence support;
- trade-show or bid preparation;
- recurring pending-claim monitoring.

Do not use this as a complete legal FTO opinion workflow. Do not use it for
design-patent image comparison without an appropriate design-FTO capability.

## Required source materials

### Risk-point Word document

Parse body paragraphs, tables, headings, headers/footers, text boxes, and
embedded figure captions where relevant. Do not rely on `Document.paragraphs`
alone.

Extract:

- project and product/process name;
- controlled product/process version;
- technical feature groups;
- essential and optional features;
- versioned product/process evidence references;
- intended jurisdictions and relevant acts;
- search/status cutoffs and decision deadline;
- family/counting convention;
- known competitors, assignees, patents, standards, or classifications;
- assumptions, exclusions, confidentiality, and distribution limits.

### Search expressions

Accept:

- a JSON file containing expressions and provenance;
- repeated command-line query arguments; or
- expressions prepared during the session and explicitly reviewed before use.

Preserve each expression exactly. Never silently add or remove a jurisdiction,
company, classification, legal-status, date, language, or family filter.

### Missing information

If any required field is unavailable:

1. record the gap;
2. state the effect on search or claim comparison;
3. request evidence when it materially changes the work;
4. continue only where the remaining work is meaningful;
5. label affected sections `Partial` or `Not assessed`;
6. never reuse facts from the source slide-rail example or a prior run.

## Data-access modes

Select one primary mode per run. Read
`references/api_call_policy.md` before accessing external data.

### Mode A — Bundled Patsnap REST workflow

Use the scripts in this package with:

```text
https://connect.patsnap.com
Authorization: Bearer <private API key>
```

The source filenames `scripts/zhihuiya_api.py` and
`references/zhihuiya_config.json` are retained solely for exact source
topology. Their localized content uses Patsnap global naming and services.

Supported endpoint roles:

| ID | Path | Role |
|---|---|---|
| P070 | `/search/patent/keyword-suggest` | Optional reviewed terminology expansion |
| P002 | `/search/patent/query-search-patent/v2` | User-expression patent retrieval |
| P018 | `/basic-patent-data/claim-data` | Claim retrieval; required path |
| AI07 | `/chat/cc-gpt-stream` | Optional supporting feature comparison |
| AI66 | Current verified `/ai/fto/...` endpoints only | Optional Patsnap FTO task/report workflow |

Never use `/basic-patent-data/claims`. Never send the API key in a URL, log,
report, exception, or output JSON.

### Mode B — Patsnap MCP-assisted evidence

Use only installed/configured connectors and their current schemas.

| Connector | Identifier / endpoint | Role |
|---|---|---|
| Patsnap Patent Research | `patsnap_patent_research` · `https://open.patsnap.com/marketplace/mcp-servers/patsnap-ip-searching` | End-to-end invention FTO submission and retrieval through `fto_review` and `get_task` |
| Advanced Patent Search | `advanced_patent_search` · `https://open.patsnap.com/marketplace/mcp-servers/patent-search` | Query, semantic, classification, assignee, similar-patent, and filtered retrieval |
| Patent Briefing | `patent_briefing` · `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing` | Claims, translated claims, description, bibliography, family, status, images, and technical summary |
| Global Core Patents | [Marketplace page](https://open.patsnap.com/marketplace/mcp-servers/core-patents) | Optional detailed legal events, status, family, PDF, reexamination, licensing, and citations |

Catalogue:
[Patsnap MCP Servers](https://open.patsnap.com/marketplace/mcp-servers).

For each call, retain connector, tool, request, filters, execution date, task
ID, returned identifiers, and limitations. Normalize results into the package's
schemas before report generation. Do not imply that the Python script itself
called an MCP server.

### Mode transition

Do not repeat quota-consuming work unnecessarily. If switching modes:

- state why;
- preserve both provenance chains;
- identify overlapping and non-overlapping result sets;
- do not merge incompatible identifiers or status dates silently.

## Search-expression rules

1. Use each user-approved expression directly.
2. Keep expression ID, source, reviewer, fields, filters, and date run.
3. Keep Patsnap syntax intact; do not “simplify” parentheses or field scoping.
4. Do not hard-code China, `CN`, a fixed company, fixed IPC, or
   `SIMPLE_LEGAL_STATUS:1`.
5. Use P070 suggestions only after technical review.
6. Record generated queries separately from user-provided queries.
7. Preserve raw, paginated, retained, duplicate, and family counts.
8. Preserve every matching query ID after deduplication.
9. State truncation when `max_total` or `max_candidates` is reached.
10. Treat empty and failed queries differently.

## Required workflow

### Step 1 — Parse and validate the risk document

1. inventory the supplied document and related files;
2. extract all semantic slots described in
   `references/report_requirements.md`;
3. normalize whitespace without altering technical meaning;
4. retain tables and feature relationships;
5. preserve figure/caption references to product evidence;
6. identify missing scope fields;
7. create a controlled run data object;
8. stop before external transmission if authorization is absent.

The sole source DOCX under `assets/` is a localized generic report
template. Do not copy its placeholders into factual findings.

### Step 2 — Retain comparison features

For each feature assign:

- stable feature ID;
- feature group;
- essential/optional status;
- normalized technical wording;
- product evidence reference, version, and date;
- source document location;
- ambiguity or missing facts;
- reviewer status.

Do not reduce the product to keyword fragments when the claim comparison
depends on relationships, order, function, composition, range, location, actor,
or process steps.

### Step 3 — Register and review queries

Create `queries.json` containing:

- schema version;
- project/run ID;
- query ID and exact expression;
- user-provided or generated origin;
- approval/reviewer state;
- intended route and purpose;
- fields, filters, language, and stemming;
- date run and result counts;
- error/partial state.

Dry-run mode may write the approved query register but must not call Patsnap.

### Step 4 — Execute P002 or equivalent connector search

For each approved expression:

1. call P002 through the bundled client or the selected MCP search tool;
2. paginate within current service limits;
3. validate HTTP/tool and business status;
4. normalize each record;
5. merge candidates without losing matching query IDs;
6. preserve raw evidence references;
7. stop safely on repeated pages or malformed data;
8. write `patent_list.json` with complete provenance.

Deduplicate by publication number, Patsnap ID, application number, or a
documented fallback. Never deduplicate by title alone.

### Step 5 — Retrieve claims through P018 or Patent Briefing

For every selected candidate:

1. identify the target-jurisdiction member;
2. retrieve claim data using P018 `/basic-patent-data/claim-data` or a verified
   claim tool;
3. select the correct language/version;
4. extract Claim 1 as the source minimum;
5. identify other material independent and dependent claims;
6. preserve raw claim evidence and parse status;
7. disclose related-family replacement;
8. record retrieval/status dates and translation basis.

If Claim 1 cannot be retrieved, mark the comparison `Not assessed`. Do not
substitute the abstract or description as claim text.

### Step 6 — Build the structured claim chart

Follow `references/claim_chart_schema.md`.

For each material limitation record:

- claim number and limitation ID;
- source-faithful limitation text;
- product/process feature and evidence;
- literal mapping and rationale;
- jurisdiction-specific equivalents assessment when appropriate;
- contrary evidence;
- missing facts;
- confidence;
- source and reviewer.

Keep literal mapping and equivalents separate. A `Y/N` comparison is
insufficient for uncertain or legally qualified facts.

### Step 7 — Optional AI07 supporting analysis

When authorized and useful:

1. construct a prompt that labels claim text and product evidence separately;
2. request limitation-level analysis, uncertainty, contrary evidence, and
   missing facts;
3. avoid asking for an absolute legal conclusion;
4. preserve raw output and parsed output;
5. compare it with the structured chart;
6. retain all conflicts;
7. require human disposition.

AI07 never overrides P018 claim text, product evidence, official status, or
qualified review.

### Step 8 — Optional AI66 workflow

Read `references/api_reference.md` before use. Enable only endpoint stages whose
current global contracts have been verified.

The source's undocumented `cc_pids` injection is prohibited. Do not send guessed
fields or claim that AI66 was constrained to the P002 list unless the current
official API explicitly supports and confirms it.

If the AI66 contract is unavailable, continue with P002/P018 structured
comparison or an approved MCP FTO workflow. Record the unavailable step.

### Step 9 — Triage screening concern

Use text labels:

- `Higher screening concern`;
- `Moderate screening concern`;
- `Lower screening concern`;
- `Pending watchlist`;
- `Not assessed`.

Base labels on current claim mapping, status evidence, jurisdiction, relevant
act, product version, confidence, and missing facts. They are not probabilities
of infringement.

### Step 10 — Generate the evidence package and reports

Write to the selected output directory:

- `queries.json`;
- `patent_list.json`;
- `claim_chart.json`;
- `fto_structured_data.json`;
- `fto-screening-report.html`;
- `fto-screening-report.docx`.

The source scripts may also retain a sanitized run manifest/error register.
Never write run artifacts into the skill package.

Use `scripts/run_generic_fto_report.py` for orchestration and
`scripts/render_report.py` for structured HTML rendering. The runner may create
DOCX directly while using the localized asset as its content/style reference.

## Report requirements

Both report formats must include:

1. cover and document control;
2. executive screening summary;
3. purpose, subject, controlled version, acts, jurisdictions, and decision;
4. scope, assumptions, exclusions, cutoffs, and family convention;
5. technical-feature and product-evidence inventory;
6. acquisition mode and query/search methodology;
7. candidate and family overview;
8. higher, moderate, lower, pending, and not-assessed lists;
9. limitation-level comparison for material candidates;
10. status, owner, family, claim-version, and translation notes;
11. unresolved evidence and search limitations;
12. prioritized actions, owners, timing, and re-review triggers;
13. source/provenance register;
14. screening boundary and legal disclaimer.

## HTML standard

The HTML report must:

- declare `lang="en"`;
- escape every dynamic value;
- permit only safe HTTP(S) evidence links;
- use a restrained white/navy/charcoal scientific/legal aesthetic;
- use text labels in addition to color;
- use semantic headings, tables, captions, and source notes;
- remain readable at desktop and mobile widths;
- constrain wide-table scrolling locally;
- include print styles;
- contain no client-side scripts unless a source-required, reviewed interaction
  cannot be represented safely as static HTML;
- contain no real key, local path, China-domain link, or personal metadata.

## DOCX standard

The localized DOCX asset remains at the exact source path
the sole DOCX under `assets/`. Its source filename is retained for topology fidelity.

Use:

- US Letter portrait and explicit margins;
- professional Western scientific/legal typography;
- real Title/Heading styles and coherent hierarchy;
- explicit table geometry and repeating headers;
- accessible table header cells and text risk labels;
- restrained navy/charcoal accents;
- cover, document-control block, running footer, and page numbering;
- no floating legacy decorative shapes;
- no broken local hyperlinks or personal metadata;
- no fixed slide-rail, Chinese company, patent, date-range, or conclusion facts;
- placeholders that remain visibly placeholders until factual data is supplied.

The DOCX must be structurally audited and rendered/visually inspected with the
document workflow when LibreOffice is available. If `soffice` is unavailable,
record that limitation and do not claim the render gate passed.

## Commands

### Dry run

```bash
python scripts/run_generic_fto_report.py \
  --input risk_points.docx \
  --queries queries.json \
  --output-dir output \
  --dry-run
```

Dry-run may parse local input and write a run plan. It must not make network
calls or imply retrieved patent results.

### REST execution

```bash
python scripts/run_generic_fto_report.py \
  --input risk_points.docx \
  --queries queries.json \
  --api-config references/zhihuiya_config.json \
  --business-config references/config.json \
  --output-dir output
```

Use `--help` for the authoritative localized CLI.

### Render an existing structured dataset

```bash
python scripts/render_report.py \
  fto_structured_data.json \
  fto-screening-report.html
```

## Failure behavior

### Missing API configuration

- Stop REST execution before any request.
- Identify the private configuration file.
- Do not print the key or configuration object.
- Offer dry-run or authorized MCP mode.

### Authentication/entitlement failure

- Stop the affected step.
- Preserve successful prior evidence.
- Record HTTP/business code without credentials.
- Do not convert the failure into an empty patent set.

### Partial pagination

- retain successful pages;
- record missing offset/page and error;
- mark search partial;
- show truncation in the report.

### Missing/ambiguous claims

- mark claim comparison not assessed;
- identify the patent/member/language requested;
- record whether related-family replacement occurred;
- do not use abstract/description as claim text.

### AI failure or conflict

- preserve raw/parsed state available;
- continue with structured primary evidence;
- retain the conflict for human review;
- never fabricate an AI conclusion.

### Report generation failure

- preserve JSON evidence;
- identify the failed output and sanitized error;
- do not state delivery is complete;
- rerun only after validating input schema and output path.

## Quality-control checklist

Before delivery confirm:

- all 12 source-package paths remain present and no target-only file was added;
- input subject, version, jurisdictions, acts, cutoffs, and decision are clear;
- every search expression and generated term is attributable;
- mode and provider provenance are complete;
- REST key is absent from logs/outputs;
- P002 counts/pagination/deduplication reconcile;
- P018 uses `claim-data`;
- claim source, language, version, replacement, and retrieval date are visible;
- every material limitation maps to versioned product evidence or a gap;
- literal and equivalents assessments are separate;
- all material independent/unreviewed claims are identified;
- status filters are not described as enforceability proof;
- pending applications are in a watchlist;
- AI conflicts are visible and human disposition is recorded;
- higher/moderate/lower labels have written bases and confidence;
- reports contain all required sections and legal boundary;
- dynamic HTML is escaped and links are safe;
- DOCX has no Chinese fixed-case content, broken local links, or personal metadata;
- no Chinese-market domain, secret, or unintended local path remains;
- generated artifacts are outside the package;
- qualified local counsel review is required for material reliance.

## Package resources

- `README.md` — global setup and connectivity;
- `references/api_call_policy.md` — REST/MCP mode and security controls;
- `references/api_reference.md` — global Patsnap REST contracts;
- `references/claim_chart_schema.md` — evidence and comparison JSON schema;
- `references/report_requirements.md` — input/output and legal requirements;
- `references/config.json` — jurisdiction-neutral business defaults;
- `references/zhihuiya_config.json` — source-preserved private global API config;
- `scripts/zhihuiya_api.py` — source-preserved global Patsnap REST client;
- `scripts/run_generic_fto_report.py` — complete workflow orchestrator;
- `scripts/render_report.py` — safe English HTML renderer;
- the sole DOCX under `assets/` — localized generic English report template; source filename retained.

Marketplace reference:
[FTO Screening Report](https://open.patsnap.com/marketplace/skill-hub/generic-fto-report).

## Disclaimer

Patent search, claim, family, ownership, and legal-status data can be incomplete,
delayed, mistranslated, or changed. Unpublished applications cannot be observed.
The output is limited to the defined product/process, version, activity,
jurisdiction, claims, evidence, source coverage, and dates. It is an FTO
screening and does not constitute legal advice or guarantee freedom to operate.
