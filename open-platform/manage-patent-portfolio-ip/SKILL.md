---
copyright: "Copyright © Patsnap. All rights reserved."
name: manage-patent-portfolio-ip
description: Design and generate a configurable single-file enterprise patent-portfolio operations workspace with a dashboard, asset register, fee/deadline view, outside-counsel analytics, competitor monitoring, FTO workflow intake, patent-value screening, and novelty-search intake. Use when a technology or life-sciences company wants a portfolio-management prototype, refreshed portfolio view, phased IP-operations roadmap, or HTML workspace based on authorized patent data.
---

# Manage a Patent Portfolio

## Purpose

Build a configurable enterprise patent-portfolio operations workspace from authorized evidence.
The primary deliverable is a self-contained HTML view plus a documented data and workflow contract.

The HTML deliverable is a portable report/prototype unless the user separately provides an approved backend.
It cannot by itself:

- store credentials securely;
- call MCP connectors;
- schedule fee or deadline reminders;
- persist payment or task changes;
- authenticate users;
- send notifications;
- perform FTO, valuation, or novelty analysis;
- write back to a docketing or source system.

Never simulate those capabilities with a progress animation or fabricated result.

## Target users

- in-house IP operations teams;
- patent portfolio managers;
- life-sciences and synthetic-biology companies;
- R&D legal and competitive-intelligence teams;
- companies planning a phased patent-management MVP.

## Trigger conditions

Use when the user asks to:

- build a patent-management workspace;
- create or refresh a portfolio dashboard;
- consolidate company patent assets and status;
- design fee/deadline, counsel, competitor, FTO, value, or novelty modules;
- iterate an existing portfolio HTML without losing records;
- define a phased patent-operations implementation roadmap.

## Required inputs

### Organization scope

- authorized legal entity or corporate group;
- subsidiaries, historic names, acquisitions, and aliases;
- effective dates for corporate relationships;
- inclusion and exclusion rules;
- portfolio owner and accountable reviewer.

### Patent scope

- authorities and jurisdictions;
- publication/application/grant identifiers;
- family and deduplication rule;
- application type and document-kind rules;
- status cutoff;
- portfolio-data source;
- whether unpublished applications are in scope.

### Operations scope

- modules required;
- user roles and permissions;
- source systems and writeback needs;
- fee/deadline authority and docketing workflow;
- refresh frequency;
- notification and approval process;
- retention, audit, privacy, and confidentiality rules;
- output location and version convention.

### Security gate

Do not transmit confidential unpublished inventions, product features, attorney work product,
API keys, billing data, or personal information to an unapproved connector or external service.

## Verified Patsnap MCP services

Use the English interface and English output.
Inspect the live tool schema before use.

### Required: Advanced Patent Search

- Connector key: `advanced_patent_search`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`
- Use: authorized portfolio retrieval and validation, entity-specific searches,
  competitor searches, and novelty-search evidence retrieval.

### Required: Patent Briefing

- Connector key: `patent_briefing`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- Use: bibliography, family, legal status, claims, description, translations, images,
  and concise technical summaries.

### Recommended: Global Core Patent Database

- Connector key: `global_core_patent_database`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/core-patents
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/core-patents`
- Use: deeper family, legal events, citations, litigation, licensing, transfer,
  reexamination/invalidation, full text, and PDF evidence where supported.

Patent MCPs do not provide authoritative fee instructions, billing status, secure writeback,
user authentication, task scheduling, or notifications.
Use official patent-office or authorized docketing evidence for fees and deadlines.

For each connector call record:

```text
connector_key
tool_name
request_id
query_or_identifier
filters
response_semantics
retrieval_timestamp
source_locator
limitations
```

## Product priority roadmap

Preserve the source complexity × value × data-maturity prioritization.

### P0 — Lightweight operational foundation

1. patent asset register and status refresh;
2. fee/deadline view and verified task handoff;
3. patent intelligence and competitor-monitoring register.

These modules establish source-of-truth, provenance, ownership, and review controls.

### P1 — Evidence-heavy analytical workflows

4. patent-value screening;
5. FTO screening intake and reviewed-report routing.

These modules must not present automated scores or risk labels without the required evidence workflow.

### P2 — Higher-complexity research workflow

