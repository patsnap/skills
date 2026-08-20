---
copyright: "Copyright © Patsnap. All rights reserved."
name: monitor-competitor-patent-landscape-ip
description: Analyze one competitor’s patent portfolio architecture in a defined technology, including public technical context, entity-resolved patent retrieval, representative-family selection, claim and specification review, core-versus-peripheral protection hypotheses, technical-density mapping, product-feature visualization, geographic filing behavior, and evidence-backed R&D actions. Use for competitor patent monitoring and strategy reports in HTML or PDF; do not use as a substitute for infringement or freedom-to-operate analysis.
---

# Monitor a competitor patent landscape

## Users and purpose

Support corporate IP teams, R&D engineers, product leaders, and strategy analysts.

Explain how one competitor appears to structure patent protection around a technology.

Identify technical concentration, portfolio layers, geographic behavior, representative patents, and research priorities.

Do not state that a low-density area is legally clear.

Do not provide an infringement conclusion.

## Required resources

Read [references/workflow_guide.md](references/workflow_guide.md) before starting.

Use `scripts/generate_report.py` to render validated analysis JSON.

Use `scripts/main.py` only as the source-preserved readiness entry point.

The source refers to a README, but no README is present in the frozen package.

Do not create or depend on that missing file.

## Inputs

| Input | Required | Description |
|---|---|---|
| Competitor | Yes | Brand plus verified legal applicants and assignees |
| Technology | Yes | Defined technical scope, inclusions, exclusions, and synonyms |
| Patsnap query | No | Preserve and review if supplied; otherwise construct transparently |
| Target jurisdictions | No | User-selected offices or territories; do not force a global default |
| Product example | No | Used only for an evidence-based, properly sourced product map |
| Top N | No | Default 10; record the selected value |
| Time window | No | Use a stated rolling period and ISO cut-off date |
| Counting unit | No | Publication, application, simple family, or another declared unit |

Also collect the business question, intended audience, date basis, evidence cut-off, and confidentiality constraints.

## Patsnap MCP

### Required: Advanced Patent Search

Official page: https://open.patsnap.com/marketplace/mcp-servers/patent-search

Verified 2026-08-07.

Configuration key: `advanced_patent_search`.

Transport: `streamableHttp`.

Current Connect-panel URL pattern:

`https://open.patsnap.com/marketplace/mcp-servers/patent-search`

Use documented assignee, nested-query, semantic, count, field, number, keyword, similarity, and image tools as appropriate.

Copy the current URL from the official page and keep the real API key secret.

### Recommended: Patent Briefing

Official page: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

Verified 2026-08-07.

Configuration key: `patent_briefing`.

Transport: `streamableHttp`.

Current Connect-panel URL pattern:

`https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`

Use `family`, `bibliography`, `legal_status`, `claims`, `claim_translated`, `description`, `description_translated`, `intelligent_image`, and `tech_summary` as needed.

Do not call the stale source names `patent.search` or `patent.fetch` as though they were verified current tools.

If live MCP is unavailable, provide a search plan and empty report structure labeled `not executed`.

Never fabricate records or metrics.

## Workflow

### Step 1: Build the technical framework

Search current public material on the competitor’s disclosed research focus, product architecture, and technology routes.

Prefer primary and authoritative sources.

Define three to six subareas only when supported.

Record sources, dates, uncertainty, inclusions, and exclusions.

Treat the framework as provisional until validated against patents.

### Step 2: Resolve entities and retrieve patents

Resolve brands to legal entities, subsidiaries, former names, acquisitions, transliterations, and native-script names.

Keep original applicant and current assignee scopes distinct.

Use the user’s query when valid, documenting any revision.

Otherwise combine verified assignees with keywords, classifications, date filters, jurisdictions, and semantic expansion.

Use 100 records only as an exploratory cap.

Preserve total-count context.

Record exact queries, arguments, time, tools, and returned identifiers.

### Step 3: Select representative patents

The source files conflict between simple-family thresholds of three and five.

Resolve this by making the threshold configurable and recording it.

