---
name: develop-patent-design-arounds-ip
description: Develop and screen single-patent design-around concepts using an application-requirements baseline, claim-feature and functional reconstruction, TRIZ trimming, evidence-backed function-oriented search, differentiated concept engineering, and jurisdiction-specific claim risk review. Use when a user asks for patent design-around options, non-equivalent alternatives, or a preliminary infringement-risk comparison against a specific patent.
---

# Develop Patent Design-Arounds

## Purpose

Develop technically plausible alternatives to a patented implementation and screen their claim-related risk.
The workflow combines:

- application-requirements definition;
- claim and disclosure reconstruction;
- feature-level functional modelling;
- TRIZ trimming;
- function-oriented cross-domain search;
- concept generation and engineering screening;
- claim-by-claim literal, equivalents, and prosecution-history review.

This skill does not provide a non-infringement opinion, freedom-to-operate opinion, or legal conclusion.
Every result is a preliminary design and legal-risk screen requiring qualified counsel and engineering validation.

## Trigger conditions

Use when the user:

- supplies a patent number, publication, PDF, or claims and requests a design-around;
- asks for technically different alternatives to a claimed solution;
- wants to compare a proposed implementation against one target patent;
- requests TRIZ trimming or function-oriented search for a patent problem;
- asks whether a proposed alternative may reduce claim risk.

For a portfolio or several blocking patents, use `design-around-multiple-patents-ip` if installed.
This skill remains self-contained and can still analyze one patent at a time.

## Required inputs

### Patent and legal context

- target patent/publication and authoritative claim text;
- target jurisdiction;
- relevant claim set and claim version;
- legal status and relevant date;
- prosecution, opposition, reexamination, invalidation, or post-grant history when relevant;
- related family members or continuation/divisional claims that may matter;
- requested legal-risk depth and counsel-review context.

### Product and engineering context

- current or proposed product/process architecture;
- intended use and operating environment;
- mandatory performance targets and tolerances;
- cost, reliability, safety, size, energy, manufacturing, regulatory, and supply constraints;
- validation methods and acceptance criteria;
- features that may or may not be changed;
- schedule and technology-readiness expectations.

If implementation facts are incomplete, use explicit assumptions and mark the legal comparison provisional.

## Verified PatSnap MCP services

Use the English interface and English output.
Confirm the live tool schema before calling a connector.
Do not invent tool names, fields, aggregations, or legal conclusions.

### Required: Advanced Patent Search

- Connector key: `advanced_patent_search`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`
- Use: identify the target record, related claims/family documents, prosecution-relevant references,
  and cross-domain patent evidence for function-oriented search.

### Required: Patent Briefing

- Connector key: `patent_briefing`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- Use: retrieve bibliography, claims, description, family, status, translations, drawings,
  and technical problem/solution/effect summaries.

### Recommended: Deep Patent Mining

- Connector key: `deep_patent_mining`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-mining
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-mining`
- Use: analyze technical topics, problems, solutions, effects, classifications, materials,
  and application domains for reconstruction and cross-domain search.

### Recommended: Global Core Patent Database

- Connector key: `global_core_patent_database`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/core-patents
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/core-patents`
- Use: inspect family, legal events, litigation, reexamination/invalidation, licensing, transfer,
  citations, full text, and PDF evidence where the live connector supports them.

Patent MCPs do not replace official prosecution files, court dockets, statutes, case law,
standards, laboratory evidence, or destination-counsel review.

## Dependency policy

The source package names three external skills that are not included in its topology.
Do not claim those skills exist and do not create new package files.
This file embeds the required contracts for:

- application requirements;
- claim-to-functional-model reconstruction;
- static HTML report generation.

If compatible installed skills are available, they may assist only when their schemas satisfy the contracts below.
The outputs must still pass this skill’s gates.

## Workflow map

```text
Stage 0: Application requirements baseline
  -> Stage I: Claim-feature and functional reconstruction (Steps 1–8)
  -> Stage II: TRIZ trimming (Step 9)
  -> Stage III: Function-oriented search (Step 10)
  -> Stage IV: Differentiated concept development (Step 11)
  -> Stage V: Jurisdiction-specific claim risk screening (Step 12)
  -> Markdown + static HTML report + five-stage traceability table
