# Workflow Modes

## Diagnostic decision

Use materials first, then ask only for missing business choices.

| Condition | Recommended mode |
|---|---|
| No usable taxonomy | `discovery` |
| Partial taxonomy or new labels allowed | `semi_open` |
| Frozen taxonomy and no new labels | `closed` |

The user confirms the recommendation. Never change mode silently.

## Discovery

1. Use the scope gate to confirm goal, unit, dimensions, mode, and candidate-label policy.
2. Select representative source records.
3. Execute keyword expansion, semantic search, classification assistance or focused retrieval, and representative topic/domain mining.
4. Perform open coding and normalize synonyms and hierarchy.
5. Use triads, descriptions, similar records, positive examples, and hard negatives to define labels.
6. Pilot with local evidence plus selective MCP enrichment for gaps and boundary cases.
7. Present taxonomy, rules, MCP evidence, pilot findings, and corrections together at the freeze gate.
8. Move to `closed` after the user freezes taxonomy and rules.

## Semi-open

1. Audit the existing taxonomy and examples.
2. Execute focused MCP retrieval for weak definitions, uncovered concepts, and adjacent-label boundaries.
3. Pilot with formal labels and record coverage gaps separately.
4. Propose candidate additions, merges, splits, or deprecations with representative evidence.
5. Present changes and pilot results together at the freeze gate.
6. Move to `closed` only after the user freezes taxonomy and rules.

## Closed

1. Load frozen taxonomy and rules.
2. Validate prerequisites.
3. Use the execution gate to confirm the full-run scope and selective-MCP trigger policy.
4. Label only with formal labels.
5. Use MCP only for missing evidence, ambiguity, boundary comparison, and QA investigation.
6. Send uncovered concepts to `unclassified`, `needs_review`, or `Taxonomy Backlog` according to the routing rules.
7. Reopen `semi_open` only with user approval.

## Task states

Use these resumable states:

`pending_validation` -> `diagnosing` -> `awaiting_scope_confirmation` -> `building_assets` -> `piloting` -> `awaiting_freeze_confirmation` -> `frozen` -> `awaiting_full_run_authorization` -> `labeling` -> `validating` -> `awaiting_review` -> `completed`

Record the current state and approved artifact versions in the task configuration.
