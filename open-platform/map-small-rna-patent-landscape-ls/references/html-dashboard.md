# Multidimensional Small-RNA Patent Timeline Specification

## Purpose

Generate one self-contained HTML file for a company or portfolio patent landscape. The visualization supports analyst exploration and stakeholder decisions while remaining a scientific evidence report rather than a decorative dashboard.

## Title and scope

Use:

```text
{Company or Portfolio} — Multidimensional Small-RNA Patent Timeline
```

Use only a verified normalized entity/portfolio name. If multiple companies are in scope, name the portfolio or state the group and explain entity normalization in Methodology. Do not select an “operating company” by unsupported inference.

## Data contract

The HTML must derive from the same reviewed structured layer and `Timeline Tag Data` used by the workbook.

### Patent/family record

```json
{
  "record_id": "FAM-001",
  "display_id": "WO...A1",
  "title": "...",
  "analytical_unit": "family",
  "family_definition": "INPADOC extended family",
  "timeline_year": 2024,
  "timeline_date_basis": "earliest verified family publication",
  "current_publication_date": "YYYY-MM-DD",
  "applicants": [],
  "jurisdictions": [],
  "family_count": 12,
  "current_member_status": "pending",
  "family_status_summary": "...",
  "review_priority": "priority_review|material|context|low_current_relevance",
  "priority_reason": "...",
  "tags": {},
  "evidence": {},
  "source_ids": [],
  "record_url": "...",
  "known_gaps": []
}
```

### Opportunity record

```json
{
  "opportunity_id": "OPP-001",
  "is_patent": false,
  "dimension": "delivery_tissue",
  "lane_tag_id": "DELIVERY-CNS-IT",
  "display_period": "Next decision horizon",
  "title": "Evaluate CNS exposure and repeat-dose delivery evidence",
  "observed_gap": "...",
  "evidence_source_ids": [],
  "counterevidence": "...",
  "hypothesis": "...",
  "recommended_validation": "...",
  "potential_filing_theme": "...",
  "confidence": "medium",
  "owner": "...",
  "timing_or_trigger": "..."
}
```

Never give an opportunity a patent publication number, patent URL, legal status, or fabricated future filing year.

## Default view

Default dimension: stakeholder-readable technology direction.

Raw genes are expert subdivisions unless the user's decision is explicitly target-by-target. Show gene/disease/platform labels in details and filters.

If no stakeholder direction has been reviewed, default to another complete dimension and label the reason. Do not invent assignments to satisfy the default.

## Dimension switches

Provide buttons/tabs for:

- Technology direction;
- Mechanism;
- RNA modality;
- Chemistry / structure;
- Delivery / tissue;
- Productization stage.

Every switch must:

- update lanes, counts, overview, selected filter, and URL/state where implemented;
- preserve current text and cross-dimension filters where meaningful;
- announce changes for assistive technology;
- handle records with multiple tags;
- expose `Unresolved` rather than dropping untagged records.

## Filters

Provide:

- All / sustained or recent growth / historically concentrated or isolated / priority review;
- active-dimension tag selector;
- free-text search across publication/family ID, title, applicant, target, mechanism, chemistry, delivery, disease, countries, and source IDs;
- optional jurisdiction/status/evidence-confidence filters when data supports them;
- clear-all control and visible result count.

Do not call a filing trend “growth” from a partial current year without adjustment/label.

## Timeline

### Date basis

Use earliest verified family publication year for a family-level view. If missing, use the current member publication year and label the fallback. If neither exists, use `Date unresolved` rather than a guessed year.

### Lanes

- one lane per active tag;
- multi-tag records may appear in multiple lanes, but the portfolio total must count unique analytical records;
- lane label includes tag definition, unique count, assignment count, and evidence coverage;
- order by a documented logic such as strategic sequence, count, or alphabetic order;
- provide a compact list/table fallback for users who cannot use the visual timeline.

### Patent cards

Card visual prominence may reflect review priority, but not legal strength. Each card includes:

- linked publication/family display ID;
- concise title;
- normalized applicant/entity;
- current versus earliest family date distinction;
- status text;
- review-priority text;
- source/evidence indicator;
- accessible name.

Do not use opacity so low that evidence becomes unreadable. Do not encode priority by color alone.

### Opportunity markers

Render only evidence-backed opportunities from the structured strategy layer. Use an amber dashed border and explicit `Analyst opportunity — not a patent` label.

