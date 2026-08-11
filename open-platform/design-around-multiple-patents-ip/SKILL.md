---
name: design-around-multiple-patents-ip
description: Develop and screen engineering design-around concepts against two or more potentially relevant patent rights using an application-driven eight-step FTO workflow. Use when users request multi-patent design-around work, freedom-to-operate screening, patent risk mapping, candidate design-space analysis, claim-by-concept cross-screening, iterative risk repair, or an attorney-review package with technical validation plans.
---

# Design Around Multiple Patents

## Operating boundary

Use this skill to develop engineering alternatives and organize an evidence-backed, multi-patent FTO pre-screen. Do not present the result as a legal opinion or as proof that a product is free to operate.

Act as an IP and engineering analysis assistant. Do not impersonate counsel. Distinguish:

- search results from the complete set of potentially relevant rights;
- an application from a granted or enforceable claim;
- a patent family from a single jurisdictional right;
- literal limitation mapping from jurisdiction-specific equivalents analysis;
- a technical difference from a legally material difference;
- a candidate concept from a manufactured product or process;
- a screening state from an infringement conclusion; and
- engineering feasibility from legal clearance.

Require qualified counsel in each relevant jurisdiction to confirm claim construction, current claims, status, enforceability, equivalents, prosecution-history effects, and a formal FTO opinion.

## Source workflow preserved

Execute all eight source steps in order:

1. define application requirements;
2. inventory the full risk set;
3. deepen review of priority patents;
4. identify parameter-level candidate design space;
5. design candidate formulations or solutions;
6. cross-screen every candidate against every material claim;
7. repair identified risks and repeat the screen; and
8. prepare an FTO review framework and experimental validation plan.

The source names three unavailable helper skills. The frozen source corpus contains no `application-requirements-card` or `patent-claim-to-funcmodel` package. A separate source package named `patent-avoidance-design` is scheduled to become `develop-patent-design-arounds-ip`, but it is not a prerequisite here. Use the complete schemas below so this skill remains self-contained. If the localized single-patent skill is available later, use it optionally for Step 3 and preserve the same handoff schemas.

## Multi-patent versus single-patent analysis

| Dimension | Single-patent design-around | Multi-patent design-around |
|---|---|---|
| Primary driver | Deep analysis of one selected claim set | Application requirements plus the combined constraint set |
| Objective | Create alternatives that avoid at least one required limitation of selected claims | Identify feasible concepts with favorable mappings across every material current claim |
| Analysis shape | Claim decomposition and focused alternative generation | Portfolio inventory, normalization, trade-space analysis, cross-screening, and iteration |
| Core output | Claim-specific design concepts | Requirements record, evidence matrix, design-space map, candidate set, and cross-screen matrix |
| Typical use | One known blocking right | Several rights, families, owners, or claim types in a target market |

Do not model the task as a simple mathematical complement of independent parameter intervals. Patent claims are conjunctions of construed limitations, and legal exposure depends on jurisdiction, claim version, acts, status, facts, and applicable law.

## Inputs

Collect or derive:

| Field | Required | Content |
|---|---:|---|
| Target product/process | Yes | Exact version, architecture, formulation, steps, suppliers, and variants |
| Intended acts | Yes | Make, use, sell, offer, import, export, supply, or other relevant acts |
| Jurisdictions | Yes | Markets, manufacturing sites, transit, and supply-chain locations |
| Decision date | Yes | Launch, investment, design-freeze, or transaction date |
| Technical requirements | Yes | Performance, safety, cost, regulatory, process, and integration constraints |
| Candidate patents | Yes to start | User list and/or authorized search results |
| Product evidence | Recommended | Specifications, drawings, recipes, bills of materials, process flows, test data |
| Patent evidence | Recommended | Current claims, family, status, term, prosecution history, translations |
| Risk tolerance | Recommended | Business-defined escalation and evidence thresholds |
| Confidentiality constraints | Recommended | Handling and redaction requirements |

If product information is incomplete, identify the missing facts and limit the analysis rather than assuming a favorable design.

## Evidence and version controls

Freeze the following for every run:

- report cutoff date;
- product/process version;
- candidate concept version;
- jurisdiction and intended act;
- patent publication and application numbers;
- family identifier and relationship;
- claim number and claim text version;
- legal-status source and as-of date;
- prosecution-history source and date;
- source-language text and translation provenance;
- search connector, tool, query, filter, and date; and
- unit, measurement basis, test method, uncertainty, and conversion method.

Never fabricate a claim, status, family relationship, prosecution statement, product value, test result, or source locator.

## Verified PatSnap MCP services

Confirm the live tool schema at runtime; do not invent tool names or parameters.

### Patsnap Patent Research — required for an authorized live FTO screen

- Connector key: `patsnap_patent_research`
- Marketplace: <https://open.patsnap.com/marketplace/mcp-servers/patsnap-ip-searching>
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patsnap-ip-searching`
- Relevant documented tools: `fto_review` and `get_task`

Use `fto_review` for an invention FTO task when the user authorizes an external search. Poll asynchronous results with `get_task`. Treat the returned candidate pool and analysis as evidence requiring verification, not as automatic legal clearance.

### Advanced Patent Search — recommended

- Connector key: `advanced_patent_search`
- Marketplace: <https://open.patsnap.com/marketplace/mcp-servers/patent-search>
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`

Use for number, assignee, inventor, keyword, classification, semantic, citation, family-neighbor, and fielded retrieval when available.

### Patent Briefing — required for candidate verification

- Connector key: `patent_briefing`
- Marketplace: <https://open.patsnap.com/marketplace/mcp-servers/patent-briefing>
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`

Use bibliography, family, legal status, claims, translated claims, descriptions, translated descriptions, images, and technical summaries as applicable.

### Global Core Patent Database — recommended

- Connector key: `global_core_patent_database`
- Marketplace: <https://open.patsnap.com/marketplace/mcp-servers/core-patents>
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/core-patents`

Use for detailed legal events, full text, PDF, images, reexamination or invalidation data, and status cross-checking when applicable.

Never expose, log, or embed a real API key. Official patent registers and courts remain authoritative for dispositive status, claim version, term, and legal-proceeding checks.

## Eight-step workflow

### Step 1 — Define application requirements

Create the application requirements record that the source expected from its missing helper.

#### Requirements record

| Requirement ID | Category | Metric or constraint | Target | Tolerance/range | Priority | Verification method | Source | Status |
|---|---|---|---|---|---|---|---|---|
| R-001 | Performance | | | | Must/Should/Could | | | |

Include:

- use case and operating environment;
- required functions;
- performance targets and tolerances;
- safety and regulatory constraints;
- material and component restrictions;
- manufacturing capability and process windows;
- supply-chain and sourcing constraints;
- interface and system constraints;
- cost, scale, yield, reliability, and sustainability requirements;
- test method, sample preparation, conditioning, and acceptance criteria; and
- requirements that may be traded versus requirements that are fixed.

Convert every vague request into a measurable requirement or mark it unresolved. Do not invent a test method or tolerance.

Record a product baseline:

| Feature ID | Product/process feature | Value or implementation | Unit/basis | Tolerance | Evidence | Confidence |
|---|---|---|---|---|---|---|

This record is the north star for every later concept. A legal difference that makes the product unusable is not a viable design-around.

### Step 2 — Inventory the full candidate patent set

Start with the user's list and, when authorized, execute a search appropriate to the product, process, jurisdictions, dates, owners, technical field, and intended acts.

For each family and jurisdictional member:

1. verify publication and application numbers;
2. identify owner/applicant and relevant assignments;
3. identify family relationships;
4. retrieve current claim text;
5. verify legal status and as-of date;
6. identify filing, priority, grant, expiry, lapse, opposition, review, or invalidation events;
7. identify continuation, divisional, national-stage, reissue, utility-model, and pending claim exposure;
8. retrieve prosecution history when material;
9. preserve source-language text and translation provenance; and
10. state why the right is included or excluded.

Do not rank risk by the size or reputation of the applicant. Rank by legal relevance, claim mapping, current status, jurisdiction, timing, evidence completeness, and business impact.

