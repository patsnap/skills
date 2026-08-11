---
name: mine-patentable-inventions-ip
description: Identify, structure, screen, and route potentially patentable inventions from R&D projects, technical improvements, standards work, existing innovations or portfolios, competitor patents, design-around needs, cross-domain technology transfer, or emerging opportunity hypotheses. Use when engineers or IP teams need a quick or deep four-block, ten-step invention-mining workflow with patent/prior-art evidence, checkpoints, innovation cards, a six-month roadmap, and Markdown or HTML reporting.
---

# Mine Patentable Inventions

## Purpose

Help R&D engineers, technical leaders, and IP professionals recognize and structure potential inventions,
test them against public evidence, and decide what technical and IP work should happen next.

The skill addresses:

- recognition bottlenecks: teams do not see what may be protectable;
- expression bottlenecks: ideas are not yet reproducible or technically specific;
- legal-framing bottlenecks: protection angles are unclear;
- direction bottlenecks: teams do not know where to expand or validate;
- portfolio bottlenecks: isolated ideas do not form a coherent protection strategy;
- competitive bottlenecks: competitor rights or designs constrain development.

## Professional boundary

This skill:

- does not invent the technology for the engineering team;
- does not replace qualified patent counsel;
- does not guarantee grant, validity, enforceability, FTO, or commercial value;
- does not draft claims before a reproducible technical disclosure exists;
- does not treat a low-density search result as proven white space;
- does not disclose confidential inventions to unapproved services.

## Core principles

1. Invention mining and portfolio strategy are related but distinct.
2. Useful inventions are found through deliberate technical and legal questioning.
3. Structured invention generation can be trained and repeated.
4. Business, standards, competitor, manufacturing, and market context inform—but do not replace—technical evidence.
5. Quality and reproducibility matter more than application count.

## Required inputs

### Required

- `tech_domain`: defined technology domain;
- `mining_purpose`: one of the scenarios below or an equivalent decision objective;
- `entity_name`: company/team or an approved anonymous label;
- available technical description;
- confidentiality and disclosure constraints.

### Optional

- `own_advantages`: technical strengths;
- `core_innovation`: known core concept;
- `competitor`: relevant competitor or technical comparator;
- `parent_tech`: parent technology for cross-domain transfer;
- `target_patent`: only for portfolio-completion, competitor-encirclement, or design-around scenarios;
- application requirements and performance targets;
- experimental, prototype, simulation, manufacturing, or field evidence;
- critical dates, publications, demonstrations, sales, offers, standards submissions, or prior disclosures;
- target jurisdictions and business markets.

Do not request a patent number in ordinary R&D-project mining when it is not needed.

## Verified PatSnap MCP services

Use the English interface and English output.
Inspect the live tool schema before calling a connector.

### Required: Advanced Patent Search

- Connector key: `advanced_patent_search`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-search
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`
- Use: landscape, assignee, citation, novelty, and prior-art searches.

### Required: Patent Briefing

- Connector key: `patent_briefing`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-briefing
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- Use: bibliography, family, status, claims, description, translations, images,
  and technical summaries for relevant patents.

### Recommended: Deep Patent Mining

- Connector key: `deep_patent_mining`
- Marketplace: https://open.patsnap.com/marketplace/mcp-servers/patent-mining
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-mining`
- Use: technical problems, solutions, effects, topics, classifications, materials,
  and application-domain evidence.

Use authoritative approved sources for:

- scientific and engineering literature;
- standards and standards proposals;
- products and manuals;
- current statutes, examination guidance, and case law;
- market and company facts.

Replace generic source labels with stable evidence records:

```text
evidence_id
source_type
publisher_or_connector
title_or_record
date
retrieved_at
URL_or_locator
evidence_scope
feature_or_claim_ids
confidence
limitations
```

## Two operating modes

### Quick mode — default when the input is sufficiently specific

1. Produce the preflight confirmation card.
2. If the user has already explicitly delegated the full workflow or said “proceed,” record approval.
3. After approval, run Blocks 1–3 continuously.
4. Mark uncertainty and continue when noncritical information is missing.
5. Before Block 4, confirm whether to create the roadmap and complete report unless that deliverable was already delegated.

### Deep mode

Use when the user requests a complete, formal, or detailed analysis, or specifies `mode=deep`.

1. Produce and approve the preflight confirmation card.
2. Stop after each Block for review unless the user explicitly delegates continuous execution.
3. Preserve every checkpoint decision.
4. Generate the complete HTML report after CP-4.

