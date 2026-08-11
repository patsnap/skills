# Scenario: Curated Patent Package and Index

Use this scenario to create a prioritized patent package, comparable patent evidence cards, or a reusable tagged patent index for product, R&D, strategy, or IP teams.

## Use for questions such as

- Which patents warrant detailed reading or continued monitoring?
- Which records should be compared, considered for a technical reference set, or referred for licensing/acquisition diligence?
- How should a structured patent index capture taxonomy and review state?
- Which fields require automated, analyst, human-subject-matter, or legal review?

## Required inputs

| Input | Requirement |
|---|---|
| `package_by` | Technology branch, application, organization, or technical problem |
| `candidate_pool` | Cleaned search population or validated tagged subset |
| `tag_fields` | Technology, product, application, problem, solution, effect, and recommendation fields as needed |
| `selection_basis` | Transparent criteria and tie handling |
| `review_depth` | Abstract-only, claim-assisted, or detailed review |
| `unit_of_analysis` | Usually family for package selection; define family method |

Do not use a fixed package quota as a success target. Include only records supported by evidence and disclose underrepresented branches.

## Global PatSnap capabilities

Use `advanced_patent_search` for the candidate population. Use `patent_briefing`, `deep_patent_mining`, and, if applicable, `global_core_patent_database` for selected-record bibliography, family, claims, descriptions, citations, status, and events exposed by the installed connectors. Never assume that a legacy source field or operation exists in the active MCP contract.

## Recommended index schema

| Field | Purpose |
|---|---|
| `family_id` | Traceable family grouping under a declared definition |
| `representative_publication` | Public record selected to represent the family |
| `title`, `abstract` | Fast relevance and traceability |
| `original_assignee` | Source identity |
| `normalized_assignee` | Comparable organization grouping |
| `priority_date`, `filing_date`, `publication_date` | Time interpretation; keep distinct |
| `jurisdiction` | Filing office or family jurisdiction, named accurately |
| `legal_status_as_of`, `legal_status_source` | Dated research signal |
| `tech_level_1`–`tech_level_3` | Versioned technology taxonomy |
| `product_type`, `application_scenario` | Product or use-context connection |
| `technical_problem` | Problem–solution analysis |
| `technical_solution` | Route clustering |
| `technical_effect` | Claimed, described, or observed effect with evidence status |
| `forward_citation_count_as_of` | Dated citation signal with source |
| `family_coverage` | Geographic/family proxy under declared method |
| `recommendation_level` | Priority under the documented rubric |
| `recommendation_reason` | Evidence-based rationale |
| `classification_status` | Automated, analyst-reviewed, SME-validated, or unresolved |
| `review_status`, `next_action` | Workflow state and responsible follow-up |
| `evidence_locator` | Source field, passage, or record reference |

## Analysis flow

1. Define whether packages are organized by branch, application, organization, or problem.
2. Start from the cleaned population and validated taxonomy artifacts from the earlier suite stages.
3. Score or rank candidates with transparent, non-dispositive criteria such as:
   - technical relevance and representative route coverage;
   - clarity of technical means and reported effect;
   - family, citation, or legal-status signals, each defined and dated;
   - organization or application representativeness;
   - evidence readability and traceability; and
   - diversity across relevant routes or organizations.
4. Test rankings for missing-data bias and duplicate-family bias.
5. Select a manageable evidence-backed set.
6. Read enough source material to write a specific recommendation rationale.
7. Record classification status, review status, uncertainty, and next action.

## Deliverable blocks

| Block | Content |
|---|---|
| Selection method | Candidate source, criteria, weights or ordering, and missing-data treatment |
| Package overview | Coverage by branch, application, or organization |
| Recommended table | Structured list with evidence and next action |
| Patent cards | Deeper summaries for top-priority records |
| Tag dictionary | Definitions, inclusions, exclusions, multi-label policy, and version |
| Review plan | Technical, business, data-quality, and legal follow-up queues |

Use this rationale pattern:

```text
Selected because [record] represents [solution route] for [technical problem].
[Evidence field] supports [bounded observation]. It is relevant to [decision context]
and merits [read / monitor / compare / technical reference / counsel review]
because [defined signal], subject to [limitation].
```

## Tagging and recommendation rules

- Permit multi-label product, application, problem, solution, and effect fields when justified.
- State whether multi-label aggregate counts duplicate records.
- Give every label inclusion, exclusion, and ambiguous-case guidance.
- Mark ambiguity `needs_review`; never force a confident tag.
- Keep recommendation priority separate from legal risk and patent validity.
- Do not overfit the taxonomy to one prior project or regional market vocabulary.
- Do not recommend acquisition, licensing, enforcement, or design-around action without appropriate specialist review.

## Quality gate

- Every selected record has a specific, traceable reason.
- Criteria, missing-data handling, and family deduplication are reproducible.
- Taxonomy version and classification status are explicit.
- Business, technical, and legal queues remain separate.
- The index is machine-readable and human-auditable.
- No confidential source identifier or historical recommendation sentence remains.

## Selection-rubric worksheet

| Dimension | Required definition |
|---|---|
| Relevance | Relationship to the decision and taxonomy branch |
| Representativeness | How well the record explains a route, not how typical it merely appears |
| Evidence depth | Available claim/description support and readability |
| Family signal | Declared family definition and coverage measure |
| Citation signal | Type, cutoff, age bias, and source |
| Status signal | Jurisdiction, as-of date, and source |
| Diversity | Route, organization, jurisdiction, or application coverage |
| Missing data | Neutral, penalized, or manually reviewed; state the choice |

### Index integrity checks

1. Validate unique identifiers and family-member relationships.
2. Keep original source values alongside normalized values.
3. Use controlled values for status and review fields.
4. Preserve null/unavailable separately from false, zero, or not applicable.
5. Test multi-label exports for duplicate-count inflation.
6. Verify every recommendation rationale against its evidence locator.
7. Record taxonomy and query versions in the package metadata.

### Review-state contract

Use a controlled progression such as `machine_tagged`, `analyst_reviewed`, `sme_validated`, `legal_review_requested`, and `resolved`. Do not imply that analyst review substitutes for subject-matter or legal review. Preserve reviewer role and review date only when privacy and project policy allow it.

### Handoff artifacts

Deliver the structured index, data dictionary, selection rubric, package membership table, patent cards, evidence register, unresolved queue, and known coverage limitations. A formatted spreadsheet may be included only if it is one of the source-authorized artifacts; the underlying data must remain machine-readable.