6. novelty-search intake and evidence review.

This module requires feature decomposition, prior-art dates, search provenance, and analyst review.

## Three-step core workflow

### Step 1 — Retrieve and normalize the authorized portfolio

#### Entity normalization

Create an entity register:

```text
entity_id
legal_name
normalized_name
aliases
subsidiaries
historic_names
relationship_type
effective_period
source_ids
approval_state
```

Do not combine subsidiaries, founders, research institutions, or licensees without evidence and approval.

#### Search and retrieval

Run entity-specific global searches with a documented query version.
Retrieve all records supported by the agreed scope.
If a complete export is unavailable, label the portfolio incomplete rather than calling it full.

#### Deduplication

Choose and disclose one primary portfolio unit:

- application;
- publication;
- grant;
- simple family;
- extended family;
- user-managed matter.

Do not deduplicate by a vendor-specific facet without confirming its current semantics.
Preserve all identifiers and relationships even when one record represents the primary row.

#### Normalized patent record

```text
record_id
matter_id
family_id
publication_number
application_number
grant_number
authority
kind_code
title
applicant_raw
applicant_normalized
inventors
priority_date
filing_date
publication_date
grant_date
raw_legal_status
normalized_status
status_as_of
application_type
IPC
CPC
technology_tags
PCT_relationship
parent_child_relationships
representative_record
source_url
source_ids
confidentiality_class
owner
review_state
```

#### Status normalization

Keep raw and normalized status side by side.
Use text states such as:

- pending;
- granted/active according to source;
- expired;
- lapsed;
- abandoned;
- ceased;
- revoked or invalidated;
- unavailable.

Status is authority-, member-, event-, record-, and date-specific.
Do not treat database status as legal advice.

### Step 2 — Identify and validate competitors

Use three evidence routes from the source:

1. shared IPC/CPC or technical classifications;
2. backward and forward citation relationships;
3. overlapping technical problems, solutions, applications, or mechanisms.

Add market/company evidence before calling an entity a commercial competitor.
A citation or shared classification alone establishes technical proximity, not competitive threat.

Competitor record:

```text
competitor_id
legal_name
normalized_name
aliases
relationship_reason
classification_evidence
citation_evidence
technical_overlap
market_evidence
portfolio_metric_state
representative_patent_ids
monitoring_queries
last_checked
confidence
limitations
```

Do not ship a fixed company list.
Do not fabricate patent counts or risk levels.

### Step 3 — Generate the single-file HTML workspace

Generate eight modules from reviewed normalized data.
All data shown must include source and cutoff metadata.

The workspace may include filters, pagination, local display state, and print/export controls.
Any action requiring a connector, persistence, notification, authentication, or writeback must be:

- disabled with a clear explanation;
- linked to an approved external workflow; or
- implemented only when an approved backend contract is actually supplied.

## Eight-module specification

### Module 1 — Portfolio dashboard

#### Summary cards

- total records under the disclosed count unit;
- pending applications;
- granted/active records according to the stated status source;
- PCT-related records under a stated definition;
- records with unavailable status;
- last verified cutoff.

#### Visuals

- legal-status distribution;
- application/document-type distribution;
- annual filing or priority trend;
- technical-theme distribution;
- data-completeness view.

Every chart must use complete normalized portfolio data.
Provide an accessible table containing the same values.

#### Task register

Show tasks such as:

- fee/deadline verification;
- office-action response;
- ownership/data-quality review;
- family/status reconciliation;
- FTO/novelty/value review;
- counsel approval.

Tasks require owner, due date, source, state, and external-system reference.

### Module 2 — Patent asset register

Provide:

- search by publication/application/grant/title/assignee;
- filters for status, authority, type, owner, technology, confidentiality, and review state;
- pagination, default ten rows per page;
- deterministic sorting;
- visible result count and active filters.

Columns:

```text
row
primary_identifier
title
priority_or_filing_date
authority
normalized_status
status_as_of
application_type
IPC/CPC
family/matter
owner
review_state
source
```

Use only an allowlisted source URL returned by the connector or an approved global Patsnap link.
Do not construct a legacy deep-link pattern from a private UUID.

### Module 3 — Fee and deadline operations

This module is an operational register, not an autonomous docketing system.