#### Patent intelligence matrix

| ID | Family/right | Jurisdiction | Owner | Current claims/status as of | Claim type | Material limitations | Product relevance | Evidence gaps | Priority |
|---|---|---|---|---|---|---|---|---|---|

Classify claims where helpful:

- composition or formulation;
- apparatus or system;
- method or process;
- performance or parameter;
- application or use;
- product-by-process;
- software or control logic;
- design right; or
- another jurisdiction-specific category.

Do not reduce process or use claims to composition intervals. Preserve the actual elements and claim dependencies.

#### Unit and measurement normalization

For every numerical limitation, record:

| Parameter | Source value | Source unit/basis | Normalized value | Conversion | Test method | Uncertainty | Confidence |
|---|---|---|---|---|---|---|---|

For composition conversions such as mole percent to weight percent:

- use the exact chemical species and molar masses;
- state whether values are oxide basis, elemental basis, dry basis, as-batched, or measured;
- account for ranges, impurities, volatiles, and normalization totals;
- retain significant figures and uncertainty;
- verify that the claim permits the proposed comparison basis; and
- never compare converted values without documenting the calculation.

### Step 3 — Deepen review of priority patents

Select one or more priority rights based on breadth of relevant mapped claims, current status, jurisdiction, product overlap, timing, evidence quality, and business impact. The source suggested one to two; use that as a workload heuristic, not a rule that excludes other material claims.

For each priority independent claim and any material dependent claim, build:

#### Claim limitation map

| Limitation ID | Exact claim text | Construction issue | Product evidence | Present/Absent/Unknown | Design variable | Source |
|---|---|---|---|---|---|---|

#### Functional model handoff

| Limitation/group | Function | Mechanism/structure | Result | Dependency | Essential to product? | Alternative opportunity |
|---|---|---|---|---|---|---|

Preserve the source's intent to create seed concepts, but do not require exactly ten. Generate enough distinct concepts to cover meaningful design variables and technical architectures.

For every seed concept, record:

- changed limitation or limitation group;
- technical mechanism;
- expected effect;
- requirements preserved or compromised;
- evidence supporting feasibility;
- manufacturing implications;
- new patent-search hypotheses;
- legal uncertainties; and
- next experiment or calculation.

If `develop-patent-design-arounds-ip` is available and suitable, it may produce these records. Otherwise perform the deep review here.

### Step 4 — Identify parameter-level candidate design space

Preserve the source's interval visualization for numerical claim limitations, but treat it as one analysis aid rather than a legal safe-zone oracle.

For each parameter:

1. identify the exact claim and dependency context;
2. record open/closed endpoints and linguistic qualifiers;
3. normalize units only when technically and legally comparable;
4. plot claimed intervals by jurisdiction and claim version;
5. identify uncovered or differently covered candidate regions;
6. account for measurement method, rounding, uncertainty, manufacturing tolerance, and specification limits;
7. test interaction with other limitations and relationship equations;
8. test technical feasibility against Step 1; and
9. flag equivalents, claim-construction, and prosecution-history questions for counsel.

#### Interval record

| Parameter | Claim/right | Claim context | Interval and endpoint semantics | Unit/test | Candidate region | Tolerance margin | Feasibility | Legal caveat |
|---|---|---|---|---|---|---|---|---|

The source required at least one “safe zone” for every parameter. Do not force one. Use `No viable candidate region identified` when the evidence supports that result, then revisit the architecture, search scope, or requirements.

Do not use a universal five-percent boundary rule. Define engineering guard bands from process capability, measurement uncertainty, product specifications, and counsel advice. A numerical difference is not automatically legally sufficient.

#### Candidate design-space assessment

| Region ID | Variables changed | Rights potentially distinguished | Requirement fit | Process tolerance | Evidence | Remaining uncertainty | Recommendation |
|---|---|---|---|---|---|---|---|

### Step 5 — Design candidate formulations or solutions

Solve against two constraint sets:

- application and manufacturing requirements from Step 1; and
- claim-informed candidate design space from Steps 2–4.

