---
name: assess-technology-market-and-patent-landscape-ip
description: Assess a defined product or technology field for project initiation by combining current market evidence, a reproducible global patent landscape, individually validated key players, technical themes and gap hypotheses, jurisdictional filing footprint, competitive tiers, risks, and differentiated project options in a self-contained scientific HTML report. Use for technology-market landscape, patent landscape, opportunity mapping, or R&D project-entry decisions.
---

# Assess a Technology Market and Patent Landscape

## Objective

Produce an evidence-backed project-initiation assessment for a defined product or technology field.
Integrate market, patent, technical, competitive, regulatory, and strategic evidence without allowing
one evidence type to stand in for another.

The output supports project screening and further diligence.
It is not investment advice, a market forecast guarantee, an FTO opinion, or a legal conclusion.

## Trigger conditions

Use when the user supplies:

- a product or technology field;
- optional keywords or classifications;
- optional known market or patent players;
- a request for market and patent landscape analysis;
- a request for technical hot spots, opportunity gaps, competitive tiers, or project directions;
- a request for an evidence-backed project-initiation report.

Reject or narrow an unsearchably broad field before analysis.

## Required inputs

Capture:

- product or technology definition;
- intended application and customer/use context;
- inclusion and exclusion rules;
- decision question and project horizon;
- geographic market scope;
- patent jurisdiction scope;
- priority/publication date window;
- family and counting rule;
- known players and aliases;
- desired technical segmentation;
- market currency and reporting basis;
- relevant standards, regulation, safety, or certification context;
- output and audience requirements.

If these are not supplied, make conservative, disclosed assumptions that do not materially change the question.

## Evidence architecture

Keep six evidence classes separate:

1. patent records and full-population patent metrics;
2. company filings and official company information;
3. government, regulator, standards-body, and industry-association sources;
4. reputable market research with visible scope and method;
5. engineering, academic, and technical evidence;
6. analytical inference.

Every material conclusion must cite one or more source IDs and state its evidence class.
Patent evidence cannot prove market size, customer demand, product deployment, company intent, or profitability.

## Verified PatSnap MCP services

Use the English interface and English output.
Inspect the live tool schema before use.

### Required: Advanced Patent Search

- Connector key: `advanced_patent_search`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`
- Use: global patent search, assignee-specific validation, representative records,
  and reproducible complete-bucket counts where supported by the live schema.

### Required: Patent Briefing

- Connector key: `patent_briefing`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- Use: representative patent bibliography, family, status, claims, description,
  translations, images, and technical problem/solution/effect summaries.

### Recommended: Deep Patent Mining

- Connector key: `deep_patent_mining`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-mining
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-mining`
- Use: technical topics, problems, solutions, effects, classifications, materials,
  and application domains.

Use authoritative web or approved sources for current market, company, policy, standards,
regulation, customer, and supply-chain evidence.

Record for every connector call:

```text
connector_key
tool_name
request_or_query_id
query_version
filters
response_semantics
retrieval_timestamp
source_locator
limitations
```

Do not invent an aggregation, count, or response field.

## Core data rule

### Full-population metrics

Use only a verified full-result aggregation or complete reproducible bucket plan for:

- annual filing/publication trends;
- applicant or assignee counts and shares;
- jurisdiction counts and shares;
- PCT-use rates;
- technical-theme counts and shares;
- concentration metrics;
- growth rates;
- competitive rankings.

### Representative records

Use a relevance-ranked record set only for:

- examples;
- technical reading;
- claim evidence;
- problem/solution/effect illustration;
- search validation.

Never calculate landscape shares or infer absence from a Top-K sample.
If complete metrics are unavailable, mark the metric `Unavailable` and explain why.

## Eleven-step workflow

### Step 1 — Parse and normalize the input

Create a scope card:

```text
scope_id
field_name
product_or_technology_definition
included_concepts
excluded_concepts
applications
decision_question
market_geographies
patent_jurisdictions
date_window
family_rule
count_unit
status_rule
cutoff
known_players
known_terms
known_classifications
```

Build:

- English-first synonyms and abbreviations;
- spelling and transliteration variants;
- technical mechanism and application terms;
- false-positive exclusions;
- IPC/CPC candidates;
- adjacent terminology likely to hide relevant work.

Output a versioned search concept map.

### Step 2 — Build the key-player validation register

Before using patent results to rank players, create a current candidate-player register from:

- user-provided companies;
- current company and market evidence;
- industry associations or authoritative sector sources;
- known technology suppliers and adjacent entrants;
- applicant names discovered during validated patent search.

For each player record:

```text
player_id
legal_name
normalized_name
aliases
corporate_group_scope
relevance_to_field
market_evidence_ids
patent_evidence_ids
validation_state
```

