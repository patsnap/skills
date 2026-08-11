---
name: conduct-patent-research-ip
description: Conduct an evidence-backed patent research program from a technical problem and preliminary solution through iterative patent searching, technology-route analysis, project novelty pre-screening, FTO-oriented risk screening, competitor monitoring, recent-publication surveillance, and self-contained HTML plus DOCX reporting. Use when a user asks for patent research, project-initiation novelty review, technical-route analysis, patent risk screening, competitor patent tracking, or a comprehensive patent-search report.
---

# Conduct Patent Research

## Purpose

Run a reproducible four-stage patent research workflow for IP professionals,
R&D engineers, project leaders, product teams, and strategy teams. Convert a
technical question and preliminary solution into traceable patent evidence,
bounded analysis, and decision-ready HTML and DOCX reports.

This skill performs research and screening. It does not provide a legal opinion,
patentability opinion, freedom-to-operate opinion, infringement conclusion,
validity conclusion, or commercial recommendation.

## Operating principles

1. Confirm the technical scope before live retrieval.
2. Search through complementary concept, solution, classification, organization,
   and citation paths.
3. Preserve query, source, date, count, family, and screening provenance.
4. Distinguish complete-population analysis from samples and selected records.
5. Distinguish patent disclosure from implementation, adoption, and performance.
6. Treat status, citation, family, litigation, and transaction data as dated signals.
7. Label facts, observations, inferences, recommendations, and legal-risk signals.
8. Use calibrated language and escalate dispositive legal questions to counsel.
9. Never fabricate a record, identifier, count, claim, status, URL, or quotation.
10. Preserve confidential inputs only within the user-authorized environment.

## Required global PatSnap services

Inspect the installed connector schema before calling any operation. Record the
connector key, operation, material request parameters, retrieval date, and result
limitations.

### Advanced Patent Search — required

- Connector key: `advanced_patent_search`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`
- Use for fielded query construction, iterative search, filters, reproducible
  result sets, and aggregations only where the live contract supports them.

### Patent Briefing — required

- Connector key: `patent_briefing`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- Use for selected-record bibliography, family context, legal-status context,
  claims, descriptions, translations, and images exposed by the live contract.

### Deep Patent Mining — recommended

- Connector key: `deep_patent_mining`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-mining
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-mining`
- Use for deeper technical problem, solution, effect, classification, material,
  process, and application analysis when supported.

### Global Core Patent Database — recommended

