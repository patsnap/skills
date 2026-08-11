---
name: reactivate-underused-patents-ip
description: Assess underused patents and related intangible assets, cluster them into decision-ready packages, evaluate internal reuse and transaction options, research candidate counterparties, and create evidence-backed portfolio activation deliverables. Use for patent portfolio activation, maintenance review, outbound licensing or assignment screening, transaction-readiness review, internal R&D reuse, candidate buyer/licensee research, management reporting, or a 30/60/90-day activation plan.
---

# Reactivate Underused Patents

## Purpose

Turn a defined patent and related-intangible-asset inventory into evidence-backed
options for:

- internal R&D or product reuse;
- retention/maintenance review;
- non-exclusive, exclusive or field-of-use licensing;
- assignment;
- option/evaluation agreements;
- joint development or research collaboration;
- cross-license, pool or venture contribution where appropriate; and
- abandonment/archiving review by authorized owners and professionals.

Do not equate a patent grant, model score, citation count, family size, absent public
implementation, or lack of a recorded license with value, dormancy, ownership,
transaction readiness, or a final action.

Read all three references before execution:

- `references/mcp-boundaries.md` for connector and evidence rules;
- `references/output-spec.md` for deliverables; and
- `references/example-prompts.md` for localized use cases.

## Define “underused” for this review

Use `underused candidate` or `under-evidenced candidate` until internal evidence is
available. Define the review population and test:

- current and planned product/process use;
- defensive, standards, cross-license, blocking or ecosystem role;
- existing licenses, assignments, options, pledges/security interests or negotiations;
- related know-how, software, data, trademark, prototype, testing and inventor team;
- jurisdictions, status, enforceable term, maintenance horizon and prosecution;
- prior investment and continuing cost;
- technical relevance to current strategy;
- field-of-use and counterparties; and
- data cutoff and unavailable internal records.

An expired/lapsed patent may relate to useful public-domain technology, know-how, data,
software or brand, but it is not an enforceable patent right. Keep those asset types and
rights distinct.

## Minimum inputs

Obtain or derive:

- asset owner and authority for the review;
- portfolio list, organization, technical domain or another resolvable population;
- objective: internal reuse, maintenance, license, assign, collaborate, diligence,
  financing/pledge exploration or portfolio cleanup;
- jurisdictions and relevant dates;
- internal-use and transaction-history records available;
- product/R&D/business context;
- related non-patent assets and evidence;
- confidentiality, external-disclosure and source-access boundaries;
- audience and requested artifact formats; and
- decision owners/professional reviewers where known.

If ownership/authority, population or objective is missing, ask once for the minimum
information. Do not create a client-ready report from a vague intent.

## MCP and source plan

Use only the roles and exact links in `references/mcp-boundaries.md`.

### Required published services

- `advanced_patent_search` for reproducible discovery and statistics.
- `global_core_patent_database` for selected-record verification.

### Recommended published services

- `patent_monetization_valuation` for transaction-oriented selected-record evidence.
- `patent_briefing` for quick selected-record technical/family/status evidence.

### Optional runtime-discovered service

Use `patent_valuation_scorecard` only when its operations are present in the live
runtime. Record tool/provenance and treat results as model-derived screening inputs.
Do not document an unverified marketplace URL or make it a dependency.

### Internal/public evidence

Use authorized internal registers, contracts, product/project records, finance/cost
data, CRM/transaction history, technical reports and governance records. For missing
corporate, procurement, transaction, regulatory or market evidence, research current
official and credible public sources when authorized. Record URL/document ID, date,
access date, evidence level and conclusion use.

Missing internal or public data remain unknown. Do not invent non-patent assets,
counterparties, use, demand or transaction history.

## Workflow

## Step 1 — Confirm objective, population and rubric

Create a confirmation record:

```text
Portfolio activation scope
Owner/authority: [...]
Population and asset types: [...]
Objective and decision date: [...]
Jurisdictions: [...]
Internal evidence available: [...]
External research authorized: [...]
Confidentiality/audience: [...]
Rubric and scenarios: [...]
Requested deliverables: [...]
Required reviewers: [...]
```

