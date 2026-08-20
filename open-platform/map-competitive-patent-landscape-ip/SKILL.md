---
copyright: "Copyright © Patsnap. All rights reserved."
name: map-competitive-patent-landscape-ip
description: Build an evidence-backed competitive patent landscape for a defined industry, technology, competitor set, geography, and time window. Use when executives, strategy teams, product leaders, competitive-intelligence analysts, or IP teams need to understand competitor technology bets, patent clusters, geographic filing behavior, cross-market differences, representative patents, potential white-space hypotheses, entry timing, and prioritized actions in an accessible HTML report; do not use this skill as an infringement or FTO opinion.
---

# Map a competitive patent landscape

## Purpose

Reveal what competitors appear to be protecting, which technical routes are accelerating, how filing strategies differ by market, and where evidence supports further opportunity validation.

Focus on competitive and product-strategy intelligence.

Do not perform infringement clearance under this workflow.

Do not state that a technical space is legally clear.

## Required source files

Read [references/SEARCH_STRATEGY.md](references/SEARCH_STRATEGY.md) before searching.

Read [references/REPORT_TEMPLATE.md](references/REPORT_TEMPLATE.md) before producing the report.

The source package mentions a README, but no README exists in the frozen source.

Do not look for or invent that missing file.

Use the MCP setup and fallback instructions in this file.

The bundled `scripts/main.py` is a preserved readiness stub, not an implementation of the research workflow.

## Trigger cases

Use this skill for:

- Competitor patent landscape analysis in a defined industry.
- Executive briefings on likely competitor R&D and product directions.
- Comparisons of competitor technology clusters.
- Comparisons of one competitor across jurisdictions or regions.
- Geographic filing-strategy analysis.
- Identification of evidence-backed white-space hypotheses.
- Assessment of whether an opportunity appears constrained, time-sensitive, open for validation, or too early to act on.

## Inputs

Collect:

| Input | Requirement | Example form |
|---|---|---|
| `industry` | Required industry or product category | Solid-state batteries |
| `technology_scope` | Required inclusions, exclusions, and adjacent areas | Sulfide electrolytes; exclude vehicle-pack controls |
| `competitors` | Required brands and known legal entities | Brand, parent, subsidiaries, markets |
| `client_name` | Required only for client-specific implications | Client organization |
| `target_jurisdictions` | Required offices or markets | US, EP, JP, KR |
| `years` | Rolling analysis period; default 5 | 5 |
| `cut_off_date` | ISO 8601 data cut-off | YYYY-MM-DD |
| `date_basis` | Priority, filing, publication, or grant | Publication |
| `counting_unit` | Publication, application, or family | Simple family |
| `report_title` | Optional | Global competitor technology signals |
| `brand_color` | Optional accessible accent | Hex color with contrast check |

Ask for the business decision the report must support.

Ask whether the user needs exhaustive retrieval or a top-k exploratory sample.

Ask which competitor relationships, acquisitions, and subsidiaries are in scope.

## Evidence and inference rules

Separate retrieved facts from strategic interpretations.

Label forward-looking product implications as hypotheses.

Support each material conclusion with patents, family data, legal-status data, or another cited source.

Record the search date, query, filters, result cap, counting unit, and deduplication method.

Never invent patent identifiers, counts, citations, assignees, filing paths, or legal status.

Do not equate patent volume with technology strength.

Do not equate forward citations with patent value.

Do not infer a product launch from a filing alone.

Do not call an area “white space” solely because a capped sample contains few results.

Do not use a fixed timing claim without stated evidence.

## MCP configuration

### Required: Advanced Patent Search

Official page: https://open.patsnap.com/marketplace/mcp-servers/patent-search

Verified 2026-08-07.

Configuration key: `advanced_patent_search`.

Transport: `streamableHttp`.

Current Connect-panel URL pattern:

`https://open.patsnap.com/marketplace/mcp-servers/patent-search`

Copy the current connection URL from the official Connect panel.

Keep the real API key outside reports, prompts, logs, and source control.

