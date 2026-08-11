# Reference implementation — high-value patent portfolio screening

These ten source-provided scripts implement the complete workflow in
`../SKILL.md`. They use the global PatSnap Connect REST service, write
restartable JSON checkpoints, always generate the required static HTML report,
and optionally generate the same evidence as a Word report.

The pipeline is a relative portfolio-screening model. It does not create a
monetary valuation, validity opinion, enforceability conclusion, or investment
recommendation.

## Requirements

Python 3.10 or later is recommended.

```bash
python -m pip install requests python-docx
```

`requests` is required for REST retrieval. `python-docx` is required only for
the optional Word report. Set `PYTHONDONTWRITEBYTECODE=1` in controlled or
read-only environments if desired.

## Global PatSnap credentials

Use one of these private local methods:

```bash
read -s PATSNAP_API_KEY
export PATSNAP_API_KEY
```

or:

```bash
export PATSNAP_API_KEY_FILE="/secure/path/patsnap-key.txt"
```

The key is sent only in `Authorization: Bearer <key>` to
`https://connect.patsnap.com`. It is not written to checkpoints or reports.
Redirects are rejected so credentials cannot cross hosts. Do not put a key in a
query file, command argument, repository, screenshot, example, or report.

## Reviewed query

Supply a human-reviewed PatSnap query:

```bash
export HVP_QUERY='TAC_ALL:("virtual reality") AND ALL_AN:("Example Corporation")'
```

or use an explicit file:

```bash
export HVP_QUERY_FILE="/project/reviewed-query.txt"
```

Record the legal entities, technologies, jurisdictions, dates, family rule,
database/status cutoffs, and screening purpose separately. The scripts preserve
the query but do not decide whether its scope is appropriate.

## Run the full pipeline

From any output directory:

```bash
python /path/to/scripts/run_all.py --output-dir ./screening-run
```

Optional Word report:

```bash
python /path/to/scripts/run_all.py --output-dir ./screening-run --word
```

P021 images are not downloaded by default because signed URLs may expire. To
embed only validated HTTP(S) image responses with an 8 MB cap:

```bash
python /path/to/scripts/run_all.py --output-dir ./screening-run --word --images
```

The selection ratio can be set within the approved 10–15% range:

```bash
python /path/to/scripts/run_all.py --selection-ratio 0.12
```

## Restartable stages

| Stage | Script | Primary output | Purpose |
|---:|---|---|---|
| 1 | `hv_1_fetch.py` | `cand_raw.json` | P002 pagination, repeated-page detection, normalization, identifier deduplication |
| 2 | `hv_2_numeric.py` | `enrich_num.json` | P014 family and P015 citation values with `available/empty/missing/error` states |
| 3 | `hv_3_legal.py` | `enrich_legal.json` | Event-level P034/P027/P028/P029 evidence and per-category state |
| 4 | `hv_4_score.py` | `scored.json` | Core inventors, 30/30/20/20 components, deterministic ranking and 10–15% selection |
| 5 | `hv_5_display.py` | `enrich_display.json` | Selected-record P021 drawing, English P025 summary and P041 simple status |
| 6 | `hv_6_assemble.py` | `final_records.json`, `high_value_patent_screening_data.json` | Report-ready selection plus complete candidate trace |
| 7 | `hv_7_html_a.py` | `high_value_patent_portfolio_screening.html` | Required safe, static, responsive and print-ready report |
| 8 | `hv_8_word.py` | `high_value_patent_portfolio_screening.docx` | Optional US-Letter scientific Word report |

Each checkpoint contains a schema version, run ID, timestamp, stage, source
mode and upstream hash. Consumers reject incompatible schemas and mismatched run
IDs.

## Important interpretation rules

- Missing and failed evidence receive zero points under the default scoring
  policy but remain visibly `missing` or `error`; they are not factual zeros.
- Percentiles are relative to available observations in this query result.
- Forward citations are affected by age, field, authority, family method and
  database coverage.
- Family size is not market coverage, commercial success, validity, or
  enforceability.
- Legal-event presence is activity, not positive value. Review the underlying
  litigation, reexamination/invalidation, license and transfer records.
- PatSnap commonly returns inventors as
  `LASTNAME, FIRSTNAME|LASTNAME, FIRSTNAME`; commas stay inside one name and
  `|`, semicolon, full-width semicolon, or a line break separates records.
- Transliteration variants and homonyms are not merged automatically.
- Publication numbers remain plain text unless a verified stable global record
  URL is supplied. The localized scripts do not invent a product deep link.

## MCP-assisted operation

The local scripts are a REST reference implementation. In an MCP-capable host,
use these verified PatSnap services and export normalized evidence into the same
checkpoint contract:

- Advanced Patent Search — Recommended for candidate retrieval:
  `advanced_patent_search`,
  `https://open.patsnap.com/marketplace/mcp-servers/patent-search`,
  https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Patent Briefing — Recommended for representative patent bibliography,
  families, descriptions, images, translations and status:
  `patent_briefing`,
  `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`,
  https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Global Core Patents — Recommended for citation, family, legal-event,
  licensing, reexamination/invalidation and litigation evidence:
  https://open.patsnap.com/marketplace/mcp-servers/core-patents

Label connector/tool/request/date provenance. Do not claim these local scripts
called MCP. Do not mix REST and MCP-import provenance within one retrieval
record.

## Review checklist

Before distribution, reconcile P002 reported, retrieved, deduplicated, scored
and selected counts. Review query scope, entity normalization, cutoffs, family
rule, all missing/error fields, inventor identity, event meaning, selected
rationales, HTML safety and the complete JSON trace. Retain all checkpoints with
the report.
