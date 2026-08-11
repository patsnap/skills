# High-Value Patent Portfolio Screening Standard

## Purpose and boundary

This standard ranks patents within one documented candidate universe. It is a
portfolio-triage model, not a monetary valuation, validity opinion,
enforceability conclusion, technology-quality rating, or investment
recommendation. Scores are relative to the query result and should not be
compared across unrelated searches.

Record the following before retrieval:

- reviewed PatSnap query and query owner;
- legal entities, technologies, jurisdictions, and date scope;
- family definition and representative-publication rule;
- database and legal-status cutoff dates;
- scoring purpose, weights, selection ratio, and any override;
- whether citations, events, and status are counted by publication, member, or
  family; and
- known language, name-normalization, and coverage limitations.

## Scoring model

Score each returned candidate on a 100-point scale.

| Indicator | Weight | Primary REST evidence | Interpretation |
|---|---:|---|---|
| Simple-family forward-citation position | 30 | P015 `patent_cited.cited_by_simple_family` | Relative downstream patent attention; strongly age-, field-, office-, family-, and coverage-dependent |
| Simple-family size position | 30 | P014 `patent_family.simple_family` | Breadth of related filings; not geographic market coverage or enforceability by itself |
| Core-inventor membership | 20 | Inventors in the P002 candidate universe | Concentration signal within the scoped result, not inventor quality |
| Qualifying legal-event presence | 20 | P034, P027, P028, P029 | Activity signal; events may be favorable, adverse, neutral, historical, or irrelevant |

Default formula:

```text
total_score = citation_score + family_score + inventor_score + event_score
```

Store each component, raw value, missingness state, source endpoint, retrieval
time, and error separately. Never convert retrieval failure into factual zero.

## Numeric indicator normalization

### Candidate sets with at least ten records

Use an empirical percentile within the candidate universe:

```text
percentile(value) = count(candidate values <= value) / count(available candidate values)
citation_score = percentile(cited_by_simple_family) * 30
family_score = percentile(simple_family_count) * 30
```

Only available numeric observations belong in the percentile denominator.
Records with missing values receive zero points under the default policy, but
retain `missing` as their evidence state. The report must state the available
count and missing count for each indicator.

### Candidate sets with fewer than ten records

Use the source's deterministic fallback:

- all available values zero: 0 points;
- all non-zero available values equal: 15 points for a non-zero record;
- otherwise use the same available-observation percentile, flagged as unstable;
- missing: 0 points plus an explicit missing-data flag.

The original scripts awarded 15 to any non-zero value in every small set. The
localized implementation retains that behavior only for the equal-non-zero
case; mixed small sets use transparent percentiles so magnitude is not erased.

## Core-inventor rule

Define core inventors from the returned candidate universe unless the user
supplies a reviewed override.

1. Treat `|`, semicolon, full-width semicolon, and line breaks as inventor-record
   separators.
2. Do not split on comma or full-width comma. In common PatSnap output,
   `LASTNAME, FIRSTNAME|LASTNAME, FIRSTNAME` uses the comma inside one name and
   the vertical bar between names.
3. Trim whitespace and count each normalized exact-returned name once per
   patent.
4. Rank by candidate-set patent count descending.
5. For an initial top-five determination, break ties by normalized exact name
   ascending. After patent scores exist, record—but do not silently use—a
   score-based secondary analysis, because using final scores to define the
   inventors that contribute to those scores is circular.
6. The first five names are core inventors; fewer than five is allowed.

Do not automatically merge initials, transliterations, maiden names, reordered
names, or homonyms. State exact-name limitations. If the user provides a core
inventor list, preserve its provenance and mark the override in every report.

Core-inventor score:

- 20 if at least one inventor exactly matches the effective top-five/override;
- 0 otherwise.

## Legal-event categories

Qualifying source categories are:

| Normalized category | REST source | Expected array |
|---|---|---|
| Litigation | P034 | `patent_litigation_data` |
| Reexamination or invalidation | P027 | `patent_reexam_invalid_data` |
| License | P028 | `patent_license_data` |
| Transfer | P029 | `patent_transfer_data` |

Event score:

- 20 if at least one verified event record is returned in any category;
- 0 if all four endpoint results are successfully retrieved and empty;
- 0 plus `missing` if one or more required event endpoints fail or are not run.