```

Stable IDs are mandatory:

- `REQ-###` for requirements;
- `CLM-###` for claims;
- `F-###` for claim features;
- `OBJ-###` for objects/components;
- `FUN-###` for functions;
- `DIR-###` for trimming directions;
- `TP-###` for trimming problems;
- `FOS-###` for searched solution principles;
- `CON-###` for developed concepts;
- `EV-###` for evidence;
- `RISK-###` for risk findings.

## Stage 0 — Define the application requirements baseline

Complete this stage before interpreting “excessive,” “insufficient,” “unnecessary,” or “feasible.”

### Inputs

- business and user need;
- product specification;
- use scenario;
- target architecture;
- constraints and validation environment.

### Requirements-card schema

```text
requirement_id
category
metric_or_condition
target_value
tolerance_or_range
unit
priority: must | should | could
verification_method
source
assumption_state
owner
```

### Required categories

- primary function;
- performance;
- reliability and lifetime;
- safety and regulatory constraints;
- manufacturability and supply;
- size, weight, energy, and environment;
- interfaces and interoperability;
- cost and maintenance;
- user/human factors;
- validation and acceptance.

### Stage 0 procedure

1. Separate hard requirements from preferences.
2. Normalize units and test conditions.
3. Record target, tolerance, priority, and verification method.
4. Identify conflicts and missing decision criteria.
5. Map each requirement to the affected subsystem or function.
6. Mark assumptions that require user or engineering confirmation.
7. Freeze a versioned requirements card for later scoring.

### Downstream use

The requirements card controls:

- whether a patent function is excessive or unnecessary;
- which components are eligible for trimming;
- FOS parameter targets;
- feasibility scoring;
- concept performance estimates;
- test plans and final ranking.

An application difference can be a strong design-around entry point,
but only when supported by facts and a claim-feature comparison.

## Stage I — Claim-feature and functional reconstruction

### Step 1 — Freeze the patent and claim basis

Record:

- publication/grant/application identifiers;
- jurisdiction and family relationship;
- priority, filing, publication, and grant dates;
- legal status as of a stated date;
- claim version and source locator;
- independent claims selected;
- dependent claims that may independently affect the product;
- prosecution and post-grant records available;
- translation source and uncertainty.

Do not analyze a title or abstract as if it were an enforceable claim.
Do not combine limitations from different claim versions without labelling them.

### Step 2 — Decompose claims into fine-grained features

Split each selected claim into atomic limitations without changing its syntax or logic.

For each feature record:

```text
feature_id
claim_id
exact_claim_text
normalized_feature
object_or_component
property_or_state
relationship_or_location
action_or_function
parameter_or_range
dependency_context
source_locator
construction_issue
```

Use an object–property–link representation where helpful:

```text
Object | Property | Link/relationship | Claim language | Feature ID
```

Preserve conjunctions, alternatives, negative limitations, ordering, ranges, and antecedent basis.

### Step 3 — Identify implicit objects and missing context

Use the description and drawings to identify context needed to understand the claim.
Distinguish:

- expressly claimed features;
- description-supported implementation context;
- technically inferred prerequisites;
- product assumptions;
- absent or ambiguous objects.

Never promote an inferred prerequisite into a claim limitation.

Create an implicit-context register:

```text
context_id | related_feature | type | evidence | inference | confidence | legal_use_limit
```

### Step 4 — Build the ontology map

Map:

- system;
- subsystems;
- components;
- materials;
- data/signals;
- energy or material flows;
- external actors and supersystem objects;
- attributes and states;
- spatial, temporal, logical, and causal relationships.

Check that every claimed noun and relationship resolves to the map.
Keep claim language, engineering interpretation, and inferred context in separate columns.

### Step 5 — Define feature-level components and system boundary

Create the feature-level component list:

```text
object_id | name | boundary: system/supersystem/environment | claimed_feature_ids | resources | constraints
```

