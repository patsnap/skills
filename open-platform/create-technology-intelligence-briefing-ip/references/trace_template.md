# Technology intelligence briefing — research trace

> Complete this record with actual values. Use `not_executed`, `unavailable`, or `not_applicable`; never leave an evidentiary field ambiguous.

## 1. Run identity and decision context

| Field | Value |
|---|---|
| Run ID | |
| Briefing title | |
| Analyst/reviewer | |
| Request received | |
| Retrieval started/ended | |
| Evidence cutoff | |
| Intended decision | |
| Intended audience | |
| Confidentiality | |
| HTML output | |
| Trace version | |

### Original request

```text

```

### Normalized research question



### Assumptions and pending confirmations

| ID | Assumption/question | Impact | Status | Resolution/evidence |
|---|---|---|---|---|
| A-01 | | | | |

## 2. Confirmed scope

| Dimension | Included | Excluded | Rationale |
|---|---|---|---|
| Companies/legal entities | | | |
| Technology | | | |
| Patent jurisdictions | | | |
| Geographic markets | | | |
| Patent date field/range | | | |
| Document types | | | |
| Languages | | | |
| Literature scope | | | |
| News scope | | | |

### Counting and selection rules

| Rule | Definition |
|---|---|
| Population counting unit | |
| Family definition | |
| Deduplication key | |
| Representative selection | |
| Display limit | |
| Trend date field | |
| Partial-period treatment | |

## 3. Entity resolution

| Input name | Canonical English name | Searched legal name | Relationship | Included | Evidence | Limitation |
|---|---|---|---|---|---|---|
| | | | | Pending | | |

### Alias-source use

| Alias-reference entry | Candidate names reviewed | Mixed-entity warning | Live validation | Decision |
|---|---|---|---|---|
| | | | | |

## 4. Technology definition and query development

### Concept matrix

| Concept | English terms | Local-language terms | Classification | Exclusions | Evidence |
|---|---|---|---|---|---|
| | | | | | |

### Query revision log

| Version | Layer | Exact query/formula | Test size | Relevant | Noise observed | Change made |
|---|---|---|---:|---:|---|---|
| Q-01 | Broad | | | | | |

### Frozen search strategy

```text

```

## 5. Patent retrieval provenance

Record one row per executed request.

| Request ID | Connector | Tool | Query/parameters | Jurisdictions | Date field/range | Counting unit | Family rule | Population count | Returned records | Retrieval time | Warning |
|---|---|---|---|---|---|---|---|---:|---:|---|---|
| P-01 | | | | | | | | | | | |

### Population versus displayed sample

| Bucket | Population count | Count status/source | Candidate records reviewed | Displayed records | Selection method |
|---|---:|---|---:|---:|---|
| | | | | | |

Never fill `Population count` with the length of a limited page unless the connector explicitly defines that page as the complete population.

### Deduplication log

| Input records | Output records | Rule | Duplicate groups reviewed | Exceptions |
|---:|---:|---|---:|---|
| | | | | |

## 6. Selected-patent verification

| Patent ID | Why selected | Bibliography source | Family source | Claims/description source | Status source/as-of | Summary evidence | Limitation |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

### Connector operations

| Request ID | Connector | Exact tool | Patent IDs | Fields requested | Records returned | Retrieval time | Error/retry |
|---|---|---|---|---|---:|---|---|
| D-01 | | | | | | | |

## 7. Literature evidence

| Literature request | Database/connector | Exact query | Filters | Results reviewed | Displayed | Retrieval date | Limitation |
|---|---|---|---|---:|---:|---|---|
| L-01 | | | | | | | |

| DOI/stable ID | Citation | Reason included | Summary evidence | Publication status | Source URL |
|---|---|---|---|---|---|
| | | | | | |

## 8. News and current-event evidence

| News request | Research tool/source | Exact query | Date range | Results reviewed | Retrieval date | Limitation |
|---|---|---|---|---:|---|---|
| N-01 | | | | | | |

| Headline | Publisher | Publication date | Event date | Primary/secondary | Relevance | URL |
|---|---|---|---|---|---|---|
| | | | | | | |

Search-result snippets are discovery aids, not final evidence.

## 9. Analysis and calculations

### Trend calculations

| Figure/table | Input population | Date field | Counting unit | Formula/transformation | Missing/partial data | Interpretation limit |
|---|---|---|---|---|---|---|
| | | | | | | |

### Topic/subtechnology assignment

| Category | Definition | Assignment method | Patent IDs | Reviewer | Ambiguity |
|---|---|---|---|---|---|
| | | | | | |

### Word/term frequency

| Source text field | Population/sample | Normalization | Stopwords | Phrase method | Limitation |
|---|---|---|---|---|---|
| | | | | | |

### Observation-to-interpretation register

| ID | Observed evidence | Calculation | Analyst interpretation | Confidence | Alternative explanation |
|---|---|---|---|---|---|
| I-01 | | | | | |

## 10. Report data integrity

| Check | Expected | Actual | Pass/fail | Correction |
|---|---|---|---|---|
| Every cited patent exists in `PATENTS` | 100% | | | |
| Company references resolve | 100% | | | |
| Subtechnology references resolve | 100% | | | |
| Population/display counts separated | Yes | | | |
| Patent URLs safe and verified | 100% | | | |
| DOI links validly formed | 100% | | | |
| News source/date/URL present | 100% | | | |
| Unavailable sections visible | Yes | | | |
| Untrusted text escaped | Yes | | | |
| No unresolved evidence placeholder | Yes | | | |

## 11. HTML and visual QA

| Check | Pass/fail | Evidence/notes |
|---|---|---|
| `lang="en"`, UTF-8, semantic headings | | |
| Keyboard-operable disclosure controls | | |
| Visible focus styles | | |
| No color-only meaning | | |
| Explicit units/counting levels | | |
| Responsive tables/cards | | |
| Print exposes all substantive sections | | |
| Sources remain visible in print | | |
| No gradient, emoji status, or automatic browser launch | | |
| Unsafe link schemes rejected | | |

## 12. Corrections, limitations, and release

### Correction log

| Time | Affected item | Problem | Correction | Reviewer |
|---|---|---|---|---|
| | | | | |

### Known limitations

- Database and connector coverage:
- Entity-resolution uncertainty:
- Query and language limitations:
- Family/counting limitations:
- Legal-status timing limitations:
- Literature coverage limitations:
- News/currentness limitations:
- Analytical limitations:

### Release decision

| Field | Value |
|---|---|
| Validation gate | Pass / Fail |
| Reviewer | |
| Review date | |
| Release state | Draft / Ready for review / Released |
| Required follow-up | |

### Final scope statement



### Final limitations statement


