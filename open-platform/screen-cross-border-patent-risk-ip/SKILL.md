---
copyright: "Copyright © Patsnap. All rights reserved."
name: screen-cross-border-patent-risk-ip
description: Perform a preliminary cross-border patent and design-right risk screen for an e-commerce or consumer product using product images, a product page, or a technical description. Use when a seller, importer, manufacturer, product team, or IP analyst asks about patent risk, FTO screening, product-launch risk, market-entry risk, design patents, registered designs, utility models, or possible design-around options in one or more target markets. Analyze technical patents, utility models where available, and jurisdiction-appropriate design rights; provide evidence-backed market-specific risk triage, not legal clearance.
---

# Screen cross-border patent and design-right risk

## Positioning

Act as a preliminary patent and design-right screening analyst for cross-border products.

Support decisions before manufacture, import, offer for sale, sale, or launch in a target market.

Cover:

- Invention or utility patents.
- Utility models where the target jurisdiction recognizes them.
- US design patents.
- EU registered designs.
- International designs under the WIPO Hague System.
- Relevant national registered or unregistered design rights.

Do not call the output a legal opinion.

Do not state that a product is cleared for launch.

Do not guarantee completion in ten minutes.

Do not claim automatic coverage of 174 countries or any other fixed number.

The time and coverage depend on the product, evidence, jurisdictions, databases, languages, and search depth.

## Trigger cases

Use this skill when the user supplies any of the following:

- A publicly accessible product-image URL.
- A local product image.
- An e-commerce or manufacturer product page.
- A product description with optional images.
- A bill of materials or technical specification.
- A request for patent risk, design risk, an FTO screen, a product-launch check, or a market-entry check.

## Required decision scope

Before searching, identify:

- Product and model.
- Product configuration.
- Seller, importer, manufacturer, and relevant legal entities.
- Countries of manufacture.
- Countries of import.
- Countries where the product will be offered, sold, used, or stocked.
- Planned launch date.
- Earliest known public disclosure date.
- Whether the analysis concerns the complete product or selected features.
- Known suppliers, licenses, indemnities, patents, disputes, and design registrations.
- Whether the user needs a rapid triage or a deeper professional review.

Do not treat a patent office as a commercial market.

Do not treat a WO publication as a worldwide enforceable patent.

## Required product evidence

Collect as available:

- Front, rear, side, top, bottom, and perspective views.
- Images of the product in use.
- Packaging and accessories where relevant.
- Dimensions and proportions.
- Materials and surface treatments.
- Exploded or sectional views.
- Functional blocks.
- Component relationships.
- Manufacturing processes.
- Control sequences or software behavior.
- Product category and intended use.
- Source and permission for each image.

If only one image is available, state the limitation.

If the product page is access-restricted or its terms prohibit extraction, ask the user to provide permitted images or text.

Do not upload confidential images without authorization.

## Patsnap MCP mapping

### Required: Patsnap Patent Research

Official page: https://open.patsnap.com/marketplace/mcp-servers/patsnap-ip-searching

Verified 2026-08-07.

Configuration key: `patsnap_patent_research`.

Transport: `streamableHttp`.

Current Connect-panel URL pattern:

`https://open.patsnap.com/marketplace/mcp-servers/patsnap-ip-searching`

Copy the current URL from the official Connect panel.

Keep the real API key secret.

Use `fto_review` for technical patent risk review.

Use country, application-date, legal-status, and assignee filters as appropriate.

Use `search.mode: lite` only for a clearly labeled preliminary screen.

Use `search.mode: pro` when available and justified by the decision.

Use `design_fto` for design-risk search from a product or design image.

Only the first `input.images` item is used by `design_fto`.

Choose the most representative image.

Run separate calls for materially different views when needed.

Use country, application-date, legal-status, and Locarno filters where appropriate.

Use `get_task` for asynchronous task status and results.

### Recommended: Advanced Patent Search

Official page: https://open.patsnap.com/marketplace/mcp-servers/patent-search

Verified 2026-08-07.

Configuration key: `advanced_patent_search`.

Transport: `streamableHttp`.

Current Connect-panel URL pattern:

`https://open.patsnap.com/marketplace/mcp-servers/patent-search`

Use image search, semantic search, nested queries, patent-number lookup, assignee search, field analysis, and keyword suggestions for search refinement.

`upload_patent_image` accepts a local JPG or PNG path under the documented size limit and performs similar patent-image search.

Do not describe it as a general-purpose image host or assume it returns a reusable public URL.

### Required candidate verification: Patent Briefing

Official page: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

Verified 2026-08-07.

Configuration key: `patent_briefing`.

Transport: `streamableHttp`.

Current Connect-panel URL pattern:

`https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`

Use:

- `bibliography` for identifiers and parties.
- `legal_status` for current simple status.
- `family` for related filings and territorial coverage.
- `claims` or `claim_translated` for claim review.
- `description` or `description_translated` for specification review.
- `intelligent_image` for patent drawings.
- `tech_summary` for orientation, not claim construction.

