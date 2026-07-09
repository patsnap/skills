# Report HTML Blueprint

This reference defines the default single-file HTML report structure for `patent-panorama-insights`.

## When To Use

Read this file when the user asks for a patent panorama report, landscape report, competitor patent insight, technology roadmap, recommended patent package, or customer-facing HTML deliverable.

## Business Goal

The report should help business, product, R&D, and IP stakeholders move from patent evidence to decisions:

- Which technology directions are active or emerging.
- Which players are investing and where.
- Which technical problems and solution routes deserve deeper reading.
- Which patent packages, asset signals, or risk signals require follow-up.
- Which portfolio or R&D actions are reasonable next steps.

## Default Report Sections

| Section | Purpose | Typical Evidence |
|---|---|---|
| Cover | Topic, decision goal, scope, date, data source | Project inputs and data cutoff |
| Executive Summary | 3 to 7 decision-oriented findings | L1 to L4 evidence chain |
| Scope And Method | Scope table, search logic, counting method, limitations | Search log and de-noising log |
| Landscape Dashboard | Trend, assignee, jurisdiction, legal status, branch overview | Aggregation tables |
| Technology Map | Taxonomy, branch heatmap, evolution, problem-solution map | Tag table and representative patents |
| Deep Dives | Key technical branches and solution clusters | Claims, abstracts, descriptions, citations |
| Competitor Portraits | Player-by-player layout and possible direction | Assignee-normalized datasets |
| Patent Package | Recommended patents, reasons, next actions | Patent cards and evidence register |
| Asset And Risk Signals | Legal status, legal events, transfers, licenses, pledges, awards | Legal and asset MCP outputs |
| Recommendations | Product, R&D, and portfolio implications | L1 to L4 synthesis |
| Appendix | Search strategy, taxonomy definitions, data tables, evidence register | Full reproducibility materials |

## Page Structure

Use a dense consultant-report layout:

1. Sticky or simple top navigation.
2. Left-aligned section headers.
3. KPI strips for sample size, cutoff date, counting method, and scope.
4. Charts near the conclusion they support.
5. Tables for taxonomy, search sets, patent package, and evidence register.
6. Compact note blocks for limitations and legal boundaries.

Avoid marketing-style hero pages. This is a decision report, not a landing page.

For visual style, dashboard layout, color tokens, chart blocks, matrices, patent cards, and responsive behavior, follow `report-visual-style.md`.

## Executive Summary Pattern

Each finding should follow:

```text
Finding -> data evidence -> representative evidence -> business implication -> recommended action
```

Use evidence tags:

| Tag | Meaning |
|---|---|
| L1 | Direct data fact |
| L2 | Observed pattern |
| L3 | Analytical inference |
| L4 | Business recommendation |
| L5 | Legal or risk signal |

## Chart And Table Library

| Question | Preferred View |
|---|---|
| Is the field growing? | Annual trend line or stacked bar |
| Who is investing? | Assignee ranking bar chart |
| Where is protection targeted? | Jurisdiction bar chart or matrix |
| Which branches are active? | Technology branch distribution |
| How do players differ? | Assignee x branch heatmap |
| What is product relevance? | Product/component x technology matrix |
| What problems are solved? | Problem x solution matrix |
| Which patents deserve reading? | Recommended patent table and cards |
| Are there asset or risk signals? | Signal table with follow-up action |

## HTML Requirements

- Single self-contained HTML file by default.
- Embedded CSS and chart data.
- No external confidential data files unless the user explicitly asks.
- Chart captions must include counting method and data cutoff.
- Legal and risk content must be labeled as signals, not legal opinions.
- Put full search logic and limitations in the appendix.
- Use readable tables with horizontal overflow for wide patent lists.
- Do not hide material limitations in footnotes only.

## Required Report Metadata

Include these near the top:

| Field | Example Placeholder |
|---|---|
| Technology domain | `[technology_domain]` |
| Decision goal | `[decision_goal]` |
| Entity scope | `[all_industry_or_selected_players]` |
| Geography | `[jurisdiction_set]` |
| Time range | `[date_range]` |
| Counting method | `[publication_or_family_or_application]` |
| Data source | `PatSnap / 智慧芽 patent MCP/API` |
| Data cutoff | `[YYYY-MM-DD]` |
| Legal boundary | `Signals only, not legal opinions` |

## V0 Boundary

V0 can generate a credible HTML structure from installed patent MCP outputs and local aggregation.

Do not present these as verified unless the environment exposes them:

- Full NPL or paper landscape.
- SEP essentiality.
- Formal FTO, infringement, validity, novelty, or inventiveness opinions.
- Complete litigation strategy.
- Built-in SaaS panorama statistics or export APIs.

## Quality Checklist

- The report opens locally without broken CSS, blank charts, or unreadable tables.
- Every major conclusion has an evidence tag.
- Search scope, cutoff date, and counting method are visible.
- Legal/risk statements are clearly framed as signals.
- No confidential customer names, project names, company combinations, patent numbers, or historical report sentences appear.
- The appendix allows another analyst to reproduce the search logic.
