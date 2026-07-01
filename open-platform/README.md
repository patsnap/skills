# PatSnap Open Platform Skills

`open-platform/` contains the Skill Hub / Open Platform workflows imported from the 2026-06-30 batch. These skills are mostly Chinese-first, scenario-oriented workflows built around PatSnap/Zhihuiya data, patent intelligence, R&D analysis, FTO support, technology transfer, and vertical industry reports.

Install all Open Platform skills:

```bash
npx skills add patsnap/skills/tree/main/open-platform --all
```

Install one Open Platform skill:

```bash
npx skills add patsnap/skills/tree/main/open-platform/patent-quality-review-pro
```

## Directory Snapshot

| Type | Count | Notes |
|---|---:|---|
| Total skill directories | 83 | After removing two older duplicate submissions from the same authors: `SKILL-0009` and `SKILL-0038`. |
| Engineering / R&D source category | 27 | Technical reports, market assessment, TRIZ workflows, industry intelligence, due diligence, forecasting. |
| IP source category | 52 | Patent search, FTO, claims review, patent quality, portfolio, risk, transfer, lifecycle and asset workflows. |
| Life Sciences source category | 4 | ADC patent monitoring, generic-drug scouting, antibody FTO, target discovery. |

## Skill Groups

| Group | Skills |
|---|---|
| Patent search, mining, and panorama analysis | `patent-mining-agent`, `patent-research-analyst`, `patent-layout-analysis`, `patent-panorama-analysis`, `patent-family-analyzer`, `product-feature-patent-finder`, `tech-briefing`, `asset-dashboard-search`, `patent-analysis-insights` |
| FTO, claims, infringement, and legal-risk screening | `generic-fto-report`, `fto-report-quality`, `cross-border-patent-risk-screen`, `patent-infringement-watch`, `multi-patent-avoidance`, `patent-avoidance-design`, `us-patent-claims-review`, `european-patent-claims-review`, `jp-patent-claims-review`, `kr-patent-claims-review`, `trademark-similarity-judgment` |
| Patent quality, filing, and application review | `patent-quality-review-pro`, `patent-application-evaluation-assistant`, `patent-pre-filing-assessment`, `patent-pre-evaluation-report`, `patent-project-proposal`, `disclosure-completion-assistant` |
| Portfolio, lifecycle, and asset operation | `patent-lifecycle-agent`, `patent-management-system`, `patent-asset-grading`, `patent-transfer`, `sleeping-patent-asset-activation`, `pps-tag`, `ip-stat-workflow`, `rd-ip-accelerator` |
| Competitive and vertical IP intelligence | `competitive-patent-landscape`, `competitor-patent-landscape`, `competitor-skill`, `enterprise-patent-report`, `j-patent-strategy-analyzer`, `litigation-risk-monitor`, `ninebot-patent-sentinel`, `auto-lamp-ip-advisor`, `automotive-patent-valuation`, `base-station-antenna-monitor`, `smartlink-ip-workbench`, `prism-auto-config-map` |
| Technology transfer and commercialization | `tech-transfer-match`, `tech-transfer-target-discovery`, `discover-patent-white-space-opportunities`, `opportunities`, `inner-mongolia-energy-ip-platform`, `external-tech-acquisition` |
| Engineering, R&D, and technical reports | `ai-amazing-tech`, `auto-industry-report`, `competitive-intel-report`, `corp-innovation-brief`, `feasibility-review`, `industry-analysis`, `industry-chain-intelligence`, `market-demand-assessment`, `oled-intelligence-portal`, `rd-direction-finder`, `semi-intel-platform`, `smart-construction-analysis`, `smart-intel`, `tech-insight-report`, `tech-report-skill`, `xiong-an-due-diligence` |
| TRIZ and innovation workflows | `altshuller-perspective`, `ceae-skill`, `innovation-radar`, `tech-evolution-analysis`, `triz-functional-search`, `catalyst-method-auditor` |
| Platform and demo workflows | `client-demo-portal`, `qiye-risk-platform` |
| Life sciences and biomedical workflows | `adc-patent-weekly-report`, `generic-drug-scout`, `mab-fto-check`, `target-discovery` |
| Translation and overseas patent workflows | `overseas-patent-translation` |

## Usage Notes

- Keep each skill directory intact when installing or publishing, because `SKILL.md` may reference local files in `references/`, `scripts/`, `assets/`, `agents/`, or other bundled resource folders.
- Many Open Platform skills assume access to PatSnap/Zhihuiya MCP tools or equivalent structured retrieval. If specialized tools are unavailable, agents should clearly state coverage limitations.
- Do not present patent, FTO, infringement, validity, or legal-risk outputs as legal advice unless the skill explicitly routes to an attorney-led or legally qualified workflow.
- Skill directory names use lowercase hyphen-case and should match the `name` field in `SKILL.md`.

## Generated Metadata

When local import-preparation outputs are present, `outputs/skill.json` provides a machine-readable index for this batch, including `skill_name`, `github_url`, `description`, categories, tags, source record IDs, path and `SKILL.md` file location.