The model is feature-level, not merely a high-level parts list.
Do not merge two separately claimed elements only because one physical part might implement both.

### Step 6 — Build the interaction matrix

For every relevant object pair, record:

```text
source_object | action/function | target_object | interaction_type | claimed? | evidence | performance_state
```

Performance states:

- useful and adequate;
- useful but insufficient;
- useful but excessive;
- harmful;
- absent/required;
- uncertain.

Use the application-requirements card to justify performance states.

### Step 7 — Perform functional and flow analysis

Represent each function as:

```text
function_id | subject | verb | object | parameter | condition | feature_ids | requirement_ids | state
```

Analyze:

- primary useful function;
- supporting and auxiliary functions;
- control functions;
- measurement and feedback functions;
- harmful, insufficient, and excessive functions;
- energy, material, signal, and information flows;
- missing resources and bottlenecks;
- main flow and control flow.

Do not label a function excessive without a requirement target and comparable operating condition.

### Step 8 — Produce the reconstructed functional model

#### Step 8.1 — Feature-level SVG model

Create an accessible inline SVG with:

- stable object and function IDs;
- system/supersystem boundary;
- main and control flows;
- text-labelled useful, harmful, insufficient, and uncertain states;
- arrow legend;
- `<title>` and `<desc>`;
- adjacent tabular equivalent.

#### Step 8.2 — Claim text versus reconstruction table

```text
claim_feature_id
exact_claim_text
reconstructed_object/function
implicit_context
application_need
possible_trim_value
evidence_ids
uncertainty
```

#### Step 8.3 — Select 3–5 trimming directions

Rank directions using:

- feature importance to literal claim coverage;
- application necessity;
- harmful/excessive/insufficient-function evidence;
- functional redundancy;
- available system/supersystem resources;
- technical feasibility;
- change impact;
- potential equivalents risk;
- evidence quality.

Three to five is a planning target.
If fewer defensible directions exist, report the valid directions and the evidence gap.

Required handoffs from Stage I:

1. fine-grained feature table;
2. implicit-context register;
3. ontology map;
4. component and boundary table;
5. interaction matrix;
6. function-performance table;
7. main/control flow analysis;
8. feature-level SVG model;
9. claim-versus-reconstruction table;
10. ranked trimming directions.

## Stage II — TRIZ trimming (Step 9)

### Objective

Apply TRIZ trimming Rules A, B, and C to each selected direction,
then create a trimmed model and explicit engineering problems.

### Step 9.1 — Confirm trimming targets

Possible target evidence includes:

- harmful, insufficient, or excessive functions;
- flow defects;
- root-cause chain findings;
- low-value or high-cost components;
- application-nonessential features;
- claim-differentiation opportunities;
- complexity, reliability, or supply constraints.

Record why a target is selected and which claim features and requirements it affects.

### Step 9.2 — Apply trimming rules

#### Rule A — Remove the carrier and its receiving object

Use when the function object can legitimately be removed from the redesigned system.

- Most aggressive rule.
- Can remove two components.
- Usually unsuitable if the object is necessary to the primary application function.
- Problem form: “How can the need for object X be eliminated?”

#### Rule B — Self-service

Use when the function object can perform the useful function itself.

- Removes the original function carrier.
- Problem form: “How can object X perform function F itself?”

#### Rule C — Reassign to another carrier

Use when a system or supersystem resource can perform the same required useful function.

A candidate carrier should satisfy at least one condition:

1. it already performs the same or similar function on the receiving object;
2. it performs the same or similar function on another object;
3. it already interacts functionally with the receiving object;
4. it possesses the resources needed for the function.

Problem form: “How can carrier Z perform function F under the stated requirements?”

Evaluate A before B before C as an exploration heuristic,
not as a guarantee of higher inventiveness or lower legal risk.

### Step 9.3 — Generate the trimmed model

For each direction:

1. remove the selected node or relationship;
2. reassign useful functions for Rule B or C;
3. mark a removed requirement for Rule A;
4. update energy, material, signal, and control flows;
5. identify newly harmful or missing functions;
6. label unresolved functions with stable problem IDs;
7. map each change to claim features and application requirements;
8. create an accessible SVG plus an equivalent table.

