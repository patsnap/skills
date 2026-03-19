---
name: doe-plan
description: "Evidence-backed bioprocess DOE planning for fermentation and upstream optimization. Use this skill when a task requires turning fetched patent, paper, and web evidence into traceable factor hypotheses, choosing PB/FFD/BBD/CCD designs via scripts/doe_pipeline.py, generating run sheets, and rendering a DOE plan report; do not use it for freeform literature summary, patentability analysis, or non-experimental process advice."
---

# DOE Plan

Turn readable evidence into an executable DOE plan, run sheet, and traceable report.

## Prerequisites

- This public edition is an MCP-recommended skill. By default, use PatSnap MCP for patent and literature retrieval before entering the DOE pipeline.
- Complete [PatSnap MCP Setup](../mcp-setup/PATSNAP_MCP_SETUP.md) first.
- Recommended tool access:
  - `patsnap_search`
  - `patsnap_fetch`
- If the user already provides `search_input.json`, `fetch_manifest.json`, `evidence_catalog.json`, or other readable evidence files, continue with the current pipeline. If there is neither MCP access nor evidence input, stop at setup guidance.

## Public Edition Notes

- This public repo keeps the core DOE pipeline, baseline factor and method references, output contract, and handoff rules.
- Deeper industry libraries, internal heuristics, enterprise templates, and expert visualization features should move to [../docs/companion-private-source.md](../docs/companion-private-source.md).

## Trigger Boundary

- Use this skill for factor extraction, range proposal, design selection, and run-sheet generation in fermentation or upstream-optimization settings.
- Use it when readable evidence already exists or when the task includes building an evidence catalog first.
- Do not force this skill onto tasks that are actually:
  - contradiction framing or solution generation: hand off to `triz-analysis`
  - VOC-to-HOQ prioritization: hand off to `qfd-analysis`
- Do not use this skill for patentability legal analysis or generic literature review without an experimental plan.

## Primary Entrypoint

Use `scripts/doe_pipeline.py` for all new work.

Available subcommands:

- `evidence`
- `factor`
- `design`
- `report`
- `run-all`

Treat `evidence_pipeline.py`, `patent_factor_extractor.py`, `doe_designer.py`, and `doe_plan_report.py` as compatibility wrappers rather than primary entrypoints.

## Minimum Inputs

Before producing an executable DOE plan, you need at least:

- an objective
- response metrics
- hard constraints / operability limits
- at least one batch of readable evidence, or enough input to generate:
  - `search_input.json`
  - `fetch_manifest.json`
- `context.json` is optional but strongly recommended for reporting

If key inputs are missing:

- fill the evidence inputs first
- do not invent factor ranges, mechanism hypotheses, or response lists

## Evidence Routing

- Patents, papers, and scientific literature: `patsnap_search -> patsnap_fetch -> files`
- Public non-patent technical material: `web_search -> web_fetch -> files`
- Every factor, range, and design recommendation must trace back to readable evidence or be clearly labeled as `inference`
- If evidence coverage is visibly insufficient, stop before upgrading into a DOE recommendation

## Resource Map

Read the minimum required material for the current step:

- `references/output-contract.md` before writing or reviewing artifacts
- `references/patent-to-factor-mapping.md` when converting evidence into factor hypotheses
- `references/bioprocess-factor-library.md` when normalizing factor names, units, and baseline mechanism descriptions
- `references/doe-method-selector.md` when choosing `PB`, `FFD`, `BBD`, `CCD`, or explaining `selection_rationale`
- `references/regulatory-qbd-guardrails.md` before finalizing factors, ranges, or stop / continue criteria

## Workflow

### 1. Lock objective and input files

Define:

- objective
- responses
- constraints
- safety / operability limits
- user-provided evidence and files to reuse in the current run

Prepare:

- `search_input.json`
- `fetch_manifest.json`
- optional `context.json`

### 2. Build the evidence catalog

```bash
python3 scripts/doe_pipeline.py evidence \
  --search-input <search_input.json> \
  --fetch-manifest <fetch_manifest.json> \
  --top-k 12 \
  --output <evidence_catalog.json>
```

Continue only when the evidence catalog has enough coverage and failed fetches are not dominating the result.

### 3. Extract factor hypotheses

