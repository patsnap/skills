---
name: patsnap-lifescience-deal-intelligence
description: |
  Use when the user asks about biopharma deals, licensing, M&A, strategic partnerships, co-development, deal terms, valuation, royalties, milestones, comparable deals, or industry deal trends.
license: MIT
metadata:
  author: patsnap
  version: '2.0.0'
  domain: lifescience
---

# Deal Intelligence
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

Search is the default evidence surface. Do not call `*_fetch` merely because `*_search` was used; stop at Search whenever it already provides the fields needed for the answer.

Use the following retrieval paths:

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `ls_evidence_by_entity_search(evidence_type="drug_deal")` → `ls_evidence_fetch(evidence_type="drug_deal")` | Search relevant records and fetch details when needed |
| 2 | `ls_evidence_by_entity_search(evidence_type="drug_deal")` | Find representative or decision-critical deal records by drug, company, or indication |
| 2b | `ls_evidence_fetch(evidence_type="drug_deal")` | Get deal details, terms, financials |
| 3 | `ls_entity_search(entity_type="drug")` → `ls_entity_fetch(entity_type="drug")` | Search relevant records and fetch details when needed |
| 4 | `ls_entity_fetch(entity_type="organization")` | Partner company profiles |
| 5 | `ls_patent_search` → `ls_patent_fetch` | IP portfolio being licensed |
| 6 | `ls_evidence_by_semantic_search(source="financial_report")` | Counterparty financial health (semantic search) |
| 7 | `ls_evidence_by_entity_search(evidence_type="news")` → `ls_evidence_fetch(evidence_type="news")` | Recent deal announcements |
| 8 | `web_search` | SEC filings (8-K), analyst commentary, comparable benchmarks (last resort) |

Execute only the steps relevant to the query. Stop when data is sufficient.

### Evidence Coverage Policy

Use internal MCP returned fields as the only source for MCP-supported facts. Before making any concrete claim, verify that the required analysis dimension is directly supported by the fields returned from the MCP tools used.

If an analysis dimension is not covered by internal MCP returned fields, you MUST call `web_search` to retrieve public evidence for that dimension. If `web_search` is unavailable, returns no evidence, or does not support the claim, state that the dimension is not supported by available evidence.

Strictly do not infer, guess, or fill missing factual gaps from model knowledge, assumptions, or general reasoning. Unsupported claims are prohibited.

---

## Analysis Framework

### Deal Terms Breakdown

| Component | Value | Notes |
|-----------|-------|-------|
| Upfront Payment | $XXM | Cash at signing |
| Development Milestones | $XXM | By phase (Phase 1/2/3/NDA) |
| Sales Milestones | $XXM | By revenue threshold |
| Royalties | X% | Tiered by sales band |

### Phase-Based Deal Value Benchmarks

| Phase at Deal | Typical Upfront | Typical Total |
|---------------|-----------------|---------------|
| Preclinical | $10–50M | $200M–1B |
| Phase 1 | $25–150M | $500M–2B |
| Phase 2 | $50–500M | $1–5B |
| Phase 3 | $200M–2B | $2–10B |
| Approved | $500M–5B+ | $2–20B+ |

### Key Valuation Metrics

| Metric | Description |
|--------|-------------|
| Upfront / Total ratio | Risk-sharing structure; higher % = buyer confidence |
| Implied peak sales | Back-calculate from royalty economics (royalty rate × peak sales) |
| Cost per phase transition | Normalize deal value by development stage |
| Milestone structure | Clinical vs regulatory vs commercial milestone weighting |
| Royalty tiers | Tiered rates by sales threshold; compare to indication benchmarks |

### BD Partner Identification — Portfolio Redundancy Filter

Apply this filter whenever the query asks about potential BD partners, out-licensing targets, or in-licensing candidates for a specific drug asset.

**Core Logic**: Large pharma companies rarely engage in BD transactions for assets that overlap with an existing internal pipeline asset or marketed product targeting the same biological mechanism or protein.

**Execution Steps**:

| Step | Action |
|------|--------|
| 1. Target Identification | Clearly identify the target (e.g., PD-L1, GLP-1, BTK) and MoA of the candidate asset |
| 2. Portfolio Conflict Check | Use `ls_entity_search(entity_type="drug")` to cross-reference the target against each potential partner's pipeline and commercial portfolio |
| 3. Exclude / Deprioritize | If a company already has a leading or mid-stage asset for that target → classify as **Low Probability** (strategic redundancy, internal cannibalization risk) |
| 4. Identify Gaps | Prioritize companies with clear TA interest but no competitive asset for that specific target or pathway |
| 5. Transparency | Explicitly state in output if a major player was excluded from the Top Tier list due to an overlapping asset |

**Partner Tier Classification**:

| Tier | Criteria |
|------|----------|
| Top Tier | TA strategic fit + no overlapping target asset |
| Mid Tier | TA fit + early/weak overlap (preclinical only) |
| Low Probability | Existing mid/late-stage or approved asset on same target |

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
