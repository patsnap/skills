---
name: novelty-check
description: "Single-reference patent novelty and anticipation analysis. Use this skill only for claim decomposition, prior-art search, and novelty analysis under US, CN, EP, or JP rules when the question is whether one readable reference defeats a claim; do not use it for multi-reference combination, inventive-step, motivation-to-combine, or secondary-consideration analysis, which belongs to non-obviousness-check."
---

# Novelty Check

Use a single-reference workflow to complete novelty search, element-by-element mapping, and conclusion framing.

## Prerequisites

- This public edition is an MCP-required skill and depends on PatSnap MCP for patent and literature retrieval.
- Complete [PatSnap MCP Setup](../mcp-setup/PATSNAP_MCP_SETUP.md) before starting.
- The skill requires access to:
  - `patsnap_search`
  - `patsnap_fetch`
- If MCP is not configured, stop and return setup guidance instead of proceeding to a novelty conclusion.

## Public Edition Notes

- This public repo keeps the core workflow, public jurisdiction summaries, artifact contracts, and handoff rules.
- Advanced case libraries, expanded jurisdiction materials, internal retrieval playbooks, and expert templates should move to [../docs/companion-private-source.md](../docs/companion-private-source.md).

## Trigger Boundary

- Handle only single-reference novelty / anticipation questions.
- As soon as the task requires D1 plus D2 or D3, motivation to combine, secondary considerations, or inventive step, hand off to `non-obviousness-check`.
- Only one readable reference that discloses every claim element can support `novelty_rejected`.

## Resource Map

Read the minimum required material in this order:

- Start with `references/legal-standards-by-jurisdiction.md`, then read only one jurisdiction guide:
  - `references/us-102.md`
  - `references/cn-novelty.md`
  - `references/ep-novelty.md`
  - `references/jp-novelty.md`
- Read `references/claim-decomposition.md` for claim parsing.
- Read `references/search-strategy.md` to design search rounds and candidate-pool strategy.
- Read `references/element-mapping.md` to standardize mapping format.
- Read `references/artifact-contract.md` for required artifact fields and status values.
- Read `references/failure-handling.md` if inputs or evidence are incomplete.
- Read `references/handoff-to-non-obviousness.md` when the task moves into inventive-step analysis.
- Read `references/report-template.md` only when a formal report is required.

## Minimum Inputs

Before you can reach a deterministic novelty conclusion, you need at least:

- the target claim, or materials sufficient to reconstruct the full claim
- the filing date, priority date, or enough information to lock the critical date
- the target jurisdiction, or a clearly stated target market / filing region
- at least one readable claim source or prior-art source

If key inputs are missing:

- send a targeted follow-up request
- if the gap cannot be resolved in the current turn, output `uncertain`
- do not give a definitive legal conclusion

## Evidence Routing

- Patents, papers, and scientific literature: `patsnap_search -> patsnap_fetch -> files`
- Company, product, market, or other public non-patent material: `web_search -> web_fetch -> files`
- Every conclusion must trace back to readable source text.
- Web evidence may support public-availability analysis, terminology, or product background, but cannot be combined into a single-reference defeat.

## Workflow

### 1. Fix scope

- target claim
- filing date or priority date
- target jurisdiction
- upstream search results or known high-risk references, if any

If the jurisdiction is still open, you may only form a provisional search view rather than a final legal conclusion.

### 2. Route jurisdiction

- read `references/legal-standards-by-jurisdiction.md`
- read only one jurisdiction quick guide
- if the user names a target market but not a jurisdiction, use the most relevant filing region as a temporary assumption and mark it in the report
- if AIA vs pre-AIA, grace period, conflicting application, or public-availability issues remain unresolved, downgrade to `uncertain`

### 3. Decompose claims

- assign stable IDs such as `E1`, `E2`
- record synonyms, terminology variants, key parameters, and functional limitations
- start with the independent claim, then decide whether key dependent claims must be covered
- produce `claim_elements.md`

