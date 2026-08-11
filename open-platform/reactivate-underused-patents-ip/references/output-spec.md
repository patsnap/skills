# Deliverable Specification

Use this reference to create internal or external portfolio-activation deliverables.
Read `mcp-boundaries.md` before describing source strength, connector outputs, or links.

## Delivery strategy

- Default to a self-contained HTML report only when the user has supplied an analyzable
  portfolio and file generation is authorized.
- Produce PDF, DOCX, XLSX, PPTX, or Markdown only when requested or clearly within the
  confirmed deliverable scope.
- Use the appropriate artifact workflow and render/inspect visual formats before delivery.
- If inputs are insufficient, provide a structured intake/gap list rather than an empty
  “client report.”
- The final handoff states absolute artifact paths, scope/cutoff, included analysis,
  unresolved diligence, and release status.

## Report architecture

1. **Decision summary:** defined portfolio, evidence coverage, supported activation
   scenarios, management decisions, and critical gates.
2. **Portfolio activation funnel:** inventory → normalized assets → packages → reviewed
   candidates → diligence-ready options, with counts and exclusions.
3. **Prioritized asset/package table:** transparent rubric, evidence quality, scenario
   results and review state.
4. **Selected asset briefs:** technical proposition, rights footprint, evidence,
   possible application, transaction structure options and diligence.
5. **Candidate-counterparty research:** entity, role, technical/rights fit, dated signals,
   exclusions, uncertainty and authorized next research step.
6. **Evidence and diligence gaps:** ownership, status, term, license/encumbrance, funding,
   technical, market, regulatory, privacy and disclosure issues.
7. **30/60/90-day plan:** user-approved owner/role, action, input, deliverable, dependency,
   decision gate and acceptance criterion.
8. **Method and limitations:** connectors, public/internal sources, rubric/scenarios,
   data cutoff, evidence states, and non-legal/non-valuation boundary.
9. **Evidence register and patent-link note:** source IDs/URLs, access conditions and
   unlinked identifiers.

Do not force every section into a one-page brief. A one-page management view may link to
or accompany a full evidence appendix when the user authorizes both.

## Visual standard

Use an international Swiss/scientific executive style:

- white or light-neutral canvas;
- strong grid, alignment, whitespace and typographic hierarchy;
- dark navy/slate text and restrained teal/blue accents;
- amber for incomplete evidence and red only for a true blocking gate;
- system fonts and no remote font dependency;
- flat 2D tables, bars, evidence labels, timelines and asset cards;
- no gradients, stock imagery, decorative hero treatment, 3D charts or vendor UI;
- color plus text/symbols, WCAG-aware contrast and grayscale readability.

The first viewport must show objective, portfolio, cutoff, evidence coverage, supported
options, management decisions and major diligence gates—not an unsupported monetary total.

## Security, accessibility and rendering

- HTML is one self-contained file with embedded CSS and pre-aggregated data.
- Prefer static HTML/CSS/SVG. Minimal inline JavaScript must progressively enhance a
  complete no-script view.
- Load no CDN, remote script/font/tracker/iframe/data file.
- Escape all internal, user, public-source and connector text.
- Validate `https` URLs and add safe external-link attributes.
- Use semantic landmarks, heading order, table headers/captions, visible focus, keyboard
  controls, text chart alternatives, responsive overflow and print/PDF CSS.
- External reports exclude confidential details, personal data, internal thresholds,
  negotiating floors, source-restricted content and post-NDA materials.
- Internal reports apply the project’s confidentiality marking and access rules.

## Patent links

Use a patent-record URL only when the active global connector returns it or current
official global documentation defines it. Never construct a regional link from a patent
ID or sample-test a link through an unavailable connector.

If a verified link is unavailable:

- show the exact publication/application/grant identifier;
- show source connector/operation and evidence ID;
- list it in `unlinked_identifiers`; and
- do not imply that database access is required to understand the public identifier.

## Portfolio activation master table

Recommended fields:

```text
review_rank,package_id,package_name,asset_ids,asset_types,technical_proposition,
application_scenarios,portfolio_role,rights_status_as_of,remaining_term_review,
internal_use_evidence,transaction_history_evidence,technical_signal,
commercial_signal,transaction_readiness,evidence_quality,scenario_results,
candidate_counterparty_types,diligence_gates,activation_options,next_action,
responsible_role,review_status
```

Keep raw facts, normalized values and inferences separate. Do not display a composite
score without dimensions, weights, missing-data treatment and sensitivity.

## Selected asset/package brief

Include:

- evidence-bounded one-sentence proposition;
- problem, technical means and reported effect;
- patents and related know-how/data/software/brand/prototype evidence;
- owner, family, jurisdiction, status, term and encumbrance review state;
- application/field-of-use hypotheses and supporting sources;
- transaction structures to evaluate;
- candidate-counterparty profile, not confirmed interest;
- NDA-safe teaser material and controlled post-NDA materials;
- uncertainties, diligence and decision owner; and
- next validation action.

Do not create an external sales claim from an unverified abstract or valuation score.

## Candidate-counterparty table

```text
candidate_entity,candidate_role,entity_resolution,technical_fit,rights_fit,
dated_need_or_strategy_signals,evidence_sources,alternative_explanations,
conflicts_or_exclusions,research_priority,diligence,next_internal_action,
outreach_authorization_status
```

An outreach hypothesis can identify a function and factual value proposition. Do not
include personal contact data or send messages without explicit authorization.

## Action plan

Each 30/60/90-day item requires:

- action and decision objective;
- responsible role only if supplied/approved;
- required evidence/material;
- dependency and blocking gate;
- deliverable;
- acceptance criterion; and
- exact due date only when user/project scheduling supplies one.

Do not invent progress, owners or deadlines merely to fill a plan.

## Formats

- **HTML:** primary interactive/readable report; validate locally.
- **PDF:** render from validated content and inspect every page.
- **DOCX:** native headings/tables/links, confidentiality/version metadata, render QA.
- **XLSX:** asset master, evidence register, counterparty and action tables; validate
  formulas, filters, data types and spreadsheet-injection safety.
- **PPTX:** management decision deck only when requested; preserve evidence/limitations.

## Disclaimer

The deliverable supports portfolio screening and business workflow design. It is not a
legal opinion, formal appraisal/valuation, tax/accounting opinion, investment advice,
maintenance/abandonment authorization, transaction commitment, confirmed buyer interest,
or permission to disclose/contact. Qualified owners, counsel, valuation/finance, tax,
regulatory, technical and business reviewers must approve the relevant decisions.

