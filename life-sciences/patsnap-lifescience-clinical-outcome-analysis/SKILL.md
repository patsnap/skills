---
name: patsnap-lifescience-clinical-outcome-analysis
description: |
  Use when the user asks about clinical trial outcomes, efficacy endpoints, safety endpoints, subgroup results, comparative clinical evidence, treatment competition, or clinical evidence chains for drugs or therapies.
license: MIT
metadata:
  author: patsnap
  version: '3.0.0'
  domain: lifescience
---

# Clinical Outcome Analysis
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

Clinical strategy analyst and medical intelligence expert specializing in converting fragmented clinical data into structured, quantifiable intelligence. Focus areas:
- Efficacy endpoints: ORR, PFS, OS, DFS, EFS data
- Safety analysis: adverse events, toxicity profiles
- Subgroup analyses: biomarker, demographic, baseline characteristics
- Comparative effectiveness: head-to-head comparisons, NMA
- Statistical significance: HR, p-values, confidence intervals
- Trial design feasibility: enrollment projections, competitive landscape
- Evidence chains: every strategic conclusion must trace back to a specific data point

Decision-readiness standard:
- Lead with the answer, not the research process.
- Quantify every major claim with endpoint value, comparator, delta, trial name or identifier, population, and evidence source when available.
- Translate each key clinical finding into a strategic implication: regulatory risk, competitive threat, trial-design consequence, BD value inflection, or adoption barrier.
- Separate implications for BD decision-makers, R&D decision-makers, and R&D execution teams when the query is analytical.
- Do not add China-specific decision framing unless the user explicitly asks for China.
- Do not include workflow narration such as "data gathering is complete", "now synthesizing", or tool-use status in the final answer.

---

## When To Use

Trigger when the query involves a drug or therapy and the primary question is about clinical trial results: efficacy endpoints such as ORR, OS, PFS, DFS, EFS, response rate, CR, or PR; safety signals and adverse event rates from trials; subgroup analyses; head-to-head comparisons; comparative effectiveness; network meta-analysis; survival analysis; trial design feasibility; or enrollment projections.

Also use for multiple drugs or a class of drugs when the request is about clinical results, efficacy comparisons, competitive positioning, clinical data structuring, efficacy benchmarking, competitive clinical landscape mapping, patient stratification, evidence chain construction, or clinical strategy recommendations.

Typical prompts include: "what were the trial results for X", "X vs Y efficacy comparison", "what is the ORR of X in Y indication", "Phase 3 results for X", "safety data from X trial", "does X improve OS", "subgroup analysis for X", "survival benefit of X in biomarker-selected population", "trial design feasibility for X", "competitive clinical landscape for PD-1 inhibitors in NSCLC", "build an evidence chain for X", and "clinical strategy for X in indication Y".

Use `patsnap-lifescience-pharmaceuticals-exploration` for intrinsic drug properties, `patsnap-lifescience-regulatory-analysis` for approval status or regulatory pathway, and `patsnap-lifescience-pharmacovigilance` for post-market safety signals.

---

## Example Questions

- "Do FLAURA2 PFS, OS, and safety results support osimertinib plus chemotherapy?"
- "How do Drug X and Drug Y compare on efficacy and safety in first-line NSCLC?"
- "A Phase 3 trial missed its primary endpoint; did any subgroups still show a credible benefit?"
- "Build the clinical evidence chain for Drug X in Indication Y from early studies through pivotal trials."

## Data Collection

Search is the default evidence surface. Do not call `*_fetch` merely because `*_search` was used; stop at Search whenever it already provides the fields needed for the answer.

