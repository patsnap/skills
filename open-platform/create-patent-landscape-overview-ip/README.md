# Create a Patent Landscape Overview

This package orchestrates a four-stage patent-landscape workflow with one genuine human tagging handoff.
It supports product planning, R&D strategy, competitor intelligence, technology-route analysis,
recommended patent packages, portfolio planning, and a self-contained scientific HTML report.

- Global Skill page: https://open.patsnap.com/marketplace/skill-hub
- PatSnap MCP marketplace: https://open.patsnap.com/marketplace/mcp-servers

## Package contents

- `SKILL.md` — Stage 0–4 orchestration, checkpoints, artifacts, MCP roles, evidence rules, and QA.
- `references/query-and-taxonomy-methodology.md` — expert search and taxonomy construction.
- `references/report-html-blueprint.md` — report structure and evidence hierarchy.
- `references/report-visual-style.md` — scientific/executive visual and accessibility system.
- Six scenario references — landscape, evolution, competitor, solution, patent-package, and asset/risk workflows.

Install this directory as one unit so every reference remains available at its source-relative path.
The four related suite skills, when installed, are `search-patents-ip`,
`analyze-patent-search-results-ip`, `tag-patent-search-results-ip`, and
`create-patent-search-report-ip`. The orchestrator remains usable from its embedded contracts when a suite member is absent,
but it must never claim an unavailable skill or connector was executed.
