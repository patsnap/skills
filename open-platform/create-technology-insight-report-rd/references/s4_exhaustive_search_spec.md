# Section 4 Patent-Landscape Coverage and Claim-Screening Specification

## Purpose

Section 4 describes the patent-search universe, coverage, activity patterns, representative records, and claim-relevance review queue. It does not establish infringement, freedom to operate, validity, patentability, or global white space.

## Correct the source's “exhaustive” terminology

The frozen source required an exhaustive download and prohibited the word “sample.” That is not portable or technically defensible across databases, connectors, limits, languages, families, and changing records.

Use precise terms:

- `matched_total`: database-reported or estimated matches for one exact query at one time;
- `returned records`: records delivered by the connector/page sequence;
- `reviewed records`: records actually inspected;
- `accepted records`: reviewed records meeting inclusion rules;
- `publication count`: distinct publication records;
- `simple-family count`: normalized simple families;
- `analysis set`: records used for a stated metric;
- `sample`: a deliberately selected subset, with selection method and limitations.

Never call `matched_total` an exhaustively reviewed set.

## Required preparation

- decision context;
- technical and product boundary;
- jurisdictions and languages;
- evidence cutoff and search dates;
- patent count unit;
- family normalization;
- legal-status “as of” rule;
- classification/version scope;
- claim-screening question;
- target product/feature evidence authorized for comparison;
- patent-professional review boundary;
- connector/tool and callable schema.

## Verified global PatSnap services

- `advanced_patent_search`: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- `patent_briefing`: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing

Use only parameters currently exposed. Do not invent source-only fetch, valuation, legal-event, citation, trend, or full-export functions.

## Iterative coverage workflow

### Step 1 — Define concepts and exclusions

Create a concept matrix:

| Concept | Synonyms | Mechanisms | Parameters | Classifications | Product anchors | Exclusions |
|---|---|---|---|---|---|---|
| Functional concept | | | | | | |

### Step 2 — Classification exploration

- identify relevant IPC/CPC or other classifications;
- review definitions and neighboring classes;
- record classification version/date when material;
- do not assume one class captures the complete technology;
- run classification-only and classification-plus-concept queries where useful.

### Step 3 — Multilingual and terminology expansion

- use languages relevant to the decision;
- include spelling, acronym, transliteration, legacy, and emerging terms;
- use claims/title/abstract/description fields as supported;
- retain query variants and their incremental accepted records.

### Step 4 — Actor and citation expansion

When justified:

- normalize applicant and assignee aliases;
- inspect relevant inventors without overclaiming identity or movement;
- inspect backward/forward citations and family relationships;
- search discovered mechanisms and classifications;
- log incremental coverage.

### Step 5 — Time and status review

- choose time windows for the decision, not a fixed recent period;
- include historical records when needed for evolution or prior art;
- keep pending, granted, expired, abandoned, lapsed, or other statuses visible when relevant;
- record status and owner as of a date;
- do not equate active/granted with technical or legal risk.

### Step 6 — Pagination and segmentation

If the connector truncates or limits results:

- paginate using supported cursors/offsets;
- segment by date, classification, jurisdiction, or other non-overlapping field only when the segmentation can be reconciled;
- record overlap and deduplication;
- compare segment totals with connector totals;
- disclose unreachable records and result caps.

Do not use the source's 500-record or five-year segmentation values as universal limits.

### Step 7 — Saturation review

Track new accepted families/publications contributed by each query iteration. A plateau may support operational stopping, but never proves complete recall.

Record:

- iteration;
- query ID;
- returned/reviewed/accepted counts;
- incremental unique families;
- cumulative families;
- reason to continue or stop;
- known coverage risks.

### Step 8 — Gap-check protocol

For a candidate gap:

1. run alternative terminology;
2. run neighboring classifications;
3. run mechanism/parameter queries;
4. run relevant languages and jurisdictions;
5. inspect citation/family/actor paths;
6. inspect non-patent evidence and commercial activity;
7. record every query and result;
8. state only “not observed in the reviewed search universe” unless a separate specialist analysis supports more.

