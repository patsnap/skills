---
copyright: "Copyright © Patsnap. All rights reserved."
name: create-technology-insight-report-rd
description: Create or rigorously review a source-traceable HTML technology-insight report that integrates patents, scientific literature, market and company evidence, standards, regulation, engineering evidence, technology routes, competitive context, candidate evidence gaps, emerging applications, claim-relevance screening, technical options, and decision actions. Use for a full technology-domain insight report or for auditing and localizing an existing report package.
---

# Create a Technology Insight Report

## Purpose

Produce a decision-ready, self-contained HTML report for a defined technology topic. The workflow integrates patent evidence with scientific, market, company, standards, regulatory, engineering, and current-awareness evidence. It preserves the source package's ten-section analytical topology and cross-section controls while replacing domestic-only assumptions, unsafe legal shortcuts, false “exhaustive” claims, fixed quotas, and external chart dependencies.

## Use this skill when

- a user requests a full technology-domain insight report in HTML;
- an R&D or strategy team needs patents, technology routes, companies, markets, standards, and applications in one evidence system;
- a product or IP team needs preliminary claim-relevance screening and a patent-professional review queue;
- a user wants an existing technology report diagnosed, localized, reconciled, or upgraded;
- the deliverable needs repeatable evidence IDs, search logs, consistency checks, and a source register;
- a technology area needs candidate research gaps and emerging-application hypotheses under bounded language.

## Do not use this skill as

- a substitute for a simple patent lookup;
- an FTO, infringement, validity, enforceability, patentability, or legal opinion;
- a pure market report with no technology or patent analysis;
- proof of global white space based on zero search results;
- an automatic investment, safety, clinical, regulatory, or procurement recommendation;
- a reason to fabricate data to complete all sections.

## Required report topology

Preserve the source's section IDs and order because the scripts and cross-section controls depend on them:

| ID | Localized section | Required purpose |
|---|---|---|
| `s0` | Decision brief | Evidence-linked actions, priorities, owners, milestones, triggers, and boundaries |
| `s1` | Market and industry context | Definition-compatible market/economic evidence and structural forces |
| `s2` | Technology routes and maturity | Routes, performance, maturity, adoption, dependencies, and uncertainty |
| `s3` | Competitive and value-chain evidence | Neutral actor mapping and comparable organization evidence |
| `s4` | Patent landscape and claim-review queue | Search coverage, metrics, representative evidence, and claim-relevance screening |
| `s5` | Standards and regulation | Applicable standards, regulation, status, clauses, dates, and gaps |
| `s6` | Signals and candidate evidence gaps | Evidence-backed activity signals and bounded research/gap candidates |
| `s7` | Emerging applications | Cross-domain transfer hypotheses, conditions, barriers, and validation |
| `s8` | Technical options and specialist review | Technical alternatives, validation needs, and legal/specialist actions |
| `s9` | Vertical scenario | One decision-relevant segment or application comparison |

All ten sections remain present. When a section is not applicable or evidence is inadequate, show an explicit state containing:

- why it is not applicable or incomplete;
- searches or evidence reviewed;
- decision consequence;
- what evidence would resolve it;
- owner and next review date.

Do not use “to be completed” placeholders in a release artifact.

## Core boundaries

### Patent boundary

This report may screen patent relevance. It does not decide infringement or FTO. Material claim interpretations and legal conclusions require a qualified patent professional in the relevant jurisdiction.

### Evidence-gap boundary

Use:

> Not observed in the reviewed search universe as of the evidence cutoff.

Do not use:

- global white space confirmed;
- no patents exist;
- no competitor is active;
- the field is unoccupied.

### Forecast boundary

Market forecasts, maturity expectations, and application scenarios retain publisher/method, assumptions, ranges, dates, and uncertainty. Do not turn a publisher forecast into an observed fact.

### Specialist boundary

Safety, regulatory, clinical, financial, environmental, export-control, competition-law, and other specialist conclusions are reviewed or withheld.

## Required intake

Establish:

- specific technology topic;
- included and excluded technical concepts;
- product/application boundary;
- decision to support;
- primary audience;
- geographies and languages;
- report date and evidence cutoff;
- historical/forecast periods;
- confidentiality and research authorization;
- target sections and depth;
- patent count unit;
- family and entity normalization rules;
- required market definition;
- target competitors or neutral inclusion criteria;
- applicable standards/regulatory jurisdictions;
- available source access;
- required reviewers;
- output path and overwrite permission.