Use documented tools as appropriate:

- `search_patents_by_original_assignee` for original-applicant retrieval.
- `search_patents_by_current_assignee` for current-owner retrieval.
- `search_patents_nested` for controlled nested queries.
- `search_patents_by_semantic` for supplementary semantic retrieval.
- `search_patent_count` for total-hit context.
- `search_patent_field` for field distributions.
- `search_patent_by_pn` for record lookup.
- `suggest_keywords` for query development.
- Similarity and image tools for documented expansion tasks.

Use only arguments exposed by the connected tool schema.

### Recommended: Patent Briefing

Official page: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

Verified 2026-08-07.

Configuration key: `patent_briefing`.

Transport: `streamableHttp`.

Current Connect-panel URL pattern:

`https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`

Use it to review two or three representative records per competitor.

Use `bibliography`, `family`, `legal_status`, `claims`, `claim_translated`, `description`, `description_translated`, `intelligent_image`, and `tech_summary` as needed.

The source’s generic instruction to “fetch” a patent is not a verified tool call.

Replace it with the documented tools above.

### Missing MCP fallback

If live tools are unavailable, do not produce data-backed conclusions.

Provide:

- The resolved scope still requiring confirmation.
- An executable search strategy.
- Entity-resolution checklist.
- Taxonomy draft.
- Empty analysis tables.
- Report shell.
- Clear `not executed` labels.

## Workflow

### Step 1: Frame the analysis

Restate the industry, technology boundary, competitors, client, markets, period, date basis, counting unit, and decision.

Identify ambiguity before retrieval.

Set the data cut-off date.

Use a rolling five-year period by default.

Do not hard-code a 2021–2026 range.

### Step 2: Resolve competitors to patent entities

Map each brand to verified legal applicants and assignees.

Consider parent companies, subsidiaries, former names, mergers, acquisitions, transliterations, and native-script names.

Record evidence for every included entity.

Keep uncertain entities separate until confirmed.

Do not compare one competitor’s full group with another competitor’s single subsidiary without disclosure.

### Step 3: Build and validate the technology search

Follow `references/SEARCH_STRATEGY.md`.

Create keyword, classification, assignee, semantic, citation, and similarity routes where appropriate.

Use English and relevant local-language terms.

For Japanese applicants, use verified Japanese entity names and Japanese technical terms where needed.

Do not assume that Chinese keywords improve Japanese retrieval.

Run pilot searches.

Review noise and missing known records.

Refine the strategy before production retrieval.

### Step 4: Retrieve each competitor independently

Use a reproducible query and consistent scope.

Use a result cap of 50–100 only as an exploratory default.

Record any cap as top-k sampling.

Retrieve total hit counts separately where possible.

Do not call sample rank a portfolio-wide rank.

Preserve query, filters, tool, timestamp, and returned identifiers.

### Step 5: Normalize and deduplicate

Normalize patent numbers, applicant names, dates, jurisdictions, and classifications.

Select a family definition.

Deduplicate before competitor and geography comparisons.

Retain family members needed to understand jurisdiction paths.

Report missing fields rather than silently filling them.

### Step 6: Build an industry-specific taxonomy

Do not reuse the source’s six tissue routes for every industry.

Develop routes from the user’s scope, seed records, validated IPC/CPC groups, literature, standards, and expert review.

Allow multi-label assignment when justified.

Document classification rules.

Validate the taxonomy against sampled records.

### Step 7: Calculate landscape measures

At minimum calculate, where data permits:

- Competitor activity by counting unit.
- Technology-cluster distribution.
- Filing or publication trend over the selected period.
- Jurisdiction or filing-office distribution.
- Family breadth.
- Representative citation context.
- Technology breadth under a stated definition.

State denominators and missingness.

Do not use a bubble size for citations without explaining aggregation and bias.

### Step 8: Select representative patents

Choose two or three per competitor only when supported.

Balance technical relevance, claim or disclosure substance, recency, legal status, family path, citations, and distinct strategic signal.

