---
name: review-fto-report-quality-ip
description: Review the quality, reproducibility, legal reasoning, and decision usefulness of an existing freedom-to-operate (FTO), patent-infringement-risk, or event IP risk report. Use for three-layer evidence review, four-dimension scoring, independent multi-route search comparison, omission analysis, fatal-defect screening, remediation planning, or HTML assessment generation. The skill audits a supplied report; it does not replace a jurisdiction-specific legal opinion.
---

# Review FTO Report Quality

Version: 9.0 localized international edition

## Purpose

Assess whether an existing FTO or patent-risk report is:

- factually supported and reproducible;
- legally reasoned for the stated jurisdiction and date;
- useful for a defined business decision;
- transparent about search, family, status, and claim-version limits;
- internally consistent across findings, scores, and recommendations.

The package contains two operating modules and an optional harness:

1. review the supplied report and its evidence;
2. independently compare search coverage through multiple routes;
3. optionally validate the generated HTML and cross-field consistency.

When this skill is used for a formal assessment, generate the final HTML with
`scripts/generate_report.py`. Run `scripts/validate_report.py` when the user
requests validation, when the output will enter a controlled workflow, or when
the assessment is materially edited after generation.

## What this skill does not do

- It does not guarantee freedom to operate.
- It does not establish that every relevant patent has been found.
- It does not treat a pending application as an enforceable patent claim.
- It does not infer current legal status from stale or missing data.
- It does not substitute generic rules for jurisdiction-specific law.
- It does not turn route overlap into a validated recall percentage.
- It does not provide a legal opinion unless appropriately qualified counsel
  separately adopts the analysis for the applicable jurisdiction.

## Source-faithful v9 capabilities

The localized workflow preserves the source package's substantive upgrades:

| Capability | Localized implementation |
|---|---|
| Scenario recognition | Target-market dimension × decision-use dimension |
| Search verification | Multiple independent routes plus a temporal watchlist |
| Coverage evaluation | Observed union, route overlap, omissions, and limitations |
| Fatal defects | Non-compensable override shown above the numerical score |
| Output modes | Standard sequence or executive-summary-first presentation |
| Recommendations | Priority, rationale, owner, trigger, dependency, and timing |
| Visual evidence | Accessible tables and labeled indicators; color is never the sole signal |
| Harness | Structural, evidence, legal-language, visual, and logic checks |

The Chinese source describes a five-route search and a Jackknife estimate, but
its bundled guide and script implement a two-pool Chapman estimator. Patent
search routes are ordinarily correlated, so their overlap does not establish
true recall. This edition preserves all search routes, route provenance,
overlap, observed union, and omission analysis. A numerical estimate may be
reported only as a qualified heuristic when the estimator, pools, assumptions,
and limitations are explicit. Otherwise report `Not estimated`.

## Trigger boundary

Use this skill when the user supplies or identifies an existing report and asks
to:

- audit its quality;
- check whether the search was adequate or reproducible;
- review claim-chart or infringement-risk reasoning;
- compare the report with an independent patent search;
- identify omitted families or stale legal-status evidence;
- score report quality or prepare a remediation plan;
- validate an assessment produced by this package.

Do not use it as the primary workflow when the user has no existing report and
only wants a new FTO screening. In that situation use the appropriate FTO
search/report workflow, then use this skill as a quality-control layer.

## Required inputs

Collect the following from the report or the user. Extract from the report
before asking follow-up questions.

### Decision context

- target product, process, service, or technical implementation;
- exact version, configuration, components, and known alternatives;
- intended activity: make, use, sell, offer, import, export, supply, or launch;
- target countries or regions;
- decision and audience: launch gate, design freeze, transaction, diligence,
  event participation, recurring monitoring, or counsel review;
- required decision date and risk tolerance.

### Report identity

- report title, author, commissioning party, and issue date;
- search cutoff and legal-status cutoff;
- report version and superseded versions;
- stated scope, exclusions, assumptions, and reliance restrictions;
- databases, tools, and external providers used.

### Search record

