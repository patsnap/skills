# Full-Scope Metrics Prompt

## Task

Collect reproducible population-level counts for the accepted technology scope. Keep them strictly separate from the representative patent sample.

## Non-negotiable rule

Never use Top-K or returned-result samples as population statistics, denominators, trends, rankings, geographic distributions, status distributions, grant rates, concentration measures, or market indicators.

Use a metric only when the live tool provides:

- a verified aggregation covering the defined population; or
- a reproducible complete bucket plan with a source-reported count for every included bucket.

Otherwise set the metric to `Unavailable`, omit the chart, and explain the gap.

## Verified connector routing

Use Advanced Patent Search for query execution and count retrieval when its discovered tools expose documented count semantics. Use Patent Briefing or Global Core Patent Database only to verify representative patent records and status; do not infer aggregate status from samples. Use Deep Patent Mining for technical enrichment, not automatic population counts unless its live schema explicitly provides them.

Technology-landscape aliases mentioned in the source package are not verified current global marketplace tools. Do not call or cite undocumented aliases unless they are actually discovered in the runtime environment.

## Collection steps

### 1. Baseline population

Run the frozen final query and record:

- source-reported match count;
- date field and range;
- jurisdictions;
- document types;
- publication versus family basis;
- query version;
- connector and live tool;
- execution timestamp; and
- truncation or coverage warnings.

### 2. Time series

Use a complete verified aggregation when available. Otherwise execute one query per defined period with identical scope except for the date filter. Preserve failed buckets as missing, never as zero.

Do not calculate CAGR when:

- the first value is zero or missing;
- periods are incomplete or inconsistent;
- the interval is shorter than the stated formula requires; or
- recent publication lag makes the comparison misleading without adjustment.

### 3. Regional benchmark

Collect only regions material to the brief. Use the same query and count basis. Do not assume China is required. Label authority, priority-origin, inventor-origin, applicant-origin, and family coverage as different concepts.

### 4. Subfield counts

For each validated subfield, run its frozen query under the shared count basis. Record total and, when justified, period buckets. Disclose overlap; do not sum overlapping subfields into a total.

### 5. Applicant, geography, and legal status

Collect these distributions only if a live verified aggregation covers the defined population. If only Top-N rows are returned:

- retain the rows as a partial ranking;
- record the known denominator and remainder if provided;
- do not compute HHI from incomplete rows;
- compute CR3/CR5 only when numerator and denominator share the same population; and
- label coverage precisely.

Never replace a failed aggregation with frequencies from the representative sample.

### 6. Quality and influence metrics

Use citation, family, status, licensing, or legal-event metrics only with comparable age, jurisdiction, document-type, and coverage definitions. Patent influence is not product quality, technical feasibility, market adoption, or commercial success.

## Output schema

```json
{
  "metric_scope": {
    "query_version": "",
    "date_field": "application | publication | priority",
    "period": {"start": "", "end": ""},
    "jurisdictions": [],
    "document_types": [],
    "count_unit": "publication | application | simple_family | extended_family | INPADOC",
    "cutoff": "",
    "connector": "",
    "tool": ""
  },
  "total_count": {"value": null, "state": "available | partial | unavailable", "source_id": ""},
  "regional_counts": [
    {"region": "", "basis": "authority | priority_origin | other", "value": null, "state": "", "source_id": ""}
  ],
  "trend": {
    "source_mode": "verified_aggregation | complete_buckets | unavailable",
    "periods": [{"period": "", "count": null, "state": "complete | partial | failed", "source_id": ""}],
    "publication_lag_note": ""
  },
  "subfields": [
    {"id": "SF01", "total": null, "trend": [], "overlap_note": "", "source_ids": []}
  ],
  "applicants": {"state": "available | partial | unavailable", "rows": [], "coverage": "", "denominator": null},
  "geography": {"state": "available | partial | unavailable", "basis": "", "rows": [], "coverage": ""},
  "legal_status": {"state": "available | partial | unavailable", "taxonomy": "", "as_of": "", "rows": [], "coverage": ""},
  "influence": {"state": "available | partial | unavailable", "metrics": [], "comparability_note": ""},
  "collection_log": [],
  "limitations": []
}
```

## Failure rules

| Condition | Required action |
|---|---|
| Complete trend aggregation available | Use it and preserve its definitions |
| No trend aggregation, count tool available | Execute and log complete buckets |
| One or more buckets fail | Mark missing; do not draw a complete trend chart |
| Applicant aggregation unavailable | Omit applicant ranking/concentration chart |
| Geography aggregation unavailable | Omit geography chart |
| Status aggregation unavailable | Omit status and grant-rate chart |
| Representative sample available only | Use it only for examples and qualitative evidence |
| Count semantics unclear | Stop that metric and document the ambiguity |

## Quality checks

- Every displayed metric has a source ID.
- Every denominator matches its numerator scope.
- Complete and partial metrics are visibly distinct.
- Zero is not used for unavailable data.
- Recent-period publication lag is disclosed.
- No sample frequency appears in `full_scope_metrics`.
- The collection log can reproduce every count.
