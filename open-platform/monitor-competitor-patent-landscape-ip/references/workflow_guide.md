# Competitor patent landscape workflow guide

## Contents

1. Define scope and technical framework
2. Resolve entities and search patents
3. Identify representative patents
4. Review claims and map technology
5. Analyze the portfolio architecture
6. Generate and validate the report
7. `analysis.json` contract
8. Quality and failure rules

## Overview

Use this workflow to examine one competitor’s patent activity in a defined technology.

Support IP, R&D, product, and strategy decisions with traceable evidence.

Do not treat the result as a freedom-to-operate opinion.

Do not infer patent importance from family size, citation count, or claim length alone.

## Step 1: Define scope and technical framework

Use current public sources to identify the competitor’s disclosed research themes, product features, and technical routes.

Search combinations such as:

- `<competitor> <technology> research`
- `<competitor> <technology> product architecture`
- `<competitor> <technology> patent strategy`
- Relevant industry reports, standards, technical papers, and company materials

Use authoritative or primary sources where possible.

Record publication date, source, link, and access date.

Create three to six technical subareas only when the evidence supports that structure.

Possible dimensions include materials, manufacturing, system integration, safety, controls, applications, and serviceability.

Document inclusions, exclusions, synonyms, and adjacent areas.

Label the framework provisional until checked against retrieved patents.

## Step 2: Resolve entities and search patents

### Entity resolution

Resolve the competitor brand to legal applicants and assignees.

Consider parent companies, subsidiaries, former names, acquisitions, native-script names, and transliterations.

Record evidence for each included entity.

Separate original applicant and current assignee scopes.

### Required MCP

Use Advanced Patent Search:

https://open.patsnap.com/marketplace/mcp-servers/patent-search

Verified configuration key: `advanced_patent_search`.

Use the current Connect-panel URL and keep the API key secret.

Use documented assignee, nested-query, semantic, count, field, number, keyword, similarity, and image capabilities as appropriate.

### Search strategy

If the user provides a valid query, preserve it and document any changes.

Otherwise combine:

- Verified assignee entities.
- Technology keywords and synonyms.
- IPC/CPC classifications.
- Jurisdiction filters.
- Date filters.
- Semantic expansion.

Record:

- Exact query or structured arguments.
- Tool and retrieval mode.
- Target jurisdictions.
- Date field and range.
- Counting unit.
- Result cap.
- Retrieval timestamp.

Use 100 results only as an exploratory default cap.

Retrieve total counts separately where supported.

Do not call a top-k sample exhaustive.

## Step 3: Identify representative patents

Use Patent Briefing for candidate verification:

https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

Verified configuration key: `patent_briefing`.

Use `family`, `bibliography`, `legal_status`, `claims`, `claim_translated`, `description`, `description_translated`, `intelligent_image`, and `tech_summary` where needed.

The source packages used inconsistent family thresholds: at least three in one file and at least five in another.

Treat family size as a configurable screening signal.

Record the threshold selected for the run.

Do not label a patent “core” only because its simple family is large.

Use a multi-factor selection method:

1. Technical relevance.
2. Independent-claim or disclosure substance.
3. Family and geographic breadth.
4. Current legal-status context.
5. Recency and continuity.
6. Citation context.
7. Relationship to other filings in the portfolio.

Use Top N = 10 as the default in the localized skill.

Allow the user to select another value.

Record the chosen Top N and selection rationale.

## Step 4: Review claims and map technology

Read the abstract for orientation only.

Read independent claims before characterizing protection scope.

Read relevant dependent claims and specification passages where necessary.

Use translated text for discovery, but check original-language wording when interpretation matters.

Map each record to one or more technical subareas.

Use `Core hypothesis`, `Peripheral hypothesis`, or `Unclassified`.

Define a core hypothesis as evidence that the filing addresses a foundational architecture, process, or recurring platform concept.

Define a peripheral hypothesis as evidence that the filing addresses an application, refinement, option, supporting structure, or variant.

State the evidence and uncertainty.

Do not make a legal breadth determination without jurisdiction-specific claim analysis.

## Step 5: Analyze the portfolio architecture

Analyze:

