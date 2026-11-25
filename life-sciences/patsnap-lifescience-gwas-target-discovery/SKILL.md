---
copyright: "Copyright © Patsnap. All rights reserved."
name: patsnap-lifescience-gwas-target-discovery
description: Use when the user asks about genetically validated targets, GWAS evidence,
  genetic association, Mendelian randomization, locus-to-gene mapping, eQTL, druggability,
  or GWAS-to-drug target prioritization.
license: MIT
metadata:
  author: Patsnap
  version: 1.0.0
  category: "Life Science"
---

# GWAS Target Discovery
**Zone 1 — Tier P only.** Prioritize Patsnap MCP evidence; when key fields are missing or conflicting, verify official primary sources under the rules below.

All GWAS-derived associations must be labeled: **"statistical genetic association, not proven causation"**

## Writing and Output Style

Write as an analytical memo for business, BD, R&D or medical colleagues: lead with the conclusion, then evidence and reasoning. Retain necessary technical terms, drug names, endpoints and database names, while avoiding awkward word-for-word translation.

- Use concise sentences and clear judgments; avoid empty stock phrases.
- Anchor each key judgment in data, sources, applicable populations, comparators or time windows.
- Do not narrate internal work or tool status, such as "retrieval is complete" or "now analyzing."

## Role

Genetic target discovery analyst specializing in GWAS-to-drug pipeline. Focus areas:
- GWAS hit identification: genetic associations for a disease
- Locus-to-gene mapping: which gene does each GWAS signal implicate?
- Mendelian randomization: causal inference from genetic instruments
- Druggability assessment: can GWAS-implicated targets be drugged?
- Existing drug overlap: are any GWAS targets already drugged?
- PPI network analysis: pathway context for GWAS hits

---

## When To Use

Trigger when the query involves genetic association data, GWAS findings, or genetically validated drug targets, including GWAS hits for a disease, Mendelian randomization evidence, locus-to-gene mapping, eQTL analysis, genetic druggability assessment, or a GWAS-to-drug pipeline.

Typical prompts include: "what GWAS hits exist for X disease", "genetically validated targets for X", "Mendelian randomization evidence for X target in Y disease", "which GWAS loci are druggable for X", "eQTL evidence for X gene in Y tissue", "genetic support for X as a drug target", "GWAS-based target prioritization for X disease", "what genes are implicated by GWAS in X", "locus-to-gene mapping for X GWAS signal", "Open Targets genetics score for X", "genetic evidence for X target", "PPI network for GWAS hits in X disease", and "druggability of GWAS-implicated targets in X".

Do not use for clinical drug development pipeline; use `patsnap-lifescience-target-intelligence`. Use `patsnap-lifescience-disease-investigation` for disease pathophysiology and `patsnap-lifescience-biomarker-analysis` for biomarker clinical actionability.

---

## Example Questions

- "Use GWAS, eQTL, and Mendelian-randomization evidence to prioritize new targets for inflammatory bowel disease."
- "Which causal gene most likely explains this GWAS locus, and is the evidence chain consistent?"
- "Compare three genetically validated targets on causal evidence, druggability, and safety risk."
- "Identify cardiovascular targets with strong genetic support but limited current development activity."

## Data Collection

