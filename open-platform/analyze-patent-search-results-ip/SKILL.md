---
copyright: "Copyright © Patsnap. All rights reserved."
name: analyze-patent-search-results-ip
description: Analyze validated patent-search artifacts at Stage 2/4 of a patent-landscape program. Use after search-patents-ip to produce population-bounded trends, organization and technology distributions, competitor profiles, a branch-organized reviewed core patent index, transparent candidate-level value proxies, chart-ready data, and a self-contained statistical snapshot for tag-patent-search-results-ip and create-patent-search-report-ip.
---

# Analyze Patent Search Results

## Role in the suite

Act as Stage 2/4 of `create-patent-landscape-overview-ip`. Consume the validated
Stage 1 scope and records, then create statistical and evidence artifacts for
`tag-patent-search-results-ip` and `create-patent-search-report-ip`.

This stage answers:

- What activity is observed under the defined search population and counting method?
- Which normalized organizations and jurisdictions appear in that population?
- Which search-rule branches and classifications are prominent?
- Which records deserve deeper review within each branch?
- Which dated patent-data proxies occur for those reviewed candidates?

This stage does not create a final taxonomy, provide legal opinions, value patents,
or produce the Stage 4 insight report.

## Required Stage 1 inputs

| Artifact | Requirement |
|---|---|
| `search_config.json` | Confirmed scope, canonical query/branches, anchor, exclusions, validation, date/unit/family rules, connector provenance, count/cap state |
| `candidate_pool.csv` | Traceable candidate records, branch hits, family/record IDs when available, query version, retrieval state |
| `core_recall.csv` | Branch-organized recall candidates, raw rank/signal definition, date and verification state |

Read and validate all three. The Stage 1 companion `run_config.json` and preliminary
`tech_taxonomy.txt` may provide context but do not override `search_config.json` or
constitute validated tags.

If a required input is missing, belongs to a different scope/version, or cannot be
reconciled, stop and return to `search-patents-ip`. Do not reconstruct the query here.

## Authoritative Stage 2 outputs

| Artifact | Content |
|---|---|
| `panorama_stats.json` | Scope-aware trends, organizations, jurisdictions, status sample/aggregation, classification/rule-hit views, organization normalization, and competitor profiles |
| `patent_index.core.json` and `patent_index.core.csv` | Same branch-organized reviewed candidates in structured and tabular forms |
| `value_signals.json` | Candidate-level dated proxy dimensions, evidence states, weights/missing-data/sensitivity, no branch-level synthesis |
| `chart_data.json` | Chart-ready aggregates with measure, unit, date basis, cutoff, population, and limitations |
| `panorama_stats_report.html` | One offline statistical data-view snapshot, distinct from Stage 4 interpretation |

Store organization-normalization decisions inside `panorama_stats.json`. Do not create
or extend `report_manifest.json`; Stage 4 owns that filename. Preserve source, operation,
request, query version, cutoff, and limitations in every Stage 2 artifact.

## Verified global Patsnap MCPs

Inspect the active schema before any call and record the exact operation used.

### Advanced Patent Search — required

- Connector key: `advanced_patent_search`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`
- Use for complete or explicitly bounded search aggregations, field facets, and
  organization/technology views where the live contract supports them.

### Patent Briefing — required for selected records

- Connector key: `patent_briefing`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- Use for selected core-record bibliography, family, status, claims, descriptions,
  translations, and images exposed by the contract.

### Deep Patent Mining — recommended

- Connector key: `deep_patent_mining`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-mining
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-mining`
- Use for selected-record technical problem, means, effect, material, process, and
  application evidence where needed.

### Global Core Patent Database — recommended