- concepts and decomposed technical features;
- keywords, synonyms, translations, spelling variants, and proximity logic;
- IPC/CPC or jurisdiction-specific classifications;
- assignee, inventor, citation, and competitor routes where relevant;
- queries, database fields, dates run, result counts, and deduplication rules;
- family definition and counting convention;
- inclusion, exclusion, and relevance-screening criteria.

### Patent-analysis record

- higher-, moderate-, and lower-risk patents or families;
- publication, application, and grant identifiers;
- jurisdiction, family members, owner, and legal-status evidence;
- claims reviewed, claim version, amendments, translations, and status date;
- claim charts or element-by-element comparisons;
- product evidence mapped to each limitation;
- validity, prosecution-history, priority, terminal-disclaimer, opposition,
  reexamination, litigation, and expiry evidence where relevant;
- pending applications maintained separately as a watchlist.

If an input is unavailable, preserve the gap. State its consequence and the
action needed to close it. Never invent a query, source, status, claim text,
score, search result, or verification date.

## Scenario matrix

Classify the assessment on two dimensions.

### Target-market dimension

| Code | Market posture | Review emphasis |
|---|---|---|
| M1 | One identified jurisdiction | Local claims, status, remedies, and activity |
| M2 | Several identified jurisdictions | Family divergence and country-by-country status |
| M3 | International launch or supply chain | Import/export exposure and jurisdiction prioritization |
| M4 | Market not yet fixed | Explicit provisional scope and decision gates |

### Decision-use dimension

| Code | Intended use | Review emphasis |
|---|---|---|
| U1 | Early technical screening | Coverage, uncertainty, and design alternatives |
| U2 | Launch or commercialization gate | Current claims, status, claim mapping, and actionability |
| U3 | Transaction or diligence | Ownership, family integrity, materiality, and reliance limits |
| U4 | Event or exhibition preparation | Venue-specific activity, rapid escalation, and evidence pack |
| U5 | Monitoring | Update triggers, pending claims, competitors, and cadence |

Retain a 100-point total. Scenario adaptation redistributes emphasis within
dimensions; it does not silently change the denominator. Record the selected
matrix cell and every weight adjustment in the report.

## Fatal-defect override

A fatal defect makes the report unsuitable for the stated decision regardless
of its numerical score. Continue the full assessment so remediation remains
actionable.

### Fatal conditions

| ID | Condition | Why it is non-compensable |
|---|---|---|
| FTL-01 | No identifiable target product/process or version | Claims cannot be mapped to an undefined subject |
| FTL-02 | No target market or jurisdiction | Patent rights and infringement standards are territorial |
| FTL-03 | Material conclusions rely on fabricated, unverifiable, or mismatched patent evidence | The factual foundation is unreliable |
| FTL-04 | No claim-level basis for a material infringement conclusion | Bibliographic similarity is not a claim comparison |
| FTL-05 | Material status or claim version is missing and the report presents a definitive conclusion | The legal premise is unbounded |
| FTL-06 | A known higher-risk finding is omitted or contradicted without explanation | Decision-makers receive a materially distorted picture |
| FTL-07 | The report gives an absolute non-infringement assurance unsupported by scope and law | The conclusion exceeds the evidence |

### Output rule

- show a prominent text-labeled fatal banner at the top;
- state each fatal defect and its evidence;
- force the quality grade to `Fatal`;
- retain the numerical dimension scores for diagnostic use;
- complete all sections and mark unavailable evidence explicitly;
- do not offset a fatal defect with strong performance elsewhere.

## Three-layer review method

### Layer 1 — Evidence and reproducibility

Test whether another qualified reviewer could reconstruct the report's inputs,
search routes, result set, family consolidation, legal-status date, claim
version, and product evidence.

Key questions:

- Is the target subject and jurisdiction unambiguous?
- Are queries and database fields reproducible?
- Are family and result-count conventions stated?
- Are sources dated and linked where permitted?
- Can each material statement be traced to evidence?
- Are missing records distinguished from negative findings?

### Layer 2 — Legal reasoning

Test whether each material conclusion applies the relevant jurisdiction's law
to the current claim set and the defined commercial activity.

Key questions:

