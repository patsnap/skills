---
name: assess-automotive-lighting-ip
description: Assess automotive-lighting component architecture, sourcing strategy, and preliminary patent and design-right risk. Use when a user provides a lamp drawing, product image, bill of materials, technical concept, or make-versus-buy question for headlamps, rear lamps, fog lamps, signal lamps, or ambient lighting and needs an evidence-backed component breakdown, sourcing decision, multi-jurisdiction FTO screening, design-risk review, design-around options, and an accessible tabbed HTML report packaged as a ZIP file.
---

# Assess automotive lighting sourcing and IP risk

## Role

Act as an automotive-lighting engineering, supply-chain, and intellectual-property analyst.

Combine optical, thermal, mechanical, electrical, manufacturing, sourcing, patent, and industrial-design perspectives.

Treat the analysis as a preliminary engineering and IP screening exercise.

Do not present it as a legal opinion.

Do not state that a product is cleared for launch.

Route final claim construction, infringement, validity, enforceability, and clearance decisions to qualified counsel in each relevant jurisdiction.

## Core outcome

Produce four connected analyses:

1. Decompose the lamp into functional modules and components.
2. Evaluate make, buy, and hybrid sourcing options.
3. Screen invention-patent, utility-model, and design-right risks.
4. Integrate sourcing, design, evidence, and risk-mitigation recommendations.

Deliver the result as one self-contained, accessible, tabbed HTML file.

Package that HTML file in a ZIP archive when file creation is requested and available.

Report the exact output paths.

## Trigger cases

Use this skill when the user provides or requests analysis of any of the following:

- A headlamp, rear lamp, fog lamp, signal lamp, marker lamp, or ambient-lighting design.
- A sketch, rendering, photograph, CAD export, drawing description, or design brief.
- A lamp bill of materials or component list.
- An optical, thermal, electronic, or mechanical lighting concept.
- A make-versus-buy question for a lamp component or subassembly.
- A supplier-selection question with an IP-risk dimension.
- A preliminary FTO review for automotive-lighting technology.
- A design-right similarity review for a lighting signature or lamp appearance.
- A design-around request for a suspected patent or registered design.

## Scope boundaries

Include automotive exterior and interior lighting when the user places it in scope.

Cover complete lamps, modules, subassemblies, and individual components.

Do not assume that all jurisdictions recognize the same right types.

Do not treat an EP patent as an EU registered design.

Do not treat a registered design as an invention patent.

Do not assume that a utility-model system exists in every target market.

Do not use one universal design-infringement test across jurisdictions.

Do not infer an active right from a publication number alone.

Do not infer infringement from visual resemblance alone.

Do not infer claim coverage from an abstract, title, drawing, or machine-generated summary.

## Required inputs

Collect the available inputs before substantive analysis.

### Product and program

- Vehicle or product program name.
- Lamp type and vehicle position.
- Intended function or functions.
- New design, carryover design, or derivative.
- Prototype, sourcing, validation, or production stage.
- Planned launch date.
- Intended countries of manufacture.
- Intended countries of sale, import, use, or offer for sale.
- Expected program lifetime.
- Target production volume.

### Visual and dimensional material

- Product images or renderings.
- Front, rear, side, perspective, and illuminated-state views.
- Drawings or CAD exports.
- Critical dimensions and tolerances.
- Section views.
- Exploded views.
- Surface and appearance specifications.
- Light-signature geometry.

### Optical architecture

- Light source type.
- LED package, chip-on-board, laser, bulb, or other source.
- Lens and reflector arrangement.
- Projector or reflector architecture.
- Light guide, thick-wall optic, micro-optic, or diffractive element.
- Beam-forming features.
- Pixel, matrix, adaptive, or scanning function.
- Daytime-running-light pattern.
- Turn-signal or animation sequence.

### Thermal and mechanical architecture

- Heat-sink material and process.
- Passive or active cooling.
- Fan or blower details.
- Thermal-interface material.
- Housing and bezel materials.
- Sealing approach.
- Venting or moisture-management approach.
- Adjustment and leveling mechanism.
- Mounting interfaces.
- Serviceability and replaceability.

### Electrical and control architecture

- Driver topology.
- Control unit and communication interface.
- Sensors and feedback loops.
- Dimming, leveling, animation, or adaptive-control logic.
- Connector and harness requirements.
- Functional-safety or cybersecurity constraints if relevant.

### Sourcing and economics

