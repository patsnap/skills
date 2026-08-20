---
copyright: "Copyright © Patsnap. All rights reserved."
name: classify-technical-evidence-ip
description: Build, refine, govern, and apply an evidence-based taxonomy to patents, scientific literature, product records, technical intelligence, customer requirements, and other structured text. Use for open label discovery, semi-open or closed-set classification, label definitions and decision rules, pilot labeling, full CSV/XLSX labeling, adjudication queues, taxonomy backlogs, quality assurance, and selective Patsnap MCP evidence enrichment.
---

# Evidence-based technical labeling

Baseline: `evidence-based-labeling-v1.1`. Default decision rules: `default-v1.1`.

## Purpose

Treat labeling as a governed lifecycle, not a one-off prompt. Keep four types of work visibly separate:

1. Business decisions: objective, unit of analysis, dimensions, formal definitions, freeze decisions, and full-run authorization.
2. Model judgment: fact extraction, candidate recall, boundary comparison, recommendations, and reasons.
3. External evidence: retrieved patents, literature, classifications, technical concepts, and provenance.
4. Deterministic validation: schemas, identifiers, label paths, record coverage, evidence presence, states, and versions.

Never promote a candidate label silently. Never force a weakly supported label to avoid a blank. Never describe retrieved results as a final classification decision.

## Load only the references needed

- For diagnosis or a mode change, read `references/workflow-modes.md`.
- Before inspecting inputs or creating deliverables, read `references/input-output-contract.md`.
- Before pilot or full labeling, read `references/default-decision-rules.md`.
- When creating, defining, merging, splitting, retiring, or versioning labels, read `references/taxonomy-design.md`.
- Before using a Patsnap MCP service, read `references/zhihuiya-mcp-orchestration.md`.
- Before pilot acceptance, full validation, or review-queue creation, read `references/quality-and-review.md`.
- When a selected domain has a manifest, read the manifest first and then only the files it names.
- For the milk-protein processing fixture, read `references/domain-milk-protein.yaml`, then its taxonomy, rules, and examples.

## Diagnose before asking

Inspect the supplied files and natural-language request before asking questions. Determine:

1. Business objective and unit of analysis.
2. Candidate dimensions.
3. Whether a usable taxonomy exists.
4. Whether labels have definitions and boundaries.
5. Whether decision rules exist.
6. Whether adjudicated examples or correction history exist.
7. Whether candidate new labels are permitted.
8. Record identifier and relevant text or metadata fields.
9. Data sensitivity, license restrictions, and whether external enrichment is authorized.

Infer items 3–6 from the material where possible. Ask only for missing business choices or permissions that would materially change the result.

Recommend one operating mode and obtain confirmation:

- `discovery`: no usable taxonomy exists.
- `semi_open`: a partial taxonomy exists or proposed candidate labels are permitted.
- `closed`: the taxonomy is frozen and new formal labels are prohibited.

Do not switch modes silently. If live retrieval is authorized and the goal is specific enough to formulate a search concept, execute the discovery capability profile before freezing dimensions or the taxonomy. If external enrichment is not authorized or unavailable, continue locally and record the unexecuted capability explicitly.

## External-data authorization gate

MCP connectivity is not permission to transmit records. Before sending any source text, identifier, excerpt, or derived query:

1. Classify the data as public, internal, confidential, restricted, or unknown.
2. Confirm the user or data owner permits the proposed external transmission.
3. State which fields, records, or normalized concepts will be sent and why.
4. Minimize content and use public publication numbers or normalized concepts when sufficient.
5. Exclude secrets, personal data, privileged material, licensed text, and export-controlled details unless specifically authorized and supported.
6. Record authorization status and the chosen minimization method.

Use `not_authorized`, `unavailable`, `incomplete`, or `not_needed` instead of pretending enrichment occurred.

## Three confirmation gates

Use three consolidated gates by default. Do not stop after every internal step.

### 1. Scope gate

Confirm:

- business objective;
- unit of analysis;
- dimensions;
- operating mode;
- candidate-label policy;
- required dimensions and selection constraints;
- data-sensitivity assessment;
- external-enrichment authorization.

### 2. Freeze gate

Confirm together:

- evidence-backed taxonomy;
- label definitions and paths;
- positive, hard-negative, and boundary examples;
- default or revised decision rules;
- pilot results;
- proposed corrections;
- unresolved taxonomy backlog;
- version to freeze.

### 3. Execution gate

Confirm:

- frozen taxonomy and rule versions;
- full-run file, sheet, record range, and counting unit;
- selective MCP trigger policy and transmission scope;
- expected outputs;
- explicit authorization to begin the full run.

