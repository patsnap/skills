# Deliverables

## Default

The default deliverable is a structured Markdown report:

- `report.md`
- `comparison_basis.md`

## Report Structure By Mode

### Overview Mode

1. Executive summary: topic landscape and main route families
2. Route taxonomy and definitions
3. Per-route profile cards
4. Frontier signals and emerging directions
5. Key evidence references

### Compare Mode

1. Executive summary: which route is recommended and why
2. Scope and comparison basis (explicit)
3. Route-by-route profile cards
4. Comparison matrix (routes × dimensions, with evidence per cell)
5. Recommendation with conditions, tradeoffs, and update triggers
6. Counterevidence and weakening conditions
7. Key evidence references

### Maturity Mode

1. Executive summary: maturity landscape and readiness gaps
2. Scope and maturity rubric (explicit level definitions)
3. Per-route maturity assessment with evidence
4. Maturity comparison matrix
5. Stage-gate or readiness roadmap
6. Risks and deployment blockers
7. Key evidence references

### Opportunity Mode

1. Executive summary: where the opportunities are
2. Route landscape and current coverage
3. Gap analysis (sparse coverage + technical value + entry path)
4. Emerging routes and early signals
5. Recommended investigation priorities
6. Key evidence references

## Comparison Matrix Format

Routes (rows) × dimensions (columns). Each cell should contain:
- Assessment level (e.g., High / Moderate / Low, or TRL level)
- Brief evidence note with source citation

## Optional Formal Export

If the host environment supports rendering, optional exports are:

- `deliverables/report.docx`
- `deliverables/report.pdf`

Suggested render paths:

- `pandoc` from Markdown to `docx` and `pdf`
- `python-docx` for custom Word formatting
- `reportlab` or another Markdown-to-PDF tool for `pdf`

These renderers are optional. The skill is still complete when the Markdown and
evidence files are strong.
