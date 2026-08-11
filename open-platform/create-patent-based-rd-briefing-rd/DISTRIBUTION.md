# Distribution and Release Guide

This guide governs packaging and review of the localized patent-based R&D
briefing skill. It replaces source guidance that described files as missing even
though some were later present, and it does not create the README files absent
from the frozen source.

## Release objective

Distribute one self-contained skill package that:

- preserves all 17 frozen-source files and relative paths;
- contains English/global content even where two legacy filenames are retained;
- supports BIPV and coffee-machine worked configurations;
- tags discovery signals without automatic relevance conclusions;
- renders only reviewer-confirmed records;
- produces static scientific HTML without network runtime;
- accurately documents optional global PatSnap MCP mappings;
- contains no patent data, secrets, cache, or generated reports.

## Authoritative topology

The package must contain exactly:

```text
.gitignore
CHANGELOG.md
DISTRIBUTION.md
IMPROVEMENTS.md
LICENSE
requirements.txt
install.sh
SKILL.md
tech-report-skill-v1.1.0_<legacy-installation-note>.txt
config/BIPV_content.py
config/BIPV_keywords.py
config/<legacy-coffee-machine>_content.py
config/<legacy-coffee-machine>_keywords.py
examples/SAMPLE_DATA.md
scripts/generate_report.py
scripts/run.sh
scripts/tag_relevant.py
```

The angle-bracket labels above describe legacy non-English filenames without
copying non-English text into localized content. Compare actual paths directly
against the frozen source during audit.

## Files intentionally not added

The frozen source mentions but does not contain:

- `README.md`;
- `config/README.md`;
- `CONTRIBUTING.md`;
- template files;
- example `.xlsx` data;
- checked-in tests;
- MCP configuration files;
- agent UI metadata.

Do not add them without explicit approval and a topology/version decision.

## File responsibilities

### `SKILL.md`

- trigger conditions;
- scope and authorization;
- workbook contract;
- reviewed workflow;
- verified MCP links;
- evidence and legal boundaries;
- commands, failure handling, QA, and handoff.

### `scripts/tag_relevant.py`

- bounded configuration loading;
- canonical field resolution;
- inclusive/exclusion discovery signals;
- review-field creation;
- workbook-copy preservation;
- overwrite protection.

### `scripts/generate_report.py`

- review-gate enforcement;
- duplicate/category/date validation;
- derived metrics;
- bounded embedded-image extraction;
- URL allowlisting and HTML escaping;
- self-contained scientific HTML;
- atomic output.

### `scripts/run.sh`

- argument/date/config/dependency checks;
- non-destructive output planning;
- tagging;
- explicit human-review pause;
- HTML generation;
- evidence/legal handoff.

### Topic configurations

- canonical fields and aliases;
- discovery terms and exclusions;
- technology taxonomy;
- report scope;
- source-example discovery leads;
- release requirements.

### Documentation

- `CHANGELOG.md`: source history and localized release changes;
- `IMPROVEMENTS.md`: implementation rationale and residual limits;
- `examples/SAMPLE_DATA.md`: safe synthetic schema guidance;
- this file: distribution gates;
- legacy installation note: archive/manual installation guidance.

### Installation and dependencies

- `install.sh`: explicit-target, backup-first installer;
- `requirements.txt`: minimal Python dependencies;
- `LICENSE`: source-provided MIT license;
- `.gitignore`: generated-data, cache, secret, and editor exclusions.

## Distribution modes

### Mode 1 — Reviewed repository

1. Create or select an authorized repository.
2. Copy the exact package directory.
3. Verify no workbook or report is present.
4. Run all gates in this guide.
5. Commit with localization version and source hash record.
6. Tag only after review approval.
7. Publish release notes with residual limitations.

Do not use placeholder repository URLs from the source package.

### Mode 2 — Tar archive

From the parent directory:

```bash
tar -czf create-patent-based-rd-briefing-rd-v1.1.0-localized.tar.gz \
  create-patent-based-rd-briefing-rd/
```

Then inspect the archive:

```bash
tar -tzf create-patent-based-rd-briefing-rd-v1.1.0-localized.tar.gz
```

Compare the list to authoritative topology.

### Mode 3 — ZIP archive

```bash
zip -r create-patent-based-rd-briefing-rd-v1.1.0-localized.zip \
  create-patent-based-rd-briefing-rd/
```

Inspect contents before distribution.

