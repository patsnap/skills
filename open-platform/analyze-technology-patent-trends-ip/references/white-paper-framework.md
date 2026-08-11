# Competitive technology insight white-paper framework

Use this framework after patent retrieval, screening, and formal tagging. It is domain-neutral. The source package's complete dairy-protein mapping is retained in Appendix A as an optional interpretation aid, not as patent evidence or a default ontology.

## 1. Upstream workflow gate

Preferred suite chain:

1. `search-patents-ip`
   - Produces the retrieved pool and search manifest.
   - Preserves query, filters, applicant/entity provenance, date scope, counting level, and pagination.
2. `analyze-patent-search-results-ip`
   - Produces reproducible descriptive statistics.
   - Does not make the human screening decision.
3. Human Stage 3.5
   - Produces retained, excluded, and uncertain decisions with reasons.
4. `tag-patent-search-results-ip`
   - Produces formal tags, dictionary/version, confidence/review status, and tag manifest.
5. `analyze-technology-patent-trends-ip`
   - Consumes validated screened/tagged records.
   - Produces this evidence-bounded white paper.

Equivalent artifacts are acceptable when their semantics and provenance match.

Do not proceed as an executed white paper when:

- only competitor names are supplied;
- retrieval scope is unknown;
- search hits are unscreened;
- formal tags are absent;
- tag definitions are unavailable;
- counting/family rules are unknown; or
- dimensions cannot be reconciled to source records.

Deliver a data-readiness report instead.

## 2. Report identity

Generate:

- evidence-based business title;
- concise subtitle;
- intended audience;
- target decision;
- dataset and analysis scope;
- analysis basis;
- evidence cutoff;
- version date generated from the actual current date; and
- draft/review/release status.

Example title pattern:

> [Technology domain] patent competition, technology routes, and strategic opportunities

Avoid promotional terms such as “ultimate,” “breakthrough landscape,” or “complete global view” unless the evidence genuinely supports them.

## 3. Executive summary

Write five to eight findings only when the evidence supports that many.

Each finding contains:

| Field | Requirement |
|---|---|
| Finding | One decision-relevant observation |
| Data basis | Table/figure/calculation and denominator |
| Interpretation | What the observation may mean |
| Implication | Relevance to the target company/decision |
| Evidence strength | Strong, Moderate, Limited, or Insufficient |
| Limitation | Alternative explanation or missing evidence |

Do not introduce a summary conclusion that is absent from or inconsistent with the body.

## 4. Research method and boundary

### 4.1 Dataset provenance

Report:

- source artifact IDs;
- search query and filters;
- jurisdictions/databases;
- exact date field and range;
- screening method and status counts;
- tag dictionary and version;
- tag-assignment and review method;
- record count before and after screening;
- publication/application/family counting unit;
- family and deduplication rule;
- applicant/entity normalization;
- languages and translation policy;
- legal-status and citation source/as-of dates;
- missing-value rule;
- multi-label counting rule; and
- evidence cutoff.

### 4.2 Field-readiness table

| Dimension | Field(s) | Definition | Non-missing coverage | Validated coverage | Counting rule | Supported analysis | Unsupported inference | Enter body? |
|---|---|---|---:|---:|---|---|---|---|
| Technology type/taxonomy | | | | | | | | |
| Technical function | | | | | | | | |
| Method/process | | | | | | | | |
| Applicant/company | | | | | | | | |
| Time | | | | | | | | |
| Legal status | | | | | | | | |
| Family/citations | | | | | | | | |

Only logically closed dimensions enter deep analysis.

### 4.3 Evidence layers

Use explicit labels:

- **Patent observation:** directly calculated from the declared patent dataset.
- **Patent-text evidence:** selected abstract, claim, description, or verified enrichment.
- **Domain mapping:** externally sourced relationship used for interpretation.
- **Analyst interpretation:** bounded reasoning based on the first three layers.
- **Unknown:** insufficient evidence.

Never merge domain mapping into the patent result without labeling it.

### 4.4 Evidence-strength criteria

- **Strong:** direct/reproducible evidence, adequate validated coverage, stable under reasonable counting/tag choices.
- **Moderate:** consistent signal with a material but bounded coverage, semantic, time, or counting limitation.
- **Limited:** sparse, indirect, mapping-dependent, or highly sensitive evidence.
- **Insufficient:** cannot support a conclusion; report as a data need.

## 5. Domain interpretation mapping

The mapping section is reference-only. Build it from current authoritative domain sources.

Generic structure:

| Technology type/category | Common technical characteristic | Potential application/user | Potential value direction | Validation needed | Source |
|---|---|---|---|---|---|

| Technical function | Potential application/user | Potential product/market direction | Evidence needed | Boundary note | Source |
|---|---|---|---|---|---|

Mapping rules:

- use “domain mapping suggests”;
- cite source and access date;
- separate technical possibility from commercial demand;
- do not infer clinical effect, regulatory status, product launch, price, or adoption;
- do not use a mapping row as evidence of competitor intent; and
- omit mappings unrelated to the selected domain.

## 6. Chapter 1 — overall competitive landscape

Analyze only supported fields:

- portfolio scale by competitor under one count unit;
- taxonomy/type breadth and concentration;
- function breadth and concentration;
- process/method breadth and concentration;
- overall hotspots;
- shared and differentiated positions;
- legal/status distribution when semantics are adequate;
- family/citation context when available; and
- main competitive battlegrounds.

Outputs:

1. strategic overview;
2. scope and denominator note;
3. competitor-layout comparison table;
4. data findings;
5. strategic interpretation;
6. implication for the target company;
7. evidence strength; and
8. limitations.

Suggested table:

| Company/entity scope | Portfolio count/unit | Type breadth | Function breadth | Method breadth | Concentration | Recent activity | Status/family evidence | Interpretation | Strength |
|---|---:|---:|---:|---:|---:|---|---|---|---|

## 7. Chapter 2 — resource positioning by technology type

Answer:

- Which types have high tagged density?
- Which companies concentrate on specific types?
- Which are broad versus focused?
- Which positions remain stable under family/document counting?
- Which types are affected by tag coverage or ontology breadth?
- Which types have potential domain value that requires external validation?

Outputs:

- company × technology-type heatmap/table;
- company positioning table;
- concentration measure and method;
- key findings;
- strategic interpretation;
- implication;
- evidence strength; and
- limitation.

Suggested table:

| Technology type | Count | Share | Main companies | Company concentration | Trend status | Domain-mapping relevance | Patent-supported conclusion | Cannot judge | Strength |
|---|---:|---:|---|---:|---|---|---|---|---|

Use visible counts alongside any heatmap. A broad tag can create artificial density.

## 8. Chapter 3 — functional value layout

Answer:

- Which functions are common?
- Which functions are shared across companies?
- Which are concentrated in a small number of portfolios?
- Which appear differentiated under the tag definitions?
- Which interpretations come from domain mapping?
- Which functions need subtagging before action?

Outputs:

- function comparison table;
- hotspot/differentiation table;
- company-function distribution;
- findings and implications;
- evidence strength; and
- limitations.

Suggested table:

| Function | Count/share | Companies | Concentration | Relevant technology types | Time signal | Domain mapping | Patent-supported conclusion | Cannot judge | Strength |
|---|---:|---|---:|---|---|---|---|---|---|

Do not infer efficacy, productization, customer demand, safety, or regulation from function tags alone.

## 9. Chapter 4 — technology type × function matrix

This is the core chapter when both axes pass the gate.

Identify:

- high-density combinations;
- high-growth combinations when comparable time fields exist;
- competitor-leading combinations when entity fields exist;
- multi-company overlap;
- persistent versus one-period clusters;
- low-density combinations; and
- potential high-value interpretations from separately sourced mapping.

Core table:

| Technology type | Function | Count/unit | Main companies | Density | Recent trend | Crowding | Domain-mapped value direction | Patent-supported conclusion | Cannot judge | Strength | Strategic meaning |
|---|---|---:|---|---|---|---|---|---|---|---|---|

Rules:

- low density alone is not an opportunity;
- high density alone is not a moat;
- omit trend when time fields fail;
- omit company leadership when entity fields fail;
- disclose multi-label counting;
- show untagged records and denominator;
- test sensitivity to tag dictionary and family rule; and
- keep opportunity language conditional.

## 10. Chapter 4B — method/process route pattern

Include only when method/process labels pass the gate.

Analyze:

- most frequent routes;
- company concentration by route;
- associated types/functions;
- route combinations;
- time persistence;
- tag coverage and ambiguity; and
- repeated pattern versus isolated use.

Core table:

| Method/process label | Main companies | Associated types | Associated functions | Count/unit | Coverage | Data-supported conclusion | Cannot judge | Strength | Strategic meaning |
|---|---|---|---|---:|---:|---|---|---|---|

Do not equate a route label with complete manufacturing capability, throughput, yield, economics, scale, ownership, or process-platform leadership.

## 11. Chapter 5 — competitor strategic profiles

Use only supported labels:

- type-concentrated;
- function-concentrated;
- combination leader within the dataset;
- broad-coverage portfolio;
- emerging-direction accelerator; and
- existing-portfolio defender.

For each company include:

- exact entity scope;
- count and unit;
- core types/functions/methods;
- leading combinations;
- breadth and concentration;
- time signal if supported;
- possible strategic interpretation;
- implication for the target company;
- evidence strength; and
- data boundary.

Profile table:

| Company/entity scope | Positioning label | Core types | Core functions | Core methods | Leading combinations | Breadth/concentration | Time signal | Possible intent | Implication | Strength | Boundary |
|---|---|---|---|---|---|---|---|---|---|---|---|

Do not assign product, formulation, customer-segment, clinical, market, or manufacturing leadership without corresponding evidence.

## 12. Chapter 6 — potential barriers and opportunity windows

### Barrier ladder

With type/function tags only, discuss:

- density;
- concentration;
- overlap;
- crowding;
- persistence; and
- evidence to validate.

With method labels, add potential route concentration.

With claims, grants/status, family, citations, continuity and technical depth, formulate stronger but still provisional barrier hypotheses.

Barrier table:

| Type | Function/method | Leading company | Existing evidence | Missing evidence | Current bounded judgment | Risk to target | Validation action | Strength |
|---|---|---|---|---|---|---|---|---|

### Opportunity gate

Require more than sparse counts:

- verified problem or need;
- plausible technical route;
- relevant target-company capability;
- stable low/medium crowding signal;
- external value evidence;
- no obvious blocking-right conclusion; and
- specific validation plan.

Opportunity table:

| Type | Function/method | Current layout | Domain-mapped value | Possible target-company opportunity | Missing evidence | Validation action | Priority | Strength |
|---|---|---|---|---|---|---|---|---|

## 13. Chapter 7 — future focus assessment

Include only with a valid date field, adequate history, comparable periods and publication-delay caveat.

Use:

- recent application growth;
- newly appearing types/functions/methods;
- combination growth;
- multi-company acceleration;
- sustained single-company concentration;
- persistence across family/counting choices; and
- small-denominator warnings.

Future-focus table:

| Signal | Date field/window | Count/baseline | Companies | Judgment basis | Domain mapping | Strength | Limitation | Monitor next |
|---|---|---:|---|---|---|---|---|---|

Never treat an incomplete current year as a full period.

## 14. Chapter 8 — R&D and patent-layout recommendations

Classify recommendations:

- A. Data-supported;
- B. Domain-mapping-inspired; and
- C. Additional data required.

Recommendation table:

| Type | Direction | Technology type | Function/method | Competitor status | Opportunity/risk | Action | Priority | Strength | Evidence IDs | Validate next |
|---|---|---|---|---|---|---|---|---|---|---|

Actions may include:

- query refinement;
- rapid prior-art review;
- R&D pre-research;
- FTO review;
- additional application/product/method/evidence tagging;
- deeper route tagging;
- competitor claim/status/family analysis;
- monitoring;
- standards mapping; and
- validation against product pipeline, technical tests, regulation and market data.

Do not recommend filing merely because a cell is sparse.

## 15. Closing

Write a concise close that:

- restates the core analytical lens;
- distinguishes data findings from mappings;
- identifies the most decision-relevant uncertainty;
- links the next action to evidence closure; and
- avoids slogans.

## 16. Reusable drafting prompt

```text
Create a management-grade competitive technology insight white paper from the supplied screened and tagged patent dataset.

Before analysis:
1. verify dataset provenance, screening state, tag dictionary/version, count/family rules, entity normalization, date field, missingness, and dimension coverage;
2. build a field-readiness gate;
3. omit unsupported deep-analysis chapters;
4. separate patent observations, patent-text evidence, domain mapping, analyst interpretation, and unknowns; and
5. label every finding Strong, Moderate, Limited, or Insufficient under the declared criteria.

Use technology type/taxonomy × technical function as the core matrix when supported. Add method/process only when its tag field and coverage pass the gate. For each chapter provide the data finding, strategic interpretation, implication for the target company, evidence strength, and limitation.

Do not equate patent counts with quality, barriers, market position, technical performance, enforceability, or FTO. Do not treat missing values as zero. Disclose denominators, multi-label counting, family rules, partial periods, and publication delay. Recommendations must be classified A (data-supported), B (domain-mapping-inspired), or C (additional data required).
```

## 17. Output requirements

- US English unless requested otherwise.
- Markdown draft or self-contained HTML per the request.
- Formal titles and concise table names.
- Raw patent details only where needed for evidence.
- Unsupported dimensions remain in methods/data needs.
- Findings are traceable and reproducible.
- Dates are exact and current, never fixed in the template.

---

# Appendix A — dairy-protein domain mapping retained from the source

This appendix preserves the source domain material. It is an optional industry/domain mapping reference. It is not patent evidence, clinical advice, a product claim, or a regulatory conclusion. Validate terminology, evidence, dose, population, jurisdiction and current regulatory status before use.

## A1. Protein type to potential value direction

