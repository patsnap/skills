# Cross-Section Evidence Synchronization Register

## Purpose

Maintain one authoritative registry for facts reused across sections s0–s9. Update the register before updating the report. This is a review-control artifact, not a substitute for the evidence register.

## Report metadata

| Field | Value | Evidence/source | Last reviewed | Owner |
|---|---|---|---|---|
| Report version | V0.0.0 | Release record | YYYY-MM-DD | |
| Report date | YYYY-MM-DD | Release record | YYYY-MM-DD | |
| Evidence cutoff | YYYY-MM-DD | Scope authorization | YYYY-MM-DD | |
| Decision context | | User authorization | YYYY-MM-DD | |
| Patent count unit | | Method record | YYYY-MM-DD | |
| Review status | draft / reviewed / approved | Review record | YYYY-MM-DD | |

## 1. Evidence-use register

| Evidence ID | Type | Stable identifier/link | Accepted finding | Sections used | Review depth | Limitations | Last reviewed |
|---|---|---|---|---|---|---|---|
| E1 | patent / paper / standard / case / market / web | | | s2, s4 | | | YYYY-MM-DD |

Rules:

- one evidence ID refers to one normalized record;
- every factual report statement resolves to accepted evidence;
- secondary repetition of one primary source is not independent corroboration;
- superseded or withdrawn evidence remains in history but is removed from current findings;
- section changes update all listed uses.

## 2. Patent identity and review register

| Evidence ID | Publication | Family ID | Jurisdiction | Priority/publication dates | Status as of | Claims reviewed | Product evidence date | Review priority | Sections | Specialist status |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | urgent/planned/monitor | s0, s4, s8 | |

Rules:

- distinguish publication, application, grant, and family IDs;
- record status as of a date;
- review priority is not an infringement conclusion;
- Section 8 technical options link to the same screening record;
- changed claim or product facts trigger all section reviews.

## 3. Market and economic data register

| Metric ID | Value/range | Unit/currency | Price year | Geography | Segment | Base/forecast year | Source/report/date | Scenario or estimate method | Sections | Last reviewed |
|---|---|---|---|---|---|---|---|---|---|---|
| M1 | | | | | | | | observed / publisher forecast / analyst scenario | s0, s1 | |

Rules:

- never reuse a number without the same definition and units;
- disclose currency conversion and inflation handling;
- publisher forecasts and analyst scenarios remain distinct;
- conflicting sources remain visible with scope differences.

## 4. Organization and competitive evidence register

| Organization ID | Canonical name | Aliases | Role/segment | Inclusion evidence | Technology-route evidence | Current event evidence/date | Confidence | Sections | Last reviewed |
|---|---|---|---|---|---|---|---|---|---|
| O1 | | | | | | | | s1, s3 | |

Rules:

- inclusion follows declared criteria, not nationality or prestige;
- corporate relationships and ownership have as-of dates;
- patent activity, products, partnerships, and announcements remain distinct;
- “no public information found” is not “no activity.”

## 5. Technology-route and maturity register

| Route ID | Definition/version | Current state | Maturity method/result | Supporting evidence | Contradicting evidence | Organizations | Sections | Review status |
|---|---|---|---|---|---|---|---|---|
| T1 | | | | | | | s0, s2, s3, s6 | |

Rules:

- route, maturity, adoption, and timing are separate;
- every state and maturity value cites evidence;
- conflicting classifications remain visible;
- changes propagate to recommendations and scenario sections.

## 6. Standards and regulation register

| Record ID | Body/jurisdiction | Identifier/title | Version/status | Clause/requirement | Effective/as-of date | Relevance | Sections | Reviewer |
|---|---|---|---|---|---|---|---|---|
| S1 | | | | | | | s0, s5, s6 | |

Rules:

- distinguish standard, regulation, guidance, draft, work item, and certification scheme;
- do not infer a requirement from a roadmap or draft;
- quote or paraphrase within licensing limits;
- jurisdiction and effective date must follow every material conclusion.

## 7. Candidate gap register

| Gap ID | Type | Bounded statement | Search IDs | Search universe | Contradicting evidence | Validation required | Sections | Status |
|---|---|---|---|---|---|---|---|---|
| G1 | patent / standard / application / evidence | Not observed in the reviewed dataset | | | | | s0, s6 | candidate |

Rules:

- no candidate is called a global white space;
- patent gaps are not FTO, novelty, or patentability conclusions;
- standards gaps distinguish absent clause, optionality, draft status, and search failure;
- every candidate has an invalidation condition.

## 8. Recommendation register

| Action ID | Decision action | Priority basis | Evidence IDs | Contradictions/risks | Owner | Time/milestone | Sections | Status |
|---|---|---|---|---|---|---|---|---|
| A1 | | | | | | | s0, s8 | proposed |

Rules:

- actions follow evidence and analysis; do not write s0 first;
- priority is decision-specific and not automatically mapped from patent labels;
- actions include owners, milestones, dependencies, and review triggers;
- legal, safety, regulatory, and financial actions receive appropriate review.

## 9. Cross-section reconciliation

| Check | Source section | Consumer section | Expected relationship | Status | Evidence | Last reviewed |
|---|---|---|---|---|---|---|
| Patent screening → decisions | s4 | s0 | Review priority and specialist action reconcile | | | |
| Patent screening → technical options | s4 | s8 | Same records and current claims/product facts | | | |
| Market evidence → decisions | s1 | s0 | Same metric definition/source | | | |
| Technology routes → company comparison | s2 | s3 | Same route vocabulary/version | | | |
| Patent/standards evidence → candidates | s4/s5 | s6 | Candidate statement cites underlying search/evidence | | | |
| Applications → vertical scenario | s7 | s9 | Same transfer conditions and maturity method | | | |

## 10. Release control

| Item | Expected | Actual | Status | Reviewer |
|---|---|---|---|---|
| Version in title/meta/footer | identical | | | |
| Report date | ISO date | | | |
| Evidence cutoff | ISO date | | | |
| Review status | machine metadata and visible text | | | |
| Source register | every accepted record exactly once | | | |
| Search logs | every research track or explicit omission | | | |
| Specialist boundaries | visible and resolved/withheld | | | |

## Change protocol

1. identify the authoritative row;
2. update the row and review date;
3. inspect every section in `Sections used`;
4. rerun derived counts and analyses;
5. update recommendations only after evidence sections;
6. record unresolved conflict;
7. run automated and manual QA;
8. approve or withhold release.