Do not use a fixed China-versus-overseas list.
Include relevant local and global players based on the decision geography and evidence.
Do not impose a market-share threshold without a dated source and compatible segment definition.

### Step 3 — Research market size and trends

Prioritize recent primary and authoritative sources.
For each market datum capture:

```text
metric_id
market_segment
geography
period
actual_or_forecast
value
currency
nominal_or_real_basis
unit
methodology
publisher
source_date
access_date
source_id
limitations
```

Analyze the most decision-relevant recent three years when comparable evidence exists.
Do not force a three-year series from incompatible sources.

Record:

- market size and growth with source-defined scope;
- forecast ranges and assumptions;
- demand drivers;
- policy and regulatory drivers;
- standards and certification requirements;
- supply-chain constraints;
- customer pain points;
- adoption barriers.

If sources disagree, explain segment, geography, currency, year, or methodology differences.
Do not average incompatible estimates.

### Step 4 — Run the global patent search

Create and validate a versioned query:

1. broad discovery search;
2. inspect relevant and irrelevant records;
3. refine concepts, classifications, fields, and exclusions;
4. test known relevant documents;
5. record query, version, database, date, filters, and matched total;
6. choose family and counting rules;
7. document publication lag and coverage limitations.

Target up to fifty representative records for evidence review when available.
If fewer valid records exist, use all valid records and disclose the count.
Do not broaden the time window or keywords merely to reach fifty.

The global scope should reflect the technology and decision question.
Common authorities may include CN, US, EP, JP, KR, WO, DE, AU, CA, GB, IN, and others,
but no fixed list proves completeness.

### Step 5 — Validate each key player separately

For every player in the register:

1. verify legal entity, subsidiaries, historic names, and aliases;
2. run a field-scoped assignee search;
3. record the query and matched total;
4. inspect representative patents;
5. classify technical themes using evidence;
6. record jurisdictions only through complete aggregation or complete buckets;
7. record unavailable metrics explicitly;
8. avoid attributing subsidiaries to a group without documenting the ownership scope and date.

Key-player table:

```text
player_id
normalized_name
alias_scope
search_query_id
full_population_count_or_unavailable
count_unit
core_technical_themes
representative_patent_ids
jurisdiction_metric_state
evidence_ids
limitations
```

### Step 6 — Analyze technical themes and gap hypotheses

#### Step 6.1 — Define the taxonomy

For each technical direction define:

- theme ID and label;
- technical inclusion and exclusion rules;
- query or classification logic;
- overlap with other themes;
- requirement or market-need linkage;
- complete metric state;
- evidence sources.

Do not force mutually exclusive shares when themes overlap.

#### Step 6.2 — Classify theme state

Use text states:

- `Hot`: high and recent activity under a disclosed, comparable threshold;
- `Mature`: established activity with evidence of stable or broad development;
- `Gap hypothesis`: apparently sparse evidence after a documented negative search;
- `Declining`: comparable activity has fallen under a disclosed method;
- `Unresolved`: evidence is incomplete or not comparable.

The source’s 15%, 50%, 3%, and three-player figures may be used only as project-specific thresholds
after confirming a complete denominator and explaining why they fit the field.
They are not universal rules.

#### Step 6.3 — Test four gap routes

1. low-density technical branch;
2. intersection of established technical routes;
3. user or market pain point with sparse patent evidence;
4. application or operating scenario with sparse validated evidence.

For every gap hypothesis perform:

- synonym and classification expansion;
- adjacent-field and mechanism search;
- assignee and inventor review;
- backward/forward citation exploration where useful;
- non-patent technical literature check;
- feasibility and operating-envelope review;
- market-need evidence check;
- standards/regulatory check;
- FTO and third-party-rights follow-up definition;
- search-limit and false-negative assessment.

Use this output:

```text
gap_id
hypothesis
need_evidence
technical_feasibility_evidence
negative_search_protocol
patent_metric_state
adjacent_evidence
known_counterevidence
confidence
entry_path
validation_gate
risks
```

Patent scarcity alone is not white space.

### Step 7 — Analyze jurisdictional filing footprint

#### Objective

Describe where applicants have filed under verified data.
Do not present filing geography as proven market intent.

#### Metrics

- authority coverage breadth;
- complete count by authority;
- share by authority when a complete denominator exists;
- PCT-route records and rate when defined consistently;
- top filing authorities;
- authorities where peers have records but the applicant has none under the search scope.

#### Required method

Use direct verified aggregations or a complete authority-by-authority bucket plan.
Do not derive a matrix from representative records.

Matrix cells must show:

- count and unit;
- query ID;
- cutoff;
- complete/unavailable state;
- not `0` unless a complete validated search returned zero.

