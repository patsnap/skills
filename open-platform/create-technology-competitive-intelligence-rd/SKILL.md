---
name: create-technology-competitive-intelligence-rd
description: Create an evidence-led technology competitive-intelligence report for a defined company, technology, market, and review period. Use when a user needs competitor tiering, patent and technology comparisons, customer or partner mapping, event monitoring, threat assessment, and actionable R&D recommendations in a self-contained HTML briefing.
---

# Create Technology Competitive Intelligence

## Purpose

Build a decision-ready competitive-intelligence briefing from reviewed patent, market, company, product, and event evidence. The report is designed for global R&D, strategy, product, and IP teams. It must distinguish sourced facts, analyst calculations, assumptions, and recommendations.

This skill preserves the source package's three report generations:

- `references/template_v8.html`: a compact thirteen-section research worksheet and compatibility layout.
- `references/template_v11.html`: the full evidence-led ten-module briefing with competitor profiles, market and portfolio comparisons, SWOT, customer matrix, events, threat assessment, actions, resource allocation, and implementation timeline.
- `references/template_v12.html`: the current template; it retains the V11 modules and exposes the four executive KPI evidence panels inline.

Use V12 unless the user specifically requests the compact V8 structure or the V11 interaction pattern.

## Appropriate requests

Use this skill for a defined technology or product domain when the user asks to:

- compare a focal company with named or discoverable competitors;
- map technical routes, patent portfolios, products, customers, partnerships, or recent events;
- identify evidence-backed threats, opportunities, gaps, and response options;
- produce a management-grade HTML competitive-intelligence briefing;
- refresh an existing briefing for a new evidence cutoff date.

Do not use the report as a substitute for legal advice, an FTO opinion, valuation advice, or primary customer research.

## Required scope

Confirm or infer conservatively:

| Field | Requirement |
|---|---|
| Focal organization | Legal or commonly used company name |
| Technology scope | Included products, functions, materials, routes, and exclusions |
| Geography | Jurisdictions and commercial markets covered |
| Time window | Evidence cutoff and event lookback period |
| Competitor set | Tier A direct competitors and Tier B adjacent or emerging players |
| Decision | The management or R&D decision the report must support |
| Evidence standard | Acceptable databases, public sources, and confidence rules |

If a scope field is missing, state the working assumption in the report. Never silently substitute a country-specific classification, company set, or market boundary.

## Evidence preparation

Build an evidence register before drawing conclusions. Each material record needs:

- a stable record identifier;
- title or event name;
- source and direct URL where licensing permits;
- publication or event date;
- access date and evidence cutoff;
- organization and technology tags;
- geography or jurisdiction;
- review status;
- analyst note and confidence level.

Normalize patent results by simple or extended family as appropriate. Record whether counts represent publications, applications, grants, or families. State the query, database, jurisdictions, date range, legal-status treatment, and deduplication method. A patent hit is evidence of a document, not proof of infringement, validity, freedom to operate, commercial use, or technical superiority.

Market values must carry currency, price year, geography, segment definition, source date, and whether the number is reported, calculated, or estimated. Company, product, customer, certification, partnership, and event claims require a dated source. Label analyst inference explicitly.

## Recommended PatSnap MCP mapping

When available in the user's environment, use the verified global connectors below and retain their returned record links or identifiers:

- `advanced_patent_search` — [PatSnap Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search) for patent discovery, family-aware review, applicants, inventors, classifications, dates, and legal-status fields.
- `patent_briefing` — [PatSnap Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing) for evidence-backed summaries of selected patent records.

Connector output still requires analyst review. Do not invent tool names, connector URLs, result fields, or record links. If a connector is unavailable, document the limitation and use user-supplied or independently verified public evidence.

## Analysis workflow

1. Freeze the scope, cutoff date, definitions, and competitor inclusion rules.
2. Build and quality-check the evidence register.
3. Separate direct competitors, adjacent players, suppliers, customers, and potential entrants.
4. Normalize patent families, names, currencies, dates, units, and market segments.
5. Compare technical routes using consistent dimensions and cited evidence.
6. Assess portfolio position without converting document counts into legal conclusions.
7. Map customers, partners, certifications, and events only when supported by dated sources.
8. Score threats and opportunities with a disclosed rubric and uncertainty.
9. Link every action to an observed gap, trigger, owner, timing, and validation metric.
10. Run the evidence, legal-language, numerical-consistency, and visual QA gates.

## Scoring rules

Scores are optional analytical aids. If used, disclose dimensions, weights, scale anchors, missing-data treatment, and calculation date. Keep raw evidence available beside the score. Never show an unexplained composite number or imply precision beyond the evidence.

For threat assessment, keep probability, impact, time horizon, reversibility, and evidence confidence separate. For opportunity assessment, distinguish market attractiveness, technical fit, access feasibility, time-to-value, and evidence confidence.

## Report modules

The current V12 report contains:

1. executive summary with four inline KPI evidence panels;
2. scope, method, coverage, and limitations;
3. market and technology landscape;
4. focal-company position and SWOT;
5. Tier A competitor profiles;
6. Tier B and emerging-player watchlist;
7. customer, partner, or application matrix;
8. material events and monitoring triggers;
9. threat and opportunity assessment;
10. prioritized actions, resource allocation, timeline, and final comparison.

Every module must tolerate missing evidence. Use `Not established from reviewed evidence` rather than fabricated values.

## Generate the HTML

Prepare a UTF-8 JSON object outside the package with the required report fields, then run:

```bash
python scripts/generate_report.py --data /path/to/reviewed-data.json --output /path/to/report.html
```

The renderer accepts only explicit template tokens and HTML-escapes inserted values. It does not perform blind company-name replacement. Run `python scripts/generate_report.py --help` for the supported contract.

The input must set `review_status` to `reviewed` and provide, at minimum, the report title, focal organization, technology scope, geography, period, evidence cutoff, and analyst. Use `--template v8`, `v11`, or `v12`; V12 is the default.

## Quality gates

Before delivery, verify:

- all decision-relevant claims have an adjacent citation or evidence identifier;
- links resolve to the intended global source and no domestic-only links remain;
- patent counts disclose unit and deduplication;
- market numbers disclose basis and units;
- calculations reconcile across the executive summary and detailed sections;
- facts, estimates, assumptions, and recommendations are visually distinct;
- legal language does not overstate infringement, validity, or FTO;
- dates use unambiguous formats and the report shows a cutoff date;
- tables have headers, interactive controls are keyboard accessible, and print output is legible;
- the HTML has no external runtime dependency and contains no credentials or private data.

## Output language and style

Use concise international business English and domain-standard terminology. Prefer neutral labels such as `focal organization`, `evidence cutoff`, `patent family`, `review status`, and `confidence`. Define specialized acronyms at first use. Use a restrained scientific/editorial visual system: white and neutral surfaces, navy text, one blue accent, semantic colors used sparingly, tabular numerals, generous whitespace, and no decorative gradients.

## Limitations statement

Include a visible statement that the briefing reflects the reviewed evidence and cutoff date, may omit non-public activity, and does not constitute legal, investment, or commercial advice. Recommend qualified patent counsel for claim-level infringement, validity, or FTO analysis.
