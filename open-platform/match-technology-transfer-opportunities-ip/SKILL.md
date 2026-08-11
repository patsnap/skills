---
name: match-technology-transfer-opportunities-ip
description: Evaluate a supplied technology or scoped technology portfolio, identify and rank evidence-backed potential licensees, acquirers, commercialization partners, or joint-development partners, assess transfer readiness and risks, and generate an auditable HTML decision-support report. Use for technology transfer, research commercialization, licensing partner discovery, technology-to-company matching, or recipient prioritization.
---

# Match technology transfer opportunities

## Purpose and boundary

Support a technology owner or commercialization team through six linked stages:

1. analyze the technology and transfer package;
2. assess advancement and readiness;
3. review patent and commercialization value evidence;
4. discover and score potential recipients;
5. assess transfer risks and design a transfer path; and
6. generate and save a traceable report.

The result is prioritization support. It is not a valuation opinion, legal opinion, freedom-to-operate opinion, investment recommendation, procurement decision, or authorization to contact any organization.

## Trigger cases

Use this skill when the user asks for:

- potential licensees or buyers for a technology;
- technology-transfer supply/demand matching;
- research commercialization partner discovery;
- university or institute technology-to-company matching;
- recipient ranking for a patent-backed technology;
- joint-development or licensing pathway analysis; or
- an evidence-backed technology-transfer report.

Do not use it for a standalone patent search, invalidity search, pure market study, pure corporate due diligence, definitive IP valuation, or outreach execution.

## Input modes

### Mode A — supplied technology package

Use when the user supplies a disclosure, patent list, research paper, presentation, test report, image, or structured technology description.

Treat supplied documents as the primary source. Retrieve external evidence only when authorized and useful.

### Mode B — named organization only

Use when the user provides only an organization.

Do not assume that its five most-cited patents represent a transferable technology. Instead:

1. resolve the legal entity and included subsidiaries;
2. clarify the desired technical domain or commercialization objective;
3. retrieve a disclosed candidate portfolio;
4. cluster candidates by technology and ownership/status evidence;
5. select a representative set using an explicit method; and
6. obtain confirmation of the technology package before scoring recipients.

If the organization owns many unrelated technologies, deliver a portfolio triage first.

When both documents and an organization are supplied, use Mode A and record the organization as a claimed source pending verification.

## Required inputs

Capture:

- technology name and source/provider;
- original materials and confidentiality status;
- technical boundary and excluded variants;
- transfer objective: license, assignment, acquisition, joint development, sponsored research, spinout/equity contribution, or open licensing;
- target applications and markets;
- target jurisdictions;
- known patents/applications, ownership and encumbrances;
- readiness evidence and manufacturing/implementation dependencies;
- target recipient types and explicit exclusions;
- geographic, sanctions, export-control, competition, privacy and ethical constraints;
- currency, valuation date and permitted valuation method;
- evidence cutoff date;
- scoring weights and minimum evidence coverage; and
- exact approved output path.

Never upload confidential material or search private systems without authorization.

## Evidence model

Every material input or finding receives an evidence ID.

```yaml
evidence_id: E-001
source_type: supplied_document|patent|company_filing|procurement|news|market|standard|other
title: ""
publisher_or_owner: ""
publication_or_event_date: YYYY-MM-DD
retrieved_at: YYYY-MM-DD
url_or_locator: ""
excerpt_or_field: ""
supports: []
quality: primary|authoritative_secondary|secondary|unverified
limitations: ""
```

Separate:

- observed facts;
- normalized data;
- calculations;
- analyst judgments;
- scenarios; and
- unknowns.

Search snippets, generated summaries, citation counts, family size and company press releases are not self-validating.

## PatSnap connector map

### Advanced Patent Search — required for executed patent discovery

- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Key: `advanced_patent_search`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`

Use the live documented schema for assignee, nested, semantic, fielded, citation, patent-number, related-record and count tasks. Record connector, exact tool, request, filters, date, response semantics and limitations.

### Patent Briefing — required for selected records

- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Key: `patent_briefing`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`

Use it for bibliography, family, status, claims, description, translations and images. Preserve the as-of date and source-language boundary.