Create three to five differentiated concepts when technically justified. Preserve the source archetypes:

1. conservative/high-margin concept;
2. performance-priority concept;
3. system-level or architecture-shift concept; and
4. optional manufacturing-ready concept.

Do not force a concept merely to satisfy the count. Diversity must come from genuinely different limitations, mechanisms, architectures, processes, or use contexts.

#### Candidate concept record

| Field | Content |
|---|---|
| Concept ID/version | Stable identifier and version |
| Positioning | Conservative, performance, architecture shift, or manufacturing ready |
| Full specification | Complete formulation, architecture, process, or control logic |
| Changed design variables | Exact values, structures, sequence, or functions |
| Requirements mapping | Met, uncertain, or unmet for each Step 1 requirement |
| Claim-informed rationale | Limitations the concept may distinguish and why |
| Feasibility evidence | Literature, experiments, models, supplier data, or engineering judgment |
| Tolerances | Manufacturing and measurement margins |
| Trade-offs | Cost, performance, yield, reliability, safety, regulation, integration |
| New search hypotheses | Features that may trigger additional patent searches |
| Validation plan | Calculations, prototypes, tests, and acceptance criteria |

The source suggested a universal ten-percent performance surplus. Replace it with requirement-specific design margin justified by uncertainty, reliability, and process capability.

### Step 6 — Cross-screen every candidate against every material claim

Create a matrix with candidate concepts as rows and material current claims as columns. Do not screen only “claim 1” if other independent or dependent claims are relevant.

For each cell, map every required limitation and assign one text state:

- `Potential literal overlap`;
- `Literal distinction identified`;
- `Equivalents/claim-construction review required`;
- `Insufficient product or claim evidence`;
- `Right not currently material for stated jurisdiction/act/date`; or
- `Excluded with documented basis`.

Do not use check marks or colors as conclusions.

#### Candidate-by-claim matrix

| Candidate | Right/claim | Jurisdiction/act | Literal mapping | Distinguishing limitation | Equivalents/construction issue | Status/date issue | Evidence state | Action |
|---|---|---|---|---|---|---|---|---|

#### Cell analysis

For every material cell:

1. identify the claim version;
2. state applicable jurisdiction and intended act;
3. list all claim limitations;
4. map product/process evidence to each limitation;
5. identify any absent or unknown limitation;
6. identify construction disputes;
7. identify jurisdiction-specific equivalents issues;
8. identify prosecution-history or estoppel evidence when available;
9. verify status and timing; and
10. state the evidence-qualified screening result.

The source used a universal means/function/effect equivalents test and “prohibition on reversal” formulation. Localize this to the law and terminology of each jurisdiction. Do not assume one doctrine or test applies worldwide.

### Step 7 — Repair identified risks and repeat

For each `Potential literal overlap`, equivalents concern, or evidence gap, create a repair record.

#### Repair record

| Field | Content |
|---|---|
| Repair ID | Stable identifier |
| Candidate/right/claim | Exact matrix cell |
| Issue | Limitation, construction, equivalent, status, or evidence gap |
| Proposed change | Specific technical modification |
| Technical rationale | Why it may preserve requirements |
| Claim rationale | Which mapped limitation changes |
| New risk | Other patents, requirements, safety, regulatory, or process effects |
| Validation | Required calculation, search, test, or counsel review |
| Result/version | New candidate version and re-screen state |

Preserve the source's repair hierarchy as engineering options:

1. adjust one component, parameter, step, or relationship;
2. compensate using another technically justified component or mechanism; and
3. change the technical system or architecture.

Before adding a new component or mechanism, search and screen the new feature. Never assume that a feature absent from the initial set is unpatented.

Repeat Steps 5–7 until:

- remaining issues are understood and accepted for escalation;
- no technically viable revision remains;
- the business changes scope; or
- counsel and engineering agree that evidence is sufficient for the decision.

Do not require every matrix cell to become a green check. A truthful `Insufficient evidence` or `Counsel review required` is preferable to false clearance.

### Step 8 — Prepare the attorney-review package and technical validation plan

