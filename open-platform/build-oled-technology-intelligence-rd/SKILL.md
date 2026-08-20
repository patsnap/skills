---
copyright: "Copyright © Patsnap. All rights reserved."
name: build-oled-technology-intelligence-rd
description: Build a source-traceable, multi-page technology-intelligence HTML portal for OLED or another defined technology domain. Use when a user asks for a technology watch portal, company and technical-route monitoring brief, news/event tracker, patent evidence page, or refreshable R&D intelligence site.
---

# Build an OLED or Technology Intelligence Portal

## Purpose

Create a self-contained, multi-page HTML intelligence portal from reviewed company, technology-route, event, publication, and patent records. OLED is the source package's worked domain, but the workflow remains reusable for batteries, semiconductors, materials, biopharma, energy, and other technical fields.

The portal supports R&D, strategy, product, competitive-intelligence, and IP teams. It must show evidence coverage and uncertainty rather than presenting model recall as a verified market map.

## Read the bundled material

- Read `references/company-mapping.md` when defining and normalizing monitored organizations.
- Read `references/tech-tags.md` when building a technology taxonomy or using the OLED seed taxonomy.
- Read `references/data-processing.md` before normalizing, deduplicating, validating, or counting records.
- Read `references/html-templates.md` before changing portal structure, visual design, accessibility, or rendering behavior.
- Run `scripts/generate_portal.py --help` before rendering.

Do not add a README or configuration file: the frozen source has exactly these six files.

## 1. Define the intelligence scope

Establish:

- technology domain and included/excluded meanings;
- decision use and intended audience;
- geographies and jurisdictions;
- monitoring period and evidence cutoff;
- languages and source types;
- company inclusion rule;
- technical-route taxonomy rule;
- patent unit, family normalization, legal-status treatment, and date fields;
- refresh cadence and material-event triggers;
- confidentiality and distribution restrictions.

If a field is missing, state a conservative working assumption. Do not silently default to China, Chinese-language sources, a fixed two-year period, or a fixed number of companies/routes.

## 2. Build a reviewed company universe

Never choose organizations solely from model memory. Start with user-supplied entities, authoritative industry sources, retrieved evidence, or the explicitly labeled OLED seed list in `references/company-mapping.md`.

For each organization record:

- stable organization ID and display name;
- legal name and normalized aliases;
- entity type and role in the value chain;
- headquarters and operating geographies when relevant;
- inclusion rationale and source IDs;
- first/last evidence dates;
- review status and confidence;
- merger, subsidiary, joint-venture, rename, or ownership notes;
- page slug generated safely by the renderer.

Separate direct competitors, suppliers, customers, research organizations, entrants, and adjacent players. Entity presence in news or patents does not prove commercial activity in the scoped segment.

## 3. Build the technology taxonomy

Use domain sources, reviewed patent/literature evidence, standards, roadmaps, and expert input. The source's 16 OLED tags are a seed taxonomy, not a universal or current ground truth.

For each route or tag record:

- stable taxonomy ID and English display name;
- definition, inclusion, and exclusion criteria;
- synonyms, acronyms, translations, and disambiguation terms;
- parent/child and related-route relationships;
- evidence IDs and review date;
- maturity or lifecycle framework if used;
- page slug generated safely by the renderer.

Avoid ambiguous substring classification. For example, `display` alone is too broad for `flexible OLED`, and `UDC` can refer to unrelated concepts. Record why each item was tagged and allow manual review/override.

## 4. Acquire evidence

Only search when the user requests research or the portal scope explicitly requires current evidence.

Verified global Patsnap mappings, when exposed in the environment:

- `advanced_patent_search` — [Patsnap Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search) for patent discovery and structured fields.
- `patent_briefing` — [Patsnap Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing) for selected patent-record review.
- `current_awareness` — optional when actually exposed, for dated news/current-awareness evidence.
- `scientific_translational_evidence` — optional when actually exposed, for scientific literature evidence.

Do not claim source-named domestic vector-search tools. Use the exact current callable schema and English interface. If an optional service is unavailable, use supplied reviewed records or independently verified public sources and record the limitation.

For each search retain search ID, query, filters, source/tool, timestamp, cutoff, requested limit, returned count, pagination/truncation, language, and review status.

## 5. Normalize records

Follow `references/data-processing.md`.

Every news, event, literature, or patent item must have a stable record ID, title, source, direct URL where available, publication/event date, access date, evidence type, language, associated companies/routes, review status, and analyst note.

