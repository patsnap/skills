# Patsnap Agent Skills

This repository contains Patsnap procedural knowledge skills for AI agents. The skills cover core intellectual property search, R&D and engineering analysis, pharmaceutical and biomedical intelligence, materials science, and the imported Open Platform workflow library.

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
| Life Sciences | `life-sciences/` | 32 | 16 pharmaceutical and biomedical intelligence skills in English and Chinese. |
| Materials | `materials/` | 10 | Includes materials explanation, technology scouting, problem solving, product translation and alloy composition search skills. |
| Open Platform | `open-platform/` | 181 | Skill Hub imported workflows for IP, R&D, engineering, life sciences, reports, FTO, patent operations, technology transfer and vertical intelligence. |

## Open Platform Imports

The 2026-06-30, 2026-07-03, 2026-07-09, 2026-08-11 and 2026-09-17 Skill Hub batches have been normalized into the top-level `open-platform/` directory instead of being mixed into the core domain directories.

| Domain | Imported skills |
|---|---:|
| Imports before 2026-08-11 | 119 |
| 2026-08-11 Engineering / R&D source category | 15 |
| 2026-08-11 IP source category | 38 |
| 2026-08-11 Life Sciences source category | 6 |
| Additional Smart Document API skill | 1 |
| 2026-09-17 Company assessment and FTO skills | 2 |
| Total imported skill directories | 181 |

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

Core patent-search skills powered by Patsnap data and related product workflows.

| Skill | Description |
|---|---|
| `free-patent-search` | Patent search powered by Patsnap's free MCP, covering novelty search, lightweight FTO triage, competitive intelligence, legal-status checks and portfolio research. |

### Life Sciences

The 16 Life Sciences skills are available in English and Chinese. See the [Life Sciences README](life-sciences/README.md) for installation and migration from the previous skill names.

