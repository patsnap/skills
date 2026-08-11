# Query and Taxonomy Construction Methodology

Use this reference in Stage 1 search/de-noising and Stage 3 taxonomy design.
It preserves the source’s expert query and classification logic while making exact syntax,
languages, authorities, dates, counting rules, and thresholds project-specific and verifiable.

The examples are structural, not live query strings.
Verify every operator against the current PatSnap product or connector schema before execution.

## Part A — Expert query construction

The main difference between a keyword bag and an analyst-grade query is controlled structure:

- field-scoped clauses;
- a constant positive topic anchor;
- relation/proximity controls;
- classifications used as parallel recall routes;
- tiered exclusions with reasons;
- one consistent scope envelope;
- measured precision and recall signals.

## A1 — Field scope is the primary precision control

PatSnap products may expose title, abstract, claim, description, assignee, authority,
classification, priority-date, and other field operators.
The source uses operators such as `TTL`, `TA`, `TAC`, `TACD`, `DESC_*`, `IPC`, `CPC`,
`all_an`, `AUTHORITY`, and `E_PRIORITY_DATE`.

Treat these as syntax candidates requiring live verification.

| Conceptual scope | Use |
|---|---|
| Title | Highest precision for defining terms or decisive title exclusions |
| Title + abstract | Default core-concept recall |
| Title + abstract + claims | Concepts commonly expressed in claims, such as control logic |
| Title + abstract + claims + description | Broad positive topic anchor |
| Description sections | Targeted embodiment/background inclusion or exclusion when supported |
| IPC/CPC | Classification-assisted recall and controlled exclusion |
| Applicant/assignee | Entity supplements and entity-specific exclusions |
| Authority and dates | Consistent scope envelope |

Rule of thumb:

1. anchor the domain broadly;
2. define the branch at a medium or narrow field scope;
3. cut noise with the narrowest decisive field;
4. document why each field was chosen.

## A2 — Constant positive topic anchor

Every branch query should include a stable positive domain anchor containing:

- official technical names;
- common alternatives;
- abbreviations;
- relevant language variants;
- spelling and transliteration variants;
- legacy names where useful.

Conceptual form:

```text
BRANCH_CLAUSE
AND BROAD_FIELD:(domain_term_1 OR domain_term_2 OR abbreviation OR language_variant ...)
```

A positive anchor is more robust than relying only on an open-ended exclusion list.
Reuse one versioned anchor across branches unless a documented exception is required.

## A3 — Relation and proximity control

When the live search syntax supports it, use proximity to express technical relationships.

| Relation | Use |
|---|---|
| Same sentence | Concept/action or component/effect pairs that must be contextually related |
| Within N words | Tight relationship such as component + mechanism |
| Plain AND | Terms may appear anywhere in the selected field |

Noise-reduction escalation:

```text
AND
-> same sentence
-> within N words
-> move the weaker term to title or title/abstract
-> add a verified classification anchor
```

Choose N from sampled evidence; do not use a universal distance.

## A4 — Classification as a parallel recall route

Do not use IPC/CPC only as a final filter.
Use classifications to rescue weaker terminology and to capture technical concepts expressed differently.

```text
strong_keyword_clause
OR (weak_or_ambiguous_term AND verified_classification_anchor)
OR highly_specific_self_sufficient_classification
```

Rules:

- a strong phrase may stand alone;
- a weak term should be anchored;
- a highly specific class may be a separate recall path after definition review;
- main-classification exclusions may remove primarily off-topic records while tolerating secondary references;
- every classification must have a current plain-language definition and version/date.

Classification coverage varies by office, period, field, and record.
Do not treat a class as ground truth for relevance.

## A5 — Tiered exclusions

Exclusions are not a flat blacklist.

| Tier | Use | Risk control |
|---|---|---|
| Whole classification | Entire off-scope domain | Validate near-miss false negatives |
| Main classification | Record is primarily about another field | Retain secondary-use records where relevant |
| Title term | Title mention is decisive evidence of wrong scope | Confirm homonyms and negation |
| Description/embodiment term | Specific embodiment creates repeated noise | Ensure useful cross-domain embodiments are not lost |
| Applicant/assignee | Known entity repeatedly pollutes a branch | Document why entity-based exclusion is analytically valid |

Every exclusion record contains:

```text
exclusion_id
field
term_or_class_or_entity
reason
examples_removed
near_miss_sample
false_negative_risk
approved_by
query_version
```

An exclusion without a reason and near-miss review is not production-ready.

## A6 — Canonical branch-query structure

```text
(
  strong field-scoped terms
  OR (weak terms AND verified IPC/CPC anchor)
  OR self-sufficient specific classification
)
AND constant topic anchor
NOT tiered exclusions with recorded reasons
AND scope envelope
```

At Checkpoint 1, show these four parts separately:

1. branch recall paths;
2. constant topic anchor;
3. exclusions and reasons;
4. authority/date/entity/document/family envelope.

## A7 — Scope envelope

Set once and reuse across comparable branches:

- authority/jurisdiction scope;
- date field and range;
- family or document count unit;
- application/publication/grant kinds;
- entity scope;
- language/translation rules;
- status filter, if any;
- database and retrieval cutoff.

Use earliest priority date for technology chronology when appropriate.
Use filing/publication/legal-event dates only when the business question requires them.
State which field is used and why.

Do not default to fixed authorities or a fixed 2023 start.

## A8 — Query version record

```text
query_id
branch_id
version
business_question
strong_terms
weak_terms
classification_paths
constant_anchor
proximity_rules
exclusions
scope_envelope
live_syntax_verified_at
matched_total
candidate_count
known_relevant_tests
known_irrelevant_tests
limitations
```