### Step 9.4 — Create and screen trimming problems

Target three to five problems per direction and 9–25 overall.
Use fewer when the model does not support the target; never duplicate or fabricate problems.

Problem register:

```text
problem_id
direction_id
original_carrier
function
receiver
function_type
trimming_rule
new_carrier_or_removal
problem_statement
affected_feature_ids
requirement_ids
technical_risk
equivalents_risk_hypothesis
evidence_ids
priority
enter_FOS
```

Prioritize Rule A/B problems when their assumptions are credible,
but allow evidence and requirements to override the heuristic.

Stage II outputs:

- trimming-problem screening table;
- trimmed functional models;
- flow-change notes;
- risk and assumption register.

## Stage III — Function-Oriented Search (Step 10)

### Objective

Find and validate cross-domain solution principles for each selected trimming problem.
FOS is an evidence search, not free association.

### Step 10.1 — Understand the problem

- restate the required function and receiver;
- identify the application context;
- identify the contradiction or resource gap;
- map affected requirements and claim features;
- define what would count as a materially different implementation.

### Step 10.2 — Extract the explicit function

Use the form:

```text
[active verb] + [object] + [performance parameter] + [operating condition]
```

The function must be concrete and testable.

### Step 10.3 — Set parameter requirements

Use the Stage 0 card for:

- performance and accuracy;
- throughput, speed, and capacity;
- cost and maintenance;
- reliability, lifetime, and failure rate;
- size, mass, energy, and side effects;
- safety and human factors;
- temperature, pressure, humidity, media, contamination, and other environment;
- manufacturing and supply constraints;
- verification method.

### Step 10.4 — Generalize the function

Replace domain-specific terms with controlled generic concepts while preserving the core relationship.

Generalize along:

- object/material hierarchy;
- spatial and interface hierarchy;
- action hierarchy;
- energy or signal mechanism;
- scale and operating regime.

Create two or more query levels:

1. precise functional query;
2. generalized cross-domain query;
3. classification or mechanism expansion when useful.

Avoid abstraction so broad that search results cannot be evaluated.

### Step 10.5 — Identify candidate leading fields

Treat fields as search hypotheses, not defaults.
Potential fields may include:

- biological and natural mechanisms;
- medicine and medical devices;
- aerospace;
- industrial processing;
- energy systems;
- electronics and precision control;
- logistics, mining, textiles, printing, papermaking, or manufacturing;
- other fields discovered from classifications and evidence.

For each field, justify:

- why the function is central;
- maturity and operating envelope;
- diversity of known mechanisms;
- relevance to the application constraints.

Select three to five credible fields when evidence supports them.

### Step 10.6 — Search and select technologies

Use verified connectors and authoritative technical sources.
For each candidate technique capture:

```text
fos_id
problem_id
field
reference_technology
mechanism
source_locator
publication/date
operating_envelope
maturity
known_implementation
transferable_principle
application_mismatch
evidence_strength
```

Do not claim a reference technology exists without a source locator.
Do not use a patent abstract alone as proof of engineering feasibility.

### Step 10.7 — Solve secondary problems

Assess:

- energy or power source;
- scaling;
- special-resource dependence;
- material compatibility;
- environment;
- control and interfaces;
- manufacturing and tolerances;
- safety and regulatory impact;
- reliability and maintenance;
- new claim-risk interactions.

Prefer existing system resources where evidence supports them.
Record every unresolved secondary problem.

### Step 10.8 — Iterate multiple cross-domain concepts

Target at least five differentiated searched principles for each selected problem.
Use different fields or genuinely different mechanisms within a field.
If fewer than five credible principles are found, return the valid set and disclose search limits.

### Step 10.9 — Present FOS results

For each problem provide:

```text
problem statement
explicit function
generalized function
parameter requirements
search queries and dates
searched sources
candidate fields
evidence-backed principles
secondary problems
adaptation hypothesis
validation need
```

### Step 10.10 — Stage III to IV concept gate

