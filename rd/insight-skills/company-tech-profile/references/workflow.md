# Workflow

Use a writable run folder such as:

`artifacts/company-tech-profile/<YYYYMMDD-company-topic>/`

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

1. Freeze scope: company, topic, purpose, time window, and audience.
2. Resolve entity boundaries and aliases before counting activity.
3. Retrieve evidence in narrow batches instead of one noisy umbrella search.
4. Promote useful sources into `source_index.csv` as you go.
5. Turn evidence into explicit claims in `claim_ledger.csv`.
6. Write `report.md` only after the major claims have evidence attached.

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

If the task drifts into arena mapping, tiering, or multi-player comparison,
stop expanding this run and move the task to `competitive-landscape`.

If the task becomes a route-only question, move it to `tech-route-comparison`.
