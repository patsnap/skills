# Scientific and Executive Visual Standard

Use this reference when rendering the client-facing HTML output. The visual system is localized for international scientific, engineering, R&D, strategy, and IP audiences. It should look like a rigorous analytical publication with executive dashboard utility—not a consumer product, marketing site, or imitation of a named software brand.

## Contents

- [Design intent](#design-intent)
- [Visual principles](#visual-principles)
- [Color and typography](#color-and-typography)
- [Layout](#layout)
- [Component contracts](#component-contracts)
- [Charts and tables](#charts-and-tables)
- [Accessibility, print, and responsive behavior](#accessibility-print-and-responsive-behavior)
- [Visual QA](#visual-qa)

## Design intent

Favor the clarity of a peer-reviewed technical report, the density of a professional intelligence dashboard, and the restraint expected in an executive briefing. Use visual hierarchy to distinguish observations, inferences, recommendations, and legal or asset signals.

## Visual principles

- Use light neutral backgrounds and white analytical surfaces.
- Prefer section rules, whitespace, and typographic hierarchy to excessive cards.
- Place the question, takeaway, evidence, and qualification in a predictable order.
- Make charts, matrices, tables, and patent evidence the main visual language.
- Keep the first viewport decision-oriented: title, scope, cutoff, unit, key metrics, and executive findings.
- Avoid gradients, floating decoration, oversized hero areas, stock imagery, glass effects, heavy shadows, and ornamental animation.
- Do not reproduce the visual identity, icons, or interface of Microsoft, PatSnap, or another vendor.
- Use cards only for repeated comparable objects such as KPIs, patents, or dated signals.

## Color and typography

Use an accessible, restrained palette. These defaults work on screen and in print:

| Token | Hex | Use |
|---|---|---|
| `page` | `#F4F6F8` | Page background |
| `surface` | `#FFFFFF` | Analytical surface |
| `surface-muted` | `#F8FAFC` | Alternate rows or notes |
| `ink` | `#17212B` | Primary text |
| `ink-muted` | `#52606D` | Captions and metadata |
| `rule` | `#D5DCE3` | Dividers and table rules |
| `data-blue` | `#2463A8` | Primary quantitative series |
| `data-teal` | `#087F8C` | Secondary series or constructive signal |
| `data-violet` | `#6B5CA5` | Optional third series |
| `caution` | `#9A6700` | Qualification or watch item |
| `risk` | `#B42318` | Escalation signal |

Do not encode meaning by color alone. Pair color with labels, symbols, line patterns, or text. Check categorical palettes for color-vision accessibility and limit simultaneous categories; use small multiples or tables when a legend becomes burdensome.

Use system fonts such as `Inter`, `Arial`, `Helvetica`, or `sans-serif`; do not depend on remote fonts. A practical scale is:

| Role | Size |
|---|---|
| Report title | 30–36 px |
| Section heading | 21–25 px |
| Subsection heading | 16–19 px |
| Body and table text | 14–15 px |
| Caption and note | 12.5–13.5 px |

Use sentence case for headings. Keep body line height around 1.45–1.6. Do not use viewport-scaled type or decorative letter spacing.

## Layout

Use a centered, readable report container with full-width analytical bands where a matrix or evidence table needs room. Maintain this narrative sequence unless the scenario reference specifies a justified variation:

```text
Executive summary → scope and method → landscape dashboard → technology map
→ deep dives → competitor profiles → patent package → asset and risk signals
→ recommendations → appendix
```

- Use CSS grid for KPI strips and comparable analytical blocks.
- Keep section headings left-aligned and stable across the document.
- Place each chart close to the claim it supports.
- Keep navigation compact, printable, and non-obstructive.
- Avoid deeply nested surfaces and card-within-card layouts.
- On narrow screens, collapse grids to one column and allow matrices and evidence tables to scroll horizontally.

## Component contracts

### Scope strip

Show technology domain, decision objective, jurisdictions, period, unit of analysis, data cutoff, and source. These are analytical controls, not decorative metadata.

### KPI block

Include the value, concise label, scope or source field, and any comparison basis. Do not show an estimate as a KPI unless it is clearly labeled and methodologically supported.

### Chart block

Include:

1. a question-led title;
2. a one-sentence takeaway;
3. the chart;
4. a caption naming date field, unit, scope, and cutoff; and
5. a limitation note where needed.

If data are missing or incomplete, show a structured unavailable-data notice with the missing requirement. Never draw plausible-looking substitute values.

### Matrix block

State row dimension, column dimension, cell measure, counting unit, multi-label duplicate-counting policy, and whether classifications are automated, reviewed, or fully validated.

### Patent evidence card

Show the publication or family identifier, normalized assignee, technical problem, solution, reported effect, evidence location, selection reason, and next action. Do not state infringement, validity, FTO, essentiality, novelty, or inventive-step conclusions.

### Signal card

Show signal type, event date, source, why it matters, recommended follow-up, and the research-only/legal-boundary note. Use caution or risk color sparingly and avoid alarmist visual treatment.

## Charts and tables

- Use flat two-dimensional charts.
- Prefer bars for rankings, lines for trends, heatmaps for matrices, and tables for patent-level evidence.
- Start quantitative axes at an honest baseline or clearly explain a truncated axis.
- Label units and denominators; show `n` where sampling is involved.
- Use direct labels when they reduce legend lookup.
- Avoid dual axes unless the relationship cannot be communicated more clearly another way.
- Avoid 3D marks, unexplained area encodings, decorative animation, and excessive precision.
- Identify missing, suppressed, or not-applicable values distinctly.
- Keep tables dense but readable, with semantic headers, aligned numeric columns, wrapped technical text, and break-safe identifiers.
- Use alternating rows only when they materially improve scanning.

## Accessibility, print, and responsive behavior

- Meet WCAG AA contrast for normal text wherever practical.
- Preserve keyboard navigation and visible focus for interactive controls.
- Use semantic headings, `<caption>` or nearby table descriptions, and text equivalents for essential chart findings.
- Do not communicate status by color alone.
- Prevent long patent numbers, chemical names, organization names, and URLs from breaking the layout.
- Include print styles that remove sticky navigation, preserve section order, avoid clipped charts, and repeat table headers where supported.
- Verify desktop, tablet, mobile, and print/PDF rendering.

## Visual QA

- The first viewport states topic, decision scope, cutoff, unit, key metrics, and executive findings.
- Visual emphasis reflects evidence strength rather than visual drama.
- Charts and tables remain legible at normal zoom and have complete captions.
- Matrices scroll safely and expose their definitions.
- Patent cards communicate problem–solution–effect and traceability.
- Legal and asset signals are distinct, dated, qualified, and non-alarmist.
- No text overlaps, clipped content, blank graphics, broken links, remote dependencies, or vendor imitation remain.
- The report prints cleanly in grayscale as well as color.

## Scientific figure conventions

Treat each visual as an analytical figure rather than decoration.

| Element | Convention |
|---|---|
| Figure number | Number sequentially when the report is long or likely to be exported |
| Question | Put the analytical question in the title or immediately above it |
| Finding | State one bounded takeaway below the title |
| Axes | Name the measure, unit, date basis, and transformation |
| Denominator | State it for shares, rates, and normalized indices |
| Uncertainty | Show confidence intervals, sample size, or a textual limitation when applicable |
| Source | Identify service, query/artifact version, and cutoff |
| Notes | Define family method, multi-label duplication, normalization, and exclusions |

Use no more numerical precision than the evidence supports. Sort categories by analytical logic rather than alphabetically when comparison is the purpose. Preserve a stable category order across comparable figures.

## Evidence-state styling

Use consistent non-color cues for evidence states:

- `L1 fact`: plain data treatment with a source marker;
- `L2 pattern`: analytical callout with the relevant measure;
- `L3 inference`: labeled “Inference” and paired with its basis;
- `L4 recommendation`: action block with owner or next step when known;
- `L5 legal/asset signal`: bordered signal block with date and verification note;
- `Unavailable`: muted hatch or text state, never zero;
- `Provisional`: dashed boundary or explicit provisional label; and
- `Human validated`: check label plus reviewer/date field when permitted.

## International formatting

- Use ISO `YYYY-MM-DD` dates in data tables and an audience-appropriate spelled-out date in prose.
- State currency and units explicitly; do not infer a currency from a symbol alone.
- Use locale-neutral decimal data in machine-readable artifacts and audience-local formatting only in the rendered view.
- Expand uncommon acronyms at first use.
- Use “organization” or the legally correct entity type instead of the China-specific generic “applicant” when discussing corporate groups.
- Preserve official patent-office and jurisdiction names; do not translate identifiers.
- Avoid flags as jurisdiction labels because they can conflate office, territory, nationality, and market.

## Export checklist

- Screen HTML, print preview, and PDF convey the same analytical hierarchy.
- Links and anchor navigation work without network access.
- Tables repeat or retain enough context across page breaks.
- Figures do not split from their titles, captions, or limitations where CSS can prevent it.
- Page headers or footers identify topic, confidentiality marking if supplied, and cutoff.
- Copying a table preserves meaningful headers and values.
- No hidden interactive state contains material evidence unavailable in print.
- The exported filename and visible title identify the report version without exposing confidential data.