Required fields:

```text
task_id
matter_id
authority
event_type
official_or_docketing_source
source_date
due_date
grace_period_or_extension
amount
currency
amount_basis
responsible_owner
outside_counsel
verification_state
payment_or_action_state
verified_by
verified_at
external_system_reference
notes
```

Rules:

- never calculate a deadline solely from database status;
- verify jurisdiction-specific law and official-office/docketing records;
- distinguish fee estimate from official amount;
- use dual review for material deadlines;
- do not mark paid without authorized source-system evidence;
- a static HTML control may filter or display state but cannot persist payment.

### Module 4 — Outside-counsel analytics

Do not infer counsel from patent wording or filing patterns.
Use verified representative/agent fields, invoices, or approved matter data.

Metrics may include:

- matters or filings handled;
- granted outcomes under a defined cohort;
- pending and censored matters;
- average pendency under a stated method;
- office-action cycles;
- technology and authority coverage;
- cost metrics from authorized billing data;
- data completeness.

Grant-rate contract:

```text
cohort_definition
filing_period
authority
application_type
denominator
grant_outcome
abandonment_outcome
pending_censored
cutoff
source_ids
```

Do not compare firms across incompatible cohorts.

### Module 5 — Competitor monitoring

Each competitor card must show:

- normalized company name;
- evidence-backed relationship reason;
- monitored query IDs;
- latest verified signal;
- representative patents;
- portfolio metric or unavailable state;
- technical-overlap observation;
- monitoring cutoff;
- confidence and limitations;
- link to a separate FTO intake, not an automatic risk verdict.

Use `High`, `Medium`, `Low`, or `Unresolved` only for a specifically defined monitoring signal.
Do not use a generic red/orange/green competitor “risk bar.”

### Module 6 — FTO screening workflow

FTO is product/feature-, claim-, jurisdiction-, date-, and use-specific.
It cannot be generated from competitor name alone.

Input form:

```text
project_id
product_or_process
technical_features
jurisdictions
target_launch_or_use_date
making/using/selling/importing context
known_competitors
design_variants
search_scope
responsible_counsel
confidentiality_class
```

Workflow:

1. route to `create-fto-screening-report-ip` if installed;
2. preserve feature-to-claim mapping and source evidence;
3. route output to `review-fto-report-quality-ip` if installed;
4. show status, report link, evidence cutoff, and counsel sign-off;
5. never display a fabricated immediate result.

Result register:

```text
FTO_project_id
scope
status
potentially_relevant_patents
claim_mapping_state
risk_state
design_options
limitations
counsel_review
report_locator
```

### Module 7 — Patent-value screening

Preserve the source T/L/B concept:

- `T` — technical evidence;
- `L` — legal and rights evidence;
- `B` — business and strategic evidence.

Do not claim a proprietary 80+ indicator model unless the actual verified service and methodology are available.
Do not call a screening score patent valuation.

For each dimension expose:

- metric definition;
- raw value;
- source and cutoff;
- normalization method;
- weight;
- missing-data treatment;
- uncertainty;
- reviewer override and rationale.

Possible evidence:

- technical relevance and claim scope;
- family and jurisdiction breadth;
- status and remaining term;
- citations with age/field/office limits;
- prosecution and challenge history;
- product/standard/use evidence;
- licensing or litigation evidence;
- strategic fit and substitutability.

Use `assess-high-value-patent-portfolio-ip` if installed and its candidate-universe contract fits.

### Module 8 — Novelty-search intake

Input:

```text
invention_id
technical_problem
technical_features
feature_relationships
claimed_or_expected_effects
critical_dates
inventor_disclosures
known_prior_art
jurisdictions_or_databases
confidentiality_class
review_owner
```

Do not include real unpublished examples in a reusable package.
Synthetic life-sciences examples may include:

- microbial production of a carotenoid;
- recombinant structural protein production;
- genome-editing recombination architecture;
- fermentation of a vitamin analogue;
- engineered-microbe synthesis of a cofactor.

Output register:

```text
search_id
feature_map
queries
databases
cutoff
candidate_prior_art
priority/publication_dates
feature_mapping
novelty_screen_state
limitations
analyst_review
report_locator
```

Never issue a novelty conclusion from title similarity alone.

