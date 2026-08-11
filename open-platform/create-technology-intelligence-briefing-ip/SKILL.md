---
name: create-technology-intelligence-briefing-ip
description: Create an auditable technology-intelligence briefing for named companies and/or a technical topic using patent, scientific-literature, and current-news evidence. Use when the user requests a technology briefing, company technology comparison, patent-and-literature scan, subtechnology map, or evidence-backed technical trend report in HTML.
---

# Create a technology intelligence briefing

## Purpose

Produce two coordinated deliverables:

1. an English, static, accessible HTML briefing; and
2. a Markdown trace that lets another analyst reproduce and challenge the work.

The briefing may cover one company, multiple companies, one technology, or a company-by-technology comparison. It is research support, not legal advice, an investment recommendation, or a completeness guarantee.

## Non-negotiable evidence rules

- Use real retrieved records only. Never invent counts, patent identifiers, papers, authors, dates, legal status, quotations, news, or URLs.
- Distinguish a database population count from the selected records displayed in the report.
- Every cited patent must occur in `PATENTS`; every company grouping and subtechnology reference must point to those same records.
- Summarize a patent's problem, technical means, or benefit only when the retrieved claims, description, abstract, or connector output supports it. Label an abstract-only interpretation.
- Treat company aliases as search candidates. They do not prove ownership, corporate control, assignment, or group membership.
- Preserve official legal names in their native script when useful for retrieval. Use an English canonical display name in the report.
- Cite literature through a DOI or stable publisher/database record.
- Cite news through a stable article or primary-source URL, publication, publication date, and retrieval date.
- Never expose API keys, tokens, private query URLs, unpublished documents, or confidential search material.
- Do not create a polished report until the validation gate passes.

## Read the bundled resources

Read these files before execution:

- `references/parse_rules.md` for request normalization;
- `references/company_aliases.json` for optional assignee candidates;
- `references/keyword_expansion.md` for query expansion;
- `references/trace_template.md` for reproducibility fields;
- `scripts/v2_data.sample.py` for the renderer data contract;
- `scripts/build_report_v2.py` and `scripts/v2_css.py` for report generation; and
- `scripts/sogou_search.py` for the legacy-path news-source normalization helper.

The compatibility filename `sogou_search.py` does not authorize Sogou scraping. Its localized implementation accepts already retrieved news records and normalizes them.

## Connector map

### Patent retrieval — required for an executed briefing

Use **Advanced Patent Search** for company/topic retrieval, nested or fielded queries, semantic retrieval, assignee searches, keyword suggestions, and counts when supported by the live schema.

- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Configuration key: `advanced_patent_search`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`

Inspect the live schema before calling a tool. Record connector, exact tool, normalized request, filters, response semantics, retrieval date, and limitations. Do not claim that a count exists unless the response defines its counting unit.

### Selected-patent verification — required

Use **Patent Briefing** for bibliography, family, legal status, claims, descriptions, translations, images, and technical summaries.

- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Configuration key: `patent_briefing`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`

Verify publication/application identifiers and distinguish source-language text from machine translation.

### Technical enrichment — recommended

Use **Deep Patent Mining** when available for technical topics, technical problem/solution/effect, classifications, materials, and application domains.

- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-mining
- Configuration key: `deep_patent_mining`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-mining`

Enrichment is evidence, not permission to fill missing fields. Preserve the connector's evidence locator and confidence/limitation state.

### Literature and news

Use a separately verified current literature connector or an authoritative literature database. Do not configure a guessed PatSnap literature MCP.

Use authorized current web research for news. Prefer company filings, regulator releases, standards bodies, conference notices, and original press releases; supplement with credible reporting when appropriate. Record publication and event dates separately.

If either source class is unavailable, set its section status to `not_executed` and explain why.

## Workflow

### 1. Parse and confirm the scope

Normalize the request according to `references/parse_rules.md`.

Capture:

- research question and intended decision;
- technology in scope and explicit exclusions;
- company names, requested subsidiaries, and excluded entities;
- patent jurisdictions and/or geographic markets;
- exact start and end dates in ISO 8601;
- date field: priority, filing, publication, or grant;
- document types;
- languages;
- population counting unit;
- family and deduplication rule;
- displayed-record selection rule;
- literature source and document types;
- news date window and source policy;
- evidence cutoff date; and
- desired output path.

Ask a focused question only when an unresolved choice would materially change the result. Otherwise state the assumption in the trace.

### 2. Resolve companies and legal entities

For each named company:

1. normalize the user-entered name;
2. consult `references/company_aliases.json` for candidate names;
3. inspect live assignee suggestions or representative records;
4. separate parent, subsidiary, acquired entity, former name, joint venture, and brand;
5. decide which legal entities are included;
6. record every inclusion/exclusion and its evidence; and
7. obtain confirmation when entity scope materially changes coverage.

Do not silently combine distinct legal entities. In particular, entries marked `mixed_source_group_requires_selection` are prompts for disambiguation, not ready-to-run OR queries.

Create an entity register with:

| Field | Meaning |
|---|---|
| `canonical_name` | English report label |
| `searched_name` | Literal assignee string or normalized identifier |
| `relationship` | Parent, subsidiary, former name, acquired entity, or unknown |
| `included` | Yes, No, or Pending |
| `evidence` | Source locator supporting the relationship decision |
| `notes` | Ambiguity and limitations |

### 3. Define and expand the technology

Use `references/keyword_expansion.md` as a method and example set, not a closed taxonomy.

Build a concept table containing:

- core concept;
- synonyms and spelling variants;
- acronyms with expanded forms;
- component, material, process, architecture, function, and application terms;
- IPC/CPC classes or other classifications, after relevance checks;
- local-language equivalents needed for recall;
- exclusions and noise terms; and
- evidence for specialized terminology.

Create broad, balanced, and precision query variants. Test representative results and revise obvious noise before final retrieval.

### 4. Retrieve and count patents

For every query or company bucket, record:

- exact query;
- connector and tool;
- request parameters;
- jurisdictions;
- date field and dates;
- document types;
- language handling;
- family/deduplication rule;
- counting unit;
- result count returned;
- pagination or limit;
- retrieval timestamp; and
- warnings or truncation.

The full population count and displayed sample are separate quantities:

```text
population_count = count returned for the defined query and counting rule
displayed_count  = number of selected records rendered in the report
```

Never require them to be equal. If no count route exists, set `population_count_status: unavailable`; do not use the length of a limited result page as the population.

Retrieve enough candidate records to support the stated selection method. A default display limit such as 30 is a presentation choice, not evidence of completeness.

### 5. Normalize, deduplicate, and select records

Normalize identifiers, dates, names, jurisdictions, classifications, status labels, and URLs.

Apply the declared deduplication rule before selecting representatives. Selection may consider:

- direct technical relevance;
- family representativeness;
- earliest priority;
- selected-market relevance;
- legal/status relevance;
- claim or disclosure richness;
- recency for emerging topics; and
- company comparability.

Record why each displayed record was selected. Do not rank records by an opaque score.

### 6. Enrich selected patents

For each selected record, populate only supported fields:

- publication number;
- application number where available;
- title;
- applicant/assignee as returned;
- inventors;
- earliest priority and publication dates;
- jurisdiction;
- document kind;
- family identifier/relationship;
- legal-status value, source, and as-of date;
- IPC/CPC;
- abstract or evidence-bounded summary;
- technical problem;
- technical means;
- reported or claimed effect;
- relevant claim/disclosure locator;
- source URL; and
- evidence limitations.

Use batches appropriate to the live connector. The source's batch size of eight is an operational starting point, not a universal requirement.

### 7. Retrieve literature

Search the confirmed technology and date scope in an authoritative scientific source.

Capture:

- title;
- authors;
- journal/conference/repository;
- year and publication date where available;
- DOI;
- stable URL;
- document type;
- reason for inclusion;
- evidence-bounded summary;
- source/database;
- retrieval date; and
- limitations, including preprint or retraction status when known.

The source's default of ten displayed papers is a presentation limit. State the selection method and do not imply systematic-review completeness.

### 8. Research current news

Use the confirmed news window. Prefer primary and authoritative sources.

Capture:

- headline;
- publisher/source;
- publication date;
- event date if different;
- URL;
- company/technology tag;
- factual synopsis;
- relevance to the research question;
- retrieval date; and
- source-quality note.

Do not use search-result snippets as final evidence. Do not scrape Sogou or another search-engine result page with brittle HTML selectors.

### 9. Build analysis structures

Construct the renderer data model shown in `scripts/v2_data.sample.py`.

Required top-level structures include:

- report metadata and scope;
- section status and limitations;
- `PATENT_TOTAL_BY_COMPANY` with population metadata;
- `TREND_SERIES` with explicit date field and counting unit;
- `WORD_CLOUD` or preferably a frequency table with method;
- `PATENTS` as the record authority;
- `PATENTS_BY_COMPANY` as references to `PATENTS`;
- `SUB_TECHS` as evidence-backed categories referencing `PATENTS`;
- `LITERATURE`;
- `NEWS`; and
- `SOURCES`/provenance records.

Subtechnology groups must be explained and reproducible. Fixed branches in the source are examples only; derive categories from the current scope and document the method.

### 10. Analyze without overstating

Separate:

- observed evidence;
- calculations;
- analyst interpretation;
- uncertainty; and
- implications for the user's decision.

Do not interpret filing counts as innovation quality, market share, commercial success, enforceability, freedom to operate, or ownership without additional evidence.

For trends, identify the date field, missing periods, counting unit, and whether partial years are present. For company comparisons, disclose entity-scope differences. For topic frequencies, disclose the text field, stopword rules, normalization, and sample/population basis.

### 11. Run the validation gate

Before HTML generation, verify:

- all required scope fields exist;
- exact ISO dates are used;
- counts have source and counting-unit metadata;
- displayed counts do not exceed available selected records;
- every patent citation resolves to one `PATENTS` record;
- company and subtechnology references resolve;
- duplicate identifiers are explained or removed;
- patent URLs are connector-returned or verified global URLs;
- DOI links are validly formed;
- news URLs use `http` or `https` and have publication/source metadata;
- all summaries are escaped as text;
- no unresolved placeholder is presented as evidence;
- limitations and not-executed sections are visible; and
- the trace is complete.

Stop and repair any failed hard check.

### 12. Generate the report

Create a working copy of `scripts/v2_data.sample.py` named `v2_data.py` only in the user's approved working/output directory. This runtime artifact is not part of the skill package.

Run from that working directory:

```bash
python -B /absolute/path/to/scripts/build_report_v2.py ./technology-intelligence-briefing.html
```

The renderer must:

- write only to the user-approved path;
- never open a browser automatically;
- escape untrusted text;
- allow only safe `http`/`https` links;
- render unavailable sections honestly;
- use accessible controls and print behavior; and
- expose source and scope notes.

### 13. Complete the trace and delivery review

Fill `references/trace_template.md` with the actual execution record.

Deliver:

- the HTML report;
- the Markdown trace;
- any user-requested structured data export;
- a concise statement of coverage and limitations; and
- unresolved entity, search, evidence, or legal-status questions.

## Failure modes

### No live patent connector

Do not produce executed counts or patent findings. Deliver the confirmed scope, query plan, entity register, data schema, and execution checklist with `not_executed` status.

### Ambiguous company

Show candidate legal entities and evidence. Do not search a broad brand/group OR expression unless the user approves that scope.

### Too few relevant records

Review names, classifications, dates, jurisdictions, and exclusions. Broaden transparently and record every query revision. A small truthful population is acceptable.

### Too many or noisy records

Inspect false positives, add field restrictions or exclusions, test precision, and preserve both the broad and revised query histories.

### Missing patent detail

Leave the field unavailable and cite the available abstract/record. Never reconstruct claims or legal status.

### Literature or news unavailable

Keep the section with a visible status, reason, and recommended next step. Patent evidence cannot substitute for literature or current-news evidence.

### Renderer validation failure

Do not deliver the HTML. Repair the data or renderer, rerun checks, and record the correction.

## Quality checklist

- The question, scope, exclusions, dates, jurisdictions, and counting rule are explicit.
- Entity resolution is evidence-backed and mixed legal entities are not silently merged.
- Query construction is reproducible.
- Population and displayed sample counts are separate.
- Patent details are verified and evidence-bounded.
- Literature and news have stable locators and retrieval dates.
- Analysis distinguishes observation, calculation, interpretation, and limitation.
- HTML is accessible, responsive, print-safe, and free of unsafe raw evidence.
- The trace can reproduce every material number and citation.
- No China-only interface, directory, scraper, domain, aesthetic, or legal assumption remains.
