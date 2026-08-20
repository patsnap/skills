---
copyright: "Copyright © Patsnap. All rights reserved."
name: create-company-patent-profile-ip
description: Create an evidence-backed executive company patent-strategy report in a continuous-scroll HTML format. Use when a CEO, general manager, board, strategy team, R&D leader, or IP team needs an eight-part profile covering executive findings, company and product context, technical strengths, competitive landscape, market opportunities, core risks, strategic recommendations, and—only when approved current materials are supplied—an aligned Patsnap solution section. Bind every material claim to patent, literature, standard, policy, company, or market evidence and label unsupported claims Unverified.
---

# Create an executive company patent profile

## Purpose

Create a data-supported patent-strategy report for senior decision-makers.

Help executives understand the company’s patent assets, technical position, competitive context, opportunities, risks, and actionable priorities.

Use a conventional continuous-scroll report.

Do not use a slide-by-slide presentation format.

Bind every material claim to traceable evidence.

Label unsupported claims `Unverified`.

## Evidence boundary

Patents can support claims about disclosed inventions, applicants, dates, families, claims, status, and filing behavior.

Patents alone do not prove:

- Product performance.
- Production capacity.
- Customer deployment.
- Revenue.
- Market size.
- Market share.
- Regulatory compliance.
- Team credentials.
- Commercial partnership.
- Product availability.
- Current pricing.

A joint patent application can indicate joint filing.

It does not by itself prove a deployed customer case or commercial success.

A highly cited paper is not automatically reliable, applicable, current, or independent.

Use citations as context rather than a quality threshold.

## Report structure

Preserve eight parts.

| Part | Title | Core content | Primary evidence |
|---|---|---|---|
| 1 | Executive summary | Position, strengths, observed standing, conclusion, key metrics | Verified portfolio and external evidence |
| 2 | Company and product context | Company facts, products, capacity, delivery, selected deployments | Company filings, official materials, standards, verified joint records |
| 3 | Technical strengths | Technical barriers, performance evidence, cases, team credentials | Patents, claims, literature, tests, standards |
| 4 | Competitive landscape | Domestic and international competitors, route comparison | Entity-resolved competitor patent data and external sources |
| 5 | Market opportunities | Policy, applications, market evidence, opportunity priorities | Official policy, standards, market research, patent signals |
| 6 | Core risks | Technical, cost, adoption, competition, IP, regulation and response | Evidence by risk type |
| 7 | Strategic recommendations | Prioritized objectives, steps, patent basis and roadmap | Findings from Parts 1–6 |
| 8 | Optional Patsnap solution alignment | Current approved solution modules mapped to evidenced needs | User-supplied approved commercial materials |

## Required inputs

Collect before research:

- Company legal name in English.
- Original-language legal name where relevant.
- Former names, subsidiaries, parent entities, acquisitions, and brands.
- Industry and value-chain position.
- Main technology directions: preferably three to five.
- Known domestic and international competitors.
- Target jurisdictions and markets.
- Target audience.
- Decision to be supported.
- Reporting period and evidence cut-off.
- Counting unit and family definition.
- Confidential company materials the user authorizes for use.
- Approved Patsnap solution materials if Part 8 is required.

The Chinese source names six commercial slide decks, but none is included in the frozen package.

Do not fabricate or reconstruct those decks.

Do not publish commercial claims attributed to them unless the user supplies approved current versions.

## Patsnap MCP

### Required: Advanced Patent Search

Official page: https://open.patsnap.com/marketplace/mcp-servers/patent-search

Verified 2026-08-07.

Configuration key: `advanced_patent_search`.

Transport: `streamableHttp`.

Current Connect-panel URL pattern:

`https://open.patsnap.com/marketplace/mcp-servers/patent-search`

Use documented tools for:

- Original-applicant search.
- Current-assignee search.
- Nested-query retrieval.
- Semantic retrieval.
- Counts.
- Field distributions.
- Patent-number verification.
- Keyword suggestions.
- Similarity expansion when needed.

### Recommended: Patent Briefing

