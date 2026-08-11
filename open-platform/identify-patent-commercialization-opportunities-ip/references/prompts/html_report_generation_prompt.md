# HTML Report Generation Prompt

## Core rule

Generate five complete, portable, evidence-backed HTML pages from the validated intermediate schema. Never put invented values into a placeholder or empty chart.

## Scientific design system

Use a restrained Western scientific/executive style:

- white or cool-neutral paper surface;
- charcoal body text;
- navy headings and navigation;
- restrained teal accent;
- muted amber/red only for evidence-qualified warnings;
- system sans-serif body and system monospace for patent IDs;
- compact metadata, semantic tables, evidence cards, and clear whitespace;
- text states in addition to color;
- responsive table wrappers and print CSS.

Do not use remote Google Fonts, ECharts CDN, Chart.js, Plotly, trackers, analytics, animated blobs, neon glow, emoji-only icons, or decorative dashboards. Use accessible HTML tables and compact inline SVG/CSS charts only when data is complete and a chart materially aids comprehension.

## Security

- Escape all user-, connector-, and patent-derived text.
- Serialize JSON safely; never interpolate untrusted strings into raw template-literal HTML.
- Build interactive rows with safe text nodes or pre-escaped server-side/template content.
- Allow only stable HTTP(S) links.
- Reject `javascript:`, `data:` for links, `file:`, inline event handlers from data, and untrusted active markup.
- Include no API key, local path, session identifier, hidden prompt, or expiring signed URL.
- Keep all report functionality available without network access.

## Five-page topology

1. `index.html` — executive assessment and full evidence narrative;
2. `patents.html` — representative patent sample with safe search/filter/pagination;
3. `evidence.html` — claim-to-evidence register;
4. `subfields.html` — four to eight subfield assessments;
5. `methodology.html` — search, metrics, scoring, QA, exclusions, and limitations.

All pages must share navigation, topic, cutoff, scope, visual tokens, accessibility conventions, and source terminology.

## Main report modules

Preserve all 15 source modules in this order:

1. report title, scope, recommendation state, evidence confidence, and navigation;
2. at least six KPI/evidence cards, with unavailable states when needed;
3. context, decision question, and background;
4. global or primary-scope period trend, only if complete;
5. decision-relevant regional comparison, only if comparable;
6. subfield activity comparison, with overlap disclosure;
7. six-dimension score/rubric and missing-weight table;
8. detailed trend interpretation;
9. detailed subfield analysis;
10. at least three candidate opportunities or an evidence-gap explanation;
11. R&D/commercialization conclusion with opportunities, risks, and validation gates;
12. IP/portfolio strategy recommendations;
13. ten representative patents or all valid records if fewer;
14. data definitions, search, sample boundary, and disclaimer; and
15. links to all companion pages.

Do not enforce Chinese character counts. Require sufficient English narrative to explain evidence, reasoning, uncertainty, and action. As a practical quality gate, the executive page should normally contain at least 1,800 English words when all modules are available, but completeness and precision control.

## Chart rules

For every chart:

- use only validated full-scope metrics;
- include a title, unit, count basis, period, query version, source IDs, and lag note;
- provide the same data in an accessible table;
- identify missing/partial buckets;
- use a descriptive SVG title and text alternative;
- avoid truncated axes or visual exaggeration; and
- omit the chart when data is unavailable.

Never chart applicant ranking, geography, legal status, grant rate, citations, or another distribution from representative sample frequencies.

## Claim and source display

Place a stable claim tag such as `T001` beside every material statement and a concise source note immediately nearby. Every tag must resolve in `evidence.html`, `evidence_mapping.csv`, and `intermediate_data.json`.

## Patent links

Use a verified stable global PatSnap or official public patent URL. Show publication number, title, applicant, date, jurisdiction, family/status-as-of information, source language, translation provenance, and sample disclaimer as available.

## Unavailable-state component

When a metric is unavailable, render:

- metric name;
- state `Unavailable` or `Partial`;
- missing connector capability or denominator;
- impact on scoring and conclusions; and
- recommended collection step.

Do not render an empty chart container.

## Quality gates

- Five HTML files exist.
- Each begins with `<!doctype html>` and uses UTF-8.
- Navigation resolves across all pages.
- All placeholders are replaced.
- No `TODO` or invented value remains.
- Every chart has complete real data and a table equivalent.
- Every material claim has a valid claim ID.
- All external text is escaped.
- No remote dependency is required.
- Pages work at 390px and desktop widths.
- Print output preserves substantive content.
- Content and values reconcile with JSON/CSV.
