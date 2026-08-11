# Deep 21-Section Target and Drug BD Report Specification

Use this reference only when the user requests a deep HTML presentation. The standard skill output may be shorter. Preserve the source's complete 21-section information architecture, but include a section only when it is relevant and evidence-supported; mark an omitted or unavailable section with reason and decision impact.

## Scope

This specification applies to oncology and non-oncology targets, target classes, targeted assets, or modality–target opportunities. It is not tied to B7-H3, a predefined set of cancer targets, China-only analysis, or fixed example counts.

## Retrieval and evidence workflow

### Stage 0 — Entity normalization

- normalize gene/protein/complex/isoform/species and aliases;
- distinguish target, ligand, receptor, pathway node, biomarker and asset;
- normalize disease/indication and company/legal entity;
- retain provider IDs and source/date;
- expose unresolved ambiguity before downstream queries.

### Stage 1 — Target and disease foundation

Use supplied evidence or verified `target_disease` capabilities. Capture target identity, structure/domain/localization, pathway/mechanism, normal and disease expression, human genetics, perturbation evidence, safety liabilities, tractability, disease linkage, epidemiology and evidence gaps.

Do not require five protein domains or other arbitrary minimums. Do not treat database `drug_count` or `disease_count` as biological validation.

### Stage 2 — Drug and asset pipeline

Use verified `drug_asset` tools. Query target/aliases, disease, organization, modality/type, phase/status and milestone as available. Page every query until the reported total is retrieved or the gap is disclosed.

Do not assume fixed provider type strings such as “Small molecule drug,” “Monoclonal antibody,” or a combined “Biological product/ADC” are accepted; use the actual tool schema. Create modality buckets after retrieval from source-backed asset attributes.

Run distinct views as needed:

- small molecule;
- conventional antibody;
- ADC/conjugate;
- bispecific/multispecific;
- cell/gene/RNA or other modality;
- approved assets by region/indication;
- target geography/market;
- active, discontinued, terminated and unknown programs.

Reconcile overlap across views at asset and indication levels.

### Stage 3 — Clinical trials and results

Use verified `clinical_trials` tools:

- `clinical_trial_search`;
- `clinical_trial_fetch`;
- `clinical_trial_result_search`;
- `clinical_trial_result_fetch`.

Search all relevant phases/statuses/geographies; do not prescribe “all Phase 3 plus a Phase 2 sample” as universal coverage. Fetch key trial details and independently identify reported-result records. Preserve registry/source ID, trial version/update date, result source/cutoff, and zero/no-result distinctions.

### Stage 4 — Patent landscape

Use `advanced_patent_search` for discovery and `patent_briefing` for claims/family/status/description/translation. Search target, modality, asset, sequence/structure, platform, epitope, payload/linker, formulation, manufacturing, use, regimen, biomarker, applicants, inventors, families and continuations as applicable.

Do not call a product/compound filter unless the current tool schema supports it. A representative top-N sample must be labeled as a sample. Claim-level FTO requires a separate jurisdiction-specific workflow, current claims/status and counsel.

### Stage 5 — Transactions and ecosystem

Use a company/deal MCP only when its current callable tools are verified. Otherwise use supplied exports, company/regulatory filings and original announcements. Page complete searches where possible.

Capture parties/roles, asset, target/modality, indication, rights, territory, dates, options, disclosed upfront/equity/milestones/royalties and original source. Do not equate headline potential value with paid value.

### Stage 6 — Scientific, translational and regulatory evidence

Use `scientific_translational_evidence`, `regulatory_guidelines`, primary papers, regulatory documents and official trial sources as appropriate. Current global scientific/translational MCP tools support translational records; do not claim generic paper tools unless actually available.

Retrieve foundational, current, conflicting and negative evidence. Record study/model/population, endpoint, sample, date and limitations.

### Stage 7 — Supplemental primary-source research

Use official registries, regulators, patent offices, peer-reviewed publishers, company filings and original announcements to fill material gaps. Label the exact source, event/publication/retrieval date and verification state. Web evidence is not automatically “unverified”; assess source authority. Conversely, a search snippet is not verified evidence.