Do not begin broad research until material ambiguity is resolved or recorded as a scope limitation.

## Evidence system

### Stable evidence IDs

Use one report-wide registry:

- `P#` or `E#` for patents only if a separate patent namespace is deliberate;
- otherwise prefer one global `E#` namespace for every evidence type;
- every ID resolves to one normalized record;
- every factual finding cites one or more IDs;
- every accepted record appears once in the source register.

### Evidence types

Keep separate:

- patent publication;
- patent family;
- scientific or technical paper;
- standard;
- regulation or official guidance;
- engineering case;
- product or company primary source;
- market report;
- funding or transaction event;
- current-awareness or other reviewed web source.

Do not add unlike counts without labels.

### Minimum evidence record

```json
{
  "id": "E1",
  "type": "patent | paper | standard | regulation | case | product | market | web",
  "title": "",
  "stable_identifier": "",
  "source_url": "https://...",
  "source_name": "",
  "published_date": "YYYY-MM-DD",
  "accessed_date": "YYYY-MM-DD",
  "language": "English",
  "geography": "Global or specified",
  "reviewed_location": "Claim, method, result, clause, page, or official section",
  "accepted_finding": "",
  "limitations": [],
  "review_depth": "full | standard | limited",
  "confidence": "high | medium | low",
  "review_status": "reviewed"
}
```

### Evidence quality

Assess:

- authority;
- directness;
- independence;
- method transparency;
- recency;
- applicability;
- contradictions;
- review depth.

Do not assign confidence solely by source type. A patent, paper, government page, or market report can still be incomplete or inapplicable.

### Corroboration

Two sources are not a mechanical requirement for every statement. Use corroboration proportionate to:

- decision impact;
- source directness;
- controversy;
- uncertainty;
- temporal volatility;
- specialist risk.

A direct primary source may support a narrow fact. A strategic conclusion usually benefits from independent evidence and contradiction review.

## Verified Patsnap MCP support

When currently exposed in the execution environment:

- `advanced_patent_search`: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- `patent_briefing`: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

Use the live tool schema as authoritative. Do not claim source-only `patent.fetch`, `paper.search`, `paper.fetch`, generic legal-event, valuation, family, citation, ranking, export, or trend functions unless independently verified.

Patsnap patent connectors do not automatically cover scientific literature, market reports, standards, regulation, company events, or engineering evidence. Use appropriate reviewed primary sources for those.

## Search log

Each search records:

- search ID;
- section/purpose;
- source or tool;
- exact query;
- fields and filters;
- classifications;
- geographies;
- languages;
- date coverage;
- searched-at timestamp;
- requested limit;
- `matched_total` and whether reported, estimated, or unavailable;
- returned count;
- reviewed IDs/count;
- accepted IDs/count;
- pagination or truncation;
- deduplication;
- limitations;
- analyst and review status.

`matched_total` is not the number reviewed. Returned records are not accepted records. Publication count is not family count.

## Phase 0 — Scope and preflight

Before analysis:

1. finalize intake;
2. copy the localized HTML skeleton into the authorized project output location;
3. set s0–s9 in exact order;
4. set version, report date, evidence cutoff, review status, and metadata;
5. initialize `references/sync_table_template.md` in the project workspace if the user authorizes a project artifact;
6. create evidence, search, rejected-record, and review registers;
7. confirm patent count and normalization rules;
8. confirm global Patsnap connector availability and schemas;
9. plan primary sources for every applicable section;
10. assign technical and specialist reviewers;
11. identify confidentiality constraints;
12. run an initial HTML structure check after placeholder content is removed or use a clearly draft-only skeleton state.

No source-absent file is added to this Skill package. Project artifacts are created only for an authorized report engagement.

## Section s1 — Market and industry context

### Purpose

Define the economic and industry context relevant to the decision. Do not insert a market number merely because the source topology contains a market section.

### Market-definition contract

Every value includes:

