# Quality and Review

## Taxonomy health

Check unique IDs, valid parent links, no cycles, unique formal paths, complete definitions, consistent dimensions, candidate/formal separation, obsolete paths, example coverage, adjacent-label ambiguity, and severe imbalance.

## Pilot coverage

Include common cases, rare cases, hard negatives, adjacent-label conflicts, incomplete text, multi-label cases, and likely unclassified cases. Expand the pilot when new error types continue to appear.

## Error diagnosis

Classify each issue as:

- taxonomy gap
- unclear definition
- missing or conflicting rule
- poor sample coverage
- missing evidence
- source data defect
- model judgment error

Propose a correction and affected-record scope. Do not silently change frozen artifacts.

## Review triggers

- low confidence
- candidate result that requires promotion, rejection, merge, or split
- missing required dimension
- multiple plausible adjacent labels
- conflicting evidence
- weak-only evidence
- dirty or unknown label path
- incomplete or truncated text
- taxonomy/rule version mismatch
- MCP enrichment requested but unavailable

An `unclassified` result alone is not a record-review trigger. If evidence is complete and no current formal label fits, keep the record result and route the coverage issue to `Taxonomy Backlog`. Likewise, do not review an optional `not_applicable` dimension merely because it is blank.

## Review routing

Use two separate queues:

- `Review Queue`: record-level decisions that may change current labels.
- `Taxonomy Backlog`: grouped taxonomy gaps, missing leaf granularity, uncovered functions, and recurring rule opportunities.

For each backlog issue, record `gap_id`, `gap_type`, `affected_records`, `current_handling`, `proposed_taxonomy_or_rule_change`, `priority`, and `record_review_required`. Deduplicate repeated gaps and ask the user once per governance issue.

## Output checks

Report total records, labeled coverage, unclassified rate, record-review rate, taxonomy-backlog count, candidate count, missing-evidence count, illegal-label count, missing-required-dimension count, duplicates, dropped source records, label distributions, and version consistency. Never combine taxonomy-backlog items into the record-review rate.

Before delivery, verify that every source record is preserved exactly once unless the user explicitly defined another scope.