## Pagination and coverage contract

For each source/module record:

```json
{
  "module": "drug_pipeline",
  "query_id": "Q-DRUG-01",
  "filters": {},
  "reported_total": 120,
  "retrieved_total": 120,
  "deduplicated_total": 87,
  "analyzed_total": 87,
  "excluded_total": 0,
  "pages_or_batches": 6,
  "cutoff": "YYYY-MM-DD",
  "status": "complete|partial|failed|unavailable",
  "known_gaps": []
}
```

If `reported_total > retrieved_total`, continue pagination under the actual tool schema. If the source caps results or pagination fails, stop claiming completeness and show the gap.

## Source notation

Every factual field must link to a source register, not a verbose tool-name string in every sentence.

```text
[DRUG-014] [TRIAL-006] [PAT-021] [PAPER-008] [DEAL-003]
```

The register contains source type, stable ID/URL, tool/query, field, value/unit, event date, retrieved date and verification status.

## The 21 sections

### Section 0 — Executive summary and KPI overview

Include:

- decision question and recommendation: GO / conditional GO / pause / NO-GO / insufficient evidence;
- confidence and decisive assumptions;
- three to six key findings;
- measurable go/no-go conditions;
- top risks/opportunities and immediate actions;
- up to eight useful KPIs only when their units, denominators, dates and sources are clear.

Possible KPIs: active assets, approved assets in scoped regions, active pivotal trials, relevant patent families, verified deals, evidence grade, target population, or differentiation benchmark. Do not force eight cards or replace missing values with zero.

### Section 1 — Target biology

- normalized identity and aliases;
- protein/domain/complex/localization;
- expression by normal/disease tissue and cell type;
- pathway and mechanism;
- genetic and functional causal evidence;
- target dependence/heterogeneity;
- safety and on-target/off-tumor risk;
- resistance/escape;
- tractability and modality constraints;
- evidence grade and gaps.

### Section 2 — Disease context and standard of care

- scoped disease/subtype/stage/line/biomarker;
- disease biology and target relationship;
- current guideline/label-supported treatment pathway by country/date;
- efficacy/safety/access limitations;
- patient-selection and diagnostic pathway;
- unmet need under defined comparator;
- development positioning.

### Section 3 — Epidemiology and market context

- incidence, prevalence, mortality and survival;
- geography/year/population and source methodology;
- biomarker prevalence and testing rate;
- addressable patient funnel;
- current/partial-year and forecast distinction;
- market estimate only with method, currency, year, scenario and uncertainty.

Do not require GLOBOCAN when the disease/source is inappropriate. Use authoritative disease-specific sources.

### Section 4 — Competitive pipeline landscape

- asset counts under explicit deduplication;
- modality, mechanism, target form/site and indication;
- development phase/status/date;
- sponsors/originators/partners;
- attrition/discontinuation;
- timing and concentration;
- differentiation clusters and gaps;
- coverage summary.

### Section 5 — Competitor deep profiles

Select material assets using explicit criteria, not a fixed Top 5. Each profile includes identity/rights, modality/MoA, indication, development status, key trials/results, safety, biomarker, manufacturing/product attributes, IP/transactions, differentiation and evidence gaps.

### Section 6 — Development pipeline detail

Provide source-backed asset tables by meaningful modality/route. Distinguish:

- global versus indication-specific phase;
- active versus discontinued/unknown;
- monotherapy versus combination;
- approved region/label;
- originator versus current developer;
- duplicate aliases/formulations.

### Section 7 — Clinical trial progress

- complete scoped trial table or disclosed sample;
- registry ID, phase, design, arms, population, biomarker;
- dose/route/schedule;
- endpoints, enrollment, geography;
- recruitment/status and source update date;
- reported result linkage;
- pivotal/readout/decision milestones;
- trial-level gaps.

### Section 8 — Patent landscape and IP questions

