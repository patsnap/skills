# Quality Gates

## Operating Gates

### Scope Gate

- [ ] Company, topic, time window, and decision use are frozen before wide retrieval
- [ ] Parent/subsidiary and alias scope is resolved or explicitly narrowed

### Evidence Gate

- [ ] Major conclusions move through `source_index.csv` and `claim_ledger.csv` before they appear in the report
- [ ] Patents, papers, and public signals are triangulated when the evidence base allows it

### Normalization Gate

- [ ] Company counts and route claims include scope caveats when office bias, family/equivalent issues, or thin coverage matter

### Downgrade Gate

- [ ] Tool tier and coverage limitations are stated explicitly
- [ ] Confidence language is weakened when the run is degraded

### Deliverable Gate

- [ ] `report.md`, `query_log.csv`, `source_index.csv`, and `claim_ledger.csv` all exist before completion claims

## Draft Gate

Before treating the draft as usable:

- [ ] Company/topic boundary is explicit and aliases resolved
- [ ] At least 1 patent search and 1 paper search executed
- [ ] Main routes or clusters are clearly stated with evidence
- [ ] The report answers the user's decision question
- [ ] The claim ledger exists and covers the main conclusions
- [ ] Each strong conclusion traces back to at least one source id
- [ ] Verified fact / evidence-backed inference / open gap clearly separated

## Formal Gate

Before calling the bundle complete:

- [ ] `report.md`, `query_log.csv`, `source_index.csv`, and `claim_ledger.csv` all exist
- [ ] If patent scope is broad, representative sampling was executed or explicitly skipped with reason
- [ ] If sampling was used, sampled set is treated as representative, not exhaustive
- [ ] Core technology routes identified with patent or paper evidence
- [ ] Company marketing claims treated as signals, not facts, unless corroborated
- [ ] Tool tier and coverage limitations stated explicitly in the output
- [ ] Uncertainty and downgrade paths are stated explicitly
- [ ] Weak signals are not overstated as confirmed facts
- [ ] No drift into generic company biography without technical substance
- [ ] If evidence is insufficient, explicitly stated with follow-up suggestions
- [ ] Optional `docx` or `pdf` outputs, if claimed, have actually been rendered

## Failure Rule

If the evidence is too thin for a strong conclusion, downgrade the wording. Do
not force certainty just to make the report sound polished.

The claim ledger is the minimum control point for strong claims.