| Dimension | Required interpretation |
|---|---|
| Technical subarea | Count and family-normalized distribution with classification confidence |
| Geography | Filing route and jurisdiction coverage, not assumed commercial market share |
| Time | Priority, filing, publication, or grant trend under a declared date basis |
| Density | Relative observed activity under a stated denominator, not legal blockage |
| Representative patents | Technical focus, family path, status, and selection reason |
| Peripheral activity | Applications, variants, supporting features, and continuity patterns |

Use `High observed density`, `Moderate observed density`, or `Low observed density`.

Display the numeric count and denominator with the label.

Do not call a low-density cell white space without broader validation.

## Product-feature visualization

Use an SVG schematic when the product mapping materially improves understanding.

Use a user-supplied image, licensed material, or an original schematic.

Record provenance.

Do not automatically copy a product photograph from the web.

Map technical subareas and representative publication numbers to clearly labeled regions.

Keep the diagram accessible with text descriptions and a legend.

## Step 6: Generate and validate the report

Use `scripts/generate_report.py`.

Write the analysis data to a JSON file following the contract below.

Run:

```bash
python scripts/generate_report.py --data-path analysis.json --output-path competitor-landscape.pdf
```

The script attempts PDF generation through WeasyPrint.

If PDF conversion is unavailable, it writes an HTML report beside the requested output.

Report the actual generated path.

Do not claim a PDF exists when the fallback produced HTML.

## `analysis.json` contract

```json
{
  "competitor": "Verified competitor display name",
  "technology": "Defined technology scope",
  "market_scope": ["US", "EP", "JP"],
  "total_patents": 85,
  "counting_unit": "simple_family",
  "date_basis": "publication",
  "date_from": "YYYY-MM-DD",
  "date_to": "YYYY-MM-DD",
  "retrieved_at": "YYYY-MM-DDTHH:MM:SSZ",
  "search_query": "Recorded query or structured-search summary",
  "sample_limit": 100,
  "exec_summary": "Evidence-backed executive summary",
  "tech_framework": [
    {"name": "Technical subarea", "description": "Definition and boundary"}
  ],
  "market_distribution": {
    "US": 25,
    "EP": 15,
    "JP": 5
  },
  "top_patents": [
    {
      "title": "Patent title",
      "publication_number": "Verified publication number",
      "patent_url": "https://analytics.patsnap.com/...",
      "family_size": 12,
      "legal_status": "Verified simple status",
      "status_date": "YYYY-MM-DD",
      "tech_sub_area": "Technical subarea",
      "layout_type": "Core hypothesis",
      "claim_summary": "Evidence-based independent-claim summary",
      "selection_reason": "Multi-factor selection rationale"
    }
  ],
  "core_analysis": "Core-architecture hypothesis and evidence",
  "periph_analysis": "Peripheral-architecture hypothesis and evidence",
  "sub_area_heatmap": [
    {
      "name": "Technical subarea",
      "count": 30,
      "core_count": 10,
      "periph_count": 20
    }
  ],
  "product_map": {
    "provenance": "User supplied, licensed, or original schematic",
    "description": "Accessible text description"
  },
  "suggestions": [
    "Evidence, uncertainty, proposed action, and owner"
  ],
  "sources": [
    {
      "label": "PatSnap patent data",
      "url": "https://open.patsnap.com/",
      "accessed": "YYYY-MM-DD"
    }
  ],
  "limitations": [
    "Sample, entity, jurisdiction, language, status, or data limitation"
  ]
}
```

## Output files

Primary requested output:

- `competitor_patent_landscape_<company>_<technology>.pdf`

Fallback output:

- `competitor_patent_landscape_<company>_<technology>.html`

Intermediate data:

- `analysis.json` only when the user requests or approves saving it.

Do not create a new bundled template or README inside the skill package.

## Quality and failure rules

- Verify every patent identifier and link.
- Retrieve simple-family membership; do not estimate it.
- State the family definition.
- State the date basis and counting unit.
- Label samples and result caps.
- Require evidence for core/peripheral hypotheses.
- Escape all JSON-derived text before HTML rendering.
- Include a low-data warning when fewer than ten records are retrieved.
- Treat the warning as a coverage limitation, not proof of opportunity.
- Ensure density labels remain understandable without color.
- Provide provenance and accessible text for every product diagram.
- Link every recommendation to supporting evidence.
- Label unverified quantities `Unverified`.
- Do not expose API keys or confidential inputs.
- Use qualified IP counsel for infringement, validity, or FTO conclusions.
