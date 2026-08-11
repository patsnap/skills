# Stage 4: Evidence Screening and Multi-Dimensional Assessment

## Position in the workflow

- Input: Stage 3 evidence and search registers.
- Output: accepted evidence with transparent assessment fields and review priority.
- Downstream: Stage 5 route labeling.
- Purpose: allocate review effort and compare records under declared assumptions.
- Not purpose: produce an objective patent value, legal strength, market value, or scientific truth score.

## Core design

Use two distinct stages:

```text
Stage A — eligibility and evidence-quality gates
    relevance, scope, reviewable text, identity, cutoff, conditions
    ↓
Stage B — decision-specific assessment
    transparent dimensions, anchors, missing-data rule, sensitivity
    ↓
review priority and accepted evidence register
```

Never use a ranking score to rescue an ineligible record. Never use eligibility as proof that a record is important.

## Required configuration

Record:

- decision context;
- evidence cutoff;
- evidence types assessed;
- patent count unit;
- unit or search track;
- assessment dimensions;
- dimension definitions;
- anchors and units;
- weights and rationale;
- missing-data rule;
- normalization method;
- time/field adjustment;
- threshold or tier purpose;
- sensitivity scenarios;
- analyst and independent reviewer;
- configuration version.

## Stage A — eligibility gates

### A1. Identity

The record has:

- a stable evidence ID;
- a publication, DOI, standard, project, or official source identifier where available;
- a stable source link;
- a document or event date;
- source type;
- organization or author metadata appropriate to the type.

### A2. Scope

The record is:

- inside the product/domain scope; or
- explicitly accepted as a cross-domain analogy; and
- linked to at least one approved functional unit.

### A3. Reviewable evidence

The available text supports the intended use:

- patent claims or relevant description for claim/implementation analysis;
- abstract plus sufficient methods/results for a paper finding;
- exact clause or status for a standard;
- primary product, engineering, regulatory, funding, or company evidence for current events.

Title-only evidence may support discovery, not detailed node assignment or forecasting.

### A4. Date and cutoff

- publication/event date is valid;
- access date is recorded;
- record does not exceed the evidence cutoff;
- legal status, standard status, product status, or funding status includes an “as of” date when used.

### A5. Conditions and comparability

Record relevant:

- units;
- operating conditions;
- sample or system scale;
- test method;
- baseline;
- uncertainty;
- observed versus expected result;
- transfer limitations.

### A6. Duplication

Apply the declared normalization:

- patent publications may remain separate for claim review;
- simple families may be used for portfolio/trend counts;
- continuations, divisionals, grants, applications, and national phases require explicit treatment;
- papers use DOI, repository ID, normalized title, and version relationships;
- secondary reports do not become independent corroboration of one primary source.

## Stage A result

Use:

- `accepted`;
- `rejected`;
- `quarantined` pending text or specialist review.

Every rejected or quarantined record retains a reason.

## Stage B — assessment principles

### B1. Separate evidence types

Patents, papers, standards, engineering cases, products, company announcements, funding events, regulatory documents, and general web sources have different fields and incentives. Do not force them into one universal score.

### B2. Use decision-specific dimensions

A technical-evolution decision may emphasize:

- mechanism relevance;
- directness of evidence;
- technical performance;
- maturity and reproducibility;
- transferability;
- actor capability;
- patent family strategy;
- claim relevance;
- citation context;
- legal-event context;
- standards or adoption evidence;
- recency;
- contradiction and uncertainty.

Choose only dimensions that affect the named decision.

### B3. Avoid double counting

Common overlaps:

- proprietary patent value may already include family, citation, remaining life, and geography;
- institution reputation may correlate with citation and venue;
- commercial product evidence may correlate with company capability;
- legal events may correlate with age and portfolio size;
- citation and family breadth may both correlate with applicant resources.

Map dependencies before assigning weights.

### B4. Missing data is not zero performance

Declare one of:

- no score until the field is reviewed;
- redistribute weight only among dimensions declared eligible for redistribution;
- retain an uncertainty penalty;
- compare only records with a common field set;
- show a score range under plausible missing values.

