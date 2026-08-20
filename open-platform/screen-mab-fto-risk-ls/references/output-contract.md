# Output Contract — mAb FTO Risk Screen

## Required artifacts

Preserve the source artifact set. Create artifacts only as workflow outputs for a matter; these are not additional package files.

| Artifact | Purpose | Produced in |
|---|---|---|
| `tech_profile.md` | Versioned candidate, activities, markets, evidence, and gaps | Step 0 |
| `competitor_entity_map.md` | Verified competitor/related-entity graph | Step 3 |
| `patent_pool.json` | Deduplicated exact publications with all source routes | Steps 1–3 |
| `patent_pool_filtered.json` | Triage/status/jurisdiction-normalized record pool | Step 4 |
| `patent_pool_family.json` | Family/continuity containers with member-level evidence | Step 4 |
| `blocking_candidates.json` | Claims selected for detailed review | Step 5 |
| `claim_diff_matrix.md` | Claim-limitation-to-candidate evidence mapping | Step 6 |
| `risk_summary.json` | Jurisdiction/member/claim review priorities and actions | Step 6 |
| `sequence_alignment_log.md` | Reproducible sequence-query and alignment log | Step 1 |
| `fto_report.html` | Self-contained review report | Step 7 |

When a module is not applicable or cannot be executed, retain the expected artifact or report section with status, reason, effect, owner, and next action rather than fabricating results.

## Cross-artifact identifiers

Use stable identifiers:

- `matter_id`;
- `candidate_version`;
- `analysis_cutoff`;
- `query_id`;
- `publication_number` including country and kind code;
- `application_number` and `grant_number` where applicable;
- `family_group_id` plus family definition/provider;
- `member_id`;
- `claim_id` and `claim_version_id`;
- `limitation_id`;
- `candidate_feature_id`;
- `source_id`.

All counts in the report must reconcile to the JSON artifacts.

## Common metadata

Every artifact must state:

```json
{
  "schema_version": "1.0",
  "matter_id": "controlled-id",
  "candidate_version": "candidate-v3",
  "analysis_cutoff": "YYYY-MM-DD",
  "generated_at": "YYYY-MM-DDThh:mm:ssZ",
  "database_cutoffs": [],
  "jurisdictions": [],
  "planned_acts": [],
  "confidentiality": "...",
  "status": "complete|provisional|blocked|not_applicable",
  "known_gaps": [],
  "reviewer": "role or controlled identifier"
}
```

Use ISO dates and time zones. Do not embed credentials, privileged advice, or uncontrolled personal data.

## `tech_profile.md`

Required sections:

1. matter and decision;
2. candidate identity/version;
3. sequence inventory and numbering;
4. target/epitope/mechanism;
5. architecture, Fc, glycan, and modification;
6. ADC/conjugate features where applicable;
7. expression/manufacturing/purification/analytics;
8. formulation/presentation/delivery;
9. indication/population/regimen/combination;
10. planned acts, sites, countries, and dates;
11. owned/licensed rights and known competitors;
12. evidence ledger;
13. unknowns, assumptions, confidentiality, and gate decision.

Feature table:

| Feature ID | Dimension | Candidate value | Status | Source/version/locator | Confidentiality | Search modules |
|---|---|---|---|---|---|---|

## `competitor_entity_map.md`

Required sections:

- named competitors and assets;
- legal names and historical aliases;
- parents/subsidiaries/acquired or divested entities;
- licensors/licensees/co-developers/collaborators;
- contract manufacturers where process scope matters;
- relevant inventors;
- search-name set and filing-period logic;
- source/date/confidence for every relationship;
- unresolved ownership/license questions.

Relationship table:

| Entity ID | Legal name | Alias | Relationship | Effective period | Technology relevance | Source/date | Confidence |
|---|---|---|---|---|---|---|---|

Do not draw an ownership or license edge from brand association alone.

## `patent_pool.json`

One object per exact publication:

```json
{
  "publication_number": "US...A1",
  "application_number": "US...",
  "grant_number": null,
  "office": "US",
  "kind_code": "A1",
  "title": "...",
  "applicants": [],
  "assignees": [],
  "inventors": [],
  "priority_dates": [],
  "application_date": "YYYY-MM-DD",
  "publication_date": "YYYY-MM-DD",
  "source_modules": ["M1", "M2"],
  "source_routes": ["sequence", "claims_keyword"],
  "query_ids": [],
  "candidate_feature_ids": [],
  "sequence_hits": [],
  "structure_hits": [],
  "claim_text_status": "available|not_retrieved|unavailable",
  "sources": [],
  "retrieved_at": "YYYY-MM-DDThh:mm:ssZ"
}
```

Do not discard duplicate-route provenance when deduplicating publications.

## `patent_pool_filtered.json`

Extend each record with:

```json
{
  "target_jurisdiction_relevance": [],
  "status_normalized": "pending|granted_active|granted_inactive|unknown",
  "status_event": "...",
  "status_effective_date": "YYYY-MM-DD|null",
  "status_source": "...",
  "status_verified_at": "YYYY-MM-DDThh:mm:ssZ|null",
  "term_estimate": {},
  "triage_decision": "retain|monitor|exclude_from_claim_queue",
  "triage_reason_code": "...",
  "triage_evidence": [],
  "triage_reviewer": "...",
  "reopen_condition": "..."
}
```

An inactive record may be excluded from present claim comparison only after live branches, historical relevance, and status evidence are considered.

## `patent_pool_family.json`

Use the family model in `patent-family-merge.md`:

```json
{
  "family_group_id": "...",
  "family_definition": "INPADOC extended family",
  "family_provider": "Patsnap",
  "earliest_priority": {},
  "family_review_priority": "critical_review|high_review|monitor|low_current_relevance|resolved",
  "priority_rationale": "...",
  "target_jurisdictions": [],
  "representative_member_id": "...",
  "representative_reason": "navigation only",
  "members": [],
  "continuity_relations": [],
  "claim_versions": [],
  "source_modules": [],
  "known_gaps": [],
  "next_monitoring_event": null
}
```

Never store one representative claim as if it controls every jurisdiction.

## `blocking_candidates.json`

Use “blocking candidate” as a review-queue term, not a legal conclusion.

```json
{
  "candidate_id": "BC-001",
  "family_group_id": "...",
  "member_id": "...",
  "jurisdiction": "US",
  "planned_acts": ["make", "sell"],
  "status_and_term": {},
  "claim_version_id": "...",
  "claims_for_review": ["1", "18"],
  "candidate_feature_ids": [],
  "selection_basis": "...",
  "missing_evidence": [],
  "review_priority": "high_review",
  "sources": []
}
```

## `sequence_alignment_log.md`

Required sections:

- service/database/version/access date;
- confidentiality authorization;
- candidate sequence inventory/checksums;
- numbering/CDR method;
- query table with thresholds/filters;
- alignment result table;
- claim/disclosure/listing context;
- sensitivity tests;
- false-positive/false-negative review;
- unresolved access/coverage gaps.

Alignment table:

| Query ID | Region | Publication/SEQ ID | Identity | Coverage | Length/gaps | Claim context | Source/export | Review status |
|---|---|---|---:|---:|---|---|---|---|

No table column may call sequence identity a risk percentage.

## `claim_diff_matrix.md`

### Claim header

For every reviewed claim state:

- country/member and stable source link;
- legal-status event/source/retrieval date;
- claim number/type/dependency;
- claim-version event/date/source;
- original language and translation status;
- planned act and candidate version;
- claim-construction assumptions reserved for counsel.

### Limitation table

| Limitation ID | Claim excerpt and locator | Candidate feature/evidence | Literal mapping | Evidence status | Construction/equivalents issue | Next action |
|---|---|---|---|---|---|---|

Controlled mapping terms:

- `mapped`;
- `not mapped`;
- `uncertain`;
- `not assessed`;
- `candidate evidence missing`.

For dependent claims, include inherited limitations or point to the complete parent matrix plus added limitations. Do not skip a dependent claim merely because it refers to another claim.

### Claim conclusion

State:

- literal mapping status under identified assumptions;
- decisive mapped/unmapped/unknown limitations;
- open claim-construction and equivalents questions;
- status/term confidence;
- other relevant family members/claims;
- technical, evidence, monitoring, license, or counsel action.

Do not state “infringes” or “does not infringe” as the model's own legal conclusion.

## `risk_summary.json`

```json
{
  "matter_id": "...",
  "candidate_version": "...",
  "analysis_cutoff": "YYYY-MM-DD",
  "overall_status": "provisional_evidence_screen",
  "jurisdiction_summaries": [
    {
      "jurisdiction": "US",
      "planned_acts": [],
      "review_priority": "critical_review|high_review|monitor|low_current_relevance|resolved",
      "basis": "...",
      "material_candidates": [],
      "official_status_coverage": "complete|partial|missing",
      "claim_coverage": "complete|partial|missing",
      "known_gaps": [],
      "actions": []
    }
  ],
  "search_coverage": {},
  "limitations": [],
  "counsel_review_required": true
}
```

No infringement-probability thresholds such as 30%, 70%, “extreme,” or “safe” are permitted.

## HTML report: general requirements

`fto_report.html` must be:

- one self-contained HTML file with inline CSS and only necessary inline JavaScript;
- English by default, with original-language claim text retained where material;
- semantic, keyboard accessible, responsive, and printable;
- readable without JavaScript;
- free of external fonts, CDNs, analytics, network calls, and embedded credentials;
- restrained scientific/editorial design suitable for US/EU life-sciences and legal review;
- explicit about preliminary status, uncertainty, and counsel review.

## Scientific visual system

### Palette

Use a light neutral canvas and high-contrast text:

```css
:root {
  --canvas: #f7f8fa;
  --surface: #ffffff;
  --ink: #17212b;
  --muted: #55616f;
  --line: #d7dde4;
  --accent: #245f73;
  --accent-soft: #e8f1f4;
  --critical: #a33a32;
  --high: #9a5b19;
  --monitor: #5b5d88;
  --low: #426b55;
  --resolved: #56616c;
}
```

Color is secondary. Every status must include visible text and, where useful, an icon-independent pattern/border.

### Typography

Use system fonts:

```css
body {
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont,
               "Segoe UI", Arial, sans-serif;
  color: var(--ink);
  background: var(--canvas);
  line-height: 1.55;
}
code, pre, .sequence {
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
}
```

Do not fetch `Inter`; it is a preference if installed, with system fallback.

### Layout

- maximum reading width about 1180 px;
- 12-column grid only where it improves comparison;
- concise title block rather than a decorative full-screen cover;
- sticky table of contents only on sufficiently wide screens;
- white evidence sections with subtle borders, not floating dashboard cards everywhere;
- tables for exact mappings and timelines for prosecution/continuity;
- callouts only for decisions, limitations, and action items;
- no gradients, glow, particles, dark sci-fi styling, ticker, decorative animation, or emoji-dependent risk communication.

### Tables

- captions and `<thead>/<tbody>`;
- left-aligned text and tabular numeric data;
- repeated headers in print;
- horizontal wrapper or stacked record view on narrow screens;
- no hover-only information;
- source and uncertainty columns visible;
- blank, zero, not reported, unknown, and not applicable remain distinct.

### Interaction

Native `<details><summary>` is preferred for collapsible evidence. If JavaScript is used:

- report remains usable without it;
- controls are buttons with accessible names and `aria-expanded`;
- keyboard and focus states work;
- reduced-motion preference is respected;
- no content is loaded from the network.

## Patent links

