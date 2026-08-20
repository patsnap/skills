# Search Loop for mAb FTO Screening

## Objective

Expand and test the candidate patent pool through complementary retrieval routes while preserving a reproducible history. Search convergence is a documented human review decision, not a numerical proof of completeness.

## Retrieval routes

### Track A — keyword and fielded search

Use for exact terminology, sequence strings, mutation syntax, targets, applicants, inventors, classifications, dates, and jurisdictions.

Concept groups may include:

- target, antigen, gene, protein, receptor, ligand, pathway, epitope, and species aliases;
- antibody, immunoglobulin, binding protein, fragment, Fab, scFv, VHH, bispecific, multispecific, fusion, and conjugate terms;
- VH, VL, CDR, SEQ ID, affinity, competition, neutralization, and functional terms;
- Fc, hinge, glycan, mutation, heterodimerization, effector, and half-life terms;
- ADC linker, payload, conjugation, DAR, cleavage, release, and manufacturing terms;
- formulation, concentration, excipient, route, container, regimen, population, biomarker, and combination terms;
- applicant/assignee names, former names, subsidiaries, acquired entities, licensors, licensees, inventors, and asset codes.

Validate current classification scope before using CPC/IPC codes. Typical starting areas include C07K 16, A61K 39, C12N, and relevant A61P branches, but classifications must be adapted to the actual technology and current scheme.

### Track B — semantic search

Use for function, mechanism, technical problem, manufacturing approach, treatment concept, and terminology not captured by exact terms.

Evolve queries through distinct perspectives:

1. implementation — concrete structure/process/use;
2. function — what the candidate does;
3. mechanism — how the effect is achieved;
4. problem — the technical or clinical issue addressed;
5. application — patient, regimen, manufacturing, formulation, or supply context.

Do not merely shuffle synonyms. Preserve each query and explain what new blind spot it tests.

### Track C — biological sequence search

Use the protocol in `sequence-search.md`. Run only through an authorized, available sequence-search service. Preserve sequence versions, thresholds, database coverage, alignments, and claim context.

### Track D — chemical structure and modification search

For ADCs, radioimmunoconjugates, labels, chelators, PEG, linkers, payloads, and other chemical modifications, use exact/substructure/similarity routes when available. Record structure normalization, stereochemistry, salts, tautomer handling, query mode, and threshold. Structural similarity is retrieval evidence, not infringement.

### Track E — applicant, inventor, family, continuity, and citation expansion

- expand verified corporate entities;
- inspect inventors on high-relevance families;
- follow priorities, continuations, divisionals, national stages, reissues, and related applications;
- inspect backward/forward citations as discovery aids;
- look for recent branches and prosecution events;
- preserve the reason each expansion was performed.

### Track F — claims-focused searching

Where supported, search claim fields for:

- exact sequence and mutation expressions;
- target/epitope and functional binding limitations;
- antibody architecture and component combinations;
- formulation ranges and excipient combinations;
- dose, schedule, patient group, biomarker, and combination;
- manufacturing and analytical steps.

Claims-focused searching supplements, but does not replace, full-record retrieval and claim-version verification.

## Round preparation

Before each round, define:

- unresolved coverage question;
- route and database;
- jurisdiction/language/date/status filters;
- exact query or sequence/structure input;
- expected false-positive pattern;
- stopping or refinement criterion;
- reviewer and execution timestamp.

Do not run an undocumented exploratory query and later present it as reproducible.

## Query history contract

Maintain a machine-readable or tabular log:

```json
{
  "matter_id": "controlled-matter-id",
  "candidate_version": "candidate-v3",
  "analysis_cutoff": "YYYY-MM-DD",
  "rounds": [
    {
      "round": 1,
      "route": "keyword",
      "module": "M2",
      "database": "Patsnap Advanced Patent Search",
      "query": "stored query or controlled reference",
      "jurisdictions": ["US", "EP"],
      "languages": ["en", "de"],
      "date_filters": {},
      "status_filters": [],
      "executed_at": "YYYY-MM-DDThh:mm:ssZ",
      "result_count": 125,
      "export_id": "...",
      "new_family_count": 18,
      "notes": "tests target alias coverage"
    }
  ]
}
```

Store confidential sequences/structures by controlled reference rather than exposing them in a general query log.

## Coverage matrix

Track completion independently from hit count:

| Dimension | Required values | Completed | Evidence | Gap/waiver |
|---|---|---|---|---|
| Modules | M1, M1.5, M2–M9 as applicable |  |  |  |
| Jurisdictions | User-selected countries/EP states |  |  |  |
| Languages | English plus locally relevant languages |  |  |  |
| Status | Granted, pending, selected historical |  |  |  |
| Dates | Foundational through cutoff |  |  |  |
| Entities | Candidate, competitors, related entities |  |  |  |
| Families | Priority/continuity/national branches |  |  |  |
| Claim versions | Current granted/pending material claims |  |  |  |
| Activities | Product, use, process, formulation, supply |  |  |  |

A route with zero hits can still be complete if it was validly executed and verified. A route with many hits can remain incomplete.

## Diagnostic script

Prepare a JSON input for `scripts/mab_fto_recall_estimator.py`:

```json
{
  "round": 2,
  "keyword_ids": ["US1", "US2"],
  "semantic_ids": ["US2", "US3"],
  "sequence_ids": ["US4"],
  "seen_ids": ["US0"],
  "delta_n_min": 5,
  "required_modules": ["M1", "M1.5", "M2", "M3", "M5", "M7", "M8", "M9"],
  "completed_modules": ["M1", "M2", "M3"],
  "required_jurisdictions": ["US", "DE", "FR"],
  "covered_jurisdictions": ["US"],
  "known_gaps": ["German-language formulation query pending"]
}
```

The script reports:

- per-track counts;
- pairwise and three-way observed overlap;
- current and cumulative union;
- new records this round;
- missing declared modules and jurisdictions;
- known gaps;
- an operational next-decision label.

It intentionally returns `recall_estimate: null`. Keyword, semantic, and sequence tracks are correlated and not random capture samples; Chapman capture–recapture assumptions are not satisfied. Legacy recall fields are accepted only for backward compatibility and are ignored.

## Interpreting decisions

- `expand_or_repair_search` — all tracks empty; validate syntax, access, data coverage, and concepts.
- `complete_required_coverage` — declared modules or jurisdictions remain incomplete.
- `resolve_known_gaps` — a named coverage issue remains.
- `continue_search` — observed incremental yield remains material.
- `manual_stop_review` — incremental yield is low and declared coverage has no recorded gap; a human must still review the stop criteria.

No decision means “FTO cleared,” “recall achieved,” or “search exhaustive.”

## Manual stop review

Search may stop only after the reviewer records all of the following:

- applicable M1–M9/M1.5 modules completed or waived with reason;
- target jurisdictions, actual EP territorial scope, and locally relevant languages covered;
- target, sequence, architecture, modification, formulation, process, use, regimen, and entity synonyms tested;
- classification and claims-focused searches tested;
- sequence/structure sensitivity passes completed where applicable;
- high-relevance families expanded through priority/continuity/national branches;
- material status and claim versions verified;
- competitor, applicant, inventor, citation, and assignee-name expansions reviewed;
- recent-publication and unpublished-application blind periods disclosed;
- zero-result queries validated;
- false-positive and false-negative samples reviewed;
- known gaps accepted with owner, action, and deadline;
- monitoring cadence defined through the relevant commercial date.

## Failure handling

### All tracks empty

- confirm permissions and service availability;
- validate syntax/fields/classifications;
- remove over-restrictive date/status/jurisdiction filters;
- test target and company aliases;
- inspect sequence format/numbering/threshold;
- broaden from implementation to mechanism/problem;
- document whether zero results remain credible.

### High overlap

High overlap may show that routes retrieve similar records; it does not prove completeness. Add routes that test different blind spots: claims, applicants, classifications, citations, family branches, local languages, structures, processes, uses, or formulations.

### Low incremental yield

Review whether the low yield results from true convergence, query duplication, restrictive filters, data-access limits, or a weak expansion. Run the manual stop review.

### Excessive result set

- preserve the broad query and count;
- sample false positives to identify exclusion concepts;
- refine by claim field, technical co-occurrence, classifications, applicants, dates, or jurisdictions;
- never replace the full clearance universe with an unexplained top-N relevance list.

### Sequence track unavailable

Label M1 uncovered, request an export or approved service, and restrict conclusions. Keyword searches for sequence strings or SEQ ID terminology are not a complete substitute.

## Quality checklist

- [ ] Every round has a defined coverage question.
- [ ] Queries, filters, databases, timestamps, and exports are preserved.
- [ ] English and relevant local-language routes are documented.
- [ ] Each hit preserves every source route/module.
- [ ] Family consolidation does not erase member/claim differences.
- [ ] Script output is described as observed diagnostics only.
- [ ] No numerical recall or completeness claim is made from track overlap.
- [ ] Stop review is signed and known gaps remain visible.
- [ ] Monitoring is scheduled for pending and unpublished risk.
