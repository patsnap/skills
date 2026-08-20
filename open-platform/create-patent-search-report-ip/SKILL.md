---
copyright: "Copyright © Patsnap. All rights reserved."
name: create-patent-search-report-ip
description: Create the final evidence-backed patent-landscape insight report from validated search, statistics, taxonomy, patent-package, and human-tagging artifacts. Use at Stage 4/4 of the create-patent-landscape-overview-ip suite to aggregate a large tagged patent pool safely, synthesize technology evolution and branch-level value signals, translate patent-package evidence into bounded user actions, and write report_manifest.json plus one self-contained scientific HTML report.
---

# Create a Patent Search Report

## Role in the suite

Act as Stage 4/4, the reporting and synthesis stage of
`create-patent-landscape-overview-ip`.

Upstream stages are:

1. `search-patents-ip` — validated scope and candidate records.
2. `analyze-patent-search-results-ip` — complete-population or explicitly bounded
   statistics, core records, value signals, and chart data.
3. `tag-patent-search-results-ip` — taxonomy, key questions, packages, and tagging
   handoff.
4. Human Stage 3.5 — validated return of `tagged_pool.csv` when performed.

Turn those artifacts into a decision-readable report. Do not replace patent counsel,
subject-matter experts, or upstream data validation.

## Questions this stage answers

- Which findings matter to the stated product, R&D, strategy, or IP decision?
- Which activity patterns, organizations, branches, and patent groups deserve attention?
- How does the evidence suggest that technical routes have changed over time?
- Where do multiple dated patent-value proxies concentrate by branch?
- What can a user reasonably monitor, read, compare, validate, or refer for review?
- Which claims remain uncertain because data, tagging, or expert review is incomplete?

## Preconditions

Use this stage only when:

- the user has confirmed report objective and audience;
- Stage 1 search scope is validated;
- Stage 2 statistics and provenance are available;
- Stage 3 taxonomy/package artifacts or a sufficiently rich human-tagged pool are
  available; and
- the output environment permits creation of `report_manifest.json` and `report.html`.

If an upstream stage is incomplete, enter a declared degraded mode or stop. Do not
invent the missing artifact.

## Authoritative artifact contract

The suite has no packaged `ARCHITECTURE.md`. Use this embedded contract.

### Stage 1 inputs

| Artifact | Required content |
|---|---|
| `search_config.json` | Scope, queries, exclusions, date/language/jurisdiction fields, unit, query version, connector provenance |
| `candidate_pool.csv` | Candidate records with stable IDs and retrieval/screening state |
| `core_recall.csv` | Known-relevant/near-miss controls and recall-review evidence |

### Stage 2 inputs

| Artifact | Required content |
|---|---|
| `panorama_stats.json` | Trends, organizations, jurisdictions, status signals, technology distributions, and competitor profiles supported by the population boundary |
| `patent_index.core.json` or equivalent source-authorized core format | Reviewed and tiered representative patents, branch IDs, evidence provenance |
| `value_signals.json` | Candidate-level dated proxy signals and verification state |
| `chart_data.json` | Chart-ready aggregates with measure, unit, date basis, cutoff, scope, and limitations |
| `panorama_stats_report.html` | Stage 2 statistical snapshot; never substitute it for this insight report |

### Stage 3 inputs

| Artifact | Required content |
|---|---|
| `tech_breakdown.json` | Versioned technology taxonomy and four-column decomposition |
| `key_questions.json` | Decision-relevant questions, branch/node seeds, rationale, and review status |
| `patent_packages.csv` | Evidence-backed patent groups, selection rubric, rationale, and review status |
| `tagging_demo_sample.csv` | Reviewed example tags and boundary cases |
| `to_be_tagged.csv` | Human-tagging input and schema/version metadata |

### Human Stage 3.5 input

| Artifact | Required content |
|---|---|
| `tagged_pool.csv` | Returned complete or explicitly bounded pool, validated taxonomy tags, technical fields, family IDs, assignee, dates, status/signals, schema/taxonomy version, row count, encoding, and reconciliation data |

### Stage 4 outputs

| Artifact | Content |
|---|---|
| `report_manifest.json` | Mode, scope, input versions/checksums, section-to-source map, evidence register, derived-field rules, limitations, output inventory, and QA state |
| `report.html` | One offline, self-contained, accessible scientific/executive insight report |

Create `report_manifest.json` only at Stage 4. Do not expect a Stage 2 manifest with
the same name. Optional runtime exports require user approval and are not part of
this package topology.

## Verify inputs before synthesis

For every available artifact:

1. confirm exact path and readable format;
2. record file size, row/object count, checksum when supplied or practical;
3. validate schema and version;
4. reconcile project, query, taxonomy, family, and data-cutoff identifiers;
5. reconcile candidate, deduplicated, tagged, and reported counts;
6. identify missing columns, null patterns, and conflicting values;
7. preserve the previous accepted version for rollback; and
8. record validation status in the manifest.

Stop if material inputs belong to different scopes or versions and cannot be
reconciled.

## Reporting modes

### Mode A — validated tagged-pool driven

Use when `tagged_pool.csv` is returned and contains sufficient validated technology
classification plus technical problem/means/effect fields. Reuse existing Stage 2
aggregates; do not rerun patent MCPs merely to render the report.

Inputs:

- `tagged_pool.csv` as the classification and technical-evidence body;
- `panorama_stats.json`, `value_signals.json`, `patent_index.core.*`, and
  `chart_data.json` as validated Stage 2 evidence; and
- Stage 3 artifacts when available.

If Stage 3 questions/packages are absent, derive provisional route and package views
from the tagged pool under the rules below. Label them `automated_derivation`, not
human-rubric output.

### Mode B — full Stage 3 contract

Use when `tech_breakdown.json`, `key_questions.json`, and `patent_packages.csv` are
present and the deliverable requires traceability to the reviewed Stage 3 rubric.
Combine them with the tagged pool and Stage 2 evidence.

### Degraded mode — statistics and reviewed packages only

Use only if `tagged_pool.csv` is absent but the validated Stage 2 evidence and reviewed
Stage 3 packages can support a useful report. Prominently state:

```text
Human-tagged population unavailable. Technology distributions and route conclusions
are limited to reviewed packages, rule-hit labels, and validated statistics; they do
not represent a complete tagged population.
```

Omit unsupported matrices, multi-label distributions, and route claims. Do not fill
them from titles alone.

## Adapt the tagged-pool schema

Inspect the header before processing. Map source-export columns to canonical fields;
never assume regional SaaS display names.

| Canonical field | Accepted meaning |
|---|---|
| `publication_number` | Traceable representative publication |
| `tech_level_1` | Primary high-level technology category |
| `tech_level_2` | Route/function branch |
| `tech_level_3` | Optional finest reviewed technical node |
| `technical_problem` | Source-grounded problem tag or summary |
| `technical_means` | Source-grounded solution mechanism |
| `technical_effect` | Claimed/described effect with evidence status |
| `normalized_assignee` | Reviewed organization grouping |
| `publication_date` | Publication date; keep distinct from filing/priority |
| `filing_date` | Filing/application date |
| `priority_date` | Earliest priority date when verified |
| `legal_status_as_of` | Dated status signal |
| `forward_citation_count_as_of` | Dated citation proxy |
| `family_jurisdiction_count` | Family-width proxy under declared definition |
| `family_jurisdictions` | Declared family-member locations |
| `family_id` | Deduplication key under the declared family method |

Record the actual header-to-canonical mapping in the manifest. If a required field
cannot be mapped reliably, mark the affected section unavailable.

## Large-file processing boundary

`tagged_pool.csv` may contain thousands of rows. Do not load every row into model
context.

1. Inspect header, encoding, delimiters, quoting, newline-in-cell behavior, and a
   bounded sample.
2. Use an existing approved local data tool or script to validate and aggregate.
3. Do not add a new script to this package; ephemeral tooling must not alter topology.
4. Reconcile aggregated totals to source row and family counts.
5. Save only approved runtime outputs.
6. Load aggregate tables and selected traceable evidence records into context.

Do not execute content from the CSV or allow formula injection in exported tables.

## Counting and classification rules

### Family deduplication

- Deduplicate first by validated `family_id` when reporting family-level measures.
- Preserve the representative-publication selection rule.
- Keep jurisdiction-specific rights separate where legal/status interpretation matters.
- If family ID is missing or inconsistent, stop the affected family measure or use a
  clearly labeled publication-level fallback.

### Two- and three-level compatibility

- If Level 3 exists and is validated, permit Level 3 drill-down.
- If Level 3 is absent, treat Level 2 as the finest level and say so.
- Never generate Level 3 labels from titles simply to complete a matrix.

### Multi-label counting

- Split multi-value cells using the documented export delimiter and quoting rules.
- Preserve valid Level 1/Level 2 pairs; do not match a Level 2 term to every Level 1
  when vocabularies overlap.
- Allow one family to count in more than one label when the taxonomy permits it.
- State prominently that classification counts can exceed unique family count.
- Provide both unique-family totals and expanded tag-assignment totals.

