# Quality Check Prompt

## Task

Audit all ten generated report artifacts for topology, data lineage, consistency, accessibility, security, and decision-quality. Do not mark the report complete until every required gate passes or is explicitly recorded as a release-blocking failure.

## Required artifacts

- `index.html`
- `patents.html`
- `evidence.html`
- `subfields.html`
- `methodology.html`
- `intermediate_data.json`
- `patent_list.csv`
- `evidence_mapping.csv`
- `README.md`
- `quality_check.md`

These generated artifacts belong in the report output directory, not in the skill package.

## 1. File and parse checks

- Verify exact filenames and nonzero byte sizes.
- Parse JSON.
- Parse CSV headers and rows using a standards-compliant reader.
- Parse HTML and verify one title, one main heading, and complete closing structure.
- Verify UTF-8.
- Verify all internal navigation targets exist.
- Verify no extra `.py`, scripts directory, cache, temporary, or generated-secret file exists.

## 2. Data lineage

- Confirm every full-scope metric contains query version, connector/tool, date field, period, jurisdiction, count unit, cutoff, and source ID.
- Confirm every period or subfield count has a complete collection-log entry.
- Confirm failed buckets are missing, not zero.
- Confirm partial rankings are labeled partial.
- Confirm representative patent fields never feed population metrics.
- Confirm unavailable applicant, geography, status, or influence aggregations produce no chart or concentration claim.
- Confirm recent-period publication lag is disclosed.

## 3. Sample boundary

- Confirm `patents.html` displays an explicit representative-sample warning.
- Confirm sample selection method, returned count, review count, and limitations are stated.
- Confirm sample applicants, jurisdictions, dates, status, citations, or families are not used as population distributions.
- Confirm fewer than the target record count is acceptable when all valid records are shown and the shortfall is disclosed.

## 4. HTML quality and security

For every HTML page:

- verify `<!doctype html>`, UTF-8, viewport, language, title, headings, landmark structure, and print CSS;
- verify responsive tables and keyboard-visible controls;
- verify text labels accompany color;
- verify charts have accessible tables and descriptions;
- verify no empty chart, empty table, placeholder, `TODO`, remote font, CDN, analytics, or tracker;
- verify no unsafe `innerHTML` with untrusted data;
- verify URLs allow only HTTP(S);
- verify no `javascript:`, `file:`, local path, real API key, session ID, or expiring signed URL;
- verify external text is escaped; and
- test a malicious fixture containing tags, quotes, and an unsafe URL.

## 5. Main-report completeness

- Confirm all 15 source modules exist or an unavailable-state module explains the gap.
- Confirm at least six KPI/evidence cards.
- Confirm trend, regional, subfield, score, opportunity, conclusion, portfolio-strategy, patent-sample, method, and navigation content.
- Confirm conclusion includes recommendation state, opportunities, risks, evidence gaps, and next validation gates.
- Confirm narrative is complete and not padded to a word count.

## 6. Cross-artifact consistency

- KPI values equal `intermediate_data.json` values.
- Chart/table series equal JSON period and subfield arrays.
- All patent IDs in HTML occur in `patent_list.csv` and JSON.
- All claim IDs in HTML occur in `evidence_mapping.csv` and JSON.
- All source IDs resolve in the source register.
- Scoring arithmetic, weights, missing weight, normalized score, and sensitivity reconcile.
- Recommendation state is identical across HTML, JSON, README, and final handoff.
- Scope, query version, cutoff, count unit, and limitations match across artifacts.

## 7. Analytical integrity

- Search strategy is executed and versioned.
- Count semantics are explicit.
- Family and publication counts are not mixed.
- CAGR formula and elapsed periods are correct.
- Applicant concentration uses a valid denominator.
- HHI is absent when the distribution is incomplete.
- Subfield overlap is disclosed and overlapping counts are not summed.
- Patent scarcity is not called white space without sensitivity and non-patent review.
- Filing activity is not called market growth.
- Patent influence is not called product quality.
- International filing is not called commercialization.
- Patent-only evidence does not produce investment advice.

## 8. Generated QA report

Write `quality_check.md` using `references/templates/quality_check_template.md`. Record:

- audit time and reviewer;
- file inventory and byte counts;
- data-lineage gate results;
- sample-boundary results;
- HTML/accessibility/security results;
- cross-artifact reconciliation;
- analytical-integrity results;
- known limitations;
- release blockers; and
- final decision: `Pass`, `Pass with disclosed limitations`, or `Fail — repair required`.

Never emit `Pass` when a required file is missing, JSON/CSV does not parse, claim/source IDs are orphaned, a chart uses sample data, unsafe content is present, or displayed values fail reconciliation.

## Final checklist

- Exactly ten required artifacts are present.
- No forbidden package/runtime artifacts are present.
- All data products parse.
- Every metric is reproducible.
- Every claim is traceable.
- Every chart is valid and accessible.
- Every page is safe and portable.
- Scores and recommendations are transparent and qualified.
- All limitations are visible.
- QA decision matches the evidence.
