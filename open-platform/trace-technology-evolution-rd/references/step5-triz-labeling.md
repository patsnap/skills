# Stage 5: Evidence-Based Evolution-Route Labeling

## Position in the workflow

- Input: Stage 4 accepted evidence and review-depth queue.
- Output: reviewed route labels, disagreements, branch-edge candidates, and evidence-linked observations.
- Downstream: Stage 6 evolution forest.
- The route framework is TRIZ-inspired and versioned. It organizes evidence; it does not prove a universal law, maturity, value, or inevitable next state.

## Critical taxonomy note

The frozen source contains two non-equivalent route-node dictionaries:

1. the longer methodology dictionary in this reference; and
2. the compact visualization dictionary in `assets/forest/triz_forest_common.py`.

Do not silently treat them as one authority. Every label records `taxonomy_id`. The localized analytical taxonomy below is `analytical-route-taxonomy-v1-localized`. The renderer accepts only `compact-display-routes-v1-localized`. A project that renders analytical labels must maintain an explicit, reviewed crosswalk.

## Labeling principles

1. Label the documented technical change, not the title or marketing theme.
2. Use zero, one, or multiple route labels only when each has independent evidence.
3. Record exact evidence text or a precise document location.
4. State the mechanism, conditions, and functional unit.
5. Separate observed result, proposed implementation, simulation, and expectation.
6. Record alternative labels and uncertainty.
7. Distinguish technology-route position from maturity or adoption.
8. Keep patent, paper, standard, case, product, and web evidence types explicit.
9. Do not average reviewer node choices when the taxonomy is ordinal and the disagreement is substantive.
10. Do not classify a paper as ahead of patents merely because it is a paper.

## Required input fields

Each record has:

- evidence ID;
- evidence type;
- stable identifier and source link;
- date and evidence cutoff;
- functional unit and SVOP anchor;
- source track: in-domain or cross-domain;
- reviewed evidence text/location;
- technical mechanism and conditions;
- Stage 4 eligibility and review depth;
- confidence and limitations;
- organization metadata where relevant;
- patent family/count information where relevant.

## Evidence requirements by type

### Patents

Use relevant:

- independent/dependent claims;
- description passages;
- examples or measured results;
- drawings when necessary;
- family members when claim differences matter.

A title or abstract may support discovery. It normally cannot support a detailed node, dependency edge, or strong forecast alone.

### Papers

Use:

- abstract for initial relevance;
- methods and system conditions;
- results and uncertainty;
- limitations and negative findings;
- review or publication status.

Do not equate laboratory demonstration with manufacturability, regulatory readiness, or adoption.

### Standards and official documents

Use exact:

- document identifier;
- status and date;
- clause, work item, or technical requirement;
- jurisdiction or scope.

### Engineering cases and products

Use direct evidence of:

- architecture or mechanism;
- deployment state;
- operating conditions;
- performance and limitations;
- responsible organization and date.

### Web and current-awareness evidence

Use it for context or corroboration only at the review depth it supports. A press release does not establish a claim limitation or independent technical result.

## Analytical route taxonomy

### Route 1 — Single, dual, multiple, and consolidated systems

Candidate nodes:

1. single system;
2. dual system;
3. multiple similar systems;
4. multiple dissimilar systems;
5. counter-system;
6. consolidated system.

Interpretation:

- early nodes add redundancy, capacity, diversity, or cooperative function;
- the terminal consolidation node may reduce components while preserving function;
- higher ordinal position is not synonymous with greater complexity.

Evidence questions:

- What constitutes a system boundary?
- Are systems actually independent?
- Is the change additive, cooperative, counteracting, or consolidating?
- Does consolidation preserve or improve the required function?

### Route 2 — Functional expansion and trimming

Candidate nodes:

1. single function;
2. multiple functions;
3. supersystem participation;
4. extreme functional focus;
5. self-service or self-maintenance.

Interpretation:

- the route may expand function before trimming or internalizing support;
- later nodes can mean simplification, integration, or removal;
- “self-service” requires a defined function and evidence.

### Route 3 — Division toward smaller scales

Candidate nodes:

1. whole structure;
2. blocks or segments;
3. particles;
4. powder-scale elements;
5. colloidal or dispersed state;
6. molecular scale;
7. ionic scale;
8. atomic scale;
9. field- or quantum-mediated state.

Interpretation:

- use physical scale and mechanism, not fashionable terminology;
- compare actual dimensions and operating state;
- field-mediated behavior may not be a direct successor for every system.

### Route 4 — Surface characteristics

Candidate nodes:

1. smooth or untreated surface;
2. roughened surface;
3. capillary-featured surface;
4. porous surface;
5. textured or architected surface;
6. adaptive surface;
7. active surface with actuation.

Evidence questions:

- What surface property changes?
- Is behavior passive, responsive, or actively controlled?
- What stimulus, actuator, and feedback are present?
- Under what operating conditions is the effect measured?

### Route 5 — Internal structure

Candidate nodes:

1. solid;
2. cavity;
3. multiple cavities;
4. cellular or honeycomb structure;
5. periodic lattice;
6. quasi-periodic structure;
7. topological structure;
8. active-field structure.

