# Deliverables

## Default

The default deliverable is a Markdown review package:

- `report.md`
- `novelty-note.md`

## Report Structure By Mode

### Screen Mode (6-8 pages equivalent)

1. Executive recommendation (proceed / proceed with conditions / hold)
2. Novelty boundary summary
3. Key risks and blockers
4. Missing materials and next steps

### Review Mode (10-14 pages equivalent)

1. Executive recommendation
2. Project scope and proposal-stated claims
3. Novelty and overlap judgment (with comparison table)
4. Feasibility and evidence sufficiency
5. Main risks and material gaps
6. Recommendation and conditions

### Innovation Mode (8-12 pages equivalent)

1. Executive summary of innovation assessment
2. Innovation-point-by-point analysis
3. Differentiation boundary table
4. Risks to innovation claims
5. Recommendation

### Assurance Mode (12-18 pages equivalent)

1. Executive recommendation with confidence level
2. Project scope and proposal coherence assessment
3. Novelty and overlap (with detailed comparison attachment)
4. Feasibility, evidence sufficiency, and technical decomposition
5. Scoring and rating logic (with explicit rubric)
6. Stage-gate matrix
7. Material gaps and data readiness
8. Counterevidence and weakening conditions

## Novelty Note

`novelty-note.md` should be a standalone attachment containing:

- Novelty-search scope (databases, time window, field scope)
- Main comparison objects
- Point-by-point overlap assessment
- Residual differentiators
- Search limitations and unsearched areas

For Chinese formal reports, name it `公开文献与专利预查新说明` or `查新与对标附件`.

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