### Mode-switch rule

If the user changes the technical domain, purpose, or material scope, return to scenario identification and CP-0.

## Engineering-language rule

Use technical language in:

- the technology tree;
- invention directions;
- competitor analysis;
- innovation cards;
- project recommendations;
- final report narrative.

Patent classification codes may appear only in the search-methodology section and must include
a plain-language definition, for example:

```text
H10K 50 (organic light-emitting device structures)
```

Do not expose unexplained classification codes to engineering users.

## Prohibited behavior

1. Do not fabricate patent numbers, applicants, classifications, citations, experiments, products, or search results.
2. Do not give a patentability or grant conclusion without prior-art analysis.
3. Do not draft a claim framework before the invention is structured and reproducible.
4. Do not fill missing parameters, results, competitor facts, or examples with generic invention-like prose.
5. Do not force competitor-encirclement or design-around concepts into patent filing when they are technically inferior or uneconomic.
6. Do not display unexplained patent classifications outside search methodology.
7. Do not begin Block 1 before CP-0 approval unless the user has already explicitly approved direct execution.
8. Do not omit the approved CP-0 project fields from the final project overview.
9. Do not expose confidential verbatim user text beyond what is necessary for traceability and authorized reporting.
10. Do not treat a patent search as a complete legal or scientific search without documented scope and limitations.

## Step 1 — Identify the mining scenario

Classify the request into one of nine source scenarios.

### Scenario 1 — R&D project mining

Question: What potentially patentable units exist in the current project?

Likely bottlenecks:

- recognition: the team thinks ongoing work is ordinary;
- expression: technical differences are hard to articulate.

### Scenario 2 — Expand around a core innovation

Question: How can protection extend around a high-value technical concept?

Likely bottlenecks:

- portfolio: the team assumes one filing exhausts the opportunity;
- direction: downstream, upstream, implementation, and application variants are unclear.

### Scenario 3 — Standards-oriented invention mining

Question: How can a standards contribution and patent strategy be coordinated lawfully and on time?

Likely bottlenecks:

- legal: standards and patents are treated as unrelated;
- direction: disclosure, filing, contribution, licensing, and competition-law timing is unclear.

Require current standards-development rules, IPR policy, disclosure obligations, meeting/publication dates,
contribution history, and counsel review. Do not promise standard-essential status.

### Scenario 4 — Technical improvement mining

Question: Which fixes, parameter changes, control changes, or manufacturing improvements contain reproducible invention value?

Likely bottlenecks:

- recognition: a bug fix or parameter change appears too small;
- expression: before/after conditions and effects are not quantified.

### Scenario 5 — Complete an existing patent portfolio

Question: Where are the technical and claim-coverage gaps around existing rights?

Likely bottlenecks:

- portfolio: gaps and dependencies are unclear;
- competitive: likely design-around routes are unknown.

### Scenario 6 — Develop alternatives around a competitor patent

Question: Which technically credible alternative paths create differentiation and negotiating options?

Likely bottlenecks:

- competitive: the target patent appears unavoidable;
- direction: substitute structures, functions, processes, materials, controls, and applications are unclear.

Route detailed work to `develop-patent-design-arounds-ip` or `design-around-multiple-patents-ip` if installed.

### Scenario 7 — Design around infringement risk

Question: Can a product be redesigned while retaining required performance and generating protectable improvements?

Likely bottlenecks:

- competitive: performance may degrade;
- direction: claim-feature and product-feature alternatives are unclear.

This scenario requires jurisdiction, claim version, product facts, relevant date, prosecution history,
requirements, and counsel review.

### Scenario 8 — Cross-domain technology transfer

Question: How can a mature parent technology be adapted to a new domain or operating environment?

Likely bottlenecks:

- direction: technical equivalence and transfer path are unclear;
- expression: adaptation logic, secondary problems, and new effects are not reproducible.

### Scenario 9 — Emerging opportunity hypothesis

Question: Which foundational technical directions may merit early research and filing work?

Likely bottlenecks:

- recognition: evidence and experiments are immature;
- direction: the apparent gap and feasible breadth are uncertain.

Call it an opportunity hypothesis, not a white space, until negative search, adjacent-art,
technical feasibility, market/need, and legal review are complete.

### If no scenario fits

Ask for `tech_domain` and `mining_purpose`, plus one or two facts that materially affect the workflow.

## Bottleneck taxonomy

