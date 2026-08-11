# Trend Analysis Prompt

## Task

Interpret the complete, scope-consistent period counts in `full_scope_metrics.trend`. Do not infer a population trend from the representative sample.

## Inputs

- period/count/state/source records;
- query and strategy version;
- date field;
- jurisdiction and document scope;
- family/counting unit;
- cutoff and publication-lag assessment;
- relevant regional benchmark series; and
- missing or failed buckets.

## Pre-analysis gate

Do not generate a continuous trend chart or CAGR when:

- any required bucket is failed or semantically inconsistent;
- query versions changed without a bridge analysis;
- count units differ;
- the first value is zero or missing;
- the selected periods are not equally spaced; or
- recent-period truncation dominates the comparison.

Show the available observations and limitations instead.

## Calculations

### Overall change

For comparable start and end periods:

`overall_change = (end_count - start_count) / start_count`

State the periods and do not annualize this value.

### Compound annual growth rate

For `n` elapsed years:

`CAGR = (end_count / start_count)^(1 / n) - 1`

State the exact endpoints, elapsed interval, and whether either endpoint is affected by publication lag.

### Recent activity

Compare a complete recent window with a complete earlier benchmark. Do not compare an incomplete current year with full prior years.

### Inflection points

Identify a peak, acceleration, or decline only when the change exceeds expected noise and is supported by at least adjacent complete periods. Treat causal explanations as hypotheses requiring external evidence.

## Stage interpretation

Use descriptive states such as:

- emerging;
- expanding;
- high-volume stable;
- volatile;
- contracting on observed complete periods; or
- not assessable.

Do not use universal filing thresholds or fixed CAGR cutoffs as objective maturity rules. Explain the observed pattern, comparison base, uncertainty, and alternative interpretations.

## Regional comparison

Compare only decision-relevant regional series that share query, period, date field, document type, and count unit. Do not call a patent authority or priority-origin share a market share or technology-source share.

## Output schema

```json
{
  "trend_analysis": {
    "state": "available | partial | unavailable",
    "scope": {
      "query_version": "",
      "period": {},
      "date_field": "",
      "jurisdictions": [],
      "count_unit": "",
      "cutoff": ""
    },
    "series": [{"period": "", "count": null, "state": "", "source_id": ""}],
    "overall_change": {"value": null, "start": "", "end": "", "state": "calculated | unavailable"},
    "cagr": {"value": null, "start": "", "end": "", "elapsed_years": null, "state": "calculated | unavailable"},
    "recent_activity": {"state": "higher | similar | lower | unavailable", "window": "", "benchmark": "", "reason": ""},
    "descriptive_stage": "emerging | expanding | high_volume_stable | volatile | contracting_observed | not_assessable",
    "stage_evidence": "",
    "inflections": [{"period": "", "type": "acceleration | peak | slowdown | decline", "evidence": "", "source_ids": []}],
    "regional_comparisons": [{"region": "", "share": null, "basis": "", "interpretation": "", "source_ids": []}],
    "publication_lag": {"affected_periods": [], "note": ""},
    "observations": [],
    "hypotheses": [],
    "limitations": []
  }
}
```

## Evidence rules

- Every number must trace to full-scope metrics.
- Every statement needs a claim ID and source IDs.
- Separate observation from causal hypothesis.
- Never say a technology is commercially mature based on filings alone.
- Never say a region leads the market based on patent counts alone.
- Do not hide missing buckets or recent publication lag.

## Quality checks

- CAGR formula and elapsed years are correct.
- Start and end periods are complete and nonzero.
- Current-year counts are not treated as complete without evidence.
- Regional series use identical count semantics.
- No Top-K sample field is used.
- Chart periods and narrative periods match.
- Inflection claims identify evidence and uncertainty.
