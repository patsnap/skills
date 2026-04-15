# Deliverables

## Default

The default deliverable is a structured Markdown report:

- `report.md`

Recommended sections:

1. Executive summary
2. Scope and candidate-pool definition
3. Final player set and tiering logic
4. Route differentiation and geography split
5. Optional white-space observations
6. Key evidence references

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