Agree whether the task is screening or a decision process. Maintenance, abandonment,
pledge, transaction, valuation and external outreach require explicit approval gates.

### Rubric design

Define dimensions appropriate to the objective, for example:

- technical relevance/differentiation;
- product/R&D reuse potential;
- evidence of commercial need;
- portfolio complementarity and strategic role;
- jurisdiction/status/term and rights fit;
- ownership/encumbrance/contract readiness;
- supporting know-how/data/software/brand/prototype completeness;
- candidate-counterparty fit;
- cost/resource requirements;
- evidence quality and uncertainty; and
- transaction/readiness constraints.

Do not reuse fixed 100-point weights or A–E cutoffs automatically. If scoring is useful:

1. define every scale and direction;
2. expose weights and calculation;
3. separate missing from low;
4. apply hard diligence gates separately;
5. run alternative weights/scenarios; and
6. show rank/class changes.

Use user-defined segment labels or descriptive states such as `activate now for review`,
`develop evidence`, `portfolio/defensive hold`, `maintenance decision review`, and
`insufficient evidence`.

## Step 2 — Build and normalize the asset inventory

### Resolve entities

Map:

- legal owner/current assignee;
- original applicant;
- parent/subsidiary and historical names;
- university department, spinout or technology-transfer entity;
- inventor/research team where authorized;
- acquisition/merger effective dates; and
- ambiguous identities marked `to_confirm`.

Do not merge corporate entities without evidence.

### Resolve patent assets

For each record preserve:

- publication, application and grant identifiers separately;
- family ID/definition and representative-publication rule;
- jurisdiction;
- priority, filing, publication, grant and status dates;
- current owner signal and source;
- simple status and legal-event details as of cutoff;
- remaining-term review state, not an unsupported computed conclusion;
- citations and event signals with type/date;
- claims/description/translation evidence state; and
- source connector/operation/run ID.

### Add related assets

Only from authorized evidence, associate:

- know-how and trade secrets;
- software/copyright;
- trademarks/product names;
- semiconductor-layout, plant-variety or other rights where relevant;
- data, models and documentation;
- prototypes, samples, testing/validation and regulatory files;
- project/funding/contracts; and
- inventor/technical-support availability.

Respect confidentiality and access controls. Do not copy source-restricted database
content into an external report.

## Step 3 — Cluster into asset packages

Group assets by evidence-backed relationships:

- shared technical problem/solution route;
- product/application/field of use;
- family or complementary claim coverage;
- research team/project/funding;
- know-how/software/data/prototype dependencies;
- common counterparty/industry context; and
- portfolio/defensive role.

Each package needs:

- stable `package_id` and external-readable name;
- technical proposition and evidence;
- included/excluded assets and rationale;
- rights/jurisdiction/status scope;
- supporting assets and missing dependencies;
- potential activation scenarios; and
- package-level diligence and uncertainty.

Do not cluster solely because titles or IPC codes are similar. Do not force three
packages or a fixed number of patents.

## Step 4 — Apply the transaction-readiness gate

For each asset/package investigate available evidence for:

1. current ownership and chain of title;
2. co-owners and consent requirements;
3. exclusive/non-exclusive licenses, options and retained rights;
4. security interests, pledges, liens and releases;
5. government/university/sponsored-research and employee-invention obligations;
6. maintenance, status, term, disclaimers/extensions/adjustments and prosecution;
7. opposition, reexamination, invalidation, litigation and settlement constraints;
8. standards/FRAND or pool commitments;
9. field, territory, sublicensing and enforcement restrictions;
10. confidentiality, know-how and disclosure rights;
11. export control, sanctions, sector regulation, ethics/biosafety and privacy;
12. competition/antitrust, tax, accounting, valuation and corporate approval; and
13. authority to market, disclose, license, assign, pledge or abandon.

Use states:

- `evidence reviewed`;
- `database signal only`;
- `official/contract verification required`;
- `blocking issue`; and
- `unknown`.

“Transaction readiness” is a workflow status, not clean-title assurance. A favorable
model score cannot override a rights or authority problem.