Every displayed publication/patent number in the risk table, claim analysis, family view, and case appendix must be linked when a stable destination exists.

Link priority:

1. exact source-record URL returned by the global Patsnap MCP/API;
2. official patent-office/register record;
3. another verified stable public patent record.

Do not synthesize an undocumented Patsnap patent-detail URL. Do not use a legacy domestic product domain or a search URL that could resolve to the wrong record. Store:

```json
{
  "publication_number": "...",
  "record_url": "...",
  "url_source": "Patsnap MCP returned URL|official register",
  "verified_at": "YYYY-MM-DD"
}
```

HTML links opening a new tab must include `rel="noopener noreferrer"`.

## Seven report chapters

Preserve the source seven-chapter information architecture.

### 1. Candidate and matter overview

1.1 Candidate identity/version and molecule type  
1.2 Sequence/target/architecture/modification/ADC summary  
1.3 Planned acts, sites, markets, timing, and decision  
1.4 Analysis cutoff, sources, confidentiality, and release type  
1.5 Material input gaps and assumptions

### 2. FTO scope

2.1 Country-by-country scope; actual EP validated/unitary states  
2.2 Granted, pending, historical, and official-status treatment  
2.3 Product/process/use/formulation/supply-chain scope  
2.4 Family/continuity and counting rules  
2.5 Exclusions, database/language coverage, and blind periods

### 3. Search strategy and coverage

3.1 M1 sequence strategy, query versions, numbering, thresholds  
3.2 M1.5 modifications and structure strategy  
3.3 M2–M8 concept queries  
3.4 M9 entity/inventor/classification/family expansion  
3.5 Query history, languages, dates, databases, and filters  
3.6 Funnel: raw results, exact publications, families, retained members, reviewed claims  
3.7 Coverage matrix, diagnostic output, false-negative tests, and gaps

### 4. Priority patent/member list

Required columns:

| Family | Country/member | Status/source date | Owner | Priority/filing | Estimated/verified term | Material claims | Review priority | Evidence gap |
|---|---|---|---|---|---|---|---|---|

Sort by decision urgency, then jurisdiction and relevant date. A text status label is mandatory. Distinguish pending from granted, and estimated from verified term.

### 5. Claim-by-claim analysis

For every material member:

5.X.1 Bibliography, status, term, ownership, and source  
5.X.2 Family/continuity and relevant claim-version history  
5.X.3 Independent and material dependent claim identification  
5.X.4 Original claim text/short excerpt and translation status  
5.X.5 Limitation segmentation  
5.X.6 Candidate evidence mapping  
5.X.7 Literal mapping summary under stated assumptions  
5.X.8 Construction/equivalents/prosecution questions for counsel  
5.X.9 Next evidence, monitoring, engineering, license, or counsel action

Do not require full reproduction of every claim. Use precise excerpts and stable locators unless counsel requests the full text.

### 6. Conclusions and actions

6.1 Jurisdiction-by-jurisdiction review priority  
6.2 Decisive claims/features and unresolved facts  
6.3 Design-around hypotheses tied to limitations  
6.4 Licensing/ownership/settlement questions  
6.5 Evidence and official-register verification plan  
6.6 Monitoring plan for pending/unpublished/status events  
6.7 Counsel review questions  
6.8 Actions with owner and timing

Suggested timing bands should follow the actual decision date, not fixed 0–1/1–3/3–6 month boilerplate.

### 7. Appendices

Appendix A — jurisdiction-specific authority and legal questions  
Appendix B — verified relevant litigation/opposition/post-grant examples, if requested  
Appendix C — limitations and non-reliance statement  
Appendix D — search strings, classifications, query history, and coverage matrix  
Appendix E — family/continuity and status evidence  
Appendix F — sequence/structure logs and data dictionaries

Do not fabricate statutes, cases, holdings, or outcomes. Verify current authority for the analysis date and target country. Secondary case summaries are not a substitute for the decision.

## Claim identification

