# Zhihuiya MCP Orchestration

## Required execution matrix

Execute the minimum useful profile for the active workflow. Do not silently skip a required phase when the connector is available.

| Phase | Required capability profile | Minimum coverage |
|---|---|---|
| Scope and dimensions | Focused patent/literature retrieval plus classification, topic, domain, or terminology assistance | Cover the main business concepts or representative records before the scope gate when the goal is clear enough to search |
| Open coding | Keyword expansion and semantic search; compare with keyword or classification-assisted retrieval | Cover each major source cluster or proposed top-level branch |
| Taxonomy construction | Technology topics, application domains, classification descriptions, and representative records | Validate every proposed top-level branch |
| Label definition | Technical triads plus descriptions or claims; retrieve similar and adjacent records | Cover every label family and every unstable boundary; provide traceable positive and hard-negative examples where practical |
| Pilot | Local evidence plus selective description, claim, triad, topic, domain, or similar-record enrichment | Enrich missing fields, incomplete records, hard negatives, and ambiguous cases |
| Boundary judgment | Similar patents or literature plus direct description/claim comparison | Required for unresolved adjacent-label or cross-dimensional conflicts |
| Full labeling | Selective record enrichment only | Call MCP only for missing evidence, low confidence, conflicts, or likely omissions; never call every clear record mechanically |
| QA | Focused semantic, similar-record, classification, or distribution investigation | Investigate unclassified clusters, unexpected distributions, and suspected omissions |

For non-patent datasets, substitute the closest patent/literature, terminology, sample-retrieval, or domain-evidence capabilities.

## Capability groups

- **Discovery**: keyword assistance, semantic search, classification assistance, counts, facets, and focused record retrieval.
- **Definition**: technology topics, application domains, classification descriptions, technical problem/approach/benefit summaries, descriptions, claims, and representative records.
- **Boundary and examples**: similar patents, related literature, positive examples, adjacent labels, and high-similarity negatives.
- **Optional downstream validation**: legal status, core patent data, applicant data, family data, and landscape analytics.

Select tools by capability rather than hard-coding endpoint names. Use available Zhihuiya/PatSnap MCP tools that provide the required capability.

## Retrieval and judgment rules

1. Start with user-provided evidence and a representative subset; do not outsource business meaning to search.
2. Use search for candidate recall and evidence discovery, never as the final label decision.
3. Deduplicate identical queries and reuse cached results.
4. Prefer representative branch coverage over a fixed number of calls.
5. Use similar-record comparison for boundary questions instead of repeatedly broadening keywords.
6. Keep retrieved concepts, candidate labels, and formal labels separate.
7. Do not promote a label only because one retrieved record contains the term.

## No-result and failure handling

- Retry once with a simpler or normalized concept when the failure may be query-specific.
- Record successful calls with empty or overbroad results as `no_result` or `limited`; do not hide them.
- Continue through other required capability groups when one tool is weak.
- If the connector or a required capability is unavailable, continue from local evidence where possible and mark `mcp_enrichment_status: incomplete`.
- State which phase and capability were not executed. Never fabricate retrieved identifiers or evidence.

## Provenance requirements

For every call, record:

`timestamp`, `stage`, `service`, `tool_or_capability`, `purpose`, `query_summary`, `record_or_label_id`, `returned_identifiers`, `status`, `notes`

Use statuses such as `success`, `limited`, `no_result`, `unavailable`, or `error`. Do not store credentials, authorization headers, or raw credential-bearing URLs.

In QA, separately report MCP call count, enriched-record count, unresolved MCP-dependent review count, and overall enrichment completeness.
