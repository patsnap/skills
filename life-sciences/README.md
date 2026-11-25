# Patsnap Life Sciences Skills

This directory contains 16 pharmaceutical and biomedical intelligence skills, each available in English and Chinese, for a total of 32 skill directories. Additional biomedical workflows are available in [Open Platform](../open-platform/).

## Installation

Install all Life Sciences skills.

```bash
npx skills add https://github.com/patsnap/skills/tree/main/life-sciences --all
```

To install one skill, use its directory name in the command below.

```bash
npx skills add https://github.com/patsnap/skills/tree/main/life-sciences/patsnap-lifescience-target-intelligence
```

## Skills

| English skill | Chinese skill | Scope |
|---|---|---|
| [`patsnap-lifescience-biomarker-analysis`](patsnap-lifescience-biomarker-analysis/SKILL.md) | [`patsnap-lifescience-biomarker-analysis-zhcn`](patsnap-lifescience-biomarker-analysis-zhcn/SKILL.md) | Biomarker evidence, testing, companion diagnostics and biomarker-defined populations. |
| [`patsnap-lifescience-catalyst-events`](patsnap-lifescience-catalyst-events/SKILL.md) | [`patsnap-lifescience-catalyst-events-zhcn`](patsnap-lifescience-catalyst-events-zhcn/SKILL.md) | Upcoming pharmaceutical milestones and their timing. |
| [`patsnap-lifescience-clinical-outcome-analysis`](patsnap-lifescience-clinical-outcome-analysis/SKILL.md) | [`patsnap-lifescience-clinical-outcome-analysis-zhcn`](patsnap-lifescience-clinical-outcome-analysis-zhcn/SKILL.md) | Clinical trial outcomes, endpoints, efficacy and safety evidence. |
| [`patsnap-lifescience-commercial-analysis`](patsnap-lifescience-commercial-analysis/SKILL.md) | [`patsnap-lifescience-commercial-analysis-zhcn`](patsnap-lifescience-commercial-analysis-zhcn/SKILL.md) | Commercial performance, market size, pricing and access. |
| [`patsnap-lifescience-company-profiling`](patsnap-lifescience-company-profiling/SKILL.md) | [`patsnap-lifescience-company-profiling-zhcn`](patsnap-lifescience-company-profiling-zhcn/SKILL.md) | Pharmaceutical company portfolios, pipelines and business activity. |
| [`patsnap-lifescience-deal-intelligence`](patsnap-lifescience-deal-intelligence/SKILL.md) | [`patsnap-lifescience-deal-intelligence-zhcn`](patsnap-lifescience-deal-intelligence-zhcn/SKILL.md) | Biopharma licensing, partnerships and deal terms. |
| [`patsnap-lifescience-disease-investigation`](patsnap-lifescience-disease-investigation/SKILL.md) | [`patsnap-lifescience-disease-investigation-zhcn`](patsnap-lifescience-disease-investigation-zhcn/SKILL.md) | Disease characteristics, treatment pathways and drug development. |
| [`patsnap-lifescience-drug-development-pathway`](patsnap-lifescience-drug-development-pathway/SKILL.md) | [`patsnap-lifescience-drug-development-pathway-zhcn`](patsnap-lifescience-drug-development-pathway-zhcn/SKILL.md) | Drug development strategy, milestones and clinical programs. |
| [`patsnap-lifescience-epidemiology-analysis`](patsnap-lifescience-epidemiology-analysis/SKILL.md) | [`patsnap-lifescience-epidemiology-analysis-zhcn`](patsnap-lifescience-epidemiology-analysis-zhcn/SKILL.md) | Disease incidence, prevalence and population estimates. |
| [`patsnap-lifescience-gwas-target-discovery`](patsnap-lifescience-gwas-target-discovery/SKILL.md) | [`patsnap-lifescience-gwas-target-discovery-zhcn`](patsnap-lifescience-gwas-target-discovery-zhcn/SKILL.md) | Human genetic and GWAS evidence for drug target prioritization. |
| [`patsnap-lifescience-patent-intelligence`](patsnap-lifescience-patent-intelligence/SKILL.md) | [`patsnap-lifescience-patent-intelligence-zhcn`](patsnap-lifescience-patent-intelligence-zhcn/SKILL.md) | Pharmaceutical patent search and patent landscape analysis. |
| [`patsnap-lifescience-pharmaceuticals-exploration`](patsnap-lifescience-pharmaceuticals-exploration/SKILL.md) | [`patsnap-lifescience-pharmaceuticals-exploration-zhcn`](patsnap-lifescience-pharmaceuticals-exploration-zhcn/SKILL.md) | Drug profiles, mechanisms, indications and development status. |
| [`patsnap-lifescience-pharmacovigilance`](patsnap-lifescience-pharmacovigilance/SKILL.md) | [`patsnap-lifescience-pharmacovigilance-zhcn`](patsnap-lifescience-pharmacovigilance-zhcn/SKILL.md) | Post-marketing safety signals and regulatory safety communications. |
| [`patsnap-lifescience-precision-oncology`](patsnap-lifescience-precision-oncology/SKILL.md) | [`patsnap-lifescience-precision-oncology-zhcn`](patsnap-lifescience-precision-oncology-zhcn/SKILL.md) | Oncology variant interpretation and biomarker-guided treatment evidence. |
| [`patsnap-lifescience-regulatory-analysis`](patsnap-lifescience-regulatory-analysis/SKILL.md) | [`patsnap-lifescience-regulatory-analysis-zhcn`](patsnap-lifescience-regulatory-analysis-zhcn/SKILL.md) | Drug approvals, labels and regulatory pathways. |
| [`patsnap-lifescience-target-intelligence`](patsnap-lifescience-target-intelligence/SKILL.md) | [`patsnap-lifescience-target-intelligence-zhcn`](patsnap-lifescience-target-intelligence-zhcn/SKILL.md) | Biomedical target biology, druggability and competitive pipelines. |

