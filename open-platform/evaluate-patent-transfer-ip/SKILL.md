---
name: evaluate-patent-transfer-ip
description: Evaluate a patent package for licensing, assignment, or collaboration opportunities; identify evidence-backed candidate counterparties; rank them with a transparent and sensitivity-tested rubric; propose diligence and outreach hypotheses; and generate a self-contained HTML transfer-intelligence brief. Use when a user provides patent identifiers and asks for patent commercialization, technology transfer, licensing candidates, acquisition candidates, partner identification, or an outreach-ready patent asset brief.
---

# Evaluate Patent Transfer Opportunities

## Purpose

Turn one or more patent identifiers into a traceable patent-package assessment,
candidate-counterparty screen, and decision-ready HTML brief for authorized internal
use. Support licensing, assignment, option, joint-development, field-of-use,
venture-contribution, and patent-pool hypotheses without representing any candidate
as willing, qualified, reachable, or certain to transact.

This skill does not provide patent valuation, legal advice, tax advice, sanctions or
export-control advice, antitrust advice, transaction authority, or permission to
contact an organization.

## Inputs

Collect or derive:

- `patent_identifiers`: required publication, application, grant, or database IDs;
- `asset_owner`: current asserted owner or authorized representative, if known;
- `industry_or_domain`: technical and commercial context;
- `transaction_objective`: license, assign, collaborate, option, pool, or explore;
- `jurisdictions`: relevant rights, markets, and counterparties;
- `field_of_use`: intended technical or market boundary;
- `candidate_constraints`: named organizations, exclusions, conflicts, or regions;
- `rubric`: user-approved dimensions and weights, if supplied;
- `report_date`: default to the current ISO date;
- `confidentiality`: handling and disclosure boundary; and
- `progress_data`: optional, user-supplied outreach or pipeline facts.

If patent identity, authority, transaction objective, or confidential-data boundary is
materially ambiguous, stop and request the missing input before live research.

## Verified PatSnap MCP services

Inspect the installed connector schema before use. Record connector key, operation,
material request parameters, retrieval date, record IDs, and limitations.

### Patent Briefing — required

- Connector key: `patent_briefing`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- Use for input-record bibliography, claims, description, family context, status,
  translations, and images exposed by the active contract.

### Advanced Patent Search — required

- Connector key: `advanced_patent_search`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`
- Use for technically similar records, classification searches, citing/cited-record
  discovery when supported, and candidate-organization patent sets.

### Deep Patent Mining — recommended

- Connector key: `deep_patent_mining`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-mining
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-mining`
- Use for technical problem, means, effect, component, material, process, and
  application-domain extraction when supported.

### Global Core Patent Database — recommended