- Current and candidate suppliers.
- Approved-vendor constraints.
- Existing tooling and manufacturing capability.
- Capital-expenditure constraints.
- Tooling assumptions.
- Target unit cost and currency.
- Quoted price, quotation date, volume basis, and Incoterms.
- Quality, logistics, capacity, warranty, and localization constraints.
- Strategic technology that must remain in-house.

### IP scope

- Features planned for in-house design.
- Known patents, designs, applications, or disputes.
- Known competitors, OEMs, and suppliers.
- Target jurisdictions.
- Search cut-off date.
- Legal-status cut-off date.
- Applicant, assignee, inventor, or designer names to include.
- Known classification codes.

## Missing-input gate

If a missing input would materially change the result, ask a focused question before assigning a recommendation.

Prioritize questions about:

- Target markets.
- Product images and views.
- Planned in-house features.
- Optical architecture.
- Materials and manufacturing process.
- Thermal approach.
- Adjustment mechanism.
- Launch date.
- Target volume and cost basis.

If the user cannot provide the information, continue only with explicit assumptions.

List each assumption.

State its effect on sourcing and IP confidence.

## Evidence rules

Distinguish user-provided facts, retrieved evidence, analyst inference, and unresolved assumptions.

Provide a source for every material external factual claim.

Use direct patent, design-register, official-office, supplier, standards, or regulatory evidence where available.

Record the publication or registration number exactly.

Record the jurisdiction and right type.

Record the application, filing, priority, publication, registration, or grant dates relevant to the conclusion.

Record the legal-status source and its retrieval date.

Record family relationships when they affect territorial coverage.

Link to the supporting record.

Never invent a patent number, design number, legal status, claim quotation, supplier, price, or technical specification.

Never convert a well-known design motif into a patent fact without verified records.

Treat named lighting signatures as search hypotheses, not evidence.

## PatSnap MCP plan

### Required: Patsnap Patent Research

Use the official Patsnap Patent Research MCP server for live FTO execution.

Official page: https://open.patsnap.com/marketplace/mcp-servers/patsnap-ip-searching

Configuration key: `patsnap_patent_research`.

Transport: `streamableHttp`.

Current Connect-panel pattern verified on 2026-08-07:

`https://open.patsnap.com/marketplace/mcp-servers/patsnap-ip-searching`

Always copy the current URL from the official Connect panel.

Never place a real API key in the report, skill, source control, or logs.

Use `fto_review` for invention-patent FTO screening.

Use country, application-date, legal-status, and assignee filters as appropriate.

Use `search.mode: lite` for a clearly labeled preliminary screen.

Use `search.mode: pro` when the task and available access justify deeper analysis.

Use `design_fto` for design-risk screening from one product or design image.

Remember that only the first `input.images` item is used by that tool.

Select the most representative view for the tool call.

Run separate calls for materially different views when necessary.

Use country, application-date, legal-status, and Locarno-classification filters where appropriate.

Use `get_task` to retrieve asynchronous status and results.

### Recommended: Patent Briefing

Use Patent Briefing to verify candidate records and evidence.

Official page: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

Configuration key: `patent_briefing`.

Transport: `streamableHttp`.

Current Connect-panel pattern verified on 2026-08-07:

`https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`

Use `search_patents` for focused candidate retrieval.

Use `bibliography` to verify identifiers and bibliographic facts.

Use `legal_status` to verify current simple legal status.

Use `family` to review related filings and jurisdictional coverage.

Use `claims` or `claim_translated` for claim review.

Use `description` or `description_translated` for specification review.

Use `intelligent_image` for available patent drawings.

Do not rely on translated text without checking the original when wording is outcome-determinative.

### Optional: Advanced Patent Search

Use Advanced Patent Search for broader search development and refinement.

Official page: https://open.patsnap.com/marketplace/mcp-servers/patent-search

Configuration key: `advanced_patent_search`.

Transport: `streamableHttp`.

Current Connect-panel pattern verified on 2026-08-07:

`https://open.patsnap.com/marketplace/mcp-servers/patent-search`

Use image search for visually similar patent material.

Use semantic search for concept exploration.

Use nested queries for controlled Boolean strategies.

Use assignee tools for supplier and OEM portfolio refinement.

Use field analytics and keyword suggestions to improve the search strategy.

### Tool fallback

The source names `patent.fetch` and `patsnap_fetch` are not verified current PatSnap Open tools.

Do not call or document them as available tools.

