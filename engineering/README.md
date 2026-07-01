# PatSnap Engineering Skills

Engineering skills support R&D, technology analysis, competitive assessment, project review, structured innovation, industry intelligence, product planning, and technical-report workflows.

Install all engineering skills:

```bash
npx skills add patsnap/skills/tree/main/engineering --all
```

Install one engineering skill:

```bash
npx skills add patsnap/skills/tree/main/engineering/company-tech-profile
```

## Directory Snapshot

| Type | Count | Notes |
|---|---:|---|
| Total skill directories | 36 | Includes original engineering skills, Chinese variants, and imported Skill Hub workflows. |
| Core/original skill directories | 9 | Includes English/Chinese R&D analysis skills and TRIZ innovation workflow. |
| Skill Hub imported directories | 27 | Added from the 2026-06-30 Skill Hub batch. |

Most engineering skills follow this layout:

```text
<skill-name>/
├── SKILL.md
├── references/     # Optional detailed methods, templates, schemas, prompts
├── scripts/        # Optional deterministic workflow helpers
├── assets/         # Optional output templates or static resources
└── examples/       # Optional usage examples
```

Keep each skill directory intact when installing or publishing, because `SKILL.md` may reference local files in bundled resource folders.

## Core Skills

| Skill | Chinese Variant | Description |
|---|---|---|
| `company-tech-profile` | `company-tech-profile-zhcn` | Build a single-company technology profile and R&D assessment for a defined technology topic. |
| `competitive-landscape` | `competitive-landscape-zhcn` | Analyze a technology-sector competitive landscape with player tiering, differentiation, and white-space identification. |
| `tech-route-comparison` | `tech-route-comparison-zhcn` | Compare two or more technical routes, architectures, or solution paths using evidence-backed criteria. |
| `rd-initiation-review` | `rd-initiation-review-zhcn` | Review an R&D project proposal or initiation package for go/no-go decisions and risk mitigation. |
| `triz-innovation-pro` | - | Run TRIZ innovation solution analysis, including system component analysis, contact relationship analysis, functional modeling, causal-chain analysis, and solution generation. |

## Skill Hub Imports

The following engineering workflows were imported from the Skill Hub 2026-06-30 batch.

| Skill | Main Use |
|---|---|
| `ai-amazing-tech` | Route technology requests into panorama analysis, patent mining, or technical intelligence brief modules. |
| `altshuller-perspective` | Apply Genrich Altshuller's TRIZ perspective to innovation and technical problem analysis. |
| `auto-industry-report` | Generate automotive industry technology panorama reports. |
| `catalyst-method-auditor` | Audit catalyst preparation and evaluation plans for energy, chemical, and materials workflows. |
| `ceae-skill` | Analyze hardware product parameter root causes with a TRIZ-style collaborative workflow. |
| `client-demo-portal` | Build client-facing demo portals and reusable presentation assets. |
| `competitive-intel-report` | Generate competitive intelligence reports with structured evidence and report templates. |
| `corp-innovation-brief` | Produce corporate innovation and technology capability briefs. |
| `disclosure-completion-assistant` | Convert rough invention notes into structured patent disclosure materials. |
| `external-tech-acquisition` | Support external technology acquisition, due diligence, and evidence-chain workflows. |
| `feasibility-review` | Review feasibility reports and project-initiation materials. |
| `industry-analysis` | Generate integrated industry analysis reports. |
| `industry-chain-intelligence` | Produce industry-chain strategy reports for enterprise decision makers. |
| `innovation-radar` | Identify, classify, and evaluate R&D innovation points. |
| `inventor-resignation-monitor` | Monitor inventor resignation risks and generate follow-up briefs. |
| `market-demand-assessment` | Assess market demand and customer inquiry value before R&D handoff. |
| `oled-intelligence-portal` | Generate OLED or technology-field intelligence brief portals. |
| `qiye-risk-platform-v2` | Reconstruct a financial-institution risk management platform workflow. |
| `rd-direction-finder` | Generate R&D direction search reports for science and technology projects. |
| `semi-intel-platform` | Build semiconductor equipment intelligence platform reports. |
| `smart-construction-analysis` | Analyze smart-construction technologies and produce structured reports. |
| `smart-intel` | Generate smart intelligence reports and supporting artifacts. |
| `tech-evolution-analysis` | Forecast technology evolution using TRIZ routes, SVOP, patents, and literature signals. |
| `tech-insight-report` | Run a standardized technical topic insight report workflow. |
| `tech-report-skill` | Generate technical R&D briefs from configured topics and data. |
| `triz-functional-search` | Use function-oriented search to find cross-domain technical solutions. |
| `xiong-an-due-diligence` | Generate enterprise and technology due-diligence reports for Xiong'an-related scenarios. |

## Usage Guidance

Choose the skill by decision object:

| Task | Recommended Skill |
|---|---|
| Profile one company in one technology area | `company-tech-profile` |
| Compare multiple players in one technology arena | `competitive-landscape` |
| Compare technical routes or architectures | `tech-route-comparison` |
| Review a concrete R&D proposal or project package | `rd-initiation-review` |
| Generate TRIZ-based innovation solutions | `triz-innovation-pro` |
| Forecast product or technology evolution | `tech-evolution-analysis` |
| Generate a technical topic report | `tech-insight-report` or `tech-report-skill` |
| Evaluate market demand before R&D handoff | `market-demand-assessment` |

## MCP And Retrieval Notes

Engineering skills are designed to be tool-adaptive. They can use structured patent retrieval, paper retrieval, web research, PatSnap/Zhihuiya MCP tools, or user-provided materials when available. When specialized retrieval is unavailable, skills should degrade gracefully and state evidence limitations clearly.

## Naming And Language

- Chinese variants use the `-zhcn` suffix when they are direct translations of English base skills.
- Imported Skill Hub workflows are mostly Chinese-first and keep their canonical technical names as directory names.
- Each skill directory should contain a `SKILL.md` whose front matter `name` matches the directory name.
