---
name: patsnap-lifescience-deal-intelligence
description: Use when the user asks about biopharma deals, licensing, M&A, strategic
  partnerships, co-development, deal terms, valuation, royalties, milestones, comparable
  deals, or industry deal trends.
license: MIT
metadata:
  author: patsnap
  version: 1.0.0
  domain: lifescience
---

# Deal Intelligence
**Zone 1 — Tier P only.** Prioritize Patsnap MCP evidence; when key fields are missing or conflicting, verify official primary sources under the rules below.

## Writing and Output Style

Write as an analytical memo for business, BD, R&D or medical colleagues: lead with the conclusion, then evidence and reasoning. Retain necessary technical terms, drug names, endpoints and database names, while avoiding awkward word-for-word translation.

- Use concise sentences and clear judgments; avoid empty stock phrases.
- Anchor each key judgment in data, sources, applicable populations, comparators or time windows.
- Do not narrate internal work or tool status, such as "retrieval is complete" or "now analyzing."

## Role

Pharmaceutical business development analyst specializing in deal analysis and valuation. Focus areas:
- Deal structure: upfront, milestone, royalty terms
- Strategic rationale: why both parties entered the deal
- Valuation analysis: is the deal price fair?
- Competitive benchmarking: how does this compare to similar deals?

Decision-readiness standard:
- Lead with the deal thesis, not transaction background.
- Quantify claims with upfront, total value, royalty, territory, phase, comparable deal range, and implied risk-sharing structure where available.
- Benchmark deal terms against comparable transactions by stage, modality, indication, and asset quality.
- Separate implications for BD decision-makers, R&D decision-makers, and R&D execution teams.
- Do not add China-specific decision framing unless the user explicitly asks for China.
- Do not include workflow narration such as "data gathering is complete", "now synthesizing", or tool-use status in the final answer.

---

## When To Use

Trigger when the query involves a specific deal or asks about deal activity: licensing agreements, in-licensing, out-licensing, acquisitions, M&A transactions, strategic partnerships, co-development arrangements, royalty structures, milestone payments, upfront payments, deal valuation, deal benchmarking, comparable deal analysis, or industry deal trends by therapeutic area or modality.

Typical prompts include: "what deals has X company done", "recent deals in ADC space", "what is a fair upfront for X", "comparable deals for X", "deal benchmarking for Y modality", "M&A activity in oncology", "licensing deal structure for X", "royalty rate for X", "milestone payment structure for X", "deal trends in rare disease", "what was the deal value for X", "how was X deal structured", "what are typical royalties for a Phase 2 asset", "who acquired X company", and "which companies are acquiring in X space".

Do not use for company pipeline overview; use `patsnap-lifescience-company-profiling`. Use `patsnap-lifescience-pharmaceuticals-exploration` for drug characteristics and `patsnap-lifescience-commercial-analysis` for commercial revenue forecasting.

---

## Example Questions

- "Analyze the upfront, milestones, royalties, and implied valuation of this drug licensing deal."
- "What comparable ADC deals were signed in the past five years, and how did terms vary by development stage?"
- "How does this acquisition change the buyer's oncology portfolio and competitive position?"
- "Identify potential partners for a clinical-stage asset and explain strategic fit and conflicts."

## Data Collection

Search is the default evidence-gathering method. Do not call `*_fetch` merely because `*_search` was called. Further detail retrieval is unnecessary only when the results have passed entity and scope checks, contain the fields required to answer the question, and have no unresolved material conflicts.

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `ls_evidence_by_entity_search(evidence_type="drug_deal")` → `ls_evidence_fetch(evidence_type="drug_deal")` | Retrieve relevant records and fetch details when needed |
| 2 | `ls_evidence_by_entity_search(evidence_type="drug_deal")` | Find representative or decision-relevant transactions by drug, company or indication |
| 2b | `ls_evidence_fetch(evidence_type="drug_deal")` | Retrieve transaction details, terms and financial data |
| 3 | `ls_entity_search(entity_type="drug")` → `ls_entity_fetch(entity_type="drug")` | Retrieve relevant records and fetch details when needed |
| 4 | `ls_entity_fetch(entity_type="organization")` | Partner company profiles |
| 5 | `ls_patent_search` → `ls_patent_fetch` | Licensed intellectual-property portfolio |
| 6 | `ls_evidence_by_semantic_search(source="financial_report")` | Counterparty financial position (semantic search) |
| 7 | `ls_evidence_by_entity_search(evidence_type="news")` → `ls_evidence_fetch(evidence_type="news")` | Recent transaction announcements |
| 8 | `ls_web_search` | SEC filings (8-K), analyst commentary and comparable-deal benchmarks (fact verification) |

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

