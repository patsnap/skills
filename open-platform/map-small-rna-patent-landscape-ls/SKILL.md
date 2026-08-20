---
copyright: "Copyright © Patsnap. All rights reserved."
name: map-small-rna-patent-landscape-ls
description: Build a company or portfolio-level patent landscape for small-RNA therapeutics from a supplied patent list or defined search scope. Use when a user wants full patent records, an ASO/siRNA/mRNA or oligonucleotide portfolio analysis, a structured XLSX evidence workbook, a small-RNA technology taxonomy, or an interactive multidimensional patent timeline.
---

# Map a Small-RNA Patent Landscape

## Purpose

Transform patent publication/application/grant identifiers or a defined company/technology scope into a traceable small-RNA patent landscape. The standard deliverable set is:

- a local Markdown corpus of retrieved patent records;
- a structured JSON/CSV analysis layer;
- an XLSX workbook for analyst and stakeholder review;
- an interactive, self-contained HTML timeline with multidimensional lanes, filters, evidence cards, distribution summaries, strategy findings, and evidence-triggered opportunity markers.

Use English for global delivery unless the user requests another language. Preserve original-language claims and abstracts with labeled translations.

## Read the package resources

1. `references/tag-taxonomy.md`
2. `references/workbook-schema.md`
3. `references/html-dashboard.md`

Use `scripts/create_landscape_project.py` only to create a new, version-safe project scaffold. It does not retrieve or analyze patents.

## Scope gate

Confirm or state:

- company/portfolio and verified legal-name aliases;
- supplied patent list or reproducible discovery query;
- small-RNA modalities in scope: ASO, siRNA, miRNA, mRNA, aptamer, guide RNA, other oligonucleotide;
- technology layers: sequence/target, chemistry, conjugate/delivery, formulation, manufacturing, use, biomarker, dose, diagnostics;
- jurisdictions, languages, date cutoff, and legal-status scope;
- counting unit: exact publications, applications, simple families, or extended families;
- stakeholder questions and comparison baseline;
- confidentiality and external-service permissions;
- required Markdown, JSON/CSV, XLSX, and HTML outputs.

Do not silently default to one company case, one disease set, or a Chinese audience.

## MCP and evidence routing

Use supplied authoritative records when complete. For live patent retrieval, use:

- `advanced_patent_search` for number, nested, semantic, field, applicant, count, and keyword-assisted retrieval: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- `patent_briefing` for bibliography, family, legal status, claims, description, translations, drawings, and technical summaries: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

Use target, drug, trial, translational, regulatory, company/deal, sequence, or chemical structure services only when relevant, authorized, and actually exposed. Do not invent legacy connector names or capabilities. Verify material legal status in official registers where the analysis relies on enforceability or term.

## Workflow

### 1. Normalize patent input

- accept one identifier per line, spreadsheet column, pasted list, or structured export;
- preserve the user's original order and exact input;
- normalize whitespace, punctuation, country code, number, and kind code without destroying the original;
- resolve identifiers through an exact patent-number lookup;
- do not blindly append `A/A1/A2/B/B1/B2` across jurisdictions—the meaning and valid kind codes differ;
- log each attempted resolution, matched record, confidence, source, timestamp, and failure reason;
- keep application, publication, and grant identifiers distinct.

Outputs: `patent_numbers.txt`, `fetch_summary.csv`, and `fetch_summary.json`.

### 2. Retrieve patent records

For each resolved publication/member, retrieve as available:

- bibliography and stable source URL;
- title and abstract;
- current claims and claim version;
- description and sequence-listing references;
- applicant/assignee and inventors;
- priority, filing, publication, and grant dates;
- family and continuity members;
- legal status and event source/date;
- CPC/IPC;
- drawings/figures where required.

Save one Markdown evidence file per exact retrieved record under `patent_markdowns/`. Name files by normalized publication number plus kind code. Include source identifier, retrieval timestamp, and missing fields.

If claims are missing, do not silently substitute another family member's claims. Store the alternate member/version separately, explain the relationship and reason, and never treat it as the controlling claim of the missing member.

### 3. Build the structured analysis layer

Create one record per selected counting unit and nested member/claim/source data. Preserve:

- input order and resolution log;
- exact publication/member and family definition;
- source URLs and retrieval dates;
- company/entity normalization with evidence;
- original/translated text distinction;
- missing, unknown, not applicable, and zero values;
- tags with evidence and confidence;
- analysis conclusions and uncertainty;
- human-review state.

Generate `patent_analysis_rows.json` and optionally CSV before XLSX/HTML. Both deliverables must derive from the same structured layer.

### 4. Apply the small-RNA taxonomy

Use `references/tag-taxonomy.md`. Preserve expert and stakeholder-readable tags across:

- technology direction;
- target/asset or platform subdivision;
- mechanism;
- RNA modality;
- chemistry/structure;
- delivery/tissue;
- productization stage;
- patent/claim type;
- evidence-backed review priority.

