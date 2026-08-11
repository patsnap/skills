---
name: search-applicant-technology-patents-ip
description: Search patents owned or filed by one or more specified applicants within a defined technology topic. Use when an IP searcher or analyst needs an applicant-first, topic-constrained PatSnap strategy; evidence-backed assignee expansion; auditable PatSnap formulas; executed retrieval and deduplicated datasets; or a Markdown and Word retrieval report. Do not use for an unconstrained applicant portfolio dump, an applicant-free technology landscape, or downstream technical tagging after retrieval.
---

# Search applicant technology patents

Build an auditable applicant-first patent search constrained to a confirmed technology topic. Preserve the applicant universe, topic logic, query provenance, deduplication levels, representative selection, and handoff artifacts.

Read both references before drafting formulas or executing retrieval:

- [Applicant-topic patent retrieval workflow](references/applicant-retrieval-workflow.md)
- [Topic limitation workflow](references/topic-limitation-workflow.md)

Read [README.md](README.md) before using live PatSnap data.

## Execution modes

Choose one mode and state it in Step 0:

| Mode | Use when | Completion requirement |
|---|---|---|
| `formula_only_mode` | The user needs methodology and executable formulas, or live retrieval is unavailable. | Expanded formulas, assumptions, pending confirmations, and a PatSnap execution checklist. Set `dataset_status: not_executed`. |
| `retrieval_dataset_mode` | The user asks the agent to retrieve/export records, deduplicate results, or prepare downstream datasets. | Retrieval provenance, full source dataset, available application/family datasets, representative dataset, editable Markdown report, and Word report unless opted out. |

Default to `formula_only_mode` until the user asks for executed retrieval or datasets.

## Non-negotiable formula firewall

The first substantive response must show Steps 0–7. Stop after Step 7 and request confirmation unless the user explicitly asks for a full draft including formulas.

Never output `ANCS`, `TA_ALL`, `APPLICANT_TOTAL`, `APPLICANT_TOPIC_FINAL`, a formal search strategy, an executable query, a count, or retrieval results before the visible pre-retrieval package is complete.

Use this fixed order:

```text
Step 0: Original request and execution mode
Step 1: Applicant entity expansion table
Step 2: Technology topic definition
Step 3: Topic boundary confirmation table
Step 4: Technology topic decomposition table
Step 5: Search element matrix
Step 6: Noise and exclusion boundary table
Step 7: Gate status before search
Step 8: Search strategy and formulas
```

Step 8 is allowed only when all Step 0–7 gates are `Pass` or, in an explicitly requested full draft, `Pending user confirmation`. Any `Fail` is a hard stop.

### Fixed meaning of each step

| Step | Content allowed in this step | Content prohibited in this step |
|---|---|---|
| Step 0 | Original request, execution mode, and assumptions. | Applicant formulas, topic formulas, and hit counts. |
| Step 1 | Applicant entity expansion table. | A final `ANCS` formula or single-expression shortcut. |
| Step 2 | A three-to-five-sentence definition of what the technology is and is not. | Keyword matrix, `TA_ALL`, search strategy, or formulas. |
| Step 3 | Topic boundary confirmation table. | Formal search strategy, `TA_ALL`, or combined formulas. |
| Step 4 | Technology topic decomposition table. | Formula blocks or count predictions. |
| Step 5 | Search element matrix. | Final `TA_ALL` or combined formulas. |
| Step 6 | Noise and exclusion boundary table. | Final formulas. |
| Step 7 | Gate status before search. | Retrieval or formulas while any gate is `Fail`. |
| Step 8+ | Search strategy and formulas after the gate and, by default, user confirmation. | Any shortcut around Steps 0–7. |

The following structures are invalid:

- `Step 2: Solid-state battery keyword matrix`; the keyword matrix belongs to Step 5.
- `Step 2: Technology topic keyword expansion`; Step 2 is a narrative definition.
- `Step 3: IPC classification mapping`; classifications belong to Step 5 or support Step 8.
- `Step 3: Formal search strategy`; Step 3 is the boundary table.
- `Step 4: Final search formulas`; formulas cannot begin before Step 8.

