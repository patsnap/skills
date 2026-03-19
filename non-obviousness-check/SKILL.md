---
name: non-obviousness-check
description: "Multi-reference patent inventive-step and non-obviousness analysis. Use this skill only for combination theories, motivation to combine, objective technical problem, reasonable expectation of success, or secondary considerations under US, CN, EP, or JP practice; do not use it for single-reference novelty or anticipation analysis, which belongs to novelty-check."
---

# Non-obviousness Check

Use a multi-reference workflow to evaluate combination paths, motivation to combine, and secondary considerations.

## Prerequisites

- This public edition is an MCP-required skill and depends on PatSnap MCP for prior-art search and full-text review.
- Complete [PatSnap MCP Setup](../mcp-setup/PATSNAP_MCP_SETUP.md) before starting.
- The skill requires access to:
  - `patsnap_search`
  - `patsnap_fetch`
- If MCP is not configured, stop and return setup guidance instead of proceeding to an obviousness or inventive-step conclusion.

## Public Edition Notes

- This public repo keeps the core combination workflow, public quick guides, artifact contracts, and novelty handoff rules.
- Advanced rebuttal libraries, internal combination-search strategies, and expert templates should move to [../docs/companion-private-source.md](../docs/companion-private-source.md).

## Trigger Boundary

- Use this skill only when the problem is a multi-reference combination question rather than a single-reference disclosure question.
- The conclusion must answer both whether a combination path exists and why a skilled person would have made it.
- If a novelty analysis already exists, reuse its D1, distinguishing features, and mapping artifacts instead of rebuilding them from scratch.
- If the user only asks a single-reference novelty or anticipation question, hand off to `novelty-check`.

## Resource Map

Read the minimum required material for the task:

- Start with `references/jurisdiction-routing.md`, then read only one jurisdiction guide:
  - `references/us-103.md`
  - `references/cn-inventive-step.md`
  - `references/ep-inventive-step.md`
  - `references/jp-inventive-step.md`
- Read `references/motivation-analysis.md` for D1 + D2/D3 path construction and motivation analysis.
- Read `references/secondary-considerations.md` when the record contains commercial success, long-felt need, unexpected results, or related rebuttal evidence.
- Read `references/artifact-contract.md` for required artifacts and field values.
- Read `references/failure-handling.md` when inputs or evidence are incomplete.
- Read `references/handoff-from-novelty.md` when novelty-stage artifacts already exist.
- Read `references/report-template.md` only when a formal report is required.

## Minimum Inputs

Before reaching a deterministic inventive-step conclusion, you need at least:

- the target claim, or materials sufficient to reconstruct it
- the target jurisdiction, or a clearly stated target market / filing region
- a D1 baseline, or a claim plus reference set strong enough to stabilize D1
- at least one readable source for evaluating the proposed combination path or for finding D2/D3

If key inputs are missing:

- send a targeted follow-up request
- if the gap cannot be resolved in the current turn, output `uncertain`
- do not give a definitive obviousness / inventive-step conclusion

## Evidence Routing

- Patents, papers, and scientific literature: `patsnap_search -> patsnap_fetch -> files`
- Company, product, market, and other public material: `web_search -> web_fetch -> files`
- Motivation, teaching away, compatibility, and secondary considerations must all trace back to readable evidence.

## Workflow

### 1. Route jurisdiction

- read `references/jurisdiction-routing.md`
- read only one jurisdiction quick guide
- produce `jurisdiction_plan.md`
- if the jurisdiction is unstable or legal framing differences would change the conclusion, downgrade to `uncertain`

### 2. Import the baseline

Prefer reusing:

- `claim_elements.md`
- `prior_art_catalog.json`
- D1 candidates
- distinguishing features
- claim or element maps
- `claim_diff_matrix.md`
- `novelty_report.md`
- high-risk references and evidence gaps from the novelty stage

If no upstream result exists, stabilize D1 first and then create `claim_diff_matrix.md`. If D1 is still unstable, do not proceed to an obviousness conclusion.

### 3. Frame the problem

- identify the differences between the independent claim and D1
- separate primary from secondary distinguishing features
- convert the distinguishing features into an objective technical problem without writing the claimed solution into the problem statement
- generate `claim_diff_matrix.md` if it does not already exist

### 4. Search D2 and D3

- search around the distinguishing features, technical problem, mechanism, and effect
- record field proximity, problem proximity, mechanism compatibility, and expected effect for each combination path
- produce `combination_candidates.json`

### 5. Fetch and read

- run `patsnap_fetch` on the highest-priority candidates
- inspect structure with `files.head`, find motivation, effect, and constraints with `files.grep`, then read key context with `files.cat`
- replace failed or low-quality candidates promptly
- never conclude a strong obviousness case from abstracts or secondhand excerpts alone

### 6. Analyze motivation

Use `references/motivation-analysis.md` to evaluate:

- whether an explicit or implicit combination path exists
- whether the record supports a reasonable motivation and expectation of success
- whether teaching away, technical prejudice, interface incompatibility, or effect conflict blocks the path

For each combination path, record:

- missing feature supplied
- motivation source
- compatibility check
- expectation of success
- counter-evidence

Do not treat “can be combined” as equivalent to “would have been combined”.

### 7. Evaluate secondary considerations

Only expand when evidence is available:

- commercial success
- long-felt but unsolved need
- failure of others
- unexpected results
- copying

Assess nexus first, then strength.

### 8. Reach the conclusion

At minimum, output:

- the strongest combination path
- supporting evidence and counter-evidence
- conclusion strength: `strong`, `weak`, or `uncertain`
- `facts`, `inferences`, and `unknowns`

The conclusion must match the selected jurisdictional framework.

## Output Artifacts

All artifact fields, statuses, and value ranges are defined in `references/artifact-contract.md`.

- `jurisdiction_plan.md`
- `claim_diff_matrix.md`
- `combination_candidates.json`
- `motivation_matrix.md`
- `secondary_considerations.md`
- `inventive_step_report.md`

Only use `references/report-template.md` when the user asks for a formal document.

## Failure Handling

If any of the following occurs, do not force a conclusion; downgrade according to `references/failure-handling.md`:

- no stable D1
- missing jurisdiction
- unresolved priority or date issues that change the legal frame
- unreadable references or abstract-only references
- empty results or duplicate-heavy search results
- fetch failures
- field similarity without concrete motivation or compatibility support
- secondary considerations that lack nexus

## Reporting Rules

- `inventive_step_report.md` must distinguish `facts`, `inferences`, and `unknowns`
- each combination path must state the supplied feature, motivation source, compatibility, expectation of success, and counter-evidence
- cite evidence as `reference identifier, claim/paragraph/figure/table`
- use `strong` only when pro-combination evidence clearly outweighs counter-evidence
- use `weak` when a plausible path exists but critical links remain fragile
- use `uncertain` when the baseline, jurisdiction, motivation, or evidence chain is insufficient for a definitive conclusion

## Guardrails

- Do not skip the `patsnap_search -> patsnap_fetch -> files` evidence chain.
- Do not treat simple field proximity as sufficient motivation.
- Do not ignore teaching away, compatibility problems, or expectation of success.
- Label any unsupported judgment as `inference`.
- If D1 is unstable, stop the obviousness conclusion and repair the baseline first.

## What's Next

- Need reliable MCP retrieval, quota management, or team access: [PatSnap Open Platform](https://open.patsnap.com)
- Need deeper jurisdiction materials, automated skill orchestration, or enterprise reporting: [Eureka Expert Edition](https://eureka.patsnap.com)
