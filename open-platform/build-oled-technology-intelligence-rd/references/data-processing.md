# Portal Data Processing and Validation

Use this reference before rendering. The renderer accepts one valid UTF-8 JSON object; it does not recover concatenated JSON objects by skipping malformed characters.

## Processing stages

1. ingest authorized source records;
2. preserve provenance and original values;
3. validate schema and required fields;
4. normalize dates, URLs, entities, taxonomy IDs, and text;
5. deduplicate under declared rules;
6. link records to organizations and routes;
7. review classifications and analyst fields;
8. calculate statistics from accepted records;
9. retain rejection counts and reasons;
10. render escaped values into safe local pages.

## Root contract

```json
{
  "review_status": "reviewed",
  "portal": {
    "title": "OLED Technology Intelligence Portal",
    "technology_domain": "Organic light-emitting diode displays",
    "scope": "Defined inclusion and exclusion boundary",
    "decision_context": "R&D route and monitoring decisions",
    "geographies": ["Global"],
    "languages": ["English"],
    "period_start": "2025-01-01",
    "period_end": "2026-06-30",
    "evidence_cutoff": "2026-06-30",
    "generated_on": "2026-08-07",
    "analyst": "Technology Intelligence Team",
    "confidentiality": "Internal",
    "methodology": "Reviewed source and search method",
    "limitations": "Known evidence and coverage limits",
    "patent_count_unit": "simple families"
  },
  "executive_findings": [],
  "companies": [],
  "technologies": [],
  "records": [],
  "events": [],
  "publications": [],
  "patents": [],
  "search_log": [],
  "rejections": []
}
```

All arrays are required but may be empty. Empty arrays render honest empty states.

## Common evidence record

Current-awareness, news, web, company, product, and policy records use:

```json
{
  "id": "E001",
  "title": "Reviewed record title",
  "record_type": "news",
  "source_name": "Publisher or database",
  "source_url": "https://example.org/record",
  "published_date": "2026-04-15",
  "event_date": "2026-04-14",
  "accessed_date": "2026-06-30",
  "language": "English",
  "summary": "Faithful evidence summary.",
  "company_ids": ["example-company"],
  "technology_ids": ["tandem-oled"],
  "evidence_type": "source fact",
  "review_status": "checked",
  "confidence": "medium",
  "analyst_note": "Limitation or interpretation.",
  "content_hash": "optional-source-hash"
}
```

Allowed `record_type` values may include `news`, `company`, `product`, `market`, `policy`, `standard`, `conference`, `investment`, and `other`. Define additions explicitly.

## Event record

Events are decision-relevant dated records, not automatically every news item:

```json
{
  "id": "EV001",
  "title": "Material event",
  "event_date": "2026-04-14",
  "source_ids": ["E001", "E002"],
  "company_ids": ["example-company"],
  "technology_ids": ["tandem-oled"],
  "observed_fact": "What the evidence establishes.",
  "analyst_inference": "Explicitly labeled interpretation.",
  "decision_relevance": "Why it matters to the scoped decision.",
  "confidence": "medium",
  "review_status": "corroborated"
}
```

## Scientific publication record

```json
{
  "id": "L001",
  "title": "Publication title",
  "authors": ["Author One", "Author Two"],
  "venue": "Journal or repository",
  "doi": "10.xxxx/example",
  "source_url": "https://doi.org/10.xxxx/example",
  "published_date": "2026-02-10",
  "abstract_summary": "Reviewed technical summary.",
  "company_ids": [],
  "technology_ids": ["oled-emissive-materials"],
  "review_status": "checked",
  "confidence": "high"
}
```

## Patent record

```json
{
  "id": "P001",
  "publication_number": "US20260000000A1",
  "title": "Patent publication title",
  "jurisdiction": "US",
  "applicants": ["Example Applicant"],
  "assignees": [],
  "earliest_priority_date": "2024-01-15",
  "publication_date": "2026-03-19",
  "simple_family_id": "provider-family-id",
  "extended_family_id": "optional-provider-family-id",
  "legal_status": "As returned by the reviewed source",
  "legal_status_as_of": "2026-06-30",
  "abstract_summary": "Reviewed technical summary.",
  "relevance_note": "Why the record is in scope.",
  "company_ids": ["example-company"],
  "technology_ids": ["tandem-oled"],
  "source_url": "https://example.org/global-patent-record",
  "review_depth": "abstract",
  "review_status": "checked",
  "confidence": "medium"
}
```

