"""Accessible scientific-report CSS used by the static HTML renderer."""

CSS = r"""
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
  --warning: #7a4e00;
  --warning-bg: #fff7df;
  --danger: #8b2c2c;
  --danger-bg: #fff0f0;
  --success: #21633b;
  --success-bg: #edf7f1;
  --radius: 4px;
  --measure: 82rem;
}

* { box-sizing: border-box; }

html {
  color-scheme: light;
  scroll-behavior: smooth;
}

body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont,
    "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 16px;
  line-height: 1.55;
}

a {
  color: var(--accent-dark);
  text-decoration-thickness: .08em;
  text-underline-offset: .14em;
  overflow-wrap: anywhere;
}

a:hover { color: var(--accent); }

a:focus-visible,
button:focus-visible,
summary:focus-visible {
  outline: 3px solid #f2b84b;
  outline-offset: 3px;
}

.skip-link {
  position: absolute;
  left: .75rem;
  top: -5rem;
  z-index: 50;
  padding: .6rem .8rem;
  background: var(--ink);
  color: var(--paper);
}

.skip-link:focus { top: .75rem; }

.report-header {
  border-bottom: 1px solid var(--line-strong);
  padding: 2.75rem max(1.25rem, calc((100vw - var(--measure)) / 2));
}

.report-kicker {
  color: var(--accent-dark);
  font-size: .78rem;
  font-weight: 700;
  letter-spacing: .1em;
  text-transform: uppercase;
}

.report-title {
  max-width: 55rem;
  margin: .35rem 0 .75rem;
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(2rem, 5vw, 3.6rem);
  font-weight: 600;
  letter-spacing: -.025em;
  line-height: 1.08;
}

.report-meta {
  display: flex;
  flex-wrap: wrap;
  gap: .5rem 1.4rem;
  color: var(--muted);
  font-size: .92rem;
}

.toc {
  position: sticky;
  top: 0;
  z-index: 20;
  border-bottom: 1px solid var(--line);
  background: rgba(255, 255, 255, .97);
}

.toc ul {
  max-width: var(--measure);
  margin: 0 auto;
  padding: .65rem 1.25rem;
  display: flex;
  gap: .35rem 1.1rem;
  overflow-x: auto;
  list-style: none;
}

.toc a {
  white-space: nowrap;
  font-size: .88rem;
  font-weight: 650;
  text-decoration: none;
}

main {
  max-width: var(--measure);
  margin: 0 auto;
  padding: 2rem 1.25rem 5rem;
}

section {
  padding: 2rem 0;
  border-bottom: 1px solid var(--line);
}

h2, h3, h4 { scroll-margin-top: 5rem; }

h2 {
  margin: 0 0 1.2rem;
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(1.55rem, 3vw, 2.2rem);
  line-height: 1.2;
}

h3 {
  margin: 1.8rem 0 .7rem;
  font-size: 1.08rem;
  letter-spacing: .01em;
}

p { max-width: 72ch; }

.scope-grid,
.metric-grid,
.finding-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
  gap: .9rem;
}

.panel,
.metric,
.finding,
.patent-card,
.literature-item,
.news-item {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--paper);
  padding: 1rem;
}

.metric-label,
.field-label {
  color: var(--muted);
  font-size: .78rem;
  font-weight: 700;
  letter-spacing: .045em;
  text-transform: uppercase;
}

.metric-value {
  margin-top: .2rem;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.8rem;
  font-variant-numeric: tabular-nums;
}

.note,
.limitation {
  border-left: 4px solid var(--line-strong);
  background: var(--wash);
  padding: .8rem 1rem;
}

.limitation { border-left-color: var(--warning); background: var(--warning-bg); }

.status {
  display: inline-block;
  border: 1px solid currentColor;
  border-radius: 999px;
  padding: .15rem .52rem;
  font-size: .78rem;
  font-weight: 700;
}

.status-executed { color: var(--success); background: var(--success-bg); }
.status-not-executed,
.status-unavailable { color: var(--warning); background: var(--warning-bg); }
.status-error { color: var(--danger); background: var(--danger-bg); }

.table-wrap { overflow-x: auto; }

table {
  width: 100%;
  border-collapse: collapse;
  font-size: .9rem;
}

caption {
  padding: 0 0 .6rem;
  text-align: left;
  color: var(--muted);
  font-weight: 650;
}

th, td {
  border-bottom: 1px solid var(--line);
  padding: .65rem .7rem;
  text-align: left;
  vertical-align: top;
}

th { background: var(--wash); font-weight: 700; }

.numeric { text-align: right; font-variant-numeric: tabular-nums; }

details {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  margin: .65rem 0;
}

summary {
  cursor: pointer;
  padding: .8rem 1rem;
  font-weight: 700;
}

details > .details-body { padding: 0 1rem 1rem; }

.bar-row {
  display: grid;
  grid-template-columns: minmax(8rem, 15rem) 1fr minmax(4rem, auto);
  gap: .75rem;
  align-items: center;
  margin: .55rem 0;
}

.bar-track { height: .7rem; background: var(--wash); border: 1px solid var(--line); }
.bar-fill { height: 100%; background: var(--accent); }

.term-list { display: flex; flex-wrap: wrap; gap: .45rem; padding: 0; list-style: none; }
.term-list li { border: 1px solid var(--line); padding: .3rem .55rem; }

.record-meta {
  display: flex;
  flex-wrap: wrap;
  gap: .3rem 1rem;
  color: var(--muted);
  font-size: .86rem;
}

.source-note { color: var(--muted); font-size: .82rem; }
.empty { color: var(--muted); font-style: italic; }

footer {
  max-width: var(--measure);
  margin: 0 auto;
  padding: 1.5rem 1.25rem 3rem;
  color: var(--muted);
  font-size: .85rem;
}

@media (max-width: 42rem) {
  .report-header { padding-top: 2rem; }
  .bar-row { grid-template-columns: 1fr auto; }
  .bar-track { grid-column: 1 / -1; }
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
}

@media print {
  :root { --ink: #000; --muted: #333; --line: #999; --paper: #fff; --wash: #f3f3f3; }
  @page { size: A4; margin: 14mm; }
  body { font-size: 10pt; }
  .skip-link, .toc { display: none; }
  .report-header, main, footer { max-width: none; padding-left: 0; padding-right: 0; }
  section { break-before: auto; }
  details { break-inside: avoid; }
  details > .details-body { display: block !important; }
  a { color: #000; text-decoration: underline; }
  a[href^="http"]::after { content: " (" attr(href) ")"; font-size: 8pt; overflow-wrap: anywhere; }
  .panel, .metric, .finding, .patent-card, .literature-item, .news-item { break-inside: avoid; box-shadow: none; }
}
"""
