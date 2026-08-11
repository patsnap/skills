# Independent Verification Guide for FTO Report Review

Version: 9.0 localized international edition

## 1. Purpose

Use this guide to compare the search set in an existing FTO or patent-risk
report with a separately executed, reproducible, multi-route patent search.

Independent verification can reveal:

- technical concepts omitted from the original strategy;
- route-specific blind spots;
- identifier or family-normalization differences;
- newly published or newly granted rights;
- potentially material omitted families;
- stale claim or legal-status evidence;
- pending applications requiring monitoring.

It cannot prove that every relevant patent has been found and does not itself
determine infringement or freedom to operate.

## 2. Preconditions

Before searching, record:

| Field | Required detail |
|---|---|
| Target subject | Product/process, configuration, essential and optional features |
| Version | Design, release, formulation, sequence, drawing, or process version |
| Activity | Make, use, sell, offer, import, export, supply, launch, or other act |
| Jurisdiction | Country or regional system for each intended activity |
| Decision | Launch, design freeze, transaction, event, monitoring, or counsel review |
| Search cutoff | Date through which publications are sought |
| Status cutoff | Date at which legal status is assessed |
| Comparison unit | Publication, application, grant, simple family, extended family, or custom unit |
| Original set | Normalized identifiers and stated inclusion rule |
| Evidence limits | Missing annexes, unavailable queries, translations, or inaccessible sources |

Do not start with a title-only classification of the technology. Decompose the
actual product or process and confirm the facts with an appropriate technical
owner.

## 3. Route design

Use routes that retrieve documents through meaningfully different mechanisms.
Record dependencies between routes; different user interfaces do not guarantee
statistical independence.

### Route 1 — Semantic concept search

1. Express the target as complete technical concepts.
2. Create separate concepts for essential feature clusters.
3. Search claims, title/abstract, and description as supported.
4. Run broad and narrow variants.
5. Record provider, fields, filters, date, and result counts.
6. Retain route provenance for every screened result.

Semantic search is useful for vocabulary variation but can be opaque. Preserve
the natural-language query and all visible controls.

### Route 2 — Keyword and nested Boolean search

1. Build a terminology table for each feature.
2. Include synonyms, acronyms, spelling variants, translations, and scientific
   nomenclature as relevant.
3. Combine essential concepts with nested Boolean and proximity logic.
4. Search appropriate fields and test sensitivity to field restriction.
5. Record exclusions and the records removed by each exclusion.
6. Save exact queries and run dates.

Avoid unexplained keyword lists. The relationship between terms is part of the
search evidence.

### Route 3 — Classification search

1. Identify IPC/CPC candidates from official schemes and relevant seed patents.
2. Review definitions, notes, inclusions, exclusions, and hierarchy.
3. Test broader, narrower, and neighboring groups.
4. Combine classifications with discriminating concepts when necessary.
5. Record the scheme/version and selection rationale.

Classification coverage varies by field, jurisdiction, and document age. It is
a route, not a completeness guarantee.

### Route 4 — Entity, inventor, and citation search

1. Identify technically relevant assignees, applicants, inventors, and seeds.
2. Normalize spelling, transliteration, subsidiaries, predecessors, and known
   ownership changes.
3. Review backward and forward citations where useful.
4. Search examiner references or cited non-patent literature when appropriate.
5. State why each entity or seed was selected.

Known-player searching supplements concept searching. It must not define the
entire universe of possible rights holders.

### Route 5 — Temporal and pending-claim watchlist

1. Search recent publications near the cutoff.
2. Identify pending national/regional members for relevant families.
3. Record claims/features to monitor and current procedural state.
4. Define the event that triggers re-review.
5. Assign an owner and cadence aligned with prosecution and launch timing.

Pending applications are not currently enforceable patent claims. Keep them
outside the enforceable-risk list unless a granted member independently applies.

## 4. PatSnap MCP-assisted research

When configured, use the global PatSnap connectors that match the task:

| Connector | Endpoint | Use |
|---|---|---|
| PatSnap Patent Research (`patsnap_patent_research`) | `https://open.patsnap.com/marketplace/mcp-servers/patsnap-ip-searching` | Structured FTO review through `fto_review`; retrieve asynchronous output through `get_task` |
| Advanced Patent Search (`advanced_patent_search`) | `https://open.patsnap.com/marketplace/mcp-servers/patent-search` | Semantic, keyword, classification, entity, and filtered searches |
| Patent Briefing (`patent_briefing`) | `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing` | Claims, translated claims, description, bibliography, family, status, images, and technical summary |

