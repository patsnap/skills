# Quality Gates

## Operating Gates

### Scope Gate

- [ ] Route set is frozen before wide retrieval
- [ ] Topic, application scenario, comparison level, and time window are explicit

### Evidence Gate

- [ ] Major route judgments move through `source_index.csv` and `claim_ledger.csv` before they appear in the report
- [ ] Per-route evidence is collected independently before cross-route comparison

### Normalization Gate

- [ ] `comparison_basis.md` exists and defines route scope, dimensions, and normalization rules
- [ ] Maturity or TRL language uses an explicit rubric

### Counterevidence Gate

- [ ] The main recommendation includes weakening conditions or update triggers

### Downgrade Gate

- [ ] Tool tier and coverage limitations are stated explicitly
- [ ] Confidence language is weakened when the run is degraded

### Deliverable Gate

- [ ] `report.md`, `comparison_basis.md`, `query_log.csv`, `source_index.csv`, and `claim_ledger.csv` all exist before completion claims

## Draft Gate

Before treating the draft as usable:

- [ ] Route set is frozen before wide retrieval
- [ ] Comparison basis is explicit and written to `comparison_basis.md`
- [ ] Comparison level is consistent (not mixing material/component/system)
- [ ] The comparison matrix is readable with evidence per cell
- [ ] The claim ledger covers the main route rankings and tradeoffs
- [ ] The recommendation is tied to the user's scenario
- [ ] Verified fact / evidence-backed inference / open gap clearly separated

## Formal Gate

Before calling the bundle complete:

- [ ] `report.md`, `comparison_basis.md`, `query_log.csv`, `source_index.csv`, and `claim_ledger.csv` all exist
- [ ] At least 2 searches per route executed with results analyzed
- [ ] Per-route evidence collected independently before cross-route comparison
- [ ] If TRL or maturity labels are used, explicit rubric is present
- [ ] Counterevidence pass completed for the main recommendation
- [ ] Every major claim has a traceable source citation
- [ ] Ranking language is matched to evidence strength
- [ ] Tool tier and coverage limitations stated explicitly
- [ ] Assumptions and normalization notes are visible
- [ ] If evidence is insufficient for confident ranking, stated explicitly
- [ ] Optional `docx` or `pdf` outputs, if claimed, have actually been rendered

## Failure Rule

If the route set is under-defined or the evidence is too thin, downgrade the
recommendation and state what would change the answer. Do not force a definitive
ranking when the comparison basis is incomplete.

The claim ledger is the minimum control point for strong claims.
