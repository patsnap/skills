---
name: review-japanese-patent-claims-ip
description: Review claims in a Japanese patent application or a PCT/Paris-route application intended for Japan across six dimensions: Japanese Patent Act/JPO compliance, evidence-backed novelty and inventive-step pre-screening, claim architecture and drafting quality, JPO examination risk, foreign-origin and translation risk, and strategic protection. Use when the user provides Japanese or foreign-language application materials and asks for a JPO-oriented claim review, amendment options, prosecution-readiness assessment, prior-art comparison, or a complete English HTML claims report.
---

# Review Japanese Patent Application Claims

## Role and legal boundary

Act as an evidence-bound patent drafting and examination-review assistant. Do
not claim to be a Japanese patent attorney (`benrishi`), law firm, examiner, or
substitute for qualified Japanese counsel.

Review the supplied claims against current official Japanese Patent Act and JPO
examination materials, including:

- description and claims requirements under Article 36;
- novelty and inventive step under Article 29(1) and (2);
- secret prior art under Article 29bis where relevant;
- prior application under Article 39 where relevant;
- unity under Article 37;
- amendment/new-matter and purpose restrictions under Article 17bis; and
- foreign-language and international-application rules where applicable.

Official starting points, rechecked at execution time:

- JPO Examination Guidelines for Patent and Utility Model in Japan:
  `https://www.jpo.go.jp/e/system/laws/rule/guideline/patent/tukujitu_kijun/index.html`
- JPO Examination Handbook case examples:
  `https://www.jpo.go.jp/e/system/laws/rule/guideline/patent/handbook_shinsa/document/index/app_a_e.pdf`
- JPO PCT national-phase guidance:
  `https://www.jpo.go.jp/e/system/patent/pct/designated/pct_applications.html`
- JPO restriction on multi-multi claims:
  `https://www.jpo.go.jp/e/system/patent/shinsa/multimulticlaims.html`

JPO English texts may be provisional translations; where interpretation is
ambiguous, the current Japanese text and qualified Japanese counsel control.

This is an application/examination-readiness review. Do not equate it with a
final validity, enforceability, opposition/invalidation, infringement, FTO, or
claim-construction opinion.

## Trigger conditions

Use this skill when the user:

- uploads a Japanese patent application, PCT application, priority application,
  or draft intended for Japan;
- asks whether claims meet JPO clarity/support/enablement requirements;
- requests a novelty/inventive-step pre-screen under Japanese practice;
- requests Japanese claim architecture or amendment options;
- asks about PCT-to-Japan or Paris-route claim/translation issues;
- requests a strategic fallback-position review; or
- requests a complete HTML Japanese claims-review report.

Do not use it for a Japanese utility model without adapting for the materially
different basic-requirements/technical-opinion framework and clearly stating
the change.

## Required inputs

Obtain or explicitly mark missing:

### Application package

- complete claims;
- description/specification;
- drawings and reference numerals;
- abstract;
- filing/application metadata;
- priority applications and priority claims;
- PCT publication, Article 19 claims, Article 34 amendments, ISR/WO-ISA/IPRP,
  when applicable;
- current Japanese translation and source-language text;
- amendments, office actions, opinions, decisions, or interview records;
- applicant's commercial/technical objectives; and
- intended claim categories and fallback priorities.

### Search scope

- effective filing/priority date for each claimed subject matter;
- known disclosures and inventor/applicant publications;
- target technology, synonyms, classifications, assignees, inventors, and
  languages;
- geographic/database scope;
- search cutoff and family-counting rule;
- known closest prior art; and
- user-approved search queries or approval of generated queries.

### Route and procedural context

- direct Japanese filing;
- Paris Convention filing;
- PCT national phase in Japan;
- foreign-language written application;
- current prosecution stage;
- current/final notice status;
- examination request status; and
- amendment constraints/time limits.

Do not guess procedural deadlines. Verify current official JPO/WIPO guidance
against the actual filing/priority dates and documents. JPO currently states
that PCT national-phase documents and required Japanese translations generally
must be submitted within 30 months from the priority date, with specific special
translation/reinstatement rules; recheck before relying on this statement.

## Required output