Use the source default rubric unless the user approves different weights:

| Dimension | Weight | Meaning |
|---|---:|---|
| Preliminary claim differentiation | 50% | Degree of feature/mechanism difference under the stated claim interpretation; not a legal conclusion |
| Engineering feasibility | 35% | Ability to satisfy the application requirements with credible technology and validation |
| Technical originality | 15% | Degree of non-routine technical departure from the target implementation |

Score each dimension 1–10 with cited evidence and uncertainty.

```text
weighted_score = differentiation * 0.50 + feasibility * 0.35 + originality * 0.15
```

Do not convert missing evidence into a zero or neutral score.
Mark the score provisional or exclude the dimension and report the missing weight.

Select up to ten concepts and seek coverage across at least three trimming directions.
If fewer defensible concepts or directions exist, preserve the valid set and explain why.

Ranking table:

```text
rank | concept_candidate | trimming_problem | field | differentiation | feasibility | originality | weighted_score | missing_weight | evidence_ids
```

## Stage IV — Develop differentiated concepts (Step 11)

### Objective

Turn the shortlisted principles into implementable concepts and test whether their technical mechanism
is materially differentiated from the target claim implementation.

For each concept provide:

- concept ID and source FOS IDs;
- architecture and operating principle;
- key components, materials, steps, and interfaces;
- target requirements and expected performance range;
- manufacturing and integration assumptions;
- secondary problems and mitigations;
- test plan and acceptance criteria;
- affected target claim features;
- means/function/result comparison;
- literal and equivalents risk hypotheses;
- other-patent and new-patent search needs;
- evidence and uncertainty.

### Means/function/result comparison

Compare the target implementation and concept without treating this framework as a universal legal test.

```text
feature_id
target means/structure/step
concept means/structure/step
target function
concept function
target result
concept result
material difference
evidence
uncertainty
```

A parameter change alone is normally weak design-around differentiation.
A changed principle may still present equivalents or other-claim risk.

### Concept validation gate

Each concept must have:

- at least one clearly identified technical difference;
- an application-requirements mapping;
- a credible operating principle;
- a testable validation plan;
- a claim-feature mapping;
- evidence for borrowed mechanisms;
- explicit unresolved legal and engineering questions.

## Stage V — Jurisdiction-specific claim risk screening (Step 12)

### Objective

Screen each concept against the selected claim set under the stated jurisdiction and facts.
Do not issue a binary non-infringement conclusion.

### Step 12.1 — Literal coverage screen

For each asserted or relevant claim:

1. use the authoritative claim version;
2. identify dependencies and incorporated limitations;
3. state any claim-construction assumptions;
4. map each limitation to the proposed implementation;
5. classify each mapping as Present, Absent, Unclear, or Disputed;
6. cite product evidence and patent evidence;
7. identify divided/indirect performance facts where relevant;
8. calculate no automatic “safe” result from one absent limitation.

Claim chart:

```text
claim_id | limitation_id | construed requirement | concept evidence | state | source | uncertainty | counsel question
```

### Step 12.2 — Equivalents or analogous-doctrine screen

Verify the current jurisdiction-specific legal test from primary authority.
Where relevant, compare:

- way/means;
- function;
- result;
- interchangeability or foreseeability;
- insubstantial or material difference;
- element-by-element constraints;
- doctrine-specific exclusions and limiting principles.

Do not assume a US-style function-way-result test controls another jurisdiction.

### Step 12.3 — Prosecution and post-grant history

Review available:

- amendments;
- arguments;
- examiner communications;
- disclaimers;
- opposition, reexamination, invalidation, or post-grant records;
- court constructions and judgments;
- related-family statements where legally relevant.

Record the source and jurisdictional significance.
Do not assume every narrowing amendment creates the same estoppel effect.

### Step 12.4 — Adjacent-rights screen

Flag:

- dependent claims;
- continuation/divisional or family claims;
- method and system claims covering different actors;
- indirect or contributory theories where relevant;
- design, utility-model, copyright, trade-secret, standards, or regulatory issues;
- third-party patents revealed by FOS or implementation search.

