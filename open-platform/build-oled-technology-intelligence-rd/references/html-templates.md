# Portal HTML Structure and Scientific Editorial Design

Use this reference when maintaining the renderer. Generated pages must be self-contained and work without network access.

## Page system

| Page | Required content |
|---|---|
| `index.html` | Scope, coverage, calculated statistics, findings, organizations, routes, events, publications, patent preview, method, search log, limitations |
| `company-{slug}.html` | Entity identity/role, inclusion evidence, routes, dated records, patents, gaps, method link |
| `tech-{slug}.html` | Route definition/criteria, organizations, dated records, patents, maturity evidence, gaps |
| `patents.html` | Patent method, count unit, coverage, filters, records, review depth, limitations |

## Visual language

- White paper surfaces on a light neutral background.
- Navy body text and one blue navigation/accent color.
- Green, amber, and red only for explicitly labeled reviewed states.
- Georgia or Times New Roman for report-scale headings; system sans-serif for interface text.
- Tabular numerals for dates and counts.
- One-pixel borders, restrained eight-pixel radii, and no decorative shadow dependence.
- No gradients, emoji, logos, external fonts, Tailwind, runtime chart libraries, floating animation, glassmorphism, or decorative SVG.
- Show charts only when a table or concise prose cannot communicate the relationship; provide an equivalent data table.

## Shared CSS foundation

