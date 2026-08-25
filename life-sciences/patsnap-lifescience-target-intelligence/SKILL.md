---
name: patsnap-lifescience-target-intelligence
description: |
  Use when the user asks about a biomedical target as the primary subject, including biology, druggability, indication fit, modality options, competitive pipeline, clinical progress, deals, or white-space opportunities.
license: MIT
metadata:
  author: patsnap
  version: '1.0.0'
  domain: lifescience
---

# Target Intelligence
## SaaS Context and MCP Enrichment Policy

This skill supports two peer workflows: global database search and SaaS-anchored analysis.

When no SaaS context is provided, use the normal global workflow for this skill: normalize entities, search the relevant full database sources, fetch details when needed, and synthesize the answer from the best available evidence.

When SaaS context is provided, treat the SaaS search result, filters, selected records, and visible fields as the primary analysis anchor. The SaaS context defines the main entities and user-visible scope, but it is not a hard ban on additional evidence. Use MCP tools to enrich missing fields, fetch details for records inside the SaaS result set, and retrieve supporting evidence that is required to answer the user's question.

Use global MCP search in SaaS context when the question requires comparison, market-wide context, missing clinical/regulatory/patent/deal/literature evidence, or explicit expansion beyond the current result set. Do not silently merge out-of-scope records into the SaaS result set. Clearly label evidence as one of:

- Current SaaS results
- MCP enrichment for current SaaS records
- Broader or out-of-scope MCP supplement

If SaaS-provided data is incomplete, state what is missing and explain which MCP tools or sources were used to supplement it. If the answer relies on out-of-scope evidence, make that boundary explicit.

### SaaS Tool-Use Priority

1. First inspect SaaS-provided records, filters, selected IDs, available fields, missing fields, and result counts.
2. If the question can be answered from SaaS data, answer from SaaS data and state the active scope.
3. If required fields are missing, use MCP fetch/search tools to enrich the entities already present in the SaaS result set.
4. If the question requires broader context, use MCP search as supplemental evidence and label it as broader/global context.
5. Keep SaaS-filtered records separate from MCP-discovered records in the final answer.

**Zone 1 — Tier P only.** All data from Patsnap MCP tools exclusively.

## Role

Decision-readiness standard:
- Lead with the target thesis, not biological background.
- Quantify target maturity with approved assets, late-stage assets, modality mix, clinical evidence, deal activity, and geography where available.
- Benchmark assets by modality, clinical evidence, safety, dosing, regulatory status, and company position.
- Translate biology and pipeline facts into development, BD, competitive, or white-space implications.
- Separate implications for BD decision-makers, R&D decision-makers, and R&D execution teams when the query is analytical.
- Do not add China-specific decision framing unless the user explicitly asks for China.
- Do not include workflow narration such as "data gathering is complete", "now synthesizing", or tool-use status in the final answer.

---

## Example Questions

- "Assess Lp(a) target biology, genetic validation, druggability, and the competitive pipeline."
- "Which companies are developing KRAS G12D-targeted drugs, and how do their modalities differ?"
- "Compare inhibition, degradation, and antibody strategies against the same target."
- "Is there still a first-in-class or best-in-class opportunity for this target, and where is the white space?"

## Data Collection

Search is the default evidence surface. Do not call `*_fetch` merely because `*_search` was used; stop at Search whenever it already provides the fields needed for the answer.

Use the following retrieval paths:

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `ls_target_fetch` | Target biological details, database IDs (KEGG, UniProt, NCBI Gene, RefSeq, UMLS CUI) |
| 2 | `ls_paper_search` → `ls_paper_fetch` | Drug development history, review literature |
| 3 | `ls_translational_medicine_search` → `ls_translational_medicine_fetch` | Search relevant records and fetch details when needed |
| 4 | `ls_drug_search` → `ls_drug_fetch` | Search relevant records and fetch details when needed |
| 5 | `ls_drug_deal_search` → `ls_drug_deal_fetch` | Search relevant records and fetch details when needed |
| 6 | `ls_clinical_trial_search` → `ls_clinical_trial_fetch` | Search relevant records and fetch details when needed |
| 7 | `ls_clinical_trial_result_search` → `ls_clinical_trial_result_fetch` | Search relevant records and fetch details when needed |
| 8 | `ls_news_vector_search` → `ls_news_fetch` | Recent target news |
| 9 | `ls_antibody_antigen_search` | Antibody-antigen relations (if antibody query) |
| 10 | `web_search` | Last resort after all MCP retrievals complete |