Do not infer node order from visual complexity alone. Record mechanism and topology.

### Route 6 — Controllability

Candidate nodes:

1. uncontrolled;
2. manual control;
3. partial automation;
4. automatic control;
5. adaptive control;
6. model- or AI-assisted decision;
7. self-modifying or self-optimizing behavior.

Requirements:

- identify sensor, controller, actuator, objective, and feedback where applicable;
- distinguish deterministic rules, optimization, machine learning, and autonomous adaptation;
- do not call ordinary automation “AI”;
- safety, validation, and human oversight remain separate dimensions.

### Route 7 — Parameter or frequency matching

Candidate nodes:

1. fixed parameter;
2. gradient variation;
3. intermittent or discrete variation;
4. matched parameter or frequency;
5. adaptive matching;
6. active tuning.

Specify parameter, range, control method, target, and time response.

### Route 8 — Dynamization

Candidate nodes:

1. static or rigid;
2. one degree of freedom;
3. multiple degrees of freedom;
4. compliant or flexure-based behavior;
5. fully flexible behavior;
6. rheological or continuously reconfigurable medium.

State geometry, constraints, actuation, reversibility, and load.

### Route 9 — Solid geometry

Candidate nodes:

1. orthogonal or prismatic geometry;
2. polygonal geometry;
3. circular geometry;
4. elliptical geometry;
5. spiral geometry;
6. fractal geometry;
7. biomimetic geometry.

Geometry is not inherently better at a later node. Connect it to a measurable function.

### Route 10 — Surface geometry

Candidate nodes:

1. plane;
2. one-dimensional curvature;
3. two-dimensional curvature;
4. free-form or irregular curvature;
5. topological surface.

Record dimensional definition, curvature, fabrication, and functional consequence.

### Route 11 — Linear-combination or array geometry

Candidate nodes:

1. point;
2. line;
3. curve;
4. planar array;
5. spherical or conformal array;
6. complex array;
7. fractal array.

Record element count, spacing, topology, control, operating wavelength/scale, and functional effect.

## Route-direction semantics

The source's key correction is retained: movement to a later declared node means movement along that route's own ordering, not universal movement toward complexity.

| Route | Possible direction | Review warning |
|---|---|---|
| 1 | addition, diversity, counter-system, then consolidation | terminal consolidation may be simpler |
| 2 | expansion followed by trimming or self-service | later can mean fewer parts/functions |
| 3 | finer scale or field mediation | feasibility and scale transition must be evidenced |
| 4 | passive to adaptive/active surfaces | activity requires stimulus/actuation evidence |
| 5 | solid to architected/active internal structure | topology labels need precise definitions |
| 6 | control and adaptation | adoption/safety is not route position |
| 7 | fixed to adaptive/active matching | specify the matched parameter |
| 8 | rigid to flexible/reconfigurable | flexibility can reduce other performance |
| 9 | changing solid geometry | later geometry is not intrinsically superior |
| 10 | changing surface curvature/topology | manufacturing limits matter |
| 11 | increasing array dimensionality/topology | element count alone may not establish a node |

The TRIZ ideality expression may be used as a qualitative prompt—useful function relative to costs and harms—but not as a measured universal objective unless the project defines numerator, denominator, units, and stakeholders.

## Label assignment workflow

### Step 1 — Read and extract

Extract:

- technical change;
- baseline and comparison;
- mechanism;
- functional unit;
- affected parameter;
- operating conditions;
- result state;
- maturity evidence;
- limitations.

### Step 2 — Generate candidate routes

List plausible routes without selecting a node. Include “no route fit.”

### Step 3 — Select node candidates

Compare the documented change against the declared node definitions. Do not infer unmentioned predecessor nodes.

### Step 4 — Test alternatives

Ask:

- Is this primarily geometry, structure, controllability, matching, or system count?
- Are two routes independently evidenced or is one merely descriptive?
- Does the label depend on a marketing term?
- Is the node distinguishable under the taxonomy definitions?
- Would another reviewer reproduce it from the cited text?

### Step 5 — Record confidence

Confidence reflects:

- evidence directness;
- taxonomy fit;
- condition clarity;
- alternative-label strength;
- reviewer agreement.

### Step 6 — Review

High-impact, low-confidence, route-defining, or dependency-edge records receive independent review.

## Review depth

Use the Stage 4 review plan:

- **Full**: claims/methods/results, all route fields, alternatives, maturity, transfer, and dependency review.
- **Standard**: reviewed text, route/node, rationale, confidence, and limitations.
- **Limited**: route-family context only; no precise node or forecast.
- **Excluded**: no label.

Do not decide depth from a score alone.

## Independent review and agreement

Create a stratified review sample that includes:

- all proposed dependency edges;
- all low-confidence labels;
- all route-defining earliest/latest nodes;
- all records used in high-impact forecasts;
- a random sample across tracks, types, units, and analysts.

Measure:

- route-family agreement;
- exact-node agreement;
- adjacent-node disagreement;
- multi-label agreement;
- evidence-location agreement;
- confidence calibration.

