---
copyright: "Copyright © Patsnap. All rights reserved."
name: find-cross-industry-functional-solutions-rd
description: Find transferable technical solutions from other industries by reframing a concrete R&D problem as functions, effects, constraints, and contradictions. Use when an engineering or research team needs a cross-industry solution search, functional patent search strategy, solution shortlist, transferability assessment, or experiment plan.
---

# Find Cross-Industry Functional Solutions

## Purpose

Convert a domain-specific technical problem into domain-neutral functions and constraints, search patents and technical evidence across industries, screen candidate mechanisms, and recommend testable transfer paths. Deliver a traceable Markdown report or self-contained HTML report when requested.

This workflow generates technical analogies and hypotheses. It does not prove feasibility, patentability, freedom to operate, or commercial readiness.

## Use this skill when

- a team has a concrete technical problem but does not know which outside fields may contain solutions;
- the user asks for function-oriented, effect-oriented, or TRIZ-inspired search;
- a search must move beyond product names and the current industry's vocabulary;
- patents/technical solutions need to be grouped by principle and assessed for transfer;
- the user wants queries, entity/family consolidation rules, a result list, and validation actions.

Do not invoke it for a routine keyword search, a formal FTO opinion, or an invention-claim draft without a cross-industry transfer objective.

## Input gate

Collect or infer cautiously:

- current system/product/process;
- undesired effect or limiting performance;
- required function and target metric;
- object acted on and operating environment;
- inputs/outputs and boundary conditions;
- constraints: size, mass, energy, temperature, pressure, materials, safety, contamination, cost, cycle time, regulation, manufacturability;
- harmful functions and trade-offs;
- prohibited/undesired solution classes;
- current attempts and why they failed;
- target readiness level, test resources, timeline, and jurisdictions;
- confidential information and approved external services.

For “improve phone heat dissipation,” ask for heat load, device volume, allowable surface/junction temperature, orientation, ambient conditions, power/noise/weight limits, materials, sealing, reliability and manufacturing constraints before ranking solutions.

## Evidence and MCP routing

Use user-supplied evidence first. For global Patsnap patent discovery, verified `advanced_patent_search` supports nested/fielded, semantic, patent-number, applicant, count and keyword-assist routes:

https://open.patsnap.com/marketplace/mcp-servers/patent-search

Use `patent_briefing` for shortlisted patents' bibliography, family, claims, description, drawings, status and translations:

https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

The global marketplace catalog advertises an `R&D Solution Search Beta` capability using TRIZ tag matching, but do not name or require an MCP connector until its stable detail page, connection key, callable tools and actual availability are verified. If available at execution time, use it as an additional candidate-generation route, not as the only evidence source.

No MCP is required when supplied patent/technical records are sufficient.

## Workflow

### 1. Problem normalization

Write a factual problem statement:

```text
In <system/context>, <undesired effect or insufficient function> occurs under
<conditions>, causing <measurable impact>. Improve <metric from baseline to
target> while preserving <constraints> and avoiding <harmful effects>.
```

Separate observed facts, assumptions, causes not yet verified, and stakeholder preferences.

### 2. Functional model

Represent:

- subject/tool;
- action/function verb;
- object;
- target parameter;
- environment;
- useful effect;
- harmful effect;
- resource/field/energy flow;
- measurement method.

Use a verb–object expression, for example:

- transfer heat;
- spread heat flux;
- reduce thermal contact resistance;
- increase effective surface area;
- transport vapor/working fluid;
- modulate phase transition;
- isolate heat-sensitive components.

Do not include the current product name in every generalized query.

### 3. Generalization ladder

Create at least three levels:

1. **Implementation level** — current materials/components/geometry;
2. **Function/effect level** — physical/chemical/biological action;
3. **Abstract transformation level** — change field, phase, interface, flow, distribution, timing or control.

Move both upward and downward. Over-generalization creates irrelevant results; implementation-only language prevents cross-industry discovery.

### 4. Contradictions and constraints

State:

- improving parameter;
- worsening parameter;
- physical contradiction if the same feature must be high/low or present/absent;
- hard versus soft constraints;
- separations by space, time, condition or scale;
- available resources in/around the system.

TRIZ concepts may help generate search terms, but do not force a contradiction matrix when the problem is adequately represented by function and constraints.

### 5. Scientific effect and mechanism map

List candidate mechanisms by causal principle, for example:

- conduction/spreading;
- convection/forced flow;
- phase change/latent heat;
- radiation/emissivity;
- capillary/heat-pipe transport;
- electrohydrodynamic or thermoelectric effects;
- geometry/topology/surface-area control;
- interface/contact/material anisotropy;
- sensing/feedback/duty-cycle control.

For each, record governing variables, expected benefit, constraints, failure modes and industries likely to use it.

### 6. Search architecture

Build multiple query families:

#### Functional

```text
(<function synonyms>) AND (<object/property synonyms>) AND (<constraint/effect>)
```

#### Mechanism/effect

```text
(<scientific effect or mechanism>) AND (<performance objective>)
```

#### Contradiction/resource

```text
(<improve parameter>) AND (<avoid worsening parameter>) AND (<available resource>)
```

#### Cross-industry seed

Search industries where the same function/constraint is extreme: aerospace, power electronics, batteries, data centers, medical devices, food processing, textiles, buildings, automotive, semiconductor manufacturing, chemical processing or relevant alternatives.

