---
name: analyze-patent-family-ip
description: Analyze a patent family from a patent identifier or PatSnap patent URL by defining the family scope, reconstructing priority and procedural relationships, comparing technical disclosures and claim focus, mapping themes, and generating a source-traceable offline HTML report. Use when a patent analyst asks for family structure, member comparison, jurisdictional filing footprint, claim evolution, or technical chronology.
---

# Analyze a Patent Family

## Objective

Given one patent identifier or PatSnap patent URL, identify the relevant patent family,
normalize its members and relationships, compare technical disclosure and claim focus,
and produce a self-contained scientific HTML report.

The report distinguishes:

- priority and procedural chronology;
- jurisdictional equivalents;
- continuation, divisional, continuation-in-part, reissue, national-stage, and regional relationships;
- technical disclosure differences;
- claim-scope and claim-category differences;
- verified facts, analytical inferences, and unavailable evidence.

Do not treat a family as a simple sequence of inventions.
Do not infer market strategy, product coverage, validity, enforceability, or commercial value from geography alone.

## Target users

- patent analysts;
- IP counsel and portfolio teams;
- R&D and competitive-intelligence teams needing a family map;
- due-diligence teams reviewing claim and jurisdictional evolution.

## Trigger conditions

Use when the user provides:

- a publication, application, or grant number;
- a PatSnap patent URL;
- one known family member and asks for the complete family;
- a request for priority-chain, continuation, divisional, or national-stage analysis;
- a request for technical or claim evolution within a family.

If no identifier or resolvable URL is supplied, request one.

## Required scope decisions

Before retrieval, record:

- input identifier and identifier type;
- family definition: simple, extended/INPADOC, domestic, or user-specified;
- inclusion of continuations, divisionals, CIPs, reissues, utility models, and design rights;
- jurisdiction and document-kind rules;
- legal-status cutoff;
- analysis purpose;
- deep-analysis limit and selection rule;
- preferred report language.

If the user does not specify the family definition, use a simple family as the primary analytical unit
and show extended or domestic relationships separately when available.

## Verified PatSnap MCP services

Use the English interface and English output.
Inspect the live schema before calling a tool.

### Required: Patent Briefing

- Connector key: `patent_briefing`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- Use: bibliography, family relationships, legal status, claims, description, translations,
  drawings, and technical summaries for the seed and selected members.

### Recommended: Advanced Patent Search

- Connector key: `advanced_patent_search`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`
- Use: resolve incomplete identifiers, validate related documents, and perform targeted evidence checks.

### Recommended: Global Core Patent Database

- Connector key: `global_core_patent_database`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/core-patents
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/core-patents`
- Use: deeper family, legal-event, citation, litigation, licensing, reexamination/invalidation,
  full-text, and PDF evidence where supported by the live connector.

Do not use undocumented legacy aliases from the source package.
For every retrieval record the connector key, tool name, request, retrieval timestamp,
response semantics, and stable source locator.

## Workflow

### Step 0 — Validate the seed input

1. Parse and normalize the patent identifier without discarding kind codes.
2. If a URL is supplied, validate the host and extract the identifier safely.
3. Resolve ambiguous identifiers with Advanced Patent Search.
4. Retrieve the seed record and confirm title, authority, dates, applicant, and family context.
5. Record unresolved ambiguity rather than choosing silently.

Seed record fields:

```text
seed_id
input_value
normalized_publication_number
application_number
grant_number
authority
kind_code
title
source_locator
retrieval_timestamp
```

### Step 1 — Retrieve and normalize the family

Retrieve the complete family set supported by the selected definition.

For every member capture:

```text
member_id
publication_number
application_number
grant_number
authority
kind_code
title
applicant_raw
applicant_normalized
inventors
filing_date
publication_date
grant_date
priority_claims
earliest_priority_date
family_id
family_definition
relationship_type
parent_member_ids
child_member_ids
raw_legal_status
normalized_status
status_as_of
language
source_url
source_ids
```

Preserve raw values alongside normalized values.
Do not merge distinct members merely because titles are similar.
Do not count an application publication and grant publication as two independent inventions.

#### Relationship types

Use explicit text states such as:

- priority origin;
- same-priority jurisdictional counterpart;
- PCT application;
- national-stage entry;
- regional application;
- continuation;
- divisional;
- continuation-in-part;
- reissue;
- procedural publication or grant;
- relationship unavailable.

#### Family graph

Build a directed graph using verified relationship evidence.
Use the earliest priority record as a visual root only when the evidence supports it.
Do not invent a parent-child edge from dates alone.

