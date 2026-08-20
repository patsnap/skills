---
copyright: "Copyright © Patsnap. All rights reserved."
name: assess-high-value-patent-portfolio-ip
description: Rank a user-defined Patsnap patent candidate universe with an auditable 30/30/20/20 model based on simple-family forward citations, simple-family size, core-inventor concentration, and verified legal-event activity; select a documented 10–15% screening portfolio and generate traceable English HTML, JSON, and optional Word outputs. Use for evidence-based patent portfolio triage, high-value patent screening, candidate prioritization, or portfolio-review preparation—not monetary valuation, validity, enforceability, or investment conclusions.
---

# Assess a High-Value Patent Portfolio

## Overview

Use this skill to turn one reviewed Patsnap patent query into a transparent,
reproducible portfolio-screening package. Retrieve the full agreed candidate
universe, enrich every candidate for scoring, apply the source 30/30/20/20
model, select a documented 10–15%, and preserve all evidence and failures.

The term **high-value** describes relative selection under this model. It does
not mean monetary value, commercial success, technical quality, validity,
enforceability, freedom to operate, essentiality, or investment merit.

Never fabricate a patent record, citation, family member, inventor identity,
legal event, legal status, drawing, technical summary, score, source link, or
missing API result. An endpoint failure stays `error`; a missing field stays
`missing`; neither becomes factual zero.

## When to use

Use this skill when the user asks to:

- identify a high-value subset within a patent search result;
- rank a portfolio or technology-specific candidate universe;
- create a traceable patent-prioritization list;
- apply the explicit citation/family/inventor/event model;
- compare screening signals across patents in one scoped run; or
- prepare a portfolio review for an analyst, IP team, R&D leader, or counsel.

Do not use it as the sole method for:

- patent valuation or pricing;
- validity, infringement, enforceability, or FTO opinions;
- standards-essentiality or claim-chart determinations;
- acquisition or investment recommendations; or
- comparisons between independently scoped query results.

## Required inputs

Obtain or explicitly mark missing:

1. The exact, human-reviewed Patsnap query.
2. The legal entities, technologies, products, and exclusions represented by
   the query.
3. Target jurisdictions or authorities.
4. Search and legal-status cutoff dates.
5. Date range and publication/application/grant treatment.
6. Family definition and representative-publication rule.
7. Screening purpose and intended audience.
8. Candidate cap, if any, and whether truncation is acceptable.
9. Selection ratio between 10% and 15%; default 10%.
10. Any reviewed core-inventor override.
11. Any user-approved weight change. If changed, do not describe the result as
    the default source model.
12. Required report language; default English.

Do not silently broaden, narrow, translate, repair, or reformulate the query.
If a generated query is proposed, require human approval before execution and
record both the draft and approved query.

## Required deliverables

Always produce:

- `high_value_patent_portfolio_screening.html` — safe static English report;
- `high_value_patent_screening_data.json` — all scored candidates plus selected
  records and evidence trace;
- `final_records.json` — selected report-ready records;
- restartable stage checkpoints described below.

Produce only when the user requests Word:

- `high_value_patent_portfolio_screening.docx` — same substantive selection,
  scores, rationales, evidence states, limitations, and sign-off controls.

The HTML is the required report. The JSON trace is required evidence, not an
optional developer artifact. Word is optional.

## Report contents

The report must include:

- reviewed query and query hash;
- run ID, source mode, generated time, and schema version;
- P002-reported total, retrieved count, deduplicated count, scored count,
  selected count, and final percentage;
- candidate cap and truncation state;
- scoring model, version, weights, and overrides;
- family and cutoff conventions;
- top five exact-returned inventor names and counts;
- selected patent table with all required fields;
- one evidence-bounded rationale per selected patent;
- endpoint/connector errors and selected-record data gaps;
- legal-event interpretation boundary;
- model limitations and required human review; and
- reviewer sign-off fields in Word output.

## Required selected-patent fields

For each selected patent preserve:

| Field | Required treatment |
|---|---|
| `rank` | Deterministic position after total score and all tie-breaks |
| `score` | 0–100 total plus four component scores |
| `rationale` | Compact source-bounded explanation including missingness |
| `pn` | Publication number from P002 when available |
| `patent_id` | Internal identifier retained in JSON evidence, not exposed as a secret |
| `record_url` | Render only a verified stable global HTTP(S) URL; otherwise plain identifier |
| `title` | Original P002 title, preserving language when returned |
| `drawing` | P021 URL or explicit state; expiring URLs are not durable evidence |
| `current_assignee` | Current assignee/patentee field and source cutoff where available |
| `legal_status` | Raw P041 simple status plus state and checked-as-of date |
| `patsnap_title` | P025 English title, if returned |
| `tech_problem` | P025 English technical-problem summary |
| `tech_approach` | P025 English technical-approach summary |
| `benefit` | P025 English benefit/effect summary |
| `cited_by_simple_family` | P015 value, state, candidate percentile, and scoring method |
| `simple_family_count` | P014 value, state, candidate percentile, and family rule |
| `core_inventor` | Boolean plus exact matched names |
| `legal_event_evidence` | Per-category state, event count, and event records |
| `gaps` | Missing/error/not-run evidence and remediation |
| provenance | Endpoint or connector/tool, retrieval time, request evidence, run ID |

Do not describe P041 simple legal status as proof of enforceability. Do not use
title, abstract, drawing, family size, citation count, or AI summary as a proxy
for claim scope.

## Default scoring standard

Read `references/screening-standard.md` before executing or modifying the
model. The default 100 points are:

| Indicator | Weight | Evidence |
|---|---:|---|
| Simple-family forward-citation position | 30 | P015 `patent_cited.cited_by_simple_family` |
| Simple-family size position | 30 | P014 `patent_family.simple_family` length |
| Core-inventor membership | 20 | Exact inventor names in the P002 candidate universe |
| Verified legal-event activity | 20 | P034/P027/P028/P029 event arrays |

Scores are candidate-universe relative. They are not calibrated estimates of
currency, probability, commercial importance, validity, or litigation risk.

### Numeric evidence

For at least ten candidates, calculate the empirical percentile using available
numeric observations only:

```text
percentile(value) = count(available values <= value) / count(available values)
component_score = percentile(value) * 30
```

For fewer than ten candidates:

- all available values zero: score zero;
- all non-zero values equal: a non-zero record receives 15;
- mixed available values: use the empirical percentile and label it unstable;
- missing/error/not-run: score zero under the default missing-data policy while
  preserving the non-zero evidence state.

Always report available and missing counts. A numeric zero returned by an
endpoint is different from no returned evidence.

### Core inventors

1. Split inventor records on `|`, semicolon, full-width semicolon, and line
   breaks.
2. Never split on comma or full-width comma. Patsnap commonly returns
   `LASTNAME, FIRSTNAME|LASTNAME, FIRSTNAME`; the comma is inside one name.
3. Normalize whitespace only and count a name once per patent.
4. Rank exact-returned names by candidate patent count descending, then name
   ascending.
5. Treat the first five as core inventors.
6. Score 20 when a patent contains at least one exact match; otherwise zero.

Do not automatically merge initials, spelling variants, transliterations,
maiden names, reordered names, or homonyms. Record a user override and its
provenance. Do not use final patent scores to define the inventors who
contribute to those scores; that is circular.

### Legal-event activity

Qualifying source categories:

- Litigation — P034 `patent_litigation_data`;
- Reexamination or invalidation — P027 `patent_reexam_invalid_data`;
- License — P028 `patent_license_data`;
- Transfer — P029 `patent_transfer_data`.

Score 20 if at least one verified event record exists in any category. Score
zero if all four checks succeeded and returned empty. If any required check is
missing, failed, or not run, retain the zero-point policy but state that absence
cannot be concluded.

An event is not inherently valuable. Litigation and invalidation may be
adverse; a license may be expired or intra-group; a transfer may be a security
interest or corporate restructuring. Preserve dates, case/proceeding numbers,
parties, country/authority, event type, and source locator when returned.

## Selection count

Default:

```text
selected_count = ceil(deduplicated_candidate_count * 0.10)
maximum_count = ceil(deduplicated_candidate_count * 0.15)
```

Rules:

- zero candidates yields zero selections and a valid no-results report;
- any non-zero candidate universe yields at least one selected record;
- never exceed 15% without a recorded user instruction;
- resolve cutoff ties using deterministic tie-breaks, not by including every
  tied record; and
- state both the selected count and percentage.

Tie-break order:

1. higher available simple-family forward-citation count;
2. higher available simple-family size;
3. verified legal-event hit;
4. core-inventor hit;
5. more verified event categories;
6. earlier valid application date;
7. publication number ascending;
8. stable internal identifier ascending.

Missing values rank below available values, including factual zero.

## Complete eight-stage workflow

The source package contains ten Python files and eight stages. Preserve all of
them; do not collapse away checkpoints or evidence.

### Stage 0 — Define scope and run controls

