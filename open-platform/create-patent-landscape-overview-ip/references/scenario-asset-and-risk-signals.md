# Scenario: Patent Asset and Risk Signals

Use this scenario to surface dated patent-asset indicators, legal-status or legal-event signals, transaction clues, and items requiring specialist follow-up. This is research triage, never a legal opinion.

## Use for questions such as

- Which families show stronger asset indicators under a transparent rubric?
- Which records may warrant monitoring, transaction diligence, or counsel review?
- Are transfers, licenses, security interests, challenges, litigation-related events, customs records, or awards available?
- How should risk and asset signals be reported without overstating them?

## Required inputs

| Input | Requirement |
|---|---|
| `candidate_pool` | Cleaned population or curated package |
| `asset_goal` | Monitoring, transaction screening, portfolio review, risk triage, or challenge watch |
| `jurisdiction_scope` | Required because event meaning and coverage vary by jurisdiction |
| `data_cutoff` | Required for every status or event statement |
| `legal_opinion_allowed` | Always `false` for this skill |
| `signal_rubric` | Optional; define dimensions, missing-data treatment, and thresholds |

## Global PatSnap capabilities

Use `patent_briefing`, `deep_patent_mining`, or `global_core_patent_database` for selected-record family, citation, legal-status, and event evidence only where the installed contracts expose those data. `advanced_patent_search` may support candidate retrieval and filters. Verify operation names and returned fields at runtime. A missing field or event is “not available in the retrieved data,” not proof that no event exists.

## Signal catalogue

| Signal | Appropriate interpretation |
|---|---|
| Legal status | Dated database status requiring jurisdiction-specific verification |
| Legal event | Recorded event for follow-up, not a legal conclusion |
| Opposition, reexamination, or invalidation event | Challenge-related clue requiring counsel and official-register verification |
| Assignment or transfer | Ownership-change clue; verify parties, date, and recordation scope |
| License | Access or commercialization clue; terms may be incomplete or unavailable |
| Security interest or pledge | Financing/encumbrance clue; legal effect varies |
| Customs or border record | Enforcement-related clue under the relevant regime |
| Award or recognition | Non-dispositive recognition signal |
| Family coverage | Geographic filing proxy under a declared family definition |
| Forward citations | Dated influence/attention proxy affected by age and citation practice |
| Remaining term estimate | Screening proxy only; requires jurisdiction and event verification |

## Analysis flow

1. Start from a deduplicated, traceable candidate set.
2. Define the decision goal and jurisdiction-specific data boundary.
3. Collect available value indicators such as family coverage, citation signal, technical centrality, decision relevance, owner type, status, and an explicitly qualified remaining-term proxy.
4. Collect dated legal and asset events where supported.
5. Preserve source, event date, retrieval date, jurisdiction, and missing-data state.
6. Apply a transparent rubric or descriptive buckets; do not convert proxies into a single false-precision “patent value.”
7. Separate business, technical, data-quality, and legal follow-up.
8. Write signal language and name the verification step.

## Report blocks

| Block | Content |
|---|---|
| Signal method | Dimensions, sources, jurisdiction coverage, cutoff, and missing-data policy |
| Candidate signal table | Record, signal, evidence, qualification, and next action |
| Asset-movement clues | Assignments, licenses, security interests, or other available events |
| Legal-event clues | Status, challenges, proceedings, or other dated events |
| Follow-up queues | Business, technical, data verification, and counsel review |
| Limitations | Coverage gaps and non-legal-opinion statement |

Prefer a transparent evidence table or patent × signal matrix. If a ranking is requested, expose criteria and avoid implying that unlike signals are commensurate. Show unavailable values distinctly from negative values.

## Safe language

Use formulations such as:

- “a legal-event signal recorded as of [date]”;
- “an ownership or asset-movement clue requiring verification”;
- “a candidate for follow-up counsel review”;
- “an input to a later FTO, validity, or transaction-diligence process”; and
- “worth monitoring under the stated rubric.”

Do not state that a patent is infringing, non-infringing, valid, invalid, enforceable, standards-essential, or sufficient for freedom to operate. Do not recommend purchase, licensing, enforcement, abandonment, or design-around action as a final decision.

## Quality gate

- Every signal identifies source, jurisdiction where relevant, event/status date, and retrieval cutoff.
- Missing data are marked unavailable rather than absent.
- Proxy definitions and ranking criteria are visible.
- Conflicting records and official-register verification needs are disclosed.
- Business, technical, and legal actions remain separate.
- No confidential source examples or China-only event assumptions remain.

## Signal-record schema

| Field | Requirement |
|---|---|
| `record_id` | Traceable publication, application, or family identifier |
| `signal_type` | Controlled event or proxy category |
| `jurisdiction` | Office or legal system to which the signal relates |
| `event_date` | Date supplied by the source, with precision noted |
| `status_as_of` | Applicable as-of date |
| `source` | Database operation, official register, or other cited source |
| `retrieved_at` | Data cutoff |
| `observation` | Factual source-grounded statement |
| `interpretation` | Bounded significance, labeled as inference where needed |
| `verification` | Official-register, counsel, ownership, or transaction check |
| `next_action` | Business, technical, data, or legal queue |

### Data and scoring checks

1. Normalize neither event terminology nor legal status across jurisdictions without a documented mapping.
2. Distinguish recorded assignment from current beneficial ownership.
3. Distinguish application status, claim status, and family-level summaries.
4. Age-normalize or qualify citation comparisons.
5. Check whether missing event data reflect connector coverage.
6. Expose weights, thresholds, and missing-value treatment for any score.
7. Test the ranking after removing each high-weight proxy to identify fragility.
8. Preserve conflicting records and the source priority used for display.

### Escalation matrix

| Queue | Examples |
|---|---|
| Business | Monitoring priority or transaction-context research |
| Technical | Claim/description reading or route relevance validation |
| Data quality | Entity resolution, event reconciliation, or official-register check |
| Counsel | FTO, validity, ownership, enforceability, term, or transaction advice |

### Handoff artifacts

Deliver the signal table, source/cutoff record, rubric, missing-data map, conflict log, and separated follow-up queues. Preserve enough context for counsel or IP operations to verify the signal independently; do not hand off only a color-coded score.

## Additional legal-boundary checks

- Confirm that “active” means the source’s recorded status, not a conclusion about every claim.
- Avoid calculating term without jurisdiction-specific priority, filing, adjustment, extension, disclaimer, and fee-event review.
- Treat a license record as incomplete unless parties, scope, effective date, and recordation basis are available.
- Treat assignment recordation as an ownership clue rather than proof of all contractual rights.
- Do not infer encumbrance priority or release from a security-interest record alone.
- Do not treat an opposition or invalidation event as the final outcome without the current decision record.
- Distinguish litigation, administrative, customs, and transactional sources.
- Date every statement that can change.
- Use official registers and qualified counsel for dispositive follow-up.
- Retain the original event wording where legally meaningful, with an English explanation rather than an unqualified paraphrase.
