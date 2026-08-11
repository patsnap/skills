# Implementation and Localization Notes

This document preserves the source package's problem/solution record while
explaining the global, evidence-safe implementation now used.

## 1. Workbook hyperlinks were lost

### Source problem

The early implementation read a workbook with pandas and wrote a replacement
with `DataFrame.to_excel()`. Cell hyperlinks, drawings, and formatting were not
preserved.

### Source correction retained

The tagging stage now:

1. reads values with pandas for analysis;
2. copies the original workbook to a separate output;
3. opens the copy with openpyxl;
4. appends review fields;
5. saves the copied workbook.

This approach preserves supported workbook metadata more reliably than
reconstructing the workbook from a DataFrame.

### Localized refinements

- Input and output paths must differ.
- Existing output is refused unless `--overwrite` is explicit.
- Required columns resolve through aliases, not fixed positions.
- Existing workflow columns are updated instead of duplicated.
- Save failure removes the partial output.
- The source workbook is never modified.

### Remaining limitations

openpyxl does not preserve every possible Excel feature. Test workbooks that use:

- macros;
- advanced drawings;
- external data connections;
- unsupported charts;
- digital signatures;
- vendor-specific metadata.

The skill does not promise bit-for-bit workbook preservation.

## 2. Embedded patent figures were lost or mismatched

### Source problem

Rewriting through pandas removed embedded images. The source then extracted
images from a fixed column and matched publication numbers from another fixed
column, making export-layout changes risky.

### Localized solution

The report generator:

1. resolves the publication-number column by configured aliases;
2. maps worksheet rows to publication numbers;
3. reads image anchors by row rather than assuming an image column;
4. keeps images only for included publications;
5. supports PNG and JPEG data URIs;
6. limits each image to 5 MB;
7. limits extraction to 200 images;
8. provides descriptive alt text;
9. shows a neutral empty state when extraction fails.

### Why no generic hero image

The source downloaded an Unsplash coffee image at report time. That introduced:

- network dependency;
- privacy and logging concerns;
- licensing uncertainty;
- nondeterministic output;
- a topic-specific image in a general skill;
- large HTML payloads;
- failure modes unrelated to patent analysis.

The localized renderer performs no network request. A reviewed embedded figure
may be used only when supplied in the authorized workbook.

### Rights boundary

Technical ability to extract an image does not establish reproduction rights.
The report owner must verify license, confidentiality, and audience permissions.

## 3. Technology categories contained too few patents

### Source problem

Each source category configured only two to five publication numbers. To make
the page look fuller, the source introduced keyword-count scores and filled each
category to a fixed Top 20.

### Why the source correction was analytically unsafe

- Match count is sensitive to text length.
- Related terms can be redundant.
- Title, abstract, solution, and claim text have different evidentiary weight.
- Long records can score higher without being more relevant.
- No score calibration or reviewer decision was retained.
- Fixed Top 20 is a presentation quota, not an analytical threshold.
- Configured representative publications could be absent from the workbook.
- The hard-coded category dictionary covered only the coffee example.

### Localized solution

Category keywords now create proposed category signals. The reviewer can assign
one or more `Reviewed category IDs`. The generator:

- accepts explicit category IDs first;
- validates IDs against the content taxonomy;
- uses configured keyword categories only as fallback organization;
- never converts a score into legal or technical significance;
- displays every included record assigned to a category;
- preserves an unclassified reviewed-record section;
- derives category counts from actual included records;
- uses no Top-N quota.

### Interpretation boundary

An empty category means no included workbook record was assigned. It is not
evidence of global patent whitespace or an opportunity.

## 4. News links were not clickable

### Source correction retained conceptually

Current-awareness records may include a stable URL and should link to the
reviewed source.

### Localization issue

The source content configurations contained future-dated articles, commercial
pages, social posts, percentages, and summaries without a frozen source
register or verification record.

### Localized solution