## Refresh and synchronization contract

The source six-stage “one-click sync” is preserved as a controlled refresh workflow:

1. authenticate through an approved secure connector host;
2. retrieve the authorized scoped portfolio;
3. normalize bibliography, family, status, and publication information;
4. reconcile fee/deadline source references without inventing payment state;
5. refresh approved competitor queries and citation relationships;
6. validate and write a versioned local snapshot or approved backend transaction.

### Refresh controls

Every stage must produce:

```text
run_id
stage
started_at
completed_at
source
record_count_in
record_count_out
added
updated
unchanged
rejected
errors
review_state
```

Never use animation as proof of success.
The UI must display actual stage results or label the control as a nonfunctional prototype.

### Record-preservation gate

Before replacing a prior version:

- load the prior normalized record set;
- reconcile stable IDs;
- compare counts by status, authority, family, and type;
- explain every deletion or merge;
- preserve user-entered owner/task/review fields;
- keep a rollback copy or versioned snapshot when authorized;
- do not silently truncate to a search Top-K.

## HTML output contract

### File

```text
patent-portfolio-workspace-v{n}.html
```

Use a user-approved workspace location.
Do not default to an undocumented session-specific scripts directory.

### Technical requirements

- one UTF-8 HTML file;
- no remote dependency or CDN;
- no credential or secret;
- no network call from the static file;
- safe escaped data;
- allowlisted HTTP(S) links;
- semantic landmarks, headings, tables, forms, and buttons;
- responsive navigation and table overflow;
- visible keyboard focus;
- reduced-motion and print support;
- text states rather than color-only meaning;
- inline static SVG/CSS charts with accessible table equivalents;
- explicit data cutoff, provenance, and prototype/product status.

### Visual language

- white paper and neutral canvas;
- navy/slate text hierarchy;
- restrained teal accent;
- system fonts;
- compact evidence-first cards;
- no gradients, glow, decorative emoji, animated progress bars, or misleading control affordances.

### Interaction safety

- local filters and pagination may run in JavaScript;
- use `textContent`, `createElement`, and `replaceChildren` for untrusted data;
- do not inject connector/user strings as raw HTML;
- do not use inline event handlers;
- disabled actions must explain the missing backend or approval;
- local display state must not be presented as persisted business state.

## Three operating scenarios

### Scenario 1 — New workspace

1. confirm entity, portfolio, module, security, and output scope;
2. retrieve and normalize authorized evidence;
3. document unavailable operational data;
4. generate the eight-module workspace;
5. validate counts, sources, security, accessibility, and prototype boundaries;
6. propose the phased implementation roadmap.

### Scenario 2 — Iterate an existing workspace

1. inspect the current HTML and its embedded data contract;
2. preserve every valid record and stable ID;
3. map requested functionality to existing modules;
4. update without weakening security or accessibility;
5. reconcile counts and user-entered fields;
6. increment the version and document changes.

Do not assume an existing CDN chart or legacy link must be preserved.
Preserve capability and data, then localize the implementation safely.

### Scenario 3 — Refresh data

1. preserve the current snapshot;
2. run the controlled six-stage refresh;
3. compare old and new records;
4. require review for removals, status changes, ownership changes, and deadlines;
5. regenerate the HTML from the approved normalized snapshot;
6. document source cutoff and refresh result.

## Common failure modes

### 1. Record loss during iteration

Cause: rebuilding from a truncated search result.
Control: reconcile stable IDs and counts against the prior complete snapshot.

### 2. Broken patent links

Cause: constructing a legacy vendor URL from a UUID.
Control: use a verified source URL returned by the connector or an approved global Patsnap product link.

### 3. Encoding corruption

Cause: inconsistent shell or locale encoding.
Control: read and write UTF-8 explicitly and validate rendered text.

### 4. Charts fail offline

Cause: CDN chart dependency or hidden-canvas initialization.
Control: use static inline SVG/CSS and adjacent tables; no CDN.

### 5. Misleading competitor data

Cause: invented lists, shared IPC treated as competition, or sample-derived counts.
Control: normalize entities, cite market and technical relationships, and show complete metrics or Unavailable.

### 6. False operational behavior