- Are enforceable claims separated from pending or expired rights?
- Is claim construction or interpretation explained where material?
- Is every limitation mapped to product/process evidence?
- Are doctrine-of-equivalents or analogous local doctrines addressed only when
  relevant and with jurisdiction-specific qualification?
- Are ownership, licence, exhaustion, safe-harbour, experimental-use, repair,
  divided-infringement, indirect-infringement, and other doctrines considered
  only when facts and local law make them relevant?
- Are validity observations kept distinct from infringement analysis?

### Layer 3 — Decision usefulness

Test whether the report enables an accountable business choice.

Key questions:

- Does the executive summary identify decision, scope, date, and residual risk?
- Are findings ranked by materiality and confidence?
- Does every material risk have a practical response path?
- Are owner, timing, dependency, trigger, and escalation point stated?
- Are monitoring and re-review triggers defined?
- Can legal, R&D, product, and management readers distinguish fact, analysis,
  assumption, and recommendation?

## Four-dimension scorecard

Use the source total of 100 points.

| Dimension | Default points | Core question |
|---|---:|---|
| A. Search-strategy quality | 25 | Was the search fit for the defined subject, market, and date? |
| B. Patent-analysis depth | 30 | Were current claims, status, and product evidence analyzed rigorously? |
| C. Legal-opinion quality | 25 | Is the legal reasoning qualified, jurisdiction-specific, and actionable? |
| D. Documentation completeness | 20 | Is the work reproducible, traceable, controlled, and reviewable? |

Use the detailed criteria in `references/assessment-checklist.md`. Do not award
points merely because a section title exists. Tie every score to observed
evidence and list the deductions.

### Grade bands

| Score | Grade | Interpretation |
|---:|---|---|
| 90–100 | Excellent | Strong evidence and decision utility; address residual issues |
| 80–89 | Good | Generally reliable with defined improvements |
| 70–79 | Adequate | Usable only within stated limitations and remediation |
| 60–69 | Needs improvement | Material gaps limit the intended decision |
| Below 60 | Unsatisfactory | Not sufficiently reliable for the intended decision |
| Any score + fatal defect | Fatal | Do not use for the intended decision until cured |

These are report-quality bands, not probabilities of infringement or legal
safe-harbour thresholds.

## Independent verification module

Run independent verification when requested, when the supplied report supports
a material launch or transaction decision, or when search quality cannot be
assessed from its record alone.

### Route 1 — Semantic concept search

- express the product or process as technical concepts;
- search claims, abstracts, and descriptions as supported;
- record query text, fields, filters, date, provider, and result count;
- preserve provenance for every retained publication.

### Route 2 — Keyword and nested Boolean search

- decompose essential and optional features;
- include synonyms, spelling variants, acronyms, translations, and proximity;
- use nested combinations to test both precision and breadth;
- document exclusions and the effect of each refinement.

### Route 3 — Classification search

- identify candidate IPC/CPC groups from seed documents and official schemes;
- search broader and narrower groups where technically justified;
- combine classifications with discriminating concepts;
- record classification versions and uncertainty.

### Route 4 — Assignee, inventor, citation, and known-player search

- normalize entity variants and ownership changes;
- search known competitors only as a supplement, not a completeness proxy;
- review backward/forward citations and examiner references when useful;
- state why each entity or seed was selected.

### Route 5 — Temporal and pending-claim watchlist

- identify recent publications and pending applications separately;
- track claims that may change during prosecution;
- define update triggers and monitoring cadence;
- do not classify pending claims as currently enforceable rights.

### MCP-assisted execution

Use only connectors that are available and configured. The tool call, request,
filters, date, and returned identifiers must be captured in the evidence log.

Preferred global PatSnap connectors:

| Connector | Identifier and endpoint | Appropriate use |
|---|---|---|
| PatSnap Patent Research | `patsnap_patent_research` · `https://open.patsnap.com/marketplace/mcp-servers/patsnap-ip-searching` | Submit and retrieve structured FTO-review tasks with `fto_review` and `get_task` |
| Advanced Patent Search | `advanced_patent_search` · `https://open.patsnap.com/marketplace/mcp-servers/patent-search` | Reproducible semantic, keyword, classification, assignee, and filtered searches |
| Patent Briefing | `patent_briefing` · `https://open.patsnap.com/marketplace/mcp-servers/patent-briefing` | Claims, translated claims, description, bibliography, family, legal status, images, and technical summary |