| Protein type | Common technical/nutritional characteristic | Potential population/application | Potential high-value direction | Validation points |
|---|---|---|---|---|
| Casein, caseinate, micellar casein | Structure, gelation, emulsification, sustained release, calcium binding | Children, older adults, general nutrition | Cheese, yogurt, high-protein foods, bone-health nutrition | Product scenario, formulation role, process, performance and evidence |
| Whey protein, WPC, WPI, WPH | Nutritional value, digestibility, amino-acid profile, muscle-protein-synthesis relevance | Sports, adult and older-adult nutrition | Protein beverages, powders, sports nutrition, older-adult nutrition | Population, product fields, composition, dose and evidence |
| Lactoferrin | Iron-binding glycoprotein; immune and antibacterial research relevance | Infant, child and immune-health research/product contexts | Infant formula, immune nutrition, high-value functional dairy | Evidence level, dose, safety, regulation and product scenario |
| Alpha-lactalbumin | Amino-acid balance and infant-nutrition relevance | Infant/child nutrition and adjacent research contexts | Infant formula and premium nutrition | Product scenario, composition, dose and evidence |
| Beta-lactoglobulin | Major whey protein; structure/function modification and allergen relevance | General nutrition and lower-allergen research contexts | Functional ingredients and allergen-control formulations | Hydrolysis, allergen evidence, safety and regulation |
| Casein phosphopeptide (CPP) | Mineral binding and calcium-absorption research relevance | Child and older-adult bone-health contexts | Calcium-absorption and bone-health products | Evidence, dose, formulation and regulation |
| Milk-derived bioactive peptides | Potential antihypertensive, antioxidant, immune and metabolic research functions | Adult, older-adult and functional-food research contexts | Functional foods and medical-nutrition-adjacent research | Sequence, mechanism, human evidence, dose, safety and regulation |
| Hydrolyzed or modified milk protein | Digestibility, allergen reduction, solubility and stability | Infant, sensitive-digestion and special-nutrition contexts | Hydrolyzed formulas, medical nutrition and high-protein beverages | Process, degree of hydrolysis, clinical evidence, safety and regulation |

## A2. Protein function to potential scenario mapping

| Protein function | Potential population/application | Potential product/market direction | Evidence to validate | Boundary note |
|---|---|---|---|---|
| Nutrition enhancement | Children, adults, older adults and sports users | High-protein dairy, powder and supplements | Product, composition, dose and formulation | Broad function; requires scenario validation |
| Immune modulation | Infant, child and immune-health research contexts | Lactoferrin products, immune nutrition and infant formula | Experimental, clinical, safety and product evidence | Do not infer clinical efficacy from a tag |
| Digestibility or hypoallergenicity | Infant and sensitive-digestion contexts | Hydrolyzed formulas and hypoallergenic nutrition | Hydrolysis, process, clinical and safety evidence | Requires source and regulatory validation |
| Muscle synthesis or recovery | Sports and older-adult nutrition | Sports and muscle-health nutrition | Composition, dose, target-population and clinical evidence | Industry mapping unless directly tagged and evidenced |
| Bone health or calcium absorption | Child and older-adult contexts | CPP/calcium and bone-health nutrition | Mechanism, dose, formulation and human evidence | Requires evidence beyond the function tag |
| Gut health | Child, adult and older-adult contexts | Fermented dairy and protein-prebiotic combinations | Microbiome, product, dose and clinical evidence | Avoid overclaiming |
| Antioxidant or anti-inflammatory | Adult and older-adult functional-food research | Functional foods and healthy-aging research | Experimental and human evidence | Concept-only claims are Limited |
| Antihypertensive or metabolic regulation | Adult/older-adult chronic-disease research contexts | Functional foods and medical-nutrition-adjacent research | Peptide, dose, mechanism, clinical and regulatory evidence | Requires strong validation |
| Texture, stability, emulsification or gelation | Formulation and manufacturing applications | Yogurt, cheese, protein beverages and shelf-life improvement | Process, formulation, performance and product evidence | Technical function, not health efficacy |

## A3. Dairy-specific matrix fields

When the supplied tag dictionary uses the source dairy fields, map them explicitly:

- the source protein-type field → `protein_type`;
- the source protein-function field → `protein_function`; and
- the source separation-method field → `separation_method`.

Do not assume these literal field names exist in a global English dataset. Record the source-to-localized field mapping in methods.

## A4. Separation-route interpretation

Potential labels in the source include:

- chromatography;
- ion exchange;
- membrane separation;
- ultrafiltration;
- reverse osmosis;
- isoelectric or electrochemical routes;
- hydrolysis routes; and
- other formally defined separation methods.

Analyze route concentration only when coverage and repeated company-level evidence support it. A few tagged patents are a signal requiring validation, not proof of a process platform.

## A5. Dairy-specific closing boundary

Use protein type × protein function to identify patent competition patterns. Link patent tagging with product, process, composition, dose, efficacy/safety evidence, regulation and market data before making commercial, health or product decisions.