| English skill | Chinese skill | Scope |
|---|---|---|
| [`patsnap-lifescience-biomarker-analysis`](life-sciences/patsnap-lifescience-biomarker-analysis/SKILL.md) | [`patsnap-lifescience-biomarker-analysis-zhcn`](life-sciences/patsnap-lifescience-biomarker-analysis-zhcn/SKILL.md) | Biomarker evidence, testing, companion diagnostics and biomarker-defined populations. |
| [`patsnap-lifescience-catalyst-events`](life-sciences/patsnap-lifescience-catalyst-events/SKILL.md) | [`patsnap-lifescience-catalyst-events-zhcn`](life-sciences/patsnap-lifescience-catalyst-events-zhcn/SKILL.md) | Upcoming pharmaceutical milestones and their timing. |
| [`patsnap-lifescience-clinical-outcome-analysis`](life-sciences/patsnap-lifescience-clinical-outcome-analysis/SKILL.md) | [`patsnap-lifescience-clinical-outcome-analysis-zhcn`](life-sciences/patsnap-lifescience-clinical-outcome-analysis-zhcn/SKILL.md) | Clinical trial outcomes, endpoints, efficacy and safety evidence. |
| [`patsnap-lifescience-commercial-analysis`](life-sciences/patsnap-lifescience-commercial-analysis/SKILL.md) | [`patsnap-lifescience-commercial-analysis-zhcn`](life-sciences/patsnap-lifescience-commercial-analysis-zhcn/SKILL.md) | Commercial performance, market size, pricing and access. |
| [`patsnap-lifescience-company-profiling`](life-sciences/patsnap-lifescience-company-profiling/SKILL.md) | [`patsnap-lifescience-company-profiling-zhcn`](life-sciences/patsnap-lifescience-company-profiling-zhcn/SKILL.md) | Pharmaceutical company portfolios, pipelines and business activity. |
| [`patsnap-lifescience-deal-intelligence`](life-sciences/patsnap-lifescience-deal-intelligence/SKILL.md) | [`patsnap-lifescience-deal-intelligence-zhcn`](life-sciences/patsnap-lifescience-deal-intelligence-zhcn/SKILL.md) | Biopharma licensing, partnerships and deal terms. |
| [`patsnap-lifescience-disease-investigation`](life-sciences/patsnap-lifescience-disease-investigation/SKILL.md) | [`patsnap-lifescience-disease-investigation-zhcn`](life-sciences/patsnap-lifescience-disease-investigation-zhcn/SKILL.md) | Disease characteristics, treatment pathways and drug development. |
| [`patsnap-lifescience-drug-development-pathway`](life-sciences/patsnap-lifescience-drug-development-pathway/SKILL.md) | [`patsnap-lifescience-drug-development-pathway-zhcn`](life-sciences/patsnap-lifescience-drug-development-pathway-zhcn/SKILL.md) | Drug development strategy, milestones and clinical programs. |
| [`patsnap-lifescience-epidemiology-analysis`](life-sciences/patsnap-lifescience-epidemiology-analysis/SKILL.md) | [`patsnap-lifescience-epidemiology-analysis-zhcn`](life-sciences/patsnap-lifescience-epidemiology-analysis-zhcn/SKILL.md) | Disease incidence, prevalence and population estimates. |
| [`patsnap-lifescience-gwas-target-discovery`](life-sciences/patsnap-lifescience-gwas-target-discovery/SKILL.md) | [`patsnap-lifescience-gwas-target-discovery-zhcn`](life-sciences/patsnap-lifescience-gwas-target-discovery-zhcn/SKILL.md) | Human genetic and GWAS evidence for drug target prioritization. |
| [`patsnap-lifescience-patent-intelligence`](life-sciences/patsnap-lifescience-patent-intelligence/SKILL.md) | [`patsnap-lifescience-patent-intelligence-zhcn`](life-sciences/patsnap-lifescience-patent-intelligence-zhcn/SKILL.md) | Pharmaceutical patent search and patent landscape analysis. |
| [`patsnap-lifescience-pharmaceuticals-exploration`](life-sciences/patsnap-lifescience-pharmaceuticals-exploration/SKILL.md) | [`patsnap-lifescience-pharmaceuticals-exploration-zhcn`](life-sciences/patsnap-lifescience-pharmaceuticals-exploration-zhcn/SKILL.md) | Drug profiles, mechanisms, indications and development status. |
| [`patsnap-lifescience-pharmacovigilance`](life-sciences/patsnap-lifescience-pharmacovigilance/SKILL.md) | [`patsnap-lifescience-pharmacovigilance-zhcn`](life-sciences/patsnap-lifescience-pharmacovigilance-zhcn/SKILL.md) | Post-marketing safety signals and regulatory safety communications. |
| [`patsnap-lifescience-precision-oncology`](life-sciences/patsnap-lifescience-precision-oncology/SKILL.md) | [`patsnap-lifescience-precision-oncology-zhcn`](life-sciences/patsnap-lifescience-precision-oncology-zhcn/SKILL.md) | Oncology variant interpretation and biomarker-guided treatment evidence. |
| [`patsnap-lifescience-regulatory-analysis`](life-sciences/patsnap-lifescience-regulatory-analysis/SKILL.md) | [`patsnap-lifescience-regulatory-analysis-zhcn`](life-sciences/patsnap-lifescience-regulatory-analysis-zhcn/SKILL.md) | Drug approvals, labels and regulatory pathways. |
| [`patsnap-lifescience-target-intelligence`](life-sciences/patsnap-lifescience-target-intelligence/SKILL.md) | [`patsnap-lifescience-target-intelligence-zhcn`](life-sciences/patsnap-lifescience-target-intelligence-zhcn/SKILL.md) | Biomedical target biology, druggability and competitive pipelines. |

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
| Patsnap LifeScience MCP | Life Sciences, Open Platform | Life Sciences skills and imported biomedical Open Platform workflows | Drugs, targets, diseases, biomarkers, companies, patents, papers, clinical trials and related pharma intelligence. |
| Patsnap / Zhihuiya patent MCP | IP, Open Platform | Free patent search plus imported patent, FTO, portfolio, transfer and competitive-intelligence workflows | Patent retrieval, applicant/topic search, legal status, patent evidence collection and workflow-specific analysis. |
| `mace-mcp` | Materials | `alloy-composition-search` | Alloy composition extraction: `query_to_alloy` -> `alloy_to_substance` -> `substance_to_document` -> `document_to_alloy`. |

## Naming And Language

- Skill directory names use lowercase hyphen-case and should match the `name` field in `SKILL.md`.
- Chinese skill variants use the `-zhcn` suffix when they are a translated counterpart of an English base skill.
- Imported Skill Hub / Open Platform skills are mostly Chinese-first workflows and keep their canonical technical names as directory names under `open-platform/`.
- Each `SKILL.md` front matter should include only `name` and `description` unless a host-specific format explicitly requires otherwise.