### Step 12.5 — Risk classification

Use text states:

- `High`: credible literal or doctrine-based coverage concern;
- `Medium`: meaningful ambiguity or evidence gap;
- `Low`: material differences supported by current evidence, with residual uncertainty;
- `Unresolved`: claim, law, history, or product facts are insufficient.

Every state must include rationale, evidence, uncertainty, and counsel action.
Never label a concept “non-infringing.”

## Required deliverables

| No. | Stage | Deliverable |
|---:|---|---|
| 0 | 0 | Application requirements card |
| 1 | I | Fine-grained claim-feature table |
| 2 | I | Implicit-context and missing-object register |
| 3 | I | Ontology map |
| 4 | I | Feature-level component and system-boundary table |
| 5 | I | Interaction matrix |
| 6 | I | Function-performance table |
| 7 | I | Main and control flow analysis |
| 8 | I | Accessible feature-level SVG model and table |
| 9 | I | Claim text versus reconstruction table |
| 10 | I | Ranked 3–5 trimming directions or disclosed valid subset |
| 11 | II | Trimming-problem screening table |
| 12 | II | Accessible trimmed-model SVGs and tables |
| 13 | III | Evidence-backed FOS results |
| 14 | III | Up-to-ten concept ranking with 50/35/15 default scoring |
| 15 | IV | Detailed differentiated concepts and validation plans |
| 16 | V | Jurisdiction-specific claim risk screening report |
| 17 | Summary | Five-stage traceability table |

## Five-stage traceability table

This table is mandatory:

```text
concept_id
trimming_direction_id
trimming_problem_id
FOS_evidence_ids
score_and_components
requirement_ids
material_difference
literal_screen
equivalents_screen
history_screen
engineering_validation
overall_risk_state
next_action
```

Every final concept must trace backward to a trimming direction and source claim features,
and forward to evidence, tests, and counsel questions.

## Report outputs

Create both formats when the user requests files:

### Markdown

- Filename: `{patent-id}_design-around-assessment.md`
- Include Stages 0–V, Deliverables 0–17, source register, limitations, and traceability.
- Preserve stable IDs and accessible tables.
- Embed or link the two types of SVG model.

### Static HTML

- Filename: `{patent-id}_design-around-assessment.html`
- Build directly from the reviewed Markdown/data contract.
- Use one self-contained file with no remote dependency.
- Provide semantic section navigation.
- Include accessible SVG titles, descriptions, legends, and table equivalents.
- Use a light scientific/legal design with white paper, navy/slate text, and restrained teal accent.
- Use text labels for risk; do not rely on green/red, stars, checkmarks, or warning emoji.
- Provide responsive table overflow and print styles.
- Escape untrusted patent and user text.
- Include evidence locators and a counsel-review gate.

Do not claim another HTML-generation skill was invoked unless it is actually installed and used.

## Worked example — baggage-conveyor separation concept

This localized example preserves the source workflow logic but is illustrative only.
It is not current legal, technical, or patent evidence and must not be reused as a conclusion.

### Example application requirement

Separate baggage streams at a defined throughput while meeting size, damage, reliability,
maintenance, energy, and safety constraints.

### Example reconstructed feature groups

- segmented chute geometry;
- differentiated-friction surfaces;
- first and second speed sensing;
- powered guide or barrier;
- receiving and extraction sections;
- roller groups;
- baggage as the function receiver;
- implied controller and power resources.

### Example trimming directions

| Direction | Feature group | Hypothesis |
|---|---|---|
| DIR-001 | Powered guide and actuation | Replace active redirection with passive geometry or material flow |
| DIR-002 | Differentiated-friction surfaces | Replace fixed surface contrast with another resistance mechanism |
| DIR-003 | Guide, actuation, and control | Reassign function to gravity or existing flow resources |
| DIR-004 | Dual speed sensing | Remove the need for sensing through self-regulating separation |
| DIR-005 | Segmented chute | Replace staged geometry with a continuous mechanism |

### Example trimming problems

