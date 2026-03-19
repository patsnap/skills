# Output Contract

All outputs below are required.

## `evidence_catalog.json`
Top-level fields:
- `objective`
- `responses`
- `constraints`
- `sources[]`
- `coverage`

Each `sources[]` entry must include:
- `source_id` (`PAT-*`, `PAP-*`, `WEB-*`)
- `source_type` (`patent|paper|web`)
- `title`
- `year`
- `url_or_id`
- `relevance_score`
- `fetch` object:
  - `status`
  - `attempts`
  - `path`
  - `error`
- `read` object:
  - `status`
  - `method`
  - `condition`
  - `result`
  - `boundary`
  - `significance`
  - `excerpt`

## `factor_hypotheses.json`
Top-level fields:
- `factors[]`
- `summary`

Each factor must include:
- `factor_id`
- `name`
- `type`
- `unit`
- `suggested_range`
- `mechanism_hypothesis`
- `risk_note`
- `confidence`
- `evidence_links[]`
- `coverage`
- `high_priority`
- `fact_or_inference`

Each `evidence_links[]` entry must include:
- `source_id`
- `quote_or_paraphrase`
- `condition`
- `result`
- `confidence`
- `fact_or_inference`

## `doe_design.json`
Top-level fields:
- `design_type`
- `selection_rationale`
- `selected_factors[]`
- `runs[]`
- `analysis_plan[]`
- `next_round_rules[]`
- `diagnostics`

`selection_rationale` must include:
- `phase`
- `factor_count`
- `resource_budget`
- `why_this_design`

`runs[]` must include:
- `run_order`
- `run_id`
- `replicate`
- `levels_actual`
- `levels_coded`

## `run_sheet.csv`
Header must include:
- `run_order`, `run_id`, `replicate`
- per-factor `_actual` columns
- per-factor `_coded` columns

## `doe_plan.md`
Must include these sections exactly:
1. Objective and Constraints
2. Selected DOE Method and Rationale
3. Run Sheet Summary
4. Evidence Coverage Matrix
5. Facts vs Inference vs Unknowns
6. Next-round Criteria
