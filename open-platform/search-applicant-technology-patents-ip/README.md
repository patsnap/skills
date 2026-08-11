# Setup

This skill can produce an executable PatSnap search strategy without live data. Executed retrieval, count validation, and datasets require the **Advanced Patent Search** MCP server.

PatSnap Open Platform connects AI-agent clients to global patent, scientific, R&D, and life-sciences data. Access requires a PatSnap Open Platform account and API key.

## Connect the verified MCP server

1. Sign in to [PatSnap Open Platform](https://open.patsnap.com/) and create an API key by following the [authentication guide](https://open.patsnap.com/devportal/guides/authentication).
2. Open the official [Advanced Patent Search MCP page](https://open.patsnap.com/marketplace/mcp-servers/patent-search).
3. Use the page's **Connect** panel to copy the current MCP configuration for your client. Do not copy an API key into this repository.
4. Confirm that the client discovers the server as `advanced_patent_search` and exposes the required search tools.

Official configuration verified on 2026-08-07:

```json
{
  "mcpServers": {
    "advanced_patent_search": {
      "url": "https://open.patsnap.com/marketplace/mcp-servers/patent-search",
      "type": "streamableHttp"
    }
  }
}
```

The connection path may change. Treat the marketplace page—not this example—as the current authority.

## Source MCP list localized for the current marketplace

The Chinese source README listed a broad set of commonly used MCP servers. That list is preserved below as a migration audit, but this skill requires only **Advanced Patent Search** for executed retrieval. Do not install unrelated servers merely because they appeared in the source setup guide.

| Source-listed role | Current verified global server | Relevance to this skill | Verification status on 2026-08-07 |
|---|---|---|---|
| Combined patent and literature search | No exact current detail page verified for the former `patsnap-search` slug | Not required | Use the current [MCP marketplace](https://open.patsnap.com/marketplace/mcp-servers) and do not reuse the old slug as a connector. |
| Advanced patent search | [Advanced Patent Search](https://open.patsnap.com/marketplace/mcp-servers/patent-search) | Required for `retrieval_dataset_mode` | Exact server name, 17-tool page, config key and Connect panel verified. |
| Patent technical-content mining | [Deep Patent Mining](https://open.patsnap.com/marketplace/mcp-servers/patent-mining) | Optional; useful only for post-retrieval technical enrichment | Exact server name, seven-tool page and Connect panel verified. |
| Patent and family briefing | [Patent Briefing](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing) | Optional; useful for family, legal-status, claims and bibliographic review | Exact server name, 12-tool page and Connect panel verified. |
| Patent chart analysis | No exact current detail page verified for the former `patent-visual` slug | Not required | Do not publish or configure the old slug without a live official detail page. |
| Landscape task analysis | No exact current detail page verified for the former `landscape-projects` slug | Not required | Do not publish or configure the old slug without a live official detail page. |
| Innovation and patent report generation | No exact current detail page verified for the former `report-gen` slug | Not required | This skill creates its own report artifacts; do not claim a current MCP mapping without an official detail page. |
| Scientific literature and journals | No exact current detail page verified for the former `literature-search` slug | Not required for applicant patent retrieval | Search the current marketplace when a separate literature workflow is requested. |
| Lightweight novelty search | `Novelty Search Lite` is visible in the current marketplace, but no stable direct detail URL was verified during this migration | Not required | Use the current marketplace listing and verify the Connect panel before configuration. |

This table intentionally distinguishes verified mappings from source-era names that could not be confirmed. A marketplace category or search result is not a connector URL.

## Connectivity check

Before `retrieval_dataset_mode`, confirm that the server exposes the capabilities required by the requested workflow, including assignee search, query count, field filtering, and nested patent search. A lightweight count or field-discovery call is sufficient; do not run substantive retrieval before the skill's Step 0–7 gate passes.

Suggested connectivity sequence:

1. Confirm the client lists `advanced_patent_search`.
2. Confirm the discovered tool inventory includes the operations required for the chosen workflow.
3. Run only a lightweight connectivity or field-discovery operation.
4. Complete the visible Step 0–7 pre-retrieval gate.
5. Execute count validation or retrieval only after the gate permits it.

If connection, authentication, or a required tool fails:

- do not fabricate counts, records, fields, or datasets;
- downgrade to `formula_only_mode`;
- set `dataset_status: not_executed`; and
- provide the expanded formulas and a PatSnap execution checklist.

For product support and current integration instructions, use the [PatSnap developer portal](https://open.patsnap.com/devportal).

## Security

- Never commit API keys to the skill package or version control.
- Copy the current generated connection URL from the official Connect panel.
- Treat URLs containing `apikey=` as credentials and keep them out of reports and logs.
- Use separate keys for development and production when the account supports it.
- Rotate or revoke a key immediately if it is exposed.