## Step 5 — Assess technical, portfolio and commercial evidence

### Three-layer patent research

Follow the funnel in `mcp-boundaries.md`:

1. explore terminology, solutions and organizations;
2. measure with versioned reproducible search and documented population/caps; and
3. verify selected assets with claims/family/status/events/full text.

### Technical assessment

Record:

- problem, technical means and reported effect;
- distinguishing evidence and nearest relevant solutions;
- evidence depth and translation status;
- current product/R&D relevance;
- integration dependencies and validation needs;
- alternative technical routes; and
- limits on claim/scope interpretation.

### Portfolio assessment

Record family/jurisdiction complementarity, gaps, overlap, defensive/cross-license role,
supporting assets, lifecycle/cost horizon and scenario fit.

### Commercial evidence

Look for current, dated:

- product/R&D strategies;
- procurement/tenders;
- licensing/assignment/partnership activity;
- standards/regulatory changes;
- funding/capacity expansion;
- hiring and technical programs; and
- market/customer evidence supplied internally or from credible public sources.

Each signal includes source, date, fact, relevance, alternative explanation and
confidence. Recruitment, financing, procurement, citation or litigation does not prove
demand, budget, willingness, infringement or transaction probability.

### Valuation evidence

If a connector returns a value or component score:

- state model/source, unit/currency, valuation date, method description available,
  inputs, limitations and missing data;
- distinguish model estimate from formal appraisal and transaction price;
- show scenario/sensitivity where possible; and
- never create a range or “activatable amount” without defensible inputs and qualified
  valuation/finance review.

## Step 6 — Research candidate counterparties

Candidate roles may include:

- internal product/R&D team;
- licensee;
- assignee/acquirer;
- joint-development or research partner;
- option/evaluation partner;
- cross-license/pool participant;
- manufacturer, integrator, supplier or channel partner; and
- financing/pledge counterparty subject to specialist review.

Build candidates from technical complementarity, similar/adjacent patents, products,
R&D programs, ecosystem/supply relationships, jurisdictions, transaction history and
current public/internal evidence.

For each candidate record:

- resolved legal entity and corporate relationship;
- role and field-of-use hypothesis;
- technical, product, rights and geographic fit;
- dated evidence and source level;
- conflicts/exclusions and sanctions/privacy review;
- alternative explanation and uncertainty;
- internal research priority and diligence; and
- outreach authorization status.

Use `candidate counterparty` or `research lead`, never confirmed buyer/licensee/interest.
Do not infer infringement as a reason for outreach.

## Step 7 — Compare activation scenarios

For every package compare only applicable scenarios:

- internal reuse;
- retain/defensive/standards role;
- license by field/territory/exclusivity;
- assignment;
- option/evaluation;
- joint development;
- cross-license/pool/venture contribution;
- pledge/financing exploration; and
- maintenance/abandonment review.

Evaluate:

- decision objective and stakeholder;
- rights/authority readiness;
- technical/commercial evidence;
- supporting assets;
- expected resource/cost inputs if supplied;
- counterparties and conflicts;
- regulatory/tax/accounting/legal dependencies;
- confidentiality and disclosure plan;
- reversible versus irreversible consequences;
- evidence quality; and
- next validation/decision gate.

Do not issue final maintenance, abandonment, license, assignment, pledge, price,
enforcement or transaction recommendations. Present supported options to authorized
decision makers and qualified reviewers.

## Step 8 — Segment the portfolio

Use descriptive or user-approved categories. If the user requires A–E labels, define
them for this project and show the rubric, gates and sensitivity. Do not inherit fixed
score ranges.

Hard gates may cap readiness, but must be jurisdiction- and objective-specific. Examples:

- unresolved ownership/authority;
- missing application/field of use;
- insufficient independent evidence;
- unreviewed confidentiality/export/sanctions/ethics/biosafety constraints;
- expired/lapsed rights without a separately supported non-patent package; and
- model-score conflict with status/transaction evidence.

Do not hide a blocking issue inside a composite score.

## Step 9 — Create deliverables

