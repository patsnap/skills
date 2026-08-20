---
copyright: "Copyright © Patsnap. All rights reserved."
name: create-patent-landscape-overview-ip
description: Orchestrate an evidence-backed patent-landscape program for product planning, R&D strategy, competitor intelligence, technology-route analysis, recommended patent packages, and portfolio planning. Use when a user needs search and de-noising, complete-population landscape statistics, taxonomy design, a genuine human tagging handoff, representative patent analysis, and a self-contained scientific HTML report.
---

# Create a Patent Landscape Overview

## Purpose

Translate a business or R&D question into a reproducible patent-landscape workflow and decision report.
The workflow preserves a four-stage suite plus one genuine human tagging handoff:

```text
Stage 0 — Scope and research questions
Stage 1 — Search and de-noising
Checkpoint 1 — Query and precision review
Stage 2 — Full-scope statistics and value signals
Checkpoint 2 — Analytical-scope review
Stage 3 — Taxonomy and tagging-system design
Checkpoint 3 — Taxonomy approval
Stage 3.5 — Human tagging in an approved data/SaaS tool
Stage 4 — Evidence synthesis and self-contained HTML report
Checkpoint 4 — Report review
```

## Suitable requests

- patent landscape or panorama;
- technology-field activity and player mapping;
- product, component, application, or R&D-direction patent analysis;
- competitor or key-player patent comparison;
- technology taxonomy and route hypotheses;
- technical problem, solution, and effect analysis;
- recommended patent packages and tagged patent indexes;
- legal, asset, transaction, or value signals requiring follow-up;
- a client-ready offline patent-intelligence HTML report.

## Out of scope unless separately authorized and supported

- non-patent-literature landscape;
- SEP essentiality;
- formal FTO, infringement, validity, novelty, or inventive-step opinions;
- complete litigation or UPC dispute strategy;
- market-size conclusions based only on patents;
- bulk REST/API export not exposed by an approved connector;
- automatic full-pool human-quality tagging.

## Decision-first operating principles

1. Start from the decision, not a list of available charts.
2. Ask only for missing information that materially changes scope.
3. Record search, dates, geography, entity normalization, count unit, family rule, cutoff, and limitations.
4. Separate complete-population metrics from candidate pools and representative patents.
5. Trace every material conclusion to data, patents, sources, or an explicit assumption.
6. Treat status, citations, family, disputes, transactions, pledges, customs, and awards as signals.
7. Use concise technical and business language with calibrated uncertainty.
8. Never invent tags, patent records, aggregations, or human-review results.

## Required inputs

- technology domain or topic;
- decision goal;
- entity scope: industry, selected applicants, or comparison set;
- product, component, application, problem, or effect focus where relevant;
- include and exclude concepts;
- geography or receiving-office scope;
- date field and range;
- count unit and family rule;
- deliverables and audience;
- confidentiality and data-handling constraints.

## Decision-relevant defaults

Use these only when they fit the request and disclose them:

| Dimension | Default |
|---|---|
| Decision goals | Product planning, R&D strategy, competitor monitoring, portfolio planning |
| Geography | Global scope narrowed to decision-relevant authorities |
| Date field | Earliest priority date for technology activity; other fields only with rationale |
| Time range | Technology-appropriate historical window plus recent-activity view |
| Count unit | Simple families for technology statistics; publications only where the question requires document-level analysis |
| Main deliverable | One self-contained HTML report plus reproducibility artifacts |
| Legal boundary | Signals and follow-up only, not legal opinion |

Do not hard-code CN/US/EP, 2023, or publication-level counting.

## Verified Patsnap MCP services

Use the English interface and English output.
Inspect the live connector schema before calling a tool.

### Required: Advanced Patent Search

- Connector key: `advanced_patent_search`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`
- Role: query planning, global patent retrieval, entity-specific search,
  representative records, and reproducible counts when supported.

### Required: Patent Briefing

- Connector key: `patent_briefing`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- Role: bibliography, family, status, claims, description, translations,
  images, and representative technical summaries.

### Recommended: Deep Patent Mining

- Connector key: `deep_patent_mining`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-mining
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-mining`
- Role: technical topics, problems, solutions, effects, classifications,
  materials, and application domains.

### Recommended: Global Core Patent Database

