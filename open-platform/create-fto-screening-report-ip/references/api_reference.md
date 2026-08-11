# PatSnap Open Platform API Reference for FTO Screening

Version: 2.0 localized international edition  
Verified against the global PatSnap Developer Center on 2026-08-07.

Use this reference to troubleshoot the bundled REST workflow. The live PatSnap
developer documentation remains authoritative because endpoints, entitlements,
limits, and response fields can change.

## 1. Scope and mode boundary

This package supports:

- bundled REST mode through `scripts/zhihuiya_api.py`; or
- MCP-assisted evidence imported under the schema in
  `references/claim_chart_schema.md`.

Do not mix modes without recording a provenance transition. This API reference
governs REST mode only. See `references/api_call_policy.md` for controls.

## 2. Global base URL

All REST requests use HTTPS:

```text
https://connect.patsnap.com
```

Do not use `connect.zhihuiya.com` in the international package.

Official overview:

```text
https://open.patsnap.com/devportal/guides/rest-api-overview
```

## 3. Authentication

Global PatSnap Open Platform API reference pages specify a valid API key in the
Authorization header as a Bearer token:

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
Accept: application/json
```

Configuration is read from the source-preserved filename:

```text
references/zhihuiya_config.json
```

The localized configuration fields are:

```json
{
  "patsnap_base_url": "https://connect.patsnap.com",
  "patsnap_auth_mode": "bearer_api_key",
  "patsnap_api_key": "PUT_YOUR_PATSNAP_API_KEY_HERE",
  "patsnap_connect_timeout_s": 10,
  "patsnap_read_timeout_s": 60,
  "patsnap_max_retries": 2,
  "patsnap_retry_backoff_s": 1.0
}
```

### 3.1 Credential rules

- Replace the placeholder only in a private local copy.
- Never append the key as `apikey=` in a URL.
- Never log request headers containing the key.
- Never embed the key in JSON work products, reports, exceptions, or test data.
- Fail closed when the placeholder is unchanged.
- Reject an unencrypted `http://` base URL.
- Do not silently fall back to a China-domain endpoint.

### 3.2 OAuth

The Chinese source retained an OAuth + query-key compatibility path. This
international edition does not enable that path by default because the current
global endpoint documentation used for this migration specifies Bearer API-key
authentication. Add or enable another mode only when the user's PatSnap account
documentation explicitly supports it and the complete flow is tested.

## 4. Common response envelope

Most source endpoints return a JSON object similar to:

```json
{
  "status": true,
  "error_code": 0,
  "data": {}
}
```

Code must not treat HTTP 200 alone as success. Verify the response type,
`status`, `error_code`, and required data shape. Preserve a sanitized error
record when the envelope is missing or inconsistent.

## 5. P070 — Keyword Assistant

Official page:

```text
https://open.patsnap.com/devportal/api-reference/search/patent/keyword-suggest
```

Endpoint:

```http
POST /search/patent/keyword-suggest
```

Request body fields are arrays:

```json
{
  "keyword": ["controller"],
  "lang": ["en"],
  "type": ["synonym", "related"]
}
```

### 5.1 Request fields

| Field | Type | Required | Notes |
|---|---|---:|---|
| `keyword` | array of strings | Yes | Terms to expand; retain each input term |
| `lang` | array of strings | Yes | Use `en` for the international workflow unless multilingual searching is justified |
| `type` | array of strings | Yes | `synonym`, `related`, and supported hierarchy options per live documentation |

The source describes `hypernym` as a “hyponym” in Chinese. Do not reproduce
that terminology error. Follow the current API definition and inspect returned
terms before incorporating them into a query.

### 5.2 Example success shape

```json
{
  "data": {
    "items": [
      {
        "input": "controller",
        "keyword_list": [
          {"keyword": "control unit"},
          {"keyword": "control module"}
        ]
      }
    ]
  },
  "status": true,
  "error_code": 0
}
```

### 5.3 Screening rule

Suggestions are vocabulary candidates. They are not automatically relevant,
complete, equivalent, or approved. Record accepted/rejected terms and reviewer
rationale. Never execute a materially broadened query without review.

## 6. P002 — Analytics Query Patent Search

Endpoint preserved from the source and current PatSnap FTO connector
capabilities:

```http
POST /search/patent/query-search-patent/v2
```

Example request:

```json
{
  "query_text": "TAC_ALL:(pump controller) AND AUTHORITY:(US)",
  "limit": 100,
  "offset": 0,
  "sort": [
    {"field": "SCORE", "order": "DESC"}
  ],
  "stemming": 0,
  "collapse_by": "PBD",
  "collapse_type": "ALL",
  "collapse_order": "LATEST",
  "collapse_order_authority": ["US", "EP", "JP", "KR", "CN"]
}
```

