# Claim Chart JSON Schema

Version: 2.0 localized international edition

## 1. Purpose

`claim_chart.json` is the traceable handoff between patent/claim retrieval,
product-feature analysis, optional AI assistance, and HTML/DOCX report
generation. It preserves the source package's comparison structure while
adding the evidence, jurisdiction, version, and review controls required for an
international screening workflow.

The schema supports screening-level analysis. It does not itself establish
claim construction, infringement, validity, enforceability, or freedom to
operate.

## 2. File origin and provenance

The file may be produced from:

1. the bundled REST runner using P002/P018 and optional AI07 results; or
2. normalized evidence retrieved through approved PatSnap MCP connectors.

Every run must state one primary acquisition mode. Imported MCP results retain
connector, tool, request, task ID, and retrieval date. The Python scripts do not
claim that they called an MCP connector.

## 3. Top-level object

```json
{
  "schema_version": "2.0",
  "project": {},
  "run_provenance": {},
  "comparisons": [],
  "pending_application_watchlist": [],
  "errors": [],
  "limitations": [],
  "review": {}
}
```

| Field | Type | Required | Description |
|---|---|---:|---|
| `schema_version` | string | Yes | Exact schema version, currently `2.0` |
| `project` | object | Yes | Subject, version, acts, jurisdictions, and cutoffs |
| `run_provenance` | object | Yes | REST or MCP mode and execution evidence |
| `comparisons` | array | Yes | One `PatentComparisonResult` per assessed patent/claim group |
| `pending_application_watchlist` | array | Yes | Pending rights tracked separately from enforceable-right screening |
| `errors` | array | Yes | Step-specific errors retained without converting them to negative findings |
| `limitations` | array | Yes | Search, claim, status, translation, product-evidence, and legal limits |
| `review` | object | Yes | Human-review status and decision boundary |

## 4. `project` object

```json
{
  "project_name": "Example controller launch screening",
  "product_name": "Laboratory pump controller",
  "product_version": "Hardware C / firmware 3.2",
  "target_jurisdictions": ["US"],
  "relevant_acts": ["import", "offer for sale", "sell", "use"],
  "search_cutoff": "2026-07-31",
  "status_cutoff": "2026-07-31",
  "family_counting_convention": "simple family",
  "decision_context": "commercial launch gate"
}
```

All decision-material fields are required. An empty value must remain explicit
and must generate a missing-evidence issue in the report.

## 5. `run_provenance` object

| Field | Type | Required | Description |
|---|---|---:|---|
| `mode` | string | Yes | `rest`, `mcp_import`, or `dry_run` |
| `provider` | string | Yes | `PatSnap Open Platform` or connector name |
| `tools_or_endpoints` | array | Yes | Endpoint paths or MCP tool names actually used |
| `started_at` | string | Yes | ISO 8601 timestamp |
| `completed_at` | string/null | Yes | ISO 8601 timestamp or null for incomplete run |
| `request_ids` | array | Yes | Non-secret request/task IDs |
| `source_files` | array | Yes | Input risk document and query file references |
| `status` | string | Yes | `complete`, `partial`, `failed`, or `dry_run` |
| `notes` | array | Yes | Mode changes, retries, unavailable services, and evidence caveats |

Never include API keys, Authorization headers, cookies, access tokens, local
user profile paths, or confidential input text not required for traceability.

## 6. `PatentComparisonResult`

```json
{
  "patent_id": "718ead9c-4f3c-4674-8f5a-24e126827269",
  "publication_number": "US11205304B2",
  "application_number": "US16/123456",
  "grant_number": "US11205304B2",
  "authority": "US",
  "family_key": "FAM-001",
  "title": "Example controller patent",
  "applicant_or_owner": "Example Controls Inc.",
  "legal_status": {},
  "claim_source": {},
  "claims_assessed": [],
  "features_comparison": [],
  "conclusion": {},
  "provenance": {},
  "review": {}
}
```

| Field | Type | Required | Description |
|---|---|---:|---|
| `patent_id` | string | No | PatSnap UUID when returned |
| `publication_number` | string | Yes | Normalized publication identifier with authority/kind code where available |
| `application_number` | string | No | Application identifier, never substituted for publication number silently |
| `grant_number` | string | No | Granted-right identifier where applicable |
| `authority` | string | Yes | Target patent authority |
| `family_key` | string | Yes | Key under the stated family convention |
| `title` | string | Yes | Patent title; not a basis for claim mapping |
| `applicant_or_owner` | string | No | Dated applicant/owner evidence where material |
| `legal_status` | object | Yes | Value, source, evidence date, and qualification |
| `claim_source` | object | Yes | Language, version, source, retrieval date, and replacement behavior |
| `claims_assessed` | array | Yes | Independent and relevant dependent claim identifiers |
| `features_comparison` | array | Yes | Limitation-level structured analysis |
| `conclusion` | object | Yes | Screening concern, rationale, confidence, and boundaries |
| `provenance` | object | Yes | Matching queries, provider/tool/endpoint, and request references |
| `review` | object | Yes | Human-review and conflict disposition |