Between gates, inspect assets, perform authorized retrieval, draft the taxonomy, create definitions, sample records, execute the pilot, and analyze errors autonomously. Pause outside these gates only when a missing choice would materially change the result or an external action requires new authority.

## Core workflow

### 1. Normalize the task

Create a task configuration from the request and files. Preserve original columns. Record:

- task ID, objective, and unit;
- source files and sheets;
- stable record ID;
- text and metadata field mapping;
- dimensions and selection constraints;
- mode and state;
- taxonomy and rules versions;
- evidence order;
- candidate-label policy;
- review-routing policy;
- MCP policy and authorization;
- translation provenance;
- confirmation states.

Validate with `scripts/validate_task_config.py`.

### 2. Inspect labeling assets

Assess:

- file and sheet structure;
- record count, blanks, duplicates, and unstable IDs;
- current labels and paths;
- label coverage and imbalance;
- duplicate or dirty paths;
- definitions, inclusion and exclusion criteria;
- hierarchy and parent integrity;
- positive, hard-negative, and boundary examples;
- decision-rule completeness;
- correction and adjudication history;
- missing or low-quality evidence fields.

Use `scripts/inspect_labeling_input.mjs` for CSV/XLSX structure and `scripts/validate_taxonomy.py` for taxonomy integrity.

### 3. Execute the authorized discovery profile

When scope is clear and external enrichment is authorized, combine:

- keyword expansion;
- semantic or field retrieval;
- classification assistance;
- focused patent or literature retrieval;
- technology topics and application domains for representative records.

Cover the main business concepts, source clusters, or proposed top-level branches. Keep retrieved concepts, proposed labels, and formal labels in separate fields.

If a capability returns no result, retry once with a simpler normalized concept when useful. Record the empty or limited result and continue through other capabilities. Do not convert retrieval output directly into formal labels.

### 4. Build or refine the taxonomy

In `discovery` mode:

- open-code representative records;
- normalize equivalent expressions;
- propose dimensions and hierarchy;
- create label confirmation cards;
- keep every new label in candidate state until confirmed.

In `semi_open` mode:

- apply formal labels where supported;
- distinguish candidate labels explicitly;
- route uncovered concepts to the taxonomy backlog;
- prevent candidate labels from entering formal output columns.

In `closed` mode:

- apply only eligible formal labels;
- use `unclassified` when no formal label fits;
- log complete-evidence gaps in the taxonomy backlog;
- never invent a formal label during the run.

### 5. Build definitions and examples from evidence

For each proposed label family, use local and authorized external evidence to define:

- definition;
- inclusion criteria;
- exclusion criteria;
- synonyms;
- confusable labels;
- representative positive example;
- high-similarity hard negative;
- boundary example;
- parent/child relationship;
- output eligibility;
- source identifiers and access date.

For patents, relevant evidence may include technology topics, application domains, classifications, technical problem/approach/benefit, description, claims, and similar or adjacent records. Cover every top-level branch and every unresolved adjacent-label boundary. Trace examples to publication or literature identifiers where practical.

### 6. Build an adaptive pilot sample

Combine local stratified sampling with authorized semantic, keyword, similar-record, or classification-assisted retrieval. Include:

- common records;
- each major branch;
- rare labels where available;
- adjacent-label conflicts;
- incomplete records;
- hard negatives;
- likely unclassified records;
- likely taxonomy gaps;
- records with translated evidence.

Do not use a fixed sample count per node mechanically. Scale the sample to taxonomy size, diversity, prevalence, and observed instability. Document the method and limitations.

### 7. Label from evidence

For each record:

1. Identify the core object, action, purpose, and technical facts.
2. Extract a short source-backed evidence excerpt.
3. Recall candidate labels.
4. Apply definitions, inclusion rules, exclusion rules, selection constraints, and conflict rules.
5. Select supported formal labels or an explicit abstention state.
6. Record reason, categorical confidence, and review status.
7. Record translation and MCP provenance where used.

Prefer user-provided evidence. During pilot and full labeling, call MCP selectively only for missing abstracts, claims, descriptions, technical triads, topics, domains, boundary ambiguity, or external corroboration. Do not send every complete record to MCP. Similar records help compare boundaries; they do not decide the label.

### 8. Review the pilot

Separate error sources:

- taxonomy coverage gap;
- unclear definition;
- hierarchy or granularity issue;
- decision-rule problem;
- missing or conflicting evidence;
- translation ambiguity;
- model judgment error;
- source-data defect.

Propose changes with affected records and expected impact. Do not apply taxonomy changes silently. Repeat the pilot until the user approves the freeze version.

### 9. Execute full labeling

Before starting, show:

- source and record count;
- range and counting unit;
- frozen taxonomy version;
- frozen rules version;
- pilot status;
- selective MCP triggers and authorization;
- output files and sheets;
- unresolved limitations.