Create a draft analytical framework, not a signed or formal legal opinion.

#### Attorney-review package

For every recommended candidate and material claim, include:

1. jurisdiction, intended act, dates, and product version;
2. patent/family identity, owner, status, term, and claim version;
3. exact claim text and source-language provenance;
4. element-by-element literal mapping;
5. identified distinguishing limitation;
6. claim-construction questions;
7. jurisdiction-specific equivalents issues;
8. prosecution-history or estoppel evidence;
9. status, family, continuation, opposition, review, or invalidation issues;
10. evidence gaps and assumptions;
11. candidate trade-offs and implementation controls; and
12. questions requiring qualified counsel.

Use outcomes such as:

- `Lower concern on reviewed evidence`;
- `Material concern`;
- `Counsel analysis required`;
- `Insufficient evidence`; or
- `Not material under stated scope`.

Do not label a candidate “non-infringing,” “infringing,” “safe,” or “cleared” without an appropriately qualified legal determination.

#### Technical validation plan

| Test ID | Candidate | Requirement/risk | Method/standard | Sample/conditioning | Acceptance criterion | Uncertainty | Priority | Owner | Dependency |
|---|---|---|---|---|---|---|---|---|---|

Cover:

- performance requirements;
- composition or dimensional verification;
- process-window and yield verification;
- measurement-method alignment with claim language;
- reliability and environmental testing;
- safety and regulatory checks;
- supplier and manufacturing controls;
- claim-relevant product teardown or inspection evidence;
- updated patent searches triggered by the design; and
- final counsel review after design freeze.

#### Follow-on action register

| Priority | Action | Owner | Trigger | Evidence needed | Completion criterion |
|---|---|---|---|---|---|

## Eight required deliverables

| No. | Deliverable | Step |
|---:|---|---:|
| 1 | Application requirements record | 1 |
| 2 | Patent intelligence matrix | 2 |
| 3 | Priority-claim maps and seed concepts | 3 |
| 4 | Parameter/constraint design-space map | 4 |
| 5 | Differentiated candidate concept set | 5 |
| 6 | Candidate-by-claim cross-screen matrix | 6 |
| 7 | Repaired candidate versions and iteration log | 7 |
| 8 | Attorney-review package and technical validation plan | 8 |

## Seven source principles, localized

1. **Drive the work from application requirements.**
   - Use requirements as design constraints, not merely context.
   - A different use case can create design options, but does not itself eliminate claim exposure.

2. **Analyze the combined constraint set rather than repeating isolated reviews.**
   - Use priority deep dives to generate concepts.
   - Still screen every material current claim.

3. **Normalize units and measurement bases transparently.**
   - Preserve source units.
   - Document conversions, methods, uncertainty, and assumptions.

4. **Separate composition, process, apparatus, performance, and use claims.**
   - Each claim type requires its own product/process evidence.
   - Do not infer process distinctions from composition alone.

5. **Use justified engineering margins.**
   - Base margins on tolerance, uncertainty, capability, requirements, and counsel input.
   - Do not use the source's universal five-percent legal or ten-percent performance rule.

6. **Maintain at least one architecture-level alternative when feasible.**
   - Treat it as a resilience option, not automatic legal clearance.
   - Screen new architecture features for other rights.

7. **Search family members, continuations, divisionals, and pending claims.**
   - Use jurisdiction-appropriate relationship types.
   - Recheck at design freeze and before material market entry.

## Illustrative source case — HAMR glass substrate

The Chinese source included a specific example involving a proposed heat-assisted magnetic recording glass substrate and eight Chinese patent publications associated with several Japanese glass companies. Preserve it only as an illustration of the eight-step structure, not as verified current FTO advice or a reusable recipe.

### Source example context

The source described a customer considering entry into the HAMR glass-substrate market and listed:

- CN102473426B;
- CN103121791B;
- CN103313948B;
- CN104230164B;
- CN104619663B;
- CN106396370B;
- CN107032603B; and
- CN107615381B.

