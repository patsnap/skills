# Scenario: Technology Evolution

Use this scenario to convert patent evidence into a technology taxonomy, route-evolution view, technical problem map, and explicitly uncertain hypotheses about future directions.

## Use for questions such as

- How has a technical route changed over time?
- Which branches or sub-routes show increasing attention?
- Which technical problems recur and how are they addressed?
- Which directions merit monitoring or R&D exploration?
- How can patent evidence inform technology or product planning?

## Required inputs

| Input | Requirement |
|---|---|
| `technology_domain` | Required with scope boundaries |
| `known_taxonomy` | Optional user taxonomy; preserve it as a versioned input rather than silently rewriting it |
| `product_or_application_scope` | Add when the decision concerns product planning |
| `date_range` | Define; earliest priority date is often preferable for route evolution |
| `depth` | Branch-level landscape or route-level deep dive |
| `unit_of_analysis` | Define publication, application, or family counting |

## Global PatSnap capabilities

Use `advanced_patent_search` for branch discovery and reproducible result sets. Use `patent_briefing` for selected-record context and `deep_patent_mining` for claims, descriptions, or deeper family evidence when supported. Use `global_core_patent_database` where its installed contract supplies needed structured intelligence. Retrieve full text selectively; do not request every claim and description for a large population without a justified batching plan.

## Analysis flow

1. Draft a three-level taxonomy:
   - Level 1: major technology category;
   - Level 2: route, function, or system branch; and
   - Level 3: specific method, component, application, problem, or effect.
2. Define each label with inclusion, exclusion, positive examples, and near misses.
3. Map query rules to preliminary labels; identify them as automated rule hits.
4. Sample every branch, ambiguous bucket, and negative-control set.
5. Revise and version the taxonomy before full tagging.
6. Create time × branch views only from the validated and adequately covered dataset.
7. Select deep-reading branches based on trend, decision relevance, concentration, and representative evidence—not a fixed quota.
8. Extract technical problem, solution mechanism, architecture or process, and reported effect from selected patents.
9. Form route-evolution hypotheses, record counterevidence, and assign uncertainty.

## Report blocks

| Block | Content |
|---|---|
| Technology taxonomy | Level 1–3 definitions, boundaries, examples, and version |
| Branch activity | Time × branch counts under a stated date and counting basis |
| Technical problem map | Recurrent problems and evidence frequency |
| Solution-route map | Solution clusters with representative patents |
| Evolution timeline | Evidence-backed route shifts and continuity |
| Direction hypotheses | Supporting evidence, counterevidence, uncertainty, and monitoring trigger |

Use hierarchical tables for taxonomy, heatmaps or small multiples for time × branch, a problem × solution matrix for route structure, and patent cards for documentary support. A timeline should mark evidence dates and must not imply uninterrupted development where data are sparse.

## Evidence chain

```text
verified branch measure → reviewed representative patents → problem/solution extraction
→ route hypothesis with counterevidence → bounded product or R&D implication
```

- Do not call a route important because one patent is interesting.
- Do not treat search-rule hits as validated technical categories.
- Claims and detailed descriptions usually provide stronger route evidence than titles alone, but remain patent disclosures rather than proof of implementation.
- Phrase a future direction as a signal or hypothesis with confidence and falsification conditions.
- Check recent-year movement for publication lag and changes in search coverage.
- Do not infer claim scope, infringement, validity, standards essentiality, or product certainty.

## Quality gate

- Every taxonomy label includes clear inclusion and exclusion rules.
- Taxonomy and query versions are recorded.
- Automated, analyst-reviewed, and human-validated labels are visibly distinct.
- Time trends state date basis, unit, scope, and cutoff.
- Each route hypothesis cites multiple representative records where available and addresses counterevidence.
- Recent-year dips are tested for publication lag.
- Confidential source wording and China-only assumptions are absent.

## Taxonomy worksheet

For every label record:

| Field | Purpose |
|---|---|
| `label_id` | Stable machine-readable identifier |
| `display_name` | Clear international English term |
| `parent_id` | Hierarchical relationship |
| `definition` | Technical meaning and system boundary |
| `include` | Positive criteria and synonyms |
| `exclude` | Near neighbors and misleading terms |
| `evidence_fields` | Title, abstract, claim, description, or classification |
| `multi_label_policy` | Whether and how sibling/cross-cutting labels coexist |
| `validation_status` | Rule-hit, analyst-reviewed, SME-validated, or unresolved |
| `version` | Taxonomy version and change reason |

### Evolution checks

1. Confirm that terminology changes are not mistaken for technical change.
2. Compare rule-hit trends with reviewed-tag trends.
3. Inspect whether classification revisions affect older and newer records differently.
4. Separate priority-year emergence from later publication visibility.
5. Look for continuity, branching, convergence, and abandoned routes—not growth alone.
6. Review negative and contradictory examples for each proposed shift.
7. Test route claims across more than one organization where the conclusion is industry-wide.

### Hypothesis record

For each future-direction hypothesis preserve the observation, representative patents, counterevidence, alternative explanation, confidence, monitoring indicator, and condition that would weaken or falsify it. Keep these fields in the evidence register even if the report presents a shorter narrative.

### Handoff artifacts

Pass the versioned taxonomy, rule mapping, validation sample, tagged population, time-basis definition, branch measures, representative evidence, and hypothesis register to reporting. Do not reduce the handoff to a static taxonomy graphic.
