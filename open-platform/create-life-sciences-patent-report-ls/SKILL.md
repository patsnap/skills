---
copyright: "Copyright © Patsnap. All rights reserved."
name: create-life-sciences-patent-report-ls
description: Create or update a traceable, self-contained HTML patent intelligence report for a life-sciences technology, target, drug, antibody, ADC, company, or patent set. Use when a user requests a life-sciences patent landscape or deep-dive report that integrates claims, sequences or conjugate technology, experiments, pipeline and clinical context, scientific evidence, deals or news, and inline patent-figure evidence.
---

# Create a Life Sciences Patent Report

## Purpose

Turn supplied patent identifiers, stable record URLs, target/drug/company entities, structured exports, or an existing report into an English, evidence-traceable life-sciences patent intelligence report. Preserve source identifiers and exact returned URLs, distinguish patent evidence from scientific/clinical/commercial context, and produce a self-contained HTML file with a restrained scientific/editorial design.

Read `references/report-spec.md` before creating or editing a report.

## Trigger boundary

Use this skill for:

- a patent-centric life-sciences landscape or deep dive;
- a refreshed/versioned run of an earlier patent report;
- antibody, ADC, biologic, drug, target, platform, or company patent analysis;
- claim, sequence, payload, linker, scaffold, experimental, clinical, literature, deal, or news context around patents;
- a self-contained HTML evidence report;
- inline, hoverable local patent-figure citations.

Do not use it for a legal FTO opinion, a generic clinical landscape with no patent objective, or a marketing landing page.

## Project and version gate

1. Define topic, decision, audience, jurisdictions, date range/cutoff, patent counting rule, and required evidence modules.
2. If the user says “rerun,” “previous project,” or similar, inspect the supplied/current workspace for prior reports and select the closest subject only from evidence. State the chosen baseline.
3. Never overwrite an earlier report unless explicitly instructed. Use a meaningful version/date suffix.
4. Reuse source-existing local styles/assets only when actually present and approved. Do not assume a personal absolute path or a nonexistent repository template.
5. If an old report is used, re-query time-sensitive facts and preserve a change log; do not copy stale data as current.

## Required inputs

At minimum:

- report topic or anchor patent/entity;
- analysis purpose and audience;
- cutoff or current-data expectation;
- requested output location/format.

Clarify or state assumptions for:

- jurisdictions and languages;
- family/publication/application counting;
- legal-status scope;
- target, drug, company, disease, modality, sequence, payload, linker, or platform boundaries;
- clinical/literature/deal/news context;
- confidential data and permitted external services;
- whether local figure extraction/preview is required.

## Evidence and MCP routing

Use supplied authoritative material first. No MCP is required when it is complete.

For live retrieval, use only available and authorized global Patsnap MCPs:

| Evidence | MCP | Verified role | Marketplace |
|---|---|---|---|
| Patent discovery | `advanced_patent_search` | Fielded, nested, semantic, number, applicant, count, and keyword-assist patent search | https://open.patsnap.com/marketplace/mcp-servers/patent-search |
| Patent/family detail | `patent_briefing` | Bibliography, family, status, claims, description, drawings, translations, and technical summary | https://open.patsnap.com/marketplace/mcp-servers/patent-briefing |
| Target/disease context | `target_disease` | Target and disease profiles and epidemiology evidence | https://open.patsnap.com/marketplace/mcp-servers/target-disease |
| Drug/pipeline context | `drug_asset` | Drug search, details, and milestones | https://open.patsnap.com/marketplace/mcp-servers/drug-asset |
| Trials/results | `clinical_trials` | Trial search/fetch and result search/fetch | https://open.patsnap.com/marketplace/mcp-servers/clinical-trials |
| Translational evidence | `scientific_translational_evidence` | Translational record search/fetch | https://open.patsnap.com/marketplace/mcp-servers/scientific-translational-evidence |
| Guidelines/labels | `regulatory_guidelines` | Optional FDA-label and guideline semantic evidence | https://open.patsnap.com/marketplace/mcp-servers/regulatory-guidelines |
| Pharmaceutical news | `current_awareness` | Optional news search/fetch | https://open.patsnap.com/marketplace/mcp-servers/current-awareness |

Do not claim that an advertised MCP supplies tools not listed on its current marketplace page. Use company/deal, sequence, or chemical structure services only when their actual tools are exposed and verified; otherwise request exports and record the gap.

## Stable source-link rule

Build a source map before drafting.

For every record, preserve:

- source type and stable entity/publication identifier;
- exact URL returned by the MCP/source, if any;
- original source URL for news, deal, clinical, regulatory, or scientific evidence where available;
- retrieval time and database cutoff;
- query/tool used;
- report claims supported;
- confidence and unresolved mismatch.

Never construct a frontend detail/list URL from an entity UUID, publication number, NCT number, title, company, or display name unless the official global documentation explicitly defines that route and identifier type. Do not place an MCP entity UUID into a search-list `query_id`. Do not place a publication number into a UUID-only `patentId` parameter. Prefer the exact returned URL; otherwise use a verified official-register or primary-source URL. If no stable link exists, cite the source/tool/identifier without inventing one.

## Workflow

### 1. Scope and entity normalization