Do not always create markers for CNS/intrathecal, ophthalmic/intravitreal, kidney, formulation, NMD, cryptic/poison exon, splice switching, or patient selection. These source-case examples are candidate questions, not universal portfolio gaps.

Place opportunities in a separate `Next decision horizon` column or strategy band unless a user-supplied target date exists. Do not place them in “current year + 1” automatically.

## Visual design

### Scientific light theme

```css
:root {
  --canvas: #f5f7f9;
  --surface: #ffffff;
  --surface-2: #eef3f5;
  --ink: #17212b;
  --muted: #586675;
  --line: #d5dde3;
  --line-strong: #b8c4cc;
  --accent: #236879;
  --accent-soft: #e0f0f3;
  --green: #3d7058;
  --green-soft: #e5f1e9;
  --amber: #8b5b18;
  --amber-soft: #fbf1df;
  --red: #963d37;
  --red-soft: #f8e9e7;
  --violet: #625989;
  --violet-soft: #eeeaf7;
  --blue: #376e9e;
  --blue-soft: #e8f0f8;
}
```

Use system fonts and high contrast. Optional dark mode may be added only after the light mode is complete and independently accessible.

### Layout

- concise evidence header, no landing-page hero;
- sticky control bar on desktop only;
- maximum content width about 1440 px where the timeline needs it;
- strategy findings above the timeline;
- main timeline plus evidence overview, collapsing to one column on smaller screens;
- compact gaps/opportunities region;
- methodology/source/counting disclosure;
- no gradient, glow, particles, ticker, decorative animation, or copied product UI.

### Lane colors

Use a color-blind-conscious palette, but keep text/status labels and borders. Assign colors deterministically by tag ID so switching/filtering does not change meaning.

Suggested palette:

```text
#376e9e  #3d7058  #8b5b18  #625989  #a45737  #1f7281
#8c4e72  #64752f  #78643b  #5d6c9e  #9a5f2f  #3e7892
```

### Review-priority treatment

Use border thickness/label placement and modest background tint:

- Priority review — stronger left/top border and explicit label;
- Material — medium border;
- Context — standard border;
- Low current relevance — subdued tint but readable text.

Do not use the source's alpha scale down to 0.28 for essential text. Do not equate brightness with claim strength.

### Card CSS pattern

```css
.patent-card {
  position: relative;
  min-width: 10rem;
  padding: .55rem .65rem;
  border: 1px solid var(--lane-color, var(--line-strong));
  border-top: 3px solid var(--lane-color, var(--accent));
  border-radius: .45rem;
  color: var(--ink);
  background: color-mix(in srgb, var(--lane-color, var(--accent)) 10%, white);
  box-shadow: 0 2px 8px rgba(23,33,43,.10);
}
.patent-card:hover,
.patent-card:focus-within {
  box-shadow: 0 7px 20px rgba(23,33,43,.17);
  transform: translateY(-1px);
}
@media (prefers-reduced-motion: reduce) {
  .patent-card { transition: none; }
}
```

If `color-mix` support is a concern, calculate safe opaque colors in data preparation and store them as CSS variables. Do not rely on JavaScript-only styling.

### Lane labels

Use a colored left border and visible text definition. Secondary text uses `--muted` with verified contrast—not white mandated by a dark theme and not illegible gray.

### Opportunity marker

```css
.opportunity {
  border: 2px dashed var(--amber);
  background: var(--amber-soft);
  border-radius: .45rem;
  padding: .55rem .65rem;
  color: var(--ink);
}
.opportunity-title { color: var(--amber); font-weight: 700; }
```

## Strategy cards

Above the timeline, render three evidence-derived groups:

- `Portfolio gaps`;
- `R&D hypotheses`;
- `Filing playbook insights`.

Each card must contain:

- finding ID;
- bounded finding;
- patent/tag/source evidence;
- counterevidence or limitation;
- recommended action;
- confidence;
- owner/timing.

Do not manually write these after data generation without adding them to the structured strategy layer and workbook.

## Hover/focus evidence panel

The panel must be accessible by pointer and keyboard and include:

