# Stage 6: Build and Render the Evolution Forest

## Position in the workflow

- Input: Stage 5 reviewed labels, taxonomy metadata, crosswalk, and dependent-route evidence.
- Output: evolution-forest data, HTML visualization, and reviewed branch/analogy/evidence-gap candidate registers.
- Downstream: Stage 7 horizon scenarios and decision report.

## Model

The source correctly reframed the output as a forest rather than one forced tree:

```text
Functional unit
├─ supported route trunk A
│  ├─ observed node with evidence
│  ├─ unobserved display node
│  └─ evidence-supported dependent route C
├─ supported route trunk B
└─ unresolved route candidate
```

The functional unit is the root. Multiple route trunks may coexist. A route edge requires causal evidence. An unobserved node is a dataset state, not proof of global white space.

## Required inputs

- product/system scope and evidence cutoff;
- hierarchy of systems, subsystems, components, and critical units;
- accepted evidence register;
- Stage 5 label records;
- analytical taxonomy ID and definitions;
- display taxonomy ID and explicit crosswalk when different;
- review and disagreement status;
- search logs and coverage limitations;
- patent family/count rule;
- organization normalization rule;
- authorized output path and overwrite decision.

## Taxonomy integrity

The localized package preserves:

- `analytical-route-taxonomy-v1-localized` for reasoning; and
- `compact-display-routes-v1-localized` for the bundled renderer.

Before rendering analytical labels, validate a crosswalk. Each mapping is exact, broader, narrower, approximate, or unmapped. Approximate/unmapped items remain visible in a review queue and are not silently coerced.

## Core concepts

### Supported route trunk

A route becomes a displayed trunk when:

- at least one accepted, reviewed record maps to it; and
- the evidence is sufficient for the declared display purpose.

Do not use a universal minimum of two or three records. One direct high-quality record may justify a sparse trunk; many weak records may not. Record the project-specific inclusion rule.

### Observed node

A node with one or more accepted records. Display:

- record count under the declared unit;
- representative record IDs;
- date range;
- evidence types;
- confidence and review status;
- contradictions or limitations.

### Sparse-evidence node

A node with limited accepted evidence under the project rule. Sparse is about evidence coverage, not technical immaturity.

### Unobserved display node

A node in the selected display skeleton with zero accepted records. Phrase exactly:

> Not observed in the reviewed dataset.

Possible explanations include:

- genuine research gap;
- search recall or language gap;
- inaccessible evidence;
- unpublished or trade-secret activity;
- taxonomy mismatch;
- different terminology or classification;
- evidence cutoff and publication lag;
- infeasible or irrelevant transition.

### Branch point

A node with accepted evidence that a second route depends on the parent state. A branch point is topological; it is not synonymous with a high-value or breakthrough patent.

### Analogy candidate

A source solution that may transfer to another unit under documented conditions. Route/node distance is only a discovery signal.

### Evidence-gap candidate

An unobserved next-node hypothesis selected for additional research or experimentation. It is not a patent white-space, novelty, FTO, or commercial-opportunity conclusion.

## Forest construction workflow

### Step 1 — Validate inputs

Reject:

- unreviewed payloads;
- missing or unknown taxonomy IDs;
- unresolved evidence references;
- invalid nodes;
- records beyond the evidence cutoff;
- duplicate IDs;
- negative counts;
- missing functional units;
- accepted dependency edges without evidence.

### Step 2 — Group records

Group by:

1. hierarchy level;
2. functional unit;
3. source track;
4. taxonomy and route;
5. node;
6. evidence type;
7. date.

Do not combine analytical and display node IDs before applying the crosswalk.

### Step 3 — Derive node aggregates

For each unit/route/node derive:

- accepted record IDs;
- publication/family counts as separately labeled units;
- evidence-type counts;
- earliest/latest dates;
- organizations;
- confidence distribution;
- review status;
- contradicting evidence IDs;
- representative records selected by declared criteria.

Do not select a representative solely by citation count. Prefer directness, technical relevance, evidence quality, and clear conditions.

### Step 4 — Select parallel trunks