- reproducible search scope/query/date/languages/jurisdictions;
- publication/family counting rules;
- claim themes and material families/members;
- applicants/assignees/continuity/geography/status;
- target, modality, epitope/sequence/structure/platform/use/formulation/manufacturing/regimen dimensions;
- sampling and blind spots;
- FTO, patentability, validity, ownership/license and monitoring questions for counsel.

Do not use red/amber/green FTO labels based solely on database hits.

### Section 9 — BD transactions and partnering signals

- complete retrieved set or sampling statement;
- parties/roles, asset/target, modality, indication, rights/territory;
- transaction and effective dates;
- transaction type;
- upfront/equity/milestone/royalty/headline values separated;
- disclosed/undisclosed fields;
- strategic pattern and rights availability;
- original sources and limitations.

### Section 10 — Scientific evidence and research activity

- query/scope and observed publication/translational counts;
- foundational and recent primary studies;
- evidence types and quality;
- mechanistic, translational, biomarker and resistance findings;
- conflicting/null evidence;
- model-to-human limitations;
- research activity as context, not validation by volume.

### Section 11 — Regulatory path

- applicable agencies/countries;
- approved precedent and label/decision date;
- endpoint/comparator/diagnostic expectations;
- orphan/fast-track/breakthrough/accelerated/conditional routes only with eligibility caveat;
- post-marketing/confirmatory risks;
- modality-specific regulatory issues;
- next authority interaction/evidence.

Do not present FDA, EMA, NMPA or other pathways as interchangeable.

### Section 12 — Health economics and access

- comparator price/cost with country/year/gross-net caveat;
- duration, administration and monitoring burden;
- biomarker/diagnostic cost and access;
- payer/value drivers;
- target-product-profile outcomes;
- scenario-based revenue/market assumptions where requested;
- data gaps and sensitivity.

### Section 13 — Priority geography / regional analysis

Replace the source's mandatory “China section” with the geography selected by the user. Include local epidemiology, care, pipeline, trials, regulator, reimbursement/access, companies, patent status/territory, manufacturing and partnering conditions. Include China only when in scope.

### Section 14 — Development cost, timeline and ROI framework

- stage/timeline/cost assumptions and source ranges;
- probability of technical/regulatory success by scenario;
- cash flow, discount rate, launch, price, population and penetration assumptions;
- NPV/ROI or decision-tree sensitivity;
- downside/upside and break-even conditions;
- explicit statement that this is a planning framework, not valuation advice.

### Section 15 — CMC and manufacturability

- modality-specific process and analytical control;
- raw materials/supply chain;
- expression/synthesis, purification, conjugation/assembly;
- potency, identity, purity, stability and comparability;
- formulation/presentation/device;
- scale, yield, cost and tech transfer;
- risks, experiments and mitigation owners.

### Section 16 — SWOT

Use an evidence-linked 2×2 table only if useful. Every item has source/assumption, confidence and implication. Avoid duplicating the executive summary or treating an inference as fact.

### Section 17 — Initiation and partnering recommendation

- recommendation and confidence;
- target product profile/differentiation thesis;
- modality and indication choice;
- build/buy/partner/licensing options;
- partner/asset shortlist criteria;
- measurable go/no-go conditions;
- experiments/search/diligence plan;
- owner/timing/decision date;
- sensitivity to key assumptions.

Do not require P1/P2/P3 or five-star scores. If a matrix is used, define dimensions, weights, missing-data behavior and sensitivity.

### Section 18 — Risk register

Include relevant categories, not a fixed seven:

- biology/translatability;
- safety;
- biomarker/diagnostic;
- clinical/regulatory;
- CMC/supply;
- patent/FTO/ownership;
- competitive/timing;
- commercial/access;
- partner/rights;
- data quality/coverage;
- financial/organizational.

For each: risk statement, evidence, trigger, likelihood definition, impact definition, mitigation, residual risk, owner and review date.

### Section 19 — Data coverage summary

Required. Show one row per module:

| Module | Query/filter | Reported | Retrieved | Deduped | Analyzed | Coverage status | Cutoff | Blind spots |
|---|---|---:|---:|---:|---:|---|---|---|