If the required MCP server is unavailable, do not fabricate search results.

Provide the search strategy, target jurisdictions, candidate fields, and execution checklist.

Label the result `not executed` or `preliminary based on supplied records`.

## Workflow

### Phase 0: Define the decision frame

Restate the user’s business decision.

Identify the product configuration being assessed.

Identify the intended market and manufacturing jurisdictions.

Identify the features planned for in-house design.

Set the evidence cut-off date.

Set the legal-status cut-off date.

Define the unit of patent counting.

Define whether the review is publication-level, application-level, family-level, or right-level.

List known exclusions.

List unresolved assumptions.

### Phase 1: Decompose the lamp

Break the system into modules without assuming the source table is exhaustive.

#### Optical module

Consider:

- Outer lens.
- Inner lens.
- Projector lens.
- Reflector.
- Light guide.
- Thick-wall optic.
- Collimator.
- Micro-optic array.
- Diffuser.
- Shutter.
- Beam-pattern element.
- Decorative optical element.

Record the function, material, geometry, interfaces, tolerances, process, and evidence.

#### Light-source module

Consider:

- LED package.
- Chip-on-board source.
- Laser source.
- Conventional bulb.
- Source carrier.
- Driver board.
- Printed circuit board.
- Optical alignment features.

Do not automatically conclude that every light source must be purchased.

Evaluate qualification, intellectual property, scale, safety, and manufacturing capability.

#### Thermal-management module

Consider:

- Die-cast heat sink.
- Extruded heat sink.
- Stamped heat spreader.
- Fan or blower.
- Heat pipe.
- Thermal-interface material.
- Venting and condensation management.
- Temperature sensing and derating.

#### Mechanical module

Consider:

- Housing.
- Bezel.
- Frame.
- Bracket.
- Adjuster.
- Leveling mechanism.
- Fasteners.
- Seals.
- Vents.
- Mounting and datum features.

#### Electrical and control module

Consider:

- Driver integrated circuit.
- Electronic control unit.
- Printed circuit board.
- Connector.
- Harness.
- Sensor.
- Communication interface.
- Control software or algorithm.

#### Appearance and signature layer

Treat appearance as a cross-module layer.

Record:

- Overall lamp form.
- Visible surface transitions.
- Lens and bezel composition.
- Illuminated and unilluminated appearance.
- Daytime-running-light signature.
- Rear-lamp signature.
- Sequential or animated behavior.
- Color, texture, pattern, and contrast.

### Component inventory table

Create one row per component or subassembly.

Use these columns:

| ID | Module | Component | Function | Material/process | Key interfaces | Critical dimensions | Source evidence | Missing information |
|---|---|---|---|---|---|---|---|---|

### Phase 2: Evaluate make, buy, and hybrid options

Evaluate each component independently.

Do not use a universal source recommendation as the conclusion.

Score or explain these dimensions:

- Strategic differentiation.
- Internal design capability.
- Internal manufacturing capability.
- Capital and tooling needs.
- Qualification burden.
- Safety and regulatory burden.
- Quality-control complexity.
- Supplier availability.
- Capacity and lead time.
- Supply concentration.
- Logistics and localization.
- Warranty exposure.
- IP density and licensing risk.
- Data and know-how sensitivity.
- Cost confidence.
- Lifecycle and serviceability.

Use `Make`, `Buy`, or `Hybrid` as the recommendation.

Use `High`, `Medium`, or `Low` for feasibility only when supported by stated criteria.

Explain the reasons.

### Cost discipline

Do not estimate a cost multiplier without a defensible basis.

When cost data exists, record:

- Currency.
- Price basis.
- Volume tier.
- Quotation date.
- Incoterms.
- Tooling amortization.
- Scrap and yield assumptions.
- Labor and overhead assumptions.
- Logistics and duty assumptions.
- Warranty and quality assumptions.
- Sensitivity range.

When cost data is absent, state `Cost estimate not available`.

Provide a cost-data request instead of a fabricated ratio.

### Sourcing decision table

Use these columns:

| Component | Buy feasibility | Make feasibility | Recommended model | Supplier/channel evidence | Cost basis | IP implications | Conditions | Confidence |
|---|---|---|---|---|---|---|---|---|

Do not present Valeo, FORVIA HELLA, Marelli, Stanley Electric, Koito, an OEM, or another organization as a suitable supplier solely from memory.

Verify current capability, geography, capacity, and product fit.

### Phase 3: Screen IP risk

