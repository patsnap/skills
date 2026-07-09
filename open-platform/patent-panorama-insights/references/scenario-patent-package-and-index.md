# Scenario: Patent Package And Index

Use this scenario when the project needs a recommended patent package, patent cards, or an Excel-style tagged patent index.

## When To Use

Use when the user asks:

- Which patents are worth detailed reading.
- Which patents should be monitored, compared, acquired, licensed, or reviewed.
- How to build a structured patent index with taxonomy tags.
- How to create a reusable labeled dataset for product, R&D, or IP teams.

## Business Questions

- Which patent families best represent each priority branch or scenario?
- Why is each patent recommended?
- Which fields should be tagged manually or semi-automatically?
- How should product, scenario, problem, solution, and effect labels be defined?
- Which records require human or legal review?

## Required Inputs

| Input | Notes |
|---|---|
| `package_by` | Technology branch, product scenario, competitor, or problem type |
| `target_count_per_package` | Default 3 to 10 families per package |
| `tag_fields` | Technology, product, scenario, problem, solution, effect, recommendation |
| `candidate_pool` | From Layer 1 or Layer 2 |
| `review_depth` | Abstract-only, claim-assisted, or full deep reading |

## Data And MCP Capabilities

| Task | Preferred Capability |
|---|---|
| Candidate pool | `search_patents` |
| Bibliographic fields | `bibliography` |
| Family coverage | `family` |
| Citation signal | `forward_citation` |
| Legal status | `get_patent_legal_status` |
| Claims and descriptions | `claims`, `description`, translated variants |
| Asset or event signals | `legal_data`, `license_data`, `transfer_data`, `pledge_data`, `customs_data`, `award_data` |

## Recommended Index Fields

| Field | Purpose |
|---|---|
| `family_id` | Family-level grouping |
| `representative_publication` | Representative public text placeholder |
| `title` | Basic understanding |
| `abstract` | Fast relevance screen |
| `normalized_assignee` | Comparable applicant statistics |
| `original_assignee` | Traceability |
| `priority_date` | Trend and remaining-term signal |
| `publication_date` | Public text timing |
| `jurisdiction` | Receiving office or target-market proxy |
| `legal_status` | Signal only |
| `tech_level_1` to `tech_level_3` | Technology taxonomy |
| `product_type` | Product planning link |
| `application_scenario` | Scenario link |
| `technical_problem` | Problem-solution analysis |
| `technical_solution` | Route clustering |
| `technical_effect` | Business and product value |
| `forward_citation_count` | Value signal |
| `family_coverage` | Geographic/value signal |
| `recommendation_level` | Priority for reading |
| `recommendation_reason` | Evidence-backed reason |
| `review_status` | Machine-tagged, sampled, manually reviewed, legal review needed |

## Analysis Flow

1. Define package logic:
   - By branch.
   - By product scenario.
   - By competitor.
   - By technical problem.
2. Build candidate pool from cleaned Layer 1 or confirmed Layer 2.
3. Score candidates using transparent criteria:
   - Technical relevance.
   - Representative solution.
   - Clear technical effect.
   - Family coverage.
   - Forward citation signal.
   - Legal status signal.
   - Claim readability.
   - Player representativeness.
   - Product or scenario fit.
4. Select a manageable number of patent families.
5. Read enough evidence to write recommendation reasons.
6. Mark review status and next action.

## Report Blocks

| Block | Content |
|---|---|
| Package selection rule | How patents were selected |
| Package overview | Counts by branch, scenario, or player |
| Recommended patent table | Structured recommended list |
| Patent cards | For top records |
| Tag dictionary | Definitions, include/exclude rules, multi-label rules |
| Review plan | Which records need manual or legal review |

## Recommendation Reason Template

```text
Recommended because [patent_placeholder] represents [solution_type] for [technical_problem].
The evidence is [abstract_or_claim_or_description_signal]. It is relevant to [product_or_scenario]
and worth [read | monitor | compare | portfolio_reference | legal_review] because [value_signal].
```

## Tagging Rules

- Product type, scenario, problem, solution, and effect may be multi-label.
- If multi-label statistics duplicate counts, state that clearly.
- Labels must have include/exclude criteria.
- Ambiguous records should be marked as `needs_review`.
- Do not overfit taxonomy to a single historical project.

## V0 Boundary

V0 can generate patent package logic, structured tables, and patent cards from MCP data.

V0 should not promise:

- Full human validation of thousands of records.
- Official legal risk ranking.
- Purchase, licensing, or enforcement recommendation without expert review.

## Quality Checklist

- Every recommended patent has a reason.
- Selection criteria are visible and reproducible.
- Review status is explicit.
- Tag definitions are included.
- Legal review items are separated from business recommendations.
- No real confidential patent numbers or historical recommendation sentences appear.