- How can the need for active lateral guidance be eliminated?
- How can baggage or the transport path self-select a route?
- How can an existing gravity field perform the redirection function?
- How can the need for fixed differential friction be eliminated?
- How can resistance adapt without the claimed surface arrangement?
- How can the need for speed sensing be eliminated?

### Example FOS hypotheses

Search—not assume—mechanisms such as:

- passive helical or curved flow paths;
- gravity classification and potential barriers;
- compliant brush or fin arrays;
- inertial or centrifugal response;
- self-adjusting rollers;
- fluid, granular, mining, packaging, or natural sorting analogies.

For each mechanism, require a source, operating envelope, transfer rationale, and secondary-problem analysis.

### Example concept differentiation

A passive helical channel may differ from an actively actuated guide in structure and operating principle,
but it still requires:

- a claim limitation map;
- equivalents analysis under the selected jurisdiction;
- family and dependent-claim review;
- engineering validation for throughput, baggage damage, jams, and safety;
- a third-party patent search.

The example does not establish Low risk or technical feasibility.

## Quality gates

### Patent and legal gate

- Authoritative claim text and version are recorded.
- Jurisdiction, relevant date, status, and family context are recorded.
- Claim construction assumptions are visible.
- Prosecution/post-grant sources are reviewed or marked unavailable.
- Current legal tests come from primary authority.

### Requirements gate

- Targets, tolerances, units, priorities, and verification methods are explicit.
- Assumptions and conflicts are identified.
- Every concept maps to relevant requirements.

### Reconstruction gate

- Every selected claim is decomposed into atomic feature IDs.
- Claim text, engineering interpretation, and inference are separated.
- The component, interaction, function, and flow models reconcile.
- SVGs have table equivalents.

### TRIZ gate

- Rules A, B, and C are applied correctly.
- Each problem traces to a direction, feature, function, and requirement.
- Quantitative targets are not padded with duplicate problems.

### FOS gate

- Search queries, connectors/sources, dates, and evidence locators are recorded.
- Candidate technologies are real and source-backed.
- Operating envelopes, maturity, mismatches, and secondary problems are disclosed.
- Fewer-than-target results are reported honestly.

### Concept gate

- Scores include evidence, uncertainty, and missing weight.
- The default 50/35/15 rubric is labelled as a screening rubric.
- Shortlisted concepts cover multiple directions where evidence permits.
- Every concept has architecture, claim mapping, requirements mapping, and validation plan.

### Risk gate

- Each claim limitation is Present, Absent, Unclear, or Disputed.
- Equivalents analysis is jurisdiction-specific and element-focused.
- Prosecution history and adjacent rights are addressed.
- Results use High, Medium, Low, or Unresolved—not “non-infringing.”
- Counsel questions and next actions are explicit.

### Report gate

- Deliverables 0–17 are present or have a documented unavailable reason.
- The five-stage traceability table reconciles every ID.
- Markdown and HTML agree.
- HTML is static, offline, accessible, responsive, print-ready, and safely escaped.
- No source, evidence, or uncertainty is hidden by visual styling.

## Failure handling

If the target claim is unavailable, do not perform a legal-risk screen from title or abstract.
If the claim version is uncertain, separate scenarios by version.
If the target jurisdiction is missing, complete technical ideation only and mark legal screening blocked.
If application requirements are incomplete, use an assumption register and do not finalize feasibility ranking.
If prosecution history is unavailable, classify history-dependent analysis Unresolved.
If FOS evidence is weak, reduce the concept set and report the search limitation.
If engineering evidence is absent, label performance as a hypothesis and specify tests.
If another patent may block a concept, flag the need for a broader FTO search.
If confidential data cannot be sent to a connector, work locally from authorized materials.

## Final response

Summarize:

- patent, claims, jurisdiction, version, and cutoff;
- application-requirements baseline;
- strongest trimming directions;
- number of evidence-backed FOS principles and developed concepts;
- concept ranking and missing evidence;
- claim-risk states and highest-risk uncertainty;
- engineering tests and legal review still required;
- Markdown and HTML output locations, when created.

Do not state that any concept is non-infringing or filing/launch ready.