### Mode 4 — Marketplace preparation

Marketplace submission is a separate activity. Confirm:

- target platform packaging requirements;
- whether UI metadata is required;
- license and attribution;
- MCP declaration format;
- security review;
- versioning and update process;
- support ownership.

Do not add marketplace-only files to this source-faithful package without an
approved topology change.

## Installation behavior review

The installer requires:

```bash
bash install.sh --target <selected-directory>
```

Optional dependency installation:

```bash
bash install.sh \
  --target <selected-directory> \
  --install-dependencies
```

Release reviewers must confirm:

- target is explicit;
- root/unresolved target is refused;
- existing target is not deleted;
- `BACKUP` confirmation is required;
- backup is timestamped;
- dependency installation is opt-in;
- Python absence is reported clearly;
- scripts receive executable permissions;
- missing README is not promised.

## Runtime behavior review

### Topic keys

Supported source examples:

- `BIPV`
- `coffee-machine`

Topic keys must contain only ASCII letters, numbers, hyphens, and underscores.
The second key maps internally to a legacy filename while maintaining English
runtime input.

### Dates

All runtime dates use `YYYY-MM-DD`:

- evidence start;
- evidence end;
- report date;
- evidence cutoff;
- review date.

### Outputs

- tagged workbook is separate from source workbook;
- HTML output is separate;
- outputs are refused when already present;
- report write is atomic;
- no report or tagged workbook belongs in the distribution archive.

## Source-data exclusion gate

Search the package for:

- `.xlsx`, `.xls`, `.csv`, or generated HTML;
- real exported patent datasets;
- confidential organization summaries;
- personal names not required by source/license;
- API keys, tokens, passwords, cookies, or environment files;
- test fixtures;
- Base64 data unrelated to source code;
- local absolute paths;
- temporary files and logs.

The example guide may contain fictional identifiers and public database home
URLs, but no real decision dataset.

## Localization gate

Inspect content for:

- CJK characters;
- domestic-only product or platform language;
- domestic domains;
- home-market-versus-overseas framing;
- local legal-status labels;
- local installation paths;
- local fonts;
- untranslated comments, UI text, errors, and examples;
- non-ISO dates;
- unexplained acronyms.

Legacy filenames themselves are preserved by topology and should be excluded
from content-character conclusions, but their file contents must be English.

## Evidence-quality gate

Confirm documentation and runtime behavior distinguish:

- search match from review;
- candidate from included record;
- publication from patent family;
- applicant string from normalized corporate entity;
- status label from current verified legal status;
- technical claim relevance from infringement/FTO;
- source report from analyst inference;
- configured discovery lead from published current-awareness fact;
- expected effect from measured performance;
- reviewed-dataset absence from global whitespace.

## Patent-professional boundary gate

The package must not claim:

- confirmed FTO;
- non-infringement;
- infringement probability;
- validity or invalidity;
- enforceability;
- legal clearance;
- no relevant patents exist;
- global white space.

The HTML must contain:

- `not legal advice`;
- `patent professional`;
- reviewed-workbook coverage boundary;
- legal-status and claim-review follow-up.

## MCP gate

Only verified optional mappings are documented:

- `advanced_patent_search`:
  https://open.patsnap.com/marketplace/mcp-servers/patent-search
- `patent_briefing`:
  https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

Confirm:

- links resolve to the intended server listing;
- no domestic connector URL remains;
- no unavailable tool name or parameter is claimed;
- current exposed schema is declared authoritative;
- connectors are optional;
- no credential is included;
- no source-absent MCP file is added.

## Static-code gate

Run Python parsing without bytecode:

```bash
python -B -c "import ast, pathlib; [ast.parse(pathlib.Path(p).read_text(encoding='utf-8')) for p in ['scripts/tag_relevant.py','scripts/generate_report.py']]"
```

Run shell syntax checks:

```bash
bash -n install.sh
bash -n scripts/run.sh
```

Inspect for:

- arbitrary configuration imports;
- path traversal;
- unescaped HTML;
- unsafe URL schemes;
- raw DOM injection;
- network downloads;
- external scripts/stylesheets/fonts;
- gradients;
- automatic dependency installation in runtime;
- destructive deletion;
- silent overwrite;
- broad recursive moves.

## End-to-end gate

Create a temporary synthetic workbook containing:

1. one in-scope BIPV record;
2. one out-of-scope record;
3. required canonical fields;
4. safe source URL;
5. optional family ID;
6. optional embedded figure.

