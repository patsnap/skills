# Quality Check Report Template

# {{TOPIC}} — Report Quality Check

**Audit time:** {{AUDIT_TIME}}  
**Reviewer:** {{REVIEWER}}  
**Search version:** {{SEARCH_VERSION}}  
**Decision cutoff:** {{CUTOFF_DATE}}

## 1. Artifact inventory

| Artifact | Exists | Bytes | Parse/result | Notes |
|---|---|---:|---|---|
| `index.html` | {{INDEX_EXISTS}} | {{INDEX_BYTES}} | {{INDEX_PARSE}} | Main assessment |
| `patents.html` | {{PATENTS_EXISTS}} | {{PATENTS_BYTES}} | {{PATENTS_PARSE}} | Representative sample |
| `evidence.html` | {{EVIDENCE_EXISTS}} | {{EVIDENCE_BYTES}} | {{EVIDENCE_PARSE}} | Evidence register |
| `subfields.html` | {{SUBFIELDS_EXISTS}} | {{SUBFIELDS_BYTES}} | {{SUBFIELDS_PARSE}} | Subfield analysis |
| `methodology.html` | {{METHODOLOGY_EXISTS}} | {{METHODOLOGY_BYTES}} | {{METHODOLOGY_PARSE}} | Methods and limitations |
| `intermediate_data.json` | {{JSON_EXISTS}} | {{JSON_BYTES}} | {{JSON_PARSE}} | Structured data |
| `patent_list.csv` | {{PATENT_CSV_EXISTS}} | {{PATENT_CSV_BYTES}} | {{PATENT_CSV_PARSE}} | Sample records |
| `evidence_mapping.csv` | {{EVIDENCE_CSV_EXISTS}} | {{EVIDENCE_CSV_BYTES}} | {{EVIDENCE_CSV_PARSE}} | Claim mapping |
| `README.md` | {{README_EXISTS}} | {{README_BYTES}} | {{README_RESULT}} | User documentation |
| `quality_check.md` | {{QA_EXISTS}} | {{QA_BYTES}} | {{QA_RESULT}} | This audit |

## 2. Data lineage

| Gate | State | Evidence/notes |
|---|---|---|
| Full-scope metric definition complete | {{METRIC_SCOPE_STATE}} | {{METRIC_SCOPE_NOTE}} |
| Query version and tool recorded | {{QUERY_PROVENANCE_STATE}} | {{QUERY_PROVENANCE_NOTE}} |
| Period/subfield buckets complete | {{BUCKET_STATE}} | {{BUCKET_NOTE}} |
| Missing buckets not encoded as zero | {{MISSING_BUCKET_STATE}} | {{MISSING_BUCKET_NOTE}} |
| Publication lag disclosed | {{LAG_STATE}} | {{LAG_NOTE}} |
| Partial aggregations labeled | {{PARTIAL_STATE}} | {{PARTIAL_NOTE}} |

## 3. Representative sample boundary

| Gate | State | Evidence/notes |
|---|---|---|
| Sample warning visible | {{SAMPLE_WARNING_STATE}} | {{SAMPLE_WARNING_NOTE}} |
| Selection and reviewed counts documented | {{SAMPLE_METHOD_STATE}} | {{SAMPLE_METHOD_NOTE}} |
| Sample excluded from population trends | {{NO_SAMPLE_TREND_STATE}} | {{NO_SAMPLE_TREND_NOTE}} |
| Sample excluded from population distributions | {{NO_SAMPLE_DISTRIBUTION_STATE}} | {{NO_SAMPLE_DISTRIBUTION_NOTE}} |

## 4. HTML, accessibility, and security

| Gate | State | Evidence/notes |
|---|---|---|
| UTF-8 and valid structure | {{HTML_STRUCTURE_STATE}} | {{HTML_STRUCTURE_NOTE}} |
| Shared navigation resolves | {{NAV_STATE}} | {{NAV_NOTE}} |
| Responsive and printable | {{RESPONSIVE_STATE}} | {{RESPONSIVE_NOTE}} |
| Charts have complete data and table equivalents | {{CHART_STATE}} | {{CHART_NOTE}} |
| No placeholders or empty components | {{PLACEHOLDER_STATE}} | {{PLACEHOLDER_NOTE}} |
| External data escaped | {{ESCAPE_STATE}} | {{ESCAPE_NOTE}} |
| Unsafe URLs rejected | {{URL_STATE}} | {{URL_NOTE}} |
| No remote dependency or tracker | {{OFFLINE_STATE}} | {{OFFLINE_NOTE}} |
| No secrets or local paths | {{SECRET_STATE}} | {{SECRET_NOTE}} |

## 5. Cross-artifact reconciliation

| Gate | State | Evidence/notes |
|---|---|---|
| KPI values match JSON | {{KPI_STATE}} | {{KPI_NOTE}} |
| Charts/tables match JSON | {{SERIES_STATE}} | {{SERIES_NOTE}} |
| Patent IDs reconcile with CSV/JSON | {{PATENT_ID_STATE}} | {{PATENT_ID_NOTE}} |
| Claim/source IDs resolve | {{CLAIM_ID_STATE}} | {{CLAIM_ID_NOTE}} |
| Scores, weights, and sensitivity reconcile | {{SCORE_STATE}} | {{SCORE_NOTE}} |
| Recommendation and limitations match | {{RECOMMENDATION_STATE}} | {{RECOMMENDATION_NOTE}} |

## 6. Analytical integrity

| Gate | State | Evidence/notes |
|---|---|---|
| Count unit and family rule explicit | {{COUNT_STATE}} | {{COUNT_NOTE}} |
| CAGR and period math correct | {{CAGR_STATE}} | {{CAGR_NOTE}} |
| Applicant concentration denominator valid | {{CONCENTRATION_STATE}} | {{CONCENTRATION_NOTE}} |
| Subfield overlap disclosed | {{OVERLAP_STATE}} | {{OVERLAP_NOTE}} |
| Candidate opportunities sensitivity-tested | {{OPPORTUNITY_STATE}} | {{OPPORTUNITY_NOTE}} |
| Patent and commercialization evidence separated | {{COMMERCIAL_STATE}} | {{COMMERCIAL_NOTE}} |

## 7. Forbidden artifact check

| Check | State |
|---|---|
| No `.py` file | {{NO_PY_STATE}} |
| No `scripts/` directory | {{NO_SCRIPTS_STATE}} |
| No cache or temporary file | {{NO_CACHE_STATE}} |
| No fabricated patent/metric | {{NO_FABRICATION_STATE}} |
| No Top-K population statistic | {{NO_SAMPLE_STAT_STATE}} |

## 8. Known limitations

{{LIMITATIONS_CONTENT}}

## 9. Release blockers

{{RELEASE_BLOCKERS}}

## 10. Audit decision

**Decision:** {{AUDIT_DECISION}}

Allowed values:

- `Pass`;
- `Pass with disclosed limitations`; or
- `Fail — repair required`.

**Basis:** {{AUDIT_BASIS}}
