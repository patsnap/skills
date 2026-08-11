# Setup guide

This skill analyzes a prepared, screened, and tagged patent dataset. A live MCP connection is optional when the user already supplies complete validated data.

## 1. Prepare the input

Preferred suite artifacts:

1. `search-patents-ip` — search results and search manifest;
2. `analyze-patent-search-results-ip` — reproducible statistics;
3. human Stage 3.5 — screening decisions;
4. `tag-patent-search-results-ip` — tagged records, tag dictionary, and tagging manifest.

Equivalent data is acceptable when it includes query scope, screening rules, tag semantics/version, counting level, family/deduplication rule, entity normalization, date field/range, missingness, coverage, and evidence cutoff.

Without a validated tagged dataset, the skill can provide a framework and data-readiness assessment, but it must not present an executed competitive analysis.

## 2. PatSnap global MCP services

Open the [PatSnap MCP marketplace](https://open.patsnap.com/marketplace/mcp-servers), sign in, open the required service page, and copy the current connection URL from its Connect panel. Keep the actual API key secret and outside report files.

### Advanced Patent Search

Use when patent retrieval, query refinement, assignee validation, counts, or dataset extension must be executed.

- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Configuration key: `advanced_patent_search`
- Transport: `streamableHttp`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`
- Requirement: Required only for live retrieval/validation; not required for supplied complete data.

### Patent Briefing

Use to verify selected patents through bibliography, family, legal status, claims, description, translations, and images.

- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Configuration key: `patent_briefing`
- Transport: `streamableHttp`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- Requirement: Recommended for representative-record verification.

### Deep Patent Mining

Use to validate or enrich technical topics, technical problem/means/effect, classifications, materials, and applications.

- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-mining
- Configuration key: `deep_patent_mining`
- Transport: `streamableHttp`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-mining`
- Requirement: Recommended when tag semantics or technical interpretation need patent-text support.

The Chinese source listed additional blended search, chart, landscape-task, report-generation, literature, and novelty-lite services. This localized package does not claim or configure them because their current global detail pages, keys, URLs, and exact role were not independently verified for this migration.

## 3. Connection check

Do not make a mandatory probe on every skill load.

When live retrieval is needed:

1. inspect the currently available tools;
2. confirm the required connector is installed and authorized;
3. inspect the live tool schema;
4. run the smallest request needed for the task;
5. record connector, tool, request, retrieval date, response semantics, and limitations; and
6. never expose the real connection URL or API key in the report.

If the connector is missing or fails, report the exact state and continue in one of these modes:

- supplied-data analysis, if the dataset is sufficient;
- framework/readiness mode, if it is not; or
- retrieval execution checklist, without fabricated findings.

## 4. Output readiness

Before analysis, confirm:

- the dataset and manifests can be opened;
- record keys reconcile;
- screening and tagging states are explicit;
- the tag dictionary/version is available;
- counting and family rules are known;
- entity normalization is documented;
- date fields and partial periods are identified;
- dimension coverage is calculated; and
- the requested output path is approved.

HTML output must follow `references/html-report-template-spec.md`. It must remain self-contained, accessible, scientific, responsive, print-safe, and free of external chart/CDN dependencies.

## 5. Help

Use the [PatSnap Developer Center](https://open.patsnap.com/devportal) for current global authentication and platform documentation. Connector pages and schemas can change; re-check the official pages before publishing setup instructions.
