# Canonical Report Payload

This file defines the strict JSON input accepted by `scripts/render_report.py`. Missing core fields, duplicate identifiers, unresolved references, unsafe URLs, count mismatches, or invalid dates are errors. The renderer does not silently substitute `Not provided` for a missing required key.

## Top-level structure

```json
{
  "schema_version": "2.0",
  "review_status": "reviewed",
  "meta": {},
  "requirement_text": "",
  "analysis": {},
  "issues": [],
  "directions": [],
  "evidence": [],
  "organizations": [],
  "search_log": [],
  "limitations": [],
  "review": {}
}
```

All keys are required. Arrays may be empty only when the report explicitly explains the gap.

## `meta`

```json
{
  "project_name": "Project name",
  "project_short_name": "Optional short name",
  "applicant_or_team": "Submitting organization or team",
  "report_date": "2026-08-07",
  "evidence_cutoff": "2026-06-30",
  "decision_context": "Decision the report supports",
  "scope": "Patents, scientific literature, standards, engineering cases, and reviewed web evidence",
  "geographies": ["Global"],
  "languages": ["English"],
  "patent_count_unit": "simple families",
  "time_zone": "Asia/Shanghai"
}
```

`project_name` and `applicant_or_team` may be empty strings when not provided; the report omits their metadata rows. Every other field is required and non-empty. Dates use `YYYY-MM-DD`.

## `requirement_text`

Store the authorized source requirement exactly enough for traceability. Do not add inferred facts. If the source contains confidential or personal information not approved for the report audience, store a reviewed redacted version and disclose that redaction in `limitations`.

## `analysis`

```json
{
  "demand": {
    "operating_context": "Source-grounded engineering or research context",
    "stakeholder_need": "Who needs the result and why",
    "technical_consequence": "Technical/safety/economic consequence supported by the source",
    "current_response": "Current workaround or baseline"
  },
  "bottleneck": {
    "performance_limit": "Observed or specified limit",
    "evidence": "Source location or evidence IDs",
    "tradeoffs": "Cost, complexity, performance, safety, or integration tradeoffs",
    "mechanistic_limit": "Physical, chemical, biological, algorithmic, or system reason"
  },
  "solution_hypothesis": {
    "technical_path": "Source-stated or clearly labeled analyst hypothesis",
    "system_concept": "Subsystem interactions and interfaces",
    "compatibility": "Integration, operation, maintenance, regulatory, or manufacturing constraints",
    "target_outcome": "Measurable target or decision criterion"
  }
}
```

Every nested key is required. Use the exact string `Not provided in the source requirement` when the source is silent. Do not confuse a desired target with achieved evidence.

## `issues`

```json
[
  {
    "id": "T1",
    "name": "Bounded technical issue",
    "description": "One source-faithful statement",
    "source_locations": ["requirement paragraph 2"],
    "dependencies": [],
    "confidence": "high"
  }
]
```

Issue IDs are `T1`, `T2`, and so on. IDs are unique. Issues should be mutually distinguishable, but real dependencies and overlaps are recorded rather than artificially erased.

## `directions`

```json
[
  {
    "id": "D1",
    "name": "Research direction",
    "issue_ids": ["T1"],
    "rationale": "Why this direction addresses the issue",
    "core_question": "Testable research question",
    "research_tasks": [
      {
        "id": "D1-R1",
        "text": "Specific research task",
        "evidence_ids": ["E1"],
        "validation_method": "Experiment, model, prototype, review, or benchmark",
        "success_metric": "Measurable criterion",
        "uncertainty": "Known uncertainty"
      }
    ],
    "target": "Technical target with units/basis where available",
    "deliverables": ["Expected evidence or artifact"],
    "evidence_ids": ["E1", "E2"],
    "evidence_gap": "What the current search did not establish",
    "confidence": "medium",
    "priority_basis": "Decision-linked rationale, not a hidden score"
  }
]
```

Direction IDs are `D1`, `D2`, and so on. Every issue must be covered by at least one direction or explicitly listed in a report limitation. The number of directions is governed by the user's scope and analytical separability, not mechanically equal to the number of issues.

Each research task must either cite evidence or state in `uncertainty` that it is an analyst-generated hypothesis requiring validation. A citation does not prove the recommended task will succeed.

## Unified `evidence` registry

All external evidence types use one global `E#` namespace. This resolves the source package's conflicting rules for A1 case/standard numbering.

```json
[
  {
    "id": "E1",
    "evidence_type": "patent",
    "title": "Evidence title",
    "source_name": "Database, publisher, standards body, institution, or site",
    "source_url": "https://example.org/record",
    "published_date": "2025-10-16",
    "accessed_date": "2026-06-30",
    "year": 2025,
    "language": "English",
    "organization_ids": ["O1"],
    "direction_ids": ["D1"],
    "summary": "Faithful evidence summary",
    "relevance": "Why it bears on the direction",
    "review_depth": "abstract",
    "review_status": "checked",
    "confidence": "medium",
    "patent": {},
    "paper": {},
    "standard_or_case": {},
    "web": {}
  }
]
```