- `CURRENT_AWARENESS` is empty by default.
- Source items remain in `SOURCE_NEWS_DISCOVERY_LEADS`.
- Every lead is marked unverified and not allowed for publication.
- Each lead states the verification action required.
- A release workflow must add reviewed evidence IDs, dates, source type, scope,
  and limitations before publishing the information.

### URL safety

The HTML renderer allows only absolute HTTP(S) links with a network location.
Local paths, JavaScript URLs, data URLs supplied as links, and other schemes are
omitted.

## 5. Decorative hero background

### Source intent

Improve visual appeal and preserve an image in a portable HTML file.

### Localized design decision

The hero download and gradient overlays were removed. The report now uses:

- white paper;
- light gray canvas;
- restrained navy and blue;
- system fonts;
- visible table borders;
- accessible text hierarchy;
- print rules;
- no external runtime.

This better fits a mainstream scientific and technical briefing and keeps
attention on evidence.

## 6. Raw HTML interpolation

### Source risk

The source concatenated topic, configuration, and workbook values directly into
HTML. Untrusted text could break markup or inject content.

### Localized solution

- All ordinary text and attributes pass through HTML escaping.
- Patent URLs pass through scheme/netloc allowlisting.
- Category IDs are validated against configuration.
- Configuration paths are bounded inside the package.
- Topic keys allow only ASCII letters, numbers, underscores, and hyphens.
- No script executes in the output.
- No unsafe DOM API exists.

### Embedded images

Only image bytes extracted from the workbook are converted to bounded PNG/JPEG
data URIs. Workbook text cannot specify an arbitrary image data URI.

## 7. Domestic-only workbook columns

### Source behavior

The scripts expected domestic export headers and status labels. Some fields were
found by positional assumptions.

### Localized solution

Each topic configuration defines canonical fields and English/global aliases.
Required canonical fields are:

- publication number;
- title;
- applicant.

Recommended fields include dates, legal status, normalized title, technical
problem, solution, effect, abstract, independent claims, family ID, and source
URL.

An unsupported header requires an approved alias. The code never guesses by
column position.

## 8. Keyword hit treated as “high relevance”

### Source behavior

Any inclusive term marked a record high relevance unless an exclusion term
appeared. Rows were colored bright yellow and the high-relevance percentage was
reported as a quality indicator.

### Localized solution

The tagging stage creates four transparent discovery outcomes:

- candidate with inclusive signal;
- candidate with inclusive and exclusion signals;
- likely out of scope with exclusion signal;
- no configured signal.

It records the exact terms found. Human review determines final inclusion.

### Why this matters

Keyword results can miss synonyms, older terminology, translations, drawings,
claims, and context. Exclusion terms can also occur in comparison passages. A
human decision is necessary.

## 9. No explicit review provenance

### Localized requirement

Included records require:

- accepted disposition;
- accepted review status;
- named reviewer;
- valid ISO review date;
- required bibliographic fields;
- valid category IDs if provided.

The generator withholds records that fail these gates and rejects an included
record with missing reviewer/date.

### Benefits

- review accountability;
- reproducible updates;
- clearer draft/release distinction;
- safer automation;
- easier dispute resolution.

## 10. Publication and family counts were conflated

### Localized solution

The briefing reports included publication records. It reports a distinct family
count only when explicit family IDs are available.

It does not infer families from publication numbers, titles, applicants, or
priority-like similarities.

### Required disclosure

Search and report documentation should state:

- publication or family unit;
- simple or extended family definition;
- deduplication rule;
- missing family-ID treatment;
- jurisdiction and language scope;
- database and date.

## 11. Activity volume implied leadership

### Source risk

Company cards combined configured technical summaries and patent lists, which
could read as verified leadership or capability conclusions.

### Localized solution

The report presents applicant-string counts only within the reviewed workbook.
It explicitly says activity volume is not proof of:

- leadership;
- product performance;
- manufacturing capability;
- market share;
- corporate ownership;
- legal clearance.

Source organization/publication lists remain discovery leads until verified.

