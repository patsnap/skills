# HTML competitive technology insight report specification

This specification governs the self-contained HTML artifact produced from a validated, screened, and tagged patent dataset. It preserves the source specification's report components and chart intents while localizing the visual system for a mainstream Western scientific and executive audience.

## 1. Design principles

- Evidence first.
- Semantic HTML.
- English interface and `lang="en"`.
- White paper, charcoal text, restrained scientific blue.
- No gradient.
- No dark sci-fi theme.
- No particle canvas.
- No marquee or ticker.
- No decorative animation.
- No emoji or icon-only status.
- No external fonts.
- No CDN or network dependency.
- No ECharts requirement.
- No hover-only information.
- No color-only meaning.
- Complete without JavaScript.
- Responsive on narrow screens.
- Print-safe on A4 and US Letter.
- Source, unit, denominator, coverage, and cutoff visible.

The report is a decision-support artifact, not a marketing landing page.

## 2. Artifact contract

The output must be one HTML file containing:

- UTF-8 content;
- inline CSS;
- inline accessible SVG only when charts are needed;
- no external script, stylesheet, image, or font dependency;
- no real API key, private URL, or confidential data not approved for delivery;
- an evidence/source register;
- a visible limitations statement; and
- the current generated date and evidence cutoff as separate fields.

The artifact must not:

- open a browser;
- start a server;
- fetch data at runtime;
- write another file;
- contact analytics;
- embed third-party tracking;
- depend on JavaScript for substantive content; or
- hide an unavailable dimension by rendering zero.

## 3. Page architecture

Use this order, omitting unsupported optional sections:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>[Report title]</title>
  <style>[self-contained CSS]</style>
</head>
<body>
  <a class="skip-link" href="#main">Skip to report content</a>
  <header class="report-header">...</header>
  <nav class="toc" aria-label="Report sections">...</nav>
  <main id="main">
    <section id="summary">...</section>
    <section id="methods">...</section>
    <section id="overview">...</section>
    <section id="tech-type">...</section>
    <section id="function">...</section>
    <section id="matrix">...</section>
    <section id="method-route">...</section>
    <section id="profiles">...</section>
    <section id="opportunity">...</section>
    <section id="future">...</section>
    <section id="action">...</section>
    <section id="sources">...</section>
  </main>
  <footer>...</footer>
</body>
</html>
```

Do not include an unsupported section in navigation.

## 4. CSS token system

Use variables rather than repeated hard-coded values:

```css
:root {
  --ink: #17212b;
  --muted: #526273;
  --line: #cbd5df;
  --line-strong: #8797a8;
  --paper: #ffffff;
  --wash: #f3f6f8;
  --accent: #155b8a;
  --accent-dark: #0d4267;
  --accent-soft: #e8f1f7;
  --positive: #21633b;
  --positive-bg: #edf7f1;
  --caution: #7a4e00;
  --caution-bg: #fff7df;
  --risk: #8b2c2c;
  --risk-bg: #fff0f0;
  --radius: 4px;
  --measure: 86rem;
}
```

Rules:

- blue is the primary analytical accent;
- green/caution/red require text labels;
- background and text must meet WCAG AA contrast;
- avoid large areas of saturated color;
- do not use transparency to make text unreadable;
- do not use glow, neon, glassmorphism, or gradient text.

## 5. Typography

Use platform fonts:

```css
body {
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont,
    "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 16px;
  line-height: 1.55;
  color: var(--ink);
}

h1, h2 {
  font-family: Georgia, "Times New Roman", serif;
  font-weight: 600;
}
```

Typography requirements:

- sentence-case headings;
- no all-caps paragraphs;
- short uppercase kicker permitted;
- body line length near 65–80 characters;
- tabular numerals for counts;
- explicit unit adjacent to values;
- link underline visible without hover.

## 6. Accessibility baseline

Required:

- skip link;
- one `<h1>`;
- hierarchical headings;
- landmark elements;
- table captions;
- `scope="col"` and `scope="row"` where appropriate;
- visible keyboard focus;
- meaningful link labels;
- no unsafe link scheme;
- SVG `<title>` and `<desc>`;
- chart values duplicated in a table or list;
- status represented by text plus optional color;
- reduced-motion compliance;
- no automatically moving content.

Focus style:

```css
a:focus-visible,
button:focus-visible,
summary:focus-visible {
  outline: 3px solid #f2b84b;
  outline-offset: 3px;
}
```

## 7. Report header

The header must contain:

- report type kicker;
- title;
- subtitle or target decision;
- intended audience;
- dataset scope;
- counting unit;
- evidence cutoff;
- generated date;
- tag dictionary/version; and
- draft/review/release status.

Example:

```html
<header class="report-header">
  <div class="report-kicker">Patent competitive technology insight</div>
  <h1>[Domain] competition, technology routes, and strategic opportunities</h1>
  <p class="report-subtitle">Decision context...</p>
  <dl class="report-meta">
    <div><dt>Data scope</dt><dd>...</dd></div>
    <div><dt>Counting unit</dt><dd>Simple family</dd></div>
    <div><dt>Evidence cutoff</dt><dd>YYYY-MM-DD</dd></div>
    <div><dt>Tag dictionary</dt><dd>Version...</dd></div>
  </dl>