- Connector key: `global_core_patent_database`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/core-patents
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/core-patents`
- Use for deeper family, citation, legal-event, challenge, litigation, license,
  assignment, and full-text/PDF evidence when exposed.

No verified global PatSnap MCP in this package supplies complete company profiles,
procurement, recruitment, financing, M&A, or news intelligence. For those signals:

1. use authorized user-supplied material; or
2. research current official company, regulator, procurement, court, funder, and
   credible-news sources when web access is authorized; or
3. mark the signal unavailable.

Do not claim that a generic corporate/news connector ran. Do not substitute an
unverified regional database or fabricate a source link.

## Evidence states

Use these states throughout:

| State | Meaning |
|---|---|
| `Observed` | Directly supported by a cited, dated source |
| `Corroborated` | Supported by at least two independent appropriate sources |
| `Inferred` | Reasoned interpretation from observed facts |
| `Unknown` | Required evidence is absent or inaccessible |
| `Contradicted` | Credible sources materially disagree |
| `Requires diligence` | A legal, commercial, technical, or ownership check is needed |

Never convert `Unknown` to zero or “no signal.”

## Step 1 — Resolve and assess the patent package

### Resolve identity and family

For every input:

1. determine identifier type and jurisdiction;
2. retrieve title, abstract, claims, description, classifications, applicant/owner,
   inventors where appropriate, priority, filing, publication, and grant dates;
3. identify family relationships under a declared definition;
4. choose representative publications without hiding jurisdiction-specific rights;
5. retrieve dated legal-status and legal-event signals;
6. record translations and text-version limitations; and
7. reconcile duplicates, conflicting records, and unresolved identifiers.

### Extract the technical proposition

Create a versioned technical profile:

- technical problem and operating context;
- solution principle and independent-claim features;
- components, relationships, materials, process, software, or control logic;
- reported effects and evidence location;
- product, application, and field-of-use relevance;
- alternative terminology, IPC/CPC groups, and exclusions; and
- limitations, dependencies, and implementation uncertainty.

Do not describe claim breadth from independent-claim count alone. Claim scope
requires claim construction and jurisdiction-specific legal review.

### Assess evidence dimensions

Use transparent indicators rather than a single “patent value” assertion:

| Dimension | Appropriate evidence and limitation |
|---|---|
| Technical coverage | Supported problem/solution/application breadth, not IPC count alone |
| Claim relevance | Claim-feature relationship to intended field, not a scope opinion |
| Family footprint | Declared family/jurisdiction measure and cutoff |
| Status | Dated database signal requiring official verification |
| Citation | Dated, age- and practice-sensitive attention proxy |
| Complementarity | Relationship among package assets and uncovered gaps |
| Evidence quality | Availability and clarity of claims/descriptions/translations |

Output a patent-package evidence card for every asset and a package-level synthesis.

### Pre-transaction rights gate

Before recommending outreach or a transaction path, identify whether evidence exists
for:

- current ownership and chain of title;
- authority to license or assign;
- co-owners, exclusive licensees, security interests, or other encumbrances;
- government, university, employee-invention, or sponsored-research obligations;
- field, territory, sublicensing, retained-right, and enforcement restrictions;
- pending challenges, litigation, prosecution, or maintenance events;
- export-control, sanctions, competition-law, privacy, and sector constraints; and
- tax, accounting, and valuation review needs.

Mark every unresolved item `Requires diligence`. Do not infer clear title from a
single database owner field.

## Step 2 — Identify candidate counterparties

### Candidate discovery paths

Build a broad candidate universe from:

1. applicants with technically similar patent disclosures;
2. forward/backward citation relationships where semantically meaningful;
3. organizations active in the same or complementary IPC/CPC and solution routes;
4. companies with products, R&D programs, standards activity, procurement, hiring,
   partnerships, financing, or public strategy relevant to the field;
5. existing supply-chain, channel, portfolio, or collaboration relationships; and
6. licensees, assignees, acquirers, aggregators, research organizations, or pools
   appropriate to the transaction objective.

Resolve parents, subsidiaries, acquired entities, former names, transliterations,
and ambiguous names. Preserve the legal entity actually supported by the evidence.

### Interpret signals cautiously

These source signals are ambiguous:

- a rejected application does not prove a capability gap or demand;
- an invalidation or opposition does not prove a defensive licensing need;
- litigation does not prove willingness to license or infringement exposure;
- co-filing does not prove general openness to collaboration;
- recruitment does not prove inability or transaction budget;
- procurement does not necessarily cover the patented solution;
- financing does not prove available funds or acquisition intent;
- citation/classification overlap does not prove technical or commercial fit; and
- geographic proximity does not establish feasibility.

Report the observed event, source, date, entity, relationship to the asset, alternative
interpretations, and confidence. Do not assign urgency from the event alone.

### Candidate rubric

Use a user-approved rubric. If no weights are provided, propose and disclose a neutral
starting point; do not hard-code the source’s 40/40/20 split.

Recommended dimensions:

| Dimension | Example subfactors |
|---|---|
| Technical fit | Problem, route, product, field-of-use, complementary capability |
| Evidence of need | Dated product/R&D/procurement/hiring/event signals with ambiguity |
| Strategic fit | Portfolio gap, roadmap compatibility, ecosystem relationship |
| Transaction feasibility | Entity, geography, transaction history, resource indicators |
| Rights fit | Jurisdiction, term/status, field, ownership, encumbrance constraints |
| Engagement feasibility | Existing relationship, authorized channel, conflict constraints |
| Evidence quality | Coverage, freshness, independence, and unresolved contradictions |

For every factor define scale, direction, evidence requirement, missing-data treatment,
and disqualifying conditions. Normalize only comparable measures.

### Sensitivity and ranking rules

1. Show raw evidence before score.
2. Expose weights and calculations.
3. Keep unknown values distinct from low values.
4. Recalculate under plausible alternative weights.
5. identify rank changes and dominant assumptions.
6. Apply hard diligence gates separately from score.
7. Select as many candidates as evidence warrants; do not force a Top 3–5.
8. Call the result a research priority, not probability of transaction.

### Candidate profile

For each prioritized organization include:

- resolved legal entity and corporate relationship;
- candidate role: licensee, assignee, collaborator, option holder, pool participant,
  distributor/integrator, or other;
- technical-fit evidence;
- observed need or timing signals with dates and sources;
- strategic/transaction fit;
- conflicts, uncertainty, and diligence requirements;
- rubric score/range and sensitivity result; and
- evidence-backed next research action.

## Step 3 — Develop action hypotheses

For each candidate, propose options rather than directives.

### Transaction structures

Consider:

- non-exclusive or exclusive license;
- field-of-use or territory-limited license;
- assignment;
- evaluation or option agreement;
- joint development or research collaboration;
- contribution to a joint venture or spinout;
- cross-license where reciprocal rights are relevant; and
- patent pool or standards-related structure only with specialist review.

Explain fit, dependencies, rights/diligence gates, and alternatives. Do not recommend
enforcement threats or imply infringement as a negotiation tactic.

### Engagement hypothesis

Record:

- approved contact function, such as licensing/business development, R&D, product,
  corporate strategy, or IP;
- evidence-based value proposition;
- factual and non-accusatory opening topic;
- disclosure level and NDA requirement;
- internal owner and approval required;
- suggested timing linked to a verified event or business cycle; and
- fallback if the observed signal is wrong.

Do not generate or send outreach without explicit user authorization. Do not identify
personal contact information unless necessary, lawful, authorized, and sourced.

### Timing language

Use exact dates and calibrated language. Replace “urgent,” “this week,” or “high” with
a dated monitoring or action window supported by evidence. A prosecution rejection,
lawsuit, financing announcement, or recruitment post is not automatically a negotiation
window.

## Step 4 — Generate the HTML brief

Produce one fully populated self-contained `.html` file. Template tokens below are
implementation guidance; no `{{...}}` token may remain in the delivered report.

### Required sections

1. Header: title, owner, domain, date, confidentiality, scope, and cutoff.
2. Executive decision summary: findings, limitations, and next gates.
3. Patent-package evidence: asset cards and package-level indicators.
4. Key observed events: date, entity, source, fact, interpretation, confidence.
5. Candidate-counterparty profiles: role, fit, signals, score, uncertainty, diligence.
6. Action hypotheses: transaction option, contact function, value proposition, gate.
7. Progress and ownership: only user-supplied targets/actions; otherwise show
   “No authorized outreach-progress data supplied.”
8. Method and score sensitivity.
9. Source and evidence register.
10. Limitations and legal/commercial diligence notice.

### Scientific and executive design

- Use system fonts (`Arial`, `Helvetica`, `sans-serif`) and no remote font.
- Use neutral page/surface colors, navy hierarchy, restrained teal emphasis, amber
  qualification, and red only for a genuine escalation gate.
- Use semantic headings, tables, lists, links, and evidence-state text.
- Avoid emoji, decorative hero sections, gradients, stock images, and nested cards.
- Pair any score with the rubric and sensitivity result.
- Use safe, responsive tables and print styles.
- Escape all retrieved/user content and allow only `https` links from verified hosts.
- Use `rel="noopener noreferrer"` for links opened in a new tab.
- Do not load scripts, styles, images, trackers, fonts, or frames from a CDN.
- Do not claim that PatSnap or another platform endorses the analysis.

### Localized HTML blueprint

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>[Patent Package] — Transfer Opportunity Brief</title>
  <style>
    :root {
      --page: #f4f6f8; --surface: #fff; --ink: #17212b;
      --muted: #52606d; --rule: #d5dce3; --navy: #17365d;
      --teal: #087f8c; --amber: #9a6700; --risk: #b42318;
    }
    * { box-sizing: border-box; }
    body { margin: 0; background: var(--page); color: var(--ink);
      font: 14px/1.55 Arial, Helvetica, sans-serif; }
    main { max-width: 1080px; margin: 0 auto; padding: 32px; background: var(--surface); }
    header { border-bottom: 3px solid var(--navy); padding-bottom: 20px; }
    h1 { margin: 0 0 8px; font-size: 30px; line-height: 1.2; }
    h2 { margin-top: 32px; font-size: 21px; color: var(--navy); }
    h3 { font-size: 16px; }
    .meta, .scope { display: grid; grid-template-columns: repeat(3,minmax(0,1fr));
      gap: 10px; color: var(--muted); }
    .kpis { display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: 12px; }
    .kpi, .record { border: 1px solid var(--rule); padding: 14px; }
    .kpi strong { display: block; color: var(--navy); font-size: 24px; }
    table { width: 100%; border-collapse: collapse; }
    th, td { border-bottom: 1px solid var(--rule); padding: 9px; text-align: left;
      vertical-align: top; }
    th { background: #eef2f6; color: var(--navy); }
    .scroll { overflow-x: auto; }
    .state { font-weight: 700; }
    .observed { color: var(--teal); }
    .inferred, .unknown { color: var(--amber); }
    .diligence { color: var(--risk); }
    .notice { border-left: 4px solid var(--amber); padding: 10px 14px;
      background: #fff8e6; }
    a { color: #145ea8; overflow-wrap: anywhere; }
    footer { margin-top: 36px; border-top: 1px solid var(--rule); padding-top: 14px;
      color: var(--muted); }
    @media (max-width: 760px) { main { padding: 18px; }
      .meta, .scope, .kpis { grid-template-columns: 1fr; } }
    @media print { body { background: #fff; } main { max-width: none; padding: 0; }
      a { color: inherit; text-decoration: none; } }
  </style>
</head>
<body><main>
  <header>
    <h1>[Populated title]</h1>
    <p>[Bounded decision purpose]</p>
    <div class="meta"><span>As of: [ISO date]</span><span>Owner: [verified]</span>
      <span>Confidentiality: [marking]</span></div>
  </header>
  <section aria-labelledby="summary"><h2 id="summary">Executive decision summary</h2>
    <div class="notice">Research screening only; complete required diligence before outreach or transaction.</div>
    [Populated findings and gates]
  </section>
  <section aria-labelledby="assets"><h2 id="assets">Patent package evidence</h2>
    <div class="kpis">[Supported package indicators]</div>[Populated asset evidence cards]
  </section>
  <section aria-labelledby="events"><h2 id="events">Observed events</h2>
    <div class="scroll"><table><thead><tr><th>Date</th><th>Entity</th><th>Observed fact</th>
      <th>Interpretation</th><th>State</th><th>Source</th></tr></thead><tbody>
      [Verified rows]</tbody></table></div>
  </section>
  <section aria-labelledby="candidates"><h2 id="candidates">Candidate counterparties</h2>
    [Populated profiles with role, evidence, score, sensitivity, uncertainty, diligence]
  </section>
  <section aria-labelledby="actions"><h2 id="actions">Action hypotheses</h2>
    [Populated options, internal owner, approval gate, timing basis, and fallback]
  </section>
  <section aria-labelledby="progress"><h2 id="progress">Authorized progress record</h2>
    [User-supplied progress or explicit unavailable state]
  </section>
  <section aria-labelledby="method"><h2 id="method">Method and sensitivity</h2>
    [Rubric, weights, missing-data policy, alternative-weight results]
  </section>
  <section aria-labelledby="sources"><h2 id="sources">Evidence register</h2>
    [Identifiers, titles, dates, URLs, access dates, evidence states]
  </section>
  <footer>[Limitations, diligence boundary, report version, and cutoff]</footer>
</main></body></html>
```

