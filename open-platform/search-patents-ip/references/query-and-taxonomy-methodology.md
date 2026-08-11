# Query and Preliminary Taxonomy Methodology

Use this reference in Stage 1 to construct auditable patent-search branches, validate
their boundary, and export a preliminary hierarchy for later Stage 3 and human review.

## Contents

- [Part A — expert query construction](#part-a--expert-query-construction)
- [Part B — preliminary taxonomy design](#part-b--preliminary-taxonomy-design)
- [Part C — hierarchy export](#part-c--hierarchy-export)
- [Part D — precision and recall validation](#part-d--precision-and-recall-validation)

## Part A — expert query construction

### A1. Assign field scope by concept decisiveness

Classify terms before writing the query:

| Term role | Typical scope |
|---|---|
| Highly distinctive technology or mechanism | Title/abstract/claims, with title-only test where justified |
| Necessary but broad context | Claims/description with a constant topic anchor |
| Functional or effect language | Claims/description, usually near an object or mechanism |
| Product/application term | Title/abstract or explicit application branch |
| Noise indicator | Staged exclusion only after reviewing false positives |

The source names product fields such as `TTL_ALL`, `TA_ALL`, `TAC_ALL`, `TACD_ALL`,
and `DESC_S`. Treat them as syntax candidates. Inspect `advanced_patent_search` and
use only fields and operators documented by the active global schema. Record the
semantic mapping and any loss of field precision.

Do not broaden every term to full text. A decisive term in an overly broad field can
create large, systematic noise.

### A2. Maintain a constant topic anchor

Build a stable disjunction that establishes the technical domain. Reuse the exact
versioned anchor in every branch so branch comparisons share a common boundary.

The anchor should:

- include the minimum set of domain-defining terms/classifications;
- cover relevant languages and transliterations;
- avoid application-specific terms that would suppress valid branches;
- remain separately inspectable in `search_config.json`; and
- change only through a new query version with a reason and count impact.

### A3. Escalate proximity deliberately

Test relations from broader to narrower:

1. Boolean co-occurrence;
2. sentence or paragraph proximity if supported;
3. word-distance proximity with documented order/distance semantics; and
4. title-focused evidence for highly distinctive concepts.

The source ladder `AND → $SEN → $Wn → TTL_ALL` is not universal syntax. Verify the
live operator. Choose the least restrictive form that meets the validation target;
do not use title-only scope merely to inflate measured precision.

Record every proximity expression, distance, order rule, and rationale.

### A4. Derive IPC/CPC from evidence

Use relevant seed patents and official classification definitions to identify IPC/CPC
candidates.

1. Start from confirmed positive records.
2. Extract their codes at appropriate hierarchy depth.
3. Read official definitions, notes, and neighboring groups.
4. Test codes independently and combined with the anchor.
5. sample false positives and false negatives.
6. retain only codes with a documented retrieval role.

Never fabricate a class or infer its meaning from the code alone. Record scheme,
version/date where available, hierarchy level, seed evidence, and inclusion reason.

### A5. Apply tiered exclusions

Every exclusion requires a false-positive example, reason, scope, and near-miss check.
Escalate from the narrowest safe exclusion:

1. distinctive title phrase;
2. specific embodiment or application context;
3. main/primary classification where the schema supports it;
4. whole IPC/CPC group only with strong evidence; and
5. organization exclusion only for a documented non-domain collision.

Avoid excluding a whole class, jurisdiction, language, or organization to solve a
small noise cluster. Keep each rule independently removable and compare before/after
counts and missed known positives.

### A6. Use the four-part branch skeleton

Each branch contains:

```text
(strong technical clause)
OR (weaker terms AND relevant classification)
OR (self-sufficient classification path)
all constrained by (constant topic anchor)
and followed by (versioned exclusion block)
```

Not every branch needs all three recall paths. Preserve an empty path explicitly with
a reason instead of filling it with weak terms.

For each branch record:

- `branch_id`, name, question, inclusion and exclusion boundary;
- strong/weak/short concepts and language variants;
- field and proximity mapping;
- anchor version;
- IPC/CPC paths and evidence;
- each exclusion and rationale;
- exact query/request and connector schema version;
- date, jurisdiction, unit, and family settings;
- result-count/cap status; and
- precision/recall validation results.

### A7. Declare date and counting basis

Choose date basis from the decision:

- earliest priority date for many technology-emergence questions;
- filing/application date for prosecution activity;
- publication date for public-availability and monitoring questions; or
- more than one view when interpretation requires it.

Do not copy fixed dates. Use exact ISO boundaries and explain publication lag.

Declare unit separately:

- publication;
- application;
- simple family;
- extended family; or
- another documented grouping.

The unit used to export candidates and the unit used for later statistics may differ;
record both and preserve traceable record-to-family mapping.

### A8. Version and reconcile the canonical query

Store the accepted anchor, branch queries, exclusions, filters, and validation as one
canonical search configuration. Re-run counts after any material change. Keep prior
versions and state which version generated each candidate record.

## Part B — preliminary taxonomy design

### B1. Use a four-column decomposition

Represent:

| Level 1 | Level 2 | Level 3 | Definition and boundary |
|---|---|---|---|
| Major technical category | Route/function/system branch | Specific method/component/problem/effect | Inclusion, exclusion, examples, and evidence |

Do not impose a universal maximum of 40 Level-3 nodes. Use the complexity supported by
the field and downstream review capacity.

Primary siblings should have clear decision boundaries. Cross-cutting application,
problem, effect, material, or product tags may be multi-label and must be modeled
separately when forced exclusivity would distort the technology.

### B2. Decompose in two passes

Top-down pass:

- use architecture, function, subsystem, route, and domain knowledge;
- identify the questions the taxonomy must answer; and
- define candidate parent/child boundaries.

Bottom-up pass:

- review a stratified evidence sample from every branch;
- add missing routes and synonyms;
- merge indistinguishable nodes;
- split overloaded nodes; and
- preserve ambiguous and negative examples.

Version every structural change and record its impact on query and tag mappings.

### B3. Control granularity

A leaf should be:

- describable in one clear technical sentence;
- searchable or classifiable using traceable evidence;
- distinguishable from primary siblings; and
- useful to the stated decision.

If a leaf cannot support a defensible query, keep it as an unresolved taxonomy concept
rather than inventing a weak search branch.

### B4. Seed key technical questions

Draft questions that connect technology evidence to later route analysis. Distribute
questions according to decision relevance and branch complexity, not a fixed minimum
or equal quota. Each question records:

- `question_id` and text;
- decision relevance;
- seed node IDs;
- expected evidence and counterevidence;
- review status; and
- uncertainty.

Stage 3 validates and owns the final questions.

### B5. Define patent-package review dimensions

Preserve the source’s six ideas as optional review dimensions:

- disruptive or materially different technology;
- novel application context;
- evidence of an unaddressed user or system need;
- substantial reported performance change;
- new function; and
- new interaction mode.

These are analyst-review prompts, not legal novelty, value, market adoption, or fixed
selection criteria. Stage 3 must define, validate, and supplement the rubric.

## Part C — hierarchy export

`tech_taxonomy.txt` is a preliminary, pure-content hierarchy for an approved tagging
tool. Each line represents one leaf path:

```text
>Level 1\Level 2\Level 3
```

If Level 3 is not justified:

```text
>Level 1\Level 2
```

Rules:

- `>` immediately precedes Level 1.
- `\` separates hierarchy levels.
- Write one path per line.
- Write no title, number, comment, blank grouping line, or metadata.
- Trim leading/trailing whitespace.
- Reject embedded line breaks and unescaped delimiter characters in labels.
- Use stable, internationally clear English terms.
- Keep multi-label behavior in the tagging schema; do not place multiple values into
  one hierarchy cell unless the approved tool explicitly defines that syntax.

Example:

```text
>Thermal management\Passive cooling\Heat pipes
>Thermal management\Active cooling\Liquid circulation
>Control systems\Predictive control\Model-based estimation
```

Validate parsing, path uniqueness, parent existence, encoding, and taxonomy version
before describing the file as ready for import. Stage 3/human review may revise it.

## Part D — precision and recall validation

### D1. Design the validation sample

For every branch, select a reproducible random or stratified sample sized for the
branch prevalence and decision risk. The source’s 20–30 records can be a planning
starting point, not a universal rule.

Stratify when relevant by year, result rank, jurisdiction, language, classification,
organization, or query path. Record seed/method and sampled identifiers.

### D2. Review relevance

Read enough evidence to make the decision—title/abstract for clear cases and claims or
description for ambiguity. Use controlled outcomes:

- relevant;
- not relevant;
- ambiguous/insufficient evidence; and
- duplicate/family handling issue.

Record exclusion reason and reviewer state. Do not classify from title alone when
technical meaning is uncertain.

### D3. Estimate precision

Calculate relevant reviewed records divided by resolved reviewed records and report
sample size, ambiguous handling, selection method, and uncertainty. A source 80%
threshold may be proposed but must be approved and fit the decision; it is not an
automatic release rule.

Tighten branches with unacceptable precision, then revalidate on a fresh sample.

### D4. Test recall boundary

Use:

- known-relevant positive controls;
- cited/citing/family neighbors;
- records just outside field, proximity, classification, date, and exclusion rules;
- alternative-language and terminology searches; and
- competitor/organization supplements.

Document recovered and missed positives, near misses, reasons, and unresolved blind
spots. Search recall cannot usually be proven complete; state the evidence and limits.

### D5. Release decision

Release a branch only when its precision, known-positive recall, near-miss behavior,
scope, count/cap status, and provenance meet the recorded acceptance criteria. Otherwise
revise, narrow the downstream claim, or mark the branch provisional.

