# Report Visual Style

Use this reference when generating the customer-facing HTML report for `patent-panorama-insights`.

## Design Intent

Use a Fluent-inspired enterprise analytics style: clean, calm, dense, trustworthy, and executive-readable.

The report should feel like a premium business intelligence dashboard for product, R&D, strategy, and IP stakeholders.

Do not copy Microsoft product screens, logos, trademarks, icons, or branded UI assets. Treat Fluent as a design inspiration, not a brand template.

## Visual Principles

- Prefer light neutral backgrounds and white analytical surfaces.
- Use subtle borders, restrained depth, and low-contrast section separation.
- Prioritize scannable dashboards over marketing-style storytelling.
- Make charts, matrices, tables, and patent cards the primary visual language.
- Keep the first screen decision-oriented: title, scope, key metrics, and executive findings.
- Avoid decorative gradients, floating blobs, oversized hero sections, stock imagery, and consumer-app styling.
- Avoid nested cards. Use cards only for repeated items such as KPI cards, patent cards, and signal cards.

## Color Tokens

| Token | Hex | Use |
|---|---|---|
| `background` | `#f5f7fb` | Page background |
| `surface` | `#ffffff` | Section and table surface |
| `surface_alt` | `#f9fafc` | Subtle alternate surface |
| `text_primary` | `#1f2937` | Main text |
| `text_secondary` | `#4b5563` | Notes, captions, metadata |
| `border` | `#d9dee8` | Table, card, and section borders |
| `primary` | `#2563eb` | Main chart and emphasis color |
| `secondary` | `#0f766e` | Positive or secondary analytical signal |
| `accent` | `#6d28d9` | Optional third analytical category |
| `warning` | `#b45309` | Watchlist or caution signal |
| `critical` | `#b91c1c` | Legal/risk escalation signal |

Use a restrained palette. Do not let the report become dominated by one hue.

## Typography

- Use system fonts: `Segoe UI`, `Inter`, `Arial`, `sans-serif`.
- Use compact headings for dashboard sections.
- Keep body text readable and business-oriented.
- Minimum readable text size: 13px.
- Do not scale font size with viewport width.
- Letter spacing should remain `0` unless a local design system already requires otherwise.

Recommended scale:

| Role | Size |
|---|---|
| Report title | 28px to 36px |
| Section title | 20px to 24px |
| Block title | 16px to 18px |
| Body | 14px to 15px |
| Caption / note | 12px to 13px |

## Layout

Use a stable report structure:

```text
Executive summary
  -> Scope and method
  -> Landscape dashboard
  -> Technology map
  -> Deep dives
  -> Competitor portraits
  -> Patent package
  -> Asset and risk signals
  -> Recommendations
  -> Appendix
```

Layout rules:

- Use a max-width report container for readability.
- Use full-width report bands or unframed layouts for major sections.
- Use CSS grid for dashboard blocks and KPI strips.
- Keep tables and matrices horizontally scrollable on smaller screens.
- Keep chart blocks consistent: title, key takeaway, visual, data caption.
- Keep navigation simple and non-distracting.

## Component Contracts

### KPI Cards

Each KPI card should include:

- Metric value.
- Short label.
- Scope note or data field.
- Optional comparison or signal.

Do not use KPI cards for unsupported estimates.

### Chart Blocks

Each chart block must include:

- Title.
- Key takeaway.
- Chart.
- Data caption.
- Limitation note when relevant.

Data caption must state:

- Date field.
- Counting method.
- Data cutoff.
- Scope.

If chart data is unavailable, show an unavailable-data note instead of a fake chart.

### Matrix Blocks

Each matrix block must define:

- Row dimension.
- Column dimension.
- Cell value.
- Counting method.
- Whether multi-label records are duplicate-counted.
- Whether labels are rule-hit labels or validated tags.

### Patent Cards

Each patent card must include:

- Representative publication or family placeholder.
- Normalized assignee.
- Technical problem.
- Technical solution.
- Technical effect.
- Evidence source.
- Recommendation reason.
- Next action.

Patent cards must not include infringement, validity, FTO, SEP essentiality, novelty, or inventiveness conclusions.

### Signal Cards

Each legal or asset signal card must include:

- Signal type.
- Evidence source.
- Why it matters.
- Recommended follow-up.
- Legal boundary note.

## Chart Style

- Use flat 2D charts only.
- Avoid 3D effects, heavy shadows, and decorative animation.
- Keep legends concise and close to the chart.
- Use direct labels where they reduce cognitive load.
- Prefer bars for ranking, lines for trends, heatmaps for matrices, and tables for patent-level evidence.
- Use color consistently across sections.
- Avoid color-only meaning; pair color with labels or text.

## Tables

- Tables should be dense but readable.
- Use sticky headers only if the report implementation supports it cleanly.
- Use alternating row backgrounds only when it improves scanning.
- Keep patent tables horizontally scrollable.
- Put long technical summaries in expandable or wrapped cells when practical.

## Accessibility And Responsiveness

- Maintain sufficient contrast for text and chart labels.
- Ensure mobile and desktop layouts do not overlap.
- Use responsive grids that collapse to one column on narrow screens.
- Do not allow long patent IDs, assignee names, or technical terms to break layout.
- Use semantic headings and table headers.

## Do Not

- Do not include fake charts or invented data.
- Do not copy Microsoft-branded UI assets.
- Do not use decorative hero imagery.
- Do not hide material limitations.
- Do not render legal/risk content as definitive legal conclusions.
- Do not use customer-confidential examples in visual placeholders.

## Visual QA Checklist

- The first viewport shows topic, scope, key metrics, and executive findings.
- Dashboard blocks are readable without zooming.
- Charts and tables have captions with data scope.
- Matrices are legible and scroll safely on mobile.
- Patent cards show problem-solution-effect clearly.
- Legal/risk signals are visually distinct but not alarmist.
- No text overlaps, clipped buttons, blank charts, or broken links.
