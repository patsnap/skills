---
name: create-patent-based-rd-briefing-rd
description: Create an evidence-bounded English patent-based R&D briefing from an authorized Excel workbook. Use when a user supplies patent records and asks to screen relevance, organize reviewed records by technology route and organization, preserve approved workbook links or figures, and generate a self-contained scientific HTML briefing with reproducible scope, review provenance, and patent-professional boundaries.
---

# Patent-Based R&D Briefing

## Purpose

Create an auditable R&D briefing from a user-authorized patent workbook. The
workflow preserves the source package's two-stage process:

1. add topic-discovery signals to the workbook;
2. render reviewer-confirmed records as a self-contained HTML briefing.

The briefing supports technical orientation, portfolio triage, competitor
monitoring, route comparison, and research-planning discussion. It does not
establish novelty, validity, enforceability, infringement, non-infringement, or
freedom to operate.

## Trigger cases

Use this skill when the user:

- asks for a patent-based technology or R&D briefing;
- supplies an authorized `.xlsx` patent export;
- wants records screened against a defined technology topic;
- wants reviewed patents organized by applicant and technology category;
- needs a portable offline HTML briefing;
- wants existing workbook patent links or embedded figures retained where safe;
- asks to reuse the BIPV or coffee-machine worked configurations;
- asks to create a new topic configuration based on reviewed scope material.

Do not invoke merely because a user mentions patents. If the user asks for a
search and supplies no workbook, perform the authorized patent search first and
build a documented evidence table before using this local rendering workflow.

## Required inputs

Collect or confirm:

1. authorized Excel workbook path;
2. topic key and technology label;
3. decision question;
4. included and excluded technical scope;
5. evidence start date and end date;
6. evidence cutoff and report date;
7. relevant jurisdictions and languages;
8. publication or family count unit;
9. reviewer identity and review date;
10. whether embedded figures may be reproduced in the report;
11. confidentiality and distribution restrictions;
12. whether patent-professional review is required before release.

Do not upload or search confidential material without authorization.

# Package topology

The localized package intentionally preserves every file in the frozen source:

```text
create-patent-based-rd-briefing-rd/
├── .gitignore
├── CHANGELOG.md
├── DISTRIBUTION.md
├── IMPROVEMENTS.md
├── LICENSE
├── requirements.txt
├── install.sh
├── SKILL.md
├── tech-report-skill-v1.1.0_<legacy-installation-note>.txt
├── config/
│   ├── BIPV_content.py
│   ├── BIPV_keywords.py
│   ├── <legacy-coffee-machine>_content.py
│   └── <legacy-coffee-machine>_keywords.py
├── examples/
│   └── SAMPLE_DATA.md
└── scripts/
    ├── generate_report.py
    ├── run.sh
    └── tag_relevant.py
```

Two filenames remain non-English only because exact source topology is a release
requirement. Their content, runtime topic key, field names, and report output are
English. Do not rename them unless the package topology is explicitly versioned.

The frozen source refers to `README.md` and `config/README.md`, but those files
are absent. Do not invent them. This file is the authoritative operating guide.

# Environment

Required:

- Python 3.9 or later;
- `pandas>=2.0.0`;
- `openpyxl>=3.1.0`;
- a local filesystem location authorized for the workbook and output;
- a human reviewer for final record inclusion.

The scripts do not install dependencies automatically and do not download
images, fonts, scripts, or other runtime assets.

# Verified PatSnap MCP mappings

The optional verified global patent connectors are:

- `advanced_patent_search` — https://open.patsnap.com/marketplace/mcp-servers/patent-search
- `patent_briefing` — https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

Use the currently exposed tool schema as authoritative. Do not copy domestic
tool names or invent parameters from the frozen source.

The local workbook workflow does not require an MCP. If a connector is missing,
record `not searched` and the resulting evidence gap. Never fabricate results.

## Patent-search use

When the user explicitly requests a search:

1. confirm scope and confidentiality;
2. use `advanced_patent_search` where available;
3. record exact queries, filters, dates, languages, requested limits, returned
   records, reviewed records, and truncation;
4. distinguish publications from simple or extended families;
5. preserve stable identifiers and links;
6. review independent claims for material technical or legal questions;
7. use `patent_briefing` only for supported synthesis;
8. export or construct the authorized workbook using the schema below.

Matched totals are not reviewed totals. A returned result page is not the global
patent universe.

# Workbook contract

## Canonical fields

The scripts accept configured aliases but normalize to:

| Canonical field | Required | Purpose |
|---|---:|---|
| `publication_number` | yes | Stable record identity |
| `title` | yes | Original or reviewed title |
| `applicant` | yes | Applicant/assignee string from the source |
| `legal_status` | recommended | Status label with separate as-of context |
| `application_date` | recommended | Filing/application date |
| `publication_date` | recommended | Publication date |
| `normalized_title` | optional | Reviewed concise title |
| `technical_problem` | optional | Evidence-grounded problem statement |
| `technical_solution` | optional | Evidence-grounded technical approach |
| `technical_effect` | optional | Reported effect, not assumed performance |
| `abstract` | optional | Abstract text used for discovery |
| `independent_claims` | recommended | Claim text or reviewed claim notes |
| `family_id` | recommended | Explicit simple-family identifier |
| `source_url` | recommended | Allowlisted HTTP(S) patent-record URL |

Configured column aliases are explicit. Do not rely on column position.

## Workflow fields

`tag_relevant.py` adds:

| Field | Meaning |
|---|---|
| `Discovery disposition` | Candidate, likely out of scope, or no configured signal |
| `Inclusive terms matched` | Exact inclusive discovery terms found |
| `Exclusion terms matched` | Exact exclusion discovery terms found |
| `Review status` | Human review state |
| `Reviewer` | Named reviewer |
| `Review date` | ISO review date |

The reviewer may add `Reviewed category IDs` using configured category IDs.

## Allowed release states

The renderer includes a record only when:

- `Discovery disposition` is `Included`, `Include`, or
  `Included — reviewer confirmed`;
- `Review status` is `Reviewed`, `Approved for briefing`, or `Complete`;
- `Reviewer` is non-empty;
- `Review date` is a valid ISO date;
- publication number, title, and applicant exist;
- category IDs, if supplied, resolve to the configured taxonomy.

Unreviewed candidates are withheld, not silently included.

# Topic configurations

## Keyword configuration

Each `_keywords.py` file defines:

- `CONFIG_VERSION`;
- `TOPIC_KEY` and `TOPIC_LABEL`;
- canonical `SEARCH_FIELDS`;
- `COLUMN_ALIASES`;
- inclusive and exclusion discovery terms;
- technology-category term sets;
- entity aliases;
- review policy.

Keyword hits are discovery evidence only. Do not label a record relevant,
novel, valuable, blocking, risky, or infringing from a keyword score.

## Content configuration

Each `_content.py` file defines:

- report scope and exclusions;
- current-awareness records approved for publication;
- migrated source discovery leads that remain withheld;
- organization discovery leads;
- technology categories and decision questions;
- release requirements.

The frozen source included future-dated news, market percentages, technical
summaries, category totals, and leadership claims without a frozen evidence
register. These have been preserved as clearly unverified discovery leads or
source-example publication lists, not release facts.

## Creating another topic

Do not add source-absent files to this package without user approval. If a user
explicitly approves a new topic configuration:

1. choose an ASCII topic key;
2. create both keyword and content configurations;
3. define canonical aliases and scope;
4. define category IDs and ensure both files agree;
5. document discovery terms and exclusions;
6. avoid embedded factual claims without evidence IDs;
7. validate with a small reviewed workbook;
8. update package topology and version documentation.

# End-to-end workflow

## Phase 1 — Scope and authorization

