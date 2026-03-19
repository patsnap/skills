---
name: qfd-analysis
description: "Quality Function Deployment / House of Quality execution. Use this skill when a task requires running scripts/qfd_pipeline.py on VOC, feature specs, and optional competitor specs to generate validated HOQ artifacts, requirement priorities, conflict analysis, and benchmark gaps; do not use it for freeform ideation, TRIZ contradiction solving, or DOE design."
---

# QFD Analysis

Run the local QFD pipeline and summarize only from generated artifacts without inventing missing inputs.

## Prerequisites

- This public edition is an MCP-optional skill. The core runtime path remains the local `scripts/qfd_pipeline.py` workflow.
- If you already have local VOC and feature-spec files, you can run the pipeline without MCP.
- If you want to use PatSnap MCP first to gather patent, literature, or competitor evidence and then turn that into local input files, complete [PatSnap MCP Setup](../mcp-setup/PATSNAP_MCP_SETUP.md).

## Public Edition Notes

- This public repo keeps the local QFD pipeline, artifact validation rules, and baseline HOQ references.
- Advanced templates, industry case libraries, enterprise report packaging, and orchestration layers should move to [../docs/companion-private-source.md](../docs/companion-private-source.md).

## Trigger Boundary

- Use this skill for VOC-to-HOQ execution, requirement prioritization, technical relationship matrices, roof correlation matrices, and benchmark gap analysis.
- The primary task must be running or reviewing `scripts/qfd_pipeline.py`.
- Do not force this skill onto tasks that are actually:
  - trade-off resolution or inventive option generation: hand off to `triz-analysis`
  - experiment design or factor screening: hand off to `doe-plan`

## Primary Entrypoint

Use only `scripts/qfd_pipeline.py`.

- Do not call:
  - `voc_processor.py`
  - `hoq_builder.py`
  - `benchmark_analyzer.py`
  - `report_generator.py`
- Treat CLI arguments and stdout JSON as the runtime contract.
- Do not describe framework-specific wrapper, handle-ref, or session-path mechanics.

## Minimum Inputs

The first run normally requires:

- `--voc-path <path>`
- `--features-path <path>`

You may omit a new `--features-path` only when the workspace already contains `02_technical/our_product_spec.json`.

Optional inputs:

- `--workspace <path>`
- `--project-name <name>`
- `--weights-path <path>`
- `--relationships-path <path>`
- `--correlations-path <path>`
- `--competitor-specs-path <path>` (repeatable)
- `--requirement-ratings-path <path>`
- `--min-frequency <int>`
- `--include-xlsx` or `--no-xlsx`

If core inputs are missing:

- ask the user for the files first
- do not fabricate feature specs, relationship matrices, or benchmark inputs

## Resource Map

- Read `references/qfd-theory.md` if the user asks how QFD works or questions the HOQ structure.
- Read `references/hoq-symbols.md` when explaining relationship strength, roof correlation, or priority score.
- Read `references/file-structure.md` when validating artifacts, reusing a workspace, or deciding which files must be read.

## PatSnap MCP Extension

- The QFD pipeline itself does not call MCP tools directly; MCP is only for upstream input preparation.
- If VOC, feature specs, or competitor evidence are incomplete, you may use `patsnap_search -> patsnap_fetch` to gather supporting material and then convert it into local input files.
- Do not treat raw MCP results as pipeline output; convert them into local input files before running `qfd_pipeline.py`.

## Preflight

Before execution, confirm:

- the VOC file path is readable
- the features JSON is readable and matches the current product version
- the workspace path is explicit so artifacts do not scatter
- an old workspace is reused only when the user explicitly wants incremental reuse

Prefer an explicit workspace so artifact paths stay stable.

## Standard Run Pattern

```bash
python3 scripts/qfd_pipeline.py \
  --voc-path <voc-file> \
  --features-path <features-json> \
  --workspace <workspace-dir> \
  --project-name "<project-name>"
```

Add optional flags only when the user supplied the relevant inputs or explicitly asked for that behavior.

If competitor inputs exist, repeat `--competitor-specs-path <path>`.

## Output Artifacts

- `project_meta.json`
- `01_voc/requirements.json`
- `02_technical/our_product_spec.json`
- `03_analysis/relationship_matrix.json`
- `03_analysis/correlation_matrix.json`
- `03_analysis/conflicts.json`
- `05_output/priority_recommendations.json`
- `05_output/qfd_report.md`
- `05_output/hoq_matrix.xlsx` when XLSX output is enabled and dependencies are available

## Validation After Run

Treat the run as successful only when all of the following are true:

- the command exit code is `0`
- stdout JSON contains `success: true`
- stdout JSON shows a completed `status`
- the workspace contains these core artifacts:
  - `project_meta.json`
  - `01_voc/requirements.json`
  - `02_technical/our_product_spec.json`
  - `03_analysis/relationship_matrix.json`
  - `03_analysis/correlation_matrix.json`
  - `03_analysis/conflicts.json`
  - `05_output/priority_recommendations.json`
  - `05_output/qfd_report.md`

Always read at least:

- `05_output/qfd_report.md`
- `05_output/priority_recommendations.json`
- `03_analysis/conflicts.json`

Read the following only when competitor specs were provided and the files exist:

- `04_benchmark/benchmark_table.json`
- `04_benchmark/gap_analysis.json`

If stdout JSON exposes `quick_access` or `read_guide`, reuse those paths and read order first.

## Failure Handling

- If stdout JSON reports `missing_inputs`, ask for the missing files and stop instead of rerunning blindly.
- If `--features-path` is missing and the workspace does not contain a fallback spec, request a valid features JSON.
- If optional JSON files are malformed, ask whether to replace them or rerun without them.
- If stdout JSON reports validation or consistency errors, do not summarize partial results as if they were complete.
- If `hoq_matrix.xlsx` is skipped because `openpyxl` is missing, continue with Markdown and JSON artifacts but say so explicitly.

## Reporting Rules

- Keep the narrative aligned with `priority_recommendations.json` and `conflicts.json`.
- Reuse requirement and feature labels exactly as they appear in generated artifacts.
- Mention benchmark conclusions only when the relevant files exist and support the claim.
- If an old workspace spec or intermediate data was reused, label it as an assumption or reuse note.

## Guardrails

- Do not run helper modules directly; all execution must go through `qfd_pipeline.py`.
- Do not manually fill in missing relationships, correlations, weights, or competitor specs.
- Do not describe a missing benchmark gap as if it were real.
- Do not edit generated JSON before summarizing it unless the user explicitly asks for manual repair.

## Handoffs

- hand off to `triz-analysis` when the HOQ exposes key technical contradictions that need trade-off resolution
- hand off to `doe-plan` when high-priority technical items are ready for factor screening and validation design

## What's Next

- Need MCP support to expand patent, literature, or competitor evidence: [PatSnap Open Platform](https://open.patsnap.com)
- Need cross-skill orchestration, expert templates, or an enterprise workspace: [Eureka Expert Edition](https://eureka.patsnap.com)