```css
:root {
  --ink: #172033;
  --muted: #5a667a;
  --line: #d8dee8;
  --paper: #ffffff;
  --wash: #f5f7fa;
  --accent: #145da0;
  --accent-soft: #eaf2f9;
  --positive: #287a55;
  --warning: #9a6318;
  --critical: #a13d3d;
  --radius: 8px;
  --measure: 1200px;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--wash);
  color: var(--ink);
  font-family: Inter, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 15px;
  line-height: 1.55;
}
a { color: var(--accent); text-underline-offset: 2px; }
a:focus-visible { outline: 3px solid #79aede; outline-offset: 2px; }
.skip-link { position: absolute; left: -9999px; top: 8px; }
.skip-link:focus { left: 8px; z-index: 100; background: white; padding: 8px; }
.masthead { background: var(--paper); border-bottom: 1px solid var(--line); }
.masthead-inner { max-width: var(--measure); margin: 0 auto; padding: 34px 28px 28px; }
.eyebrow { color: var(--accent); font-size: 12px; font-weight: 750; letter-spacing: .08em; text-transform: uppercase; }
h1 { max-width: 920px; margin: 8px 0 12px; font: 600 clamp(32px,5vw,54px)/1.08 Georgia,"Times New Roman",serif; }
h2 { margin: 0 0 6px; font: 600 28px/1.2 Georgia,"Times New Roman",serif; }
h3 { margin: 18px 0 7px; font-size: 16px; }
.deck { max-width: 900px; color: var(--muted); font-size: 17px; }
.meta-grid { display: grid; grid-template-columns: repeat(4,minmax(150px,1fr)); gap: 1px; margin-top: 24px; border: 1px solid var(--line); background: var(--line); }
.meta { min-height: 76px; padding: 12px 14px; background: var(--paper); }
.meta-label { color: var(--muted); font-size: 10px; font-weight: 750; letter-spacing: .05em; text-transform: uppercase; }
.meta-value { margin-top: 5px; font-weight: 650; }
.topnav { position: sticky; top: 0; z-index: 20; border-bottom: 1px solid var(--line); background: rgba(255,255,255,.97); }
.topnav-inner { display: flex; gap: 6px; max-width: var(--measure); margin: 0 auto; padding: 8px 28px; overflow-x: auto; }
.topnav a { padding: 7px 10px; color: var(--muted); font-size: 13px; text-decoration: none; white-space: nowrap; }
.topnav a:hover, .topnav a:focus { color: var(--accent); background: var(--accent-soft); }
main { max-width: var(--measure); margin: 22px auto 60px; padding: 0 28px; }
section { margin-bottom: 22px; padding: 24px; border: 1px solid var(--line); border-radius: var(--radius); background: var(--paper); }
.section-deck { margin: 0 0 18px; color: var(--muted); }
.stats { display: grid; grid-template-columns: repeat(6,minmax(0,1fr)); gap: 1px; border: 1px solid var(--line); background: var(--line); }
.stat { padding: 14px; background: var(--paper); }
.stat-value { font: 600 26px Georgia,serif; font-variant-numeric: tabular-nums; }
.stat-label { color: var(--muted); font-size: 11px; }
.grid { display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: 12px; }
.card { display: block; border: 1px solid var(--line); border-top: 3px solid var(--accent); padding: 15px; color: inherit; text-decoration: none; }
.card:hover { border-color: #9ebbd4; background: #fbfdff; }
.card-title { font-weight: 700; }
.card-meta { margin-top: 5px; color: var(--muted); font-size: 12px; }
.tag { display: inline-block; border: 1px solid var(--line); border-radius: 999px; padding: 2px 8px; font-size: 11px; font-weight: 700; }
.tag.checked { color: var(--positive); background: #eff8f3; }
.tag.gap { color: var(--critical); background: #fff3f3; }
.tag.inference { color: var(--warning); background: #fff9ef; }
.finding { display: grid; grid-template-columns: 42px minmax(0,1fr); gap: 12px; padding: 13px 0; border-bottom: 1px solid var(--line); }
.finding-index { color: var(--accent); font: 24px Georgia,serif; }
.timeline { border-left: 2px solid var(--line); margin-left: 6px; padding-left: 18px; }
.event { position: relative; padding: 0 0 18px; }
.event::before { content: ""; position: absolute; left: -24px; top: 6px; width: 8px; height: 8px; border: 2px solid var(--accent); border-radius: 50%; background: white; }
.event-date { color: var(--muted); font-size: 11px; font-variant-numeric: tabular-nums; }
.event-title { font-weight: 700; }
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: 13px; font-variant-numeric: tabular-nums; }
caption { padding-bottom: 8px; color: var(--muted); text-align: left; }
th, td { padding: 10px 9px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
th { background: var(--wash); color: var(--muted); font-size: 10px; letter-spacing: .04em; text-transform: uppercase; }
.notice { border-left: 4px solid var(--warning); padding: 11px 14px; background: #fff9ef; color: #6c481a; }
.empty { color: var(--muted); font-style: italic; }
.source-list { padding-left: 20px; }
.source-list li { margin: 5px 0; }
.detail-header { display: flex; justify-content: space-between; gap: 18px; align-items: flex-start; }
.back-link { display: inline-block; margin-bottom: 16px; }
.two-col { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 12px; }
.panel { border: 1px solid var(--line); padding: 14px; }
footer { border-top: 1px solid var(--line); padding: 24px 28px; color: var(--muted); font-size: 12px; }
@media (max-width: 900px) { .stats { grid-template-columns: repeat(3,1fr); } .grid { grid-template-columns: repeat(2,1fr); } .meta-grid { grid-template-columns: repeat(2,1fr); } }
@media (max-width: 620px) { .stats,.grid,.meta-grid,.two-col { grid-template-columns: 1fr; } main,.masthead-inner { padding-left: 15px; padding-right: 15px; } section { padding: 17px; } }
@media print { body { background: white; font-size: 10pt; } .topnav,.skip-link,.no-print { display: none; } main { max-width: none; margin: 0; padding: 0; } section,.card { break-inside: avoid; } a { color: inherit; text-decoration: none; } }
```

## Shared page shell

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escaped_title}</title>
  <style>{shared_css}</style>
</head>
<body>
  <a class="skip-link" href="#main">Skip to main content</a>
  <header class="masthead">
    <div class="masthead-inner">
      <div class="eyebrow">Technology intelligence · reviewed evidence</div>
      <h1>{escaped_title}</h1>
      <p class="deck">{escaped_decision_context}</p>
      <div class="meta-grid" aria-label="Portal metadata">{metadata_cells}</div>
    </div>
  </header>
  <nav class="topnav" aria-label="Portal navigation"><div class="topnav-inner">{navigation}</div></nav>
  <main id="main">{page_sections}</main>
  <footer>{escaped_footer}</footer>