Interpretation states:

- broad international filing footprint;
- regionally concentrated filing footprint;
- selected international filings;
- insufficient evidence.

Avoid “offensive,” “defensive,” or “target market” labels unless supported by independent company evidence.

### Step 8 — Build competitive tiers

Use a transparent multi-evidence framework, not patent count alone.

Possible dimensions:

- verified market position;
- patent activity under a complete metric;
- claim and technical depth from representative evidence;
- breadth of technical themes;
- jurisdictional filing footprint;
- product or deployment evidence;
- standards/regulatory position;
- evidence quality and currency.

Create three tiers only when the evidence supports meaningful grouping.
Otherwise use a comparative table without forced tiers.

For each company show:

- entity scope;
- tier or state;
- key strengths;
- technical focus;
- representative patents;
- filing-footprint observation;
- market evidence;
- limitations.

### Step 9 — Assess opportunities and risks

Create three to five evidence-backed items in each group where available.

Opportunity dimensions:

- validated customer or market need;
- technical gap hypothesis;
- emerging application;
- standards or policy change;
- supply-chain or cost change;
- partnership or licensing option;
- under-served geography or segment supported by market evidence.

Risk dimensions:

- incumbent scale and product position;
- credible claim-level patent barriers;
- regulatory and certification burden;
- engineering maturity and validation risk;
- supply-chain dependency;
- price and business-model pressure;
- market-cycle or forecast uncertainty;
- search and evidence limitations.

Assign `High`, `Medium`, `Low`, or `Unresolved` signal strength with source IDs and rationale.

### Step 10 — Develop differentiated project options

Generate two to four options only when the evidence supports them.

Each option must include:

```text
option_id
decision_problem
target_user_or_customer
core_value
technical_route
differentiation
market_evidence
patent_evidence
engineering_evidence
regulatory_or_standards_evidence
strategic_fit
recommended_filing_authorities_and_rationale
FTO_follow_up
key_risks
validation_plan
go_no_go_gate
confidence
```

Recommended filing authorities must follow actual business, manufacturing, competitor, enforcement,
and budget considerations; do not derive them from an empty matrix cell alone.

### Step 11 — Generate the HTML report

Create one self-contained HTML file:

```text
{technology-field-slug}_market_patent_landscape.html
```

Use an English lowercase kebab-case slug.

## HTML report design

### Visual language

- white paper and neutral canvas;
- navy and slate hierarchy;
- restrained teal accent;
- system font stack;
- no gradients, glow, emoji-only icons, stars, or animated progress bars;
- text labels and evidence IDs;
- no remote fonts, scripts, chart libraries, or analytics;
- safe escaped data and allowlisted HTTP(S) links.

### Navigation and access

- semantic header, navigation, main, sections, and footer;
- responsive top or compact side navigation;
- visible keyboard focus;
- skip link;
- accessible tables and chart equivalents;
- horizontal overflow for wide matrices;
- print styles and repeated table headers;
- reduced-motion support;
- no color-only meaning.

### Required modules in order

#### Cover and executive summary

- title, scope, date, version, cutoff;
- three concise, evidence-qualified conclusions;
- score coverage and unavailable evidence.

#### Section 1 — Market overview

- market metrics with geography, segment, year, currency, and source IDs;
- comparable trend evidence;
- drivers, constraints, policy, standards, and customer needs;
- source-method differences.

#### Section 2 — Patent and technical landscape

- query and population definition;
- full-population metrics or unavailable states;
- theme table and state labels;
- representative patent evidence;
- publication-lag and family/count notes.

#### Section 3 — Technical activity and gap hypotheses

- Hot, Mature, Gap hypothesis, Declining, or Unresolved states;
- threshold and denominator;
- negative-search protocol;
- need and feasibility evidence;
- counterevidence and validation gates.

#### Section 4 — Jurisdictional filing footprint

- applicant-by-authority table;
- counts, units, query IDs, cutoffs, and completeness;
- PCT definition and metric state;
- bounded footprint observations;
- no color-only intensity.

#### Section 5 — Competitive landscape

- key-player validation register;
- comparative evidence or justified tiers;
- market, technical, patent, filing, and evidence dimensions;
- representative patents and limitations.

#### Section 6 — Opportunities and risks

- two-column structure when space permits;
- signal strength in text;
- source IDs, rationale, uncertainty, and owner/next action.

#### Section 7 — Project options

- two to four option cards;
- value, route, differentiation, evidence, authorities, risks, FTO follow-up, and gates;
- no patent-only recommendation.

#### Section 8 — Multi-dimensional screening

Assess:

- market evidence;
- technical feasibility;
- competitive intensity;
- policy/regulatory fit;
- IP position and diligence burden.