- metric ID;
- exact market/product/service definition;
- included/excluded segments;
- geography;
- currency;
- price year;
- base year;
- forecast year;
- source publisher;
- report title;
- publication date;
- observed, publisher estimate, publisher forecast, or analyst scenario;
- methodology/access limitations.

### Market reconciliation

When sources differ:

- display both or all relevant values;
- explain scope, currency, timing, method, and segment differences;
- avoid averaging incompatible definitions;
- select a decision baseline only with rationale;
- preserve uncertainty range.

### CAGR check

If CAGR is used:

```text
CAGR = (ending value / starting value)^(1 / number of years) - 1
```

Verify start/end years, values, and whether intervals or year labels are used.

### Industry frameworks

Porter Five Forces, PEST, value-chain analysis, S-curves, and portfolio matrices are optional analytical frames. They do not create data.

For each force or factor provide:

- evidence IDs;
- scope;
- observed facts;
- analyst interpretation;
- uncertainty;
- decision implication.

Do not force all frameworks into every report.

## Section s2 — Technology routes and maturity

### Route definition

For every route:

- route ID and name;
- technical definition;
- mechanism;
- architecture/components;
- performance metrics and conditions;
- advantages and tradeoffs;
- enabling dependencies;
- failure modes;
- maturity method;
- patent and literature evidence;
- organizations;
- standards/regulatory dependencies;
- adoption state;
- update date.

### Separate dimensions

Do not conflate:

- route identity;
- measured performance;
- TRL or maturity;
- manufacturing readiness;
- commercial adoption;
- patent activity;
- market share;
- timing scenario.

### TRL use

TRL is optional. If used:

- select a domain-appropriate definition;
- cite evidence for each level;
- record assessor and date;
- state uncertainty;
- do not infer TRL from “paper/patent/news” source type alone.

### Technology timeline

Technical routes often overlap. Label a timeline as:

- evidence dates;
- development phases;
- adoption milestones;
- scenarios.

Do not imply a strict generation sequence when routes coexist.

## Section s3 — Competitive and value-chain evidence

### Neutral organization inclusion

Include organizations based on declared evidence such as:

- relevant patent families or claims;
- technical publications;
- products/deployments;
- standards participation;
- manufacturing/supply capability;
- partnerships/acquisitions;
- market evidence;
- relevance to the decision.

Do not use “international versus domestic” as the required global structure. Use geography only when decision-relevant and neutrally defined.

### Organization normalization

Record:

- canonical name;
- aliases;
- historical names;
- parent/subsidiary relationship;
- relationship as-of date;
- geography;
- role in value chain;
- included evidence IDs;
- confidence.

### Comparison table

Use a shared field set:

| Organization | Role | Route evidence | Patent evidence | Product/deployment evidence | Current events | Limitations | Confidence |
|---|---|---|---|---|---|---|---|

Do not require a patent for every relevant actor if a patent is not the appropriate evidence. Do not treat absence of current public news as no activity.

### Value-chain view

Adapt roles to the domain:

- materials or data;
- components or enabling IP;
- equipment/infrastructure;
- system/platform integration;
- product/service delivery;
- downstream deployment/user;
- standards/regulatory/support ecosystem.

Organizations may span roles. Record the evidence for each role.

### Current events

The source fixed “last 12 months.” Use a window suited to volatility and evidence cutoff. Every event includes date, primary source, event type, technical relevance, and uncertainty.

## Section s4 — Patent landscape and claim-review queue

Read `references/s4_exhaustive_search_spec.md` before Section 4.

### Search coverage

Use iterative query expansion across:

- technical concepts and exclusions;
- IPC/CPC and neighboring classifications;
- synonyms/acronyms/translations;
- title/abstract/claims/description as supported;
- actors and aliases;
- citation/family relationships as available;
- time, jurisdiction, and status dimensions;
- recently published records;
- gap-check searches.

### Correct metric language

Use:

- database-reported `matched_total`;
- returned records;
- reviewed records;
- accepted records;
- publication records;
- simple families;
- transparent sample with selection method;
- analysis set.

Do not ban the word “sample.” A properly described sample is more honest than pretending a top-N return is exhaustive.

### Trend and share metrics

Every metric states:

- exact search universe;
- count unit;
- date field/range;
- classification scope;
- jurisdiction/status filters;
- family normalization;
- denominator;
- pagination/truncation;
- refresh date;
- limitations.

