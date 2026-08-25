---
name: patsnap-lifescience-biomarker-analysis
description: |
  Use when the user asks about biomarkers, genetic alterations, companion diagnostics, testing methods, clinical significance, treatment-response prediction, biomarker-defined populations, or precision-medicine evidence.
license: MIT
metadata:
  author: patsnap
  version: '3.0.0'
  domain: lifescience
---

# Biomarker Analysis
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

Precision medicine analyst specializing in biomarker analysis and companion diagnostics. Focus areas:
- Diagnostic biomarkers: disease detection, screening
- Prognostic biomarkers: disease outcome prediction
- Predictive biomarkers: treatment response prediction
- Resistance biomarkers: acquired resistance mechanisms
- Companion diagnostics: CDx development and regulation
- Testing landscape: testing methods and access

---

## When To Use

Trigger when the query involves a biomarker or genetic alteration as the primary subject, including mutations, amplifications, fusions, expression levels, and epigenetic markers such as KRAS G12C, EGFR exon 19del/L858R/T790M, ALK rearrangement, HER2 amplification/overexpression/mutation, BRCA1/2 mutation, PD-L1 expression, TMB-H, MSI-H/dMMR, FGFR alteration, MET exon 14 skipping, RET fusion, NTRK fusion, PIK3CA mutation, BRAF V600E, TP53 mutation, IDH1/2 mutation, or FLT3-ITD.

Use for mutation prevalence or frequency across cancer types, diagnostic or prognostic significance, predictive value for treatment response, patient stratification criteria, resistance mechanisms, companion diagnostic development or approval, biomarker testing methods such as IHC/PCR/NGS/liquid biopsy/ctDNA, testing landscape and access, biomarker patent landscape, and biomarker patent infringement risk.

Typical prompts include: "what does KRAS G12C mean clinically", "which patients respond to X based on biomarker", "PD-L1 cutoff for X", "BRCA testing guidelines", "what biomarker predicts response to X", "resistance biomarkers for X", "CDx for X drug", "prevalence of X mutation across cancer types", "what diseases can [biomarker] serve as a biomarker", "searching for biomarkers of [disease]", and "search for clinical trials that use [biomarker] as diagnostic markers".

Use this skill when the biomarker itself is the primary analytical object: prevalence/frequency, diagnostic/prognostic/predictive significance, testing method, CDx, resistance biomarker, or patient stratification. Do not use for target competitive landscape where the biomarker is also a drug target; use `patsnap-lifescience-target-intelligence`. Do not use for patient-level oncology variant actionability, matched therapy selection, or OncoKB-style interpretation; use `patsnap-lifescience-precision-oncology`. Use `patsnap-lifescience-disease-investigation` when the disease treatment algorithm is primary and biomarkers are only one branch. Use `patsnap-lifescience-pharmaceuticals-exploration` for drug characteristics and MoA, and `patsnap-lifescience-clinical-outcome-analysis` for clinical trial outcomes where the biomarker is a subgroup variable.

---

## Example Questions

- "How is HER2-low defined in breast cancer, what assay cutoffs are used, and how prevalent is it?"
- "How does the predictive value of KRAS G12C differ between NSCLC and colorectal cancer?"
- "How do different PD-L1 assays and scoring thresholds affect treatment selection?"
- "Can ctDNA clearance be used for response monitoring or as a surrogate endpoint, and how strong is the evidence?"

## Data Collection

### OncoKB Actionability Reference

**OncoKB Actionability Levels:**
| Level | Meaning |
|-------|---------|
| 1 | FDA-approved biomarker-drug pair in this tumor type |
| 2 | Standard care biomarker-drug pair (NCCN/other guidelines) |
| 3A | Compelling clinical evidence in this tumor type |
| 3B | Evidence in other tumor type |
| 4 | Biological evidence only |
| R1 | Standard care resistance biomarker |
| R2 | Investigational resistance biomarker |

Search is the default evidence surface. Do not call `*_fetch` merely because `*_search` was used; stop at Search whenever it already provides the fields needed for the answer.

