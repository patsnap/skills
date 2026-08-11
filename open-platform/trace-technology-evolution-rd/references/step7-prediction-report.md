# Stage 7: Horizon Scenarios and Decision Report

## Position in the workflow

- Input: reviewed evolution forest, evidence register, search logs, branch/analogy/evidence-gap candidates, maturity evidence, and limitations.
- Output: horizon scenarios, pathway and disruption monitoring registers, concept alternatives, consistency results, and final scientific/editorial report.
- Audience: R&D, product, engineering, strategy, innovation, and IP teams.
- Boundary: scenario analysis, not a deterministic forecast, legal opinion, investment recommendation, safety approval, or regulatory conclusion.

## Decision questions

Stage 7 answers:

1. Which technical states are directly observed at the evidence cutoff?
2. Which adjacent states are plausible under declared dependencies?
3. Which cross-domain mechanisms may transfer, and what blocks transfer?
4. Which high-probability pathways need roadmap monitoring?
5. Which low-probability, high-impact conditions need trigger-based contingency planning?
6. Which product concepts remain internally compatible across components?
7. What evidence would invalidate or materially change the assessment?

## Required project frame

Record:

- report date;
- evidence cutoff;
- forecast baseline date;
- decision context;
- product/system scope;
- geography and language scope;
- forecast horizons as calendar ranges;
- taxonomy IDs and crosswalk version;
- maturity method;
- patent count unit;
- scenario owner and reviewers;
- monitoring owner and cadence;
- confidentiality and licensing constraints.

Do not use “3 years,” “5 years,” or “10 years” without translating them into calendar ranges from a stated baseline. Horizons may differ by domain and decision.

## Forecasting principles

### 1. Route position is not time

A route/node describes an analytical state under a declared taxonomy. It does not determine:

- time to prototype;
- manufacturing readiness;
- qualification or certification;
- cost competitiveness;
- supply-chain readiness;
- customer adoption;
- legal availability;
- safety or regulatory acceptance.

### 2. Maturity evidence is distinct

Use TRL or another maturity scale only when:

- the scale is appropriate to the domain;
- definitions and evidence anchors are explicit;
- assessors apply it consistently;
- uncertainty is recorded;
- maturity is not inferred from document type alone.

A paper is not automatically TRL 1–3. A patent is not automatically later. A product announcement is not automatically a verified commercial deployment.

### 3. Scenarios are conditional

Every scenario states:

- current observed state;
- candidate state;
- mechanism;
- dependencies;
- supporting evidence;
- contradicting evidence;
- maturity and transfer conditions;
- barriers;
- confidence;
- trigger;
- invalidation condition;
- next review date.

### 4. Route direction is route-specific

Later declared nodes do not always mean greater complexity:

- Route 1 can move through multiplication toward consolidation.
- Route 2 can move toward trimming or self-service.
- Other routes may increase control, structural freedom, scale resolution, or adaptivity.

Concept synthesis must not add modules to a route whose declared transition is simplification or integration.

### 5. Several architectures may coexist

Do not assume one global current node or one inevitable successor. Segment by architecture, application, geography, cost tier, operating environment, or value proposition when necessary.

## Evidence classes for scenarios

Use separate evidence roles:

- **direct technical evidence**: claims, methods, results, standards clauses, verified engineering records;
- **maturity evidence**: prototype, pilot, qualification, manufacturing, certification, deployment;
- **adoption evidence**: products, procurement, installed base, standards use, ecosystem support;
- **economic evidence**: cost, yield, investment, supply chain, pricing under defined scope;
- **constraint evidence**: safety, reliability, regulation, environment, interfaces, intellectual property;
- **contradicting evidence**: failed results, limitations, withdrawals, negative tests, incompatible conditions.

Do not count several reports repeating one announcement as independent corroboration.

## Scenario record

```json
{
  "scenario_id": "H1",
  "unit_id": "P4.2",
  "baseline_date": "2026-07-31",
  "horizon": {"from": "2028-01-01", "to": "2030-12-31"},
  "current_states": [
    {
      "route": 11,
      "node": "planar array",
      "evidence_ids": ["E17", "E22"]
    }
  ],
  "candidate_state": {
    "route": 11,
    "node": "spherical or conformal array",
    "status": "conditional scenario"
  },
  "mechanism": "Reviewed mechanism statement",
  "supporting_evidence_ids": ["E31"],
  "contradicting_evidence_ids": ["E45"],
  "dependencies": [],
  "barriers": [],
  "maturity": {},
  "confidence": "medium",
  "trigger_conditions": [],
  "invalidation_conditions": [],
  "review_by": "2027-01-31"
}
```

