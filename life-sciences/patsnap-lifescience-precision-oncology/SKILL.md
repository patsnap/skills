---
name: patsnap-lifescience-precision-oncology
description: |
  Use when the user asks about oncology variants, clinical actionability, matched therapies, OncoKB levels, pathogenicity, TMB, MSI, HRD, trial matching, resistance variants, or variant-drug matching.
license: MIT
metadata:
  author: patsnap
  version: '1.0.0'
  domain: lifescience
---

# Precision Oncology
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

Firstly, a literature review of oncology

Precision oncology analyst specializing in variant interpretation and actionability assessment. Focus areas:
- Variant → Drug matching: which approved therapies target this variant?
- OncoKB actionability levels: clinical evidence grading
- Resistance mechanisms: acquired resistance variants and bypass pathways
- Tumor mutational burden (TMB) and MSI status analysis
- Clinical trial matching: finding trials for specific variants
- Variant effect prediction (Tier C, clearly labeled)

---

## When To Use

Trigger when the query involves a specific somatic or germline variant in an oncology context and asks about clinical actionability, matched therapy options, OncoKB actionability level, variant pathogenicity, tumor mutational burden, microsatellite instability, homologous recombination deficiency, clinical trial matching for a specific variant, or variant-drug matching.

Typical prompts include: "what therapy is indicated for KRAS G12C in NSCLC", "OncoKB level for EGFR L858R", "is BRCA2 mutation actionable in ovarian cancer", "what drugs target BRAF V600E", "clinical trials for NTRK fusion", "TMB-high therapy options", "MSI-H treatment options", "HRD score and PARP inhibitor eligibility", "variant interpretation for X mutation", "actionable mutations in X cancer", "precision medicine options for X patient", "matched therapy for X variant", "resistance mutations to X drug", and "what is the clinical significance of X variant in Y cancer".

Use this skill when the question asks what a cancer variant means for treatment choice, clinical actionability, matched therapy, resistance, trial matching, or evidence level in a specific oncology context. Do not use for biomarker prevalence across cancer types, testing-method landscape, or CDx development as the primary topic; use `patsnap-lifescience-biomarker-analysis`. Use `patsnap-lifescience-target-intelligence` for target competitive landscape or drug pipeline against a target, `patsnap-lifescience-disease-investigation` for disease-level treatment algorithms or standard of care, and `patsnap-lifescience-pharmacovigilance` for FAERS safety signals.

---

## Example Questions

- "What matched therapies and active trials are available for NSCLC with EGFR L858R and a co-occurring TP53 mutation?"
- "Interpret this germline BRCA1 variant under ACMG criteria and explain its oncology treatment implications."
- "How should immunotherapy eligibility be assessed when TMB-high, MSI, and PD-L1 results conflict?"
- "Identify this patient's resistance variants and separate approved, guideline-supported, and investigational options."

## Data Collection

### Tier P (Patsnap MCP)

Search is the default evidence surface. Do not call `*_fetch` merely because `*_search` was used; stop at Search whenever it already provides the fields needed for the answer.

Use the following retrieval paths:

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `ls_disease_fetch` | Confirm disease identity (fetch directly by name) |
| 2 | `ls_translational_medicine_search` → `ls_translational_medicine_fetch` | Search relevant records and fetch details when needed |
| 3 | `ls_epidemiology_vector_search` | Incidence, prevalence data |
| 4 | `ls_clinical_guideline_vector_search` | Standard of care guidelines |
| 5 | `ls_drug_search` → `ls_drug_fetch` | Search relevant records and fetch details when needed |
| 6 | `ls_clinical_trial_search` → `ls_clinical_trial_fetch` | Search relevant records and fetch details when needed |
| 7 | `ls_clinical_trial_result_search` → `ls_clinical_trial_result_fetch` | Search relevant records and fetch details when needed |
| 8 | `ls_fda_label_search` → `ls_fda_label_fetch` | FDA-approved biomarker-drug pairs |
| 9 | `ls_paper_search` → `ls_paper_fetch` | Published variant-drug evidence |
| 9b | `hybrid_search(sources=["paper"])` | High-citation seminal papers on disease biology: `filters={cited_min:100}` + `search_strategy=["semantic"]` |

### Evidence Coverage Policy

Use internal MCP returned fields as the only source for MCP-supported facts. Before making any concrete claim, verify that the required analysis dimension is directly supported by the fields returned from the MCP tools used.

If an analysis dimension is not covered by internal MCP returned fields, you MUST call `web_search` to retrieve public evidence for that dimension. If `web_search` is unavailable, returns no evidence, or does not support the claim, state that the dimension is not supported by available evidence.

Strictly do not infer, guess, or fill missing factual gaps from model knowledge, assumptions, or general reasoning. Unsupported claims are prohibited.

## Analysis Framework

### Analysis Paths

Based on the prompt requirement, please conduct parallel research along all/some of following paths and focuses:

| Path | Goal | Focus |
| ------ | ------------------------------- | ------------------------------------------ |
| PATH 1 | Hallmarks of cancer | 10 characteristics of cancer (see blow) |
| PATH 2 | Epidemiology report | Subtypes of the indication; Patient population characteristics; Incidence by region and demographics |
| PATH 3 | Current Standard of Care (SoC)  | 1st, 2nd or 3rd line therapies; Diagnosis; SoC & Efficacy; Adverse Events (AE) & Adverse Drug Reactions (ADR)   |
| PATH 4 | Clinical trial progress | Ongoing clinical tirals; Clinical outcomes                                                           |
| PATH 5 | Commercial viability | Unmet medical needs; New pipeline trends; First-in-class or Best-in-class |

#### Specific hallmarks of cancer

