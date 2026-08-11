---
name: identify-patent-commercialization-opportunities-ip
description: Assess a narrowly defined technology opportunity through reproducible patent searches, full-scope metrics, representative patent evidence, transparent scoring, and an offline multi-page decision report. Use when a user asks whether a specific technical route merits further R&D, licensing, partnering, or commercialization diligence.
---

# Identify Patent Commercialization Opportunities

## Purpose

Turn a well-bounded technology question into an evidence-backed patent opportunity assessment.
The result supports R&D, licensing, partnering, and portfolio-screening decisions.
It is a patent-intelligence assessment, not investment, legal, valuation, or freedom-to-operate advice.

## Trigger conditions

Use this skill when the user asks to:

- assess the patent opportunity around a specific technology;
- decide whether a technical route deserves deeper R&D or commercialization diligence;
- examine patent activity, maturity, crowding, or white space in a narrow field;
- identify representative patents and evidence behind an opportunity hypothesis;
- produce a structured patent opportunity report for a decision meeting.

Do not trigger on a broad label such as “artificial intelligence,” “batteries,” “semiconductors,”
“biotechnology,” or “materials” without a technical mechanism, application, or boundary.
First narrow the subject using `references/prompts/input_scoping_prompt.md`.

## Required outcome

Create a reproducible assessment whose conclusions can be traced to:

1. a documented scope;
2. disclosed search logic;
3. full-population or reproducibly bucketed metrics;
4. a separately labelled representative patent set;
5. claim-level evidence links;
6. explicit limitations and unavailable metrics;
7. a complete ten-file report package.

## Non-negotiable evidence rules

### Full scope and representative records are different datasets

Never use a relevance-ranked patent sample to calculate:

- filing or publication trends;
- applicant rankings;
- jurisdiction shares;
- legal-status distributions;
- subfield shares;
- concentration metrics;
- market or portfolio-wide conclusions.

Use full-population aggregation returned by a verified tool, or use complete reproducible buckets.
If neither method is available, mark the metric `Unavailable` and explain why.
Do not substitute a Top-K sample.

### Representative patents are evidence, not a census

Retrieve up to 50 high-relevance records for evidence review.
Target at least 20 valid records where the search results support that number.
If fewer exist, include all valid records and disclose the shortfall.
Never fabricate records or pad the set with weakly related patents.

### Every material conclusion needs a traceable claim

Assign a stable `claim_id` to each decision-relevant conclusion.
Connect it to the metric, search, patent, or limitation that supports it.
Capture uncertainty and contrary evidence as well as supportive evidence.

### Commercial language must remain qualified

Patent evidence can indicate activity, crowding, momentum, maturity, or technical white space.
It cannot by itself prove market demand, commercial viability, profitability, valuation, or FTO.
Use calibrated language such as “supports further diligence” or “does not yet support prioritization.”

## Inputs

### Required

- a narrowly defined technology topic or technical solution;
- the decision context: R&D, licensing, partnering, portfolio review, or another stated use;
- the relevant application or use environment, when material.

### Resolve before searching

- included and excluded technical concepts;
- synonyms, abbreviations, spelling variants, and adjacent concepts;
- relevant patent classifications;
- priority-date or publication-date window;
- jurisdiction or regional benchmark, if requested;
- patent-family counting rule;
- status rule and reporting cutoff date;
- whether results should emphasize patent families, publications, or applications.

### Defaults when the user does not specify them

- use a decision-relevant global scope rather than a fixed country comparison;
- define a recent and historically meaningful date window for the technology;
- count one representative record per simple family for portfolio-level analysis;
- state the reporting cutoff date;
- disclose every assumed boundary in the methodology.

## Verified PatSnap MCP services

Use the English interface and English output.
Do not invent tool names, parameters, aggregations, or response fields.

### Required: Advanced Patent Search

- Connector key: `advanced_patent_search`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`
- Role: construct and run patent searches, retrieve matched totals, and obtain representative records.

### Required: Patent Briefing

- Connector key: `patent_briefing`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- Role: inspect important patents and create concise evidence-grounded briefs.

### Recommended: Deep Patent Mining

- Connector key: `deep_patent_mining`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-mining
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-mining`
- Role: deepen technical, family, citation, and portfolio review where supported by the live schema.

### Optional: Global Core Patent Database

