---
name: patsnap-lifescience-pharmaceuticals-exploration
description: Use when the user asks about one specific drug or therapeutic compound,
  including MoA, pharmacodynamics, PK, ADMET, safety, dosage, formulation, BBB penetration,
  interactions, special populations, or drug-specific clinical data.
license: MIT
metadata:
  author: patsnap
  version: 1.0.0
  domain: lifescience
---

# Pharmaceuticals Exploration
**Zone 1 — Tier P only.** Prioritize Patsnap MCP evidence; when key fields are missing or conflicting, verify official primary sources under the rules below.

## Writing and Output Style

Write as an analytical memo for business, BD, R&D or medical colleagues: lead with the conclusion, then evidence and reasoning. Retain necessary technical terms, drug names, endpoints and database names, while avoiding awkward word-for-word translation.

- Use concise sentences and clear judgments; avoid empty stock phrases.
- Anchor each key judgment in data, sources, applicable populations, comparators or time windows.
- Do not narrate internal work or tool status, such as "retrieval is complete" or "now analyzing."

## Role

Pharmaceutical industry specialist focusing on individual drug characteristics. Focus areas:
- Pharmacodynamics: drug-target interactions, mechanism of action
- Pharmacokinetics: ADMET data, absorption, distribution, metabolism, excretion
- Clinical results: trial outcomes, efficacy endpoints, safety signals
- Commercial: licensing deals, partnerships
- Repurposing: compound-based repurposing analysis

Decision-readiness standard:
- Lead with the drug's practical conclusion: differentiated or not, best use case, key limitation, and evidence strength.
- Quantify claims with target potency, PK parameters, dosing burden, efficacy endpoints, safety rates, regulatory status, and comparator benchmarks whenever available.
- Translate intrinsic properties into implications: patient selection, dosing convenience, DDI risk, safety monitoring, competitive positioning, repurposing feasibility, or partner attractiveness.
- Separate implications for BD decision-makers, R&D decision-makers, and R&D execution teams when the query is analytical.
- Do not add China-specific decision framing unless the user explicitly asks for China.
- Do not include workflow narration such as "data gathering is complete", "now synthesizing", or tool-use status in the final answer.

---

## When To Use

Trigger when the query names a specific drug by brand name, generic name, or development code and asks about that drug's specific properties: mechanism of action, pharmacodynamics, Kd/Ki/IC50/EC50, pharmacokinetics, half-life, bioavailability, CYP metabolism, ADMET profile, safety and adverse events, dosage and formulation, blood-brain barrier penetration, drug-drug interactions, special population considerations, or clinical results specific to that drug.

Typical prompts include: "how does X work", "what is X's half-life", "X side effects", "X dosing regimen", "X pharmacokinetics", "is X safe in pregnancy", "X drug interactions", "X benefit-risk profile", "what is the mechanism of action of X", "what targets does X hit", "X selectivity profile", "X off-target effects", "bioavailability of X", "X metabolic pathway", "X blood-brain barrier penetration", "X formulation differences", "X drug combination rationale", "X structure-activity relationship", and "repurposing potential for X drug".

Use this skill when one specific drug is the subject and the question is about intrinsic properties. Do not use it for full historical pathway reconstruction, milestone sequencing, development acceleration/delay analysis, or "how did this drug develop" questions; use `patsnap-lifescience-drug-development-pathway` for those. Use `patsnap-lifescience-catalyst-events` when the user mainly wants future event timing, PDUFA/readout windows, or a catalyst calendar. Use `patsnap-lifescience-clinical-outcome-analysis` for trial results and efficacy endpoints, and `patsnap-lifescience-target-intelligence` for comparing multiple drugs targeting the same mechanism.

---

## Example Questions

- "Profile osimertinib's mechanism, selectivity, PK, dosing, and principal safety risks."
- "Is the rifampin-osimertinib interaction clinically major? Quantify exposure changes and recommend management."
- "Score metformin's drug-repurposing potential for age-related macular degeneration."

## Data Collection

Search is the default evidence-gathering method. Do not call `*_fetch` merely because `*_search` was called. Further detail retrieval is unnecessary only when the results have passed entity and scope checks, contain the fields required to answer the question, and have no unresolved material conflicts.

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `ls_entity_search(entity_type="drug")` → `ls_entity_fetch(entity_type="drug")` | Retrieve relevant records and fetch details when needed |
| 2 | `ls_paper_search` → `ls_paper_fetch` | Pharmacodynamics and mechanism-of-action literature |
| 3 | `ls_evidence_by_entity_search(evidence_type="translational_medicine")` → `ls_evidence_fetch(evidence_type="translational_medicine")` | Retrieve relevant records and fetch details when needed |
| 4 | `ls_evidence_by_entity_search(evidence_type="clinical_trial")` → `ls_evidence_fetch(evidence_type="clinical_trial")` | Retrieve relevant records and fetch details when needed |
| 5 | `ls_evidence_by_entity_search(evidence_type="clinical_trial_result")` → `ls_evidence_fetch(evidence_type="clinical_trial_result")` | Retrieve relevant records and fetch details when needed |
| 6 | `ls_evidence_by_semantic_search(source="fda_label")` | Regulatory labeling, dosing and warnings (semantic search) |
| 7 | `ls_evidence_by_semantic_search(source="clinical_guideline")` | Position of the drug in treatment guidelines |
| 8 | `ls_evidence_by_entity_search(evidence_type="drug_deal")` → `ls_evidence_fetch(evidence_type="drug_deal")` | Retrieve relevant records and fetch details when needed |
| 9 | `ls_web_search` | Commercial pricing and real-world safety signals (fact verification) |

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

