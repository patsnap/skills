---
name: triz-analysis
description: "TRIZ engineering contradiction analysis for product, process, or system trade-offs. Use this skill when a task requires turning an ambiguous technical problem into a bounded contradiction model, exactly three evidence-backed solution paths, a weighted recommendation, and a validation roadmap; do not use it for patentability-only analysis, VOC-to-HOQ prioritization, or DOE run-sheet design."
---

# TRIZ Analysis

Turn an ambiguous engineering problem into three executable solution paths, one ranked recommendation, and a validation roadmap.

## Prerequisites

- This public edition is an MCP-recommended skill. By default, use PatSnap MCP to collect patents, papers, and technical literature before TRIZ modeling.
- Complete [PatSnap MCP Setup](../mcp-setup/PATSNAP_MCP_SETUP.md) first.
- Recommended tool access:
  - `patsnap_search`
  - `patsnap_fetch`
- If the user already provides enough readable evidence files, continue with the workflow. If there is neither MCP access nor readable evidence, stop at setup guidance or an assumption-heavy framing stage.

## Public Edition Notes

- This public repo keeps the three-option structure, public TRIZ references, output contract, and basic case snippets.
- Advanced case libraries, internal scoring templates, and deeper expert routes should move to [../docs/companion-private-source.md](../docs/companion-private-source.md).

## Trigger Boundary

- Use this skill for engineering contradictions, trade-offs, bottleneck breakthroughs, and solution generation under hard constraints.
- Do not keep using this skill when the task becomes:
  - single-reference novelty / anticipation: hand off to `novelty-check`
  - multi-reference inventive-step / obviousness: hand off to `non-obviousness-check`
  - VOC prioritization / House of Quality: hand off to `qfd-analysis`
  - factor screening / DOE run sheet / lab design: hand off to `doe-plan`
- The final structure must contain exactly three options:
  - Conservative
  - Balanced
  - Breakthrough

## Resource Map

Read only what the current step needs:

- `references/triz-core.md` for boundaries, technical contradiction, physical contradiction, IFR, and resource analysis
- `references/scenario-templates.md` for scoring scenario and weights
- `references/evidence-search.md` for search design and evidence credibility tracking
- `references/triz-advanced.md` only when core mapping is insufficient
- `references/output-contract.md` before saving the final answer or report
- `references/case-snippets.md` only when the user asks for examples, analogies, or teaching material

## Minimum Inputs

Before making a deterministic recommendation, you need at least:

- an objective and target metric
- the current baseline or known status quo
- hard constraints
- unacceptable side effects
- a clear system boundary or operating context

If key inputs are missing:

- request a targeted follow-up
- if the gap cannot be closed in the current turn, make assumptions explicit
- do not rank options before the boundary is stable

## Evidence Routing

- Patents, papers, and scientific literature: `patsnap_search -> patsnap_fetch -> files`
- Public technical material, vendor documentation, and engineering sources: `web_search -> web_fetch -> files`
- Unless the user explicitly wants brainstorming only, collect at least three credible evidence sources.
- Every final option must map to at least one readable source.
- Label any unsupported mechanism, benefit, or risk judgment as `inference`.

## Workflow

### 1. Fix the frame

Define:

- objective and target metric
- current baseline
- scope / boundary
- hard constraints
- unacceptable side effects
- user-supplied data, references, or known failure modes

If the boundary is unclear, ask or state assumptions before generating options.

### 2. Choose the scoring scenario

- read `references/scenario-templates.md`
- choose one of:
  - `enterprise engineering`
  - `research project`
  - `teaching or learning project`
- use that scenario’s weights for all later ranking

### 3. Build the TRIZ model

Based on `references/triz-core.md`, output the minimum sufficient model:

- technical contradiction
- physical contradiction, if present
- IFR statement
- resource inventory

Keep the model tied to the actual system and constraints rather than abstracting it into something unusable.

### 4. Gather evidence

- use `references/evidence-search.md` to define queries and screening rules
- prioritize recent, primary sources for feasibility assessment
- use classic literature only when explaining mechanism
- record relevance, credibility, and option linkage for every source

### 5. Generate exactly three options

Only output:

1. Conservative
2. Balanced
3. Breakthrough

For each option, state:

- core mechanism
- expected metric movement
- required resources
- main risks and mitigations
- linked evidence

### 6. Score and rank

Score each option from 1 to 5 on:

- Impact
- Feasibility
- CostEfficiency
- RiskControl
- Novelty

Produce a weighted ranking that matches the selected scenario and explain the key trade-off behind the recommendation.

### 7. Add the validation roadmap

For the recommended option, provide:

- a minimal viable experiment
- success and failure thresholds
- timeline and owners / resources
- stop-loss conditions
- next data needed

### 8. Separate certainty levels

Before closing, distinguish:

- facts
- inferences
- unknowns

## Output Artifacts

- `triz_analysis_report.md`
- If the user wants an inline answer instead of a saved file, keep the same section order defined in `references/output-contract.md`

## Advanced Escalation

Read `references/triz-advanced.md` only when one of the following is true:

- core mapping does not produce a robust option set
- contradictions are coupled across multiple subsystems
- the physical contradiction requires explicit separation logic
- the user explicitly asks for deeper innovation exploration

After advanced analysis, return to the standard three-option structure.

## Reporting Rules

- Follow the structure defined in `references/output-contract.md` for the final answer or saved report.
- If the user asks for a saved file, the default filename is `triz_analysis_report.md`.
- The recommendation must explain:
  - why this option is best now
  - which trade-off is being accepted
  - what conditions would reverse the recommendation
- Lower `confidence` when evidence is weak; do not invent facts.

## Guardrails

- Do not rank options before the system boundary is stable.
- Do not output more than three final options.
- Do not turn this skill into patentability analysis or a legal conclusion.
- Do not treat secondhand summaries, marketing copy, or unread source material as strong evidence.
- If the user does not want brainstorming and the evidence is too weak to support a recommendation, stop at `uncertain` or an assumption-heavy state.

## Handoffs

- hand off to `novelty-check` when the task becomes single-reference novelty / anticipation
- hand off to `non-obviousness-check` when the task becomes D1 + D2/D3 inventive-step / obviousness
- hand off to `qfd-analysis` when the task needs VOC-to-HOQ deployment and quantified requirement priorities
- hand off to `doe-plan` when the chosen option must move into factor screening, design matrices, and run-sheet planning

## What's Next

- Need stronger evidence retrieval and technical-source access: [PatSnap Open Platform](https://open.patsnap.com)
- Need deeper case libraries, automated orchestration, or an enterprise innovation workspace: [Eureka Expert Edition](https://eureka.patsnap.com)