### 6.1 Required controls

- Preserve the exact user-approved `query_text`.
- Use English field names/queries as supported by PatSnap syntax.
- Keep `offset`, `limit`, sort, stemming, collapse, and authority order.
- Record every page request and raw/retained count.
- Enforce the current endpoint's offset/limit limits.
- Stop on repeated pages, malformed result arrays, or unrecoverable errors.
- Do not hard-code `CN` or `SIMPLE_LEGAL_STATUS:1`.
- Do not equate a status filter with enforceability.
- Explain family collapse and counting behavior.

### 6.2 Response fields used by this package

The runner normalizes fields when available:

| Normalized field | Possible source field | Purpose |
|---|---|---|
| `patent_id` | `patent_id` | PatSnap record identifier |
| `publication_number` | `pn`, `publication_number` | Display and deduplication |
| `application_number` | `apno`, `application_number` | Identifier reconciliation |
| `title` | `title` | Candidate context only |
| `current_assignee` | `current_assignee` | Entity context with date/source qualification |
| `publication_date` | `pbdt`, `publication_date` | Temporal evidence |
| `authority` | explicit or parsed from number | Target-jurisdiction check |
| `simple_legal_status` | current status field | Screening filter only |

Do not discard unknown fields from the stored raw response if they are needed
for audit, but do not expose secrets or unnecessary personal data.

### 6.3 Deduplication

Deduplicate by normalized publication number, then PatSnap patent ID, then
application number, and only then by a documented stable fallback. Merge
matching query IDs and retrieval provenance. Never deduplicate on title alone.

## 7. P018 — Claim Data

Official page:

```text
https://open.patsnap.com/devportal/api-reference/basic-patent-data/claim-data
```

Required endpoint:

```http
GET /basic-patent-data/claim-data
```

Query parameters:

| Parameter | Required | Notes |
|---|---:|---|
| `patent_id` or `patent_number` | Yes | Prefer the unambiguous identifier returned by search |
| `replace_by_related` | No | `0` by default; if `1`, disclose the replacement family member |

Example:

```http
GET https://connect.patsnap.com/basic-patent-data/claim-data?patent_number=US11205304B2&replace_by_related=0
Authorization: Bearer YOUR_API_KEY
```

Do not use the obsolete `/basic-patent-data/claims` path.

### 7.1 Typical response shape

```json
{
  "status": true,
  "data": [
    {
      "pn": "US11205304B2",
      "claims": [
        {
          "lang": "EN",
          "claim_text": "1. A method comprising ..."
        }
      ]
    }
  ],
  "error_code": 0
}
```

The source response examples include HTML-formatted claim fragments. The
client must support both plain and HTML-encoded text, preserve paragraph and
claim boundaries, and escape the content in reports.

### 7.2 Claim 1 extraction

The minimum source workflow extracts Claim 1. The parser must:

1. select the correct language record;
2. identify claim number 1 structurally when possible;
3. avoid truncating embedded numbering or dependent references;
4. preserve raw claim evidence separately;
5. record when parsing is heuristic;
6. fail visibly when Claim 1 cannot be identified.

Do not remove all whitespace from English claim text. Normalize only redundant
HTML/space while retaining readable limitation boundaries.

### 7.3 Legal limitation

Claim 1 alone is not a complete FTO review. Other independent claims and
material dependent claims may apply. The report must list reviewed and
unreviewed claims, current claim version, jurisdictional member, translation,
status evidence date, and family replacement behavior.

## 8. AI07 — CC GPT supporting analysis

Source endpoint:

```http
POST /chat/cc-gpt-stream
```

Example request:

```json
{
  "prompt": "Compare the supplied claim limitations with the cited product evidence. Return uncertainty and missing facts.",
  "stream": true
}
```

### 8.1 Controls

- Follow the current documented input length and streaming contract.
- Never send confidential product text without user authorization.
- Use a structured prompt that distinguishes claim text from product evidence.
- Ask for literal mapping, uncertainty, contrary evidence, and missing facts.
- Do not ask the model for an unqualified legal conclusion.
- Save the raw response and parsed output with a run-local reference.
- Record model/tool, date, request ID, and parse errors.
- Never allow AI output to overwrite the retrieved claim or product evidence.

### 8.2 Conflict rule

If AI07 conflicts with:

- the P018 claim text;
- a current official claim version;
- versioned product/process evidence;
- official legal-status evidence; or
- a qualified human review,

retain the conflict. The report must show the authoritative evidence and the
required human disposition. Do not silently prefer either output.

## 9. AI66 — FTO workflow endpoints

