# Deliverables

## Default

The default deliverable is a structured Markdown report:

- `report.md`

Recommended sections:

1. Executive summary
2. Company-topic scope and boundary
3. Route profile and technical focus
4. Evidence-backed strengths and limits
5. Implications for the user's decision
6. Key evidence references

## Optional Formal Export

If the host environment supports rendering, optional exports are:

- `deliverables/report.docx`
- `deliverables/report.pdf`

Suggested render paths:

- `pandoc` from Markdown to `docx` and `pdf`
- `python-docx` when a custom Word layout is needed
- `reportlab` or Markdown-to-PDF tooling when direct `pdf` output is preferred

These renderers are optional. The skill should still be considered complete when
the Markdown is high quality and the evidence files are intact.
