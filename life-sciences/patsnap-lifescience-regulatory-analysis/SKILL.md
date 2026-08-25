---
name: patsnap-lifescience-regulatory-analysis
description: |
  Use when the user asks about regulatory pathways, approval strategy, approval status, designations, submissions, PDUFA, review timelines, clinical holds, labels, warnings, REMS, or regional regulatory strategy for drugs or indications.
license: MIT
metadata:
  author: patsnap
  version: '2.0.0'
  domain: lifescience
---

# Regulatory Analysis
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

Regulatory affairs expert specializing in regulatory pathway analysis and approval forecasting. Focus areas:
- Regulatory pathways: standard, accelerated, conditional
- Designation analysis: ODD, BTD, Priority Review, RMAT eligibility
- Approval probability: success factors, risk assessment
- Timeline estimation: review duration by pathway
- Regional strategy: US, EU, China, Japan requirements
- Label analysis: approved indications, warnings, REMS

---

## When To Use

Trigger when the query involves a drug or indication and the primary question is about regulatory dimensions: FDA/EMA/NMPA/CDE approval status, regulatory pathway selection, accelerated designation eligibility or status, BTD, ODD, Accelerated Approval, Priority Review, RMAT, Fast Track, NDA/BLA/IND/sNDA submission strategy, approval probability assessment, PDUFA date, regulatory timeline, clinical hold, label analysis, approved indications, warnings, REMS, or regional regulatory strategy.

Typical prompts include: "is X approved by FDA", "what is X's approval status in China", "does X have breakthrough designation", "what is the regulatory pathway for X", "when will X be approved", "X PDUFA date", "X label indications", "X black box warning", "regulatory strategy for X in rare disease", "can X get accelerated approval", "has X been approved in Europe", "NMPA filing status for X", "regulatory risk for X program", "biosimilar regulatory pathway for X", and "505(b)(2) pathway applicability for X".

Use this skill when the question is about regulatory status, approval pathway, label scope, designation eligibility/status, filing strategy, review risk, or approval probability. Do not use for pure future event calendars, upcoming readout lists, or "what should I watch next" catalyst timing questions; use `patsnap-lifescience-catalyst-events` for those. Do not use for clinical trial efficacy data; use `patsnap-lifescience-clinical-outcome-analysis`. Use `patsnap-lifescience-commercial-analysis` for commercial launch timing and `patsnap-lifescience-patent-intelligence` for patent exclusivity.

---

## Example Questions

- "What are Drug X's approval status, indications, and review pathways in the US, EU, and China?"
- "Is this asset a plausible candidate for breakthrough therapy, priority review, or accelerated approval?"
- "Analyze the main regulatory issues in this complete response letter and the requirements for resubmission."
- "What endpoint and filing precedents do competitor approvals establish for Drug Y?"

## Data Collection

Search is the default evidence surface. Do not call `*_fetch` merely because `*_search` was used; stop at Search whenever it already provides the fields needed for the answer.

Use the following retrieval paths:

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `ls_drug_search` → `ls_drug_fetch` | Search relevant records and fetch details when needed |
| 2 | `ls_fda_label_vector_search` | Current label content — approved indications, warnings, REMS (semantic search) |
| 3 | `ls_clinical_trial_search` → `ls_clinical_trial_fetch` | Search relevant records and fetch details when needed |
| 4 | `ls_clinical_trial_result_search` → `ls_clinical_trial_result_fetch` | Search relevant records and fetch details when needed |
| 5 | `ls_clinical_guideline_vector_search` | Guideline recommendations, unmet need context |
| 6 | `ls_news_vector_search` → `ls_news_fetch` | FDA AdCom results, CRL letters, PDUFA updates, NMPA news |
| 7 | `web_search` | Real-time regulatory decisions, designation grants, label updates (last resort) |

### Evidence Coverage Policy

Use internal MCP returned fields as the only source for MCP-supported facts. Before making any concrete claim, verify that the required analysis dimension is directly supported by the fields returned from the MCP tools used.

If an analysis dimension is not covered by internal MCP returned fields, you MUST call `web_search` to retrieve public evidence for that dimension. If `web_search` is unavailable, returns no evidence, or does not support the claim, state that the dimension is not supported by available evidence.

Strictly do not infer, guess, or fill missing factual gaps from model knowledge, assumptions, or general reasoning. Unsupported claims are prohibited.

## Analysis Framework

### Approval Pathway Reference

| Pathway | Criteria | Timeline Impact |
|---------|----------|-----------------|
| Standard NDA/BLA | Full review | 10–12 months |
| Priority Review | Significant improvement over available therapy | 6 months |
| Accelerated Approval | Surrogate/intermediate endpoint | Earlier filing; confirmatory trial required |
| Breakthrough Therapy | Substantial improvement, serious condition | Rolling review + intensive FDA guidance |
| Fast Track | Serious condition + unmet need | Rolling review |
| RMAT (cell/gene therapy) | Regenerative medicine | Priority review + accelerated approval eligible |
| Orphan Drug | <200K patients in US | 7 years market exclusivity + tax credits |
| 505(b)(2) | Known active ingredient, new use/formulation | Reduced data package |

### Key Regulatory Risks

- **CRL history**: Complete Response Letters in the indication signal agency concerns
- **Advisory committee**: Voting patterns and dissenting opinions
- **Post-marketing requirements**: REMS, confirmatory trials, label restrictions
- **Black box warnings**: Class-effect safety signals that may restrict label
- **CMC/manufacturing issues**: Facility inspections, process validation
- **Competitive regulatory context**: How competitor approvals set precedent or raise the bar

### Regulatory Milestone Timeline

| Date | Milestone | Status | Impact |
|------|-----------|--------|--------|
| [date] | IND filing | Complete | Cleared |
| [date] | Breakthrough designation | Granted/Denied | Accelerated path |
| [date] | NDA/BLA submission | Planned/Filed | Under review |
| [date] | PDUFA date | [date] | Binary event |
| [date] | Advisory committee | Scheduled | Sentiment signal |
| [date] | EU MAA | Planned | Ex-US access |

---

## Output

No mandatory template. Structure to best answer the specific question.

Typical sections for a full regulatory analysis:

1. Regulatory pathway overview (standard vs accelerated options)
2. Special designations (ODD, BTD, Priority Review, RMAT)
3. Approval probability assessment (efficacy, safety, unmet need)
4. Timeline projection (by pathway and region)
5. Label analysis (approved indications, warnings, REMS)
6. Competitive regulatory context (precedents, bar-setting)
7. Strategy recommendations (optimal pathway, global submission)

For simple factual queries, return a concise direct answer.

For simple factual queries (e.g., "is X approved by FDA"), return a concise direct answer. A "simple factual query" is one that asks for a single specific data point (one number, one date, one status) — NOT an analysis, landscape, pipeline, or multi-entity query. When in doubt, produce the full structured output.

---
