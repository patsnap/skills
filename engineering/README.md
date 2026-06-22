# PatSnap Engineering Skills

Engineering skills support R&D, technology analysis, competitive assessment, project review, and structured innovation workflows. Each skill is packaged as a self-contained directory with a `SKILL.md` file and, where needed, supporting `references/`, `templates/`, and `examples/` folders.

## Available Skills

| Skill | Chinese Variant | Description |
|---|---|---|
| `company-tech-profile` | `company-tech-profile-zhcn` | Build a single-company technology profile and R&D assessment for a defined technology topic. |
| `competitive-landscape` | `competitive-landscape-zhcn` | Analyze a technology-sector competitive landscape with player tiering, differentiation, and white-space identification. |
| `tech-route-comparison` | `tech-route-comparison-zhcn` | Compare two or more technical routes, architectures, or solution paths using evidence-backed criteria. |
| `rd-initiation-review` | `rd-initiation-review-zhcn` | Review an R&D project proposal or initiation package for go/no-go decisions and risk mitigation. |
| `triz-innovation-pro` | - | Run TRIZ innovation solution analysis, including system component analysis, contact relationship analysis, functional modeling, causal chain analysis, and solution generation. |

## Language Variants

Chinese versions use the `-zhcn` suffix and are separate skill directories. Use the Chinese variant when the expected user interaction, report structure, and deliverables should be in Simplified Chinese.

## Directory Structure

Most engineering skills follow this layout:

```text
<skill-name>/
├── SKILL.md
├── references/
├── templates/
└── examples/
```

- `SKILL.md`: main protocol, routing logic, execution rules, and output requirements.
- `references/`: method notes, quality gates, source-routing guidance, evidence schema, and deliverable rules.
- `templates/`: starter files for request capture, workplan, reports, query logs, and claim/evidence ledgers.
- `examples/`: minimal prompts, fallback examples, and run structure examples.

`triz-innovation-pro` additionally includes TRIZ-specific reference modules and a `manifest.json`.

## Usage Guidance

Choose the skill by decision object:

| Task | Recommended Skill |
|---|---|
| Profile one company in one technology area | `company-tech-profile` |
| Compare multiple players in one technology arena | `competitive-landscape` |
| Compare technical routes or architectures | `tech-route-comparison` |
| Review a concrete R&D proposal or project package | `rd-initiation-review` |
| Generate TRIZ-based innovation solutions | `triz-innovation-pro` |

Keep each skill directory intact when installing or publishing, because `SKILL.md` may reference local files in `references/`, `templates/`, or `examples/`.

## MCP Dependencies

These skills are designed to be tool-agnostic. They can use structured retrieval, web research, or MCP tools when available, but they should degrade gracefully to user-provided context and traceable evidence logs when no specialized MCP server is connected.