| Bottleneck | Typical symptom | Mining response |
|---|---|---|
| Entry | Work exists but the team cannot identify protectable units | Map technical changes, decisions, and effects |
| Recognition | The team sees no meaningful invention | Establish baseline, comparator, constraint, and measurable difference |
| Direction | A broad idea lacks implementable paths | Decompose functions, mechanisms, resources, and validation routes |
| Competitive | Competitor rights or products constrain action | Map evidence, claim/product facts, alternatives, and design requirements |
| Expression | A concept is not reproducible | Capture structure, sequence, materials, parameters, conditions, and effects |
| Legal framing | Protection angle is unclear | Compare method, apparatus, system, composition, use, control, and manufacturing disclosures |
| Portfolio | One filing does not form a coherent position | Map core, implementation, application, manufacturing, monitoring, and fallback layers |

## CP-0 — Preflight confirmation card

The first workflow output is:

```text
Invention Mining Preflight Card

Mining scenario: [scenario]
Operating mode: [Quick or Deep, with explanation]
Project entity: [authorized name or anonymous label]
Likely bottlenecks: [list with concise rationale]
Proposed technical workstreams:
  - Workstream 1: [...]
  - Workstream 2: [...]
  - Workstream N: [...]
Confidentiality/disclosure constraints: [...]
Target jurisdictions or decision context: [...]

Please confirm or correct this scope before Block 1.
```

If information is missing, add:

```text
Material information needed: [one or two items]
If already authorized to proceed, missing noncritical fields will remain Unresolved and will not be invented.
```

### CP-0 approval logic

- If the user confirms, corrects, says “proceed,” “continue,” or “do it directly,” record approval.
- If the initial request already expressly delegates the complete workflow without per-step confirmation,
  record that instruction as approval and do not ask redundantly.
- If a missing choice would materially change scope, confidentiality, jurisdiction, or external disclosure,
  obtain it before Block 1.
- Otherwise stop after the card until approval.

### CP-0 snapshot

Record:

```text
confirm_mining_type
confirm_mining_mode
confirm_entity
confirm_pain_points
confirm_tech_lines
confirm_user_extra
approval_text_or_instruction
approval_timestamp
confidentiality_constraints
```

Preserve meaning and traceability.
Quote verbatim user text in the report only where authorized and necessary; otherwise retain a faithful,
privacy-minimized project record and a source locator.

## Four blocks and ten steps

## Block 1 — Technical decomposition

### Step 1 — Patent and technical scan

Use the user’s scope to search:

- recent five-year activity for current competitive context;
- older and non-patent evidence needed for prior-art and technical baseline;
- key applicants and inventors;
- technically dense directions;
- apparent sparse directions requiring further validation;
- standards, products, literature, and public disclosures where relevant;
- citations and related families for important records.

The five-year window is a recent-activity view, not the complete prior-art period.

#### Search strategy

Record:

- English and other relevant-language keywords;
- technical classifications with plain-language definitions;
- field restrictions;
- applicants and aliases;
- dates and relevant prior-art cutoff;
- exclusions and false-positive controls;
- jurisdictions and databases;
- family/count rule;
- query version and retrieval date;
- matched totals and sample boundaries;
- known limitations.

Do not calculate landscape statistics from a relevance-ranked sample.

### Step 2 — Decompose the technology

Break the project or problem domain into the smallest reproducible candidate invention units.

Possible branches:

```text
R&D project
├── Product/components
│   ├── geometry and structure
│   ├── materials and compositions
│   ├── interfaces and relationships
│   ├── sensing and control
│   ├── manufacturing tools
│   └── manufacturing processes
├── System
│   ├── architecture
│   ├── workflow or method
│   ├── data and algorithms
│   ├── assembly and calibration
│   └── operation and maintenance
└── Application and lifecycle
    ├── use scenarios
    ├── performance adaptation
    ├── diagnostics and monitoring
    ├── recycling or end-of-life
    └── safety, standards, and compliance
```

For every node capture:

```text
node_id
technical_description
baseline_or_comparator
change_or_decision
problem
mechanism
expected_effect
evidence
requirements
dependencies
uncertainty
```

### CP-1 — Block 1 self-check

- Search terms, classifications, fields, dates, and query versions are documented.
- Key technical and commercial comparators are evidence-backed.
- Dense and apparently sparse directions are qualified by search scope.
- The technical tree uses engineering language.
- At least three potential problem points are identified when the evidence supports them.
- Confidential data handling remains authorized.

