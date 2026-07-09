# Scenario: Industry Landscape

Use this scenario for the first layer of a patent panorama report: industry trend, major players, target jurisdictions, legal status overview, and high-level technology branch distribution.

## When To Use

Use when the user asks:

- Whether a technology field is growing or declining.
- Which companies or institutions are investing most heavily.
- Which regions or receiving offices are most active.
- Which technical branches are hot.
- How the overall landscape supports product, R&D, or portfolio decisions.

## Business Questions

- Is the technology domain active enough to justify deeper analysis?
- Which players define the competitive baseline?
- Which geographies appear to be target protection markets?
- Are recent filings concentrated in particular branches or applications?
- What should be selected for Layer 2 tagging and Layer 3 deep reading?

## Required Inputs

| Input | Notes |
|---|---|
| `technology_domain` | Required |
| `include_topics` and `exclude_topics` | Use if the domain is broad or noisy |
| `geography` | Default CN, US, EP if not specified |
| `date_range` | Default earliest priority date on or after 2023-01-01 for v0 quick scans |
| `entity_scope` | All industry, selected players, or player vs industry |
| `counting_method` | Publication-level by v0 default unless the user requests family-level |

## Data And MCP Capabilities

| Task | Preferred Capability |
|---|---|
| Candidate pool construction | `search_patents` |
| Bibliographic fields | `bibliography` |
| Family context | `family` |
| Simple legal status | `get_patent_legal_status` |
| Forward citation signal | `forward_citation` |
| Translated abstract for relevance sampling | `abstract_translated` |

Use local aggregation for trends, assignee ranking, jurisdiction distribution, and branch rule-hit counts.

## Analysis Flow

1. Translate the business question into 3 to 7 research questions.
2. Build first-pass technology and product decomposition.
3. Create multiple rule-based search sets:
   - `S1`: technology keywords plus IPC/CPC.
   - `S2`: product or scenario keywords plus IPC/CPC.
   - `S3`: technical problem or effect keywords.
   - `S4`: applicant or competitor supplement.
   - `S5`: exclusion set for noise.
4. Pull bibliographic fields for a manageable candidate pool.
5. Normalize assignee names and jurisdictions.
6. Estimate noise by sampling major buckets.
7. Generate preliminary statistics.
8. Propose Layer 2 tagging scope.

## Report Blocks

| Block | Content |
|---|---|
| Landscape KPI strip | Raw hits, cleaned hits, date range, geography, counting method |
| Annual trend | Application, priority, or publication trend with lag note |
| Major assignees | Normalized top assignees and recent movement |
| Jurisdiction view | Receiving office or family coverage proxy |
| Legal status overview | Simple status only, signal level |
| Rule-hit branch view | Preliminary branch distribution, not final taxonomy |
| Layer 2 proposal | Subsets, tag fields, sample cap, tradeoff |

## Charts And Tables

| Output | Recommended Format |
|---|---|
| Annual trend | Line or stacked bar |
| Assignee ranking | Horizontal bar |
| Jurisdiction distribution | Bar chart or matrix |
| Legal status | Stacked bar or donut |
| Branch distribution | Bar chart |
| Assignee x branch | Heatmap |
| Search sets | Table with search intent and sample count |
| De-noising | Table with rule, reason, and effect |

## Evidence Rules

- Trends and rankings are L1 facts if directly counted from the dataset.
- Growth, concentration, and dispersion are L2 observed patterns.
- Strategic implications are L3 or L4 and require representative evidence.
- Simple legal status is L5 signal only.

## V0 Boundary

V0 can support a basic industry landscape with installed patent MCP tools and local aggregation.

Be careful with:

- Publication lag in recent years.
- Assignee aliasing and subsidiaries.
- Rule-hit branch labels, which are not final manual labels.
- Jurisdiction distribution, which is a proxy for target markets.
- Legal status, which is not a legal conclusion.

## Quality Checklist

- Search sets and sample counts are recorded.
- Each major chart states the counting method.
- Assignee normalization is visible.
- Major noise sources are named.
- The output includes a clear Layer 2 tagging proposal.
- No confidential customer or historical-report details appear.