## Horizon construction

### Nearer horizon

Candidate characteristics may include:

- direct target-domain prototype or product evidence;
- defined manufacturing and integration path;
- applicable standards or qualification work;
- multiple independent organizations;
- limited unresolved barriers;
- monitorable implementation milestones.

Do not label “high confidence” merely because a large applicant filed a patent.

### Middle horizon

Candidate characteristics may include:

- cross-domain prototype or target-domain early demonstration;
- plausible transfer path;
- material but identifiable manufacturing, cost, reliability, or ecosystem barriers;
- several independent technical signals;
- a defined experiment or milestone sequence.

### Longer horizon

Candidate characteristics may include:

- early mechanism evidence;
- substantial scale, manufacturing, safety, regulatory, cost, or ecosystem barriers;
- uncertain architecture;
- dependence on several unresolved enabling technologies;
- broad timing range and explicit invalidation conditions.

Do not call all longer-horizon candidates “blue sky.” Preserve evidence and causal mechanism.

## Timing method

For every scenario evaluate:

1. demonstrated technical state;
2. manufacturing readiness;
3. reliability and lifetime evidence;
4. safety and regulatory path;
5. standards and interoperability;
6. cost and yield trajectory;
7. supply-chain capacity;
8. integration dependencies;
9. customer/user adoption;
10. intellectual-property and licensing constraints;
11. organization capability;
12. external event dependencies.

Convert this evidence to a range only with a declared method. When timing evidence is inadequate, provide milestone dependencies and monitoring triggers instead of a date.

The source contains typical cycles for selected route families. Treat those as source hypotheses, not defaults. Calibrate with historical transitions from the actual domain.

## High-probability pathways and low-probability disruptions

The source uses “gray rhino” and “black swan.” Retain the familiar labels only with precise operational definitions.

### High-probability pathway

A pathway has:

- accumulating independent evidence;
- a plausible and relatively clear implementation path;
- observable milestones;
- material decision impact;
- a need for roadmap or resource action.

Management behavior:

- incorporate into the roadmap;
- monitor path milestones;
- update timing when milestones move;
- define option or commitment points.

### Low-probability disruption

A disruption candidate has:

- uncertain event timing or threshold;
- a plausible causal mechanism;
- material impact if triggered;
- explicit observable triggers;
- a contingency action that can be prepared proportionately.

Management behavior:

- monitor triggers;
- preserve options;
- define escalation conditions;
- avoid treating speculation as a baseline forecast.

### Dual classification

One topic may have:

- an orderly baseline pathway; and
- a separate event-driven acceleration or disruption condition.

Create linked records without conflating probabilities.

## Pathway record

```json
{
  "id": "PTH-01",
  "name": "Pathway name",
  "classification": "high-probability pathway",
  "baseline_date": "2026-07-31",
  "window": {"from": "2028-01-01", "to": "2031-12-31"},
  "supporting_evidence_ids": [],
  "contradicting_evidence_ids": [],
  "milestones": [],
  "monitor_frequency": "semiannual",
  "decision_points": [],
  "strategic_actions": [],
  "confidence": "medium",
  "linked_disruption_id": null,
  "owner": "",
  "review_by": ""
}
```

## Disruption record

```json
{
  "id": "DSP-01",
  "name": "Disruption condition",
  "classification": "low-probability disruption",
  "mechanism": "Why the event could change the system",
  "probability_statement": "Qualitative or calibrated estimate with method",
  "impact_statement": "Scope and severity with evidence",
  "supporting_evidence_ids": [],
  "contradicting_evidence_ids": [],
  "trigger_signals": [],
  "trigger_threshold": "Observable escalation condition",
  "contingency_action": "Proportionate prepared response",
  "monitor_frequency": "quarterly or event-driven",
  "linked_pathway_id": null,
  "owner": "",
  "review_by": ""
}
```

## BSS and TDI rubrics

The source introduces:

- BSS, a ten-point signal-strength rubric; and
- TDI, a hundred-point disruption-impact/urgency rubric.