Perform this phase for every feature planned for in-house design and every purchased component whose contractual allocation leaves material exposure.

#### 3.1 Define technical and visual features

Create a feature list before searching.

Separate functional technical features from visual design features.

For technical features, record:

- Problem addressed.
- Components involved.
- Required relationships.
- Operating sequence.
- Claimed benefit.
- Optional versus essential elements.

For visual features, record:

- Overall form.
- Dominant visual features.
- Surface transitions.
- Proportions.
- Pattern and arrangement.
- Illuminated appearance.
- Unilluminated appearance.
- Features dictated solely by technical function.

#### 3.2 Select right types by jurisdiction

Consider invention patents in every relevant patent jurisdiction.

Consider utility models only where available and relevant.

Consider US design patents for the United States.

Consider EU registered designs through EUIPO for EU-wide registered design coverage.

Consider international designs through the WIPO Hague System where applicable.

Consider national registered or unregistered design rights where relevant.

Consider copyright, trade dress, unfair competition, contract, and confidential know-how only when supported by the user’s scope and local law.

Do not label EPO invention-patent results as design rights.

#### 3.3 Build the search strategy

Search by:

- Function.
- Structure.
- Component relationships.
- Optical path.
- Thermal path.
- Control sequence.
- Material and process.
- Applicant or assignee.
- Inventor.
- Citation.
- Patent classification.
- Locarno classification for designs.
- Image similarity.
- Semantic similarity.
- Known patent or design number.

Use synonyms, abbreviations, spelling variants, and relevant local-language terms.

Document the exact search expressions and filters.

#### 3.4 Jurisdiction matrix

Create one row for each target market.

Use these columns:

| Market | Manufacture/import/sale/use activity | Invention patents | Utility models | Design channel | Search source | Cut-off | Counsel needed |
|---|---|---|---|---|---|---|---|

Use jurisdiction-specific channels, including as applicable:

- CNIPA for China.
- USPTO for the United States.
- EPO for European patents.
- EUIPO for EU registered designs.
- WIPO Hague for international designs.
- JPO for Japan.
- KIPO for Korea.
- DPMA for German national rights.
- Other national or regional offices selected by the user.

Do not force CN, US, EP, JP, KR, or DE when they are outside the commercial scope.

Do not omit a market merely because it was absent from the source default list.

#### 3.5 Candidate screening

For every candidate, verify:

- Publication or registration number.
- Application or filing number where available.
- Right type.
- Jurisdiction.
- Applicant and current owner where available.
- Priority date.
- Filing date.
- Publication, registration, or grant date.
- Earliest priority family.
- Legal status and status date.
- Expected term only when verified under applicable law.
- Independent claims or protected design views.
- Relevant drawings.
- Product-feature mapping.
- Uncertainties.

#### 3.6 Invention and utility-model analysis

Read the independent claims.

Use dependent claims when they materially affect the risk analysis.

Break each relevant claim into limitations.

Map each limitation to the assessed product with evidence.

Use `Present`, `Absent`, or `Unclear`.

Do not use doctrine-of-equivalents analysis as a substitute for counsel.

Flag means-plus-function, functional claiming, prosecution history, translation, or claim-construction issues for legal review.

#### Claim comparison table

| Candidate | Claim | Limitation | Product evidence | Mapping | Uncertainty | Preliminary implication |
|---|---|---|---|---|---|---|

#### 3.7 Design-right analysis

Review every available registered view.

Compare the assessed product in equivalent views.

Identify dominant similarities and differences.

Separate visible appearance from features dictated solely by function where applicable.

Consider the applicable jurisdiction’s legal test.

Do not state one global “overall visual effect” rule.

Do not assume that a different badge, color, or minor detail avoids risk.

Do not assume that a similar lighting signature is protected without a verified registration.

#### Design comparison table

| Candidate design | Jurisdiction | Registered views | Product view | Dominant similarities | Material differences | Legal-test note | Preliminary risk |
|---|---|---|---|---|---|---|---|

#### 3.8 Branded design motifs

Treat famous lighting signatures as leads for evidence collection.

Examples may include halo-like light rings, hammer-shaped daytime-running lights, star motifs, continuous light bars, pixel patterns, or other recognizable signatures.

Do not attribute a motif to a brand without verification.

Do not claim that the motif is patented or registered without an identifier and source.

Do not repeat the source’s unsupported “Audi Thor’s Hammer” attribution.