The Chinese source describes an eight-step internal workflow. The international
edition retains the documented capability map but does not guess unsupported
fields or route private behavior.

Known FTO workflow families include:

| Stage | Source path / current family | Purpose |
|---|---|---|
| Submit | `/ai/fto/submit` | Create a task from technical input |
| Extract features | `/ai/fto/feature/extract` or the currently documented endpoint | Obtain feature candidates |
| Confirm features | `/ai/fto/feature/confirm` | Confirm selected features |
| Start search | `/ai/fto/search/agent` | Begin agent search |
| Get search result | `/ai/fto/search/agent/result` | Poll result and retrieve candidates |
| Create report | `/ai/fto/report/create` | Submit selected final results |
| Get report | `/ai/fto/report/get` | Poll report and retrieve authorized output URL |

Official example for feature extraction:

```text
https://open.patsnap.com/devportal/api-reference/ai/fto/feature/extract
```

### 9.1 Contract-verification gate

Before enabling an AI66 stage:

1. open the current global developer page for that exact endpoint;
2. confirm method, path, authentication, request schema, response schema,
   status values, limits, and entitlement;
3. implement a mocked contract fixture;
4. perform an authorized narrow sandbox/live test;
5. record the verified contract date.

If any step cannot be verified, leave the stage disabled and use P002/P018 or
an approved PatSnap MCP workflow.

### 9.2 Removal of the source `cc_pids` assumption

The source speculates that adding an undocumented `cc_pids` array to the search
result request might inject a P002 candidate list. It then attempts to infer
server behavior from the returned records. This is not a verified public
contract and must not be used in the international implementation.

Do not send undocumented fields. If the user requires P002-controlled
candidates:

- retain them in the package's own normalized candidate set;
- retrieve claims through P018;
- perform the structured comparison locally or through an explicitly supported
  connector/tool; and
- preserve independent provenance for any AI66 result.

Never describe an AI66 result as limited to the P002 list unless the current
official contract explicitly supports and confirms that behavior.

### 9.3 Feature confirmation

The source fallback marks every extracted feature `is_select=true`. Do not do
this automatically. A reviewer must confirm which features define the target
product/process and which are optional, contextual, or incorrect.

### 9.4 Report result limits

The source states that report creation accepts one to five final results. Treat
this as a source constraint until reverified. The client must validate the
current official limit before a live call and must not truncate silently.

### 9.5 Asynchronous polling

- Use bounded polling with configurable interval and maximum wait.
- Honor server retry guidance where available.
- Stop on explicit failed/cancelled status.
- Record the last status and task ID on timeout.
- Do not submit duplicate paid tasks automatically after an ambiguous timeout.
- Never expose a task URL containing credentials.

## 10. P025 fallback evidence

The source client defines:

```text
/high-value-data/tech-problem-and-benefit-summary
```

This is technical summary evidence, not claim text. It must not replace P018
for limitation analysis. Enable only when the current global contract is
verified and label the output accurately.

## 11. Error handling

### 11.1 Platform/business codes from source and current docs

| Code | Meaning | Handling |
|---:|---|---|
| 67200001 | Usage/total limit exceeded | Stop or reduce scope; preserve partial state |
| 67200002 | Quota/QPS limit | Retry only when allowed, with bounded backoff |
| 67200003 | Authentication error or expired access | Stop; validate private key configuration |
| 67200004 | No entitlement / quota unavailable | Stop the affected step; do not infer no result |
| 67200005 | Insufficient balance/calls | Stop and report entitlement issue |
| 67200006 | Client expired | Stop and require account action |
| 67200007 | Call limit exceeded | Stop or wait according to official guidance |
| 67200008 | Authentication parameter missing in some legacy contracts | Do not expose key; compare current endpoint auth docs |
| 67200009 | Key/token mismatch in legacy flow | Fail closed; do not guess credentials |
| 67200100 | Service busy/timeout | Bounded retry for idempotent calls |
| 67200101 | Endpoint not found | Reverify current global path |
| 68300004 | Invalid parameter | Validate request against current schema |
| 68300005 | Search API failure | Preserve failure; retry only when appropriate |
| 68300006 | Access error | Check entitlement |
| 68300007 | Bad request | Fix schema; do not retry unchanged |
| 68300008 | Service error | Bounded retry for safe/idempotent call |
| 68300010 | File specification error | Validate upload/input contract |

The live page for each endpoint is authoritative. Codes and wording can vary by
API generation.

### 11.2 HTTP handling