### Deep Patent Mining — recommended

- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-mining
- Key: `deep_patent_mining`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-mining`

Use evidence-backed technical topics, problems, effects, classifications, materials and applications to support—not replace—technical review.

### Patent Monetization & Valuation — optional

- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-monetize
- Key: `patent_monetization_valuation`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-monetize`

Treat any result as one bounded input. Record method, assumptions, date, currency, data coverage and uncertainty. Never present a connector score as a transaction price.

No verified global PatSnap procurement connector is claimed. Procurement, company, finance, market, news, standards and legal evidence require separately authorized current sources.

## Stage 1 — technology content analysis

### 1.1 Source and ownership register

Record:

- provider and legal entity;
- inventors/research team;
- document provenance;
- patent/application identifiers;
- ownership and assignment evidence;
- co-owners, funding obligations and university/employer rights;
- licences, options, pledges, grants or field restrictions;
- confidentiality/public-disclosure status; and
- unresolved title or authority questions.

Do not equate named applicant with current ownership.

### 1.2 Technical summary

Provide:

- one-sentence technical topic;
- concise mechanism and method;
- problem addressed;
- conventional alternatives and limitations;
- system boundary and dependencies;
- four or more supported innovation points when evidence permits; and
- three to five plausible application scenarios linked to requirements.

If the source is sparse, preserve unknowns rather than meeting a fixed word or item quota with invention.

### 1.3 Readiness assessment

Use TRL 1–9 only when appropriate to the discipline and supported by evidence. Record:

- readiness framework and version;
- claimed and independently supported level;
- validation environment;
- scale and sample count;
- reproducibility;
- safety/regulatory status;
- manufacturing or implementation readiness;
- supply-chain dependencies;
- integration requirements; and
- evidence gaps to reach the next level.

Do not convert “prototype,” “pilot,” or “field trial” mechanically into a TRL.

### 1.4 KPI register

For each KPI capture:

| Field | Requirement |
|---|---|
| Name | Unambiguous metric |
| Value/range | Exact reported value |
| Unit | SI or stated domain unit |
| Method | Test protocol and conditions |
| Sample | Size, batch and comparator |
| Source | Evidence ID and locator |
| Uncertainty | Error, variability or limitation |

Do not create a four-card KPI dashboard when fewer than four verified metrics exist.

### 1.5 Alternative comparison

Compare the technology with relevant alternatives across equivalent conditions. Include at least:

- mechanism/architecture;
- performance;
- cost evidence or status;
- scale/readiness;
- integration/compatibility;
- safety/regulatory burden;
- supply-chain constraints; and
- evidence date/source.

Use `not comparable` where test conditions differ materially. “Domestic substitution” is not a global comparison dimension; use supply security, regional availability and localization needs as relevant.

### 1.6 Transfer advantages and barriers

List evidence-backed:

- recipient benefits;
- integration fit;
- time-to-value;
- protected know-how or data;
- training/support package;
- validation assets;
- scale-up barriers;
- tacit-knowledge dependence;
- required inventor participation; and
- missing transfer package components.

## Stage 2 — advancement and readiness assessment

Retain the source’s eight-factor baseline only as a configurable rubric:

| Factor | Baseline weight |
|---|---:|
| Breakthrough in technical principle | 15 |
| Novelty of core method | 10 |
| Difficulty of substitution | 10 |
| Height of technical barriers | 10 |
| Process/system compatibility | 15 |
| Commercialization readiness | 15 |
| Technical stability/reproducibility | 10 |
| Scalability potential | 15 |

Before scoring:

1. confirm that the rubric fits the technology and transfer objective;
2. adjust weights if needed and record approval;
3. define anchors for 0, 25, 50, 75 and 100;
4. map evidence IDs to each factor;
5. identify missing evidence; and
6. record reviewer uncertainty.

For each factor output:

- raw score;
- weight;
- weighted contribution;
- evidence IDs;
- one- or two-sentence rationale;
- confidence;
- missing evidence; and
- sensitivity to a reasonable score range.

Suggested descriptive bands may be used only after disclosure:

- 0–39: early or insufficient evidence;
- 40–54: emerging;
- 55–69: differentiated;
- 70–84: strong evidence of advancement; and
- 85–100: exceptional under the declared rubric.

Do not call a technology “breakthrough” solely from the numerical band.

## Stage 3 — patent and commercialization value review

### 3.1 Portfolio definition

Record:

- search/entity scope;
- patent population count and counting unit;
- displayed subset and selection method;
- simple/extended family rule;
- applications versus grants;
- jurisdictions;
- status cutoff; and
- ownership uncertainty.

### 3.2 Technical value

Assess with evidence:

- claim/disclosure coverage of the transferable implementation;
- dependence on unprotected know-how;
- problem/means/effect relevance;
- blocking or complementary relationships;
- platform versus narrow-use potential;
- citation context, not count alone; and
- alternatives and design-around exposure.

### 3.3 Market value evidence

Assess:

- addressable use cases;
- recipient economics;
- market-size source and methodology;
- adoption barriers;
- regulatory timing;
- competitive substitutes;
- geographic family alignment; and
- credible commercialization evidence.

Never derive TAM from patent data alone.

### 3.4 Legal value evidence

Assess only with current records and qualified review where needed:

- status by family member and as-of date;
- remaining term assumptions;
- claim version and scope;
- prosecution/opposition/invalidation history;
- ownership and encumbrances;
- maintenance/annuity status;
- territorial fit; and
- known disputes.

Do not state “stable claims,” “valid patent,” or “no infringement risk” from database status alone.

### 3.5 Strategic value

Assess:

- fit with recipient portfolios and roadmaps;
- complementarity or gap filling;
- standards relevance supported by standards/claim mapping;
- licensing/assignment/joint-development feasibility;
- bundling options;
- know-how and data transfer; and
- field/geography/exclusivity choices.

Do not label a patent an SEP candidate merely because its topic relates to a standard.

### 3.6 Valuation boundary

Remove the source’s fixed RMB ranges and scarcity/family/SEP multipliers.

When valuation is authorized, state:

- valuation purpose;
- method: cost, market, income, relief-from-royalty, option/scenario, or triangulation;
- currency and valuation date;
- revenue/cost/royalty assumptions;
- probability and discount rates;
- tax, term and territory;
- comparable-transaction limitations;
- low/base/high scenarios; and
- sensitivity.

Otherwise output `valuation_status: not_assessed` and list required inputs.

### 3.7 Patent portfolio report modules

Preserve:

- portfolio statistics with counting rules;
- classification distribution with definitions;
- selected-patent analysis with safe global links;
- title, identifiers and dates;
- abstract/claim-bounded interpretation;
- classifications, status/as-of and evidence tags;
- citation count with database/date/context;
- filing chronology;
- PCT/foreign filing opportunities, subject to deadlines and counsel; and
- portfolio gaps and packaging recommendations.

Never force four IPC classes or a fixed patent count when evidence does not support them.

## Stage 4 — potential-recipient discovery

### 4.1 Define recipient types

Candidate types may include:

- operating companies with technical complementarity;
- suppliers or integrators;
- licensees in adjacent fields;
- joint-development partners;
- manufacturers or scale-up partners;
- distributors with technical capability;
- strategic acquirers;
- spinout investors, when requested; and
- public or nonprofit implementers.

Separate a company’s technical fit from willingness, authority, financial capacity and legal eligibility.

### 4.2 Candidate generation

Generate candidates from disclosed, auditable evidence such as:

- relevant patent activity;
- verified technical roadmaps;
- product and capability evidence;
- current investment, hiring or facility activity;
- collaboration or licensing statements;
- procurement opportunities;
- grants and funded projects;
- standards participation; and
- supplied relationship data.

Do not infer purchase intent from one news article or one patent.

### 4.3 Entity resolution and eligibility

For every candidate confirm:

- canonical legal name;
- parent/subsidiary relationship;
- operating region;
- relevant business unit;
- sanctions/export/control constraints where applicable;
- conflicts and excluded parties;
- current operational status; and
- evidence IDs.

### 4.4 Three evidence dimensions

Retain the source baseline as configurable:

- patent/technical evidence: 40 points;
- current public/company evidence: 30 points; and
- procurement/contract evidence: 30 points.

Procurement may be irrelevant in some sectors. In that case, redesign the rubric before scoring; do not silently redistribute missing points.

Use `scripts/match_scorer.py` for deterministic computation after evidence coding.

### 4.5 Patent/technical dimension

Candidate indicators include:

- classification/topic overlap;
- claim/disclosure semantic relevance;
- recent relevant activity;
- citation or family relationships interpreted in context;
- complementary capabilities;
- portfolio gap evidence; and
- development-stage alignment.

Fixed thresholds such as three IPCs, 0.75 semantic similarity, 20% growth, 50 citations or five countries are not universal. Define sector-, age-, database- and geography-adjusted anchors.

### 4.6 Public/company signal dimension

Candidate indicators include:

- explicit partnership or technology-acquisition intent;
- facility/product expansion;
- R&D program or laboratory investment;
- university/government/consortium activity;
- relevant hiring or capital allocation;
- conference/standards participation; and
- certification or regulatory progress.

Record event date, publication date, source quality and contradictory signals.

### 4.7 Procurement/contract dimension

Use only authorized, jurisdiction-appropriate sources. Candidate indicators include:

- relevant open or recent procurement;
- buyer/supplier role;
- technical requirement fit;
- budget and currency, normalized to the declared valuation date;
- award history;
- repeat/renewal behavior;
- procurement stage and deadline; and
- eligibility constraints.

The bundled `scripts/gov_bid_api.py` is a localized normalization adapter, not a configured global procurement API client. It must not send network requests or contain credentials.

### 4.8 Evidence coverage and missing data

For every metric record:

- normalized value;
- evidence IDs;
- source quality;
- as-of date;
- confidence;
- missing status; and
- normalization anchor/version.

Missing is not zero. The scorer returns:

- raw weighted score;
- available-weight score;
- evidence coverage;
- confidence/quality indicator;
- eligibility gate state; and
- sensitivity interval.

Do not rank candidates below the approved evidence-coverage floor as if comparable.

### 4.9 Recipient ranking and cards

Each recipient card includes:

- canonical company/entity name;
- recipient type and relevant business unit;
- total score and declared model version;
- dimension scores and coverage;
- evidence-quality label;
- eligibility status;
- at least three supported reasons when available;
- contradictory or missing evidence;
- one or two appropriate next validation actions; and
- source IDs.

Use text grades, not star icons. Treat score bands as prioritization labels, not objective probabilities.

### 4.10 Robustness checks

Before final ranking:

- vary top-level weights;
- vary key normalization anchors;
- test missing-data treatment;
- compare rank stability;
- inspect outliers;
- check entity duplicates;
- review source concentration; and
- conduct a human reasonableness review.

Show unstable rankings as tiers or ranges.

## Stage 5 — transfer risk and pathway

### 5.1 Four risk dimensions

Retain four 25-point baseline dimensions only after defining evidence anchors:

1. technical risk: readiness, reproducibility, key-person dependence, integration, scale-up and obsolescence;
2. market risk: demand, substitutes, adoption timing, pricing and policy/regulatory change;
3. legal/IP risk: title, scope, status, third-party rights, confidentiality, export/control and contract terms; and
4. partner risk: absorption capacity, financial/operational health, intent quality, governance and information asymmetry.

Risk score direction must be explicit: higher means greater risk.

### 5.2 Risk bands

If the user accepts the source baseline, use:

- 0–20: low;
- 21–40: moderate-low;
- 41–60: moderate-high;
- 61–80: high; and
- 81–100: critical.

These are rubric bands, not probabilities. Show each dimension’s evidence, uncertainty, owner, mitigation and decision gate.

### 5.3 Recipient-specific risk profiles

For the top three eligible recipients, provide unique profiles with:

- integration mismatch;
- licensing/ownership concern;
- organizational or financial constraint;
- geography/regulatory issue;
- evidence gap;
- mitigation action; and
- validation owner.

Do not duplicate generic concerns across all cards.

### 5.4 Transfer pathway

Build a gated timeline rather than a guaranteed schedule:

- near term, typically 0–6 months: evidence closure, ownership, package, outreach preparation, NDA and validation plan;
- medium term, typically 6–18 months: evaluation, pilot, diligence, negotiation and milestones; and
- longer term, typically beyond 18 months: scale-up, regulatory/quality work, commercialization, royalties/equity and post-transfer support.

Adapt timing to the sector.

Compare at least these routes when relevant:

- licence;
- assignment;
- joint development;
- sponsored research;
- spinout/equity contribution; and
- open/nonexclusive access.

For each route show control, exclusivity, funding, IP improvements, data/know-how, territory/field, milestones, termination, audit and support implications.

## Stage 6 — report generation and file service

Use `scripts/report_generator.py` to create the static report only after hard validation passes.

The report must contain:

- executive decision summary;
- scope, methods, evidence cutoff and data coverage;
- technology content and transfer package;
- readiness and KPI evidence;
- alternative comparison;
- advancement assessment;
- patent/commercialization value review;
- portfolio statistics and selected patents;
- recipient-discovery method and ranking;
- recipient cards and sensitivity;
- four-dimension risk review;
- individualized top-recipient risk profiles;
- pathway and route comparison;
- source register; and
- limitations and next validation actions.

The renderer must:

- escape all untrusted values;
- allow only safe HTTP(S) links;
- be self-contained and work without a CDN;
- use semantic English HTML;
- use accessible native SVG/tables instead of opaque external charts;
- expose data values in text;
- use color-independent labels;
- support keyboard, mobile and print; and
- never open a browser or server automatically.

Use `scripts/report_generator_patch.py` only to write to an exact user-approved path and optional user-approved backup path.

Do not:

- write to Desktop, home, session or temp by assumption;
- overwrite an existing file without explicit permission;
- start an HTTP server;
- announce a path that was not successfully written; or
- create files inside this skill package at runtime.

## Validation gate

Stop report generation if any hard check fails:

- technology identity/scope unresolved;
- provider or ownership assertion unsupported;
- confidential handling not approved;
- invented KPI, comparison, score, patent, market, company or procurement fact;
- recipient entity unresolved;
- prohibited recipient or compliance gate failed;
- score lacks evidence IDs;
- evidence coverage below the approved ranking floor;
- missing data treated as zero or silently renormalized;
- currency/date/unit absent from money values;
- unsafe URL or unescaped text;
- valuation presented without method and assumptions;
- legal/SEP/FTO conclusion presented without proper evidence/review; or
- output path not approved.

## Failure paths

### Patent connectors unavailable

Deliver a non-executed portfolio/search plan and required query/entity fields. Do not score patent evidence.

### Procurement source unavailable or irrelevant

Mark the dimension `not_scored`. Redesign/approve an alternative rubric if recipient ranking must continue.

### Sparse technology evidence

Deliver a transfer-package gap analysis and evidence-acquisition plan before recipient ranking.

### Ambiguous ownership

Pause commercialization conclusions and route title/authority review to qualified counsel or the technology-transfer office.

### Insufficient candidate evidence

Return an unranked candidate longlist with evidence gaps. Do not manufacture three reasons or an action.

### Valuation inputs missing

Set `not_assessed`. Provide a data request and scenario template.

### Unstable ranking

Use tiers/ranges, show weight sensitivity and identify decisive missing evidence.

### Renderer or output failure

Do not claim delivery. Return the exact error, preserve validated input, and retry only within the approved path.

## Quality checklist

- Both source input modes remain supported with a safe Mode B gate.
- All six source stages are present.
- All eight advancement factors are preserved as a configurable baseline.
- All four patent/commercialization value dimensions are present.
- All three recipient evidence dimensions and two-layer logic are represented.
- All four transfer-risk dimensions and top-three individualized profiles are present.
- The three time horizons and transfer routes are present.
- Every metric, score, recommendation and risk maps to evidence.
- Missing data and coverage are explicit.
- Patent, company, market, procurement and valuation semantics are separated.
- MCP names and links are verified global services only.
- No source credential, China-only provider assumption or regional domain remains.
- Report design is English, scientific, accessible, static and print-safe.
- Output writes occur only to user-approved paths.