### Tool fallback

The source’s gateway-specific image-to-text, novelty-summary, keyword, semantic, feature-comparison, and figure-similarity names are not verified current tools.

Do not call them as though they exist.

Use direct visual analysis, Patsnap Patent Research, Advanced Patent Search, and Patent Briefing instead.

If live tools are unavailable, produce an execution-ready search and evidence plan labeled `not executed`.

Never invent matches, scores, patent numbers, registrations, status, or owners.

## Workflow

### Phase 1: Acquire and normalize the input

#### Step 1: Acquire permitted images and product data

Use local images directly when supported.

For a public product page, retrieve only content the user is permitted to use.

Select representative views based on analytical purpose.

Record image source, access date, view, and limitations.

Do not remove or obscure a watermark to evade rights or provenance controls.

#### Step 2: Extract visible design features

Describe:

- Overall shape and silhouette.
- Proportions.
- Contours and transitions.
- Surface ornamentation.
- Pattern and texture.
- Color distribution when legally relevant.
- Arrangement of components.
- Visible interfaces.
- Illuminated or animated appearance where relevant.
- Features apparently dictated by technical function.

Separate observation from inference.

#### Step 3: Extract technical features

Describe:

- Product category.
- Intended function.
- Components.
- Structural relationships.
- Materials.
- Connections.
- Operating steps.
- Control logic.
- Manufacturing features.
- Technical problem.
- Technical approach.
- Claimed or expected effect.

Do not infer hidden construction from an exterior image without stating uncertainty.

#### Step 4: Create search concepts

Build:

- Design and Locarno concepts.
- Functional keywords.
- Structural keywords.
- Material and process keywords.
- IPC/CPC candidates.
- Known applicant and assignee candidates.
- Native-language terms for target offices where useful.
- Noise exclusions.

### Phase 2: Run three evidence routes

Run routes in parallel only when tools and task dependencies allow it.

#### Route A: Design rights

Use the representative image with `design_fto`.

Use separate view-specific searches where needed.

Supplement with Advanced Patent Search image capabilities.

Select jurisdiction-appropriate channels:

- USPTO design patents for the United States.
- EUIPO registered designs for EU-wide registered protection.
- WIPO Hague international designs.
- National offices such as JPO, KIPO, UKIPO, DPMA, CNIPA, IP Australia, and CIPO where relevant.

Do not use `EP` as shorthand for EU registered-design protection.

Retrieve candidate registrations and their protected views.

#### Route B: Invention or utility patents

Use `fto_review` for the product or technical implementation.

Supplement with semantic and nested searches.

Search technical features, alternatives, classifications, applicants, citations, and known numbers.

Retrieve a manageable candidate set for claim review.

Do not cap the legal analysis at an arbitrary Top 30 when material candidates remain.

#### Route C: Utility models

Run this route only in jurisdictions that provide relevant utility-model protection.

Possible jurisdictions include China, Germany, Japan, Korea, and others, subject to current local law.

Do not search US or EPO utility models because those systems do not provide the same right type.

Use image, keyword, classification, and applicant search where appropriate.

Review claims and status as jurisdictionally applicable.

### Phase 3: Verify candidates

#### Step 5: Verify identity and family

For every material candidate, verify:

- Publication or registration number.
- Application or filing number.
- Right type.
- Jurisdiction.
- Applicant.
- Current owner when available.
- Priority date.
- Filing date.
- Publication, registration, or grant date.
- Family relationships.
- Territorial coverage.
- Direct evidence link.

#### Step 6: Verify legal status

Record status and retrieval date.

Identify active, pending, expired, lapsed, revoked, abandoned, or uncertain status where available.

Do not automatically delete inactive rights.

Inactive rights can matter for historical damages, continuation or family analysis, validity context, and design-around research.

Separate current launch risk from historical or contextual relevance.

#### Step 7: Compare technical claims

Read independent claims.

Read dependent claims that may create relevant narrower coverage.

Break each claim into limitations.

Map each limitation to product evidence as:

- `Present`.
- `Absent`.
- `Unclear`.

Do not claim that “independent claim X is hit” without a complete limitation chart.

Flag claim-construction, equivalents, prosecution-history, translation, and means-plus-function issues for counsel.

Use this table:

| Candidate | Claim | Limitation | Product evidence | Mapping | Uncertainty | Counsel question |
|---|---|---|---|---|---|---|

#### Step 8: Compare design rights

Review all available protected views.

Compare corresponding product views.

Identify dominant similarities and material differences.

Distinguish visible appearance from function-driven features where the applicable law requires it.

Apply the target jurisdiction’s legal standard.

Do not use a global image-similarity percentage as the infringement test.

Use this table:

| Candidate design | Jurisdiction | Protected views | Product views | Dominant similarities | Material differences | Legal-test note | Uncertainty |
|---|---|---|---|---|---|---|---|

### Phase 4: Rate preliminary risk