Generate one complete, safe, static English HTML report in the user-approved
output directory. Suggested filename:

```text
japanese_patent_claims_review.html
```

Include:

1. executive conclusion and review readiness;
2. application/route metadata and missing-input register;
3. claim inventory and dependency tree;
4. six-dimension review;
5. prior-art search protocol and evidence table;
6. claim-to-reference limitation charts;
7. claim-by-claim issue and amendment table;
8. overall and priority ratings with transparent criteria;
9. mandatory actions, owners, and counsel-review gates;
10. legal/search/translation limitations;
11. source and query register; and
12. reviewer sign-off.

Do not add a template or script file to the skill package; this package has one
source file only.

## Five-step workflow

### Step 1 — Parse and freeze the application package

Extract without silently normalizing substantive text:

- application/publication/priority/PCT identifiers;
- applicant and inventors;
- filing, priority, publication, and translation dates;
- title and technical field;
- every claim number and exact text;
- independent/dependent status;
- dependency and multi-dependency;
- claim category;
- paragraph and drawing locators;
- reference numerals;
- source language and translation version; and
- prosecution/amendment version.

Create a claim inventory:

| Claim | Version | Category | Independent/dependent | Depends on | Multi-multi | Key limitations | Spec/drawing basis | Translation state |
|---:|---|---|---|---|---|---|---|---|

Create a machine- and human-readable claim tree. Detect:

- missing or duplicate claim numbers;
- circular or invalid dependencies;
- dependency on cancelled claims;
- multiple dependent claims;
- multi-multi claims prohibited under current JPO practice;
- category shifts;
- inconsistent terminology;
- reference-numeral inconsistencies; and
- missing source/translation versions.

Determine route:

- direct Japanese application;
- Paris Convention route;
- PCT national phase;
- foreign-language written application; or
- unknown.

If description/drawings/priority text are missing, continue with a claims-only
screen but mark support, enablement, new matter, priority entitlement, and
translation conclusions `not_assessable`.

### Step 2 — Review all six dimensions

#### Dimension 1 — Article 36 and formal/legal compliance

Review each claim and the claim set for:

##### Clarity

- unclear antecedent basis;
- inconsistent labels for the same feature;
- relative or subjective terms without objective boundary;
- undefined parameters, measurement conditions, ranges, or units;
- ambiguity between structural, functional, process, and result limitations;
- optional/permissive wording;
- contradictory limitations;
- unclear Markush alternatives;
- unclear negative limitations/disclaimers;
- unclear numerical endpoints, rounding, significant figures, or test methods;
- reference-numeral misuse; and
- claim/category mismatch.

Do not flag a term merely because it is broad. Explain why the claim boundary
cannot be understood in its application context.

##### Support

- map every limitation to exact description/drawing support;
- determine whether scope exceeds the disclosed generalization;
- identify single-example overgeneralization;
- review genus/species, ranges, alternatives, parameter spaces, and functional
  results;
- distinguish literal support from inferred support; and
- identify contrary embodiments or definitions.

Proposed amendments require a direct, traceable basis. Do not invent a basis.

##### Enablement and description sufficiency

- identify the claimed scope and skilled-person assumptions;
- check disclosed implementation across the scope;
- identify undue experimentation risks;
- review essential conditions, materials, algorithms, parameters, controls, and
  measurement methods;
- distinguish aspirational effects from enabled technical teaching; and
- note fields where working examples/data may be expected.

##### Claim statement and dependency requirements

- correct claim numbering and dependency;
- permissible multiple dependency;
- JPO multi-multi restriction;
- claim categories and statutory subject matter;
- concise but complete limitation statements;
- incorporation by reference or vague external definition; and
- unity indicators for later analysis.

Output for Dimension 1:

| Issue ID | Claim(s) | Requirement | Exact text | Finding | Basis/evidence | Severity | Amendment direction | Counsel gate |
|---|---:|---|---|---|---|---|---|---|

#### Dimension 2 — Evidence-backed novelty and inventive-step pre-screen

This dimension requires real prior-art research when the user authorizes it and
search access exists. Use the verified evidence workflow below; do not invoke or
simulate an unavailable helper.

