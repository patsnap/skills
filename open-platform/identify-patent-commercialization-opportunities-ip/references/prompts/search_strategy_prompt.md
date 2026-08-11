# Search Strategy Prompt

## Task

Develop, test, and version a reproducible patent search for the accepted technology scope. Optimize recall and precision using the live connector schema rather than assuming one query syntax.

## Inputs

- normalized topic and original request;
- concept groups, synonyms, translations, and exclusions;
- candidate IPC/CPC or other classifications;
- technical and application boundaries;
- target jurisdictions and business context;
- date field and range;
- family-counting rule; and
- prior search versions and validation patents, if any.

## Strategy construction

### Concept blocks

Create blocks for:

1. core mechanism or technical effect;
2. material, device, component, or architecture;
3. process or method;
4. application context;
5. classifications; and
6. exclusions and false-positive controls.

Use `OR` within a concept and `AND` across essential concepts. Preserve spelling variants, acronyms, chemical names, transliterations, and jurisdiction-language terms when material.

### Search routes

Use a combination of routes when supported:

- fielded keyword or nested query;
- classification-led retrieval;
- semantic retrieval;
- citation expansion;
- similar-patent expansion;
- assignee or inventor validation; and
- targeted number or family verification.

Do not present an Analytics-style query as executable until it has been tested against the live tool schema.

### Validation loop

1. Run a broad pilot query.
2. Inspect a documented sample across relevance ranks.
3. Identify false-positive and false-negative concepts.
4. Test known relevant patents when available.
5. Refine inclusions, exclusions, fields, and classifications.
6. Record every version and the reason for change.
7. Freeze the final query before generating full-period or subfield counts.

Do not use rigid universal thresholds such as fewer than 100 or more than 50,000 results. Adjust only when the result set is unsuitable for the stated decision and document why.

## Time-series and comparison plan

If a verified aggregation tool returns a complete series with defined semantics, record it directly. Otherwise plan reproducible buckets using the same frozen query:

- one period per bucket;
- one consistent date field;
- one consistent jurisdiction and document/family scope;
- source-reported count for each bucket;
- explicit failed or partial buckets; and
- publication-lag treatment for recent periods.

Use annual buckets only when annual resolution is decision-relevant. Choose a defensible start year rather than hard-coding 2015.

## Subfield plan

For each of four to eight candidate subfields:

- define the subfield and exclusions;
- create an independently testable query;
- document overlap with other subfields;
- decide whether counts are mutually exclusive or intentionally overlapping;
- validate representative records; and
- use identical date, jurisdiction, and family rules where comparison is intended.

## Output schema

```json
{
  "strategy_version": "v1.0",
  "topic": "",
  "connector": "advanced_patent_search",
  "live_tool_names": [],
  "primary_query": {"syntax": "", "fields": [], "filters": {}},
  "concept_blocks": {
    "core_mechanism": [],
    "material_component_architecture": [],
    "process_method": [],
    "application": [],
    "classifications": [],
    "exclusions": []
  },
  "search_routes": [],
  "geographic_scope": [],
  "time_scope": {"start": "", "end": "", "date_field": ""},
  "family_counting_rule": "",
  "document_types": [],
  "validation": {
    "known_relevant": [],
    "known_irrelevant": [],
    "sample_reviewed": 0,
    "precision_notes": "",
    "recall_notes": ""
  },
  "bucket_plan": {
    "enabled": false,
    "periods": [],
    "query_template": "",
    "count_semantics": ""
  },
  "subfield_queries": [
    {"id": "SF01", "name": "", "definition": "", "query": {}, "overlap_note": ""}
  ],
  "version_history": [{"version": "", "date": "", "change": "", "reason": ""}],
  "limitations": []
}
```

## Quality checks

- The query has been executed, not merely drafted.
- Every classification is verified and relevant.
- The same frozen query underlies comparable buckets.
- Count semantics are explicit.
- Family and publication counts are not mixed.
- Subfield overlap is disclosed.
- Recent-period lag is planned.
- Search scope and version are saved to `intermediate_data.json`.
