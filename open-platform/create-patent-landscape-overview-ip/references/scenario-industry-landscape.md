# Scenario: Industry Patent Landscape

Use this scenario for the first analytical layer: activity trends, leading organizations, filing jurisdictions, high-level legal-status signals, and preliminary technology-branch distribution.

## Use for questions such as

- Is a technology field expanding, stable, or declining under a defined measure?
- Which companies, universities, or research organizations are most active?
- Which patent offices or family jurisdictions receive protection?
- Which technical branches appear active?
- What should advance to taxonomy validation and patent-level deep reading?

## Required inputs

| Input | Requirement |
|---|---|
| `technology_domain` | Required, with explicit inclusion boundary |
| `include_topics`, `exclude_topics` | Add for broad, polysemous, or noisy fields |
| `jurisdictions` | Ask the user or choose a reasoned global scope; never assume CN/US/EP |
| `date_range` | Ask or state a fit-for-purpose period and publication-lag caveat |
| `organization_scope` | Industry-wide, selected organizations, or organization versus industry |
| `unit_of_analysis` | Publication, application, simple family, or extended family; define it |
| `date_basis` | Priority, filing, or publication date; use one consistently per trend |

Do not preserve the source’s China-oriented or fixed “since 2023” defaults. Select scope from the decision question and document it before retrieval.

## Global PatSnap capabilities

| Task | Preferred service and operation |
|---|---|
| Construct and refine the candidate population | Advanced Patent Search MCP: `advanced_patent_search` |
| Retrieve structured records, family context, citations, and legal-event context for selected patents | Patent Briefing MCP: `patent_briefing` |
| Expand selected records into deeper evidence | Deep Patent Mining MCP: `deep_patent_mining` |
| Obtain broader patent intelligence for selected records when available | Global Core Patent Database MCP: `global_core_patent_database` |

Use only operations exposed by the installed connector schema. Do not invent source-era operation names such as `search_patents`, `bibliography`, or `forward_citation`. Perform reproducible local aggregation only after confirming that retrieval or server-side buckets cover the intended population.

## Analysis flow

1. Convert the decision objective into three to seven research questions.
2. Draft the technology, product, application, problem, and effect decomposition.
3. Build auditable search sets:
   - `S1`: technology terms plus relevant IPC/CPC anchors;
   - `S2`: product or application terms plus classification anchors;
   - `S3`: technical-problem or effect terms;
   - `S4`: organization-name supplement, used for recall checking rather than defining the market alone; and
   - `S5`: staged exclusions with reasons and near-miss checks.
4. Confirm the intended population and export or aggregate method.
5. Normalize organization names without silently merging uncertain entities.
6. Sample major buckets and near misses to estimate relevance and recall risk.
7. Produce only the statistics supported by complete retrieval or verified aggregations.
8. Propose the subsets and fields for taxonomy validation and deep reading.

## Report blocks

| Block | Content |
|---|---|
| Scope and KPI strip | Raw results, screened population, period, jurisdiction, date basis, unit, and cutoff |
| Activity trend | Priority-, filing-, or publication-based series with lag note |
| Leading organizations | Normalized rankings and recent movement |
| Jurisdiction view | Patent-office activity or family coverage, named accurately |
| Legal-status overview | Dated research signals only |
| Preliminary branch view | Search-rule hits, visibly distinguished from validated taxonomy tags |
| Next-stage proposal | Subsets, tag fields, review method, and trade-offs |

Preferred views include lines or stacked bars for trends, horizontal bars for rankings, matrices for organization × branch or jurisdiction, and tables for search sets and screening rules. Avoid donut charts when exact comparison matters.

## Evidence and interpretation

- Direct counts from a verified population are L1 facts.
- Growth, concentration, and dispersion calculated under the stated method are L2 observations.
- Strategic interpretation is L3; recommendations are L4 and require representative patent evidence.
- Legal status and transaction events are L5 signals only.
- Jurisdiction counts indicate filing or family coverage, not proven market demand or commercial presence.
- A recent decline may reflect publication lag; test and state this before interpreting it.

## Quality gate

- Search sets, query versions, result counts, and exclusions are recorded.
- Every chart states date basis, unit, scope, and cutoff.
- Organization normalization and unresolved aliases are visible.
- Material noise sources and recall risks are named.
- Rule-hit labels are not represented as human-validated tags.
- The next-stage classification proposal is actionable.
- No confidential or China-market legacy examples remain.

## Analyst worksheet

Record these decisions before drafting conclusions:

| Decision | Record |
|---|---|
| Business decision | What action will the landscape inform? |
| Search boundary | Included technologies, applications, and exclusions |
| Jurisdiction meaning | Office of filing, family member location, or another defined measure |
| Time basis | Priority, filing, or publication date |
| Counting unit | Publication, application, or declared family definition |
| Population basis | Complete retrieval, verified aggregation, or sample |
| Organization policy | Normalization, subsidiaries, and unresolved aliases |
| Taxonomy state | Rule-hit, analyst-reviewed, or human-validated |
| Cutoff | Retrieval date and latest covered event/date |

### Minimum diagnostic checks

1. Compare keyword-only and classification-assisted result sets.
2. Review high-volume organizations for false positives caused by broad portfolios.
3. Inspect at least the dominant buckets, low-frequency branches, and near misses.
4. Test whether family deduplication changes rankings materially.
5. Compare recent publication-based movement with an earlier stable period.
6. Identify whether office-specific language, transliteration, or translated abstracts create blind spots.
7. Reconcile chart totals with the documented screened population.

### Interpretation traps

- More filings do not necessarily mean greater technical quality or commercial success.
- Family breadth is affected by filing strategy, cost, and jurisdictional practice.
- Assignee rankings can change materially after corporate-name resolution.
- A branch can appear small because terminology or classification coverage differs.
- Status categories are not harmonized legal opinions across offices.
- The absence of a record in the retrieved set is not evidence of absence from the field.

### Handoff artifacts

Pass the versioned query, search-set counts, normalization table, preliminary taxonomy, sampling log, limitations, and candidate identifiers to the next suite stage. Do not pass only a presentation or chart image; downstream tagging must be able to trace every included record.