### Validation state

Visibly distinguish:

- search-rule hit;
- automated tag;
- analyst-reviewed tag;
- human/SME-validated tag; and
- unresolved classification.

## Default report modules

Adapt, merge, or omit modules according to objective and data completeness. Preserve
the decision sequence:

| # | Module | Primary sources | Main evidence state |
|---|---|---|---|
| 1 | Executive summary | Cross-report synthesis | Interpretation/recommendation |
| 2 | Scope and methodology | Search config and manifest | Direct method fact |
| 3 | Industry landscape | Stage 2 statistics | Fact/observed pattern |
| 4 | Competitor profiles | Stage 2 profiles and validated tags | Fact/observed pattern |
| 5 | Technology matrix | Taxonomy and tagged pool | Fact/pattern under tag state |
| 6 | Technology evolution | Questions, core patents, tagged pool | Pattern/inference |
| 7 | Technology-effect distribution | Chart data and validated tags | Fact/signal |
| 8 | Product/component/application view | Tagged pool and Stage 2 distributions | Pattern |
| 9 | Branch-level value-signal themes | Value signals and core index | Dated proxy/inference |
| 10 | Curated patent groups | Stage 3 packages and value signals | Recommendation |
| 11 | Risks and limitations | All inputs and validation log | Boundary |
| 12 | Appendix and data assets | Manifest and input inventory | Reproducibility |

Place technology evolution immediately after the technology matrix. Explain signal
themes before user actions and patent groups.

## Module 6 — Technology evolution

### Evidence chain

Build each route as:

```text
versioned branch/question → time-bounded family evidence → technical problem/means/effect
→ observed change → alternative explanation → bounded route interpretation
```

### Summary hierarchy

Include:

| Level | Field | Content |
|---|---|---|
| Section | `evolution_overview` | Cross-branch observations: acceleration, continuity, convergence, divergence, or emerging attention, each qualified |
| Route | `route_summary` | One sentence describing the observed earlier/current/recent technical emphasis without inventing continuity |
| Phase | `phase_caption` | Evidence-grounded technical characteristics and organizations for that period |

### Select route evidence

In Mode B, map `key_questions.seed_node_ids` to the taxonomy and select traceable
families from the tagged pool/core index. In Mode A without key questions:

1. use validated Level 1 branches as provisional routes;
2. identify dominant valid Level 1/Level 2 pairs by declared measure;
3. select representative families that match both paired levels;
4. segment time according to the dataset and decision—quantiles, technology eras,
   or explicit periods—not fixed calendar years;
5. consider technical relevance, evidence depth, date, and diversity;
6. prevent accidental family reuse when it would distort comparison; and
7. disclose any algorithmic diversity/organization rotation as a sampling choice,
   not evidence of actual market entry timing.

Do not require three families or three non-empty phases. Show sparse/empty periods.

### Turning points

Use controlled types only when evidence supports them:

- route branching;
- notable disclosure;
- organization entry in the observed dataset;
- disclosed performance or capability change; and
- application-context shift.

Each `turning_point` contains `type`, `note`, evidence IDs, date basis, and uncertainty.
Generate its note from the selected family’s problem/means/effect evidence. Do not
invent a transition between records.

### Visualization

Use accessible HTML/CSS/SVG timelines or small multiples. Each route shows date basis,
family IDs/publications, organization, validated node, evidence state, and sparse-data
qualification. Static text must convey the finding without interaction.

## Module 7 — Technology-effect distribution

Build a technical-means × reported-effect matrix from validated upstream chart data
or tagged-pool aggregation.

- Define row, column, cell measure, unit, multi-label policy, tag state, and cutoff.
- Use family count only after validated family deduplication.
- Distinguish claimed/described effects from independently demonstrated performance.
- Represent unavailable cells separately from observed zero.
- Do not call a combination “insignificant” merely because the dataset has no records.
- Use an accessible heatmap/table or bubbles with a tabular alternative.

## Module 9 — Branch-level value-signal themes

Aggregate candidate-level proxies in `value_signals.json` by validated `branch_id`.
Possible dimensions include dated citation, family breadth, legal-status, organization
concentration, transaction/assertion-event, and portfolio-priority signals.

For each dimension record:

- definition and source;
- verified versus recall-proxy state;
- date/cutoff and jurisdiction coverage;
- normalization and missing-data treatment;
- aggregation function and denominator; and
- sensitivity to outliers or branch size.

Describe results as “higher observed signal concentration under this dataset” or
“lower observed signal density.” Do not call the score patent value, moat strength,
defensibility, blue ocean, freedom to operate, availability, or market opportunity.