Official page: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

Verified 2026-08-07.

Configuration key: `patent_briefing`.

Transport: `streamableHttp`.

Current Connect-panel URL pattern:

`https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`

Use bibliography, family, legal status, claims, translated claims, descriptions, translated descriptions, drawings, and technical summaries for representative records.

### Other evidence

Use authoritative company sources for company and product facts.

Use official government or standards sources for policy and standards.

Use current, credible market sources for market size and forecasts.

Use primary literature for performance and mechanism claims where possible.

Do not present patent search results as market-size or policy evidence.

If live tools are unavailable, provide an evidence plan and report shell labeled `not executed`.

## Workflow

### Step 0: Confirm scope and evidence

Restate:

- Company and resolved entities.
- Industry and technology scope.
- Competitors.
- Jurisdictions.
- Audience and decision.
- Period, cut-off and date basis.
- Counting unit and family definition.
- Supplied internal sources.
- Part 8 availability.

Create an evidence register with:

| Evidence ID | Claim supported | Source type | Source | Date | Direct/inferred | Confidence | Limitation |
|---|---|---|---|---|---|---|---|

### Step 1: Execute five research streams

#### Search 1: Company portfolio

Resolve applicants and assignees.

Retrieve total records under the declared counting unit.

Analyze patent types, families, status, dates, jurisdictions, technology fields, and representative patents.

Do not mix publications and families in one metric.

#### Search 2: Industry landscape

Use a documented broad technology query.

Retrieve enough data for a defensible view.

Do not treat Top 30 as exhaustive.

Identify observed technical themes and leading applicants under a stated sample and count method.

#### Search 3: Competitor portfolios

Search each competitor independently with comparable entity scope, time period, query and counting unit.

Use Top 15 only as an exploratory candidate set, not a complete portfolio.

Review representative claims and family context before stating technical positioning.

#### Search 4: Application scenarios

Search scenario-specific patents and external evidence.

Distinguish disclosed applications from demonstrated deployments.

#### Search 5: Literature and standards

Search performance, mechanism and benchmark evidence.

Do not select literature solely because it has at least 20 citations.

Assess relevance, method, sample, recency, independence, and limitations.

### Step 2: Bind claims to evidence

Use these minimum requirements:

| Claim type | Required evidence |
|---|---|
| Company patent count | Reproducible entity-resolved query, counting unit, date and result count |
| Joint filing | Verified bibliography naming both applicants; do not call it deployment proof |
| Performance comparison | Comparable independent tests, standards or literature with units and conditions |
| Competitor position | Representative patents plus broader portfolio evidence and uncertainty |
| Market-size number | Current traceable market source, scope, currency, base year and methodology |
| Policy driver | Official policy, regulation or standard; patents may illustrate response but not establish policy |
| Capacity or delivery | Current authoritative company or regulatory source |
| Commercial case | Direct case source and corroboration where material |

If evidence is missing, use:

`Unverified — owner: [role]; required evidence: [source]; validation date: [date].`

Do not place an unverified number prominently without the label and limitation.

## Part 1: Executive summary

Use objective language.

Do not include the reader’s name or honorific in the title.

Use `Executive findings` or `Strategic summary`.

Organize four findings:

- Company position.
- Evidence-backed strengths.
- Observed competitive position.
- Decision implication.

Show up to four verified key metrics.

Each metric must include unit, period, counting basis, and source.

Do not use decorative quadrant colors as meaning.

Attach one or two evidence references to each finding.

## Part 2: Company and product context

Cover:

- Legal entity and ownership context.
- Qualifications and awards, individually sourced.
- Product portfolio.
- Product specifications with units and test conditions.
- Capacity and delivery only when verified.
- Selected customers or deployments only when independently supported.
- Joint applications as filing evidence, not deployment proof.

Use at least four product rows only when four products or configurations are verified.

Do not invent a product ladder to fill a table.

## Part 3: Technical strengths

Build a seven- or eight-dimension comparison only when the dimensions and data are comparable.

State:

- Metric definition.
- Units.
- Test or operating conditions.
- Source date.
- Missing values.
- Whether values are measured, claimed, modeled, or inferred.

Do not mark `Leading` solely through color.

Do not state a multiplier without showing numerator, denominator and comparable conditions.

Use at least two literature sources only when two relevant sources exist.

Quantify cases only with direct evidence.

## Part 4: Competitive landscape

Select three or four domestic competitors only when relevant to the scope.

Include international competitors selected by technology and market relevance.

Resolve legal entities consistently.

Compare:

- Technology routes.
- Patent activity.
- Family and jurisdiction behavior.
- Representative claims.
- Product or market evidence separately.

Do not exaggerate the company’s advantage.

Do not disparage alternative routes.

If routes serve different power, scale, cost, response, safety or application requirements, state that they may be complementary rather than direct substitutes.

## Part 5: Market opportunities

Use official sources for policy drivers.

Do not use a policy-related patent as proof that a policy exists.

Prioritize applications using stated criteria such as:

- Customer value.
- Regulatory support.
- Technical fit.
- Company capability.
- Evidence of adoption.
- Competitive intensity.
- IP exposure.
- Implementation dependency.

For market forecasts record:

- Source.
- Publication date.
- Base year.
- Forecast year.
- Currency.
- Geography.
- Product definition.
- Nominal or real values.
- Method limitation.

If absent, mark `Unverified` rather than inventing a number.

## Part 6: Core risks

Do not force every company into only cost, awareness and competition risks.

Assess relevant risks such as:

- Technical performance.
- Cost and scale-up.
- Manufacturing and supply.
- Customer adoption.
- Regulatory and standards.
- Competition.
- Patent and FTO exposure.
- Data or software dependency.
- Execution capability.

For each risk show:

| Risk | Evidence | Likelihood | Impact | Current controls | Proposed response | Owner | Confidence |
|---|---|---|---|---|---|---|---|

Use text labels and defined criteria.

When cost reduction creates a genuine technical trade-off, express the contradiction explicitly.

Do not invent a contradiction solely to sell a TRIZ service.

## Part 7: Strategic recommendations

Provide three prioritized recommendations when supported.

Possible categories include:

- Technical iteration.
- Scale-up and cost.
- Ecosystem partnership.
- Portfolio strengthening.
- Geographic filing.
- FTO and design-around.
- Evidence development.

For each recommendation include:

- Objective.
- Rationale.
- Evidence.
- Actions.
- Owner.
- Timing.
- Dependency.
- Existing patent basis.
- Success measure.
- Risk.

Use a three-phase roadmap only when it fits the decision.

Label revenue estimates `Unverified` unless supported by an approved financial model.

## Part 8: Optional Patsnap solution alignment

Include this part only when the user requests it and supplies current approved source materials.

Frame challenges as industry patterns unless company-specific evidence supports a company finding.

Do not use a generic pain point as a factual criticism of the subject company.

The source proposes three modules:

1. Patent landscape and portfolio-planning report.
2. TRIZ plus AI cost/performance problem solving.
3. FTO risk control and TRIZ-based design-around.

Preserve these as a provisional mapping framework.

Validate current names, scope, deliverables, claims, pricing, metrics and examples from approved materials.

### Module 1: Patent landscape and portfolio planning

The source outlines six logical chapters:

1. Inventory the current portfolio.
2. Map the technology field.
3. Analyze competitors.
4. Develop coverage options.
5. Review benchmark strategies.
6. Produce an action-priority list.

Localize examples to the client’s industry.

Do not reuse a historical CATL example without current evidence and relevance.

### Module 2: TRIZ and AI problem solving

The source outlines five steps:

1. Functional analysis.
2. Cause-and-effect analysis.
3. Trimming.
4. Technical or physical contradiction formulation.
5. Solution-direction generation.

Do not publish the source’s “2 solutions/30 days,” “20 solutions/3 days,” “10x” or workshop price claims without approved current evidence.

Use `Unverified commercial claim` when a placeholder is necessary.

### Module 3: FTO and design-around

The source outlines:

1. Claim and technical-feature decomposition.
2. Component or feature substitution.
3. Cross-domain search for alternatives.

Do not publish the source’s US litigation count or average-damages value without a current authoritative source, defined year, case set, currency and conversion basis.

Do not treat FTO screening as legal clearance.

### AI capability catalog

The source lists nine capabilities.

Treat the list as a source-era commercial inventory requiring current product confirmation:

1. Patent landscape map generation.
2. Technology-effect matrix analysis.
3. Competitor patent decomposition.
4. Claim-quality assessment.
5. PCT timing alerts.
6. TRIZ contradiction-matrix matching.
7. Functional-trimming suggestions.
8. FTO risk screening.
9. Design-around generation.

Do not claim permanent availability, deployment, entitlement or support without a current contract or product source.

### Implementation roadmap

The source proposes five phases:

1. Diagnose.
2. Plan.
3. Solve selected technical problems.
4. Develop and execute portfolio actions.
5. Institutionalize repeatable workflows and monitoring.

Localize schedule, owner, deliverable and dependencies.

Do not copy source-specific Week 1–2 or Month 6+ timing without feasibility review.

## HTML specification

Create one final self-contained HTML file.

Use eight semantic sections with stable anchors.

Use continuous vertical reading.

Use a responsive top or side navigation that does not obscure content.

Use a content width appropriate to tables and executive reading.

Use print CSS that hides navigation and prints every section.

Do not create eight physical part files unless the user explicitly approves additional files.

Use a safe workspace output path.

Use filename:

`[company-slug]-patent-strategy-report.html`

## Scientific executive visual standard

Use:

- White background.
- Charcoal text.
- Restrained blue accent.
- Neutral borders.
- English system fonts.
- Sentence-case headings.
- Accessible tables.
- Captions and source notes.
- Direct evidence links.
- Text-plus-color risk labels.
- Responsive layout.
- Print-safe styles.

Do not use:

- Dark gradient cover cards.
- Glow effects.
- Decorative quadrant colors.
- Oversized metric badges.
- Color-only `Leading` or risk states.
- Decorative cards without analytical purpose.
- Slide navigation controls.
- Pagination dots.

## Quality checklist

Before each part:

- Every material claim has an evidence ID or `Unverified` label.
- Industry patterns are not attributed to the company without evidence.
- Numbers include source, date, unit, scope and method.
- Patent links are verified and global.
- Competitor findings come from comparable searches.
- Executive titles contain no reader name or honorific.

Before final delivery:

- All eight anchors work.
- The report is continuous-scroll and white-background.
- Print preview includes every section without navigation overlap.
- Counting unit, family definition, date basis and cut-off are visible.
- Patents are not used as proof of market, policy, capacity or deployment claims.
- Joint filings are not called customer cases without additional evidence.
- Part 6 contradictions are evidence-based.
- Part 8 maps only to evidenced needs.
- Part 8 uses current approved commercial materials.
- Unsupported source-era pricing, litigation, damages, efficiency and capability claims are absent or explicitly unverified.
- No missing PPT or README is implied to exist.

## Common errors

| Error | Correction |
|---|---|
| Attribute a generic industry issue to the company | Use industry language or provide company-specific evidence |
| Use a slide-deck layout | Use one continuous-scroll executive report |
| Publish a market number without a source | Mark it Unverified and list the validation owner |
| Treat a joint patent as proof of deployment | State only the verified joint filing |
| Use a patent as policy proof | Cite the official policy or standard |
| State competitor performance from user memory | Verify comparable evidence and disclose conditions |
| Include a patent number without a link | Add a verified Patsnap or official record link |
| Force Part 8 into the conclusion | Include it only when requested and evidence-aligned |
| Recreate missing commercial decks | Ask for approved materials; do not fabricate |
| Publish source-era price or efficiency claims | Verify current approved evidence or omit |

## Output

Deliver one HTML file that opens directly in a browser.

Support browser printing to PDF.

Return a clickable path.

State evidence cut-off and unresolved `Unverified` items.