Use a declared rule, for example:

- reviewed evidence exists;
- route fit meets minimum confidence;
- no material unresolved taxonomy conflict;
- route contributes to the decision.

Sort for presentation by a disclosed criterion. Visual order does not imply a single dominant route unless analysis supports that conclusion.

### Step 5 — Create accepted branch edges

Accept only Stage 5 edges with:

- parent route and node;
- dependent route;
- causal rationale;
- evidence ID and location;
- confidence;
- independent review.

### Step 6 — Create heuristic edge candidates

Co-occurrence may generate a candidate review queue when:

- several independent records share two route labels;
- time/order and mechanism are compatible;
- the relationship is not explained by generic multi-functionality.

Label such items `cooccurrence_candidate`. Do not render them as accepted dependency edges unless reviewed.

### Step 7 — Generate analogy candidates

Use route similarity, functional similarity, or node differences only to discover candidates. Then review:

- mechanism;
- scale;
- conditions;
- materials/media;
- manufacturing;
- reliability;
- cost;
- safety/regulation;
- interfaces;
- intellectual-property constraints;
- required experiment.

### Step 8 — Generate evidence-gap candidates

For a supported trunk:

1. identify the current observed frontier under the declared taxonomy;
2. identify a candidate adjacent node along the route's declared direction;
3. confirm that no accepted record occupies it;
4. run targeted gap-check searches across synonyms, languages, classifications, citation paths, and adjacent mechanisms;
5. record search coverage and remaining uncertainty;
6. test physical/technical relevance;
7. define a falsifiable experiment or research question;
8. retain as a candidate only after review.

Never equate the highest observed ordinal node with the only “current” state. Different architectures may coexist.

## Pseudocode

```text
validate payload, taxonomy IDs, crosswalk, evidence references, and review status

for each hierarchy level:
  for each functional unit:
    labels = accepted labels for unit
    for each route supported by reviewed labels:
      aggregate accepted records by node and evidence type
      build route trunk in declared taxonomy order
      attach accepted dependency edges
      queue unresolved co-occurrence candidates
      derive adjacent-node evidence-gap candidates for review

for each route across units:
  discover analogy candidates
  apply transfer screen

reconcile all displayed counts with the accepted evidence register
render HTML from reviewed compact-taxonomy payload
```

## Forest data contract

```json
{
  "schema_version": "2.0",
  "review_status": "reviewed",
  "meta": {
    "project": "Project name",
    "report_date": "2026-08-08",
    "evidence_cutoff": "2026-07-31",
    "analytical_taxonomy_id": "analytical-route-taxonomy-v1-localized",
    "display_taxonomy_id": "compact-display-routes-v1-localized",
    "patent_count_unit": "simple families"
  },
  "forest": [],
  "accepted_edges": [],
  "edge_candidates": [],
  "analogy_candidates": [],
  "evidence_gap_candidates": [],
  "search_log_ids": [],
  "limitations": [],
  "review": {}
}
```

## Functional-unit record

```json
{
  "unit_id": "P4.2",
  "unit_name": "Beamforming processor",
  "hierarchy": ["Product", "Control", "Capture", "Microphone array"],
  "parallel_trunks": [
    {
      "route": 11,
      "route_name": "Linear-combination or array geometry",
      "nodes": [
        {
          "node": "planar array",
          "node_index": 4,
          "evidence_ids": ["E17", "E22"],
          "evidence_type_counts": {"patent": 1, "paper": 1},
          "state": "observed",
          "confidence": "high"
        }
      ],
      "limitations": []
    }
  ]
}
```

## Accepted edge record

```json
{
  "edge_id": "B1",
  "unit_id": "P4.2",
  "from_route": 7,
  "from_node": "adaptive matching",
  "to_route": 6,
  "dependency": "The feedback controller depends on the tunable parameter state.",
  "evidence_ids": ["E31"],
  "confidence": "medium",
  "review_status": "reviewed"
}
```

## Analogy-candidate record