Legal status is time-sensitive and jurisdiction-specific. Do not translate provider labels into a different legal conclusion.

## Search-log record

```json
{
  "id": "S001",
  "source_or_tool": "PatSnap advanced_patent_search",
  "searched_at": "2026-06-30T10:30:00Z",
  "query": "Exact query text",
  "filters": {"jurisdictions": ["US", "EP", "WO"]},
  "languages": ["English"],
  "requested_limit": 100,
  "returned_count": 87,
  "reviewed_ids": ["P001"],
  "pagination_or_truncation": "One page reviewed",
  "deduplication": "Simple family representative",
  "limitations": "Publication lag and language recall"
}
```

## JSON ingestion

Reject:

- concatenated JSON objects;
- trailing non-JSON content;
- invalid UTF-8;
- duplicate object keys when detectable;
- non-object root values;
- unknown required-reference IDs;
- raw HTML fields;
- control characters not valid in JSON strings.

Return the exact path or array index of an invalid record. Do not advance one character at a time after a decode error; that can silently invent a partial dataset.

## Date normalization

Use ISO 8601 dates. Preserve the source value separately during preprocessing when conversion is ambiguous. Do not infer day/month order. Unix timestamps require an explicit unit and time zone; use UTC when the source defines UTC, otherwise retain the uncertainty.

Distinguish:

- publication date;
- event date;
- earliest priority date;
- filing date;
- access date;
- legal-status `as of` date;
- portal evidence cutoff.

## URL handling

Accept only `https` or, when explicitly allowed, `http`. Reject `javascript`, `data`, `file`, local user paths, protocol-relative URLs, and embedded credentials. When absent or rejected, render plain text `Source link not supplied`.

Canonicalization for deduplication may remove tracking parameters only under a documented rule. Preserve the reviewed source URL for citation.

## Text normalization

- Normalize line endings and surrounding whitespace.
- Preserve meaningful capitalization, chemical notation, symbols, and acronyms.
- Do not transliterate names without retaining the source form in preprocessing.
- Limit display excerpts by characters without breaking HTML because rendering occurs after escaping.
- Do not strip qualifiers such as `planned`, `reported`, `estimated`, or `not demonstrated`.

## Deduplication

### Current-awareness records

Prefer stable provider IDs. Otherwise compare canonical URL, title, publisher, and date. Syndicated articles may be distinct sources supporting one event; link them to one event rather than deleting corroboration.

### Patents

Choose the unit before counting:

- publications for publication-level monitoring;
- applications/grants for procedure-specific questions;
- simple families for invention-level trend summaries;
- extended families only when the analysis defines why.

Keep all publication records available even when a family representative is used for counts.

### Organizations and routes

Use stable IDs and reviewed aliases. Never merge on acronym or substring alone.

## Classification

Automated term or semantic matching proposes company/technology associations. A reviewed portal must store the matching basis and confidence. Ambiguous records remain `unclassified` or `manual review`; they are not forced into the nearest page.

## Calculated statistics

The renderer calculates:

- accepted current-awareness record count;
- event count;
- publication count;
- patent count under the declared unit;
- monitored company count;
- technology-route count;
- reviewed/unreviewed counts;
- records inside/outside the stated period;
- rejected-record count.

Do not accept a supplied `stats` object as authority. Reconcile page counts against accepted arrays.

## Safe output behavior

- Escape all text and attribute values.
- Allowlist URLs.
- Generate safe, unique slugs from stable IDs.
- Reject path traversal and reserved filenames.
- Write only known portal pages.
- Refuse a non-empty output directory unless `--overwrite` is supplied.
- With overwrite, replace only the generator's known page set and never recursively delete the directory.
- Create no cache or temporary file inside the package.

## Rejection log

Each rejected record includes source location, record identifier if available, reason, reviewer/process, and whether it can be corrected. Report rejection totals in methodology; do not silently reduce counts.

## Final validation

Confirm referential integrity, date/period consistency, duplicate IDs, slug uniqueness, local page links, genuine external URLs, count units, evidence-linked findings, escaped content, and explicit limitations before publication.