Explain cross-module overlap and counting units. Do not include fixed example counts or labels such as “E42/E50.”

### Section 20 — Sources

- complete source register;
- primary versus secondary/database-derived evidence;
- stable identifier/URL;
- event/publication/retrieval date;
- tool/query/filter;
- fields/findings supported;
- verification status;
- inaccessible/temporary source caveat.

### Section 21 — Limitations and non-reliance

State:

- decision scope, target/asset version, jurisdictions and cutoff;
- database/search/publication/translation limits;
- dynamic pipeline/trial/status/deal/guideline data;
- unpublished/non-indexed evidence;
- no medical, legal, FTO, valuation or investment advice;
- specialist review and monitoring required;
- confidential-information handling.

## Scientific HTML design

Use a self-contained, accessible, responsive, printable HTML file.

### Visual variables

```css
:root {
  --canvas: #f6f8fa;
  --surface: #ffffff;
  --surface-alt: #edf3f5;
  --ink: #17212b;
  --muted: #596674;
  --line: #d5dde3;
  --accent: #245f73;
  --accent-soft: #e4f0f2;
  --caution: #8a5b1d;
  --caution-soft: #fbf1df;
  --risk: #983d36;
  --risk-soft: #f8e9e7;
  --positive: #3b6d52;
  --positive-soft: #e5f1e9;
  --hypothesis: #625989;
  --hypothesis-soft: #eeeaf7;
}
```

### Components

- concise report header with version/cutoff/release status;
- sticky section navigation on desktop, accessible menu on mobile;
- KPI cards with unit/denominator/as-of/source and missing-data state;
- evidence cards for assets/competitors;
- claim/IP question cards that avoid legal risk colors as conclusions;
- SWOT and priority matrices with text labels;
- callouts for finding, caution, risk question, hypothesis and recommendation;
- coverage table in readable monospace/numeric format;
- source chips linking exact returned/primary URLs;
- native SVG/CSS charts plus accessible data tables;
- print footer with report metadata.

Use system fonts. No external CDN, web font, image, chart library or analytics. Avoid gradients, landing-page hero, glow, decorative animation, product UI imitation and emoji-only status.

### Layout and accessibility

- maximum width around 1200–1280 px;
- one `<h1>` and logical headings;
- skip link/landmarks;
- table captions and scoped headers;
- visible focus and keyboard controls;
- status communicated by text plus optional color;
- responsive cards/tables below 768 px;
- reduced-motion support;
- charts with alt text/data table;
- interactive content usable without hover and preferably without JavaScript.

### Print

- A4/Letter-safe margins;
- repeat table headers;
- avoid orphan headings and split cards/tables where possible;
- hide navigation/controls;
- show stable source URLs/IDs;
- do not print signed/private query URLs.

## Output naming

Use a filesystem-safe English slug and version/date:

```text
<target-or-asset-slug>_target_bd_assessment_v1.0.0.html
```

Increment semver or append the cutoff date for reruns. Do not overwrite prior versions. Do not assume a session-specific output path; use the user's workspace/approved output location.

## Validation gates

- [ ] Target/entity identity and scope are explicit.
- [ ] Every endpoint with total > returned is paginated or caveated.
- [ ] Counts reconcile after asset/trial/patent/deal deduplication.
- [ ] Approval/phase/status/results show geography/date/source.
- [ ] Trial IDs and outcomes come from primary/verified records.
- [ ] Patent sample/coverage/counting/FTO boundary is explicit.
- [ ] Deal roles/rights/economics are correctly separated.
- [ ] Regional section reflects user scope, not a fixed country.
- [ ] Cost/market/ROI assumptions have units/sensitivity.
- [ ] All 21 sections are populated, marked not applicable, or omitted with reason.
- [ ] HTML parses, links/anchors work, and no external dependency/credential exists.
- [ ] Desktop/mobile/keyboard/print checks ran or are accurately caveated.
- [ ] Data coverage summary and source register are complete.