</header>
```

Do not use KPI cards to display a value that is missing or non-comparable.

## 8. Table of contents

Use a compact sticky horizontal table of contents when screen width permits.

```css
.toc {
  position: sticky;
  top: 0;
  z-index: 20;
  border-bottom: 1px solid var(--line);
  background: rgba(255,255,255,.97);
}

.toc ul {
  max-width: var(--measure);
  margin: 0 auto;
  padding: .65rem 1.25rem;
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  list-style: none;
}
```

Rules:

- English section names;
- meaningful anchors;
- unsupported sections omitted;
- no Chinese ordinal requirement;
- no fixed full-height sidebar;
- hidden in print.

## 9. Section structure

Each substantive section uses:

```html
<section id="[section-id]">
  <header class="section-header">
    <div class="section-kicker">[Analytical lens]</div>
    <h2>[Section title]</h2>
    <p>[Purpose, denominator, and boundary]</p>
  </header>
  <div class="data-boundary">[Coverage or missingness note]</div>
  [findings, tables, figures]
</section>
```

Each section must expose:

- data finding;
- strategic interpretation;
- implication for target company;
- evidence strength;
- limitation;
- source/table/figure reference.

No fade-in observer or animation is required.

## 10. Executive finding component

```html
<article class="finding finding-moderate">
  <div class="finding-index">01</div>
  <div>
    <h3>[Finding]</h3>
    <p>[Interpretation]</p>
    <dl>
      <div><dt>Data basis</dt><dd>Table T-01...</dd></div>
      <div><dt>Evidence strength</dt><dd>Moderate</dd></div>
      <div><dt>Limitation</dt><dd>...</dd></div>
    </dl>
  </div>
</article>
```

Evidence labels:

- Strong;
- Moderate;
- Limited;
- Insufficient.

Do not use cyan/gold/orange card variants as semantic grades.

## 11. Data boundary component

```html
<aside class="data-boundary" aria-label="Data boundary">
  <strong>Data boundary.</strong>
  Method/process tags cover 41% of retained simple families; route findings are Limited.
</aside>
```

Use when:

- coverage is incomplete;
- partial years exist;
- a counting-unit change affects totals;
- entity normalization is incomplete;
- a chart is based on a selected subset;
- status/citation data has an as-of limitation; or
- domain mapping is used.

Do not proceed with a misleading zero-filled chart.

## 12. Metric component

```html
<div class="metric">
  <div class="metric-label">Retained portfolio</div>
  <div class="metric-value">1,234</div>
  <div class="metric-unit">simple families</div>
  <div class="metric-note">Screened through YYYY-MM-DD</div>
</div>
```

Every metric requires:

- value;
- unit/counting level;
- denominator when a percentage;
- source or calculation ID;
- cutoff; and
- missing/not-comparable state.

## 13. Competitor profile component

```html
<article class="profile">
  <header>
    <h3>[Canonical company/legal-entity scope]</h3>
    <span class="profile-label">Broad-coverage portfolio</span>
  </header>
  <dl class="profile-fields">
    <div><dt>Portfolio</dt><dd>...</dd></div>
    <div><dt>Core types</dt><dd>...</dd></div>
    <div><dt>Core functions</dt><dd>...</dd></div>
    <div><dt>Methods</dt><dd>...</dd></div>
    <div><dt>Leading combinations</dt><dd>...</dd></div>
    <div><dt>Concentration</dt><dd>...</dd></div>
    <div><dt>Time signal</dt><dd>...</dd></div>
    <div><dt>Evidence strength</dt><dd>...</dd></div>
  </dl>
  <p class="interpretation">...</p>
  <p class="limitation">...</p>
</article>
```

Do not use a company initial avatar as a substitute for identity resolution.

## 14. Insight component

Use neutral callouts:

```css
.interpretation {
  border-left: 4px solid var(--accent);
  background: var(--accent-soft);
  padding: .8rem 1rem;
}

