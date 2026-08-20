---
copyright: "Copyright © Patsnap. All rights reserved."
name: tag-patent-search-results-ip
description: Design and calibrate the Stage 3/4 tagging system for a patent-landscape program. Use after search-patents-ip and analyze-patent-search-results-ip to create a versioned four-column technology taxonomy, decision-relevant technical questions, evidence-backed patent groups, a reviewed tagging demonstration, and a complete empty-tag CSV for genuine human tagging at Stage 3.5; validate the returned tagged_pool.csv before routing to create-patent-search-report-ip.
---

# Tag Patent Search Results

## Role in the suite

Act as Stage 3/4 of `create-patent-landscape-overview-ip`.

Consume Stage 1 search/candidate artifacts and Stage 2 statistics/core/value evidence.
Produce the tagging design, reviewed examples, and full-pool handoff. Pause for genuine
human tagging at Stage 3.5. Validate the returned tagged pool, then route to
`create-patent-search-report-ip`.

Do not tag the complete pool automatically. Do not require `tagged_pool.csv` before
Stage 3; it is the output of the later human handoff.

## Objectives

- Define a clear, versioned four-column technology decomposition.
- Calibrate it top-down from architecture and bottom-up from patent evidence.
- Form decision-relevant technical questions for Stage 4 evolution analysis.
- Select evidence-backed patent groups for deeper reading and reporting.
- Demonstrate the tag rules on a reviewed representative sample.
- Export the complete pool with genuinely empty human tag fields.
- Validate the human-returned dataset without inventing or repairing labels silently.

This is a classification-design and workflow stage, not a full legal review, a patent
valuation, or a substitute for expert human tagging.

## Required inputs

| Artifact | Source | Use |
|---|---|---|
| `candidate_pool.csv` | Stage 1 | Stable full or explicitly bounded record universe and branch hits |
| `search_config.json` | Stage 1 | Scope, branch logic, preliminary concepts, query/version/provenance |
| `panorama_stats.json` | Stage 2 | Population patterns, organizations, technology views, normalization decisions |
| `patent_index.core.json` | Stage 2 | Reviewed branch evidence and technical-reading candidates |
| `value_signals.json` | Stage 2 | Dated candidate-level proxies and evidence states |

Optional:

- `core_recall.csv` for recall provenance;
- `tech_taxonomy.txt` as a preliminary Stage 1 hierarchy; and
- `chart_data.json` for aggregate cross-checks.

The preliminary hierarchy never overrides evidence or Stage 3 validation.

## Authoritative outputs

| Artifact | Content |
|---|---|
| `tech_breakdown.json` | Versioned four-column technology taxonomy, dictionary, validation, and rationale metadata |
| `key_questions.json` | Decision-relevant questions linked to validated nodes and evidence |
| `patent_packages.csv` | Evidence-backed reviewed patent groups and selection reasons |
| `tagging_demo_sample.csv` | Representative records with reviewed example tags and evidence |
| `to_be_tagged.csv` | Complete approved record set with empty human tag fields and handoff metadata referenced in the controlling JSON artifacts |

Do not create `taxonomy_proposal.md`; store its substantive decomposition, question,
selection, dictionary, and review rationale in the JSON metadata and handoff summary.
Do not regenerate `panorama_stats_report.html`; Stage 2 already owns it.

## Verified global MCP services

Reuse persisted upstream evidence first.

### Deep Patent Mining — recommended

