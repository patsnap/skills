# Workflow

Use a writable run folder such as:

`artifacts/competitive-landscape/<YYYYMMDD-topic>/`

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

1. Freeze scope: topic, region, purpose, time window, and player count target.
2. Build a candidate pool from multiple searches and source lanes.
3. Tag or normalize the candidate pool before tiering.
4. Promote the strongest players into the final comparison set.
5. Compare route bets and geography splits on that narrowed set.
6. Write `report.md` only after the player set and major claims are traceable.

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

If the task narrows to one company, move it to `company-tech-profile`.

If the task becomes a route-only decision with no player object, move it to `tech-route-comparison`.
