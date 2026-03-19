# QFD Workspace File Structure

Use this file to verify pipeline outputs and know which artifacts to read first.

## Core Layout

```text
<workspace>/
  project_meta.json
  01_voc/
    requirements.json
    cluster_diagnostics.json
    llm_merge_trace.json
  02_technical/
    our_product_spec.json
  03_analysis/
    relationship_matrix.json
    correlation_matrix.json
    conflicts.json
  04_benchmark/
    benchmark_table.json
    gap_analysis.json
  05_output/
    priority_recommendations.json
    qfd_report.md
    hoq_matrix.xlsx          # optional
```

## Read Order

1. `05_output/qfd_report.md`
2. `05_output/priority_recommendations.json`
3. `03_analysis/conflicts.json`
4. `04_benchmark/gap_analysis.json` when competitor specs were supplied

## Notes

- `cluster_diagnostics.json` and `llm_merge_trace.json` document VOC processing behavior.
- `benchmark_table.json` and `gap_analysis.json` are still written even when benchmark coverage is thin; inspect contents before describing competitor gaps.
- `hoq_matrix.xlsx` is optional and depends on `openpyxl`.
