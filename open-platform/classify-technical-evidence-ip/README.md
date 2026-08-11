# Setup guide

This skill can classify records entirely from user-provided files. PatSnap MCP services are optional evidence sources for terminology discovery, representative patents, technical concepts, claims, descriptions, and boundary cases. They are not substitutes for taxonomy governance or human confirmation.

## 1. Decide whether external enrichment is permitted

Before connecting a service, determine whether the records contain confidential, personal, export-controlled, licensed, or otherwise restricted information.

- Do not send source records, excerpts, identifiers, or queries to an external service until the user or data owner has authorized that transfer.
- Prefer normalized concepts or public publication numbers when those are sufficient.
- Minimize each request to the evidence needed for the active decision.
- Never place an API key, bearer token, authorization header, or credential-bearing URL in a workbook, provenance table, chat message, or skill file.
- When enrichment is not authorized, use the local workflow and record `mcp_enrichment_status: not_authorized`.

## 2. Get a PatSnap Open Platform API key

Sign in at [PatSnap Open Platform](https://open.patsnap.com/) and follow the current [authentication guide](https://open.patsnap.com/devportal/guides/authentication). Store the key only in the MCP client's credential mechanism.

## 3. Choose only the MCP services needed

Open the [global MCP marketplace](https://open.patsnap.com/marketplace/mcp-servers), select a service, and copy the current connection URL from that service's **Connect** panel. Connector URLs can change; the detail page is authoritative.

| Service | Use in this skill | Installation |
|---|---|---|
| [Advanced Patent Search](https://open.patsnap.com/marketplace/mcp-servers/patent-search) | Keyword assistance, semantic and field searches, classification-assisted retrieval, representative patents, and patent-number lookup | Recommended for patent taxonomies |
| [Deep Patent Mining](https://open.patsnap.com/marketplace/mcp-servers/patent-mining) | Technical problem/approach/benefit, technology topic, classification description, and application domain | Recommended for technical definitions |
| [Patent Briefing](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing) | Claims, descriptions, bibliography, family data, status, images, and candidate verification | Recommended when full patent evidence is needed |
| [Scientific & Translational Evidence](https://open.patsnap.com/marketplace/mcp-servers/scientific-translational-evidence) | Scientific literature and translational evidence for suitable life-science labeling tasks | Optional and domain-dependent |

Verified configuration names and Connect-panel values on 2026-08-07:

| Service | Configuration key | Transport | Published connection URL |
|---|---|---|---|
| Advanced Patent Search | `advanced_patent_search` | `streamableHttp` | `https://open.patsnap.com/marketplace/mcp-servers/patent-search` |
| Deep Patent Mining | `deep_patent_mining` | `streamableHttp` | `https://open.patsnap.com/marketplace/mcp-servers/patent-mining` |
| Patent Briefing | `patent_briefing` | `streamableHttp` | `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing` |

Do not paste a real key into this README or another project file. Generate the current authenticated connection URL through the official marketplace Connect action and copy it directly into the MCP client.

## 4. Confirm connectivity

Use the client's MCP status command or tool list to confirm that the selected server is connected. Then run one low-volume, non-sensitive probe that matches the intended capability.

Record:

- service and tool;
- timestamp and status;
- non-sensitive query summary;
- returned identifiers;
- whether the response was complete, limited, empty, unavailable, or erroneous.

Do not treat a successful connection as authorization to transmit the labeling data.

## 5. Failure and local-only behavior

If a required capability is unavailable:

1. Confirm the exact official service page and client status.
2. Check authentication without exposing the key.
3. Retry a query-specific failure once with a simpler normalized concept.
4. Continue with user-provided evidence when that is sufficient.
5. Set `mcp_enrichment_status` to `incomplete`, `unavailable`, or `not_authorized`.
6. Name the affected stage and capability in the QA summary.
7. Never fabricate retrieved records, evidence, counts, or identifiers.

## 6. Runtime dependencies

The bundled `.mjs` helpers require the workspace-provided spreadsheet runtime. Load workspace dependencies first, copy the helper to a writable working directory, and make that directory resolve the bundled `node_modules`. Do not install replacement packages or hard-code a user-specific runtime path.

The Python validators use the standard library for JSON and CSV. A non-JSON YAML task configuration additionally requires an already approved YAML parser. The validator must report the missing parser; it must not install one.

## 7. Included domain fixture

The milk-protein package is a translated historical patent-labeling fixture built from Chinese and Korean records. It is useful for testing taxonomy boundaries and validation behavior, but it is not a representative sample of the global patent landscape.

- Keep publication numbers, record IDs, label IDs, source filenames, gold-label relationships, and version identifiers unchanged.
- Treat English patent excerpts as working translations and retain original-language provenance.
- Do not use the fixture's class distribution as a global benchmark.
- Do not silently replace the customer-confirmed v2 boundaries with model or MCP suggestions.

## Connectivity message

When live enrichment is requested but no suitable service is connected, report:

> PatSnap MCP enrichment is not currently available. The local evidence-based labeling workflow can continue, but live terminology, patent, literature, or boundary enrichment will be marked incomplete. Connect only the needed service from the PatSnap global MCP marketplace and authorize any external transmission before retrying.
