# R&D Direction Evidence Report Structure

This file is the presentation and section-order contract for both Markdown and HTML. The renderer generates every section from the validated payload; do not paste a separate report body into the payload.

## Front matter

The Markdown report starts with:

```markdown
# R&D Direction Evidence Report

> **Project:** {project_name when supplied}
> **Applicant or team:** {applicant_or_team when supplied}
> **Report date:** {report_date}
> **Evidence cutoff:** {evidence_cutoff}
> **Scope:** {scope}
> **Geographies:** {geographies}
> **Languages:** {languages}
> **Patent count unit:** {patent_count_unit}
```

Omit the complete Project or Applicant row when its value is empty. Do not write `Not provided` in an optional metadata row.

## Source requirement

```markdown
## Source Requirement

> {requirement_text}
```

The text is source evidence, not an analyst paraphrase. Preserve approved redaction notices.

## 1. Requirement analysis

| Dimension | Required subfields |
|---|---|
| Demand and operating need | Operating context; stakeholder need; technical consequence; current response |
| Bottleneck | Performance limit; supporting evidence; tradeoffs; mechanistic limit |
| Solution hypothesis | Technical path; system concept; compatibility; target outcome |

Keep the order fixed. For a required field absent from the source, show `Not provided in the source requirement`. Clearly label the solution hypothesis when it is analyst-generated rather than source-stated.

## 2. Technical issue decomposition

| ID | Technical issue | Source locations | Dependencies | Confidence |
|---|---|---|---|---|
| T1 | Name and source-faithful description | Requirement paragraph | Other issue IDs or None | High/medium/low |

After the table, show an issue-to-direction coverage statement. Do not claim issues are mutually exclusive when the source shows dependencies.

## 3. Proposed R&D directions

### 3.1 Evidence summary

Show derived counts:

- standards and engineering cases;
- papers;
- patent records and aggregate count under the declared unit;
- authoritative web sources;
- unique normalized organizations;
- organizations displayed;
- search log entries;
- rejected/unavailable evidence described in limitations.

Counts are derived from the unified evidence registry and must reconcile with A1–A4.

### 3.2 onward — one section per direction

```markdown
### 3.2 D1 — {direction_name}

**Issues addressed:** T1, T2

**Rationale:** ...

**Core research question:** ...

**Technical target:** ...

**Confidence and priority basis:** ...

#### Research tasks

| Task | Research activity | Validation method | Success metric | Evidence | Uncertainty |
|---|---|---|---|---|---|
| D1-R1 | ... | ... | ... | [E1] | ... |

#### Representative evidence

Show a decision-useful subset by evidence type. Selection is explained; it is not mechanically limited to three or five items. The complete registry remains in the appendices.

#### Evidence gap

State what the current search and sources did not establish.

#### Expected deliverables

List specific experimental data, models, prototypes, designs, process windows, standards evidence, validation packages, decision gates, or other artifacts. Do not promise outcomes unsupported by evidence.

### Direction synthesis

| Direction | Issues | Core question | Target | Deliverables | Evidence | Confidence |
|---|---|---|---|---|---|---|

## 4. Research and industry organizations

| Organization | Type | Directions | Evidence-backed focus | Representative outputs | Evidence | Confidence |
|---|---|---|---|---|---|---|

Show the number of unique organizations in the full accepted evidence set and the number displayed. Do not call a selected top group the total. Ordering may use relevance to the user's decision, evidence coverage, or another disclosed method; citation counts alone are not authority or quality.

## 5. Search method and coverage

| Search ID | Direction | Evidence type | Source/tool | Query | Filters | Requested | Returned | Reviewed | Deduplication | Limits |
|---|---|---|---|---|---|---:|---:|---:|---|---|

Show unavailable tools/platforms and coverage gaps. A zero result means no retained relevant record under the documented search, not that no prior work exists.

## 6. Limitations and specialist review

List every payload limitation and the legal boundary. Include:

- incomplete or ambiguous source requirements;
- database and publication lag;
- multilingual and classification recall;
- paywall/full-text/access constraints;
- patent family, entity, legal-status, and citation-count limits;
- standards/version and engineering-case verification;
- analytical hypotheses requiring experimental validation;
- safety, regulatory, legal, commercial, or specialist review as relevant.

## 7. Appendices

### A1. Standards and engineering cases

| Evidence | Type | Year/date | Publisher | Document/project | Context/status | Summary | Directions | Review |
|---|---|---|---|---|---|---|---|---|

### A2. Scientific and technical papers

| Evidence | Year/date | Authors/affiliations | Title | Venue/DOI | Citation count as of source date | Directions | Review |
|---|---|---|---|---|---|---|---|

### A3. Patent evidence

| Evidence | Publication | Title | Applicants/assignees | Priority/publication | Family | Legal status as of | Directions | Review depth |
|---|---|---|---|---|---|---|---|---|

### A4. Authoritative web evidence

| Evidence | Date | Publisher/type | Title | Summary | Directions | Review |
|---|---|---|---|---|---|---|

All evidence uses global `E#` identifiers. If an appendix has no records, show an explicit empty state and preserve the heading.

## Complete source register

List every `E#` once with title, evidence type, source, date, reviewed URL or `Source link not supplied`, review depth, status, and confidence.

## HTML-specific requirements

- Use a restrained scientific/editorial light design.
- Use semantic headings and a generated table of contents.
- Keep the requirement visibly distinct from analysis.
- Provide captions and column headers for tables.
- Make evidence IDs link to source-register anchors.
- External links use `target="_blank" rel="noopener noreferrer"`; missing URLs are not anchors.
- Include a skip link and visible focus styles.
- No gradients, emojis, domestic fonts, external CSS/fonts/scripts, unsafe raw HTML, analytics, or runtime network requests.
- Responsive and print layouts are required.

## Completion checks

The renderer verifies all required sections are present in Markdown and HTML, artifact files are non-empty, count summaries equal appendix rows under the declared units, every reference resolves, no unresolved token remains, and existing outputs are not overwritten without authorization.