</body>
</html>
```

## Metadata cell

```html
<div class="meta">
  <div class="meta-label">{escaped_label}</div>
  <div class="meta-value">{escaped_value}</div>
</div>
```

## Organization card

```html
<a class="card" href="company-{safe_slug}.html">
  <div class="card-title">{escaped_display_name}</div>
  <div class="card-meta">{escaped_roles}</div>
  <p>{escaped_inclusion_rationale}</p>
  <span class="tag {review_class}">{escaped_review_status}</span>
  <span class="card-meta">Evidence through {escaped_last_evidence_date}</span>
</a>
```

Do not render a company card as a link if its local page was not generated.

## Technology-route card

```html
<a class="card" href="tech-{safe_slug}.html">
  <div class="card-title">{escaped_route_name}</div>
  <p>{escaped_definition}</p>
  <span class="tag {review_class}">{escaped_review_status}</span>
  <span class="card-meta">{accepted_record_count} reviewed records</span>
</a>
```

## Executive finding

```html
<article class="finding">
  <div class="finding-index">{two_digit_index}</div>
  <div>
    <strong>{escaped_finding}</strong>
    <p>{escaped_basis}</p>
    <div class="card-meta">Evidence: {linked_evidence_ids} · Confidence: {escaped_confidence}</div>
  </div>
</article>
```

## Timeline event

```html
<article class="event">
  <div class="event-date">{escaped_event_date}</div>
  <div class="event-title">{escaped_title}</div>
  <p>{escaped_observed_fact}</p>
  <p><span class="tag inference">Analyst inference</span> {escaped_inference}</p>
  <div class="card-meta">Sources: {linked_source_ids} · Confidence: {escaped_confidence}</div>
</article>
```

## Patent evidence row

```html
<tr>
  <td>{publication_link_or_plain_text}</td>
  <td>{escaped_title}</td>
  <td>{escaped_applicants}</td>
  <td>{escaped_priority_date}<br>{escaped_publication_date}</td>
  <td>{escaped_family_unit}</td>
  <td>{escaped_technology_routes}</td>
  <td>{escaped_relevance_note}</td>
  <td>{escaped_review_depth}<br>{escaped_review_status}</td>
</tr>
```

Never use a placeholder anchor. If the URL is absent or rejected, show `Source link not supplied`.

## Methodology and limitations

Every page must show or link to:

- domain scope and exclusions;
- period and evidence cutoff;
- geographies, languages, and source types;
- search-log identifiers;
- organization/taxonomy inclusion rules;
- deduplication and patent count unit;
- accepted and rejected record counts;
- model/analyst inference labeling;
- unavailable sources and known gaps;
- legal/investment/commercial disclaimer.

## Detail-page rules

Company pages use a visible `Back to portal` link with `target="_self"`. Route pages do the same. Do not set a document-wide base target. External links use `target="_blank" rel="noopener noreferrer"`; local links stay in the same browsing context.

## No JavaScript requirement

Core navigation, tables, filters-as-static-metadata, and evidence access must work without JavaScript. Add no prompt-based date editor: changing displayed dates without refreshing evidence is misleading. The evidence period is immutable in a rendered build.

## Rendering security

- Escape text and attributes with a standard-library encoder.
- Validate URLs before creating anchors.
- Validate slugs before joining paths.
- Never pass untrusted content into an HTML-parsing DOM sink.
- Do not embed raw JSON in executable script blocks.
- Do not fetch remote resources at runtime.
- Do not expose local absolute paths in page content.

## Visual QA checklist

Inspect desktop, narrow viewport, and print output. Verify skip navigation, heading order, table headers/captions, focus visibility, color contrast, long titles, long URLs, empty states, missing dates, no-record pages, local links, external-link labels, and page breaks.
