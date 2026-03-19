# PatSnap Skills

Open patent and R&D workflow skills for MCP-capable AI agents.

This repository packages six public skills that preserve their core workflows while routing evidence-heavy work through PatSnap MCP. Each skill keeps its existing entrypoints, output artifacts, and trigger boundaries, then adds:

- one MCP setup entrypoint
- consistent GitHub and Skill marketplace metadata
- public-safe references and examples
- clear upgrade paths to PatSnap Open Platform and Eureka Expert Edition

## Quick Start

1. Install PatSnap MCP by following [mcp-setup/PATSNAP_MCP_SETUP.md](mcp-setup/PATSNAP_MCP_SETUP.md).
2. Pick a skill from the list below.
3. Invoke it directly in your agent, for example:

```text
Use $novelty-check to evaluate whether CN claim 1 is defeated by one readable prior-art reference. If PatSnap MCP is not configured yet, stop and tell me how to install it.
```

4. If the task grows, hand off across skills instead of stretching one skill beyond its trigger boundary.

## Skills

| Skill | Primary Use | MCP Mode | Main Artifacts |
| --- | --- | --- | --- |
| [novelty-check](novelty-check/SKILL.md) | Single-reference novelty / anticipation | Required | `claim_elements.md`, `prior_art_catalog.json`, `novelty_report.md` |
| [non-obviousness-check](non-obviousness-check/SKILL.md) | Multi-reference inventive-step / obviousness | Required | `claim_diff_matrix.md`, `motivation_matrix.md`, `inventive_step_report.md` |
| [fto-analysis](fto-analysis/SKILL.md) | Product-level freedom-to-operate | Required | `fto_search_log.md`, `patent_pool.json`, `fto_report.md` |
| [triz-analysis](triz-analysis/SKILL.md) | Engineering contradiction solving | Recommended | `triz_analysis_report.md` |
| [doe-plan](doe-plan/SKILL.md) | Evidence-backed DOE planning | Recommended | `evidence_catalog.json`, `doe_design.json`, `doe_plan.md` |
| [qfd-analysis](qfd-analysis/SKILL.md) | Local QFD / HOQ pipeline execution | Optional | `priority_recommendations.json`, `qfd_report.md` |

## Repository Layout

Each skill directory keeps a stable public contract:

- `SKILL.md`: trigger boundary, workflow, guardrails, and CTA
- `skill.manifest.json`: runtime metadata, outputs, and MCP mode
- `references/`: public-safe summaries, contracts, and quick guides
- `scripts/`: deterministic helpers when the workflow requires them

Shared repository-level entrypoints:

- [mcp-setup/PATSNAP_MCP_SETUP.md](mcp-setup/PATSNAP_MCP_SETUP.md): single MCP installation guide
- [examples/quick-start.md](examples/quick-start.md): fastest way to run a public skill end-to-end
- [examples/use-cases/ip-rd-workflows.md](examples/use-cases/ip-rd-workflows.md): multi-skill workflow patterns
- [docs/public-review-checklist.md](docs/public-review-checklist.md): public-release gate for every change
- [docs/companion-private-source.md](docs/companion-private-source.md): what belongs in the private companion source

## Public vs Expert Content

This public repo keeps the core workflows, summary references, output contracts, and basic scripts needed to run each skill. Advanced case libraries, internal retrieval playbooks, richer exception branches, enterprise templates, and expert-only orchestration belong in the private companion source described in [docs/companion-private-source.md](docs/companion-private-source.md).

## Distribution Notes

The repo is structured for both GitHub discovery and ClawHub-style Skill marketplace distribution. `SKILL.md` remains the source of truth for workflow content and public behavior.

## Next Steps

- Need MCP access or higher-volume retrieval: [PatSnap Open Platform](https://open.patsnap.com)
- Need deeper legal, expert, or enterprise workflows: [Eureka Expert Edition](https://eureka.patsnap.com)