When reviewers disagree:

- compare evidence and definitions;
- resolve with a domain reviewer where material;
- retain both candidates if unresolved;
- do not take the numeric average of nodes;
- lower confidence and record the decision.

The source's fixed 5% sample is not universal. Set sample size by risk, volume, expected disagreement, and decision importance.

## Evidence-supported dependent routes

A route B may be represented as dependent on route A only when:

1. the source record clearly locates the parent route and node;
2. a distinct route dimension is also documented;
3. the route B implementation depends causally on the route A state;
4. a precise evidence passage supports the dependency;
5. an independent reviewer accepts the relationship.

Required fields:

```json
{
  "from_route": 7,
  "from_node": "adaptive matching",
  "to_route": 6,
  "dependency": "Control is enabled by the tunable parameter state",
  "evidence_id": "E17",
  "evidence_location": "Claim 1 and paragraph 0042",
  "confidence": "medium",
  "review_status": "reviewed"
}
```

Mere multi-label co-occurrence is not causality. A co-occurrence heuristic may create a review candidate, never an accepted edge without evidence.

## Papers and potential leading signals

For papers:

- record laboratory, simulation, prototype, pilot, or other maturity state;
- compare actual dates with patent evidence;
- compare mechanism and conditions;
- record manufacturing, scale, reliability, cost, safety, and regulatory gaps;
- use “potential leading signal” only with a defined baseline and evidence.

Do not infer that a paper node two positions beyond a patent node means a fixed number of years of lead.

## Breakthrough observations

The source used `breakthrough=true`. Localize this to a bounded observation:

- first observed in the reviewed dataset;
- materially different mechanism under declared conditions;
- corroborated by independent evidence;
- potential route-defining record;
- academic first demonstration;
- not established as first globally.

Every such observation includes search scope and a non-globality disclaimer unless a dedicated novelty search supports stronger language.

## Analogy candidates

An analogy record includes:

- source and target functional units;
- shared mechanism;
- route and node;
- conditions that match;
- conditions that differ;
- transfer barriers;
- safety, regulatory, manufacturing, cost, and interface consequences;
- supporting and contradicting evidence;
- confidence and required experiment.

Node distance alone is insufficient.

## Label record schema

```json
{
  "evidence_id": "E17",
  "evidence_type": "patent",
  "taxonomy_id": "analytical-route-taxonomy-v1-localized",
  "unit_id": "P4.2",
  "source_track": "cross_domain_patent",
  "review_depth": "full",
  "labels": [
    {
      "route": 11,
      "route_name": "Linear-combination or array geometry",
      "node": "spherical or conformal array",
      "node_index": 5,
      "evidence_location": "Claim 1; paragraphs 0031–0037",
      "evidence_excerpt": "Short reviewed excerpt within permitted limits",
      "reasoning": "The disclosed sensor elements form a conformal array.",
      "alternative_labels": [],
      "confidence": "high"
    }
  ],
  "maturity": {
    "state": "prototype",
    "method": "Evidence-based qualitative assessment",
    "evidence_ids": ["E17"]
  },
  "potential_leading_signal": false,
  "route_defining_observation": false,
  "dependent_routes": [],
  "analogy_candidates": [],
  "limitations": [],
  "reviewer": "Technical reviewer",
  "review_status": "reviewed"
}
```

## Taxonomy crosswalk

If a Stage 6 renderer uses the compact display taxonomy, create a project-level crosswalk with:

- analytical taxonomy ID;
- display taxonomy ID;
- analytical route/node;
- display route/node;
- mapping type: exact / broader / narrower / approximate / unmapped;
- rationale;
- reviewer;
- version.

Approximate mappings must be visible. Do not modify evidence labels merely to fit the renderer.

## Stage gate

Do not advance until:

- every label names a taxonomy version;
- every node cites reviewable evidence;
- title-only items have no detailed node;
- maturity and route position are separate;
- alternatives and uncertainty are recorded;
- dependent routes have causal evidence and independent review;
- co-occurrence is not accepted as causality;
- potential leading signals have a defined comparison baseline;
- analogy candidates include transfer barriers;
- high-impact and low-confidence labels receive review;
- unresolved disagreements remain visible;
- any renderer crosswalk is explicit and reviewed.

## Outputs

- labeled evidence register;
- taxonomy definition and version;
- taxonomy crosswalk when required;
- reviewer sample and agreement report;
- disagreement and resolution log;
- dependent-route candidate and accepted-edge registers;
- route-defining observation register;
- analogy-candidate register;
- limitations and unresolved review queue;
- Stage 6 handoff.

## Limitations

- Route and node boundaries are interpretive.
- Taxonomy coverage differs by technology domain.
- The source's two dictionaries are structurally inconsistent.
- Evidence access and translation affect reproducibility.
- Patent disclosure may be broad, strategic, or incomplete.
- Papers may be early, non-replicated, or difficult to manufacture.
- Reviewer agreement may remain imperfect.
- Route position does not establish inevitability, timing, value, safety, or legal status.