## 12. Legal status and claims lacked boundaries

### Localized solution

- Status is shown as a workbook value and may be absent.
- Material status claims require a source and as-of date.
- Claim relevance requires independent claim review.
- The report contains a prominent not-legal-advice notice.
- Patent-professional review is required for material FTO, infringement,
  validity, enforceability, and claim-construction questions.

No keyword score becomes a legal-risk percentage.

## 13. Installation was product-specific and destructive

### Source behavior

The installer targeted a product-specific hidden directory, asked whether to
overwrite, then moved the old directory. Earlier distribution guidance included
recursive deletion.

### Localized solution

- `--target` is mandatory.
- Root or unresolved targets are refused.
- Existing target is moved only after typing `BACKUP`.
- Backup uses a timestamped sibling path.
- No recursive delete is issued.
- Dependency installation is opt-in.
- Package copy and dependency installation are separate decisions.

## 14. Runtime installed dependencies automatically

### Source risk

`run.sh` invoked pip when imports failed. This changed the environment during a
report task and could access the network unexpectedly.

### Localized solution

The runner checks dependencies and stops with instructions. Only the installer,
with `--install-dependencies`, may invoke pip.

## 15. Dates and output paths were ambiguous

### Localized solution

- Start, end, report, review, and cutoff dates use `YYYY-MM-DD`.
- Start cannot be after end.
- Output filenames use readable ISO ranges.
- Existing outputs are refused.
- HTML writes use a sibling temporary file and atomic replacement.
- No local path is rendered into the report.

## 16. Source documentation referenced missing files

The frozen source repeatedly references `README.md` and `config/README.md`, but
neither exists. The localized migration:

- records the discrepancy;
- does not create either file;
- points users to `SKILL.md` and `examples/SAMPLE_DATA.md`;
- preserves exact source file topology.

## 17. Verified MCP mapping

Optional global mappings:

- patent search: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- patent briefing: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

The current connector schema is authoritative. The scripts do not assume a
connector is installed and do not embed credentials or MCP configuration files.

## 18. Testing strategy

### Static checks

- Python AST parse without bytecode;
- shell syntax check;
- exact source/target topology;
- target/source line parity;
- CJK content scan;
- domestic-domain scan;
- gradient/external-runtime scan;
- unsafe DOM scan;
- credential/path/cache scan.

### Positive runtime checks

- synthetic workbook creation;
- discovery signal creation;
- workbook metadata preservation check;
- reviewer confirmation;
- category assignment;
- self-contained HTML generation;
- HTML parser acceptance;
- included record appears;
- unreviewed record is withheld;
- no external script or gradient.

### Negative checks

- path traversal topic key;
- missing configuration;
- missing required field;
- existing output;
- no reviewed record;
- missing reviewer;
- invalid review date;
- duplicate publication number;
- unknown category;
- unsafe URL;
- raw HTML escaping.

## 19. Recommended operating sequence

1. Frame decision and scope.
2. Prepare authorized workbook.
3. Record search methodology.
4. Run discovery tagging.
5. Review records and claims.
6. Normalize families/entities.
7. Assign categories.
8. Generate static briefing.
9. Inspect HTML and evidence register.
10. Obtain specialist review.
11. Approve or withhold release.

## 20. Residual limitations

Even after localization, quality depends on:

- search coverage;
- database scope and lag;
- multilingual recall;
- export completeness;
- claim and status review;
- family normalization;
- entity normalization;
- reviewer judgment;
- image rights;
- workbook feature compatibility;
- downstream browser and print behavior.

The package exposes these limitations; it cannot eliminate them automatically.

## Related files

- `SKILL.md` — workflow and policies
- `scripts/tag_relevant.py` — auditable discovery tagging
- `scripts/generate_report.py` — static report generator
- `scripts/run.sh` — reviewed orchestration
- `examples/SAMPLE_DATA.md` — workbook schema
- `DISTRIBUTION.md` — package release checklist

No source-absent file is added.
