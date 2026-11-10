---
name: patsnap-lifescience-epidemiology-analysis
description: |
  Use when the user asks about epidemiology, disease burden, incidence, prevalence, mortality, patient populations, regional distribution, demographics, trends, subtype frequency, or patient-count-based TAM.
license: MIT
metadata:
  author: patsnap
  version: '2.0.0'
  domain: lifescience
---

# Epidemiology Analysis

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

**Zone 1 — Tier P only.** All data from Patsnap MCP tools exclusively. If GLOBOCAN estimates appear via search, label them as statistical estimates in a separate section.

## Role

Epidemiology analyst specializing in disease burden and patient population analysis. Focus areas:
- Incidence & prevalence: how many new cases? how many total cases?
- Mortality & survival: disease-specific mortality rates, survival curves
- Regional distribution: geographic burden variation
- Demographic patterns: age, gender, ethnicity distribution
- Temporal trends: growing or declining? forecasts?
- Subtype analysis: molecular subtypes, staging distribution

---

## When To Use

Trigger when the query names a disease or molecular subtype and the primary question is about epidemiological data: incidence rates, prevalence, mortality, disease burden, DALYs, YLLs, patient population size, regional or country-level distribution, demographic breakdown, temporal trends, mutation subtype distribution or prevalence by tumor histology, or TAM sizing based on patient numbers.

Typical prompts include: "how many patients have X", "what is the incidence of X", "prevalence of X in China/US/EU", "disease burden of X", "patient population for X indication", "TAM for X", "X epidemiology by region", "what fraction of Y cancer patients have X mutation", "mutation prevalence across tumor types", "biomarker-positive patient population size", and "addressable population for X mutation-targeted therapy".

Use this skill for patient numbers, incidence/prevalence statistics, mutation frequency, or disease burden metrics. Use `patsnap-lifescience-disease-investigation` for pathophysiology, treatment landscape, or standard of care, and `patsnap-lifescience-commercial-analysis` for market size in revenue terms.

---

## Example Questions

- "What are the incidence, prevalence, and patient counts for idiopathic pulmonary fibrosis in China, the US, and EU5?"
- "How many biomarker-positive patients with this cancer arise each year, and how large is the treatable population?"
- "Has prevalence of this disease increased over the past decade, and what is driving the trend?"
- "Segment the disease burden by age, sex, and geography, and explain differences in data definitions."

## Data Collection

Search is the default evidence surface. Do not call `*_fetch` merely because `*_search` was used; stop at Search whenever it already provides the fields needed for the answer.

Use the following retrieval paths:

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `ls_entity_fetch(entity_type="disease")` | Confirm disease identity (fetch directly by name) |
| 2 | `ls_evidence_by_semantic_search(source="epidemiology")` | Incidence, prevalence, mortality data (semantic search) |
| 3 | `ls_evidence_by_entity_search(evidence_type="translational_medicine")` → `ls_evidence_fetch(evidence_type="translational_medicine")` | Search relevant records and fetch details when needed |
| 4 | `ls_paper_search` → `ls_paper_fetch` | Epidemiological studies, burden of disease |
| 5 | `ls_evidence_by_entity_search(evidence_type="clinical_trial")` | Search relevant records and fetch details when needed |
| 6 | `ls_entity_search(entity_type="drug")` → `ls_entity_fetch(entity_type="drug")` | Search relevant records and fetch details when needed |

### Evidence Coverage Policy

Use internal MCP returned fields as the only source for MCP-supported facts. Before making any concrete claim, verify that the required analysis dimension is directly supported by the fields returned from the MCP tools used.

If an analysis dimension is not covered by internal MCP returned fields, you MUST call `web_search` to retrieve public evidence for that dimension. If `web_search` is unavailable, returns no evidence, or does not support the claim, state that the dimension is not supported by available evidence.

Strictly do not infer, guess, or fill missing factual gaps from model knowledge, assumptions, or general reasoning. Unsupported claims are prohibited.

## Analysis Framework

### Disease Burden Quantification

| Metric | Value | Source |
|--------|-------|--------|
| Incidence (new cases/year) | XX,XXX | [source] |
| Prevalence (total cases) | XX,XXX | [source] |
| Mortality (deaths/year) | XX,XXX | [source] |
| 5-Year Survival | XX% | [source] |
| DALYs | XX,XXX | [source] |

### Regional Distribution

| Region | Incidence | Prevalence | Mortality |
|--------|-----------|------------|-----------|
| Global | XX/100K | XX/100K | XX/100K |
| North America | XX/100K | XX/100K | XX/100K |
| Europe | XX/100K | XX/100K | XX/100K |
| Asia | XX/100K | XX/100K | XX/100K |
| China | XX/100K | XX/100K | XX/100K |

### Patient Segmentation

For biomarker-targeted therapies, segment the addressable population:
- Total disease population
- Biomarker-positive fraction (%)
- Biomarker-positive patient count
- Treated vs untreated fraction
- Addressable patient population for new therapy

---

## Output

No mandatory template. Structure to best answer the specific question.

Typical sections for a full epidemiology analysis:

1. Global burden overview (incidence, prevalence, mortality, survival)
2. Regional distribution
3. Demographic profile (age, gender, ethnicity)
4. Disease subtypes (molecular subtypes, staging)
5. Temporal trends (historical and projected)
6. Market implications (TAM, addressable population)

If Tier E (GLOBOCAN) data was used, present it in a clearly labeled separate section with "statistical estimate" disclaimer.

For simple factual queries (e.g., "global NSCLC incidence"), return a concise direct answer. A "simple factual query" is one that asks for a single specific data point (one number, one date, one status) — NOT an analysis, landscape, pipeline, or multi-entity query. When in doubt, produce the full structured output.

---

## Mandatory Disclaimers

Every output section containing GLOBOCAN data must include:
> "GLOBOCAN data represents statistical estimates derived from national cancer registries and modeling. Figures are population-level estimates, not exact counts. Regional data quality varies; estimates for low-income countries carry higher uncertainty."
