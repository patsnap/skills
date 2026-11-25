---
copyright: "Copyright © Patsnap. All rights reserved."
name: patsnap-lifescience-disease-investigation
description: Use when the user asks about a disease or indication, including pathophysiology,
  molecular mechanisms, standard of care, guidelines, unmet need, subtypes, diagnosis,
  or emerging therapies.
license: MIT
metadata:
  author: Patsnap
  version: 1.0.0
  category: "Life Science"
---

# Disease Investigation
**Zone 1 — Tier P only.** Prioritize Patsnap MCP evidence; when key fields are missing or conflicting, verify official primary sources under the rules below.

## Writing and Output Style

Write as an analytical memo for business, BD, R&D or medical colleagues: lead with the conclusion, then evidence and reasoning. Retain necessary technical terms, drug names, endpoints and database names, while avoiding awkward word-for-word translation.

- Use concise sentences and clear judgments; avoid empty stock phrases.
- Anchor each key judgment in data, sources, applicable populations, comparators or time windows.
- Do not narrate internal work or tool status, such as "retrieval is complete" or "now analyzing."

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

This skill requires the Patsnap `pharma-intelligence` MCP service. See the [MCP setup guide](https://github.com/patsnap/skills/blob/main/life-sciences/MCP_SETUP.md) for connection and verification steps.

Search is the default evidence-gathering method. Do not call `*_fetch` merely because `*_search` was called. Further detail retrieval is unnecessary only when the results have passed entity and scope checks, contain the fields required to answer the question, and have no unresolved material conflicts.

| Step | Tool | Purpose |
| ---- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| 1 | `ls_entity_fetch(entity_type="disease")` | Confirm disease identity by direct name-based retrieval |
| 2 | `ls_paper_search` → `ls_paper_fetch`                  | Pathophysiology and mechanisms |
| 3 | `ls_evidence_by_entity_search(evidence_type="translational_medicine")` → `ls_evidence_fetch(evidence_type="translational_medicine")` | Retrieve relevant records and fetch details when needed |
| 4 | `ls_evidence_by_semantic_search(source="epidemiology")`                    | Incidence and prevalence data |
| 5 | `ls_evidence_by_semantic_search(source="clinical_guideline")`                 | Standard-of-care guidelines |
| 6 | `ls_evidence_by_entity_search(evidence_type="clinical_trial")` → `ls_evidence_fetch(evidence_type="clinical_trial")`         | Retrieve relevant records and fetch details when needed |
| 7 | `ls_entity_search(entity_type="drug")` → `ls_entity_fetch(entity_type="drug")`                   | Retrieve relevant records and fetch details when needed |
| 8 | `ls_evidence_by_entity_search(evidence_type="drug_deal")` → `ls_evidence_fetch(evidence_type="drug_deal")`              | Retrieve relevant records and fetch details when needed |

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

- Define region, period, disease stage, treatment line, testing method and population denominator before using percentages. The proportion randomized among screened trial participants describes trial selection only, not biomarker prevalence or the treatable share of the disease population.
- For populations defined by multiple conditions, preserve testing methods, thresholds and AND/OR relationships and account for intersections. Do not multiply marginal rates from different studies under an unverified independence assumption or add overlapping subgroups directly.
- In patient-pool or market estimates, identify the source, conditional probability and assumption for each component. Without representative testing or epidemiological evidence, provide ranges or unresolved conditions rather than inventing a definite patient count.
- Organize treatment pathways by region, guideline version, treatment line and patient characteristics. Distinguish approved scope, guideline recommendations and study regimens. Recommendations require applicability conditions; cross-trial values cannot directly rank regimen superiority.

---

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
