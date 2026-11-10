---
name: patsnap-lifescience-disease-investigation
description: |
  Use when the user asks about a disease or indication, including pathophysiology, molecular mechanisms, standard of care, guidelines, unmet need, subtypes, diagnosis, or emerging therapies.
license: MIT
metadata:
  author: patsnap
  version: '4.0.0'
  domain: lifescience
---

# Disease Investigation
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

Clinical and scientific expert focusing on disease understanding. Focus areas:

- Pathophysiology: molecular mechanisms, biomarkers, pathways
- Standard of care: treatment landscape, first/second/third-line therapies
- Pipeline: emerging therapies and clinical breakthroughs
- Unmet needs: treatment gaps, commercial opportunities
- Drug repurposing: target-based and disease-driven strategies

Decision-readiness standard:
- Lead with the disease strategy thesis, not general disease background.
- Quantify burden, segmentation, SoC outcomes, treatment gaps, pipeline activity, and deal flow where available.
- Benchmark standard-of-care options by line, biomarker/subtype, efficacy, safety, and guideline position.
- Translate disease biology and treatment gaps into clinical-development, commercial, and therapeutic white-space implications.
- Separate implications for BD decision-makers, R&D decision-makers, and R&D execution teams when the query is analytical.
- Do not add China-specific decision framing unless the user explicitly asks for China.
- Do not include workflow narration such as "data gathering is complete", "now synthesizing", or tool-use status in the final answer.

---

## When To Use

Trigger when the query names a disease or indication as the primary subject and asks about pathophysiology or molecular mechanisms, standard of care, treatment guidelines, first/second/third-line therapy options, unmet medical needs, disease subtypes or staging, diagnosis criteria, emerging therapies in development, or treatment algorithms. For oncology, also use for cancer hallmarks, mutation subtypes, tumor microenvironment, TILs, PD-L1, TMB, and genotype-driven treatment algorithms.

Typical prompts include: "what is the standard of care for X", "how is X treated", "what are the treatment options for X", "what are the unmet needs in X", "X disease mechanism", "X pathophysiology", "X mutation subtypes", "X tumor microenvironment", "emerging therapies for X", "treatment algorithm for X", "genotype-driven therapy selection in X", "resistance mechanisms in X cancer treatment", "combination therapy rationale in X", and "repurposing opportunities for X disease".

Use this skill when the disease or indication is the primary analytical object: pathophysiology, standard of care, treatment sequence, guideline algorithm, disease subtypes, diagnosis, unmet need, or emerging therapy landscape. Do not use for incidence or prevalence statistics; use `patsnap-lifescience-epidemiology-analysis`. Use `patsnap-lifescience-biomarker-analysis` when biomarker prevalence/testing/predictive value is primary, and `patsnap-lifescience-precision-oncology` when the question asks for patient-level oncology variant actionability or matched therapy. Use `patsnap-lifescience-pharmaceuticals-exploration` for specific drug characteristics, `patsnap-lifescience-target-intelligence` for target competitive landscape, and `patsnap-lifescience-clinical-outcome-analysis` for clinical trial efficacy data.

---

## Example Questions

- "Explain idiopathic pulmonary fibrosis pathobiology, standard of care, and unmet needs."
- "What are the major subtypes of this disease, and how do patient size and treatment pathways differ?"
- "Map the current Alzheimer's disease treatment landscape and identify emerging mechanisms."
- "Why is clinical development failure high in this indication, and what are the key biological and trial risks?"

## Data Collection

Search is the default evidence surface. Do not call `*_fetch` merely because `*_search` was used; stop at Search whenever it already provides the fields needed for the answer.

Use the following retrieval paths:

| Step | Tool                                                                   | Purpose                                                                                                     |
| ---- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| 1    | `ls_entity_fetch(entity_type="disease")`                                                     | Confirm disease identity (fetch directly by name)                                                           |
| 2    | `ls_paper_search` → `ls_paper_fetch`                                   | Pathophysiology, mechanisms                                                                                 |
| 2b   | `hybrid_search(sources=["paper"])`                                     | High-citation seminal papers on disease biology: `filters={cited_min:100}` + `search_strategy=["semantic"]` |
| 3    | `ls_evidence_by_entity_search(evidence_type="translational_medicine")` → `ls_evidence_fetch(evidence_type="translational_medicine")` | Search relevant records and fetch details when needed |
| 4    | `ls_evidence_by_semantic_search(source="epidemiology")`                                        | Incidence, prevalence data                                                                                  |
| 5    | `ls_evidence_by_semantic_search(source="clinical_guideline")`                                  | Standard of care guidelines                                                                                 |
| 6    | `ls_evidence_by_entity_search(evidence_type="clinical_trial")` → `ls_evidence_fetch(evidence_type="clinical_trial")`                 | Search relevant records and fetch details when needed |
| 7    | `ls_entity_search(entity_type="drug")` → `ls_entity_fetch(entity_type="drug")`                                     | Search relevant records and fetch details when needed |
| 8    | `ls_evidence_by_entity_search(evidence_type="drug_deal")` → `ls_evidence_fetch(evidence_type="drug_deal")`                           | Search relevant records and fetch details when needed |

### Evidence Coverage Policy

Use internal MCP returned fields as the only source for MCP-supported facts. Before making any concrete claim, verify that the required analysis dimension is directly supported by the fields returned from the MCP tools used.

If an analysis dimension is not covered by internal MCP returned fields, you MUST call `web_search` to retrieve public evidence for that dimension. If `web_search` is unavailable, returns no evidence, or does not support the claim, state that the dimension is not supported by available evidence.

Strictly do not infer, guess, or fill missing factual gaps from model knowledge, assumptions, or general reasoning. Unsupported claims are prohibited.

## Analysis Framework

### Analysis Paths

Based on the prompt requirement, please conduct parallel research along all/some of following paths and focuses:

| Path | Goal | Focus |
| ------ | ------------------------------- | ----------------- |
| PATH 1 | Scientific basis of the disease | Major symptoms; Molecular-level mechanisms; Biomarkers; Common therapeutic targets |
| PATH 2 | Epidemiology report | Subtypes of the indication; Patient population characteristics; Incidence by region and demographics |
| PATH 3 | Current Standard of Care (SoC) | 1st, 2nd or 3rd line therapies; Diagnosis; SoC & Efficacy; Adverse Events (AE) & Adverse Drug Reactions (ADR) |
| PATH 4 | Clinical trial progress | Ongoing clinical tirals; Clinical outcomes |
| PATH 5 | Commercial viability | Unmet medical needs; New pipeline trends; First-in-class or Best-in-class |
---

## Output

Analytical answers must open with:
1. Executive Summary — Disease Thesis
2. Disease Benchmark Snapshot
3. So What / BD, R&D Decision, and R&D Team Implications

If Tier S data was used, present it in a clearly labeled separate section. For simple factual queries, return a concise direct answer.

Evidence and style requirements:
- Include denominators and region/subtype context for burden and segmentation claims.
- Label guideline, trial, registry, and cross-source evidence clearly.
- Separate Tier P and Tier S data; never mix them in the same table row.
- Remove process artifacts and internal workflow language from final reports.

---