Invalid output:

```text
Step 3: Formal search strategy
Applicant expression: ANCS:(...)
Topic expression: TA_ALL=(...)
Combined query: ANCS:(...) AND TA_ALL=(...)
```

It remains invalid even if introduced with “based on the analysis above” when the visible Step 0–7 package is missing.

Invalid output:

```text
Step 2: Solid-state battery keyword matrix
TA_ALL=(...)
Step 3: Combined query
ANCS:(...) AND TA_ALL=(...)
```

Step 2 must define the topic and Step 3 must confirm its boundary.

Invalid output:

```text
Step 2: Technology topic keyword expansion
Step 3: IPC classification mapping
Step 4: Recommended final formulas
```

This order misassigns all three steps and bypasses the mandatory gate.

### Minimum visible evidence before formulas

| Gate | Minimum visible evidence |
|---|---|
| Applicant entity expansion | Candidate legal entities and name variants with `Yes`, `No`, or `Pending`. |
| Technology topic definition | Three to five sentences explaining what the topic is and is not. |
| Boundary confirmation | Include/exclude/pending table with rationale, search impact, and status. |
| Topic decomposition | Object/material, function/effect, mechanism/process, application, classification, and noise facets. |
| Search element matrix | Local-language and English terms, field scope, operator/proximity plan, formula role, and status. |
| Noise boundary | Noise source, exclusion logic, over-exclusion risk, and status. |
| Gate status | Every gate is `Pass` or `Pending`; stop on any `Fail`. |

## Step 0: Preserve the request and establish scope

Quote the user's original request verbatim before interpreting it. Separate:

- user-confirmed facts;
- agent inferences; and
- assumptions pending user confirmation.

Capture the target applicant or group, technology topic, jurisdiction/database coverage, date range, patent type, legal-status filters, subsidiary/acquisition scope, purpose, seeds, and deliverable mode. Ask only for missing parameters that materially change the search.

## Step 1: Disambiguate and expand applicant entities

If the input is a brand, abbreviation, group name, or historical name, do not select a legal entity silently. List plausible current and historical entities, their industry, relationship, and likely search path, then request confirmation when more than one route is reasonable.

For each candidate entity, record:

| Field | Required content |
|---|---|
| Canonical legal name | Current registered or otherwise authoritative name. |
| Local-language and English names | Preserve names used in filings and authoritative records. |
| Relationship basis | Parent, subsidiary, R&D entity, manufacturing entity, historical name, acquisition, branch, joint venture, alias, or user-provided entity. |
| Evidence source and note | Official website, annual report, business registry, PatSnap applicant profile, patent evidence, or user evidence. |
| Confidence | `High`, `Medium`, or `Low`. |
| Include in search | `Yes`, `No`, or `Pending`. |

Do not treat a large company or group as one applicant expression. Include evidence-supported core entities, relevant parents, R&D and manufacturing entities, historical names, acquired entities when in scope, and local-language variants. Keep uncertain relationships `Pending` and outside the final formula.

The entity table must exist before any applicant count, topic presearch, scale estimate, or combined retrieval.

## Confirm the applicant field

Require an explicit field selection before count validation, final applicant formulas, retrieval, merging, deduplication, or report completion.

| Field | Meaning |
|---|---|
| `ALL_AN` | All applicant/assignee fields |
| `AN` | Original applicant/assignee |
| `ANC` | Current applicant/assignee |
| `ANS` | Normalized original applicant/assignee |
| `ANS_EXACT` | Exact normalized original applicant/assignee |
| `ANCS` | Normalized current applicant/assignee; recommended but never assumed |
| `ANCS_EXACT` | Exact normalized current applicant/assignee |

Use a colon between field and value, for example `{field}:("Applicant name")`. Never use `=` and never use the invalid field `ANSC`.