### Claim-relevance screening

For a defined product or feature:

1. identify the relevant jurisdiction/family member;
2. obtain current claim text and status context;
3. capture dated product/feature evidence;
4. map claim elements one by one;
5. record observed/possible/not observed/insufficient correspondence;
6. state uncertainty and claim-construction issues;
7. assign internal review priority;
8. send material items to a patent professional.

Do not use “more than 50% of elements” or similar percentages to determine legal risk.

### Section 4 outputs

- search coverage and log summary;
- activity metrics with denominators;
- IPC/CPC or concept distribution when supported;
- time trends when supported;
- organization/family patterns when supported;
- representative evidence;
- claim-relevance review queue;
- candidate gaps with search IDs;
- limitations and specialist boundary.

## Section s5 — Standards and regulation

### Evidence fields

For every record:

- issuing body or regulator;
- jurisdiction;
- identifier/title;
- version;
- document type;
- published, draft, ballot, proposed, effective, withdrawn, superseded, or other status;
- clause/section/work item;
- publication/effective/as-of dates;
- technical relevance;
- mandatory or voluntary status where determinable;
- source link;
- limitations and reviewer.

### Standards gaps

Distinguish:

- no applicable standard identified in the reviewed sources;
- standard lacks an explicit clause;
- clause is optional;
- work item is in progress;
- source access is incomplete;
- technical interpretation requires a specialist.

Do not call every absent clause a commercial opportunity.

### PEST or policy analysis

Use only when it supports the decision. Separate policy objective, binding rule, incentive, enforcement, standard, and analyst interpretation.

## Section s6 — Signals and candidate evidence gaps

### Activity signals

Possible signals:

- search-normalized patent-family growth;
- literature activity and methods/results;
- product/deployment milestones;
- funding/transaction events;
- standards/regulatory movement;
- new entrants or partnerships;
- performance/cost threshold changes.

Every signal has:

- metric/definition;
- baseline and date range;
- evidence IDs;
- denominator;
- confidence;
- contradicting evidence;
- decision implication.

The source's fixed thresholds—top three, fewer than ten, 60% concentration, 50% growth—are not universal. Calibrate them to the query universe, field size, and historical variance.

### Candidate-gap types

- patent evidence gap;
- standards/requirement gap;
- research/evidence gap;
- application/transfer gap;
- performance gap;
- integration/interface gap;
- capability/supply-chain gap.

### Candidate-gap record

```json
{
  "gap_id": "G1",
  "type": "patent evidence gap",
  "statement": "Not observed in the reviewed search universe",
  "search_ids": ["PS-21", "PS-22"],
  "search_scope": "",
  "supporting_evidence_ids": [],
  "contradicting_evidence_ids": [],
  "technical_relevance": "",
  "validation_required": [],
  "invalidation_conditions": [],
  "confidence": "low",
  "review_status": "reviewed-candidate"
}
```

### Gap-check

Inspect:

- synonyms and translations;
- classifications and adjacent classes;
- mechanism and parameter terms;
- actors and aliases;
- citations and families as available;
- product and non-patent evidence;
- secrecy/indexing/access limitations;
- feasibility and relevance.

No fixed number of zero queries proves absence.

## Section s7 — Emerging applications

### Transfer workflow

1. define the source function and mechanism;
2. identify candidate target applications;
3. compare conditions and constraints;
4. review target-domain evidence;
5. assess maturity separately for source and target;
6. identify transfer barriers;
7. define validation experiments;
8. estimate decision value and timing conditionally;
9. record IP, safety, regulatory, and ecosystem questions.

### Transfer screen

Compare:

- scale and geometry;
- materials/media;
- temperature, pressure, frequency, load, data rate, or environment;
- manufacturing and yield;
- reliability/lifetime;
- safety/regulation;
- cost/supply chain;
- interfaces/integration;
- user/workflow;
- intellectual-property/licensing;
- evidence maturity.

Do not use a fixed TRL-difference threshold as the recommendation rule.

### Application record

| Candidate application | Shared mechanism | Matching conditions | Different conditions | Evidence | Barriers | Required validation | Maturity/confidence |
|---|---|---|---|---|---|---|---|

## Section s8 — Technical options and specialist review