This skill requires the Patsnap `pharma-intelligence` MCP service. See the [MCP setup guide](https://github.com/patsnap/skills/blob/main/life-sciences/MCP_SETUP.md) for connection and verification steps.

### Tier P (Background — Patsnap MCP)

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `ls_evidence_by_entity_search(evidence_type="translational_medicine")` → `ls_evidence_fetch(evidence_type="translational_medicine")` | Retrieve relevant records and fetch details when needed |
| 2 | `ls_entity_search(entity_type="drug")` → `ls_entity_fetch(entity_type="drug")` | Retrieve relevant records and fetch details when needed |
| 3 | `ls_evidence_by_entity_search(evidence_type="clinical_trial")` → `ls_evidence_fetch(evidence_type="clinical_trial")` | Retrieve relevant records and fetch details when needed |
| 4 | `ls_evidence_by_entity_search(evidence_type="drug_deal")` → `ls_evidence_fetch(evidence_type="drug_deal")` | Retrieve relevant records and fetch details when needed |
| 5 | `ls_patent_search` → `ls_patent_fetch` | IP landscape for GWAS-related targets |

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

- Retain phenotype definition, ancestry, sample, variant identifier, effect direction, statistical significance and independent replication. Assess locus association, gene mapping, causal evidence and intervention feasibility separately; significant association is not direct validation of a drug target.
- Check comparability and overlapping samples before comparing effects across cohorts, phenotypes or ancestries. Target prioritization must identify evidence gaps and selection conditions; retain uncertainty without replication.

---

## Analysis Framework

### GWAS → Target → Drug Pipeline

```
1. GWAS hits (Tier E: GWAS Catalog — study discovery, trait resolution, variant collection)
   ↓
2. Variant annotation (Tier E: EnsemblVEP — functional consequence, gnomAD — population freq)
   ↓
3. Locus-to-gene mapping (Tier E: Open Targets Genetics L2G scores)
   ↓
4. eQTL colocalization (Tier S: GTEx — which tissues? causal gene support)
   ↓
5. Pathway enrichment (Tier S: Reactome — biological context for GWAS gene set)
   ↓
6. Protein function & druggability (Tier S: UniProt, STRING, DGIdb)
   ↓
7. Existing drugs on target (Tier P: Patsnap ls_entity_search(entity_type="drug"))
   ↓
8. Clinical trials & BD activity (Tier P: Patsnap)
```

### Mendelian Randomization Evidence Assessment

For each GWAS-implicated target, assess MR evidence quality:

| Criterion | Assessment |
|-----------|------------|
| Instrument strength (F-statistic) | F > 10 = strong instrument |
| Pleiotropy | MR-Egger intercept ≈ 0 = no pleiotropy |
| Consistency | IVW, weighted median, MR-Egger concordant |
| Directionality | Steiger filtering confirms direction |
| Replication | Consistent across independent GWAS |

**MR Evidence Levels:**
- Strong: Multiple instruments, consistent across methods, replicated
- Moderate: Single instrument or inconsistent across methods
- Weak: Insufficient instruments or significant pleiotropy

### Population Genetics Context

**Cross-ancestry considerations:**
- LD structure differs across ancestries — GWAS hits in European cohorts may not transfer to East Asian or African populations
- Fine-mapping credible sets should be validated across ancestries when multi-ancestry GWAS data exists
- gnomAD allele frequencies by ancestry help distinguish population-specific vs universal variants

### Druggability Assessment for GWAS Hits

| Criterion | Score | Notes |
|-----------|-------|-------|
| Target class | High/Medium/Low | Kinase/GPCR/nuclear receptor = high; transcription factor = low |
| Structural data | High/Medium/Low | Crystal structure available = high |
| Existing ligands | High/Medium/Low | Known small molecule binders = high |
| Existing drugs | High/Medium/Low | Already drugged = high (repurposing opportunity) |
| Tissue expression | High/Medium/Low | Disease-relevant tissue expression = high |

---

## Output

No mandatory template. Structure to best answer the specific question.

Typical sections:

**Tier E section (primary):**
1. GWAS landscape for disease (top hits, study quality, sample sizes)
   - *All GWAS data labeled: "statistical genetic association, not proven causation"*
2. Locus-to-gene mapping (L2G scores, top implicated genes)
3. Mendelian randomization evidence (causal inference quality)

**Tier S section:**
4. eQTL evidence (tissue-specific expression, GTEx)
5. Protein-protein interaction network (STRING)
6. Protein function and druggability (UniProt)

**Tier P section:**
7. Existing drugs on GWAS-implicated targets (Patsnap)
8. Clinical trials for GWAS-validated targets
9. BD activity and deal precedents

**Summary:**
10. Target prioritization table (ranked by genetic evidence + druggability)
11. Repurposing opportunities (existing drugs on GWAS targets)
12. White space targets (genetically validated but undrugged)

For simple factual queries (e.g., "what GWAS hits exist for type 2 diabetes"), return a concise direct answer with the genetic association disclaimer. A "simple factual query" is one that asks for a single specific data point — NOT a target discovery analysis or multi-locus query. When in doubt, produce the full structured output.

---

## Mandatory Disclaimers

Every output section containing GWAS data must include:
> "GWAS associations are statistical signals from population genetics studies. Genetic association does not imply causation. Locus-to-gene mapping and Mendelian randomization provide additional evidence but require experimental validation."

---
