# Evidence to Factor Mapping

Convert evidence text into factor hypotheses with local traceability.

## Required Factor Fields
- `factor_id`
- `name`
- `type`
- `unit`
- `suggested_range`
- `confidence`
- `evidence_links[]`
- `coverage`
- `fact_or_inference`

## Required Evidence Link Fields
- `source_id`
- `quote_or_paraphrase`
- `condition`
- `result`
- `confidence`
- `fact_or_inference`

## Mapping Workflow
1. Detect canonical factors using strict pattern matching.
2. For each detected factor, extract numeric range from a local text window around the match.
3. Normalize unit per factor.
4. Build one evidence link per matched occurrence.
5. Compute confidence from relevance + significance + condition/result completeness.
6. Mark factor as `fact` only when patent + paper support both exist.

## Guardrails
- Do not use highly ambiguous aliases (for example bare `do`).
- Do not reuse one global range for all factors in the same sentence.
- Keep every recommendation traceable to `source_id`.
