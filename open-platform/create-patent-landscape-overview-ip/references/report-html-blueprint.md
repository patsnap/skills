# Patent Landscape HTML Report Blueprint

Use this reference when the requested deliverable is a patent landscape, competitor patent assessment, technology-evolution review, recommended patent package, or client-facing HTML report. Pair it with `report-visual-style.md` and the relevant scenario reference.

## Contents

- [Decision purpose](#decision-purpose)
- [Default report architecture](#default-report-architecture)
- [Evidence model](#evidence-model)
- [Views and components](#views-and-components)
- [HTML and metadata requirements](#html-and-metadata-requirements)
- [V0 boundary](#v0-boundary)
- [Quality gate](#quality-gate)

## Decision purpose

Build an evidence-led report that helps business, product, R&D, strategy, and IP stakeholders decide:

- which technical directions are active, mature, or emerging;
- which organizations are investing and how their portfolios differ;
- which technical problems and solution routes warrant deeper review;
- which patent groups, asset signals, or risk signals need follow-up; and
- which portfolio, product, or R&D actions are proportionate to the evidence.

Do not turn the report into a marketing page or a legal opinion.

## Default report architecture

| Section | Decision function | Typical evidence |
|---|---|---|
| Cover and scope strip | Identify topic, decision, scope, cutoff, and source | Project inputs and collection record |
| Executive summary | Present three to seven decision-relevant findings | L1–L4 evidence chains |
| Scope and method | Make the search, taxonomy, counting, and limits reproducible | Search and screening logs |
| Landscape dashboard | Show trends, organizations, jurisdictions, status, and branches | Verified population aggregations |
| Technology map | Explain taxonomy, branch activity, evolution, and problem–solution structure | Tagged records and representative families |
| Technical deep dives | Examine important branches and solution clusters | Claims, abstracts, descriptions, and citations |
| Competitor profiles | Compare normalized organization portfolios and apparent emphases | Organization-normalized records |
| Patent package | Prioritize records or families and specify follow-up | Patent cards and evidence register |
| Asset and risk signals | Surface legal events, transfers, licenses, pledges, or awards when available | Dated event and asset records |
| Recommendations | State product, R&D, and portfolio implications | L1–L4 synthesis |
| Appendix | Preserve methods, definitions, tables, and evidence traceability | Reproducibility materials |

Use a compact top navigation when helpful, left-aligned headings, a visible scope strip, and charts adjacent to the conclusion they support. Use tables for taxonomies, search sets, patent packages, and evidence registers. Put material qualifications in the main narrative as well as the appendix.

## Evidence model

Write each major finding as:

```text
Finding → quantitative or documentary evidence → representative patent evidence
→ decision implication → proportionate next action
```

Apply these labels consistently:

| Label | Meaning |
|---|---|
| L1 | Direct, source-backed fact |
| L2 | Pattern observed in the defined dataset |
| L3 | Analytical inference, explicitly identified as such |
| L4 | Business, R&D, or portfolio recommendation |
| L5 | Legal, transactional, or risk signal requiring specialist review |

Never upgrade an L3 inference to fact or an L5 signal to a legal conclusion. Every representative patent must be traceable to its publication or family identifier and evidence field.

## Views and components

| Decision question | Preferred view |
|---|---|
| Is activity changing over time? | Annual line or stacked bar with date basis stated |
| Which organizations are active? | Normalized-assignee ranking |
| Where is protection sought? | Jurisdiction bar chart or matrix |
| Which technical branches are active? | Branch distribution with taxonomy version |
| How do organizations differ? | Organization × branch heatmap |
| How does the topic map to products? | Product/component × technology matrix |
| Which problems and solutions recur? | Problem × solution matrix |
| Which patents need human reading? | Prioritized table plus patent cards |
| Which asset or risk events matter? | Dated signal table with follow-up action |

Every chart block must contain a title, one-sentence takeaway, visual, data caption, and relevant limitation. Every matrix must name its row and column dimensions, cell measure, counting method, treatment of multi-label records, and tag-validation state.

Patent cards should contain:

- representative publication or family identifier;
- normalized assignee;
- technical problem, solution, and reported effect;
- supporting patent field or passage location;
- reason for prioritization; and
- next review action.

Asset or legal-signal cards should contain the signal type, dated source, significance, recommended follow-up, and a boundary statement.

## HTML and metadata requirements

Deliver a single self-contained HTML file unless the user requests another package format.

- Embed CSS and report data; do not load remote scripts, fonts, trackers, or CDN assets.
- Prefer semantic HTML, keyboard-safe navigation, accessible tables, and printable styles.
- Keep wide tables horizontally scrollable and long identifiers break-safe.
- Show an explicit unavailable-data state instead of an invented chart.
- Include counting method and data cutoff in each quantitative caption.
- Keep complete-population metrics separate from samples, candidate pools, and Top-K lists.
- Put the complete query logic, taxonomy version, screening rules, and limitations in the appendix.

Show this metadata near the beginning:

| Field | Placeholder or convention |
|---|---|
| Technology domain | `[technology_domain]` |
| Decision objective | `[decision_objective]` |
| Organization scope | `[industry_wide_or_named_organizations]` |
| Jurisdictions | `[jurisdiction_set]` |
| Time period | `[date_range]` |
| Unit of analysis | `[publication_application_or_family]` |
| Data sources | `PatSnap global patent services and documented supplementary sources` |
| Data cutoff | `[YYYY-MM-DD]` |
| Legal boundary | `Research signals only; not a legal opinion` |

Use ISO dates. Explain whether “priority year,” “filing year,” or “publication year” drives a time series. State the family definition and assignee-normalization policy when either affects counts.

## V0 boundary

V0 may build a credible landscape from installed global PatSnap MCP outputs and reproducible local aggregation. Do not claim that any of the following are verified unless a suitable source and method are available:

- a complete non-patent-literature landscape;
- standards-essential-patent essentiality;
- formal freedom-to-operate, infringement, validity, novelty, or inventive-step opinions;
- a complete litigation strategy; or
- proprietary in-product analytics or export capabilities that the active MCP contract does not expose.

## Quality gate

- The report opens locally with no missing assets, blank charts, or unreadable tables.
- Topic, decision objective, scope, cutoff, unit, and source are visible without searching the appendix.
- Every major conclusion carries the appropriate evidence label and traceable support.
- Population metrics are based on verified complete retrieval or server-side aggregations.
- Samples and prioritization lists are visibly identified and never presented as the full population.
- Legal and asset statements remain dated signals, not opinions or predictions.
- Confidential client names, project terms, patent identifiers, and legacy report prose are absent unless explicitly supplied for this report.
- Another analyst can reproduce the search and classification logic from the appendix.