- Confirm the reviewed query and contextual scope.
- Select REST or MCP-import source mode.
- Generate one run ID shared by every checkpoint.
- Set a documented maximum record count.
- Confirm selection ratio and overrides.
- Never place a credential in query text, arguments, logs, outputs, or reports.

### Stage 1 — Retrieve P002 candidates

Use P002 `/search/patent/query-search-patent/v2`.

- Send the exact approved `query_text`.
- Page with bounded `limit` and `offset`.
- Retain reported total and per-page request evidence.
- Detect repeated page signatures and stop with an error.
- Record truncation when the agreed maximum is reached.
- Normalize identifiers, title, assignee, inventor, dates, and authority.
- Deduplicate by `patent_id`, then publication number fallback.
- Preserve duplicate decisions.
- Output `cand_raw.json`.

An empty result is a valid state only after a successful call. A request failure
is not a no-results conclusion.

### Stage 2 — Enrich every candidate with numeric evidence

For all deduplicated candidates:

- P014 `/basic-patent-data/patent-family` for simple-family members;
- P015 `/basic-patent-data/forward-citation/v3` for
  `cited_by_simple_family` and available detail fields.

Batch within documented endpoint limits. Preserve `available`, `empty`,
`missing`, `error`, or `not_run`, along with request evidence and errors. Output
`enrich_num.json`.

### Stage 3 — Enrich every candidate with legal events

For every candidate retrieve:

- P034 `/high-value-data/litigation`;
- P027 `/advanced-patent-data/re-examination-and-invalidation`;
- P028 `/advanced-patent-data/license-data`;
- P029 `/advanced-patent-data/transfer-data`.

Retain complete returned event arrays, normalized English category, state,
count, request evidence, and error. Output `enrich_legal.json`.

### Stage 4 — Calculate and rank

- Compute top-five exact-name inventors or apply a reviewed override.
- Build numeric vectors from available values only.
- Apply the documented numeric fallbacks.
- Calculate all four components and total.
- Record missing-policy points separately from raw evidence state.
- Apply all deterministic tie-breaks.
- Select the approved 10–15%.
- Output `scored.json` with all candidates, not only selections.

### Stage 5 — Enrich selected records for display

For selected patents only:

- P021 `/basic-patent-data/abstract-image`;
- P025 `/high-value-data/tech-problem-and-benefit-summary` with `lang=en`;
- P041 `/basic-patent-data/simple-legal-status`.

P021 links may expire. Store their state and text alternative; download only for
an explicitly requested Word report, allow HTTP(S) only, reject redirects, cap
bytes, require an image content type, and handle expiration safely. Output
`enrich_display.json`.

### Stage 6 — Assemble records and trace

Join `scored.json`, `enrich_display.json`, and `cand_raw.json` by run ID and
patent identifier.

- Reject mismatched run IDs.
- Generate evidence-bounded English rationales.
- Preserve all component scores and states.
- Retain event-level evidence and errors.
- Do not build an undocumented China or global product deep link.
- Render a publication hyperlink only when a verified stable global URL is
  supplied.
- Output `final_records.json` and
  `high_value_patent_screening_data.json`.

### Stage 7 — Generate required HTML

Use `scripts/hv_7_html_a.py`.

- Escape every dynamic value.
- Permit only absolute HTTP(S) URLs.
- Use `rel="noopener noreferrer"` for external links.
- Include no scripts or event handlers.
- Use semantic headings, tables, captions, text states, local table overflow,
  responsive breakpoints, reduced-motion support, and Letter landscape print
  rules.
- Avoid gradients, glow, decorative badges, emoji, and color-only meaning.
- Include all methodology, gaps, limitations, provenance, and reviewer gates.

### Stage 8 — Generate optional Word

Use `scripts/hv_8_word.py` only when requested.

- Keep selection, scores, rationales, evidence states, and limitations aligned
  with HTML/JSON.
- Use US-Letter landscape, Arial, restrained navy/teal/charcoal, real styles,
  repeating table headers, page numbers, fixed margins, and text labels.
- Use safe HTTP(S) hyperlinks only.
- Keep image download off by default.
- Include sign-off controls and metadata without personal paths.

## REST authentication and call policy

Global base URL:

```text
https://connect.patsnap.com
```

Authentication:

```http
Authorization: Bearer <private-api-key>
```

Use `PATSNAP_API_KEY` or an explicitly configured
`PATSNAP_API_KEY_FILE`. Do not accept a default working-directory key file.
Require HTTPS, reject redirects, bound connect/read timeouts, retry only
transient HTTP states and network exceptions, honor bounded `Retry-After`, and
return structured safe errors. Never persist credentials or response bodies in
exceptions.

