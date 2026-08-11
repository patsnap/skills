---
name: monitor-patent-litigation-risk-ip
description: Monitor patent-litigation exposure for a primary company and up to four named comparison parties. Use when users need target-centric identification of potentially litigated patents, patent-family and claim analysis, verified proceeding timelines, case deep dives, inventor activity, geographic exposure, litigation alerts, technology trends, and an evidence-backed HTML report with structured JSON or CSV attachments.
---

# Monitor Patent Litigation Risk

## Purpose and boundary

Create an evidence-backed monitoring report for one primary target and, optionally, up to four comparison parties. Preserve the source workflow's patent discovery, public-record verification, family expansion, claim comparison, legal-history review, litigation timeline, case analysis, inventor activity, three-dimensional conclusions, and target-centric HTML output.

Act as an intelligence analyst, not as counsel, a court, a tribunal, or a prediction service. Do not provide legal advice or state that a party will win, lose, infringe, obtain an injunction, invalidate a patent, or settle. Separate:

- discovery signals from verified proceedings;
- allegations from findings and holdings;
- procedural rulings from merits dispositions;
- patent legal status from enforceability;
- patent-family coverage from commercial or litigation exposure;
- descriptive inventor activity from causal predictions; and
- source facts from analyst inference.

Treat PatSnap legal-event data as a patent-data and discovery source. Verify material case facts using primary tribunal, court, agency, or official-register records current to the report cutoff.

## Suitable requests

Use this skill for requests such as:

- monitor patent litigation involving a named company;
- identify patents reported as asserted against or by a target;
- expand asserted patents to their INPADOC families;
- build a proceeding timeline with asserted patent numbers;
- compare representative family claims across material jurisdictions;
- review litigation posture, defenses, outcomes, and appeals;
- map recent activity of inventors linked to the reviewed families; or
- create a target-centric litigation-risk monitoring report.

Do not use this skill as the primary workflow for a standalone novelty opinion, inventive-step opinion, invalidity search, infringement opinion, FTO legal opinion, or open-ended technology landscape without named parties.

## Input contract

| Field | Required | Meaning |
|---|---:|---|
| `parties` | Yes | One to five named organizations; the first is the monitored target |
| `target_aliases` | No | Verified former names, subsidiaries, abbreviations, and spelling variants |
| `jurisdictions` | No | Courts, tribunals, and patent authorities material to the business question |
| `cutoff_date` | Yes for final | Date through which case and patent facts were verified |
| `inventor_lookback_years` | No | Recent filing lookback; source default is 3 years |
| `family_scope` | No | Source default is INPADOC; state any alternative |
| `max_litigated_per_party` | No | Review cap; source default is 30 and must be disclosed |
| `business_context` | No | Product, market, transaction, launch, or monitoring objective |
| `known_cases_or_patents` | No | User-supplied leads requiring independent verification |
| `output_path` | No | Destination for HTML, JSON, and CSV artifacts |

Do not stop for routine confirmations once inputs are sufficient. Record reasonable assumptions and continue. Ask only when party identity is genuinely ambiguous or a missing choice materially changes the requested scope.

## Target-centric rule

Use the first party as the grammatical and analytical subject of the report. Classify the target's role for every proceeding and asserted patent as one of:

- `plaintiff`;
- `defendant`;
- `counterclaimant`;
- `co_party`; or
- `other`.

Do not organize chapters around a comparison party as though it were the monitored target. Do not infer a role from patent ownership alone. Verify roles from the actual proceeding record.

## Evidence model

Assign stable identifiers:

- cases: `CASE-001`, `CASE-002`, and so on;
- patents: publication number plus a stable record ID if needed;
- sources: `S001`, `S002`, and so on;
- search runs: `Q001`, `Q002`, and so on;
- findings: `F001`, `F002`, and so on.

For each material fact, preserve:

| Field | Required content |
|---|---|
| Fact | Exact proposition supported |
| Source type | Primary docket/order, official register, patent record, news, or other |
| Source locator | URL, docket entry, page, paragraph, patent number, event, or claim |
| Source date | Filing, publication, order, event, or status date |
| Accessed | Retrieval date |
| Evidence state | `verified`, `partially_verified`, `unverified`, or `conflicting` |
| Coverage | What the source establishes and does not establish |
| Notes | Translation, party-name, date, family, or status limitation |

Use reporting, press releases, law-firm notes, and database signals as secondary leads. Never cite a search-results page as proof of a court fact when a primary source is available.