Show dimensions, weights, raw scores, evidence, missing-data treatment, and missing weight.
Do not use a radar chart unless the same data appear in an accessible table.
The score is a screening aid, not an investment verdict.

#### Section 9 — Sources, methods, and limitations

- patent source register;
- market/company/policy/standard source register;
- query versions and count semantics;
- cutoff and lag;
- exclusions and unavailable metrics;
- limitations and recommended diligence.

## Quality assurance rules

### QA-01 — Relevant-player coverage

All players in the validated key-player register are represented or have a documented exclusion reason.
No country-specific player is mandatory without evidence of relevance to the scoped market.

### QA-02 — Individual player validation

Every key player has a separately recorded entity-normalized search, even when no valid records are found.
A zero is reported only from a complete scoped search.

### QA-03 — Traceable sources

Every market figure, patent metric, representative patent, company fact, policy statement,
technical claim, and recommendation has a source ID.

### QA-04 — Compatible data definitions

Market figures disclose segment, geography, period, currency, basis, and methodology.
Incompatible sources are not averaged or spliced into a trend.

### QA-05 — Population and sample separation

Full-scope metrics and representative records are labelled distinctly everywhere.
No Top-K sample supports a population conclusion.

### QA-06 — Entity and omission review

Legal names, subsidiaries, aliases, acquisitions, and corporate-group scope are reconciled.
Every player and report module is checked before completion.

### QA-07 — Theme and gap completeness

Every theme has a definition, query/evidence basis, state, denominator or unavailable state,
overlap note, and validation need.

### QA-08 — Filing-footprint integrity

The authority matrix appears only with complete validated metrics or explicit unavailable cells.
It cannot be replaced by sample-derived counts or unqualified intent labels.

### QA-09 — Self-contained safe HTML

The report is UTF-8, offline, semantic, responsive, print-ready, keyboard usable, safely escaped,
free of remote dependencies, and does not rely on color alone.

## Search request patterns

Use the live Advanced Patent Search schema rather than assuming exact parameter names.

### Global field search concept

```json
{
  "query_id": "Q-GLOBAL-001",
  "concepts": ["primary technology term", "synonym", "mechanism term"],
  "classifications": ["validated IPC/CPC candidates"],
  "exclusions": ["known false-positive concept"],
  "date_window": {"field": "priority_date", "from": "YYYY-MM-DD", "to": "YYYY-MM-DD"},
  "family_rule": "simple family",
  "purpose": "population count and representative evidence"
}
```

### Key-player validation concept

```json
{
  "query_id": "Q-PLAYER-001",
  "technology_scope": "Q-GLOBAL-001",
  "assignee_aliases": ["legal name", "historic name", "validated subsidiary"],
  "corporate_group_cutoff": "YYYY-MM-DD",
  "purpose": "separate full-scope player validation"
}
```

### Authority-bucket concept

```json
{
  "query_id": "Q-PLAYER-AUTHORITY-001",
  "technology_scope": "Q-GLOBAL-001",
  "assignee_scope": "Q-PLAYER-001",
  "authority": "decision-relevant authority",
  "count_unit": "simple families or publications",
  "purpose": "complete reproducible authority bucket"
}
```

These are semantic request contracts, not claims about the connector’s exact live field names.

## Version capability history

The localized workflow preserves the source evolution:

- Version 1 introduced international company patent-layout analysis.
- Version 2 expanded to full project-initiation analysis, player validation, market evidence,
  competitive tiers, and project recommendations.
- Version 3 added technical activity/gap analysis, jurisdictional filing footprint,
  an expanded nine-section HTML report, and additional QA gates.

The localized edition removes the source’s fixed China-versus-overseas assumptions and sample-derived statistics
while preserving those analytical capabilities under global, reproducible evidence rules.

## Failure handling

If the field is too broad, narrow it before searching.
If market sources are incompatible, report separate values and the reason.
If a key player cannot be validated, retain it as Unresolved with the search evidence.
If full-population patent metrics are unavailable, omit the chart and show an unavailable panel.
If a theme overlaps another, disclose overlap and avoid additive shares.
If a negative search is incomplete, call the result a gap hypothesis, not white space.
If claim-level evidence is absent, do not call patent activity a barrier or FTO risk.
If fewer than two to four credible project options exist, return the valid subset.
If HTML validation fails, repair it before declaring completion.

## Final response

Summarize:

- normalized field and decision scope;
- strongest market signal and its source boundary;
- strongest patent/technical signal and metric state;
- leading player observation;
- most credible gap hypothesis and required validation;
- preferred project option and go/no-go gate;
- most important risk or unavailable evidence;
- report output path.
