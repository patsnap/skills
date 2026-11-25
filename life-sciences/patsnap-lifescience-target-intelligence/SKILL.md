---
name: patsnap-lifescience-target-intelligence
description: Use when the user asks about a biomedical target as the primary subject,
  including biology, druggability, indication fit, modality options, competitive pipeline,
  clinical progress, deals, or white-space opportunities.
license: MIT
metadata:
  author: patsnap
  version: 1.0.0
  domain: lifescience
---

# Target Intelligence
**Zone 1 — Tier P only.** Prioritize Patsnap MCP evidence; when key fields are missing or conflicting, verify official primary sources under the rules below.

## Writing and Output Style

Write as an analytical memo for business, BD, R&D or medical colleagues: lead with the conclusion, then evidence and reasoning. Retain necessary technical terms, drug names, endpoints and database names, while avoiding awkward word-for-word translation.

- Use concise sentences and clear judgments; avoid empty stock phrases.
- Anchor each key judgment in data, sources, applicable populations, comparators or time windows.
- Do not narrate internal work or tool status, such as "retrieval is complete" or "now analyzing."

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

Search is the default evidence-gathering method. Do not call `*_fetch` merely because `*_search` was called. Further detail retrieval is unnecessary only when the results have passed entity and scope checks, contain the fields required to answer the question, and have no unresolved material conflicts.

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `ls_entity_fetch(entity_type="target")` | Target biology details and database IDs (KEGG, UniProt, NCBI Gene, RefSeq, UMLS CUI) |
| 2 | `ls_paper_search` → `ls_paper_fetch` | Drug development history and reviews |
| 3 | `ls_evidence_by_entity_search(evidence_type="translational_medicine")` → `ls_evidence_fetch(evidence_type="translational_medicine")` | Retrieve relevant records and fetch details when needed |
| 4 | `ls_entity_search(entity_type="drug")` → `ls_entity_fetch(entity_type="drug")` | Retrieve relevant records and fetch details when needed |
| 5 | `ls_evidence_by_entity_search(evidence_type="drug_deal")` → `ls_evidence_fetch(evidence_type="drug_deal")` | Retrieve relevant records and fetch details when needed |
| 6 | `ls_evidence_by_entity_search(evidence_type="clinical_trial")` → `ls_evidence_fetch(evidence_type="clinical_trial")` | Retrieve relevant records and fetch details when needed |
| 7 | `ls_evidence_by_entity_search(evidence_type="clinical_trial_result")` → `ls_evidence_fetch(evidence_type="clinical_trial_result")` | Retrieve relevant records and fetch details when needed |
| 8 | `ls_evidence_by_entity_search(evidence_type="news")` → `ls_evidence_fetch(evidence_type="news")` | Recent target news |
| 9 | `ls_web_search` | Verify official primary sources when key facts are missing, conflicting or return zero hits |

Execute only steps relevant to the question; stop when the available data are sufficient.

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

- Establish trial identity using registry number, official protocol number, sponsor and intervention. Do not assign a study-series name from a similar code. Preserve key inclusion subtypes and exclusions rather than substituting the drug's previously approved population. Render ACTIVE_NOT_RECRUITING as "ongoing, no longer recruiting," include the registry update date, and qualify stale records as "the registry reports."
- Update decision-relevant results and milestones before ranking development directions. Do not treat results disclosed before the cutoff as future triggers. Success of a direction does not establish efficacy of a proposed asset; positive competing regimens do not prove that the direction has no opportunity. Give conditional priorities based on the company's existing assets, stage, technical/manufacturing capabilities, resources and regional pathways. If the starting point is unknown, give scenarios rather than promising a fixed development duration.
- Even structured screening requires candidate-level checks of region, indication, actual-start evidence and asset role. Separate an ADC antibody's recognition target from its payload mechanism. A study involving an EGFR drug does not establish that all patients have EGFR mutations; a comparator drug is not automatically the investigational asset.
- Record trial phase, study region, recruitment status, start date with actual/estimated designation, and registry update date separately. A global maximum phase does not establish the phase for a particular region and indication.
- "Conducted" or "started" requires actual-start evidence within the requested scope. An elapsed estimated start date does not prove initiation; if the record is stale, state that initiation remains unconfirmed. Interpret Study Start by the registry definition. Global first enrollment does not automatically establish first enrollment or first dosing at a particular country's sites.
- Verify phase, regional participation and actual initiation separately. Do not universally add requirements such as ethics approval documents; use procedural evidence as a selection criterion only when explicitly requested.
- Merge drug aliases using reliable identity mappings, but retain trials by registry identifier. Merging registrations requires a shared protocol, cross-registration or official mapping; similar names, enrollment or dates are insufficient. Combination and multi-arm trials can involve multiple assets.
- Distinguish direct drug targets, conjugate antibody targets, payload mechanisms and enrollment biomarkers, and state the target definition used for screening.
- Judge efficacy across modalities or trials only under comparable conditions. Prioritize development directions using evidence maturity, population, feasibility and resources, stating conditions that would change the ranking; do not rank directly by numbers from different trials.
- Define region, period, disease stage, treatment line, testing method and population denominator before using percentages. The proportion randomized among screened trial participants describes trial selection only, not biomarker prevalence or the treatable share of the disease population.
- For populations defined by multiple conditions, preserve testing methods, thresholds and AND/OR relationships and account for intersections. Do not multiply marginal rates from different studies under an unverified independence assumption or add overlapping subgroups directly.
- In patient-pool or market estimates, identify the source, conditional probability and assumption for each component. Without representative testing or epidemiological evidence, provide ranges or unresolved conditions rather than inventing a definite patient count.

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
- Select representative assets and key risks according to the user request; rankings require a comparable basis and applicability conditions.
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
