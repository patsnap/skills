# Evidence Schema

## query_log.csv

Minimum columns:

- `query_id`
- `timestamp`
- `tool`
- `purpose`
- `query_text`
- `scope`
- `result_count`
- `notes`

## source_index.csv

Minimum columns:

- `source_id`
- `title`
- `source_type`
- `organization`
- `date`
- `url_or_locator`
- `why_it_matters`
- `confidence`

## claim_ledger.csv

Minimum columns:

- `claim_id`
- `claim`
- `claim_type`
- `supporting_source_ids`
- `confidence`
- `counterpoint_or_limit`
- `decision_relevance`

## Citation Discipline

- A source belongs in `source_index.csv` before it is cited in `report.md`.
- A major conclusion belongs in `claim_ledger.csv` before it is promoted into the report.
- Use stable source ids such as `S001`, `S002`, `S003`.