They may be useful project rubrics, but the source thresholds are unvalidated initial suggestions. Do not use BSS ≥ 6 or TDI ≥ 51 as universal rules.

### Rubric requirements

For each score define:

- decision purpose;
- dimensions;
- anchors;
- weights;
- evidence source for every dimension;
- missing-data treatment;
- double-counting controls;
- calibration examples;
- sensitivity analysis;
- reviewer agreement;
- version and review date.

### Candidate BSS dimensions

- patent activity acceleration under a declared family/query method;
- cross-domain migration;
- funding or capital evidence;
- research-front activity;
- standards or regulatory movement;
- cost or performance threshold evidence.

Each can be zero, low, medium, or high under explicit anchors. A funding headline without technical linkage does not score highly.

### Candidate TDI dimensions

- substitution potential;
- market/system impact;
- time-to-impact under stated conditions;
- ecosystem readiness;
- reversibility and switching cost;
- safety/regulatory consequence where relevant.

Do not display a 0–100 score to two decimal places when anchors are qualitative.

### Calibration

Use a historical case set:

1. choose transitions known before and after a cutoff;
2. reconstruct only information available at the historical cutoff;
3. score independently;
4. compare predicted class with observed outcome;
5. examine false positives and false negatives;
6. adjust dimensions/thresholds;
7. retain the audit trail.

## Monitoring register

For every pathway or disruption define:

- monitoring question;
- source or connector;
- exact query or watch condition;
- cadence;
- owner;
- evidence cutoff/update date;
- trigger threshold;
- response;
- last reviewed status;
- data-access failure behavior.

Monitoring may require separate authorization and tooling. Do not claim a recurring monitor has been created unless it actually has.

## Concept synthesis

### Purpose

Translate component scenarios into coherent product/system concepts while exposing incompatibilities.

### Required checks

- system architecture compatibility;
- interface compatibility;
- power, compute, data, thermal, volume, mass, and latency budgets;
- manufacturing and supply chain;
- safety and regulation;
- reliability and maintainability;
- cost and target segment;
- intellectual-property/licensing questions;
- user value and adoption;
- component timing alignment;
- contradiction among route directions.

### Three branches

Produce at least:

1. **Conservative** — relies on nearer-horizon evidence and existing integration paths.
2. **Accelerated** — assumes defined enabling milestones occur earlier.
3. **Disruption-conditioned** — includes one or more explicit triggers and contingency assumptions.

More branches may be needed for different architectures or market segments. Do not force exactly three when the decision requires another structure.

### Concept record

```json
{
  "concept_id": "CPT-01",
  "name": "Concept name",
  "branch": "conservative",
  "value_proposition": "Decision-relevant outcome",
  "component_states": [],
  "supporting_scenario_ids": [],
  "system_budgets": {},
  "dependencies": [],
  "conflicts": [],
  "required_experiments": [],
  "evidence_ids": [],
  "confidence": "medium",
  "limitations": []
}
```

## Report structure

The localized report preserves the source's fourteen-part skeleton:

0. table of contents;
1. executive summary;
2. methodology;
3. evidence funnel;
4. system decomposition;
5. route distribution;
6. forest findings;
7. route-defining evidence;
8. evidence-gap and analogy candidates;
9. horizon scenarios;
10. high-probability pathways and low-probability disruptions;
11. concept specification;
12. alternative branches;
13. methods, evidence, consistency checks, and limitations.

Add a complete source register and search-method disclosure when not already visible in section 13.

## Scientific/editorial visual system

Use `assets/report/report_skeleton_mckinsey.html` as the exact source-topology report asset. The filename is retained for topology only. The localized file:

- does not claim McKinsey affiliation;
- uses restrained navy/blue/neutral colors;
- has no gradients, neon theme, decorative emoji, or external runtime;
- uses semantic HTML and accessible tables;
- supports responsive screens and print;
- distinguishes evidence, hypothesis, limitation, and decision;
- uses tabular numerals for quantitative data;
- shows sources and cutoff prominently;
- contains explicit empty states;
- requires safe escaping by any population process.

Do not offer a “technology dark/neon” style merely for presentation. Style must not change wording, evidence, totals, or confidence.

## Consistency checks

The source defines LR-01 through LR-08. Localize and strengthen them:

### LR-01 — Evidence resolution

Every factual finding and route-defining observation resolves to accepted evidence and a stable identifier/link.