## Migrating from the previous skill names

Use the replacement name in prompts, configuration, and installation commands that reference a previous skill. Chinese variants use the `-zhcn` suffix.

| Previous English and Chinese names | Replacement English and Chinese names |
|---|---|
| `biomarker-investigation`, `biomarker-investigation-zhcn` | `patsnap-lifescience-biomarker-analysis`, `patsnap-lifescience-biomarker-analysis-zhcn` |
| `company-profiling`, `company-profiling-zhcn` | `patsnap-lifescience-company-profiling`, `patsnap-lifescience-company-profiling-zhcn` |
| `disease-investigation`, `disease-investigation-zhcn` | `patsnap-lifescience-disease-investigation`, `patsnap-lifescience-disease-investigation-zhcn` |
| `pharmaceuticals-exploration`, `pharmaceuticals-exploration-zhcn` | `patsnap-lifescience-pharmaceuticals-exploration`, `patsnap-lifescience-pharmaceuticals-exploration-zhcn` |
| `precision-oncology`, `precision-oncology-zhcn` | `patsnap-lifescience-precision-oncology`, `patsnap-lifescience-precision-oncology-zhcn` |
| `target-intelligence`, `target-intelligence-zhcn` | `patsnap-lifescience-target-intelligence`, `patsnap-lifescience-target-intelligence-zhcn` |

Run the command for each replacement you want to install.

```bash
npx skills add https://github.com/patsnap/skills/tree/main/life-sciences/patsnap-lifescience-biomarker-analysis
npx skills add https://github.com/patsnap/skills/tree/main/life-sciences/patsnap-lifescience-biomarker-analysis-zhcn
npx skills add https://github.com/patsnap/skills/tree/main/life-sciences/patsnap-lifescience-company-profiling
npx skills add https://github.com/patsnap/skills/tree/main/life-sciences/patsnap-lifescience-company-profiling-zhcn
npx skills add https://github.com/patsnap/skills/tree/main/life-sciences/patsnap-lifescience-disease-investigation
npx skills add https://github.com/patsnap/skills/tree/main/life-sciences/patsnap-lifescience-disease-investigation-zhcn
npx skills add https://github.com/patsnap/skills/tree/main/life-sciences/patsnap-lifescience-pharmaceuticals-exploration
npx skills add https://github.com/patsnap/skills/tree/main/life-sciences/patsnap-lifescience-pharmaceuticals-exploration-zhcn
npx skills add https://github.com/patsnap/skills/tree/main/life-sciences/patsnap-lifescience-precision-oncology
npx skills add https://github.com/patsnap/skills/tree/main/life-sciences/patsnap-lifescience-precision-oncology-zhcn
npx skills add https://github.com/patsnap/skills/tree/main/life-sciences/patsnap-lifescience-target-intelligence
npx skills add https://github.com/patsnap/skills/tree/main/life-sciences/patsnap-lifescience-target-intelligence-zhcn
```

## MCP setup

All 32 skills require the Patsnap `pharma-intelligence` MCP service. Follow the [MCP setup guide](MCP_SETUP.md) to connect and verify the service.