Optional deeper legal-event research may use
[Global Core Patents](https://open.patsnap.com/marketplace/mcp-servers/core-patents)
when available.

For every call record connector, tool, request/query, filters, run date, returned
identifiers, and any task ID. Never copy an API key into the evidence record.
Confirm decision-material status or file-history facts against an authoritative
source when required.

## 5. Normalization

### 5.1 Publication identifiers

- retain country/authority code, number, and kind code when available;
- distinguish publication, application, and grant identifiers;
- remove presentation punctuation only for matching;
- preserve the display identifier and source URL separately;
- never merge records based only on a shared numeric stem.

### 5.2 Family units

State the family definition. For every member retain:

- priority data;
- jurisdiction and stage;
- publication/application/grant identifiers;
- current legal status and status date;
- current claim version where material;
- relationship to the selected family representative.

### 5.3 Deduplication

Record:

- raw results per route;
- duplicate publications;
- publications consolidated into families;
- excluded records and reasons;
- final retained publications and families.

The same record found by several routes remains one record with multiple route
provenance labels.

## 6. Comparison analysis

Let:

- `R` = normalized family set in the reviewed report;
- `S_i` = retained family set from independent route `i`;
- `U` = observed union of all `S_i`.

Report:

- size of each `S_i`;
- `|U|` and `|R|`;
- intersections between routes;
- pairwise Jaccard similarity `|S_i ∩ S_j| / |S_i ∪ S_j|`;
- `R \ U` (report-only families);
- `U \ R` (independent-only families);
- route provenance for every member;
- reasons for family or identifier differences.

These are observed-set measures, not true recall.

## 7. Omission review

For every independent-only family:

1. confirm the identifier and family mapping;
2. identify the target-jurisdiction member;
3. check legal status as of a stated date;
4. identify the current relevant claims;
5. compare claims with the defined product/process evidence;
6. assess whether it falls within the original report's stated scope;
7. classify the difference and document the reason.

Use these categories:

| Category | Meaning | Score effect |
|---|---|---|
| Identifier/family difference | Same substantive family represented differently | Usually none; fix normalization |
| Relevant non-material addition | In scope but no material current claim concern shown | Note coverage improvement |
| Potentially material omission | Status/claims/product mapping require further review | Deduct only for supported search-quality gap; escalate |
| Confirmed material omission | Current claim and product evidence support decision materiality | Material deduction; evaluate fatal condition if knowingly omitted |

Do not label an omission “high risk” from title, abstract, classification, or
semantic similarity alone.

## 8. Coverage estimation

### 8.1 Default rule

Report `Recall: Not estimated`. Show route coverage, observed union, and overlap.

### 8.2 Why overlap is insufficient

Patent-search routes are correlated through shared terminology, classifications,
citations, database indexing, seed documents, and reviewer decisions. The
unobserved relevant universe is unknown. High overlap can reflect dependence;
low overlap can reflect route diversity or noise.

### 8.3 Qualified heuristic exception

A Chapman, capture-recapture, Jackknife, or related estimate may be displayed
only when the reviewer documents:

1. the capture pools and comparison unit;
2. pool construction and screening equivalence;
3. independence assumptions or a dependence model;
4. stable family normalization;
5. estimator equation and uncertainty;
6. sensitivity to route grouping and exclusions;
7. known violations and their likely direction;
8. the label `qualified heuristic, not true recall`.

If any prerequisite is unsupported, omit the number. Never use a numeric
estimate as evidence of no infringement risk.

## 9. Script workflow

The bundled `scripts/fto_independent_search.py` does not call a network service.
It normalizes already retrieved results and calculates observed comparisons.

Prepare a JSON file containing:

- report patents/families;
- named route result arrays;
- publication identifiers and family keys;
- optional status, assignee, IPC/CPC, and pending indicators;
- optional estimator assumptions when genuinely supported.

Run:

```bash
python scripts/fto_independent_search.py normalized-routes.json comparison.json
```

Review the output for:

- normalization exceptions;
- observed union;
- route overlap matrix;
- report-only and independent-only lists;
- pending-application watchlist;
- explicit recall status.

The script output supports reviewer analysis. It does not decide relevance,
claim coverage, enforceability, or materiality.

## 10. Degraded mode

If search tools or source evidence are unavailable:

1. continue the supplied-report quality review;
2. state which routes could not be run;
3. state which conclusions are affected;
4. create reproducible route plans and evidence requests;
5. mark independent verification `Not performed`;
6. do not fabricate counts, overlaps, omissions, or status checks.

## 11. Evidence table

| ID | Route | Query/request | Provider/fields | Filters/date | Raw | Retained | Family rule | Limitation |
|---|---|---|---|---|---:|---:|---|---|
| R1 | Semantic | | | | | | | |
| R2 | Keyword/Boolean | | | | | | | |
| R3 | Classification | | | | | | | |
| R4 | Entity/citation | | | | | | | |
| R5 | Temporal/watchlist | | | | | | | |

## 12. Completion gate

Before describing verification as complete, confirm:

- target subject, version, activity, jurisdiction, and dates are explicit;
- all applicable routes were run or visibly marked unavailable;
- queries and tool calls are reproducible;
- identifiers and families are normalized under a stated convention;
- route provenance is retained;
- observed measures are not called true recall;
- omissions received status, claim, and product review before materiality labels;
- pending applications remain a separate watchlist;
- all limitations and re-review triggers are recorded;
- qualified counsel reviews decision-material legal conclusions.

## 13. Review boundary

Independent verification is a search-quality and evidence-comparison procedure.
It is not a legal opinion, does not establish a complete relevant universe, and
does not guarantee freedom to operate. Results remain limited by the specified
subject, jurisdiction, activity, claim version, evidence, provider coverage,
and review date.