- Connector key: `deep_patent_mining`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-mining
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-mining`
- Use for bounded calibration of technical problem, means, effect, material, process,
  and application when the active schema supports it.

### Patent Briefing — recommended

- Connector key: `patent_briefing`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- Use for ambiguous/selected claims, descriptions, family, status, translations, and
  images when deeper evidence is required.

### Optional gap resolution

- `advanced_patent_search` — https://open.patsnap.com/marketplace/mcp-servers/patent-search
- `global_core_patent_database` — https://open.patsnap.com/marketplace/mcp-servers/core-patents

Use optional connectors only for an approved material gap. Inspect the live schema and
record operation/request/date/provenance. Do not copy source endpoint or operation aliases.

## Step 0 — Validate and lock the Stage 3 scope

1. reconcile project/query version and data cutoff;
2. reconcile candidate row/family counts and stable identifiers;
3. reconcile Stage 2 branch IDs and organization normalization;
4. inspect preliminary taxonomy and branch-rule overlap;
5. record complete/capped/sample state;
6. define taxonomy purpose and downstream decisions;
7. define primary hierarchy versus cross-cutting tag dimensions;
8. define calibration evidence depth and bounded retrieval plan;
9. define human-review workload, authorized tool, privacy boundary, and return format;
10. preserve input versions/checksums and rollback state.

Stop if inputs come from different scopes or the human handoff cannot be authorized.

## Step 1 — Draft the taxonomy top-down

Use system architecture, function, route, subsystem, process, material, product, and
application knowledge to draft:

| Column | Meaning |
|---|---|
| `level_1` | Major technology category or system area |
| `level_2` | Route, function, subsystem, or capability |
| `level_3` | Specific taggable method, mechanism, component, material, process, or technique |
| `description` | Inclusion, exclusion, ambiguity, and why the node matters |

Use Stage 1 branches as anchors, not final taxonomy labels. Give every node a stable
machine-readable ID and human-readable English display name.

Do not impose four to six Level-1 branches or forty Level-3 nodes. Choose a hierarchy
that is discriminative, explainable, feasible to review, and useful to the decision.

## Step 2 — Calibrate bottom-up

### Select calibration evidence

Choose a reproducible sample across:

- every preliminary branch;
- high- and low-volume groups;
- ambiguous/overlap cases;
- organizations, years, languages, and jurisdictions;
- high-priority core records; and
- known near misses or unclassified records.

The source’s fifteen-to-twenty records per branch can be a planning starting point,
not a universal limit. Define a bounded plan based on evidence complexity, connector
limits, privacy, cost, context, and review risk.

### Read evidence

Use:

- `light`: title and abstract for clear calibration/demo cases;
- `standard`: title, abstract, and selected claims for ambiguity/high-priority groups;
- `deep`: claims and description only for selected cases where the taxonomy boundary
  cannot otherwise be resolved.

Record evidence source, passage/field, translation state, and reviewer state.

### Revise nodes

- add missing routes;
- merge indistinguishable nodes;
- split overloaded nodes;
- rename region-specific or opaque terminology;
- preserve ambiguous/unclassified states;
- define positive, negative, and near-miss examples; and
- version every material change and impact.

Stop calibration at the approved boundary and mark unresolved nodes. Do not fabricate
technical problem, means, effect, IPC/CPC, or classification evidence.

## Step 3 — Define label semantics

### Primary hierarchy

Primary route siblings should be mutually clear enough for consistent classification.
Do not assert strict mutual exclusivity where a patent genuinely combines routes.

### Cross-cutting dimensions

Model these separately when useful:

- product/component;
- application context;
- technical problem;
- technical means;
- technical effect;
- material/process; and
- organization or review state.

Allow multi-label values when the domain requires them. Define delimiter, duplicate-
count policy, maximum only if operationally justified, and how aggregate reports treat
multi-label records.

### Ambiguity rules

- A Level-3 label must belong to a valid Level-2 parent.
- Do not force a primary label when evidence is insufficient.
- Use `needs_review` or `unclassified` with reason.
- Preserve secondary/cross-cutting tags instead of hiding them in free text.
- Never treat Stage 1 search-rule hits as final labels.

## Step 4 — Write `tech_breakdown.json`

Use this semantic contract:

```text
nodes[]:
  node_id
  parent_id
  level_1
  level_2
  level_3
  description
  include_rules[]
  exclude_rules[]
  ambiguous_case_rules[]
  positive_examples[]
  negative_examples[]
  evidence_fields[]
  multi_label_policy
  validation_status
  example_publications[]
