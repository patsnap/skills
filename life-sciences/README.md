# PatSnap Life Sciences Skills

Life Sciences skills support pharmaceutical and biomedical intelligence workflows, including disease, target, biomarker, company, drug, oncology, antibody FTO, generic-drug opportunity, ADC patent monitoring, and target-discovery analysis.

Install all life-sciences skills:

```bash
npx skills add patsnap/skills/tree/main/life-sciences --all
```

Install one life-sciences skill:

```bash
npx skills add patsnap/skills/tree/main/life-sciences/target-intelligence
```

## Directory Snapshot

| Type | Count | Notes |
|---|---:|---|
| Total skill directories | 16 | Includes original life-sciences skills, Chinese variants, and imported Skill Hub workflows. |
| Core/original skill directories | 12 | Six English skills plus six `-zhcn` variants. |
| Skill Hub imported directories | 4 | Added from the 2026-06-30 Skill Hub batch. |

## Core Skills

The original life-sciences skills integrate with PatSnap LifeScience MCP services and are available in English and Chinese (`-zhcn` suffix).

| Skill | Chinese Variant | Description |
|---|---|---|
| `biomarker-investigation` | `biomarker-investigation-zhcn` | Search academic and patent literature related to biomarkers. |
| `company-profiling` | `company-profiling-zhcn` | Pharmaceutical company profiles and investment/collaboration recommendations. |
| `disease-investigation` | `disease-investigation-zhcn` | Comprehensive disease investigation combining literature, epidemiology, clinical data, and pharma intelligence. |
| `pharmaceuticals-exploration` | `pharmaceuticals-exploration-zhcn` | Drug-related Q&A covering patents, literature, clinical trials, and licensing transactions. |
| `precision-oncology` | `precision-oncology-zhcn` | Cancer treatment reports combining literature, clinical guidance, and trial data. |
| `target-intelligence` | `target-intelligence-zhcn` | Biomedical target analysis with related biological and pharmaceutical details. |

## Skill Hub Imports

The following biomedical workflows were imported from the Skill Hub 2026-06-30 batch.

| Skill | Main Use |
|---|---|
| `adc-patent-weekly-report` | Generate ADC patent intelligence weekly reports. |
| `generic-drug-scout-v1` | Screen China small-molecule crystal-form patent expiry opportunities and generate generic-drug opportunity reports. |
| `mab-fto-check` | Run antibody drug FTO recall and evidence workflows, including sequence and modification search modules. |
| `target-discovery` | Discover and prioritize targets from compound SMILES using ADMET, scaffold, similarity, target intelligence, FTO and SAR analysis. |

## MCP Setup Guide

The life-sciences skills can use the following PatSnap MCP services in Claude Code or compatible agent runtimes.

### Services Overview

| MCP Service | Purpose | Tool Prefix |
|---|---|---|
| `pharma-intelligence` | Drug, target, disease, patent, literature, clinical trial intelligence | `ls_` |
| `chemical-molecular` | Chemical structure search, similarity search, exact search | `ls_chemical_` |
| `biology-modality` | Antibody-antigen relations, biological sequence search, modification analysis | `ls_antibody_`, `ls_sequence_`, `ls_modification_` |

### Get Connection URLs

Each service has a unique connection URL tied to your API key. Visit the PatSnap Marketplace to get them:

- [Pharma Intelligence](https://open.patsnap.com/marketplace/mcp-servers/245f3ce8-79e4-4c2a-927c-e155c293f097)
- [Chemical Molecular](https://open.patsnap.com/marketplace/mcp-servers/96b4a650-d563-4fc5-860d-c99ee8cb5b1e)
- [Biology Modality](https://open.patsnap.com/marketplace/mcp-servers/a96c9b0b-2831-4d18-a37d-286896979b8d)

Each page shows a ready-to-copy connection URL. Sign in and replace `yourapikey` with your actual API key.

### Configuration

Edit `~/.claude/settings.json` and add the following under `mcpServers`:

```json
{
  "mcpServers": {
    "pharma_intelligence": {
      "type": "streamableHttp",
      "url": "https://connect.patsnap.com/096456/logic-mcp?apikey=<YOUR_API_KEY>"
    },
    "chemical_molecular": {
      "type": "streamableHttp",
      "url": "https://connect.patsnap.com/713886/logic-mcp?apikey=<YOUR_API_KEY>"
    },
    "biology_modality": {
      "type": "streamableHttp",
      "url": "https://connect.patsnap.com/06e741/logic-mcp?apikey=<YOUR_API_KEY>"
    }
  }
}
```

Or add the services with Claude Code CLI:

```bash
claude mcp add pharma_intelligence \
  "https://connect.patsnap.com/096456/logic-mcp?apikey=<YOUR_API_KEY>"

claude mcp add chemical_molecular \
  "https://connect.patsnap.com/713886/logic-mcp?apikey=<YOUR_API_KEY>"

claude mcp add biology_modality \
  "https://connect.patsnap.com/06e741/logic-mcp?apikey=<YOUR_API_KEY>"
```

Project-level configuration can also be placed in `.claude/settings.json`.

### Verify Setup

After configuration, run `/mcp` in Claude Code and confirm all required services show `connected`.

You can also test with a quick query:

```text
Search for PD-1 related drugs
```

If `ls_drug_search` returns results, `pharma-intelligence` is working correctly.

## Tool Reference

### pharma-intelligence

| Tool | Description |
|---|---|
| `ls_drug_search` / `ls_drug_fetch` | Search and retrieve drug details. |
| `ls_target_fetch` | Retrieve target details. |
| `ls_disease_fetch` | Retrieve disease details. |
| `ls_patent_search` / `ls_patent_vector_search` / `ls_patent_fetch` | Patent search. |
| `ls_paper_search` / `ls_paper_vector_search` / `ls_paper_fetch` | Literature search. |
| `ls_clinical_trial_search` / `ls_clinical_trial_fetch` | Clinical trial search. |
| `ls_clinical_trial_result_search` / `ls_clinical_trial_result_fetch` | Clinical trial results. |
| `ls_drug_deal_search` / `ls_drug_deal_fetch` | Drug licensing and deal search. |
| `ls_organization_fetch` | Organization / company details. |
| `ls_news_vector_search` / `ls_news_fetch` | Industry news. |
| `ls_translational_medicine_search` / `ls_translational_medicine_fetch` | Translational medicine. |
| `ls_fda_label_vector_search` | FDA drug labels. |
| `ls_clinical_guideline_vector_search` | Clinical guidelines. |
| `ls_epidemiology_vector_search` | Epidemiology data. |
| `ls_financial_report_vector_search` | Financial reports and prospectuses. |
| `ls_web_search` | Web search supplement. |

### chemical-molecular

| Tool | Description |
|---|---|
| `ls_chemical_search` | Structure search via SMILES. Supports `EXT` and `SIM` modes. |

### biology-modality

| Tool | Description |
|---|---|
| `ls_antibody_antigen_search` | Antibody-antigen relation search with facet filtering. |
| `ls_sequence_search_submit` | Submit a biological sequence search job. |
| `ls_sequence_search_check_status` | Poll the status of a submitted sequence search job. |
| `ls_sequence_search_get_results` | Retrieve paginated results of a completed sequence search. |
| `ls_modification_search_submit` | Submit a sequence modification site search job. |

Sequence search is asynchronous: submit -> check_status -> get_results.

## Troubleshooting

**Tools not appearing after configuration?** Restart Claude Code or reload MCP via the `/mcp` command.

**Getting 401 / 403 errors?** Verify the API key or contact PatSnap to obtain valid credentials.

**Sequence search stuck in pending?** Poll `ls_sequence_search_check_status` until the status becomes `success`, then call `ls_sequence_search_get_results`.