Begin only after explicit full-run authorization. Keep formal, candidate, unclassified, and review states distinct. Preserve every source row and original column.

### 10. Validate and deliver

Deliver:

- original data plus labeling fields;
- evidence long table;
- taxonomy;
- decision rules;
- review queue;
- taxonomy backlog;
- QA summary;
- task metadata;
- MCP provenance.

Validate:

- source/result record coverage;
- stable IDs;
- legal label paths;
- parent and version consistency;
- formal-label evidence;
- required dimensions;
- single/multi-select constraints;
- status and confidence values;
- candidate leakage;
- review routing;
- enrichment and translation provenance.

Use `scripts/create_labeling_workbook.mjs` and `scripts/validate_labeling_output.mjs` where the runtime is available.

## MCP capability mapping

Read `references/zhihuiya-mcp-orchestration.md` before live calls.

- Advanced Patent Search: discovery, keyword assistance, semantic/field/classification-assisted retrieval, and representative patents.
- Deep Patent Mining: technical problem/approach/benefit, technology topic, classification description, and application domain.
- Patent Briefing: claims, descriptions, bibliography, family, status, images, and direct candidate verification.
- Scientific & Translational Evidence: literature-domain evidence where the selected task fits its published scope.

Select by capability rather than assuming a universal server. Do not hard-code a credential-bearing endpoint. Cache identical public-patent and query results when permitted. Record service, tool, purpose, query summary, record/label ID, returned identifiers, status, and notes.

If a connector or capability is unavailable, continue with local material when possible and mark enrichment incomplete. State the unexecuted stage and capability. Never fabricate identifiers or evidence.

## Output states

Use exactly:

- `formal`
- `candidate`
- `unclassified`
- `needs_review`

Use `high`, `medium`, or `low` confidence. Tie confidence to evidence quality and boundary clarity. Do not invent probability percentages.

Do not equate `unclassified` or `not_applicable` with `needs_review`.

### Review Queue

Send a record to `Review Queue` only when a human decision can change its current outcome:

- low confidence;
- scope ambiguity;
- unresolved adjacent labels;
- conflicting or incomplete evidence;
- translation ambiguity affecting the decision;
- dirty paths;
- missing required dimensions.

### Taxonomy Backlog

Send complete-evidence coverage gaps, missing leaf granularity, and uncovered concepts to `Taxonomy Backlog`. Group repeated gaps by issue type and list all affected records.

- Complete-evidence `not_applicable` may pass automatically for an optional dimension.
- A directly supported, output-eligible formal parent label may pass without record review.
- Log useful child-granularity gaps in the backlog.
- Convert repeatedly confirmed boundary decisions into versioned rules.

Report record review rate and taxonomy backlog count as separate QA metrics.

## Bundled helpers

- `scripts/inspect_labeling_input.mjs`: inspect workbook or CSV structure.
- `scripts/validate_task_config.py`: validate task configuration and gates.
- `scripts/validate_taxonomy.py`: validate taxonomy schema and hierarchy.
- `scripts/create_labeling_workbook.mjs`: create the standard ten-sheet workbook.
- `scripts/validate_labeling_output.mjs`: validate workbook-level output.

Before running an `.mjs` helper, load workspace dependencies. Copy the helper into a writable working directory and ensure that directory resolves the bundled dependency directory. Do not install replacement packages and do not hard-code a user-specific runtime path.

Assets are starting templates, not immutable policy. Preserve their schemas unless an approved migration or task-specific change is recorded.

## Workbook and report presentation

Use a restrained scientific format:

- descriptive sheet and table names;
- neutral readable typography;
- white background with dark navy section headers;
- subtle structural borders;
- frozen header rows and filters;
- explicit text statuses in addition to color;
- units, counts, versions, and data cut-off dates;
- source and limitation notes;
- machine-readable flat tables;
- no decorative gradients, emoji, or color-only decisions.

Keep source data separate from results and evidence. Do not use formatting as the only carrier of analytical meaning.

## Final checks

Before delivery:

1. Confirm scope and execution authorization.
2. Confirm source/result row equality.
3. Confirm no source column or record was dropped.
4. Confirm every formal label is eligible and evidenced.
5. Confirm candidates did not leak into formal outputs.
6. Confirm review queue and taxonomy backlog are routed separately.
7. Confirm taxonomy/rules versions are consistent.
8. Confirm translation provenance for translated evidence.
9. Confirm MCP authorization, calls, and failures are recorded without credentials.
10. Confirm workbook formulas, key ranges, and visual rendering have no obvious errors.

This skill produces an auditable classification workflow. It does not replace subject-matter adjudication, legal advice, or data-governance approval.