### Output integrity

- Replace every template marker with verified content or a visible unavailable state.
- Show actual asset, candidate, and prioritized-opportunity counts only.
- Do not invent an annual target, pipeline status, weekly event, or outreach progress.
- Explain rubric dimensions, weights, and missing-data handling in the report.
- Cite patent events and external signals with precise source URLs and dates.
- Use only URLs returned by or documented for the active global service; otherwise
  show the patent identifier and source without fabricating a deep link.
- Keep observations, inferences, options, and diligence requirements visually distinct.

## Quality gate

### Patent package

- Every input identifier is resolved or explicitly unresolved.
- Family, status, owner, claim, citation, and event data carry provenance and cutoff.
- Technical propositions cite source fields or passages.
- No claim-scope, validity, enforceability, value, or adoption conclusion is implied.

### Candidates and scoring

- Candidate legal entities and corporate relationships are resolved.
- Every signal has a date, source, fact, interpretation, and alternative explanation.
- No event is treated as proof of need, urgency, willingness, or budget.
- Rubric definitions, weights, missing-data policy, hard gates, and sensitivity are shown.
- The ranked output is called research priority, not transaction likelihood.

### Actions and diligence

- Transaction structures fit the objective and known rights.
- Ownership/authority, encumbrance, legal, commercial, regulatory, and tax gates are visible.
- Outreach is not generated or sent without explicit authorization.
- Personal data and confidential technical information stay within approved boundaries.