Never silently drop a missing dimension from the denominator.

## Patent assessment dimensions

### P1. Technical and functional relevance

Review:

- claim or disclosure link to the SVOP function;
- mechanism correspondence;
- parameter and condition correspondence;
- target-domain versus cross-domain context;
- implementation specificity;
- evidence contradictions.

Suggested anchors:

| Level | Meaning |
|---|---|
| 0 | no usable technical correspondence |
| 1 | broad conceptual overlap only |
| 2 | partial functional match with major condition gaps |
| 3 | material mechanism match with stated transfer limits |
| 4 | direct, well-supported match under comparable conditions |

### P2. Family and filing context

Consider:

- earliest priority date;
- simple and extended family definitions;
- jurisdictions and national phases;
- continuation/divisional relationships;
- claim differences across members;
- pending, granted, expired, abandoned, or other status as of a date.

Broad family coverage may indicate filing strategy and expenditure. It does not prove technical merit, commercial adoption, validity, or freedom to operate.

### P3. Citation context

Review:

- forward and backward citations;
- examiner versus applicant citations where available;
- self-citation and related entities;
- document age;
- field/classification citation baseline;
- who cites and why;
- whether the cited feature is the relevant one.

Use age- and field-normalized context when possible. A raw citation cutoff is not portable.

### P4. Applicant and assignee context

Assess evidence of capability relevant to this mechanism:

- repeated technical output;
- manufacturing or research capability;
- standards participation;
- product or engineering evidence;
- partnerships or acquisitions;
- current entity and ownership status.

Do not rely on a static “top company” or university ranking whitelist. New entrants and small specialist teams may be strategically important.

### P5. Claim and disclosure quality

When the decision requires it, record:

- independent claims reviewed;
- relevant claim elements;
- specification support;
- examples and measured results;
- claim breadth only as a specialist-reviewed interpretation;
- unresolved claim construction or legal questions.

Short claims are not automatically strong. Long claims are not automatically narrow in a decision-relevant sense.

### P6. Legal and transaction events

Events may include:

- assignment;
- licensing disclosed in reliable records;
- security interests;
- opposition, review, invalidation, or litigation;
- lapse, expiry, abandonment, or restoration.

An event shows an event. It does not automatically prove value or threat. Interpret jurisdiction, procedural posture, outcome, and relevant claims with a patent professional when material.

### P7. Technical performance evidence

Extract:

- metric;
- value and unit;
- test conditions;
- baseline;
- sample size;
- uncertainty;
- observed or simulated status;
- source location.

Do not use numerical text as a hard gate until units, conditions, and extraction quality are reviewed.

## Paper assessment dimensions

### L1. Research-question relevance

- direct link to the SVOP function;
- mechanism correspondence;
- target conditions;
- cross-domain transfer conditions;
- explicit limitations.

### L2. Study design and methods

- primary research, review, preprint, conference, thesis, or other type;
- method appropriateness;
- controls and baseline;
- sample/system scale;
- statistical or uncertainty treatment;
- data/code/material availability;
- replication status.

### L3. Results and directness

- measured versus modeled result;
- effect size and units;
- confidence interval or uncertainty;
- boundary conditions;
- negative results and failure modes;
- whether the result supports the report claim.

### L4. Editorial and publication status

- peer reviewed, accepted, preprint, retracted, corrected, or other status;
- publisher or repository;
- conflicts of interest and funding when relevant;
- post-publication concerns.

### L5. Citation and field context

Use:

- age-normalized citation context;
- field and document type;
- independent replication or use;
- substantive citing relationship.

Do not apply a fixed recent-paper exemption or absolute percentile without explaining the dataset and method.

### L6. Organization context

Review demonstrated expertise and relevant outputs. Do not substitute QS, THE, or other institution rank for methods quality or direct evidence.

## Standards, cases, products, funding, and web sources

Assess:

- source authority;
- directness;
- document/event status;
- date and geography;
- method or verification transparency;
- independence;
- applicability;
- contradictions;
- commercial or promotional incentive;
- update and supersession risk.