| HTTP state | Action |
|---|---|
| 200/2xx | Still validate JSON envelope and required data |
| 400 | Validate request; do not retry unchanged |
| 401 | Stop and check private Bearer key |
| 403 | Stop and check entitlement/quota |
| 404 | Reverify global endpoint; do not fall back to a legacy domain |
| 408/429 | Retry only with bounded backoff and idempotency awareness |
| 5xx | Bounded retry; preserve final failure and partial evidence |
| Non-JSON | Record content type/status safely; do not parse as success |

### 11.3 Retry policy

Retry only transient, safe requests. Recommended behavior:

1. maximum retries from private configuration;
2. exponential backoff with jitter;
3. separate connect and read timeouts;
4. respect `Retry-After` when present;
5. no automatic duplicate asynchronous task submission;
6. record attempts and final sanitized error;
7. never log Authorization headers or full confidential prompts.

## 12. Pagination and limits

- Enforce endpoint-specific page and total limits.
- Validate non-negative `offset` and positive `limit`.
- Detect identical repeated pages.
- Stop when a page is shorter than the requested limit or documented total is
  reached.
- Reconcile requested, returned, deduplicated, retained, and family counts.
- Preserve every matching query ID on merged candidates.
- Do not silently drop results at `max_total` or `max_candidates`; state the
  truncation and selection method.

## 13. Language policy

Use English interface values and output in the international workflow:

- P070 `lang: ["en"]` unless additional languages are justified;
- English report labels and error messages;
- preserve source-language claims and identify working/official translations;
- do not remove meaningful spaces from English claim text;
- retain non-English terms only as evidence with an English explanation.

## 14. Security tests

The REST client must pass tests showing that:

- the key appears only in the in-memory Authorization header;
- `repr`, exceptions, logs, and output JSON do not contain the key;
- only HTTPS is accepted;
- redirects do not send Authorization to an unapproved host;
- report URLs are restricted to HTTP(S);
- dynamic HTML is escaped;
- local file URLs and user-profile paths are rejected;
- malformed JSON and oversized responses fail visibly;
- confidential prompts are not sent in dry-run mode.

## 15. Provenance record

For every REST operation record:

```json
{
  "provider": "PatSnap Open Platform",
  "mode": "rest",
  "endpoint": "/basic-patent-data/claim-data",
  "method": "GET",
  "request_reference": "REQ-CLAIM-009",
  "executed_at": "2026-08-07T09:30:00Z",
  "status": "success",
  "returned_identifiers": ["US11205304B2"],
  "limitations": []
}
```

Store a normalized/sanitized request or request hash when query confidentiality
requires it. Do not store the key or raw Authorization header.

## 16. MCP mapping for equivalent capabilities

REST endpoints remain the bundled runner's implementation. Agent environments
may instead use:

| Connector | Identifier / endpoint | Role |
|---|---|---|
| Patsnap Patent Research | `patsnap_patent_research` · `https://open.patsnap.com/marketplace/mcp-servers/patsnap-ip-searching` | End-to-end invention FTO task (`fto_review`, `get_task`) |
| Advanced Patent Search | `advanced_patent_search` · `https://open.patsnap.com/marketplace/mcp-servers/patent-search` | Query, semantic, classification, assignee, and similar-patent retrieval |
| Patent Briefing | `patent_briefing` · `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing` | Claims, translations, description, bibliography, family, status, and technical summary |
| Global Core Patents | Marketplace page `/core-patents` | Detailed legal-event, status, family, PDF, licensing, and citation research |

MCP tools have their own documented schemas. Do not translate REST endpoint
arguments into guessed MCP arguments. Normalize returned evidence only after a
real connector call under its current tool schema.

## 17. Pre-run checklist

- [ ] Correct target product/process and controlled version
- [ ] Target jurisdictions and relevant acts
- [ ] Search/status cutoffs and family convention
- [ ] Approved queries and any generated-query review
- [ ] Private config with placeholder replaced locally
- [ ] Global HTTPS base URL
- [ ] Required endpoint entitlements
- [ ] Output directory outside the skill package
- [ ] Confidential-data transmission authorized
- [ ] Dry-run reviewed

## 18. Post-run checklist

- [ ] Every call has sanitized provenance
- [ ] Counts and pagination reconcile
- [ ] Claim source/language/version is recorded
- [ ] P018 family replacement is disclosed
- [ ] Partial and failed steps remain visible
- [ ] AI conflicts remain visible
- [ ] Pending applications are separate
- [ ] Credentials and absolute personal paths are absent
- [ ] Report is labeled FTO screening
- [ ] Qualified local counsel review is required for material reliance

## 19. Boundary

These APIs provide patent data and AI-assisted workflow outputs. They do not
guarantee data completeness, current enforceability, correct claim
construction, infringement, validity, or freedom to operate. The screening
remains limited to the defined product/process, version, acts, jurisdictions,
claims, evidence, source coverage, and dates.
