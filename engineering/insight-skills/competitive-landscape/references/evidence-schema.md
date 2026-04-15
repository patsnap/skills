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

- Keep player inclusion logic traceable in the claim ledger.
- Keep final tiering logic traceable in the claim ledger.
- Use stable source ids such as `S001`, `S002`, `S003`.