Cause: static buttons imitate refresh, payment, reminders, or analysis.
Control: disable, label as prototype, or connect only through an approved real backend contract.

### 7. Deadline liability

Cause: treating database events as official instructions.
Control: use official/docketing sources, owner assignment, verification timestamp, and dual review.

## Phased implementation plan

### MVP — approximately 6–8 weeks, subject to scope

- authorized portfolio asset register;
- source/status/family reconciliation;
- fee/deadline register with official-system references;
- outside-counsel data model;
- competitor-monitoring query register;
- read-only self-contained workspace;
- role, security, audit, backup, and acceptance plan.

### Phase 2 — approximately 3–4 months, subject to integrations

- approved backend and authentication;
- secure scheduled refresh;
- persistent tasks and notifications;
- FTO intake/report routing;
- transparent patent-value screening;
- outside-counsel and cost analytics;
- data-quality and audit dashboards.

### Phase 3 — six months or more, subject to validation

- novelty-search intake and analyst workflow;
- advanced competitor monitoring;
- portfolio scenario and maintenance review;
- controlled writeback to docketing or knowledge systems;
- model governance, human review, and ongoing quality monitoring.

Timelines are planning ranges, not commitments.

## Success criteria

### Data integrity

- agreed portfolio unit and scope are explicit;
- record counts reconcile across versions;
- raw/normalized status and source dates are preserved;
- family/entity duplicates are reviewed;
- no record disappears without a documented reason.

### Operational integrity

- every deadline/task has owner, source, state, and verification;
- static prototype limitations are visible;
- real backend actions have authentication, authorization, logging, and rollback;
- no secret appears in HTML or logs.

### Analytical integrity

- competitor relationships are evidence-backed;
- FTO is feature/claim/jurisdiction/date-specific;
- value scores expose dimensions and missing data;
- novelty screens map features to dated prior art;
- no sample is presented as a complete population.

### Usability and accessibility

- all eight modules are navigable;
- tables, filters, pagination, focus, responsive layout, and print work;
- charts have table equivalents;
- status and risk are understandable without color;
- source and cutoff are visible.

## Quality gates

### Package gate

- Exact one-file source topology is preserved.
- No README, agent, reference, script, asset, example, test, or data file is added.

### Source gate

- Entity and portfolio scope are authorized.
- Every data element has source and cutoff.
- Confidentiality classification and handling are approved.

### Module gate

- Dashboard, assets, fees/deadlines, counsel, competitors, FTO, value, and novelty modules are present.
- Unsupported modules show a clear unavailable/prototype state.

### Legal gate

- Fee/deadline data has official/docketing verification.
- FTO, value, novelty, status, and counsel metrics carry appropriate limitations.
- No database result is presented as legal instruction.

### Product gate

- Static and production capabilities are clearly distinguished.
- No fake synchronization, payment, alert, FTO, value, or novelty outcome appears.
- Backend-dependent controls are disabled or linked to an approved workflow.

### Security gate

- No credential, unpublished invention text, attorney work product, private UUID list,
  billing data, or personal information is exposed without authorization.
- Links and rendered text are safe.
- Role, audit, retention, backup, and rollback requirements are documented.

### Visual gate

- HTML is self-contained, safe, semantic, accessible, responsive, and print-ready.
- No CDN, gradient, emoji-only state, color-only meaning, unsafe injection, or legacy China link remains.

## Failure handling

If the portfolio cannot be retrieved completely, label the dataset partial.
If entity scope is unresolved, do not merge records.
If status is stale, preserve raw status and mark normalized status Unavailable.
If fee/deadline evidence is not official or docketed, do not issue an instruction.
If outside counsel is unverified, do not infer it.
If a competitor relationship lacks market evidence, call it technical proximity only.
If FTO/value/novelty evidence is missing, create an intake and next-action record, not a result.
If a prior HTML lacks normalized source data, extract and reconcile before iteration.
If a real integration is requested without an approved backend/security contract, stop at the prototype specification.

## Final response

State:

- authorized entity and portfolio scope;
- count unit, record count, and cutoff;
- modules delivered and modules still prototype/unavailable;
- source and refresh status;
- highest-priority data or operational risk;
- phased next step;
- output path and version;
- required IP-operations, counsel, security, or backend approval.