#### Classification/citation/inventor

Use CPC/IPC, citations, families, applicants/inventors and similar-patent routes after high-quality seeds emerge. Record current classification definitions and search date.

Run exact/nested/fielded, semantic and keyword-assist routes separately. Preserve complete query history, filters, dates, databases, counts and exports.

### 7. Screen and consolidate

First remove:

- false function matches;
- background-only mentions;
- solutions violating hard constraints;
- duplicate exact publications;
- records with insufficient technical disclosure.

Then group by:

- mechanism/principle;
- required function;
- transfer interface;
- source industry;
- implementation architecture;
- patent family under stated definition.

Do not merge different technical principles merely because titles are similar. Preserve member/claim/status differences where IP implications are discussed.

### 8. Transferability assessment

For each candidate solution, assess:

| Dimension | Questions |
|---|---|
| Functional equivalence | Does it perform the same function on a comparable object? |
| Governing physics | Are scale, fields and transport regimes comparable? |
| Boundary conditions | Temperature, pressure, flow, duty cycle, environment? |
| Interface | How is it integrated with the target system? |
| Performance | Source metric and comparable target metric? |
| Materials/process | Compatible, manufacturable and supply-available? |
| Safety/regulatory | New hazards or compliance burden? |
| Reliability | Lifetime, contamination, degradation and maintenance? |
| Economics | BOM, energy, installation, service and scale? |
| IP | Relevant claims/families/jurisdictions and open questions? |
| Evidence | Prototype, test, simulation, patent assertion or analogy only? |

Use ratings with rationale and confidence, not an opaque score.

### 9. Adaptation paths

For priority solutions specify:

- source principle and evidence;
- target function/constraint;
- what transfers unchanged;
- what must be redesigned;
- scaling/model assumptions;
- potential failure modes;
- required prototype/simulation/experiment;
- success/failure criteria;
- patentability/FTO search question;
- owner and timing.

Do not recommend direct copying of a patented implementation. A transferable principle may require a distinct architecture and counsel review.

### 10. Validate and iterate

- test false positives and false negatives;
- search alternative mechanisms and industries;
- inspect claims/description/drawings of key patents;
- compare against non-patent literature/standards where available;
- involve domain experts;
- update problem/constraints after experiments;
- preserve decision history.

## Prioritization

Use a decision table:

| Criterion | Evidence |
|---|---|
| Functional fit | Direct versus partial |
| Constraint fit | Hard constraints passed/unknown/failed |
| Mechanistic plausibility | Governing model and scale |
| Evidence maturity | Deployed/tested/prototype/simulation/assertion |
| Integration effort | Architecture/material/process changes |
| Performance potential | Comparable measured evidence |
| Reliability/safety | Known failure modes and controls |
| Cost/time | Test and scale pathway |
| IP uncertainty | Claims/status/jurisdiction review needed |
| Strategic differentiation | Distinct value and defensibility |

Show sensitivity to uncertain assumptions. A high-potential solution with weak evidence may rank as a high-priority experiment, not a recommendation to deploy.

## Report structure

1. executive summary and decision;
2. source problem and measurable constraints;
3. functional/generalization/contradiction model;
4. mechanism/effect map;
5. reproducible search strategy and coverage;
6. result funnel and consolidation rules;
7. cross-industry solution matrix;
8. top transfer paths with evidence and confidence;
9. prototype/experiment plan;
10. IP questions and legal boundary;
11. sources, exclusions, blind spots and next iteration.

For HTML, use a self-contained responsive scientific/editorial design: light neutral background, high-contrast text, muted blue/teal accent, semantic headings/tables, source links, accessible status labels and print CSS. Avoid gradients, dark sci-fi styling, particles, decorative animation, external dependencies and product-interface imitation.

## Failure paths

- **Problem lacks metrics/constraints:** produce a structured intake and preliminary function model only.
- **Search returns excessive noise:** adjust abstraction level, co-occurrence, fields, classifications, constraints and negative concepts; preserve broad-query counts.
- **No cross-industry results:** test adjacent mechanisms, scientific effects, resources and non-patent technical sources.
- **Evidence is patent assertion only:** label unvalidated and propose experiment.
- **Scale/boundary mismatch:** retain as low-transferability context or reject with reason.
- **MCP unavailable:** provide reproducible queries and required export fields; do not invent results.
- **Potential blocking claim:** identify the record/question and refer to jurisdiction-specific IP review.

## Quality gates

- [ ] Problem statement includes baseline, target, conditions and constraints.
- [ ] Facts, assumed causes and preferences are separate.
- [ ] Function, object, effect and measurement are explicit.
- [ ] Multiple abstraction levels and mechanism families were searched.
- [ ] Queries/filters/database/date/counts are reproducible.
- [ ] Exact publications and patent families are consolidated under stated rules.
- [ ] Every recommended solution has source, mechanism, transfer logic, constraints and confidence.
- [ ] Opportunity/transfer hypothesis is not presented as a patent fact.
- [ ] Prototype plan has measurable success/failure criteria.
- [ ] Patent claims/status and legal conclusions are appropriately bounded.
- [ ] No patent, technology evidence, MCP, source or performance value is fabricated.

## Boundary

Validate recommendations through engineering analysis and experiment. Obtain qualified patent counsel for material patentability, FTO, infringement, validity or licensing decisions.
