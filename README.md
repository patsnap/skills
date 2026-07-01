# PatSnap Agent Skills

This repository contains PatSnap procedural knowledge skills for AI agents. The skills cover core intellectual property search, R&D and engineering analysis, pharmaceutical and biomedical intelligence, materials science, and the imported Open Platform workflow library.

Each skill is a self-contained directory with a required `SKILL.md` file and optional bundled resources such as `references/`, `scripts/`, `assets/`, `templates/`, and `agents/`.

## Installation

Install all skills from one domain:

```bash
npx skills add patsnap/skills/tree/main/ip --all
npx skills add patsnap/skills/tree/main/engineering --all
npx skills add patsnap/skills/tree/main/life-sciences --all
npx skills add patsnap/skills/tree/main/materials --all
npx skills add patsnap/skills/tree/main/open-platform --all
```

Install one skill:

```bash
npx skills add patsnap/skills/tree/main/ip/free-patent-search
```

## Structure

```text
skills/
├── engineering/          # Core R&D, technology analysis, innovation and TRIZ workflows
├── ip/                   # Core free patent-search workflows
├── life-sciences/        # Core pharmaceutical and biomedical intelligence workflows
├── materials/            # Materials science, technology scouting and alloy composition workflows
├── open-platform/        # Imported Skill Hub / Open Platform workflow skills
├── package.json
└── README.md
```

## Repository Snapshot

| Domain | Directory | Skill directories | Notes |
|---|---:|---:|---|
| Engineering / R&D | `engineering/` | 9 | Core R&D analysis skills, Chinese variants, and TRIZ innovation workflow. |
| IP / Patent Intelligence | `ip/` | 2 | Free patent-search skills in English and Chinese. |
| Life Sciences | `life-sciences/` | 12 | Original pharma intelligence skills and Chinese variants. |
| Materials | `materials/` | 10 | Includes materials explanation, technology scouting, problem solving, product translation and alloy composition search skills. |
| Open Platform | `open-platform/` | 83 | Skill Hub imported workflows for IP, R&D, engineering, life sciences, reports, FTO, patent operations, technology transfer and vertical intelligence. |

## Open Platform Imports

The 2026-06-30 Skill Hub batch has been normalized into the top-level `open-platform/` directory instead of being mixed into the core domain directories. Two older duplicate submissions from the same authors were removed from the import metadata (`SKILL-0009` and `SKILL-0038`), leaving the later submissions (`SKILL-0084` and `SKILL-0082`) as the retained records.

| Domain | Imported skills |
|---|---:|
| Engineering / R&D source category | 27 |
| IP source category | 52 |
| Life Sciences source category | 4 |
| Total imported skill directories | 83 |

The generated upload/index metadata is available locally at `outputs/skill.json` when the import-preparation outputs are present. It includes `skill_name`, `github_url`, `description`, domain, path and `SKILL.md` file location for the newly imported skills.

## Core Skills

### Engineering

General-purpose R&D analysis skills. Several core skills are available in English and Chinese (`-zhcn` suffix).

| Skill | Description |
|---|---|
| `company-tech-profile` | Single-company technology profile and R&D assessment for a defined technology topic. |
| `competitive-landscape` | Technology-sector competitive landscape analysis with player tiering and white-space identification. |
| `tech-route-comparison` | Evidence-backed comparison of technical routes, architectures or solution paths. |
| `rd-initiation-review` | R&D project initiation pre-screen and proposal audit for go/no-go decisions. |
| `triz-innovation-pro` | TRIZ innovation solution analysis with component, contact, functional and causal-chain workflows. |

### IP

Core patent-search skills powered by PatSnap data and related product workflows.

| Skill | Description |
|---|---|
| `free-patent-search` | Patent search powered by PatSnap's free MCP, covering novelty search, lightweight FTO triage, competitive intelligence, legal-status checks and portfolio research. |

### Life Sciences

Pharmaceutical and biomedical intelligence skills. The original six skills integrate with PatSnap LifeScience MCP services and are available in English and Chinese (`-zhcn` suffix).

| Skill | Description |
|---|---|
| `biomarker-investigation` | Search academic and patent literature related to biomarkers. |
| `company-profiling` | Pharmaceutical company profiles and investment/collaboration recommendations. |
| `disease-investigation` | Disease investigation combining literature, epidemiology, clinical data and pharma intelligence. |
| `pharmaceuticals-exploration` | Drug-related Q&A covering patents, literature, clinical trials and licensing transactions. |
| `precision-oncology` | Cancer treatment reports combining literature, clinical guidance and trial data. |
| `target-intelligence` | Biomedical target analysis with biological and pharmaceutical details. |

### Materials

Materials science and engineering skills for metals, polymers, ceramics, composites and energy materials.

| Skill | Description | MCP |
|---|---|---|
| `understand-technology` | Explain materials science concepts, structure-property relationships and processing methods. | - |
| `scout-tech-landscape` | Analyze technology landscapes including value chains, key players and R&D trends. | - |
| `solve-tech-problems` | Solution-oriented analysis for materials engineering challenges. | - |
| `tech-to-product` | Translate materials technologies into real-world products and systems. | - |
| `alloy-composition-search` | Search, filter and analyze alloy compositions from structured data and patent sources. | `mace-mcp` |

## MCP Dependencies

Some skills rely on external MCP servers for retrieval. Skills without MCP dependencies can still operate from user-provided context, bundled references, public sources or model reasoning, subject to the limits described in each `SKILL.md`.

| MCP Server / Tooling | Domain | Used By | Capabilities |
|---|---|---|---|
| PatSnap LifeScience MCP | Life Sciences, Open Platform | Original life-sciences skills and imported biomedical Open Platform workflows | Drugs, targets, diseases, biomarkers, companies, patents, papers, clinical trials and related pharma intelligence. |
| PatSnap / Zhihuiya patent MCP | IP, Open Platform | Free patent search plus imported patent, FTO, portfolio, transfer and competitive-intelligence workflows | Patent retrieval, applicant/topic search, legal status, patent evidence collection and workflow-specific analysis. |
| `mace-mcp` | Materials | `alloy-composition-search` | Alloy composition extraction: `query_to_alloy` -> `alloy_to_substance` -> `substance_to_document` -> `document_to_alloy`. |

## Naming And Language

- Skill directory names use lowercase hyphen-case and should match the `name` field in `SKILL.md`.
- Chinese skill variants use the `-zhcn` suffix when they are a translated counterpart of an English base skill.
- Imported Skill Hub / Open Platform skills are mostly Chinese-first workflows and keep their canonical technical names as directory names under `open-platform/`.
- Each `SKILL.md` front matter should include only `name` and `description` unless a host-specific format explicitly requires otherwise.
