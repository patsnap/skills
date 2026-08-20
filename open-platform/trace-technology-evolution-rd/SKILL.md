---
copyright: "Copyright © Patsnap. All rights reserved."
name: trace-technology-evolution-rd
description: Build an evidence-backed technology-evolution map for a product or technical system using system decomposition, SVOP functional abstraction, parallel patent and literature research, reviewed scoring, a versioned TRIZ-inspired route taxonomy, evolution-forest visualization, and scenario-based forecasts. Use for technology evolution, next-generation product forms, route maps, cross-domain analogies, candidate white spaces, horizon scenarios, gray-rhino pathways, or low-probability disruption signals.
---

# Trace Technology Evolution

## Purpose

Turn a defined product or technical system into a decision-ready evolution assessment. Decompose the system into searchable functional units, abstract each unit with Subject–Verb–Object–Parameter (SVOP), collect patent and non-patent evidence, map observed solutions onto a disclosed route taxonomy, identify evidence gaps and transferable analogies, and produce scenario ranges rather than deterministic forecasts.

The source workflow has seven stages. Preserve that sequence, but do not preserve source-case counts, fixed cutoffs, hard-coded jurisdictions, or unsupported claims that a taxonomy node is a universal law.

## Use this skill when

- a user asks how a product or technology may evolve;
- a team needs a technology route map or evolution forest;
- the request seeks next-generation forms over stated horizons;
- a user wants cross-domain functional analogies;
- a team wants candidate evidence gaps or research targets;
- the request distinguishes high-probability pathways from low-probability disruption triggers;
- an R&D, product, strategy, or IP team needs an evidence-linked briefing.

## Do not use this skill as

- a substitute for a straightforward patent search when no evolution analysis is requested;
- an FTO, infringement, validity, patentability, or legal opinion;
- proof that an unobserved taxonomy node is legally or technically unoccupied;
- a valuation, market forecast, safety determination, or regulatory conclusion without appropriate evidence and specialist review;
- a reason to expose confidential product details to an external search service without authorization.

## Method boundaries

The eleven route families are a versioned analytical taxonomy derived from the source package's TRIZ-inspired method. They are hypotheses for organizing observed changes, not immutable physical laws. Record the taxonomy version used. The source package contains two non-equivalent node dictionaries: a compact renderer skeleton and a longer methodology dictionary. The localized package preserves both functions but does not silently merge them. The renderer uses the compact visualization skeleton in `assets/forest/triz_forest_common.py`; analytical labeling uses the declared methodology taxonomy in `references/step5-triz-labeling.md`. Any mapping between them must be explicit in project data.

An empty rendered node means “no accepted record in the reviewed dataset for this node.” It does not prove global white space, freedom to operate, novelty, or absence of commercial products. Call it an evidence gap or candidate research target until a documented search and specialist review support stronger language.

## Required intake

Before research, establish:

- product or system definition and excluded variants;
- decision the analysis must support;
- users and technical stakeholders;
- current baseline and target outcome;
- geographies and languages relevant to the decision;
- evidence cutoff and report date;
- forecast horizons as calendar ranges from the report date;
- whether cross-domain research is authorized;
- confidential-data handling constraints;
- patent count unit and family normalization rule;
- required specialist reviews;
- available time, source access, and acceptable evidence gaps.

Do not default to 3/5/10 years when the decision requires other horizons. If the user uses those labels, convert them to explicit calendar ranges and disclose uncertainty.

## Evidence model

Maintain one evidence register with stable IDs and these minimum fields:

- evidence ID and type;
- title and stable source link;
- publication or event date;
- accessed date and evidence cutoff;
- publisher, applicant, assignee, author, or organization as applicable;
- language and geography;
- reviewed text location: claim, abstract, methods, results, standard clause, official announcement, or equivalent;
- functional unit and SVOP anchor;
- route and node assignment;
- assignment rationale and quoted or precisely located support;
- observed result versus proposed or expected effect;
- confidence, review depth, and reviewer;
- limitations, contradictions, and update status.

Keep patent publications, patent families, papers, standards, engineering cases, funding events, product announcements, and web pages as distinct evidence types. Do not add their counts together without labels.

## Verified Patsnap MCP support

Patent research may use these verified global services when they are available in the execution environment:

- `advanced_patent_search`: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- `patent_briefing`: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

Use the currently exposed connector schema as authoritative. Do not claim source-only functions such as generic paper search, family fetch, valuation, legal-event lookup, or trend analysis unless those functions are actually exposed and verified at execution time.

For scientific literature, standards, product evidence, capital events, and regulatory or market signals, use reviewed primary publishers, repositories, standards bodies, regulators, company filings, or other authoritative sources appropriate to the domain. A pharma-specific connector is not a general engineering literature or news connector.

Every search log records service/source, query, filters, language, date searched, requested limit, returned count, reviewed IDs, pagination or truncation, deduplication, and coverage limitations.