Treat family size as one screening signal, not the definition of importance.

Balance technical relevance, independent-claim substance, family breadth, status, recency, continuity, citation context, and portfolio relationships.

Use Top N = 10 unless the user selects another value.

State why each patent was selected.

### Step 4: Review technical content

Use abstracts for orientation.

Read independent claims before characterizing scope.

Read relevant dependent claims and specification passages.

Check original-language text where translated wording is material.

Map each record to one or more technical subareas.

Classify its portfolio role as `Core hypothesis`, `Peripheral hypothesis`, or `Unclassified`.

Attach evidence and confidence.

Do not infer legal claim breadth from word count.

### Step 5: Analyze technical activity

Calculate subarea counts under the selected counting unit.

Analyze simple-family distributions.

Identify relative observed density.

Use `High observed density`, `Moderate observed density`, and `Low observed density` with numeric values.

Do not use density as proof of blocking rights or white space.

Test entity coverage, language, classification, jurisdiction, and sample bias.

### Step 6: Map patents to product features

Use a product SVG only when it improves the decision.

Use user-provided, licensed, or original schematic material.

Do not automatically copy a product photograph.

Record provenance.

Map subareas and verified publication numbers to product regions.

Provide an accessible text description and legend.

### Step 7: Analyze geographic behavior

Compare filing jurisdictions and family routes.

Distinguish office, publication authority, PCT route, regional filing, national phase, and commercial market.

Report grant and legal-status data separately from filing counts.

Do not treat a WO publication as a worldwide enforceable patent.

### Step 8: Synthesize strategy

Address:

- Technical architecture and concentration.
- Geographic filing behavior.
- Core and peripheral portfolio hypotheses.
- Continuation or generational patterns where verified.
- Multiple-applicant structures where verified.
- R&D research priorities.
- Areas requiring FTO or design-around work under separate workflows.

Connect every material conclusion to a patent number and source.

Label quantities that cannot be verified as `Unverified`.

### Step 9: Generate HTML or PDF

Prepare `analysis.json` according to the complete contract in the workflow guide.

Run:

```bash
python scripts/generate_report.py --data-path analysis.json --output-path competitor-landscape.pdf
```

The renderer escapes all JSON-derived content.

It attempts PDF through WeasyPrint.

If conversion fails, it writes an HTML fallback and reports the actual path.

Do not claim a PDF was generated when only HTML exists.

## Report modules

Include:

1. Report metadata and coverage warning.
2. Executive summary.
3. Technical framework.
4. Filing-jurisdiction distribution.
5. Representative patent table.
6. Core and peripheral hypotheses.
7. Technical-subarea activity table.
8. Product-feature mapping and provenance.
9. R&D and IP actions.
10. Sources, methodology, and limitations.

## Scientific visual standard

Use a white background, charcoal text, a restrained blue accent, and neutral rules.

Use English system fonts.

Do not use gradients, emoji, decorative dashboard cards, pill badges, or color-only heatmaps.

Keep density understandable through text labels and counts.

Use semantic HTML, captions, stated units, denominators, retrieval dates, and source notes.

Make tables horizontally usable on narrow screens.

Add print CSS for PDF conversion.

## Quality gate

- Verify every patent number and Patsnap link.
- Retrieve family membership; do not estimate it.
- State the family definition, counting unit, and date basis.
- State the result cap and sample limitation.
- Explain every representative-patent selection.
- Support core/peripheral hypotheses with claims and portfolio context.
- Treat citations as context, not value.
- Treat low density as a validation lead, not clearance.
- Warn when fewer than ten records are retrieved.
- Escape all report data.
- Verify product-image or SVG provenance.
- Keep visual states meaningful without color.
- Test HTML and actual output paths.
- Preserve the non-legal-opinion boundary.

## Final response

Lead with the main portfolio-architecture finding.

State competitor, technology, jurisdictions, time window, counting unit, and sample status.

State the strongest uncertainty.

Link the actual HTML or PDF output.

Recommend a separate FTO review when the decision requires legal clearance.
