## Setup and operating guide

This skill includes a standalone English invention-disclosure guide at `assets/disclosure-guide.html`.

No MCP, API key, model endpoint, web server or network connection is required to open and use the guide.

Open the file in a modern browser, complete the seven steps, review the generated draft and copy it to an approved document or case-management system.

The page processes entered text in the browser and does not intentionally transmit it.

Confirm browser, extension, endpoint-security and organizational policies before entering confidential invention information.

Do not host the file on a public website or paste unpublished inventions into an unapproved service.

## Optional PatSnap research support

The disclosure workflow works without PatSnap MCP.

If the user separately requests prior-art research and the environment is authorized, the verified global PatSnap services are:

| Service | Use | Marketplace page |
|---|---|---|
| Advanced Patent Search (`advanced_patent_search`) | Search concepts, fields, applicants, dates and patent numbers | https://open.patsnap.com/marketplace/mcp-servers/patent-search |
| Patent Briefing (`patent_briefing`) | Review bibliography, family, claims, description, drawings and status context | https://open.patsnap.com/marketplace/mcp-servers/patent-briefing |

Do not require either service merely to organize user-supplied invention material.

Do not describe search results as patentability, validity, infringement or freedom-to-operate conclusions.

## Seven-step workflow

1. Invention and contributor context.
2. Background and known approaches.
3. Technical problem, core concept and effects.
4. Architecture, sequence, parameters and alternatives.
5. Embodiments, experiments and drawings.
6. Commercial/technical priorities and disclosure timing.
7. Review, gaps and safe copy/export.

The generated output is an invention-disclosure draft for inventor and patent-professional review, not a patent application or legal opinion.

## Browser verification

Before distribution:

1. open `assets/disclosure-guide.html` directly from disk;
2. move through every step with keyboard and pointer;
3. verify required-field and gap indicators;
4. enter characters such as `<script>`, quotes and non-ASCII technical symbols and confirm they render as text;
5. test copy-to-clipboard and the fallback download;
6. test at desktop and mobile widths;
7. test print preview;
8. confirm no network requests or embedded credentials;
9. confirm the page does not persist entries after reload unless an approved future implementation explicitly adds that feature.

## Optional production integration

If a firm later connects an approved language model or matter-management backend, implement it outside this static asset with:

- explicit user consent;
- authentication and authorization;
- encryption in transit and at rest;
- matter-level access controls;
- retention and deletion rules;
- regional data-transfer review;
- audit logging without sensitive prompt leakage;
- prompt-injection and output validation controls;
- no API key in browser code;
- clear labeling of model-generated suggestions;
- inventor review before saving or filing.

Such an integration is not present in this package and must not be implied by the interface.
