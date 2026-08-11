---
name: search-patents-ip
description: Build and validate expert patent-search branches for Stage 1/4 of a patent-landscape program. Use when starting create-patent-landscape-overview-ip or when a user needs a reusable, field-scoped, anchored, classification-assisted, de-noised patent search configuration with precision/recall validation, a traceable family-aware candidate pool, a lightweight core-recall set, and a preliminary taxonomy export for later human review.
---

# Search Patents for a Landscape

## Role in the suite

Act as Stage 1/4 of `create-patent-landscape-overview-ip`. Translate the confirmed
decision question into auditable search branches, validate their boundary, and hand
traceable artifacts to `analyze-patent-search-results-ip`.

This stage owns search quality. It does not produce landscape statistics, competitor
profiles, patent-value conclusions, a final taxonomy, or the final report.

Read `references/query-and-taxonomy-methodology.md` completely before constructing
queries or exporting the preliminary taxonomy.

## Verified MCP services

### Advanced Patent Search — required

- Connector key: `advanced_patent_search`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`
- Use for live-schema fielded searching, result counts, filters, and reproducible
  retrieval where the active contract supports them.

### Patent Briefing — recommended

- Connector key: `patent_briefing`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- Use for seed, near-miss, and representative-record claims, descriptions, family,
  status, translations, and images where supported.

### Deep Patent Mining — optional

- Connector key: `deep_patent_mining`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-mining
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-mining`
- Use for controlled concept expansion when the retrieved evidence supports it.

### Global Core Patent Database — optional

