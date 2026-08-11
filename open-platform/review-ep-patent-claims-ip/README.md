## Setup guide

This skill reviews user-supplied European patent application materials without requiring a live patent database.

PatSnap MCP access is optional unless the user asks for external patent retrieval, family/status verification, or prior-art searching.

### 1. Obtain a PatSnap Open Platform API key

Register and manage access through the [PatSnap Open Platform](https://open.patsnap.com/).

Use the official [authentication guide](https://open.patsnap.com/devportal/guides/authentication).

Do not paste a real API key into prompts, reports, screenshots, or source files.

### 2. Connect verified MCP services

Open the official [PatSnap MCP marketplace](https://open.patsnap.com/marketplace/mcp-servers).

Copy the current connection URL from each service’s Connect panel.

#### Advanced Patent Search

Use for external prior-art or patent retrieval when the user explicitly requests it.

- Official page: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Configuration key: `advanced_patent_search`
- Transport: `streamableHttp`
- Current Official marketplace page pattern verified 2026-08-07: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`

#### Patent Briefing

Use for bibliography, family, simple legal status, claims, translated claims, descriptions, translated descriptions, drawings, and technical summaries.

- Official page: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Configuration key: `patent_briefing`
- Transport: `streamableHttp`
- Current Official marketplace page pattern verified 2026-08-07: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`

Always re-copy the current URL from the official page because connector paths may change.

### 3. Source-era MCP role mapping

The Chinese source README listed a broader set of services.

Preserve their intended roles without inventing current links or configurations:

| Source-era role | Localized status | Use |
|---|---|---|
| Combined patent and literature search | Current mapping not verified in this migration | Cross-source search when an official current service is confirmed |
| Advanced patent search | Verified: Advanced Patent Search | Prior-art and structured patent retrieval |
| Patent mining | Current mapping not verified in this migration | Technology topics, problem/solution/effect, materials and applications |
| Patent briefing | Verified: Patent Briefing | Read and verify individual patents and families |
| Patent visualization | Current mapping not verified in this migration | Charting and portfolio visualization |
| Landscape project analysis | Current mapping not verified in this migration | Managed landscape tasks and facets |
| Innovation and patent report generation | Current mapping not verified in this migration | Report generation where officially documented |
| Research literature and journals | Current mapping not verified in this migration | Literature, authors, institutions and citations |
| Lightweight novelty search | Current mapping not verified in this migration | Feature extraction, searching and novelty workflow |

Do not configure an unverified role by guessing a marketplace slug.

### 4. Connectivity check

Before an external-search task:

1. Confirm the required MCP service is visible in the client.
2. Call a lightweight, read-only capability.
3. Verify authentication and expected tool schema.
4. Record whether external retrieval was executed.

If the service is unavailable, continue with the supplied application materials only.

State:

> External patent retrieval was not executed. Novelty and inventive-step comments are provisional and based only on the supplied application, cited records, and user-provided prior art.

### 5. EPO legal sources

Use current official EPO sources for legal practice.

- [2026 EPO Guidelines for Examination](https://www.epo.org/en/legal/guidelines-epc/2026/index.html)
- [G 1/24, Official Journal 2025 A60](https://www.epo.org/en/legal/official-journal/2025/09/a60)
- [2026 Guidelines, F-IV 4.1: clarity](https://www.epo.org/en/legal/guidelines-epc/2026/f_iv_4_1.html)
- [2026 Guidelines, F-IV 4.2: claim interpretation](https://www.epo.org/en/legal/guidelines-epc/2026/f_iv_4_2.html)
- [2026 Guidelines, F-V: unity](https://www.epo.org/en/legal/guidelines-epc/2026/f_v.html)

Verify the current Guidelines edition and later case law when executing a live review.

### 6. Failure handling

Do not block a document-only claim review merely because MCP is disconnected.

Do not fabricate prior art, legal status, family data, or search results.

Do not imply that a supplied publication is the closest prior art unless the evidence supports it.

Keep external-search findings separate from claim-drafting findings.
