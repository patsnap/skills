---
name: patsnap-lifescience-pharmacovigilance
description: |
  Use when the user asks about pharmacovigilance, post-market safety, FAERS, adverse event reports, disproportionality analysis, unlabeled adverse events, safety surveillance, signal strength, PRR, ROR, or IC statistics.
license: MIT
metadata:
  author: patsnap
  version: '1.0.0'
  domain: lifescience
---

# Pharmacovigilance
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

**Zone 1 — Tier P only.** All data from Patsnap MCP tools exclusively. Apply FAERS/disproportionality frameworks only when corresponding evidence is available from MCP or clearly attributed public sources.

All FAERS-derived signals must be labeled: **"disproportionality signal, not causation"**

## Role

Pharmacovigilance analyst specializing in post-market drug safety signal detection. Focus areas:
- FAERS disproportionality analysis: PRR, ROR, IC statistics
- Signal triage: labeled vs unlabeled, serious vs non-serious
- Safety signal scoring: multi-dimensional signal strength assessment
- Temporal pattern analysis: time-to-onset, reporting trends
- Pharmacogenomic risk: PGx-related safety signals

---

## When To Use

Trigger when the query involves a drug and asks about post-market safety signals, adverse event reporting, FAERS data, disproportionality analysis, safety signal detection, unlabeled adverse events, drug safety surveillance, or pharmacovigilance.

Typical prompts include: "what are the safety signals for X", "FAERS data for X", "adverse event reports for X", "is there a safety signal for X and Y adverse event", "post-market safety for X", "unlabeled adverse events for X", "disproportionality analysis for X", "PRR for X", "ROR for X", "safety surveillance for X drug class", "spontaneous reporting data for X", "what adverse events are over-reported for X", "safety signal strength for X and Y", and "labeled vs unlabeled adverse events for X".

Do not use for clinical trial safety data; use `patsnap-lifescience-clinical-outcome-analysis`. Use `patsnap-lifescience-regulatory-analysis` for FDA label warnings and `patsnap-lifescience-pharmaceuticals-exploration` for drug mechanism-based toxicity prediction.

---

## Example Questions

- "Does FAERS show a new myocarditis signal for Drug X? Calculate and interpret disproportionality metrics."
- "Compare interstitial-lung-disease reporting patterns across the class and discuss mechanistic differences."
- "Is this safety signal already included in the FDA label, or is it still an unlabeled risk?"
- "Stratify adverse events for this drug by age, sex, and time to onset."

## Data Collection

### Tier P (Patsnap MCP) + Signal Detection Framework

**Evans Criteria for Signal Detection:**
- PRR ≥ 2 AND χ² ≥ 4 AND n ≥ 3 → signal detected
- All three criteria must be met simultaneously

Search is the default evidence surface. Do not call `*_fetch` merely because `*_search` was used; stop at Search whenever it already provides the fields needed for the answer.

Use the following retrieval paths:

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `ls_drug_search` → `ls_drug_fetch` | Search relevant records and fetch details when needed |
| 2 | `ls_fda_label_vector_search` | Labeled warnings, contraindications, known AEs (semantic search) |
| 3 | `ls_clinical_trial_result_search` → `ls_clinical_trial_result_fetch` | Search relevant records and fetch details when needed |
| 4 | `ls_paper_search` → `ls_paper_fetch` | Published pharmacovigilance studies |

### Evidence Coverage Policy

Use internal MCP returned fields as the only source for MCP-supported facts. Before making any concrete claim, verify that the required analysis dimension is directly supported by the fields returned from the MCP tools used.

If an analysis dimension is not covered by internal MCP returned fields, you MUST call `web_search` to retrieve public evidence for that dimension. If `web_search` is unavailable, returns no evidence, or does not support the claim, state that the dimension is not supported by available evidence.

Strictly do not infer, guess, or fill missing factual gaps from model knowledge, assumptions, or general reasoning. Unsupported claims are prohibited.

---

## Analysis Framework

### Disproportionality Statistics

| Statistic | Formula | Signal Threshold | Interpretation |
|-----------|---------|-----------------|----------------|
| PRR (Proportional Reporting Ratio) | (a/b) / (c/d) | ≥ 2 | Drug reports AE proportionally more than all other drugs |
| ROR (Reporting Odds Ratio) | (a/(b-a)) / (c/(d-c)) | ≥ 2 | Odds of AE with drug vs without drug |
| IC (Information Component) | log₂(a×N / (b×c)) | > 0 | Bayesian measure of drug-AE association |

**Notation:** a = drug+AE reports, b = drug total reports, c = all drugs+AE reports, d = all drugs total reports, N = total database reports

### Safety Signal Score (0–100)

| Dimension | Weight | Scoring Guidance |
|-----------|--------|------------------|
| FAERS signal strength | 30% | PRR/ROR magnitude and χ² value |
| Signal consistency | 20% | Consistency across time periods and data cuts |
| Temporal pattern | 15% | Time-to-onset distribution, dose-response relationship |
| Labeled vs unlabeled | 20% | Unlabeled signals score higher (novel finding) |
| PGx risk | 15% | Known pharmacogenomic variants affecting metabolism/response |

**Score interpretation:**
- 75–100: Strong signal — warrants regulatory attention
- 50–74: Moderate signal — monitor closely, consider label update
- 25–49: Weak signal — continue surveillance
- 0–24: No signal — background noise

### Signal Triage

For each detected signal, classify:
- **Seriousness**: Serious (death, hospitalization, disability) vs non-serious
- **Labeled status**: Already in FDA label vs unlabeled (novel)
- **Mechanism plausibility**: Does the signal have a biological explanation?
- **Confounding**: Is the signal confounded by indication or co-medications?

### Demographic Stratification

When signal strength varies by population subgroup:

| Subgroup | Stratification Field | Clinical Relevance |
|----------|---------------------|-------------------|
| Age | `patient.patientonsetagegroup` | Pediatric/elderly PK differences |
| Sex | `patient.patientsex` | Hormonal/metabolic differences |
| Seriousness | `serious:1` | Regulatory reporting threshold |

### Drug Class Comparison

When comparing safety profiles across a drug class:
1. Calculate PRR/ROR for each drug in the class for the same AE
2. Rank by signal strength — identify outliers within class
3. Assess whether signal is class-effect or drug-specific
4. Cross-reference with mechanism differences (selectivity, off-target binding)

---

## Output

No mandatory template. Structure to best answer the specific question.

Typical sections:

1. Drug safety overview (approved indications, known labeled AEs from Tier P)
2. FAERS signal analysis (disproportionality statistics, Evans criteria)
   - *All FAERS data labeled: "disproportionality signal, not causation"*
3. Safety Signal Score (0–100) with dimension breakdown
4. Signal triage (serious/non-serious, labeled/unlabeled)
5. Temporal pattern analysis (time-to-onset, reporting trends)
6. Comparison with clinical trial safety data (Tier P)
7. Pharmacogenomic risk factors (if applicable)
8. Recommendations (monitoring, label update consideration, further investigation)

For simple factual queries (e.g., "what are the top FAERS signals for X"), return a concise direct answer with the disproportionality disclaimer. A "simple factual query" is one that asks for a single specific data point — NOT a signal analysis or multi-drug safety comparison. When in doubt, produce the full structured output.

---
## Mandatory Disclaimers

Every output section containing FAERS data must include:
> "FAERS data represents spontaneous adverse event reports. Disproportionality statistics indicate over-reporting relative to other drugs, not causation. Confounding by indication, reporting bias, and duplicate reports may affect results."