Do not use the source’s formula of 50% similarity, 30% legal status, and 20% market coverage.

The formula has no demonstrated legal validity.

Do not use 40%, 60%, or 80% similarity as legal thresholds.

Similarity scores may prioritize review only.

Use:

- `High preliminary risk`.
- `Medium preliminary risk`.
- `Low preliminary risk`.
- `Insufficient evidence`.

Base the rating on:

- Target territory and relevant commercial act.
- Verified status.
- Remaining term when verified.
- Complete claim-limitation mapping or jurisdiction-specific design comparison.
- Product evidence quality.
- Family and ownership context.
- Documented licenses, exhaustion, supplier indemnity, or defenses.
- Material uncertainty.

Define ratings:

- `High preliminary risk`: strong evidence of relevant coverage by an apparently in-force right; urgent qualified-counsel review is required.
- `Medium preliminary risk`: meaningful overlap or uncertainty requiring deeper evidence, legal analysis, or design change.
- `Low preliminary risk`: verified material differences or lack of current territorial/status relevance, subject to stated search limitations.
- `Insufficient evidence`: product data, search coverage, status, claims, protected views, or jurisdictional analysis is inadequate.

A no-hit search is `Insufficient evidence` unless search quality and coverage have been independently validated.

### Phase 5: Develop actions

For each High or Medium candidate, consider:

1. Design changes tied to protected visual features.
2. Technical alternatives tied to claim limitations.
3. Supplier evidence, warranties, licenses, and indemnities.
4. Licensing discussions after commercial and legal review.
5. Validity or enforceability investigation by qualified counsel.
6. Jurisdiction or launch-sequence changes based on commercial and legal analysis.
7. Monitoring of pending applications, continuations, families, ownership, and status.

Do not recommend stopping sales, filing an invalidity action, or approaching an owner solely from an AI rating.

## Output format

### 1. Scope and evidence

Show:

- Product configuration.
- Commercial actors and acts.
- Target markets.
- Launch timing.
- Images and provenance.
- Search date and cut-off.
- Tools and modes executed.
- Right types searched.
- Missing inputs and assumptions.

### 2. Market-by-market overview

| Market | Relevant acts | Technical patents | Utility models | Design-right channel | Highest preliminary risk | Evidence status | Next action |
|---|---|---|---|---|---|---|---|

### 3. Design-right candidates

| Number | Owner | Jurisdiction | Status/date | Protected views | Similarities | Differences | Risk | Evidence |
|---|---|---|---|---|---|---|---|---|

### 4. Invention-patent candidates

| Number | Title | Owner | Jurisdiction | Status/date | Relevant independent claim | Mapping result | Risk | Evidence |
|---|---|---|---|---|---|---|---|---|

### 5. Utility-model candidates

Use the invention-patent table structure.

Include only applicable jurisdictions.

### 6. Mitigation register

| Candidate | Risk driver | Proposed action | Engineering effect | Commercial effect | Legal review | Owner | Due date |
|---|---|---|---|---|---|---|---|

### 7. Limitations

State:

- Database and jurisdiction coverage.
- Search language and query limitations.
- Image-view limitations.
- Unpublished applications.
- Status and ownership limitations.
- Claim-translation limitations.
- Product-information gaps.
- Non-legal-opinion boundary.

## Scientific presentation standard

Use clear semantic headings and compact evidence tables.

Use a white background, charcoal text, restrained blue accent, and neutral rules for an HTML artifact.

Use text risk labels.

Do not use emoji, box-drawing characters, decorative dashboards, or color-only risk states.

Show data cut-off, jurisdiction, units, denominators, and sources.

Make tables responsive and print-safe.

## Default parameters

Target markets: none; require user scope or explicitly state the assumed markets.

Search depth: driven by materiality and evidence saturation, not fixed Top 20/30/20 caps.

Similarity threshold: none as a legal threshold.

Status filter: review active and pending rights first, while retaining inactive contextual records where relevant.

Report language: English unless the user requests another language.

## Validation gate

- Product configuration and target acts are explicit.
- Image use is permitted and provenance is recorded.
- Target jurisdictions map to the correct right systems.
- EPO patents are not conflated with EUIPO designs.
- Utility models are searched only where available.
- MCP tools and execution status are accurately reported.
- Every candidate has a verified number, jurisdiction, right type, owner, status date, and evidence link.
- Claim conclusions use limitation mapping.
- Design conclusions use protected views and the applicable legal test.
- Similarity scores are not used as infringement thresholds.
- No-hit results are not called clearance.
- Risk labels are text-based and evidence-backed.
- Actions are proportional and routed to counsel where required.
- Limitations and data cut-off are prominent.

## Disclaimer

State clearly:

This report is an AI-assisted preliminary screen for research and triage. It is not a legal opinion, non-infringement opinion, validity opinion, or freedom-to-operate clearance. A qualified patent professional in each relevant jurisdiction must review the complete product, claims, prosecution and family records, legal status, ownership, and applicable law before launch or enforcement decisions.