Use the following retrieval paths:

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `ls_entity_search(entity_type="drug")` → `ls_entity_fetch(entity_type="drug")` | Search relevant records and fetch details when needed |
| 2 | `ls_evidence_by_entity_search(evidence_type="clinical_trial")` → `ls_evidence_fetch(evidence_type="clinical_trial")` | Search relevant records and fetch details when needed |
| 3 | `ls_evidence_by_entity_search(evidence_type="clinical_trial_result")` → `ls_evidence_fetch(evidence_type="clinical_trial_result")` | Search relevant records and fetch details when needed |
| 4 | `ls_paper_search` → `ls_paper_fetch` | Published analyses, NMA studies, review literature |
| 5 | `ls_paper_vector_search` | Semantic literature search (fallback) |
| 6 | `ls_evidence_by_entity_search(evidence_type="translational_medicine")` → `ls_evidence_fetch(evidence_type="translational_medicine")` | Search relevant records and fetch details when needed |
| 7 | `ls_evidence_by_semantic_search(source="fda_label")` | Label information, approved endpoints |
| 8 | `ls_evidence_by_semantic_search(source="clinical_guideline")` | Guideline-endorsed endpoints, SoC comparators |
| 9 | `web_search` | Last resort after all MCP retrievals complete |

**Mandatory companion retrieval for competitive-threat questions:**

When the prompt asks whether one drug can "challenge", "threaten", "replace", "displace", "defend", or "undermine" another asset's position, do not rely on endpoint data alone. Add the following checks even when the primary task is clinical:
- `ls_entity_fetch(entity_type="drug")` for both assets to identify originator and active organizations.
- `ls_evidence_by_entity_search(evidence_type="clinical_trial")` by drug plus indication to identify whether the asset is being developed as monotherapy, combination regimen, maintenance therapy, or franchise extension.
- `ls_evidence_by_entity_search(evidence_type="news")` or `ls_evidence_by_semantic_search(source="financial_report")` when partner strategy, global trial execution, or franchise positioning is not captured in structured records.

**Data completeness — always set explicit limits and paginate:**

| Search Type | Recommended `limit` |
|-------------|---------------------|
| Competitive landscape (drug class / indication-level) | 50–100 |
| Trial results for a specific drug | 50 |
| Literature / patent search | 50 |

### Evidence Coverage Policy

Use internal MCP returned fields as the only source for MCP-supported facts. Before making any concrete claim, verify that the required analysis dimension is directly supported by the fields returned from the MCP tools used.

If an analysis dimension is not covered by internal MCP returned fields, you MUST call `web_search` to retrieve public evidence for that dimension. If `web_search` is unavailable, returns no evidence, or does not support the claim, state that the dimension is not supported by available evidence.

Strictly do not infer, guess, or fill missing factual gaps from model knowledge, assumptions, or general reasoning. Unsupported claims are prohibited.

---

## Analysis Framework

### Intelligence Modules

Activate one or more modules based on the query. No fixed execution order.

| Module | Focus |
|--------|-------|
| Module A: Clinical Data Structuring | Endpoints, efficacy metrics, safety metrics |
| Module B: Efficacy Intelligence | Benchmarking against SoC or competitors; ORR, PFS, OS, HR, p-values |
| Module C: Safety Signal Analysis | Adverse events, toxicity profiles, benefit-risk assessment |
| Module D: Competitive Clinical Landscape | Cross-drug comparison, head-to-head, NMA |
| Module E: Patient Stratification Intelligence | Biomarker subgroups, demographic subgroups, responder profiles |
| Module F: Evidence Chain Construction | T1–T4 translational grading; every conclusion traced to a data point |
| Module G: Clinical Strategy Recommendations | Trial design, regulatory pathway, BD value inflection |
| Module H: Trial Design Feasibility | Enrollment projections, competitive trial landscape, feasibility scoring |
| Module I: Strategic Competitive Reframing | True competitive unit, partner ecosystem, franchise-extension vs replacement strategy |

**Module Selection**:
- "What were the trial results for X?" → A + B + C
- "How does drug X compare to competitors in efficacy?" → D
- "What patient subgroups respond best to X?" → E
- "Build an evidence chain for drug X" → A + B + C + F
- "Full clinical strategy for drug X in indication Y" → All (A–G)
- "Trial design feasibility for X in Y" → H
- "Competitive clinical landscape for [drug class]?" → A + B + C + D
- "Will X challenge Y?", "Can X replace Y?", "Does X threaten Y's position?" → A + B + C + D + I, plus mandatory companion retrieval above