For deeper jurisdictional status, reexamination, litigation, or related legal
events, the optional PatSnap Global Core connector may be used when available:
[Global Core Patents](https://open.patsnap.com/marketplace/mcp-servers/core-patents).

Connector catalogue:
[PatSnap MCP Servers](https://open.patsnap.com/marketplace/mcp-servers).

Never embed a real API key in a report, script, example, or skill file. A
connector result is evidence from a named source at a stated time; it is not a
substitute for the official register or legal review when those are required.

### When connectors are unavailable

- continue the document-quality review;
- mark independent searching as not performed;
- list the unavailable routes and expected effect;
- do not fabricate results or call the report independently verified;
- provide a reproducible search plan for later execution.

### Coverage and omission analysis

For every route, retain normalized publication identifiers, family keys, and
route provenance. Report:

- unique publications and families by route;
- observed union and intersection;
- pairwise overlap or Jaccard similarity;
- families in the supplied report but not the independent union;
- families in the independent union but absent from the supplied report;
- reasons for inclusion, exclusion, deduplication, and family consolidation;
- material omissions only after claim/status/product review.

Do not call every search-only difference a report defect. Classify it as:

1. identifier or family-consolidation difference;
2. relevant but non-material additional family;
3. potentially material omission requiring claim/status review;
4. confirmed material omission supported by evidence.

### Qualified coverage estimate

The default output is `Recall: Not estimated`.

A Chapman, Jackknife, capture-recapture, or other estimator may be shown only
when all of the following are documented:

- precisely defined capture pools;
- stable deduplication and family unit;
- defensible capture independence or a model addressing dependence;
- comparable opportunity for relevant records to enter each pool;
- estimator equation, uncertainty, sensitivity, and limitations;
- clear label: `qualified heuristic, not true recall`.

Where those conditions are absent, show observed route coverage and overlap.
Never infer a no-risk conclusion from zero results.

## Six-step operating workflow

### Step 1 — Parse the report and lock scope

1. inventory every supplied file and annex;
2. extract report identity, target subject, jurisdictions, activity, dates,
   versions, authorship, and intended decision;
3. record ambiguities and missing evidence;
4. select the scenario matrix cell;
5. define the review unit: publication, application, patent, simple family, or
   extended family;
6. create an evidence register before scoring.

### Step 2 — Review search-strategy quality (25 points)

Assess target-market database coverage, feature decomposition, synonyms,
translations, classifications, assignee/citation routes, date coverage,
pending-publication risk, query reproducibility, screening criteria, result
counts, deduplication, and family method.

Do not require a fixed number of databases, a universal 20-year lookback, or a
universal freshness period. Judge scope against the technology, jurisdiction,
right type, prosecution timeline, and decision date. State why the selected
coverage is fit or insufficient.

### Step 3 — Independently search and compare

1. run the applicable routes;
2. normalize publication identifiers and family keys;
3. preserve route provenance;
4. compare the supplied set with the observed union;
5. investigate potentially material omissions;
6. verify higher-risk claim/status evidence as of a stated date;
7. maintain pending applications as a separate watchlist;
8. report limitations and unsearched areas.

Use `scripts/fto_independent_search.py` to normalize already obtained results,
merge route provenance, calculate observed overlap, list omissions, and build
the temporal watchlist. The script does not perform network searches itself.

### Step 4 — Review patent-analysis depth (30 points)

For each material family:

- identify the correct jurisdictional member and current claim set;
- distinguish application, publication, grant, and family identifiers;
- trace owner and status to dated evidence;
- map each claim limitation to product/process evidence;
- identify missing limitations, contested interpretations, and equivalents;
- separate infringement, validity, enforceability, ownership, and commercial
  exposure;
- explain risk tier and confidence;
- link the conclusion to the report's defined activity and product version.

### Step 5 — Review legal-opinion quality (25 points)

Assess whether the report:

- states applicable jurisdictions and legal sources;
- applies the correct infringement framework;
- handles claim construction and equivalents with appropriate qualification;
- addresses indirect or divided infringement only where relevant;
- distinguishes pending from enforceable claims;
- avoids conflating validity arguments with a non-infringement conclusion;
- explains assumptions and uncertainty;
- gives prioritized mitigation tied to specific findings;
- treats SEP/FRAND, regulatory, customs, exhibition, or supply-chain issues only
  when the facts and jurisdiction warrant them.

### Step 6 — Review documentation and generate output (20 points)

Check source citations, queries, result counts, screening records, family map,
claim versions, status dates, product evidence, reviewer identity, approvals,
version history, annexes, unresolved issues, and re-review triggers.

Then:

1. complete `assets/assessment-report-template.md` or the equivalent data model;
2. populate all required sections, including explicit missing-evidence states;
3. generate HTML with `scripts/generate_report.py`;
4. validate with `scripts/validate_report.py` when applicable;
5. resolve fatal/error harness findings or record why they remain;
6. deliver the HTML plus the evidence and limitation summary requested by the
   user—without adding files to this skill package.

## Output modes

### Mode A — Standard review sequence

Use the fixed sixteen-section sequence generated by the script. This mode is
best for legal, IP, and technical reviewers who need the audit trail.

### Mode B — Executive-summary-first reading

Keep the same underlying sections and evidence, but lead the user-facing
presentation with:

1. decision and scope;
2. fatal-defect status;
3. overall grade and four-dimension score;
4. top findings and omissions;
5. prioritized actions and decision gates;
6. limitations and counsel-review boundary.

Do not delete the detailed review merely because an executive reader is the
primary audience.

## Mandatory report modules

The source defines thirteen substantive modules. The generator expresses them
through sixteen stable sections:

1. report identity and scope;
2. executive summary;
3. three-layer review overview;
4. four-dimension scorecard;
5. independent-search comparison and omissions;
6. search-topic fit;
7. search-scope coverage;
8. claim-comparison rigor;
9. higher-risk patent list;
10. moderate-risk patent list;
11. lower-risk patent list;
12. response-measure quality;
13. risk-mitigation recommendations;
14. consolidated issue register;
15. conclusion and remediation plan;
16. review boundary and disclaimer.

Every module must contain evidence, an explicit not-applicable rationale, or a
clear missing-evidence statement. Empty decorative sections are not acceptable.

## Recommendation design

Recommendations must be decision-ready.

| Field | Requirement |
|---|---|
| Finding | Patent/family, claim, issue, or report defect addressed |
| Action | Concrete next step, not a generic request to “review” |
| Priority | Critical, high, medium, or low with rationale |
| Owner | Legal, IP, R&D, product, procurement, business, or named role |
| Timing | Date, milestone, or event-relative deadline |
| Trigger | Fact or threshold that starts/escalates the action |
| Dependency | Evidence, counsel, design data, register extract, or negotiation |
| Decision | Launch, hold, redesign, licence, opinion, monitor, or accept |
| Residual risk | What remains after the action |

Typical options include claim-specific design-around, further status or file
history review, targeted validity research, non-infringement or invalidity
opinion, licence or acquisition analysis, supplier allocation, indemnity review,
customs/event protocol, pending-claim monitoring, and scheduled re-review.

## Harness consistency rules

Apply the source cross-field checks with localized, evidence-sensitive logic.

| Rule | Potential contradiction |
|---|---|
| LR-01 | High search-coverage score with only one unexplained source |
| LR-02 | High infringement-analysis score with no material patent analysis |
| LR-03 | High mitigation score with no actionable recommendation |
| LR-04 | Strong legal-status score with no status date or source |
| LR-05 | Full version-control/reproducibility score with missing queries |
| LR-06 | Excellent grade coexisting with a fatal defect |
| LR-07 | High validity-analysis score with no cited basis |
| LR-08 | Numeric recall claim with no estimator assumptions |
| LR-09 | Higher-risk patent with no linked response measure |
| LR-10 | Pending application presented as a currently enforceable claim |

The harness flags contradictions for human review. A flag is not itself a legal
conclusion.

## Scientific visual standard

The final HTML must be restrained, legible, and suitable for scientific and
legal review:

- use the fixed `assets/fto_report.css` stylesheet;
- use English labels and `lang="en"`;
- use semantic headings, tables, captions, and text labels;
- retain white space, navy/neutral tones, and accessible contrast;
- do not rely on color alone for grade, risk, priority, or pass/fail state;
- avoid ornamental gradients, oversized icons, novelty dashboards, or
  unsupported precision;
- make wide tables horizontally scrollable on screen and legible in print;
- include focus styles and reduced-motion behavior;
- do not use inline styles or client-side scripts in the stable output;
- embed the fixed CSS once so the report remains portable.

Required semantic classes include `card`, `verify`, `mitigation`, `chapter-no`,
`dim`, `bar`, `bar-fill`, grade/risk/percentage classes, `fatal-banner`,
priority classes, and `scene-badge`.

## Script usage

### Generate the report

```bash
python scripts/generate_report.py assessment.json fto-quality-assessment.html
```

Or generate an explicit evidence-gap skeleton:

```bash
python scripts/generate_report.py fto-quality-assessment.html
```

The second form must not be described as a completed assessment.

### Normalize independent-search results

```bash
python scripts/fto_independent_search.py normalized-routes.json comparison.json
```

Supply already retrieved route results. Review the input schema described by
the script before use.

### Validate the report

```bash
python scripts/validate_report.py fto-quality-assessment.html --out-dir validation
```

Optionally lock the reviewed stylesheet fingerprint:

```bash
python scripts/validate_report.py fto-quality-assessment.html \
  --expected-css-sha256 SHA256 --out-dir validation
```

Validation outputs are generated work products, not additional files in this
skill package.

## Quality-control checklist

Before delivery confirm:

- all supplied materials were inventoried;
- the target subject, product/process version, activity, and markets are clear;
- search and legal-status cutoffs are stated;
- family and result-count rules are stated;
- every score is evidence-backed;
- deductions and unresolved gaps are visible;
- fatal conditions were evaluated;
- independent routes are described accurately;
- observed overlap is not misrepresented as true recall;
- potentially material omissions received claim/status review;
- pending applications are in a separate watchlist;
- claim versions and translations are identified;
- conclusions are jurisdiction- and date-qualified;
- higher-risk findings have linked actions;
- recommendations name priority, owner, timing, and trigger;
- the HTML contains all sixteen sections;
- dynamic text is escaped and links are HTTP(S)-only;
- no secret, local absolute path, or Chinese-market-only link appears;
- the validator's fatal and error findings are resolved or expressly reported.

## Review boundary and disclaimer

This skill evaluates the quality of an existing FTO or patent-risk report and
may compare its search results with separately obtained patent data. Patent
coverage, claims, ownership, and legal status can change. Search databases have
jurisdictional, timing, translation, family, and indexing limitations. Any
conclusion must remain tied to the defined product or process, commercial
activity, jurisdiction, claim version, evidence, and review date.

The output is a quality assessment and decision-support work product. It is not
legal advice, does not guarantee freedom to operate, and should be reviewed by
qualified counsel before a material legal or commercial decision.

## Package files

- `assets/assessment-report-template.md` — complete assessment drafting model;
- `assets/fto_report.css` — fixed scientific/legal report styling;
- `assets/harness_report.css` — fixed validation-harness styling;
- `references/assessment-checklist.md` — detailed score and evidence checklist;
- `references/fto-quality-standards.md` — quality standards and interpretation;
- `references/harness-checks.md` — machine-check catalogue;
- `references/independent-verification-guide.md` — multi-route comparison guide;
- `scripts/fto_independent_search.py` — offline result normalization and overlap;
- `scripts/generate_report.py` — safe static HTML generator;
- `scripts/validate_report.py` — report and cross-field validation harness.

Marketplace reference:
[FTO Report Quality Review](https://open.patsnap.com/marketplace/skill-hub/fto-report-quality).

Global PatSnap links and connectors are listed in the MCP-assisted execution
section. The Chinese-source mapping remains in the localization index rather
than in the internationally distributed package.
