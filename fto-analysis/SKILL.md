---
name: fto-analysis
description: "Freedom-to-operate analysis for product-level clearance work. Use this skill for market-specific patent clearance, blocking-patent discovery, recall estimation with scripts/fto_recall_estimator.py, infringement and design-around risk triage, and structured FTO reporting; do not use it for isolated single-patent novelty or inventive-step review."
---

# FTO Analysis

Use a traceable search, screening, validity-attack, and risk-framing workflow for product or technology clearance analysis.

## Prerequisites

- This public edition is an MCP-required skill and depends on PatSnap MCP for blocking-patent discovery and full-text review.
- Complete [PatSnap MCP Setup](../mcp-setup/PATSNAP_MCP_SETUP.md) before starting.
- The skill requires access to:
  - `patsnap_search`
  - `patsnap_fetch`
- If MCP is not configured, stop before entering the FTO search loop and return setup guidance.

## Public Edition Notes

- This public repo keeps the search loop, recall-estimation script, core output contract, and cross-skill handoff pattern.
- Advanced jurisdiction playbooks, internal retrieval strategies, expert templates, and enterprise risk packaging should move to [../docs/companion-private-source.md](../docs/companion-private-source.md).

## Trigger Boundary

- Use this skill for product-level, solution-level, pre-launch, or market-entry FTO / clearance analysis.
- Use it when the task requires multi-round patent search, blocking-patent discovery, infringement risk triage, or design-around recommendations.
- If the problem narrows down to a single-patent novelty or inventive-step judgment, do not stretch this skill:
  - single-reference novelty / anticipation: hand off to `novelty-check`
  - multi-reference inventive-step / obviousness: hand off to `non-obviousness-check`

## Primary Entrypoint

- For every round, compute Chapman recall estimate, overlap, `delta_n`, and early-stop signals by running:
  - `python3 scripts/fto_recall_estimator.py --input-json <path>`
- Do not calculate those metrics manually in the prompt.
- The script only handles deterministic statistics; query evolution, validity attack, infringement mapping, and FTO framing remain governed by this skill.

## Resource Map

- Read `references/search-loop.md` before starting the search loop.
- Read `references/output-contract.md` before writing or reviewing artifacts.
- Reuse:
  - `novelty-check`
  - `non-obviousness-check`
  when the workflow moves into validity attacks.

## Minimum Inputs

Before reaching a traceable FTO conclusion, you need at least:

- a product or technology description
- target jurisdictions
- a recall target
- a legal-status filter
- analysis depth: `Quick` or `Deep`

If key inputs are missing:

- narrow the scope first instead of jumping into search
- use defaults only to start round one, never to hide uncertainty:
  - jurisdiction: `CN + US`
  - legal status filter: `active only`
  - recall target: `85%`
  - `delta_n_min`: `5`

## Evidence Routing

- Patent search and full text: `patsnap_search` + `patsnap_fetch`
- Every FTO conclusion must trace back to readable patent text, legal-status evidence, or a clearly labeled `inference`
- If the search loop is not complete, do not give a definitive clearance conclusion

## Workflow

### 1. Lock scope

Define:

- product or technology under review
- jurisdictions
- active-only or broader legal-status scope
- recall target and `delta_n_min`
- `Quick` or `Deep`

### 2. Run the search loop

- run keyword and semantic search paths in parallel
- maintain `query_history`
- for each round, use `scripts/fto_recall_estimator.py` to compute round metrics before deciding:
  - `target_met`
  - `diminishing_returns`
  - `continue_search`
  - `expand_search`
- only claim that the recall target is met or that marginal returns are shrinking when the script output supports it

### 3. Screen the pool

- deduplicate
- filter legal status according to scope
- assess technical relevance, claim breadth, and expiry window
- output a `Quick` top 10 or a `Deep` shortlist

### 4. Attack validity

For each high-risk patent in the shortlist:

1. run a `novelty-check`-style single-reference anticipation attack
2. run a `non-obviousness-check`-style multi-reference combination attack
3. only if the patent still appears potentially valid, proceed to infringement mapping and design-around analysis

### 5. Write the opinion

- organize `fto_search_log.md`, `patent_pool.json`, and `fto_report.md` according to `references/output-contract.md`
- use “estimated recall,” never “100% recall”

## Guardrails

- Never claim exhaustive search or `100%` recall.
- Lock jurisdiction before the first search round; state assumptions explicitly when needed.
- Reuse `claim_diff_matrix` from novelty attack into the inventive-step attack.
- High-risk conclusions must include a legal disclaimer and recommend formal attorney review.

## Output Artifacts

- `fto_search_log.md`
- `patent_pool.json`
- `claim_diff_matrix_[patent_no].md`
- `motivation_matrix_[patent_no].md`
- `fto_report.md`

## What's Next

- Need reliable MCP retrieval, quota management, or team access: [PatSnap Open Platform](https://open.patsnap.com)
- Need automated novelty / obviousness / FTO orchestration or enterprise reporting: [Eureka Expert Edition](https://eureka.patsnap.com)
