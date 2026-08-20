---
copyright: "Copyright © Patsnap. All rights reserved."
name: analyze-technology-patent-trends-ip
description: Convert an already retrieved, screened, and tagged patent dataset into an evidence-bounded competitive technology insight report. Use when the user requests patent-based technology-route analysis, competitor positioning, taxonomy-by-function matrices, process-route analysis, opportunity windows, trend signals, R&D/IP actions, or a management-grade Markdown or self-contained HTML white paper from prepared patent data.
---

# Analyze technology patent trends

## Purpose

Transform a prepared patent dataset into decision-ready competitive technology insight without exceeding the dataset's fields, tag semantics, coverage, or evidence boundary.

This skill is the final analysis stage, not a substitute for retrieval, screening, tagging, legal review, market research, or product evidence.

Read:

- `references/white-paper-framework.md` before drafting any report; and
- `references/html-report-template-spec.md` before generating HTML.

Read `README.md` only when setup or connector guidance is needed.

## Upstream workflow gate

The preferred local suite is:

1. `search-patents-ip` — retrieved patent pool and search manifest;
2. `analyze-patent-search-results-ip` — reproducible dataset statistics;
3. human Stage 3.5 — retained/excluded/uncertain screening decisions;
4. `tag-patent-search-results-ip` — tagged records, tag dictionary and tagging manifest; and
5. this skill — competitive technology analysis.

Equivalent user-supplied artifacts are acceptable if they contain the same provenance and semantics.

Do not imply that an upstream stage was completed when its artifact is missing.

### If only company names are supplied

Run or propose retrieval first. Resolve legal entities and define the technology scope before analysis.

### If records are retrieved but unscreened

Run or request screening. Do not treat every search hit as technically relevant.

### If records are retained but untagged

Run or request tagging. Do not construct a technology-type/function matrix from titles alone and describe it as formally tagged data.

### If tags are partial

Analyze only supported dimensions. Report missingness and tag coverage in the research boundary.

## Required input contract

Capture or derive:

- original research question and target decision;
- target company or reference portfolio, if any;
- source dataset and immutable artifact identifier;
- retrieval query and search cutoff;
- screening criteria and status counts;
- tag dictionary, definitions, hierarchy and version;
- tag-assignment method and reviewer status;
- patent record count;
- publication/application/family counting unit;
- family and deduplication rule;
- assignee/entity normalization method;
- jurisdictions and languages;
- date field and exact range;
- legal-status source and as-of date;
- citation source and retrieval date;
- multi-label counting rule;
- missing-value rule;
- coverage for each candidate dimension;
- industry/domain mapping sources; and
- output format and approved path.

Never silently combine publication-, application-, and family-level counts.

## Output selection

- Use Markdown when the user asks for a draft, outline, analytical narrative, reviewable content, or no file.
- Use self-contained HTML only when requested for HTML, a visual report, a single-page report, or a final artifact that clearly benefits from it.
- If the user requests a complete/final report but does not specify a format, ask only when the artifact choice materially matters; otherwise provide Markdown and state that HTML is available.
- Do not create a script, dataset, README, asset, or agent file inside this package at runtime.

## Connector boundary

MCP is not required when the user supplies a complete validated tagged dataset.

### Advanced Patent Search

Required only when retrieval or validation must be executed or extended.

- https://open.patsnap.com/marketplace/mcp-servers/patent-search
- key: `advanced_patent_search`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`

### Patent Briefing

Recommended for selected-record bibliography, family, legal status, claims, description, translations, and images.

- https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- key: `patent_briefing`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`

### Deep Patent Mining

Recommended to validate technical topics, problem/means/effect, classifications, materials, and applications.

