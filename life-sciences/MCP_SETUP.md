# Patsnap LifeScience MCP Setup Guide

Configure the Patsnap MCP services listed in your skill's dependencies. The 32 Life Sciences skills in this directory use `pharma-intelligence`.

---

## Services Overview

| MCP Service           | Purpose                                                                       | Tool Prefix                                        |
|-----------------------|-------------------------------------------------------------------------------|----------------------------------------------------|
| `pharma-intelligence` | Drug, target, disease, patent, literature, clinical trial intelligence        | `ls_`                                              |
| `chemical-molecular`  | Chemical structure search (similarity / exact match)                          | `ls_chemical_`                                     |
| `biology-modality`    | Antibody-antigen relations, biological sequence search, modification analysis | `ls_antibody_`, `ls_sequence_`, `ls_modification_` |

---

## Get Your Connection URLs

Each service has a unique connection URL tied to your API key. Visit the Patsnap Marketplace to get them:

- [Pharma Intelligence](https://open.patsnap.com/marketplace/mcp-servers/245f3ce8-79e4-4c2a-927c-e155c293f097)
- [Chemical Molecular](https://open.patsnap.com/marketplace/mcp-servers/96b4a650-d563-4fc5-860d-c99ee8cb5b1e)
- [Biology Modality](https://open.patsnap.com/marketplace/mcp-servers/a96c9b0b-2831-4d18-a37d-286896979b8d)

Each page shows a ready-to-copy connection URL. Sign in and replace `yourapikey` with your actual API key.

---

## Configuration

### Option 1. Claude Code CLI

Run the command for each service your skill requires. These examples register the servers for your user account across projects. Use the connection URL from the corresponding Marketplace page.

```bash
claude mcp add --transport http --scope user pharma_intelligence \
  "https://connect.patsnap.com/096456/logic-mcp?apikey=<YOUR_API_KEY>"

claude mcp add --transport http --scope user chemical_molecular \
  "https://connect.patsnap.com/713886/logic-mcp?apikey=<YOUR_API_KEY>"

claude mcp add --transport http --scope user biology_modality \
  "https://connect.patsnap.com/06e741/logic-mcp?apikey=<YOUR_API_KEY>"
```

### Option 2. Project-level configuration

Add the required servers to `.mcp.json` in your project root. Set the corresponding API key environment variables before starting Claude Code.

```json
{
  "mcpServers": {
    "pharma_intelligence": {
      "type": "http",
      "url": "https://connect.patsnap.com/096456/logic-mcp?apikey=${PATSNAP_PHARMA_API_KEY}"
    },
    "chemical_molecular": {
      "type": "http",
      "url": "https://connect.patsnap.com/713886/logic-mcp?apikey=${PATSNAP_CHEMICAL_API_KEY}"
    },
    "biology_modality": {
      "type": "http",
      "url": "https://connect.patsnap.com/06e741/logic-mcp?apikey=${PATSNAP_BIOLOGY_API_KEY}"
    }
  }
}
```

See the [Claude Code MCP documentation](https://code.claude.com/docs/en/mcp) for configuration scopes and environment variable expansion.

---

## Verify the Setup

Run `/mcp` in Claude Code and confirm each required service shows `connected`.

You can also test with a quick query:

```
Search for PD-1 related drugs
```

If `ls_entity_search(entity_type="drug")` returns results, drug search is available. For the Drug Development Pathway skill, open the connected `pharma_intelligence` server in `/mcp` and check for `ls_drug_milestone_fetch` if the client shows tool names. If it shows only a tool count, use the ID returned by drug search to test `ls_drug_milestone_fetch(drug_id=<drug_id>, offset=0, limit=10)` and check the actual tool response. If the tool is unavailable, check the configured server URL and whether the current connection exposes it before treating the timeline as empty. [Claude Code MCP tool availability](https://code.claude.com/docs/en/mcp#tool-availability)

---

## Tool Reference

### pharma-intelligence

| Tool                                                                   | Description                        |
|------------------------------------------------------------------------|------------------------------------|
| `ls_entity_search(entity_type="drug")` / `ls_entity_fetch(entity_type="drug")`                                     | Search and retrieve drug details   |
| `ls_drug_milestone_fetch` | Retrieve development milestones such as IND filings, phase transitions, and approvals. Use `offset` and `limit` to page through results. |
| `ls_entity_fetch(entity_type="target")`                                                      | Retrieve target details            |
| `ls_entity_fetch(entity_type="disease")`                                                     | Retrieve disease details           |
| `ls_patent_search` / `ls_patent_fetch`                          | Structured, keyword, and semantic patent search |
| `ls_paper_search` / `ls_paper_vector_search` / `ls_paper_fetch`        | Literature search                  |
| `ls_evidence_by_entity_search(evidence_type="clinical_trial")` / `ls_evidence_fetch(evidence_type="clinical_trial")`                 | Clinical trial search              |
| `ls_evidence_by_entity_search(evidence_type="clinical_trial_result")` / `ls_evidence_fetch(evidence_type="clinical_trial_result")`   | Clinical trial results             |
| `ls_evidence_by_entity_search(evidence_type="drug_deal")` / `ls_evidence_fetch(evidence_type="drug_deal")`                           | Drug licensing and deal search     |
| `ls_entity_fetch(entity_type="organization")`                                                | Organization / company details     |
| `ls_evidence_by_entity_search(evidence_type="news")` / `ls_evidence_fetch(evidence_type="news")`                              | Industry news                      |
| `ls_evidence_by_entity_search(evidence_type="translational_medicine")` / `ls_evidence_fetch(evidence_type="translational_medicine")` | Translational medicine             |
| `ls_evidence_by_semantic_search(source="fda_label")`                                           | FDA drug labels                    |
| `ls_evidence_by_semantic_search(source="clinical_guideline")`                                  | Clinical guidelines                |
| `ls_evidence_by_semantic_search(source="epidemiology")`                                        | Epidemiology data                  |
| `ls_evidence_by_semantic_search(source="financial_report")`                                    | Financial reports and prospectuses |
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
Verify the API key in the connection URL, or contact Patsnap to obtain valid credentials.

**Sequence search stuck in pending?**
Poll `ls_sequence_search_check_status` until the status becomes `success`, then call `ls_sequence_search_get_results`.