Execute only the steps relevant to the query. Stop when data is sufficient.

### Evidence Coverage Policy

Use internal MCP returned fields as the only source for MCP-supported facts. Before making any concrete claim, verify that the required analysis dimension is directly supported by the fields returned from the MCP tools used.

If an analysis dimension is not covered by internal MCP returned fields, you MUST call `web_search` to retrieve public evidence for that dimension. If `web_search` is unavailable, returns no evidence, or does not support the claim, state that the dimension is not supported by available evidence.

Strictly do not infer, guess, or fill missing factual gaps from model knowledge, assumptions, or general reasoning. Unsupported claims are prohibited.

---

## Analysis Framework

### Investigation Paths

Based on the prompt requirement, please conduct parallel research along all/some of following paths and focuses:

| Path | Goal | Focus |
|------|-------|----------------|
| PATH 1 | Target biological details  | Database IDs, Structure, Pathway, Function |
| PATH 2 | Drug development history | Approved drugs, Pior generations, First-in-class, Best-in-class |
| PATH 3 | Current pipeline drug list | The R&D drugs for the target |
| PATH 4 | Clinical trial progress | Trial arm-level results: experimental vs. comparator arm, patient population (N), primary endpoint result, key secondary endpoints, failed/discontinued reasons |
| PATH 5 | Competitive landscape | Chances for first-in-class or best-in-class |

**Path Selection by Query Type**:

| User Question Type | Paths to Execute |
|-------------------|-----------------|
| Basic target info only | PATH 1 |
| Drug development history | PATH 1 + PATH 2 |
| Current pipeline drug list | PATH 1 + PATH 3 |
| Clinical trial progress | PATH 3 + PATH 4 |
| Competitive landscape / market analysis | PATH 3 + PATH 5 |
| Full target intelligence report | All PATH 1–5 |

### Search Strategy

**Precision First, Fallback as Needed:**
1. Condition Search (structured parameters) — primary
2. Vector Search — secondary fallback only when condition search is insufficient

Never start with vector search.

### Competitive Landscape (PATH 5)

Filter competitive analysis candidates:
- Approved drugs: include all
- Non-approved drugs: include only those with new clinical progress in the past five years

**Tier Classification** — classify every included drug before the deep-dive:
- Tier 1: Approved + cardiovascular/clinical outcomes data
- Tier 2: Approved or Phase 3 positive, no outcomes data yet
- Tier 3: Early stage or differentiated modality bet

Lead each player deep-dive with: `[Tier] | [Modality] | [Geography]`

**Modality Differentiation Matrix** — group drugs by modality and output a comparison table:

| Drug | Company | Modality | Dosing | Key Trial | Primary Endpoint Result | Outcomes Data | Status |
|------|---------|---------|--------|-----------|------------------------|---------------|--------|

**Geographic Segmentation** — only add region-specific analysis when the user asks for a region. Otherwise use a global/US-EU decision frame and avoid China-specific sections.

For each included drug: indication, target, drug type, MoA, developer, clinical performance, failed/discontinued trial reasons.

**Target Thesis Requirements**:
- Identify the top 3 best-positioned assets/companies and top 3 risks.
- Distinguish validated biology from pipeline optionality.
- Label clinical comparisons as head-to-head, cross-trial, label-based, or NMA.

---

## Output

Analytical answers must open with:
1. Executive Summary — Target Thesis
2. Target Benchmark Snapshot
3. So What / BD, R&D Decision, and R&D Team Implications

For simple factual target queries, return a concise direct answer. Include source-linked evidence where available and remove process artifacts from final reports.

---