## 7. `legal_status` object

```json
{
  "normalized_status": "Active — verify in official register",
  "raw_status": "1",
  "source": "PatSnap P002",
  "status_as_of": "2026-07-31",
  "official_register_checked": false,
  "notes": ["SIMPLE_LEGAL_STATUS is a screening filter, not proof of enforceability."]
}
```

Status must never be represented as a timeless Boolean `valid` value.

## 8. `claim_source` object

| Field | Type | Required | Description |
|---|---|---:|---|
| `source` | string | Yes | P018, Patent Briefing, official file, or another named source |
| `retrieved_at` | string | Yes | ISO 8601 timestamp |
| `language` | string | Yes | Source claim language |
| `translation_source` | string/null | Yes | Official, provider, working translation, or null |
| `claim_version` | string | Yes | Granted, published, amended date/version, or explicitly unknown |
| `related_family_replacement` | boolean | Yes | Whether another family member supplied missing claims |
| `replacement_patent` | string/null | Yes | Identifier if replacement occurred |
| `raw_evidence_reference` | string | Yes | Stable run-local reference, not an embedded secret/path |

Family replacement must be visible because another member's claims may differ.

## 9. `claims_assessed` elements

```json
{
  "claim_number": "1",
  "claim_type": "independent",
  "claim_text": "A controller comprising ...",
  "selection_reason": "Minimum source workflow and potentially material scope",
  "assessment_status": "reviewed"
}
```

Allowed `assessment_status` values are `reviewed`, `partial`, `missing`, and
`not_selected`. Claim 1 is the source workflow minimum; other material
independent and dependent claims must be added when required by the evidence.

## 10. `features_comparison` elements

```json
{
  "claim_number": "1",
  "limitation_id": "1.a",
  "claim_limitation": "a processor configured to ...",
  "product_feature": "Firmware module F-14 ...",
  "product_evidence": {
    "reference": "SYS-SPEC-032 section 4.2",
    "version": "3.2",
    "date": "2026-07-25"
  },
  "literal_mapping": "uncertain",
  "literal_rationale": "The supplied specification does not identify where the transformation executes.",
  "equivalents_assessment": "not_assessed",
  "equivalents_rationale": "Requires jurisdiction-specific counsel review after the product fact is confirmed.",
  "contrary_evidence": [],
  "missing_information": ["Execution-location evidence"],
  "confidence": "moderate",
  "source": "structured reviewer comparison"
}
```

### Required fields

| Field | Type | Values / rule |
|---|---|---|
| `claim_number` | string | Claim containing the limitation |
| `limitation_id` | string | Stable within the comparison |
| `claim_limitation` | string | Source-faithful limitation text |
| `product_feature` | string | Feature or `Not identified` |
| `product_evidence` | object | Reference, version, and date |
| `literal_mapping` | string | `mapped`, `not_mapped`, `uncertain`, `not_assessed` |
| `literal_rationale` | string | Evidence-based explanation |
| `equivalents_assessment` | string | `potentially_equivalent`, `not_equivalent`, `uncertain`, `not_applicable`, `not_assessed` |
| `equivalents_rationale` | string | Jurisdiction-qualified explanation |
| `contrary_evidence` | array | Evidence or interpretations against the provisional position |
| `missing_information` | array | Facts needed to resolve uncertainty |
| `confidence` | string | `high`, `moderate`, or `low` |
| `source` | string | Human reviewer, AI-assisted, or another named source |

Do not use a single `Y/N` field for both literal mapping and equivalents.

## 11. `conclusion` object

```json
{
  "screening_concern": "moderate",
  "label": "Moderate screening concern",
  "basis": "One limitation remains uncertain under the supplied product evidence.",
  "confidence": "moderate",
  "material_claims_reviewed": ["1"],
  "claims_not_reviewed": ["8"],
  "status_qualification": "Status evidence is current to 2026-07-31 and requires official-register confirmation.",
  "recommended_actions": ["Confirm execution location", "Obtain US counsel review"],
  "legal_boundary": "Screening result only; not a legal opinion or FTO guarantee."
}
```

Allowed concern values are `higher`, `moderate`, `lower`, `pending_watchlist`,
and `not_assessed`. A pending application cannot be labeled as a currently
enforceable higher-risk claim solely because its pending claim text maps.