Before confirmation, you may preserve the request, disambiguate entities, clarify group scope, draft a pending entity table, define the topic boundary, and choose an execution mode. You may not execute or finalize a query.

Use this field-confirmation prompt when the user has not chosen a field:

```text
Before I run or finalize the search, confirm which applicant/assignee field to use.
I recommend ANCS (normalized current applicant/assignee), but I need your explicit selection.

Available fields:
- ALL_AN: all applicant/assignee fields
- AN: original applicant/assignee
- ANC: current applicant/assignee
- ANS: normalized original applicant/assignee
- ANS_EXACT: exact normalized original applicant/assignee
- ANCS: normalized current applicant/assignee (recommended)
- ANCS_EXACT: exact normalized current applicant/assignee

Reply with the field, for example: ANCS or ANC.
```

Do not perform evidence-backed entity expansion, count validation, retrieval, merge, deduplication, final topic combination, or final report completion before field confirmation. You may draft a pending expansion table, but label every unverified entity and assumption.

## Steps 2–7: Build the topic preflight package

Follow [topic-limitation-workflow.md](references/topic-limitation-workflow.md) in full.

### Step 2: Technology topic definition

Write three to five sentences explaining what the topic is, what it is not, why the boundary matters for retrieval, and which terms are broad or noisy. Mark the status `Confirmed`, `Pending user confirmation`, or `Agent-inferred`.

### Step 3: Topic boundary confirmation

Create a table covering the core technical object, must-have features, optional or adjacent technology, explicit exclusions, ambiguous terms, rationale, retrieval impact, and confirmation status.

### Step 4: Technology topic decomposition

Cover object/material/component, function/effect/problem, mechanism/process/method, application/end product, classification anchors, and exclusions/noise. Assign each branch a `Core`, `Recall`, `Precision`, or `Noise` role.

### Step 5: Search element matrix

Include local-language and English terms, abbreviations, spelling variants, lower concepts, representative members, trade/common/chemical names where relevant, field scope, proximity rule, formula role, and confirmation status. Use IPC/CPC anchors when supported. Treat local-language terms as query data, not interface prose.

Use `$Wn`, `$PREn`, `$SEN`, or `$PARA` when proximity or order materially improves precision. Use `IPC_LOW` or `CPC_LOW` when parent-group recall is intended; use exact codes only when the scope requires them.

### Step 6: Noise and exclusion boundary

For each proposed exclusion, record the noise source, why it is noise, terms/classes, over-exclusion risk, and confirmation status. Do not use applicant names as a substitute for topic logic.

### Step 7: Gate status

Show the evidence and status for the applicant entity table, topic definition, boundary, decomposition, search matrix, and noise rationale. Stop on any `Fail`.

## Step 8: Construct and audit formulas

Build the applicant and topic layers independently before combining them.

Applicant layers:

- `A0`: seed or exact expressions;
- `A1`: verified entity expansion;
- `APPLICANT_TOTAL` and fully expanded `APPLICANT_TOTAL_EXPANDED`.

Topic layers:

- `S0_TOPIC_SEED`;
- `S1_TOPIC_CORE`;
- `S2_TOPIC_RECALL`;
- `S3_TOPIC_PRECISION`;
- `S4_TOPIC_FINAL_BALANCED`;
- optional `N_*` exclusions.

Provide fully expanded, executable formulas. Do not deliver unresolved shorthand such as `A_TOTAL AND S1`.

```text
APPLICANT_TOPIC_FINAL_EXPANDED =
(<fully expanded applicant expressions>) AND (<fully expanded topic formula>)
```

When exclusions are justified:

```text
APPLICANT_TOPIC_PRECISION_EXPANDED =
(<fully expanded applicant expressions>) AND (<fully expanded topic formula>) NOT (<fully expanded noise formula>)
```