.limitation {
  border-left: 4px solid var(--caution);
  background: var(--caution-bg);
  padding: .8rem 1rem;
}
```

The label “Interpretation” or “Limitation” must appear in text.

## 15. Chart contract

Every chart must provide:

- figure number;
- title;
- analytical question;
- population/sample;
- counting unit;
- date field/range;
- axis labels and units;
- legend in text;
- source/calculation note;
- coverage/limitation note;
- accessible SVG title/description; and
- equivalent table/list.

Use native SVG, CSS bars, or an HTML table. Prefer a table when the chart does not materially improve comprehension.

Chart colors must be stable and distinguishable in grayscale through labels, line styles, symbols, or patterns.

## 16. Chart 1 — legal/status distribution

Source intent retained: distribution of active/granted, pending/application, and lapsed/expired/invalid categories.

Localization rules:

- use the exact source status taxonomy;
- do not collapse jurisdictions with incompatible status semantics without a mapping table;
- show status as-of date;
- show counts and percentages;
- define denominator;
- use a bar/table instead of a donut when labels are clearer;
- do not call active status “valid and enforceable.”

Suggested table:

| Normalized status | Raw statuses included | Count | Share | Counting unit | As of |
|---|---|---:|---:|---|---|

## 17. Chart 2 — comparative capability profile

Source intent retained: multi-company comparison across up to six supported dimensions.

Possible dimensions:

- portfolio scale;
- technology-type breadth;
- function breadth;
- method diversity;
- recent activity; and
- active/granted share.

Rules:

- include only supported dimensions;
- define each normalization formula;
- do not fill absent dimensions with zero;
- do not use a radar chart when scales/coverage are not comparable;
- provide normalized-value table and raw-value table;
- cap company count for readability but disclose selection.

## 18. Chart 3 — company × technology-type heatmap

Source intent retained: heatmap of tagged density.

Rules:

- derive categories from the actual tag dictionary;
- select top categories by a declared rule;
- show raw counts in every cell;
- provide a table equivalent;
- disclose family/document and multi-label rules;
- distinguish missing/unavailable from zero;
- show tag coverage; and
- avoid hard-coded dairy companies or categories.

Table:

| Company | Type A | Type B | Type C | Untagged | Total/unit |
|---|---:|---:|---:|---:|---:|

## 19. Chart 4 — function distribution

Source intent retained: stacked horizontal comparison by function.

Rules:

- actual function tags only;
- top category selection disclosed;
- company series use stable labels;
- axis starts at zero for counts;
- totals visible;
- percentage version requires consistent denominators;
- multi-label totals may exceed portfolio count and must be noted;
- provide accessible table.

## 20. Chart 5 — type × function matrix

Source intent retained: matrix/bubble view of type-function combinations.

Rules:

- X axis: actual technology types;
- Y axis: actual functions;
- size: declared count/unit;
- label: exact count;
- tooltip cannot be the only detail;
- table must include main companies and evidence strength;
- missing is not zero;
- bubble area scaling must be mathematically correct;
- use minimum/maximum sizes only with a visible legend;
- do not imply sparse cells are opportunities.

Table:

| Technology type | Function | Count | Main companies | Trend | Crowding | Evidence strength | Limitation |
|---|---|---:|---|---|---|---|---|

## 21. Chart 6 — method/process route comparison

Source intent retained: company route diversity/profile.

Rules:

- optional only when method tags pass the field gate;
- actual tag categories only;
- no zero for unavailable tags;
- disclose tag coverage by company;
- radar permitted only with comparable complete dimensions;
- otherwise use grouped bars/table;
- do not claim manufacturing capability.

## 22. Chart 7 — method/process stacked bars

Source intent retained: route composition by company.

Rules:

- company on X or rows;
- one series/column per route;
- raw and percentage views must not be mixed;
- total and denominator visible;
- “Other/unknown” visible;
- provide table and coverage note.

## 23. Chart 8 — competitor strategic profile

Source intent retained: eight-dimension normalized comparison.

Potential dimensions:

- portfolio scale;
- type breadth;
- function coverage;
- method coverage;
- recent growth;
- active/granted share;
- combination concentration; and
- differentiation.

Rules:

- include only dimensions with formulas and adequate coverage;
- disclose normalization and direction;
- compare raw values;
- do not call normalized score “capability” without qualification;
- no missing-as-zero;
- no opaque composite total;
- provide sensitivity or omit unstable dimensions.

## 24. Additional trend chart

When time fields pass:

- show annual/quarterly counts;
- declare date field;
- mark partial periods;
- disclose publication lag;
- use zero baseline for count lines/bars;
- identify small denominators;
- do not forecast without a stated method;
- include source table.

## 25. Tables

Base style:

```css
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: .9rem; }
caption { text-align: left; color: var(--muted); font-weight: 700; padding: 0 0 .6rem; }
th, td { border-bottom: 1px solid var(--line); padding: .65rem .7rem; text-align: left; vertical-align: top; }
thead th { background: var(--wash); }
.numeric { text-align: right; font-variant-numeric: tabular-nums; }
```

Requirements:

- caption;
- units in headers;
- counting level in caption/note;
- sort rule stated;
- “Not available” distinct from `0`;
- source and cutoff note;
- row/column headers;
- no meaning conveyed only on hover;
- repeat headers in print where supported.

## 26. Recommendation table

Required fields:

| Recommendation class | Direction | Type | Function/method | Competitor evidence | Opportunity/risk | Action | Priority | Strength | Evidence IDs | Validate next |
|---|---|---|---|---|---|---|---|---|---|---|

Class labels:

- A — Data-supported;
- B — Domain-mapping-inspired;
- C — Additional data required.

Priority labels must be words, not red/yellow/blue alone.

## 27. Source register

Use:

| Source ID | Type | Title/artifact | Publisher/owner | Date | Retrieved | Locator | Supports | Quality | Limitation |
|---|---|---|---|---|---|---|---|---|---|

Include:

- search manifest;
- screening artifact;
- tagging manifest/dictionary;
- patent connectors and retrieval operations;
- representative patent records;
- domain-mapping sources; and
- calculations/figures where needed.

Do not expose secret query URLs or keys.

## 28. Footer

Footer contains:

- report title/short label;
- evidence cutoff;
- generated date;
- dataset/counting unit;
- version/status;
- disclaimer.

Example:

```html
<footer>
  <p><strong>[Short report title]</strong></p>
  <p>Evidence cutoff: YYYY-MM-DD · Generated: YYYY-MM-DD · Counting unit: simple family</p>
  <p>This report is based on the declared patent dataset and tag outputs. Findings require review against claims, current legal status, technical evidence, and relevant market/domain sources. It is not legal or investment advice.</p>
