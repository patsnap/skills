# Setup Guide — FTO Screening Report

This package converts a risk-point Word document and user-approved PatSnap
search expressions into a traceable, screening-level FTO report. It supports a
self-contained PatSnap REST workflow and an MCP-assisted evidence workflow.
Choose one mode per run and retain complete provenance.

## 1. Prerequisites

- Python 3.10 or later;
- `requests` and `python-docx`;
- a readable risk-point `.docx` file;
- target product/process and version;
- target jurisdiction(s) and relevant commercial acts;
- one or more reviewed PatSnap search expressions;
- either PatSnap REST API access or the relevant PatSnap MCP connector(s).

This package generates an FTO screening, not a legal clearance opinion.

## 2. Choose a data-access mode

### Mode A — PatSnap REST API

1. Register or sign in at the
   [PatSnap Open Platform](https://open.patsnap.com/).
2. Obtain an API key with access to the required endpoints.
3. Open `references/zhihuiya_config.json`.
4. Replace `PUT_YOUR_PATSNAP_API_KEY_HERE` in your private local copy.
5. Keep `patsnap_base_url` set to `https://connect.patsnap.com` unless PatSnap
   provides a different approved endpoint for your account.

The source filename `zhihuiya_config.json` is retained to preserve the original
package topology. Its content and authentication behavior are global PatSnap.

The REST client sends the key as:

```http
Authorization: Bearer YOUR_API_KEY
```

Never commit, publish, log, or embed a real key in a report. Do not append the
key to a URL.

Official resources:

- [PatSnap Developer Center](https://open.patsnap.com/devportal)
- [REST API overview](https://open.patsnap.com/devportal/guides/rest-api-overview)
- [P070 Keyword Assistant](https://open.patsnap.com/devportal/api-reference/search/patent/keyword-suggest)
- [P018 Claim](https://open.patsnap.com/devportal/api-reference/basic-patent-data/claim-data)

### Mode B — PatSnap MCP connectors

Browse the current
[PatSnap MCP marketplace](https://open.patsnap.com/marketplace/mcp-servers)
and install only the connectors required for the run.

| Connector | Use | Requirement |
|---|---|---|
| [Patsnap Patent Research](https://open.patsnap.com/marketplace/mcp-servers/patsnap-ip-searching) | End-to-end invention FTO task submission and retrieval through `fto_review` and `get_task` | Recommended for complete agent-assisted screening |
| [Advanced Patent Search](https://open.patsnap.com/marketplace/mcp-servers/patent-search) | Query, semantic, classification, assignee, similar-patent, and filtered retrieval | Recommended for independent search control |
| [Patent Briefing](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing) | Claims, translated claims, description, bibliography, family, status, images, and technical summary | Required for candidate verification when those fields are not otherwise supplied |
| [Global Core Patents](https://open.patsnap.com/marketplace/mcp-servers/core-patents) | Detailed legal events, status, family, PDF, reexamination, licensing, and citations | Optional for deeper verification |

Verified connector identifiers and endpoints:

```text
patsnap_patent_research
https://open.patsnap.com/marketplace/mcp-servers/patsnap-ip-searching

advanced_patent_search
https://open.patsnap.com/marketplace/mcp-servers/patent-search

patent_briefing
https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
```

Do not place a real key in documentation or source control. Configure the MCP
URL through the client UI or its secure local configuration.

## 3. Connectivity check

### REST mode

Run a dry run first; it must not call PatSnap:

```bash
python scripts/run_generic_fto_report.py \
  --input risk_points.docx \
  --queries queries.json \
  --output-dir output \
  --dry-run
```

Then run a narrowly scoped authorized request. Confirm that:

- the base URL is `https://connect.patsnap.com`;
- authentication is sent in the Bearer header;
- the endpoint is authorized for the key;
- request/response metadata is logged without the key;
- a failed call exits visibly and does not create a false no-result conclusion.

### MCP mode

Use the client's connector status view to confirm the selected connector is
available. Call one low-cost read/search operation appropriate to the task and
verify that the result includes identifiable patent records and provenance.
Do not run a full FTO task merely as a connectivity probe.

If a connector is unavailable, continue only with evidence already supplied or
switch to REST mode with user authorization. Record the mode change.

## 4. Inputs

The risk document should identify:

- product/process name and controlled version;
- technical feature groups and product evidence;
- target jurisdictions;
- relevant commercial acts;
- search and legal-status cutoffs;
- known competitors or assignees, if relevant;
- family/counting convention;
- report purpose and decision date.

Search expressions may be supplied through a JSON file or repeated command-line
arguments. They must be preserved exactly in `queries.json` with their source.

## 5. Typical REST execution

```bash
python scripts/run_generic_fto_report.py \
  --input risk_points.docx \
  --queries queries.json \
  --api-config references/zhihuiya_config.json \
  --business-config references/config.json \
  --output-dir output
```

Use `--help` for the authoritative argument list in the localized runner.

Expected work products include:

- `queries.json` — reviewed search expressions and provenance;
- `patent_list.json` — normalized candidates and matching queries;
- `claim_chart.json` — structured claim-limitation comparisons;
- `fto_structured_data.json` — complete report data and limitations;
- an English HTML report;
- an English DOCX report.

Generated work products belong in the run output directory, not in this skill
package.

## 6. Evidence and legal controls

- P018 must use `/basic-patent-data/claim-data`.
- Claim 1 screening does not prove that all material claims were reviewed.
- Confirm each target-jurisdiction family member and current claim version.
- A status filter is not proof of enforceability.
- Pending applications belong in a watchlist.
- AI07 output is supporting evidence; retain conflicts and rely on retrieved
  claims, product evidence, and qualified review.
- Do not state “no risk,” “cleared,” or “all relevant patents found.”
- Qualified local counsel should review decision-material conclusions.

## 7. Troubleshooting

| Symptom | Check |
|---|---|
| 401 / authentication failure | Key placeholder, Bearer header, key validity |
| 403 / no permission | Endpoint entitlement and account quota |
| 404 | Global base URL and current endpoint path |
| Timeout | Read timeout, retry limit, request size, service status |
| Empty result | Query syntax, jurisdiction filter, dates, pagination, and response status |
| Missing claims | Correct patent identifier, P018 response language, family member, and `replace_by_related` policy |
| Partial report | Inspect the run manifest and per-step errors; do not infer a negative search result |
| MCP unavailable | Verify connector installation and configuration; use REST only with authorization |

## 8. Security checklist

- real keys remain in private local configuration only;
- logs and exceptions redact credentials;
- no query URL contains a key;
- output JSON records provenance but not credentials;
- confidential product materials are transmitted only with user authorization;
- local absolute paths and personal metadata are removed from deliverables.

## 9. Marketplace reference

[FTO Screening Report](https://open.patsnap.com/marketplace/skill-hub/generic-fto-report)