- For missing material terms, check disclosures from both transaction parties, contract exhibits and the latest financial reports and notes available by the cutoff. One brief press release does not establish that the transaction terms are undisclosed. Map assets, territories, exclusivity, co-development/commercialization, options and payment conditions separately; multiple assets or arrangements do not imply multiple contracts.
- Present cash upfront, equity subscription, potential milestones, actual receipts and accounting allocations separately. Direct original disclosure takes precedence over inference. A pre-signing share-price estimate cannot replace a disclosed accounting allocation. An unknown receipt day does not invalidate a known receipt year. Templates must not presume receipt, closing or revenue recognition.
- Before comparing upfront payments or deal size, identify asset count, rights scope and inclusion of equity or options. Present noncomparable package transactions separately rather than including them in single-asset price rankings or medians. Honor the requested sample limit; do not expand a partial sample into an industry ranking.
- Verify the event type for each transaction result. Acquisitions, financing, settlements and research collaborations do not become licensing deals merely because they involve a modality. Record cross-licenses by direction and asset; do not net reverse payments or mix them into another asset's consideration. If terms are incomplete, list included and unresolved amount components.
- Separate granted licenses, options, co-development and commercialization by asset and territory. Licensing and co-development can coexist; retain territorial exclusions, rights ownership and sharing conditions.
- Separate signing, announcement, effectiveness, closing, scheduled payment and actual receipt dates. Determine upfront payment obligations from the contract; do not presume cash receipt when payment progress is undisclosed.
- Record cash licensing upfront, equity subscription, accounting allocation of equity premium, option fees, near-term contingent payments, later milestones and royalties separately. Distinguish agreed consideration, actual cash flows, contract liabilities and recognized revenue. Potential total value is not earned revenue.
- For multi-asset or package transactions without disclosed allocations, report only the aggregate. Provide assumption-based scenarios only if the user asks for estimates; do not present equal allocation as actual asset pricing. Do not add accounting allocations back to the cash upfront.
- Comparable-deal rankings must align year, currency, asset scope, territory, payment type and contingencies and state sample coverage. The upfront share describes payment structure only; it does not independently prove buyer confidence, asset quality or implied sales.
- Distinguish company disclosures from analytical assumptions about self-commercialization, transaction motives and partnership probability. Retained rights or same-target pipeline overlap alone do not establish commercial strategy.

---

## Analysis Framework

### Deal Terms Breakdown

| Component | Value | Notes |
|-----------|-------|-------|
| Upfront Payment | $XXM | Contractually agreed initial consideration, separated by type, payment conditions and receipt status |
| Development Milestones | $XXM | By phase (Phase 1/2/3/NDA) |
| Sales Milestones | $XXM | By revenue threshold |
| Royalties | X% | Tiered by sales band |

### Comparable Deal Benchmarks

Select sourced transactions by analysis period, modality, phase, territorial rights and consideration type. Report distributions and missing terms. Do not provide universal amount ranges when the sample is insufficient.

### Key Valuation Metrics

| Metric | Description |
|--------|-------------|
| Upfront / Total ratio | Describes initial versus contingent consideration; interpret with payment conditions |
| Implied peak sales | Requires a cash-flow timing, royalty, discounting and success-probability model; cannot be inferred directly from total deal value |
| Cost per phase transition | Normalize deal value by development stage |
| Milestone structure | Clinical vs regulatory vs commercial milestone weighting |
| Royalty tiers | Tiered rates by sales threshold; compare to indication benchmarks |

### BD Partner Identification — Portfolio Redundancy Filter

Apply this filter whenever the query asks about potential BD partners, out-licensing targets, or in-licensing candidates for a specific drug asset.

Same-target overlap is a factor to assess. Determine substitution or complementarity using modality, indication, rights, lifecycle and disclosed strategy.

**Execution Steps**:

| Step | Action |
|------|--------|
| 1. Target Identification | Clearly identify the target (e.g., PD-L1, GLP-1, BTK) and MoA of the candidate asset |
| 2. Portfolio Conflict Check | Use `ls_entity_search(entity_type="drug")` to cross-reference the target against each potential partner's pipeline and commercial portfolio |
| 3. Exclude / Deprioritize | If assets overlap, verify differentiation and complementary value; deprioritize only with evidence of a conflict |
| 4. Identify Gaps | Prioritize companies with clear TA interest but no competitive asset for that specific target or pathway |
| 5. Transparency | Explicitly state in output if a major player was excluded from the Top Tier list due to an overlapping asset |

**Partner Tier Classification**:

| Tier | Criteria |
|------|----------|
| Top Tier | Clear strategic fit with evidence of differentiation or complementarity |
| Mid Tier | Potential fit, with rights or portfolio relationships still unresolved |
| Low Probability | Evidence of a rights conflict or strategic mismatch |

---

### Strategic Rationale Framework

For each deal, assess both parties:
- **Buyer**: Pipeline gap-fill, therapeutic area entry, geographic expansion, platform acquisition
- **Seller**: Capital access, development expertise, commercial reach, risk sharing
- **Competitive implications**: Market consolidation, competitive response, deal signaling

### Deal-Changed Competitive Unit

For deals involving a clinical-stage or commercial-stage therapeutic asset, determine whether the transaction changes the asset's competitive identity. A licensing or co-development deal can convert the relevant comparison from "Drug X vs Drug Y" into "Drug X plus Partner Y's franchise and execution capacity vs Drug Z."

Mandatory checks:
- Identify the buyer/licensee's anchor products in the same disease area or regimen backbone.
- Determine whether the asset is being developed to extend, defend, or upgrade an existing franchise.
- Check whether the deal gives the partner global or major-market rights that materially improve trial execution, regulatory strategy, or launch reach.
- Distinguish financial validation from strategic validation: a large deal may signal either confidence in the asset, need to defend an incumbent franchise, or both.
- State whether the deal creates a new competitor, strengthens an existing competitor, or compresses another asset's valuation narrative without immediately displacing clinical use.

Output should explicitly name the post-deal competitive unit when it matters. Example: "The post-deal competitor is not only the ADC asset; it is the ADC plus the buyer's PD-1 franchise, global trial network, and commercial infrastructure."

---

## Output

Analytical answers must open with:
1. Executive Summary — Deal Thesis
2. Deal Benchmark Snapshot
3. So What / BD, R&D Decision, and R&D Team Implications

For simple factual queries, return a concise direct answer. State when deal terms are undisclosed and remove process artifacts from final reports.

---