### 4. Search prior art

- search patents and papers first, then decide whether web evidence is needed for support
- record the purpose of each round: broad search, narrowing, or gap filling
- prioritize candidates with acceptable publication date, relevance, and readability
- keep `prior_art_catalog.json` up to date

### 5. Fetch and read

- run `patsnap_fetch` on high-priority candidates
- inspect structure with `files.head`, locate elements with `files.grep`, then read key context with `files.cat`
- replace failed or low-quality fetches instead of accepting a broken evidence chain
- never conclude `novelty_rejected` from abstracts or secondhand excerpts alone

### 6. Build the element map

For each candidate reference, answer:

- whether the element is disclosed
- whether the disclosure is explicit, implicit, or inherent
- where the evidence appears
- what the risk point is

Implicit disclosure requires a stated reasoning chain. Inherent disclosure requires necessity, not plausibility.

### 7. Build `claim_diff_matrix.md`

- select the strongest D1 candidate
- compare the target claim against D1 element by element
- mark each element as `matched`, `partial`, `missing`, or `uncertain`
- treat this file as the canonical bridge artifact for `non-obviousness-check`

### 8. Reach the novelty conclusion

- one readable reference that covers every element: `novelty_rejected`
- every reviewed reference still misses at least one element: `novelty_preserved`
- incomplete evidence, unlocked jurisdiction, or contested public availability: `uncertain`

Always state:

- the strongest D1 candidate
- missing or disputed elements
- high-risk references
- unresolved questions

## Output Artifacts

All artifact fields, statuses, and value ranges are defined in `references/artifact-contract.md`.

- `claim_elements.md`: claim decomposition and search anchors
- `prior_art_catalog.json`: search rounds, candidate pool, and read status
- `element_mapping.md`: element-by-element mapping for the strongest candidates
- `claim_diff_matrix.md`: target claim vs strongest D1 bridge matrix
- `novelty_report.md`: final novelty conclusion and risk summary

Only use `references/report-template.md` when the user asks for a formal saved report.

## Failure Handling

If any of the following occurs, do not force a conclusion; downgrade according to `references/failure-handling.md`:

- unreadable references or abstract-only references
- missing jurisdiction
- unknown filing date or unresolved priority chain
- empty results or duplicate-heavy results
- fetch failures
- evidence that supports only a partial map
- public-disclosure uncertainty
- grace-period uncertainty
- inherency without proof of necessity

## Reporting Rules

- `novelty_report.md` must distinguish `facts`, `inferences`, and `unknowns`
- cite evidence as `reference identifier, claim/paragraph/figure/table`
- when the conclusion is `novelty_rejected`, name exactly one defeating reference
- when the conclusion is `novelty_preserved`, list the elements still missing across all reviewed references
- when the conclusion is `uncertain`, state the exact blockers

## Guardrails

- Do not skip the `patsnap_search -> patsnap_fetch -> files` evidence chain.
- Do not combine multiple references into a novelty rejection.
- Label any unsupported judgment as `inference`.
- Confirm the applicable jurisdiction and critical date before the final conclusion.
- If the strongest D1 still contains any `missing`, `partial`, or `uncertain` element, do not write `novelty_rejected`.

## Handoff to Non-obviousness

When the task becomes an obviousness or inventive-step problem, hand off:

- `claim_elements.md`
- `prior_art_catalog.json`
- the closest prior-art candidate (D1)
- `claim_diff_matrix.md`
- the completed `element_mapping.md`
- `novelty_report.md`
- high-risk references and unresolved risks

## What's Next

- Need reliable MCP retrieval, quota management, or team access: [PatSnap Open Platform](https://open.patsnap.com)
- Need deeper jurisdiction materials, automated skill orchestration, or enterprise reporting: [Eureka Expert Edition](https://eureka.patsnap.com)