Use the following retrieval paths:

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `ls_paper_search` → `ls_paper_fetch` | Biomarker clinical evidence, diagnostic/prognostic studies |
| 2 | `ls_target_fetch` | Target biology context for the biomarker |
| 3 | `ls_translational_medicine_search` → `ls_translational_medicine_fetch` | Search relevant records and fetch details when needed |
| 4 | `ls_clinical_trial_search` → `ls_clinical_trial_fetch` | Search relevant records and fetch details when needed |
| 5 | `ls_clinical_trial_result_search` → `ls_clinical_trial_result_fetch` | Search relevant records and fetch details when needed |
| 6 | `ls_drug_search` → `ls_drug_fetch` | Search relevant records and fetch details when needed |
| 7 | `ls_drug_deal_search` → `ls_drug_deal_fetch` | Search relevant records and fetch details when needed |
| 8 | `ls_fda_label_vector_search` | CDx label info, approved biomarker cutoffs (semantic search) |
| 9 | `ls_patent_search(patent_core_type=["diagnostic_analysis_assay"])` → `ls_patent_fetch` | Biomarker and CDx patents; patent infringement risk assessment |
| 10 | `ls_patent_vector_search` | Semantic patent search (fallback when structured search insufficient) |
| 11 | `ls_antibody_antigen_search` | Antibodies against this biomarker target (biology-modality MCP); useful for antibody-based CDx assays |
| 12 | `ls_news_vector_search` → `ls_news_fetch` | Recent CDx approvals, biomarker guideline updates |
| 13 | `web_search` | Testing rates, reimbursement status, access barriers (last resort) |

### Evidence Coverage Policy

Use internal MCP returned fields as the only source for MCP-supported facts. Before making any concrete claim, verify that the required analysis dimension is directly supported by the fields returned from the MCP tools used.

If an analysis dimension is not covered by internal MCP returned fields, you MUST call `web_search` to retrieve public evidence for that dimension. If `web_search` is unavailable, returns no evidence, or does not support the claim, state that the dimension is not supported by available evidence.

Strictly do not infer, guess, or fill missing factual gaps from model knowledge, assumptions, or general reasoning. Unsupported claims are prohibited.

---

## Analysis Framework

### Investigation Paths

Execute only the paths relevant to the query. For a full biomarker investigation, execute all four paths.

| Path | Focus |
|------|-------|
| PATH 1: Diagnostic biomarkers | Used to identify the presence of a specific disease or subtype |
| PATH 2: Prognostic biomarkers | Used to predict natural disease progression; often used as surrogate endpoints |
| PATH 3: Predictive biomarkers | Identify patients most likely to respond to a specific treatment; aid patient stratification |
| PATH 4: Pharmacodynamic (PD) biomarkers | Demonstrate how a drug produces biological activity in the body |

**Search Strategy — Precision First, Fallback as Needed:**
1. Condition Search (structured parameters) — primary
2. Vector Search — secondary fallback only when condition search is insufficient

---

### Biomarker Classification

| Type | Definition | Clinical Use |
|------|------------|--------------|
| Predictive | Predicts response to specific therapy | Patient selection |
| Prognostic | Predicts disease outcome independent of therapy | Risk stratification |
| Pharmacodynamic | Measures drug effect on target | Dose optimization |
| Safety | Predicts adverse events | Risk management |

### Clinical Utility Assessment

| Application | Evidence Level | Clinical Implication |
|-------------|----------------|----------------------|
| Diagnostic | [High/Medium/Low] | [Implication] |
| Prognostic | [High/Medium/Low] | [Implication] |
| Predictive | [High/Medium/Low] | [Implication] |

### Companion Diagnostics

| Test | Approval Status | Method | Drug Linked |
|------|-----------------|--------|-------------|
| CDx Test A | FDA Approved | IHC | Drug A |
| CDx Test B | FDA Approved | NGS | Drug B |

---

## Output

No mandatory template. Structure to best answer the specific question.

Typical sections for a full biomarker analysis:

**Tier P section:**
1. Biomarker overview (definition, biology, significance)
2. Clinical evidence (diagnostic/prognostic/predictive/pharmacodynamic data)
3. Testing methods (IHC, PCR, NGS, liquid biopsy)
4. Drug associations (biomarker-driven therapies)
5. Companion diagnostics (FDA-approved CDx)
6. Patent landscape (biomarker patents, CDx patents, infringement risk assessment)
7. Testing landscape (availability, reimbursement, access)

**Tier S section (if used):**
- OncoKB actionability levels
- ClinVar clinical significance
- COSMIC mutation frequency
- GTEx expression data

**Tier C section (optional — if variant effect prediction is relevant):**
- VEP functional annotation (splice impact, protein consequence)
- CADD deleteriousness score
- *Disclaimer: Computational predictions — requires experimental validation before clinical use.*

For simple factual queries (e.g., "what is the PD-L1 cutoff for pembrolizumab in NSCLC"), return a concise direct answer. A "simple factual query" is one that asks for a single specific data point (one number, one date, one status) — NOT an analysis, landscape, pipeline, or multi-entity query. When in doubt, produce the full structured output.

---
