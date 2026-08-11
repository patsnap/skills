# Scenario: Technical Solution Deep Dive

Use this scenario to examine a defined technical problem, technology branch, product feature, component constraint, or implementation route at patent level.

## Use for questions such as

- Which disclosed solutions address a defined technical problem?
- How do organizations approach the same problem differently?
- Which patents best represent each route?
- Which technical effects and trade-offs are reported?
- What evidence could inform R&D or product planning?

## Required inputs

| Input | Requirement |
|---|---|
| `technical_problem_or_branch` | Required, framed neutrally |
| `technology_domain` | Required with clear relationship to the problem |
| `selected_organizations` | Optional for route comparison |
| `product_or_application_scope` | Optional for decision relevance |
| `selection_basis` | Relevance, route coverage, evidence depth, and diversity criteria |
| `review_depth` | Abstract screen, claim-assisted review, or description-level reading |

Do not impose a fixed number of patents per route. Select enough evidence to represent meaningful variation, and report sparse routes honestly.

## Global PatSnap capabilities

Use `advanced_patent_search` for focused retrieval. Use `patent_briefing`, `deep_patent_mining`, and, where suitable, `global_core_patent_database` to inspect selected records, family context, claims, descriptions, citations, status, or images that the installed contracts expose. Confirm the live schema and treat unavailable fields as unavailable; do not translate legacy source operation labels into nonexistent calls.

## Analysis flow

1. Define the technical problem, affected system boundary, success criteria, and exclusions.
2. Construct focused query sets from technology, problem, effect, component, and application concepts.
3. Screen titles and abstracts; retain near misses to test the boundary.
4. Cluster records by technical means rather than title similarity alone.
5. Review claims and descriptions selectively for representative and ambiguous records.
6. Extract:
   - problem and operating context;
   - technical means, architecture, material, process, or control logic;
   - disclosed or claimed effect;
   - implementation relevance and dependencies;
   - limitations, trade-offs, and uncertainty; and
   - evidence field and location.
7. Compare organization-specific routes when requested.
8. Recommend which records to read, monitor, compare, use as technical references, or send for counsel review.

## Report blocks

| Block | Content |
|---|---|
| Problem framing | Engineering context, boundary, and decision relevance |
| Candidate set | Query logic, counts, screening, and known recall risks |
| Solution clusters | Route definitions and distinguishing technical means |
| Problem × solution matrix | Problem, route, effect, evidence, and representative records |
| Organization × route comparison | Only under a normalized organization scope |
| Patent evidence cards | Concise technical reading and selection reason |
| Implications | Bounded R&D, product, portfolio, or follow-up actions |

### Patent evidence card

| Field | Content |
|---|---|
| Representative record | Publication or family identifier |
| Normalized assignee | With unresolved ownership caveat where relevant |
| Technical problem | Source-grounded formulation |
| Technical means | Mechanism, architecture, process, or component |
| Reported effect | Distinguish claimed, described, measured, and inferred effects |
| Evidence | Abstract, claim, description, drawing, family, or dated event |
| Selection reason | Relevance, representativeness, route diversity, family/citation signal, or decision fit |
| Next action | Read, monitor, compare, technical reference, or counsel review |

## Evidence rules

- Ground problems and effects in the patent record; cite the field or passage location.
- Require more than one record for a cluster unless it is explicitly a single notable disclosure.
- Do not treat a disclosed effect as independently validated experimental performance.
- Do not infer infringement, non-infringement, claim scope, or design-around feasibility.
- Describe legal relevance as an input to later counsel review.
- A representative patent may inspire an R&D question but does not demonstrate market adoption.

## Quality gate

- The technical problem and system boundary are explicit.
- Clusters are defined by understandable technical distinctions.
- Every patent card has traceable evidence and a documented selection reason.
- Sparse and contradictory evidence remains visible.
- R&D implications are separated from legal follow-up.
- No confidential source identifiers or China-only assumptions remain.

## Route-definition worksheet

| Field | Record |
|---|---|
| Route label | Clear technical name, not a marketing label |
| Defining means | Mechanism, architecture, material, process, or control feature |
| Included variants | Known implementations within the route |
| Excluded neighbors | Similar results reached through materially different means |
| Dependencies | Required components, inputs, operating conditions, or upstream processes |
| Reported effects | With claim/description/abstract evidence status |
| Trade-offs | Cost, complexity, performance, manufacturability, safety, or integration considerations |
| Representative records | Selection rationale and evidence location |

### Deep-reading checks

1. Confirm that the representative publication contains the evidence attributed to the family.
2. Distinguish independent-claim features from optional embodiments.
3. Separate applicant assertions from comparative or measured results.
4. Note whether translations, OCR, or machine-generated abstracts may affect interpretation.
5. Check family members for clearer text without merging materially different claim sets.
6. Identify routes represented only by a single disclosure.
7. Record contradictory effects, implementation constraints, and missing parameters.

### Comparative interpretation

Compare technical means on the same system boundary and decision criteria. Do not score unlike routes on a single composite scale unless the user supplies weights and the evidence supports each dimension. Use a trade-off table when route selection depends on competing performance, cost, integration, or maturity considerations.

### Handoff artifacts

Preserve focused queries, screening decisions, route definitions, evidence extracts, selected publications/families, trade-off observations, and unresolved questions. Counsel or technical experts must be able to distinguish the analyst’s synthesis from the patent text.

Record the search and evidence cutoff, translation status, and reviewer role. If the source text is unavailable, mark the route interpretation provisional rather than filling the gap from related family members without disclosure.

Keep the final route names consistent with the versioned taxonomy used by the broader landscape.
