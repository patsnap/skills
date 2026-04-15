# Quality Gates

## Operating Gates

### Scope Gate

- [ ] Concrete project object, review gate, and mode are frozen before wide retrieval
- [ ] Proposal materials are extracted before any external search

### Evidence Gate

- [ ] Major review conclusions move through `source_index.csv` and `claim_ledger.csv` before they appear in the report
- [ ] Proposal-stated, externally corroborated, inferred, and open-gap layers remain distinct

### Normalization Gate

- [ ] Innovation points are normalized into a stable comparison set before novelty assessment
- [ ] Expertise/resources and material completeness are treated as explicit review dimensions

### Counterevidence Gate

- [ ] The main recommendation includes weakening conditions, blockers, or next-evidence needs

### Downgrade Gate

- [ ] Tool tier and coverage limitations are stated explicitly
- [ ] Public-only runs do not imply internal duplicate-project exclusion

### Deliverable Gate

- [ ] `report.md`, `novelty-note.md`, `query_log.csv`, `source_index.csv`, and `claim_ledger.csv` all exist before completion claims

## Draft Gate

### All Modes

- [ ] Concrete project object identified (not just a topic)
- [ ] Proposal-stated claims extracted before external search
- [ ] Four-layer evidence separation maintained (proposal-stated / externally corroborated / evidence-backed inference / open gap)
- [ ] Tool tier and coverage limitations explicitly stated
- [ ] Material completeness assessment present
- [ ] If internal archives unavailable, stated as `内部查重边界未核验`
- [ ] `novelty-note.md` exists when overlap is part of the decision
- [ ] Proposal claims and external evidence are not mixed carelessly
- [ ] The claim ledger covers novelty, feasibility, and evidence-gap conclusions

### Screen Mode Additional

- [ ] Go/no-go recommendation present with conditions
- [ ] Novelty boundary summary present
- [ ] Key gaps and next steps identified

### Review Mode Additional

- [ ] At least 2 patent searches and 1 paper search executed per innovation point
- [ ] Novelty comparison table present
- [ ] Every major claim has a traceable source citation

### Innovation Mode Additional

- [ ] Each innovation point assessed individually
- [ ] Differentiation boundary table present
- [ ] Residual differentiators explicitly stated per point

## Formal Gate

### All Modes

- [ ] `report.md`, `novelty-note.md`, `query_log.csv`, `source_index.csv`, and `claim_ledger.csv` all exist
- [ ] Proposal claims and external evidence are not mixed carelessly
- [ ] Limitations and missing data are stated explicitly
- [ ] The claim ledger remains the control point for strong conclusions

### Assurance Mode Additional

- [ ] Scoring rubric explicit and traceable
- [ ] Stage-gate matrix with conditions, owners, and consequences
- [ ] Counterevidence pass completed
- [ ] Technical decomposition covers main chain, dependencies, and failure modes
- [ ] Optional `docx` or `pdf` outputs, if claimed, have actually been rendered

## Failure Rule

If the evidence is too thin for a strong go/no-go statement, downgrade the
wording and keep the recommendation conditional. Do not force certainty.

The claim ledger is the minimum control point for strong claims.