Prefer bars, dot plots, or a signal matrix. Avoid radar charts when dimensions have
unlike scales or missing values.

## Module 10 — Curated patent groups

### Preserve analyst evidence

Retain Stage 3 `recommendation_reason`, rubric dimensions, evidence IDs, review status,
and all limitations in the manifest/evidence layer.

### Translate into bounded user actions

For each family add:

| Field | Meaning |
|---|---|
| `use_case` | Evidence-supported next action such as read, monitor, compare, technical reference, data validation, or counsel/commercial review |
| `purpose_tag` | Controlled action category approved for this report |
| `answers_question` | Link to a validated key question when the mapping exists |
| `package_summary` | What the group addresses, why it matters, and which records to start with |

Do not hard-code the source’s five Chinese action labels. Define an English controlled
vocabulary appropriate to the objective. Never translate proxies into “design-around,”
“licensing candidate,” “acquire,” “enforce,” or “FTO action” without qualified review.

### Mode A provisional package derivation

If `patent_packages.csv` is absent:

1. derive candidates by validated finest branch;
2. rank with disclosed relevance, evidence-depth, family/citation/status proxies;
3. treat missing proxy data explicitly;
4. test for age, organization, and family-size bias;
5. select only supported records rather than a fixed two-to-three quota;
6. label the group `automated_derivation`; and
7. require human review before any transaction, legal, or portfolio action.

When no `key_questions` mapping exists, leave `answers_question` unresolved. Do not
fabricate a question link.

### Two-layer rendering

Main layer:

- decision-readable action;
- purpose tag;
- linked question if verified; and
- package summary.

Expandable evidence layer:

- original rubric/reason;
- family, citation, status, organization, and review signals;
- evidence IDs and provenance; and
- limitations/legal boundary.

The report must remain understandable when expandable controls are not used or when
printed.

## Evidence model

Use:

| Level | Meaning |
|---|---|
| L1 | Direct, source-backed data or method fact |
| L2 | Observed pattern in the defined dataset |
| L3 | Analytical interpretation with alternatives and uncertainty |
| L4 | Business/R&D/IP workflow recommendation |
| L5 | Legal, transaction, status, or risk signal requiring specialist review |

Every material claim maps to one or more evidence entries. A manifest evidence entry
contains:

```json
{
  "evidence_id": "E-001",
  "level": "L2",
  "claim": "[bounded observation]",
  "source_file": "[validated upstream artifact]",
  "source_field": "[field or aggregate]",
  "record_ids": ["[traceable IDs]"],
  "counting_method": "[unit, deduplication, multi-label policy]",
  "data_cutoff": "[YYYY-MM-DD]",
  "validation_state": "[verified/proxy/reviewed/unresolved]",
  "limitations": "[material boundary]"
}
```

Do not include confidential examples in the Skill package.

## `report_manifest.json` contract

Include:

- report ID, version, generated date, objective, audience, and mode;
- scope, jurisdictions, date basis, unit, family definition, and data cutoff;
- every input path, artifact version, checksum/size/count, validation result;
- header/column mappings and transformations;
- section order and section-to-source/evidence mapping;
- evolution overview, routes, summaries, phases, and turning points;
- branch signal definitions and aggregations;
- package summaries, bounded use cases, purpose tags, question links, original reasons;
- evidence register;
- degraded/automated/proxy flags;
- limitations and unresolved items;
- output paths and QA results; and
- no secret, API key, raw confidential payload, or absolute user path.

Write atomically when possible. Validate JSON before handoff.

## `report.html` design contract

### Information architecture

- Start with title, decision objective, mode, scope, date basis, family unit, cutoff,
  sources, and limitations.
- Make executive findings evidence-linked and action-bounded.
- Place each visualization next to its claim and qualification.
- Preserve the default module sequence unless an approved audience need changes it.
- End with reproducibility assets and legal/data boundaries.

### Scientific/executive visual system

- Use a white/neutral canvas, dark navy/slate hierarchy, restrained teal data accent,
  amber qualifications, and red only for real escalation.
- Use system fonts; do not rely on regional or remote fonts.
- Prefer whitespace, rules, and typography over nested cards.
- Use flat 2D bars, lines, heatmaps/tables, timelines, and evidence cards.
- Avoid decorative hero sections, gradients, stock imagery, 3D charts, visual drama,
  and vendor-interface imitation.
- Pair color with labels or symbols and maintain accessible contrast.

### Technical safety

- Deliver one HTML file with inline CSS and pre-aggregated data.
- Prefer static HTML/CSS/SVG; allow minimal inline JavaScript only as progressive
  enhancement with a complete non-script fallback.