There is no magic three-zero-query rule.

## Search-log minimum

```json
{
  "search_id": "PS-01",
  "tool": "advanced_patent_search",
  "searched_at": "2026-08-08T12:00:00Z",
  "query": "exact query",
  "filters": {},
  "languages": ["English"],
  "requested_limit": 100,
  "matched_total": null,
  "matched_total_type": "reported | estimated | unavailable",
  "returned_count": 100,
  "reviewed_count": 38,
  "accepted_ids": [],
  "pagination": "cursor and truncation description",
  "deduplication": "publication and simple-family rules",
  "limitations": ""
}
```

## Landscape metrics

Every metric states:

- query/search universe;
- count unit;
- date field and range;
- jurisdiction treatment;
- family normalization;
- status filter;
- denominator;
- coverage limitations;
- refresh date.

Do not build trends, rankings, or IPC shares from an undisclosed top-N relevance return. A transparent sample may be used for qualitative analysis, never mislabeled as population statistics.

## Claim-relevance screening

### Purpose

Identify records requiring deeper patent-professional review against a defined product or feature set.

### Inputs

- current claims from the relevant family member and jurisdiction;
- prosecution, opposition, litigation, or status context when material and available;
- dated product/feature evidence;
- claim-term interpretations explicitly marked as preliminary;
- jurisdiction and temporal scope;
- specialist reviewer.

### Element-by-element record

| Claim | Element | Evidence location | Product/feature evidence | Preliminary correspondence | Uncertainty | Specialist action |
|---|---|---|---|---|---|---|

Allowed correspondence labels:

- observed correspondence;
- possible correspondence;
- not observed in supplied material;
- insufficient information;
- requires claim construction or legal review.

Do not calculate infringement risk from a percentage of elements. All-elements rules, equivalents, claim construction, ownership, status, jurisdiction, defenses, exceptions, and product facts require qualified legal analysis.

### Review priority

Prioritize specialist review using transparent factors such as:

- product/feature relevance;
- directness of claim correspondence;
- current status and jurisdiction;
- business exposure;
- uncertainty;
- implementation timing;
- available alternatives.

Use `urgent`, `planned`, or `monitor` only as internal review priority, not a legal risk conclusion.

## Technical design options

For a screened record, Section 8 may document:

- change a feature or architecture;
- use a different technical principle;
- alter sequence, interface, parameter, or system boundary;
- obtain further evidence or testing;
- seek a license, partnership, acquisition, challenge, or legal opinion.

Every option states technical feasibility, performance/cost/safety consequences, validation needs, and patent-professional review. Do not call an option a successful design-around.

## Section 4 minimum content

- scope, cutoff, tool, query families, classifications, languages, and jurisdictions;
- search-log table with matched/returned/reviewed/accepted distinctions;
- patent count unit and family/entity normalization;
- coverage/truncation/saturation limitations;
- activity metrics only where denominators support them;
- representative evidence with stable links;
- claim-relevance review queue with bounded language;
- candidate gaps with gap-check IDs and non-globality disclaimer;
- complete source register references;
- patent-professional review boundary.

## Prohibited claims

- “exhaustive worldwide search” without defensible proof;
- `matched_total` equals records reviewed;
- no result means no patent exists;
- a high citation count equals broad enforceable scope;
- a granted/active patent automatically creates infringement risk;
- a percentage of claim elements determines infringement;
- a technical modification confirms non-infringement;
- a landscape substitutes for FTO.

## Stage gate

- [ ] Search universe and count unit are explicit.
- [ ] All searches are reproducibly logged.
- [ ] Pagination/truncation and coverage are disclosed.
- [ ] Family and entity normalization are documented.
- [ ] Statistics use an appropriate analysis set and denominator.
- [ ] Claim screening uses current claim text and defined product evidence.
- [ ] No automated infringement/FTO conclusion appears.
- [ ] Candidate gaps use bounded language and gap-check IDs.
- [ ] Technical options retain validation and specialist-review requirements.
- [ ] Every patent identifier and link is verified.