Failure: block release.

### LR-02 — Evidence-gap language

Every gap says “not observed in the reviewed dataset,” includes gap-search IDs, and avoids novelty/FTO/global-white-space claims.

Failure: block release.

### LR-03 — Analogy transfer

Every analogy includes mechanism, matching/different conditions, barriers, and required validation. Do not use node distance alone.

Failure: block release for decision use; otherwise quarantine.

### LR-04 — Scenario traceability

Every scenario has supporting and contradicting evidence, dependencies, baseline, calendar range, confidence, triggers, and invalidation conditions.

Failure: block release.

### LR-05 — Coverage balance

Report domain/cross-domain composition by evidence type and explain imbalance. The source's 70% maximum is not universal.

Failure: warn or block when bias invalidates the decision.

### LR-06 — Search coverage

Every track has a reproducible log or explicit omission/failure. Recall estimates state method and uncertainty.

Failure: block strong absence claims.

### LR-07 — Scenario coherence

Later-horizon states do not contradict nearer-horizon dependencies without explanation. Ordinal route position alone does not define chronology.

Failure: block release.

### LR-08 — Monitoring actionability

Every disruption has observable triggers, threshold, owner, cadence, and contingency action.

Failure: quarantine as speculative issue.

### LR-09 — Count reconciliation

All totals derive from the accepted evidence register and identify publication/family/paper/source units.

Failure: block release.

### LR-10 — Taxonomy integrity

All labels use declared taxonomy IDs; analytical/display crosswalks are versioned and reviewed.

Failure: block release.

### LR-11 — Security and portability

HTML is escaped, self-contained, accessible, responsive, printable, and free of secrets, local paths, external runtime, or unsafe DOM behavior.

Failure: block release.

### LR-12 — Specialist boundaries

Material patent, safety, regulatory, clinical, financial, or other specialist conclusions are reviewed or explicitly withheld.

Failure: block release of the affected conclusion.

## Consistency result

```json
{
  "check_id": "LR-04",
  "status": "pass | warn | fail | not_applicable",
  "scope": "H1",
  "evidence": "Machine- or reviewer-verifiable basis",
  "issues": [],
  "reviewer": "",
  "reviewed_on": "2026-08-08"
}
```

## Failure behavior

- Sparse evidence: retain a sparse state and broaden only within authorized scope.
- No maturity evidence: provide milestones, not timing.
- Conflicting evidence: show both and lower confidence.
- Taxonomy disagreement: retain alternatives and do not force a forest frontier.
- No trigger: quarantine the disruption candidate.
- Concept incompatibility: split concepts or reject the combination.
- Failed consistency gate: produce a review queue instead of a polished unsupported report.
- Missing external access: provide query and monitoring plans only.

## Required deliverables

- horizon-scenario register;
- high-probability pathway register;
- low-probability disruption register;
- linked dual-classification relationships;
- BSS/TDI configuration and calibration only if used;
- monitoring register;
- conservative, accelerated, and disruption-conditioned concepts;
- compatibility/conflict review;
- consistency-check results;
- final self-contained report;
- complete evidence/source register;
- search log and limitations;
- specialist-review queue.

## Stage gate

Do not deliver until:

- all horizons use calendar ranges and baseline dates;
- route position and maturity are separate;
- scenarios have supporting and contradicting evidence;
- dependencies, barriers, triggers, and invalidation conditions are explicit;
- timing method is disclosed;
- high-probability pathways and disruptions have different management actions;
- BSS/TDI rubrics are calibrated or clearly exploratory;
- concept branches pass compatibility review;
- all LR checks have results;
- report totals reconcile;
- report HTML passes security and accessibility review;
- all limitations and specialist boundaries are visible.

## Limitations

1. Scenario ranges remain uncertain and domain-dependent.
2. Publication, indexing, and legal-status lag affect the baseline.
3. Route taxonomies simplify real technical change.
4. Maturity assessments depend on evidence quality and scale definitions.
5. Funding, announcements, and standards activity may not result in adoption.
6. Cost, yield, supply chain, regulation, and user behavior may dominate technical feasibility.
7. Cross-domain analogies may fail under target conditions.
8. Low-probability disruptions are especially prone to narrative bias.
9. Rubric scores can create false precision without calibration.
10. Static reports age; every conclusion needs an update date and owner.
