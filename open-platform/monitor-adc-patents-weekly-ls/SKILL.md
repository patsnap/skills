---
name: monitor-adc-patents-weekly-ls
description: Create an evidence-backed weekly monitor of newly published antibody-drug conjugate (ADC) patent applications. Use when a user asks for an ADC patent weekly, new WO/PCT publications, emerging ADC targets or technologies, priority claim comparisons, or a shortlist of records that warrant claim review.
---

# Monitor ADC Patents Weekly

## Purpose

Identify patent publications relevant to antibody-drug conjugates within a defined reporting week, remove predictable noise in two documented screening passes, explain the most important disclosures, and deliver a decision-ready weekly brief for IP, R&D, competitive-intelligence, and business-development teams.

This workflow supports monitoring and triage. It does not establish freedom to operate, infringement, validity, patentability, ownership, or clinical efficacy.

## Use this skill when

- the user requests a weekly ADC patent intelligence report;
- the user wants WO/PCT publications first published during a specified week;
- a team needs new ADC assets, targets, linker/payload technologies, conjugation methods, or manufacturing signals;
- the user asks which high-relevance records warrant detailed claim comparison;
- patent events must be interpreted alongside supplied drug, clinical, company, or market evidence.

Do not invoke it for a one-off claim chart, a legal FTO opinion, or general oncology news without a patent-monitoring objective.

## Required decisions before retrieval

Confirm or state every assumption:

1. **Reporting interval** — start and end dates, time zone, and whether boundaries are inclusive. Default to the most recently completed Monday–Sunday interval in the user's time zone; otherwise use UTC and say so.
2. **Publication event** — default to the publication date of an international application with a `WO` publication number. Do not substitute filing, priority, grant, database-ingestion, or national-publication dates.
3. **Technology scope** — broad ADC monitoring or a defined target, antibody format, payload, linker, conjugation chemistry, indication, company, or competitor set.
4. **Territorial scope** — WO-only as in the source workflow, or WO plus selected national offices. Keep the result sets separate if both are requested.
5. **Family counting rule** — default to one row per INPADOC/simple family with the earliest in-window WO publication as the representative; retain all in-window WO members in the evidence record.
6. **Language rule** — search English plus relevant synonyms and identifiers; inspect translated titles/abstracts/claims where available. Label machine-translated text.
7. **Delivery format** — Markdown by default; a self-contained HTML report only when requested.

If the user gives no interval and a reliable current date is unavailable, ask for dates rather than inventing a week.

## Inputs

### Minimum viable input

- reporting interval;
- WO-only or expanded jurisdiction scope;
- broad ADC scope or a defined monitoring question.

### Helpful input

- target and antigen aliases;
- company and subsidiary aliases;
- known drug names, development codes, payload classes, linker families, or conjugation chemistries;
- prior weekly report or monitoring query;
- inclusion/exclusion policy;
- preferred recipients and decision horizon.

Record missing inputs and their effect on coverage.

## Data and MCP selection

Use user-supplied, authoritative exports when they cover the requested interval and required fields. No MCP is required in that mode.

For live retrieval, use only connectors that are actually available and authorized:

| Need | PatSnap MCP | Role | Marketplace |
|---|---|---|---|
| Reproducible publication-date and technical-field search | `advanced_patent_search` | Primary; use `search_patents_nested`, `search_patent_count`, field filtering, and keyword assistance as available | https://open.patsnap.com/marketplace/mcp-servers/patent-search |
| Bibliography, family, status, claims, description, drawings, translation, and technical problem/solution/benefit | `patent_briefing` | Verification and enrichment of shortlisted records | https://open.patsnap.com/marketplace/mcp-servers/patent-briefing |
| Pharmaceutical news | `current_awareness` | Optional context through `news_search` and `news_fetch`; never a patent source | https://open.patsnap.com/marketplace/mcp-servers/current-awareness |
| Drug details and development milestones | `drug_asset` | Optional drug-context verification through `drug_search`, `drug_fetch`, and `drug_milestone_fetch` | https://open.patsnap.com/marketplace/mcp-servers/drug-asset |

Copy the current connection URL from the marketplace page. Do not guess endpoints, tool names, credentials, or access rights. Never place an API key in the report.

If live patent retrieval is unavailable, stop at a search protocol and input-gap statement; do not fabricate a weekly result set.

## Search protocol

### 1. Build the ADC concept set

Use several concept families instead of a single acronym:

- `antibody-drug conjugate`, `antibody drug conjugate`, `immunoconjugate`;
- antibody or antigen-binding terms near conjugate/linker/payload/cytotoxin terms;
- ADC format terms such as bispecific ADC, dual-payload ADC, fragment-drug conjugate, site-specific conjugate;
- payload classes and named payloads relevant to the brief;
- cleavable/non-cleavable linker, spacer, self-immolative unit, conjugation, drug-to-antibody ratio, and site-specific attachment terms;
- target, indication, company, and asset aliases when the scope is narrower.

Treat `ADC` alone as noisy because it has non-biopharmaceutical meanings. Preserve the complete query or structured filters in the report appendix.

### 2. Apply the date and publication gate

Require:

- publication number begins with `WO` for the default scope;
- publication date falls inside the inclusive reporting interval;
- the record is a patent publication, not a journal, trial, press release, or database update.

Retrieve slightly beyond the nominal interval only to test boundary behavior, then exclude out-of-window records explicitly.

### 3. Run two-pass screening

#### Pass 1 — bibliographic and semantic noise removal

Exclude or set aside records when:

- ADC appears only in background, citations, boilerplate, or an unrelated acronym expansion;
- the publication date or kind is outside scope;
- the record is a duplicate family member under the counting rule;
- the title/abstract has no plausible antibody–linker–payload or ADC platform relationship;
- evidence is too incomplete to establish relevance.

Keep an exclusion log with publication number, reason code, and reviewer note.

#### Pass 2 — disclosure and claim relevance

Review representative independent claims and supporting description where available. Assign one primary relevance class:

- **Core ADC composition** — antibody/antigen-binding moiety, linker, payload, or complete conjugate is materially claimed;
- **Platform or enabling technology** — conjugation, linker, payload, analytical, formulation, manufacturing, or delivery technology is materially tied to ADCs;
- **Use or treatment** — an ADC, defined class, or named asset is materially claimed for a disease, regimen, biomarker, or combination;
- **Peripheral mention** — ADC is an option in a broad list without claim-level or disclosure-level focus;
- **Not relevant** — false positive.

High relevance requires claim-level evidence or a clear ADC-focused disclosure. Abstract relevance alone is not enough for a recommendation to compare claims.

### 4. Consolidate families and entities

- Normalize applicant and assignee names without erasing the name shown on the publication.
- Distinguish applicant, original assignee, current assignee, and parent company where data permits.
- Keep family consolidation separate from applicant normalization.
- Record representative publication, family identifier, earliest priority, in-window members, and other relevant jurisdictions.
- Never infer ownership solely from corporate branding or a news article.

## Evidence record

Create one structured record per included family:

| Field | Requirement |
|---|---|
| Representative publication | WO publication number and kind code |
| Publication date | ISO `YYYY-MM-DD` |
| Title | Original or verified English translation |
| Applicant/assignee | As published; normalized entity in a separate field |
| Inventors | When available |
| Earliest priority | Date and application identifier |
| Family | Identifier or documented grouping basis |
| ADC relevance class | One controlled class from Pass 2 |
| Target/antigen | Explicit, inferred, or not reported |
| Antibody format | Explicit, inferred, or not reported |
| Payload | Name/class and evidence status |
| Linker/conjugation | Named technology and evidence status |
| Indication/use | Claimed, disclosed, or not reported |
| Claim evidence | Claim number and a short paraphrase; quote only when necessary |
| Technical triad | Problem, disclosed approach, and stated benefit |
| Novel signal | What appears new relative to the monitored baseline; not a legal novelty conclusion |
| Follow-up priority | High, medium, or low with rationale |
| Sources | Stable patent record links and optional context links |
| Confidence | High, medium, or low with reason |

Use `not reported`, `not retrieved`, and `not applicable` distinctly. Never turn missing values into zero or negative evidence.

## Technical triad and insight writing

Summarize every priority record using this self-explanatory triad:

1. **Technical problem** — the limitation, unmet need, or performance issue described by the publication;
2. **Disclosed approach** — the claimed or described antibody, target, linker, payload, conjugation, formulation, method, or use;
3. **Stated benefit** — the effect asserted by the publication, clearly attributed and not presented as independently proven.

Then add an **Analyst interpretation** paragraph that separates:

- source fact;
- reasoned inference;
- comparison with the monitored baseline;
- recommended next action.

Do not use promotional language such as “breakthrough” unless quoting and attributing a source. Do not convert patent assertions into clinical proof.

## Prioritization

Use transparent factor ratings rather than a false-precision composite score:

| Factor | High-priority signal |
|---|---|
| Claim centrality | ADC element or use is present in an independent claim |
| Strategic overlap | Matches the user's target, modality, payload, linker, indication, or competitor |
| Technical specificity | Concrete sequence, structure, conjugation site, ratio, formulation, or regimen |
| Family/territory signal | Relevant family coverage or national-stage activity, with date caveats |
| Development linkage | Verified connection to a drug or milestone, not name similarity alone |
| Uncertainty | Material ambiguity that requires primary-document review |

Recommend detailed claim comparison when claim centrality and strategic overlap are both material, or when uncertainty could change a high-impact decision. State the specific claims and comparison question.

## Weekly report structure

1. **Title and reporting interval**
2. **Executive takeaways** — three to six evidence-backed signals
3. **Coverage and method** — sources, query, dates, WO rule, family/counting rule, retrieval timestamp, and limitations
4. **Funnel** — retrieved, Pass-1 retained, Pass-2 included, consolidated families, and excluded counts
5. **Priority watchlist** — concise table of high-priority families
6. **New publications** — one evidence card per included family
7. **Technology signals** — targets, formats, payloads, linkers/conjugation, manufacturing, uses, or combinations
8. **Applicant and asset signals** — normalized cautiously
9. **Claims requiring comparison** — record, claims, comparison objective, and urgency
10. **Optional drug/news context** — clearly separated from patent evidence
11. **Opportunities, risks, and next actions** — owner and timing where supplied
12. **Exclusions and limitations**
13. **Sources and search appendix**

If no relevant publication survives screening, issue a valid zero-result report containing the executed query, date window, retrieval status, exclusion counts, limitations, and proposed query adjustments. Do not pad it with out-of-window records.

## HTML presentation, when requested

Create a self-contained, responsive, printable HTML file with a restrained scientific/editorial style:

- light neutral background, dark charcoal text, one muted blue or teal accent, and accessible contrast;
- clear typographic hierarchy using system fonts;
- compact evidence tables, plain cards, generous whitespace, and consistent labels;
- no dark sci-fi theme, gradients, glowing effects, particles, stock dashboard chrome, ticker, or decorative animation;
- no external CDN, font, chart, or script dependency unless the user explicitly authorizes it;
- semantic headings, table captions, keyboard-accessible controls, visible focus states, and non-color status labels;
- responsive tables or stacked evidence cards below narrow breakpoints;
- print CSS that preserves URLs, headings, table headers, and page breaks.

Preserve the report's information architecture in a globally familiar scientific format; do not imitate a product-specific desktop interface.

## Quality gates

Before delivery, verify:

- [ ] interval, time zone, publication event, and inclusion boundaries are explicit;
- [ ] WO publication filtering is applied as requested;
- [ ] query concepts and structured filters are reproducible;
- [ ] two-pass screening and exclusion reasons are documented;
- [ ] family counting and applicant normalization are not conflated;
- [ ] every included record has a publication number, date, relevance evidence, source, and confidence;
- [ ] technical problem, disclosed approach, stated benefit, and analyst interpretation are separated;
- [ ] claims recommended for comparison are identified precisely;
- [ ] patent facts, drug milestones, clinical evidence, and news are visibly separated;
- [ ] missing data is labeled, not silently treated as zero;
- [ ] all counts reconcile from retrieval to final families;
- [ ] legal, clinical, and commercial conclusions are appropriately bounded;
- [ ] links resolve to the intended global PatSnap or primary source page;
- [ ] the report contains no credentials, hidden personal data, invented patents, or unsupported claims.

## Failure and escalation paths

- **No live source:** provide the protocol and required export fields; do not produce results.
- **Partial interval coverage:** identify the uncovered dates and label the report provisional.
- **Ambiguous publication date:** exclude from period counts until verified; retain in a review queue.
- **Incomplete claims:** rate relevance from available disclosure but do not recommend a claim-level conclusion.
- **Conflicting family or assignee data:** show both values, sources, and retrieval timestamps.
- **Very large result set:** report the count, refine transparently, and preserve the broader query for audit.
- **Potential FTO or infringement issue:** identify the question and relevant records, then recommend qualified counsel and a dedicated jurisdiction-specific analysis.

## Output boundaries

- Do not invent patents, applicants, claims, targets, payloads, milestones, market events, or technical evidence.
- Do not call a document novel, valid, enforceable, blocking, or infringing based on this monitor.
- Do not treat a WO publication as a granted or enforceable right.
- Do not infer clinical success from a patent publication.
- Cite the primary patent record for patent facts and the original source for external context.
- Mark analysis and uncertainty explicitly.