## Seven-stage workflow

### Stage 1 — Decompose the system

Use the source hierarchy:

```text
Product or system
→ major systems
→ subsystems
→ components
→ critical parts or functional modules
```

The source's execution/control/power/transmission grouping is a useful starting frame, not a mandatory universal ontology. Adapt system boundaries to the domain while preserving traceability.

Evaluate a candidate critical part across four independent dimensions:

1. distinct physical or computational constraints;
2. a distinct engineering contradiction or tradeoff;
3. a stable, replaceable, or reviewable interface;
4. a distinct supplier, research, standards, or developer ecosystem.

Do not mechanically retain or delete a unit based on a score. Document the decision, dependencies, and consequences for search coverage.

Use `assets/mindmap/render_mindmap.py` with a reviewed JSON file to render the five-column decomposition. The bundled PLC JSON is an English structural example, not current market evidence.

### Stage 2 — Create SVOP anchors

For every selected component and critical part, record:

```text
Subject → Verb → Object → Parameter
```

- Keep the subject specific enough to identify the functional unit.
- Generalize the verb to a function transferable across product families.
- Generalize the object to the affected physical, informational, biological, or computational entity.
- Define the parameter as the measurable property changed or maintained by the action.
- Preserve secondary functions when they materially change search coverage; do not discard them automatically.
- Record synonyms, units, operating conditions, exclusions, and domain anchors.

Test each abstraction against at least one in-domain query and several plausibly different product families. Too-specific anchors miss analogies; overly abstract anchors create noise.

Follow `references/step1-2-components-svop.md`.

### Stage 3 — Run parallel research tracks

Run four conceptual tracks per approved anchor:

1. in-domain patents;
2. in-domain scientific or technical literature;
3. cross-domain patents;
4. cross-domain scientific or technical literature.

Add standards, regulation, engineering cases, product evidence, investment or funding, and new-entrant signals when relevant. These additional sources remain outside patent scoring.

Patent queries use claims/classification/keywords/semantics as supported by the verified connector. Literature queries prioritize technical relevance and direct methods/results over absolute citation rank. Do not force a minimum paper percentage or fill a quota with weak records. A sparse track is a disclosed finding, not permission to lower relevance.

Search windows, jurisdictions, languages, legal-status filters, citation filters, and result limits are decision-specific. Never apply the source's 2018 start, five-jurisdiction list, active-only status, citation threshold, or fixed per-bucket count as a universal default.

Follow `references/step3-double-track-search.md`.

### Stage 4 — Screen and assess evidence

Separate eligibility gates from ranking:

- Eligibility asks whether a record is relevant, reviewable, inside scope, and supported by adequate text.
- Ranking asks which accepted records deserve deeper attention.

Potential patent dimensions include family strategy, forward citation context, applicant capability, claim relevance, legal-event context, technical performance evidence, and adoption evidence. Potential paper dimensions include study relevance, methods quality, result directness, reproducibility, venue/editorial status, institutional context, and citation context.

Weights and anchors must be selected for the decision, sum correctly, treat missing values explicitly, avoid double counting, and include a sensitivity check. Proprietary values or opaque ratings are supplementary signals, never unexamined truth. Litigation, assignment, licensing, or broad family coverage does not by itself prove technical quality or commercial success.

Follow `references/step4-multi-dim-scoring.md`.

### Stage 5 — Label accepted evidence

Map each accepted record to zero, one, or more versioned route nodes. Do not classify from title alone. Use claims and description for patents where needed; use abstracts, methods, results, or full text for literature; use authoritative clauses or statements for other sources.

For each label, record:

- taxonomy and version;
- route and node;
- evidence text or location;
- reasoning;
- confidence;
- uncertainty and plausible alternative label;
- evidence type and maturity state;
- functional unit;
- whether the record suggests a dependent route transition;
- reviewer and review status.

A paper may demonstrate a laboratory state ahead of patent evidence, but node distance is not automatically a 1–3 year lead. Distinguish demonstrated maturity, manufacturing readiness, regulatory readiness, and adoption.

Use independent second review for high-impact or low-confidence labels. Measure agreement by route and node; do not average ordinal labels automatically when reviewers disagree. Resolve material disagreement or retain both interpretations.

Follow `references/step5-triz-labeling.md`.

### Stage 6 — Build the evolution forest

Organize accepted records as:

```text
Functional unit
├─ parallel route trunk A
│  ├─ observed nodes
│  └─ evidence-supported dependent route
└─ parallel route trunk B
```

Preserve multiple supported route trunks. A dependent route edge requires evidence of dependency, not mere co-occurrence. If a legacy co-occurrence heuristic is shown, label it as an unverified candidate and keep it visually distinct.

Use three carefully bounded concepts:

- **branch point**: a node with evidence that another route depends on it;
- **analogy candidate**: a source solution with documented functional transfer conditions and barriers;
- **evidence-gap candidate**: an unobserved next node in the accepted dataset that requires further search and feasibility review.

Do not call every zero-hit node an opportunity. Search recall, taxonomy fit, commercial secrecy, language, access, and publication lag may explain the gap.

Render with:

```bash
python assets/forest/render_forest.py \
  --records <reviewed-records.json> \
  --out <evolution-forest.html> \
  --title "Technology Evolution Forest"
```

The renderer displays the compact route skeleton declared in `triz_forest_common.py`. It escapes untrusted text, validates route/node references, derives counts, refuses unreviewed inputs, and does not create a legal or global-white-space conclusion.

Follow `references/step6-evolution-tree.md`.

### Stage 7 — Develop horizon scenarios and report

Forecasting is scenario analysis. For each candidate path, state:

- baseline date and horizon range;
- current observed state;
- candidate next state;
- supporting and contradicting evidence IDs;
- technical dependencies and bottlenecks;
- manufacturing, cost, supply-chain, safety, regulatory, standards, ecosystem, and adoption conditions;
- maturity estimate and method;
- confidence and update trigger;
- invalidation condition;
- responsible monitor and review cadence.

Do not convert route position directly into a calendar date. TRL or another maturity scale informs readiness only when supported by evidence and used consistently. Route direction describes an analytical change, not speed.

Classify strategic signals by decision behavior rather than dramatic labels:

- a high-probability pathway has accumulating independent evidence and a monitorable implementation path;
- a low-probability disruption has uncertain timing, a plausible causal mechanism, material impact, and explicit triggers;
- the same topic may require both a baseline roadmap and a contingency trigger.

Any BSS or TDI score is a transparent project-specific rubric. Define dimensions, anchors, weights, missing-data treatment, calibration set, and sensitivity. Never present the source's initial thresholds as validated universal cutoffs.

Develop a conservative, accelerated, and disruption-conditioned product concept. Avoid a single overfit flagship. Check system compatibility and conflicts among component predictions.

Populate `assets/report/report_skeleton_mckinsey.html` only with reviewed, escaped content. Despite the legacy filename, the localized visual system is neutral scientific/editorial design and does not claim affiliation with McKinsey & Company.

Follow `references/step7-prediction-report.md`.

## Required consistency gates

Before delivery, verify:

- every factual finding cites an accepted evidence ID;
- every patent reference has a stable publication identifier or record link;
- every paper reference has a DOI, repository ID, or stable publisher link when available;
- every route assignment has evidence and taxonomy version;
- every branch edge distinguishes explicit dependency from heuristic co-occurrence;
- every analogy names transfer conditions and barriers;
- every gap uses “not observed in the reviewed dataset” unless stronger research proves more;
- every forecast has a baseline, horizon, dependencies, evidence, confidence, trigger, and invalidation condition;
- evidence types and count units remain separate;
- all displayed totals derive from accepted records;
- report statements reconcile with the source register and search log;
- HTML is escaped, self-contained, accessible, responsive, and printable;
- no secret, personal path, cache, temporary file, domestic-only link, or unapproved extra package file remains.

## Deliverables

Use source-defined artifact names only when the user needs file outputs. The package itself adds no source-absent files. Typical project artifacts include:

- system-decomposition data and HTML;
- SVOP register;
- patent, paper, standards, case, and web evidence registers;
- search log and rejected-record log;
- scoring configuration and sensitivity results;
- labeled evidence and reviewer-disagreement log;
- evolution-forest JSON and HTML;
- branch, analogy, and evidence-gap candidate registers;
- horizon scenarios and monitoring triggers;
- concept alternatives;
- consistency-check results;
- final scientific/editorial report and complete source register.

## Failure behavior

- If the product boundary is unclear, analyze no further than a provisional decomposition and state what remains unresolved.
- If research access is unavailable, provide the method and query plan only; do not invent current evidence.
- If a track is sparse, preserve the sparse state and search limitations.
- If only titles are available, do not assign detailed nodes or make forecasts from them.
- If route reviewers materially disagree, retain the disagreement and lower confidence.
- If a gap search is incomplete, do not label global white space.
- If evidence does not support calendar timing, provide dependencies and monitoring triggers instead of a date.
- If the report cannot pass consistency gates, deliver an explicit review queue rather than a polished but unsupported conclusion.

## Handoff

Lead with decision implications and include:

- scope and evidence cutoff;
- systems, functional units, and route taxonomy version;
- accepted evidence totals by type and patent count unit;
- searches run, omitted, failed, or truncated;
- strongest observed pathways and their evidence;
- analogy and evidence-gap candidates with limitations;
- scenario ranges, assumptions, triggers, and invalidation conditions;
- specialist review still required;
- paths to the complete artifacts.

Do not paste a duplicate full report when the user requested files.
