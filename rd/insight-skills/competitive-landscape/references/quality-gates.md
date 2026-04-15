# Quality Gates

## Operating Gates

### Scope Gate

- [ ] Arena, geography, time window, and decision use are frozen before wide retrieval
- [ ] Candidate discovery happens before tiering

### Evidence Gate

- [ ] Sector-level and player-level evidence are kept distinct
- [ ] Major conclusions move through `source_index.csv` and `claim_ledger.csv` before they appear in the report

### Normalization Gate

- [ ] Discovered players, shortlisted players, and deep-dived players are not collapsed into one undifferentiated set

### Downgrade Gate

- [ ] Tool tier and coverage limitations are stated explicitly
- [ ] Completeness language is weakened when the run is degraded

### Deliverable Gate

- [ ] `report.md`, `query_log.csv`, `source_index.csv`, and `claim_ledger.csv` all exist before completion claims

## Draft Gate

Before treating the draft as usable:

- [ ] Arena scope and geography are explicit
- [ ] At least 3 sector-wide searches executed with results analyzed
- [ ] Candidate pool was built from evidence before tiering
- [ ] Final player set is defensible with inclusion/exclusion logic recorded
- [ ] Route or geography claims are backed by sources
- [ ] The claim ledger covers the main rankings and conclusions
- [ ] Each strong conclusion traces back to at least one source id
- [ ] Verified fact / evidence-backed inference / open gap clearly separated

## Formal Gate

Before calling the bundle complete:

- [ ] `report.md`, `query_log.csv`, `source_index.csv`, and `claim_ledger.csv` all exist
- [ ] If sector or player patent scopes are broad, representative sampling was executed or explicitly skipped with reason
- [ ] If sampling was used, sector sample supported route discovery rather than directly deciding final player tiers
- [ ] If player sampling was used, each player was sampled independently
- [ ] Top players deep-dived individually (not merged across players)
- [ ] Route differentiation matrix present with evidence backing per cell
- [ ] White-space claims satisfy all 3 criteria (sparse + valuable + entry path) or are labeled as observations
- [ ] The report distinguishes discovered players from prioritized players
- [ ] No tier assigned without patent, paper, or product evidence basis
- [ ] Tool tier and coverage limitations stated explicitly in the output
- [ ] Weak signals are not overstated as confirmed facts
- [ ] Optional `docx` or `pdf` outputs, if claimed, have actually been rendered

## Failure Rule

If player discovery is incomplete or the sample is too thin, downgrade the
wording. Do not force a completeness claim when the evidence does not support it.

The claim ledger is the minimum control point for strong claims.