Preserve event date, proceeding/case number, event type, parties, country or
authority, source locator, endpoint, and retrieval time when returned. A hit is
not inherently positive: litigation or invalidation may reduce value; a license
or transfer may be intra-group, expired, disputed, or unrelated to the relevant
member. Reports must use “event activity detected,” never “valuable because a
legal event exists.”

## Selection ratio

Default:

```text
selected_count = ceil(candidate_count * 0.10)
maximum_count = ceil(candidate_count * 0.15)
```

Rules:

- zero candidates produces zero selections and a valid no-results state;
- any non-zero candidate set produces at least one selection;
- do not exceed the 15% ceiling without a recorded user override;
- resolve cutoff ties with the deterministic rules below rather than selecting
  every tied record; and
- report both the P002-reported total and the deduplicated/scored count.

## Deterministic tie-breaks

When total scores tie, rank by:

1. higher available simple-family forward-citation count;
2. higher available simple-family count;
3. verified legal-event hit;
4. core-inventor hit;
5. more verified event categories;
6. earlier valid application date;
7. publication number ascending;
8. stable internal identifier ascending.

Missing numeric values sort below available values, including a factual zero.

## Required checkpoint states

Every enrichment field uses one of:

- `available`: endpoint returned a usable value;
- `empty`: endpoint call succeeded and returned no relevant record;
- `missing`: source record lacks the requested field;
- `error`: endpoint or parsing failed;
- `not_run`: stage was intentionally skipped.

Each checkpoint records schema version, run ID, generated-at timestamp, query
hash (not credentials), source mode (`rest` or `mcp_import`), input filename,
upstream checkpoint hash, endpoint/path or connector/tool, retrieval time, and
errors. A consumer must reject an incompatible schema version.

## Required report columns

| Column | Content |
|---|---|
| Rank | Position after score and tie-break rules |
| Screening score | 0–100, including all four components |
| Selection rationale | Compact evidence-based summary with missingness |
| Publication number | Stable identifier; hyperlink only when a verified safe global URL exists |
| Original title | P002 title and language when available |
| Abstract drawing | P021 image or “No usable abstract drawing returned” |
| Current assignee or owner | Source label, entity string, and cutoff if available |
| Simple legal status | Raw P041 status plus checked-as-of date; not enforceability proof |
| PatSnap title | P025 English title when returned |
| Technical problem | P025 English summary with provenance |
| Technical approach | P025 English summary with provenance |
| Technical benefit or effect | P025 English summary with provenance |
| Simple-family forward citations | Raw value, percentile, state, and cutoff |
| Simple-family size | Raw value, percentile, state, and family rule |
| Core-inventor match | Yes/No and exact matched names |
| Legal-event activity | Normalized categories and event-level evidence |
| Data gaps | Missing/error/not-run fields and remediation action |

## Rationale wording

Use neutral, evidence-bounded language:

```text
Simple-family forward citations: 14 (candidate-set P92; available).
Simple-family size: 8 (candidate-set P85; available). Core-inventor match:
Alex Morgan. Event activity detected: License (1), Transfer (2). Selected under
the documented 30/30/20/20 screening model; no monetary-value conclusion.
```

When evidence is incomplete:

```text
Simple-family forward-citation evidence: error (P015 timeout; zero points under
the missing-data policy). Simple-family size: 6 (candidate-set P85; available).
No core-inventor match. P034 and P028 returned empty; P027 and P029 were not
retrieved. Legal-event absence cannot be concluded.
```

## Quality and release gates

- Query scope, cutoffs, family rule, scoring version, weights, and overrides are
  visible in both report and trace.
- P002 total, deduplicated count, scored count, missing counts, and selected
  count reconcile.
- Every selected record can be traced through all checkpoints.
- Available zero and missing/error are never conflated.
- Inventor names are not fragmented on Western commas.
- Legal-event records retain category and event-level context.
- Dynamic HTML values are escaped; only HTTP(S) links are rendered.
- Reports use text labels, semantic tables, responsive local overflow, US-Letter
  print rules, and no color-only meaning.
- Secrets, local paths, China-only domains, guessed product URLs, and expiring
  image credentials are absent from persisted reports.
- A human reviewer approves the query, scoring interpretation, exceptions, and
  final narrative before distribution.