1. Confirm the user has authority to process the workbook.
2. Record the decision question.
3. Define mechanisms, applications, dates, regions, and languages.
4. Define exclusions and adjacent routes.
5. Select the count unit.
6. Record confidentiality and distribution limits.
7. Establish reviewer and patent-professional responsibilities.

Do not silently treat a domestic or single-language export as global coverage.

## Phase 2 — Inspect and normalize the workbook

1. Confirm `.xlsx` format.
2. Read headers before modifying data.
3. Resolve canonical fields through the topic aliases.
4. reject missing required fields;
5. identify duplicate publication numbers;
6. assess family and applicant normalization;
7. inspect links and embedded-image rights;
8. preserve the source workbook unchanged.

The tagging script writes a separate output workbook and refuses overwrite by
default.

## Phase 3 — Add discovery signals

Run:

```bash
python -B scripts/tag_relevant.py \
  input.xlsx \
  tagged.xlsx \
  BIPV
```

For the second source example, use topic key `coffee-machine`.

Optional reviewed metadata:

```bash
python -B scripts/tag_relevant.py \
  input.xlsx \
  tagged.xlsx \
  BIPV \
  --reviewer "Reviewer name" \
  --review-date 2026-08-08
```

This metadata does not by itself approve records. The reviewer must still set
the disposition and status.

## Phase 4 — Human relevance review

For every candidate:

1. read the title and abstract;
2. review relevant independent claims for material findings;
3. verify technical scope and exclusions;
4. distinguish applicant, current owner, and corporate group;
5. identify duplicate publications or family members;
6. verify status only from an appropriate current source;
7. assign zero or more reviewed category IDs;
8. record inclusion/exclusion reason;
9. name the reviewer and review date.

Do not use a target percentage such as 30–60% as a quality criterion. Relevance
rates depend on the search universe and decision question.

## Phase 5 — Build the briefing

Run:

```bash
python -B scripts/generate_report.py \
  tagged.xlsx \
  briefing.html \
  BIPV \
  2026-01-01 \
  2026-03-31 \
  --report-date 2026-04-02 \
  --evidence-cutoff 2026-03-31
```

The renderer:

- loads only bounded package configurations;
- validates topic/config agreement;
- withholds unreviewed records;
- rejects duplicate included publication numbers;
- derives counts from included records;
- separates publication and recorded family counts;
- escapes all workbook/config text;
- allowlists HTTP(S) links;
- extracts only bounded embedded images associated with included publications;
- performs no network requests;
- emits no script or external stylesheet;
- writes atomically and refuses overwrite by default;
- produces English static HTML with print rules.

## Phase 6 — Review the HTML

Review:

- title, topic, period, cutoff, and version;
- included-record count;
- publication/family count-unit labels;
- organization strings and aliases;
- category assignments;
- technical problem/approach/effect wording;
- legal-status dates and limitations;
- patent links;
- embedded-image rights and accuracy;
- legal and evidence boundaries;
- narrow-screen and print layout;
- confidentiality and distribution.

## Phase 7 — Release or withhold

Release only when:

- all included records have review provenance;
- material technical findings trace to evidence;
- search scope and limitations are disclosed;
- entity/family treatment is clear;
- specialist review is complete or explicitly pending;
- HTML is free of placeholders and temporary paths;
- output is approved for its intended audience.

# Report structure

The localized HTML includes:

1. report metadata;
2. scope, method, and boundaries;
3. reviewed-dataset metrics;
4. applicant activity within the reviewed dataset;
5. configured technology categories;
6. reviewed patent cards;
7. unclassified-review queue where applicable;
8. evidence register;
9. next-review actions;
10. legal and coverage disclaimer.

The source's industry-news, company, and category modules remain conceptually
preserved, but only evidence-backed content may be published. Empty or withheld
modules must not be filled with source-example assertions.

# Scientific editorial design

Use:

- light paper and canvas colors;
- restrained navy and blue accents;
- system fonts;
- accessible contrast;
- consistent tables and units;
- concise cards for homogeneous records;
- clear captions and evidence boundaries;
- responsive and print-safe layout.

Avoid:

- gradients and neon decoration;
- remote hero images;
- Google Fonts or other external runtime;
- hover-only navigation;
- decorative emojis;
- unlabelled charts;
- arbitrary “Top 20” lists;
- color as the sole meaning carrier.

# Evidence interpretation rules

## Counts

Always label whether a number represents:

- matched records;
- returned records;
- reviewed records;
- included publications;
- simple families;
- applicants;
- categories;
- current-awareness events.

Configured source-example counts are never authoritative.

## Organizations

Patent activity in the reviewed workbook is not proof of:

- technical leadership;
- product performance;
- manufacturing capability;
- market share;
- ownership of all family members;
- freedom to operate.

Normalize aliases and corporate relationships when material.

## Categories

Category-term hits are proposed classifications. The reviewer confirms category
assignment. A record may belong to multiple categories. An empty category means
no included record was assigned in this reviewed workbook, not global absence.

## Legal status

Record the source and as-of date. Status labels may be incomplete, delayed, or
jurisdiction-specific. Do not infer enforceability from a simple status field.

## Claims and legal conclusions

Read relevant independent claims and required context. The report may summarize
technical claim relevance but must not automate infringement or FTO conclusions.
Escalate material questions to a qualified patent professional.

# Failure handling

If a configuration is missing:

- report the exact topic key;
- list available supported keys where safe;
- do not dynamically load an arbitrary path;
- do not create a new file without approval.

If the workbook lacks required fields:

- list the missing canonical fields;
- request an updated export or approved alias mapping;
- do not infer values from column position.

If no record is reviewer-confirmed:

- retain the tagged workbook;
- withhold the HTML report;
- explain the review fields required.

If an image cannot be extracted:

- show a neutral no-reviewed-figure state;
- do not download a replacement;
- do not misassociate images by fixed column position.

If an output exists:

- refuse overwrite by default;
- use `--overwrite` only after confirming the exact target;
- never delete unrelated files.

# Security and privacy

- Treat workbook values as untrusted text.
- Escape text and attributes.
- Allow only HTTP(S) external links.
- Do not execute workbook macros.
- Do not load arbitrary configuration paths.
- Do not expose local paths in released HTML.
- Do not transmit the workbook to external services without authorization.
- Bound embedded-image size and count.
- Do not add analytics, pixels, or remote assets.
- Remove temporary and cache files after testing.

# Quality checks

Before release:

```bash
python -B -c "import ast, pathlib; [ast.parse(pathlib.Path(p).read_text(encoding='utf-8')) for p in ['scripts/tag_relevant.py', 'scripts/generate_report.py']]"
bash -n install.sh
bash -n scripts/run.sh
```

Then run a representative end-to-end fixture and negative tests for:

- missing required fields;
- invalid topic key;
- path traversal;
- existing output refusal;
- unreviewed candidate withholding;
- missing reviewer;
- invalid review date;
- duplicate publication number;
- unknown category ID;
- unsafe URL removal;
- HTML escaping;
- no external script, stylesheet, gradient, or network dependency;
- no cache or temporary artifact in the package.

# Deliverables

Provide:

1. tagged workbook containing discovery and review fields;
2. self-contained HTML briefing containing only confirmed records;
3. concise handoff with scope, dates, count unit, included count, evidence gaps,
   specialist-review status, and output paths.

Do not create additional package files without authorization.

# Handoff language

State:

- “Keyword matches were used as discovery signals and reviewed before use.”
- “Counts describe the documented reviewed workbook.”
- “The report is not legal advice.”
- “Patent-professional review remains required for material claim, status, FTO,
  validity, enforceability, and infringement questions.”

Never describe the report as exhaustive, legally cleared, globally complete, or
proof that no relevant patents exist.