Verify the patent number and family.

Read claims and specification sections needed for the interpretation.

Extract:

- Technical problem.
- Technical solution.
- Claimed or disclosed benefit.
- Independent-claim focus.
- Priority and family path.
- Jurisdiction coverage.
- Legal-status context.
- Reason for selection.

### Step 9: Compare geographic strategies

Compare competitors using normalized counting.

Distinguish priority country, filing office, publication authority, PCT route, regional route, national phase, and commercial market.

For a competitor appearing in multiple markets, run a dedicated cross-market comparison.

Test alternative explanations such as procedural practice, data coverage, sample bias, or entity scope.

### Step 10: Develop strategic interpretations

Identify up to three leading technology trends.

For each competitor, describe evidence-backed technical emphasis.

Distinguish observation from inference.

State confidence and counter-evidence.

Translate findings into client-specific opportunities or risks only after considering client capabilities and objectives.

### Step 11: Assess opportunity status

Use four text labels:

- `Constrained`.
- `Time-sensitive`.
- `Open hypothesis`.
- `Monitor`.

For each label, show the evidence, uncertainty, and validation step.

Do not use red, yellow, green, gray, or emoji as the sole meaning.

Do not claim a 12–18-month window unless the time estimate is derived and explained.

### Step 12: Generate the HTML report

Follow `references/REPORT_TEMPLATE.md`.

Use five chapters:

1. Executive landscape and conclusions.
2. Competitor deep dives.
3. Representative patent reviews.
4. Geographic strategy comparison.
5. Strategic implications and opportunity windows.

Put the executive conclusion before detailed charts.

Include a bubble chart only when patent activity, technology breadth, and citation aggregation are valid and explained.

Include a horizontal competitor bar chart with a zero baseline.

Include a radar chart only when all dimensions share a defensible normalized scale.

Include a stacked area chart only when category rules remain consistent over time.

Include a heatmap only with an accessible data table.

Place one decision-relevant interpretation below every chart.

Do not merely restate the plotted values.

## Visual standard

Use a light report with a white background and restrained accent color.

Use charcoal body text and neutral separators.

Use a Western system-font stack.

Do not use PingFang SC or Microsoft YaHei as the primary global font.

Do not use a dark theme.

Do not use gradients, decorative cards, pill badges, emoji, or yellow insight boxes.

Ensure accessible contrast.

Use direct labels, legends, captions, units, denominators, cut-off dates, and source notes.

Make charts understandable in monochrome.

Make tables responsive.

Add anchor navigation.

Add print CSS.

If using Chart.js, use a permitted, available dependency and preserve an accessible table for every chart.

If external dependencies are not permitted, use HTML/CSS or accessible inline SVG and disclose the method.

## Output

Create a complete HTML report.

Use a safe filename derived from the client and technology names.

Write it to the current workspace or user-approved output directory.

Do not use the source-specific `@session/output/` path unless it exists in the active environment.

Return a clickable file link when supported.

## Validation checklist

- All four inputs and optional fields are handled.
- Entity resolution is documented.
- Technology boundaries and taxonomy are documented.
- Time window and cut-off are current and explicit.
- Date basis and counting unit are explicit.
- Queries and filters are reproducible.
- Top-k samples are labeled.
- Family deduplication is applied or its absence disclosed.
- Representative patents have verified identifiers.
- Legal status is dated.
- Strategy claims are labeled as inference.
- Opportunity labels have evidence and confidence.
- No infringement or clearance conclusion appears.
- Every chart has a caption, unit, denominator, source, and interpretation.
- The report is responsive, accessible, and print-safe.
- No stale client example or China-only default remains.
- No real API key is exposed.
- Missing MCP capability triggers the documented fallback.

## Final response

Lead with the most decision-relevant finding.

State the competitor, technology, jurisdiction, time, and counting scope.

State whether the analysis is exhaustive or sample-based.

State the evidence cut-off date.

Link the generated HTML report.

Name the highest-priority validation action.