Allowed `evidence_type` values:

- `patent`;
- `paper`;
- `standard`;
- `engineering_case`;
- `authoritative_web`.

Only the matching subtype object is populated; other subtype objects are empty.

### Patent subtype

```json
{
  "publication_number": "US20260000000A1",
  "jurisdiction": "US",
  "applicants": ["Example Applicant"],
  "assignees": [],
  "earliest_priority_date": "2024-01-15",
  "publication_date": "2026-03-19",
  "simple_family_id": "provider-family-id",
  "legal_status": "Source-returned label",
  "legal_status_as_of": "2026-06-30",
  "cited_by": null
}
```

`cited_by` is an integer or `null`; citation counts are source/date dependent and are not quality scores.

### Paper subtype

```json
{
  "authors": ["Author One"],
  "affiliations": ["Organization One"],
  "venue": "Journal or repository",
  "doi": "10.xxxx/example",
  "publication_type": "journal article",
  "peer_review_status": "peer reviewed",
  "cited_by": null
}
```

### Standard or engineering-case subtype

```json
{
  "publisher": "Standards body or project organization",
  "document_number": "Identifier",
  "status_or_stage": "Published, draft, operating, reported, or other source label",
  "location_or_system": "Relevant system or project context"
}
```

### Authoritative-web subtype

```json
{
  "publisher_type": "government, university, standards body, company, repository, or other",
  "content_category": "technical note, project record, guidance, dataset, or other"
}
```

`source_url` accepts an absolute HTTP(S) URL or an empty string. An empty URL renders as plain text, never a fake anchor.

## `organizations`

```json
[
  {
    "id": "O1",
    "name": "Normalized organization name",
    "aliases": ["Source alias"],
    "organization_type": "company, university, institute, standards body, or other",
    "direction_ids": ["D1"],
    "focus": "Evidence-backed technical focus",
    "evidence_ids": ["E1"],
    "representative_outputs": "Evidence-backed outputs",
    "confidence": "medium"
  }
]
```

Organization totals count unique normalized IDs across all accepted evidence. The report may show a reviewed subset, but it must not call that subset the total.

## `search_log`

```json
[
  {
    "id": "S1",
    "direction_id": "D1",
    "evidence_type": "patent",
    "source_or_tool": "PatSnap advanced_patent_search",
    "searched_at": "2026-06-30T10:30:00Z",
    "query": "Exact query",
    "filters": {},
    "languages": ["English"],
    "requested_limit": 100,
    "returned_count": 87,
    "reviewed_evidence_ids": ["E1"],
    "deduplication": "Simple family representative",
    "pagination_or_truncation": "One page reviewed",
    "limitations": "Publication lag and terminology recall"
  }
]
```

Requested, returned, reviewed, retained, and deduplicated counts remain distinct.

## `limitations`

Each entry is a non-empty string covering missing sources, search coverage, source quality, publication lag, language, jurisdiction, unavailable fields, unresolved technical assumptions, and specialist-review needs.

## `review`

```json
{
  "analyst": "Name or accountable role",
  "reviewer": "Independent reviewer or Not independently reviewed",
  "reviewed_on": "2026-08-07",
  "quality_status": "ready for review",
  "legal_boundary": "Not a patentability, FTO, infringement, validity, investment, or safety opinion"
}
```

## Derived report appendices and counts

The renderer derives:

- A1 standards and engineering cases;
- A2 papers;
- A3 patents;
- A4 authoritative web sources;
- evidence counts by type;
- unique organization total;
- organizations displayed;
- per-direction evidence counts;
- complete source register.

No `summary` or duplicated `appendix` object is accepted as authority. This removes divergence between embedded direction evidence, appendices, and totals.

## Referential-integrity rules

- Every `direction.issue_ids` resolves to an issue.
- Every issue is covered or explicitly disclosed as uncovered.
- Every evidence/organization/search direction ID resolves.
- Every direction/task/organization evidence ID resolves.
- Every subtype matches `evidence_type`.
- All IDs are globally unique within their namespace.
- Every `E#` is retained once in the unified registry.
- Evidence dates do not exceed the cutoff without an explicit limitation.
- The declared patent count unit is used consistently.

## Rendering and safety

All text is HTML-escaped. URLs are allowlisted. Markdown links are emitted only from validated URLs. Existing outputs require `--overwrite`. Symbolic-link targets and filesystem roots are refused. Validation fails before any output is written.
