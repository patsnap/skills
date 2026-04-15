# Workflow

Use a writable run folder such as:

`artifacts/tech-route-comparison/<YYYYMMDD-topic>/`

Recommended layout:

- `request.md`
- `workplan.md`
- `method_decisions.md`
- `query_log.csv`
- `source_index.csv`
- `claim_ledger.csv`
- `report.md`
- `notes/`
- `deliverables/`

## Execution Order

1. Freeze scope: topic, route set, scenario, purpose, time window, and mode.
2. Write the comparison basis before wide retrieval.
3. Retrieve route evidence in comparable buckets.
4. Normalize the evidence into one comparison matrix.
5. Promote the major route judgments into the claim ledger.
6. Write `report.md` only after the main ranking logic is traceable.

## Resume Order

If the run is interrupted, read these files first:

1. `request.md`
2. `workplan.md`
3. `method_decisions.md`
4. `claim_ledger.csv`
5. `source_index.csv`
6. `query_log.csv`
7. `report.md`

## Routing Rule

If a named company becomes the main object, move the task to `company-tech-profile`.

If player discovery or arena mapping becomes the main object, move the task to `competitive-landscape`.

If a concrete proposal becomes the main object, move the task to `rd-initiation-review`.