- current publication/family identifier and exact source link;
- title and normalized applicant;
- stakeholder direction and expert subdivision;
- patent/claim type;
- current publication date and earliest family date;
- target/disease/mechanism;
- RNA modality;
- chemistry/structure;
- delivery/tissue/route;
- productization layer;
- family count and jurisdictions with family definition;
- current-member status and family-status caveat;
- review priority and rationale;
- claim, family, status, and tag evidence strength separately;
- design-around assessment state—not a definitive difficulty score;
- reusable filing insight;
- differentiation hypothesis;
- recommended action;
- sources, confidence, and known gaps.

Avoid vague labels such as “moat.” Prefer `claim protection signal`, `portfolio layer`, or `competitive review point`.

Do not make crucial content hover-only. Provide click/focus pinning or a details drawer and ensure it appears in the table fallback.

## Header legend

Show text labels for review priority. If chips/dots are used, add accessible names and do not rely on hue/opacity alone.

## Right-side overview

Title: `Tag Overview and Distribution`.

For the active dimension show:

1. unique visible tags;
2. unique patent/family records;
3. patent-tag assignments;
4. concentrated tags;
5. recent/sustained activity with period caveat;
6. historically concentrated/declining/isolated tags;
7. unresolved evidence count.

For each tag:

- definition;
- small year-distribution chart plus accessible data table;
- share with denominator;
- main years and partial-year marker;
- trend label and basis;
- priority-review count;
- average family count with missing-data rule;
- portfolio coverage judgment: strong / moderate / weak / unknown;
- evidence-backed gap hypothesis;
- recommended validation/action.

The panel is analytical, not merely a color legend.

## Charts

Use native SVG, CSS, or canvas only if the report remains understandable through text/table alternatives. Do not load external chart libraries. Chart axes, units, counting rules, partial periods, and data source must be visible.

## Interaction requirements

- buttons are `<button>` elements, not clickable `<div>`;
- active dimension uses `aria-pressed` or tab semantics;
- filter labels and result count are announced;
- search is debounced only if needed and works without network access;
- hover panel also opens on focus/click;
- Escape closes pinned panels;
- focus returns to trigger;
- URL/hash state is optional but must not leak confidential queries;
- reduced motion is honored;
- no telemetry or external requests.

## Responsive behavior

At narrow widths:

- controls wrap or become labeled select elements;
- timeline supports safe horizontal scrolling with a visible cue;
- lane labels remain associated with rows;
- evidence panel becomes an in-flow dialog/details region;
- strategy cards stack;
- tables use wrappers or record cards;
- no text smaller than a readable mobile size.

## Print behavior

Print a report view, not the entire interactive canvas at unreadable scale:

- title/scope/key findings;
- strategy cards;
- filtered/current dimension table;
- priority records;
- opportunity hypotheses;
- tag overview;
- methodology/sources.

Hide interactive controls and hover panels. Repeat table headers and show source URLs/IDs.

## Opportunity evidence test

Before adding a marker, verify:

- portfolio coverage was measured under the declared counting rule;
- source/claim/tag evidence is sufficient;
- comparator or scientific evidence is cited if used;
- absence is not merely missing retrieval/tagging;
- proposed R&D hypothesis is technically plausible;
- novelty/FTO/patentability are not assumed;
- a validation action and owner exist;
- marker confidence is displayed.

## Methodology panel

Include:

- scope/cutoff/jurisdictions/languages;
- input and resolution method;
- source/MCP tools and database cutoffs;
- family definition/counting unit;
- timeline year rule;
- status/claim-version hierarchy;
- tag taxonomy version and review method;
- trend windows/partial years;
- strategy/opportunity derivation;
- missing-data semantics;
- known limitations and monitoring plan.

## Implementation checklist

- [ ] HTML is self-contained and parses.
- [ ] Timeline data matches workbook/JSON IDs and counts.
- [ ] Default and all five alternate dimensions render.
- [ ] Multi-tags do not inflate unique portfolio totals.
- [ ] Date basis and unresolved dates are visible.
- [ ] All filters/search/clear controls work.
- [ ] Patent cards are readable and status/priority do not rely on color.
- [ ] Evidence panel works with pointer, keyboard, click, and Escape.
- [ ] Strategy cards derive from the structured layer.
- [ ] Every opportunity passes the evidence test and says `not a patent`.
- [ ] Tag overview shows denominators, periods, and accessible chart data.
- [ ] Narrow viewport and print are usable.
- [ ] No external dependency, credential, absolute path, legacy domain, or fabricated fact remains.
