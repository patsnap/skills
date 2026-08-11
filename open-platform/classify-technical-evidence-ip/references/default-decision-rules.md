# Default Decision Rules

Use these defaults unless the user edits or replaces them.

## Evidence and relevance

1. Require traceable evidence for every formal label.
2. Prefer the field that most directly expresses the core object, action, purpose, or effect.
3. Treat titles and keywords as weak evidence when richer text exists.
4. Do not label background discussion, optional lists, incidental mechanisms, or examples as core content without supporting context.
5. Search and MCP results recall candidates; they do not determine final labels.

## Granularity

1. Prefer the most specific supported label.
2. Use a parent label when child-level evidence is insufficient and parent labels are allowed.
3. Do not output parent and child together by default.
4. Preserve uncertainty rather than guessing a child label.

## Selection

1. Obey each dimension's single- or multi-select policy.
2. In multi-select dimensions, require independent evidence for each label.
3. Prefer the main object, main purpose, and key process over exhaustive tagging.
4. Do not convert a candidate label into a formal label without confirmation.

## Conflicts and abstention

1. Send mutually plausible adjacent labels to review when evidence cannot distinguish them.
2. Use `unclassified` when no formal label fits in closed mode.
3. Use `needs_review` for incomplete evidence, conflicting evidence, dirty paths, missing required dimensions, or unresolved granularity.
4. Never force a label merely to improve coverage.

## Review routing

1. Do not send every `unclassified` result to record review.
2. Send a record to manual review only when a human decision can change its current outcome: scope boundary, unresolved adjacent labels, conflicting or incomplete evidence, dirty paths, missing required dimensions, or low confidence.
3. Send complete-evidence taxonomy gaps, missing leaf granularity, and uncovered concepts to `Taxonomy Backlog`; keep the record's closed-mode result unchanged.
4. Group repeated taxonomy gaps by issue type and list all affected records instead of creating duplicate review tasks.
5. Treat `not_applicable` as an automatic pass when the dimension is optional and evidence shows that the dimension is genuinely absent.
6. Allow a clear, output-eligible formal parent label without record review; log the missing child granularity in `Taxonomy Backlog` when relevant.
7. Turn user-confirmed recurring boundary decisions into versioned rules and apply them automatically to later records.

## Confidence

- `high`: direct core evidence, definition match, no material conflict.
- `medium`: reasonable support with a manageable ambiguity.
- `low`: incomplete evidence, weak field, or unresolved adjacent labels.

Low confidence defaults to manual review. Confidence is categorical, not a fabricated probability.

## Default configurable values

- Parent-child coexistence: false.
- Candidate labels: true in discovery and semi-open; false in closed.
- Evidence required: true.
- Low confidence action: manual review.
- Missing required dimension: flag; do not guess.
- New formal labels during full run: false.
- Unclassified action: taxonomy backlog unless a human decision can change the current record outcome.
- Not-applicable action: auto-pass when the dimension is optional and evidence is complete.
- Formal parent action: auto-pass when the parent is output-eligible and directly supported.
- Review deduplication: group by issue type and affected-record set.