Use the verified PatSnap workflow below. If search cannot be performed, label
the dimension `Search not performed`; provide only a search plan and drafting
observations, never a novelty/inventive-step conclusion.

##### Required PatSnap MCP services

Advanced Patent Search — Required:

- connector key: `advanced_patent_search`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-search`
- official page:
  `https://open.patsnap.com/marketplace/mcp-servers/patent-search`
- role: query, semantic, classification, assignee, inventor, similar-patent,
  citation, and filtered retrieval as supported by current tools.

Patent Briefing — Required for cited references:

- connector key: `patent_briefing`
- Official marketplace page: `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- official page:
  `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing`
- role: bibliography, priority/family, status metadata, claims, descriptions,
  translations, images, and technical summaries as supported.

Record connector, tool, normalized request, query, filters, cutoff, retrieval
time, result identifiers, and source locator. Do not imply a connector call if
one was not executed.

##### Search protocol

1. Freeze each independent claim version.
2. Decompose each into individually testable limitations.
3. Identify essential technical relationships, not just nouns.
4. Create a synonym/concept/classification matrix in relevant languages.
5. Confirm the effective date for each subject matter and priority support.
6. Search exact phrases, concepts, classifications, assignees/inventors,
   citations, and similar patents as appropriate.
7. Search patent and relevant non-patent literature where authorized.
8. Cover jurisdictions/databases appropriate to technology, language, and date;
   JP, WO, US, EP, CN, and KR are common sources but not a completeness limit.
9. Deduplicate by a declared family rule.
10. Retrieve full references, not title/abstract snippets only.
11. Verify public availability date and priority/publication chronology.
12. Map every claim limitation to each candidate reference.
13. Preserve contrary evidence and missing disclosure.
14. Document search limits and unsearched sources/languages.

##### Novelty analysis — Article 29(1)

For each independent claim, determine whether one pre-effective-date reference
discloses every limitation and required relationship, expressly or as supported
by the applicable standard. Do not mosaic references for novelty. Do not treat
title/abstract similarity, same purpose, or overlapping keywords as full
disclosure.

Use a limitation chart:

| Claim | Limitation | Reference | Exact passage/figure/claim | Disclosure state | Date relevance | Translation | Contrary evidence |
|---:|---|---|---|---|---|---|---|

Disclosure states:

- `expressly disclosed`;
- `arguably implicit — legal review required`;
- `not disclosed`;
- `uncertain translation`;
- `date/availability unresolved`; and
- `source not retrieved`.

##### Inventive-step analysis — Article 29(2)

For each claim:

1. identify a reasoned primary reference/starting point;
2. state differences limitation by limitation;
3. formulate the technical problem without hindsight or embedding the solution;
4. identify alleged motivation/suggestion, common general knowledge, design
   variation, or combination rationale;
5. assess technical-field proximity and problem/operation/function similarity;
6. assess obstacles, teaching away, incompatible purposes, or required redesign;
7. evaluate advantageous effects with application support and comparative
   relevance;
8. consider predictability, parameter optimization, selection invention,
   numerical ranges, and aggregation versus combination as applicable;
9. identify hindsight risk; and
10. state missing evidence.

Use the Japanese examination framing and current JPO examples, not a mechanical
US `motivation to combine` test or EPO problem-solution formula presented as
Japanese law.

##### Problem–solution–effect record

For each independent claim record:

| Claim | Objective technical problem | Claimed means/relationships | Supported effect | Closest evidence | Difference | Why easy/not easy | Confidence |
|---:|---|---|---|---|---|---|---|

##### Output states

Use provisional, evidence-bound states:

- `No single anticipation reference identified in this search`;
- `Potential anticipation — counsel review required`;
- `Inventive-step challenge appears material`;
- `Inventive-step position appears arguable`;
- `Evidence incomplete`;
- `Date/priority unresolved`; and
- `Search not performed`.

Never state `valid`, `invalid`, `novel`, `inventive`, or `stable` as a final legal
conclusion from a bounded search.

#### Dimension 3 — Claim architecture and drafting quality

Review:

- independent claim categories and strategic purpose;
- dependency tree and progressive fallback positions;
- whether dependent claims add meaningful limitations;
- consistent breadth across apparatus/system/method/product/use/program/media
  categories where appropriate;
- essential feature placement;
- avoidable process limitations in product/apparatus claims;
- product-by-process wording and risk;
- functional/result-to-be-achieved wording and support;
- means-plus-function-like ambiguity;
- parameter and range drafting;
- Markush groups;
- negative limitations;
- optional features;
- omnibus/external references;
- claim differentiation without relying on another jurisdiction's doctrine;
- redundancy, gaps, and contradictory claims;
- Japanese translation economy and precision; and
- prosecution-friendly amendment paths.

Create a claim architecture table:

| Independent claim | Category | Core inventive concept | Breadth | Main fallback claims | Missing fallback | Cross-category alignment | Drafting risk |
|---:|---|---|---|---|---|---|---|

#### Dimension 4 — JPO examination-practice risks

Review current JPO practice for:

- unity under Article 37 and special technical features;
- multi-multi claim restriction;
- description/claim clarity, support, and enablement;
- category and expression-specific guidance;
- product-by-process claims;
- functional language and results;
- numerical limitations and selections;
- new matter under Article 17bis(3);
- amendment-purpose restrictions, including final-notice context;
- amendment changing special technical features;
- prior application/secret prior art;
- examiner search/claim interpretation risks;
- communication/response posture; and
- request-for-examination/procedural facts when relevant.

Distinguish:

- issue in the filed claims;
- likely reason for refusal;
- amendment constraint caused by procedural stage;
- optional drafting improvement; and
- matter requiring Japanese counsel.

Do not invent an examiner outcome or deadline.

#### Dimension 5 — Foreign-origin, PCT, Paris, and translation risk

Apply only when relevant.

##### Text/version reconciliation

Create a side-by-side record:

| Claim | Priority/PCT/source text | Current Japanese text | Approved English rendering | Substantive difference | Risk | Action |
|---:|---|---|---|---|---|---|

Review:

- missing/added limitations;
- antecedent and dependency changes;
- singular/plural and article effects;
- technical term consistency;
- functional/causal relationship changes;
- numerical range/unit changes;
- negative limitations;
- claim category changes;
- translation of PCT Article 19/34 amendments;
- basis for post-entry amendments; and
- whether priority text supports each claimed subject matter.

##### PCT-to-Japan controls

Verify current facts for:

- 30-month national-document/translation period;
- special translation time limit where applicable;
- translation of description, claims, drawing text, and abstract;
- Article 19/34 amendment translations;
- domestic representative requirements for overseas applicants;
- examination-request deadline; and
- reinstatement/fees/procedural relief.

Use the current JPO guidance cited above; do not carry fees or dates into a
report without a current check.

##### Paris-route controls

Verify:

- first application and 12-month patent-priority period;
- priority document/claim requirements;
- priority entitlement and applicant/successor facts;
- subject-matter support for each claim;
- intervening disclosures; and
- Japanese filing/translation consistency.

Translation review is not certification. Require a qualified Japanese patent
professional/translator for filing text.

#### Dimension 6 — Strategic protection assessment

Assess, with evidence:

- whether independent claims protect distinct commercially relevant concepts;
- whether essential implementation variants are covered;
- whether fallback claims preserve useful scope;
- whether competitors can omit/substitute/reorder features;
- whether claim categories cover relevant acts and product architecture;
- whether interface, control, manufacturing, maintenance, software, data, and
  system-level aspects need separate protection;
- whether trade secret, design, trademark, copyright, contract, or defensive
  publication may complement patents;
- whether divisional/continuation opportunities exist under current Japanese
  procedure and disclosure; and
- whether foreign/Japanese portfolios require coordinated scope.

Do not state infringement or design-around success without product evidence and
claim construction. Recommendations must trace to the specification and
business objective.

### Step 3 — Produce claim-by-claim amendment options

For every claim, include:

| Claim | Exact current text | Issue(s) | Requirement/evidence | Conservative amendment | Balanced amendment | Strategic fallback | Basis locator | Scope effect | Search impact | Translation note | Counsel gate |
|---:|---|---|---|---|---|---|---|---|---|---|---|

#### Amendment disciplines

- Quote exact current text.
- Preserve the claim version.
- Provide basis by paragraph/drawing/claim and source language.
- Do not add unsupported subject matter.
- Do not silently narrow or broaden.
- Explain every added, deleted, or changed limitation.
- State effect on dependent claims.
- Re-run novelty/inventive-step mapping for materially changed claims.
- Recheck unity/category/dependency/multi-multi issues.
- Reconcile Japanese and source-language wording.
- Identify procedural limits from current prosecution stage.
- Mark proposed wording `illustrative — Japanese counsel review required`.

If basis is missing, do not draft the amendment as if permitted. State `No
verified basis identified` and list the evidence needed.

### Step 4 — Rate readiness and prioritize actions

Do not use unexplained stars, percentages, traffic lights, or color-only ratings.

#### Overall examination-readiness rating

Use:

- `Ready for filing/examination review`;
- `Conditionally ready — targeted corrections required`;
- `Material revision required`; or
- `Not assessable from supplied materials`.

Rate using explicit components:

| Component | State | Evidence | Blocking issue | Required action |
|---|---|---|---|---|
| Article 36 clarity/support/enablement | | | | |
| Claim architecture/dependency | | | | |
| Novelty search | | | | |
| Inventive-step evidence | | | | |
| JPO procedure/amendment constraints | | | | |
| Translation/route consistency | | | | |
| Strategic fallback coverage | | | | |

#### Search-based patentability risk

Use:

- `Higher provisional examination risk`;
- `Moderate provisional examination risk`;
- `Lower provisional risk in this bounded search`; or
- `Not assessed / evidence incomplete`.

State search scope, effective date, references, unmapped limitations, languages,
databases, cutoff, and uncertainty. Never call this `right stability` without a
full legally appropriate analysis.

#### Priority levels

- **Required before filing/response** — legal/formal, deadline, new matter,
  translation, dependency, or material prior-art issue.
- **High** — likely examination issue or loss of material strategic scope.
- **Medium** — drafting robustness/fallback improvement.
- **Monitor** — future prosecution/market/technology trigger.

Every action includes owner role, due date/decision gate, evidence dependency,
and completion criterion.

### Step 5 — Generate and validate the HTML report

Use one continuous static HTML file with:

- skip link;
- report header and metadata;
- sticky or responsive table of contents;
- executive conclusion;
- claim tree/inventory;
- six numbered review-dimension sections;
- evidence/search section with queries, references, limitation charts, and
  source cards;
- claim-by-claim amendment table;
- rating and action register;
- missing-input/limitations/source register; and
- sign-off.

#### Scientific/legal visual system

- white paper background;
- navy/charcoal text;
- one teal accent;
- text severity/status labels;
- semantic headings and tables;
- captions and source notes;
- local overflow for wide tables;
- responsive layout at 390 px;
- reduced-motion support;
- Letter/A4 print CSS; and
- no gradients, glow, 3D, decorative badges, emoji, or color-only meaning.

#### Static security

- Escape every dynamic value.
- Permit only absolute HTTP(S) URLs.
- Use `target="_blank" rel="noopener noreferrer"` externally.
- No script or inline event handler.
- No `javascript:` or `data:text`.
- No untrusted raw HTML from documents, APIs, searches, or model output.
- No credential, personal path, hidden prompt, or local link.

#### Required report sections

1. Scope, legal boundary, and missing inputs.
2. Application metadata and route.
3. Claim inventory/tree.
4. Executive readiness conclusion.
5. Dimension 1 — Article 36 compliance.
6. Dimension 2 — novelty/inventive-step search evidence.
7. Dimension 3 — claim architecture/drafting.
8. Dimension 4 — JPO practice/procedural risk.
9. Dimension 5 — foreign/PCT/Paris/translation risk.
10. Dimension 6 — strategic protection.
11. Claim-by-claim amendments.
12. Ratings and prioritized actions.
13. Search/query/source register.
14. Limitations and reviewer sign-off.

## Search evidence contract

For each search record preserve:

- search ID;
- target claim/version;
- approved query;
- query origin and approver;
- connector/tool or database;
- filters and classifications;
- jurisdictions/languages;
- cutoff/retrieval time;
- family rule;
- result identifiers;
- candidate selection reason;
- full-text retrieval state; and
- error/limitation.

For each reference preserve:

- publication/application/grant identifiers;
- title;
- authority;
- applicant/assignee;
- priority, filing, publication dates;
- family/member used;
- legal-status metadata as of date;
- cited claims/passages/figures;
- translation/source language;
- public-availability assessment;
- relevance to each limitation; and
- source URL/locator.

No API/search result means `no returned record in this query`, not `no prior
art`.

## Missing-input and partial-review rules

| Missing material | Permitted work | Prohibited conclusion |
|---|---|---|
| Description/drawings | Claim grammar, dependency, preliminary clarity | Support, enablement, new matter, complete amendment basis |
| Priority application | Claim drafting and bounded search | Priority entitlement/effective date for added subject matter |
| Japanese translation | Source-language claim analysis | Japanese text accuracy/compliance |
| Search access | Search strategy and drafting observations | Novelty/inventive-step finding |
| Full reference text | Candidate relevance from metadata/snippet | Limitation disclosure conclusion |
| Effective date | General search and issue spotting | Date-qualified novelty conclusion |
| Prosecution history | Filed-claim review | Procedural amendment availability/current-stage advice |
| Business/product evidence | Drafting/examination review | Strategic commercial coverage/design-around conclusion |

Continue useful work but display the limitations prominently.

## Final acceptance checklist

### Source and parsing

- [ ] All supplied files and versions are inventoried.
- [ ] Every claim is captured exactly once.
- [ ] Claim dependencies/tree reconcile.
- [ ] Application route and stage are identified or marked unknown.
- [ ] Japanese/source/English text versions are distinguished.

### Six dimensions

- [ ] Dimension 1 covers clarity, support, enablement, statement/dependency.
- [ ] Dimension 2 uses real search evidence or clearly says search not performed.
- [ ] Dimension 3 covers categories, fallbacks, dependencies, functional/range
  and strategic architecture.
- [ ] Dimension 4 covers unity, multi-multi, amendment/new matter, JPO practice.
- [ ] Dimension 5 covers route, priority, translation, Article 19/34 where relevant.
- [ ] Dimension 6 covers strategic scope/fallback/design-around/IP-mode issues.

### Search

- [ ] Every query and connector/tool is recorded.
- [ ] Effective dates and public availability are addressed.
- [ ] Novelty uses one-reference limitation mapping.
- [ ] Inventive step states references, differences, rationale, effects, and
  hindsight/contrary evidence.
- [ ] Full sources, not title-only snippets, support mappings.
- [ ] Search limits and unsearched sources/languages are explicit.
- [ ] No final validity/stability conclusion appears.

### Amendments

- [ ] Every claim receives issue/action treatment.
- [ ] Proposed wording has verified basis or explicitly lacks it.
- [ ] Scope effect and dependent-claim impact are stated.
- [ ] Changed claims are rechecked against search evidence.
- [ ] Japanese counsel/translation gates are visible.

### HTML

- [ ] One complete English HTML report.
- [ ] All required sections and navigation targets appear.
- [ ] Dynamic values are escaped.
- [ ] No script, handler, unsafe URL, credential, or local path.
- [ ] Tables are semantic and scroll locally.
- [ ] Text, not color alone, conveys status.
- [ ] Mobile and print layouts are legible.
- [ ] Source and query registers resolve all citations.

### Localization

- [ ] No Chinese interface text or China marketplace link remains.
- [ ] No unavailable named skill dependency remains.
- [ ] Only verified global PatSnap MCP services appear.
- [ ] Current official JPO sources support legal/procedural statements.
- [ ] Japanese legal terms are not replaced by foreign analogues.
- [ ] Fees/deadlines are verified at execution time.

## Final disclaimer

State prominently:

> This report is an evidence-bound Japanese patent application and examination
> readiness review. It is not a legal opinion on validity, enforceability,
> infringement, freedom to operate, or final patentability. Prior-art searches
> are bounded by the documented databases, queries, languages, dates, and
> access. Proposed Japanese wording, amendments, priority positions, and
> procedural actions require review by qualified Japanese patent counsel and,
> where applicable, a qualified translator.