Verify the brand, designer, record owner, jurisdiction, and protected subject matter.

#### 3.9 Risk rating

Use `High`, `Medium`, `Low`, or `Insufficient evidence`.

Do not use emoji as the sole rating.

Do not rely on color alone.

Base the rating on:

- Territorial relevance.
- Current legal status.
- Remaining term where verified.
- Claim or design-feature mapping.
- Product evidence quality.
- Family and ownership context.
- Known licensing, exhaustion, supplier indemnity, or other defenses only when documented.
- Material uncertainty.

Define ratings:

- `High`: strong preliminary mapping to an apparently relevant, in-force right in a target jurisdiction; urgent counsel review required.
- `Medium`: meaningful overlap or uncertainty requiring additional evidence, claim/design review, or counsel input.
- `Low`: material differences or lack of territorial/status relevance based on verified evidence, while preserving stated limitations.
- `Insufficient evidence`: search, status, claims, views, or product information is inadequate for a defensible rating.

#### Candidate-right table

| ID | Number | Right type | Owner | Jurisdiction | Status | Relevant feature | Mapping summary | Risk | Evidence link | Next action |
|---|---|---|---|---|---|---|---|---|---|---|

### Phase 4: Develop mitigation and design-around options

Develop options only after identifying the relevant claim limitations or protected visual features.

For technical rights, consider:

- Removing an essential claim limitation.
- Changing component relationships.
- Changing the optical path.
- Changing the control sequence.
- Changing the thermal architecture.
- Changing the adjustment mechanism.
- Changing material or manufacturing process where technically meaningful.
- Purchasing a licensed component.
- Seeking a license.
- Challenging validity only with appropriate evidence and counsel.

For design rights, consider:

- Changing the overall form.
- Changing dominant proportions.
- Changing surface transitions.
- Changing the arrangement of visual elements.
- Changing the light-signature geometry.
- Changing the illuminated sequence or pattern where legally relevant.
- Creating multiple visually distinct alternatives.

Do not recommend cosmetic changes that leave the same dominant impression without analysis.

Do not recommend technical changes that compromise photometry, safety, thermal performance, manufacturability, serviceability, or regulatory compliance.

### Design-around table

| Candidate right | Risk driver | Proposed change | Claim/design effect | Engineering effect | Cost/schedule effect | Verification needed | Residual risk |
|---|---|---|---|---|---|---|---|

### Integrated recommendation

Connect the sourcing and IP results.

For each component, state:

- Recommended make, buy, or hybrid model.
- Technical reason.
- Commercial reason.
- IP reason.
- Required supplier warranty, license, or indemnity issue.
- Required design change.
- Required verification.
- Decision owner.
- Due date.

Use an action register:

| Priority | Action | Owner | Dependency | Evidence required | Due date | Decision gate |
|---|---|---|---|---|---|---|

## HTML report specification

Create one self-contained HTML5 file when the user requests the report artifact.

Use `lang="en"`.

Use semantic landmarks: `header`, `nav`, `main`, `section`, and `footer`.

Keep CSS and JavaScript inline.

Do not require remote fonts, frameworks, scripts, or images to render the report.

Use a restrained scientific visual system.

Use a white background.

Use near-black or charcoal body text.

Use one restrained blue accent.

Use light neutral rules and table backgrounds.

Do not use gradients.

Do not use oversized decorative cards.

Do not use emoji as status markers.

Do not use color as the only carrier of meaning.

Use a system-font stack suitable for Western business and scientific reports.

Use sentence-case headings.

Use consistent spacing and table density.

Use captions for figures and tables.

Show units in headers.

Show the evidence and legal-status cut-off dates.

Show the jurisdiction scope.

Show the counting unit.

Show missing-data notes.

Show source links adjacent to supported claims.

### Required report tabs

Include these tabs:

1. Executive summary.
2. Product and assumptions.
3. Component architecture.
4. Make-versus-buy analysis.
5. Patent and utility-model screening.
6. Design-right screening.
7. Mitigation and design-around options.
8. Evidence and methodology.

### Accessible tabs

Implement the tabs as an accessible tab interface.

Use `role="tablist"`, `role="tab"`, and `role="tabpanel"`.

Connect tabs and panels with `aria-controls` and `aria-labelledby`.

Expose the selected state with `aria-selected`.

Support keyboard activation.

Support Left Arrow and Right Arrow navigation.

Support Home and End where practical.

Keep focus visible.

Provide a no-script fallback with anchor navigation or visible sections.