## Verified PatSnap MCP mappings

Confirm each connector's live tool schema at runtime. Do not invent source tool names or parameters.

### Global Core Patent Database — required

Use for patent search, detailed legal events, simple status, full text, images, and reexamination or invalidation data.

- Connector key: `global_core_patent_database`
- Marketplace: <https://open.patsnap.com/marketplace/mcp-servers/core-patents>
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/core-patents`

### Patent Briefing — required

Use for bibliography, legal status, family relationships, technical summaries, intelligent attached images, claims, descriptions, and translations.

- Connector key: `patent_briefing`
- Marketplace: <https://open.patsnap.com/marketplace/mcp-servers/patent-briefing>
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`

### Advanced Patent Search — optional

Use for broader assignee, inventor, classification, keyword, and technology retrieval when its search routes improve coverage.

- Connector key: `advanced_patent_search`
- Marketplace: <https://open.patsnap.com/marketplace/mcp-servers/patent-search>
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`

Never expose or reproduce a real API key. Obtain the current connection URL through the official marketplace Connect action.

PatSnap MCPs do not replace jurisdiction-specific court and tribunal sources. Use available public-source research for discovery and primary-source verification, and log every query, filter, date, and limitation.

## Execution workflow

### Step 1 — Normalize parties and freeze scope

1. Confirm the primary target and comparison parties.
2. Build an alias table using verified corporate names, former names, subsidiaries, and spelling variants.
3. Distinguish parent, subsidiary, affiliate, and acquired entity; do not collapse them without evidence.
4. Record material jurisdictions, date range, business context, family definition, review cap, and cutoff.
5. Create an explicit exclusion list for false-positive names.
6. Record whether the request concerns incoming claims, offensive enforcement, both, or general monitoring.

| Entity ID | Canonical name | Alias | Relationship | Effective dates | Source | Include/exclude |
|---|---|---|---|---|---|---|

### Step 2 — Dual-route litigation-patent screening

Run patent-data discovery and public-record discovery independently.

#### Patent-data route

Search normalized assignee and applicant variants using Global Core Patent Database and, when useful, Advanced Patent Search. Review legal-event fields for litigation, infringement, complaints, injunctions, invalidity, opposition, administrative review, licensing disputes, or comparable jurisdiction-specific events.

Do not equate a keyword or event label with a verified asserted patent. Store candidates separately from verified asserted patents.

#### Public-record route

Search party aliases with jurisdiction-appropriate terms for complaints, cases, dockets, decisions, appeals, investigations, oppositions, reviews, and patent numbers. Prefer:

1. court or tribunal dockets and orders;
2. official agency or patent-office registers;
3. filed pleadings from reliable repositories;
4. company regulatory filings;
5. reputable reporting and practitioner commentary as secondary sources.

#### Identifier extraction

Extract patent and application identifiers using jurisdiction-aware patterns. Preserve the displayed identifier and record normalization separately. Support, as evidence requires, publication, grant, application, PCT, design, utility-model, and local registration formats.

Do not assume a ZL or CN format, strip digits indiscriminately, or infer a publication number from an application number. Verify every normalized identifier through patent data.

#### Merge and triage

De-duplicate by verified publication/application identity and family relationship. For each candidate, assign:

- `patent_data_signal`;
- `public_record_signal`;
- `both_signals`; or
- `user_supplied_lead`.

Then classify as:

- `verified asserted patent`;
- `case-related but assertion unclear`;
- `legal-event lead only`;
- `false positive`; or
- `unresolved`.

Record why the item changed state.

### Step 3 — Verify proceedings and target roles

For each candidate proceeding, verify:

- official case name and case number;
- tribunal, jurisdiction, and division;
- plaintiffs, defendants, counterclaimants, intervenors, and other parties;
- filing date and current procedural posture;
- asserted patents and, where available, asserted claims;
- allegations and causes of action;
- defenses and counterclaims;
- material orders, stays, transfers, institution decisions, trials, and appeals;
- settlement, dismissal, consent order, judgment, or other disposition;
- verification date and primary-source locator.

Do not describe a dismissal without prejudice, settlement, preliminary ruling, institution decision, or appeal as a final merits victory. If the public record is incomplete, state exactly what remains unverified.

Build a case record compatible with `scripts/orchestrator.py`.

### Step 4 — Expand families and analyze patents

For each verified or materially unresolved asserted patent:

1. Retrieve bibliography, family, legal status, full text, claims, translations, images, and material legal details.
2. Extract the canonical PatSnap or public patent locator from returned data; never fabricate an internal ID or UUID.
3. State the family definition and de-duplicate consistently.
4. Preserve continuation, divisional, continuation-in-part, national-stage, grant, reissue, and related relationships where material.
5. Verify legal status separately for each family member and state the as-of date.
6. Identify which family member and claims are actually asserted; do not transfer assertion to all relatives.
7. Select representative jurisdictions based on the case, business markets, family coverage, and claim availability—not a fixed CN/US/EP trio.

For representative claims, compare:

- independent-claim category;
- principal limitations;
- scope emphasis;
- material prosecution or amendment differences;
- translation provenance;
- apparent overlap and divergence; and
- limitations relevant to the alleged product or conduct, if verified.

Do not perform a dispositive claim-construction or infringement analysis unless separately requested and appropriately sourced.

### Step 5 — Retrieve and handle drawings safely

Use Patent Briefing's intelligent attached-image capability or another verified patent-record image source. Prefer a stable local copy or validated base64 payload for a portable report.

- Validate media type and size.
- Reject active content, `javascript:` URLs, non-HTTP(S) remote URLs, and malformed base64.
- Do not rely on expiring signed URLs for the final report.
- Use descriptive alt text.
- If no verified image is available, show a textual `Image not available` state.
- Do not fail the substantive report because an image is missing.

### Step 6 — Build the litigation timeline

Create a single chronological timeline with:

| Date | Case ID | Event | Patents/claims | Target role | Source | Evidence state |
|---|---|---|---|---|---|---|

Include a patent number at each node when the event actually concerns a patent. Do not attach every case patent to every procedural event. Distinguish filing, service, answer, counterclaim, claim-construction, stay, institution, trial, order, settlement, judgment, and appeal.

Normalize dates to ISO format while preserving uncertain or partial source dates.

### Step 7 — Perform case deep dives

For each verified case, cover:

1. parties and target role;
2. forum and procedural posture;
3. asserted patents and claims;
4. accused products or conduct, if publicly identified;
5. allegations, clearly labeled;
6. defenses and counterclaims, clearly labeled;
7. disputed technical and legal issues;
8. material orders and reasoning;
9. outcome and appeal status;
10. operational monitoring triggers;
11. primary and secondary sources; and
12. evidence gaps.

Attach `[S###]` citations to every material fact. Quote sparingly and within applicable copyright limits. Prefer paraphrase plus a precise locator.

### Step 8 — Analyze core inventor activity

Aggregate inventors from the reviewed patent families, rank by transparent criteria, and select up to the source default of ten. Search the configured recent period, default three years, using verified inventor identity and assignee context.

For each inventor, report:

- normalized identity and ambiguity;
- recent filing count and counting method;
- annual counts;
- top classifications;
- three to five evidence-backed technology themes;
- representative publications and links; and
- source and cutoff.

Inventor activity is descriptive. Do not treat it as proof of future litigation, employee movement, strategic intent, or product launch.

### Step 9 — Synthesize three dimensions

#### Geographic exposure

For each material jurisdiction, consider verified proceedings, asserted patents, current family members, business activity supplied by the user, and procedural posture. Use states:

- `Elevated`;
- `Moderate`;
- `Lower on reviewed evidence`; or
- `Not assessable`.

Family count or active-patent count alone cannot determine exposure.

#### Litigation alert

Summarize disputed issues, target role, procedural posture, defenses, counterparties, asserted claims, material deadlines only when verified, and monitoring actions. Do not impose a word quota; write enough to make evidence, uncertainty, and action clear.

#### Technology trend

Describe recent filing directions from the inventor and family evidence. Separate observed filing activity from inferred strategy and forecast scenarios. Provide near-, medium-, and long-term monitoring hypotheses only when evidence supports them, with explicit uncertainty.

### Step 10 — Produce artifacts

Create:

1. one target-centric HTML report;
2. one structured JSON evidence record compatible with `scripts/orchestrator.py` when requested or useful; and
3. CSV exports for cases, asserted patents/families, timeline, inventors, and sources when requested.

Do not add these generated outputs to the skill package itself.

## Active report structure

Use the following continuous report order:

0. Executive summary
1. Scope, target, method, cutoff, and limitations
2. Target overview and party-to-patent mapping
3. Litigation timeline
4. Target's verified asserted patents and family details
5. Proceeding deep dives
6. Core inventor activity
7. Three-dimensional conclusions
8. Action register
9. Patent/family summary list
10. Sources, search log, assumptions, and limitations

Use seven concise navigation tabs by grouping adjacent chapters:

- Summary
- Scope and Overview
- Timeline
- Patents
- Cases
- Inventors
- Conclusions and Sources

## Counting semantics

Never mix these counts:

- query matches reported by a source;
- records returned;
- unique publications reviewed;
- candidate litigation-linked patents;
- verified asserted patents;
- family members;
- patent families;
- verified proceedings; and
- procedural events.

State the family definition, jurisdiction coverage, date range, de-duplication rule, pagination limit, and unresolved records next to every material count.

## Visual and HTML specification

Use one portable, static, English HTML file with a restrained Western scientific/legal design:

- white or neutral paper surface;
- navy and slate hierarchy;
- system sans-serif typography;
- compact metadata band and executive facts;
- semantic tables, evidence cards, and timeline;
- text labels in addition to color;
- responsive table wrappers;
- print CSS and repeated table headers;
- no decorative emoji, gradients, faux gauges, or unsupported precision.

Do not require Chart.js, a CDN, remote JavaScript, analytics, trackers, or external fonts. Use simple HTML/CSS tables or accessible static SVG only when a chart materially improves comprehension.

Escape all external text. Reject unsafe URLs. Do not embed API keys, local paths, session IDs, hidden prompts, source credentials, or expiring signed links. Confirm every required chapter, case, patent, and citation appears in the final output.

Direct evidence-backed HTML authoring is the default. The source-retained `scripts/render_report.py` is an optional safe deterministic export and test surface; it is not an excuse to populate placeholders or synthetic facts. `SKILL.md.bak_v9_css` is a localized historical specification and is not authoritative.

## Script contracts

### `scripts/config.py`

Read when defaults, report section names, target roles, evidence states, risk states, or field semantics are needed.

### `scripts/orchestrator.py`

Use to create an empty JSON skeleton and validate cross-field references. It never retrieves data. Populate its records only from evidence gathered by the agent.

Example:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python scripts/orchestrator.py --parties "Target Corp,Comparison Corp" --cutoff-date 2026-08-07 --out report_data.json
```

### `scripts/render_report.py`

Use only after the record is populated and validated. The renderer escapes text, rejects unsafe URLs, and creates an offline HTML file.

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python scripts/render_report.py --data report_data.json --out litigation_report.html --lang en
```

### `scripts/tests/smoke.py`

Run offline to test schema validation, safe rendering, required content, and removal of active-content payloads.

### `scripts/main.py`

Retain as the source package's minimal entry point. It reports helper availability and does not claim to execute the evidence workflow.

## Failure and fallback behavior

- If a connector is unavailable, document which capability is missing and continue only with sources that can be verified.
- If primary case records are inaccessible, retain the item as `partially_verified` or `unverified`; do not elevate reporting to a holding.
- If patent and court identifiers conflict, preserve both, investigate, and mark `conflicting`.
- If party identity is ambiguous, exclude or isolate the record until resolved.
- If legal status lacks an as-of date, do not present it as current.
- If an asserted claim is not public, state that the patent is reported as asserted but claim-level scope is not verified.
- If an image cannot be safely embedded, omit it and keep the patent analysis.
- If inventor identity cannot be disambiguated, aggregate only verified records and disclose the limitation.
- If counts are truncated or sampled, label them as returned or reviewed counts, not totals.
- If no verified cases remain, deliver a negative-result monitoring report with search coverage and limitations; do not manufacture examples.

## Final self-check

- The target and comparison parties are correctly identified and normalized.
- Every case has a stable ID, verified role, tribunal, case number, source, and as-of date.
- Every asserted patent is linked to a case or explicitly marked unresolved.
- Candidate signals are not presented as verified assertions.
- Allegations, orders, holdings, dispositions, and inferences are distinguishable.
- Patent numbers, family relationships, status, claims, and images are verified.
- Family definition and count semantics are stated.
- Representative claim jurisdictions are selected for materiality, not by a fixed country list.
- Timeline nodes cite the specific event and relevant patents.
- Inventor trends are descriptive and use a stated identity/count method.
- Geographic, alert, and trend conclusions cite evidence and uncertainty.
- Global Core Patent Database, Patent Briefing, and any Advanced Patent Search use is logged accurately.
- Primary public sources verify material case facts.
- All external content is escaped and all links are safe.
- HTML is complete, offline, responsive, printable, accessible, and free of secrets.
- JSON and CSV outputs, when generated, reconcile with displayed counts.
- No placeholder, fabricated patent ID, invented case, or unsupported prediction remains.

## Structured record reference

Use this reference to reconcile direct HTML, JSON, and CSV outputs. Do not populate absent facts with empty-looking prose; preserve an empty value plus an explicit limitation.

### Root record

| Field | Type | Requirement |
|---|---|---|
| `schema_version` | string | Use the version implemented by the orchestrator |
| `generated_at` | ISO timestamp | Record generation time in UTC |
| `cutoff_date` | ISO date | Last date through which material facts were checked |
| `report_language` | string | Default `en`; preserve source-language evidence separately |
| `target` | object | Primary monitored organization and aliases |
| `comparison_parties` | array | Other named organizations, excluding the target |
| `scope` | object | Jurisdictions, family rule, search runs, caps, and limitations |
| `overview` | object | Reconciled descriptive counts |
| `family_analysis` | object | Geography, classifications, status, claims, and counting rule |
| `litigated_patents` | array | Verified or explicitly qualified patent records |
| `litigation_timeline` | array | Chronological, source-linked events |
| `cases` | array | Verified or explicitly qualified proceeding records |
| `inventors` | array | Disambiguated descriptive activity records |
| `conclusions` | object | Three dimensions and action register |
| `sources` | array | Evidence and query register |
| `assumptions` | array | Necessary assumptions stated as assumptions |
| `limitations` | array | Material coverage and evidentiary limits |

### Target object

| Field | Meaning |
|---|---|
| `name` | Canonical monitored entity name |
| `aliases` | Verified names and variants used in searches |
| `role_basis` | Why this party is the report's target |

Keep subsidiaries and affiliates in the alias register only when the relationship and relevant dates are sourced. Otherwise represent them as separate parties.

### Scope object

| Field | Meaning |
|---|---|
| `jurisdictions` | Included courts, tribunals, and patent authorities |
| `family_scope` | Family definition used for expansion and counts |
| `inventor_lookback_years` | Descriptive recent-activity period |
| `max_litigated_per_party` | Review cap, not a total-count claim |
| `top_inventors` | Maximum inventor records presented |
| `searches` | Reproducible query and connector log |
| `limitations` | Scope-specific omissions and access restrictions |

Each search entry should contain:

- stable search ID;
- connector or public source;
- discovered tool name;
- query and aliases;
- filters and jurisdictions;
- date range;
- execution timestamp;
- matched count if source-reported;
- returned count;
- reviewed count;
- selected records;
- de-duplication rule; and
- limitations or errors.

### Overview object

Use only reconciled values:

| Field | Counting basis |
|---|---|
| `party_count` | Target plus comparison parties |
| `candidate_patent_count` | De-duplicated discovery leads before verification |
| `verified_asserted_patent_count` | Patents linked to proceedings by sufficient evidence |
| `family_member_count` | Publications under the stated family rule |
| `verified_case_count` | Proceedings verified to the report's evidence standard |
| `party_patent_map` | Explicit party, role, patent, case, and source edges |

### Patent record

For each element of `litigated_patents`, preserve:

| Field | Requirement |
|---|---|
| `publication_number` | Verified canonical publication or grant number |
| `application_number` | Verified application number when available |
| `patent_url` | Stable HTTP(S) locator |
| `title` | Source title and translation provenance if translated |
| `filing_date` | Verified filing date |
| `publication_date` | Verified publication date |
| `priority_date` | Earliest relevant priority, qualified when entitlement is not reviewed |
| `legal_status` | Status label from named source |
| `legal_status_as_of` | Date of status verification |
| `target_role` | Verified role in linked proceeding |
| `risk_state` | Evidence-qualified state, not an outcome prediction |
| `evidence_state` | Verification completeness |
| `case_ids` | Existing stable case IDs only |
| `asserted_claims` | Publicly verified asserted claims only |
| `abstract_image_b64` | Validated bounded PNG payload without prefix |
| `abstract_image_url` | Safe HTTP(S) fallback only |
| `technology_problem` | Evidence-backed technical problem summary |
| `technology_means` | Evidence-backed solution mechanism |
| `technology_effect` | Evidence-backed technical benefit or result |
| `open_questions` | Unresolved claim, status, family, or case questions |
| `claims` | Exact or clearly translated claim text |
| `claim_source_language` | Language of the authoritative claim text |
| `family_members` | Related publications under the stated rule |
| `sources` | Patent and proceeding evidence locators |

Do not use a patent card to imply that every listed family member was asserted. Mark the asserted member and the relationship explicitly.

### Family member record

Preserve, when available:

- publication number;
- application number;
- jurisdiction;
- relationship type;
- filing date;
- publication date;
- grant date;
- priority date;
- legal status;
- status as-of date;
- representative-claim reason;
- source-language status;
- translation provenance; and
- source locator.

### Claim comparison record

For each compared representative claim, record:

- family identifier;
- publication number;
- jurisdiction;
- claim number;
- claim category;
- exact source-language text locator;
- English working translation source;
- principal limitations;
- protection emphasis;
- material amendment or prosecution context;
- overlap with other representatives;
- material differences;
- relevance to the proceeding; and
- analysis limitation.

### Case record

For each element of `cases`, preserve:

| Field | Requirement |
|---|---|
| `case_id` | Stable internal report identifier |
| `case_name` | Official or source-verified caption |
| `case_number` | Official docket, proceeding, or investigation number |
| `tribunal` | Court, tribunal, board, or agency |
| `jurisdiction` | Country and relevant territorial level |
| `filed_date` | Filing or institution date, labeled accurately |
| `verified_as_of` | Date current posture was checked |
| `plaintiffs` | Verified named plaintiffs or complainants |
| `defendants` | Verified named defendants or respondents |
| `target_role` | Target's role in this proceeding |
| `asserted_patents` | Verified patent identifiers |
| `asserted_claims` | Verified claim numbers when public |
| `allegations` | Party allegations, labeled as allegations |
| `defenses` | Pleaded or reported defenses, labeled accurately |
| `procedural_posture` | Current stage as of verification date |
| `disposition` | Accurate outcome or explicit absence of final disposition |
| `appeal` | Verified appeal status and identifier |
| `timeline` | Case-specific event records |
| `sources` | Primary locators first, secondary context second |
| `evidence_state` | Verification completeness |

### Timeline event

Each event should include:

- ISO or source-preserved date;
- case ID;
- event label;
- neutral description;
- event type;
- relevant patents;
- relevant claims;
- target role;
- source ID and locator;
- evidence state; and
- uncertainty note.

### Inventor record

Each inventor entry should include:

- normalized name;
- source variants;
- disambiguation method;
- identity confidence;
- recent filing count;
- counting method;
- yearly statistics;
- top classifications;
- technology themes;
- representative publications;
- current assignee only when verified;
- source and cutoff; and
- limitations.

### Conclusion record

Each geographic item should contain jurisdiction, evidence-qualified state, verified proceedings, asserted patents, family context, business-context input, reasoning, uncertainty, trigger, and action.

The litigation alert should contain current posture, disputed issues, verified deadlines or events, target role, counterparties, defenses, open evidence questions, monitoring cadence, and responsible owner.

The technology trend should contain observed period, counting basis, themes, representative evidence, alternative explanations, near-term hypothesis, medium-term hypothesis, long-term hypothesis, and confidence.

Each action should contain:

- priority;
- concrete action;
- owner;
- trigger;
- due date only when verified or user assigned;
- dependent evidence;
- source IDs; and
- completion criterion.

### Source record

For each element of `sources`, preserve:

- source ID;
- source type;
- title or label;
- issuing body;
- stable URL or record locator;
- docket entry, page, paragraph, claim, or event locator;
- publication or filing date;
- access date;
- language;
- translation provenance;
- coverage;
- limitation; and
- associated case, patent, event, or finding IDs.

### CSV exports

When CSV is requested, create separate files for:

1. `cases.csv`;
2. `asserted_patents.csv`;
3. `family_members.csv`;
4. `timeline.csv`;
5. `inventors.csv`;
6. `search_log.csv`; and
7. `sources.csv`.

Use UTF-8, stable headers, ISO dates, explicit empty values, and semicolon-separated stable IDs for many-to-many fields. Do not flatten allegations or holdings into an unlabeled free-text cell.

### Cross-artifact reconciliation

Before delivery, verify:

- JSON case IDs equal the set referenced by patents and timeline events;
- verified case count equals verified case records;
- verified asserted patent count equals qualifying patent records;
- family-member count follows the stated family and de-duplication rule;
- CSV row counts reconcile with JSON arrays;
- every HTML case and patent has a JSON counterpart;
- every material HTML fact has a source ID;
- every action has a trigger or rationale;
- no source ID points to a missing source record; and
- the displayed cutoff matches every output artifact.
