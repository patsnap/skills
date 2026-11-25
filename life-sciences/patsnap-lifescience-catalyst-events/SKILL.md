---
copyright: "Copyright © Patsnap. All rights reserved."
name: patsnap-lifescience-catalyst-events
description: Use when the user asks about upcoming or historical biopharma catalyst
  events, binary event calendars, clinical readouts, PDUFA, AdCom, filings, conference
  releases, INDs, trial starts, or event-driven company/drug risk.
license: MIT
metadata:
  author: Patsnap
  version: 1.0.0
  category: "Life Science"
---

# Catalyst Events
**Zone 1 — Tier P only.** Prioritize Patsnap MCP evidence; when key fields are missing or conflicting, verify official primary sources under the rules below.

## Writing and Output Style

Write as an analytical memo for business, BD, R&D or medical colleagues: lead with the conclusion, then evidence and reasoning. Retain necessary technical terms, drug names, endpoints and database names, while avoiding awkward word-for-word translation.

- Use concise sentences and clear judgments; avoid empty stock phrases.
- Anchor each key judgment in data, sources, applicable populations, comparators or time windows.
- Do not narrate internal work or tool status, such as "retrieval is complete" or "now analyzing."

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

This skill requires the Patsnap `pharma-intelligence` MCP service. See the [MCP setup guide](https://github.com/patsnap/skills/blob/main/life-sciences/MCP_SETUP.md) for connection and verification steps.

Search is the default evidence-gathering method. Do not call `*_fetch` merely because `*_search` was called. Further detail retrieval is unnecessary only when the results have passed entity and scope checks, contain the fields required to answer the question, and have no unresolved material conflicts.

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `ls_entity_search(entity_type="drug")` → `ls_entity_fetch(entity_type="drug")` | Retrieve relevant records and fetch details when needed |
| 2 | `ls_evidence_by_entity_search(evidence_type="clinical_trial")` → `ls_evidence_fetch(evidence_type="clinical_trial")` | Retrieve relevant records and fetch details when needed |
| 3 | `ls_evidence_by_entity_search(evidence_type="clinical_trial_result")` → `ls_evidence_fetch(evidence_type="clinical_trial_result")` | Retrieve relevant records and fetch details when needed |
| 4 | `ls_evidence_by_entity_search(evidence_type="drug_deal")` → `ls_evidence_fetch(evidence_type="drug_deal")` | Retrieve relevant records and fetch details when needed |
| 5 | `ls_entity_fetch(entity_type="organization")` | Company pipeline and event-calendar context |
| 6 | `ls_evidence_by_entity_search(evidence_type="news")` → `ls_evidence_fetch(evidence_type="news")` | Recent catalyst announcements, conference abstracts and PDUFA updates |
| 7 | `ls_evidence_by_semantic_search(source="financial_report")` | Earnings-call guidance on expected milestones (semantic search) |
| 8 | `ls_web_search` | Current PDUFA calendars, advisory committee schedules and conference abstracts (fact verification) |

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
- Record trial phase, study region, recruitment status, start date with actual/estimated designation, and registry update date separately. A global maximum phase does not establish the phase for a particular region and indication.
- "Conducted" or "started" requires actual-start evidence within the requested scope. An elapsed estimated start date does not prove initiation; if the record is stale, state that initiation remains unconfirmed. Interpret Study Start by the registry definition. Global first enrollment does not automatically establish first enrollment or first dosing at a particular country's sites.
- Verify phase, regional participation and actual initiation separately. Do not universally add requirements such as ethics approval documents; use procedural evidence as a selection criterion only when explicitly requested.
- Merge drug aliases using reliable identity mappings, but retain trials by registry identifier. Merging registrations requires a shared protocol, cross-registration or official mapping; similar names, enrollment or dates are insufficient. Combination and multi-arm trials can involve multiple assets.
- List approved scope by drug, formulation or regimen, indication, treatment line and region. Separate submission, acceptance, review, approval and launch. Count only items supported by approval evidence as approved, and distinguish announcement dates from decision dates.
- To verify current status, check labels and approval changes applicable by the query cutoff. If no approval record is retrieved for a region, mark it unverified rather than declaring the indication unapproved.
- Check regulatory requirements by region, indication and pathway. One project failure, withdrawal or immature endpoint does not establish a universal approval threshold for a drug class. Existing marketing approval does not exclude registration opportunities for new indications, combinations or formulations.
- For future events, record the expected window, guidance source and disclosure date. After that window passes, check updates and distinguish confirmed delay, disclosed results and unresolved status. A regulatory target date, meeting schedule or study completion date does not guarantee approval or results publication on that date.

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