Audit bidirectional consistency: every entity marked `Yes` must appear in the applicant formula, every formula entity must have a `Yes` row, and `No`/`Pending` entities must not appear.

## MCP dependencies

| Server | Level | Used for | Capabilities | Marketplace | Verified | Connection | Fallback |
|---|---|---|---|---|---|---|---|
| Advanced Patent Search | Required for `retrieval_dataset_mode`; not required for `formula_only_mode` | Applicant checks, field discovery, keyword support, count checkpoints, topic/applicant queries, nested retrieval and sample validation | `search_patents_by_original_assignee`, `search_patents_by_current_assignee`, `search_patent_count`, `search_patent_field`, `search_patents_nested`, `suggest_keywords`, semantic and patent-number search as applicable | [Official server page](https://open.patsnap.com/marketplace/mcp-servers/patent-search) | 2026-08-07 | Config key `advanced_patent_search`; `streamableHttp`; copy the current generated URL from the official Connect panel | Downgrade to `formula_only_mode`; never fabricate live results |

Do not call the MCP before the relevant gate permits it. Use only tools actually discovered in the connected server; do not infer tool availability from this document.

If a connector, fallback path, or previous partial response jumps directly to formula generation, ignore that shortcut and return to the missing gate. A connection failure never authorizes a shallow search path. Downgrade to `formula_only_mode` or pause at the current gate and identify the missing input.

## Execute retrieval and preserve provenance

In `retrieval_dataset_mode`, run checkpoints in this order:

1. Confirm all preflight artifacts exist.
2. Validate applicant expressions/counts.
3. Validate topic seed/core expressions/counts.
4. Run the applicant-topic combined query.
5. Run a justified precision/noise-filtered variant.
6. Review a sample when records are available.

For every batch preserve the normalized applicant group, matched entity, exact applicant expression, topic formula version, batch ID, source database, ISO 8601 retrieval date, jurisdiction/date/legal-status filters, retrieved count, included count, and notes.

Keep source/publication counts, application-level counts, and simple-family counts separate. Treat source hit counts as audit metrics, not downstream representative counts.

## Merge, deduplicate, and select representatives

Preserve publication/application identifiers, matched applicant names, expression provenance, formula version, batch ID, family IDs, legal status, and patent type when available.

Report these levels when fields support them:

| Level | Primary key | Purpose |
|---|---|---|
| Source/publication | Publication number plus kind code | Reproducibility and source audit |
| Application | Application number or normalized application ID | Filing-level statistics and fallback |
| Simple family | Simple-family ID or documented priority-family key | Preferred downstream representative dataset |

Choose representatives for the user's target market. Prefer a complete member in that jurisdiction; otherwise prefer WO/US/EP or another commercially relevant jurisdiction, then the record with the richest title, abstract and claims, useful legal-status certainty, and earliest application/priority context. If China is the selected market or the source task explicitly requires a China-first view, CN may be the first jurisdiction. Record the selection reason.

If family fields are unavailable, state:

```text
simple_family_status: unavailable
downstream_dataset_type: application_level_representative_fallback
```

## Required deliverables

In `formula_only_mode`, create `<applicant>_<topic>_patent_search_strategy.md` with the preflight package, expanded formulas, assumptions, limitations, and execution checklist.

In `retrieval_dataset_mode`, create:

- `<applicant>_<topic>_patent_retrieval_report.md`;
- `<applicant>_<topic>_patent_retrieval_report.docx` unless the user opts out;
- full source/hit dataset;
- application-level dataset when fields support it;
- simple-family representative dataset when fields support it; and
- query/audit appendix.

Use a scientific report structure: scope and mode, preflight package, method, formulas, provenance, datasets, validation, limitations, and appendices. Use sentence-case headings, accessible tables, source notes, print-safe styles, and restrained color. Do not use decorative gradients or dashboard card grids.

## Required report content

Every report must contain:

- the original user request;
- execution mode and pre-retrieval gate status;
- the selected applicant field and evidence of user confirmation;
- applicant scope and entity expansion table;
- technology topic definition;
- topic boundary confirmation table and confirmation status;
- technology topic decomposition table;
- search element matrix;
- noise and exclusion table;
- applicant expression audit table;
- topic strategy table and layered topic formulas;
- `APPLICANT_TOTAL_EXPANDED`;
- `TOPIC_FINAL_BALANCED_EXPANDED`;
- `APPLICANT_TOPIC_FINAL_EXPANDED`;
- `NOISE_TOTAL_EXPANDED` when noise exclusions are proposed;
- `APPLICANT_TOPIC_PRECISION_EXPANDED` when exclusions are applied;
- retrieval batch log in `retrieval_dataset_mode`;
- merge and deduplication summary in `retrieval_dataset_mode`;
- downstream dataset selection in `retrieval_dataset_mode`;
- recall and precision validation guidance without unsupported performance claims;
- handoff gate; and
- data gaps, ambiguous entities, zero-hit expressions, boundary risks, and manual-review notes.

The first substantive section must be `Step 0: Original request and execution mode`. A report must not begin with Search strategy, Applicant expression, Technology topic keywords, or a formula.

## Constraint checklist

- Never assume `ANCS` silently.
- Never infer an ambiguous applicant entity silently.
- Never skip the applicant entity expansion table for a well-known company or familiar abbreviation.
- Never use a short dimensions-plus-keywords table as the complete topic preflight package.
- Never output `ANCS`, `TA_ALL`, or a combined query before the visible Step 0–7 package.
- Never label formal strategy as Step 3, keyword expansion as Step 2, classification mapping as Step 3, or final formulas as Step 4.
- Never use applicant names in place of topic logic; applicant and topic formulas must both be explicit.
- Never rely only on literal synonyms of the user's topic; expand across multiple technical facets.
- Never run applicant-scale estimates, topic presearch, or combined retrieval before both applicant and topic preflight artifacts exist.
- Never deliver only shorthand formulas; provide fully expanded executable expressions.
- Never claim complete recall or precision without executed results and validation samples.
- Never include an ambiguous affiliate without evidence or user approval.
- Never hide applicant expressions, topic formulas, or query strings.
- Never use the full source hit list directly as the downstream representative dataset when application or family fields support deduplication.
- Never route directly to downstream screening/tagging unless the user explicitly requests that separate post-retrieval step.
- Never mark `retrieval_dataset_mode` complete without `downstream_dataset_type`, `downstream_dataset_file`, and `downstream_dataset_count`.
- Never omit the editable Word report in `retrieval_dataset_mode` unless the user opts out.

## Validation and handoff

Do not claim recall or precision without executed results, sampled relevance labels, and independent recall samples. Classify misses as boundary disagreement, missing technical facet, field-scope issue, translation gap, classification gap, stable noise, or operator/bracket error, then update every affected table and formula consistently.

Before handoff verify applicant field confirmation, entity disambiguation, preflight order, formula-table consistency, expanded formulas, noise logic, retrieval provenance, deduplication, representative dataset, Word output requirement, and full-hit exclusion from downstream representative input.

Use one of these handoff blocks:

```text
execution_mode: retrieval_dataset_mode
retrieval_mode: applicant_topic_limited_retrieval
target_applicant: <applicant group>
applicant_field: <confirmed field>
technology_topic: <confirmed topic>
topic_limitation: <formula version>
source_hit_count: <raw count>
source_hit_count_usage: audit_only
downstream_dataset_type: simple_family_representative
downstream_dataset_file: <file>
downstream_dataset_count: <actual representative count>
ready_for: downstream_review_or_analysis
```

```text
execution_mode: formula_only_mode
retrieval_mode: applicant_topic_limited_formula
target_applicant: <applicant group>
applicant_field: <confirmed field>
technology_topic: <confirmed or pending topic>
expanded_formula_status: complete
dataset_status: not_executed
ready_for: patsnap_execution
```