- Connector key: `global_core_patent_database`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/core-patents
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/core-patents`
- Use for deeper family, citation, legal-event, challenge, litigation, licensing,
  transfer, and full-text/PDF evidence where supported.

Do not copy any source-era regional operation name into a global MCP call unless the
active connector explicitly exposes that exact operation. Do not silently map an old
operation to a new one with different semantics.

## Stage 1 — Frame and confirm the research question

### Collect the core inputs

Obtain or derive:

1. `technical_problem` — the specific problem, failure mode, constraint, or need.
2. `preliminary_solution` — proposed technical means, principle, architecture,
   process, material, component, function, and differentiating features.
3. `target_product_or_process` — sufficiently concrete for later claim mapping.
4. `decision_objective` — route review, novelty pre-screen, FTO screening,
   competitor monitoring, recent-publication watch, or a combination.
5. `jurisdictions` — the patent offices and legal systems relevant to the decision.
6. `date_scope` — relevant prior-art, activity, monitoring, and data-cutoff dates.
7. `known_organizations` — optional competitors, partners, assignees, or owners.
8. `language_scope` — search languages, translations, transliterations, and known
   terminology limitations.
9. `deliverables` — HTML, DOCX, or both.
10. `confidentiality_boundary` — what may be sent to connectors or shown in output.

If the technical problem or preliminary solution cannot be derived, ask for the
missing information. Do not begin a novelty or FTO-oriented search from an
undefined invention or product.

### Build the confirmation card

Present a compact confirmation card:

```text
Research confirmation
Technical problem: [...]
Preliminary solution: [...]
Target product/process and maturity: [...]
Decision objective: [...]
Jurisdictions: [...]
Date and language scope: [...]
Organizations: [... or not specified]
Deliverables: [...]
Known limitations/confidentiality boundary: [...]
```

Require confirmation before a broad, costly, or legally sensitive live search.
If the user has already explicitly confirmed an equivalent written scope, record
that confirmation and proceed without repeating the question.

## Stage 2 — Search patents iteratively

### Decompose the question

Create a concept table covering:

| Dimension | Examples of content |
|---|---|
| Problem | Failure, bottleneck, constraint, unwanted effect |
| Solution principle | Mechanism, algorithm, chemistry, architecture, process |
| Structure or material | Component, relationship, composition, layer, geometry |
| Function | Operation or capability |
| Effect | Performance, safety, reliability, quality, efficiency |
| Product/application | System, use case, environment, user, industry |
| Exclusions | Homonyms, neighboring fields, irrelevant uses |
| Classification | Candidate IPC/CPC groups and definitions |

Expand concepts across relevant languages and technical synonyms. Preserve the
original technical meaning; do not translate a term into a broader commercial
phrase merely to increase hit count.

### Run complementary search paths

#### Path A — problem-oriented search

- Combine problem, context, effect, and technology anchors.
- Use title/abstract/claim/full-text fields only when the live schema documents them.
- Start with strong terms and add weaker synonyms in controlled recall branches.
- Sample results for false positives and near misses.

#### Path B — solution-oriented search

- Search the proposed mechanism, structure, process, material, function, and
  relationships among features.
- Separate indispensable features from optional embodiments.
- Test alternative terminology and functional language.

#### Path C — classification-assisted recall

- Identify candidate IPC/CPC codes from relevant results and official definitions.
- Search classification codes in parallel with text concepts.
- Do not equate a classification hit with substantive relevance.

#### Path D — organization supplement

- Resolve organization names, subsidiaries, historical names, transliterations,
  acquisitions, and uncertain aliases.
- Apply organization filters to the technical scope; do not use organization-only
  results as evidence of a technical landscape.

#### Path E — citation and family follow-up

- Trace backward citations for possible earlier disclosures.
- Trace forward citations as a dated attention signal, not a quality conclusion.
- Review family members for clearer text and jurisdiction context.
- Preserve which family member supplied each evidence passage.

### Verify search quality

After each material revision:

1. record query text or structured request;
2. record filters, date basis, jurisdiction, language, and family setting;
3. record raw count and retrievable-count limitation;
4. review a reproducible relevance sample;
5. review likely near misses or known relevant controls;
6. identify dominant noise sources and exclusion effects;
7. revise only with a recorded reason; and
8. keep the previous version for rollback.

Do not use a universal 60% relevance threshold or stop automatically after three
rounds. Set fit-for-purpose acceptance criteria. Stop when the scope is adequate,
further revision produces no material improvement, or the tool/data boundary is
reached; disclose the reason.

### Build the canonical result set

Combine accepted paths with explicit Boolean or structured-query logic. Deduplicate
under a declared publication, application, simple-family, or extended-family rule.
Preserve:

- `query_id` and version;
- search intent and exact query/request;
- connector and operation;
- execution date and data cutoff;
- raw and deduplicated counts;
- screening method and observed relevance;
- exclusions and known recall risks; and
- canonical record identifiers.

All population-level analyses must use verified complete retrieval or server-side
aggregations whose population and semantics are known. If only a candidate pool,
Top-K list, capped export, or stratified sample is available, label it accordingly.
Never present sample counts as the complete global population.

## Stage 3 — Select and conduct analytical dimensions

On first entry, present the available dimensions in plain English:

1. Technology-route analysis.
2. Project novelty pre-screen and innovation-space assessment.
3. FTO-oriented patent-risk screening and claim-feature charts.
4. Competitor patent monitoring.
5. Recent-publication watch.

Let the user select all or a subset. If the original request already identifies the
dimensions, proceed with those and state the selection.

## Dimension 1 — Technology-route analysis

### Objective

Identify and compare meaningful technical routes over a decision-relevant period,
then locate the proposed solution within that map.

### Method

1. Draft a versioned taxonomy with inclusion and exclusion rules.
2. Tag the population or an explicitly defined reviewed dataset.
3. Distinguish automated rule hits from analyst- or expert-validated tags.
4. Analyze trends using a declared priority, filing, or publication date.
5. Check recent years for publication lag.
6. Select representative patents using declared relevance and diversity criteria.
7. Read claims/descriptions for routes that support important conclusions.
8. Compare route benefits, limitations, dependencies, and evidence maturity.
9. Map the preliminary solution to one or more routes with uncertainty.

Do not force three to six routes or two to three patents per route. Use the number
supported by the technology and evidence.

### Output

For each route provide:

- definition and boundaries;
- technical means and operating principle;
- reported advantages and limitations;
- evidence strength and known trade-offs;
- representative publication/family identifiers;
- evidence locator and source link when verified; and
- relationship to the user’s preliminary solution.

## Dimension 2 — Project novelty pre-screen

### 2A. Competitor and neighboring disclosures

- Search named organizations and evidence-led additional organizations under the
  same technical scope.
- Normalize assignee identities and preserve uncertain aliases.
- List representative records with identifier, assignee, title, technical point,
  relevant date, evidence location, and source.

### 2B. Innovation-space assessment

Identify evidence-backed opportunities from:

1. problem gaps — unresolved failure modes, performance limits, or reliability;
2. multi-objective trade-offs — safety, cost, efficiency, quality, or sustainability;
3. new constraints — regulation, cybersecurity, interoperability, supply chain,
   environment, or accessibility;
4. alternative principles — materially different mechanisms or architectures;
5. cross-domain transfer — a proven concept from another technical field;
6. system integration — interactions among hardware, software, data, and process;
7. materials and manufacturing — new compositions, treatments, or processes; and
8. digital methods — sensing, control, models, predictive maintenance, or twins.

For every opportunity state the evidence, gap, hypothesis, dependency, and next
validation action. Do not manufacture three to five opportunities to satisfy a quota.

### 2C. Novelty pre-screen

Break the proposed invention into candidate claim features and combinations. For
each potentially anticipatory reference:

- verify the relevant public-availability or prior-art date;
- identify whether one reference discloses every material feature directly and
  unambiguously;
- identify the exact passage or claim supporting each disclosure;
- distinguish explicit, implicit, uncertain, and missing disclosure;
- avoid mosaicing multiple references into a novelty conclusion;
- record jurisdiction and applicable-law uncertainty; and
- route inventive-step/obviousness combinations to a separate analysis.

Use outcomes such as:

- `no single-reference anticipation observed in searched evidence`;
- `potential partial disclosure`;
- `potential single-reference anticipation concern`; or
- `unresolved — additional search or counsel review required`.

Never label the solution simply “novel,” “partly novel,” or “not novel” as a legal
conclusion. Limit closest-reference lists by relevance, not an arbitrary maximum.

## Dimension 3 — FTO-oriented risk screening

### Scope boundary

FTO is jurisdiction-, date-, claim-, product-, and fact-specific. This dimension
prioritizes patents for qualified legal review. It cannot establish infringement,
non-infringement, validity, enforceability, claim construction, or freedom to operate.

### 3A. Candidate screening table

Search for potentially relevant granted and pending claims in the target jurisdictions.
Group records by family without hiding jurisdiction-specific rights. Order for review:

1. apparently in-force granted claims in relevant jurisdictions;
2. pending applications with potentially relevant claims;
3. expired, lapsed, abandoned, revoked, or otherwise non-live records as technical
   or historical context when useful.

Use these columns:

| Field | Requirement |
|---|---|
| Review ID | Stable local identifier |
| Patent/publication | Verified identifier and link if returned/documented |
| Jurisdiction | Relevant right or application |
| Applicant/owner | Source value plus normalization status |
| Title | Source title |
| Status as of | Dated database signal and source |
| Relevant claim | Claim number and version/date |
| Potential overlap | Bounded description |
| Screening priority | High, medium, low, or unresolved under the rubric |
| Next action | Claim review, status verification, product fact gathering, counsel |

Do not use red/yellow/green alone. Pair color with text, and do not equate “active”
database status with enforceability or an infringement risk conclusion.

### 3B. Claim-feature chart

Start with claim 1 when it is the relevant independent claim, preserving the source
workflow’s default. Add other independent claims and material dependent claims when
they may cover the product/process or change the screening result.

Before charting:

1. retrieve the complete relevant claim text from a verified source;
2. record publication/grant version, jurisdiction, claim number, and retrieval date;
3. verify current status in an official register where the decision requires it;
4. obtain a sufficiently complete product/process description;
5. identify missing product facts; and
6. do not send confidential implementation details outside the authorized boundary.

Quote only the claim text necessary for the feature analysis and permitted by the
source/user context. Preserve exact wording for each limitation; do not paraphrase
the evidence column.

Use this chart:

| Claim limitation (verbatim) | Technical interpretation | Product/process evidence | Screening state | Source/notes |
|---|---|---|---|---|
| Exact limitation segment | Non-legal technical explanation | Verified implementation fact or unknown | Observed literal correspondence / possible equivalence issue / absent in supplied facts / unknown | Claim and product evidence |

Use `possible equivalence issue` only as a flag for counsel. Equivalence depends on
jurisdiction-specific law, claim construction, prosecution history, timing, and facts;
do not apply a universal function-way-result test as a dispositive rule.

Conclude with one of:

- `potential concern — counsel review prioritized`;
- `lower observed overlap under supplied facts — not an FTO conclusion`;
- `unresolved because product or claim evidence is incomplete`; or
- `pending-claim watch item — reassess after prosecution changes`.

For a pending application, place this notice before the chart:

> Pending-claim notice: The application is under examination and its claims may
> change, be rejected, or never grant. This chart is a monitoring aid based on the
> retrieved claim version and does not establish a present infringement risk.

### FTO quality checks

- Every relevant limitation appears once and remains traceable to the claim.
- Conjunctive relationships and dependencies are preserved.
- Product facts are sourced; assumptions and unknowns are explicit.
- Family members are not treated as interchangeable rights.
- Status is dated and jurisdiction-specific.
- The chart does not decide infringement, equivalence, validity, or FTO.
- Counsel escalation identifies the unresolved question and evidence package.

## Dimension 4 — Competitor patent monitoring

### With named organizations

1. Resolve parent, subsidiaries, historical names, acquisitions, transliterations,
   and ambiguous entities.
2. Apply the same technical and date scope to each organization.
3. Compare routes, activity, and representative recent disclosures.
4. Preserve filing strategy, family, and publication-lag qualifications.

### Without named organizations

Identify leading assignees in the verified result population. Do not split results
into “domestic Top 3” and “overseas Top 3” by default. Choose an organization set
that fits the global decision, disclose the selection rule, and avoid interpreting
patent count as market leadership.

### Recent period

Calculate a rolling or calendar period dynamically from the current date. State the
start/end dates and whether priority, filing, or publication date is used. Never copy
the source’s static `20250101–20261231` example.

### Output

For each organization provide the resolved name set, scope count, route distribution,
recent representative records, evidence-backed observations, uncertainties, and
monitoring triggers. Treat patents as disclosed technical activity, not proof of a
future product or corporate strategy.

## Dimension 5 — Recent-publication watch

1. Calculate the requested lookback dynamically; use three months only when the
   user accepts or requests it.
2. Filter on publication date, not filing date.
3. Search within the canonical technical scope and add recall branches as needed.
4. Screen technical relevance and potential claim relevance separately.
5. Retrieve claims/status for prioritized records where available.
6. Deduplicate family members without hiding jurisdiction-specific applications.
7. Record the monitoring cutoff and next refresh date.

Use columns for publication identifier, applicant, publication date, title, technical
point, relevant claim or evidence, screening rationale, uncertainty, and next action.
Call these “recent potentially relevant publications,” not “new high-risk patents,”
unless a qualified legal review supports stronger wording.

## Stage 4 — Produce the report

Generate self-contained HTML first and a content-equivalent DOCX when requested and
the environment supports safe document creation. If document tooling is unavailable,
state the limitation; do not create a fake `.docx` by renaming another format.

### Report architecture

1. Project and research scope.
2. Technology-route analysis.
3. Project novelty pre-screen.
   - 3.1 Competitor and neighboring disclosures.
   - 3.2 Innovation-space assessment.
   - 3.3 Single-reference novelty pre-screen.
4. FTO-oriented patent-risk screening.
   - 4.1 Prioritized candidate table.
   - 4.2 Claim-feature charts and bounded screening outcomes.
5. Competitor patent monitoring.
6. Recent-publication watch.
7. Conclusions, next actions, and limitations.

Appendices:

1. Search objectives, concepts, synonyms, classifications, and exclusions.
2. Query log with intent, exact request, filters, execution date, raw/deduplicated
   counts, screening result, and revision rationale.
3. Patent evidence register with identifier, dates, title, abstract or bounded
   summary, technical problem, means, effect, family/status provenance, source,
   evidence locator, and review state.

Include only selected dimensions, but preserve numbering or explain omitted sections
so HTML and DOCX remain aligned.

### Evidence labels

Use:

- `F1` — direct patent/database fact;
- `O1` — observed dataset pattern;
- `I1` — analytical inference;
- `R1` — business/R&D recommendation; and
- `L1` — legal or risk-screening signal requiring qualified review.

Connect every material finding to evidence-register IDs. Do not use `[S#]` labels
without a defined register mapping.

### Patent identifiers and links

Every displayed patent identifier must be traceable. Apply these rules:

1. Preserve the publication/application/grant identifier exactly.
2. Use a global PatSnap record URL only when the active connector returns it or
   current official documentation defines a stable construction method.
3. Otherwise show the identifier, source connector/operation, and evidence-register
   ID without inventing a URL.
4. Do not use a legacy regional portal, an unverified UUID, or an undocumented
   patent-number URL template.
5. Validate URL scheme and host before rendering.
6. Add `rel="noopener noreferrer"` to external links opened in a new tab.
7. Keep HTML and DOCX link destinations identical.

### HTML specification

- Produce one self-contained HTML file with embedded CSS and necessary static data.
- Use semantic `header`, `nav`, `main`, `section`, `table`, and `footer` elements.
- Use a compact responsive navigation; do not require a fixed 220 px sidebar.
- Show scope, data cutoff, unit, selected dimensions, and legal boundary near the top.
- Use restrained neutral, navy, and teal colors suitable for scientific/executive work.
- Pair status and priority color with visible text.
- Include accessible headings, table headers, focus states, and chart alternatives.
- Prefer HTML/CSS/SVG that remains readable in print and without JavaScript.
- Escape all retrieved/user content and allow only safe verified links.
- Do not load remote scripts, fonts, trackers, iframes, or CDN assets.
- Show unavailable data explicitly; never render a plausible placeholder chart.
- Use responsive overflow for wide claim charts and patent tables.
- Include print styles and verify page breaks for tables and evidence cards.
- Do not include costs unless the user explicitly requests an authorized cost analysis.

### DOCX specification

- Match the HTML scope, findings, evidence IDs, tables, qualifications, and links.
- Use native headings, tables, captions, page breaks, headers/footers, and hyperlinks.
- Keep claim text and product evidence columns readable in landscape pages when needed.
- Include document title, version, data cutoff, confidentiality marking if supplied,
  and page numbers.
- Do not embed remote assets or hidden external content.
- Render and visually inspect the document when document tooling is available.

## Patent-search field guidance

The source names fields such as `TACD_ALL`, `TAC_ALL`, `PA`, `IPC`, `CPC`, `APD`,
and `PBD`. Treat these as PatSnap product syntax candidates, not universal MCP
parameters.

| Intent | Candidate field concept |
|---|---|
| Broad technical text | Title, abstract, claims, and description/full text |
| Focused technical text | Title, abstract, and claims |
| Organization | Applicant/assignee/owner with entity-resolution policy |
| Classification | IPC and CPC |
| Filing period | Filing/application date |
| Publication period | Publication date |
| Priority period | Earliest priority date where supported |

Inspect the live schema and use its documented parameter names. Record any semantic
difference between the requested field and the available implementation.

## Data-integrity rules

- Reconcile raw, deduplicated, analyzed, sampled, and reported counts.
- Do not claim global completeness without a verified population boundary.
- If retrieval is capped, use server-side aggregations or label sampled estimates.
- Stratify samples by relevant year, classification, jurisdiction, or organization;
  disclose weights and uncertainty.
- Do not require twenty evidence-register records when fewer are relevant.
- Keep publication, application, grant, and family identifiers distinct.
- State family definition and representative-publication rule.
- Date status, citation, ownership, litigation, and transaction fields.
- Treat missing connector data as unavailable, not negative evidence.
- Preserve translated-text status and inspect machine translation for key findings.
- Record source and evidence location for every quoted claim or technical statement.

## Report quality gate

### Scope and search

- Required inputs are complete and confirmed.
- At least two complementary search paths were considered; any omitted path is explained.
- Query versions, filters, counts, and screening decisions are reproducible.
- Known-relevant and near-miss controls were considered where available.
- The population/sample boundary is visible in every relevant conclusion.

### Technology and novelty

- Route labels have definitions, boundaries, and representative evidence.
- Rule-hit and validated tags are distinct.
- Innovation opportunities contain evidence and a next validation step.
- Novelty pre-screen uses relevant dates and single-reference logic.
- No legal patentability conclusion is stated.

### FTO screening

- Candidate rights are jurisdiction- and status-specific.
- Every relevant claim limitation is represented in each chart.
- Product facts, assumptions, and unknowns are separated.
- Pending claims carry the pending-claim notice.
- The outcome is a screening priority, not infringement or FTO advice.

### Monitoring

- Organization aliases and unresolved identities are documented.
- Recent periods are dynamic and exact dates are shown.
- Publication lag and family duplication are addressed.
- Patent activity is not represented as product-launch certainty or market share.

### Deliverables

- HTML opens locally with no remote dependency, broken navigation, or unsafe content.
- DOCX, if requested, matches the HTML and passes render review.
- Every identifier and URL is verified and traceable.
- Every material conclusion maps to evidence.
- Limitations and counsel-review boundaries are prominent.

## Stop conditions

Stop or narrow the work when:

- the technical problem or proposed solution remains undefined;
- confidential details cannot be shared safely with the required connector;
- the active MCP is unavailable or lacks the necessary field/operation;
- a complete-population claim cannot be supported;
- claim text, claim version, product facts, or status is insufficient for charting;
- a stable global record URL cannot be verified;
- official-register or counsel input is required for a dispositive conclusion; or
- the requested output would require fabricated data, legal certainty, or hidden assumptions.

Return the completed work, missing requirement, attempted method, residual risk, and
specific next action. Do not fill the gap with plausible text.

## Prohibitions

- Do not search before scope confirmation when material ambiguity remains.
- Do not analyze only Top-K records while describing the result as the full population.
- Do not fabricate patent numbers, claims, statuses, counts, sources, or links.
- Do not hide capped retrieval or sampling.
- Do not conflate publication, application, grant, and family records.
- Do not treat an “active” status label as an enforceability conclusion.
- Do not decide novelty, inventive step, validity, infringement, equivalence, or FTO.
- Do not use claim 1 as the only claim when another claim is materially relevant.
- Do not paraphrase claim language in the verbatim-evidence column.
- Do not mark a missing product fact as a missing claim limitation.
- Do not treat pending claims as granted rights.
- Do not rank pending applications ahead of relevant in-force granted claims without
  explaining a different monitoring purpose.
- Do not use fixed source dates for “last year” or “last three months.”
- Do not split competitors into domestic and overseas groups unless the decision
  specifically requires a defined geography comparison.
- Do not use any Zhihuiya/Eureka URL in the localized package.
- Do not create a PatSnap deep link from an unverified identifier or UUID.
- Do not expose secrets, API keys, confidential invention details, or personal data.
- Do not load remote report dependencies or execute retrieved content.

## Configuration boundary

This skill requires the relevant global PatSnap MCP connectors and authorized access
for live patent evidence. If they are unavailable, provide only a clearly labeled
research plan, query design, data schema, and report framework. Do not claim that a
search, status check, claim retrieval, or evidence-backed analysis was completed.