## 12. `provenance` object

```json
{
  "matching_query_ids": ["Q-001", "Q-004"],
  "retrieval_mode": "rest",
  "provider": "PatSnap Open Platform",
  "tools_or_endpoints": [
    "/search/patent/query-search-patent/v2",
    "/basic-patent-data/claim-data"
  ],
  "request_ids": ["REQ-SEARCH-001", "REQ-CLAIM-009"],
  "retrieved_at": "2026-08-07T09:30:00Z"
}
```

For MCP imports, use connector and tool names and preserve task IDs. Do not
invent a request ID when the service does not provide one; use a run-local
evidence record ID and label it accordingly.

## 13. `review` object

| Field | Type | Required | Description |
|---|---|---:|---|
| `ai_assistance_used` | boolean | Yes | Whether AI07 or another model assisted |
| `ai_output_reference` | string/null | Yes | Run-local raw-output reference |
| `ai_conflicts` | array | Yes | Conflicts with claims, product facts, or structured mapping |
| `human_review_status` | string | Yes | `not_reviewed`, `reviewed`, or `approved` |
| `reviewer_role` | string | Yes | Role, not personal data unless required |
| `reviewed_at` | string/null | Yes | ISO 8601 date/time |
| `disposition` | string | Yes | How conflicts and missing facts were handled |

## 14. Pending-application watchlist

```json
{
  "publication_number": "US20240123456A1",
  "authority": "US",
  "family_key": "FAM-014",
  "procedural_status": "Pending",
  "status_as_of": "2026-07-31",
  "claims_or_features_to_monitor": ["Independent claim 1"],
  "trigger": "Notice of allowance or material amendment",
  "owner": "IP operations",
  "cadence": "Quarterly and event-driven"
}
```

## 15. Error object

```json
{
  "step": "claim_retrieval",
  "patent_or_query": "US11205304B2",
  "error_type": "permission_error",
  "message": "P018 access was not authorized for this key.",
  "retryable": false,
  "effect": "Claim comparison not assessed",
  "recorded_at": "2026-08-07T09:35:00Z"
}
```

Error messages must be useful but must not contain credentials, Authorization
headers, full confidential input text, or local absolute paths.

## 16. Complete example

```json
{
  "schema_version": "2.0",
  "project": {
    "project_name": "Example controller launch screening",
    "product_name": "Laboratory pump controller",
    "product_version": "Hardware C / firmware 3.2",
    "target_jurisdictions": ["US"],
    "relevant_acts": ["import", "sell", "use"],
    "search_cutoff": "2026-07-31",
    "status_cutoff": "2026-07-31",
    "family_counting_convention": "simple family",
    "decision_context": "launch gate"
  },
  "run_provenance": {
    "mode": "rest",
    "provider": "PatSnap Open Platform",
    "tools_or_endpoints": ["P002", "P018"],
    "started_at": "2026-08-07T09:00:00Z",
    "completed_at": "2026-08-07T09:40:00Z",
    "request_ids": [],
    "source_files": ["risk_points.docx", "queries.json"],
    "status": "partial",
    "notes": ["One dependent claim remains unreviewed."]
  },
  "comparisons": [],
  "pending_application_watchlist": [],
  "errors": [],
  "limitations": [
    "Unpublished applications cannot be observed.",
    "The screening does not establish complete recall."
  ],
  "review": {
    "human_review_status": "not_reviewed",
    "reviewer_role": "qualified patent reviewer required",
    "reviewed_at": null,
    "decision_boundary": "Not for decision reliance until reviewed."
  }
}
```

## 17. Validation rules

1. `schema_version` equals `2.0`.
2. Required project fields exist, even when visibly empty.
3. Every comparison has a publication number, authority, family key, status
   object, claim source, claim list, feature list, conclusion, and provenance.
4. Every feature comparison identifies a claim and stable limitation ID.
5. Literal and equivalents assessments are separate.
6. Every product mapping cites versioned evidence or states it is missing.
7. Every conclusion lists reviewed and unreviewed material claims.
8. Pending applications are not mixed into enforceable-right risk lists.
9. Partial/failed steps appear in `errors` and affect report status.
10. AI conflicts remain visible until human disposition.
11. URLs are HTTP(S)-only and credentials are absent.
12. The report renderer escapes every dynamic value.

## 18. Boundary

The schema organizes screening evidence. It does not determine the legal scope
of a claim, whether a product infringes, whether a patent is valid/enforceable,
or whether the user has freedom to operate. Those questions require complete
evidence and qualified jurisdiction-specific legal review.