Quick mode proceeds automatically after approval when CP-1 passes.
Deep mode pauses for Block 1 review unless continuous execution was delegated.
Missing information becomes an explicit evidence gap; do not fabricate it.

## Block 2 — Form invention concepts

### Step 3 — Identify and prioritize problems

Find problems from:

- unmet requirements;
- failure modes and defects;
- excess cost, energy, size, mass, time, or complexity;
- unstable control or poor reliability;
- material, manufacturing, assembly, calibration, or supply constraints;
- safety, usability, standards, or regulatory constraints;
- competitor/claim limitations;
- unserved applications or environments;
- integration and lifecycle issues.

Problem record:

```text
problem_id
technical_tree_node
problem_statement
baseline
cause_hypothesis
affected_requirement
severity
frequency
strategic_relevance
evidence_ids
priority: P0 | P1 | P2
owner
uncertainty
```

### Step 4 — Develop solution concepts

Use appropriate methods such as:

- TRIZ;
- functional analysis;
- contradiction mapping;
- function-effect search;
- morphological analysis;
- controlled brainstorming;
- cross-domain analogies;
- design of experiments;
- failure-mode analysis;
- manufacturing and lifecycle analysis.

For every P0/P1 problem create at least one defensible concept when possible.

Concept record:

```text
concept_id
problem_id
solution_principle
structure_or_steps
materials_or_components
relationships
parameters_and_ranges
operating_conditions
control_logic
expected_effect
effect_measurement
secondary_problems
alternatives
evidence_ids
technical_readiness
missing_information
```

Do not invent quantitative effects.
If an effect is untested, label it as a hypothesis and define the experiment.

### CP-2 — Block 2 self-check

- Problems are P0/P1/P2 and linked to technical-tree nodes.
- Every P0/P1 problem has a concept or an explicit reason it does not.
- Every concept has a mechanism and expected effect.
- Quantification is evidence-backed or clearly a test target.
- Reproducibility gaps are explicit.

Quick mode proceeds to Block 3 when CP-2 passes.
Deep mode pauses unless continuous execution was delegated.

## Block 3 — Evaluate invention concepts

### Step 5 — Establish the relevant public baseline and prior art

Search:

- patents and patent families;
- scientific literature;
- conference materials;
- standards and standards contributions;
- product manuals, catalogs, webpages, and public use/sale evidence;
- theses, technical reports, regulatory documents, and other applicable sources.

Record for each reference:

```text
reference_id
source_type
title_or_identifier
publisher_or_owner
priority_or_publication_date
public_availability_date
jurisdiction_or_database
URL_or_locator
relevant_features
concept_ids
feature_mapping
relevance
limitations
```

Determine the applicable critical date and legal rules with qualified counsel.
Do not limit patentability searching to five recent years.

### Step 6 — Screen patentability and differentiation

Assess, as applicable:

- novelty;
- inventive step/nonobviousness;
- utility/industrial applicability;
- eligibility/patentable subject matter;
- enablement, support, written description, clarity, and definiteness;
- unity/restriction and claim-category strategy;
- ownership, inventorship, entitlement, and disclosure timing.

Use evidence states:

- feature overlap: High / Medium / Low / Unresolved;
- differentiation space: Clear / Limited / Unresolved;
- disclosure support: Adequate / Partial / Insufficient / Unresolved;
- evidence confidence: High / Medium / Low.

Do not state “grant prospects are good/bad.”
Recommend experiments, clarification, route changes, or further search.

### Step 7 — Conditional infringement-risk screen

Run only for:

- competitor-patent alternatives;
- design-around work;
- portfolio-completion work where product use is in scope.

Require:

- target jurisdiction;
- authoritative claim version;
- relevant date and status;
- product/process facts;
- claim construction assumptions;
- prosecution/post-grant history;
- counsel review.

Use claim-feature states `Present`, `Absent`, `Unclear`, or `Disputed`.
Use overall screening states `High`, `Medium`, `Low`, or `Unresolved` with evidence and limitations.
Never call a concept non-infringing.

### Step 8 — Conditional design-around work

For high or unresolved risk, consider:

- trimming/removal;
- substitution;
- combination or reallocation;
- decomposition;
- changed principle or architecture;
- changed actor, sequence, material, control, or operating environment.

Route detailed work to an installed design-around skill when appropriate.
If the alternative fails requirements or is uneconomic, recommend redesign or no filing.

### Step 9 — Extract innovation points

Evaluate each concept across:

#### Technical dimension