Then:

1. run tagging;
2. verify terms and candidate status;
3. set one record to included/reviewed;
4. name reviewer and ISO review date;
5. assign a valid category ID;
6. generate HTML;
7. parse HTML;
8. confirm included record appears;
9. confirm unreviewed record is absent;
10. verify counts;
11. verify no external runtime;
12. delete temporary artifacts.

## Negative gate

Confirm rejection or withholding for:

- invalid topic-key characters;
- topic path traversal;
- missing keyword/content configuration;
- missing required workbook field;
- empty workbook;
- same input/output tagging path;
- existing tagged output;
- no confirmed record;
- included record without reviewer;
- invalid review date;
- duplicate included publication;
- unknown category ID;
- invalid report dates;
- start date after end date;
- existing report output;
- unsafe URL;
- raw HTML characters.

## HTML presentation gate

Inspect at desktop, narrow width, and print preview.

Confirm:

- clear title and evidence period;
- readable metadata cards;
- explicit scope/method section;
- derived metrics;
- organization table boundary;
- category sections and empty states;
- patent cards and figures;
- evidence register;
- no horizontal clipping outside intended table scrolling;
- accessible contrast;
- meaningful alt text;
- no color-only state;
- no dark neon or decorative gradient;
- no remote hero image;
- no hover-only essential navigation.

## Documentation gate

Verify:

- all Markdown is English;
- commands match current script interfaces;
- version is consistent;
- requirements match imports;
- missing README discrepancy is explicit;
- source-example claims are marked unverified;
- exact topology is documented without adding files;
- BIPV and coffee-machine configurations are explained;
- current date and source hashes are recorded in localization index;
- residual risks are not hidden.

## License gate

The source provides an MIT license. Confirm:

- `LICENSE` is unchanged unless legal review authorizes change;
- copyright notice remains;
- license travels with every archive;
- third-party data and images are not assumed covered by the code license;
- exported patent data licenses are reviewed separately.

## Version gate

Localized version: `v1.1.0-localized`.

Confirm it appears consistently in:

- installation note;
- changelog;
- installer output;
- HTML title/meta/footer;
- distribution archive name;
- localization index.

The source file names that contain `v1.1.0` are retained by exact topology.

## Final package checklist

- [ ] Exact 17/17 topology matches frozen source.
- [ ] Every source file was fully read.
- [ ] Every target content file is English/global.
- [ ] Every target file meets or exceeds source line coverage.
- [ ] No README or other source-absent file exists.
- [ ] Python AST checks pass.
- [ ] Shell syntax checks pass.
- [ ] Both topic configurations load.
- [ ] End-to-end BIPV test passes.
- [ ] Coffee-machine key resolves and config agreement passes.
- [ ] Negative tests pass.
- [ ] HTML parses.
- [ ] Links and images are bounded.
- [ ] No network request occurs.
- [ ] No external runtime or gradient exists.
- [ ] No unsafe DOM construction exists.
- [ ] No CJK content remains.
- [ ] No domestic domain remains.
- [ ] No local absolute path remains.
- [ ] No credential or secret remains.
- [ ] No cache or temporary file remains.
- [ ] MCP names and links are verified.
- [ ] Patent/legal boundaries are present.
- [ ] Manual visual review is completed or recorded as pending.
- [ ] Package audit reports zero issues.
- [ ] Localization index row and detailed record are updated.
- [ ] Release decision is `Ready for review`, not automatically released.

## Release record

Record:

- package name and version;
- frozen source path;
- Chinese source marketplace URL;
- source hashes;
- file-by-file localization scope;
- tests and audit commands;
- reviewer and date;
- unresolved risks;
- release status;
- verified MCP mappings.

## Residual risks to disclose

- multilingual search recall;
- database/publication lag;
- legal-status lag;
- family and entity normalization;
- claim interpretation;
- source licensing;
- workbook feature compatibility;
- image reproduction rights;
- configuration quality;
- reviewer judgment;
- downstream browser and print behavior;
- future connector-schema changes.

## Distribution decision

Use one of:

- `Ready for review` — migration and automated checks complete;
- `Approved for controlled distribution` — authorized reviewer approved audience;
- `Withheld` — a blocking evidence, legal, security, or quality issue remains;
- `Superseded` — a later approved package replaces this version.

Automated checks alone do not authorize release.