### Purpose

Document decision options arising from technical and patent evidence. Do not promise legal clearance.

### Option types

- modify a feature or architecture;
- use a different technical mechanism;
- alter sequence, interface, parameter, or system boundary;
- gather product/claim/test evidence;
- monitor a family or event;
- seek patent-professional opinion;
- explore license, partnership, acquisition, challenge, or other business/legal action with appropriate review.

### Option record

```json
{
  "option_id": "O1",
  "linked_screening_id": "CR-1",
  "technical_change": "",
  "mechanism": "",
  "performance_effect": "",
  "cost_and_manufacturing_effect": "",
  "safety_and_regulatory_effect": "",
  "validation": [],
  "supporting_evidence_ids": [],
  "uncertainty": [],
  "patent_professional_action": "",
  "owner": "",
  "status": "candidate"
}
```

Avoid star feasibility ratings without defined anchors. Use explicit evidence, dependencies, test plan, owner, and decision date.

## Section s9 — Vertical scenario

### Selection

Choose one segment/application because it materially affects the decision. State why it is selected and what is excluded.

### Analysis

Include as appropriate:

- user/system need;
- operating conditions;
- required metrics;
- technology routes;
- organizations/value chain;
- patent and standards context;
- economics;
- safety/regulation;
- adoption barriers;
- scenarios and triggers;
- recommendation boundaries.

### Visualization choice

Prefer a table when dimensions are heterogeneous or qualitative. Use CSS bars only with common scales and accessible values. Use a static inline SVG only when generated from reviewed data and accompanied by a table. Do not add Chart.js or external runtime.

Radar charts can conceal scale and weighting assumptions. If used, define every axis, scale, direction, source, and uncertainty; include the exact data table.

# End-to-end workflow

The workflow is evidence-first and iterative. A section is complete only when its statements trace to reviewed evidence, calculations are reproducible, and decision implications are bounded.

## Phase 1 — Frame the decision

### Confirm the decision question

Capture the decision, readers, decision owners, technology and application scope, geography, languages, time horizon, evidence cutoff, required comparisons, exclusions, legal or regulatory constraints, expected depth, and delivery date.

If the request is broad, propose and disclose a working scope. Never silently narrow a global request to one jurisdiction, language, database, or organization type.

### Build the scope model

Define the technology through:

1. core mechanism;
2. functional outcome;
3. components and materials;
4. process or architecture;
5. application context;
6. adjacent and substitute routes;
7. explicit exclusions.

Record later scope changes with a reason, date, and effect on prior results.

### Establish evidence classes

| Class | Typical source | Appropriate use | Important limitation |
|---|---|---|---|
| E1 | Primary paper, standard, patent publication, regulator record, official filing | Direct factual support | May be narrow, dated, or self-reported |
| E2 | Official organization publication, product documentation, public dataset | Organization, product, or market facts | Commercial framing may be selective |
| E3 | Reputable review, industry analysis, professional body | Context and synthesis | Verify methods, coverage, and date |
| E4 | News, commentary, search snippet, unverified aggregation | Discovery lead only | Never sole support for material claims |

Record provenance, publication date, retrieval date, scope, and limitations. The class does not replace source-specific judgment.

## Phase 2 — Design and execute research

### Create a query register

For every query, record:

- query ID and question served;
- source or database;
- exact query and filters;
- jurisdiction and language;
- date range;
- family/publication treatment;
- execution timestamp;
- matched total, if reported;
- returned, reviewed, accepted, and excluded counts;
- exclusions and follow-up action.

Never substitute matched totals for reviewed records. Never describe one returned page as the full universe.

### Search in layers

Use:

1. terminology and taxonomy discovery;
2. core-mechanism searches;
3. component, material, process, and architecture searches;
4. application and problem searches;
5. organization and inventor/author searches;
6. citation, family, and reference expansion;
7. substitute and adjacent-route searches;
8. negative and gap checks;
9. recent-event and status refresh.

For patent evidence, use the verified Patsnap patent-search MCP where available. Use patent briefing only for supported patent synthesis. Preserve connector names and registry links exactly; never invent tools or parameters.

### Assess coverage