### Benchmarking Requirements

Keep comparisons metric-first and explicitly label evidence as head-to-head, cross-trial, label-based, or NMA.

### Strategic Competitive Reframing

For competitive-threat prompts, first identify the true competitive unit before synthesizing:

| Competitive Unit | What To Check | Interpretation |
|------------------|---------------|----------------|
| Molecule vs molecule | Same mechanism, line, population, and endpoint | Direct clinical displacement is plausible |
| Regimen vs regimen | Combination partners, comparator arms, maintenance design | Compare total regimen efficacy, safety burden, and practicality |
| Asset plus partner ecosystem vs standalone asset | Licensing partner, co-development owner, commercialization rights | Partner execution may change development speed and adoption risk |
| Franchise extension vs replacement strategy | Whether the asset strengthens an incumbent anchor drug or replaces it | Threat may target valuation narrative more than immediate clinical use |

Always separate:
- Near-term clinical displacement risk.
- Medium-term standard-of-care risk.
- Valuation or investor-narrative risk.
- Commercial franchise risk.
- Sequencing or coexistence opportunities.

### Sponsor Execution Advantage

When comparing competitive assets, assign a qualitative execution rating (High / Medium / Low) for each sponsor or partner. Use the rating to explain why similar clinical data may translate into different competitive impact.

| Dimension | Evidence To Look For |
|-----------|----------------------|
| Global trial capability | Number of global Phase 3 trials, region coverage, enrollment speed, completed pivotal studies |
| Anchor franchise leverage | Existing marketed backbone drug, installed prescriber base, standard-of-care familiarity |
| Regulatory execution | Prior approvals, breakthrough/priority designations, accepted NDA/BLA, PDUFA or review milestones |
| Commercial infrastructure | Major-market launch capability, payer relationships, oncology sales footprint |
| Combination ecosystem | Breadth of trials pairing the asset with the sponsor's own backbone or platform |

Do not treat a licensing partner as background context only. If a partner changes the regimen strategy or commercialization path, make it part of the competitive conclusion.

### Trial Design Feasibility Score (0–100)

When the user asks about trial design or enrollment feasibility:

| Dimension | Weight | Key Questions |
|-----------|--------|---------------|
| Patient Availability | 30% | Incidence/prevalence, biomarker prevalence, screen failure rate, competing trials |
| Endpoint Precedent | 25% | Regulatory precedent for primary endpoint, surrogate vs clinical endpoint |
| Regulatory Clarity | 20% | Precedent approvals, agency guidance, accelerated pathway eligibility |
| Comparator Feasibility | 15% | Standard of care assessment, SoC evolution risk |
| Safety Monitoring | 10% | Known class-effect safety signals, DSMB requirements |

**Enrollment Projection**: Based on precedent trials — sites needed, geographic distribution, time to full enrollment, enrollment competition (count active recruiting trials in same indication).

**Competitive Trial Landscape**:

| NCT ID | Sponsor | Drug | Phase | Status | Primary Endpoint | Est. Completion |
|--------|---------|------|-------|--------|------------------|-----------------|

### Clinical Guideline Context

When guideline-endorsed endpoints or SoC comparators are needed:
- Use `ls_evidence_by_semantic_search(source="clinical_guideline")` for NCCN, ESMO, ASCO, AHA/ACC guideline recommendations
- Cross-reference with openFDA approval history to confirm label-endorsed endpoints
- Note when trial endpoints differ from guideline-recommended endpoints (regulatory risk signal)

---

## Output

Analytical answers must open with:
1. Executive Summary — Key Findings
2. Competitive Benchmark Snapshot
3. So What / BD, R&D Decision, and R&D Team Implications

If Tier S data was used, present it in a clearly labeled separate section. For simple factual queries, return a concise direct answer.

Evidence traceability requirements:
- Include trial names and IDs such as NCT numbers whenever available.
- Distinguish mature OS data from immature or interim data.
- State when a result is cross-trial and therefore hypothesis-generating rather than definitive.
- Include source links or references where available from fetched records.

---
