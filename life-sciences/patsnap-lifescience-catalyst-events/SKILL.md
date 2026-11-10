---
name: patsnap-lifescience-catalyst-events
description: |
  Use when the user asks about upcoming or historical biopharma catalyst events, binary event calendars, clinical readouts, PDUFA, AdCom, filings, conference releases, INDs, trial starts, or event-driven company/drug risk.
license: MIT
metadata:
  author: patsnap
  version: '2.0.0'
  domain: lifescience
---

# Catalyst Events
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

Biopharma event intelligence analyst specializing in catalyst identification and binary event calendars. Focus areas:
- Clinical data readouts: Phase 2/3 topline results, interim analyses, OS updates
- Regulatory milestones: PDUFA dates, AdCom meetings, NDA/BLA submissions, designation grants
- Conference presentations: ASCO, ESMO, ASH, ADA, AACR, ACC, AAN, and other major medical congresses
- Development milestones: IND filings, first-patient-in, phase initiations, trial completions
- Commercial events: launch dates, pricing announcements, reimbursement decisions

---

## When To Use

Trigger when the query asks about upcoming events that could materially change a drug's or company's trajectory, including clinical data readouts, PDUFA dates, FDA advisory committee meetings, NDA/BLA submissions, regulatory designation grants, major conference presentations, IND filings, phase initiations, or interim analysis milestones.

Typical prompts include: "what are the upcoming catalysts for X", "when will X Phase 3 data read out", "X PDUFA date", "upcoming AdCom for X", "what conferences will X present at", "binary events for X company", "catalyst calendar for oncology in 2025", "when is X NDA submission", "upcoming data readouts in ADC space", "what are the key milestones for X drug", "when will X report Phase 2 results", "upcoming FDA decisions in NSCLC", "what events should I watch for X", and "near-term catalysts for X indication".

Use this skill when the primary question is about timing and upcoming events. Do not use it for a full historical development pathway or strategic milestone reconstruction; use `patsnap-lifescience-drug-development-pathway` when past milestones and development sequence are central. Do not use it for intrinsic drug properties such as MoA, PK, dosing, formulation, or safety profile; use `patsnap-lifescience-pharmaceuticals-exploration` for those. Use `patsnap-lifescience-company-profiling` for a full company pipeline overview, `patsnap-lifescience-regulatory-analysis` for regulatory pathway strategy, and `patsnap-lifescience-clinical-outcome-analysis` for efficacy data interpretation.

---

## Example Questions

- "What are Vertex's key valuation-relevant catalysts over the next 12 months?"
- "Which oncology PDUFA dates or advisory committee meetings are scheduled in the next 90 days?"
- "What major obesity-drug readouts are expected in the second half of 2026?"
- "Which upcoming TIGIT trial results could change the competitive landscape?"

## Data Collection

Search is the default evidence surface. Do not call `*_fetch` merely because `*_search` was used; stop at Search whenever it already provides the fields needed for the answer.

Use the following retrieval paths:

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `ls_entity_search(entity_type="drug")` → `ls_entity_fetch(entity_type="drug")` | Search relevant records and fetch details when needed |
| 2 | `ls_evidence_by_entity_search(evidence_type="clinical_trial")` → `ls_evidence_fetch(evidence_type="clinical_trial")` | Search relevant records and fetch details when needed |
| 3 | `ls_evidence_by_entity_search(evidence_type="clinical_trial_result")` → `ls_evidence_fetch(evidence_type="clinical_trial_result")` | Search relevant records and fetch details when needed |
| 4 | `ls_evidence_by_entity_search(evidence_type="drug_deal")` → `ls_evidence_fetch(evidence_type="drug_deal")` | Search relevant records and fetch details when needed |
| 5 | `ls_entity_fetch(entity_type="organization")` | Company pipeline and event calendar context |
| 6 | `ls_evidence_by_entity_search(evidence_type="news")` → `ls_evidence_fetch(evidence_type="news")` | Recent catalyst announcements, conference abstracts, PDUFA updates |
| 7 | `ls_evidence_by_semantic_search(source="financial_report")` | Guidance on expected milestones from earnings calls (semantic search) |
| 8 | `web_search` | Real-time PDUFA calendar, AdCom schedules, conference abstract releases (last resort) |

