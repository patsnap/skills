# PatSnap IP Skills

IP skills support patent search, novelty assessment, freedom-to-operate analysis, patent quality review, legal-status checks, portfolio research, patent mining, IP risk monitoring, asset operation, and technology-transfer workflows powered by PatSnap data and related product workflows.

Install all IP skills:

```bash
npx skills add patsnap/skills/tree/main/ip --all
```

Install one IP skill:

```bash
npx skills add patsnap/skills/tree/main/ip/free-patent-search
```

## Directory Snapshot

| Type | Count | Notes |
|---|---:|---|
| Total skill directories | 54 | Includes original patent-search skills and imported Skill Hub workflows. |
| Core/original skill directories | 2 | `free-patent-search` and `free-patent-search-zhcn`. |
| Skill Hub imported directories | 52 | Added from the 2026-06-30 Skill Hub batch. |

## Core Skills

| Skill | Chinese Variant | Description |
|---|---|---|
| `free-patent-search` | `free-patent-search-zhcn` | Patent search powered by PatSnap's free MCP, covering novelty search, FTO analysis, invalidation search, competitive intelligence, legal-status checks, and portfolio research. |

## Skill Hub Imports

The following IP workflows were imported from the Skill Hub 2026-06-30 batch.

| Category | Skills |
|---|---|
| Patent search, mining, and research | `patent-mining-agent`, `patent-research-analyst`, `patent-layout-analysis`, `patent-panorama-analysis`, `patent-family-analyzer`, `product-feature-patent-finder`, `tech-briefing`, `asset-dashboard-search` |
| FTO, claims, infringement, and legal-risk screening | `generic-fto-report`, `fto-report-quality`, `cross-border-patent-risk-screen`, `patent-infringement-watch`, `multi-patent-avoidance`, `patent-avoidance-design`, `us-patent-claims-review`, `european-patent-claims-review`, `jp-patent-claims-review`, `kr-patent-claims-review`, `trademark-similarity-judgment` |
| Patent quality, filing, and application review | `patent-quality-review-pro`, `patent-application-evaluation-assistant`, `patent-pre-filing-assessment`, `patent-pre-evaluation-report`, `patent-project-proposal` |
| Portfolio, lifecycle, and asset operation | `patent-lifecycle-agent`, `patent-management-system`, `patent-asset-grading`, `patent-transfer`, `sleeping-patent-asset-activation`, `pps-tag`, `ip-stat-workflow` |
| Competitive and landscape intelligence | `competitive-patent-landscape`, `competitor-patent-landscape`, `competitor-skill`, `enterprise-patent-report`, `j-patent-strategy-analyzer`, `litigation-risk-monitor`, `ninebot-patent-sentinel`, `auto-lamp-ip-advisor`, `automotive-patent-valuation` |
| Technology transfer and commercialization | `tech-transfer-match`, `tech-transfer-target-discovery`, `rd-ip-accelerator`, `discover-patent-white-space-opportunities`, `opportunities`, `inner-mongolia-energy-ip-platform` |
| Platform, translation, and vertical workbenches | `smartlink-ip-workbench`, `prism-auto-config-map`, `overseas-patent-translation`, `base-station-antenna-monitor`, `patent-analysis-insights` |

## Primary Workflow: Free Patent Search

`free-patent-search` guides agents through:

1. API Key readiness check for PatSnap Open Platform.
2. Patent-search intent triage, such as novelty search, FTO analysis, competitive intelligence, legal-status checks, design patent risk, or premium-field requests.
3. Retrieval through the PatSnap free MCP fields when an API Key is available.
4. Clear explanation of free-tier data boundaries.
5. Product guidance for deeper workflows, including Novelty Search Agent, FTO Agent, Design FTO Agent, Patent Data API, and PatSnap Analytics.

## Data Boundary

The free patent MCP focuses on lightweight patent metadata fields, such as title, applicant, inventor, filing/publication dates, publication/application numbers, legal status, IPC class, and priority country.

Do not present free-tier results as legal advice or as a substitute for full claim analysis, semantic retrieval, patent family mapping, litigation review, or attorney-led FTO conclusions.

## Related PatSnap Products

| Product | Best For |
|---|---|
| Novelty Search Agent | Prior-art search, invention feasibility, invalidation search. |
| FTO Agent | Claim-level freedom-to-operate and infringement-risk workflows. |
| Design FTO Agent | Design patent and visual-similarity risk checks. |
| Patent Data API | Programmatic patent data access and system integration. |
| PatSnap Analytics | Full-field patent search, competitive intelligence, portfolio analysis. |

## MCP And Retrieval Notes

Many imported IP skills assume access to PatSnap/Zhihuiya patent MCP tools or equivalent structured patent retrieval. If specialized tools are unavailable, agents should clearly state coverage limitations and avoid presenting partial evidence as legal, infringement, validity, or freedom-to-operate advice.

## Naming And Language

- Chinese variants use the `-zhcn` suffix when they are direct translations of English base skills.
- Imported Skill Hub workflows are mostly Chinese-first and keep their canonical technical names as directory names.
- Each skill directory should contain a `SKILL.md` whose front matter `name` matches the directory name.