- Connector key: `global_core_patent_database`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/core-patents
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/core-patents`
- Role: validate core bibliographic or family information when the available connector supports it.

If a connector is unavailable, continue only with evidence that can still be reproduced.
Mark affected metrics and modules unavailable; do not simulate missing MCP output.

## Workflow

### Phase 0 — Normalize and approve the analytical scope

Load `references/prompts/input_scoping_prompt.md`.

1. Parse the technology, mechanism, application, and decision context.
2. Draft inclusion and exclusion rules.
3. Build an English-first synonym and classification concept map.
4. Identify ambiguous terms and false-positive risks.
5. Choose the date, jurisdiction, family, and status conventions.
6. Record assumptions that materially affect interpretation.

Proceed without stopping for confirmation when the user has delegated the full analysis and the assumptions are low risk.
Ask only when a missing boundary would materially change the research question.

### Phase 1 — Build the search strategy

Load `references/prompts/search_strategy_prompt.md`.

1. Create a broad discovery query.
2. Inspect terminology and classifications from valid results.
3. Create a precision query with explicit exclusions.
4. Test known relevant and irrelevant concepts.
5. Record the final query syntax and query version.
6. Record search date, database, filters, and matched total.

Do not rely on a single keyword.
Do not silently change the query after analysis begins.
Version and explain every material revision.

### Phase 2 — Collect full-scope metrics

Load `references/prompts/full_scope_metrics_prompt.md`.

Collect only metrics that can be produced from a complete result population or reproducible complete buckets.
Possible metrics include:

- annual filing or publication counts;
- counts for explicitly defined regional benchmarks;
- independent counts for mutually documented technical subfields;
- total matched records and family counts;
- any verified aggregation exposed by the live connector.

For a trend series, run and preserve one complete date bucket per period when a direct aggregation is unavailable.
For a subfield series, run and preserve one complete scoped query per subfield.
Do not sum overlapping subfields and label the sum as a unique population.

For every metric, capture:

- `metric_id`;
- definition and unit;
- population and counting rule;
- query or filter;
- time coverage and cutoff;
- value or series;
- source connector;
- retrieval timestamp;
- limitations.

### Phase 3 — Retrieve representative patent evidence

Use the final approved scope and search strategy.

1. Retrieve relevance-ranked records from Advanced Patent Search.
2. Deduplicate consistently using the selected family rule.
3. Retain up to 50 valid representative records.
4. Validate identifiers, titles, applicants, dates, jurisdictions, and status fields when available.
5. Use Patent Briefing for patents that materially support or challenge the assessment.
6. Preserve stable source links where the connector returns them.

Label the dataset `representative_evidence_sample`.
Never call it the full landscape.

### Phase 4 — Analyze the opportunity

Load these prompts in order:

1. `references/prompts/applicant_analysis_prompt.md`
2. `references/prompts/trend_analysis_prompt.md`
3. `references/prompts/subfield_analysis_prompt.md`
4. `references/prompts/scoring_prompt.md`
5. `references/prompts/evidence_mapping_prompt.md`

Applicant analysis must distinguish verified population aggregation from observations in representative records.
Trend analysis must distinguish filing behavior from publication lag.
Subfield analysis must disclose overlaps and residual categories.
Scoring must expose dimensions, weights, missing-data treatment, and uncertainty.
Evidence mapping must include supportive, neutral, limiting, and contradictory evidence.

Assess six decision dimensions when evidence allows:

1. patent activity and momentum;
2. technical maturity;
3. competitive intensity;
4. white-space clarity;
5. evidence quality and reproducibility;
6. strategic fit with the stated decision context.

Do not convert missing evidence into a neutral score.
Remove and renormalize missing dimensions, and report the missing weight.

### Phase 5 — Write the structured data outputs

Create the following files in this order and verify each write before continuing:

1. `full_scope_metrics.json`
2. `patent_records.json`
3. `evidence_mapping.csv`

`full_scope_metrics.json` must separate definitions, queries, values, unavailable metrics, and limitations.
`patent_records.json` must declare that it is a representative evidence sample and state the family rule.
`evidence_mapping.csv` must contain at least these columns:

```text
claim_id,claim_text,data_source,data_value,supporting_patents,evidence_strength,reasoning,limitations
```

Target at least ten decision-relevant claims when the evidence supports them.
Do not fabricate claims to satisfy a row count.

### Phase 6 — Render the five-page offline report

Load `references/prompts/html_report_generation_prompt.md`.
Render the templates in this order, verifying each file after it is written:

1. `references/templates/index_template.html` → `index.html`
2. `references/templates/patents_template.html` → `patents.html`
3. `references/templates/subfields_template.html` → `subfields.html`
4. `references/templates/evidence_template.html` → `evidence.html`
5. `references/templates/methodology_template.html` → `methodology.html`

The five pages must share navigation, terminology, scope, cutoff date, and visual language.
All report assets must work offline.
Use system fonts, semantic HTML, accessible tables, and static SVG where a chart adds value.
Do not load remote fonts, chart libraries, analytics, or other CDN resources.
Do not insert untrusted data through unsafe HTML operations.

The overview must preserve all fifteen analytical modules:

1. decision headline;
2. scope and cutoff;
3. overall opportunity score;
4. six-dimension score profile;
5. full-scope trend;
6. regional benchmark, if verified;
7. subfield distribution;
8. applicant or assignee view, if verified;
9. legal-status view, if verified;
10. representative patents;
11. technical white space;
12. supporting evidence;
13. risks and limitations;
14. recommended next diligence;
15. source and reproducibility summary.

When a module lacks valid data, show a clear unavailable state or omit the chart while preserving the explanation.
Never render an empty chart or placeholder as if it were evidence.

### Phase 7 — Complete documentation and quality assurance

Render `references/templates/README_template.md` as `README.md` for the generated report package.
Load `references/prompts/quality_check_prompt.md` and record the result in
`references/templates/quality_check_template.md` rendered as `quality_check.md`.

The package is complete only when all ten output files exist:

```text
index.html
patents.html
subfields.html
evidence.html
methodology.html
full_scope_metrics.json
patent_records.json
evidence_mapping.csv
README.md
quality_check.md
```

## Output contracts

### `index.html`

Executive overview of the decision, score, verified metrics, evidence, uncertainty, and next diligence.

### `patents.html`

Searchable representative patent register with disclosed sample and family rules.

### `subfields.html`

Technical segmentation with definitions, query logic, overlap warnings, and full-scope counts.

### `evidence.html`

Claim register linking each conclusion to metrics, patents, reasoning, evidence strength, and limitations.

### `methodology.html`

Reproducibility record for scope, versions, connectors, searches, metrics, lag, unavailable analyses, scoring, and QA.

### `full_scope_metrics.json`

Machine-readable metric definitions, values, query provenance, retrieval times, unavailable metrics, and limitations.

### `patent_records.json`

Machine-readable representative records, identifiers, family handling, available bibliographic fields, and source links.

### `evidence_mapping.csv`

Portable evidence-to-claim mapping for review and downstream analysis.

### `README.md`

Report map, intended use, data boundary, navigation, reproduction notes, and caveats.

### `quality_check.md`

Completed QA checklist with pass, fail, unavailable, and remediation notes.

## Quality gates

### Scope gate

- The subject is narrow enough to search reproducibly.
- Inclusion and exclusion rules are explicit.
- Date, jurisdiction, family, and status conventions are disclosed.

### Search gate

- Search syntax is documented and versioned.
- Synonyms and classifications are justified.
- False positives and false negatives are tested and discussed.

### Data gate

- Full-scope metrics are separated from representative records.
- Every chart uses verified complete-population data or complete reproducible buckets.
- Unavailable metrics are explicit.
- No record, metric, citation, or status is fabricated.

### Evidence gate

- Every material conclusion has a stable `claim_id`.
- Supporting sources are traceable.
- Contrary and limiting evidence is visible.
- Evidence strength matches the underlying support.

### Scoring gate

- Dimensions and weights are visible.
- Missing dimensions are removed and weights renormalized.
- Missing weight and uncertainty are reported.
- The score is a screening aid, not an investment recommendation.

### Report gate

- All ten outputs exist and open correctly.
- All five HTML pages have UTF-8 metadata and consistent navigation.
- The report works offline and uses no remote dependencies.
- Tables provide equivalents for meaningful charts.
- Keyboard focus, labels, contrast, and responsive behavior are usable.
- User-provided or connector-returned text is rendered safely.

### Consistency gate

- Topic, scope, cutoff, counts, and terminology agree across all outputs.
- Claim IDs match between the report and evidence CSV.
- Patent identifiers match between HTML, JSON, and evidence mapping.
- Metric IDs match between charts, methodology, and JSON.

## Failure handling

If the technology scope is too broad, narrow it before searching.
If the query is noisy, revise and version the search rather than silently filtering records.
If an MCP connector fails, record the failure and identify the affected outputs.
If a full-scope aggregation is unavailable, mark the metric unavailable.
If fewer representative patents exist than the target, use all valid records and disclose the count.
If evidence is insufficient for a commercialization conclusion, recommend specific additional diligence.
If any required file fails validation, repair it before declaring the report complete.

## Final response

Summarize:

- the normalized technology scope;
- the decision headline and confidence;
- the strongest verified opportunity signal;
- the most important risk or missing evidence;
- the report output location;
- the exact next diligence step.

Do not claim completion until the ten-file package passes the quality gates.