Follow `references/output-spec.md`.

Default to HTML only when inputs and authorization support a real report. Create PDF,
DOCX, XLSX or PPTX only when requested/authorized and use the appropriate verified
artifact workflow.

Include as relevant:

- management summary;
- activation funnel and evidence coverage;
- portfolio master table;
- selected asset/package briefs;
- candidate-counterparty table;
- diligence and evidence gaps;
- 30/60/90-day plan;
- method, source hierarchy and limitations;
- evidence register; and
- patent-link/unlinked-identifier note.

### Patent links

Use only URLs returned by or officially documented for the active global service.
Never construct a regional URL from `patent_id`. If unavailable, preserve the identifier,
source and evidence ID and list it as unlinked.

### Internal versus external

Create only the audience version authorized:

- **Internal:** may include controlled evidence, internal decisions and diligence under
  project permissions.
- **External/NDA-safe:** remove confidential technical detail, negotiating positions,
  personal data, internal costs/thresholds, restricted sources and post-NDA materials.

## Step 10 — Build the action plan

For each supported action record:

- phase (30/60/90-day or project-defined);
- objective and action;
- responsible role only if approved;
- required materials/evidence;
- dependency/blocking gate;
- deliverable and acceptance criterion;
- due date only if supplied/scheduled; and
- decision/reviewer role.

Do not invent owners, dates, progress, buyer responses or monetary targets.

## Step 11 — Sequential role review

Preserve the source’s role separation as a sequential self-review checklist:

1. asset normalization and rights-data review;
2. technical evidence and search-boundary review;
3. public/internal commercial-signal review;
4. candidate-entity and exclusion review;
5. scenario/transaction/diligence review;
6. visual/artifact review; and
7. independent final QA against sources and authorization.

Do not automatically spawn or delegate based on portfolio size. Batch deterministically,
persist checkpoints and stop if the portfolio exceeds safe resources.

## Step 12 — Final QA and handoff

### Evidence and scope

- Review population and “underused” definition are explicit.
- Internal-use/transaction-history gaps remain unknown.
- Every material fact has source/date and evidence level.
- Search results distinguish complete, capped, sampled and selected records.
- Entity, asset and family mappings reconcile.

### Rights and decisions

- Ownership, authority, co-owner, license, encumbrance, funding, term/status, challenge,
  regulatory and disclosure gates are visible.
- Database/model results are not legal assurance or formal valuation.
- Counterparties are research leads, not confirmed interest.
- No irreversible decision or outreach exceeds authorization.

### Rubric and scenarios

- Dimensions, weights, missing data, gates and sensitivity are transparent.
- No fixed quota/cutoff creates false precision.
- Every activation option lists dependencies, evidence and next gate.

### Deliverables

- Content matches the confirmed audience and formats.
- HTML is offline, semantic, safe, accessible, responsive and printable.
- PDF/DOCX/XLSX/PPTX, if requested, passes format-specific render/data QA.
- Patent links are verified global URLs or identifiers remain unlinked and documented.
- No secret, local path, confidential leak, fake value, buyer, progress or source remains.

Return absolute paths, portfolio/scope/cutoff, included sections, unresolved professional
reviews and release status. Do not describe an unreviewed artifact as client-ready.

## Stop conditions

Stop or narrow when:

- owner/authority, population or objective is unresolved;
- internal-use/transaction evidence is required but unavailable;
- ownership, licenses, encumbrances, term/status or funding obligations conflict;
- the required connector/source is unavailable or stale;
- search caps prevent a requested population conclusion;
- a value/score lacks method, unit/date or provenance;
- counterparty identity or current evidence cannot be verified;
- confidential or restricted data cannot be handled safely;
- sanctions/export/competition/privacy/tax/accounting/valuation/legal review is needed;
- portfolio size exceeds safe batch/checkpoint resources;
- outreach or external disclosure lacks explicit authorization; or
- artifact validation fails.

Return completed work, failed evidence/gate, affected assets/options and exact next step.
Do not fill gaps with a plausible valuation, use history, buyer, transaction path,
maintenance decision or report claim.