- Connector key: `global_core_patent_database`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/core-patents
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/core-patents`
- Use for deeper family, citation, status/event, litigation, license, transfer, and
  full-text evidence where supported.

Do not use regional endpoint IDs or source-era operation aliases. Do not call a result
“official statistics” unless the current connector contract documents the measure and
population.

## Validate and plan execution

Before S1:

1. verify project/query version, branch IDs, and scope;
2. verify jurisdictions, languages, dates, date basis, unit, and family definition;
3. reconcile search counts with candidate rows and family mappings;
4. identify complete, capped, sampled, and unavailable populations;
5. inspect branch multi-hit and duplicate behavior;
6. verify core-recall signal definitions and rankings;
7. record named organizations and normalization requirements;
8. define population metrics, sample estimates, and selected-record enrichments;
9. define batch size, persistence checkpoint, rate/context budget, and retry policy;
10. define output schemas and null/proxy states.

Use decision- and connector-appropriate limits. Do not copy fixed Top 10, Top 50,
20-record batches, or 120-record thresholds as universal rules.

## S1 — Industry-level statistics

### Objective

Describe scale, time distribution, filing/publication jurisdictions, and available
status information under the exact search scope.

### Population rules

Use server-side aggregations only when:

- the query and filters match the accepted Stage 1 configuration;
- the aggregation covers the intended population rather than a capped result page;
- the field meaning, date basis, family behavior, and missing values are documented;
- multi-query/branch overlap is reconciled; and
- totals can be checked against available search counts.

Otherwise use complete reproducible retrieval or label a sample/partial view.

### Trend

- Use the date basis declared in `search_config.json`.
- Keep priority, filing, and publication trends separate.
- State the unit and family definition.
- Check recent periods for publication lag and database cutoff.
- Do not describe growth/decline without a stable comparison period and denominator.

### Jurisdiction

- Name the measure accurately: filing office, publication authority, family-member
  jurisdiction, or another documented field.
- Do not call it target market, sales market, nationality, or commercial presence.
- Reconcile multi-jurisdiction family counts and duplicate behavior.

### Legal status

If a complete documented status aggregation is unavailable, select a reproducible
sample from a defined population and label the output `sample_estimate`.

Record sample method, size, strata, cutoff, jurisdiction semantics, unknown share, and
uncertainty. Never generalize a convenience sample of high-ranked core records to the
full population.

### S1 outputs

Write to `panorama_stats.json` and `chart_data.json`:

- total/capped/complete state;
- time series;
- jurisdiction distribution;
- status aggregation or sample estimate;
- method, unit, cutoff, provenance, and limitations.

## S2 — Organization landscape

### Resolve organizations

Create an organization-normalization register inside `panorama_stats.json`:

| Field | Meaning |
|---|---|
| `canonical_name` | Display/grouping name |
| `source_names` | Exact assignee/applicant variants |
| `relationship` | Parent, subsidiary, former name, acquisition, JV, unresolved |
| `effective_period` | Time relevance when known |
| `evidence` | Corporate/patent source and date |
| `decision` | Include, exclude, separate, or `to_confirm` |

Do not silently merge uncertain subsidiaries, common-name collisions, universities,
joint ventures, or acquired entities. Preserve original assignee values.

### Calculate organization views

Under one consistent query/date/unit/family policy:

- organization ranking and share;
- organization trend;
- named-organization presence and anomalies;
- organization × jurisdiction; and
- unresolved alias impact.

If only a Top-K facet is available, label it Top-K and do not calculate total-market
shares from the truncated list.

Patent count does not establish market leadership, R&D spend, product success, or
technical quality.

## S3 — Technology structure and competitor profiles

### S3A. Technology structure

Produce separate views for:

1. IPC/CPC or connector-defined technology categories; and
2. Stage 1 branch-rule hits.

Label branch-rule counts as preliminary, potentially duplicate-counted search hits.
They are not Stage 3/human-validated taxonomy tags.

For every matrix state row/column dimensions, cell measure, family/unit rule,
multi-label duplicate policy, query version, and cutoff.

### S3B. Competitor profiles

Only run when named organizations or the decision requires comparison.

For each organization:

1. apply the resolved name set;
2. calculate comparable scale and trend;
3. calculate jurisdiction and technology views under the same policy;
4. define a dynamic recent period and account for publication lag;
5. identify representative/high-attention records under a disclosed signal; and
6. record sparse data, unusual filing practices, and alias uncertainty.

Output organization × branch, organization × jurisdiction, and recent-focus views.
Select representative records based on evidence; do not force three to five.

Use “the patent evidence suggests” and “more prominent under this scope,” not product
roadmap certainty or absence of capability.

## S4 — Branch-organized core review index

### Objective

Prioritize records for human technical, taxonomy, and report review. “Core” means
selected for this research workflow, not legally or commercially essential.

### Default path

1. Read `core_recall.csv` and group by `branch_id`.
2. preserve source ranking/signal and query version.
3. select a decision-appropriate set across branches without fixed quotas.
4. batch-retrieve only required display/evidence fields.
5. persist every completed batch immediately.
6. store large payloads on disk and retain only progress/reconciliation in context.
7. assign `unverified_recall_priority` until evidence is checked.

Do not automatically convert `both`, citation rank, or family rank into a high-value
or verified tier.

### Verification fallback

Verify additional records when a priority branch is sparse, evidence is contradictory,
or a conclusion depends on a record. Plan a bounded set based on decision risk, data
availability, connector limits, privacy, and context.

For selected records verify available:

- bibliography and identity;
- family definition and members;
- citation count/type/as-of date;
- jurisdiction-specific legal status/event as of date;
- claims/description evidence for technical relevance; and
- source/operation/provenance.

Stop when the approved budget is exhausted and record `verification_incomplete`; do
not silently continue, invent facts, or move the work into an unapproved execution
context.

### Review rubric

Keep dimensions separate:

- technical relevance;
- branch representativeness;
- evidence depth;
- family breadth proxy;
- dated citation proxy;
- dated legal/status signal;
- organization diversity; and
- review need.

Expose any score/weights and missing-data treatment. Do not define Tier 1 solely as a
fixed conjunction of citations, three jurisdictions, and active status.

### Core index schema

Preserve the source’s 23-field intent:

| Field | Rule |
|---|---|
| `record_id` | Stable source or local ID |
| `branch_id` | Stage 1 branch |
| `patent_id` | Source ID when returned |
| `publication_number` | Exact publication identifier |
| `title` | Source title/translation state |
| `normalized_assignee` | Reviewed grouping |
| `original_assignee` | Source value |
| `publication_date` | ISO date |
| `priority_date` | Earliest verified priority date |
| `jurisdiction` | Defined office/right context |
| `legal_status` | Dated signal or null |
| `family_size` | Defined family measure or null |
| `citation_count` | Defined citation type/as-of or null |
| `score` | Transparent screening score/range or null |
| `tier` | Controlled review priority, not legal/value tier |
| `abstract` | Retrieved text/translation state |
| `ai_summary` | Source-grounded machine summary with evidence references |
| `technical_problem` | Evidence-grounded or null |
| `technical_solution` | Evidence-grounded or null |
| `technical_effect` | Claimed/described status or null |
| `recommendation_reason` | Leave for Stage 3 review unless explicitly supported |
| `review_status` | Recall-only, partially verified, verified fields, needs review |
| `source_run_id` | Query/retrieval provenance |

Write identical semantic content to JSON and CSV. Keep unavailable facts null. Never
derive legal status from recall source or fabricate a summary when text is unavailable.

## S5 — Candidate-level value proxies

### Reuse persisted facts

Read `patent_index.core.*`. Do not re-query every record for facts already persisted.
Candidate dimensions may include:

| Dimension | Interpretation |
|---|---|
| Citation | Dated attention/influence proxy with age/practice bias |
| Family breadth | Geographic filing proxy under declared family method |
| Legal status | Dated jurisdiction-specific database signal |
| Organization concentration | Who appears in the branch under the normalized dataset |
| Portfolio/priority signal | Connector/local screening proxy with definition |
| Assertion/litigation/event | Exposure/event clue requiring legal verification |

Do not use a recall label as an active-status proxy. If a fact is null, preserve null
and reduce evidence completeness rather than substitute a different construct.

### Normalize and combine

If a composite screening index is useful:

1. define cohort and denominator;
2. age- and jurisdiction-adjust where relevant;
3. normalize only comparable measures;
4. expose weights and contribution of every dimension;
5. define null treatment;
6. preserve verified/proxy/unavailable state;
7. test plausible alternative weights and outlier sensitivity; and
8. label the result `screening_index`, not `value_score` in narrative.

Output candidate ID, branch ID, each raw/normalized dimension, source/date/state,
weights, composite if used, sensitivity, signals fired, and limitations.

Do not aggregate to branch “moat” themes here; Stage 4 owns that synthesis.

## S6 — Optional asset/event signals

Run only when the user requests asset intelligence or a defined reviewed candidate
requires it. Retrieve available assignments/transfers, licenses, awards, challenges,
litigation, or other events through a verified current connector.

For every event record date, jurisdiction, parties, source, retrieval cutoff,
observation, uncertainty, and required verification. Missing connector data do not
prove absence. Do not recommend acquisition, licensing, enforcement, or legal action.

## S7 — Statistical snapshot HTML

### Role

Render `panorama_stats_report.html` only from persisted Stage 2 artifacts and
`search_config.json`. Make no new MCP call.

Put this statement near the top:

```text
Statistical snapshot (data view). Interpretation, technology-evolution synthesis,
branch-level signal themes, and curated actions belong to the Stage 4 insight report.
```

### Default modules

Use available evidence to render:

1. scope and data state;
2. search quality;
3. industry/time/jurisdiction view;
4. organization landscape;
5. technology/classification and rule-hit branches;
6. competitor matrices when in scope;
7. core review index and verification state; and
8. method, limitations, and Stage 3 proposal.

Do not force eight sections when data are unavailable. State omissions.

### Scientific/executive visual contract

- Deliver one self-contained HTML file with embedded CSS and pre-aggregated data.
- Use semantic HTML, a neutral/white canvas, navy/slate hierarchy, and restrained teal.
- Use system fonts and accessible contrast; do not copy a vendor interface.
- Prefer static HTML/CSS/SVG charts and tables.
- Permit minimal inline JavaScript only as progressive enhancement with fallback.
- Load no CDN, remote font, image, tracker, frame, or external data file.
- Escape all user/retrieved values and validate safe URLs.
- Provide chart captions with measure, denominator, date basis, unit, family method,
  scope, cutoff, completeness/sample state, and limitations.
- Use labels plus color for priority/status/evidence states.
- Provide responsive overflow, keyboard-visible controls, text chart alternatives,
  reduced-motion behavior, and print/PDF styles.
- Show unavailable data rather than a fake chart.

After validating the file, report its section/chart counts without pasting the HTML.

## Stage 2 summary and Stage 3 proposal

Report:

```text
Stage 2 statistical summary
Scope: [query version, dates, jurisdictions, unit, family, cutoff]
Population state: [complete aggregation / complete retrieval / capped / sampled]
Industry: [bounded facts and patterns]
Organizations: [normalized leading groups and unresolved aliases]
Technology: [classification and rule-hit views, duplicate policy]
Core review index: [branch counts and verification-state counts]
Value proxies: [dimensions, missingness, sensitivity; no valuation]
Optional events: [scope and verification]
Snapshot: panorama_stats_report.html ([sections/charts])