### HTML

- The file opens locally and contains no remote dependency or executable retrieved content.
- All template tokens are resolved.
- Navigation, headings, tables, links, responsive layout, and print layout work.
- Content is escaped and URLs are safe and verified.
- No fake event, progress, score, source, endorsement, or data timestamp remains.

## Stop conditions

Stop or narrow the work when:

- a patent identifier cannot be reliably resolved;
- the user cannot establish ownership/authority for transaction planning;
- the required global MCP or external source is unavailable;
- current status, ownership, claim, or event evidence is insufficient;
- a corporate/news signal lacks a precise credible source;
- confidential data cannot be processed within the approved environment;
- sanctions, export control, competition, privacy, or other specialist review is needed;
- the user requests unauthorized outreach; or
- a populated report would require invented data or unverified links.

Return the completed evidence, the missing requirement, the reason it matters, and the
specific next diligence step. Do not fill the gap with a plausible candidate profile.

## Configuration boundary

Live, evidence-backed output requires authorized access to the relevant global PatSnap
MCP connectors. Corporate, procurement, recruitment, financing, and news signals also
require authorized user material or current credible public-source research. If these
are unavailable, deliver only a clearly labeled analysis plan, candidate-discovery
method, rubric, and unpopulated report schema—not a purported transaction brief.