Never silently edit a query after analysis begins.

## Part B — Technology breakdown methodology

## B1 — Four-column structure

| Column | Content | Rule |
|---|---|---|
| Level 1 | Major technical domain | Usually 4–6 architecture-level branches |
| Level 2 | Subsystem, capability, or functional branch | Usually 3–8 per parent where supported |
| Level 3 | Concrete taggable technique | Atomic primary tag with a testable membership rule |
| Technical description | What it does, why it matters, include/exclude criteria | Written for consistent human tagging |

Approximately 40 Level-3 primary tags is a practical human-consistency ceiling.
It is not a reason to merge technically material distinctions blindly.

## B2 — Two-pass decomposition

### Pass 1 — Top-down architecture

Start from how the system is built and used:

- structures and hardware;
- materials and processes;
- sensing, control, computation, and software;
- interfaces and system integration;
- manufacturing and test;
- products, applications, and operating environments.

This creates a stable skeleton independent of the current patent distribution.

### Pass 2 — Bottom-up evidence

Use seed searches, sampled abstracts/claims/descriptions, and clustering evidence to:

- confirm nodes;
- split overly broad nodes;
- merge empty or indistinguishable nodes;
- expose missing technical routes;
- define cross-cutting tags;
- refine include/exclude rules.

The final taxonomy reconciles architecture and evidence.

## B3 — Granularity and overlap controls

A Level-3 tag must be:

- searchable through a distinct rule;
- describable in one or two sentences;
- distinguishable from primary siblings;
- meaningful to the decision;
- taggable from the available evidence.

If a patent fits multiple primary siblings frequently:

1. sharpen the definitions;
2. choose a documented primary-tag priority rule; or
3. move the shared concept to a separate multi-label dimension.

Multi-label statistics must state whether one record contributes to more than one cell.

## B4 — Key technical questions

Create a parallel list of open technical problems.
These questions drive deep reading and route interpretation; they are not taxonomy tags.

Each question contains:

```text
question_id
branch_ids
neutral_problem_statement
why_it_matters
requirements_or_effects
evidence_ids
representative_family_candidates
route_hypotheses
uncertainty
```

Target at least ten across major branches when the evidence supports them.
Do not invent questions to meet a quota.

## B5 — Recommended patent packages

Each decision-priority branch, scenario, player, or problem may become a package.

Target:

- three to ten representative families per package;
- at least three for a route narrative;
- at least ten packages for a full project when the field supports them.

Selection criteria:

- technical relevance;
- representative mechanism;
- problem/effect evidence;
- family/citation/status signals;
- player or application relevance;
- claim readability;
- review depth;
- decision fit.

Recommendation reasons use evidence-backed categories such as:

- technically differentiated route;
- novel application scenario;
- documented performance improvement;
- distinctive function or interaction;
- representative competitor approach;
- important legal/asset follow-up signal.

Avoid marketing labels such as “disruptive” unless the evidence and definition justify them.

## Part C — Applying the methodology across the suite

| Suite stage | Application |
|---|---|
| `search-patents-ip` Stage 1 | Build anchor, recall paths, tiered exclusions, scope envelope, and versioned queries |
| Stage 1 Checkpoint | Present the four query components plus precision and near-miss results |
| `tag-patent-search-results-ip` Stage 3 | Propose the four-column taxonomy and key-question list |
| Stage 3 patent packages | Apply transparent selection and recommendation reasons |
| `analyze-patent-search-results-ip` Stage 2 | Keep rule-hit branches separate from human-reviewed tags |
| `create-patent-search-report-ip` Stage 4 | Explain taxonomy, package, evidence, and uncertainty in the report |

## Part D — Precision and recall validation

## D1 — Precision sample

For each branch:

1. draw a random or reproducible sample;
2. use 20–30 records when the branch is large enough;
3. read title and abstract, then claims/description where needed;
4. apply the written Level-3 or branch membership rule;
5. record Relevant, Not relevant, or Unresolved;
6. calculate estimated precision from resolved records;
7. report sample size and uncertainty.

```text
estimated_precision = relevant / (relevant + not_relevant)
```

Do not count Unresolved as relevant.

## D2 — Near-miss recall signal

Sample from:

- records removed by each material exclusion;
- known relevant seeds missed by the query;
- adjacent classification buckets;
- alternate language or terminology results;
- records just outside proximity/field limits.

Measure how often useful records were excluded and document likely recall gaps.
This is a recall sanity check, not proof of complete recall.

## D3 — Acceptance decisions

The source suggests 80% precision as a branch target.
Use it as a planning default only.

Set the project threshold based on:

- use case;
- prevalence;
- cost of false positives and false negatives;
- downstream human review capacity;
- branch importance;
- sample size and confidence.

Low-precision branches require a query revision or an approved manual-review plan.
High precision with weak recall evidence is not enough.

## D4 — Checkpoint table

| Branch | Definition | Strong/weak/classification paths | Anchor | Exclusions | Matched total | Sample | Relevant | Not relevant | Unresolved | Precision | Near-miss result | Decision |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|

The table makes query quality auditable rather than asserted.

## Quality checklist

- Exact live query syntax was verified.
- Every branch uses a positive anchor.
- Weak terms are anchored by relation, field, or classification.
- Every exclusion has a reason and near-miss test.
- Scope envelope is comparable across branches.
- Query versions and cutoffs are recorded.
- Precision sample and unresolved records are visible.
- Recall is discussed cautiously.
- Level-3 tags have include/exclude rules.
- Primary tags are distinguishable; cross-cutting labels are explicit.
- Multi-label duplicate counting is documented.
- Question and package targets are not padded.
- Confidential historical query strings or customer taxonomies are not reused.