Identify claim dependency through both explicit references and claim structure. Common dependent markers such as “of claim 1” are useful, but not a complete parser for every jurisdiction/language.

Record:

```text
Claim 1 — independent composition claim
Claim 2 — depends from claim 1; adds sequence limitation
Claim 8 — independent method claim
Claim 12 — multiple dependent; dependency alternatives preserved
```

Review material dependent claims because they can add the feature that creates relevance. Do not apply the source rule that only independent claims may be analyzed.

## Translation

- preserve original-language claim text/source;
- label machine, database, analyst, or certified translation;
- do not silently improve or broaden technical/legal terminology;
- cite the original for material conclusions;
- obtain local patent-professional review where translation nuance matters.

## Limitation and non-reliance statement

Use a matter-specific statement containing at least:

- the report is a preliminary evidence-based screen, not legal advice or an infringement/validity opinion;
- conclusions apply only to the candidate version, acts, countries, dates, sources, and assumptions stated;
- patent databases and translations may be incomplete, delayed, or erroneous;
- applications, claims, ownership, legal status, term, and law can change;
- unpublished applications and non-indexed records create blind spots;
- official registers and primary documents control where they conflict;
- qualified counsel must evaluate claim construction, equivalents, defenses/exemptions, enforceability, validity, ownership/license scope, and litigation risk;
- monitoring is required through the relevant commercial date;
- confidential information must be handled under applicable controls.

Do not use a fixed “valid for six months” promise. State a recommended refresh event/cadence based on pending claims, launch timing, and status change risk.

## Print requirements

```css
@media print {
  @page { size: A4; margin: 14mm; }
  body { background: #fff; font-size: 10pt; }
  nav, .screen-only { display: none !important; }
  section, table, figure { break-inside: avoid; }
  h1, h2, h3 { break-after: avoid; }
  thead { display: table-header-group; }
  a[href]::after { content: " (" attr(href) ")"; font-size: 8pt; }
}
```

Prevent long URLs/sequences from overflowing. Do not hide sources in print.

## Accessibility checklist

- [ ] One `<h1>` and logical heading levels.
- [ ] Skip link and meaningful landmarks.
- [ ] Descriptive link text, not repeated “click here.”
- [ ] Table captions, scoped headers, and no layout tables.
- [ ] Status text independent of color/icons.
- [ ] Sufficient contrast and visible focus.
- [ ] Buttons are keyboard operable and expose state.
- [ ] Charts have data tables or text alternatives.
- [ ] Language attributes identify page and claim-language changes.
- [ ] No auto-playing or decorative motion.

## Data and legal QA

- [ ] Candidate version and analysis cutoff match every artifact.
- [ ] Planned acts and countries are explicit.
- [ ] Query/result/family/claim counts reconcile.
- [ ] All applicable M1–M9/M1.5 modules are complete or visibly waived.
- [ ] Sequence and structure queries preserve inputs, parameters, and exports.
- [ ] Every material claim has the controlling version/source or is marked missing.
- [ ] Independent and material dependent claims are covered.
- [ ] Member-level official status/term evidence supports priority labels.
- [ ] WO/PCT and EP territorial effects are not overstated.
- [ ] Multiple module hits and similarity do not become legal risk scores.
- [ ] Missing evidence remains unknown, not a negative fact.
- [ ] Patent links are exact, global/official, and verified.
- [ ] Authority/cases are current, accurate, and jurisdiction-specific.
- [ ] Design-around ideas map to claim limitations and validation needs.
- [ ] No credentials, fabricated evidence, or uncontrolled confidential data appear.

## Release decision

The report footer must state one release class:

- `Preliminary evidence screen — material gaps remain`;
- `Review-ready evidence screen — counsel review required`;
- `Monitoring update — scope unchanged except as stated`;
- `Counsel support package — no independent legal conclusion`.

It must also state generated date, analysis cutoff, database/official-register retrieval dates, candidate version, jurisdictions, and reviewer role.