- Connector key: `global_core_patent_database`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/core-patents
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/core-patents`
- Use for deeper seed/family/citation evidence where exposed.

Inspect the live schema before use. Do not assume source product fields, proximity
operators, rankings, or endpoint aliases exist globally.

## Step 0 — Initialize and confirm scope

Capture:

- decision objective and audience;
- technology/domain boundary;
- products, applications, problems, means, effects, inclusions, and exclusions;
- known relevant and irrelevant records;
- organizations, languages, transliterations, and terminology;
- jurisdictions and geographic meaning;
- exact date range and date basis;
- publication/application/family unit and family definition;
- population completeness requirement;
- validation acceptance criteria;
- confidentiality boundary; and
- connector/schema/version and data cutoff.

Do not copy fixed CN/US/EP, 2020–2026, competitor-versus-industry, or counting defaults.
Choose each setting from the decision and record the rationale.

Write `run_config.json` as a source-authorized reproducibility companion. Store the
same authoritative scope/provenance in `search_config.json`; downstream Stage 2 must
not depend on `run_config.json` alone.

## Step 1 — Construct expert search branches

Apply Parts A and D of the methodology reference.

### 1. Layer concepts

Separate:

- strong distinctive terms;
- weak/context-dependent terms;
- short/polysemous terms;
- structures/materials/processes/functions/effects;
- product/application terms;
- language variants and transliterations; and
- noise indicators.

### 2. Assign verified fields and proximity

Map each concept to fields/operators available in the live
`advanced_patent_search` schema. Record source-intent-to-live-schema mappings. If the
necessary field or proximity operator is unavailable, redesign the branch and disclose
the precision/recall trade-off.

### 3. Build the constant anchor

Create one versioned topic anchor reused in every branch. Test the anchor independently
and keep it stable through branch comparison.

### 4. Derive classification paths

Use confirmed seed patents and official IPC/CPC definitions. Record codes, hierarchy,
definitions, seed evidence, and query role. Never fabricate or guess a code.

### 5. Build staged exclusions

For each `NOT` rule record false-positive evidence, reason, scope, before/after count,
known-positive impact, and near-miss result. Prefer narrow exclusions.

### 6. Complete the four-part skeleton

For every branch record strong terms, weak terms plus classification, self-sufficient
classification path, constant anchor, exclusions, filters, exact request, and version.

### 7. Validate

Use reproducible samples, known-positive controls, near misses, and alternative recall
paths. Report precision, uncertainty, recall evidence, and unresolved blind spots.
Do not release merely because a universal 80% target or three iterations were reached.

## Step 2 — Write `search_config.json`

Include:

- project/scope/version identifiers;
- objective, jurisdictions, languages, dates, date basis, unit, and family method;
- live connector/operation/schema provenance;
- concept dictionary and translations;
- constant anchor and version;
- branch definitions and A6 paths;
- classification evidence;
- exclusions and impact;
- exact queries/requests;
- counts, caps, and completeness state;
- validation sample method/results;
- known positives, near misses, and blind spots;
- accepted/provisional/rejected branch status; and
- generated artifact inventory.

Validate JSON and write atomically when possible. Do not write a partial
`report_manifest.json`; Stage 4 owns that filename.

## Step 3 — Export `candidate_pool.csv`

Deduplicate under the declared family method when the downstream analysis is
family-level. Preserve sufficient traceability. Recommended columns:

```text
record_id,publication_number,application_number,family_id,representative_publication,
branch_rule_hits,query_version,retrieved_at,screening_state,source_connector
```

Use only fields actually returned and verified; retain nulls where unavailable. Do not
reduce the pool to `publication_number,branch_rule_hits` when that prevents family,
version, or source reconciliation.

Rules:

- distinguish publication-level rows from family representatives;
- preserve all valid branch hits for multi-label search logic;
- escape CSV safely and neutralize formula-leading values for spreadsheet use;
- reconcile row/family counts with the search configuration;
- mark capped/partial retrieval; and
- never call Top-K or sampled records the complete candidate population.

## Step 4 — Export `core_recall.csv`

Build a lightweight recall set for downstream review. Consider citation, family
breadth, technical relevance, organization diversity, date coverage, and other
available signals, but do not combine them into patent value.

Recommended columns:

```text
branch_id,record_id,family_id,publication_number,recall_source,raw_rank,
signal_definition,signal_as_of,verification_state,query_version
```

The source suggests cited/family Top 10 per branch. Treat that as a planning option,
not a quota. Select enough records to inspect the branch and preserve sparse branches
honestly. State whether rankings are server-returned, locally calculated, or proxies.

## Step 5 — Export `tech_taxonomy.txt`

Create the source-authorized preliminary hierarchy after candidate-pool validation.
Follow Part C exactly.

- Use one `>L1\L2\L3` or justified `>L1\L2` path per line.
- Use only hierarchy content—no header, numbering, comments, or blank grouping lines.
- Validate UTF-8 encoding, delimiter safety, uniqueness, and parent/child logic.
- Label the artifact in `search_config.json` as `preliminary_search_taxonomy`.
- State that Stage 3 and human review own validation and revision.
- Describe it as ready for schema review/import into an approved tagging tool, not a
  specific regional SaaS product.

## Output contract

### Core downstream artifacts

| File | Consumer | Content |
|---|---|---|
| `search_config.json` | Stage 2 and later | Authoritative scope, queries, provenance, validation, counts, and artifact metadata |
| `candidate_pool.csv` | Stage 2 and later | Traceable deduplicated candidate records and branch hits |
| `core_recall.csv` | Stage 2 | Lightweight branch recall candidates and signal provenance |

### Source-authorized companion artifacts

| File | Role |
|---|---|
| `run_config.json` | Human-readable/reproducible initialization companion; not a substitute for `search_config.json` |
| `tech_taxonomy.txt` | Preliminary hierarchy for Stage 3/human review; not validated tags |

Do not produce Stage 2 statistics or Stage 4 report files.

## Handoff to Stage 2

Before handoff:

1. validate all five runtime artifacts;
2. reconcile scope/version/counts/checksums where recorded;
3. identify accepted and provisional branches;
4. identify capped retrieval and unresolved blind spots;
5. distinguish preliminary taxonomy from validated tagging;
6. list connector/schema provenance; and
7. preserve rollback paths.

Return:

```text
Stage 1 complete: [accepted/provisional branch counts], [candidate row/family counts],
[core recall count], query version [id].
Core handoff: search_config.json, candidate_pool.csv, core_recall.csv.
Companions: run_config.json, tech_taxonomy.txt (preliminary).
Unresolved: [summary].
```

Then route to `analyze-patent-search-results-ip`.

## Quality gate

- Objective, scope, date, language, jurisdiction, unit, and family method are explicit.
- Every branch uses a stable anchor and auditable four-part skeleton.
- Every field/operator exists in the active schema or has a disclosed fallback.
- IPC/CPC codes have official-definition and seed evidence.
- Every exclusion has evidence, rationale, impact, and recall check.
- Precision samples are reproducible and uncertainty is stated.
- Known positives and near misses test recall boundaries.
- Counts identify complete, capped, sampled, and deduplicated states.
- Candidate rows preserve stable identifiers, query version, and source.
- Core recall ranks/signals are defined and dated.
- Preliminary taxonomy is syntactically valid and not misrepresented as validated.
- No fixed regional/date/mode default or quota drives the result.
- No Stage 1 partial report manifest is created.

## Stop conditions

Stop or narrow when:

- the business/technology boundary is not confirmed;
- the required global search connector or field/operator is unavailable;
- seed classifications cannot be verified;
- precision remains unacceptable or recall controls reveal material gaps;
- retrieval caps prevent the required candidate-population claim;
- family identifiers cannot support requested deduplication;
- confidential terms cannot be processed safely;
- an artifact cannot be validated or reconciled; or
- producing a clean-looking output would require invented records, codes, counts, or
  taxonomy paths.

Return completed branches, failed criteria, residual risk, and exact next step. Do not
silently pass a provisional branch to Stage 2.