Do not use “first/second/third generation” as the primary axis unless the user supplies a defined convention. Modern portfolios are more usefully interpreted by asset/disease, mechanism, chemistry, delivery, manufacturing/formulation, use, and productization.

Tags are multi-label where appropriate. Each assignment needs evidence, source locator, confidence, and reviewer state. Do not infer chemical modification, delivery, clinical stage, or claim strength from the title alone.

### 5. Analyze strategy

Create a second analytical layer:

- priority patent evidence chains;
- portfolio gap matrix;
- R&D hypothesis cards;
- peer/leader filing playbook comparison;
- strategy recommendations with owner/timing;
- contradictions and missing evidence.

Opportunity markers are analyst hypotheses, never patent records. Generate them only when observed portfolio evidence, competitor comparison, technology feasibility, business relevance, and uncertainty support them. Do not always insert CNS, ophthalmic, kidney, NMD, cryptic-exon, formulation, or patient-selection opportunities merely because they appeared in the source case.

### 6. Generate XLSX

Use `references/workbook-schema.md`.

The full workbook includes:

1. `Strategy Summary`
2. `Priority Patent Evidence`
3. `Portfolio Gap Matrix`
4. `R&D Hypothesis Cards`
5. `Peer Filing Playbooks`
6. `Patent Strategy Master`
7. `Timeline Tag Data`
8. `Methodology`

A lighter first pass may use the documented five-sheet alternative. Do not omit methodology and source/gap fields.

Apply professional spreadsheet conventions:

- frozen header, filters, wrapped text, stable column widths, source hyperlinks;
- tables rather than decorative merged cells;
- text-plus-color status labels;
- formulas where useful, no hidden unexplained constants;
- explicit units, dates, denominators, and counting rules;
- no missing-as-zero behavior.

Render or inspect every sheet, verify names, dimensions, formulas, links, and sample rows.

### 7. Generate HTML timeline

Use `references/html-dashboard.md`.

The default view should be the most stakeholder-readable evidence-backed technology direction, not raw gene names. Provide switches for:

- technology direction;
- mechanism;
- RNA modality;
- chemistry/structure;
- delivery/tissue;
- productization stage.

Provide filters for trend/review priority, active-dimension tag, jurisdiction/status if useful, and free-text search across publication number, title, mechanism, chemistry, delivery, entities, and countries.

Use earliest verified family publication year for family-level timelines; otherwise use the current record's publication year and label the fallback. Never place a patent or opportunity marker in a fabricated future year.

Patent cards and evidence panels must include source-backed fields and distinguish:

- current member publication date from earliest family publication;
- current member status from family status summary;
- claim evidence from description inference;
- observed portfolio evidence from analyst opportunity hypotheses.

### 8. Validate

#### Evidence

- reconcile inputs, resolved records, exact publications, families, tags, counts, and outputs;
- verify source URLs and retrieval dates;
- sample claim, chemistry, delivery, status, family, and strategy assignments;
- confirm missing claims are not silently replaced;
- confirm opportunity markers have explicit evidence and uncertainty.

#### XLSX

- open/render every sheet;
- verify expected names, row/column counts, filters, frozen panes, formulas, hyperlinks, and no spreadsheet errors;
- inspect wide/wrapped cells and stakeholder readability.

#### HTML

- parse HTML and verify data schema;
- test default and every alternate dimension;
- test filters, search, hover/focus cards, opportunity markers, keyboard navigation, narrow viewport, and print;
- ensure no external dependency, credential, absolute path, legacy domestic domain, or missing asset;
- confirm static report content remains usable without JavaScript where practical.

Record static versus browser validation honestly.

## Naming and project outputs

Use a new project directory and stable subpaths:

```text
<company-slug>-small-rna-landscape/
  landscape_config.json
  patent_numbers.txt
  patent_markdowns/
  outputs/intermediate/fetch_summary.csv
  outputs/intermediate/fetch_summary.json
  outputs/intermediate/patent_analysis_rows.json
  outputs/patent_analysis/<company-slug>_patent_landscape.xlsx
  outputs/patent_analysis/<company-slug>_multidimensional_patent_timeline.html
```

Do not overwrite a non-empty project. Version reruns or use a new directory.

## Quality gates

- [ ] Source input order and resolution attempts are preserved.
- [ ] Identifier matching is jurisdiction-aware and exact.
- [ ] Every Markdown record identifies source/member/version/retrieval date.
- [ ] Family and legal-status evidence is current or explicitly missing.
- [ ] Claim substitution is never silent.
- [ ] All tag assignments have evidence/confidence.
- [ ] Expert and stakeholder-readable tags remain distinct but mapped.
- [ ] Workbook and HTML derive from the same structured data.
- [ ] Strategy findings and opportunity markers are evidence-based, not preloaded conclusions.
- [ ] XLSX and HTML pass structural and visual checks.
- [ ] Output is English-localized and uses a restrained scientific format.
- [ ] No invented patent, status, tag, opportunity, source, or MCP capability appears.

## Boundaries

This is a landscape and strategy workflow, not an FTO, infringement, validity, or patentability opinion. Review material legal conclusions with qualified counsel.