The source filenames and P-number labels are retained for topology and workflow
fidelity. Verify current global endpoint contracts before a live run.

## Verified Patsnap MCP mapping

MCP is optional and available only in an MCP-capable host. The reference Python
pipeline executes REST; it must never claim it directly called MCP.

| Service | Role | Verified configuration |
|---|---|---|
| Advanced Patent Search | Recommended for candidate query, semantic, classification, assignee, similar-patent, and filtered retrieval | key `advanced_patent_search`; Official marketplace page `https://open.patsnap.com/marketplace/mcp-servers/patent-search`; https://open.patsnap.com/marketplace/mcp-servers/patent-search |
| Patent Briefing | Recommended for representative bibliography, family, claims, descriptions, translations, images, status, and technical summary | key `patent_briefing`; Official marketplace page `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`; https://open.patsnap.com/marketplace/mcp-servers/patent-briefing |
| Global Core Patents | Recommended for detailed citation, family, legal-event, licensing, reexamination/invalidation, litigation, and related core data | https://open.patsnap.com/marketplace/mcp-servers/core-patents |

For MCP-import evidence, record connector key, tool name, normalized request,
retrieval time, record identifiers, and source response locator. Do not mix REST
and MCP-import provenance within one retrieval record. Normalize imported data
to the same checkpoint states and retain raw evidence outside the report where
the execution environment permits.

## Checkpoint contract

Every checkpoint must contain:

- `schema_version`;
- `stage`;
- `run_id`;
- `generated_at` with timezone;
- `source_mode`;
- query hash when applicable;
- upstream checkpoint SHA-256 when applicable;
- candidate or selected count;
- structured records;
- request/connector evidence; and
- structured errors.

Consumers must reject incompatible schema versions, missing required fields,
and mismatched run IDs. Keep the complete chain with the final report.

## Failure handling

| Condition | Required behavior |
|---|---|
| Missing credential | Stop REST retrieval with safe setup guidance |
| Missing reviewed query | Stop before network calls |
| P002 failure | Stop; do not report zero candidates |
| P002 successful empty result | Generate a zero-selection report and trace |
| Candidate cap reached | Mark the universe truncated; do not describe it as complete |
| Repeated page | Stop pagination and record an error |
| P014/P015 failure | Retain affected candidates, zero points under policy, explicit error state |
| Legal endpoint failure | Retain affected candidates; do not conclude absence |
| P025/P041 missing | Keep selected patent and explicit display gap |
| Expired/unsafe drawing URL | Do not embed; show state and text alternative |
| Checkpoint run mismatch | Reject assembly |
| Report link not verified | Render identifier as plain text |
| No Word dependency | HTML/JSON remain valid; explain optional Word requirement |

## Quality gates

Before delivery verify:

- exact source file topology is preserved;
- all source stages, endpoints, metrics, fields, checkpoints, outputs, and
  optional Word behavior remain represented;
- P002 totals reconcile with retrieved, deduplicated, scored, and selected
  counts;
- selected count is within the approved 10–15% rule;
- available zeros are distinguishable from missing/error/not-run;
- every selected patent traces through all checkpoints;
- inventor commas are not fragmented;
- no automatic cross-language identity merge occurs;
- all four legal-event categories retain event-level evidence;
- event activity is not presented as inherently positive;
- citation and family limitations are visible;
- technical summaries are English and clearly sourced;
- publication links are verified global HTTP(S) or plain text;
- HTML has no unescaped dynamic markup, script, handler, unsafe URL, or
  color-only meaning;
- Word contains no personal metadata, local link, floating decorative object,
  or China-only content;
- credentials and private paths are absent;
- all JSON and YAML parse;
- all Python files pass AST and CLI checks;
- no `__pycache__` or `.pyc` is distributed; and
- a human reviewer approves the query, evidence gaps, event meaning, scoring
  interpretation, selected narratives, and intended use.

## Reference implementation

Read:

- `references/screening-standard.md` for model details, states, schema, and
  rationale wording;
- `scripts/README.md` for secure setup, stage execution, MCP boundaries, and
  artifact review;
- `scripts/hv_common.py` for global REST, retry, provenance, and checkpoint
  helpers;
- `scripts/hv_1_fetch.py` through `scripts/hv_8_word.py` for the complete source
  stage topology; and
- `scripts/run_all.py` for end-to-end orchestration.