Coverage is a documented argument, not the word “exhaustive.” Review synonym saturation, classification coverage, major organizations and inventors/authors, citation saturation, language and jurisdiction gaps, historical terminology, adjacent mechanisms, database limits, and contradictory evidence.

If new queries continue to produce material concepts, the search is not saturated. If stopping for time or access, state the stop rule and residual risk.

### Normalize records

For each accepted record:

- assign a stable evidence ID;
- preserve identifier and URL;
- capture bibliographic or business metadata;
- distinguish source, publication, priority, event, and retrieval dates;
- record the relevant passage, figure, table, claim, or data field;
- summarize only the point used;
- record inclusion or exclusion reasoning;
- identify duplicates and family relationships;
- label uncertainty and conflicts.

Do not count family members as independent inventions. Label whether counts are publications, applications, grants, families, organizations, products, or events.

## Phase 3 — Analyze without overclaiming

### Separate statement types

Distinguish observed fact, derived calculation, analyst interpretation, scenario assumption, and recommendation. Do not present inference as source fact. Preserve calculation inputs, formula, unit, missing-value treatment, and rounding.

### Resolve contradictions

When sources conflict:

1. check scope, date, unit, and definition;
2. prefer direct and authoritative evidence for the claim;
3. retain the conflict in the register;
4. explain which value is used and why;
5. carry material uncertainty into recommendations.

Never average incompatible figures simply to obtain one number.

### Compare technology routes

Choose decision-relevant dimensions such as mechanism, architecture, performance, reliability, lifetime, manufacturability, yield, scale-up, cost, supply dependencies, integration, safety, regulation, standards, ecosystem, evidence maturity, and intellectual property.

If using a weighted score, disclose anchors, weights, owner, sensitivity, missing-data treatment, and whether it is descriptive or decision-authoritative.

### Analyze organizations fairly

Separate research activity, patent activity, product availability, manufacturing capability, partnerships, regulatory status, and demonstrated performance. Publication or patent volume alone does not prove leadership, quality, freedom to operate, or commercial success.

### Handle patent evidence responsibly

This skill provides public-information technical intelligence, not a legal opinion.

- Read relevant independent claims and necessary context.
- Distinguish application, publication, grant, family, and legal status.
- Verify material status with an appropriate official or professional source.
- Avoid title-only relevance judgments.
- Never derive infringement probability from keyword or element percentages.
- Never label a route safe, clear, or non-infringing.
- Escalate material claim questions to a patent professional.

The report must explicitly state that it is not legal advice.

### Treat absence carefully

Use wording such as:

> No responsive evidence was observed in the reviewed search universe as of the evidence cutoff.

Do not convert zero results into claims that no technology, patent, organization, risk, market, or opportunity exists. Record query, source, date, scope, and limitations.

## Phase 4 — Synchronize the report

### Maintain one evidence registry

Use `references/sync_table_template.md` as the canonical working structure. Every material claim, metric, organization, route, risk, and recommendation links to evidence IDs or a labeled assumption.

Update the registry before finalizing prose. Never patch numbers independently in HTML.

### Run cross-section checks

Verify:

- scope terms remain consistent across s0–s9;
- dates and cutoff agree;
- organization names and aliases are normalized;
- routes use one taxonomy;
- counts retain unit and denominator;
- patent-family rules remain consistent;
- scenarios use stated assumptions;
- s8 options answer s6 issues;
- s9 reuses shared evidence and boundaries;
- s0 recommendations are supported downstream.

### Track changes

For material revisions record version, date, changed evidence or assumption, affected sections, changed implication, reviewer, and open action. Newer evidence does not automatically invalidate older evidence; assess whether it changes the relevant fact or decision.

## Phase 5 — Produce and release the HTML report

### Use the supplied template

Start from `references/html_skeleton_template.html`. Preserve section IDs s0 through s9 and their order. Replace all editorial markers before release.

Do not introduce external scripts, stylesheets, analytics, tracking pixels, remote fonts, or unreviewed embeds. The deliverable must work offline.

### Apply scientific editorial design

Use a light background, restrained navy and blue accents, readable system fonts, clear hierarchy, accessible contrast, efficient spacing, bordered tables with units and source notes, captions, and print-friendly layout.

Avoid neon styling, gradients, glass effects, ornamental dashboards, decorative motion, unexplained gauges, and color-only meaning.