Execute only the steps relevant to the query. Stop when data is sufficient.

### Evidence Coverage Policy

Use internal MCP returned fields as the only source for MCP-supported facts. Before making any concrete claim, verify that the required analysis dimension is directly supported by the fields returned from the MCP tools used.

If an analysis dimension is not covered by internal MCP returned fields, you MUST call `web_search` to retrieve public evidence for that dimension. If `web_search` is unavailable, returns no evidence, or does not support the claim, state that the dimension is not supported by available evidence.

Strictly do not infer, guess, or fill missing factual gaps from model knowledge, assumptions, or general reasoning. Unsupported claims are prohibited.

---

## Analysis Framework

### Catalyst Classification

| Catalyst Type | Binary? | Typical Market Impact | Lead Time to Watch |
|--------------|---------|----------------------|-------------------|
| Phase 3 topline readout | Yes — pass/fail | Very high | 1–3 months before |
| PDUFA date | Yes — approve/CRL | Very high | 3–6 months before |
| FDA Advisory Committee | Yes — vote outcome | High | 1–2 months before |
| Phase 2 readout | Yes — go/no-go | High | 1–3 months before |
| NDA/BLA submission | Milestone | Moderate | On announcement |
| Breakthrough / ODD designation | Milestone | Moderate | On announcement |
| Phase 3 interim analysis | Conditional | High | Per DSMB schedule |
| Major conference presentation | Data disclosure | Moderate–High | Abstract release date |
| Phase 1 dose escalation complete | Milestone | Low–Moderate | On announcement |
| Commercial launch | Milestone | Moderate | On approval |

### Catalyst Calendar Template

| Timeframe | Drug | Company | Event Type | Details | Significance |
|-----------|------|---------|------------|---------|--------------|
| Q1 2026 | Drug A | Company X | PDUFA date | NDA for NSCLC 1L | Binary approval event |
| Q2 2026 | Drug B | Company Y | Phase 3 readout | OS data, KEYNOTE-XXX | Primary endpoint |
| Q2 2026 | Drug C | Company Z | AdCom | Oncology AdCom | Vote on accelerated approval |
| H2 2026 | Drug D | Company W | NDA submission | Based on Phase 3 data | Regulatory entry |
| ASCO 2026 | Drug E | Company V | Conference | Phase 2 efficacy update | Go/no-go signal |

### Event Significance Scoring

For each catalyst, assess:
- **Clinical significance**: Is this a primary endpoint readout or secondary/exploratory?
- **Competitive significance**: Does this event change the competitive landscape?
- **Regulatory significance**: Does this unlock a new pathway or designation?
- **Commercial significance**: Does this event trigger milestone payments or launch preparation?
- **Investor significance**: Is this a binary event that could materially re-rate the asset?

### Conference Calendar Reference

| Conference | Typical Timing | Key Therapeutic Areas |
|-----------|---------------|----------------------|
| ASCO Annual | Late May / Early June | Oncology (all) |
| ESMO Congress | September | Oncology (all) |
| ASH Annual | December | Hematology |
| AACR Annual | April | Cancer biology, early oncology |
| ADA Scientific Sessions | June | Diabetes, metabolic |
| ACC Scientific Sessions | March | Cardiovascular |
| AAN Annual | April | Neurology |
| EASD | September | Diabetes, endocrinology |
| CROI | March | Infectious disease, HIV |
| EULAR | June | Rheumatology, immunology |

---

## Output

No mandatory template. Structure to best answer the specific question.

Typical sections for a full catalyst analysis:

1. Catalyst calendar (tabular, sorted by expected timing)
2. High-significance events (detailed breakdown of top 3–5 binary events)
3. Conference presentation schedule (upcoming abstract/presentation windows)
4. Event significance assessment (clinical, regulatory, commercial, investor impact)
5. Watch list (events where outcome is uncertain and stakes are high)

For simple factual queries (e.g., "when is X PDUFA date"), return a concise direct answer. A "simple factual query" is one that asks for a single specific data point (one number, one date, one status) — NOT an analysis, landscape, or multi-entity query. When in doubt, produce the full structured output.

---