- Connector key: `global_core_patent_database`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/core-patents
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/core-patents`
- Role: family, legal events, citations, disputes, licensing, transfer,
  reexamination/invalidation, full text, and PDF where exposed by the live schema.

Do not require legacy endpoint IDs from the source package.
Do not claim that a chart, panorama, asynchronous-project, or report-generation connector exists
unless its current global marketplace contract and runtime tool are verified.

For each call record:

```text
connector_key
tool_name
request_id
query_version_or_identifier
parameters_and_filters
response_semantics
retrieved_at
source_locator
limitations
```

If a required connector is unavailable, continue only with authorized user-supplied data or preparation work.
Mark all affected modules unavailable; never simulate connector results.

## PPS suite relationships

The localized suite uses clear task names:

| Stage | Skill | Responsibility |
|---|---|---|
| 1 | `search-patents-ip` | Search design, retrieval, de-noising, candidate pool, core recall |
| 2 | `analyze-patent-search-results-ip` | Complete-scope statistics, patterns, value and risk signals |
| 3 | `tag-patent-search-results-ip` | Taxonomy, key questions, patent packages, tagging demo and export |
| 4 | `create-patent-search-report-ip` | Evidence synthesis, route interpretation and safe HTML report |

These are suite links, not automatic proof that a skill is installed.
When a suite member is present, load and apply its contract.
When it is absent, execute the embedded stage contract below or stop at a genuine tool/human boundary.
Do not invent a sub-skill call.

The source package cites an `ARCHITECTURE.md` that is not present.
Do not add it. This file is the authority for cross-stage schemas and checkpoints.

## Progress reporting

Use English stage names consistently:

- `[Stage 1/4 · Search and De-noising]`
- `[Stage 2/4 · Landscape Statistics]`
- `[Stage 3/4 · Taxonomy and Tagging Design]`
- `[Stage 3.5 · Human Tagging Handoff]`
- `[Stage 4/4 · Evidence Report]`

At stage start, state the stage and objective in one line.
At stage completion, report:

- artifacts written;
- input/output record counts;
- query/taxonomy/report version;
- unresolved issues;
- next stage and whether user or human action is required.

Avoid decorative symbols as the only state indicator.

## Stage 0 — Turn the decision into a searchable structure

### Step 0.1 — Normalize the request

Create:

```text
project_id
technology_domain
decision_goals
entity_scope
product_component_application_scope
include_topics
exclude_topics
geography
date_field
date_range
count_unit
family_rule
status_rule
data_cutoff
deliverables
audience
confidentiality
```

### Step 0.2 — Draft 3–7 research questions

Examples:

- Is activity increasing, stable, or declining under a comparable count method?
- Which normalized players are active and in which technical branches?
- Which technical problems and solution types appear repeatedly?
- Which branches merit deeper claim/description reading?
- Which patents are representative enough for a reviewed package?
- Which portfolio or R&D hypotheses deserve follow-up?
- Which legal/asset signals require qualified review?

### Step 0.3 — Build a first-pass decomposition

Use:

- sub-technologies;
- products and components;
- applications and operating environments;
- technical problems and effects;
- material, process, control, and architecture routes;
- known noise and excluded domains.

This is search scaffolding, not the approved Stage 3 taxonomy.

## Cross-stage artifact contract

Every artifact must include:

- `schema_version`;
- `project_id`;
- `stage`;
- `created_at`;
- `source_cutoff`;
- `input_artifact_ids`;
- `record_count`;
- `checksum` where practical;
- `status`;
- `limitations`;
- `review_state`.

### Stage 1 outputs

```text
search_config.json
candidate_pool.csv
core_recall.csv
```

### Stage 2 outputs

```text
panorama_stats.json
patent_index.core.json or patent_index.core.csv
value_signals.json
chart_data.json
panorama_stats_report.html
```

### Stage 3 outputs

```text
tech_breakdown.json
key_questions.json
patent_packages.csv
tagging_demo_sample.csv
to_be_tagged.csv
```

### Human Stage 3.5 output

```text
tagged_pool.csv
```

### Stage 4 outputs

```text
report_manifest.json
report.html
```

Files are generated project deliverables outside this skill package.
Do not add them to the reusable skill directory.

## Stage 1 — Search and de-noising

Load `references/query-and-taxonomy-methodology.md`.

### Stage 1.1 — Build search concepts

Create:

- constant topic anchor;
- strong defining terms;
- weaker terms that require classification or proximity support;
- technical classifications verified against current definitions;
- product/application/problem/effect terms;
- applicant and inventor supplements where relevant;
- tiered exclusions with a reason for each;
- language, spelling, transliteration, and abbreviation variants.

Verify the exact query syntax against the live product/tool.

### Stage 1.2 — Build branch queries

Use the localized canonical structure:

```text
(
  strong field-scoped terms
  OR (weaker terms AND classification anchor)
  OR self-sufficient specific classifications
)
AND constant topic anchor
NOT tiered exclusions with reasons
AND scope envelope
```

### Stage 1.3 — Retrieve and de-noise

Capture:

- raw matched total;
- candidate records;
- de-noising rule hits;
- excluded records and reasons;
- family/document relationships;
- entity aliases;
- missing/ambiguous metadata;
- query and retrieval provenance.

### Stage 1.4 — Validate precision and recall signals

For each branch:

1. draw a random or otherwise reproducible sample, typically 20–30 when available;
2. evaluate against the written branch inclusion rule;
3. report sample size, relevant count, and estimated precision;
4. examine a near-miss sample removed by exclusions or just outside the boundary;
5. record possible false negatives;
6. tighten or broaden the query with a versioned rationale.

An 80% precision target is a planning default, not a universal acceptance threshold.
Report confidence intervals or small-sample limitations where appropriate.

### Stage 1 candidate record

```text
record_id
family_id
publication_number
application_number
grant_number
authority
title
applicant_raw
applicant_normalized
priority_date
filing_date
publication_date
raw_status
normalized_status
status_as_of
IPC_CPC
branch_rule_hits
query_ids
relevance_state
exclusion_reason
source_url
source_ids
```

### Checkpoint 1 — Query and precision review

Show:

- each branch definition;
- the four query components;
- matched total and candidate count;
- sampling method and estimated precision;
- near-miss/false-negative observations;
- important exclusions and risks.

Choices:

- approve and continue;
- edit specified branches and rerun only affected searches;
- restart Stage 0.

If the user already delegated the full workflow, proceed when the agreed threshold and risk gates pass,
but still record the checkpoint decision. Do not bypass material scope changes.

## Stage 2 — Landscape statistics and value signals

### Population rule

Use only verified complete-result aggregations or reproducible complete buckets for:

- annual trends;
- applicant rankings and trends;
- receiving-office or authority distributions;
- technical branch counts/shares;
- applicant × branch matrices;
- status distributions;
- concentration and growth metrics.

Candidate pools, Top-K lists, and representative patents cannot provide population denominators.
If complete metrics are unavailable, mark them `Unavailable`.

### Stage 2.1 — Normalize analytical dimensions

Document:

- family/count unit;
- date field;
- jurisdiction and authority semantics;
- applicant group and alias rules;
- status mapping;
- taxonomy rule-hit versus reviewed-tag distinction;
- multi-label duplicate-counting rule;
- publication lag;
- cutoff and database coverage.

### Stage 2.2 — Generate full-scope statistics

Where supported:

- annual activity;
- normalized applicants;
- applicant trends;
- authorities/jurisdictions;
- preliminary branch rule hits;
- applicant × branch;
- simple status observations;
- family/citation indicators.

### Stage 2.3 — Cross-screen value and risk signals

Possible signals:

- technical relevance and branch centrality;
- family breadth;
- forward citations with age/field/office limits;
- status and remaining-term proxy;
- legal events or challenges;
- transfer, license, pledge, customs, or award records;
- competitor concentration;
- product/application relevance;
- representative claim/description evidence.

Use transparent criteria and preserve missing data.
No signal proves value, validity, enforceability, market adoption, or legal risk.

### Checkpoint 2 — Analytical-scope review

Show:

- top trend, player, authority, and branch findings;
- denominator and data completeness;
- value/risk-signal shortlist;
- unavailable metrics and limitations;
- proposed scope for taxonomy design.

Choices:

- approve and continue;
- narrow branches, change players/date/count rules, and rerun affected stages.

## Stage 3 — Taxonomy and tagging-system design

Load `references/query-and-taxonomy-methodology.md`.

### Stage 3.1 — Build the four-column taxonomy

```text
level_1_branch
level_2_branch
level_3_taggable_technique
technical_description_and_membership_rule
```

Rules:

- top-down architecture plus bottom-up patent evidence;
- typically 4–6 level-1 branches;
- typically 3–8 level-2 branches per parent;
- level 3 is the atomic primary tag;
- each level-3 tag has include/exclude rules and a testable query;
- approximately 40 level-3 tags is a human-consistency ceiling, not a reason to suppress necessary distinctions;
- primary sibling tags should be mutually clear;
- cross-cutting themes may be separate multi-label fields;
- duplicate counting from multi-label tags must be disclosed.

### Stage 3.2 — Define key technical questions

Target at least ten across major branches when evidence supports them.

Each question includes:

- question ID;
- branch IDs;
- technical problem;
- why it matters;
- supporting evidence;
- representative-family candidates;
- uncertainty;
- proposed deep-reading route.

### Stage 3.3 — Build recommended patent packages

Target at least ten packages and at least three families per package when the evidence supports them.
Do not pad packages.

Selection dimensions:

- technical relevance;
- representative solution;
- technical-effect evidence;
- family/citation/status signals;
- player or application relevance;
- claim readability;
- business decision fit;
- review status.

Recommendation reasons use clear evidence, not unsupported labels.

### Stage 3.4 — Create a tagging demo and export

Create a 20–30 record demo when enough valid records exist.
Use it to test:

- taxonomy clarity;
- multi-label rules;
- ambiguous cases;
- reviewer consistency;
- required columns;
- encoding and delimiter.

Then export the full untagged pool for human work.

### Checkpoint 3 — Binding taxonomy review

Show:

- four-column taxonomy;
- key technical questions;
- patent packages;
- demo labels and ambiguous records;
- required human-tagging columns;
- taxonomy and schema versions.

The user or authorized reviewer must approve the taxonomy before Stage 3.5.
Do not auto-approve this checkpoint.

## Stage 3.5 — Genuine human tagging handoff

This is a real human boundary.

### Before handoff

Validate `to_be_tagged.csv`:

- file exists;
- UTF-8 encoding;
- expected row count;
- stable record/family identifiers;
- taxonomy version;
- required columns;
- no duplicate primary IDs;
- no unauthorized confidential columns;
- checksum and export timestamp.

### User instruction

Ask the authorized user to tag the full pool in their approved SaaS or data tool,
then return `tagged_pool.csv` to the agreed project path.

Do not require a specific regional product.
Do not fabricate tags.
Stop at the handoff.

### On return

Validate:

- returned file exists and is readable;
- row count reconciles with export;
- stable IDs match;
- required tag fields contain values or explicit review states;
- taxonomy version matches;
- multi-label delimiter is valid;
- unknown labels are rejected;
- duplicate/missing rows are reported;
- checksum and reviewer metadata are recorded.

Do not enter Stage 4 until the returned data pass or have an approved exception record.

## Stage 4 — Evidence synthesis and HTML report

Load only the scenario references required by the request:

- `references/scenario-industry-landscape.md`
- `references/scenario-technology-evolution.md`
- `references/scenario-competitor-portrait.md`
- `references/scenario-solution-deep-dive.md`
- `references/scenario-patent-package-and-index.md`
- `references/scenario-asset-and-risk-signals.md`

Load:

- `references/report-html-blueprint.md`
- `references/report-visual-style.md`

### Stage 4.1 — Reconcile inputs

Read and validate all Stage 1–3.5 artifacts.
Confirm schema, project, taxonomy, count, checksum, cutoff, and approval compatibility.
Do not rely on conversation memory as the data source.

### Stage 4.2 — Build evidence chains

Use:

```text
complete metric
-> observed pattern
-> representative patents or tagged evidence
-> bounded inference
-> decision implication
-> recommended action
```

### Evidence levels

| Level | Meaning | Allowed output |
|---|---|---|
| L1 | Direct complete-scope data fact | Count, ranking, trend, distribution |
| L2 | Observed pattern | Growth, concentration, dispersion, migration |
| L3 | Analytical inference | Possible technology focus or strategic implication |
| L4 | Business recommendation | Read, monitor, compare, research, portfolio action |
| L5 | Legal or risk signal | Follow-up legal review; not a conclusion |

### Stage 4.3 — Create manifest and report

`report_manifest.json` records:

- every input artifact and checksum;
- scope and cutoff;
- report sections;
- charts/tables and source metric IDs;
- claims/findings and evidence IDs;
- unavailable modules;
- visual QA status;
- approval state.

`report.html` follows the report blueprint and visual style.

### Checkpoint 4 — Report review

Show:

- report path;
- section list;
- evidence coverage;
- unavailable modules;
- visual QA result;
- limitations and next actions.

The user may accept or request a scoped revision.
Do not silently mark a report accepted.

## Rollback and restart

- Query change: rerun Stage 1 and all affected downstream stages.
- Date/count/entity change without query change: rerun Stage 2 onward as required.
- Taxonomy change: rerun Stage 3, human tagging, and Stage 4.
- Tag correction: preserve Stage 1–3 and rerun reconciliation/Stage 4.
- Report wording/layout change only: rerun Stage 4.
- Scope restart: return to Stage 0 and create a new project version.

Never delete unaffected approved artifacts during rollback.
Mark superseded versions and preserve provenance.

## V0 capability boundary

V0 can support, when verified data are available:

- patent search and bibliography;
- family and receiving-office footprint;
- citations and simple status;
- claims, description, translations, images;
- legal/asset-event signals;
- complete aggregations or reproducible buckets;
- technical pre-tags and local reviewed taxonomy;
- patent packages and indexes;
- safe self-contained HTML.

V0 does not promise:

- complete NPL;
- SEP essentiality;
- full litigation/UPC mapping;
- unsupported bulk exports;
- unavailable panorama/report MCPs;
- formal legal opinions;
- automated full-pool human-quality tagging.

## HTML report structure

Use a decision-first, dense, scientific/executive report:

1. cover and scope metadata;
2. executive summary;
3. scope and method;
4. landscape dashboard;
5. technology taxonomy and map;
6. technical route and problem/solution deep dives;
7. competitor portraits;
8. recommended patent packages and index;
9. asset/legal/risk signals;
10. product, R&D, and portfolio recommendations;
11. appendix with search, taxonomy, data, evidence, and limitations.

Default to one self-contained HTML file.
Do not create a data folder unless the user explicitly requests one or the approved data volume makes one file impractical.

## Report safety and aesthetics

- white/neutral canvas;
- navy/slate hierarchy;
- restrained teal accent;
- system font stack;
- semantic header, navigation, main, sections, tables, and footer;
- accessible static SVG/CSS charts plus table equivalents;
- data captions with date field, count unit, cutoff, and scope;
- responsive navigation and horizontal table overflow;
- visible keyboard focus and reduced motion;
- print CSS and repeated table headers;
- escaped user/database text and allowlisted HTTP(S) links;
- no remote dependency, marketing hero, gradient, floating blob, stock image,
  canvas-only evidence, color-only meaning, or confidential placeholder.

If chart data are unavailable, show an unavailable panel instead of a fake or empty chart.

## Final quality gates

### Orchestration

- Stages 0–4 and Stage 3.5 are complete or appropriately paused.
- Checkpoints 1–4 have decision records.
- Suite skills used are actually installed or the embedded contract was executed.

### Artifacts

- Every required artifact exists or has an approved unavailable reason.
- Schema/project/stage/taxonomy versions reconcile.
- Counts, IDs, checksums, cutoffs, and approvals reconcile.

### Search

- Branch queries follow the expert method.
- Precision and near-miss recall checks are recorded.
- Exclusions have reasons.
- Live query syntax was verified.

### Statistics

- Complete-population metrics and representative records are separated.
- Every chart discloses date field, count unit, cutoff, scope, and duplicate-counting rule.
- Publication lag and entity normalization are visible.

### Taxonomy and tagging

- Tags have include/exclude rules.
- Primary siblings are clear; cross-cutting multi-labels are explicit.
- Human handoff is genuine and returned tags are validated.
- No missing tag was invented.

### Evidence and legal calibration

- Major findings have evidence IDs and levels.
- Status/citation/family/event/transaction records are signals.
- No FTO, infringement, validity, novelty, inventive-step, SEP, or enforceability conclusion appears.

### Report

- HTML opens offline and passes visual inspection.
- Navigation, tables, SVGs, responsive layout, focus, and print are usable.
- No blank chart, broken link, overlap, unsafe content, or hidden material limitation remains.

## Final response

Summarize:

- confirmed project scope and defaults actually used;
- data queried or user-supplied;
- stages and checkpoints completed;
- artifacts and counts;
- unavailable tools or skipped modules;
- top L1/L2 evidence and bounded L3/L4 implications;
- legal/risk signals and review needs;
- HTML path and visual-QA status;
- limitations and next action.

Keep the conversational handoff concise unless the user requests the full report inline.