Stage 3 proposal
Candidate/tagging scope: [...]
Suggested evidence depth: abstract / claim-assisted / full-text selected records
Priority branches/organizations: [... with rationale]
Unresolved: [...]
```

Obtain user confirmation when the Stage 3 scope would materially change cost, data
handling, or human-review workload. Otherwise route to `tag-patent-search-results-ip`.

## Evidence language

- “rule-hit approximation; multi-label/branch overlap may duplicate families”;
- “forward-citation attention signal as of [date], not quality or legal value”;
- “family-breadth filing proxy under [definition], not claim scope”;
- “database status signal as of [date], requiring official/legal verification”;
- “composite screening index under disclosed weights, not valuation”; and
- “the patent evidence suggests under this dataset,” not “the organization will.”

Every material output traces to query version, connector/operation, request, date,
unit, family definition, and data cutoff.

## Quality gate

### Inputs and population

- Stage 1 artifacts reconcile by scope, version, branches, counts, and family method.
- Every statistic identifies complete aggregation/retrieval, capped result, or sample.
- No convenience sample is generalized to the population.
- Publication lag and missing values are explicit.

### Organizations and technology

- Original and normalized assignees are preserved.
- Uncertain aliases remain `to_confirm`.
- Rankings/shares state Top-K limitations.
- Classification, rule-hit, automated, and validated tags are distinct.
- Multi-label duplicate counting is disclosed.

### Core and signals

- All 23 core-index fields exist or are explicitly null.
- Recall priority and verified evidence states are distinct.
- Batches persist and reconcile; no large payload accumulates in context.
- Citation/family/status/event fields are defined and dated.
- Composite weights, missing data, and sensitivity are visible.
- No recall label substitutes for a missing fact.

### Outputs and handoff

- All five authoritative Stage 2 outputs exist and validate.
- JSON/CSV semantic parity and chart totals reconcile.
- Snapshot is offline, safe, accessible, responsive, printable, and clearly a data view.
- No Stage 2 report manifest or unsynchronized normalization file is created.
- Stage 3 and Stage 4 receive exact artifact paths and unresolved issues.

## Stop conditions

Stop or narrow when:

- upstream artifacts conflict or cannot be parsed;
- the search connector cannot provide the required aggregation semantics;
- caps prevent a requested population claim;
- family/unit/date settings cannot be reconciled;
- entity aliases materially affect rankings and remain unresolved;
- selected-record evidence cannot support the core-index claim;
- a batch/checkpoint fails and cannot resume safely;
- value/event data are stale, incomparable, or unavailable;
- confidential data cannot be handled within the authorized boundary;
- output validation fails; or
- the requested conclusion requires legal, valuation, or transaction expertise.

Return completed artifacts, failed checks, affected conclusions, and exact next action.
Do not silently substitute a sample, proxy, ranking, or invented value.