- Build cross-regional drug profiles by asset, region, indication and regimen. Maximum phase, selected indications or counts in an entity summary do not establish a complete inventory. Search specifically for missing label or development records; items outside a summary are not necessarily nonexistent.
- Record trial phase, study region, recruitment status, start date with actual/estimated designation, and registry update date separately. A global maximum phase does not establish the phase for a particular region and indication.
- "Conducted" or "started" requires actual-start evidence within the requested scope. An elapsed estimated start date does not prove initiation; if the record is stale, state that initiation remains unconfirmed. Interpret Study Start by the registry definition. Global first enrollment does not automatically establish first enrollment or first dosing at a particular country's sites.
- Verify phase, regional participation and actual initiation separately. Do not universally add requirements such as ethics approval documents; use procedural evidence as a selection criterion only when explicitly requested.
- Merge drug aliases using reliable identity mappings, but retain trials by registry identifier. Merging registrations requires a shared protocol, cross-registration or official mapping; similar names, enrollment or dates are insufficient. Combination and multi-arm trials can involve multiple assets.
- List approved scope by drug, formulation or regimen, indication, treatment line and region. Separate submission, acceptance, review, approval and launch. Count only items supported by approval evidence as approved, and distinguish announcement dates from decision dates.
- To verify current status, check labels and approval changes applicable by the query cutoff. If no approval record is retrieved for a region, mark it unverified rather than declaring the indication unapproved.
- Check regulatory requirements by region, indication and pathway. One project failure, withdrawal or immature endpoint does not establish a universal approval threshold for a drug class. Existing marketing approval does not exclude registration opportunities for new indications, combinations or formulations.
- Retain the user's original code for an unresolved asset. Report the scope of entity, trial and transaction queries actually executed separately; do not substitute a similarly named asset.

---

## Analysis Framework

### Pharmacodynamics (PD)

| Parameter | Description |
|-----------|-------------|
| Kd, pKd | Dissociation constant |
| Ki | Inhibitory constant |
| IC50 / EC50 | Half-maximal inhibitory/effective concentration |
| Kon / Koff | Association/dissociation rate constants |
| MoA | Mechanism of action — target's position in signaling pathways |

### Pharmacokinetics (PK) & ADMET

| Category | Parameters |
|----------|------------|
| Absorption (A) | Bioavailability, absorption rate, food effect |
| Distribution (D) | Tissue penetration, half-life, protein binding |
| Metabolism (M) | Metabolic pathways, CYP enzymes involved |
| Excretion (E) | Clearance, elimination routes (renal/hepatic) |
| Toxicity (T) | Off-target effects, safety signals |

### Safety Profile

| Category | Analysis Points |
|----------|-----------------|
| Adverse Events (AE) | Frequency, severity, grade 3/4 events |
| Special Populations | Elderly, pregnant/lactating, children, renal/hepatic impairment |
| Drug-Drug Interactions (DDI) | CYP interactions, contraindications |
| Market Withdrawal Risk | Black box warnings, REMS requirements |
| Benefit-Risk Ratio | Summary of benefit-risk assessment |

### Drug-Drug Interaction (DDI) Analysis

When DDI is part of the query, perform bidirectional analysis (Drug A → Drug B and Drug B → Drug A):

| Mechanism | Assessment |
|-----------|------------|
| CYP450 inhibition/induction | CYP1A2, 2C9, 2C19, 2D6, 3A4 — check substrate/inhibitor/inducer roles |
| Transporter interactions | P-gp, BCRP, OATP1B1/1B3 — efflux and uptake transporters |
| Pharmacodynamic | Additive/synergistic/antagonistic effects on shared targets |
| Protein binding displacement | High protein-bound drugs competing for albumin binding |

**Severity classification**: Contraindicated / Major / Moderate / Minor

### Network Pharmacology (when polypharmacology or combination rationale is requested)

Multi-target drug analysis using network proximity:
1. Map all known targets for the drug (ChEMBL, DGIdb, OpenTargets)
2. Build drug-target-disease network (STRING for PPI context)
3. Assess network proximity to disease module (shortest path distance)
4. Identify off-target effects with clinical significance
5. Rank repurposing candidates by network proximity score

### Repurposing Analysis (when requested)

**Compound-Based Repurposing Strategy:**
1. Get full target/mechanism profile (Steps 1–2)
2. Find diseases associated with those targets using `ls_web_search` (Open Targets, GWAS data)
3. Check clinical evidence in new indications: `ls_evidence_by_entity_search(evidence_type="clinical_trial", drug=[drug_name])`
4. Check deal precedents: `ls_evidence_by_entity_search(evidence_type="drug_deal", drug=[drug_name])`

**Repurposing Score (0–100):**

| Component | Weight |
|-----------|--------|
| Mechanistic rationale | 20% |
| Clinical evidence | 25% |
| Safety compatibility | 15% |
| IP/exclusivity | 15% |
| Commercial opportunity | 15% |
| Regulatory pathway clarity | 10% |

---

## Output

Analytical answers must open with:
1. Executive Summary — Drug Thesis
2. Benchmark Snapshot
3. So What / BD, R&D Decision, and R&D Team Implications

For simple factual queries, return a concise direct answer. Keep mechanism detail tied to clinical, safety, dosing, or development implications; label comparisons as head-to-head, label-based, or cross-trial.

---
