# Workflow

Use a writable run folder such as:

`artifacts/rd-initiation-review/<YYYYMMDD-project>/`

Recommended layout:

- `request.md`
- `workplan.md`
- `method_decisions.md`
- `query_log.csv`
- `source_index.csv`
- `claim_ledger.csv`
- `report.md`
- `novelty-note.md`
- `notes/`
- `deliverables/`

## Execution Order

1. Freeze scope: project object, gate, audience, time window, and mode.
2. Extract proposal-stated claims before external search.
3. Normalize the innovation points into a short comparison set.
4. Retrieve external evidence to test novelty, feasibility, and overlap.
5. Build the recommendation and conditions in the claim ledger.
6. Write `report.md` and `novelty-note.md` only after the main claims are traceable.

## Resume Order

If the run is interrupted, read these files first:

1. `request.md`
2. `workplan.md`
3. `method_decisions.md`
4. `claim_ledger.csv`
5. `source_index.csv`
6. `query_log.csv`
7. `report.md`
8. `novelty-note.md`

## Routing Rule

If there is no concrete project object, stop stretching this skill.

- Route route-only decisions to `tech-route-comparison`.
- Route company-only profiling to `company-tech-profile`.
- Route multi-player arena work to `competitive-landscape`.