- https://open.patsnap.com/marketplace/mcp-servers/patent-mining
- key: `deep_patent_mining`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-mining`

Inspect live schemas and record connector, tool, request, response semantics, retrieval date, and limitations. Do not claim other source-listed MCPs are configured unless independently verified.

## Core evidence rules

1. Analyze only dimensions represented by formal fields or declared derived fields.
2. Do not infer or invent absent tags.
3. Omit an unsupported deep-analysis chapter; describe the gap in methods and next-data recommendations.
4. Separate patent-data observations from domain/industry mappings.
5. Domain knowledge may help interpret a tag; it does not prove competitor activity, product strategy, clinical effect, market demand, or manufacturing capability.
6. Every strategic finding must cite its data table/calculation and, where relevant, representative patent evidence.
7. Use bounded language: “indicates within this dataset,” “is consistent with,” “suggests,” or “requires validation.”
8. Assign evidence strength under explicit criteria.
9. Record counting, denominator, missingness, tie, and multi-label rules.
10. Do not equate patent count with quality, barrier, market share, R&D spend, product success, enforceability, or freedom to operate.

## Field and coverage gate

Create a field-readiness table before analysis:

| Dimension | Field(s) | Semantic definition | Non-missing coverage | Validated coverage | Counting rule | Supported analysis | Unsupported inference | Decision |
|---|---|---|---:|---:|---|---|---|---|

Candidate dimensions:

- technology type/category;
- technical function;
- process/method;
- material/component;
- application/use case;
- applicant/assignee;
- filing/priority/publication time;
- legal/status fields;
- family fields;
- citations;
- claims/technical text; and
- domain-specific tags.

Use a dimension in the body only when:

- the field exists;
- its definition is unambiguous;
- coverage is disclosed and fit for the requested inference;
- counting semantics are consistent;
- validation quality is adequate; and
- the analysis can close a defensible evidence chain.

Do not use a universal coverage threshold. State why the chosen threshold is adequate for the decision and run sensitivity when borderline.

Missing values are unavailable, not zero.

## Data preparation

### Validate record identity

- Confirm unique record keys.
- Detect duplicate publications and family members.
- Preserve original and normalized assignees.
- Separate family-level from document-level analysis.
- Confirm screening status and tag lineage.

### Validate tags

- Check dictionary version and definitions.
- Identify mutually exclusive versus multi-label fields.
- Check unknown/other handling.
- Review tag combinations that violate the dictionary.
- Quantify untagged, partially tagged, and reviewer-unconfirmed records.
- Preserve confidence or reviewer status where available.

### Normalize time

- Use one declared date field per trend.
- Identify partial years.
- Do not compare incomplete current periods with full prior periods without adjustment or warning.
- Use exact current report-generation and evidence-cutoff dates; never hard-code a year.

### Normalize assignees

- Separate legal entity, normalized group, and display label.
- Do not aggregate subsidiaries without an approved rule.
- Record mergers, former names, and acquisitions only with evidence.

### Define multi-label counts

State whether:

- each record contributes once per label;
- fractional counting is used;
- primary labels are used; or
- combinations are counted as distinct cells.

Totals across labels may exceed the number of patents; disclose this.

## Recommended analytical frame

Use **technology taxonomy/type × technical function** as the core matrix when both fields pass the gate.

Add **method/process** as a route lens only when that field passes.

For another domain, rename these axes to fit the supplied ontology while preserving the logic:

- what the technology is;
- what it does; and
- how it is implemented.

## Analysis modules

### 1. Overall competitive landscape

When supported, analyze:

- portfolio scale under one counting unit;
- type/taxonomy breadth and concentration;
- function breadth and concentration;
- method/process breadth and concentration;
- shared hotspots;
- differentiated clusters; and
- dominant competitive battlegrounds.

Output:

- strategic overview;
- competitor comparison table;
- data findings;
- strategic interpretation;
- relevance to the target company; and
- evidence strength.

### 2. Resource positioning by technology type

Ask:

- Which types have the highest tagged density?
- Which companies concentrate on specific types?
- Which portfolios are broad or focused?
- Which positions persist across counting/family rules?
- Which types have domain-mapping relevance that requires external validation?

Output a company × type table or heatmap with visible values and coverage notes.

### 3. Functional value layout

Ask:

- Which functions are common?
- Which are concentrated?
- Which show potential differentiation?
- Which functions are broad labels that require subdivision?
- Which domain/market interpretations are mappings rather than patent conclusions?

Do not infer efficacy, productization, users, price, regulation, or market performance from a function tag alone.

### 4. Type × function matrix

This is the core chapter when both axes pass the gate.

Identify:

- high-density combinations;
- recent-growth combinations when time exists;
- company-leading combinations when assignee exists;
- multi-company overlap;
- low-density combinations; and
- potentially valuable combinations under separately sourced domain mapping.

Do not call low density an opportunity without need/feasibility/evidence. Do not call high density a moat without claims, status, family, continuity, technical depth, and alternatives.

### 4B. Method/process route pattern

Include only when method/process tags pass the gate.

Analyze:

- route frequency;
- company concentration;
- association with types and functions;
- temporal persistence;
- tag coverage; and
- whether evidence supports repeated route positioning or isolated mentions.

A method tag is not proof of full manufacturing capability or process-platform leadership.

### 5. Competitor strategic profiles

Use bounded, supported labels such as:

- type-concentrated;
- function-concentrated;
- type-function combination leader within the dataset;
- broad-coverage portfolio;
- emerging-direction accelerator; or
- existing-portfolio defender.

For each company report:

- included legal entities;
- portfolio count/unit;
- core types/functions/methods;
- leading combinations;
- breadth and concentration;
- time trend if supported;
- possible strategic interpretation;
- implication for the target company;
- evidence strength; and
- data boundary.

Do not assert product-market or customer-segment strategies without relevant external evidence.

### 6. Potential barriers and opportunity windows

Use conservative layers.

With type/function tags only, discuss density, concentration, crowding, overlap, and evidence needed.

With method tags, discuss potential route concentration—not manufacturing dominance.

Assess stronger barrier hypotheses only when claims, grants/status, family, citations, continuations, ownership, and relevant technical evidence support them.

Opportunity windows require:

- problem or need;
- technical feasibility;
- low/medium crowding evidence;
- white-space stability across query/tag choices;
- relevance to the target company; and
- validation actions.

### 7. Future focus assessment

Include only with adequate time fields and comparable periods.

Use:

- recent application growth;
- newly appearing tags;
- combination growth;
- multi-company acceleration;
- sustained single-company concentration; and
- persistence across family/counting rules.

Label partial years and small denominators. Patent publication delay limits recency inference.

### 8. R&D and patent-layout recommendations

Classify every recommendation:

- A — directly supported by the analyzed data;
- B — inspired by separately identified domain/industry mapping; or
- C — requires additional data before decision.

Possible actions include:

- targeted prior-art or landscape refinement;
- R&D pre-research;
- FTO review;
- added tagging for method, product, application, evidence, standards, or claims;
- competitor claim/status/family review;
- portfolio gap review;
- monitoring; and
- validation against product, technical, regulatory, or market evidence.

Do not recommend filing solely because a matrix cell is sparse.

## Evidence strength

Use:

- **Strong:** direct, reproducible dataset evidence; adequate coverage; stable under reasonable counting/tag choices; representative records verified where needed.
- **Moderate:** consistent signal with some coverage, semantic, time, or counting limitation.
- **Limited:** sparse or indirect evidence, mapping-dependent interpretation, or high sensitivity.
- **Insufficient:** cannot support the conclusion; place in data needs, not findings.

For each finding state:

- observation;
- calculation/table/figure ID;
- representative evidence if needed;
- interpretation;
- implication;
- strength; and
- limitation/alternative explanation.

## Standard report structure

Adapt chapters to available fields:

| Section | HTML ID | Content |
|---|---|---|
| Executive summary | `summary` | Strategic findings and strength |
| Methods and boundary | `methods` | Scope, fields, counting, coverage |
| Competitive overview | `overview` | Overall landscape |
| Technology type | `tech-type` | Type positioning |
| Function | `function` | Functional layout |
| Core matrix | `matrix` | Type × function |
| Method/process | `method-route` | Optional route analysis |
| Profiles | `profiles` | Competitor profiles |
| Barriers/opportunities | `opportunity` | Bounded hypotheses |
| Future focus | `future` | Optional time signals |
| Actions | `action` | A/B/C recommendations |
| Sources/limitations | `sources` | Evidence and caveats |

Omit unsupported deep-analysis sections from navigation and body.

## Writing style

Use US English unless the user requests another language.

Write for management readers:

- lead with the decision-relevant outcome;
- use precise patent and technical terminology;
- keep observation separate from interpretation;
- define counts and denominators;
- explain uncertainty without burying it;
- avoid promotional superlatives; and
- use formal, restrained white-paper language.

Every substantive chapter should contain:

- data finding;
- strategic interpretation;
- implication for the target company;
- evidence strength; and
- limitation.

## HTML boundary

Follow `references/html-report-template-spec.md`.

The HTML artifact must be:

- self-contained;
- semantic and `lang="en"`;
- accessible without color, hover, animation, or JavaScript;
- based only on validated values;
- explicit about chart units, axes, denominators, and missing data;
- responsive and print-safe;
- free of gradients, particles, ticker/marquee, emoji, and external CDN dependencies; and
- saved only to the user-approved path.

Do not render an unavailable dimension as zero.

## Final validation

- Upstream artifact status is truthful.
- Source counts reconcile.
- All dimensions have field and coverage support.
- Tag dictionary/version and multi-label rule are visible.
- Company/entity aggregation is explicit.
- Date field and partial periods are visible.
- Patent observations and industry/domain mappings are separated.
- Matrix totals use declared counting rules.
- Evidence strengths meet their definitions.
- Every strategic conclusion maps to evidence.
- Unsupported chapters are omitted.
- Legal/status/citation language is bounded.
- HTML has no placeholder, external dependency, missing-as-zero, or inaccessible chart.
- Current dates are generated dynamically, not hard-coded.