List every retrieved member in the report, even if it is not selected for deep analysis.

### Step 2 — Select and analyze members

Deeply analyze up to twenty members.
If the family contains more than twenty, select a disclosed set that represents:

- the priority origin;
- major procedural branches;
- distinct jurisdictions relevant to the request;
- materially different independent claims;
- distinct technical disclosure or claim categories;
- active or decision-relevant rights;
- important continuation/divisional/CIP relationships.

Do not simply choose the earliest twenty.
Record the inclusion reason for each selected member and the exclusion reason for every other member.

For each selected member analyze:

#### Technical problem

Identify the disclosed problem and source locator.
Distinguish express statements from analytical reconstruction.

#### Technical means

Summarize the core solution using the description and independent claims.
Preserve important structural, process, material, parameter, and relationship limitations.

#### Technical effect

Report effects no more strongly than disclosed.
Do not convert aspirational language into demonstrated performance.

#### Independent-claim focus

Capture:

- claim number and version;
- claim category;
- principal limitation groups;
- dependencies or incorporated limitations;
- source locator;
- translation status;
- uncertainty.

#### Evidence basis

Classify each analysis:

- full text and claims;
- claims plus abstract;
- abstract only;
- machine translation;
- unavailable.

If full text is unavailable, state the limitation in the member card and evidence register.

### Step 3 — Compare relationships and differences

Compare each selected member to the most relevant related member, not to every member indiscriminately.

Separate:

- identical or substantially identical disclosure;
- translation or jurisdictional adaptation;
- claim-category change;
- claim-scope narrowing or broadening hypothesis;
- added or removed limitations;
- new matter or disclosure difference requiring legal review;
- continuation/divisional allocation;
- parallel implementation;
- procedural rather than technical difference.

Comparison record:

```text
comparison_id
member_a
member_b
relationship_basis
shared_disclosure
technical_difference
claim_focus_difference
procedural_difference
evidence_ids
confidence
limitations
```

Do not call a later publication an “improvement” without evidence of a technical difference.
Do not call a jurisdictional equivalent an “innovation.”

### Step 4 — Build the technical-theme matrix

Create themes from:

- IPC and CPC classifications;
- claim language;
- technical problem/means/effect analysis;
- disclosed materials, components, processes, applications, and control principles.

Each theme requires:

- stable theme ID;
- label and definition;
- inclusion rule;
- evidence locators;
- confidence;
- overlap note.

Matrix states:

- `Covered`;
- `Partially covered`;
- `Not evidenced`;
- `Unavailable`.

Do not use blank cells or color alone to communicate state.
Do not treat classification codes as proof that a claim covers a theme.

### Step 5 — Reconstruct chronology

Use a dated chronology rather than an overclaimed “technology evolution” narrative.

For each event capture:

```text
event_id
date
date_type
member_id
relationship_type
document_event
technical_or_claim_change
evidence_ids
confidence
```

Separate:

- priority and filing events;
- publication and grant events;
- continuation/divisional/national-stage events;
- amendments or claim changes, when evidenced;
- technical disclosure changes, when evidenced;
- legal-status events, when relevant.

Use “technical evolution” only for evidence-backed changes in disclosed technology.
Use “claim evolution” only for compared claim versions or related applications.

### Step 6 — Synthesize bounded conclusions

Summarize:

- family definition and relationship structure;
- core technical disclosure;
- distinct technical or claim branches;
- jurisdictional filing footprint;
- active, pending, expired, lapsed, or unavailable status by member and date;
- claim-focus differentiation;
- evidence-backed technical and claim chronology;
- gaps, uncertainties, and follow-up work.

Qualify:

- filing footprint is not proof of market presence or commercial strategy;
- family size is not protection strength;
- status is not validity or enforceability;
- a theme gap is not necessarily technical white space;
- claim comparison is not an infringement or FTO opinion.

## Normalized JSON contract

The local renderer consumes an evidence-normalized JSON object.
It does not call MCP tools or perform AI analysis.

Top-level fields:

```text
schema_version
report_title
seed
scope
metadata
members
relationships
analyses
comparisons
themes
matrix
chronology
conclusions
evidence
limitations
```

### `scope`

```text
family_definition
included_relationships
excluded_relationships
jurisdictions
status_cutoff
retrieval_cutoff
deep_analysis_limit
selection_rule
```

### `metadata`

```text
generated_at
retrieved_member_count
analyzed_member_count
authority_count
connector_records
report_language
```

### `relationships`