- freeze topic, cutoff, jurisdictions, languages, counting rules, and deliverable version;
- normalize patent publications/applications/grants and family IDs;
- normalize target/gene/protein, drug/development-code, company/legal-name, disease, trial, and paper identifiers;
- retain aliases and source-specific IDs without merging uncertain entities;
- define modules that are required, optional, not applicable, or blocked.

### 2. Patent retrieval

- use known patent numbers as anchor records;
- run structured and semantic searches for the technology scope;
- capture complete reproducible queries and counts;
- consolidate exact duplicates and families under the declared counting rule;
- retrieve claims, description, bibliography, family, legal status, translations, and drawings for priority records;
- distinguish granted/pending and verify material status in official registers when legal significance is discussed;
- for antibody/ADC work, use verified sequence/structure exports or services when actually available.

Do not dump a broad target search directly into the report. Refine by modality, target/epitope, payload/linker, indication, company, claim concept, date, jurisdiction, or technical route and show the funnel.

### 3. Context retrieval

Use only relevant modules:

- target biology and disease context;
- drug/pipeline identity and milestones;
- clinical trials and results;
- scientific/translational evidence;
- regulatory labels/guidelines;
- company/deal/news context;
- sequences, structures, SAR, payloads, linkers, scaffolds, or conjugation.

Keep patent, experimental, clinical, regulatory, literature, and commercial evidence visibly separate. A patent assertion is not experimental validation; a trial result is not claim scope; a deal is not ownership/license proof unless the underlying agreement supports it.

### 4. Source matrix

Create an internal matrix:

| Source ID | Type | Entity/publication ID | Exact URL | Retrieved | Supports | Primary/secondary | Notes |
|---|---|---|---|---|---|---|---|

Every specific number, date, status, claim, sequence, assay result, clinical outcome, deal term, or analyst conclusion must trace to one or more source IDs.

### 5. Draft report

Use the information architecture in `references/report-spec.md`:

- overview and key findings;
- patent core/family/status;
- target or technology background;
- claims, sequence, scaffold, payload/linker, or technical-route analysis;
- experimental evidence;
- pipeline and clinical landscape;
- clinical results;
- patent landscape and risk/opportunity implications;
- literature/translational/regulatory evidence;
- deals/company/news;
- inline figure evidence and figure index;
- sources, query provenance, counting and link audit.

Include only applicable chapters, but record omitted modules and reasons. Separate source fact, interpretation, uncertainty, and recommended action.

### 6. Inline figure evidence

When a locally stored patent figure/table/graph is available and legally/operationally appropriate:

- place the citation immediately beside the claim it supports;
- use a normal link that works without JavaScript;
- add hover/focus preview as progressive enhancement;
- use a descriptive caption with patent/source and figure/table identifier;
- preserve a figure appendix/index;
- verify the local file exists and remains within the report package;
- provide accessible alt text and keyboard/focus behavior.

Do not create a package asset or report image that was not supplied/extracted during the report task. Do not imply that a figure proves more than its experiment supports.

### 7. Validate

- parse HTML;
- verify required IDs/anchors are unique;
- audit all source URLs and identifier types;
- reject invented list/detail routes and mismatched UUID/PN/NCT parameters;
- verify every local `src`, `href`, and `data-img` file;
- confirm no absolute developer path, API key, network request, external CDN/font/script, or missing asset;
- test hover and keyboard focus in a browser where available;
- test narrow viewport and print layout;
- reconcile citations, source map, counts, and claims;
- preserve old report versions.

If browser testing is unavailable, state exactly which static checks ran; do not claim interactive validation.

## Report design

Use a globally familiar scientific/editorial format:

- English by default;
- light neutral canvas, dark text, muted blue/teal accent, accessible status colors with text labels;
- system fonts, clear hierarchy, dense but readable tables, evidence callouts, and generous spacing;
- restrained sticky navigation on larger screens;
- semantic sections and responsive table wrappers;
- optional dark mode only if it remains accessible and adds no external dependency;
- no landing-page hero, gradients, glow, particles, ticker, decorative motion, or product-interface imitation;
- print CSS with source URLs, repeated table headers, and controlled page breaks.

## Quality gates

- [ ] Scope, cutoff, jurisdictions, languages, and counting rules are explicit.
- [ ] Earlier files were preserved and stale facts were rechecked.
- [ ] Entity normalization preserves aliases and unresolved collisions.
- [ ] Patent query, funnel, family grouping, and legal-status caveats are reproducible.
- [ ] Patent claims/status and non-patent context are distinguished.
- [ ] Every factual statement and key inference has a source ID.
- [ ] Exact returned/verified URLs are used; no identifier-based route was guessed.
- [ ] Sequences/structures are handled only by verified available services or exports.
- [ ] Inline figures exist, are accessible, and appear near supported statements.
- [ ] HTML parses and works without JavaScript.
- [ ] Hover/focus, responsive, and print behavior were tested or accurately caveated.
- [ ] No credential, absolute personal path, legacy domestic domain, invented evidence, or unsupported legal/clinical conclusion remains.

## Output boundaries

- Do not fabricate patents, claims, sequences, structures, experiments, trials, results, papers, deals, news, links, UUIDs, or figures.
- Do not present a patent's stated benefit as independently proven.
- Do not present database status as a legal opinion.
- Do not call a landscape exhaustive without evidence.
- Do not expose API keys or confidential material.
- Do not overwrite old reports without explicit instruction.
