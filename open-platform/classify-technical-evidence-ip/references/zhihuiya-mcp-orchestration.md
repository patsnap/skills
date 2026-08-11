# PatSnap MCP orchestration

The filename is retained to preserve the source package topology. Its content describes the global PatSnap Open Platform.

## Authorization precedes connectivity

Do not send a record, excerpt, identifier, or derived query to an MCP service merely because the connector is available.

1. Assess data sensitivity and license constraints.
2. Obtain authorization for the proposed external transmission.
3. Minimize the payload.
4. Prefer public publication numbers or normalized concepts when sufficient.
5. Record the authorization state and minimization method.
6. Never store credentials or a credential-bearing URL in provenance.

If transmission is not authorized, continue locally and record `mcp_enrichment_status: not_authorized`.

## Required execution matrix

Execute the minimum useful, authorized profile for the active workflow. A profile is required only when live enrichment is both permitted and available. Never hide an unexecuted capability.

| Phase | Capability profile | Minimum coverage |
|---|---|---|
| Scope and dimensions | Focused patent/literature retrieval plus classification, topic, domain, or terminology assistance | Main business concepts or representative records before the scope gate |
| Open coding | Keyword expansion and semantic search compared with keyword or classification-assisted retrieval | Each major source cluster or proposed top-level branch |
| Taxonomy construction | Technology topics, application domains, classification descriptions, and representative records | Every proposed top-level branch |
| Label definition | Technical problem/approach/benefit plus descriptions or claims; similar and adjacent records | Every label family and unstable boundary, with traceable positives and hard negatives where practical |
| Pilot | Local evidence plus selective description, claim, triad, topic, domain, or similar-record enrichment | Missing fields, incomplete records, hard negatives, and ambiguous cases |
| Boundary judgment | Similar records plus direct description/claim comparison | Unresolved adjacent-label or cross-dimensional conflicts |
| Full labeling | Selective record enrichment only | Missing evidence, low confidence, conflicts, or likely omissions; never every clear record mechanically |
| QA | Focused semantic, similar-record, classification, or distribution investigation | Unclassified clusters, unexpected distributions, and suspected omissions |

For non-patent data, select the closest literature, terminology, sample-retrieval, or domain-evidence capability. Do not force a patent tool onto an unsuitable data set.

## Verified global services

Verification date: 2026-08-07. Always copy the current connection URL from the official Connect panel.

### Advanced Patent Search

- Page: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Configuration key: `advanced_patent_search`
- Transport: `streamableHttp`
- Published Connect URL: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`
- Use: keyword assistance, semantic/field/nested searches, classification-assisted retrieval, assignee and patent-number searches, counts, and representative patent discovery.

### Deep Patent Mining

- Page: https://open.patsnap.com/marketplace/mcp-servers/patent-mining
- Configuration key: `deep_patent_mining`
- Transport: `streamableHttp`
- Published Connect URL: `https://open.patsnap.com/marketplace/mcp-servers/patent-mining`
- Relevant tools: `tech_problem_benefit_summary`, `technology_topic`, `classification_description`, and `application_domain`.
- The service also exposes `seic_classification`, but SEIC is China-specific. Do not make it a global labeling baseline unless the task explicitly concerns that Chinese classification system.

### Patent Briefing

- Page: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Configuration key: `patent_briefing`
- Transport: `streamableHttp`
- Published Connect URL: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- Use: claims, descriptions, bibliography, family, legal status, drawings, technical summaries, and direct verification of candidate examples.

### Scientific & Translational Evidence

- Page: https://open.patsnap.com/marketplace/mcp-servers/scientific-translational-evidence
- Use only when the labeling domain matches the service's published literature and translational-evidence scope.
- Copy the current generated connection details from the official page; do not infer or hard-code an unverified key or URL.

## Capability groups

- **Discovery:** keyword assistance, semantic search, classification assistance, counts, facets, and focused record retrieval.
- **Definition:** technology topics, application domains, classification descriptions, technical problem/approach/benefit, descriptions, claims, and representative records.
- **Boundary and examples:** similar patents, related literature, positive examples, adjacent labels, and high-similarity hard negatives.
- **Optional downstream validation:** legal status, family, applicant, and bibliographic data where relevant.

Select tools by published capability. A service name is not evidence that it supports an undocumented tool.

## Retrieval and judgment rules

1. Start from user-provided evidence and a representative subset.
2. Do not outsource business meaning to search.
3. Use retrieval for candidate recall and evidence discovery, not the final label decision.
4. Deduplicate identical queries and reuse permitted cached results.
5. Prefer representative branch coverage to a fixed number of calls.
6. Use similar-record comparison for boundary questions instead of repeatedly broadening keywords.
7. Keep retrieved concepts, candidate labels, and formal labels separate.
8. Do not promote a label merely because one retrieved record contains the term.
9. Distinguish source-language text, machine or working translation, and analyst interpretation.

## No-result and failure handling

- Retry once with a simpler normalized concept when a failure may be query-specific.
- Record successful calls with empty or overbroad results as `no_result` or `limited`.
- Continue through other useful capability groups when one tool is weak.
- If a connector is unavailable, use local evidence where possible and mark `mcp_enrichment_status: incomplete`.
- If transmission is not permitted, mark `not_authorized`.
- State the affected stage and capability.
- Never fabricate identifiers, records, counts, or evidence.

## Provenance schema

For every call, record:

`timestamp`, `stage`, `service`, `tool_or_capability`, `purpose`, `query_summary`, `record_or_label_id`, `returned_identifiers`, `status`, `notes`

Use `success`, `limited`, `no_result`, `not_authorized`, `unavailable`, or `error`.

Do not store API keys, authorization headers, bearer tokens, raw credential-bearing URLs, privileged text, or unnecessary personal data.

In QA, report MCP call count, enriched-record count, unresolved MCP-dependent review count, and overall enrichment completeness separately.