- Use no external CDN, D3, font, image, iframe, tracker, or network dependency.
- Escape all user and retrieved content.
- Permit only validated safe URLs and add `rel="noopener noreferrer"` to new-tab links.
- Do not execute or interpolate raw CSV/JSON content as code.
- Prevent spreadsheet-formula and HTML/script injection in displayed/exported values.

### Accessibility and print

- Use semantic landmarks, ordered heading levels, table headers/captions, visible focus,
  keyboard-safe controls, and text equivalents for charts.
- Keep wide tables horizontally scrollable and long identifiers break-safe.
- Respect reduced motion and avoid animation needed for meaning.
- Ensure collapsed evidence is visible or summarized in print.
- Verify desktop, narrow viewport, grayscale, and PDF/print layouts.

### Chart captions

Every quantitative view states:

- question and bounded takeaway;
- measure and denominator;
- date field and period;
- unit/family definition;
- scope and cutoff;
- multi-label duplicate-count policy;
- validation/proxy state; and
- material limitation.

Show unavailable data rather than a fake or zero-valued chart.

## MCP boundary

Stage 4 normally reuses validated upstream artifacts. Do not rerun MCPs merely to
recreate existing statistics.

If an approved material evidence gap requires retrieval, use only the installed live
schema of these verified global connectors:

- `advanced_patent_search` — https://open.patsnap.com/marketplace/mcp-servers/patent-search
- `patent_briefing` — https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- `deep_patent_mining` — https://open.patsnap.com/marketplace/mcp-servers/patent-mining
- `global_core_patent_database` — https://open.patsnap.com/marketplace/mcp-servers/core-patents

Record why the gap could not be resolved from upstream artifacts and how new evidence
was reconciled. Do not use source endpoint aliases as connector names.

## Legal and analytical boundaries

Do not provide:

- formal freedom-to-operate or infringement opinions;
- patent validity, novelty, or inventive-step opinions;
- standards-essentiality opinions;
- legal claim-scope conclusions;
- patent valuation or transaction recommendations;
- product-launch or market-adoption certainty; or
- unsupported business conclusions.

Use language such as “under the defined dataset,” “the patent evidence suggests,”
“observed proxy concentration,” and “requires technical, commercial, or legal review.”

## Quality gate

### Input and mode

- Every required input exists or the mode declares its absence.
- Schema, version, count, checksum, scope, taxonomy, family, and cutoff reconcile.
- Mode A, Mode B, or degraded mode is explicit at the top and in the manifest.
- No large tagged pool was loaded row-by-row into context.

### Data and synthesis

- Family and multi-label counting rules are applied and disclosed.
- Population, sample, core set, package, and representative records are distinct.
- Evolution periods derive from the dataset and contain no fabricated transition.
- Turning points cite their family and technical evidence.
- Value themes expose proxy definitions, missing data, aggregation, and limitations.
- Package actions are bounded and preserve original Stage 3 evidence.

### Evidence and law

- Every material claim maps to evidence IDs.
- Facts, patterns, interpretations, recommendations, and legal signals are distinct.
- Status/citation/family/transaction values are dated and source-labeled.
- No moat, blue-ocean, design-around, licensing, FTO, validity, or value conclusion is
  inferred from proxies.

### Outputs

- `report_manifest.json` is valid, complete, and contains no secrets/absolute paths.
- `report.html` opens offline and contains all promised sections or explicit omissions.
- HTML has no missing assets, remote dependencies, unsafe content, broken links,
  inaccessible controls, blank charts, overlap, clipping, or print loss.
- Section/evidence counts reported in the handoff match the files.

## Handoff

After writing and validating both outputs, return control to
`create-patent-landscape-overview-ip`. Report:

```text
report.html written ([section count] sections, [chart count] charts);
report_manifest.json written ([evidence count] evidence entries).
Mode: [A/B/degraded]. Unresolved: [count and summary].
```

Do not paste the full HTML into the conversation unless the user asks.

## Stop conditions

Stop or degrade when:

- upstream artifacts are missing, incompatible, or from different scopes;
- `tagged_pool.csv` cannot be parsed or reconciled;
- family or taxonomy identifiers are unreliable for a requested measure;
- a population claim is unsupported by complete retrieval/aggregation;
- a required route, value, or package conclusion would need fabricated evidence;
- confidential data cannot be processed safely;
- the report cannot be written or validated in the authorized workspace; or
- a requested conclusion requires expert legal or commercial review.

Return the completed sections, failed validation, affected claims, and exact next step.
Do not silently omit a failed section.