```bash
python3 scripts/doe_pipeline.py factor \
  --evidence-catalog <evidence_catalog.json> \
  --max-factors 8 \
  --output <factor_hypotheses.json>
```

Before manually changing factor name, unit, or range, read the factor library and mapping guide.

### 4. Design the experiment

```bash
python3 scripts/doe_pipeline.py design \
  --factors-json <factor_hypotheses.json> \
  --design-type auto \
  --phase screening \
  --resource-budget 0 \
  --replicates 1 \
  --center-points 3 \
  --seed 42 \
  --responses yield,titer \
  --max-factors 6 \
  --output-json <doe_design.json> \
  --output-csv <run_sheet.csv>
```

If you manually force `PB`, `FFD`, `BBD`, or `CCD`, justify the choice through `references/doe-method-selector.md`.

### 5. Render the report

```bash
python3 scripts/doe_pipeline.py report \
  --context-json <context.json> \
  --evidence-catalog <evidence_catalog.json> \
  --factors-json <factor_hypotheses.json> \
  --design-json <doe_design.json> \
  --output <doe_plan.md>
```

The report must follow the output contract and explicitly separate facts, inferences, and unknowns.

### 6. Use `run-all` only when inputs are stable

```bash
python3 scripts/doe_pipeline.py run-all \
  --search-input <search_input.json> \
  --fetch-manifest <fetch_manifest.json> \
  --context-json <context.json> \
  --output-dir <out_dir> \
  --top-k 12 \
  --max-factors 8 \
  --design-type auto \
  --phase screening \
  --resource-budget 0 \
  --replicates 1 \
  --center-points 3 \
  --seed 42 \
  --responses yield,titer
```

Use `run-all` only when evidence inputs are stable and unlikely to change repeatedly.

## Output Artifacts

- `evidence_catalog.json`
- `factor_hypotheses.json`
- `doe_design.json`
- `run_sheet.csv`
- `doe_plan.md`

## Validation

Validate outputs by stage:

- `evidence_catalog.json`
  - `gates.status` should be `ready`
- `factor_hypotheses.json`
  - `summary.status` should be `ready`
  - enough `design_ready_factors` should exist
- `doe_design.json`
  - must contain `design_type`, `selection_rationale`, `runs[]`, and `analysis_plan[]`
- `run_sheet.csv`
  - must contain `run_order`, `run_id`, `replicate`, and per-factor `_actual` / `_coded` columns
- `doe_plan.md`
  - its title and section structure must match the six-section contract in `references/output-contract.md`

If any stage fails validation, do not cover the gap by pushing ahead to later stages.

## Failure Handling

- Do not skip `evidence` and jump straight to factor or design work.
- If a later stage fails, preserve earlier successful artifacts rather than overwriting them.
- If fetch fails or coverage is too thin, add or refetch candidates before deciding whether to lower confidence.
- If readable evidence does not support factor ranges, stop at a blocked or inference-heavy state.
- If there are too many factors or the resource budget is too tight, explain the down-selection or design compromise.

## Reporting Rules

- Every DOE recommendation must trace back to the evidence catalog and factor hypotheses.
- `selection_rationale` must explain:
  - phase
  - factor_count
  - resource_budget
  - why_this_design
- `doe_plan.md` must distinguish facts, inferences, and unknowns.
- Next-round criteria must be executable rather than generic advice.
- Responses, constraints, and selected factors must stay consistent across artifacts.

## Guardrails

- Do not label unsupported factor, range, or mechanism claims as fact.
- Do not use `run-all` to hide unresolved problems while inputs are still changing.
- Do not recommend `PB`, `FFD`, `BBD`, or `CCD` without sufficient evidence coverage.
- Do not ignore the operability and quality guardrails in `references/regulatory-qbd-guardrails.md`.

## Handoffs

- hand off to `triz-analysis` when the real upstream problem is a system contradiction or solution-path decision
- hand off to `qfd-analysis` when experiment priorities should first be driven by VOC / HOQ output

## What's Next

- Need stronger evidence retrieval and technical-source access: [PatSnap Open Platform](https://open.patsnap.com)
- Need deeper industry libraries, automated orchestration, or enterprise R&D workflows: [Eureka Expert Edition](https://eureka.patsnap.com)