```json
{
  "analogy_id": "A1",
  "source_unit": "Radar array",
  "target_unit": "Microphone array",
  "shared_function": "Shape spatial response",
  "route": 11,
  "source_evidence_ids": ["E44"],
  "matching_conditions": [],
  "different_conditions": [],
  "transfer_barriers": [],
  "required_validation": "Scaled array test under target frequencies and geometry",
  "confidence": "low",
  "review_status": "reviewed"
}
```

## Evidence-gap candidate record

```json
{
  "gap_id": "G1",
  "unit_id": "P4.2",
  "route": 11,
  "candidate_node": "spherical or conformal array",
  "status": "not observed in the reviewed dataset",
  "supporting_evidence_ids": [],
  "contradicting_evidence_ids": [],
  "gap_search_ids": ["S81", "S82"],
  "technical_relevance": "Why this adjacent state might matter",
  "feasibility_questions": [],
  "invalidation_conditions": [],
  "confidence": "low",
  "review_status": "reviewed-candidate"
}
```

## Bundled forest renderer

Use:

```bash
python assets/forest/render_forest.py \
  --records reviewed-forest-records.json \
  --out evolution-forest.html \
  --title "Technology Evolution Forest"
```

Required compact renderer payload:

```json
{
  "schema_version": "2.0",
  "review_status": "reviewed",
  "taxonomy_id": "compact-display-routes-v1-localized",
  "part_names": {"P4.2": "Beamforming processor"},
  "records": [
    {
      "id": "E17",
      "publication_id": "US0000000A1",
      "unit_id": "P4.2",
      "core": "Reviewed technical change",
      "labels": {"11": {"node": "11.3", "action": "Reviewed action"}},
      "dependent_routes": []
    }
  ]
}
```

The renderer:

- validates the exact compact taxonomy;
- rejects unreviewed input;
- escapes all data;
- derives hit states;
- displays every node in each active route;
- distinguishes multiple records, one record, and not observed;
- renders only explicit evidence-supported dependency edges;
- contains no external runtime;
- refuses overwrite unless authorized;
- writes atomically.

## Visual semantics

### Multiple accepted records

Means two or more accepted records under the payload's record unit. It does not mean mature, commercial, safe, or legally clear.

### One accepted record

Means sparse accepted evidence. It may be important but requires careful review.

### Not observed

Means zero accepted records in this dataset. It is not labeled “opportunity” by the localized renderer.

### Route frame

Shows a route skeleton for orientation. It does not assert that every system must traverse every node or that traversal is inevitable.

### Dependency annotation

Shows only an accepted evidence-supported edge. The evidence ID remains visible.

## Required outputs

- full analytical forest JSON;
- compact renderer payload with crosswalk provenance;
- self-contained forest HTML;
- accepted branch-point register;
- heuristic edge-candidate queue;
- analogy-candidate register;
- evidence-gap candidate register;
- taxonomy/crosswalk version;
- count reconciliation;
- review and limitation log.

## Stage gate

Do not advance until:

- taxonomy IDs and crosswalk are explicit;
- every displayed observed node resolves to accepted evidence;
- count units reconcile;
- route inclusion rules are disclosed;
- accepted branch edges have causal evidence and review;
- heuristic co-occurrence remains a candidate;
- analogies include transfer barriers;
- evidence gaps use bounded language and gap-check searches;
- representative records are not selected solely by citation;
- HTML escapes all content and has no external runtime;
- overwrite is explicit and bounded;
- no source-case facts or hard-coded unit names remain in the renderer;
- accessibility, narrow-screen behavior, and print output are reviewed.

## Limitations

1. Taxonomy boundaries are interpretive.
2. The analytical and display taxonomies are not identical.
3. Search and full-text access affect observed-node density.
4. Multiple technical architectures can coexist at different nodes.
5. Co-occurrence is not causal dependency.
6. A visual sequence may imply inevitability unless limitations are prominent.
7. Evidence gaps may reflect secrecy, language, indexing, or publication lag.
8. Cross-domain transfer requires engineering validation.
9. The bundled renderer displays functional-unit roots; deeper nested hierarchy remains in the analytical data and report.
10. The forest is not a legal, commercial, safety, or investment conclusion.