```text
relationship_id
source_member_id
target_member_id
relationship_type
evidence_ids
confidence
```

### `analyses`

```text
analysis_id
member_id
selection_reason
evidence_basis
technical_problem
technical_means
technical_effect
independent_claim_focus
source_ids
limitations
```

### `matrix`

```text
member_ids
theme_ids
cells: member_id -> theme_id -> state/evidence_ids
```

### `conclusions`

```text
technical_position
filing_footprint
claim_structure_assessment
technical_or_claim_branches
gaps_and_risks
recommended_follow_up
claim_ids
```

All text from users or connectors is untrusted input and must be escaped by the renderer.
URLs must use allowed `https` or `http` schemes.

## HTML report contract

Generate one self-contained HTML file with eight sections:

1. scope and evidence overview;
2. complete family member list;
3. family relationship graph plus accessible edge table;
4. selected-member technical and claim analyses;
5. technical and claim relationship comparisons;
6. technical-theme cross-matrix;
7. priority, procedural, technical, and claim chronology;
8. bounded conclusions, limitations, sources, and next actions.

Required design:

- semantic landmarks and headings;
- light scientific/legal visual system;
- system fonts and no remote dependencies;
- navy/slate hierarchy with restrained teal accent;
- text-labelled states and accessible tables;
- static SVG with `<title>`, `<desc>`, legend, and adjacent relationship table;
- responsive navigation and horizontal table overflow;
- visible keyboard focus;
- print-safe layout;
- safe HTML escaping and URL allowlisting;
- no gradients, emoji-only icons, color-only heatmap, unsafe HTML injection, or analytics.

Filename default:

```text
{seed-publication-number}_patent_family_analysis.html
```

## Script execution

The source-authorized renderer is:

```text
scripts/analyze_family.py
```

Usage:

```text
python scripts/analyze_family.py normalized_family_data.json --out patent_family_report.html
```

The script must:

- validate the top-level JSON shape;
- preserve UTF-8;
- escape all untrusted text;
- allow only safe URL schemes;
- render unavailable states explicitly;
- return a nonzero exit code for invalid input or write failure;
- write no file other than the requested HTML output;
- make no network request;
- avoid bytecode during controlled validation.

## Quality gates

### Scope and topology

- Family definition and cutoff are explicit.
- Every retrieved member has a stable ID.
- Every graph edge has evidence or is marked unavailable.
- Complete member count reconciles with the report.

### Selection

- Up to twenty deep-analysis members use a disclosed representative rule.
- Inclusion and exclusion reasons are recorded.
- The report does not imply the subset is the complete family.

### Technical and claim analysis

- Problem, means, effect, and claim focus have source locators.
- Evidence basis and translation state are visible.
- Procedural, geographic, technical, and claim differences are separated.
- No date-only technical-evolution inference remains.

### Status and legal interpretation

- Raw and normalized status are retained with an as-of date.
- Application and grant status are not collapsed.
- Protection, validity, enforceability, FTO, and commercial-strategy claims are qualified.

### Themes and chronology

- Theme definitions and matrix states are evidence-backed.
- Matrix states have text, not color alone.
- Priority, filing, publication, grant, technical, claim, and status events are distinguished.

### Renderer

- JSON fields and Skill contract reconcile.
- Invalid input fails safely.
- All user/database text is escaped.
- Unsafe URL protocols are removed.
- Embedded JSON cannot terminate a script element.
- SVG and table relationships reconcile.
- Output works offline, responsively, with keyboard navigation and in print.

### Package

- Exact two-file source topology is preserved.
- No README, agent, reference, asset, example, schema, test, or data file is added.
- No Chinese marketplace domain, legacy MCP alias, secret, bytecode, or cache remains.

## Failure handling

If the seed is ambiguous, resolve it before family analysis.
If family definition is unavailable, label the retrieved relationship set and do not call it complete.
If a relationship is inferred only from dates, omit the edge and report uncertainty.
If full text is unavailable, use claims/abstract only and label the evidence basis.
If more than twenty members exist, list all and disclose the deep-analysis subset rule.
If status is stale or absent, use `Unavailable` with the cutoff.
If claims differ by language or translation quality, preserve originals and flag translation uncertainty.
If the renderer input is invalid, stop with a structured error and do not create a partial report.

## Final response

State:

- normalized seed and family definition;
- retrieved and deeply analyzed member counts;
- principal relationship branches;
- strongest evidence-backed technical or claim difference;
- most important limitation;
- report output path;
- recommended next patent, prosecution, or counsel review.