### Choose visuals deliberately

- table for heterogeneous comparisons;
- bars for common-scale comparisons;
- line chart for comparable time series;
- scatterplot for two quantitative variables;
- timeline for events;
- flow diagram for dependencies;
- matrix for categorical relationships.

Prefer HTML/CSS. If inline SVG is necessary, generate it from reviewed data, add accessible text, and include the underlying table. Never construct HTML from unescaped source values.

### Cite at claim level

Place evidence IDs beside material claims. Each source-register record must provide title, publisher, date, identifier, link, retrieval date, evidence class, relevant scope, and limitations. A list of links alone is insufficient.

### Apply release metadata

Include report version, report date, evidence cutoff, review status, document title, matching footer version, and legal/evidence boundaries. Use ISO dates (`YYYY-MM-DD`).

# Quality-control protocol

## Manual review

Complete `references/quality_checklist.md`. Review decision alignment, coverage, traceability, calculations, terminology, units, legal boundaries, recommendation logic, accessibility, printing, confidentiality, and security.

## Automated checks

Run:

```bash
python scripts/sop_checklist.py all
python scripts/quality_check.py path/to/report.html
```

Automated checks are release gates, not substitutes for substantive review. Correct the report rather than weakening a checker to obtain a pass.

## Required negative tests

Verify that the checker rejects:

- missing, duplicated, or out-of-order section IDs;
- version mismatch;
- invalid dates;
- editorial placeholders;
- local absolute paths;
- external scripts or stylesheets;
- malformed table rows;
- unqualified legal conclusions;
- missing legal disclaimer.

# Common failure modes and corrections

## 1. Search totals treated as reviewed evidence

Report matched, returned, reviewed, accepted, and deduplicated counts separately.

## 2. Claimed exhaustive global coverage

Document the reviewed universe, search layers, stop rule, and residual gaps.

## 3. Publications and families conflated

Label count unit and deduplication rule every time.

## 4. Patent volume equated with leadership

Triangulate technical quality, products, manufacturing, partnerships, status, and evidence maturity.

## 5. Claim similarity converted into infringement risk

Provide an evidence-linked relevance screen and request patent-professional review.

## 6. Whitespace declared from zero results

Report bounded non-observation and test synonyms, classifications, jurisdictions, languages, assignees, and citations.

## 7. Arbitrary quotas or thresholds

Justify depth by decision materiality, diversity, saturation, and uncertainty; disclose operational limits.

## 8. Uncertainty hidden in a score

Show definitions, raw evidence, missing values, weights, sensitivity, and limitations.

## 9. Stale and current facts mixed

Separate source date, event date, status-check date, report date, and evidence cutoff.

## 10. Sources cited only at section level

Bind claims and calculations to evidence IDs at point of use.

## 11. Attractive but non-auditable output

Prioritize traceability, units, definitions, tables, and reproducibility over decoration.

## 12. Disconnected vertical scenario

Reuse the registry and show how the scenario changes the central decision.

## 13. Silent scope change

Record scope changes and revisit affected queries, counts, interpretations, and recommendations.

## 14. Automated checks treated as approval

Retain named human review for evidence, domain judgment, and legal boundaries.

# Failure and limitation handling

If a source, connector, or database is unavailable:

1. record what was unavailable and when;
2. continue with other authorized sources when useful;
3. never fabricate counts or content;
4. label the coverage gap;
5. explain its decision effect;
6. propose a specific follow-up.

If evidence cannot support a recommendation, provide a conditional recommendation or evidence-acquisition plan. Never force a definitive answer.

Protect confidential material. Do not expose it through external tools, logs, URLs, or a public source register.

# Deliverables

Unless the user requests otherwise, deliver:

1. one self-contained HTML report using s0–s9;
2. one completed synchronized evidence/search register;
3. quality-check output;
4. a concise handoff covering scope, evidence cutoff, limitations, and open actions.

Do not create extra deliverable files unless requested. The skill package contains only files present in the source package.

# Final handoff

Tell the user the decision addressed, report location, cutoff, review status, evidence classes and sources, coverage gaps, specialist-review needs, checks passed, and next validation action.

Never describe the report as legally cleared, exhaustive, or complete beyond its documented review universe.