meta:
  taxonomy_id
  taxonomy_version
  purpose
  source_query_version
  decomposition_rationale
  calibration_method
  node_counts_by_level
  overlap_metrics
  unclassified_rate
  coverage_metrics
  change_log[]
  human_review_plan
```

Validate unique IDs, parent paths, definitions, allowed values, cycles, duplicate
labels, unresolved nodes, and version metadata.

## Step 5 — Write `key_questions.json`

Create open technical questions that seed Stage 4 evolution analysis.

Each question contains:

```text
question_id
level_1_or_cross_branch_scope
question
decision_relevance
rationale
seed_node_ids[]
expected_evidence[]
counterevidence[]
review_status
uncertainty
```

Distribute questions by decision importance and branch complexity. Do not force ten
questions or equal branch counts. A question must map to valid nodes and be answerable
through patent evidence without presuming an evolution conclusion.

## Step 6 — Write `patent_packages.csv`

### Group logic

Organize groups by a priority node, route, technical question, product/application,
organization comparison, or technical problem. Declare the logic.

### Selection dimensions

Preserve the source’s six prompts as optional analyst hypotheses:

- materially different/disruptive technology;
- new application context;
- possible unaddressed user/system need;
- substantial reported performance change;
- new function; and
- new interaction mode.

These prompts do not establish legal novelty, inventiveness, technical superiority,
demand, adoption, value, or licensing suitability.

Also consider technical relevance, route representativeness, evidence depth, family/
citation/status proxies, organization diversity, missing data, and review workload.

Do not require ten groups or three families each. Preserve sparse groups and state why.

### Columns

```text
package_id,package_basis,sub_domain,node_ids,family_id,representative_publication,
title,normalized_assignee,recommendation_reason,rubric_dimensions,value_signal,
evidence_ids,selection_limitations,review_status,next_review_action
```

Use review states such as `abstract_based`, `claim_assisted`, `description_reviewed`,
and `needs_review`. Keep family/status/citation data dated and source-labeled.

## Step 7 — Write `tagging_demo_sample.csv`

Choose enough records to demonstrate:

- each major primary branch;
- cross-cutting and multi-label behavior;
- boundary/near-miss cases;
- `unclassified`/`needs_review` states;
- different evidence depths; and
- common tagging errors.

Do not force twenty to thirty rows. Use a sample that teaches the taxonomy and remains
reviewable.

Use columns:

```text
record_id,publication_number,title,abstract,normalized_assignee,
tech_level_1,tech_level_2,tech_level_3,technical_problem,technical_means,
technical_effect,recommendation_level,evidence_text,evidence_source,
taxonomy_version,review_status,review_notes
```

Every filled tag must exist in the controlled dictionary and have traceable evidence.

## Step 8 — Write `to_be_tagged.csv`

Export the complete approved candidate set using deterministic local file processing.
Do not load every row into model context.

Use the same core column layout as the demo, plus any required traceability fields.
Keep human tag fields empty:

- `tech_level_1`;
- `tech_level_2`;
- `tech_level_3`;
- `technical_problem`;
- `technical_means`;
- `technical_effect`;
- human recommendation/review fields.

Do not prefill them from branch-rule hits or machine suggestions. Machine suggestions,
if explicitly requested, must use separate columns and must not masquerade as human tags.

### CSV safety

- Use UTF-8 and a documented delimiter/quote/newline policy.
- Preserve stable record and family IDs and source order.
- Neutralize formula-leading values for spreadsheet/tool safety.
- Reject or escape embedded control characters and delimiter conflicts.
- Do not include secrets, unnecessary personal data, or unauthorized confidential text.
- Reconcile row count and identifier set against the approved candidate pool.

Record taxonomy/schema version, required/optional columns, allowed values, multi-label
delimiter, row count, identifier checksum, file checksum, generation date, privacy
boundary, and return instructions in `tech_breakdown.json.meta` and the handoff summary.

## Step 9 — Validate Stage 3 outputs

### Taxonomy

- IDs and parents are valid and versioned.
- Every node has definition/include/exclude/ambiguity guidance.
- Primary overlaps and cross-cutting multi-label policies are explicit.
- Coverage, overlap, and unclassified metrics are reported.
- No unsupported node or technical fact is fabricated.

### Questions and groups

- Every question maps to valid seed nodes and has uncertainty/counterevidence.
- Every selected family has traceable reason/evidence and review state.
- Sparse evidence is visible; no quota drives invented groups or records.
- Analyst rubric prompts are not represented as legal or market conclusions.

### Demo and handoff

- Demo values exist in the dictionary and cover material boundary cases.
- Full handoff contains every approved record exactly as intended.
- Human tag columns are empty.
- CSV encoding, quoting, delimiter, formula safety, IDs, row count, and checksums pass.
- Output schemas and taxonomy versions reconcile.

## Stage 3.5 — Genuine human tagging boundary

After all five Stage 3 outputs validate:

1. provide `to_be_tagged.csv`, taxonomy dictionary/version, demonstration sample, and
   instructions to the authorized user/reviewer;
2. the user imports them into an approved tagging/data tool under their privacy and
   access controls;
3. authorized human reviewers classify the full approved pool;
4. the user returns the result as `tagged_pool.csv`; and
5. do not proceed to Stage 4 until the return validates.

Do not require a specific regional tagging product. Do not upload or send the file
without explicit authorization.

## Validate `tagged_pool.csv`

Check:

- expected filename, encoding, delimiter, columns, and taxonomy/schema version;
- file/identifier checksum and row-count reconciliation;
- stable record/family ID uniqueness and coverage;
- missing, duplicate, unexpected, and reordered records;
- allowed values and parent-child consistency;
- multi-label delimiter and duplicate behavior;
- evidence/review fields and unresolved states;
- formula/control-character safety;
- unexpected machine-filled versus human-reviewed fields; and
- privacy/security boundary.

Produce a validation summary with accepted/rejected row counts and issue categories.
Do not silently coerce invalid labels, fill missing tags, drop rows, or change taxonomy
version. Return failures to the authorized human reviewer.

## Handoff to Stage 4

When the return validates, provide:

```text
Stage 3 complete: taxonomy [id/version], [node counts], [question count],
[package/family counts], demo [row count].
Stage 3.5 accepted: tagged_pool.csv [row/family counts], [unresolved count],
schema/taxonomy [versions], checksum [recorded].
Route to create-patent-search-report-ip with all Stage 1–3.5 artifacts.
```

Do not create the Stage 4 report here.

## Quality gate

- All required Stage 1/2 artifacts reconcile.
- No preexisting `tagged_pool.csv` is required to begin Stage 3.
- Exactly five authoritative Stage 3 outputs are created.
- Taxonomy rationale is preserved in JSON metadata, not an extra package/runtime file.
- Level counts and question/package/demo sizes are evidence-driven rather than quotas.
- Primary and cross-cutting/multi-label dimensions are clearly separated.
- Every demonstration/package tag and reason is traceable.
- Full-pool processing is deterministic and does not load every row into context.
- Human tag fields remain genuinely empty before Stage 3.5.
- Returned-pool validation passes before Stage 4.
- No Stage 2 snapshot or Stage 4 report is regenerated.

## Stop conditions

Stop or narrow when:

- upstream artifacts conflict or cannot be parsed;
- taxonomy purpose or human-review capacity is undefined;
- calibration evidence cannot distinguish key nodes;
- connector limits or confidential-data rules prevent necessary evidence retrieval;
- a package/question/demo would require fabricated evidence;
- full-pool export cannot preserve safe stable identifiers;
- no authorized human tagging workflow exists;
- returned rows/versions/checksums/tags fail reconciliation; or
- the user requests automated full-pool tagging as if it were human validation.

Return completed artifacts, failed checks, affected rows/nodes, residual risk, and the
exact next action. Do not bypass the Stage 3.5 boundary.