Do not use `#` as a fake source link. When no URL exists, render `Source link not supplied` without an anchor.

Patent records additionally require publication number, jurisdiction, applicant/assignee as returned, priority/publication date where available, simple/extended family identity where available, legal-status source/date, technical relevance, and review depth. Do not conflate publication, application, grant, and family counts.

## 6. Validate and deduplicate

Before analysis and rendering:

- reject invalid root types and missing required metadata;
- normalize unambiguous dates to ISO 8601;
- preserve source time zones when timestamps matter;
- deduplicate news/events by stable ID, canonical URL, or reviewed title/date/source logic;
- deduplicate patents according to the declared publication or family unit;
- normalize aliases without collapsing distinct legal entities;
- validate `https`/`http` URLs and suppress disallowed schemes;
- calculate statistics from accepted records rather than trusting supplied totals;
- preserve rejected-record counts and reasons.

Do not silently skip malformed bytes or JSON characters. Return actionable validation errors with record locations.

## 7. Analyze without fabricating

Summaries, trends, company signals, route signals, and major-event notes must link to record IDs. Separate:

- source fact;
- analyst calculation;
- analyst inference;
- estimate;
- missing evidence.

Do not turn source frequency into market share, technical leadership, product use, patent strength, or business impact without an appropriate method and evidence.

## 8. Prepare renderer input

Supply one UTF-8 JSON object. The complete contract is in `references/data-processing.md`. At minimum include:

- `review_status: "reviewed"`;
- portal metadata and cutoff;
- methodology and limitations;
- reviewed arrays for companies, technology routes, events, publications, and patents;
- optional executive findings with evidence IDs.

Do not supply raw HTML. All inserted values are escaped by the renderer.

## 9. Render the portal

Run:

```bash
python scripts/generate_portal.py --data /path/to/reviewed-portal.json --output /path/to/portal
```

The renderer creates the source-prescribed topology inside the selected output directory:

```text
portal/
├── index.html
├── company-{safe-slug}.html
├── tech-{safe-slug}.html
└── patents.html
```

One company page is generated per company and one route page per technical route. The renderer writes only known generated files into a new or empty output directory unless `--overwrite` is explicitly supplied. It does not delete unrelated files.

## 10. Portal modules

The index page includes:

1. metadata, evidence cutoff, and coverage;
2. calculated record statistics;
3. evidence-linked executive findings;
4. monitored organization cards;
5. technical-route cards;
6. major event timeline;
7. literature/current-awareness overview when supplied;
8. patent evidence preview;
9. methodology, search log, limitations, and refresh status.

Company pages include role, inclusion evidence, associated routes, dated records, patents, and limitations. Technology pages include definition, inclusion/exclusion criteria, associated companies, dated records, patents, maturity evidence, and gaps. The patent page includes coverage/method, count unit, filters, and reviewed records.

## Visual and editorial standard

Follow `references/html-templates.md`:

- restrained global scientific/editorial design;
- white and neutral surfaces, navy text, one blue accent, semantic colors used sparingly;
- no gradients, emoji navigation, decorative floating cards, external fonts, Tailwind CDN, or chart libraries;
- tabular numerals, readable tables, generous whitespace;
- semantic HTML, skip link, visible keyboard focus, accessible navigation, descriptive link text;
- responsive and print layouts;
- no runtime network dependency, analytics, storage, or credentials.

Use concise international English. Define OLED-specific acronyms at first meaningful use.

## Quality gates

Verify:

- portal scope, period, cutoff, geographies, languages, and source coverage are visible;
- every company/route inclusion has evidence or is labeled as a seed/hypothesis;
- every factual summary links to evidence IDs;
- dates and counts reconcile across pages;
- patent units and family treatment are disclosed;
- source URLs are genuine global links or rendered as unavailable;
- no domestic-only tool/link, fixed source-case date, or unsupported ranking remains;
- user/tool content is HTML-escaped and URLs are allowlisted;
- slugs cannot traverse directories or collide silently;
- generated links resolve locally;
- HTML parses and navigation works without external resources;
- no cache, temporary file, credential, or local user path is packaged.

## Completion and limitations

Deliver the portal path, calculated file/record counts, evidence cutoff, unavailable sources, rejected records, and refresh instructions. State that public evidence may omit non-public activity and that the portal is not legal, investment, or commercial advice. Patent evidence does not establish infringement, validity, freedom to operate, or technical leadership.
