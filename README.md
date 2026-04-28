# PatSnap Agent Skills

This repository contains official procedural knowledge skills for AI agents, powered by PatSnap's industry-leading data. Covering engineering analysis, life sciences, and materials science.

## Installation

```bash
npx skills add patsnap/skills/tree/main/life-sciences --all
```

## Structure

```
skills/
├── engineering/          # R&D and technology analysis
├── ip/                   # Intellectual property and innovation methodology
├── life-sciences/        # Pharmaceutical and biomedical intelligence
├── materials/            # Materials science and alloy research
└── README.md
```

## Skills Overview

### Engineering

General-purpose R&D analysis skills. Available in English and Chinese (`-zh` suffix).

| Skill | Description |
|-------|-------------|
| `company-tech-profile` | Single-company technology profile and R&D assessment for a defined technology topic |
| `competitive-landscape` | Technology-sector competitive landscape analysis with player tiering and white-space identification |
| `tech-route-comparison` | Evidence-backed comparison of two or more technical routes, architectures, or solution paths |
| `rd-initiation-review` | R&D project initiation pre-screen and proposal audit for go/no-go decisions |

### Life Sciences

Pharmaceutical and biomedical intelligence skills. All 6 skills integrate with the **lifesciences MCP** service for database retrieval.

| Skill | Description |
|-------|-------------|
| `patsnap-lifescience-biomarker-investigation` | Search academic and patent literature related to biomarkers |
| `patsnap-lifescience-company-profiling` | Pharmaceutical company profiles and investment/collaboration recommendations |
| `patsnap-lifescience-disease-investigation` | Comprehensive disease investigation combining literature, epidemiology, clinical data, and pharma intelligence |
| `patsnap-lifescience-pharmaceuticals-exploration` | Drug-related Q&A covering patents, literature, clinical trials, and licensing transactions |
| `patsnap-lifescience-precision-oncology` | Cancer treatment reports combining literature, clinical guidance, and trial data |
| `patsnap-lifescience-target-intelligence` | Biomedical target analysis with related biological and pharmaceutical details |

### IP (Intellectual Property & Innovation)

TRIZ-based innovation methodology skills for systematic inventive problem solving.

| Skill | Description |
|-------|-------------|
| `triz-innovation-pro` | TRIZ innovation solution analysis — system component analysis, contact relationship analysis, functional modeling, causal chain analysis, and innovation solution generation |

### Materials

Materials science and engineering skills for metals, polymers, ceramics, composites, and energy materials.

| Skill | Description | MCP |
|-------|-------------|-----|
| `understand-technology` | Explain materials science concepts, structure-property relationships, and processing methods | - |
| `scout-tech-landscape` | Analyze technology landscapes including value chains, key players, and R&D trends | - |
| `solve-tech-problems` | Solution-oriented analysis for materials engineering challenges | - |
| `tech-to-product` | Translate materials technologies into real-world products and systems | - |
| `alloy-composition-search` | Search, filter, and analyze alloy compositions from structured data and patent sources | `mace-mcp` |

## MCP Dependencies

Some skills rely on external MCP servers for data retrieval:

| MCP Server | Domain | Used By | Capabilities |
|------------|--------|---------|--------------|
| `lifesciences MCP` | Life Sciences | All 6 life-sciences skills | Pharmaceutical database retrieval (drugs, targets, diseases, biomarkers, companies, clinical trials) |
| `mace-mcp` | Materials | `alloy-composition-search` | Alloy composition extraction — `query_to_alloy` → `alloy_to_substance` → `substance_to_document` → `document_to_alloy` |

Skills without MCP dependencies work as pure prompt skills, generating responses from the model's knowledge and any user-provided context.

## Language Support

- **Engineering**: English + Chinese (separate `-zh` skill variants)
- **Life Sciences**: English (responds in user's language)
- **Materials**: English (responds in user's language)
