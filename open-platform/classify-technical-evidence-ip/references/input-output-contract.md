# Input and Output Contract

## Minimum user input

- Source records or text.
- Business purpose for the labels.

If the purpose is unclear, stop and ask. Do not manufacture a business objective.

## Optional assets

- Taxonomy, definitions, rules, examples, correction history, field preferences, output preferences, and evidence restrictions.

## Auto-detect

- File and sheet types, record identifier, title/abstract/claims/body fields, existing label columns, label paths, definitions, row count, blanks, duplicates, and dirty labels.

Generate a task configuration and ask the user to confirm the inferred mapping.

## Taxonomy fields

`label_id`, `dimension`, `label_name`, `label_path`, `parent_label_id`, `definition`, `include_when`, `exclude_when`, `synonyms`, `confusable_labels`, `positive_example`, `negative_example`, `status`, `taxonomy_version`

## Label result fields

Preserve all original fields and add:

`record_id`, dimension label columns, `candidate_labels`, `label_status`, `evidence_field`, `evidence_excerpt`, `reason`, `confidence`, `needs_review`, `review_reason`, `taxonomy_version`, `rules_version`, `mcp_enrichment_status`

## Evidence long table

One row per record-label judgment:

`record_id`, `dimension`, `label_id`, `label_path`, `label_status`, `evidence_field`, `evidence_excerpt`, `reason`, `confidence`, `needs_review`, `review_reason`, `source_type`, `source_identifier`

## Workbook sheets

1. `Source Data`
2. `Labeling Results`
3. `Evidence`
4. `Review Queue`
5. `Taxonomy Backlog`
6. `Taxonomy`
7. `Decision Rules`
8. `QA Summary`
9. `Task Info`
10. `MCP Provenance`

`Review Queue` contains only record-level decisions that may change current labels.

`Taxonomy Backlog` fields:

`gap_id`, `gap_type`, `affected_records`, `current_handling`, `proposed_taxonomy_or_rule_change`, `priority`, `record_review_required`

## Provenance fields

`timestamp`, `stage`, `service`, `tool`, `purpose`, `query_summary`, `record_or_label_id`, `returned_identifiers`, `status`, `notes`

Do not store credentials, authorization headers, or raw credential-bearing URLs.