The source summarized requirements such as a high glass-transition temperature, elastic-modulus and density relationship, thermal-expansion range, and alkali-free composition. It then grouped the patents into formulation, process, and edge-processing types; selected CN103313948B for deeper review; plotted example boron-oxide, modifier-oxide, and aluminum-oxide ranges; generated four HAMR concepts; identified two cross-screen issues; and suggested revised formulations plus testing and prosecution-history review.

### Localization caveats for the example

- Do not reuse the listed status, claims, ownership, or family facts without current verification.
- Do not treat the example intervals as globally safe regions.
- Do not use the source's exact compositions as engineering recommendations without materials evidence and testing.
- Do not infer that a Chinese-grant analysis covers Japan, the United States, Europe, or another jurisdiction.
- Do not claim the referenced companies are high risk because they are large.
- Do not represent the source's final dual-track recommendation as current advice.
- Use the example only to demonstrate how requirements, claim matrices, design-space views, candidate concepts, repair, and validation connect.

## Output format and scientific presentation

Produce Markdown by default and a single portable HTML report when requested. Use a restrained Western scientific/legal aesthetic:

- neutral paper surface and charcoal text;
- navy/slate hierarchy;
- concise executive assessment and scope banner;
- semantic tables with captions and text states;
- claim-limitation and candidate matrices;
- interval plots with open/closed endpoint legends, units, and test methods;
- design-trade-space and iteration records;
- source and assumption registers;
- responsive wrappers and print CSS;
- no emoji-only states, decorative gradients, faux certainty, or remote runtime dependencies.

If creating interval plots, ensure each plot shows:

- parameter and normalized unit;
- source claim/right and jurisdiction;
- claim dependency context;
- open and closed endpoints;
- measurement method;
- manufacturing tolerance and uncertainty;
- candidate values and version;
- feasibility state; and
- legal caveat.

Escape all external content in HTML. Reject unsafe URLs. Do not embed secrets, API keys, local absolute paths, `file:` URLs, internal IDs, active remote scripts, or untrusted markup.

## Failure and fallback behavior

- Missing live MCP: provide the workflow and analyze supplied verified materials only; do not simulate searches.
- Missing current claims: do not complete a claim mapping for that right.
- Missing status date: label status as unverified and request official-register review.
- Missing product feature: mark the limitation mapping `Unknown`.
- Missing unit basis or method: do not convert or compare values as equivalent.
- No viable parameter region: revisit architecture, requirements, or search; do not invent a safe zone.
- No feasible candidate: report the constraint conflict and required decision.
- Missing prosecution history: identify equivalents/estoppel analysis as incomplete.
- Conflicting translations: preserve source language and route to qualified review.
- Incomplete search coverage: never state that all relevant patents were found.
- Confidential inputs: minimize external disclosure and follow user-authorized connector boundaries.

## Final acceptance checklist

- All eight source steps were executed or explicitly marked incomplete.
- All eight required deliverables are present.
- All seven source principles are preserved in localized form.
- Requirements and product versions are frozen.
- Jurisdictions, intended acts, dates, and business scope are explicit.
- Search routes and caps are reproducible.
- Patent numbers, families, owners, claims, status, and dates are verified.
- Every material independent and dependent claim is considered.
- Unit conversions include basis, method, uncertainty, and calculation.
- Numerical intervals retain endpoint semantics and claim context.
- No universal safe-zone, five-percent, or ten-percent rule is applied.
- Priority rights were selected by evidence, not applicant reputation.
- Candidate concepts are technically differentiated and versioned.
- Every candidate is cross-screened against every material current claim.
- Literal mapping is separate from jurisdiction-specific equivalents analysis.
- Prosecution-history issues are sourced or marked incomplete.
- Repair changes are re-searched and re-screened.
- No green check or “safe” label substitutes for analysis.
- The attorney-review package is clearly a draft analytical framework.
- Technical tests have methods, samples, acceptance criteria, uncertainty, and owners.
- The HAMR source case is labeled illustrative and not current advice.
- MCP keys, pages, endpoints, tools, queries, dates, and limitations are accurate.
- Official-register and qualified-counsel gates are explicit.
- HTML, if produced, is safe, accessible, responsive, printable, and portable.