- problem specificity;
- mechanism clarity;
- reproducibility;
- measured or testable effect;
- alternatives and fallback embodiments;
- technical readiness.

#### Legal/IP dimension

- prior-art differentiation;
- disclosure support;
- claim-category options;
- detectability and enforceability hypotheses;
- design-around resilience;
- ownership/inventorship and public-disclosure risks.

#### Business/strategy dimension

- product and roadmap relevance;
- standards or regulatory relevance;
- competitive leverage;
- secrecy versus patent tradeoff;
- lifecycle and jurisdiction relevance;
- cost and time to validate.

Innovation card:

```text
innovation_id
concept_id
title
problem
solution
technical_effect
essential_features
optional_features
alternatives
evidence_ids
prior_art_difference
disclosure_support
patentability_questions
infringement_questions
business_relevance
validation_need
confidence
```

### CP-3 — Block 3 self-check

- Innovation-point register exists.
- Prior-art references have traceable evidence IDs and dates.
- Each concept has a feature-level comparison.
- Search blind spots and unavailable sources are explicit.
- No unsupported patentability or infringement conclusion appears.

After CP-3, quick and deep modes pause before Block 4 unless roadmap/report execution was already delegated.

## Block 4 — Decide next actions

### Step 10 — Route each innovation and build a six-month roadmap

Disposition states:

### File promptly

Use only when disclosure, evidence, ownership, dates, and business need support prompt counsel action.

### Refine and validate

Use when experiments, parameters, embodiments, alternatives, or searches are missing.

### Incubate

Use when direction is strategically useful but technical readiness is low.

### Consider trade-secret protection

Evaluate:

- information secrecy;
- independent economic value from secrecy;
- reasonable measures;
- employee/vendor controls;
- detectability and reverse engineering;
- patent disclosure tradeoffs;
- duration and mobility of know-how;
- ownership and jurisdiction.

### Do not pursue

Use when the concept is public, trivial, unsupported, technically inferior, uneconomic,
misaligned, or creates unacceptable risk.

For each innovation record:

```text
innovation_id
disposition
rationale
owner
target_date
dependency
required_evidence
counsel_action
confidentiality_action
success_criterion
```

### Six-month roadmap

Include:

- month or date range;
- innovation IDs;
- technical experiments;
- search and legal review;
- inventorship/ownership review;
- disclosure-control action;
- drafting/filling or secrecy decision;
- portfolio/standards/business coordination;
- owner;
- milestone and gate.

Dates and owners are proposed until the user confirms them.

### CP-4 — Final self-check

- Every innovation has a disposition.
- Owner and target date are present or explicitly Unassigned.
- Six-month roadmap exists.
- CP-0 project fields appear faithfully in the project overview.
- Confidential text is handled according to approval and minimization rules.
- All unresolved patent, legal, technical, and business questions remain visible.

## Mandatory project overview

The final report begins, after title and metadata, with:

| Field | Source |
|---|---|
| Mining scenario | `confirm_mining_type` |
| Operating mode | `confirm_mining_mode` |
| Project entity | `confirm_entity` |
| Likely bottlenecks | `confirm_pain_points` |
| Technical workstreams | `confirm_tech_lines` |
| User additions and constraints | `confirm_user_extra` |
| Approval record | `approval_text_or_instruction` and timestamp |
| Confidentiality controls | `confidentiality_constraints` |

Preserve the approved meaning and all material facts.
Use exact quotation only where authorized and necessary; otherwise use a faithful privacy-minimized record
with a locator to the approved source interaction.

## Output formats

### Conversational and quick-mode output

Use Markdown:

- preflight confirmation card;
- technical tree as an indented tree or accessible diagram;
- search/evidence register;
- problem and concept tables;
- innovation cards;
- roadmap table;
- progress and next gate.

### Complete report

Generate one self-contained light HTML file when requested.

Required sections:

1. title and metadata;
2. mandatory project overview;
3. scope, mode, confidentiality, and evidence boundaries;
4. patent and technical scan;
5. technical tree;
6. problem register;
7. invention concepts;
8. prior-art and feature mappings;
9. patentability/differentiation screen;
10. conditional infringement/design-around analysis;
11. innovation cards and dispositions;
12. six-month roadmap;
13. sources, limitations, approvals, and next actions.

### HTML visual system

