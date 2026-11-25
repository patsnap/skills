---
copyright: "Copyright © Patsnap. All rights reserved."
name: patsnap-lifescience-precision-oncology
description: Use when the user asks about oncology variants, clinical actionability,
  matched therapies, OncoKB levels, pathogenicity, TMB, MSI, HRD, trial matching,
  resistance variants, or variant-drug matching.
license: MIT
metadata:
  author: Patsnap
  version: 1.0.0
  category: "Life Science"
---

# Precision Oncology
**Zone 1 — Tier P only.** Prioritize Patsnap MCP evidence; when key fields are missing or conflicting, verify official primary sources under the rules below.

## Writing and Output Style

Write as an analytical memo for business, BD, R&D or medical colleagues: lead with the conclusion, then evidence and reasoning. Retain necessary technical terms, drug names, endpoints and database names, while avoiding awkward word-for-word translation.

- Use concise sentences and clear judgments; avoid empty stock phrases.
- Anchor each key judgment in data, sources, applicable populations, comparators or time windows.
- Do not narrate internal work or tool status, such as "retrieval is complete" or "now analyzing."

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

This skill requires the Patsnap `pharma-intelligence` MCP service. See the [MCP setup guide](https://github.com/patsnap/skills/blob/main/life-sciences/MCP_SETUP.md) for connection and verification steps.

### Tier P (Background — Patsnap MCP)

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `ls_entity_fetch(entity_type="disease")` | Confirm disease identity by direct name-based retrieval |
| 2 | `ls_evidence_by_entity_search(evidence_type="translational_medicine")` → `ls_evidence_fetch(evidence_type="translational_medicine")` | Retrieve relevant records and fetch details when needed |
| 3 | `ls_evidence_by_semantic_search(source="epidemiology")` | Incidence and prevalence data |
| 4 | `ls_evidence_by_semantic_search(source="clinical_guideline")` | Standard-of-care guidelines |
| 5 | `ls_entity_search(entity_type="drug")` → `ls_entity_fetch(entity_type="drug")` | Retrieve relevant records and fetch details when needed |
| 6 | `ls_evidence_by_entity_search(evidence_type="clinical_trial")` → `ls_evidence_fetch(evidence_type="clinical_trial")` | Retrieve relevant records and fetch details when needed |
| 7 | `ls_evidence_by_entity_search(evidence_type="clinical_trial_result")` → `ls_evidence_fetch(evidence_type="clinical_trial_result")` | Retrieve relevant records and fetch details when needed |
| 8 | `ls_evidence_by_semantic_search(source="fda_label", query="Approved labeling for the drug and biomarker", lang="EN")` | FDA-approved biomarker–drug pairs |
| 9 | `ls_paper_search` → `ls_paper_fetch` | Published variant–drug evidence |

Search is the default evidence-gathering method. Do not call `*_fetch` merely because `*_search` was called. Further detail retrieval is unnecessary only when the results have passed entity and scope checks, contain the fields required to answer the question, and have no unresolved material conflicts.

### Evidence Coverage and Conclusion Verification

- Support specific facts with retrieved record fields, retaining source identifiers, applicable regions and record dates. For approval status, clinical endpoints and contractual terms that affect the conclusion, prioritize the relevant official decision, registry or original results, contract or original announcement. When structured results have missing key fields, conflicts, zero hits or unresolved entity identity, use `ls_web_search` from the MCP contract to verify official primary sources without waiting for all structured searches to finish. Build queries from the entity name, reliable identifiers, fact to verify, region and period. Prioritize regulators, trial registries, company announcements, exchange filings and patent authorities. Check whether the returned content directly supports the fact and retain its link, date and scope. Do not infer missing fields from merely relevant titles or abstracts. Mark evidence insufficient only after verification still fails, and limit the affected conclusions accordingly. If `ls_web_search` is unavailable or fails, state that verification is blocked; do not substitute tools outside the contract and present them as completion of this verification step.
- Inspect both call status and error, warnings and items in the response. Distinguish parameter, authentication and service errors from explicit no-match messages by their meaning, not merely the presence of an error field. If unclear, retain the original message and mark it unresolved. A total=0 attached to an error is not a valid zero-hit result; even a valid zero-hit result does not prove that the fact does not exist. Record rejected parameters, service failures, valid zero-hit queries and unexecuted queries separately. Retain status codes as returned unless a code table confirms their meaning.
- If one identifier blocks a batch query, retain successful records and isolate the failed items using the current schema. If a plausibly formatted identifier is rejected, check the official registry through `ls_web_search`; do not infer nonexistence. Do not repeatedly retry the same failure. After one correction or split still fails, verify primary sources through `ls_web_search` or mark the task blocked.
- Semantic search produces candidates only. Before accepting evidence, verify the name or alias mapping, registry/protocol number, relevant entity and relevance of the original text. Nonempty results, similar titles and ranking do not prove a match. Do not replace an unresolved entity with a similar one or attribute candidate records to the original name. Track coverage separately for pipeline, results, transactions and other evidence branches; an unqueried branch cannot be described as having no records.
- Retain each conflicting record with its own date, version and scope, and determine whether the records concern different populations, regions or events. Leave unexplained differences unresolved rather than inventing causes. Explicitly label model-based inferences and scenario assumptions and give their basis.
- Before reporting totals or rankings, check query scope, pagination, the deduplication unit and exclusion criteria. If only part of the records was retrieved, describe the sample scope instead of treating it as the full population. Respect the requested item limit, cutoff date and comparison scope.
- Map requested conclusions to retrieved evidence. When missing fields affect a conclusion, first retrieve the relevant details; if gaps or conflicts remain, verify primary sources using `ls_web_search`. If still unavailable, state the gap and affected judgment. A maximum number of items is a ceiling, not a quota to fill with irrelevant records. A few reliable examples neither establish complete coverage nor replace a requested comprehensive review.
- Before delivery, check the summary, tables, body and revised text against the evidence mapping. Status, monetary units, region, population and certainty must agree for the same fact. Place material qualifications beside the relevant value or judgment, not only in a closing disclaimer. After correcting a fact, recheck dependent comparisons, totals and recommendations; do not overwrite verified content without a source. Normalize monetary amounts to one currency and base unit before display conversion, checking million, billion, ten-thousand, hundred-million and ratio conversions. Do not add incompatible denominators, periods or analysis versions to force a total. Keep complete, locatable citation identifiers without truncation.

- Maintain a concise evidence mapping for decision-relevant facts: conclusion, entity, scope, value and unit, document date, complete source identifier and original-text location. Record what the task needs without exposing internal verification narration. A search-generated answer is not the original source. Verification requires locatable original content that directly supports the conclusion. A working link, successful call or a returned claim of verification is insufficient. If the original cannot be obtained, retain an unresolved status; do not invent page numbers, quotations or record identifiers.
- When updating an analysis, revisit previously located primary sources and check revisions, subsequent announcements and report notes available by the question cutoff. The old answer itself is not evidence. Do not discard still-applicable primary evidence merely because the current search missed it; explicitly replace outdated evidence. Do not upgrade an unresolved conclusion to certainty unless new evidence directly supports it.
- Distinguish "not obtained in this search," "not stated in the documents reviewed" and "explicitly undisclosed." Before denying disclosure or claiming only, first or all, check the required sources and search coverage; otherwise restrict the claim to the material obtained. Multiple entry points may share a parser or underlying source. Their count is not independent corroboration, and identical errors do not rule out a system issue.

### Business Judgment Rules

- Update decision-relevant results and milestones before ranking development directions. Do not treat results disclosed before the cutoff as future triggers. Success of a direction does not establish efficacy of a proposed asset; positive competing regimens do not prove that the direction has no opportunity. Give conditional priorities based on the company's existing assets, stage, technical/manufacturing capabilities, resources and regional pathways. If the starting point is unknown, give scenarios rather than promising a fixed development duration.
- Biomarker conditions such as high expression and amplification may overlap. Preserve the protocol testing methods, thresholds and AND/OR relationships rather than rewriting them as mutually exclusive categories. Exclusive groups and their intersection each require supporting data; different names alone do not establish differentiated patient pools.
- Before comparing resistance strategies, align prior therapy, resistance testing and study population. First-line, adjuvant or other-tumor results for an asset do not replace evidence in the target resistant population. If efficacy or safety gaps affect priority, retrieve the relevant results before giving conditional research recommendations.
- Define region, period, disease stage, treatment line, testing method and population denominator before using percentages. The proportion randomized among screened trial participants describes trial selection only, not biomarker prevalence or the treatable share of the disease population.
- For populations defined by multiple conditions, preserve testing methods, thresholds and AND/OR relationships and account for intersections. Do not multiply marginal rates from different studies under an unverified independence assumption or add overlapping subgroups directly.
- In patient-pool or market estimates, identify the source, conditional probability and assumption for each component. Without representative testing or epidemiological evidence, provide ranges or unresolved conditions rather than inventing a definite patient count.
- Match variant significance and therapy selection to tumor type, variant, test method, treatment line, region and evidence version. Without co-mutation or specific subgroup results, do not turn mechanistic speculation into definite efficacy or lack of efficacy.
- Thresholds and drug examples in this skill are search leads only. Verify treatment eligibility against the current applicable label and population criteria rather than inferring it from one positive marker.

---

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

For germline variants in Mendelian disease, use the evidence combinations in [ACMG/AMP Table 5](https://www.nature.com/articles/gim201530). Apply relevant gene- or disease-specific specifications when available.

| Class | Label | Criteria |
|-------|-------|----------|
| 5 | Pathogenic | PVS1 + (≥1 strong, ≥2 moderate, 1 moderate + 1 supporting, or ≥2 supporting)<br>or ≥2 strong<br>or 1 strong + (≥3 moderate, 2 moderate + ≥2 supporting, or 1 moderate + ≥4 supporting) |
| 4 | Likely Pathogenic | PVS1 + 1 moderate<br>or 1 strong + (1–2 moderate or ≥2 supporting)<br>or ≥3 moderate<br>or 2 moderate + ≥2 supporting<br>or 1 moderate + ≥4 supporting |
| 3 | Uncertain Significance | No other classification criteria met, or the criteria support conflicting pathogenic and benign classifications |
| 2 | Likely Benign | 1 strong benign + 1 supporting benign, or ≥2 supporting benign |
| 1 | Benign | ≥2 strong benign, or 1 stand-alone benign |

In rows 4–5, evidence strengths refer to pathogenic evidence. PS, PM and PP denote strong, moderate and supporting pathogenic evidence, respectively. BA1 is stand-alone benign evidence. BS and BP denote strong and supporting benign evidence. For example, PP1 and PP3 alone, both at supporting strength and with no other evidence, yield uncertain significance.

**Variant notation normalization**: Always validate HGVS notation before querying databases. Use VariantValidator or EnsemblVEP to normalize.

### Immunotherapy Response Prediction

When immunotherapy eligibility is the question:

| Biomarker | Threshold | Implication |
|-----------|-----------|-------------|
| TMB-H | ≥13 mut/Mb by an FDA-authorized test | U.S. pembrolizumab tumor-agnostic indication under the 2026-10-16 FDA update. Check all conditions below before determining whether the indication applies. |
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
- Under the U.S. FDA update dated 2026-10-16, the pembrolizumab TMB-H indication covers adult and pediatric patients with unresectable or metastatic solid tumors, TMB ≥13 mut/Mb by an FDA-authorized test, progression after prior treatment, and no satisfactory alternative treatment options. [FDA approval notice](https://www.fda.gov/drugs/cancer-approvals/fda-grants-traditional-approval-pembrolizumab-or-pembrolizumab-and-berahyaluronidase-alfa-pmph)
- Check the product label and version applicable to the jurisdiction and date in the question. Report the assay and its measured TMB. If an indication criterion is unknown, state that eligibility cannot be determined. Treat the former U.S. accelerated-approval cutoff of ≥10 mut/Mb as historical.

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
