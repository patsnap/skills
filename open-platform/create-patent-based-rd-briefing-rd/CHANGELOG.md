# Changelog

This file records the source history and the English/global localization. The
package uses semantic versioning, with `-localized` identifying the migration.

## [1.1.0-localized] — 2026-08-08

### Source-faithful migration

- Preserved all 17 frozen-source files and their relative paths.
- Translated and localized the skill, installation note, changelog,
  distribution guide, implementation notes, example-data guide, shell scripts,
  Python scripts, and four topic configurations.
- Preserved the BIPV and coffee-machine worked domains.
- Preserved separate keyword and content configurations.
- Preserved workbook tagging followed by static HTML generation.
- Preserved approved workbook hyperlinks and embedded-image support.
- Did not add the README files mentioned but absent from the frozen source.

### Global workbook contract

- Replaced domestic-only headers with canonical English/global fields and
  explicit configurable aliases.
- Added publication number, title, applicant, dates, legal status, technical
  problem/solution/effect, abstract, claims, family ID, and source URL fields.
- Added auditable discovery-disposition, matched-term, reviewer, and review-date
  fields.
- Removed reliance on fixed Excel column positions.
- Added duplicate included-publication rejection.
- Added explicit publication-versus-family count handling.

### Relevance review

- Replaced automatic “high relevance” labels with candidate discovery signals.
- Retained inclusive and exclusion terms as transparent provenance.
- Added conflict state when both inclusive and exclusion terms match.
- Required named human review before a record can enter the briefing.
- Added reviewed category IDs and taxonomy validation.
- Removed target relevance-rate guidance.
- Removed fixed Top-20 classification as an analytical rule.

### Patent and legal boundaries

- Added claim-relevance and patent-professional review requirements.
- Prohibited automated novelty, infringement, FTO, validity, enforceability, and
  legal-status conclusions.
- Added status as-of and family/entity normalization limitations.
- Bounded zero-category language to the reviewed workbook.
- Added explicit not-legal-advice language in the HTML and operating guide.

### Verified MCP mapping

- Mapped optional patent retrieval to `advanced_patent_search`:
  https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Mapped supported patent synthesis to `patent_briefing`:
  https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Removed unsupported domestic connector names and schemas.
- Made the workbook workflow independent of connector availability.

### Secure static report

- Rebuilt the generator around escaped text and allowlisted HTTP(S) URLs.
- Removed remote hero-image download and all other network access.
- Removed gradients, dark neon styling, external scripts, external stylesheets,
  remote fonts, analytics, and tracking.
- Added a light scientific editorial visual system.
- Added responsive and print styles.
- Added bounded embedded-image size and count.
- Added atomic HTML writes and overwrite refusal.
- Added source/evidence register and machine-readable metadata.

### Installation and execution

- Replaced a product-specific default installation path with explicit `--target`.
- Replaced deletion/overwrite with a confirmed timestamped backup.
- Made dependency installation opt-in.
- Removed automatic package installation from the report workflow.
- Added ISO date validation and ASCII topic-key validation.
- Added interactive review pause between tagging and report generation.
- Added a noninteractive flag only for already-reviewed controlled automation.

### Source-example facts

- Preserved source organization and publication lists as discovery leads.
- Withheld unverified future-dated news, market percentages, leadership claims,
  category totals, and technical summaries from automatic publication.
- Added required actions for verifying every current-awareness lead.
- Replaced home-market-versus-overseas framing with neutral global geography.

### Validation

- Python AST parsing without bytecode.
- Shell syntax validation.
- End-to-end workbook tagging and HTML rendering.
- Included/unreviewed record boundary test.
- HTML parsing and static-runtime checks.
- Planned package topology, localization, security, and line-parity audit before
  review release.

## [1.1.0-source] — 2026-06-06

This section records the frozen source release without treating its claims as
current evidence.

### Added in the source

- Decorative hero-image download and Base64 embedding.
- Click-through news links.
- Keyword-count-based per-category Top-20 selection.
- Coffee-machine topic examples with six categories.
- Installation, requirements, license, ignore rules, distribution guide,
  implementation notes, sample-data guide, and changelog.

### Fixed in the source

- Workbook hyperlinks lost by DataFrame export.
- Embedded figures lost by DataFrame export.
- Sparse category display caused by short configured patent lists.

### Source limitations addressed by localization

- Remote runtime download.
- Unsafe raw HTML interpolation.
- Domestic field names, sites, examples, and installation paths.
- Fixed column assumptions.
- Keyword match interpreted as confirmed relevance.
- Hard-coded category dictionary in the renderer.
- Arbitrary Top-20 display rule.
- Unverified fixed facts and future dates.
- No explicit human review state.
- No family/count-unit boundary.
- No patent-professional boundary.

## [1.0.0-source] — 2026-05-28

- Initial patent keyword-tagging script.
- Initial HTML briefing generator.
- Initial BIPV configuration.
- Industry-current-awareness, organization, category, and patent-detail modules.
- Responsive card layout and fixed navigation.
- Inline CSS and workbook processing with pandas.

## Versioning policy

- Major: incompatible input, output, or review-contract change.
- Minor: backward-compatible capability or topic addition.
- Patch: backward-compatible correction.
- Localized suffix: source-faithful English/global migration with documented
  evidence, legal, security, and presentation changes.

## Forward work

Potential future work requires separate scope and approval:

- tests checked into a versioned test topology;
- additional reviewed topic configurations;
- accessible static charts backed by data tables;
- PDF export with visual verification;
- explicit multilingual search/review support;
- structured evidence-register import;
- current legal-status refresh integration;
- approved connector-assisted workbook construction.

Do not add source-absent files or functionality merely because it appeared in a
source roadmap.