- white or light-neutral background;
- navy/slate hierarchy;
- restrained teal accent;
- system fonts;
- semantic headings, tables, forms, and navigation;
- technical tree as accessible HTML/CSS or static SVG with a table equivalent;
- roadmap as a table with responsive overflow;
- evidence and uncertainty in text;
- visible keyboard focus;
- print CSS and repeated table headers;
- escaped untrusted text and allowlisted HTTP(S) links;
- no remote dependency, gradient, dark background, star rating, or emoji-only state.

## Multi-turn management

### Progress memory

At each pause, state:

- approved scope and mode;
- completed Block and checkpoint;
- unresolved information;
- next action and whether approval is required.

### Scenario switch

If the technology domain or purpose changes materially, return to Step 1 and create a new CP-0 snapshot.

### Rollback

If the user says “return to the previous step” or “restart from Block X,” preserve prior evidence,
mark superseded decisions, and restart from the requested point.

### Direct progression

If the user says “proceed,” “continue,” “no confirmation,” or delegates all Blocks,
record the instruction and advance through non-material checkpoints without redundant questions.
Do not bypass a confidentiality, jurisdiction, authorization, or scope choice that materially changes the work.

## Quality gates

### QG-01 — Evidence integrity

- No patent, applicant, reference, classification, product, experiment, or search result is invented.
- Every source has an evidence ID, date, locator, and scope.
- Search samples and complete populations are labelled separately.

### QG-02 — Technical specificity

- Problems, mechanisms, structures/steps, parameters, conditions, effects, and alternatives are captured.
- Untested effects are hypotheses with test plans.
- Claim drafting does not begin before reproducibility.

### QG-03 — Prior-art and dates

- Critical dates are identified or Unresolved.
- Search extends beyond the recent activity window.
- Patent and non-patent evidence is mapped feature by feature.
- Public availability and translation uncertainty are reviewed.

### QG-04 — Legal calibration

- Destination patentability rules are current and source-backed.
- Patentability is a provisional screen, not a grant prediction.
- Conditional infringement/design-around work is jurisdiction-, claim-, date-, and fact-specific.
- Ownership, inventorship, disclosure, eligibility, and secrecy issues are visible.

### QG-05 — Workflow parity

- Nine scenarios and seven bottlenecks remain available.
- Two modes remain available.
- CP-0 through CP-4 are recorded.
- Blocks 1–4 and Steps 1–10 are complete or have explicit unavailable reasons.
- CP-0 project fields reconcile with the final overview.

### QG-06 — Classification language

- Classification codes appear only in search methodology with plain-language definitions.
- Technical trees, recommendations, and report prose use engineering language.

### QG-07 — Actionability

- Every innovation has evidence, confidence, validation, disposition, owner, target date, and gate.
- The roadmap includes technical, search, counsel, ownership, confidentiality, and business actions.

### QG-08 — Privacy and security

- Confidential invention text is shared only with approved tools and audiences.
- User quotations are minimized and authorized.
- No secret or unpublished matter appears in reusable package text or an unintended report.

### QG-09 — Report quality

- Markdown and HTML agree.
- HTML is offline, semantic, accessible, responsive, print-ready, and safely escaped.
- Evidence, limitations, approvals, and unresolved items are visible.

## Failure handling

If the input lacks a technical mechanism, remain at CP-0 and request the material facts.
If the user withholds a company name, use an approved anonymous label.
If the search is unavailable, provide a preparation framework and mark patentability screening blocked.
If prior-art dates are unclear, do not issue a novelty screen.
If the invention is not reproducible, return to Block 2 and define experiments or disclosure needs.
If a design-around concept fails requirements, recommend product redesign or no filing.
If ownership or public disclosure is uncertain, escalate promptly to counsel.
If fewer concepts exist than a template suggests, report the defensible set rather than fabricate.

## Reference and authority discipline

The source package names several invention-mining and patent-practice books, but does not bundle their text.
Do not claim to have applied a named book unless it was actually accessed and reviewed.

For execution, prioritize:

- current official patent-office examination guidance;
- current statutes, rules, and relevant primary legal authority;
- WIPO and standards-organization materials where applicable;
- reviewed engineering and scientific evidence;
- qualified local patent counsel.

## Final response

State:

- approved scenario, mode, entity label, and technical workstreams;
- Blocks and checkpoints completed;
- number of problem, concept, reference, and innovation records;
- strongest evidence-backed differentiation;
- most important technical, legal, disclosure, or search gap;
- dispositions and six-month priority actions;
- report path when created;
- exact counsel, engineering, ownership, confidentiality, or standards review required.
