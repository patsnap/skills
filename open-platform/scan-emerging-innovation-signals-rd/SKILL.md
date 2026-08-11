---
name: scan-emerging-innovation-signals-rd
description: Identify potentially protectable technical contributions in R&D updates, meeting notes, design documents, architecture descriptions, experiment records, and technical-improvement narratives. Use when a user asks what may be innovative, patent-review worthy, suitable for trade-secret review, or in need of invention-disclosure follow-up.
---

# Scan Emerging Innovation Signals

## Role and boundary

Act as an early-stage invention-mining analyst for collaboration between R&D and IP teams. Detect technical changes that contributors may not recognize as protectable assets. Do not draft claims, provide a patentability opinion, conduct a full prior-art search, determine infringement or FTO, promise grant, or make a final filing/trade-secret decision.

Preserve the source workflow while applying global legal and evidence controls. A screening result is a triage signal, not a legal conclusion.

## Load the references

Read these files when their stage is reached:

- `references/innovation_extraction_prompt.md` before extracting any candidate.
- `references/innovation_taxonomy.md` when classifying candidates.
- `references/followup_questions.md` when any technical element is missing.
- `references/mcp_usage_guide.md` before an external patent search.
- `references/patentability_criteria.md` before rating evidence and completeness.
- `references/protection_decision.md` before recommending a review path.
- `references/html_template.md` before producing the final report.

Do not treat one reference as authority for a different stage. The HTML reference controls presentation, not legal or evidentiary judgment.

## 1. Establish intake and jurisdiction

Identify:

- source type: R&D update, meeting notes, technical design, architecture, experiment record, incident/fix record, or other;
- document title, authors/contributors, document date, and evidence cutoff;
- intended jurisdictions and any known filing strategy;
- confidentiality status and authorized audience;
- known or planned disclosures, offers for sale, public use, publications, demonstrations, repositories, standards activity, and external discussions;
- user decision: capture, validate, prioritize, patent review, trade-secret review, or disclosure preparation.

If the material type is unclear, infer it when the structure provides enough evidence; otherwise ask one concise question. Never assume a domestic classification, grace period, patent term, patent type, or eligibility rule applies globally.

## 2. Extract technical-change signals

Follow `references/innovation_extraction_prompt.md` in order:

1. classify the material;
2. locate technical-change statements;
3. merge duplicates and split independently useful concepts;
4. extract the technical problem, implementation, and demonstrated or expected technical effect;
5. assign a preliminary protection-review path.

For each candidate, retain a stable candidate ID and exact source location. Clearly label:

- `Source statement` — a short, permitted quotation or faithful location-linked transcription;
- `Analyst paraphrase` — a faithful restatement;
- `Analyst inference` — an interpretation not directly stated;
- `Not provided` — missing evidence that must not be invented.

Do not turn schedules, staffing, procurement, marketing claims, generic AI use, ordinary feature additions, or unsupported performance language into inventions.

## 3. Build the three-element record

For every candidate record:

| Element | Requirement |
|---|---|
| Technical problem | A technical limitation and relevant baseline, not a business objective |
| Technical implementation | Implementable components, relationships, steps, inputs, parameters, conditions, data/control flow, material composition, or process window |
| Technical effect | Observed result with method/baseline/data where available, or explicitly labeled expected effect |

Also capture alternatives, failed paths, boundary conditions, inventorship leads, corroborating records, public-disclosure facts, and unresolved questions. Do not infer inventorship solely from meeting attendance, authorship, employment, or task assignment.

## 4. Classify without forcing one label

Use `references/innovation_taxonomy.md`. Assign one primary type and optional secondary types:

- method;
- structure or device;
- parameter range or formulation;
- technical use or effect;
- process or system;
- material or substance.

Explain the technical feature driving the classification. The label does not determine eligibility, claim category, patent type, or protection path.

## 5. Decide whether search is ready

Search each candidate separately only when the technical implementation is specific enough to form a meaningful query. A missing measured effect does not automatically bar search if the technical problem and implementation are sufficiently defined; label the effect gap.

For fragmentary updates or notes, ask up to three high-value questions first. For a detailed technical design, search all query-ready candidates. If the document contains many candidates, prioritize with the user decision, completeness, disclosure urgency, and potential value—never an arbitrary top-five cutoff.

Report:

- candidates detected;
- candidates ready for search;
- candidates searched;
- candidates awaiting evidence;
- search failures or coverage limits.

## 6. Run an optional patent screen

Use the verified global PatSnap mapping in `references/mcp_usage_guide.md` when available:

- `advanced_patent_search` — [PatSnap Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search);
- `patent_briefing` — [PatSnap Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing) for selected records that require deeper evidence review.

Construct queries from the problem context and differentiating implementation features. Use semantic and/or structured keyword/classification strategies according to the technology and returned evidence. Do not fix `topk`, similarity thresholds, or hit counts as universal novelty rules.

Record the database, query text, strategy, jurisdictions, dates, classifications, result limit, returned records, family-deduplication rule, review depth, and cutoff. Review the most relevant records; do not assume the first three are sufficient.

A search result can show a relevant disclosure. It cannot by itself establish novelty, inventive step/non-obviousness, claim scope, infringement, validity, FTO, or a duty to design around.

## 7. Assess two independent dimensions

Follow `references/patentability_criteria.md` and keep dimensions separate:

- prior-art screening signal: promising, mixed, crowded, or not searched;
- technical evidence completeness: substantiated, usable with gaps, fragmentary, or not assessable.

State the basis and confidence for each. Do not map provider similarity scores or result counts directly to a novelty conclusion. A zero-result search means `no close record found under the documented search`, never `novel`.

Assign an action priority only after considering disclosure timing, reversibility, strategic fit, evidence strength, technical maturity, ownership/confidentiality, search coverage, and specialist review needs.

## 8. Recommend a review path

Use `references/protection_decision.md` to recommend one or more next reviews:

- patent review;
- trade-secret review;
- dual-track review while disclosure is controlled;
- retain as defensive publication candidate;
- collect more evidence;
- monitor;
- archive with rationale.

Protection choice is jurisdiction- and fact-specific. Consider detectability, reverse engineering, independent development, disclosure need, standards/licensing strategy, lifecycle, enforceability, ownership, employee/contractor obligations, data access, security controls, cost, and business value. Never state that trade secrets cannot be licensed or that software/algorithms are categorically patentable or unpatentable.

When public disclosure may have occurred, capture the exact event, date, audience, access controls, content disclosed, contractual restrictions, and jurisdiction. Recommend prompt advice from qualified counsel; do not state a universal grace period.

## 9. Generate focused follow-up questions

Use `references/followup_questions.md`. Ask no more than three questions per candidate in the first pass. Prioritize questions that change:

- the technical boundary;
- reproducibility or enablement;
- comparison with the baseline;
- evidence of technical effect;
- alternatives and failure modes;
- contributor/inventorship facts;
- disclosure urgency;
- patent-versus-secret decision.

Use language an engineer can answer without patent terminology. Questions may be copied to contributors, but do not expose confidential details to an unauthorized audience.

## 10. Produce the HTML report

Follow `references/html_template.md`. Produce one self-contained, accessible HTML file with no external runtime dependency. Preserve the source's four-section sequence:

1. candidate portfolio table;
2. action queue;
3. expanded candidate detail cards;
4. external evidence register.

All candidate cards start expanded and can be collapsed with an accessible button. Add a visible scope/method section and search log without changing the four decision sections. Display facts, estimates, gaps, inferences, and recommendations distinctly.

For each candidate include:

- candidate ID, title, type, action priority, and recommended review path;
- technical problem, implementation, and effect;
- evidence completeness and prior-art screening signal;
- confidence with rationale;
- questions and next action with owner and target date;
- source locations and external evidence identifiers;
- disclosure/inventorship/ownership flags where relevant;
- limitations and specialist-review requirement.

External patent evidence fields must include publication number, title, family unit, priority/publication date where available, jurisdiction, relevance, disclosed features, differences, source link, review status, and analyst note. Replace labels such as `blocking`, `must avoid`, or `infringing` with neutral screening language unless qualified counsel supplied the conclusion and attribution is shown.

## Scenario-specific emphasis

### R&D updates

Look for technical lessons inside changes, failures, tuning, workarounds, and root-cause findings. Exclude pure progress statements unless they reveal a technical change. Search only query-ready candidates.

### Meeting notes

Capture old-to-new decisions, reasons, rejected alternatives, experimental observations, and speaker attribution as a contributor lead—not an inventorship conclusion. Preserve rejected routes when they support boundaries, trade-secret review, or design history.

### Technical designs and experiment records

Use background limitations, implementation sections, drawings, results, controls, parameters, alternatives, and negative evidence. Search all query-ready candidates, while documenting gaps and independent candidates separately.

## Quality gates

Before delivery verify:

- every candidate has a source location and no invented element;
- duplicates are merged and broad concepts are split where independently actionable;
- source fact, paraphrase, inference, and missing evidence are distinguishable;
- searches are candidate-specific and reproducible;
- patent families/publications and result counts are not conflated;
- no similarity threshold is treated as a legal test;
- no patentability, infringement, validity, FTO, ownership, or inventorship conclusion is overstated;
- disclosure advice is jurisdiction-sensitive;
- counts reconcile across summary, portfolio, details, actions, and evidence;
- URLs are global and resolve to intended records;
- HTML is responsive, keyboard accessible, printable, and safely escaped;
- report cutoff, reviewer, limitations, and next specialist review are visible.

## Completion statement

Tell the user where the report was saved, what was and was not searched, the evidence cutoff, and which items need contributor, IP-professional, counsel, security, or business review. Do not imply that generating the report files or running a limited screen completes protection.

## Candidate state model

Maintain one explicit state per candidate:

1. `detected` — a technical-change signal has a traceable source location;
2. `awaiting-contributor-evidence` — a decisive technical field is missing;
3. `query-ready` — differentiating implementation features support a meaningful search;
4. `searched-screening-only` — a documented limited search was completed;
5. `specialist-review` — an IP professional, counsel, security, ownership, or business review is required;
6. `monitor` — retain with a defined refresh trigger;
7. `archived` — closed with a documented reason.

Do not label a candidate complete merely because a search returned results. Preserve state history, reviewer, date, and the event that caused each transition.

## Candidate splitting and dependency rules

Keep one candidate when multiple embodiments share the same differentiating concept and decision path. Split when contributions have independently meaningful:

- technical problems;
- implementation features;
- effects;
- contributor facts;
- disclosure events;
- search queries;
- review paths.

Record parent/child, alternative, prerequisite, and system/subcomponent relationships. Do not inflate counts by treating every parameter or module as a separate invention signal.

## Source-type refinements

### Bug fixes and incident records

Separate the observed failure, root-cause evidence, remedy, implementation boundary, verification, and reusable rule. A one-off manual correction is not automatically a candidate; a generalizable technical mechanism may be.

### Release and change logs

Trace the changed version, commit/design record, reason, implementation, validation, authorship/contribution evidence, and any earlier external release. Do not infer the entire product feature from a short release note.

### Research and laboratory records

Capture protocol, materials, equipment, calibration, controls, samples, exclusions, repeats, uncertainty, negative results, and safety constraints. Distinguish exploratory observation from a reproducible contribution.

### Product requirements

Treat a requirement as a problem or desired outcome. Extract a candidate only when the material also provides a specific technical mechanism or links to an implementation record.

## External-evidence relevance scale

Use neutral labels:

- `directly relevant for specialist review` — the reviewed record appears to disclose several differentiating features;
- `partially relevant` — overlapping field or features, with material differences;
- `background context` — useful for terminology, baseline, or technical history;
- `not relevant after review` — apparent hit rejected with reason.

For every label identify the reviewed passage or claim location and the unresolved interpretation. Never use `blocking`, `must avoid`, or `safe` unless the report quotes and attributes a qualified legal conclusion.

## Protection-path evidence requirements

Before recommending patent review, record the technical contribution, contributor leads, disclosure facts, ownership/third-party flags, and at least a preliminary observability rationale.

Before recommending trade-secret review, record the secret subject matter, business value, authorized access, existing controls, reverse-engineering risk, independent-development risk, and proposed reasonable measures.

Before recommending defensive-publication review, identify the strategic purpose, review authority, confidential/third-party material to remove, publication venue, and consequences for later rights.

Before archiving, preserve the source location, assessment basis, duplicates, search status, disclosure status, approver, and revisit trigger.

## Report consistency rules

The portfolio row, detail card, action item, search log, and external-evidence table must use the same candidate ID. Reconcile:

- total candidates = every unique detail card;
- priority counts = portfolio rows by current priority;
- query-ready count = candidates passing the recorded readiness gate;
- searched count = candidates with at least one successfully logged search;
- unsearched count = query-ready failures plus candidates awaiting evidence, shown separately when useful;
- action count = executable owner/date tasks, not narrative recommendations;
- external-evidence count = reviewed records, not total search hits.

If the search connector truncates or paginates results, report that limit. If one patent family has multiple publications, do not count each publication as an independent technical disclosure unless the analysis explicitly needs publication-level units.

## Data-handling gate

Before sending any source-derived query to a connector, confirm authorization and minimize confidential detail. Keep secrets, personal data, unpublished contributor facts, customer identifiers, export-controlled information, and third-party confidential content out of external queries unless the approved environment and policy permit them.

The final report must not contain credentials, hidden prompts, local user paths, session identifiers, or unauthorized source text. Use the organization's approved storage and retention process; the skill does not invent a storage location.