</footer>
```

Never hard-code 2026 or any other year.

## 29. Responsive behavior

```css
@media (max-width: 56rem) {
  .two-column,
  .three-column,
  .profile-grid { grid-template-columns: 1fr; }
  .report-header { padding-top: 2rem; }
}

@media (max-width: 38rem) {
  body { font-size: 15px; }
  main { padding-left: 1rem; padding-right: 1rem; }
}
```

Rules:

- no horizontal page overflow;
- tables scroll within `.table-wrap` on screen;
- navigation can scroll horizontally;
- charts resize through viewBox, not JavaScript;
- text remains readable at 200% zoom.

## 30. Reduced motion

No substantive animation is allowed.

```css
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  * { animation-duration: .01ms !important; transition-duration: .01ms !important; }
}
```

Do not include particle movement, ticker loops, pulsing labels, or scroll-entry animation.

## 31. Print behavior

```css
@media print {
  :root {
    --ink: #000;
    --muted: #333;
    --line: #999;
    --paper: #fff;
    --wash: #f3f3f3;
  }
  @page { size: auto; margin: 14mm; }
  body { font-size: 9.5pt; }
  .skip-link, .toc { display: none; }
  .report-header, main, footer { max-width: none; padding-left: 0; padding-right: 0; }
  section { break-before: auto; }
  article, figure, table { break-inside: avoid; }
  a { color: #000; text-decoration: underline; }
  a[href^="http"]::after { content: " (" attr(href) ")"; font-size: 7.5pt; overflow-wrap: anywhere; }
}
```

Print requirements:

- all substantive sections visible;
- chart data tables visible;
- sources visible;
- dark backgrounds removed;
- colors distinguishable in grayscale;
- URLs shown when useful;
- no fixed navigation overlay.

## 32. Security and escaping

- Escape all untrusted text.
- Allow only `http` and `https` links.
- Add `rel="noopener noreferrer"` to new-window links.
- Do not inject raw patent abstracts, tags, company names, or source titles as HTML.
- Do not evaluate input as JavaScript.
- Do not insert spreadsheet formulas into HTML as executable content.
- Do not expose API keys or credentials.
- Do not include local absolute paths unless the user explicitly wants a local delivery link.

## 33. Data-content rules

All content must come from actual validated input:

1. KPI counts reconcile with source records.
2. Company counts use the declared entity aggregation.
3. Type heatmap uses actual formal tags.
4. Function analysis uses actual formal tags.
5. Matrix uses actual cross-tabulation.
6. Legal/status chart uses actual status fields and as-of date.
7. Method/process charts require adequate coverage.
8. Competitor profiles map to calculations and evidence.
9. Recommendations map to findings and evidence class.
10. Domain mapping is labeled and sourced.
11. Missing fields render as unavailable or omit the chart.
12. Placeholder/example values never appear in a final report.

## 34. Figure quality assurance

For every figure verify:

- correct population;
- correct counting unit;
- correct category order;
- correct company/entity labels;
- correct total;
- correct multi-label handling;
- correct missing/zero distinction;
- explicit source/cutoff;
- correct axis baseline;
- readable labels;
- accessible text equivalent;
- print legibility;
- no unsupported interpretation in title.

## 35. Chapter quality assurance

For every chapter verify:

- section passed field gate;
- coverage shown;
- finding/calculation reconcile;
- interpretation is bounded;
- implication is decision-relevant;
- evidence strength follows criteria;
- alternative explanation included;
- external mapping labeled;
- no legal, market, product, efficacy, manufacturing, or FTO overclaim.

## 36. Final artifact acceptance gate

The HTML is ready only when:

- title and dates are current;
- navigation matches rendered sections;
- all values reconcile;
- unavailable dimensions are not zero-filled;
- every chart has a table/text equivalent;
- evidence strengths are textual;
- source register is complete;
- links are safe;
- no placeholder remains;
- no CJK interface prose remains unless requested;
- no Zhihuiya regional domain remains;
- no absolute developer path remains;
- no external CDN or network call remains;
- no gradient, particle, ticker, emoji, or decorative animation remains;
- responsive and print rules are present;
- disclaimers and limitations are visible; and
- output location is user-approved.

## 37. Source chart-intent crosswalk

| Source chart/component intent | Localized implementation |
|---|---|
| Legal-status donut | Accessible status bar/table with raw-status mapping |
| Six-dimension radar | Normalized comparison table; optional SVG only with complete comparable data |
| Protein-type heatmap | Domain-neutral company × technology-type matrix |
| Function stacked bars | Function distribution table plus optional CSS/SVG bars |
| Protein × function bubble chart | Domain-neutral type × function matrix plus table |
| Separation-route radar | Optional method/process comparison with coverage gate |
| Separation-route stacked bars | Optional company × method composition table/chart |
| Eight-dimension company radar | Transparent raw/normalized profile comparison without opaque total |
| Executive colored cards | Neutral finding cards with textual evidence strength |
| Competitor avatar cards | Legal-entity-scoped profile cards |
| Dark sci-fi hero | Scientific report header |
| Particle canvas | Removed; no analytical value |
| Scrolling ticker | Removed; metrics shown statically with units |
| ECharts CDN | Removed; self-contained HTML/SVG/table |
| Fixed 2026 footer | Dynamic generated date and evidence cutoff |
| Missing dimensions filled with 0 | Omitted or explicitly unavailable |

## 38. Dairy-protein localization example

When the dataset genuinely uses the source dairy fields:

- `protein_type` may populate the technology-type axis;
- `protein_function` may populate the function axis;
- `separation_method` may populate the optional method/process axis;
- Appendix A of `white-paper-framework.md` may support clearly labeled domain mapping;
- health, efficacy, population, product and regulatory interpretations require separate evidence.

Do not hard-code dairy categories, companies, chart dimensions, or Chinese field labels into a report for another domain.

## 39. Minimal static chart example

```html
<figure aria-labelledby="fig-1-title">
  <figcaption id="fig-1-title">
    Figure 1. Retained simple families by technology type
  </figcaption>
  <svg viewBox="0 0 720 260" role="img" aria-labelledby="fig-1-svg-title fig-1-svg-desc">
    <title id="fig-1-svg-title">Retained simple families by technology type</title>
    <desc id="fig-1-svg-desc">Type A has 42 families; Type B has 31; Type C has 18.</desc>
    <!-- Escaped, validated static bars and text. -->
  </svg>
  <div class="table-wrap">
    <table>
      <caption>Figure 1 data</caption>
      <thead><tr><th>Technology type</th><th class="numeric">Simple families</th></tr></thead>
      <tbody>...</tbody>
    </table>
  </div>
  <p class="source-note">Source: tagged dataset vX; evidence cutoff YYYY-MM-DD; multi-label counting.</p>
</figure>
```

The table is mandatory even if SVG is present.

## 40. Delivery note

This package contains a specification, not a renderer script. Generate the requested HTML artifact in the user's approved output location. Do not add a renderer to the skill directory without explicit approval because no such source file exists.