### Responsive behavior

Make tables horizontally scrollable on narrow screens.

Keep body text readable without zooming.

Allow tab navigation to wrap or scroll.

Avoid fixed widths that clip content.

Use meaningful link text.

### Print behavior

Add print CSS.

Show every tab panel when printed.

Hide interactive-only controls when printed.

Avoid splitting table rows where practical.

Repeat table headers where supported.

Preserve URLs or source labels in the printed report.

Use a professional page title and footer.

### Executive summary content

Include:

- Decision requested.
- Product and market scope.
- Evidence cut-off.
- Top sourcing recommendations.
- Highest-priority IP risks.
- Critical missing information.
- Immediate actions.
- Preliminary-status and legal-review notice.

### Methodology content

Include:

- Inputs reviewed.
- Assumptions.
- Search tools and databases.
- Exact search date.
- Search strategy summary.
- Jurisdictions.
- Right types.
- Deduplication or family method.
- Legal-status method.
- Risk-rating definitions.
- Limitations.

## ZIP packaging

After validating the HTML, package it into a ZIP file when the environment permits and the user requested a file deliverable.

Use safe, explicit paths inside the working directory.

Do not overwrite an unrelated file.

Use a clear filename such as:

`automotive-lighting-sourcing-ip-assessment.html`

Use a matching archive name such as:

`automotive-lighting-sourcing-ip-assessment.zip`

Include only the deliverable files intended by the user.

Do not bundle secrets, raw API responses containing confidential data, caches, temporary files, or unrelated workspace content.

Tell the user where both files were written.

## Validation gate

Before delivery, verify all of the following.

### Source and scope

- The assessed product configuration is explicit.
- Target markets are explicit.
- Manufacturing and commercial acts are distinguished.
- Evidence and legal-status cut-off dates are present.
- Missing inputs and assumptions are visible.

### Engineering

- All relevant modules are represented.
- Component functions and interfaces are traceable.
- Make-versus-buy recommendations have stated criteria.
- Cost statements have a basis, currency, date, and volume context.
- Technical changes preserve regulatory and performance constraints or flag required validation.

### IP

- Every reported right has a verified identifier.
- Right type and jurisdiction are correct.
- EPO patents and EUIPO designs are not conflated.
- Utility models are limited to applicable jurisdictions.
- Status and status date are reported.
- Claims or registered design views were reviewed where required.
- Family relationships are considered.
- Invention and design analysis are separated.
- Jurisdiction-specific legal standards are not replaced by a universal rule.
- Unsupported branded-design claims are absent.
- Risk ratings follow the defined rubric.
- Legal conclusions are reserved for qualified counsel.

### Evidence

- External factual claims have sources.
- Links resolve or are marked unavailable.
- User facts, retrieved facts, inference, and assumptions are distinguished.
- No patent number, design number, status, owner, supplier, or cost was invented.
- Search limitations and unavailable MCP calls are disclosed.

### Visual and accessibility

- HTML is valid enough to open locally.
- The document language is English.
- Tabs work with mouse and keyboard.
- Focus is visible.
- All sections appear in print.
- Tables remain usable on narrow screens.
- Risk is understandable without color.
- No gradients, decorative dashboard clutter, or emoji-only markers remain.
- Captions, units, sources, and cut-off dates are present.

### Packaging

- The HTML opens before zipping.
- The ZIP contains the intended report.
- The archive contains no secrets or temporary artifacts.
- The reported paths exist.

## Failure modes

If no image is available for a design review, do not claim that `design_fto` was executed.

If only one view is available, state the view limitation.

If the MCP server is unavailable, deliver a documented search plan rather than synthetic results.

If legal status cannot be verified, use `Status unverified`.

If claims are unavailable, do not assign a claim-coverage conclusion.

If registered design views are unavailable, do not assign a design-similarity conclusion.

If the target market is unknown, do not present a global clearance conclusion.

If cost data is unknown, do not manufacture a make-versus-buy cost ratio.

If a supplier relationship or license is unknown, state it as an open diligence item.

If the user requests a legal opinion, explain the preliminary nature of this workflow and recommend qualified counsel.

## Final response

Lead with the decision-relevant findings.

State the product and jurisdiction scope.

State whether live patent and design searches were executed.

State the evidence cut-off date.

State the highest-priority unresolved issue.

Link the HTML and ZIP files when created.

End with the preliminary-screening limitation and the next decision gate.