## Scoring model

If a numeric score adds decision value:

```text
dimension score = anchored assessment within its declared range
weighted contribution = normalized dimension score × declared weight
total = sum of weighted contributions under the declared missing-data rule
```

Requirements:

- weights sum to 1 or 100%;
- every dimension has written anchors;
- evidence type has its own model;
- a score is accompanied by uncertainty or sensitivity;
- raw input fields remain visible;
- no unsupported precision is displayed;
- ranking does not replace analyst review.

## Example configuration structure

```json
{
  "model_id": "patent-evolution-priority-v1",
  "decision_context": "Select records for detailed evolution labeling",
  "evidence_type": "patent",
  "dimensions": [
    {
      "id": "technical_relevance",
      "weight": 0.40,
      "anchors": {"0": "none", "4": "direct under comparable conditions"}
    },
    {
      "id": "evidence_directness",
      "weight": 0.25,
      "anchors": {"0": "title only", "4": "reviewed claims and examples"}
    },
    {
      "id": "transferability",
      "weight": 0.20,
      "anchors": {"0": "incompatible", "4": "transfer conditions addressed"}
    },
    {
      "id": "strategic_context",
      "weight": 0.15,
      "anchors": {"0": "no support", "4": "corroborated actor/family/event context"}
    }
  ],
  "missing_data_rule": "show score range and require review",
  "sensitivity_scenarios": ["base", "technical-heavy", "transfer-heavy"]
}
```

This is an illustration, not a default.

## Sensitivity analysis

At minimum:

1. identify the top-ranked records under the base model;
2. vary material weights within a justified range;
3. test plausible missing-data values;
4. compare rank or tier stability;
5. flag records whose priority changes materially;
6. review whether one correlated dimension dominates;
7. retain results and model version.

## Review-depth assignment

The source used fixed score bands to decide full, standard, light, or skipped labeling. Localize this as a review plan:

- **Full review** — high decision impact, uncertain classification, or potentially route-defining evidence.
- **Standard review** — relevant evidence with adequate text and moderate decision impact.
- **Limited review** — contextual density or background only; no detailed claims.
- **Excluded from labeling** — ineligible, duplicate, or insufficient text.

Do not derive depth solely from the total score. Include risk, novelty of mechanism, disagreement, and evidence quality.

## Assessment record

```json
{
  "evidence_id": "E1",
  "eligibility": "accepted",
  "eligibility_reasons": [],
  "model_id": "patent-evolution-priority-v1",
  "dimension_scores": [],
  "raw_fields": {},
  "missing_fields": [],
  "score": null,
  "score_range": null,
  "sensitivity_status": "stable | unstable | not run",
  "review_depth": "full",
  "analyst_notes": "",
  "reviewer": "",
  "review_status": "reviewed"
}
```

## Stage gate

Do not advance until:

- eligibility and ranking are separated;
- every accepted record has adequate text;
- every model is evidence-type specific;
- anchors, weights, and missing-data rules are explicit;
- patent count unit and family handling are disclosed;
- field/age normalization is used or its absence is disclosed;
- opaque proprietary values are supplementary only;
- legal events are neutrally interpreted;
- paper methods and result directness are reviewed;
- sensitivity is run for material decisions;
- rejected and quarantined records remain traceable;
- full-review records are actually reviewed before route labeling.

## Outputs

- accepted evidence register;
- rejected/quarantined register;
- model configuration and version;
- raw and normalized dimension fields;
- score or qualitative assessment with uncertainty;
- sensitivity results;
- review-depth queue;
- unresolved specialist-review queue;
- Stage 5 handoff.

## Limitations

- Structured fields are incomplete and uneven across jurisdictions and document types.
- Citation, family, legal-event, and organization signals are confounded by age, field, resources, and reporting practice.
- Proprietary valuation methods may be opaque and correlated with other dimensions.
- Technical-performance extraction can fail on units, conditions, or claim context.
- Numeric scoring creates false precision if anchors are weak.
- A high review priority is not a legal, commercial, or technical conclusion.
