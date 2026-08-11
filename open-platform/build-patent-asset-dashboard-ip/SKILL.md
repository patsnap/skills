---
name: build-patent-asset-dashboard-ip
description: Build the patent-data layer for an applicant asset dashboard using PatSnap search and analytics APIs. Use when an IP analyst or developer needs applicant patent retrieval, patent-type subsets, filing trends, industry distribution, filing-office coverage, top inventors, or an innovation word cloud with documented collapse and counting rules.
---

# Build a patent asset dashboard

## Overview

Use PatSnap Open Platform patent-search and analytics APIs to populate an applicant patent asset dashboard. Preserve the source capability identifiers `P00X`, `A00X`, `S00X`, and `D00X` because they identify API contracts rather than Chinese UI labels.

## Authentication

Pass a PatSnap Open Platform API key in the HTTP Authorization header:
```
Authorization: Bearer <token>
```
Read the key from `PATSNAP_API_KEY` or accept it through a secure runtime argument. Never embed or log a real key. See the current [PatSnap authentication guide](https://open.patsnap.com/devportal/guides/authentication).

---

## Shared fixed request parameters for the P002 series

```json
{
  "collapse_by": "PBD",
  "collapse_type": "APNO",
  "collapse_order": "LATEST"
}
```
> **Do not add `collapse_order_authority` to this source-defined P002 dashboard request.** The frozen source validation found that it changed the CN application count. If a future official schema or business rule requires the field, treat that as a versioned contract change and revalidate every dashboard count.

---

## P002 — Retrieve all applicant patents with application-level collapsing

### Endpoint

- **Method**: POST
- **URL**: `https://connect.patsnap.com/search/patent/query-search-patent/v2`
- **Current official capability evidence**: the PatSnap Developer Center and current patent-search MCP pages document the global query-search path and `data.results` response convention. Recheck the OpenAPI schema before production release.

### Request body
```json
{
  "query_text": "ANCS:(Applicant name)",
  "collapse_by": "PBD",
  "collapse_type": "APNO",
  "collapse_order": "LATEST"
}
```

### Response paths
```python
total = result["data"]["total_search_result_count"]
patents = result["data"]["results"]
```

### Historical source validation records

These counts were recorded against the Chinese source environment. Preserve them as regression provenance, not as current global counts.

| Source test applicant | Returned total | Source status |
|-----------|---------|------|
| Beijing Low Carbon Clean Energy Research Institute | 3,341 | Passed in source fixture |
| CHN Energy Science and Technology Research Institute Co., Ltd. | 1,463 | Passed in source fixture |

---

## P002B — Retrieve granted invention patents by applicant

### Request body
```json
{
  "query_text": "ANCS:(Applicant name) and PATENT_TYPE:(B)",
  "collapse_by": "PBD",
  "collapse_type": "APNO",
  "collapse_order": "LATEST"
}
```

---

## P002U — Retrieve utility models by applicant

### Request body
```json
{
  "query_text": "ANCS:(Applicant name) and PATENT_TYPE:(U)",
  "collapse_by": "PBD",
  "collapse_type": "APNO",
  "collapse_order": "LATEST"
}
```

---

## P002D — Retrieve design patents or registered designs by applicant

### Request body
```json
{
  "query_text": "ANCS:(Applicant name) and PATENT_TYPE:(D)",
  "collapse_by": "PBD",
  "collapse_type": "APNO",
  "collapse_order": "LATEST"
}
```
> Some applicants have no design records in the selected scope. Treat `total_search_result_count = 0` as a valid result, not an API failure.

---

## A001 — Filing trend for the most recent ten complete years

### Endpoint

- **Method**: POST
- **Source endpoint**: `/insights-openapi/patent-trends-query`
- **Global endpoint status**: not verified in the current public PatSnap Developer Center on 2026-08-07. Do not construct or publish a `connect.patsnap.com` URL by substitution. Obtain the current endpoint from the authenticated API catalog before execution.

### Request body
```json
{
  "query_text": "ANCS:(Applicant name)",
  "collapse_by": "PBD",
  "collapse_type": "APNO",
  "collapse_order": "LATEST"
}
```
> Do not add `collapse_order_authority` under the source-defined counting contract.

### Response structure
```json
{
  "status": true,
  "data": [
    {"year": "2016", "application": 163, "granted": 133, "percentage": 0.816},
    ...
  ]
}
```
> `data` is a direct array. Read it through `result["data"]`, then select the required year window.

### Rolling-window logic
```python
from datetime import date

end_year = date.today().year - 1
years_10 = [str(y) for y in range(end_year - 9, end_year + 1)]
trend_10y = [item for item in result["data"] if item["year"] in years_10]
```

Record the computed start and end years in the dashboard metadata. To reproduce the frozen source fixture exactly, set the window explicitly to 2016–2025.

---

## S001 — International technology classification distribution

### Localization decision

The source S001 used nine categories from China's Strategic Emerging Industries (SEIC) policy taxonomy. That taxonomy is not an internationally recognized patent classification and is not suitable as the default for a global applicant dashboard. Replace the China-specific nine-query loop with IPC/CPC aggregation while preserving the source objective: show where an applicant's patent activity is concentrated.

### Verified global endpoints

- **Aggregation**: POST `https://connect.patsnap.com/search/patent/query/v2`
- **Official documentation**: [P003 Analytics Query Search and Filter](https://open.patsnap.com/devportal/api-reference/patent-field/query)
- **Classification discovery**: GET `https://connect.patsnap.com/search/patent/classification/helper-search`
- **Official documentation**: [P072 Classification Search Assistant](https://open.patsnap.com/devportal/api-reference/search/patent/classification/helper-search)
- **Classification descriptions**: POST `https://connect.patsnap.com/high-value-data/patent-classification-description`
- **Official documentation**: [P066 Patent Classification Description](https://open.patsnap.com/devportal/api-reference/high-value-data/patent-classification-description)

### Default classification views

1. IPC section, class, subclass, and main-group distribution.
2. CPC section, class, subclass, and main-group distribution when CPC coverage is sufficient.
3. LOC distribution for a design-focused dashboard when requested.
4. UPC, FI, or F-term only for a relevant jurisdiction or specialist workflow.
5. User-defined technology taxonomy only when the mapping rules and unmapped share are documented.

### Aggregation request pattern

```json
{
  "lang": "en",
  "query": "ANCS:(Applicant name)",
  "field": "IPC_SUB_CLASS,CPC_SUB_CLASS",
  "limit": 100,
  "offset": 0,
  "stemming": 0,
  "collapse_by": "PBD",
  "collapse_type": "APNO",
  "collapse_order": "LATEST"
}
```

Use only field names supported by the current P003 schema. Query one classification level at a time if the response or entitlement does not support multiple fields.

### Required S001 output

| Classification | Code | English description | Patent count | Share of classified records | Level | Version/source |
|---|---|---|---:|---:|---|---|

Report:

- the applicant query and applicant-field definition;
- IPC/CPC level and classification version;
- collapse/counting method;
- total portfolio count;
- classified-record count and unclassified-record count;
- whether patents can appear in more than one class;
- top-N cutoff and omitted-category share; and
- data cut-off date.

Do not compare classification shares as mutually exclusive when one patent may carry multiple IPC/CPC codes. Do not label an IPC/CPC class as an “industry” without a documented mapping.

---

## D109 — Filing-office distribution and foreign-filing coverage

### Endpoint

- **Method**: POST
- **Source endpoint**: `/shhgy/reportdata/rec-office`
- **Global endpoint status**: not verified in the current public PatSnap Developer Center on 2026-08-07. Obtain the exact current endpoint from the authenticated API catalog; do not publish a guessed host/path combination.

### Request body
```json
{
  "query_text": "ANCS:(Applicant name)",
  "collapse_by": "PBD",
  "collapse_type": "APNO",
  "collapse_order": "LATEST"
}
```
> Do not add `collapse_order_authority` under the frozen source contract. The source fixture for Baoshan Iron & Steel changed from 13,378 to 16,179 CN records when the field was added.

### Foreign-filing calculation

Define a configurable `home_authority` for the applicant and report it explicitly:

`foreign filing count = sum of all receiving-office counts − home-authority count`

For the source China-specific fixture, `home_authority = CN`.

### Response structure
```json
{
  "data": {
    "values": [
      {"rec_office": "China", "code": "CN", "num": 13378},
      {"rec_office": "European Patent Office", "code": "EP", "num": 628},
      ...
    ]
  }
}
```

### Calculation logic
```python
values = result["data"]["values"]
total_all = sum(item["num"] for item in values)
home_authority = "CN"
home_count = next((item["num"] for item in values if item["code"] == home_authority), 0)
foreign_count = total_all - home_count
```

### Historical source validation records

| Applicant | Total | CN | Foreign |
|--------|------|----|------|
| Beijing Low Carbon Clean Energy Research Institute | 3,341 | 3,066 | 275, passed source fixture |
| Baoshan Iron & Steel Co., Ltd. | 17,088 | 13,378 | 3,710, passed source fixture |

---

## A006 — Top inventors by active patent holdings

### Endpoint

- **Method**: GET
- **URL**: `https://connect.patsnap.com/insights/inventor-ranking`
- **Official documentation**: [A006 Top Inventors](https://open.patsnap.com/devportal/api-reference/insights/inventor-ranking), verified 2026-08-07.

### `query_text` format
```
ANCS:(Applicant name) and SIMPLE_LEGAL_STATUS:(1) and PATENT_TYPE:(B or U or D)
```

### Response structure
```json
{
  "data": [
    {"name": "Example inventor", "count": 137},
    ...
  ]
}
```

### Data path
```python
inventors = result["data"]  # Direct array ordered by descending count.
```

---

## A002 — Innovation word cloud

### Endpoint

- **Method**: POST
- **URL**: `https://connect.patsnap.com/insights/word-cloud-query`
- **Official documentation**: [A002 Innovation Word Cloud](https://open.patsnap.com/devportal/api-reference/insights/word-cloud-query), verified 2026-08-07.

### Complete request body
```json
{
  "lang": "en",
  "query_text": "ANCS:(Applicant name)",
  "collapse_by": "PBD",
  "collapse_type": "DOCDB",
  "collapse_order": "LATEST"
}
```
> This endpoint uses `collapse_type: DOCDB`, unlike the APNO collapse used by the other source dashboard queries.
> Pass `lang`, `collapse_by`, and `collapse_order`; omitting any of them can change the result.
> Default to `lang: en` for the global dashboard. Use `cn` or `jp` only when the requested output or corpus requires that supported language.

### Data path
```python
words = result["data"]  # Direct array, up to 100 terms ordered by descending count.
```

---

## Capability summary

| Capability | Method | Endpoint | Description |
|----------|------|------|------|
| P002 | POST | query-search-patent/v2 | All patent types |
| P002B | POST | query-search-patent/v2 | Granted invention patents |
| P002U | POST | query-search-patent/v2 | Utility models |
| P002D | POST | query-search-patent/v2 | Designs |
| A001 | POST | patent-trends-query | Rolling ten-year filing/grant trend; global endpoint requires verification |
| S001 | POST/GET | query/v2 plus classification helper/description | International IPC/CPC technology distribution replacing the China-only SEIC taxonomy |
| D109 | POST | rec-office | Filing-office distribution; configurable home authority; global endpoint requires verification |
| A006 | GET | inventor-ranking | Top inventors by active holdings |
| A002 | POST | word-cloud-query | Innovation word cloud with `lang: en` and `collapse_type: DOCDB` |

---

## Planned expansion

- Add capabilities only when they are introduced in the authoritative source package or separately approved under the migration source-structure gate.

## MCP and API configuration

This source package is primarily a PatSnap REST API workflow. It does not contain a README and no new setup file may be added without approval.

- Authenticate REST calls with a PatSnap Open Platform API key.
- Verify each endpoint in the current [PatSnap Developer Center](https://open.patsnap.com/devportal) before execution.
- The [Global Core Patent Database](https://open.patsnap.com/marketplace/mcp-servers/core-patents) MCP may optionally provide its documented `search_patents` capability for P002-style retrieval.
- Do not claim that this MCP implements A001, D109, A006, or A002 unless those exact tools are discovered and documented.
- When an endpoint or entitlement is unavailable, provide the dashboard schema and mark the affected panel `Data unavailable`; never fabricate values.
