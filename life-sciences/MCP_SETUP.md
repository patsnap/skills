# PatSnap LifeScience MCP Setup Guide

This document explains how to configure the following three MCP services in Claude Code to enable the lifescience
skills.

---

## Services Overview

| MCP Service           | Purpose                                                                       | Tool Prefix                                        |
|-----------------------|-------------------------------------------------------------------------------|----------------------------------------------------|
| `pharma-intelligence` | Drug, target, disease, patent, literature, clinical trial intelligence        | `ls_`                                              |
| `chemical-molecular`  | Chemical structure search (similarity / exact match)                          | `ls_chemical_`                                     |
| `biology-modality`    | Antibody-antigen relations, biological sequence search, modification analysis | `ls_antibody_`, `ls_sequence_`, `ls_modification_` |

---

## Get Your Connection URLs

Each service has a unique connection URL tied to your API key. Visit the PatSnap Marketplace to get them:

- [Pharma Intelligence](https://open.patsnap.com/marketplace/mcp-servers/245f3ce8-79e4-4c2a-927c-e155c293f097)
- [Chemical Molecular](https://open.patsnap.com/marketplace/mcp-servers/96b4a650-d563-4fc5-860d-c99ee8cb5b1e)
- [Biology Modality](https://open.patsnap.com/marketplace/mcp-servers/a96c9b0b-2831-4d18-a37d-286896979b8d)

Each page shows a ready-to-copy connection URL. Sign in and replace `yourapikey` with your actual API key.

---

## Configuration

### Option 1: Edit settings.json (Recommended)

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

> Replace `<YOUR_API_KEY>` with your actual API key.

---

### Option 2: Claude Code CLI

```bash
claude mcp add pharma_intelligence \
  "https://connect.patsnap.com/096456/logic-mcp?apikey=<YOUR_API_KEY>"

claude mcp add chemical_molecular \
  "https://connect.patsnap.com/713886/logic-mcp?apikey=<YOUR_API_KEY>"

claude mcp add biology_modality \
  "https://connect.patsnap.com/06e741/logic-mcp?apikey=<YOUR_API_KEY>"
```

---

### Option 3: Project-level Configuration

Create `.claude/settings.json` in your project root using the same format as Option 1. Project-level config takes
precedence over global config.

---

## Verify the Setup

After configuration, run `/mcp` in Claude Code and confirm all three services show `connected`.

You can also test with a quick query:

```
Search for PD-1 related drugs
```

If `ls_drug_search` returns results, `pharma-intelligence` is working correctly.

---

## Tool Reference

### pharma-intelligence

| Tool                                                                   | Description                        |
|------------------------------------------------------------------------|------------------------------------|
| `ls_drug_search` / `ls_drug_fetch`                                     | Search and retrieve drug details   |
| `ls_target_fetch`                                                      | Retrieve target details            |
| `ls_disease_fetch`                                                     | Retrieve disease details           |
| `ls_patent_search` / `ls_patent_vector_search` / `ls_patent_fetch`     | Patent search                      |
| `ls_paper_search` / `ls_paper_vector_search` / `ls_paper_fetch`        | Literature search                  |
| `ls_clinical_trial_search` / `ls_clinical_trial_fetch`                 | Clinical trial search              |
| `ls_clinical_trial_result_search` / `ls_clinical_trial_result_fetch`   | Clinical trial results             |
| `ls_drug_deal_search` / `ls_drug_deal_fetch`                           | Drug licensing and deal search     |
| `ls_organization_fetch`                                                | Organization / company details     |
| `ls_news_vector_search` / `ls_news_fetch`                              | Industry news                      |
| `ls_translational_medicine_search` / `ls_translational_medicine_fetch` | Translational medicine             |
| `ls_fda_label_vector_search`                                           | FDA drug labels                    |
| `ls_clinical_guideline_vector_search`                                  | Clinical guidelines                |
| `ls_epidemiology_vector_search`                                        | Epidemiology data                  |
| `ls_financial_report_vector_search`                                    | Financial reports and prospectuses |
| `ls_web_search`                                                        | Web search supplement              |

### chemical-molecular

| Tool                 | Description                                                                               |
|----------------------|-------------------------------------------------------------------------------------------|
| `ls_chemical_search` | Structure search via SMILES. Supports `EXT` (exact/extended) and `SIM` (similarity) modes |

### biology-modality

| Tool                              | Description                                               |
|-----------------------------------|-----------------------------------------------------------|
| `ls_antibody_antigen_search`      | Antibody-antigen relation search with facet filtering     |
| `ls_sequence_search_submit`       | Submit a biological sequence search job (BLAST-style)     |
| `ls_sequence_search_check_status` | Poll the status of a submitted sequence search job        |
| `ls_sequence_search_get_results`  | Retrieve paginated results of a completed sequence search |
| `ls_modification_search_submit`   | Submit a sequence modification site search job            |

> Sequence search in `biology-modality` is asynchronous: submit → check_status → get_results.

---

## Troubleshooting

**Tools not appearing after configuration?**
Restart Claude Code or reload MCP via the `/mcp` command.

**Getting 401 / 403 errors?**
Verify the API key in the `Authorization` header, or contact PatSnap to obtain valid credentials.

**Sequence search stuck in pending?**
Poll `ls_sequence_search_check_status` until the status becomes `success`, then call `ls_sequence_search_get_results`.