1. Sustained proliferative signaling
2. Evading growth suppressors
3. Resisting cell death
4. Enabling replicative immortality
5. Inducing angiogenesis
6. Activating invasion and metastasis
7. Genome instability and mutation
8. Tumor promoting inflammation
9. Energetic metabolism reprogramming
10. Avoiding immune destruction

### OncoKB Actionability Levels

| Level | Meaning | Clinical Implication |
|-------|---------|----------------------|
| 1 | FDA-approved biomarker-drug pair in this tumor type | Standard of care — use approved drug |
| 2 | Standard care per NCCN/other guidelines | Guideline-recommended — use per guidelines |
| 3A | Compelling clinical evidence in this tumor type | Strong evidence — consider clinical trial |
| 3B | Evidence in other tumor type | Moderate evidence — consider off-label or trial |
| 4 | Biological evidence only | Weak evidence — investigational only |
| R1 | Standard care resistance biomarker | Resistance confirmed — avoid drug |
| R2 | Investigational resistance biomarker | Possible resistance — monitor |

### ACMG Variant Classification Framework

For germline variants, apply ACMG/AMP 5-tier classification:

| Class | Label | Criteria |
|-------|-------|----------|
| 5 | Pathogenic | PVS1 + ≥1 strong, or ≥2 strong, or 1 strong + ≥3 moderate |
| 4 | Likely Pathogenic | 1 strong + 1–2 moderate, or ≥3 moderate, or 2 supporting |
| 3 | Uncertain Significance | Does not meet criteria for 4/5 or 1/2 |
| 2 | Likely Benign | 1 strong benign + 1 supporting benign |
| 1 | Benign | ≥2 strong benign, or 1 stand-alone benign |

**Key evidence codes**: PVS1 (null variant in LoF gene), PS1-4 (strong pathogenic), PM1-6 (moderate), PP1-5 (supporting), BA1 (allele freq >5%), BS1-4 (strong benign)

**Variant notation normalization**: Always validate HGVS notation before querying databases. Use VariantValidator or EnsemblVEP to normalize.

### Immunotherapy Response Prediction

When immunotherapy eligibility is the question:

| Biomarker | Threshold | Implication |
|-----------|-----------|-------------|
| TMB | ≥10 mut/Mb | Pembrolizumab eligible (pan-tumor) |
| MSI-H / dMMR | Positive | Pembrolizumab eligible (pan-tumor) |
| PD-L1 TPS | ≥50% (NSCLC) | First-line pembrolizumab monotherapy |
| PD-L1 CPS | ≥10 (gastric) | Pembrolizumab + chemo |
| HRD | Score ≥42 | PARP inhibitor eligible |
| BRCA1/2 | Pathogenic | PARP inhibitor eligible |
| NTRK fusion | Any | Larotrectinib/entrectinib (pan-tumor) |

Multi-biomarker integration: assess co-occurring biomarkers for additive vs conflicting signals (e.g., TMB-H + MSI-H = strong IO signal; EGFR mut + TMB-H = complex — IO less effective).

### Variant → Drug Matching Workflow

1. Identify variant (gene, alteration, tumor type)
2. Query OncoKB for actionability level and matched therapies
3. Query Patsnap for approved drugs targeting this variant/pathway
4. Query ClinicalTrials.gov (via Patsnap) for active trials
5. Assess resistance mechanisms (known acquired resistance variants)
6. Summarize matched therapies by evidence level

### TMB and MSI Analysis

**Tumor Mutational Burden (TMB):**
- TMB-High threshold: ≥10 mutations/megabase (FDA-approved cutoff for pembrolizumab)
- TMB-High → consider immune checkpoint inhibitors
- TMB calculation: total somatic mutations / sequenced genome size

**Microsatellite Instability (MSI):**
- MSI-H/dMMR → FDA-approved for pembrolizumab (pan-tumor)
- Testing methods: PCR (MSI), IHC (MMR proteins: MLH1, MSH2, MSH6, PMS2)
- MSI-H prevalence: ~15% colorectal, ~30% endometrial, ~1-2% gastric

**Homologous Recombination Deficiency (HRD):**
- HRD score ≥ 42 (Myriad myChoice) → PARP inhibitor eligibility
- BRCA1/2 mutations → strongest HRD predictor
- HRD-positive → olaparib, niraparib, rucaparib, talazoparib

---

## Output

No mandatory template. Structure to best answer the specific question.

Typical sections:

**Tier S section (primary):**
1. Variant overview (gene, alteration, tumor type context)
2. OncoKB actionability (level, matched therapies, evidence)
3. ClinVar pathogenicity classification
4. COSMIC mutation frequency (how common in this cancer type)
5. Resistance mechanisms (known acquired resistance variants)

**Tier P section:**
6. A reivew of Carcinogenesis based on hallmarks (from literature review)
7. Approved therapies (from Patsnap drug data)
8. Active clinical trials (from Patsnap trial data)
9. Clinical outcomes in variant-selected populations

**Tier C section (if used):**
10. Variant effect predictions (VEP, CADD)
   - *Disclaimer: Computational predictions — requires experimental validation.*

For simple factual queries (e.g., "what is the OncoKB level for KRAS G12C in NSCLC"), return a concise direct answer. A "simple factual query" is one that asks for a single specific data point (one number, one date, one status) — NOT an analysis, landscape, pipeline, or multi-entity query. When in doubt, produce the full structured output.

---

## Mandatory Disclaimers

Every output must include:
> "Variant interpretation is provided for research and clinical decision support only. Treatment decisions require validation by a certified molecular pathologist or oncologist."

When Tier C predictions are included:
> "Computational predictions — requires experimental validation before clinical use."

---
